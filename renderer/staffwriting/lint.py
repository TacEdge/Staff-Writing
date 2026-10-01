"""Post-render structural lint (docs/architecture.md section 6).

Checks the .docx itself (and, when given, its PDF preview) against the tokens.
Returns a list of (level, message) where level is ERROR or WARN.
"""

from __future__ import annotations

import re
import subprocess
import zipfile
from pathlib import Path

from docx import Document
from docx.oxml.ns import qn

from . import styles as S
from .tokens import load

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
MARKING_WORDS = {"UNCLASSIFIED", "RESTRICTED", "CONFIDENTIAL", "SECRET", "TOP SECRET",
                 "IN-CONFIDENCE", "SENSITIVE", "STAFF-IN-CONFIDENCE"}


def _xml(docx: Path, name: str):
    from lxml import etree
    with zipfile.ZipFile(docx) as z:
        if name not in z.namelist():
            return None
        return etree.fromstring(z.read(name))


def lint(docx: Path, pdf: Path | None = None, *, doc_type: str = "minute",
         max_main_pages: int | None = None, margins: str = "standard") -> list[tuple[str, str]]:
    tk = load()
    out: list[tuple[str, str]] = []
    err = lambda m: out.append(("ERROR", m))  # noqa: E731
    warn = lambda m: out.append(("WARN", m))  # noqa: E731
    d = Document(str(docx))

    # -- page setup (1.2.16(1)-(2)) --------------------------------------
    m = tk.margins(margins)
    for i, s in enumerate(d.sections):
        w, h = round(s.page_width.cm, 1), round(s.page_height.cm, 1)
        if sorted((w, h)) != [21.0, 29.7]:
            err(f"Section {i + 1}: page is {w} x {h} cm, not A4 (1.2.16(1)).")
        for side in ("top", "bottom", "left", "right"):
            got = round(getattr(s, f"{side}_margin").cm, 2)
            if abs(got - m[side]) > 0.01:
                err(f"Section {i + 1}: {side} margin {got} cm, expected {m[side]} cm (1.2.16(2)).")
        for kind in ("header", "footer"):
            got = round(getattr(s, f"{kind}_distance").cm, 2)
            if abs(got - 1.0) > 0.01:
                err(f"Section {i + 1}: {kind} distance {got} cm, expected 1 cm (1.2.16(2)).")

    # -- fonts, sizes, colour (1.2.16(4)) --------------------------------
    styles_xml = _xml(docx, "word/styles.xml")
    rfonts = styles_xml.find(f"{W}docDefaults/{W}rPrDefault/{W}rPr/{W}rFonts")
    if rfonts is None or rfonts.get(f"{W}ascii") != tk.font_family:
        err("Document default font is not Calibri (1.2.16(4)).")
    lang = styles_xml.find(f"{W}docDefaults/{W}rPrDefault/{W}rPr/{W}lang")
    if lang is None or lang.get(f"{W}val") != "en-NZ":
        err("Default proofing language is not en-NZ (1.2.5b).")
    expected_sizes = {
        "Normal": tk.size("body"), S.BODY: tk.size("body"), S.SUBJECT: tk.size("heading"),
        S.GROUP_HEADING: tk.size("heading"), S.MAIN_HEADING: tk.size("heading"),
        S.MARKING: tk.size("protective_marking"), S.FOOTNOTE_TEXT: tk.size("footnote"),
    }
    for name, pt in expected_sizes.items():
        st = d.styles[name]
        size = _effective_size(st)
        if size is not None and abs(size - pt) > 0.01:
            err(f"Style '{name}' is {size} pt, expected {pt} pt.")
    doc_xml = _xml(docx, "word/document.xml")
    for part in _content_parts(docx):
        root = _xml(docx, part)
        for rf in root.iter(f"{W}rFonts"):
            fam = rf.get(f"{W}ascii")
            if fam and fam != tk.font_family:
                err(f"{part}: run font '{fam}' is not Calibri (1.2.16(4)).")
        for c in root.iter(f"{W}color"):
            if c.get(f"{W}val") not in ("000000", "auto", None):
                err(f"{part}: coloured text ({c.get(W + 'val')}) is not permitted here (1.2.16(4)).")
        if root.find(f".//{W}hyperlink") is not None and doc_type in ("minute", "submission", "letter"):
            err(f"{part}: hyperlinks are not used in minutes or letters (Table 1-1).")

    # -- settings ------------------------------------------------------------
    settings = _xml(docx, "word/settings.xml")
    hy = settings.find(f"{W}autoHyphenation")
    if hy is not None and hy.get(f"{W}val") not in ("0", "false"):
        err("Automatic hyphenation is on (1.2.7(11)(b)).")
    tab = settings.find(f"{W}defaultTabStop")
    if tab is None or abs(int(tab.get(f"{W}val")) - 567) > 1:
        err("Default tab stop is not 1 cm (1.2.16(3)).")

    # -- markings in every header/footer (1.2.16(5), 1.2.18) -----------------
    header_sets, footer_sets = [], []
    for i, s in enumerate(d.sections):
        variants = [("default", s.header, s.footer)]
        if s.different_first_page_header_footer:
            variants.append(("first", s.first_page_header, s.first_page_footer))
        for label, hdr, ftr in variants:
            h = [p.text.strip() for p in hdr.paragraphs if p.text.strip() in MARKING_WORDS]
            f = [p.text.strip() for p in ftr.paragraphs if p.text.strip() in MARKING_WORDS]
            header_sets.append(tuple(h))
            footer_sets.append(tuple(f))
            if list(reversed(h)) != f:
                err(f"Section {i + 1} {label}: footer markings {f} do not mirror header {h} (1.2.18c).")
            if f and ftr.paragraphs[-1].text.strip() != f[-1]:
                err(f"Section {i + 1} {label}: classification is not the last footer line (1.2.16(5)).")
            for p in hdr.paragraphs + ftr.paragraphs:
                if p.text.strip() in MARKING_WORDS:
                    if not all(r.bold or r.bold is None and _style_bold(p) for r in p.runs):
                        err(f"Marking '{p.text.strip()}' is not bold (1.2.16(5)).")
    if len(set(header_sets)) > 1:
        err(f"Markings differ between pages/sections: {sorted(set(header_sets))} (1.2.16(5)).")

    # -- page numbering (1.2.16(6)-(7)) -------------------------------------
    s0 = d.sections[0]
    classified = any(x in ("CONFIDENTIAL", "SECRET", "TOP SECRET") for x in (header_sets[0] if header_sets else ()))
    if not classified:
        if not s0.different_first_page_header_footer:
            err("First page is numbered on an unclassified/restricted document (1.2.16(6)).")
        elif "PAGE" in _instr(s0.first_page_footer):
            err("First-page footer contains a page number (1.2.16(6)).")
        if "PAGE" not in _instr(s0.footer):
            err("Continuation pages have no page number (1.2.16(6), 2.1.11(18)).")
    else:
        for i, s in enumerate(d.sections):
            if "NUMPAGES" not in _instr(s.footer):
                err(f"Section {i + 1}: classified document lacks 'Page n of N' (1.2.16(7)).")

    # -- subject heading (1.2.17(1)) ----------------------------------------
    for p in d.paragraphs:
        if p.style.name == S.SUBJECT and p.text != p.text.upper():
            err(f"Subject heading not in upper case: {p.text!r} (1.2.9(6)).")

    # -- numbering scheme C geometry (2.1.3(3)) ------------------------------
    num_xml = _xml(docx, "word/numbering.xml")
    expected = tk.get("numbering.correspondence.levels")
    for absn in num_xml.findall(f"{W}abstractNum"):
        lvls = absn.findall(f"{W}lvl")
        if len(lvls) == 4 and lvls[0].find(f"{W}lvlText").get(f"{W}val") == "%1.":
            for lv, exp in zip(lvls, expected):
                ind = lv.find(f"{W}pPr/{W}ind")
                left = int(ind.get(f"{W}left"))
                if abs(left - round(exp["wrap"] * 566.929)) > 2:
                    err(f"Numbering level {lv.get(W + 'ilvl')} turnover at {left} twips, expected {exp['wrap']} cm.")

    # -- OOXML child order (Word rejects out-of-order elements) ------------------
    for e in xml_order_errors(docx):
        err(e)

    # -- PDF checks ------------------------------------------------------------
    if pdf is not None and Path(pdf).exists():
        out.extend(_pdf_checks(Path(pdf), header_sets[0] if header_sets else ()))
        if max_main_pages:
            pages = _pdf_pages(Path(pdf))
            main = next((i for i, pg in enumerate(pages)
                         if re.search(r"^\s{20,}(ANNEX|APPENDIX) ", pg, re.M)), len(pages))
            if main > max_main_pages:
                warn(f"Main document is {main} pages; ideally no longer than {max_main_pages} "
                     "(2.1.12b(6)). Consider moving detail to annexes.")
    return out


