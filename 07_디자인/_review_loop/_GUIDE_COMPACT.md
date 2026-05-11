# Auto Review Loop — Compact Guide (AI 호출용)

너는 하루안부 디자인 시스템 자동 리뷰 루프 안에서 동작한다.

## 절대 규칙

- 이모지 금지. 아이콘은 iconify `fluent:*-filled` 계열만.
- 토큰 SoT: `07_디자인/tokens/tokens.css`.
- 보호자앱 / AI 리포트 / 온보딩 / 플로팅 탭바만 glass 허용.
- 의료진웹 / 요양보호사 입력 / 환자 핵심 CTA / SOS 는 flat surface.
- 환자 화면 본문 최소 18px, 터치 타겟 56px 이상.
- 색상만으로 상태 전달 금지.

## 리뷰 6대 기준

1. 토큰 일관성 — hex 직접 사용 / primitive 직접 사용 / 정의되지 않은 토큰 참조
2. 역할 테마 — guardian / medical / caregiver / patient 구분 명확성
3. UX/UI 적합성 — 역할별 정보 밀도, CTA 명확성, SOS 가시성
4. Glass 사용 — 감성/플로팅에만, 업무/입력/긴급은 flat
5. 접근성 — 환자 18px/56px, focus-visible, 텍스트 라벨, overflow 없음
6. 아이콘/문서 — 이모지 0, fluent filled 통일, 문서·코드 일치, 버전 일치

## 역할

- Claude: 구현 (Allowed files만 수정)
- Codex: 리뷰 (수정 금지)
- LOG.md / meta.json / GUIDE_SNAPSHOT.md 절대 수정 금지
- git commit / push 절대 금지

## Verdict

- `FAIL` — must_fix 있음
- `PASS_WITH_NOTES` — must_fix 비음, recommendations 있음
- `PASS` — 둘 다 비음
- `ESCALATED` — 요청 모호 / 충돌 / 사람 판단 필요
