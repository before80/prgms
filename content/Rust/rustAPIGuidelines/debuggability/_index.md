+++
title = "第9章 可调试性"
date = 2026-08-18T21:50:00+08:00
weight = 110
type = "docs"
description = "可调试性 — Rust API Guidelines"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Rust API Guidelines](https://rust-lang.github.io/api-guidelines/)

> 原文链接: [https://rust-lang.github.io/api-guidelines/debuggability.html](https://rust-lang.github.io/api-guidelines/debuggability.html)

# 可调试性

## 所有公开类型实现 `Debug` (C-DEBUG) {#c-debug}

即便有例外，也极为少见。

## `Debug` 表示永不空 (C-DEBUG-NONEMPTY) {#c-debug-nonempty}

即便对于概念上为空的值，`Debug` 表示也永不应当为空。

```rust
let empty_str = "";
assert_eq!(format!("{:?}", empty_str), "\"\"");

let empty_vec = Vec::<bool>::new();
assert_eq!(format!("{:?}", empty_vec), "[]");
```
