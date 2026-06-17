# 하루안부 디자인 시스템 v3.2 검증 기록

검증일: 2026-05-11  
검증자: Codex  
검증 대상: 디자인 시스템 프리뷰, AI/차트/패턴 데모, 실제 앱 시안, 앱 공통 다크 모드 전파

## 1. 검증 요약

이번 수정은 범위가 크다. `07_디자인`의 프리뷰와 문서, `tokens.css`, 실제 앱 시안 다수가 변경되었고, 새 공통 스크립트 `07_디자인/_app-theme.js`와 `07_디자인/_preview-controls.js`가 추가되었다.

핵심 결론:

| 항목 | 결과 | 메모 |
|---|---:|---|
| 디자인 시스템 메인 프리뷰 로드 | 통과 | `preview.html` 정상 로드 |
| 프리뷰 페이지 우상단 다크 토글 | 통과 | 프리뷰 4종 모두 `data-theme="dark"` 전환 확인 |
| AI 컴포넌트 라이브 데모 | 통과 | `preview-components.html`에 AI 컴포넌트 섹션 존재 |
| 차트/매직넘버/일러스트/동사 매트릭스 | 통과 | `preview-foundations.html`에 섹션 존재 |
| AI 패턴 5종/알림 4채널 매트릭스 | 통과 | `preview-patterns.html`에 섹션 존재 |
| 실제 앱 시안 로드 | 통과 | 새 시안 3종 로드 확인 |
| 설정에서 다크 선택 후 새 진입 반영 | 통과 | `localStorage` 기반으로 새로고침/새 진입 시 반영 |
| 설정에서 다크 선택 후 이미 열린 모든 앱 동시 반영 | 실패 | 다른 탭이 `storage` 이벤트를 듣지 않음 |
| 프로젝트 규칙: 이모지 금지 | 대체로 통과 | 이모지 범위 문자는 없음. 단 `★` 장식 문자 다수 존재 |
| 프로젝트 규칙: 아이콘 통일 | 일부 실패 | `g07-settings.html`에 inline SVG 잔존 |
| `open file://` 방식 콘솔 에러 | 일부 실패 | manifest 로드가 CORS로 차단됨 |

전체적으로 보면 “v3.2 프리뷰/시안은 존재하고 대부분 동작한다”는 점은 긍정적이다. 다만 사용자가 언급한 “보호자앱 설정에서 다크 토글하면 모든 앱이 동시에 다크”는 현재 구현만으로는 정확히 성립하지 않는다. 지금 상태는 “설정값 저장 후 새로고침/새 진입 시 다크 적용”이다.

## 2. 변경 파일 현황

검증 시점 `git status --short` 기준으로 디자인 시스템과 앱 시안에 대량 변경이 있었다.

주요 수정 파일:

- `07_디자인/01_FOUNDATIONS.md`
- `07_디자인/02_COMPONENTS.md`
- `07_디자인/03_PATTERNS.md`
- `07_디자인/README.md`
- `07_디자인/_preview-shared.css`
- `07_디자인/preview.html`
- `07_디자인/preview-components.html`
- `07_디자인/preview-foundations.html`
- `07_디자인/preview-patterns.html`
- `07_디자인/preview-roles.html`
- `07_디자인/tokens/tokens.css`
- `v11_보호자앱/g07-settings.html`
- `v11_보호자앱/g03-sotong.html`
- `v11_보호자앱/g02-ai-guide.html`
- `v11_보호자앱/g02-ai-report.html`
- `v11_보호자앱/g05-records.html`
- `v11_보호자앱/g06-alert.html`
- `v11_보호자앱/g08-billing.html`
- `v11_보호자앱/g09-prescription.html`
- `v11_보호자앱/g10-timeline.html`
- `v11_요양보호사앱/c01-today.html`
- `v11_요양보호사앱/c02-checklist.html`
- `v11_요양보호사앱/c03-sotong.html`
- `v11_요양보호사앱/c04-mypage.html`
- `v11_요양보호사앱/c04-schedule.html`
- `v12_환자앱/index.html`
- `v12_환자앱/p01-today.html`
- `v12_환자앱/p02-med-alert.html`
- `v12_환자앱/p03-call.html`
- `v12_환자앱/p05-voice.html`
- `v12_환자앱/p06-photo.html`
- `v12_환자앱/p07-message.html`
- `v12_환자앱/p08-help.html`
- `v12_환자앱/p09-sos.html`
- `v12_환자앱/p10-med-done.html`
- `v13_온보딩/ob01-welcome.html`
- `v15_의료진앱/d01-home.html`
- `v15_의료진앱/d02-round.html`
- `v15_의료진앱/d03-inbox.html`
- `v15_의료진앱/d04-handover.html`
- `v15_의료진앱/d05-mypage.html`

