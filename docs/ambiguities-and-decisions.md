# Ambiguity and decision register

Status values: **OPEN** (needs your decision), **PROPOSED** (my default; it will
be adopted unless you object), **DECIDED** (approved; the decision and date are
recorded).

## Decisions recorded 2026-10-01 (foundation review)

The foundation was provisionally approved. All **PROPOSED** defaults are adopted,
except as directed below.

| ID | Decision |
|---|---|
| A-01 | DECIDED: as proposed (no leading zero in correspondence, letters and administrative documents; leading zero in publication headers, record of change and repeal notes). |
| A-02 | DECIDED: as proposed. Leave the signing day blank by default, with configurable support for digital completion (`date.day`). |
| A-05 | DECIDED: follow the written DFI rule unless an explicit document-specific written rule overrides it. Conflicting template or example indentation is an ambiguity, not the governing rule. So correspondence and administrative documents (including delegations and the MOU) turn over to the margin; directives, AIs and DFO(T)s hang (fn 23, 3.2.11(6), 3.2.18(6), 3.2.22a(7)). |
| A-07 | DECIDED: follow the written prohibition on em dashes in generated administrative writing. Keep an em dash only where mandatory or prescribed boilerplate is reproduced verbatim. |
| A-34 | DECIDED: include **Financial and resource implications** in submissions, per the written structural requirement (2.1.12b(3)). |
| A-36 | DECIDED: the authority order is page **ii**, consistent with DFI 5.1 itself and the exemplars. The conflict with 4.4.7b(1) remains recorded. |
| A-02 / T-06 related | DECIDED: the primary product is a finished .docx. Blank reusable templates may come later. |
| Section E | DECIDED: correct obvious typographical or grammatical errors in generated content. Do **not** silently correct, update or reinterpret substantive policy, legislative or legal references (eg E-06 Privacy Act 1993): flag them for review. |
| T-01 / T-02 | DECIDED: Python/python-docx generation and validation, with structured YAML content and specification files. |
| T-06 | DECIDED: finished .docx first; blank templates later. |
| External inputs | DECIDED: missing external artefacts (NZDF_DSWT templates, badge/logo files, rank lists, PSR/DFO 51 material) must not block Phase 1. Record their absence, and design so they can be added later without rework. |

Every entry cites DFI 5.1 v2.01. A "proposed default" is how the renderer will
behave until you decide. It never changes the DFI.

- **Section A:** ambiguities and conflicts within DFI 5.1
- **Section E:** apparent errors in DFI template or boilerplate text
- **Section T:** technical and implementation decisions (not DFI matters)

---

## Phase 1 (Minute): items that emerged

Implementation decisions I-M1 to I-M12, discrepancies D-01 to D-10 and Word
verification items V-01 to V-04 are recorded in `templates/minute/NOTES.md` §6–7.
Decisions recorded 2026-10-01 (Minute gate review):

| ID | Decision |
|---|---|
| D-01 | DECIDED: bold every action addressee. The Annex 2C inconsistency stays in the discrepancy record. |
| D-06 | DECIDED: do not implement signature-area shading for now. It remains **unresolved** pending authoritative Word-template or digital-signature evidence. |
| D-09, D-10 | DECIDED: defer paragraph grading indicators and the single-approval statement. They are not implemented during the Minute validation gate. |
| I-M7 | Kept: Word conditional field. Verified in Word (V-01 PASS, 2026-10-01). |

## Submission: items that emerged

Decisions I-S1 to I-S8 and discrepancies DS-01 to DS-07 are recorded in
`templates/submission/NOTES.md`. Decisions recorded 2026-10-01 (Submission review):

| ID | Decision |
|---|---|
| S-01 | **APPROVED AS IMPLEMENTED.** Consultation is required. Content, Sections, Argument, Implications and Effects are **not** required as fixed headings. They are author considerations under the written guidance (2.1.12b(2)), not mandatory structure. (I-S3) |
| S-02 | **APPROVED AS IMPLEMENTED.** Financial and resource implications goes after Context and before Summary. This is an **implementation decision [I]**: DFI requires the paragraph (2.1.12b(3)) but does not specify its position. (I-S2) |

## Phase 2 (DPB, VR/PAR, internal and external letters): items that emerged

Full records are in each template's `NOTES.md` (I-D, I-V, I-L, I-E decisions;
DP, DV, DL, DE discrepancies). Decisions recorded 2026-10-01 (Phase 2 review):
all four items are **CLOSED**.

