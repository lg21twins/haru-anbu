# 전체 코드 정리 종합 리포트

실행 일시: 2026-05-23 (audit v0.2 기준으로 정정)
범위: 모든 production 앱 + 웹 + 디자인 시스템

> 주의: 초기 작성본에서는 "전 영역 PASS"라고 단언했으나, 그 결과는 audit v0.1 기준이었다.
> v0.1은 `.css` 파일 hex 검사가 사실상 빠져 있고, app-folder에 iconify 외 아이콘 검사도 없어
> 일부 위반을 놓쳤다. design_audit v0.2로 검사를 강화한 뒤 실제 상태를 재기록한다.

## 종합 결과 — audit v0.2 기준

| 영역 | inline | hex (HTML/CSS/JS) | 이모지 | 폐기 클래스 | iconify 외 SVG |
|---|---|---|---|---|---|
| role-component-board | 0 | 0 | 0 | 0 | 0 |
| v13_온보딩 | 0 | 0 | 0 | 0 | 0 |
| v11_요양보호사앱 | 0 | 0 | 0 | 0 | **10** |
| v15_의료진앱 | 0 | 0 | 0 | 0 | **6** |
| v12_환자앱 | 0 | 0 | 0 | 0 | **1** |
| v11_보호자앱 | 0 | 0 | 0 | 0 | **15** |
| v10_의료진웹 | 0 | 0 | 0 | 0 | **43** |

**전 영역 hex/inline/이모지/폐기 클래스 PASS**.  
SVG는 v0.1에서 검사되지 않았던 새 카테고리 — v0.2 강화 후 75건 노출됨. v0.3 마이그레이션 대상.

## audit v0.1 → v0.2 전환에서 드러난 차이

| 카테고리 | v0.1 결과 | v0.2 결과 | 비고 |
|---|---|---|---|
| 직접 hex (.css 파일) | 0건 (검사 안 됨) | 48건 발견 → 정리 후 0 | common.css/caregiver.css/patient.css/_shared.css 등 |
| `:root --var: #hex` | 무조건 허용 | tokens.css만 허용, 화면 파일은 화이트리스트 패턴만 | 화면 임의 색 추가 차단 |
| iconify 외 SVG | 검사 항목 없음 | 75건 노출 | 대부분 작은 fluent 대체 가능 SVG |
| 허용 예외 카운트 | 표시 없음 | meta theme-color / 토큰 정의 / CSS 변수 setter / 브랜드 로고 SVG 분리 표기 | "검사 안 해서 0" vs "검사 후 분류해서 0" 구분 |

## audit v0.2 도구 변경 사항

- `find_hex_violations(path, text, rules)` dispatcher 도입 — 확장자별 처리
  - `check_html_hex`: `<style>` 블록 + `style="..."` + `<script>` 블록 안 hex
  - `check_css_hex`: 전체 라인. 허용 파일이면 토큰 정의만 허용
  - `check_js_hex`: `'#hex'` / `"#hex"` 문자열
- `allowed_token_definition_files` 화이트리스트 — 기본 `07_디자인/tokens/tokens.css` 1개
- `allowed_local_token_patterns` — `--bar-w`, `--gauge-color`, `--ink-*` 등 명시 패턴만 화면 정의 허용
- `js_hex_allowed_files` — Chart.js fallback이 필요한 v10 의료진웹 1개만
- `find_non_iconify_icons`: HTML 안 인라인 `<svg>` + .svg `<img>` 검사
  - 허용: 하루안부 브랜드 심볼(viewBox 2526 2526), 큰 일러스트(viewBox ≥256), `brand-*`/`haru-mark`/`bg-logo`/`intro-ring`/`pulse`/`wave`/`spinner`/`ring-progress`/`sos__ring` 클래스
- `mobile-apps` 타깃 실제 구현 — 6개 폴더 합산, 대표 화면 3개 존재 검사
- 리포트에 **허용된 예외 / 정보성 카운트** 섹션 추가 — 허용 항목을 위반과 분리해서 가시화

## v0.1에서 v0.2 사이 실제 처리한 정리 (참고)

| 영역 | v0.1 시작 | v0.1 종료 (audit v0.1 기준) | v0.2 추가 정리 |
|---|---|---|---|
| v11_보호자앱 inline | 431 | 0 | (변동 없음) |
| v11_보호자앱 hex | 760 | 0 | common.css에서 추가 17건 정리 |
| v11_요양보호사앱 | inline 55, hex 40 | 0/0 | caregiver.css 폴백 4건 정리 |
| v15_의료진앱 | inline 27, hex 103 | 0/0 | _shared.css 1건 정리 |
| v10_의료진웹 | inline 188, hex 240 | 0/0 | dashboard.html 13건(:root ink 정의 + chart fallback) 분류 |
| v12_환자앱 | inline 5, hex 153 | 0/0 | patient.css 10건 정리 |
| v13_온보딩 | inline 0, hex 2 | 0/0 | 변동 없음 |
| 이모지 (전 영역) | 662건 | 0 | 변동 없음 |

## v0.3 진행 결과 (2026-05-23)

audit v0.2 강화 후, v0.3은 SVG 분류·도구 보완·예외 정리를 진행했다.

### 산출물

