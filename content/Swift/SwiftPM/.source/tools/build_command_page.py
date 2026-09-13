#!/usr/bin/env python3
"""Generate a translated SwiftPM command reference page.

Usage:  python3 build_command_page.py <slug> [slug ...]

The page structure (headings, paragraphs, option bullets, code blocks) is kept
exactly as in the prepared English file so that ``verify.py`` passes; only the
text is replaced, using ``tools/option_zh.json``.
"""

from __future__ import annotations

import json
import pathlib
import re
import sys

import registry
import zh_extra

HERE = registry.HERE
PREPARED = HERE / "prepared"
PAGES = {page["slug"]: page for page in registry.flat_pages()}
TABLE = json.loads((HERE / "tools" / "option_zh.json").read_text(encoding="utf-8"))
HEADS = zh_extra.HEADS

TERM = re.compile(r"^- term\s+(.*?)\s*:\s*$")
ITALIC = re.compile(r"^\*(.+)\*$")
HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*$")


def front_matter(page: dict[str, object], title: str) -> str:
    return (
        "+++\n"
        f'title = "{title}"\n'
        "date = 2026-09-11T21:45:00+08:00\n"
        f'weight = {page["weight"]}\n'
        'type = "docs"\n'
        'description = ""\n'
        "isCJKLanguage = true\n"
        "draft = false\n"
        "+++\n"
    )


def build(slug: str) -> None:
    page = PAGES[slug]
    number = str(page["stem"]).split("-", 1)[0]
    title = f'{number} {page["cn_title"]}'
    url = f"https://docs.swift.org/latest/documentation/packagemanagerdocs/{slug}/"
    out: list[str] = [front_matter(page, title), "", f"> 原文链接: [{url}]({url})", "", f"# {title}"]

    unknown: set[str] = set()
    fence = False
    first_heading = True
    for line in (PREPARED / f"{slug}.md").read_text(encoding="utf-8").split("\n"):
        if line.startswith("```"):
            fence = not fence
            out.append(line)
            continue
        if fence:
            out.append(line)
            continue

        stripped = line.strip()
        if not stripped:
            out.append(line)
            continue

        heading = HEADING.match(line)
        if heading and first_heading:
            first_heading = False           # replaced by the Chinese H1
            continue
        if heading:
            text, _, anchor = heading.group(2).partition(" {#")
            base = text.strip()
            suffix = f" {{#{anchor.strip().rstrip('}')}}}" if anchor else ""
            out.append(f"{heading.group(1)} {HEADS.get(base, base)}{suffix}")
            if base not in HEADS and base not in ("build.help", "swift.test.list", "swift.test.last", "run.help"):
                unknown.add(base)
            continue

        term = TERM.match(line)
        if term:
            out.append(f"- {term.group(1)}：")
            continue

        italic = ITALIC.match(stripped)
        if italic:
            text = italic.group(1)
            out.append(f"*{TABLE.get(text, text)}*")
            if text not in TABLE:
                unknown.add(text)
            continue

        out.append(TABLE.get(stripped, line))
        if stripped not in TABLE and not stripped.startswith("|") and not stripped.startswith("- "):
            unknown.add(stripped)

    target = registry.REPO / page["file"]
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"生成 {page['file']}" + (f"（{len(unknown)} 处未翻译）" if unknown else ""))
    for text in sorted(unknown):
        print("   未译:", text[:110])


def main() -> None:
    for slug in sys.argv[1:]:
        build(slug)


if __name__ == "__main__":
    main()