| ID | Decision |
|---|---|
| DL-02 | **APPROVED AS IMPLEMENTED.** When the day is to be handwritten, the month and year stay at the left margin. No reserved space is invented, because the written rule does not direct it (2.1.16(5)). |
| I-L4 | **APPROVED AS IMPLEMENTED.** One line between the body and the close, then six lines between the close and the signature block (1.2.21c). The close stays attached to the signature block. |
| I-V3 | **APPROVED AS IMPLEMENTED.** The travel table follows template 2Q, not example 2P. The discrepancy stays documented (DV-03, I-V3/I-V4). |
| I-D6 | **APPROVED AS IMPLEMENTED.** "Format" in Fig 2-17 is example content, not a mandatory DPB heading. |

Applied consistently with earlier decisions (recorded, no new decision needed):
the date indent of 1 cm for administrative documents where templates 2O and 2Q
show the margin (A-06, 2.2.3(1)); bold action addressees (D-01); upper-case
annex identifiers (A-12); the example's missing rank line in a letter
signature (DL-04, 2.1.16(17)).

## Phase status (2026-10-01)

Microsoft Word checks V-01 to V-04 **PASSED** on 2026-10-01 and are closed
(`templates/minute/NOTES.md` §7). The Word version, OS and per-check
observations were not supplied and are recorded as such.

The **shared renderer foundation for Phases 1–2 is accepted** (2026-10-01):
the engine, Annex 1A validation, Minute, Submission, DPB, VR/PAR, internal
and external letters. User direction: no further architectural changes unless a
subsequently implemented DFI document type requires them.

Next family: Administrative Instruction, CDF Directive, CDF Operational
Directive (`docs/phase3-directives-plan.md`). Decisions recorded below.

## Decisions recorded 2026-10-01 (Phase 3: identity artwork and directive family)

Governing principle (user, 2026-10-01): **DFI controls document structure; the
NZDF Visual Identity Standards (VIS) supply artwork and identity treatment only
where DFI points to them.** Where adopting a recommendation would introduce
information, structure or behaviour not supported by DFI, the item is surfaced
instead of adopted.

| ID | Decision |
|---|---|
| BR-01 | APPROVED. Use the official VIS artwork in generated NZDF documents within this repository. Keep provenance and checksums. Keep **one controlled source** (the VIS PDF). Derive the rendering assets reproducibly from it at render time; do not commit duplicate extracted artwork. |
| BR-02 | DECIDED. Do not invent wording-mark placement. Apply the Force for New Zealand wording mark only where the VIS and the applicable DFI document treatment support it. Do not add it to a DFI template that does not show it. |
| BR-03 | APPROVED. DFI-specific document layout takes precedence (unit name top right, Fig 2-8). |
| BR-04 | APPROVED. Standard NZDF badge by default. The CDF gold-leaf badge only where the source supports it: CDF and their office (1.2.26e, 2.1.16(3)(b)). |
| BR-05 | APPROVED. Intended size from the DFI figures, never below an applicable VIS minimum. |
| BR-06 | APPROVED. Replace the badge and logo placeholders in accepted Phase 1–2 outputs as the first Phase 3 step. This is a **controlled baseline update**: regression must show that the artwork is the only change. |
| DR-01 | DECIDED. Count the main document only (SECTIONPAGES) for the two-page threshold. Annexes keep their own numbering regime. |
| DR-02 | DECIDED. The AI follows A-11 and the general page-number rule (1.2.16(6)–(7)). |
| DR-03 | DECIDED. Number the AI cancellation paragraph (3.2.22a(7); the written rule wins). |
| DR-04 | DECIDED. Heading-only paragraphs are paragraph headings per 1.2.17(4): bold, with a full stop. |
| DR-05 | ADOPTED (traceable): "Tasks" as drawn in Fig 3-7. 3.2.22a(6) describes the content and does not prescribe heading text. |
| DR-06 | APPROVED, on condition: a section is **mandatory only where DFI prose requires it**. A section shown only in a template figure is optional: it is rendered when content is supplied, omitted cleanly otherwise, with a warning naming the omitted template section. Mandatory status is never inferred from a figure alone. |
| DR-07 | APPROVED. Date at the margin in all three types. |
| DR-08 | APPROVED. Dates generated within the text use the abbreviated form "2 Sep 26" (1.2.10b; A-01). |
| DR-09 | ADOPTED (traceable): warn on abbreviated day names (1.2.10a), except in the 1.2.10d combined day-date-time form. Warning only. |
| DR-10 | DECIDED. Copy number stays in the header, right-aligned (A-21). |
| DR-11 | DECIDED. The Op Directive minimum elements (3.2.17(5)–(7)) are **required schema fields**. They are rendered as the author's own paragraphs in the prose order. **No headings are generated for them.** Required fields and rendered headings are separate concepts. |
| DR-12 | **SURFACED, NOT ADOPTED.** The recommendation (optional extra sections before Acknowledgement) would add a structural position that DFI does not define. 3.2.16c permits the format to change but does not say how. The Op Directive is implemented in the fixed Fig 3-6 order only. Decide later if needed. |
| DR-13 | DECIDED. Commander and senior-executive directives are variants of the CDF Directive template (`issuer` option), not separate engines or templates. |
| DR-14 | ADOPTED (traceable, 3.2.11(7), 3.2.18(7)): CDF's block is always rendered. The handwritten "for" is not generated. |
| DR-15 | ADOPTED (traceable, [T]): "See distribution" weight as drawn: bold in Fig 3-5, regular in Figs 3-6 and 3-7. |
| DR-16 | ADOPTED (traceable, 3.2.22a(4)): AI Purpose uses the Fig 3-7 stem with its items; a warning when there are more than two. |
| DR-17 | DECIDED. Enforce the one-year limit as an error for CDF Directives. 3.2.9d states the period and makes the end-of-period action mandatory ("are to be incorporated … or cancelled"). Not applied to the commander and senior-executive variants: 3.2.9d is about CDF Directives, and 3.2.13b extends only the layout. |
| E-13 | DECIDED. Do not alter the fixed "DFO 14" reference. It is reproduced verbatim, and a warning flags it on every use, pending authoritative resolution. |
| E-14 | DECIDED. Obvious capitalisation error, corrected without changing meaning: "this administrative instruction" becomes "this Administrative Instruction" (Fig 3-7 Purpose stem and Cancellation), matching paras 1–3 and 3.2.21. |
| OP-01 | **OPEN (surfaced by BR-02).** 2.1.16(3)(c) requires the Force for New Zealand logotype with the logo on formal letters from members other than COS and the executive committee. Figs 2-7 to 2-12 do not show it, and the VIS placement (bottom right of a single-page document, or the back cover) does not fit multi-page letters. Not generated. Needs your decision. See `docs/baselines/2026-10-01-identity-artwork.md`. |
| V-05 | ADDED. Microsoft Word check of the directive page-1 conditional number. **NOT TESTED.** |


