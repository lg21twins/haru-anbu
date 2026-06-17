# Codex Review of Claude + Codex Auto Loop Plan

검토 대상: `07_디자인/CLAUDE_CODEX_AUTO_LOOP_PLAN_20260510.md`

작성일: 2026-05-10

## 총평

A안은 방향 자체는 가능하다. `claude -p`와 `codex exec` 모두 현재 로컬 환경에 존재하고, non-interactive 실행도 지원한다. 따라서 "요청 작성 -> Claude 작업 -> Codex 리뷰 -> Claude 반영 -> Codex 최종 QA"를 한 줄 명령으로 묶는 것은 기술적으로 가능하다.

다만 현재 설계 그대로 바로 구현하기에는 위험한 지점이 있다. 가장 큰 문제는 다음 세 가지다.

1. AI가 같은 `LOG.md`에 직접 append하도록 하는 구조
2. `LOG.md` 텍스트 grep으로 상태와 verdict를 판단하는 구조
3. 현재 repo처럼 dirty working tree가 큰 프로젝트에서는 "작업 전 clean abort" 정책 때문에 루프가 거의 항상 시작되지 않을 수 있다는 점

권장 방향은 "풀 자동 수정"보다 먼저 "통제된 반자동 루프"로 시작하는 것이다. Claude와 Codex를 호출하되, 각 AI는 구조화된 결과 파일을 만들고, 스크립트가 검증한 뒤 `LOG.md`에 병합하는 구조가 더 안전하다.

## 13번 열린 질문 답변

### 1. Codex CLI 헤드리스 명령

현재 환경 기준으로 `codex exec`가 맞다.

확인 결과:

```bash
codex exec [OPTIONS] [PROMPT]
```

쓸 수 있는 주요 옵션:

```bash
codex exec -C "/Users/yechanshon/Desktop/Haru Anbu" -s workspace-write -a never "..."
```

또는 stdin으로 프롬프트를 넘길 수 있다.

```bash
codex exec -C "$REPO" -s workspace-write -a never - < prompt.txt
```

JSONL 이벤트 출력도 가능하다.

```bash
codex exec --json ...
```

마지막 응답만 파일로 저장하는 옵션도 있다.

```bash
codex exec -o "$LOOP_DIR/codex-review.md" ...
```

권장:

- 리뷰만 하는 단계라도 `LOG.md`를 쓰게 하려면 `read-only`가 아니라 `workspace-write`가 필요하다.
- 하지만 Codex에게 직접 `LOG.md`를 append시키기보다 `-o "$LOOP_DIR/codex-review-round-1.md"`로 마지막 응답을 저장하고, 스크립트가 `LOG.md`에 붙이는 편이 안전하다.

### 2. Codex가 파일 쓰기 가능한가

가능하다. 단, sandbox 설정에 따라 다르다.

- `-s read-only`: 파일 쓰기 불가
- `-s workspace-write`: repo 안 파일 쓰기 가능
- `-s danger-full-access`: 더 넓은 쓰기 가능하지만 자동 루프에는 비추천

자동 루프에서는 `workspace-write` + `-a never` 조합이 현실적이다. 다만 Codex 리뷰 단계는 원칙적으로 소스 파일을 수정하면 안 되므로, 쓰기 범위를 `LOG.md` 또는 결과 파일로 제한하는 프롬프트만으로는 부족하다.

권장 안전장치:

- Codex 호출 전후 `git diff --name-only`를 비교한다.
- Codex 단계 이후 변경 파일이 `LOG.md` 또는 `codex-*.md` 외에 있으면 즉시 FAIL 처리한다.
- 더 안전하게는 Codex에 `-o`로 마지막 메시지만 저장하게 하고, Codex가 직접 파일 쓰기를 하지 않게 한다.

### 3. 무한 루프 휴리스틱

v1에서는 중복도 휴리스틱이 필요 없다. `max_rounds=2`면 충분하다.

이유:

- 리뷰 중복도 90% 같은 휴리스틱은 구현 대비 신뢰도가 낮다.
- 자연어 리뷰는 같은 문제를 다른 표현으로 말할 수 있고, 반대로 다른 문제도 비슷하게 보일 수 있다.
- 자동 판단이 틀리면 더 위험하다.

권장:

- v1은 무조건 `max_rounds=1` 또는 `max_rounds=2`로 제한
- round 2에서도 FAIL이면 `ESCALATED`
- 중복 휴리스틱은 v2 이후에나 고려

