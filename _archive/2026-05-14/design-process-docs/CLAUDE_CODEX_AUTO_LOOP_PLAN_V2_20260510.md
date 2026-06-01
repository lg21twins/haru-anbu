# Claude + Codex 자동 리뷰 루프 v2 계획서

작성일: 2026-05-10
선행 문서:
- v1: `07_디자인/CLAUDE_CODEX_AUTO_LOOP_PLAN_20260510.md`
- Codex 리뷰: `07_디자인/CODEX_REVIEW_OF_AUTO_LOOP_PLAN_20260510.md`

이 문서는 v1을 대체한다. v1은 이력 보존용으로만 남기고, 실제 구현은 v2 기준으로 진행한다.

---

## 0. v1 → v2 핵심 변경점

Codex 리뷰의 지적을 반영해서 다음 5가지를 바꾼다.

| # | v1 | v2 |
|---|---|---|
| 1 | AI가 `LOG.md`에 직접 append | AI는 단계별 결과 파일(.md/.json)만 생성. 스크립트가 `LOG.md`로 병합 |
| 2 | LOG.md grep으로 verdict 판정 | `verdict.json` (스키마 강제)으로 판정. LOG.md는 사람용 |
| 3 | dirty working tree면 abort | 기본은 별도 git worktree에서 실행. dirty 허용 |
| 4 | max_rounds=2 기본 | max_rounds=1 기본. 명시적 옵션으로 2 가능 |
| 5 | REQUEST.md 본문에 범위 서술 | REQUEST.md에 `Allowed files` 섹션 필수. 스크립트가 기계 검증 |

추가 반영:
- PASS 판정 4단계화 (`PASS` / `PASS_WITH_NOTES` / `FAIL` / `ESCALATED`)
- Codex 리뷰 단계는 read-only 샌드박스 + stdout 리다이렉션
- `_GUIDE.md` 풀 가이드와 `_GUIDE_COMPACT.md` 호출용 압축 가이드 분리
- 각 루프 시작 시 `GUIDE_SNAPSHOT.md` 생성 (기준 동결)
- lock 파일로 동시 실행 차단
- 모델/effort 명시
- 한글/공백 경로 quoting 표준화
- static verify 옵션 추가

---

## 1. 사용자 관점

### 1-1. 기본 사용

```bash
./scripts/review-loop.sh tokens-only
```

`REQUEST.md` 가 에디터로 열리고, 사용자가 `Allowed files` + 요청 작성 후 닫으면 자동 진행. 5~15분 후 결과.

### 1-2. 인자/옵션

```bash
./scripts/review-loop.sh [OPTIONS] <name> [request-body]
```

| 옵션 | 기본 | 의미 |
|---|---|---|
| `--worktree` | on (기본) | 별도 git worktree에서 실행. dirty 허용 |
| `--no-worktree` | off | 현재 디렉터리에서 실행. clean 강제 |
| `--rounds N` | 1 | 최대 라운드 수 (1\|2) |
| `--verify MODE` | static | `none\|static\|browser` |
| `--budget USD` | 3 | Claude 호출 누적 예산 (`--max-budget-usd`) |
| `--dry-run` | off | 폴더만 만들고 AI 호출 안 함 |

### 1-3. 종료 출력

```txt
[review-loop] done.
[review-loop] result:    PASS_WITH_NOTES (round 1)
[review-loop] worktree:  /tmp/haru-anbu-loops/2026-05-10_tokens-only
[review-loop] log:       07_디자인/_review_loop/2026-05-10_tokens-only/LOG.md
[review-loop] diff:      07_디자인/_review_loop/2026-05-10_tokens-only/diff.patch
[review-loop] notes (2):
  - patient + caregiver 토큰 분리 권장 (다음 루프)
  - tokens.css 헤더 코멘트 갱신 권장
[review-loop] next:      review the diff in worktree, then merge into your branch
```

---

## 2. 폴더 구조

