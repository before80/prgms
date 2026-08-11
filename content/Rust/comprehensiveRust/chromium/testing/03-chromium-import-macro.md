+++
title = "6.3 `chromium::import!` 宏"
date = 2026-08-11T11:30:00+08:00
weight = 268
type = "docs"
description = "03-`chromium::import!` 宏 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/chromium/testing/chromium-import-macro.html](https://google.github.io/comprehensive-rust/chromium/testing/chromium-import-macro.html)

# 6.3 `chromium::import!` 宏

在把 `:my_rust_lib` 加入 GN `deps` 之后，我们仍需了解如何从 `my_rust_lib_unittest.rs` 导入并使用 `my_rust_lib`。我们没有为 `my_rust_lib` 提供显式 `crate_name`，因此其 crate 名基于完整目标路径与名称计算。幸好我们可以使用自动导入的 `chromium` crate 中的 `chromium::import!` 宏，避免处理如此别扭的名字：

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
chromium::import! {
    "//ui/base:my_rust_lib";
}

use my_rust_lib::my_function_under_test;
```

在底层，该宏展开为类似这样的内容：

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
extern crate ui_sbase_cmy_urust_ulib as my_rust_lib;

use my_rust_lib::my_function_under_test;
```

更多信息见 `chromium::import` 宏的[文档注释][0]。

> `rust_static_library` 支持通过 `crate_name` 属性指定显式名称，但这样做不鼓励。不鼓励是因为 crate 名必须全局唯一。crates.io 保证其 crate 名的唯一性，因此 `cargo_crate` GN 目标（由稍后介绍的 `gnrt` 工具生成）使用短 crate 名。


[0]: https://source.chromium.org/chromium/chromium/src/+/main:build/rust/chromium_prelude/chromium_prelude.rs?q=f:chromium_prelude.rs%20pub.use.*%5Cbimport%5Cb;%20-f:third_party&ss=chromium%2Fchromium%2Fsrc
