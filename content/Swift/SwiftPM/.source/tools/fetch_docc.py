#!/usr/bin/env python3
"""Download the rendered page JSON for every page of the Swift Package Manager
documentation from https://docs.swift.org/latest/ .

The downloaded files are kept as-is under .source/docc-json/ so that the
original chapter sources are preserved.
"""

import json
import pathlib
import time
import urllib.request

import registry

BASE = "https://docs.swift.org/latest"
BOOK = "packagemanagerdocs"
OUT = registry.HERE / "docc-json"


def get(url: str, attempts: int = 5) -> bytes:
    last: Exception | None = None
    for attempt in range(attempts):
        try:
            with urllib.request.urlopen(url, timeout=30) as response:
                return response.read()
        except Exception as error:  # noqa: BLE001 - retry on any network problem
            last = error
            time.sleep(2 + attempt)
    raise SystemExit(f"failed to download {url}: {last}")


def main() -> None:
    OUT.mkdir(exist_ok=True)
    (OUT / "index.json").write_bytes(get(f"{BASE}/data/documentation/{BOOK}.json"))
    for page in registry.flat_pages():
        slug = page["slug"]
        target = OUT / f"{slug}.json"
        if target.exists() and target.stat().st_size > 0:
            continue
        data = get(f"{BASE}/data/documentation/{BOOK}/{slug.lower()}.json")
        target.write_bytes(data)
        print("saved", slug, len(data), flush=True)


if __name__ == "__main__":
    main()
