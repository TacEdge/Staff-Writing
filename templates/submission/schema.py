"""Content schema for the Submission (DFI 5.1 2.1.12; Annexes 2E/2F).

A submission is a minute that seeks a decision (2.1.12a, fn 32). Its body is
given as structured fields and composed into shared body blocks:

  Purpose            group heading                         [M] 2.1.12b(1)
    1. Issue.                                              [M] 2.1.12b(1)(a)
    2. Recommendation(s). lead + note/agree list           [M] 2.1.12b(1)(b)
    3. Timing.          (omit if timing has no bearing)    [M] 2.1.12b(1)(c)
  Context            group heading                         [M] 2.1.12b(2); Fig 2-6
    author's blocks (group headings allowed, eg Background) 2.1.12b(2)(b)
    must include Consultation (paragraph heading, Fig 2-6 f.) [M] 2.1.12b(2)(e)
    n. Financial and resource implications.                [M] 2.1.12b(3); A-34
  Summary            optional                              [D] 2.1.12b(4)
"""

from __future__ import annotations

import re
from typing import Literal, Optional, Union

from pydantic import Field, field_validator, model_validator

from staffwriting.model import (
    Addressee, Annex, BodyBlock, CopyNumber, DocDate, GroupHeading, Identifier, Markings, Para,
    ParaBlock, Recommendations, Signature, Strict,
)
from staffwriting.wording import block_texts, para_headings, standard_warnings, text_warnings


class SubmissionRecommendations(Recommendations):
    """2.1.12b(1)(b): lead (eg 'It is recommended that COMLOG:') and a
    note/agree list; bold verbs and list punctuation as for minutes."""

    heading: str = "unused"


class Content(Strict):
    type: Literal["submission"]
    markings: Markings = Markings()
    copy_number: Optional[CopyNumber] = None
    draft: Optional[Literal["electronic", "hardcopy"]] = None

    originator: str
    identifier: Optional[Identifier] = None
    date: DocDate
    file_reference: Optional[str] = None

    to: list[Addressee] = Field(min_length=1)          # the decision-maker 2.1.11(6)
    info: list[str] = []                               # only if essential 2.1.11(6)

    subject: str
    references: list[str] = []

    issue: str                                         # 2.1.12b(1)(a)
    recommendations: SubmissionRecommendations         # 2.1.12b(1)(b)
    timing: Optional[str] = None                       # 2.1.12b(1)(c)
    context: list[BodyBlock] = Field(min_length=1)     # 2.1.12b(2)
    financial_and_resource_implications: str           # 2.1.12b(3), A-34
    summary: list[Union[str, Para]] = []               # 2.1.12b(4)

    signature: Signature                               # 2.1.12b(5)
    telephone: Optional[str] = None
    annexes: list[Annex] = []
    enclosures: list[str] = []
    copy_distribution: list[str] = []

    # The generic blocks read these minute fields.
    @property
    def distribution(self) -> list[str]:
        return []

    @field_validator("financial_and_resource_implications")
    @classmethod
    def _fri(cls, v):
        if not v.strip():
            raise ValueError("Financial and resource implications must be stated; if there are none, "
                             "say so (2.1.12b(3)).")
        return v

    @model_validator(mode="after")
    def _rules(self):
        if len(self.info) > 6:
            raise ValueError("A maximum of six information addressees may be included (2.1.11(5)).")
        headings = [h.strip().lower() for h in para_headings(self.context)]
        groups = [b.group.strip().lower() for b in self.context if isinstance(b, GroupHeading)]
        if "consultation" not in headings + groups:
            raise ValueError("Context must include consultation (2.1.12b(2)(e) 'are to be included'): "
                             "add a paragraph or sub-paragraph headed 'Consultation' (Fig 2-6 f.).")
        return self

    # -- composition into shared body blocks --------------------------------
    def compose_body(self) -> list:
        r = self.recommendations
        rec_heading = "Recommendation" if len(r.items) == 1 else "Recommendations"   # A-27
        purpose = [
            GroupHeading(group="Purpose"),
            ParaBlock(para=Para(heading="Issue", text=self.issue)),
            ParaBlock(para=Para(heading=rec_heading, text=r.lead, sub=list(r.items),
                                sentence_list=r.conjunction)),
        ]
        if self.timing:
            purpose.append(ParaBlock(para=Para(heading="Timing", text=self.timing)))
        context = [GroupHeading(group="Context"), *self.context,
                   ParaBlock(para=Para(heading="Financial and resource implications",
                                       text=self.financial_and_resource_implications))]
        summary = []
        if self.summary:
            summary = [GroupHeading(group="Summary"), *(ParaBlock(para=p) for p in self.summary)]
        return purpose + context + summary

    # -- non-blocking findings ----------------------------------------------
    def warnings(self) -> list[str]:
        w: list[str] = []
        if len(self.to) > 1:
            w.append("There should be only one addressee, the decision-maker (2.1.11(6)).")
        if len(re.findall(r"[.?](\s|$)", self.issue.strip())) > 2:
            w.append("Set out the issue in one or two short sentences (2.1.12b(1)(a)).")
        w.extend(standard_warnings(self, self.subject))
        verbs = {re.match(r"\*\*(\w+)\*\*", i.strip()).group(1).lower() for i in self.recommendations.items
                 if re.match(r"\*\*(\w+)\*\*", i.strip())}
        if not verbs & {"agree", "approve"}:
            w.append("A submission seeks a decision: use 'agree' (or 'approve') where a decision is required "
                     "(2.1.12a, 2.1.12b(1)(b)).")
        w.extend(text_warnings(self._texts(), doc_name="minutes"))
        return w

    def _texts(self):
        yield self.subject
        yield from self.references
        yield self.issue
        yield self.recommendations.lead
        yield from self.recommendations.items
        if self.timing:
            yield self.timing
        yield from block_texts(self.context)
        yield self.financial_and_resource_implications
        yield from block_texts([ParaBlock(para=p) for p in self.summary])
        for a in self.annexes:
            yield a.title
            yield from block_texts(a.body)
