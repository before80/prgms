#!/usr/bin/env python3
"""Check a translated SwiftUI page against its prepared English source."""

from __future__ import annotations

import os
import pathlib
import re
import sys

import registry

HERE = registry.HERE
PREPARED = HERE / "prepared"
REPO = registry.REPO
PAGES = registry.as_dict()
_root = registry.root_page()
PAGES["__root__"] = {**_root, "weight": 1, "cn_title": "SwiftUI", "stem": "SwiftUI"}
URL_TO_SLUG = {page["url_dir"]: slug for slug, page in PAGES.items()}
URL_TO_SLUG[registry.root_page()["url_dir"]] = "__root__"

HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*$", re.MULTILINE)
ANCHOR = re.compile(r"\{#([^}]+)\}\s*$")
LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)\)")
IMAGE = re.compile(r"!\[[^\]]*\]\(([^)\s]+)\)")


def parse(text: str):
    lines = text.split("\n")
    if lines and lines[0].strip() == "+++":
        lines = lines[lines.index("+++", 1) + 1:]
    lines = [line for line in lines if not line.startswith("> 原文链接:")]
    body = "\n".join(lines)

    headings = [h for h in HEADING.finditer(body) if not h.group(2).startswith("```")]
    anchors = [
        ANCHOR.search(h.group(2).strip()).group(1)
        for h in headings
        if ANCHOR.search(h.group(2).strip())
    ]
    levels = [len(h.group(1)) for h in headings]

    blocks, current, fenced = [], None, False
    for line in lines:
        if line.startswith("```"):
            if fenced:
                blocks.append("\n".join(current))
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

    counts = {"para": 0, "bullet": 0}
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
        "levels": levels,
        "code_blocks": blocks,
        "links": links,
        "images": images,
        "counts": counts,
    }


def code_without_comments(block: str) -> list[str]:
    # 去掉块注释（可能出现在行内，例如 `Button { /* action */ } label: {`）
    while True:
        stripped = re.sub(r"/\*[^/*]*\*/", "", block, flags=re.DOTALL)
        if stripped == block:
            break
        block = stripped
    out = []
    for line in block.split("\n"):
        stripped = line.strip()
        if stripped.startswith(("//", "/*", "*", "*/")):
            continue
        marker = line.find("//")
        if marker > 0:
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


def check_case_sensitive(rel: str) -> bool:
    cur = REPO
    for part in [p for p in rel.split("/") if p and p != "."]:
        try:
            names = os.listdir(cur)
        except (FileNotFoundError, NotADirectoryError):
            return False
        if part not in names:
            return False
        cur = cur / part
    return True


def check_links(slug: str, links: list[str]) -> list[str]:
    problems = []
    current = PAGES[slug]["url_dir"]
    for target in links:
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        resolved = resolve(current, target)
        path = resolved.partition("#")[0].lstrip("/")
        if path.endswith("/"):
            base = path.rstrip("/")
            if check_case_sensitive(base + ".md") or check_case_sensitive(base + "/_index.md"):
                continue
            problems.append(f"链接指向不存在的章节: {target}")
        elif not check_case_sensitive(path):
            problems.append(f"链接指向不存在的文件: {target}")
    return problems


def check(slug: str) -> list[str]:
    page = PAGES[slug]
    target = REPO / page["file"]
    if not target.exists():
        return [f"{slug}: 文件尚未生成（{page['file']}）"]
    source_text = (PREPARED / f"{slug}.md").read_text(encoding="utf-8")
    source = parse(source_text)
    result = parse(target.read_text(encoding="utf-8"))
    problems: list[str] = []

    expected = [
        ANCHOR.search(h.group(2).strip()).group(1)
        for h in HEADING.finditer(source_text)
        if ANCHOR.search(h.group(2).strip())
    ]
    if expected != result["anchors"]:
        missing = [a for a in expected if a not in result["anchors"]]
        extra = [a for a in result["anchors"] if a not in expected]
        problems.append(
            f"锚点不一致: 缺 {missing[:4]} 多 {extra[:4]}" if (missing or extra) else "锚点顺序不一致"
        )
    if source["levels"] != result["levels"]:
        problems.append("标题层级不一致")
    if len(source["code_blocks"]) != len(result["code_blocks"]):
        problems.append(
            f"代码块数量不一致: {len(source['code_blocks'])} / {len(result['code_blocks'])}"
        )
    else:
        for i, (a, b) in enumerate(zip(source["code_blocks"], result["code_blocks"]), 1):
            if code_without_comments(a) != code_without_comments(b):
                problems.append(f"第 {i} 个代码块的非注释内容与原文不一致")
    if source["links"] != result["links"]:
        missing = [l for l in source["links"] if l not in result["links"]]
        extra = [l for l in result["links"] if l not in source["links"]]
        problems.append(
            f"链接不一致: 缺 {missing[:3]} 多 {extra[:3]}" if (missing or extra) else "链接顺序不一致"
        )
    if source["images"] != result["images"]:
        problems.append(f"图片不一致: {source['images'][:2]} / {result['images'][:2]}")
    for key in ("para", "bullet"):
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
