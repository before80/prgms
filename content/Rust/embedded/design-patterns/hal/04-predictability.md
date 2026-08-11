+++
title = "04-可预测性"
date = 2026-08-01T10:38:00+08:00
weight = 126
type = "docs"
description = "可预测性（Predictability）"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Embedded Rust Book](https://doc.rust-lang.org/stable/embedded-book/)

# 可预测性 {#predictability}


> 原文链接: [https://doc.rust-lang.org/stable/embedded-book/design-patterns/hal/predictability.html](https://doc.rust-lang.org/stable/embedded-book/design-patterns/hal/predictability.html)


<a id="c-ctor"></a>
## 使用构造函数而非扩展 trait（C-CTOR） {#constructors-are-used-instead-of-extension-traits-c-ctor}

凡是 HAL 为其增加功能的外设，都应包装在新类型中，即便该功能不需要额外字段。

应避免为原始外设实现扩展 trait。

<a id="c-inline"></a>
## 在适当时为方法添加 `#[inline]`（C-INLINE） {#methods-are-decorated-with-inline-where-appropriate-c-inline}

Rust 编译器默认不会跨 crate 边界执行充分内联。嵌入式应用对意外的代码体积增长敏感，因此应按如下方式使用 `#[inline]` 引导编译器：

* 所有「小」函数都应标记 `#[inline]`。「小」是主观判断，但一般而言，预期会编译成个位数指令序列的函数都可视为小函数。
* 很可能以常量值作为参数的函数也应标记 `#[inline]`。这样在函数输入已知时，编译器甚至能在编译期完成复杂的初始化逻辑。
