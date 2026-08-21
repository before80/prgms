+++
title = "16-const 和 static"
date = 2026-08-21T12:46:00+08:00
weight = 17
type = "docs"
description = "const 和 static — Easy Rust 中文译本"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Easy Rust](https://dhghomon.github.io/easy_rust/)

> 原文链接: [https://dhghomon.github.io/easy_rust/Chapter_15.html](https://dhghomon.github.io/easy_rust/Chapter_15.html)

> 中文参考：[kumakichi/easy_rust_chs](https://kumakichi.github.io/easy_rust_chs/)

# const 和 static

有两种声明值的方法，不仅仅是用`let`。它们是`const`和`static`。另外，Rust不会使用类型推理：你需要为它们编写类型。这些都是用于不改变的值（`const`意味着常量）。区别在于:

- `const`是用于不改变的值，当使用它时，名字会被替换成值。
- `static`与`const`类似，但有一个固定的内存位置，可以作为一个全局变量使用。

所以它们几乎是一样的。Rust程序员几乎总是使用`const`。

一般用全大写字母作为名字，而且通常在`main`之外，这样它们就可以在整个程序中生存。

两个例子是 `const NUMBER_OF_MONTHS: u32 = 12;` 和 `static SEASONS: [&str; 4] = ["Spring", "Summer", "Fall", "Winter"];`
