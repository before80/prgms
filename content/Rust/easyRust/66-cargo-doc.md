+++
title = "66-cargo 文档"
date = 2026-08-21T12:46:00+08:00
weight = 67
type = "docs"
description = "cargo 文档 — Easy Rust 中文译本"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Easy Rust](https://dhghomon.github.io/easy_rust/)

> 原文链接: [https://dhghomon.github.io/easy_rust/Chapter_65.html](https://dhghomon.github.io/easy_rust/Chapter_65.html)

> 中文参考：[kumakichi/easy_rust_chs](https://kumakichi.github.io/easy_rust_chs/)

# cargo 文档

你可能已经注意到，Rust文档看起来总是几乎一样。在左边你可以看到`struct`和`trait`，代码例子在右边等等。这是因为你只要输入`cargo doc`就可以自动创建文档。

即使是创建一个什么都不做的项目，也可以帮助你了解Rust中的特性。例如，这里有两个几乎什么都不做的结构体，以及一个也什么都不做的`fn main()`。

```rust
struct DoesNothing {}
struct PrintThing {}

impl PrintThing {
    fn prints_something() {
        println!("I am printing something");
    }
}

fn main() {}
```


但如果你输入`cargo doc --open`，你可以看到比你想象中更多的信息。首先它给你显示的是这样的:

```text
Crate rust_book

Structs
DoesNothing
PrintThing

Functions
main
```

但是如果你点击其中的一个结构，会让你看到很多你没有想到的trait。

```text
Struct rust_book::DoesNothing
[+] Show declaration
Auto Trait Implementations
impl RefUnwindSafe for DoesNothing
impl Send for DoesNothing
impl Sync for DoesNothing
impl Unpin for DoesNothing
impl UnwindSafe for DoesNothing
Blanket Implementations
impl<T> Any for T
where
    T: 'static + ?Sized,
[src]
[+]
impl<T> Borrow<T> for T
where
    T: ?Sized,
[src]
[+]
impl<T> BorrowMut<T> for T
where
    T: ?Sized,
[src]
[+]
impl<T> From<T> for T
[src]
[+]
impl<T, U> Into<U> for T
where
    U: From<T>,
[src]
[+]
impl<T, U> TryFrom<U> for T
where
    U: Into<T>,
[src]
[+]
impl<T, U> TryInto<U> for T
where
    U: TryFrom<T>,
```

这是因为Rust自动为每个类型实现的所有trait。

那么如果我们添加一些文档注释，当你输入`cargo doc`的时候就可以看到。

```rust
/// 这是一个什么也不做的结构体
struct DoesNothing {}
/// 这个结构体只有一个方法。
struct PrintThing {}
/// 它只是打印同一条消息。
impl PrintThing {
    fn prints_something() {
        println!("I am printing something");
    }
}

fn main() {}
```


现在会打印:

```text
Crate rust_book
Structs
DoesNothing This is a struct that does nothing
PrintThing  This struct only has one method.
Functions
main
```

当你使用很多别人的crate时，`cargo doc`是非常好的。因为这些crate都在不同的网站上，可能需要一些时间来搜索所有的crate。但如果你使用`cargo doc`，你就会把它们都放在你硬盘的同一个地方。
