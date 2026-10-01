"""Content schema for the internal formal (demi-official) letter
(DFI 5.1 2.1.13-2.1.17; Annexes 2G/2H). Shared letter fields and rules are in
staffwriting.letters.LetterBase."""

from __future__ import annotations

import re
from typing import Literal, Optional

from pydantic import model_validator

from staffwriting.letters import LetterBase

# 2.1.15a: reporting or acknowledging a laudatory achievement, condolences, an
# administrative reprimand, a reply to an admonitory letter; plus routine use
# (2.1.15b-c) and admonition (2.1.17b, d(2)).
Purpose = Literal["routine", "congratulatory", "condolence", "admonition", "reprimand", "reply_to_admonition"]


class Content(LetterBase):
    type: Literal["internal-letter"]
    purpose: Purpose = "routine"
    file_reference: Optional[str] = None               # 2.1.16(6)
    references: list[str] = []                         # 2.1.16(10)

    @model_validator(mode="after")
    def _rules(self):
        if self.purpose in ("congratulatory", "condolence") and self.file_reference:
            raise ValueError("File references are not used on congratulatory letters or letters of condolence (2.1.16(6)).")
        if self.purpose == "admonition" and (self.salutation.mode != "none" or self.close.mode != "none"):
            raise ValueError("A letter of admonition has no salutation or ending; the writer signs over "
                             "the signature block (2.1.17d(2)).")
        return self

    def warnings(self) -> list[str]:
        w = self.common_warnings(external=False)
        if self.purpose in ("congratulatory", "condolence") and self.salutation.mode == "typed":
            w.append("The salutation in congratulatory letters and letters of condolence is usually handwritten (2.1.17c).")
        if self.purpose in ("congratulatory", "condolence"):
            caps = sorted({m for t in self.letter_texts() for m in re.findall(r"\b[A-Z]{2,}\b", t)})
            if caps:
                w.append(f"Abbreviations are inappropriate in laudatory and condolence letters (1.2.8d): {', '.join(caps)}")
            if self.subject:
                w.append("A subject heading should not be used for personal letters where an official tone is not required (2.1.16(9)).")
        if self.purpose == "admonition":
            w.append("Check: in a letter of admonition the recipient appears as rank, initials and surname, then appointment (2.1.17b).")
        return w
