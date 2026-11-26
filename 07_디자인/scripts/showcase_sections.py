#!/usr/bin/env python3
"""쇼케이스를 섹션별로 찍는다 (헤드리스, 데스크톱 1440 + 모바일 390).

    python3 07_디자인/scripts/measure_server.py &      # 8000 번 포트(점검 도구 공통 기본값)
    python3 07_디자인/scripts/showcase_sections.py --out 07_디자인/review-reports/showcase_sections
    python3 07_디자인/scripts/showcase_sections.py --page en --vp mobile

섹션마다 스크롤해서 1.2초 기다린 뒤 뷰포트를 찍는다 — reveal·lazy·iframe 이
실제로 붙은 상태를 보기 위해서다. 가로 넘침(scrollWidth > innerWidth)도 같이 보고한다.
"""
import argparse, os
from playwright.sync_api import sync_playwright

PAGES = {"ko": "haru-anbu-showcase-v8.html", "en": "haru-anbu-showcase-v8.en.html"}
VPS = {"desktop": (1440, 900), "mobile": (390, 844)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default="http://127.0.0.1:8000/haru-anbu-showcase-v8-bundle/")
    ap.add_argument("--page", default="ko", choices=PAGES)
    ap.add_argument("--vp", default="both", choices=["desktop", "mobile", "both"])
    ap.add_argument("--out", required=True)
    ap.add_argument("--wait", type=int, default=1200)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch(headless=True)
        for vp in (["desktop", "mobile"] if a.vp == "both" else [a.vp]):
            w, h = VPS[vp]
            ctx = b.new_context(viewport={"width": w, "height": h}, device_scale_factor=1,
                                is_mobile=vp == "mobile", has_touch=vp == "mobile")
            ctx.add_init_script("try{sessionStorage.setItem('haru-tour-asked','1')}catch(e){}")   # 투어 안내창이 화면을 가리지 않게
            pg = ctx.new_page()
            pg.goto(a.base + PAGES[a.page], wait_until="load")
            pg.wait_for_timeout(1500)
            ids = pg.evaluate("[...document.querySelectorAll('section[id], footer')].map(s => s.id || 'footer')")
            for i, sid in enumerate(ids):
                sel = f"#{sid}" if sid != "footer" else "footer"
                pg.evaluate(f"document.querySelector('{sel}').scrollIntoView({{block:'start'}})")
                pg.wait_for_timeout(a.wait)
                ov = pg.evaluate("document.documentElement.scrollWidth - innerWidth")
                pg.screenshot(path=os.path.join(a.out, f"{a.page}-{vp}-{i:02d}-{sid}.png"))
                print(vp, f"{i:02d}", sid, "overflow-x" if ov > 0 else "", ov if ov > 0 else "")
            ctx.close()
        b.close()


if __name__ == "__main__":
    main()
