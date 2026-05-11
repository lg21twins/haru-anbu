# 요양보호사 앱 v11 UX/UI 디자인 리뷰

작성일: 2026-05-10  
검토 대상: `v11_요양보호사앱` 전체  
검토 방식: 파일 전체 정독 기반 UX/UI 리뷰  
주요 관점: 디자인 시스템 통일성, 현장 사용성, 정보 위계, 탭별 UX, 심미성

---

## 0. 한 줄 결론

요양보호사 앱은 “현장에서 한 손으로 빠르게 기록하는 도구”라는 방향은 좋다. 특히 `c02-checklist.html`의 빠른 기록, 환자별 기록, 8단계 스텝퍼는 제품 핵심이 잘 살아 있다. 다만 현재는 보호자앱 v9.5의 글래스/그라디언트 스타일과 새 디자인 시스템 v3.1 방향이 섞여 있어, 앱 전체가 깔끔하지만 아직 최신 디자인 시스템으로 정돈된 느낌은 약하다.

가장 큰 문제는 다음 5가지다.

1. `tokens.css`만 import하고 `system/app.css`, `system/components.css`를 쓰지 않는다.
2. 화면마다 header, card, tabbar, SOS, toast, sheet, icon button을 반복 정의한다.
3. README와 구현 파일에 오래된 디자인 기준, 하드코딩 색상, 특수기호, 외부 아이콘 세트가 남아 있다.
4. 현장 사용 앱인데 34px, 36px, 40px 버튼이 많아 48px 터치 타깃 원칙과 충돌한다.
5. 주요 업무 액션이 toast-only로 끝나는 곳이 많아 실제 제품처럼 느껴지지 않는다.

요양보호사 앱은 의료진 앱보다 “사용자 연령, 현장 동선, 손이 바쁜 상황”을 더 강하게 고려해야 한다. 디자인은 예쁘게 보이는 것보다 더 크고, 더 명확하고, 더 덜 헷갈리는 쪽이 맞다.

---

## 1. 검토 대상 파일

- `README.md`: 요양보호사 앱 v11 원칙과 화면 인벤토리
- `c01-today.html`: 오늘 탭
- `c02-checklist.html`: 케어 기록/체크리스트 탭
- `c03-sotong.html`: 소통 탭
- `c04-mypage.html`: 마이 탭
- `c04-schedule.html`: 일정 detail 화면

---

## 2. 전체 디자인 시스템 통일성

### 잘 된 점

- 모든 주요 HTML이 `<html lang="ko" data-role="caregiver" data-platform="mobile">`을 사용한다.
- 모든 주요 HTML이 `../07_디자인/tokens/tokens.css`를 import한다.
- 색상 방향은 caregiver 역할에 맞게 green 계열을 중심으로 잡았다.
- 탭 구조가 단순하다: 홈, 기록, 소통, 마이.
- SOS가 전역 FAB로 존재해 현장 업무 앱의 긴급성을 반영한다.
- 카드, 탭바, 바텀시트, toast 등 기본 UI 패턴이 화면마다 비슷해 최소한의 일관성은 있다.

### 문제점

현재 구현은 `tokens.css` 위에 각 화면이 자기 CSS를 잔뜩 얹은 구조다. 디자인 시스템의 공통 컴포넌트를 실제로 재사용하는 구조가 아니다.

반복되는 로컬 정의:

- `--accent`, `--accent-soft`, `--accent-strong`
- `--danger`, `--warn`, `--t1`, `--t2`, `--t3`
- `body`, `.bg`, `.app`
- `.header`, `.icon-btn`
- `.card`, `.tabbar`, `.sos-fab` 또는 `.sos`
- `.toast`, `.sheet`, `.overlay`, `.bottom-bar`

이 상태에서는 한 화면을 고쳐도 나머지 화면은 그대로 남는다. 예를 들어 `c01`의 SOS는 3초 롱프레스 로직이 있지만 `c02`, `c03`, `c04`에서는 SOS가 toast-only에 가깝다. 같은 앱의 같은 SOS인데 화면마다 실제 경험이 다르다.

