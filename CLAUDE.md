# CLAUDE.md

Guidance for AI coding assistants working in this repository.

## Project Overview

하루안부 (Haru Anbu) is a senior-care service design project (university coursework / exhibition /
competition deliverables). The product is a set of high-fidelity **static HTML prototypes** — no build
step, no framework — for four user roles, plus a public showcase site and a Next.js "making-of"
presentation microsite. Prototypes exist in ko/en/zh variants (`*.html`, `*.en.html`, `*.zh.html`).

Data canon (fixed across all designs — do not invent new patients):
박영자 78·A-3 / 최명자 82·B-1 / 김순자 79·B-2 / 이정숙 85·A-7(미열).

## Hard Rules

- **이모지 절대 금지**: no emoji anywhere in UI (HTML/CSS/JS or docs rendered as UI). Icons must use
  `iconify-icon` (`fluent:*` family). Replace any emoji you encounter while editing a file.
- **Design tokens over raw hex**: use variables from `07_디자인/tokens/tokens.css`; avoid inline
  styles and direct hex values (enforced by `design_audit.py`).
- **Never push to `main`.** Always: new branch (`feat/...`, `fix/...`, `chore/...`) → commit →
  `git push -u origin <branch>` → `gh pr create`.
- `06_로그/대화기록_작업로그.md` is an append-only session log the user expects Claude to update on request.

## Directory Map

```
01_기획 … 06_로그               # planning, market research, design docs, research, decks, logs
07_디자인/                      # design system: tokens/tokens.css, system/ (shared CSS/JS,
                                #   interactions.js/css), scripts/ (audit tools), review-reports/
v11_보호자앱/                   # guardian app        (entry: g-guardian-live.html)
v11_요양보호사앱/               # caregiver app       (entry: c01-today.html)
v12_환자앱/                     # patient app         (entry: p01-today.html)
v15_의료진앱/                   # medical-staff app   (entry: d01-home.html)
v10_의료진웹/                   # medical-staff web   (entry: 의료진_대시보드_v9.5.html)
v13_온보딩/                     # onboarding          (entry: ob01-welcome.html)
haru-anbu-showcase-v8-bundle/   # public showcase site (ko + .en.html)
haru-anbu-making-of/            # SEPARATE nested git repo — Next.js 16.2.6, React 19, TS,
                                #   Tailwind 4, GSAP, Lenis; live at haru-anbu-making-of.vercel.app
중간고사기획서/                 # proposal deck (하루안부_기획서_v15.html + untracked EN version)
vercel.json / serve.py          # deployment rewrites / local no-cache server
```

Shared per-app CSS extracted by the 2026-07-12 cleanup lives in each app's `styles/` folder
(e.g. `v11_보호자앱/styles/`). Common toast/interaction code: `07_디자인/system/interactions.js|css`.

## Run

```bash
cd '/Users/yechanshon/Desktop/Haru Anbu'
python3 -m http.server 8000          # plain static server, or:
python3 serve.py                     # no-cache server on :8910 (avoids stale browser cache)
```

Making-of site (Node >= 20): `cd haru-anbu-making-of && npm install && npm run dev`
(also `npm run lint`, `npm run build`).

## Verify (run all after any prototype change)

```bash
python3 07_디자인/scripts/static_integrity.py                  # 66 active HTML: structure/refs/JS/CSS
python3 07_디자인/scripts/test_fixtures/test_runner.py         # audit regression tests (8)
python3 07_디자인/scripts/design_audit.py --target mobile-apps # token/emoji/icon/inline-style audit
python3 07_디자인/scripts/visual_check.py                      # static checks; --capture uses headless Chrome
```

All four passed as of 2026-07-13. Reports land in `07_디자인/review-reports/`.

## Deployment (Vercel, static)

`vercel.json` rewrites: `/` and `/ko` → `haru-anbu-showcase-v8-bundle/haru-anbu-showcase-v8.html`,
`/en` → the `.en.html` version, `/making_of` → proxied to the separate Next.js deployment.

## Related Working Copies (do not confuse) — full map in `_버전지도.md`

- **This repo** — the Codex structural-refactor line (styles/ extraction), branch
  `chore/cleanup-split-20260712`. The deployed line (haruanbu.site).

**Nested inside this repo folder** (NOT at `~/Desktop/` — earlier docs were wrong). All three are
gitignore-protected, so they never enter this repo's commits and survive `git clean`:

- `./Haru-Anbu-실험_피드백반영_20260710/` — independent git repo (branch `master`, last 2026-07-22),
  **the DESIGN-CANONICAL line** (mentor feedback 21건 + policy + data canon applied). Merging into
  this repo requires **porting, not file copy**. Local-only, not deployed/pushed. Read-only reference.
- `./HaruAnbu_싹통일전백업_20260625_1351/` — plain snapshot from before the 2026-06-25 icon/style
  unification. Reference/restore only.
- `./haru-anbu-making-of/` — separate Next.js repo (its own git + Vercel deploy).

Absent now: `하루안부v2` (only a stale `.gitignore` rule remains); the old Desktop review tools
(`하루안부-비교-런처.html` etc.) are no longer at `~/Desktop/`.

## Status as of 2026-07-13

- Branch `chore/cleanup-split-20260712` is **local-only** (no upstream, no PR). Latest commit
  `eb4b91b`: large cleanup — shared CSS extraction, toast commonization, 690 `type="button"` fixes.
- Uncommitted: 6 modified tracked files (`.vercelignore`, `vercel.json`, work log, showcase ko/en HTML,
  기획서 v15) + ~15 untracked items (portfolio-panels/, 전람회_표지/, EN deck, EN voice samples, work-instruction .md files).
- Nested `haru-anbu-making-of` repo: 14+ modified files + asset deletions uncommitted on `main` —
  deliberately left pending user review. Do NOT mix pre-existing user changes with cleanup changes in one commit.
- Detailed handoff: `CLAUDE_HANDOFF_CODE_CLEANUP_20260712.md` (read it before continuing cleanup work).

## Pending Work

1. Push branch + create PR for the cleanup work (after reviewing the split with the user).
2. Real-browser visual audit (handoff §4): capture 6 representative screens (the entry files listed
   in the map above) at the same mobile viewport via Playwright; compare header/card/tabbar/token
   consistency; then re-run all Verify commands.
3. Review + commit `haru-anbu-making-of` changes with the user (separate repo, separate commits).
4. Merge decision vs the design-canonical experiment repo — porting, not copying.
5. Figma migration pilot interrupted 2026-07-13 (see experiment repo `v11_보호자앱/_figma_handoff.md`):
   guardian home being recreated in Figma file `f8I9rALSAUEH9cEb7iEK0W`; header/greeting done, rest unfinished.
6. Queued tasks in `중간고사기획서/` untracked docs: `_굿디자인_출품_작성.md` (Good Design award entry),
   `_덱폴리시_작업지시.md`, `_앱영어화_작업지시.md` (app English localization).
7. `07_디자인/review-reports/component_divergence_*.md`: divergence candidates must NOT be bulk-unified —
   mix of intended role variants and true duplicates; review case-by-case with captures (handoff §5).
