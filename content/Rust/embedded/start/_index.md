+++
title = "02-入门指南"
date = 2026-08-01T10:38:00+08:00
weight = 38
type = "docs"
description = "入门指南（Getting started）"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Embedded Rust Book](https://doc.rust-lang.org/stable/embedded-book/)

# 入门指南 {#getting-started}


> 原文链接: [https://doc.rust-lang.org/stable/embedded-book/start/](https://doc.rust-lang.org/stable/embedded-book/start/)


在本节中，我们将带你走完编写、构建、烧录与调试嵌入式程序的过程。由于我们会用流行的开源硬件模拟器 QEMU 展示基础内容，你大多可以在没有特殊硬件的情况下尝试这些示例。自然，唯一需要硬件的是[硬件](02-hardware/)一节，我们会在那里用 OpenOCD 对 [STM32F3DISCOVERY] 进行编程。

[STM32F3DISCOVERY]: http://www.st.com/en/evaluation-tools/stm32f3discovery.html

## 本章其它页面 {#other-pages-in-this-chapter}

- [QEMU](01-qemu/)
- [硬件](02-hardware/)
- [内存映射寄存器](03-memory-mapped-registers/)
- [半主机（Semihosting）](04-semihosting/)
- [Panic 处理](05-panicking/)
- [异常](06-exceptions/)
- [中断](07-interrupts/)
