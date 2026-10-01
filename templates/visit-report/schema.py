"""Content schema for the Visit report / Post activity report (DFI 5.1
2.2.9-2.2.11; Annexes 2P/2Q).

Body composed into shared blocks (2.2.11 'is to conform to the following structure'):
  Introduction                          [M] 2.2.11(1)
  Visit report | Post activity report   [M] 2.2.11(2)  (content)
  Decisions  (Agreement / For action / For information / Further action)   [M] 2.2.11(4)
  Background information                [D] 2.2.11(5) 'should be provided'
  Conclusion(s)                         [D] 2.2.11(7) 'not always required'
  Recommendation(s)                     [D] 2.2.11(8) 'only where appropriate'
Annex A: summary of travel details     [M] 2.2.10(9), 2.2.11(3)
"""

from __future__ import annotations

import datetime as dt
from typing import Literal, Optional, Union

from pydantic import Field, model_validator

from staffwriting.model import (
    Addressee, Annex, BodyBlock, Cell, CopyNumber, DocDate, GroupHeading, Markings,
    Para, ParaBlock, Signature, Strict, Table, TableBlock,
)
from staffwriting.wording import block_texts, standard_warnings, text_warnings

DECISION_HEADINGS = {           # 2.2.11(4)(a)-(d)
    "agreement": "Agreement",
    "for_action": "For action",
    "further_action": "Further action",
    "for_information": "For information",
}

TRAVEL_ROWS = [                 # Fig 2-19 p3 (template) row labels, verbatim
    ("air_travel", "Air travel"),
    ("ground_transportation", "Ground transportation\n(incl. taxi, shuttlebus, rental vehicles)"),
    ("accommodation", "Accommodation"),
    ("meals", "Meals"),
    ("incidental_expenses", "Incidental expenses"),
]


class Decision(Strict):
    type: Literal["agreement", "for_action", "further_action", "for_information"]
    text: str


class Decisions(Strict):
    lead: str                                       # Fig 2-19 para 3 "[Click to enter text]:"
    items: list[Decision] = Field(min_length=1)


class TravelLine(Strict):
    details: str = ""
    cost: str = ""                                  # as written, eg "NZ$1,250" or "1,250"


class Travel(Strict):
    """Summary of travel details: transportation, accommodation and incidental
    costs, including conference fees (2.2.10(9))."""

    event: str
    dates: str
    air_travel: TravelLine = TravelLine()
    ground_transportation: TravelLine = TravelLine()
    accommodation: TravelLine = TravelLine()
    meals: TravelLine = TravelLine()
    incidental_expenses: TravelLine = TravelLine()


