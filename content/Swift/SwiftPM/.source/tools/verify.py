#!/usr/bin/env python3
"""Check translated SwiftPM pages against their prepared English sources.

Compared per page: heading anchors and levels, code blocks (code must be
unchanged apart from comments), links, images, paragraph / bullet / grammar-line
counts.  Run without arguments to check every page.
"""

from __future__ import annotations

import os
import pathlib
import re
import sys

import registry

HERE = registry.HERE
PREPARED = HERE / "prepared"
REPO = registry.REPO
CONTENT = REPO          # REPO is already the Hugo content root
PAGES = {page["slug"]: page for page in registry.flat_pages()}


def url_dir(slug: str) -> str:
    page = PAGES[slug]
    parts = [registry.OUTPUT_ROOT, page["section_dir"]]
    if page.get("parent"):
        parts.append(page["parent"])
    parts.append(page["stem"])
    return "/" + "/".join(parts) + "/"


url_to_slug = {url_dir(slug): slug for slug in PAGES}
url_to_slug["/" + registry.OUTPUT_ROOT + "/"] = "__root__"

HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*$", re.MULTILINE)
ANCHOR = re.compile(r"\{#([^}]+)\}\s*$")
LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)\)")
IMAGE = re.compile(r"!\[[^\]]*\]\(([^)\s]+)\)")


def parse(text: str):
    lines = text.split("\n")
    if lines[0].strip() == "+++":
        lines = lines[lines.index("+++", 1) + 1 :]
    lines = [line for line in lines if not line.startswith("> 原文链接:")]
    body = "\n".join(lines)

    headings = [h for h in HEADING.finditer(body) if not h.group(2).startswith("```")]
    anchors = [ANCHOR.search(h.group(2).strip()).group(1) for h in headings if ANCHOR.search(h.group(2).strip())]

    code_blocks, current, fenced = [], None, False
    for line in lines:
        if line.startswith("```"):
            if fenced:
                code_blocks.append("\n".join(current))
                current, fenced = None, False
            else:
                fenced, current = True, []
            continue
        if fenced:
            current.append(line)

    without_code = re.sub(r"^```.*?^```", "", body, flags=re.DOTALL | re.MULTILINE)
    without_code = re.sub(r"`[^`\n]*`", "", without_code)
    links = sorted(set(LINK.findall(without_code)) - set(IMAGE.findall(without_code)))
    images = sorted(set(IMAGE.findall(without_code)))

    counts = {"para": 0, "bullet": 0, "grammar": 0}
    fenced = False
    in_para = False
    for raw in lines:
        s = raw.strip()
        if s.startswith("```"):
            fenced = not fenced
            in_para = False
            continue
        if fenced:
            continue
        if "→" in s and s.startswith(">"):
            counts["grammar"] += 1
        if not s or s.startswith(("#", "|", ">")):
            in_para = False
            continue
        if re.match(r"^([-*+]|\d+[.)])\s", s):
            counts["bullet"] += 1
            in_para = False
            continue
        if not in_para:
            counts["para"] += 1
            in_para = True

    return {
        "anchors": anchors,
        "levels": [len(h.group(1)) for h in headings],
        "code_blocks": code_blocks,
        "links": links,
        "images": images,
        "counts": counts,
    }


def code_without_comments(block: str) -> list[str]:
    while True:
        stripped = re.sub(r"/\*[^/*]*\*/", "", block, flags=re.DOTALL)
        if stripped == block:
            break
        block = stripped
    out = []
    for line in block.split("\n"):
        stripped = line.strip()
        if stripped.startswith(("#!", "//")) or re.match(r"^#(\s|$)", stripped):
            continue
        marker = line.find("//")
        if marker > 0:
            line = line[:marker].rstrip()
        marker = line.find("#")
        if marker > 0 and not line[:marker].strip() and not line.lstrip().startswith("#"):
            line = line[:marker].rstrip()
        out.append(line.rstrip())
    return [line for line in out if line.strip()]


def resolve(current: str, target: str) -> str:
    path, _, anchor = target.partition("#")
    if not path:
        return current + (f"#{anchor}" if anchor else "")
    joined = os.path.normpath(str(pathlib.PurePosixPath(current + path)))
    if path.endswith("/"):
        joined += "/"
    return joined + (f"#{anchor}" if anchor else "")


def check_links(slug: str, links: list[str]) -> list[str]:
    problems = []
    current = url_dir(slug)
    for target in links:
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        resolved = resolve(current, target)
        path, _, anchor = resolved.partition("#")
        if path.endswith("/"):
            if path in url_to_slug:
                continue
            file = CONTENT / path.lstrip("/") / "_index.md"
            if not file.exists():
                problems.append(f"链接指向不存在的章节: {target}")
            continue
        file = CONTENT / path.lstrip("/")
        if not file.exists():
            problems.append(f"链接指向不存在的文件: {target}")
    return problems


def check(slug: str) -> list[str]:
    candidates = [REPO / p["file"] for p in registry.flat_pages() if p["slug"] == slug]
    targets = [c for c in candidates if c.exists()]
    if not targets:
        return [f"{slug}: 文件尚未生成（{candidates[0]}）"]

    source_text = (PREPARED / f"{slug}.md").read_text(encoding="utf-8")
    source = parse(source_text)
    target = targets[0]
    result = parse(target.read_text(encoding="utf-8"))
    problems: list[str] = []

    expected = [ANCHOR.search(h.group(2).strip()).group(1) for h in HEADING.finditer(source_text) if ANCHOR.search(h.group(2).strip())]
    if expected != result["anchors"]:
        missing = [a for a in expected if a not in result["anchors"]]
        extra = [a for a in result["anchors"] if a not in expected]
        problems.append(f"锚点不一致: 缺 {missing[:4]} 多 {extra[:4]}" if (missing or extra) else "锚点顺序不一致")
    if source["levels"] != result["levels"]:
        problems.append("标题层级不一致")
    if len(source["code_blocks"]) != len(result["code_blocks"]):
        problems.append(f"代码块数量不一致: {len(source['code_blocks'])} / {len(result['code_blocks'])}")
    else:
        for i, (a, b) in enumerate(zip(source["code_blocks"], result["code_blocks"]), 1):
            if code_without_comments(a) != code_without_comments(b):
                problems.append(f"第 {i} 个代码块的非注释内容与原文不一致")
    if source["links"] != result["links"]:
        missing = [l for l in source["links"] if l not in result["links"]]
        extra = [l for l in result["links"] if l not in source["links"]]
        problems.append(f"链接不一致: 缺 {missing[:3]} 多 {extra[:3]}" if (missing or extra) else "链接顺序不一致")
    if source["images"] != result["images"]:
        problems.append(f"图片不一致: {source['images'][:2]} / {result['images'][:2]}")
    for key in ("para", "bullet", "grammar"):
        if source["counts"][key] != result["counts"][key]:
            problems.append(f"{key} 数量不一致: {source['counts'][key]} / {result['counts'][key]}")
    problems.extend(check_links(slug, result["links"]))
    return problems


def main() -> None:
    slugs = sys.argv[1:] or list(PAGES)
    failed = 0
    for slug in slugs:
        problems = check(slug)
        if problems:
            failed += 1
            print(f"✗ {slug}")
            for problem in problems:
                print(f"    - {problem}")
    print(f"\n{len(slugs) - failed}/{len(slugs)} 通过")


if __name__ == "__main__":
    main()