## A. Ambiguities and conflicts in DFI 5.1

### Originally needing your decision (all DECIDED 2026-10-01: see the decision tables above; text below is the original analysis)

| ID | Issue | DFI evidence | Proposed default |
|---|---|---|---|
| **A-01** | **Leading zero on the day of the month.** | The prose says "'0' is not to be included" (2.1.11(2), 2.1.16(5), 2.2.3(1)). Example 2E shows "01 Jun 25". Publication headers show "03 October 2025" (4.4.8a(5) "dd Month yyyy"); 4.4.17 shows "02 October 2015"; the record of change shows "03 November 2021". | No leading zero in correspondence, letters and administrative documents (the prose governs). Leading zero in publication headers, record of change and repeal notes (4.4.8 "dd"). |
| **A-02** | **Handwritten day.** The DFI expects the day to be handwritten at signing. Generated documents may be signed digitally. | fn 20, 2.1.11(2), 2.1.16(5), 2.2.3(1), 2.3.8(5). QA form note 3 allows digital or email sign-off. | Default: render the month and year only, leaving space for the day. Giving `date.day` fills the day when the document will be signed electronically. **DECIDED.** |
| **A-05** | **Turnover lines of first-level paragraphs in correspondence.** | The prose says subsequent lines "align with the left margin" (2.1.3(3)), and "hanging indents are not used in correspondence" (1.2.16(3)). Fig 1-4 follows this. Figs 2-3, 2-5 and 2-27 mix both styles on the same page. Delegations (2K–2N) and the MOU (2V) are drawn hanging throughout. | Applying the precedence rule (prose > figure): every correspondence and administrative document, **including delegations and the MOU** (2.2.3 applies the correspondence standards to them), has turnover lines back at the margin. Directives, AI and DFO(T): hanging (fn 23, 3.2.11(6)). **Question: do you want delegations and the MOU to follow the prose or the drawn templates?** |
| **A-07** | **Em dash in administrative documents.** | 1.2.7(10)(a) and 1.2.23c say no em dash in correspondence or administrative documentation; use a colon. The delegation templates and examples (2K–2N) and the MOU (2V) use em dashes. | Two repository rules collide here: verbatim boilerplate vs prose precedence. Proposed: keep the em dash in the **fixed boilerplate** of delegations and the MOU, and use a colon for list lead-ins in **user-authored** content. Alternative: replace with colons throughout (strict prose). |
| **A-10** | **Rank abbreviations and signature-block line 2.** DFI gives no authoritative rank-abbreviation list, and its examples are inconsistent. | fn 19 lists RA, MGEN, AVM, CDRE, AIRCDRE, BRIG, CAPT… Fig 2-18 uses "MAJGEN". 2.1.11(17)(b) says "Rank/Title and Service separated by a comma", but the examples show "BRIG" or "CDR" with no Service. | Accept rank and Service as input. Validate against a rank table you supply (or one we build from fn 19 plus a source you approve). Render "RANK, Service" only when a Service is given. **Question: is there an authoritative NZDF abbreviation list we should load?** |
| **A-13** | **Protective-marking vocabulary.** DFI defers to the PSR and DFO 51. It is inconsistent about whether IN-CONFIDENCE is a classification or an endorsement. | 1.1.10; 2.1.6c(4) "special handling marking"; 2.1.8(3) "In-Confidence classification"; 2.3.12c "endorsement marking"; 2.1.16(1) "UNCLASSIFIED – IN-CONFIDENCE". | Treat markings as validated input from a closed list (`standards/07` §2). **Question: can you supply the current NZDF/PSR marking list and combination rules (DFO 51 Vol 1 Ch 7)?** |
| **A-14** | **Badge position: header or below the header?** | 1.2.18a: the header contains no badge, and the badge goes immediately below the header in line with the address block. 2.1.16(3): the identifier goes "in the top left of the header" of a letter. The templates show the badge top left and the address top right, under the markings. | Place the badge in the first-page body area, top left, aligned with the address block (top right), below any markings. This matches both the figures and 1.2.18a. |
| **A-22** | **Sizes not stated in prose.** Minute originator descriptor and identifier; DPB, AI and agenda title lines; cover-sheet titles. | Fig 2-4 shows the descriptor centred, bold and visibly larger than 12 pt. | Measured from the DFI figures relative to the 12 pt body text: **16 pt** (I-M1), tagged `[T]`. **Better: if you have the official NZDF_DSWT Word templates (1.1.1f), they are the definitive source for these values (see T-03).** |
| **A-34** | **Submission: "Financial and resource implications" missing from the template.** | 2.1.12b(3): "all submissions must include specific text under a paragraph heading 'Financial and resource implications'". Figs 2-5 and 2-6 do not show it. | Add it as a mandatory paragraph heading at the end of Context (before Summary). The schema requires text (or an explicit "none" statement). |
| **A-36** | **Roman page numbering start in publications.** | 4.4.7b(1): numbering "commencing with 'i' on the first page of the authority order". Figs 4-4, 4-5 **and DFI 5.1 itself** (the exemplar, 4.4.1b) show "ii" on the authority order. | The precedence rule (prose) gives "i" on the authority order; every exemplar shows "ii". Proposed: follow the exemplar ("ii"), because the prose may simply count the unnumbered title page as "i". Please confirm. |

