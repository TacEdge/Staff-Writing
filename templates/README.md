# Templates

One folder per DFI 5.1 document type. Implemented: `minute`, `submission`,
`dpb`, `visit-report`, `internal-letter`, `external-letter`, plus the
validation-only `_validation-annex-1a`. The full list of document types, their DFI sources and their
priorities is in [`docs/template-inventory.md`](../docs/template-inventory.md).

Every template folder must follow [`_SPEC-FORMAT.md`](_SPEC-FORMAT.md), and the
template workflow in [`CLAUDE.md`](../CLAUDE.md) §3.

A template holds only what is **unique** to its document type: the order of its
blocks, its choice of shared variants (numbering scheme, signature block, page
numbering regime, identity device) and any cited overrides. Everything else
comes from `standards/` and `standards/spec/`.