새로 추가된 파일:

- `07_디자인/_app-theme.js`
- `07_디자인/_preview-controls.js`
- `v10_의료진웹/m02-patient-side-panel.html`
- `v11_보호자앱/g03-chat-ai-v32.html`
- `v12_환자앱/p11-settings.html`

## 3. 요청 파일별 확인 결과

### 3.1 디자인 시스템 메인

대상:

```bash
open "/Users/yechanshon/Desktop/Haru Anbu/07_디자인/preview.html"
```

결과: 통과

확인 내용:

- 페이지 타이틀: `하루안부 디자인 시스템 v3.2`
- 우상단 다크 토글 존재: 있음
- 다크 토글 클릭 시:
  - `<html data-theme="dark">` 적용
  - `--color-bg-canvas` 값이 `#F0F4F8`에서 `#0F1115`로 변경
- 메인 페이지에 다음 텍스트/콘텐츠 신호 존재:
  - AI 패턴 관련 내용
  - 알림 매트릭스 관련 내용
  - 차트 관련 내용
  - 동사 매트릭스 관련 내용
  - 매직넘버 관련 내용
  - 일러스트 관련 내용
  - AI 컴포넌트 관련 내용

판단:

메인 프리뷰는 v3.2 변경점을 소개하는 허브로 정상 동작한다.

### 3.2 AI 컴포넌트 라이브 데모

대상:

```bash
open "/Users/yechanshon/Desktop/Haru Anbu/07_디자인/preview-components.html"
```

결과: 통과

확인 내용:

- 페이지 타이틀: `Components · 하루안부 디자인 시스템 v3.2`
- 우상단 다크 토글 존재: 있음
- 다크 토글 클릭 시 `data-theme="dark"` 적용
- AI 컴포넌트 관련 텍스트 신호 존재
- `H1`, AI 입력/응답 계열 섹션 존재

판단:

AI 컴포넌트 라이브 데모는 페이지에 반영되어 있다.

### 3.3 차트 + 매직넘버 + 일러스트 + 동사 매트릭스

대상:

```bash
open "/Users/yechanshon/Desktop/Haru Anbu/07_디자인/preview-foundations.html"
```

결과: 통과

확인 내용:

- 페이지 타이틀: `Foundations · 하루안부 디자인 시스템 v3.2`
- 우상단 다크 토글 존재: 있음
- 다크 토글 클릭 시 `data-theme="dark"` 적용
- 다음 텍스트 신호 존재:
  - `차트`
  - `Okabe`
  - `매직넘버`
  - `일러스트`
  - `동사`
  - `닫기`

판단:

요청한 foundations 확장 항목은 페이지에 반영되어 있다.

주의점:

해당 페이지에는 `★` 장식 문자가 여러 군데 있다. 프로젝트의 “이모지 절대 금지”가 유니코드 장식 기호까지 엄격히 포함하는 운영 규칙이라면 일반 텍스트나 `badge` 컴포넌트로 바꾸는 것이 좋다.

확인된 예:

- `콤비 — 가로 (★ 기본)`
- `★ 500 · accent`
- `--space-5 (16px) ★ page-margin (mobile)`
- `★ 하루안부 심볼`

### 3.4 AI 패턴 5종 + 알림 4채널 매트릭스

대상:

```bash
open "/Users/yechanshon/Desktop/Haru Anbu/07_디자인/preview-patterns.html"
```

결과: 통과

