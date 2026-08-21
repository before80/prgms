+++
title = "09-外部函数接口（FFI）"
date = 2026-08-18T22:10:00+08:00
weight = 13
type = "docs"
description = "外部函数接口（FFI） — Rust Design Patterns"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Rust Design Patterns](https://rust-unofficial.github.io/patterns/)

> 原文链接: [https://rust-unofficial.github.io/patterns/idioms/ffi/intro.html](https://rust-unofficial.github.io/patterns/idioms/ffi/intro.html)

# 外部函数接口（FFI）

编写 FFI 代码本身就可以单独开一门课。不过，这里有若干惯用法可以作为指引，帮助不熟悉 `unsafe` Rust 的人避开陷阱。

本节收录在进行 FFI 时可能有用的惯用法。

1. [地道的错误处理](01-idiomatic-errors/) — 用整数错误码和哨兵返回值（例如 `NULL` 指针）处理错误

2. [接受字符串](02-accepting-strings/)：尽量减少 `unsafe` 代码

3. [传递字符串](03-passing-strings/) 给 FFI 函数
