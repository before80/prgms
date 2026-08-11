+++
title = "05-与机器沟通"
date = 2026-08-01T10:33:00+08:00
weight = 25
type = "docs"
description = "结构化输出与管道协作"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Command Line Applications in Rust](https://rust-cli.github.io/book/)

# 与机器沟通 {#communicating-with-machines}


> 原文链接: [https://rust-cli.github.io/book/in-depth/machine-communication.html](https://rust-cli.github.io/book/in-depth/machine-communication.html)


命令行工具的真正威力，在你能把它们组合起来时才会显现。这并不是新想法：事实上，[Unix 哲学][Unix philosophy]里有这样一句话：

> 期望每个程序的输出都能成为另一个（尚且未知的）程序的输入。

[Unix philosophy]: https://en.wikipedia.org/wiki/Unix_philosophy

如果我们的程序满足这一期望，用户就会开心。为确保这一点运作良好，我们不应只提供给人看的漂亮输出，还应提供为其它程序量身定制的版本。来看看可以怎么做。

<aside>

**注意：**
请先阅读教程中的 [CLI 输出一章][output]。那一章讲如何向终端写入输出。

[output]: /cli/tutorial/05-output-for-humans-and-machines/

</aside>

## 谁在读？

首先要问的是：我们的输出是给坐在彩色终端前的人看的，还是给另一个程序看的？要回答这个问题，可以用 [IsTerminal] trait：

[IsTerminal]: https://doc.rust-lang.org/stable/std/io/trait.IsTerminal.html

```rust
use std::io::IsTerminal;

if std::io::stdout().is_terminal() {
    println!("I'm a terminal");
} else {
    println!("I'm not");
}
```

取决于谁会读我们的输出，我们可以添加额外信息。人类往往喜欢颜色，例如，在某个随机的 Rust 项目中运行 `ls`，你可能会看到类似这样的内容：

```console
$ ls
CODE_OF_CONDUCT.md   LICENSE-APACHE       examples
CONTRIBUTING.md      LICENSE-MIT          proptest-regressions
Cargo.lock           README.md            src
Cargo.toml           convey_derive        target
```

因为这种风格是为人设计的，在多数配置下它甚至会用颜色打印一些名字（如 `src`）以表明它们是目录。如果你把输出管道到文件，或像 `cat` 这样的程序，`ls` 会调整其输出。它不会再用适合我终端窗口的列排版，而是每个条目单独一行。它也不会发出任何颜色。

```console
$ ls | cat
CODE_OF_CONDUCT.md
CONTRIBUTING.md
Cargo.lock
Cargo.toml
LICENSE-APACHE
LICENSE-MIT
README.md
convey_derive
examples
proptest-regressions
src
target
```

## 面向机器的简单输出格式

历史上，命令行工具产生的唯一输出类型就是字符串。这对坐在终端前的人通常没问题，他们能阅读文本并理解其含义。其它程序通常没有这种能力：它们要理解像 `ls` 这样工具的输出，唯一办法是程序作者内置了一个恰好能解析 `ls` 当前输出的解析器。

这往往意味着输出被限制在易于解析的范围内。诸如 TSV（制表符分隔值）这类格式——每条记录一行，每行包含制表符分隔的内容——非常流行。这些基于文本行的简单格式，让像 `grep` 这样的工具可以用于 `ls` 一类工具的输出。`| grep Cargo` 并不关心你的行来自 `ls` 还是文件，它只是逐行过滤。

这样做的缺点是，你不能用简单的 `grep` 调用过滤出 `ls` 给你的所有目录。要做到那一点，每个目录项需要携带额外数据。

## 面向机器的 JSON 输出

制表符分隔值是输出结构化数据的简单方式，但它要求另一个程序知道要期望哪些字段（以及以何种顺序），并且难以输出不同类型的消息。例如，假设我们的程序想告诉消费者它正在等待下载，之后再输出一条描述所获数据的消息。那是非常不同的消息类型，试图把它们统一到 TSV 输出中会要求我们发明一种区分它们的方法。当我们想打印一条包含两个长度不等的列表的消息时也一样。

即便如此，选择一种在大多数编程语言/环境中都易于解析的格式仍是好主意。因此，过去几年里许多应用获得了以 [JSON] 输出数据的能力。它足够简单，几乎每种语言都有解析器，又足够强大，在很多场景下都有用。虽然它是人类也能读的文本格式，也有很多人致力于实现能非常快速地解析 JSON、以及把数据序列化为 JSON 的实现。

[JSON]: https://www.json.org/

在上面的描述中，我们谈到了程序「写出」的「消息」。这是思考输出的好方式：你的程序不一定只输出一大块数据，实际上可能在运行过程中发出许多不同信息。在输出 JSON 时支持这种做法的一种简单方式，是每条消息写一个 JSON 文档，并把每个 JSON 文档放在新的一行（有时称为[按行分隔的 JSON][jsonlines]）。这可以让实现简单到只需使用普通的 `println!`。

[jsonlines]: https://en.wikipedia.org/wiki/JSON_streaming#Line-delimited_JSON

下面是一个简单例子，使用 [serde_json] 的 `json!` 宏，在 Rust 源码中快速写出有效的 JSON：

[serde_json]: https://crates.io/crates/serde_json

```rust
use clap::Parser;
use serde_json::json;

/// 在文件中搜索模式，并显示包含它的行。
#[derive(Parser)]
struct Cli {
    /// 输出 JSON，而不是人类可读的消息
    #[arg(long = "json")]
    json: bool,
}

fn main() {
    let args = Cli::parse();
    if args.json {
        println!(
            "{}",
            json!({
                "type": "message",
                "content": "Hello world",
            })
        );
    } else {
        println!("Hello world");
    }
}
```

输出如下：

```console
$ cargo run -q
Hello world
$ cargo run -q -- --json
{"content":"Hello world","type":"message"}
```

（用 `-q` 运行 `cargo` 会抑制其通常的输出。`--` 之后的参数会传给我们的程序。）

### 实践例子：ripgrep

_[ripgrep]_ 是用 Rust 编写的 _grep_ 或 _ag_ 替代品。默认情况下它会产出类似这样的输出：

[ripgrep]: https://github.com/BurntSushi/ripgrep

```console
$ rg default
src/lib.rs
37:    Output::default()

src/components/span.rs
6:    Span::default()
```

但加上 `--json` 后它会打印：

```console
$ rg default --json
{"type":"begin","data":{"path":{"text":"src/lib.rs"}}}
{"type":"match","data":{"path":{"text":"src/lib.rs"},"lines":{"text":"    Output::default()\n"},"line_number":37,"absolute_offset":761,"submatches":[{"match":{"text":"default"},"start":12,"end":19}]}}
{"type":"end","data":{"path":{"text":"src/lib.rs"},"binary_offset":null,"stats":{"elapsed":{"secs":0,"nanos":137622,"human":"0.000138s"},"searches":1,"searches_with_match":1,"bytes_searched":6064,"bytes_printed":256,"matched_lines":1,"matches":1}}}
{"type":"begin","data":{"path":{"text":"src/components/span.rs"}}}
{"type":"match","data":{"path":{"text":"src/components/span.rs"},"lines":{"text":"    Span::default()\n"},"line_number":6,"absolute_offset":117,"submatches":[{"match":{"text":"default"},"start":10,"end":17}]}}
{"type":"end","data":{"path":{"text":"src/components/span.rs"},"binary_offset":null,"stats":{"elapsed":{"secs":0,"nanos":22025,"human":"0.000022s"},"searches":1,"searches_with_match":1,"bytes_searched":5221,"bytes_printed":277,"matched_lines":1,"matches":1}}}
{"data":{"elapsed_total":{"human":"0.006995s","nanos":6994920,"secs":0},"stats":{"bytes_printed":533,"bytes_searched":11285,"elapsed":{"human":"0.000160s","nanos":159647,"secs":0},"matched_lines":2,"matches":2,"searches":2,"searches_with_match":2}},"type":"summary"}
```

如你所见，每个 JSON 文档都是一个包含 `type` 字段的对象（映射）。这让我们可以为 `rg` 写一个简单的前端，在这些文档陆续到来时读取它们，并显示匹配项（以及它们所在的文件），即使 _ripgrep_ 仍在搜索中。

<aside>

**注意：**
这就是 Visual Studio Code 用 _ripgrep_ 做代码搜索的方式。

</aside>

## 如何处理管道传入的输入

假设我们有一个读取文件中单词数的程序：

```rust
use clap::Parser;
use std::path::PathBuf;

/// 统计文件中的行数
#[derive(Parser)]
#[command(arg_required_else_help = true)]
struct Cli {
    /// 要读取的文件路径
    file: PathBuf,
}

fn main() {
    let args = Cli::parse();
    let mut word_count = 0;
    let file = args.file;

    for line in std::fs::read_to_string(&file).unwrap().lines() {
        word_count += line.split(' ').count();
    }

    println!("Words in {}: {}", file.to_str().unwrap(), word_count)
}
```

它接受文件路径，逐行读取，并统计以空格分隔的单词数。

运行时，它会输出文件中的总单词数：

```console
$ cargo run README.md
Words in README.md: 47
```

但如果我们想统计管道传入程序的单词数呢？Rust 程序可以通过标准库的 [stdin 函数](https://doc.rust-lang.org/std/io/fn.stdin.html) 获得 [Stdin 结构体](https://doc.rust-lang.org/std/io/struct.Stdin.html) 来读取经 stdin 传入的数据。与读取文件的行类似，它也可以从 stdin 读取行。

下面是一个统计经 stdin 管道传入内容单词数的程序：

```rust
use clap::{CommandFactory, Parser};
use std::{
    fs::File,
    io::{BufRead, BufReader, IsTerminal, stdin},
    path::PathBuf,
};

/// 统计文件或 stdin 中的行数
#[derive(Parser)]
#[command(arg_required_else_help = true)]
struct Cli {
    /// 要读取的文件路径；使用 - 从 stdin 读取（stdin 不能是 tty）
    file: PathBuf,
}

fn main() {
    let args = Cli::parse();

    let word_count;
    let mut file = args.file;

    if file == PathBuf::from("-") {
        if stdin().is_terminal() {
            Cli::command().print_help().unwrap();
            ::std::process::exit(2);
        }

        file = PathBuf::from("<stdin>");
        word_count = words_in_buf_reader(BufReader::new(stdin().lock()));
    } else {
        word_count = words_in_buf_reader(BufReader::new(File::open(&file).unwrap()));
    }

    println!("Words from {}: {}", file.to_string_lossy(), word_count)
}

fn words_in_buf_reader<R: BufRead>(buf_reader: R) -> usize {
    let mut count = 0;
    for line in buf_reader.lines() {
        count += line.unwrap().split(' ').count()
    }
    count
}
```

如果你用管道传入文本运行该程序，并用 `-` 表示要从 `stdin` 读取，它会输出单词数：

```console
$ echo "hi there friend" | cargo run -- -
Words from stdin: 3
```

它要求 stdin 不是交互式的，因为我们期望的是通过管道传入程序的输入，而不是运行时键入的文本。如果 stdin 是 tty，它会输出帮助文档，以便说明为何无法工作。
