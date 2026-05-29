# design_audit 개선 지시

작성일: 2026-05-23  
대상 파일:

- `07_디자인/scripts/design_audit.py`
- `07_디자인/review-rules/app-folder.json`
- `07_디자인/review-rules/mobile-apps.json`
- `07_디자인/review-reports/full_cleanup_summary_20260523.md`
- 필요 시 `07_디자인/tokens/tokens.css`

목적: 현재 자동 감사 결과가 전 영역 PASS로 나오지만, 감사 로직이 일부 위반을 놓칠 수 있으므로 검사 기준을 강화한다.

## 1. 전체 판단

현재 작업 방향은 좋다.

좋은 점:

- `role-component-board` 기준 보드 감사가 동작함
- `app-folder` 타깃이 추가됨
- CSS 변수 setter inline style을 허용한 것은 현실적임
- 감사 리포트가 MD로 생성되는 구조가 생김
- 전체 앱을 정리하려는 흐름 자체는 맞음

하지만 현재 “전 영역 PASS”는 그대로 신뢰하면 안 된다.  
이유는 일부 파일 유형, 특히 `.css` 파일의 hex 검사가 제대로 작동하지 않기 때문이다.

정확히는 다음과 같이 표현하는 것이 맞다.

```text
현재 audit v0.1 기준 PASS.
단, CSS 파일 hex 검사, app-folder iconify 검사, 토큰 정의 허용 범위는 v0.2에서 강화 필요.
```

## 2. 가장 큰 문제: CSS 파일 hex 검사가 사실상 빠져 있음

현재 `find_hex_in_body()`는 HTML 안의 `<style>...</style>` 블록을 중심으로 검사한다.

문제:

- `.css` 파일에는 `<style>` 블록이 없다.
- 그래서 `.css` 파일 안에 직접 hex가 있어도 검사 결과가 0건으로 나올 수 있다.
- 즉, 현재 app-folder PASS는 “정책적으로 허용해서 PASS”가 아니라 “검사가 안 돼서 PASS”인 부분이 있다.

실제 수동 검색 결과, active 앱 파일에는 아직 hex가 잡힌다.

예:

```text
v11_보호자앱      635건
v11_요양보호사앱   26건
v15_의료진앱       63건
v10_의료진웹      362건
v12_환자앱         59건
v13_온보딩          1건
```

물론 이 중에는 `meta theme-color`, 토큰 정의, 허용 가능한 변수 정의도 섞여 있다.  
하지만 현재 스크립트는 그 구분 이전에 `.css` 파일을 제대로 검사하지 못하고 있다.

## 3. 개선 1: 파일 확장자별 hex 검사 분리

`find_hex_in_body()` 하나로 모든 파일을 처리하지 말고, 파일 확장자별 검사 함수를 분리한다.

권장 구조:

```python
def find_hex_violations(path: Path, text: str, rules: dict) -> list[tuple[int, str]]:
    if path.suffix == ".html":
        return find_hex_in_html(path, text, rules)
    if path.suffix == ".css":
        return find_hex_in_css(path, text, rules)
    if path.suffix == ".js":
        return find_hex_in_js(path, text, rules)
    return []
```

### 3.1 HTML 검사

HTML에서는 아래를 구분한다.

검사 대상:

- `<style>` 블록 안 직접 hex
- `style="..."` 안 직접 hex
- JS 문자열 안 직접 hex

허용 후보:

- `<meta name="theme-color" content="#...">`  
  단, 이건 별도 카운트로 “허용된 meta theme-color”라고 리포트에 표시하면 좋다.

주의:

`meta theme-color`도 가능하면 토큰과 맞춰 관리해야 하지만, 브라우저 메타 태그 특성상 CSS var가 안정적으로 동작하지 않을 수 있으므로 일단 허용 가능하다.

### 3.2 CSS 검사

CSS 파일에서는 전체 파일을 검사한다.

허용:

- `07_디자인/tokens/tokens.css` 안의 토큰 정의
- 명시적으로 허용된 토큰 파일

경고 또는 실패:

- 앱 CSS 파일 안의 직접 hex
- `var(--token, #fallback)` 형태의 hex fallback
- 로컬 `--some-color: #hex` 정의

중요:

앱 파일의 `:root { --local-color: #hex; }`를 무조건 허용하면 안 된다.  
이것은 화면별 색상 독립을 다시 허용하는 것과 같다.

### 3.3 JS 검사

JS에서는 아래 패턴을 검사한다.

- `"#2C7AFC"` 같은 색상 문자열
- `'#2C7AFC'`
- template string 안 hex
- DOM에 직접 넣는 inline style 문자열

다만 Chart.js 등 외부 라이브러리 fallback은 예외가 필요할 수 있다. 이 경우도 무조건 허용하지 말고, 허용 목록으로 관리한다.

