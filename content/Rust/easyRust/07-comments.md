+++
title = "07-注释"
date = 2026-08-21T12:46:00+08:00
weight = 8
type = "docs"
description = "注释 — Easy Rust 中文译本"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Easy Rust](https://dhghomon.github.io/easy_rust/)

> 原文链接: [https://dhghomon.github.io/easy_rust/Chapter_6.html](https://dhghomon.github.io/easy_rust/Chapter_6.html)

> 中文参考：[kumakichi/easy_rust_chs](https://kumakichi.github.io/easy_rust_chs/)

# 注释

注释是给程序员看的，而不是给电脑看的。写注释是为了帮助别人理解你的代码。 这也有利于帮助你以后理解你的代码。 (很多人写了很好的代码，但后来却忘记了他们为什么要写它。)在Rust中写注释，你通常使用 `//`．

```rust
fn main() {
    // Rust 程序从 fn main() 开始
    // 代码写在块里，以 { 开始、以 } 结束
    let some_number = 100; // 这里想写多少都可以，编译器不会看
}
```

当你这样做时，编译器不会看`//`右边的任何东西。

还有一种注释，你用`/*`开始写，`*/`结束写。这个写在你的代码中间很有用。

```rust
fn main() {
    let some_number/*: i16*/ = 100;
}
```

对编译器来说，`let some_number/*: i16*/ = 100;`看起来像`let some_number = 100;`。

`/* */`形式对于超过一行的非常长的注释也很有用。在这个例子中，你可以看到你需要为每一行写`//`。但是如果您输入 `/*`，它不会停止，直到您用 `*/` 完成它。

```rust
fn main() {
    let some_number = 100; /* 让我跟你说说
    这个数字。
    它是 100，我最喜欢的数字。
    名字叫 some_number，但其实我觉得…… */

    let some_number = 100; // 让我跟你说说
    // 这个数字。
    // 它是 100，我最喜欢的数字。
    // 名字叫 some_number，但其实我觉得……
}
```
