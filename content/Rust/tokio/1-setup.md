+++
title = "1 环境准备"
date = 2026-08-23T16:54:00+08:00
weight = 2
type = "docs"
description = ""
isCJKLanguage = true
draft = false

+++


> 原文链接: [https://tokio.rs/tokio/tutorial/setup](https://tokio.rs/tokio/tutorial/setup)

本教程将带你逐步完成构建 [Redis] 客户端和服务器的过程。我们将从 Rust 异步编程的基础开始，逐步深入。我们将实现 Redis 命令的一个子集，但会全面了解 Tokio。


你在本教程中要构建的项目在 GitHub 上以 [Mini-Redis][mini-redis] 的形式提供。Mini-Redis 的主要设计目标是学习 Tokio，因此注释非常详尽，但这也意味着 Mini-Redis 缺少你在真正的 Redis 库中会想要的一些功能。你可以在 [crates.io](https://crates.io/) 上找到可用于生产环境的 Redis 库。

我们将在教程中直接使用 Mini-Redis。这使我们能够在教程中使用 Mini-Redis 的部分功能，之后再在教程中实现它们。

# 获取帮助

任何时候，如果你遇到困难，都可以在 [Discord] 或 [GitHub 讨论区][disc] 寻求帮助。不必担心提出「初学者」问题。我们都是从零开始的，很乐意提供帮助。

[discord]: https://discord.gg/tokio
[disc]: https://github.com/tokio-rs/tokio/discussions

# 前置条件

读者应已熟悉 [Rust]。[Rust 程序设计][book] 是一本出色的入门资源。

虽然不是必需的，但使用 [Rust 标准库][std] 或其他语言编写网络代码的一些经验会有所帮助。

不需要预先了解 Redis。

[rust]: https://rust-lang.org
[book]: https://doc.rust-lang.org/book/
[std]: https://doc.rust-lang.org/std/

## Rust

开始之前，请确保已安装并配置好 [Rust][install-rust] 工具链。如果尚未安装，最简单的方式是使用 [rustup]。

本教程要求 Rust 最低版本为 `1.45.0`，但建议使用最新的稳定版 Rust。

要检查计算机上是否已安装 Rust，请运行以下命令：

```bash
$ rustc --version
```

你应该会看到类似 `rustc 1.46.0 (04488afe3 2020-08-24)` 的输出。

## Mini-Redis 服务器

接下来，安装 Mini-Redis 服务器。我们将在构建客户端的过程中用它来测试客户端。

```bash
$ cargo install mini-redis
```

通过启动服务器来确认安装成功：

```bash
$ mini-redis-server
```

然后，在另一个终端窗口中，使用 `mini-redis-cli` 尝试获取键 `foo`：

```bash
$ mini-redis-cli get foo
```

你应该会看到 `(nil)`。

# 准备就绪

就是这样，一切准备就绪。前往下一页，编写你的第一个异步 Rust 应用。

[redis]: https://redis.io
[mini-redis]: https://github.com/tokio-rs/mini-redis
[install-rust]: https://www.rust-lang.org/tools/install
[rustup]: https://rustup.rs/
