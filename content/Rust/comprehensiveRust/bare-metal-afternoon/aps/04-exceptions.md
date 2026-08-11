+++
title = "1.8 例外情况"
date = 2026-08-11T11:30:00+08:00
weight = 328
type = "docs"
description = "04-例外情况 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/bare-metal/aps/exceptions.html](https://google.github.io/comprehensive-rust/bare-metal/aps/exceptions.html)

# 1.8 例外情况

AArch64定义了一个异常向量表，有16个条目，分别对应4种类型
4 种状态的异常（同步、IRQ、FIQ、SError）（当前 EL 带有 SP0、
当前 EL 使用 SPx，较低 EL 使用 AArch64，较低 EL 使用 AArch32）。我们
在汇编中实现此功能以将易失性寄存器保存到堆栈中
调用 Rust 代码：

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
use log::error;
use smccc::Hvc;
use smccc::psci::system_off;

// 安全：没有此名称的其他全局函数。
#[unsafe(no_mangle)]
extern "C" fn sync_current(_elr: u64, _spsr: u64) {
    error!("sync_current");
    system_off::<Hvc>().unwrap();
}

// 安全：没有此名称的其他全局函数。
#[unsafe(no_mangle)]
extern "C" fn irq_current(_elr: u64, _spsr: u64) {
    error!("irq_current");
    system_off::<Hvc>().unwrap();
}

// 安全：没有此名称的其他全局函数。
#[unsafe(no_mangle)]
extern "C" fn fiq_current(_elr: u64, _spsr: u64) {
    error!("fiq_current");
    system_off::<Hvc>().unwrap();
}

// 安全：没有此名称的其他全局函数。
#[unsafe(no_mangle)]
extern "C" fn serror_current(_elr: u64, _spsr: u64) {
    error!("serror_current");
    system_off::<Hvc>().unwrap();
}

// 安全：没有此名称的其他全局函数。
#[unsafe(no_mangle)]
extern "C" fn sync_lower(_elr: u64, _spsr: u64) {
    error!("sync_lower");
    system_off::<Hvc>().unwrap();
}

// 安全：没有此名称的其他全局函数。
#[unsafe(no_mangle)]
extern "C" fn irq_lower(_elr: u64, _spsr: u64) {
    error!("irq_lower");
    system_off::<Hvc>().unwrap();
}

// 安全：没有此名称的其他全局函数。
#[unsafe(no_mangle)]
extern "C" fn fiq_lower(_elr: u64, _spsr: u64) {
    error!("fiq_lower");
    system_off::<Hvc>().unwrap();
}

