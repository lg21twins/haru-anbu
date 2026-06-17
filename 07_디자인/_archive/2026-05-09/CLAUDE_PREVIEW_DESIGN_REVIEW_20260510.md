# Claude 전달용 Preview 디자인 시스템 통일성 리뷰

대상:

- `07_디자인/preview.html`
- `07_디자인/_preview-shared.css`
- `07_디자인/tokens/tokens.css`
- `07_디자인/preview-roles.html`
- 관련 문서 `README.md`, `01_FOUNDATIONS.md`, `02_COMPONENTS.md`, `03_PATTERNS.md`

작성일: 2026-05-10

## 총평

현재 디자인 시스템은 이전보다 훨씬 정리되어 있고, `preview.html`도 문서 허브 형태로 좋아졌다. 다만 "디자인 통일성" 관점에서는 아직 토큰 기반 시스템과 프리뷰 구현이 완전히 맞물리지 않는다.

특히 preview 계열 파일에 하드코딩된 색, radius, blur, shadow가 많아서 실제 앱 구현자가 복붙하면 시스템이 다시 흩어질 수 있다. 아래 항목을 우선순위대로 개선해달라.

## 우선 개선 사항

### 1. preview 계열 파일의 하드코딩 값을 토큰으로 치환

`preview.html`, `_preview-shared.css`, `preview-roles.html`에 아래 값들이 직접 들어가 있다.

- `#2C7AFC`, `#22C55E`, `#FB923C`
- `border-radius: 18px`, `14px`, `9999px`, `50%`
- `blur(16px)`, `blur(20px)`
- `rgba(44, 122, 252, ...)`
- `box-shadow: 0 8px 28px ...`

문서에서는 "컴포넌트는 hex 직접 사용 금지"라고 하는데, 프리뷰 코드가 예외처럼 보인다. 프리뷰는 팀원이 가장 많이 복붙할 가능성이 있으니 실제 컴포넌트 예시는 반드시 토큰 기반으로 바꿔야 한다.

권장:

- `#2C7AFC` -> `var(--color-accent)` 또는 `var(--brand-blue-500)`
- `18px` -> `var(--radius-card-lg)`
- `14px` -> `var(--radius-card)`
- `9999px` -> `var(--radius-pill)`
- `blur(16px)` -> `blur(var(--blur-card))`
- 직접 shadow -> `var(--shadow-*)`

단, 색상표/설명용 hex 텍스트 자체는 유지해도 된다. 문제는 실제 컴포넌트 스타일 예시에 hex가 들어가는 것이다.

### 2. 환자 토큰 우선순위 충돌 수정

`tokens.css`에서 `[data-role="patient"]`가 본문 18px, 버튼 56px로 상향되는데, 뒤쪽 `[data-platform="mobile"]`에서 다시 본문 16px, touch target 44px로 덮는다.

문서에는 "환자 자동 상향"이라고 되어 있어서 구현 의도와 실제 CSS 우선순위가 어긋난다.

권장:

- `[data-role="patient"][data-platform="mobile"]` 조합 규칙 추가
- 또는 role 규칙을 platform 규칙 뒤로 이동

예시:

```css
[data-role="patient"][data-platform="mobile"] {
  --text-body: var(--font-18);
  --text-headline: var(--font-20);
  --text-title: var(--font-24);
  --size-touch-target: 56px;
  --size-button-default: 56px;
  --size-row: 64px;
}
```

### 3. `--color-accent-rgb` 토큰 추가

`02_COMPONENTS.md`에서는 `rgba(var(--color-accent-rgb), 0.25)`를 쓰는데 `tokens.css`에는 해당 토큰이 없다.

권장:

```css
:root {
  --color-accent-rgb: 44, 122, 252;
}

[data-role="guardian"] {
  --color-accent-rgb: 44, 122, 252;
}

[data-role="medical"],
[data-role="doctor"],
[data-role="nurse"],
[data-role="caregiver"] {
  --color-accent-rgb: 34, 197, 94;
}

[data-role="patient"] {
  --color-accent-rgb: 251, 146, 60;
}
```

이 토큰이 있어야 hero card, FAB, emphasis border의 역할별 그림자와 틴트가 안정적으로 동작한다.

### 4. 글래스모피즘 원칙을 화면 유형별로 나누기

현재 원칙은 "글래스모피즘이 기본"인데, 이건 보호자앱/온보딩/AI 리포트에는 잘 맞지만 의료진웹, 요양보호사앱에는 과할 수 있다.

권장:

- 감성형 화면: glass 기본
- 업무형 화면: flat/card-row 기본
- 환자 화면: 큰 CTA와 명확한 표면 우선
- glass는 "브랜드 감성/요약/강조 영역"에 제한

문구 변경 제안:

기존:

> 글래스모피즘이 기본

수정:

> 감성형 화면은 glass, 업무형 화면은 flat/card-row. 보호자 홈, AI 리포트, 온보딩은 glass를 적극 사용하되 의료진웹과 요양보호사 입력 화면은 flat/card-row를 기본으로 한다.