개인적으로 첫 버전은 `max_rounds=1`을 기본값으로 추천한다. 자동 반영까지 허용하는 경우 2라운드는 생각보다 많은 변경을 만들 수 있다.

### 4. VERDICT 파싱

`LOG.md`를 grep으로 파싱하는 것은 불안정하다.

문제:

- AI가 예시로 `VERDICT: PASS`를 문장 안에 써도 grep에 걸릴 수 있다.
- 이전 라운드의 verdict와 최신 verdict를 구분해야 한다.
- `PASS-NO-CHANGES`와 `PASS`가 섞이면 파싱 규칙이 복잡해진다.
- LOG는 사람이 읽는 문서이고, 상태 판단은 기계가 읽어야 하므로 역할이 다르다.

권장:

- AI가 `verdict.json` 또는 단계별 `codex-review.round1.json`을 생성하게 한다.
- 더 안전한 방식은 Codex의 마지막 응답을 `--output-schema`로 제한하는 것이다.
- 최소한 verdict는 별도 파일로 분리한다.

예시:

```json
{
  "actor": "codex",
  "step": "final",
  "round": 1,
  "verdict": "PASS",
  "must_fix_count": 0,
  "recommendation_count": 2,
  "changed_files_allowed": true
}
```

`LOG.md`는 사람이 보는 기록으로만 쓰고, 스크립트 판정은 JSON만 보게 하는 것이 좋다.

### 5. 첫 작업 범위

`tokens-only`는 적절하지만, 요청 내용은 더 작게 쪼개는 것이 좋다.

현재 제안:

> tokens.css의 hex 하드코딩을 semantic token으로 정리. --color-accent-rgb 추가.

위 요청 중 "hex 하드코딩 정리"는 범위가 애매하다. 토큰 파일의 primitive layer에는 hex가 있는 것이 정상이다. 따라서 AI가 primitive palette까지 잘못 정리할 위험이 있다.

첫 루프 추천:

```txt
tokens.css에 --color-accent-rgb를 추가하고, role별 값을 연결한다.
patient + mobile 토큰 우선순위 충돌을 수정한다.
다른 파일은 수정하지 않는다.
primitive palette의 hex 값은 유지한다.
```

첫 루프는 1개 파일, 2개 변경만 하는 것이 좋다.

### 6. 빠진 안전장치

추가해야 할 안전장치가 꽤 있다.

필수 추가:

- 루프 시작 전 `git diff --name-only` baseline 저장
- 각 AI 단계 후 변경 파일 allowlist 검사
- Codex review 단계에서는 소스 파일 변경 금지 검사
- Claude 단계에서도 REQUEST에 명시된 파일 외 변경 금지 검사
- `diff.patch`는 전체 repo diff가 아니라 baseline 이후 diff로 저장
- `LOG.md`, `meta.json`, 결과 파일은 작업 diff와 분리해서 관리
- 스크립트 자신의 생성물 때문에 working tree dirty 검사가 실패하지 않도록 예외 처리
- 명령 실행 로그와 모델 stdout/stderr를 별도 파일로 저장
- 실패 시 자동 restore를 할지, 보존만 할지 정책 명시
- symlink 경로와 한글 경로 처리 검증
- `set -euo pipefail` 환경에서 `grep` no-match, `jq` 실패 처리를 명확히
- 네트워크/API 실패와 모델 rate limit 실패 구분

강력 추천:

- 자동 루프는 별도 git worktree에서 실행
- 또는 최소한 루프 시작 시 임시 branch를 만들고 그 안에서 실행

현재 repo는 이미 working tree가 매우 dirty하다. 따라서 "dirty면 abort" 정책을 그대로 쓰면 지금 환경에서는 루프가 시작되지 않는다. 이 프로젝트에서는 별도 worktree 기반이 훨씬 현실적이다.

### 7. `_GUIDE.md` 분량

풀 가이드를 매번 읽히는 것은 비용과 흔들림 면에서 비효율적이다.

권장:

- `_GUIDE.md`: 사람이 읽는 전체 규칙
- `_GUIDE_COMPACT.md`: 매 호출에 넣는 1~2페이지 핵심 규칙
- 작업별 추가 context는 REQUEST에 명시

즉, 매 호출은 compact guide를 기본으로 읽고, 필요한 경우만 full guide를 참조하게 하는 것이 좋다.

특히 자동 루프에서는 토큰 비용보다 "지시가 길어져 모델이 핵심을 놓치는 것"이 더 문제다. 핵심 규칙은 짧고 반복 가능해야 한다.

