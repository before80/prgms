+++
title = "05-包布局"
date = 2026-07-30T14:49:00+08:00
weight = 25
type = "docs"
description = "Cargo 包的标准目录与文件布局"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Cargo Book](https://doc.rust-lang.org/cargo/)

# 包布局 {#package-layout}


> 原文链接: [https://doc.rust-lang.org/cargo/guide/project-layout.html](https://doc.rust-lang.org/cargo/guide/project-layout.html)


Cargo 对文件放置有约定，便于你快速上手一个新的 Cargo [包][def-package]：

```text
.
├── Cargo.lock
├── Cargo.toml
├── src/
│   ├── lib.rs
│   ├── main.rs
│   └── bin/
│       ├── named-executable.rs
│       ├── another-executable.rs
│       └── multi-file-executable/
│           ├── main.rs
│           └── some_module.rs
├── benches/
│   ├── large-input.rs
│   └── multi-file-bench/
│       ├── main.rs
│       └── bench_module.rs
├── examples/
│   ├── simple.rs
│   └── multi-file-example/
│       ├── main.rs
│       └── ex_module.rs
└── tests/
    ├── some-integration-tests.rs
    └── multi-file-test/
        ├── main.rs
        └── test_module.rs
```

* `Cargo.toml` 与 `Cargo.lock` 存放在包的根目录（*包根*）。
* 源代码放在 `src` 目录中。
* 默认库文件是 `src/lib.rs`。
* 默认可执行文件是 `src/main.rs`。
    * 其他可执行文件可放在 `src/bin/` 中。
* 基准测试放在 `benches` 目录中。
* 示例放在 `examples` 目录中。
* 集成测试放在 `tests` 目录中。

若二进制、示例、基准测试或集成测试由多个源文件组成，请在 `src/bin`、`examples`、`benches` 或 `tests` 目录的子目录中放置一个 `main.rs`，连同额外的[*模块（module）*][def-module]。可执行文件的名称即为该子目录名。

> **注意：** 按约定，二进制、示例、基准测试与集成测试遵循 `kebab-case` 命名风格，除非有兼容性理由另做处理（例如与既有二进制名称兼容）。这些目标内的模块采用 `snake_case`，遵循 [Rust 标准](https://rust-lang.github.io/rfcs/0430-finalizing-naming-conventions.html)。

你可以在[《Rust 程序设计语言》][book-modules]中了解更多关于 Rust 模块系统的内容。

关于手动配置目标的更多细节，参见[配置目标][Configuring a target]。关于控制 Cargo 如何自动推断目标名称的更多信息，参见[目标自动发现][Target auto-discovery]。

[book-modules]: https://doc.rust-lang.org/book/ch07-00-managing-growing-projects-with-packages-crates-and-modules.html
[Configuring a target]: ../../cargo-reference/the-manifest-format/01-cargo-targets/#configuring-a-target
[def-package]:           ../../appendix/01-glossary/#package          '"package" (glossary entry)'
[def-module]:            ../../appendix/01-glossary/#module           '"module" (glossary entry)'
[Target auto-discovery]: ../../cargo-reference/the-manifest-format/01-cargo-targets/#target-auto-discovery