### Defaults (all ADOPTED 2026-10-01 unless decided otherwise above)

| ID | Issue | DFI evidence | Proposed default |
|---|---|---|---|
| A-03 | References heading wording | "References" with A., B. (1.2.19a); "Reference" without punctuation (2.1.11(9), Figs 2-3, 2-4); "Reference/s:" (Fig 1-4). | "Reference" for one reference and "References" for more, in bold, no colon, items A., B. |
| A-04 | Distribution: heading and threshold | Minute: more than six addressees (2.1.11(7)); the example note says "seven or more". Directive and AI: more than four (3.2.11(3), 3.2.22a(1)). Heading "**Distribution**" followed by a colon (2.1.11(7), Figs 2-4, 3-5) or not (Figs 1-4, 2-3). | Thresholds per type as stated. Heading "**Distribution:**" (with colon, per the prose). |
| A-06 | Date-line indentation | Administrative documents: month and year indented to 1 cm (2.2.3(1)). The minute example indents (Fig 2-3); the minute template does not (Fig 2-4). | Indent 1 cm for minutes, submissions and administrative documents (leaving room for the handwritten day). Letters at the left margin (2.1.16(5)). Ministerial notes at the right margin. |
| A-08 | "Six lines below the last line of text" | 1.2.21c; the templates show roughly four blank lines plus a shaded signature box. | Six empty body-style lines (12 pt, single) between the last text line and line 1 of the block. |
| A-09 | Quotation size "one half point lower font" | 1.2.14b | 11.5 pt (body minus 0.5 pt). Alternative: 11 pt. |
| A-11 | Page-number presentation | Fig 2-3 shows "[1 of xx (only if classified)]" vs prose "Page 1 of 25" (1.2.16(7)). Fig 3-7 (AI) shows "(Page 1 of 2)" on an unmarked template. Unclassified first page: not numbered (1.2.16(6)). | Prose governs: unclassified/restricted → plain number, no number on page 1 (except directives); above Restricted → "Page n of N". |
| A-12 | Annex and appendix identifying block | Prose: bold upper case. Examples: mixed case lines 2–3 ("Organisation Detail", "31 December 2021", "DD Mmm YY"). Appendix: "APPENDIX 1 OF ANNEX A" (1.2.24(2)(a)) vs "APPENDIX [n] TO ANNEX [X]" (Fig 1-6). | All lines bold upper case, right-aligned (the prose governs over the mixed-case examples, so dates read for example "31 DECEMBER 2021"). Appendix wording "APPENDIX 1 OF ANNEX A" (the prose governs over Fig 1-6). The date uses the parent document's date style. |
| A-15 | Internal letter salutation | 2.1.17c: "In most other formal letters there is no salutation". Templates 2H and the example 2G include an introduction line ("Dear Alexander"). | Salutation optional, controlled by the letter purpose (congratulatory/condolence: handwritten slot; admonition: none). |
| A-16 | Capital letter on recommendation items | 1.2.23b(1): single-sentence list items start lower case. Templates 2AC, 2AD and 2AF show "Note that"/"Agree to"; 2Y, 2Z and 2C show lower case. | Lower case, with the action verb in bold (1.2.11(2), 1.2.23). |
| A-17 | NTM naming and cover-sheet errors | 2.3.7 calls them "Note to the Minister" / "Note to the Minister Cover Sheet"; the annexes call them "Submission to the Minister". The 2AB footnote 1 reads "To accompany jointly prepared documents" (copied from 2X); the 2AB title placeholder reads "[TITLE OF BRIEFING NOTE]". | Keep the annex titles for template names. Reproduce fixed form text verbatim except E-09. |
| A-18 | Minister for Veterans template | 2.3.8(3) requires the Veterans' Affairs logo, which 2AD does not show. 2AD reads "Minister of Veterans" (the prose says "Minister for Veterans"). The referral line names the Minister of Defence. | Add the VA logo slot per the prose. Use "Minister for Veterans". Referral text as a parameter. |
| A-19 | Briefing note date position | 2AE: "Mmm YYYY" below the signature block; 2AF: "Date: [Select date]"; 2.3.8(5): month and year at the right margin (for notes). | Follow template 2AF ("Date:" below the signature block). |
| A-20 | Temporary delegation has two headings | 2L shows "[SUBJECT LINE]" and "DELEGATION OF AUTHORITY"; 2K shows only "DELEGATION OF AUTHORITY". | Optional subject line. When it is absent, "DELEGATION OF AUTHORITY" is the subject heading. |
| A-21 | Copy-number placement | 1.2.16(9): right-aligned in the header, below the markings. 1.2.18c: "appended immediately below the header". Fig 1-4: right-aligned in the body below the crest line (and fn 2: only above Restricted). Fig 3-6: at the left, in the body, above the date. | Header, right-aligned (1.2.16(9) is the most specific prose). |
| A-23 | Caption numbering without parts or chapters | 1.2.25b numbers by part (or chapter). Correspondence has neither. | Correspondence: "Table 1", "Figure 1" (sequence only). Publications: part-seq or chapter-seq. |
| A-24 | Shading and colours in tables and forms | Not stated in prose. The templates show grey header rows, grey label cells and importance boxes in red, orange and green. | Reproduce as `[T]`, with colours sampled from the DFI figures. |
| A-25 | Publication header footnote 98 | "If not separated into parts leave this line blank" is attached to the version-number item (4.4.8a(3)); logically it belongs to the part/chapter item (4). | Apply it to line 3 left (part/chapter); the version number is always shown. |
| A-26 | "Roman letters" / "Arabic letters" | 4.4.13 "lower case Roman letters"; 4.4.15c "lower case Arabic letters". Both mean Latin letters (a, b, c). | Latin lower-case letters a., b., c. |
| A-27 | "Annex(es)" / "Enclosure(s)" literal headings | The templates print the parenthetical forms. 1.2.24(5)(c) uses "Enclosure" for one. | Singular or plural by count: Annex/Annexes, Enclosure/Enclosures. |
| A-28 | Officer or Authority terminology | 4.1.11: Authorising **Authority** and Approving **Authority**. Templates 4E: Authorising **Officer**, Approving **Officer**. DFI 5.1's own preliminary provisions: "Approving Authority" and "Custodian". | Reproduce the 4E template headings verbatim (it is the template). |
| A-29 | Numbers below 10 vs quantitative amounts | 1.2.13(1): numerals for 10 and above. 1.2.13(3): spell out a number that "refers to a quantitative amount of units (ie, twelve)". | Apply (1). Spell out only at the start of a sentence. Flag (3) for drafting guidance only. |
| A-30 | External letter date | 2.1.16(5): all letters are dated. Example 2I has no date; template 2J has [Date]. | Date required. |
| A-31 | Classified pagination and annex numbering | Deferred to DFO 51 Vol 1 Ch 7 (1.2.24(1)(f), 4.4.7c). Not held. | Implement 1.2.16(7) "Page n of N" across the whole file. Flag any document above Restricted for manual check until DFO 51 is supplied. |
| A-32 | Identity standards reference | DFI 0.103 NZDF Identity Standards (1.1.3f, 4.1.7b) vs DFI 3.1 NZDF Identity Standards (1.2.26). 1.2.26f also names the "NZDF Visual Identity Standards". | Cite both. The supplied *NZDF Visual Identity Standards* v1.1 (Apr 2022) matches the 1.2.26f title, but it carries neither DFI reference. It is used for artwork and logo/logotype use only (see `source/nzdf-visual-identity/SOURCE.md`). |
| A-33 | Letterhead address size | Header/footer content 12 pt (1.2.16(4)(c)); Fig 1-4 annotates the unit address "(Calibri 10)". | 10 pt for the letterhead address block (it is not header content per 1.2.18a); 12 pt for header and footer content. |
| A-35 | Images inside forms | The NZDF QA form page 2 contains a sign-off process graphic (an image, not text). | Reproduce from a user-supplied image or omit with a placeholder. Do not redraw it. |
| A-37 | DFO drafting conformance | DFOs follow PCO drafting and punctuation rules (4.3.14a), which are not in DFI 5.1. | Generate the DFO layout per 4A–4G only. State that PCO conformance is out of scope. |
| A-38 | "UNCLASSIFIED" on unclassified documents | fn 24: not required. Publication templates show UNCLASSIFIED on every page; 4.4.7a(2): markings on all pages. | Correspondence: omit when unclassified (fn 24). Publications: always show the marking (4.4.7a(2)). Ministerial: minimum IN-CONFIDENCE (2.3.6f). |
| A-39 | Order of blocks after the signature | Fig 1-4: Annex(es), Enclosure(s), Distribution. Fig 2-17 (DPB): DTelN, Enclosure(s), Flags, Consulted. 1.2.16(9): Copy Distribution last. | Signature → DTelN → Annexes → Enclosures → Flags → Distribution → Copy Distribution → Consulted (DPB) or Ministerial referral (NTM). |
| A-40 | Which "briefs" may use the 4 cm right margin | 1.2.16(2) "briefs"; 2.2.7(1) DPB. | Optional for DPBs only (`margins: brief`). Not for briefing notes to the Minister (a fixed form). |

