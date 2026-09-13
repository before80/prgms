#!/usr/bin/env python3
"""Turn the upstream DocC markdown of every SwiftPM page into a prepared
English markdown file that is easy to translate:

  * DocC directives and HTML comments are dropped
  * every heading gets the anchor used by the rendered page, written as a
    goldmark attribute:  ``## Overview {#Overview}``
  * ``<doc:Chapter#Anchor>`` links become ordinary relative links that already
    point at the final Docsy URL of the target page
  * hard-wrapped paragraphs are joined into one line per paragraph

The result is stored in .source/prepared/<Slug>.md and kept as part of the
preserved source material.
"""

from __future__ import annotations

import json
import pathlib
import re

import registry

HERE = registry.HERE
BOOK = HERE / "swift-package-manager" / "Sources" / "PackageManagerDocs" / "Documentation.docc"
JSON_DIR = HERE / "docc-json"
PREPARED = HERE / "prepared"
REPO = registry.REPO

PAGES = {page["slug"]: page for page in registry.flat_pages()}


def load_anchors(slug: str):
    data = json.loads((JSON_DIR / f"{slug}.json").read_text(encoding="utf-8"))
    headings = []
    for section in data.get("primaryContentSections", []):
        for block in section.get("content", []):
            if block.get("type") == "heading":
                headings.append((block["level"], block["text"], block["anchor"]))
    return headings


ANCHORS = {slug: load_anchors(slug) for slug in PAGES}
ANCHOR_TEXT = {slug: {a: t for _l, t, a in ANCHORS[slug]} for slug in PAGES}


def url_dir(slug: str) -> str:
    page = PAGES[slug]
    parts = [registry.OUTPUT_ROOT, page["section_dir"]]
    if page.get("parent"):
        parts.append(page["parent"])
    if page["is_collection"] or page.get("parent"):
        parts.append(page["stem"])
    else:
        parts.append(page["stem"])
    return "/" + "/".join(parts) + "/"


def relative_url(current: str, target: str) -> str:
    cur = [p for p in current.strip("/").split("/") if p]
    tgt = [p for p in target.strip("/").split("/") if p]
    common = 0
    while common < min(len(cur), len(tgt)) and cur[common] == tgt[common]:
        common += 1
    parts = [".."] * (len(cur) - common) + tgt[common:]
    return "/".join(parts) + "/" if parts else "./"


DOC_LINK = re.compile(r"<doc:([A-Za-z0-9._-]+)?(?:#([^>]+))?>")
DOC_MD_LINK = re.compile(r"\[([^\]]+)\]\(<doc:([A-Za-z0-9._-]+)?(?:#([^>]+))?>\)")
DOC_BARE_LINK = re.compile(r"\[([^\]]+)\]\(doc:([A-Za-z0-9._-]+)?(?:#([^)]+))?\)")


def resolve_reference(raw_slug: str | None, current_slug: str) -> tuple[str, str] | None:
    """Resolve a doc: reference to ("page", slug) or ("anchor", name)."""
    if not raw_slug:
        return None
    if raw_slug in ANCHOR_TEXT.get(current_slug, {}):
        return ("anchor", raw_slug)
    slug = LOOKUP.get(_key(raw_slug))
    if slug is None:
        # anchors are sometimes written as if they were page names
        matches = [s for s, anchors in ANCHOR_TEXT.items() if raw_slug in anchors]
        if len(matches) == 1:
            return ("anchor", raw_slug) if matches[0] == current_slug else ("page", matches[0])
        raise SystemExit(f"unknown chapter reference: {raw_slug}")
    return ("page", slug)


def _key(name: str) -> str:
    return re.sub(r"[^a-z0-9]", "", name.lower())


def _build_lookup() -> dict[str, str]:
    lookup: dict[str, str] = {}
    for slug, page in PAGES.items():
        lookup[_key(slug)] = slug
        lookup[_key(pathlib.Path(page["source"]).stem)] = slug
        lookup[_key(page["stem"])] = slug
    for slug in PAGES:
        data = json.loads((JSON_DIR / f"{slug}.json").read_text(encoding="utf-8"))
        lookup.setdefault(_key(data["metadata"]["title"]), slug)
    return lookup


