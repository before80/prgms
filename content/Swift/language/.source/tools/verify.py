#!/usr/bin/env python3
"""Check a translated chapter against its prepared English source.

The check is structural: headings/anchors, code blocks (code itself must be
unchanged, only comments may be translated), links and image references must
all line up with the English original.  Run it without arguments to check
every translated chapter, or with chapter slugs to check a few.
"""

from __future__ import annotations

import os
import pathlib
import re
import sys

import registry

HERE = pathlib.Path(__file__).resolve().parent.parent
PREPARED = HERE / "prepared"
REPO = HERE.parents[2]
PAGES = registry.as_dict()
CONTENT = REPO / "content"

# URL directory -> anchor set, filled in main()
ANCHORS_BY_URL: dict[str, set[str]] = {}
SECTION_URLS = {
    PAGES[slug]["url_dir"]: PAGES[slug]["section_dir"] for slug in PAGES
}
SECTION_URLS.update(
    {
        f"/{registry.OUTPUT_ROOT}/{page['section_dir']}/": page["section_dir"]
        for page in PAGES.values()
    }
)

HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*$", re.MULTILINE)
FENCE = re.compile(r"^```(.*)$")
ANCHOR = re.compile(r"\{#([^}]+)\}\s*$")
LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)\)")
IMAGE = re.compile(r"!\[[^\]]*\]\(([^)\s]+)\)")


def parse(text: str):
    lines = text.split("\n")
    if lines[0].strip() == "+++":
        end = lines.index("+++", 1)
        lines = lines[end + 1 :]
    lines = [line for line in lines if not line.startswith("> 原文链接:")]
    body = "\n".join(lines)

    headings = []
    in_fence = False
    for match in HEADING.finditer(body):
        if match.group(2).startswith("```"):
            continue
        headings.append((len(match.group(1)), match.group(2).strip()))
    anchors = [ANCHOR.search(h[1]).group(1) for h in headings if ANCHOR.search(h[1])]

    code_blocks = []
    current = None
    in_fence = False
    for line in lines:
        if line.startswith("```"):
            if in_fence:
                code_blocks.append("\n".join(current))
                current, in_fence = None, False
            else:
                in_fence = True
                current = []
            continue
        if in_fence:
            current.append(line)

    # inline code spans are not links (e.g. `[String](values)`)
    without_code = re.sub(r"^```.*?^```", "", body, flags=re.DOTALL | re.MULTILINE)
    without_code = re.sub(r"`[^`\n]*`", "", without_code)
    links = sorted(set(LINK.findall(without_code)) - set(IMAGE.findall(without_code)))
    images = sorted(set(IMAGE.findall(without_code)))
    return {
        "anchors": anchors,
        "heading_levels": [h[0] for h in headings],
        "code_blocks": code_blocks,
        "links": links,
        "images": images,
    }


def code_without_comments(block: str) -> list[str]:
    # remove nested block comments from the inside out
    while True:
        stripped = re.sub(r"/\*[^/*]*\*/", "", block, flags=re.DOTALL)
        if stripped == block:
            break
        block = stripped
    out = []
    for line in block.split("\n"):
        stripped = line.strip()
        if stripped.startswith("//"):
            continue
        marker = line.find("//")
        if marker > 0:
            line = line[:marker].rstrip()
        out.append(line.rstrip())
    return [line for line in out if line.strip()]


def anchors_in_source(text: str) -> list[str]:
    result = []
    for match in HEADING.finditer(text):
        found = ANCHOR.search(match.group(2).strip())
        if found and len(match.group(1)) > 1:
            result.append(found.group(1))
    return result


def level_two_headings(text: str) -> int:
    return len([h for h in anchors_in_source(text)])


