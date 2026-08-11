+++
title = "3 对比 Chromium 与 Cargo 生态"
date = 2026-08-11T11:30:00+08:00
weight = 258
type = "docs"
description = "03-对比 Chromium 与 Cargo 生态 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/chromium/cargo.html](https://google.github.io/comprehensive-rust/chromium/cargo.html)

# 3 对比 Chromium 与 Cargo 生态

Rust 社区通常使用 `cargo` 以及来自 [crates.io][2] 的库。Chromium 使用 `gn` 与 `ninja` 构建，并采用一组经过筛选的依赖。

用 Rust 写代码时，你的选择是：

- 借助 `//build/rust/*.gni` 中的模板（例如稍后会见到的 `rust_static_library`）使用 `gn` 与 `ninja`。这会使用 Chromium 审计过的工具链与 crate。
- 使用 `cargo`，但[把自己限制在 Chromium 审计过的工具链与 crate][0]
- 使用 `cargo`，信任从互联网下载的[工具链][1]和/或[crate][2]

从这里起我们将聚焦 `gn` 与 `ninja`，因为这是把 Rust 代码构建进 Chromium 浏览器的方式。与此同时，Cargo 是 Rust 生态的重要部分，你应把它留在工具箱里。

## 小练习

分成小组并：

- 头脑风暴 `cargo` 可能具有优势的场景，并评估这些场景的风险概况。
- 讨论使用 `gn` 与 `ninja`、离线 `cargo` 等时，需要信任哪些工具、库与人群。

> 请学员在完成练习前避免偷看讲师备注。假设参加课程的人在物理上在一起，请他们分成 3–4 人的小组讨论。
>
> 与练习第一部分相关的笔记/提示（“Cargo 可能具有优势的场景”）：
>
> - 写工具或原型化 Chromium 的一部分时，能访问 crates.io 丰富的库生态非常棒。几乎任何事都有对应的 crate，而且通常用起来很愉快。（`clap` 用于命令行解析，`serde` 用于与各种格式之间的序列化/反序列化，`itertools` 用于处理迭代器，等等。）
>
>   - `cargo` 让试用一个库很容易（只需在 `Cargo.toml` 加一行就开始写代码）
>   - 或许值得比较 CPAN 如何帮助让 `perl` 成为流行选择，或与 `python` + `pip` 比较。
>
> - 开发体验不仅由核心 Rust 工具（例如用 `rustup` 切换到不同 `rustc` 版本以测试需要在 nightly、当前 stable 与更旧 stable 上工作的 crate）造就，也由第三方工具生态造就（例如 Mozilla 提供 `cargo vet` 以简化并共享安全审计；`criterion` crate 提供精简的基准测试方式）。
>
>   - `cargo` 让添加工具很容易：`cargo install --locked cargo-vet`。
>   - 或许值得与 Chrome Extensions 或 VScode extensions 比较。
>
> - `cargo` 可能是正确选择的宽泛、通用项目示例：
>
>   - 或许令人惊讶，Rust 在业界写命令行工具方面越来越受欢迎。库的广度与人体工程学可与 Python 媲美，同时更稳健（得益于丰富的类型系统）且运行更快（作为编译语言而非解释语言）。
>   - 参与 Rust 生态需要使用 Cargo 等标准 Rust 工具。希望获得外部贡献、并希望在 Chromium 之外使用（例如在 Bazel 或 Android/Soong 构建环境中）的库应使用 Cargo。
>
> - 基于 `cargo` 的 Chromium 相关项目示例：
>   - `serde_json_lenient`（Google 其他部分做过实验，带来了性能改进的 PR）
>   - 像 `font-types` 这样的 Fontations 库
>   - `gnrt` 工具（课程稍后会见到），它依赖 `clap` 做命令行解析、依赖 `toml` 处理配置文件。
>     - 免：使用 `cargo` 的一个独特原因是：在构建 Rust 工具链时构建并引导 Rust 标准库时，`gn` 不可用。
>     - `run_gnrt.py` 使用 Chromium 自带的 `cargo` 与 `rustc`。`gnrt` 依赖从互联网下载的第三方库，但 `run_gnrt.py` 通过 `Cargo.lock` 要求 `cargo` 只允许 `--locked` 内容。）
>
> 学员可能识别出以下被隐式或显式信任的项：
>
> - `rustc`（Rust 编译器），它又依赖 LLVM 库、Clang 编译器、`rustc` 源码（从 GitHub 获取，由 Rust 编译器团队审查）、用于引导的二进制 Rust 编译器
> - `rustup`（值得指出 `rustup` 在 https://github.com/rust-lang/ 组织下开发——与 `rustc` 相同）
> - `cargo`、`rustfmt` 等
> - 各种内部基础设施（构建 `rustc` 的 bot、向 Chromium 工程师分发预构建工具链的系统等）
> - 像 `cargo audit`、`cargo vet` 等 Cargo 工具
> - vendored 到 `//third_party/rust` 的 Rust 库（由 security@chromium.org 审计）
> - 其他 Rust 库（有些小众，有些相当流行且常用）


[0]: https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/rust.md#Using-cargo
[1]: https://rustup.rs/
[2]: https://crates.io/
