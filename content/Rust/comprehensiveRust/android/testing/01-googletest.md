+++
title = "5.1 GoogleTest"
date = 2026-08-11T11:30:00+08:00
weight = 231
type = "docs"
description = "01-GoogleTest — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/android/testing/googletest.html](https://google.github.io/comprehensive-rust/android/testing/googletest.html)

# 5.1 GoogleTest

[GoogleTest](https://docs.rs/googletest/) crate 允许使用 _matcher_ 做灵活的测试断言：

```rust
// Copyright 2024 Google LLC
// SPDX-License-Identifier: Apache-2.0
use googletest::prelude::*;

#[googletest::test]
fn test_elements_are() {
    let value = vec!["foo", "bar", "baz"];
    expect_that!(value, elements_are!(eq(&"foo"), lt(&"xyz"), starts_with("b")));
}
```

若把最后一个元素改成 `"!"`，测试会失败，并给出精确定位错误的结构化错误信息：

```text
---- test_elements_are stdout ----
Value of: value
Expected: has elements:
  0. is equal to "foo"
  1. is less than "xyz"
  2. starts with prefix "!"
Actual: ["foo", "bar", "baz"],
  where element #2 is "baz", which does not start with "!"
  at src/testing/googletest.rs:6:5
Error: See failure output above
```

> - GoogleTest 不在 Rust Playground 中，因此需要在本地环境运行本示例。使用 `cargo add googletest` 可快速把它加到现有 Cargo 项目。
>
> - `use googletest::prelude::*;` 这行会导入一组[常用宏与类型][prelude]。
>
> - 这只是皮毛，还有许多内置 matcher。建议阅读
>   [“Advanced testing for Rust applications”](https://rust-exercises.com/advanced-testing/)
>   的第一章，这是一门自引导的 Rust 课程：它提供对该库的引导式介绍，并配有练习，帮助你熟悉 `googletest` 宏、matcher 及其整体理念。
>
> - 一个特别好用的特性是：多行字符串中的不匹配会以 diff 形式显示：
>
> ```rust
> // Copyright 2024 Google LLC
> // SPDX-License-Identifier: Apache-2.0
> #[test]
> fn test_multiline_string_diff() {
>     let haiku = "Memory safety found,\n\
>                  Rust's strong typing guides the way,\n\
>                  Secure code you'll write.";
>     assert_that!(
>         haiku,
>         eq("Memory safety found,\n\
>             Rust's silly humor guides the way,\n\
>             Secure code you'll write.")
>     );
> }
> ```
>
> 会显示带颜色的 diff（此处不显示颜色）：
>
> ```text
>     Value of: haiku
> Expected: is equal to "Memory safety found,\nRust's silly humor guides the way,\nSecure code you'll write."
> Actual: "Memory safety found,\nRust's strong typing guides the way,\nSecure code you'll write.",
>   which isn't equal to "Memory safety found,\nRust's silly humor guides the way,\nSecure code you'll write."
> Difference(-actual / +expected):
>  Memory safety found,
> -Rust's strong typing guides the way,
> +Rust's silly humor guides the way,
>  Secure code you'll write.
>   at src/testing/googletest.rs:17:5
> ```
>
> - 该 crate 是 [GoogleTest for C++](https://google.github.io/googletest/) 的 Rust 移植。
>
> [prelude]: https://docs.rs/googletest/latest/googletest/prelude/index.html

