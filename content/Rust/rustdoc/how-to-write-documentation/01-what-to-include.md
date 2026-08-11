+++
title = "01-应包含（和排除）什么"
date = 2026-08-01T07:35:00+08:00
weight = 41
type = "docs"
description = "文档应写哪些内容、哪些可省略"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The rustdoc book](https://doc.rust-lang.org/rustdoc/)

# 应包含（和排除）什么 {#what-to-include}


> 原文链接: [https://doc.rust-lang.org/rustdoc/write-documentation/what-to-include.html](https://doc.rust-lang.org/rustdoc/write-documentation/what-to-include.html)


说项目里的一切都必须有文档很容易，而且往往正确，但怎样做到？又有没有本不该写进文档的东西？

在二进制项目的 `src/lib.rs` 或 `main.rs` 文件顶部加入如下属性（attribute）：

```rust
#![warn(missing_docs)]
```

然后运行 `cargo doc` 并查看输出。示例如下：

```text
 Documenting docdemo v0.1.0 (/Users/username/docdemo)
warning: missing documentation for the crate
 --> src/main.rs:1:1
  |
1 | / #![warn(missing_docs)]
2 | |
3 | | fn main() {
4 | |     println!("Hello, world!");
5 | | }
  | |_^
  |
note: the lint level is defined here
 --> src/main.rs:1:9
  |
1 | #![warn(missing_docs)]
  |         ^^^^^^^^^^^^

warning: 1 warning emitted

    Finished dev [unoptimized + debuginfo] target(s) in 2.96s
```

作为库作者，添加 lint `#![deny(missing_docs)]` 是确保项目不会逐渐缺少文档的好办法；`#![warn(missing_docs)]` 则是迈向全面文档的好起点。

后续章节 [rustdoc 专用 lint][rustdoc-lints] 中还有更多 lint。

## 示例 {#examples}

当然这个例子被刻意简化了，但文档的一部分力量在于展示易于跟上的代码，而不必追求完全贴近真实用法。文档常在错误处理上走捷径，因为完整设置会让一个简单示例变得很难跟读。

`Async` 就是很好的例子。要执行 `async` 示例，需要有执行器。示例往往会省略这一点，留给用户自己把 `async` 代码放进自己的运行时。

更推荐在示例中不要使用 `unwrap()`；若某些错误处理会让示例太难跟上，也可以将其隐藏。

``````text
/// 示例
/// ```rust
/// let fourtytwo = "42".parse::<u32>()?;
/// println!("{} + 10 = {}", fourtytwo, fourtytwo+10);
/// ```
``````

当 rustdoc 把它包进 `main` 函数时，会因 `?` 返回了带有 `ParseIntError` 的 `Result`、而默认的 `main` 无法处理该错误而编译失败。为了同时帮助读者和测试套件，这个示例需要一些额外代码：

``````text
/// 示例
/// ```rust
/// # fn main() -> Result<(), std::num::ParseIntError> {
/// let fortytwo = "42".parse::<u32>()?;
/// println!("{} + 10 = {}", fortytwo, fortytwo+10);
/// #     Ok(())
/// # }
/// ```
``````

在文档页面上示例看起来一样，但任何想使用你的 crate 的人都能拿到这些额外信息。关于测试的更多内容见后续的[文档测试][Documentation tests]章节。

## 应排除什么 {#what-to-exclude}

公开接口的某些部分默认会出现在 rustdoc 输出中。属性 `#[doc(hidden)]` 可以隐藏实现细节，以鼓励对 crate 的惯用法。

例如，某个让 crate 更易实现的内部 `macro!` 若出现在公开文档中，可能成为用户的陷阱。可能存在内部 `Error` 类型，且 `impl` 细节应隐藏，详见 [API Guidelines]。

## 自定义输出 {#customizing-the-output}

可以向 `rustdoc` 传入自定义 css 文件来为文档设置样式。

```bash
rustdoc --extend-css custom.css src/lib.rs
```

用该功能做深色主题的一个好例子记录在[这篇博客][on this blog]。请记住，rustdoc 输出已内置深色主题，点击右上角齿轮图标即可。为主题添加额外选项很简单：创建一个自定义主题 `.css` 文件，并使用如下语法：

```bash
rustdoc --theme awesome.css src/lib.rs
```

这里有一个新主题示例：[Ayu]。

[Ayu]: https://github.com/rust-lang/rust/blob/HEAD/src/librustdoc/html/static/css/rustdoc.css#L2384-L2574
[API Guidelines]: https://rust-lang.github.io/api-guidelines/documentation.html#rustdoc-does-not-show-unhelpful-implementation-details-c-hidden
[Documentation tests]: 05-documentation-tests/
[on this blog]: https://blog.guillaume-gomez.fr/articles/2016-09-16+Generating+doc+with+rustdoc+and+a+custom+theme
[rustdoc-lints]: ../05-rustdoc-specific-lints/
