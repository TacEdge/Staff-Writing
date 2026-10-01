"""Shared content models (pydantic) used by document-type schemas.

These describe *content*, not layout. Layout comes from tokens and the
template's template.yaml.
"""

from __future__ import annotations

import re
from typing import Literal, Optional, Union

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from .inline import plain

# ----------------------------------------------------------------- markings
# Closed vocabulary pending register A-13 (PSR / DFO 51 not held). Only markings
# that appear in DFI 5.1 are accepted.
CLASSIFICATIONS = ["UNCLASSIFIED", "RESTRICTED", "CONFIDENTIAL", "SECRET", "TOP SECRET"]
ABOVE_RESTRICTED = {"CONFIDENTIAL", "SECRET", "TOP SECRET"}
ENDORSEMENTS = ["IN-CONFIDENCE", "SENSITIVE", "STAFF-IN-CONFIDENCE"]
Classification = Literal["UNCLASSIFIED", "RESTRICTED", "CONFIDENTIAL", "SECRET", "TOP SECRET"]
Endorsement = Literal["IN-CONFIDENCE", "SENSITIVE", "STAFF-IN-CONFIDENCE"]
assert list(Classification.__args__) == CLASSIFICATIONS and list(Endorsement.__args__) == ENDORSEMENTS


class Strict(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Markings(Strict):
    classification: Optional[Classification] = None
    endorsement: Optional[Endorsement] = None

    @property
    def above_restricted(self) -> bool:
        return self.classification in ABOVE_RESTRICTED

    def header_lines(self) -> list[str]:
        # 1.2.16(5): classification first line; endorsement inside it.
        return [x for x in (self.classification, self.endorsement) if x]

    def footer_lines(self) -> list[str]:
        # Mirror order: classification on the last line.
        return [x for x in (self.endorsement, self.classification) if x]

    def warnings(self) -> list[str]:
        w = []
        if self.endorsement and not self.classification:
            w.append("1.1.10f: an endorsement marking is not used without a security "
                     "classification (register A-13).")
        return w


class CopyNumber(Strict):
    number: int = Field(ge=1)
    of: int = Field(ge=1)

    @model_validator(mode="after")
    def _within_total(self):
        if self.number > self.of:
            raise ValueError("Copy number exceeds total copies (1.2.16(9)).")
        return self


class Identifier(Strict):
    """'[Appointment] MINUTE [nn/yyyy]' (2.1.11(3)). The appointment and nn/yyyy
    may be omitted for internal unit minutes or personal matters."""

    appointment: Optional[str] = None
    number: Optional[int] = Field(default=None, ge=1)
    year: Optional[int] = Field(default=None, ge=1900, le=2999)   # yyyy (2.1.11(3))

    @model_validator(mode="after")
    def _pair(self):
        if (self.number is None) != (self.year is None):
            raise ValueError("Give both number and year (nn/yyyy) or neither (2.1.11(3)).")
        return self


def check_initials(v: str) -> str:
    """Initials: capitals, no spaces or punctuation (1.2.7(3), 2.1.11(17)(a))."""
    if not re.fullmatch(r"[A-Z]{1,5}", v):
        raise ValueError("Initials are capitals without spaces or punctuation (2.1.11(17)(a), 1.2.7(3)).")
    return v


# --------------------------------------------------------------------- dates

class DocDate(Strict):
    """A document date. `day` is left out by default: DFI expects the day to be
    handwritten at signature (fn 20, 2.1.11(2); register A-02)."""

    year: int = Field(ge=1900, le=2999)
    month: int = Field(ge=1, le=12)
    day: Optional[int] = Field(default=None, ge=1, le=31)

    @model_validator(mode="after")
    def _real_date(self):
        if self.day is not None:
            import datetime as _dt
            try:
                _dt.date(self.year, self.month, self.day)
            except ValueError as e:
                raise ValueError(f"Not a calendar date: {self.day}/{self.month}/{self.year} ({e}).") from None
        return self


# ---------------------------------------------------------------- body text

class Bullet(Strict):
    """Bulleted item (1.2.23g): dot at the first tab, diamond at the second."""

    text: str
    sub: list[str] = []


class Para(Strict):
    """A numbered paragraph (level set by nesting)."""

    heading: Optional[str] = None  # paragraph heading, bold, ends with a full stop (1.2.17(4))
    text: str = ""
    sub: list[Union[str, "Para"]] = []
    # Apply single-sentence list punctuation to `sub` items (1.2.23b(1)):
    # ';' after each, '; and' / '; or' before the last, '.' at the end.
    sentence_list: Optional[Literal["and", "or"]] = None
    # Unordered list that will not be referred back to (1.2.23g). Not allowed in
    # formal letters, orders, directions or instructions (templates enforce).
    bullets: list[Union[str, Bullet]] = []

    @field_validator("heading")
    @classmethod
    def _heading(cls, v):
        if v is not None and v.rstrip().endswith("."):
            raise ValueError("Give the paragraph heading without its full stop; it is added (1.2.17(4)).")
        return v


class GroupHeading(Strict):
    group: str


class MainHeading(Strict):
    main: str


class ParaBlock(Strict):
    para: Union[str, Para]


class Recommendations(Strict):
    """Recommendations group (2.1.11(13)). Items are a single-sentence list
    whose action verb (note/agree/approve...) is set in bold (1.2.11(2))."""

    heading: str = "Recommendations"
    lead: str  # eg "It is recommended that CA:"
    items: list[str] = Field(min_length=1)
    conjunction: Literal["and", "or"] = "and"

    @field_validator("items")
    @classmethod
    def _bold_verb(cls, items):
        for it in items:
            if not it.lstrip().startswith("**"):
                raise ValueError(f"Recommendation must start with a bold action verb, eg '**note** that ...' (1.2.11(2)): {it!r}")
            if it.rstrip().endswith(";") or it.rstrip().endswith((" and", " or")):
                raise ValueError(f"Give recommendation items without list punctuation; it is applied (1.2.23b(1)): {it!r}")
        return items


class RecommendationsBlock(Strict):
    recommendations: Recommendations


class ApprovalBlock(Strict):
    """Single-approval statement placed above the signature block (2.1.11(13))."""

    approval: Literal["approved_not_approved"]


class Cell(Strict):
    text: str = ""
    bold: bool = False
    span: int = Field(default=1, ge=1)
    align: Literal["left", "center", "right"] = "left"
    # For multi-line cells ("\n"): bold applies to the first line only.
    first_line_bold_only: bool = True


class Table(Strict):
    """A DFI table (1.2.25). Rows are lists of cells (or plain strings)."""

    rows: list[list[Union[Cell, str]]] = Field(min_length=1)
    header_rows: int = 0
    col_widths_cm: Optional[list[float]] = None
    caption: Optional[str] = None  # rendered "Table n<tab>caption" above (1.2.25b; A-23)

    @field_validator("rows")
    @classmethod
    def _cells(cls, rows):
        return [[c if isinstance(c, Cell) else Cell(text=c) for c in row] for row in rows]


class TableBlock(Strict):
    table: Table


BodyBlock = Union[GroupHeading, MainHeading, ParaBlock, RecommendationsBlock, TableBlock]


# ---------------------------------------------------------------- addressees

class Addressee(Strict):
    appointment: str
    through: Optional[str] = None  # rendered "(through X)" (2.1.11(5), fn 33-34)


# ----------------------------------------------------------------- signature

class Signature(Strict):
    initials: str
    surname: str
    rank: str  # abbreviated rank/title for minutes (2.1.11(17)(b)); list pending A-10
    service: Optional[str] = None
    appointment: str

    @field_validator("initials")
    @classmethod
    def _initials(cls, v):
        return check_initials(v)

    @field_validator("rank")
    @classmethod
    def _rank(cls, v):
        if "." in v:
            raise ValueError("No full stops in abbreviated ranks or titles (1.2.7(3), 1.2.9(4)).")
        return v


# ------------------------------------------------------- supporting documents

def _date_needs_identifier(obj):
    # 1.2.24(1)(c)-(d): the authorisation date accompanies the unique identifier;
    # without one the identifying block shows only the reference.
    if obj.date is not None and not obj.identifier:
        raise ValueError("An annex or appendix date is shown with its unique identifier; give an "
                         "identifier or omit the date (1.2.24(1)(c)-(d)).")
    return obj


class AppendixContent(Strict):
    title: str
    identifier: Optional[str] = None
    date: Optional[DocDate] = None
    subject: Optional[str] = None
    body: list[BodyBlock] = []

    @model_validator(mode="after")
    def _date(self):
        return _date_needs_identifier(self)


class Annex(Strict):
    """Listed under Annex(es) and, if `body` is given, rendered after the
    parent in the same file (1.2.24(6))."""

    title: str  # as listed after the signature block
    identifier: Optional[str] = None  # unique identifier for the identifying block
    date: Optional[DocDate] = None  # authorisation date (1.2.24(1)(c))
    subject: Optional[str] = None  # annex subject heading; defaults to title
    body: list[BodyBlock] = []
    appendices: list[AppendixContent] = []

    @model_validator(mode="after")
    def _date(self):
        return _date_needs_identifier(self)


def plain_len(text: str) -> int:
    return len(plain(text))


Para.model_rebuild()


class Letterhead(Strict):
    """Badge/logo slot (top left) and address block (top right) (Fig 1-4; A-14).
    `device` names the badge or logo; artwork is a later input (T-05)."""

    device: Optional[str] = None
    unit: Optional[str] = None  # first line in bold, eg "[Unit name]" (Figs 2-8, 2-9) [T]
    address: list[str] = Field(min_length=1)
