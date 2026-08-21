+++
title = "13-栈、堆和指针"
date = 2026-08-21T12:46:00+08:00
weight = 14
type = "docs"
description = "栈、堆和指针 — Easy Rust 中文译本"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Easy Rust](https://dhghomon.github.io/easy_rust/)

> 原文链接: [https://dhghomon.github.io/easy_rust/Chapter_12.html](https://dhghomon.github.io/easy_rust/Chapter_12.html)

> 中文参考：[kumakichi/easy_rust_chs](https://kumakichi.github.io/easy_rust_chs/)

# 栈、堆和指针

栈、堆和指针在Rust中非常重要。

栈和堆是计算机中保存内存的两个地方。重要的区别是:

栈的速度非常快, 但堆的速度就不那么快了. 它也不是超慢，但栈总是更快。但是你不能一直使用栈，因为:
- Rust需要在编译时知道一个变量的大小。所以像`i32`这样的简单变量就放在堆栈上，因为我们知道它们的确切大小。你总是知道`i32`要4字节，因为32位=4字节。所以`i32`总是可以放在栈上。
- 但有些类型在编译时不知道大小。但是栈需要知道确切的大小。那么你该怎么做呢？首先你把数据放在堆中，因为堆中可以有任何大小的数据。然后为了找到它，一个指针就会进入栈。这很好，因为我们总是知道指针的大小。所以，计算机就会先去栈，读取指针，然后跟着指针到数据所在的堆。

指针听起来很复杂，但它们很容易。指针就像一本书的目录。想象一下这本书。

```text
MY BOOK

TABLE OF CONTENTS

Chapter                        Page
Chapter 1: My life              1
Chapter 2: My cat               15
Chapter 3: My job               23
Chapter 4: My family            30
Chapter 5: Future plans         43
```

所以这就像五个指针。你可以阅读它们，找到它们所说的信息。"我的生活"这一章在哪里？在第1页(它*指向*第1页)。"我的工作"这一章在哪里？它在第23页。

在Rust中通常看到的指针叫做**引用**。这是重要的部分，要知道:一个引用指向另一个值的内存。引用意味着你*借*了这个值，但你并不拥有它。这和我们的书一样:目录并不拥有信息。章节才是信息的主人。在Rust中，引用文献的前面有一个`&`。所以:

- `let my_variable = 8`是一个普通的变量，但是:
- `let my_reference = &my_variable`是一个引用。

你把 `my_reference = &my_variable` 读成这样: "my_reference是对my_variable的引用". 或者:"my_reference是对my_variable的引用"。

这意味着`my_reference`只看`my_variable`的数据。`my_variable`仍然拥有它的数据。

你也可以有一个引用的引用，或者任何数量的引用。

```rust
fn main() {
    let my_number = 15; // 这是 i32
    let single_reference = &my_number; // 这是 &i32
    let double_reference = &single_reference; // 这是 &&i32
    let five_references = &&&&&my_number; // 这是 &&&&&i32
}
```

这些都是不同的类型，就像 "朋友的朋友"和 "朋友"不同一样。
