"""Content schema for the Dot-point brief (DFI 5.1 2.2.6-2.2.8; Annex 2O).

A DPB informs; it may offer an opinion but does not seek a decision (2.2.6).
"""

from __future__ import annotations

import re
from typing import Literal, Optional, Union

from pydantic import Field, model_validator

from staffwriting.model import (
    Annex, CopyNumber, DocDate, GroupHeading, MainHeading, Markings, ParaBlock,
    RecommendationsBlock, Signature, Strict,
)
from staffwriting.wording import block_texts, standard_warnings, text_warnings

# Recommendations are deliberately excluded: a DPB does not seek a decision (2.2.6).
DpbBlock = Union[GroupHeading, MainHeading, ParaBlock]


class Content(Strict):
    type: Literal["dpb"]
    markings: Markings = Markings()
    copy_number: Optional[CopyNumber] = None
    draft: Optional[Literal["electronic", "hardcopy"]] = None
    margins: Literal["standard", "brief"] = "standard"   # 4 cm right margin option (2.2.7(1))

    date: DocDate                                       # 2.2.3(1)
    file_reference: Optional[str] = None                # 2.2.3(3)
    brief_for: str                                      # "DOT-POINT BRIEF FOR [INSERT APPOINTMENT]"
    subject: str                                        # 2.2.3(4)
    body: list[DpbBlock] = Field(min_length=1)

    signature: Signature
    telephone: Optional[str] = None
    annexes: list[Annex] = []
    enclosures: list[str] = []
    flags: list[str] = []                               # 2.2.7(4)
    consulted: list[str] = []                           # 2.2.7(5)

    # Fields read by shared blocks that a DPB does not have.
    @property
    def distribution(self) -> list[str]:
        return []

    @model_validator(mode="before")
    @classmethod
    def _no_decision(cls, data):
        for blk in (data or {}).get("body", []) or []:
            if isinstance(blk, dict) and "recommendations" in blk:
                raise ValueError("A dot-point brief does not seek a decision (2.2.6): "
                                 "use a minute or submission for recommendations.")
        return data

    def warnings(self) -> list[str]:
        w: list[str] = []
        first = self.body[0]
        if not (isinstance(first, GroupHeading) and first.group.strip().lower() == "purpose"):
            w.append("Commence with a short Purpose statement (2.2.8d(1)).")
        w.extend(standard_warnings(self, self.subject))
        if self.signature.service:
            w.append("The DPB signature block shows title/rank only (Fig 2-17); the Service given is not rendered.")
        texts = list(self._texts())
        joined = " ".join(texts)
        for i, _ in enumerate(self.flags):
            letter = chr(65 + i)
            if not re.search(rf"\*\*Flag {letter}\d*\*\*", joined):
                w.append(f"Flag {letter} is listed but not introduced in bold in the text, eg '**Flag {letter}**' (1.2.24(4)(a)).")
        if self.flags and not (self.enclosures or self.annexes):
            w.append("Flags identify material in an enclosure (2.2.7(4)); no enclosure is listed.")
        w.extend(text_warnings(texts, doc_name="dot-point briefs"))
        return w

    def _texts(self):
        yield self.subject
        yield from block_texts(self.body)
        for a in self.annexes:
            yield a.title
            yield from block_texts(a.body)
