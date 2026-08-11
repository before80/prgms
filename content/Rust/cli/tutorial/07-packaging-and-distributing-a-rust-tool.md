+++
title = "07-打包与分发 Rust 工具"
date = 2026-08-01T10:33:00+08:00
weight = 17
type = "docs"
description = "打包并分发 Rust CLI 工具"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Command Line Applications in Rust](https://rust-cli.github.io/book/)

# 打包与分发 Rust 工具 {#packaging-and-distributing-a-rust-tool}


> 原文链接: [https://rust-cli.github.io/book/tutorial/packaging.html](https://rust-cli.github.io/book/tutorial/packaging.html)


如果你确信程序已经准备好给别人用，
就是打包和发布的时候了！

有几种做法，
我们会看其中三种，
从搭建最快到对用户最方便。

## 最快：`cargo publish` {#quickest-cargo-publish}

发布应用最简单的方式是用 cargo。
还记得我们如何给项目加外部依赖吗？
Cargo 从默认的 crate 注册表 [crates.io] 下载它们。
用 `cargo publish`，
你可以把 crate 发布到 [crates.io]，
这对所有 crate 都适用，
包括带二进制目标的那些。

把 crate 发布到 [crates.io] 只需几步。
首先，如果还没有，在 [crates.io] 创建账户，
这通过 GitHub 授权完成，
所以你需要有 GitHub 账户
并已登录。
其次，在本机用 cargo 登录。
为此，打开你的
[crates.io 账户页面]，
创建一个新 token，
然后运行 `cargo login <your-new-token>`。
每台电脑只需做一次。
你可以在 cargo 的[发布指南]里
了解更多。

现在 cargo 和 crates.io 认识你了，
就可以发布 crate。
在匆忙发布新 crate 版本之前，
最好再打开一次 `Cargo.toml`，
确认已添加必要的元数据。
你可以在 [cargo 的清单格式]文档中
找到所有可设置的字段。
下面是一些常见条目的快速概览：

```toml
[package]
name = "grrs"
version = "0.1.0"
authors = ["Your Name <your@email.com>"]
license = "MIT OR Apache-2.0"
description = "A tool to search files"
readme = "README.md"
homepage = "https://github.com/you/grrs"
repository = "https://github.com/you/grrs"
keywords = ["cli", "search", "demo"]
categories = ["command-line-utilities"]
```

<aside class="note">

**说明：**
本示例包含必填的 license 字段，
取值是 Rust 项目常见的选择：
与编译器本身相同的许可证。
它还引用了 `README.md` 文件。
其中应有项目简介，
不仅会出现在 crates.io 的 crate 页面上，
GitHub 默认也会在仓库页面显示它。

</aside>

[crates.io]: https://crates.io/
[crates.io account page]: https://crates.io/me
[publishing guide]: https://doc.rust-lang.org/1.39.0/cargo/reference/publishing.html
[cargo's manifest format]: https://doc.rust-lang.org/1.39.0/cargo/reference/manifest.html

### 如何从 crates.io 安装二进制 {#how-to-install-a-binary-from-cratesio}

我们已经看到如何把 crate 发布到 crates.io，
你可能想知道如何安装它。
与库不同——
当你运行 `cargo build` 或类似命令时，
cargo 会下载并编译库——
安装二进制需要明确告诉它。

做法是
`cargo install <crate-name>`。
默认情况下它会下载 crate，
编译其中所有二进制目标
（以 “release” 模式，所以可能要一会儿），
并把它们复制到 `~/.cargo/bin/` 目录。
确保你的 shell 知道去那里找二进制！

也可以从 git 仓库安装 crate、
只安装某个 crate 中的特定二进制，
以及指定另一个安装目录。
详情见 `cargo install --help`。

### 何时使用 {#when-to-use-it}

`cargo install` 是安装二进制 crate 的简单方式。
对 Rust 开发者来说非常方便，
但也有明显缺点：
因为它总是从源码重新编译，
工具用户需要在机器上安装
Rust、cargo，以及项目所需的其它系统依赖。
编译大型 Rust 代码库可能很耗时。

最适合用来分发
面向其它 Rust 开发者的工具。
例如，
很多 cargo 子命令，
如 `cargo-tree` 或 `cargo-outdated`，
都可以用它安装。

## 分发二进制 {#distributing-binaries}

Rust 是编译到原生代码的语言，
默认静态链接所有依赖。
当你对包含名为 `grrs` 的二进制的项目运行 `cargo build` 时，
最终会得到一个叫 `grrs` 的二进制文件。
试试看！
用 `cargo build` 时，它在 `target/debug/grrs`，
运行 `cargo build --release` 时，在 `target/release/grrs`。
除非你使用的 crate
明确需要在目标系统上安装外部库
（比如使用系统版本的 OpenSSL），
这个二进制只依赖常见系统库。
也就是说，
你拿那一个文件，
发给和你跑同一操作系统的人，
他们就能运行它。

这已经很强大了！
它绕开了我们刚才看到的 `cargo install` 的两个缺点：
用户机器上不必安装 Rust，
也不用花一分钟编译，
可以立刻运行二进制。

如我们所见，
`cargo build` *已经*在为我们构建二进制。
问题在于，
那些二进制并不保证能在所有平台上工作。
如果你在 Windows 机器上运行 `cargo build`，
默认不会得到能在 Mac 上运行的二进制。
有没有办法自动为所有目标平台
生成这些二进制？

### 在 CI 上构建二进制发布 {#building-binary-releases-on-ci}

如果你的工具开源并托管在 GitHub 上，
很容易搭一个免费的 CI（持续集成）服务，
比如 [Travis CI]。
还有其它提供类似功能的服务，但 Travis 很流行。
每次你向仓库推送变更时，
它会在虚拟机里运行设置好的命令。
那些命令是什么、
跑在哪些类型的机器上，
都可以配置。
例如，
在装有 Rust 和一些常见构建工具的机器上运行 `cargo test` 是个好主意。
如果失败，
你就知道最近的变更有问题。

[Travis CI]: https://travis-ci.com/

我们也可以用它
构建二进制并上传到 GitHub！
如果我们运行
`cargo build --release`
并把二进制上传到某处，
就搞定了，对吧？
不完全是。
我们仍需确保构建的二进制
尽可能与更多系统兼容。
例如，
在 Linux 上我们可以为当前系统编译，
或为 `x86_64-unknown-linux-musl` 目标编译，
从而不依赖默认系统库。
在 macOS 上，可以把 `MACOSX_DEPLOYMENT_TARGET` 设为 `10.7`，
从而只依赖 10.7 及更早版本中已有的系统特性。

你可以看到用这种方法构建二进制的一个示例：
[这里][wasm-pack-travis]是 Linux 和 macOS，
[这里][wasm-pack-appveyor]是用 AppVeyor 的 Windows。

[wasm-pack-travis]: https://github.com/rustwasm/wasm-pack/blob/51e6351c28fbd40745719e6d4a7bf26dadd30c85/.travis.yml#L74-L91
[wasm-pack-appveyor]: https://github.com/rustwasm/wasm-pack/blob/51e6351c28fbd40745719e6d4a7bf26dadd30c85/.appveyor.yml

另一种方式是使用预构建（例如 Docker）镜像，
其中包含我们需要的所有工具
来构建二进制。
这也让我们更容易面向更冷门的平台。
[trust] 项目包含
你可以放进项目的脚本，
以及如何搭建的说明。
它还通过 AppVeyor 支持 Windows。

如果你更想在本地设置，
并在自己的机器上生成发布文件，
也可以看看 [trust]。
它内部使用 [cross]，
工作方式类似 cargo，
但会把命令转发到 Docker 容器内的 cargo 进程。
镜像定义也在
[cross 的仓库][cross]中。

[trust]: https://github.com/japaric/trust
[cross]: https://github.com/rust-embedded/cross

### 如何安装这些二进制 {#how-to-install-these-binaries}

你把用户指向发布页面，
可能看起来[像这样][wasm-pack-release]，
他们就可以下载我们刚创建的产物。
我们生成的发布产物没什么特别。
它们只是包含二进制的归档文件！
这意味着工具用户
可以用浏览器下载它们，
解压（常常是自动的），
并把二进制复制到喜欢的位置。

[wasm-pack-release]: https://github.com/rustwasm/wasm-pack/releases/tag/v0.5.1

这确实需要一些手动安装程序的经验，
所以你要在 README 里加一节，
说明如何安装这个程序。

<aside class="note">

**说明：**
如果你用 [trust] 构建二进制并加到 GitHub releases，
也可以告诉人们运行
`curl -LSfs https://japaric.github.io/trust/install.sh | sh -s -- --git your-name/repo-name`，
如果你觉得这样更方便的话。

</aside>

### 何时使用 {#when-to-use-binaries}

有二进制发布总的来说是个好主意。
几乎没有坏处。
它并不能解决用户必须手动
安装和更新
你的工具的问题，
但他们可以快速拿到最新发布版本，
而无需安装 Rust。

### 二进制之外还应打包什么 {#what-to-package-in-addition-to-your-binaries}

目前，
用户下载我们的发布构建时，
会得到一个只包含二进制文件的 `.tar.gz`。
在我们的示例项目中，
他们只会得到一个可运行的 `grrs` 文件，
但仓库里还有更多他们可能想要的文件。
例如说明如何使用工具的 README，
以及许可证文件。
既然已经有了，
加进去很容易。

还有更多有意义的文件，
尤其对命令行工具而言。
除了 README，我们是否也要附带 man page，
以及为 shell 补全可能标志的配置文件？
你可以手写这些，
但我们用的参数解析库 *clap*
（clap 建立在其上）
有办法为我们生成所有这些文件。
详见[这篇深入章节][clap-man-pages]。


[clap-man-pages]: /cli/in-depth/06-rendering-documentation-for-your-cli-apps/


## 让应用进入软件包仓库 {#getting-your-app-into-package-repositories}

到目前为止我们看到的两种做法，
都不是你通常在机器上安装软件的方式，
尤其是那些在大多数操作系统上
用全局包管理器安装的命令行工具。
对用户的好处很明显：
若能用安装其它工具的同样方式安装你的程序，
就不必再想安装方法。
这些包管理器也允许用户在有新版本时
更新程序。

遗憾的是，支持不同系统意味着
你得了解这些系统各自如何工作。
对有些系统，
可能只需向仓库加一个文件
（例如为 macOS 的 `brew` 加一个像[这样][rg-formula]的 Formula 文件），
对其它系统，你往往需要自己提交补丁，
把工具加进它们的仓库。
有一些有用的工具，如
[cargo-bundle](https://crates.io/crates/cargo-bundle)、
[cargo-deb](https://crates.io/crates/cargo-deb) 和
[cargo-aur](https://crates.io/crates/cargo-aur)，
但描述它们如何工作、
以及如何为那些不同系统正确打包工具，
超出了本章范围。

[rg-formula]: https://github.com/BurntSushi/ripgrep/blob/31adff6f3c4bfefc9e77df40871f2989443e6827/pkg/brew/ripgrep-bin.rb

相反，
我们来看一个用 Rust 写的工具，
它已出现在许多不同的包管理器中。

### 示例：ripgrep {#an-example-ripgrep}

[ripgrep] 是 `grep`/`ack`/`ag` 的替代品，用 Rust 写成。
它相当成功，并为许多操作系统打包：
看看其 README 的[“Installation” 一节][rg-install]！

注意它列出了几种安装方式：
先是指向 GitHub releases 的链接，
其中包含可直接下载的二进制；
接着列出用一堆不同包管理器安装的方法；
也可以用 `cargo install` 安装。

这看起来是个很好的主意。
不要只挑这里介绍的某一种做法。
从 `cargo install` 开始，
再加二进制发布，
最后再通过系统包管理器分发工具。

[ripgrep]: https://github.com/BurntSushi/ripgrep
[rg-install]: https://github.com/BurntSushi/ripgrep/tree/31adff6f3c4bfefc9e77df40871f2989443e6827#installation
