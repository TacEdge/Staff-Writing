"""Shared content rules for orders, directions and instructions (DFI 5.1
Part 3, Sections 5-8; 1.2.23): the Administrative Instruction, CDF Directive
(and its commander and senior-executive variants) and CDF Operational
Directive. The counterpart of `letters.py`.

Register decisions applied here: DR-04 (heading-only paragraphs are paragraph
headings), DR-06 (mandatory only where the prose requires; template-only
sections optional, with a warning when omitted), DR-08 (abbreviated dates in
text), DR-09 (day names).
"""

from __future__ import annotations

import re
from typing import Iterable, Optional, Union

from pydantic import model_validator

from . import dates
from .model import Addressee, DocDate, GroupHeading, Para, ParaBlock, Strict
from .wording import block_texts, para_texts, standard_warnings, text_warnings

# 3.2.11(3), 3.2.22a(1): more than four addressees -> a distribution list.
DISTRIBUTION_THRESHOLD = 4

Item = Union[str, Para]          # one author paragraph (with optional sub-paragraphs)


# --------------------------------------------------------------------- checks

def _walk(p):
    if isinstance(p, str):
        return
    yield p
    for s in p.sub:
        yield from _walk(s)


def paras_in(blocks: Iterable) -> Iterable[Para]:
    for blk in blocks:
        if isinstance(blk, (str, Para)):
            yield from _walk(blk)
        elif isinstance(blk, ParaBlock):
            yield from _walk(blk.para)


def check_no_bullets(blocks: Iterable, where: str) -> None:
    """1.2.23g: bulleted lists must not be used in orders, directions or
    instructions (every list component is numbered, 1.2.23f)."""
    for p in paras_in(blocks):
        if p.bullets:
            raise ValueError(f"{where}: bulleted lists must not be used in orders, directions or "
                             "instructions; number the items as sub-paragraphs (1.2.23f-g).")


def check_addressees(to: list[Addressee], distribution: list[str]) -> None:
    """3.2.11(3), 3.2.22a(1): more than four addressees -> a distribution list,
    which replaces the addressee lines ('See distribution', Figs 3-5, 3-7)."""
    if len(to) > DISTRIBUTION_THRESHOLD:
        raise ValueError(f"More than {DISTRIBUTION_THRESHOLD} addressees: a distribution list is to be "
                         "used (3.2.11(3), 3.2.22a(1)).")
    if to and distribution:
        raise ValueError("Give either addressees (four or fewer) or a distribution list, not both: "
                         "'See distribution' replaces the addressees (Figs 3-5, 3-7).")
    if not to and not distribution:
        raise ValueError("Give the addressees or a distribution list (3.2.11(3), 3.2.22a(1)).")


def check_stem_items(items: list[str], where: str) -> None:
    """Items completing a lead-in stem take their punctuation from the
    renderer (1.2.23b(1)): '; ' / '; and' / '.'."""
    for it in items:
        if it.rstrip().endswith((".", ";", ",", ":")):
            raise ValueError(f"{where}: give each item without closing punctuation; "
                             "it is added (1.2.23b(1)).")


def full_date(d: DocDate, where: str) -> DocDate:
    if d.day is None:
        raise ValueError(f"{where}: give the full date, including the day.")
    return d


# ------------------------------------------------------- shared sub-structures

class Administration(Strict):
    """'Administration' with Finance and Legal (Figs 3-5, 3-7) [T].
    Each is a heading-only paragraph with the author's sub-paragraphs (DR-04)."""

    finance: list[Item] = []
    legal: list[Item] = []


class CommandAndControl(Strict):
    """'Command and control' with Reporting, DIRLAUTH and Points of contact
    (Figs 3-5, 3-7) [T]."""

    reporting: list[Item] = []
    dirlauth: list[Item] = []
    points_of_contact: list[Item] = []


def heading_para(heading: str, items: list[Item]) -> ParaBlock:
    """'10. **Finance.**' then a., b. (DR-04: bold with a full stop, 1.2.17(4))."""
    return ParaBlock(para=Para(heading=heading, sub=list(items)))


def section(group: str, items: Iterable) -> list:
    """Group heading followed by first-level paragraphs (1.2.17(3))."""
    out: list = [GroupHeading(group=group)]
    for it in items:
        out.append(it if not isinstance(it, (str, Para)) else ParaBlock(para=it if isinstance(it, Para) else Para(text=it)))
    return out


