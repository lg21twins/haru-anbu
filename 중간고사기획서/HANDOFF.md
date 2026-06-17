# 하루안부 기획서 v12 — 작업 인수인계

## 파일
- 메인: `/Users/henkoo/Library/Mobile Documents/com~apple~CloudDocs/클로드/자율주행자동차처럼/하루안부_기획서_v12.html`
- 슬라이드 규격: 1920×1080px, 한국어 기획서 덱

## 전역 스타일 핵심
- `p { line-height: 1.6 }` (전역 — 레이아웃 계산 시 반드시 고려)
- `.src { font-size:16; margin-top:8px; color:#b3b3b3 }`
- 컬러 변수: `--blue:#2c7afc`, `--slate:#64748b`, `--rule:#e4e4e4`
- 폰트: Pretendard Variable

## 슬라이드 10 (s10) 현재 상태 — line ~2923부터
### 좌측 블록 (top:208, left:88, width:840, bottom:80)
- flex column, 제목/설명/`.src` 상단, 차트 블록은 `margin-top:auto`로 **바닥 정렬**
- 차트 블록 내부 순서: 라벨(16px) → mb32 → 차트(360px) → mb20 → `.src`(mt8 + 25.6)
- 총 블록 높이 471.2px → 바닥 y=1000 기준 블록 top = **528.8px**
- 따라서 좌측 "돌봄 앱 사용자 잔존율" 라벨의 top ≈ **529px**

### 우측 블록 (인터뷰)
- `position:absolute; top:529px; left:976; right:88; bottom:80`
- "사용자 인터뷰" 라벨(16px, mb32) + 3개 인용 박스(gap:16, padding:20px 24px, border:1px var(--rule), radius:8)
- 각 박스: 인용문(20px italic slate, line-height:1.6) + 화자(16px, mt8, #b3b3b3)
- 중앙 세로 구분선은 삭제된 상태

## 최근 작업 히스토리
1. s10 우측 인터뷰 레이아웃 통일성 작업 — 배경 박스 → border 스타일로 변경
2. flex 사이징 복구(카드 위로 몰리는 현상 수정)
3. 중앙 세로 구분선 삭제
4. 박스 상하 패딩 축소(32 → 20)
5. 인용문 텍스트 단축(레이아웃 유지 위해)
6. **좌우 라벨 픽셀 정렬** — 우측 top을 계산 기반 529px로 고정 (방금 완료)

## 사용자 피드백에서 학습한 작업 원칙
- **"비슷하게 말고 똑같이 맞추라"** — 정렬 요청 시 시각적 근사치 금지, 픽셀 단위 계산으로 정확히 맞출 것
- 레이아웃 수정 시 기존 `flex:1` 같은 사이징을 임의로 제거하지 말 것 (카드 몰림 사고 있었음)
- 피드백을 과해석해서 엉뚱한 메모리/규칙 만들지 말 것 — 실행 품질 문제를 프로세스 문제로 치환 금지
- 사용자가 판단 위임("너가 판단해서")하면 텍스트 축약 등 능동적 조정 OK
- 응답 간결하게, 불필요한 요약/서론 제거

## 메모리 시스템
- 위치: `/Users/henkoo/.claude/projects/-Users-henkoo-Library-Mobile-Documents-com-apple-CloudDocs--------------/memory/`
- 현재 저장된 항목: userEmail(lg22twins@gmail.com), currentDate(2026-04-19)
- 쓸데없는 규칙성 메모리 추가하지 말 것 (과거에 지적받음)

## 다음 작업 시 주의사항
- s10 외 다른 슬라이드로 확장될 수 있음 — 덱 전체 구조 파악 필요할 땐 Grep/Read로 확인
- 레이아웃 정렬은 항상 line-height 1.6, margin, gap 모두 합산해서 계산
- 파일이 커서 Read 시 offset/limit 필수
