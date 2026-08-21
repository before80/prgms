+++
title = "03-字符类型"
date = 2026-08-18T08:45:00+08:00
weight = 68
type = "docs"
description = "字符类型 — The Rust Reference"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Reference](https://doc.rust-lang.org/reference/)

> 原文链接: [https://doc.rust-lang.org/reference/types/char.html](https://doc.rust-lang.org/reference/types/char.html)

r[type.char]
# 字符类型

r[type.char.intro]
`char` 类型表示单个 [Unicode 标量值][Unicode scalar value]（即非代理项的码点）。

> [!EXAMPLE]
> ```rust
> let c: char = 'a';
> let emoji: char = '😀';
> let unicode: char = '\u{1F600}';
> ```

> **注意**
> 关于 `char` 类型的 impl，见[标准库文档][`char`]。

r[type.char.value]
`char` 类型的值表示为 32 位无符号字，取值范围为 0x0000 到 0xD7FF 或 0xE000 到 0x10FFFF。创建落在此范围之外的 `char` 立即构成[未定义行为][undefined behavior]。

r[type.char.layout]
在所有平台上，`char` 保证与 `u32` 具有相同的大小和对齐。

r[type.char.validity]
`char` 的每一个字节都保证已初始化。换句话说，`transmute::<char, [u8; size_of::<char>()]>(...)` 总是健全的——但由于某些位模式不是合法 `char`，反过来并不总是健全。

[Unicode scalar value]: http://www.unicode.org/glossary/#unicode_scalar_value
[undefined behavior]: ../behavior-considered-undefined.md
