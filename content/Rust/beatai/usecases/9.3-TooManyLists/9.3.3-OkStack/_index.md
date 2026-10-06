+++
title = "还可以的单向链表"
date = 2026-10-06T16:45:00+08:00
weight = 5
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

> 原文链接: [https://beatai.org/rust-course/too-many-lists/ok-stack/intro](https://beatai.org/rust-course/too-many-lists/ok-stack/intro)

# 还可以的单向链表

　在之前我们写了一个最小可用的单向链表，下面一起来完善下，首先创建一个新的文件 `src/second.rs`，然后在 `lib.rs` 中引入：
```rust
// in lib.rs

pub mod first;
pub mod second;
```

　并将 `first.rs` 中的所有内容拷贝到 `second.rs` 中。
