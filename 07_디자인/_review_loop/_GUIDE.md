# Auto Review Loop — Full Guide

이 문서는 사람이 읽는 풀 가이드다. AI 호출에는 `_GUIDE_COMPACT.md` 가 들어간다.

선행 문서:
- `07_디자인/CLAUDE_CODEX_REVIEW_LOOP_PROPOSAL_20260510.md`
- `07_디자인/CLAUDE_CODEX_AUTO_LOOP_PLAN_V2_20260510.md` (구현 기준)
- `07_디자인/CODEX_REVIEW_OF_AUTO_LOOP_PLAN_20260510.md` (반영 출처)

## 1. 역할

| 역할 | 담당 |
|---|---|
| Claude | 구현/정리 (소스 파일 수정) |
| Codex  | 리뷰/QA (수정 금지, read-only) |
| 사용자 | 방향성과 최종 의사결정. PASS여도 머지 결정은 사람 |

## 2. 리뷰 6대 기준

### 2-1. 토큰 일관성

- hex 직접 사용이 남아 있는가?
- radius / spacing / shadow / blur가 토큰을 쓰는가?
- primitive token을 화면에서 직접 쓰지 않는가? (의도된 경우 제외)
- semantic / component token이 실제로 정의되어 있는가?
- 문서 예시가 존재하지 않는 토큰을 쓰고 있지 않은가?

### 2-2. 역할 테마 일관성

- guardian / medical / caregiver / patient 역할이 명확한가?
- "색만 바뀐다"가 아니라 환자 접근성 스케일까지 반영되는가?
- 의료진웹과 요양보호사앱이 같은 green 안에서도 사용 맥락 차이를 갖는가?
- 온보딩이 특정 역할에 과하게 치우치지 않는가?

### 2-3. UX/UI 적합성

- 보호자앱은 안심감과 감성 톤이 살아 있는가?
- 의료진웹은 정보 밀도와 스캔성이 좋은가?
- 요양보호사앱은 현장 입력이 빠르고 명확한가?
- 환자앱은 선택지가 적고 버튼/글자가 충분히 큰가?
- SOS / 긴급 / 오류 상태가 glass나 장식에 묻히지 않는가?

### 2-4. Glass 사용 원칙

> Glass는 브랜드 감성 / 요약 / 플로팅 레이어에만 사용한다.
> Flat은 입력 / 목록 / 업무 / 긴급 정보의 기본 표면으로 사용한다.

- glass가 보호자 홈, AI 리포트, 온보딩, 플로팅 탭바에 제한되어 있는가?
- 의료진웹 / 요양보호사 입력 / 환자 핵심 CTA / SOS에는 flat surface를 쓰는가?
- glass 위 텍스트 대비가 충분한가?
- blur와 투명도가 과하지 않은가?

### 2-5. 접근성

- 환자 화면 본문 최소 18px인가?
- 환자 주요 터치 타겟이 56px 이상인가?
- 색상만으로 상태를 전달하지 않는가?
- 주요 아이콘에 텍스트 라벨이 있는가?
- focus-visible이 보이는가?
- 모바일에서 텍스트 겹침/가로 overflow가 없는가?

### 2-6. 아이콘 / 문서 규칙

- 이모지가 없는가? (CLAUDE.md 절대 금지)
- iconify `fluent:*-filled` 계열만 쓰는가?
- AI 진입점은 sparkle이 아니라 하루안부 심볼을 쓰는가?
- 문서와 실제 코드가 서로 다른 말을 하지 않는가?
- 버전과 날짜가 맞는가?

## 3. Verdict 정의

| Verdict | 의미 |
|---|---|
| `PASS` | must_fix 비음, recommendations 비음 |
| `PASS_WITH_NOTES` | must_fix 비음, recommendations 있음 (다음 루프 후보) |
| `FAIL` | must_fix 있음 |
| `ESCALATED` | 요청 자체가 모호 / 충돌 / 사람 판단 필요 |

스크립트는 `PASS`와 `PASS_WITH_NOTES` 둘 다 자동 종료. 그래도 머지는 사람 결정.

## 4. 운영 원칙

- 자동 루프는 git commit / push 절대 안 한다.
- worktree 안에서 실행되며, worktree는 사용자 승인 전 자동 삭제 안 한다.
- Allowed files 외 파일은 단계마다 `enforce_scope` 가 차단한다.
- 금지 파일: `.env*`, `secrets/**`, `package*.json`, `*.lock`, `yarn.lock`. allowlist에 들어 있어도 차단.
- 한 루프는 1 라운드 기본. `--rounds 2` 로 늘릴 수 있지만 같은 지적이 두 번 반복되면 ESCALATED.
- 디자인 / 의료 / 접근성 결정은 사람이 최종 판단.

## 5. 실패 모드

| 상황 | 결과 | 사용자 복구 |
|---|---|---|
| Allowed files 누락 | abort, exit 1 | REQUEST.md 에 섹션 추가 |
| Allowed files 외 변경 감지 | FAIL_SCOPE_VIOLATION, exit 3 | worktree 폐기, REQUEST 다듬기 |
| 금지 파일 변경 | FAIL_FORBIDDEN_FILES, exit 3 | 동일 |
| Codex verdict ESCALATED | 종료, exit 2 | LOG.md 읽고 사람이 판단 |
| max_rounds 소진 | ESCALATED, exit 2 | 동일 |
| Claude / Codex CLI 인증 만료 | abort, exit 4 / 5 | 인증 후 재실행 |
| 동시 실행 (lock 충돌) | abort, exit 7 | 기존 루프 종료 후 재실행 |
| 중간 Ctrl+C | meta status=interrupted | 새 루프 시작 (resume 미지원) |

## 6. 폴더 구조 약속

```txt
07_디자인/_review_loop/
├── _GUIDE.md                 # 이 파일
├── _GUIDE_COMPACT.md         # AI 호출 시 들어가는 압축본
├── _TEMPLATE/                # 새 루프 복사 원본
├── schemas/
│   └── codex-verdict.schema.json
└── <YYYY-MM-DD>_<name>/      # 실제 루프
    ├── REQUEST.md
    ├── GUIDE_SNAPSHOT.md
    ├── meta.json
    ├── diff.patch
    ├── LOG.md
    ├── command.log
    ├── stdio/
    └── round-N/
        ├── claude-work.{md,json}
        ├── codex-review.{md,json}
        ├── claude-response.{md,json}
        └── codex-final.{md,json}
```

LOG.md, meta.json, GUIDE_SNAPSHOT.md 는 스크립트만 작성. AI는 round-N 폴더 자기 파일만 작성.

## 7. 첫 루프 권장

```bash
./scripts/review-loop.sh tokens-only
```

REQUEST 본문은 `12절 첫 루프` (V2 계획서) 또는 이 폴더 README의 예시 참조.