```txt
07_디자인/_review_loop/
├── _GUIDE.md                 # 사람용 풀 가이드 (선행 문서의 리뷰 기준 6개 항목)
├── _GUIDE_COMPACT.md         # AI 호출용 1~2페이지 압축 가이드
├── _TEMPLATE/
│   ├── REQUEST.md            # Allowed files / Request / Done criteria 빈 양식
│   └── meta.json             # 빈 양식
├── schemas/
│   └── codex-verdict.schema.json
└── 2026-05-10_tokens-only/
    ├── REQUEST.md
    ├── GUIDE_SNAPSHOT.md     # 시작 시점의 _GUIDE_COMPACT.md 복사본
    ├── meta.json
    ├── diff.patch            # baseline 기반 + allowed files 한정
    ├── LOG.md                # 스크립트가 round-N 산출물에서 합성
    ├── command.log           # 실행 명령/시간/exit code 기록
    ├── stdio/
    │   ├── claude-work-r1.stdout
    │   ├── claude-work-r1.stderr
    │   ├── codex-review-r1.stdout
    │   └── ...
    └── round-1/
        ├── claude-work.md
        ├── claude-work.json     # 변경 파일 목록 등 메타
        ├── codex-review.md
        ├── codex-review.json    # verdict
        ├── claude-response.md
        ├── claude-response.json
        ├── codex-final.md
        └── codex-final.json     # 최종 verdict
```

worktree 사용 시 실제 파일 수정은 worktree 안에서 일어나고, 위 `_review_loop/<loop>/` 산출물도 worktree의 동일 경로에 생긴다. 스크립트가 마지막에 산출물을 메인 워킹트리로 복사한다 (3-3 참조).

---

## 3. git worktree 운영

### 3-1. 왜 worktree

현재 repo는 dirty 상태가 잦다. v1의 "dirty면 abort"는 실사용을 막는다. 별도 worktree를 쓰면:
- 사용자 변경과 자동 루프 변경이 섞이지 않음
- baseline 잡기 쉬움 (worktree 시작점이 곧 baseline)
- 사고 시 worktree만 폐기하면 됨

### 3-2. worktree 생성

```bash
WORKTREE_ROOT="${HARU_LOOP_WORKTREE_ROOT:-/tmp/haru-anbu-loops}"
WORKTREE_DIR="$WORKTREE_ROOT/$LOOP_NAME"
BRANCH="loop/$LOOP_NAME"

mkdir -p "$WORKTREE_ROOT"
git worktree add -b "$BRANCH" "$WORKTREE_DIR" HEAD
```

`HEAD`에서 분기하므로 현재 브랜치의 마지막 커밋이 baseline. 사용자의 untracked/uncommitted 변경은 따라오지 않는다.

### 3-3. 산출물 복사

루프 종료 시:

```bash
mkdir -p "$MAIN_REPO/07_디자인/_review_loop/$LOOP_NAME"
rsync -a "$WORKTREE_DIR/07_디자인/_review_loop/$LOOP_NAME/" \
        "$MAIN_REPO/07_디자인/_review_loop/$LOOP_NAME/"
```

worktree는 보존 (사용자가 diff/머지 결정용으로 본다). 정리는 사용자가 명시적으로:

```bash
git worktree remove /tmp/haru-anbu-loops/2026-05-10_tokens-only
git branch -D loop/2026-05-10_tokens-only
```

스크립트는 worktree를 자동 삭제하지 않는다. 머지 전 삭제하면 변경분이 날아가기 때문.

### 3-4. `--no-worktree` 모드

```bash
./scripts/review-loop.sh --no-worktree tokens-only
```

`git status --porcelain` 결과가 비어있어야 시작. 더럽다면 abort. 빠른 디버깅용으로만 사용.

---

## 4. REQUEST.md 포맷

스크립트가 파싱하는 섹션이 있으므로 헤더 이름은 고정한다.

```md
# 작업 요청

## Allowed files

- 07_디자인/tokens/tokens.css

## Allowed-file globs (선택)

- 07_디자인/tokens/**

## Request

1. `--color-accent-rgb` 토큰을 `:root`와 각 role selector에 추가한다.
2. `[data-role="patient"][data-platform="mobile"]` 조합 규칙을 추가해 환자 접근성 토큰이 mobile 규칙에 덮이지 않게 한다.
3. primitive palette의 hex 값은 유지한다.

## Done criteria

- `02_COMPONENTS.md`의 `rgba(var(--color-accent-rgb), ...)` 예시가 실제 토큰과 맞는다.
- patient + mobile 조합에서 `--text-body: 18px`, `--size-touch-target: 56px`, `--size-button-default: 56px`가 유지된다.

## Notes (선택)

- primitive layer의 hex는 SoT다. 변경 금지.
```

