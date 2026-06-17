# 하루안부 디자인 시스템 v3.1 피드백

작성일: 2026-05-10  
리뷰 관점: 웹사이트 소개 페이지보다, 실제 앱 전체에 적용될 디자인 시스템의 통일감, 심미성, 적용 가능성 중심

## 총평

이번 v3.1 업데이트는 방향이 좋습니다. 이전보다 훨씬 차분하고 깔끔해졌고, flat-first 원칙도 의료/돌봄 서비스에 잘 맞습니다. 특히 홈 preview에 보호자, 의료진, 환자 미니 앱 프리뷰가 들어가면서 “이 디자인 시스템이 실제 앱에서 어떻게 보이는지”가 전보다 훨씬 명확해졌습니다.

현재 상태는 예쁜 문서형 preview에서 실제 제품 시스템으로 넘어가는 중간 단계로 보입니다. 시각적 인상은 충분히 좋아졌지만, 아직 일부 예시가 inline style, primitive color token, glass 카드에 기대고 있어서 “같은 규칙으로 모든 앱을 묶는다”는 설득력은 조금 더 다듬을 필요가 있습니다.

간단 평가:

- 통일감: 8/10
- 심미성: 8/10
- 디자인 시스템 신뢰도: 7/10
- 실제 앱 적용 가능성: 8/10

## 좋아진 점

### 1. 첫인상이 훨씬 제품 중심으로 바뀌었습니다

`preview.html`의 홈 화면에 역할별 미니 앱 프리뷰가 들어간 것은 좋은 개선입니다. 단순히 문서 목차를 보여주는 느낌에서 벗어나, 하루안부가 보호자, 의료진, 환자 경험을 하나의 시스템으로 묶고 있다는 점이 바로 보입니다.

이 변화 덕분에 디자인 시스템의 목적이 더 선명해졌습니다. “예쁜 가이드 문서”가 아니라 “여러 사용자 앱을 통합하기 위한 기준”처럼 느껴집니다.

### 2. flat-first 방향이 서비스 성격과 잘 맞습니다

의료, 돌봄, 가족 안심 서비스에서는 과한 glassmorphism보다 안정적이고 읽기 쉬운 flat surface가 더 적합합니다. v3.1에서 card-default, card-action, card-alert, card-hero처럼 카드 역할을 명확히 나눈 점은 좋습니다.

특히 일반 정보 카드는 flat하게 두고, glass는 AI 리포트나 사진 위 오버레이처럼 특정 상황에만 쓰는 방향이 맞습니다.

### 3. 색상 톤이 전보다 차분하고 신뢰감 있습니다

보호자 blue, 의료진/요양보호사 green, 환자 orange 계열은 역할 구분이 직관적입니다. 전체 색감도 지나치게 화려하지 않고, 헬스케어 제품에 필요한 안정감이 있습니다.

## 개선하면 좋은 점

### 1. 역할별 미니 앱 프리뷰가 아직 “시스템”보다 “개별 일러스트”처럼 보입니다

현재 홈의 역할별 미니 프리뷰는 시각적으로는 좋지만, 코드와 구조 관점에서는 inline style과 primitive token에 많이 의존합니다.

개선 제안:

- `data-role="guardian"`, `data-role="medical"`, `data-role="patient"` 기반으로 역할 색상과 강조 스타일을 제어
- 예시 화면 안에서는 `--brand-blue-500` 같은 primitive token보다 `--color-accent`, `--role-accent`, `--color-danger` 같은 semantic token 사용
- 카드 내부 구조는 최대한 동일하게 유지하고, 역할별 차이는 색상, 밀도, 타이포 크기, 상태 표현 정도로 제한

이렇게 하면 “같은 구조, 다른 맥락”이라는 메시지가 더 강해집니다.

### 2. 홈에서 요양보호사 맥락이 약합니다

문서에서는 보호자, 의료진, 요양보호사, 환자 앱 전체를 포괄한다고 보이지만, 홈 미니 프리뷰는 보호자, 의료진, 환자 중심입니다. 요양보호사가 의료진 green theme에 포함되는 것인지, 별도 경험으로 다루는 것인지 초반에는 조금 불명확합니다.

개선 제안:

- 홈 미니 프리뷰에 요양보호사 카드를 별도로 추가
- 또는 의료진 카드 제목을 “의료진/요양보호사”로 명확히 하고, 같은 green theme 안에서도 밀도와 업무 흐름이 어떻게 달라지는지 role page에서 보여주기

사용자 역할이 제품의 핵심이면, 첫 화면에서도 그 역할 구분이 바로 드러나는 편이 좋습니다.

### 3. “같은 구조”라는 메시지에 비해 카드 내부 레이아웃 차이가 큽니다

홈 미니 프리뷰의 세 역할 카드가 모두 보기 좋지만, 내부 구조가 완전히 같은 컴포넌트 변형처럼 보이지는 않습니다. 지금은 각 역할별로 별도 디자인을 만든 느낌이 조금 있습니다.

개선 제안:

- 세 카드 모두 동일한 내부 순서 사용: role label, status hero, 핵심 row, action/nav
- hero 영역 높이, badge 위치, row spacing을 통일
- 차이는 색상, 아이콘, 문장 톤, 정보 밀도에서만 표현

