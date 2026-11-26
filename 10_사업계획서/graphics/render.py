#!/usr/bin/env python3
"""graphics/*.html → PNG (2x). 헤드리스 크롬. 사용: python3 render.py fig1_flow.html [...]"""
import sys, pathlib
from playwright.sync_api import sync_playwright
here = pathlib.Path(__file__).parent.resolve()
with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    for name in sys.argv[1:]:
        f = here / name
        pg = b.new_page(device_scale_factor=2, viewport={"width": 820, "height": 1000})  # 좁게 열어 화면용 @media(min-width:900) 를 피한다
        pg.goto(f.as_uri()); pg.wait_for_timeout(600)
        w, h = pg.evaluate("[document.body.scrollWidth, document.body.scrollHeight]")
        pg.set_viewport_size({"width": w, "height": h})
        out = f.with_suffix(".png"); pg.screenshot(path=str(out), full_page=True); print(out)
    b.close()
