# 컴포넌트 정의 다이버전스 리포트

실행 일시: 2026-05-23 19:19:57

## 의미

같은 CSS 클래스명이 여러 화면에서 **서로 다른 사양**으로 정의된 경우.
디자인 시스템 원칙상 컴포넌트는 한 곳(system/components.css)에서 정의되어야 한다.
화면별 로컬 정의는 의도된 변형이 아닌 한 통일 대상.

## 총 발견: 368개 클래스

정규화: 공백·순서·var() 폴백 hex 무시. 그래도 다른 값이면 다이버전스로 판단.

| 클래스 | 정의 파일 수 | 다른 사양 수 |
|---|---:|---:|
| `.header` | 12 | 7 |
| `.toast` | 12 | 6 |
| `.nav-btn` | 11 | 7 |
| `.main` | 10 | 10 |
| `.msg-item` | 10 | 9 |
| `.msg-time` | 9 | 6 |
| `.tl-item` | 8 | 8 |
| `.fam-icon-btn` | 8 | 7 |
| `.chip` | 7 | 7 |
| `.tl-now-strip` | 6 | 6 |
| `.quick-btn` | 6 | 6 |
| `.help-btn` | 6 | 6 |
| `.actions` | 6 | 5 |
| `.sec-label` | 6 | 5 |
| `.a-btn` | 6 | 5 |
| `.input-field` | 6 | 3 |
| `.btn-back` | 6 | 2 |
| `.messages` | 6 | 2 |
| `.switch` | 6 | 2 |
| `.card` | 5 | 5 |
| `.cp-ai-act` | 5 | 5 |
| `.ho-manual-open` | 5 | 5 |
| `.summary-bar` | 5 | 5 |
| `.tl-month` | 5 | 5 |
| `.fam-row` | 5 | 5 |
| `.icon-btn` | 5 | 4 |
| `.msg` | 5 | 3 |
| `.sec` | 5 | 3 |
| `.tabbar` | 5 | 2 |
| `.sos` | 5 | 2 |
| `.timeline` | 4 | 4 |
| `.search-input` | 4 | 4 |
| `.ph-item` | 4 | 4 |
| `.al-item` | 4 | 4 |
| `.med-row` | 4 | 4 |
| `.cl-row` | 4 | 4 |
| `.pt-row` | 4 | 4 |
| `.ho-row` | 4 | 4 |
| `.rec-row` | 4 | 4 |
| `.ai-orb` | 4 | 4 |
| `.logo` | 4 | 4 |
| `.moment-card` | 4 | 4 |
| `.sch-item` | 4 | 4 |
| `.msg-bubble` | 4 | 4 |
| `.menu-item` | 4 | 4 |
| `.hero` | 4 | 4 |
| `.sheet` | 4 | 4 |
| `.opt` | 4 | 4 |
| `.tx` | 4 | 4 |
| `.cancel-big` | 4 | 4 |
| `.todo-list` | 4 | 4 |
| `.sidebar-facility` | 4 | 3 |
| `.sec-head` | 4 | 3 |
| `.unread-line` | 4 | 3 |
| `.filter-row` | 4 | 3 |
| `.av` | 4 | 3 |
| `.msg-body` | 4 | 3 |
| `.overlay` | 4 | 3 |
| `.bubble` | 4 | 2 |
| `.msg-read` | 4 | 2 |
| `.gps-pulse` | 4 | 2 |
| `.sec-ttl` | 4 | 2 |
| `.row` | 4 | 2 |
| `.topbar` | 3 | 3 |
| `.sidebar` | 3 | 3 |
| `.nav-item` | 3 | 3 |
| `.btn` | 3 | 3 |
| `.btn-primary` | 3 | 3 |
| `.section-title` | 3 | 3 |
| `.timeline__row` | 3 | 3 |
| `.page-date` | 3 | 3 |
| `.sos-btn` | 3 | 3 |
| `.content` | 3 | 3 |
| `.priority-hero` | 3 | 3 |
| `.kpi-bar` | 3 | 3 |
| `.tl-wrap` | 3 | 3 |
| `.tl-line` | 3 | 3 |
| `.cp-body` | 3 | 3 |
| `.af-item` | 3 | 3 |
| `.cp-ai-intro` | 3 | 3 |
| `.cp-msg-list` | 3 | 3 |
| `.pt-qs-track` | 3 | 3 |
| `.ho-hero-stat` | 3 | 3 |
| `.memo-save` | 3 | 3 |
| `.ai-placeholder` | 3 | 3 |
| `.ai-fab` | 3 | 3 |
| `.chat-messages` | 3 | 3 |
| `.voice` | 3 | 3 |
| `.tl` | 3 | 3 |
| `.logout` | 3 | 3 |
| `.sch-day` | 3 | 3 |
| `.obs-card` | 3 | 3 |
| `.roster-wrap` | 3 | 3 |
| `.roster-row` | 3 | 3 |
| `.act-card` | 3 | 3 |
| `.sos-fab` | 3 | 3 |
| `.p-settings-quick` | 3 | 3 |
| `.quick-chip` | 3 | 3 |
| `.fam-icon-btn--primary` | 3 | 3 |
| `.now-action` | 3 | 3 |
| `.fn-schedule` | 3 | 3 |
| `.help-grid-routine` | 3 | 3 |
| `.home-btn` | 3 | 3 |
| `.stage` | 3 | 3 |
| `.action` | 3 | 3 |
| `.role-card` | 3 | 3 |
| `.swipe-next` | 3 | 3 |
| `.alert-icon-wrap` | 3 | 3 |
| `.info-row` | 3 | 3 |
| `.sec-head__title` | 3 | 2 |
| `.msg-sender` | 3 | 2 |
| `.input-bar` | 3 | 2 |
| `.msg-name-row` | 3 | 2 |
| `.msg-name` | 3 | 2 |
| `.msg-preview` | 3 | 2 |
| `.msg-meta` | 3 | 2 |
| `.msg-badge` | 3 | 2 |
| `.voice-prev-q` | 3 | 2 |
| `.page-title` | 2 | 2 |
| `.btn-secondary` | 2 | 2 |
| `.side-panel__close` | 2 | 2 |
| `.sidebar-logo` | 2 | 2 |
| `.logo-icon` | 2 | 2 |
| `.logo-name` | 2 | 2 |
| `.logo-sub` | 2 | 2 |
| `.facility-dot` | 2 | 2 |
| `.facility-name` | 2 | 2 |
| `.nav-section-label` | 2 | 2 |
| `.nav-list` | 2 | 2 |
| `.nav-link` | 2 | 2 |
| `.nav-icon` | 2 | 2 |
| `.sidebar-user` | 2 | 2 |
| `.user-avatar` | 2 | 2 |
| `.user-name` | 2 | 2 |
| `.user-role` | 2 | 2 |
| `.main-wrapper` | 2 | 2 |
| `.greet-pill` | 2 | 2 |
| `.ph-all` | 2 | 2 |
| `.ph-time` | 2 | 2 |
| `.ph-btn` | 2 | 2 |
| `.kpi` | 2 | 2 |
| `.kpi-sub` | 2 | 2 |
| `.kpi-chip` | 2 | 2 |
| `.kpi-value` | 2 | 2 |
| `.kpi-denom` | 2 | 2 |
| `.kpi-fill` | 2 | 2 |
| `.kpi-badge` | 2 | 2 |
| `.kpi-name-chip` | 2 | 2 |
| `.kpi-name-chip-room` | 2 | 2 |
| `.card-head` | 2 | 2 |
| `.tl-live-dot` | 2 | 2 |
| `.tl-time-col` | 2 | 2 |
| `.tl-name` | 2 | 2 |
| `.tl-desc` | 2 | 2 |
| `.al-btn` | 2 | 2 |
| `.ai-badge` | 2 | 2 |
| `.focus-btn` | 2 | 2 |
| `.chat-row` | 2 | 2 |
| `.chat-av` | 2 | 2 |
| `.chat-name` | 2 | 2 |
| `.chat-time` | 2 | 2 |
| `.af-badge` | 2 | 2 |
| `.cp-ai-sub` | 2 | 2 |
| `.cp-ai-item` | 2 | 2 |
| `.cp-ai-item-head` | 2 | 2 |
| `.cp-ai-item-pt` | 2 | 2 |
| `.cp-ai-item-body` | 2 | 2 |
| `.cp-ai-ask-row` | 2 | 2 |
| `.cp-input-row` | 2 | 2 |
| `.cp-input` | 2 | 2 |
| `.cp-convo-input` | 2 | 2 |
| `.med-name` | 2 | 2 |
| `.med-tl-pt` | 2 | 2 |
| `.med-tl-track` | 2 | 2 |
| `.med-tl-block` | 2 | 2 |
| `.cl-group-head` | 2 | 2 |
| `.pt-room` | 2 | 2 |
| `.pt-qs-item` | 2 | 2 |
| `.pt-qs-more` | 2 | 2 |
| `.pt-act` | 2 | 2 |
| `.pt-more` | 2 | 2 |
| `.week-day` | 2 | 2 |
| `.sch-nf-btn` | 2 | 2 |
| `.sb` | 2 | 2 |
| `.ho-pri` | 2 | 2 |
| `.rec-alert-btn` | 2 | 2 |
| `.rec-tl-mk-lbl` | 2 | 2 |
| `.rec-tl-now` | 2 | 2 |
| `.rec-gauge-cell` | 2 | 2 |
| `.rec-gauge-ring` | 2 | 2 |
| `.rec-hero-missing-item` | 2 | 2 |
| `.rec-aiq-item` | 2 | 2 |
| `.rec-aiq-gen-btn` | 2 | 2 |
| `.rec-aiq-bulk` | 2 | 2 |
| `.ho-tl-now` | 2 | 2 |
| `.ho-tl-now-lbl` | 2 | 2 |
| `.ho-tm-block` | 2 | 2 |
| `.ho-tm-action` | 2 | 2 |
| `.cl-don-cell` | 2 | 2 |
| `.cl-don-ring` | 2 | 2 |
| `.cl-tl-evt` | 2 | 2 |
| `.my-row` | 2 | 2 |
| `.my-toggle` | 2 | 2 |
| `.memo-panel__close` | 2 | 2 |
| `.memo-card__delete` | 2 | 2 |
| `.cat-row` | 2 | 2 |
| `.nurse-av` | 2 | 2 |
| `.header-btn` | 2 | 2 |
| `.duty-av` | 2 | 2 |
| `.duty-badge` | 2 | 2 |
| `.chat-item` | 2 | 2 |
| `.ai-orb-bg` | 2 | 2 |
| `.intro` | 2 | 2 |
| `.intro-text` | 2 | 2 |
| `.intro-ring-progress` | 2 | 2 |
| `.intro-skip` | 2 | 2 |
| `.ch-icon-btn` | 2 | 2 |
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
| `.grid` | 2 | 2 |
| `.grid-full` | 2 | 2 |
| `.w` | 2 | 2 |
| `.w-dot` | 2 | 2 |
| `.sleep-ticks` | 2 | 2 |
| `.w-head` | 2 | 2 |
| `.w-title` | 2 | 2 |
| `.insight-card` | 2 | 2 |
| `.quick-scroll` | 2 | 2 |
| `.quick-icon` | 2 | 2 |
| `.quick-label` | 2 | 2 |
| `.unread-divider` | 2 | 2 |
| `.chat-input` | 2 | 2 |
| `.voice-bar` | 2 | 2 |
| `.summary-bar__dot` | 2 | 2 |
| `.summary-bar__text` | 2 | 2 |
| `.av--nurse` | 2 | 2 |
| `.page-sub` | 2 | 2 |
| `.sched-scroll` | 2 | 2 |
| `.sched-chip` | 2 | 2 |
| `.feed-card` | 2 | 2 |
| `.insight-item` | 2 | 2 |
| `.cta-row` | 2 | 2 |
| `.mode-bar` | 2 | 2 |
| `.action-btn` | 2 | 2 |
| `.qq` | 2 | 2 |
| `.input-mic` | 2 | 2 |
| `.profile` | 2 | 2 |
| `.qr-btn` | 2 | 2 |
| `.care-row` | 2 | 2 |
| `.menu-title` | 2 | 2 |
| `.menu-group` | 2 | 2 |
| `.mi-icon` | 2 | 2 |
| `.mi-body` | 2 | 2 |
| `.mi-label` | 2 | 2 |
| `.mi-desc` | 2 | 2 |
| `.live-dock__primary` | 2 | 2 |
| `.sd-now` | 2 | 2 |
| `.sh-btn` | 2 | 2 |
| `.hero-wrap` | 2 | 2 |
| `.hero-more` | 2 | 2 |
| `.handover-wrap` | 2 | 2 |
| `.obs-call-mini` | 2 | 2 |
| `.sheet-row-label` | 2 | 2 |
| `.sheet-row-val` | 2 | 2 |
| `.h-title` | 2 | 2 |
| `.profile-hero` | 2 | 2 |
| `.pf-top` | 2 | 2 |
| `.pf-ava` | 2 | 2 |
| `.pf-name` | 2 | 2 |
| `.pf-stats` | 2 | 2 |
| `.pf-stat` | 2 | 2 |
| `.gps` | 2 | 2 |
| `.rows` | 2 | 2 |
| `.lq` | 2 | 2 |
| `.back-btn` | 2 | 2 |
| `.now-row` | 2 | 2 |
| `.now-card-cta` | 2 | 2 |
| `.pt-row-c` | 2 | 2 |
| `.grid8` | 2 | 2 |
| `.g-card` | 2 | 2 |
| `.dots` | 2 | 2 |
| `.dot` | 2 | 2 |
| `.v-field` | 2 | 2 |
| `.chk` | 2 | 2 |
| `.btn-prev` | 2 | 2 |
| `.bs-pt` | 2 | 2 |
| `.bs-pt-c` | 2 | 2 |
| `.bs-f` | 2 | 2 |
| `.bs-btn` | 2 | 2 |
| `.hc` | 2 | 2 |
| `.act-cta` | 2 | 2 |
| `.pick-row` | 2 | 2 |
| `.b-text` | 2 | 2 |
| `.b-text--live` | 2 | 2 |
| `.listen-status` | 2 | 2 |
| `.opt__toggle` | 2 | 2 |
| `.msg-av` | 2 | 2 |
| `.msg-photos` | 2 | 2 |
| `.voice-btn` | 2 | 2 |
| `.fam-quick-more` | 2 | 2 |
| `.fam-row-meta` | 2 | 2 |
| `.fam-row-status` | 2 | 2 |
| `.fam-row-actions` | 2 | 2 |
| `.now-confirm` | 2 | 2 |
| `.cf-btn` | 2 | 2 |
| `.cf-btn--ghost` | 2 | 2 |
| `.screens` | 2 | 2 |
| `.screen-card` | 2 | 2 |
| `.help-grid-special` | 2 | 2 |
| `.help-btn--brand` | 2 | 2 |
| `.help-btn--urgent` | 2 | 2 |
| `.help-family` | 2 | 2 |
| `.count-card` | 2 | 2 |
| `.count-ring` | 2 | 2 |
| `.count-text` | 2 | 2 |
| `.quick-row` | 2 | 2 |
| `.progress` | 2 | 2 |
| `.progress-bar` | 2 | 2 |
| `.progress-fill` | 2 | 2 |
| `.todo-item` | 2 | 2 |
| `.todo-time` | 2 | 2 |
| `.todo-name` | 2 | 2 |
| `.todo-sub` | 2 | 2 |
| `.todo-status` | 2 | 2 |
| `.done-mark` | 2 | 2 |
| `.cards` | 2 | 2 |
| `.call-cols` | 2 | 2 |
| `.call-panel` | 2 | 2 |
| `.fam-row-name` | 2 | 2 |
| `.tl-day` | 2 | 2 |
| `.tl-item--unread` | 2 | 2 |
| `.bottom` | 2 | 2 |
| `.caption` | 2 | 2 |
| `.or-row` | 2 | 2 |
| `.input-ttl` | 2 | 2 |
| `.swipe-skip` | 2 | 2 |
| `.pl-item` | 2 | 2 |
| `.intro-btn-primary` | 2 | 2 |
| `.intro-hist-row` | 2 | 2 |
| `.ja-opt` | 2 | 2 |
| `.alert-sub` | 2 | 2 |
| `.alert-cta` | 2 | 2 |
| `.compose-send` | 2 | 2 |
| `.sbar-row` | 2 | 2 |
| `.sbar-kv` | 2 | 2 |
| `.check-row` | 2 | 2 |
| `.conf-overlay` | 2 | 2 |
| `.conf-sheet` | 2 | 2 |
| `.conf-eyebrow` | 2 | 2 |
| `.conf-ttl` | 2 | 2 |
| `.conf-sub` | 2 | 2 |
| `.conf-cancel` | 2 | 2 |
| `.action-primary` | 2 | 2 |
| `.action-secondary` | 2 | 2 |
| `.conf-opt` | 2 | 2 |
| `.conf-action-danger` | 2 | 2 |

