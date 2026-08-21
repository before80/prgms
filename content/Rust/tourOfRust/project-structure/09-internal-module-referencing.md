+++
title = "09-模块内部引用"
date = 2026-08-17T22:00:00+08:00
weight = 116
type = "docs"
description = "模块内部引用 — Rust 语言之旅"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Tour of Rust / Rust 语言之旅](https://github.com/richardanaya/tour_of_rust)

> 原文链接: [https://tourofrust.com/114_zh-cn.html](https://tourofrust.com/114_zh-cn.html)

# 模块内部引用

你可以在你的 `use` 路径中使用如下 Rust 关键字来获得你想要的模块：
* `crate` - 你的 crate 的根模块
* `super` - 当前模块的父模块
* `self` - 当前模块
