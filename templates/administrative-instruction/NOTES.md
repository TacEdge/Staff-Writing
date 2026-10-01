# Administrative Instruction: traceability notes

Status: **implemented (Phase 3, directive family); awaiting the family review
gate.** Word check V-05 does not apply: an AI follows the general page-number
rule (DR-02).

## 1. DFI sources

| Source | Reference | PDF pages |
|---|---|---|
| Prose | 3.2.21 (coordination of non-operational activities; AIs), 3.2.22 (layout conventions); fn 23 (hanging indents); 1.2.10, 1.2.17, 1.2.23 | 176–177 |
| Template | Annex 3F, Fig 3-7 | 178–179 |
| Example | none | – |

## 2. Structure (as implemented, in order)

[M] = required by DFI prose and enforced by the schema. [T] = shown in Fig 3-7
only. It is rendered when content is supplied, omitted cleanly otherwise, and a
warning names it (DR-06).

| # | Element | Tag | Source |
|---|---|---|---|
| 1 | Markings, header and footer | [M] | 1.2.16(5) |
| 2 | Originating HQ line: centred, bold, upper case, 16 pt; [Originator] line centred | [T] | Fig 3-7; size measured as A-22 |
| 3 | Date at the margin (day handwritten by default), file reference right | [M] date 3.2.22b; [T] position | DR-07; A-02 |
| 4 | Addressees (four or fewer) **or** "See distribution" (regular weight) | [M] | 3.2.22a(1); DR-15 |
| 5 | "[APPOINTMENT] ADMINISTRATIVE INSTRUCTION NN/YYYY", bold upper case, immediately above the subject | [M] | 3.2.22a(2) |
| 6 | SUBJECT HEADING | [M] | 3.2.22a(3) |
| 7 | Authority: "Administrative Instruction nn/yyyy is issued by …." (number taken from the identifier) | [T] | Fig 3-7 para 1 |
| 8 | Applicability: paras 2–3, fixed wording; para 3 completed by `applies_to` | [T] | Fig 3-7 paras 2–3 |
| 9 | Purpose: "The purpose of this Administrative Instruction is—", then lettered items | [M] | 3.2.22a(4); E-14; DR-16 |
| 10 | Introduction | [M] | 3.2.22a(5) |
| 11 | Conduct | [T] | Fig 3-7 |
| 12 | Tasks (author's group headings allowed) | [M] | 3.2.22a(6), (6)(c); DR-05 |
| 13 | Coordinating arrangements | [T] | Fig 3-7 |
| 14 | Administration: Finance, Legal (paragraph headings, bold with a full stop) | [T] | Fig 3-7; DR-04 |
| 15 | Command and control: Reporting, DIRLAUTH, Points of contact | [T] | Fig 3-7; DR-04 |
| 16 | Cancellation: "This Administrative Instruction is cancelled on 2 Sep 26.", **numbered** | [M] | 3.2.22a(6)(d), (7); DR-03; DR-08; E-14 |
| 17 | Signature: NAME / title-rank / organisation | [M] signed 3.2.22b; [T] lines | Fig 3-7 |
| 18 | Annex(es), Enclosure(s), Distribution: | [D] | 3.2.22a(8); A-27; A-04 |
| 19 | Annex pages (scheme D numbering) | [M] | 1.2.24; fn 23 |

**Rejected by the schema:**
- a missing Purpose, Introduction, Tasks, cancellation date (with day), date,
  signature, subject, or an identifier without authority and number;
- more than four addressees without a distribution list;
- both addressees and a distribution list;
- bullets (1.2.23g);
- a badge, crest or logo (3.2.22a(2));
- stem items carrying their own punctuation;
- a cancellation date before the date of issue.

**Warnings:**
- omitted template sections (DR-06);
- more than two Purpose items (DR-16);
- Tasks without mandatory language (3.2.21b(2)(e));
- a colon list lead-in (1.2.23c(2));
- abbreviated day names (DR-09);
- an annex or enclosure not introduced in the text (3.2.22a(8));
- the standard wording checks.

Em dashes are **not** reported in this family (A-07, 1.2.23c(2)).

## 3. Shared rules used

- Page setup, markings, fonts and copy number: `standards/`, tokens.
- Scheme D numbering (`numbering.directive`).
- The general page-number rule (DR-02, A-11).
- `orders.py`: distribution threshold, bullet ban, sub-structures and order
  warnings.
- Blocks: `originating_hq`, `directive_identifier`, `date_line`, `addressees`,
  `subject`, `body`, `signature` (admin), list blocks, `supporting_documents`.

## 4. Implementation decisions (I-A)

| ID | Decision | Reason |
|---|---|---|
| I-A1 | Listed addressees (four or fewer) use the shared addressee block, which renders them in bold. | No DFI AI figure shows listed addressees. The minute convention (D-01) is reused rather than a new format invented. |
| I-A2 | Annex and appendix paragraphs use scheme D. | fn 23: "Hanging indents are used in Directives, Orders and Instructions." Applies throughout the document. |
| I-A3 | The third signature line holds the sender organisation, in the shared `appointment` field. | Fig 3-7: "[Sender organisation]". |
| I-A4 | The identifier uses its own style (bold, body size, left margin), created only when used. | 3.2.22a(2). Accepted Phase 1–2 documents are left unchanged. |
| I-A5 | The Authority wording uses a two-digit number ("07/2026"), as the identifier does. | Fig 3-7 "[nn/yyyy]"; 2.1.11(3) form. |

## 5. Differences from Fig 3-7

| ID | Difference | Disposition |
|---|---|---|
| DA-01 | Fig 3-7 shows "(Page 1 of 2)" on an unmarked template | DR-02 / A-11: general rule. Page 1 unnumbered; plain numbers from page 2; "Page n of N" only above Restricted. |
| DA-02 | The Fig 3-7 cancellation paragraph is unnumbered | DR-03: numbered (3.2.22a(7)). |
| DA-03 | Fig 3-7 shows "Finance", "Legal" etc. plain, without a full stop | DR-04: bold with a full stop (1.2.17(4)). |
| DA-04 | "this administrative instruction" (Purpose stem, Cancellation) | E-14: capitalised. |
| DA-05 | The light-blue signature box | Not reproduced (D-06). |
| DA-06 | Fig 3-7 placeholders are red | Black text, per 1.2.16(4). The red marks DSWT fields only. |

## 6. Validation record (2026-10-01)

| Fixture | Purpose | Result |
|---|---|---|
| `3f-structure.yaml` | Every Fig 3-7 element, distribution list, annex and enclosure | Renders 4 pp; lint clean; compared with PDF pp 178–179 |
| `variant-minimal.yaml` | Prose-mandatory elements only; four addressees | Only Purpose, Introduction, Tasks and Cancellation headings; DR-06 warning |
| `variant-classified.yaml` | CONFIDENTIAL with endorsement; copy number; sub-paragraphs to (a); two Purpose items | "Page n of N" on every page; lint clean |

Visual comparison: LibreOffice with Carlito standing in for Calibri. The
element order, headings, numbering geometry and fixed wording match Fig 3-7,
apart from DA-01 to DA-06. Tests: `renderer/tests/test_administrative_instruction.py`.
