+++
title = "12-可变性"
date = 2026-08-21T12:46:00+08:00
weight = 13
type = "docs"
description = "可变性 — Easy Rust 中文译本"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Easy Rust](https://dhghomon.github.io/easy_rust/)

> 原文链接: [https://dhghomon.github.io/easy_rust/Chapter_11.html](https://dhghomon.github.io/easy_rust/Chapter_11.html)

> 中文参考：[kumakichi/easy_rust_chs](https://kumakichi.github.io/easy_rust_chs/)

# 可变性

当你用`let`声明一个变量时，它是不可改变的(不能改变)。

这将无法工作:

```rust
fn main() {
    let my_number = 8;
    my_number = 10; // ⚠️
}
```

编译器说:`error[E0384]: cannot assign twice to immutable variable my_number`。这是因为如果你只写`let`，变量是不可变的。

但有时你想改变你的变量。要创建一个可以改变的变量，就在`let`后面加上`mut`。

```rust
fn main() {
    let mut my_number = 8;
    my_number = 10;
}
```

现在没有问题了。

但是，你不能改变类型:甚至`mut`也不能让你这样做:这将无法工作。

```rust
fn main() {
    let mut my_variable = 8; // 现在它是 i32。类型不能改
    my_variable = "Hello, world!"; // ⚠️
}
```

你会看到编译器发出的同样的 "预期"信息。`expected integer, found &str`. `&str`是一个字符串类型，我们很快就会知道。

## 遮蔽

shadowing是指使用`let`声明一个与另一个变量同名的新变量。它看起来像可变性，但完全不同。shadowing看起来是这样的:

```rust
fn main() {
    let my_number = 8; // 这是 i32
    println!("{}", my_number); // 打印 8
    let my_number = 9.2; // 这是同名的 f64。但不是第一个 my_number——完全是另一个！
    println!("{}", my_number) // 打印 9.2
}
```

这里我们说我们用一个新的 "let绑定"对`my_number`进行了 "shadowing"。

那么第一个`my_number`是否被销毁了呢？没有，但是当我们调用`my_number`时，我们现在得到`my_number`的`f64`。因为它们在同一个作用域块中(同一个 `{}`)，我们不能再看到第一个 `my_number`。

但如果它们在不同的块中，我们可以同时看到两个。
 例如:

```rust
fn main() {
    let my_number = 8; // 这是 i32
    println!("{}", my_number); // 打印 8
    {
        let my_number = 9.2; // 这是 f64。不是原来的 my_number——完全是另一个！
        println!("{}", my_number) // 打印 9.2
                                  // 但被遮蔽的 my_number 只活到这里。
                                  // 第一个 my_number 还活着！
    }
    println!("{}", my_number); // 打印 8
}
```

因此，当你对一个变量进行shadowing处理时，你不会破坏它。你**屏蔽**了它。

那么shadowing的好处是什么呢？当你需要经常改变一个变量的时候，shadowing是很好的。想象一下，你想用一个变量做很多简单的数学运算。

```rust
fn times_two(number: i32) -> i32 {
    number * 2
}

fn main() {
    let final_number = {
        let y = 10;
        let x = 9; // x 从 9 开始
        let x = times_two(x); // 用新的 x 遮蔽：18
        let x = x + y; // 再用新的 x 遮蔽：28
        x // 返回 x：final_number 现在是 x 的值
    };
    println!("The number is now: {}", final_number)
}
```

如果没有shadowing，你将不得不考虑不同的名称，尽管你并不关心x。

```rust
fn times_two(number: i32) -> i32 {
    number * 2
}

fn main() {
    // 假装我们在用不支持遮蔽的 Rust
    let final_number = {
        let y = 10;
        let x = 9; // x 从 9 开始
        let x_twice = times_two(x); // x 的第二个名字
        let x_twice_and_y = x_twice + y; // x 的第三个名字！
        x_twice_and_y // 可惜没有遮蔽——不然直接用 x 就行
    };
    println!("The number is now: {}", final_number)
}
```

一般来说，你在Rust中看到的shadowing就是这种情况。它发生在你想快速取用变量，对它做一些事情，然后再做其他事情的地方。而你通常将它用于那些你不太关心的快速变量。
