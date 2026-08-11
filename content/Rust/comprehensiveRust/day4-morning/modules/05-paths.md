+++
title = "3.5 `use`、`super`、`self`"
date = 2026-08-11T11:30:00+08:00
weight = 175
type = "docs"
description = "05-`use`、`super`、`self` — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/modules/paths.html](https://google.github.io/comprehensive-rust/modules/paths.html)

# 3.5 `use`、`super`、`self`

模块可以用 `use` 把另一个模块中的符号引入作用域。每个模块顶部通常会看到类似这样的写法：

```rust
// Copyright 2022 Google LLC
// SPDX-License-Identifier: Apache-2.0
use std::collections::HashSet;
use std::process::abort;
```

## 路径

路径按如下方式解析：

1. 作为相对路径：
   - `foo` 或 `self::foo` 指当前模块中的 `foo`，
   - `super::foo` 指父模块中的 `foo`。

2. 作为绝对路径：
   - `crate::foo` 指当前 crate 根中的 `foo`，
   - `bar::foo` 指 `bar` crate 中的 `foo`。

> - 常见做法是在更短的路径上「再导出」（re-export）符号。例如，crate 顶层的 `lib.rs` 可能写成：
>
>   ```rust
>   // Copyright 2022 Google LLC
>   // SPDX-License-Identifier: Apache-2.0
>   #
>   mod storage;
>
>   pub use storage::disk::DiskStorage;
>   pub use storage::network::NetworkStorage;
>   ```
>
>   这样其他 crate 就能用方便、简短的路径使用 `DiskStorage` 和 `NetworkStorage`。
>
> - 大体上，只有出现在模块中的项才需要 `use`。但要调用某个 trait 上的方法，该 trait 必须在作用域中——即便已实现该 trait 的类型已经在作用域中。例如，要对实现了 `Read` trait 的类型调用 `read_to_string`，需要 `use std::io::Read`。
>
> - `use` 语句可以使用通配符：`use std::io::*`。不鼓励这样做，因为不清楚导入了哪些项，而且这些项可能随时间变化。

