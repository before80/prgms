+++
title = "14.1 用发布配置自定义构建"
date = 2026-08-05T08:44:00+08:00
weight = 62
type = "docs"
description = "用 Cargo 发布配置（dev / release）自定义编译选项与优化级别"
isCJKLanguage = true
draft = false
rust_version = "1.97.1"

+++

> 译文 · 基于 [The Rust Programming Language](https://doc.rust-lang.org/stable/book/)（rustc 1.97.1）

# 用发布配置自定义构建


> 原文链接: [https://doc.rust-lang.org/stable/book/ch14-01-release-profiles.html](https://doc.rust-lang.org/stable/book/ch14-01-release-profiles.html)


## 用发布配置自定义构建

　　在 Rust 中，*发布配置*（release profiles）是一组预定义、可定制的配置，让你能更细致地控制编译选项。每个配置彼此独立设置。

　　Cargo 有两个主要配置：运行 `cargo build` 时使用的 `dev` 配置，以及运行 `cargo build --release` 时使用的 `release` 配置。`dev` 为开发提供了合适的默认值，`release` 则为发布构建提供了合适的默认值。

　　这些配置名你可能已经在构建输出里见过：


```console
$ cargo build
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.00s
$ cargo build --release
    Finished `release` profile [optimized] target(s) in 0.32s
```

　　这里的 `dev` 和 `release`，就是编译器使用的不同配置。

　　若项目的 *Cargo.toml* 中没有显式添加任何 `[profile.*]` 小节，Cargo 会对每个配置使用默认设置。你可以为想自定义的配置添加 `[profile.*]` 小节，从而覆盖默认设置中的任意子集。例如，下面是 `dev` 与 `release` 配置中 `opt-level` 的默认值：

<span class="filename">文件名：Cargo.toml</span>

```toml
[profile.dev]
opt-level = 0

[profile.release]
opt-level = 3
```

　　`opt-level` 控制 Rust 对代码应用多少优化，取值范围是 0 到 3。优化越多，编译时间越长。因此在开发阶段、需要频繁编译时，通常希望少做优化，以便更快编完——即便生成的代码运行会慢一些。于是 `dev` 的默认 `opt-level` 是 `0`。准备发布时，更值得多花编译时间：发布模式往往只编译一次，却会反复运行编译结果，因此用更长的编译时间换取更快的运行速度。这也是 `release` 配置默认 `opt-level` 为 `3` 的原因。

　　你可以在 *Cargo.toml* 里为某项设置指定不同的值，从而覆盖默认值。例如，若希望在开发配置中使用优化级别 1，可以在项目的 *Cargo.toml* 中加入这两行：

<span class="filename">文件名：Cargo.toml</span>

```toml
[profile.dev]
opt-level = 1
```

　　这段配置会覆盖默认的 `0`。此后运行 `cargo build` 时，Cargo 会沿用 `dev` 配置的其余默认值，再加上我们对 `opt-level` 的定制。因为把 `opt-level` 设为了 `1`，Cargo 会比默认多做一些优化，但又不会像发布构建那样激进。

　　各配置的完整选项与默认值，见 [Cargo 文档](https://doc.rust-lang.org/cargo/reference/profiles.html)。
