+++
title = "第7章 属性"
date = 2026-08-18T08:45:00+08:00
weight = 33
type = "docs"
description = "属性 — The Rust Reference"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Reference](https://doc.rust-lang.org/reference/)

> 原文链接: [https://doc.rust-lang.org/reference/attributes.html](https://doc.rust-lang.org/reference/attributes.html)

r[attributes]
# 属性

r[attributes.syntax]
```grammar,attributes
InnerAttribute -> `#` `!` `[` Attr `]`

OuterAttribute -> `#` `[` Attr `]`

Attr ->
      SimplePath AttrInput?
    | `unsafe` `(` SimplePath AttrInput? `)`

AttrInput ->
      DelimTokenTree
    | `=` Expression
```

r[attributes.intro]
_属性_（attribute）是一种通用的自由形式元数据，其解释取决于名称、约定、语言以及编译器版本。属性的模型来自 [ECMA-335] 中的 Attributes，语法则来自 [ECMA-334]（C#）。

r[attributes.inner]
_内部属性_（inner attributes）作用于声明该属性的那个语法形式本身。

> [!EXAMPLE]
> ```rust
> // 应用于外层模块或 crate 的一般元数据。
> #![crate_type = "lib"]
>
> // 内部属性作用于整个函数。
> fn some_unused_variables() {
>   #![allow(unused_variables)]
>
>   let x = ();
>   let y = ();
>   let z = ();
> }
> ```

r[attributes.outer]
_外部属性_（outer attributes）作用于紧跟在该属性之后的语法形式。

> [!EXAMPLE]
> ```rust
> // 标记为单元测试的函数
> #[test]
> fn test_foo() {
>     /* ... */
> }
>
> // 条件编译的模块
> #[cfg(target_os = "linux")]
> mod bar {
>     /* ... */
> }
>
> // 用于抑制警告/错误的 lint 属性
> #[allow(non_camel_case_types)]
> type int8_t = i8;
> ```

r[attributes.input]
属性由指向该属性的路径组成，其后可跟一个可选的定界记号树，其解释由该属性定义。除宏属性外，属性还允许输入为等号（`=`）后跟一个表达式。更多细节见下文的[元项语法](#meta-item-attribute-syntax)。

r[attributes.safety]
某些属性的应用可能是不安全的。为避免使用这些属性时出现未定义行为，必须满足某些编译器无法检查的义务。为断言这些义务已满足，需将属性包在 `unsafe(..)` 中，例如 `#[unsafe(no_mangle)]`。

下列属性是不安全的：

* [`export_name`]
* [`link_section`]
* [`naked`]
* [`no_mangle`]

r[attributes.kind]
属性可分为以下种类：

* [内置属性][Built-in attributes]
* [过程宏属性][attribute macros]
* [Derive 宏辅助属性][Derive macro helper attributes]
* [工具属性](#tool-attributes)

r[attributes.allowed-position]
属性可应用于语言中的多种形式：

* 所有[项声明][item declarations]接受外部属性，而[外部块][external blocks]、[函数][functions]、[实现][implementations]和[模块][modules]接受内部属性。
* 大多数[语句][statements]接受外部属性（表达式语句的限制见[表达式属性][Expression Attributes]）。
* [块表达式][Block expressions]接受外部与内部属性，但仅当它们是[表达式语句][expression statement]的外层表达式，或是另一个块表达式的最终表达式时。
* [枚举][Enum]变体以及[结构体][struct]和[联合体][union]的字段接受外部属性。
* [`match` 表达式][match expressions]的分支接受外部属性。
* [泛型生命周期或类型参数][generics]接受外部属性。
* 表达式仅在有限情况下接受外部属性，细节见[表达式属性][Expression Attributes]。
* [函数][functions]、[闭包][closure]以及[函数指针][function pointer]的参数接受外部属性。这包括函数指针与[外部块][variadic functions]中以 `...` 表示的可变参数上的属性。
* [内联汇编][Inline assembly]的模板字符串与操作数接受外部属性。语义上仅接受某些属性；细节见 [asm.attributes.supported-attributes]。

r[attributes.meta]
## 元项属性语法

r[attributes.meta.intro]
“元项”（meta item）是大多数[内置属性][built-in attributes]用于 [Attr] 规则的语法。其文法如下：

r[attributes.meta.syntax]
```grammar,attributes
@root MetaItem ->
      SimplePath
    | SimplePath `=` Expression
    | SimplePath `(` MetaSeq? `)`

MetaSeq ->
    MetaItemInner ( `,` MetaItemInner )* `,`?

MetaItemInner ->
      MetaItem
    | Expression
```

r[attributes.meta.literal-expr]
元项中的表达式必须宏展开为字面量表达式，且不得包含整数或浮点类型后缀。非字面量表达式在语法上会被接受（并可传给过程宏），但在解析之后会被拒绝。

r[attributes.meta.order]
注意：若属性出现在另一个宏之内，它会在该外层宏之后展开。例如，下列代码会先展开 `Serialize` 过程宏，该宏必须保留 `include_str!` 调用以便其随后被展开：

```rust ignore
#[derive(Serialize)]
struct Foo {
    #[doc = include_str!("x.md")]
    x: u32
}
```

r[attributes.meta.order-macro]
此外，属性中的宏仅在应用于该项的所有其他属性之后才展开：

```rust ignore
#[macro_attr1] // 最先展开
#[doc = mac!()] // `mac!` 第四个展开。
#[macro_attr2] // 第二个展开
#[derive(MacroDerive1, MacroDerive2)] // 第三个展开
fn foo() {}
```

r[attributes.meta.builtin]
各种内置属性使用元项语法的不同子集来指定其输入。下列文法规则展示了一些常用形式：

r[attributes.meta.builtin.syntax]
```grammar,attributes
@root MetaWord ->
    IDENTIFIER

MetaNameValueStr ->
    IDENTIFIER `=` (STRING_LITERAL | RAW_STRING_LITERAL)

@root MetaListPaths ->
    IDENTIFIER `(` ( SimplePath (`,` SimplePath)* `,`? )? `)`

@root MetaListIdents ->
    IDENTIFIER `(` ( IDENTIFIER (`,` IDENTIFIER)* `,`? )? `)`

@root MetaListNameValueStr ->
    IDENTIFIER `(` ( MetaNameValueStr (`,` MetaNameValueStr)* `,`? )? `)`
```

元项的一些示例如下：

样式 | 示例
------|--------
[MetaWord] | `no_std`
[MetaNameValueStr] | `doc = "example"`
[MetaListPaths] | `allow(unused, clippy::inline_always)`
[MetaListIdents] | `macro_use(foo, bar)`
[MetaListNameValueStr] | `link(name = "CoreFoundation", kind = "framework")`

r[attributes.activity]
## 活跃属性与惰性属性

r[attributes.activity.intro]
属性要么是活跃的（active），要么是惰性的（inert）。在属性处理过程中，*活跃属性*会从其所附着的形式上移除自身，而*惰性属性*则保留在原处。

[`cfg`] 与 [`cfg_attr`] 属性是活跃的。[属性宏][Attribute macros]是活跃的。所有其他属性都是惰性的。

r[attributes.tool]
## 工具属性

r[attributes.tool.intro]
编译器可以允许供外部工具使用的属性，每个工具位于[工具 prelude][tool prelude] 中各自的模块内。属性路径的第一段是工具名称，其后可有一段或多段，其解释由该工具决定。

r[attributes.tool.ignored]
当某工具未在使用时，该工具的属性会被无警告地接受。当工具在使用时，由该工具负责处理与解释其属性。

r[attributes.tool.prelude]
若使用了 [`no_implicit_prelude`] 属性，则工具属性不可用。

```rust
// 告知 rustfmt 工具不要格式化其后的元素。
#[rustfmt::skip]
struct S {
}

// 控制 clippy 工具的“圈复杂度”阈值。
#[clippy::cyclomatic_complexity = "100"]
pub fn f() {}
```

> **注意**
> `rustc` 当前识别的工具有 "clippy"、"rustfmt"、"diagnostic"、"miri" 和 "rust_analyzer"。

r[attributes.builtin]
## 内置属性索引

以下是所有内置属性的索引。

- 条件编译
  - [`cfg`] —— 控制条件编译。
  - [`cfg_attr`] —— 有条件地包含属性。

- 测试
  - [`test`] —— 将函数标记为测试。
  - [`ignore`] —— 禁用测试函数。
  - [`should_panic`] —— 表示测试应产生 panic。

- Derive
  - [`derive`] —— 自动 trait 实现。
  - [`automatically_derived`] —— 由 `derive` 创建的实现的标记。

- 宏
  - [`macro_export`] —— 导出 `macro_rules` 宏以供跨 crate 使用。
  - [`macro_use`] —— 扩展宏可见性，或从其他 crate 导入宏。
  - [`proc_macro`] —— 定义类函数宏。
  - [`proc_macro_derive`] —— 定义 derive 宏。
  - [`proc_macro_attribute`] —— 定义属性宏。

- 诊断
  - [`allow`]、[`expect`]、[`warn`]、[`deny`]、[`forbid`] —— 改变默认 lint 级别。
  - [`deprecated`] —— 生成弃用通知。
  - [`must_use`] —— 对未使用的值生成 lint。
  - [`diagnostic::on_unimplemented`] —— 提示编译器在 trait 未实现时发出特定错误消息。
  - [`diagnostic::do_not_recommend`] —— 提示编译器不要在错误消息中显示某个 trait 实现。

- ABI、链接、符号与 FFI
  - [`link`] —— 指定与 `extern` 块链接的本地库。
  - [`link_name`] —— 指定 `extern` 块中函数或静态项的符号名。
  - [`link_ordinal`] —— 指定 `extern` 块中函数或静态项的符号序号。
  - [`no_link`] —— 阻止链接某个 extern crate。
  - [`repr`] —— 控制类型布局。
  - [`crate_type`] —— 指定 crate 类型（库、可执行文件等）。
  - [`no_main`] —— 禁用发出 `main` 符号。
  - [`export_name`] —— 指定函数或静态项的导出符号名。
  - [`link_section`] —— 指定函数或静态项所用的目标文件节区。
  - [`no_mangle`] —— 禁用符号名改写。
  - [`used`] —— 强制编译器在输出目标文件中保留某个静态项。
  - [`crate_name`] —— 指定 crate 名称。

- 代码生成
  - [`inline`] —— 提示内联代码。
  - [`cold`] —— 提示某函数不太可能被调用。
  - [`naked`] —— 阻止编译器发出函数序言与尾声。
  - [`no_builtins`] —— 禁用某些内置函数的使用。
  - [`target_feature`] —— 配置特定平台的代码生成。
  - [`track_caller`] —— 将父调用位置传给 `std::panic::Location::caller()`。
  - [`instruction_set`] —— 指定生成函数代码所用的指令集。

- 文档
  - `doc` —— 指定文档。更多信息见 [The Rustdoc Book]。[文档注释][Doc comments]会被转换为 `doc` 属性。

- Prelude
  - [`no_std`] —— 从 prelude 中移除 std。
  - [`no_implicit_prelude`] —— 禁用模块内的 prelude 查找。

- 模块
  - [`path`] —— 指定模块的文件名。

- 限制
  - [`recursion_limit`] —— 设置某些编译期操作的最大递归限制。
  - [`type_length_limit`] —— 设置多态类型的最大大小。

- 运行时
  - [`panic_handler`] —— 设置处理 panic 的函数。
  - [`global_allocator`] —— 设置全局内存分配器。
  - [`windows_subsystem`] —— 指定要链接的 Windows 子系统。

- 特性
  - `feature` —— 用于启用不稳定或实验性的编译器特性。`rustc` 中已实现的特性见 [The Unstable Book]。

- 类型系统
  - [`non_exhaustive`] —— 表示将来会向类型添加更多字段/变体。

- 调试器
  - [`debugger_visualizer`] —— 嵌入指定类型调试器输出的文件。
  - [`collapse_debuginfo`] —— 控制宏调用在调试信息中的编码方式。

[Doc comments]: comments.md#doc-comments
[ECMA-334]: https://www.ecma-international.org/publications-and-standards/standards/ecma-334/
[ECMA-335]: https://www.ecma-international.org/publications-and-standards/standards/ecma-335/
[Expression Attributes]: expressions.md#expression-attributes
[The Rustdoc Book]: ../rustdoc/the-doc-attribute.html
[The Unstable Book]: ../unstable-book/index.html
[`allow`]: attributes/diagnostics.md#lint-check-attributes
[`automatically_derived`]: attributes/derive.md#the-automatically_derived-attribute
[`cfg_attr`]: conditional-compilation.md#the-cfg_attr-attribute
[`cfg`]: conditional-compilation.md#the-cfg-attribute
[`cold`]: attributes/codegen.md#the-cold-attribute
[`collapse_debuginfo`]: attributes/debugger.md#the-collapse_debuginfo-attribute
[`crate_name`]: crates-and-source-files.md#the-crate_name-attribute
[`crate_type`]: linkage.md
[`debugger_visualizer`]: attributes/debugger.md#the-debugger_visualizer-attribute
[`deny`]: attributes/diagnostics.md#lint-check-attributes
[`deprecated`]: attributes/diagnostics.md#the-deprecated-attribute
[`derive`]: attributes/derive.md
[`export_name`]: abi.md#the-export_name-attribute
[`expect`]: attributes/diagnostics.md#lint-check-attributes
[`forbid`]: attributes/diagnostics.md#lint-check-attributes
[`global_allocator`]: runtime.md#the-global_allocator-attribute
[`ignore`]: attributes/testing.md#the-ignore-attribute
[`inline`]: attributes/codegen.md#the-inline-attribute
[`instruction_set`]: attributes/codegen.md#the-instruction_set-attribute
[`link_name`]: items/external-blocks.md#the-link_name-attribute
[`link_ordinal`]: items/external-blocks.md#the-link_ordinal-attribute
[`link_section`]: abi.md#the-link_section-attribute
[`link`]: items/external-blocks.md#the-link-attribute
[`macro_export`]: macros-by-example.md#the-macro_export-attribute
[`macro_use`]: macros-by-example.md#the-macro_use-attribute
[`must_use`]: attributes/diagnostics.md#the-must_use-attribute
[`naked`]: attributes/codegen.md#the-naked-attribute
[`no_builtins`]: attributes/codegen.md#the-no_builtins-attribute
[`no_implicit_prelude`]: names/preludes.md#the-no_implicit_prelude-attribute
[`no_link`]: items/extern-crates.md#the-no_link-attribute
[`no_main`]: crates-and-source-files.md#the-no_main-attribute
[`no_mangle`]: abi.md#the-no_mangle-attribute
[`no_std`]: names/preludes.md#the-no_std-attribute
[`non_exhaustive`]: attributes/type_system.md#the-non_exhaustive-attribute
[`panic_handler`]: panic.md#the-panic_handler-attribute
[`path`]: items/modules.md#the-path-attribute
[`proc_macro_attribute`]: procedural-macros.md#the-proc_macro_attribute-attribute
[`proc_macro_derive`]: macro.proc.derive
[`proc_macro`]: procedural-macros.md#the-proc_macro-attribute
[`recursion_limit`]: attributes/limits.md#the-recursion_limit-attribute
[`repr`]: type-layout.md#representations
[`should_panic`]: attributes/testing.md#the-should_panic-attribute
[`target_feature`]: attributes/codegen.md#the-target_feature-attribute
[`test`]: attributes/testing.md#the-test-attribute
[`track_caller`]: attributes/codegen.md#the-track_caller-attribute
[`type_length_limit`]: attributes/limits.md#the-type_length_limit-attribute
[`used`]: abi.md#the-used-attribute
[`warn`]: attributes/diagnostics.md#lint-check-attributes
[`windows_subsystem`]: runtime.md#the-windows_subsystem-attribute
[attribute macros]: procedural-macros.md#the-proc_macro_attribute-attribute
[block expressions]: expressions/block-expr.md
[built-in attributes]: #built-in-attributes-index
[derive macro helper attributes]: procedural-macros.md#derive-macro-helper-attributes
[enum]: items/enumerations.md
[expression statement]: statements.md#expression-statements
[external blocks]: items/external-blocks.md
[functions]: items/functions.md
[generics]: items/generics.md
[implementations]: items/implementations.md
[item declarations]: items.md
[match expressions]: expressions/match-expr.md
[modules]: items/modules.md
[statements]: statements.md
[struct]: items/structs.md
[tool prelude]: names/preludes.md#tool-prelude
[union]: items/unions.md
[closure]: expressions/closure-expr.md
[function pointer]: types/function-pointer.md
[variadic functions]: items/external-blocks.html#variadic-functions
[`diagnostic::on_unimplemented`]: attributes/diagnostics.md#the-diagnosticon_unimplemented-attribute
[`diagnostic::do_not_recommend`]: attributes/diagnostics.md#the-diagnosticdo_not_recommend-attribute
[Inline assembly]: inline-assembly.md