## 상세 (상위 30개)

### `.header` — 12개 파일, 7개 다른 사양

**버전 1** (2개 파일):
- `v11_보호자앱/g03-chat-nurse.html`: `position:sticky;top:0;z-index:30;display:flex;align-items:center;gap:12px;paddin`
- `v11_보호자앱/g03-chat-patient.html`: `position:sticky;top:0;z-index:30;display:flex;align-items:center;gap:12px;paddin`

**버전 2** (1개 파일):
- `v11_보호자앱/g03-chat.html`: `position:sticky;top:0;z-index:30;padding:calc(env(safe-area-inset-top,0px) + 8px`

**버전 3** (1개 파일):
- `v11_보호자앱/g-guardian-live.html`: `padding:calc(env(safe-area-inset-top,0px) + 6px) 20px 0;position:static;backgrou`

**버전 4** (1개 파일):
- `v11_보호자앱/g03-chat-ai.html`: `position:sticky;top:0;z-index:30;display:flex;align-items:center;gap:12px;paddin`

**버전 5** (1개 파일):
- `v11_요양보호사앱/c01-today.html`: `position: static; padding: calc(var(--safe-t) + 6px) var(--page-pad) 0; backgrou`

**버전 6** (3개 파일):
- `v11_요양보호사앱/c03-sotong.html`: `padding:calc(var(--safe-t) + 6px) var(--page-pad) 0;position:static;`
- `v15_의료진앱/d01-home.html`: `padding:calc(var(--safe-t) + 6px) var(--page-pad) 0; position:static;`
- `v15_의료진앱/d03-inbox.html`: `padding:calc(var(--safe-t) + 6px) var(--page-pad) 0; position:static;`

