+++
title = "附录D 有用的开发工具"
date = 2026-08-05T08:44:00+08:00
weight = 108
type = "docs"
description = "rustfmt、rustfix、Clippy 与 rust-analyzer 等开发工具"
isCJKLanguage = true
draft = false
rust_version = "1.97.1"

+++

> 译文 · 基于 [The Rust Programming Language](https://doc.rust-lang.org/stable/book/)（rustc 1.97.1）

# D - 有用的开发工具 {#d}


> 原文链接: [https://doc.rust-lang.org/stable/book/appendix-04-useful-development-tools.html](https://doc.rust-lang.org/stable/book/appendix-04-useful-development-tools.html)


## 附录 D：有用的开发工具

　　本附录介绍 Rust 项目提供的一些实用开发工具。我们会看到自动格式化、快速应用警告修复、代码检查工具，以及与 IDE 的集成。

### 用 `rustfmt` 自动格式化

　　`rustfmt` 工具会按社区代码风格重新格式化你的代码。许多协作项目使用 `rustfmt`，以免在写 Rust 时争论该用哪种风格：大家都用这个工具格式化代码。

　　Rust 安装默认包含 `rustfmt`，因此系统上通常已有 `rustfmt` 和 `cargo-fmt` 这两个程序。二者与 `rustc`、`cargo` 类似：`rustfmt` 提供更细粒度的控制，而 `cargo-fmt` 理解使用 Cargo 的项目约定。要格式化任意 Cargo 项目，输入：

```console
$ cargo fmt
```

　　运行该命令会格式化当前 crate 中的所有 Rust 代码。这应当只改变代码风格，而不改变语义。关于 `rustfmt` 的更多信息，见[其文档][rustfmt]。

### 用 `rustfix` 修复代码

　　`rustfix` 工具随 Rust 安装一并提供，可以自动修复那些有明确纠正方式、且通常正是你想要的结果的编译器警告。你大概已经见过编译器警告。例如看这段代码：

<span class="filename">文件名：src/main.rs</span>

```rust
fn main() {
    let mut x = 42;
    println!("{x}");
}
```

　　这里我们把变量 `x` 定义为可变，但从未真正修改它。Rust 会为此发出警告：

```console
$ cargo build
   Compiling myprogram v0.1.0 (file:///projects/myprogram)
warning: variable does not need to be mutable
 --> src/main.rs:2:9
  |
2 |     let mut x = 0;
  |         ----^
  |         |
  |         help: remove this `mut`
  |
  = note: `#[warn(unused_mut)]` on by default
```

　　警告建议我们去掉 `mut` 关键字。可以用 `rustfix` 工具通过运行 `cargo fix` 自动应用该建议：

```console
$ cargo fix
    Checking myprogram v0.1.0 (file:///projects/myprogram)
      Fixing src/main.rs (1 fix)
    Finished dev [unoptimized + debuginfo] target(s) in 0.59s
```

　　再看 *src/main.rs*，会发现 `cargo fix` 已经改动了代码：

<span class="filename">文件名：src/main.rs</span>

```rust
fn main() {
    let x = 42;
    println!("{x}");
}
```

　　变量 `x` 现在是不可变的，警告也不再出现。

　　还可以用 `cargo fix` 命令在不同 Rust edition 之间迁移代码。Edition 见[附录 E][editions]。

### 用 Clippy 做更多检查

　　Clippy 是一组 lint 的集合，用于分析代码，帮助你发现常见错误并改进 Rust 代码。标准 Rust 安装已包含 Clippy。

　　要对任意 Cargo 项目运行 Clippy 的检查，输入：

```console
$ cargo clippy
```

　　例如，假设你写了一个用近似数学常量（比如 pi）的程序，如下所示：

**文件名：`src/main.rs`**
```rust
fn main() {
    let x = 3.1415;
    let r = 8.0;
    println!("the area of the circle is {}", x * r * r);
}
```

　　对该项目运行 `cargo clippy` 会得到这样的错误：

```text
error: approximate value of `f{32, 64}::consts::PI` found
 --> src/main.rs:2:13
  |
2 |     let x = 3.1415;
  |             ^^^^^^
  |
  = note: `#[deny(clippy::approx_constant)]` on by default
  = help: consider using the constant directly
  = help: for further information visit https://rust-lang.github.io/rust-clippy/master/index.html#approx_constant
```

　　这个错误告诉你：Rust 已经定义了更精确的 `PI` 常量，改用该常量会让程序更正确。于是你应把代码改成使用 `PI` 常量。

　　下面的代码不会再收到 Clippy 的任何错误或警告：

**文件名：`src/main.rs`**
```rust
fn main() {
    let x = std::f64::consts::PI;
    let r = 8.0;
    println!("the area of the circle is {}", x * r * r);
}
```

　　关于 Clippy 的更多信息，见[其文档][clippy]。

### 用 `rust-analyzer` 集成 IDE

　　为帮助与 IDE 集成，Rust 社区推荐使用 [`rust-analyzer`][rust-analyzer]。这组以编译器为中心的工具遵循 [Language Server Protocol][lsp]（语言服务器协议）——一种让 IDE 与编程语言彼此通信的规范。不同客户端都可以使用 `rust-analyzer`，例如 [Visual Studio Code 的 Rust analyzer 插件][vscode]。

　　安装说明见 `rust-analyzer` 项目的[主页][rust-analyzer]，然后在你所用的 IDE 中安装语言服务器支持。IDE 将获得自动补全、跳转到定义、内联错误提示等能力。

[rustfmt]: https://github.com/rust-lang/rustfmt
[editions]: ../05-e-editions/
[clippy]: https://github.com/rust-lang/rust-clippy
[rust-analyzer]: https://rust-analyzer.github.io
[lsp]: http://langserver.org/
[vscode]: https://marketplace.visualstudio.com/items?itemName=rust-lang.rust-analyzer
