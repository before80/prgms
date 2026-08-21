+++
title = "第19章 标准库类型"
date = 2026-08-20T21:20:00+08:00
weight = 158
type = "docs"
description = "标准库类型 — Rust By Example"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Rust By Example](https://doc.rust-lang.org/stable/rust-by-example/)

> 原文链接: [https://doc.rust-lang.org/stable/rust-by-example/std.html](https://doc.rust-lang.org/stable/rust-by-example/std.html)

# 标准库类型

标准库提供了很多自定义类型，在**原生类型**基础上进行了大量扩充。这是部分自定义类型：

* 可增长的 `String`（字符串），如: `"hello world"`
* 可增长的向量（vector）: `[1, 2, 3]`
* 选项类型（optional types）: `Option<i32>`
* 错误处理类型（error handling types）: `Result<i32, i32>`
* 堆分配的指针（heap allocated pointers）: `Box<i32>`

### 参见： {#参见}

[原生类型][primitives] 和 [标准库][std]

[primitives]: ../primitives/
[std]: https://rustwiki.org/zh-CN/std/
