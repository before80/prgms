+++
title = "4.1 常见前置条件"
date = 2026-08-11T11:30:00+08:00
weight = 517
type = "docs"
description = "常见前置条件 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/unsafe-deep-dive/safety-preconditions/common-preconditions.html](https://google.github.io/comprehensive-rust/unsafe-deep-dive/safety-preconditions/common-preconditions.html)

# 4.1 常见前置条件

- 别名与可变性（Aliasing and Mutability）
- 对齐（Alignment）
- 数组访问在边界内
- 初始化（Initialization）
- 生命周期（Lifetimes）
- 指针来源（Pointer provenance）
- 有效性（Validity）
- 内存（Memory）

> 避免花太多时间逐一解释每个前置条件：课程后续会深入细节。此处意在说明前置条件有很多种。
>
> 「这只是一份不完整的列表，但足以让我们开始思考几个主要的安全前置条件。」
>
> - 有效性（Validity）。值必须是其所代表类型的有效值。Rust 的引用不能为 null。用 `unsafe` 创建会导致……
> - 对齐（Alignment）。对值的引用必须正确对齐，这意味着……
> - 别名（Aliasing）。所有 Rust 代码都必须遵守 Rust 的借用（borrowing）规则。如果你手动从指针创建可变引用（`&mut T`），则只能创建……
> - 初始化（Initialization）。Rust 类型的所有实例必须完全初始化。要从原始内存创建值，我们需要确保已经写入……
> - 指针来源（Pointer provenance）。指针的来源很重要。将 `usize` 转换为原始指针已不再被允许。
> - 生命周期（Lifetimes）。引用不能比其指向的对象活得更久。
>
> 有些条件比初看时更加微妙。
>
> 以「数组访问在边界内」为例。读取该内存位置（即解引用）并不是程序崩溃所必需的。创建越界引用就已经破坏了编译器的假设，导致行为异常。
>
> Rust 告诉 LLVM 使用其 `getelementptr inbounds` 假设。该假设会导致编译器后续的优化过程行为异常（因为越界内存访问不可能发生）。
>
> 可选：打开 [playground][1]，其中展示了下面的代码。说明这本质上是用 Rust 语法写的 C 函数，从数组中获取元素。点击 **Show LLVM IR** 按钮生成 LLVM IR。高亮 `getelementptr inbounds i32, ptr %array, i64 %offset`。
>
> ```rust
> // Copyright 2026 Google LLC
> // SPDX-License-Identifier: Apache-2.0
> #[unsafe(no_mangle)]
> pub unsafe fn get(array: *const i32, offset: isize) -> i32 {
>     unsafe { *array.offset(offset) }
> }
> ```
>
> 预期输出（需要高亮的那行以 `%_3` 开头）：
>
> ```llvm
> define noundef i32 @get(ptr noundef readonly captures(none) %array, i64 noundef %offset) unnamed_addr #0 {
> start:
>   %_3 = getelementptr inbounds i32, ptr %array, i64 %offset
>   %_0 = load i32, ptr %_3, align 4, !noundef !3
>   ret i32 %_0
> }
> ```
>
> [1]: https://play.rust-lang.org/?version=stable&mode=release&edition=2024&gist=4116c4de01c863cac918f193448210b1
>
> 边界：你正确指出，由于 LLVM 的 inbounds 假设，即使不解引用，创建越界指针（超出「末尾后一位」规则）也是 UB。