### 개선안

- `07_디자인/system/app.css`, `07_디자인/system/components.css`를 연결한다.
- 요양보호사 앱 전용 공통 CSS가 필요하면 `v11_요양보호사앱/caregiver.css` 같은 파일로 분리한다.
- 화면별 HTML 내부 style은 layout과 화면 고유 컴포넌트만 남긴다.
- appbar, tabbar, SOS, toast, sheet, card, icon button, status badge는 공통화한다.
- README의 디자인 기준도 최신 디자인 시스템 기준으로 수정한다.

---

## 3. 심미성 평가

### 현재 인상

전반적으로 따뜻하고 부드럽다. green 계열, glass card, 둥근 pill, 흐린 배경이 요양/케어 서비스의 부드러운 이미지를 만든다. 보호자앱보다 업무 중심으로 정리되어 있고, 의료진 앱보다 친근한 톤이라 사용자 역할에 맞는 방향은 잡혀 있다.

하지만 심미성 면에서 몇 가지가 아쉽다.

- green 계열이 배경, 카드, badge, icon, button에 너무 넓게 퍼져 단조롭게 보일 수 있다.
- glass 스타일이 여러 화면에서 반복되지만 정확한 수치가 다르다.
- card radius가 16px, 20px 등으로 섞여 있고, shadow/border도 화면마다 다르다.
- 배경에 radial/linear gradient가 자주 쓰이는데 v3.1의 flat-first 방향과는 거리가 있다.
- `ph:*`, `tabler:*`, inline SVG 로고, fluent icon이 섞여 아이콘 시스템이 통일되지 않는다.

### 개선 방향

요양보호사 앱은 “따뜻함”보다 “현장에서 바로 알아보는 명확함”이 더 중요하다. 따라서 다음 방향이 좋다.

- 배경은 더 flat하게 만들고, green은 상태/CTA/역할 강조에만 쓴다.
- card는 shadow보다 border와 spacing으로 구분한다.
- 위험/주의/완료/대기 상태는 색상뿐 아니라 텍스트와 iconify fluent 아이콘으로 같이 표현한다.
- 10px, 11px 텍스트를 줄이고, 핵심 업무 문구는 최소 13px 이상으로 정리한다.
- 한 화면에서 primary CTA는 하나만 명확하게 둔다.

---

## 4. README 기준 문제

`README.md`는 현재 최신 규칙과 충돌하는 내용이 있다.

### 문제점

- 상태 줄에 이모지가 들어가 있다. 프로젝트 규칙은 UI와 문서 전체에서 이모지 금지다.
- “데스크톱 웹 아님” 설명에도 이모지 기호가 들어가 있다.
- 디자인 기준이 “v9.5 보호자앱 시각 언어 공유”로 되어 있는데, 현재 프로젝트 기준은 `07_디자인`의 새 디자인 시스템이다.
- 색상이 `#059669`, `#22C55E`처럼 하드코딩되어 있다.
- “인지·정서 이모지 4단계”라고 되어 있어 앱 규칙과 정면 충돌한다.
- Pretendard Variable이라고 쓰여 있지만 실제 HTML은 Google Fonts의 Noto Sans SC만 import한다.

### 개선안

- README에서 이모지와 장식 기호를 모두 제거한다.
- 디자인 기준을 `07_디자인/tokens/tokens.css`, `system/app.css`, `system/components.css` 중심으로 바꾼다.
- “인지·정서 이모지 4단계”는 “인지·정서 5단계 텍스트/아이콘 선택”처럼 바꾼다.
- 폰트 정책을 실제 구현과 맞춘다. 한국어 기본은 디자인 시스템 폰트, 중국어/베트남어 폴백만 별도 정의하는 식이 좋다.

---

## 5. 전체 UX 구조

### 잘 된 점

- 4탭 구조가 명확하다.
- `오늘`은 지금 해야 할 일을 보여주고, `기록`은 실제 기록을 담당하고, `소통`은 보고/보호자 공유를 담당하고, `마이`는 근무/설정을 담당한다.
- 요양보호사 앱답게 케어 기록이 가장 깊게 설계되어 있다.
- 빠른 기록과 스텝퍼를 모두 제공해 숙련 사용자와 초보 사용자를 동시에 고려했다.
- SOS를 전역화한 점은 현장 앱에서 적절하다.

