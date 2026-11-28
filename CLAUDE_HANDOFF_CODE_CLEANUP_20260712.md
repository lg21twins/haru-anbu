# 하루안부 코드 정리·디자인 시스템 작업 인수인계

- 작성일: 2026-07-12
- 작업 루트: `/Users/yechanshon/Desktop/Haru Anbu`
- 루트 브랜치: `feat/v11-guardian-app` (`origin`보다 3커밋 앞선 상태)
- 별도 저장소: `haru-anbu-making-of/` (`main`, 커밋·푸시하지 않음)

## 1. 반드시 먼저 알아둘 점

작업 시작 당시 루트 작업 트리는 이미 매우 더러운 상태였다.

- 추적 파일 삭제 약 940개
- 기존 수정 파일 다수
- 기존 미추적 파일 다수
- 특히 `_archive/`, 기획 문서, 과거 목업, 음원과 이미지 삭제가 이미 Git 상태에 잡혀 있었다.

위 대규모 삭제는 이 작업에서 새로 시작한 것이 아니다. 사용자가 반복해서 불필요한 파일 삭제를 지시했기 때문에 기존 삭제 상태를 복구하지 않고 그대로 보존했다. 따라서 커밋 전에는 반드시 `git diff`, `git status`, 삭제 목록을 사용자와 다시 검토해야 한다.

또한 `haru-anbu-making-of/`는 루트에서 무시되는 별도 Git 저장소이며, 그 저장소에도 작업 시작 전부터 수정·미추적 파일이 존재했다. 기존 사용자 변경을 되돌리지 않았다.

## 2. 완료한 작업

### 2.1 저장소·자산 정리

- 루트 `.vercel/` 및 `haru-anbu-making-of/.vercel/` 로컬 배포 메타데이터 제거
- `haru-anbu-showcase-v8-bundle/발표/audio/clover_prenorm_backup/` 중복 음원 백업 제거
- `haru-anbu-making-of`의 미참조 공개 자산 정리
  - 레거시 단계 이미지
  - 사용하지 않는 화면 캡처
  - 사용하지 않는 `sian/`, `stack/` 이미지
  - 사용하지 않는 `iter1~4` 영상·포스터
  - 과거 `archive-hero`, `v11-preview/index.html`
- `haru-anbu-making-of` 프로젝트 크기 약 92MB → 56MB
- 공개 자산 117개 → 22개
- 검증 후 `node_modules/`, `.next/` 삭제

### 2.2 Next.js 앱 최적화

대상: `haru-anbu-making-of/`

- 미사용 런타임·개발 의존성 9개 제거
  - `@react-three/drei`
  - `@react-three/fiber`
  - `diff`
  - `framer-motion`
  - `fuse.js`
  - `react-markdown`
  - `shiki`
  - `three`
  - 관련 `@types/*`
- 설치 패키지 약 518개 → 358개
- `package-lock.json` 동기화
- React 린트·성능 문제 수정
  - effect 내부 동기 상태 변경 제거
  - 렌더 중 ref 변경 제거
  - effect 의존성 보완
  - 미사용 상태값 제거
- `CodeMaterializeScene.tsx`의 UI 이모지를 Iconify로 교체
- `public/transform/*.html`에 남아 있던 UI 이모지를 모두 Iconify로 교체

주의: 아래 파일들은 작업 시작 전부터 수정 상태였으므로 모든 diff가 이번 작업만의 변경은 아니다.

- `app/globals.css`
- `components/Scenes.tsx`
- `components/StartGate.tsx`
- `components/scenes/*`
- `lib/waitForSpace.ts`
- `next.config.ts`

이번 작업에서 직접 수정한 핵심 파일은 다음과 같다.

- `components/effects/EdgeGlow.tsx`
- `components/scenes/BentoTransformScene.tsx`
- `components/scenes/CodeMaterializeScene.tsx`
- `lib/useSpaceGate.ts`
- `package.json`
- `package-lock.json`
- `public/transform/bento-transform.html`
- `public/transform/bento-transform-2.html`
- 미참조 `public/` 자산 삭제

