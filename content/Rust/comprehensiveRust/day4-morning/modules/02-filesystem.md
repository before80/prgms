+++
title = "3.2 文件系统层次结构"
date = 2026-08-11T11:30:00+08:00
weight = 172
type = "docs"
description = "02-文件系统层次结构 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/modules/filesystem.html](https://google.github.io/comprehensive-rust/modules/filesystem.html)

# 3.2 文件系统层次结构

省略模块内容会告诉 Rust 到另一个文件中查找：

```rust
// Copyright 2022 Google LLC
// SPDX-License-Identifier: Apache-2.0
mod garden;
```

这表示 `garden` 模块的内容位于 `src/garden.rs`。类似地，`garden::vegetables` 模块可以位于 `src/garden/vegetables.rs`。

`crate` 根位于：

- `src/lib.rs`（库 crate）
- `src/main.rs`（二进制 crate）

文件中定义的模块也可以用「内部文档注释」（inner doc comments）来写文档。这类注释记录的是*包含它们的项*——此处即模块本身。

```rust
// Copyright 2022 Google LLC
// SPDX-License-Identifier: Apache-2.0
//! 本模块实现花园，包括高性能的发芽实现。

// 再导出本模块中的类型。
pub use garden::Garden;
pub use seeds::SeedPacket;

/// 播种给定的种子包。
pub fn sow(seeds: Vec<SeedPacket>) {
    todo!()
}

/// 收获花园中已成熟的产物。
pub fn harvest(garden: &mut Garden) {
    todo!()
}
```

> - 在 Rust 2018 之前，模块需要放在 `module/mod.rs` 而不是 `module.rs`；2018 及之后的 edition 仍支持这种写法。
>
> - 引入 `filename.rs` 作为 `filename/mod.rs` 的替代方案，主要是因为大量名为 `mod.rs` 的文件在 IDE 中难以区分。
>
> - 即便主模块是单个文件，更深层的嵌套仍可使用文件夹：
>
>   ```ignore
>   src/
>   ├── main.rs
>   ├── top_module.rs
>   └── top_module/
>       └── sub_module.rs
>   ```
>
> - 可以用编译器指令改变 Rust 查找模块的位置：
>
>   ```rust
>   // Copyright 2022 Google LLC
>   // SPDX-License-Identifier: Apache-2.0
>   #
>   #[path = "some/path.rs"]
>   mod some_module;
>   ```
>
>   例如，若希望把某个模块的测试放在名为 `some_module_test.rs` 的文件中（类似 Go 的惯例），这就很有用。

