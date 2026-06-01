# 요양보호사 앱 · 외부 레퍼런스 GAP 분석

작성일: 2026-05-13
대상: `v11_요양보호사앱` (c01~c04 + c04-schedule)
보완 문서: `CODEX_CAREGIVER_APP_IMPROVEMENT_AUDIT_20260513.md` (내부 일관성)
이 문서: **외부 헬스케어/케어기버/로스터 앱 패턴과의 GAP**

> Mobbin MCP가 연결되지 않아 직접 스크린샷 비교는 불가. 대신 `ui-ux-pro-max` 검색 엔진의 product/style/color/ux 도메인에서 추출한 **검증된 패턴 카탈로그**와, 업계에서 잘 알려진 대표 앱 분석을 결합했습니다.

---

## 0. 외부 레퍼런스 매핑

| 화면 | 우리 화면 아키타입 | 대표 외부 레퍼런스 | 적용 가능한 패턴 |
|---|---|---|---|
| c01-today | Healthcare Home + Now/Next | **Medisafe**, **CareLinx**, **Honor** | 큰 원형 ring + Next-up timeline + 단일 CTA |
| c02-checklist | Medication/Care log | **Medisafe**, **MyChart**, **PointClickCare** | 1-task-per-screen stepper, swipe-to-complete |
| c03-sotong | Triaged Inbox | **Slack**, **Linear Inbox**, **WhatsApp Business** | Priority leading edge bar, swipe actions, mute |
| c04-mypage | Worker Profile | **Strava Profile**, **Apple Health** | Profile + Today Stats + Quick Actions 3분할 |
| c04-schedule | Shift/Roster | **When I Work**, **7shifts**, **Sling** | Day chip row + muted off-day, color-band shift type |

---

## 1. c01-today (홈) ← Healthcare Home 아키타입

**우리 현재**
- 헤더(로고) → 근무 스트립(slim 44px ring) → 히어로(지금 박영자) → AI 인수인계 → 관찰 카드 → 담당 로스터
- CTA: `지금 기록 시작` (단일)

**외부 레퍼런스 (Medisafe / CareLinx)**
- **큰 원형 진행 ring** (90~120px, 화면 정 중앙 상단) — 한눈에 "오늘 진척률"
- Next-up은 **타임라인**(현재 시각 + 다음 3건 vertical list)으로 함께 표시
- 단일 hero CTA는 우리와 동일 ✓

**GAP**

| 항목 | 우리 | 외부 표준 | 영향 |
|---|---|---|---|
| 진척 시각화 | 44px ring + 텍스트 "3/8 완료" | 90~120px ring + 중앙 큰 숫자 | 한눈에 진척률 인지 ↓ |
| Next-up 컨텍스트 | hero에 "다음까지 46분"만 | 미니 타임라인 3-4건 | "지금 외 그 다음 무엇" 모름 |
| 색상 톤 | 그린 단일 + amber 경고 | 그린(완료)/블루(예정)/앰버(주의) 3톤 | 시각 우선순위 약함 |

**개선 권고 (P1)**
- 근무 스트립을 확대해 ring을 88px로 키우고, 중앙에 `3/8` 표기 → 진척 가시성 향상
- hero 아래에 **미니 next-up 리스트** 추가 (`11:00 김영자 식사보조` / `11:30 이순자 혈압` 2~3건)
- 카드 hierarchy 토큰: `card / card--priority / card--ambient` 3단으로 재정렬

**참고 표준 색상** (ui-ux-pro-max: Medication & Pill Reminder)
```
trust blue + missed alert red + taken green + clean white
```
우리는 그린 단일이라 **"예정"과 "주의"가 시각적으로 구분되지 않음**.

---

## 2. c02-checklist (케어 기록) ← Medication Log 아키타입

**우리 현재**
- 환자별/시간순 탭 → 현재 환자 카드 → 빠른 기록 6 grid → 환자 상세 stepper (8 step)
- "5초 저장" 카피 ✓ — 외부 표준에 부합

**외부 레퍼런스 (Medisafe / PointClickCare)**
- **첫 화면은 가장 임박한 1건만 ALL-CAPS hero**로 (예: `NOW · 박영자 혈압`)
- 나머지는 collapsed 리스트 — 펼치면 stepper
- **swipe-right = 완료 / swipe-left = 보류** 제스처가 표준

**GAP**

