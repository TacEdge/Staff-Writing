# Architecture

Status: **as built, Phases 1–3** (decisions T-01, T-02, T-06 approved; BR-01 identity artwork). The
module-level detail lives in `renderer/README.md`; this document keeps the
structure, data flow and validation contract.

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
│       └── (blank.yaml)          Blank-template content: deferred (T-06)
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

## 4. Renderer components (as built)

See the module table in `renderer/README.md`. In summary: `tokens`, `styles`,
`numbering`, `page` (sections and header/footer furniture), `ooxml` (fields,
footnotes, settings, watermark), `blocks` (reusable blocks), `tables`,
`letters` (shared letter rules), `orders` (shared rules for orders, directions
and instructions), `artwork` (identity artwork derived from the controlled VIS
source), `model` (shared content models), `inline`, `wording`, `dates`,
`builder`, `render` (template loading and CLI), and the validation tools
`lint`, `preview`, `compare` and `baseline`.

## 5. Template definition

Each template folder holds `template.yaml` (an ordered block list with
options), `schema.py` (a pydantic `Content` model, which may provide
`compose_body()` and `warnings()`) and `NOTES.md`. See `templates/minute/` for
a worked example and `templates/_SPEC-FORMAT.md` for the required keys.

The renderer acts on `page`, `date`, `blocks` and `lint`. The `numbering`,
`page_numbering` and `identity` keys are **declarative**. They record the shared
variant the template uses, for review and traceability. The behaviour itself
comes from the blocks and options listed, and the page-number regime follows
from the markings.

## 6. Validation (definition of done for any template)

1. **Input schema:** mandatory elements present; enumerations (markings,
   importance, urgency); counts (information addressees ≤ 6, a single addressee
   for submissions, one page for briefing notes and cover sheets as a
   post-render check); date formats.
Items marked (planned) are not yet implemented in `lint.py` or the schemas.

2. **Docx structural lint:**
   - every run is Calibri and black (except hyperlink, warning, caution, note);
     sizes match tokens;
   - margins and header/footer distances; A4; correct orientation;
   - markings present on **every** page header and footer, in the right order;
   - page-number fields per regime; first-page suppression where required;
   - paragraph numbering geometry matches the template's declared scheme
     (C, or D for orders, directions and instructions); no bullets in scheme
     D documents; bullets and paragraph numbers in letters are prevented by
     the letter schema;
   - directive page-number regime: page 1 numbered when the main document has
     two or more pages (conditional field; Word check V-05);
   - no hyperlinks in minutes or letters;
   - signature block preceded by at least two lines of text on the same page
     (checked on PDF render);
   - annexes, appendices and enclosures in one file (schema warning);
     annex marking ≤ parent marking (planned: annexes inherit the parent's
     markings today);
   - OOXML child order of paragraph and section properties;
   - language en-NZ; auto-hyphenation off.
3. **Output regression:** `staffwriting.baseline` snapshots every fixture
   (canonical XML of each part, media checksums). A change to shared code is
   checked against the last accepted snapshot. A controlled baseline update
   proves its only change (see `docs/baselines/`).
4. **Visual regression:** render DFI example fixtures → PDF → PNG and compare
   side by side with `reference/dfi-pages/`. Differences are listed in the
   template's `NOTES.md` and accepted by a human.
5. **Wording warnings (T-10):** implemented: exclamation marks, full stops in
   eg/ie/etc, "%", hyperlinks, em dashes in correspondence; in letters,
   abbreviated days and dates, 12- or 24-hour clock, and unexplained
   abbreviations (external letters); in orders, directions and instructions,
   abbreviated day names (except 1.2.10d), colon list lead-ins, missing
   mandatory language in tasks, and annexes or enclosures not introduced in
   the text (em dashes are not reported there). Planned: numerals below 10,
   US spelling.

## 7. Non-goals for now

- Rewriting or summarising content on the author's behalf.
- Email, Cabinet papers, OPORDs, FRAGOs, business cases, academic papers (not
  DFI templates; see the inventory §3).
- Applying PDF security, digital signatures, DDMS filing.
