+++
title = "04-与人沟通"
date = 2026-08-01T10:33:00+08:00
weight = 24
type = "docs"
description = "面向终端用户的输出与交互"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Command Line Applications in Rust](https://rust-cli.github.io/book/)

# 与人沟通 {#communicating-with-humans}


> 原文链接: [https://rust-cli.github.io/book/in-depth/human-communication.html](https://rust-cli.github.io/book/in-depth/human-communication.html)


请先阅读教程中的 [CLI 输出一章][output]。那一章讲如何向终端写入输出，而本章讨论的是要输出*什么*。

[output]: /cli/tutorial/05-output-for-humans-and-machines/

## 一切正常时

即使一切正常，报告应用进度也很有用。这些消息应尽量信息充分且简洁。日志里不要用过于技术化的术语。记住：应用并没有崩溃，用户没有理由去查找错误。

最重要的是，沟通风格要一致。使用相同的前缀和句子结构，让日志易于扫读。

尽量让应用输出讲述一个故事：它在做什么，以及对用户有何影响。这可以表现为展示相关步骤的时间线，甚至为长时间操作显示进度条和指示器。用户在任何时候都不应觉得应用在做一些神秘、跟不上的事情。

## 难以判断发生了什么时

在沟通非正常状态时，一致性同样重要。一个大量打日志却不遵循严格日志级别的应用，提供的信息量可能与完全不打日志的应用相当，甚至更少。

因此，重要的是为事件及其相关消息定义严重程度，并对它们使用一致的日志级别。这样用户就可以通过 `--verbose` 标志或环境变量（如 `RUST_LOG`）自行选择日志量。

常用的 `log` crate [定义][log-levels]了以下级别（按严重程度递增排列）：

- trace
- debug
- info
- warning
- error

把 *info* 当作默认日志级别是个好主意。用它输出，嗯，信息性内容。（一些偏好更安静输出风格的应用，默认可能只显示 warning 和 error。）

此外，在各条日志消息中使用相似的前缀和句子结构总是好的，这样便于用 `grep` 一类工具过滤。一条消息本身应提供足够上下文，以便在过滤后的日志里仍有用，同时又不要*过于*冗长。

[log-levels]: https://docs.rs/log/0.4.4/log/enum.Level.html

### 日志语句示例

```console
error: could not find `Cargo.toml` in `/home/you/project/`
```

```console
=> Downloading repository index
=> Downloading packages...
```

以下日志输出取自 [wasm-pack]：

```console
 [1/7] Adding WASM target...
 [2/7] Compiling to WASM...
 [3/7] Creating a pkg directory...
 [4/7] Writing a package.json...
 > [WARN]: Field `description` is missing from Cargo.toml. It is not necessary, but recommended
 > [WARN]: Field `repository` is missing from Cargo.toml. It is not necessary, but recommended
 > [WARN]: Field `license` is missing from Cargo.toml. It is not necessary, but recommended
 [5/7] Copying over your README...
 > [WARN]: origin crate has no README
 [6/7] Installing WASM-bindgen...
 > [INFO]: wasm-bindgen already installed
 [7/7] Running WASM-bindgen...
 Done in 1 second
```

## 发生 panic 时

一个常被忽略的方面是：程序崩溃时也会有输出。在 Rust 中，「崩溃」最常见的是「panic」（即「受控的崩溃」，相对于「被操作系统杀掉」）。默认情况下，发生 panic 时，「panic 处理器」会向控制台打印一些信息。

例如，如果你用 `cargo new --bin foo` 创建一个新的二进制项目，并把 `fn main` 的内容替换为 `panic!("Hello World")`，运行程序时会得到：

```console
thread 'main' panicked at 'Hello, world!', src/main.rs:2:5
note: Run with `RUST_BACKTRACE=1` for a backtrace.
```

这对你（开发者）很有用。（惊喜：程序因 `main.rs` 文件第 2 行而崩溃。）但对连源码都没有的用户来说，这没什么价值。事实上，它多半只会令人困惑。因此，添加一个自定义的 panic 处理器、提供更面向最终用户的输出是个好主意。

专门做这件事的一个库叫 [human-panic]。要把它加到你的 CLI 项目中，导入它，并在 `main` 函数开头调用 `setup_panic!()` 宏：

```rust
use human_panic::setup_panic;

fn main() {
   setup_panic!();

   panic!("Hello world")
}
```

这会显示一条非常友好的消息，并告诉用户可以做什么：

```console
Well, this is embarrassing.

foo had a problem and crashed. To help us diagnose the problem you can send us a crash report.

We have generated a report file at "/var/folders/n3/dkk459k908lcmkzwcmq0tcv00000gn/T/report-738e1bec-5585-47a4-8158-f1f7227f0168.toml". Submit an issue or email with the subject of "foo Crash Report" and include the report as an attachment.

- Authors: Your Name <your.name@example.com>

We take privacy seriously, and do not perform any automated error collection. In order to improve the software, we rely on people to submit reports.

Thank you kindly!
```

[human-panic]: https://crates.io/crates/human-panic
[wasm-pack]: https://crates.io/crates/wasm-pack
