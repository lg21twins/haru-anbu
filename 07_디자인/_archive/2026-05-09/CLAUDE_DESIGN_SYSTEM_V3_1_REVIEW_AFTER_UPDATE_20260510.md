# 하루안부 디자인 시스템 v3.1 업데이트 후 재리뷰

작성일: 2026-05-10  
리뷰 관점: 이전 Codex 피드백 반영 여부, 디자인 통일감, 심미성, 디자인 시스템 적용 가능성

## 총평

이번 업데이트는 확실히 좋아졌습니다. 이전 피드백에서 지적했던 핵심 문제들이 상당 부분 반영됐고, 이제 디자인 시스템으로서의 설득력이 훨씬 올라갔습니다.

특히 홈 preview에 보호자, 의료진, 요양보호사, 환자 4개 역할이 모두 보이게 된 점이 좋습니다. 단순한 문서 목차가 아니라 “같은 구조를 역할별 맥락에 맞게 변형하는 제품 시스템”처럼 보이기 시작했습니다.

현재 상태는 큰 방향 전환이 필요한 단계가 아니라, 마감 정리 단계입니다. 디자인은 이미 충분히 깔끔하고 통일감이 있으며, 남은 문제는 semantic token 사용, 오래된 문구, 일부 preview 예시의 시스템 일관성입니다.

간단 평가:

- 통일감: 8.5/10
- 심미성: 8/10
- 디자인 시스템 신뢰도: 8/10
- 실제 앱 적용 가능성: 8/10

## 잘 반영된 점

### 1. 4-role 미니 앱 프리뷰가 추가되어 제품 구조가 선명해졌습니다

홈 preview에 보호자, 의료진, 요양보호사, 환자 카드가 모두 들어간 것은 좋은 수정입니다. 이전에는 요양보호사 맥락이 초반에 약했는데, 이제 네 역할이 모두 제품군 안에 있다는 점이 바로 보입니다.

또한 각 카드를 head, hero, row, caption의 동일한 4단 구조로 맞춘 점도 좋습니다. 이 덕분에 “같은 구조, 다른 맥락”이라는 메시지가 전보다 훨씬 잘 전달됩니다.

### 2. `data-role` 기반 구조로 정리된 점이 좋습니다

역할별 미니 카드가 `data-role` 기반으로 바뀌면서, 단순한 개별 일러스트가 아니라 시스템 변형처럼 보이기 시작했습니다. 이 방향은 맞습니다.

특히 보호자, 의료진, 요양보호사, 환자가 같은 카드 구조를 공유하고 색상, 문장 톤, 정보 밀도, 접근성 스케일만 달라지는 방식은 디자인 시스템의 핵심 원칙과 잘 맞습니다.

### 3. flat-first 원칙이 더 명확해졌습니다

tokens와 preview 문서에서 flat-first 정책이 더 명확해졌습니다. 일반 정보 카드는 흰 surface, 1px border, 약한 shadow를 기본으로 두고, glass는 탭바, 모달, AI 리포트, 가족 사진 카드처럼 제한된 맥락에서만 쓰는 방향이 잘 잡혔습니다.

roles preview에서도 기본 카드가 glass에서 flat으로 바뀐 점은 좋은 개선입니다. 이제 의료/돌봄 서비스에 맞는 안정감과 가독성이 더 잘 살아납니다.

### 4. 버전 표기가 정리됐습니다

`tokens.css`의 헤더가 v3.1로 정리된 점이 좋습니다. 디자인 시스템 문서에서는 이런 작은 버전 불일치도 신뢰도에 영향을 주기 때문에, 이번 수정은 의미가 있습니다.

### 5. SOS와 위험 색상이 semantic token 중심으로 정리됐습니다

이전에는 `#DC2626` 같은 hard-coded color가 눈에 띄었는데, 이번에는 `--color-danger` 중심으로 많이 정리됐습니다. 긴급 상황 색상은 역할과 무관하게 동일한 위험 신호로 유지하는 방향이 맞습니다.

## 아직 개선하면 좋은 점

### 1. role mini card 색상은 아직 primitive token을 직접 사용합니다

홈 role mini card 구조는 좋아졌지만, 내부 CSS에서는 아직 `--brand-blue-500`, `--brand-green-500`, `--brand-orange-400` 같은 primitive token을 직접 사용합니다.

디자인 시스템 원칙상 화면 코드는 primitive token보다 semantic token을 보는 편이 좋습니다. 특히 문서에서 “화면 코드는 token만 본다”, “역할은 `data-role`이 조정한다”고 말하고 있기 때문에, role mini card도 그 원칙을 더 엄격히 따라가면 좋겠습니다.

개선 제안:

- dot, icon color: `--color-accent`
- hero gradient: `--color-accent`, `--color-accent-strong` 또는 전용 semantic token
- shadow/tint: `rgba(var(--color-accent-rgb), 0.25)`
- success/warning pill: 현재처럼 상태 semantic token 유지

