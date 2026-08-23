+++
title = "4 不太好的安全双端队列"
date = 2026-08-23T16:06:00+08:00
weight = 40
type = "docs"
description = ""
isCJKLanguage = true
draft = false

+++


> 原文链接: [https://rust-unofficial.github.io/too-many-lists/fourth.html](https://rust-unofficial.github.io/too-many-lists/fourth.html)

既然我们已经见过 `Rc`，也听说过内部可变性，这让人产生一个有趣的想法……也许我们*可以*通过 `Rc` 来修改数据。如果*真是*这样，也许我们就能完全安全地实现一个*双向*链表！

在这个过程中，我们会熟悉*内部可变性*，而且很可能会以惨痛的方式认识到：安全并不意味着*正确*。双向链表很难，我总是在某个地方犯错。

让我们新建一个名为 `fourth.rs` 的文件：

```rust
// 在 lib.rs 中

pub mod first;
pub mod second;
pub mod third;
pub mod fourth;
```

这又是一次从零开始的实现，不过和往常一样，我们很可能会发现有些逻辑可以原封不动地复用。

免责声明：这一章基本上是在演示这是一个非常糟糕的主意。
