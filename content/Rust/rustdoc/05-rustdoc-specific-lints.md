+++
title = "05-rustdoc 专用 lint"
date = 2026-08-01T07:35:00+08:00
weight = 50
type = "docs"
description = "rustdoc 提供的专用 lint"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The rustdoc book](https://doc.rust-lang.org/rustdoc/)

# rustdoc 专用 lint {#lints}


> 原文链接: [https://doc.rust-lang.org/rustdoc/lints.html](https://doc.rust-lang.org/rustdoc/lints.html)


`rustdoc` 提供了一些 lint，帮助你编写和测试文档。你可以像使用其他 lint 一样使用它们：

```rust
#![allow(rustdoc::broken_intra_doc_links)] // 允许该 lint，不会报告任何诊断
#![warn(rustdoc::broken_intra_doc_links)] // 若存在损坏的文档内链接则警告
#![deny(rustdoc::broken_intra_doc_links)] // 若存在损坏的文档内链接则报错
```

注意，除了 `missing_docs` 之外，这些 lint 仅在运行 `rustdoc` 时可用，在 `rustc` 中不可用。

以下是 `rustdoc` 提供的 lint 列表：

## `broken_intra_doc_links`

此 lint **默认警告（warn）**。它会检测[文档内链接]无法解析的情况。例如：

[文档内链接]: how-to-write-documentation/04-linking-to-items-by-name/

```rust
/// 我想链接到 [`Nonexistent`]，但它不存在！
pub fn foo() {}
```

你会收到如下警告：

```text
warning: unresolved link to `Nonexistent`
 --> test.rs:1:24
  |
1 | /// I want to link to [`Nonexistent`] but it doesn't exist!
  |                        ^^^^^^^^^^^^^ no item named `Nonexistent` in `test`
```

当存在歧义时，它也会发出警告，并建议如何消歧：

```rust
/// [`Foo`]
pub fn function() {}

pub enum Foo {}

pub fn Foo(){}
```

```text
warning: `Foo` is both an enum and a function
 --> test.rs:1:6
  |
1 | /// [`Foo`]
  |      ^^^^^ ambiguous link
  |
  = note: `#[warn(rustdoc::broken_intra_doc_links)]` on by default
help: to link to the enum, prefix with the item type
  |
1 | /// [`enum@Foo`]
  |      ^^^^^^^^^^
help: to link to the function, add parentheses
  |
1 | /// [`Foo()`]
  |      ^^^^^^^

```

## `private_intra_doc_links`

此 lint **默认警告（warn）**。它会检测从公开项指向私有项的[文档内链接]。例如：

```rust
#![warn(rustdoc::private_intra_doc_links)] // 注：多余——默认即为 warn

/// [private]
pub fn public() {}
fn private() {}
```

这会给出警告，说明该链接出现在文档中时将会损坏：

```text
warning: public documentation for `public` links to private item `private`
 --> priv.rs:1:6
  |
1 | /// [private]
  |      ^^^^^^^ this item is private
  |
  = note: `#[warn(rustdoc::private_intra_doc_links)]` on by default
  = note: this link will resolve properly if you pass `--document-private-items`
```

注意：是否传入 `--document-private-items`，行为会有所不同！
若你为私有项生成文档，即便有警告，它仍会生成链接：

```text
warning: public documentation for `public` links to private item `private`
 --> priv.rs:1:6
  |
1 | /// [private]
  |      ^^^^^^^ this item is private
  |
  = note: `#[warn(rustdoc::private_intra_doc_links)]` on by default
  = note: this link resolves only because you passed `--document-private-items`, but will break without
```

[文档内链接]: how-to-write-documentation/04-linking-to-items-by-name/

## `missing_docs`

此 lint **默认允许（allow）**。它会检测缺少文档的项。例如：

```rust
#![warn(missing_docs)]

pub fn undocumented() {}
# fn main() {}
```

随后，`undocumented` 函数会收到如下警告：

```text
warning: missing documentation for a function
  --> your-crate/lib.rs:3:1
   |
 3 | pub fn undocumented() {}
   | ^^^^^^^^^^^^^^^^^^^^^
```

注意：与其他 rustdoc lint 不同，此 lint 也可直接从 `rustc` 使用。

## `missing_crate_level_docs`

此 lint **默认允许（allow）**。它会检测 crate 根是否缺少文档。例如：

```rust
#![warn(rustdoc::missing_crate_level_docs)]
```

这将生成如下警告：

```text
warning: no documentation found for this crate's top-level module
  |
  = help: The following guide may be of use:
          https://doc.rust-lang.org/nightly/rustdoc/how-to-write-documentation.html
```

目前默认是 “allow”，但计划将来改为警告。用意是引导新用户了解*如何*为 crate 编写文档，把他们指向一些入门说明，同时避免像 `missing_docs` 那样产生铺天盖地的警告。

## `missing_doc_code_examples`

此 lint **默认允许（allow）**，且**仅 nightly 可用**。它会检测文档块是否缺少代码示例。例如：

```rust
#![warn(rustdoc::missing_doc_code_examples)]

/// 没有代码示例！
pub fn no_code_example() {}
# fn main() {}
```

随后，`no_code_example` 函数会收到如下警告：

```text
warning: Missing code example in this documentation
  --> your-crate/lib.rs:3:1
   |
LL | /// There is no code example!
   | ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
```

要消除该 lint，需要在文档块中加入代码示例：

```rust
/// 没有代码示例！
///
/// ```
/// println!("calling no_code_example...");
/// no_code_example();
/// println!("we called no_code_example!");
/// ```
pub fn no_code_example() {}
```

以下项不会触发此 lint：

 * impl 块（trait 与固有 impl）
 * 枚举变体
 * 结构体/联合体字段
 * 类型别名，包括关联类型
 * 静态项/常量
 * 模块（包括 crate 的顶层模块）
 * 通过重导出引入的外部项（函数、静态项、类型等）

## `private_doc_tests`

此 lint **默认允许（allow）**。它会检测位于私有项上的文档测试。例如：

```rust
#![warn(rustdoc::private_doc_tests)]

mod foo {
    /// 私有文档测试
    ///
    /// ```
    /// assert!(false);
    /// ```
    fn bar() {}
}
# fn main() {}
```

将得到：

```text
warning: Documentation test in private item
  --> your-crate/lib.rs:4:1
   |
 4 | /     /// private doc test
 5 | |     ///
 6 | |     /// ```
 7 | |     /// assert!(false);
 8 | |     /// ```
   | |___________^
```

## `invalid_codeblock_attributes`

此 lint **默认警告（warn）**。它会检测文档示例中代码块属性可能存在的拼写错误。例如：

```rust
#![warn(rustdoc::invalid_codeblock_attributes)]  // 注：多余——默认即为 warn

/// 示例。
///
/// ```should-panic
/// assert_eq!(1, 2);
/// ```
pub fn foo() {}
```

将得到：

```text
warning: unknown attribute `should-panic`. Did you mean `should_panic`?
 --> src/lib.rs:1:1
  |
1 | / /// Example.
2 | | ///
3 | | /// ```should-panic
4 | | /// assert_eq!(1, 2);
5 | | /// ```
  | |_______^
  |
  = note: `#[warn(rustdoc::invalid_codeblock_attributes)]` on by default
  = help: the code block will either not be tested if not marked as a rust one or won't fail if it doesn't panic when running
```

在上面的例子中，正确写法是 `should_panic`。这有助于发现一些常见属性的拼写错误。

## `invalid_html_tags`

此 lint **默认警告（warn）**。它会检测未闭合或无效的 HTML 标签。例如：

```rust
#![warn(rustdoc::invalid_html_tags)]

/// <h1>
/// </script>
pub fn foo() {}
```

将得到：

```text
warning: unopened HTML tag `script`
 --> foo.rs:1:1
  |
1 | / /// <h1>
2 | | /// </script>
  | |_____________^
  |
  note: the lint level is defined here
 --> foo.rs:1:9
  |
1 | #![warn(rustdoc::invalid_html_tags)]
  |         ^^^^^^^^^^^^^^^^^^^^^^^^^^

warning: unclosed HTML tag `h1`
 --> foo.rs:1:1
  |
1 | / /// <h1>
2 | | /// </script>
  | |_____________^

warning: 2 warnings emitted
```

## `invalid_rust_codeblocks`

此 lint **默认警告（warn）**。它会检测文档示例中无效的 Rust 代码块（例如为空、无法解析为 Rust）。例如：

```rust
/// 空代码块（带与不带 `rust` 标记）：
///
/// ```rust
/// ```
///
/// 代码块中的无效语法：
///
/// ```rust
/// '<
/// ```
pub fn foo() {}
```

将得到：

```text
warning: Rust code block is empty
 --> lint.rs:3:5
  |
3 |   /// ```rust
  |  _____^
4 | | /// ```
  | |_______^
  |
  = note: `#[warn(rustdoc::invalid_rust_codeblocks)]` on by default

warning: could not parse code block as Rust code
  --> lint.rs:8:5
   |
8  |   /// ```rust
   |  _____^
9  | | /// '<
10 | | /// ```
   | |_______^
   |
   = note: error from rustc: unterminated character literal
```

## `bare_urls`

此 lint **默认警告（warn）**。它会检测不是链接的 URL。例如：

```rust
#![warn(rustdoc::bare_urls)] // 注：多余——默认即为 warn

/// http://example.org
/// [http://example.net]
pub fn foo() {}
```

将得到：

```text
warning: this URL is not a hyperlink
 --> links.rs:1:5
  |
1 | /// http://example.org
  |     ^^^^^^^^^^^^^^^^^^ help: use an automatic link instead: `<http://example.org>`
  |
  = note: `#[warn(rustdoc::bare_urls)]` on by default

warning: this URL is not a hyperlink
 --> links.rs:3:6
  |
3 | /// [http://example.net]
  |      ^^^^^^^^^^^^^^^^^^ help: use an automatic link instead: `<http://example.net>`

warning: 2 warnings emitted
```

## `unescaped_backticks`

此 lint **默认允许（allow）**。它会检测未转义的反引号（\`）。这通常意味着行内代码写坏了。例如：

```rust
#![warn(rustdoc::unescaped_backticks)]

/// `add(a, b) 与 `add(b, a)` 相同。
pub fn add(a: i32, b: i32) -> i32 { a + b }
```

将得到：

```text
warning: unescaped backtick
 --> src/lib.rs:3:41
  |
3 | /// `add(a, b) is the same as `add(b, a)`.
  |                                         ^
  |
note: the lint level is defined here
 --> src/lib.rs:1:9
  |
1 | #![warn(rustdoc::unescaped_backticks)]
  |         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
help: a previous inline code might be longer than expected
  |
3 | /// `add(a, b)` is the same as `add(b, a)`.
  |               +
help: if you meant to use a literal backtick, escape it
  |
3 | /// `add(a, b) is the same as `add(b, a)\`.
  |                                         +

warning: 1 warning emitted
```

## `redundant_explicit_links`

此 lint **默认警告（warn）**。它会检测与自动计算链接相同的显式链接。
这通常意味着这些显式链接可以删除。例如：

```rust
#![warn(rustdoc::redundant_explicit_links)] // 注：多余——默认即为 warn

/// add 接受 2 个 [`usize`](usize) 并对它们做加法，
/// 然后返回结果。
pub fn add(left: usize, right: usize) -> usize {
    left + right
}
```

将得到：

```text
error: redundant explicit rustdoc link
  --> src/lib.rs:3:27
   |
3  | /// add takes 2 [`usize`](usize) and performs addition
   |                           ^^^^^
   |
   = note: Explicit link does not affect the original link
note: the lint level is defined here
  --> src/lib.rs:1:9
   |
1  | #![deny(rustdoc::redundant_explicit_links)]
   |         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
   = help: Remove explicit link instead
```
