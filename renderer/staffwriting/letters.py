"""Shared models and rules for formal letters (DFI 5.1 2.1.13-2.1.18).

Used by templates/internal-letter and templates/external-letter so the
salutation / complimentary close / signature rules exist once.
"""

from __future__ import annotations

import re
from typing import Literal, Optional, Union

from pydantic import Field, field_validator, model_validator

from .model import CopyNumber, DocDate, Letterhead, Markings, Para, Strict
from .wording import block_texts, text_warnings


class Salutation(Strict):
    """Typed, handwritten (space left) or none (2.1.17c-d, 2.1.18(1))."""

    mode: Literal["typed", "handwritten", "none"] = "none"
    text: Optional[str] = None          # eg "Dear Colonel Smith" (typed only)

    @field_validator("text")
    @classmethod
    def _no_comma(cls, v):
        if v is not None and v.rstrip().endswith(","):
            raise ValueError("There is no comma following the salutation (2.1.17d(4), 2.1.18(1)).")
        return v


class Close(Strict):
    mode: Literal["typed", "handwritten", "none"] = "none"
    text: Optional[str] = None          # eg "Yours sincerely" (typed only)

    @field_validator("text")
    @classmethod
    def _no_comma(cls, v):
        if v is not None and v.rstrip().endswith(","):
            raise ValueError("There is no comma following the complimentary close (2.1.17d(4), 2.1.18(10)).")
        return v


class FromLine(Strict):
    """'From: [appointment or name]' below the header (2.1.16(4))."""

    text: str
    shows: Literal["appointment", "name", "name_and_appointment"] = "appointment"


class LetterSignature(Strict):
    """Initials and surname (bold upper case), full rank for uniformed
    personnel, appointment title (2.1.16(17))."""

    initials: str
    surname: str
    rank: Optional[str] = None          # full rank, eg "Wing Commander" (2.1.16(17))
    appointment: str

    @field_validator("initials")
    @classmethod
    def _initials(cls, v):
        if not re.fullmatch(r"[A-Z]{1,5}", v):
            raise ValueError("Initials are capitals without spaces or punctuation (1.2.7(3)).")
        return v


LetterPara = Union[str, Para]


class LetterParaBlock(Strict):
    para: LetterPara

    @field_validator("para")
    @classmethod
    def _flat(cls, v):
        if isinstance(v, Para) and (v.sub or v.bullets):
            raise ValueError("Formal letter paragraphs are unnumbered, with no sub-paragraphs or bullets "
                             "(2.1.16(12), 1.2.23g).")
        return v


def check_pairing(sal: Salutation, close: Close) -> None:
    """Errors for the mandatory pairing rules."""
    if sal.mode != close.mode:
        raise ValueError("Format of the salutation and complimentary close are to agree: if the "
                         "salutation is handwritten the close is handwritten (2.1.17d(3), 2.1.18(11)); "
                         "no greeting means no close (2.1.18(9)).")
    for part, name in ((sal, "salutation"), (close, "close")):
        if part.mode == "typed" and not part.text:
            raise ValueError(f"A typed {name} needs its text.")
        if part.mode != "typed" and part.text:
            raise ValueError(f"Text is only given for a typed {name}.")


def pairing_warnings(sal: Salutation, close: Close) -> list[str]:
    """Advisory: 'Dear Colonel Smith' -> 'Yours faithfully'; 'Dear Richard' ->
    'Yours sincerely' (2.1.17d(1), 2.1.18(2)-(6)). The DFI lets the writer vary
    the close (2.1.17d), so these are warnings."""
    if sal.mode != "typed" or not sal.text or not close.text:
        return []
    words = sal.text.split()[1:] if sal.text.lower().startswith("dear ") else []
    sir = sal.text.lower() in ("dear sir", "dear madam", "dear sir or madam")
    expect = None
    if sir or len(words) >= 2:
        expect = "Yours faithfully"
    elif len(words) == 1:
        expect = "Yours sincerely"
    if expect and close.text.strip() != expect:
        return [f"'{sal.text}' is normally closed with '{expect}' (2.1.17d(1), 2.1.18)."]
    return []


