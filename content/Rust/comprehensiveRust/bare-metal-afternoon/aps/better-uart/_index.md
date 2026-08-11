+++
title = "1.5 更好的 UART 驱动程序"
date = 2026-08-11T11:30:00+08:00
weight = 319
type = "docs"
description = "更好的 UART 驱动程序 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/bare-metal/aps/better-uart.html](https://google.github.io/comprehensive-rust/bare-metal/aps/better-uart.html)

# 1.5 更好的 UART 驱动程序

PL011实际上有[更多寄存器][1]，并添加偏移量来构造
访问它们的指针容易出错且难以阅读。此外，一些
它们是位字段，可以很好地以结构化方式访问。

|偏移|注册名称 |宽度|
| ------ | ------------- | -----|
| 0x00 | 0x00博士| 12 | 12
| 0x04 | 0x04 RSR | 4 |
| 0x18 | 0x18法国 | 9 |
| 0x20 | 0x20 ILPR | 8 |
| 0x24 | 0x24国际复兴开发银行 | 16 | 16
| 0x28 | 0x28 FBRD | 6 |
| 0x2c | 0x2c LCR_H | 8 |
| 0x30 | 0x30 CR | 16 | 16
| 0x34 | 0x34国际生命安全研究所 | 6 |
| 0x38 | 0x38 IMSC | 11 | 11
| 0x3c | 0x3c RIS | 11 | 11
| 0x40 | 0x40管理信息系统 | 11 | 11
| 0x44 | 0x44 ICR | 11 | 11
| 0x48 | 0x48 DMACR | 3 |

> - 为了简洁起见，还省略了一些 ID 寄存器。


[1]: https://developer.arm.com/documentation/ddi0183/g/programmers-model/summary-of-registers
