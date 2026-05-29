# role-component-board 검토 피드백

작성일: 2026-05-23  
검토 대상: `07_디자인/role-component-board.html`, `07_디자인/preview.html`  
목적: 클로드가 만든 모바일 3종 컴포넌트 보드를 하루안부 디자인 시스템의 기준 보드로 채택하기 전, 필요한 수정 사항을 정리한다.

## 1. 전체 판단

`07_디자인/role-component-board.html`은 방향이 좋고, 실제 디자인 기준 보드로 사용할 수 있는 상태다.

확인된 장점:

- 12개 컴포넌트 섹션 구성 확인
- 보호자, 요양보호사, 의료진모바일 3개 role 컬럼 구성 확인
- `tokens.css`의 `data-role` / `data-platform` 구조를 이용해 role별 차이를 비교하는 방식이 적절함
- `preview.html`에 `Board (모바일 3종)` 상단 nav 연결과 카드 그리드 진입점이 추가됨
- 브라우저 렌더링 시 콘솔 오류 없음
- 이모지 사용 없음
- 아이콘은 `iconify-icon` 기반

따라서 보드는 폐기하거나 다시 만들 필요가 없다. 다만 “정답 기준 보드”로 쓰려면 아래 항목을 수정해야 한다.

## 2. 반드시 수정할 항목

### 2.1 SOS danger 설명값 수정

현재 보드에는 SOS danger 값이 `#FF3B30`으로 표시되어 있다.

예상 위치:

- `role-component-board.html`의 SOS 섹션
- `danger · #FF3B30` 텍스트 3곳

문제:

현재 `tokens.css` 기준 danger는 `#E32B25` 계열이다. 예전 iOS red 또는 임시 red인 `#FF3B30`으로 설명되면 보드와 실제 토큰이 어긋난다.

수정 방향:

```text
danger · #FF3B30
```

를 아래처럼 바꾼다.

```text
danger · var(--color-danger)
```

또는 설명값을 꼭 보여주고 싶다면:

```text
danger · var(--color-danger) · #E32B25
```

권장안은 첫 번째다. 이 보드는 색상표가 아니라 컴포넌트 보드이므로, 직접 hex보다 토큰명을 보여주는 편이 좋다.

### 2.2 설명 텍스트 안의 직접 hex 표기 줄이기

보드의 CSS 스타일 블록 안에는 직접 hex가 없지만, 화면에 보이는 설명 텍스트에는 hex가 남아 있다.

예:

```text
accent · #2C7AFC
accent · #22C55E
active · #2C7AFC
active · #22C55E
둘 다 #22C55E primary
```

문제:

디자인 시스템 기준 보드에서 직접 색상값이 계속 보이면, 이후 작업자가 토큰보다 hex를 기준으로 이해할 수 있다.

수정 방향:

아래처럼 토큰명 중심으로 바꾼다.

```text
accent · var(--color-accent)
active · var(--color-accent)
primary · var(--color-accent)
```

필요하다면 보조 설명에만 괄호로 현재 값을 적는다.

```text
accent · var(--color-accent) (guardian blue)
accent · var(--color-accent) (care green)
```

권장:

- 컬럼 헤더의 `col__hex` 클래스명도 가능하면 `col__token`으로 바꾼다.
- 당장 클래스명 변경이 부담되면 텍스트만 먼저 바꿔도 된다.

### 2.3 inline style 3건 제거

현재 탭바 섹션의 `col__body`에 inline style이 3건 있다.

예:

```html
<div class="col__body" style="display: flex; justify-content: center; padding-top: 40px; padding-bottom: 40px;">
```

문제:

보드가 “직접 스타일 금지”의 기준 페이지가 되어야 하는데, 보드 내부에 inline style이 남아 있으면 기준이 약해진다.

수정 방향:

CSS에 전용 클래스를 추가한다.

```css
.col__body--tabbar {
  display: flex;
  justify-content: center;
  padding-top: var(--space-9);
  padding-bottom: var(--space-9);
}
```

그리고 HTML은 아래처럼 바꾼다.

```html
<div class="col__body col__body--tabbar">
```

주의:

- `40px` 직접값 대신 가능하면 `var(--space-9)` 또는 적절한 spacing token을 사용한다.
- 세 role 컬럼 모두 같은 클래스를 사용한다.

## 3. 보고 문구 정정

### 3.1 iconify 개수 표현 정정

클로드 보고에는 `iconify-icon: 133회`라고 되어 있었지만, 실제 `<iconify-icon` 요소 수는 63개다.

이 차이는 `iconify-icon` 문자열 검색 시 CSS 선택자, 닫는 태그, 텍스트 등이 같이 잡혀서 생긴 것으로 보인다.

수정 권장 문구:

```text
iconify-icon 요소: 63개
iconify-icon 문자열 출현: 133회
```

또는 간단히:

```text
모든 아이콘은 iconify-icon 기반으로 구성됨
```

숫자를 꼭 쓸 필요는 없다.

### 3.2 hex 0건 표현 정정

현재 “스타일 블록 안 직접 hex 0건”은 맞다. 하지만 문서 텍스트에는 hex가 남아 있다.

수정 권장 문구:

```text
CSS 스타일 정의 안 직접 hex: 0건
설명 텍스트의 hex 표기는 토큰명 중심으로 정리 예정
```

수정 후에는 아래처럼 말할 수 있다.

```text
스타일 정의와 설명 텍스트 모두 토큰명 중심으로 정리
```

## 4. caregiver와 medical의 시각 차이 결정

보드 footer의 핵심 발견은 타당하다.

현재 요양보호사앱과 의료진모바일은 토큰 레벨에서 거의 동일하다. 12개 섹션 중 다수에서 두 앱의 시각 차이는 색이 아니라 콘텐츠, 문장, 아이콘, 정보 밀도에서만 생긴다.

