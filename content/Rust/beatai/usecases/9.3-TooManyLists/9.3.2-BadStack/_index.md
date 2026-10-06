+++
title = "不太优秀的单向链表：栈"
date = 2026-10-06T16:45:00+08:00
weight = 4
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

> 原文链接: [https://beatai.org/rust-course/too-many-lists/bad-stack/intro](https://beatai.org/rust-course/too-many-lists/bad-stack/intro)

# 不太优秀的单向链表：栈

　本章，让我们用一个不咋样的单向链表来实现一个栈数据结构，因为不咋样，实现起来倒是很简单。

　首先，创建一个文件 `src/first.rs` 用于存放本章节的链表代码，虽然糟糕，也不能用完就扔，大家说是不 :P 然后在 `lib.rs` 中添加这一行代码：

```rust
// in lib.rs
pub mod first;
```
