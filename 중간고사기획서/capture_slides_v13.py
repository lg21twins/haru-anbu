#!/usr/bin/env python3
"""
하루안부 기획서 v13 — 슬라이드 전체 스크린샷
1920×1080 px, 50장, 스크린샷_v13/ 폴더에 저장
"""

import asyncio
import os
from pathlib import Path
from playwright.async_api import async_playwright

HTML_FILE = Path(__file__).parent / "하루안부_기획서_v13.html"
OUT_DIR   = Path(__file__).parent / "스크린샷_v13"
OUT_DIR.mkdir(exist_ok=True)

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            executable_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage"]
        )
        page = await browser.new_page()

        # 1920×1080 뷰포트
        await page.set_viewport_size({"width": 1920, "height": 1080})
        await page.goto(f"file://{HTML_FILE.resolve()}", wait_until="load", timeout=60000)
        await page.wait_for_timeout(2000)  # 폰트·이미지 렌더링 여유

        # body padding 제거 + slide-outer margin 제거
        await page.add_style_tag(content="""
            body { padding: 0 !important; margin: 0 !important; background: #fff !important; }
            .slide-outer { margin-bottom: 0 !important; }
        """)

        # setScale() 재실행
        await page.evaluate("""
            () => {
                document.querySelectorAll('.slide-outer').forEach(outer => {
                    const slide = outer.querySelector('.slide');
                    if (!slide) return;
                    const scale = outer.offsetWidth / 1920;
                    slide.style.transform = 'scale(' + scale + ')';
                    outer.style.height = (1080 * scale) + 'px';
                });
            }
        """)
        await page.wait_for_timeout(500)

        # 모든 .slide 요소 수집
        slides = await page.query_selector_all(".slide-outer .slide")
        total = len(slides)
        print(f"총 슬라이드 수: {total}")

        if total != 50:
            print(f"⚠️  주의: 슬라이드가 50장이 아닙니다 ({total}장)")

        for i, slide in enumerate(slides, start=1):
            # 페이지 번호 추출 (.pgc span)
            pgc = await slide.query_selector(".pgc")
            if pgc:
                pg_text = (await pgc.inner_text()).strip().zfill(2)
            else:
                pg_text = str(i).zfill(2)

            fname = OUT_DIR / f"{pg_text}_slide.png"

            # 해당 슬라이드만 화면에 오도록 스크롤 후 element screenshot
            await slide.scroll_into_view_if_needed()
            await page.wait_for_timeout(80)

            # clip 사용: slide div의 bounding box를 기준으로 정확히 캡처
            bbox = await slide.bounding_box()
            if bbox:
                await page.screenshot(
                    path=str(fname),
                    clip={
                        "x": bbox["x"],
                        "y": bbox["y"],
                        "width":  1920,
                        "height": 1080,
                    }
                )
            else:
                await slide.screenshot(path=str(fname))

            print(f"  [{i:02d}/{total}] pg{pg_text} → {fname.name}")

        await browser.close()

    # 결과 검증
    files = sorted(OUT_DIR.glob("*_slide.png"))
    print(f"\n완료: {len(files)}장 저장 → {OUT_DIR}")
    if len(files) != 50:
        print("⚠️  50장 누락 확인 필요!")
    else:
        print("✅  50장 모두 정상 저장")

asyncio.run(main())
