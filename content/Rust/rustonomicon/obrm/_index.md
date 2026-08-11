+++
title = "第6章 基于所有权的资源管理"
date = 2026-08-06T17:08:00+08:00
weight = 31
type = "docs"
description = "OBRM：构造、析构与泄漏"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [The Rustonomicon](https://doc.rust-lang.org/nomicon/)

# 基于所有权的资源管理


> 原文链接: [https://doc.rust-lang.org/nomicon/obrm.html](https://doc.rust-lang.org/nomicon/obrm.html)


　　OBRM（亦称 RAII：Resource Acquisition Is Initialization，资源获取即初始化）是 Rust 中你会频繁接触的模式。尤其使用标准库时。

　　大致模式如下：获取资源时，创建管理它的对象。释放资源时，只需销毁对象，它会替你清理资源。此模式管理的常见「资源」就是*内存*。`Box`、`Rc` 以及 `std::collections` 中几乎所有类型，都是便于正确管理内存的便利工具。这在 Rust 中尤其重要，因为我们没有可广泛依赖的 GC 做内存管理。而这正是重点：Rust 关乎控制。不过我们并不限于内存。几乎任何其他系统资源，如线程、文件或 socket，都通过此类 API 暴露。
