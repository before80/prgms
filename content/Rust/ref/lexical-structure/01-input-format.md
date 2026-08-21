+++
title = "01-输入格式"
date = 2026-08-18T08:45:00+08:00
weight = 5
type = "docs"
description = "输入格式 — The Rust Reference"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Reference](https://doc.rust-lang.org/reference/)

> 原文链接: [https://doc.rust-lang.org/reference/input-format.html](https://doc.rust-lang.org/reference/input-format.html)

r[input]
# 输入格式

r[input.syntax]
```grammar,lexer
CHAR -> [U+0000-U+D7FF U+E000-U+10FFFF] // Unicode 标量值

ASCII -> [U+0000-U+007F]

NUL -> U+0000

EOF -> !CHAR  // 文件或输入结束
```

r[input.intro]
本章描述如何将源文件解释为 token 序列。

程序如何组织到文件中，见 [Crate 与源文件][Crates and source files]。

r[input.encoding]
## 源编码

r[input.encoding.utf8]
每个源文件都被解释为以 UTF-8 编码的 Unicode 字符序列。

r[input.encoding.invalid]
若文件不是合法 UTF-8，则为错误。

r[input.byte-order-mark]
## 字节序标记的移除

若序列中的第一个字符是 `U+FEFF`（[字节序标记][BYTE ORDER MARK]），则将其移除。

r[input.crlf]
## CRLF 规范化

每一对紧接着的 `U+000D`（CR）后跟 `U+000A`（LF）的字符，都替换为单个 `U+000A`（LF）。这只发生一次，不会反复进行，因此规范化之后，输入中仍可能存在紧跟着 `U+000A`（LF）的 `U+000D`（CR）（例如，若原始输入包含 “CR CR LF LF”）。

字符 `U+000D`（CR）的其他出现保持原位（它们被当作 [空白][whitespace] 处理）。

r[input.shebang]
## Shebang 的移除

r[input.shebang.removal]
若存在 [shebang]，则将其从输入序列中移除（因此会被忽略）。

r[input.tokenization]
## 词法分析

随后，得到的字符序列按本章其余部分所述转换为 token。

> **注意**
> 标准库的 [`include!`] 宏对其读取的文件应用下列变换：
>
> - 字节序标记的移除。
> - CRLF 规范化。
> - 在项（item）上下文中调用时移除 shebang（与表达式或语句上下文相对）。
>
> [`include_str!`] 和 [`include_bytes!`] 宏不应用这些变换。

[BYTE ORDER MARK]: https://en.wikipedia.org/wiki/Byte_order_mark#UTF-8
[Crates and source files]: crates-and-source-files.md
[shebang]: shebang.md
[whitespace]: whitespace.md
