# 02 · Components

**하루안부 디자인 시스템 v3.2 — 컴포넌트 카탈로그**

이 문서는 화면을 만들 때 가져다 쓰는 모든 UI 컴포넌트의 명세다. 각 컴포넌트는 토큰을 참조하므로 `data-role`이 바뀌면 자동으로 색이 바뀐다. **hex를 직접 적지 않는다.**

> **v3.1 변경**: Flat이 기본, Glass는 예외. 카드 타입은 4종으로 고정 (default / action / alert / hero). Glass card는 더 이상 일반 정보 카드의 기본이 아니다.

카테고리는 M3 / KT Seamless Flow 패턴을 따른다:
- **Action** — 사용자가 누르는 것 (버튼, FAB, 칩)
- **Containment** — 콘텐츠를 담는 그릇 (카드 4종, 시트, 모달)
- **Navigation** — 화면 이동 (헤더, 탭바, 사이드바)
- **Communication** — 시스템이 사용자에게 말하는 것 (뱃지, 토스트, SOS, 알림)
- **Input** — 사용자가 입력하는 것 (텍스트 필드, 검색)
- **Display** — 데이터를 보여주는 것 (타임라인, 아바타)
- **AI** — AI가 사용자에게 말하는 것 (Prompt Input/Output, 인라인 제안, 거절·불확실성)

파운데이션 토큰은 [01_FOUNDATIONS.md](01_FOUNDATIONS.md), 화면 단위 패턴은 [03_PATTERNS.md](03_PATTERNS.md) 참조.

## 카드 타입 4종 (v3.1 고정)

화면마다 다른 카드 스타일을 고를 필요가 없게, 카드는 다음 4가지로만 고정한다.

| 타입 | 용도 | 표면 |
|---|---|---|
| **`card-default`** | 일반 정보 표시 (대부분의 카드) | 흰 surface + 1px 보더 + shadow-1 |
| **`card-action`** | 클릭 가능한 카드 (탭하면 이동) | 흰 surface + hover/active 피드백 |
| **`card-alert`** | SOS·위험·주의 등 상태 강조 | 상태 soft 배경 (success/warning/danger soft) |
| **`card-hero`** | 화면당 최대 1개 — 오늘의 한 줄, AI 리포트 표지 | 역할 그라디언트 + on-accent 텍스트 |

**삭제된 변형**: `card-glass` (정보 카드 기본 사용 금지) / `card-emphasis` (남용 위험으로 제거) / `card-row` (default + 작은 padding으로 충분).

Glass 효과는 다음 4곳에만 한정:
1. 플로팅 필 탭바
2. 모달 오버레이의 sheet 표면
3. AI 리포트 카드 (선택적, hero 대신 쓸 때)
4. 환자앱 가족 사진 카드 (감성 자료)

---

## A. Action

### A1. Button

#### A1.1 Primary

화면당 1개 권장. 라벨은 동사 ("확인", "전송", "삭제하기").

```css
.btn-primary {
  background: var(--color-accent);
  color: var(--color-accent-on);
  font: var(--weight-semibold) var(--text-headline)/1 var(--font-family-base);
  height: var(--size-button-default);   /* 48px (환자 56px 자동) */
  padding: 0 var(--space-6);              /* 0 20px */
  border-radius: var(--radius-button);    /* 14px */
  border: 0;
  transition: 150ms var(--easing-standard);
}
.btn-primary:active {
  transform: scale(0.98);
  opacity: 0.8;
}
.btn-primary:disabled {
  opacity: 0.4;
  pointer-events: none;
}
```

#### A1.2 Secondary

Primary와 함께 짝지을 때. 흰 표면 + 보더.

```css
.btn-secondary {
  background: var(--color-bg-surface);
  color: var(--color-text-primary);
  border: 1px solid var(--color-border-subtle);
  /* 나머지는 primary와 동일 */
}
```

#### A1.3 Destructive

삭제·제거·위험 액션. **기본 CTA로 절대 사용 금지**.

```css
.btn-destructive {
  background: var(--color-danger);
  color: var(--color-text-on-dark);
  /* 나머지는 primary와 동일 */
}
```

#### A1.4 Ghost

본문 안 인라인 링크형. 보더 없음, accent 텍스트.

```css
.btn-ghost {
  background: transparent;
  color: var(--color-accent);
  font-weight: var(--weight-semibold);
  padding: 0 var(--space-3);
}
```

#### A1.5 사이즈 변형

| 변형 | 높이 | 토큰 |
|---|---|---|
| 기본 | 48px | `--size-button-default` |
| Compact | 44px | `--size-button-compact` |
| Large | 56px | `--size-button-large` (환자 자동) |
| 풀 너비 | `width: 100%` | `.btn--full` 추가 |

#### A1.6 사용 규칙

- 한 화면에 Primary 1개. 두 개의 액션이 동등하면 Primary + Secondary 짝.
- 라벨은 동사 + 명사 ("기록 저장", "알림 보내기"). 형용사·"확인" 같은 모호어 지양.
- 아이콘은 라벨 좌측 4px 간격. 아이콘 단독 버튼은 `aria-label` 필수.

---

### A2. FAB (Floating Action Button)

플로팅 탭바 우측에 분리 배치된 원형 버튼. **AI 진입점 전용**.

```css
.fab-ai {
  position: fixed;
  right: var(--space-5);                   /* 16px */
  bottom: calc(var(--space-5) + env(safe-area-inset-bottom) + 56px + var(--space-4));
  width: 56px;
  height: 56px;
  border-radius: var(--radius-full);
  background: linear-gradient(135deg, var(--color-accent) 0%, var(--color-accent-strong) 100%);
  box-shadow: 0 8px 28px rgba(var(--color-accent-rgb), 0.25);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-accent-on);
  border: 0;
}
.fab-ai__symbol {
  width: 28px;
  height: 28px;
  /* logo/brand-system/05_단색버전.svg를 흰색으로 사용 */
  filter: brightness(0) invert(1);
}
```

```html
<button class="fab-ai" aria-label="AI 어시스턴트 열기">
  <img src="../07_디자인/logo/brand-system/01_심볼단독.svg" class="fab-ai__symbol" alt="">
</button>
```

- 아이콘: **하루안부 심볼** (`logo/brand-system/01_심볼단독.svg`) — Fluent sparkle 아니라 브랜드 심볼. 28px, FAB 그라디언트 위에서 흰색으로 보이도록 `filter: brightness(0) invert(1)` 또는 `05_단색버전.svg` 직접 사용.
- 탭 시 AI 어시스턴트 바텀시트 오픈 (B2 참조).
- 탭바와 분리되어 있어야 한다. 탭 안에 끼워 넣지 않는다.

