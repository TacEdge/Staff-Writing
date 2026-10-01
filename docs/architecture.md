# Architecture

Status: **proposal for approval**. The technology choices depend on register
items T-01 to T-06.

## 1. Principles

1. **One authority.** DFI 5.1 (`source/`) is the only source of formatting
   rules. Everything else is derived from it and traceable to it.
2. **Extract once, reference everywhere.** Shared rules live in `standards/` and
   their machine-readable form in `standards/spec/`. Templates hold only what is
   unique to a document type.
3. **Mandatory vs implementation is explicit.** Every encoded value carries a tag
   (M/D/T/I/A-nn) and a citation, so a reviewer can tell DFI requirements from
   our choices.
4. **Real Word documents.** Outputs use Word styles, numbering, fields, sections
   and footnotes, so staff can keep editing them in MS Word.
5. **Fail loudly.** Missing mandatory elements, invalid markings, forbidden
   constructs (for example bullets in a directive) and unresolved ambiguities
   produce errors or warnings, never silent guesses.

## 2. Repository structure

```
Staff-Writing/
├── CLAUDE.md                     Rules for Claude (authority, template workflow)
├── README.md
├── source/                       (1) ORIGINAL AUTHORITATIVE SOURCE: read-only
│   └── dfi-5.1/
│       ├── dfi_5_1.pdf           DFI 5.1 v2.01, byte-identical to the upload
│       ├── SOURCE.md             Provenance, SHA-256, annex → page map
│       └── derived/
│           └── dfi_5_1.layout.txt   Text extract for search (non-authoritative)
├── standards/                    (2) EXTRACTED COMMON STANDARDS
│   ├── README.md                 Index and tag legend
│   ├── 01-principles-and-language.md
│   ├── 02-page-layout.md
│   ├── 03-headings-paragraphs-lists.md
│   ├── 04-correspondence-elements.md
│   ├── 05-supporting-documents.md
│   ├── 06-tables-figures-highlights.md
│   ├── 07-identity-and-markings.md
│   ├── 08-publications.md
│   └── spec/
│       └── dfi-5.1-tokens.yaml   Machine-readable shared values
├── templates/                    (3) INDIVIDUAL DOCUMENT TEMPLATES
│   ├── README.md
│   ├── _SPEC-FORMAT.md           Required layout of every template folder
│   └── <doc-type>/               created in phase 2+, eg minute/, submission/
│       ├── template.yaml         Ordered blocks, variant selections, overrides (cited)
│       ├── schema.py|json        Content schema (mandatory and optional elements)
│       ├── NOTES.md              DFI references, ambiguities, deviations
│       └── blank.yaml            Content that reproduces the DFI blank template
├── renderer/                     (4) REUSABLE GENERATION COMPONENTS
│   └── README.md                 Planned modules (see §4)
├── reference/                    (5) VALIDATION / REFERENCE EXAMPLES
│   ├── README.md
│   ├── dfi-pages/                PNG renders of DFI template and example pages
│   └── fixtures/<doc-type>/      DFI examples re-keyed as content + expected checks
├── output/                       (6) GENERATED OUTPUTS: git-ignored
│   └── README.md
└── docs/
    ├── template-inventory.md
    ├── ambiguities-and-decisions.md
    ├── architecture.md           (this file)
    └── implementation-plan.md
```

## 3. Data flow

```
 content.yaml ──► schema validation ──► template.yaml (ordered blocks)
 (user input)     (per doc type)              │
                                              ▼
 standards/spec/dfi-5.1-tokens.yaml ──► renderer: style sheet + numbering
                                              │     + page furniture
                                              ▼
                                       block builders ──► .docx writer ──► output/
                                                                     │
                                       docx lint + visual diff ◄─────┘
```

- `content.yaml` holds what the author supplies (addressees, subject,
  paragraphs, recommendations, markings, signatory, annexes). It does not hold
  layout.
- `template.yaml` declares the document type's block sequence, which shared
  variants it uses (for example `numbering: correspondence`,
  `signature: minute`, `page_numbering: unclassified_from_page_2`), and any
  cited overrides.
- The renderer turns tokens into Word styles and numbering definitions once, then
  each block builder emits paragraphs, tables, fields and sections.

## 4. Renderer components (planned)