**버전 7** (3개 파일):
- `v15_의료진앱/d02-round.html`: `padding:calc(var(--safe-t) + 14px) var(--pad) 8px; position:relative;z-index:5;`
- `v15_의료진앱/d04-handover.html`: `padding:calc(var(--safe-t) + 14px) var(--pad) 8px;position:relative;z-index:5;`
- `v15_의료진앱/d05-mypage.html`: `padding:calc(var(--safe-t) + 14px) var(--pad) 8px;position:relative;z-index:5;`

### `.toast` — 12개 파일, 6개 다른 사양

**버전 1** (1개 파일):
- `v11_보호자앱/g-guardian-live.html`: `position:fixed;top:80px;left:50%;transform:translateX(-50%) translateY(-8px);bac`

**버전 2** (2개 파일):
- `v11_요양보호사앱/c04-schedule.html`: `position: fixed; top: 80px; left: 50%; transform: translateX(-50%) translateY(-8`
- `v11_요양보호사앱/c03-sotong.html`: `position: fixed; top: 80px; left: 50%; transform: translateX(-50%) translateY(-8`

**버전 3** (1개 파일):
- `v11_요양보호사앱/c01-today.html`: `position: fixed; left: 50%; bottom: calc(var(--safe-b) + var(--tab-h) + var(--ta`

