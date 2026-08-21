+++
title = "02-Shebang"
date = 2026-08-18T08:45:00+08:00
weight = 6
type = "docs"
description = "Shebang — The Rust Reference"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Reference](https://doc.rust-lang.org/reference/)

> 原文链接: [https://doc.rust-lang.org/reference/shebang.html](https://doc.rust-lang.org/reference/shebang.html)

r[shebang]
# Shebang

r[shebang.intro]
*[shebang]* 是可选的一行，在类 Unix 系统中通常用于指定执行该文件的解释器。

> [!EXAMPLE]
> <!-- ignore: tests don't like shebang -->
> ```rust
> #!/usr/bin/env rustx
>
> fn main() {
>     println!("Hello!");
> }
> ```

r[shebang.syntax]
```grammar,lexer
@root SHEBANG ->
    `#!` !((WHITESPACE | LINE_COMMENT | BLOCK_COMMENT)* `[`)
    ~LF* (LF | EOF)
```

r[shebang.syntax-description]
shebang 以字符 `#!` 开始，一直延伸到第一个 `U+000A`（LF），若没有 LF 则延伸到 EOF。若 `#!` 字符之后跟着 `[`（忽略其间任何 [注释][comments] 或 [空白][whitespace]），则该行不被视为 shebang（以避免与 [内部属性][inner attribute] 产生歧义）。

r[shebang.position]
shebang 可以紧挨着出现在文件开头，或出现在可选的 [字节序标记][byte order mark] 之后。

[byte order mark]: https://en.wikipedia.org/wiki/Byte_order_mark#UTF-8
[comments]: comments.md
[inner attribute]: attributes.md
[shebang]: https://en.wikipedia.org/wiki/Shebang_(Unix)
[whitespace]: whitespace.md
