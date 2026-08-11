+++
title = "3.4 注释"
date = 2026-08-05T08:44:00+08:00
weight = 13
type = "docs"
description = "在 Rust 源码中编写行注释"
isCJKLanguage = true
draft = false
rust_version = "1.97.1"

+++

> 译文 · 基于 [The Rust Programming Language](https://doc.rust-lang.org/stable/book/)（rustc 1.97.1）

# 注释 {#comments}


> 原文链接: [https://doc.rust-lang.org/stable/book/ch03-04-comments.html](https://doc.rust-lang.org/stable/book/ch03-04-comments.html)


## 注释 {#comments-heading}

　　所有程序员都力求让代码易于理解，但有时仍需要额外说明。这时，程序员会在源代码中留下*注释*（comments）：编译器会忽略它们，但阅读源码的人可能会觉得有用。

　　下面是一条简单的注释：

```rust
// hello, world
```

　　在 Rust 中，惯用的注释风格是以两个斜杠开始，注释一直持续到行末。若注释超过一行，每一行都需要包含 `//`，像这样：

```rust
// So we're doing something complicated here, long enough that we need
// multiple lines of comments to do it! Whew! Hopefully, this comment will
// explain what's going on.
```

　　注释也可以放在包含代码的行末：

<span class="filename">文件名：src/main.rs</span>

```rust
fn main() {
    let lucky_number = 7; // I'm feeling lucky today
}
```

　　但你会更常看到这种格式：注释单独占一行，写在它所注解的代码上方：

<span class="filename">文件名：src/main.rs</span>

```rust
fn main() {
    // I'm feeling lucky today
    let lucky_number = 7;
}
```

　　Rust 还有另一种注释——文档注释，我们会在第 14 章的[「将 Crate 发布到 Crates.io」][publishing]一节讨论。

[publishing]: ../../more-about-cargo/02-publishing-to-crates-io/
