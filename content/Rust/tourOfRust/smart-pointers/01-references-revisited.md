+++
title = "01-重温引用"
date = 2026-08-17T22:00:00+08:00
weight = 92
type = "docs"
description = "重温引用 — Rust 语言之旅"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Tour of Rust / Rust 语言之旅](https://github.com/richardanaya/tour_of_rust)

> 原文链接: [https://tourofrust.com/90_zh-cn.html](https://tourofrust.com/90_zh-cn.html)

# 重温引用

引用本质上只是表示内存中某些字节起始位置的数字。 它唯一的目的就是表示特定类型的数据存在于何处。 引用与数字的不同之处在于，Rust 将验证引用自身的生命周期不会超过它指向的内容（否则我们在使用它时会出错！）。
