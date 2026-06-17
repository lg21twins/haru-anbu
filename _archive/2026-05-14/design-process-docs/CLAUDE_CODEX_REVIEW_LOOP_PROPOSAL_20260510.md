# Claude + Codex 상호 피드백 루프 제안서

작성일: 2026-05-10

목적: 하루안부 디자인 시스템과 앱 화면 작업에서 Claude와 Codex가 서로 건설적으로 비판하고 반영하는 과정을 반복 가능하게 만든다.

## 배경

현재 작업 흐름은 대략 다음과 같다.

1. Claude가 디자인 시스템 또는 화면을 정리/수정한다.
2. 사용자가 Codex에게 "이거 어때?"라고 물어본다.
3. Codex가 통일성, UX/UI, 토큰, 접근성 관점에서 비판한다.
4. 사용자가 그 내용을 Claude에게 다시 전달한다.
5. Claude가 반영한다.

이 방식은 품질은 좋아질 수 있지만 매번 사용자가 중간 전달자가 되어야 해서 피곤하다. 따라서 각 AI가 읽고 쓸 파일을 정해두고, 같은 구조로 리뷰를 주고받게 만들면 반복 작업이 쉬워진다.

## 목표

- Claude는 구현/정리 담당
- Codex는 비판/QA/일관성 리뷰 담당
- 사용자는 방향성과 최종 의사결정 담당
- 리뷰 내용은 매번 md 파일로 남겨 추적 가능하게 한다.
- 디자인 시스템, 보호자앱, 의료진웹, 요양보호사앱, 환자앱 모두 같은 루프를 적용할 수 있게 한다.

## 제안 폴더 구조

위치:

```txt
07_디자인/_review_loop/
```

기본 파일:

```txt
07_디자인/_review_loop/
├── 00_LOOP_GUIDE.md
├── 01_REQUEST.md
├── 02_CLAUDE_OUTPUT.md
├── 03_CODEX_REVIEW.md
├── 04_CLAUDE_RESPONSE.md
├── 05_CODEX_FINAL_QA.md
└── archive/
```

각 파일 역할:

| 파일 | 작성자 | 목적 |
|---|---|---|
| `00_LOOP_GUIDE.md` | 사람/Codex | 루프 규칙, 역할, 리뷰 기준 |
| `01_REQUEST.md` | 사용자 또는 Claude | 이번 작업 요청과 범위 |
| `02_CLAUDE_OUTPUT.md` | Claude | Claude가 한 작업 요약, 변경 파일, 의도 |
| `03_CODEX_REVIEW.md` | Codex | Codex의 건설적 비판, 리스크, 개선 제안 |
| `04_CLAUDE_RESPONSE.md` | Claude | 리뷰 반영 여부, 반영/미반영 이유 |
| `05_CODEX_FINAL_QA.md` | Codex | 최종 검수 결과, 남은 리스크 |
| `archive/` | 자동/수동 | 완료된 루프 보관 |

## 기본 워크플로우

### Step 1. 요청 작성

사용자가 `01_REQUEST.md`에 이번 작업 범위를 작성한다.

예시:

```md
# 작업 요청

대상:
- `07_디자인/preview.html`
- `07_디자인/tokens/tokens.css`
- `07_디자인/preview-roles.html`

요청:
- 디자인 시스템 preview의 통일성을 개선한다.
- 프리뷰 코드가 실제 토큰 시스템을 따르게 한다.
- 직접적인 화면 리디자인보다 토큰/문서/원칙 정리를 우선한다.

주의:
- 이모지 금지
- Fluent/iconify 아이콘만 사용
- 환자앱 접근성 유지
- 의료진/요양보호사 업무 화면에는 과도한 glass 사용 금지
```

### Step 2. Claude 작업

Claude는 `01_REQUEST.md`를 읽고 실제 파일을 수정한다. 이후 `02_CLAUDE_OUTPUT.md`를 작성한다.

`02_CLAUDE_OUTPUT.md` 형식:

```md
# Claude 작업 요약

## 변경 파일

- `...`
- `...`

## 변경 내용

- ...
- ...

## 의도

- ...

## Claude가 판단한 리스크

- ...

## Codex에게 리뷰 요청할 포인트

- 토큰 일관성 확인
- glass 사용 범위 확인
- 환자 접근성 충돌 여부 확인
```

### Step 3. Codex 리뷰

Codex는 `01_REQUEST.md`, `02_CLAUDE_OUTPUT.md`, 실제 변경 파일, 가능하면 `git diff`를 보고 `03_CODEX_REVIEW.md`를 작성한다.

Codex는 직접 수정하지 않고 비판과 제안만 작성한다.

`03_CODEX_REVIEW.md` 형식:

```md
# Codex 리뷰

## 총평

...

## 반드시 수정

1. ...
2. ...

## 개선 권장

1. ...
2. ...

## 유지하면 좋은 점

- ...

## 확인한 파일

- ...

## Claude에게 요청

- ...
```

