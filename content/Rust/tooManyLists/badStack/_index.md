+++
title = "1 不太好的单向链表栈"
date = 2026-08-23T16:06:00+08:00
weight = 10
type = "docs"
description = ""
isCJKLanguage = true
draft = false

+++


> 原文链接: [https://rust-unofficial.github.io/too-many-lists/first.html](https://rust-unofficial.github.io/too-many-lists/first.html)

这一章会*远远*是最长的一章，因为我们需要介绍 Rust 的几乎所有基础知识，并且会「用困难的方式」逐步构建一些东西，以便更好地理解这门语言。

我们会把第一个链表放在 `src/first.rs` 里。需要告诉 Rust，`first.rs` 是我们的库要用到的东西。只需在 `src/lib.rs`（Cargo 为我们创建的）顶部加上：

```rust
// 在 lib.rs 中
pub mod first;
```
