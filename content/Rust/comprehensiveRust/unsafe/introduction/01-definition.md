+++
title = "3.1 Unsafe Rust 的定义"
date = 2026-08-11T11:30:00+08:00
weight = 501
type = "docs"
description = "01-Unsafe Rust 的定义 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/unsafe-deep-dive/introduction/definition.html](https://google.github.io/comprehensive-rust/unsafe-deep-dive/introduction/definition.html)

# 3.1 Unsafe Rust 的定义

```bob
╭───────────────────────────────────────────────────────────╮
│╭─────────────────────────────────────────────────────────╮│
││                                                         ││
││  Safe                                                   ││
││  Rust                                                   ││
││                                                         ││
││                                                         ││
│╰─────────╮                                               ││
│          │                                               ││
│  Unsafe  │                                               ││
│   Rust   │                                               ││
│          ╰───────────────────────────────────────────────╯│
╰───────────────────────────────────────────────────────────╯
```

> 「Unsafe Rust 是 Safe Rust 的超集。」
>
> 「Unsafe Rust 增加了额外能力，例如允许你解引用 raw pointer（原始指针），以及调用若使用不当可能破坏 Rust 安全保证的函数。」
>
> 「这些额外能力称为 _unsafe 操作_。」
>
> 「unsafe 操作构成了 Rust 标准库的基础。例如，若不能解引用 raw pointer，就不可能实现 `Vec` 或 `Box`。」
>
> 「编写 Unsafe Rust 时，编译器仍会协助你。borrow checking（借用检查）与类型安全仍然适用。unsafe 操作有各自的规则，本课程将学习这些规则。」
>
> [Rust Reference] 中的 unsafe 操作（不必在此花太多时间）：
>
> > 以下语言级特性不能在 Rust 的安全子集中使用：
> >
> > - 解引用 raw pointer。
> > - 读取或写入可变或 unsafe 的外部 static 变量。
> > - 访问 union 的字段，除非是为了赋值。
> > - 调用 `unsafe` 函数。
> > - 从没有 `<target_feature>` 属性启用相同特性的函数中，调用带有 `<target_feature>` 的安全函数。
> > - 实现 unsafe trait。
> > - 声明 extern 块。
> > - 对项应用 unsafe 属性。
>
> [Rust Reference]: https://doc.rust-lang.org/reference/unsafety.html