def sub_sections(group: str, parts: list[tuple[str, list[Item]]], missing: list[str]) -> list:
    """A group of heading-only paragraphs; parts without content are omitted
    and named in `missing` (DR-06)."""
    present = [(h, items) for h, items in parts if items]
    for h, items in parts:
        if not items:
            missing.append(f"{group}: {h}")
    if not present:
        return []
    return [GroupHeading(group=group), *(heading_para(h, items) for h, items in present)]


def stem_para(stem: str, items: list[str]) -> ParaBlock:
    """'The purpose of this … is—' with lettered items (Figs 3-5, 3-7)."""
    return ParaBlock(para=Para(text=stem, sub=list(items), sentence_list="and"))


def date_in_text(d: DocDate) -> str:
    """DR-08: abbreviated date in the text, eg '2 Sep 26' (1.2.10b; A-01)."""
    return dates.abbreviated(d)


# ------------------------------------------------------------------- warnings

_DAY = r"\b(Mon|Tue|Wed|Thu|Fri|Sat|Sun)\b"
_MON = r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)"
_COMBINED = rf"{_DAY},\s\d{{1,2}}\s\d{{4}}\s{_MON}\s\d{{2}}\b"          # 1.2.10d
_MANDATORY = re.compile(r"\b(is to|are to|must|you are to|be prepared to|BPT|on order)\b", re.I)


def day_warnings(texts) -> list[str]:
    """DR-09: spell out the day in orders, directions and instructions
    (1.2.10a), except in the combined day-date-time form (1.2.10d)."""
    w = []
    for t in texts:
        rest = re.sub(_COMBINED, "", t or "")
        if re.search(_DAY, rest):
            w.append(f"Spell out the day in full in orders, directions and instructions, eg 'Tuesday' "
                     f"(1.2.10a); the abbreviated day is used only in the day-date-time form "
                     f"'Mon, 16 1300 Aug 21' (1.2.10d): {t[:60]!r}")
    return w


def lead_in_warnings(blocks) -> list[str]:
    """1.2.23c(2): a vertical list in orders and instructions is introduced
    with an em dash, not a colon."""
    return [f"Introduce a vertical list with an em dash in orders and instructions, not a colon "
            f"(1.2.23c(2)): {p.text[:60]!r}"
            for p in paras_in(blocks) if p.sub and p.text.rstrip().endswith(":")]


def mandatory_language_warning(blocks, where: str, rule: str) -> list[str]:
    texts = " ".join(t for t in block_texts(list(_as_blocks(blocks))) if t)
    if not _MANDATORY.search(texts):
        return [f"{where} should be written in mandatory language ('is to', 'are to', 'must', "
                f"'you are to', 'be prepared to', 'on order') ({rule}; 1.2.6)."]
    return []


def introduced_warnings(texts, annexes, enclosures) -> list[str]:
    """3.2.11(8), 3.2.18(8), 3.2.22a(8): annexes and enclosures must be
    introduced in the text."""
    body = " ".join(t for t in texts if t)
    w = []
    for i, _ in enumerate(annexes):
        letter = chr(ord("A") + i)
        if not re.search(rf"\bAnnex(es)?\b[^.]*?\b{letter}\b", body):
            w.append(f"Annex {letter} is not introduced in the text (3.2.11(8), 3.2.18(8), 3.2.22a(8)).")
    for i, _ in enumerate(enclosures):
        n = i + 1
        if not re.search(rf"\bEnclosures?\b[^.]*?\b{n}\b", body):
            w.append(f"Enclosure {n} is not introduced in the text (3.2.11(8), 3.2.18(8), 3.2.22a(8)).")
    return w


def omitted_warning(names: list[str], fig: str) -> list[str]:
    """DR-06: a template-only section that is omitted is reported, not required."""
    if not names:
        return []
    return [f"Omitted section(s) shown in {fig}: {', '.join(names)}. DFI prose does not make them "
            "mandatory; confirm they are not needed (register DR-06)."]


def _as_blocks(items):
    for it in items:
        if isinstance(it, (str, Para)):
            yield ParaBlock(para=it if isinstance(it, Para) else Para(text=it))
        else:
            yield it


def order_warnings(content, *, subject: Optional[str], blocks: list) -> list[str]:
    """Warnings shared by the family (T-10: reported, never rewritten)."""
    texts = list(block_texts(blocks))
    w = standard_warnings(content, subject)
    w += text_warnings([subject, *texts], doc_name="orders, directions and instructions", orders=True)
    w += day_warnings(texts)
    w += lead_in_warnings(blocks)
    w += introduced_warnings(texts, getattr(content, "annexes", []), getattr(content, "enclosures", []))
    return w
