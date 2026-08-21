+++
title = "01-示例宏"
date = 2026-08-18T08:45:00+08:00
weight = 13
type = "docs"
description = "示例宏 — The Rust Reference"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Reference](https://doc.rust-lang.org/reference/)

> 原文链接: [https://doc.rust-lang.org/reference/macros-by-example.html](https://doc.rust-lang.org/reference/macros-by-example.html)

r[macro.decl]
# 示例宏

r[macro.decl.syntax]
```grammar,macros
MacroRulesDefinition ->
    `macro_rules` `!` IDENTIFIER MacroRulesDef

MacroRulesDef ->
      `(` MacroRules `)` `;`
    | `[` MacroRules `]` `;`
    | `{` MacroRules `}`

MacroRules ->
    MacroRule ( `;` MacroRule )* `;`?

MacroRule ->
    MacroMatcher `=>` MacroTranscriber

MacroMatcher ->
      `(` MacroMatch* `)`
    | `[` MacroMatch* `]`
    | `{` MacroMatch* `}`

MacroMatch ->
      Token _except `$` and [delimiters][lex.token.delim]_
    | MacroMatcher
    | `$` ( IDENTIFIER_OR_KEYWORD _except `crate`_ | RAW_IDENTIFIER ) `:` MacroFragSpec
    | `$` `(` MacroMatch+ `)` MacroRepSep? MacroRepOp

MacroFragSpec ->
      `block` | `expr` | `expr_2021` | `ident` | `item` | `lifetime` | `literal`
    | `meta` | `pat` | `pat_param` | `path` | `stmt` | `tt` | `ty` | `vis`

MacroRepSep -> Token _except [delimiters][lex.token.delim] and [MacroRepOp]_

MacroRepOp -> `*` | `+` | `?`

MacroTranscriber -> DelimTokenTree
```

r[macro.decl.intro]
`macro_rules` 允许用户以声明式方式定义语法扩展。我们称此类扩展为“示例宏”（macros by example），或简称“宏”。

每个示例宏都有一个名称，以及一条或多条 *规则*。每条规则有两部分：*匹配器*，描述它所匹配的语法；以及 *转写器*，描述将替换成功匹配的调用的语法。匹配器和转写器都必须由定界符包围。宏可以展开为表达式、语句、项（包括 trait、impl 和外部项）、类型或模式。

r[macro.decl.transcription]
## 转写

r[macro.decl.transcription.intro]
当宏被调用时，宏展开器按名称查找宏调用，并依次尝试每条宏规则。它转写第一次成功的匹配；若这导致错误，则不再尝试后续匹配。

r[macro.decl.transcription.lookahead]
匹配时不进行前瞻；若编译器无法一次一个 token 地无歧义地确定如何分析该宏调用，则为错误。在下列示例中，编译器不会越过标识符向前看下一个 token 是否为 `)`，即使那样做能让它无歧义地分析该调用：

```rust
macro_rules! ambiguity {
    ($($i:ident)* $j:ident) => { };
}

ambiguity!(error); // Error: 局部歧义
```

r[macro.decl.transcription.syntax]
在匹配器和转写器中，`$` token 用于调用宏引擎的特殊行为（下文在 [元变量][Metavariables] 和 [重复][Repetitions] 中描述）。不属于此类调用的 token 按字面匹配和转写，有一个例外。例外是匹配器的外层定界符将匹配任意一对定界符。因此，例如，匹配器 `(())` 将匹配 `{()}` 但不匹配 `{{}}`。字符 `$` 不能按字面匹配或转写。

r[macro.decl.transcription.fragment]
### 转发已匹配的片段

当把已匹配的片段转发给另一个示例宏时，第二个宏中的匹配器会看到该片段类型的不透明 AST。第二个宏不能用字面 token 来匹配匹配器中的这些片段，只能使用相同类型的片段说明符。`ident`、`lifetime` 和 `tt` 片段类型是例外，*可以* 由字面 token 匹配。下列代码说明了这一限制：

```rust
macro_rules! foo {
    ($l:expr) => { bar!($l); }
// ERROR:               ^^ 宏调用中没有规则期望此 token
}

macro_rules! bar {
    (3) => {}
}

foo!(3);
```

下列代码说明在匹配 `tt` 片段之后如何直接匹配 token：

```rust
// 编译通过
macro_rules! foo {
    ($l:tt) => { bar!($l); }
}

macro_rules! bar {
    (3) => {}
}

foo!(3);
```

r[macro.decl.meta]
## 元变量

r[macro.decl.meta.intro]
在匹配器中，`$` *name* `:` *fragment-specifier* 匹配指定种类的 Rust 语法片段，并将其绑定到元变量 `$`*name*。

r[macro.decl.meta.specifier]
合法的片段说明符有：

  * `block`：一个 [BlockExpressionNoInnerAttributes]
  * `expr`：一个 [Expression]
  * `expr_2021`：一个 [Expression]，但 [UnderscoreExpression] 和 [ConstBlockExpression] 除外（见 [macro.decl.meta.edition2024]）
  * `ident`：一个 [IDENTIFIER_OR_KEYWORD]，但 `_`、[RAW_IDENTIFIER] 或 [`$crate`] 除外
  * `item`：一个 [Item]
  * `lifetime`：一个 [LIFETIME_TOKEN]
  * `literal`：匹配 `-`<sup>?</sup>[LiteralExpression]
  * `meta`：一个 [Attr]，即属性的内容
  * `pat`：一个 [Pattern]（见 [macro.decl.meta.edition2021]）
  * `pat_param`：一个 [PatternNoTopAlt]
  * `path`：一个 [TypePath]
  * `stmt`：一个不带尾部分号的 [Statement][grammar-Statement]（需要分号的项语句除外）
  * `tt`：一个 [TokenTree]&nbsp;（单个 [token] 或位于配对定界符 `()`、`[]` 或 `{}` 中的 token）
  * `ty`：一个 [Type][grammar-Type]
  * `vis`：一个可能为空的 [Visibility] 限定符

r[macro.decl.meta.transcription]
在转写器中，元变量仅通过 `$`*name* 引用，因为片段种类已在匹配器中指定。元变量被替换为匹配它们的语法元素。元变量可以被转写多次，也可以完全不被转写。

r[macro.decl.meta.dollar-crate]
关键字元变量 [`$crate`] 可用于引用当前 crate。

r[macro.decl.meta.edition2021]
> [!EDITION-2021]
> 从 2021 edition 开始，`pat` 片段说明符匹配顶层 or 模式（即它们接受 [Pattern]）。
>
> 在 2021 edition 之前，它们匹配与 `pat_param` 完全相同的片段（即它们接受 [PatternNoTopAlt]）。
>
> 相关的 edition 是对 `macro_rules!` 定义生效的那个。

r[macro.decl.meta.edition2024]
> [!EDITION-2024]
> 在 2024 edition 之前，`expr` 片段说明符在顶层不匹配 [UnderscoreExpression] 或 [ConstBlockExpression]。它们在子表达式内是允许的。
>
> `expr_2021` 片段说明符的存在是为了与 2024 之前的 edition 保持向后兼容。

r[macro.decl.repetition]
## 重复

r[macro.decl.repetition.intro]
在匹配器和转写器中，通过把要重复的 token 放在 `$(`…`)` 内，后跟重复运算符，并可选地在其间放置分隔 token，来表示重复。

r[macro.decl.repetition.separator]
分隔 token 可以是除定界符或重复运算符之一以外的任何 token，但 `;` 和 `,` 最常见。例如，`$( $i:ident ),*` 表示任意数量的由逗号分隔的标识符。允许嵌套重复。

r[macro.decl.repetition.operators]
重复运算符为：

- `*` —— 表示任意次数的重复。
- `+` —— 表示任意次数但至少一次。
- `?` —— 表示零次或一次出现的可选片段。

r[macro.decl.repetition.optional-restriction]
由于 `?` 表示至多一次出现，它不能与分隔符一起使用。

r[macro.decl.repetition.fragment]
重复的片段既匹配也转写为指定数量的该片段，由分隔 token 分隔。元变量被匹配到其对应片段的每一次重复。例如，上文的 `$( $i:ident ),*` 示例将 `$i` 匹配到列表中的所有标识符。

在转写期间，对重复还有额外限制，以便编译器知道如何正确地展开它们：

1.  元变量在转写器中出现的重复次数、种类和嵌套顺序必须与它在匹配器中完全相同。因此对于匹配器 `$( $i:ident ),*`，转写器 `=> { $i }`、`=> { $( $( $i )* )* }` 和 `=> { $( $i )+ }` 都是非法的，但 `=> { $( $i );* }` 是正确的，并将逗号分隔的标识符列表替换为分号分隔的列表。
2.  转写器中的每个重复必须包含至少一个元变量，以决定展开多少次。若同一重复中出现多个元变量，它们必须绑定到相同数量的片段。例如，`( $( $i:ident ),* ; $( $j:ident ),* ) => (( $( ($i,$j) ),* ))` 必须将相同数量的 `$i` 片段与 `$j` 片段绑定。这意味着用 `(a, b, c; d, e, f)` 调用该宏是合法的，并展开为 `((a,d), (b,e), (c,f))`，但 `(a, b, c; d, e)` 是非法的，因为数量不同。此要求适用于嵌套重复的每一层。

r[macro.decl.scope]
## 作用域、导出与导入

r[macro.decl.scope.intro]
由于历史原因，示例宏的作用域并不完全像项那样工作。宏有两种形式的作用域：文本作用域，以及基于路径的作用域。文本作用域基于事物在源文件中出现的顺序，甚至可以跨越多个文件，并且是默认作用域。下文将进一步说明。基于路径的作用域与项的作用域工作方式完全相同。宏的作用域、导出和导入很大程度上由属性控制。

r[macro.decl.scope.unqualified]
当宏由非限定标识符（不是多段路径的一部分）调用时，首先在文本作用域中查找。若这没有产生任何结果，则在基于路径的作用域中查找。若宏的名称带有路径限定，则只在基于路径的作用域中查找。

<!-- ignore: requires external crates -->
```rust
use lazy_static::lazy_static; // 基于路径的导入。

macro_rules! lazy_static { // 文本定义。
    (lazy) => {};
}

lazy_static!{lazy} // 文本查找首先找到我们的宏。
self::lazy_static!{} // 基于路径的查找忽略我们的宏，找到导入的那个。
```

r[macro.decl.scope.textual]
### 文本作用域

r[macro.decl.scope.textual.intro]
文本作用域很大程度上基于事物在源文件中出现的顺序，其工作方式类似于用 `let` 声明的局部变量的作用域，只是它也适用于模块级。当使用 `macro_rules!` 定义宏时，该宏在定义之后进入作用域（注意它仍可递归使用，因为名称是从调用点查找的），直到其外围作用域（通常是一个模块）关闭。这可以进入子模块，甚至跨越多个文件：

<!-- ignore: requires external modules -->
```rust
//// src/lib.rs
mod has_macro {
    // m!{} // Error: m 不在作用域中。

    macro_rules! m {
        () => {};
    }
    m!{} // OK: 出现在 m 的声明之后。

    mod uses_macro;
}

// m!{} // Error: m 不在作用域中。

//// src/has_macro/uses_macro.rs

m!{} // OK: 出现在 src/lib.rs 中 m 的声明之后
```

r[macro.decl.scope.textual.shadow]
多次定义同一个宏不是错误；最近的声明将遮蔽前一个，除非前一个已离开作用域。

```rust
macro_rules! m {
    (1) => {};
}

m!(1);

mod inner {
    m!(1);

    macro_rules! m {
        (2) => {};
    }
    // m!(1); // Error: 没有规则匹配 '1'
    m!(2);

    macro_rules! m {
        (3) => {};
    }
    m!(3);
}

m!(1);
```

宏也可以在函数内部局部声明和使用，工作方式类似：

```rust
fn foo() {
    // m!(); // Error: m 不在作用域中。
    macro_rules! m {
        () => {};
    }
    m!();
}

// m!(); // Error: m 不在作用域中。
```

r[macro.decl.scope.textual.shadow.path-based]
宏的文本作用域名称绑定会遮蔽指向宏的基于路径的作用域绑定。

```rust
macro_rules! m2 {
    () => {
        println!("m2");
    };
}

// 解析为下方 use 声明的基于路径的候选。
m!(); // 打印 "m2\n"

// 为 `m` 引入第二个文本作用域候选。
//
// 这会遮蔽下方基于路径的候选，直到本示例其余部分结束。
macro_rules! m {
    () => {
        println!("m");
    };
}

// 将 `m2` 宏引入为基于路径的候选。
//
// 该项在本示例的整个范围内都在作用域中，而不仅是
// use 声明之下。
use m2 as m;

// 解析为 use 声明之上的文本宏候选。
m!(); // 打印 "m\n"
```

> **注意**
> 不允许遮蔽的情形见 [名称解析歧义][name resolution ambiguities]。

r[macro.decl.scope.path-based]
### 基于路径的作用域

r[macro.decl.scope.path-based.intro]
默认情况下，宏没有基于路径的作用域。宏可通过两种方式获得基于路径的作用域：

- [use 声明再导出][Use declaration re-export]
- [`macro_export`]

r[macro.decl.scope.path.reexport]
宏可以被再导出，以从 crate 根以外的模块赋予它们基于路径的作用域。

```rust
mac::m!(); // OK: 基于路径的查找在 mac 模块中找到 `m`。

mod mac {
    // 以文本作用域引入宏 `m`。
    macro_rules! m {
        () => {};
    }

    // 从 `m` 的文本作用域内再导出，带基于路径的作用域。
    pub(crate) use m;
}
```

r[macro.decl.scope.path-based.visibility]
宏有隐式可见性 `pub(crate)`。`#[macro_export]` 将隐式可见性改为 `pub`。

```rust
// 隐式可见性是 `pub(crate)`。
macro_rules! private_m {
    () => {};
}

// 隐式可见性是 `pub`。
#[macro_export]
macro_rules! pub_m {
    () => {};
}

pub(crate) use private_m as private_macro; // OK.
pub use pub_m as pub_macro; // OK.
```

```rust
## // 隐式可见性是 `pub(crate)`。
## macro_rules! private_m {
##     () => {};
## }
#
## // 隐式可见性是 `pub`。
## #[macro_export]
## macro_rules! pub_m {
##     () => {};
## }
#
## pub(crate) use private_m as private_macro; // OK.
## pub use pub_m as pub_macro; // OK.
#
pub use private_m; // ERROR: `private_m` 仅在 crate 内公开
                   // 而不能被再导出到外部。
```

<!-- template:attributes -->
r[macro.decl.scope.macro_use]
### `macro_use` 属性

r[macro.decl.scope.macro_use.intro]
*`macro_use` [属性][attributes]* 有两个用途：它可用在模块上以扩展在其中定义的宏的作用域，也可用在 [`extern crate`][items.extern-crate] 上以从另一个 crate 将宏导入到 [`macro_use` prelude] 中。

> [!EXAMPLE]
> ```rust
> #[macro_use]
> mod inner {
>     macro_rules! m {
>         () => {};
>     }
> }
> m!();
> ```
>
> ```rust
> #[macro_use]
> extern crate log;
> ```

r[macro.decl.scope.macro_use.syntax]
用在模块上时，`macro_use` 属性使用 [MetaWord] 语法。

用在 `extern crate` 上时，它使用 [MetaWord] 和 [MetaListIdents] 语法。这些语法如何使用，见 [macro.decl.scope.macro_use.prelude]。

r[macro.decl.scope.macro_use.allowed-positions]
`macro_use` 属性可以应用于模块或 `extern crate`。

> **注意**
> `rustc` 忽略其他位置上的使用，但会对其发出 lint。将来这可能变成错误。

r[macro.decl.scope.macro_use.extern-crate-self]
`macro_use` 属性不得用在 [`extern crate self`] 上。

r[macro.decl.scope.macro_use.duplicates]
`macro_use` 属性可以在一个形式上使用任意次数。

可以指定多个 [MetaListIdents] 语法的 `macro_use` 实例。将导入所有指定宏的并集。

> **注意**
> 在模块上，`rustc` 会对第一个之后的任何 [MetaWord] `macro_use` 属性发出 lint。
>
> 在 `extern crate` 上，`rustc` 会对因未导入任何尚未被另一个 `macro_use` 属性导入的宏而没有效果的任何 `macro_use` 属性发出 lint。若两个或更多 [MetaListIdents] `macro_use` 属性导入同一个宏，则对第一个发出 lint。若存在任何 [MetaWord] `macro_use` 属性，则对所有 [MetaListIdents] `macro_use` 属性发出 lint。若存在两个或更多 [MetaWord] `macro_use` 属性，则对第一个之后的那些发出 lint。

r[macro.decl.scope.macro_use.mod-decl]
当 `macro_use` 用在模块上时，该模块的宏作用域延伸到模块的词法作用域之外。

> [!EXAMPLE]
> ```rust
> #[macro_use]
> mod inner {
>     macro_rules! m {
>         () => {};
>     }
> }
> m!(); // OK
> ```

r[macro.decl.scope.macro_use.prelude]
在 crate 根的 `extern crate` 声明上指定 `macro_use` 会导入该 crate 中导出的宏。

以这种方式导入的宏被导入到 [`macro_use` prelude] 中，而不是按文本导入，这意味着它们可以被任何其他名称遮蔽。由 `macro_use` 导入的宏可以在导入语句之前使用。

> **注意**
> 发生冲突时，`rustc` 目前偏好最后导入的宏。不要依赖这一点。这种行为不寻常，因为 Rust 中的导入通常与顺序无关。`macro_use` 的这种行为将来可能改变。
>
> 细节见 [Rust issue #148025](https://github.com/rust-lang/rust/issues/148025)。

使用 [MetaWord] 语法时，导入所有导出的宏。使用 [MetaListIdents] 语法时，只导入指定的宏。

> [!EXAMPLE]
> <!-- ignore: requires external crates -->
> ```rust
> #[macro_use(lazy_static)] // 或 `#[macro_use]` 以导入所有宏。
> extern crate lazy_static;
>
> lazy_static!{}
> // self::lazy_static!{} // ERROR: lazy_static 未在 `self` 中定义。
> ```

r[macro.decl.scope.macro_use.export]
要用 `macro_use` 导入的宏必须用 [`macro_export`][macro.decl.scope.macro_export] 导出。

<!-- template:attributes -->
r[macro.decl.scope.macro_export]
### `macro_export` 属性

r[macro.decl.scope.macro_export.intro]
*`macro_export` [属性][attributes]* 将该宏从 crate 中导出，并使其在 crate 根中可用于基于路径的解析。

> [!EXAMPLE]
> ```rust
> self::m!();
> //  ^^^^ OK: 基于路径的查找在当前模块中找到 `m`。
> m!(); // 同上。
>
> mod inner {
>     super::m!();
>     crate::m!();
> }
>
> mod mac {
>     #[macro_export]
>     macro_rules! m {
>         () => {};
>     }
> }
> ```

r[macro.decl.scope.macro_export.syntax]
`macro_export` 属性使用 [MetaWord] 和 [MetaListIdents] 语法。使用 [MetaListIdents] 语法时，它接受单个 [`local_inner_macros`][macro.decl.scope.macro_export.local_inner_macros] 值。

r[macro.decl.scope.macro_export.allowed-positions]
`macro_export` 属性可以应用于 `macro_rules` 定义。

> **注意**
> `rustc` 忽略其他位置上的使用，但会对其发出 lint。将来这可能变成错误。

r[macro.decl.scope.macro_export.duplicates]
只有宏上第一次使用 `macro_export` 有效果。

> **注意**
> `rustc` 会对第一次之后的任何使用发出 lint。

r[macro.decl.scope.macro_export.path-based]
默认情况下，宏只有 [文本作用域][macro.decl.scope.textual]，不能通过路径解析。使用 `macro_export` 属性时，该宏在 crate 根中可用，并可通过其路径引用。

> [!EXAMPLE]
> 没有 `macro_export` 时，宏只有文本作用域，因此对该宏的基于路径的解析会失败。
>
> ```rust
> macro_rules! m {
>     () => {};
> }
> self::m!(); // ERROR
> crate::m!(); // ERROR
> # fn main() {}
> ```
>
> 有了 `macro_export`，基于路径的解析可以工作。
>
> ```rust
> #[macro_export]
> macro_rules! m {
>     () => {};
> }
> self::m!(); // OK
> crate::m!(); // OK
> # fn main() {}
> ```

r[macro.decl.scope.macro_export.export]
`macro_export` 属性使宏从 crate 根导出，从而可以在其他 crate 中通过路径引用。

> [!EXAMPLE]
> 给定 `log` crate 中的下列内容：
>
> ```rust
> #[macro_export]
> macro_rules! warn {
>     ($message:expr) => { eprintln!("WARN: {}", $message) };
> }
> ```
>
> 从另一个 crate，你可以通过路径引用该宏：
>
> <!-- ignore: requires external crates -->
> ```rust
> fn main() {
>     log::warn!("example warning");
> }
> ```

r[macro.decl.scope.macro_export.macro_use]
`macro_export` 允许在 `extern crate` 上使用 [`macro_use`][macro.decl.scope.macro_use]，以将该宏导入到 [`macro_use` prelude] 中。

> [!EXAMPLE]
> 给定 `log` crate 中的下列内容：
>
> ```rust
> #[macro_export]
> macro_rules! warn {
>     ($message:expr) => { eprintln!("WARN: {}", $message) };
> }
> ```
>
> 在依赖 crate 中使用 `macro_use` 允许你从 prelude 使用该宏：
>
> <!-- ignore: requires external crates -->
> ```rust
> #[macro_use]
> extern crate log;
>
> pub mod util {
>     pub fn do_thing() {
>         // 通过宏 prelude 解析。
>         warn!("example warning");
>     }
> }
> ```

r[macro.decl.scope.macro_export.local_inner_macros]
在 `macro_export` 属性中加入 `local_inner_macros` 会使宏定义中所有单段宏调用带有隐式 `$crate::` 前缀。

> **注意**
> 这主要是作为工具，用于将在 [`$crate`] 加入语言之前编写的代码迁移为能与 Rust 2018 基于路径的宏导入一起工作。不鼓励在新代码中使用它。

> [!EXAMPLE]
> ```rust
> #[macro_export(local_inner_macros)]
> macro_rules! helped {
>     () => { helper!() } // 自动转换为 $crate::helper!()。
> }
>
> #[macro_export]
> macro_rules! helper {
>     () => { () }
> }
> ```

r[macro.decl.hygiene]
## 卫生性

r[macro.decl.hygiene.intro]
示例宏具有 *混合位点卫生性*。这意味着 [循环标签][loop labels]、[块标签][block labels] 和局部变量在宏定义点查找，而其他符号在宏调用点查找。例如：

```rust
let x = 1;
fn func() {
    unreachable!("this is never called")
}

macro_rules! check {
    () => {
        assert_eq!(x, 1); // 使用定义点的 `x`。
        func();           // 使用调用点的 `func`。
    };
}

{
    let x = 2;
    fn func() { /* 不会 panic */ }
    check!();
}
```

在宏展开中定义的标签和局部变量不在各次调用之间共享，因此这段代码无法编译：

```rust
macro_rules! m {
    (define) => {
        let x = 1;
    };
    (refer) => {
        dbg!(x);
    };
}

m!(define);
m!(refer);
```

r[macro.decl.hygiene.crate]
一个特例是 `$crate` 元变量。它引用定义该宏的 crate，并可用于路径开头，以查找在调用点不在作用域中的项或宏。

<!-- ignore: requires external crates -->
```rust
//// helper_macro crate 中的定义。
#[macro_export]
macro_rules! helped {
    // () => { helper!() } // 这可能因 'helper' 不在作用域中而导致错误。
    () => { $crate::helper!() }
}

#[macro_export]
macro_rules! helper {
    () => { () }
}

//// 在另一个 crate 中使用。
// 注意 `helper_macro::helper` 并未被导入！
use helper_macro::helped;

fn unit() {
    helped!();
}
```

注意，因为 `$crate` 引用当前 crate，在引用非宏项时必须与完全限定的模块路径一起使用：

```rust
pub mod inner {
    #[macro_export]
    macro_rules! call_foo {
        () => { $crate::inner::foo() };
    }

    pub fn foo() {}
}
```

r[macro.decl.hygiene.vis]
此外，尽管 `$crate` 允许宏在展开时引用其自身 crate 内的项，它的使用对可见性没有影响。被引用的项或宏仍必须从调用点可见。在下列示例中，任何从 crate 外部调用 `call_foo!()` 的尝试都会失败，因为 `foo()` 不是公开的。

```rust
#[macro_export]
macro_rules! call_foo {
    () => { $crate::foo() };
}

fn foo() {}
```

> **注意**
> 在 Rust 1.30 之前，`$crate` 和 [`local_inner_macros`][macro.decl.scope.macro_export.local_inner_macros] 不受支持。它们与 [基于路径的宏导入][macro.decl.scope.macro_export] 一同加入，以确保辅助宏不必由导出宏的 crate 的用户手动导入。为更早版本的 Rust 编写、使用辅助宏的 crate 需要修改为使用 `$crate` 或 `local_inner_macros`，才能与基于路径的导入良好协作。

r[macro.decl.follow-set]
## Follow-set 歧义限制

r[macro.decl.follow-set.intro]
宏系统使用的分析器相当强大，但其能力受到限制，以防止当前或未来语言版本中的歧义。

r[macro.decl.follow-set.token-restriction]
特别地，除关于歧义展开的规则外，由元变量匹配的非终结符后面必须跟着已被判定可安全用在该类匹配之后的 token。

举例来说，像 `$i:expr [ , ]` 这样的宏匹配器理论上在今天的 Rust 中可以被接受，因为 `[,]` 不能成为合法表达式的一部分，因此分析总是无歧义的。然而，因为 `[` 可以开始尾随表达式，`[` 不是可以安全地排除在表达式之后出现的字符。若 `[,]` 在后续版本的 Rust 中被接受，此匹配器将变得有歧义或会错误分析，从而破坏正在工作的代码。然而，像 `$i:expr,` 或 `$i:expr;` 这样的匹配器是合法的，因为 `,` 和 `;` 是合法的表达式分隔符。具体规则为：

r[macro.decl.follow-set.token-expr-stmt]
  * `expr` 和 `stmt` 后面只能跟下列之一：`=>`、`,` 或 `;`。

r[macro.decl.follow-set.token-pat_param]
  * `pat_param` 后面只能跟下列之一：`=>`、`,`、`=`、`|`、`if` 或 `in`。

r[macro.decl.follow-set.token-pat]
  * `pat` 后面只能跟下列之一：`=>`、`,`、`=`、`if` 或 `in`。

r[macro.decl.follow-set.token-path-ty]
  * `path` 和 `ty` 后面只能跟下列之一：`=>`、`,`、`=`、`|`、`;`、`:`、`>`、`>>`、`[`、`{`、`as`、`where`，或 `block` 片段说明符的宏变量。

r[macro.decl.follow-set.token-vis]
  * `vis` 后面只能跟下列之一：`,`、非原始 `priv` 以外的标识符、任何可以开始类型的 token，或带有 `ident`、`ty` 或 `path` 片段说明符的元变量。

r[macro.decl.follow-set.token-other]
  * 所有其他片段说明符没有限制。

r[macro.decl.follow-set.edition2021]
> [!EDITION-2021]
> 在 2021 edition 之前，`pat` 后面也可以跟 `|`。

r[macro.decl.follow-set.repetition]
当涉及重复时，这些规则适用于每一种可能的展开次数，并考虑分隔符。这意味着：

  * 若重复包含分隔符，该分隔符必须能够跟在重复内容之后。
  * 若重复可以多次重复（`*` 或 `+`），则内容必须能够跟在其自身之后。
  * 重复的内容必须能够跟在前面的内容之后，而后面的内容必须能够跟在重复的内容之后。
  * 若重复可以匹配零次（`*` 或 `?`），则后面的内容必须能够跟在前面的内容之后。

更多细节见 [形式规范][formal specification]。

[Metavariables]: #元变量
[Repetitions]: #重复
[`macro_export`]: #the-macro_export-attribute
[`$crate`]: macro.decl.hygiene.crate
[`extern crate self`]: items.extern-crate.self
[`macro_use` prelude]: names/preludes.md#macro_use-prelude
[block labels]: expr.loop.block-labels
[delimiters]: tokens.md#delimiters
[formal specification]: macro-ambiguity.md
[loop labels]: expressions/loop-expr.md#loop-labels
[name resolution ambiguities]: names/name-resolution.md#r-names.resolution.expansion.imports.ambiguity
[token]: tokens.md
[use declaration re-export]: items/use-declarations.md#use-visibility
