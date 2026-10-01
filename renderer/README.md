# Renderer (reusable document-generation components)

Not implemented yet (Phase 0). The planned modules, data flow and validation are
in [`docs/architecture.md`](../docs/architecture.md) §3–§6. The proposed stack
(Python + python-docx with an OXML helper layer) is pending approval
(register T-01).

Rules:
- Read every formatting value from `standards/spec/dfi-5.1-tokens.yaml`. Do not
  hard-code values in the renderer.
- Emit real Word constructs (styles, numbering definitions, PAGE/NUMPAGES fields,
  sections, footnotes), never visual imitations.
- `assets/` (badges, logos, coat of arms) will hold **official artwork supplied
  by the user only** (register T-05). Do not extract artwork from the DFI PDF.
