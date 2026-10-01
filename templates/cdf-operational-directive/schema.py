"""Content schema for the CDF Operational Directive (DFI 5.1 3.2.16-3.2.18;
Annex 3E, Fig 3-6).

  Authority                 1. "Issued by the Chief of Defence Force."            [M] 3.2.17(1)
  Situation                                                                         [M] 3.2.17(2)
  Mission                                                                           [M] 3.2.17(3)
  Execution                 (lead) a. **Intent.** b. **Tasks.**                     [M] 3.2.17(4)
  Coordinating instructions minimum elements (a)-(e)                                [M] 3.2.17(5)
  Logistics and administration  minimum elements (a)-(e)                            [M] 3.2.17(6)
  Command and control       elements (a)-(d)                                        [M] 3.2.17(7)
  Acknowledgement                                                                   [M] 3.2.17(8)
  Cancellation instructions                                                         optional 3.2.17(9)

DR-11: the minimum elements are required fields; they are rendered as the
author's paragraphs in the prose order, with no generated headings. The
optional `lead` of each section becomes its numbered paragraph, with the
elements as sub-paragraphs (Fig 3-6 shows one numbered paragraph per section).
"""

from __future__ import annotations

from typing import Literal, Optional

from pydantic import Field, field_validator, model_validator

from staffwriting.model import (
    Addressee, Annex, CopyNumber, DocDate, Identifier, Letterhead, Markings, Para, ParaBlock, Signature, Strict,
)
from staffwriting.orders import (
    CDF_BADGES, Item, check_badge, check_cdf_signatory, check_no_bullets, directive_identifier,
    element_paras, headed, mandatory_language_warning, omitted_warning, order_warnings, section,
)

AUTHORITY = "Issued by the Chief of Defence Force."         # Fig 3-6 para 1 (verbatim); 3.2.17(1)
ADDRESSEE = "COMJFNZ"                                       # 3.2.18(3)
FIG = "Fig 3-6"

Elements = list[Item]


def _req():
    return Field(min_length=1)


class Execution(Strict):
    """3.2.17(4): Intent and Tasks (paragraph headings drawn in Fig 3-6)."""

    lead: Optional[str] = None
    intent: Item                    # (a) purpose of the mission, key tasks or effects, end state
    tasks: Item                     # (b) mandatory language: 'you are to', 'BPT', 'on order'


class CoordinatingInstructions(Strict):
    """3.2.17(5) minimum elements (a)-(e), in this order."""

    lead: Optional[str] = None
    command_and_control_arrangements: Elements = _req()     # (a)
    locations: Elements = _req()                             # (b)
    timings: Elements = _req()                               # (c)
    planning_guidance: Elements = _req()                     # (d)
    freedoms_and_constraints: Elements = _req()              # (e)

    def elements(self):
        return [self.command_and_control_arrangements, self.locations, self.timings,
                self.planning_guidance, self.freedoms_and_constraints]


class LogisticsAndAdministration(Strict):
    """3.2.17(6) minimum elements (a)-(e)."""

    lead: Optional[str] = None
    logistics_guidance: Elements = _req()                    # (a)
    finance_and_resources: Elements = _req()                 # (b)
    public_affairs: Elements = _req()                        # (c)
    legal_aspects: Elements = _req()                         # (d) eg ROE, SOFA
    nzdf_output: Elements = _req()                           # (e) the associated NZDF output

    def elements(self):
        return [self.logistics_guidance, self.finance_and_resources, self.public_affairs,
                self.legal_aspects, self.nzdf_output]


class OpCommandAndControl(Strict):
    """3.2.17(7) elements (a)-(d) ('including—')."""

    lead: Optional[str] = None
    command_status: Elements = _req()                        # (a) command status or relationships
    dirlauth: Elements = _req()                              # (b)
    critical_information_requirements: Elements = _req()     # (c) "Command critical information requirements"
    points_of_contact: Elements = _req()                     # (d)

    def elements(self):
        return [self.command_status, self.dirlauth, self.critical_information_requirements,
                self.points_of_contact]


