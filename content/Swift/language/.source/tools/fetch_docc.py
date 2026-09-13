#!/usr/bin/env python3
"""Download the rendered page data (JSON) for every page of
The Swift Programming Language from https://docs.swift.org/latest/ .

The files are kept as-is under .source/docc-json/ so that the original
downloaded chapter sources are preserved.
"""

import json
import os
import pathlib
import urllib.request

BASE = "https://docs.swift.org/latest"
BOOK = "the-swift-programming-language"
HERE = pathlib.Path(__file__).resolve().parent.parent
OUT = HERE / "docc-json"


def get(url: str) -> bytes:
    with urllib.request.urlopen(url, timeout=30) as response:
        return response.read()


def main() -> None:
    OUT.mkdir(exist_ok=True)
    index = json.loads(get(f"{BASE}/data/documentation/{BOOK}.json"))
    (OUT / "The-Swift-Programming-Language.json").write_bytes(
        get(f"{BASE}/data/documentation/{BOOK}.json")
    )

    entries = []
    for section in index["topicSections"]:
        for identifier in section["identifiers"]:
            slug = identifier.rsplit("/", 1)[-1]
            page = f"{BASE}/documentation/{BOOK}/{slug.lower()}/"
            data = get(f"{BASE}/data/documentation/{BOOK}/{slug.lower()}.json")
            (OUT / f"{slug}.json").write_bytes(data)
            entries.append(
                {
                    "section": section["title"],
                    "slug": slug,
                    "page": page,
                    "json": f"{BASE}/data/documentation/{BOOK}/{slug.lower()}.json",
                }
            )
            print("saved", slug, len(data), flush=True)

    (OUT / "_meta.json").write_text(
        json.dumps(entries, indent=1, ensure_ascii=False), encoding="utf-8"
    )
    print("total pages:", len(entries))


if __name__ == "__main__":
    main()
