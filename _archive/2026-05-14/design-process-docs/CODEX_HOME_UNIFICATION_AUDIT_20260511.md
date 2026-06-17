# 하루안부 3개 앱 홈 화면 통일성 감사 및 개선 지시서

작성일: 2026-05-11  
작성자: Codex  
대상 화면:

- 보호자앱 홈: `v11_보호자앱/g-guardian-live.html`
- 요양보호사앱 홈: `v11_요양보호사앱/c01-today.html`
- 의료진앱 홈: `v15_의료진앱/d01-home.html`

목적:

세 홈 화면이 현재 “하루안부라는 같은 제품군”으로 느껴지는지 확인하고, 디자인 시스템·홈 구조·버튼 위치·탭바·헤더·카드 문법·CTA 위치 관점에서 무엇을 고쳐야 하는지 클로드가 바로 실행할 수 있게 정리한다.

## 0. 결론

현재 세 홈은 같은 서비스라기보다 **각각 다른 앱/다른 시안 라인**처럼 보인다.

가장 큰 원인은 색이 아니다. 다음 네 가지가 더 크다.

1. **보호자앱 홈이 디자인 시스템 밖에 있다.**
   - `data-role`, `data-platform`, `tokens.css`, `_app-theme.js`가 없다.
   - 로컬 변수 `--blue`, `--green`, `--t1` 등을 직접 정의한다.
   - AI 오브, 인트로, 리포트 시트가 너무 강해서 제품 공통 골격이 사라진다.

2. **세 홈의 “첫 화면 뼈대”가 다르다.**
   - 보호자: 감성 인사 + AI 오브 + 리포트 시트
   - 요양보호사: 근무 스트립 + 관찰 카드 + 지금 기록 카드
   - 의료진: 근무 인사 + 위험 환자 alert + 다음 3가지

3. **주요 액션 위치가 다르다.**
   - 보호자: AI 채팅 힌트, 일일 리포트 버튼, 하단 AI FAB, 채팅 입력창이 분산됨
   - 요양보호사: 히어로 카드 하단에 `지금 기록 시작`이 명확함
   - 의료진: 위험 alert는 있지만 `지금 확인`, `회진 시작` 같은 명시 primary action이 약함

4. **하단 바는 비슷하지만 규격과 의미가 다르다.**
   - 보호자: 탭바 + AI FAB
   - 요양보호사: 탭바 + SOS
   - 의료진: 탭바 + SOS
   - 위치와 개념은 유사하지만 높이, inset, 배경, 탭명, active 처리, FAB 의미가 다르다.

따라서 개선 방향은 “세 화면을 똑같이 만들기”가 아니다.  
**같은 위치에 같은 의미의 요소를 두고, 역할별 내용만 바꾸는 것**이다.

## 1. 스크린샷 근거

검증 당시 viewport: 390 x 844 모바일 기준.

스크린샷은 repo 안에 보존했다.

| 화면 | 파일 |
|---|---|
| 보호자앱 홈, 인트로 스킵 후 | `07_디자인/review-assets/guardian-home-after-skip-20260511.png` |
| 요양보호사앱 홈 | `07_디자인/review-assets/caregiver-home-20260511.png` |
| 의료진앱 홈 | `07_디자인/review-assets/medical-home-20260511.png` |

### 1.1 보호자앱 홈 스크린샷 관찰

![보호자 홈](review-assets/guardian-home-after-skip-20260511.png)

관찰:

- 첫 화면의 주인공은 “오늘도 수고하셨어요, 영자님 잘 있어요” 감성 문장과 큰 청록 AI 오브다.
- 상단에는 로고, 알림, 프로필이 있으나 36px 수준으로 작고, 다른 앱의 48px 헤더 버튼과 다르다.
- `AI 채팅하기` 힌트가 화면 중앙에 떠 있고, 그 아래 리포트 시트가 화면을 크게 덮는다.
- 리포트 시트가 홈 본문 역할을 하며, 카드와 차트가 그 안에 들어간다.
- 하단은 탭바 + AI FAB 구조다.
- 좋은 점: 보호자에게 감성적이고 AI 중심의 경험은 강하다.
- 문제: 요양보호사/의료진앱과 같은 제품군의 홈 구조로 읽히지 않는다.

### 1.2 요양보호사앱 홈 스크린샷 관찰

![요양보호사 홈](review-assets/caregiver-home-20260511.png)

관찰:

- 화면 상단부터 “근무 중인 현장 앱” 느낌이 명확하다.
- 헤더 우측 알림/마이 버튼은 48px로 명확하고 현장 터치성이 좋다.
- 근무 상태 스트립, 관찰 카드, 지금 할 일 카드, 기록 시작 버튼 순서가 실무적이다.
- `지금 기록 시작` CTA가 첫 화면 중앙 카드 하단에 있어 다음 행동이 명확하다.
- 하단 탭바 + SOS 구조가 의료진앱과 닮아 있다.
- 문제: 의료진앱과 같은 그린 역할권인데도 카드 반경, 헤더 높이, 여백, 로고 표현, 섹션 구조가 다르다.
- 문제: 담당 목록이 하단 탭바와 시각적으로 겹쳐 보이는 구간이 있다.

