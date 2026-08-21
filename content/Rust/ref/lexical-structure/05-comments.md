+++
title = "05-注释"
date = 2026-08-18T08:45:00+08:00
weight = 9
type = "docs"
description = "注释 — The Rust Reference"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Reference](https://doc.rust-lang.org/reference/)

> 原文链接: [https://doc.rust-lang.org/reference/comments.html](https://doc.rust-lang.org/reference/comments.html)

r[comments]
# 注释

r[comments.syntax]
```grammar,lexer
@root COMMENT ->
      LINE_COMMENT
    | INNER_LINE_DOC
    | OUTER_LINE_DOC
    | INNER_BLOCK_DOC
    | OUTER_BLOCK_DOC
    | BLOCK_COMMENT

LINE_COMMENT ->
      `//` (~[`/` `!` LF] | `//`) ~LF*
    | `//` EOF
    | `//` _immediately followed by LF_

BLOCK_COMMENT ->
    `/*` ^
      ( BLOCK_COMMENT_OR_DOC | (!`*/` CHAR) )*
    `*/`

INNER_LINE_DOC ->
    `//!` ^ LINE_DOC_COMMENT_CONTENT (LF | EOF)

LINE_DOC_COMMENT_CONTENT -> (!CR ~LF)*

INNER_BLOCK_DOC ->
    `/*!` ^ ( BLOCK_COMMENT_OR_DOC | BLOCK_CHAR )* `*/`

OUTER_LINE_DOC ->
    `///` ^ LINE_DOC_COMMENT_CONTENT (LF | EOF)

OUTER_BLOCK_DOC ->
    `/**` ![`*` `/`]
      ^
      ( ~`*` | BLOCK_COMMENT_OR_DOC )
      ( BLOCK_COMMENT_OR_DOC | BLOCK_CHAR )*
    `*/`

BLOCK_CHAR -> (!(`*/` | CR) CHAR)

BLOCK_COMMENT_OR_DOC ->
      INNER_BLOCK_DOC
    | OUTER_BLOCK_DOC
    | BLOCK_COMMENT
```

r[comments.normal]
## 非文档注释

注释遵循一般的 C++ 风格：行注释（`//`）与块注释（`/* ... */`）形式。支持嵌套块注释。

r[comments.normal.tokenization]
非文档注释被解释为一种空白。

r[comments.doc]
## 文档注释

r[comments.doc.syntax]
以恰好 *三个* 斜杠（`///`）开头的行文档注释，以及块文档注释（`/** ... */`），二者都是外部文档注释，被解释为 [`doc` 属性][`doc` attributes] 的特殊语法。

r[comments.doc.attributes]
也就是说，它们等价于在注释体周围书写 `#[doc="..."]`，即 `/// Foo` 变成 `#[doc=" Foo"]`，`/** Bar */` 变成 `#[doc=" Bar "]`。因此它们必须出现在接受外部属性的对象之前。

r[comments.doc.inner-syntax]
以 `//!` 开头的行注释以及块注释 `/*! ... */` 是应用于注释之父级（而非其后的项）的文档注释。

r[comments.doc.inner-attributes]
也就是说，它们等价于在注释体周围书写 `#![doc="..."]`。`//!` 注释通常用于为占据一个源文件的模块编写文档。

r[comments.doc.bare-crs]
文档注释中不允许字符 `U+000D`（CR）。

> **注意**
> 按惯例，文档注释包含 Markdown，这是 `rustdoc` 所期望的。然而，注释语法并不尊重任何内部 Markdown。``/** `glob = "*/*.rs";` */`` 会在第一个 `*/` 处终止注释，剩余代码将导致语法错误。这使块文档注释的内容相对于行文档注释略受限制。

> **注意**
> 紧跟着 `U+000A`（LF）的序列 `U+000D`（CR）此前已被变换为单个 `U+000A`（LF）。

## 示例

```rust
//! 应用于本 crate 隐式匿名模块的文档注释

pub mod outer_module {

    //!  - 内部行文档注释
    //!! - 仍是内部行文档注释（但开头带一个感叹号）

    /*!  - 内部块文档注释 */
    /*!! - 仍是内部块文档注释（但开头带一个感叹号） */

    //   - 只是注释
    ///  - 外部行文档注释（恰好 3 个斜杠）
    //// - 只是注释

    /*   - 只是注释 */
    /**  - 外部块文档注释（恰好）2 个星号 */
    /*** - 只是注释 */

    pub mod inner_module {}

    pub mod nested_comments {
        /* 在 Rust 中 /* 我们可以 /* 嵌套注释 */ */ */

        // 全部三种块注释都可以包含其他类型，
        // 或嵌套在其他类型之中：

        /*   /* */  /** */  /*! */  */
        /*!  /* */  /** */  /*! */  */
        /**  /* */  /** */  /*! */  */
        pub mod dummy_item {}
    }

    pub mod degenerate_cases {
        // 空的内部行文档注释
        //!

        // 空的内部块文档注释
        /*!*/

        // 空的行注释
        //

        // 空的外部行文档注释
        ///

        // 空的块注释
        /**/

        pub mod dummy_item {}

        // 空的 2 星号块不是文档块，而是块注释
        /***/

    }

    /* 下一个不被允许，因为外部文档注释
       需要有一个将接收该文档的项 */

    /// 我的项在哪里？
##   mod boo {}
}
```

[`doc` attributes]: ../rustdoc/the-doc-attribute.html
