#!/usr/bin/env python3
"""Translate the section headings of already generated SwiftPM pages.

Heading text is replaced with its Chinese translation while the level and the
goldmark anchor (``{#Some-Anchor}``) are preserved, so every existing
``../chapter/#Anchor`` link keeps working.
"""

from __future__ import annotations

import json
import pathlib
import re
import sys

import registry

HERE = registry.HERE
REPO = registry.REPO
TABLE = json.loads((HERE / "tools" / "headings_zh.json").read_text(encoding="utf-8"))
HEADING = re.compile(r"^(#{2,6})\s+(.*?)\s*$", re.MULTILINE)


def main() -> None:
    pages = registry.flat_pages()
    slugs = sys.argv[1:] or [page["slug"] for page in pages]
    selected = {page["slug"]: page for page in pages}
    changed = 0
    missing: set[str] = set()
    for slug in slugs:
        page = selected.get(slug)
        if page is None:
            continue
        target = REPO / page["file"]
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
                    suffix = f" {{#{anchor}}}" if anchor else ""
                    new = f"{match.group(1)} {TABLE[base]}{suffix}"
                    if new != line:
                        changed += 1
                    out.append(new)
                    continue
                if re.match(r"^[A-Za-z]", base):
                    missing.add(base)
            out.append(line)
        target.write_text("\n".join(out), encoding="utf-8")
    print(f"已改写标题行：{changed}")
    if missing:
        print("尚无译名的标题：")
        for item in sorted(missing):
            print("  -", item)


if __name__ == "__main__":
    main()
