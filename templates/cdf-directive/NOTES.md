# CDF Directive (with commander and senior-executive variants): traceability notes

Status: **implemented (Phase 3, directive family); awaiting the family review
gate.** Word check **V-05** (page-1 conditional number): **NOT TESTED**.

## 1. DFI sources

| Source | Reference | PDF pages |
|---|---|---|
| Prose | 3.2.8 (issuing directives), 3.2.9 (CDF Directives), 3.2.10 (content), 3.2.11 (layout), 3.2.12 (COS and commanders), 3.2.13 (senior executives), 3.2.14 (legal advice); fn 23; 1.2.10, 1.2.17, 1.2.23, 1.2.26 | 158–160 |
| Template | Annex 3D, Fig 3-5 | 167–168 |
| Example | none | – |

## 2. Structure (as implemented, in order)

[M] = DFI prose, enforced by the schema. [T] = Fig 3-5 only. It is optional,
omitted cleanly, and a warning names it (DR-06).

| # | Element | Tag | Source |
|---|---|---|---|
| 1 | Markings | [M] | 1.2.16(5) |
| 2 | Badge top left (official artwork, 2.5 cm); address line top right | [M] badge; [T] address | 3.2.11(2); Fig 3-5; A-14; BR-01, BR-05 |
| 3 | Date at the margin (abbreviated; day handwritten by default) | [M] | 3.2.9d; 1.2.10b; DR-07; A-02 |
| 4 | Addressees (four or fewer) **or** "See distribution" (bold) | [M] | 3.2.11(3); DR-15 |
| 5 | "CDF DIRECTIVE NN/YYYY", bold upper case, immediately above the subject | [M] | 3.2.11(4) |
| 6 | SUBJECT HEADING | [M] | 3.2.11(5) |
| 7 | Authority: "Issued by the Chief of Defence Force." | [M] | 3.2.10(1); Fig 3-5 para 1 |
| 8 | Applicability: paras 2–4, fixed wording; para 3 completed by `responsibilities` | [T] | Fig 3-5 |
| 9 | Purpose: "The purpose of this Directive is—", then "a. to …" ("to" is fixed) | [M] | 3.2.10(2) |
| 10 | Context/Situation | [M] | 3.2.10(3) |
| 11 | Conduct; Accountabilities and responsibilities | [T] | Fig 3-5 |
| 12 | Coordinating arrangements: **Planning guidance.** | [T] | Fig 3-5; DR-04 |
| 13 | Administration: **Finance.** **Legal.** | [T] | Fig 3-5; DR-04 |
| 14 | Command and control: **Reporting.** **DIRLAUTH.** **Points of contact.** | [T] | Fig 3-5; DR-04 |
| 15 | Cancellation and disposal instructions: one of the two Fig 3-5 wordings, date "31 Mar 27" | [M] | 3.2.10(4); DR-08; E-13 |
| 16 | Signature: NAME / rank / Chief of Defence Force (no typed "for") | [M] | 3.2.11(7); DR-14 |
| 17 | Annex(es), Enclosure(s), Distribution: ; annex pages in scheme D | [D] | 3.2.11(8); fn 23 |
| — | Page numbers: every page including page 1 when the **main document** has two or more pages | [M] | 3.2.11(1); DR-01; V-05 |

**Rejected by the schema:**
- a missing Purpose, Context/Situation, cancellation (option and full date),
  number, year, subject, date or signature;
- a missing badge, or a badge other than the NZDF or CDF gold-leaf badge
  (3.2.11(2); BR-04);
- a signature appointment other than "Chief of Defence Force" (3.2.11(7));
- a cancellation date more than one year after signature (3.2.9d; DR-17);
- a changed identifier or Authority wording;
- more than four addressees without a distribution list;
- bullets;
- Purpose items that repeat the fixed "to".

**Warnings:**
- omitted template sections (DR-06);
- the fixed "DFO 14" reference (E-13);
- annexes in a CDF Directive ("exceptional circumstances", 3.2.11(8));
- the order wording checks (see the AI notes).

## 3. Variants (DR-13; `issuer`)

| `issuer` | Identifier | Authority | Badge | One-year limit |
|---|---|---|---|---|
| `cdf` (default) | CDF DIRECTIVE NN/YYYY | Fixed (3.2.10(1)) | Required: NZDF or gold-leaf (3.2.11(2); BR-04) | Error (DR-17) |
| `commander` (3.2.12) | [APPOINTMENT] DIRECTIVE NN/YYYY | Author's text; reported if omitted | Optional: Service badge or NZDF badge (3.2.12b) | Not applied (3.2.9d is about CDF Directives) |
| `senior_executive` (3.2.13) | [APPOINTMENT] DIRECTIVE NN/YYYY | Author's text; reported if omitted | Rejected (3.2.13c) | Not applied |

The variants share every other rule. 3.2.13b says these directives "should
generally conform to the layout for a CDF Directive". 3.2.12 gives commanders
no separate layout, so the CDF layout is used (DR-13).

## 4. Implementation decisions (I-C)

| ID | Decision | Reason |
|---|---|---|
| I-C1 | Variant identifiers are numbered ("[APPOINTMENT] DIRECTIVE NN/YYYY"), and the number is required. | 3.2.13b (layout conforms to the CDF Directive); DR-13. No DFI figure shows a variant identifier. |
| I-C2 | Command and unit badges are not held, so a commander may use a Service badge or the NZDF badge only. | 3.2.12b allows a Service, command or unit badge. Only the Service and NZDF badges are in the VIS (SOURCE.md). |
| I-C3 | The page-1 field caches "1". LibreOffice shows "1" on a one-page directive. Word recalculates the field (V-05). | DR-01. The page count is not known when the document is generated. |
| I-C4 | Listed addressees use the shared bold addressee lines, as for the AI (I-A1). | Fig 3-5 shows one bold placeholder "[Addressee or See distribution]". |

## 5. Differences from Fig 3-5

| ID | Difference | Disposition |
|---|---|---|
| DC-01 | Fig 3-5 page 1 shows no page number | DR-01: the prose (3.2.11(1)) governs; page 1 is numbered when the main document has two or more pages. |
| DC-02 | "Planning guidance", "Finance" etc. are plain in Fig 3-5 | DR-04: bold with a full stop (1.2.17(4)). |
| DC-03 | "DD Mmm YYYY" in the cancellation wording | DR-08: "31 Mar 27" (1.2.10b; A-01). |
| DC-04 | The italic "or" between the two cancellation wordings | One wording is chosen (`cancellation.option`). "or" is template guidance, not content. |
| DC-05 | Light-blue signature box | Not reproduced (D-06). |
| DC-06 | Placeholders in red | Black text (1.2.16(4)). |

## 6. Validation record (2026-10-01)

| Fixture | Purpose | Result |
|---|---|---|
| `3d-structure.yaml` | Every Fig 3-5 element; distribution; two pages | 2 pp; lint clean; page 1 numbered; compared with PDF pp 167–168 |
| `variant-single-page.yaml` | One page, two addressees, "with effect" wording | 1 p; conditional field present (V-05) |
| `variant-commander.yaml` | CA directive, Army badge, author's Authority | Lint clean |
| `variant-senior-executive.yaml` | CFO directive, no badge | Lint clean; no picture |
| `variant-classified.yaml` | CONFIDENTIAL, copy number, annex introduced in the text | "Page n of N" on every page; lint clean |

Visual comparison: LibreOffice with Carlito standing in for Calibri. The
layout, element order, numbering geometry, badge position and fixed wording
match Fig 3-5, apart from DC-01 to DC-06. Tests:
`renderer/tests/test_cdf_directive.py`.
