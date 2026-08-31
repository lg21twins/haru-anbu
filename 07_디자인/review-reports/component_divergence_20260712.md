# 컴포넌트 정의 다이버전스 리포트

실행 일시: 2026-07-12 22:36:16

## 의미

같은 CSS 클래스명이 여러 화면에서 **서로 다른 사양**으로 정의된 경우.
디자인 시스템 원칙상 컴포넌트는 한 곳(system/components.css)에서 정의되어야 한다.
화면별 로컬 정의는 의도된 변형이 아닌 한 통일 대상.

## 총 발견: 410개 클래스

정규화: 공백·순서·var() 폴백 hex 무시. 그래도 다른 값이면 다이버전스로 판단.

| 클래스 | 정의 파일 수 | 다른 사양 수 |
|---|---:|---:|
| `.toast` | 17 | 7 |
| `.tl-now-strip` | 12 | 6 |
| `.header` | 11 | 7 |
| `.nav-btn` | 11 | 7 |
| `.msg-item` | 10 | 9 |
| `.cp-ai-act` | 10 | 5 |
| `.ho-manual-open` | 10 | 5 |
| `.tl-item` | 9 | 8 |
| `.card` | 9 | 6 |
| `.msg-time` | 9 | 6 |
| `.med-row` | 9 | 5 |
| `.input-field` | 9 | 4 |
| `.obs-card` | 9 | 3 |
| `.roster-wrap` | 9 | 3 |
| `.roster-row` | 9 | 3 |
| `.chip` | 8 | 8 |
| `.main` | 8 | 8 |
| `.fam-icon-btn` | 8 | 7 |
| `.search-input` | 8 | 4 |
| `.ph-item` | 8 | 4 |
| `.al-item` | 8 | 4 |
| `.cl-row` | 8 | 4 |
| `.pt-row` | 8 | 4 |
| `.ho-row` | 8 | 4 |
| `.rec-row` | 8 | 4 |
| `.sidebar-facility` | 8 | 3 |
| `.bottom-scrim` | 8 | 2 |
| `.opt` | 7 | 5 |
| `.sheet` | 7 | 5 |
| `.overlay` | 7 | 4 |
| `.btn` | 6 | 6 |
| `.help-btn` | 6 | 6 |
| `.sec-label` | 6 | 5 |
| `.a-btn` | 6 | 5 |
| `.priority-hero` | 6 | 4 |
| `.cp-ai-intro` | 6 | 4 |
| `.menu-item` | 6 | 4 |
| `.tx` | 6 | 4 |
| `.page-date` | 6 | 3 |
| `.sos-btn` | 6 | 3 |
| `.kpi-bar` | 6 | 3 |
| `.cp-body` | 6 | 3 |
| `.af-item` | 6 | 3 |
| `.cp-input` | 6 | 3 |
| `.cp-msg-list` | 6 | 3 |
| `.cp-convo-input` | 6 | 3 |
| `.pt-qs-track` | 6 | 3 |
| `.ho-hero-stat` | 6 | 3 |
| `.memo-save` | 6 | 3 |
| `.tabbar` | 6 | 3 |
| `.sch-day` | 6 | 3 |
| `.sec` | 6 | 3 |
| `.btn-back` | 6 | 2 |
| `.messages` | 6 | 2 |
| `.tab-label` | 6 | 2 |
| `.hero-wrap` | 6 | 2 |
| `.hero-more` | 6 | 2 |
| `.handover-wrap` | 6 | 2 |
| `.obs-call-mini` | 6 | 2 |
| `.sheet-row-label` | 6 | 2 |
| `.sheet-row-val` | 6 | 2 |
| `.voice-prev-q` | 6 | 2 |
| `.switch` | 6 | 2 |
| `.tl-month` | 5 | 5 |
| `.summary-bar` | 5 | 5 |
| `.sos-fab` | 5 | 5 |
| `.fam-row` | 5 | 5 |
| `.content` | 5 | 3 |
| `.tl-line` | 5 | 3 |
| `.msg` | 5 | 3 |
| `.bubble` | 5 | 3 |
| `.btn-primary` | 5 | 3 |
| `.row` | 5 | 3 |
| `.av` | 5 | 3 |
| `.home-ind` | 5 | 2 |
| `.sos` | 5 | 2 |
| `.stage` | 4 | 4 |
| `.quick-btn` | 4 | 4 |
| `.moment-card` | 4 | 4 |
| `.sch-item` | 4 | 4 |
| `.sd-now` | 4 | 4 |
| `.nav-tab` | 4 | 4 |
| `.todo-list` | 4 | 4 |
| `.tl-wrap` | 4 | 3 |
| `.unread-line` | 4 | 3 |
| `.sec-head` | 4 | 3 |
| `.filter-row` | 4 | 3 |
| `.msg-body` | 4 | 3 |
| `.icon-btn` | 4 | 3 |
| `.actions` | 4 | 3 |
| `.sidebar` | 4 | 2 |
| `.sidebar-logo` | 4 | 2 |
| `.logo-icon` | 4 | 2 |
| `.logo-name` | 4 | 2 |
| `.logo-sub` | 4 | 2 |
| `.facility-dot` | 4 | 2 |
| `.facility-name` | 4 | 2 |
| `.nav-section-label` | 4 | 2 |
| `.nav-list` | 4 | 2 |
| `.nav-link` | 4 | 2 |
| `.nav-icon` | 4 | 2 |
| `.sidebar-user` | 4 | 2 |
| `.user-avatar` | 4 | 2 |
| `.user-name` | 4 | 2 |
| `.user-role` | 4 | 2 |
| `.main-wrapper` | 4 | 2 |
| `.topbar` | 4 | 2 |
| `.greet-pill` | 4 | 2 |
| `.ph-all` | 4 | 2 |
| `.ph-time` | 4 | 2 |
| `.ph-btn` | 4 | 2 |
| `.kpi` | 4 | 2 |
| `.kpi-sub` | 4 | 2 |
| `.kpi-chip` | 4 | 2 |
| `.kpi-value` | 4 | 2 |
| `.kpi-denom` | 4 | 2 |
| `.kpi-fill` | 4 | 2 |
| `.kpi-badge` | 4 | 2 |
| `.kpi-name-chip` | 4 | 2 |
| `.kpi-name-chip-room` | 4 | 2 |
| `.tl-live-dot` | 4 | 2 |
| `.tl-time-col` | 4 | 2 |
| `.tl-name` | 4 | 2 |
| `.al-btn` | 4 | 2 |
| `.ai-badge` | 4 | 2 |
| `.focus-btn` | 4 | 2 |
| `.chat-row` | 4 | 2 |
| `.af-badge` | 4 | 2 |
| `.cp-ai-sub` | 4 | 2 |
| `.cp-ai-item` | 4 | 2 |
| `.cp-ai-item-head` | 4 | 2 |
| `.cp-ai-item-pt` | 4 | 2 |
| `.cp-ai-item-body` | 4 | 2 |
| `.cp-ai-ask-row` | 4 | 2 |
| `.cp-ai-ask-input` | 4 | 2 |
| `.cp-input-row` | 4 | 2 |
| `.med-tl-pt` | 4 | 2 |
| `.med-tl-track` | 4 | 2 |
| `.med-tl-block` | 4 | 2 |
| `.cl-group-head` | 4 | 2 |
| `.pt-room` | 4 | 2 |
| `.pt-qs-item` | 4 | 2 |
| `.pt-qs-more` | 4 | 2 |
| `.pt-act` | 4 | 2 |
| `.pt-more` | 4 | 2 |
| `.week-day` | 4 | 2 |
| `.sch-nf-btn` | 4 | 2 |
| `.ho-pri` | 4 | 2 |
| `.rec-alert-btn` | 4 | 2 |
| `.rec-tl-mk-lbl` | 4 | 2 |
| `.rec-tl-now` | 4 | 2 |
| `.rec-gauge-cell` | 4 | 2 |
| `.rec-gauge-ring` | 4 | 2 |
| `.rec-hero-missing-item` | 4 | 2 |
| `.rec-aiq-item` | 4 | 2 |
| `.rec-aiq-gen-btn` | 4 | 2 |
| `.rec-aiq-bulk` | 4 | 2 |
| `.ho-tl-now` | 4 | 2 |
| `.ho-tl-now-lbl` | 4 | 2 |
| `.ho-tm-block` | 4 | 2 |
| `.ho-tm-action` | 4 | 2 |
| `.cl-don-cell` | 4 | 2 |
| `.cl-don-ring` | 4 | 2 |
| `.cl-tl-evt` | 4 | 2 |
| `.my-row` | 4 | 2 |
| `.my-toggle` | 4 | 2 |
| `.memo-panel__close` | 4 | 2 |
| `.memo-card__delete` | 4 | 2 |
| `.v10-memo-input` | 4 | 2 |
| `.msg-read` | 4 | 2 |
| `.tab-icon` | 4 | 2 |
| `.hero` | 4 | 2 |
| `.back-btn` | 4 | 2 |
| `.now-row` | 4 | 2 |
| `.now-card-cta` | 4 | 2 |
| `.pt-row-c` | 4 | 2 |
| `.grid8` | 4 | 2 |
| `.g-card` | 4 | 2 |
| `.v-field` | 4 | 2 |
| `.chk` | 4 | 2 |
| `.btn-prev` | 4 | 2 |
| `.bs-pt` | 4 | 2 |
| `.bs-pt-c` | 4 | 2 |
| `.bs-f` | 4 | 2 |
| `.bs-btn` | 4 | 2 |
| `.gps-pulse` | 4 | 2 |
| `.sec-ttl` | 4 | 2 |
| `.chat-messages` | 3 | 3 |
| `.msg-bubble` | 3 | 3 |
| `.chat-input` | 3 | 3 |
| `.btn-icon` | 3 | 3 |
| `.voice` | 3 | 3 |
| `.grid` | 3 | 3 |
| `.logout` | 3 | 3 |
| `.tab` | 3 | 3 |
| `.section` | 3 | 3 |
| `.section-title` | 3 | 3 |
| `.input` | 3 | 3 |
| `.progress-bar` | 3 | 3 |
| `.tl` | 3 | 3 |
| `.ai-orb` | 3 | 3 |
| `.top-nav` | 3 | 3 |
| `.ai-placeholder` | 3 | 3 |
| `.ai-fab` | 3 | 3 |
| `.cg-iconbtn` | 3 | 3 |
| `.act-card` | 3 | 3 |
| `.help-grid-routine` | 3 | 3 |
| `.home-btn` | 3 | 3 |
| `.action` | 3 | 3 |
| `.fam-icon-btn--primary` | 3 | 3 |
| `.timeline` | 3 | 3 |
| `.now-action` | 3 | 3 |
| `.p-settings-quick` | 3 | 3 |
| `.quick-chip` | 3 | 3 |
| `.fn-schedule` | 3 | 3 |
| `.role-card` | 3 | 3 |
| `.alert-icon-wrap` | 3 | 3 |
| `.info-row` | 3 | 3 |
| `.msg-cta` | 3 | 3 |
| `.swipe-next` | 3 | 3 |
| `.page-title` | 3 | 2 |
| `.card-head` | 3 | 2 |
| `.tl-desc` | 3 | 2 |
| `.chat-av` | 3 | 2 |
| `.chat-name` | 3 | 2 |
| `.chat-time` | 3 | 2 |
| `.med-name` | 3 | 2 |
| `.sb` | 3 | 2 |
| `.msg-sender` | 3 | 2 |
| `.input-bar` | 3 | 2 |
| `.sec-head__title` | 3 | 2 |
| `.profile` | 3 | 2 |
| `.menu-title` | 3 | 2 |
| `.menu-group` | 3 | 2 |
| `.mi-icon` | 3 | 2 |
| `.mi-body` | 3 | 2 |
| `.mi-label` | 3 | 2 |
| `.mi-desc` | 3 | 2 |
| `.msg-name-row` | 3 | 2 |
| `.msg-name` | 3 | 2 |
| `.msg-preview` | 3 | 2 |
| `.msg-meta` | 3 | 2 |
| `.msg-badge` | 3 | 2 |
| `.sh-btn` | 3 | 2 |
| `.shift` | 3 | 2 |
| `.hero-title` | 3 | 2 |
| `.dots` | 3 | 2 |
| `.dot` | 3 | 2 |
| `.nurse-av` | 2 | 2 |
| `.header-title` | 2 | 2 |
| `.header-btn` | 2 | 2 |
| `.duty-av` | 2 | 2 |
| `.duty-badge` | 2 | 2 |
| `.chat-item` | 2 | 2 |
| `.unread-divider` | 2 | 2 |
| `.voice-bar` | 2 | 2 |
| `.o4-sec` | 2 | 2 |
| `.insight-item` | 2 | 2 |
| `.qr-btn` | 2 | 2 |
| `.care-row` | 2 | 2 |
| `.quick-icon` | 2 | 2 |
| `.quick-label` | 2 | 2 |
| `.live-dock__primary` | 2 | 2 |
| `.feed-card` | 2 | 2 |
| `.phone` | 2 | 2 |
| `.sbar` | 2 | 2 |
| `.btn-link` | 2 | 2 |
| `.header-right` | 2 | 2 |
| `.section-header` | 2 | 2 |
| `.badge` | 2 | 2 |
| `.badge--success` | 2 | 2 |
| `.badge--warning` | 2 | 2 |
| `.badge--critical` | 2 | 2 |
| `.badge--info` | 2 | 2 |
| `.toggle` | 2 | 2 |
| `.avatar` | 2 | 2 |
| `.avatar--sm` | 2 | 2 |
| `.avatar--md` | 2 | 2 |
| `.avatar--lg` | 2 | 2 |
| `.cat-row` | 2 | 2 |
| `.sched-scroll` | 2 | 2 |
| `.sched-chip` | 2 | 2 |
| `.ai-orb-bg` | 2 | 2 |
| `.intro` | 2 | 2 |
| `.intro-check` | 2 | 2 |
| `.intro-check-done` | 2 | 2 |
| `.intro-skip` | 2 | 2 |
| `.logo` | 2 | 2 |
| `.ch-icon-btn` | 2 | 2 |
| `.ch-search-inner` | 2 | 2 |
| `.ch-new-btn` | 2 | 2 |
| `.ch-item` | 2 | 2 |
| `.ai-prompts-label` | 2 | 2 |
| `.ai-prompt-item` | 2 | 2 |
| `.chat-input-area` | 2 | 2 |
| `.ai-mic-btn` | 2 | 2 |
| `.report-view-btn` | 2 | 2 |
| `.chat-hint-btn` | 2 | 2 |
| `.bottom-bar` | 2 | 2 |
| `.section-cta` | 2 | 2 |
| `.moment-photo` | 2 | 2 |
| `.moment-body` | 2 | 2 |
| `.moment-quote` | 2 | 2 |
| `.moment-meta` | 2 | 2 |
| `.grid-full` | 2 | 2 |
| `.w` | 2 | 2 |
| `.w-dot` | 2 | 2 |
| `.sleep-ticks` | 2 | 2 |
| `.w-head` | 2 | 2 |
| `.w-title` | 2 | 2 |
| `.insight-card` | 2 | 2 |
| `.quick-scroll` | 2 | 2 |
| `.page-sub` | 2 | 2 |
| `.mode-bar` | 2 | 2 |
| `.action-btn` | 2 | 2 |
| `.qq` | 2 | 2 |
| `.input-mic` | 2 | 2 |
| `.summary-bar__dot` | 2 | 2 |
| `.summary-bar__text` | 2 | 2 |
| `.av--nurse` | 2 | 2 |
| `.cta-row` | 2 | 2 |
| `.nav-card` | 2 | 2 |
| `.nav-row` | 2 | 2 |
| `.nav-month` | 2 | 2 |
| `.nav-range` | 2 | 2 |
| `.sum-row` | 2 | 2 |
| `.sum-pill` | 2 | 2 |
| `.cg-sos` | 2 | 2 |
| `.cg-sos-card` | 2 | 2 |
| `.cg-sos-countdown__cancel` | 2 | 2 |
| `.cg-row` | 2 | 2 |
| `.cg-keypad__btn` | 2 | 2 |
| `.cg-switch` | 2 | 2 |
| `.hc` | 2 | 2 |
| `.act-cta` | 2 | 2 |
| `.pick-row` | 2 | 2 |
| `.h-title` | 2 | 2 |
| `.profile-hero` | 2 | 2 |
| `.pf-top` | 2 | 2 |
| `.pf-ava` | 2 | 2 |
| `.pf-name` | 2 | 2 |
| `.pf-stats` | 2 | 2 |
| `.pf-stat` | 2 | 2 |
| `.gps` | 2 | 2 |
| `.rows` | 2 | 2 |
| `.opt__toggle` | 2 | 2 |
| `.help-grid-special` | 2 | 2 |
| `.help-btn--brand` | 2 | 2 |
| `.help-btn--urgent` | 2 | 2 |
| `.help-family` | 2 | 2 |
| `.done-mark` | 2 | 2 |
| `.cards` | 2 | 2 |
| `.msg-av` | 2 | 2 |
| `.msg-photos` | 2 | 2 |
| `.bottom` | 2 | 2 |
| `.caption` | 2 | 2 |
| `.clock-time` | 2 | 2 |
| `.nav-tab--active` | 2 | 2 |
| `.glass` | 2 | 2 |
| `.btn--xl` | 2 | 2 |
| `.btn--lg` | 2 | 2 |
| `.btn--md` | 2 | 2 |
| `.btn--primary` | 2 | 2 |
| `.call-cols` | 2 | 2 |
| `.call-panel` | 2 | 2 |
| `.fam-row-meta` | 2 | 2 |
| `.fam-row-name` | 2 | 2 |
| `.fam-row-status` | 2 | 2 |
| `.fam-row-actions` | 2 | 2 |
| `.tl-day` | 2 | 2 |
| `.tl-item--unread` | 2 | 2 |
| `.progress` | 2 | 2 |
| `.progress-fill` | 2 | 2 |
| `.todo-item` | 2 | 2 |
| `.todo-time` | 2 | 2 |
| `.todo-name` | 2 | 2 |
| `.todo-sub` | 2 | 2 |
| `.todo-status` | 2 | 2 |
| `.voice-btn` | 2 | 2 |
| `.fam-quick-more` | 2 | 2 |
| `.now-confirm` | 2 | 2 |
| `.cf-btn` | 2 | 2 |
| `.cf-btn--ghost` | 2 | 2 |
| `.b-text` | 2 | 2 |
| `.b-text--live` | 2 | 2 |
| `.listen-status` | 2 | 2 |
| `.or-row` | 2 | 2 |
| `.alert-sub` | 2 | 2 |
| `.action-primary` | 2 | 2 |
| `.action-secondary` | 2 | 2 |
| `.conf-overlay` | 2 | 2 |
| `.conf-sheet` | 2 | 2 |
| `.conf-eyebrow` | 2 | 2 |
| `.conf-ttl` | 2 | 2 |
| `.conf-sub` | 2 | 2 |
| `.conf-opt` | 2 | 2 |
| `.conf-action-danger` | 2 | 2 |
| `.conf-cancel` | 2 | 2 |
| `.alert-cta` | 2 | 2 |
| `.compose-input` | 2 | 2 |
| `.compose-send` | 2 | 2 |
| `.sbar-tile` | 2 | 2 |
| `.sbar-rec-row` | 2 | 2 |
| `.check-row` | 2 | 2 |
| `.input-ttl` | 2 | 2 |
| `.swipe-skip` | 2 | 2 |
| `.pl-item` | 2 | 2 |
| `.intro-btn-primary` | 2 | 2 |
| `.intro-hist-row` | 2 | 2 |
| `.ja-opt` | 2 | 2 |

