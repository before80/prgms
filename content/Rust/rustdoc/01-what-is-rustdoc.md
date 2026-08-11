+++
title = "01-rustdoc 是什么？"
date = 2026-08-01T07:35:00+08:00
weight = 10
type = "docs"
description = "rustdoc 简介与基本用法"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The rustdoc book](https://doc.rust-lang.org/rustdoc/)

# rustdoc 是什么？ {#what-is-rustdoc}


> 原文链接: [https://doc.rust-lang.org/rustdoc/what-is-rustdoc.html](https://doc.rust-lang.org/rustdoc/what-is-rustdoc.html)


标准 Rust 发行版自带一个名为 `rustdoc` 的工具。它的工作是为 Rust 项目生成文档。从根本上说，rustdoc 接收一个 crate 根或一个 Markdown 文件作为参数，并产出 HTML、CSS 和 JavaScript。

## 基本用法 {#basic-usage}

来试一下！用 Cargo 创建一个新项目：

```bash
$ cargo new docs --lib
$ cd docs
```

在 `src/lib.rs` 中，Cargo 已经生成了一些示例代码。删掉它，换成下面这样：

```rust
/// foo 是一个函数
fn foo() {}
```

接下来对这段代码运行 `rustdoc`。可以用指向 crate 根的路径来调用它，像这样：

```bash
$ rustdoc src/lib.rs
```

这会创建一个名为 `doc` 的新目录，里面是一个网站！在我们的例子中，主页位于 `doc/lib/index.html`。如果用浏览器打开它，你会看到一个带搜索栏的页面，顶部写着 “Crate lib”，但没有任何内容。

你也可以用 `cargo doc` 为整个项目生成文档。参见 [与 Cargo 一起使用 rustdoc](#using-rustdoc-with-cargo)。

## 配置 rustdoc {#configuring-rustdoc}

这里有两个问题：第一，为什么它认为我们的 crate 名叫 “lib”？第二，为什么没有任何内容？

第一个问题是因为 `rustdoc` 想帮你一把；和 `rustc` 一样，它假定 crate 的名字就是 crate 根文件的文件名。要修复这一点，可以传入一个命令行标志：

```bash
$ rustdoc src/lib.rs --crate-name docs
```

现在会生成 `doc/docs/index.html`，页面上显示 “Crate docs.”。

第二个问题是因为我们的函数 `foo` 不是公有的；`rustdoc` 默认只为公有函数生成文档。如果我们改一下代码……

```rust
/// foo 是一个函数
pub fn foo() {}
```

……然后重新运行 `rustdoc`：

```bash
$ rustdoc src/lib.rs --crate-name docs
```

现在就有生成的文档了。打开 `doc/docs/index.html` 看看！它应该会显示指向 `foo` 函数页面的链接，该页面位于 `doc/docs/fn.foo.html`。在那个页面上，你会看到我们写在 crate 文档注释里的 “foo 是一个函数”。

## 与 Cargo 一起使用 rustdoc {#using-rustdoc-with-cargo}

Cargo 也与 `rustdoc` 集成，以便更轻松地生成文档。我们可以不用 `rustdoc` 命令，而是这样做：

```bash
$ cargo doc
```

如果你希望 `cargo` 自动打开生成的文档，可以使用：

```bash
$ cargo doc --open
```

在内部，`cargo doc` 会像这样调用 `rustdoc`：

```bash
$ rustdoc --crate-name docs src/lib.rs -o <path>/docs/target/doc -L
dependency=<path>/docs/target/debug/deps
```

你可以通过 `cargo doc --verbose` 看到这一点。

它会为我们生成正确的 `--crate-name`，并指向 `src/lib.rs`。但那些其它参数呢？
 - `-o` 控制文档的*输出*（*o*utput）位置。注意 Cargo 把生成的文档放在 `target` 下，而不是顶层的 `doc` 目录。在 Cargo 项目中，那是生成文件的惯用位置。
 - `-L` 标志帮助 rustdoc 找到代码所依赖的依赖项。如果我们的项目使用了依赖，也会为它们生成文档！

## 外部与内部文档 {#outer-and-inner-documentation}

`///` 语法用于为紧跟其后的项编写文档。因此它被称为外部文档（outer documentation）。
还有另一种语法：`//!`，用于为它所在的项编写文档。它被称为内部文档（inner documentation）。
在为整个 crate 编写文档时经常会用到它，因为在它前面没有任何东西：它位于 crate 的根部。
所以要为整个 crate 编写文档，需要使用 `//!` 语法。例如：

``` rust
//! 这是我的第一个 rust crate
```

在 crate 根中使用时，它会为它所在的项（也就是 crate 本身）编写文档。

关于 `//!` 语法的更多信息，参见 [The Book][the Book]。

[the Book]: https://doc.rust-lang.org/book/ch14-02-publishing-to-crates-io.html#commenting-contained-items


## 使用独立 Markdown 文件 {#using-standalone-markdown-files}

`rustdoc` 也可以从独立的 Markdown 文件生成 HTML。来试一下：创建一个包含以下内容的 `README.md` 文件：

````text
# 文档

这是一个用于试用 `rustdoc` 的项目。

[这里有一个链接！](https://www.rust-lang.org)

## 示例

```rust
fn foo() -> i32 {
    1 + 1
}
```
````

然后对它调用 `rustdoc`：

```bash
$ rustdoc README.md
```

你会在 `docs/doc/README.html` 中找到由其 Markdown 内容生成的 HTML 文件。

遗憾的是，Cargo 目前还不理解独立的 Markdown 文件。

## 小结 {#summary}

以上覆盖了 `rustdoc` 最简单的用例。本书的其余部分将说明 `rustdoc` 的所有选项，以及如何使用它们。
