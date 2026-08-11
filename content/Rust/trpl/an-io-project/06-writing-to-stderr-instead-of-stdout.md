+++
title = "12.6 将错误输出重定向到标准错误"
date = 2026-08-05T08:44:00+08:00
weight = 55
type = "docs"
description = "用 eprintln! 把错误信息写到标准错误而非标准输出"
isCJKLanguage = true
draft = false
rust_version = "1.97.1"

+++

> 译文 · 基于 [The Rust Programming Language](https://doc.rust-lang.org/stable/book/)（rustc 1.97.1）

# 将错误输出重定向到标准错误


> 原文链接: [https://doc.rust-lang.org/stable/book/ch12-06-writing-to-stderr-instead-of-stdout.html](https://doc.rust-lang.org/stable/book/ch12-06-writing-to-stderr-instead-of-stdout.html)


## 将错误重定向到标准错误

　　目前我们用 `println!` 宏把所有输出都写到终端。在大多数终端中，输出分为两类：用于一般信息的*标准输出*（`stdout`），以及用于错误信息的*标准错误*（`stderr`）。这种区分让用户可以把程序的成功输出定向到文件，同时仍把错误信息打印到屏幕上。

　　`println!` 只能打印到标准输出，因此要打印到标准错误，必须用别的方式。

### 检查错误写到了哪里

　　首先观察一下：`minigrep` 当前打印的内容（包括我们希望改写到标准错误的错误信息）是如何全部写到标准输出的。做法是把标准输出流重定向到文件，并故意制造一个错误。我们不重定向标准错误流，因此发往标准错误的内容会继续显示在屏幕上。

　　命令行程序应当把错误信息发送到标准错误流，这样即便把标准输出重定向到文件，仍能在屏幕上看到错误。我们的程序目前行为不当：马上就会看到，它把错误信息也保存进了文件！

　　为演示这种行为，用不带任何参数的方式运行程序（这应会触发错误），并用 `>` 和文件路径 *output.txt* 把标准输出重定向过去：

```console
$ cargo run > output.txt
```

　　`>` 语法告诉 shell：把标准输出的内容写到 *output.txt*，而不是屏幕。我们没有在屏幕上看到预期的错误信息，说明它一定进了文件。*output.txt* 的内容如下：

```text
Problem parsing arguments: not enough arguments
```

　　没错，错误信息被打印到了标准输出。像这样的错误信息打印到标准错误会有用得多，这样只有成功运行产生的数据才会进入文件。我们来改掉这一点。

### 把错误打印到标准错误

　　用示例 12-24 中的代码改变错误信息的打印方式。得益于本章前面的重构，所有打印错误信息的代码都集中在一个函数 `main` 里。标准库提供了向标准错误流打印的 `eprintln!` 宏，因此把两处用于打印错误的 `println!` 改成 `eprintln!` 即可。

**文件名：`src/main.rs`**
```rust
fn main() {
    let args: Vec<String> = env::args().collect();

    let config = Config::build(&args).unwrap_or_else(|err| {
        eprintln!("Problem parsing arguments: {err}");
        process::exit(1);
    });

    if let Err(e) = run(config) {
        eprintln!("Application error: {e}");
        process::exit(1);
    }
}
```

**示例 12-24：用 `eprintln!` 把错误信息写到标准错误而非标准输出**

　　再用同样方式运行：不带参数，并用 `>` 重定向标准输出：

```console
$ cargo run > output.txt
Problem parsing arguments: not enough arguments
```

　　现在错误出现在屏幕上，而 *output.txt* 为空——这正是命令行程序应有的行为。

　　再用不引起错误的参数运行一次，同时仍把标准输出重定向到文件：

```console
$ cargo run -- to poem.txt > output.txt
```

　　终端上看不到任何输出，*output.txt* 中会是我们的结果：

<span class="filename">文件名：output.txt</span>

```text
Are you nobody, too?
How dreary to be somebody!
```

　　这说明我们现在已按预期：成功输出走标准输出，错误输出走标准错误。

## 小结

　　本章回顾了此前学过的一些重要概念，并介绍了如何在 Rust 中执行常见的 I/O 操作。通过使用命令行参数、文件、环境变量，以及用 `eprintln!` 宏打印错误，你已经具备编写命令行应用的基础。结合前面各章的概念，你的代码会组织良好、用合适的数据结构有效存储数据、妥善处理错误，并且测试充分。

　　接下来，我们将探索一些受函数式语言影响的 Rust 特性：闭包与迭代器。
