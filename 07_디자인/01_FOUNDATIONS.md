# 01 · Foundations

**하루안부 디자인 시스템 v3.2 — 파운데이션**

이 문서는 하루안부의 모든 앱이 공유하는 기반 규칙이다. 컬러·타이포·간격 같은 토큰부터 브랜드 톤·로고·접근성 원칙까지 — 화면 한 줄을 그리기 전에 결정되어야 하는 것들만 모았다. 컴포넌트 단위 규칙은 [02_COMPONENTS.md](02_COMPONENTS.md), 화면 단위 패턴은 [03_PATTERNS.md](03_PATTERNS.md) 참조.

토큰의 실제 값은 [tokens/tokens.css](tokens/tokens.css)에 있다. 이 문서는 "왜 이렇게 정했는가" 와 "어떻게 써야 하는가" 를 다룬다.

## v3.1 핵심 철학

> **조용한 기본값 + 필요한 순간의 강조.**

하루안부는 정보 확인·돌봄 기록·경보 판단이 중요한 서비스다. UI는 예뻐 보이는 것보다 **읽히고 신뢰받는 것**이 우선이다. 따라서:

- **Flat이 기본**: 카드는 단단한 흰색 + 1px 보더 + 약한 shadow. Glass(반투명+blur)는 탭바·모달·특수 강조 한정.
- **그라디언트 절제**: 큰 면 배경은 매우 약한 tint. 강한 히어로 그라디언트는 화면당 최대 1개.
- **역할색 = accent**: 큰 면을 칠하는 테마색이 아니라, 버튼·활성 탭·작은 배지·포커스 링에만 쓰는 액센트.
- **상태색 ≠ 역할색**: 의료진 그린 accent와 success 그린은 시각적으로 분리(success는 -700 어두운 톤).
- **카드 타입 4종 고정**: default / action / alert / hero. 화면마다 카드 스타일을 고를 필요가 없게.
- **좌측 컬러 바(border-left) 패턴 금지**: 정보 강조는 `card-alert` 또는 flat tinted 배경으로만. 수직 컬러 라인 장식은 통일감을 깨고 어디에도 어울리지 않는다.

## v3.2.13 — 3앱 통일 라운드 결과 반영

> **임상 모바일(보호자·요양보호사·의료진) 디자인 시스템 1:1 정렬.**

3개 앱의 모바일 화면을 픽셀-퍼펙트 동일하게 만든 결과를 SoT 토큰·컴포넌트에 흡수했다:

