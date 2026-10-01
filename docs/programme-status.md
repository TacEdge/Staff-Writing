# Programme status (2026-10-01, after the Phase 3 review)

## 1. Implemented DFI document types (9 of 28 buildable products)

| # | Document type | DFI | Status |
|---|---|---|---|
| 1 | Minute | 2.1.10–2.1.11; 2C/2D | Accepted |
| 2 | Submission | 2.1.12; 2E/2F | Accepted |
| 4 | Dot-point brief | 2.2.6–2.2.8; 2O | Accepted |
| 5 | Visit report / PAR | 2.2.9–2.2.11; 2P/2Q | Accepted |
| 6 | Internal formal letter | 2.1.13–2.1.17; 2G/2H | Accepted (OP-01 gap) |
| 7 | External letter | 2.1.13–2.1.18; 2I/2J | Accepted (OP-01 gap) |
| 8 | Administrative Instruction | 3.2.21–3.2.22; 3F | Provisionally accepted |
| 9 | CDF Directive, plus commander and senior-executive variants | 3.2.8–3.2.14; 3D | Provisionally accepted (V-05) |
| 24 | CDF Operational Directive | 3.2.16–3.2.18; 3E | Provisionally accepted (V-05) |

Also implemented:
- **Annex and appendix pages (item 3):** a shared capability used by every type.
- **The Annex 1A generic layout (item 30):** validated.
- **Email (item 31):** not a .docx product.

Coverage:
- **By count:** 9 of the 28 buildable products (32 per cent).
- **By staff-writing family:** all correspondence and letters, both general
  reports, and all directives are covered.

## 2. Document types still to build (19)

| Family | Items | DFI examples available | Main new capability |
|---|---|---|---|
| **Meetings** | 20 Meeting agenda (landscape), 21 Minutes of a meeting | 2R, 2T | Landscape, table-based layouts |
| **Delegations** | 18 temporary, 19 permanent | 2K, 2M | Verbatim delegation wording; A-05 and A-07 already decided |
| **Ministerial** | 10 Note to the Minister, 11 cover sheet, 12 QA Form, 13 Briefing Note, 14 Veterans, 15–17 Joint Note, cover sheet and QA Form | 2Y, 2AE | Boxed forms; one-page checks; identity assets not held (A-18) |
| **DFO(T)** | 22 conditions of service, 23 officers' postings | 3A, 3B | Scheme D (exists); DFO conventions |
| **Publications** | 25 DFI/DM, 26 DFO, 27 Publications QA Form | 4A–4G | Scheme P, TOC field, part and chapter numbering, revision bars |
| **Other** | 28 MOU, 29 professional literature preliminary page | 2W | Long drawn template (MOU) |

## 3. Accepted shared capabilities

**Document engine**
- Tokens as the single source of formatting values.
- Real Word construction: styles, numbering definitions, fields, sections,
  footnotes and the draft watermark.

**Numbering**
- Schemes C (correspondence) and D (directives, hanging), plus lettered and
  numbered lists, bullets and sentence-list punctuation.

**Page furniture**
- Markings: header and footer mirroring.
- Page-number regimes:
  - unclassified (no number on page 1);
  - above Restricted ("Page n of N");
  - annex numbering "A-1";
  - directive page 1 when there are two or more pages (V-05).
- Copy number.

**Blocks**
- Header and identity: letterhead with official artwork, descriptor or HQ line,
  identifiers (including directive identifiers), date and file reference.
- Addressees and subject: addressee and distribution modes, subject,
  references.
- Body: group, main and paragraph headings, and tables.
- Signature variants: minute, admin and letter.
- Lists and closing elements: annex, enclosure and flag lists; consulted;
  copy distribution.
- Letter elements: From line, recipient, salutation and close.

**Supporting documents**
- Annexes and appendices in the same file, following the parent's scheme.

**Shared rule modules**
- `letters.py`: formal letters.
- `orders.py`: orders, directions and instructions.
- `wording.py`: T-10 warnings (reported, never rewritten).

**Identity artwork**
- Derived at render time from the controlled VIS source, with its checksum
  verified first. Badge and logo sizes follow BR-05.

**Validation**
- Schema validation per type.
- The `.docx` checker (`lint`), aware of each template's scheme and page-number
  regime.
- PDF checks.
- Visual comparison with the DFI pages.
- `baseline` snapshot, diff and proof for controlled updates.

## 4. Unresolved source dependencies and ambiguities

| ID | Item | Needed from |
|---|---|---|
| **OP-01** | Force for New Zealand logotype on letters: **known compliance gap** | Authoritative NZDF Word letter template or approved example |
| T-03 | Official NZDF_DSWT Word templates. Would also settle A-22 sizes, D-06 shading and OP-01. | NZDF Publications Centre / DSWT |
| A-10 | Authoritative rank and appointment abbreviation list (addressees are not checked) | NZDF |
| A-13, A-31 | PSR/DFO 51 marking vocabulary; classified pagination rules | PSR, DFO 51 Vol 1 Ch 7 |
| A-18 and others | Veterans' Affairs logo, MoD Chief Executive coat of arms, Office of the Chief Executives crest (ministerial family) | Authoritative artwork |
| I-C2 | Command and unit badges: accepted limitation | Authoritative artwork, if ever wanted |
| D-06 | Signature-area shading: unresolved | DSWT or digital-signature evidence |
| D-09, D-10 | Paragraph grading indicators; single-approval statement: deferred | Your decision when needed |
| E-13 | Fixed "DFO 14" in the CDF Directive cancellation wording | Authoritative resolution |
| E-01 to E-12 | Apparent DFI errors in templates not yet built | Decide per template under the section E policy |
| DR-12 | Op Directive format variation (3.2.16c): not implemented | Your decision if needed |

## 5. Microsoft Word checks still outstanding

| ID | Check | Status |
|---|---|---|
| V-01 to V-04 | Annex numbering, watermark, footnotes, clean open | **PASSED** 2026-10-01. Word version, OS and V-01 to V-03 observations not supplied. |
| **V-05** | Directive page 1: "1" when two or more pages; no number on one page | **NOT TESTED.** Use `cdf-directive/3d-structure` and `variant-single-page`. |
| (future) | Every new conditional field or construct LibreOffice cannot evaluate | Added per family |

## 6. Automated tests

**238** tests pass: `cd renderer && python3 -m pytest -q tests`.

There are 32 fixtures:
- 21 from Phases 1–2;
- 11 from Phase 3.

All fixtures render and lint clean. The accepted Phase 1–2 outputs differ from
their accepted baseline only by the identity artwork
(`docs/baselines/2026-10-01-identity-artwork.md`).

## 7. Recommended next family: Meetings (agenda and minutes of a meeting)

1. **Frequent use.** Unit-level staff work, including at a training
   establishment, produces agendas and meeting minutes routinely. Most
   remaining families (ministerial, DFO(T), publications) are produced
   centrally or rarely.
2. **Real validation.** Both items have DFI worked examples (2R, 2T). The
   directive family could only be compared with templates.
3. **Bounded new surface.** Landscape sections and table-based layouts reuse the
   existing `tables` module. No identity artwork is needed: DFI says badges are
   not applied to agendas or minutes. No open source dependency blocks it.

After that: **Delegations** (verbatim wording, A-05 and A-07 already decided).
Then decide whether the ministerial family is needed, because it is
form-heavy and blocked in part by missing identity assets.
