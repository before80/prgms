+++
title = "5.2 结构体示例程序"
date = 2026-08-05T08:44:00+08:00
weight = 21
type = "docs"
description = "结构体示例程序：用矩形面积示例从变量重构到结构体与 Debug"
isCJKLanguage = true
draft = false
rust_version = "1.97.1"

+++

> 译文 · 基于 [The Rust Programming Language](https://doc.rust-lang.org/stable/book/)（rustc 1.97.1）

# 结构体示例程序


> 原文链接: [https://doc.rust-lang.org/stable/book/ch05-02-example-structs.html](https://doc.rust-lang.org/stable/book/ch05-02-example-structs.html)


## 使用结构体的示例程序

　　为理解何时可能想用结构体，我们来写一个计算矩形面积的程序。先从单独的变量开始，再逐步重构，直到改用结构体。

　　用 Cargo 新建一个名为 *rectangles* 的二进制项目：它接收以像素为单位指定的矩形宽和高，并计算面积。示例 5-8 展示了在项目的 *src/main.rs* 中实现这一点的一种简短写法。

**文件名：`src/main.rs`**
```rust
fn main() {
    let width1 = 30;
    let height1 = 50;

    println!(
        "The area of the rectangle is {} square pixels.",
        area(width1, height1)
    );
}

fn area(width: u32, height: u32) -> u32 {
    width * height
}
```

**示例 5-8：用各自独立的宽、高变量计算矩形面积**

　　现在用 `cargo run` 运行该程序：

```console
$ cargo run
   Compiling rectangles v0.1.0 (file:///projects/rectangles)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.42s
     Running `target/debug/rectangles`
The area of the rectangle is 1500 square pixels.
```

　　这段代码通过把各个维度传给 `area` 函数，成功算出了矩形面积，但我们还能让代码更清晰、更易读。

　　问题在 `area` 的签名里一目了然：

```rust
fn area(width: u32, height: u32) -> u32 {
```

　　`area` 本应计算*一个*矩形的面积，但我们写的函数有两个参数，程序里也看不出这两个参数彼此相关。把宽和高组合在一起会更易读、更好管理。第 3 章[「元组类型」](../../common-programming-concepts/02-data-types/)一节已经讨论过一种做法：使用元组。

### 用元组重构

　　示例 5-9 展示使用元组的另一版程序。

**文件名：`src/main.rs`**
```rust
fn main() {
    let rect1 = (30, 50);

    println!(
        "The area of the rectangle is {} square pixels.",
        area(rect1)
    );
}

fn area(dimensions: (u32, u32)) -> u32 {
    dimensions.0 * dimensions.1
}
```

**示例 5-9：用元组指定矩形的宽和高**

　　一方面，这个程序更好了：元组带来一点结构，现在只需传一个参数。另一方面，这版又没那么清晰：元组不为元素命名，我们只能用索引取各部分，计算意图也就不那么明显。

　　对面积计算来说，弄混宽和高无关紧要；但若要在屏幕上绘制矩形，就很要紧！我们必须记住 `width` 是元组索引 `0`，`height` 是索引 `1`。别人使用我们的代码时更难弄清并记住这一点。因为没有在代码中传达数据的含义，现在更容易引入错误。

### 用结构体重构

　　我们用结构体给数据的各个部分命名，从而赋予它们明确含义。可以把正在使用的元组改写成结构体：既为整体命名，也为各字段命名，如示例 5-10 所示。

**文件名：`src/main.rs`**
```rust
struct Rectangle {
    width: u32,
    height: u32,
}

fn main() {
    let rect1 = Rectangle {
        width: 30,
        height: 50,
    };

    println!(
        "The area of the rectangle is {} square pixels.",
        area(&rect1)
    );
}

fn area(rectangle: &Rectangle) -> u32 {
    rectangle.width * rectangle.height
}
```

**示例 5-10：定义 `Rectangle` 结构体**

　　这里我们定义了名为 `Rectangle` 的结构体。在花括号内定义字段 `width` 和 `height`，类型都是 `u32`。然后在 `main` 中创建了一个具体的 `Rectangle` 实例，宽为 `30`，高为 `50`。

　　现在的 `area` 函数只有一个参数，我们命名为 `rectangle`，类型是对 `Rectangle` 结构体实例的不可变借用。如第 4 章所述，我们想借用结构体而不是取得其所有权。这样 `main` 仍保留所有权，可以继续使用 `rect1`——这也是函数签名和调用处使用 `&` 的原因。

　　`area` 函数访问 `Rectangle` 实例的 `width` 和 `height` 字段（注意：访问借用结构体实例的字段不会移动字段值，因此你常会看到对结构体的借用）。现在 `area` 的函数签名准确表达了我们的意图：用其 `width` 和 `height` 字段计算 `Rectangle` 的面积。这既说明宽和高彼此相关，又给这些值起了描述性名字，而不是使用元组索引 `0` 和 `1`。可读性明显更好。

### 用派生特征增加功能

　　调试程序时，若能打印 `Rectangle` 实例并看到所有字段的值会很有用。示例 5-11 尝试像前几章那样使用 [`println!` 宏][println]。然而这行不通。

**文件名：`src/main.rs`**
```rust
struct Rectangle {
    width: u32,
    height: u32,
}

fn main() {
    let rect1 = Rectangle {
        width: 30,
        height: 50,
    };

    println!("rect1 is {rect1}");
}
```

**示例 5-11：尝试打印 `Rectangle` 实例**

　　编译这段代码时，会得到核心信息如下的错误：

```text
$ cargo run
   Compiling rectangles v0.1.0 (file:///projects/rectangles)
error[E0277]: `Rectangle` doesn't implement `std::fmt::Display`
  --> src/main.rs:12:24
   |
12 |     println!("rect1 is {rect1}");
   |                        ^^^^^^^ `Rectangle` cannot be formatted with the default formatter
   |
help: the trait `std::fmt::Display` is not implemented for `Rectangle`
  --> src/main.rs:1:1
   |
 1 | struct Rectangle {
   | ^^^^^^^^^^^^^^^^
   = note: in format strings you may be able to use `{:?}` (or {:#?} for pretty-print) instead

For more information about this error, try `rustc --explain E0277`.
error: could not compile `rectangles` (bin "rectangles") due to 1 previous error
```

　　`println!` 宏可以做多种格式化；默认情况下，花括号告诉 `println!` 使用名为 `Display` 的格式：面向最终用户直接阅读的输出。我们目前见过的基本类型默认实现了 `Display`，因为展示 `1` 或其他基本类型给用户通常只有一种合理方式。但对结构体来说，`println!` 应如何格式化输出就不那么明确了——显示可能性更多：要不要逗号？要不要打印花括号？是否显示所有字段？由于存在这种歧义，Rust 不会猜测我们想要什么，结构体也就没有提供可与 `println!` 和 `{}` 占位符一起使用的 `Display` 实现。

　　若继续读错误信息，会看到这条有用的说明：

```text
help: the trait `std::fmt::Display` is not implemented for `Rectangle`
  --> src/main.rs:1:1
```

　　试试看！现在的 `println!` 宏调用会像 `println!("rect1 is {rect1:?}");`。在花括号内放入说明符 `:?`，就告诉 `println!` 我们想使用名为 `Debug` 的输出格式。`Debug` 特征让我们能以对开发者有用的方式打印结构体，从而在调试时看到其值。

　　带着这一改动再编译。糟糕！仍然报错：

```text
$ cargo run
   Compiling rectangles v0.1.0 (file:///projects/rectangles)
error[E0277]: `Rectangle` doesn't implement `Debug`
  --> src/main.rs:12:31
   |
12 |     println!("rect1 is {:?}", rect1);
   |                        ----   ^^^^^ `Rectangle` cannot be formatted using `{:?}` because it doesn't implement `Debug`
   |                        |
   |                        required by this formatting parameter
   |
   = help: the trait `Debug` is not implemented for `Rectangle`
   = note: add `#[derive(Debug)]` to `Rectangle` or manually `impl Debug for Rectangle`
help: consider annotating `Rectangle` with `#[derive(Debug)]`
   |
 1 + #[derive(Debug)]
 2 | struct Rectangle {
   |

For more information about this error, try `rustc --explain E0277`.
error: could not compile `rectangles` (bin "rectangles") due to 1 previous error
```

　　不过编译器再次给出了有用的说明：

```text
   |                        required by this formatting parameter
   |
```

　　Rust *确实*包含打印调试信息的功能，但我们必须显式选择启用，才能让结构体使用它。做法是在结构体定义正上方添加外部属性 `#[derive(Debug)]`，如示例 5-12 所示。

**文件名：`src/main.rs`**
```rust
#[derive(Debug)]
struct Rectangle {
    width: u32,
    height: u32,
}

fn main() {
    let rect1 = Rectangle {
        width: 30,
        height: 50,
    };

    println!("rect1 is {rect1:?}");
}
```

**示例 5-12：添加派生 `Debug` 特征的属性，并用调试格式打印 `Rectangle` 实例**

　　现在运行程序不会再有错误，会看到如下输出：

```console
$ cargo run
   Compiling rectangles v0.1.0 (file:///projects/rectangles)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.48s
     Running `target/debug/rectangles`
rect1 is Rectangle { width: 30, height: 50 }
```

　　不错！输出格式并不美观，但显示了该实例所有字段的值，调试时绝对有帮助。结构体更大时，更易读的输出会很有用；这时可以在 `println!` 字符串里用 `{:#?}` 代替 `{:?}`。本例中使用 `{:#?}` 风格会输出如下：

```console
$ cargo run
   Compiling rectangles v0.1.0 (file:///projects/rectangles)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.48s
     Running `target/debug/rectangles`
rect1 is Rectangle {
    width: 30,
    height: 50,
}
```

　　另一种用 `Debug` 格式打印值的方式是使用 [`dbg!` 宏][dbg]：它取得表达式的所有权（而 `println!` 取得引用），打印出该 `dbg!` 宏调用在代码中的文件与行号以及该表达式的结果值，然后归还该值的所有权。

> 注意：调用 `dbg!` 宏会打印到标准错误控制台流（`stderr`），而 `println!` 打印到标准输出控制台流（`stdout`）。关于 `stderr` 和 `stdout`，我们会在[第 12 章「把错误重定向到标准错误」一节][err]再谈。

　　下面的例子中，我们既关心赋给 `width` 字段的值，也关心整个结构体 `rect1` 的值：

```rust
#[derive(Debug)]
struct Rectangle {
    width: u32,
    height: u32,
}

fn main() {
    let scale = 2;
    let rect1 = Rectangle {
        width: dbg!(30 * scale),
        height: 50,
    };

    dbg!(&rect1);
}
```

　　可以把 `dbg!` 包在表达式 `30 * scale` 外面；因为 `dbg!` 会归还表达式值的所有权，`width` 字段得到的值与没有 `dbg!` 时相同。我们不希望 `dbg!` 取得 `rect1` 的所有权，因此下一次调用传入对 `rect1` 的引用。该示例的输出如下：

```console
$ cargo run
   Compiling rectangles v0.1.0 (file:///projects/rectangles)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.61s
     Running `target/debug/rectangles`
[src/main.rs:10:16] 30 * scale = 60
[src/main.rs:14:5] &rect1 = Rectangle {
    width: 60,
    height: 50,
}
```

　　可以看到，第一段输出出自 *src/main.rs* 第 10 行，我们在调试表达式 `30 * scale`，结果值为 `60`（整数实现的 `Debug` 格式化就是只打印其值）。*src/main.rs* 第 14 行的 `dbg!` 调用输出 `&rect1` 的值，也就是 `Rectangle` 结构体。该输出使用了 `Rectangle` 类型更易读的 `Debug` 格式。当你想弄清代码在做什么时，`dbg!` 宏会非常有用！

　　除了 `Debug` 特征，Rust 还提供了许多可与 `derive` 属性一起使用的特征，能为自定义类型添加有用行为。这些特征及其行为列在[附录 C][app-c]中。如何用自定义行为实现这些特征，以及如何创建自己的特征，会在第 10 章介绍。除了 `derive` 还有许多其他属性；更多信息见 [《Rust 参考手册》的「属性（Attributes）」一节][attributes]。

　　我们的 `area` 函数非常具体：它只计算矩形的面积。把这种行为与 `Rectangle` 结构体更紧密地绑定会很有帮助，因为它对其他类型并不适用。接下来看看如何继续重构这段代码：把 `area` 函数变成定义在 `Rectangle` 类型上的 `area` 方法。

[the-tuple-type]: ../../common-programming-concepts/02-data-types/
[app-c]: ../../appendix/03-c-derivable-traits/
[println]: https://doc.rust-lang.org/std/macro.println.html
[dbg]: https://doc.rust-lang.org/std/macro.dbg.html
[err]: ../../an-io-project/06-writing-to-stderr-instead-of-stdout/
[attributes]: https://doc.rust-lang.org/reference/attributes.html
