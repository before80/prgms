#!/usr/bin/env python3
"""Registry for the SwiftUI documentation tree.

The order and hierarchy come from Apple's navigator index
(``.source/swiftui_index.json``); only pages published under
``/documentation/swiftui`` are translated, other frameworks' pages stay
external links.
"""

from __future__ import annotations

import json
import pathlib
import re

HERE = pathlib.Path(__file__).resolve().parent.parent
REPO = HERE.parents[2]          # .../content
OUTPUT_ROOT = "Swift/SwiftUI"

SECTION_DIRS = {
    "Essentials": "essentials",
    "App structure": "appstructure",
    "Data and storage": "datastorage",
    "Views": "views",
    "View layout": "viewlayout",
    "Event handling": "eventhandling",
    "Accessibility": "accessibility",
    "Framework integration": "frameworkintegration",
    "Tool support": "toolsupport",
}

TITLES_ZH_FILE = HERE / "tools" / "titles_zh.json"


def _pascal(slug: str) -> str:
    parts = re.split(r"[-_]", slug)
    return "".join(p[:1].upper() + p[1:] for p in parts if p)


def _titles_zh() -> dict[str, str]:
    if TITLES_ZH_FILE.exists():
        return json.loads(TITLES_ZH_FILE.read_text(encoding="utf-8"))
    return {}


def pages():
    manifest = json.loads((HERE / "nav_manifest.json").read_text(encoding="utf-8"))
    cn = _titles_zh()
    by_slug = {m["slug"]: m for m in manifest}
    counters: dict[str, int] = {}
    child_counters: dict[str, int] = {}
    result = []

    for entry in manifest:
        section = entry["section"]
        directory = SECTION_DIRS[section]
        counters.setdefault(section, 0)
        if entry["parent"] is None:
            counters[section] += 1
            number = str(counters[section])
            parent_dir = None
        else:
            key = entry["parent"]
            child_counters.setdefault(key, 0)
            child_counters[key] += 1
            parent_entry = next(
                (r for r in result if r["slug"] == entry["parent"]), None
            )
            parent_number = parent_entry["number"] if parent_entry else "0"
            number = f"{parent_number}.{child_counters[key]}"
            parent_dir = parent_entry["stem"] if parent_entry else None

        stem = f"{number}-{_pascal(entry['slug'])}"
        if parent_dir:
            base = f"{OUTPUT_ROOT}/{directory}/{parent_dir}"
            file = (
                f"{base}/_index.md"
                if entry["slug"] == entry["parent"]
                else f"{base}/{stem}.md"
            )
        else:
            file = f"{OUTPUT_ROOT}/{directory}/{stem}.md"

        result.append(
            {
                "slug": entry["slug"],
                "title_en": entry["title"],
                "cn_title": cn.get(entry["slug"], entry["title"]),
                "kind": entry["type"],
                "section": section,
                "section_dir": directory,
                "parent": entry["parent"],
                "stem": stem,
                "number": number,
                "weight": int(number.split(".")[-1]),
                "file": file,
                "url_dir": "/" + str(pathlib.PurePosixPath(file).parent) + f"/{stem}/",
                "path": entry["path"],
            }
        )

    # 有子章节的页面本身是目录索引
    parents = {r["parent"] for r in result if r["parent"]}
    for page in result:
        if page["slug"] in parents:
            base = f"{OUTPUT_ROOT}/{page['section_dir']}/{page['stem']}"
            page["file"] = f"{base}/_index.md"
            page["url_dir"] = f"/{base}/"
    return result


def as_dict():
    return {page["slug"]: page for page in pages()}


def root_page():
    return {
        "slug": "__root__",
        "file": f"{OUTPUT_ROOT}/_index.md",
        "url_dir": f"/{OUTPUT_ROOT}/",
    }


if __name__ == "__main__":
    print(json.dumps(pages(), indent=1, ensure_ascii=False))