### 1.3 의료진앱 홈 스크린샷 관찰

![의료진 홈](review-assets/medical-home-20260511.png)

관찰:

- 헤더, 근무 인사, 위험 환자 alert, 다음 3가지 순서로 의료진 업무 우선순위는 분명하다.
- 요양보호사앱과 하단 탭바 + SOS 구조가 비슷하다.
- 위험 alert 카드가 크고 강해서 “즉시 확인”의 중요성은 보인다.
- 문제: alert 카드 안에 명시적인 primary action이 없다. 카드 전체가 링크이긴 하지만 버튼으로 읽히지 않는다.
- 문제: `다음 3가지` 세 번째 카드가 하단 탭바와 겹쳐 보인다.
- 문제: `data-role`, `tokens.css`는 쓰지만 공용 `system/app.css`, `system/components.css`를 쓰지 않아 시스템 편입이 반쯤만 되어 있다.

## 2. 파일 구조 감사

### 2.1 보호자앱 홈

대상:

```text
v11_보호자앱/g-guardian-live.html
```

핵심 문제:

```html
<html lang="ko">
```

근거: `g-guardian-live.html:2`

보호자 홈은 `data-role="guardian"`과 `data-platform="mobile"`이 없다. 이 때문에 `tokens.css`의 역할 테마, 다크 모드, 접근성 토큰과 연결되지 않는다.

현재 import:

```html
<link rel="stylesheet" href="pretendard.css">
<script src="../07_디자인/_iconify-icon.min.js"></script>
```

근거: `g-guardian-live.html:13-14`

누락된 것:

```html
<link rel="stylesheet" href="../07_디자인/tokens/tokens.css">
<script src="../07_디자인/_app-theme.js"></script>
<link rel="stylesheet" href="../07_디자인/system/app.css">
<link rel="stylesheet" href="../07_디자인/system/components.css">
```

로컬 변수:

```css
:root {
  --blue:#2C7AFC;
  --blue-l:#5B9BFF;
  --blue-d:#1D6AF2;
  --green:#34D399;
  --green-d:#059669;
  --amber:#F59E0B;
  --red:#EF4444;
  --t1:#111827;
  --t2:rgba(0,0,0,.5);
  --t3:rgba(0,0,0,.35);
}
```

근거: `g-guardian-live.html:19-28`

문제:

- 디자인 시스템의 semantic token을 우회한다.
- 다크 모드와 고대비 모드가 제대로 반영될 수 없다.
- 다른 앱의 `--color-accent`, `--color-text-primary`, `--color-bg-canvas` 등과 분리된다.

AI 오브:

```css
.ai-orb-bg { ... }
.ai-orb { background: radial-gradient(...); filter: blur(24px); animation: orbBreath ... }
```

근거: `g-guardian-live.html:39-60`

문제:

- 보호자 홈의 시각 주인공이 디자인 시스템 카드/헤더/탭바가 아니라 AI 오브다.
- 브랜드의 따뜻한 AI 경험으로는 좋지만, 다른 앱과 공통된 홈 문법을 압도한다.
- 다크 모드·저전력·reduced motion 대응을 공통 토큰으로 묶기 어렵다.

인트로:

```css
.intro { position: fixed; inset: 0; z-index: 101; ... }
```

근거: `g-guardian-live.html:62-114`

문제:

- 홈 비교와 사용 진입을 방해할 정도로 강하다.
- 매번 보이면 홈이 아니라 온보딩/스플래시처럼 느껴진다.
- 제품군 통일성 관점에서는 최초 1회 또는 온보딩으로 분리해야 한다.

AI 입력:

```css
.chat-input-area { position: fixed; bottom: ... + 104px; ... }
```

근거: `g-guardian-live.html:206-219`

문제:

- 하단 탭바 위에 또 하나의 고정 입력창이 존재한다.
- 보호자 홈의 primary action이 `AI 채팅하기`, `일일 리포트 보기`, AI FAB, 채팅 입력창으로 분산된다.

리포트 시트:

```css
.report-sheet {
  margin-top: calc(37vh + 2px);
  border-radius: 28px 28px 0 0;
  min-height: calc(100vh + 240px);
}
```

근거: `g-guardian-live.html:276-304`

문제:

- 홈 콘텐츠가 일반 카드가 아니라 대형 bottom sheet처럼 보인다.
- 요양보호사/의료진 홈의 “카드 스택” 문법과 완전히 다르다.

하단 바:

```css
.bottom-bar { bottom: calc(env(safe-area-inset-bottom,0px) + 24px); width: calc(100% - 48px); max-width:370px; }
.tabbar { height:60px; background:rgba(210,225,250,.55); ... }
.ai-fab { width:60px; height:60px; background:rgba(210,225,250,.55); ... }
```

근거: `g-guardian-live.html:421-429`

문제:

- 요양보호사/의료진의 하단 바보다 좌우 inset이 다르다.
- AI FAB가 보호자 역할에서 필요한 것은 맞지만, 표면/크기/그림자 규격은 공통화해야 한다.

아이콘 규칙 위반:

```text
fluent:emoji-24-filled
tabler:pill-filled
```

