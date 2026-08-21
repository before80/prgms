+++
title = "第7章 指导原则与理据"
date = 2026-08-18T22:00:00+08:00
weight = 80
type = "docs"
description = "指导原则与理据 — The Rust Style Guide"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Style Guide](https://doc.rust-lang.org/nightly/style-guide/)

> 原文链接: [https://doc.rust-lang.org/nightly/style-guide/principles.html](https://doc.rust-lang.org/nightly/style-guide/principles.html)

# 指导原则与理据

在确定风格指南时，风格团队遵循以下指导原则（大致按优先级排序）：

- 可读性
  - 可扫读性
  - 避免误导性格式
  - 无障碍性——让使用尽可能多种硬件的用户都能阅读和编辑，包括非视觉无障碍界面
  - 在没有语法高亮或 IDE 辅助的场景中仍可读，例如 rustc 错误信息、diff、grep 以及其他纯文本场景

- 美观
  - 「美」的感觉
  - 与其他语言/工具一致

- 具体考量
  - 与版本控制实践兼容——保留 diff、便于合并等
  - 防止向右漂移
  - 尽量减少纵向空间

- 可应用性
  - 便于手工应用
  - 便于实现（在 `rustfmt` 以及其他工具/编辑器/代码生成器中）
  - 内部一致性
  - 格式规则简明
