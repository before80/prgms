+++
title = "07-中断"
date = 2026-08-01T10:38:00+08:00
weight = 45
type = "docs"
description = "中断（Interrupts）"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Embedded Rust Book](https://doc.rust-lang.org/stable/embedded-book/)

# 中断 {#interrupts}


> 原文链接: [https://doc.rust-lang.org/stable/embedded-book/start/interrupts.html](https://doc.rust-lang.org/stable/embedded-book/start/interrupts.html)


中断与异常在多个方面不同，但它们的操作与使用大体相似，并且也由同一中断控制器处理。异常由 Cortex-M 架构定义，而中断始终是厂商（往往甚至是芯片）特定的实现，无论是命名还是功能。

中断允许很大的灵活性，在尝试以高级方式使用它们时需要加以考虑。本书不会涵盖那些用法，但记住以下几点是个好主意：

* 中断有可编程优先级，决定其处理函数的执行顺序
* 中断可以嵌套与抢占，即一个中断处理函数的执行可能被另一个更高优先级的中断打断
* 一般而言，需要清除导致中断触发的原因，以防止无限地反复进入中断处理函数

运行时的一般初始化步骤始终相同：
* 设置外设，使其在期望的时机生成中断请求
* 在中断控制器中设置中断处理函数的期望优先级
* 在中断控制器中启用中断处理函数

与异常类似，cortex-m-rt crate 暴露 [`interrupt`] 属性用于声明中断处理函数。不过，该属性仅在启用 device 特性时可用。也就是说，该属性不打算直接使用——直接使用会导致编译错误。

相反，你应使用设备 crate（通常用 svd2rust 生成）重新导出的 interrupt 属性版本。这确保编译器能验证该中断确实存在于目标设备上。可用中断列表——以及它们在中断向量表中的位置——通常由 svd2rust 从 SVD 文件自动生成。

[`interrupt`]: https://docs.rs/cortex-m-rt-macros/0.1.5/cortex_m_rt_macros/attr.interrupt.html

``` rust,ignore
use lm3s6965::interrupt; // 设备 crate 重新导出的属性

// Timer2 中断的中断处理函数
#[interrupt]
fn TIMER2A() {
    // ..
    // 清除生成中断请求的原因
}
```

中断处理函数看起来像普通函数（除了缺少参数），与异常处理函数类似。但由于特殊的调用约定，它们不能被固件的其它部分直接调用。不过，可以在软件中生成中断请求，以触发转入中断处理函数。

与异常处理函数类似，也可以在中断处理函数内部声明 `static mut` 变量，以*安全*地保持状态。

``` rust,ignore
#[interrupt]
fn TIMER2A() {
    static mut COUNT: u32 = 0;

    // `COUNT` 的类型是 `&mut u32`，可以安全使用
    *COUNT += 1;
}
```

关于此处演示机制的更详细描述，请参阅[异常]一节。

[异常]: 06-exceptions/