---

### A3. Chip / Pill

#### A3.1 Mode Chip (필터·선택)

```css
.chip {
  display: inline-flex;
  align-items: center;
  height: 32px;
  padding: 0 var(--space-5);
  border-radius: var(--radius-pill);
  background: var(--color-bg-surface);
  border: 1px solid var(--color-border-subtle);
  font: var(--weight-regular) var(--text-callout)/1 var(--font-family-base);
  color: var(--color-text-primary);
}
.chip[aria-pressed="true"],
.chip.is-active {
  background: var(--color-accent);
  color: var(--color-accent-on);
  border-color: transparent;
}
```

#### A3.2 사용

- 카드 상단 필터 row (전체 / 식사 / 투약 / 활동).
- 채팅 모드 토글 (가족 / 간호사 / AI).
- 다중 선택은 `aria-pressed`, 단일 선택은 `role="radio"` 그룹.

---

## B. Containment

### B1. Card — 4종 고정 (v3.1)

#### B1.1 `card-default` — 기본 정보 카드 ★

대부분의 카드는 이것. 흰 surface + 약한 보더 + 약한 shadow. **Glass·blur 사용 안 함.**

```css
.card {
  background: var(--color-bg-surface);
  border: 1px solid var(--color-border-subtle);
  border-radius: var(--radius-card);       /* 14px */
  box-shadow: var(--shadow-1);
  padding: var(--card-padding);            /* 16px (환자 24px 자동) */
}
```

#### B1.2 `card-action` — 클릭 가능한 카드

탭하면 이동·실행. `card-default` + hover/active 피드백.

```css
.card-action {
  /* card 기본 위에 */
  cursor: pointer;
  transition: 150ms var(--easing-standard);
}
.card-action:active {
  transform: scale(0.99);
  box-shadow: var(--shadow-2);
}
```

#### B1.3 `card-alert` — 상태 강조 카드

SOS·위험·주의·정보. 상태 soft 배경으로 화면에서 즉시 식별.

```css
.card-alert {
  border-radius: var(--radius-card);
  padding: var(--card-padding);
  border: 1px solid transparent;
}
.card-alert--danger  { background: var(--color-danger-soft);  color: var(--color-danger);  }
.card-alert--warning { background: var(--color-warning-soft); color: var(--palette-amber-700); }
.card-alert--success { background: var(--color-success-soft); color: var(--color-success); }
.card-alert--info    { background: var(--color-info-soft);    color: var(--color-info);    }
```

#### B1.4 `card-hero` — 화면당 최대 1개

오늘의 한 줄·AI 리포트 표지·완료 순간 등 **단 하나의 강조**. 화면당 1개를 넘지 않는다.

```css
.card-hero {
  background: linear-gradient(135deg, var(--color-accent) 0%, var(--color-accent-strong) 100%);
  color: var(--color-accent-on);
  border-radius: var(--radius-hero);       /* 24px */
  box-shadow: 0 8px 28px rgba(var(--color-accent-rgb), 0.25);
  padding: var(--space-7);                 /* 24px */
}
```

#### B1.5 ~~Glass card~~ (제거)

v3.1부터 일반 정보 카드의 기본 Glass는 **사용 안 함**. Glass 효과는 탭바·모달 sheet·AI 리포트 카드(선택적)·환자앱 가족 사진 카드 4곳에만 한정.

#### B1.6 ~~Card Emphasis~~ (제거)

남용 위험으로 제거. "특별한 카드"가 필요하면 `card-alert--info` 또는 `card-hero` 사용.

---

### B2. Bottom Sheet

모바일 모달의 기본 형태. 풀스크린 모달 거의 사용 안 함.

```css
.bottom-sheet {
  position: fixed;
  left: 0;
  right: 0;
  bottom: 0;
  max-height: 90vh;
  background: rgba(255, 255, 255, 0.97);
  backdrop-filter: blur(40px);
  border-radius: 28px 28px 0 0;
  box-shadow: 0 -4px 30px rgba(0, 0, 0, 0.10);
  padding: var(--space-7);
  z-index: var(--z-modal);
  transform: translateY(100%);
  transition: transform 350ms var(--easing-emphasize);
}
.bottom-sheet.is-open {
  transform: translateY(0);
}
```

상단에 드래그 핸들 4×40px (rgba(0,0,0,0.15)) 권장. ESC·딤 클릭으로 닫기.

---

### B3. Modal Overlay

웹 데스크톱·강제 동의 화면 한정. 모바일은 Bottom Sheet 우선.

```css
.modal-overlay {
  position: fixed;
  inset: 0;
  background: var(--color-bg-overlay);     /* rgba(0,0,0,0.40) */
  backdrop-filter: blur(2px);
  z-index: var(--z-overlay);
}
.modal {
  position: fixed;
  top: 50%; left: 50%;
  transform: translate(-50%, -50%);
  background: var(--color-bg-surface);
  border-radius: var(--radius-modal);      /* 18px */
  box-shadow: var(--shadow-3);
  padding: var(--space-7);
  max-width: 480px;
  z-index: var(--z-modal);
}
```

강제 동의(법정 약관 등)일 경우 닫기 버튼 제거 — KRDS 원칙.

---

### B4. Side Panel (Non-modal · v3.2 신설)

**의료진 웹 전용.** 환자 상세 페이지를 닫지 않고 옆에 메모·차트·과거 기록을 펼치는 보조 패널. Fluent 2 Non-modal Dialog + KT Seamless Context Panel 패턴.

```css
.side-panel {
  position: fixed;
  top: var(--size-topbar-height);              /* 64px (헤더 아래) */
  right: 0;
  bottom: 0;
  width: 380px;                                 /* 콘텐츠 1280px 안에서 가로 분할 */
  max-width: 30vw;
  background: var(--color-bg-surface);
  border-left: 1px solid var(--color-border-subtle);
  box-shadow: -4px 0 16px rgba(0, 0, 0, 0.06);
  z-index: var(--z-sticky);                     /* modal보다 낮음 — 본문은 계속 조작 가능 */
  transform: translateX(100%);
  transition: transform 250ms var(--easing-standard);
  display: flex;
  flex-direction: column;
}
.side-panel.is-open {
  transform: translateX(0);
}
.side-panel__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 56px;
  padding: 0 var(--space-5);
  border-bottom: 1px solid var(--color-border-subtle);
  flex-shrink: 0;
}
.side-panel__title {
  font: var(--w-strong) var(--text-headline)/1 var(--font-family-base);
  color: var(--color-text-primary);
}
.side-panel__body {
  flex: 1;
  overflow-y: auto;
  padding: var(--space-5);
}
.side-panel__footer {
  padding: var(--space-5);
  border-top: 1px solid var(--color-border-subtle);
  display: flex;
  justify-content: flex-end;
  gap: var(--space-3);
  flex-shrink: 0;
}
```