LOOKUP = _build_lookup()


def replace_doc_link(match: re.Match[str], current_slug: str) -> str:
    raw_slug, anchor = match.group(1), match.group(2)
    resolved = resolve_reference(raw_slug, current_slug)
    if resolved is None:  # self reference, e.g. <doc:#Anchor>
        target = "./"
        text = ANCHOR_TEXT[current_slug].get(anchor, anchor) if anchor else "self"
        return f"[{text}]({target}{( '#' + anchor) if anchor else ''})"
    kind, slug = resolved
    if kind == "anchor":
        return f"[{ANCHOR_TEXT[current_slug].get(slug, slug)}](./#{slug})"
    if slug not in PAGES:
        raise SystemExit(f"unknown chapter reference: {slug}")
    target = relative_url(url_dir(current_slug), url_dir(slug))
    if anchor:
        target += f"#{anchor}"
    text = ANCHOR_TEXT[slug].get(anchor) if anchor else None
    if text is None:
        text = PAGES[slug]["cn_title"] if False else title_en(slug)
    return f"[{text}]({target})"


def replace_doc_md_link(match: re.Match[str], current_slug: str) -> str:
    """Handle markdown links whose destination is a doc: reference."""
    text, raw_slug, anchor = match.group(1), match.group(2), match.group(3)
    resolved = resolve_reference(raw_slug, current_slug)
    if resolved is None:
        target = "./" + (f"#{anchor}" if anchor else "")
    elif resolved[0] == "anchor":
        target = f"./#{resolved[1]}"
    else:
        target = relative_url(url_dir(current_slug), url_dir(resolved[1]))
        if anchor:
            target = target.rstrip("/") + "/#" + anchor
    return f"[{text}]({target})"


def replace_doc_bare_link(match: re.Match[str], current_slug: str) -> str:
    """Handle markdown links written as [text](doc:Chapter)."""
    return replace_doc_md_link(match, current_slug)


def title_en(slug: str) -> str:
    data = json.loads((JSON_DIR / f"{slug}.json").read_text(encoding="utf-8"))
    return data["metadata"]["title"]


TITLES_EN = {slug: title_en(slug) for slug in PAGES}

IMAGE = re.compile(r"!\[([^\]]*)\]\(([^)\s]+)\)")


def image_target_dir(slug: str) -> pathlib.Path:
    """Every top-level section keeps its own ``images`` folder.

    Images are copied next to the chapter files of their section and are
    referenced from the translated markdown as ``./images/<name>``.
    """
    return (REPO / PAGES[slug]["file"]).parent / "images"


def copy_images(
    text: str, current_slug: str, images: dict[pathlib.Path, set[str]]
) -> str:
    def repl(match: re.Match[str]) -> str:
        alt, name = match.group(1), match.group(2)
        if name.startswith("http") or name.startswith("../"):
            return match.group(0)
        source = None
        for candidate in (
            BOOK / "Assets" / f"{name}@2x.svg",
            BOOK / "Assets" / f"{name}.svg",
            BOOK / "Assets" / f"{name}@2x.png",
            BOOK / "Assets" / f"{name}.png",
            BOOK / "Assets" / f"{name}.jpg",
        ):
            if candidate.exists():
                source = candidate
                break
        if source is None:
            raise SystemExit(f"missing image asset: {name}")
        target_name = f"{name}{source.suffix}"
        images.setdefault(image_target_dir(current_slug), set()).add(target_name)
        return f"![{alt}](./images/{target_name})"

    return IMAGE.sub(repl, text)


COMMENTS = re.compile(r"<!--.*?-->", re.DOTALL)
DIRECTIVE = re.compile(r"^@(Metadata|Options|AutomaticSeeAlso)[^\n]*\n(?:.*?\n)*?\}\n", re.MULTILINE)


def strip_source(text: str) -> str:
    text = DIRECTIVE.sub("", COMMENTS.sub("", text))
    # The "Topics" section lists the child pages; navigation is provided by the
    # Docsy sidebar instead, and it has no anchors in the rendered page data.
    for marker in (r"^## Topics\s*$", r"^## See Also\s*$"):
        found = re.search(marker, text, re.MULTILINE)
        if found:
            text = text[: found.start()]
    return text


