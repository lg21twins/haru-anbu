# role-component-board 재검토 피드백

작성일: 2026-05-23  
검토 대상: `07_디자인/role-component-board.html`, `07_디자인/preview.html`, `07_디자인/tokens/tokens.css`  
목적: 클로드가 수정한 모바일 3종 컴포넌트 보드의 남은 수정 사항을 정리한다.

## 1. 재검토 결론

보드의 큰 구조는 유지되어 있고, 기준 보드로 가는 방향은 맞다.

확인 결과:

- `role-component-board.html`: 1382줄
- 섹션 수: 12개
- role 컬럼 수: 36개
- guardian / caregiver / medical 각각 12개씩
- `<iconify-icon>` 요소: 63개
- 이모지: 0건

하지만 이전 피드백 중 일부 핵심 항목이 아직 반영되지 않았다.

남은 문제:

- 상단 버전은 여전히 `v0.1`, footer는 `v0.2`
- `col__hex` 클래스명과 직접 hex 설명 텍스트가 여전히 남아 있음
- 탭바 섹션에 inline style 3건이 남아 있음
- `preview.html` nav에서 `Errors` 링크 들여쓰기/구조가 아직 어긋나 있음
- `tokens.css`의 danger 관련 히스토리 주석과 현재 값 설명이 서로 충돌함

## 2. 남은 필수 수정 사항

### 2.1 보드 버전 표기 통일

현재:

```html
<div class="pv-nav__version">v0.1 · 2026-05-23</div>
<h1 class="pv-header__title">모바일 컴포넌트 보드 v0.1</h1>
...
<h3>v0.2 — 12종 모두 수록</h3>
```

문제:

상단은 `v0.1`, footer는 `v0.2`라서 문서 상태가 헷갈린다.

수정:

```html
<div class="pv-nav__version">v0.2 · 2026-05-23</div>
<h1 class="pv-header__title">모바일 컴포넌트 보드 v0.2</h1>
```

footer의 `v0.2 — 12종 모두 수록`은 유지한다.

### 2.2 `col__hex`를 `col__token`으로 변경

현재:

```css
.col__hex { ... }
```

```html
<div class="col__hex">accent · #2C7AFC</div>
<div class="col__hex">accent · #22C55E</div>
```

문제:

이 보드는 색상표가 아니라 컴포넌트 기준 보드다. 클래스명과 표시 문구가 `hex` 중심이면, 작업자가 토큰보다 직접 색상값을 기준으로 이해할 수 있다.

수정:

```css
.col__token {
  font-family: var(--font-family-mono);
  font-size: 11px;
  opacity: 0.85;
  margin-top: 2px;
}
```

모든 HTML의 `col__hex`를 `col__token`으로 변경한다.

### 2.3 설명 텍스트의 직접 hex를 토큰명 중심으로 변경

현재 남아 있는 예:

```text
accent · #2C7AFC
accent · #22C55E
active · #2C7AFC
active · #22C55E
둘 다 #22C55E primary
danger · #FF3B30
```

수정 방향:

```text
accent · var(--color-accent)
active · var(--color-accent)
primary · var(--color-accent)
danger · var(--color-danger)
```

권장 문구:

```html
<div class="col__token">accent · var(--color-accent)</div>
<div class="col__token">active · var(--color-accent)</div>
<div class="col__token">danger · var(--color-danger)</div>
```

delta 문장도 아래처럼 수정한다.

현재:

```text
둘 다 #22C55E primary, 52px, 같은 라운드.
```

수정:

```text
둘 다 var(--color-accent) primary, 52px, 같은 라운드.
```

주의:

현재 `tokens.css` 기준 `--color-danger`는 `#FF3B30`으로 되어 있으므로, `danger · #FF3B30`이 색상 자체로 틀린 것은 아니다. 다만 보드에서는 직접값보다 `var(--color-danger)`로 표기하는 것이 맞다.

### 2.4 탭바 섹션 inline style 3건 제거

현재:

```html
<div class="col__body" style="display: flex; justify-content: center; padding-top: 40px; padding-bottom: 40px;">
```

3개 role 컬럼에 동일하게 남아 있다.

문제:

보드가 “직접 스타일 금지”의 기준 페이지인데, 보드 안에 inline style이 남아 있다.

수정:

CSS에 클래스 추가:

```css
.col__body--tabbar {
  display: flex;
  justify-content: center;
  padding-top: var(--space-9);
  padding-bottom: var(--space-9);
}
```

HTML 변경:

```html
<div class="col__body col__body--tabbar">
```

세 role 컬럼 모두 같은 클래스를 사용한다.

### 2.5 `preview.html` nav 구조 정리

현재:

```html
<a href="role-component-board.html" class="pv-nav__link">Board (모바일 3종)</a>
<a href="preview-errors.html" class="pv-nav__link">Errors</a>
</div>
```

실제 파일에서는 `Errors` 링크 들여쓰기가 한 단계 빠져 보인다.

수정:

```html
<div class="pv-nav__links">
  <a href="preview.html" class="pv-nav__link pv-nav__link--active">개요</a>
  <a href="preview-foundations.html" class="pv-nav__link">Foundations</a>
  <a href="preview-components.html" class="pv-nav__link">Components</a>
  <a href="preview-patterns.html" class="pv-nav__link">Patterns</a>
  <a href="preview-roles.html" class="pv-nav__link">Roles</a>
  <a href="role-component-board.html" class="pv-nav__link">Board (모바일 3종)</a>
  <a href="preview-errors.html" class="pv-nav__link">Errors</a>
</div>
```

