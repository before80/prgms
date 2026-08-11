+++
title = "1.3 Hello, Cargo!"
date = 2026-08-05T08:44:00+08:00
weight = 7
type = "docs"
description = "用 Cargo 创建、构建与运行 Rust 项目"
isCJKLanguage = true
draft = false
rust_version = "1.97.1"

+++

> 译文 · 基于 [The Rust Programming Language](https://doc.rust-lang.org/stable/book/)（rustc 1.97.1）

# Hello, Cargo! {#hello-cargo}


> 原文链接: [https://doc.rust-lang.org/stable/book/ch01-03-hello-cargo.html](https://doc.rust-lang.org/stable/book/ch01-03-hello-cargo.html)


## Hello, Cargo! {#hello-cargo-heading}

　　Cargo 是 Rust 的构建系统与包管理器。大多数 Rustacean 都用它来管理 Rust 项目，因为 Cargo 会替你处理大量事务，例如构建代码、下载代码所依赖的库，以及构建那些库。（我们把代码所需的库称为*依赖*（dependencies）。）

　　像我们目前写过的那种最简单的 Rust 程序并没有依赖。若我们当初用 Cargo 构建「Hello, world!」项目，它只会用到 Cargo 中负责构建代码的那一部分。随着你编写更复杂的 Rust 程序，你会添加依赖；而若用 Cargo 启动项目，添加依赖会容易得多。

　　因为绝大多数 Rust 项目都使用 Cargo，本书其余部分也假定你在使用 Cargo。若你使用的是[「安装」][installation]一节中讨论的官方安装程序，Cargo 会随 Rust 一并安装。若你通过其他方式安装了 Rust，可在终端中输入以下命令检查 Cargo 是否已安装：

```console
$ cargo --version
```

　　若看到版本号，说明已安装！若看到诸如 `command not found` 之类的错误，请查阅你所用安装方式的文档，了解如何单独安装 Cargo。

### 用 Cargo 创建项目 {#creating-a-project-with-cargo}

　　让我们用 Cargo 创建一个新项目，看看它与原来的「Hello, world!」项目有何不同。回到你的 *projects* 目录（或你决定存放代码的任何位置）。然后在任意操作系统上运行：

```console
$ cargo new hello_cargo
$ cd hello_cargo
```

　　第一条命令会创建一个名为 *hello_cargo* 的新目录与项目。我们把项目命名为 *hello_cargo*，Cargo 会在同名目录中创建其文件。

　　进入 *hello_cargo* 目录并列出文件。你会看到 Cargo 为我们生成了两个文件和一个目录：一个 *Cargo.toml* 文件，以及一个内含 *main.rs* 的 *src* 目录。

　　它还初始化了一个新的 Git 仓库，并生成了 *.gitignore* 文件。若你在已有的 Git 仓库内运行 `cargo new`，则不会生成 Git 相关文件；可用 `cargo new --vcs=git` 覆盖这一行为。

> 注意：Git 是常见的版本控制系统。你可以通过 `--vcs` 标志让 `cargo new` 使用其他版本控制系统，或不使用版本控制。运行 `cargo new --help` 可查看可用选项。

　　用你喜欢的文本编辑器打开 *Cargo.toml*。它应类似于示例 1-2 中的代码。

**文件名：`Cargo.toml`**
```toml
[package]
name = "hello_cargo"
version = "0.1.0"
edition = "2024"

[dependencies]
```

**示例 1-2：由 `cargo new` 生成的 *Cargo.toml* 内容**

　　该文件采用 [_TOML_][toml]（*Tom’s Obvious, Minimal Language*）格式，这是 Cargo 的配置格式。

　　第一行 `[package]` 是节标题，表示后面的语句在配置一个包。随着我们向该文件添加更多信息，还会加入其他节。

　　接下来三行设置 Cargo 编译程序所需的配置信息：名称、版本，以及要使用的 Rust edition。我们会在[附录 E][appendix-e]讨论 `edition` 键。

　　最后一行 `[dependencies]` 是一个节的开始，供你列出项目的任何依赖。在 Rust 中，代码包被称为 *crate*。本项目不需要其他 crate，但第 2 章的第一个项目会需要，那时我们会用到这个依赖节。

　　现在打开 *src/main.rs* 看一看：

<span class="filename">文件名：src/main.rs</span>

```rust
fn main() {
    println!("Hello, world!");
}
```

　　Cargo 已经为你生成了一个「Hello, world!」程序，和示例 1-1 中我们写的一样！到目前为止，我们的项目与 Cargo 生成的项目的差异在于：Cargo 把代码放在了 *src* 目录中，并且顶层目录有一个 *Cargo.toml* 配置文件。

　　Cargo 期望你的源文件位于 *src* 目录内。顶层项目目录则留给 README、许可证信息、配置文件，以及与代码无关的其他内容。使用 Cargo 有助于组织项目：各得其所，井然有序。

　　若你像「Hello, world!」项目那样，一开始没有使用 Cargo，也可以把它转换成使用 Cargo 的项目。把项目代码移到 *src* 目录，并创建合适的 *Cargo.toml* 文件。获取该 *Cargo.toml* 的一个简便办法是运行 `cargo init`，它会自动为你创建。

### 构建并运行 Cargo 项目 {#building-and-running-a-cargo-project}

　　现在看看用 Cargo 构建并运行「Hello, world!」程序有何不同！在 *hello_cargo* 目录中，输入以下命令构建项目：

```console
$ cargo build
   Compiling hello_cargo v0.1.0 (file:///projects/hello_cargo)
    Finished dev [unoptimized + debuginfo] target(s) in 2.85 secs
```

　　该命令会在 *target/debug/hello_cargo*（Windows 上为 *target\debug\hello_cargo.exe*）创建可执行文件，而不是在当前目录。因为默认构建是调试构建，Cargo 把二进制文件放在名为 *debug* 的目录中。可以用这条命令运行可执行文件：

```console
$ ./target/debug/hello_cargo # 或在 Windows 上使用 .\target\debug\hello_cargo.exe
Hello, world!
```

　　若一切顺利，终端应打印 `Hello, world!`。首次运行 `cargo build` 时，Cargo 还会在顶层创建一个新文件：*Cargo.lock*。该文件会跟踪项目中依赖的确切版本。本项目没有依赖，所以文件内容比较少。你永远不必手动修改这个文件；Cargo 会替你管理其内容。

　　我们刚才用 `cargo build` 构建了项目，并用 `./target/debug/hello_cargo` 运行了它，但也可以用 `cargo run` 一条命令完成编译并运行生成的可执行文件：

```console
$ cargo run
    Finished dev [unoptimized + debuginfo] target(s) in 0.0 secs
     Running `target/debug/hello_cargo`
Hello, world!
```

　　使用 `cargo run` 比先记着运行 `cargo build`、再使用二进制文件的完整路径更方便，因此大多数开发者都使用 `cargo run`。

　　注意这次我们没有看到 Cargo 正在编译 `hello_cargo` 的输出。Cargo 判断文件没有改动，因此没有重新构建，只是运行了二进制文件。若你修改了源代码，Cargo 会在运行前重新构建项目，你会看到类似这样的输出：

```console
$ cargo run
   Compiling hello_cargo v0.1.0 (file:///projects/hello_cargo)
    Finished dev [unoptimized + debuginfo] target(s) in 0.33 secs
     Running `target/debug/hello_cargo`
Hello, world!
```

　　Cargo 还提供了名为 `cargo check` 的命令。该命令会快速检查代码能否编译，但不生成可执行文件：

```console
$ cargo check
   Checking hello_cargo v0.1.0 (file:///projects/hello_cargo)
    Finished dev [unoptimized + debuginfo] target(s) in 0.32 secs
```

　　为什么不想要可执行文件呢？通常 `cargo check` 比 `cargo build` 快得多，因为它跳过了生成可执行文件的步骤。若你在写代码时不断检查工作，使用 `cargo check` 能更快地知道项目是否仍能编译！因此，许多 Rustacean 在编写程序时会定期运行 `cargo check` 以确保能编译，等到需要可执行文件时再运行 `cargo build`。

　　让我们回顾目前学到的关于 Cargo 的内容：

- 可以用 `cargo new` 创建项目。
- 可以用 `cargo build` 构建项目。
- 可以用 `cargo run` 一步构建并运行项目。
- 可以用 `cargo check` 在不生成二进制文件的情况下构建项目以检查错误。
- Cargo 不会把构建结果保存在与代码相同的目录中，而是放在 *target/debug* 目录。

　　使用 Cargo 的另一个好处是：无论你在哪个操作系统上工作，命令都相同。因此从现在起，我们不再分别给出 Linux/macOS 与 Windows 的具体说明。

### 为发布构建 {#building-for-release}

　　当你的项目终于准备好发布时，可以用 `cargo build --release` 以优化方式编译。该命令会在 *target/release* 而不是 *target/debug* 中创建可执行文件。优化会让你的 Rust 代码运行得更快，但开启优化会延长编译时间。这就是为什么有两种不同的配置：一种用于开发，你希望频繁、快速地重新构建；另一种用于构建最终交给用户的程序，它不会反复重建，并且要尽可能快地运行。若你要测量代码的运行时间，请务必用 `cargo build --release` 构建，并用 *target/release* 中的可执行文件做基准测试。

### 善用 Cargo 的约定 {#leveraging-cargos-conventions}

　　对于简单项目，Cargo 相比直接使用 `rustc` 优势不大，但随着程序变得更复杂，它的价值会显现出来。一旦程序扩展到多个文件或需要依赖，让 Cargo 协调构建就容易得多。

　　即便 `hello_cargo` 项目很简单，它也已经用上了你今后 Rust 生涯中大部分会用到的真实工具。事实上，要处理任何现有项目，你都可以用下面的命令通过 Git 检出代码、进入项目目录并构建：

```console
$ git clone example.org/someproject
$ cd someproject
$ cargo build
```

　　关于 Cargo 的更多信息，请参阅[其文档][cargo]。

## 小结 {#summary}

　　你已经在 Rust 之旅上有了一个很好的开端！在本章中，你学会了如何：

- 使用 `rustup` 安装最新的稳定版 Rust。
- 更新到更新的 Rust 版本。
- 打开本地安装的文档。
- 直接用 `rustc` 编写并运行「Hello, world!」程序。
- 按 Cargo 的约定创建并运行新项目。

　　现在正是构建一个更充实的程序、熟悉读写 Rust 代码的好时机。因此在第 2 章，我们会构建一个猜数字游戏程序。若你更想先了解常见编程概念在 Rust 中如何工作，请先看第 3 章，然后再回到第 2 章。

[installation]: ../01-installation/#installation
[toml]: https://toml.io
[appendix-e]: ../../appendix/05-e-editions/
[cargo]: https://doc.rust-lang.org/cargo/
