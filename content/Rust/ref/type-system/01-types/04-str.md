+++
title = "04-字符串切片类型"
date = 2026-08-18T08:45:00+08:00
weight = 69
type = "docs"
description = "字符串切片类型 — The Rust Reference"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Reference](https://doc.rust-lang.org/reference/)

> 原文链接: [https://doc.rust-lang.org/reference/types/str.html](https://doc.rust-lang.org/reference/types/str.html)

r[type.str]
# 字符串切片类型

r[type.str.intro]
字符串切片（`str`）类型表示一个字符序列。

```rust
let greeting1: &str = "Hello, world!";
let greeting2: &str = "你好，世界";
```

> **注意**
> 关于 `str` 类型的 impl，见[标准库文档][`str`]。

r[type.str.value]
`str` 类型的值与 `[u8]`（8 位无符号字节切片）的表示方式相同。

> **注意**
> 标准库对 `str` 有额外假定：作用于 `str` 的方法假定并确保其包含的数据是合法 UTF-8。对非 UTF-8 缓冲区调用 `str` 方法现在或将来都可能导致[未定义行为][undefined behavior]。

r[type.str.unsized]
`str` 是[动态大小类型][dynamically sized type]。它只能通过指针类型实例化，例如 `&str`。`&str` 的布局与 `&[u8]` 的布局相同。

[undefined behavior]: ../behavior-considered-undefined.md
[dynamically sized type]: ../dynamically-sized-types.md
