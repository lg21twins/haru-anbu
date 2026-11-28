#!/usr/bin/env python3
"""미드저니 흰 화면 폰 사진에 실제 앱 캡처를 원근 합성. 흰 픽셀만 바꿔 손가락을 보존한다.
사용: python3 composite_phone.py 배경.png 앱캡처.png 출력.png"""
import sys, numpy as np
from PIL import Image, ImageFilter
bg = Image.open(sys.argv[1]).convert("RGB"); app = Image.open(sys.argv[2]).convert("RGB")
a = np.asarray(bg).astype(int)
white = (a.min(axis=2) > 215) & (a.max(axis=2) - a.min(axis=2) < 25)
ys, xs = np.nonzero(white)
# 화면 영역만: 가장 큰 흰 덩어리 근사 — 중앙 근처 점만 사용
cx, cy = np.median(xs), np.median(ys)
keep = (abs(xs - cx) < 200) & (abs(ys - cy) < 320)
xs, ys = xs[keep], ys[keep]
s, d = xs + ys, xs - ys
tl = (xs[s.argmin()], ys[s.argmin()]); br = (xs[s.argmax()], ys[s.argmax()])
tr = (xs[d.argmax()], ys[d.argmax()]); bl = (xs[d.argmin()], ys[d.argmin()])
quad = [tl, tr, br, bl]
if len(sys.argv) > 4:  # 수동 꼭짓점: "x,y x,y x,y x,y" (좌상 우상 우하 좌하)
    quad = [tuple(map(float, q.split(","))) for q in sys.argv[4].split()]
print("quad", quad)
# 앱 캡처를 화면 비율로 맞춤(가로 중앙 크롭)
qw = (np.hypot(tr[0]-tl[0], tr[1]-tl[1]) + np.hypot(br[0]-bl[0], br[1]-bl[1])) / 2
qh = (np.hypot(bl[0]-tl[0], bl[1]-tl[1]) + np.hypot(br[0]-tr[0], br[1]-tr[1])) / 2
r = qw / qh
W, H = app.size
if W / H > r:
    nw = int(H * r); app = app.crop(((W - nw) // 2, 0, (W - nw) // 2 + nw, H))
else:
    app = app.crop((0, 0, W, int(W / r)))
W, H = app.size
def coeffs(dst, src):
    A, B = [], []
    for (x, y), (u, v) in zip(dst, src):
        A += [[x, y, 1, 0, 0, 0, -u*x, -u*y], [0, 0, 0, x, y, 1, -v*x, -v*y]]; B += [u, v]
    return np.linalg.solve(np.array(A, float), np.array(B, float)).tolist()
c = coeffs(quad, [(0, 0), (W, 0), (W, H), (0, H)])
warped = app.transform(bg.size, Image.PERSPECTIVE, c, Image.BICUBIC)
from PIL import ImageDraw
rm = Image.new("L", (W, H), 0)
ImageDraw.Draw(rm).rounded_rectangle([0, 0, W - 1, H - 1], radius=int(W * 0.11), fill=255)
m = rm.transform(bg.size, Image.PERSPECTIVE, c, Image.BICUBIC).filter(ImageFilter.GaussianBlur(0.8))
# 화면 밝기를 사진 톤에 맞게 살짝 낮춤
warped = Image.blend(warped, Image.new("RGB", bg.size, (235, 232, 226)), 0.06)
out = Image.composite(warped, bg, m); out.save(sys.argv[3]); print(sys.argv[3])
