"""Content schema for the CDF Directive (DFI 5.1 3.2.8-3.2.14; Annex 3D,
Fig 3-5) and its variants (register DR-13):

  issuer: cdf               CDF Directive (3.2.9-3.2.11)
  issuer: commander         COS, COMJFNZ and subordinate commanders (3.2.12)
  issuer: senior_executive  senior executives with delegated authority (3.2.13)

Tags: [M] DFI prose requirement; [T] Fig 3-5 only, so optional and reported
when omitted (DR-06).

  Authority                1. "Issued by the Chief of Defence Force."       [M] 3.2.10(1) (CDF; variants: author text [T])
  Applicability            2.-4. fixed wording, 3 completed by `responsibilities` [T]
  Purpose                  "The purpose of this Directive is—" a. to …      [M] 3.2.10(2)
  Context/Situation                                                         [M] 3.2.10(3)
  Conduct                                                                   [T]
  Accountabilities and responsibilities                                     [T]
  Coordinating arrangements  Planning guidance                              [T]
  Administration           Finance, Legal                                   [T]
  Command and control      Reporting, DIRLAUTH, Points of contact           [T]
  Cancellation and disposal instructions  one of the two Fig 3-5 wordings   [M] 3.2.10(4)
"""

from __future__ import annotations

from typing import Literal, Optional

from pydantic import Field, field_validator, model_validator

from staffwriting.model import (
    Addressee, Annex, CopyNumber, DocDate, Identifier, Letterhead, Markings, Signature, Strict,
)
from staffwriting.orders import (
    CDF_BADGES, Administration, CommandAndControl, Item, add_years, check_addressees, check_badge,
    check_cdf_signatory, check_no_bullets, check_stem_items, date_in_text, directive_identifier, full_date,
    omitted_warning, order_warnings, section, stem_para, sub_sections,
)

# Fixed wording, Fig 3-5 (verbatim; CLAUDE.md §3 rule 6).
AUTHORITY_CDF = "Issued by the Chief of Defence Force."                                        # para 1
APPLICABILITY_GENERAL = ("This Directive constitutes a general order to members of the Armed Forces "
                         "and instructions to the Civil Staff and persons seconded to the NZDF from "
                         "external employers, contractors, sub-contractors and their respective "
                         "employees.")                                                          # para 2
APPLICABILITY_SCOPE = ("This Directive applies to all members of the NZDF who have responsibilities "
                       "for {responsibilities}. The orders, directions and instructions in this "
                       "Directive are to be considered applicable to all whom they may concern.")  # para 3
APPLICABILITY_COMPLIANCE = ("Non-compliance with this Directive may result in disciplinary action being "
                            "taken in accordance with the Armed Forces Discipline Act 1971 or may result "
                            "in possible sanctions in accordance with the Civil Staff Code of Conduct.")  # para 4
PURPOSE_STEM = "The purpose of this Directive is—"                                             # para 5
PURPOSE_ITEM = "to {text}"                                                                      # 5a ("to" fixed)
# Para 15, two template options. E-13 (decided 2026-10-01): "DFO 14" is fixed
# text in Fig 3-5; reproduced verbatim and flagged on every use.
CANCEL_INCORPORATED = ("This Directive is to be cancelled when the instructions contained herein have "
                       "been incorporated in DFO 14 and no later than {date}.")
CANCEL_WITH_EFFECT = "This Directive is cancelled with effect {date}."

FIG = "Fig 3-5"
SERVICE_BADGES = ("navy_badge", "army_badge", "airforce_badge", "nzdf_badge")


class Cancellation(Strict):
    """3.2.10(4) [M]: disposal instructions; one of the two Fig 3-5 wordings."""

    option: Literal["incorporated", "with_effect"]
    date: DocDate

    @field_validator("date")
    @classmethod
    def _full(cls, v):
        return full_date(v, "Cancellation date (3.2.10(4))")


class CoordinatingArrangements(Strict):
    planning_guidance: list[Item] = []          # [T] Fig 3-5 para 9