이렇게 바꾸면 role mini card가 “예쁜 예시”가 아니라 실제 앱 구현 기준처럼 보입니다.

### 2. 일부 문구가 이전 버전의 glass 개념을 아직 끌고 갑니다

roles preview의 카드 비교 섹션 제목이 아직 “같은 글래스 카드”로 남아 있습니다. 실제 구현은 flat-first로 바뀌었기 때문에 문구와 화면이 충돌합니다.

개선 제안:

- “같은 글래스 카드” → “같은 정보 카드 — 액센트만 다름”
- 또는 “같은 flat card — 역할별 액센트만 다름”

이런 문구 정리는 작아 보이지만, 디자인 시스템의 철학을 일관되게 만드는 데 중요합니다.

### 3. role row의 desktop grid는 조금 더 유연하게 만들 수 있습니다

role 설명 row는 모바일 대응이 추가되어 이전보다 좋아졌습니다. 다만 desktop 기본값은 아직 `24px 200px 1fr`처럼 고정 column을 사용합니다.

현재로도 크게 문제는 아니지만, 긴 역할명이나 다국어 텍스트가 들어갔을 때 더 안정적으로 보이려면 `minmax()`를 쓰는 편이 좋습니다.

개선 제안:

```css
.role-row {
  grid-template-columns: 24px minmax(160px, 220px) minmax(0, 1fr);
}
```

이렇게 하면 데스크톱에서도 고정폭 느낌은 유지하면서, 텍스트가 길어질 때 더 안정적으로 반응합니다.

### 4. patterns preview의 FAB/hero 쪽은 아직 primitive color와 rgba shadow가 많습니다

patterns 문서의 FAB, hero, active tab 예시는 아직 `--brand-blue-500`, `--brand-green-500`, `--brand-orange-400`와 직접 rgba shadow를 많이 사용합니다.

문서용 예시라서 당장 치명적이지는 않지만, 디자인 시스템 문서 자체가 구현 기준이라면 semantic token으로 통일하는 편이 좋습니다.

개선 제안:

- role별 active color: `--color-accent`
- role별 strong color: `--color-accent-strong`
- role별 shadow: `rgba(var(--color-accent-rgb), 0.25)`
- role별 hero gradient: `linear-gradient(135deg, var(--color-accent), var(--color-accent-strong))`

이렇게 하면 preview 문서와 tokens 철학이 더 강하게 맞물립니다.

### 5. hero 설명의 “세 개의 테마, 다섯 개의 제품 표면”은 조금 더 명확히 설명하면 좋습니다

홈 hero에서 “세 개의 테마, 다섯 개의 제품 표면”이라고 설명합니다. 방향은 좋지만, 처음 보는 사람에게는 “4개 역할인데 왜 3개 테마인가”, “5개 제품 표면은 무엇인가”가 잠깐 헷갈릴 수 있습니다.

개선 제안:

- 3개 테마: 보호자 blue, 의료진/요양보호사 green, 환자 orange
- 5개 제품 표면: 보호자앱, 의료진웹, 의료진앱, 요양보호사앱, 환자앱 또는 온보딩 포함 여부 명확화

현재 문구도 나쁘지는 않지만, 디자인 시스템 문서 첫 화면에서는 구조가 한 번에 이해되는 것이 중요합니다.

## 우선순위 액션

### P0: 바로 고치면 좋은 마감

1. roles preview의 “같은 글래스 카드” 문구를 flat-first 철학에 맞게 수정
2. 홈 role mini card의 dot/icon/hero 색상을 primitive token에서 semantic token으로 교체
3. patterns preview의 FAB/hero shadow를 `--color-accent-rgb` 기반으로 정리

### P1: 시스템 일관성 강화

1. role row desktop grid를 `minmax()` 기반으로 개선
2. hero 설명에서 “3개 테마 / 5개 제품 표면”의 의미를 더 명확히 설명
3. preview, roles, patterns에서 role accent 사용 방식을 동일한 CSS 패턴으로 정렬

### P2: 완성도 향상

1. 모든 preview 예시에서 primitive token 직접 사용 여부 점검
2. 실제 앱 코드에 복사 가능한 semantic token 예시를 components 문서에 추가
3. glass 사용 가능 범위를 components, patterns, roles 문서에서 동일한 문장으로 반복

## 최종 의견

이번 업데이트는 이전 피드백을 잘 반영했습니다. 특히 4-role preview 추가, `data-role` 기반 구조 정리, flat-first 원칙 강화는 모두 좋은 방향입니다.

지금 디자인은 충분히 깔끔하고 보기 좋습니다. 통일감도 전보다 훨씬 좋아졌습니다. 남은 작업은 큰 디자인 변경이 아니라, 디자인 시스템답게 token 사용과 문구를 끝까지 정리하는 것입니다.

한 줄로 정리하면:

현재 v3.1은 시각적으로는 거의 설득됐고, 이제 semantic token과 문서 문구만 끝까지 맞추면 실제 앱 전체에 적용해도 좋은 디자인 시스템이 됩니다.