// 安全：没有此名称的其他全局函数。
#[unsafe(no_mangle)]
extern "C" fn serror_lower(_elr: u64, _spsr: u64) {
    error!("serror_lower");
    system_off::<Hvc>().unwrap();
}
```

> - EL是例外级别；今天下午我们所有的例子都在 EL1 中运行。
> - 为简单起见，我们不区分当前 EL 的 SP0 和 SPx
>   异常，或者在 AArch32 和 AArch64 之间（对于较低的 EL 异常）。
> - 对于这个例子，我们只是记录异常并断电，正如我们所预料的那样
>   其中任何一个都会真正发生。
> - 我们或多或少可以想到异常处理程序和我们的主执行上下文
>   就像不同的线程一样。 [`Send`和`Sync`][1] 将控制我们可以分享的内容
>   它们之间，就像线程一样。例如，如果我们想分享一些
>   异常处理程序和程序其余部分之间的值，它是`Send`但不是`Sync`，然后我们需要将它包裹在类似`Mutex`并把
>   它处于静态。
>
> 异常向量的汇编代码：
>
> ```armasm
> /**
>  * 将易失性寄存器保存到堆栈上。目前这需要
>  * 14条指令，因此可以用在18条异常处理程序中
>  * 留下指示。
>  *
>  * 返回时，x0 和 x1 被初始化为 elr_el2 和 spsr_el2
>  * 分别可以用作第一个和第二个参数
>  * 后续呼叫的。
>  */
> .macro save_volatile_to_stack
> 	/* 保留堆栈空间并保存寄存器 x0-x18、x29 和 x30。 */
> 	stp x0, x1, [sp, #-(8 * 24)]!
> 	stp x2, x3, [sp, #8 * 2]
> 	stp x4, x5, [sp, #8 * 4]
> 	stp x6, x7, [sp, #8 * 6]
> 	stp x8, x9, [sp, #8 * 8]
> 	stp x10, x11, [sp, #8 * 10]
> 	stp x12, x13, [sp, #8 * 12]
> 	stp x14, x15, [sp, #8 * 14]
> 	stp x16, x17, [sp, #8 * 16]
> 	str x18, [sp, #8 * 18]
> 	stp x29, x30, [sp, #8 * 20]
>
> 	/*
> 	 * 保存 elr_el1 和 spsr_el1。这样我们就可以嵌套
> 	 * 例外，但仍然可以放松。
> 	 */
> 	mrs x0, elr_el1
> 	mrs x1, spsr_el1
> 	stp x0, x1, [sp, #8 * 22]
> .endm
>
> /**
>  * 从堆栈中恢复易失性寄存器。目前这个
>  * 需要 14 条指令，因此可以在异常处理程序中使用
>  * 同时还剩下 18 条指令；如果搭配
>  * save_volatile_to_stack，还有4条指令可供使用。
>  */
> .macro restore_volatile_from_stack
> 	/* 恢复寄存器 x2-x18、x29 和 x30。 */
> 	ldp x2, x3, [sp, #8 * 2]
> 	ldp x4, x5, [sp, #8 * 4]
> 	ldp x6, x7, [sp, #8 * 6]
> 	ldp x8, x9, [sp, #8 * 8]
> 	ldp x10, x11, [sp, #8 * 10]
> 	ldp x12, x13, [sp, #8 * 12]
> 	ldp x14, x15, [sp, #8 * 14]
> 	ldp x16, x17, [sp, #8 * 16]
> 	ldr x18, [sp, #8 * 18]
> 	ldp x29, x30, [sp, #8 * 20]
>
> 	/*
> 	 * 恢复寄存器 elr_el1 和 spsr_el1，使用 x0 和 x1 作为暂存。
> 	 */
> 	ldp x0, x1, [sp, #8 * 22]
> 	msr elr_el1, x0
> 	msr spsr_el1, x1
>
> 	/* 恢复x0和x1，并释放堆栈空间。 */
> 	ldp x0, x1, [sp], #8 * 24
> .endm
>
> /**
>  * 这是当前 EL 发生的异常的通用处理程序。它节省了
>  * 易失性寄存器到堆栈，调用 Rust 处理程序，恢复易失性
>  * 注册，然后返回。
>  *
>  * 如果我们不关心的话，这也适用于从较低 EL 获取的异常
>  * 非易失性寄存器。
>  *
>  * 保存状态并跳转到 Rust 处理程序需要 15 条指令，并且
>  * 恢复和返回也需要15条指令，所以我们可以拟合整个
>  * 处理程序的指令数量为 30 条，低于 32 条的限制。
>  */
> .macro current_exception handler:req
> 	save_volatile_to_stack
> 	bl \handler
> 	restore_volatile_from_stack
> 	eret
> .endm
>
> .section .text.vector_table_el1, "ax"
> .global vector_table_el1
> .balign 0x800
> vector_table_el1:
> sync_cur_sp0:
> 	current_exception sync_current
>
> .balign 0x80
> irq_cur_sp0:
> 	current_exception irq_current
>
> .balign 0x80
> fiq_cur_sp0:
> 	current_exception fiq_current
>
> .balign 0x80
> serr_cur_sp0:
> 	current_exception serror_current
>
> .balign 0x80
> sync_cur_spx:
> 	current_exception sync_current
>
> .balign 0x80
> irq_cur_spx:
> 	current_exception irq_current
>
> .balign 0x80
> fiq_cur_spx:
> 	current_exception fiq_current
>
> .balign 0x80
> serr_cur_spx:
> 	current_exception serror_current
>
> .balign 0x80
> sync_lower_64:
> 	current_exception sync_lower
>
> .balign 0x80
> irq_lower_64:
> 	current_exception irq_lower
>
> .balign 0x80
> fiq_lower_64:
> 	current_exception fiq_lower
>
> .balign 0x80
> serr_lower_64:
> 	current_exception serror_lower
>
> .balign 0x80
> sync_lower_32:
> 	current_exception sync_lower
>
> .balign 0x80
> irq_lower_32:
> 	current_exception irq_lower
>
> .balign 0x80
> fiq_lower_32:
> 	current_exception fiq_lower
>
> .balign 0x80
> serr_lower_32:
> 	current_exception serror_lower
> ```


[1]: ../../concurrency/send-sync.md
