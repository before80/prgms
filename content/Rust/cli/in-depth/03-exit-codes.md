+++
title = "03-退出码"
date = 2026-08-01T10:33:00+08:00
weight = 23
type = "docs"
description = "CLI 退出码约定与实践"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Command Line Applications in Rust](https://rust-cli.github.io/book/)

# 退出码 {#exit-codes}


> 原文链接: [https://rust-cli.github.io/book/in-depth/exit-code.html](https://rust-cli.github.io/book/in-depth/exit-code.html)


程序并不总能成功。出错时，你应确保正确发出必要的信息。除了[向用户报告错误](04-communicating-with-humans/)之外，在大多数系统上，进程退出时还会发出一个退出码（0 到 255 之间的整数与大多数平台兼容）。你应尽量按程序状态发出正确的退出码。例如，在理想情况下程序成功时，应以 `0` 退出。

出错时就稍微复杂一些。在现实中，许多工具在常见失败时以 `1` 退出。目前，Rust 在进程 panic 时会设置退出码 `101`。除此之外，人们在程序里做过各种各样的事。

那么该怎么做？BSD 生态为退出码收集了一套常用定义（你可以在[这里][`sysexits.h`]找到它们）。Rust 库 [`exitcode`] 提供了相同的这些码，可直接用于你的应用。请参阅其 API 文档了解可用取值。

在 `Cargo.toml` 中加入 `exitcode` 依赖后，可以这样使用：

```rust
fn main() {
    // ...实际工作...
    match result {
        Ok(_) => {
            println!("Done!");
            std::process::exit(exitcode::OK);
        }
        Err(CustomError::CantReadConfig(e)) => {
            eprintln!("Error: {}", e);
            std::process::exit(exitcode::CONFIG);
        }
        Err(e) => {
            eprintln!("Error: {}", e);
            std::process::exit(exitcode::DATAERR);
        }
    }
}
```

[`exitcode`]: https://crates.io/crates/exitcode
[`sysexits.h`]: https://www.freebsd.org/cgi/man.cgi?query=sysexits&apropos=0&sektion=0&manpath=FreeBSD+11.2-stable&arch=default&format=html