---

## E. Apparent errors in DFI template or boilerplate text

**Decision needed (T-11):** reproduce these verbatim (strict fidelity) or apply
the corrections below (fidelity with logged corrections)? Proposed default:
**correct E-01, E-02, E-08, E-11 and E-12 (pure typos and punctuation); keep the
others verbatim, flagged in the template notes, until you decide each one.**

| ID | Location | Text in DFI | Suggested correction |
|---|---|---|---|
| E-01 | 2C para 8 | "It is recommend that CA:" | "It is recommended that CA:" |
| E-02 | 2O signature block | "DTeIN" | "DTelN" |
| E-03 | 2M | Paras 6–9 should be 6 a.–c.; "Chief Financial Offer"; the delegation to the CFO refers to "functions imposed on Defence Legal Services" | Example only; fix if re-keyed as a fixture |
| E-04 | 3C para 5 | "c. is not entitled to— / d. [state all entitlements…]" (mis-levelled; the subject is missing) | "c. [Serviceperson's description] is not entitled to— (1) [state all non-entitlements …]" (as in 3B) |
| E-05 | 3B, 3C para 2 | "during his/her appointment" | Conflicts with 1.1.7 gender-neutral language: "during their appointment" |
| E-06 | 3A para 5; 2V cl 18–19; 2.3.2b(6); 2.3.14b(1) | "Privacy Act 1993" (repealed); "Privacy Act 1990" (never existed) | "Privacy Act 2020" (as in 1.1.10h, 4.2.4f) |
| E-07 | 2W Disclaimer | "…do not necessarily represent the views of the New Zealand Government will not legally be responsible…" (a missing clause) | Needs your wording. Likely "…the views of the New Zealand Defence Force or the New Zealand Government. The New Zealand Government will not…" |
| E-08 | 2L para 3d, 5a–b | "'absent on duty;" (missing closing quote); "You must…" capitalised in a single-sentence list | "'absent on duty';", "you must…" |
| E-09 | 2AB | Footnote 1 "To accompany jointly prepared documents"; Title "[TITLE OF BRIEFING NOTE]" | "To accompany NZDF submissions to the Minister of Defence"; "[TITLE OF SUBMISSION]" (needs approval) |
| E-10 | Annex A abbreviations | "HQNZDF: Headquarters Defence Force New Zealand" | "Headquarters New Zealand Defence Force" (as on the title page) |
| E-11 | 2V cl 15 | "own resources and;" | "own resources and:" (or an em dash, per A-07) |
| E-12 | 2Q, 2Z, 2AC, 2AD | Enclosure item "1" without a full stop; "[Addressee (through Appointment XYZ]" with an unclosed parenthesis | "1."; "[Addressee] (through [Appointment])" |
| E-13 | 3D para 15 (first cancellation option) | "…incorporated in DFO 14 and no later than DD Mmm YYYY." "DFO 14" is printed as fixed text, not as a placeholder | DECIDED 2026-10-01: reproduce verbatim and flag with a warning; no correction without an authoritative basis |
| E-14 | 3F paras 1–4 and Cancellation | "Administrative Instruction" vs "administrative instruction" within the same boilerplate | DECIDED 2026-10-01: corrected to "Administrative Instruction" (obvious capitalisation error) |

