+++
title = "第1章 记号"
date = 2026-08-18T08:45:00+08:00
weight = 3
type = "docs"
description = "记号 — The Rust Reference"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Reference](https://doc.rust-lang.org/reference/)

> 原文链接: [https://doc.rust-lang.org/reference/notation.html](https://doc.rust-lang.org/reference/notation.html)

r[notation]
# 记号

r[notation.grammar]
## 文法

r[notation.grammar.syntax]

*词法分析器（Lexer）* 与 *语法（Syntax）* 文法片段使用下列记号：

| 记号              | 示例                          | 含义                                      |
|-------------------|-------------------------------|-------------------------------------------|
| CAPITAL           | KW_IF, INTEGER_LITERAL        | 词法分析器产生的 token                    |
| _ItalicCamelCase_ | _LetStatement_, _Item_        | 语法产生式                                |
| `string`          | `x`, `while`, `*`             | 精确的一个或多个字符                      |
| x<sup>?</sup>     | `pub`<sup>?</sup>             | 可选的项                                  |
| x<sup>\*</sup>    | _OuterAttribute_<sup>\*</sup> | 0 个或多个 x                              |
| x<sup>+</sup>     |  _MacroMatch_<sup>+</sup>     | 1 个或多个 x                              |
| x<sup>a..b</sup>  | HEX_DIGIT<sup>1..6</sup>      | x 重复 a 到 b 次，不含 b                  |
| x<sup>a..=b</sup> | HEX_DIGIT<sup>1..=5</sup>     | x 重复 a 到 b 次，含 b                    |
| x<sup>n:a..=b</sup> | `#`<sup>n:1..=255</sup>      | x 重复 a 到 b 次（含 b），次数绑定到名称 n |
| x<sup>n</sup>     | `#`<sup>n</sup>               | x 按先前带标签重复所绑定的 n 次重复       |
| Rule1 Rule2       | `fn` _Name_ _Parameters_      | 按顺序排列的规则序列                      |
| \|                | `u8` \| `u16`, Block \| Item  | 二者择一                                  |
| !                 | !COMMENT                      | 若该表达式并不紧随其后则匹配，且不消耗任何输入 |
| \[ ]               | \[`b` `B`]                     | 所列出的任意字符                          |
| \[ - ]             | \[`a`-`z`]                     | 该范围内的任意字符                        |
| ~\[ ]              | ~\[`b` `B`]                    | 除所列之外的任意字符                      |
| ~`string`         | ~`\n`, ~`*/`                  | 除该序列之外的任意字符                    |
| ( )               | (`,` _Parameter_)<sup>?</sup> | 将项分组                                  |
| ^                 | `b'` ^ ASCII_FOR_CHAR         | 序列的其余部分必须匹配，否则无条件分析失败（[硬切断运算符][hard cut operator]） |
| U+xxxx..xxxxxx    | U+0060                        | 单个 Unicode 字符                         |
| \<text\>          | \<除 CR 外的任意 ASCII 字符\>  | 对应匹配内容的文字描述                    |
| Rule <sub>suffix</sub> | IDENTIFIER_OR_KEYWORD <sub>_except `crate`_</sub> | 对前一规则的修改 |
| // Comment. | // 单行注释。 | 延伸到行尾的注释。 |

序列的优先级高于 `|` 选择。

r[notation.grammar.cut]
### 硬切断运算符

文法使用有序选择：分析器从左到右尝试各备选，并采用第一个匹配者。若某个备选在序列中途失败，分析器通常会回溯并尝试下一个备选。切断运算符（`^`）阻止这种回溯。一旦序列中 `^` 左侧的每个表达式都已匹配，序列的其余部分必须匹配，否则分析无条件失败。

Mizushima 等人将 [切断运算符][cut operator paper] 引入了解析表达式文法。在 PEG 文献中，*软切断（soft cut）* 仅阻止紧邻包围的有序选择之内的回溯——外层选择仍可恢复。*硬切断（hard cut）* 阻止越过切断点的一切回溯；失败是确定的。本文法中使用的 `^` 是硬切断。

之所以需要硬切断运算符，是因为 Rust 中有些 token 以本身也是合法 token 的前缀开头。例如，`c"` 开始一个 C 字符串字面量，但单独的 `c` 是合法标识符。若没有切断，当 `c"\0"` 未能作为 C 字符串字面量进行词法分析时（因为 C 字符串中不允许空字节），分析器可能回溯并将其分析为两个 token：标识符 `c` 和字符串字面量 `"\0"`。[`c"` 之后的切断][cut after `c"`] 阻止了这一点——一旦识别出开定界符，分析器就不能回头。同样的理由也适用于 [字节字面量][byte literals]、[字节字符串字面量][byte string literals]、[原始字符串字面量][raw string literals]，以及其他带有本身即为合法 token 的前缀的字面量。

r[notation.grammar.string-tables]
### 字符串表产生式

文法中的某些规则——特别是 [一元运算符][unary operators]、[二元
运算符][binary operators] 和 [关键字][keywords]——以简化形式给出：即一份
可打印字符串的列表。这些情形构成关于
[token][tokens] 规则的规则的一个子集，并被假定为词法分析
阶段的结果，该阶段由一台 <abbr title="Deterministic Finite
Automaton">DFA</abbr> 驱动，向分析器提供输入，并在所有此类字符串表
条目的析取之上运行。

当文法中出现 `monospace` 字体的此类字符串时，
它是对此类字符串表产生式中单个成员的隐式引用。
更多信息见 [tokens]。

r[notation.grammar.visualizations]
### 文法可视化

每个文法块下方都有一个按钮，用于切换 [语法图][syntax diagram] 的显示。方形元素是非终结规则，圆角矩形是终结符。

[binary operators]: expressions/operator-expr.md#arithmetic-and-logical-binary-operators
[byte literals]: tokens.md#r-lex.token.byte.syntax
[byte string literals]: tokens.md#r-lex.token.str-byte.syntax
[cut after `c"`]: tokens.md#r-lex.token.str-c.syntax
[cut operator paper]: https://kmizu.github.io/papers/paste513-mizushima.pdf
[hard cut operator]: notation.md#the-hard-cut-operator
[keywords]: keywords.md
[raw string literals]: tokens.md#r-lex.token.literal.str-raw.syntax
[syntax diagram]: https://en.wikipedia.org/wiki/Syntax_diagram
[tokens]: tokens.md
[unary operators]: expressions/operator-expr.md#borrow-operators
