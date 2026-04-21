# 하루안부 — 세션 핸드오프

> 마지막 업데이트: 2026-04-17

---

## 1. 프로젝트 목표와 배경

하루안부(Haru Anbu)는 요양시설에 계신 어르신의 보호자를 위한 한국어 케어 플랫폼 앱이다. 보호자가 입소자의 건강 상태, 투약, 식사, 활동 등을 실시간으로 확인하고, 간호사·AI·가족과 소통할 수 있는 모바일 웹앱 프로토타입이다.

현재 작업 중인 버전은 `v9_보호자앱` (보호자 앱 v9)이며, 각 페이지가 독립적인 단일 HTML 파일로 구성되어 있다. 외부 CSS 파일 없이 인라인 스타일로 동작하도록 전환 완료.

---

## 2. 합의된 디자인 시스템 / 결정 사항

### 디자인 토큰

```css
:root {
  --blue: #2C7AFC;
  --blue-l: #5B9BFF;
  --blue-d: #1D6AF2;
  --green: #34D399;
  --green-d: #059669;
  --amber: #F59E0B;
  --red: #EF4444;
  --t1: #111827;
  --t2: rgba(0,0,0,.5);
  --t3: rgba(0,0,0,.35);            /* WCAG 대비 개선: 기존 .25 → .35 */
  --surface: rgba(255,255,255,.88);  /* 글라스 카드 투명도: 기존 .92 → .88 */
  --font: 'Pretendard Variable', 'Pretendard', -apple-system, system-ui, sans-serif;
}
```

### 글라스모피즘 UI 규칙

- 카드 배경: `rgba(255,255,255,.88)` + `backdrop-filter: blur(20px)`
- 모서리: `border-radius: 16–20px`
- 그림자: `0 4px 16px rgba(0,0,0,.1)`
- 모바일 전용: `max-width: 430px`
- Safe area 대응: `env(safe-area-inset-bottom)` 적용

### 표준 네비게이션 바

모든 메인/서브 페이지에 동일한 floating pill-style 탭바를 사용한다.

**구조:**

```html
<div class="bottom-bar">
  <nav class="tabbar">
    <a href="g-guardian-live.html" class="tab {active?}"><!-- 탭1: 집(홈) 아이콘 --></a>
    <a href="g02-ai-guide.html" class="tab {active?}"><!-- 탭2: 방패체크(shield-checkmark) 아이콘 --></a>
    <a href="g03-sotong.html" class="tab {active?}"><!-- 탭3: 말풍선 아이콘 --></a>
    <a href="g05-records.html" class="tab {active?}"><!-- 탭4: 리스트 아이콘 --></a>
    <a href="g05-mypage-B.html" class="tab {active?}"><!-- 탭5: 사람 아이콘 --></a>
  </nav>
  <a href="g03-chat-ai.html" class="ai-fab"><!-- AI FAB 버튼 --></a>
</div>
```

**탭바 CSS (글라스 블러):**

```css
.bottom-bar { position:fixed; bottom:calc(max(env(safe-area-inset-bottom,0px),20px) + 12px); left:50%; transform:translateX(-50%); display:flex; align-items:center; gap:10px; z-index:40; width:calc(100% - 48px); max-width:370px }
.tabbar { flex:1; min-width:0; height:56px; background:rgba(210,225,250,.55); backdrop-filter:blur(20px); border:1px solid rgba(255,255,255,.45); border-radius:999px; box-shadow:0 4px 20px rgba(0,0,0,.08), inset 0 1px 0 rgba(255,255,255,.35); display:flex; align-items:stretch; justify-content:space-around; padding:0 10px }
.ai-fab { width:56px; height:56px; border-radius:50%; background:rgba(210,225,250,.55); backdrop-filter:blur(20px); border:1px solid rgba(255,255,255,.45); box-shadow:0 4px 20px rgba(0,0,0,.08), inset 0 1px 0 rgba(255,255,255,.35); display:flex; align-items:center; justify-content:center; cursor:pointer; transition:transform .12s; flex-shrink:0; text-decoration:none }
.ai-fab:active { transform:scale(.92) }
.tab { display:flex; flex-direction:column; align-items:center; justify-content:center; gap:2px; flex:1; padding:8px 4px; border-radius:999px; color:rgba(28,28,30,.45); text-decoration:none; transition:all .18s }
.tab.active { color:#2C7AFC }
.tab-icon svg { width:24px; height:24px; fill:currentColor }
```

**5개 탭 아이콘 (Iconify Fluent Filled — 모든 페이지 동일, 24px):**

