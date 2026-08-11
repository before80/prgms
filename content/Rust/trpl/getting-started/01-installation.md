+++
title = "1.1 安装"
date = 2026-08-05T08:44:00+08:00
weight = 5
type = "docs"
description = "用 rustup 安装、更新与卸载 Rust"
isCJKLanguage = true
draft = false
rust_version = "1.97.1"

+++

> 译文 · 基于 [The Rust Programming Language](https://doc.rust-lang.org/stable/book/)（rustc 1.97.1）

# 安装 {#installation}


> 原文链接: [https://doc.rust-lang.org/stable/book/ch01-01-installation.html](https://doc.rust-lang.org/stable/book/ch01-01-installation.html)


## 安装 {#installation-heading}

　　第一步是安装 Rust。我们会通过命令行工具 `rustup` 下载 Rust，它用来管理 Rust 版本及相关工具。下载需要联网。

> 注意：若因某种原因不想使用 `rustup`，请参阅 [其他 Rust 安装方式][otherinstall] 页面了解更多选项。

　　下面的步骤会安装最新的稳定版 Rust 编译器。Rust 的稳定性保证意味着：本书中所有能编译通过的示例，在更新的 Rust 版本上仍应能编译。不同版本之间输出可能略有差异，因为 Rust 经常会改进错误信息与警告。换句话说，只要用这些步骤安装任何更新的稳定版 Rust，都应能正常配合本书内容使用。

> ### 命令行记号
>
> 在本章以及全书中，我们会展示一些在终端里使用的命令。需要你在终端中输入的行都以 `$` 开头。你不必输入 `$` 字符；它只是命令行提示符，用来标示每条命令的开始。不以 `$` 开头的行通常是上一条命令的输出。此外，针对 PowerShell 的示例会使用 `>` 而不是 `$`。

### 在 Linux 或 macOS 上安装 `rustup` {#installing-rustup-on-linux-or-macos}

　　如果你使用 Linux 或 macOS，打开终端并输入以下命令：

```console
$ curl --proto '=https' --tlsv1.2 https://sh.rustup.rs -sSf | sh
```

　　该命令会下载一个脚本并开始安装 `rustup` 工具，进而安装最新的稳定版 Rust。过程中可能会提示你输入密码。若安装成功，会出现下面这行：

```text
Rust is installed now. Great!
```

　　你还需要一个*链接器*（linker），也就是 Rust 用来把编译产物合并成一个文件的程序。你多半已经装好了。如果遇到链接器相关错误，应安装一个 C 编译器，它通常会附带链接器。C 编译器也很有用，因为一些常见的 Rust 包会依赖 C 代码，因而需要 C 编译器。

　　在 macOS 上，可以通过运行以下命令获得 C 编译器：

```console
$ xcode-select --install
```

　　Linux 用户一般应按发行版文档安装 GCC 或 Clang。例如，若使用 Ubuntu，可以安装 `build-essential` 包。

### 在 Windows 上安装 `rustup` {#installing-rustup-on-windows}

　　在 Windows 上，请前往 [https://www.rust-lang.org/tools/install][install] 并按说明安装 Rust。安装过程中会提示你安装 Visual Studio，它会提供链接器以及编译程序所需的原生库。若这一步需要更多帮助，请参阅
　　[https://rust-lang.github.io/rustup/installation/windows-msvc.html][msvc]。

　　本书其余部分使用的命令在 *cmd.exe* 和 PowerShell 中都能工作。若有具体差异，我们会说明该用哪一种。

### 排查问题 {#troubleshooting}

　　要检查 Rust 是否安装正确，打开一个 shell 并输入：

```console
$ rustc --version
```

　　你应能看到最新已发布稳定版的版本号、提交哈希和提交日期，格式如下：

```text
rustc x.y.z (abcabcabc yyyy-mm-dd)
```

　　若看到这些信息，说明 Rust 已安装成功！若没有，请按下面方式检查 Rust 是否在系统的 `%PATH%` 变量中。

　　在 Windows CMD 中：

```console
> echo %PATH%
```

　　在 PowerShell 中：

```powershell
> echo $env:Path
```

　　在 Linux 和 macOS 中：

```console
$ echo $PATH
```

　　若这些都正确而 Rust 仍无法使用，还有不少地方可以寻求帮助。如何联系其他 Rustacean（我们对自己的戏称），请见[社区页面][community]。

### 更新与卸载 {#updating-and-uninstalling}

　　一旦通过 `rustup` 安装了 Rust，更新到新发布的版本就很简单。在 shell 中运行：

```console
$ rustup update
```

　　若要卸载 Rust 和 `rustup`，在 shell 中运行：

```console
$ rustup self uninstall
```

### 阅读本地文档 {#reading-the-local-documentation}

　　安装 Rust 时也会附带一份本地文档副本，方便离线阅读。运行 `rustup doc` 即可在浏览器中打开本地文档。

　　每当标准库提供了某个类型或函数，而你不确定它做什么或怎么用时，就去查阅应用程序接口（API）文档吧！

### 使用文本编辑器与 IDE {#using-text-editors-and-ides}

　　本书不对你用什么工具编写 Rust 代码做任何假定。几乎任何文本编辑器都能胜任！不过，许多文本编辑器和集成开发环境（IDE）已内置对 Rust 的支持。你可以在 Rust 网站的[工具页面][tools]上找到一份相当新的编辑器与 IDE 列表。

### 离线使用本书 {#working-offline-with-this-book}

　　在若干示例中，我们会用到标准库之外的 Rust 包。要完成那些示例，你要么需要联网，要么需要提前下载这些依赖。要提前下载依赖，可以运行下面的命令。（我们稍后会详细解释 `cargo` 是什么，以及每条命令分别做什么。）


```console
$ cargo new get-dependencies
$ cd get-dependencies
$ cargo add rand@0.10.1 trpl@0.2.0
```

　　这会缓存这些包的下载，之后就不必再下载。运行完该命令后，不必保留 `get-dependencies` 文件夹。若已运行过此命令，本书后续所有 `cargo` 命令都可以加上 `--offline` 标志，以使用这些缓存版本，而不再尝试联网。

[otherinstall]: https://forge.rust-lang.org/infra/other-installation-methods.html
[install]: https://www.rust-lang.org/tools/install
[msvc]: https://rust-lang.github.io/rustup/installation/windows-msvc.html
[community]: https://www.rust-lang.org/community
[tools]: https://www.rust-lang.org/tools
