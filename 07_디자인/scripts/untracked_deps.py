#!/usr/bin/env python3
"""살아있는 코드가 참조하는데 **git 이 모르는** 파일을 찾는다.

    python3 07_디자인/scripts/untracked_deps.py
    python3 07_디자인/scripts/untracked_deps.py --목록     # 경로만 (git add 에 붙이기 좋게)

왜 있는가
---------
`static_integrity.py` 는 **"파일이 있는가"**를 본다. 이 도구는 **"그 파일이 저장소에 있는가"**를 본다.
내 컴퓨터에서 잘 열리는 것과 배포되는 것은 다른 문제다.

2026-08-09에 처음 돌려 보고 알았다 — **40개였다.**

    07_디자인/_iconify-bundle.js        18곳이 참조. 없으면 **전 사이트 아이콘이 사라진다**
    haru-anbu-showcase-v8-bundle/img/opt/*  히어로 · 갤러리 · 아바타 전부
    07_디자인/fonts/*.woff2 · vendor/chart.umd.min.js
    v11_보호자앱/img/opt/*.webp          일일 리포트 사진 · 식사 사진

전부 에셋 최적화 과정에서 새로 생긴 파일인데 `git add` 가 안 됐다.
**이 상태로 커밋해 배포하면 haruanbu.site 의 히어로와 갤러리가 통째로 비고 아이콘이 깨진다.**
그런데 로컬에서는 완벽하게 보인다. 그래서 아무도 몰랐다.

제안서가 가장 많이 하는 말이 **"공개 배포 중입니다"**다.
그 한 줄이 무너지면 나머지 70쪽이 같이 무너진다. 그래서 이건 배포 스크립트가 아니라 검사 항목이다.

무엇을 세지 않는가
------------------
- 없는 파일 (그건 `static_integrity.py` 몫)
- 외부 URL · data: · 앵커(#) · 템플릿 변수({...})
- `.gitignore` 로 **의도적으로** 뺀 것도 똑같이 잡힌다 — 의도를 코드가 알 수 없기 때문이다.
  의도된 것이면 아래 `IGNORE` 에 이유와 함께 적는다. **이유 없이 넣지 않는다.**
"""
from __future__ import annotations

import glob
import os
import re
import subprocess
import sys
from urllib.parse import unquote

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 참조하는 쪽 — 배포에 실제로 들어가는 것만
SOURCES = [
    "v10_의료진웹/*.html", "v11_보호자앱/*.html", "v11_요양보호사앱/*.html",
    "v12_환자앱/*.html", "v15_의료진앱/*.html", "v13_온보딩/*.html",
    "haru-anbu-showcase-v8-bundle/*.html",
    "v*/styles/*.css", "07_디자인/system/*.css",
]

# 미추적이어도 괜찮은 것 — **이유를 반드시 적는다**
IGNORE: dict[str, str] = {}

REF_RE = re.compile(r"""(?:href|src)=["']([^"']+)["']|url\(\s*['"]?([^'")]+)['"]?\s*\)""")
COMMENT_RE = re.compile(r"/\*.*?\*/", re.S)


def tracked_files() -> set[str]:
    out = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True)
    return set(out.stdout.split("\n"))


def scan() -> dict[str, set[str]]:
    tracked = tracked_files()
    found: dict[str, set[str]] = {}
    for pattern in SOURCES:
        for path in sorted(glob.glob(os.path.join(ROOT, pattern))):
            rel_src = os.path.relpath(path, ROOT)
            body = COMMENT_RE.sub("", open(path, encoding="utf-8", errors="ignore").read())
            base = os.path.dirname(path)
            for m in REF_RE.finditer(body):
                ref = (m.group(1) or m.group(2) or "").strip()
                if (not ref or "{" in ref
                        or ref.startswith(("http", "//", "data:", "#", "javascript:",
                                           "mailto:", "tel:"))):
                    continue
                clean = ref.split("?", 1)[0].split("#", 1)[0]
                if not clean:
                    continue
                target = os.path.normpath(os.path.join(base, unquote(clean)))
                if not os.path.exists(target):
                    continue                      # 없는 파일은 static_integrity 몫
                rel = os.path.relpath(target, ROOT)
                if rel in tracked or rel in IGNORE:
                    continue
                found.setdefault(rel, set()).add(rel_src)
    return found


def main() -> int:
    found = scan()
    if "--목록" in sys.argv or "--list" in sys.argv:
        for k in sorted(found):
            print(k)
        return 1 if found else 0

    if not found:
        print("미추적 의존성 검사: 없음 (참조되는 파일이 전부 저장소에 있다)")
        return 0

    total = sum(len(v) for v in found.values())
    print(f"미추적 의존성 {len(found)}개 · 참조 {total}건\n")
    for k in sorted(found, key=lambda x: (-len(found[x]), x)):
        who = sorted(found[k])
        print(f"  {k}")
        print(f"      {len(who)}곳이 참조 — 예: {who[0]}")
    print("\n  **로컬에서는 잘 보인다.** 배포는 저장소에서 나가므로 이대로 올리면 깨진다.")
    print("  `--목록` 으로 경로만 뽑아 확인한 뒤 git add 한다.")
    print("  일부러 뺀 것이면 이 파일의 IGNORE 에 **이유와 함께** 적는다.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
