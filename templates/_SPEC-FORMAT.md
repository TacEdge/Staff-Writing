# Template folder specification

```
templates/<doc-type>/
├── template.yaml   Block sequence, shared-variant selections, cited overrides
├── schema.*        Content schema: mandatory and optional elements, enumerations, counts
├── blank.yaml      Content that reproduces the DFI *template* annex (placeholders)
├── NOTES.md        Traceability record (below)
└── (no shared rules may be copied here)
```

## NOTES.md: required sections

1. **DFI sources.** Section paragraphs, template annex and figure, example annex
   and figure, PDF pages.
2. **Structure.** Ordered list of elements, each with a tag and citation:
   `[M]` mandatory, `[D]` default, `[T]` template-derived, `[I]` implementation,
   `[A-nn]` ambiguity.
3. **Shared rules used.** Links to `standards/` sections and token keys.
4. **Overrides.** Each departure from the shared rules, with its DFI reason.
5. **Verbatim text.** Fixed wording reproduced from the DFI, and any section E
   corrections applied (with the approval reference).
6. **Ambiguities.** Register IDs that affect this template, and the decision
   applied.
7. **Validation record.** Fixture used, render date, visual-comparison
   differences and whether each is accepted.

## template.yaml: required keys

| Key | Meaning |
|---|---|
| `id` | Folder name |
| `dfi` | `{ section, template, example }` |
| `page` | Margins variant, orientation |
| `numbering` | `correspondence` \| `directive` \| `publication` \| `none` |
| `page_numbering` | Regime key from the tokens |
| `identity` | Identity device rule (see `standards/07`) |
| `markings` | Minimum or required markings (eg `minimum: IN-CONFIDENCE`) |
| `date` | Style, alignment, indent, handwritten day |
| `blocks` | Ordered block list with per-block options |
| `overrides` | List of `{ key, value, src, reason }` (must cite DFI) |