class Content(Strict):
    type: Literal["cdf-operational-directive"]
    markings: Markings = Markings()
    copy_number: Optional[CopyNumber] = None    # header right (A-21; DR-10)
    draft: Optional[Literal["electronic", "hardcopy"]] = None

    letterhead: Letterhead                      # badge [M] 3.2.18(2)
    date: DocDate
    distribution: list[str] = []                # information addressees [M] 3.2.18(3)

    number: int = Field(ge=1)                   # [M] 3.2.18(4) (controlled by AC SCE)
    year: int = Field(ge=1900, le=2999)
    operation: str                              # [M] 3.2.18(5): the name of the operation

    situation: Elements = _req()                # [M] 3.2.17(2)
    mission: Elements = _req()                  # [M] 3.2.17(3)
    execution: Execution                        # [M] 3.2.17(4)
    coordinating_instructions: CoordinatingInstructions          # [M] 3.2.17(5)
    logistics_and_administration: LogisticsAndAdministration    # [M] 3.2.17(6)
    command_and_control: OpCommandAndControl                    # [M] 3.2.17(7)
    acknowledgement: Elements = _req()          # [M] 3.2.17(8)
    cancellation: Elements = []                 # optional 3.2.17(9)

    signature: Signature                        # [M] 3.2.18(7)
    annexes: list[Annex] = []                   # 3.2.18(8)
    enclosures: list[str] = []

    # Fields the shared blocks read.
    @property
    def to(self) -> list[Addressee]:
        return [Addressee(appointment=ADDRESSEE)]

    @property
    def info(self) -> list[str]:
        return []

    @property
    def subject(self) -> str:
        return f"OPERATION {self.operation}"

    @property
    def identifier(self) -> Identifier:
        return directive_identifier("CDF", self.number, self.year)

    @model_validator(mode="before")
    @classmethod
    def _fixed(cls, data):
        if isinstance(data, dict):
            if data.get("to"):
                raise ValueError("Operational Directives are addressed to COMJFNZ (3.2.18(3)); "
                                 "information addressees go on the distribution list.")
            if data.get("subject"):
                raise ValueError("The subject heading is the name of the operation (3.2.18(5)); "
                                 "give `operation`.")
        return data

    @field_validator("operation")
    @classmethod
    def _op(cls, v):
        if v.strip().upper().startswith("OPERATION"):
            raise ValueError("Give the operation name only; 'OPERATION' is added (Fig 3-6).")
        return v

    @model_validator(mode="after")
    def _rules(self):
        check_badge(self.letterhead, CDF_BADGES, "3.2.18(2)")
        check_cdf_signatory(self.signature, "3.2.18(7)")
        ex, ci, la, cc = (self.execution, self.coordinating_instructions,
                          self.logistics_and_administration, self.command_and_control)
        check_no_bullets([*self.situation, *self.mission, ex.intent, ex.tasks,
                          *(i for el in ci.elements() + la.elements() + cc.elements() for i in el),
                          *self.acknowledgement, *self.cancellation], "Operational Directive")
        return self

    # -- composition --------------------------------------------------------
    def _structure(self) -> tuple[list, list[str]]:
        ex = self.execution
        intent, tasks = headed("Intent", ex.intent), headed("Tasks", ex.tasks)
        if ex.lead:
            execution = [ParaBlock(para=Para(text=ex.lead, sub=[intent, tasks]))]
        else:
            execution = [ParaBlock(para=intent), ParaBlock(para=tasks)]
        ci, la, cc = (self.coordinating_instructions, self.logistics_and_administration,
                      self.command_and_control)
        blocks = [
            *section("Authority", [AUTHORITY]),
            *section("Situation", self.situation),
            *section("Mission", self.mission),
            *section("Execution", execution),
            *section("Coordinating instructions", element_paras(ci.lead, ci.elements())),
            *section("Logistics and administration", element_paras(la.lead, la.elements())),
            *section("Command and control", element_paras(cc.lead, cc.elements())),
            *section("Acknowledgement", self.acknowledgement),
        ]
        missing = []
        if self.cancellation:
            blocks += section("Cancellation instructions", self.cancellation)
        else:
            missing.append("Cancellation instructions (optional, 3.2.17(9))")
        return blocks, missing

    def compose_body(self) -> list:
        return self._structure()[0]

    # -- non-blocking findings ----------------------------------------------
    def warnings(self) -> list[str]:
        blocks, missing = self._structure()
        w = omitted_warning(missing, FIG)
        w += mandatory_language_warning([self.execution.tasks], "Tasks", "3.2.17(4)(b)")
        w += order_warnings(self, subject=self.subject,
                            blocks=blocks + [blk for an in self.annexes for blk in an.body])
        return w