**버전 4** (6개 파일):
- `v11_요양보호사앱/c04-mypage.html`: `position:fixed;left:50%;bottom:calc(var(--safe-b) + var(--tab-h) + var(--tab-bot`
- `v15_의료진앱/d02-round.html`: `position:fixed;left:50%;bottom:calc(var(--safe-b) + var(--tab-h) + var(--tab-bot`
- `v15_의료진앱/d01-home.html`: `position:fixed;left:50%;bottom:calc(var(--safe-b) + var(--tab-h) + var(--tab-bot`
- `v15_의료진앱/d03-inbox.html`: `position:fixed;left:50%;bottom:calc(var(--safe-b) + var(--tab-h) + var(--tab-bot`
- `v15_의료진앱/d04-handover.html`: `position:fixed;left:50%;bottom:calc(var(--safe-b) + var(--tab-h) + var(--tab-bot`
- … 외 1개

**버전 5** (1개 파일):
- `v11_요양보호사앱/c02-checklist.html`: `position: fixed; top: 72px; left: 50%; transform: translateX(-50%) translateY(-8`

**버전 6** (1개 파일):
- `v15_의료진앱/d-sos.html`: `position:fixed;left:50%;bottom:calc(var(--safe-b) + 110px); transform:translateX`

### `.nav-btn` — 11개 파일, 7개 다른 사양

**버전 1** (3개 파일):
- `v11_보호자앱/g03-chat-nurse.html`: `width:36px;height:36px;border-radius:50%;background:rgba(255,255,255,.6);border:`
- `v11_보호자앱/g03-chat-patient.html`: `width:36px;height:36px;border-radius:50%;background:rgba(255,255,255,.6);border:`
- `v11_보호자앱/g03-chat-ai.html`: `width:36px;height:36px;border-radius:50%;background:rgba(255,255,255,.6);border:`

**버전 2** (3개 파일):
- `v11_보호자앱/g03-chat-nurse.html`: `transform:scale(.93)`
- `v11_보호자앱/g03-chat-patient.html`: `transform:scale(.93)`
- `v11_보호자앱/g03-chat-ai.html`: `transform:scale(.93)`

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

### `.main` — 10개 파일, 10개 다른 사양

**버전 1** (1개 파일):
- `v10_의료진웹/m02-patient-side-panel.html`: `padding: var(--space-7); max-width: var(--size-content-max); margin: 0 auto; tra`

**버전 2** (1개 파일):
- `v12_환자앱/p05-voice.html`: `flex: 1; display: grid; grid-template-rows: 1fr auto auto; gap: var(--space-6); `

**버전 3** (1개 파일):
- `v12_환자앱/p01-today.html`: `flex: 1; display: grid; grid-template-columns: 7fr 3fr; gap: 16px; min-height: 0`

**버전 4** (1개 파일):
- `v12_환자앱/p08-help.html`: `flex: 1; display: flex; flex-direction: column; gap: var(--space-4); min-height:`

**버전 5** (1개 파일):
- `v12_환자앱/p09-sos.html`: `flex: 1; display: flex; flex-direction: column; align-items: center; justify-con`

**버전 6** (1개 파일):
- `v12_환자앱/p02-med-alert.html`: `flex: 1; display: flex; flex-direction: column; gap: var(--space-5); min-height:`

**버전 7** (1개 파일):
- `v12_환자앱/p10-med-done.html`: `flex: 1; display: flex; flex-direction: column; align-items: center; gap: var(--`

**버전 8** (1개 파일):
- `v12_환자앱/p03-call.html`: `flex: 1; display: flex; flex-direction: column; gap: 18px; min-height: 0;`

**버전 9** (1개 파일):
- `v12_환자앱/p07-message.html`: `flex: 1; display: grid; grid-template-rows: auto 1fr auto auto; gap: var(--space`

**버전 10** (1개 파일):
- `v12_환자앱/p06-photo.html`: `flex: 1; display: grid; grid-template-columns: 1fr; grid-template-rows: auto 1fr`

### `.msg-item` — 10개 파일, 9개 다른 사양

**버전 1** (1개 파일):
- `v11_보호자앱/g03-sotong.html`: `display: flex; align-items: center; gap: var(--space-4); padding: var(--space-4)`

**버전 2** (2개 파일):
- `v11_보호자앱/g03-sotong.html`: `transform: scale(0.98);`
- `v11_요양보호사앱/c03-sotong.html`: `transform: scale(0.98);`

**버전 3** (1개 파일):
- `v11_보호자앱/g03-sotong.html`: `animation: haru-fade-in-up var(--motion-enter) var(--easing-standard) both;`

**버전 4** (1개 파일):
- `v11_보호자앱/g03-sotong.html`: `animation: none !important;`

**버전 5** (1개 파일):
- `v11_요양보호사앱/c03-sotong.html`: `display: flex; align-items: center; gap: var(--space-4); padding: var(--space-4)`

**버전 6** (1개 파일):
- `v15_의료진앱/d03-inbox.html`: `display:flex;align-items:center;gap:14px; padding:12px 16px; background:var(--pa`

