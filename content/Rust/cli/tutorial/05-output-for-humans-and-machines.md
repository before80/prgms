+++
title = "05-面向人与机器的输出"
date = 2026-08-01T10:33:00+08:00
weight = 15
type = "docs"
description = "人类可读输出与机器可解析输出"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Command Line Applications in Rust](https://rust-cli.github.io/book/)

# 面向人与机器的输出 {#output-for-humans-and-machines}


> 原文链接: [https://rust-cli.github.io/book/tutorial/output.html](https://rust-cli.github.io/book/tutorial/output.html)


## 打印 “Hello World” {#printing-hello-world}

```rust
println!("Hello World");
```

嗯，挺简单。
很好！下一话题。

## 使用 `println!` {#using-println}

用 `println!` 宏几乎可以打印你喜欢的所有东西。
这个宏能力相当惊人，
但也有一套特殊语法。
它期望第一个参数是包含占位符的字符串字面量。
后面参数的值会填进
这个字符串。

例如：

```rust
let x = 42;
println!("My lucky number is {}.", x);
```

会打印：

```console
My lucky number is 42.
```

上面字符串里的花括号（`{}`）就是一种占位符。
这是默认占位符类型，
会尽量以人类可读的方式打印给定值。
对数字和字符串效果很好，
但并非所有类型都能这样做。
因此还有一种“调试表示”，
可以通过把占位符写成 `{:?}` 来获得。

例如：

```rust
let xs = vec![1, 2, 3];
println!("The list is: {:?}", xs);
```

会打印：

```console
The list is: [1, 2, 3]
```

若希望自己的数据类型也能用于调试和日志打印，
通常可以在定义上方加上 `#[derive(Debug)]`。

<aside>

**说明：**
“对用户友好”的打印通过 [`Display`] trait 完成，
调试输出（人类可读但面向开发者）使用 [`Debug`] trait。
关于可在 `println!` 中使用的语法，
更多信息见 [`std::fmt` 模块的文档][std::fmt]。

[`Display`]: https://doc.rust-lang.org/1.39.0/std/fmt/trait.Display.html
[`Debug`]: https://doc.rust-lang.org/1.39.0/std/fmt/trait.Debug.html
[std::fmt]: https://doc.rust-lang.org/1.39.0/std/fmt/index.html

</aside>

## 打印错误 {#printing-errors}

打印错误应通过 `stderr`，
以便用户
和其它工具
更容易把输出管道到文件
或更多工具。

<aside>

**说明：**
在大多数操作系统上，
程序可以写入两个输出流：`stdout` 和 `stderr`。
`stdout` 用于程序的实际输出，
而 `stderr` 让错误和其它消息与 `stdout` 分开。
这样，
输出可以存到文件或管道给另一个程序，
同时错误仍展示给用户。

</aside>

在 Rust 中，这通过
`println!` 和 `eprintln!` 实现，
前者打印到 `stdout`，
后者打印到 `stderr`。

```rust
println!("This is information");
eprintln!("This is an error! :(");
```

<aside>

**注意**：打印[转义码]可能有危险，
会把用户的终端弄进奇怪状态。
手动打印时务必小心！

[escape codes]: https://en.wikipedia.org/wiki/ANSI_escape_code

理想情况下，处理原始转义码时应使用像 `ansi_term`
这样的 crate，
让你（和用户）的生活更轻松。

</aside>

## 关于打印性能的说明 {#a-note-on-printing-performance}

往终端打印出奇地慢！
如果在循环里调用 `println!` 之类的东西，
很容易成为原本很快的程序里的瓶颈。
要加速，
可以做两件事。

第一，
你可能想减少真正“刷新”到终端的写入次数。
`println!` 会*每次*告诉系统刷新到终端，
因为常见做法是每行打印一次。
若不需要这样，
可以把 `stdout` 句柄包在 [`BufWriter`] 里，
默认最多缓冲 8 kB。
仍可在想立即打印时对这个 `BufWriter`
调用 `.flush()`。

```rust
use std::io::{self, Write};

let stdout = io::stdout(); // 获取全局 stdout
let mut handle = io::BufWriter::new(stdout); // 可选：用缓冲区包住该句柄
writeln!(handle, "foo: {}", 42); // 若关心错误，在此加 `?`
```

第二，
获取 `stdout`（或 `stderr`）上的锁，
并用 `writeln!` 直接打印会有帮助。
这能避免系统反复锁定和解锁 `stdout`。

```rust
use std::io::{self, Write};

let stdout = io::stdout(); // 获取全局 stdout
let mut handle = stdout.lock(); // 获取其上的锁
writeln!(handle, "foo: {}", 42); // 若关心错误，在此加 `?`
```

也可以把两种做法结合起来。

[`BufWriter`]: https://doc.rust-lang.org/1.39.0/std/io/struct.BufWriter.html

## 显示进度条 {#showing-a-progress-bar}

有些 CLI 应用运行不到一秒，
有些则要几分钟或几小时。
如果你写的是后一类程序，
可能希望让用户看到正在发生什么。
为此，应尽量打印有用的状态更新，
最好是易于消化的形式。

使用 [indicatif] crate，
可以为程序添加进度条
和小小的旋转指示器。
下面是一个快速示例：

```rust
fn main() {
    let pb = indicatif::ProgressBar::new(100);
    for i in 0..100 {
        do_hard_work();
        pb.println(format!("[+] finished #{}", i));
        pb.inc(1);
    }
    pb.finish_with_message("done");
}
```

更多信息见[文档][indicatif docs]
和[示例][indicatif examples]。

[indicatif]: https://crates.io/crates/indicatif
[indicatif docs]: https://docs.rs/indicatif
[indicatif examples]: https://github.com/console-rs/indicatif/tree/main/examples

## 日志 {#logging}

为了更容易理解程序在做什么，
我们可能想加一些日志语句。
写应用时这通常很容易，
半年后再跑这个程序时会非常有用。
在某些方面，
打日志和用 `println!` 一样，
只不过你可以指定消息的重要性。
通常可用的级别是 _error_、_warn_、_info_、_debug_ 和 _trace_
（_error_ 优先级最高，_trace_ 最低）。

要为应用添加简单日志，
需要两样东西：
[log] crate（包含以日志级别命名的宏）
以及一个真正把日志写到有用地方的*适配器*。
能使用日志适配器非常灵活：
例如，你不仅可以写到终端，
还可以写到 [syslog] 或中央日志服务器。

[syslog]: https://en.wikipedia.org/wiki/Syslog

既然我们只关心写 CLI 应用，
一个易用的适配器是 [env_logger]。
之所以叫 “env” logger，是因为你可以用
环境变量指定想记录应用的哪些部分，
以及在哪个级别记录。
它会在日志消息前加上时间戳
以及消息来自的模块。
由于库也可以使用 `log`，
你也能轻松配置它们的日志输出。

[log]: https://crates.io/crates/log
[env_logger]: https://crates.io/crates/env_logger

快速示例如下：

```rust
use log::{info, warn};

fn main() {
    env_logger::init();
    info!("starting up");
    warn!("oops, nothing implemented!");
}
```

假定该文件是 `src/bin/output-log.rs`，
在 Linux 和 macOS 上可以这样运行：
```console
$ env RUST_LOG=info cargo run --bin output-log
    Finished dev [unoptimized + debuginfo] target(s) in 0.17s
     Running `target/debug/output-log`
[2018-11-30T20:25:52Z INFO  output_log] starting up
[2018-11-30T20:25:52Z WARN  output_log] oops, nothing implemented!
```

在 Windows PowerShell 中可以这样运行：
```console
$ $env:RUST_LOG="info"
$ cargo run --bin output-log
    Finished dev [unoptimized + debuginfo] target(s) in 0.17s
     Running `target/debug/output-log.exe`
[2018-11-30T20:25:52Z INFO  output_log] starting up
[2018-11-30T20:25:52Z WARN  output_log] oops, nothing implemented!
```

在 Windows CMD 中可以这样运行：
```console
$ set RUST_LOG=info
$ cargo run --bin output-log
    Finished dev [unoptimized + debuginfo] target(s) in 0.17s
     Running `target/debug/output-log.exe`
[2018-11-30T20:25:52Z INFO  output_log] starting up
[2018-11-30T20:25:52Z WARN  output_log] oops, nothing implemented!
```

`RUST_LOG` 是用来设置日志配置的环境变量名。
`env_logger` 也包含一个 builder，
以便以编程方式调整这些设置，
例如默认显示 _info_ 级别消息。

外面还有很多其它日志适配器，
以及对 `log` 的替代与扩展。
如果你知道应用会打很多日志，
务必审阅它们，
让用户的生活更轻松。

<aside>

**提示：**
经验表明，哪怕只是略有用处的 CLI 程序，也可能被用上很多年，
尤其是当初只打算当临时方案的那些。
如果你的应用出了问题，
有人（例如未来的你）需要弄清原因，
能够传入 `--verbose` 拿到额外日志输出，
可能决定调试是几分钟还是几小时。
[clap-verbosity-flag] crate 提供了一种快捷方式，
可为使用 `clap` 的项目添加 `--verbose`。

[clap-verbosity-flag]: https://crates.io/crates/clap-verbosity-flag

</aside>
