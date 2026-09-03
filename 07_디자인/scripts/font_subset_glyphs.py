#!/usr/bin/env python3
"""쇼케이스·앱 공용 Pretendard 서브셋용 글리프 추출기 (2026-08-09 개정).

07_디자인/fonts/pretendard-subset.woff2 를 만들 때 쓴다. 이 폰트는
07_디자인/tokens/tokens.css 의 @font-face 로 선언되어 쇼케이스와 앱 전체가 함께 쓴다
(그 전엔 tokens.css 가 jsDelivr 의 dynamic-subset 을 @import 해서, 쇼케이스 한 장을
띄우는 데 CDN 으로만 240회가 나갔다).

본문 텍스트를 고쳐 새 글자가 들어가면 다시 뽑아 서브셋과 tokens.css 의 unicode-range 를
함께 갱신해야 한다(안 하면 그 글자만 시스템 폰트로 떨어진다).

    cd '<repo>'
    python3 07_디자인/scripts/font_subset_glyphs.py <대상 HTML...>   # used.txt / range.txt
    curl -sL -o /tmp/pv.woff2 \\
      https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/packages/pretendard/dist/web/variable/woff2/PretendardVariable.woff2
    pyftsubset /tmp/pv.woff2 --unicodes-file=used.txt --flavor=woff2 \\
      --layout-features='kern' --no-hinting --desubroutinize \\
      --output-file=07_디자인/fonts/pretendard-subset.woff2
    # range.txt 내용을 tokens.css 의 @font-face unicode-range 에 붙여넣는다

인자를 주지 않으면 쇼케이스 2종만 본다. 전체 앱까지 덮으려면 활성 HTML 목록을 넘길 것.
기호·구두점 블록은 여유 있게 통째로 포함한다(✓ 같은 글자가 빠져 폴백되는 사고 방지).
"""
# 렌더될 가능성이 있는 문자만 모은다 — 주석은 제외, 스크립트의 문자열 리터럴은 포함.
import io, re, sys

B = '/Users/yechanshon/Desktop/Haru Anbu/haru-anbu-showcase-v8-bundle/'

def collect(fn):
    s = io.open(B + fn, encoding='utf-8').read()
    s = re.sub(r'<!--.*?-->', ' ', s, flags=re.S)          # HTML 주석
    out = []
    # <style> 안: /* */ 주석 제거 후 content: 값만 (그 외는 렌더 텍스트 아님)
    for m in re.finditer(r'<style[^>]*>(.*?)</style>', s, re.S):
        css = re.sub(r'/\*.*?\*/', ' ', m.group(1), flags=re.S)
        out += re.findall(r'content\s*:\s*["\']([^"\']*)["\']', css)
    # <script> 안: 주석 제거 후 문자열 리터럴만
    for m in re.finditer(r'<script[^>]*>(.*?)</script>', s, re.S):
        js = re.sub(r'/\*.*?\*/', ' ', m.group(1), flags=re.S)
        js = re.sub(r'(^|[^:"\'])//[^\n]*', r'\1 ', js)
        out += re.findall(r'"([^"\\\n]*)"', js)
        out += re.findall(r"'([^'\\\n]*)'", js)
        out += re.findall(r'`([^`\\]*)`', js)
    # 본문: script/style 통째로 제거 후 태그 제거 + 속성 중 사람이 읽는 것
    body = re.sub(r'<(script|style)[^>]*>.*?</\1>', ' ', s, flags=re.S)
    out += re.findall(r'(?:alt|title|aria-label|placeholder|content)\s*=\s*"([^"]*)"', body)
    out.append(re.sub(r'<[^>]+>', ' ', body))
    return set(''.join(out))

files = sys.argv[1:] or ['haru-anbu-showcase-v8.html', 'haru-anbu-showcase-v8.en.html']
chars = set()
for f in files:
    chars |= collect(f)
for c in range(0x20, 0x7f):
    chars.add(chr(c))                                       # 기본 라틴은 통째로 안전 확보
# 기호·구두점·전각 블록은 통째로 (몇 KB 안 되고, 빠지면 그 글자만 폴백되어 티가 난다)
for a, z in [(0x00A0, 0x00FF), (0x2000, 0x206F), (0x2190, 0x21FF), (0x2200, 0x22FF),
             (0x2460, 0x24FF), (0x2500, 0x257F), (0x25A0, 0x25FF), (0x2600, 0x27BF),
             (0x3000, 0x303F), (0xFF00, 0xFFEF)]:
    for c in range(a, z + 1):
        chars.add(chr(c))
cps = sorted(ord(c) for c in chars if ord(c) >= 0x20 and ord(c) != 0x7f)
rng, s0 = [], None
prev = None
for c in cps:
    if prev is None:
        s0 = prev = c; continue
    if c == prev + 1:
        prev = c; continue
    rng.append((s0, prev)); s0 = prev = c
rng.append((s0, prev))
io.open('used.txt', 'w', encoding='utf-8').write(','.join('U+%04X' % c for c in cps))
io.open('range.txt', 'w', encoding='utf-8').write(', '.join(('U+%04X' % a) if a == b else ('U+%04X-%04X' % (a, b)) for a, b in rng))
ko = [c for c in cps if 0xAC00 <= c <= 0xD7A3]
print(f'{len(files)}개 파일 · 코드포인트 {len(cps)} (한글음절 {len(ko)}) · 구간 {len(rng)} · range 길이 {len(io.open("range.txt",encoding="utf-8").read())}B')
