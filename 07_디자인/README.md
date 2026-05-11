# 하루안부 디자인 시스템

**v3.2.3 | 2026.05.11**

이 문서 묶음은 하루안부 5개 앱(보호자/의료진/요양보호사/환자/온보딩)이 시각적으로 단일한 제품처럼 보이게 만드는 규칙이다. 모든 결정은 [tokens/tokens.css](tokens/tokens.css) 한 파일이 진실의 원천(SoT)이며, 이 문서들은 그 토큰을 어떻게 쓰는지 설명한다.

## 구조

### 문서 (읽기용)

| 문서 | 다루는 것 | 언제 보는가 |
|---|---|---|
| [01_FOUNDATIONS.md](01_FOUNDATIONS.md) | 브랜드·로고·컬러·타이포·간격·형태·고도·모션·아이콘·접근성·다국어 | 새 화면 만들 때 첫 참조 |
| [02_COMPONENTS.md](02_COMPONENTS.md) | 버튼·카드·탭바·헤더·모달·뱃지·인풋 등 모든 UI 컴포넌트 | 컴포넌트 구현 / 재사용 |
| [03_PATTERNS.md](03_PATTERNS.md) | 홈 화면·AI 리포트·경보 위계·빈 상태·폼 검증 등 화면 단위 패턴 | 새 페이지 IA 잡을 때 |
| [tokens/tokens.css](tokens/tokens.css) | 실제 CSS 변수 정의 (3계층 + 2축) | 화면 코드에서 import |
| [tokens/README.md](tokens/README.md) | 토큰 사용법 (data-role / data-platform) | 토큰 import 시 |
| [tokens/MIGRATION.md](tokens/MIGRATION.md) | 구 토큰 → 신 토큰 매핑 | v11_보호자앱 이전 작업 |

### 시각화 (브라우저로 보기)

| 페이지 | 보는 것 |
|---|---|
| [preview.html](preview.html) | 전체 시스템 진입점 + 4개 페이지 카드 + 핵심 원칙 5가지 |
| [preview-foundations.html](preview-foundations.html) | 로고·컬러 사다리·타이포·간격·라운드·그림자·모션·아이콘·접근성·다국어 |
| [preview-components.html](preview-components.html) | 모든 UI 컴포넌트 라이브 데모 (6 카테고리) |
| [preview-patterns.html](preview-patterns.html) | 보호자 홈·AI 리포트·의료진 대시보드·경보 위계 등 화면 단위 목업 |
| [preview-roles.html](preview-roles.html) | 같은 컴포넌트가 보호자·의료진·환자 테마에서 어떻게 다른지 비교 |

## 3 역할 테마 × 5 제품 표면

역할(role)과 제품(앱)을 분리해서 본다 — **3개의 색 테마**가 **5개의 제품 표면**에 매핑된다.

