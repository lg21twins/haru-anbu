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

> 전체 구성은 `_저장소지도.md`, 사본·백업 관계는 `_버전지도.md`.

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
중간고사기획서/                 # proposal deck (하루안부_기획서_v15.html + EN) + 원본 에셋 245MB
08_제안서/                      # 제안서 산출물 일체 — README.md가 진입점
                                #   PDF/(완성본 7종) 원고/(19) 시각화/(HTML) assets/
09_포트폴리오/                  # 패널·전람회 표지·인스타 출력·출품 가이드
_작업파일/                      # 미적용 수정 스크립트 2개(08_제안서 문서가 호출 — 지우지 말 것) · 메일 세팅 메모
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
python3 07_디자인/scripts/static_integrity.py                  # 72 active HTML: structure/refs/JS/CSS
python3 07_디자인/scripts/test_fixtures/test_runner.py         # audit regression tests (8)
python3 07_디자인/scripts/design_audit.py --target mobile-apps # token/emoji/icon/inline-style audit
python3 07_디자인/scripts/visual_check.py                      # static checks (6); --capture uses headless Chrome
python3 07_디자인/scripts/untracked_deps.py                    # assets referenced by live code but not in git
```

`static_integrity.py` also resolves `url()` inside `v*/styles/*.css` — the 2026-07-12 extraction moved
those sheets one directory deeper and silently broke three relative image paths.

`untracked_deps.py` (added 2026-08-09) answers a different question: the file exists locally, but is it
**in the repo**? On first run it found **40** — including `07_디자인/_iconify-bundle.js` (referenced by 18
files) and the entire showcase `img/opt/` set. Deploying that state would blank the hero, the gallery and
every icon on haruanbu.site while looking perfect locally. Nothing has been `git add`ed — that is the
user's call, since the assets are in-flight optimization work.

Reports land in `07_디자인/review-reports/`.

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

## Status as of 2026-11-15

- `main` = PR #9 (2026-09-03, 로컬 Pretendard 서브셋). 그 뒤 2026-07 의 `chore/cleanup-split-20260712` 계열은 PR #4~#9 로 전부 병합됐다 —
  예전 이 자리에 적혀 있던 "local-only, no PR" 는 더 이상 사실이 아니다.
- 현재 브랜치 `chore/opus55-refresh-20261115` (← `chore/deep-cleanup-20260925` ← `feat/presentation-tour-20260911`). **upstream 없음, 커밋 안 됨.**
  발표용 투어 커밋 `c3dc9ba` 는 main 에 **없다** → haruanbu.site 에는 아직 투어 개선이 나가지 않았다.
- 이 브랜치의 미커밋 작업(2026-11-15): 쇼케이스 ko·en 최적화/접근성/반응형 수정, 점검 스크립트 6종 + 측정 서버(`07_디자인/scripts/`:
  `showcase_perf.py` · `showcase_sections.py` · `responsive_sweep.py` · `showcase_a11y.py` · `occluded_text.py` · `dead_css.py` · `measure_server.py`), 쇼케이스 README 재작성,
  `03_설계/architecture.md` 모델 ID 갱신. 상세·재현법은 `_인수인계_20261115_opus55.md`.
  같은 날 전수 정리(6차): 루트 미사용 png 2개 · 병합된 슬라이드 조각 · `.playwright-mcp` · 패널 디버그 흔적을 치웠고, `발표/` 의 TTS 제작 페이지 5개는 `.vercelignore` 로 배포에서 뺐다(파일은 남음). **휴지통은 비워질 수 있다** — 미추적 파일은 지우기 전에 프로젝트 안 보관 폴더로 옮길 것.
- 같은 작업트리에 **다른 세션의 미커밋 수정**이 섞여 있다(01_기획 3개 · 02_시장조사 · 06_로그 · `_버전지도.md` · 기획서 v15 · `icon-set-v1.html` 삭제).
  커밋할 땐 파일을 이름으로 골라 올린다(`git add -A` 금지).
- 중첩 repo `haru-anbu-making-of` 는 별도 저장소 — 여기서 건드리지 않는다.
- 상세 정리 이력: `CLAUDE_HANDOFF_CODE_CLEANUP_20260712.md`.

## Claude 모델 표기 (2026-11-15 기준)

- 제품이 호출하는 모델의 ID 는 5.5 세대로 갱신했다: `claude-sonnet-5-5` · `claude-haiku-5-5`
  (`03_설계/architecture.md` 코드 예시, `scripts/review-loop.sh` 기본값, 화면명세서 v2.0).
- **일부러 안 바꾼 것**: ① 비용 절감률(90%·50%)·단가($3/$15 등)는 이전 세대 값이라 5.5 단가를 확인하기 전까지 인용하지 않는다
  (`03_설계/architecture.md` 6.3 에 확인필요 표시). ② 01_기획 통합기획서(v6.0 md·시각화·배포용)와 `04_리서치/하루안부_분석보고서.md` 는
  공개/제출용 문서라 수치와 같이 사람이 정한다. ③ "Claude Opus 4.7 작성" 같은 과거 작성자 서명은 기록이므로 그대로 둔다.

## Pending Work

1. 이 브랜치를 커밋 → push → PR (사용자 요청 시). 다른 세션의 미커밋 파일과 섞지 않는다.
2. 쇼케이스 남은 사용성: 폰에서 "자세히 알아보기" 텍스트 높이 21px(누르는 면적은 `::after` 로 44px 확보돼 있음), 가로 폰(844×390) 릴레이 양끝 베젤 8px.
   (Space·↓ 투어 가로채기는 2026-11-15 해결 — 투어가 꺼져 있을 땐 Enter 만 깨운다. 푸터는 `--brand-blue-600` 유지로 결정.)
3. `.claude/settings.local.json` 의 Stop 훅이 없는 경로(`shonz_vibe/care_platform/…`)에 쓴다 — 작업로그에 "세션 종료" 자동 기록 193개가 쌓여 있다. 정리 여부 사용자 확인.
4. Merge decision vs the design-canonical experiment repo — porting, not copying.
5. Figma migration: 38 screens done (file `f8I9rALSAUEH9cEb7iEK0W`, 폰트 Noto 대체 — Pretendard 는 재시작 필요). 상세는 프로젝트 메모리.
6. Queued tasks in `중간고사기획서/` untracked docs: `_굿디자인_출품_작성.md`, `_덱폴리시_작업지시.md`, `_앱영어화_작업지시.md`.
7. `07_디자인/review-reports/component_divergence_*.md`: divergence candidates must NOT be bulk-unified — review case-by-case with captures.
8. 01_기획·04_리서치 문서의 모델 표기와 비용 수치(위 "Claude 모델 표기" ②) — 5.5 단가 확인 후 사람이 결정.