근거: `g-guardian-live.html:593`, `g-guardian-live.html:1589`

문제:

- 프로젝트 규칙상 이모지 아이콘, tabler 혼용은 지양해야 한다.
- `iconify-icon`은 쓰더라도 `fluent:*` 계열로 통일해야 한다.

### 2.2 요양보호사앱 홈

대상:

```text
v11_요양보호사앱/c01-today.html
```

좋은 점:

```html
<html lang="ko" data-role="caregiver" data-platform="mobile">
```

근거: `c01-today.html:2`

좋은 import:

```html
<link rel="stylesheet" href="../07_디자인/tokens/tokens.css">
<script src="../07_디자인/_app-theme.js"></script>
<link rel="stylesheet" href="../07_디자인/system/app.css">
<link rel="stylesheet" href="../07_디자인/system/components.css">
<link rel="stylesheet" href="caregiver.css">
```

근거: `c01-today.html:15-20`

이 화면은 세 화면 중 디자인 시스템 편입도가 가장 높다.

문제 1: 로컬 토큰 재정의가 많다.

```css
:root {
  --text-body: 18px;
  --size-touch-target: 48px;
  --accent: var(--color-accent);
  --t1: var(--color-text-primary);
  --safe-t: max(env(safe-area-inset-top, 0px), 52px);
  --tab-h: 64px;
  --page-pad: 16px;
}
```

근거: `c01-today.html:31-54`

해석:

- alias 자체는 나쁘지 않지만, 화면마다 `--page-pad`, `--tab-h` 같은 레이아웃 토큰을 직접 정하면 의료진앱과 어긋난다.
- 공통 모바일 홈 규격으로 승격해야 한다.

문제 2: 배경이 토큰이 아니라 커스텀 gradient다.

```css
.bg {
  background:
    radial-gradient(...),
    radial-gradient(...),
    linear-gradient(180deg,#EAF6EE 0%,#F0F8F3 35%,#F4FAF6 100%);
}
```

근거: `c01-today.html:59-66`

해석:

- 디자인 시스템의 “약한 role tint gradient” 원칙과 유사하긴 하다.
- 하지만 의료진앱도 비슷한 gradient를 따로 정의하고 있고, 보호자앱은 완전히 다른 배경을 쓴다.
- `--color-bg-role-gradient` 기반으로 통일하는 편이 좋다.

문제 3: 헤더는 좋지만 의료진과 규격이 다르다.

```css
.header {
  position: sticky;
  padding: calc(var(--safe-t) + 4px) var(--page-pad) 10px;
}
.icon-btn { width: 48px; height: 48px; ... }
```

근거: `c01-today.html:73-101`

해석:

- 48px 버튼은 좋다.
- 하지만 의료진앱은 sticky가 아니고, padding token도 `--pad:22px`라 다르다.
- 보호자앱은 36px 버튼이라 더 다르다.

문제 4: 홈 우선순위가 살짝 흔들린다.

현재 순서:

1. 헤더
2. 근무 상태 스트립
3. 관찰 카드
4. 지금 할 일 hero
5. AI 인수인계
6. 담당 목록

근거:

- `shift`: `c01-today.html:103-127`
- `hero`: `c01-today.html:129-188`
- `handover`: `c01-today.html:190-252`
- `obs-card`: `c01-today.html:254-342`
- `roster`: `c01-today.html:345-423`

문제:

- 스크린샷에서는 관찰 카드가 hero보다 먼저 보인다.
- 사용자의 다음 행동은 `지금 기록 시작`인데, 그 위에 관찰 카드가 먼저 있어 시선이 한 번 꺾인다.

권장:

- `Context Strip` 다음에는 항상 `Priority Card`를 둔다.
- 관찰/주의 카드는 `Priority Card`가 긴급일 때만 첫 카드로 승격하고, 일반 상황에서는 priority 아래로 둔다.

문제 5: 공용 `caregiver.css`가 있는데 화면 내부에 같은 컴포넌트 스타일이 중복된다.

`caregiver.css`는 header, bottom bar, SOS, sheet, toast를 공통화한다고 문서화한다.

근거: `caregiver.css:10-15`, `caregiver.css:62-123`

하지만 `c01-today.html` 내부에도 `.header`, `.icon-btn`, `.bottom-bar`, `.tabbar`, `.sos`, `.sheet` 정의가 많다.

근거: `c01-today.html:73-101`, `c01-today.html:426-520`

해석:

- 공용 CSS와 화면 내부 CSS의 책임 경계가 아직 정리되지 않았다.
- 이 상태에서는 다른 화면과 통일하기 어렵다.

### 2.3 의료진앱 홈

대상:

```text
v15_의료진앱/d01-home.html
```

좋은 점:

```html
<html lang="ko" data-role="medical" data-platform="mobile">
```

근거: `d01-home.html:2`

`tokens.css`와 `_app-theme.js`를 사용한다.

근거: `d01-home.html:10-13`

문제 1: `system/app.css`, `system/components.css`를 쓰지 않는다.

현재 import:

```html
<link rel="stylesheet" href="../07_디자인/tokens/tokens.css">
<script src="../07_디자인/_app-theme.js"></script>
<link rel="stylesheet" href="./_shared.css">
```