**버전 7** (1개 파일):
- `v15_의료진앱/d03-inbox.html`: `transform:scale(.99);`

**버전 8** (1개 파일):
- `v15_의료진앱/d03-inbox.html`: `animation: haru-fade-in-up var(--duration-slow, 350ms) var(--easing-standard) bo`

**버전 9** (1개 파일):
- `v15_의료진앱/d03-inbox.html`: `animation:none !important;`

### `.msg-time` — 9개 파일, 6개 다른 사양

**버전 1** (3개 파일):
- `v11_보호자앱/g03-chat-nurse.html`: `font-size:10px;color:var(--t3);align-self:flex-end;flex-shrink:0;padding-bottom:`
- `v11_보호자앱/g03-chat-patient.html`: `font-size:10px;color:var(--t3);align-self:flex-end;flex-shrink:0;padding-bottom:`
- `v11_보호자앱/g03-chat-ai.html`: `font-size:10px;color:var(--t3);align-self:flex-end;flex-shrink:0;padding-bottom:`

**버전 2** (1개 파일):
- `v11_보호자앱/g03-chat-family.html`: `font-size: var(--text-mini); color: var(--text-tertiary); align-self: flex-end; `

**버전 3** (2개 파일):
- `v11_보호자앱/g03-sotong.html`: `font-size: var(--text-mini); color: var(--color-text-tertiary); font-weight: var`
- `v11_요양보호사앱/c03-sotong.html`: `font-size: var(--text-mini); color: var(--color-text-tertiary); font-weight: var`

**버전 4** (1개 파일):
- `v12_환자앱/p01-today.html`: `font-size: 18px; font-weight: 600; color: var(--patient-text-warm); margin-top: `

**버전 5** (1개 파일):
- `v12_환자앱/p07-message.html`: `font: var(--weight-medium) 14px / 1 var(--font-family-base); color: var(--color-`

**버전 6** (1개 파일):
- `v15_의료진앱/d03-inbox.html`: `font-size:11.5px;font-weight:500;color:var(--t3);`

### `.tl-item` — 8개 파일, 8개 다른 사양

**버전 1** (1개 파일):
- `v10_의료진웹/의료진_대시보드_v9.5.html`: `display: flex; gap: 0; position:relative; align-items:stretch;`

**버전 2** (1개 파일):
- `v11_보호자앱/g10-timeline.html`: `padding: 0; position: relative;`

**버전 3** (1개 파일):
- `v11_보호자앱/g10-timeline.html`: `content: ''; position: absolute; left: -22px; top: 18px; width: 10px; height: 10`

**버전 4** (1개 파일):
- `v11_보호자앱/g10-timeline.html`: `animation: haru-fade-in-up var(--motion-enter) var(--easing-standard) both;`

**버전 5** (1개 파일):
- `v11_보호자앱/g10-timeline.html`: `animation: none !important;`

**버전 6** (1개 파일):
- `v12_환자앱/p03-call.html`: `outline: 3px solid var(--brand-orange-500); outline-offset: 3px; border-radius: `

**버전 7** (1개 파일):
- `v12_환자앱/p03-call.html`: `display: grid; grid-template-columns: 48px 1fr; gap: 12px; align-items: start; p`

**버전 8** (1개 파일):
- `v12_환자앱/p03-call.html`: `background: rgba(255, 255, 255, 0.6);`

### `.fam-icon-btn` — 8개 파일, 7개 다른 사양

**버전 1** (1개 파일):
- `v12_환자앱/p01-today.html`: `width: 44px; height: 44px; border-radius: 50%; display: inline-flex; align-items`

**버전 2** (2개 파일):
- `v12_환자앱/p01-today.html`: `background: var(--brand-orange-100);`
- `v12_환자앱/p03-call.html`: `background: var(--brand-orange-100);`

**버전 3** (1개 파일):
- `v12_환자앱/p01-today.html`: `transform: scale(.92);`

**버전 4** (1개 파일):
- `v12_환자앱/p03-call.html`: `border-radius: 50%; outline-offset: 4px;`

**버전 5** (1개 파일):
- `v12_환자앱/p03-call.html`: `width: 60px; height: 60px; border-radius: 50%; display: inline-flex; align-items`

**버전 6** (1개 파일):
- `v12_환자앱/p03-call.html`: `transform: scale(.94);`

**버전 7** (1개 파일):
- `v12_환자앱/p03-call.html`: `width: 52px; height: 52px;`

### `.chip` — 7개 파일, 7개 다른 사양

**버전 1** (1개 파일):
- `v11_보호자앱/g03-chat-ai.html`: `display:flex;align-items:center;gap:5px;padding:7px 14px;border-radius:999px;fon`

**버전 2** (1개 파일):
- `v11_보호자앱/g03-chat-ai.html`: `transform:scale(.95)`

**버전 3** (1개 파일):
- `v12_환자앱/p07-message.html`: `padding: 14px 22px; border-radius: 999px; background: rgba(255, 255, 255, 0.9); `

**버전 4** (1개 파일):
- `v12_환자앱/p07-message.html`: `background: var(--brand-orange-100); color: var(--brand-orange-700);`

**버전 5** (1개 파일):
- `v12_환자앱/p07-message.html`: `transform: scale(.96);`

**버전 6** (1개 파일):
- `v12_환자앱/p07-message.html`: `font-size: 18px; padding: 12px 18px;`

**버전 7** (1개 파일):
- `v15_의료진앱/d03-inbox.html`: `flex-shrink:0; height:34px;padding:0 14px; border-radius:999px; background:rgba(`

### `.tl-now-strip` — 6개 파일, 6개 다른 사양

**버전 1** (1개 파일):
- `v10_의료진웹/의료진_대시보드_v9.5.html`: `display: flex; align-items:center; gap:8px; padding: 9px 14px; margin-bottom: 20`

**버전 2** (1개 파일):
- `v10_의료진웹/의료진_대시보드_v9.5.html`: `font-family: var(--font-mono), var(--font); font-feature-settings: 'tnum' 1, 'ze`

**버전 3** (1개 파일):
- `v10_의료진웹/의료진_대시보드_v9.5.html`: `font-family: var(--font) !important;`