### 2.3 디자인 토큰·공통 스타일 정리

- 모든 현행 앱군의 `tokens.css` 연결과 `data-role`, `data-platform` 사용 검사
- 의료진 웹의 웜 뉴트럴 색상을 공통 토큰으로 이전
- 직접 hex, 금지된 inline style, 이모지, 비표준 아이콘 위반 정리
- `--shadow-card`, `--z-fixed` 등 미정의 토큰 참조 수정
- 접근성 숨김 텍스트용 `.u-visually-hidden` 공통 유틸리티 추가
- 의료진 앱의 의도된 데이터 차트 SVG가 아이콘 위반으로 오탐되지 않도록 감사 규칙 개선
- 영문 의료진 웹의 Canvas 차트 fallback 허용 규칙을 한국어판과 동일하게 수정

주요 수정 파일:

- `07_디자인/tokens/tokens.css`
- `07_디자인/tokens/template.html`
- `07_디자인/review-rules/mobile-apps.json`
- `07_디자인/review-rules/app-folder.json`
- `07_디자인/scripts/design_audit.py`
- `07_디자인/scripts/component_divergence.py`

### 2.4 언어별 중복 CSS 제거

한·영·중 HTML 사이에서 byte 단위로 완전히 동일한 `<style>` 블록만 추출했다.

- 동일 CSS 그룹: 20개
- 적용 HTML: 42개
- 제거된 inline CSS: 13,503줄
- 새 공통 CSS: 31개
- 현행 HTML/CSS/JS 전체 순감소: 약 7,271줄

추출 위치:

- `v11_보호자앱/styles/`
- `v11_요양보호사앱/styles/`
- `v12_환자앱/styles/`
- `v15_의료진앱/styles/`

자동화 도구:

- `07_디자인/scripts/extract_shared_styles.py`

이 도구는 현재 동일한 inline style 그룹이 더 이상 없으면 추가 변경을 만들지 않는다.

### 2.5 공통 상호작용 정리

25개 화면에 반복되던 토스트 JavaScript와 CSS를 공통 모듈로 통합했다.

- `07_디자인/system/interactions.js`
- `07_디자인/system/interactions.css`
- `07_디자인/scripts/deduplicate_interactions.py`

화면별 기존 노출 시간은 `<html data-toast-duration="...">`로 보존한다.

### 2.6 파일별 접근성·구조 정리

- `<form>`이 없는 정적 화면의 버튼 690개에 `type="button"` 명시
- 중복 ID 4건 제거
- 잘못 닫힌 HTML 태그 3건 수정
  - `v11_요양보호사앱/c03-sotong.html`
  - `v11_요양보호사앱/c03-sotong.en.html`
  - `v11_요양보호사앱/c03-sotong.zh.html`
- 손상된 CSS 잔여 조각 제거
  - `v11_요양보호사앱/styles/c02-checklist.css`
  - `@keyframes` 시작 없이 남아 있던 `to { ... } }` 한 줄
- SOS 카운트다운의 `innerHTML` 재생성을 DOM API로 교체

자동화 도구:

- `07_디자인/scripts/accessibility_cleanup.py`
- `07_디자인/scripts/static_integrity.py`

## 3. 최종 검증 결과

아래 검증은 모두 통과했다.

### 정적 앱

```bash
python3 07_디자인/scripts/static_integrity.py
python3 07_디자인/scripts/test_fixtures/test_runner.py
python3 07_디자인/scripts/design_audit.py --target mobile-apps
python3 07_디자인/scripts/visual_check.py
```

결과:

- 현행 HTML 66개 구조·참조 무결성: 오류 0
- 중복 ID: 0
- 깨진 로컬 `href`/`src`: 0
- inline/external JavaScript 문법 오류: 0
- CSS 괄호 균형 오류: 0
- 디자인 시스템 감사: 7/7 통과
- 감사 회귀 테스트: 8/8 통과
- 대표 화면 정적 검사: 6/6 통과
- UI 이모지: 0

리포트:

