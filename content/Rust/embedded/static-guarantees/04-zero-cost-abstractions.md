+++
title = "04-零成本抽象"
date = 2026-08-01T10:38:00+08:00
weight = 72
type = "docs"
description = "零成本抽象（Zero Cost Abstractions）"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Embedded Rust Book](https://doc.rust-lang.org/stable/embedded-book/)

# 零成本抽象 {#zero-cost-abstractions}


> 原文链接: [https://doc.rust-lang.org/stable/embedded-book/static-guarantees/zero-cost-abstractions.html](https://doc.rust-lang.org/stable/embedded-book/static-guarantees/zero-cost-abstractions.html)


类型状态也是零成本抽象（Zero Cost Abstractions）的绝佳例子 —— 即把某些行为移到编译期执行或分析的能力。这些类型状态不包含实际数据，而是用作标记。由于它们不含数据，在运行时内存中没有实际表示：

```rust,ignore
use core::mem::size_of;

let _ = size_of::<Enabled>();    // == 0
let _ = size_of::<Input>();      // == 0
let _ = size_of::<PulledHigh>(); // == 0
let _ = size_of::<GpioConfig<Enabled, Input, PulledHigh>>(); // == 0
```

## 零大小类型 {#zero-sized-types}

```rust,ignore
struct Enabled;
```

像这样定义的结构体称为零大小类型（Zero Sized Types），因为它们不包含实际数据。虽然这些类型在编译期表现得像「真实」的 —— 你可以复制它们、移动它们、取引用等等 —— 但优化器会把它们完全剥离掉。

在这段代码中：

```rust,ignore
pub fn into_input_high_z(self) -> GpioConfig<Enabled, Input, HighZ> {
    self.periph.modify(|_r, w| w.input_mode().high_z());
    GpioConfig {
        periph: self.periph,
        enabled: Enabled,
        direction: Input,
        mode: HighZ,
    }
}
```

我们返回的 `GpioConfig` 在运行时从不存在。调用这个函数通常会归结为一条汇编指令 —— 把一个常量寄存器值存到一个寄存器位置。这意味着我们开发的类型状态接口是零成本抽象 —— 它不花费更多 CPU、RAM 或代码空间来跟踪 `GpioConfig` 的状态，并编译成与直接寄存器访问相同的机器码。

## 嵌套 {#nesting}

一般而言，这些抽象可以按你希望的深度嵌套。只要所用组件都是零大小类型，整个结构在运行时就不会存在。

对于复杂或深度嵌套的结构，定义所有可能的状态组合可能很繁琐。在这些情况下，可以用宏来生成所有实现。
