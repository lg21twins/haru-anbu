# Claude 전달용 디자인 시스템 리뷰

대상 파일: `07_디자인/preview.html`, `07_디자인/tokens/tokens.css`, `07_디자인/README.md`, `07_디자인/01_FOUNDATIONS.md`, `07_디자인/02_COMPONENTS.md`, `07_디자인/03_PATTERNS.md`

작성일: 2026-05-09

## 총평

현재 디자인 시스템 v3.0은 방향성이 좋다. 역할별 색상, 공통 컴포넌트, Fluent Filled 아이콘 단일화, 이모지 금지, 알림 위계, AI 리포트 패턴까지 묶은 점은 하루안부를 하나의 제품군처럼 보이게 만드는 데 도움이 된다.

다만 지금 상태는 실제 구현 가능한 디자인 시스템이라기보다 선언적 가이드에 가깝다. 특히 토큰과 문서가 맞지 않는 부분, 업무형 화면에 과한 글래스모피즘, 환자앱 접근성 특수성 부족, preview.html의 샘플 코드 품질 문제가 있다. 아래 항목을 우선 수정해달라.

## 최우선 수정

### 1. 환자 토큰이 mobile 토큰에 덮이는 문제 수정

`tokens.css`에서 `[data-role="patient"]`는 본문 18px, headline 20px, title 24px, touch target 56px로 상향한다. 하지만 뒤쪽의 `[data-platform="mobile"]`에서 `--text-body: 16px`, `--size-touch-target: 44px`를 다시 선언하고 있어 환자 접근성 토큰이 깨질 수 있다.

수정 방향:

- `[data-role="patient"]` 규칙을 platform 규칙 뒤로 옮기거나,
- `[data-role="patient"][data-platform="mobile"]` 조합 규칙을 추가한다.

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

### 2. `--color-accent-rgb` 토큰 추가

`02_COMPONENTS.md`에서 아래처럼 `rgba(var(--color-accent-rgb), ...)`를 사용하고 있다.

```css
box-shadow: 0 8px 28px rgba(var(--color-accent-rgb), 0.25);
border-color: rgba(var(--color-accent-rgb), 0.12);
```

하지만 `tokens.css`에는 `--color-accent-rgb`가 없다. 그대로 구현하면 그림자와 보더가 깨진다.

수정 방향:

```css
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

기본 `:root`에도 guardian 기준 fallback을 넣어두는 것이 좋다.

### 3. 글래스모피즘 기본 원칙 완화

현재 README는 "글래스모피즘이 기본"이라고 되어 있다. 보호자앱 홈, AI 리포트, 온보딩처럼 감성/안심을 주는 화면에는 잘 맞는다. 그러나 의료진웹과 요양보호사앱처럼 반복 입력, 빠른 스캔, 업무 효율이 중요한 화면에서는 모든 카드가 glass이면 가독성과 정보 밀도가 떨어질 수 있다.

수정 방향:

- 보호자앱/온보딩/AI 리포트: glass 적극 사용
- 의료진웹/요양보호사앱: flat/card-row를 기본, glass는 요약/강조 영역에 제한
- 환자앱: 큰 CTA와 명확한 표면 우선, glass는 과하게 쓰지 않음

문구 변경 제안:

기존:

> 글래스모피즘이 기본

수정:

> 감성형 화면은 글래스, 업무형 화면은 플랫. 보호자 홈·AI 리포트·온보딩은 glass를 기본으로 쓰되, 의료진웹·요양보호사 입력 화면은 flat/card-row를 기본으로 사용한다.

### 4. preview.html도 토큰 기반으로 정리

문서에서는 "컴포넌트는 hex를 직접 적지 않는다"고 하지만 `preview.html`에는 hex와 inline style이 많다. 프리뷰 파일이라 예외일 수 있지만, Claude나 팀원이 샘플 코드로 복붙할 가능성이 크다.

수정 방향:

- 가능한 hex 직접 사용을 CSS 변수로 대체
- role card, swatch 등 설명 목적의 hex 표기는 유지 가능
- 실제 컴포넌트 예시는 반드시 semantic/component token 사용
- `blur(16px)`처럼 문서와 토큰이 다른 값은 `var(--blur-card)`로 통일

## 중간 우선순위 수정

### 5. 역할별 색상 차이를 조금 더 정교하게

현재 구조는 보호자=블루, 의료진/요양보호사=그린, 환자=오렌지로 명확하다. 이해하기 쉽지만 의료진웹과 요양보호사앱이 같은 그린으로 묶이면 직군 차이가 약해질 수 있다.

수정 방향:

- 구조와 primary accent는 유지
- 의료진웹은 조금 더 차분한 green surface
- 요양보호사앱은 현장성 있는 green tint 또는 warmer neutral 보조 표면
- 색 자체를 완전히 분리하지 말고 surface tint, icon background, chart color 정도에서 구분

### 6. 환자앱 접근성 규칙 강화

환자앱은 18px 본문과 56px 터치만으로는 부족할 수 있다. 고령 사용자를 고려하면 화면 구조 자체가 단순해야 한다.

추가 규칙 제안:

- 첫 화면 CTA는 1-2개만 노출
- 아이콘 단독 금지, 모든 주요 아이콘에 텍스트 라벨 병기
- 카드 수를 줄이고 한 화면의 선택지를 제한
- 상태 문구는 짧고 직접적으로 작성
- 색상만으로 상태를 전달하지 말고 텍스트와 아이콘을 함께 사용

### 7. "하루안부만의 고유함" 강화

현재 문서는 Apple Health, Toss, KRDS, M3의 좋은 점을 잘 가져왔지만, 하루안부만의 고유한 시각/언어 장치는 아직 약하다.

강화할 수 있는 방향:

- "오늘의 한 문장"을 핵심 브랜드 패턴으로 격상
- 가족에게 전달되는 말투와 의료진 기록 말투의 변환 규칙 명시
- 안부 리듬: 하루 단위, 저녁 확인, 주간 흐름을 UI 패턴으로 정리
- AI 리포트의 문장 톤을 디자인 시스템 일부로 포함

## 낮은 우선순위 수정

### 8. preview에 role/platform 전환 예시 추가

현재 preview는 `data-platform="mobile"`만 선언되어 있고, 실제 역할별 화면이 어떻게 변하는지 충분히 보여주지 않는다.

추가 제안:

- guardian / medical / caregiver / patient 토글
- mobile / web 토글
- 같은 버튼/카드/탭바가 역할별로 어떻게 바뀌는지 한 섹션에 표시

### 9. 의료진웹은 모바일 탭바보다 웹 셸을 더 전면에

프리뷰에서는 플로팅 필 탭바가 강한 시그니처로 보인다. 보호자앱과 환자앱에는 좋지만, 의료진웹은 sidebar/topbar 패턴이 더 중요하다.

수정 방향:

- preview에 의료진웹 sidebar/topbar 샘플 추가
- "탭바는 모바일 앱 시그니처, 의료진웹은 sidebar/topbar가 기본"이라고 명시

### 10. 문서 내부 용어와 버전 정리

README에는 v3.0인데 `tokens.css` 헤더는 v1.0 / 2026.04.18로 되어 있다. 문서 묶음이 v3.0이라면 토큰 파일 헤더도 현재 상태를 반영해야 한다.

수정 방향:

- `tokens.css` 헤더 버전과 날짜 업데이트
- README의 `v11_보호자앱 이전 작업` 표현 확인. 현재 프로젝트 구조상 보호자앱은 v9.5, 의료진웹 v10, 요양보호사앱 v11, 환자앱 v12로 보인다.

## Claude 작업 체크리스트

- [ ] `tokens.css`에서 patient + mobile 토큰 우선순위 충돌 수정
- [ ] `--color-accent-rgb` 기본값과 역할별 값을 추가
- [ ] `README.md`의 "글래스모피즘 기본" 원칙을 화면 유형별 원칙으로 완화
- [ ] `02_COMPONENTS.md`의 코드 예시가 실제 `tokens.css`에 존재하는 토큰만 쓰는지 점검
- [ ] `preview.html`의 실제 컴포넌트 예시를 semantic/component token 기반으로 정리
- [ ] 환자앱 접근성 규칙을 `01_FOUNDATIONS.md`와 `03_PATTERNS.md`에 보강
- [ ] 의료진웹/요양보호사앱은 업무형 화면 원칙을 별도로 명시
- [ ] role/platform 전환 예시를 preview에 추가
- [ ] 문서 버전과 날짜, 앱 버전 표기를 정리
- [ ] 실제 화면 1개씩 보호자/의료진/요양보호사/환자에 토큰을 적용해 검증

## 유지하면 좋은 점

- 역할별 accent 구조는 유지
- Fluent Filled 아이콘 단일화 유지
- 이모지 절대 금지 유지
- SOS/주의/정보 알림 위계 유지
- AI 리포트의 "진단하지 않음, 처방 제안 금지, 사실과 수치 분리" 원칙 유지
- "하나의 차체, 세 개의 테마" 방향 유지

## 한 줄 결론

이 디자인 시스템은 방향은 맞지만, 바로 구현에 들어가기 전에 토큰 충돌과 문서/코드 불일치를 먼저 잡아야 한다. 이후 glass를 업무형 화면에서 완화하고, 환자앱 접근성과 하루안부 고유 패턴을 강화하면 훨씬 단단한 시스템이 된다.