### 8. Codex 입장에서 프롬프트가 쓸 만한가

6-2, 6-4의 방향은 좋지만 그대로 쓰기엔 몇 가지 보완이 필요하다.

문제:

- "Do NOT modify any source file. Only append to LOG.md"는 Codex가 파일을 쓰게 하므로 sandbox가 `workspace-write`여야 한다.
- 이 경우 실수로 소스 파일을 건드릴 수 있다.
- `diff.patch`만 보면 실제 파일 상태와 어긋날 수 있다. 최종 QA는 실제 파일도 읽어야 한다.
- "반드시 수정이 비었고 개선 권장도 비면 PASS"는 너무 엄격하다. 개선 권장이 있어도 PASS일 수 있다.

권장 프롬프트 수정:

- Codex는 소스 파일을 수정하지 않는다.
- Codex는 리뷰 결과를 최종 응답으로만 출력한다.
- 스크립트가 `-o`로 결과를 저장하고 LOG에 병합한다.
- verdict는 `PASS | PASS_WITH_NOTES | FAIL | ESCALATED`로 나눈다.

추천 verdict:

- `PASS`: 반드시 수정 없음, 남은 권장사항도 범위 밖이거나 사소함
- `PASS_WITH_NOTES`: 반드시 수정 없음, 개선 권장 있음
- `FAIL`: 반드시 수정 있음
- `ESCALATED`: 사람 판단 필요

## 반드시 수정해야 할 설계 리스크

### 1. LOG.md append-only 직접 쓰기 구조는 취약함

Claude와 Codex가 같은 파일을 직접 append하면 아래 문제가 생긴다.

- frontmatter를 실수로 수정할 수 있음
- 헤더 포맷이 조금만 달라도 파싱 실패
- 동시에 실행되거나 중단되면 파일이 깨질 수 있음
- 리뷰 단계에서 Codex가 소스 파일을 건드릴 권한까지 필요해짐

권장 구조:

```txt
round-1/
├── claude-work.md
├── claude-work.json
├── codex-review.md
├── codex-review.json
├── claude-response.md
├── claude-response.json
├── codex-final.md
└── codex-final.json
```

그리고 스크립트가 이 파일들을 모아 `LOG.md`를 생성하거나 append한다.

### 2. clean working tree 요구는 현재 프로젝트와 맞지 않음

계획서에는 dirty working tree면 abort라고 되어 있다. 원칙적으로는 안전하지만, 현재 repo는 이미 많은 변경과 untracked 파일이 있다. 이 정책이면 루프가 실사용되지 못할 가능성이 높다.

대안:

1. 별도 git worktree를 만들어 거기서 실행
2. 시작 시 baseline diff를 저장하고, REQUEST allowlist 파일만 변경 허용
3. dirty tree 허용 모드와 clean-only 모드를 나눔

가장 추천:

```bash
./scripts/review-loop.sh --worktree tokens-only "..."
```

이 옵션이 새 worktree/branch를 만들고 자동 루프는 그 안에서만 실행되게 한다.

### 3. 작업 범위 제한을 프롬프트에만 맡기면 안 됨

"REQUEST.md에 명시된 파일 외엔 수정 금지"는 프롬프트만으로는 부족하다.

스크립트가 기계적으로 검사해야 한다.

예시:

```txt
REQUEST.md에 allowed_files 섹션을 둔다.
각 단계 후 git diff --name-only를 allowed_files와 비교한다.
위반 시 FAIL_SCOPE_VIOLATION.
```

권장 REQUEST 포맷:

```md
## Allowed files
- 07_디자인/tokens/tokens.css

## Request
...
```

### 4. diff.patch 관리 방식이 불명확함

계획서의 `save_diff_to "$LOOP_DIR/diff.patch"`는 전체 repo diff를 저장할 가능성이 있다. 현재 repo처럼 이미 dirty한 상태에서는 자동 루프와 무관한 변경까지 diff.patch에 섞인다.

권장:

- 루프 시작 시 baseline을 저장
- 루프 변경만 별도 patch로 생성
- 가능하면 worktree 사용으로 이 문제 제거

baseline 기반이 어렵다면 최소한 allowed files만 patch에 저장한다.

```bash
git diff -- "${ALLOWED_FILES[@]}" > "$LOOP_DIR/diff.patch"
```

### 5. PASS 판정 규칙이 너무 단순함

현재:

> 반드시 수정이 비고 개선 권장도 비면 PASS

