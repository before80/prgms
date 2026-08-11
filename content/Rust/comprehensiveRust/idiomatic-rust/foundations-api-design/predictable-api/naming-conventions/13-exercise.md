+++
title = "2.2.1.13 练习"
date = 2026-08-11T11:30:00+08:00
weight = 413
type = "docs"
description = "13-练习 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/idiomatic/foundations-api-design/predictable-api/naming-conventions/exercise.html](https://google.github.io/comprehensive-rust/idiomatic/foundations-api-design/predictable-api/naming-conventions/exercise.html)

# 2.2.1.13 练习

1. 这些名字暗示它们做什么？
2. 这些签名该如何命名？

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
// 这些方法的类型是什么？
Option::is_some // ?
slice::get // ?
slice::get_unchecked_mut // ?
Option::as_ref // ?
str::from_utf8_unchecked_mut // ?
Rc::get_mut // ?
Vec::dedup_by_key // ?

// 具有这些类型的方法该叫什么？
fn ____(String) -> Self;
fn ____(&self) -> Option<&InnerType>; // InnerType 的细节无关紧要。
fn ____(self, String) -> Self;
fn ____(&mut self) -> Option<&mut InnerType>;
```

> - 与学员一起过一遍示例中的方法，讨论函数的类型应当是什么。
>
> - 过一遍未命名的方法，头脑风暴这些方法应有什么名字。
>
>   缺失类型的答案：
>   - `Option::is_some(&self) -> bool`
>   - `slice::get(&self /* &[T] */, usize) -> Option<&T>`
>   - `slice::get_unchecked_mut(&self /* &[T] */, usize) -> &T`（unsafe 且简化）
>   - `Option::as_ref(&self /* &Option<T> */) -> Option<&T>`
>   - `str::from_utf8_unchecked_mut(v: &mut [u8]) -> &mut str`（unsafe）
>   - `Rc::get_mut(&mut self /* &mut Rc<T> */) -> Option<&mut T>`（简化）
>   - `Vec::dedup_by_key<K: PartialEq>(&mut self /* &mut Vec<T> */, key: impl FnMut(&mut T) -> K)`
>     （简化）
>
>   缺失名字的答案：
>   - `fn from_string(String) -> Self`
>   - `fn inner(&self) -> Option<&InnerType>` 或 `as_ref`，取决于语境
>   - `fn with_string(self, String) -> Self`
>   - `fn inner_mut(&mut self) -> Option<&mut InnerType>` 或 `as_ref_mut`，
>     取决于语境

