+++
title = "Clippy 文档"
date = 2026-08-22T18:00:00+08:00
weight = 1
type = "docs"
description = "Clippy 简介与 lint 分类概览"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Clippy Documentation](https://doc.rust-lang.org/nightly/clippy/)

# 简介 {#introduction}


> 原文链接: [https://doc.rust-lang.org/nightly/clippy/index.html](https://doc.rust-lang.org/nightly/clippy/index.html)


[![License: MIT OR Apache-2.0](https://img.shields.io/crates/l/clippy.svg)](https://github.com/rust-lang/rust-clippy#license)

一组用于发现常见错误并改进 [Rust](https://github.com/rust-lang/rust) 代码的 lint。

[本 crate 中包含 800 多个 lint！](https://rust-lang.github.io/rust-clippy/master/index.html)

Lint 按类别划分，每个类别都有默认的 [lint 级别](https://doc.rust-lang.org/rustc/lints/levels.html)。你可以通过按类别调整 lint 级别，来控制 Clippy 对你的「帮助」程度。

| 类别 | 说明 | 默认级别 |
|-----------------------|-------------------------------------------------------------------------------------|---------------|
| `clippy::all` | 默认启用的所有 lint（correctness、suspicious、style、complexity、perf） | **warn/deny** |
| `clippy::correctness` | 明显错误或毫无用处的代码 | **deny** |
| `clippy::suspicious` | 很可能错误或毫无用处的代码 | **warn** |
| `clippy::style` | 应以更地道方式编写的代码 | **warn** |
| `clippy::complexity` | 用复杂方式完成简单事情的代码 | **warn** |
| `clippy::perf` | 可以写得更快运行的代码 | **warn** |
| `clippy::pedantic` | 相当严格或偶有误报的 lint | allow |
| `clippy::restriction` | 限制使用某些语言与库特性的 lint[^restrict] | allow |
| `clippy::nursery` | 仍在开发中的新 lint | allow |
| `clippy::cargo` | 针对 Cargo manifest 的 lint | allow |

更多内容敬请期待；如有想法请 [提交 issue](https://github.com/rust-lang/rust-clippy/issues)！

`restriction` 类别**绝不应**整体启用。其中 lint 可能针对完全合理的代码、可能没有替代建议，也可能与其他 lint（包括其他类别）冲突。启用前应逐个 lint 权衡。

[^restrict]: `restriction` lint 的一些用例包括：
    - 严格的编码风格（例如 [`clippy::else_if_without_else`]）。
    - 在 CI 上附加限制（例如 [`clippy::todo`]）。
    - 禁止在特定函数中 panic（例如 [`clippy::unwrap_used`]）。
    - 仅在代码子集上运行某个 lint（例如在模块上使用 `#[forbid(clippy::float_arithmetic)]`）。

[`clippy::else_if_without_else`]: https://rust-lang.github.io/rust-clippy/master/index.html#else_if_without_else
[`clippy::todo`]: https://rust-lang.github.io/rust-clippy/master/index.html#todo
[`clippy::unwrap_used`]: https://rust-lang.github.io/rust-clippy/master/index.html#unwrap_used
