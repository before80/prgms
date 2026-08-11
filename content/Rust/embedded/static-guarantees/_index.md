+++
title = "04-静态保证"
date = 2026-08-01T10:38:00+08:00
weight = 68
type = "docs"
description = "静态保证（Static Guarantees）"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Embedded Rust Book](https://doc.rust-lang.org/stable/embedded-book/)

# 静态保证 {#static-guarantees}


> 原文链接: [https://doc.rust-lang.org/stable/embedded-book/static-guarantees/](https://doc.rust-lang.org/stable/embedded-book/static-guarantees/)


Rust 的类型系统在编译期防止数据竞争（参见 [`Send`] 与 [`Sync`] trait）。类型系统也可以用来在编译期检查其他属性；从而在某些情况下减少运行时检查的需求。

[`Send`]: https://doc.rust-lang.org/core/marker/trait.Send.html
[`Sync`]: https://doc.rust-lang.org/core/marker/trait.Sync.html

将这些*静态检查*应用到嵌入式程序时，例如可以强制要求 I/O 接口的配置正确完成。比方说，可以设计这样一种 API：只有先配置好串口将使用的引脚，才能初始化串口接口。

也可以静态检查某些操作（例如把引脚拉低）只能在正确配置的外设上执行。例如，试图改变配置为浮空输入模式的引脚的输出状态，会引发编译错误。

并且，如[上一章](../peripherals/)所见，所有权概念可以应用到外设上，以确保只有程序的某些部分能修改外设。这种*访问控制*相比把外设当作全局可变状态来处理，让软件更易于推理。

## 本章其它页面 {#related-pages}

- [01-类型状态编程](01-typestate-programming/)
- [02-作为状态机的外设](02-peripherals-as-state-machines/)
- [03-设计契约](03-design-contracts/)
- [04-零成本抽象](04-zero-cost-abstractions/)
