+++
title = "03-解引用"
date = 2026-08-17T22:00:00+08:00
weight = 94
type = "docs"
description = "解引用 — Rust 语言之旅"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Tour of Rust / Rust 语言之旅](https://github.com/richardanaya/tour_of_rust)

> 原文链接: [https://tourofrust.com/92_zh-cn.html](https://tourofrust.com/92_zh-cn.html)

# 解引用

访问或操作 由*引用*（例如`&i32`）指向的数据的过程称为*解除引用*。             
有两种方式通过引用来访问或操作数据： 
 * 在变量赋值期间访问引用的数据。
 * 访问引用数据的字段或方法。

Rust 有一些强大的运算符可以让我们做到这一点。
