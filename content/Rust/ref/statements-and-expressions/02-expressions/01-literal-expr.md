+++
title = "01-字面量表达式"
date = 2026-08-18T08:45:00+08:00
weight = 44
type = "docs"
description = "字面量表达式 — The Rust Reference"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Reference](https://doc.rust-lang.org/reference/)

> 原文链接: [https://doc.rust-lang.org/reference/expressions/literal-expr.html](https://doc.rust-lang.org/reference/expressions/literal-expr.html)

r[expr.literal]
# 字面量表达式

r[expr.literal.syntax]
```grammar,expressions
LiteralExpression ->
      CHAR_LITERAL
    | STRING_LITERAL
    | RAW_STRING_LITERAL
    | BYTE_LITERAL
    | BYTE_STRING_LITERAL
    | RAW_BYTE_STRING_LITERAL
    | C_STRING_LITERAL
    | RAW_C_STRING_LITERAL
    | INTEGER_LITERAL
    | FLOAT_LITERAL
    | `true`
    | `false`
```

r[expr.literal.intro]
*字面量表达式*是由单个 token（而非一串 token）构成的表达式，它立即且直接地指明其求值所得的值，而不是通过名称或其他求值规则来引用该值。

r[expr.literal.const-expr]
字面量是一种[常量表达式][constant expression]，因此（主要）在编译期求值。

r[expr.literal.literal-token]
前文所述的每一种词法[字面量][literal tokens]形式都可以构成字面量表达式，关键字 `true` 和 `false` 也可以。

```rust
"hello";   // 字符串类型
'5';       // 字符类型
5;         // 整数类型
```

r[expr.literal.string-representation]
在下文的描述中，token 的*字符串表示*是输入中匹配了该 token 在 *Lexer* 文法片段中的产生式的那一串字符。

> **注意**
> 该字符串表示从不包含紧跟着 `U+000A`（LF）的字符 `U+000D`（CR）：这一对会在此前已被转换为单个 `U+000A`（LF）。

r[expr.literal.escape]
## 转义

r[expr.literal.escape.intro]
下文对文本字面量表达式的描述使用了若干种形式的*转义*。

r[expr.literal.escape.sequence]
每种转义形式的特征是：
 * 一个*转义序列*：一串字符，总是以 `U+005C`（`\`）开始
 * 一个*转义值*：要么是单个字符，要么是空的字符序列

在下文转义的定义中：
 * *八进制数字*是范围 \[`0`-`7`] 中的任意字符。
 * *十六进制数字*是范围 \[`0`-`9`]、\[`a`-`f`] 或 \[`A`-`F`] 中的任意字符。

r[expr.literal.escape.simple]
### 简单转义

下表第一列中出现的每一串字符都是转义序列。

在每种情况下，转义值都是第二列对应条目中给出的字符。

| 转义序列        | 转义值                   |
|-----------------|--------------------------|
| `\0`            | U+0000 (NUL)             |
| `\t`            | U+0009 (HT)              |
| `\n`            | U+000A (LF)              |
| `\r`            | U+000D (CR)              |
| `\"`            | U+0022 (QUOTATION MARK)  |
| `\'`            | U+0027 (APOSTROPHE)      |
| `\\`            | U+005C (REVERSE SOLIDUS) |

r[expr.literal.escape.hex-octet]
### 8 位转义

转义序列由 `\x` 后跟两位十六进制数字组成。

转义值是这样一个字符：其[Unicode 标量值][Unicode scalar value]等于把转义序列的最后两个字符按十六进制整数来解释的结果，如同使用进制为 16 的 [`u8::from_str_radix`]。

> **注意**
> 因此，转义值的[Unicode 标量值][Unicode scalar value]落在 [`u8`][numeric types] 的范围内。

r[expr.literal.escape.hex-ascii]
### 7 位转义

转义序列由 `\x` 后跟一位八进制数字再跟一位十六进制数字组成。

转义值是这样一个字符：其[Unicode 标量值][Unicode scalar value]等于把转义序列的最后两个字符按十六进制整数来解释的结果，如同使用进制为 16 的 [`u8::from_str_radix`]。

r[expr.literal.escape.unicode]
### Unicode 转义

转义序列由 `\u{`、随后一串每个都是十六进制数字或 `_` 的字符、再随后 `}` 组成。

转义值是这样一个字符：其[Unicode 标量值][Unicode scalar value]等于把转义序列中所含的十六进制数字按十六进制整数来解释的结果，如同使用进制为 16 的 [`u32::from_str_radix`]。

> **注意**
> [CHAR_LITERAL] 或 [STRING_LITERAL] token 的合法形式确保存在这样的字符。

r[expr.literal.continuation]
### 字符串续行转义

转义序列由紧跟着 `U+000A`（LF）的 `\`，以及下一个非空白字符之前的所有后续空白字符组成。就此而言，空白字符为 `U+0009`（HT）、`U+000A`（LF）、`U+000D`（CR）和 `U+0020`（SPACE）。

转义值是空的字符序列。

> **注意**
> 这种转义的效果是字符串续行会跳过后续空白，包括额外的换行。因此 `a`、`b` 和 `c` 相等：
>
> ```rust
> let a = "foobar";
> let b = "foo\
>          bar";
> let c = "foo\
>
>      bar";
>
> assert_eq!(a, b);
> assert_eq!(b, c);
> ```
>
> 跳过额外的换行（如示例 c）可能令人困惑且出人意料。此行为将来可能会调整。在做出决定之前，建议不要依赖用续行来跳过多个换行。更多信息见[此 issue](https://github.com/rust-lang/reference/pull/1042)。

r[expr.literal.char]
## 字符字面量表达式

r[expr.literal.char.intro]
字符字面量表达式由单个 [CHAR_LITERAL] token 组成。

r[expr.literal.char.type]
该表达式的类型是原始 [`char`] 类型。

r[expr.literal.char.no-suffix]
该 token 不得带有后缀。

r[expr.literal.char.literal-content]
该 token 的*字面内容*是其字符串表示中第一个 `U+0027`（`'`）之后、最后一个 `U+0027`（`'`）之前的字符序列。

r[expr.literal.char.represented]
字面量表达式的*所表示字符*由字面内容按如下方式导出：

r[expr.literal.char.escape]
* 若字面内容是下列形式的转义序列之一，则所表示字符就是该转义序列的转义值：
    * [简单转义][Simple escapes]
    * [7 位转义][7-bit escapes]
    * [Unicode 转义][Unicode escapes]

r[expr.literal.char.single]
* 否则，所表示字符就是构成字面内容的那个单个字符。

r[expr.literal.char.result]
该表达式的值是与所表示字符的[Unicode 标量值][Unicode scalar value]相对应的 [`char`]。

> **注意**
> [CHAR_LITERAL] token 的合法形式确保这些规则总是产生单个字符。

字符字面量表达式的示例：

```rust
'R';                               // R
'\'';                              // '
'\x52';                            // R
'\u{00E6}';                        // 拉丁小写字母 AE (U+00E6)
```

r[expr.literal.string]
## 字符串字面量表达式

r[expr.literal.string.intro]
字符串字面量表达式由单个 [STRING_LITERAL] 或 [RAW_STRING_LITERAL] token 组成。

r[expr.literal.string.type]
该表达式的类型是指向原始 [`str`] 类型的共享引用（生命周期为 `static`）。亦即类型为 `&'static str`。

r[expr.literal.string.no-suffix]
该 token 不得带有后缀。

r[expr.literal.string.literal-content]
该 token 的*字面内容*是其字符串表示中第一个 `U+0022`（`"`）之后、最后一个 `U+0022`（`"`）之前的字符序列。

r[expr.literal.string.represented]
字面量表达式的*所表示字符串*是由字面内容按如下方式导出的字符序列：

r[expr.literal.string.escape]
* 若该 token 是 [STRING_LITERAL]，则字面内容中出现的下列任何形式的每个转义序列，都会被替换为该转义序列的转义值。
    * [简单转义][Simple escapes]
    * [7 位转义][7-bit escapes]
    * [Unicode 转义][Unicode escapes]
    * [字符串续行转义][String continuation escapes]

  这些替换按从左到右的顺序进行。例如，token `"\\x41"` 被转换为字符 `\` `x` `4` `1`。

r[expr.literal.string.raw]
* 若该 token 是 [RAW_STRING_LITERAL]，则所表示字符串与字面内容相同。

r[expr.literal.string.result]
该表达式的值是对静态分配的 [`str`] 的引用，其中包含所表示字符串的 UTF-8 编码。

字符串字面量表达式的示例：

```rust
"foo"; r"foo";                     // foo
"\"foo\""; r#""foo""#;             // "foo"

"foo #\"# bar";
r##"foo #"# bar"##;                // foo #"# bar

"\x52"; "R"; r"R";                 // R
"\\x52"; r"\x52";                  // \x52
```

r[expr.literal.byte-char]
## 字节字面量表达式

r[expr.literal.byte-char.intro]
字节字面量表达式由单个 [BYTE_LITERAL] token 组成。

r[expr.literal.byte-char.literal]
该表达式的类型是原始 [`u8`][numeric types] 类型。

r[expr.literal.byte-char.no-suffix]
该 token 不得带有后缀。

r[expr.literal.byte-char.literal-content]
该 token 的*字面内容*是其字符串表示中第一个 `U+0027`（`'`）之后、最后一个 `U+0027`（`'`）之前的字符序列。

r[expr.literal.byte-char.represented]
字面量表达式的*所表示字符*由字面内容按如下方式导出：

r[expr.literal.byte-char.escape]
* 若字面内容是下列形式的转义序列之一，则所表示字符就是该转义序列的转义值：
    * [简单转义][Simple escapes]
    * [8 位转义][8-bit escapes]

r[expr.literal.byte-char.single]
* 否则，所表示字符就是构成字面内容的那个单个字符。

r[expr.literal.byte-char.result]
该表达式的值是所表示字符的[Unicode 标量值][Unicode scalar value]。

> **注意**
> [BYTE_LITERAL] token 的合法形式确保这些规则总是产生单个字符，且其 Unicode 标量值落在 [`u8`][numeric types] 的范围内。

字节字面量表达式的示例：

```rust
b'R';                              // 82
b'\'';                             // 39
b'\x52';                           // 82
b'\xA0';                           // 160
```

r[expr.literal.byte-string]
## 字节字符串字面量表达式

r[expr.literal.byte-string.intro]
字节字符串字面量表达式由单个 [BYTE_STRING_LITERAL] 或 [RAW_BYTE_STRING_LITERAL] token 组成。

r[expr.literal.byte-string.type]
该表达式的类型是指向元素类型为 [`u8`][numeric types] 的数组的共享引用（生命周期为 `static`）。亦即类型为 `&'static [u8; N]`，其中 `N` 是下文所述所表示字符串中的字节数。

r[expr.literal.byte-string.no-suffix]
该 token 不得带有后缀。

r[expr.literal.byte-string.literal-content]
该 token 的*字面内容*是其字符串表示中第一个 `U+0022`（`"`）之后、最后一个 `U+0022`（`"`）之前的字符序列。

r[expr.literal.byte-string.represented]
字面量表达式的*所表示字符串*是由字面内容按如下方式导出的字符序列：

r[expr.literal.byte-string.escape]
* 若该 token 是 [BYTE_STRING_LITERAL]，则字面内容中出现的下列任何形式的每个转义序列，都会被替换为该转义序列的转义值。
    * [简单转义][Simple escapes]
    * [8 位转义][8-bit escapes]
    * [字符串续行转义][String continuation escapes]

  这些替换按从左到右的顺序进行。例如，token `b"\\x41"` 被转换为字符 `\` `x` `4` `1`。

r[expr.literal.byte-string.raw]
* 若该 token 是 [RAW_BYTE_STRING_LITERAL]，则所表示字符串与字面内容相同。

r[expr.literal.byte-string.result]
该表达式的值是对静态分配数组的引用，该数组按相同顺序包含所表示字符串中各字符的[Unicode 标量值][Unicode scalar values]。

> **注意**
> [BYTE_STRING_LITERAL] 和 [RAW_BYTE_STRING_LITERAL] token 的合法形式确保这些规则总是产生落在 [`u8`][numeric types] 范围内的数组元素值。

字节字符串字面量表达式的示例：

```rust
b"foo"; br"foo";                     // foo
b"\"foo\""; br#""foo""#;             // "foo"

b"foo #\"# bar";
br##"foo #"# bar"##;                 // foo #"# bar

b"\x52"; b"R"; br"R";                // R
b"\\x52"; br"\x52";                  // \x52
```

r[expr.literal.c-string]
## C 字符串字面量表达式

r[expr.literal.c-string.intro]
C 字符串字面量表达式由单个 [C_STRING_LITERAL] 或 [RAW_C_STRING_LITERAL] token 组成。

r[expr.literal.c-string.type]
该表达式的类型是指向标准库 [CStr] 类型的共享引用（生命周期为 `static`）。亦即类型为 `&'static core::ffi::CStr`。

r[expr.literal.c-string.no-suffix]
该 token 不得带有后缀。

r[expr.literal.c-string.literal-content]
该 token 的*字面内容*是其字符串表示中第一个 `"` 之后、最后一个 `"` 之前的字符序列。

r[expr.literal.c-string.represented]
字面量表达式的*所表示字节*是由字面内容按如下方式导出的字节序列：

r[expr.literal.c-string.escape]
* 若该 token 是 [C_STRING_LITERAL]，则字面内容被视为一个项序列，其中每一项要么是除 `\` 之外的单个 Unicode 字符，要么是一次[转义][Escape]。该项序列按如下方式转换为字节序列：
  * 每个单独的 Unicode 字符贡献其 UTF-8 表示。
  * 每次[简单转义][Simple escape]贡献其转义值的[Unicode 标量值][Unicode scalar value]。
  * 每次[8 位转义][8-bit escape]贡献一个包含其转义值之[Unicode 标量值][Unicode scalar value]的单字节。
  * 每次[Unicode 转义][Unicode escape]贡献其转义值的 UTF-8 表示。
  * 每次[字符串续行转义][String continuation escape]不贡献任何字节。

r[expr.literal.c-string.raw]
* 若该 token 是 [RAW_C_STRING_LITERAL]，则所表示字节是字面内容的 UTF-8 编码。

> **注意**
> [C_STRING_LITERAL] 和 [RAW_C_STRING_LITERAL] token 的合法形式确保所表示字节从不包含空字节。

r[expr.literal.c-string.result]
该表达式的值是对静态分配的 [CStr] 的引用，其字节数组包含所表示字节后跟一个空字节。

C 字符串字面量表达式的示例：

```rust
c"foo"; cr"foo";                     // foo
c"\"foo\""; cr#""foo""#;             // "foo"

c"foo #\"# bar";
cr##"foo #"# bar"##;                 // foo #"# bar

c"\x52"; c"R"; cr"R";                // R
c"\\x52"; cr"\x52";                  // \x52

c"æ";                                // 拉丁小写字母 AE (U+00E6)
c"\u{00E6}";                         // 拉丁小写字母 AE (U+00E6)
c"\xC3\xA6";                         // 拉丁小写字母 AE (U+00E6)

c"\xE6".to_bytes();                  // [230]
c"\u{00E6}".to_bytes();              // [195, 166]
```

r[expr.literal.int]
## 整数字面量表达式

r[expr.literal.int.intro]
整数字面量表达式由单个 [INTEGER_LITERAL] token 组成。

r[expr.literal.int.suffix]
若该 token 带有[后缀][suffix]，则后缀必须是[原始整数类型][numeric types]之一的名称：`u8`、`i8`、`u16`、`i16`、`u32`、`i32`、`u64`、`i64`、`u128`、`i128`、`usize` 或 `isize`，且该表达式具有该类型。

r[expr.literal.int.infer]
若该 token 没有后缀，则该表达式的类型由类型推断确定：

r[expr.literal.int.inference-unique-type]
* 若可以从周围的程序上下文中*唯一*确定一个整数类型，则该表达式具有该类型。

r[expr.literal.int.inference-default]
* 若程序上下文对该类型约束不足，则默认采用有符号 32 位整数 `i32`。

r[expr.literal.int.inference-error]
* 若程序上下文对该类型约束过度，则视为静态类型错误。

整数字面量表达式的示例：

```rust
123;                               // 类型 i32
123i32;                            // 类型 i32
123u32;                            // 类型 u32
123_u32;                           // 类型 u32
let a: u64 = 123;                  // 类型 u64

0xff;                              // 类型 i32
0xff_u8;                           // 类型 u8

0o70;                              // 类型 i32
0o70_i16;                          // 类型 i16

0b1111_1111_1001_0000;             // 类型 i32
0b1111_1111_1001_0000i64;          // 类型 i64

0usize;                            // 类型 usize
```

r[expr.literal.int.representation]
该表达式的值由该 token 的字符串表示按如下方式确定：

r[expr.literal.int.radix]
* 通过检查该字符串的前两个字符来选择整数进制，如下：

    * `0b` 表示进制 2
    * `0o` 表示进制 8
    * `0x` 表示进制 16
    * 否则进制为 10。

r[expr.literal.int.radix-prefix-stripped]
* 若进制不是 10，则从该字符串中移除前两个字符。

r[expr.literal.int.type-suffix-stripped]
* 从该字符串中移除任何后缀。

r[expr.literal.int.separators-stripped]
* 从该字符串中移除所有下划线。

r[expr.literal.int.u128-value]
* 将该字符串按所选进制转换为 `u128` 值，如同使用 [`u128::from_str_radix`]。若该值无法放入 `u128`，则为编译器错误。

r[expr.literal.int.cast]
* 该 `u128` 值通过[数值转换][numeric cast]转换为该表达式的类型。

> **注意**
> 若字面量的值无法放入该表达式的类型，最终的转换会截断该值。`rustc` 包含一个名为 `overflowing_literals` 的[lint 检查][lint check]，默认级别为 `deny`，会拒绝发生这种情况的表达式。

> **注意**
> 例如，`-1i8` 是对字面量表达式 `1i8` 应用[取负运算符][negation operator]，而不是单个整数字面量表达式。关于如何表示有符号类型的最小负值，见[溢出][overflow]。

r[expr.literal.float]
## 浮点字面量表达式

r[expr.literal.float.intro]
浮点字面量表达式有两种形式之一：
 * 单个 [FLOAT_LITERAL] token
 * 单个带有后缀且没有进制指示的 [INTEGER_LITERAL] token

r[expr.literal.float.suffix]
若该 token 带有[后缀][suffix]，则后缀必须是[原始浮点类型][floating-point types]之一的名称：`f32` 或 `f64`，且该表达式具有该类型。

r[expr.literal.float.infer]
若该 token 没有后缀，则该表达式的类型由类型推断确定：

r[expr.literal.float.inference-unique-type]
* 若可以从周围的程序上下文中*唯一*确定一个浮点类型，则该表达式具有该类型。

r[expr.literal.float.inference-default]
* 若程序上下文对该类型约束不足，则默认为 `f64`。

r[expr.literal.float.inference-error]
* 若程序上下文对该类型约束过度，则视为静态类型错误。

浮点字面量表达式的示例：

```rust
123.0f64;        // 类型 f64
0.1f64;          // 类型 f64
0.1f32;          // 类型 f32
12E+99_f64;      // 类型 f64
5f32;            // 类型 f32
let x: f64 = 2.; // 类型 f64
```

r[expr.literal.float.result]
该表达式的值由该 token 的字符串表示按如下方式确定：

r[expr.literal.float.type-suffix-stripped]
* 从该字符串中移除任何后缀。

r[expr.literal.float.separators-stripped]
* 从该字符串中移除所有下划线。

r[expr.literal.float.value]
* 将该字符串转换为该表达式的类型，如同使用 [`f32::from_str`] 或 [`f64::from_str`]。

> **注意**
> 例如，`-1.0` 是对字面量表达式 `1.0` 应用[取负运算符][negation operator]，而不是单个浮点字面量表达式。

> **注意**
> `inf` 和 `NaN` 不是字面量 token。可以使用 [`f32::INFINITY`]、[`f64::INFINITY`]、[`f32::NAN`] 和 [`f64::NAN`] 常量来代替字面量表达式。在 `rustc` 中，大到会被求值为无穷大的字面量会触发 `overflowing_literals` lint 检查。

r[expr.literal.bool]
## 布尔字面量表达式

r[expr.literal.bool.intro]
布尔字面量表达式由关键字 `true` 或 `false` 之一组成。

r[expr.literal.bool.result]
该表达式的类型是原始[布尔类型][boolean type]，其值为：
 * 关键字为 `true` 时为 true
 * 关键字为 `false` 时为 false

[Escape]: #escapes
[Simple escape]: #simple-escapes
[Simple escapes]: #simple-escapes
[8-bit escape]: #8-bit-escapes
[8-bit escapes]: #8-bit-escapes
[7-bit escape]: #7-bit-escapes
[7-bit escapes]: #7-bit-escapes
[Unicode escape]: #unicode-escapes
[Unicode escapes]: #unicode-escapes
[String continuation escape]: #string-continuation-escapes
[String continuation escapes]: #string-continuation-escapes
[boolean type]: ../types/boolean.md
[constant expression]: ../const_eval.md#constant-expressions
[CStr]: core::ffi::CStr
[floating-point types]: ../types/numeric.md#floating-point-types
[lint check]: ../attributes/diagnostics.md#lint-check-attributes
[literal tokens]: ../tokens.md#literals
[numeric cast]: operator-expr.md#numeric-cast
[numeric types]: ../types/numeric.md
[suffix]: ../tokens.md#suffixes
[negation operator]: operator-expr.md#negation-operators
[overflow]: operator-expr.md#overflow
[Unicode scalar value]: http://www.unicode.org/glossary/#unicode_scalar_value
[Unicode scalar values]: http://www.unicode.org/glossary/#unicode_scalar_value
[`char`]: ../types/char.md
[`f32::from_str`]: ../../core/primitive.f32.md#method.from_str
[`f64::from_str`]: ../../core/primitive.f64.md#method.from_str
[`str`]: ../types/str.md