## 상세 (상위 30개)

### `.toast` — 17개 파일, 7개 다른 사양

**버전 1** (1개 파일):
- `v11_보호자앱/common.css`: `position: fixed; top: 80px; left: 50%; transform: translateX(-50%); display: fle`

**버전 2** (1개 파일):
- `v11_보호자앱/styles/g-guardian-live-part-2.css`: `position:fixed;top:80px;left:50%;transform:translateX(-50%) translateY(-8px);bac`

**버전 3** (3개 파일):
- `v11_요양보호사앱/c04-schedule.html`: `position: fixed; top: 80px; left: 50%; transform: translateX(-50%) translateY(-8`
- `v11_요양보호사앱/styles/c04-schedule.css`: `position: fixed; top: 80px; left: 50%; transform: translateX(-50%) translateY(-8`
- `v11_요양보호사앱/styles/c03-sotong.css`: `position: fixed; top: 80px; left: 50%; transform: translateX(-50%) translateY(-8`

**버전 4** (3개 파일):
- `v11_요양보호사앱/c01-today.en.html`: `position: fixed; left: 50%; bottom: calc(var(--safe-b) + var(--tab-h) + var(--ta`
- `v11_요양보호사앱/c01-today.html`: `position: fixed; left: 50%; bottom: calc(var(--safe-b) + var(--tab-h) + var(--ta`
- `v11_요양보호사앱/c01-today.zh.html`: `position: fixed; left: 50%; bottom: calc(var(--safe-b) + var(--tab-h) + var(--ta`