파싱 규칙:
- `## Allowed files` 아래 `- ` 항목이 정확한 경로 allowlist.
- `## Allowed-file globs` 아래 항목은 glob 매칭 (예: `**/tokens/*.css`).
- 두 섹션 둘 다 비어 있으면 abort (`MISSING_ALLOWLIST`).
- `## Request` 비어 있으면 abort.
- `## Done criteria`는 권장이지만 비어 있어도 진행 (warning).

스크립트는 매 단계 후 `git diff --name-only`(worktree 기준)를 두 allowlist + `_review_loop/$LOOP_NAME/**` 와 비교. 위반 시 즉시 `FAIL_SCOPE_VIOLATION` 종료.

---

## 5. 단계별 산출물 파일

각 단계는 자기 폴더(`round-N/`)에 두 파일 생성:
- `<actor>-<step>.md` — 사람이 읽는 본문
- `<actor>-<step>.json` — 스크립트가 읽는 메타

### 5-1. claude-work.json

```json
{
  "actor": "claude",
  "step": "work",
  "round": 1,
  "started_at": "...",
  "ended_at": "...",
  "changed_files": ["07_디자인/tokens/tokens.css"],
  "intent_summary": "추가/수정한 의도 한 줄",
  "concerns": ["patient + mobile 충돌 가능성"],
  "review_focus": ["토큰 일관성", "환자 접근성"]
}
```

### 5-2. codex-review.json — verdict 스키마 (필수)

`schemas/codex-verdict.schema.json` 으로 강제.

```json
{
  "actor": "codex",
  "step": "review",
  "round": 1,
  "verdict": "FAIL",
  "must_fix": [
    {"file": "07_디자인/tokens/tokens.css", "line": 142, "issue": "glass-blur primitive 직접 사용"}
  ],
  "recommendations": [
    {"file": "07_디자인/tokens/tokens.css", "issue": "patient 스케일 분리 권장"}
  ],
  "kept_well": ["semantic token 분리 깔끔"],
  "files_inspected": ["07_디자인/tokens/tokens.css"],
  "scope_violations": []
}
```

verdict 값:
- `FAIL`: must_fix 비어있지 않음
- `PASS_WITH_NOTES`: must_fix 비고 recommendations 있음
- `PASS`: must_fix와 recommendations 모두 비음
- `ESCALATED`: 요청 자체가 불명확하거나 충돌 (사람 판단 요)

### 5-3. claude-response.json

```json
{
  "actor": "claude",
  "step": "response",
  "round": 1,
  "applied": [{"item_ref": "must_fix[0]", "note": "semantic token으로 분리"}],
  "skipped": [{"item_ref": "recommendations[0]", "reason": "이번 범위 밖, 다음 루프"}],
  "additional_changed_files": []
}
```

### 5-4. codex-final.json

```json
{
  "actor": "codex",
  "step": "final",
  "round": 1,
  "verdict": "PASS_WITH_NOTES",
  "remaining_issues": ["patient 스케일 (다음 루프 이월)"],
  "scope_violations": []
}
```

### 5-5. LOG.md 자동 생성

스크립트가 `round-*/` 의 `.md` 본문을 시간순으로 이어 붙여 `LOG.md`로 만든다. AI는 LOG.md를 절대 수정하지 않는다.

```md
---
loop: 2026-05-10_tokens-only
status: done
result: PASS_WITH_NOTES
rounds: 1
generated_by: review-loop.sh
---

# Loop log

## [Claude 2026-05-10 14:32:15] round 1 work
<round-1/claude-work.md 내용>

---

## [Codex 2026-05-10 14:55:02] round 1 review
<round-1/codex-review.md 내용>

...
```

---

## 6. 스크립트 동작

### 6-1. 의사코드