실제로는 개선 권장이 있어도 PASS로 끝낼 수 있어야 한다. 개선 권장이 모두 다음 루프로 이월 가능한 내용이면 PASS_WITH_NOTES가 맞다.

권장:

- `FAIL`: must fix 있음
- `PASS_WITH_NOTES`: must fix 없음, recommendations 있음
- `PASS`: must fix 없음, recommendations 없음
- `ESCALATED`: 충돌/판단 필요/요청 범위 불명확

자동 종료는 `PASS`와 `PASS_WITH_NOTES` 모두 허용하되, 터미널에는 notes를 보여준다.

### 6. Claude CLI 권한 옵션이 불충분함

Claude는 현재 `-p/--print`를 지원한다. 하지만 실제 파일 수정까지 하려면 permission mode와 tool 권한 설정이 중요하다.

검토된 옵션:

- `--permission-mode`
- `--allowedTools`
- `--disallowedTools`
- `--max-budget-usd`
- `--output-format`

권장:

```bash
claude -p \
  --permission-mode acceptEdits \
  --max-budget-usd 3 \
  "$PROMPT"
```

다만 실제 허용 모드는 테스트가 필요하다. 자동 루프 v1은 반드시 작은 샘플 repo 또는 별도 worktree에서 실험해야 한다.

### 7. Codex review 단계는 `codex review`도 검토할 수 있음

Codex CLI에는 `review` 서브커맨드가 있다. 현재 설계는 `codex exec`로 충분하지만, git diff 기반 코드 리뷰만 필요하면 `codex exec review` 또는 `codex review`가 더 적합할 수 있다.

다만 디자인/UX 문맥과 문서 리뷰까지 필요하므로 v1은 `codex exec`가 더 유연하다.

### 8. 자동 비용 제한이 빠져 있음

Claude에는 `--max-budget-usd` 옵션이 있다. Codex CLI 쪽 비용 제한은 help에서 바로 보이지 않는다.

권장:

- Claude 호출에는 `--max-budget-usd` 적용
- Codex 호출에는 timeout과 max_rounds로 간접 제한
- 루프 전체 예상 비용을 meta.json에 기록

### 9. 테스트/검증 단계가 없음

디자인 시스템 루프라면 최소 검증이 필요하다.

권장 옵션:

- `--verify none`: 검증 생략
- `--verify static`: rg 기반 금지 패턴 검사
- `--verify browser`: 로컬 preview 열고 screenshot/overflow 검사

최소 static 검사:

- 이모지 금지
- 금지 파일 변경 없음
- `--color-accent-rgb` 같은 required token 존재
- preview 파일의 하드코딩 hex 감소 여부

### 10. 한글 경로와 공백 경로 처리

repo 경로가 `/Users/yechanshon/Desktop/Haru Anbu`이고 한글 폴더가 많다. bash 스크립트에서 quoting이 조금만 어긋나도 깨진다.

권장:

- 모든 경로 변수는 반드시 quote
- 배열로 파일 목록 관리
- `find ... -print0` / `xargs -0` 사용
- `git diff --name-only -z` 고려

## 빠진 부분

### 1. 모델별 역할 고정

자동 루프에서는 모델 변경이 결과를 크게 흔든다. Claude와 Codex 각각 어떤 모델/effort를 쓸지 명시해야 한다.

예:

```txt
Claude: sonnet, implementation
Codex: default or gpt-5.x, review
Codex effort: medium/high
```

### 2. 루프 동시 실행 lock

v1에서 병렬 루프를 빼더라도, 사용자가 실수로 두 번 실행할 수 있다. lock 파일이 필요하다.

예:

```txt
07_디자인/_review_loop/.review-loop.lock
```

### 3. archive 정책

v1에서 자동 archive 이동을 빼는 건 괜찮지만, 완료 루프가 쌓이면 혼란스럽다. 최소한 status별 폴더명 또는 index가 필요하다.

### 4. 사람이 승인해야 하는 지점

"사람 개입 없음"은 편하지만, 디자인/의료/접근성 관련 결정은 사람이 승인해야 한다.

권장:

- 자동 루프는 commit하지 않음
- PASS여도 "ready for human review" 상태로 끝냄
- 터미널에 변경 파일과 남은 notes를 강하게 출력

### 5. 리뷰 기준 버전 관리

`_GUIDE.md`가 바뀌면 과거 루프의 판단 기준도 바뀐다. 각 루프 시작 시 guide snapshot을 loop folder에 복사해야 한다.

예:

```txt
2026-05-10_tokens-only/GUIDE_SNAPSHOT.md
```

