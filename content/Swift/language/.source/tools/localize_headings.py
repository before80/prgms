#!/usr/bin/env python3
"""Translate the section headings of already generated chapters.

Heading text is replaced with its Chinese translation while the level and the
Hugo/goldmark anchor (``{#Some-Anchor}``) are preserved, so every existing
``../chapter/#Anchor`` link keeps working.

Usage:  python3 localize_headings.py [slug ...]   (default: every chapter)
"""

from __future__ import annotations

import json
import pathlib
import re
import sys

import registry

HERE = pathlib.Path(__file__).resolve().parent.parent
REPO = HERE.parents[2]
PAGES = registry.as_dict()
TABLE = json.loads((HERE / "tools" / "headings_zh.json").read_text(encoding="utf-8"))

HEADING = re.compile(r"^(#{2,6})\s+(.*?)\s*$", re.MULTILINE)


def main() -> None:
    slugs = sys.argv[1:] or list(PAGES)
    missing: set[str] = set()
    changed = 0
    for slug in slugs:
        target = REPO / PAGES[slug]["file"]
        if not target.exists():
            continue
        text = target.read_text(encoding="utf-8")
        in_fence = False
        out: list[str] = []
        for line in text.split("\n"):
            if line.startswith("```"):
                in_fence = not in_fence
                out.append(line)
                continue
            match = HEADING.match(line) if not in_fence else None
            if match:
                title = match.group(2)
                base, _, anchor = title.partition(" {#")
                base = base.strip()
                anchor = anchor.strip().rstrip("}")
                if base in TABLE:
                    suffix = f" {{#{anchor.strip()}}}" if anchor else ""
                    new = f"{match.group(1)} {TABLE[base]}{suffix}"
                    if new != line:
                        changed += 1
                    out.append(new)
                    continue
                if re.match(r"^[A-Za-z0-9`]", base) and not base.startswith(("Int", "UInt")):
                    missing.add(base)
            out.append(line)
        target.write_text("\n".join(out), encoding="utf-8")
    print(f"已改写标题行：{changed}")
    if missing:
        print("尚无译名的小标题：")
        for item in sorted(missing):
            print("  -", item)


if __name__ == "__main__":
    main()
