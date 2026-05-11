# Claude + Codex 풀 자동 리뷰 루프 (A안) 설계서

작성일: 2026-05-10
작성자: Claude (사용자 요청에 따라 Codex 리뷰용으로 작성)
선행 문서: `07_디자인/CLAUDE_CODEX_REVIEW_LOOP_PROPOSAL_20260510.md`

목적: Claude와 Codex가 같은 폴더를 매개로 자동으로 작업 → 리뷰 → 반영 → 최종 QA 4단계를 순차 수행한다. 사용자는 명령어 한 줄과 REQUEST 5줄만 작성한다.

Codex에게: 이 문서는 구현 전 단계의 설계서다. **실제로 만들기 전에 너의 비판이 필요하다.** 직접 코드를 만들지 말고, 이 설계가 실제로 굴러갈지 / 빠진 게 있는지 / 위험한 부분은 없는지 검토해라. 검토 결과는 같은 폴더에 `CODEX_REVIEW_OF_AUTO_LOOP_PLAN_20260510.md`로 작성해라.

---

## 1. 사용자 관점 — 실제 사용 흐름

### 1-1. 가장 짧은 형태

```bash
./scripts/review-loop.sh tokens-only "tokens.css의 hex 하드코딩 정리, --color-accent-rgb 추가"
```

이후 사람 개입 없음. 5~15분 후 터미널에:

```txt
[review-loop] done.
[review-loop] result: PASS (round 1)
[review-loop] log:    07_디자인/_review_loop/2026-05-10_tokens-only/LOG.md
[review-loop] diff:   07_디자인/_review_loop/2026-05-10_tokens-only/diff.patch
[review-loop] next:   review the diff and commit if OK
```

### 1-2. 인자 형태

| 인자 | 필수 | 의미 |
|---|---|---|
| `$1` | 필수 | 루프 이름 (kebab-case 권장: `tokens-only`, `preview-roles`) |
| `$2` | 선택 | REQUEST 본문. 생략 시 `$EDITOR`로 `REQUEST.md`를 연다 |

루프 폴더 이름은 자동으로 `YYYY-MM-DD_$1` 형식이 된다. 같은 날 같은 이름이면 `_2`, `_3`이 붙는다.

---

## 2. 폴더 구조

```txt
07_디자인/_review_loop/
├── _GUIDE.md                       # 루프 규칙·기준·프롬프트 SoT (사람이 작성)
├── _TEMPLATE/                      # 새 루프 복사용
│   ├── REQUEST.md                  # 빈 양식
│   └── LOG.md                      # 빈 양식 (frontmatter만)
├── 2026-05-10_tokens-only/         # 실제 루프 (스크립트가 생성)
│   ├── REQUEST.md                  # 사용자 작성
│   ├── LOG.md                      # Claude/Codex가 append
│   ├── diff.patch                  # Claude가 저장
│   └── meta.json                   # 스크립트가 관리 (status, round, timestamps)
└── archive/                        # 완료된 루프 이동 (선택)
```

`_GUIDE.md` 는 선행 문서의 "리뷰 기준" 6개 섹션 그대로 옮겨 둔다. 이 파일이 SoT 이므로 Claude/Codex 둘 다 매번 읽는다.

---

## 3. LOG.md 포맷

루프 폴더 안의 LOG.md는 양쪽 AI가 append-only로 쓴다.

```md
---
loop: 2026-05-10_tokens-only
status: codex-turn        # claude-turn | codex-turn | done | escalated
round: 1
max_rounds: 2
result:                   # PASS | FAIL | ESCALATED (status=done 일 때만)
---

# Loop log

## [Claude 2026-05-10 14:32:15] round 1 work

### 변경 파일
- 07_디자인/tokens/tokens.css

### 의도
- hex 하드코딩 → semantic token 치환

### 걱정되는 부분
- patient + mobile 토큰 충돌 가능성

### Codex 리뷰 포인트
- 토큰 일관성, 환자 접근성

---

## [Codex 2026-05-10 14:55:02] round 1 review

### 반드시 수정
1. tokens.css:142 — glass-blur가 primitive 직접 사용

### 개선 권장
1. patient 스케일 별도 분리 권장

### 유지 좋은 점
- semantic token 분리 깔끔함

---

## [Claude 2026-05-10 15:10:44] round 1 response

### 반영
- [x] glass-blur semantic token 분리

### 미반영
- [ ] patient 스케일 분리 → 다음 루프

---

## [Codex 2026-05-10 15:20:11] final QA

결과: PASS
남은 이슈: patient 스케일 (다음 루프 이월)
```

규칙:
- `## [Actor YYYY-MM-DD HH:MM:SS] round N <kind>` 헤더로 구분
- `<kind>` 는 `work | review | response | final` 중 하나
- 각 섹션 끝에 `---` 구분선
- frontmatter는 스크립트만 수정. Claude/Codex는 본문만 append