def time_warnings(texts, *, external: bool) -> list[str]:
    w = []
    for t in texts:
        # 24-hour times: "at 1300", "1300 hrs" (bare four-digit numbers are usually years).
        if external and re.search(r"\b(at|from|until|by|between)\s([01]\d|2[0-3])[0-5]\d\b|"
                                  r"\b([01]\d|2[0-3])[0-5]\d\s?hrs\b", t):
            w.append(f"External letters use the 12-hour clock, eg 8:00 am (2.1.16(15)): {t[:60]!r}")
        if not external and re.search(r"\b\d{1,2}(:\d\d)?\s?(am|pm)\b", t):
            w.append(f"Internal letters use the 24-hour clock (2.1.16(15)): {t[:60]!r}")
    return w


_DAY = r"\b(Mon|Tue|Wed|Thu|Fri|Sat|Sun)\b"
_MON = r"(Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)"


def date_style_warnings(texts) -> list[str]:
    """Formal letters spell out the day (Tuesday) and use the full date
    (2 September 2016) (1.2.10a-b)."""
    w = []
    for t in texts:
        if re.search(_DAY, t):
            w.append(f"Spell out the day in full in formal letters, eg 'Tuesday' (1.2.10a): {t[:60]!r}")
        if re.search(rf"\b\d{{1,2}}\s{_MON}\s\d{{2}}\b", t):
            w.append(f"Use the full date in formal letters, eg '2 September 2016' (1.2.10b): {t[:60]!r}")
    return w


# ------------------------------------------------------------------ base content


class LetterBase(Strict):
    """Fields and rules shared by internal and external formal letters."""

    markings: Markings = Markings()                    # exceptional (2.1.16(1))
    copy_number: Optional[CopyNumber] = None           # 2.1.16(2)
    draft: Optional[Literal["electronic", "hardcopy"]] = None
    letterhead: Letterhead                             # 2.1.16(3)-(4)
    from_line: Optional[FromLine] = None               # 2.1.16(4)
    date: DocDate                                      # 2.1.16(5)
    recipient: list[str] = Field(min_length=1)        # 2.1.16(7)
    salutation: Salutation = Salutation()
    subject: Optional[str] = None                      # 1.2.17(1), 2.1.16(9)
    body: list[LetterParaBlock] = Field(min_length=1) # 2.1.16(12)
    close: Close = Close()
    signature: LetterSignature                         # 2.1.16(17)
    enclosures: list[str] = []                         # 2.1.16(18)

    # Fields the shared blocks read that a letter does not use.
    annexes: list = Field(default_factory=list, exclude=True)
    distribution: list = Field(default_factory=list, exclude=True)

    @property
    def appointment_in_from_line(self) -> bool:
        # 2.1.16(17): omit the appointment when it is shown below the header.
        return bool(self.from_line and self.from_line.shows in ("appointment", "name_and_appointment"))

    @model_validator(mode="before")
    @classmethod
    def _no_annexes(cls, data):
        if isinstance(data, dict) and data.get("annexes"):
            raise ValueError("Annexes are not appropriate in formal letters; use enclosures (2.1.16(18)).")
        return data

    @model_validator(mode="after")
    def _pairing(self):
        check_pairing(self.salutation, self.close)
        return self

    def common_warnings(self, *, external: bool) -> list[str]:
        w = pairing_warnings(self.salutation, self.close)
        if self.subject and self.subject != self.subject.upper():
            w.append("Subject heading supplied in mixed case; rendered in upper case (1.2.9(6)).")
        if self.copy_number and not self.markings.above_restricted:
            w.append("Copy numbers are for documents classified above Restricted (1.2.16(9)).")
        w.append("Check the visual identifier against the signatory (2.1.16(3)): COS and executive committee use the "
                 "assented NZDF or single-Service badge; others use the NZDF/Service logo with the Force for "
                 "New Zealand logotype.")
        texts = list(self.letter_texts())
        w.extend(time_warnings(texts, external=external))
        w.extend(date_style_warnings(texts))
        w.extend(text_warnings(texts, doc_name="letters"))
        return w

    def letter_texts(self):
        if self.subject:
            yield self.subject
        yield from block_texts(self.body)
