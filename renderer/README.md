# Renderer (reusable document-generation components)

Python package `staffwriting`: Python 3.11, python-docx 1.2, pydantic 2, PyYAML.
It generates finished `.docx` documents that conform to DFI 5.1 from structured
YAML content (register T-01, T-02, T-06).

## Setup

```bash
pip install -r renderer/requirements.txt
# Preview and validation tooling (system packages):
apt-get install libreoffice-writer fonts-crosextra-carlito poppler-utils
```

LibreOffice Writer and the Carlito font are needed **only** for PDF previews and
visual checks. Carlito is metric-compatible with Calibri. The deliverable is the
`.docx` opened in Microsoft Word.

## Use

```bash
PYTHONPATH=renderer python3 -m staffwriting render CONTENT.yaml -o output/x.docx [--pdf] [--lint]
PYTHONPATH=renderer python3 -m staffwriting.compare      # DFI vs rendered side-by-side images
cd renderer && python3 -m pytest -q tests                 # schema, render, lint and negative tests
```

The content file's `type:` selects `templates/<type>/` (its `template.yaml`
block sequence and its `schema.py` content model).

## Architecture as built (Phases 1–2)

```
content.yaml ─► templates/<id>/schema.py (pydantic: mandatory elements, counts, warnings)
                       │
templates/<id>/template.yaml (ordered blocks + options)
                       │
standards/spec/dfi-5.1-tokens.yaml ─► tokens.py
                       │
builder.py  Document + styles.py (style sheet) + numbering.py (Word numbering
            definitions) + ooxml.Footnotes (real footnotes) + page.Furniture
            (sections, markings, page numbers, copy number, watermark)
                       │
blocks.py   REGISTRY of reusable blocks: letterhead, originator_descriptor,
            identifier, date_line, addressees, subject, references, body
            (scheme C numbering, paragraph headings, sentence lists, bullets,
            recommendations, tables; or unnumbered letter paragraphs), signature
            (minute/admin/letter variants), telephone, annex_list, enclosure_list,
            flag_list, consulted, distribution, copy_distribution, title_line,
            from_line, recipient, salutation, supporting_documents
                       │
.docx ─► lint.py (page setup, fonts/sizes/colour, settings, markings on every
         header/footer, page-number regime, subject case, numbering geometry,
         OOXML child order; PDF: markings first/last line on every page,
         signature orphan rule)
      ─► preview.py (LibreOffice PDF/PNG) ─► compare.py (DFI side-by-side)
```

| Module | Responsibility |
|---|---|
| `tokens.py` | Loads the shared DFI values (fonts, sizes, spacing, indents, page size). Renderer modules read formatting values from here |
| `builder.py` | Owns the python-docx Document and shared services (styles, numbering, footnotes, furniture) |
| `dates.py` | Date formatting (abbreviated and full; handwritten day) |
| `styles.py` | Word style sheet (Calibri, en-NZ, spacing, heading styles, footnote styles) |
| `numbering.py` | Abstract numbering for scheme C, lists and bullets; per-body restart instances |
| `ooxml.py` | Fields (PAGE, NUMPAGES, nested IF/SECTIONPAGES), footnotes part, settings, watermark, page-number restart |
| `page.py` | Section setup and header/footer composition by marking and page-number regime |
| `blocks.py` | The reusable blocks above |
| `model.py` | Shared content models: markings, dates, paragraphs, recommendations, tables, addressees, signature, annexes, letterhead |
| `tables.py` | DFI tables (1.2.25): 0.5 pt borders, 10/11 pt, repeated header row, centred, optional caption |
| `letters.py` | Shared formal-letter models and rules: salutation, close, From line, letter signature, `LetterBase` |
| `wording.py` | Shared wording warnings (hyperlinks, exclamation marks, em dashes, %, eg/ie/etc) |
| `inline.py` | `**bold**`, `*italic*`, `__underline__`, `^[footnote]` |
| `render.py`, `__main__.py` | Template loading, validation, build, CLI |
| `lint.py`, `preview.py`, `compare.py` | Validation tooling |

Rules:
- Read every formatting value from the tokens.
- Emit real Word constructs (styles, numbering, fields, sections, footnotes).
- `assets/` will hold **official artwork supplied by the user only** (T-05).
  Until then the letterhead block renders a labelled placeholder.
