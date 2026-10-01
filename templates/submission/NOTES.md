# Submission: traceability notes

Status: **implemented; review decisions S-01 and S-02 approved 2026-10-01. Accepted 2026-10-01; Word checks V-01 to V-04 passed.** It shares every engine component with
the Minute. The only engine change is a `compose_body()` hook, which lets a
schema map structured fields onto the shared body blocks.

## 1. DFI sources

| Source | Reference | PDF pages |
|---|---|---|
| Prose | 2.1.12 (structure of a submission); 2.1.10–2.1.11 apply because a submission is a minute (2.1.12a, fn 32) | 64–66 |
| Template | Annex 2F, Fig 2-6 | 76–77 |
| Example | Annex 2E, Fig 2-5 | 74–75 |

## 2. Structure (as implemented, in order)

The header and closing are identical to the Minute (`templates/minute/NOTES.md`
§2, items 1–8 and 12–18), except that there is no Distribution block (I-S4).

| # | Element | Tag | Source |
|---|---|---|---|
| B1 | **Purpose** group heading | [M] | 2.1.12b(1) |
| B2 | 1. **Issue.** One or two short sentences (warning if longer) | [M] | 2.1.12b(1)(a) |
| B3 | 2. **Recommendation(s).** Lead + single-sentence note/agree list, bold verbs | [M] | 2.1.12b(1)(b), 1.2.11(2) |
| B4 | 3. **Timing.** Omitted when timing has no bearing | [M] | 2.1.12b(1)(c) |
| B5 | **Context** group heading, then the author's blocks (group, main and paragraph headings allowed) | [M] / [T] | 2.1.12b(2); Fig 2-6 |
| B6 | Consultation (a paragraph, sub-paragraph or group heading) must be present | [M] / [T] | 2.1.12b(2)(e); Fig 2-6 f. |
| B7 | n. **Financial and resource implications.** Mandatory; state "none" if there are none. Its position is [I] (S-02). | [M] / [I] | 2.1.12b(3); A-34; S-02 |
| B8 | **Summary** (optional; no new information) | [D] | 2.1.12b(4) |
| B9 | Signature block as for minutes | [M] | 2.1.12b(5) |

Length: ideally four pages or fewer (2.1.12b(6)). Lint warns when the main
document (before the first annex) exceeds four pages.

## 3. Shared rules used

Everything listed in the Minute notes §3. No overrides.

## 4. Implementation decisions (I-S)

| ID | Decision | Why |
|---|---|---|
| I-S1 | The body is given as structured fields (`issue`, `recommendations`, `timing`, `context`, `financial_and_resource_implications`, `summary`) and composed into shared blocks | The schema can enforce 2.1.12b's mandatory elements; no submission-specific rendering code |
| I-S2 | Financial and resource implications is a numbered first-level paragraph with a paragraph heading, placed after Context and before Summary. **[I]**: the paragraph is DFI-mandated but its position is our decision. **Approved 2026-10-01 (S-02).** | 2.1.12b(3) requires "a paragraph heading". The template gives no position; this follows the prose order of 2.1.12b ((2) Context → (3) F&R → (4) Summary). |
| I-S3 | Context is free-form apart from requiring Consultation. The 2F sub-headings Content, Sections, Argument, Implications and Effects are **not** forced | 2.1.12b(2) describes them as considerations ("depends on", "where appropriate", "may be split into sections"). Only consultation is an "are to" (2.1.12b(2)(e)). **Approved 2026-10-01 (S-01).** |
| I-S4 | No Distribution block | Not in template 2F. There should be only one addressee (2.1.11(6)). |
| I-S5 | "Recommendation." or "Recommendations." by number of items | A-27 applied to the template's "Recommendation(s)." |
| I-S6 | Over four pages → lint warning, not error | 2.1.12b(6) says "ideally" |
| I-S7 | Warning when no item uses **agree** or **approve** | A submission seeks a decision (2.1.12a; 2.1.12b(1)(b) "use 'agree' to identify where a decision is required") |
| I-S8 | More than one action addressee → warning, not error | 2.1.11(6) says "should" |

## 5. Validation record (2026-10-01)

| Fixture | Purpose | Result |
|---|---|---|
| `2e-example.yaml` | Re-key of Annex 2E (with the F&R paragraph added per A-34) | 2 pp; lint clean |
| `2f-structure.yaml` | Element set and order of Annex 2F, with an annex | 3 pp; order test passes |
| `variant-long.yaml` | CONFIDENTIAL, no Timing, two addressees, over four pages | "Page n of N"; warnings for addressees and length |

Differences from Figs 2-5 and 2-6 (LibreOffice preview; images in
`output/comparisons/submission-*`):

| ID | Difference | Disposition |
|---|---|---|
| DS-01 | 2E identifier is about 12 pt and set tight under the descriptor; 2F (like 2D) shows 16 pt | Template governs (I-M1) |
| DS-02 | 2E date "01 Jun 25" (leading zero, slight indent); ours "1 Jun 25" at the margin | A-01 decided; I-M3 (typed day at the margin) |
| DS-03 | 2E "COMLOG" not bold; ours bold | D-01 decided (bold all action addressees) |
| DS-04 | Ours adds "Financial and resource implications." (para 5); Summary becomes para 6 | A-34 decided |
| DS-05 | 2F shaded signature box | D-06 decided: not implemented, unresolved |
| DS-06 | 2E italic annotations "(remove this block if not required)" | Omitted: DFI instructions, not content (CLAUDE.md §3 rule 8) |
| DS-07 | Page break positions | Expected (illustrative pagination) |

Word verification items V-01 to V-04 from the Minute apply equally. **Status: PASSED in Microsoft Word 2026-10-01** (record in `templates/minute/NOTES.md` §7).