- **모바일 헤더**: `<header class="header"><div class="top-nav">` 신표준. 홈은 flex space-between, 서브(`:has(.title-block)`)는 grid 44/1fr/44.
- **`.icon-btn`** 글라스 44×44 — 헤더 액션 / floating action 표준. `.notif-dot` 8×8 포함.
- **카드 elevation**: `.card` 기본 shadow → `--shadow-card-floating` (0 4px 12px / hairline). 3앱 마이페이지 통일.
- **임상 캔버스 토큰**: `--clinical-canvas` (#F4FAF6) + `--clinical-bg-image` (radial+linear gradient).
- **`.bottom-bar / .tab-wrap`** 임상 변형: 흰색 글라스 알약 탭바 + 64×64 SOS sibling.
- **상태 pill 5단계**: `.status-observe/watch/urgent/ready/pending`.
- **공통 애니메이션**: `haru-fade-in-up` (등장) · `haru-pulse` (라이브 dot) · `haru-ring` (GPS).
- **medical+mobile = caregiver 토큰**: 본문 18px / 터치 48px / 버튼 52px / row 60px (`[data-role="medical"|"nurse"|"doctor"][data-platform="mobile"]`).

---

## 1. 브랜드

### 1.1 이름과 의미

**하루안부 (Haru Anbu)** — "매일 안부를 묻다"
- 하루(日): 일상의 단위
- 안부(安否): 편안함과 그렇지 않음을 묻는 행위

슬로건: **"오늘 하루도, 안녕하셨습니다"** — 보고이자 인사가 되는 이중성이 브랜드의 핵심.

### 1.2 브랜드 퍼스낼리티

> 따뜻하지만 전문적인 — 안심을 디자인하다

| 속성 | 의미 | 시각·언어 표현 |
|---|---|---|
| 따뜻함 (Warm) | 가족에게 보내는 편지 | 둥근 모서리, 부드러운 그림자, ~요체 어미 |
| 전문성 (Professional) | 의료진이 신뢰할 수 있음 | 명확한 정보 위계, 정확한 수치 |
| 안심감 (Reassuring) | "오늘도 잘 계셔" | 딥 블루, 완료 그린, 충분한 여백 |
| 부드러움 (Soft) | 병원·키오스크 거부 | 글래스 카드, 라인 일러스트 |

### 1.3 포지셔닝

```
              따뜻함
                ↑
  캐주얼 ──────┼──────→ 전문적
        하루안부 ●     ← 유일한 사분면
                ↓
              차가움
```

기존 의료 SaaS는 전문/차가움(우하), 일반 케어 매칭 앱은 캐주얼/따뜻함(좌상). 하루안부는 전문/따뜻함(우상)을 잡는다.

### 1.4 보이스 & 톤

- **친근함**: -요, -어요 종결어미. "어머님", "보호자님" 호칭.
- **정확함**: 수치·시간 명확. 모호 표현 배제.
- **간결함**: 한 문장으로 핵심.
- **안심감**: 긍정 프레이밍. "완료" 보다 "잘 됐어요".

피해야 할 표현:
- 의료 용어 과다 — "투약/처치" → "약/케어"
- 기계적 어미 — "~하십시오" → "~해보세요"
- 불안 자극 — "주의/경고/실패" 남발 금지

벤치마킹 톤: **토스**(카드 UI + 시멘틱 컬러), **Apple Health**(4px 그리드), **당근마켓**(따뜻한 ~요체), **밀리의서재**(여백 미학).

### 1.5 액션 동사 매트릭스 (v3.2 신설)

Fluent 2의 Done/Finish/Close/Dismiss 컨벤션을 하루안부 한국어 톤에 맞춰 표준화. **컨텍스트별로 동사가 고정**되어야 사용자가 학습 부담 없이 한 화면에서 다음 화면을 예측할 수 있다.

#### 1.5.1 닫기 계열 (4종 구분)

| 동사 | 영문 매핑 | 사용 컨텍스트 | 예 |
|---|---|---|---|
| **닫기** | Close | 정보를 보고 닫는 모달·바텀시트·사이드 패널. **작업 결과 없음**. | 도움말 모달의 [닫기], 사이드 패널의 × |
| **취소** | Cancel | 진행 중인 입력·작업을 **버리고 이전으로**. | 폼 입력 중 [취소], 사진 첨부 후 [취소] |
| **확인** | OK / Acknowledge | 정보를 **봤다고 알림** (작업 결과 없음, 동의도 아님). | "기록이 저장되었어요" 다이얼로그의 [확인] |
| **돌아가기** | Back | 한 단계 **위 화면으로**. 헤더 좌측 chevron-left와 동일. | 단계형 폼의 [돌아가기] |

**금지 조합:**
- 모달에 [닫기]와 [취소]를 동시에 두지 않는다. 둘 중 하나만.
- "닫기"와 "확인"이 같은 의미일 때는 [확인] 우선 (긍정 표현).

#### 1.5.2 저장·완료 계열 (5종 구분)

| 동사 | 영문 매핑 | 사용 컨텍스트 | 예 |
|---|---|---|---|
| **저장** | Save | 작성 중인 콘텐츠를 보존. 다시 편집 가능. | 메모 [저장], 설정 [저장] |
| **완료** | Done | **편집 모드 종료** + 저장. 토글 상태로 돌아감. | 케어 체크리스트 [완료], 인수인계 [완료] |
| **확정** | Confirm | 되돌릴 수 없는 결정. | 결제 [확정], 약속 잡기 [확정] |
| **전송** | Send | 외부(다른 사용자·서버)로 보냄. | 메시지 [전송], AI 질문 [전송] |
| **제출** | Submit | 폼을 처리 시스템에 넘김 (검증·승인 흐름). | 본인 인증 [제출], 가입 신청 [제출] |

#### 1.5.3 부정·위험 계열 (3종 구분)

| 동사 | 영문 매핑 | 사용 컨텍스트 | 시각 |
|---|---|---|---|
| **삭제** | Delete | 콘텐츠 영구 삭제. 복구 가능성 명시 ("30일 내 복구 가능"). | `btn-destructive` (빨강) |
| **취소하기** | Cancel a thing | **예약/약속 등 외부 영향 있는 취소**. 단순 작업 취소가 아님. | `btn-destructive` 또는 보더 빨강 |
| **나가기** | Leave | 채팅방·그룹 등에서 본인만 나감. | `btn-secondary` + danger 텍스트 |

**금지:** [삭제]는 단독 클릭으로 실행 금지 — 항상 확인 모달 1단계 거침.

#### 1.5.4 시작·진행 계열 (3종 구분)

| 동사 | 영문 매핑 | 사용 컨텍스트 |
|---|---|---|
| **시작** | Start | 처음 진입. 온보딩 [시작], 영상 [시작] |
| **계속** | Continue | 중단된 흐름 이어서. 폼 중간 저장 후 [계속], 다음 단계 [계속] |
| **다시 시도** | Retry | 실패한 동작 재시도. 네트워크 오류 후 [다시 시도] |

#### 1.5.5 동사 + 명사 패턴

버튼 라벨은 **동사 + 명사** 권장 (의미 명확):

| 모호 | 권장 |
|---|---|
| 확인 | **메시지 보내기** / 저장 / 다음 |
| 등록 | **환자 등록** / **계정 만들기** |
| 변경 | **비밀번호 변경** / **사진 바꾸기** |
| 신청 | **본인 인증 제출** / **상담 예약** |

#### 1.5.6 강제 동의 모달 (KRDS 원칙 + Fluent)

강제 동의(법정 약관)는 닫기 버튼이 없고, **단일 액션** "동의하고 계속" 으로 고정.

| 컨텍스트 | 권장 라벨 |
|---|---|
| 법정 약관 (필수) | [동의하고 계속] |
| 선택 약관 | [동의] / [동의 안 함] 짝 |
| 본인 인증 | [본인 인증 제출] |
| 메디컬 면책 ("최종 판단은 의료진") | (액션 없음, 정보 표시만 — 닫기는 우상단 ×) |

---

## 2. 로고

### 2.1 자산 위치

[logo/brand-system/](logo/brand-system/)에 6종이 있다 (v3.1):

| 파일 | 용도 | viewBox |
|---|---|---|
| `01_심볼단독.svg` | 앱 아이콘 · 파비콘 · FAB · AI 진입점 (정사각 컨테이너) | 512×512 |
| `02_워드마크단독.svg` | 헤더 · 푸터 · 텍스트 위주 자리 | 220×56 |
| `03_콤비네이션_가로.svg` | **(기본) 일반 헤더 · 명함 · 발표자료 · 광고** | 360×96 |
| `04_콤비네이션_세로.svg` | 스플래시 · 온보딩 · 포스터 · 인쇄물 | 240×220 |
| `05_단색버전.svg` | 단색 인쇄 · 음각 · 워터마크 · 컬러 배경 위 | 512×512 |
| `06_콤비네이션_심플.svg` | **모바일 헤더 · 사이드바 상단 · 좁은 자리** (태그라인 없음, 24~48px 높이) | 200×48 |

### 2.2 컬러 규칙

- 메인 컬러: `--brand-blue-500` (#2C7AFC) — 로고 원색이자 보호자 테마 anchor.
- 컬러 버전 위 배경: 흰색 / `--color-bg-canvas` (#F0F4F8) / 매우 옅은 그라디언트만 허용.
- 그린·오렌지 배경 위에 로고를 올릴 때는 **단색 버전(흰색)** 을 사용. 컬러 로고를 의료진 그린/환자 오렌지 화면에 그대로 올리지 않는다.

### 2.3 최소 크기 & 여백

| 사용 자리 | 최소 크기 (높이) | 권장 자산 | 안전 여백 |
|---|---|---|---|
| 모바일 헤더 (44px) | 24~28px | `06_콤비네이션_심플` | 심볼 너비의 1/2 |
| 웹 헤더 (64px) | 32~40px | `03_콤비네이션_가로` | 심볼 너비의 1/2 |
| 명함 · 발표자료 | 48~60px | `03_콤비네이션_가로` | 심볼 너비의 1/2 |
| 사이드바 상단 | 28~32px | `06_콤비네이션_심플` | 심볼 너비의 1/4 |
| 심볼 단독 (FAB·아이콘) | 16px | `01_심볼단독` | 심볼 너비의 1/4 |
| 워드마크 단독 | 18px | `02_워드마크단독` | 'ㅎ' 글자 높이의 1/2 |
| 스플래시 · 온보딩 | 120~200px | `04_콤비네이션_세로` | 화면 너비의 1/4 이상 |

### 2.4 사용 금지 사례

- 로고 회전·기울임·왜곡 (절대 금지)
- 그라디언트 적용 (히어로 카드 가이드라인은 제품 컴포넌트 한정)
- 다른 색으로 변경 (단색 버전이 따로 있음)
- 글래스 카드 안쪽에 배치 — 마스코트와 마찬가지로 깨끗한 흰 또는 캔버스 표면 위에만
- 로고 옆에 다른 아이콘·이모지 병기

---

## 3. 컬러

### 3.1 컬러 모델 — "1 차체, 3 테마"

모든 화면은 **`--color-accent` 하나**의 anchor 토큰만 본다. `data-role`이 이 anchor 값을 바꾼다. 컴포넌트 코드는 절대 hex를 직접 적지 않는다.

| 역할 | data-role | accent | 용도 |
|---|---|---|---|
| 보호자 | `guardian` | `#2C7AFC` | 보호자앱 — iOS 딥블루, 신뢰·안심 |
| 의료진 | `medical` / `doctor` / `nurse` / `caregiver` | `#22C55E` | 의료진웹·요양보호사앱 — 케어 그린 |
| 환자 | `patient` | `#FB923C` | 환자앱 — 웜 오렌지 |

각 역할마다 4단계: `accent-soft` (배경/칩) / `accent` (기본) / `accent-strong` (Pressed) / `accent-on` (텍스트).

### 3.1.1 의료 보조 컬러 — Medical Blue (v3.2.4 신설)

의료진 메인은 그린(`#22C55E`)이지만 **진단·정보 카드·환자 상세 헤더** 같이 국제 표준 의료 톤이 어울리는 자리에는 Medical Blue를 보조로 쓴다 (UX MAX "Medical Clinic" 패턴 권장).

| 토큰 | 값 | 용도 |
|---|---|---|
| `--color-medical-info` | `#0369A1` (sky-700) | 진단·정보 헤더 텍스트·아이콘 |
| `--color-medical-info-soft` | `#BAE6FD` (sky-100) | 진단 정보 카드 배경 |
| `--color-medical-info-deep` | `#0C4A6E` (sky-900) | 강조 라인·강한 보더 |

#### 사용 규칙

- **의료진 웹·앱 한정**. 보호자·환자·요양보호사 화면에서는 사용 금지 (보호자 블루와 시각 충돌).
- 환자 상세 페이지 헤더, 진단 정보 박스, 검사 결과 카드 라벨 등 "객관 정보 표시" 자리에만.
- 액션 버튼·CTA는 그대로 의료진 그린 (`--color-accent`). Medical Blue는 **읽기 정보**용.

### 3.2 시멘틱 컬러 (상태)

| 상태 | 토큰 | 메인 | Soft (배경) | 사용처 |
|---|---|---|---|---|
| 정상/완료 | `--color-success` | `#16A34A` | `#DCFCE7` | 체크리스트 완료, "정상" 뱃지 |
| 주의 | `--color-warning` | `#F59E0B` | `#FEF3C7` | 미완료, 확인 필요 |
| 위험/긴급 | `--color-danger` | `#E32B25` (Rivian Alarm) | `#FEE2E2` | 긴급 알림 CTA·뱃지·삭제 액션 (SOS는 `--palette-red-600` `#C8231E` 직접 참조 — 위계 차) |
| 정보 | `--color-info` | accent와 alias | accent-soft | 일반 안내 — **역할 색을 따라간다** |
| 포인트 | `--color-point` | `#F5D310` | — | 별점, 중요 뱃지, 역할 무관 강조 1회용 |

핵심 원칙: **`--color-info`는 `--color-accent`의 별칭**이다. 의료진 화면에서 정보 알림은 자동으로 그린, 환자 화면에서는 자동으로 오렌지가 된다.

### 3.3 표면 (Surface)

| 토큰 | 값 | 용도 |
|---|---|---|
| `--color-bg-canvas` | `#F0F4F8` | 앱 전체 배경 (쿨 블루그레이) |
| `--color-bg-surface` | `#FFFFFF` | 단단한 카드, 모달 |
| `--color-bg-surface-muted` | `#FAFAFA` | 낮은 강조 카드 |
| `--color-bg-glass` | `rgba(255,255,255,0.75)` | 글래스 카드 — 기본 카드 표면 |
| `--color-bg-overlay` | `rgba(0,0,0,0.40)` | 모달 딤 |

### 3.4 텍스트

| 토큰 | 값 | 용도 |
|---|---|---|
| `--color-text-primary` | `#1C1C1E` | 본문, 헤드라인. 순흑 아닌 다크 |
| `--color-text-secondary` | `#8E8E93` | 캡션, 메타정보 |
| `--color-text-tertiary` | `#9E9E9E` | 비활성, placeholder |
| `--color-text-disabled` | `#D4D4D8` | disabled 텍스트 |
| `--color-text-on-accent` | `#FFFFFF` | accent 위 텍스트 |

### 3.5 보더

| 토큰 | 값 | 용도 |
|---|---|---|
| `--color-border-subtle` | `#E5E5EA` | 기본 1px 보더 |
| `--color-border-strong` | `#D4D4D8` | 강조 보더 (드뭄) |
| `--color-border-glass` | `rgba(255,255,255,0.55)` | 글래스 카드 프로스티드 하이라이트 |
| `--color-border-focus` | accent 별칭 | 포커스 링 |

### 3.6 역할 배경 그라디언트

각 역할의 페이지 상단을 부드럽게 물들인다.

| 역할 | 그라디언트 |
|---|---|
| 보호자 | `linear-gradient(180deg, #d4e4ff 0%, #e8f0fe 40%, #f2f6ff 70%, #EEF3FB 100%)` (4-stop, +radial glow) |
| 의료진 | `linear-gradient(180deg, #DCFCE7 0%, #F0F4F8 120px)` |
| 환자 | `linear-gradient(180deg, #FFEDD5 0%, #F0F4F8 120px)` |

보호자만 소프트 글로우 오버레이(`radial-gradient(circle, rgba(44,122,252,.14) 0%, transparent 65%)` + blur 30px) 추가 — 가디언 화면의 "분위기"를 만드는 시그니처.

### 3.7 히어로 그라디언트 (강조 카드 전용)

| 역할 | 그라디언트 |
|---|---|
| 보호자 | `linear-gradient(135deg, #2C7AFC 0%, #1E5FD6 100%)` |
| 의료진 | `linear-gradient(135deg, #22C55E 0%, #16A34A 100%)` |
| 환자 | `linear-gradient(135deg, #FB923C 0%, #EA580C 100%)` |

히어로 카드, AI 리포트 커버, 강조 CTA 한정. 일반 카드는 절대 그라디언트 사용 금지.

### 3.8 접근성 대비

- 본문 텍스트 / 배경: WCAG AA 4.5:1 이상
- 큰 텍스트(18px+) / 배경: 3:1 이상
- UI 컴포넌트 / 배경: 3:1 이상
- 환자 화면 고대비 모드(`data-a11y-contrast="high"`): 본문 7:1 (KRDS 매직 90)

### 3.9 명도 매직넘버 사다리 (v3.2 신설 · KRDS 차용)

KRDS의 명도 매직넘버(40/50/70/90)는 "컨텍스트별 명도가 자동으로 시각적 위계를 만든다"는 강점이 있다. 하루안부의 그레이 스케일을 매직넘버 별칭으로 통일.

| 별칭 | 값 | 의미 | 사용처 |
|---|---|---|---|
| `--neutral-10` | `#FFFFFF` | 가장 밝은 표면 | 카드, 시트 |
| `--neutral-40` | `#F0F4F8` | 페이지 배경 | body, page canvas |
| `--neutral-50` | `#E5E5EA` | 약한 디바이더 | 보더, 디바이더 |
| `--neutral-70` | `#8E8E93` | 보조 텍스트 | 캡션, placeholder |
| `--neutral-90` | `#1C1C1E` | 본문 텍스트 | 4.5:1 보장 |
| `--neutral-strong` | `#0A0A0C` | 환자 고대비 | 7:1 (KRDS magic 90) |

#### 활용 규칙

- **본문 = 90 / 보조 = 70 / 보더 = 50 / 배경 = 40** 사다리 외 명도 사용 금지.
- 강조 텍스트는 `--color-accent` 또는 `--color-text-primary` 사용. 임의 명도(`-60`, `-80` 등) 신설 금지.

---

## 4. 타이포그래피

### 4.1 서체

**Pretendard Variable** 단일. 한글·영문·숫자 모두.

```css
font-family: 'Pretendard Variable', 'Pretendard',
             -apple-system, BlinkMacSystemFont,
             'Helvetica Neue', 'Segoe UI', Roboto, sans-serif;
```

- CDN: `https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css`
- 모노: `ui-monospace, 'SF Mono', Menlo, Consolas, monospace` — 디버그·코드블록 한정.
- 영문 전용 컨텍스트면 Inter도 허용하지만 운영 화면은 한국어 우선.

### 4.2 타입 스케일

| 토큰 | 크기 | 굵기 | line-height | 사용처 |
|---|---|---|---|---|
| `--text-display` | 32px | 600 | 1.2 | 화면 대제목, 큰 숫자 |
| `--text-title` | 22px | 600 | 1.2 | 섹션 헤더, 모달 제목 |
| `--text-headline` | 17px | 600 | 1.4 | 카드 제목, 리스트 행 제목, 버튼 라벨 |
| `--text-body` | 16px | 400 | 1.4 | 본문 (보호자/의료진) |
| `--text-body-lg` | 18px | 400 | 1.6 | 환자 본문, AI 리포트 |
| `--text-callout` | 14px | 400 | 1.4 | 부제, 인풋 텍스트 |
| `--text-caption` | 13px | 400 | 1.4 | 타임스탬프, 메타 |
| `--text-mini` | 11px | 400 | 1.2 | 뱃지, 마이크로 라벨 |

탭바 라벨(11px / 700)은 예외적으로 700 굵기 — 작은 글자에서 활성 상태 색 대비를 유지하기 위함.

### 4.3 환자 자동 상향

`data-role="patient"` 화면은 토큰 자체가 자동 상향된다 (분기 코드 없이):
- `--text-body` → 18px
- `--text-headline` → 20px
- `--text-title` → 24px

### 4.4 굵기 사다리

400 (Regular) / 500 (Medium·드뭄) / 600 (SemiBold·헤드라인) / 700 (Bold·탭바 라벨 한정).

- **300은 금지** — 한글이 글래스 표면에서 흐릿하게 읽힌다.
- **800·900도 사용 금지** — 브랜드 톤은 "강조"가 아닌 "안정".
- 디스플레이 사이즈에 negative tracking(자간 좁힘) 적용 금지 — 한글 균형이 깨진다.

### 4.5 행간 사다리

- Tight (1.2): 헤딩, 큰 숫자
- Normal (1.4): 본문 기본
- Relaxed (1.6): 환자 본문, AI 리포트, 긴 설명문

### 4.6 다국어 (i18n)

하루안부는 한국어 우선이지만 일부 역할은 외국인 사용자가 많다.

| 역할 | 1차 언어 | 추가 지원 | 폰트 전략 |
|---|---|---|---|
| 보호자 | 한국어 | 영문 (메뉴 라벨) | Pretendard 단독으로 충분 |
| 의료진 | 한국어 | 영문 (의료 용어) | Pretendard 단독 |
| **요양보호사** | 한국어 | **중국어 간체**, 영문 | **Pretendard + Noto Sans SC** |
| 환자 | 한국어 | — | Pretendard 단독 |
| 온보딩 | 한국어 | — | Pretendard 단독 |

#### Pretendard의 한계

Pretendard는 한글·라틴·숫자·기본 문장부호만 커버. **중국어(CJK Han)·일본어(가나)는 포함하지 않는다.** Pretendard가 없는 글자에 대해서는 폰트 폴백 chain이 시스템 폰트로 떨어져 글자 인식은 되지만 한글 본문과 시각적으로 따로 놀 수 있다.

#### 해결 — Noto Sans SC 폴백

`tokens.css`의 `--font-family-base`는 다음 chain으로 정의되어 있다:

```css
'Pretendard Variable', 'Pretendard',
'Noto Sans SC', 'Noto Sans',
-apple-system, BlinkMacSystemFont,
'Helvetica Neue', 'Segoe UI', Roboto, sans-serif;
```

- 한글·영문: Pretendard가 처리
- 중국어: Noto Sans SC가 처리 (브라우저가 unicode 범위로 자동 선택)
- 일본어: -apple-system / Segoe UI가 시스템 가나 폰트로 처리

#### 요양보호사앱 — Noto Sans SC 다운로드

다른 앱은 chain만 길고 Noto Sans를 다운로드하지 않는다 (한국어 본문에 Pretendard만 적용되므로). 요양보호사앱은 자체 HTML `<head>`에서 명시적으로 Noto Sans SC를 다운로드:

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;600;700&display=swap">
```

가중치는 Pretendard와 동일(400/500/600/700) 4단계만 받아 페이로드를 줄인다 (~150KB 추가).

#### 다국어 본문 작성 가이드

- 한 문장 안에서 한·중·영 혼용 가능 — 폰트 chain이 자동 처리.
- 중국어 본문은 Pretendard와 시각적 균형이 약간 다를 수 있음. 본문 사이즈는 통일하되 line-height는 1.5 이상 권장 (한글 1.4보다 0.1 여유).
- 라벨/버튼 같은 짧은 UI 텍스트는 일관성 유지를 위해 **번역키 + ICU 메시지** 사용 권장 (구현 시점 결정).
- 중국어 본문에는 **번체(TC) 보다 간체(SC)** 우선 — 중국·동남아 출신 보호사 대상.

#### 향후 추가 가능

- 베트남어: Latin 글자라 Pretendard 라틴 fallback이 처리, 추가 폰트 불필요.
- 태국어·아랍어: 별도 Noto 변형 필요. 현재 v3.0 미지원.

---

## 5. 간격 (Spacing)

### 5.1 4px 그리드

모든 간격은 4의 배수. 2px(`--space-1`)는 인라인 아이콘 패딩 미세조정 한정.

| 토큰 | 값 |
|---|---|
| `--space-1` | 2px |
| `--space-2` | 4px |
| `--space-3` | 8px |
| `--space-4` | 12px |
| `--space-5` | 16px |
| `--space-6` | 20px |
| `--space-7` | 24px |
| `--space-8` | 32px |
| `--space-9` | 40px |
| `--space-10` | 48px |
| `--space-11` | 64px |
| `--space-12` | 96px |

### 5.2 시멘틱 간격 (의도 기반)

직접 `--space-N`을 쓰는 대신 의미를 가진 별칭 사용 권장:

- **Inset** (컴포넌트 내부 패딩) — `--space-inset-compact` 8px / `--space-inset-default` 16px / `--space-inset-loose` 24px
- **Stack** (세로 간격) — `--space-stack-tight` 4px / `--space-stack-default` 12px / `--space-stack-loose` 24px / `--space-stack-section` 32px
- **Inline** (가로 간격) — `--space-inline-tight` 4px / `--space-inline-default` 8px / `--space-inline-loose` 16px

### 5.3 페이지 마진

- 모바일: `--space-page-margin` = 16px (양쪽)
- 웹: `--space-page-margin` = 24px (양쪽), 본문 max-width 1280px

`data-platform`이 자동 오버라이드하므로 화면 코드는 토큰만 본다.

### 5.4 화면 리듬

- 카드 내부 padding: 16px (기본) / 24px (히어로)
- 리스트 행 간격: 12px
- 카드 간격: 24px
- 섹션 간격: 32px
- 메이저 블록: 48px

---

## 6. 형태 (Shape — Border Radius)

| 토큰 | 값 | 사용처 |
|---|---|---|
| `--radius-0` | 0 | 풀-블리드 이미지, 디바이더 |
| `--radius-1` | 4px | 마이크로 태그 |
| `--radius-2` | 8px | 인풋, 칩, 작은 뱃지 |
| `--radius-3` | 12px | 인라인 카드, 보조 표면 |
| `--radius-4` | 14px | **카드 기본·버튼 기본** (브랜드 시그니처 라운드) |
| `--radius-5` | 18px | 글래스 카드, 모달 |
| `--radius-6` | 24px | 히어로 카드 |
| `--radius-7` | 28px | 바텀시트 (위 모서리만) |
| `--radius-full` | 9999px | 탭바, 뱃지, FAB, 모드 칩 |

시멘틱 별칭:
- `--radius-control` = 8px (인풋)
- `--radius-button` = 14px
- `--radius-card` = 14px
- `--radius-card-lg` = 18px
- `--radius-modal` = 18px
- `--radius-hero` = 24px
- `--radius-pill` = 9999px

### 6.1 형태 원칙

- 직각 카드(0~4px) 금지. 최소 8px.
- 원형(`pill`)은 탭바·뱃지·FAB 등 명확히 "둥글어야 하는 것"만.
- 사이 값(예: 16px, 20px) 사용 금지 — 사다리 외 값은 시각적 일관성을 깬다.

---

## 7. 고도 (Elevation — Shadow & Blur)

### 7.1 그림자 사다리

| 토큰 | 값 | 사용처 |
|---|---|---|
| Flat | 그림자 없음 | 인라인 텍스트, 본문 |
| `--shadow-1` | `0 1px 4px rgba(0,0,0,0.06), 0 0 1px rgba(0,0,0,0.04)` | 일반 카드 |
| `--shadow-2` | `0 4px 16px rgba(0,0,0,0.08)` | 중요 카드, 버튼 그룹 |
| `--shadow-3` | `0 8px 28px rgba(0,0,0,0.12)` | 히어로 카드, 모달 |
| `--shadow-glass` | `0 4px 20px rgba(0,0,0,0.08), inset 0 1px 0 rgba(255,255,255,0.35)` | 탭바·FAB·글래스 표면 (인셋 하이라이트가 글래스 시그니처) |

### 7.2 그림자 철학

- 모든 그림자는 **부드럽고 따뜻**: rgba(0,0,0,0.06–0.12). 0.20 이상은 금지.
- 임상 EMR·금융 앱의 다층 강한 그림자 거부.
- 유일한 강한 그림자는 **히어로 액센트 그림자** — 역할 컬러를 25% alpha로 떨어뜨려 카드에 색 블룸을 입힘.

| 역할 | 히어로 그림자 |
|---|---|
| 보호자 | `0 8px 28px rgba(44,122,252,0.25)` |
| 의료진 | `0 8px 28px rgba(34,197,94,0.25)` |
| 환자 | `0 8px 28px rgba(251,146,60,0.25)` |

### 7.3 블러 (Backdrop Filter)

| 토큰 | 값 | 사용처 |
|---|---|---|
| `--blur-card` | 20px | 글래스 카드 (실제 사용은 16px로 조정 가능) |
| `--blur-tab` | 24px | 플로팅 탭바 |
| 모달 | 40px | 바텀시트 |
| 헤더 | 12px | 모바일 sticky 헤더 |

블러 + 인셋 하이라이트가 합쳐져 "이건 페인트가 아니라 유리" 라는 시각 신호를 만든다.

### 7.4 저전력 / 투명도 감소 폴백 (v3.2 신설)

iOS Safari 저전력 모드, Windows "투명 효과 끄기", macOS "투명도 줄이기" 등에서 `backdrop-filter`가 비활성된다. 이 상태에서 글래스 표면은 반투명 채로 본문이 비쳐 가독성이 깨진다.

#### 자동 폴백 (tokens.css에 이미 적용)

```css
@media (prefers-reduced-transparency: reduce) {
  /* 글래스 alpha → 0.97로 강화, blur → 0 */
  /* 글래스 4곳(탭바·모달·AI·가족사진) 모두 backdrop-filter: none */
}
```

#### 수동 폴백 — `.no-blur` 헬퍼 클래스

JS에서 저전력 감지(예: iOS Battery Saver) 시 `<html>`에 `.no-blur` 추가하면 모든 글래스가 단단한 surface로 폴백.

```js
// 예시 — 배터리 < 20% 또는 사용자 토글 시
if (battery.level < 0.2 || userPrefersHighOpacity) {
  document.documentElement.classList.add('no-blur');
}
```

#### 폴백 시 시각

- 탭바: 반투명 흰색 → 단단한 흰색 + 강화된 그림자
- 모달 sheet: 반투명 + blur → 단단한 흰색
- AI 카드: 변화 없음 (원래 flat surface)
- 환자 가족사진 카드: 글래스 → 단단한 흰색

---

## 8. 모션 (Motion)

### 8.1 지속시간 토큰

| 토큰 | 값 | 사용처 |
|---|---|---|
| `--motion-micro` (= `--duration-fast`) | 150ms | 버튼 누름, 토글 |
| `--motion-transition` (= `--duration-normal`) | 250ms | 카드 펼침, 탭 전환 |
| `--motion-enter` (= `--duration-slow`) | 350ms | 모달 등장, 화면 전환 |

### 8.2 이징

- `--easing-standard`: `cubic-bezier(0.2, 0, 0, 1)` — 기본
- `--easing-emphasize`: `cubic-bezier(0.2, 0, 0, 1.2)` — 살짝 오버슈트, 등장 강조

### 8.3 표준 애니메이션

```css
/* 카드 등장 */
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(16px); }
  to   { opacity: 1; transform: translateY(0); }
}
/* 적용: animation: fadeInUp 300ms var(--easing-standard) forwards; */

/* 버튼 프레스 (universal feedback) */
.btn:active {
  transform: scale(0.98);
  opacity: 0.8;
  transition: 150ms var(--easing-standard);
}
```

### 8.4 모션 원칙

- 모션은 **정보 전달을 돕는 것**. 장식 모션은 브랜드 신뢰를 깎는다.
- `prefers-reduced-motion: reduce` 미디어 쿼리에서 모든 애니메이션 0.01ms로 단축 (tokens.css에 이미 적용).
- 카드 진입은 50ms 순차 딜레이로 리스트 stagger.

### 8.5 상태 (Hover · Active · Selected · Focus — v3.2 신설)

v3.1까지는 "호버 문서화 안 함"이 원칙이었으나, **의료진 웹은 마우스가 주 입력**이라 hover 없이는 클릭 가능 영역 식별이 어렵다. v3.2에서 `data-platform="web"`에 한해 상태 토큰을 정식화한다.

| 상태 | 토큰 | 라이트 | 다크 | 적용처 |
|---|---|---|---|---|
| Hover | `--state-hover-overlay` | rgba(0,0,0,0.04) | rgba(255,255,255,0.06) | 카드·리스트 행·메뉴 아이템 |
| Hover (accent) | `--state-hover-accent` | rgba(34,197,94,0.08) | (역할별 RGB 자동) | accent 버튼·탭 hover |
| Active (mouse down) | `--state-active-overlay` | rgba(0,0,0,0.06) | rgba(255,255,255,0.10) | 클릭 순간 |
| Selected | `--state-selected-bg` | accent-soft | accent-soft | 사이드바 활성, 선택된 행 |
| Focus | (focus ring 별도) | — | — | `:focus-visible` 사용, hover와 독립 |

#### 8.5.1 모바일에서는 정의 안 함

`data-platform="mobile"`에서는 hover 토큰을 정의하지 않는다 — 터치는 직접 누르고, hover는 stuck-hover 문제를 일으킨다. 모바일은 `:active` + `transform: scale(0.98)` 피드백만.

#### 8.5.2 적용 패턴

```css
/* 의료진 웹 카드·리스트 행 (data-platform="web"에서만) */
[data-platform="web"] .card-action:hover {
  background: linear-gradient(var(--state-hover-overlay), var(--state-hover-overlay)),
              var(--color-bg-surface);
  border-color: var(--state-hover-border);
}
[data-platform="web"] .card-action:active {
  background: linear-gradient(var(--state-active-overlay), var(--state-active-overlay)),
              var(--color-bg-surface);
}
[data-platform="web"] .sidebar__nav-item:hover {
  background: var(--state-hover-overlay);
}
[data-platform="web"] .sidebar__nav-item.is-active {
  background: var(--state-selected-bg);
  color: var(--color-accent);
}
```

#### 8.5.3 hover 금지 자리

- 환자·요양보호사·보호자 모바일 앱 전반
- 탭바 (모바일·웹 공통 — 탭바는 항상 터치 모델 따름)
- SOS Banner, Toast (인터랙티브 아니거나 즉시 닫힘)
- Disabled 요소 (hover 시 cursor만 not-allowed)

---

## 9. 아이콘 (Iconography)

### 9.1 라이브러리 — Microsoft Fluent Icons (Filled)

```html
<script src="https://cdn.jsdelivr.net/npm/iconify-icon@2.3.0/dist/iconify-icon.min.js"></script>
<iconify-icon icon="fluent:home-24-filled"></iconify-icon>
```

- **Filled 단일 사용**. Outline / Regular 절대 혼용 금지.
- 사이즈 variant: `-16-filled` / `-20-filled` / `-24-filled` / `-28-filled`.
- 컬러는 `currentColor` 상속. CSS `color`로 제어.

### 9.2 사이즈 매핑

| 컨텍스트 | variant | 렌더 크기 |
|---|---|---|
| 탭바 (모바일) | `-24-filled` | 24px |
| 헤더, 주요 버튼 | `-24-filled` | 24px |
| 웹 사이드바 | `-24-filled` | 24px |
| 인라인 리스트 행 | `-20-filled` | 20px |
| 칩, 마이크로 뱃지 | `-16-filled` | 16px |
| 히어로, 빈 상태 | `-28-filled` 이상 | 28~48px |

토큰: `--size-icon-sm` 20px / `--size-icon-md` 24px / `--size-icon-lg` 28px / `--size-icon-xl` 32px.

### 9.3 핵심 아이콘 매핑

| 용도 | 아이콘 |
|---|---|
| 홈 (탭바) | `fluent:home-24-filled` |
| 케어 가이드 | `fluent:clipboard-task-list-ltr-24-filled` |
| 소통/채팅 | `fluent:chat-24-filled` |
| 기록 | `fluent:document-text-24-filled` |
| 마이/프로필 | `fluent:person-24-filled` |
| 알림 | `fluent:alert-24-filled` |
| 투약/약 | `fluent:pill-24-filled` |
| 식사 | `fluent:food-24-filled` |
| 심박/건강 | `fluent:heart-pulse-24-filled` |
| 활동 | `fluent:accessibility-24-filled` |
| AI 진입점 | **하루안부 심볼** (`logo/brand-system/01_심볼단독.svg`) — Fluent 아이콘 대신 브랜드 심볼 사용 |
| 전송 | `fluent:send-24-filled` |
| 긴급/사이렌 | `fluent:siren-24-filled` |
| 검색 | `fluent:search-24-filled` |
| 설정 | `fluent:settings-24-filled` |
| 닫기 | `fluent:dismiss-24-filled` |
| 뒤로 | `fluent:chevron-left-24-filled` |
| 더보기 | `fluent:more-horizontal-24-filled` |

### 9.4 AI 아이콘 = 하루안부 심볼 (브랜드 결정)

AI 진입점은 다른 일반 아이콘처럼 Fluent에서 가져오지 않는다. **하루안부 심볼([logo/brand-system/01_심볼단독.svg](logo/brand-system/01_심볼단독.svg))을 그대로 사용**한다 — 브랜드 자체가 "매일 안부를 묻는 AI"를 상징하기 때문이다. 사용 위치:

- AI FAB (탭바 옆 원형 버튼)
- AI 어시스턴트 챗 진입점
- AI 리포트 카드 좌상단 마크
- AI 추천/제안 메시지 좌측 마크

크기: 컨테이너 사이즈에 맞춰 24~48px. FAB 안에 들어갈 때는 흰색 단색 버전(`05_단색버전.svg`)으로.

### 9.5 금지 사항

- **이모지 절대 금지** — Unicode emoji (스마일·체크·약·청진기 등 어떤 종류든) 일체 사용 안 함. 모두 fluent 아이콘 또는 하루안부 심볼로 대체.
- 다른 아이콘 라이브러리 혼용 금지 (Lucide, Phosphor, Tabler, Material Symbols).
- Filled / Outline 토글로 활성 상태 표현 금지 — 색만 바꾼다.
- 커스텀 SVG는 **로고 자산 + AI 심볼 한정**. 일반 UI 아이콘은 Fluent에서 가져온다.

---

## 10. 접근성

### 10.1 터치 타겟

| 플랫폼·역할 | 최소 크기 |
|---|---|
| 모바일 (보호자/의료진/요양) | 44 × 44px (iOS HIG) |
| 모바일 (환자) | 56 × 56px |
| 웹 (마우스) | 36 × 36px |

`data-role="patient"`는 토큰이 자동으로 56px 상향. 화면 코드는 분기하지 않는다.

### 10.2 색 대비 (반복 강조)

- 본문 4.5:1, 큰 텍스트 3:1.
- **색상에만 의존 금지** — SOS는 빨강 + 사이렌 아이콘 + "긴급" 텍스트의 **3중** 표현.
- 환자 화면은 모든 아이콘에 텍스트 라벨 병기.

### 10.3 포커스 링

```css
:focus-visible {
  outline: none;
  box-shadow: 0 0 0 2px var(--color-border-focus);
  border-radius: var(--radius-control);
}
```

`--color-border-focus`는 `--color-accent` 별칭 → 자동으로 역할 컬러 따라간다.

### 10.4 ARIA 기본

- 모든 아이콘 버튼 `aria-label` 필수.
- 토글 `role="switch"` + `aria-checked`.
- 모달 진입 시 포커스 트랩, ESC 닫기 지원.
- SOS 배너 `role="alert"` + `aria-live="assertive"`.
- 탭바 `role="tablist"`, 각 탭 `role="tab"` + `aria-selected`.

### 10.5 환자 추가 규칙 (강화)

`data-role="patient"` + `data-platform="mobile"` 조합은 토큰이 자동으로 다음을 적용한다 — **분기 코드 작성 금지**.

| 토큰 | 환자 값 |
|---|---|
| `--text-body` | 18px (vs 16px 기본) |
| `--text-headline` | 20px (vs 17px 기본) |
| `--text-title` | 24px (vs 22px 기본) |
| `--size-touch-target` | 56px (vs 44px 기본) |
| `--size-button-default` | 56px (vs 48px 기본) |
| `--size-row` | 64px (vs 56px 기본) |
| `--card-padding` | 20px (vs 16px 기본) |

#### 화면 구조 규칙

자동 토큰 외에도 다음 규칙을 환자앱은 추가로 따른다:

- **첫 화면 CTA 1~2개만 노출** — 선택지 5개 이상은 인지 부담. 핵심 행동 한두 개로 좁힌다.
- **아이콘 단독 금지** — 모든 주요 액션은 아이콘 + 한국어 라벨 병기. 휴대전화 아이콘만 보여주지 말고 "전화 걸기" 글자 함께.
- **상태 문구는 짧고 직접적** — "현재 처리 중인 작업이 있습니다" 가 아니라 "지금 보내고 있어요".
- **카드 수 제한** — 한 화면에 카드 5개 이상 쌓지 않는다. 스크롤 부담을 줄인다.
- **색 단독 의존 금지** — SOS는 빨강 + 사이렌 아이콘 + "긴급" 텍스트의 3중. 색맹·시각 차이 사용자에게도 의미 전달.
- **글래스보다 plain 흰 카드 우선** — 가독성 최우선. 글래스는 가족 사진처럼 감성 자료에만 제한.
- **1.6 행간으로 가독성 확보** — `--leading-relaxed` 자동 적용.
- **버튼 라벨은 SemiBold(600) 이상** — 작은 화면에서도 읽힌다.

### 10.6 접근성 모드 토글 (v3.2 신설)

환자앱 설정 페이지에서 사용자가 직접 활성화하는 접근성 모드 2종. 보호자/요양보호사도 시니어 사용자 대비 활성 가능 (역할 무관).

| 모드 | 속성 | 효과 |
|---|---|---|
| **글자 크게** | `data-a11y-text="large"` | 본문 20px (환자 기본 18보다 한 단계 위), 터치 60px |
| **고대비** | `data-a11y-contrast="high"` | 본문 7:1 (`--neutral-strong`), 글래스 효과 비활성 |

```html
<html lang="ko" data-role="patient" data-platform="mobile"
      data-a11y-text="large" data-a11y-contrast="high">
```

#### 토글 UI (환자앱 설정 페이지)

```
┌──────────────────────────────────┐
│  화면 설정                          │
├──────────────────────────────────┤
│  글자 크게      [ ○ ── ]           │ ← 토글 (기본 OFF)
│   본문이 더 크게 표시돼요             │
│                                    │
│  고대비         [ ○ ── ]           │ ← 토글 (기본 OFF)
│   글자와 배경 대비를 강하게 해요      │
│                                    │
│  화면 읽어주기   [ ── ● ]           │ ← TTS 토글 (기본 ON)
│   AI 응답을 음성으로도 들려드려요    │
└──────────────────────────────────┘
```

#### 보이스 우선 (TTS·STT)

환자앱은 **보이스가 1차 입력·출력**이다. AI 컴포넌트 H1 Prompt Input의 음성 모드는 환자앱에서 기본 활성, H2 Prompt Output은 카드 우측에 스피커 아이콘 → 탭 시 TTS로 읽어준다.

| 보이스 기능 | 상태 |
|---|---|
| 음성 입력 (STT) | 모든 텍스트 필드에 마이크 아이콘 (환자앱 기본) |
| 음성 출력 (TTS) | AI 응답·알림 라벨 → 스피커 아이콘 탭으로 재생 |
| 자동 읽기 | 새 알림 도착 시 화면이 깨어 있다면 자동 TTS (사용자 토글 가능) |

음성 처리는 Web Speech API 우선, 미지원 환경에서는 외부 TTS 서비스 호출.

#### 규칙

- 토글 활성 상태는 localStorage 보존 → 다음 진입부터 자동 적용.
- 토글 변경 시 즉시 화면 반영 (페이지 리로드 없이 — CSS 변수만 변경).
- "글자 크게 + 고대비" 동시 활성 가능 (서로 독립적인 속성).
- 의료진 웹은 이 모드 비활성 — dense 정보 밀도가 우선.

---

## 11. 플랫폼 매트릭스

| 역할 | 플랫폼 | data-role | data-platform | 비고 |
|---|---|---|---|---|
| 보호자 | 모바일 PWA | `guardian` | `mobile` | 4-stop 그라디언트 + 글로우 |
| 의사 | 데스크톱 웹 | `doctor` | `web` | 사이드바 240px |
| 간호사 | 데스크톱 웹 | `nurse` | `web` | 의사와 동일 테마 |
| 요양보호사 | 모바일 PWA | `caregiver` | `mobile` | 의료진 그린 공유, 한 손 조작 |
| 환자 | 모바일 PWA | `patient` | `mobile` | 18px 본문, 56px 터치 자동 |
| 온보딩 | 모바일 PWA | (역할 선택 전) | `mobile` | 기본값 보호자 블루 |

---

## 12. 변경 / 미정의 영역

### 12.1 미정의 (v3.2 시점)

- **다크 모드** — v3.2에서 한 번 도입했으나 v9.5 시대 페이지의 hex 충돌로 봉인. 정책상 **하루안부는 라이트 단일**로 운영 (사용자 결정, 2026-05-11).
- **폼 검증 다중 에러** — 단일 에러는 정의됨, 비동기 검증 스피너·다중 메시지 패턴 미정 (P1 #8 후속).
- **알림 통합 체계** — 인앱·푸시·배너·토스트 4채널 통합 우산 미정 (P1 #6 후속).
- **저전력 모드 폴백** — Safari low-power에서 backdrop-filter 비활성 시 처리 정책 미정 (P2 #14 후속).

### 12.2 다음 버전 후보

- 일러스트 시스템 (현재는 마스코트만, Empty State 일러스트 사양 부족) — P2 #13 후속.
- 로딩 스켈레톤 표준 — 회색 블록 우선 권장하지만 토큰 미정 — P2 #12 후속.
- ~~차트·시각화 컬러 팔레트~~ — **v3.2에서 P0 #4로 정의** (§14 참조).

---

## 13. ~~다크 모드~~ (v3.2.8 제거 — 라이트 단일 운영)

> **결정 (2026-05-17, v3.2.8):** 하루안부는 **라이트 모드 단일**. 다크 모드는 v3.2에서 도입했으나 v9.5 시대 페이지의 hex 직접 사용과 충돌하며 깨진 화면("글자 안 보임", "반은 라이트 반은 다크")을 노출. v3.2.3에서 일단 봉인했고, v3.2.8에서 **코드 자체를 삭제**(`tokens.css` THEME D, `_app-theme.js`의 `setTheme`/`isDark`, `_preview-controls.js`의 강제 라이트 + 토글 바인딩, `_preview-shared.css`의 `[data-theme="dark"]` 보강 분기).
>
> 신규 페이지는 `data-theme` 속성 자체를 쓰지 않는다. 라이트가 기본값. `prefers-color-scheme: dark`도 무시한다 — 사용자 OS 설정과 무관하게 항상 라이트로 렌더된다.

---

## 14. 데이터 시각화 (v3.2 신설)

하루안부의 차트는 의료/돌봄 데이터를 다룬다 — 색 자체가 의미를 갖는다. 따라서 차트 색 사다리는 **역할 accent와 독립적**이다 (역할이 바뀐다고 "정상" 색이 바뀌면 안 된다).

### 14.1 8단계 카테고리 팔레트 (색맹 안전)

Okabe-Ito 색맹 안전 팔레트를 하루안부 톤에 맞춰 변형한 8단계. 시리즈가 많은 차트(예: 환자별 비교)에서 인덱스 순서대로 할당.

| 토큰 | 값 | 시그니처 |
|---|---|---|
| `--chart-1` | `#2C7AFC` | 보호자 블루 — 메인 라인 |
| `--chart-2` | `#22C55E` | 의료진 그린 |
| `--chart-3` | `#F59E0B` | 앰버 |
| `--chart-4` | `#8B5CF6` | 바이올렛 |
| `--chart-5` | `#EC4899` | 핑크 |
| `--chart-6` | `#14B8A6` | 틸 |
| `--chart-7` | `#F97316` | 오렌지 |
| `--chart-8` | `#64748B` | 슬레이트 — 평균선·기타 |

### 14.2 의미 기반 별칭 (의료/돌봄 도메인)

카테고리 차트가 아닌 **상태 데이터**(정상/주의/위험)는 다음 별칭을 쓴다 — 무지개 색 의존 금지.

| 토큰 | 값 | 의미 |
|---|---|---|
| `--chart-positive` | `#16A34A` | "정상", "완료", "달성" 시리즈 |
| `--chart-attention` | `#F59E0B` | "주의", "미완료", "확인 필요" |
| `--chart-critical` | `#C8231E` (Rivian Alarm 600) | "위험", "이상치", "긴급" |
| `--chart-baseline` | `#9E9E9E` | "평균", "기준선" — **dashed** 표현 |
| `--chart-prediction` | `#93C5FD` | "예측", "추세선" — **dashed** 표현 |

### 14.3 차트 구조 토큰

| 토큰 | 값 | 용도 |
|---|---|---|
| `--chart-grid` | border-subtle | 그리드 라인 (매우 약하게) |
| `--chart-axis` | text-tertiary | 축 라벨 |
| `--chart-bar-radius` | 4px | 막대 모서리 — 너무 둥글면 데이터 왜곡 |
| `--chart-line-width` | 2px | 기본 라인 |
| `--chart-line-width-bold` | 3px | 강조 라인 (선택된 시리즈) |
| `--chart-dot-size` | 8px | 데이터 포인트 점 |
| `--chart-dot-size-lg` | 12px | 강조 포인트 (이상치, 마지막 점) |

### 14.4 사용 규칙

- **차트 안 색 외에 패턴/모양 보조 필수** — 색맹 사용자에게도 시리즈 구분이 되도록 (라인 차트: solid/dashed/dotted 3종 / 막대 차트: 패턴 fill 옵션).
- **카테고리 개수 ≤ 8개**. 9개 이상이면 차트 분할 또는 "기타" 그룹화.
- **`chart-positive`·`chart-attention`·`chart-critical`은 카테고리 시리즈에 쓰지 않는다** — 사용자가 무의식적으로 "이게 위험한 데이터구나" 라고 오해.
- **평균선·예측선은 dashed**로 — 실측치와 시각적으로 분리.
- **차트 안 텍스트는 `--chart-axis` 한 색만**. accent 컬러로 라벨 칠하지 않는다.
- **차트 배경은 transparent** — 카드 안에 들어가므로 카드 surface를 그대로 활용.
- 환자앱 차트는 **고대비 모드(`data-a11y-contrast="high"`) 자동 반영** — 라인 굵기 `--chart-line-width-bold` (3px), 포인트 12px.

### 14.5 추천 라이브러리

- 모바일: **Recharts** (React) / **uPlot** (성능 우선) / **순수 SVG**(간단한 막대·도넛).
- 의료진 웹: **Apache ECharts** (의료 데이터 양 많을 때) / **D3.js** (커스텀).
- Chart.js·Highcharts는 채택하지 않음 — 토큰 매핑이 까다롭다.

---

## 15. 일러스트 시스템 (v3.2 신설)

마스코트(하루)는 이미 정의돼 있으나 Empty State·온보딩·에러 화면에서 쓰는 일반 일러스트 사양이 부족했다. v3.2에서 통일.

### 15.1 일러스트 3종 분류

| 종류 | 용도 | 표현 |
|---|---|---|
| **마스코트 (하루)** | 브랜드 톤·온보딩 환영·완료 축하 | 풀 컬러, 라인 + 채움 |
| **라인 일러스트** | Empty State·오류·일반 안내 | 2px 단색 스트로크, 라운드 캡 |
| **스폿 일러스트** | 마이크로 카드·인라인 강조 | 24~48px, 단색 |

### 15.2 라인 일러스트 사양

| 항목 | 값 |
|---|---|
| 스트로크 굵기 | **2px** (모든 라인) |
| 캡 | round (`stroke-linecap: round`) |
| 조인 | round (`stroke-linejoin: round`) |
| 색 | `--color-text-tertiary` (단색) — 다크 모드 자동 반전 |
| 크기 | 120~200px (Empty State) / 240~320px (온보딩) |
| 채움 | 없음 — 외곽선만 |
| 그림자 | 없음 |
| 그라디언트 | 없음 |

```css
.illust-line {
  width: 160px;
  height: 160px;
  color: var(--color-text-tertiary);  /* SVG는 currentColor 상속 */
}
.illust-line svg {
  width: 100%;
  height: 100%;
  fill: none;
  stroke: currentColor;
  stroke-width: 2;
  stroke-linecap: round;
  stroke-linejoin: round;
}
```

### 15.3 사용 매트릭스

| 상황 | 일러스트 |
|---|---|
| 첫 진입 (데이터 없음) | 라인 일러스트 — "빈 노트북" / "물음표 카드" |
| 검색 결과 없음 | 라인 일러스트 — "돋보기" |
| 네트워크 오류 | 라인 일러스트 — "끊어진 와이파이" |
| 권한 없음 | 라인 일러스트 — "자물쇠" |
| **온보딩 환영** | **마스코트** (풀 컬러) |
| **완료 축하** (체크리스트 모두 완료, 가입 완료) | **마스코트** + 컨페티 효과 |
| **AI 응답** | **하루안부 심볼** (마스코트 아님) |
| 인라인 강조 카드 | 스폿 일러스트 (단색 24~48px) |

### 15.4 마스코트와 라인 일러스트 분리 원칙

- **마스코트는 "사람과의 만남" 순간에만** — 환영, 완료, 축하.
- **빈 상태·오류·중립 정보는 라인 일러스트** — 마스코트가 빈 상태에 나오면 친근함이 흐트러진다.
- 두 종류를 한 화면에 동시 사용 금지.

### 15.5 접근성

- 일러스트는 **장식 목적**이 기본 — `alt=""` 또는 `aria-hidden="true"`.
- 일러스트만으로 의미를 전달하는 경우(드물게) `alt="빈 상자"` 같은 짧은 라벨.
- 일러스트 옆 텍스트가 본 메시지를 담는다 — 일러스트는 보조.

---

*하루안부 Foundations v3.2.3 — 2026.05.11 — 기반: tokens.css SoT (v3.2.3: 다크 모드 봉인, 라이트 단일 운영)*

---

*하루안부 Foundations v3.2 — 2026.05.11 — 기반: tokens.css SoT (v3.2: 다크 모드 §13 신설)*
