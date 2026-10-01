"""Build the DFI style sheet from tokens (1.2.16, 1.2.17, 1.2.19)."""

from __future__ import annotations

from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, RGBColor

from .tokens import Tokens, cm_to_twips

# Style names used by the block builders. Kept in one place so a future
# official NZDF_DSWT template (register T-03) can be mapped onto them.
BODY = "DFI Body"
BLOCK = "DFI Block"
MARKING = "DFI Marking"
ORIGINATOR = "DFI Originator"
IDENTIFIER = "DFI Identifier"
DIRECTIVE_ID = "DFI Directive Identifier"   # 3.2.11(4), 3.2.18(4), 3.2.22a(2)
SUBJECT = "DFI Subject Heading"
MAIN_HEADING = "DFI Main Heading"
GROUP_HEADING = "DFI Group Heading"
PARA = ["DFI Para 1", "DFI Para 2", "DFI Para 3", "DFI Para 4"]
PARA_UNNUMBERED = "DFI Para Unnumbered"
LIST_ITEM = "DFI List Item"
BULLET = "DFI Bullet"
TABLE_TEXT = "DFI Table Text"
TABLE_HEADER = "DFI Table Header"
TABLE_CAPTION = "DFI Table Caption"
# Styles that carry body text; hard-copy drafts double-space these only (1.2.22(3)).

SIGNATURE = "DFI Signature"
ANNEX_ID = "DFI Supporting Identifier"
FOOTNOTE_TEXT = "footnote text"        # Word built-in (styleId FootnoteText)
FOOTNOTE_REF = "footnote reference"   # Word built-in (styleId FootnoteReference)
LETTERHEAD = "DFI Letterhead Address"


def _set_rfonts(rpr_parent, family: str) -> None:
    rpr = rpr_parent.get_or_add_rPr() if hasattr(rpr_parent, "get_or_add_rPr") else rpr_parent
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.insert(0, rfonts)
    for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rfonts.set(qn(attr), family)
    for attr in ("w:asciiTheme", "w:hAnsiTheme", "w:cstheme", "w:eastAsiaTheme"):
        if rfonts.get(qn(attr)) is not None:
            del rfonts.attrib[qn(attr)]


def _set_lang(rpr, lang: str) -> None:
    el = rpr.find(qn("w:lang"))
    if el is None:
        el = OxmlElement("w:lang")
        rpr.append(el)
    el.set(qn("w:val"), lang)
    el.set(qn("w:eastAsia"), lang)
    el.set(qn("w:bidi"), "ar-SA")


def _doc_defaults(document, tk: Tokens) -> None:
    styles_el = document.styles.element
    defaults = styles_el.find(qn("w:docDefaults"))
    rpr_default = defaults.find(qn("w:rPrDefault"))
    rpr = rpr_default.find(qn("w:rPr"))
    _set_rfonts(rpr, tk.font_family)
    for tag in ("w:sz", "w:szCs"):
        el = rpr.find(qn(tag))
        if el is None:
            el = OxmlElement(tag)
            rpr.append(el)
        el.set(qn("w:val"), str(int(tk.size("body") * 2)))
    _set_lang(rpr, tk.value("page.language"))
    color = rpr.find(qn("w:color"))
    if color is None:
        color = OxmlElement("w:color")
        rpr.append(color)
    color.set(qn("w:val"), tk.value("font.colour"))


def _para_style(document, name: str, *, base: str | None = BODY, size=None, bold=None,
                italic=None, align=None, before=None, after=None, left_cm=None,
                hanging_cm=None, first_cm=None, keep_next=None, superscript=None):
    styles = document.styles
    try:
        st = styles[name]
    except KeyError:
        st = styles.add_style(name, WD_STYLE_TYPE.PARAGRAPH)
    if base and name != base:
        st.base_style = styles[base]
    st.quick_style = True
    f, pf = st.font, st.paragraph_format
    if size is not None:
        f.size = Pt(size)
    if bold is not None:
        f.bold = bold
    if italic is not None:
        f.italic = italic
    if superscript is not None:
        f.superscript = superscript
    if align is not None:
        pf.alignment = align
    if before is not None:
        pf.space_before = Pt(before)
    if after is not None:
        pf.space_after = Pt(after)
    if left_cm is not None:
        pf.left_indent = _cm(left_cm)
    if hanging_cm is not None:
        pf.first_line_indent = -_cm(hanging_cm)
    if first_cm is not None:
        pf.first_line_indent = _cm(first_cm)
    if keep_next is not None:
        pf.keep_with_next = keep_next
    return st


def _cm(cm: float):
    from docx.shared import Twips
    return Twips(cm_to_twips(cm))