## 4. 개선 2: `:root` / `[data-*]` 토큰 정의 허용 범위 제한

현재 정책:

```text
:root / [data-*] 블록 안 `--var: #hex` 토큰 정의는 허용
```

문제:

이 정책은 너무 넓다. 앱 화면 파일에서 새 색상을 마음대로 만들어도 통과할 수 있다.

개선 방향:

```text
토큰 정의 파일에서는 `--var: #hex` 허용
앱 화면 파일에서는 기본적으로 금지
예외가 필요하면 review-rules에 허용 파일/허용 변수명을 명시
```

권장 규칙 예시:

```json
{
  "allowed_token_definition_files": [
    "07_디자인/tokens/tokens.css"
  ],
  "allowed_local_token_patterns": [
    "--chart-*",
    "--gauge-*"
  ]
}
```

주의:

허용 패턴은 최소화한다.  
`--*` 전체 허용은 금지한다.

## 5. 개선 3: `app-folder`에도 iconify 외 아이콘 검사 추가

현재 `role-component-board`에는 `find_non_iconify_icons()`가 들어가 있지만, `app-folder`에는 적용되지 않는다.

문제:

앱 폴더 안에 인라인 `<svg>`가 남아 있어도 현재 감사는 PASS할 수 있다.

실제 예:

```text
v11_요양보호사앱/c03-sotong.html
<svg width="22" height="22" ... fill="#fff" ...>
```

개선:

`check_app_folder()`에서도 아래를 집계한다.

- 인라인 `<svg>`
- `.svg` 이미지 중 브랜드 로고가 아닌 것
- `iconify-icon`이 아닌 아이콘 사용

예외:

- 하루안부 브랜드 로고 SVG
- `logo/brand-system/` 경로
- 접근성상 장식으로 쓰는 브랜드 심볼

리포트 항목 추가:

```text
아이콘 · iconify-icon 외 사용
```

## 6. 개선 4: 리포트 문구 정정

현재 `full_cleanup_summary_20260523.md`는 “전 영역 PASS”라고 강하게 말한다.

문제:

감사 로직이 아직 충분히 강하지 않은 상태에서 “전 영역 PASS”라고 쓰면, 실제 디자인 시스템 정리가 완전히 끝난 것으로 오해할 수 있다.

수정 권장:

```text
전 영역 PASS
```

를 아래처럼 변경한다.

```text
audit v0.1 기준 전 영역 PASS
```

그리고 상단에 주석 추가:

```text
주의: 현재 PASS는 audit v0.1 규칙 기준이다.
v0.2에서 CSS 파일 hex 검사, app-folder iconify 검사, 토큰 정의 허용 범위를 강화해야 한다.
```

## 7. 개선 5: 유틸리티 클래스 남발 방지 규칙 추가

`tokens.css`에 `.u-fs-26`, `.u-h-8`, `.u-w-40` 같은 유틸리티가 많이 추가되었다.

장점:

- inline style을 줄일 수 있다.
- 반복되는 임시 치수를 빠르게 정리할 수 있다.

위험:

- 너무 많아지면 사실상 “class로 쓰는 inline style”이 된다.
- 디자이너 관점에서 의미가 없는 숫자 클래스가 늘어난다.
- 컴포넌트 기준 정리가 아니라 유틸리티 조합으로 화면마다 다시 달라질 수 있다.

권장 정책:

- 숫자형 유틸리티는 임시 정리용으로 제한한다.
- 자주 쓰이는 패턴은 의미 기반 컴포넌트 클래스로 승격한다.
- 새 유틸리티 추가 시 리포트에 카운트한다.

감사 항목 후보:

```text
유틸리티 클래스 수
숫자형 유틸리티 수
새로 추가된 u-* 클래스 목록
```

권장:

`.u-fs-26`보다 `.u-text-display` 선호  
`.u-w-40`보다 `.avatar--sm`, `.icon-btn--sm` 같은 의미 기반 클래스 선호

## 8. 개선 6: `mobile-apps` 타깃 실제 구현

현재 `mobile-apps.json`은 stub 상태다.

문제:

전체 앱을 관리하려면 `mobile-apps` 타깃이 실제로 작동해야 한다.

구현 대상:

```text
v11_보호자앱
v11_요양보호사앱
v15_의료진앱
```

확장 후보:

```text
v12_환자앱
v13_온보딩
v10_의료진웹
```

검사 항목:

- 각 폴더의 inline style
- 직접 hex
- 이모지
- iconify 외 아이콘
- 공통 CSS import 누락
- `tokens.css` import 누락
- 대표 화면 3개 존재 여부
- 대표 화면이 role-component-board 기준 컴포넌트를 쓰는지 여부

대표 화면:

```text
v11_보호자앱/g-guardian-live.html
v11_요양보호사앱/c01-today.html
v15_의료진앱/d01-home.html
```

## 9. 우선순위

### P0 — 반드시 먼저

1. `.css` 파일 hex 검사 제대로 구현
2. `:root --var: #hex` 허용 범위를 `tokens.css` 중심으로 제한
3. `app-folder`에 iconify 외 아이콘 검사 추가

