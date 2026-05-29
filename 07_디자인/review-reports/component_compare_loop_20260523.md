# 컴포넌트 1:1 대조 점검 — 누적 리포트

실행: 2026-05-23, 8 사이클 누적
대상: v11_보호자앱 / v11_요양보호사앱 / v15_의료진앱(모바일) 트라이어드
방법: 클래스별 정의 위치·사양 비교, 시각 영향 여부 판정

## 통과 (시각 일치 확인)

| 컴포넌트 | 결과 | 비고 |
|---|---|---|
| `.bottom-bar` (tabbar) | ✓ 3앱 통일 | system 단일 소스, z-index만 system 10 vs 사용처 40 차이 |
| `.icon-btn` | ✓ 3앱 시각 100% 일치 | 단, 보호자 16파일에 `!important` 로컬 중복 |
| `.card` | ✓ 단일 소스 | common.css의 정의는 dead code |

## 변종 분리 후보 (의도된 차이로 보임)

| 컴포넌트 | 패턴 |
|---|---|
| `.chip` | system(토글)·보호자 채팅(작은 옵션)·의료진 인박스(글라스 필터) 3종이 같은 이름. `.chip--option` / `.chip--filter`로 분리 권장 |
| `.toast` | 표준 A(탭바 위, 10파일), 변종 B(보호자 home 상단, 1), 변종 C(SOS, 1). `.toast--top`, `.toast--sos` 분리 권장 |
| `.nav-btn` | 보호자 채팅 4페이지 전용. system 미등록 인라인 4중 복붙 |

## 결정 필요 (실제 차이 또는 의도 불분명)

| # | 항목 | 현황 | 사용자 결정 필요 |
|---|---|---|---|
| 1 | `.section-title` weight | 인라인 800 / system 700 (특이도로 700 적용) | 700·800 중 의도 확정 |
| 2 | `.icon-btn` 로컬 중복 | 보호자 16파일에 system과 동일 값 `!important` 재정의 | 일괄 제거 OK? (시각 영향 0) |
| 3 | `.chip` 변종 분리 | 3종이 같은 이름 사용 | 변종명 작명 OK? |
| 4 | `.nav-btn` system 등록 | 보호자 채팅 4파일 인라인 | system 이전 OK? |
| 5 | `.toast` 클래스명 통일 | 사용처 `.show` / system `.is-shown` | 어느 쪽으로 통일? |
| 6 | `.bottom-bar` z-index | system 10 / 사용 40 | system을 40으로 올릴지 |
| 7 | `.input-field` height | g03-chat-ai 38px / nurse·patient 100% | ai 38px 의도성? |

## 부가 발견

- **`v11_보호자앱/common.css`**: 16개 보호자 페이지 중 1개만 link, 그마저 `.card` 미사용 → 사실상 dead file. 정리 가능.
- **divergence 정의 파일 수 상위 클래스 다수**: `.main` (10/10), `.msg-item` (10/9), `.tl-item` (8/8) — 페이지마다 본문 컨테이너·메시지 행이 약간씩 다른 형태. 보통 의도된 페이지별 변형이라 자동 통합 부적합.

## 결론

3앱 트라이어드 시각 통일은 거의 완료 상태. 남은 작업은:
1. **즉시 가능(저위험)**: `.icon-btn` 로컬 중복 제거(16파일), `.bottom-bar` z-index 정렬
2. **명명 결정 필요**: `.chip` / `.toast` 변종 클래스 분리
3. **의도 확정 필요**: `.section-title` weight, `.input-field` height

루프를 계속 돌려도 같은 패턴(인라인 N중 복붙)만 발견될 가능성 높음 — 결정 신호 후 일괄 처리가 효율적.