---

## BR. Brand artwork (NZDF Visual Identity Standards, supplied 2026-10-01)

Source: `source/nzdf-visual-identity/` (record, checksum and artwork map). DFI 5.1
still governs layout. **All items DECIDED 2026-10-01**: see the Phase 3 decision table above. Original analysis below.

| ID | Issue | Evidence | Recommendation | Alternative |
|---|---|---|---|---|
| BR-01 | **Extraction, storage and authorisation.** The badges and logos are protected (Flags, Emblems, and Names Protection Act 1981; VIS p3). The VIS says not to manipulate, recolour or recreate them. | VIS pp 3, 8, 12 | Render the vector artwork unaltered, at 600 dpi with a transparent background, into `renderer/assets/` as derived files. Record each file's source page and checksum. Insert each as a real Word inline picture. Needs your confirmation that you are authorised to reproduce the artwork in generated documents, and that committing it to this repository is acceptable. | Keep the assets local and git-ignored (T-05), supplied at render time. |
| BR-02 | **Force for New Zealand logotype placement.**<br>- DFI: the logo is used "in conjunction with" the logotype "as specified in the NZDF Visual Identity Standards" (1.2.26f), and the identifier goes top left of the header (2.1.16(3)).<br>- VIS: the logotype is secondary, at 50 per cent of the logo's size, "bottom right hand corner of a single page document or on the back cover of a multi-page document".<br>- The current fixtures label the logo and logotype together, top left. | 1.2.26f, 2.1.16(3)(c); VIS pp 10–11 | NZDF or Service logo top left of page 1. The logotype bottom right of page 1, in the first-page footer at 50 per cent of the logo's size. This is correct for one-page letters. For multi-page letters it is a logged deviation, because a letter has no back cover. | Logotype on the last page, bottom right (an anchored picture); or no logotype ("when appropriate", 1.2.26f). |
| BR-03 | **Unit name with the logo.**<br>- VIS: a portfolio, command or unit name goes in plain text beside the NZDF logo, separated by a rule.<br>- DFI 2H: [Unit name] in bold at the top right, above the sender address. | 2.1.16(4), Fig 2-8; VIS p13 | DFI governs the letter layout: unit name top right, as now. | VIS treatment. |
| BR-04 | **CDF gold-leaf badge.**<br>- DFI: "CDF and their office may use the gold leaf badge" (1.2.26e, 2.1.16(3)(b)).<br>- VIS: "reserved for the sole use of the Chief of Defence Force".<br>- 3.2.11(2) and Fig 3-5 show the standard assented badge on CDF Directives. | 1.2.26e, 2.1.16(3)(b), 3.2.11(2); VIS p12 | Default to the standard badge everywhere. Gold is an option only when the originator is CDF or the Office of CDF (DFI governs the "their office" scope). The schema rejects it otherwise. | Gold for CDF only (VIS). |
| BR-05 | **Device size.** DFI prose gives no size. The VIS gives a 35 mm minimum width for the NZDF logo and no size for the badge. | VIS p8; Figs 1-4, 2-8, 3-5 | Measure the size from the DFI figures relative to the 12 pt body (`[T]`, as in A-22), never below the VIS minimum. Hold it as a token. | A size you specify. |
| BR-06 | **Scope and timing.** The current letters and Annex 1A fixtures use free-text device labels and placeholders. Real artwork would change the appearance of accepted Phase 1–2 outputs, and needs a fixed device vocabulary (eg `nzdf_badge`, `cdf_gold_badge`, `army_logo`). | T-05; user direction of 2026-10-01 on architectural changes | Add the artwork as the first step of Phase 3, because CDF Directives and Op Directives need the badge (3.2.11(2), 3.2.18(2)). In the same step, apply it to the letters and Annex 1A, with a regression check that only the device changes. | Phase 3 types only; keep the placeholders in Phase 1–2 types. |