### P1 — 리포트 신뢰도 개선

4. `full_cleanup_summary_20260523.md` 문구를 “audit v0.1 기준 PASS”로 수정
5. 허용된 예외와 실제 위반을 분리해서 리포트
6. meta theme-color, tokens.css hex, CSS 변수 setter 등 허용 항목을 별도 카운트

### P2 — 운영성 개선

7. 유틸리티 클래스 남발 방지 규칙 추가
8. `mobile-apps` 타깃 실제 구현
9. 이후 `visual_check.py`로 브라우저 렌더링 확인 추가

## 10. 수정 후 기대되는 감사 결과 형식

단순히 0건만 보여주지 말고, 아래처럼 분리해서 보여주는 것이 좋다.

```text
직접 hex 위반: 0건
허용된 tokens.css 토큰 정의: 180건
허용된 meta theme-color: 6건
허용된 CSS 변수 setter inline style: 12건
iconify 외 아이콘 위반: 0건
브랜드 로고 SVG 허용: 3건
```

이렇게 해야 “검사를 안 해서 0건”인지 “검사했지만 허용/위반을 분리해서 0건”인지 명확해진다.

## 11. 클로드에게 바로 보낼 요약 지시

아래 문장을 그대로 전달해도 된다.

```text
현재 정리 방향은 좋고 app-folder 타깃/리포트 자동화도 잘 갔어. 다만 지금 PASS를 그대로 믿기엔 design_audit.py가 아직 너무 느슨해.

핵심 문제는 `.css` 파일 hex 검사가 사실상 빠져 있다는 점이야. 현재 find_hex_in_body()가 HTML의 <style> 블록 중심이라 CSS 파일에는 hex가 있어도 0건으로 처리될 수 있어. 실제 rg로 보면 active 앱 폴더에 아직 hex가 많이 잡혀.

다음 개선을 해줘:

1. hex 검사를 파일 확장자별로 분리해줘. HTML/CSS/JS를 다르게 처리해야 해.
2. CSS 파일은 전체 내용을 검사해줘. 단, `07_디자인/tokens/tokens.css`의 토큰 정의는 허용해줘.
3. `:root`나 `[data-*]` 안의 `--var: #hex`를 무조건 허용하지 말아줘. 토큰 정의 파일에서는 허용, 앱 화면 파일에서는 기본 금지로 바꿔줘. 예외는 review-rules에 명시하는 방식으로.
4. app-folder 감사에도 iconify 외 아이콘 검사를 추가해줘. 인라인 svg, 브랜드 로고가 아닌 svg 이미지 사용을 잡아줘.
5. full_cleanup_summary_20260523.md의 “전 영역 PASS”는 “audit v0.1 기준 PASS”로 수정해줘. 그리고 v0.2에서 검사 강화가 필요하다는 주석을 추가해줘.
6. tokens.css에 추가된 숫자형 유틸리티 클래스가 너무 많아지지 않도록, 새 u-* 클래스 수와 숫자형 유틸리티 수를 리포트에 표시하는 규칙을 추가해줘.
7. mobile-apps 타깃은 현재 stub이니까 실제로 v11_보호자앱, v11_요양보호사앱, v15_의료진앱을 검사하도록 구현해줘.

수정 후 리포트는 위반 0건뿐 아니라 허용된 예외도 따로 보여줘. 예: tokens.css 토큰 정의 hex 몇 건 허용, meta theme-color 몇 건 허용, CSS 변수 setter inline style 몇 건 허용. 그래야 검사를 안 해서 0건인지, 검사하고 분류해서 0건인지 구분할 수 있어.
```

## 12. 완료 기준

이 개선 라운드는 아래 조건을 만족하면 완료로 본다.

- `.css` 파일 내 hex 검사 작동
- 앱 파일의 로컬 `--var: #hex`가 기본적으로 경고 또는 실패 처리
- `tokens.css`의 토큰 정의는 허용 처리
- `app-folder`에서 iconify 외 아이콘 사용 검사
- `mobile-apps` 타깃 실제 구현
- 리포트에서 위반과 허용 예외를 분리 표기
- 기존 `role-component-board`는 계속 PASS
- 대표 모바일 앱 폴더 감사 결과가 신뢰 가능한 형태로 출력