### Step 4. Claude 반영

Claude는 `03_CODEX_REVIEW.md`를 읽고 반영한다. 이후 `04_CLAUDE_RESPONSE.md`를 작성한다.

`04_CLAUDE_RESPONSE.md` 형식:

```md
# Claude 리뷰 반영 내역

## 반영한 항목

- [x] ...
- [x] ...

## 반영하지 않은 항목

- [ ] ...

반영하지 않은 이유:
...

## 추가 변경 파일

- ...

## Codex 최종 QA 요청

- ...
```

### Step 5. Codex 최종 QA

Codex는 최종 파일을 확인하고 `05_CODEX_FINAL_QA.md`를 작성한다.

`05_CODEX_FINAL_QA.md` 형식:

```md
# Codex 최종 QA

## 결과

통과 / 부분 통과 / 재작업 필요

## 남은 이슈

- ...

## 최종 판단

...
```

## 리뷰 기준

디자인 시스템과 앱 화면을 리뷰할 때 Codex는 아래 기준을 반복 적용한다.

### 1. 토큰 일관성

- hex 직접 사용이 남아 있는가?
- radius, spacing, shadow, blur가 토큰을 쓰는가?
- primitive token을 실제 화면에서 직접 쓰고 있지 않은가?
- semantic/component token이 실제로 정의되어 있는가?
- 문서 예시가 존재하지 않는 토큰을 쓰고 있지 않은가?

### 2. 역할 테마 일관성

- guardian / medical / caregiver / patient 역할이 명확한가?
- "색만 바뀐다"가 아니라 환자 접근성 스케일까지 반영되는가?
- 의료진웹과 요양보호사앱이 같은 green 안에서도 사용 맥락 차이를 갖는가?
- 온보딩이 특정 역할에 과하게 치우치지 않는가?

### 3. UX/UI 적합성

- 보호자앱은 안심감과 감성 톤이 살아 있는가?
- 의료진웹은 정보 밀도와 스캔성이 좋은가?
- 요양보호사앱은 현장 입력이 빠르고 명확한가?
- 환자앱은 선택지가 적고 버튼/글자가 충분히 큰가?
- SOS/긴급/오류 상태가 glass나 장식에 묻히지 않는가?

### 4. Glass 사용 원칙

권장 원칙:

> Glass는 브랜드 감성/요약/플로팅 레이어에만 사용한다. Flat은 입력/목록/업무/긴급 정보의 기본 표면으로 사용한다.

리뷰 기준:

- glass가 보호자 홈, AI 리포트, 온보딩, 플로팅 탭바에 제한되어 있는가?
- 의료진웹/요양보호사 입력/환자 핵심 CTA/SOS에는 flat surface를 쓰는가?
- glass 위 텍스트 대비가 충분한가?
- blur와 투명도가 과하지 않은가?

### 5. 접근성

- 환자 화면 본문 최소 18px인가?
- 환자 주요 터치 타겟이 56px 이상인가?
- 색상만으로 상태를 전달하지 않는가?
- 주요 아이콘에 텍스트 라벨이 있는가?
- focus-visible이 보이는가?
- 모바일에서 텍스트 겹침/가로 overflow가 없는가?

### 6. 아이콘/문서 규칙

- 이모지가 없는가?
- iconify `fluent:*-filled` 계열만 쓰는가?
- AI 진입점은 sparkle이 아니라 하루안부 심볼을 쓰는가?
- 문서와 실제 코드가 서로 다른 말을 하지 않는가?
- 버전과 날짜가 맞는가?

## Claude용 고정 프롬프트

Claude에게 아래 프롬프트를 주면 된다.

```md
`07_디자인/_review_loop/00_LOOP_GUIDE.md`와 `01_REQUEST.md`를 읽어라.

너는 하루안부 디자인 시스템 구현/정리 담당이다.

작업 원칙:
- AGENTS.md의 이모지 금지 규칙을 지킨다.
- UI 아이콘은 iconify의 fluent filled 계열만 사용한다.
- 토큰 SoT는 `07_디자인/tokens/tokens.css`다.
- 실제 컴포넌트 예시는 가능하면 semantic/component token만 사용한다.
- 보호자앱/AI리포트/온보딩은 glass를 사용할 수 있다.
- 의료진웹/요양보호사 입력/환자 핵심 CTA/SOS는 flat surface를 기본으로 한다.

작업 후 `02_CLAUDE_OUTPUT.md`를 작성하라.
Codex가 리뷰하기 쉽도록 변경 파일, 변경 의도, 걱정되는 부분을 명확히 적어라.
```

## Codex용 고정 프롬프트

Codex에게 아래 프롬프트를 주면 된다.

