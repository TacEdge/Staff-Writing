"""Low-level OOXML helpers for things python-docx does not expose.

Covers: tab stops, complex fields (PAGE, NUMPAGES, nested IF/SECTIONPAGES),
footnotes part, numbering definitions, page-number restarts, the DRAFT
watermark, and document settings (hyphenation, default tab, language).
"""

from __future__ import annotations

import copy

from docx.opc.constants import RELATIONSHIP_TYPE as RT
from docx.opc.packuri import PackURI
from docx.opc.part import Part
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
from docx.text.paragraph import Paragraph

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"


# ---------------------------------------------------------------- paragraphs

def add_tab(paragraph: Paragraph, pos_twips: int, align: str = "left") -> None:
    """Add a tab stop using python-docx's schema-order-aware API."""
    from docx.enum.text import WD_TAB_ALIGNMENT
    from docx.shared import Twips

    paragraph.paragraph_format.tab_stops.add_tab_stop(
        Twips(pos_twips), {"left": WD_TAB_ALIGNMENT.LEFT, "right": WD_TAB_ALIGNMENT.RIGHT,
                           "center": WD_TAB_ALIGNMENT.CENTER}[align]
    )


def set_num(paragraph: Paragraph, num_id: int, ilvl: int) -> None:
    """Attach list numbering (schema-order-aware via python-docx)."""
    numPr = paragraph._p.get_or_add_pPr().get_or_add_numPr()
    numPr.get_or_add_ilvl().val = ilvl
    numPr.get_or_add_numId().val = num_id


# -------------------------------------------------------------------- fields

def _fld_char(kind: str):
    el = OxmlElement("w:fldChar")
    el.set(qn("w:fldCharType"), kind)
    return el


def _run(rpr=None):
    r = OxmlElement("w:r")
    if rpr is not None:
        r.append(copy.deepcopy(rpr))
    return r


def field_runs(instr_parts, result_text: str = "1", rpr=None) -> list:
    """Return w:r elements for a complex field.

    instr_parts: list of str (instruction text) and lists (nested fields given as
    their own instr_parts lists) - lets us build { IF { SECTIONPAGES } > 1 ... }.
    """
    runs = []
    r = _run(rpr)
    r.append(_fld_char("begin"))
    runs.append(r)
    for part in instr_parts:
        if isinstance(part, list):
            runs.extend(field_runs(part, "1", rpr))
        else:
            r = _run(rpr)
            t = OxmlElement("w:instrText")
            t.set(qn("xml:space"), "preserve")
            t.text = part
            r.append(t)
            runs.append(r)
    r = _run(rpr)
    r.append(_fld_char("separate"))
    runs.append(r)
    r = _run(rpr)
    t = OxmlElement("w:t")
    t.set(qn("xml:space"), "preserve")
    t.text = result_text
    r.append(t)
    runs.append(r)
    r = _run(rpr)
    r.append(_fld_char("end"))
    runs.append(r)
    return runs


def append_field(paragraph: Paragraph, instr_parts, result_text: str = "1") -> None:
    for r in field_runs(instr_parts, result_text):
        paragraph._p.append(r)


# ------------------------------------------------------------------ settings

def apply_settings(document, default_tab_twips: int, language: str) -> None:
    settings = document.settings.element
    # Default tab stop interval (1.2.16(3)).
    tab = settings.find(qn("w:defaultTabStop"))
    if tab is None:
        tab = OxmlElement("w:defaultTabStop")
        settings.append(tab)
    tab.set(qn("w:val"), str(default_tab_twips))
    # Automatic hyphenation off (1.2.7(11)(b)): explicit element.
    hyph = settings.find(qn("w:autoHyphenation"))
    if hyph is None:
        hyph = OxmlElement("w:autoHyphenation")
        settings.append(hyph)
    hyph.set(qn("w:val"), "0")
    # No w:updateFields: it triggers an "update fields?" prompt on every open, and
    # Word recalculates PAGE/NUMPAGES/SECTIONPAGES in headers and footers anyway.
    _reorder_settings(settings)


