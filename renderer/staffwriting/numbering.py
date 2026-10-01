"""Word numbering definitions built from the token numbering schemes.

Scheme C (correspondence), D (directive) and the simple list schemes
(references A., annex list A., enclosure list 1.) are generated from
standards/spec/dfi-5.1-tokens.yaml `numbering.*`.
"""

from __future__ import annotations

from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls, qn

from .tokens import Tokens, cm_to_twips

_STYLE_TO_FMT = {
    None: "decimal",
    "decimal": "decimal",
    "lowerLetter": "lowerLetter",
    "upperLetter": "upperLetter",
    "lowerRoman": "lowerRoman",
    "upperRoman": "upperRoman",
}


def _lvl_xml(ilvl: int, fmt: str, text: str, label_cm: float, text_cm: float, wrap_cm: float) -> str:
    left = cm_to_twips(wrap_cm)
    first = cm_to_twips(label_cm) - left  # negative = hanging
    ind = f'w:left="{left}" ' + (f'w:hanging="{-first}"' if first < 0 else f'w:firstLine="{first}"')
    return (
        f'<w:lvl w:ilvl="{ilvl}"><w:start w:val="1"/><w:numFmt w:val="{fmt}"/>'
        f'<w:lvlText w:val="{text}"/><w:lvlJc w:val="left"/>'
        f'<w:pPr><w:tabs><w:tab w:val="num" w:pos="{cm_to_twips(text_cm)}"/></w:tabs>'
        f"<w:ind {ind}/></w:pPr>"
        '<w:rPr><w:b w:val="0"/><w:i w:val="0"/></w:rPr></w:lvl>'
    )


class Numbering:
    def __init__(self, document, tk: Tokens):
        self.tk = tk
        self.root = document.part.numbering_part.element
        self._abstract: dict[str, int] = {}
        existing_abs = [int(a.get(qn("w:abstractNumId"))) for a in self.root.findall(qn("w:abstractNum"))]
        existing_num = [int(n.get(qn("w:numId"))) for n in self.root.findall(qn("w:num"))]
        self._next_abs = max(existing_abs, default=-1) + 1
        self._next_num = max(existing_num, default=0) + 1

    # -- definitions -------------------------------------------------------
    def _add_abstract(self, key: str, levels: list[dict]) -> int:
        aid = self._next_abs
        self._next_abs += 1
        lvls = []
        for i, lv in enumerate(levels):
            fmt = _STYLE_TO_FMT[lv.get("style")]
            text = _level_text(lv["fmt"], i)
            lvls.append(_lvl_xml(i, fmt, text, lv["indent"], lv["text"], lv["wrap"]))
        xml = (
            f'<w:abstractNum {nsdecls("w")} w:abstractNumId="{aid}">'
            '<w:multiLevelType w:val="multilevel"/>' + "".join(lvls) + "</w:abstractNum>"
        )
        el = parse_xml(xml)
        first_num = self.root.find(qn("w:num"))
        if first_num is not None:
            first_num.addprevious(el)
        else:
            self.root.append(el)
        self._abstract[key] = aid
        return aid

    def abstract(self, scheme: str) -> int:
        """scheme: 'correspondence' | 'directive' | 'references' | 'annex_list' | 'enclosure_list' | 'flag_list'."""
        if scheme in self._abstract:
            return self._abstract[scheme]
        node = self.tk.get(f"numbering.{scheme}")
        if "levels" in node:
            levels = node["levels"]
        else:  # single-level list schemes
            levels = [{"fmt": node["fmt"], "style": node.get("style"), "indent": 0, "text": 1, "wrap": 1}]
        return self._add_abstract(scheme, levels)

    def bullets(self) -> int:
        """Bullet definition from tokens.bullets (1.2.23g(1), Fig 1-4 para 7)."""
        if "bullets" in self._abstract:
            return self._abstract["bullets"]
        aid = self._next_abs
        self._next_abs += 1
        lvls = []
        for i, key in enumerate(("level1", "level2")):
            node = self.tk.get(f"bullets.{key}")
            label = cm_to_twips(node["label_indent"])
            text = label + cm_to_twips(1.0)
            lvls.append(
                f'<w:lvl w:ilvl="{i}"><w:start w:val="1"/><w:numFmt w:val="bullet"/>'
                f'<w:lvlText w:val="{node["symbol"]}"/><w:lvlJc w:val="left"/>'
                f'<w:pPr><w:tabs><w:tab w:val="num" w:pos="{text}"/></w:tabs>'
                f'<w:ind w:left="{text}" w:hanging="{text - label}"/></w:pPr>'
                f'<w:rPr><w:rFonts w:ascii="{node["font"]}" w:hAnsi="{node["font"]}" w:hint="default"/></w:rPr></w:lvl>'
            )
        el = parse_xml(f'<w:abstractNum {nsdecls("w")} w:abstractNumId="{aid}">'
                       '<w:multiLevelType w:val="hybridMultilevel"/>' + "".join(lvls) + "</w:abstractNum>")
        first_num = self.root.find(qn("w:num"))
        if first_num is not None:
            first_num.addprevious(el)
        else:
            self.root.append(el)
        self._abstract["bullets"] = aid
        return aid

    def bullet_instance(self) -> int:
        aid = self.bullets()
        nid = self._next_num
        self._next_num += 1
        self.root.append(parse_xml(f'<w:num {nsdecls("w")} w:numId="{nid}"><w:abstractNumId w:val="{aid}"/></w:num>'))
        return nid

    # -- instances ---------------------------------------------------------
    def instance(self, scheme: str) -> int:
        """A new numbering instance that restarts at 1 (eg each annex body)."""
        aid = self.abstract(scheme)
        nid = self._next_num
        self._next_num += 1
        xml = (
            f'<w:num {nsdecls("w")} w:numId="{nid}"><w:abstractNumId w:val="{aid}"/>'
            '<w:lvlOverride w:ilvl="0"><w:startOverride w:val="1"/></w:lvlOverride></w:num>'
        )
        self.root.append(parse_xml(xml))
        return nid


def _level_text(fmt: str, ilvl: int) -> str:
    """Token formats use %1..%n per level position; normalise to this level."""
    import re

    return re.sub(r"%\d", f"%{ilvl + 1}", fmt)
