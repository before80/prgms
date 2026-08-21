+++
title = "06-创建模块"
date = 2026-08-17T22:00:00+08:00
weight = 113
type = "docs"
description = "创建模块 — Rust 语言之旅"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Tour of Rust / Rust 语言之旅](https://github.com/richardanaya/tour_of_rust)

> 原文链接: [https://tourofrust.com/111_zh-cn.html](https://tourofrust.com/111_zh-cn.html)

# 创建模块

当我们想到项目时，我们通常会想象一个以目录组织的文件层次结构。Rust 允许您创建与您的文件结构密切相关的模块。

在 Rust 中，有两种方式来声明一个模块。例如，模块 `foo` 可以表示为： 

  * 一个名为 `foo.rs` 的文件。
  * 在名为 `foo` 的目录，里面有一个叫 `mod.rs` 文件。
