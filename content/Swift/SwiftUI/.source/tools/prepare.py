#!/usr/bin/env python3
"""Render Apple's DocC JSON into an English markdown intermediate.

Only the pages listed in ``nav_manifest.json`` are rendered.  The result is
stored in ``.source/prepared/<slug>.md`` and keeps one block per line so the
translated page can be compared against it (see ``verify.py``).
"""

from __future__ import annotations

import html
import json
import pathlib
import re
import subprocess
import sys

import registry

HERE = registry.HERE
JSON_DIR = HERE / "docc-json"
PREPARED = HERE / "prepared"
DATA_ROOT = "https://developer.apple.com/tutorials/data"
IMAGE_ROOT = "https://developer.apple.com/tutorials"
APPLE_DOCS = "https://developer.apple.com"
PAGES = registry.as_dict()

ASIDE_LABEL = {
    "note": "Note",
    "important": "Important",
    "warning": "Warning",
    "tip": "Tip",
    "experiment": "Experiment",
}


def valid_image(path: pathlib.Path) -> bool:
    """检查已下载的文件是不是真正的图片（PNG/JPEG/GIF/SVG）"""
    if not path.exists() or path.stat().st_size < 64:
        return False
    head = path.read_bytes()[:16]
    return (
        head.startswith(b"\x89PNG")
        or head.startswith(b"\xff\xd8")
        or head.startswith(b"GIF8")
        or head.lstrip().startswith(b"<?xml")
        or head.lstrip().startswith(b"<svg")
    )


def slug_from_url(url: str) -> str | None:
    """从 ``/documentation/swiftui/xxx`` 取出我们翻译的页面 slug"""
    match = re.match(r"^/documentation/swiftui/([^/#]+)", url or "")
    if not match:
        return None
    return match.group(1)


def relative_url(current: str, target: str) -> str:
    cur = [p for p in current.strip("/").split("/") if p]
    tgt = [p for p in target.strip("/").split("/") if p]
    i = 0
    while i < len(cur) and i < len(tgt) and cur[i] == tgt[i]:
        i += 1
    return "../" * (len(cur) - i) + "/".join(tgt[i:]) + "/"


def link_for(reference: dict, page: dict, anchor: str = "") -> str:
    """把 DocC reference 变成 markdown 链接目标"""
    url = reference.get("url") or ""
    if not url:
        # 视频等资源只在 variants 里给出地址
        variants = reference.get("variants") or []
        url = (variants[0].get("url") if variants else "") or ""
    slug = slug_from_url(url)
    if slug and slug in PAGES:
        target = relative_url(page["url_dir"], PAGES[slug]["url_dir"])
        return target + (f"#{anchor}" if anchor else "")
    if url.startswith("http"):
        return url
    if url.startswith("/") and reference.get("type") == "video":
        return IMAGE_ROOT + url
    if url.startswith("/"):
        # Apple 站点上的相对路径（HIG、技术概览等）补全为官方地址
        return APPLE_DOCS + url
    return url or "#"


def render_inline(items: list | None, page: dict, images: set[str]) -> str:
    out: list[str] = []
    for item in items or []:
        kind = item.get("type")
        if kind == "text":
            out.append(item.get("text", ""))
        elif kind == "codeVoice":
            out.append(f"`{item.get('code', '')}`")
        elif kind == "emphasis":
            out.append(f"*{render_inline(item.get('inlineContent'), page, images)}*")
        elif kind == "strong":
            out.append(f"**{render_inline(item.get('inlineContent'), page, images)}**")
        elif kind == "reference":
            identifier = item.get("identifier", "")
            ref = page["_refs"].get(identifier, {})
            anchor = identifier.split("#", 1)[1] if "#" in identifier else ""
            title = ref.get("title") or ref.get("alt") or item.get("title") or identifier
            target = link_for(ref, page, anchor)
            prefix = "视频：" if ref.get("type") == "video" else ""
            out.append(f"{prefix}[{title}]({target})")
        elif kind == "image":
            out.append(render_image(page["_refs"].get(item.get("identifier", ""), {}), images))
        elif kind == "inlineHead":
            out.append(f"**{render_inline(item.get('inlineContent'), page, images)}**")
        elif kind == "codeVoice":
            out.append(f"`{item.get('code', '')}`")
    return "".join(out)


def render_image(ref: dict, images: set[str]) -> str:
    alt = ref.get("alt") or ""
    variants = ref.get("variants") or []
    url = ""
    for variant in variants:
        if "dark" in (variant.get("traits") or []):
            continue
        url = variant.get("url") or url
    if not url:
        return f"![{alt}]()"
    name = pathlib.PurePosixPath(url).name
    images.add((url, name))
    return f"![{alt}](./images/{name})"


