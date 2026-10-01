# Staff Writing

A reusable NZDF staff-writing and document-generation system. It is built to
produce documents that conform to **DFI 5.1 Defence Force Writing**
(v2.01, 03 Oct 2025), the authoritative source for all NZDF writing, formatting,
structure and layout.

**Status: Phases 1–2 accepted (2026-10-01); Word checks V-01 to V-04 passed.
Phase 3 (Administrative Instruction, CDF Directive with variants, CDF
Operational Directive) provisionally accepted 2026-10-01; Word check V-05 not
tested. Known compliance gap OP-01 (Force for New Zealand logotype on letters).** Identity artwork comes from the NZDF Visual Identity
Standards (`source/nzdf-visual-identity/`). Implemented: Minute, Submission, Dot-point brief, Visit
report/PAR, internal formal letter, external letter, Administrative
Instruction, CDF Directive, CDF Operational Directive. See
[docs/template-inventory.md](docs/template-inventory.md) and
[renderer/README.md](renderer/README.md).

| Start here | |
|---|---|
| [CLAUDE.md](CLAUDE.md) | Authority rules and the workflow for creating or modifying templates |
| [docs/template-inventory.md](docs/template-inventory.md) | Every DFI document type: section, template and example annexes, structure, unique formatting, priority |
| [standards/](standards/README.md) | Common standards extracted from DFI 5.1 (with citations), plus machine-readable tokens |
| [docs/ambiguities-and-decisions.md](docs/ambiguities-and-decisions.md) | DFI ambiguities, apparent DFI errors, and technical decisions, with their status |
| [docs/architecture.md](docs/architecture.md) | Repository structure, data flow, renderer components, validation |
| [docs/implementation-plan.md](docs/implementation-plan.md) | Recommended build sequence |
| [docs/programme-status.md](docs/programme-status.md) | Programme-level status: coverage, open dependencies, Word checks, next family |
| [source/dfi-5.1/SOURCE.md](source/dfi-5.1/SOURCE.md) | Provenance and checksum of the DFI, and the annex → PDF page map |

Repository areas: `source/` (original DFI, read-only) · `standards/` (shared
rules) · `templates/` (per-document-type specs) · `renderer/` (generation
components) · `reference/` (validation examples) · `output/` (generated,
git-ignored).
