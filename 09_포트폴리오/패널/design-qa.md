# Design QA — 하루안부 ATOMX 패널

- Source visual truth:
  - `_뷰어에셋/ref-ATOMX-01_개요리서치판_보드1원본.png`
  - `_뷰어에셋/ref-ATOMX-02_화면갤러리판_하루안부배치WIP_보드2원본.png`
- Implementation:
  - `하루안부_패널_ATOMX판_A4가로_2장.html`
  - `_뷰어에셋/atomx-b1.png`
  - `_뷰어에셋/atomx-b2.png`
- Viewport: A4 landscape, 297 × 210mm; browser QA viewport 1122 × 794 CSS px per board.
- Density normalization: implementation viewer assets 3507 × 2480px. Reference preview assets 1572 × 1112px were normalized to 1754 × 1240px for full-view comparisons. PDF pages were rendered independently at 120dpi for print verification.
- State: all embedded app screens loaded; print background enabled; two-page PDF.
- Full-view evidence:
  - `_qa/compare-board1.png`
  - `_qa/compare-board2.png`
- Focused-region evidence:
  - `_qa/compare-board2-focus.png` — board 2 right/lower clinical and system region.
  - `_qa/compare-when-opacity.png` — reported transparent clock body versus the corrected opaque cutout.
- Browser-rendered evidence:
  - `_qa/chrome-final-css.png`
  - `_qa/pdf-final/page-2-latest.png`

## Findings

- No actionable P0/P1/P2 visual differences remain.
- Fonts and typography: the existing SUIT/Pretendard token scale, weights, line height, and letter spacing remain intact. Added system evidence uses only the existing 5.4pt, 6.1pt, and 12.4pt tokens.
- Spacing and layout rhythm: the source's asymmetric five-zone gallery and 4.2mm outer margin remain intact. The clinical evidence band now occupies the source's production-evidence position without colliding with the lower device row.
- Colors and visual tokens: role colors remain fixed to family blue, care-team green, and resident orange. No new gradient family or semantic color was introduced.
- Image quality and asset fidelity: the two generated Korean elder-care photographs are correctly cropped for their panel slots, have sufficient source resolution for their physical print sizes, and avoid hospital/emergency framing. The When graphic now preserves the solid white clock face and pale-blue pedestal while only the exterior background remains transparent.
- Copy and content: service identity, patient canon, SaMD-safe wording, sourced statistics, and vendor-neutral AI language remain unchanged.
- Icons: existing product icons and device chrome remain unchanged; no emoji was introduced.
- Print: final PDF is two A4 landscape pages with backgrounds, live-screen captures, page runner, and no clipped board content.
- Console: one non-blocking `MutationObserver.observe` TypeError was observed inside an embedded app during browser inspection; it did not affect any visible panel screen or the final PDF render.

## Comparison history

1. Earlier P1: clinician SOS was 9.2mm wide and the clinician web dashboard was reduced to an unreadable full-page thumbnail.
   - Fix: replaced both with larger, focused crops; SOS now reads as a distinct alert surface and the web view exposes the relevant activity context.
   - Post-fix evidence: `_qa/compare-board2-focus.png`.
2. Earlier P1: board 2 had no visible design-system evidence.
   - Fix: added a compact three-column evidence strip for 357 tokens, role colors, the shared icon/tab language, and deliberately removed patterns.
   - Post-fix evidence: `_qa/compare-board2.png` and `_qa/pdf-final/page-2-latest.png`.
3. Earlier P2: supporting lifestyle photos looked like generic promotional imagery and the resident photo's autumn palette fought the source's cool blue field.
   - Fix: generated and placed two calm Korean elder-care facility images with matching cool daylight and dignified subjects.
   - Post-fix evidence: `_뷰어에셋/atomx-b1.png` and `_뷰어에셋/atomx-b2.png`.
4. Earlier P2: PDF export occasionally captured the final clinician screen before it finished loading.
   - Fix: re-exported after the embedded screens settled and verified the second page visually.
   - Post-fix evidence: `_qa/pdf-final/page-2-latest.png`.
5. Earlier P2: background extraction removed the pale clock face and pedestal along with the checkerboard, making the When graphic look unintentionally hollow.
   - Fix: regenerated the asset against an object-safe chroma background, removed only that background, and replaced the panel asset with the corrected RGBA cutout.
   - Post-fix evidence: `_qa/compare-when-opacity.png`.

## Primary checks

- Live HTML loaded both boards and all embedded device/app frames.
- Two-page print pagination and A4 landscape page size confirmed.
- Browser console checked.
- No new navigation or form behavior was required because the deliverable is a static print panel; the embedded source apps remain live in the HTML preview.

## Follow-up polish

- P3: if the final physical test print makes the 5.4pt evidence captions feel too light, increase only weight/ink within the existing token system rather than increasing the type scale.

final result: passed