---

## 4. meta.json

스크립트가 관리하는 상태 파일. AI는 읽기만.

```json
{
  "loop": "2026-05-10_tokens-only",
  "status": "codex-turn",
  "round": 1,
  "max_rounds": 2,
  "result": null,
  "started_at": "2026-05-10T14:32:00+09:00",
  "history": [
    {"step": "claude-work",    "round": 1, "at": "...", "duration_s": 423},
    {"step": "codex-review",   "round": 1, "at": "...", "duration_s": 187},
    {"step": "claude-respond", "round": 1, "at": "...", "duration_s": 312}
  ]
}
```

---

## 5. 스크립트 동작 흐름

### 5-1. 의사코드

```bash
#!/usr/bin/env bash
set -euo pipefail

NAME="${1:?usage: review-loop.sh <name> [request-body]}"
REQUEST_BODY="${2:-}"

ROOT="07_디자인/_review_loop"
DATE=$(date +%Y-%m-%d)
LOOP_DIR=$(unique_dir "$ROOT/${DATE}_${NAME}")        # _2, _3 접미사 자동
MAX_ROUNDS=2

# --- 0. setup ---
cp -r "$ROOT/_TEMPLATE/." "$LOOP_DIR/"
init_meta_json "$LOOP_DIR" "$NAME"

if [ -n "$REQUEST_BODY" ]; then
  printf "# 작업 요청\n\n%s\n" "$REQUEST_BODY" > "$LOOP_DIR/REQUEST.md"
else
  "${EDITOR:-vim}" "$LOOP_DIR/REQUEST.md"
fi

# --- 1..N. loop ---
for round in $(seq 1 "$MAX_ROUNDS"); do
  set_meta status=claude-turn round="$round"

  # 1. Claude work
  claude -p "$(prompt_claude_work "$LOOP_DIR" "$round")"
  save_diff_to "$LOOP_DIR/diff.patch"
  set_meta status=codex-turn

  # 2. Codex review
  codex exec "$(prompt_codex_review "$LOOP_DIR" "$round")"
  set_meta status=claude-turn

  # 3. parse review verdict
  if codex_said_pass_without_must_fix "$LOOP_DIR/LOG.md"; then
    finalize PASS
    exit 0
  fi

  # 4. Claude respond
  claude -p "$(prompt_claude_respond "$LOOP_DIR" "$round")"
  save_diff_to "$LOOP_DIR/diff.patch"
  set_meta status=codex-turn

  # 5. Codex final QA for this round
  codex exec "$(prompt_codex_final "$LOOP_DIR" "$round")"

  if codex_final_pass "$LOOP_DIR/LOG.md"; then
    finalize PASS
    exit 0
  fi
done

# 모든 라운드 소진
finalize ESCALATED
exit 2
```

### 5-2. finalize 동작

- meta.json에 `status=done`, `result=PASS|ESCALATED` 기록
- 마지막 git diff 다시 저장
- 터미널에 결과 요약 출력
- **git commit은 절대 하지 않는다** (사람 결정)
- ESCALATED인 경우 exit code 2로 종료해서 사용자/CI가 인지

---

## 6. AI 프롬프트

### 6-1. Claude work 프롬프트

```txt
You are working in the Haru Anbu repo.

REQUIRED reading first:
1. 07_디자인/_review_loop/_GUIDE.md
2. {LOOP_DIR}/REQUEST.md
3. {LOOP_DIR}/LOG.md (if not empty — prior rounds)

You are the implementation/cleanup role.

Rules:
- 이모지 금지 (CLAUDE.md)
- 아이콘은 iconify fluent filled 계열만
- 토큰 SoT는 07_디자인/tokens/tokens.css
- 보호자앱/AI리포트/온보딩만 glass 허용
- 의료진/요양보호사 입력/환자 CTA/SOS는 flat surface

Tasks:
1. Implement the request.
2. Append a section to {LOOP_DIR}/LOG.md with this exact header:
   ## [Claude {ISO_TIMESTAMP}] round {ROUND} work
3. The section must include: 변경 파일 / 의도 / 걱정되는 부분 / Codex 리뷰 포인트.
4. End the section with a `---` line.
5. Do NOT modify frontmatter or meta.json.
6. Do NOT commit.

Stop when done.
```

### 6-2. Codex review 프롬프트

