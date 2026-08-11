+++
title = "2.2.1.5 With：复制并修改"
date = 2026-08-11T11:30:00+08:00
weight = 405
type = "docs"
description = "05-With：复制并修改 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/idiomatic/foundations-api-design/predictable-api/naming-conventions/with-copy-setter.html](https://google.github.io/comprehensive-rust/idiomatic/foundations-api-design/predictable-api/naming-conventions/with-copy-setter.html)

# 2.2.1.5 With：复制并修改

当值被复制，同时又以特定方式被修改时，会出现 `with`。

`with` 意为“像 `<value>`，但有某处不同。”

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
impl Path {
    // 简化。"/home/me/mortgage.pdf".with_extension("mov") =>
    // "/home/me/mortgage.mov"
    fn with_extension(&self, ext: &OsStr) -> PathBuf;
}
```

> - `with` 可用于复制一个值、但随后修改该值某一部分的方法。
>
>   在本例中，`with_extension` 把 `&Path` 的数据复制到新的 `PathBuf`，但把扩展名改成别的。
>
>   原来的 `Path` 不变。