근거: `d01-home.html:10-13`

해석:

- 디자인 토큰은 쓰지만 공용 앱 셸/컴포넌트는 쓰지 않는다.
- 요양보호사앱과 같은 하단 바를 거의 복붙으로 다시 만들고 있다.

문제 2: `_shared.css`가 별도 레이아웃 토큰을 만든다.

```css
:root {
  --safe-t: max(env(safe-area-inset-top, 0px), 52px);
  --safe-b: max(env(safe-area-inset-bottom, 0px), 20px);
  --tab-h: 64px;
  --tab-bot: 14px;
  --pad: 22px;
}
```

근거: `_shared.css:26-31`

요양보호사앱:

```css
--tab-bot: 12px;
--page-pad: 16px;
```

근거: `c01-today.html:51-53`

해석:

- 의료진과 요양보호사 모두 현장 모바일 앱인데 좌우 padding, tab bottom, header padding이 다르다.
- 이 차이가 미세하게 “다른 앱” 느낌을 만든다.

문제 3: 위험 alert는 큰데 primary action이 약하다.

```html
<a class="alert" href="d02-round.html?focus=10">
  ...
  <div class="alert-main">최명자 어르신<br>혈압 180/110</div>
</a>
```

근거: `d01-home.html:304-317`

해석:

- 카드 전체가 링크지만 사용자는 버튼으로 인지하지 못할 수 있다.
- `지금 확인`, `보고하기`, `회진 시작` 같은 명시 action이 카드 하단에 있어야 요양보호사앱의 `지금 기록 시작`과 같은 문법이 된다.

문제 4: 하단 탭바가 요양보호사와 거의 같지만 별도 구현이다.

```css
.tab-wrap { bottom: calc(var(--safe-b) + var(--tab-bot)); width: calc(100% - 32px); max-width:398px; }
.tabbar { height: var(--tab-h); background:rgba(255,255,255,.85); ... }
.sos { width:var(--tab-h); height:var(--tab-h); ... }
```

근거: `d01-home.html:229-260`

요양보호사:

```css
.bottom-bar { bottom: calc(var(--safe-b) + var(--tab-bot)); width: calc(100% - 32px); max-width:398px; }
.tabbar { height: var(--tab-h); background: rgba(255,255,255,.8); ... }
.sos { width: var(--tab-h); height: var(--tab-h); ... }
```

근거: `c01-today.html:426-464`

해석:

- 거의 같은 구조인데 클래스명과 세부값이 다르다.
- 이건 공통 컴포넌트로 빼야 한다.

문제 5: 하단 탭바와 콘텐츠 겹침

스크린샷에서 `다음 3가지` 세 번째 카드가 하단 탭바 뒤에 걸린다.

원인 후보:

- 본문 하단 padding은 있지만 첫 화면에서 카드 위치와 하단 고정 바가 충돌한다.
- `next-card` 세 번째가 y=745, h=99이고 탭바가 y=746부터 시작한다.

실측:

```text
medical next-card 3: y=745, h=99
medical tabbar: y=746, h=64
```

권장:

- 홈 첫 화면에서 하단바와 겹치지 않게 `next-list`의 세 번째 카드 노출을 줄이거나, `Priority Card + 2개 Next`까지만 첫 viewport에 보이도록 조정한다.
- 또는 하단 bar 위 영역에 `padding-bottom`을 더 크게 주고, 섹션 간격을 조정한다.

## 3. 같은 앱처럼 보이지 않는 핵심 원인 매트릭스

| 항목 | 보호자앱 | 요양보호사앱 | 의료진앱 | 통일성 판단 |
|---|---|---|---|---|
| `data-role`/`data-platform` | 없음 | 있음 | 있음 | 보호자만 이탈 |
| `tokens.css` | 없음 | 있음 | 있음 | 보호자만 이탈 |
| `_app-theme.js` | 없음 | 있음 | 있음 | 보호자만 이탈 |
| 공용 `system` CSS | 없음 | 있음 | 없음 | 세 앱 불일치 |
| 홈 첫 구조 | AI 오브 + 리포트 시트 | 근무 + 지금 기록 | 근무 + 위험 환자 | 보호자만 완전 별도 |
| 헤더 버튼 크기 | 36px | 48px | 48px | 보호자 이탈 |
| 하단 우측 FAB | AI | SOS | SOS | 역할별 차이는 OK |
| 하단 바 규격 | 60px, inset 24/48 | 64px, inset 12/32 | 64px, inset 14/32 | 부분 불일치 |
| primary action | 분산 | 명확 | 약함 | 재정렬 필요 |
| 카드 문법 | sheet/grid/widget | shift/hero/handover/roster | alert/next/risk | 공통 패턴 없음 |
| 다크 모드 | 공통 불가 | 가능 | 가능 | 보호자 이탈 |
| 아이콘 규칙 | 일부 위반 | 대체로 양호 | 대체로 양호 | 보호자 우선 정리 |

## 4. 통일 원칙

세 앱 홈은 완전히 같아질 필요 없다. 역할이 다르기 때문이다.