**버전 5** (2개 파일):
- `v11_요양보호사앱/c02-checklist.en.html`: `position: fixed; top: 72px; left: 50%; transform: translateX(-50%) translateY(-8`
- `v11_요양보호사앱/styles/c02-checklist.css`: `position: fixed; top: 72px; left: 50%; transform: translateX(-50%) translateY(-8`

**버전 6** (6개 파일):
- `v11_요양보호사앱/styles/c04-mypage.css`: `position:fixed;left:50%;bottom:calc(var(--safe-b) + var(--tab-h) + var(--tab-bot`
- `v15_의료진앱/d05-mypage.html`: `position:fixed;left:50%;bottom:calc(var(--safe-b) + var(--tab-h) + var(--tab-bot`
- `v15_의료진앱/styles/d01-home.css`: `position:fixed;left:50%;bottom:calc(var(--safe-b) + var(--tab-h) + var(--tab-bot`
- `v15_의료진앱/styles/d03-inbox.css`: `position:fixed;left:50%;bottom:calc(var(--safe-b) + var(--tab-h) + var(--tab-bot`
- `v15_의료진앱/styles/d04-handover.css`: `position:fixed;left:50%;bottom:calc(var(--safe-b) + var(--tab-h) + var(--tab-bot`
- … 외 1개

**버전 7** (1개 파일):
- `v15_의료진앱/d-sos.html`: `position:fixed;left:50%;bottom:calc(var(--safe-b) + 110px); transform:translateX`

### `.tl-now-strip` — 12개 파일, 6개 다른 사양

**버전 1** (2개 파일):
- `v10_의료진웹/의료진_대시보드_v9.5.en.html`: `display: flex; align-items:center; gap:8px; padding: 9px 14px; margin-bottom: 20`
- `v10_의료진웹/의료진_대시보드_v9.5.html`: `display: flex; align-items:center; gap:8px; padding: 9px 14px; margin-bottom: 20`

**버전 2** (2개 파일):
- `v10_의료진웹/의료진_대시보드_v9.5.en.html`: `font-family: var(--font-mono), var(--font); font-feature-settings: 'tnum' 1, 'ze`
- `v10_의료진웹/의료진_대시보드_v9.5.html`: `font-family: var(--font-mono), var(--font); font-feature-settings: 'tnum' 1, 'ze`

**버전 3** (2개 파일):
- `v10_의료진웹/의료진_대시보드_v9.5.en.html`: `font-family: var(--font) !important;`
- `v10_의료진웹/의료진_대시보드_v9.5.html`: `font-family: var(--font) !important;`

**버전 4** (2개 파일):
- `v10_의료진웹/의료진_대시보드_v9.5.en.html`: `font-family: var(--font-mono), var(--font) !important;`
- `v10_의료진웹/의료진_대시보드_v9.5.html`: `font-family: var(--font-mono), var(--font) !important;`

