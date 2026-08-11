+++
title = "12.1 接受命令行参数"
date = 2026-08-05T08:44:00+08:00
weight = 50
type = "docs"
description = "用 std::env::args 读取并保存命令行参数"
isCJKLanguage = true
draft = false
rust_version = "1.97.1"

+++

> 译文 · 基于 [The Rust Programming Language](https://doc.rust-lang.org/stable/book/)（rustc 1.97.1）

# 接受命令行参数


> 原文链接: [https://doc.rust-lang.org/stable/book/ch12-01-accepting-command-line-arguments.html](https://doc.rust-lang.org/stable/book/ch12-01-accepting-command-line-arguments.html)


## 接受命令行参数

　　一如既往，我们用 `cargo new` 创建新项目。项目命名为 `minigrep`，以便与系统中可能已有的 `grep` 工具区分开：

```console
$ cargo new minigrep
     Created binary (application) `minigrep` project
$ cd minigrep
```

　　第一项任务是让 `minigrep` 接受两个命令行参数：文件路径，以及要搜索的字符串。也就是说，我们希望能这样运行程序：用 `cargo run`，再加两个连字符表示后面的参数属于我们的程序而非 `cargo`，然后是搜索字符串和文件路径，例如：

```console
$ cargo run -- searchstring example-filename.txt
```

　　目前 `cargo new` 生成的程序还无法处理我们传入的参数。[crates.io](https://crates.io/) 上已有一些库可以帮助编写接受命令行参数的程序，但既然你才刚接触这个概念，我们就自己来实现这项能力。

### 读取参数值

　　要让 `minigrep` 读取传入的命令行参数值，需要用到 Rust 标准库提供的 `std::env::args` 函数。它返回一个迭代器，产生传给 `minigrep` 的各个命令行参数。迭代器会在 [第 13 章][ch13] 完整讲解。眼下你只需知道两点：迭代器会依次产生一系列值；可以对迭代器调用 `collect` 方法，把它变成包含全部元素的集合（例如向量）。

　　示例 12-1 中的代码让 `minigrep` 读取传入的任意命令行参数，并把这些值收集到一个向量中。

**文件名：`src/main.rs`**
```rust
use std::env;

fn main() {
    let args: Vec<String> = env::args().collect();
    dbg!(args);
}
```

**示例 12-1：将命令行参数收集到向量中并打印**

　　首先，用 `use` 语句把 `std::env` 模块引入作用域，以便使用其中的 `args` 函数。注意 `std::env::args` 嵌套在两层模块里。正如我们在 [第 7 章][ch7-idiomatic-use] 讨论过的：当目标函数嵌套在多层模块中时，我们选择引入父模块而不是函数本身。这样可以方便地使用 `std::env` 中的其他函数；也比写 `use std::env::args` 再直接调用 `args` 更不容易产生歧义，因为 `args` 很容易被误认为是当前模块里定义的函数。

> ### `args` 函数与无效 Unicode
>
> 注意：若任一参数包含无效 Unicode，`std::env::args` 会 panic。若程序需要接受包含无效 Unicode 的参数，请改用 `std::env::args_os`。该函数返回的迭代器产生 `OsString` 而非 `String`。这里为简单起见选用 `std::env::args`，因为 `OsString` 因平台而异，使用起来也比 `String` 更复杂。

　　在 `main` 的第一行，我们调用 `env::args`，并立刻用 `collect` 把迭代器变成包含其全部值的向量。`collect` 可以创建多种集合，因此我们显式标注 `args` 的类型，指明要的是字符串向量。虽然在 Rust 中很少需要标注类型，但 `collect` 是你经常需要标注的函数之一，因为 Rust 无法推断你想要哪种集合。

　　最后，用调试宏打印该向量。先不带参数运行，再带两个参数运行：

```console
$ cargo run
   Compiling minigrep v0.1.0 (file:///projects/minigrep)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.61s
     Running `target/debug/minigrep`
[src/main.rs:5:5] args = [
    "target/debug/minigrep",
]
```

```console
$ cargo run -- needle haystack
   Compiling minigrep v0.1.0 (file:///projects/minigrep)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 1.57s
     Running `target/debug/minigrep needle haystack`
[src/main.rs:5:5] args = [
    "target/debug/minigrep",
    "needle",
    "haystack",
]
```

　　注意向量的第一个值是 `"target/debug/minigrep"`，也就是二进制文件的名称。这与 C 中参数列表的行为一致，程序可以在执行时使用调用它的名称。能拿到程序名往往很方便——例如在消息里打印它，或根据用来启动程序的命令行别名改变行为。但在本章中，我们会忽略它，只保存需要的那两个参数。

### 把参数值保存到变量中

　　程序现在已经能访问作为命令行参数指定的值了。接下来要把这两个参数的值保存到变量里，以便在程序其余部分使用。做法见示例 12-2。

**文件名：`src/main.rs`**
```rust
use std::env;

fn main() {
    let args: Vec<String> = env::args().collect();

    let query = &args[1];
    let file_path = &args[2];

    println!("Searching for {query}");
    println!("In file {file_path}");
}
```

**示例 12-2：创建变量保存查询参数与文件路径参数**

　　正如打印向量时所见，程序名占据向量中 `args[0]` 的位置，因此参数从索引 1 开始。`minigrep` 的第一个参数是要搜索的字符串，我们把对它的引用放进变量 `query`；第二个参数是文件路径，放进变量 `file_path`。

　　我们暂时打印这些变量的值，以证明代码按预期工作。再用参数 `test` 和 `sample.txt` 运行一次：

```console
$ cargo run -- test sample.txt
   Compiling minigrep v0.1.0 (file:///projects/minigrep)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.0s
     Running `target/debug/minigrep test sample.txt`
Searching for test
In file sample.txt
```

　　很好，程序能工作了！需要的参数值已经保存到正确的变量中。稍后我们会加入错误处理，应对用户未提供参数等潜在错误情况；眼下先忽略这些，转而添加读取文件的能力。

[ch13]: ../../functional-features/
[ch7-idiomatic-use]: ../../modules/04-bringing-paths-into-scope-with-the-use-keyword/#creating-idiomatic-use-paths