| 제품 표면 | 플랫폼 | 적용 역할(data-role) | 적용 테마 | 자동 상향 |
|---|---|---|---|---|
| **v11 보호자앱** | 모바일 PWA | `guardian` | 보호자 블루 (#2C7AFC) | 없음 |
| **v10 의료진웹** | 데스크톱 웹 | `medical` / `doctor` / `nurse` | 의료진 그린 (#22C55E) | 없음 (마우스 36px 터치) |
| **v11 요양보호사앱** | 모바일 PWA | `caregiver` | 의료진 그린 공유 | 없음 (현장 한 손 조작) |
| **v12 환자앱** | 모바일 PWA (태블릿 거치) | `patient` | 환자 오렌지 (#FB923C) | **본문 18px·터치 56px·행 64px** |
| **v13 온보딩** | 모바일 PWA | (역할 선택 전) | 기본 보호자 블루 | 없음 (선택 후 350ms fade로 전환) |

같은 그린 테마지만 의료진웹은 사이드바 + 톱바 시그니처(데스크톱 dense), 요양보호사앱은 플로팅 필 탭바 시그니처(현장 모바일)로 표면 형태가 다르다.

## 핵심 원칙 6가지

> 한 줄 철학: **조용한 기본값 + 필요한 순간의 강조.** 큰 색면·그라디언트·글래스·강한 그림자는 예외로만 쓴다.

1. **하나의 차체, 세 개의 액센트** — 보호자 블루(#2C7AFC) / 의료진 그린(#22C55E) / 환자 오렌지(#FB923C)는 **테마색이 아니라 액센트색**이다. 큰 배경·큰 카드 면은 모든 역할에서 중립색(흰색·캔버스 그레이)으로 통일하고, 역할색은 **버튼·활성 탭·작은 배지·포커스 링·보조선**에만 쓴다. 환자만 본문 18px·터치 56px 자동 상향.
2. **Flat이 기본, Glass는 예외** — 기본 카드는 단단한 흰색 surface + 1px 보더 + 약한 shadow. **Glass(반투명 + blur)는 플로팅 탭바·모달 오버레이·특수 강조 4종에만** 제한적으로. 정보 카드에 blur 기본 적용하지 않는다 — 텍스트 대비와 정보 밀도가 우선.
3. **그라디언트 절제** — 배경 그라디언트는 매우 약한 tint만. 강한 히어로 그라디언트는 **화면당 최대 1개**. FAB은 단색 또는 매우 은은한 2-stop. 일반 카드는 절대 그라디언트 사용 금지.
4. **카드 타입은 4종으로 고정** — `card-default` / `card-action` / `card-alert` / `card-hero`. 화면마다 다른 카드 스타일을 고를 필요가 없게 한다.
5. **모바일 시그니처 = 플로팅 필 탭바, 웹 시그니처 = 사이드바 + 톱바** — 탭바 배경은 **모든 역할에서 거의 동일한 흰색/반투명 흰색**. 활성 아이콘과 라벨만 역할색. 탭바를 역할별 tint로 칠하지 않는다.
6. **Pretendard + Fluent Filled 단일, 이모지 금지** — 모든 글자 Pretendard Variable (요양보호사 Noto Sans SC 폴백), 모든 아이콘 `fluent:*-filled`. AI 진입점은 sparkle 아닌 하루안부 심볼. UI/문서 어디서도 이모지 사용 안 함.

## 사용 시작 (5분)

새 화면을 만든다면:

```html
<!doctype html>
<html lang="ko" data-role="guardian" data-platform="mobile">
<head>
  <link rel="stylesheet" href="../07_디자인/tokens/tokens.css">
  <script src="https://cdn.jsdelivr.net/npm/iconify-icon@2.3.0/dist/iconify-icon.min.js"></script>
</head>
<body>
  <button class="btn-primary">확인</button>
</body>
</html>
```

`data-role` 값으로 `guardian` / `medical` / `doctor` / `nurse` / `caregiver` / `patient` 가능. `data-platform`은 `mobile` 또는 `web`.

## 변경 이력

- **v3.2.3 (2026.05.11)**: **다크 모드 봉인 — 라이트 단일 운영.** v9.5 시대 페이지들이 hex를 직접 사용해 다크 토큰과 충돌(글자 안 보임 / 사이드바·본문 명도 불일치)하는 문제로 봉인. `_app-theme.js`가 항상 `data-theme="light"` 강제, 다크 토글 위젯 제거, localStorage 자동 정리. tokens.css 다크 블록 코드는 보존(향후 모든 페이지가 토큰 기반이 되면 봉인 해제 검토).
- **v3.2 (2026.05.11)**: 외부 디자인 시스템 3사이트(KRDS·Fluent 2·KT Seamless Flow) 갭 분석 기반 15건 개선. 
  **신설:** AI 컴포넌트 카테고리(H1~H4), AI 패턴 5종(P3A~P3E), 차트 팔레트(--chart-1~8 + 의미 별칭, Okabe-Ito 색맹 안전), Side Panel(Non-modal B4), 알림 4채널 통합 매트릭스(P6), 의료진 웹 hover 상태(--state-*), 다중 에러 + 비동기 검증 패턴(P8.3~P8.4), 라이팅 액션 동사 매트릭스(§1.5), 컴포넌트 6종 추가(Section Tab/Stepper/Progress/Accordion/Tooltip/Pagination), 매직넘버 명도 사다리(--neutral-10~90 + strong), 스켈레톤 토큰(--skeleton-*), 일러스트 시스템(§15 라인 일러스트 vs 마스코트 분리), 저전력 폴백(@prefers-reduced-transparency + .no-blur), 환자앱 접근성 토글([data-a11y-text="large"] · [data-a11y-contrast="high"]).
  *(다크 모드 §13 도입은 v3.2.3에서 봉인됨 — 위 항목 참조.)*
- **v3.1 (2026.05.10)**: Flat-first 정책, --color-bg-glass OPTIONAL 격하, 탭바 배경 모든 역할 통일, 환자 그라디언트 약화, 의료진/요양보호사 surface density 차별화.
- **v3.0 (2026.05.09)**: 문서 IA를 M3·KRDS 패턴으로 재정렬. 흩어진 v2.0 문서 4개를 3개 파일로 통합. 로고 시스템·접근성·패턴 섹션 신설. 다국어(Noto Sans SC) 지원 추가. AI 진입점 = 하루안부 심볼로 일원화.
- **v2.0 (2026.04.18)**: 보호자 Primary `#2C7AFC` 확정, Fluent Filled 아이콘 단일화, 플로팅 필 탭바 정식 채택, tokens.css SoT 도입.
- **v1.0 (2026.04.17)**: 최초 디자인 시스템 가이드 작성.