그러나 다음은 같아야 한다.

### 4.1 같은 위치의 같은 의미

| 슬롯 | 보호자 | 요양보호사 | 의료진 |
|---|---|---|---|
| Header | 로고, 알림, 프로필 | 로고, 알림, 마이 | 로고, 알림, 마이 |
| Context Strip | 오늘 날짜/대상자 상태 | 근무 시간/담당 수 | 근무/환자 수/라운드 |
| Priority Card | 오늘 안심 상태 | 지금 할 일 | 즉시 확인 환자 |
| Primary Action | 리포트 보기 또는 AI에게 묻기 | 지금 기록 시작 | 지금 확인 또는 회진 시작 |
| AI Summary | 일일 리포트 요약 | AI 인수인계 | AI 판단 요약 |
| Secondary List | 다음 일정/최근 변화 | 담당자 상태 | 다음 3가지/주의 환자 |
| Bottom Action | AI FAB | SOS | SOS |

### 4.2 공통 홈 골격

모든 모바일 홈은 아래 순서를 기본으로 한다.

```text
1. Header
2. Context Strip
3. Priority Card
4. Primary Action
5. AI Summary
6. Secondary List
7. Bottom Bar
```

역할별로 일부 슬롯은 합칠 수 있다.

예:

- 요양보호사: Priority Card 안에 Primary Action 포함
- 의료진: Priority Alert 안에 `지금 확인` 버튼 포함
- 보호자: Priority Card 안에 오늘 안심 상태, AI Summary는 그 아래 일일 리포트 카드

### 4.3 공통 치수

권장 공통 mobile home 토큰:

```css
--home-max-width: 430px;
--home-page-x: 20px;       /* 현재 16/22/24로 갈림. 20 또는 token 하나로 통일 */
--home-header-hit: 48px;
--home-bottom-height: 64px;
--home-bottom-gap: 10px;
--home-bottom-inset-x: 16px;
--home-bottom-inset-bottom: 12px;
--home-card-radius: 20px;
--home-card-padding: 18px;
--home-section-gap: 24px;
```

단, 실제 구현은 `tokens.css` 또는 `system/app.css`에 넣는 것이 좋다. 각 화면 내부 `:root`에 흩뿌리지 말 것.

## 5. 앱별 개선 지시

### 5.1 보호자앱 홈 개선 지시

대상:

```text
v11_보호자앱/g-guardian-live.html
```

P0 개선:

1. `<html>`을 아래처럼 바꾼다.

```html
<html lang="ko" data-role="guardian" data-platform="mobile">
```

2. head import를 디자인 시스템 기준으로 맞춘다.

```html
<link rel="stylesheet" href="../07_디자인/tokens/tokens.css">
<script src="../07_디자인/_app-theme.js"></script>
<link rel="stylesheet" href="../07_디자인/system/app.css">
<link rel="stylesheet" href="../07_디자인/system/components.css">
```

3. 로컬 `:root`의 색 토큰을 제거하거나 semantic token alias로 바꾼다.

금지:

```css
--blue:#2C7AFC;
--green:#34D399;
--t1:#111827;
```

권장:

```css
--accent: var(--color-accent);
--accent-soft: var(--color-accent-soft);
--t1: var(--color-text-primary);
--t2: var(--color-text-secondary);
--t3: var(--color-text-tertiary);
```

4. 홈 첫 화면에서 긴 인트로를 기본 노출하지 않는다.

선택지:

- 최초 진입 1회만 localStorage로 표시
- 온보딩 또는 스플래시 페이지로 분리
- 홈에서는 `body.ready` 상태로 바로 진입

5. AI 오브를 홈 전체 배경 주인공에서 `AI Summary` 또는 `AI FAB` 보조 장식으로 낮춘다.

권장:

- 오브는 `AI Summary` 카드 안에서만 작게 사용
- 또는 하단 AI FAB hover/active 장식으로 사용
- 홈 배경은 `--color-bg-role-gradient`와 카드 스택 중심으로 회귀

6. 리포트 시트를 홈 본문으로 쓰지 말고 카드로 바꾼다.

현재:

```text
큰 report-sheet가 화면 절반을 덮음
```

권장:

```text
Priority Card: 오늘 안심 상태
AI Summary Card: 일일 리포트 한 문장 + 사진 thumbnail
Secondary Grid: 투약/맥박/식사/수면
```

7. primary action을 하나로 정한다.

권장:

- 첫 카드 하단: `리포트 보기`
- 보조: `AI에게 물어보기`
- 하단 우측: AI FAB 유지

금지:

- `AI 채팅하기`, `일일 리포트 보기`, AI FAB, 입력창이 모두 같은 priority로 떠 있는 구조

8. 하단 바 규격을 전문직 앱과 맞춘다.

권장:

```css
bottom: calc(env(safe-area-inset-bottom, 0px) + 12px);
width: calc(100% - 32px);
max-width: 398px;
height: 64px;
```

9. 헤더 버튼을 48px로 맞춘다.

현재:

```css
.nav-btn { width:36px; height:36px; }
```

근거: `g-guardian-live.html:188-191`

권장:

```css
.nav-btn { width:48px; height:48px; }
```

