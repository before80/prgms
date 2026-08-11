+++
title = "19.1 模式可以使用的所有位置"
date = 2026-08-05T08:44:00+08:00
weight = 91
type = "docs"
description = "模式会出现在 Rust 的很多地方，而你可能已经在不知不觉中用了很多次！本节会讨论所有可以合法使用模式的位置。"
isCJKLanguage = true
draft = false
rust_version = "1.97.1"

+++

> 译文 · 基于 [The Rust Programming Language](https://doc.rust-lang.org/stable/book/)（rustc 1.97.1）

# 模式可以使用的所有位置


> 原文链接: [https://doc.rust-lang.org/stable/book/ch19-01-all-the-places-for-patterns.html](https://doc.rust-lang.org/stable/book/ch19-01-all-the-places-for-patterns.html)


## 所有可以使用模式的位置

　　模式会出现在 Rust 的很多地方，而你可能已经在不知不觉中用了很多次！本节会讨论所有可以合法使用模式的位置。

### `match` 分支

　　正如第六章讨论过的，我们会在 `match` 表达式的分支中使用模式。从形式上看，`match` 表达式由 `match` 关键字、要匹配的值，以及一个或多个 `match` 分支组成；这些分支包含一个模式，以及当值匹配该分支模式时要运行的表达式，就像这样：


<pre><code>match <em>VALUE</em> {
    <em>PATTERN</em> => <em>EXPRESSION</em>,
    <em>PATTERN</em> => <em>EXPRESSION</em>,
    <em>PATTERN</em> => <em>EXPRESSION</em>,
　　}</code></pre>

　　例如，下面是示例 6-5 中那个匹配变量 `x` 内 `Option<i32>` 值的 `match` 表达式：

```rust
match x {
    None => None,
    Some(i) => Some(i + 1),
}
```

　　这个 `match` 表达式中的模式，就是每个箭头左边的 `None` 和 `Some(i)`。

　　`match` 表达式有一个要求，那就是它必须是**穷尽的**（*exhaustive*）：`match` 表达式中值的所有可能情况都必须被覆盖到。确保覆盖所有可能性的一种方式，是让最后一个分支使用“捕获所有”的模式；例如，一个可以匹配任意值的变量名永远不会失败，因此它能够覆盖所有剩余情况。

　　特定的模式 `_` 可以匹配任何东西，但它永远不会绑定到变量上，因此常被用于最后一个 `match` 分支。当你想忽略某个未指定的值时，`_` 模式会非常有用。稍后在本章的 [「忽略模式中的值」][ignoring-values-in-a-pattern] 一节中，我们会更详细地讨论 `_` 模式。

### `let` 语句

　　在本章之前，我们只明确讨论过在 `match` 和 `if let` 中使用模式，但实际上，我们也在其他地方使用过模式，包括 `let` 语句。例如，来看这个简单直接的变量赋值：

```rust
let x = 5;
```

　　每次你写出像这样的 `let` 语句时，其实都在使用模式，只是你可能没有意识到！更正式地说，`let` 语句看起来像这样：


<pre>
<code>let <em>PATTERN</em> = <em>EXPRESSION</em>;</code>
</pre>

　　在像 `let x = 5;` 这样的语句中，位于 `PATTERN` 位置的变量名只是模式的一种特别简单的形式。Rust 会拿表达式与模式进行比较，并将它找到的任何名字赋值。所以，在 `let x = 5;` 这个例子中，`x` 是一个模式，表示“把这里匹配到的内容绑定到变量 `x`”。因为名字 `x` 本身就是整个模式，所以这个模式实际上等于“无论值是什么，都把它绑定到变量 `x`”。

　　为了更清楚地看出 `let` 的模式匹配这一面，来看示例 19-1，它在 `let` 中使用模式来解构一个元组。

```rust
    let (x, y, z) = (1, 2, 3);
```

**示例 19-1：使用模式解构元组，并一次创建三个变量**

　　这里，我们让一个元组去匹配一个模式。Rust 会比较值 `(1, 2, 3)` 和模式 `(x, y, z)`，并发现该值和模式匹配，也就是说，两边的元素个数相同；于是 Rust 将 `1` 绑定到 `x`，将 `2` 绑定到 `y`，将 `3` 绑定到 `z`。你可以把这个元组模式看作其中嵌套了三个独立的变量模式。

　　如果模式中的元素数量与元组中的元素数量不一致，那么整体类型就不会匹配，编译器也会报错。例如，示例 19-2 展示了试图用两个变量去解构一个三个元素的元组，这样是行不通的。

```rust
    let (x, y) = (1, 2, 3);
```

**示例 19-2：错误地构造了一个模式，其变量数量与元组中的元素数量不匹配**

　　尝试编译这段代码会得到如下类型错误：

```console
$ cargo run
   Compiling patterns v0.1.0 (file:///projects/patterns)
error[E0308]: mismatched types
 --> src/main.rs:2:9
  |
2 |     let (x, y) = (1, 2, 3);
  |         ^^^^^^   --------- this expression has type `({integer}, {integer}, {integer})`
  |         |
  |         expected a tuple with 3 elements, found one with 2 elements
  |
  = note: expected tuple `({integer}, {integer}, {integer})`
             found tuple `(_, _)`

For more information about this error, try `rustc --explain E0308`.
error: could not compile `patterns` (bin "patterns") due to 1 previous error
```

　　要修复这个错误，可以像本章后面 [「忽略模式中的值」][ignoring-values-in-a-pattern] 一节中会看到的那样，使用 `_` 或 `..` 来忽略元组中的一个或多个值。如果问题在于模式里的变量太多，那么解决办法就是删掉一些变量，使变量数量与元组中的元素数量相等。

### 条件 `if let` 表达式

　　在第六章中，我们讨论过如何使用 `if let` 表达式，它主要是用来简写只匹配一种情况的 `match`。此外，`if let` 还可以有一个对应的 `else`，在 `if let` 中的模式不匹配时执行其中的代码。

　　示例 19-3 表明，我们也可以混合使用 `if let`、`else if`、`else if let` 和 `else`。与 `match` 表达式相比，这样做给了我们更多灵活性；在 `match` 中，我们只能表达“把一个值与若干模式比较”。另外，Rust 也不要求一连串 `if let`、`else if` 和 `else if let` 分支中的条件彼此相关。

　　示例 19-3 中的代码会根据一系列条件检查来决定背景色应该是什么。为了举例，我们创建了几个带硬编码值的变量；而在真实程序里，这些值可能来自用户输入。

**文件名：`src/main.rs`**
```rust
fn main() {
    let favorite_color: Option<&str> = None;
    let is_tuesday = false;
    let age: Result<u8, _> = "34".parse();

    if let Some(color) = favorite_color {
        println!("Using your favorite color, {color}, as the background");
    } else if is_tuesday {
        println!("Tuesday is green day!");
    } else if let Ok(age) = age {
        if age > 30 {
            println!("Using purple as the background color");
        } else {
            println!("Using orange as the background color");
        }
    } else {
        println!("Using blue as the background color");
    }
}
```

**示例 19-3：混合使用 `if let`、`else if`、`else if let` 和 `else`**

　　如果用户指定了喜欢的颜色，就用该颜色作为背景色。如果没有指定喜欢的颜色，而且今天是星期二，那么背景色就是绿色。否则，如果用户把年龄作为字符串提供出来，并且我们能够成功将其解析为数字，那么背景色就会根据该数字的值变成紫色或橙色。如果这些条件都不满足，背景色就是蓝色。

　　这种条件结构让我们能够支持复杂的需求。使用这里的硬编码值，这个例子会打印 `Using purple as the background color`。

　　你还可以看到，`if let` 也能像 `match` 分支一样引入新变量，并遮蔽已有变量：`if let Ok(age) = age` 这一行引入了一个新的 `age` 变量，它保存 `Ok` 变体中的值，并遮蔽了原来的 `age` 变量。这意味着我们必须把 `if age > 30` 这个条件放在该代码块内部：不能把这两个条件合并成 `if let Ok(age) = age && age > 30`。因为我们想拿来和 `30` 比较的那个新 `age`，在由大括号开启的新作用域开始之前是无效的。

　　使用 `if let` 表达式的缺点是，编译器不会像检查 `match` 那样检查它的穷尽性。如果我们省略最后一个 `else` 块，从而漏掉对某些情况的处理，编译器也不会提醒我们这里可能存在逻辑错误。

### `while let` 条件循环

　　与 `if let` 在结构上类似的是 `while let` 条件循环，它允许 `while` 循环在模式持续匹配期间一直运行。示例 19-4 展示了一个 `while let` 循环，它等待线程之间发送的消息，不过这里检查的是 `Result`，而不是 `Option`。

```rust
    let (tx, rx) = std::sync::mpsc::channel();
    std::thread::spawn(move || {
        for val in [1, 2, 3] {
            tx.send(val).unwrap();
        }
    });

    while let Ok(value) = rx.recv() {
        println!("{value}");
    }
```

**示例 19-4：使用 `while let` 循环，只要 `rx.recv()` 返回 `Ok` 就打印值**

　　这个例子会打印 `1`、`2`，然后是 `3`。`recv` 方法会从信道的接收端取出第一条消息，并返回 `Ok(value)`。在第十六章第一次见到 `recv` 时，我们是直接对错误调用 `unwrap`，或者把它当作迭代器配合 `for` 循环使用。不过正如示例 19-4 所示，我们也可以使用 `while let`，因为只要发送端还存在，且不断有消息到达，`recv` 每次都会返回 `Ok`；当发送端断开连接后，它就会返回 `Err`。

### `for` 循环

　　在 `for` 循环中，紧跟在 `for` 关键字后面的值就是一个模式。例如，在 `for x in y` 中，`x` 就是那个模式。示例 19-5 展示了如何在 `for` 循环中使用模式来解构一个元组。

```rust
    let v = vec!['a', 'b', 'c'];

    for (index, value) in v.iter().enumerate() {
        println!("{value} is at index {index}");
    }
```

**示例 19-5：在 `for` 循环中使用模式来解构一个元组**

　　示例 19-5 中的代码会打印出如下内容：

```console
$ cargo run
   Compiling patterns v0.1.0 (file:///projects/patterns)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.52s
     Running `target/debug/patterns`
a is at index 0
b is at index 1
c is at index 2
```

　　我们使用 `enumerate` 方法适配了一个迭代器，使它产生由“值及其索引”组成的元组。它产生的第一个值是元组 `(0, 'a')`。当该值与模式 `(index, value)` 匹配时，`index` 会是 `0`，`value` 会是 `'a'`，于是打印出输出的第一行。

### 函数参数

　　函数参数也可以是模式。示例 19-6 中的代码声明了一个名为 `foo` 的函数，它接收一个名为 `x`、类型为 `i32` 的参数；到现在为止，这种写法应该已经很熟悉了。

```rust
fn foo(x: i32) {
    // code goes here
}
```

**示例 19-6：在参数中使用模式的函数签名**

　　`x` 这一部分就是一个模式！就像我们在 `let` 中做的那样，也可以在函数参数中用模式匹配一个元组。示例 19-7 展示了在向函数传参时如何拆开元组中的值。

**文件名：`src/main.rs`**
```rust
fn print_coordinates(&(x, y): &(i32, i32)) {
    println!("Current location: ({x}, {y})");
}

fn main() {
    let point = (3, 5);
    print_coordinates(&point);
}
```

**示例 19-7：一个在参数中解构元组的函数**

　　这段代码会打印 `Current location: (3, 5)`。值 `&(3, 5)` 会匹配模式 `&(x, y)`，因此 `x` 的值是 `3`，`y` 的值是 `5`。

　　由于闭包与函数类似，正如第十三章所讨论的那样，我们也可以像在函数参数列表中那样，在闭包参数列表中使用模式。

　　现在我们已经看过很多使用模式的方式了，不过模式在各处并不总是以同样的方式工作；在某些位置，模式必须是不可反驳的（*irrefutable*），这意味着它们必须匹配所提供的任何值；而在另一些位置，它们则可以是可反驳的（*refutable*）。接下来让我们讨论这两个概念。

[ignoring-values-in-a-pattern]: ../03-pattern-syntax/#ignoring-values-in-a-pattern
