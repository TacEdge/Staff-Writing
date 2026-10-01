# Phase 3 plan: Administrative Instruction, CDF Directive, CDF Operational Directive

Status: **PLAN ONLY, awaiting approval (2026-10-01).** Nothing in this plan has
been implemented. The decisions in §5 are needed before implementation starts.

Constraint from the user (2026-10-01): the Phase 1–2 renderer foundation is
accepted, and no further architectural changes are to be made unless a newly
implemented DFI document type requires them. §4 lists every change this family
needs and the DFI rule that requires each one.

## 1. DFI sources read

| Type | Prose | Template annex (PDF page) | Example annex |
|---|---|---|---|
| Administrative Instruction (AI) | 3.2.21–3.2.22 | 3F, Fig 3-7 (pp 178–179) | None |
| CDF Directive | 3.2.8–3.2.14 | 3D, Fig 3-5 (pp 167–168) | None |
| CDF Operational Directive | 3.2.15–3.2.19 | 3E, Fig 3-6 (pp 173–174) | None |
| Shared | 1.2.10 (days and dates), 1.2.16(6)–(7) and fn 23 (pages, hanging indents), 1.2.17 (headings), 1.2.23c, f, g (lists), 1.2.21 (signature), 1.2.24 (supporting documents) | | |

No DFI example annex exists for any of the three types. Validation can therefore
only compare against the **template** figures (structure and layout), not
against a worked example. This is a limitation of the DFI, not of the plan.

## 2. Shared requirements of the family

| # | Requirement | Source | Tag | AI | CDF Dir | Op Dir |
|---|---|---|---|---|---|---|
| F-1 | Hanging first-level numbering: number at the margin, text starts and wraps at 1 cm (scheme D) | 3.2.11(6), 3.2.18(6), 3.2.22a(7), fn 23 | M | ✓ | ✓ | ✓ |
| F-2 | Sub-paragraph levels a., (1), (a) on scheme D geometry | Figs 3-5 to 3-7 | T | ✓ | ✓ | ✓ |
| F-3 | Group headings (bold sentence case, unnumbered); paragraph numbers run continuously across them | 1.2.17(3); Figs 3-5 to 3-7 | M/T | ✓ | ✓ | ✓ |
| F-4 | Identifier in bold upper case **immediately above** the subject heading (or operation name), including the number and year of issue | 3.2.11(4), 3.2.18(4), 3.2.22a(2) | M | ✓ | ✓ | ✓ |
| F-5 | Subject heading: short, accurate, bold capitals | 3.2.11(5), 3.2.18(5), 3.2.22a(3), 1.2.17(1) | M | ✓ | ✓ | ✓ (operation name) |
| F-6 | No bulleted lists | 1.2.23g | M | ✓ | ✓ | ✓ |
| F-7 | Vertical-list lead-ins take an em dash, not a colon | 1.2.23c(2); A-07 | M | ✓ | ✓ | ✓ |
| F-8 | All vertical-list components numbered | 1.2.23f | M | ✓ | ✓ | ✓ |
| F-9 | Mandatory language ("is to", "are to", "must") | 3.2.9b, 3.2.17(4)(b), 3.2.21b(2)(e); 1.2.6 | M | ✓ | ✓ | ✓ |
| F-10 | Abbreviated appointment titles for addressees and in the text | 3.2.11(3), (9); 3.2.18(3), (9); 3.2.22a(1) | M | ✓ | ✓ | ✓ |
| F-11 | Distribution list when there are more than four addressees | 3.2.11(3), 3.2.22a(1); A-04 | M | ✓ | ✓ | (F-12) |
| F-12 | Op Directive: addressed to COMJFNZ; information addressees always by distribution list | 3.2.18(3) | M | | | ✓ |
| F-13 | Annexes and enclosures must be introduced in the text | 3.2.11(8), 3.2.18(8), 3.2.22a(8) | M | ✓ | ✓ | ✓ |
| F-14 | Day names in full in orders, directions and instructions; abbreviated dates (2 Sep 26); 24-hour clock | 1.2.10a–c | D | ✓ | ✓ | ✓ |
| F-15 | Repeated sections: Authority, Administration (Finance, Legal), Command and control (Reporting, DIRLAUTH, Points of contact), then cancellation | Figs 3-5, 3-7 | T | ✓ | ✓ | (own list, 3.2.17(7)) |
| F-16 | A cancellation instruction | 3.2.10(4) M; 3.2.22a(6)(d) M; 3.2.17(9) optional | M/D | required | required | optional |
| F-17 | Signature block: name (bold upper case), title/rank, appointment or organisation | Figs 3-5 to 3-7; 1.2.21 | T | ✓ | ✓ | ✓ |
| F-18 | Page numbers: all pages including page 1 when there are two or more pages | 3.2.11(1), 3.2.18(1) | M | (DR-02) | ✓ | ✓ |
| F-19 | Markings, page setup, fonts, supporting documents, copy number: shared standards, unchanged | `standards/` | M | ✓ | ✓ | ✓ |

