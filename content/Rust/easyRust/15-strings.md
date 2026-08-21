+++
title = "15-字符串"
date = 2026-08-21T12:46:00+08:00
weight = 16
type = "docs"
description = "字符串 — Easy Rust 中文译本"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Easy Rust](https://dhghomon.github.io/easy_rust/)

> 原文链接: [https://dhghomon.github.io/easy_rust/Chapter_14.html](https://dhghomon.github.io/easy_rust/Chapter_14.html)

> 中文参考：[kumakichi/easy_rust_chs](https://kumakichi.github.io/easy_rust_chs/)

# 字符串

Rust有两种主要类型的字符串。`String`和`&str`. 有什么区别呢？

- `&str`是一个简单的字符串。当你写`let my_variable = "Hello, world!"`时，你会创建一个`&str`。`&str`是非常快的。
- `String`是一个更复杂的字符串。它比较慢，但它有更多的功能。`String`是一个指针，数据在堆上。

另外注意，`&str`前面有`&`，因为你需要一个引用来使用`str`。这是因为我们上面看到的原因:堆需要知道大小。所以我们给它一个`&`，它知道大小，然后它就高兴了。另外，因为你用一个`&`与一个`str`交互，你并不拥有它。但是一个`String`是一个*拥有*的类型。我们很快就会知道为什么这一点很重要。

`&str`和`String`都是UTF-8。例如，你可以写

```rust
fn main() {
    let name = "서태지"; // 这是韩文名字。没问题，因为 &str 是 UTF-8。
    let other_name = String::from("Adrian Fahrenheit Țepeș"); // Ț 和 ș 在 UTF-8 里也没问题。
}
```

你可以在`String::from("Adrian Fahrenheit Țepeș")`中看到，很容易从`&str`中创建一个`String`。这两种类型虽然不同，但联系非常紧密。

你甚至可以写表情符号，这要感谢UTF-8。

```rust
fn main() {
    let name = "😂";
    println!("My name is actually {}", name);
}
```

在你的电脑上，会打印`My name is actually 😂`，除非你的命令行不能打印。那么它会显示`My name is actually �`。但Rust对emojis或其他Unicode没有问题。

我们再来看看`str`使用`&`的原因，以确保我们理解。

- `str`是一个动态大小的类型(动态大小=大小可以不同)。比如 "서태지"和 "Adrian Fahrenheit Țepeș"这两个名字的大小是不一样的。

```rust
fn main() {

    println!("A String is always {:?} bytes. It is Sized.", std::mem::size_of::<String>()); // std::mem::size_of::<Type>() 给出某类型的字节大小
    println!("And an i8 is always {:?} bytes. It is Sized.", std::mem::size_of::<i8>());
    println!("And an f64 is always {:?} bytes. It is Sized.", std::mem::size_of::<f64>());
    println!("But a &str? It can be anything. '서태지' is {:?} bytes. It is not Sized.", std::mem::size_of_val("서태지")); // std::mem::size_of_val() 给出某变量的字节大小
    println!("And 'Adrian Fahrenheit Țepeș' is {:?} bytes. It is not Sized.", std::mem::size_of_val("Adrian Fahrenheit Țepeș"));
}
```

这个打印:

```text
A String is always 24 bytes. It is Sized.
And an i8 is always 1 bytes. It is Sized.
And an f64 is always 8 bytes. It is Sized.
But a &str? It can be anything. '서태지' is 9 bytes. It is not Sized.
And 'Adrian Fahrenheit Țepeș' is 25 bytes. It is not Sized.
```

这就是为什么我们需要一个 &，因为 `&` 是一个指针，而 Rust 知道指针的大小。所以指针会放在栈中。如果我们写`str`，Rust就不知道该怎么做了，因为它不知道指针的大小。



有很多方法可以创建`String`。下面是一些。

- `String::from("This is the string text");` 这是String的一个方法，它接受文本并创建一个String.
- `"This is the string text".to_string()`. 这是&str的一个方法，使其成为一个String。
- `format!` 宏。
 这和`println!`一样，只是它创建了一个字符串，而不是打印。所以你可以这样做:

```rust
fn main() {
    let my_name = "Billybrobby";
    let my_country = "USA";
    let my_home = "Korea";

    let together = format!(
        "I am {} and I come from {} but I live in {}.",
        my_name, my_country, my_home
    );
}
```

现在我们有了一个一起命名的字符串，但还没有打印出来。

还有一种创建String的方法叫做`.into()`，但它有点不同，因为`.into()`并不只是用来创建`String`。有些类型可以很容易地使用`From`和`.into()`转换为另一种类型，并从另一种类型转换出来。而如果你有`From`，那么你也有`.into()`。`From` 更加清晰，因为你已经知道了类型:你知道 `String::from("Some str")` 是一个来自 `&str` 的 `String`。但是对于`.into()`，有时候编译器并不知道。

```rust
fn main() {
    let my_string = "Try to make this a String".into(); // ⚠️
}
```

Rust不知道你要的是什么类型，因为很多类型都可以从一个`&str`创建出来。它说:"我可以把一个&str做成很多东西。你想要哪一种？"

```text
error[E0282]: type annotations needed
 --> src\main.rs:2:9
  |
2 |     let my_string = "Try to make this a String".into();
  |         ^^^^^^^^^ consider giving `my_string` a type
```

所以你可以这样做:

```rust
fn main() {
    let my_string: String = "Try to make this a String".into();
}
```

现在你得到了一个字符串。