| Module | Responsibility | Key DFI sources |
|---|---|---|
| `tokens` | Load and validate `dfi-5.1-tokens.yaml`; expose typed values; refuse unresolved `A-nn` values unless they have an approved default | standards/spec |
| `styles` | Build the Word style sheet: Normal (Calibri 12), Subject, Main/Group heading, Para levels, Table caption/header/body, Footnote, Marking, Publication H1–H5, Warning/Caution/Note, Hyperlink; en-NZ; hyphenation off | 1.2.16, 1.2.17, 4.4.11 |
| `numbering` | Abstract numbering definitions for schemes C, D, P, intro/end matter, references, annex/enclosure lists, bullets; the "single first-level paragraph unnumbered" logic | 2.1.3(3), 3.2.11(6), 4.4.13–16, 1.2.23 |
| `page` | Sections, margins, header/footer distance, orientation (landscape agenda), first-page-different, DRAFT watermark, draft line spacing | 1.2.16, 1.2.22 |
| `furniture` | Header and footer composition: markings (mirror order), page number formats (n, Page n of N, A-1, A-1-1, Roman, part-n, EM-n), copy number, publication running headers | 1.2.16(5)–(9), 1.2.18, 4.4.7–4.4.8 |
| `blocks` | Reusable blocks: originator descriptor, identifier, date line + file reference, addressees, subject, references, paragraphs, recommendations, signature-block variants, list blocks (annexes, enclosures, flags, distribution, copy distribution, consulted, ministerial referral), badge/address letterhead | standards/04, 05, 07 |
| `supporting` | Annex, appendix and enclosure sections: identifying block, own subject heading, page numbering restart, (cont.) | 1.2.24, 4.4.7a(6) |
| `tables` | DFI table style (0.5 pt borders, 10/11 pt, repeat header, "(cont.)" captions), boxed forms (cover sheets, QA forms, agenda) | 1.2.25 |
| `footnotes` | Real Word footnotes (10 pt, consecutive) | 1.2.19b |
| `inline` | Inline mark-up: bold, italic, underline, footnote refs, non-breaking spaces before units, en dashes in ranges, macron safety | 1.2.7, 1.2.13 |
| `writer` | Assemble the document, set core properties, write the .docx; optional PDF preview via LibreOffice | T-07 |
| `lint` | Post-render checks (§6) | – |

## 5. Template definition (sketch)

```yaml
# templates/minute/template.yaml  (illustrative only, not yet implemented)
id: minute
dfi: { section: "2.1.10-2.1.11", template: "2D", example: "2C" }
page: { margins: standard, orientation: portrait }
numbering: correspondence
page_numbering: unclassified_from_page_2      # 1.2.16(6), 2.1.11(18)
identity: none                                 # 2.1.11(1)
date: { style: abbreviated, indent_cm: 1.0, handwritten_day: true }  # A-01/02/06
blocks:
  - markings
  - originator_descriptor        # required
  - identifier: { pattern: "{appointment} MINUTE {nn}/{yyyy}", optional_parts: [appointment, number] }
  - date_line: { file_reference: right }
  - addressees: { action: required, through: optional, info_max: 6, distribution_over: 6 }
  - subject                      # required
  - references: { optional: true }
  - body                         # purpose recommended; main/group headings
  - recommendations: { optional: true }
  - signature: minute
  - telephone: { optional: true }
  - annex_list
  - enclosure_list
  - distribution
  - copy_distribution
```

## 6. Validation (definition of done for any template)

1. **Input schema:** mandatory elements present; enumerations (markings,
   importance, urgency); counts (information addressees ≤ 6, a single addressee
   for submissions, one page for briefing notes and cover sheets as a
   post-render check); date formats.
2. **Docx structural lint:**
   - every run is Calibri and black (except hyperlink, warning, caution, note);
     sizes match tokens;
   - margins and header/footer distances; A4; correct orientation;
   - markings present on **every** page header and footer, in the right order;
   - page-number fields per regime; first-page suppression where required;
   - numbering definitions match the scheme; no bullets in letters or
     directives; no paragraph numbers in external letters;
   - no hyperlinks in minutes or letters;
   - signature block preceded by at least two lines of text on the same page
     (checked on PDF render);
   - annexes, appendices and enclosures in one file; annex marking ≤ parent
     marking;
   - language en-NZ; auto-hyphenation off.
3. **Visual regression:** render DFI example fixtures → PDF → PNG and compare
   side by side with `reference/dfi-pages/`. Differences are listed in the
   template's `NOTES.md` and accepted by a human.
4. **Wording warnings (T-10):** exclamation marks, full stops in abbreviations,
   "%", numerals below 10, US spelling (-ize, color, program), "shall"/"will" in
   orders, missing first-use expansion of abbreviations, em dashes in
   correspondence.

## 7. Non-goals for now

- Rewriting or summarising content on the author's behalf.
- Email, Cabinet papers, OPORDs, FRAGOs, business cases, academic papers (not
  DFI templates; see the inventory §3).
- Applying PDF security, digital signatures, DDMS filing.