**버전 5** (2개 파일):
- `v10_의료진웹/의료진_대시보드_v9.5.en.html`: `position: relative;`
- `v10_의료진웹/의료진_대시보드_v9.5.html`: `position: relative;`

**버전 6** (2개 파일):
- `v10_의료진웹/의료진_대시보드_v9.5.en.html`: `content: 'LIVE'; margin-left: auto; font-size: 9px; font-weight: 800; letter-spa`
- `v10_의료진웹/의료진_대시보드_v9.5.html`: `content: 'LIVE'; margin-left: auto; font-size: 9px; font-weight: 800; letter-spa`

### `.header` — 11개 파일, 7개 다른 사양

**버전 1** (2개 파일):
- `v11_보호자앱/g03-chat-nurse.html`: `position:sticky;top:0;z-index:30;display:flex;align-items:center;gap:12px;paddin`
- `v11_보호자앱/g03-chat-patient.html`: `position:sticky;top:0;z-index:30;display:flex;align-items:center;gap:12px;paddin`

**버전 2** (1개 파일):
- `v11_보호자앱/g03-chat.html`: `position:sticky;top:0;z-index:30;padding:calc(env(safe-area-inset-top,0px) + 8px`

**버전 3** (1개 파일):
- `v11_보호자앱/common.css`: `display: flex; align-items: center; justify-content: space-between; height: var(`

**버전 4** (1개 파일):
- `v11_보호자앱/styles/g-guardian-live-part-2.css`: `padding:calc(env(safe-area-inset-top,0px) + 6px) 20px 0;position:static;backgrou`

**버전 5** (1개 파일):
- `v11_보호자앱/styles/g03-chat-ai-part-1.css`: `position:sticky;top:0;z-index:30;display:flex;align-items:center;gap:12px;paddin`

**버전 6** (2개 파일):
- `v11_요양보호사앱/styles/c03-sotong.css`: `padding:calc(var(--safe-t) + 6px) var(--page-pad) 0;position:static;`
- `v15_의료진앱/styles/d03-inbox.css`: `padding:calc(var(--safe-t) + 6px) var(--page-pad) 0; position:static;`

**버전 7** (3개 파일):
- `v15_의료진앱/d05-mypage.html`: `padding:calc(var(--safe-t) + 14px) var(--page-pad) 8px;position:relative;z-index`
- `v15_의료진앱/styles/d04-handover.css`: `padding:calc(var(--safe-t) + 14px) var(--page-pad) 8px;position:relative;z-index`
- `v15_의료진앱/styles/d02-round.css`: `padding:calc(var(--safe-t) + 14px) var(--page-pad) 8px; position:relative;z-inde`

### `.nav-btn` — 11개 파일, 7개 다른 사양

**버전 1** (3개 파일):
- `v11_보호자앱/g03-chat-nurse.html`: `width:36px;height:36px;border-radius:50%;background:rgba(255,255,255,.6);border:`
- `v11_보호자앱/g03-chat-patient.html`: `width:36px;height:36px;border-radius:50%;background:rgba(255,255,255,.6);border:`
- `v11_보호자앱/styles/g03-chat-ai-part-1.css`: `width:36px;height:36px;border-radius:50%;background:rgba(255,255,255,.6);border:`

**버전 2** (3개 파일):
- `v11_보호자앱/g03-chat-nurse.html`: `transform:scale(.93)`
- `v11_보호자앱/g03-chat-patient.html`: `transform:scale(.93)`
- `v11_보호자앱/styles/g03-chat-ai-part-1.css`: `transform:scale(.93)`

**버전 3** (1개 파일):
- `v12_환자앱/p06-photo.html`: `width: 88px; height: 88px; border-radius: 50%; background: var(--color-bg-surfac`

**버전 4** (1개 파일):
- `v12_환자앱/p06-photo.html`: `box-shadow: 0 12px 30px rgba(0, 0, 0, 0.16);`

**버전 5** (1개 파일):
- `v12_환자앱/p06-photo.html`: `transform: scale(.93);`

**버전 6** (1개 파일):
- `v12_환자앱/p06-photo.html`: `opacity: .35; cursor: default;`

**버전 7** (1개 파일):
- `v12_환자앱/p06-photo.html`: `width: 60px; height: 60px;`

### `.msg-item` — 10개 파일, 9개 다른 사양

**버전 1** (1개 파일):
- `v11_보호자앱/styles/g03-sotong-part-1.css`: `display: flex; align-items: center; gap: var(--space-4); padding: var(--space-4)`

**버전 2** (2개 파일):
- `v11_보호자앱/styles/g03-sotong-part-1.css`: `transform: scale(0.98);`
- `v11_요양보호사앱/styles/c03-sotong.css`: `transform: scale(0.98);`

**버전 3** (1개 파일):
- `v11_보호자앱/styles/g03-sotong-part-1.css`: `animation: haru-fade-in-up var(--motion-enter) var(--easing-standard) both;`

**버전 4** (1개 파일):
- `v11_보호자앱/styles/g03-sotong-part-1.css`: `animation: none !important;`

**버전 5** (1개 파일):
- `v11_요양보호사앱/styles/c03-sotong.css`: `display: flex; align-items: center; gap: var(--space-4); padding: var(--space-4)`

**버전 6** (1개 파일):
- `v15_의료진앱/styles/d03-inbox.css`: `display:flex;align-items:center;gap:14px; padding:12px 16px; background:var(--pa`

**버전 7** (1개 파일):
- `v15_의료진앱/styles/d03-inbox.css`: `transform:scale(.99);`

**버전 8** (1개 파일):
- `v15_의료진앱/styles/d03-inbox.css`: `animation: haru-fade-in-up var(--duration-slow, 350ms) var(--easing-standard) bo`

**버전 9** (1개 파일):
- `v15_의료진앱/styles/d03-inbox.css`: `animation:none !important;`

### `.cp-ai-act` — 10개 파일, 5개 다른 사양

**버전 1** (2개 파일):
- `v10_의료진웹/의료진_대시보드_v9.5.en.html`: `padding: 4px 12px; border-radius: 999px; font-size: 11px; font-weight: 600; bord`
- `v10_의료진웹/의료진_대시보드_v9.5.html`: `padding: 4px 12px; border-radius: 999px; font-size: 11px; font-weight: 600; bord`

**버전 2** (2개 파일):
- `v10_의료진웹/의료진_대시보드_v9.5.en.html`: `border-color: var(--ink-4); color: var(--ink-2);`
- `v10_의료진웹/의료진_대시보드_v9.5.html`: `border-color: var(--ink-4); color: var(--ink-2);`

**버전 3** (2개 파일):
- `v10_의료진웹/의료진_대시보드_v9.5.en.html`: `display: inline-flex; align-items: center; justify-content: center; height: 28px`
- `v10_의료진웹/의료진_대시보드_v9.5.html`: `display: inline-flex; align-items: center; justify-content: center; height: 28px`

**버전 4** (2개 파일):
- `v10_의료진웹/의료진_대시보드_v9.5.en.html`: `background: var(--surface-warm); color: var(--ink); box-shadow: 0 2px 4px rgba(0`
- `v10_의료진웹/의료진_대시보드_v9.5.html`: `background: var(--surface-warm); color: var(--ink); box-shadow: 0 2px 4px rgba(0`

**버전 5** (2개 파일):
- `v10_의료진웹/의료진_대시보드_v9.5.en.html`: `box-shadow: 0 0 0 3px rgba(var(--brand-green-500-rgb), .30), 0 1px 2px rgba(0,0,`
- `v10_의료진웹/의료진_대시보드_v9.5.html`: `box-shadow: 0 0 0 3px rgba(var(--brand-green-500-rgb), .30), 0 1px 2px rgba(0,0,`

### `.ho-manual-open` — 10개 파일, 5개 다른 사양