기능상 큰 문제는 아니지만, 기준 문서이므로 HTML 구조도 깔끔하게 맞추는 것이 좋다.

## 3. 새로 확인된 tokens.css 이슈

### 3.1 danger red 히스토리 주석과 현재 값 충돌

현재 `tokens.css` 상단 히스토리는 `Danger Red #E32B25`를 기준으로 설명한다.

예:

```text
v3.2.7 · Danger Red 재정의 (rose → Rivian Alarm #E32B25)
```

하지만 현재 실제 semantic token은 아래처럼 되어 있다.

```css
--color-danger: #FF3B30; /* v3.2.9 (2026-05-23): iOS System Red로 통일 — 세 앱 일관성 (사용자 결정) */
```

문제:

실제 값은 `#FF3B30`인데 문서 상단 히스토리와 중간 설명은 여전히 `#E32B25` 중심이다. 나중에 누가 보더라도 “현재 danger가 무엇인가”를 헷갈릴 수 있다.

수정 방향:

`tokens.css` 상단 변경 이력에 v3.2.9를 명확히 추가한다.

권장 추가 문구:

```text
v3.2.9 (2026.05.23): Danger Red를 iOS System Red #FF3B30으로 재통일.
                     세 앱 SOS/긴급/위험 시그널을 같은 값으로 맞춤.
                     palette-red 스케일은 과거 Rivian 계열이 남아 있으나,
                     실제 컴포넌트는 --color-danger를 기준으로 사용한다.
```

또는 더 깔끔하게 가려면 `--palette-red-500` 자체도 `#FF3B30`으로 바꾸고 red scale을 다시 정리한다. 다만 이건 영향 범위가 커질 수 있으므로, 지금은 우선 주석 정리를 권장한다.

## 4. caregiver와 medical 정책 문구는 현재 방향 유지 가능

클로드가 이번 수정에서 다음 방향으로 정리했다.

```text
요양보호사앱과 의료진모바일은 별도 앱이지만 디자인 컴포넌트는 완전히 일치한다.
```

이 방향은 현재 단계에서 받아들일 수 있다.

다만 표현을 조금만 부드럽게 하는 것을 권장한다.

현재 표현:

```text
디자인 컴포넌트는 100% 동일하다.
```

권장 표현:

```text
공통 컴포넌트의 형태와 물성은 동일하게 유지한다.
차이는 콘텐츠, 라벨, 아이콘 선택, 정보 구조에서 만든다.
```

이유:

`100% 동일`이라고 쓰면 향후 의료진 앱에 정보 밀도나 우선순위 표시가 추가될 때 예외를 만들기 어려워진다. “형태와 물성은 동일”이라고 쓰면 같은 컴포넌트 시스템을 유지하면서도 화면 구조 차이는 허용할 수 있다.

## 5. 수정 후 재검증 명령

아래 기준으로 재확인한다.

```bash
python3 - <<'PY'
from pathlib import Path
import re
s = Path('07_디자인/role-component-board.html').read_text()
print('sections', s.count('<section class="section'))
print('cols', s.count('<div class="col" data-role='))
for role in ['guardian','caregiver','medical']:
    print(role, s.count(f'data-role="{role}"'))
print('inline style', s.count('style="'))
print('iconify elements', s.count('<iconify-icon'))
print('hex occurrences', len(re.findall(r'#[0-9A-Fa-f]{3,8}', s)))
PY
```

기대 결과:

```text
sections 12
cols 36
guardian 12
caregiver 12
medical 12
inline style 0
hex occurrences 0
```

단, `tokens.css` 내부는 색상 정의 파일이므로 hex가 있어도 정상이다. 위 검사는 `role-component-board.html`에만 적용한다.

## 6. 클로드에게 바로 보낼 요약 지시

아래 문장을 그대로 전달해도 된다.

```text
수정본 다시 봤는데 큰 구조는 좋아. 12섹션/36컬럼/3-role 구조는 유지됐고 방향도 맞아. 다만 이전 피드백 중 몇 개가 아직 남아 있어.

1. role-component-board 상단 버전이 아직 v0.1이고 footer는 v0.2야. nav version과 h1을 v0.2로 통일해줘.
2. `.col__hex` 클래스명과 표시 문구가 아직 hex 중심이야. `.col__token`으로 바꾸고, `accent · #2C7AFC`, `active · #22C55E`, `danger · #FF3B30` 같은 문구를 `accent · var(--color-accent)`, `active · var(--color-accent)`, `danger · var(--color-danger)`로 바꿔줘.
3. 버튼 delta에 남아 있는 `#22C55E primary`도 `var(--color-accent) primary`로 바꿔줘.
4. 탭바 섹션에 inline style 3건이 아직 있어. `.col__body--tabbar` 클래스로 빼고, 40px 직접값은 `var(--space-9)` 같은 spacing token으로 바꿔줘.
5. preview.html nav에서 Errors 링크 들여쓰기/구조가 아직 어긋나 있어. Board 링크와 같은 depth로 정리해줘.
6. tokens.css는 현재 `--color-danger: #FF3B30`인데 상단 히스토리에는 #E32B25 설명이 강하게 남아 있어. v3.2.9 danger 변경 이력을 상단에 추가해서 현재 기준이 #FF3B30임을 명확히 해줘.
7. footer의 “100% 동일” 표현은 조금 강하니 “공통 컴포넌트의 형태와 물성은 동일, 차이는 콘텐츠/라벨/아이콘/정보 구조에서 만든다”로 다듬어줘.

수정 후 role-component-board.html 기준으로 inline style 0건, 직접 hex 0건, 12섹션/36컬럼 유지되는지 다시 검증해줘.
```