| # | 탭 | 링크 | Iconify 코드 |
|---|---|---|---|
| 1 | 홈 | g-guardian-live.html | `fluent:home-24-filled` |
| 2 | AI 케어 가이드 | g02-ai-guide.html | `fluent:shield-checkmark-24-filled` ← v9 변경 |
| 3 | 소통 | g03-sotong.html | `fluent:chat-24-filled` |
| 4 | 기록 | g05-records.html | `fluent:document-text-24-filled` |
| 5 | 마이페이지 | g05-mypage-B.html | `fluent:person-24-filled` |

```html
<!-- 탭바 HTML 템플릿 (아이콘만, 텍스트 없음) -->
<a href="g-guardian-live.html" class="tab">
  <span class="tab-icon"><iconify-icon icon="fluent:home-24-filled" style="font-size:24px"></iconify-icon></span>
</a>
<a href="g02-ai-guide.html" class="tab">
  <span class="tab-icon"><iconify-icon icon="fluent:shield-checkmark-24-filled" style="font-size:24px"></iconify-icon></span>
</a>
<a href="g03-sotong.html" class="tab">
  <span class="tab-icon"><iconify-icon icon="fluent:chat-24-filled" style="font-size:24px"></iconify-icon></span>
</a>
<a href="g05-records.html" class="tab">
  <span class="tab-icon"><iconify-icon icon="fluent:document-text-24-filled" style="font-size:24px"></iconify-icon></span>
</a>
<a href="g05-mypage-B.html" class="tab">
  <span class="tab-icon"><iconify-icon icon="fluent:person-24-filled" style="font-size:24px"></iconify-icon></span>
</a>
```

> 아이콘 원칙: Fluent UI filled 계열 통일, 24px 고정, 탭 간 형태 중복 금지

**Active 탭 규칙:**

- 메인 탭: 해당 탭에 `.active` 클래스 부여
- 서브 페이지: 상위 섹션 탭에 `.active` 부여
  - g02-ai-report, g-ai → 탭2(가이드) active
  - g03-chat, g03-chat-family → 탭3(소통) active
  - g08-billing, g09-prescription, g10-timeline → 탭4(기록) active
- active 없음: g06-alert, g07-settings
- 탭바 없음(의도적): g03-chat-ai, g03-chat-nurse, g03-chat-patient

### common.css 제거 정책

`common.css` 외부 파일은 사용하지 않는다. 모든 페이지는 인라인 `<style>` 블록에 종합 `:root` 변수 + 리셋 + 컴포넌트 스타일을 포함한다. Pretendard 폰트는 CDN 링크로 로드.

---

## 3. 완료된 작업

### UX 전면 감사 및 수정

- [x] `--t3` 대비 개선: `rgba(0,0,0,.25)` → `.35` — 전체 12개+ 페이지 적용
- [x] 글라스 카드 투명도 통일: `0.92` → `0.88` — 전체 페이지 적용
- [x] 채팅 입력 버튼 `:active` 피드백 추가 (g03-chat-nurse, g03-chat-patient)

### common.css 의존성 제거 (6개 파일)

- [x] g07-settings.html
- [x] g08-billing.html
- [x] g09-prescription.html
- [x] g10-timeline.html
- [x] g-ai.html
- [x] g02-ai-report.html

각 파일에 종합 `:root` 변수 블록 + Pretendard CDN 링크 삽입 완료.

### 네비게이션 바 전체 통일

- [x] g08-billing.html — 빈 탭바 → 표준 5탭 추가
- [x] g-ai.html — 완전히 다른 네비바 (흰 배경, 3탭) → 표준 글라스 탭바로 교체
- [x] g03-sotong.html — 잘못된 아이콘(집/나침반) → 표준 하루안부 로고/문서 아이콘으로 교체
- [x] g02-ai-report.html — 구형 흰색 탭바 → 글라스 블러 + bottom-bar 래퍼 + ai-fab 추가, 탭 링크 표준화
- [x] g03-chat.html — 구형 흰색 탭바 → 글라스 블러 + bottom-bar 래퍼 + ai-fab 추가, 탭 링크 표준화
- [x] g03-sotong.html — tabbar height:68→56px, ai-fab 52→56px 통일
- [x] g-guardian-live.html — 탭1 집 아이콘→하루안부 로고, 탭2 나침반→문서 아이콘 교체
- [x] g02-ai-report.html — 탭4 grid→list 아이콘, 탭2 문서 아이콘(3줄thin→2줄thick) 통일
- [x] g03-chat.html — 탭4 grid→list 아이콘 통일
- [x] **2026-04-17** 탭1 로고(viewBox 2526×2526) → **집(house)** 아이콘 교체, 탭2 문서 아이콘 → **나침반(compass)** 아이콘 교체 (15개 네비바 페이지 전체: g-guardian-live, g02-ai-guide, g02-ai-report, g03-sotong, g03-chat, g03-chat-family, g05-records, g05-mypage, g05-mypage-v2, g06-alert, g07-settings, g08-billing, g09-prescription, g10-timeline, g-ai) — 아이콘_가이드.html "C 라운드 소프트" 스타일 준수