**버전 4** (1개 파일):
- `v10_의료진웹/의료진_대시보드_v9.5.html`: `font-family: var(--font-mono), var(--font) !important;`

**버전 5** (1개 파일):
- `v10_의료진웹/의료진_대시보드_v9.5.html`: `position: relative;`

**버전 6** (1개 파일):
- `v10_의료진웹/의료진_대시보드_v9.5.html`: `content: 'LIVE'; margin-left: auto; font-size: 9px; font-weight: 800; letter-spa`

### `.quick-btn` — 6개 파일, 6개 다른 사양

**버전 1** (1개 파일):
- `v11_보호자앱/g-guardian-live.html`: `flex-shrink:0;display:flex;align-items:center;gap:8px;padding:12px 18px;border-r`

**버전 2** (1개 파일):
- `v11_보호자앱/g-guardian-live.html`: `transform:scale(.96)`

**버전 3** (1개 파일):
- `v11_보호자앱/g05-mypage.html`: `display: flex; flex-direction: column; align-items: center; gap: var(--space-2);`

**버전 4** (1개 파일):
- `v11_보호자앱/g05-mypage.html`: `transform: scale(0.97);`

**버전 5** (1개 파일):
- `v12_환자앱/p09-sos.html`: `height: 80px; border: 0; cursor: pointer; border-radius: 20px; display: flex; al`

**버전 6** (1개 파일):
- `v12_환자앱/p09-sos.html`: `transform: scale(.97);`

### `.help-btn` — 6개 파일, 6개 다른 사양

**버전 1** (1개 파일):
- `v12_환자앱/p01-today.html`: `flex-shrink: 0; height: 88px; border-radius: 22px; border: 0; cursor: pointer; d`

**버전 2** (1개 파일):
- `v12_환자앱/p01-today.html`: `transform: scale(.97); box-shadow: 0 5px 16px rgba(227, 43, 37,.3);`

**버전 3** (1개 파일):
- `v12_환자앱/p08-help.html`: `display: flex; flex-direction: column; align-items: center; justify-content: cen`

**버전 4** (1개 파일):
- `v12_환자앱/p08-help.html`: `transform: translateY(-3px); box-shadow: 0 10px 28px rgba(194, 98, 28, 0.15);`

**버전 5** (1개 파일):
- `v12_환자앱/p08-help.html`: `transform: scale(.97);`

**버전 6** (1개 파일):
- `v12_환자앱/p08-help.html`: `padding: var(--space-4); gap: 12px;`

### `.actions` — 6개 파일, 5개 다른 사양

**버전 1** (1개 파일):
- `v10_의료진웹/m02-patient-side-panel.html`: `display: flex; gap: var(--space-3); margin-bottom: var(--space-6);`

**버전 2** (2개 파일):
- `v12_환자앱/p05-voice.html`: `display: grid; grid-template-columns: 1fr 1fr; gap: var(--space-4);`
- `v12_환자앱/p07-message.html`: `display: grid; grid-template-columns: 1fr 1fr; gap: var(--space-4);`

**버전 3** (1개 파일):
- `v12_환자앱/p05-voice.html`: `grid-template-columns: 1fr;`

**버전 4** (1개 파일):
- `v12_환자앱/p09-sos.html`: `width: 100%; max-width: 720px; display: grid; grid-template-columns: 1fr; gap: v`

**버전 5** (1개 파일):
- `v15_의료진앱/d-sos.html`: `margin-top:auto;display:flex;flex-direction:column;gap:10px;`

### `.sec-label` — 6개 파일, 5개 다른 사양

**버전 1** (2개 파일):
- `v11_보호자앱/g03-sotong.html`: `display: flex; align-items: center; gap: var(--space-3); padding: var(--space-3)`
- `v11_요양보호사앱/c03-sotong.html`: `display: flex; align-items: center; gap: var(--space-3); padding: var(--space-3)`

**버전 2** (1개 파일):
- `v11_보호자앱/g03-sotong.html`: `animation: haru-fade-in-up var(--motion-enter) var(--easing-standard) both; anim`

**버전 3** (1개 파일):
- `v11_요양보호사앱/c03-sotong.html`: `animation-delay: 260ms;`

**버전 4** (1개 파일):
- `v15_의료진앱/d03-inbox.html`: `display:flex;align-items:center;gap:10px; padding:8px 4px 6px;cursor:pointer;`

**버전 5** (1개 파일):
- `v15_의료진앱/d03-inbox.html`: `animation-delay:120ms;`

### `.a-btn` — 6개 파일, 5개 다른 사양

**버전 1** (1개 파일):
- `v12_환자앱/p05-voice.html`: `height: 96px; border: 0; cursor: pointer; border-radius: 22px; display: flex; al`

**버전 2** (2개 파일):
- `v12_환자앱/p05-voice.html`: `transform: scale(.97);`
- `v12_환자앱/p07-message.html`: `transform: scale(.97);`

**버전 3** (1개 파일):
- `v12_환자앱/p05-voice.html`: `height: 76px; font-size: 20px;`

**버전 4** (1개 파일):
- `v12_환자앱/p07-message.html`: `height: 92px; border: 0; cursor: pointer; border-radius: 22px; display: flex; al`

**버전 5** (1개 파일):
- `v12_환자앱/p07-message.html`: `height: 72px; font-size: 20px;`

### `.input-field` — 6개 파일, 3개 다른 사양

**버전 1** (2개 파일):
- `v11_보호자앱/g03-chat-nurse.html`: `flex:1;height:100%;border:none;font-family:var(--font);font-size:15px;outline:no`
- `v11_보호자앱/g03-chat-patient.html`: `flex:1;height:100%;border:none;font-family:var(--font);font-size:15px;outline:no`

**버전 2** (3개 파일):
- `v11_보호자앱/g03-chat-nurse.html`: `color:rgba(28,28,30,.4)`
- `v11_보호자앱/g03-chat-patient.html`: `color:rgba(28,28,30,.4)`
- `v11_보호자앱/g03-chat-ai.html`: `color:rgba(28,28,30,.4)`

**버전 3** (1개 파일):
- `v11_보호자앱/g03-chat-ai.html`: `flex:1;height:38px;border:none;font-family:var(--font);font-size:15px;outline:no`

### `.btn-back` — 6개 파일, 2개 다른 사양