```txt
You are reviewing in the Haru Anbu repo.

REQUIRED reading:
1. 07_디자인/_review_loop/_GUIDE.md
2. {LOOP_DIR}/REQUEST.md
3. {LOOP_DIR}/LOG.md
4. {LOOP_DIR}/diff.patch

You are the QA/review role. **Do NOT modify any source file.**
Only append to {LOOP_DIR}/LOG.md.

Apply the 6 review criteria from _GUIDE.md:
토큰 일관성, 역할 테마, UX/UI, glass 사용, 접근성, 아이콘/문서

Output format — append to LOG.md exactly:

## [Codex {ISO_TIMESTAMP}] round {ROUND} review

### 반드시 수정
1. ...

### 개선 권장
1. ...

### 유지 좋은 점
- ...

### 확인한 파일
- ...

---

If "반드시 수정" is empty AND "개선 권장" is empty, end the section with:
VERDICT: PASS-NO-CHANGES

Do not modify frontmatter or meta.json. Do not commit.
```

### 6-3. Claude respond 프롬프트

```txt
Read {LOOP_DIR}/LOG.md. Find the latest [Codex review] section.

Apply the "반드시 수정" items. Apply "개선 권장" if compatible with the request scope.
For items you skip, document the reason.

Append a section:

## [Claude {ISO_TIMESTAMP}] round {ROUND} response

### 반영
- [x] ...

### 미반영
- [ ] ... — reason: ...

### 추가 변경 파일
- ...

---

Do not modify frontmatter or meta.json. Do not commit.
```

### 6-4. Codex final QA 프롬프트

```txt
Read {LOOP_DIR}/LOG.md and {LOOP_DIR}/diff.patch (refreshed).

Verify the latest Claude response addressed the previous review.

Append:

## [Codex {ISO_TIMESTAMP}] round {ROUND} final

결과: PASS | FAIL
남은 이슈: ...
최종 판단: ...

VERDICT: PASS    # or VERDICT: FAIL

---

Do not modify any source file. Do not modify frontmatter or meta.json.
```

스크립트는 LOG.md에서 마지막 `VERDICT: PASS` 또는 `VERDICT: PASS-NO-CHANGES` 줄을 찾아 종료 판정한다.

---

## 7. 안전장치

### 7-1. 자동 루프의 본질적 위험

사용자가 안 보는 동안 AI가 파일을 고친다. 잘못 고치면 알아차리는 게 늦다. 따라서:

