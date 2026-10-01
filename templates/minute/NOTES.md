# Minute: traceability notes

Status: **implemented (Phase 1); gate review passed 2026-10-01 with decisions D-01, D-06, D-09 and D-10.** Not yet verified in MS Word
(see §7, items V-01 to V-04).

## 1. DFI sources

| Source | Reference | PDF pages |
|---|---|---|
| Prose | 2.1.3 (correspondence conventions), 2.1.10 (use of minutes), 2.1.11 (minute layout conventions), plus Part 1 Ch 2 shared rules | 59–60, 69–71 |
| Template | Annex 2D, Fig 2-4 | 72–73 |
| Example | Annex 2C, Fig 2-3 | 70–71 |
| Layout reference | Annex 1A, Figs 1-4 to 1-6 | 49–53 |

## 2. Structure (as implemented, in order)

| # | Element | Tag | Source | Notes |
|---|---|---|---|---|
| 1 | Protective markings, header and footer, every page | [M] | 1.2.16(5), 1.2.18 | Mirror order; omitted when unclassified (fn 24) |
| 2 | Originator descriptor, centred, bold, 16 pt | [M] / [T] | 2.1.3(1); Fig 2-4 | Size measured from Fig 2-4 (A-22): I-M1 |
| 3 | Identifier "[Appointment] MINUTE [nn/yyyy]", centred, bold, 16 pt | [M] / [T] | 2.1.11(3) | Appointment and number optional |
| 4 | Date (dd Mmm yy) and file reference (right margin) on one line | [M] | 2.1.11(2), (4); 2.1.3(2) | Handwritten-day form indented 1 cm (A-06); typed day at the margin (I-M3) |
| 5 | Action addressee(s), bold, "(through X)" not bold | [M] / [T] | 2.1.11(5); Fig 2-3 | I-M2 |
| 6 | "For information" + up to six addressees | [M] | 2.1.11(5) | Over six → schema error |
| 6a | or "See distribution" (bold) | [D] | 2.1.11(7) | Mutually exclusive with 5–6 (I-M6) |
| 7 | SUBJECT HEADING, bold, upper case | [M] | 2.1.11(8), 1.2.17(1) | Upper-cased automatically, with a warning (I-M9) |
| 8 | Reference(s), lettered A. | [D] | 2.1.11(9), 1.2.19a | "Reference"/"References" by count (A-03) |
| 9 | Body: group, main and paragraph headings; scheme C numbering | [M] | 1.2.17, 2.1.3(3) | Single first-level paragraph not numbered |
| 10 | Purpose (recommended first) | [D] | 2.1.11(11) | Warning if absent |
| 11 | Recommendations: group heading, lead, single-sentence list, bold verbs | [M] | 2.1.11(13), 1.2.11(2), 1.2.23b(1) | Punctuation applied automatically (I-M5) |
| 12 | Six blank lines, then the signature block (SB-MINUTE) | [M] | 1.2.21c, 2.1.11(17) | Last text paragraph kept with the block (orphan rule) |
| 13 | DTelN line | [T] | Fig 2-4 | Optional |
| 14 | Annex(es) list | [M] | 1.2.24(1)(a) | Singular/plural (A-27) |
| 15 | Enclosure(s) list | [M] | 1.2.24(3) | Singular/plural (A-27) |
| 16 | "Distribution:" list | [D] | 2.1.11(7) | Colon per prose (A-04) |
| 17 | Copy Distribution | [M] | 1.2.16(9) | Only with numbered copies |
| 18 | Annex and appendix pages in the same file | [M] | 1.2.24(6), 2.1.11(16) | Warning when an annex is listed without content |

Page furniture: unclassified/restricted documents leave page 1 unnumbered and
show "2", "3"… (1.2.16(6), 2.1.11(18)). Above Restricted: "Page n of N" on every
page, annexes included (1.2.16(7)). Copy number right-aligned in the header on
page 1 (1.2.16(9); A-21). DRAFT watermark and double spacing for hard copy
(1.2.22).

## 3. Shared rules used

`standards/02` (page, fonts, spacing, markings, page numbers), `standards/03` §2
scheme C and §4 bullets, `standards/04` §1–2 (blocks, SB-MINUTE), `standards/05`
(annexes and appendices). Token keys: `page.*`, `font.*`, `spacing.*`,
`numbering.correspondence`, `numbering.references`, `numbering.annex_list`,
`numbering.enclosure_list`, `bullets.*`, `page_numbering.*`, `copy_number`.

## 4. Overrides

None. The minute uses the shared rules unchanged.

## 5. Verbatim text and section E corrections

- No fixed boilerplate in the minute.
- E-01 ("It is recommend that") is corrected in the 2C fixture under the
  section E policy (obvious typo).

## 6. Ambiguities and decisions applied

| Register | Applied |
|---|---|
| A-01, A-02, A-06 | No leading zero; day blank by default (1 cm indent); `date.day` for digital completion |
| A-03, A-04, A-27 | "Reference(s)"; "Distribution:" with colon; singular/plural list headings |
| A-05 | Turnover to the margin for first-level paragraphs (prose), although 2C mixes styles |
| A-07 | Em dash flagged as a warning in minute text |
| A-08 | Six blank 12 pt lines before the signature block |
| A-10 | "RANK, Service" when a Service is given, otherwise rank only; no rank list held |
| A-11 | First page unnumbered when Unclassified/Restricted |
| A-12 | Annex/appendix identifying block bold upper case; "APPENDIX n OF ANNEX X" |
| A-13 | Closed marking list from DFI only. An endorsement without a classification is a **warning**, not an error, because DFI's own Fig 2-13 shows IN CONFIDENCE alone (I-M13). |
| A-21 | Copy number in the header, right-aligned |
| A-22 | Descriptor and identifier 16 pt (measured), pending official templates |

