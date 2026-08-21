+++
title = "关于"
date = 2026-08-18T18:10:00+08:00
weight = 10
type = "docs"
description = "关于 — Pragmatic Rust Guidelines"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Pragmatic Rust Guidelines](https://microsoft.github.io/rust-guidelines/)

> 原文链接: [https://microsoft.github.io/rust-guidelines/guidelines/index.html](https://microsoft.github.io/rust-guidelines/guidelines/index.html)

# 关于

一套务实的设计指南，帮助应用与库开发者写出可扩展的惯用 Rust。

版本：2026.6

## 元设计原则

我们建立在既有的高质量指南之上，尤其是 [Rust API Guidelines](https://rust-lang.github.io/api-guidelines/checklist.html)，
并针对 Rust 开发者常遇到的主题。一条指南要进入本书，应满足以下条件：

- [ ] 它对 { 安全、COGS（成本）、可维护性 } 有正面影响；即在适用时必须
  - [ ] 促进 **安全最佳实践** 并防范风险来源
  - [ ] 带来 **高吞吐**、**低延迟** 与 **低内存占用**
  - [ ] 使代码 **可读、可理解**
- [ ] 多数有经验（3 年以上）的 **Rust 开发者会认同该指南**。
- [ ] 该指南对 Rust 新手（4 周以上）**合理可理解**。
- [ ] 它是 **务实的**，因为不切实际的指南不会被遵循。

## 适用范围

标为 _必须_ 的条目理应始终成立，标为 _应当_ 的条目则留有更大余地。

话虽如此，各团队可按自身情况采纳这些指南；偶尔你也有充分理由采取不同做法。

我们建议你尽量将所有条目应用到项目中。若某条不适用，请与我们联系。要么该条目有问题需要更新，要么它确实不适用（我们仍可能更新它以指出这些边界情况）。

> ### 💡  黄金法则
>
> 这里的每一条都有其存在理由；重要的是精神，而非字面。
>
> 在试图绕过某条指南之前，你应当理解它为何存在、试图守护什么。
> 同样，若明显遵循某条指南会违背其初衷，也不应盲目照做！

## 提交新指南

你是否有一条能提升安全性、COGS（成本）或可维护性的实用指南？我们很乐意听取！
请按以下流程：

- 检查你的指南是否符合上文的 [元设计原则](#meta-design-principles)。
- 检查你的建议是否已被 [API Guidelines](https://rust-lang.github.io/api-guidelines/checklist.html) 或 [Clippy](https://rust-lang.github.io/rust-clippy/master/?groups) 覆盖。
- 提交 [PR 或 issue](https://github.com/microsoft/rust-guidelines)。

本书最近生成于：构建时生成
