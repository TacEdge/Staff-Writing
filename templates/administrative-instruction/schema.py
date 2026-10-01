"""Content schema for the Administrative Instruction (DFI 5.1 3.2.21-3.2.22;
Annex 3F, Fig 3-7).

Body composed into shared blocks (scheme D numbering, continuous across group
headings). Tags: [M] DFI prose requirement; [T] shown in Fig 3-7 only, so
optional and reported when omitted (register DR-06).

  Authority                1. "Administrative Instruction nn/yyyy is issued by …."   [T]
  Applicability            2.-3. fixed wording, 3 completed by `applies_to`          [T]
  Purpose                  stem "The purpose of this Administrative Instruction is—" [M] 3.2.22a(4)
  Introduction                                                                         [M] 3.2.22a(5)
  Conduct                                                                              [T]
  Tasks                    group headings allowed                                      [M] 3.2.22a(6)
  Coordinating arrangements                                                            [T]
  Administration           Finance, Legal                                              [T]
  Command and control      Reporting, DIRLAUTH, Points of contact                      [T]
  Cancellation             numbered (DR-03); effective date required                   [M] 3.2.22a(6)(d)
"""

from __future__ import annotations

import re
from typing import Literal, Optional

from pydantic import Field, field_validator, model_validator

from staffwriting.model import (
    Addressee, Annex, BodyBlock, CopyNumber, DocDate, Identifier, Markings, Para, ParaBlock, Signature,
    Strict,
)
from staffwriting.orders import (
    Administration, CommandAndControl, Item, check_addressees, check_no_bullets, check_stem_items,
    date_in_text, full_date, mandatory_language_warning, omitted_warning, order_warnings, section,
    stem_para, sub_sections,
)

# Fixed wording, Fig 3-7 (reproduced verbatim; CLAUDE.md §3 rule 6).
AUTHORITY = "Administrative Instruction {number} is issued by {issued_by}."                     # para 1
APPLICABILITY_GENERAL = ("This Administrative Instruction is a general order to members of the Armed "
                         "Forces, and instructions to the Civil Staff and persons seconded to the NZDF "
                         "from external employers, contractors, sub-contractors and their respective "
                         "employees.")                                                              # para 2
APPLICABILITY_SCOPE = "This Administrative Instruction applies to {applies_to}."                 # para 3
# E-14 (decided 2026-10-01): Fig 3-7 prints "this administrative instruction" in
# the Purpose stem and Cancellation; capitalised to match paras 1-3 and 3.2.21.
PURPOSE_STEM = "The purpose of this Administrative Instruction is—"                              # para 4
CANCELLATION = "This Administrative Instruction is cancelled on {date}."                         # Cancellation

FIG = "Fig 3-7"


