# External letter: traceability notes

Status: **implemented (Phase 2); provisionally accepted 2026-10-01.** Word checks
V-01 to V-04: PASSED in Microsoft Word 2026-10-01 (record in
`templates/minute/NOTES.md` §7).

## 1. DFI sources

| Source | Reference | PDF pages |
|---|---|---|
| Prose | 2.1.13 (use), 2.1.14 (writing), 2.1.16 (layout), 2.1.18 (salutation and close: external); 2.1.3(4) (no paragraph numbers externally) | 78–82, 57–58 |
| Template | Annex 2J: Fig 2-11 (typewritten), Fig 2-12 (handwritten) | 87–88 |
| Example | Annex 2I, Fig 2-10 | 86 |

## 2. Structure (as implemented, in order)

As for the internal letter (`templates/internal-letter/NOTES.md` §2), except:

| Element | External rule | Source |
|---|---|---|
| Letterhead | Device top left; sender address top right (no bold unit line in Fig 2-11) | 2.1.16(3)–(4); Fig 2-11 |
| File reference | **Not used** (schema error) | 2.1.16(6) |
| References | **No references block**: identify the reference in the opening paragraph ("Thank you for your letter of …") (schema error) | 2.1.16(10) |
| Subject heading | Discretionary | 1.2.17(1) |
| Salutation and close | 2.1.18 rules: first name → sincerely; Mr/Mrs/Ms/Miss + surname, or first name + surname → faithfully; Sir/Madam → faithfully; unnamed recipient → no greeting and no close | 2.1.18(2)–(11) |
| Times | 12-hour clock with am/pm (warning on 24-hour times) | 2.1.16(15), 1.2.10c |
| Abbreviations | Warning on unexplained abbreviations (initials and terms introduced in brackets are excluded) | 2.1.16(14) |
| Signatory | Standing reminder: CDF, a COS, or a delegated senior commander or executive | 2.1.16(16) |

## 3. Shared rules used

`staffwriting.letters.LetterBase` (shared with the internal letter): salutation,
close and From line, letter signature, pairing rules, date-style and time
warnings, no annexes, no sub-paragraphs or bullets. No new engine blocks.

## 4. Implementation decisions (I-E)

| ID | Decision | Why |
|---|---|---|
| I-E1 | A file reference or references block on an external letter is a schema error | 2.1.16(6), (10) |
| I-E2 | The abbreviation warning ignores personal initials and terms already introduced in brackets | Avoids false positives on "Captain CD Example" and "Leadership Centre (NZALC)" |
| I-E3 | The pairing rules for unnamed recipients (no greeting, no close) are enforced through the shared pairing rule | 2.1.18(7), (9) |

## 5. Validation record (2026-10-01)

| Fixture | Purpose | Result |
|---|---|---|
| `2i-example.yaml` | Re-key of Annex 2I (date added per A-30) | 1 p; lint clean |
| `2j-typed-structure.yaml` | Element set and order of Fig 2-11 | lint clean |
| `2j-handwritten.yaml` | Fig 2-12, handwritten salutation and close | Abbreviation warning for unexplained NZALC (as intended) |
| `variant-unnamed-recipient.yaml` | Job-title recipient: no greeting or close; no subject | No "Dear" or "Yours" rendered |

Differences from Figs 2-10 to 2-12 (`output/comparisons/external-letter-*`):

| ID | Difference | Disposition |
|---|---|---|
| DE-01 | Fig 2-10 has no date | A-30 decided: date required (2.1.16(5)) |
| DE-02 | Fig 2-10 shows the NZ Army logo | **Resolved 2026-10-01** (BR-06): official artwork, army_logo, 1.25 cm high (BR-05). The fixture label was corrected from "NZ Army badge". No Force for New Zealand wording mark is added (BR-02: Figs 2-10 to 2-12 do not show one). **Known compliance gap OP-01:** 2.1.16(3)(c) requires it; placement awaits an authoritative source. |
| DE-03 | About two lines between the last paragraph and the close in Fig 2-10; ours one | I-L4 (close one line below; six lines below the close for the signature, 1.2.21c) |
| DE-04 | Fig 2-10 italic annotations not reproduced | DFI notes, not content |
