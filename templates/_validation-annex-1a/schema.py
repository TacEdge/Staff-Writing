"""Schema for the Annex 1A layout-validation document (validation only).

Fig 1-4 shows addressees *and* a distribution list together for illustration,
so both are allowed here (unlike the Minute)."""

from __future__ import annotations

from typing import Literal, Optional

from pydantic import Field

from staffwriting.model import (
    Addressee, Annex, BodyBlock, CopyNumber, DocDate, Letterhead, Markings, Signature, Strict,
)


class Content(Strict):
    type: Literal["_validation-annex-1a"]
    markings: Markings = Markings()
    copy_number: Optional[CopyNumber] = None
    draft: Optional[Literal["electronic", "hardcopy"]] = None
    letterhead: Optional[Letterhead] = None
    date: DocDate
    file_reference: Optional[str] = None
    to: list[Addressee] = []
    info: list[str] = []
    distribution: list[str] = []
    subject: str
    references: list[str] = []
    body: list[BodyBlock] = Field(min_length=1)
    signature: Signature
    annexes: list[Annex] = []
    enclosures: list[str] = []
