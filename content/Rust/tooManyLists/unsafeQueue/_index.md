+++
title = "5 不安全的单向链表队列"
date = 2026-08-23T16:06:00+08:00
weight = 50
type = "docs"
description = ""
isCJKLanguage = true
draft = false

+++


> 原文链接: [https://rust-unofficial.github.io/too-many-lists/fifth.html](https://rust-unofficial.github.io/too-many-lists/fifth.html)

好吧，那引用计数加内部可变性的东西有点失控了。Rust 真的不指望你平时就那样做吗？嗯，是也不是。`Rc` 和 `RefCell` 处理简单情况很棒，但会变得难以驾驭。尤其是当你想隐藏这一切正在发生的时候。肯定有更好的办法！

在这一章里，我们要回到单链表，实现一个单链表队列，来涉足*裸指针*和*Unsafe Rust*。

> **旁白：** 我会指出错误。

而且我们*不会*犯*任何*错误。

让我们新建一个名为 `fifth.rs` 的文件：

```rust
// 在 lib.rs 中

pub mod first;
pub mod second;
pub mod third;
pub mod fourth;
pub mod fifth;
```

我们的代码很大程度上会派生自 `second.rs`，因为在链表的世界里，队列基本上是对栈的增强。不过我们还是要从头开始，因为有一些关于布局等的基本问题需要解决。