BLOCK_START = re.compile(
    r"^\s*(#{1,6}\s|```|>\s*$|>\s|>\S|\*\s|-\s|\+\s|\d+[.)]\s|\||@[A-Za-z]+\b|\[[^\]]+\]:\s)"
)


def join_wrapped_lines(text: str) -> str:
    out: list[str] = []
    fenced = False
    for raw in text.split("\n"):
        line = raw.rstrip()
        if line.strip().startswith("```"):
            fenced = not fenced
            out.append(line)
            continue
        if fenced:
            out.append(raw)
            continue
        if not out or not out[-1].strip():
            out.append(line)
            continue
        previous = out[-1]
        if (
            line.strip()
            and not BLOCK_START.match(line)
            and not previous.endswith("\\")
            and not previous.strip().startswith("```")
            and not re.match(r"^\[[^\]]+\]:\s*$", previous.strip())
        ):
            out[-1] = previous.rstrip() + " " + line.strip()
        else:
            out.append(line)
    return "\n".join(out)


HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*$", re.MULTILINE)
TYPOGRAPHY = {"\u2019": "'", "\u2018": "'", "\u201c": '"', "\u201d": '"', "\u2014": "-", "\u2013": "-"}


def normalize(text: str) -> str:
    for a, b in TYPOGRAPHY.items():
        text = text.replace(a, b)
    return " ".join(text.split())


def add_anchors(text: str, slug: str) -> str:
    rendered = [list(item) for item in ANCHORS[slug]]

    def fragment(title: str) -> str:
        """"DocC style fragment, used for headings that the live page doesn't have."""
        cleaned = re.sub(r"[^0-9A-Za-z\u00c0-\uffff -]", "", title)
        return re.sub(r"\s+", "-", cleaned).strip("-")

    def repl(match: re.Match[str]) -> str:
        hashes, title = match.group(1), match.group(2)
        if len(hashes) == 1:
            return f"{hashes} {title}"
        base = title.split(" {#")[0].strip()
        index = next(
            (
                i
                for i, (level, expected, _anchor) in enumerate(rendered)
                if level == len(hashes) and normalize(expected) == normalize(base)
            ),
            None,
        )
        if index is None:
            anchor = fragment(base)
        else:
            anchor = rendered[index][2]
            del rendered[: index + 1]
        return f"{hashes} {base} {{#{anchor}}}"

    return HEADING.sub(repl, text)


def prepare(slug: str, images: set[str]) -> str:
    page = PAGES[slug]
    source = (HERE / "swift-package-manager" / page["source"]).read_text(encoding="utf-8")
    text = strip_source(source)
    text = DOC_MD_LINK.sub(lambda m: replace_doc_md_link(m, slug), text)
    text = DOC_BARE_LINK.sub(lambda m: replace_doc_bare_link(m, slug), text)
    text = DOC_LINK.sub(lambda m: replace_doc_link(m, slug), text)
    text = copy_images(text, slug, images)
    text = join_wrapped_lines(text)
    text = add_anchors(text, slug)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip() + "\n"


def main() -> None:
    PREPARED.mkdir(exist_ok=True)
    images: dict[pathlib.Path, set[str]] = {}
    for slug in PAGES:
        target = PREPARED / f"{slug}.md"
        if target.exists() and target.stat().st_size > 0:
            continue
        text = prepare(slug, images)
        target.write_text(text, encoding="utf-8")
        print(f"prepared {slug}: {len(text)} bytes", flush=True)
    copied = 0
    for image_dir, names in images.items():
        image_dir.mkdir(parents=True, exist_ok=True)
        for name in sorted(names):
            stem, suffix = pathlib.Path(name).stem, pathlib.Path(name).suffix
            for candidate in (BOOK / "Assets" / f"{stem}{suffix}", BOOK / "Assets" / f"{stem}@2x{suffix}"):
                if candidate.exists():
                    import shutil

                    shutil.copyfile(candidate, image_dir / name)
                    copied += 1
                    break
    if copied:
        print(f"copied {copied} images to {len(images)} images folder(s)")
    print("done")


if __name__ == "__main__":
    main()