**버전 1** (2개 파일):
- `v10_의료진웹/의료진_대시보드_v9.5.en.html`: `padding: 5px 10px; border-radius: 999px; font-size: 10.5px; font-weight: 600; bo`
- `v10_의료진웹/의료진_대시보드_v9.5.html`: `padding: 5px 10px; border-radius: 999px; font-size: 10.5px; font-weight: 600; bo`

**버전 2** (2개 파일):
- `v10_의료진웹/의료진_대시보드_v9.5.en.html`: `background: var(--surface); color: var(--ink);`
- `v10_의료진웹/의료진_대시보드_v9.5.html`: `background: var(--surface); color: var(--ink);`

**버전 3** (2개 파일):
- `v10_의료진웹/의료진_대시보드_v9.5.en.html`: `border: 0 !important; background: var(--surface);`
- `v10_의료진웹/의료진_대시보드_v9.5.html`: `border: 0 !important; background: var(--surface);`

**버전 4** (2개 파일):
- `v10_의료진웹/의료진_대시보드_v9.5.en.html`: `background: var(--surface-tint-3);`
- `v10_의료진웹/의료진_대시보드_v9.5.html`: `background: var(--surface-tint-3);`

**버전 5** (2개 파일):
- `v10_의료진웹/의료진_대시보드_v9.5.en.html`: `background: var(--surface-warm); box-shadow: 0 2px 4px rgba(0,0,0,.07), 0 4px 10`
- `v10_의료진웹/의료진_대시보드_v9.5.html`: `background: var(--surface-warm); box-shadow: 0 2px 4px rgba(0,0,0,.07), 0 4px 10`

### `.tl-item` — 9개 파일, 8개 다른 사양

**버전 1** (2개 파일):
- `v10_의료진웹/의료진_대시보드_v9.5.en.html`: `display: flex; gap: 0; position:relative; align-items:stretch;`
- `v10_의료진웹/의료진_대시보드_v9.5.html`: `display: flex; gap: 0; position:relative; align-items:stretch;`

**버전 2** (1개 파일):
- `v11_보호자앱/styles/g10-timeline-part-1.css`: `position: relative;`

**버전 3** (1개 파일):
- `v11_보호자앱/styles/g10-timeline-part-1.css`: `content: ''; position: absolute; left: -22px; top: 23px; width: 10px; height: 10`

**버전 4** (1개 파일):
- `v11_보호자앱/styles/g10-timeline-part-1.css`: `animation: haru-fade-in-up var(--motion-enter) var(--easing-standard) both;`

**버전 5** (1개 파일):
- `v11_보호자앱/styles/g10-timeline-part-1.css`: `animation: none !important;`

**버전 6** (1개 파일):
- `v12_환자앱/styles/p03-call.css`: `outline: 3px solid var(--brand-orange-500); outline-offset: 3px; border-radius: `

**버전 7** (1개 파일):
- `v12_환자앱/styles/p03-call.css`: `display: grid; grid-template-columns: 48px 1fr; gap: 12px; align-items: start; p`

**버전 8** (1개 파일):
- `v12_환자앱/styles/p03-call.css`: `background: rgba(255, 255, 255, 0.6);`

### `.card` — 9개 파일, 6개 다른 사양

**버전 1** (2개 파일):
- `v10_의료진웹/의료진_대시보드_v9.5.en.html`: `background: var(--card-bg); border: var(--card-br); border-radius: var(--card-ra`
- `v10_의료진웹/의료진_대시보드_v9.5.html`: `background: var(--card-bg); border: var(--card-br); border-radius: var(--card-ra`

**버전 2** (2개 파일):
- `v10_의료진웹/의료진_대시보드_v9.5.en.html`: `box-shadow: var(--card-sh);`
- `v10_의료진웹/의료진_대시보드_v9.5.html`: `box-shadow: var(--card-sh);`

**버전 3** (1개 파일):
- `v11_보호자앱/g05-mypage.html`: `box-shadow: var(--shadow-card-floating) !important; border: 0 !important;`

**버전 4** (1개 파일):
- `v11_보호자앱/common.css`: `background: var(--surface); border-radius: var(--radius-md); padding: var(--spac`

**버전 5** (2개 파일):
- `v11_요양보호사앱/c04-schedule.html`: `background: var(--cg-card-bg); border: 0; border-radius: var(--cg-card-radius); `
- `v11_요양보호사앱/styles/c04-schedule.css`: `background: var(--cg-card-bg); border: 0; border-radius: var(--cg-card-radius); `

**버전 6** (1개 파일):
- `v15_의료진앱/styles/d02-round.css`: `background:var(--palette-white);border-radius:var(--radius-card-lg); box-shadow:`

### `.msg-time` — 9개 파일, 6개 다른 사양

**버전 1** (3개 파일):
- `v11_보호자앱/g03-chat-nurse.html`: `font-size:10px;color:var(--t3);align-self:flex-end;flex-shrink:0;padding-bottom:`
- `v11_보호자앱/g03-chat-patient.html`: `font-size:10px;color:var(--t3);align-self:flex-end;flex-shrink:0;padding-bottom:`
- `v11_보호자앱/styles/g03-chat-ai-part-1.css`: `font-size:10px;color:var(--t3);align-self:flex-end;flex-shrink:0;padding-bottom:`

**버전 2** (1개 파일):
- `v11_보호자앱/g03-chat-family.html`: `font-size: var(--text-mini); color: var(--text-tertiary); align-self: flex-end; `

**버전 3** (2개 파일):
- `v11_보호자앱/styles/g03-sotong-part-1.css`: `font-size: var(--text-mini); color: var(--color-text-tertiary); font-weight: var`
- `v11_요양보호사앱/styles/c03-sotong.css`: `font-size: var(--text-mini); color: var(--color-text-tertiary); font-weight: var`

**버전 4** (1개 파일):
- `v12_환자앱/p07-message.html`: `font: var(--weight-medium) 14px / 1 var(--font-family-base); color: var(--color-`

**버전 5** (1개 파일):
- `v12_환자앱/styles/p01-today.css`: `font-size: 18px; font-weight: 600; color: var(--patient-text-warm); margin-top: `

**버전 6** (1개 파일):
- `v15_의료진앱/styles/d03-inbox.css`: `font-size:11.5px;font-weight:500;color:var(--t3);`

### `.med-row` — 9개 파일, 5개 다른 사양

**버전 1** (2개 파일):
- `v10_의료진웹/의료진_대시보드_v9.5.en.html`: `display: grid; grid-template-columns: 200px 1fr 120px 84px 90px 110px 96px; gap:`
- `v10_의료진웹/의료진_대시보드_v9.5.html`: `display: grid; grid-template-columns: 200px 1fr 120px 84px 90px 110px 96px; gap:`

**버전 2** (2개 파일):
- `v10_의료진웹/의료진_대시보드_v9.5.en.html`: `padding-top: 13px; padding-bottom: 13px; border-bottom: 1px solid var(--surface)`
- `v10_의료진웹/의료진_대시보드_v9.5.html`: `padding-top: 13px; padding-bottom: 13px; border-bottom: 1px solid var(--surface)`

**버전 3** (2개 파일):
- `v10_의료진웹/의료진_대시보드_v9.5.en.html`: `background: var(--surface-warm);`
- `v10_의료진웹/의료진_대시보드_v9.5.html`: `background: var(--surface-warm);`

**버전 4** (2개 파일):
- `v10_의료진웹/의료진_대시보드_v9.5.en.html`: `border-bottom: none;`
- `v10_의료진웹/의료진_대시보드_v9.5.html`: `border-bottom: none;`

**버전 5** (1개 파일):
- `v11_보호자앱/styles/g09-prescription-part-1.css`: `display: flex; align-items: center; gap: var(--space-3); padding: var(--space-3)`

### `.input-field` — 9개 파일, 4개 다른 사양

**버전 1** (2개 파일):
- `v11_보호자앱/g03-chat-nurse.html`: `flex:1;height:100%;border:none;font-family:var(--font);font-size:15px;outline:no`
- `v11_보호자앱/g03-chat-patient.html`: `flex:1;height:100%;border:none;font-family:var(--font);font-size:15px;outline:no`

