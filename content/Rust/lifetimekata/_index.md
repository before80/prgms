+++
title = "LifetimeKata"
date = 2026-08-23T16:26:00+08:00
weight = 1
type = "docs"
description = ""
isCJKLanguage = true
draft = false

+++


> 原文链接: [https://tfpk.github.io/lifetimekata/index.html](https://tfpk.github.io/lifetimekata/index.html)

欢迎来到 LifetimeKata——一套帮助你加深对 Rust 中生命周期理解的练习。许多任务要求你写出能通过编译的代码，有些则要求你刻意制造特定的编译错误。

请按顺序完成这些 kata，因为难度会逐步提升，且后面的练习依赖前面的内容。

## 入门

克隆本仓库：

```sh
$ git clone https://www.github.com/tfpk/lifetimekata/
```

大多数练习分两步运行：

```sh
$ cargo build --package ex04
```

然后任选其一：

```sh
$ cargo test --package ex04
```

或：

```sh
$ cargo run --package ex04
```

具体取决于该练习是二进制 crate 还是库 crate。