| 항목 | 우리 | 외부 표준 | 영향 |
|---|---|---|---|
| 첫 화면 밀도 | 환자 카드 + 빠른 기록 6 + 환자별 토글 | 1 hero task + collapsed list | 인지 부하 ↑ |
| 제스처 | 탭만 | swipe(완료/보류) | 한 손 조작 ↓ |
| 진행률 표시 | 환자 카드 내 텍스트 | 상단 sticky progress bar | 진척 모름 |
| 빠른 기록 grid | 2x4 grid (8개) | 1xN horizontal scroll | 화면 밀도 분산 |

**개선 권고 (P1)**
- 빠른 기록 grid는 **horizontal scroll snap**으로 전환 (Slack/Linear inbox quick-action 패턴)
- stepper 진입 후 상단 **sticky progress bar** (`Step 3 / 8` + 16px line)
- 환자 카드에 swipe-right 제스처 추가 (`HaruCG.bindSwipe()` 생성 권장)

---

## 3. c03-sotong (소통) ← Triaged Inbox 아키타입

**우리 현재**
- 인수인계 확인 카드 → 보호자 공유 카드 → 메시지 리스트 (읽지 않음/오늘/이전)
- 우선순위는 `tg-crit / tg-nurse / tg-guard / tg-ai` **얇은 칩**으로만 표시

**외부 레퍼런스 (Slack / Linear Inbox / WhatsApp Business)**
- **4~6px 두께의 좌측 컬러 leading edge** — 메시지 종류를 한눈에
- **읽지 않음은 좌측 dot 4px + 굵은 텍스트** — 이중 표식
- **swipe-left = archive / swipe-right = mute** 제스처
- **그룹 구분선**은 24px 큰 여백 + 13px 라벨 (`긴급` / `오늘`)

**GAP**

| 항목 | 우리 | 외부 표준 | 영향 |
|---|---|---|---|
| 우선순위 visual | 얇은 색칩 (12px) | 좌측 4px 컬러 bar | 스캐닝 시 종류 구분 ↓ |
| 읽음 상태 | bold + dot 8px | bold + 좌측 4px dot + 미세 배경 틴트 | 약함 |
| 제스처 | 탭만 | swipe archive/mute | 인박스 위생 도구 부재 |
| 그룹 헤더 | 14px 라벨 | 13px tracking +.5 small caps + 큰 여백 | 그룹 인지 ↓ |
| 보호자 공유 카드 | 첫 화면 중앙 | 메시지 컨텍스트 안에서만 (or FAB) | 정보 목적 혼합 |

**개선 권고 (P1) ★ 가장 빠른 효과**
- `.msg`에 `border-left: 4px solid var(--prio-color)` 추가 + 좌측 padding 4px 보정
- prio-color 매핑: `crit→red 600`, `nurse→indigo 500`, `guard→amber 600`, `ai→accent`
- "오늘 보호자에게 공유" 카드는 **메시지 리스트 끝**으로 이동 또는 FAB로 격하 (Codex 감사 §6.3과 일치)

---

## 4. c04-mypage (마이) ← Worker Profile 아키타입

**우리 현재**
- 프로필 카드 → 오늘 근무 카드 → 일정 진입 → 의무 진척도 → 서비스 기록/알림 설정/자격/앱 설정...

**외부 레퍼런스 (Strava Profile / Apple Health)**
- 첫 화면은 **3 section만**: Profile + Today's Stats + 3-4 Quick Actions
- 설정은 **별도 화면**(우상단 톱니바퀴) — Apple Health 처럼 분리
- 자격/교육은 **Tab 전환** 또는 `자격 관리` 진입점 1개

**GAP**

| 항목 | 우리 | 외부 표준 | 영향 |
|---|---|---|---|
| 첫 화면 길이 | 9 sections | 3 sections + 설정 진입 | 스크롤 피로 ↑ |
| 마이 vs 설정 | 한 화면 혼합 | 명확히 분리 | IA 약함 |
| Quick Actions | 메뉴 리스트 4-6 stacked | 3-4 chip grid (icon+label) | 시각 밀도 ↓ |

**개선 권고 (P0) ★ Codex 감사와 중첩**
- 첫 화면: 프로필 + 오늘 근무 + 이번 주 일정 진입 + 이달 의무 진척도 + **3-4개 quick chip** (자격 / 출퇴근 / 급여 / 고객센터)
- 알림/언어/앱설정 → `c04-settings.html` 별도 push (우상단 톱니바퀴)

---

## 5. c04-schedule (일정) ← Shift Roster 아키타입

**우리 현재**
- 주 네비게이션 + 요약 chip(주간/야간/휴무) → 7일 리스트 (date · shift chip · time · 환자 아바타 · chevron)
- 휴무는 dashed border chip + `—` em-dash

