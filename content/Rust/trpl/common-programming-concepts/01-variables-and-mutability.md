+++
title = "3.1 变量与可变性"
date = 2026-08-05T08:44:00+08:00
weight = 10
type = "docs"
description = "不可变变量、mut、常量与遮蔽"
isCJKLanguage = true
draft = false
rust_version = "1.97.1"

+++

> 译文 · 基于 [The Rust Programming Language](https://doc.rust-lang.org/stable/book/)（rustc 1.97.1）

# 变量与可变性 {#variables-and-mutability}


> 原文链接: [https://doc.rust-lang.org/stable/book/ch03-01-variables-and-mutability.html](https://doc.rust-lang.org/stable/book/ch03-01-variables-and-mutability.html)


## 变量与可变性 {#variables-and-mutability-heading}

　　正如[「用变量存储值」][storing-values-with-variables]一节所述，变量默认是不可变的。这是 Rust 给你的众多引导之一，促使你以能发挥 Rust 安全性与轻松并发优势的方式编写代码。不过，你仍然可以让变量可变。让我们探讨 Rust 为何鼓励你偏爱不可变性，以及有时为何又想要可变性。

　　当变量不可变时，一旦把值绑定到某个名字，就不能再改变那个值。为说明这一点，请在 *projects* 目录中用 `cargo new variables` 生成一个名为 *variables* 的新项目。

　　然后在新的 *variables* 目录中打开 *src/main.rs*，将其代码替换为下面这段目前尚不能编译的代码：

<span class="filename">文件名：src/main.rs</span>

```rust
fn main() {
    let x = 5;
    println!("The value of x is: {x}");
    x = 6;
    println!("The value of x is: {x}");
}
```

　　保存并用 `cargo run` 运行程序。你应会收到关于不可变性错误的错误信息，如下所示：

```console
$ cargo run
   Compiling variables v0.1.0 (file:///projects/variables)
error[E0384]: cannot assign twice to immutable variable `x`
 --> src/main.rs:4:5
  |
2 |     let x = 5;
  |         - first assignment to `x`
3 |     println!("The value of x is: {x}");
4 |     x = 6;
  |     ^^^^^ cannot assign twice to immutable variable
  |
help: consider making this binding mutable
  |
2 |     let mut x = 5;
  |         +++

For more information about this error, try `rustc --explain E0384`.
error: could not compile `variables` (bin "variables") due to 1 previous error
```

　　这个例子展示了编译器如何帮助你发现程序中的错误。编译错误可能令人沮丧，但它们其实只意味着你的程序还没有安全地做你想做的事；它们*并不*意味着你不是一名好程序员！经验丰富的 Rustacean 仍会碰到编译错误。

　　你收到错误信息 `` cannot assign twice to immutable variable `x` ``，是因为你试图给不可变变量 `x` 赋第二次值。

　　当我们试图改变被指定为不可变的值时，在编译期得到错误非常重要，因为这种情况很容易导致 bug。若代码的一部分假定某个值永远不会改变，而另一部分却改变了它，第一部分就可能无法按设计运行。这类 bug 事后往往很难追踪，尤其是当第二段代码只是*有时*才改变该值时。Rust 编译器保证：当你声明某个值不会改变时，它就真的不会改变，因此你不必自己去追踪。这样你的代码也更容易推理。

　　但可变性可能非常有用，也能让代码写起来更方便。尽管变量默认不可变，你可以像在[第 2 章][storing-values-with-variables]那样，在变量名前加上 `mut` 来使其可变。加上 `mut` 也向未来的代码阅读者传达了意图：代码的其他部分会改变这个变量的值。

　　例如，把 *src/main.rs* 改成下面这样：

<span class="filename">文件名：src/main.rs</span>

```rust
fn main() {
    let mut x = 5;
    println!("The value of x is: {x}");
    x = 6;
    println!("The value of x is: {x}");
}
```

　　现在运行程序，会得到：

```console
$ cargo run
   Compiling variables v0.1.0 (file:///projects/variables)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.30s
     Running `target/debug/variables`
The value of x is: 5
The value of x is: 6
```

　　使用 `mut` 时，我们被允许把绑定到 `x` 的值从 `5` 改成 `6`。最终，是否使用可变性取决于你，也取决于你认为在那种具体情况下怎样最清晰。

### 声明常量 {#declaring-constants}

　　与不可变变量类似，*常量*（constants）也是绑定到名字且不允许改变的值，但常量与变量有几处不同。

　　首先，常量不允许使用 `mut`。常量不只是默认不可变——它们始终不可变。你用 `const` 关键字而不是 `let` 关键字声明常量，并且*必须*标注值的类型。我们会在下一节[「数据类型」][data-types]讨论类型与类型标注，现在不必担心细节。只需知道你必须始终标注类型。

　　常量可以在任何作用域中声明，包括全局作用域，因此很适合那些代码多处都需要知道的值。

　　最后一点不同是：常量只能设置为常量表达式，而不能是只能在运行时才能算出的值的结果。

　　下面是一个常量声明的例子：

```rust
const THREE_HOURS_IN_SECONDS: u32 = 60 * 60 * 3;
```

　　该常量名为 `THREE_HOURS_IN_SECONDS`，其值设为：60（一分钟的秒数）乘以 60（一小时的分钟数）再乘以 3（本程序要计时的小时数）。Rust 的常量命名约定是全部大写，单词之间用下划线分隔。编译器能在编译期求值一组有限的运算，这让我们可以选择以更易理解、更易核对的方式写出这个值，而不是把常量直接设为 10800。关于声明常量时可以使用哪些运算，见 [Rust Reference 中关于常量求值的章节][const-eval]。

　　在声明它们的作用域内，常量在程序整个运行期间都有效。这一性质使常量很适合应用领域中程序多处可能需要知道的值，例如游戏中任何玩家允许获得的最大分数，或光速。

　　把程序中到处使用的硬编码值命名为常量，有助于向未来的维护者传达该值的含义。若将来需要更新这个硬编码值，也只需改代码中的一处。

### 遮蔽 {#shadowing}

　　正如你在[第 2 章][comparing-the-guess-to-the-secret-number]猜数字游戏教程中所见，你可以声明一个与先前变量同名的新变量。Rustacean 会说第一个变量被第二个*遮蔽*（shadowed）了，意味着当你使用该变量名时，编译器看到的是第二个变量。实际上，第二个变量盖过了第一个，把对该名字的使用都转到自己身上，直到它自己也被遮蔽，或作用域结束。我们可以通过使用相同的变量名并再次使用 `let` 关键字来遮蔽变量，如下所示：

<span class="filename">文件名：src/main.rs</span>

```rust
fn main() {
    let x = 5;

    let x = x + 1;

    {
        let x = x * 2;
        println!("The value of x in the inner scope is: {x}");
    }

    println!("The value of x is: {x}");
}
```

　　这个程序首先把 `x` 绑定为 `5`。然后通过再次写 `let x =` 创建新变量 `x`，取原值并加 `1`，使 `x` 的值为 `6`。接着，在用花括号创建的内部作用域中，第三条 `let` 语句也遮蔽了 `x` 并创建新变量，把先前的值乘以 `2`，使 `x` 的值为 `12`。当该作用域结束时，内部的遮蔽结束，`x` 又变回 `6`。运行这个程序会输出：

```console
$ cargo run
   Compiling variables v0.1.0 (file:///projects/variables)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.31s
     Running `target/debug/variables`
The value of x in the inner scope is: 12
The value of x is: 6
```

　　遮蔽与把变量标记为 `mut` 不同，因为若我们不小心在没有使用 `let` 关键字的情况下重新赋值，会得到编译期错误。通过使用 `let`，我们可以对一个值做几次变换，而在这些变换完成后变量仍然是不可变的。

　　`mut` 与遮蔽的另一点不同是：再次使用 `let` 关键字时，我们实际上是在创建新变量，因此可以改变值的类型却复用同一个名字。例如，假设程序请用户输入空格字符来表示希望文本之间有多少空格，然后我们想把该输入存成数字：

```rust
    let spaces = "   ";
    let spaces = spaces.len();
```

　　第一个 `spaces` 变量是字符串类型，第二个 `spaces` 变量是数字类型。遮蔽因此让我们不必想出不同的名字，例如 `spaces_str` 和 `spaces_num`；相反，我们可以复用更简单的 `spaces` 名字。然而，若试图为此使用 `mut`，如下所示，会得到编译期错误：

```rust
    let mut spaces = "   ";
    spaces = spaces.len();
```

　　错误指出我们不允许改变变量的类型：

```console
$ cargo run
   Compiling variables v0.1.0 (file:///projects/variables)
error[E0308]: mismatched types
 --> src/main.rs:3:14
  |
2 |     let mut spaces = "   ";
  |                      ----- expected due to this value
3 |     spaces = spaces.len();
  |              ^^^^^^^^^^^^ expected `&str`, found `usize`

For more information about this error, try `rustc --explain E0308`.
error: could not compile `variables` (bin "variables") due to 1 previous error
```

　　既然我们已经探讨了变量如何工作，接下来看看它们可以拥有的更多数据类型。

[comparing-the-guess-to-the-secret-number]: ../../guessing-game/#comparing-the-guess-to-the-secret-number
[data-types]: ../02-data-types/#data-types
[storing-values-with-variables]: ../../guessing-game/#storing-values-with-variables
[const-eval]: https://doc.rust-lang.org/reference/const_eval.html
