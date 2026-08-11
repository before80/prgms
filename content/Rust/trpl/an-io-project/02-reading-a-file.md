+++
title = "12.2 读取文件"
date = 2026-08-05T08:44:00+08:00
weight = 51
type = "docs"
description = "用 fs::read_to_string 读取文件内容"
isCJKLanguage = true
draft = false
rust_version = "1.97.1"

+++

> 译文 · 基于 [The Rust Programming Language](https://doc.rust-lang.org/stable/book/)（rustc 1.97.1）

# 读取文件


> 原文链接: [https://doc.rust-lang.org/stable/book/ch12-02-reading-a-file.html](https://doc.rust-lang.org/stable/book/ch12-02-reading-a-file.html)


## 读取文件

　　接下来为程序添加读取 `file_path` 参数所指定文件的功能。首先需要一个用于测试的示例文件：我们用一首多行、篇幅不长、且有一些重复词的文本。示例 12-3 是艾米莉·狄金森（Emily Dickinson）的一首诗，很适合这个用途！在项目根目录创建名为 *poem.txt* 的文件，并录入诗歌 “I’m Nobody! Who are you?”。

**文件名：`poem.txt`**
```text
I'm nobody! Who are you?
Are you nobody, too?
Then there's a pair of us - don't tell!
They'd banish us, you know.

How dreary to be somebody!
How public, like a frog
To tell your name the livelong day
To an admiring bog!
```

**示例 12-3：艾米莉·狄金森的诗是很好的测试用例**

　　文本就绪后，编辑 *src/main.rs*，加入读取文件的代码，如示例 12-4 所示。

**文件名：`src/main.rs`**
```rust
use std::env;
use std::fs;

fn main() {
    // --snip--

    println!("In file {file_path}");

    let contents = fs::read_to_string(file_path)
        .expect("Should have been able to read the file");

    println!("With text:\n{contents}");
}
```

**示例 12-4：读取第二个参数所指定文件的内容**

　　首先用 `use` 语句引入标准库中相关的部分：处理文件需要 `std::fs`。

　　在 `main` 中，新增的 `fs::read_to_string` 会接收 `file_path`，打开该文件，并返回类型为 `std::io::Result<String>` 的值，其中包含文件内容。

　　之后我们再次加入临时的 `println!`，在读完文件后打印 `contents` 的值，以便确认目前为止程序工作正常。

　　用任意字符串作为第一个命令行参数（因为搜索功能尚未实现）、用 *poem.txt* 作为第二个参数运行这段代码：

```console
$ cargo run -- the poem.txt
   Compiling minigrep v0.1.0 (file:///projects/minigrep)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.0s
     Running `target/debug/minigrep the poem.txt`
Searching for the
In file poem.txt
With text:
I'm nobody! Who are you?
Are you nobody, too?
Then there's a pair of us - don't tell!
They'd banish us, you know.

How dreary to be somebody!
How public, like a frog
To tell your name the livelong day
To an admiring bog!
```

　　很好！代码读取并打印了文件内容。不过代码还有几处不足。目前 `main` 函数承担了多项职责：一般来说，每个函数只负责一件事时会更清晰、更易维护。另一个问题是错误处理还不够完善。程序还很小，这些问题暂时不算严重；但随着程序变大，就更难干净地修复它们。开发时尽早开始重构是好习惯，因为重构少量代码容易得多。接下来我们就来做这件事。