| 안전장치 | 구현 |
|---|---|
| git commit 절대 금지 | 스크립트가 `git commit` 호출 안 함. 프롬프트에서도 명시 금지 |
| 작업 전 브랜치 확인 | main 브랜치면 abort. feat/* 또는 chore/* 만 허용 |
| 작업 전 working tree 깨끗 확인 | `git status --porcelain`이 비어있지 않으면 abort (사용자 변경 덮어쓰기 방지) |
| 작업 범위 제한 | REQUEST.md에 명시된 파일/폴더 외엔 수정 금지 (프롬프트로 강제) |
| max_rounds | 기본 2. 무한 루프 방지 |
| 타임아웃 | 각 단계 최대 10분. 초과 시 abort |
| 사용자 인터럽트 | Ctrl+C 시 meta.json에 `status=interrupted` 남기고 종료 |
| 외부 패키지 변경 차단 | package.json / lock 파일은 수정 금지 (프롬프트 + 후 검증) |
| 비밀파일 차단 | `.env*`, `secrets/*` 는 수정 금지 (프롬프트 + 후 검증) |

### 7-2. 후처리 검증

스크립트가 모든 라운드 끝난 뒤 한 번 더 검증:

```bash
# 금지된 파일이 변경되었는지 체크
forbidden=$(git diff --name-only | grep -E '(\.env|secrets/|package(-lock)?\.json|yarn\.lock)' || true)
if [ -n "$forbidden" ]; then
  finalize FAIL_FORBIDDEN_FILES
  exit 3
fi
```

### 7-3. 무한 핑퐁 방지

같은 지적이 round 1, round 2에 반복되면 ESCALATED로 종료. 구체적으로는:

```bash
if grep -c "동일 키워드" 등 휴리스틱 → 위험. 대신:
round 2의 Codex review가 round 1의 review와 90% 이상 중복되면 사람에게.
```

휴리스틱 정확도는 낮을 수 있으므로 **기본은 max_rounds=2로 강제 종료**하는 쪽이 안전.

---

## 8. 의존성

| 항목 | 비고 |
|---|---|
| `claude` CLI | 헤드리스 `-p` 또는 `--print` 모드. 인증 완료 가정 |
| `codex` CLI | 헤드리스 실행 모드. 정확한 명령은 `codex --help` 확인 필요 |
| `jq` | meta.json 조작 |
| `git` | diff 추출, 브랜치 확인 |
| bash 4+ | macOS 기본은 3.2 — `/opt/homebrew/bin/bash` 사용 권장 |

`codex exec` 가 정확한 명령인지 확실하지 않다. 첫 구현 전 `codex --help` 출력으로 확정 필요.

---

## 9. 첫 적용 시나리오

가장 작은 범위로 루프 자체의 안정성을 검증한다.

```bash
./scripts/review-loop.sh tokens-only "tokens.css의 hex 하드코딩을 semantic token으로 정리. --color-accent-rgb 추가. 다른 파일은 건드리지 마라."
```

기대 결과:
- LOG.md에 4개 섹션 (Claude work / Codex review / Claude response / Codex final)
- diff.patch는 tokens.css 단일 파일
- 결과 PASS

이게 한 번 깔끔히 돌면 그 다음 후보:
1. `preview-roles` (preview-roles.html 통일성)
2. `glass-policy` (glass 사용 범위 정리)
3. `patient-a11y` (환자앱 접근성 audit)

---

## 10. 실패 모드와 복구

| 상황 | 스크립트 동작 | 사용자 복구 |
|---|---|---|
| Claude CLI 인증 만료 | 즉시 abort, exit 4 | `claude login` 후 재실행 |
| Codex CLI 인증 만료 | abort, exit 5 | Codex 인증 후 재실행 |
| working tree dirty | abort, exit 6 | 변경사항 커밋 또는 stash 후 재실행 |
| ESCALATED | 종료, exit 2 | LOG.md 읽고 사람이 판단 후 직접 수정 또는 새 루프 |
| FAIL_FORBIDDEN_FILES | 종료, exit 3 | git restore로 되돌리고 REQUEST 다듬기 |
| 중간에 Ctrl+C | meta.json status=interrupted | 같은 폴더에 `--resume` 옵션으로 재개 (확장 기능) |

`--resume` 은 v1에서는 빼도 됨. 중단 시 폴더 그대로 두고 새 루프 시작.

---

## 11. 비용/시간 추정

| 항목 | 추정 |
|---|---|
| 한 라운드 = 4번 모델 호출 | Claude work / Codex review / Claude respond / Codex final |
| 한 호출당 토큰 | 입력 5~30k, 출력 1~5k (변경 파일 크기에 따라) |
| 한 라운드 시간 | 5~15분 |
| 한 라운드 비용 | $0.5 ~ $3 (모델/길이에 따라) |
| 2 라운드 풀 진행 | 10~30분, $1~$6 |

작업 1건당 사람 시간 대비 비용 균형은 명확히 사용자 시간 절약 쪽.

---

## 12. v1에서 빼는 것 (의도적 단순화)

- `--resume`
- 자동 archive 이동
- 무한 핑퐁 휴리스틱 (max_rounds 강제로 충분)
- 병렬 루프 (한 번에 한 루프만)
- Slack/이메일 알림 (`osascript` 로컬 알림은 가능하지만 v1에서는 빼고 터미널 출력만)
- AI가 PR 자동 생성 (사람이 직접 만든다)

이것들은 v1이 안정화되고 사용 패턴이 보이면 추가.

---

## 13. 열린 질문 (Codex가 답해줬으면 하는 부분)

1. **Codex CLI 헤드리스 명령**: 정확히 `codex exec "<prompt>"` 가 맞는가? 다른 형태인가? 환경에 따라 다른가?
2. **Codex가 파일 쓰기 가능한가**: 헤드리스 모드에서 LOG.md에 append할 수 있는가? 권한 모델이 어떻게 되는가?
3. **무한 루프 휴리스틱**: 라운드 간 review 중복도 검사가 필요한가, 아니면 max_rounds=2면 충분한가?
4. **VERDICT 파싱**: LOG.md를 grep으로 파싱하는 게 안정적인가? 더 좋은 방법(별도 verdict 파일 등)이 있는가?
5. **첫 작업 범위**: 첫 루프로 tokens-only가 적절한가, 더 작아야 하는가?
6. **이 설계에 빠진 안전장치**: 7-1 표 외에 추가해야 할 것이 있는가?
7. **`_GUIDE.md` 분량**: 매 호출마다 읽으면 비용이 누적된다. 핵심만 추리는 게 좋은가, 풀로 가는 게 좋은가?
8. **Codex 입장에서 작성하기 어려운 프롬프트가 있는가**: 6-2, 6-4의 프롬프트가 실제로 쓸 만한가?

---

## 14. 결론

A안(풀 자동)은 기술적으로 가능하다. 본질적 위험은 unattended 작업의 사고 가능성이며, 이는 git commit 차단 / 작업 범위 제한 / max_rounds로 통제한다.

이 설계대로 구현하면 사용자는 명령어 1줄 + REQUEST 5줄로 한 사이클을 돌릴 수 있고, 모든 기록이 LOG.md에 남는다.

**Codex에게**: 13번의 열린 질문을 우선 검토해라. 추가로 이 문서 전반에서 빠졌거나 위험하거나 비현실적인 부분을 짚어줘. 결과는 `07_디자인/CODEX_REVIEW_OF_AUTO_LOOP_PLAN_20260510.md`로 작성한다.