### 6. 사용자 변경 보호

루프 도중 사용자가 파일을 수정할 수 있다. 시작 시점 baseline만으로는 중간 사용자 변경과 AI 변경을 구분하기 어렵다.

권장:

- 실행 중에는 lock 메시지 표시
- 각 단계 전후 파일 mtime 또는 git diff 체크
- 가능하면 별도 worktree 사용

## 더 안전한 v1 구조 제안

현재 A안을 바로 "풀 자동"으로 만들기보다 아래 v1을 추천한다.

### v1 목표

- 한 루프 한 번에 allowed files만 수정
- max_rounds 기본 1
- Claude만 소스 수정 가능
- Codex는 파일 수정 금지, 결과만 output file로 저장
- 스크립트가 LOG와 meta를 관리
- dirty repo 문제는 worktree 옵션으로 해결

### v1 폴더 구조

```txt
07_디자인/_review_loop/
├── _GUIDE_COMPACT.md
├── 2026-05-10_tokens-only/
│   ├── REQUEST.md
│   ├── GUIDE_SNAPSHOT.md
│   ├── meta.json
│   ├── diff.patch
│   ├── LOG.md
│   ├── round-1/
│   │   ├── claude-work.md
│   │   ├── codex-review.md
│   │   ├── codex-review.json
│   │   ├── claude-response.md
│   │   ├── codex-final.md
│   │   └── codex-final.json
│   └── command.log
```

### v1 Codex 호출 예시

```bash
codex exec \
  -C "/Users/yechanshon/Desktop/Haru Anbu" \
  -s workspace-write \
  -a never \
  --ephemeral \
  -o "$LOOP_DIR/round-1/codex-review.md" \
  "$PROMPT"
```

더 안전하게 Codex가 파일을 전혀 쓰지 않게 하려면 stdout 리다이렉션을 쓴다.

```bash
codex exec \
  -C "$REPO" \
  -s read-only \
  -a never \
  --ephemeral \
  "$PROMPT" > "$LOOP_DIR/round-1/codex-review.md"
```

이 경우 Codex는 repo 파일을 못 쓰고, shell이 output file을 만든다. 리뷰 단계에는 이 방식이 더 안전하다.

### v1 판정

Codex에게 JSON만 별도로 출력하게 하는 게 가장 좋다.

가능하면 `--output-schema` 사용:

```bash
codex exec \
  --output-schema "$ROOT/schemas/codex-verdict.schema.json" \
  -o "$LOOP_DIR/round-1/codex-final.json" \
  "$PROMPT"
```

단, 사람이 읽을 리뷰 md도 필요하므로 md와 json을 분리한다.

## 첫 루프 추천 요청문

`tokens-only`는 아래처럼 좁혀서 시작하라.

```md
## Allowed files

- 07_디자인/tokens/tokens.css

## Request

1. `--color-accent-rgb` 토큰을 `:root`와 각 role selector에 추가한다.
2. `[data-role="patient"][data-platform="mobile"]` 조합 규칙을 추가해 환자 접근성 토큰이 mobile 규칙에 덮이지 않게 한다.
3. primitive palette의 hex 값은 유지한다.
4. 다른 파일은 수정하지 않는다.

## Done criteria

- `02_COMPONENTS.md`의 `rgba(var(--color-accent-rgb), ...)` 예시가 실제 토큰과 맞는다.
- patient + mobile 조합에서 `--text-body: 18px`, `--size-touch-target: 56px`, `--size-button-default: 56px`가 유지된다.
```

## 최종 판단

이 설계는 "가능하지만, 그대로 풀 자동 구현하면 위험하다."

구현 전 반드시 바꿔야 할 핵심은 다음이다.

1. AI가 `LOG.md`를 직접 append하지 않게 한다.
2. verdict는 `LOG.md` grep이 아니라 JSON/별도 파일로 판정한다.
3. Codex 리뷰 단계는 가능하면 read-only로 돌리고 stdout을 스크립트가 파일에 저장한다.
4. dirty working tree 문제를 해결하기 위해 별도 worktree 또는 baseline/allowlist 방식을 넣는다.
5. 첫 버전은 `max_rounds=1`, allowed files 1개, 작은 변경으로 검증한다.

이 다섯 가지를 반영하면 v1 자동 루프는 충분히 시도할 만하다. 반대로 이걸 반영하지 않으면, 자동화 자체가 디자인 품질을 올리기보다 repo 상태를 더 복잡하게 만들 위험이 있다.
