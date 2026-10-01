# Visit report / Post activity report: traceability notes

Status: **implemented (Phase 2); provisionally accepted 2026-10-01.** Word checks
V-01 to V-04: PASSED in Microsoft Word 2026-10-01 (record in
`templates/minute/NOTES.md` §7).

## 1. DFI sources

| Source | Reference | PDF pages |
|---|---|---|
| Prose | 2.2.9 (use), 2.2.10 (layout), 2.2.11 (structure); 2.2.1–2.2.3 (administrative documentation) | 101–103 |
| Template | Annex 2Q, Fig 2-19 | 107–109 |
| Example | Annex 2P, Fig 2-18 | 104–106 |

## 2. Structure (as implemented, in order)

| # | Element | Tag | Source |
|---|---|---|---|
| 1 | Markings; classified no lower than the activity (reminder only) | [M] | 2.2.10(1) |
| 2 | Date (Mmm yy indented 1 cm) + file reference right | [M] | 2.2.3(1), 2.2.10(3) |
| 3 | Action addressee(s), bold, "(through …)" | [M] | 2.2.10(4) |
| 4 | "For information" + addressees, **or** "For information / See distribution" | [T] | Figs 2-18, 2-19 |
| 5 | Subject "VISIT REPORT – …" / "POST ACTIVITY REPORT – …" | [M] | 2.2.10(5) |
| 6 | Introduction (date, time, location, purpose, participants) | [M] | 2.2.11(1) |
| 7 | "Visit report" / "Post activity report" group heading + content | [M] / [T] | 2.2.11(2); Fig 2-19 |
| 8 | Decisions: lead + Agreement / For action / For information / Further action | [M] | 2.2.11(4) |
| 9 | Background information (warning if absent) | [D] | 2.2.11(5) |
| 10 | Conclusion(s) (optional) | [D] | 2.2.11(7) |
| 11 | Recommendation(s) (optional) | [D] | 2.2.11(8) |
| 12 | Signature (SB-MINUTE): senior member (reminder only) | [M] | 2.2.10(7) |
| 13 | DTelN | [T] | Fig 2-19 |
| 14 | Annex(es): **Annex A Summary of travel details is always first** | [M] | 2.2.10(9), 2.2.11(3) |
| 15 | Enclosure(s), Distribution: | [T] | Fig 2-19 |
| 16 | Annex A: identifying block, SUMMARY OF TRAVEL DETAILS, travel table | [M] / [T] | 2.2.10(9); Fig 2-19 p3 |

Plain paper, no device (2.2.10(2)). The travel table uses the shared DFI table
style: 0.5 pt borders, 10 pt content, header row repeated, centred (1.2.25).

## 3. Shared rules used and engine additions

Uses the Minute's shared blocks unchanged. Additions made for this template,
available to every template:
- `tables.py` + `Table` / `Cell` / `TableBlock` content models: DFI tables
  in any body.
- `addressees` option `distribution_mode: info`. The default behaviour of
  existing templates is unchanged.

## 4. Implementation decisions (I-V)

| ID | Decision | Why |
|---|---|---|
| I-V1 | The subject prefix is generated from `report_type`; the author gives only the title | 2.2.10(5) makes the first words mandatory |
| I-V2 | The travel table is generated from structured fields with the template's row labels, verbatim | Fig 2-19 p3; prevents omission of mandatory cost lines (2.2.10(9)) |
| I-V3 | "Event" and "Dates" rows span the full width with the value in bold (**approved 2026-10-01**) | Fig 2-19 shows "[Event]" and "[Dates]" as full-width bold placeholders (2P shows labels instead; the template governs) |
| I-V4 | The 2P footnote "All details must be consistent with the approved travel claim" is not reproduced | Absent from template 2Q (the template governs) |
| I-V5 | Annex A identifier "VISIT REPORT [file ref]" / "POST ACTIVITY REPORT [file ref]" + report date, upper case | Fig 2-18 "Visit Report ABC 8000-000 / DD Mmm YY"; upper case per A-12 |
| I-V6 | The content group heading follows the report type ("Visit report" or "Post activity report") | Fig 2-19 shows "Visit Report"; the DFI gives no PAR form. Sentence case per 1.2.17(3). |
| I-V7 | Information addressees are given either as a list or via a distribution list, not both | Figs 2-18, 2-19 replace the information list with "See distribution" |
| I-V8 | Warnings: report more than 14 days after `activity_end`; empty travel table; standing reminders (classification of the activity, senior signatory) | 2.2.9a "normally within two weeks"; 2.2.10(1), (7) cannot be machine-checked |

## 5. Validation record (2026-10-01)

| Fixture | Purpose | Result |
|---|---|---|
| `2p-example.yaml` | Re-key of Annex 2P | 3 pp; lint clean |
| `2q-structure.yaml` | Element set and order of 2Q, filled travel table | 3 pp; order and table tests pass |
| `variant-par.yaml` | Post activity report, RESTRICTED, information list, late report, Annex B | Two-week warning; Annex B after Annex A |

Differences from Figs 2-18 and 2-19 (`output/comparisons/vr-*`):

| ID | Difference | Disposition |
|---|---|---|
| DV-01 | 2Q shows the date at the margin; ours indented 1 cm | 2.2.3(1) prose governs (A-06) |
| DV-02 | Annex A identifier is mixed case in 2P; ours upper case | A-12 decided |
| DV-03 | 2P footnote on "Expense" not reproduced | I-V4 (template governs) |
| DV-04 | The DFI table is about 90 per cent of the text width; ours 15 cm of 16 cm | Minor [T]; within margins (1.2.25a) |
| DV-05 | 2P "(incl. Taxi, …)" has a capital T and a smaller font | Template 2Q wording and size used ("taxi", 10 pt) |
| DV-06 | Annex page-number field shows "1A-" in the preview | V-01 (Word verification) |