Type-specific requirements:

- **AI.**
  - No badge, crest or logo (3.2.22a(2), M).
  - Centred originating-HQ line in upper case, then an [Originator] line.
  - Date at the left and the file reference at the right.
  - Identifier "[AUTHORISED APPOINTMENT] ADMINISTRATIVE INSTRUCTION [NN/YYYY]". It must include the issuing authority (M).
  - Authority paragraph: "Administrative Instruction [nn/yyyy] is issued by […]."
  - Applicability paragraphs 2–3, verbatim.
  - Purpose stem "The purpose of this administrative instruction is—".
  - Then Introduction, Conduct, Tasks, Coordinating arrangements, Administration, Command and control and Cancellation.
  - An effective cancellation date is required (3.2.22a(6)(d), M).
  - Signed and dated by a person with delegated authority (3.2.22b, M).
- **CDF Directive.**
  - Assented NZDF badge (3.2.11(2), M) at the top left; address line at the top right.
  - Date, then the addressee or "See distribution" (bold).
  - Identifier "CDF DIRECTIVE [NN/YYYY]". The number comes from OCDF (input only).
  - Authority "Issued by the Chief of Defence Force."
  - Applicability paragraphs 2–4, verbatim.
  - Purpose stem "The purpose of this Directive is—" followed by "a. to […]".
  - Then Context/Situation, Conduct, Accountabilities and responsibilities, Coordinating arrangements (Planning guidance), Administration, Command and control, and Cancellation and disposal instructions (two template wordings).
  - Effective for one year or less (3.2.9d, M). Never amended; a change means cancel and reissue (3.2.9f, M).
  - Signed by CDF. VCDF or CoS HQNZDF may sign over the block with a handwritten "for" (3.2.11(7)).
  - Variants:
    - COS/commander directive: badge at the issuer's discretion (3.2.12).
    - Senior-executive directive: no badge (3.2.13c, M).
- **CDF Operational Directive.**
  - Official NZDF badge (3.2.18(2), M).
  - "Copy [n] of [N]" (optional).
  - Date, then COMJFNZ, then "For information / See distribution".
  - Identifier "CDF OPERATIONAL DIRECTIVE [NN/YYYY]". The number is controlled by AC SCE (input only).
  - Subject "OPERATION [NAME]".
  - Sections: Authority, Situation, Mission, Execution (Intent, Tasks), Coordinating instructions, Logistics and administration, Command and control, Acknowledgement (required, 3.2.17(8)) and Cancellation instructions (optional, 3.2.17(9)).
  - Minimum elements:
    - coordinating instructions (3.2.17(5)): five elements;
    - logistics and administration (3.2.17(6)): five elements;
    - command and control (3.2.17(7)): four elements.
  - Tasks use "you are to", "BPT" or "on order" (3.2.17(4)(b)).
  - Signed by CDF. VCDF may sign over the block with "for" (3.2.18(7)).

## 3. What is reused unchanged

