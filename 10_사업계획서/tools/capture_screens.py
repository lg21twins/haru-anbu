#!/usr/bin/env python3
"""부록용 실제 화면 캡처 (헤드리스 크롬, 로컬 서버 8910 필요: python3 serve.py).
    python3 tools/capture_screens.py [이름 …]  → graphics/src/cap/<이름>.png
폰은 390×844 · 3배, 어르신 태블릿은 1194×834 · 2배, 의료진 웹은 1440×900 · 2배. 첫 화면만 찍는다.
"""
import sys, pathlib, urllib.parse
from playwright.sync_api import sync_playwright
OUT = pathlib.Path(__file__).resolve().parent.parent / "graphics/src/cap"
B = "http://localhost:8910/"
PHONE = dict(viewport={"width": 390, "height": 844}, device_scale_factor=3, is_mobile=True, has_touch=True)
TAB = dict(viewport={"width": 1194, "height": 834}, device_scale_factor=2)
WEB = dict(viewport={"width": 1440, "height": 900}, device_scale_factor=2)
JOBS = {
  # 요양보호사
  "c01": ("v11_요양보호사앱/c01-today.html", PHONE), "c02": ("v11_요양보호사앱/c02-checklist.html", PHONE),
  "c03": ("v11_요양보호사앱/c03-sotong.html", PHONE), "c04s": ("v11_요양보호사앱/c04-schedule.html", PHONE),
  # 가족
  "g01": ("v11_보호자앱/g-guardian-live.html", PHONE), "g10": ("v11_보호자앱/g10-timeline.html", PHONE),
  "g05r": ("v11_보호자앱/g05-records.html", PHONE), "g03n": ("v11_보호자앱/g03-chat-nurse.html", PHONE),
  "g09": ("v11_보호자앱/g09-prescription.html", PHONE), "g06": ("v11_보호자앱/g06-alert.html", PHONE),
  # 어르신
  "p01": ("v12_환자앱/p01-today.html", TAB), "p03": ("v12_환자앱/p03-call.html", TAB), "p02": ("v12_환자앱/p02-med-alert.html", TAB),
  "p08": ("v12_환자앱/p08-help.html", TAB), "p06": ("v12_환자앱/p06-photo.html", TAB), "p05": ("v12_환자앱/p05-voice.html", TAB),
  # 의료진 앱
  "d02": ("v15_의료진앱/d02-round.html", PHONE), "d03": ("v15_의료진앱/d03-inbox.html", PHONE), "d04": ("v15_의료진앱/d04-handover.html", PHONE),
  # 의료진 웹
  "w01": ("v10_의료진웹/의료진_대시보드_v9.5.html", WEB),
}
names = sys.argv[1:] or list(JOBS)
with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    for n in names:
        path, opt = JOBS[n]
        ctx = b.new_context(**opt, locale="ko-KR")
        pg = ctx.new_page()
        pg.goto(B + urllib.parse.quote(path), wait_until="networkidle", timeout=30000)
        pg.wait_for_timeout(1800)
        pg.screenshot(path=str(OUT / f"{n}.png"))
        print(n, "ok"); ctx.close()
    b.close()
