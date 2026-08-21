+++
title = "第8章 风格版本"
date = 2026-08-18T22:00:00+08:00
weight = 90
type = "docs"
description = "风格版本 — The Rust Style Guide"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Style Guide](https://doc.rust-lang.org/nightly/style-guide/)

> 原文链接: [https://doc.rust-lang.org/nightly/style-guide/editions.html](https://doc.rust-lang.org/nightly/style-guide/editions.html)

# 风格版本

默认的 Rust 风格会随时间演进，一如 Rust 本身。不过，为避免破坏既有代码风格以及检查代码风格的 CI 任务，对默认 Rust 风格的变更只会出现在*风格版本*中。

以某一
[Rust 版本](https://doc.rust-lang.org/edition-guide/)
编写的代码，默认使用对应的 Rust 风格版本。为便于将代码风格迁移与 Rust 版本之间的语义变更分开进行，`rustfmt` 等格式化工具允许独立于 Rust 版本更新风格版本。

本风格指南的当前版本描述最新的 Rust 风格版本。每一种不同的过往风格都会有对应的风格指南归档版本。

请注意，风格指南的归档版本不会记录归档时尚不存在的较新 Rust 语法结构的格式。不过，每个风格版本仍会格式化该 Rust 版本中所有合法的语法结构；较新结构的风格来自随后第一个为该结构提供格式规则的风格版本（但不包含该风格版本中的系统性/全局变更）。

并非所有 Rust 版本都对应 Rust 风格的变更。例如，Rust 2015、Rust 2018 和 Rust 2021 都使用同一风格版本。

## 下一版 Rust 风格 {#rust-next-style-edition}

- 切勿在无参函数调用 `func()` 或单元字面量 `()` 内部换行。

## Rust 2024 风格版本 {#rust-2024-style-edition}

本风格指南描述的是 Rust 2024 风格版本。Rust 2024 风格版本目前仅限 nightly，并可能在 Rust 2024 发布前发生变化。

有关 Rust 2024 风格版本变更的完整历史，参见风格指南的 git 历史。Rust 2024 风格版本中的显著变更包括：

- 若干 `rustfmt` 缺陷修复。
- 使用版本排序（按 `x8`、`x16`、`x32`、`x64`、`x128` 这一顺序排序）。
- 将「ASCIIbetical」排序改为 Unicode 感知的「非小写字母排在小写字母之前」。

## Rust 2015/2018/2021 风格版本 {#rust-201520182021-style-edition}

位于
<https://github.com/rust-lang/rust/tree/37343f4a4d4ed7ad0891cb79e8eb25acf43fb821/src/doc/style-guide/src>
的风格指南归档版本，描述了对应于 Rust 2015、Rust 2018 和 Rust 2021 的风格版本。