```bash
#!/usr/bin/env bash
# /opt/homebrew/bin/bash 권장 (macOS 기본 3.2 회피)
set -Eeuo pipefail
IFS=$'\n\t'

NAME="${1:?usage: review-loop.sh <name> [request-body]}"; shift || true
BODY="${1:-}"

LOOP_ROOT="07_디자인/_review_loop"
DATE=$(date +%Y-%m-%d)
LOOP_NAME=$(unique_dir_name "${DATE}_${NAME}")     # 충돌 시 _2, _3
LOCK="$LOOP_ROOT/.review-loop.lock"
ROUNDS="${ROUNDS:-1}"
VERIFY="${VERIFY:-static}"
BUDGET="${BUDGET:-3}"
USE_WT="${USE_WT:-1}"

acquire_lock_or_die "$LOCK"
trap 'release_lock "$LOCK"; finalize_on_signal' EXIT INT TERM

# --- 0. worktree ---
if [ "$USE_WT" = 1 ]; then
  WT_DIR="${HARU_LOOP_WORKTREE_ROOT:-/tmp/haru-anbu-loops}/$LOOP_NAME"
  git worktree add -b "loop/$LOOP_NAME" "$WT_DIR" HEAD
  WORKDIR="$WT_DIR"
else
  ensure_clean_tree
  WORKDIR="$PWD"
fi

cd "$WORKDIR"
LOOP_DIR="$LOOP_ROOT/$LOOP_NAME"
mkdir -p "$LOOP_DIR"/{stdio,round-1}
cp -r "$LOOP_ROOT/_TEMPLATE/." "$LOOP_DIR/"
cp "$LOOP_ROOT/_GUIDE_COMPACT.md" "$LOOP_DIR/GUIDE_SNAPSHOT.md"

write_request "$LOOP_DIR/REQUEST.md" "$BODY"     # 인자 없으면 $EDITOR
parse_allowlist "$LOOP_DIR/REQUEST.md"           # ALLOWED_FILES 배열 채움
[ ${#ALLOWED_FILES[@]} -gt 0 ] || die MISSING_ALLOWLIST

BASELINE_REF=$(git rev-parse HEAD)
init_meta_json

# --- 1..N rounds ---
for round in $(seq 1 "$ROUNDS"); do
  RD="$LOOP_DIR/round-$round"
  mkdir -p "$RD"

  # 1) Claude work
  set_meta status=claude-work round="$round"
  call_claude_work "$round" "$RD" \
    > "$LOOP_DIR/stdio/claude-work-r$round.stdout" \
    2> "$LOOP_DIR/stdio/claude-work-r$round.stderr"
  enforce_scope "$BASELINE_REF" "${ALLOWED_FILES[@]}" "$LOOP_DIR/**"
  refresh_diff_patch "$BASELINE_REF" "${ALLOWED_FILES[@]}"

  # 2) Codex review (read-only)
  set_meta status=codex-review
  call_codex_review "$round" "$RD" \
    > "$RD/codex-review.md" \
    2> "$LOOP_DIR/stdio/codex-review-r$round.stderr"
  validate_json "$RD/codex-review.json" schemas/codex-verdict.schema.json
  V=$(jq -r .verdict "$RD/codex-review.json")
  [[ "$V" =~ ^(PASS|PASS_WITH_NOTES|FAIL|ESCALATED)$ ]] || die BAD_VERDICT

  if [ "$V" = "PASS" ] || [ "$V" = "PASS_WITH_NOTES" ]; then
    finalize "$V"
  fi
  if [ "$V" = "ESCALATED" ]; then
    finalize ESCALATED
  fi

  # 3) Claude respond
  set_meta status=claude-response
  call_claude_respond "$round" "$RD" \
    > "$LOOP_DIR/stdio/claude-respond-r$round.stdout" \
    2> "$LOOP_DIR/stdio/claude-respond-r$round.stderr"
  enforce_scope "$BASELINE_REF" "${ALLOWED_FILES[@]}" "$LOOP_DIR/**"
  refresh_diff_patch "$BASELINE_REF" "${ALLOWED_FILES[@]}"

  # 4) Codex final QA (read-only)
  set_meta status=codex-final
  call_codex_final "$round" "$RD" \
    > "$RD/codex-final.md" \
    2> "$LOOP_DIR/stdio/codex-final-r$round.stderr"
  validate_json "$RD/codex-final.json" schemas/codex-verdict.schema.json
  VF=$(jq -r .verdict "$RD/codex-final.json")

  if [ "$VF" = "PASS" ] || [ "$VF" = "PASS_WITH_NOTES" ]; then
    finalize "$VF"
  fi
  if [ "$VF" = "ESCALATED" ] || [ "$round" = "$ROUNDS" ]; then
    finalize ESCALATED
  fi
  # 다음 라운드로
done
```

### 6-2. enforce_scope

```bash
enforce_scope() {
  local base=$1; shift
  local allow=("$@")
  local violators=()
  while IFS= read -rd '' f; do
    if ! is_allowed "$f" "${allow[@]}"; then
      violators+=("$f")
    fi
  done < <(git diff --name-only -z "$base"...HEAD --)
  # untracked도 체크
  while IFS= read -rd '' f; do
    is_allowed "$f" "${allow[@]}" || violators+=("$f")
  done < <(git ls-files --others --exclude-standard -z)

  if (( ${#violators[@]} > 0 )); then
    set_meta status=done result=FAIL_SCOPE_VIOLATION
    printf 'scope violation: %s\n' "${violators[@]}" >&2
    exit 3
  fi
}
```