Still not held (needed later): the Veterans' Affairs logo (2.3.8(3); A-18), the MoD Chief
Executive coat of arms (2.3.8(2)), the Office of the Chief Executives crest (Joint
Note), and command or unit badges (3.2.12b).

## T. Technical and implementation decisions

| ID | Decision | Options | Recommendation | Status |
|---|---|---|---|---|
| **T-01** | Rendering stack | (a) Python 3 + python-docx with an OXML helper layer; (b) Node + `docx` (docx-js); (c) fill official `.dotx` templates | **(a) Python.** It reads and writes .docx (needed for validation as well as generation). Pydantic, Jinja2 and PyYAML are already available. The OXML layer covers what python-docx lacks (numbering definitions, footnotes, fields, watermark). | DECIDED |
| **T-02** | Content input format | (a) YAML document files validated by per-template schemas; (b) Markdown with front matter; (c) Python API only | **(a) YAML** with a small inline mark-up for **bold**, *italic*, footnotes and cross-references. It maps 1:1 to DFI structural elements, so the schema can enforce mandatory elements. | DECIDED |
| **T-03** | Source of Word styles | (a) Generate all styles from `standards/spec/dfi-5.1-tokens.yaml`; (b) start from the official NZDF_DSWT `.dotx` files (1.1.1f) | **(b) if you can supply them; otherwise (a).** The official templates would settle A-22 and A-24 and give exact style names. **Do you have access to the NZDF_DSWT templates?** | OPEN: official templates not supplied; styles generated from tokens meanwhile |
| **T-04** | Verification rendering | LibreOffice headless docx→PDF→PNG for visual comparison with DFI pages | Use it, with Carlito standing in for Calibri. Final sign-off in MS Word by a human reviewer. | ADOPTED |
| **T-05** | Badge, logo and coat-of-arms assets | Extract from the DFI PDF (low resolution, not authorised) vs supplied official artwork | **Supplied official artwork only**, stored in `renderer/assets/` (git-ignored if restricted). Until then, render a labelled placeholder frame. | DECIDED 2026-10-01 (BR-01): official artwork from the NZDF Visual Identity Standards (`source/nzdf-visual-identity/`), derived reproducibly at render time. |
| **T-06** | Product type | (a) Generate **finished documents** from structured content; (b) generate **blank Word templates** with placeholders (like the DSWT); (c) both | **(c), with (a) first.** The engine that fills documents can also emit templates with DFI placeholder text. | DECIDED (finished .docx first) |
| **T-07** | Output formats | .docx only; optional PDF via LibreOffice; PDF permission security (1.1.3d(8)) | .docx primary; PDF optional for previews only; PDF security left to the user's approved tooling. | ADOPTED |
| **T-08** | DFI file location | Moved `dfi_5_1.pdf` from the repo root to `source/dfi-5.1/` with `git mv`. The bytes are unchanged; the SHA-256 is recorded. | Done during this phase. Revert if you want the file at the root. | ADOPTED |
| **T-09** | Validation approach | (1) Schema validation of input; (2) docx structural lint (fonts, sizes, margins, markings on every page, numbering, no bullets where forbidden, signature-block orphan rule); (3) visual diff against re-keyed DFI examples | All three, as in `docs/architecture.md` §6. | ADOPTED |
| **T-10** | Content assistance | Should Claude also lint the **wording** (directive language, abbreviations, numbers, dates, NZ spelling) or only the layout? | Layout is enforced. Wording rules are reported as warnings, never rewritten automatically. | ADOPTED |
| **T-11** | Policy for DFI errors (section E) | Strict verbatim vs logged corrections | See section E. | DECIDED (section E policy above) |
| **T-12** | Implementation order | `docs/implementation-plan.md` | Approve or re-order P1–P4. | DECIDED (P1, then the Phase 2 batch DPB → VR/PAR → letters; see implementation-plan.md) |
