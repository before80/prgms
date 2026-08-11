+++
title = "嵌入式 Rust 手册"
date = 2026-08-01T10:38:00+08:00
weight = 1
type = "docs"
description = "在裸机嵌入式系统上使用 Rust 的入门手册"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Embedded Rust Book](https://doc.rust-lang.org/stable/embedded-book/)

# 嵌入式 Rust 手册 {#the-embedded-rust-book}


> 原文链接: [https://doc.rust-lang.org/stable/embedded-book/](https://doc.rust-lang.org/stable/embedded-book/)


欢迎阅读 **嵌入式 Rust 手册**：一本关于在“裸机（bare metal）”嵌入式系统（例如微控制器）上使用 Rust 的入门书。

## 章节 {#sections}

**[引言](intro/)**

嵌入式 Rust 面向谁、本书范围、安装前的准备与工具链。

**[入门指南](start/)**

从 QEMU 与真实硬件开始，到寄存器、半主机、panic、异常与中断。

**[外设](peripherals/)**

用 Rust 安全地表示与使用外设。

**[静态保证](static-guarantees/)**

类型状态、状态机与零成本抽象。

**[可移植性](portability/)** · **[并发](concurrency/)** · **[集合](collections/)**

跨芯片复用、并发模型与在 `no_std` 下使用集合。

**[设计模式](design-patterns/)**

HAL 设计约定与检查清单。

**[给嵌入式 C 开发者的提示](c-tips/)**

从 C 迁移到嵌入式 Rust 的对照说明。

**[互操作性](interoperability/)**

Rust 与 C 互相调用。

**[未分类主题](unsorted/)**

优化权衡与数学功能等。

**[附录 A：术语表](appendix/01-glossary/)**

常用术语释义。
