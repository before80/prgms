+++
title = "3.7 需要更严格的开发流程"
date = 2026-08-11T11:30:00+08:00
weight = 514
type = "docs"
description = "05-需要更严格的开发流程 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/unsafe-deep-dive/introduction/impact-on-workflow.html](https://google.github.io/comprehensive-rust/unsafe-deep-dive/introduction/impact-on-workflow.html)

# 3.7 需要更严格的开发流程

编写代码时

- 确认你理解任何 `unsafe` 函数/trait 的前置条件
- 检查前置条件是否已满足
- 在 safety comment（安全注释）中记录你的推理

加强代码审查

- 自审 → 同行审查者 → unsafe Rust 专家（必要时）
- 升级给熟悉你的代码与推理的人

> 「`unsafe` 关键字给程序员带来更多责任，因此需要更严格的开发流程。」
>
> 「本课程假设一种特定的软件开发流程：代码审查是强制性的，作者与主要审查者可以接触到 unsafe Rust 专家。」
>
> 「作者与主要审查者会自行验证简单的 unsafe Rust 代码，必要时再交给 unsafe 专家。」
>
> 「unsafe Rust 专家人数不多，且非常忙碌，因此我们需要最优地利用他们的时间。」

