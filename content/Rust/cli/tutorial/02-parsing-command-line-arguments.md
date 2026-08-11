+++
title = "02-解析命令行参数"
date = 2026-08-01T10:33:00+08:00
weight = 12
type = "docs"
description = "解析 CLI 参数（含 clap）"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Command Line Applications in Rust](https://rust-cli.github.io/book/)

# 解析命令行参数 {#parsing-command-line-arguments}


> 原文链接: [https://rust-cli.github.io/book/tutorial/cli-args.html](https://rust-cli.github.io/book/tutorial/cli-args.html)


我们的 CLI 工具一次典型调用会像这样：

```console
$ grrs foobar test.txt
```

我们期望程序查看 `test.txt`，
并打印出包含 `foobar` 的行。
但这两个值该怎么拿到？

程序名后面的文本通常叫做
“命令行参数”（command-line arguments），
或“命令行标志”（command-line flags）
（尤其是形如 `--this` 的时候）。
在操作系统内部，它们通常表示成
字符串列表。一般由空格分隔。

关于这些参数有很多种理解方式，
以及如何把它们解析成
更便于使用的形式。
你还需要告诉程序的用户
需要提供哪些参数，
以及期望的格式是什么。

## 获取参数 {#getting-the-arguments}

标准库提供了函数
[`std::env::args()`]，它会给你一个包含给定参数的[迭代器]。
第一项（索引 `0`）是用来启动程序的名称
（例如 `grrs`）。后面的才是用户随后写下的内容。

[`std::env::args()`]: https://doc.rust-lang.org/1.39.0/std/env/fn.args.html
[iterator]: https://doc.rust-lang.org/1.39.0/std/iter/index.html

用这种方式拿到原始参数很直接（在文件 `src/main.rs` 中）：

```rust
fn main() {
    let pattern = std::env::args().nth(1).expect("no pattern given");
    let path = std::env::args().nth(2).expect("no path given");

    println!("pattern: {:?}, path: {:?}", pattern, path)
}
```

我们可以用 `cargo run` 运行它，
在 `--` 后面写上要传入的参数：

```console
$ cargo run -- some-pattern some-file
    Finished dev [unoptimized + debuginfo] target(s) in 0.11s
     Running `target/debug/grrs some-pattern some-file`
pattern: "some-pattern", path: "some-file"
```

## 把 CLI 参数当作数据类型 {#cli-arguments-as-data-types}

与其把它们想成一堆文本，
更划算的做法往往是把 CLI 参数看作一种自定义数据类型，
用来表示程序的输入。

看 `grrs foobar test.txt`，
有两个参数：
首先是 `pattern`（要查找的字符串），
然后是 `path`（要在其中查找的文件）。

还能说些什么？
首先，两者都是必填的。
我们还没谈过默认值，
所以期望用户总是提供两个值。
此外，还能说说它们的类型：
模式期望是字符串，
而第二个参数期望是文件路径。

在 Rust 中，围绕所处理的数据来组织程序很常见，
因此这样看待 CLI 参数非常契合。我们先从这段开始（在文件
`src/main.rs` 中，`fn main() {` 之前）：

```rust
struct Cli {
    pattern: String,
    path: std::path::PathBuf,
}
```

这定义了一个新结构体（[`struct`]），
有两个字段用来存数据：`pattern` 和 `path`。

[`struct`]: https://doc.rust-lang.org/1.39.0/book/ch05-00-structs.html

<aside>

**说明：**
[`PathBuf`] 类似 [`String`]，但是用于跨平台的文件系统路径。

[`PathBuf`]: https://doc.rust-lang.org/1.39.0/std/path/struct.PathBuf.html
[`String`]: https://doc.rust-lang.org/1.39.0/std/string/struct.String.html

</aside>

现在，仍需把实际参数转换成这种形式。
一种做法是手动解析操作系统给我们的字符串列表，
然后自己构造这个结构体。
大概会像这样：

```rust
fn main() {
    let pattern = std::env::args().nth(1).expect("no pattern given");
    let path = std::env::args().nth(2).expect("no path given");

    let args = Cli {
        pattern,
        path: std::path::PathBuf::from(path),
    };

    println!("pattern: {:?}, path: {:?}", args.pattern, args.path);
}
```

这能用，但不太方便。
如果要支持 `--pattern="foo"` 或 `--pattern "foo"` 该怎么办？
如何实现 `--help`？

## 用 Clap 解析 CLI 参数 {#parsing-cli-arguments-with-clap}

更方便的做法是使用众多现成库中的一个。
解析命令行参数最流行的库
叫做 [`clap`]。
它具备你期望的全部功能，
包括子命令、[shell 补全]，以及出色的帮助信息。

[`clap`]: https://docs.rs/clap/
[shell completions]: https://docs.rs/clap_complete/

先把 `clap` 引进来：在 `Cargo.toml` 的 `[dependencies]` 段加入
`clap = { version = "4.0", features = ["derive"] }`。

然后可以在代码里写 `use clap::Parser;`，
并在 `struct Cli` 正上方加上 `#[derive(Parser)]`。
顺带也写一些文档注释。

看起来会像这样（在文件 `src/main.rs` 中，`fn main() {` 之前）：

```rust
use clap::Parser;

/// 在文件中搜索模式并显示包含它的行。
#[derive(Parser)]
struct Cli {
    /// 要查找的模式
    pattern: String,
    /// 要读取的文件路径
    path: std::path::PathBuf,
}
```

<aside class="node">

**说明：**
字段上可以加很多自定义属性。
例如，
若希望该字段对应 `-o` 或 `--output` 后面的参数，
可以加上 `#[arg(short = 'o', long = "output")]`。
更多信息见 [clap 文档][`clap`]。

</aside>

在 `Cli` 结构体正下方，模板里有它的 `main` 函数。
程序启动时会调用这个函数：

```rust
fn main() {
    let args = Cli::parse();

    println!("pattern: {:?}, path: {:?}", args.pattern, args.path)
}
```

这会尝试把参数解析进我们的 `Cli` 结构体。

但如果失败了呢？
这正是这种方法的妙处：
Clap 知道期望哪些字段
以及它们的格式。
它可以自动生成漂亮的 `--help` 信息，
也能在你写成 `--putput` 时给出很好的错误，
建议你改用 `--output`。

<aside class="note">

**说明：**
`parse` 方法应在 `main` 函数中使用。
失败时，
它会打印错误或帮助信息，
并立即退出程序。
不要在其它地方使用它！

</aside>

## 收尾 {#wrapping-up}

你的代码现在应如下所示：

```rust
use clap::Parser;

/// 在文件中搜索模式并显示包含它的行。
#[derive(Parser)]
struct Cli {
    /// 要查找的模式
    pattern: String,
    /// 要读取的文件路径
    path: std::path::PathBuf,
}

fn main() {
    let args = Cli::parse();

    println!("pattern: {:?}, path: {:?}", args.pattern, args.path)
}
```

不带任何参数运行：

```console
$ cargo run
    Finished dev [unoptimized + debuginfo] target(s) in 10.16s
     Running `target/debug/grrs`
error: The following required arguments were not provided:
    <pattern>
    <path>

USAGE:
    grrs <pattern> <path>

For more information try --help
```

传入参数运行：

```console
$ cargo run -- some-pattern some-file
    Finished dev [unoptimized + debuginfo] target(s) in 0.11s
     Running `target/debug/grrs some-pattern some-file`
pattern: "some-pattern", path: "some-file"
```

输出表明程序已成功
把参数解析进了 `Cli` 结构体。