이렇게 하면 디자인 통일성이 더 강해지고, 실제 앱 확장성도 좋아집니다.

### 4. Roles preview 쪽은 아직 glass 기본 느낌이 남아 있습니다

components 문서에서는 flat-first 원칙이 잘 정리되어 있지만, roles preview 일부에서는 `.demo-card`와 `.mini-c`가 glass 배경을 기본처럼 사용합니다. 이러면 문서마다 카드 철학이 조금 다르게 느껴질 수 있습니다.

개선 제안:

- role demo의 기본 정보 카드는 flat surface로 변경
- glass는 AI 요약, 사진 위 오버레이, hero성 강조 영역 등 예외 상황에만 사용
- roles page에도 “flat default, glass selective” 원칙을 명시적으로 반영

디자인 시스템은 예외보다 기본값이 더 중요합니다. 기본 카드가 어디서나 같은 인상을 주는 것이 좋습니다.

### 5. semantic token 사용을 더 엄격히 하면 좋겠습니다

현재 일부 예시에서 hard-coded color나 primitive brand token이 직접 쓰입니다. 문서용 color swatch에서는 괜찮지만, 실제 앱 UI 예시에서는 semantic token을 쓰는 편이 시스템 신뢰도가 높습니다.

개선 제안:

- 위험/긴급: `#DC2626` 직접 사용 대신 `--color-danger`
- 역할 강조: `--brand-blue-500` 직접 사용 대신 `--role-accent` 또는 `--color-accent`
- 배경 gradient: 역할별 primitive 조합 대신 `--role-gradient-soft` 같은 semantic token

디자인 시스템 문서에서 예시 코드가 token 사용 원칙을 직접 보여줘야, 이후 앱 구현도 흔들리지 않습니다.

### 6. 일부 오래된 용어가 남아 있습니다

patterns 쪽에 `card-emphasis` 같은 이전 체계의 표현이 남아 있습니다. components 문서에서는 card 종류가 v3.1 기준으로 정리되어 있으므로, 오래된 이름은 제거하는 편이 좋습니다.

개선 제안:

- `card-emphasis`를 제거
- 맥락에 따라 `card-action`, `card-alert`, `card-hero` 중 하나로 교체
- preview, components, patterns, roles 문서의 카드 명칭을 한 번에 정렬

작은 용어 차이지만, 디자인 시스템에서는 이런 부분이 신뢰도에 영향을 줍니다.

### 7. 버전 표기를 맞춰야 합니다

preview는 v3.1로 보이지만, tokens 파일 헤더에는 v3.0 표기가 남아 있습니다. 실제 규칙은 v3.1로 업데이트되어 있어도, 버전 표기가 다르면 문서 관리가 덜 정리된 느낌을 줍니다.

개선 제안:

- `tokens.css` 헤더를 v3.1로 업데이트
- v3.1 변경 사항을 짧게 주석으로 남기기
- preview 문서와 token 문서의 버전 표기 통일

### 8. 모바일에서 role 설명 row가 깨질 가능성이 있습니다

roles page의 role 설명 row는 fixed column 구조처럼 보입니다. 작은 화면에서는 역할명, 컬러명, 설명이 좁게 눌릴 가능성이 있습니다.

개선 제안:

- role row를 class 기반 grid로 정리
- desktop: icon, role name, description 3열
- mobile: icon + role name 상단, description 하단 stack
- inline grid style 제거

모바일에서 깨지는 문서 예시는 실제 앱의 반응형 신뢰도까지 낮춰 보일 수 있습니다.

## 우선순위 액션

### P0: 바로 고치면 좋은 것

1. `tokens.css` 버전 표기 v3.1로 통일
2. `card-emphasis` 등 오래된 카드 명칭 제거
3. SOS, danger, role accent 예시의 hard-coded color를 semantic token으로 교체
4. roles page의 기본 glass card를 flat-first 원칙에 맞게 수정

### P1: 디자인 완성도를 올리는 것

1. 홈 role mini card를 동일한 내부 구조로 재정렬
2. `data-role` 기반 role styling으로 inline style 줄이기
3. 요양보호사 맥락을 홈 또는 roles page에서 더 명확히 노출
4. role row 모바일 레이아웃 개선

### P2: 시스템 신뢰도를 높이는 것

1. preview, foundations, components, patterns, roles 전체에서 token 사용 규칙 통일
2. glass 사용 가능 범위를 pattern 문서와 component 예시에서 동일하게 설명
3. 실제 앱 화면 예시는 primitive token이 아니라 semantic token만 사용하도록 정리

## 최종 의견

이번 업데이트는 확실히 좋아졌습니다. 디자인이 전보다 덜 장식적이고, 더 신뢰감 있으며, 하루안부 서비스의 의료/돌봄 맥락에 잘 맞습니다. 지금 필요한 것은 큰 방향 전환이 아니라 정리입니다.

핵심은 하나입니다.

현재 preview는 이미 보기 좋습니다. 다음 단계는 이 보기 좋은 예시들이 모두 같은 token, 같은 component 구조, 같은 역할별 규칙으로 만들어졌다는 것을 코드와 문서에서 증명하는 것입니다.

그 정리만 되면 하루안부 디자인 시스템은 충분히 깔끔하고 통일감 있는 기준으로 사용할 수 있습니다.