def _effective_size(style):
    st = style
    while st is not None:
        if st.font.size is not None:
            return st.font.size.pt
        st = st.base_style
    return None


def _style_bold(p):
    st = p.style
    while st is not None:
        if st.font.bold is not None:
            return st.font.bold
        st = st.base_style
    return False


def _instr(hf) -> str:
    return " ".join(t.text or "" for t in hf._element.iter(qn("w:instrText")))


def _content_parts(docx: Path) -> list[str]:
    with zipfile.ZipFile(docx) as z:
        return [n for n in z.namelist() if re.fullmatch(r"word/(document|header\d+|footer\d+|footnotes)\.xml", n)]


def _pdf_pages(pdf: Path) -> list[str]:
    txt = subprocess.run(["pdftotext", "-layout", str(pdf), "-"], capture_output=True, text=True, check=True).stdout
    return txt.split("\f")[:-1] if txt.endswith("\f") else txt.split("\f")


def _pdf_checks(pdf: Path, markings: tuple) -> list[tuple[str, str]]:
    out = []
    pages = _pdf_pages(pdf)
    for n, page in enumerate(pages, start=1):
        lines = [l.strip() for l in page.splitlines() if l.strip()]
        if markings:
            if not lines or lines[0] != markings[0]:
                out.append(("ERROR", f"PDF page {n}: first line is not the classification {markings[0]!r} (1.2.16(5))."))
            if not lines or lines[-1] != markings[0]:
                out.append(("ERROR", f"PDF page {n}: last line is not the classification {markings[0]!r} (1.2.16(5))."))
    # Signature orphan rule (1.2.21c): find the bold name line = first line that is
    # all capitals followed within 6 lines by blank gap; approximate via the block
    # that follows six empty lines. We check that the page holding the signature
    # has at least two non-marking text lines before it.
    for n, page in enumerate(pages, start=1):
        raw = page.splitlines()
        for i in range(6, len(raw)):
            if raw[i].strip() and re.fullmatch(r"[A-Z]{1,5} [A-Z][A-Z'\-]+", raw[i].strip()) and \
               all(not x.strip() for x in raw[max(0, i - 4):i]):
                above = [l for l in raw[:i] if l.strip() and l.strip() not in MARKING_WORDS
                         and not re.fullmatch(r"Copy \d+ of \d+", l.strip())]
                if len(above) < 2:
                    out.append(("ERROR", f"PDF page {n}: signature block has fewer than two lines of text above it (1.2.21c)."))
    return out


