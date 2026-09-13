#!/usr/bin/env python3
"""Turn the upstream DocC markdown of every chapter into a *prepared*
English markdown file that is easy to translate:

  * DocC directives and the test-support HTML comments are dropped
  * every heading gets the anchor that the rendered page uses, written as
    a Hugo/goldmark attribute:  ``## Some Heading {#Some-Anchor}``
  * ``<doc:Chapter#Anchor>`` links become ordinary relative links that
    already point at the final Docsy URL of the target page
  * images are copied to the output tree and referenced with a relative path
  * hard-wrapped paragraphs are joined into one line per paragraph

The result is stored in .source/prepared/<Slug>.md and is kept as part of
the preserved source material.
"""

from __future__ import annotations

import json
import pathlib
import re
import shutil

import registry

HERE = pathlib.Path(__file__).resolve().parent.parent
BOOK = HERE / "swift-book" / "TSPL.docc"
JSON_DIR = HERE / "docc-json"
PREPARED = HERE / "prepared"
REPO = HERE.parents[2]  # .../content

PAGES = registry.as_dict()


def load_anchors(slug: str):
    data = json.loads((JSON_DIR / f"{slug}.json").read_text(encoding="utf-8"))
    headings = []
    for section in data.get("primaryContentSections", []):
        for block in section.get("content", []):
            if block.get("type") == "heading":
                headings.append((block["level"], block["text"], block["anchor"]))
    return headings


ANCHOR_TEXT = {}
ANCHORS = {}
for _slug in PAGES:
    _headings = load_anchors(_slug)
    ANCHORS[_slug] = _headings
    ANCHOR_TEXT[_slug] = {anchor: text for _level, text, anchor in _headings}

ANCHOR_TEXT["The-Swift-Programming-Language"] = {}


def relative_url(current_url_dir: str, target_url_dir: str) -> str:
    """Relative link from one page URL directory to another page URL directory."""
    current = [part for part in current_url_dir.strip("/").split("/") if part]
    target = [part for part in target_url_dir.strip("/").split("/") if part]
    common = 0
    while common < len(current) and common < len(target) and current[common] == target[common]:
        common += 1
    up = [".."] * (len(current) - common)
    parts = up + target[common:]
    if not parts:
        return "./"
    return "/".join(parts) + "/"


def page_url_dir(slug: str) -> str:
    if slug == "The-Swift-Programming-Language":
        return f"/{registry.OUTPUT_ROOT}/"
    page = PAGES[slug]
    return page["url_dir"]


def link_text(slug: str, anchor: str | None) -> str:
    if anchor and anchor in ANCHOR_TEXT.get(slug, {}):
        return ANCHOR_TEXT[slug][anchor]
    if slug == "The-Swift-Programming-Language":
        return "The Swift Programming Language"
    if anchor:
        return anchor.replace("-", " ")
    return PAGES[slug]["cn_title"] if False else title_en(slug)


def title_en(slug: str) -> str:
    """English title of a chapter, taken from its DocC metadata."""
    data = json.loads((JSON_DIR / f"{slug}.json").read_text(encoding="utf-8"))
    return data["metadata"]["title"]


TITLES_EN = {slug: title_en(slug) for slug in PAGES}
TITLES_EN["The-Swift-Programming-Language"] = "The Swift Programming Language"


DOC_LINK = re.compile(r"<doc:([A-Za-z]+)(?:#([^>]+))?>")


def replace_doc_link(match: re.Match[str], current_slug: str) -> str:
    slug, anchor = match.group(1), match.group(2)
    if slug not in PAGES:
        raise SystemExit(f"unknown chapter reference: {slug}")
    target = relative_url(page_url_dir(current_slug), page_url_dir(slug))
    if anchor:
        target += f"#{anchor}"
    text = ANCHOR_TEXT[slug].get(anchor) if anchor else None
    if text is None:
        text = TITLES_EN[slug]
    return f"[{text}]({target})"


IMAGE = re.compile(r"!\[([^\]]*)\]\(([^)\s]+)\)")


def image_target_dir(slug: str) -> pathlib.Path:
    """Every top-level section keeps its own ``images`` folder.

    Images are copied next to the chapter files of their section and are
    referenced from the translated markdown as ``./images/<name>``.
    """
    return (REPO / PAGES[slug]["file"]).parent / "images"


