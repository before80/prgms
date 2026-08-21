+++
title = "01-内存分配与生命周期"
date = 2026-08-18T08:45:00+08:00
weight = 103
type = "docs"
description = "内存分配与生命周期 — The Rust Reference"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Reference](https://doc.rust-lang.org/reference/)

> 原文链接: [https://doc.rust-lang.org/reference/memory-allocation-and-lifetime.html](https://doc.rust-lang.org/reference/memory-allocation-and-lifetime.html)

r[alloc]
# 内存分配与生命周期

r[alloc.static]
程序的*项*是那些在编译时计算其值、并唯一存储在 rust 进程内存映像中的函数、模块与类型。项既不会被动态分配，也不会被释放。

r[alloc.dynamic]
*堆*是描述 box 的通用术语。堆中一次分配的生命周期取决于指向它的 box 值的生命周期。由于 box 值本身可能传入传出栈帧，或存储在堆中，堆分配可能比分配它的栈帧存活更久。堆中的一次分配保证在其整个生命周期内位于堆中的同一位置——绝不会因移动 box 值而被重定位。