# CT_Settings has a strict child order; Word rejects out-of-order elements.
_SETTINGS_ORDER = [
    "writeProtection", "view", "zoom", "removePersonalInformation", "removeDateAndTime",
    "doNotDisplayPageBoundaries", "displayBackgroundShape", "printPostScriptOverText",
    "printFractionalCharacterWidth", "printFormsData", "embedTrueTypeFonts",
    "embedSystemFonts", "saveSubsetFonts", "saveFormsData", "mirrorMargins",
    "alignBordersAndEdges", "bordersDoNotSurroundHeader", "bordersDoNotSurroundFooter",
    "gutterAtTop", "hideSpellingErrors", "hideGrammaticalErrors", "activeWritingStyle",
    "proofState", "formsDesign", "attachedTemplate", "linkStyles",
    "stylePaneFormatFilter", "stylePaneSortMethod", "documentType", "mailMerge",
    "revisionView", "trackRevisions", "doNotTrackMoves", "doNotTrackFormatting",
    "documentProtection", "autoFormatOverride", "styleLockTheme", "styleLockQFSet",
    "defaultTabStop", "autoHyphenation", "consecutiveHyphenLimit", "hyphenationZone",
    "doNotHyphenateCaps", "showEnvelope", "summaryLength", "clickAndTypeStyle",
    "defaultTableStyle", "evenAndOddHeaders", "bookFoldRevPrinting", "bookFoldPrinting",
    "bookFoldPrintingSheets", "drawingGridHorizontalSpacing",
    "drawingGridVerticalSpacing", "displayHorizontalDrawingGridEvery",
    "displayVerticalDrawingGridEvery", "doNotUseMarginsForDrawingGridOrigin",
    "drawingGridHorizontalOrigin", "drawingGridVerticalOrigin", "doNotShadeFormData",
    "noPunctuationKerning", "characterSpacingControl", "printTwoOnOne",
    "strictFirstAndLastChars", "noLineBreaksAfter", "noLineBreaksBefore", "savePreviewPicture",
    "doNotValidateAgainstSchema", "saveInvalidXml", "ignoreMixedContent",
    "alwaysShowPlaceholderText", "doNotDemarcateInvalidXml", "saveXmlDataOnly",
    "useXSLTWhenSaving", "saveThroughXslt", "showXMLTags", "alwaysMergeEmptyNamespace",
    "updateFields", "hdrShapeDefaults", "footnotePr", "endnotePr", "compat", "docVars",
    "rsids", "mathPr", "attachedSchema", "themeFontLang", "clrSchemeMapping",
    "doNotIncludeSubdocsInStats", "doNotAutoCompressPictures", "forceUpgrade",
    "captions", "readModeInkLockDown", "smartTagType", "schemaLibrary",
    "shapeDefaults", "doNotEmbedSmartTags", "decimalSymbol", "listSeparator",
]


def _reorder_settings(settings) -> None:
    order = {name: i for i, name in enumerate(_SETTINGS_ORDER)}
    children = list(settings)

    def key(el):
        local = el.tag.split("}")[-1]
        return order.get(local, len(order))

    for el in children:
        settings.remove(el)
    for el in sorted(children, key=key):
        settings.append(el)


# ----------------------------------------------------------------- footnotes

FOOTNOTES_CT = "application/vnd.openxmlformats-officedocument.wordprocessingml.footnotes+xml"


class Footnotes:
    """Creates /word/footnotes.xml and adds real Word footnotes (1.2.19b)."""

    def __init__(self, document):
        self.document = document
        self.next_id = 1
        xml = (
            f'<w:footnotes {nsdecls("w")}>'
            '<w:footnote w:type="separator" w:id="-1"><w:p><w:pPr><w:spacing w:before="0" w:after="0" w:line="240" w:lineRule="auto"/></w:pPr>'
            '<w:r><w:separator/></w:r></w:p></w:footnote>'
            '<w:footnote w:type="continuationSeparator" w:id="0"><w:p><w:pPr><w:spacing w:before="0" w:after="0" w:line="240" w:lineRule="auto"/></w:pPr>'
            '<w:r><w:continuationSeparator/></w:r></w:p></w:footnote>'
            "</w:footnotes>"
        )
        self.element = parse_xml(xml)
        self.part = None

    def _ensure_part(self):
        if self.part is not None:
            return
        doc_part = self.document.part
        self.part = Part(PackURI("/word/footnotes.xml"), FOOTNOTES_CT, b"", doc_part.package)
        doc_part.relate_to(self.part, RT.FOOTNOTES)
        settings = self.document.settings.element
        fpr = parse_xml(
            f'<w:footnotePr {nsdecls("w")}><w:footnote w:id="-1"/><w:footnote w:id="0"/></w:footnotePr>'
        )
        settings.append(fpr)
        _reorder_settings(settings)

    def add(self, run_parent_p, style_text: str, style_ref: str) -> Paragraph:
        """Insert a footnote reference at the end of run_parent_p (a CT_P).

        Returns a Paragraph inside the footnote body to receive the text runs.
        """
        self._ensure_part()
        fid = self.next_id
        self.next_id += 1
        # Reference in body.
        ref_run = parse_xml(
            f'<w:r {nsdecls("w")}><w:rPr><w:rStyle w:val="{style_ref}"/><w:vertAlign w:val="superscript"/></w:rPr>'
            f'<w:footnoteReference w:id="{fid}"/></w:r>'
        )
        run_parent_p.append(ref_run)
        # Footnote body: mark + space + text.
        fn = parse_xml(
            f'<w:footnote {nsdecls("w")} w:id="{fid}"><w:p><w:pPr><w:pStyle w:val="{style_text}"/></w:pPr>'
            f'<w:r><w:rPr><w:rStyle w:val="{style_ref}"/><w:vertAlign w:val="superscript"/></w:rPr><w:footnoteRef/></w:r>'
            '<w:r><w:t xml:space="preserve"> </w:t></w:r></w:p></w:footnote>'
        )
        self.element.append(fn)
        return Paragraph(fn[0], None)

    def finalise(self):
        if self.part is not None:
            from lxml import etree

            # Generic python-docx Part serialises its _blob verbatim.
            self.part._blob = etree.tostring(  # type: ignore[attr-defined]
                self.element, xml_declaration=True, encoding="UTF-8", standalone=True
            )


