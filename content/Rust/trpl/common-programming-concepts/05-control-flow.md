+++
title = "3.5 控制流"
date = 2026-08-05T08:44:00+08:00
weight = 14
type = "docs"
description = "if 表达式与 loop、while、for 循环"
isCJKLanguage = true
draft = false
rust_version = "1.97.1"

+++

> 译文 · 基于 [The Rust Programming Language](https://doc.rust-lang.org/stable/book/)（rustc 1.97.1）

# 控制流 {#control-flow}


> 原文链接: [https://doc.rust-lang.org/stable/book/ch03-05-control-flow.html](https://doc.rust-lang.org/stable/book/ch03-05-control-flow.html)


## 控制流 {#control-flow-heading}

　　根据条件是否为 `true` 来运行某些代码，以及在条件为 `true` 时反复运行某些代码的能力，是大多数编程语言的基本构件。让你控制 Rust 代码执行流的最常见结构是 `if` 表达式和循环。

### `if` 表达式 {#if-expressions}

　　`if` 表达式允许你根据条件对代码进行分支。你提供一个条件，然后说明：「若满足此条件，运行这块代码。若不满足，则不运行这块代码。」

　　在 *projects* 目录中新建一个名为 *branches* 的项目来探索 `if` 表达式。在 *src/main.rs* 文件中输入以下内容：

<span class="filename">文件名：src/main.rs</span>

```rust
fn main() {
    let number = 3;

    if number < 5 {
        println!("condition was true");
    } else {
        println!("condition was false");
    }
}
```

　　所有 `if` 表达式都以关键字 `if` 开头，后跟一个条件。在本例中，条件检查变量 `number` 的值是否小于 5。我们把条件为 `true` 时要执行的代码块紧接在条件之后放在花括号内。与 `if` 表达式中的条件关联的代码块有时称为*分支*（arms），就像我们在第 2 章[「比较猜测与秘密数字」][comparing-the-guess-to-the-secret-number]一节讨论的 `match` 表达式中的分支一样。

　　可选地，我们也可以包含一个 `else` 表达式（本例中我们选择这样做），以便在条件求值为 `false` 时给程序一个替代的代码块去执行。若你不提供 `else` 表达式且条件为 `false`，程序会跳过 `if` 块，继续执行下一段代码。

　　试着运行这段代码；你应看到如下输出：

```console
$ cargo run
   Compiling branches v0.1.0 (file:///projects/branches)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.31s
     Running `target/debug/branches`
condition was true
```

　　让我们试着把 `number` 的值改成使条件为 `false` 的值，看看会发生什么：

```rust
    let number = 7;
```

　　再次运行程序，查看输出：

```console
$ cargo run
   Compiling branches v0.1.0 (file:///projects/branches)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.31s
     Running `target/debug/branches`
condition was false
```

　　还值得注意的是，这段代码中的条件*必须*是 `bool`。若条件不是 `bool`，我们会得到错误。例如，试着运行下面的代码：

<span class="filename">文件名：src/main.rs</span>

```rust
fn main() {
    let number = 3;

    if number {
        println!("number was three");
    }
}
```

　　这次 `if` 条件求值为值 `3`，Rust 会抛出错误：

```console
$ cargo run
   Compiling branches v0.1.0 (file:///projects/branches)
error[E0308]: mismatched types
 --> src/main.rs:4:8
  |
4 |     if number {
  |        ^^^^^^ expected `bool`, found integer

For more information about this error, try `rustc --explain E0308`.
error: could not compile `branches` (bin "branches") due to 1 previous error
```

　　错误指出 Rust 期望 `bool` 却得到了整数。与 Ruby 和 JavaScript 等语言不同，Rust 不会自动尝试把非布尔类型转换成布尔值。你必须明确地始终为 `if` 提供布尔值作为条件。例如，若我们希望仅当数字不等于 `0` 时才运行 `if` 代码块，可以把 `if` 表达式改成下面这样：

<span class="filename">文件名：src/main.rs</span>

```rust
fn main() {
    let number = 3;

    if number != 0 {
        println!("number was something other than zero");
    }
}
```

　　运行这段代码会打印 `number was something other than zero`。

#### 用 `else if` 处理多个条件 {#handling-multiple-conditions-with-else-if}

　　你可以通过在 `else if` 表达式中组合 `if` 和 `else` 来使用多个条件。例如：

<span class="filename">文件名：src/main.rs</span>

```rust
fn main() {
    let number = 6;

    if number % 4 == 0 {
        println!("number is divisible by 4");
    } else if number % 3 == 0 {
        println!("number is divisible by 3");
    } else if number % 2 == 0 {
        println!("number is divisible by 2");
    } else {
        println!("number is not divisible by 4, 3, or 2");
    }
}
```

　　这个程序有四条可能的路径。运行后，你应看到如下输出：

```console
$ cargo run
   Compiling branches v0.1.0 (file:///projects/branches)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.31s
     Running `target/debug/branches`
number is divisible by 3
```

　　当这个程序执行时，它会依次检查每个 `if` 表达式，并执行第一个条件求值为 `true` 的主体。注意，即便 6 能被 2 整除，我们也看不到输出 `number is divisible by 2`，也看不到来自 `else` 块的 `number is not divisible by 4, 3, or 2` 文本。那是因为 Rust 只执行第一个为 `true` 的条件对应的块，一旦找到一个，甚至不会再检查其余条件。

　　使用太多 `else if` 表达式会让代码显得杂乱，所以若你有不止一个，可能想重构代码。第 6 章会描述一种强大的 Rust 分支结构 `match`，适用于这些情况。

#### 在 `let` 语句中使用 `if` {#using-if-in-a-let-statement}

　　因为 `if` 是表达式，我们可以在 `let` 语句的右侧使用它，把结果赋给变量，如示例 3-2 所示。

**文件名：`src/main.rs`**
```rust
fn main() {
    let condition = true;
    let number = if condition { 5 } else { 6 };

    println!("The value of number is: {number}");
}
```

**示例 3-2：把 `if` 表达式的结果赋给变量**

　　`number` 变量会根据 `if` 表达式的结果绑定到一个值。运行这段代码看看会发生什么：

```console
$ cargo run
   Compiling branches v0.1.0 (file:///projects/branches)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.30s
     Running `target/debug/branches`
The value of number is: 5
```

　　请记住，代码块求值为其中的最后一个表达式，而数字本身也是表达式。在本例中，整个 `if` 表达式的值取决于哪个代码块被执行。这意味着 `if` 各分支有可能作为结果的值必须是相同类型；在示例 3-2 中，`if` 分支和 `else` 分支的结果都是 `i32` 整数。若类型不匹配，如下面的例子，我们会得到错误：

<span class="filename">文件名：src/main.rs</span>

```rust
fn main() {
    let condition = true;

    let number = if condition { 5 } else { "six" };

    println!("The value of number is: {number}");
}
```

　　当我们试图编译这段代码时，会得到错误。`if` 和 `else` 分支的值类型不兼容，Rust 会明确指出程序中哪里有问题：

```console
$ cargo run
   Compiling branches v0.1.0 (file:///projects/branches)
error[E0308]: `if` and `else` have incompatible types
 --> src/main.rs:4:44
  |
4 |     let number = if condition { 5 } else { "six" };
  |                                 -          ^^^^^ expected integer, found `&str`
  |                                 |
  |                                 expected because of this

For more information about this error, try `rustc --explain E0308`.
error: could not compile `branches` (bin "branches") due to 1 previous error
```

　　`if` 块中的表达式求值为整数，`else` 块中的表达式求值为字符串。这行不通，因为变量必须具有单一类型，而 Rust 需要在编译期明确知道 `number` 变量是什么类型。知道 `number` 的类型能让编译器验证我们使用 `number` 的每一处类型是否有效。若 `number` 的类型只在运行时才确定，Rust 就无法做到这一点；若必须为任何变量跟踪多种假设类型，编译器会更复杂，对代码的保证也会更少。

### 用循环重复执行 {#repetition-with-loops}

　　经常需要把一块代码执行不止一次。为此，Rust 提供了几种*循环*（loops），它们会执行循环体内的代码直到末尾，然后立即从开头重新开始。为试验循环，让我们新建一个名为 *loops* 的项目。

　　Rust 有三种循环：`loop`、`while` 和 `for`。让我们逐一尝试。

#### 用 `loop` 重复代码 {#repeating-code-with-loop}

　　`loop` 关键字告诉 Rust 一遍又一遍地执行一块代码，要么永远执行，要么直到你显式告诉它停止。

　　例如，把 *loops* 目录中的 *src/main.rs* 文件改成这样：

<span class="filename">文件名：src/main.rs</span>

```rust
fn main() {
    loop {
        println!("again!");
    }
}
```

　　运行这个程序时，我们会看到 `again!` 不断打印，直到我们手动停止程序。大多数终端支持用键盘快捷键 <kbd>ctrl</kbd>-<kbd>C</kbd> 中断陷入持续循环的程序。试一试：


```console
$ cargo run
   Compiling loops v0.1.0 (file:///projects/loops)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.08s
     Running `target/debug/loops`
again!
again!
again!
again!
^Cagain!
```

　　符号 `^C` 表示你按下了 <kbd>ctrl</kbd>-<kbd>C</kbd> 的位置。

　　在 `^C` 之后你可能看到也可能看不到单词 `again!`，这取决于代码在收到中断信号时正处于循环的何处。

　　幸运的是，Rust 也提供了用代码跳出循环的方式。你可以在循环内放置 `break` 关键字，告诉程序何时停止执行循环。回想一下，我们在第 2 章猜数字游戏的[「猜对后退出」][quitting-after-a-correct-guess]一节中这样做过，以便在用户猜对正确数字赢得游戏时退出程序。

　　我们在猜数字游戏中也用过 `continue`，它在循环中告诉程序跳过本次迭代中剩余的代码，进入下一次迭代。

#### 从循环返回值 {#returning-values-from-loops}

　　`loop` 的用途之一是重试你知道可能失败的操作，例如检查某个线程是否已完成工作。你可能还需要把该操作的结果从循环传给代码的其余部分。为此，你可以在用来停止循环的 `break` 表达式之后加上想返回的值；该值会从循环中返回，以便你使用，如下所示：

```rust
fn main() {
    let mut counter = 0;

    let result = loop {
        counter += 1;

        if counter == 10 {
            break counter * 2;
        }
    };

    println!("The result is {result}");
}
```

　　在循环之前，我们声明一个名为 `counter` 的变量并初始化为 `0`。然后声明一个名为 `result` 的变量来保存从循环返回的值。在循环的每次迭代中，我们给 `counter` 变量加 `1`，然后检查 `counter` 是否等于 `10`。若是，我们使用带有值 `counter * 2` 的 `break` 关键字。循环之后，我们用分号结束把值赋给 `result` 的语句。最后，我们打印 `result` 中的值，本例中是 `20`。

　　你也可以从循环内部 `return`。`break` 只退出当前循环，而 `return` 总是退出当前函数。

#### 用循环标签消除歧义 {#disambiguating-with-loop-labels}

　　若你有嵌套循环，`break` 和 `continue` 会作用于此时最内层的循环。你可以选择性地为循环指定*循环标签*（loop label），然后在 `break` 或 `continue` 中使用该标签，以指定这些关键字作用于带标签的循环，而不是最内层循环。循环标签必须以单引号开头。下面是一个有两个嵌套循环的例子：

```rust
fn main() {
    let mut count = 0;
    'counting_up: loop {
        println!("count = {count}");
        let mut remaining = 10;

        loop {
            println!("remaining = {remaining}");
            if remaining == 9 {
                break;
            }
            if count == 2 {
                break 'counting_up;
            }
            remaining -= 1;
        }

        count += 1;
    }
    println!("End count = {count}");
}
```

　　外层循环有标签 `'counting_up`，它会从 0 计数到 2。没有标签的内层循环从 10 倒数到 9。第一个未指定标签的 `break` 只会退出内层循环。`break 'counting_up;` 语句会退出外层循环。这段代码打印：

```console
$ cargo run
   Compiling loops v0.1.0 (file:///projects/loops)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.58s
     Running `target/debug/loops`
count = 0
remaining = 10
remaining = 9
count = 1
remaining = 10
remaining = 9
count = 2
remaining = 10
End count = 2
```

#### 用 while 精简条件循环 {#streamlining-conditional-loops-with-while}

　　程序经常需要在循环内求值一个条件。只要条件为 `true`，循环就运行。当条件不再为 `true` 时，程序调用 `break`，停止循环。可以用 `loop`、`if`、`else` 和 `break` 的组合实现这类行为；若愿意，你现在就可以在程序中试一试。不过，这种模式非常常见，Rust 为此内置了一种语言结构，称为 `while` 循环。在示例 3-3 中，我们用 `while` 让程序循环三次，每次倒数，然后在循环后打印一条消息并退出。

**文件名：`src/main.rs`**
```rust
fn main() {
    let mut number = 3;

    while number != 0 {
        println!("{number}!");

        number -= 1;
    }

    println!("LIFTOFF!!!");
}
```

**示例 3-3：用 `while` 循环在条件求值为 `true` 时运行代码**

　　这种结构消除了若使用 `loop`、`if`、`else` 和 `break` 所必需的大量嵌套，也更清晰。只要条件求值为 `true`，代码就运行；否则就退出循环。

#### 用 `for` 遍历集合 {#looping-through-a-collection-with-for}

　　你可以选择用 `while` 结构来遍历集合的元素，例如数组。例如，示例 3-4 中的循环会打印数组 `a` 中的每个元素。

**文件名：`src/main.rs`**
```rust
fn main() {
    let a = [10, 20, 30, 40, 50];
    let mut index = 0;

    while index < 5 {
        println!("the value is: {}", a[index]);

        index += 1;
    }
}
```

**示例 3-4：用 `while` 循环遍历集合的每个元素**

　　这里，代码通过数组中的元素向上计数。它从索引 `0` 开始，然后循环直到到达数组的最后一个索引（也就是当 `index < 5` 不再为 `true` 时）。运行这段代码会打印数组中的每个元素：

```console
$ cargo run
   Compiling loops v0.1.0 (file:///projects/loops)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.32s
     Running `target/debug/loops`
the value is: 10
the value is: 20
the value is: 30
the value is: 40
the value is: 50
```

　　如预期，五个数组值都出现在终端中。即便 `index` 在某个时刻会达到值 `5`，循环也会在试图从数组获取第六个值之前停止执行。

　　不过，这种方法容易出错；若索引值或测试条件不正确，可能导致程序 panic。例如，若你把 `a` 数组的定义改成有四个元素，却忘了把条件更新为 `while index < 4`，代码就会 panic。它也较慢，因为编译器会添加运行时代码，在循环的每次迭代中执行索引是否在数组边界内的条件检查。

　　作为更简洁的替代方案，你可以使用 `for` 循环，对集合中的每一项执行一些代码。`for` 循环看起来像示例 3-5 中的代码。

**文件名：`src/main.rs`**
```rust
fn main() {
    let a = [10, 20, 30, 40, 50];

    for element in a {
        println!("the value is: {element}");
    }
}
```

**示例 3-5：用 `for` 循环遍历集合的每个元素**

　　运行这段代码时，我们会看到与示例 3-4 相同的输出。更重要的是，我们提高了代码的安全性，消除了因越过数组末尾或走得不够远而漏掉某些项所可能导致的 bug。由 `for` 循环生成的机器码也可能更高效，因为不必在每次迭代时把索引与数组长度比较。

　　使用 `for` 循环时，若你改变了数组中值的数量，不必像示例 3-4 所用的方法那样记得去改任何其他代码。

　　`for` 循环的安全性与简洁性使它们成为 Rust 中最常用的循环结构。即便在你想像示例 3-3 中使用 `while` 循环的倒数例子那样、想把某些代码运行特定次数的情况下，大多数 Rustacean 也会使用 `for` 循环。做法是使用标准库提供的 `Range`，它会生成从某个数开始、到另一个数之前结束的连续所有数字。

　　下面是用 `for` 循环以及我们尚未讨论过的另一个方法 `rev`（用于反转范围）实现倒数的样子：

<span class="filename">文件名：src/main.rs</span>

```rust
fn main() {
    for number in (1..4).rev() {
        println!("{number}!");
    }
    println!("LIFTOFF!!!");
}
```

　　这段代码是不是更简洁一点？

## 小结 {#summary}

　　你做到了！这是篇幅不小的一章：你学到了变量、标量与复合数据类型、函数、注释、`if` 表达式和循环！为练习本章讨论的概念，试着构建程序来做以下事情：

- 在华氏度与摄氏度之间转换温度。
- 生成第 *n* 个斐波那契数。
- 打印圣诞颂歌「The Twelve Days of Christmas」的歌词，利用歌曲中的重复。

　　当你准备好继续前进时，我们将讨论一个在其他编程语言中*并不*常见的 Rust 概念：所有权（ownership）。

[comparing-the-guess-to-the-secret-number]: ../../guessing-game/#comparing-the-guess-to-the-secret-number
[quitting-after-a-correct-guess]: ../../guessing-game/#quitting-after-a-correct-guess
