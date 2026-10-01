# CLAUDE.md — Staff Writing repository

This repository is a reusable NZDF staff-writing and document-generation system.
Its job is to produce documents that conform exactly to **DFI 5.1 Defence Force
Writing** (Version 2.01, 03 October 2025).

## 1. The source of truth

- `source/dfi-5.1/dfi_5_1.pdf` is the **only** authority for NZDF writing,
  formatting, structure and layout in this repository.
- Do **not** substitute generic military-writing conventions, other nations'
  service-writing standards, US/UK staff formats, house styles or your own
  preferences where DFI 5.1 gives direction.
- Where DFI 5.1 says it is silent and refers elsewhere (for example DFO 51 for
  classified page numbering, the Cabinet Manual for Cabinet papers, The Chicago
  Manual of Style for professional literature, COMJFNZ standards for OPORDs),
  do not invent the missing rule. Record it as out of scope or as an open item in
  `docs/ambiguities-and-decisions.md`.
- The PDF is read-only. Never edit, re-save, optimise, rename or replace it. Its
  SHA-256 is recorded in `source/dfi-5.1/SOURCE.md`; if the checksum changes,
  stop and tell the user.
- `source/dfi-5.1/derived/dfi_5_1.layout.txt` is a machine text extraction that
  makes the PDF searchable. It is **not** authoritative. It loses bold, colour,
  italics, alignment and exact indentation. Before you rely on a visual detail,
  check the PDF page itself (render it with
  `pdftoppm -f N -l N -r 100 -png source/dfi-5.1/dfi_5_1.pdf /tmp/page`).
  `SOURCE.md` maps every annex to its PDF page.
- DFI 5.1 para 16 says that only the online copy in the NZDF Publications Centre
  is authoritative; all other copies are uncontrolled. If the user supplies a
  newer version, treat it as a controlled change (see §7).

## 2. Repository layout (what goes where)

| Path | Purpose | Rules |
|---|---|---|
| `source/` | Original authoritative DFI and derived extracts | Never modify the original. Derived files must say they are derived. |
| `standards/` | Common standards extracted **once** from DFI 5.1 | Every rule cites its DFI paragraph or annex. Templates reference these rules and do not restate them. |
| `standards/spec/` | Machine-readable version of the shared standards (tokens) | This is the single source the renderer uses for fonts, sizes, spacing, indents and so on. |
| `templates/` | One folder per document type: template spec, content schema, notes | Holds only what is unique to that document type. Shared rules are referenced, not copied. |
| `renderer/` | Reusable generation components (styles, numbering, page furniture, blocks, writer) | Must not hard-code values that already exist in `standards/spec/`. |
| `reference/` | Validation material: DFI page images, re-keyed DFI examples, expected-output fixtures | Fictional or DFI-supplied content only. |
| `output/` | Generated documents | Git-ignored. Never commit generated documents. |
| `docs/` | Inventory, architecture, decisions/ambiguity register, implementation plan | Keep up to date when anything changes. |

## 3. Rules for creating or modifying a staff-writing template

Follow these steps every time you create or modify a template.

1. **Read the DFI first.** Read the DFI section for the document type (prose),
   its template annex and its example annex (if one exists). Render the annex
   pages and look at them. The inventory in `docs/template-inventory.md` lists
   them.
2. **Prose outranks figures.** Where the DFI prose (an "is to", "must" or
   "are to" statement) conflicts with a template or example figure, the prose
   governs. Where the prose is silent, the template figure governs. Where the
   template is silent, the example figure governs. Every conflict must be logged
   in the register, even when the hierarchy resolves it.
3. **Classify every rule you encode** with one of these tags, and cite the source:
   - `[M]` Mandatory: DFI imperative ("is to", "are to", "must", "must not").
   - `[D]` DFI default or guidance: "should", "may", "generally", "usually".
   - `[T]` Template-derived: shown in a DFI template or example figure but not
     stated in prose.
   - `[I]` Implementation decision: not in DFI. It needs an entry in
     `docs/ambiguities-and-decisions.md`, and user approval when it affects
     appearance or content.
   - `[A-nn]` Ambiguous: points to the register entry. Do not resolve an
     ambiguity silently.
4. **Reuse, don't duplicate.** Page setup, fonts, spacing, markings, page
   numbering, paragraph numbering schemes, signature blocks, annex/appendix/
   enclosure handling, tables and lists belong in `standards/` and
   `standards/spec/`. A template may only **select** a shared variant (for
   example `paragraph_scheme: correspondence`) or **override** one with a cited
   DFI reason.
