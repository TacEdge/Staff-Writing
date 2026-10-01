# Internal formal (demi-official) letter: traceability notes

Status: **implemented (Phase 2); provisionally accepted 2026-10-01.** Word checks
V-01 to V-04: PASSED in Microsoft Word 2026-10-01 (record in
`templates/minute/NOTES.md` §7).

## 1. DFI sources

| Source | Reference | PDF pages |
|---|---|---|
| Prose | 2.1.13 (use), 2.1.14 (writing), 2.1.15 (internal addressees), 2.1.16 (layout), 2.1.17 (salutation and close: internal) | 78–81 |
| Template | Annex 2H: Fig 2-8 (typewritten), Fig 2-9 (handwritten) | 84–85 |
| Example | Annex 2G, Fig 2-7 | 83 |

## 2. Structure (as implemented, in order)

| # | Element | Tag | Source |
|---|---|---|---|
| 1 | Markings, only in exceptional circumstances | [D] | 2.1.16(1) |
| 2 | Visual identifier top left (placeholder until artwork is supplied, T-05); unit name (bold) and address top right, 10 pt | [M] / [T] | 2.1.16(3)–(4); Figs 2-8, 2-9; A-14, A-33 |
| 3 | "From: [appointment or name]" centred, 12 pt before and after (optional) | [D] | 2.1.16(4) |
| 4 | Full date at the left margin (day blank by default) + file reference right, on the same line | [M] | 2.1.16(5)–(6); A-01, A-02 |
| 5 | Recipient: name, appointment/post (one addressee, by name) | [M] | 2.1.16(7), 2.1.17a |
| 6 | Salutation: typed / handwritten (space left) / none | [M] / [D] | 2.1.16(8), 2.1.17c–d |
| 7 | SUBJECT HEADING (optional) | [D] | 2.1.16(9) |
| 8 | Principal reference below the subject (optional) | [D] | 2.1.16(10) |
| 9 | Unnumbered paragraphs, paragraph headings allowed, no bullets | [M] | 2.1.16(12), 2.1.14b |
| 10 | Complimentary close, matching the salutation's format | [M] | 2.1.17d |
| 11 | Six lines, then INITIALS SURNAME (bold) / full rank / appointment (omitted if in the From line) | [M] | 1.2.21c, 2.1.16(17) |
| 12 | Enclosure(s) (no annexes) | [M] | 2.1.16(18) |

Page numbering: unclassified regime (2.1.16(19)). Footnotes allowed
(2.1.16(11)). No hyperlinks (Table 1-1).

## 3. Shared rules used and engine additions

New shared module `renderer/staffwriting/letters.py` holds the salutation,
close and From-line models, the letter signature, the pairing rules, and the
time and date-style checks. The external letter reuses it. New blocks:
`from_line`, `recipient`, `salutation`, `body {numbering: none}`, signature
variant `letter`. `letterhead` gained an optional bold `unit` line. `subject`
now skips cleanly when absent. Existing templates are unaffected (all their
tests pass).

## 4. Implementation decisions (I-L)

| ID | Decision | Why |
|---|---|---|
| I-L1 | `purpose` field (routine, congratulatory, condolence, admonition, reprimand, reply_to_admonition) drives the rules | 2.1.15a and 2.1.17 tie the format to the purpose |
| I-L2 | Errors: salutation/close format mismatch; commas after either; a file reference on congratulatory or condolence letters; a salutation or close on an admonition; annexes; sub-paragraphs or bullets | 2.1.17d(2)–(4), 2.1.16(6), (12), (18) |
| I-L3 | Warnings: close not matching the salutation form (first name → sincerely; rank/title + surname → faithfully); typed salutation on congratulatory or condolence letters; abbreviations in them; subject heading on personal letters; am/pm times; abbreviated days or dates | 2.1.17d(1) (the writer may vary the close); 2.1.17c "usually"; 1.2.8d; 2.1.16(9) "should not"; 2.1.16(15); 1.2.10a–b |
| I-L4 | The close sits one line below the last paragraph; the signature block is six lines below the close (**approved 2026-10-01**) | 1.2.21c ("six lines below the last line of text"); the close is the last line of text. The six lines hold the handwritten signature (Fig 2-7). |
| I-L5 | A handwritten salutation or close leaves one empty line | Fig 2-9 shows blank space where the typed line would be |
| I-L6 | Standing reminder to check the identity device against the signatory | 2.1.16(3) depends on who signs; not machine-checkable |

## 5. Validation record (2026-10-01)

| Fixture | Purpose | Result |
|---|---|---|
| `2g-example.yaml` | Re-key of Annex 2G | 1 p; lint clean |
| `2h-typed-structure.yaml` | Element set and order of Fig 2-8 | Order, no-numbering and signature tests pass |
| `2h-handwritten-congratulatory.yaml` | Fig 2-9: handwritten salutation and close, congratulatory | Empty slots rendered; no file reference |

Differences from Figs 2-7 to 2-9 (`output/comparisons/internal-letter-*`):

| ID | Difference | Disposition |
|---|---|---|
| DL-01 | The figures put the file reference on its own line above the date; ours is on the date line | 2.1.16(6) prose: "on the same line as the date, against the right-hand margin" |
| DL-02 | With the day left blank, the date reads "November 2025" at the margin with no space reserved for the day | 2.1.16(5) says left margin and day handwritten. **APPROVED AS IMPLEMENTED 2026-10-01**: no reserved space. |
| DL-03 | The template shows about four blank lines before the close and one after; ours has one before and six after | 1.2.21c prose (I-L4). A bug that put the six-line gap **before** the close as well (twelve blank lines) was found during the external-letter comparison and fixed; it is covered by `test_close_follows_text_then_six_lines`. |
| DL-04 | Example 2G omits the rank line from the signature block | 2.1.16(17) requires the full rank; the prose governs |
| DL-05 | Badge and logo are labelled placeholders | T-05 (artwork not held) |
| DL-06 | Example 2G italic annotations and the handwritten signature are not reproduced | DFI notes, not content |
