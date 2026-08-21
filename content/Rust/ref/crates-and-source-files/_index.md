+++
title = "第4章 Crate 与源文件"
date = 2026-08-18T08:45:00+08:00
weight = 15
type = "docs"
description = "Crate 与源文件 — The Rust Reference"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Reference](https://doc.rust-lang.org/reference/)

> 原文链接: [https://doc.rust-lang.org/reference/crates-and-source-files.html](https://doc.rust-lang.org/reference/crates-and-source-files.html)

r[crate]
# Crate 与源文件

r[crate.syntax]
```grammar,items
@root Crate ->
    InnerAttribute*
    Item*
```

> **注意**
> 尽管 Rust 与任何其他语言一样，既可以由解释器也可以由编译器实现，但现有的唯一实现是编译器，并且该语言一直被设计为被编译。由于这些原因，本节假定使用编译器。

r[crate.compile-time]
Rust 的语义遵守编译期与运行时之间的 *阶段区分*。[^phase-distinction] 具有 *静态解释* 的语义规则决定编译的成功或失败，而具有 *动态解释* 的语义规则决定程序在运行时的行为。

r[crate.unit]
编译模型围绕称为 *crate* 的产物。每次编译处理源形式的单个 crate，若成功，则产生二进制形式的单个 crate：要么是可执行文件，要么是某种库。[^cratesourcefile]

r[crate.module]
*crate* 是编译与链接的单位，也是版本管理、分发和运行时加载的单位。crate 包含嵌套 [模块][module] 作用域的 *树*。此树的顶层是一个匿名模块（从该模块内路径的角度看），crate 内的任何项都有一条规范的 [模块路径][module path]，表示其在 crate 模块树中的位置。

r[crate.input-source]
Rust 编译器总是以单个源文件作为输入被调用，并总是产生单个输出 crate。对该源文件的处理可能导致其他源文件作为模块被加载。源文件具有扩展名 `.rs`。

r[crate.module-def]
Rust 源文件描述一个模块，其名称与位置——在当前 crate 的模块树中——从源文件外部定义：要么由引用源文件中的显式 [Module][grammar-Module] 项定义，要么由 crate 自身的名称定义。

r[crate.inline-module]
每个源文件都是一个模块，但并非每个模块都需要自己的源文件：[模块定义][module] 可以嵌套在同一个文件中。

r[crate.items]
每个源文件包含零个或多个 [Item] 定义的序列，并可以可选地以任意数量应用于所含模块的 [属性][attributes] 开头，其中大多数会影响编译器的行为。

r[crate.attributes]
匿名 crate 模块可以有应用于整个 crate 的额外属性。

> **注意**
> 文件内容前面可以有 [shebang]。

```rust
// 指定 crate 名称。
#![crate_name = "projx"]

// 指定输出产物的类型。
#![crate_type = "lib"]

// 打开一项警告。
// 这可以在任何模块中完成，而不仅是匿名 crate 模块。
#![warn(non_camel_case_types)]
```

r[crate.main]
## main 函数

r[crate.main.executable]
包含 `main` [函数][function] 的 crate 可以编译为可执行文件。

r[crate.main.restriction]
若存在 `main` 函数，它必须不接受参数，不得声明任何 [trait 或生命周期约束][trait or lifetime bounds]，不得有任何 [where 子句][where clauses]，并且其返回类型必须实现 [`Termination`] trait。

```rust
fn main() {}
```
```rust
fn main() -> ! {
    std::process::exit(0);
}
```
```rust
fn main() -> impl std::process::Termination {
    std::process::ExitCode::SUCCESS
}
```

r[crate.main.import]
`main` 函数可以是导入，例如来自外部 crate 或当前 crate。

```rust
mod foo {
    pub fn bar() {
        println!("Hello, world!");
    }
}
use foo::bar as main;
```

> **注意**
> 标准库中实现了 [`Termination`] 的类型包括：
>
> * `()`
> * [`!`]
> * [`Infallible`]
> * [`ExitCode`]
> * `Result<T, E> where T: Termination, E: Debug`

<!-- If the previous section needs updating (from "must take no arguments"
  onwards, also update it in the testing.md file -->

r[crate.uncaught-foreign-unwinding]
### 未捕获的外部展开

当“外部”展开（例如从 C++ 代码抛出的异常，或使用不同 panic 处理器的 Rust 代码中的 `panic!`）传播到 `main` 函数之外时，进程将被安全终止。这可能采取中止的形式，在这种情况下不保证会执行任何 `Drop` 调用，并且错误输出可能不如运行时被“原生” Rust `panic` 终止时那样翔实。

更多信息见 [panic 文档][panic-docs]。

r[crate.no_main]
### `no_main` 属性

*`no_main` [属性][attribute]* 可以在 crate 级应用，以禁止为可执行二进制文件发出 `main` 符号。当要链接到的某个其他目标已定义 `main` 时，这很有用。

r[crate.crate_name]
## `crate_name` 属性

r[crate.crate_name.general]
*`crate_name` [属性][attribute]* 可以在 crate 级应用，以 [MetaNameValueStr] 语法指定 crate 的名称。

```rust
#![crate_name = "mycrate"]
```

r[crate.crate_name.restriction]
crate 名称不得为空，且只能包含 [Unicode 字母数字][Unicode alphanumeric] 或 `_`（U+005F）字符。

[^phase-distinction]: 这种区分在解释器中也会存在。像语法分析、类型检查和 lint 这样的静态检查，无论程序何时执行，都应在程序执行之前发生。

[^cratesourcefile]: crate 在某种程度上类似于 ECMA-335 CLI 模型中的 *assembly*、SML/NJ Compilation Manager 中的 *library*、Owens 和 Flatt 模块系统中的 *unit*，或 Mesa 中的 *configuration*。

[Unicode alphanumeric]: char::is_alphanumeric
[`!`]: types/never.md
[`ExitCode`]: std::process::ExitCode
[`Infallible`]: std::convert::Infallible
[`Termination`]: std::process::Termination
[attribute]: attributes.md
[attributes]: attributes.md
[function]: items/functions.md
[module]: items/modules.md
[module path]: paths.md
[panic-docs]: panic.md#unwinding-across-ffi-boundaries
[shebang]: shebang.md
[trait or lifetime bounds]: trait-bounds.md
[where clauses]: items/generics.md#where-clauses
