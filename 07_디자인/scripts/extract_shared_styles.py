#!/usr/bin/env python3
"""Extract byte-identical inline style blocks shared by localized HTML files."""

from __future__ import annotations

import hashlib
import re
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
APP_DIRS = (
    "v10_의료진웹",
    "v11_보호자앱",
    "v11_요양보호사앱",
    "v12_환자앱",
    "v13_온보딩",
    "v15_의료진앱",
)
STYLE_RE = re.compile(r"<style[^>]*>(.*?)</style>", re.DOTALL)
LOCALE_RE = re.compile(r"\.(?:en|zh)$")


def shared_groups() -> list[list[Path]]:
    groups: dict[str, list[Path]] = defaultdict(list)
    for app_dir in APP_DIRS:
        for path in (ROOT / app_dir).glob("*.html"):
            blocks = STYLE_RE.findall(path.read_text(encoding="utf-8"))
            if not blocks:
                continue
            digest = hashlib.sha256("\n".join(blocks).strip().encode()).hexdigest()
            groups[digest].append(path)
    return [paths for paths in groups.values() if len(paths) > 1]


def extract_group(paths: list[Path]) -> tuple[int, int]:
    source = paths[0].read_text(encoding="utf-8")
    blocks = STYLE_RE.findall(source)
    base_name = LOCALE_RE.sub("", paths[0].stem)
    styles_dir = paths[0].parent / "styles"
    styles_dir.mkdir(exist_ok=True)

    links: list[str] = []
    for index, block in enumerate(blocks, 1):
        suffix = "" if len(blocks) == 1 else f"-part-{index}"
        css_name = f"{base_name}{suffix}.css"
        (styles_dir / css_name).write_text(block.strip() + "\n", encoding="utf-8")
        links.append(f'<link rel="stylesheet" href="styles/{css_name}">')

    removed_lines = 0
    for path in paths:
        text = path.read_text(encoding="utf-8")
        own_blocks = STYLE_RE.findall(text)
        if own_blocks != blocks:
            raise RuntimeError(f"Style blocks changed while extracting: {path}")
        removed_lines += sum(len(block.splitlines()) for block in own_blocks)
        link_iter = iter(links)
        text = STYLE_RE.sub(lambda _: next(link_iter), text)
        path.write_text(text, encoding="utf-8")
    return len(paths), removed_lines


def main() -> None:
    file_count = 0
    removed_lines = 0
    groups = shared_groups()
    for paths in groups:
        files, lines = extract_group(paths)
        file_count += files
        removed_lines += lines
        print(f"{paths[0].parent.name}/{LOCALE_RE.sub('', paths[0].stem)}: {files} files")
    print(f"Extracted {len(groups)} groups from {file_count} files; removed {removed_lines} inline CSS lines")


if __name__ == "__main__":
    main()