### Implementation decisions that emerged (I-M)

| ID | Decision | Why |
|---|---|---|
| I-M1 | Descriptor and identifier 16 pt bold | Measured from Fig 2-4: glyph height is 1.33× the 12 pt body. Example 2C shows the descriptor at about 14 pt; the template governs. |
| I-M2 | Every action addressee in bold | Fig 2-4 shows "[Action addressee]" in bold. Fig 2-3's second line "COMD 1 BDE NZ" is not bold, and DFI does not say whether it is a second action addressee (D-01). |
| I-M3 | Typed day → date at the margin | The 1 cm indent exists to leave room for the handwritten day (2.2.3(1)). |
| I-M4 | Block spacing: one 12 pt line before each block; two before "For information" | Measured from Fig 2-4 (not in prose). |
| I-M5 | Recommendation and sentence-list punctuation applied by the renderer | Enforces 1.2.23b(1) consistently; authors give the items without list punctuation. |
| I-M6 | Distribution list and addressees are alternatives | 2.1.11(7) ("in place of the addressees"). Fig 2-3 shows both for illustration. |
| I-M7 | Single-page annex suppression uses a Word conditional field `{IF {SECTIONPAGES} > 1 "A-{PAGE}" ""}` | Word-native and survives later edits. LibreOffice cannot evaluate it (V-01). |
| I-M8 | Bullet glyphs: Symbol F0B7 (dot) and Wingdings F075 (diamond) | Word's standard glyphs. The Unicode ♦ fell back to a red emoji glyph. |
| I-M9 | Subject heading upper-cased automatically, with a warning | 1.2.9(6) is mandatory; the author's text is otherwise unchanged. |
| I-M10 | Style names "DFI …" plus Word's built-in "footnote text" and "footnote reference" | Readable in Word; can be remapped to official DSWT names later (T-03). |
| I-M11 | No "update fields on open" setting | Avoids a Word prompt on every open; Word updates header and footer fields anyway. |
| I-M12 | Copy number on a document not above Restricted → warning | Fig 1-4 fn 2. |

## 7. Validation record (2026-10-01)

Fixtures in `reference/fixtures/minute/`:

| Fixture | Purpose | Result |
|---|---|---|
| `2c-example.yaml` | Faithful re-key of Annex 2C | Renders 2 pp; lint clean; visual comparison below |
| `2d-structure.yaml` | Element set and order of Annex 2D | Order test passes (`test_2d_element_order`) |
| `variant-classified.yaml` | CONFIDENTIAL, copy number, distribution, multi-page, footnotes, annex + appendix | "Page n of N" on all 4 pp; markings mirror; signature kept with text |
| `variant-draft.yaml` | RESTRICTED, hard-copy DRAFT, single unnumbered paragraph, typed day | Watermark; double spacing on body text only |

Visual comparison (LibreOffice preview with Carlito; images in
`output/comparisons/`). Differences from DFI Figs 2-3 and 2-4:

| ID | Difference | Disposition |
|---|---|---|
| D-01 | "COMD 1 BDE NZ" is bold in ours, not bold in 2C | **DECIDED 2026-10-01:** bold all action addressees. The 2C inconsistency is retained here as a record. |
| D-02 | 2D shows the date at the margin; 2C indents it | Resolved by A-06 (indent when the day is handwritten) |
| D-03 | 2C turnover lines are mixed (paras 4 and 5 hang; 2, 5 and 6 return to the margin) | Resolved by A-05 (prose: margin) |
| D-04 | 2C shows addressees and a Distribution list together | Resolved by prose 2.1.11(7) (I-M6); exercised in `variant-classified` |
| D-05 | "Annex(es)" / "Enclosure(s)" literal headings | Resolved by A-27 |
| D-06 | 2D has a light-blue shaded signature box (probably a Word content control for a signature image) | **DECIDED 2026-10-01:** not implemented. **Unresolved** pending authoritative Word-template or digital-signature evidence. |
| D-07 | Gap between descriptor and identifier is slightly larger in 2D (about 10 pt vs our 6 pt) | Minor [T]. Would be settled by the official DSWT template (T-03). |
| D-08 | Page-break position differs from 2C | Expected: DFI figure pagination is illustrative |
| D-09 | Paragraph grading indicator "2.(U)" (2.1.11(12)) | **Deferred** (decided 2026-10-01) |
| D-10 | Single-approval "approved / not approved" statement above the signature (2.1.11(13)) | **Deferred** (decided 2026-10-01) |

### Needs verification in Microsoft Word (cannot be checked in this environment): status NOT TESTED

| ID | Item |
|---|---|
| V-01 | Annex/appendix page numbers: "A-1", "A-2" on multi-page annexes and none on a single-page annex (conditional field; LibreOffice shows "1A-"). |
| V-02 | DRAFT watermark appearance (VML; correct in LibreOffice). |
| V-03 | Footnote separator, numbering and 10 pt text. |
| V-04 | The file opens without a repair prompt, and the styles show in the Styles pane. |
