# 01 · Foundations

**하루안부 디자인 시스템 v3.1 — 파운데이션**

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

---

## 2. 로고

### 2.1 자산 위치

[logo/brand-system/](logo/brand-system/)에 6종이 있다 (v3.1):

| 파일 | 용도 | viewBox |
|---|---|---|
| `01_심볼단독.svg` | 앱 아이콘 · 파비콘 · FAB · AI 진입점 (정사각 컨테이너) | 512×512 |
| `02_워드마크단독.svg` | 헤더 · 푸터 · 텍스트 위주 자리 | 220×56 |
| `03_콤비네이션_가로.svg` | ★ **일반 헤더 · 명함 · 발표자료 · 광고 (기본)** | 360×96 |
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

### 3.2 시멘틱 컬러 (상태)

| 상태 | 토큰 | 메인 | Soft (배경) | 사용처 |
|---|---|---|---|---|
| 정상/완료 | `--color-success` | `#16A34A` | `#DCFCE7` | 체크리스트 완료, "정상" 뱃지 |
| 주의 | `--color-warning` | `#F59E0B` | `#FEF3C7` | 미완료, 확인 필요 |
| 위험/긴급 | `--color-danger` | `#DC2626` | `#FEE2E2` | SOS, 긴급 알림, 삭제 액션 |
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
- 다크모드는 v3.0 미정의 — 후속 작업

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
- 호버 상태는 **문서화하지 않는다** — 터치 우선 제품. 활성/Pressed만 정의.
- 카드 진입은 50ms 순차 딜레이로 리스트 stagger.

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

- **이모지 절대 금지** — 😊 ✅ 🙂 💊 🩺 등 일체 사용 안 함. 모두 fluent 아이콘 또는 하루안부 심볼로 대체.
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

### 12.1 미정의 (v3.0 시점)

- **다크 모드** — 글래스 카드의 다크 버전(반투명 검정 vs 딥 네이비) 미결정.
- **폼 검증 다중 에러** — 단일 에러는 정의됨, 비동기 검증 스피너·다중 메시지 패턴 미정.
- **알림 통합 체계** — 인앱·푸시·배너·토스트 4채널 통합 우산 미정 (현재는 토스트·SOS만).
- **저전력 모드 폴백** — Safari low-power에서 backdrop-filter 비활성 시 처리 정책 미정.

### 12.2 다음 버전 후보

- 일러스트 시스템 (현재는 마스코트만, Empty State 일러스트 사양 부족).
- 로딩 스켈레톤 표준 — 회색 블록 우선 권장하지만 토큰 미정.
- 차트·시각화 컬러 팔레트 — 데이터 시각화 색 사다리 미정.

---

*하루안부 Foundations v3.0 — 2026.05.09 — 기반: tokens.css SoT*