```html
<aside class="side-panel is-open" role="region" aria-label="환자 메모 패널">
  <header class="side-panel__header">
    <span class="side-panel__title">메모 · 김OO 환자</span>
    <button type="button" aria-label="패널 닫기"><iconify-icon icon="fluent:dismiss-24-filled"></iconify-icon></button>
  </header>
  <div class="side-panel__body">
    <!-- 메모 폼·과거 기록 타임라인 등 -->
  </div>
  <footer class="side-panel__footer">
    <button class="btn-secondary">취소</button>
    <button class="btn-primary">메모 저장</button>
  </footer>
</aside>
```

#### B4.1 Modal과의 차이 (Fluent 2 3분리)

| 구분 | Modal (B3) | Bottom Sheet (B2) | **Side Panel (B4)** |
|---|---|---|---|
| 본문 조작 가능 | 불가 (딤 처리) | 불가 (딤 처리) | **가능** (본문 계속 사용) |
| 닫는 방법 | 닫기 버튼 / ESC / 딤 클릭 | 핸들 드래그 / ESC | 닫기 버튼 / ESC |
| 동시 열기 | 1개만 | 1개만 | **여러 본문에 동시 사용 가능** (단 1개 패널) |
| 적용 플랫폼 | 웹 + 모바일 | 모바일 | **웹 전용** |
| Z-index | `--z-modal` (200) | `--z-modal` | `--z-sticky` (10) |

#### B4.2 사용 시나리오

- 의료진 웹 환자 상세 페이지 → 우측 패널에 메모 작성하면서 본문 차트는 계속 확인.
- 환자 목록 페이지 → 환자 한 명 선택 시 우측 패널에 요약 카드 (전체 페이지 전환 없이).
- AI 어시스턴트 진입 시 우측 패널로 챗 — 본문 작업과 병행.

#### B4.3 절대 규칙

- **모바일에는 사용 금지** — Bottom Sheet(B2)를 쓴다.
- **패널 안에 또 다른 모달·바텀시트 띄우기 금지** — Z 순서가 꼬인다. 패널 내부 액션은 inline으로.
- 본문 max-width(1280px)는 패널이 열려도 유지 — 패널은 그 외 공간에 들어간다.
- 패널이 열린 상태에서 헤더의 사이드바·검색은 계속 작동. 본문 readonly로 만들지 않는다.
- ESC 키로 패널 닫기 지원. 단, 모달이 동시에 열려 있으면 모달이 우선 닫힌다.

---

## C. Navigation

### C1. Header — Mobile

```css
.header-mobile {
  position: sticky;
  top: 0;
  z-index: var(--z-sticky);
  height: var(--size-header);              /* 44px */
  padding: 0 var(--space-page-margin);     /* 16px */
  background: transparent;
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  align-items: center;
}
```

3 영역: 좌(뒤로/메뉴) — 중앙(제목 17px/600) — 우(알림/검색). 투명 배경이라 페이지 그라디언트가 비쳐 헤더가 페이지의 일부처럼 읽힌다.

---

### C2. Header — Web

```css
.header-web {
  height: var(--size-topbar-height);       /* 64px */
  padding: 0 var(--space-7);
  background: var(--color-bg-surface);
  border-bottom: 1px solid var(--color-border-subtle);
  display: flex;
  align-items: center;
  gap: var(--space-5);
}
```

좌측 로고(콤비네이션 가로) + 검색 인풋(중앙) + 알림/아바타(우측). 의료진 웹 전용.

---

### C3. Tabbar — Floating Pill (모바일 시그니처)

> **v3.1 변경**: 탭바 배경은 **모든 역할에서 동일한 흰색/반투명 흰색**. 역할별 surface tint(딥블루/그린/오렌지 글래스)는 제거. 활성 아이콘과 라벨만 역할색으로 변한다.

```css
.tabbar {
  position: fixed;
  left: var(--space-5);                    /* 16px */
  right: var(--space-5);                   /* 16px */
  bottom: calc(var(--space-5) + env(safe-area-inset-bottom));
  height: var(--tabbar-height);            /* 56px */
  background: var(--tabbar-bg);            /* rgba(255,255,255,0.85) — 모든 역할 공통 */
  backdrop-filter: blur(var(--tabbar-blur));
  -webkit-backdrop-filter: blur(var(--tabbar-blur));
  border: var(--tabbar-border);            /* 1px solid border-subtle */
  border-radius: var(--radius-pill);
  box-shadow: var(--tabbar-shadow);        /* shadow-1 — 약한 그림자 */
  display: flex;
  align-items: center;
  z-index: var(--z-sticky);
  padding: 0 var(--space-4);
}
.tabbar__item {
  flex: 1;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 2px;
  color: rgba(28, 28, 30, 0.45);
  font: var(--weight-bold) var(--font-11)/1 var(--font-family-base);
  background: transparent;
  border: 0;
}
.tabbar__item iconify-icon {
  font-size: 24px;
}
.tabbar__item[aria-selected="true"],
.tabbar__item.is-active {
  color: var(--color-accent);
}
```

#### C3.1 절대 규칙

- **풀-블리드 금지** — 좌우 16px 인셋. 이게 시그니처다.
- 5탭 이내 (홈 / 가이드 / 소통 / 기록 / 마이).
- 탭 라벨 항상 표시. 환자 화면도 동일.
- AI FAB은 별도 원형 버튼으로 탭바 우측에 떨어뜨려 배치.
- **탭바 배경은 모든 역할에서 동일** (v3.1) — 역할별 글래스 tint 사용하지 않는다. 활성 아이콘·라벨 색만 변한다.

---

### C4. Sidebar — Web (의료진)

```css
.sidebar {
  width: var(--size-sidebar-width);        /* 240px */
  height: 100vh;
  background: var(--color-bg-surface);
  border-right: 1px solid var(--color-border-subtle);
  padding: var(--space-7) var(--space-5);
}
.sidebar__nav-item {
  display: flex;
  align-items: center;
  gap: var(--space-4);
  height: 44px;
  padding: 0 var(--space-5);
  border-radius: var(--radius-card);
  color: var(--color-text-secondary);
  font: var(--weight-semibold) var(--text-callout)/1 var(--font-family-base);
}
.sidebar__nav-item.is-active {
  background: var(--color-accent-soft);
  color: var(--color-accent);
}
```

- 1024px 미만: 64px 아이콘-only로 축소.
- 768px 미만: 드로어 오버레이로 전환.

---

## D. Communication

### D1. Badge