### 최종 검증 결과 (14개 네비바 페이지)

| 항목 | 상태 |
|---|---|
| 탭바 CSS (height:56px, 글라스 블러) | 14/14 동일 |
| ai-fab 크기 (56×56px) | 14/14 동일 |
| bottom-bar 래퍼 | 14/14 있음 |
| 탭 링크 5개 (홈/AI가이드/소통/기록/마이페이지) | 14/14 통일 |
| 탭 아이콘 SVG 5종 | 14/14 동일 |
| active 탭 상태 | 각 페이지 정확 |

---

## 4. 남아있는 할 일 / 다음 단계

### 즉시 확인 필요

- [ ] 전체 페이지 실기기/브라우저에서 시각적 QA (특히 네비바 통일 후 렌더링)
- [ ] 온보딩 플로우 (`onboarding/ob01~ob08`) 디자인 감사 미진행
- [ ] icon-pick 페이지 3개 디자인 감사 미진행
- [ ] 채팅 상세 페이지 (g03-chat-ai, g03-chat-nurse, g03-chat-patient) — 탭바 없는 것이 의도적인지 확인

### 추후 고려 사항

- [ ] 다크모드 지원 여부
- [ ] 실제 데이터 연동 / API 구조 설계
- [ ] 접근성(a11y) 전면 감사: aria-label, 키보드 내비게이션, 스크린 리더 호환
- [ ] PWA manifest 및 서비스 워커 세팅
- [ ] 페이지 간 전환 애니메이션
- [ ] 성능 최적화: 인라인 SVG 중복 제거 (공통 심볼 방식 고려)

---

## 5. 주요 파일/리소스 경로

```
v9_보호자앱/
├── g-guardian-live.html      # 보호자 홈 (메인)
├── g02-ai-guide.html         # AI 가이드
├── g02-ai-report.html        # AI 리포트 (서브)
├── g03-sotong.html            # 소통 허브 (메인)
├── g03-chat.html              # 채팅 목록 (서브)
├── g03-chat-ai.html           # AI 채팅 (서브, 탭바 없음)
├── g03-chat-nurse.html        # 간호사 채팅 (서브, 탭바 없음)
├── g03-chat-patient.html      # 환자 채팅 (서브, 탭바 없음)
├── g03-chat-family.html       # 가족 채팅 (서브, 탭바 있음)
├── g05-records.html           # 기록 (메인)
├── g05-mypage.html            # 마이페이지 (메인)
├── g06-alert.html             # 긴급 알림
├── g07-settings.html          # 설정
├── g08-billing.html           # 청구/결제
├── g09-prescription.html      # 처방전
├── g10-timeline.html          # 타임라인
├── g-ai.html                  # AI 어시스턴트
├── icon-pick-*.html           # 아이콘 선택 (3개)
├── onboarding/                # 온보딩 플로우 (ob01~ob08)
├── common.css                 # 더 이상 사용하지 않음 (레거시)
├── manifest.json              # PWA 매니페스트
└── app-icon.svg               # 앱 아이콘
```

**외부 CDN:**

- 폰트: `https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css`
- 아이콘: `https://cdn.jsdelivr.net/npm/iconify-icon@2.3.0/dist/iconify-icon.min.js` (Fluent 디자인 시스템 기반)

---

## 6. 작업 방식 / 제약 사항

- **단일 파일 원칙**: 각 HTML 파일은 독립적으로 동작해야 한다. 외부 CSS 의존 금지 (CDN 폰트/아이콘 제외).
- **한국어 우선**: UI 텍스트, 주석, 커뮤니케이션 모두 한국어.
- **모바일 퍼스트**: max-width 430px 기준, iOS safe-area 대응 필수.
- **수정 시 전체 일관성 유지**: 하나의 컴포넌트를 바꾸면 전체 페이지에 동일하게 반영해야 한다.
- **파일 직접 수정 선호**: 보고서나 제안 대신 직접 코드를 수정하는 방식을 선호.
- **빠른 실행**: 긴 설명보다 바로 실행 후 결과 보여주기.
