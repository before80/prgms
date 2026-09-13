#!/usr/bin/env python3
"""把已翻译页面中的代码块内容替换为中间稿里的原始代码。

Apple 的 DocC JSON 里偶尔会包含不间断空格等不可见字符，手写代码块很难
与之完全一致，因此用这个脚本把原始代码原样搬过来。
用法：python3 tools/sync_code.py <slug> [<slug> ...]
"""

from __future__ import annotations

import re
import sys

import registry

PREPARED = registry.HERE / "prepared"
FENCE = re.compile(r"^```[^\n]*\n(.*?)^```", re.DOTALL | re.MULTILINE)


def blocks(text: str) -> list[str]:
    return [match.group(1) for match in FENCE.finditer(text)]


def sync(slug: str) -> str | None:
    page = registry.as_dict()[slug]
    target = registry.REPO / page["file"]
    if not target.exists():
        return f"{slug}: file not generated"
    source = (PREPARED / f"{slug}.md").read_text(encoding="utf-8")
    text = target.read_text(encoding="utf-8")
    original = blocks(source)
    current = blocks(text)
    if len(original) != len(current):
        return f"{slug}: code block count {len(original)} / {len(current)}"
    out, last = [], 0
    for match, replacement in zip(FENCE.finditer(text), original):
        out.append(text[last:match.start(1)])
        out.append(replacement)
        last = match.end(1)
    out.append(text[last:])
    target.write_text("".join(out), encoding="utf-8")
    return None


def main() -> None:
    for slug in sys.argv[1:]:
        problem = sync(slug)
        print(f"FAIL {problem}" if problem else f"OK   {slug}")


if __name__ == "__main__":
    main()
