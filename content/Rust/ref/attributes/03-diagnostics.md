+++
title = "03-诊断"
date = 2026-08-18T08:45:00+08:00
weight = 36
type = "docs"
description = "诊断 — The Rust Reference"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Reference](https://doc.rust-lang.org/reference/)

> 原文链接: [https://doc.rust-lang.org/reference/attributes/diagnostics.html](https://doc.rust-lang.org/reference/attributes/diagnostics.html)

r[attributes.diagnostics]
# 诊断

下列[属性][attributes]用于在编译期间控制或生成诊断消息。

r[attributes.diagnostics.lint]
## Lint 检查属性

Lint 检查会为可能不受欢迎的编码模式命名，例如不可达代码或缺失文档。

r[attributes.diagnostics.lint.level]
Lint 属性 `allow`、`expect`、`warn`、`deny` 和 `forbid` 使用 [MetaListPaths] 语法，指定一组 lint 名称，以更改该属性所应用实体的 lint 级别。

对于任意 lint 检查 `C`：

r[attributes.diagnostics.lint.allow]
* `#[allow(C)]` 会覆盖对 `C` 的检查，使违规不再被报告。

r[attributes.diagnostics.lint.expect]
* `#[expect(C)]` 表示预期会发出 lint `C`。该属性会抑制 `C` 的发出；若期望未兑现，则会发出警告。

r[attributes.diagnostics.lint.warn]
* `#[warn(C)]` 会对 `C` 的违规发出警告，但继续编译。

r[attributes.diagnostics.lint.deny]
* `#[deny(C)]` 在遇到 `C` 的违规后发出错误，

r[attributes.diagnostics.lint.forbid]
* `#[forbid(C)]` 与 `deny(C)` 相同，但还禁止之后再更改该 lint 级别，

> **注意**
> `rustc` 所支持的 lint 检查可通过 `rustc -W help` 查看（含默认设置），并在 [rustc book] 中有文档说明。

```rust
pub mod m1 {
    // 此处忽略缺失文档
    #[allow(missing_docs)]
    pub fn undocumented_one() -> i32 { 1 }

    // 此处缺失文档会发出警告
    #[warn(missing_docs)]
    pub fn undocumented_too() -> i32 { 2 }

    // 此处缺失文档会发出错误
    #[deny(missing_docs)]
    pub fn undocumented_end() -> i32 { 3 }
}
```

r[attributes.diagnostics.lint.override]
Lint 属性可以覆盖先前属性指定的级别，只要该级别不是试图更改已被 `forbid` 的 lint（`deny` 除外：它允许出现在 `forbid` 上下文中，但会被忽略）。先前属性是指语法树中更高层的属性，或同一实体上按从左到右源码顺序排列的前一个属性。

下面的例子展示了如何使用 `allow` 和 `warn` 来打开或关闭某项检查：

```rust
#[warn(missing_docs)]
pub mod m2 {
    #[allow(missing_docs)]
    pub mod nested {
        // 此处忽略缺失文档
        pub fn undocumented_one() -> i32 { 1 }

        // 尽管上面有 allow，此处缺失文档仍会发出警告。
        #[warn(missing_docs)]
        pub fn undocumented_two() -> i32 { 2 }
    }

    // 此处缺失文档会发出警告
    pub fn undocumented_too() -> i32 { 3 }
}
```

下面的例子展示了如何使用 `forbid` 来禁止对该 lint 检查使用 `allow` 或 `expect`：

```rust
#[forbid(missing_docs)]
pub mod m3 {
    // 试图切换警告级别会在此处发出错误
    #[allow(missing_docs)]
    /// 返回 2。
    pub fn undocumented_too() -> i32 { 2 }
}
```

> **注意**
> `rustc` 允许在[命令行][rustc-lint-cli]上设置 lint 级别，也支持为所报告的 lint [设置上限][rustc-lint-caps]。

r[attributes.diagnostics.lint.reason]
### Lint 原因

所有 lint 属性都支持额外的 `reason` 参数，用于说明添加该属性的原因。若 lint 以所定义的级别发出，该原因会作为 lint 消息的一部分显示。

```rust
// `keyword_idents` 默认是 allow。此处将其设为 deny，
// 以免在升级 edition 时迁移标识符。
#![deny(
    keyword_idents,
    reason = "we want to avoid these idents to be future compatible"
)]

// 该名称在 Rust 2015 edition 中是允许的。我们仍希望避免使用它，
// 以保持面向未来的兼容性，并避免让最终用户产生混淆。
fn dyn() {}
```

下面是另一个例子，其中以带原因的方式 allow 了该 lint：

```rust
use std::path::PathBuf;

pub fn get_path() -> PathBuf {
    // `allow` 属性上的 `reason` 参数可作为给读者的文档。
    #[allow(unused_mut, reason = "this is only modified on some platforms")]
    let mut file_name = PathBuf::from("git");

    #[cfg(target_os = "windows")]
    file_name.set_extension("exe");

    file_name
}
```

r[attributes.diagnostics.expect]
### `#[expect]` 属性

r[attributes.diagnostics.expect.intro]
`#[expect(C)]` 属性会为 lint `C` 创建一条 lint 期望。若在同一位置使用 `#[warn(C)]` 属性会导致发出该 lint，则该期望即被兑现。若期望未兑现（因为不会发出 lint `C`），则会在该属性处发出 `unfulfilled_lint_expectations` lint。

```rust
fn main() {
    // 该 `#[expect]` 属性创建了一条 lint 期望：随后的语句会发出 `unused_variables`
    // lint。由于 `question` 变量被 `println!` 宏使用，该期望未兑现。
    // 因此会在该属性处发出 `unfulfilled_lint_expectations` lint。
    #[expect(unused_variables)]
    let question = "who lives in a pineapple under the sea?";
    println!("{question}");

    // 该 `#[expect]` 属性创建的 lint 期望会被兑现，因为 `answer` 变量从未被使用。
    // 通常会发出的 `unused_variables` lint 被抑制。语句或属性都不会发出警告。
    #[expect(unused_variables)]
    let answer = "SpongeBob SquarePants!";
}
```

r[attributes.diagnostics.expect.fulfillment]
Lint 期望仅由被该 `expect` 属性抑制的 lint 发出所兑现。若在作用域内用其他级别属性（如 `allow` 或 `warn`）修改了 lint 级别，则 lint 会按相应级别处理，期望仍保持未兑现。

```rust
#[expect(unused_variables)]
fn select_song() {
    // 这将按 `warn` 属性所定义的 warn 级别发出 `unused_variables` lint。
    // 这不会兑现函数上方的期望。
    #[warn(unused_variables)]
    let song_name = "Crab Rave";

    // `allow` 属性会抑制该 lint 的发出。这不会兑现期望，因为它是被 `allow`
    // 属性抑制的，而不是被函数上方的 `expect` 属性抑制的。
    #[allow(unused_variables)]
    let song_creator = "Noisestorm";

    // 该 `expect` 属性会抑制该变量处的 `unused_variables` lint 发出。
    // 函数上方的 `expect` 属性仍不会被兑现，因为这次 lint 发出是被局部的
    // expect 属性抑制的。
    #[expect(unused_variables)]
    let song_version = "Monstercat Release";
}
```

r[attributes.diagnostics.expect.independent]
若 `expect` 属性包含多个 lint，则分别对每一个建立期望。对于 lint 组，组内只要有一个 lint 被发出即足够：

```rust
// 该期望会因函数内未使用的值而兑现，因为发出的 `unused_variables` lint 属于 `unused` lint 组。
#[expect(unused)]
pub fn thoughts() {
    let unused = "I'm running out of examples";
}

pub fn another_example() {
    // 该属性创建了两条 lint 期望。`unused_mut` lint 会被抑制，从而兑现第一条期望。
    // 由于变量被使用，不会发出 `unused_variables`。因此该期望未兑现，并会发出警告。
    #[expect(unused_mut, unused_variables)]
    let mut link = "https://www.rust-lang.org/";

    println!("Welcome to our community: {link}");
}
```

> **注意**
> `#[expect(unfulfilled_lint_expectations)]` 的行为当前定义为总会生成 `unfulfilled_lint_expectations` lint。

r[attributes.diagnostics.lint.group]
### Lint 组

Lint 可以组织到命名组中，以便一并调整相关 lint 的级别。使用命名组等价于列出该组内的所有 lint。

```rust
// 这会 allow “unused” 组中的所有 lint。
#[allow(unused)]
// 这会将 “unused” 组中的 “unused_must_use” lint 覆盖为 deny。
#[deny(unused_must_use)]
fn example() {
    // 这不会生成警告，因为 “unused_variables” lint 属于 “unused” 组。
    let x = 1;
    // 这会生成错误，因为结果未被使用，且 “unused_must_use” 被标记为 “deny”。
    std::fs::remove_file("some_file"); // ERROR: unused `Result` that must be used
}
```

r[attributes.diagnostics.lint.group.warnings]
有一个名为 “warnings” 的特殊组，包含所有处于 “warn” 级别的 lint。“warnings” 组会忽略属性顺序，并应用于该实体内原本会发出警告的所有 lint。

```rust
## unsafe fn an_unsafe_fn() {}
// 这两个属性的顺序无关紧要。
#[deny(warnings)]
// `unsafe_code` lint 默认通常为 “allow”。
#[warn(unsafe_code)]
fn example_err() {
    // 这是一个错误，因为 `unsafe_code` 警告已被提升为 “deny”。
    unsafe { an_unsafe_fn() } // ERROR: use of `unsafe` block
}
```

r[attributes.diagnostics.lint.tool]
### 工具 lint 属性

r[attributes.diagnostics.lint.tool.intro]
工具 lint 允许使用带作用域的 lint，以 `allow`、`warn`、`deny` 或 `forbid` 某些工具的 lint。

r[attributes.diagnostics.lint.tool.activation]
工具 lint 仅在关联工具处于活动状态时才会被检查。若某个 lint 属性（例如 `allow`）引用了不存在的工具 lint，编译器在使用该工具之前不会对不存在的 lint 发出警告。

除此之外，它们的工作方式与普通 lint 属性相同：

```rust
// 将整个 `pedantic` clippy lint 组设为 warn
#![warn(clippy::pedantic)]
// 抑制来自 `filter_map` clippy lint 的警告
#![allow(clippy::filter_map)]

fn main() {
    // ...
}

// 仅对此函数抑制 `cmp_nan` clippy lint
#[allow(clippy::cmp_nan)]
fn foo() {
    // ...
}
```

> **注意**
> `rustc` 当前识别 “[clippy]” 和 “[rustdoc]” 的工具 lint。

r[attributes.diagnostics.deprecated]
## `deprecated` 属性

r[attributes.diagnostics.deprecated.intro]
*`deprecated` 属性*将某项标记为已弃用。`rustc` 会在使用 `#[deprecated]` 项时发出警告。`rustdoc` 会显示项的弃用信息，包括 `since` 版本和 `note`（若有）。

r[attributes.diagnostics.deprecated.syntax]
`deprecated` 属性有多种形式：

- `deprecated` --- 发出通用消息。
- `deprecated = "message"` --- 在弃用消息中包含给定字符串。
- [MetaListNameValueStr] 语法，带有两个可选字段：
  - `since` --- 指定该项被弃用的版本号。`rustc` 当前不会解释该字符串，但 [Clippy] 等外部工具可能会检查其值的有效性。
  - `note` --- 指定应包含在弃用消息中的字符串。通常用于说明弃用原因及首选替代方案。

r[attributes.diagnostic.deprecated.allowed-positions]
`deprecated` 属性可应用于任何[项][item]、[trait 项][trait item]、[枚举变体][enum variant]、[结构体字段][struct field]、[外部块项][external block item]或[宏定义][macro definition]。它不能应用于 [trait 实现项][trait-impl]。当应用于包含其他项的项（例如[模块][module]或[实现][implementation]）时，所有子项都会继承该弃用属性。
<!-- NOTE: It is only rejected for trait impl items
(AnnotationKind::Prohibited). In all other locations, it is silently ignored.
Tuple struct fields are ignored.
-->

下面是一个例子：

```rust
#[deprecated(since = "5.2.0", note = "foo was rarely used. Users should instead use bar")]
pub fn foo() {}

pub fn bar() {}
```

该 [RFC][1270-deprecation.md] 包含动机及更多细节。

[1270-deprecation.md]: https://github.com/rust-lang/rfcs/blob/master/text/1270-deprecation.md

<!-- template:attributes -->
r[attributes.diagnostics.must_use]
## `must_use` 属性

r[attributes.diagnostics.must_use.intro]
*`must_use` [属性][attribute]*标记应当被使用的值。

r[attributes.diagnostics.must_use.syntax]
`must_use` 属性使用 [MetaWord] 和 [MetaNameValueStr] 语法。

> [!EXAMPLE]
> ```rust
> #[must_use]
> fn use_me1() -> u8 { 0 }
>
> #[must_use = "explanation of why it should be used"]
> fn use_me2() -> u8 { 0 }
> ```

r[attributes.diagnostics.must_use.allowed-positions]
`must_use` 属性可应用于：

- [结构体][Struct]
- [枚举][Enumeration]
- [联合体][Union]
- [函数][Function]
- [Trait][Trait]

> **注意**
> `rustc` 会忽略其他位置上的使用，但会对其发出 lint。将来这可能变成错误。

r[attributes.diagnostics.must_use.duplicates]
`must_use` 属性在一项上只能使用一次。

> **注意**
> `rustc` 会对第一次之后的使用发出 lint。将来这可能变成错误。

r[attributes.diagnostics.must_use.message]
`must_use` 属性可通过 [MetaNameValueStr] 语法包含一条消息，例如 `#[must_use = "example message"]`。该消息可能会作为 lint 的一部分发出。

r[attributes.diagnostics.must_use.type]
当该属性应用于[结构体][struct]、[枚举][enumeration]或[联合体][union]时，若[表达式语句][expression statement]的[表达式][expression]具有该类型，则此次使用会触发 `unused_must_use` lint。

```rust
#![deny(unused_must_use)]
#[must_use]
struct MustUse();
MustUse(); // ERROR: Unused value that must be used.
```

r[attributes.diagnostics.must_use.type.uninhabited]
作为 [attributes.diagnostics.must_use.type] 的例外，当 `E` 为 [uninhabited] 时，`Result<(), E>` 不会触发该 lint；当 `B` 为 [uninhabited] 时，`ControlFlow<B, ()>` 也不会。来自外部 crate 的 `#[non_exhaustive]` 类型在此意义上不视为 uninhabited，因为它将来可能增加构造函数。

```rust
#![deny(unused_must_use)]
## use core::ops::ControlFlow;
enum Empty {}
fn f1() -> Result<(), Empty> { Ok(()) }
f1(); // OK：`Empty` 是 uninhabited。
fn f2() -> ControlFlow<Empty, ()> { ControlFlow::Continue(()) }
f2(); // OK：`Empty` 是 uninhabited。
```

r[attributes.diagnostics.must_use.fn]
若[表达式语句][expression statement]的[表达式][expression]是[调用表达式][call expression]或[方法调用表达式][method call expression]，且其函数操作数是应用了该属性的函数，则此次使用会触发 `unused_must_use` lint。

```rust
#![deny(unused_must_use)]
#[must_use]
fn f() {}
f(); // ERROR: Unused return value that must be used.
```

r[attributes.diagnostics.must_use.trait]
若[表达式语句][expression statement]的[表达式][expression]是[调用表达式][call expression]或[方法调用表达式][method call expression]，且其函数操作数所返回的类型为 [impl trait] 或 [dyn trait]，并且约束中的一个或多个 trait 带有该属性，则此次使用会触发 `unused_must_use` lint。

```rust
#![deny(unused_must_use)]
#[must_use]
trait Tr {}
impl Tr for () {}
fn f() -> impl Tr {}
f(); // ERROR: Unused implementor that must be used.
```

r[attributes.diagnostics.must_use.trait-function]
当该属性应用于 trait 声明中的函数时，若[调用表达式][call expression]或[方法调用表达式][method call expression]的函数操作数是该函数的某个实现，则 [attributes.diagnostics.must_use.fn] 中描述的规则同样适用。

```rust
#![deny(unused_must_use)]
trait Tr {
    #[must_use]
    fn use_me(&self);
}

impl Tr for () {
    fn use_me(&self) {}
}

().use_me(); // ERROR: Unused return value that must be used.
```

```rust
## #![deny(unused_must_use)]
## trait Tr {
##     #[must_use]
##     fn use_me(&self);
## }
#
## impl Tr for () {
##     fn use_me(&self) {}
## }
#
<() as Tr>::use_me(&());
//          ^^^^^^^^^^^ ERROR: Unused return value that must be used.
```

r[attributes.diagnostics.must_use.block-expr]
在检查[表达式语句][expression statement]的[表达式][expression]是否符合 [attributes.diagnostics.must_use.type]、[attributes.diagnostics.must_use.fn]、[attributes.diagnostics.must_use.trait] 和 [attributes.diagnostics.must_use.trait-function] 时，该 lint 会穿透[块表达式][block expression]（包括 [`unsafe` 块][`unsafe` blocks] 和[带标签的块表达式][labeled block expressions]），检查各自的尾随表达式。这对嵌套的块表达式递归适用。

```rust
#![deny(unused_must_use)]
#[must_use]
fn f() {}

{ f() };        // ERROR：lint 会穿透块表达式。
unsafe { f() }; // ERROR：lint 会穿透 `unsafe` 块。
{ { f() } };    // ERROR：lint 会穿透嵌套块。
```

r[attributes.diagnostics.must_use.trait-impl-function]
当用于 trait 实现中的函数时，该属性没有任何效果。

```rust
#![deny(unused_must_use)]
trait Tr {
    fn f(&self);
}

impl Tr for () {
    #[must_use] // 这没有任何效果。
    fn f(&self) {}
}

().f(); // OK.
```

> **注意**
> `rustc` 会对 trait 实现中函数上的使用发出 lint。将来这可能变成错误。

r[attributes.diagnostics.must_use.wrapping-suppression]
> **注意**
> 将 `#[must_use]` 函数的结果包裹在某些表达式中，可能会抑制[基于函数的检查][attributes.diagnostics.must_use.fn]，因为[表达式语句][expression statement]的[表达式][expression]并不是对 `#[must_use]` 函数的[调用表达式][call expression]或[方法调用表达式][method call expression]。若整个表达式的类型带有 `#[must_use]`，则[基于类型的检查][attributes.diagnostics.must_use.type]仍然适用。
>
> ```rust
> #![deny(unused_must_use)]
> #[must_use]
> fn f() {}
>
> // 基于函数的检查对以下任何情况都不会触发，因为
> // 表达式语句的表达式并不是对 `#[must_use]` 函数的调用。
> (f(),);                    // 表达式是元组，不是调用。
> Some(f());                 // 被调用者 `Some` 不是 `#[must_use]`。
> if true { f() } else {};   // 表达式是 `if`，不是调用。
> match true {               // 表达式是 `match`，不是调用。
>     _ => f()
> };
> ```
>
> ```rust
> #![deny(unused_must_use)]
> #[must_use]
> struct MustUse;
> fn g() -> MustUse { MustUse }
>
> // 尽管 `if` 表达式不是调用，基于类型的检查仍会触发，
> // 因为该表达式的类型是 `MustUse`，而它带有 `#[must_use]` 属性。
> if true { g() } else { MustUse }; // ERROR: Must be used.
> ```

r[attributes.diagnostics.must_use.underscore-idiom]
> **注意**
> 当有意丢弃必须使用的值时，使用模式为 `_` 的 [let 语句][let statement]或[解构赋值][destructuring assignment]是惯用法。
>
> ```rust
> #![deny(unused_must_use)]
> #[must_use]
> fn f() {}
> let _ = f(); // OK.
> _ = f(); // OK.
> ```

r[attributes.diagnostic.namespace]
## `diagnostic` 工具属性命名空间

r[attributes.diagnostic.namespace.intro]
`#[diagnostic]` 属性命名空间用于存放影响编译期错误消息的属性。这些属性所提供的提示不保证会被使用。

r[attributes.diagnostic.namespace.unknown-invalid-syntax]
该命名空间中未知的属性会被接受，不过可能会对未使用的属性发出警告。此外，已知属性的无效输入通常会是警告（详见各属性的定义）。这是为了允许将来添加或丢弃属性、以及更改输入，从而无需让无意义的属性或选项继续保持有效。

r[attributes.diagnostic.on_unimplemented]
### `diagnostic::on_unimplemented` 属性

r[attributes.diagnostic.on_unimplemented.intro]
`#[diagnostic::on_unimplemented]` 属性是给编译器的提示，用于在要求某个 trait 但某类型未实现该 trait 时，补充原本会生成的错误消息。

r[attributes.diagnostic.on_unimplemented.allowed-positions]
该属性应放在 [trait 声明][trait declaration]上，不过放在其他位置也不算错误。

r[attributes.diagnostic.on_unimplemented.syntax]
该属性使用 [MetaListNameValueStr] 语法指定其输入；为同时提供向前和向后兼容性，对该属性的任何格式错误的输入都不视为错误。

r[attributes.diagnostic.on_unimplemented.keys]
下列键具有给定含义：
* `message` --- 顶层错误消息的文本。
* `label` --- 错误消息中在出错代码处内联显示的标签文本。
* `note` --- 提供附加说明。

r[attributes.diagnostic.on_unimplemented.note-repetition]
`note` 选项可以出现多次，从而发出多条 note 消息。

r[attributes.diagnostic.on_unimplemented.repetition]
若其他任一选项出现多次，则以该选项第一次出现的值作为实际使用的值。后续出现会生成警告。

r[attributes.diagnostic.on_unimplemented.unknown-keys]
对任何未知的键都会生成警告。

r[attributes.diagnostic.on_unimplemented.format-string]
这三个选项都接受字符串作为参数，并使用与 [`std::fmt`] 字符串相同的格式化规则进行解释。

r[attributes.diagnostic.on_unimplemented.format-parameters]
带有给定命名参数的格式参数会被替换为以下文本：
* `{Self}` --- 实现该 trait 的类型名称。
* `{` *GenericParameterName* `}` --- 给定泛型参数所对应的泛型实参类型名称。

r[attributes.diagnostic.on_unimplemented.invalid-formats]
任何其他格式参数都会生成警告，但除此之外会按原样包含在字符串中。

r[attributes.diagnostic.on_unimplemented.invalid-string]
无效的格式字符串可能会生成警告，但除此之外是允许的，只是可能不会按预期显示。格式说明符可能会生成警告，但除此之外会被忽略。

在本例中：

```rust
#[diagnostic::on_unimplemented(
    message = "My Message for `ImportantTrait<{A}>` implemented for `{Self}`",
    label = "My Label",
    note = "Note 1",
    note = "Note 2"
)]
trait ImportantTrait<A> {}

fn use_my_trait(_: impl ImportantTrait<i32>) {}

fn main() {
    use_my_trait(String::new());
}
```

编译器可能会生成如下所示的错误消息：

```text
error[E0277]: My Message for `ImportantTrait<i32>` implemented for `String`
  --> src/main.rs:14:18
   |
14 |     use_my_trait(String::new());
   |     ------------ ^^^^^^^^^^^^^ My Label
   |     |
   |     required by a bound introduced by this call
   |
   = help: the trait `ImportantTrait<i32>` is not implemented for `String`
   = note: Note 1
   = note: Note 2
```

r[attributes.diagnostic.do_not_recommend]
### `diagnostic::do_not_recommend` 属性

r[attributes.diagnostic.do_not_recommend.intro]
`#[diagnostic::do_not_recommend]` 属性是给编译器的提示，表示不要在诊断消息中展示被标注的 trait 实现。

> **注意**
> 若你知道该推荐通常对程序员没有帮助，抑制推荐会很有用。这常见于宽泛的 blanket impl。推荐可能把程序员引向错误方向，或者该 trait 实现可能是你不想暴露的内部细节，又或者其中的约束程序员无法满足。
>
> 例如，在关于某类型未实现所需 trait 的错误消息中，编译器可能会找到一个 trait 实现：若不是该实现中的特定约束，它本可以满足要求。编译器可能会告诉用户存在这样一个 impl，但问题出在该 trait 实现的约束上。可以使用 `#[diagnostic::do_not_recommend]` 属性告知编译器*不要*向用户提及该 trait 实现，而只是简单地告诉用户该类型未实现所需 trait。

r[attributes.diagnostic.do_not_recommend.allowed-positions]
该属性应放在 [trait 实现项][trait-impl]上，不过放在其他位置也不算错误。

r[attributes.diagnostic.do_not_recommend.syntax]
该属性不接受任何参数，不过意外的参数不视为错误。

在下面的例子中，有一个名为 `AsExpression` 的 trait，用于将任意类型转换为 SQL 库中使用的 `Expression` 类型。另有一个名为 `check` 的方法，它接受 `AsExpression`。

```rust
## pub trait Expression {
##     type SqlType;
## }
#
## pub trait AsExpression<ST> {
##     type Expression: Expression<SqlType = ST>;
## }
#
## pub struct Text;
## pub struct Integer;
#
## pub struct Bound<T>(T);
## pub struct SelectInt;
#
## impl Expression for SelectInt {
##     type SqlType = Integer;
## }
#
## impl<T> Expression for Bound<T> {
##     type SqlType = T;
## }
#
## impl AsExpression<Integer> for i32 {
##     type Expression = Bound<Integer>;
## }
#
## impl AsExpression<Text> for &'_ str {
##     type Expression = Bound<Text>;
## }
#
## impl<T> Foo for T where T: Expression {}

// 取消注释此行以更改推荐。
// #[diagnostic::do_not_recommend]
impl<T, ST> AsExpression<ST> for T
where
    T: Expression<SqlType = ST>,
{
    type Expression = T;
}

trait Foo: Expression + Sized {
    fn check<T>(&self, _: T) -> <T as AsExpression<<Self as Expression>::SqlType>>::Expression
    where
        T: AsExpression<Self::SqlType>,
    {
        todo!()
    }
}

fn main() {
    SelectInt.check("bar");
}
```

`SelectInt` 类型的 `check` 方法期望 `Integer` 类型。用 i32 类型调用可以工作，因为它会通过 `AsExpression` trait 转换为 `Integer`。然而，用字符串调用则不行，并可能生成如下所示的错误：

```text
error[E0277]: the trait bound `&str: Expression` is not satisfied
  --> src/main.rs:53:15
   |
53 |     SelectInt.check("bar");
   |               ^^^^^ the trait `Expression` is not implemented for `&str`
   |
   = help: the following other types implement trait `Expression`:
             Bound<T>
             SelectInt
note: required for `&str` to implement `AsExpression<Integer>`
  --> src/main.rs:45:13
   |
45 | impl<T, ST> AsExpression<ST> for T
   |             ^^^^^^^^^^^^^^^^     ^
46 | where
47 |     T: Expression<SqlType = ST>,
   |        ------------------------ unsatisfied trait bound introduced here
```

通过向 `AsExpression` 的 blanket `impl` 添加 `#[diagnostic::do_not_recommend]` 属性，消息会变为：

```text
error[E0277]: the trait bound `&str: AsExpression<Integer>` is not satisfied
  --> src/main.rs:53:15
   |
53 |     SelectInt.check("bar");
   |               ^^^^^ the trait `AsExpression<Integer>` is not implemented for `&str`
   |
   = help: the trait `AsExpression<Integer>` is not implemented for `&str`
           but trait `AsExpression<Text>` is implemented for it
   = help: for that trait implementation, expected `Text`, found `Integer`
```

第一条错误消息包含关于 `&str` 与 `Expression` 关系的、略显令人困惑的说明，以及 blanket impl 中未满足的 trait 约束。添加 `#[diagnostic::do_not_recommend]` 后，它不再将该 blanket impl 纳入推荐。消息应当更清晰一些，并指出字符串无法转换为 `Integer`。

[Clippy]: https://github.com/rust-lang/rust-clippy
[`Drop`]: ../special-types-and-traits.md#drop
[`unsafe` blocks]: ../expressions/block-expr.md#unsafe-blocks
[attribute]: ../attributes.md
[attributes]: ../attributes.md
[block expression]: ../expressions/block-expr.md
[call expression]: ../expressions/call-expr.md
[destructuring assignment]: expr.assign.destructure
[method call expression]: ../expressions/method-call-expr.md
[dyn trait]: ../types/trait-object.md
[enum variant]: ../items/enumerations.md
[enumeration]: ../items/enumerations.md
[expression statement]: ../statements.md#expression-statements
[expression]: ../expressions.md
[external block item]: ../items/external-blocks.md
[functions]: ../items/functions.md
[impl trait]: ../types/impl-trait.md
[implementation]: ../items/implementations.md
[item]: ../items.md
[labeled block expressions]: ../expressions/block-expr.md#labeled-block-expressions
[let statement]: ../statements.md#let-statements
[macro definition]: ../macros-by-example.md
[module]: ../items/modules.md
[rustc book]: ../../rustc/lints/index.html
[rustc-lint-caps]: ../../rustc/lints/levels.html#capping-lints
[rustc-lint-cli]: ../../rustc/lints/levels.html#via-compiler-flag
[rustdoc]: ../../rustdoc/lints.html
[struct field]: ../items/structs.md
[struct]: ../items/structs.md
[external block]: ../items/external-blocks.md
[trait declaration]: ../items/traits.md
[trait item]: ../items/traits.md
[trait-impl]: ../items/implementations.md#trait-implementations
[traits]: ../items/traits.md
[uninhabited]: glossary.uninhabited
[union]: ../items/unions.md