- `07_디자인/review-reports/mobile-apps_audit_20260712.md`
- `07_디자인/review-reports/visual_check_v0.3_20260712.md`
- `07_디자인/review-reports/component_divergence_20260712.md`

### Next.js 앱

```bash
cd haru-anbu-making-of
npm install --ignore-scripts --no-audit --no-fund
npm run lint
npm run build
rm -rf node_modules .next
```

결과:

- ESLint 통과
- TypeScript 통과
- Next.js 16 프로덕션 빌드 통과
- 정적 라우트 `/`, `/_not-found` 생성 성공

## 4. 아직 완료하지 못한 작업

### 실제 브라우저 캡처 기반 시각 감사

코드·토큰·정적 검사는 통과했지만 실제 렌더링 화면을 동일 뷰포트에서 캡처해 비교하는 최종 시각 감사는 완료하지 못했다.

사유:

- 현재 Codex 세션에서 Browser 플러그인은 설치돼 있었지만 사용 가능한 브라우저 surface가 0개로 반환됐다.
- 인앱 Browser, 기본 Browser 자동 선택, 재연결 확인까지 시도했으나 사용할 수 없었다.
- 근거 없는 기존 스크린샷이나 별도 도구로 대체해 검증 완료라고 주장하지 않았다.

클로드가 브라우저/Playwright를 사용할 수 있다면 다음 대표 화면을 동일한 모바일 뷰포트로 캡처해 비교해야 한다.

1. `v11_보호자앱/g-guardian-live.html`
2. `v11_요양보호사앱/c01-today.html`
3. `v15_의료진앱/d01-home.html`
4. `v12_환자앱/p01-today.html`
5. `v13_온보딩/ob01-welcome.html`
6. `v10_의료진웹/의료진_대시보드_v9.5.html`

검수 항목:

- 헤더 높이와 좌우 여백
- 로고 크기와 아이콘 버튼 크기
- 페이지 배경과 카드 surface 단계
- 카드 radius, shadow, 내부 padding
- 제목·본문·보조 텍스트 크기와 weight
- 탭바 높이, radius, 위치, 활성 상태
- 역할별 accent 색상
- SOS·위험·주의 상태 색상
- 환자 화면의 큰 글자·큰 터치 영역
- 포커스 링, 키보드 이동, reduced motion
- 360/390/430px 모바일 폭과 의료진 웹 데스크톱 reflow

## 5. 컴포넌트 편차 리포트 해석 주의

`component_divergence.py`가 외부 CSS도 검사하도록 수정됐다. 현재 리포트에 많은 편차 후보가 보일 수 있다.

여기에는 다음이 섞여 있다.

- 역할별로 의도된 변형
- 같은 이름을 우연히 쓴 화면 전용 클래스
- 실제 공통화 대상
- 공통 CSS를 페이지가 의도적으로 override한 경우

따라서 `.card`, `.header`, `.toast`, `.msg-item` 등을 숫자만 보고 일괄 통일하면 안 된다. 실제 캡처와 역할 컨텍스트를 확인한 뒤 수정해야 한다.

## 6. 클로드가 다음에 할 일

1. 먼저 루트와 `haru-anbu-making-of`의 `git status`를 각각 확인한다.
2. 기존 940개 삭제와 이번 코드 정리를 한 커밋에 섞지 않는다.
3. 가능하면 현재 상태를 별도 안전 브랜치/커밋으로 분리한다.
4. 로컬 정적 서버를 실행한다.

```bash
cd '/Users/yechanshon/Desktop/Haru Anbu'
python3 -m http.server 8000
```

5. 위 대표 화면 6개를 캡처하고 시각 일관성을 비교한다.
6. 발견된 문제만 토큰·공통 컴포넌트 기준으로 최소 수정한다.
7. 수정 후 3장의 모든 검증 명령을 다시 실행한다.
8. 사용자 승인 전 `main`에 직접 push하지 않는다.

## 7. Git 작업 원칙

프로젝트 지침:

- `main` 직접 push 금지
- 새 브랜치 사용
- 변경 커밋 후 브랜치 push
- PR 생성

이번 Codex 작업에서는 커밋·push·PR 생성까지 하지 않았다.