`is_allowed` 는 정확한 경로 일치 또는 glob 매칭. `_review_loop/$LOOP_NAME/**` 는 항상 허용 (산출물 경로).

### 6-3. refresh_diff_patch

```bash
refresh_diff_patch() {
  local base=$1; shift
  local files=("$@")
  git add -N -- "${files[@]}" 2>/dev/null || true
  git diff "$base" -- "${files[@]}" > "$LOOP_DIR/diff.patch"
}
```

baseline 이후 allowed files만의 변경. dirty 상태와 무관.

### 6-4. finalize

```bash
finalize() {
  local result=$1
  set_meta status=done result="$result"
  build_log_md_from_rounds                      # round-*/.md 합성
  copy_artifacts_to_main_repo_if_worktree
  print_summary
  exit "$(exit_code_for "$result")"             # PASS=0 PASS_WITH_NOTES=0 FAIL=2 ESCALATED=2 SCOPE_VIOLATION=3
}
```

스크립트는 절대 `git commit` 안 함. worktree도 자동 제거 안 함. 사용자가 워크트리에서 diff 확인 후 직접 머지.

---

## 7. CLI 호출 (Codex 리뷰로 확정)

### 7-1. Claude work / respond (수정 권한 필요)

```bash
claude -p \
  --permission-mode acceptEdits \
  --max-budget-usd "$BUDGET" \
  --output-format text \
  "$(render_prompt claude_work)"
```

`--permission-mode acceptEdits` 가 실제 환경에서 유효한 모드인지 첫 dry-run으로 검증 필요. 실패 시 fallback으로 `--dangerously-skip-permissions` 는 **사용 안 함**. 대신 사용자에게 모드 직접 지정하도록 에러 안내.

### 7-2. Codex review / final (read-only)

read-only + stdout 리다이렉션이 가장 안전 (Codex 리뷰가 권한 모델 강조).

```bash
codex exec \
  -C "$WORKDIR" \
  -s read-only \
  -a never \
  --ephemeral \
  "$(render_prompt codex_review)" \
  > "$RD/codex-review.md" \
  2> "$LOOP_DIR/stdio/codex-review-r$round.stderr"
```

verdict JSON은 별도 호출 또는 같은 호출에서 끝부분 fenced JSON 블록으로 받아 `jq` 로 분리 파싱. 후자는 약하므로 두 호출로 분리:

```bash
codex exec ... > "$RD/codex-review.md"           # 사람 읽기용
codex exec ... \
  --output-schema "$ROOT/schemas/codex-verdict.schema.json" \
  -o "$RD/codex-review.json" \
  ...                                            # 기계 판정용
```

`--output-schema` 가 실제 옵션인지 환경별 차이 있을 수 있으므로 첫 dry-run으로 확정.  미지원 시 차선:

```bash
# 단일 호출, 끝에 ```json 블록 강제
codex exec ... > "$RD/codex-review.md"
extract_last_json_block "$RD/codex-review.md" > "$RD/codex-review.json"
validate_json "$RD/codex-review.json" "$ROOT/schemas/codex-verdict.schema.json" \
  || die BAD_VERDICT
```

### 7-3. 모델/effort 명시

스크립트 상단 상수:

```bash
CLAUDE_MODEL="${CLAUDE_MODEL:-claude-sonnet-4-6}"
CODEX_MODEL="${CODEX_MODEL:-gpt-5}"        # 환경에 따라 조정
CODEX_EFFORT="${CODEX_EFFORT:-medium}"
```

`meta.json`에 기록.

---

## 8. AI 프롬프트 (수정판)

공통 헤더로 들어가는 텍스트는 호출 시점에 `_GUIDE_COMPACT.md` + `REQUEST.md` + 직전 단계 산출물만. 풀 가이드는 안 넣는다.

### 8-1. Claude work

```txt
[role]
You are Claude, the implementation role in the Haru Anbu auto-review loop.

[context files]
- {LOOP_DIR}/GUIDE_SNAPSHOT.md
- {LOOP_DIR}/REQUEST.md

