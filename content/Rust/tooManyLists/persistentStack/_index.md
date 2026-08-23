+++
title = "3 持久化单向链表栈"
date = 2026-08-23T16:06:00+08:00
weight = 30
type = "docs"
description = ""
isCJKLanguage = true
draft = false

+++


> 原文链接: [https://rust-unofficial.github.io/too-many-lists/third.html](https://rust-unofficial.github.io/too-many-lists/third.html)

好，我们已经掌握了可变单链表栈。

接下来从*单一*所有权转向*共享*所有权，写一个*持久化*不可变单链表。这正是函数式程序员熟悉和喜爱的那种链表。你可以取头*或*尾，把一个人的头接到另一个人的尾巴上……基本上就这些。不可变性真是厉害。

过程中我们主要熟悉 Rc 和 Arc，这也会为下一个*改变游戏规则*的链表铺路。

新建一个名为 `third.rs` 的文件：

```rust
// 在 lib.rs 中

pub mod first;
pub mod second;
pub mod third;
```

这次不复制粘贴。这是全新开工。
