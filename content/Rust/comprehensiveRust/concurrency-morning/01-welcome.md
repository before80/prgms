+++
title = "1 欢迎"
date = 2026-08-11T11:30:00+08:00
weight = 344
type = "docs"
description = "01-欢迎 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/concurrency/welcome.html](https://google.github.io/comprehensive-rust/concurrency/welcome.html)

# 1 欢迎

Rust 通过操作系统线程、互斥锁与通道，完整支持并发。

Rust 类型系统在让许多并发缺陷成为编译期错误方面扮演重要角色。这一理念称为 *fearless concurrency*（无畏并发）：你可以依赖编译器在运行时保证正确性。

## 日程

含每次 10 分钟休息，本时段约需 3 小时 20 分钟。内容包括：

| 小节 | 时长 |
| --- | --- |
| 线程 | 30 分钟 |
| 通道 | 20 分钟 |
| `Send` 与 `Sync` | 15 分钟 |
| 共享状态 | 30 分钟 |
| 练习 | 1 小时 10 分钟 |


> - Rust 让我们使用操作系统的并发工具箱：线程、同步原语等。
> - 类型系统在不引入特殊特性的情况下为我们提供并发安全。
> - 那些帮助单线程内「并发」访问的工具（例如被调用函数可能修改参数，或保存引用供稍后读取）同样能让我们远离多线程问题。