### 문제점

#### 하단 탭이 아이콘만 있어 인지가 느릴 수 있다

현장 사용자는 앱을 오래 들여다볼 여유가 없다. 아이콘만 있으면 `기록`, `소통`, `마이`를 빠르게 구분하기 어렵다.

개선안:

- 전체 탭 라벨을 표시한다.
- 공간이 부족하면 active 탭에만 라벨을 표시한다.
- 라벨은 `오늘`, `기록`, `소통`, `마이`로 짧게 둔다.

#### SOS 경험이 화면마다 다르다

`c01-today.html`은 3초 롱프레스와 유형 선택 sheet가 있지만, 다른 화면의 SOS는 toast-only에 가깝다.

개선안:

- 전 화면에서 동일한 SOS 컴포넌트를 사용한다.
- 짧게 누르면 유형 선택 sheet, 길게 누르면 즉시 발신 준비 상태로 통일한다.
- 즉시 발신은 countdown, 취소, 확인 로그가 있어야 한다.

#### toast-only 액션이 너무 많다

일정, 소통, 마이, 기록 곳곳에서 누르면 toast만 뜨는 항목이 많다. 프로토타입에서는 괜찮지만 실제 앱처럼 보이려면 액션의 결과가 명확해야 한다.

개선안:

- detail 화면으로 이동할 액션은 실제 링크로 만든다.
- 아직 구현 전인 액션은 disabled 또는 `준비중` badge로 표시한다.
- 전송/보고/SOS/보호자 공유 같은 업무 액션은 confirmation sheet를 둔다.

#### 터치 타깃이 작다

요양보호사 앱은 손이 바쁜 현장에서 한 손으로 쓰는 앱이다. 그런데 34px, 36px, 40px 버튼이 많다.

개선안:

- 모든 주요 버튼의 실제 hit area를 48px 이상으로 맞춘다.
- icon visual은 작아도 button padding/hit area는 크게 잡는다.
- 작은 토글, 작은 화살표 버튼, 주간 네비 버튼도 48px 기준으로 재정리한다.

---

## 6. 탭별 상세 리뷰

## 6.1 `c01-today.html` - 오늘 탭

### 좋은 점

- 현재 해야 할 일, 근무 진행, 주의 환자, AI 인수인계를 한 화면에서 잘 보여준다.
- “지금 기록 시작” CTA가 명확하다.
- 담당 환자 목록을 너무 앞세우지 않고, 지금 업무와 관찰 이슈를 우선하는 구조가 좋다.
- SOS 3초 롱프레스 아이디어는 현장 앱에 잘 맞는다.

### 불편할 수 있는 점

#### 헤더 로고와 알림 액션이 애매하다

로고는 `href="#"`이고 알림은 toast만 보여준다. 홈에서 가장 자주 누를 수 있는 영역인데 실제 이동이나 detail이 없다.

개선안:

- 로고는 홈이면 링크 제거 또는 현재 화면 표시만 한다.
- 알림은 `c03-sotong.html`의 알림 필터로 이동하게 한다.
- 알림 개수와 unread 상태를 실제 소통 탭과 맞춘다.

#### SOS는 좋지만 발신 확인/취소가 부족하다

3초 길게 누르면 즉시 음성 SOS가 발신되는 구조는 강력하다. 하지만 오발신 방지와 로그가 더 필요하다.

개선안:

- 길게 누른 뒤 바로 발신보다 1초 confirmation countdown을 둔다.
- 발신 직전 “취소”를 제공한다.
- 발신 후에는 간호사/보호자/센터 중 누구에게 전송됐는지 표시한다.

#### 관찰 카드와 SOS의 위험도 언어가 섞일 수 있다

미열 관찰 카드가 warning tone이고 SOS는 emergency tone이다. 두 상태의 차이를 더 명확히 해야 한다.

개선안:

