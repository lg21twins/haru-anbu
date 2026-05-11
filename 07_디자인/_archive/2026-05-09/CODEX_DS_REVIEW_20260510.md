# 하루안부 디자인 시스템 리뷰 및 개선안

작성일: 2026-05-10  
리뷰 대상: `07_디자인/preview.html`, `tokens/tokens.css`, `preview-*.html`, `01_FOUNDATIONS.md`, `02_COMPONENTS.md`, `03_PATTERNS.md`  
작성 목적: 클로드가 만든 새 디자인 시스템이 실제 사용자별 앱에 적용될 수 있는지 판단하고, 더 깔끔하고 통일된 제품 경험으로 만들기 위한 건설적 개선안 정리

---

## 1. 결론

새 디자인 시스템의 방향은 좋다. 특히 `tokens.css`를 중심으로 역할별 테마와 플랫폼별 치수를 나누고, 환자 앱은 자동으로 글자와 터치 타깃을 키우는 구조는 현재 앱들의 문제를 해결하는 데 도움이 된다.

다만 지금 상태 그대로 전체 앱에 적용하기에는 아직 이르다. 이유는 명확하다.

1. 문서와 프리뷰 사이에 v3.0 / v3.1 철학이 섞여 있다.
2. `tokens.css`는 "flat 기본, glass 예외"라고 말하지만, 일부 프리뷰는 여전히 "glass 기본"처럼 보여준다.
3. 컴포넌트 명세와 실제 프리뷰 클래스명이 다르다.
4. 역할별 통일성은 좋아졌지만, 의료진과 요양보호사 구분은 아직 약하다.
5. 실제 앱에 적용할 때 공통 컴포넌트 CSS가 부족해서 화면별 재구현이 반복될 가능성이 크다.

즉, 이 디자인 시스템은 "적용하면 좋아질 수 있는 기반"이다. 하지만 먼저 시스템 내부의 모순을 정리하고, 파일럿 화면 1~2개에 적용해 검증한 뒤 확장하는 것이 좋다.

---

## 2. 잘한 점

### 2.1 토큰 중심 구조가 생겼다

`tokens/tokens.css`는 primitive, semantic, component layer로 나뉘어 있고, 이 방향은 맞다. 화면 코드가 직접 hex를 쓰지 않고 `--color-accent`, `--color-bg-surface`, `--card-padding` 같은 semantic token을 보게 만들면 장기적으로 유지보수가 쉬워진다.

특히 좋은 구조:

- `data-role="guardian"`: 보호자 블루
- `data-role="medical"`, `doctor`, `nurse`, `caregiver`: 의료/돌봄 그린
- `data-role="patient"`: 환자 오렌지
- `data-platform="mobile"` / `web`: 화면 밀도와 터치 기준 분리

이 구조는 지금 앱들이 역할별로 따로 노는 문제를 줄여준다.

### 2.2 환자 접근성 상향 규칙이 좋다

환자 역할에서 본문, 헤드라인, 버튼, 행 높이, 터치 타깃을 자동으로 키우는 방향은 매우 적절하다. 환자 앱은 고령 사용자를 전제로 하므로, 색만 바꾸는 테마가 아니라 조작 난이도 자체를 낮춰야 한다.

좋은 결정:

- 환자 본문 18px
- 환자 터치 타깃 56px
- 환자 행 높이 64px
- 환자 카드는 더 여유 있는 padding

이건 기존 환자앱의 방향성과도 잘 맞는다.

### 2.3 "Flat 기본, Glass 예외" 정책은 맞다

현재 앱들은 예쁜 대신 glass, radial gradient, blur, shadow가 화면마다 많이 들어가 있다. 보호자앱은 감성적으로 어울리지만, 의료진/요양보호사 업무 화면에서는 정보 판단을 방해할 수 있다.

따라서 v3.1의 정책은 좋다.

- 일반 정보 카드: 흰 surface + 1px border + 약한 shadow
- glass: 탭바, 모달, AI 리포트, 환자 가족 사진 카드 등 제한적 사용
- 위험/긴급 정보: 장식보다 상태 색상과 정보 위계 우선

이 방향으로 가면 훨씬 깔끔해진다.

### 2.4 카드 타입 4종 고정은 좋은 정리다

`02_COMPONENTS.md`의 카드 4종 정의는 실무적으로 좋다.

- `card-default`: 대부분의 정보 카드
- `card-action`: 클릭 가능한 카드
- `card-alert`: 위험/주의/상태 강조
- `card-hero`: 화면당 최대 1개

이 규칙을 적용하면 화면마다 "이번엔 어떤 카드 스타일을 쓰지?"라는 고민이 줄어든다.

---

## 3. 가장 큰 문제