확인 내용:

- 페이지 타이틀: `Patterns · 하루안부 디자인 시스템 v3.2`
- 우상단 다크 토글 존재: 있음
- 다크 토글 클릭 시 `data-theme="dark"` 적용
- 다음 텍스트 신호 존재:
  - `AI 패턴 5종`
  - `P3A`
  - `알림 4채널`
  - `4채널`

판단:

AI 패턴 5종과 알림 채널 매트릭스는 화면에 반영되어 있다.

### 3.5 보호자앱 AI 시안

대상:

```bash
open "/Users/yechanshon/Desktop/Haru Anbu/v11_보호자앱/g03-chat-ai-v32.html"
```

결과: 통과

확인 내용:

- 파일 존재 확인
- 페이지 타이틀: `하루안부 — AI 어시스턴트 (v3.2)`
- `<html data-role="guardian" data-platform="mobile">` 적용
- `tokens.css` import 확인
- `_app-theme.js` import 확인
- `window.HaruTheme` 존재 확인
- `haru-app-theme=dark`가 저장된 상태에서 새로 진입하면 다크 토큰 적용 확인

주의점:

해당 페이지는 공통 `system/app.css`, `system/components.css`를 import하지 않고 `tokens.css`와 페이지 자체 CSS 중심으로 동작한다. 디자인 시스템의 공용 컴포넌트 사용률을 높이려면 후속 정리가 필요하다.

### 3.6 의료진웹 Side Panel 시안

대상:

```bash
open "/Users/yechanshon/Desktop/Haru Anbu/v10_의료진웹/m02-patient-side-panel.html"
```

결과: 통과

확인 내용:

- 파일 존재 확인
- 페이지 타이틀: `하루안부 — 환자 상세 + Side Panel (v3.2 데모)`
- `<html data-role="medical" data-platform="web">` 적용
- `tokens.css` import 확인
- `_app-theme.js` import 확인
- `window.HaruTheme` 존재 확인
- 상단 다크 토글 버튼 `#topbar-theme` 존재

주의점:

해당 페이지도 공통 `system/app.css`, `system/components.css`를 import하지 않고 있다. 의료진웹은 정보 밀도와 hover/focus 상태가 중요하므로 공용 컴포넌트 레이어로 흡수하는 것이 좋다.

### 3.7 환자앱 설정 시안

대상:

```bash
open "/Users/yechanshon/Desktop/Haru Anbu/v12_환자앱/p11-settings.html"
```

결과: 통과

확인 내용:

- 파일 존재 확인
- 페이지 타이틀: `하루안부 · 내 화면 설정`
- `<html data-role="patient" data-platform="mobile">` 적용
- `tokens.css` import 확인
- `_app-theme.js` import 확인
- `patient.css` import 확인
- `window.HaruTheme` 존재 확인
- 다크 모드, 기기 설정 따라가기, 글자 크게, 진하게 보기 토글 UI 존재

주의점:

환자앱 설정은 환자용 큰 터치 타겟을 잘 의식하고 있다. 다만 이 페이지 또한 이미 열린 다른 앱 탭으로 테마 변경을 동시 전파하지는 못한다.

### 3.8 보호자앱 설정

대상:

```bash
open "/Users/yechanshon/Desktop/Haru Anbu/v11_보호자앱/g07-settings.html"
```

결과: 일부 실패

통과한 부분:

- 파일 존재 확인
- 페이지 타이틀: `하루안부 — 알림 설정`
- `<html data-role="guardian" data-platform="mobile">` 적용
- `tokens.css` import 확인
- `_app-theme.js` import 확인
- `system/app.css`, `system/components.css` import 확인
- 다크 모드, 시스템 따라가기, 글자 크게, 고대비 모드 토글 존재
- 다크 토글 클릭 시 현재 페이지는 즉시 다크 모드로 변경됨
- `localStorage.haru-app-theme = "dark"` 저장 확인

실패한 부분:

- 이미 열려 있던 다른 앱 탭은 즉시 다크 모드로 바뀌지 않음
- 다른 탭의 `localStorage` 값은 `dark`로 바뀌지만, `<html data-theme="dark">`가 적용되지 않음
- 따라서 실제 동작은 “모든 앱 동시 다크”가 아니라 “다음 로드부터 다크”임

