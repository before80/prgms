+++
title = "02-偏好小型 crate"
date = 2026-08-18T22:10:00+08:00
weight = 36
type = "docs"
description = "偏好小型 crate — Rust Design Patterns"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Rust Design Patterns](https://rust-unofficial.github.io/patterns/)

> 原文链接: [https://rust-unofficial.github.io/patterns/patterns/structural/small-crates.html](https://rust-unofficial.github.io/patterns/patterns/structural/small-crates.html)

# 偏好小型 crate

## 描述 {#description}

偏好只把一件事做好的小型 crate。

Cargo 与 crates.io 使添加第三方库变得容易，远胜于例如 C 或 C++。此外，由于 crates.io 上的包在发布后不能被编辑或移除，现在能工作的任何构建在将来也应当继续工作。我们应当利用这些工具，使用更小、更细粒度的依赖。

## 优点 {#advantages}

- 小型 crate 更易于理解，并鼓励更模块化的代码。
- Crate 允许在项目之间复用代码。例如，`url` crate 是作为 Servo 浏览器引擎的一部分开发的，但此后在项目之外也得到了广泛使用。
- 由于 Rust 的编译单元是 crate，将项目拆分为多个 crate 可以让更多代码并行构建。

## 缺点 {#disadvantages}

- 这可能导致“依赖地狱”，即项目同时依赖某个 crate 的多个冲突版本。例如，`url` crate 同时有 1.0 和 0.5 版本。由于来自 `url:1.0` 的 `Url` 与来自 `url:0.5` 的 `Url` 是不同的类型，使用 `url:0.5` 的 HTTP 客户端不会接受使用 `url:1.0` 的网页抓取器给出的 `Url` 值。
- crates.io 上的包未经策展。某个 crate 可能写得很差、文档无用，甚至可能是恶意的。
- 两个小型 crate 可能不如一个大型 crate 优化得好，因为编译器默认不执行链接时优化（LTO）。

## 示例 {#examples}

[`url`](https://crates.io/crates/url) crate 提供用于处理 URL 的工具。

[`num_cpus`](https://crates.io/crates/num_cpus) crate 提供查询机器 CPU 数量的函数。

[`ref_slice`](https://crates.io/crates/ref_slice) crate 提供将 `&T` 转换为 `&[T]` 的函数。（历史示例）

## 参见 {#see-also}

- [crates.io：Rust 社区的 crate 托管站点](https://crates.io/)
