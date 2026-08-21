+++
title = "63-cargo"
date = 2026-08-21T12:46:00+08:00
weight = 64
type = "docs"
description = "cargo — Easy Rust 中文译本"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Easy Rust](https://dhghomon.github.io/easy_rust/)

> 原文链接: [https://dhghomon.github.io/easy_rust/Chapter_62.html](https://dhghomon.github.io/easy_rust/Chapter_62.html)

> 中文参考：[kumakichi/easy_rust_chs](https://kumakichi.github.io/easy_rust_chs/)

# cargo

`rustc`的意思是Rust编译器，实际的编译工作由它完成。一个rust文件的结尾是`.rs`。但大多数人不会写出类似 `rustc main.rs` 的东西来编译。他们使用的是名为 `cargo` 的东西，它是 Rust 的主包管理器。

关于这个名字的一个说明: 之所以叫`cargo`，是因为当你把crate放在一起时，你会得到cargo。Crate就是你在船上或卡车上看到的木箱，但你记住，每个Rust项目也叫Crate。那么当你把它们放在一起时，你就会得到整个cargo。

当你使用cargo来运行一个项目时，你可以看到这一点。让我们用 `rand` 试试简单的东西:我们只是在八个字母之间随机选择。

```rust
use rand::seq::SliceRandom; // 用来对切片调用 .choose

fn main() {

    let my_letters = vec!['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'];

    let mut rng = rand::thread_rng();
    for _ in 0..6 {
        print!("{} ", my_letters.choose(&mut rng).unwrap());
    }
}
```

这样就会打印出`b c g h e a`这样的东西。但我们想先看看`cargo`的作用。要使用 `cargo` 并运行我们的程序，通常我们输入 `cargo run`。这样就可以构建我们的程序，并为我们运行它。当它开始编译的时候，会做这样的事情:

```text
   Compiling getrandom v0.1.14
   Compiling cfg-if v0.1.10
   Compiling ppv-lite86 v0.2.8
   Compiling rand_core v0.5.1
   Compiling rand_chacha v0.2.2
   Compiling rand v0.7.3
   Compiling rust_book v0.1.0 (C:\Users\mithr\OneDrive\Documents\Rust\rust_book)
    Finished dev [unoptimized + debuginfo] target(s) in 13.13s
     Running `C:\Users\mithr\OneDrive\Documents\Rust\rust_book\target\debug\rust_book.exe`
g f c f h b
```

所以看起来不只是引入了`rand`，还引入了一些其他的crate。这是因为我们的crate需要`rand`，但`rand`也有一些代码也需要其他crate。所以`cargo`会找到我们需要的所有crate，并把它们放在一起。在我们的案例中，只有7个，但在非常大的项目中，你可能会有200个或更多的crate要引入。

这就是你可以看到Rust的权衡的地方。Rust的速度非常快，因为它提前编译。它通过查看代码，看你写的代码到底做了什么。例如，你可能会写这样的泛型代码:

```rust
use std::fmt::Display;

fn print_and_return_thing<T: Display>(input: T) -> T {
    println!("You gave me {} and now I will give it back.", input);
    input
}

fn main() {
    let my_name = print_and_return_thing("Windy");
    let small_number = print_and_return_thing(9.0);
}
```

这个函数可以用任何实现了`Display`的作为参数，所以我们给它一个`&str`，接下来给它一个`f64`，这对我们来说是没有问题的。但是编译器不看泛型，因为它不想在运行时做任何事情。它想把一个能运行的程序尽可能快地组装起来。所以当它看第一部分的`"Windy"`时，它没有看到`fn print_and_return_thing<T: Display>(input: T) -> T`，它看到的是`fn print_and_return_thing(input: &str) -> &str`这样的东西。而接下来它看到的是`fn print_and_return_thing(input: f64) -> f64`。所有关于trait的检查等等都是在编译时完成的。这就是为什么泛型需要更长的时间来编译，因为它需要弄清楚它们，并使之具体化。

还有一点:Rust 2020正在努力处理编译时间问题，因为这部分需要的时间最长。每一个版本的Rust在编译时都会快一点，而且还有一些其他的计划来加快它的速度。但与此同时，以下是你应该知道的:

- `cargo build`会构建你的程序，这样你就可以运行它了。
- `cargo run`将建立你的程序并运行它。
- `cargo build --release`和`cargo run --release`发布模式下有同样的效果。什么是发布模式？当你的代码最终完成后就可以用发布模式了。Rust会花更多的时间来编译，但它这样做是因为它使用了它所知道的一切，来使编译出的程序运行更快。Release模式实际上比常规模式*快的多*，常规模式被称为debug模式。那是因为它的编译速度更快，而且有更多的调试信息。常规的`cargo build`叫做 "debug build"，`cargo build --release`叫做 "release build"。
- `cargo check`是一种检查代码的方式。它就像编译一样，只不过它不会真正地创建你的程序。这是一个很好的检查你的代码的方法，因为它不像`build`或`run`那样需要很长时间。

对了，命令中的`--release`部分叫做`flag`。这意味着命令中的额外信息。

其他一些你需要知道的事情是:

- `cargo new`. 这样做是为了创建一个新的Rust项目。`new`之后，写上项目的名称，`cargo`将会创建所有你需要的文件和文件夹。
- `cargo clean`. 当你把crate添加到`Cargo.toml`时，电脑会下载所有需要的文件，它们会占用很多空间。如果你不想再让它们在你的电脑上，输入`cargo clean`。

关于编译器还有一点:只有当你第一次使用`cargo build`或`cargo run`时，它才会花费最多的时间。之后它就会记住，它又会快速编译。但如果你使用 `cargo clean`，然后运行 `cargo build`，它将不得不再慢慢地编译一次。