```css
.badge {
  display: inline-flex;
  align-items: center;
  height: 22px;
  padding: 0 var(--space-3);
  border-radius: var(--radius-pill);
  font: var(--weight-semibold) var(--text-mini)/1 var(--font-family-base);
}
.badge--success { background: var(--color-success-soft); color: #15803D; }
.badge--warning { background: var(--color-warning-soft); color: #B45309; }
.badge--danger  { background: var(--color-danger-soft);  color: var(--color-danger); }
.badge--info    { background: var(--color-info-soft);    color: var(--color-info); }
```

뱃지 안 아이콘은 16px(`--size-icon`은 별도, 16px 명시).

---

### D2. Toast

플로팅 탭바 위 100px 지점에 떠 있다 사라진다.

```css
.toast {
  position: fixed;
  left: 50%;
  bottom: 100px;
  transform: translateX(-50%) translateY(20px);
  opacity: 0;
  background: var(--color-text-primary);   /* #1C1C1E */
  color: var(--color-text-on-dark);
  font: var(--weight-regular) var(--text-callout)/1.4 var(--font-family-base);
  padding: var(--space-4) var(--space-6);
  border-radius: var(--radius-pill);
  box-shadow: var(--shadow-3);
  z-index: var(--z-toast);
  transition: 250ms var(--easing-standard);
}
.toast.is-shown {
  transform: translateX(-50%) translateY(0);
  opacity: 1;
}
```

자동 닫기 2.5초. 동시 노출 1개 권장 (Fluent 2: 4개까지 허용이지만 하루안부는 1개).

---

### D3. SOS Banner

화면 최상단, 다른 카드 안에 들어가지 않음.

```css
.sos-banner {
  display: flex;
  align-items: center;
  gap: var(--space-4);
  background: var(--color-danger);
  color: var(--color-text-on-dark);
  border-radius: var(--radius-card);
  padding: var(--space-5);
  font: var(--weight-semibold) var(--text-headline)/1.4 var(--font-family-base);
}
.sos-banner iconify-icon {
  font-size: 28px;
}
```

- 아이콘: `fluent:siren-24-filled` 또는 `fluent:warning-24-filled`.
- `role="alert"` + `aria-live="assertive"` 필수.
- 닫기 버튼 없음 (KRDS 원칙: 긴급 공지는 닫을 수 없음).

---

### D4. Alert / MessageBar (인라인)

페이지 안에 inline으로 박히는 알림 카드. SOS와 달리 본문 흐름의 일부.

```css
.alert {
  display: flex;
  gap: var(--space-4);
  padding: var(--space-5);
  border-radius: var(--radius-card);
  font: var(--weight-regular) var(--text-callout)/1.4 var(--font-family-base);
}
.alert--info    { background: var(--color-info-soft);    color: var(--color-info); }
.alert--success { background: var(--color-success-soft); color: #15803D; }
.alert--warning { background: var(--color-warning-soft); color: #B45309; }
.alert--danger  { background: var(--color-danger-soft);  color: var(--color-danger); }
```

좌측 아이콘 24px + 본문 + (선택) 우측 닫기 버튼.

---

## E. Input

### E1. Text Field

```css
.input {
  width: 100%;
  height: var(--size-input);               /* 48px */
  padding: 0 var(--space-5);               /* 0 16px */
  background: var(--color-bg-canvas);      /* 캔버스 색 = 흰 카드 위에서 살짝 들어간 표면 */
  color: var(--color-text-primary);
  font: var(--weight-regular) var(--text-callout)/1 var(--font-family-base);
  border: 1px solid var(--color-border-subtle);
  border-radius: var(--radius-control);    /* 8px */
  transition: 150ms var(--easing-standard);
}
.input:focus {
  outline: none;
  border-color: var(--color-accent);       /* 자동 역할 컬러 */
  box-shadow: 0 0 0 3px var(--color-accent-soft);
}
.input.is-error {
  border-color: var(--color-danger);
}
.input:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
.input::placeholder {
  color: var(--color-text-tertiary);
}
```

- 라벨은 인풋 위 `font: 600 var(--text-callout)`, 4px 아래 인풋.
- 에러 메시지는 인풋 아래 `font: var(--text-caption)`, danger 컬러, 4px 위.
- 헬퍼 텍스트는 `--color-text-secondary`, caption 사이즈.

---

### E2. Search Input

```css
.search {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  height: var(--size-input);
  padding: 0 var(--space-5);
  background: var(--color-bg-canvas);
  border: 1px solid var(--color-border-subtle);
  border-radius: var(--radius-pill);       /* pill */
}
.search iconify-icon {
  font-size: 20px;
  color: var(--color-text-tertiary);
}
.search input {
  flex: 1;
  border: 0;
  background: transparent;
  font: var(--text-callout) var(--font-family-base);
  outline: none;
}
```

좌측 `fluent:search-24-filled` 20px. 의료진 환자 목록·소통 검색에서 사용.

---

### E3. Textarea

```css
.textarea {
  /* .input과 동일하나 */
  height: auto;
  min-height: 120px;
  padding: var(--space-4) var(--space-5);
  resize: vertical;
  line-height: var(--leading-normal);
}
```

---

### E4. Toggle (Switch)

```css
.toggle {
  width: 52px;
  height: 32px;
  background: var(--color-border-strong);
  border-radius: var(--radius-pill);
  position: relative;
  transition: 200ms var(--easing-standard);
  cursor: pointer;
}
.toggle::after {
  content: "";
  position: absolute;
  top: 2px; left: 2px;
  width: 28px; height: 28px;
  background: white;
  border-radius: 50%;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.15);
  transition: 200ms var(--easing-standard);
}
.toggle[aria-checked="true"] {
  background: var(--color-accent);
}
.toggle[aria-checked="true"]::after {
  transform: translateX(20px);
}
```

`role="switch"` + `aria-checked` 필수.

---

### E5. Checkbox

```css
.checkbox {
  width: 24px; height: 24px;
  border: 2px solid var(--color-border-strong);
  border-radius: var(--radius-1);          /* 4px */
  background: var(--color-bg-surface);
}
.checkbox[aria-checked="true"] {
  background: var(--color-accent);
  border-color: var(--color-accent);
  /* 체크 아이콘은 fluent:checkmark-16-filled, 흰색 */
}
```

요양보호사 빠른 체크리스트에 다수 사용.

---

## F. Display

### F1. Avatar

```css
.avatar {
  border-radius: var(--radius-full);
  overflow: hidden;
  background: var(--color-bg-surface-muted);
  flex-shrink: 0;
}
.avatar--sm { width: var(--size-avatar-sm); height: var(--size-avatar-sm); }   /* 32px */
.avatar--md { width: var(--size-avatar-md); height: var(--size-avatar-md); }   /* 40px */
.avatar--lg { width: var(--size-avatar-lg); height: var(--size-avatar-lg); }   /* 56px */
.avatar--xl { width: var(--size-avatar-xl); height: var(--size-avatar-xl); }   /* 72px */
```

