+++
title = "引言"
date = 2026-08-18T22:10:00+08:00
weight = 2
type = "docs"
description = "引言 — Rust Design Patterns"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Rust Design Patterns](https://rust-unofficial.github.io/patterns/)

> 原文链接: [https://rust-unofficial.github.io/patterns/intro.html](https://rust-unofficial.github.io/patterns/intro.html)

# 引言

## 参与 {#participation}

如果你有兴趣为本书做出贡献，请参阅
[贡献指南](https://github.com/rust-unofficial/patterns/blob/master/CONTRIBUTING.md)。

## 动态 {#news}

- **2025-12-14**：新增模式：
  [使用自定义 trait 避免复杂的类型约束](../design-patterns/03-structural/04-avoid-complex-type-bounds-with-custom-traits/)
- **2024-03-17**：现在可以下载
  [PDF 格式的本书](https://rust-unofficial.github.io/patterns/rust-design-patterns.pdf)。

## 设计模式 {#design-patterns}

在软件开发中，我们经常会遇到一些无论出现在何种环境中都具有相似性的问题。
尽管实现细节对于解决眼前的任务至关重要，但我们可以从这些特殊性中抽象出来，
找出普遍适用的常见实践。

设计模式是一组经过测试、可复用的工程问题解决方案，用于应对反复出现的问题。
它们使我们的软件更加模块化、可维护和可扩展。此外，这些模式为开发者提供了
一种共同语言，是团队解决问题时进行有效沟通的绝佳工具。

请记住：每种模式都有其自身的权衡取舍。关键在于关注你为什么选择某种模式，
而不仅仅是如何实现它。[^1]

## Rust 中的设计模式 {#design-patterns-in-rust}

Rust 并非面向对象语言，其功能式元素、强类型系统和借用检查器等全部特性
组合在一起，使它独树一帜。因此，Rust 的设计模式与其他传统面向对象编程语言
有所不同。这正是我们决定撰写本书的原因。希望你阅读愉快！本书分为三个主要章节：

- [惯用法](../idioms/)：编码时应遵循的指南。它们是社区的社交规范。
  只有当你有充分理由时，才应打破它们。
- [设计模式](../design-patterns/)：编码时解决常见问题的方法。
- [反模式](../anti-patterns/)：同样是编码时解决常见问题的方法。
  然而，设计模式会带来收益，反模式却会制造更多问题。

[^1]: <https://www.infoq.com/podcasts/software-architecture-hard-parts/>
    ([存档](https://web.archive.org/web/20240124025806/https://www.infoq.com/podcasts/software-architecture-hard-parts/))
