+++
title = "2.1.8 练习"
date = 2026-08-11T11:30:00+08:00
weight = 398
type = "docs"
description = "08-练习 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/idiomatic/foundations-api-design/meaningful-doc-comments/exercise.html](https://google.github.io/comprehensive-rust/idiomatic/foundations-api-design/meaningful-doc-comments/exercise.html)

# 2.1.8 练习

不必要的细节有时可能暗示着真正需要文档化的东西。

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
/// Sorts a slice. Implemented using recursive quicksort.
fn sort_quickly<T: Ord>(to_sort: &mut [T]) { ... }
```

> - 问问学员：这个注释对该函数是否必要？
>
> - 叙事：扮演课堂与作者之间的中介（例如 PM、经理等），告诉学员该函数作者在推回。
>
> - 问问学员：为何写这种注释的作者会推回？
>
>   若学员追问作者为何推回，先不要给细节。
>
> - 问问学员：调用者为何需要知道使用的排序算法？
>
> - 叙事：从与原作者的会议“回来”，向学员解释：这是应用代码，作用于不可信数据，而不可信数据
>   [可能被恶意构造以在排序时触发二次行为](https://www.cs.dartmouth.edu/~doug/mdmspe.pdf)。
>
> - 问问学员：现在有了更多细节，该如何注释这个函数？
>
>   要点是：是否算实现细节，很大程度上取决于公开契约是什么（例如，你能否提供不可信数据），这需要仔细判断。
>
>   考虑注释是在解释用了 for 循环（不必要细节），还是在解释内部算法有已知漏洞（文档把注意力引向错误之处）。

