+++
title = "04-依赖"
date = 2026-07-30T14:49:00+08:00
weight = 24
type = "docs"
description = "在 Cargo.toml 中添加与使用依赖"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Cargo Book](https://doc.rust-lang.org/cargo/)

# 依赖 {#dependencies}


> 原文链接: [https://doc.rust-lang.org/cargo/guide/dependencies.html](https://doc.rust-lang.org/cargo/guide/dependencies.html)


[crates.io] 是 Rust 社区的中央[*包注册表（package registry）*][def-package-registry]，用作发现与下载[包][def-package]的位置。`cargo` 默认配置为使用它来查找所请求的包。

要依赖托管在 [crates.io] 上的库，请将其添加到你的 `Cargo.toml`。

[crates.io]: https://crates.io/

## 添加依赖 {#adding-a-dependency}
若你的 `Cargo.toml` 还没有 `[dependencies]` 节，请先添加，然后列出你想使用的 [crate][def-crate] 名称与版本。下面的例子添加了对 `time` crate 的依赖：

```toml
[dependencies]
time = "0.1.12"
```

版本字符串是 [SemVer] 版本需求。[指定依赖](../../cargo-reference/specifying-dependencies/)文档有更多关于此处可用选项的信息。

[SemVer]: https://semver.org

若还想添加对 `regex` crate 的依赖，无需为列出的每个 crate 都添加 `[dependencies]`。下面是同时依赖 `time` 与 `regex` 时，整个 `Cargo.toml` 文件的样子：

```toml
[package]
name = "hello_world"
version = "0.1.0"
edition = "2024"

[dependencies]
time = "0.1.12"
regex = "0.1.41"
```

重新运行 `cargo build`，Cargo 会获取新依赖及其所有依赖、全部编译它们，并更新 `Cargo.lock`：

```console
$ cargo build
      Updating crates.io index
   Downloading memchr v0.1.5
   Downloading libc v0.1.10
   Downloading regex-syntax v0.2.1
   Downloading memchr v0.1.5
   Downloading aho-corasick v0.3.0
   Downloading regex v0.1.41
     Compiling memchr v0.1.5
     Compiling libc v0.1.10
     Compiling regex-syntax v0.2.1
     Compiling memchr v0.1.5
     Compiling aho-corasick v0.3.0
     Compiling regex v0.1.41
     Compiling hello_world v0.1.0 (file:///path/to/package/hello_world)
```

`Cargo.lock` 包含这些依赖所用的确切修订信息。

现在，即使 `regex` 有了更新，你仍会用同一修订来构建，直到你选择运行 `cargo update`。

现在你可以在 `main.rs` 中使用 `regex` 库了。

```rust,ignore
use regex::Regex;

fn main() {
    let re = Regex::new(r"^\d{4}-\d{2}-\d{2}$").unwrap();
    println!("Did our date match? {}", re.is_match("2014-01-01"));
}
```

运行会显示：

```console
$ cargo run
   Running `target/hello_world`
Did our date match? true
```

[def-crate]:             ../../appendix/01-glossary/#crate             '"crate" (glossary entry)'
[def-package]:           ../../appendix/01-glossary/#package           '"package" (glossary entry)'
[def-package-registry]:  ../../appendix/01-glossary/#package-registry  '"package-registry" (glossary entry)'
