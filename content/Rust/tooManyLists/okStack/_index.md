+++
title = "2 还可以的单向链表栈"
date = 2026-08-23T16:06:00+08:00
weight = 20
type = "docs"
description = ""
isCJKLanguage = true
draft = false

+++


> 原文链接: [https://rust-unofficial.github.io/too-many-lists/second.html](https://rust-unofficial.github.io/too-many-lists/second.html)

在上一章里，我们实现了一个最小可用的单链表栈。不过有几处设计选择让它有点难用。
我们来把它改得好用一些。在此过程中，我们会：

* 不再重复造轮子
* 让链表能处理任意元素类型
* 添加 peek 功能
* 让链表可迭代

同时我们还会学到：

* Option 的高级用法
* 泛型
* 生命周期
* 迭代器

先新建一个名为 `second.rs` 的文件：

```rust
// 在 lib.rs 中

pub mod first;
pub mod second;
```

然后把 `first.rs` 里的内容全部复制进去。