**외부 레퍼런스 (When I Work / 7shifts / Sling)**
- 근무일은 **좌측 4px 컬러 bar** (주간=그린 / 야간=인디고)
- **휴무는 60% opacity + 더 얕은 row** (시각적 후퇴) — 우리는 이미 muted지만 색 톤이 강함
- 오늘은 **배경 틴트** + `오늘` pill (우리 `sd-now` 패턴과 일치 ✓)
- "PDF 공유"는 **roster export**로 명명 (`근무표 공유`)

**GAP**

| 항목 | 우리 | 외부 표준 | 영향 |
|---|---|---|---|
| Shift 타입 시각화 | 우측 chip(주간/야간) | 좌측 4px 컬러 bar + chip | 한눈에 패턴 인지 ↓ |
| 휴무 row | 같은 높이 (56px) + dashed chip | 같은 높이지만 60% opacity, hairline 분리 | "일하는 날" 인식 약함 |
| 공유 버튼 | "공유" (모호) | "근무표 공유" / "PDF로 내보내기" | CTA 약함 (Codex §6.5와 일치) |

**개선 권고 (P2)**
- `.sch-day`에 `border-left: 3px solid` 추가 (주간=accent / 야간=indigo / 휴무=transparent)
- 휴무 row는 `opacity: 0.72` + 텍스트만 표시 (chevron 유지) — 시각적 후퇴
- 공유 버튼 aria-label/toast 카피 → `근무표 공유`

---

## 6. 가장 빠르게 적용 가능한 개선 TOP 3 (즉시 코드)

외부 레퍼런스 GAP 기반, **단일 파일·CSS only·30분 이내** 작업:

1. **c03-sotong 메시지 좌측 priority bar** (외부 inbox 표준)
   - `.msg`에 `border-left: 4px solid` 추가
   - 우선순위별 컬러 토큰 정의
   - 스캐닝 속도 즉시 향상

2. **c04-schedule 휴무 row 시각 후퇴** (외부 roster 표준)
   - `.sch-day:has(.sd-chip.off) { opacity: .72; }`
   - 근무일에는 좌측 3px 컬러 bar 추가

3. **c01-today 진척 ring 확대** (Medisafe 표준)
   - `.shift-ring` 44px → 64px, 중앙 숫자 16px
   - 근무 스트립 padding 12→16, height auto

---

## 7. 외부 표준 색상 토큰 권고 (앱 전체 공통)

ui-ux-pro-max "Medication & Pill Reminder" 팔레트 기반으로, 우리 그린 단톤을 보완:

```css
--prio-crit:    #DC2626;  /* 긴급/이상감지 — red 600 */
--prio-nurse:   #4F46E5;  /* 의료진 — indigo 600 */
--prio-guard:   #D97706;  /* 보호자 — amber 600 */
--prio-ai:      var(--color-accent);  /* AI — 우리 그린 */
--prio-off:     #9CA3AF;  /* 휴무/비활성 — slate 400 */
```

**원칙**: 색은 컨텍스트만 부여, 인터랙션 색은 그린 단일 유지.

---

## 8. 적용 우선순위 (Codex 감사 + 본 문서 통합)

| 우선순위 | 출처 | 작업 |
|---|---|---|
| P0 | Codex §2.1 | 탭바 겹침 (c02·c03 하단 padding) |
| P0 | Codex §4.2 | SOS 단일화 |
| P0 | Codex §5.1 | `fluent:emoji-*` 교체 |
| **P0-ext** | **본 문서 §6.1** | **c03 메시지 우선순위 left bar** |
| P1 | Codex §3.1 | 헤더 규칙 통일 |
| **P1-ext** | **본 문서 §6.2** | **c04-schedule 휴무 후퇴 + shift bar** |
| **P1-ext** | **본 문서 §6.3** | **c01 ring 확대** |
| P2 | Codex §6.4 | 마이/설정 분리 |
| **P2-ext** | **본 문서 §3** | **c03 swipe archive/mute** (JS 신규) |
| **P2-ext** | **본 문서 §2** | **c02 빠른기록 horizontal scroll** |

---

## 9. 한계 및 후속 작업

- **Mobbin MCP 미연결**: 본 문서는 ui-ux-pro-max DB의 검증된 패턴 카탈로그 기반. 실제 Mobbin 스크린샷 비교는 사용자가 직접 링크 제공 시 추가 가능.
- **Figma MCP 미인증**: 디자인 파일이 있다면 인증 후 토큰 직접 동기화 가능.
- **다음 단계 제안**: 본 문서 §6의 TOP 3 즉시 적용 → 결과 스크린샷 확인 → §6.7 색상 토큰을 `caregiver.css`로 회수.