**버전 2** (3개 파일):
- `v11_보호자앱/g03-chat-nurse.html`: `box-shadow:0 0 0 2px var(--color-accent), 0 0 0 4px rgba(var(--color-accent-rgb)`
- `v11_보호자앱/g03-chat-patient.html`: `box-shadow:0 0 0 2px var(--color-accent), 0 0 0 4px rgba(var(--color-accent-rgb)`
- `v11_보호자앱/styles/g03-chat-ai-part-1.css`: `box-shadow:0 0 0 2px var(--color-accent), 0 0 0 4px rgba(var(--color-accent-rgb)`

**버전 3** (3개 파일):
- `v11_보호자앱/g03-chat-nurse.html`: `color:rgba(28,28,30,.4)`
- `v11_보호자앱/g03-chat-patient.html`: `color:rgba(28,28,30,.4)`
- `v11_보호자앱/styles/g03-chat-ai-part-1.css`: `color:rgba(28,28,30,.4)`

**버전 4** (1개 파일):
- `v11_보호자앱/styles/g03-chat-ai-part-1.css`: `flex:1;height:38px;border:none;font-family:var(--font);font-size:15px;outline:no`

### `.obs-card` — 9개 파일, 3개 다른 사양

**버전 1** (3개 파일):
- `v11_요양보호사앱/c01-today.en.html`: `margin: 12px var(--page-pad) 0; padding: 11px 14px 10px; display: flex; flex-dir`
- `v11_요양보호사앱/c01-today.html`: `margin: 12px var(--page-pad) 0; padding: 11px 14px 10px; display: flex; flex-dir`
- `v11_요양보호사앱/c01-today.zh.html`: `margin: 12px var(--page-pad) 0; padding: 11px 14px 10px; display: flex; flex-dir`

**버전 2** (3개 파일):
- `v11_요양보호사앱/c01-today.en.html`: `transform: scale(.995);`
- `v11_요양보호사앱/c01-today.html`: `transform: scale(.995);`
- `v11_요양보호사앱/c01-today.zh.html`: `transform: scale(.995);`

**버전 3** (3개 파일):
- `v11_요양보호사앱/c01-today.en.html`: `animation-delay: .04s;`
- `v11_요양보호사앱/c01-today.html`: `animation-delay: .04s;`
- `v11_요양보호사앱/c01-today.zh.html`: `animation-delay: .04s;`

### `.roster-wrap` — 9개 파일, 3개 다른 사양

**버전 1** (3개 파일):
- `v11_요양보호사앱/c01-today.en.html`: `margin: 18px var(--page-pad) 0; position: relative; z-index: 1;`
- `v11_요양보호사앱/c01-today.html`: `margin: 18px var(--page-pad) 0; position: relative; z-index: 1;`
- `v11_요양보호사앱/c01-today.zh.html`: `margin: 18px var(--page-pad) 0; position: relative; z-index: 1;`

**버전 2** (3개 파일):
- `v11_요양보호사앱/c01-today.en.html`: `animation: haru-fade-in-up var(--duration-slow, 350ms) var(--easing-standard) bo`
- `v11_요양보호사앱/c01-today.html`: `animation: haru-fade-in-up var(--duration-slow, 350ms) var(--easing-standard) bo`
- `v11_요양보호사앱/c01-today.zh.html`: `animation: haru-fade-in-up var(--duration-slow, 350ms) var(--easing-standard) bo`

**버전 3** (3개 파일):
- `v11_요양보호사앱/c01-today.en.html`: `animation-delay: .16s;`
- `v11_요양보호사앱/c01-today.html`: `animation-delay: .16s;`
- `v11_요양보호사앱/c01-today.zh.html`: `animation-delay: .16s;`

### `.roster-row` — 9개 파일, 3개 다른 사양

**버전 1** (3개 파일):
- `v11_요양보호사앱/c01-today.en.html`: `display: flex; align-items: center; gap: 10px; padding: 10px 12px; border-bottom`
- `v11_요양보호사앱/c01-today.html`: `display: flex; align-items: center; gap: 10px; padding: 10px 12px; border-bottom`
- `v11_요양보호사앱/c01-today.zh.html`: `display: flex; align-items: center; gap: 10px; padding: 10px 12px; border-bottom`

**버전 2** (3개 파일):
- `v11_요양보호사앱/c01-today.en.html`: `border-bottom: 0;`
- `v11_요양보호사앱/c01-today.html`: `border-bottom: 0;`
- `v11_요양보호사앱/c01-today.zh.html`: `border-bottom: 0;`

**버전 3** (3개 파일):
- `v11_요양보호사앱/c01-today.en.html`: `background: rgba(0,0,0,.02);`
- `v11_요양보호사앱/c01-today.html`: `background: rgba(0,0,0,.02);`
- `v11_요양보호사앱/c01-today.zh.html`: `background: rgba(0,0,0,.02);`

### `.chip` — 8개 파일, 8개 다른 사양

**버전 1** (1개 파일):
- `v11_보호자앱/common.css`: `display: inline-flex; align-items: center; gap: var(--space-xs); height: var(--b`

**버전 2** (1개 파일):
- `v11_보호자앱/styles/g03-chat-ai-part-1.css`: `display:flex;align-items:center;gap:5px;padding:7px 14px;border-radius:999px;fon`

**버전 3** (1개 파일):
- `v11_보호자앱/styles/g03-chat-ai-part-1.css`: `transform:scale(.95)`

**버전 4** (1개 파일):
- `v12_환자앱/p07-message.html`: `padding: 14px 22px; border-radius: 999px; background: rgba(255, 255, 255, 0.9); `

**버전 5** (1개 파일):
- `v12_환자앱/p07-message.html`: `background: var(--brand-orange-100); color: var(--brand-orange-700);`

**버전 6** (1개 파일):
- `v12_환자앱/p07-message.html`: `transform: scale(.96);`

**버전 7** (1개 파일):
- `v12_환자앱/p07-message.html`: `font-size: 18px; padding: 12px 18px;`

**버전 8** (1개 파일):
- `v15_의료진앱/styles/d03-inbox.css`: `flex-shrink:0; height:34px;padding:0 14px; border-radius:999px; background:rgba(`

### `.main` — 8개 파일, 8개 다른 사양

**버전 1** (1개 파일):
- `v12_환자앱/p08-help.html`: `flex: 1; display: flex; flex-direction: column; gap: var(--space-4); min-height:`

**버전 2** (1개 파일):
- `v12_환자앱/p10-med-done.html`: `flex: 1; display: flex; flex-direction: column; align-items: center; gap: var(--`

**버전 3** (1개 파일):
- `v12_환자앱/p07-message.html`: `flex: 1; display: grid; grid-template-rows: auto 1fr auto auto; gap: var(--space`

**버전 4** (1개 파일):
- `v12_환자앱/p06-photo.html`: `flex: 1; display: grid; grid-template-columns: 1fr; grid-template-rows: auto 1fr`

**버전 5** (1개 파일):
- `v12_환자앱/styles/p03-call.css`: `flex: 1; display: flex; flex-direction: column; gap: 18px; min-height: 0;`

**버전 6** (1개 파일):
- `v12_환자앱/styles/p02-med-alert.css`: `flex: 1; display: flex; flex-direction: column; gap: var(--space-5); min-height:`

**버전 7** (1개 파일):
- `v12_환자앱/styles/p01-today.css`: `flex: 1; display: grid; grid-template-columns: 7fr 3fr; gap: 16px; min-height: 0`

**버전 8** (1개 파일):
- `v12_환자앱/styles/p05-voice.css`: `flex: 1; display: grid; grid-template-rows: 1fr auto auto; gap: var(--space-6); `

### `.fam-icon-btn` — 8개 파일, 7개 다른 사양

**버전 1** (1개 파일):
- `v12_환자앱/styles/p03-call.css`: `border-radius: 50%; outline-offset: 4px;`

**버전 2** (1개 파일):
- `v12_환자앱/styles/p03-call.css`: `width: 60px; height: 60px; border-radius: 50%; display: inline-flex; align-items`

