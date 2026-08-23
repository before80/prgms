+++
title = "3 Lint"
date = 2026-08-23T13:57:00+08:00
weight = 4
type = "docs"
description = "Clippy 与性能相关 lint"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Rust Performance Book](https://nnethercote.github.io/perf-book/)

# Lint {#linting}


> 原文链接: [https://nnethercote.github.io/perf-book/linting.html](https://nnethercote.github.io/perf-book/linting.html)


[Clippy] 是一组用于捕获 Rust 代码中常见错误的 lint。它是运行 Rust 代码的出色工具。它也有助于性能，因为其中许多 lint 与可能导致次优性能的代码模式有关。

鉴于自动检测问题优于手动检测，本书其余部分将不再提及 Clippy 默认能检测到的性能问题。

## 基础

[Clippy]: https://github.com/rust-lang/rust-clippy

安装后，运行很简单：
```text
cargo clippy
```
完整的性能 lint 列表可通过访问 [lint 列表][lint list]并取消选择除「Perf」以外的所有 lint 组来查看。

[lint list]: https://rust-lang.github.io/rust-clippy/master/

除了使代码更快之外，性能 lint 建议通常还会使代码更简单、更符合惯用法，因此即使对于不常执行的代码也值得遵循。

反之，一些非性能 lint 建议可以改善性能。例如，[`ptr_arg`] 风格 lint 建议将各种容器参数改为切片，例如将 `&mut Vec<T>` 参数改为 `&mut [T]`。这里的主要动机是切片提供更灵活的 API，但由于减少了间接访问并为编译器提供了更好的优化机会，也可能产生更快的代码。
[**示例**](https://github.com/fschutt/fastblur/pull/3/files)。

[`ptr_arg`]: https://rust-lang.github.io/rust-clippy/master/index.html#ptr_arg

## 禁止特定类型 {#disallowing-types}

在后续章节中，我们将看到有时值得避免使用某些标准库类型，转而使用更快的替代方案。如果你决定使用这些替代方案，很容易在某些地方误用标准库类型。

你可以使用 Clippy 的 [`disallowed_types`] lint 来避免此问题。例如，要禁止使用标准哈希表（原因见[哈希][Hashing]一节），在代码中添加包含以下内容的 `clippy.toml` 文件。
```toml
disallowed-types = ["std::collections::HashMap", "std::collections::HashSet"]
```

[Hashing]: ../6-hashing/
[`disallowed_types`]: https://rust-lang.github.io/rust-clippy/master/index.html#disallowed_types