10. 아이콘 규칙 정리.

교체 필요:

- `fluent:emoji-24-filled` 사용 금지
- `tabler:pill-filled` 사용 금지

권장:

- 기분: `fluent:person-heart-24-filled`, `fluent:heart-24-filled`, 또는 `fluent:accessibility-24-filled`
- 투약: `fluent:pill-24-filled`

### 5.2 요양보호사앱 홈 개선 지시

대상:

```text
v11_요양보호사앱/c01-today.html
v11_요양보호사앱/caregiver.css
```

P0 개선:

1. `c01-today.html` 내부의 header/tabbar/SOS/sheet/toast 스타일을 `caregiver.css` 또는 공용 home CSS로 이동한다.

현재 `caregiver.css`가 공통화를 선언하지만 실제 화면 내부에 중복 정의가 많다.

근거:

- `caregiver.css:10-15`
- `c01-today.html:73-101`
- `c01-today.html:426-520`

2. `--page-pad:16px`를 공통 home token으로 바꾼다.

현재:

```css
--page-pad: 16px;
```

근거: `c01-today.html:53`

의료진:

```css
--pad: 22px;
```

근거: `_shared.css:31`

권장:

- 세 앱 공통 `--home-page-x`를 사용한다.
- 390px 모바일 기준 20px 권장.

3. 홈 순서를 공통 골격에 맞춘다.

현재:

```text
근무 스트립 → 관찰 카드 → 지금 할 일 hero → AI 인수인계 → 담당 목록
```

권장:

```text
Header
Context Strip: 오전 근무 · 완료/남은/담당
Priority Card: 박영자 어르신 · 혈압 측정
Primary Action: 지금 기록 시작
AI Summary: AI 인수인계
Secondary List: 담당 4명 상태
Observation Card: 이정숙 미열 관찰
```

예외:

- 관찰 카드가 긴급/위험이면 Priority Card로 승격 가능.
- 단 그 경우 hero CTA도 관찰 카드 안에 포함해야 한다.

4. 관찰 카드의 시각 언어를 `card-alert--warning` 계열로 맞춘다.

현재:

```css
.obs-card { background:#fff; border-radius:14px; ... }
.obs-vitals { background: rgba(245, 158, 11, .05); }
```

근거: `c01-today.html:254-342`

권장:

- 카드 전체는 `card-alert--warning` 또는 `home-alert-card`
- 내부 vitals는 별도 pale block
- 좌측 컬러 라인 패턴은 쓰지 않는다.

5. 히어로 CTA는 유지한다.

현재 `지금 기록 시작`은 좋다.

근거: `c01-today.html:174-188`

유지하되 버튼 스타일은 공용 `.btn .btn--primary .btn--full` 구조로 이동한다.

6. 하단 탭바/SOS는 의료진과 완전히 동일한 공용 클래스로 묶는다.

현재 요양보호사와 의료진의 구조는 거의 같은데 별도 구현이다.

권장 공용:

```html
<div class="home-bottom">
  <nav class="home-tabbar">...</nav>
  <a class="home-fab home-fab--sos">...</a>
</div>
```

### 5.3 의료진앱 홈 개선 지시

대상:

```text
v15_의료진앱/d01-home.html
v15_의료진앱/_shared.css
```

P0 개선:

1. 공용 system CSS를 import한다.

현재:

```html
<link rel="stylesheet" href="../07_디자인/tokens/tokens.css">
<script src="../07_디자인/_app-theme.js"></script>
<link rel="stylesheet" href="./_shared.css">
```

근거: `d01-home.html:10-13`

권장:

```html
<link rel="stylesheet" href="../07_디자인/tokens/tokens.css">
<script src="../07_디자인/_app-theme.js"></script>
<link rel="stylesheet" href="../07_디자인/system/app.css">
<link rel="stylesheet" href="../07_디자인/system/components.css">
<link rel="stylesheet" href="./_shared.css">
```

2. `_shared.css`의 `--pad`, `--tab-h`, `--tab-bot`을 공통 home token으로 대체한다.

현재:

```css
--tab-h: 64px;
--tab-bot: 14px;
--pad: 22px;
```

근거: `_shared.css:26-31`

권장:

```css
--home-page-x: var(--space-6); /* 20px */
--home-bottom-height: 64px;
--home-bottom-bottom: 12px;
```

3. 위험 alert 카드에 명시 action을 추가한다.

현재 alert:

```html
<a class="alert" href="d02-round.html?focus=10">
  ...
  <div class="alert-main">최명자 어르신<br>혈압 180/110</div>
</a>
```

근거: `d01-home.html:304-317`

권장:

```html
<div class="home-priority__actions">
  <span class="btn btn--primary btn--full">지금 확인</span>
</div>
```

또는 실제 버튼:

```html
<button class="btn btn--primary btn--full">지금 확인</button>
```

단, 카드 전체가 링크이면 nested button은 피하고 카드 하단 CTA-looking span을 둔다.

4. `다음 3가지`의 세 번째 카드가 하단 바와 겹치지 않게 조정한다.

현재 측정:

```text
third next-card: y=745, h=99
tabbar: y=746, h=64
```