def build(document, tk: Tokens) -> None:
    _doc_defaults(document, tk)
    family = tk.font_family

    normal = document.styles["Normal"]
    _set_rfonts(normal.element, family)
    normal.font.size = Pt(tk.size("body"))
    normal.font.color.rgb = RGBColor.from_string(tk.value("font.colour"))
    npf = normal.paragraph_format
    npf.alignment = WD_ALIGN_PARAGRAPH.LEFT  # 1.2.16(10)
    npf.line_spacing_rule = WD_LINE_SPACING.SINGLE  # 1.2.16(11)(f)
    before, after = tk.spacing("paragraph")
    npf.space_before, npf.space_after = Pt(before), Pt(after)
    npf.widow_control = True

    _para_style(document, BODY, base="Normal")
    _para_style(document, BLOCK, before=0, after=0)

    # Header and footer content: 12 pt, single spacing (1.2.16(4)(c), (11)(h)).
    for name in ("Header", "Footer"):
        st = document.styles[name]
        _set_rfonts(st.element, family)
        st.font.size = Pt(tk.size("header_footer"))
        st.paragraph_format.space_before = Pt(0)
        st.paragraph_format.space_after = Pt(0)
        st.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER

    pm = tk.get("font.size.protective_marking")
    _para_style(document, MARKING, base="Header", size=pm["value"], bold=pm["bold"],
                align=WD_ALIGN_PARAGRAPH.CENTER, before=0, after=0)

    od = tk.get("font.size.originator_descriptor")
    _para_style(document, ORIGINATOR, size=od["value"], bold=True,
                align=WD_ALIGN_PARAGRAPH.CENTER, before=0, after=0, keep_next=True)
    _para_style(document, IDENTIFIER, size=od["value"], bold=True,
                align=WD_ALIGN_PARAGRAPH.CENTER, before=6, after=0, keep_next=True)

    sb, sa = tk.spacing("subject_heading")
    _para_style(document, SUBJECT, bold=True, before=sb, after=sa, keep_next=True)
    mb, ma = tk.spacing("main_heading")
    _para_style(document, MAIN_HEADING, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER,
                before=mb, after=ma, keep_next=True)
    gb, ga = tk.spacing("group_heading")
    _para_style(document, GROUP_HEADING, bold=True, before=gb, after=ga, keep_next=True)

    _para_style(document, PARA_UNNUMBERED)
    for i, name in enumerate(PARA):
        _para_style(document, name)  # indents come from the numbering definition

    _para_style(document, BULLET)
    tb, ta = tk.spacing("table_cell")
    _para_style(document, TABLE_TEXT, size=tk.size("table_body"), before=tb, after=ta)      # 1.2.25c
    _para_style(document, TABLE_HEADER, base=TABLE_TEXT, size=tk.size("table_header"))       # 1.2.16(4)(b)
    _para_style(document, TABLE_CAPTION, size=tk.size("table_caption"),
                align=WD_ALIGN_PARAGRAPH.CENTER, before=12, after=3, keep_next=True)         # 1.2.25b
    _para_style(document, LIST_ITEM, before=0, after=0, left_cm=tk.tab_cm, hanging_cm=tk.tab_cm)  # [T] "A.<tab>"
    _para_style(document, SIGNATURE, before=0, after=0)
    _para_style(document, ANNEX_ID, bold=True, align=WD_ALIGN_PARAGRAPH.RIGHT, before=0, after=0)
    _para_style(document, LETTERHEAD, size=tk.size("letterhead_address"), before=0, after=0)

    fn = _para_style(document, FOOTNOTE_TEXT, base="Normal", size=tk.size("footnote"),
                     before=0, after=0)
    fn.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
    fn.element.set(qn("w:styleId"), "FootnoteText")
    try:
        ref = document.styles[FOOTNOTE_REF]
    except KeyError:
        ref = document.styles.add_style(FOOTNOTE_REF, WD_STYLE_TYPE.CHARACTER)
    ref.font.superscript = True
    ref.element.set(qn("w:styleId"), "FootnoteReference")


def style_id(document, name: str) -> str:
    return document.styles[name].style_id


BODY_TEXT_STYLES = [*PARA, PARA_UNNUMBERED, BULLET]


def ensure_directive_id(document, tk: Tokens) -> str:
    """Directive/AI identifier style, created on first use so that documents
    which do not use it are unchanged. Bold, left margin, immediately above the
    subject heading (3.2.11(4), 3.2.18(4), 3.2.22a(2)); spacing as the subject
    heading [T] Figs 3-5 to 3-7."""
    if DIRECTIVE_ID not in [st.name for st in document.styles]:
        sb, _ = tk.spacing("subject_heading")
        _para_style(document, DIRECTIVE_ID, bold=True, before=sb, after=0, keep_next=True)
    return DIRECTIVE_ID
