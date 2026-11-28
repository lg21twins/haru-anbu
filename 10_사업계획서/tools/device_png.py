#!/usr/bin/env python3
"""실제 화면 캡처(graphics/src/cap2) → 기기 목업 투명 PNG(부록/그림/<이름>.png).
    python3 tools/device_png.py
프레임: 쇼케이스 Mockup-templates 원본(iPhone 17 Pro · iPad Pro M5 11" · iMac 24")을 줄인 graphics/src/frames.
폰은 캡처(390×790)를 상태바 54px 아래에 두고, 위 띠는 화면 맨 위 색, 상태바는 iOS 26 Community SVG."""
import pathlib, sys
from PIL import Image
from playwright.sync_api import sync_playwright
G = pathlib.Path(__file__).resolve().parent.parent / "graphics"
OUT = G.parent / "부록/그림"
FR = (G / "src/frames").as_uri() + "/"
CAP = (G / "src/cap2").as_uri() + "/"
TOP = {'c02':'#f4faf6','c03':'#f4faf6','c04s':'#f4faf6','g01':'#f7f7f3','g06':'#f0f4f8','g03n':'#bfdbfe','d01':'#f4faf6','d02':'#f4faf6'}
PHONES = ['c02','c03','c04s','g01','g06','g03n','d01','d02','ob01','ob04','c01','c04m','c02en','c02zh','c03zh','g10','g08','g03f','g03s','dsos','d01o']
TABS = ['p01','p08','p03','p02','p10','p07','p06']; MACS = ['w01']
ONLY = set(sys.argv[1:])
for n in PHONES:
    if n not in TOP:
        im = Image.open(G / f'src/cap2/{n}.png').convert('RGB'); TOP[n] = '#%02x%02x%02x' % im.getpixel((im.width // 2, 2))
CSS = """*{margin:0;padding:0;box-sizing:border-box}html,body{background:transparent}
.dev{position:relative}.scr{position:absolute;overflow:hidden}.scr>img{position:absolute;left:0;right:0;bottom:0;width:100%;object-fit:cover;object-position:top center}
.fr{position:absolute;inset:0;width:100%;height:100%}
.iphone{width:900px;height:1840px}.iphone .scr{left:5.333%;top:2.5%;width:89.333%;height:95%;border-radius:15.84%/7.28%}.iphone .scr>img{top:6.4%;height:93.6%}
.sb{position:absolute;left:0;right:0;top:1.05%;height:4.6%;display:flex;align-items:center;z-index:2}.sb .l{width:34%;display:flex;justify-content:center}.sb .m{flex:0 0 32%}.sb .r{width:34%;display:flex;justify-content:center;gap:4%}.sb img{height:21px;width:auto}
.ipad{width:1800px;height:1281px}.ipad .scr{left:4.167%;top:5.638%;width:91.667%;height:88.723%;border-radius:1.98%/2.88%}.ipad .scr>img{top:0;height:100%}
.imac{width:2000px;height:1701px}.imac .scr{left:2.941%;top:3.704%;width:94.118%;height:62.222%}.imac .scr>img{top:0;height:100%}"""
def phone(n):
    sb = f'<div class="sb"><div class="l"><img src="{FR}Time.svg"></div><div class="m"></div><div class="r"><img src="{FR}Cellular%20Connection.svg"><img src="{FR}Wifi.svg"><img src="{FR}Frame.svg"></div></div>'
    return f'<div class="dev iphone"><div class="scr" style="background:{TOP[n]}"><img src="{CAP}{n}.png">{sb}</div><img class="fr" src="{FR}iphone.png"></div>'
def other(n, kind, frame):
    return f'<div class="dev {kind}"><div class="scr"><img src="{CAP}{n}.png"></div><img class="fr" src="{FR}{frame}"></div>'
jobs = [(n, phone(n)) for n in PHONES] + [(n, other(n, 'ipad', 'ipad.png')) for n in TABS] + [(n, other(n, 'imac', 'imac.png')) for n in MACS]
with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    pg = b.new_page(viewport={"width": 2100, "height": 1900})
    for n, html in jobs:
        if ONLY and n not in ONLY: continue
        # set_content(about:blank)에서는 file:// 그림이 막혀 틀만 찍힌다 → 임시 파일로 연다
        tmp = G / "_device_tmp.html"; tmp.write_text(f"<!DOCTYPE html><meta charset=utf-8><style>{CSS}</style>{html}", encoding="utf-8")
        pg.goto(tmp.as_uri(), wait_until="networkidle"); pg.wait_for_timeout(300)
        pg.locator(".dev").screenshot(path=str(OUT / f"{n}.png"), omit_background=True); print(n)
    b.close()
(G / "_device_tmp.html").unlink(missing_ok=True)