class Content(Strict):
    type: Literal["administrative-instruction"]
    markings: Markings = Markings()
    copy_number: Optional[CopyNumber] = None
    draft: Optional[Literal["electronic", "hardcopy"]] = None

    originating_hq: Optional[str] = None            # [T] Fig 3-7 header
    originator: Optional[str] = None                # [T] Fig 3-7 "[Originator]"
    date: DocDate                                   # [M] 3.2.22b "signed and dated"
    file_reference: Optional[str] = None            # [T] "(if required)"

    to: list[Addressee] = []                        # [M] 3.2.22a(1): four or fewer ...
    distribution: list[str] = []                    # ... otherwise a distribution list

    identifier: Identifier                          # [M] 3.2.22a(2): issuing authority, number, year
    subject: str                                    # [M] 3.2.22a(3)

    issued_by: Optional[str] = None                 # [T] para 1
    applies_to: Optional[str] = None                # [T] para 3
    purpose: list[str] = Field(min_length=1)        # [M] 3.2.22a(4)
    introduction: list[Item] = Field(min_length=1)  # [M] 3.2.22a(5)
    conduct: list[Item] = []                        # [T]
    tasks: list[BodyBlock] = Field(min_length=1)    # [M] 3.2.22a(6); group headings (6)(c)
    coordinating_arrangements: list[Item] = []      # [T]
    administration: Administration = Administration()            # [T]
    command_and_control: CommandAndControl = CommandAndControl()  # [T]
    cancellation_date: DocDate                      # [M] 3.2.22a(6)(d)

    signature: Signature                            # [M] 3.2.22b; appointment line = organisation (Fig 3-7)
    annexes: list[Annex] = []                       # 3.2.22a(8)
    enclosures: list[str] = []

    @property
    def info(self) -> list[str]:
        return []          # information addressees are on the distribution list (3.2.22a(1))

    @model_validator(mode="before")
    @classmethod
    def _no_badge(cls, data):
        if isinstance(data, dict) and data.get("letterhead"):
            raise ValueError("Badges, crests or logos are not applied to AIs (3.2.22a(2)).")
        return data

    @field_validator("identifier")
    @classmethod
    def _ident(cls, v):
        if not v.appointment or v.number is None:
            raise ValueError("The AI identifier must include the issuing authority and be numbered "
                             "with the number and year of issue (3.2.22a(2)).")
        return v

    @field_validator("cancellation_date")
    @classmethod
    def _cancel(cls, v):
        return full_date(v, "Cancellation date (3.2.22a(6)(d))")

    @field_validator("issued_by", "applies_to")
    @classmethod
    def _field_text(cls, v):
        if v is not None and v.rstrip().endswith("."):
            raise ValueError("Give the text without the closing full stop; the fixed sentence supplies it.")
        return v

    @model_validator(mode="after")
    def _rules(self):
        check_addressees(self.to, self.distribution)
        check_stem_items(self.purpose, "Purpose")
        check_no_bullets([*self.introduction, *self.conduct, *self.tasks, *self.coordinating_arrangements,
                          *self.administration.finance, *self.administration.legal,
                          *self.command_and_control.reporting, *self.command_and_control.dirlauth,
                          *self.command_and_control.points_of_contact], "Administrative Instruction")
        if self.cancellation_date.as_date() < self.date.as_date(earliest=True):
            raise ValueError("The cancellation date is before the date of the AI.")
        return self

    # -- composition --------------------------------------------------------
    def _structure(self) -> tuple[list, list[str]]:
        missing: list[str] = []
        blocks: list = []
        if self.issued_by:
            number = f"{self.identifier.number:02d}/{self.identifier.year}"
            blocks += section("Authority", [AUTHORITY.format(number=number, issued_by=self.issued_by)])
        else:
            missing.append("Authority")
        if self.applies_to:
            blocks += section("Applicability", [APPLICABILITY_GENERAL,
                                                APPLICABILITY_SCOPE.format(applies_to=self.applies_to)])
        else:
            missing.append("Applicability")
        blocks += [*section("Purpose", []), stem_para(PURPOSE_STEM, self.purpose)]
        blocks += section("Introduction", self.introduction)
        if self.conduct:
            blocks += section("Conduct", self.conduct)
        else:
            missing.append("Conduct")
        blocks += section("Tasks", self.tasks)                       # DR-05
        if self.coordinating_arrangements:
            blocks += section("Coordinating arrangements", self.coordinating_arrangements)
        else:
            missing.append("Coordinating arrangements")
        a, c = self.administration, self.command_and_control
        blocks += sub_sections("Administration", [("Finance", a.finance), ("Legal", a.legal)], missing)
        blocks += sub_sections("Command and control", [("Reporting", c.reporting), ("DIRLAUTH", c.dirlauth),
                                                       ("Points of contact", c.points_of_contact)], missing)
        blocks += section("Cancellation", [CANCELLATION.format(date=date_in_text(self.cancellation_date))])  # DR-03
        return blocks, missing

    def compose_body(self) -> list:
        return self._structure()[0]

    # -- non-blocking findings ----------------------------------------------
    def warnings(self) -> list[str]:
        blocks, missing = self._structure()
        w = omitted_warning(missing, FIG)
        if len(self.purpose) > 2:
            w.append("Outline the purpose of the AI in one or two short sentences (3.2.22a(4); DR-16).")
        if not self.originating_hq:
            w.append("No originating headquarters line (shown in Fig 3-7).")
        w += mandatory_language_warning(self.tasks, "The Tasks section", "3.2.21b(2)(e)")
        w += order_warnings(self, subject=self.subject, blocks=blocks + [
            blk for a in self.annexes for blk in a.body])
        return w
