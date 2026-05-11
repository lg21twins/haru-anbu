# 02 · Components

**하루안부 디자인 시스템 v3.1 — 컴포넌트 카탈로그**

이 문서는 화면을 만들 때 가져다 쓰는 모든 UI 컴포넌트의 명세다. 각 컴포넌트는 토큰을 참조하므로 `data-role`이 바뀌면 자동으로 색이 바뀐다. **hex를 직접 적지 않는다.**

> **v3.1 변경**: Flat이 기본, Glass는 예외. 카드 타입은 4종으로 고정 (default / action / alert / hero). Glass card는 더 이상 일반 정보 카드의 기본이 아니다.

카테고리는 M3 / KT Seamless Flow 패턴을 따른다:
- **Action** — 사용자가 누르는 것 (버튼, FAB, 칩)
- **Containment** — 콘텐츠를 담는 그릇 (카드 4종, 시트, 모달)
- **Navigation** — 화면 이동 (헤더, 탭바, 사이드바)
- **Communication** — 시스템이 사용자에게 말하는 것 (뱃지, 토스트, SOS, 알림)
- **Input** — 사용자가 입력하는 것 (텍스트 필드, 검색)
- **Display** — 데이터를 보여주는 것 (타임라인, 아바타)

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
- 호버 상태 정의 금지 (터치 우선).
- 이모지 절대 금지 (Fluent 아이콘으로).
- **좌측 컬러 바(`border-left: Npx solid …`) 강조 패턴 절대 금지** — 정보 강조는 `card-alert` 또는 flat tinted 배경으로만. 좌측 수직 라인은 장식적이고 통일감을 깬다.

---

*하루안부 Components v3.0 — 2026.05.09 — tokens.css 기반*