폴백: 이미지 없으면 이니셜 + 역할 컬러 배경.

---

### F2. Timeline

```
[원형 도트]──┐
            │ [카드: 시간 + 내용]
[원형 도트]──┤
            │ [카드: 시간 + 내용]
```

```css
.timeline {
  display: grid;
  grid-template-columns: 12px 1fr;
  gap: var(--space-4);
  position: relative;
}
.timeline::before {
  content: "";
  position: absolute;
  left: 5px; top: 0; bottom: 0;
  width: 2px;
  background: var(--color-border-subtle);
}
.timeline__dot {
  width: 12px; height: 12px;
  border-radius: 50%;
  background: var(--color-accent);
  margin-top: 8px;
  z-index: 1;
}
.timeline__card {
  /* card-row 또는 card 사용 */
}
```

기록 페이지·인수인계 요약에서 핵심 컴포넌트.

---

### F3. Stat Card (큰 숫자 카드)

```css
.stat-card {
  /* card 위에 덧붙임 */
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}
.stat-card__value {
  font: var(--weight-semibold) var(--text-display)/1 var(--font-family-base);
  color: var(--color-accent);
}
.stat-card__label {
  font: var(--text-caption) var(--font-family-base);
  color: var(--color-text-secondary);
}
.stat-card__delta {
  /* 증감 뱃지 (success / danger) */
}
```

의료진 대시보드·보호자 주간 안심 지수에 사용.

---

### F4. Empty State

```html
<div class="empty">
  <iconify-icon icon="fluent:document-text-24-filled"></iconify-icon>
  <p class="empty__title">아직 오늘의 기록이 없어요</p>
  <p class="empty__hint">간호사가 첫 기록을 남기면 여기에 표시됩니다</p>
</div>
```

```css
.empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: var(--space-10) var(--space-5);
  gap: var(--space-3);
  color: var(--color-text-secondary);
}
.empty iconify-icon {
  font-size: 48px;
  color: var(--color-text-tertiary);
}
.empty__title {
  font: var(--weight-semibold) var(--text-headline) var(--font-family-base);
  color: var(--color-text-primary);
}
.empty__hint {
  font: var(--text-callout) var(--font-family-base);
}
```

UX 라이팅 원칙: "데이터 없음" 같은 시스템 메시지 금지. "아직 ~이 없어요" 톤.

---

### F5. Section Tab (v3.2 신설)

페이지 내부 콘텐츠 분할용 탭. **탭바(C3)와 명확히 구분** — 탭바는 페이지 이동, Section Tab은 페이지 내 콘텐츠 토글.

```css
.section-tabs {
  display: flex;
  gap: var(--space-2);
  border-bottom: 1px solid var(--color-border-subtle);
  margin-bottom: var(--space-6);
}
.section-tabs__tab {
  height: 44px;
  padding: 0 var(--space-5);
  background: transparent;
  border: 0;
  border-bottom: 2px solid transparent;
  font: var(--w-strong) var(--text-callout)/1 var(--font-family-base);
  color: var(--color-text-secondary);
  cursor: pointer;
  transition: 150ms var(--easing-standard);
  margin-bottom: -1px;  /* 상위 border와 정렬 */
}
.section-tabs__tab[aria-selected="true"] {
  color: var(--color-accent);
  border-bottom-color: var(--color-accent);
}
[data-platform="web"] .section-tabs__tab:hover:not([aria-selected="true"]) {
  color: var(--color-text-primary);
  background: var(--state-hover-overlay);
}
```

- `role="tablist"` + 각 탭 `role="tab"` + `aria-selected` + `aria-controls`.
- 탭 카운트 ≤ 5개 권장 (모바일), ≤ 7개 (웹).
- 탭바와 시각 차이 핵심: **flat underline 강조** vs 탭바의 **pill 배경**.

---

### F6. Stepper (v3.2 신설)

다단계 폼·온보딩 진행 표시.

```
①─────②─────③─────④
완료   진행중  대기    대기
```

```css
.stepper {
  display: flex;
  align-items: center;
  gap: var(--space-3);
}
.stepper__step {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-2);
  flex: 1;
}
.stepper__dot {
  width: 28px;
  height: 28px;
  border-radius: var(--radius-pill);
  background: var(--color-bg-surface-muted);
  border: 1px solid var(--color-border-subtle);
  display: flex;
  align-items: center;
  justify-content: center;
  font: var(--w-strong) var(--text-caption)/1 var(--font-family-base);
  color: var(--color-text-secondary);
  flex-shrink: 0;
}
.stepper__step[data-state="done"] .stepper__dot {
  background: var(--color-accent);
  color: var(--color-accent-on);
  border-color: var(--color-accent);
}
.stepper__step[data-state="current"] .stepper__dot {
  background: var(--color-bg-surface);
  border: 2px solid var(--color-accent);
  color: var(--color-accent);
}
.stepper__connector {
  flex: 1;
  height: 2px;
  background: var(--color-border-subtle);
}
.stepper__connector[data-state="done"] {
  background: var(--color-accent);
}
.stepper__label {
  font: var(--text-caption)/1 var(--font-family-base);
  color: var(--color-text-secondary);
  text-align: center;
}
```

- 단계 ≤ 5개. 6개 이상이면 "1/8 진행 중" 같은 progress bar로 대체.
- 완료 단계는 클릭 가능 (뒤로 돌아가기). 미완료 단계는 클릭 불가.
- 환자앱에서 사용 시 `aria-current="step"` 필수.

---

### F7. Progress Bar (v3.2 신설)

```css
.progress {
  width: 100%;
  height: 6px;
  background: var(--color-bg-surface-muted);
  border-radius: var(--radius-pill);
  overflow: hidden;
}
.progress__fill {
  height: 100%;
  background: var(--color-accent);
  border-radius: var(--radius-pill);
  transition: width 250ms var(--easing-standard);
}
.progress--indeterminate .progress__fill {
  width: 30%;
  animation: progress-slide 1.5s ease-in-out infinite;
}
@keyframes progress-slide {
  0%   { transform: translateX(-100%); }
  100% { transform: translateX(400%); }
}
```

- 비율 알 때: width %.
- 비율 모를 때(AI 응답 생성 중 등): `--indeterminate` 변형.
- 6px 막대가 기본. 강조 필요 시 8px.
- ARIA: `role="progressbar"` + `aria-valuenow` / `aria-valuemax`.

---

### F8. Accordion (v3.2 신설)

