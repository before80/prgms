+++
title = "第9章 仅 Nightly 的语法"
date = 2026-08-18T22:00:00+08:00
weight = 100
type = "docs"
description = "仅 Nightly 的语法 — The Rust Style Guide"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Style Guide](https://doc.rust-lang.org/nightly/style-guide/)

> 原文链接: [https://doc.rust-lang.org/nightly/style-guide/nightly.html](https://doc.rust-lang.org/nightly/style-guide/nightly.html)

# 仅 Nightly 的语法

本章记录仅 nightly 语法的风格与格式。风格指南的其余部分记录稳定版 Rust 语法的风格；nightly 语法只出现在本章。此处每一节都包含特性开关的名称，以便在 Rust 仓库中搜索（例如 `git grep`）某项 nightly 特性时，也能找到对应的风格指南章节。

仅 nightly 语法的风格与格式应在稳定化时从本章移除，并并入风格指南的相应章节。

与风格指南的其余部分不同，本章不保证稳定性。关于对本章的破坏性变更，请参阅风格团队针对 nightly 格式化流程的政策。

### Frontmatter（文件头） {#frontmatter}

*位置：放在[根模块](../introduction/)中注释与属性之前。*

*跟踪 issue：[#136889](https://github.com/rust-lang/rust/issues/136889)*

*特性开关：`frontmatter`*

frontmatter 与文件开头或 shebang 之间不应有空行。
frontmatter 与其后任何内容之间可以有零行或一行。

frontmatter 围栏应使用容纳其中内容所需的最少短横线数量（比内容中最长的起始短横线序列多一条，最少为 3 条才能被识别为 frontmatter 分隔符）。
若开始围栏后带有 infostring，两者之间应有一个空格。
frontmatter 围栏行不应有尾随空白。

```rust
#!/usr/bin/env cargo
--- cargo
[dependencies]
regex = "1"
---

fn main() {}
```
