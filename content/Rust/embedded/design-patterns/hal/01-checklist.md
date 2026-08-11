+++
title = "01-检查清单"
date = 2026-08-01T10:38:00+08:00
weight = 123
type = "docs"
description = "检查清单（Checklist）"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Embedded Rust Book](https://doc.rust-lang.org/stable/embedded-book/)

# HAL 设计模式检查清单 {#hal-design-patterns-checklist}


> 原文链接: [https://doc.rust-lang.org/stable/embedded-book/design-patterns/hal/checklist.html](https://doc.rust-lang.org/stable/embedded-book/design-patterns/hal/checklist.html)


- **命名** *(crate 符合 Rust 命名约定)*
  - [ ] crate 命名恰当（[C-CRATE-NAME]）
- **互操作性** *(crate 能与其它库功能良好协作)*
  - [ ] 包装类型提供析构方法（[C-FREE]）
  - [ ] HAL 再导出其寄存器访问 crate（[C-REEXPORT-PAC]）
  - [ ] 类型实现 `embedded-hal` trait（[C-HAL-TRAITS]）
- **可预测性** *(crate 能写出易读且行为与外观一致的代码)*
  - [ ] 使用构造函数而非扩展 trait（[C-CTOR]）
- **GPIO 接口** *(GPIO 接口遵循统一模式)*
  - [ ] 引脚类型默认为零大小类型（[C-ZST-PIN]）
  - [ ] 引脚类型提供擦除引脚与端口的方法（[C-ERASED-PIN]）
  - [ ] 引脚状态应编码为类型参数（[C-PIN-STATE]）

[C-CRATE-NAME]: 02-naming/#c-crate-name

[C-FREE]: 03-interoperability/#c-free
[C-REEXPORT-PAC]: 03-interoperability/#c-reexport-pac
[C-HAL-TRAITS]: 03-interoperability/#c-hal-traits

[C-CTOR]: 04-predictability/#c-ctor

[C-ZST-PIN]: 05-gpio/#c-zst-pin
[C-ERASED-PIN]: 05-gpio/#c-erased-pin
[C-PIN-STATE]: 05-gpio/#c-pin-state