```md
`07_디자인/_review_loop/00_LOOP_GUIDE.md`, `01_REQUEST.md`, `02_CLAUDE_OUTPUT.md`를 읽어라.

너는 하루안부 디자인 시스템 리뷰어다.

직접 수정하지 말고, 아래 관점으로 건설적 비판만 작성하라.

- 토큰 일관성
- 역할 테마 일관성
- UX/UI 적합성
- glass 사용 범위
- 환자 접근성
- 의료진/요양보호사 업무 효율
- 이모지/아이콘 규칙
- 모바일 오버플로우/텍스트 겹침
- 문서와 코드 불일치

리뷰 결과는 `03_CODEX_REVIEW.md`에 작성하라.
반드시 "반드시 수정", "개선 권장", "유지하면 좋은 점"을 나눠라.
```

## 수동 루프 운영 방법

현재 가장 현실적인 방식은 수동 파일 기반 루프다.

1. 사용자가 `01_REQUEST.md` 작성
2. Claude에게 "이 파일 보고 작업하고 `02_CLAUDE_OUTPUT.md` 작성해"라고 요청
3. Codex에게 "루프 파일 보고 `03_CODEX_REVIEW.md` 작성해"라고 요청
4. Claude에게 "Codex 리뷰 반영하고 `04_CLAUDE_RESPONSE.md` 작성해"라고 요청
5. Codex에게 "최종 QA하고 `05_CODEX_FINAL_QA.md` 작성해"라고 요청

장점:

- 도구/API 연동 없이 바로 가능
- 모든 피드백이 파일로 남음
- 사용자가 중간 설명을 반복하지 않아도 됨
- 디자인 시스템 품질 기준이 누적됨

단점:

- 사용자가 Claude와 Codex 사이에서 실행 요청은 해줘야 함
- 완전 자동은 아님

## 반자동화 아이디어

나중에 Claude CLI, Codex CLI 또는 API가 로컬에서 안정적으로 가능하면 아래처럼 스크립트화할 수 있다.

```txt
Claude 작업
-> git diff 저장
-> Codex 리뷰 파일 생성
-> Claude 리뷰 반영
-> Codex 최종 QA
```

예상 폴더:

```txt
scripts/
└── review-loop.sh
```

예상 명령:

```bash
./scripts/review-loop.sh design
```

다만 이 단계는 현재 필수는 아니다. 먼저 md 기반 수동 루프를 안정화하는 것이 좋다.

## 자동화 시 주의점

- AI가 서로의 지적을 무한 반복하지 않도록 최대 반복 횟수를 둔다.
- 예: 최대 2회 반영 루프 후 사람이 결정.
- 모든 변경은 git diff로 확인한다.
- Claude와 Codex가 같은 파일을 동시에 수정하지 않게 한다.
- Codex 리뷰 단계는 기본적으로 수정 금지, 리뷰 파일 작성만 한다.
- 긴급/접근성/의료 관련 UX는 사람이 최종 판단한다.

## 제안하는 첫 적용 대상

첫 루프는 디자인 시스템 preview로 시작하는 것이 좋다.

대상:

- `07_디자인/preview.html`
- `07_디자인/_preview-shared.css`
- `07_디자인/preview-roles.html`
- `07_디자인/tokens/tokens.css`
- `07_디자인/README.md`

첫 요청 예시:

```md
디자인 시스템 preview의 통일성을 개선한다.

목표:
- preview 계열 코드의 하드코딩 값을 토큰 기반으로 정리
- patient + mobile 토큰 충돌 수정
- `--color-accent-rgb` 추가
- glass 사용 원칙을 감성형/업무형 화면으로 분리
- 메인 preview와 하위 preview의 visual rhythm 통일

수정 후 Claude는 `02_CLAUDE_OUTPUT.md`에 변경 의도와 변경 파일을 적는다.
```

## 기대 효과

- Claude의 구현 속도와 Codex의 비판적 검토를 분리할 수 있다.
- 디자인 시스템이 선언으로 끝나지 않고 실제 코드 품질로 이어진다.
- 같은 실수, 예를 들어 hex 하드코딩, token 누락, glass 과사용, 환자 접근성 누락을 반복해서 줄일 수 있다.
- 리뷰 기록이 남아서 프로젝트 후반에 "왜 이렇게 정했는지" 추적하기 쉽다.

## 결론

Claude와 Codex의 상호 피드백은 완전 자동화보다 먼저 파일 기반 수동 루프로 시작하는 것이 현실적이다. `07_디자인/_review_loop/`에 정해진 파일을 두고, Claude는 구현 요약을 쓰고 Codex는 리뷰를 쓰고 Claude가 반영 내역을 쓰는 구조를 만들면 사용자는 중간 전달 부담을 크게 줄일 수 있다.

이 루프가 안정화되면 나중에 CLI/API 기반 반자동화로 확장하면 된다.