## 4. 다크 모드 전파 상세 분석

### 4.1 현재 구조

공통 스크립트:

```text
07_디자인/_app-theme.js
```

핵심 저장 키:

```text
haru-app-theme       = dark | light | system
haru-app-text-size   = large
haru-app-contrast    = high
```

초기 로드 시 동작:

1. `localStorage.getItem('haru-app-theme')`를 읽음
2. 값이 `dark` 또는 `light`면 `<html data-theme="...">`를 설정
3. 값이 `system` 또는 null이면 `data-theme`를 제거하고 CSS의 `prefers-color-scheme`에 맡김

현재 탭에서 `setTheme()` 호출 시 동작:

1. 현재 탭의 `<html>`에 `data-theme` 설정 또는 제거
2. `localStorage`에 저장
3. 현재 탭에만 `haru:theme-change` 커스텀 이벤트 dispatch

### 4.2 실제 테스트 결과

테스트 절차:

1. `g07-settings.html` 열기
2. `localStorage.clear()`
3. 설정 페이지 새로고침
4. 같은 브라우저 컨텍스트에서 다음 탭 열기:
   - `g03-chat-ai-v32.html`
   - `m02-patient-side-panel.html`
   - `p11-settings.html`
5. 보호자 설정 페이지에서 `#toggle-dark` 클릭
6. 각 탭의 `data-theme`, `--color-bg-canvas`, `localStorage.haru-app-theme` 확인

클릭 전:

| 탭 | `data-theme` | `--color-bg-canvas` | `window.HaruTheme` |
|---|---|---|---|
| 보호자 설정 | null | `#F0F4F8` | true |
| AI 어시스턴트 | null | `#F0F4F8` | true |
| 의료진 Side Panel | null | `#F0F4F8` | true |
| 환자 설정 | null | `#F0F4F8` | true |

클릭 후:

| 탭 | `data-theme` | `--color-bg-canvas` | `localStorage.haru-app-theme` |
|---|---|---|---|
| 보호자 설정 | `dark` | `#0F1115` | `dark` |
| AI 어시스턴트 | null | `#F0F4F8` | `dark` |
| 의료진 Side Panel | null | `#F0F4F8` | `dark` |
| 환자 설정 | null | `#F0F4F8` | `dark` |

해석:

- `localStorage`는 같은 origin 안에서 공유되고 있다.
- 하지만 이미 로드된 다른 탭은 `localStorage` 변경을 감지해 DOM 속성을 갱신하지 않는다.
- `_app-theme.js`에 `storage` 이벤트 리스너가 없기 때문이다.

### 4.3 필요한 수정

`07_디자인/_app-theme.js`에 다음 기능이 필요하다.

1. 저장값을 DOM에 반영하는 공용 함수 분리
2. `window.addEventListener('storage', ...)` 추가
3. `haru-app-theme`, `haru-app-text-size`, `haru-app-contrast` 변경 시 현재 탭의 `<html>` 속성 즉시 갱신
4. 현재 탭 안의 설정 UI도 바뀐 값을 sync할 수 있도록 커스텀 이벤트 발행

권장 구조:

```js
function applyStoredTheme() {
  const theme = localStorage.getItem('haru-app-theme');
  if (theme === 'dark' || theme === 'light') {
    root.setAttribute('data-theme', theme);
  } else {
    root.removeAttribute('data-theme');
  }

  const textSize = localStorage.getItem('haru-app-text-size');
  root.toggleAttribute('data-a11y-text', textSize === 'large');
  if (textSize === 'large') root.setAttribute('data-a11y-text', 'large');

  const contrast = localStorage.getItem('haru-app-contrast');
  root.toggleAttribute('data-a11y-contrast', contrast === 'high');
  if (contrast === 'high') root.setAttribute('data-a11y-contrast', 'high');
}

window.addEventListener('storage', (event) => {
  if (![
    'haru-app-theme',
    'haru-app-text-size',
    'haru-app-contrast'
  ].includes(event.key)) return;

  applyStoredTheme();
  window.dispatchEvent(new CustomEvent('haru:theme-sync', {
    detail: {
      theme: localStorage.getItem('haru-app-theme') || 'system',
      textSize: localStorage.getItem('haru-app-text-size') || 'normal',
      contrast: localStorage.getItem('haru-app-contrast') || 'normal',
      source: 'storage'
    }
  }));
});
```