# ------------------------------------------------------------------ sections

def set_page_number_start(section, start: int | None, fmt: str | None = None) -> None:
    sectPr = section._sectPr
    pg = sectPr.find(qn("w:pgNumType"))
    if pg is None:
        pg = OxmlElement("w:pgNumType")
        # pgNumType sits after pgMar/paperSrc/pgBorders/lnNumType; append before cols.
        cols = sectPr.find(qn("w:cols"))
        if cols is not None:
            cols.addprevious(pg)
        else:
            sectPr.append(pg)
    if start is not None:
        pg.set(qn("w:start"), str(start))
    if fmt is not None:
        pg.set(qn("w:fmt"), fmt)


# ----------------------------------------------------------------- watermark

def watermark_run(text: str):
    """VML text watermark as produced by Word's Design > Watermark (1.2.22(1))."""
    xml = (
        f'<w:r {nsdecls("w")} xmlns:v="urn:schemas-microsoft-com:vml" '
        'xmlns:o="urn:schemas-microsoft-com:office:office"><w:pict>'
        '<v:shapetype id="_x0000_t136" coordsize="21600,21600" o:spt="136" adj="10800" '
        'path="m@7,l@8,m@5,21600l@6,21600e">'
        '<v:formulas><v:f eqn="sum #0 0 10800"/><v:f eqn="prod #0 2 1"/><v:f eqn="sum 21600 0 @1"/>'
        '<v:f eqn="sum 0 0 @2"/><v:f eqn="sum 21600 0 @3"/><v:f eqn="if @0 @3 0"/>'
        '<v:f eqn="if @0 21600 @1"/><v:f eqn="if @0 0 @2"/><v:f eqn="if @0 @4 21600"/>'
        '<v:f eqn="mid @5 @6"/><v:f eqn="mid @8 @5"/><v:f eqn="mid @7 @8"/><v:f eqn="mid @6 @7"/>'
        '<v:f eqn="sum @6 0 @5"/></v:formulas>'
        '<v:path textpathok="t" o:connecttype="custom" '
        'o:connectlocs="@9,0;@10,10800;@11,21600;@12,10800" o:connectangles="270,180,90,0"/>'
        '<v:textpath on="t" fitshape="t"/><o:lock v:ext="edit" text="t" shapetype="t"/></v:shapetype>'
        '<v:shape id="PowerPlusWaterMarkObject" o:spid="_x0000_s2049" type="#_x0000_t136" '
        'style="position:absolute;margin-left:0;margin-top:0;width:415pt;height:166pt;'
        'rotation:315;z-index:-251657216;mso-position-horizontal:center;'
        'mso-position-horizontal-relative:margin;mso-position-vertical:center;'
        'mso-position-vertical-relative:margin" o:allowincell="f" fillcolor="silver" stroked="f">'
        '<v:fill opacity=".5"/>'
        f'<v:textpath style="font-family:&quot;Calibri&quot;;font-size:1pt" string="{text}"/>'
        '<w10:wrap anchorx="margin" anchory="margin" xmlns:w10="urn:schemas-microsoft-com:office:word"/>'
        "</v:shape></w:pict></w:r>"
    )
    return parse_xml(xml)
