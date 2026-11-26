# Haru Anbu Showcase v8 (haruanbu.site)

공개 쇼케이스 사이트. 정적 HTML 두 장(ko · en)이 전부이고 빌드 단계는 없다.
2026-11-15 기준으로 다시 쓴 문서 — 예전 README 가 적어 둔 `_archive/`·`07_디자인/mockup/` 구조는 지금 번들에 없다.

## 진입 파일

| 파일 | 용도 |
|------|------|
| `haru-anbu-showcase-v8.html` | 한국어판 — `/`, `/ko` 로 배포 |
| `haru-anbu-showcase-v8.en.html` | 영문판 — `/en` 으로 배포 |

두 파일은 구조가 같다. **한쪽을 고치면 다른 쪽도 같이 고친다**(스크립트·CSS 블록은 거의 그대로 복제되어 있다).
라우팅은 루트 `vercel.json` 의 rewrites 가 맡는다.

## 폴더

- `img/` — 쇼케이스용 이미지. `img/opt/` 가 웹 최적화본(webp)이고 페이지는 이쪽을 참조한다.
- `video/` — Real Story 영상(`haru-real.mp4`) + 포스터.
- `발표/` — 발표 대본·큐시트·TTS 대본, 그리고 `발표/audio/` 음성 파일(투어가 재생).
  TTS 제작용 작업 페이지 5개(`04_TTS대본_일레븐랩스` · `05_음원확인` · `07_TTS_재추출_11개` · `08_음원매칭_확인` · `09_나레이션_TTS복붙`)는 파일만 두고 `.vercelignore` 로 배포에서 뺐다.
- `Mockup-templates/` — 기기 프레임·상태바 SVG.
- `07_디자인/` — 번들 안에서만 쓰는 목업 사본(SOS 플로우 iframe 이 상대경로로 읽는다 — 지우면 데모가 깨진다).
- `docs/` — 리뷰 문서·발표 스크립트 초안.
- `카드뉴스.html` · `instagram-carousel.html` · `slide06-options.html` — 파생 산출물(공개 라우트 없음).

폰트·아이콘은 네트워크에서 받지 않는다 — 로컬 Pretendard 서브셋과 `../07_디자인/_iconify-bundle.js` 동봉본을 쓴다
(`_iconify-bundle.js` 에 `defer` 를 달면 동봉이 무력화되니 달지 않는다).

## 투어 (발표 · 방문자 겸용)

- 데스크톱에서 처음 열면 "자동 투어로 보시겠어요?" 카드가 뜬다. **예** = 음성 없이 Enter 로 한 구간씩, 상단 "나레이션 켜기" = 음성 포함.
- 같은 세션에선 한 번 답하면 다시 묻지 않는다(`sessionStorage` 의 `haru-tour-asked`). `#섹션` 딥링크로 들어오면 아예 묻지 않는다. Esc = 아니요.
- 카드가 없어도 **Enter** 가 조용한 투어를 깨운다(발표자의 키). ↓·Space·↑ 는 투어가 켜진 뒤에만 넘김 키이고, 꺼져 있을 땐 방문자의 스크롤 키로 둔다.
  꺼져 있을 때 링크·버튼에 포커스가 있으면 Enter 도 그 요소의 것(키보드 사용자). 닫힌 카드는 `inert` 라 Tab 이 닿지 않는다. 폰(터치)에는 투어가 없다.
- `?tour=present` 또는 `?sync=` 는 발표 모드(아이패드 동기화).

## 점검 도구 (저장소 루트에서)

