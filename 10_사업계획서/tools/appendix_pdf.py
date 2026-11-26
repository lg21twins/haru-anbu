#!/usr/bin/env python3
"""부록 PDF 굽기: graphics/appendix.html → ~/Desktop/하루안부_달란트_부록.pdf (+ 쪽 미리보기 graphics/_appx_look/)
    python3 tools/appendix_pdf.py
헤드리스 크롬 page.pdf(A4 가로). 글꼴은 설치된 Pretendard JP."""
import pathlib, sys, shutil
from playwright.sync_api import sync_playwright
H = pathlib.Path(__file__).resolve().parent.parent / "graphics/appendix.html"
OUT = pathlib.Path.home() / "Desktop/하루안부_달란트_부록.pdf"
with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    pg = b.new_page(viewport={"width": 1123, "height": 794})
    pg.goto(H.as_uri(), wait_until="networkidle"); pg.wait_for_timeout(800)
    pg.pdf(path=str(OUT), width="297mm", height="210mm", print_background=True, prefer_css_page_size=True)
    # 넘침 점검: 쪽 안에서 잘린 요소
    over = pg.evaluate("""() => [...document.querySelectorAll('.page')].map((s,i)=>{const r=s.getBoundingClientRect();
      const bad=[...s.querySelectorAll('.it,.cap')].filter(e=>{const q=e.getBoundingClientRect();return q.bottom>r.bottom-4||q.right>r.right-4}).length;return [i+1,bad]})""")
    print("overflow per page", over)
    b.close()
shutil.copy(OUT, H.parent / OUT.name)  # 로컬 서버(8910)로 열 수 있게 graphics/ 에도 사본
print(OUT, round(OUT.stat().st_size/1024), "KB")
