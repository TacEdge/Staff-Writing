# Extracted common standards (DFI 5.1 v2.01)

These files hold the rules that apply across many document types. They are
extracted **once** from DFI 5.1 so that individual templates never restate them.
Templates in `templates/` select from or override these rules. Overrides must
cite a DFI reason.

| File | Covers |
|---|---|
| [01-principles-and-language.md](01-principles-and-language.md) | Writing principles, directive language, spelling, punctuation, abbreviations, capitalisation, days/dates/times, numbers, emphasis, quotations, references, terminology, te reo Māori, inclusive language |
| [02-page-layout.md](02-page-layout.md) | Paper, margins, tabs, font and sizes, justification, line spacing, headers/footers, protective markings, page numbering, copy numbers, drafts, hyperlinks |
| [03-headings-paragraphs-lists.md](03-headings-paragraphs-lists.md) | Heading types, the three paragraph-numbering schemes, vertical lists, bullets |
| [04-correspondence-elements.md](04-correspondence-elements.md) | Originator descriptor, identifier, date line, file reference, addressees, references, footnotes, signature blocks, distribution |
| [05-supporting-documents.md](05-supporting-documents.md) | Annexes, appendices, enclosures, flags, and how they are listed and paginated |
| [06-tables-figures-highlights.md](06-tables-figures-highlights.md) | Tables, figures, captions, warnings, cautions, notes |
| [07-identity-and-markings.md](07-identity-and-markings.md) | Badge/logo usage matrix, letterhead, protective-marking placement |
| [08-publications.md](08-publications.md) | DFO/DFI/DM structure, publication headers, page numbering, heading styles, amendments |
| [spec/dfi-5.1-tokens.yaml](spec/dfi-5.1-tokens.yaml) | Machine-readable values used by the renderer |

## Tags

Every rule carries one of these tags and a DFI citation (paragraph number,
annex, or figure):

| Tag | Meaning |
|---|---|
| `[M]` | **Mandatory.** DFI uses an imperative: "is to", "are to", "must", "must not", or states the rule as fact without discretion. |
| `[D]` | **DFI default or guidance.** "should", "may", "generally", "usually"; discretion allowed. |
| `[T]` | **Template-derived.** Visible in a DFI template or example figure but not stated in prose. |
| `[I]` | **Implementation decision.** Not in DFI. Needs a register entry. |
| `[A-nn]` | **Ambiguous or conflicting** in DFI. See `docs/ambiguities-and-decisions.md` entry A-nn. |

Precedence when DFI sources conflict: prose rule > template figure > example
figure. Every conflict is still logged.

## Scope notes

- DFI 5.1 applies to the document types listed in para 1.1.3. Service-specific
  styles for SOs, ROs and internal circulars are permitted (1.1.3e). Informal
  public-facing material falls under the NZDF identity standards instead
  (1.1.3f).
- These standards cover what DFI 5.1 itself prescribes. Where DFI defers to
  another source (DFO 51, PSR, Cabinet Manual, Chicago Manual, DFO 108, COMJFNZ
  standards, Treasury Better Business Cases, NZDC guides), the standards say so
  and do not fill the gap.
