#!/usr/bin/env python3
"""Apply safe, mechanical accessibility fixes to active static app screens."""

from __future__ import annotations

import re
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
BUTTON_RE = re.compile(r"<button\b(?![^>]*\btype\s*=)([^>]*)>", re.IGNORECASE)


def main() -> None:
    files_changed = 0
    buttons_fixed = 0
    for app_dir in APP_DIRS:
        for path in (ROOT / app_dir).glob("*.html"):
            html = path.read_text(encoding="utf-8")
            html, count = BUTTON_RE.subn(r'<button type="button"\1>', html)
            if not count:
                continue
            path.write_text(html, encoding="utf-8")
            files_changed += 1
            buttons_fixed += count
    print(f"Added explicit type to {buttons_fixed} buttons in {files_changed} files")


if __name__ == "__main__":
    main()
