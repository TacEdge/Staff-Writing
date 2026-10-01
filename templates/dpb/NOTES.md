# Dot-point brief: traceability notes

Status: **implemented (Phase 2), awaiting review.** Word checks V-01 to V-04:
NOT TESTED.

## 1. DFI sources

| Source | Reference | PDF pages |
|---|---|---|
| Prose | 2.2.5 (briefs), 2.2.6 (purpose of a DPB), 2.2.7 (layout), 2.2.8 (content); 2.2.1–2.2.3 (administrative documentation) | 98–99, 90–91 |
| Template | Annex 2O, Fig 2-17 | 100 |
| Example | none | – |

## 2. Structure (as implemented, in order)

| # | Element | Tag | Source |
|---|---|---|---|
| 1 | Markings (header/footer) | [M] | 1.2.16(5) |
| 2 | Date (Mmm yy indented 1 cm; day handwritten) + file reference right | [M] | 2.2.3(1), (3) |
| 3 | "DOT-POINT BRIEF FOR [APPOINTMENT]" bold upper case | [T] | Fig 2-17 |
| 4 | SUBJECT HEADING | [M] | 2.2.3(4) |
| 5 | Purpose group heading + short statement (warning if absent) | [D] | 2.2.8d(1) |
| 6 | Group-headed numbered paragraphs with bullets (dot at 1 cm, text at 2 cm; diamond at 2 cm) | [D] / [M] | 2.2.8b, d(2); 2.2.7(2)–(3); 1.2.23g |
| 7 | Signature: NAME / rank / organisation | [T] | Fig 2-17 |
| 8 | DTelN line | [T] | Fig 2-17 |
| 9 | Annex(es) (optional) | [D] | 2.2.3(7) |
| 10 | Enclosure(s) | [T] | Fig 2-17 |
| 11 | Flags, lettered A. | [D] | 2.2.7(4), 1.2.24(4) |
| 12 | Commands, departments and authorities consulted (below the signature block) | [M] | 2.2.7(5) |

Margins: standard, or `margins: brief` for a 4 cm right margin (2.2.7(1) "may").
No identity device (2.2.3(2)). No addressee block (Fig 2-17).

## 3. Shared rules used

Scheme C numbering, bullets, page furniture, list blocks and supporting
documents, as for the Minute. New shared blocks added for the DPB, available to
any template: `title_line`, `flag_list`, `consulted`. A content-selectable
margin variant was also added (`margins`).

## 4. Implementation decisions (I-D)

| ID | Decision | Why |
|---|---|---|
| I-D1 | The schema rejects a Recommendations block | "A DPB does not seek a decision" (2.2.6) |
| I-D2 | The date is indented 1 cm, although Fig 2-17 shows it at the margin | 2.2.3(1) prose governs (DP-01) |
| I-D3 | Signature line 2 is the rank only (no Service) | Fig 2-17 "[Title/rank]" (unlike the minute's "[Title/rank, Service]") |
| I-D4 | Annexes allowed although Fig 2-17 lists none | 2.2.3(7): supporting documents may be included with all administrative documentation |
| I-D5 | Warning if a listed flag is not introduced in bold in the text, or if there are flags but no enclosure | 1.2.24(4)(a); 2.2.7(4) |
| I-D6 | "Format" in Fig 2-17 is treated as a placeholder group heading, not a fixed one | It sits in the same position as the minute's "[Group heading]"; 2.2.8d(2) says to use group headings to structure the text |

## 5. Validation record (2026-10-01)

| Fixture | Purpose | Result |
|---|---|---|
| `2o-structure.yaml` | Element set and order of Annex 2O | 1 p; lint clean; order test passes |
| `variant-brief-margin.yaml` | 4 cm right margin, RESTRICTED, typed day | Right margin 4.0 cm; lint clean |

Differences from Fig 2-17 (LibreOffice preview; `output/comparisons/dpb-2o-template-1.png`):

| ID | Difference | Disposition |
|---|---|---|
| DP-01 | Date at the margin in Fig 2-17; ours indented 1 cm | 2.2.3(1) prose governs (A-06) |
| DP-02 | Shaded signature box | D-06: not implemented, unresolved |
| DP-03 | "DTeIN" in Fig 2-17 | Rendered "DTelN" (E-02, typo correction policy) |
| DP-04 | No example annex exists | No re-keyed DFI example possible; structure checked against the template only |
