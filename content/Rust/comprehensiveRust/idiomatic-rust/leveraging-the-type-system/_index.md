+++
title = "3 利用类型系统"
date = 2026-08-11T11:30:00+08:00
weight = 425
type = "docs"
description = "利用类型系统 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/idiomatic/leveraging-the-type-system.html](https://google.github.io/comprehensive-rust/idiomatic/leveraging-the-type-system.html)

# 3 利用类型系统

Rust 的类型系统很有**表现力**：你可以用类型和 trait 构建抽象，让代码更难被误用。

在某些情况下，甚至能在**编译期**强制正确性，且没有运行时开销。

类型和 trait 可以建模业务领域中的概念与约束。精心设计后，能提升整个代码库的清晰度与可维护性。

> 讲师可补充的要点：
>
> - Rust 的类型系统借鉴了许多函数式语言的思想。
>
>   例如，Rust 的枚举在 Haskell、OCaml 等语言中称为「代数数据类型」（algebraic data types）。在寻求如何用类型做设计的指导时，可以参考面向函数式语言的学习材料。[《Domain Modeling Made Functional》][1] 是该主题的优秀资源，示例用 F# 编写。
>
> - 尽管 Rust 有函数式渊源，并非所有函数式设计模式都能轻松迁移到 Rust。
>
>   例如，要设计利用高阶函数与高阶类型（higher-kinded types）的 API，需要对大量进阶主题有扎实掌握。
>
>   请按具体情况评估：更偏命令式的做法是否更易实现。可考虑就地修改，并依靠 Rust 的借用检查器（borrow checker）与类型系统来控制何处、何物可被修改。
>
> - 对面向对象设计模式也应同样谨慎。Rust 不支持继承，对象拆分时需考虑借用检查器带来的约束。
>
> - 可提及类型级编程常用于打造「零成本抽象」，不过这个标签可能有误导：对编译时间与代码复杂度的影响可能很大。


本小节约需 7 小时 30 分钟。内容包括：

| 内容 | 时长 |
| --- | --- |
| 利用类型系统 | 5 分钟 |
| Newtype 模式 | 20 分钟 |
| RAII | 1 小时 50 分钟 |
| 扩展 Trait | 1 小时 5 分钟 |
| Typestate 模式 | 1 小时 5 分钟 |
| 借用检查不变量 | 1 小时 30 分钟 |
| 令牌类型 | 1 小时 35 分钟 |


[1]: https://pragprog.com/titles/swdddf/domain-modeling-made-functional/
