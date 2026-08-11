+++
title = "06-抓取示例"
date = 2026-08-01T07:35:00+08:00
weight = 60
type = "docs"
description = "从 crate 中抓取示例代码展示在文档中"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The rustdoc book](https://doc.rust-lang.org/rustdoc/)

# 抓取示例 {#scraped-examples}


> 原文链接: [https://doc.rust-lang.org/rustdoc/scraped-examples.html](https://doc.rust-lang.org/rustdoc/scraped-examples.html)


Rustdoc 有一项不稳定特性：可以自动从 Cargo workspace 的 `examples/` 目录中抓取被文档化项的用法示例。这些示例会包含在该项目生成的文档中。例如，若你的库中有一个公开函数：

```rust,ignore (needs-other-file)
// a_crate/src/lib.rs
pub fn a_func() {}
```

并且你有一个调用该函数的示例：

```rust,ignore (needs-other-file)
// a_crate/examples/ex.rs
fn main() {
  a_crate::a_func();
}
```

那么这段代码片段就会被包含进 `a_func` 的文档中。该文档由 Rustdoc 插入，crate 作者无法手动编辑。


## 如何使用此特性 {#how-to-use-this-feature}

此特性不稳定，可通过向 Rustdoc 传入不稳定标志 `rustdoc-scrape-examples` 启用：

```bash
cargo doc -Zunstable-options -Zrustdoc-scrape-examples
```

若要在 [docs.rs](https://docs.rs) 上启用，请在 Cargo.toml 中加入：

```toml
[package.metadata.docs.rs]
cargo-args = ["-Zunstable-options", "-Zrustdoc-scrape-examples"]
```


## 工作原理 {#how-it-works}

运行 `cargo doc` 时，Rustdoc 会分析所有匹配 Cargo `--examples` 过滤器的 crate，查找被文档化项的用法实例，然后将这些实例的源代码包含进生成的文档中。

Rustdoc 采用若干手段，避免示例淹没读者，也不会让页面体积膨胀：

1. 对给定项，页面最多包含 5 个示例；其余示例仅提供源代码链接。
2. 默认只显示一个示例，其余示例隐藏在折叠控件之后。
3. 对包含示例的给定文件，生成文档时只会纳入包含这些示例的那一项。

对给定项，Rustdoc 会按示例大小排序——较小的示例优先显示。


## 常见问题 {#faq}

### 我的示例没有出现在文档中 {#my-example-is-not-showing-up-in-the-documentation}

此特性使用 Cargo 查找示例的约定。请确认 `cargo check --examples` 会包含你的示例文件。
