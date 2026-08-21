+++
title = "43-Cow"
date = 2026-08-21T12:46:00+08:00
weight = 44
type = "docs"
description = "Cow — Easy Rust 中文译本"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Easy Rust](https://dhghomon.github.io/easy_rust/)

> 原文链接: [https://dhghomon.github.io/easy_rust/Chapter_42.html](https://dhghomon.github.io/easy_rust/Chapter_42.html)

> 中文参考：[kumakichi/easy_rust_chs](https://kumakichi.github.io/easy_rust_chs/)

# Cow

Cow是一个非常方便的枚举。它的意思是 "写时克隆"，如果你不需要`String`，可以返回一个`&str`，如果你需要，可以返回一个`String`。(它也可以对数组与Vec等做同样的处理)。

为了理解它，我们看一下签名。它说

```rust
pub enum Cow<'a, B>
where
    B: 'a + ToOwned + ?Sized,
 {
    Borrowed(&'a B),
    Owned(<B as ToOwned>::Owned),
}

fn main() {}
```

你马上就知道，`'a`意味着它可以和引用一起工作。`ToOwned`的特性意味着它是一个可以变成拥有类型的类型。例如，`str`通常是一个引用(`&str`)，你可以把它变成一个拥有的`String`。

接下来是`?Sized`。这意味着 "也许是Sized，但也许不是"。Rust中几乎每个类型都是Sized的，但像`str`这样的类型却不是。这就是为什么我们需要一个 `&` 来代替 `str`，因为编译器不知道大小。所以，如果你想要一个可以使用 `str` 这样的trait，你可以添加 `?Sized.`

接下来是`enum`的变种。它们是 `Borrowed` 和 `Owned`。

想象一下，你有一个返回 `Cow<'static, str>` 的函数。如果你告诉函数返回`"My message".into()`，它就会查看类型:"My message"是`str`. 这是一个`Borrowed`的类型，所以它选择`Borrowed(&'a B)`。所以它就变成了`Cow::Borrowed(&'static str)`。

而如果你给它一个`format!("{}", "My message").into()`，那么它就会查看类型。这次是一个`String`，因为`format!`创建了`String`。所以这次会选择 "Owned"。

下面是一个测试`Cow`的例子。我们将把一个数字放入一个函数中，返回一个`Cow<'static, str>`。根据这个数字，它会创建一个`&str`或`String`。然后它使用`.into()`将其变成`Cow`。这样做的时候，它就会选择`Cow::Borrowed`或者`Cow::Owned`。那我们就匹配一下，看看它选的是哪一个。

```rust
use std::borrow::Cow;

fn modulo_3(input: u8) -> Cow<'static, str> {
    match input % 3 {
        0 => "Remainder is 0".into(),
        1 => "Remainder is 1".into(),
        remainder => format!("Remainder is {}", remainder).into(),
    }
}

fn main() {
    for number in 1..=6 {
        match modulo_3(number) {
            Cow::Borrowed(message) => println!("{} went in. The Cow is borrowed with this message: {}", number, message),
            Cow::Owned(message) => println!("{} went in. The Cow is owned with this message: {}", number, message),
        }
    }
}
```

这个打印:

```text
1 went in. The Cow is borrowed with this message: Remainder is 1
2 went in. The Cow is owned with this message: Remainder is 2
3 went in. The Cow is borrowed with this message: Remainder is 0
4 went in. The Cow is borrowed with this message: Remainder is 1
5 went in. The Cow is owned with this message: Remainder is 2
6 went in. The Cow is borrowed with this message: Remainder is 0
```

`Cow`还有一些其他的方法，比如`into_owned` 或者 `into_borrowed`，这样如果你需要的话，你可以改变它。
