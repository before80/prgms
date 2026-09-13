#!/usr/bin/env python3
"""Combine the hand-written renderings into ``tools/option_zh.json``.

Sources:
  * ``pending_zh.json`` -- the English strings that had no rendering yet,
    plus ``zh_extra.py``'s two ordered lists (same order, zipped).
  * ``auto_zh.json``   -- pairs harvested from pages that were translated by
    hand and already pass ``verify.py``.
"""

from __future__ import annotations

import json
import pathlib

import zh_extra

HERE = pathlib.Path(__file__).resolve().parent


def main() -> None:
    pending = json.loads((HERE / "pending_zh.json").read_text(encoding="utf-8"))
    mapping: dict[str, str] = {}
    auto = HERE / "auto_zh.json"
    if auto.exists():
        mapping.update(json.loads(auto.read_text(encoding="utf-8")))

    for key, english, chinese in (
        ("italic", pending["italic"], zh_extra.ITALIC),
        ("plain", pending["plain"], zh_extra.PLAIN),
    ):
        if len(english) != len(chinese):
            raise SystemExit(f"{key}: {len(english)} 条原文 / {len(chinese)} 条译文，长度不一致")
        for en, zh in zip(english, chinese):
            mapping[en] = zh

    (HERE / "option_zh.json").write_text(
        json.dumps(mapping, ensure_ascii=False, indent=1, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"写入 {len(mapping)} 条译名到 tools/option_zh.json")


if __name__ == "__main__":
    main()