긴 케어 가이드, FAQ에 사용.

```css
.accordion__item {
  border-bottom: 1px solid var(--color-border-subtle);
}
.accordion__header {
  width: 100%;
  min-height: 56px;
  padding: var(--space-4) 0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-4);
  background: transparent;
  border: 0;
  cursor: pointer;
  text-align: left;
}
.accordion__title {
  font: var(--w-strong) var(--text-headline)/1.3 var(--font-family-base);
  color: var(--color-text-primary);
}
.accordion__chevron {
  transition: transform 200ms var(--easing-standard);
  color: var(--color-text-secondary);
}
.accordion__item[aria-expanded="true"] .accordion__chevron {
  transform: rotate(180deg);
}
.accordion__body {
  padding: 0 0 var(--space-5);
  font: var(--text-body)/var(--leading-relaxed) var(--font-family-base);
  color: var(--color-text-secondary);
  display: none;
}
.accordion__item[aria-expanded="true"] .accordion__body {
  display: block;
}
```

- Chevron 아이콘: `fluent:chevron-down-20-filled`, 펼쳐지면 180° 회전.
- 동시에 여러 항목 펼침 허용 (single-open 강제 안 함). 사용자가 비교 읽기 편함.
- ARIA: `<button aria-expanded>` + `<div role="region">`.

---

### F9. Tooltip — Web 한정 (v3.2 신설)

**의료진 웹 전용.** 모바일에서는 사용 금지 (터치에서 stuck-hover 문제).

```css
.tooltip {
  position: absolute;
  bottom: calc(100% + 8px);
  left: 50%;
  transform: translateX(-50%);
  background: var(--palette-gray-900);
  color: var(--color-text-on-dark);
  padding: var(--space-3) var(--space-4);
  border-radius: var(--radius-2);
  font: var(--w-strong) var(--text-caption)/1.3 var(--font-family-base);
  white-space: nowrap;
  box-shadow: var(--shadow-2);
  pointer-events: none;
  opacity: 0;
  transition: opacity 150ms var(--easing-standard);
}
[data-platform="web"] .tooltip-trigger:hover .tooltip,
[data-platform="web"] .tooltip-trigger:focus-visible .tooltip {
  opacity: 1;
}
```

- 모바일에서는 `display: none` (CSS `[data-platform="web"]` 외부에서는 미적용).
- 트리거 hover 후 500ms 지연 권장 (즉시 표시는 시각 노이즈).
- 한 화면 동시 표시 1개만 — 새 tooltip 열리면 이전은 즉시 닫힘.
- 라벨이 한 줄 안에 안 들어가면 별도 모달이나 Popover로 — Tooltip은 짧은 단서 한정.

---

### F10. Pagination — Web 한정 (v3.2 신설)

**의료진 웹 환자 목록 등.** 모바일은 무한 스크롤 또는 "더 보기" 버튼.

```css
.pagination {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  justify-content: center;
}
.pagination__btn {
  min-width: 36px;
  height: 36px;
  padding: 0 var(--space-3);
  border-radius: var(--radius-control);
  background: transparent;
  border: 1px solid var(--color-border-subtle);
  color: var(--color-text-primary);
  font: var(--text-callout) var(--font-family-base);
  cursor: pointer;
}
.pagination__btn[aria-current="page"] {
  background: var(--color-accent);
  color: var(--color-accent-on);
  border-color: var(--color-accent);
}
.pagination__btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}
[data-platform="web"] .pagination__btn:hover:not([aria-current="page"]):not(:disabled) {
  background: var(--state-hover-overlay);
}
```

- 좌우 chevron + 페이지 번호 + 이동 인풋 (선택적).
- 페이지 수 ≤ 7개면 모두 표시, 그 이상이면 1 / 2 / 3 / … / N 줄임.
- ARIA: `<nav aria-label="페이지 이동">` + 현재 페이지 `aria-current="page"`.

---

## H. AI

**v3.2 신설.** 하루안부의 AI(보호자 챗, 환자 음성 도우미, 요양보호사 사진 메모, AI 리포트, 가족 채팅 보조)는 모두 같은 시각 언어로 말한다. 다음 4개 컴포넌트로 분리한다.

> AI 진입점 마크는 **항상 하루안부 심볼**(`logo/brand-system/01_심볼단독.svg`)이다. Fluent sparkle 사용 금지. AI 표면 색은 **역할 accent가 아닌 중립**(흰색·gray-50) — 역할이 바뀌어도 AI 톤은 동일하게 보여야 "이건 AI" 인식이 즉시 된다.

### H1. AI Prompt Input

사용자가 AI에게 묻는 입력란. 일반 텍스트 인풋(E1)과 외형은 비슷하나, **음성·파일 첨부 어포던스**가 항상 우측에 있고 좌측에 **하루안부 심볼**이 들어간다.

```css
.ai-prompt {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  min-height: var(--size-input);
  padding: var(--space-3) var(--space-5);
  background: var(--ai-surface);
  border: var(--ai-border);
  border-radius: var(--radius-pill);
  box-shadow: var(--shadow-1);
}
.ai-prompt__mark {
  width: var(--ai-mark-size-sm);
  height: var(--ai-mark-size-sm);
  flex-shrink: 0;
}
.ai-prompt__input {
  flex: 1;
  border: 0;
  background: transparent;
  font: var(--text-callout) var(--font-family-base);
  outline: none;
}
.ai-prompt__actions {
  display: flex;
  align-items: center;
  gap: var(--space-2);
}
.ai-prompt__actions button {
  width: 36px; height: 36px;
  border-radius: var(--radius-pill);
  color: var(--color-text-secondary);
}
.ai-prompt__send {
  background: var(--color-accent);
  color: var(--color-accent-on);
}
```

```html
<form class="ai-prompt" role="search" aria-label="AI 어시스턴트에게 질문">
  <img class="ai-prompt__mark" src="../07_디자인/logo/brand-system/01_심볼단독.svg" alt="">
  <input class="ai-prompt__input" placeholder="궁금한 점을 적어보세요" aria-label="AI에게 물어보기">
  <div class="ai-prompt__actions">
    <button type="button" aria-label="사진 첨부"><iconify-icon icon="fluent:image-24-filled"></iconify-icon></button>
    <button type="button" aria-label="음성 입력"><iconify-icon icon="fluent:mic-24-filled"></iconify-icon></button>
    <button type="submit" class="ai-prompt__send" aria-label="전송"><iconify-icon icon="fluent:send-24-filled"></iconify-icon></button>
  </div>
</form>
```

#### 규칙

