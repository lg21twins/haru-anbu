#!/usr/bin/env python3
"""HWP 문단 목록(컨트롤 표시 포함). 사용: python3 hwp_paras.py 파일.hwp [검색어...]"""
import olefile, zlib, struct, sys
f = olefile.OleFileIO(sys.argv[1]); keys = sys.argv[2:]
data = zlib.decompress(f.openstream("BodyText/Section0").read(), -15)
i = 0; paras = []
while i < len(data):
    h = struct.unpack_from('<I', data, i)[0]; tag = h & 0x3ff; lvl = (h >> 10) & 0x3ff; size = (h >> 20) & 0xfff; i += 4
    if size == 0xfff: size = struct.unpack_from('<I', data, i)[0]; i += 4
    rec = data[i:i+size]; i += size
    if tag == 66 and lvl == 0: paras.append('')
    elif tag == 67 and lvl == 1 and paras:
        t = ''; j = 0
        while j + 1 < len(rec):
            c = struct.unpack_from('<H', rec, j)[0]
            if c < 32 and c not in (10, 13): t += '[그림/개체]' if c == 11 else f'<{c}>'; j += 16 if c in (1,2,3,11,12,14,15,16,17,18,21,22,23) else 2; continue
            t += chr(c); j += 2
        paras[-1] = t
for k, t in enumerate(paras):
    if not keys or any(x in t for x in keys): print(k, repr(t[:110]))
