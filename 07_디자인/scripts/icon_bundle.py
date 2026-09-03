#!/usr/bin/env python3
"""아이콘 데이터 동봉 파일 생성기 — 07_디자인/_iconify-bundle.js (2026-08-09 신설).

iconify-icon 은 화면에 나온 아이콘을 api.iconify.design 에서 실시간으로 받아온다.
전시장·심사 현장처럼 네트워크가 막히거나 느리면 아이콘이 통째로 사라지므로,
쇼케이스와 앱들이 쓰는 아이콘을 미리 등록해 왕복을 없앤다(계측: 37회 → 0회).

    cd '<repo>'
    python3 07_디자인/scripts/icon_bundle.py

활성 HTML 을 훑어 icon="prefix:name" 을 모으고, iconify API 에서 한 번만 받아
_iconify-bundle.js 를 다시 쓴다. 아이콘을 새로 쓰면 이 스크립트를 다시 돌릴 것.
_iconify-bundle.js 는 반드시 _iconify-icon.min.js 다음에 로드해야 한다.
"""
import io, json, os, re, subprocess, sys
from collections import defaultdict

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
OUT = os.path.join(ROOT, '07_디자인/_iconify-bundle.js')
SKIP = ('_원본백업_', '_archive', 'node_modules', 'Haru-Anbu-실험', 'HaruAnbu_싹통일',
        'making-of', '08_제안서/_원본백업', '_리디자인_에디토리얼_', '.git')

ICON = re.compile(r'icon=["\']([a-z0-9-]+:[a-z0-9-]+)["\']')
# JS 로 조립하는 아이콘 이름도 잡는다 (문자열 리터럴 안의 prefix:name)
LIT = re.compile(r'["\']([a-z0-9-]+:[a-z0-9-]+(?:-fill|-line|-regular|-filled|-rounded|-outline|-bold))["\']')

# 대상 = 이 번들을 실제로 로드하는 HTML + 쇼케이스 2종.
# (저장소 전체를 훑으면 실험본·아카이브의 아이콘까지 들어가 파일이 5배로 커진다)
targets = []
for dirpath, dirnames, filenames in os.walk(ROOT):
    rel = os.path.relpath(dirpath, ROOT)
    if any(s in rel for s in SKIP):
        dirnames[:] = []
        continue
    for fn in filenames:
        if not fn.endswith('.html'):
            continue
        path = os.path.join(dirpath, fn)
        try:
            s = io.open(path, encoding='utf-8').read()
        except Exception:
            continue
        if '_iconify-bundle.js' in s:
            targets.append((path, s))

names = set()
for path, s in targets:
    names |= set(ICON.findall(s)) | set(LIT.findall(s))
print(f'대상 {len(targets)}개 파일 · 아이콘 이름 {len(names)}종')

by_prefix = defaultdict(set)
for n in names:
    p, name = n.split(':', 1)
    by_prefix[p].add(name)

out = {}
for prefix, icons in sorted(by_prefix.items()):
    url = f'https://api.iconify.design/{prefix}.json?icons=' + ','.join(sorted(icons))
    r = subprocess.run(['curl', '-sL', '-A', 'Mozilla/5.0', url],
                       capture_output=True, text=True, timeout=120)
    try:
        j = json.loads(r.stdout)
    except Exception:
        print(f'  {prefix}: 응답 파싱 실패 — 건너뜀', file=sys.stderr)
        continue
    got = set(j.get('icons', {})) | set(j.get('aliases', {}))
    miss = sorted(i for i in icons if i not in got)
    if miss:
        print(f'  {prefix}: 존재하지 않는 이름 {miss} — 오탈자일 수 있다', file=sys.stderr)
    keep = ('prefix', 'icons', 'aliases', 'width', 'height', 'left', 'top', 'rotate', 'hFlip', 'vFlip')
    out[prefix] = {k: j[k] for k in keep if k in j}

data = json.dumps(out, ensure_ascii=False, separators=(',', ':'))
io.open(OUT, 'w', encoding='utf-8').write('''/* 하루안부 아이콘 데이터 동봉 · 자동 생성 (07_디자인/scripts/icon_bundle.py)
 *
 * iconify-icon 은 화면에 나온 아이콘을 api.iconify.design 에서 실시간으로 받아온다.
 * 전시장·심사 현장처럼 네트워크가 막히거나 느리면 아이콘이 통째로 사라지므로,
 * 쇼케이스와 앱들이 쓰는 아이콘을 미리 등록해 왕복을 없앤다.
 * 등록에 실패해도 기존 원격 조회가 그대로 동작한다(더 나빠지지 않는다).
 *
 * 반드시 _iconify-icon.min.js 다음에 로드할 것.
 * 손으로 고치지 말고 스크립트를 다시 돌릴 것.
 */
(function () {
  var C = window.customElements && customElements.get('iconify-icon');
  if (!C || typeof C.addCollection !== 'function') return;
  var D = ''' + data + ''';
  for (var p in D) { try { C.addCollection(D[p]); } catch (e) {} }
})();
''')
total = sum(len(v.get('icons', {})) for v in out.values())
print(f'생성: {os.path.relpath(OUT, ROOT)} · 컬렉션 {len(out)} · 아이콘 {total}개 · '
      f'{os.path.getsize(OUT) / 1024:.1f}KB')
