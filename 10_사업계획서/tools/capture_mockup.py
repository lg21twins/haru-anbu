#!/usr/bin/env python3
"""부록 기기 목업용 화면 캡처 (헤드리스 크롬, 로컬 서버 8910: python3 serve.py).
    python3 tools/capture_mockup.py [이름 …] → graphics/src/cap2/<이름>.png
- 폰: ?embed=1(가짜 상태바 안 그림), 390×790 · 3배 — 아이폰 화면(390×844)에서 상태바 54px 를 뺀 높이. 부록에서 위 띠를 화면 맨 위 색으로 채우고 상태바 그림을 얹는다
- 어르신 태블릿: iPad Pro 11" 화면 비율(2420×1668 = 1.451)에 맞춰 1210×834 · 2배, embed 없음(쇼케이스 기준과 같다)
- 의료진 웹: iMac 화면 16:9 → 1600×900 · 2배
- d01(의료진 홈): 원본 파일은 고치지 않고, 응답을 가로채 _작업파일/의료진화면_수정.py 의 문구 교체(SaMD 경계 · 호실 캐논)를 적용해 찍는다
"""
import sys, pathlib, urllib.parse, importlib.util
from playwright.sync_api import sync_playwright
HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
OUT = HERE.parent / "graphics/src/cap2"
B = "http://localhost:8910/"
spec = importlib.util.spec_from_file_location("fix", REPO / "_작업파일/의료진화면_수정.py"); fix = importlib.util.module_from_spec(spec); spec.loader.exec_module(fix)
def fix_d01(body):
    for pairs in (fix.SAMD + fix.SAMD_LOOSE, fix.ROOMS + fix.SYMPTOM + fix.SYMPTOM_SUB):
        body = fix.apply(pairs, body, [], False)
    return body
PHONE = dict(viewport={"width": 390, "height": 790}, device_scale_factor=3, is_mobile=True, has_touch=True)
TAB = dict(viewport={"width": 1210, "height": 834}, device_scale_factor=2)
WEB = dict(viewport={"width": 1600, "height": 900}, device_scale_factor=2)
JOBS = {
  "c02": ("v11_요양보호사앱/c02-checklist.html", PHONE, True), "c03": ("v11_요양보호사앱/c03-sotong.html", PHONE, True),
  "c04s": ("v11_요양보호사앱/c04-schedule.html", PHONE, True),
  "g01": ("v11_보호자앱/g-guardian-live.html", PHONE, True), "g06": ("v11_보호자앱/g06-alert.html", PHONE, True),
  "g03n": ("v11_보호자앱/g03-chat-nurse.html", PHONE, True),
  "d01": ("v15_의료진앱/d01-home.html", PHONE, True), "d02": ("v15_의료진앱/d02-round.html", PHONE, True),
  "p01": ("v12_환자앱/p01-today.html", TAB, False), "p08": ("v12_환자앱/p08-help.html", TAB, False), "p03": ("v12_환자앱/p03-call.html", TAB, False),
  "w01": ("v10_의료진웹/의료진_대시보드_v9.5.html", WEB, False),   # 11-26 부록에서 뺌: AI 요약 피드 · 권장 · 이상 징후 감지 문구(계획서 SaMD 경계와 충돌)
  # 11-26 부록 15쪽 확장 후보
  "ob01": ("v13_온보딩/ob01-welcome.html", PHONE, True), "ob04": ("v13_온보딩/ob04-agree.html", PHONE, True),
  "c01": ("v11_요양보호사앱/c01-today.html", PHONE, True), "c04m": ("v11_요양보호사앱/c04-mypage.html", PHONE, True),
  "c02en": ("v11_요양보호사앱/c02-checklist.en.html", PHONE, True), "c02zh": ("v11_요양보호사앱/c02-checklist.zh.html", PHONE, True),
  "c03zh": ("v11_요양보호사앱/c03-sotong.zh.html", PHONE, True), "c01en": ("v11_요양보호사앱/c01-today.en.html", PHONE, True),
  "g10": ("v11_보호자앱/g10-timeline.html", PHONE, True), "g05r": ("v11_보호자앱/g05-records.html", PHONE, True),
  "g03f": ("v11_보호자앱/g03-chat-family.html", PHONE, True), "g03s": ("v11_보호자앱/g03-sotong.html", PHONE, True),
  "g08": ("v11_보호자앱/g08-billing.html", PHONE, True), "g07": ("v11_보호자앱/g07-settings.html", PHONE, True), "g05m": ("v11_보호자앱/g05-mypage.html", PHONE, True),
  "d05": ("v15_의료진앱/d05-mypage.html", PHONE, True), "dsos": ("v15_의료진앱/d-sos.html", PHONE, True),
  "p02": ("v12_환자앱/p02-med-alert.html", TAB, False), "p06": ("v12_환자앱/p06-photo.html", TAB, False),
  "p07": ("v12_환자앱/p07-message.html", TAB, False), "p10": ("v12_환자앱/p10-med-done.html", TAB, False),
  "d01o": ("v15_의료진앱/d01-home.html", PHONE, True),   # 문구 수정 전 원본(전후 비교용, 가로채지 않음)
  "show": ("haru-anbu-showcase-v8-bundle/haru-anbu-showcase-v8.html", dict(viewport={"width": 1440, "height": 900}, device_scale_factor=2), False),
}
names = sys.argv[1:] or list(JOBS)
with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    for n in names:
        path, opt, embed = JOBS[n]
        ctx = b.new_context(**opt, locale="ko-KR"); pg = ctx.new_page()
        url = B + urllib.parse.quote(path) + ("?embed=1" if embed else "")
        if n == "d01":
            def handle(route):
                r = route.fetch(); route.fulfill(response=r, body=fix_d01(r.text()))
            pg.route("**/d01-home.html*", handle)
        if n == "dsos":   # 캐논: 최명자는 2층 B-1호(이 화면만 B-2호로 남아 있다)
            def handle2(route):
                r = route.fetch(); route.fulfill(response=r, body=r.text().replace("2층 B-2호", "2층 B-1호"))
            pg.route("**/d-sos.html*", handle2)
        pg.goto(url, wait_until="networkidle", timeout=30000)
        pg.wait_for_timeout(1500)
        if n == "g01":   # 첫 방문 인사 애니메이션: SKIP 을 누르고 기다린다
            for sel in ["text=SKIP", "text=Skip", "[aria-label*=건너]"]:
                try: pg.click(sel, timeout=1500); break
                except Exception: pass
            pg.wait_for_timeout(3500)
        if n == "show":  # 첫 방문 "자동 투어로 보시겠어요?" 창을 닫는다
            try: pg.click("text=아니요", timeout=3000); pg.wait_for_timeout(2500)
            except Exception: pass
        pg.screenshot(path=str(OUT / f"{n}.png")); print(n, "ok"); ctx.close()
    b.close()