권장:

- 첫 viewport에서는 `다음 2가지`만 보이게 하거나
- 위험 alert 높이를 줄이고 CTA를 명확히 하거나
- 하단 padding/section gap을 조정한다.

5. 의료진과 요양보호사 하단 바를 공통 컴포넌트로 합친다.

현재 의료진:

```css
.tab-wrap
.tabbar
.sos
```

근거: `d01-home.html:229-260`

현재 요양보호사:

```css
.bottom-bar
.tabbar
.sos
```

근거: `c01-today.html:426-464`

권장:

- 클래스명 통일
- 값 통일
- 전문직 앱은 우측 `home-fab--sos`

## 6. 공통 컴포넌트/패턴 제안

새 공통 CSS를 하나 만들거나 기존 `system/components.css`에 추가한다.

권장 파일:

```text
07_디자인/system/home.css
```

또는 기존 파일에 섹션 추가:

```text
07_디자인/system/components.css
```

권장 클래스:

```css
.home-shell
.home-bg
.home-header
.home-header__logo
.home-header__actions
.home-icon-button
.home-context
.home-priority
.home-priority--safe
.home-priority--task
.home-priority--alert
.home-primary-action
.home-ai-summary
.home-section
.home-list-card
.home-bottom
.home-tabbar
.home-tab
.home-fab
.home-fab--ai
.home-fab--sos
```

핵심은 “디자인이 예쁘게 비슷함”이 아니라, 세 앱이 같은 구조를 공유하게 만드는 것이다.

## 7. 적용 우선순위

### P0. 제품군 통일성 즉시 개선

1. 보호자 홈을 `tokens.css`와 `_app-theme.js`에 연결한다.
2. 보호자 홈에 `data-role="guardian" data-platform="mobile"`을 추가한다.
3. 세 홈의 하단 바 위치/높이/inset/blur/shadow를 통일한다.
4. 세 홈의 헤더 버튼을 48px hit area로 통일한다.
5. 세 홈의 primary action 위치를 Priority Card 하단으로 통일한다.
6. 의료진 alert 카드에 명시 action을 추가한다.
7. 보호자 홈의 긴 인트로를 최초 1회 또는 별도 온보딩으로 분리한다.

### P1. 디자인 시스템 편입

1. 의료진앱에 `system/app.css`, `system/components.css`를 붙인다.
2. `v15_의료진앱/_shared.css`와 `v11_요양보호사앱/caregiver.css`의 공통값을 `system/home.css`로 승격한다.
3. 요양보호사 홈 내부 중복 CSS를 줄인다.
4. 보호자 홈 로컬 tokens를 semantic tokens로 교체한다.
5. 공통 home 슬롯 구조를 문서화한다.

### P2. 정리

1. `fluent:*` 외 iconify 제거.
2. inline SVG 직접 삽입 제거, 브랜드 심볼은 asset `<img>` 사용.
3. hard-coded hex/rgba를 semantic token으로 전환.
4. 보호자 홈의 AI 오브를 카드 내부 보조 장식으로 축소.
5. 세 홈의 section label, card radius, shadow, typography scale을 맞춘다.

## 8. 완료 기준

수정 완료 후 아래 기준을 만족해야 한다.

### 8.1 구조 기준

- 세 홈 모두 `<html data-role="..." data-platform="mobile">`를 가진다.
- 세 홈 모두 `tokens.css`와 `_app-theme.js`를 import한다.
- 세 홈 모두 같은 home header/bottom bar 규격을 사용한다.
- 세 홈 모두 첫 화면에서 다음 요소 순서를 따른다:

```text
Header → Context → Priority → Primary Action → AI Summary/Secondary
```

### 8.2 시각 기준

- 헤더 우측 버튼 크기는 모두 48px.
- 하단 바 높이는 모두 64px.
- 하단 바 bottom inset은 모두 12px 또는 같은 token.
- 카드 기본 radius는 18-20px 범위로 통일.
- primary action은 첫 priority card 안 또는 바로 아래에 있다.
- 보호자만 “전혀 다른 인터랙션 앱”처럼 보이지 않아야 한다.

### 8.3 기능 기준

- 보호자 홈도 다크 모드 저장값을 반영한다.
- 전문직 앱의 우측 FAB은 SOS, 보호자앱의 우측 FAB은 AI로 유지한다.
- 의료진 홈 alert를 탭하면 명확히 “지금 확인” 행동으로 읽힌다.
- 요양보호사 홈의 `지금 기록 시작`은 유지된다.

### 8.4 규칙 기준

- UI 내 이모지 사용 금지.
- `fluent:*` 외 iconify 혼용 제거.
- 불필요한 inline SVG 제거.
- 새로 추가하는 색상은 semantic token 사용.
- 화면 내부 CSS는 화면 고유 레이아웃만 남기고 공통 UI는 system CSS로 이동.

## 9. 클로드에게 복붙할 프롬프트

아래 프롬프트를 그대로 복붙하면 된다.