def render_blocks(blocks: list | None, page: dict, images: set[str], level: int = 2) -> list[str]:
    lines: list[str] = []
    for block in blocks or []:
        kind = block.get("type")
        if kind == "heading":
            hashes = "#" * int(block.get("level", level))
            anchor = block.get("anchor")
            suffix = f" {{#{anchor}}}" if anchor else ""
            lines += ["", f"{hashes} {block.get('text', '').strip()}{suffix}", ""]
        elif kind == "paragraph":
            lines += ["", render_inline(block.get("inlineContent"), page, images), ""]
        elif kind == "codeListing":
            syntax = block.get("syntax") or ""
            lines += ["", f"```{syntax}"] + list(block.get("code") or []) + ["```", ""]
        elif kind in ("unorderedList", "orderedList"):
            marker = "-" if kind == "unorderedList" else "1."
            for item in block.get("items") or []:
                content = item.get("content") or []
                text = render_blocks(content, page, images, level + 1)
                text = [t for t in text if t.strip()]
                if text:
                    lines.append(f"{marker} {text[0].strip()}")
                    lines += text[1:]
                else:
                    lines.append(f"{marker} ")
            lines.append("")
        elif kind == "aside":
            style = ASIDE_LABEL.get(block.get("style"), "Note")
            body = render_blocks(block.get("content"), page, images, level + 1)
            body = [b for b in body if b.strip()]
            lines.append("")
            for index, text in enumerate(body):
                prefix = f"> {style}: " if index == 0 else "> "
                lines.append(prefix + text.strip())
            lines.append("")
        elif kind == "tabNavigator":
            for tab in block.get("tabs") or []:
                lines += ["", f"**{tab.get('title', '')}**", ""]
                lines += render_blocks(tab.get("content"), page, images, level + 1)
        elif kind == "video":
            ref = page["_refs"].get(block.get("identifier", ""), {})
            poster = ref.get("poster")
            poster_ref = page["_refs"].get(poster, {}) if poster else {}
            if poster_ref:
                lines += ["", render_image(poster_ref, images), ""]
            variants = ref.get("variants") or []
            url = variants[0].get("url") if variants else ""
            title = ref.get("alt") or ref.get("title") or block.get("identifier", "")
            if url:
                lines += [f"视频：[{title[:60]}]({IMAGE_ROOT + url})", ""]
        elif kind == "row":
            for column in block.get("columns") or []:
                lines += render_blocks(column.get("content"), page, images, level + 1)
        elif kind == "links":
            for identifier in block.get("items") or []:
                ref = page["_refs"].get(identifier, {})
                title = ref.get("title") or identifier
                lines.append(f"- [{title}]({link_for(ref, page)})")
            lines.append("")
        elif kind == "termList":
            for item in block.get("items") or []:
                term = render_inline((item.get("term") or {}).get("inlineContent"), page, images)
                definition = render_blocks((item.get("definition") or {}).get("content"), page, images, level + 1)
                definition = [d for d in definition if d.strip()]
                text = definition[0].strip() if definition else ""
                lines.append(f"- term {term}: {text}")
                lines += definition[1:]
            lines.append("")
        elif kind == "table":
            rows = block.get("rows") or []
            header_is_row = block.get("header") == "row"

            def cell_text(cell) -> str:
                parts: list[str] = []
                for item in cell or []:
                    if item.get("type") == "paragraph":
                        parts.append(render_inline(item.get("inlineContent"), page, images))
                    else:
                        parts.extend(x.strip() for x in render_blocks([item], page, images) if x.strip())
                return " ".join(p for p in parts if p).replace("|", "\\|")

            lines.append("")
            for index, row in enumerate(rows):
                lines.append("| " + " | ".join(cell_text(cell) for cell in row) + " |")
                if index == 0 and header_is_row:
                    lines.append("| " + " | ".join("---" for _ in row) + " |")
            lines.append("")
    return lines


def render_topic_sections(data: dict, page: dict, images: set[str]) -> list[str]:
    lines: list[str] = []
    for section in data.get("topicSections") or []:
        title = section.get("title") or ""
        anchor = section.get("anchor")
        lines += ["", f"## {title}" + (f" {{#{anchor}}}" if anchor else ""), ""]
        for identifier in section.get("identifiers") or []:
            ref = page["_refs"].get(identifier, {})
            title_ref = ref.get("title") or identifier
            abstract = render_inline((ref.get("abstract") or []), page, images)
            target = link_for(ref, page, identifier.split("#", 1)[1] if "#" in identifier else "")
            suffix = f" — {abstract}" if abstract else ""
            lines.append(f"- [{title_ref}]({target}){suffix}")
        lines.append("")
    return lines


def render(slug: str, download_images: bool = True) -> str:
    if slug == "__root__":
        page = dict(registry.root_page())
    else:
        page = dict(PAGES[slug])
    data = json.loads((JSON_DIR / f"{slug}.json").read_text(encoding="utf-8"))
    page["_refs"] = data.get("references", {})
    images: set[tuple[str, str]] = set()

    lines = [f"# {data.get('metadata', {}).get('title', slug)}", ""]
    abstract = render_inline(data.get("abstract"), page, images)
    if abstract:
        lines += [abstract, ""]
    for section in data.get("primaryContentSections") or []:
        lines += render_blocks(section.get("content"), page, images, 2)
    lines += render_topic_sections(data, page, images)

    if download_images and images:
        target_dir = (registry.REPO / page["file"]).parent / "images"
        target_dir.mkdir(parents=True, exist_ok=True)
        for url, name in sorted(images):
            target = target_dir / name
            if valid_image(target):
                continue
            subprocess.run(
                ["curl", "-sS", "-A", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
                 "-o", str(target), IMAGE_ROOT + url],
                check=False,
            )
            if not valid_image(target):
                print(f"    ⚠ 图片下载失败: {url}", file=sys.stderr)

    text = "\n".join(lines)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip() + "\n"


def main() -> None:
    PREPARED.mkdir(exist_ok=True)
    slugs = sys.argv[1:] or list(PAGES)
    for slug in slugs:
        text = render(slug)
        (PREPARED / f"{slug}.md").write_text(text, encoding="utf-8")
        print(f"prepared {slug}: {len(text)} bytes", flush=True)


if __name__ == "__main__":
    main()
