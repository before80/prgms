#!/usr/bin/env python3
"""Insert verbatim code blocks from the prepared English page.

Some upstream code blocks contain characters that are painful to reproduce by
hand (non-breaking spaces in file trees, box-drawing glyphs).  Write a line
`@@CB:n@@` inside the fence instead, and this script swaps it for the exact
text of code block `n` (1-based) taken from `prepared/<slug>.md`.

Usage:  python3 fill_codeblocks.py <slug> [slug ...]
"""

from __future__ import annotations

import re
import sys

import registry

PAGES = {page["slug"]: page for page in registry.flat_pages()}
PLACEHOLDER = re.compile(r"^@@CB:(\d+)@@\s*$")


def code_blocks(text: str) -> list[str]:
    blocks: list[str] = []
    current = None
    fenced = False
    for line in text.split("\n"):
        if line.startswith("```"):
            if fenced:
                blocks.append("\n".join(current))
                current, fenced = None, False
            else:
                fenced, current = True, []
            continue
        if fenced:
            current.append(line)
    return blocks


def main() -> None:
    for slug in sys.argv[1:]:
        source = code_blocks(
            (registry.HERE / "prepared" / f"{slug}.md").read_text(encoding="utf-8")
        )
        target = registry.REPO / PAGES[slug]["file"]
        out: list[str] = []
        for line in target.read_text(encoding="utf-8").split("\n"):
            match = PLACEHOLDER.match(line)
            if match:
                out.extend(source[int(match.group(1)) - 1].split("\n"))
            else:
                out.append(line)
        target.write_text("\n".join(out), encoding="utf-8")
        print(f"filled {slug}")


if __name__ == "__main__":
    main()
