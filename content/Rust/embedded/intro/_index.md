+++
title = "01-引言"
date = 2026-08-01T10:38:00+08:00
weight = 11
type = "docs"
description = "引言（Introduction）"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Embedded Rust Book](https://doc.rust-lang.org/stable/embedded-book/)

# 引言 {#introduction}


> 原文链接: [https://doc.rust-lang.org/stable/embedded-book/intro/](https://doc.rust-lang.org/stable/embedded-book/intro/)


欢迎阅读《嵌入式 Rust 手册》：一本关于在“裸机（bare metal）”嵌入式系统（例如微控制器）上使用 Rust 编程语言的入门书。

## 嵌入式 Rust 面向谁 {#who-embedded-rust-is-for}

嵌入式 Rust 面向所有希望在做嵌入式编程的同时，利用 Rust 语言提供的更高层抽象与安全保证的人。
（另见 [Rust 面向谁](https://doc.rust-lang.org/book/ch00-00-introduction.html)）

## 范围 {#scope}

本书的目标是：

* 帮助开发者快速上手嵌入式 Rust 开发，例如如何搭建开发环境。

* 分享当前使用 Rust 做嵌入式开发的最佳实践，例如如何更好地运用 Rust 语言特性写出更正确的嵌入式软件。

* 在某些场景下充当“菜谱（cookbook）”，例如如何在同一项目中混用 C 与 Rust？

本书尽量保持通用，但为了降低读者与作者双方的难度，所有示例都使用 ARM Cortex-M 架构。不过本书并不假设读者熟悉该架构，并会在必要时解释该架构特有的细节。

## 本书面向谁 {#who-this-book-is-for}

本书面向有一定嵌入式背景或一定 Rust 背景的读者；不过我们也相信，任何对嵌入式 Rust 编程感到好奇的人都能从中有所收获。对于没有任何先验知识的读者，建议先阅读“假设与前置知识”一节，补齐缺失知识，以便更好地理解本书、改善阅读体验。你可以查看“其它资源”一节，找到可能需要补习的主题相关资料。

### 假设与前置知识 {#assumptions-and-prerequisites}

* 你已能自如使用 Rust 编程语言，并在桌面环境中编写、运行与调试过 Rust 应用程序。你还应熟悉 [2018 edition] 的惯用法，因为本书面向 Rust 2018。

[2018 edition]: https://doc.rust-lang.org/edition-guide/

* 你已能用其它语言（如 C、C++ 或 Ada）开发并调试嵌入式系统，并熟悉如下概念：
    * 交叉编译（Cross Compilation）
    * 内存映射外设（Memory Mapped Peripherals）
    * 中断（Interrupts）
    * 常见接口，如 I2C、SPI、串口等

### 其它资源 {#other-resources}

如果你对上文提到的任何内容不熟悉，或想进一步了解本书中的某一主题，下面这些资源可能会有帮助。

| 主题 | 资源 | 说明 |
|------|------|------|
| Rust | [《Rust 程序设计语言》](https://doc.rust-lang.org/book/) | 若你还不熟悉 Rust，强烈建议先阅读这本书。 |
| Rust，嵌入式 | [《探索之书》（Discovery Book）](https://docs.rust-embedded.org/discovery/) | 若你从未做过嵌入式编程，这本书可能是更好的起点 |
| Rust，嵌入式 | [嵌入式 Rust 书架](https://docs.rust-embedded.org) | 这里可以找到 Rust 嵌入式工作组提供的其它多种资源。 |
| Rust，嵌入式 | [Embedonomicon](https://docs.rust-embedded.org/embedonomicon/) | 用 Rust 做嵌入式编程时的硬核细节。 |
| Rust，嵌入式 | [嵌入式 FAQ](https://docs.rust-embedded.org/faq.html) | 嵌入式语境下关于 Rust 的常见问题。 |
| Rust，嵌入式 | [Comprehensive Rust 🦀：裸机](https://google.github.io/comprehensive-rust/bare-metal.html) | 为期 4 天的裸机 Rust 开发教学材料 |
| 中断 | [中断（Interrupt）](https://en.wikipedia.org/wiki/Interrupt) | - |
| 内存映射 I/O / 外设 | [内存映射 I/O](https://en.wikipedia.org/wiki/Memory-mapped_I/O) | - |
| SPI、UART、RS232、USB、I2C、TTL | [Stack Exchange：关于 SPI、UART 及其它接口](https://electronics.stackexchange.com/questions/37814/usart-uart-rs232-usb-spi-i2c-ttl-etc-what-are-all-of-these-and-how-do-th) | - |

### 译本 {#translations}

本书已有志愿者完成的译本。若希望你的译本列在此处，请提交 PR 添加。

* [Japanese](https://tomoyuki-nakabayashi.github.io/book/)
  （[仓库](https://github.com/tomoyuki-nakabayashi/book)）

* [Chinese](https://xxchang.github.io/book/)
  （[仓库](https://github.com/XxChang/book)）

## 如何使用本书 {#how-to-use-this-book}

本书一般假设你从前到后阅读。后面章节会建立在前面章节的概念之上；前面章节对某主题可能不会深入，而在后续章节再回访。

本书大部分示例会使用 STMicroelectronics 的 [STM32F3DISCOVERY] 开发板。该板基于 ARM Cortex-M 架构；尽管基于该架构的多数 CPU 基本功能相同，但外设以及其它微控制器实现细节在不同厂商之间不同，甚至同一厂商的不同微控制器系列之间也常有差异。

因此，建议购买 [STM32F3DISCOVERY] 开发板，以便跟随本书示例。

[STM32F3DISCOVERY]: http://www.st.com/en/evaluation-tools/stm32f3discovery.html

## 为本书做贡献 {#contributing-to-this-book}

本书的工作在[此仓库]协调，主要由 [资源团队] 开发。

[此仓库]: https://github.com/rust-embedded/book
[资源团队]: https://github.com/rust-embedded/wg#the-resources-team

若你在跟随本书说明时遇到困难，或发现某节不够清晰、难以跟上，那就是一个 bug，应在本书的[问题跟踪器]中报告。

[问题跟踪器]: https://github.com/rust-embedded/book/issues/

欢迎提交修复拼写错误与新增内容的 Pull Request！

## 材料的再利用 {#re-using-this-material}

本书按以下许可分发：

* 本书中的代码示例与独立 Cargo 项目同时按 [MIT License] 与 [Apache License v2.0] 许可。
* 本书中的文字、图片与图表按 Creative Commons [CC-BY-SA v4.0] 许可。

[MIT License]: https://opensource.org/licenses/MIT
[Apache License v2.0]: http://www.apache.org/licenses/LICENSE-2.0
[CC-BY-SA v4.0]: https://creativecommons.org/licenses/by-sa/4.0/legalcode

简而言之：若想在你的作品中使用我们的文字或图片，你需要：

* 给出适当署名（例如在幻灯片上提及本书，并提供相关页面链接）
* 提供指向 [CC-BY-SA v4.0] 许可的链接
* 说明你是否对材料做过任何修改，并以相同许可提供对我们材料的任何修改

另外，若你觉得本书有用，也请告诉我们！

## 本章其它页面 {#other-pages-in-this-chapter}

- [硬件](01-hardware/)
- [no_std](02-no-std/)
- [工具链](03-tooling/)
- [安装](install/)
