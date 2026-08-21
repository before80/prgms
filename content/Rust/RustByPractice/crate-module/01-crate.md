+++
title = "01-包 Crate"
date = 2026-08-12T20:00:00+08:00
weight = 43
type = "docs"
description = "包 Crate — Rust By Practice"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Rust By Practice / Rust 语言实战](https://github.com/sunface/rust-by-practice)

> 原文链接: [https://practice-rust-zh.beatai.org/crate-module/crate.html](https://practice-rust-zh.beatai.org/crate-module/crate.html)

# 包 Crate
`package` 是你通过 `Cargo` 创建的工程或项目，因此在 `package` 的根目录下会有一个 `Cargo.toml` 文件。

1. 🌟 创建一个 `package`，拥有以下目录结构:
```shell
.
├── Cargo.toml
└── src
    └── main.rs

1 directory, 2 files
```

```toml
## in Cargo.toml
[package]
name = "hello-package"
version = "0.1.0"
edition = "2021"
```

> 注意! 我们会在包与模块中使用上面的项目作为演示，因此不要删除

2. 🌟 创建一个 package，拥有以下目录结构:
```shell
.
├── Cargo.toml
└── src
    └── lib.rs

1 directory, 2 files
```

```toml
## in Cargo.toml
[package]
name = "hello-package1"
version = "0.1.0"
edition = "2021"
```

> 该项目可以安全的移除

3. 🌟 
```rust
/* 使用你的答案填空 */

// Q: package 1# 和 2# 的区别是什么 ?
// A: __
```


## 包Crate
一个包可以是二进制也可以一个依赖库。每一个包都有一个包根，例如二进制包的包根是 `src/main.rs`，库包的包根是 `src/lib.rs`。包根是编译器开始处理源代码文件的地方，同时也是包模块树的根部。 

在 package `hello-package` 中，有一个二进制包，该包与 `package` 同名 : `hello-package`,  其中 `src/main.rs` 是该二进制包的包根.

与 `hello-package` 类似, `hello-package1` 同样包含一个包，但是与之前的二进制包不同，该 package 包含的是库包，其中 `src/lib.rs` 是其包根.

4. 🌟
```rust
/* 填空 */

// Q: package `hello-package1` 中的库包名称是?
// A: __
```


5. 🌟🌟 为 `hello-package` 添加一个库包，并且完成以下目录结构的填空:
```shell,editable
## 填空
.
├── Cargo.lock
├── Cargo.toml
├── src
│   ├── __
│   └── __
```

在上一个步骤后，我们的 `hello-package` 中已经存在两个包：一个二进制包和一个库包，两个包的名称都与 package 相同：`hello-package`。



6. 🌟🌟🌟 一个 package 最多只能包含一个库包，但是却可以包含多个二进制包：通过将二进制文件放入到 `src/bin` 目录下实现: **该目录下的每个文件都是一个独立的二进制包，包名与文件名相同，不再与 package 的名称相同。**.

```shell,editable
## 创建一个 a package 包含以下包： 
## 1. 三个二进制包: `hello-package`, `main1` and `main2`
## 2. 一个库包
## 并完成以下目录结构的填空
.
├── Cargo.toml
├── Cargo.lock
├── src
│   ├── __
│   ├── __
│   └── __
│       └── __
│       └── __
├── tests # 存放集成测试文件的目录
│   └── some_integration_tests.rs
├── benches # 存放 benchmark 文件的目录dir for benchmark files
│   └── simple_bench.rs
└── examples # 存放示例文件的目录
    └── simple_example.rs
```

可以看到，上面的 package 结构非常标准，你可以在很多 Rust 项目中看到该结构的身影。


> 你可以在[这里](https://github.com/sunface/rust-by-practice/blob/master/solutions/crate-module/crate.md)找到答案(在 solutions 路径下) 
