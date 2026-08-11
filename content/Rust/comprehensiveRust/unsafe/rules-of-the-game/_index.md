+++
title = "5 游戏规则"
date = 2026-08-11T11:30:00+08:00
weight = 525
type = "docs"
description = "游戏规则 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/unsafe-deep-dive/rules-of-the-game.html](https://google.github.io/comprehensive-rust/unsafe-deep-dive/rules-of-the-game.html)

# 5 游戏规则

> 「我们在课程里见过很多有问题的代码示例，但一直缺少统一的术语。
>
> 「下一节的目标是引入一些术语，用来描述我们一直在思考的那些概念。
>
> - 未定义行为（undefined behavior）
> - 健全（sound）
> - 不健全（unsound）
>
> 「鉴于许多安全前置条件是语义层面的而非语法层面的，使用共享词汇非常重要。这样我们才能就语义达成一致。
>
> 「总体目标是建立关于健全性（soundness）的心智模型，并确保包含 `unsafe` 的 Rust 代码保持健全。」

