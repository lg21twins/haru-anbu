#!/usr/bin/env python3
"""HWP 5.x 본문 텍스트 추출 (저장본 검증용). 사용: python3 hwp_text.py 파일.hwp"""
import olefile, zlib, struct, sys
f = olefile.OleFileIO(sys.argv[1])
comp = f.openstream('FileHeader').read()[36] & 1
secs = sorted([e for e in f.listdir() if e[0] == 'BodyText'], key=lambda e: int(e[1][7:]))
out = []
for s in secs:
    data = f.openstream(s).read()
    if comp: data = zlib.decompress(data, -15)
    i = 0
    while i < len(data):
        h = struct.unpack_from('<I', data, i)[0]; tag = h & 0x3ff; size = (h >> 20) & 0xfff; i += 4
        if size == 0xfff: size = struct.unpack_from('<I', data, i)[0]; i += 4
        rec = data[i:i+size]; i += size
        if tag == 67:
            txt = ''; j = 0
            while j + 1 < len(rec):
                c = struct.unpack_from('<H', rec, j)[0]
                if c in (1,2,3,4,5,6,7,8,9,11,12,14,15,16,17,18,19,20,21,22,23): j += 16; txt += ' ' if c == 9 else ''; continue
                if c in (10, 13): txt += '\n'; j += 2; continue
                txt += chr(c); j += 2
            if txt.strip(): out.append(txt.rstrip('\n'))
print('\n'.join(out))
