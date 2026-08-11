+++
title = "4.7 练习：ROT13"
date = 2026-08-11T11:30:00+08:00
weight = 119
type = "docs"
description = "练习：ROT13 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/std-traits/exercise.html](https://google.github.io/comprehensive-rust/std-traits/exercise.html)

# 4.7 练习：ROT13

在本例中，你将实现经典的
["ROT13" 密码](https://en.wikipedia.org/wiki/ROT13)。把这段代码复制到 playground，并实现缺失部分。只旋转 ASCII 字母字符，以确保结果仍是有效的 UTF-8。

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
use std::io::Read;

struct RotDecoder<R: Read> {
    input: R,
    rot: u8,
}

// 为 `RotDecoder` 实现 `Read` trait。

#[cfg(test)]
mod test {
    use super::*;

    #[test]
    fn joke() {
        let mut rot =
            RotDecoder { input: "Gb trg gb gur bgure fvqr!".as_bytes(), rot: 13 };
        let mut result = String::new();
        rot.read_to_string(&mut result).unwrap();
        assert_eq!(&result, "To get to the other side!");
    }

    #[test]
    fn binary() {
        let input: Vec<u8> = (0..=255u8).collect();
        let mut rot = RotDecoder::<&[u8]> { input: input.as_slice(), rot: 13 };
        let mut buf = [0u8; 256];
        assert_eq!(rot.read(&mut buf).unwrap(), 256);
        for i in 0..=255 {
            if input[i] != buf[i] {
                assert!(input[i].is_ascii_alphabetic());
                assert!(buf[i].is_ascii_alphabetic());
            }
        }
    }
}
```

若把两个 `RotDecoder` 实例串起来，每个都旋转 13 个字符，会发生什么？
