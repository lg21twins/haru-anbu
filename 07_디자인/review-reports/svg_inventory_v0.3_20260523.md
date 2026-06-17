# SVG 인벤토리 v0.3 — 분류 및 처리 이력

작성일: 2026-05-23
최종 상태: v0.4 시점에 전 영역 audit PASS — 본 문서는 **완료 기록 + 분류 참조**.
대상: audit v0.2가 위반으로 잡은 인라인 SVG 75건
방법: 파일/라인/viewBox/주변 클래스/주변 라벨로 용도 식별 → 3가지로 분류 → 처리

## 분류 기준

| 분류 | 의미 | 처리 |
|---|---|---|
| **iconify 전환** | 일반 UI 아이콘(메뉴, back, action 등) | `<iconify-icon icon="fluent:*">` 교체 |
| **SVG 유지** | 브랜드, 차트, ring, 시각화 | audit `BRAND_KEYWORDS`에 클래스 등록 → 자동 허용 |
| **검토 필요** | 아이콘인지 시각화인지 애매 | 디자이너 판단 필요 |

## 1. v10 의료진웹 (43건 — 가장 큰 영역)

### iconify 전환 (40건)

| 라인 | 종류 | viewBox | 추정 라벨 | fluent 매핑 |
|---|---|---|---|---|
| L3595 | `.nav-icon` | 20 20 | 홈 | `fluent:home-24-filled` |
| L3603 | `.nav-icon` | 20 20 | 환자 (people) | `fluent:people-24-filled` |
| L3612 | `.nav-icon` | 20 20 | 알림 (info circle) | `fluent:alert-24-filled` |
| L3621 | `.nav-icon` | 20 20 | 클립보드/기록 | `fluent:clipboard-text-24-filled` |
| L3630 | `.nav-icon` | 20 20 | 인박스/메일 | `fluent:mail-24-filled` |
| L3639 | `.nav-icon` | 20 20 | 캘린더 | `fluent:calendar-24-filled` |
| L3647 | `.nav-icon` | 20 20 | 폴더 | `fluent:folder-24-filled` |
| L3656 | `.nav-icon` | 20 20 | 프로필 | `fluent:person-24-filled` |
| L3685 | `.search-icon` | 20 20 | 검색 | `fluent:search-24-filled` |
| L3693 | (icon) | 20 20 | (미정) | `fluent:filter-24-filled` 가정 |
| L3700 | 12x12 | 20 20 | 작은 인디케이터 | `fluent:chevron-down-12-filled` |
| L4070, L4554, L5393, L5792, L5820, L6057 | 13x13 | 20 20 | chevron/arrow | `fluent:chevron-right-16-filled` |
| L4272, L4755, L5144, L5596, L6307 | 12x12 | 20 20 | small indicator | `fluent:chevron-down-12-filled` |
| L4995 | 13x13 | 20 20 | indicator | (라인별 추정) |
| L6520, L6530, L6540, L6550, L6567, L6577, L6587, L6604 | 16x16 ink-3 | 20 20 | meta icon | `fluent:more-vertical-16-filled` 등 |
| L6614 | 16x16 danger | 20 20 | warn icon | `fluent:warning-16-filled` |
| L6833, L6846, L6857, L6871 | menu icon | 20 20 | 메모 메뉴 | 메뉴 액션별 매핑 |

### SVG 유지 (3건)

| 라인 | viewBox | 종류 | 사유 |
|---|---|---|---|
| L4783, L4813, L4843, L4873, L4903, L4933, L4962 | 16 8 | mini sparkline indicator | 차트 패스 데이터 — fluent에 없음 |

→ 이 7건은 `chart-indicator` 또는 `spark-line` 클래스를 추가해 BRAND_KEYWORDS로 허용.

> v0.3 작업 노트: 실제 전환은 L3595–L3656 nav-icon 8건부터 시작. 나머지는 라벨 컨텍스트를 확인 후 진행. 한 번에 일괄 변경하면 sidebar/header 레이아웃이 어색해질 수 있어 단계적으로.

## 2. v11_보호자앱 (14건)

### iconify 전환 (12건)

대부분 `<svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor">` 패턴 — 화면별 단일 액션 아이콘(back/menu/info 등).

| 파일 | 라인 | 추정 용도 |
|---|---|---|
| g-guardian-live.html | L927 | 헤더 액션 |
| g02-ai-guide.html | L429 | 헤더 액션 |
| g02-ai-report.html | L531 | 헤더 액션 |
| g03-sotong.html | L465 | 헤더 액션 |
| g05-mypage.html | L424 | 헤더 액션 |
| g05-records.html | L474 | 헤더 액션 |
| g06-alert.html | L297 | 헤더 액션 |
| g08-billing.html | L310 | 헤더 액션 |
| g09-prescription.html | L266 | 헤더 액션 |
| g10-timeline.html | L287 | 헤더 액션 |
| g03-chat.html | L329, L338 | 채팅 컨트롤 |

→ fluent 매핑 후 일괄 교체. 22px width 유지.

### iconify 전환 가능 (2건, 채팅 family)

| 파일 | 라인 | 용도 |
|---|---|---|
| g03-chat-family.html | L376, L385 | 채팅 컨트롤 |

### SVG 유지 (1건)

| 파일 | 라인 | viewBox | 사유 |
|---|---|---|---|
| g02-ai-report.html | L374 | 84 84 | AI 점수 ring — viewBox 84 자동 허용 |

## 3. v11_요양보호사앱 (1건, 검사 정상화 후)

shift-ring 시각화 — `.shift-ring__svg` 클래스 추가로 audit 허용 처리 완료.

## 4. v15_의료진앱 (PASS, 분류 없음)

탭바 `.tab-svg` + d04 viewBox 44 44 모두 audit 허용 처리.

## 5. v12_환자앱 (PASS, 분류 없음)

p09-sos viewBox 140 140 자동 허용.

## 처리 결과 (v0.4 완료 시점)

| 단계 | 처리 | 결과 |
|---|---|---|
| 1 | audit 허용 (BRAND_KEYWORDS + 명시 viewBox) | mini sparkline 7건, 탭바 `.tab-svg`, SOS/AI ring, shift-ring 등 |
| 2 | v11_보호자앱 chat-bubble + 채팅 컨트롤 → fluent | 16건 마이그레이션 |
| 3 | v10 sidebar nav-icon 8건 → fluent (home/people/pill/clipboard/arrow-swap/calendar/folder/person) | 8건 |
| 4 | v10 반복 path 일괄 (plus, list, edit, search) | 11건 |
| 5 | v10 path 시그니처 매핑 (bell, info, chat, add-circle, …) | 6건 |
| 6 | v10 잔여 11건 개별 매핑 (question-circle, calendar, settings, weather-moon, arrow-upload, key, sign-out, send×3, dismiss) | 11건 |

**최종**: 75건 중 52건 iconify로 마이그레이션, 23건 BRAND_KEYWORDS/viewBox로 허용 처리. 전 영역 audit PASS.

## 정책: 새 SVG 작성 시 (계속 유효)

- 일반 아이콘은 항상 `<iconify-icon icon="fluent:*">`
- 차트/ring/시각화는 SVG 허용하되 클래스를 `*-ring`, `*-spark`, `*-chart`, `*-progress` 등으로 명명
- 새 시각화 SVG 추가 시 `BRAND_KEYWORDS`에 클래스 등록
