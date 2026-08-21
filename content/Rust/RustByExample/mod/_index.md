+++
title = "第10章 模块"
date = 2026-08-20T21:20:00+08:00
weight = 68
type = "docs"
description = "模块 — Rust By Example"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Rust By Example](https://doc.rust-lang.org/stable/rust-by-example/)

> 原文链接: [https://doc.rust-lang.org/stable/rust-by-example/mod.html](https://doc.rust-lang.org/stable/rust-by-example/mod.html)

# 模块

Rust 提供了一套强大的模块（module）系统，可以将代码按层次分成多个逻辑单元（模块），并管理这些模块之间的可见性（公有（public）或私有（private））。

模块是项（item）的集合，项可以是：函数，结构体，trait，`impl` 块，甚至其它模块。