```text
하루안부 repo에서 다음 문서를 먼저 읽고 그대로 작업해줘.

읽을 문서:
07_디자인/CODEX_HOME_UNIFICATION_AUDIT_20260511.md

목표:
보호자앱 홈(v11_보호자앱/g-guardian-live.html), 요양보호사앱 홈(v11_요양보호사앱/c01-today.html), 의료진앱 홈(v15_의료진앱/d01-home.html)이 같은 하루안부 제품군처럼 보이도록 홈 화면 구조와 디자인 시스템 적용을 통일해줘.

핵심 문제:
1. 보호자앱 홈이 data-role/data-platform/tokens.css/_app-theme.js 없이 디자인 시스템 밖에 있음.
2. 세 홈의 Header, Context, Priority Card, Primary Action, AI Summary, Bottom Bar 위치와 규격이 다름.
3. 보호자앱은 AI 오브/인트로/리포트 시트가 너무 강해서 다른 앱과 완전히 다른 경험처럼 보임.
4. 요양보호사와 의료진은 서로 비슷하지만 padding, header, bottom bar, card 문법이 다름.
5. 의료진앱 alert에는 명시적인 primary action이 약함.

반드시 지켜야 할 것:
- AGENTS.md 규칙 준수: UI/문서에서 이모지 금지.
- 아이콘은 iconify-icon의 fluent:* 계열로 통일. tabler/ph/emoji 계열 제거.
- 브랜드 심볼은 inline SVG 직접 삽입보다 07_디자인/logo/brand-system/01_심볼단독.svg asset 사용.
- 색/간격/라운드/그림자는 가능한 tokens.css semantic token 사용.
- 기존 사용자 변경을 되돌리지 말고, 필요한 범위만 수정.
- 보호자/요양보호사/의료진 역할 차이는 유지하되, 같은 위치에 같은 의미의 요소가 오게 해줘.

우선순위:
P0:
1. g-guardian-live.html에 data-role="guardian" data-platform="mobile" 추가.
2. g-guardian-live.html에 tokens.css, _app-theme.js, system/app.css, system/components.css 연결.
3. 보호자 홈의 로컬 --blue/--green/--t1 등은 semantic token alias로 정리.
4. 세 홈의 헤더 규격을 통일: 좌측 로고, 우측 알림/프로필, 48px hit area.
5. 세 홈의 하단 바 규격 통일: 높이 64px, 좌우 inset 동일, bottom inset 동일, blur/shadow 동일.
6. 세 홈의 홈 골격을 Header → Context Strip → Priority Card → Primary Action → AI Summary/Secondary List → Bottom Bar 순서로 맞춤.
7. 보호자 홈의 긴 인트로는 최초 1회 또는 별도 온보딩으로 분리하거나 기본 홈에서는 바로 본문이 보이게 조정.
8. 의료진 홈의 위험 alert 카드에 “지금 확인” 또는 “회진 시작” action을 명확히 추가.
9. 요양보호사 홈의 “지금 기록 시작” CTA는 유지하되 공통 버튼 문법으로 맞춤.

P1:
1. 의료진앱에도 system/app.css, system/components.css를 연결.
2. v15_의료진앱/_shared.css와 v11_요양보호사앱/caregiver.css의 중복 bottom bar/header 값을 공통화.
3. 가능하면 07_디자인/system/home.css를 만들거나 system/components.css에 home 공통 클래스를 추가.
4. 요양보호사 홈 내부에 중복된 header/tabbar/SOS/sheet/toast CSS를 줄이고 공통 CSS로 옮김.

완료 기준:
- 세 홈을 390x844 viewport로 열었을 때 같은 제품군이라는 느낌이 나야 함.
- 보호자앱도 다크 모드 공통 설정을 반영해야 함.
- 하단 바와 헤더 위치가 세 앱에서 같은 규칙으로 보일 것.
- primary action 위치가 세 앱에서 같은 규칙으로 보일 것.
- rg로 tabler:, ph:, emoji 아이콘 사용이 홈 화면에서 없어야 함.
- rg로 g-guardian-live.html 내 불필요한 hard-coded --blue/--green/--t1 중심 구조가 제거되거나 semantic token alias로 바뀌어야 함.

수정 후 확인:
1. open "v11_보호자앱/g-guardian-live.html"
2. open "v11_요양보호사앱/c01-today.html"
3. open "v15_의료진앱/d01-home.html"
4. 세 화면의 스크린샷을 비교해서 header/context/priority/action/bottom bar가 같은 위치 규칙을 따르는지 확인.
5. 변경 내용과 남은 리스크를 요약해줘.
```

## 10. 클로드 작업 시 주의사항

클로드가 바로 전체 리디자인을 크게 벌리면 위험하다. 다음 순서로 나눠서 작업하는 것이 좋다.

1. 보호자 홈을 디자인 시스템에 연결한다.
2. 세 홈의 header와 bottom bar만 먼저 맞춘다.
3. 세 홈의 priority/action 위치를 맞춘다.
4. 보호자 홈의 AI 오브/리포트 시트를 공통 홈 골격에 맞게 낮춘다.
5. 마지막에 색/아이콘/토큰 정리를 한다.

한 번에 모든 카드 내부 콘텐츠를 갈아엎지 말고, 먼저 “같은 제품군으로 보이는 뼈대”부터 맞춰야 한다.