### 5. preview.html 첫 화면의 블루 보호자 중심성 완화

`preview.html`이 `data-role="guardian"`이고 hero도 보호자 블루 그라디언트라, 디자인 시스템 전체가 보호자앱 중심처럼 보인다. 의료진/환자까지 포함한 시스템이라면 첫 화면은 neutral base에 3-role 신호가 같이 보여야 한다.

권장:

- hero 안에 보호자/의료진/환자 3색 미니 스트립 또는 role chips 추가
- 첫 화면 배경은 과한 guardian gradient보다 neutral + 세 역할 accent 조합 권장
- "하나의 차체, 세 개의 테마"를 시각적으로 첫 화면에서 바로 보여주기

### 6. preview-roles.html의 "색만 바뀐다" 표현 조정

문서에서는 구조는 동일하고 색만 바뀐다고 하지만, 실제로 환자는 typography/touch target/row height가 달라져야 한다. 즉 "색만"이 아니라 "색 + 접근성 스케일"이 바뀐다.

권장 문구:

> 구조는 동일, 역할에 따라 색과 접근성 스케일이 조정된다.

환자앱은 동일 구조를 강제하기보다 단순화/확대 규칙을 더 명확히 해야 한다.

### 7. 의료진웹/요양보호사앱 차별 강화

현재 `medical`, `doctor`, `nurse`, `caregiver`가 모두 같은 green이다. 통일성에는 좋지만 의료진웹과 요양보호사앱의 사용 맥락이 달라서 구분감이 부족하다.

권장:

- primary accent는 green으로 유지
- 의료진웹: dense, calm, table-friendly surface
- 요양보호사앱: 현장 입력 중심, 더 큰 row/touch, warmer neutral
- 색 자체 분리보다 surface tint, icon background, density token으로 차이 주기

### 8. 프리뷰 페이지 공통 구조 통일

하위 페이지는 `.pv-nav`, `.pv-header`, `.pv-container` 체계가 있는데 메인 `preview.html`은 별도 `.hero`, `.container`, `.preview-card` 스타일을 쓴다. 허브 페이지라 다를 수 있지만, 디자인 시스템 프리뷰 전체로 보면 약간 별도 랜딩처럼 느껴진다.

권장:

- 메인 preview도 `.pv-*` 구조 일부를 공유
- 카드, section title, footer 스타일을 `_preview-shared.css`로 더 이동
- 프리뷰 전체의 nav/header/card 리듬 통일

### 9. 문서와 토큰 버전 불일치 수정

README/preview는 v3.0, 2026.05.09인데 `tokens.css` 헤더는 v1.0, 2026.04.18이다. SoT 파일이라면 버전 표기가 가장 중요하다.

권장:

- `tokens.css` 헤더를 v3.0 / 2026.05.09로 업데이트
- 변경 이력에 v3.0 토큰 변경 요약 추가

### 10. "5개 앱" 표현과 실제 role 수 정리

문구에는 "보호자·의료진·환자 5개 앱"이라고 되어 있는데, 실제로는 보호자/의료진웹/요양보호사/환자/온보딩인 듯하다. role은 3개, product surface는 5개라서 혼동된다.

권장:

- "3개 역할 테마, 5개 제품 표면"으로 정리
- guardian / medical / caregiver / patient / onboarding의 관계를 표로 명시

## 유지하면 좋은 점

- `preview.html`을 허브로 나눈 구조는 좋다.
- `preview-foundations`, `preview-components`, `preview-patterns`, `preview-roles` 분리는 명확하다.
- Fluent Filled 단일화, 이모지 금지, AI 진입점=하루안부 심볼 원칙은 유지.
- Roles Side-by-Side 페이지는 방향이 좋으니 실제 토큰 기반으로만 더 다듬으면 된다.
- 모바일 오버플로우는 Roles 페이지 기준 큰 문제 없음.

## Claude 작업 체크리스트

- [ ] `tokens.css`에 `--color-accent-rgb` 추가
- [ ] patient + mobile 토큰 우선순위 충돌 수정
- [ ] preview 계열 파일의 실제 컴포넌트 스타일을 토큰 기반으로 치환
- [ ] `preview.html` 첫 화면에 3-role 신호 강화
- [ ] "색만 바뀐다" 문구를 "색 + 접근성 스케일"로 수정
- [ ] glass 기본 원칙을 감성형/업무형 화면으로 분리
- [ ] 의료진웹/요양보호사앱 차이를 density/surface token으로 정리
- [ ] 메인 preview와 하위 preview의 nav/header/card 리듬 통일
- [ ] `tokens.css` 헤더 버전/날짜 업데이트
- [ ] "3개 역할 테마, 5개 제품 표면" 관계를 문서화

## 한 줄 결론

현재 디자인 시스템은 구조는 좋아졌지만, 프리뷰 코드가 아직 토큰 시스템을 완전히 따르지 않는다. Claude는 우선 하드코딩 제거, 환자 토큰 충돌 수정, `--color-accent-rgb` 추가, glass 원칙 재정의, 3-role 시각 균형 강화를 진행하면 된다.