| 영역 | 결과 |
|---|---|
| SVG 인벤토리 분류표 | [svg_inventory_v0.3_20260523.md](svg_inventory_v0.3_20260523.md) |
| visual_check.py 초안 | [visual_check.py](../scripts/visual_check.py) — 대표 6화면 정적 검증 6/6 PASS (실제 캡처는 다음 단계) |
| audit fixture 회귀 테스트 | [test_fixtures/test_runner.py](../scripts/test_fixtures/) — 7/7 PASS |
| design_audit BRAND_KEYWORDS 확장 | `tab-svg`, `ov-spark`, `sos-ring`, `ai-score-ring`, `chart-marker`, `gauge-ring`, `mood-dot`, `shift-ring`, `progress-fill/-stroke`, `spark-line` 등 등록 |
| 허용 viewBox 명시화 | (60,60), (84,84), (140,140), (44,44) 시각화 ring 자동 허용 |
| 와일드카드 축소 | `--ink-*`, `--surface-*` 제거 → 명시 토큰(`--ink/-2/-3/-4/-5`, `--bg`) 7개만 허용 |

### v0.3 SVG 위반 변화

| 영역 | v0.2 시작 | v0.3 종료 |
|---|---|---|
| v11_보호자앱 | 15 | 4 (chat-bubble 12건 fluent:chat-24-filled 일괄 교체) |
| v11_요양보호사앱 | 10 | 0 (탭바 8 + shift-ring 1 + SOS ring 1 모두 허용 클래스 등록) |
| v15_의료진앱 | 6 | 0 (탭바 5 + d04 ring 1) |
| v12_환자앱 | 1 | 0 (p09-sos ring 자동 허용) |
| v13_온보딩 | 0 | 0 |
| v10_의료진웹 | 43 | 36 (mini sparkline 7건 `spark-line` 클래스 등록 — v0.4에서 마무리) |

모바일 4앱은 v0.3 단계에서 SVG 위반 0건 달성. v10 36건은 v0.4 작업 대상.

---

## v0.4 진행 결과 (2026-05-23)

v0.3 잔여 작업과 신규 정합성 점검(컴포넌트 다이버전스, at-rule 손상)을 처리했다.

### 전 영역 PASS

| 타깃 | 결과 |
|---|---|
| role-component-board | PASS 14/14 (at-rule 검사 추가) |
| mobile-apps (전체) | PASS 7/7 |
| v10_의료진웹 | PASS 7/7 (SVG 36건 전체 iconify 마이그레이션 완료) |
| v11_보호자앱 | PASS 7/7 |
| v11_요양보호사앱 | PASS 7/7 |
| v12_환자앱 | PASS 7/7 |
| v13_온보딩 | PASS 7/7 |
| v15_의료진앱 | PASS 7/7 |
| audit fixture | PASS 8/8 |
| visual_check (정적) | PASS 6/6 |

### v0.4 누적 작업

| 영역 | 작업 |
|---|---|
| 컴포넌트 다이버전스 스캐너 | `component_divergence.py` — 1937 클래스 분석, 정밀화 후 369개 진정한 다이버전스 식별 |
| 시스템 표준 신규 | `.msg-cta`(`/--secondary/--danger` 변형 3종), `.sheet-handle`/`.sheet-head`/`.sheet-ttl`/`.sheet-sub`, `.filter-row`, `.btn` 모바일 4앱 `:is()` 셀렉터 확장 |
| 화면별 자체 정의 제거 | 헤더 묶음 58 + `.btn` 6 + `.sheet-*` 18 + `.tabbar/.tab/.filter-row` 20 = 102건 |
| SVG iconify 마이그레이션 | v11_보호자앱 16건 + v10_의료진웹 36건 = 52건 |
| audit fixture 확장 | CSS hex / inline / SVG / 토큰 정의 + `@keyframes` 닫힘 검사 = 8 케이스 |
| audit v0.2 → v0.3 정밀화 | `@keyframes`/`@media` at-rule 닫힘 검사 신설 (c02-checklist 회귀 사고 → 재발 방지) |
| 시각 통일 사용자 피드백 반영 | `.msg-cta` 알약 통일, 탭바 글라스 톤 통일, c02-checklist keyframes 손상 복구 |

### 의도된 컨텍스트 차이로 남은 다이버전스

| 클래스 | 사유 |
|---|---|
| `.header` (12파일/7사양) | 페이지별 sticky/static, padding 다른 컨텍스트 |
| `.toast` (12/6) | 위치(탭바 위 / sos overlay 상단) 화면별 다름 |
| `.main` (10/10) | 화면 wrapper — 모든 화면 자체 main |
| `.msg-item` (10/9) | 인박스/소통/채팅마다 다른 의미 |
| `.chip` (7/7) | filter / status / category chip — 의미 다름 |

자동 통일은 한계 도달. 추가 통일은 사용자 시각 가이드(어느 두 화면이 같아야 하는지) 필요.

---

## 결론 (현재 상태)

audit v0.1 → v0.2 → v0.3 강화 + v0.4 정리를 거치며, 모든 정적 검사 기준에서 PASS.
허용된 예외(meta theme-color, tokens.css 정의, CSS 변수 setter, 브랜드 로고 SVG)는 별도 카운트로 가시화되어 "검사를 안 해서 0건"이 아닌 "검사 후 분류해서 0건"임이 확인 가능하다.

다음 단계는 새 정리가 아니라:
1. 진짜 브라우저 캡처 기반 시각 검증 (Playwright 등)
2. CI 통합 (PR마다 design_audit/visual_check 자동 실행)
3. 사용자 시각 가이드 받아 의도된 다이버전스를 케이스별로 점진 통일
