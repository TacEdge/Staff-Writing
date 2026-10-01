# CDF Operational Directive: traceability notes

Status: **implemented (Phase 3, directive family); awaiting the family review
gate.** Word check **V-05** (page-1 conditional number): **NOT TESTED**.

## 1. DFI sources

| Source | Reference | PDF pages |
|---|---|---|
| Prose | 3.2.15 (warning orders, context), 3.2.16 (Operational Directives), 3.2.17 (content), 3.2.18 (layout), 3.2.19; fn 23; 1.2.10, 1.2.17, 1.2.23 | 170–172 |
| Template | Annex 3E, Fig 3-6 | 173–174 |
| Example | none | – |

## 2. Structure (as implemented, in order)

| # | Element | Tag | Source |
|---|---|---|---|
| 1 | Markings; copy number in the header, right-aligned | [M] | 1.2.16(5), (9); A-21; DR-10 |
| 2 | NZDF badge top left (2.5 cm); address line top right | [M] badge; [T] address | 3.2.18(2); Fig 3-6; BR-01, BR-05 |
| 3 | Date at the margin (abbreviated) | [M] | 1.2.10b; DR-07 |
| 4 | **COMJFNZ** (fixed), then "For information / See distribution" when there is a distribution list | [M] | 3.2.18(3); DR-15 |
| 5 | "CDF OPERATIONAL DIRECTIVE NN/YYYY", bold upper case, immediately above the operation name | [M] | 3.2.18(4) |
| 6 | "OPERATION [NAME]" as the subject heading | [M] | 3.2.18(5) |
| 7 | Authority: "Issued by the Chief of Defence Force." | [M] | 3.2.17(1); Fig 3-6 |
| 8 | Situation; Mission | [M] | 3.2.17(2)–(3) |
| 9 | Execution: optional lead, then **Intent.** and **Tasks.** | [M] | 3.2.17(4); Fig 3-6 |
| 10 | Coordinating instructions: optional lead, then elements (a)–(e) as the author's paragraphs | [M] | 3.2.17(5); DR-11 |
| 11 | Logistics and administration: optional lead, then elements (a)–(e) | [M] | 3.2.17(6); DR-11 |
| 12 | Command and control: optional lead, then elements (a)–(d) | [M] | 3.2.17(7); DR-11 |
| 13 | Acknowledgement | [M] | 3.2.17(8) |
| 14 | Cancellation instructions | optional | 3.2.17(9) |
| 15 | Signature: NAME / rank / Chief of Defence Force (no typed "for") | [M] | 3.2.18(7); DR-14 |
| 16 | Annex(es), Enclosure(s), Distribution: ; annex pages in scheme D | [D] | 3.2.18(8); fn 23 |
| — | Page numbers: every page including page 1 when the main document has two or more pages | [M] | 3.2.18(1); DR-01; V-05 |

**DR-11.** The 14 minimum elements are separate required fields:
- `coordinating_instructions`: command_and_control_arrangements, locations,
  timings, planning_guidance, freedoms_and_constraints;
- `logistics_and_administration`: logistics_guidance, finance_and_resources,
  public_affairs, legal_aspects, nzdf_output;
- `command_and_control`: command_status, dirlauth,
  critical_information_requirements, points_of_contact.

They are rendered in the prose order as the author's paragraphs. **No field
name is rendered as a heading.** With a section `lead`, the lead becomes the
numbered paragraph and the elements become a., b., …. Without one, each element
is a first-level paragraph.

**Rejected by the schema:**
- any missing section or minimum element, Intent or Tasks;
- a missing badge, or a badge other than the NZDF or gold-leaf badge (BR-04);
- a signatory other than CDF's block;
- addressees other than COMJFNZ;
- a `subject` field;
- an operation name that starts with "OPERATION";
- bullets.

**Warnings:**
- Tasks without mandatory language (3.2.17(4)(b));
- no Cancellation instructions (optional; DR-06);
- the order wording checks.

## 3. Implementation decisions (I-O)

| ID | Decision | Reason |
|---|---|---|
| I-O1 | Each section has an optional `lead` paragraph. | Fig 3-6 shows one numbered paragraph per section. DR-11 forbids generated headings, so the elements follow the lead or stand as paragraphs. |
| I-O2 | The field for 3.2.17(7)(c) is named `critical_information_requirements`. | The DFI text reads "Command critical information requirements". The wording is not reproduced, because the field is not rendered. |
| I-O3 | Gold-leaf badge permitted. | The directive is CDF's (1.2.26e; BR-04). 3.2.18(2) names the official NZDF badge, which is the default. |

## 4. Differences from Fig 3-6

| ID | Difference | Disposition |
|---|---|---|
| DO-01 | "Copy [ ] of [ ]" in the body at the left | DR-10: header, right-aligned (A-21). |
| DO-02 | One paragraph per section in Fig 3-6 | The required minimum elements are rendered as additional numbered paragraphs or sub-paragraphs (DR-11, I-O1). |
| DO-03 | Light-blue signature box; red placeholders | Not reproduced (D-06); black text. |

## 5. Not implemented (surfaced)

- **DR-12:** 3.2.16c lets the format change "to suit the particular
  circumstances". No extra-section mechanism exists, because DFI does not say
  where such sections go.
- **Out of scope:**
  - FRAGO format and the close-off signal (AC SCE, 3.2.16c–d);
  - CDF Warning Orders (3.2.15);
  - OPORDs and OPINSTs (COMJFNZ standards, 3.2.19).

## 6. Validation record (2026-10-01)

| Fixture | Purpose | Result |
|---|---|---|
| `3e-structure.yaml` | Every Fig 3-6 element, with section leads, distribution and annex | 3 pp; lint clean; compared with PDF pp 173–174 |
| `variant-no-leads.yaml` | No leads, no distribution (COMJFNZ only), no cancellation | Lint clean; DR-06 warning |
| `variant-classified-copy.yaml` | CONFIDENTIAL, copy number, annex | Copy number in the first-page header; "Page n of N" |

Visual comparison: LibreOffice with Carlito standing in for Calibri. Element
order, addressee block, identifier and operation name, and the Intent/Tasks
sub-paragraphs match Fig 3-6, apart from DO-01 to DO-03. Tests:
`renderer/tests/test_cdf_operational_directive.py`.