def check(slug: str) -> list[str]:
    page = PAGES[slug]
    target = REPO / page["file"]
    problems: list[str] = []
    if not target.exists():
        return [f"{slug}: 文件尚未生成 ({page['file']})"]

    source = parse((PREPARED / f"{slug}.md").read_text(encoding="utf-8"))
    result = parse(target.read_text(encoding="utf-8"))

    expected_anchors = anchors_in_source((PREPARED / f"{slug}.md").read_text(encoding="utf-8"))
    if expected_anchors != result["anchors"]:
        only_source = [a for a in expected_anchors if a not in result["anchors"]]
        only_target = [a for a in result["anchors"] if a not in expected_anchors]
        if only_source or only_target:
            problems.append(f"锚点不一致: 缺少 {only_source[:5]} 多出 {only_target[:5]}")
        else:
            problems.append("锚点顺序不一致")

    if len(source["code_blocks"]) != len(result["code_blocks"]):
        problems.append(
            f"代码块数量不一致: 原文 {len(source['code_blocks'])} / 译文 {len(result['code_blocks'])}"
        )
    else:
        for index, (a, b) in enumerate(zip(source["code_blocks"], result["code_blocks"]), start=1):
            if code_without_comments(a) != code_without_comments(b):
                problems.append(f"第 {index} 个代码块的非注释内容与原文不一致")

    if source["links"] != result["links"]:
        missing = [l for l in source["links"] if l not in result["links"]]
        extra = [l for l in result["links"] if l not in source["links"]]
        if missing or extra:
            problems.append(f"链接不一致: 缺少 {missing[:5]} 多出 {extra[:5]}")
        else:
            problems.append("链接顺序不一致")

    if source["images"] != result["images"]:
        problems.append(
            f"图片引用不一致: {source['images'][:3]} / {result['images'][:3]}"
        )

    if source["heading_levels"] != result["heading_levels"]:
        problems.append(
            f"标题层级不一致: 原文 {source['heading_levels'][:8]} / 译文 {result['heading_levels'][:8]}"
        )
    problems.extend(check_links(slug, result["links"]))
    return problems


def resolve(current_url_dir: str, target: str) -> str:
    """Resolve a relative link target against a page URL directory."""
    path, _, anchor = target.partition("#")
    directory = current_url_dir
    if path:
        joined = os.path.normpath(directory + path)
        if path.endswith("/"):
            joined += "/"
        return joined + (f"#{anchor}" if anchor else "")
    return directory + (f"#{anchor}" if anchor else "")


def check_links(slug: str, links: list[str]) -> list[str]:
    problems = []
    current = PAGES[slug]["url_dir"]
    for target in links:
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        resolved = resolve(current, target)
        path, _, anchor = resolved.partition("#")
        if path.endswith("/"):
            if path in ANCHORS_BY_URL:
                if anchor and anchor not in ANCHORS_BY_URL[path]:
                    problems.append(f"链接锚点不存在: {target}")
                continue
            if path.startswith(f"/{registry.OUTPUT_ROOT}/"):
                file = CONTENT / path.lstrip("/") / "_index.md"
                if not file.exists():
                    problems.append(f"链接指向不存在的章节索引: {target}")
                continue
            problems.append(f"无法解析的链接: {target}")
            continue
        file = CONTENT / path.lstrip("/")
        if not file.exists():
            problems.append(f"链接指向不存在的文件: {target}")
    return problems


def main() -> None:
    for page in PAGES.values():
        text = (PREPARED / f"{page['slug']}.md").read_text(encoding="utf-8")
        ANCHORS_BY_URL[page["url_dir"]] = set(anchors_in_source(text))
    ANCHORS_BY_URL[f"/{registry.OUTPUT_ROOT}/"] = set()

    slugs = sys.argv[1:] or list(PAGES)
    failed = 0
    for slug in slugs:
        problems = check(slug)
        if problems:
            failed += 1
            print(f"✗ {slug}")
            for problem in problems:
                print(f"    - {problem}")
        else:
            print(f"✓ {slug}")
    print(f"\n{len(slugs) - failed}/{len(slugs)} 通过")


if __name__ == "__main__":
    main()