- 좌측 심볼은 항상 보인다. 음성 입력 중에는 심볼을 `pulse` 애니메이션으로 활성 표시.
- 음성 모드는 **환자앱·요양보호사앱에서 기본 활성**. 보호자앱·의료진은 아이콘만 제공.
- 첨부 가능 종류는 컨텍스트별로 다름 — 보호자 챗(없음), 요양보호사(사진), 의료진(차트 파일 v3.2 미정).
- 비활성 상태(`disabled`)면 placeholder를 "지금은 답하기 어려워요"로.

---

### H2. AI Prompt Output

AI가 사용자에게 답하는 카드. 일반 정보 카드와 외형은 비슷하나 **좌상단 마크 + 우상단 라벨 슬롯**이 시그니처다.

```css
.ai-output {
  background: var(--ai-surface);
  border: var(--ai-border);
  border-radius: var(--ai-radius);
  padding: var(--ai-padding);
  box-shadow: var(--shadow-1);
  position: relative;
}
.ai-output__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-4);
  margin-bottom: var(--space-4);
}
.ai-output__mark {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  font: var(--w-strong) var(--text-caption)/1 var(--font-family-base);
  color: var(--color-text-secondary);
}
.ai-output__mark img {
  width: var(--ai-mark-size-md);
  height: var(--ai-mark-size-md);
}
.ai-output__badge {
  /* 우상단 라벨: "AI 생성" / "확신 없음" / "초안" 등 */
  font: var(--w-strong) var(--text-mini)/1 var(--font-family-base);
  padding: var(--space-1) var(--space-3);
  border-radius: var(--radius-pill);
  background: var(--color-bg-surface-muted);
  color: var(--color-text-secondary);
}
.ai-output__body {
  font: var(--text-body)/var(--leading-relaxed) var(--font-family-base);
  color: var(--color-text-primary);
}
.ai-output__citation {
  margin-top: var(--space-5);
  padding-top: var(--space-4);
  border-top: 1px dashed var(--ai-accent-hairline);    /* AI Purple hairline · v3.2.4 */
  font: var(--text-caption)/1.5 var(--font-family-base);
  color: var(--ai-citation-color);
}
```

```html
<article class="ai-output" aria-label="AI 응답">
  <header class="ai-output__header">
    <div class="ai-output__mark">
      <img src="../07_디자인/logo/brand-system/01_심볼단독.svg" alt="">
      <span>하루안부 AI</span>
    </div>
    <span class="ai-output__badge">AI 생성</span>
  </header>
  <div class="ai-output__body">
    오늘 어머님은 식사를 2/3 드셨고, 오후 산책을 20분 하셨습니다. 평소 패턴에서 큰 변화는 없어 보여요.
  </div>
  <footer class="ai-output__citation">
    근거 · 09:14 식사 기록, 14:32 활동 기록 · 최종 판단은 의료진이 합니다
  </footer>
</article>
```

#### 변형 (badge slot)

| 라벨 | 토큰 | 의미 |
|---|---|---|
| `AI 생성` | 기본 회색 | 기본 응답 — 모든 AI 카드에 표시 |
| `확신 없음` | `--ai-uncertainty-color` (amber-700) | 데이터가 부족하거나 추론 신뢰도가 낮을 때 |
| `초안` | 회색 | 사용자가 검토·수정 후 전송하는 메시지 (요양보호사 메모 등) |
| `최신 아님` | 회색 | 캐시된 응답 — 새로고침 권장 |

#### 규칙

- **인용·근거 footer는 필수가 아니지만 권장**. 의료/돌봄 정보는 출처 표기 필수(시간·기록 ID).
- **"최종 판단은 의료진이 합니다" 면책**은 의료 관련 응답에 항상 footer 마지막 줄로.
- AI 응답 본문에 `--leading-relaxed` (1.6)을 기본으로 — 읽기 부담을 줄임.
- 변형 1: hero 변형(`ai-output--hero`)은 `card-hero` 그라디언트 위 흰 텍스트 — AI 리포트 표지 한정.

---

### H3. AI Text Field (Inline Suggestion)

본문 안에 AI가 제안하는 텍스트. 사용자가 쓰는 인풋·textarea 위에 **회색 흐림 제안**으로 떠 있다가 Tab 또는 우측 ✓ 버튼으로 채택. 요양보호사 메모, 보호자 답장 작성에 사용.

```css
.ai-suggest {
  position: relative;
}
.ai-suggest__field {
  /* .textarea와 동일, 하지만 우측에 chip 공간 확보 */
  padding-right: 88px;
}
.ai-suggest__chip {
  position: absolute;
  bottom: var(--space-3);
  right: var(--space-3);
  display: flex;
  align-items: center;
  gap: var(--space-2);
  height: 28px;
  padding: 0 var(--space-3);
  background: var(--ai-surface-soft);
  border: var(--ai-border);
  border-radius: var(--radius-pill);
  font: var(--w-strong) var(--text-mini)/1 var(--font-family-base);
  color: var(--color-text-secondary);
}
.ai-suggest__chip img {
  width: 14px; height: 14px;
}
.ai-suggest__chip[data-state="active"] {
  border-color: var(--color-accent-soft);
  color: var(--color-accent);
}
```

```html
<div class="ai-suggest">
  <textarea class="ai-suggest__field" placeholder="기록을 작성하세요">오전 식사를 잘 드</textarea>
  <button type="button" class="ai-suggest__chip" data-state="active" aria-label="AI 제안 채택">
    <img src="../07_디자인/logo/brand-system/01_심볼단독.svg" alt="">
    <span>제안 채택 · Tab</span>
  </button>
</div>
```

#### 규칙

- 제안은 **음영 회색 텍스트**(`--color-text-tertiary`)로 미리보기 — 채택 전에는 인풋 값에 들어가지 않는다.
- Tab 키 또는 칩 클릭으로 채택. ESC 또는 다른 키로 무시.
- 제안이 5초 이상 변하지 않으면 부드럽게 페이드아웃 — 입력을 방해하지 않는다.
- **환자앱에서는 사용 금지** — 글자가 작아 가독성을 해친다. 환자 입력은 보이스 모드 우선.

---

### H4. AI Refusal Card (거절 · 불확실성)

AI가 답할 수 없거나 답하면 안 되는 요청에 대한 표준 응답. **빈 채팅 버블 대신 명시적 카드**로 — 사용자가 "왜 답이 없지?" 라고 헷갈리지 않게.

