+++
title = "03-把不安全封装在小模块中"
date = 2026-08-18T22:10:00+08:00
weight = 37
type = "docs"
description = "把不安全封装在小模块中 — Rust Design Patterns"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Rust Design Patterns](https://rust-unofficial.github.io/patterns/)

> 原文链接: [https://rust-unofficial.github.io/patterns/patterns/structural/unsafe-mods.html](https://rust-unofficial.github.io/patterns/patterns/structural/unsafe-mods.html)

# 把不安全封装在小模块中

## 描述 {#description}

若你有 `unsafe` 代码，创建尽可能小的、能维护所需不变量的模块，以便在其上构建最小的安全接口。将它嵌入到一个更大的、只包含安全代码并提供符合人体工程学接口的模块中。注意，外层模块可以包含直接调用不安全代码的 `unsafe` 函数和方法。用户可以利用这一点获得性能收益。

## 优点 {#advantages}

- 这限制了必须审计的不安全代码范围
- 编写外层模块容易得多，因为你可以依赖内层模块的保证

## 缺点 {#disadvantages}

- 有时可能很难找到合适的接口。
- 抽象可能引入低效。

## 示例 {#examples}

- [`toolshed`](https://docs.rs/toolshed) crate 将其不安全操作放在子模块中，向用户呈现安全接口。
- `std` 的 `String` 类是 `Vec<u8>` 的包装器，额外不变量是内容必须是有效的 UTF-8。对 `String` 的操作确保这一行为。然而，用户可以选择使用 `unsafe` 方法创建 `String`，此时保证内容有效的责任落在他们身上。

## 参见 {#see-also}

- [Ralf Jung 关于不安全代码中不变量的博客](https://www.ralfj.de/blog/2018/08/22/two-kinds-of-invariants.html)