**버전 3** (2개 파일):
- `v12_환자앱/styles/p03-call.css`: `background: var(--brand-orange-100);`
- `v12_환자앱/styles/p01-today.css`: `background: var(--brand-orange-100);`

**버전 4** (1개 파일):
- `v12_환자앱/styles/p03-call.css`: `transform: scale(.94);`

**버전 5** (1개 파일):
- `v12_환자앱/styles/p03-call.css`: `width: 52px; height: 52px;`

**버전 6** (1개 파일):
- `v12_환자앱/styles/p01-today.css`: `width: 44px; height: 44px; border-radius: 50%; display: inline-flex; align-items`

**버전 7** (1개 파일):
- `v12_환자앱/styles/p01-today.css`: `transform: scale(.92);`

### `.search-input` — 8개 파일, 4개 다른 사양

**버전 1** (2개 파일):
- `v10_의료진웹/의료진_대시보드_v9.5.en.html`: `width: 100%; padding: 7px 12px 7px 29px; background: var(--surface); border: 1px`
- `v10_의료진웹/의료진_대시보드_v9.5.html`: `width: 100%; padding: 7px 12px 7px 29px; background: var(--surface); border: 1px`

**버전 2** (2개 파일):
- `v10_의료진웹/의료진_대시보드_v9.5.en.html`: `border-color: rgba(var(--brand-green-500-rgb), .35); box-shadow: 0 0 0 3px rgba(`
- `v10_의료진웹/의료진_대시보드_v9.5.html`: `border-color: rgba(var(--brand-green-500-rgb), .35); box-shadow: 0 0 0 3px rgba(`

**버전 3** (2개 파일):
- `v10_의료진웹/의료진_대시보드_v9.5.en.html`: `box-shadow: 0 0 0 3px rgba(var(--brand-green-500-rgb), .12);`
- `v10_의료진웹/의료진_대시보드_v9.5.html`: `box-shadow: 0 0 0 3px rgba(var(--brand-green-500-rgb), .12);`

**버전 4** (2개 파일):
- `v10_의료진웹/의료진_대시보드_v9.5.en.html`: `box-shadow: 0 0 0 3px rgba(var(--brand-green-500-rgb), .14), 0 1px 2px rgba(0,0,`
- `v10_의료진웹/의료진_대시보드_v9.5.html`: `box-shadow: 0 0 0 3px rgba(var(--brand-green-500-rgb), .14), 0 1px 2px rgba(0,0,`

### `.ph-item` — 8개 파일, 4개 다른 사양

**버전 1** (2개 파일):
- `v10_의료진웹/의료진_대시보드_v9.5.en.html`: `display: grid; grid-template-columns: 68px 1fr 92px 78px; gap: 16px; align-items`
- `v10_의료진웹/의료진_대시보드_v9.5.html`: `display: grid; grid-template-columns: 68px 1fr 92px 78px; gap: 16px; align-items`

**버전 2** (2개 파일):
- `v10_의료진웹/의료진_대시보드_v9.5.en.html`: `border-bottom: none;`
- `v10_의료진웹/의료진_대시보드_v9.5.html`: `border-bottom: none;`

**버전 3** (2개 파일):
- `v10_의료진웹/의료진_대시보드_v9.5.en.html`: `background: var(--surface-warm);`
- `v10_의료진웹/의료진_대시보드_v9.5.html`: `background: var(--surface-warm);`

**버전 4** (2개 파일):
- `v10_의료진웹/의료진_대시보드_v9.5.en.html`: `background: rgba(var(--brand-green-500-rgb), .025) !important;`
- `v10_의료진웹/의료진_대시보드_v9.5.html`: `background: rgba(var(--brand-green-500-rgb), .025) !important;`

### `.al-item` — 8개 파일, 4개 다른 사양

**버전 1** (2개 파일):
- `v10_의료진웹/의료진_대시보드_v9.5.en.html`: `display: flex; align-items:flex-start; gap:12px; padding: 13px 14px; border-radi`
- `v10_의료진웹/의료진_대시보드_v9.5.html`: `display: flex; align-items:flex-start; gap:12px; padding: 13px 14px; border-radi`

**버전 2** (2개 파일):
- `v10_의료진웹/의료진_대시보드_v9.5.en.html`: `background: var(--surface-warm);`
- `v10_의료진웹/의료진_대시보드_v9.5.html`: `background: var(--surface-warm);`

**버전 3** (2개 파일):
- `v10_의료진웹/의료진_대시보드_v9.5.en.html`: `background: var(--surface);`
- `v10_의료진웹/의료진_대시보드_v9.5.html`: `background: var(--surface);`

**버전 4** (2개 파일):
- `v10_의료진웹/의료진_대시보드_v9.5.en.html`: `background: var(--surface-soft);`
- `v10_의료진웹/의료진_대시보드_v9.5.html`: `background: var(--surface-soft);`

### `.cl-row` — 8개 파일, 4개 다른 사양

**버전 1** (2개 파일):
- `v10_의료진웹/의료진_대시보드_v9.5.en.html`: `display: grid; grid-template-columns: 40px 180px 1fr 110px 80px 110px; gap: 12px`
- `v10_의료진웹/의료진_대시보드_v9.5.html`: `display: grid; grid-template-columns: 40px 180px 1fr 110px 80px 110px; gap: 12px`

**버전 2** (2개 파일):
- `v10_의료진웹/의료진_대시보드_v9.5.en.html`: `padding-top: 12px; padding-bottom: 12px; border-bottom: 1px solid var(--surface)`
- `v10_의료진웹/의료진_대시보드_v9.5.html`: `padding-top: 12px; padding-bottom: 12px; border-bottom: 1px solid var(--surface)`

**버전 3** (2개 파일):
- `v10_의료진웹/의료진_대시보드_v9.5.en.html`: `background: var(--surface-warm);`
- `v10_의료진웹/의료진_대시보드_v9.5.html`: `background: var(--surface-warm);`

**버전 4** (2개 파일):
- `v10_의료진웹/의료진_대시보드_v9.5.en.html`: `border-bottom: none;`
- `v10_의료진웹/의료진_대시보드_v9.5.html`: `border-bottom: none;`

### `.pt-row` — 8개 파일, 4개 다른 사양

**버전 1** (2개 파일):
- `v10_의료진웹/의료진_대시보드_v9.5.en.html`: `display: grid; grid-template-columns: 210px 108px 1fr 145px 84px 108px; gap: 14p`
- `v10_의료진웹/의료진_대시보드_v9.5.html`: `display: grid; grid-template-columns: 210px 108px 1fr 145px 84px 108px; gap: 14p`

**버전 2** (2개 파일):
- `v10_의료진웹/의료진_대시보드_v9.5.en.html`: `padding-top: 13px; padding-bottom: 13px; border-bottom: 1px solid var(--surface)`
- `v10_의료진웹/의료진_대시보드_v9.5.html`: `padding-top: 13px; padding-bottom: 13px; border-bottom: 1px solid var(--surface)`

**버전 3** (2개 파일):
- `v10_의료진웹/의료진_대시보드_v9.5.en.html`: `background: var(--surface-warm);`
- `v10_의료진웹/의료진_대시보드_v9.5.html`: `background: var(--surface-warm);`

**버전 4** (2개 파일):
- `v10_의료진웹/의료진_대시보드_v9.5.en.html`: `border-bottom: none;`
- `v10_의료진웹/의료진_대시보드_v9.5.html`: `border-bottom: none;`

### `.ho-row` — 8개 파일, 4개 다른 사양

**버전 1** (2개 파일):
- `v10_의료진웹/의료진_대시보드_v9.5.en.html`: `display: grid; grid-template-columns: 200px 1fr 96px 110px 96px; gap: 12px; alig`
- `v10_의료진웹/의료진_대시보드_v9.5.html`: `display: grid; grid-template-columns: 200px 1fr 96px 110px 96px; gap: 12px; alig`

**버전 2** (2개 파일):
- `v10_의료진웹/의료진_대시보드_v9.5.en.html`: `padding-top: 16px; padding-bottom: 16px; border-bottom: 1px solid var(--surface)`
- `v10_의료진웹/의료진_대시보드_v9.5.html`: `padding-top: 16px; padding-bottom: 16px; border-bottom: 1px solid var(--surface)`