```bash
python3 07_디자인/scripts/measure_server.py &        # 8000 번 포트(도구 공통 기본값). 캐시되는 서버로 잰다 — 접속 대기열을 키워 둔 것(기본 http.server 는 iframe 이 몰리면 ERR_CONNECTION_RESET 이 간헐로 난다). serve.py 는 no-cache 라 수치가 부풀려진다

python3 07_디자인/scripts/showcase_perf.py            # 요청 수·바이트·LCP·CLS·TBT, 콘솔 오류, 실패 요청
python3 07_디자인/scripts/showcase_sections.py --out DIR   # 섹션별 캡처 (데스크톱 1440 + 390)
python3 07_디자인/scripts/responsive_sweep.py          # 폭 320~1600 을 훑으며 잘리는 요소 찾기
python3 07_디자인/scripts/showcase_a11y.py --axe PATH/axe.min.js   # axe-core + 자체 지표 + '판정 보류' 목록 (npm i axe-core 로 받아 경로만 준다)
python3 07_디자인/scripts/dead_css.py FILE.html [--apply]          # 인라인 <style> 의 죽은 규칙
python3 07_디자인/scripts/occluded_text.py [--page en] [--widths 320,390,768,1440]   # 다른 요소에 가려진 글자 (벤 다이어그램·겹친 라벨)
```

2026-11-15 기준선: axe **새 위반 0건**(ko·en × 데스크톱·모바일) + 알려진 결정 24~29노드(역할 색 위 흰 글씨 — 스크립트가 따로 센다) · CLS 0 · LCP ≈ 1.0s · TBT 15~30ms ·
모바일 첫 화면 요청 17개 / 1.6MB(이전 69개 / 2.2MB).

## 고칠 때 지켜야 할 것

- 이모지 금지, 아이콘은 `iconify-icon`(`fluent:*` · 이미 쓰는 mingcute/ph). 색은 `07_디자인/tokens/tokens.css` 토큰.
- 그라데이션 · 이탤릭 · 불필요한 테두리 금지(예외는 프로젝트 메모리의 확정 2건뿐).
- iframe(앱 목업)은 `loading="lazy"` 를 유지하고, DOM 을 옮기는 코드는 lazy 를 무력화하니 `data-lazy-src` 패턴을 따른다.
- 체험 모드가 꺼진 목업 iframe 은 `tabindex=-1`(Tab 이 목업 안으로 끌려가지 않게), 켜지면(`.interactive`) 0. 새 목업 래퍼를 만들면 `.feat-*-wrap` 클래스를 따른다.
- 영문은 한국어보다 길다 — 겹친 도형 안 라벨·고정 셀 라벨은 영문 폭으로 확인한다(`occluded_text.py --page en`).
- 글자 대비는 AA(4.5:1). 보조 회색은 `--mute`(`#5C6270`), 브랜드 블루 위 읽는 글자는 `--brand-blue-600` 배경.
- **axe 는 스크롤로 나타나는(reveal) 요소가 투명한 동안엔 그 글자를 검사하지 않는다.** 빨리 훑고 재면 위반이 과소 집계된다("0건" 이 나왔는데 제대로 나타난 뒤엔 59건이었다) — `showcase_a11y.py` 는 천천히 훑고 남은 reveal 을 켠 뒤 잰다.
- **역할 색(블루·그린·오렌지) 위 흰 글씨는 2026-08-16 에 시각 통일을 위해 유지하기로 한 결정**이다(컬러 스와치·벤 원 라벨·"눌러보세요" 알약·칩). 스크립트의 `ACCEPTED` 목록이 이를 따로 센다 — 바꾸려면 그 결정부터 다시 내린다.
- **axe 위반 0건이 곧 읽힌다는 뜻은 아니다.** 사진 위 글자·SVG 글자는 axe 가 대비를 못 재서 '판정 보류'로 빠진다 — 차트 축 라벨이 `#CCC`(1.5:1)였던 것도 이렇게 빠져 있었다.
  SVG 글자는 `var(--mute)`, 사진(히어로) 위 흰 글자는 단색 스크림 0.24 + 옅은 글자 그림자(그라데이션 금지). 점검 스크립트의 '판정 보류' 목록을 눈으로 본다.
