# Controlled baseline update: identity artwork (BR-06), 2026-10-01

**Change.** In the accepted Phase 1–2 outputs, the labelled badge and logo
placeholders are replaced with the official artwork from the NZDF Visual
Identity Standards (BR-01). The artwork is rendered at render time from the
controlled source, and its checksum is verified first. Sizes follow BR-05:
badge 2.5 cm high, logo 1.25 cm high, with a minimum logo width of 35 mm.

**Inputs changed.** The fixture `letterhead.device` values changed from free
text to manifest keys:

| Fixture | Before | After | Note |
|---|---|---|---|
| annex-1a/1a-classified, 1a-unclassified | NZDF badge | `nzdf_badge` | Fig 1-4 |
| internal-letter/2g-example | RNZAF logo with Force for New Zealand logotype | `airforce_logo` | Fig 2-7 shows the logo only (BR-02) |
| internal-letter/2h-typed-structure | NZ Army logo with Force for New Zealand logotype | `army_logo` | BR-02 |
| internal-letter/2h-handwritten-congratulatory | NZDF logo with Force for New Zealand logotype | `nzdf_logo` | BR-02 |
| external-letter/2i-example | NZ Army badge | `army_logo` | **Correction.** Fig 2-10 shows the NZ Army logo. This was already recorded as DE-02, but the fixture said "badge". 2.1.16(3)(c) agrees: the signatory is a Deputy Chief of Army, not a COS. |
| external-letter/2j-typed-structure | NZ Army logo with Force for New Zealand logotype | `army_logo` | BR-02 |
| external-letter/2j-handwritten, variant-unnamed-recipient | NZDF logo with Force for New Zealand logotype | `nzdf_logo` | BR-02 |

No other content, template, token or block changed for these outputs. The
`identity.*` tokens and the image insertion in `letterhead` are new.

## Proof 1: package-level comparison of every fixture

Method:
1. `python -m staffwriting.baseline snapshot` was run on the accepted code
   (commit `7930669`, in a temporary worktree) and on the updated code.
2. Each snapshot holds the canonical XML of every package part, with
   relationship ids resolved to their targets, plus the media checksums.
3. `python -m staffwriting.baseline prove-artwork before after` then
   checked each differing fixture: the placeholder run is replaced by one
   picture run and nothing else in the document changes; exactly one image
   relationship is added and none removed; only the PNG content type is added;
   exactly one media part appears.

```
PASS annex-1a__1a-classified
    ok   content types: PNG default added only
    ok   media: exactly one image (348137 B)
    ok   relationships: one image relationship added, none removed
    ok   document: one placeholder run replaced by one picture run, all else identical
PASS annex-1a__1a-unclassified
    ok   content types: PNG default added only
    ok   media: exactly one image (348137 B)
    ok   relationships: one image relationship added, none removed
    ok   document: one placeholder run replaced by one picture run, all else identical
PASS external-letter__2i-example
    ok   content types: PNG default added only
    ok   media: exactly one image (38334 B)
    ok   relationships: one image relationship added, none removed
    ok   document: one placeholder run replaced by one picture run, all else identical
PASS external-letter__2j-handwritten
    ok   content types: PNG default added only
    ok   media: exactly one image (40026 B)
    ok   relationships: one image relationship added, none removed
    ok   document: one placeholder run replaced by one picture run, all else identical
PASS external-letter__2j-typed-structure
    ok   content types: PNG default added only
    ok   media: exactly one image (38334 B)
    ok   relationships: one image relationship added, none removed
    ok   document: one placeholder run replaced by one picture run, all else identical
PASS external-letter__variant-unnamed-recipient
    ok   content types: PNG default added only
    ok   media: exactly one image (40026 B)
    ok   relationships: one image relationship added, none removed
    ok   document: one placeholder run replaced by one picture run, all else identical
PASS internal-letter__2g-example
    ok   content types: PNG default added only
    ok   media: exactly one image (45957 B)
    ok   relationships: one image relationship added, none removed
    ok   document: one placeholder run replaced by one picture run, all else identical
PASS internal-letter__2h-handwritten-congratulatory
    ok   content types: PNG default added only
    ok   media: exactly one image (40026 B)
    ok   relationships: one image relationship added, none removed
    ok   document: one placeholder run replaced by one picture run, all else identical
PASS internal-letter__2h-typed-structure
    ok   content types: PNG default added only
    ok   media: exactly one image (38334 B)
    ok   relationships: one image relationship added, none removed
    ok   document: one placeholder run replaced by one picture run, all else identical
12 fixture(s) identical in every part; 9 changed
```

Result: **PASS.** 12 fixtures are identical in every part. In the 9 changed
fixtures, the only change is the artwork.

## Proof 2: rendered pagination (LibreOffice with Carlito)

Every fixture was rendered to PDF before and after. Page counts are identical
for all 21. The text on each page is identical for 19 (ignoring the placeholder
text). In the two Annex 1A fixtures, sub-paragraph 5a moves from the foot of
page 1 to the top of page 2. The reason is that the badge is 2.5 cm high, while
the placeholder was two text lines. This is the direct, expected effect of the
artwork occupying its DFI-figure size. No text, order or formatting changed.
DFI figure pagination is illustrative only (D-08).

## Open point raised by this update

**OP-01.** 2.1.16(3)(c) says that members other than COS and the executive
committee "are to use the NZDF logo or relevant single-Service logo **and the
Force for New Zealand logotype**" on formal letters. Figs 2-7 to 2-12 show
the logo only. The VIS places the wording mark bottom right of a single-page
document or on the back cover. Per BR-02, it is not added. The prose
requirement therefore remains unmet in generated letters until you decide
where the wording mark goes.

## Re-check at the end of the Phase 3 family (2026-10-01)

The same proof was run on the final Phase 3 code (after the shared directive
capabilities, the AI, the CDF Directive and the Op Directive) against the
accepted Phase 1–2 snapshot:

```
12 fixture(s) identical in every part; 9 changed; 11 new (not in the first snapshot)
```

All 9 changed fixtures pass `prove-artwork`: the artwork is still their only
change. The 11 new fixtures belong to the three new document types. None of
the Phase 3 shared changes altered an accepted output.
