"""Content schema for the Minute (DFI 5.1 2.1.10-2.1.11, Annexes 2C/2D)."""

from __future__ import annotations

from typing import Literal, Optional

from pydantic import Field, model_validator

from staffwriting.wording import block_texts, text_warnings
from staffwriting.model import (
    Addressee, Annex, BodyBlock, CopyNumber, DocDate, GroupHeading, Markings,
    ParaBlock, Para, RecommendationsBlock, Signature, Strict,
)


class Identifier(Strict):
    """'[Appointment] MINUTE [nn/yyyy]' (2.1.11(3)). The appointment and nn/yyyy
    may be omitted for internal unit minutes or personal matters."""

    appointment: Optional[str] = None
    number: Optional[int] = Field(default=None, ge=1)
    year: Optional[int] = None

    @model_validator(mode="after")
    def _pair(self):
        if (self.number is None) != (self.year is None):
            raise ValueError("Give both number and year (nn/yyyy) or neither (2.1.11(3)).")
        return self


class Content(Strict):
    type: Literal["minute"]
    markings: Markings = Markings()
    copy_number: Optional[CopyNumber] = None
    draft: Optional[Literal["electronic", "hardcopy"]] = None  # 1.2.22

    originator: str                                   # 2.1.3(1) first line [M]
    identifier: Optional[Identifier] = None           # 2.1.11(3); None renders 'MINUTE'
    date: DocDate                                     # 2.1.11(2)
    file_reference: Optional[str] = None              # 2.1.11(4)

    to: list[Addressee] = []                          # action addressee(s) 2.1.11(5)
    info: list[str] = []                              # max six 2.1.11(5)
    distribution: list[str] = []                      # 2.1.11(7)

    subject: str                                      # 2.1.11(8)
    references: list[str] = []                        # 2.1.11(9)
    body: list[BodyBlock] = Field(min_length=1)
    signature: Signature                              # 2.1.11(17)
    telephone: Optional[str] = None                   # [T] DTelN (nnn) nnnn

    annexes: list[Annex] = []
    enclosures: list[str] = []
    copy_distribution: list[str] = []

    @model_validator(mode="after")
    def _rules(self):
        if not self.to and not self.distribution:
            raise ValueError("A minute must have an action addressee (2.1.11(5)) or a distribution list (2.1.11(7)).")
        if self.distribution and (self.to or self.info):
            raise ValueError("With a distribution list, 'See distribution' replaces the addressees (2.1.11(7)); "
                             "list everyone under distribution instead of to/info.")
        if len(self.info) > 6:
            raise ValueError("A maximum of six information addressees may be included (2.1.11(5)); use a distribution list.")
        if self.copy_number and self.copy_number.number > self.copy_number.of:
            raise ValueError("Copy number exceeds total copies.")
        return self

    # Non-blocking findings (register T-10: report, never rewrite).
    def warnings(self) -> list[str]:
        w: list[str] = []
        if self.copy_number and not self.markings.above_restricted:
            w.append("Copy numbers are for documents classified above Restricted (1.2.16(9), Fig 1-4 fn 2).")
        if len(self.to) + len(self.info) > 6 and not self.distribution:
            w.append("More than six addressees: a distribution list may be used (2.1.11(7)).")
        first = self.body[0]
        if not (isinstance(first, GroupHeading) and first.group.strip().lower() == "purpose"):
            w.append("A 'Purpose' paragraph at the start is often useful (2.1.11(11)).")
        if self.subject != self.subject.upper():
            w.append("Subject heading supplied in mixed case; rendered in upper case (1.2.9(6)).")
        w.extend(text_warnings(_all_text(self), doc_name="minutes"))
        return w


def _all_text(c: Content):
    yield c.subject
    yield from c.references
    yield from block_texts(c.body)
    for a in c.annexes:
        yield a.title
        yield from block_texts(a.body)
