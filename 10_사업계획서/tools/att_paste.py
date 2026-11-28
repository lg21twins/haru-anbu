#!/usr/bin/env python3
"""붙임 두 쪽 그림(graphics/att1_screens.png · att2_outputs.png)을 rhwp 붙여넣기용 JSON 으로.
    python3 tools/att_paste.py → hwp/att1.json · att2.json ({"html","text"})
HTML 붙여넣기의 <img> 는 높이를 150px 로 넣으므로, 붙인 뒤 개체 속성에서 비율 유지 끄고 높이(mm)를 넣는다(출력에 적힘).
"""
import base64, io, json, pathlib
from PIL import Image
G = pathlib.Path(__file__).resolve().parent.parent / "graphics"
OUT = G / "hwp"
W_MM = 164.04
ITEMS = [("att1", "att1_screens.png", "붙임 1. 실제 구현 화면 — 같은 하루, 네 사람의 화면"),
         ("att2", "att2_outputs.png", "붙임 2. 디자인 산출물 — 브랜드에서 현장 검증까지")]
for key, png, title in ITEMS:
    im = Image.open(G / png).convert("RGB")
    buf = io.BytesIO(); im.save(buf, "JPEG", quality=86)
    uri = "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()
    (OUT / f"{key}.jpg").write_bytes(buf.getvalue())
    html = (f'<p style="text-align:left;font-size:11pt;font-weight:bold;margin:0 0 4pt 0">{title}</p>'
            f'<p style="text-align:center"><img src="{uri}" width="620"></p>')
    (OUT / f"{key}.json").write_text(json.dumps({"html": html, "text": title + "\n"}, ensure_ascii=False), encoding="utf-8")
    print(key, f"{len(buf.getvalue())//1024}KB", f"높이 {W_MM * im.height / im.width:.1f}mm")