**버전 3** (2개 파일):
- `v10_의료진웹/의료진_대시보드_v9.5.en.html`: `background: var(--surface-warm);`
- `v10_의료진웹/의료진_대시보드_v9.5.html`: `background: var(--surface-warm);`

**버전 4** (2개 파일):
- `v10_의료진웹/의료진_대시보드_v9.5.en.html`: `border-bottom: none;`
- `v10_의료진웹/의료진_대시보드_v9.5.html`: `border-bottom: none;`

### `.rec-row` — 8개 파일, 4개 다른 사양

**버전 1** (2개 파일):
- `v10_의료진웹/의료진_대시보드_v9.5.en.html`: `display: grid; grid-template-columns: 200px 1fr 110px 110px 90px 144px; gap: 12p`
- `v10_의료진웹/의료진_대시보드_v9.5.html`: `display: grid; grid-template-columns: 200px 1fr 110px 110px 90px 144px; gap: 12p`

**버전 2** (2개 파일):
- `v10_의료진웹/의료진_대시보드_v9.5.en.html`: `padding-top: 13px; padding-bottom: 13px; border-bottom: 1px solid var(--surface)`
- `v10_의료진웹/의료진_대시보드_v9.5.html`: `padding-top: 13px; padding-bottom: 13px; border-bottom: 1px solid var(--surface)`

**버전 3** (2개 파일):
- `v10_의료진웹/의료진_대시보드_v9.5.en.html`: `background: var(--surface-warm);`
- `v10_의료진웹/의료진_대시보드_v9.5.html`: `background: var(--surface-warm);`

**버전 4** (2개 파일):
- `v10_의료진웹/의료진_대시보드_v9.5.en.html`: `border-bottom: none;`
- `v10_의료진웹/의료진_대시보드_v9.5.html`: `border-bottom: none;`

### `.sidebar-facility` — 8개 파일, 3개 다른 사양

**버전 1** (2개 파일):
- `v10_의료진웹/의료진_대시보드_v9.5.en.html`: `margin: 10px 12px 4px; padding: 8px 12px; background: rgba(255,255,255,.04); bor`
- `v10_의료진웹/의료진_대시보드_v9.5.html`: `margin: 10px 12px 4px; padding: 8px 12px; background: rgba(255,255,255,.04); bor`

**버전 2** (4개 파일):
- `v10_의료진웹/의료진_대시보드_v9.5.en.html`: `border: 0 !important;`
- `v10_의료진웹/의료진_대시보드_v9.5.en.html`: `border: 0 !important;`
- `v10_의료진웹/의료진_대시보드_v9.5.html`: `border: 0 !important;`
- `v10_의료진웹/의료진_대시보드_v9.5.html`: `border: 0 !important;`

**버전 3** (2개 파일):
- `v10_의료진웹/의료진_대시보드_v9.5.en.html`: `background: rgba(255,255,255,.04) !important; box-shadow: none !important; borde`
- `v10_의료진웹/의료진_대시보드_v9.5.html`: `background: rgba(255,255,255,.04) !important; box-shadow: none !important; borde`

### `.bottom-scrim` — 8개 파일, 2개 다른 사양

**버전 1** (4개 파일):
- `v11_보호자앱/common.css`: `position:fixed;left:0;right:0;bottom:0;height:108px;z-index:39;pointer-events:no`
- `v11_보호자앱/styles/g-guardian-live-part-2.css`: `position:fixed;left:0;right:0;bottom:0;height:108px;z-index:39;pointer-events:no`
- `v11_요양보호사앱/caregiver.css`: `position:fixed;left:0;right:0;bottom:0;height:108px;z-index:39;pointer-events:no`
- `v15_의료진앱/_shared.css`: `position:fixed;left:0;right:0;bottom:0;height:108px;z-index:39;pointer-events:no`

**버전 2** (4개 파일):
- `v11_보호자앱/common.css`: `backdrop-filter:none;-webkit-backdrop-filter:none`
- `v11_보호자앱/styles/g-guardian-live-part-2.css`: `backdrop-filter:none;-webkit-backdrop-filter:none`
- `v11_요양보호사앱/caregiver.css`: `backdrop-filter:none;-webkit-backdrop-filter:none`
- `v15_의료진앱/_shared.css`: `backdrop-filter:none;-webkit-backdrop-filter:none`

### `.opt` — 7개 파일, 5개 다른 사양

**버전 1** (1개 파일):
- `v11_보호자앱/_prescription-card-options.html`: `background:var(--color-bg-surface);border-radius:18px;padding:16px 16px 18px;box`

**버전 2** (2개 파일):
- `v11_요양보호사앱/c02-checklist.en.html`: `padding: 11px 6px; background: rgba(255,255,255,.82); border: 1px solid transpar`
- `v11_요양보호사앱/styles/c02-checklist.css`: `padding: 11px 6px; background: rgba(255,255,255,.82); border: 1px solid transpar`

**버전 3** (2개 파일):
- `v11_요양보호사앱/c02-checklist.en.html`: `transform: scale(.97);`
- `v11_요양보호사앱/styles/c02-checklist.css`: `transform: scale(.97);`

**버전 4** (1개 파일):
- `v12_환자앱/p11-settings.html`: `display: flex; align-items: center; gap: var(--space-5); min-height: 88px; paddi`

**버전 5** (1개 파일):
- `v12_환자앱/p11-settings.html`: `transform: scale(0.99);`

### `.sheet` — 7개 파일, 5개 다른 사양

**버전 1** (1개 파일):
- `v11_보호자앱/common.css`: `background: var(--surface); border-radius: var(--radius-lg) var(--radius-lg) 0 0`

**버전 2** (3개 파일):
- `v11_요양보호사앱/c01-today.en.html`: `background: rgba(250,253,251,.94); backdrop-filter: blur(60px) saturate(140%); -`
- `v11_요양보호사앱/c01-today.html`: `background: rgba(250,253,251,.94); backdrop-filter: blur(60px) saturate(140%); -`
- `v11_요양보호사앱/c01-today.zh.html`: `background: rgba(250,253,251,.94); backdrop-filter: blur(60px) saturate(140%); -`

**버전 3** (1개 파일):
- `v11_요양보호사앱/styles/c03-sotong.css`: `background: var(--color-bg-surface); border-top: .5px solid var(--color-border-s`

**버전 4** (1개 파일):
- `v15_의료진앱/styles/d03-inbox.css`: `background:var(--palette-white);border-radius:28px 28px 0 0; padding:22px 24px c`

**버전 5** (1개 파일):
- `v15_의료진앱/styles/d02-round.css`: `background:var(--palette-white);border-radius:28px 28px 0 0; padding:18px 18px c`

### `.overlay` — 7개 파일, 4개 다른 사양

**버전 1** (1개 파일):
- `v11_보호자앱/common.css`: `position: fixed; inset: 0; background: rgba(0, 0, 0, 0.4); z-index: var(--z-over`

**버전 2** (3개 파일):
- `v11_요양보호사앱/c01-today.en.html`: `position: fixed; inset: 0; background: rgba(0,0,0,.36); backdrop-filter: blur(10`
- `v11_요양보호사앱/c01-today.html`: `position: fixed; inset: 0; background: rgba(0,0,0,.36); backdrop-filter: blur(10`
- `v11_요양보호사앱/c01-today.zh.html`: `position: fixed; inset: 0; background: rgba(0,0,0,.36); backdrop-filter: blur(10`

**버전 3** (1개 파일):
- `v11_요양보호사앱/styles/c03-sotong.css`: `position: fixed; inset: 0; z-index: 200; background: rgba(0,0,0,.28); backdrop-f`

**버전 4** (2개 파일):
- `v15_의료진앱/styles/d03-inbox.css`: `position:fixed;inset:0;background:rgba(0,0,0,.4); backdrop-filter:blur(10px);-we`
- `v15_의료진앱/styles/d02-round.css`: `position:fixed;inset:0;background:rgba(0,0,0,.4); backdrop-filter:blur(10px);-we`
