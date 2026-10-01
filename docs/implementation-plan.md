# Recommended implementation sequence

Status: **Phases 0–2 complete and accepted (2026-10-01); Word checks V-01 to
V-04 passed.** Phase 2 was re-ordered by the user to DPB → VR/PAR → internal
letter → external letter. The Administrative Instruction and CDF Directive were
held back to form the next batch with the CDF Operational Directive: planned in
[phase3-directives-plan.md](phase3-directives-plan.md), awaiting approval. Original plan text follows. No template implementation begins
until this plan and the OPEN register items it depends on are approved.

Each phase ends with a review point where you see the rendered output beside the
DFI pages.

## Phase 0: Foundation ✅ accepted

- Repository architecture, CLAUDE.md, source record and page map.
- Extracted common standards (`standards/`) and tokens (`standards/spec/`).
- Template inventory, ambiguity and decision register, architecture.

**Exit criteria:** you approve the structure, decide the OPEN items in register
sections A and T (at least A-01, A-02, A-05, T-01, T-02, T-03, T-06), and set
the policy for section E.

## Phase 1: Shared engine and the first two templates (P1)

1. Set up the Python package skeleton, token loader and test harness (pytest).
2. `styles`, `numbering` (scheme C), `page`, `furniture` (unclassified and
   "Page n of N" regimes, markings), `footnotes`, `inline`.
3. Shared `blocks` used by minutes: descriptor, identifier, date line,
   addressees, subject, references, paragraphs, recommendations, SB-MINUTE,
   list blocks.
4. `supporting`: annex and appendix pages (A-1, A-1-1, identifying block).
5. **Generic layout check:** re-key Annex 1A (Fig 1-4) and compare. This is the
   first visual regression target because it states the most rules.
6. **Minute** template + schema; re-key Example 2C; compare.
7. **Submission** template + schema; re-key Example 2E; compare.
8. The docx lint (architecture §6) for everything above.

**Review point 1:** the Minute and Submission, side by side with Figs 2-3 and
2-5; the lint report.

## Phase 2: Common staff products (P2)

Order chosen to maximise reuse:

1. **Dot-point brief** (bullets, brief margin, consulted block).
2. **Visit report / PAR** (decisions block, mandatory travel-cost Annex A table:
   first use of the `tables` module).
3. **Administrative Instruction** (scheme D hanging numbering, em-dash lists,
   distribution threshold of four).
4. **CDF Directive** (badge slot, page 1 numbered, verbatim applicability
   boilerplate) + commander and senior-executive variants.
5. **Internal formal letter** (letterhead block, From line, salutation and close
   logic, SB-LETTER, typed and handwritten variants).
6. **External letter** (12-hour clock, no file reference, salutation rules).

**Review point 2.**

## Phase 3: Ministerial, delegations, meetings, orders (P3)

1. NZDF Quality Assurance Form (the boxed-form builder).
2. NZDF Submission to the Minister + cover sheet.
3. Briefing Note to the Minister (a one-page form with an embedded numbered body).
4. Correspondence to the Minister for Veterans (dual identity).
5. Joint Note to the Minister + Joint cover sheet + Joint QA Form (SB-JOINT).
6. Delegations (temporary and permanent).
7. Meeting agenda (landscape) and minutes of a meeting.
8. DFO(T) (both variants) and CDF Operational Directive.

**Review point 3.**

## Phase 4: Publications and remaining items (P4)

1. DFI/DM publication: title page, authority order, foreword, contents (TOC
   field), preliminary provisions, main content (scheme P, Heading 1–5, part and
   chapter page numbering, warnings/cautions/notes), end matter (record of
   change), annexes "1A", revision bars and amendment numbering.
2. DFO publication variant.
3. Publications QA Form.
4. MOU.
5. Professional literature preliminary page.
6. Optional: blank-template (.dotx-style) output mode for all types (T-06).

**Review point 4.**

## Cross-cutting work (start in Phase 1, extend each phase)

- Re-key every DFI example annex as a fixture in `reference/fixtures/`.
- Render the DFI template and example pages into `reference/dfi-pages/`.
- Keep `docs/template-inventory.md` statuses and the register current.
- Wording lint (T-10) after Phase 2.

## Inputs needed from you

| Needed for | Item |
|---|---|
| Phase 1 | Decisions on the OPEN register items; the section E policy |
| Phase 1 (preferred) | The official NZDF_DSWT Word templates, if you can access them (T-03) |
| Phase 2 | Official badge and logo artwork, or approval to use labelled placeholders (T-05) |
| Phase 2 | An authoritative rank and appointment abbreviation list (A-10) |
| Phase 3 | The PSR/DFO 51 marking vocabulary and classified pagination rules (A-13, A-31) |