### 3.1 디자인 시스템 내부 철학이 아직 충돌한다

가장 먼저 고쳐야 할 부분이다.

`tokens.css`와 `02_COMPONENTS.md`는 v3.1 기준으로 "flat 기본, glass 예외"를 말한다. 그런데 `preview.html`의 핵심 원칙에는 아직 "글래스모피즘이 기본"이라고 적혀 있다.

이 상태로 다른 사람이 보면 기준을 헷갈린다.

수정 방향:

```md
기존:
글래스모피즘이 기본 — 카드는 반투명 흰색 + blur...

수정:
Flat surface가 기본 — 일반 정보 카드는 흰 surface + 1px border + 약한 shadow.
Glass는 탭바, 모달, AI 리포트, 환자 가족 사진 카드처럼 감성/플로팅 맥락에만 제한적으로 사용한다.
```

### 3.2 프리뷰 페이지가 새 정책을 아직 반영하지 못했다

`preview-components.html`, `preview-patterns.html`, `preview-roles.html`에는 아직 구버전 glass 중심 예시가 남아 있다.

문제 예:

- `card · glass (기본)` 같은 표현
- 보호자 홈 패턴에서 `c-glass` 카드 반복
- 탭바가 역할별 tinted glass로 표시됨
- 배경이 여전히 강한 radial gradient 중심

이건 실제 앱에 적용할 때 혼선을 만든다. 문서는 "glass 줄여라"라고 말하는데 프리뷰는 "glass 쓰면 예쁘다"라고 말하는 상태다.

수정 방향:

- 모든 일반 정보 카드는 `card-default` 예시로 교체
- 클릭 카드는 `card-action`
- 위험/주의는 `card-alert`
- glass 예시는 별도 "예외 사용" 섹션으로 격리
- 탭바는 역할별 배경 tint가 아니라 공통 흰 반투명 + active만 role accent

### 3.3 실제 앱 적용용 공통 CSS가 부족하다

현재 `tokens.css`는 값의 시스템이다. 하지만 실제 앱에서 바로 쓸 수 있는 `.app-shell`, `.app-header`, `.tabbar`, `.card`, `.btn`, `.badge`, `.sos`, `.fab-ai` 같은 제품 컴포넌트 CSS는 아직 부족하다.

이 상태에서 각 앱 화면에 적용하면 개발자가 다시 화면마다 CSS를 만들게 된다. 그러면 지금과 같은 문제가 반복된다.

필요한 파일 제안:

```text
07_디자인/system/
├── app.css              # reset + app shell + page layout
├── components.css       # button, card, badge, tabbar, header, FAB, SOS
├── patterns.css         # home, report, checklist, chat, patient tablet 패턴
└── README.md            # import 순서와 사용 규칙
```

권장 import:

```html
<link rel="stylesheet" href="../07_디자인/tokens/tokens.css">
<link rel="stylesheet" href="../07_디자인/system/app.css">
<link rel="stylesheet" href="../07_디자인/system/components.css">
```

### 3.4 의료진과 요양보호사의 구분이 약하다

현재 의료진, 간호사, 요양보호사는 같은 green accent를 공유한다. 같은 제품군처럼 보이는 장점은 있지만, 실제 사용 맥락은 꽤 다르다.

의료진:

- 빠른 판단
- 위험 환자 우선
- 정보 밀도 높음
- desktop/web 가능성 큼

요양보호사:

- 현장 한 손 조작
- 체크리스트/기록 중심
- 큰 터치 타깃
- 다국어/가독성 고려

둘을 완전히 다른 색으로 나누자는 뜻은 아니다. 같은 green 계열을 유지하되 surface, 밀도, 컴포넌트 크기로 역할 차이를 줘야 한다.

개선안:

- 의료진: 더 차분하고 dense한 surface, 작은 row, table/list 중심
- 요양보호사: 더 큰 row, 더 큰 button, 더 명확한 CTA, 현장 기록 중심
- `data-role="caregiver"`는 accent는 같더라도 `--size-touch-target`, `--size-row`, `--card-padding` 차이를 더 명확히 적용

### 3.5 원시 팔레트 직접 사용이 아직 많다

문서에서는 화면 코드가 primitive token을 직접 쓰지 말라고 되어 있다. 하지만 프리뷰 예시에서는 `--brand-blue-500`, `--brand-green-100`, hex, rgba가 많이 쓰인다.

프리뷰 문서라 어느 정도는 괜찮지만, 실제 앱에 적용할 기준 파일에서는 semantic token 사용을 강제해야 한다.

권장:

- 앱 화면에서는 `--brand-*` 직접 사용 금지
- 예외: 파운데이션 문서에서 색상 팔레트 보여줄 때만 허용
- 앱/패턴 예시에서는 `--color-accent`, `--color-accent-soft`, `--color-bg-role-gradient`, `--card-bg`, `--color-danger` 사용

---

## 4. 적용하면 기존 앱이 좋아질 부분

### 4.1 보호자앱

현재 보호자앱은 화면별 스타일 편차가 가장 크다. 일부는 liquid glass, 일부는 일반 card, 일부는 직접 SVG icon, 일부는 iconify가 섞여 있다.

DS 적용 효과:

- 탭바 통일
- AI FAB 브랜드 심볼 통일
- 카드 스타일 정리
- blue accent 일관화
- 구 토큰 `--blue`, `--t1` 같은 alias 의존도 감소

개선 포인트:

- `g-ai.html`의 cyan 계열 `#22D3EE`, `#0891B2`를 role accent 또는 AI 전용 semantic token으로 정리
- 탭바 직접 SVG와 iconify 혼용 제거
- active tab 정확히 수정
- glass background는 AI/감성 영역에만 유지하고, 일반 정보는 flat card로 교체

### 4.2 요양보호사앱

요양보호사앱은 UX 흐름이 좋다. 지금 할 일, 관찰 카드, 인수인계, 담당자 목록의 순서가 실무적이다.

DS 적용 효과:

- field app답게 더 안정적이고 덜 장식적인 화면이 됨
- 버튼/카드/배지 크기 정리
- caregiver의 큰 터치 타깃이 유지됨

개선 포인트:

- green gradient와 orb를 더 약하게
- 카드 대부분을 flat으로
- 위험/주의 정보는 `card-alert`로 통일
- "지금 기록 시작" 같은 primary CTA는 화면당 1개만 유지

### 4.3 환자앱

환자앱은 방향이 가장 명확하다. 큰 글자, 큰 버튼, 가족 연결감이 좋다. 다만 홈 화면 정보량은 많다.

DS 적용 효과:

- 환자 접근성 token이 자동 적용됨
- orange accent가 과하지 않게 정리됨
- 큰 카드/큰 버튼 기준이 일관됨

개선 포인트:

- 홈 화면은 지금보다 더 줄이는 것이 좋다.
- 한 화면에 가족 메시지, 빠른 답장, 음성 버튼, 가족 전화, 약 복용, 일정 전체, 도움 버튼이 동시에 보이면 고령 사용자에게 많다.
- 일정 리스트는 "지금 + 다음 1개"만 홈에 두고 전체는 별도 화면으로 이동.
- 환자 화면의 primary action은 항상 하나만 크게 보여야 한다.

### 4.4 의료진앱 / 의료진웹

의료진앱은 정보 위계가 좋다. 위험 환자, 다음 3가지, 주의 환자 목록이 명확하다.

DS 적용 효과:

- 위험/주의/일반 상태 카드가 명확히 나뉨
- 초록 accent가 업무 화면에서 덜 과해짐
- web/mobile density 차이를 토큰으로 관리 가능

개선 포인트:

- 의료진 화면에서는 glass 거의 금지
- alert는 `card-alert--danger` 또는 명확한 danger hero로
- green accent와 success green이 충돌하지 않도록 success는 작은 배지/아이콘에만 사용
- table/list 중심의 dense pattern을 별도 정의

---

## 5. 우선순위 개선안

### P0. 지금 바로 고쳐야 할 것

1. `preview.html`의 핵심 원칙 2번 수정
   - "글래스모피즘이 기본" 삭제
   - "Flat surface가 기본, glass는 제한적 사용"으로 변경

2. 모든 프리뷰 버전 표기 통일
   - 현재 v3.0 / v3.1 혼재
   - 실제 철학은 v3.1이므로 `preview*.html` 제목, nav, footer를 v3.1로 통일

3. `preview-components.html`의 card 예시 수정
   - `card · glass (기본)` 제거
   - `card-default`, `card-action`, `card-alert`, `card-hero` 순서로 재구성

4. `preview-patterns.html`의 일반 정보 카드에서 `c-glass` 제거
   - 2x2 요약 카드, 업무 카드, 대시보드 카드 모두 flat card로 교체

5. 탭바 예시를 token 정책과 일치
   - 배경은 `--tabbar-bg`
   - active icon/text만 `--color-accent`
   - 역할별 tinted tabbar 제거

### P1. 실제 앱 적용 전 해야 할 것

1. `system/components.css` 생성
2. 실제 앱에서 공통으로 쓸 클래스 확정
3. 보호자 홈 1개, 요양보호사 홈 1개, 환자 홈 1개, 의료진 홈 1개를 파일럿으로 변환
4. 변환 전후 비교 기준 정의

비교 기준:

- hex 하드코딩 수 감소
- inline style 수 감소
- 카드 타입 4종 준수 여부
- primary CTA 화면당 1개 여부
- 환자 터치 타깃 56px 이상 여부
- glass 사용 위치 제한 여부

### P2. 전체 적용

1. 보호자앱 전체 탭바/헤더/카드부터 정리
2. 요양보호사앱 체크리스트/소통/마이페이지 정리
3. 환자앱 정보량 축소 및 접근성 토큰 적용
4. 의료진앱/웹 dense pattern 적용
5. 온보딩은 마지막에 브랜드 감성 화면으로 별도 polish

---

## 6. 권장 디자인 원칙 최종안

아래 5개를 최종 원칙으로 잡는 것이 좋다.

### 1. 하나의 제품군, 역할별 accent만 다르게

구조, radius, spacing, card, tabbar는 동일하게 간다. 역할별 차이는 큰 면적 색칠이 아니라 active state, CTA, 작은 badge, focus ring으로 준다.

### 2. Flat first, glass selective

일반 정보 카드는 flat. glass는 플로팅/감성/AI/가족 사진 같은 제한된 맥락에서만 쓴다.

### 3. 화면당 hero는 하나만

카드마다 강조하면 아무것도 강조되지 않는다. 각 화면에는 가장 중요한 카드 1개만 hero로 둔다.

### 4. 환자는 정보량보다 행동 명확성

환자앱은 많은 정보를 보여주는 앱이 아니라, 지금 할 일을 쉽게 하게 만드는 앱이다. CTA는 크고 명확해야 하며, 일정/상세 정보는 별도 화면으로 빼는 것이 낫다.

### 5. 업무 화면은 예쁨보다 판독성

의료진/요양보호사 화면은 감성보다 판단 속도가 중요하다. 위험, 주의, 완료, 예정 상태가 즉시 구분되어야 한다.

---

## 7. 앱 적용 체크리스트

### 공통

- [ ] `tokens.css`를 첫 번째로 import했는가
- [ ] `html`에 `data-role`, `data-platform`이 있는가
- [ ] 화면 코드에서 hex를 직접 쓰지 않았는가
- [ ] 일반 카드는 `card-default`인가
- [ ] glass를 일반 정보 카드에 쓰지 않았는가
- [ ] primary CTA가 화면당 1개 이하인가
- [ ] 탭바는 모든 앱에서 같은 구조인가
- [ ] iconify fluent 계열로 통일했는가
- [ ] 이모지를 쓰지 않았는가

### 보호자

- [ ] 블루 accent가 CTA/active/badge 중심으로만 쓰이는가
- [ ] AI 진입점이 sparkle이 아니라 하루안부 심볼인가
- [ ] 리포트/상태 카드는 과도한 blur 없이 읽기 쉬운가

### 요양보호사

- [ ] 주요 버튼이 48px 이상인가
- [ ] 지금 할 일이 화면에서 가장 먼저 보이는가
- [ ] 위험/주의 상태가 `card-alert`로 구분되는가
- [ ] 다국어 폰트 fallback이 유지되는가

### 환자

- [ ] 터치 타깃이 56px 이상인가
- [ ] 본문 18px 이상인가
- [ ] 한 화면에 너무 많은 액션이 있지 않은가
- [ ] "지금 할 일"이 가장 크게 보이는가

### 의료진

- [ ] 정보 밀도가 업무에 맞게 충분한가
- [ ] 위험 환자가 가장 먼저 보이는가
- [ ] success green과 role green이 충돌하지 않는가
- [ ] 데스크톱 웹은 dense layout을 쓰는가

---

## 8. 최종 판단

이 디자인 시스템은 현재 앱을 더 깔끔하고 통일성 있게 만드는 데 도움이 된다. 특히 기존 앱의 문제였던 화면별 색상 편차, 과한 glass, 탭바/아이콘 혼용, 환자 접근성 기준 부족을 해결할 수 있다.

하지만 지금의 `preview.html`만 기준으로 삼으면 안 된다. `tokens.css`, `02_COMPONENTS.md`, `03_PATTERNS.md`의 v3.1 정책이 더 올바른 방향이다.

따라서 권장 결론은 다음과 같다.

> 적용해도 된다. 단, 먼저 DS 프리뷰 내부의 v3.0 흔적과 glass 기본 철학을 제거하고, `Flat first / Glass selective` 기준으로 프리뷰와 컴포넌트를 정리한 뒤 앱에 적용해야 한다.

가장 좋은 다음 단계는 "디자인 시스템 정리 → 보호자 홈 1개 파일럿 적용 → 환자 홈 정보량 축소 → 요양/의료진 업무 카드 정리" 순서다.

