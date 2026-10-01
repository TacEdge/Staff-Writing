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
| I-M7 | Kept: Word conditional field; to be verified in Word (V-01). |

## Submission: items that emerged

Decisions I-S1 to I-S8 and discrepancies DS-01 to DS-07 are recorded in
`templates/submission/NOTES.md`. Decisions recorded 2026-10-01 (Submission review):

| ID | Decision |
|---|---|
| S-01 | **APPROVED AS IMPLEMENTED.** Consultation is required. Content, Sections, Argument, Implications and Effects are **not** required as fixed headings. They are author considerations under the written guidance (2.1.12b(2)), not mandatory structure. (I-S3) |
| S-02 | **APPROVED AS IMPLEMENTED.** Financial and resource implications goes after Context and before Summary. This is an **implementation decision [I]**: DFI requires the paragraph (2.1.12b(3)) but does not specify its position. (I-S2) |

## Phase 2 (DPB, VR/PAR, internal and external letters): items that emerged

Full records are in each template's `NOTES.md` (I-D, I-V, I-L, I-E decisions;
DP, DV, DL, DE discrepancies). These need your decision:

| ID | Issue | Proposed |
|---|---|---|
| DL-02 | Letters: with the day left blank for handwriting, the date reads "November 2025" at the left margin and no space is reserved for the day. 2.1.16(5) says left margin and handwritten day, but not where the day goes. | Keep at the margin (prose). Alternative: reserve space with a leading tab. |
| I-L4 | Letters: the template shows about four lines before the close and one after; the prose requires the signature block six lines below the last line of text. | Close one line below the last paragraph; signature block six lines below the close (prose) |
| I-V3 | VR/PAR travel table: "Event" and "Dates" rows full width with the value in bold (template 2Q), not as labels (example 2P). | Template governs |
| I-D6 | DPB: "Format" in Fig 2-17 treated as a placeholder group heading, not a fixed heading. | Placeholder (author's own group headings) |

Applied consistently with earlier decisions (recorded, no new decision needed):
the date indent of 1 cm for administrative documents where templates 2O and 2Q
show the margin (A-06, 2.2.3(1)); bold action addressees (D-01); upper-case
annex identifiers (A-12); the example's missing rank line in a letter
signature (DL-04, 2.1.16(17)).

## Phase status (2026-10-01)

Phase 1 (engine, Annex 1A validation, Minute, Submission) is **provisionally
accepted, pending Microsoft Word validation**. Phase 2 (DPB, VR/PAR, internal
and external letters) is **implemented and awaiting review**; the same Word
checks apply to it. Checks V-01 to V-04
(`templates/minute/NOTES.md` §7) have **not been tested in Word**. Do not
report them as passed until a person has opened the outputs in Word and
recorded the result.

## A. Ambiguities and conflicts in DFI 5.1

### Needing your decision (OPEN)

| ID | Issue | DFI evidence | Proposed default |
|---|---|---|---|
| **A-01** | **Leading zero on the day of the month.** | The prose says "'0' is not to be included" (2.1.11(2), 2.1.16(5), 2.2.3(1)). Example 2E shows "01 Jun 25". Publication headers show "03 October 2025" (4.4.8a(5) "dd Month yyyy"); 4.4.17 shows "02 October 2015"; the record of change shows "03 November 2021". | No leading zero in correspondence, letters and administrative documents (the prose governs). Leading zero in publication headers, record of change and repeal notes (4.4.8 "dd"). |
| **A-02** | **Handwritten day.** The DFI expects the day to be handwritten at signing. Generated documents may be signed digitally. | fn 20, 2.1.11(2), 2.1.16(5), 2.2.3(1), 2.3.8(5). QA form note 3 allows digital or email sign-off. | Default: render the month and year only, leaving space for the day. Option `date_mode: full` fills the day when the document will be signed electronically. Please confirm this option is acceptable. |
| **A-05** | **Turnover lines of first-level paragraphs in correspondence.** | The prose says subsequent lines "align with the left margin" (2.1.3(3)), and "hanging indents are not used in correspondence" (1.2.16(3)). Fig 1-4 follows this. Figs 2-3, 2-5 and 2-27 mix both styles on the same page. Delegations (2K–2N) and the MOU (2V) are drawn hanging throughout. | Applying the precedence rule (prose > figure): every correspondence and administrative document, **including delegations and the MOU** (2.2.3 applies the correspondence standards to them), has turnover lines back at the margin. Directives, AI and DFO(T): hanging (fn 23, 3.2.11(6)). **Question: do you want delegations and the MOU to follow the prose or the drawn templates?** |
| **A-07** | **Em dash in administrative documents.** | 1.2.7(10)(a) and 1.2.23c say no em dash in correspondence or administrative documentation; use a colon. The delegation templates and examples (2K–2N) and the MOU (2V) use em dashes. | Two repository rules collide here: verbatim boilerplate vs prose precedence. Proposed: keep the em dash in the **fixed boilerplate** of delegations and the MOU, and use a colon for list lead-ins in **user-authored** content. Alternative: replace with colons throughout (strict prose). |
| **A-10** | **Rank abbreviations and signature-block line 2.** DFI gives no authoritative rank-abbreviation list, and its examples are inconsistent. | fn 19 lists RA, MGEN, AVM, CDRE, AIRCDRE, BRIG, CAPT… Fig 2-18 uses "MAJGEN". 2.1.11(17)(b) says "Rank/Title and Service separated by a comma", but the examples show "BRIG" or "CDR" with no Service. | Accept rank and Service as input. Validate against a rank table you supply (or one we build from fn 19 plus a source you approve). Render "RANK, Service" only when a Service is given. **Question: is there an authoritative NZDF abbreviation list we should load?** |
| **A-13** | **Protective-marking vocabulary.** DFI defers to the PSR and DFO 51. It is inconsistent about whether IN-CONFIDENCE is a classification or an endorsement. | 1.1.10; 2.1.6c(4) "special handling marking"; 2.1.8(3) "In-Confidence classification"; 2.3.12c "endorsement marking"; 2.1.16(1) "UNCLASSIFIED – IN-CONFIDENCE". | Treat markings as validated input from a closed list (`standards/07` §2). **Question: can you supply the current NZDF/PSR marking list and combination rules (DFO 51 Vol 1 Ch 7)?** |
| **A-14** | **Badge position: header or below the header?** | 1.2.18a: the header contains no badge, and the badge goes immediately below the header in line with the address block. 2.1.16(3): the identifier goes "in the top left of the header" of a letter. The templates show the badge top left and the address top right, under the markings. | Place the badge in the first-page body area, top left, aligned with the address block (top right), below any markings. This matches both the figures and 1.2.18a. |
| **A-22** | **Sizes not stated in prose.** Minute originator descriptor and identifier; DPB, AI and agenda title lines; cover-sheet titles. | Fig 2-4 shows the descriptor centred, bold and visibly larger than 12 pt. | Measure from the DFI figures relative to the 12 pt body text (I estimate 14 pt) and tag the value `[T]`. **Better: if you have the official NZDF_DSWT Word templates (1.1.1f), they are the definitive source for these values (see T-03).** |
| **A-34** | **Submission: "Financial and resource implications" missing from the template.** | 2.1.12b(3): "all submissions must include specific text under a paragraph heading 'Financial and resource implications'". Figs 2-5 and 2-6 do not show it. | Add it as a mandatory paragraph heading at the end of Context (before Summary). The schema requires text (or an explicit "none" statement). |
| **A-36** | **Roman page numbering start in publications.** | 4.4.7b(1): numbering "commencing with 'i' on the first page of the authority order". Figs 4-4, 4-5 **and DFI 5.1 itself** (the exemplar, 4.4.1b) show "ii" on the authority order. | The precedence rule (prose) gives "i" on the authority order; every exemplar shows "ii". Proposed: follow the exemplar ("ii"), because the prose may simply count the unnumbered title page as "i". Please confirm. |

### Proposed defaults (PROPOSED: adopted unless you object)

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
| A-32 | Identity standards reference | DFI 0.103 NZDF Identity Standards (1.1.3f, 4.1.7b) vs DFI 3.1 NZDF Identity Standards (1.2.26). | Cite both. The asset source is your call (T-05). |
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

---

## T. Technical and implementation decisions

| ID | Decision | Options | Recommendation | Status |
|---|---|---|---|---|
| **T-01** | Rendering stack | (a) Python 3 + python-docx with an OXML helper layer; (b) Node + `docx` (docx-js); (c) fill official `.dotx` templates | **(a) Python.** It reads and writes .docx (needed for validation as well as generation). Pydantic, Jinja2 and PyYAML are already available. The OXML layer covers what python-docx lacks (numbering definitions, footnotes, fields, watermark). | OPEN |
| **T-02** | Content input format | (a) YAML document files validated by per-template schemas; (b) Markdown with front matter; (c) Python API only | **(a) YAML** with a small inline mark-up for **bold**, *italic*, footnotes and cross-references. It maps 1:1 to DFI structural elements, so the schema can enforce mandatory elements. | OPEN |
| **T-03** | Source of Word styles | (a) Generate all styles from `standards/spec/dfi-5.1-tokens.yaml`; (b) start from the official NZDF_DSWT `.dotx` files (1.1.1f) | **(b) if you can supply them; otherwise (a).** The official templates would settle A-22 and A-24 and give exact style names. **Do you have access to the NZDF_DSWT templates?** | OPEN |
| **T-04** | Verification rendering | LibreOffice headless docx→PDF→PNG for visual comparison with DFI pages | Use it, with Carlito standing in for Calibri. Final sign-off in MS Word by a human reviewer. | PROPOSED |
| **T-05** | Badge, logo and coat-of-arms assets | Extract from the DFI PDF (low resolution, not authorised) vs supplied official artwork | **Supplied official artwork only**, stored in `renderer/assets/` (git-ignored if restricted). Until then, render a labelled placeholder frame. | OPEN |
| **T-06** | Product type | (a) Generate **finished documents** from structured content; (b) generate **blank Word templates** with placeholders (like the DSWT); (c) both | **(c), with (a) first.** The engine that fills documents can also emit templates with DFI placeholder text. | OPEN |
| **T-07** | Output formats | .docx only; optional PDF via LibreOffice; PDF permission security (1.1.3d(8)) | .docx primary; PDF optional for previews only; PDF security left to the user's approved tooling. | PROPOSED |
| **T-08** | DFI file location | Moved `dfi_5_1.pdf` from the repo root to `source/dfi-5.1/` with `git mv`. The bytes are unchanged; the SHA-256 is recorded. | Done during this phase. Revert if you want the file at the root. | PROPOSED |
| **T-09** | Validation approach | (1) Schema validation of input; (2) docx structural lint (fonts, sizes, margins, markings on every page, numbering, no bullets where forbidden, signature-block orphan rule); (3) visual diff against re-keyed DFI examples | All three, as in `docs/architecture.md` §6. | PROPOSED |
| **T-10** | Content assistance | Should Claude also lint the **wording** (directive language, abbreviations, numbers, dates, NZ spelling) or only the layout? | Layout is enforced. Wording rules are reported as warnings, never rewritten automatically. | PROPOSED |
| **T-11** | Policy for DFI errors (section E) | Strict verbatim vs logged corrections | See section E. | OPEN |
| **T-12** | Implementation order | `docs/implementation-plan.md` | Approve or re-order P1–P4. | OPEN |