단, 위 코드는 방향 예시다. 실제 반영 시에는 현재 `_app-theme.js`의 API와 중복 없이 정리하는 것이 좋다.

## 5. 프리뷰 다크 토글과 앱 다크 토글의 차이

현재 프리뷰와 실제 앱은 서로 다른 저장 키를 쓴다.

프리뷰:

```text
haru-preview-theme
haru-preview-role
```

실제 앱:

```text
haru-app-theme
haru-app-text-size
haru-app-contrast
```

이 구분 자체는 나쁘지 않다. 프리뷰의 역할 선택이나 실험 상태가 실제 앱 설정을 오염시키지 않기 때문이다.

다만 사용자가 “디자인 시스템 메인에서 다크 토글”과 “보호자앱 설정에서 모든 앱 다크”를 같은 기능처럼 기대한다면, 문서에 다음 차이를 명확히 써야 한다.

- 프리뷰 토글: 디자인 시스템 데모용, `haru-preview-theme`
- 앱 설정 토글: 실제 앱 공통 설정용, `haru-app-theme`

## 6. 콘솔 에러

`open ".../g07-settings.html"`처럼 `file://`로 직접 열면 다음 콘솔 에러가 발생한다.

```text
Access to manifest at 'file:///.../manifest.json' from origin 'null' has been blocked by CORS policy
Failed to load resource: net::ERR_FAILED
```

원인:

- `file://` origin에서는 manifest 로드가 브라우저 정책에 의해 제한된다.

영향:

- 화면 자체와 테마 토글 기능에는 직접적인 문제를 만들지 않았다.
- 하지만 사용자가 콘솔을 열면 에러가 보인다.

대응 옵션:

1. 실제 검증은 간단한 로컬 서버로 실행한다.
2. `file://` 프리뷰용 페이지에서는 manifest link를 제거하거나 조건부로 삽입한다.
3. “open file 방식에서는 manifest 에러가 날 수 있음”을 README에 명시한다.

## 7. 프로젝트 규칙 위반 가능성

### 7.1 inline SVG 잔존

프로젝트 AGENTS 규칙:

```text
아이콘이 필요하면 iconify-icon(fluent:* 등)로 통일.
```

확인된 위반:

```text
v11_보호자앱/g07-settings.html:146
```

내용:

- 소통 탭 아이콘이 inline SVG로 남아 있음

확인된 위반:

```text
v11_보호자앱/g07-settings.html:151
```

내용:

- AI FAB 심볼이 inline SVG로 직접 삽입되어 있음

권장 수정:

- 소통 탭: `iconify-icon icon="fluent:chat-24-filled"` 또는 시스템에서 정한 소통 아이콘으로 교체
- AI FAB: inline SVG 대신 브랜드 심볼 파일 사용

예:

```html
<img src="../07_디자인/logo/brand-system/01_심볼단독.svg" alt="">
```

또는 공용 컴포넌트가 이미 있다면 `.fab-ai` 구조를 사용한다.

### 7.2 장식 별표 문자

이모지 범위 문자 검색에서는 일반 이모지는 발견되지 않았다. 다만 `★` 문자가 프리뷰에 다수 존재한다.

확인 예:

```text
07_디자인/preview-components.html
07_디자인/preview-foundations.html
07_디자인/preview-patterns.html
```

해석:

- `★`는 일반적인 이모지는 아니지만 장식 기호다.
- “이모지 절대 금지”를 넓게 해석하면 제거하는 것이 안전하다.

권장 수정:

- `★`를 텍스트로 대체:
  - `기본`
  - `권장`
  - `핵심`
  - `Primary`
- 또는 `badge` 컴포넌트로 표시:

