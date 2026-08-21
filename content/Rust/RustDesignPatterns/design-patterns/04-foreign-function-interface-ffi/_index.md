+++
title = "04-外部函数接口（FFI）"
date = 2026-08-18T22:10:00+08:00
weight = 39
type = "docs"
description = "外部函数接口（FFI） — Rust Design Patterns"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Rust Design Patterns](https://rust-unofficial.github.io/patterns/)

> 原文链接: [https://rust-unofficial.github.io/patterns/patterns/ffi/intro.html](https://rust-unofficial.github.io/patterns/patterns/ffi/intro.html)

# 外部函数接口（FFI）

编写 FFI 代码本身就是一门完整课程。不过，这里有若干习语可以作为指引，并帮助不安全 Rust 的经验不足的用户避开陷阱。

本节包含在做 FFI 时可能有用的设计模式。

1. [基于对象的 API](01-object-based-apis/) 设计具有良好的内存安全特性，以及安全与不安全之间清晰的边界

2. [将类型收拢到包装器中](02-type-consolidation-into-wrappers/) — 将多个 Rust 类型组合进一个不透明的“对象”