| Need | Existing component |
|---|---|
| Scheme D numbering geometry | `numbering.directive` in the tokens; `Numbering.instance("directive")`; `body` block option `numbering: directive`. The paragraph styles take their indents from the numbering definition, so no style change is needed. |
| Group headings, continuous numbering, paragraph headings ("**Intent.**"), em-dash sentence lists | `body_blocks`, `_render_para`, `Para.sentence_list` |
| Badge (placeholder, T-05) and address block | `letterhead` block |
| Date with the file reference at the right | `date_line` (option `indent_cm: 0`) |
| Addressees / "See distribution" / "For information / See distribution" | `addressees` with `distribution_mode: all` or `info` |
| Identifier "[APPT] WORD NN/YYYY" | `identifier` block (option `word`) and the shared `Identifier` model |
| Subject, annex and enclosure lists, distribution, supporting documents, markings, copy number, "Page n of N" above Restricted | existing blocks and `Furniture` |
| Fixed paragraphs (Authority, Applicability, Purpose stem) | Composed by each schema's `compose_body()`, as the Submission already does. The verbatim text is held as cited constants in the template's `schema.py`. No new block is needed. |
| Day, abbreviation, exclamation, "%" and eg/ie/etc warnings | `wording.py`, `letters.date_style_warnings` (full day names) |

## 4. New renderer capabilities required (all additive)

Each item is needed only because a rule of this family cannot be met by the
current code. Existing templates keep their behaviour and output unchanged,
and that is tested (§6, T-R1).

