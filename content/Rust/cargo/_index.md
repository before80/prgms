+++
title = "Cargo手册"
date = 2026-07-30T14:49:00+08:00
weight = 1
type = "docs"
description = "Cargo 手册导读：包管理器简介与各章节导航"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Cargo Book](https://doc.rust-lang.org/cargo/)

# Cargo 手册 {#the-cargo-book}


> 原文链接: [https://doc.rust-lang.org/cargo/index.html](https://doc.rust-lang.org/cargo/index.html)


![Cargo Logo](images/Cargo-Logo-Small.png)

Cargo 是 [Rust] 的[包管理器（package manager）][def-package-manager]。Cargo 会下载你的 Rust [包（package）][def-package]的依赖、编译包、制作可分发的包，并将它们上传到 [crates.io]——Rust 社区的[包注册表（package registry）][def-package-registry]。你可以在 [GitHub] 上为本手册做出贡献。

## 章节 {#sections}
**[入门指南](getting-started/)**

要开始使用 Cargo，请安装 Cargo（以及 Rust），并创建你的第一个 [*crate*][def-crate]。

**[Cargo 指南](cargo-guide/)**

本指南会介绍用 Cargo 开发 Rust 包所需的全部知识。

**[Cargo 参考](cargo-reference/)**

参考文档涵盖 Cargo 各领域细节。

**[Cargo 命令](cargo-commands/)**

命令章节介绍如何通过命令行接口与 Cargo 交互。

**[常见问题](05-faq/)**

**附录：**
* [术语表](appendix/01-glossary/)
* [Git 身份验证](appendix/02-git-authentication/)

**其他文档：**
* [更新日志](06-changelog/)
  --- 各版本 Cargo 变更的详细说明。
* [Rust 文档网站](https://doc.rust-lang.org/) --- 官方 Rust 文档与工具的链接。

[def-crate]: appendix/01-glossary/#crate            '"crate" (glossary entry)'
[def-package]: appendix/01-glossary/#package          '"package" (glossary entry)'
[def-package-manager]: appendix/01-glossary/#package-manager  '"package manager" (glossary entry)'
[def-package-registry]: appendix/01-glossary/#package-registry '"package registry" (glossary entry)'
[rust]: https://www.rust-lang.org/
[crates.io]: https://crates.io/
[GitHub]: https://github.com/rust-lang/cargo/tree/master/doc/book