- `관찰`, `주의`, `응급`의 단계별 색상/아이콘/문구 기준을 만든다.
- 미열은 warning card, SOS는 emergency action으로 구분한다.

#### 작은 텍스트가 많다

10px, 11px 보조 텍스트가 많다. 요양보호사 사용자층과 현장 사용성을 고려하면 너무 작을 수 있다.

개선안:

- 시간/메타 텍스트도 최소 12px 이상으로 올린다.
- 핵심 업무 문구는 16px 이상, 버튼 텍스트는 15px 이상 유지한다.

### 우선 수정

- 알림을 소통 탭 detail로 연결한다.
- SOS confirmation/cancel flow를 추가한다.
- 작은 버튼과 헤더 액션의 hit area를 48px로 키운다.
- 위험 단계의 용어와 색상 기준을 정리한다.

---

## 6.2 `c02-checklist.html` - 케어 기록/체크리스트

### 좋은 점

- 앱의 핵심 화면이다.
- 허브, 환자 상세, 빠른 기록, 스텝퍼를 모두 제공해 업무 흐름이 풍부하다.
- “환자별”과 “시간순” 전환은 현장 업무에 맞다.
- 빠른 기록은 5초 저장이라는 목표가 명확하다.
- 8단계 스텝퍼는 초보 사용자나 꼼꼼한 기록이 필요한 상황에 유용하다.
- 오프라인 대기/동기화 pill은 PWA 현장 앱에 필요한 방향이다.

### 불편할 수 있는 점

#### 화면이 너무 많은 역할을 동시에 한다

`c02-checklist.html` 하나 안에 L1 허브, L2 환자 상세, L3 스텝퍼, quick sheet, voice sheet가 모두 들어 있다. 기능은 좋지만 코드와 UX 모두 복잡하다.

사용자 입장에서는 다음 상태가 헷갈릴 수 있다.

- 지금 환자별 목록을 보는 중인지
- 환자 상세를 보는 중인지
- quick sheet로 빠른 기록 중인지
- full stepper로 순차 기록 중인지
- 음성 기록 결과를 확인 중인지

개선안:

- 화면 상태마다 상단 title과 back behavior를 명확히 한다.
- `환자 상세`와 `스텝퍼`는 가능하면 별도 component/state로 명확히 분리한다.
- 하단 탭바가 보여야 하는 상태와 숨겨야 하는 상태를 정한다.
- stepper full screen에서는 하단 탭/SOS가 보이지 않게 하는 것이 맞다.

#### 8단계 스텝퍼는 좋지만 입력이 실제 form처럼 보이지 않는다

혈압, 체온, 맥박, 혈당 버튼을 누르면 toast가 뜬다. 실제 입력/수정 UI가 없으면 기록 앱으로서 신뢰가 떨어진다.

개선안:

- numeric input 또는 keypad sheet를 제공한다.
- 이전 값/현재 값/수정 여부를 명확히 표시한다.
- 저장 전 확인 화면에서 변경된 항목만 요약한다.

#### 정서 단계의 아이콘 시스템이 규칙과 맞지 않는다

`ph:smiley-fill`, `fluent:emoji-24-filled` 같은 아이콘과 README의 “이모지 4단계” 표현은 프로젝트 규칙과 맞지 않는다.

개선안:

- 정서 상태는 `우울`, `무기력`, `양호`, `활기`, `불안` 같은 텍스트 chip으로 유지한다.
- 아이콘이 필요하면 fluent 계열의 face/mood 대체 아이콘 또는 neutral status icon을 사용한다.
- 이모지라는 용어를 README와 UI에서 제거한다.

#### 빠른 기록의 “5초 저장”은 좋지만 저장 신뢰 피드백이 약하다

현재 저장은 toast `기록 저장됨`으로 끝난다. 현장 기록에서는 누락 방지가 중요하다.

개선안:

- 저장 후 해당 환자 row의 완료 count/progress가 즉시 갱신되어야 한다.
- 저장 시 “오프라인 대기”인지 “서버 저장 완료”인지 구분한다.
- 오류/미동기화 상태를 환자 row와 header pill에 반영한다.