선택지는 두 가지다.

### A안: 현 상태 유지

요양보호사앱과 의료진모바일을 같은 그린 제품군으로 유지한다.

장점:

- 같은 서비스의 역할별 앱이라는 신호가 강함
- 토큰 구조가 단순함
- 색상 체계가 복잡해지지 않음
- 현재 작업물을 크게 흔들지 않음

단점:

- 한눈에 보면 두 앱이 비슷해 보일 수 있음
- 컴포넌트만 떼어놓으면 역할 차이가 약함

### B안: caregiver에 sub-accent 추가

요양보호사앱에만 살짝 다른 그린, 라임 계열 보조 accent, 또는 surface tint를 추가한다.

장점:

- 요양보호사앱과 의료진모바일이 즉시 구분됨
- 보드 위에서 앱별 차이가 더 명확함

단점:

- 같은 서비스 제품군의 통일감이 약해질 수 있음
- 색상 규칙이 복잡해짐
- 이후 화면마다 색상 적용 기준을 다시 정해야 함

## 5. 권장 결정

현재 단계에서는 A안을 권장한다.

이유:

- 하루안부는 여러 앱이 같은 서비스를 이루는 구조이므로, 우선은 통일감이 더 중요하다.
- 요양보호사앱과 의료진모바일은 실제 사용자 역할이 다르지만, 둘 다 돌봄/의료 현장 그룹으로 묶을 수 있다.
- 색을 먼저 나누기보다 정보 밀도, 문장 톤, 아이콘 선택, 카드 내용 구조로 차이를 만드는 편이 안전하다.
- 추후 대표 화면 3개를 보드 기준으로 맞춘 뒤에도 두 앱이 너무 비슷하면 그때 `caregiver` sub-accent를 추가해도 늦지 않다.

따라서 footer에는 아래처럼 정리하는 것을 권장한다.

```text
현재 결정: A안 유지.
요양보호사앱과 의료진모바일은 같은 care green 제품군으로 유지한다.
차이는 색보다 정보 밀도, 문장 톤, 아이콘, CTA 우선순위로 만든다.
단, 대표 화면 적용 후에도 구분이 약하면 caregiver sub-accent를 v0.3 후보로 재검토한다.
```

## 6. 추가로 하면 좋은 정리

### 6.1 보드 버전 표기 통일

현재 상단에는 `v0.1`, footer에는 `v0.2`가 섞여 있다.

수정 방향:

- 둘 중 하나로 통일한다.
- 12종이 모두 들어간 현재 상태라면 `v0.2`가 적절하다.

권장:

```text
모바일 컴포넌트 보드 v0.2
```

### 6.2 `preview.html` nav 들여쓰기 확인

`preview.html` nav 부분에서 `Errors` 링크의 들여쓰기/구조가 약간 어긋나 보인다.

예상 위치:

```html
<a href="role-component-board.html" class="pv-nav__link">Board (모바일 3종)</a>
<a href="preview-errors.html" class="pv-nav__link">Errors</a>
```

기능상 문제는 없어 보이나, HTML 구조가 깔끔하도록 같은 depth 안에 정렬한다.

## 7. 수정 후 재검증 체크리스트

수정 후 아래 항목을 다시 확인한다.

```bash
wc -l 07_디자인/role-component-board.html
rg -n "style=" 07_디자인/role-component-board.html
rg -n "#[0-9A-Fa-f]{3,8}" 07_디자인/role-component-board.html
rg -n "[\\x{1F300}-\\x{1FAFF}]" 07_디자인/role-component-board.html
rg -n "<iconify-icon" 07_디자인/role-component-board.html
```

기대 결과:

- inline style: 0건
- 설명 텍스트 포함 직접 hex: 가능하면 0건
- 이모지: 0건
- 아이콘: 모두 `iconify-icon`
- 12개 섹션 유지
- 36개 role 컬럼 유지
- `preview.html`에서 보드 진입 가능
- 브라우저 렌더링 시 콘솔 오류 없음

## 8. 클로드에게 바로 보낼 요약 지시

아래 문장을 그대로 전달해도 된다.

```text
role-component-board.html은 방향이 좋고 채택 가능해. 다만 정답 기준 보드로 쓰기 전에 아래만 정리해줘.

1. SOS 섹션의 danger 설명값 `#FF3B30`을 현재 토큰 기준으로 수정해줘. 가능하면 `danger · var(--color-danger)`처럼 토큰명 중심으로 표시해줘.
2. 컬럼 헤더와 delta 설명에 남아 있는 `#2C7AFC`, `#22C55E` 같은 직접 hex 텍스트를 `var(--color-accent)` 중심으로 바꿔줘. 보드는 색상값보다 토큰명을 보여주는 게 맞아.
3. 탭바 섹션의 inline style 3건을 `.col__body--tabbar` 같은 클래스로 빼줘. 40px 직접값은 spacing token으로 바꿔줘.
4. 상단 v0.1 / footer v0.2 버전 표기를 v0.2로 통일해줘.
5. preview.html nav에서 Board와 Errors 링크 구조/들여쓰기를 깔끔하게 맞춰줘.
6. footer의 caregiver vs medical 결정은 현재 A안 유지로 정리해줘. 같은 care green 제품군으로 두고, 차이는 색보다 정보 밀도, 문장 톤, 아이콘, CTA 우선순위로 만든다는 방향으로 적어줘. caregiver sub-accent는 v0.3 후보로 남겨줘.

수정 후에는 inline style 0건, 설명 텍스트 포함 직접 hex 가능하면 0건, 이모지 0건, 12섹션/36컬럼 유지, 브라우저 콘솔 오류 0건으로 다시 검증해줘.
```
