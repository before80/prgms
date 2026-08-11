+++
title = "附录E 版本（Editions）"
date = 2026-08-05T08:44:00+08:00
weight = 109
type = "docs"
description = "Rust Edition 的含义、兼容性与升级方式"
isCJKLanguage = true
draft = false
rust_version = "1.97.1"

+++

> 译文 · 基于 [The Rust Programming Language](https://doc.rust-lang.org/stable/book/)（rustc 1.97.1）

# E - 版本（Editions） {#e-editions}


> 原文链接: [https://doc.rust-lang.org/stable/book/appendix-05-editions.html](https://doc.rust-lang.org/stable/book/appendix-05-editions.html)


## 附录 E：版本（Editions）

　　第 1 章里你已经看到，`cargo new` 会在 *Cargo.toml* 里写入一点关于 edition 的元数据。本附录就来说明这是什么意思！

　　Rust 语言与编译器采用六周一次的发布周期，用户能持续获得新功能。其他编程语言往往较少发布、但单次改动更大；Rust 则更频繁地发布较小更新。时间一长，这些细小变化会累积起来。但从一次发布到下一次发布之间，往往很难回头说：“哇，从 Rust 1.10 到 Rust 1.31，Rust 变了好多！”

　　大约每三年，Rust 团队会推出一个新的 Rust *edition*（版本）。每个 edition 把已落地的特性收拢成一套清晰的整体，并配上全面更新的文档与工具链。新 edition 仍随常规的六周发布流程推出。

　　对不同人群，edition 的意义不同：

- 对活跃的 Rust 用户，新 edition 把渐进式改动整理成容易理解的一揽子变化。
- 对尚未使用 Rust 的人，新 edition 标志着一些重大进展已经落地，或许值得再看一眼 Rust。
- 对参与开发 Rust 的人，新 edition 为整个项目提供了一个汇聚点。

　　撰写本书时，可用的 Rust edition 有四个：Rust 2015、Rust 2018、Rust 2021 和 Rust 2024。本书采用 Rust 2024 edition 的惯用法编写。

　　*Cargo.toml* 中的 `edition` 键告诉编译器应按哪个 edition 处理你的代码。若没有该键，出于向后兼容，Rust 会把 edition 当作 `2015`。

　　每个项目都可以选择采用默认 2015 以外的 edition。Edition 可能包含不兼容改动，例如新增与代码中标识符冲突的关键字。但除非你主动选择这些改动，否则即使升级所用的 Rust 编译器版本，代码仍能继续编译。

　　所有 Rust 编译器版本都支持在该编译器发布之前就存在的任何 edition，并且可以把任意受支持 edition 的 crate 链接在一起。Edition 的变化只影响编译器最初解析代码的方式。因此，如果你使用 Rust 2015，而某个依赖使用 Rust 2018，你的项目仍能编译并使用该依赖。反过来——项目用 Rust 2018、依赖用 Rust 2015——同样可以。

　　需要说清楚：大多数特性在所有 edition 上都可用。无论使用哪个 Rust edition，开发者都会随着新的稳定版发布而继续看到改进。不过在某些情况下（主要是新增关键字时），部分新特性可能只在较新的 edition 中可用。若要使用这类特性，就需要切换 edition。

　　更多细节见 [*The Rust Edition Guide*][edition-guide]。那是一本完整的书，列举了各 edition 之间的差异，并说明如何通过 `cargo fix` 自动把代码升级到新 edition。

[edition-guide]: https://doc.rust-lang.org/stable/edition-guide
