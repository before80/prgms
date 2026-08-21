+++
title = "09-类型推导"
date = 2026-08-21T12:46:00+08:00
weight = 10
type = "docs"
description = "类型推导 — Easy Rust 中文译本"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Easy Rust](https://dhghomon.github.io/easy_rust/)

> 原文链接: [https://dhghomon.github.io/easy_rust/Chapter_8.html](https://dhghomon.github.io/easy_rust/Chapter_8.html)

> 中文参考：[kumakichi/easy_rust_chs](https://kumakichi.github.io/easy_rust_chs/)

# 类型推导

类型推导的意思是，如果你不告诉编译器类型，但它可以自己决定，它就会决定。编译器总是需要知道变量的类型，但你并不总是需要告诉它。实际上，通常你不需要告诉它。例如，对于`let my_number = 8`，`my_number`将是一个`i32`。这是因为如果你不告诉它，编译器会选择i32作为整数。但是如果你说`let my_number: u8 = 8`，它就会把`my_number`变成`u8`，因为你告诉它`u8`。

通常编译器都能猜到。但有时你需要告诉它，原因有两个。

1) 你正在做一些非常复杂的事情，而编译器不知道你想要的类型。
2) 你想要一个不同的类型(例如，你想要一个`i128`，而不是`i32`)。

要指定一个类型，请在变量名后添加一个冒号。

```rust
fn main() {
    let small_number: u8 = 10;
}
```

对于数字，你可以在数字后面加上类型。你不需要空格--只需要在数字后面直接输入。

```rust
fn main() {
    let small_number = 10u8; // 10u8 = 类型为 u8 的 10
}
```

如果你想让数字便于阅读，也可以加上`_`。

```rust
fn main() {
    let small_number = 10_u8; // 这样更好读
    let big_number = 100_000_000_i32; // 一亿用 _ 分隔更好读
}
```

`_`不会改变数字。它只是为了让你方便阅读。而且你用多少个`_`都没有关系。

```rust
fn main() {
    let number = 0________u8;
    let number2 = 1___6______2____4______i32;
    println!("{}, {}", number, number2);
}
```

这样打印出的是`0, 1624`。

## 浮点数

浮点数是带有小数点的数字。5.5是一个浮点数，6是一个整数。5.0也是一个浮点数，甚至5.也是一个浮点数。

```rust
fn main() {
    let my_float = 5.; // Rust 看到 . 就知道这是浮点数
}
```

但类型不叫`float`，叫`f32`和`f64`。这和整数一样:`f`后面的数字显示的是位数。如果你不写类型，Rust会选择`f64`。

当然，只有同一类型的浮点数可以一起使用。所以你不能把`f32`加到`f64`上。

```rust
fn main() {
    let my_float: f64 = 5.0; // 这是 f64
    let my_other_float: f32 = 8.5; // 这是 f32

    let third_float = my_float + my_other_float; // ⚠️
}
```

当你尝试运行这个时，Rust会说。

```text
error[E0308]: mismatched types
 --> src\main.rs:5:34
  |
5 |     let third_float = my_float + my_other_float;
  |                                  ^^^^^^^^^^^^^^ expected `f64`, found `f32`
```

当你使用错误的类型时，编译器会写 "expected (type), found (type)"。它这样读取你的代码。

```rust
fn main() {
    let my_float: f64 = 5.0; // 编译器看到的是 f64
    let my_other_float: f32 = 8.5; // 编译器看到的是 f32。类型不同。
    let third_float = my_float + // 你想把 my_float 和某个东西相加，所以必须是 f64 加另一个 f64。现在它期望 f64……
    let third_float = my_float + my_other_float;  // ⚠️ 但它找到的是 f32。无法相加。
}
```

所以，当你看到 "expected(type)，found(type)"时，你必须找到为什么编译器预期的是不同的类型。

当然，用简单的数字很容易解决。你可以用`as`把`f32`转成`f64`。

```rust
fn main() {
    let my_float: f64 = 5.0;
    let my_other_float: f32 = 8.5;

    let third_float = my_float + my_other_float as f64; // my_other_float as f64 = 把 my_other_float 当作 f64 用
}
```

或者更简单，去掉类型声明。("声明一个类型"="告诉Rust使用该类型")Rust会选择可以加在一起的类型。

```rust
fn main() {
    let my_float = 5.0; // Rust 会选 f64
    let my_other_float = 8.5; // 这里同样会选 f64

    let third_float = my_float + my_other_float;
}
```

Rust编译器很聪明，如果你需要f32，就不会选择f64。

```rust
fn main() {
    let my_float: f32 = 5.0;
    let my_other_float = 8.5; // 通常 Rust 会选 f64，

    let third_float = my_float + my_other_float; // 但现在它知道你要加到 f32 上，所以 my_other_float 也选成 f32
}
```
