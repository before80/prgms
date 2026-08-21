+++
title = "53-属性"
date = 2026-08-21T12:46:00+08:00
weight = 54
type = "docs"
description = "属性 — Easy Rust 中文译本"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Easy Rust](https://dhghomon.github.io/easy_rust/)

> 原文链接: [https://dhghomon.github.io/easy_rust/Chapter_52.html](https://dhghomon.github.io/easy_rust/Chapter_52.html)

> 中文参考：[kumakichi/easy_rust_chs](https://kumakichi.github.io/easy_rust_chs/)

# 属性

你以前见过`#[derive(Debug)]`这样的代码:这种类型的代码叫做*属性*。这些属性是给编译器提供信息的小段代码。它们不容易创建，但使用起来非常方便。如果你只用`#`写一个属性，那么它将影响下一行的代码。但如果你用`#!`来写，那么它将影响自己空间里的一切。

下面是一些你会经常看到的属性。

`#[allow(dead_code)]` 和 `#[allow(unused_variables)]`。 如果你写了不用的代码，Rust仍然会编译，但会让你知道。例如，这里有一个结构体，里面什么都没有，只有一个变量。我们不使用它们中的任何一个。

```rust
struct JustAStruct {}

fn main() {
    let some_char = 'ん';
}
```

如果你这样写，Rust会提醒你，你没有使用它们。

```text
warning: unused variable: `some_char`
 --> src\main.rs:4:9
  |
4 |     let some_char = 'ん';
  |         ^^^^^^^^^ help: if this is intentional, prefix it with an underscore: `_some_char`
  |
  = note: `#[warn(unused_variables)]` on by default

warning: struct is never constructed: `JustAStruct`
 --> src\main.rs:1:8
  |
1 | struct JustAStruct {}
  |        ^^^^^^^^^^^
  |
  = note: `#[warn(dead_code)]` on by default
```

我们知道，可以在名字前写一个`_`，让编译器安静下来。

```rust
struct _JustAStruct {}

fn main() {
    let _some_char = 'ん';
}
```

但你也可以使用属性。你会注意到在消息中，它使用了`#[warn(unused_variables)]`和`#[warn(dead_code)]`。在我们的代码中，`JustAStruct`是死代码，而`some_char`是一个未使用的变量。`warn`的反义词是`allow`，所以我们可以这样写，它不会说什么。

```rust
#![allow(dead_code)]
#![allow(unused_variables)]

struct Struct1 {} // 创建五个结构体
struct Struct2 {}
struct Struct3 {}
struct Struct4 {}
struct Struct5 {}

fn main() {
    let char1 = 'ん'; // 还有四个变量。一个都没用，但编译器不抱怨了
    let char2 = ';';
    let some_str = "I'm just a regular &str";
    let some_vec = vec!["I", "am", "just", "a", "vec"];
}
```

当然，处理死代码和未使用的变量是很重要的。但有时你希望编译器安静一段时间。或者您可能需要展示一些代码或教人们Rust，但又不想用编译器的信息来迷惑他们。

`#[derive(TraitName)]`让你可以为你创建的结构和枚举派生一些trait。这适用于许多可以自动派生的常见trait。有些像 `Display` 这样的特性不能自动衍生，因为对于 `Display`，你必须选择如何显示。

```rust
// ⚠️
#[derive(Display)]
struct HoldsAString {
    the_string: String,
}

fn main() {
    let my_string = HoldsAString {
        the_string: "Here I am!".to_string(),
    };
}
```

错误信息会告诉你:

```text
error: cannot find derive macro `Display` in this scope
 --> src\main.rs:2:10
  |
2 | #[derive(Display)]
  |
```

但是对于可以自动推导出的trait，你可以随心所欲的放进去。让我们给`HoldsAString`在一行中加入七个trait，只是为了好玩，尽管它只需要一个。

```rust
#[derive(Debug, PartialEq, Eq, Ord, PartialOrd, Hash, Clone)]
struct HoldsAString {
    the_string: String,
}

fn main() {
    let my_string = HoldsAString {
        the_string: "Here I am!".to_string(),
    };
    println!("{:?}", my_string);
}
```

另外，如果(也只有在)它的字段都实现了`Copy`的情况下，你才可以创建一个`Copy`结构。`HoldsAString`包含`String`，它没有实现`Copy`，所以你不能对它使用`#[derive(Copy)]`。但是对下面这个结构你可以:

```rust
#[derive(Clone, Copy)] // 要用 Copy，还需要 Clone
struct NumberAndBool {
    number: i32, // i32 是 Copy
    true_or_false: bool // bool 也是 Copy。没问题
}

fn does_nothing(input: NumberAndBool) {

}

fn main() {
    let number_and_bool = NumberAndBool {
        number: 8,
        true_or_false: true
    };

    does_nothing(number_and_bool);
    does_nothing(number_and_bool); // 如果没有 Copy，这里会报错
}
```


`#[cfg()]`的意思是配置，告诉编译器是否运行代码。它通常是这样的:`#[cfg(test)]`。你在写测试函数的时候用这个，这样它就知道除非你在测试，否则不要运行它们。那么你可以在你的代码附近写测试，但编译器不会运行它们，除非你告诉编译器。

还有一个使用`cfg`的例子是`#[cfg(target_os = "windows")]`。有了它，你可以告诉编译器只在Windows，Linux或其他平台则不能运行代码。

`#![no_std]`是一个有趣的属性，它告诉Rust不要引入标准库。这意味着你没有`Vec`，`String`，以及标准库中的其他任何东西。你会在那些没有多少内存或空间的小型设备的代码中看到这个。

你可以在[这里](https://doc.rust-lang.org/reference/attributes.html)看到更多的属性。
