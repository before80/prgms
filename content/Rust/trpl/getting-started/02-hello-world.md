+++
title = "1.2 Hello, World!"
date = 2026-08-05T08:44:00+08:00
weight = 6
type = "docs"
description = "编写并运行第一个 Hello, world! 程序"
isCJKLanguage = true
draft = false
rust_version = "1.97.1"

+++

> 译文 · 基于 [The Rust Programming Language](https://doc.rust-lang.org/stable/book/)（rustc 1.97.1）

# Hello, World! {#hello-world}


> 原文链接: [https://doc.rust-lang.org/stable/book/ch01-02-hello-world.html](https://doc.rust-lang.org/stable/book/ch01-02-hello-world.html)


## Hello, World! {#hello-world-heading}

　　既然已经安装好 Rust，是时候编写你的第一个 Rust 程序了。学习一门新语言时，传统做法是写一个小程序，把文本 `Hello, world!` 打印到屏幕上，我们也照此办理！

> 注意：本书假定你对命令行有基本了解。Rust 对你用什么编辑器、什么工具、代码放在哪里没有特别要求，所以若你更喜欢用 IDE 而不是命令行，完全可以使用你喜欢的 IDE。许多 IDE 如今都对 Rust 有一定支持；细节请查阅该 IDE 的文档。Rust 团队一直在通过 `rust-analyzer` 推动出色的 IDE 支持。更多细节见[附录 D][devtools]。

### 准备项目目录 {#project-directory-setup}

　　首先创建一个目录来存放你的 Rust 代码。对 Rust 来说，代码放在哪里并不重要，但就本书的练习与项目而言，我们建议在主目录下建一个 *projects* 目录，并把所有项目都放在那里。

　　打开终端，输入以下命令，创建 *projects* 目录，并在其中为「Hello, world!」项目再建一个目录。

　　在 Linux、macOS 以及 Windows 上的 PowerShell 中，输入：

```console
$ mkdir ~/projects
$ cd ~/projects
$ mkdir hello_world
$ cd hello_world
```

　　在 Windows CMD 中，输入：

```cmd
> mkdir "%USERPROFILE%\projects"
> cd /d "%USERPROFILE%\projects"
> mkdir hello_world
> cd hello_world
```

### Rust 程序基础 {#rust-program-basics}

　　接下来，新建一个源文件，命名为 *main.rs*。Rust 源文件总是以 *.rs* 扩展名结尾。若文件名包含多个单词，惯例是用下划线分隔。例如，用 *hello_world.rs*，而不是 *helloworld.rs*。

　　现在打开刚创建的 *main.rs*，输入示例 1-1 中的代码。

**文件名：`main.rs`**
```rust
fn main() {
    println!("Hello, world!");
}
```

**示例 1-1：打印 `Hello, world!` 的程序**

　　保存文件，回到位于 *~/projects/hello_world* 目录的终端窗口。在 Linux 或 macOS 上，输入以下命令编译并运行该文件：

```console
$ rustc main.rs
$ ./main
Hello, world!
```

　　在 Windows 上，用 `.\main` 代替 `./main`：

```powershell
> rustc main.rs
> .\main
Hello, world!
```

　　无论操作系统如何，终端都应打印出字符串 `Hello, world!`。若没有看到该输出，请回到[「安装」][troubleshooting]一节的「排查问题」部分寻求帮助。

　　若确实打印了 `Hello, world!`，恭喜！你已经正式写出了一个 Rust 程序。这意味着你成了一名 Rust 程序员——欢迎！

### Rust 程序的解剖 {#the-anatomy-of-a-rust-program}

　　让我们仔细看看这个「Hello, world!」程序。谜题的第一块是：

```rust
fn main() {

}
```

　　这几行定义了一个名为 `main` 的函数。`main` 函数很特别：它始终是每个可执行 Rust 程序中最先运行的代码。这里，第一行声明了一个名为 `main` 的函数，它没有参数，也不返回任何值。若有参数，它们会写在圆括号（`()`）里。

　　函数体包在 `{}` 中。Rust 要求所有函数体都使用花括号。良好的风格是把起始花括号放在与函数声明同一行，中间加一个空格。

> 注意：若希望在各个 Rust 项目间保持统一风格，可以使用名为 `rustfmt` 的自动格式化工具，按特定风格格式化代码（关于 `rustfmt` 的更多内容见[附录 D][devtools]）。Rust 团队已把该工具随标准 Rust 发行版一并提供，就像 `rustc` 一样，因此你的电脑上应该已经安装好了！

　　`main` 函数的函数体包含下面这行代码：

```rust
println!("Hello, world!");
```

　　这一行完成了这个小程序的全部工作：把文本打印到屏幕上。这里有三个重要细节需要注意。

　　第一，`println!` 调用的是一个 Rust 宏。若调用的是函数，则会写成 `println`（没有 `!`）。Rust 宏是一种编写能生成代码、从而扩展 Rust 语法的方式；我们会在[第 20 章][ch20-macros]更详细地讨论。眼下你只需知道：使用 `!` 表示你在调用宏而不是普通函数，并且宏并不总是遵循与函数相同的规则。

　　第二，你会看到字符串 `"Hello, world!"`。我们把它作为参数传给 `println!`，该字符串就会被打印到屏幕上。

　　第三，我们用分号（`;`）结束这一行，表示该表达式已经结束，下一条可以开始了。大多数 Rust 代码行都以分号结尾。

### 编译与运行 {#compilation-and-execution}

　　你刚刚运行了一个新创建的程序，下面我们逐步看看整个过程。

　　在运行 Rust 程序之前，必须用 Rust 编译器编译它：输入 `rustc` 命令，并传入源文件名，像这样：

```console
$ rustc main.rs
```

　　若你有 C 或 C++ 背景，会发现这与 `gcc` 或 `clang` 很像。编译成功后，Rust 会输出一个二进制可执行文件。

　　在 Linux、macOS 以及 Windows 上的 PowerShell 中，可以在 shell 里输入 `ls` 命令查看可执行文件：

```console
$ ls
main  main.rs
```

　　在 Linux 和 macOS 上，你会看到两个文件。在 Windows 的 PowerShell 上，你会看到与用 CMD 时相同的三个文件。在 Windows 的 CMD 中，可以输入：

```cmd
> dir /B  # /B 选项表示只显示文件名
main.exe
main.pdb
main.rs
```

　　这里会看到带 *.rs* 扩展名的源文件、可执行文件（Windows 上是 *main.exe*，其他平台上是 *main*），以及在 Windows 上带 *.pdb* 扩展名、包含调试信息的文件。接下来运行 *main* 或 *main.exe* 文件，像这样：

```console
$ ./main # 或在 Windows 上使用 .\main
```

　　若你的 *main.rs* 就是「Hello, world!」程序，这一行会在终端打印 `Hello, world!`。

　　若你更熟悉 Ruby、Python 或 JavaScript 这类动态语言，可能不习惯把编译和运行分成两步。Rust 是*提前编译*（ahead-of-time compiled）语言，这意味着你可以编译程序，把可执行文件交给别人，对方即使没有安装 Rust 也能运行。若你交给别人的是 *.rb*、*.py* 或 *.js* 文件，对方需要分别安装 Ruby、Python 或 JavaScript 的实现。但在那些语言里，你通常只需一条命令就能编译并运行程序。语言设计处处都是权衡。

　　对简单程序来说，只用 `rustc` 编译就够了；但随着项目变大，你会想管理各种选项，并方便地共享代码。接下来，我们会介绍 Cargo 工具，它会帮助你编写实际的 Rust 程序。

[troubleshooting]: ../01-installation/#troubleshooting
[devtools]: ../../appendix/04-d-useful-development-tools/
[ch20-macros]: ../../advanced-features/05-macros/
