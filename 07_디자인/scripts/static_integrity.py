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


def main() -> None:
    errors: list[str] = []
    checked = 0
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

    print(f"Checked {checked} active HTML files")
    if errors:
        print(f"Integrity failures: {len(errors)}")
        print("\n".join(errors))
        raise SystemExit(1)
    print("Integrity failures: 0")


if __name__ == "__main__":
    main()
