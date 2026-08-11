+++
title = "1.1 准备使用 Rust"
date = 2026-08-11T11:30:00+08:00
weight = 313
type = "docs"
description = "01-准备使用 Rust — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/bare-metal/aps/entry-point.html](https://google.github.io/comprehensive-rust/bare-metal/aps/entry-point.html)

# 1.1 准备使用 Rust

在开始运行 Rust 代码之前，我们需要进行一些初始化。

```armasm
/**
 * 这是图像的通用入口点。它执行的是
 * 准备要运行的加载映像所需的操作。
 * 具体来说，它
 *
 * - 使用虚拟到物理的身份映射设置MMU
 * 地址并启用缓存
 * - 启用浮点
 * - 使用寄存器 x25 及以上将 bss 部分归零
 * - 准备堆栈，指向图像中的一个部分
 * - 设置异常向量
 * - 分支到 Rust 的 `main` 函数
 *
 * 它为 Rust 入口点保留 x0-x3，因为它们可能包含
 * 启动参数。
 */
.section .init.entry, "ax"
.global entry
entry:
    /*
     * 加载并应用内存管理配置，准备好
     * 启用 MMU 和缓存。
     */
    adrp x30, idmap
    msr ttbr0_el1, x30

    mov_i x30, .Lmairval
    msr mair_el1, x30

    mov_i x30, .Ltcrval
    /* 将支持的 PA 范围复制到 TCR_EL1.IPS。 */
    mrs x29, id_aa64mmfr0_el1
    bfi x30, x29, #32, #4

    msr tcr_el1, x30

    mov_i x30, .Lsctlrval

    /*
     * 确保这一点之前的所有事情都已完成，然后
     * 在任何可能过时的本地 TLB 条目失效之前
     * 开始被使用。
     */
    isb
    tlbi vmalle1
    ic iallu
    dsb nsh
    isb

    /*
     * 配置 sctlr_el1 以启用 MMU 和缓存，然后不继续
     * 直到这完成。
     */
    msr sctlr_el1, x30
    isb

    /* 禁用 EL1 中的捕获浮点访问。 */
    mrs x30, cpacr_el1
    orr x30, x30, #(0x3 << 20)
    msr cpacr_el1, x30
    isb

    /* 将 bss 部分清零。 */
    adr_l x29, bss_begin
    adr_l x30, bss_end
0:  cmp x29, x30
    b.hs 1f
    stp xzr, xzr, [x29], #16
    b 0b

1:  /* Prepare the stack. */
    adr_l x30, boot_stack_end
    mov sp, x30

    /* 设置异常向量。 */
    adr x30, vector_table_el1
    msr vbar_el1, x30

    /* 调用 Rust 代码。 */
    bl main

    /* 永远循环等待中断。 */
2:  wfi
    b 2b
```

> 这段代码位于`src/bare-metal/aps/examples/src/entry.S`。没有必要
> 详细理解这一点——要点是需要一些低级设置
> 满足 Rust 对系统的期望。
>
> - 这与 C 的情况相同：初始化处理器状态，
>   将 BSS 清零，并设置堆栈指针。
>   - BSS（区块起始符号，由于历史原因）是区块链的一部分
>     包含静态分配变量的目标文件
>     初始化为零。图像中省略了它们，以避免浪费空间
>     在零上。编译器假设加载程序将负责归零
>     他们。
> - BSS 可能已经被清零，具体取决于内存的初始化方式和
>   图像已加载，但为了确定我们将其归零。
> - 在读取或写入任何内存之前，我们需要启用 MMU 和缓存。如果
>   我们不：
>   - 未对齐的访问将会出错。我们构建 Rust 代码
>     `aarch64-unknown-none`设定的目标`+strict-align`以防止
>     编译器不会生成未对齐的访问，所以在这方面应该没问题
>     情况，但一般情况下不一定如此。
>   - 如果它在虚拟机中运行，这可能会导致缓存一致性问题。这
>     问题是虚拟机在禁用缓存的情况下直接访问内存，
>     而主机具有同一内存的可缓存别名。即使主持人
>     没有显式访问内存，推测性访问可能会导致缓存
>     填充，然后当缓存时，其中一个或另一个的更改将丢失
>     已清理或虚拟机启用缓存。 （缓存由物理地址作为键控，
>     不是 VA 或 IPA。）
> - 为了简单起见，我们只使用硬编码的页表（参见`idmap.S`） 那
>   身份映射设备的前 1 GiB 地址空间，接下来的 1 GiB
>   DRAM，另外 1 GiB 更高，可容纳更多设备。这和记忆相符
>   QEMU 使用的布局。
> - 我们还设置了异常向量（`vbar_el1`），我们将看到更多关于
>   之后。
> - 今天下午的所有示例都假设我们将在异常级别 1 下运行
>   （EL1）。如果您需要在不同的异常级别运行，则需要
>   修改`entry.S`因此。