#### 환자별/시간순 토글 접근성이 약하다

`role="tablist"`는 있지만 `aria-selected`, `aria-controls`가 없다. 실제 탭으로 쓸 거면 접근성 상태가 필요하다.

개선안:

- `aria-selected`, `aria-controls`, `role="tab"`을 추가한다.
- 단순 정렬 토글이면 segmented control로 명명하고 role을 더 단순화한다.

### 우선 수정

- `c02` 내부 상태를 허브/환자상세/스텝퍼/시트로 명확히 분리한다.
- 입력 필드 toast-only를 실제 입력 sheet로 바꾼다.
- 저장 후 progress와 동기화 상태를 갱신한다.
- 이모지/외부 아이콘 세트 사용을 정리한다.
- full stepper에서 tabbar/SOS 노출 여부를 재검토한다.

---

## 6.3 `c03-sotong.html` - 소통

### 좋은 점

- 인수인계 확인, 메시지, 알림, 보호자 공유가 한 탭에 모여 있어 업무 의도가 명확하다.
- 빠른 보고 sheet는 요양보호사와 간호사 사이의 실제 업무 흐름에 잘 맞는다.
- 보호자 공유 카드도 “오늘의 안부 보내기”라는 명확한 목표가 있다.
- 필터와 unread/today/prev 섹션 구조는 정보 정리에 도움이 된다.

### 불편할 수 있는 점

#### 인수인계 미확인 항목이 toast-only다

“가족 통보” 같은 미확인 항목은 단순 toast보다 실제 처리 flow가 필요하다.

개선안:

- 미확인 항목 클릭 시 detail sheet를 열고 환자, 사유, 추천 문구, 전송 대상, 확인 버튼을 제공한다.
- 처리 후 `4/5`가 `5/5`로 바뀌어야 한다.

#### 이상감지 메시지가 detail 없이 toast만 뜬다

미열, 체위 변경 리마인더, AI 인수인계 등은 현장 대응이 필요한 정보다. toast-only면 위험하다.

개선안:

- alert 메시지는 detail sheet로 열어야 한다.
- detail에는 환자 정보, 발생 시각, 관찰 값, 다음 행동, 간호사 호출/기록으로 이동 CTA를 넣는다.

#### 보호자 공유는 전송 전 확인이 필요하다

“오늘의 안부 보내기 (4명)”은 보호자에게 정보가 나가는 중요한 액션이다. 지금은 버튼 한 번으로 toast 완료가 뜬다.

개선안:

- 전송 전 preview sheet를 띄운다.
- 공유 항목, 대상 보호자, 민감정보 제외 여부를 확인하게 한다.
- 전송 후에는 발송 로그 또는 실패 대상 표시가 필요하다.

#### 아이콘 세트가 섞인다

`ph:sparkle-fill`, inline SVG 로고, fluent icon, tabler pill 등이 섞여 있다.

개선안:

- 모든 UI icon은 `iconify-icon`의 fluent 계열로 통일한다.
- 브랜드 로고는 공통 컴포넌트 또는 이미지 asset으로만 사용한다.

### 우선 수정

- 인수인계 미확인 항목 detail flow 추가
- 이상감지/리마인더 detail sheet 추가
- 보호자 공유 preview/confirmation 추가
- 아이콘 세트 통일

---

## 6.4 `c04-mypage.html` - 마이

### 좋은 점

- 프로필, 오늘 근무, 주간 일정, 의무 진척도, 서비스 기록, 알림 설정, 자격/앱 설정이 잘 묶여 있다.
- 요양보호사에게 중요한 “급여제공기록지”, “출퇴근 GPS”, “의무교육”을 보여주는 점이 좋다.
- 마이 탭이 단순 계정 화면이 아니라 근무 관리 허브 역할을 하는 점은 적절하다.

### 불편할 수 있는 점

#### header icon button이 34px로 너무 작다

설정 버튼과 spacer가 34px 기준이다. 현장 모바일앱 기준으로 작다.

개선안:

- 설정 버튼의 hit area를 48px로 키운다.
- visual icon은 작게 유지해도 실제 button box는 크게 만든다.

