# Staff Writing

A reusable NZDF staff-writing and document-generation system. It is built to
produce documents that conform to **DFI 5.1 Defence Force Writing**
(v2.01, 03 Oct 2025), the authoritative source for all NZDF writing, formatting,
structure and layout.

**Status: Phase 0 (foundation), awaiting approval.** No templates are
implemented yet.

| Start here | |
|---|---|
| [CLAUDE.md](CLAUDE.md) | Authority rules and the workflow for creating or modifying templates |
| [docs/template-inventory.md](docs/template-inventory.md) | Every DFI document type: section, template and example annexes, structure, unique formatting, priority |
| [standards/](standards/README.md) | Common standards extracted from DFI 5.1 (with citations), plus machine-readable tokens |
| [docs/ambiguities-and-decisions.md](docs/ambiguities-and-decisions.md) | DFI ambiguities, apparent DFI errors, and technical decisions awaiting approval |
| [docs/architecture.md](docs/architecture.md) | Repository structure, data flow, renderer components, validation |
| [docs/implementation-plan.md](docs/implementation-plan.md) | Recommended build sequence |
| [source/dfi-5.1/SOURCE.md](source/dfi-5.1/SOURCE.md) | Provenance and checksum of the DFI, and the annex → PDF page map |

Repository areas: `source/` (original DFI, read-only) · `standards/` (shared
rules) · `templates/` (per-document-type specs) · `renderer/` (generation
components) · `reference/` (validation examples) · `output/` (generated,
git-ignored).