# ---------------------------------------------------------------- XML order
# Child order required by the OOXML schema (CT_PPr, CT_RPr subsets we emit).
_PPR_ORDER = ["pStyle", "keepNext", "keepLines", "pageBreakBefore", "framePr", "widowControl",
              "numPr", "suppressLineNumbers", "pBdr", "shd", "tabs", "suppressAutoHyphens",
              "kinsoku", "wordWrap", "overflowPunct", "topLinePunct", "autoSpaceDE", "autoSpaceDN",
              "bidi", "adjustRightInd", "snapToGrid", "spacing", "ind", "contextualSpacing",
              "mirrorIndents", "suppressOverlap", "jc", "textDirection", "textAlignment",
              "textboxTightWrap", "outlineLvl", "divId", "cnfStyle", "rPr", "sectPr", "pPrChange"]
_SECT_ORDER = ["headerReference", "footerReference", "footnotePr", "endnotePr", "type", "pgSz",
               "pgMar", "paperSrc", "pgBorders", "lnNumType", "pgNumType", "cols", "formProt",
               "vAlign", "noEndnote", "titlePg", "textDirection", "bidi", "rtlGutter", "docGrid",
               "printerSettings", "sectPrChange"]


def xml_order_errors(docx: Path) -> list[str]:
    errs = []
    for part in _content_parts(docx) + ["word/styles.xml", "word/numbering.xml"]:
        root = _xml(docx, part)
        for tag, order in (("pPr", _PPR_ORDER), ("sectPr", _SECT_ORDER)):
            rank = {n: i for i, n in enumerate(order)}
            if tag == "sectPr":  # EG_HdrFtrReferences is a repeating choice: any interleave
                rank["footerReference"] = rank["headerReference"]
            for el in root.iter(f"{W}{tag}"):
                seq = [rank.get(c.tag.split("}")[-1], -1) for c in el]
                seq = [x for x in seq if x >= 0]
                if seq != sorted(seq):
                    errs.append(f"{part}: <w:{tag}> children out of schema order: "
                                f"{[c.tag.split('}')[-1] for c in el]}")
                    break
    return errs
