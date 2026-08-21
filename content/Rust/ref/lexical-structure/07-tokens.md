+++
title = "07-词法标记"
date = 2026-08-18T08:45:00+08:00
weight = 11
type = "docs"
description = "词法标记 — The Rust Reference"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Reference](https://doc.rust-lang.org/reference/)

> 原文链接: [https://doc.rust-lang.org/reference/tokens.html](https://doc.rust-lang.org/reference/tokens.html)

r[lex.token]
# 词法标记

r[lex.token.syntax]
```grammar,lexer
Token ->
      RESERVED_TOKEN
    | RAW_IDENTIFIER
    | CHAR_LITERAL
    | STRING_LITERAL
    | RAW_STRING_LITERAL
    | BYTE_LITERAL
    | BYTE_STRING_LITERAL
    | RAW_BYTE_STRING_LITERAL
    | C_STRING_LITERAL
    | RAW_C_STRING_LITERAL
    | FLOAT_LITERAL
    | INTEGER_LITERAL
    | LIFETIME_TOKEN
    | PUNCTUATION
    | IDENTIFIER_OR_KEYWORD
```

r[lex.token.intro]
Token 是文法中由正则（非递归）语言定义的基本产生式。Rust 源输入可分解为下列种类的 token：

* [关键字][Keywords]
* [标识符][identifier]
* [字面量](#字面量)
* [生命周期](#生命周期与循环标签)
* [标点](#标点)
* [定界符](#定界符)

在本文档的文法中，“简单”token 以 [字符串表产生式][string table production] 的形式给出，并以 `monospace` 字体出现。

[string table production]: notation.md#string-table-productions

r[lex.token.literal]
## 字面量

字面量是用于 [字面量表达式][literal expressions] 的 token。

### 示例

#### 字符与字符串

|                                              | 示例            | `#`&nbsp;组数[^nsets] | 字符        | 转义                |
|----------------------------------------------|-----------------|------------|-------------|---------------------|
| [字符](#字符字面量)             | `'H'`           | 0          | 全部 Unicode | [引号](#引号转义) 与 [ASCII](#ascii-转义) 与 [Unicode](#unicode-转义) |
| [字符串](#字符串字面量)                   | `"hello"`       | 0          | 全部 Unicode | [引号](#引号转义) 与 [ASCII](#ascii-转义) 与 [Unicode](#unicode-转义) |
| [原始字符串](#原始字符串字面量)           | `r#"hello"#`    | <256       | 全部 Unicode | `N/A`                                                      |
| [字节](#字节字面量)                       | `b'H'`          | 0          | 全部 ASCII   | [引号](#引号转义) 与 [字节](#字节转义)                               |
| [字节字符串](#字节字符串字面量)         | `b"hello"`      | 0          | 全部 ASCII   | [引号](#引号转义) 与 [字节](#字节转义)                               |
| [原始字节字符串](#原始字节字符串字面量) | `br#"hello"#`   | <256       | 全部 ASCII   | `N/A`                                                      |
| [C 字符串](#c-字符串字面量)               | `c"hello"`      | 0          | 全部 Unicode | [引号](#引号转义) 与 [字节](#字节转义) 与 [Unicode](#unicode-转义)   |
| [原始 C 字符串](#原始-c-字符串字面量)       | `cr#"hello"#`   | <256       | 全部 Unicode | `N/A`                                                                           |

[^nsets]: 同一字面量两侧的 `#` 数量必须相等。


#### ASCII 转义

|   | 名称 |
|---|------|
| `\x41` | 7 位字符码（恰好 2 位十六进制数字，最大 0x7F） |
| `\n` | 换行 |
| `\r` | 回车 |
| `\t` | 制表符 |
| `\\` | 反斜杠 |
| `\0` | 空字符 |

#### 字节转义

|   | 名称 |
|---|------|
| `\x7F` | 8 位字符码（恰好 2 位十六进制数字） |
| `\n` | 换行 |
| `\r` | 回车 |
| `\t` | 制表符 |
| `\\` | 反斜杠 |
| `\0` | 空字符 |

#### Unicode 转义

|   | 名称 |
|---|------|
| `\u{7FFF}` | 24 位 Unicode 字符码（最多 6 位十六进制数字） |

#### 引号转义

|   | 名称 |
|---|------|
| `\'` | 单引号 |
| `\"` | 双引号 |

#### 数字

| [数字字面量](#数字字面量)[^nl] | 示例 | 指数 |
|----------------------------------------|---------|----------------|
| 十进制整数 | `98_222` | `N/A` |
| 十六进制整数 | `0xff` | `N/A` |
| 八进制整数 | `0o77` | `N/A` |
| 二进制整数 | `0b1111_0000` | `N/A` |
| 浮点数 | `123.0E+77` | `Optional` |

[^nl]: 所有数字字面量都允许 `_` 作为视觉分隔符：`1_234.0E+18f64`

r[lex.token.literal.suffix]
#### 后缀

r[lex.token.literal.literal.suffix.intro]
后缀是紧跟在字面量主体部分之后（中间没有空白）、形式与非原始标识符或关键字相同的字符序列。

r[lex.token.literal.suffix.syntax]
```grammar,lexer
SUFFIX ->
      `_` ^ XID_Continue+
    | XID_Start XID_Continue*
```

r[lex.token.literal.suffix.validity]
任何种类的字面量（字符串、整数等）带任何后缀作为 token 都是合法的。

带任何后缀的字面量 token 都可以传给宏而不产生错误。宏自身将决定如何解释这样的 token，以及是否产生错误。特别地，示例宏的 `literal` 片段说明符会匹配带任意后缀的字面量 token。

```rust
macro_rules! blackhole { ($tt:tt) => () }
macro_rules! blackhole_lit { ($l:literal) => () }

blackhole!("string"suffix); // 可以
blackhole_lit!(1suffix); // 可以
```

r[lex.token.literal.suffix.parse]
然而，被解释为字面量表达式或模式的字面量 token 上的后缀是受限的。非数字字面量 token 上的任何后缀都会被拒绝，数字字面量 token 仅在带有下表中的后缀时才被接受。

| 整数 | 浮点 |
|---------|----------------|
| `u8`, `i8`, `u16`, `i16`, `u32`, `i32`, `u64`, `i64`, `u128`, `i128`, `usize`, `isize` | `f32`, `f64` |

### 字符与字符串字面量

r[lex.token.literal.char]
#### 字符字面量

r[lex.token.literal.char.syntax]
```grammar,lexer
CHAR_LITERAL ->
    `'`
        ( ~[`'` `\` LF CR TAB] | QUOTE_ESCAPE | ASCII_ESCAPE | UNICODE_ESCAPE )
    `'` SUFFIX?

QUOTE_ESCAPE -> `\'` | `\"`

ASCII_ESCAPE ->
      `\x` OCT_DIGIT HEX_DIGIT
    | `\n` | `\r` | `\t` | `\\` | `\0`

UNICODE_ESCAPE ->
    `\u{` ( HEX_DIGIT `_`* ){1..=6} _valid hex char value_ `}`[^valid-hex-char]
```

[^valid-hex-char]: 见 [lex.token.literal.char-escape.unicode]。

r[lex.token.literal.char.intro]
*字符字面量* 是由两个 `U+0027`（单引号）字符括起的单个 Unicode 字符，但 `U+0027` 自身除外，它必须由前面的 `U+005C` 字符（`\`）*转义*。

r[lex.token.literal.str]
#### 字符串字面量

r[lex.token.literal.str.syntax]
```grammar,lexer
STRING_LITERAL ->
    `"` (
        ~[`"` `\` CR]
      | QUOTE_ESCAPE
      | ASCII_ESCAPE
      | UNICODE_ESCAPE
      | STRING_CONTINUE
    )* `"` SUFFIX?

STRING_CONTINUE -> `\` LF
```

r[lex.token.literal.str.intro]
*字符串字面量* 是由两个 `U+0022`（双引号）字符括起的任意 Unicode 字符序列，但 `U+0022` 自身除外，它必须由前面的 `U+005C` 字符（`\`）*转义*。

r[lex.token.literal.str.linefeed]
由字符 `U+000A`（LF）表示的换行在字符串字面量中是允许的。字符 `U+000D`（CR）不得出现在字符串字面量中。当未转义的 `U+005C` 字符（`\`）紧挨着出现在换行之前时，该换行不会出现在该 token 所表示的字符串中。细节见 [字符串续行转义][String continuation escapes]。

r[lex.token.literal.char-escape]
#### 字符转义

r[lex.token.literal.char-escape.intro]
在字符字面量或非原始字符串字面量中还可使用一些额外的 *转义*。转义以 `U+005C`（`\`）开始，并以下列形式之一继续：

r[lex.token.literal.char-escape.ascii]
* *7 位码点转义* 以 `U+0078`（`x`）开始，后跟恰好两个值不超过 `0x7F` 的 *十六进制数字*。它表示值等于所给十六进制值的 ASCII 字符。更高的值不被允许，因为它们究竟表示 Unicode 码点还是字节值是有歧义的。

r[lex.token.literal.char-escape.unicode]
* *24 位码点转义* 以 `U+0075`（`u`）开始，后跟最多六个由花括号 `U+007B`（`{`）和 `U+007D`（`}`）包围的 *十六进制数字*。它表示等于所给十六进制值的 Unicode 码点。该值必须是合法的 Unicode 标量值。

r[lex.token.literal.char-escape.whitespace]
* *空白转义* 是字符 `U+006E`（`n`）、`U+0072`（`r`）或 `U+0074`（`t`）之一，分别表示 Unicode 值 `U+000A`（LF）、`U+000D`（CR）或 `U+0009`（HT）。

r[lex.token.literal.char-escape.null]
* *空字符转义* 是字符 `U+0030`（`0`），表示 Unicode 值 `U+0000`（NUL）。

r[lex.token.literal.char-escape.slash]
* *反斜杠转义* 是字符 `U+005C`（`\`），为表示其自身必须被转义。

r[lex.token.literal.str-raw]
#### 原始字符串字面量

r[lex.token.literal.str-raw.syntax]
```grammar,lexer
RAW_STRING_LITERAL ->
      `r` `"` ^ RAW_STRING_CONTENT `"` SUFFIX?
    | `r` `#`{n:1..=255} ^ `"` RAW_STRING_CONTENT_HASHED `"` `#`{n} SUFFIX?

RAW_STRING_CONTENT -> (!`"` ~CR )*

RAW_STRING_CONTENT_HASHED -> (!(`"` `#`{n}) ~CR )*
```

r[lex.token.literal.str-raw.intro]
原始字符串字面量不处理任何转义。它们以字符 `U+0072`（`r`）开始，后跟少于 256 个字符 `U+0023`（`#`），再跟一个 `U+0022`（双引号）字符。

r[lex.token.literal.str-raw.body]
*原始字符串体* 可以包含除 `U+000D`（CR）之外的任何 Unicode 字符序列。它仅由另一个 `U+0022`（双引号）字符终止，其后跟着与开 `U+0022`（双引号）字符之前相同数量的 `U+0023`（`#`）字符。

r[lex.token.literal.str-raw.content]
原始字符串体中包含的所有 Unicode 字符都表示其自身，字符 `U+0022`（双引号）（除非其后跟着至少与开始该原始字符串字面量时所用数量相同的 `U+0023`（`#`）字符）或 `U+005C`（`\`）没有任何特殊含义。

字符串字面量的示例：

```rust
"foo"; r"foo";                     // foo
"\"foo\""; r#""foo""#;             // "foo"

"foo #\"# bar";
r##"foo #"# bar"##;                // foo #"# bar

"\x52"; "R"; r"R";                 // R
"\\x52"; r"\x52";                  // \x52
```

### 字节与字节字符串字面量

r[lex.token.byte]
#### 字节字面量

r[lex.token.byte.syntax]
```grammar,lexer
BYTE_LITERAL ->
    `b'` ^ ( ASCII_FOR_CHAR | BYTE_ESCAPE )  `'` SUFFIX?

ASCII_FOR_CHAR -> ![`'` `\` LF CR TAB] ASCII

BYTE_ESCAPE ->
      `\x` HEX_DIGIT HEX_DIGIT
    | `\n` | `\r` | `\t` | `\\` | `\0` | `\'` | `\"`
```

r[lex.token.byte.intro]
*字节字面量* 是单个 ASCII 字符（在 `U+0000` 到 `U+007F` 范围内）或单个 *转义*，前面是字符 `U+0062`（`b`）和 `U+0027`（单引号），后面是字符 `U+0027`。若字面量中出现字符 `U+0027`，它必须由前面的 `U+005C`（`\`）字符 *转义*。它等价于 `u8` 无符号 8 位整数 *数字字面量*。

r[lex.token.str-byte]
#### 字节字符串字面量

r[lex.token.str-byte.syntax]
```grammar,lexer
BYTE_STRING_LITERAL ->
    `b"` ^ ( ASCII_FOR_STRING | BYTE_ESCAPE | STRING_CONTINUE )* `"` SUFFIX?

ASCII_FOR_STRING -> ![`"` `\` CR] ASCII
```

r[lex.token.str-byte.intro]
非原始 *字节字符串字面量* 是 ASCII 字符与 *转义* 的序列，前面是字符 `U+0062`（`b`）和 `U+0022`（双引号），后面是字符 `U+0022`。若字面量中出现字符 `U+0022`，它必须由前面的 `U+005C`（`\`）字符 *转义*。或者，字节字符串字面量可以是下文定义的 *原始字节字符串字面量*。

r[lex.token.str-byte.linefeed]
由字符 `U+000A`（LF）表示的换行在字节字符串字面量中是允许的。字符 `U+000D`（CR）不得出现在字节字符串字面量中。当未转义的 `U+005C` 字符（`\`）紧挨着出现在换行之前时，该换行不会出现在该 token 所表示的字符串中。细节见 [字符串续行转义][String continuation escapes]。

r[lex.token.str-byte.escape]
在字节字面量或非原始字节字符串字面量中还可使用一些额外的 *转义*。转义以 `U+005C`（`\`）开始，并以下列形式之一继续：

r[lex.token.str-byte.escape-byte]
* *字节转义* 转义以 `U+0078`（`x`）开始，后跟恰好两个 *十六进制数字*。它表示等于所给十六进制值的字节。

r[lex.token.str-byte.escape-whitespace]
* *空白转义* 是字符 `U+006E`（`n`）、`U+0072`（`r`）或 `U+0074`（`t`）之一，分别表示字节值 `0x0A`（ASCII LF）、`0x0D`（ASCII CR）或 `0x09`（ASCII HT）。

r[lex.token.str-byte.escape-null]
* *空字符转义* 是字符 `U+0030`（`0`），表示字节值 `0x00`（ASCII NUL）。

r[lex.token.str-byte.escape-slash]
* *反斜杠转义* 是字符 `U+005C`（`\`），为表示其 ASCII 编码 `0x5C` 必须被转义。

r[lex.token.str-byte-raw]
#### 原始字节字符串字面量

r[lex.token.str-byte-raw.syntax]
```grammar,lexer
RAW_BYTE_STRING_LITERAL ->
      `br` `"` ^ RAW_BYTE_STRING_CONTENT `"` SUFFIX?
    | `br` `#`{n:1..=255} ^ `"` RAW_BYTE_STRING_CONTENT_HASHED `"` `#`{n} SUFFIX?

RAW_BYTE_STRING_CONTENT -> (!`"` ASCII_FOR_RAW )*

RAW_BYTE_STRING_CONTENT_HASHED -> (!(`"` `#`{n}) ASCII_FOR_RAW )*

ASCII_FOR_RAW -> !CR ASCII
```

r[lex.token.str-byte-raw.intro]
原始字节字符串字面量不处理任何转义。它们以字符 `U+0062`（`b`）开始，后跟 `U+0072`（`r`），再跟少于 256 个字符 `U+0023`（`#`），以及一个 `U+0022`（双引号）字符。

r[lex.token.str-byte-raw.body]
*原始字符串体* 可以包含除 `U+000D`（CR）之外的任何 ASCII 字符序列。它仅由另一个 `U+0022`（双引号）字符终止，其后跟着与开 `U+0022`（双引号）字符之前相同数量的 `U+0023`（`#`）字符。原始字节字符串字面量不能包含任何非 ASCII 字节。

r[lex.token.literal.str-byte-raw.content]
原始字符串体中包含的所有字符都表示其 ASCII 编码，字符 `U+0022`（双引号）（除非其后跟着至少与开始该原始字符串字面量时所用数量相同的 `U+0023`（`#`）字符）或 `U+005C`（`\`）没有任何特殊含义。

字节字符串字面量的示例：

```rust
b"foo"; br"foo";                     // foo
b"\"foo\""; br#""foo""#;             // "foo"

b"foo #\"# bar";
br##"foo #"# bar"##;                 // foo #"# bar

b"\x52"; b"R"; br"R";                // R
b"\\x52"; br"\x52";                  // \x52
```

### C 字符串与原始 C 字符串字面量

r[lex.token.str-c]
#### C 字符串字面量

r[lex.token.str-c.syntax]
```grammar,lexer
C_STRING_LITERAL ->
    `c"` ^ (
        ~[`"` `\` CR NUL]
      | BYTE_ESCAPE _except `\0` or `\x00`_
      | UNICODE_ESCAPE _except `\u{0}`, `\u{00}`, …, `\u{000000}`_
      | STRING_CONTINUE
    )* `"` SUFFIX?
```

r[lex.token.str-c.intro]
*C 字符串字面量* 是 Unicode 字符与 *转义* 的序列，前面是字符 `U+0063`（`c`）和 `U+0022`（双引号），后面是字符 `U+0022`。若字面量中出现字符 `U+0022`，它必须由前面的 `U+005C`（`\`）字符 *转义*。或者，C 字符串字面量可以是下文定义的 *原始 C 字符串字面量*。

[CStr]: core::ffi::CStr

r[lex.token.str-c.null]
C 字符串由字节 `0x00` 隐式终止，因此 C 字符串字面量 `c""` 等价于从字节字符串字面量 `b"\x00"` 手动构造 `&CStr`。除隐式终止符外，C 字符串中不允许字节 `0x00`。

r[lex.token.str-c.linefeed]
由字符 `U+000A`（LF）表示的换行在 C 字符串字面量中是允许的。字符 `U+000D`（CR）不得出现在 C 字符串字面量中。当未转义的 `U+005C` 字符（`\`）紧挨着出现在换行之前时，该换行不会出现在该 token 所表示的字符串中。细节见 [字符串续行转义][String continuation escapes]。

r[lex.token.str-c.escape]
在非原始 C 字符串字面量中还可使用一些额外的 *转义*。转义以 `U+005C`（`\`）开始，并以下列形式之一继续：

r[lex.token.str-c.escape-byte]
* *字节转义* 转义以 `U+0078`（`x`）开始，后跟恰好两个 *十六进制数字*。它表示等于所给十六进制值的字节。

r[lex.token.str-c.escape-unicode]
* *24 位码点转义* 以 `U+0075`（`u`）开始，后跟最多六个由花括号 `U+007B`（`{`）和 `U+007D`（`}`）包围的 *十六进制数字*。它表示等于所给十六进制值的 Unicode 码点，按 UTF-8 编码。

r[lex.token.str-c.escape-whitespace]
* *空白转义* 是字符 `U+006E`（`n`）、`U+0072`（`r`）或 `U+0074`（`t`）之一，分别表示字节值 `0x0A`（ASCII LF）、`0x0D`（ASCII CR）或 `0x09`（ASCII HT）。

r[lex.token.str-c.escape-slash]
* *反斜杠转义* 是字符 `U+005C`（`\`），为表示其 ASCII 编码 `0x5C` 必须被转义。

r[lex.token.str-c.char-unicode]
C 字符串表示没有定义编码的字节，但 C 字符串字面量可以包含高于 `U+007F` 的 Unicode 字符。此类字符将被替换为该字符 UTF-8 表示的字节。

下列 C 字符串字面量是等价的：

```rust
c"æ";        // 拉丁小写字母 AE (U+00E6)
c"\u{00E6}";
c"\xC3\xA6";
```

r[lex.token.str-c.edition2021]
> [!EDITION-2021]
> C 字符串字面量在 2021 edition 或之后被接受。在更早的 edition 中，token `c""` 被词法分析为 `c ""`。

r[lex.token.str-c-raw]
#### 原始 C 字符串字面量

r[lex.token.str-c-raw.syntax]
```grammar,lexer
RAW_C_STRING_LITERAL ->
      `cr` `"` ^ RAW_C_STRING_CONTENT `"` SUFFIX?
    | `cr` `#`{n:1..=255} ^ `"` RAW_C_STRING_CONTENT_HASHED `"` `#`{n} SUFFIX?

RAW_C_STRING_CONTENT -> (!`"` ~[CR NUL] )*

RAW_C_STRING_CONTENT_HASHED -> (!(`"` `#`{n}) ~[CR NUL] )*
```

r[lex.token.str-c-raw.intro]
原始 C 字符串字面量不处理任何转义。它们以字符 `U+0063`（`c`）开始，后跟 `U+0072`（`r`），再跟少于 256 个字符 `U+0023`（`#`），以及一个 `U+0022`（双引号）字符。

r[lex.token.str-c-raw.body]
*原始 C 字符串体* 可以包含除 `U+0000`（NUL）和 `U+000D`（CR）之外的任何 Unicode 字符序列。它仅由另一个 `U+0022`（双引号）字符终止，其后跟着与开 `U+0022`（双引号）字符之前相同数量的 `U+0023`（`#`）字符。

r[lex.token.str-c-raw.content]
原始 C 字符串体中包含的所有字符都以 UTF-8 编码表示其自身。字符 `U+0022`（双引号）（除非其后跟着至少与开始该原始 C 字符串字面量时所用数量相同的 `U+0023`（`#`）字符）或 `U+005C`（`\`）没有任何特殊含义。

r[lex.token.str-c-raw.edition2021]
> [!EDITION-2021]
> 原始 C 字符串字面量在 2021 edition 或之后被接受。在更早的 edition 中，token `cr""` 被词法分析为 `cr ""`，而 `cr#""#` 被词法分析为 `cr #""#`（这不合文法）。

#### C 字符串与原始 C 字符串字面量的示例

```rust
c"foo"; cr"foo";                     // foo
c"\"foo\""; cr#""foo""#;             // "foo"

c"foo #\"# bar";
cr##"foo #"# bar"##;                 // foo #"# bar

c"\x52"; c"R"; cr"R";                // R
c"\\x52"; cr"\x52";                  // \x52
```

r[lex.token.literal.num]
### 数字字面量

*数字字面量* 要么是 *整数字面量*，要么是 *浮点字面量*。识别这两类字面量的文法是混合的。

r[lex.token.literal.int]
#### 整数字面量

r[lex.token.literal.int.syntax]
```grammar,lexer
INTEGER_LITERAL ->
    ( BIN_LITERAL | OCT_LITERAL | HEX_LITERAL | DEC_LITERAL )
    ^ !RESERVED_FLOAT SUFFIX?

DEC_LITERAL -> DEC_DIGIT (DEC_DIGIT|`_`)*

BIN_LITERAL -> `0b` ^ `_`* BIN_DIGIT (BIN_DIGIT|`_`)* ![`e` `E` `2`-`9`]

OCT_LITERAL -> `0o` ^ `_`* OCT_DIGIT (OCT_DIGIT|`_`)* ![`e` `E` `8`-`9`]

HEX_LITERAL -> `0x` ^ `_`* HEX_DIGIT (HEX_DIGIT|`_`)*

BIN_DIGIT -> [`0`-`1`]

OCT_DIGIT -> [`0`-`7`]

DEC_DIGIT -> [`0`-`9`]

HEX_DIGIT -> [`0`-`9` `a`-`f` `A`-`F`]

RESERVED_FLOAT -> `.` !(`.` | `_` | XID_Start)
```

r[lex.token.literal.int.kind]
*整数字面量* 有四种形式之一：

r[lex.token.literal.int.kind-dec]
* *十进制字面量* 以 *十进制数字* 开始，并继续任意混合的 *十进制数字* 和 *下划线*。

r[lex.token.literal.int.kind-hex]
* *十六进制字面量* 以字符序列 `U+0030` `U+0078`（`0x`）开始，并继续十六进制数字与下划线的任意混合（至少有一位数字）。

r[lex.token.literal.int.kind-oct]
* *八进制字面量* 以字符序列 `U+0030` `U+006F`（`0o`）开始，并继续八进制数字与下划线的任意混合（至少有一位数字）。

r[lex.token.literal.int.kind-bin]
* *二进制字面量* 以字符序列 `U+0030` `U+0062`（`0b`）开始，并继续二进制数字与下划线的任意混合（至少有一位数字）。

r[lex.token.literal.int.suffix]
与任何字面量一样，整数字面量后面可以（立即、中间没有空格）跟上文所述的后缀。后缀不得以 `e` 或 `E` 开头，因为那会被解释为浮点字面量的指数。这些后缀的效果见 [整数字面量表达式][Integer literal expressions]。

作为字面量表达式被接受的整数字面量示例：

```rust
## #![allow(overflowing_literals)]
123;
123i32;
123u32;
123_u32;

0xff;
0xff_u8;
0x01_f32; // 整数 7986，不是浮点 1.0
0x01_e3;  // 整数 483，不是浮点 1000.0

0o70;
0o70_i16;

0b1111_1111_1001_0000;
0b1111_1111_1001_0000i64;
0b________1;

0usize;

// 这些对其类型来说太大，但作为字面量表达式被接受。
128_i8;
256_u8;

// 这是整数字面量，作为浮点字面量表达式被接受。
5f32;
```

注意例如 `-1i8` 被分析为两个 token：`-` 后跟 `1i8`。

不作为字面量表达式被接受的整数字面量示例：

```rust
## #[cfg(false)] {
0invalidSuffix;
123AFB43;
0b010a;
0xAB_CD_EF_GH;
0b1111_f32;
## }
```

r[lex.token.literal.int.invalid]
##### 无效的整数字面量

r[lex.token.literal.int.invalid.intro]
某些整数字面量形式是无效的。为避免歧义，词法分析器拒绝它们，而不是把它们拆成独立的 token。

```rust
0b0102;  // 这不是 `0b010` 后跟 `2`。
0o1279;  // 这不是 `0o127` 后跟 `9`。
0x80.0;  // 这不是 `0x80` 后跟 `.` 和 `0`。
0b101e;  // 这不是带后缀的字面量，也不是 `0b101` 后跟 `e`。
0b;      // 这不是整数字面量，也不是 `0` 后跟 `b`。
0b_;     // 这不是整数字面量，也不是 `0` 后跟 `b_`。
2em;     // 这不是带后缀的字面量，也不是 `2` 后跟 `em`。
2.0em;   // 这不是带后缀的字面量，也不是 `2.0` 后跟 `em`。
```

r[lex.token.literal.int.out-of-range]
无后缀的二进制或八进制字面量后面若没有间隔空白、紧跟着其进制范围之外的十进制数字，则为错误。

r[lex.token.literal.int.period]
无后缀的二进制、八进制或十六进制字面量后面若没有间隔空白、紧跟着句点字符（受与浮点字面量中句点之后可跟内容相同的限制），则为错误。

r[lex.token.literal.int.exp]
无后缀的二进制或八进制字面量后面若没有间隔空白、紧跟着字符 `e` 或 `E`，则为错误。

r[lex.token.literal.int.empty-with-radix]
进制前缀在任意可选的前导下划线之后若没有至少一位对其进制合法的数字，则为错误。

r[lex.token.literal.int.tuple-field]
#### 元组索引

r[lex.token.literal.int.tuple-field.syntax]
```grammar,lexer
TUPLE_INDEX -> DEC_LITERAL | BIN_LITERAL | OCT_LITERAL | HEX_LITERAL
```

r[lex.token.literal.int.tuple-field.intro]
元组索引用于引用 [元组][tuples]、[元组结构体][tuple structs] 和 [元组枚举变体][tuple enum variants] 的字段。

r[lex.token.literal.int.tuple-field.eq]
元组索引直接与字面量 token 比较。元组索引从 `0` 开始，每个后续索引将值按十进制加 `1`。因此只有十进制值会匹配，且该值不得有任何额外的 `0` 前缀字符。

元组索引不得包含任何后缀（如 `usize`）。

```rust
let example = ("dog", "cat", "horse");
let dog = example.0;
let cat = example.1;
// 下列示例无效。
let cat = example.01;  // ERROR 没有名为 `01` 的字段
let horse = example.0b10;  // ERROR 没有名为 `0b10` 的字段
let unicorn = example.0usize; // ERROR 元组索引上的后缀无效
let underscore = example.0_0; // ERROR 类型 `(&str, &str, &str)` 上没有字段 `0_0`
```

r[lex.token.literal.float]
#### 浮点字面量

r[lex.token.literal.float.syntax]
```grammar,lexer
FLOAT_LITERAL ->
      DEC_LITERAL (`.` DEC_LITERAL)? FLOAT_EXPONENT SUFFIX?
    | DEC_LITERAL `.` DEC_LITERAL SUFFIX?
    | DEC_LITERAL `.` !(`.` | `_` | XID_Start)

FLOAT_EXPONENT ->
    (`e`|`E`) ^ (`+`|`-`)? `_`* DEC_DIGIT (DEC_DIGIT|`_`)*
```

r[lex.token.literal.float.form]
*浮点字面量* 有两种形式之一：

* *十进制字面量* 后跟句点字符 `U+002E`（`.`）。这可选地后跟另一个十进制字面量，以及可选的 *指数*。
* 单个 *十进制字面量* 后跟 *指数*。

r[lex.token.literal.float.suffix]
与整数字面量一样，浮点字面量后面可以跟后缀，只要后缀前的部分不以 `U+002E`（`.`）结尾。若字面量不包含指数，后缀不得以 `e` 或 `E` 开头。这些后缀的效果见 [浮点字面量表达式][Floating-point literal expressions]。

作为字面量表达式被接受的浮点字面量示例：

```rust
123.0f64;
0.1f64;
0.1f32;
12E+99_f64;
let x: f64 = 2.;
```

最后一个例子有所不同，因为不可能对以句点结尾的浮点字面量使用后缀语法。`2.f64` 会尝试在 `2` 上调用名为 `f64` 的方法。

注意例如 `-1.0` 被分析为两个 token：`-` 后跟 `1.0`。

不作为字面量表达式被接受的浮点字面量示例：

```rust
## #[cfg(false)] {
2.0f80;
2e5f80;
2e5e6;
2.0e5e6;
1.3e10u64;
## }
```

r[lex.token.literal.float.invalid-exponent]
浮点字面量具有没有数字的指数是错误。

```rust
2e;   // 这不是浮点字面量，也不是 `2` 后跟 `e`。
2.0e; // 这不是浮点字面量，也不是 `2.0` 后跟 `e`。
```

r[lex.token.life]
## 生命周期与循环标签

r[lex.token.life.syntax]
```grammar,lexer
LIFETIME_TOKEN ->
      RAW_LIFETIME
    | `'` IDENTIFIER_OR_KEYWORD !`'`

LIFETIME_OR_LABEL ->
      RAW_LIFETIME
    | `'` NON_KEYWORD_IDENTIFIER !`'`

RAW_LIFETIME ->
    `'r#` ^ IDENTIFIER_OR_KEYWORD !`'`

RESERVED_RAW_LIFETIME -> `'r#` (`_` | `crate` | `self` | `Self` | `super`) !(`'` | XID_Continue)
```

r[lex.token.life.intro]
生命周期参数和 [循环标签][loop labels] 使用 LIFETIME_OR_LABEL token。任何 LIFETIME_TOKEN 都会被词法分析器接受，例如可以在宏中使用。

r[lex.token.life.raw.intro]
原始生命周期与普通生命周期类似，但其标识符带有 `r#` 前缀。（注意 `r#` 前缀并不包含在实际生命周期中。）

r[lex.token.life.raw.allowed]
与普通生命周期不同，原始生命周期可以是除上文 `RAW_LIFETIME` 所列之外的任何严格或保留关键字。

r[lex.token.life.raw.reserved]
使用 [RESERVED_RAW_LIFETIME] token 是错误。

r[lex.token.life.raw.edition2021]
> [!EDITION-2021]
> 原始生命周期在 2021 edition 或之后被接受。在更早的 edition 中，token `'r#lt` 被词法分析为 `'r # lt`。

r[lex.token.punct]
## 标点

r[lex.token.punct.intro]
标点 token 用作运算符、分隔符以及文法的其他部分。

r[lex.token.punct.syntax]
```grammar,lexer
PUNCTUATION ->
      `...`
    | `..=`
    | `<<=`
    | `>>=`
    | `!=`
    | `%=`
    | `&&`
    | `&=`
    | `*=`
    | `+=`
    | `-=`
    | `->`
    | `..`
    | `/=`
    | `::`
    | `<-`
    | `<<`
    | `<=`
    | `==`
    | `=>`
    | `>=`
    | `>>`
    | `^=`
    | `|=`
    | `||`
    | `!`
    | `#`
    | `$`
    | `%`
    | `&`
    | `(`
    | `)`
    | `*`
    | `+`
    | `,`
    | `-`
    | `.`
    | `/`
    | `:`
    | `;`
    | `<`
    | `=`
    | `>`
    | `?`
    | `@`
    | `[`
    | `]`
    | `^`
    | `{`
    | `|`
    | `}`
    | `~`
```

> **注意**
> 标点字符如何使用的链接见 [语法索引][syntax index]。

r[lex.token.delim]
## 定界符

括号标点用于文法的各个部分。开括号必须始终与闭括号配对。括号及其内部的 token 在 [宏][macros] 中称为“token 树”。三种括号是：

| 括号 | 类型            |
|---------|-----------------|
| `{` `}` | 花括号    |
| `[` `]` | 方括号 |
| `(` `)` | 圆括号     |

r[lex.token.reserved]
## 保留 token

r[lex.token.reserved.intro]
若干 token 形式为将来使用或为避免混淆而保留。源输入匹配这些形式之一是错误。

r[lex.token.reserved.syntax]
```grammar,lexer
RESERVED_TOKEN ->
      RESERVED_GUARDED_STRING_LITERAL
    | RESERVED_POUNDS
    | RESERVED_RAW_IDENTIFIER
    | RESERVED_RAW_LIFETIME
    | RESERVED_TOKEN_DOUBLE_QUOTE
    | RESERVED_TOKEN_LIFETIME
    | RESERVED_TOKEN_POUND
    | RESERVED_TOKEN_SINGLE_QUOTE
```

r[lex.token.reserved-prefix]
## 保留前缀

r[lex.token.reserved-prefix.syntax]
```grammar,lexer
RESERVED_TOKEN_DOUBLE_QUOTE ->
    IDENTIFIER_OR_KEYWORD _except `b` or `c` or `r` or `br` or `cr`_ `"`

RESERVED_TOKEN_SINGLE_QUOTE ->
    IDENTIFIER_OR_KEYWORD _except `b`_ `'`

RESERVED_TOKEN_POUND ->
    IDENTIFIER_OR_KEYWORD _except `r` or `br` or `cr`_ `#`

RESERVED_TOKEN_LIFETIME ->
    `'` IDENTIFIER_OR_KEYWORD _except `r`_ `#`
```

r[lex.token.reserved-prefix.intro]
一些称为 *保留前缀* 的词法形式为将来使用而保留。

r[lex.token.reserved-prefix.id]
若源输入在其他情况下会被词法解释为非原始标识符（或关键字），且其后立即跟着 `#`、`'` 或 `"` 字符（中间没有空白），则被识别为保留前缀。

r[lex.token.reserved-prefix.raw-token]
注意原始标识符、原始字符串字面量和原始字节字符串字面量可以包含 `#` 字符，但不会被解释为包含保留前缀。

r[lex.token.reserved-prefix.strings]
类似地，原始字符串字面量、字节字面量、字节字符串字面量、原始字节字符串字面量、C 字符串字面量和原始 C 字符串字面量中使用的 `r`、`b`、`br`、`c` 和 `cr` 前缀不会被解释为保留前缀。

r[lex.token.reserved-prefix.life]
若源输入在其他情况下会被词法解释为非原始生命周期（或关键字），且其后立即跟着 `#` 字符（中间没有空白），则被识别为保留生命周期前缀。

r[lex.token.reserved-prefix.edition2021]
> [!EDITION-2021]
> 从 2021 edition 开始，保留前缀由词法分析器报告为错误（特别是，它们不能被传给宏）。
>
> 在 2021 edition 之前，保留前缀被词法分析器接受并解释为多个 token（例如，标识符或关键字一个 token，后跟一个 `#` token）。
>
> 在所有 edition 中都被接受的示例：
> ```rust
> macro_rules! lexes {($($_:tt)*) => {}}
> lexes!{a #foo}
> lexes!{continue 'foo}
> lexes!{match "..." {}}
> lexes!{r#let#foo}         // 三个 token：r#let # foo
> lexes!{'prefix #lt}
> ```
>
> 在 2021 edition 之前被接受、之后被拒绝的示例：
> ```rust
> macro_rules! lexes {($($_:tt)*) => {}}
> lexes!{a#foo}
> lexes!{continue'foo}
> lexes!{match"..." {}}
> lexes!{'prefix#lt}
> ```

r[lex.token.reserved-guards]
## 保留守卫

r[lex.token.reserved-guards.syntax]
```grammar,lexer
RESERVED_GUARDED_STRING_LITERAL -> `#`+ STRING_LITERAL

RESERVED_POUNDS -> `#`{2..}
```

r[lex.token.reserved-guards.intro]
保留守卫是为将来使用而保留的语法，若使用将产生编译错误。

r[lex.token.reserved-guards.string-literal]
*保留守卫字符串字面量* 是一个或多个 `U+0023`（`#`）立即后跟 [STRING_LITERAL] 的 token。

r[lex.token.reserved-guards.pounds]
*保留井号* 是两个或更多 `U+0023`（`#`）的 token。

r[lex.token.reserved-guards.edition2024]
> [!EDITION-2024]
> 在 2024 edition 之前，保留守卫被词法分析器接受并解释为多个 token。例如，`#"foo"#` 形式被解释为三个 token。`##` 被解释为两个 token。

[Floating-point literal expressions]: expressions/literal-expr.md#floating-point-literal-expressions
[identifier]: identifiers.md
[Integer literal expressions]: expressions/literal-expr.md#integer-literal-expressions
[keywords]: keywords.md
[literal expressions]: expressions/literal-expr.md
[loop labels]: expressions/loop-expr.md#loop-labels
[macros]: macros-by-example.md
[String continuation escapes]: expressions/literal-expr.md#string-continuation-escapes
[syntax index]: syntax-index.md#operators-and-punctuation
[tuple structs]: items/structs.md
[tuple enum variants]: items/enumerations.md
[tuples]: types/tuple.md