class Content(Strict):
    type: Literal["cdf-directive"]
    issuer: Literal["cdf", "commander", "senior_executive"] = "cdf"     # DR-13
    markings: Markings = Markings()
    copy_number: Optional[CopyNumber] = None
    draft: Optional[Literal["electronic", "hardcopy"]] = None

    letterhead: Optional[Letterhead] = None     # badge [M] 3.2.11(2); address line (Fig 3-5; 1.2.18a)
    date: DocDate                               # effective from signature (3.2.9d)
    to: list[Addressee] = []                    # [M] 3.2.11(3): four or fewer ...
    distribution: list[str] = []                # ... otherwise a distribution list

    identifier_appointment: Optional[str] = None   # variants: "[APPOINTMENT] DIRECTIVE" (DR-13)
    number: int = Field(ge=1)                   # [M] 3.2.11(4) (OCDF supplies CDF numbers)
    year: int = Field(ge=1900, le=2999)         # [M] 3.2.11(4)
    subject: str                                # [M] 3.2.11(5)

    authority: Optional[str] = None             # variants only (CDF wording is fixed)
    responsibilities: Optional[str] = None      # [T] Applicability para 3 field
    purpose: list[str] = Field(min_length=1)    # [M] 3.2.10(2); items follow the fixed "to"
    context: list[Item] = Field(min_length=1)   # [M] 3.2.10(3)
    conduct: list[Item] = []                    # [T]
    accountabilities: list[Item] = []           # [T] "Accountabilities and responsibilities"
    coordinating_arrangements: CoordinatingArrangements = CoordinatingArrangements()  # [T]
    administration: Administration = Administration()                                 # [T]
    command_and_control: CommandAndControl = CommandAndControl()                      # [T]
    cancellation: Cancellation                  # [M] 3.2.10(4)

    signature: Signature                        # [M] 3.2.11(7)
    annexes: list[Annex] = []                   # 3.2.11(8)
    enclosures: list[str] = []

    @property
    def info(self) -> list[str]:
        return []

    @property
    def identifier(self) -> Identifier:
        appt = "CDF" if self.issuer == "cdf" else self.identifier_appointment
        return directive_identifier(appt, self.number, self.year)

    @field_validator("purpose")
    @classmethod
    def _purpose(cls, v):
        check_stem_items(v, "Purpose")
        for it in v:
            if it.lower().startswith("to "):
                raise ValueError("Purpose items follow the fixed word 'to' (Fig 3-5 para 5a): "
                                 "give the text after 'to'.")
        return v

    @field_validator("responsibilities")
    @classmethod
    def _resp(cls, v):
        if v is not None and v.rstrip().endswith("."):
            raise ValueError("Give the text without the closing full stop; the fixed sentence supplies it.")
        return v

    @model_validator(mode="after")
    def _rules(self):
        check_addressees(self.to, self.distribution)
        check_no_bullets([*self.context, *self.conduct, *self.accountabilities,
                          *self.coordinating_arrangements.planning_guidance,
                          *self.administration.finance, *self.administration.legal,
                          *self.command_and_control.reporting, *self.command_and_control.dirlauth,
                          *self.command_and_control.points_of_contact], "Directive")
        if self.cancellation.date.as_date() < self.date.as_date(earliest=True):
            raise ValueError("The cancellation date is before the date of the directive.")
        if self.issuer == "cdf":
            check_badge(self.letterhead, CDF_BADGES, "3.2.11(2)")
            check_cdf_signatory(self.signature, "3.2.11(7)")
            if self.identifier_appointment or self.authority:
                raise ValueError("A CDF Directive's identifier ('CDF DIRECTIVE') and Authority wording "
                                 "are fixed (3.2.10(1), 3.2.11(4), Fig 3-5).")
            # DR-17: effective for one year or less from signature (3.2.9d).
            latest_signature = self.date.as_date(earliest=False)
            if self.cancellation.date.as_date() > add_years(latest_signature):
                raise ValueError("A CDF Directive is effective for one year or a lesser period from the "
                                 "date of signature; the cancellation date is later (3.2.9d; DR-17).")
        else:
            if not self.identifier_appointment:
                raise ValueError("Give the issuing appointment for the identifier, "
                                 "eg 'COMJFNZ DIRECTIVE 03/2026' (DR-13).")
            device = self.letterhead.device if self.letterhead else None
            if self.issuer == "senior_executive" and device:
                raise ValueError("Directives issued by senior executives do not use any badge, crest or "
                                 "logo (3.2.13c).")
            if self.issuer == "commander" and device and device not in SERVICE_BADGES:
                raise ValueError("A commander's directive may carry the Service, command or unit badge "
                                 f"(3.2.12b); available: {', '.join(SERVICE_BADGES)} (BR-04).")
        return self

    # -- composition --------------------------------------------------------
    def _structure(self) -> tuple[list, list[str]]:
        missing: list[str] = []
        blocks: list = []
        if self.issuer == "cdf":
            blocks += section("Authority", [AUTHORITY_CDF])
        elif self.authority:
            blocks += section("Authority", [self.authority])
        else:
            missing.append("Authority")
        if self.responsibilities:
            blocks += section("Applicability", [
                APPLICABILITY_GENERAL,
                APPLICABILITY_SCOPE.format(responsibilities=self.responsibilities),
                APPLICABILITY_COMPLIANCE])
        else:
            missing.append("Applicability")
        blocks += [*section("Purpose", []),
                   stem_para(PURPOSE_STEM, [PURPOSE_ITEM.format(text=t) for t in self.purpose])]
        blocks += section("Context/Situation", self.context)
        for name, items in (("Conduct", self.conduct), ("Accountabilities and responsibilities", self.accountabilities)):
            if items:
                blocks += section(name, items)
            else:
                missing.append(name)
        blocks += sub_sections("Coordinating arrangements",
                               [("Planning guidance", self.coordinating_arrangements.planning_guidance)], missing)
        a, c = self.administration, self.command_and_control
        blocks += sub_sections("Administration", [("Finance", a.finance), ("Legal", a.legal)], missing)
        blocks += sub_sections("Command and control", [("Reporting", c.reporting), ("DIRLAUTH", c.dirlauth),
                                                       ("Points of contact", c.points_of_contact)], missing)
        wording = CANCEL_INCORPORATED if self.cancellation.option == "incorporated" else CANCEL_WITH_EFFECT
        blocks += section("Cancellation and disposal instructions",
                          [wording.format(date=date_in_text(self.cancellation.date))])
        return blocks, missing

    def compose_body(self) -> list:
        return self._structure()[0]

    # -- non-blocking findings ----------------------------------------------
    def warnings(self) -> list[str]:
        blocks, missing = self._structure()
        w = omitted_warning(missing, FIG)
        if self.cancellation.option == "incorporated":
            w.append("Cancellation wording reproduces the fixed 'DFO 14' reference from Fig 3-5 verbatim; "
                     "confirm the parent publication (register E-13).")
        if self.issuer == "cdf" and self.annexes:
            w.append("Annexes and enclosures are included in a CDF Directive only in exceptional "
                     "circumstances, and must relate directly to the orders issued (3.2.11(8)).")
        w += order_warnings(self, subject=self.subject,
                            blocks=blocks + [blk for an in self.annexes for blk in an.body])
        return w
