#!/usr/bin/env python3
"""Validate structural integrity and local references in active static app screens."""

from __future__ import annotations

import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[2]
APP_DIRS = (
    "v10_의료진웹",
    "v11_보호자앱",
    "v11_요양보호사앱",
    "v12_환자앱",
    "v13_온보딩",
    "v15_의료진앱",
)
VOID_ELEMENTS = {
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "param", "source", "track", "wbr",
}
LOCAL_REF_RE = re.compile(r'''(?:href|src)=["']([^"']+)["']''')

# CSS url() — HTML 참조와 별개로 확인해야 한다.
#
# 2026-07-12 `styles/` 추출에서 CSS 가 한 단계 깊어졌는데 상대 경로를 안 고쳤다.
# `url('mockup.png')` 이 `v11_보호자앱/mockup.png` 가 아니라
# `v11_보호자앱/styles/mockup.png` 를 가리키게 됐고, **보호자앱 일일 리포트 사진이 빈 칸이 됐다.**
# 그 상태로 찍은 스크린샷이 제안서 인쇄물에 실려 8/12 인쇄를 기다리고 있었다.
#
# **이 검사기도 design_audit 도 CSS 를 열어본 적이 없어서** 넉 주를 아무도 몰랐다.
# HTML 의 href/src 만 보면 CSS 안의 참조는 통째로 사각지대다.
CSS_COMMENT_RE = re.compile(r"/\*.*?\*/", re.S)
CSS_URL_RE = re.compile(r"""url\(\s*['"]?([^'")]+)['"]?\s*\)""")
CSS_DIRS = ("styles",)


class StructureParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.stack: list[tuple[str, tuple[int, int]]] = []
        self.errors: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag not in VOID_ELEMENTS:
            self.stack.append((tag, self.getpos()))

    def handle_endtag(self, tag: str) -> None:
        if tag in VOID_ELEMENTS:
            return
        if not self.stack:
            self.errors.append(f"{self.getpos()}: unexpected </{tag}>")
            return
        if self.stack[-1][0] == tag:
            self.stack.pop()
            return
        open_tags = [item[0] for item in self.stack]
        if tag not in open_tags:
            self.errors.append(f"{self.getpos()}: unmatched </{tag}>")
            return
        self.errors.append(
            f"{self.getpos()}: closing </{tag}> while <{self.stack[-1][0]}> is open"
        )
        while self.stack and self.stack[-1][0] != tag:
            self.stack.pop()
        self.stack.pop()


def local_reference_exists(page: Path, reference: str) -> bool:
    clean = reference.split("?", 1)[0].split("#", 1)[0]
    if not clean or clean.startswith(
        ("http:", "https:", "data:", "javascript:", "mailto:", "tel:")
    ):
        return True
    if "{" in clean:
        return True
    return (page.parent / unquote(clean)).resolve().exists()


def css_asset_errors(sheet: Path) -> list[str]:
    """CSS 안의 url() 이 실제 파일을 가리키는지. 주석은 먼저 걷어낸다 —
    걷어내지 않으면 주석 속 `url(#glass-warp)` 설명문까지 결함으로 잡힌다."""
    body = CSS_COMMENT_RE.sub("", sheet.read_text(encoding="utf-8", errors="ignore"))
    out = []
    for match in CSS_URL_RE.finditer(body):
        ref = match.group(1).strip()
        if ref.startswith(("data:", "http:", "https:", "//", "#")):
            continue          # 인라인·외부·SVG 필터 참조
        clean = ref.split("?", 1)[0].split("#", 1)[0]
        if not clean:
            continue
        target = (sheet.parent / unquote(clean)).resolve()
        if target.exists():
            continue
        line = body.count("\n", 0, match.start()) + 1
        # 한 단계 위에 있으면 `../` 누락이다 — 고치는 법까지 알려준다
        up = (sheet.parent.parent / unquote(clean)).resolve()
        hint = f" (상위 폴더에 있다 — '../{ref}' 아닌가)" if up.exists() else ""
        out.append(f"{sheet.relative_to(ROOT)}:{line}: missing css asset {ref!r}{hint}")
    return out


def main() -> None:
    errors: list[str] = []
    checked = 0
    sheets = 0
    for app_dir in APP_DIRS:
        for css_dir in CSS_DIRS:
            for sheet in sorted((ROOT / app_dir / css_dir).glob("*.css")):
                sheets += 1
                errors.extend(css_asset_errors(sheet))
    for app_dir in APP_DIRS:
        for page in (ROOT / app_dir).glob("*.html"):
            checked += 1
            html = page.read_text(encoding="utf-8")
            relative = page.relative_to(ROOT)

            parser = StructureParser()
            parser.feed(html)
            parser.close()
            errors.extend(f"{relative}: {error}" for error in parser.errors)
            errors.extend(
                f"{relative}: unclosed <{tag}> from {position}"
                for tag, position in parser.stack
                if tag not in {"html", "body"}
            )

            ids = re.findall(r'''\bid=["']([^"']+)''', html)
            errors.extend(
                f"{relative}: duplicate id={element_id!r}"
                for element_id in set(ids)
                if ids.count(element_id) > 1
            )
            errors.extend(
                f"{relative}: missing local reference {reference!r}"
                for reference in LOCAL_REF_RE.findall(html)
                if not local_reference_exists(page, reference)
            )

    print(f"Checked {checked} active HTML files · {sheets} extracted stylesheets")
    if errors:
        print(f"Integrity failures: {len(errors)}")
        print("\n".join(errors))
        raise SystemExit(1)
    print("Integrity failures: 0")


if __name__ == "__main__":
    main()
