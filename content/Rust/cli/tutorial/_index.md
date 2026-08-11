+++
title = "01-15 分钟写出一个命令行应用"
date = 2026-08-01T10:33:00+08:00
weight = 10
type = "docs"
description = "从零构建一个简单的 CLI 工具教程"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Command Line Applications in Rust](https://rust-cli.github.io/book/)

# 15 分钟写出一个命令行应用 {#a-command-line-app-in-15-minutes}


> 原文链接: [https://rust-cli.github.io/book/tutorial/index.html](https://rust-cli.github.io/book/tutorial/index.html)


本教程将引导你用 [Rust] 编写一个
CLI（命令行界面）应用。
大约十五分钟后，
你就能得到一个可以运行的程序
（大约到第 1.3 章）。
之后我们会继续打磨这个程序，
直到可以发布这款小工具。

[Rust]: https://rust-lang.org/

你会学到起步所需的全部要点，
以及去哪里查找更多信息。
觉得暂时用不到的部分可以跳过，
也可以从任意位置切入。

<aside>

**先决条件：**
本教程不能替代一般的编程入门，
并假定你已熟悉一些常见概念。
你应当能自如地使用命令行/终端。
如果你已经会几门其它语言，
这会是一次不错的 Rust 初体验。

**获取帮助：**
如果在任何时候觉得被所用特性淹没或弄糊涂了，
可以先查阅 Rust 自带的详尽官方文档，
首要的是那本《The Rust Programming Language》。
大多数 Rust 安装里都有它
（`rustup doc`），
也可以在线阅读：[doc.rust-lang.org]。

[doc.rust-lang.org]: https://doc.rust-lang.org

也非常欢迎提问——
Rust 社区以友好、乐于助人称道。
可以看看 [community page]，
了解人们讨论 Rust 的各种场所。

[community page]: https://www.rust-lang.org/community

</aside>

你想写什么样的项目？
不妨从简单的开始：
我们来写一个小型的 `grep` 克隆。
也就是：给它一个字符串和一条路径，
它就只打印包含该字符串的那些行。
我们把它叫做 `grrs`（读作 “grass”）。

最终，
我们希望能这样运行这个工具：

```console
$ cat test.txt
foo: 10
bar: 20
baz: 30
$ grrs foo test.txt
foo: 10
$ grrs --help
[some help text explaining the available options]
```

<aside class="note">

**说明：**
本书面向 [Rust 2018]。
这些代码示例也能在 Rust 2015 上使用，
但你可能需要稍作调整；
例如加上 `extern crate foo;`。

请确保运行的是 Rust 1.31.0（或更新版本），
并在 `Cargo.toml` 的 `[package]` 段中设置
`edition = "2018"`。

[Rust 2018]: https://doc.rust-lang.org/edition-guide/index.html

</aside>

## 本章其它页面 {#related-pages}

- [01-项目准备](01-project-setup/)
- [02-解析命令行参数](02-parsing-command-line-arguments/)
- [03-第一次实现](03-first-implementation/)
- [04-更友好的错误报告](04-nicer-error-reporting/)
- [05-面向人与机器的输出](05-output-for-humans-and-machines/)
- [06-测试](06-testing/)
- [07-打包与分发 Rust 工具](07-packaging-and-distributing-a-rust-tool/)