```html
<span class="badge badge--info">기본</span>
```

## 8. 디자인 시스템 관점 평가

### 8.1 좋아진 점

1. 다크 모드가 문서 수준이 아니라 실제 토큰과 데모에 연결되었다.
2. `tokens.css`에 `data-theme="dark"`와 `prefers-color-scheme` 처리가 들어갔다.
3. 프리뷰 4종에 우상단 토글이 일관되게 들어갔다.
4. 실제 앱 시안에도 `_app-theme.js`를 붙여 앱 설정과 토큰을 연결하려고 했다.
5. 보호자/의료진/환자 역할별 `data-role`, `data-platform` 구조가 유지되었다.
6. AI 컴포넌트와 AI 패턴을 별도 카테고리로 승격한 점은 하루안부 제품 성격과 맞다.
7. 차트 팔레트, 매직넘버, 알림 매트릭스, 동사 매트릭스는 현업형 디자인 시스템에 필요한 운영 규칙에 가깝다.

### 8.2 아직 부족한 점

1. 공통 테마 스크립트가 다른 열린 탭에 변경을 즉시 반영하지 못한다.
2. 공용 컴포넌트 CSS 사용률이 파일마다 다르다.
3. 일부 새 시안은 `tokens.css`만 사용하고 `system/app.css`, `system/components.css`는 사용하지 않는다.
4. 일부 UI에 inline SVG가 남아 프로젝트 아이콘 규칙과 충돌한다.
5. 프리뷰용 테마 저장 키와 앱용 테마 저장 키가 분리되어 있어 사용자가 혼동할 수 있다.
6. `file://` 직접 open 방식에서 manifest 콘솔 에러가 발생한다.
7. 토글 UI가 `aria-checked`는 갖고 있지만, 다른 탭에서 설정이 바뀔 때 스위치 UI를 다시 sync하는 이벤트 계약은 없다.

## 9. 우선순위별 개선안

### P0. 앱 다크 모드 동시 전파 수정

대상:

```text
07_디자인/_app-theme.js
```

해야 할 일:

- 저장값 적용 함수를 `applyStoredPreferences()`처럼 분리
- 초기 실행 시 해당 함수 호출
- `setTheme`, `setTextSize`, `setContrast`에서도 같은 함수 사용
- `storage` 이벤트 리스너 추가
- 변경 감지 시 `data-theme`, `data-a11y-text`, `data-a11y-contrast` 즉시 갱신
- `haru:theme-sync` 또는 기존 `haru:theme-change` 이벤트를 다른 탭에서도 발행

완료 기준:

- `g07-settings.html`과 `g03-chat-ai-v32.html`을 동시에 열어 둔다.
- 설정에서 다크 토글 클릭.
- 두 탭 모두 새로고침 없이 `--color-bg-canvas = #0F1115`로 변경된다.

### P0. inline SVG 제거

대상:

```text
v11_보호자앱/g07-settings.html
```

해야 할 일:

- 소통 탭 inline SVG를 `iconify-icon`으로 교체
- AI FAB inline SVG를 브랜드 심볼 이미지 또는 공용 `.fab-ai` 구조로 교체

완료 기준:

```bash
rg -n "<svg" "v11_보호자앱/g07-settings.html"
```

결과가 0건이어야 한다.

### P1. 설정 UI 동기화 이벤트 추가

대상:

```text
v11_보호자앱/g07-settings.html
v12_환자앱/p11-settings.html
v10_의료진웹/m02-patient-side-panel.html
```

해야 할 일:

- `_app-theme.js`가 발행하는 sync 이벤트를 각 설정 UI가 듣도록 구성
- 다른 탭에서 다크/라이트가 변경되면 현재 설정 페이지 스위치 상태도 바뀌게 함

완료 기준:

- 보호자 설정과 환자 설정을 동시에 연다.
- 보호자에서 다크를 켠다.
- 환자 설정 페이지의 다크 토글도 새로고침 없이 켜진 상태로 바뀐다.

### P1. 공용 CSS 사용 원칙 정리

문제:

