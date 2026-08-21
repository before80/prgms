+++
title = "第1章 惯用法"
date = 2026-08-18T22:10:00+08:00
weight = 4
type = "docs"
description = "惯用法 — Rust Design Patterns"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Rust Design Patterns](https://rust-unofficial.github.io/patterns/)

> 原文链接: [https://rust-unofficial.github.io/patterns/idioms/index.html](https://rust-unofficial.github.io/patterns/idioms/index.html)

# 惯用法

[惯用法](https://en.wikipedia.org/wiki/Programming_idiom)是社区大体认同的常用风格、指南和模式。
编写符合惯用法的代码能让其他开发者更好地理解正在发生的事情。

毕竟，计算机只关心编译器生成的机器码。源代码主要是对开发者有益。
那么，既然已经有了这层抽象，为什么不让它更易读呢？

请记住 [KISS 原则](https://en.wikipedia.org/wiki/KISS_principle)：
「保持简单，傻瓜」（Keep It Simple, Stupid）。它主张「大多数系统在保持简单而非变得复杂时工作得最好；
因此，简单应成为设计的关键目标，应避免不必要的复杂性」。

> 代码是写给人看的，而不是写给计算机看的。
