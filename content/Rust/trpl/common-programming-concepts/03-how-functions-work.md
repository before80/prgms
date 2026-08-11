+++
title = "3.3 函数"
date = 2026-08-05T08:44:00+08:00
weight = 12
type = "docs"
description = "函数定义、参数、语句与表达式、返回值"
isCJKLanguage = true
draft = false
rust_version = "1.97.1"

+++

> 译文 · 基于 [The Rust Programming Language](https://doc.rust-lang.org/stable/book/)（rustc 1.97.1）

# 函数 {#functions}


> 原文链接: [https://doc.rust-lang.org/stable/book/ch03-03-how-functions-work.html](https://doc.rust-lang.org/stable/book/ch03-03-how-functions-work.html)


## 函数 {#functions-heading}

　　函数在 Rust 代码中无处不在。你已经见过语言中最重要的函数之一：`main` 函数，它是许多程序的入口点。你也见过 `fn` 关键字，它允许你声明新函数。

　　Rust 代码对函数名和变量名使用*蛇形命名法*（snake case）作为惯例风格：所有字母小写，单词之间用下划线分隔。下面的程序包含一个示例函数定义：

<span class="filename">文件名：src/main.rs</span>

```rust
fn main() {
    println!("Hello, world!");

    another_function();
}

fn another_function() {
    println!("Another function.");
}
```

　　在 Rust 中，我们通过输入 `fn`、后跟函数名和一对圆括号来定义函数。花括号告诉编译器函数体从哪里开始、到哪里结束。

　　我们可以通过输入已定义函数的名字并后跟一对圆括号来调用它。因为程序中定义了 `another_function`，所以可以从 `main` 函数内部调用它。注意我们在源码中把 `another_function` 定义在了 `main` 函数*之后*；也可以定义在之前。Rust 不关心你在哪里定义函数，只要求它们定义在调用者可见的某个作用域中。

　　让我们新建一个名为 *functions* 的二进制项目，进一步探索函数。把 `another_function` 示例放到 *src/main.rs* 中并运行。你应看到如下输出：

```console
$ cargo run
   Compiling functions v0.1.0 (file:///projects/functions)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.28s
     Running `target/debug/functions`
Hello, world!
Another function.
```

　　各行按它们在 `main` 函数中出现的顺序执行。首先打印「Hello, world!」消息，然后调用 `another_function` 并打印它的消息。

### 参数 {#parameters}

　　我们可以定义带*参数*（parameters）的函数，参数是函数签名的一部分的特殊变量。当函数有参数时，你可以为其提供具体的值。从技术上讲，这些具体值称为*实参*（arguments），但在日常交谈中，人们往往把*参数*和*实参*互换使用，既指函数定义中的变量，也指调用时传入的具体值。

　　在这个版本的 `another_function` 中，我们添加了一个参数：

<span class="filename">文件名：src/main.rs</span>

```rust
fn main() {
    another_function(5);
}

fn another_function(x: i32) {
    println!("The value of x is: {x}");
}
```

　　试着运行这个程序；你应得到如下输出：

```console
$ cargo run
   Compiling functions v0.1.0 (file:///projects/functions)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 1.21s
     Running `target/debug/functions`
The value of x is: 5
```

　　`another_function` 的声明有一个名为 `x` 的参数。`x` 的类型被指定为 `i32`。当我们把 `5` 传入 `another_function` 时，`println!` 宏会把格式字符串中包含 `x` 的那对花括号替换为 `5`。

　　在函数签名中，你*必须*声明每个参数的类型。这是 Rust 设计中的刻意决定：要求在函数定义中标注类型，意味着编译器几乎从不需要你在代码其他地方再写类型标注来弄清你指的是什么类型。若编译器知道函数期望的类型，也能给出更有帮助的错误信息。

　　定义多个参数时，用逗号分隔参数声明，像这样：

<span class="filename">文件名：src/main.rs</span>

```rust
fn main() {
    print_labeled_measurement(5, 'h');
}

fn print_labeled_measurement(value: i32, unit_label: char) {
    println!("The measurement is: {value}{unit_label}");
}
```

　　这个例子创建了一个名为 `print_labeled_measurement` 的函数，它有两个参数。第一个参数名为 `value`，类型是 `i32`。第二个名为 `unit_label`，类型是 `char`。函数随后打印包含 `value` 和 `unit_label` 的文本。

　　让我们试着运行这段代码。把 *functions* 项目的 *src/main.rs* 中当前的程序替换为前面的示例，并用 `cargo run` 运行：

```console
$ cargo run
   Compiling functions v0.1.0 (file:///projects/functions)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.31s
     Running `target/debug/functions`
The measurement is: 5h
```

　　因为我们调用函数时把 `5` 作为 `value` 的值、把 `'h'` 作为 `unit_label` 的值，程序输出中包含这些值。

### 语句与表达式 {#statements-and-expressions}

　　函数体由一系列语句构成，并可选择以一个表达式结束。到目前为止，我们讲过的函数都没有包含结尾表达式，但你已经见过作为语句一部分的表达式。因为 Rust 是一门基于表达式的语言，理解这一区别很重要。其他语言未必有同样的区分，所以让我们看看什么是语句、什么是表达式，以及它们的差异如何影响函数体。

- *语句*（Statements）是执行某些操作但不返回值的指令。
- *表达式*（Expressions）求值得到一个结果值。

　　让我们看一些例子。

　　其实我们已经用过语句和表达式。用 `let` 关键字创建变量并赋给它一个值就是一条语句。在示例 3-1 中，`let y = 6;` 是一条语句。

**文件名：`src/main.rs`**
```rust
fn main() {
    let y = 6;
}
```

**示例 3-1：包含一条语句的 `main` 函数声明**

　　函数定义也是语句；前面整个例子本身就是一条语句。（我们很快会看到，调用函数并不是语句。）

　　语句不返回值。因此，你不能像下面这段代码试图做的那样，把一条 `let` 语句赋给另一个变量；你会得到错误：

<span class="filename">文件名：src/main.rs</span>

```rust
fn main() {
    let x = (let y = 6);
}
```

　　运行这个程序时，你会得到类似这样的错误：

```console
$ cargo run
   Compiling functions v0.1.0 (file:///projects/functions)
error: expected expression, found `let` statement
 --> src/main.rs:2:14
  |
2 |     let x = (let y = 6);
  |              ^^^
  |
  = note: only supported directly in conditions of `if` and `while` expressions

warning: unnecessary parentheses around assigned value
 --> src/main.rs:2:13
  |
2 |     let x = (let y = 6);
  |             ^         ^
  |
  = note: `#[warn(unused_parens)]` (part of `#[warn(unused)]`) on by default
help: remove these parentheses
  |
2 -     let x = (let y = 6);
2 +     let x = let y = 6 ;
  |

warning: `functions` (bin "functions") generated 1 warning
error: could not compile `functions` (bin "functions") due to 1 previous error; 1 warning emitted
```

　　`let y = 6` 语句不返回值，因此没有东西可以绑定给 `x`。这与 C 和 Ruby 等其他语言不同，在那些语言里赋值会返回所赋的值。在那些语言中，你可以写 `x = y = 6`，让 `x` 和 `y` 都具有值 `6`；在 Rust 中则不行。

　　表达式会求值为一个值，并构成你在 Rust 中编写的其余大部分代码。考虑一个数学运算，例如 `5 + 6`，它是一个求值为 `11` 的表达式。表达式可以是语句的一部分：在示例 3-1 中，语句 `let y = 6;` 里的 `6` 就是一个求值为 `6` 的表达式。调用函数是表达式。调用宏是表达式。用花括号创建的新作用域块也是表达式，例如：

<span class="filename">文件名：src/main.rs</span>

```rust
fn main() {
    let y = {
        let x = 3;
        x + 1
    };

    println!("The value of y is: {y}");
}
```

　　这个表达式：

```rust
{
    let x = 3;
    x + 1
}
```

　　是一个在本例中求值为 `4` 的块。该值作为 `let` 语句的一部分被绑定到 `y`。注意末尾没有分号的 `x + 1` 这一行，这与你目前见过的大多数行不同。表达式不以结尾分号结束。若你在表达式末尾加上分号，就把它变成了语句，然后它就不会返回值。在接下来探索函数返回值与表达式时，请记住这一点。

### 带返回值的函数 {#functions-with-return-values}

　　函数可以把值返回给调用它们的代码。我们不为返回值命名，但必须在箭头（`->`）之后声明它们的类型。在 Rust 中，函数的返回值等同于函数体块中最后一个表达式的值。你可以使用 `return` 关键字并指定一个值来提前从函数返回，但大多数函数会隐式返回最后一个表达式。下面是一个返回值的函数示例：

<span class="filename">文件名：src/main.rs</span>

```rust
fn five() -> i32 {
    5
}

fn main() {
    let x = five();

    println!("The value of x is: {x}");
}
```

　　`five` 函数中没有函数调用、宏，甚至没有 `let` 语句——只有单独的数字 `5`。这在 Rust 中是完全合法的函数。注意函数的返回类型也被指定了，为 `-> i32`。试着运行这段代码；输出应如下所示：

```console
$ cargo run
   Compiling functions v0.1.0 (file:///projects/functions)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.30s
     Running `target/debug/functions`
The value of x is: 5
```

　　`five` 中的 `5` 就是函数的返回值，因此返回类型是 `i32`。让我们更仔细地看看。有两点很重要：第一，`let x = five();` 这一行表明我们在用函数的返回值来初始化变量。因为函数 `five` 返回 `5`，那一行等价于：

```rust
let x = 5;
```

　　第二，`five` 函数没有参数，并定义了返回值的类型，但函数体是一个孤单的、没有分号的 `5`，因为它是一个我们想要返回其值的表达式。

　　再看另一个例子：

<span class="filename">文件名：src/main.rs</span>

```rust
fn main() {
    let x = plus_one(5);

    println!("The value of x is: {x}");
}

fn plus_one(x: i32) -> i32 {
    x + 1
}
```

　　运行这段代码会打印 `The value of x is: 6`。但若我们在包含 `x + 1` 的那一行末尾加上分号，把它从表达式变成语句，会发生什么？

<span class="filename">文件名：src/main.rs</span>

```rust
fn main() {
    let x = plus_one(5);

    println!("The value of x is: {x}");
}

fn plus_one(x: i32) -> i32 {
    x + 1;
}
```

　　编译这段代码会产生如下错误：

```console
$ cargo run
   Compiling functions v0.1.0 (file:///projects/functions)
error[E0308]: mismatched types
 --> src/main.rs:7:24
  |
7 | fn plus_one(x: i32) -> i32 {
  |    --------            ^^^ expected `i32`, found `()`
  |    |
  |    implicitly returns `()` as its body has no tail or `return` expression
8 |     x + 1;
  |          - help: remove this semicolon to return this value

For more information about this error, try `rustc --explain E0308`.
error: could not compile `functions` (bin "functions") due to 1 previous error
```

　　主要错误信息 `mismatched types` 揭示了这段代码的核心问题。函数 `plus_one` 的定义说它将返回一个 `i32`，但语句不会求值为一个值，这由单元类型 `()` 表示。因此什么也没有返回，这与函数定义矛盾并导致错误。在这段输出中，Rust 提供了一条可能有助于纠正问题的消息：它建议去掉分号，那样就能修复错误。
