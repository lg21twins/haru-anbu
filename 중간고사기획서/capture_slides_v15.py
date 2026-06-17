#!/usr/bin/env python3
"""
하루안부 기획서 v15 — 슬라이드 전체 스크린샷
1920×1080 px, 표지(1) ~ 46번까지, 스크린샷_v15/ 폴더에 저장
"""

import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

HTML_FILE = Path(__file__).parent / "하루안부_기획서_v15.html"
OUT_DIR   = Path(__file__).parent / "스크린샷_v15"
OUT_DIR.mkdir(exist_ok=True)

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        ctx = await browser.new_context(
            viewport={"width": 1920, "height": 1080},
            device_scale_factor=2,  # 고해상도
        )
        page = await ctx.new_page()

        await page.goto(f"file://{HTML_FILE.resolve()}", wait_until="load", timeout=60000)
        await page.wait_for_timeout(2500)  # 폰트·이미지 렌더링 여유

        # 간격/스케일 제거 → 각 슬라이드를 정확히 1920×1080으로 고정
        await page.add_style_tag(content="""
            body { padding: 0 !important; margin: 0 !important; background: #fff !important; }
            .slide-outer { margin-bottom: 0 !important; }
            .slide-outer .slide { transform: none !important; }
            .slide-outer { width: 1920px !important; height: 1080px !important; }
        """)
        await page.evaluate("""
            () => {
                document.querySelectorAll('.slide-outer').forEach(outer => {
                    outer.style.width = '1920px';
                    outer.style.height = '1080px';
                    const slide = outer.querySelector('.slide');
                    if (slide) slide.style.transform = 'none';
                });
            }
        """)
        await page.wait_for_timeout(500)

        slides = await page.query_selector_all(".slide-outer .slide")
        total = len(slides)
        print(f"총 슬라이드 수: {total}")

        for i, slide in enumerate(slides, start=1):
            fname = OUT_DIR / f"{i}.png"
            await slide.scroll_into_view_if_needed()
            await page.wait_for_timeout(100)
            bbox = await slide.bounding_box()
            if not bbox:
                print(f"  [{i:02d}] bounding_box 실패")
                continue
            await page.screenshot(
                path=str(fname),
                clip={"x": bbox["x"], "y": bbox["y"], "width": 1920, "height": 1080},
            )
            print(f"  [{i:02d}/{total}] → {fname.name}")

        await browser.close()

    files = sorted(OUT_DIR.glob("*.png"), key=lambda f: int(f.stem))
    print(f"\n완료: {len(files)}장 저장 → {OUT_DIR}")

asyncio.run(main())
