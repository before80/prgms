+++
title = "02-Extern crate"
date = 2026-08-18T08:45:00+08:00
weight = 19
type = "docs"
description = "Extern crate — The Rust Reference"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Reference](https://doc.rust-lang.org/reference/)

> 原文链接: [https://doc.rust-lang.org/reference/items/extern-crates.html](https://doc.rust-lang.org/reference/items/extern-crates.html)

r[items.extern-crate]
# Extern crate

r[items.extern-crate.syntax]
```grammar,items
ExternCrate -> `extern` `crate` CrateRef AsClause? `;`

CrateRef -> IDENTIFIER | `self`

AsClause -> `as` ( IDENTIFIER | `_` )
```

r[items.extern-crate.intro]
*`extern crate` 声明*指定对外部 crate 的依赖。

r[items.extern-crate.namespace]
随后，该外部 crate 以给定的[标识符][identifier]绑定到声明所在作用域的[类型命名空间][type namespace]中。

r[items.extern-crate.extern-prelude]
此外，若 `extern crate` 出现在 crate 根中，则 crate 名也会加入[extern prelude]，从而在所有模块中自动进入作用域。

r[items.extern-crate.as]
`as` 子句可用于将导入的 crate 绑定到不同的名称。

r[items.extern-crate.lookup]
外部 crate 在编译期解析为特定的 `soname`，并向链接器传递对该 `soname` 的运行时链接需求，以便在运行时加载。`soname` 在编译期通过扫描编译器的库路径，并将可选的 `crate_name` 与该外部 crate 编译时所声明的 [`crate_name` 属性][`crate_name` attributes]相匹配来解析。若未提供 `crate_name`，则假定一个默认的 `name` 属性，等于 `extern crate` 声明中给出的[标识符][identifier]。

r[items.extern-crate.self]
可以导入 `self` crate，从而创建对当前 crate 的绑定。此时必须使用 `as` 子句指定要绑定到的名称。

三则 `extern crate` 声明的例子：

<!-- ignore: requires external crates -->
```rust
extern crate pcre;

extern crate std; // 等价于：extern crate std as std;

extern crate std as ruststd; // 以另一个名称链接到 'std'
```

r[items.extern-crate.name-restrictions]
为 Rust crate 命名时不允许使用连字符。不过 Cargo 包可以使用它们。在这种情况下，当 `Cargo.toml` 未指定 crate 名时，Cargo 会透明地将 `-` 替换为 `_`（更多细节参见 [RFC 940]）。

示例如下：

<!-- ignore: requires external crates -->
```rust
// 导入 Cargo 包 hello-world
extern crate hello_world; // 连字符被替换为下划线
```

r[items.extern-crate.underscore]
## 下划线导入

r[items.extern-crate.underscore.intro]
可以使用带下划线的形式 `extern crate foo as _` 声明外部 crate 依赖而不将其名称绑定到作用域中。这对于只需链接、从不被引用的 crate 可能有用，并能避免被报告为未使用。

r[items.extern-crate.underscore.macro_use]
[`macro_use` 属性][`macro_use` attribute]照常工作，并将宏名称导入 [`macro_use` prelude]。

<!-- template:attributes -->
r[items.extern-crate.no_link]
## `no_link` 属性

r[items.extern-crate.no_link.intro]
*`no_link` [属性][attributes]*可以应用于 `extern crate` 项，以阻止链接该 crate。

> **注意**
> 这很有用，例如只需要某个 crate 的宏时。

> [!EXAMPLE]
> <!-- ignore: requires external crates -->
> ```rust
> #[no_link]
> extern crate other_crate;
>
> other_crate::some_macro!();
> ```

r[items.extern-crate.no_link.syntax]
`no_link` 属性使用 [MetaWord] 语法。

r[items.extern-crate.no_link.allowed-positions]
`no_link` 属性只能应用于 `extern crate` 声明。

> **注意**
> `rustc` 会忽略其他位置上的使用，但会对其发出 lint。将来这可能变为错误。

r[items.extern-crate.no_link.duplicates]
只有第一次在 `extern crate` 声明上使用 `no_link` 会生效。

> **注意**
> `rustc` 会对第一次之后的任何使用发出 lint。将来这可能变为错误。

[identifier]: ../identifiers.md
[RFC 940]: https://github.com/rust-lang/rfcs/blob/master/text/0940-hyphens-considered-harmful.md
[`macro_use` attribute]: ../macros-by-example.md#the-macro_use-attribute
[extern prelude]: ../names/preludes.md#extern-prelude
[`macro_use` prelude]: ../names/preludes.md#macro_use-prelude
[`crate_name` attributes]: ../crates-and-source-files.md#the-crate_name-attribute
[type namespace]: ../names/namespaces.md
