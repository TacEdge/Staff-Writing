"""Shared wording checks (register T-10: report as warnings, never rewrite).

Used by every correspondence schema so the rules live in one place.
"""

from __future__ import annotations

import re

from .inline import plain
from .model import ParaBlock, RecommendationsBlock


def text_warnings(texts, *, doc_name: str = "minutes") -> list[str]:
    w: list[str] = []
    for text in texts:
        t = plain(text or "")
        if re.search(r"https?://|www\.", t):
            w.append(f"Hyperlinks are not used in {doc_name} (Table 1-1): {t[:60]!r}")
        if "!" in t:
            w.append(f"Exclamation marks are not to be used (1.2.7(2)): {t[:60]!r}")
        if "—" in t:
            w.append(f"Em dash is not used in correspondence (1.2.7(10)(a); A-07): {t[:60]!r}")
        if re.search(r"\b\d+\s?%", t):
            w.append(f"Use 'per cent', not '%' (1.2.13(8)): {t[:60]!r}")
        if re.search(r"\b(e\.g\.|i\.e\.|etc\.)", t):
            w.append(f"No full stops in abbreviations: eg, ie, etc (1.2.7(5)): {t[:60]!r}")
    return w


def block_texts(blocks):
    for blk in blocks:
        if isinstance(blk, ParaBlock) or hasattr(blk, "para"):
            yield from para_texts(blk.para)
        elif isinstance(blk, RecommendationsBlock):
            yield blk.recommendations.lead
            yield from blk.recommendations.items
        elif hasattr(blk, "table"):
            for row in blk.table.rows:
                for cell in row:
                    yield cell.text
        else:
            yield getattr(blk, "group", None) or getattr(blk, "main", "")


def para_texts(p):
    if isinstance(p, str):
        yield p
        return
    if p.heading:
        yield p.heading
    yield p.text
    for s in p.sub:
        yield from para_texts(s)
    for b in p.bullets:
        if isinstance(b, str):
            yield b
        else:
            yield b.text
            yield from b.sub


def para_headings(blocks):
    """All paragraph headings at any level (for structural checks)."""
    def walk(p):
        if isinstance(p, str):
            return
        if p.heading:
            yield p.heading
        for s in p.sub:
            yield from walk(s)
    for blk in blocks:
        if isinstance(blk, ParaBlock):
            yield from walk(blk.para)


def standard_warnings(content, subject: str | None) -> list[str]:
    """Warnings every document type shares (single implementation)."""
    w: list[str] = []
    cn = getattr(content, "copy_number", None)
    if cn and not content.markings.above_restricted:
        w.append("Copy numbers are for documents classified above Restricted (1.2.16(9), Fig 1-4 fn 2).")
    if subject and subject != subject.upper():
        w.append("Subject heading supplied in mixed case; rendered in upper case (1.2.9(6)).")
    return w