| # | Capability | Required by | Change |
|---|---|---|---|
| N-1 | **Page-number regime "number page 1 when there are two or more pages"** | 3.2.11(1), 3.2.18(1) | `page.py`: `Furniture` gets an optional `regime` argument (default: today's behaviour, derived from the markings). In the new regime the first-page footer carries `{IF {SECTIONPAGES} > 1 "{PAGE}" ""}` (or NUMPAGES, see DR-01). The same nested-field helper is already used for annex numbers. `template.yaml` selects it through the existing `page:` key, which the renderer already reads. Above Restricted, "Page n of N" is unchanged. |
| N-2 | **Lint: regime-aware page-number check** | N-1 | `lint.py` today reports an error when page 1 of an unclassified document carries a number. It will accept the conditional field when the template declares the directive regime (through the template's existing `lint:` key). |
| N-3 | **Lint: scheme-aware numbering geometry** | F-1 | `lint.py` checks scheme C geometry only. Generalise the check to read the expected indents for the declared scheme (`correspondence` or `directive`) from the tokens, and flag any bullet numbering in these types (F-6). |
| N-4 | **Shared order/directive content module** `orders.py` | F-6 to F-18 | The counterpart of `letters.py`: shared pydantic pieces (cancellation, Administration and Command and control sub-structures, distribution threshold of four, badge rule by issuer, bullet prohibition) and shared warnings. Additive. |
| N-5 | **Wording warnings for orders** | 1.2.23c(2), A-07, 1.2.10a, 3.2.17(4)(b) | `text_warnings` currently always warns on em dashes ("not used in correspondence"). Add a document-class parameter so orders do **not** warn on em dashes and **do** warn on a colon list lead-in. New order warnings: abbreviated day names (DR-09); a Tasks paragraph without mandatory language; an annex or enclosure not mentioned in the text (F-13). These stay warnings and never rewrite (T-10). |
| N-6 | **AI originating-HQ block** | Fig 3-7 | A small block: a centred upper-case HQ line, then a centred [Originator] line. The size is measured from Fig 3-7 against the 12 pt body, as in A-22 (`[T]`), and held as a token. Kept separate from `originator_descriptor` so the Minute is unaffected. |
| N-7 | **"See distribution" weight option** | Fig 3-5 bold; Fig 3-7 regular | An `addressees` option, default unchanged (DR-15). |
| N-8 | **Optional: an unnumbered paragraph among numbered ones** | Fig 3-7 cancellation | Needed **only if** DR-03 is decided for the template (unnumbered). It would be an optional `numbered: false` flag on the shared paragraph block. |

Not needed: new styles, new numbering code, new section handling, changes to the
footnote or supporting-document builders.

The family needs one new Word check, because LibreOffice cannot evaluate
conditional fields (as with V-01):

- **V-05:** directive page 1 shows "1" when the document has two or more pages, and no number on a single page.

## 5. Ambiguities and decisions needed

The recommendation follows the repository rule: prose ("is to"/"must") over
template, template over example. Each item will be entered in the register
when decided.

| ID | Issue | DFI evidence | Recommendation | Alternative |
|---|---|---|---|---|
| **DR-01** | What counts as "two or more pages" for page-1 numbering? Does a one-page directive with an annex count? | 3.2.11(1), 3.2.18(1). Annexes are numbered A-1 independently when unclassified (1.2.24). Fig 3-5 p1 shows **no** page number, which conflicts with the prose; Fig 3-6 p1 shows "1". | Count the main document only (SECTIONPAGES). The prose governs Fig 3-5. Log the Fig 3-5 conflict. | Count every page in the file (NUMPAGES). |
| **DR-02** | AI page numbering. 3.2.22 has no page-number rule, but Fig 3-7 shows "(Page 1 of 2)" on an unmarked template. | 1.2.16(6), 1.2.16(7); A-11 | Confirm that A-11 applies: the general rule, so page 1 is unnumbered and later pages carry plain numbers. "Page n of N" applies only above Restricted. | Treat the AI as a directive: number page 1 when there are two or more pages. |
| **DR-03** | The AI cancellation paragraph is unnumbered in Fig 3-7. | 3.2.22a(7): first-level paragraphs are numbered (M); 1.2.23f | Number it (the prose governs). Log the figure conflict. | Reproduce the figure (needs N-8). |
| **DR-04** | Heading-only numbered paragraphs ("9. Planning guidance", "10. Finance", "Legal", "Reporting", "DIRLAUTH", "Points of contact") are drawn plain, with no full stop and the text in sub-paragraph a. | 1.2.17(4): a paragraph heading is bold sentence case with a full stop (M). Figs 3-5 and 3-7 draw them plain. Fig 3-6 draws "**Intent.**" per 1.2.17(4). | Render them as paragraph headings per 1.2.17(4): "10. **Finance.**", then "a. …". The current renderer already does this. | Reproduce the figures: a plain "Finance" with no full stop. |
| **DR-05** | AI section heading "Tasks" (Fig 3-7) vs "Instructions" (3.2.22a(6)). | The prose describes the section's content; it does not prescribe heading text. | "Tasks" (the template supplies the heading text). | "Instructions". |
| **DR-06** | Which sections are mandatory? The prose lists "key features"; the templates show more sections without "(remove if not required)". | 3.2.10, 3.2.17, 3.2.22a | **Required:** sections the prose makes mandatory, plus the fixed boilerplate (Authority, Applicability, Purpose).<br>- CDF Directive: also Context/Situation and Cancellation.<br>- Op Directive: Situation, Mission, Execution (Intent and Tasks), Coordinating instructions, Logistics and administration, Command and control and Acknowledgement.<br>- AI: also Introduction, the instructions section and Cancellation.<br>**Other template sections:** optional, omitted cleanly, and a warning names any that are omitted. | Every template section required. |
| **DR-07** | Date-line position. A-06 indents the date 1 cm for administrative documents (2.2.3(1), Part 2), but Figs 3-5 to 3-7 show it at the margin. | 2.2.3(1) is in Part 2 (correspondence and administrative documents); Part 3 is silent. | Margin for all three types (`[T]`; Part 2 does not govern Part 3). The day is handwritten by default (A-02). | 1 cm indent, as for administrative documents. |
| **DR-08** | Date format in the text. The Fig 3-5 cancellation shows "DD Mmm YYYY". 1.2.10b gives "2 Sep 16" for Directives (guidance). A-01: no leading zero. | 1.2.10b (D), Fig 3-5 (T), A-01 | The cancellation and other generated dates use "2 Sep 26" (1.2.10b names Directives explicitly; A-01 applies). Log the figure. | "2 Sep 2026" (four-digit year, as drawn, without the leading zero). |
| **DR-09** | Day names. 1.2.10a: spell the day out in full in orders. 1.2.10d: the combined form for directives and orders is "Mon, 16 1300 Aug 21" (abbreviated). | 1.2.10a vs 1.2.10d | Warn on abbreviated day names, except in the 1.2.10d combined day-date-time form. Warn only; never rewrite. | Warn on every abbreviated day. |
| **DR-10** | Copy-number placement on the Op Directive: in the body at the left above the date (Fig 3-6), vs header right (A-21, decided). | 1.2.16(9), A-21 | Keep A-21 (header, right-aligned). Log the Fig 3-6 conflict. | Body, as drawn in Fig 3-6 (type-specific override). |
| **DR-11** | Op Directive minimum elements (3.2.17(5)–(7): "must comprise the following minimum elements"). Fig 3-6 shows one free paragraph for each section. | 3.2.17(5)–(7) (M) | Structured, required sub-paragraphs a., b., … in the prose order, each with a paragraph heading taken from the prose wording ("Command and control arrangements", "Locations", "Timings", …). The headings are an implementation decision `[I]` (not drawn in Fig 3-6), so they need your approval. | Free text, with a warning when an element appears to be missing (weaker). |
| **DR-12** | 3.2.16c: "the format may be changed to suit the particular circumstances of an operation". | 3.2.16c (D) | Fixed section order, plus optional author-supplied additional group-headed sections before Acknowledgement. Each one is reported as a format variation. | No variation allowed. |
| **DR-13** | COS/commander and senior-executive directives (3.2.12, 3.2.13). Their identifier wording and Authority wording are not given. | 3.2.12, 3.2.13b ("should generally conform") | Implement them as an `issuer` option on the CDF Directive template:<br>- identifier "[APPOINTMENT] DIRECTIVE NN/YYYY";<br>- Authority text supplied by the author;<br>- badge per rule (commander: optional Service, command or unit badge placeholder; senior executive: none);<br>- Applicability boilerplate unchanged;<br>- the one-year rule (3.2.9d is about CDF Directives) is a warning only. | Defer the variants; CDF Directive only. |
| **DR-14** | "for" signatory. VCDF or CoS HQNZDF signs over CDF's block and **handwrites** "for". | 3.2.11(7), 3.2.18(7) | Always render CDF's block. Render nothing for "for", because it is handwritten. The schema fixes the appointment line as "Chief of Defence Force". | An option to type "for". |
| **DR-15** | "See distribution" weight: bold in Fig 3-5, regular in Fig 3-7 (and in Fig 3-6 under "For information"). | Figs 3-5 to 3-7 (T) | As drawn for each type (N-7). | Bold everywhere. |
| **DR-16** | AI Purpose: "one or two short sentences" (3.2.22a(4)) vs the Fig 3-7 stem "is—" plus a lettered item. | 3.2.22a(4), Fig 3-7 | Template stem with one or two items; a warning when there are more than two. | Free sentences without the stem. |
| **DR-17** | The one-year limit for CDF Directives (3.2.9d, M). | 3.2.9d | Schema **error** if the cancellation date is more than one year after the date of signature. A handwritten day gives month precision. | Warning only. |

Apparent DFI errors (proposed for register section E; not corrected unless you approve):

| ID | Location | Text in DFI | Suggested correction |
|---|---|---|---|
| E-13 | Fig 3-5 para 15, first option | "…have been incorporated in DFO 14 and no later than DD Mmm YYYY." "DFO 14" is printed as fixed black text, not as a placeholder. | Treat it as a field: "[parent publication]". Default to the verbatim "DFO 14" until you decide. |
| E-14 | Fig 3-7 paras 1–4 and Cancellation | "Administrative Instruction" (paras 1–3) vs "administrative instruction" (para 4 stem, Cancellation) | Reproduce verbatim (the capitalisation is inconsistent, but each form is plausible). Correct it only if you direct. |

Out of scope (DFI defers elsewhere; recorded, not implemented):

- FRAGO format and the mission close-off signal (AC SCE, 3.2.16c–d);
- CDF Warning Orders and Administrative Warning Orders ("no particular format", 3.2.15, 3.2.21b(1)(c));
- OPORD and OPINST (COMJFNZ standards, 3.2.19);
- the CDF Directive register (CoS HQNZDF, 3.2.9g).

Directive and Op Directive numbers are supplied by OCDF and AC SCE. They are input only and never generated.

## 6. Proposed tests

The existing 107 tests must keep passing unchanged.

| ID | Test |
|---|---|
| T-R1 | Regression: every Phase 1–2 fixture renders text identical to its pre-Phase-3 output, and lints clean. |
| T-S1 | Schema rejects a missing mandatory element for each type: the DR-06 list, the identifier number and year, the AI issuing appointment, a cancellation date (AI and CDF Directive), and Op Directive Acknowledgement. |
| T-S2 | Schema rejects bullets in any of the three types (1.2.23g). |
| T-S3 | More than four addressees with no distribution list is rejected; with a distribution list, "See distribution" is rendered (AI and CDF Directive). |
| T-S4 | Op Directive: the action addressee is COMJFNZ; information addressees appear only as "For information / See distribution". |
| T-S5 | Badge rules: the CDF Directive and Op Directive require the badge slot; the AI and senior-executive directive reject a device; for commanders it is optional. |
| T-S6 | CDF Directive cancellation date more than one year after the date: error (DR-17). |
| T-S7 | Op Directive minimum elements (DR-11): each one missing is rejected. |
| T-B1 | Boilerplate is verbatim: Authority, Applicability (3D paras 2–4; 3F paras 2–3), Purpose stems and cancellation wordings match the DFI text extraction character for character, apart from fields. |
| T-B2 | The AI Authority paragraph fills its number from the identifier ("Administrative Instruction 07/2026 is issued by …"). |
| T-L1 | Scheme D geometry in the .docx: level 1 number at 0 cm with text and turnover at 1 cm; levels 2–4 per the tokens (lint N-3). |
| T-L2 | Identifier paragraph immediately precedes the subject or operation-name paragraph. It is bold upper case. |
| T-L3 | Page-number regime: the CDF Directive and Op Directive first-page footer carries the conditional PAGE field. The AI follows 1.2.16(6). Above Restricted, "Page n of N" appears on every page. Lint passes for each case (N-1, N-2). |
| T-L4 | Group headings unnumbered and continuous paragraph numbering across them (1 … 15 in the 3D structure fixture). |
| T-L5 | Heading-only paragraphs render per DR-04. |
| T-L6 | Optional sections omitted cleanly: no empty headings and no DFI instruction text (CLAUDE.md §3 rule 8). |
| T-W1 | Order wording warnings: a colon lead-in warns; an em dash does not; an abbreviated day warns except in the 1.2.10d form; a Tasks paragraph without mandatory language warns; an annex or enclosure not cited in the text warns. |
| T-W2 | Correspondence warnings are unchanged (an em dash in a minute still warns). |
| T-V1 | Fixtures render and lint clean, and their PDFs pass the markings-on-every-page and signature-orphan checks. |
| T-V2 | Visual comparison: `3f-structure`, `3d-structure` and `3e-structure` against PDF pp 178–179, 167–168 and 173–174, with differences listed in each `NOTES.md`. |

Fixtures (fictional content, or the DFI placeholder text; no real operation names):

| Template | Fixtures |
|---|---|
| `administrative-instruction/` | `3f-structure` (Fig 3-7 re-keyed); `variant-distribution` (more than four addressees, annex and enclosure); `variant-classified` (CONFIDENTIAL, copy number, Page n of N) |
| `cdf-directive/` | `3d-structure` (two or more pages: page 1 numbered); `variant-single-page` (page 1 unnumbered); `variant-commander` (optional badge); `variant-senior-executive` (no badge); `variant-classified` |
| `cdf-operational-directive/` | `3e-structure` (Fig 3-6 re-keyed, with fictional "OPERATION EXAMPLE" and the minimum elements); `variant-classified-copy` (a marking from DFI 5.1 only, copy number, annexes) |

The expected number of new tests is about 40. Word check V-05 is added for a
person to run in Microsoft Word.

## 7. Implementation sequence (after approval)

1. Record the DR decisions in the register; update the tokens (N-6 size) and the standards where needed.
2. Shared capabilities N-1 to N-5 (and N-7/N-8 if decided), each with its regression test T-R1 first.
3. **Administrative Instruction**: template, schema, NOTES, fixtures, comparison.
4. **CDF Directive** plus the variants (DR-13).
5. **CDF Operational Directive.**
6. Records: inventory items 8, 9 and 24; register; README; implementation plan.
7. Full test run, then the review point. Commit and push to `claude/dfi-foundation`.

Proposed review point: one at the end of the family, matching Phase 2. If you
prefer a gate after the AI, say so.

## 8. Inputs needed from you

| Item | Needed for |
|---|---|
| Decisions DR-01 to DR-17, E-13, E-14 | Before step 1 |
| Official NZDF badge artwork (T-05), or continued labelled placeholders | CDF Directive and Op Directive (placeholders by default) |
| Authoritative appointment-abbreviation list (A-10) | F-10 can only be checked once it exists. Until then it is not checked. |
| Marking vocabulary (A-13) | Unchanged: DFI 5.1 markings only |
| Word version and OS, and the V-01 to V-03 observations, for the validation record | `templates/minute/NOTES.md` §7 |