class Content(Strict):
    type: Literal["visit-report"]
    report_type: Literal["visit", "post_activity"]  # 2.2.10(5)
    markings: Markings = Markings()
    copy_number: Optional[CopyNumber] = None
    draft: Optional[Literal["electronic", "hardcopy"]] = None

    date: DocDate
    file_reference: Optional[str] = None            # 2.2.10(3)
    activity_end: Optional[DocDate] = None          # for the 'within two weeks' check (2.2.9a)

    to: list[Addressee] = Field(min_length=1)       # action addressee 2.2.10(4)
    info: list[str] = []
    distribution: list[str] = []                    # renders 'For information / See distribution'

    title: str                                      # subject after the prefix
    introduction: list[Union[str, Para]] = Field(min_length=1)       # 2.2.11(1)
    report: list[BodyBlock] = Field(min_length=1)                     # 2.2.11(2)
    decisions: Decisions                                              # 2.2.11(4)
    background: list[Union[str, Para]] = []                           # 2.2.11(5)
    conclusions: list[Union[str, Para]] = []                          # 2.2.11(7)
    recommendations: list[Union[str, Para]] = []                      # 2.2.11(8)

    signature: Signature                            # senior member (2.2.10(7))
    telephone: Optional[str] = None
    travel: Travel                                  # Annex A (2.2.10(9))
    additional_annexes: list[Annex] = []            # Annex B onwards
    enclosures: list[str] = []
    copy_distribution: list[str] = []

    @model_validator(mode="after")
    def _rules(self):
        if self.info and self.distribution:
            raise ValueError("Give information addressees either as 'info' or via a distribution list, not both.")
        if len(self.info) > 6:
            raise ValueError("Use a distribution list for more than six information addressees (2.1.11(5), (7)).")
        return self

    # -- shared-block interface ----------------------------------------------
    @property
    def report_name(self) -> str:
        return "Visit report" if self.report_type == "visit" else "Post activity report"

    @property
    def subject(self) -> str:
        # 2.2.10(5): first words are 'Visit report' or 'Post activity report'.
        return f"{self.report_name} – {self.title}"

    @property
    def annexes(self) -> list[Annex]:
        return [self._travel_annex(), *self.additional_annexes]

    def _travel_annex(self) -> Annex:
        t = self.travel
        rows = [
            [Cell(text=t.event, bold=True, span=3)],
            [Cell(text=t.dates, bold=True, span=3)],
            [Cell(text="Expense", bold=True), Cell(text="Details", bold=True), Cell(text="Cost (NZ$)", bold=True)],
        ]
        for key, label in TRAVEL_ROWS:
            line = getattr(t, key)
            rows.append([Cell(text=label, bold=True), Cell(text=line.details), Cell(text=line.cost)])
        ident = f"{self.report_name} {self.file_reference}" if self.file_reference else None
        return Annex(
            title="Summary of travel details",
            identifier=ident,
            date=self.date if ident else None,
            subject="Summary of travel details",
            body=[TableBlock(table=Table(rows=rows, col_widths_cm=[5.0, 5.0, 5.0]))],
        )

    def compose_body(self) -> list:
        def paras(items):
            return [ParaBlock(para=p) for p in items]

        d = self.decisions
        decision_para = Para(text=d.lead, sub=[Para(heading=DECISION_HEADINGS[i.type], text=i.text) for i in d.items])
        out = [GroupHeading(group="Introduction"), *paras(self.introduction),
               GroupHeading(group=self.report_name), *self.report,
               GroupHeading(group="Decisions"), ParaBlock(para=decision_para)]
        if self.background:
            out += [GroupHeading(group="Background information"), *paras(self.background)]
        if self.conclusions:
            out += [GroupHeading(group="Conclusion" if len(self.conclusions) == 1 else "Conclusions"),
                    *paras(self.conclusions)]
        if self.recommendations:
            out += [GroupHeading(group="Recommendation" if len(self.recommendations) == 1 else "Recommendations"),
                    *paras(self.recommendations)]
        return out

    # -- warnings ---------------------------------------------------------
    def warnings(self) -> list[str]:
        w: list[str] = []
        if not self.background:
            w.append("Limited background information should be provided so a reader can understand the decisions (2.2.11(5)).")
        if self.activity_end and self.date.day:
            gap = (dt.date(self.date.year, self.date.month, self.date.day)
                   - dt.date(self.activity_end.year, self.activity_end.month, self.activity_end.day or 1)).days
            if gap > 14:
                w.append(f"Report dated {gap} days after the activity; normally within two weeks (2.2.9a).")
        t = self.travel
        if not any(getattr(t, k).details or getattr(t, k).cost for k, _ in TRAVEL_ROWS):
            w.append("Annex A travel summary has no entries; it must detail travel, accommodation and incidental costs (2.2.10(9)).")
        w.extend(standard_warnings(self, self.title))
        w.append("Check: the report is classified no lower than the visit or activity (2.2.10(1)), and is signed "
                 "by the senior member of the party or host unit (2.2.10(7)).")
        w.extend(text_warnings(self._texts(), doc_name="reports"))
        return w

    def _texts(self):
        yield self.title
        for group in (self.introduction, self.background, self.conclusions, self.recommendations):
            yield from block_texts([ParaBlock(para=p) for p in group])
        yield from block_texts(self.report)
        yield self.decisions.lead
        for i in self.decisions.items:
            yield i.text
        for a in self.additional_annexes:
            yield a.title
            yield from block_texts(a.body)
