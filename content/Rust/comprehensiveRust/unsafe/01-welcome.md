+++
title = "1 欢迎"
date = 2026-08-11T11:30:00+08:00
weight = 498
type = "docs"
description = "01-欢迎 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/unsafe-deep-dive/welcome.html](https://google.github.io/comprehensive-rust/unsafe-deep-dive/welcome.html)

> 重要提示：本模块仍处于早期开发阶段
>
> 请勿将 Comprehensive Rust 的这一模块视为已完成。在此前提下，我们非常欢迎你的反馈、评论，尤其是你的顾虑。
>
> 若要就本模块的开发发表评论，请使用 [GitHub issue tracker]。

[GitHub issue tracker]: https://github.com/google/comprehensive-rust/issues

# 1 欢迎

本深度专题旨在让你能够高效地使用 Unsafe Rust。

我们将从三个方面入手：

- 建立 Unsafe Rust 的心智模型
- 练习阅读与编写 Unsafe Rust
- 练习对 Unsafe Rust 进行代码审查

> 本课程的目标是教你足够的 Unsafe Rust 知识，使你能够自行审查简单案例，并识别需要更有经验的 Unsafe Rust 工程师审查的困难案例。
>
> - 建立 Unsafe Rust 的心智模型
>   - `unsafe` 关键字的含义
>   - 讨论安全性的共同词汇
>   - 内存如何工作的心智模型
>   - 常见模式
>   - 对使用 `unsafe` 的代码的期望
>
> - 练习使用 unsafe
>   - 阅读与编写代码及文档
>   - 使用 unsafe API
>   - 设计与实现 unsafe API
>
> - 代码审查
>   - 有信心自行审查简单案例
>   - 具备识别困难案例的知识
>
> 「我们将采用螺旋式教学法。这意味着我们会多次回到同一主题，并逐层加深。」
>
> 如果学员彼此不太熟悉，进行一轮自我介绍会很有帮助。请每个人做自我介绍，并记下对本课程的具体目标。
>
> - 你是谁？
> - 你在做什么项目？
> - 你对本课程有什么目标？