#### 많은 메뉴가 toast-only다

서비스 제공기록지, 출퇴근 기록, 인수인계 메모, 자격증, AI 업무 가이드, 언어, 고객센터가 대부분 toast로 끝난다.

개선안:

- 실제로 중요한 `서비스 제공기록지`, `출퇴근 기록`, `언어 설정`은 detail 화면 또는 sheet로 연결한다.
- 구현 전 메뉴는 준비중 badge를 붙인다.
- 한 번 눌렀는데 아무것도 열리지 않는 느낌을 줄인다.

#### 알림 설정 switch가 작고 접근성이 약하다

switch는 시각적으로 작고, row 전체 클릭 가능 여부가 명확하지 않다.

개선안:

- row 전체를 클릭 가능하게 한다.
- switch에 `role="switch"`, `aria-checked`를 넣는다.
- 상태 변경 후 저장 여부를 명확히 보여준다.

### 우선 수정

- 설정/icon button hit area 48px화
- 주요 메뉴 detail 연결 또는 준비중 구분
- switch 접근성/터치 영역 개선

---

## 6.5 `c04-schedule.html` - 일정 detail

### 좋은 점

- 마이에서 push되는 detail 화면으로 별도 tabbar가 없는 구조는 적절하다.
- 주간 일정, 근무 종류, 환자 배정, 근무 관리 메뉴가 한 화면에 잘 정리되어 있다.
- 복잡한 캘린더보다 리스트 중심으로 만든 점은 모바일 현장 앱에 맞다.

### 불편할 수 있는 점

#### 주간 네비 버튼이 작다

이전/다음 주 버튼이 32px다. 실제 사용성 기준으로 작다.

개선안:

- hit area를 48px 이상으로 키운다.
- 화면상 버튼은 32px처럼 보여도 padding으로 터치 영역을 확보한다.

#### 날짜 row가 너무 촘촘할 수 있다

`grid-template-columns: 44px 54px 1fr auto auto` 구조는 작은 화면에서 긴 시간/환자 아바타/chevron이 밀릴 수 있다.

개선안:

- 320px대 폭에서 환자 아바타를 다음 줄로 보내거나, patient count chip으로 축약한다.
- “07:00 -> 15:00” 같은 시간은 줄바꿈 없이 유지하되 카드 폭을 보장한다.

#### 일정 상세도 toast-only다

각 날짜를 누르면 toast만 뜬다. 일정 detail 앱이라면 날짜 detail이 열려야 한다.

개선안:

- 날짜 클릭 시 해당 일자의 근무 상세 sheet를 연다.
- 환자 목록, 인수인계, 출근 기록, 교대자, 메모를 보여준다.

### 우선 수정

- 주 네비 버튼 hit area 48px화
- 날짜 detail sheet 추가
- 작은 화면 grid overflow 확인

---

## 7. 디자인 시스템 불일치 목록

### 7.1 공통 컴포넌트 미사용

문제:

- `tokens.css`는 쓰지만 system CSS는 쓰지 않는다.
- 화면마다 동일 컴포넌트가 반복 정의되어 유지보수가 어렵다.

개선:

- app shell, header, tabbar, SOS, card, sheet, toast를 공통화한다.

### 7.2 하드코딩 색상과 primitive token 직접 사용

문제:

- `#DCFCE7`, `#F4FAF6`, `#fff`, `rgba(34,197,94,...)` 등 직접 색상이 많다.
- `var(--brand-green-400)`, `var(--palette-red-700)`, `var(--palette-amber-700)` 같은 primitive token 직접 사용이 많다.

개선:

- 화면에서는 semantic token을 사용한다.
- caregiver 역할 색상은 한 곳에서만 alias로 관리한다.

### 7.3 아이콘 시스템 혼재

문제:

- fluent, ph, tabler, inline SVG가 섞여 있다.
- 프로젝트 규칙은 아이콘 필요 시 `iconify-icon` fluent 계열로 통일이다.

개선:

- `ph:sparkle-fill`, `ph:smiley-fill`, `tabler:pill-filled`, `fluent:emoji-24-filled`를 fluent 대체 아이콘으로 교체한다.
- 로고는 공통 asset/component로 분리한다.

### 7.4 터치 타깃 기준 미달

문제:

- 34px, 36px, 40px 버튼이 많다.
- 일부 CTA도 38px, 44px로 작다.

개선:

- 모든 interactive control의 실제 hit area를 48px 이상으로 맞춘다.

### 7.5 접근성 상태 부족

문제:

- tablist/segmented control에 selected 상태가 부족하다.
- switch에 role/aria 상태가 없다.
- 링크처럼 보이는 `a` 태그가 href 없이 onclick만 갖는 경우가 많다.

개선:

- 실제 이동은 `href`를 제공한다.
- 액션은 `button`으로 바꾼다.
- `aria-current`, `aria-selected`, `aria-checked`를 추가한다.

---

## 8. UX 위험도 기준 우선순위

### P0 - 먼저 고칠 것

- SOS를 전 화면에서 동일한 flow로 통일
- SOS 즉시 발신에 confirmation/cancel/log 추가
- 보호자 공유/간호사 보고/미확인 인수인계 처리에 confirmation 또는 detail sheet 추가
- 주요 alert와 이상감지 메시지가 toast-only로 끝나지 않게 수정
- README와 UI에서 이모지/이모지 용어 제거

### P1 - 사용성 개선

- 하단 탭 라벨 추가
- 모든 touch target 48px 이상 보장
- `c02` 기록 입력을 실제 input/keypad sheet로 개선
- 저장 후 progress, 완료 count, 동기화 상태 즉시 갱신
- 마이/일정의 toast-only 메뉴를 detail/disabled/준비중으로 분리

### P2 - 디자인 완성도

- 공통 CSS 추출
- hardcoded color, rgba, gradient 정리
- iconify fluent 계열로 아이콘 통일
- glass/gradient 과사용 줄이고 flat-first 방향으로 조정
- 작은 10px/11px 텍스트 축소 및 정보 위계 재정리

---

## 9. 브라우저로 추가 확인해야 할 항목

이번 리뷰는 파일 기준으로 충분히 유효하다. 다만 다음은 브라우저 모바일 viewport에서 확인해야 한다.

- 320px 폭에서 하단 tabbar와 SOS FAB가 겹치지 않는지
- `c02-checklist.html`의 full stepper, bottom sheet, tabbar가 서로 겹치지 않는지
- 긴 환자명, 긴 보호자 메시지, 긴 근무 시간이 줄바꿈될 때 카드가 깨지지 않는지
- `c04-schedule.html`의 주간 리스트 grid가 작은 화면에서 overflow되지 않는지
- 48px hit area가 실제 클릭 영역으로 확보되는지
- Noto Sans SC import가 한국어 화면에서 의도치 않은 폰트 인상을 만들지 않는지
- green 계열 배경이 실제 화면에서 너무 단조롭거나 흐릿하지 않은지

---

## 10. Claude에게 보낼 복붙 프롬프트

아래 내용을 그대로 Claude에게 보내면 된다.

