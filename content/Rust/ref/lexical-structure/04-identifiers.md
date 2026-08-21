+++
title = "04-标识符"
date = 2026-08-18T08:45:00+08:00
weight = 8
type = "docs"
description = "标识符 — The Rust Reference"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Reference](https://doc.rust-lang.org/reference/)

> 原文链接: [https://doc.rust-lang.org/reference/identifiers.html](https://doc.rust-lang.org/reference/identifiers.html)

r[ident]
# 标识符

r[ident.syntax]
```grammar,lexer
IDENTIFIER_OR_KEYWORD -> ( XID_Start | `_` ) XID_Continue*

XID_Start -> <`XID_Start` defined by Unicode>

XID_Continue -> <`XID_Continue` defined by Unicode>

RAW_IDENTIFIER -> `r#` IDENTIFIER_OR_KEYWORD

NON_KEYWORD_IDENTIFIER -> IDENTIFIER_OR_KEYWORD _except a [strict][lex.keywords.strict] or [reserved][lex.keywords.reserved] keyword_

IDENTIFIER -> NON_KEYWORD_IDENTIFIER | RAW_IDENTIFIER

RESERVED_RAW_IDENTIFIER ->
    `r#` (`_` | `crate` | `self` | `Self` | `super`) !XID_Continue
```

<!-- When updating the version, update the UAX links, too. -->
r[ident.unicode]
标识符遵循 [Unicode 标准附录 #31][UAX31] 中针对 Unicode 17.0 版本的规范，并加上下文所述的补充。标识符的一些例子：

* `foo`
* `_identifier`
* `r#true`
* `Москва`
* `東京`

r[ident.profile]
从 UAX #31 使用的配置文件为：

* Start := [`XID_Start`]，外加下划线字符（U+005F）
* Continue := [`XID_Continue`]
* Medial := 空

> **注意**
> 以下划线开头的标识符通常用于表示有意不使用的标识符，并会在 `rustc` 中消除未使用警告。

r[ident.keyword]
若没有下文 [原始标识符](#原始标识符) 中所述的 `r#` 前缀，标识符不得为 [严格][strict] 或 [保留][reserved] 关键字。

r[ident.zero-width-chars]
标识符中不允许零宽非连接符（ZWNJ U+200C）和零宽连接符（ZWJ U+200D）字符。

r[ident.ascii-limitations]
在下列情形中，标识符被限制为 [`XID_Start`] 和 [`XID_Continue`] 的 ASCII 子集：

* [`extern crate`] 声明（[AsClause] 标识符除外）
* 路径中引用的外部 crate 名
* 没有 [`path` 属性][`path` attribute] 而从文件系统加载的 [模块][Module] 名
* 带 [`no_mangle`] 属性的项
* [外部块][external blocks] 中的项名

r[ident.normalization]
## 规范化

标识符使用 [Unicode 标准附录 #15][UAX15] 中定义的规范化形式 C（NFC）进行规范化。两个标识符若其 NFC 形式相等则相等。

[过程宏][proc-macro] 和 [声明宏][mbe] 在其输入中接收规范化后的标识符。

r[ident.raw]
## 原始标识符

r[ident.raw.intro]
原始标识符与普通标识符类似，但带有 `r#` 前缀。（注意 `r#` 前缀并不包含在实际标识符中。）

r[ident.raw.allowed]
与普通标识符不同，原始标识符可以是除上文 `RAW_IDENTIFIER` 所列之外的任何严格或保留关键字。

r[ident.raw.reserved]
使用 [RESERVED_RAW_IDENTIFIER] token 是错误。

[`extern crate`]: items/extern-crates.md
[`no_mangle`]: abi.md#the-no_mangle-attribute
[`path` attribute]: items/modules.md#the-path-attribute
[`XID_Continue`]: http://unicode.org/cldr/utility/list-unicodeset.jsp?a=%5B%3AXID_Continue%3A%5D&abb=on&g=&i=
[`XID_Start`]:  http://unicode.org/cldr/utility/list-unicodeset.jsp?a=%5B%3AXID_Start%3A%5D&abb=on&g=&i=
[external blocks]: items/external-blocks.md
[mbe]: macros-by-example.md
[module]: items/modules.md
[path]: paths.md
[proc-macro]: procedural-macros.md
[reserved]: keywords.md#reserved-keywords
[strict]: keywords.md#strict-keywords
[UAX15]: https://www.unicode.org/reports/tr15/tr15-57.html
[UAX31]: https://www.unicode.org/reports/tr31/tr31-43.html