def media_for(name: str) -> pathlib.Path | None:
    for candidate in (
        BOOK / "Assets" / f"{name}@2x.png",
        BOOK / "Assets" / f"{name}.png",
        BOOK / "Assets" / f"{name}.jpg",
        BOOK / "Assets" / f"{name}@2x.jpg",
    ):
        if candidate.exists():
            return candidate
    return None


def copy_images(
    text: str, current_slug: str, images: dict[pathlib.Path, set[str]]
) -> str:
    def repl(match: re.Match[str]) -> str:
        alt, name = match.group(1), match.group(2)
        if name.startswith("http") or name.startswith("../"):
            return match.group(0)
        source = media_for(name)
        if source is None:
            raise SystemExit(f"missing image asset: {name}")
        suffix = source.suffix
        target_name = f"{name}{suffix}"
        images.setdefault(image_target_dir(current_slug), set()).add(target_name)
        return f"![{alt}](./images/{target_name})"

    return IMAGE.sub(repl, text)


COMMENTS = re.compile(r"<!--.*?-->", re.DOTALL)
DIRECTIVE = re.compile(r"^@(Metadata|Options|AutomaticSeeAlso)[^\n]*\n(?:.*?\n)*?\}\n", re.MULTILINE)


def strip_source(text: str) -> str:
    text = COMMENTS.sub("", text)
    text = DIRECTIVE.sub("", text)
    return text


BLOCK_START = re.compile(
    r"^(#{1,6}\s|\s*```|>\s*$|>\s|>\S|\*\s|-\s|\+\s|\d+[.)]\s|\||@[A-Za-z]+\b|\[[^\]]+\]:\s)"
)


def join_wrapped_lines(text: str) -> str:
    """Join hard-wrapped lines of a paragraph into a single line."""
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
            and not re.match(r"^\[[^\]]+\]:\s*$", previous.strip())
            and not previous.strip().startswith("```")
            and not previous.endswith("\\")
            and not previous.rstrip().endswith("  ")
            and not previous.strip().endswith("|")
        ):
            out[-1] = previous.rstrip() + " " + line.strip()
        else:
            out.append(line)
    return "\n".join(out)


HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*$", re.MULTILINE)

TYPOGRAPHY = {
    "\u2019": "'",
    "\u2018": "'",
    "\u201c": '"',
    "\u201d": '"',
    "\u2014": "-",
    "\u2013": "-",
    "\u00a0": " ",
}


def normalize(text: str) -> str:
    for source, target in TYPOGRAPHY.items():
        text = text.replace(source, target)
    return " ".join(text.split())


def add_anchors(text: str, slug: str) -> str:
    anchors = iter(ANCHORS[slug])
    headings = list(HEADING.finditer(text))
    level_two = [m for m in headings if len(m.group(1)) > 1]

    def repl(match: re.Match[str]) -> str:
        hashes, title = match.group(1), match.group(2)
        if len(hashes) == 1:
            return f"{hashes} {title}"
        level, expected_text, anchor = next(anchors)
        if level != len(hashes):
            raise SystemExit(f"heading level mismatch in {slug}: {title!r}")
        base = title.split(" {#")[0].strip()
        if normalize(base) != normalize(expected_text):
            raise SystemExit(f"heading text mismatch in {slug}:\n  md:   {base!r}\n  docc: {expected_text!r}")
        return f"{hashes} {base} {{#{anchor}}}"

    result = HEADING.sub(repl, text)
    leftover = [a for a in anchors]
    if leftover:
        raise SystemExit(f"{len(leftover)} unused anchors in {slug}")
    if len(level_two) != len(ANCHORS[slug]):
        raise SystemExit(f"heading count mismatch in {slug}")
    return result


def prepare(slug: str, images: dict[pathlib.Path, set[str]]) -> str:
    page = PAGES[slug]
    source = (BOOK / page["source"].replace("TSPL.docc/", "")).read_text(encoding="utf-8")
    text = strip_source(source)
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
        text = prepare(slug, images)
        (PREPARED / f"{slug}.md").write_text(text, encoding="utf-8")
        print(f"prepared {slug}: {len(text)} bytes", flush=True)

    copied = 0
    for image_dir, names in images.items():
        image_dir.mkdir(parents=True, exist_ok=True)
        for name in sorted(names):
            source = media_for(pathlib.Path(name).stem)
            if source is None:
                raise SystemExit(f"missing image asset: {name}")
            shutil.copyfile(source, image_dir / name)
            copied += 1
    print(f"copied {copied} images to {len(images)} images folder(s)")


if __name__ == "__main__":
    main()