```text
v11_요양보호사앱 전체를 UX/UI와 디자인 시스템 통일성 중심으로 개선해줘.

반드시 이 리뷰 파일을 먼저 읽어:
v11_요양보호사앱/CODEX_CAREGIVER_APP_UXUI_REVIEW_20260510.md

그리고 디자인 시스템 기준 파일도 같이 참고해:
07_디자인/tokens/tokens.css
07_디자인/system/app.css
07_디자인/system/components.css
v11_요양보호사앱/README.md

이번 작업 목표는 새 기능을 많이 추가하는 게 아니라, 기존 요양보호사 모바일앱을 더 통일감 있고, 깔끔하고, 실제 현장에서 한 손으로 쓰기 편한 앱처럼 다듬는 거야.

우선순위는 다음이야.

1. v11_요양보호사앱의 공통 CSS를 정리해줘. header, card, tabbar, SOS, toast, sheet, icon button, status badge 같은 반복 스타일을 공통화하고 각 HTML 내부에는 화면 고유 layout만 남겨줘.
2. 07_디자인의 design system v3.1 방향과 맞게 semantic token 중심으로 정리해줘. hardcoded hex, rgba, primitive token 직접 사용은 최대한 줄여줘.
3. README도 최신 규칙에 맞게 정리해줘. 이모지와 이모지라는 용어를 제거하고, 디자인 기준을 v9.5 보호자앱이 아니라 07_디자인 시스템 기준으로 바꿔줘.
4. 프로젝트 규칙상 UI와 문서에서 이모지는 절대 쓰지 말고, 아이콘은 iconify-icon fluent 계열로 통일해줘. ph, tabler, inline SVG 혼용도 정리해줘.
5. 현장 앱이므로 모든 주요 터치 타깃을 실제 48px 이상으로 맞춰줘. 특히 icon button, tab, SOS, switch, 주간 네비 버튼, 작은 CTA를 확인해줘.
6. 하단 탭은 아이콘만 있어서 인지성이 낮아. 전체 라벨 또는 active 탭 라벨을 추가해서 `오늘`, `기록`, `소통`, `마이`가 빠르게 구분되게 해줘.
7. SOS는 c01에서는 3초 롱프레스가 있지만 다른 화면에서는 toast-only에 가까워. 모든 화면에서 같은 SOS flow를 쓰게 하고, 즉시 발신에는 confirmation, cancel, 발신 로그를 추가해줘.
8. c01-today.html의 알림/관찰/SOS 흐름을 정리해줘. 알림은 소통 탭 detail로 연결하고, 관찰/주의/응급 단계의 색상과 문구를 분리해줘.
9. c02-checklist.html은 핵심 화면이지만 허브, 환자 상세, 빠른 기록, 스텝퍼, 음성 결과가 한 파일에 너무 복잡하게 섞여 있어. 사용자가 현재 어떤 상태에 있는지 header/back/tabbar/SOS 상태가 명확하게 보이도록 정리해줘.
10. c02의 혈압, 체온, 맥박, 혈당, 식사량 같은 기록 항목은 toast-only가 아니라 실제 input 또는 keypad sheet로 수정해줘. 저장 후에는 환자 row progress, 완료 count, 동기화 상태가 즉시 갱신되게 해줘.
11. c03-sotong.html의 인수인계 미확인 항목, 이상감지 메시지, 체위 변경 리마인더는 toast-only로 끝나면 안 돼. 클릭 시 detail sheet를 열고, 환자/시간/관찰 값/다음 행동/확인 CTA를 보여줘.
12. c03의 보호자 공유는 전송 전 preview/confirmation을 추가해줘. 공유 항목, 대상 보호자, 민감정보 제외 여부를 확인하고 전송하게 해줘.
13. c04-mypage.html과 c04-schedule.html의 toast-only 메뉴를 정리해줘. 실제 detail로 이동하거나, 아직 구현 전이면 준비중 badge 또는 disabled 상태로 명확히 보여줘.
14. c04-schedule.html의 주간 리스트는 작은 화면에서 overflow 가능성이 있어. 320px 모바일 폭에서도 시간/환자 아바타/chevron이 깨지지 않게 반응형으로 정리해줘.
15. switch, tablist, segmented control에 aria 상태를 추가해줘. href 없는 a 태그는 button으로 바꾸고, 실제 이동은 href를 명확히 넣어줘.
16. 최종적으로 모바일 viewport에서 tabbar, SOS FAB, bottom sheet, full stepper, 긴 텍스트가 겹치거나 잘리지 않는지 확인해줘.

중요:
- 기존 앱의 핵심 업무 흐름은 유지해.
- 새 디자인을 과하게 화려하게 만들지 말고, 요양보호사가 현장에서 빠르게 보고 정확하게 누를 수 있는 방향으로 정리해.
- v11_요양보호사앱 리뷰 파일은 하나로 유지하고, 새 리뷰 파일을 여러 개 만들지 마.
- 수정 후 어떤 파일을 바꿨는지와, 각 화면에서 무엇이 개선됐는지 요약해줘.
```