[rules]
- Modify ONLY files listed in REQUEST.md "Allowed files" (or matching its globs).
- 이모지 금지. 아이콘은 iconify fluent filled 계열만.
- Do NOT modify _review_loop/** except your own outputs at {RD}/.
- Do NOT commit, do NOT push, do NOT touch git config.

[task]
1. Implement the request.
2. Write {RD}/claude-work.md describing 변경 파일 / 의도 / 걱정되는 부분 / Codex 리뷰 포인트.
3. Write {RD}/claude-work.json matching this shape:
   {actor:"claude", step:"work", round:{R}, started_at, ended_at, changed_files, intent_summary, concerns, review_focus}
4. Stop. Do not write LOG.md. Do not write meta.json.
```

### 8-2. Codex review (read-only)

```txt
[role]
You are Codex, the review role. Read-only mode. You cannot write files.

[context files]
- {LOOP_DIR}/GUIDE_SNAPSHOT.md
- {LOOP_DIR}/REQUEST.md
- {LOOP_DIR}/diff.patch
- {RD}/claude-work.md
- {RD}/claude-work.json
- the actual files listed in claude-work.json.changed_files

[criteria]
Apply 6 lenses from GUIDE_SNAPSHOT: 토큰 일관성 / 역할 테마 / UX/UI / glass / 접근성 / 아이콘·문서.

[output]
Print review markdown to stdout. End with:

```json
{ "actor":"codex", "step":"review", "round":{R},
  "verdict":"PASS|PASS_WITH_NOTES|FAIL|ESCALATED",
  "must_fix":[{"file":"...","line":0,"issue":"..."}],
  "recommendations":[{"file":"...","issue":"..."}],
  "kept_well":["..."],
  "files_inspected":["..."],
  "scope_violations":[] }
```

verdict rule:
- FAIL if must_fix non-empty
- PASS_WITH_NOTES if must_fix empty and recommendations non-empty
- PASS if both empty
- ESCALATED if request is ambiguous, conflicts with rules, or requires human design judgment

Constraint: do not modify any file.
```

### 8-3. Claude respond

```txt
[role]
You are Claude. Apply Codex review.

[context]
- {LOOP_DIR}/REQUEST.md, GUIDE_SNAPSHOT.md
- {RD}/codex-review.md, codex-review.json (must_fix items)

[task]
- Apply ALL must_fix items.
- Apply recommendations only if compatible with REQUEST scope. Document skipped ones.
- Stay within Allowed files.
- Write {RD}/claude-response.md and {RD}/claude-response.json
  ({actor, step:"response", round, applied, skipped, additional_changed_files}).
- Do not commit. Do not write LOG.md.
```

### 8-4. Codex final (read-only)

```txt
[role]
You are Codex final QA. Read-only.

[context]
- updated diff.patch and current source files
- {RD}/codex-review.md (your previous review)
- {RD}/claude-response.md, claude-response.json
- {LOOP_DIR}/REQUEST.md "Done criteria"

[task]
- Verify must_fix items are addressed.
- Verify Done criteria are met.
- Verify scope was respected.

[output]
Markdown summary, then JSON:
```json
{"actor":"codex","step":"final","round":{R},
 "verdict":"PASS|PASS_WITH_NOTES|FAIL|ESCALATED",
 "remaining_issues":["..."],
 "scope_violations":[]}
```
```

---

## 9. 안전장치 (확장)

| 항목 | 구현 |
|---|---|
| git commit/push 금지 | 스크립트 미호출. 프롬프트에 명시 |
| working tree 격리 | 기본 worktree |
| baseline 기준 diff | `git diff $BASELINE_REF -- "${ALLOWED_FILES[@]}"` |
| scope allowlist 강제 | enforce_scope (단계마다) |
| 금지 파일 | `.env*`, `secrets/**`, `package*.json`, `*lock*` 는 allowlist 무관하게 차단 |
| LOG.md/meta.json 무결성 | AI 미수정. 스크립트 단독 작성 |
| verdict 스키마 검증 | `ajv` 또는 `python -c jsonschema` |
| max_rounds | 기본 1, 최대 2 |
| timeout | 단계별 600s |
| 비용 한도 | Claude `--max-budget-usd`. 환경변수 `BUDGET` |
| lock 파일 | `flock` 또는 디렉터리 lock으로 중복 실행 차단 |
| GUIDE 동결 | 시작 시 `GUIDE_SNAPSHOT.md` 생성 |
| 한글/공백 경로 | 모든 변수 quote, `-z` 와 `-print0` 일관 사용 |
| stdout/stderr 보존 | `stdio/` 폴더에 단계별 저장 |
| static verify | 기본 on. ripgrep 기반 (이모지·required token·금지 패턴) |
| 신호 처리 | EXIT/INT/TERM trap 으로 lock 해제 + meta 기록 |
| 사람 승인 지점 | finalize는 PASS여도 절대 머지 안 함. "ready for human review" 출력 |

### 9-1. static verify 검사

`--verify static` 시 finalize 직전 실행. 실패 시 verdict 강등 + `verify` 필드에 기록.

```bash
# 이모지
rg --pcre2 '[\x{1F300}-\x{1FAFF}\x{2600}-\x{27BF}]' -- "${ALLOWED_FILES[@]}" \
  && fail "emoji found"

# 필수 토큰 (REQUEST.md done criteria에서 추출하거나 RC 파일에서 읽음)
for token in "${REQUIRED_TOKENS[@]}"; do
  rg -q "$token" 07_디자인/tokens/tokens.css || fail "missing $token"
done
```

### 9-2. browser verify (선택)

`--verify browser` 는 v2 범위 밖. v3에서 Playwright 또는 `osascript`로 preview 띄우고 screenshot diff. 지금은 placeholder.

---

## 10. meta.json (확장)

```json
{
  "loop": "2026-05-10_tokens-only",
  "status": "done",
  "round": 1,
  "max_rounds": 1,
  "result": "PASS_WITH_NOTES",
  "started_at": "2026-05-10T14:32:00+09:00",
  "ended_at":   "2026-05-10T15:21:30+09:00",
  "baseline_ref": "abc1234",
  "worktree": "/tmp/haru-anbu-loops/2026-05-10_tokens-only",
  "branch": "loop/2026-05-10_tokens-only",
  "models": {"claude": "claude-sonnet-4-6", "codex": "gpt-5", "codex_effort": "medium"},
  "budget_usd": 3.0,
  "verify": {"mode": "static", "passed": true, "checks": ["emoji", "required-tokens"]},
  "history": [
    {"step":"claude-work",    "round":1, "duration_s":423, "exit":0},
    {"step":"codex-review",   "round":1, "duration_s":187, "exit":0, "verdict":"FAIL"},
    {"step":"claude-respond", "round":1, "duration_s":312, "exit":0},
    {"step":"codex-final",    "round":1, "duration_s":141, "exit":0, "verdict":"PASS_WITH_NOTES"}
  ]
}
```

---

## 11. 의존성

| 항목 | 비고 |
|---|---|
| `bash` 4+ | `/opt/homebrew/bin/bash`. 첫 줄 shebang에 명시 |
| `git` 2.5+ | worktree 지원 |
| `jq` | meta/JSON 조작 |
| `ajv` 또는 `python3 + jsonschema` | verdict 스키마 검증 |
| `rg` | static verify |
| `claude` CLI | `-p`, `--permission-mode`, `--max-budget-usd` |
| `codex` CLI | `exec`, `-s read-only/workspace-write`, `-a never`, `-C`, `--ephemeral` |
| `flock` | lock (macOS는 `mkdir` 디렉터리 lock으로 대체 가능) |

스크립트 시작 시 `command -v` 로 모두 점검.

---

## 12. 첫 루프 (Codex 추천 그대로)

```bash
./scripts/review-loop.sh tokens-only
```

`REQUEST.md`:

```md
# 작업 요청

## Allowed files

- 07_디자인/tokens/tokens.css

## Request

1. `--color-accent-rgb` 토큰을 `:root`와 각 role selector에 추가한다.
2. `[data-role="patient"][data-platform="mobile"]` 조합 규칙을 추가해 환자 접근성 토큰이 mobile 규칙에 덮이지 않게 한다.
3. primitive palette의 hex 값은 유지한다.
4. 다른 파일은 수정하지 않는다.

## Done criteria

- `02_COMPONENTS.md` 의 `rgba(var(--color-accent-rgb), ...)` 예시가 실제 토큰과 맞는다.
- patient + mobile 조합에서 `--text-body: 18px`, `--size-touch-target: 56px`, `--size-button-default: 56px` 가 유지된다.
```

기대:
- worktree `/tmp/haru-anbu-loops/2026-05-10_tokens-only` 생성
- `loop/2026-05-10_tokens-only` 브랜치
- diff.patch 는 tokens.css 단일 파일
- max_rounds=1, 결과 PASS 또는 PASS_WITH_NOTES

이게 깔끔히 돌면 다음 후보:
1. `preview-roles` (preview-roles.html 통일성)
2. `glass-policy` (glass 사용 범위 정리)
3. `patient-a11y` (환자앱 접근성 audit)

---

## 13. v2에서도 의도적으로 빼는 것

- `--resume` (중단 시 새 루프로 시작)
- 자동 archive 이동
- 루프 동시 실행 (lock으로 차단)
- 무한 핑퐁 휴리스틱 (max_rounds로 충분)
- Slack/이메일 알림 (`osascript` 데스크톱 알림은 v2.1 후보)
- 자동 PR 생성/머지 (사람이 직접)
- `--verify browser` (v3 후보)
- 비용 동적 산정 (지금은 상한선만)

---

## 14. 구현 전 검증 체크리스트

스크립트 작성 전, 작은 dry-run 한 번으로 다음을 확정한다.

- [ ] `claude -p --permission-mode acceptEdits --max-budget-usd 3 "echo hi"` 정상 동작
- [ ] `codex exec -C "$REPO" -s read-only -a never --ephemeral "echo hi"` stdout 정상
- [ ] `codex exec --output-schema ...` 또는 fenced JSON 추출 중 어느 쪽이 안정적인지
- [ ] worktree 생성/제거 한글 경로에서 문제 없음
- [ ] `_GUIDE_COMPACT.md` 1~2페이지로 압축 가능 (`_GUIDE.md`에서 핵심 추출)
- [ ] `verdict.schema.json` 작성 + ajv/jsonschema 검증 동작
- [ ] static verify 명령들이 macOS의 `rg`에서 정상 (특히 PCRE 이모지 패턴)

이 7개가 OK면 v2 구현 진행.

---

## 15. v1 대비 반영 추적

Codex 리뷰의 어느 항목이 v2 어디로 갔는지.

| Codex 리뷰 섹션 | v2 반영 위치 |
|---|---|
| 1. AI가 LOG.md 직접 append 취약 | 5절 (단계별 산출물), 5-5 (LOG.md 자동 생성) |
| 2. clean working tree 비현실적 | 3절 (worktree 기본) |
| 3. 작업 범위 프롬프트 의존 | 4절 (Allowed files 섹션 강제), 6-2 (enforce_scope) |
| 4. diff.patch 모호 | 6-3 (baseline + allowlist 한정) |
| 5. PASS 판정 단순 | 5-2 (verdict 4단계) |
| 6. Claude CLI 권한 | 7-1 (`--permission-mode acceptEdits`) |
| 7. Codex review 명령 | 7-2 (read-only + stdout) |
| 8. 비용 제한 | 7-1 (`--max-budget-usd`), 1-2 옵션 |
| 9. 검증 단계 부재 | 9-1 (static verify) |
| 10. 한글/공백 경로 | 9절 표, 6절 의사코드 |
| 모델 역할 고정 | 7-3, 10절 meta |
| 동시 실행 lock | 9절 표 |
| GUIDE 버전 동결 | 2절 GUIDE_SNAPSHOT |
| 사람 승인 | 6-4 finalize (commit 안 함) |
| 사용자 변경 보호 | 3절 worktree |
| _GUIDE 압축 | 2절 _GUIDE_COMPACT 분리 |
| 첫 루프 좁히기 | 12절 (Codex 추천 그대로) |
| Codex 리뷰 출력 분리 | 7-2 (stdout 또는 -o) |
| `--output-schema` | 7-2, 14절 (검증 후 확정) |

---

## 16. 결론과 다음 액션

v2는 v1의 "풀 자동" 야망을 한 단계 낮추고, 통제된 자동화로 조정했다.
- 사용자 명령은 여전히 한 줄
- 위험은 worktree로 격리
- 판정은 JSON으로 결정론적
- 첫 루프는 작게 (1 라운드, 1 파일, 명시적 Done criteria)

다음 액션 (사용자 결정 필요):
1. 14절 검증 체크리스트 7개를 dry-run으로 확인 — 이 단계만 사용자 시간 10~20분 필요
2. OK면 `_GUIDE_COMPACT.md` + `_TEMPLATE/` + `schemas/codex-verdict.schema.json` 작성
3. 그 다음 `scripts/review-loop.sh` 작성
4. 첫 루프 `tokens-only` 실행

원하시면 1번부터 진행하겠다. 14절 dry-run 명령을 직접 한 번에 돌리고 결과를 보고하면, 그 결과 기준으로 7-2의 어느 분기로 갈지 확정한다.