**버전 1** (3개 파일):
- `v11_보호자앱/g03-chat-nurse.html`: `width:36px;height:36px;border-radius:50%;background:rgba(255,255,255,.6);border:`
- `v11_보호자앱/g03-chat-patient.html`: `width:36px;height:36px;border-radius:50%;background:rgba(255,255,255,.6);border:`
- `v11_보호자앱/g03-chat-ai.html`: `width:36px;height:36px;border-radius:50%;background:rgba(255,255,255,.6);border:`

**버전 2** (3개 파일):
- `v11_보호자앱/g03-chat-nurse.html`: `transform:scale(.93)`
- `v11_보호자앱/g03-chat-patient.html`: `transform:scale(.93)`
- `v11_보호자앱/g03-chat-ai.html`: `transform:scale(.93)`

### `.messages` — 6개 파일, 2개 다른 사양

**버전 1** (3개 파일):
- `v11_보호자앱/g03-chat-nurse.html`: `flex:1;overflow-y:auto;padding:16px;display:flex;flex-direction:column;gap:12px;`
- `v11_보호자앱/g03-chat-patient.html`: `flex:1;overflow-y:auto;padding:16px;display:flex;flex-direction:column;gap:12px;`
- `v11_보호자앱/g03-chat-ai.html`: `flex:1;overflow-y:auto;padding:16px;display:flex;flex-direction:column;gap:12px;`

**버전 2** (3개 파일):
- `v11_보호자앱/g03-chat-nurse.html`: `display:none`
- `v11_보호자앱/g03-chat-patient.html`: `display:none`
- `v11_보호자앱/g03-chat-ai.html`: `display:none`

### `.switch` — 6개 파일, 2개 다른 사양

**버전 1** (3개 파일):
- `v11_요양보호사앱/c04-mypage.html`: `position:relative;width:48px;height:30px;border-radius:999px; background:rgba(0,`
- `v15_의료진앱/d03-inbox.html`: `position:relative;width:48px;height:30px;border-radius:999px; background:rgba(0,`
- `v15_의료진앱/d05-mypage.html`: `position:relative;width:48px;height:30px;border-radius:999px; background:rgba(0,`

**버전 2** (3개 파일):
- `v11_요양보호사앱/c04-mypage.html`: `content:"";position:absolute;top:3px;left:3px;width:24px;height:24px; border-rad`
- `v15_의료진앱/d03-inbox.html`: `content:"";position:absolute;top:3px;left:3px;width:24px;height:24px; border-rad`
- `v15_의료진앱/d05-mypage.html`: `content:"";position:absolute;top:3px;left:3px;width:24px;height:24px; border-rad`

### `.card` — 5개 파일, 5개 다른 사양

**버전 1** (1개 파일):
- `v10_의료진웹/의료진_대시보드_v9.5.html`: `background: var(--card-bg); border: var(--card-br); border-radius: var(--card-ra`

**버전 2** (1개 파일):
- `v10_의료진웹/의료진_대시보드_v9.5.html`: `box-shadow: var(--card-sh);`

**버전 3** (1개 파일):
- `v11_보호자앱/g05-mypage.html`: `box-shadow: var(--shadow-card-floating) !important; border: 0 !important;`

**버전 4** (1개 파일):
- `v11_요양보호사앱/c04-schedule.html`: `background: var(--cg-card-bg); border: 0; border-radius: var(--cg-card-radius); `

**버전 5** (1개 파일):
- `v15_의료진앱/d02-round.html`: `background:var(--palette-white);border-radius:var(--radius-card-lg); box-shadow:`

### `.cp-ai-act` — 5개 파일, 5개 다른 사양

**버전 1** (1개 파일):
- `v10_의료진웹/의료진_대시보드_v9.5.html`: `padding: 4px 12px; border-radius: 999px; font-size: 11px; font-weight: 600; bord`

**버전 2** (1개 파일):
- `v10_의료진웹/의료진_대시보드_v9.5.html`: `border-color: var(--ink-4); color: var(--ink-2);`

**버전 3** (1개 파일):
- `v10_의료진웹/의료진_대시보드_v9.5.html`: `display: inline-flex; align-items: center; justify-content: center; height: 28px`

**버전 4** (1개 파일):
- `v10_의료진웹/의료진_대시보드_v9.5.html`: `background: var(--surface-warm); color: var(--ink); box-shadow: 0 2px 4px rgba(0`

**버전 5** (1개 파일):
- `v10_의료진웹/의료진_대시보드_v9.5.html`: `box-shadow: 0 0 0 3px rgba(34,197,94,.30), 0 1px 2px rgba(0,0,0,.06), 0 2px 6px `

### `.ho-manual-open` — 5개 파일, 5개 다른 사양

**버전 1** (1개 파일):
- `v10_의료진웹/의료진_대시보드_v9.5.html`: `padding: 5px 10px; border-radius: 999px; font-size: 10.5px; font-weight: 600; bo`

**버전 2** (1개 파일):
- `v10_의료진웹/의료진_대시보드_v9.5.html`: `background: var(--surface); color: var(--ink);`

**버전 3** (1개 파일):
- `v10_의료진웹/의료진_대시보드_v9.5.html`: `border: 0 !important; background: var(--surface);`

**버전 4** (1개 파일):
- `v10_의료진웹/의료진_대시보드_v9.5.html`: `background: var(--surface-tint-3);`

**버전 5** (1개 파일):
- `v10_의료진웹/의료진_대시보드_v9.5.html`: `background: var(--surface-warm); box-shadow: 0 2px 4px rgba(0,0,0,.07), 0 4px 10`

### `.summary-bar` — 5개 파일, 5개 다른 사양

**버전 1** (1개 파일):
- `v11_보호자앱/g03-sotong.html`: `display: flex; align-items: center; gap: var(--space-3); padding: var(--space-4)`

**버전 2** (1개 파일):
- `v11_요양보호사앱/c03-sotong.html`: `display: flex; align-items: center; gap: var(--space-3); padding: var(--space-4)`

**버전 3** (1개 파일):
- `v11_요양보호사앱/c03-sotong.html`: `animation: haru-fade-in-up var(--motion-enter) var(--easing-standard) both;`

**버전 4** (1개 파일):
- `v11_요양보호사앱/c03-sotong.html`: `animation-delay: 60ms;`

**버전 5** (1개 파일):
- `v15_의료진앱/d03-inbox.html`: `display:flex;align-items:center;gap:12px; padding:12px 16px; background:var(--pa`