```css
.ai-refuse {
  display: flex;
  align-items: flex-start;
  gap: var(--space-4);
  background: var(--ai-refuse-bg);
  border: var(--ai-refuse-border);
  border-radius: var(--ai-radius);
  padding: var(--ai-padding);
  color: var(--color-text-secondary);
}
.ai-refuse__icon {
  flex-shrink: 0;
  width: var(--ai-mark-size-md);
  height: var(--ai-mark-size-md);
  color: var(--color-text-tertiary);
}
.ai-refuse__title {
  font: var(--w-strong) var(--text-headline)/1.3 var(--font-family-base);
  color: var(--color-text-primary);
  margin-bottom: var(--space-2);
}
.ai-refuse__hint {
  font: var(--text-callout)/1.5 var(--font-family-base);
}
.ai-refuse__action {
  margin-top: var(--space-4);
  display: inline-flex;
}
```

```html
<aside class="ai-refuse" role="status" aria-label="AI 응답 불가">
  <iconify-icon class="ai-refuse__icon" icon="fluent:info-24-filled"></iconify-icon>
  <div>
    <div class="ai-refuse__title">이 질문은 의료진께 문의해 주세요</div>
    <p class="ai-refuse__hint">처방 변경·진단에 관한 답변은 드릴 수 없어요. 담당 의료진에게 바로 연결해 드릴게요.</p>
    <a class="ai-refuse__action btn-ghost" href="#contact">담당 간호사에게 메시지</a>
  </div>
</aside>
```

#### 거절 사유별 표준 카피 (3종 고정)

| 사유 | 제목 | 보조 | 대체 액션 |
|---|---|---|---|
| 의료 진단·처방 변경 요청 | "이 질문은 의료진께 문의해 주세요" | "처방 변경·진단은 답변하지 않아요" | "담당 간호사에게 메시지" |
| 개인정보·민감 정보 요청 | "이 정보는 알려드릴 수 없어요" | "개인정보 보호를 위해 보호자님 본인 확인이 필요해요" | "본인 인증" |
| 데이터 부족 | "오늘은 답변할 데이터가 부족해요" | "기록이 더 쌓이면 다시 시도해 주세요" | "기록 확인" |

#### 규칙

- **danger 톤(빨강) 사용 금지** — 거절은 위험이 아니다. 중립 회색.
- **모든 거절 카드는 대체 액션 1개를 제시한다** — 사용자를 막다른 골목에 두지 않는다.
- 거절 카드는 채팅 흐름에서 **AI 메시지처럼 좌측에 정렬** (`ai-output`과 같은 위치).
- `role="status"` + `aria-live="polite"` — SOS와 달리 침입적이지 않게.

---

### H. AI 컴포넌트 사용 규칙 요약

| 컴포넌트 | 사용처 | 음성 우선 |
|---|---|---|
| H1 Prompt Input | 보호자 챗, 환자 도우미, 요양보호사 메모 작성 | 환자·요양보호사 |
| H2 Prompt Output | AI 리포트 본문, 챗 응답, 요약 카드 | — |
| H3 Inline Suggestion | 요양보호사 메모 자동완성, 보호자 답장 작성 | (환자앱 제외) |
| H4 Refusal Card | 처방·진단 거절, 데이터 부족, 본인 확인 필요 | — |

**일관 규칙 (모든 AI 컴포넌트 공통):**

- 진입점 마크는 **하루안부 심볼 1종**. Fluent sparkle / wand / robot 절대 사용 금지.
- AI 표면은 항상 **중립**(흰색 또는 gray-50). 역할 accent로 큰 면 칠하지 않는다.
- 의료 관련 응답 마지막은 **`.ai-disclaimer` 클래스로 면책 1줄 필수** (v3.2.4 표준화).
- 모든 AI 카드 위쪽에 `AI 생성` 라벨 — 사용자가 사람 메시지와 헷갈리지 않도록.
- 인용·근거는 dashed top-border로 본문과 시각적으로 분리(`--ai-citation-color`).

### H5. AI Disclaimer (v3.2.4 신설 표준)

의료 관련 AI 응답·리포트의 면책 1줄을 일관 적용. tokens.css 표준 클래스.

```html
<!-- 기본 (짧은 응답 카드용) -->
<p class="ai-disclaimer">최종 판단은 의료진이 합니다</p>

<!-- 풀 사이즈 (AI 리포트 표지·긴 응답용) -->
<p class="ai-disclaimer ai-disclaimer--full">
  최종 판단은 의료진이 합니다. 증상이 갑작스럽거나 평소와 다르면 담당 간호사에게 바로 연락하세요.
</p>

<!-- 인라인 변형 (H4 거절 카드 등 footer 분리 없이) -->
<p class="ai-disclaimer ai-disclaimer--inline">최종 판단은 의료진이 합니다</p>
```

#### 규칙

- 의료/처방/투약/활력 관련 AI 응답에 **자동 박힘 의무**. 누락된 화면은 P0 위반으로 간주.
- 좌측 `ⓘ` 마크 + AI Purple hairline top-border로 본문과 자연스럽게 분리.
- `--full` 변형은 AI 리포트 표지(P3D)·일간/주간 리포트 끝에 한 번만.
- 환자앱에서는 자동으로 본문 18px 상향 (토큰 자동 처리).
- AI가 아닌 일반 정보(공지·시설 안내)에는 사용 금지 — 면책의 무게가 희석된다.

---

## G. 사용 규칙 (반복 강조)

### Do

- 모든 색·간격·라운드·그림자는 토큰을 통해서만 사용.
- 컴포넌트 마크업은 `data-role`을 신경 쓰지 않는다 — 토큰이 알아서 바뀐다.
- 글래스 카드를 기본으로, flat·hero는 의도적 예외.
- 활성 상태는 색만 바꾸고, 절대 Filled/Outline 토글로 표현하지 않는다.
- 버튼은 시각 피드백 `transform: scale(0.98)` + `opacity: 0.8` 150ms.

### Don't

- hex 직접 사용 금지 (`#2C7AFC` 등 코드에 등장하면 안 됨).
- 새 라운드 값 도입 금지 (16px, 20px 등 사다리 외 값).
- 하드 그림자 (`rgba(0,0,0,0.20)+`) 금지.
- 카드 안에 `card`를 또 중첩 금지 — 정보가 시각적으로 깊어 보이지만 실제로는 읽기 어려움.
- 아이콘 라이브러리 혼용 금지.
- 호버 상태 정의 금지 — **모바일 한정**. 의료진 웹(data-platform="web")은 hover 토큰 정식 사용 (FOUNDATIONS §8.5).
- 이모지 절대 금지 (Fluent 아이콘으로).
- **좌측 컬러 바(`border-left: Npx solid …`) 강조 패턴 절대 금지** — 정보 강조는 `card-alert` 또는 flat tinted 배경으로만. 좌측 수직 라인은 장식적이고 통일감을 깬다.

---

*하루안부 Components v3.2 — 2026.05.11 — tokens.css 기반 (v3.2: H. AI 카테고리 4종 신설)*
