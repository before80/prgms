+++
title = "06-空白"
date = 2026-08-18T08:45:00+08:00
weight = 10
type = "docs"
description = "空白 — The Rust Reference"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Reference](https://doc.rust-lang.org/reference/)

> 原文链接: [https://doc.rust-lang.org/reference/whitespace.html](https://doc.rust-lang.org/reference/whitespace.html)

r[lex.whitespace]
# 空白

r[whitespace.syntax]
```grammar,lexer
WHITESPACE ->
      U+0009 // 水平制表符，`'\t'`
    | U+000A // 换行，`'\n'`
    | U+000B // 垂直制表符
    | U+000C // 换页
    | U+000D // 回车，`'\r'`
    | U+0020 // 空格，`' '`
    | U+0085 // 下一行
    | U+200E // 从左至右标记
    | U+200F // 从右至左标记
    | U+2028 // 行分隔符
    | U+2029 // 段分隔符

TAB -> U+0009 // 水平制表符，`'\t'`

LF -> U+000A  // 换行，`'\n'`

CR -> U+000D  // 回车，`'\r'`
```

r[lex.whitespace.intro]
空白是任何非空、且仅包含具有 [`Pattern_White_Space`] Unicode 属性的字符的字符串。

r[lex.whitespace.token-sep]
Rust 是一门“自由格式”语言，这意味着所有形式的空白只用于在文法中分隔 *token*，没有语义上的意义。

r[lex.whitespace.replacement]
若将每个空白元素替换为任何其他合法空白元素（例如单个空格字符），Rust 程序的含义相同。

[`Pattern_White_Space`]: https://www.unicode.org/reports/tr31/
