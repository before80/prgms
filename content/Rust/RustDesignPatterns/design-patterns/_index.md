+++
title = "第2章 设计模式"
date = 2026-08-18T22:10:00+08:00
weight = 23
type = "docs"
description = "设计模式 — Rust Design Patterns"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Rust Design Patterns](https://rust-unofficial.github.io/patterns/)

> 原文链接: [https://rust-unofficial.github.io/patterns/patterns/index.html](https://rust-unofficial.github.io/patterns/patterns/index.html)

# 设计模式

[设计模式](https://en.wikipedia.org/wiki/Software_design_pattern) 是「软件设计中，针对特定情境下反复出现的问题的通用可复用解决方案」。设计模式是描述一门编程语言文化的极佳方式。设计模式高度依赖于语言——某种模式在一门语言中可能必不可少，在另一门语言中却可能因语言特性而变得多余，或因缺少某种特性而无法表达。

若滥用，设计模式会给程序增加不必要的复杂度。但它们仍是分享一门语言中级与高级知识的好方法。

## Rust 中的设计模式 {#design-patterns-in-rust}

Rust 有许多独特的特性。这些特性通过消除整类问题给我们带来巨大收益。其中一些也是 Rust *独有* 的模式。

## YAGNI {#yagni}

YAGNI 是 `You Aren't Going to Need It`（你不会需要它）的缩写。这是编写代码时应当遵循的重要软件设计原则。

> 我写过最好的代码，是那些我从未写过的代码。

若把 YAGNI 应用到设计模式上，会发现 Rust 的特性让我们可以抛弃许多模式。例如，Rust 中并不需要[策略模式](https://en.wikipedia.org/wiki/Strategy_pattern)，因为直接使用 [trait](https://doc.rust-lang.org/book/traits.html) 即可。