- 일부 화면은 `tokens.css`만 import
- 일부 화면은 `tokens.css + system/app.css + system/components.css` import

권장 원칙:

새 화면 기본 import:

```html
<link rel="stylesheet" href="../07_디자인/tokens/tokens.css">
<script src="../07_디자인/_app-theme.js"></script>
<link rel="stylesheet" href="../07_디자인/system/app.css">
<link rel="stylesheet" href="../07_디자인/system/components.css">
```

예외:

- 완전 독립형 실험/프리뷰
- 환자앱처럼 기존 `patient.css`와 충돌을 정리하기 전인 과도기 화면

문서 수정 필요:

- `07_디자인/tokens/README.md`의 “모든 화면은 tokens.css 하나만 import” 문구를 현재 구조에 맞게 업데이트
- `07_디자인/README.md`의 사용 시작 예시도 `.btn-primary`가 아니라 실제 CSS 구조인 `.btn .btn--primary`와 맞춰야 함

### P1. `file://` manifest 에러 대응

대상:

```text
v11_보호자앱/g07-settings.html
```

선택지:

1. 로컬 서버로 검증하는 방식을 공식화
2. `file://` 프리뷰용으로 manifest link 제거
3. JS로 `location.protocol !== 'file:'`일 때만 manifest 삽입

권장:

정식 PWA 검증은 서버 기준으로 하고, 단순 `open file` 검증에서는 콘솔 에러가 나지 않게 조건부 삽입을 고려한다.

### P2. 장식 기호 정리

대상:

```text
07_디자인/preview-components.html
07_디자인/preview-foundations.html
07_디자인/preview-patterns.html
```

해야 할 일:

- `★`를 `기본`, `권장`, `핵심` 같은 텍스트 또는 badge 컴포넌트로 교체

완료 기준:

```bash
rg -n "★" "07_디자인"
```

프리뷰 UI 영역에서 불필요한 장식 문자가 없어야 한다.

## 10. 재검증 체크리스트

수정 후 다음 순서로 재검증한다.

1. `preview.html` 열기
2. 우상단 다크 토글 클릭
3. `preview-components.html`, `preview-foundations.html`, `preview-patterns.html` 각각 다크 토글 확인
4. `g07-settings.html`, `g03-chat-ai-v32.html`, `m02-patient-side-panel.html`, `p11-settings.html`을 동시에 열기
5. `g07-settings.html`에서 다크 토글 클릭
6. 다른 앱 탭들이 새로고침 없이 다크로 바뀌는지 확인
7. `p11-settings.html`의 다크 토글 UI 상태도 함께 바뀌는지 확인
8. `g07-settings.html`에서 시스템 따라가기 클릭
9. 명시 `data-theme`가 제거되고 시스템 설정을 따르는지 확인
10. `rg -n "<svg" "v11_보호자앱/g07-settings.html"` 결과 확인
11. `rg -nP "[\\x{1F300}-\\x{1FAFF}\\x{2600}-\\x{27BF}]"`로 장식 문자 확인
12. 브라우저 콘솔 에러 확인

## 11. 최종 판단

이번 수정은 방향이 좋다. 특히 v3.2에서 다크 모드, AI 컴포넌트, 차트 팔레트, 매직넘버, 일러스트, 동사 매트릭스, AI 패턴, 알림 채널 매트릭스를 한 번에 확장한 것은 디자인 시스템을 “문서”에서 “제품 운영 규칙”으로 끌어올리는 작업이다.

하지만 아직 사용자가 말한 핵심 주장인 “보호자앱 설정에서 다크 토글하면 모든 앱이 동시에 다크”는 구현적으로 미완성이다. 현재는 `localStorage` 저장까지만 공유되고, 이미 열린 탭의 DOM에는 즉시 반영되지 않는다.

따라서 다음 작업의 첫 번째 목표는 `_app-theme.js`를 실제 공통 상태 동기화 레이어로 만드는 것이다. 그 다음 `g07-settings.html`의 inline SVG와 `file://` manifest 에러를 정리하면, v3.2는 데모 수준을 넘어 실제 앱 공통 시스템으로 꽤 단단해질 수 있다.
