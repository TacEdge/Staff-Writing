"""Content schema for the external letter (DFI 5.1 2.1.13-2.1.16, 2.1.18;
Annexes 2I/2J). Shared letter fields and rules are in staffwriting.letters."""

from __future__ import annotations

import re
from typing import Literal

from pydantic import model_validator

from staffwriting.letters import LetterBase


class Content(LetterBase):
    type: Literal["external-letter"]
    # No file_reference (2.1.16(6)) and no references block: identify any
    # reference in the introductory paragraph (2.1.16(10)).

    @model_validator(mode="before")
    @classmethod
    def _no_internal_fields(cls, data):
        if isinstance(data, dict):
            if data.get("file_reference"):
                raise ValueError("File references are not used on external letters (2.1.16(6)).")
            if data.get("references"):
                raise ValueError("In an external letter, identify the reference in the introductory paragraph, "
                                 "eg 'Thank you for your letter of dd Month yyyy concerning…' (2.1.16(10)).")
        return data

    def warnings(self) -> list[str]:
        w = self.common_warnings(external=True)
        body = " ".join(t for blk in self.body for t in [getattr(blk.para, "text", blk.para)])
        tokens = set(re.findall(r"\b[A-Z]{2,}\b", body))
        initials = set(re.findall(r"\b([A-Z]{1,3})\s[A-Z][a-z]", body))   # eg 'Captain CD Example'
        introduced = set(re.findall(r"\(([A-Z]{2,})\)", body))           # 'Leadership Centre (NZALC)'
        caps = sorted(tokens - initials - introduced)
        if caps:
            w.append("Avoid Service abbreviations in external letters; write any abbreviation in full at first use, "
                     f"then the abbreviation in brackets (2.1.16(14)). Check: {', '.join(caps)}")
        w.append("Check: external letters are only signed by CDF, a Chief of Service, or a senior commander or "
                 "executive with delegated authority (2.1.16(16)).")
        return w