### `.tl-month` — 5개 파일, 5개 다른 사양

**버전 1** (1개 파일):
- `v11_보호자앱/g10-timeline.html`: `position: relative; font-size: var(--text-mini); font-weight: var(--weight-bold)`

**버전 2** (1개 파일):
- `v11_보호자앱/g10-timeline.html`: `content: ''; position: absolute; left: -23px; top: 50%; transform: translateY(-5`

**버전 3** (1개 파일):
- `v11_보호자앱/g10-timeline.html`: `margin-top: 0;`

**버전 4** (1개 파일):
- `v11_보호자앱/g10-timeline.html`: `animation: haru-fade-in-up var(--motion-enter) var(--easing-standard) both;`

**버전 5** (1개 파일):
- `v11_보호자앱/g10-timeline.html`: `animation-delay: 150ms;`

### `.fam-row` — 5개 파일, 5개 다른 사양

**버전 1** (1개 파일):
- `v12_환자앱/p01-today.html`: `display: flex; align-items: center; gap: 12px; padding: 10px 12px; border-radius`

**버전 2** (1개 파일):
- `v12_환자앱/p01-today.html`: `background: rgba(255, 255, 255, 0.95); box-shadow: 0 4px 14px rgba(251, 146, 60,`

**버전 3** (1개 파일):
- `v12_환자앱/p03-call.html`: `display: flex; align-items: center; gap: 16px; padding: 16px 18px; border-radius`

**버전 4** (1개 파일):
- `v12_환자앱/p03-call.html`: `background: rgba(255, 255, 255, 0.95); box-shadow: 0 6px 18px rgba(251, 146, 60,`

**버전 5** (1개 파일):
- `v12_환자앱/p03-call.html`: `padding: 14px 16px; gap: 14px;`

### `.icon-btn` — 5개 파일, 4개 다른 사양

**버전 1** (1개 파일):
- `v11_요양보호사앱/c04-schedule.html`: `width: 44px; height: 44px; border-radius: 50%; background: rgba(255,255,255,.55)`

**버전 2** (1개 파일):
- `v11_요양보호사앱/c01-today.html`: `width: 44px; height: 44px; border-radius: 50%; background: rgba(255,255,255,.55)`

**버전 3** (1개 파일):
- `v11_요양보호사앱/c04-mypage.html`: `width:44px;height:44px;border-radius:50%; background:rgba(255,255,255,.55); bord`

**버전 4** (2개 파일):
- `v15_의료진앱/d01-home.html`: `width:44px;height:44px;border-radius:50%; background:rgba(255,255,255,.55); bord`
- `v15_의료진앱/d04-handover.html`: `width:44px;height:44px;border-radius:50%; background:rgba(255,255,255,.55); bord`

### `.msg` — 5개 파일, 3개 다른 사양

**버전 1** (3개 파일):
- `v11_보호자앱/g03-chat-nurse.html`: `display:flex;flex-wrap:wrap;align-items:flex-end;gap:4px;max-width:85%`
- `v11_보호자앱/g03-chat-patient.html`: `display:flex;flex-wrap:wrap;align-items:flex-end;gap:4px;max-width:85%`
- `v11_보호자앱/g03-chat-ai.html`: `display:flex;flex-wrap:wrap;align-items:flex-end;gap:4px;max-width:85%`

**버전 2** (1개 파일):
- `v11_보호자앱/g03-chat-family.html`: `display: flex; flex-wrap: wrap; align-items: flex-end; gap: var(--space-xs); max`

**버전 3** (1개 파일):
- `v12_환자앱/p07-message.html`: `display: flex; gap: 12px; max-width: 82%;`

### `.sec` — 5개 파일, 3개 다른 사양

**버전 1** (3개 파일):
- `v11_요양보호사앱/c04-mypage.html`: `animation:haru-fade-in-up var(--duration-slow,350ms) var(--easing-standard) 160m`
- `v15_의료진앱/d01-home.html`: `animation:haru-fade-in-up var(--duration-slow,350ms) var(--easing-standard) 160m`
- `v15_의료진앱/d05-mypage.html`: `animation:haru-fade-in-up var(--duration-slow,350ms) var(--easing-standard) 160m`

**버전 2** (1개 파일):
- `v11_요양보호사앱/c02-checklist.html`: `margin-top: 18px;`

**버전 3** (1개 파일):
- `v15_의료진앱/d04-handover.html`: `margin:20px var(--pad) 0;position:relative;z-index:1;`

### `.tabbar` — 5개 파일, 2개 다른 사양

**버전 1** (2개 파일):
- `v11_보호자앱/g03-chat.html`: `position:fixed;bottom:calc(env(safe-area-inset-bottom,0px) + 12px);left:50%;tran`
- `v11_보호자앱/g03-chat-family.html`: `position:fixed;bottom:calc(env(safe-area-inset-bottom,0px) + 12px);left:50%;tran`

**버전 2** (3개 파일):
- `v15_의료진앱/d02-round.html`: `flex:1;min-width:0;height:var(--tab-h); background:rgba(255,255,255,.85); backdr`
- `v15_의료진앱/d01-home.html`: `flex:1;min-width:0;height:var(--tab-h); background:rgba(255,255,255,.85); backdr`
- `v15_의료진앱/d04-handover.html`: `flex:1;min-width:0;height:var(--tab-h); background:rgba(255,255,255,.85); backdr`

### `.sos` — 5개 파일, 2개 다른 사양

**버전 1** (4개 파일):
- `v15_의료진앱/d02-round.html`: `position:relative;width:var(--tab-h);height:var(--tab-h);flex-shrink:0;border-ra`
- `v15_의료진앱/d01-home.html`: `position:relative;width:var(--tab-h);height:var(--tab-h);flex-shrink:0;border-ra`
- `v15_의료진앱/d03-inbox.html`: `position:relative;width:var(--tab-h);height:var(--tab-h);flex-shrink:0;border-ra`
- `v15_의료진앱/d04-handover.html`: `position:relative;width:var(--tab-h);height:var(--tab-h);flex-shrink:0;border-ra`

**버전 2** (1개 파일):
- `v15_의료진앱/d05-mypage.html`: `position:relative;width:var(--tab-h);height:var(--tab-h);flex-shrink:0;border-ra`
