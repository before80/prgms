+++
title = "第17章 不安全性"
date = 2026-08-18T08:45:00+08:00
weight = 108
type = "docs"
description = "不安全性 — The Rust Reference"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Reference](https://doc.rust-lang.org/reference/)

> 原文链接: [https://doc.rust-lang.org/reference/unsafety.html](https://doc.rust-lang.org/reference/unsafety.html)

r[safety]
# 不安全性

r[safety.intro]
不安全操作是那些可能违反 Rust 静态语义所保证的内存安全的操作。

r[safety.unsafe-ops]
下列语言级特性不能在 Rust 的安全子集中使用：

r[safety.unsafe-deref]
- 解引用[裸指针][raw pointer]。

r[safety.unsafe-static]
- 读取或写入[可变][mutable]或不安全的[外部][external]静态变量。

r[safety.unsafe-union-access]
- 访问 [`union`] 的字段（赋值除外）。

r[safety.unsafe-call]
- 调用不安全函数。

r[safety.unsafe-target-feature-call]
- 从未启用相同特性的 `target_feature` 属性的函数中，调用带有 [`target_feature`][attributes.codegen.target_feature] 标记的安全函数（参见 [attributes.codegen.target_feature.safety-restrictions]）。

r[safety.unsafe-impl]
- 实现[不安全 trait][unsafe trait]。

r[safety.unsafe-extern]
- 声明 [`extern`] 块[^extern-2024]。

r[safety.unsafe-attribute]
- 将[不安全属性][unsafe attribute]应用到项上。

[^extern-2024]: 在 2024 edition 之前，允许在没有 `unsafe` 的情况下声明 extern 块。

[`extern`]: items/external-blocks.md
[`union`]: items/unions.md
[mutable]: items/static-items.md#mutable-statics
[external]: items/external-blocks.md
[raw pointer]: types/pointer.md
[unsafe trait]: items/traits.md#unsafe-traits
[unsafe attribute]: attributes.md