5. **Preserve the official format.** Do not modernise, redesign, re-order,
   rename or "improve" official formats, headings, boilerplate wording or
   element order unless the user explicitly tells you to. That includes
   pleasing-looking changes such as different fonts, colours, extra headings or
   a cover page.
6. **Boilerplate wording** in DFI templates (for example the Applicability
   paragraphs of a CDF Directive, or delegation wording) must be reproduced
   verbatim. If the DFI text contains an obvious error, do not silently correct
   it. Log it, propose the correction and wait for approval
   (see register section E).
7. **Placeholders.** Use the DFI placeholder names (for example
   `[Appointment] MINUTE [nn/yyyy]`) to name content fields, so a reviewer can
   trace each field back to the DFI template.
8. **Optional elements** (for example "For information", "Reference", "Annex(es)",
   "Summary", "Timing") must be omitted cleanly when unused. Never output an
   empty heading or the DFI instruction text "(remove if not required)".
9. **Validation is part of done.** A template is not complete until:
   - its content schema rejects missing mandatory elements;
   - it renders a `.docx` without errors;
   - the DFI example annex (where one exists) is re-keyed into
     `reference/` and the rendered output has been compared visually with the DFI
     page image, with the differences listed; and
   - the document-level checks in `docs/architecture.md` §6 pass.
10. **Update the records.** Every template change updates the inventory status,
    any affected register entries and the template's own `NOTES.md`.

## 4. Writing rules Claude must apply to generated *content*

When you draft text as well as layout, apply DFI 5.1 Part 1 Chapter 2
(see `standards/02-language-and-style.md`). The key rules are:

- New Zealand English (New Zealand Oxford Dictionary): -ise, colour, programme.
- No exclamation marks. No full stops in initials, honorifics or abbreviations
  (eg, ie, etc).
- Directive language carries meaning (1.2.6). "Is to", "are to" and "must" are
  orders; "should" leaves discretion; "may" is permissive. Do not soften or
  harden the language the user supplies.
- Numbers: spell out one to nine; use numerals for 10 and above; write "per cent",
  not "%".
- Dates: dd Mmm yy in correspondence and administrative documentation; full
  date in formal letters and publications; 24-hour clock internally.
- Gender-neutral language (1.1.7).
- Use correct te reo Māori macrons.
- Em dashes only in DFOs, DFIs and orders/directions/instructions. Do not use
  them in correspondence or administrative documentation (1.2.7(10)), subject to
  register item A-07.

## 5. Security and content handling

- This repository holds **unclassified** material only. Never commit real
  correspondence, personal information, or protectively marked content. Examples
  and fixtures must be fictional or taken from DFI 5.1 (which is releasable to
  the public).
- The renderer applies protective markings as **user-supplied, validated input**.
  Never infer a classification or endorsement marking from the content.
- The full vocabulary of markings comes from the PSR and DFO 51, which are not in
  this repository (register item A-13). Until the user supplies that list, accept
  only markings that appear in DFI 5.1 and flag anything else.

## 6. Technical conventions

- Target output is `.docx` that opens cleanly in Microsoft Word and uses real
  Word styles, numbering definitions, fields (PAGE, NUMPAGES), sections and
  footnotes. Do not fake these with manual spacing, typed numbers or text boxes,
  so that a staff officer can keep editing the file normally.
- Font: Calibri, black, set explicitly. If verification rendering uses
  LibreOffice, Carlito (metric-compatible) is an acceptable stand-in for
  checking. Say so in any visual-comparison note.
- Language en-NZ. Automatic hyphenation off (1.2.7(11)(b)). Spacing between
  paragraphs of the same style must not be suppressed (4.4.16a).
- The technology stack and input format are set out in `docs/architecture.md`.
  They remain proposals until register section T is approved.

## 7. Change control

- **DFI update:** If a new DFI 5.1 version arrives, add it as a new folder
  (`source/dfi-5.1-vX.YY/`) and keep the old one. Diff the content, list the
  affected standards and templates, and get approval before migrating.
- **Ambiguity resolved by the user:** Record the decision, date and wording in
  the register, then update the affected standards and tokens. Templates follow
  automatically through the shared rules.
- Do not begin implementing templates that the user has not approved
  (see `docs/implementation-plan.md`).
