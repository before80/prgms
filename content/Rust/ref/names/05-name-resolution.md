+++
title = "05-名称解析"
date = 2026-08-18T08:45:00+08:00
weight = 100
type = "docs"
description = "名称解析 — The Rust Reference"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Reference](https://doc.rust-lang.org/reference/)

> 原文链接: [https://doc.rust-lang.org/reference/names/name-resolution.html](https://doc.rust-lang.org/reference/names/name-resolution.html)

r[names.resolution]
# 名称解析

r[names.resolution.intro]
_名称解析_（name resolution）是将路径及其他标识符与实体声明绑定的过程。名称按不同的[命名空间][namespaces]划分，使得不同命名空间中的实体可以共用同一名称而不冲突。每个名称在一个[作用域][scope]内有效——即源码中允许引用该名称的区域。对名称的访问还可能受其[可见性][visibility]限制。

名称解析在整个编译过程中分为三个阶段。第一阶段是*展开期解析*（expansion-time resolution），解析所有[`use` 声明][`use` declarations]和[宏调用][macro invocations]。第二阶段是*主解析*（primary resolution），解析尚未解析且不依赖类型信息即可解析的所有名称。最后阶段是*相对类型的解析*（type-relative resolution），在类型信息可用后解析剩余名称。

> **注意**
> 展开期解析也称为*早期解析*（early resolution）。主解析也称为*晚期解析*（late resolution）。

r[names.resolution.general]
## 通则

r[names.resolution.general.intro]
本节中的规则适用于名称解析的所有阶段。

r[names.resolution.general.scopes]
### 作用域

r[names.resolution.general.scopes.intro]
> **注意**
> 此处为占位内容，供日后补充关于在各类作用域中解析名称的说明。

r[names.resolution.expansion]
## 展开期名称解析

r[names.resolution.expansion.intro]
展开期名称解析是完成宏展开、并完整生成 crate 的 [AST] 所必需的名称解析阶段。该阶段需要解析宏调用和 `use` 声明。解析 `use` 声明对于通过[基于路径的作用域][path-based scope]解析的宏调用是必需的。解析宏调用则是为了将其展开。

r[names.resolution.expansion.unresolved-invocations]
展开期名称解析之后，AST 中不得再包含任何未展开的宏调用。每个宏调用都必须解析到最终 AST 中或外部 crate 中存在的有效定义。

```rust
m!(); // 错误：在此作用域中找不到宏 `m`。
```

r[names.resolution.expansion.expansion-order-stability]
名称的解析必须是稳定的。展开之后，无论宏的展开顺序以及导入的解析顺序如何，完全展开后的 AST 中的名称都必须解析到同一份定义。

r[names.resolution.expansion.speculation]
宏展开期间选出的所有名称解析候选都被视为推测性的。一旦 crate 已完全展开，所有推测性的导入解析都会被验证，以确保宏展开没有引入任何新的歧义。

> **注意**
> 由于宏展开的迭代性质，这会导致所谓的时间旅行歧义（time traveling ambiguities），例如当某个宏或 glob 导入引入一项与其自身基路径产生歧义的项时。
>
> ```rust
> # fn main() {}
> macro_rules! f {
>     () => {
>         mod m {
>             pub(crate) use f;
>         }
>     }
> }
> f!();
>
> const _: () = {
>     // 最初，我们推测性地将 `m` 解析为
>     // crate 根中的模块。
>     //
>     // `f` 的展开在此函数体内部引入了
>     // 第二个 `m` 模块。
>     //
>     // 展开期解析通过重新解析所有导入和宏调用
>     // 来最终确定解析结果，发现引入的歧义，
>     // 并将其报告为错误。
>     m::f!(); // 错误：`m` 有歧义。
> };
> ```

r[names.resolution.expansion.imports]
### 导入
r[names.resolution.expansion.imports.intro]
所有 `use` 声明都在此解析阶段被完全解析。[相对类型的路径][type-relative paths]无法在此阶段解析，会产生错误。

```rust
mod m {
    pub const C: () = ();
    pub enum E { V }
    pub type A = E;
    impl E {
        pub const C: () = ();
    }
}

// 在展开期解析的有效导入：
use m::C; // 可行。
use m::E; // 可行。
use m::A; // 可行。
use m::E::V; // 可行。

// 在相对类型的解析期间解析的有效表达式：
let _ = m::A::V; // 可行。
let _ = m::E::C; // 可行。
```

```rust
## mod m {
##     pub const C: () = ();
##     pub enum E { V }
##     pub type A = E;
##     impl E {
##         pub const C: () = ();
##     }
## }
// 无法在展开期解析的无效相对类型导入：
use m::A::V; // 错误：未解析的导入 `m::A::V`。
use m::E::C; // 错误：未解析的导入 `m::E::C`。
```

r[names.resolution.expansion.imports.shadowing]
通过 `use` 声明在[外层作用域][outer scope]中引入的名称，会被内层作用域中同一命名空间下同名的候选所遮蔽，除非另受[名称解析歧义][name resolution ambiguities]限制。

```rust
pub mod m1 {
    pub mod ambig {
        pub const C: u8 = 1;
    }
}

pub mod m2 {
    pub mod ambig {
        pub const C: u8 = 2;
    }
}

// 这在外层作用域中引入名称 `ambig`。
use m1::ambig;
const _: () = {
    // 这在内层作用域中遮蔽了 `ambig`。
    use m2::ambig;
    // 此处选择内层候选作为
    // `ambig` 的解析结果。
    use ambig::C;
    assert!(C == 2);
};
```

r[names.resolution.expansion.imports.shadowing.shared-scope]
在同一作用域内，通过 `use` 声明引入的名称的遮蔽在下列情况下是允许的：

- [`use` glob 遮蔽][`use` glob shadowing]
- [宏文本作用域遮蔽][Macro textual scope shadowing]

r[names.resolution.expansion.imports.ambiguity]
#### 歧义

r[names.resolution.expansion.imports.ambiguity.intro]
在展开期解析过程中，存在某些情况：导入或宏调用的名称可能指向多个宏定义、`use` 声明或模块，而编译器无法一致地判定哪个候选应遮蔽另一个。这些情况下不允许遮蔽，编译器改为发出歧义错误。

r[names.resolution.expansion.imports.ambiguity.glob-vs-glob]
名称不得通过有歧义的 glob 导入来解析。只要该名称未被使用，glob 导入允许在同一命名空间中导入冲突的名称。来自有歧义 glob 导入的冲突候选名称仍可被非 glob 导入遮蔽，并在使用时不产生错误。错误发生在使用时，而非导入时。

```rust
mod m1 {
    pub struct Ambig;
}

mod m2 {
    pub struct Ambig;
}

// 可行：这将同一命名空间中冲突的名称带入作用域，
// 但它们尚未被使用。
use m1::*;
use m2::*;

const _: () = {
    // 当使用具有冲突候选的名称时，
    // 错误才会发生。
    let x = Ambig; // 错误：`Ambig` 有歧义。
};
```

```rust
## mod m1 {
##     pub struct Ambig;
## }
#
## mod m2 {
##     pub struct Ambig;
## }
#
## use m1::*;
## use m2::*; // 可行：无名称冲突。
const _: () = {
    // 这是允许的，因为解析并非通过
    // 有歧义的 glob 进行。
    struct Ambig;
    let x = Ambig; // 可行。
};
```

允许多个 glob 导入导入同一名称，且若这些导入指向同一项（遵循再导出），则允许使用该名称。该名称的可见性是这些导入中可见性的最大值。

```rust
mod m1 {
    pub struct Ambig;
}

mod m2 {
    // 这从第二个模块再导出同一 `Ambig` 项。
    pub use super::m1::Ambig;
}

mod m3 {
    // 这两者都导入同一 `Ambig`。
    //
    // `Ambig` 的可见性是 `pub`，因为那是
    // 这两个 `use` 声明之间可见性的最大值。
    pub use super::m1::*;
    use super::m2::*;
}

mod m4 {
    // 可通过 `m3` 的 glob 使用 `Ambig`，
    // 且仍具有 `pub` 可见性。
    pub use crate::m3::Ambig;
}

const _: () = {
    // 因此，我们可以在此处使用它。
    let _ = m4::Ambig; // 可行。
};
## fn main() {}
```

r[names.resolution.expansion.imports.ambiguity.glob-vs-outer]
当[外层作用域][outer scope]中另有可用候选时，导入和宏调用中的名称不得通过 glob 导入来解析。

r[names.resolution.expansion.imports.ambiguity.panic-hack]
> **注意**
> 当因[标准库 prelude][standard library prelude]而将 [`core::panic!`] 或 [`std::panic!`] 之一带入作用域，且用户编写的 [glob 导入][glob import] 将另一个也带入作用域时，`rustc` 当前允许使用 `panic!`，即使它是有歧义的。为消解此歧义，用户编写的 glob 导入优先。
>
> 在 Rust 2021 及之后的版本中，[`core::panic!`] 与 [`std::panic!`] 行为相同。但在更早的 edition 中二者不同；只有 [`std::panic!`] 接受 [`String`] 作为格式参数。
>
> 例如，这是错误：
>
> ```rust
> extern crate core;
> use ::core::prelude::v1::*;
> fn main() {
>     panic!(std::string::String::new()); // 错误。
> }
> ```
>
> 而这是被接受的：
>
> <!-- ignore: Can't test with `no_std`. -->
> ```rust
> #![no_std]
> extern crate std;
> use ::std::prelude::v1::*;
> fn main() {
>     panic!(std::string::String::new()); // 可行。
> }
> ```
>
> 不要依赖此行为；计划将其移除。
>
> 详情见 [Rust issue #147319](https://github.com/rust-lang/rust/issues/147319)。

```rust
mod glob {
    pub mod ambig {
        pub struct Name;
    }
}

// 外层 `ambig` 候选。
pub mod ambig {
    pub struct Name;
}

const _: () = {
    // 由于上方存在外层 `ambig` 候选，
    // 不能通过此 glob 解析 `ambig`。
    use glob::*;
    use ambig::Name; // 错误：`ambig` 有歧义。
};
```

```rust
// 同上，但是用宏。
pub mod m {
    macro_rules! f {
        () => {};
    }
    pub(crate) use f;
}
pub mod glob {
    macro_rules! f {
        () => {};
    }
    pub(crate) use f as ambig;
}

use m::f as ambig;

const _: () = {
    use glob::*;
    ambig!(); // 错误：`ambig` 有歧义。
};
```

> **注意**
> 这些歧义错误是展开期解析所特有的。在后续解析阶段，某个名称有多个可用候选并不视为错误。只要各个导入本身没有歧义，就总会有唯一且无歧义的最近解析结果。
>
> ```rust
> mod glob {
>     pub const AMBIG: u8 = 1;
> }
>
> mod outer {
>     pub const AMBIG: u8 = 2;
> }
>
> use outer::AMBIG;
>
> const C: () = {
>     use glob::*;
>     assert!(AMBIG == 1);
>     //      ^---- 此 `AMBIG` 在主解析期间被解析。
> };
> ```

r[names.resolution.expansion.imports.ambiguity.path-vs-textual-macro]
名称不得通过有歧义的宏再导出来解析。当宏再导出会遮蔽[外层作用域][outer scope]中同名的文本宏候选时，该再导出是有歧义的。

```rust
// 文本宏候选。
macro_rules! ambig {
    () => {}
}

// 基于路径的宏候选。
macro_rules! path_based {
    () => {}
}

pub fn f() {
    // 将 `path_based` 宏定义再导出为 `ambig`
    // 不得遮蔽通过文本宏作用域解析的
    // `ambig` 宏定义。
    use path_based as ambig;
    ambig!(); // 错误：`ambig` 有歧义。
}
```

> **注意**
> 此限制是由于编译器的实现细节所需，具体而言是当前的作用域遍历逻辑以及支持该行为的复杂性。此歧义错误未来可能会被移除。

r[names.resolution.expansion.macros]
### 宏

r[names.resolution.expansion.macros.intro]
宏通过遍历可用作用域以查找可用候选来解析。宏分为两个子命名空间：一个用于函数式宏，另一个用于属性和 derive。来自错误子命名空间的解析候选会被忽略。

r[names.resolution.expansion.macros.visitation-order]
可用的作用域种类按下列顺序访问。每一种作用域种类代表一个或多个作用域。

* [Derive 助手][Derive helpers]
* [文本作用域宏][Textual scope macros]
* [基于路径的作用域宏][Path-based scope macros]
* [`macro_use` prelude]
* [标准库 prelude][Standard library prelude]
* [内置属性][Builtin attributes]

> **注意**
> 编译器会尝试解析在其关联宏将其引入作用域之前就使用的 derive 助手。此作用域在用于解析已正确位于作用域中的 derive 助手候选的作用域之后访问。此行为计划移除。
>
> 更多信息见 [derive 助手作用域][derive helper scope]。

> **注意**
> 此访问顺序未来可能会改变，例如根据词法作用域交错访问文本作用域与基于路径的作用域候选。

> [!EDITION-2018]
> 从 2018 edition 起，当存在 [`#[no_implicit_prelude]`][names.preludes.no_implicit_prelude] 时，不再访问 `#[macro_use]` prelude。

r[names.resolution.expansion.macros.reserved-names]
名称 `cfg` 和 `cfg_attr` 在宏属性[子命名空间][sub-namespace]中是保留的。

r[names.resolution.expansion.macros.ambiguity]
#### 歧义

r[names.resolution.expansion.macros.ambiguity.more-expanded-vs-outer]
名称不得通过宏展开内部的有歧义候选来解析。当宏展开内部的候选会遮蔽该第一候选宏展开之外的同名候选，且正在解析的名称调用也来自该第一候选宏展开之外时，这些候选是有歧义的。

```rust
macro_rules! define_ambig {
    () => {
        macro_rules! ambig {
            () => {}
        }
    }
}

// 为 `ambig` 宏调用引入外层候选定义。
macro_rules! ambig {
    () => {}
}

// 在宏展开内部为 `ambig` 引入第二个候选定义。
define_ambig!();

// 来自第二次 `define_ambig` 调用的
// `ambig` 定义是最内层候选。
//
// 来自第一次 `define_ambig` 调用的
// `ambig` 定义是第二候选。
//
// 编译器检查第一候选是否位于宏展开内部、
// 第二候选是否不来自同一宏展开，以及
// 正在解析的名称是否不来自同一宏展开。
ambig!(); // 错误：`ambig` 有歧义。
```

反过来的情况不视为有歧义。

```rust
## macro_rules! define_ambig {
##     () => {
##         macro_rules! ambig {
##             () => {}
##         }
##     }
## }
// 交换定义顺序。
define_ambig!();
macro_rules! ambig {
    () => {}
}
// 现在最内层候选展开程度更低，因此可以遮蔽
// 其上由宏展开得到的定义。
ambig!();
```

若正在解析的调用位于最内层候选的展开内部，也不视为有歧义。

```rust
macro_rules! ambig {
    () => {}
}

macro_rules! define_and_invoke_ambig {
    () => {
        // 定义最内层候选。
        macro_rules! ambig {
            () => {}
        }

        // `ambig` 的调用与最内层候选
        // 处于同一展开中。
        ambig!(); // 可行
    }
}

define_and_invoke_ambig!();
```

两个定义是否来自同一宏的调用无关紧要；最外层候选仍被视为“展开程度更低”，因为它不位于包含最内层候选定义的那次展开之内。

```rust
## macro_rules! define_ambig {
##     () => {
##         macro_rules! ambig {
##             () => {}
##         }
##     }
## }
define_ambig!();
define_ambig!();
ambig!(); // 错误：`ambig` 有歧义。
```

只要该名称的最内层候选来自宏展开内部，这也适用于导入。

```rust
macro_rules! define_ambig {
    () => {
        mod ambig {
            pub struct Name;
        }
    }
}

mod ambig {
    pub struct Name;
}

const _: () = {
    // 在此宏展开中为 `ambig` 模块
    // 引入最内层候选。
    define_ambig!();
    use ambig::Name; // 错误：`ambig` 有歧义。
};
```

r[names.resolution.expansion.macros.ambiguity.built-in-attr]
用户定义的属性或 derive 宏不得遮蔽内置的非宏属性（例如 inline）。

<!-- ignore: test doesn't support proc-macro -->
```rust
// with-helper/src/lib.rs
## use proc_macro::TokenStream;
#[proc_macro_derive(WithHelperAttr, attributes(non_exhaustive))]
//                                             ^^^^^^^^^^^^^^
//                                   用户定义的属性候选。
// ...
## pub fn derive_with_helper_attr(_item: TokenStream) -> TokenStream {
##     TokenStream::new()
## }
```

<!-- ignore: requires external crates -->
```rust
// src/lib.rs
#[derive(with_helper::WithHelperAttr)]
#[non_exhaustive] // 错误：`non_exhaustive` 有歧义。
struct S;
```

> **注意**
> 无论内置属性作为哪个名称的候选，这都适用：
>
> <!-- ignore: test doesn't support proc-macro -->
> ```rust
> // with-helper/src/lib.rs
> # use proc_macro::TokenStream;
> #
> #[proc_macro_derive(WithHelperAttr, attributes(helper))]
> //                                             ^^^^^^
> //                                 用户定义的属性候选。
> // ...
> # pub fn derive_with_helper_attr(_item: TokenStream) -> TokenStream {
> #     TokenStream::new()
> # }
> ```
>
> <!-- ignore: requires external crates -->
> ```rust
> // src/lib.rs
> use inline as helper;
> //            ^----- 通过再导出得到的内置属性候选。
>
> #[derive(with_helper::WithHelperAttr)]
> #[helper] // 错误：`helper` 有歧义。
> struct S;
> ```

r[names.resolution.primary]
## 主名称解析
> **注意**
> 此处为占位内容，供日后补充关于主名称解析的说明。

r[names.resolution.type-relative]
## 相对类型的解析
> **注意**
> 此处为占位内容，供日后补充关于依赖类型的解析的说明。

[AST]: glossary.ast
[Builtin attributes]: ./preludes.md#r-names.preludes.lang
[Derive helpers]: ../procedural-macros.md#r-macro.proc.derive.attributes
[Macros]: ../macros.md
[Path-based scope macros]: ../macros.md#r-macro.invocation.name-resolution
[Standard library prelude]: ./preludes.md#r-names.preludes.std
[Textual scope macros]: ../macros-by-example.md#r-macro.decl.scope.textual
[`let` bindings]: ../statements.md#let-statements
[`macro_use` prelude]: ./preludes.md#r-names.preludes.macro_use
[`use` declarations]: ../items/use-declarations.md
[`use` glob shadowing]: ../items/use-declarations.md#r-items.use.glob.shadowing
[derive helper scope]: ../procedural-macros.md#r-macro.proc.derive.attributes.scope
[glob import]: items.use.glob
[item definitions]: ../items.md
[macro invocations]: ../macros.md#macro-invocation
[macro textual scope shadowing]: ../macros-by-example.md#r-macro.decl.scope.textual.shadow
[name resolution ambiguities]: #r-names.resolution.expansion.imports.ambiguity
[namespaces]: ../names/namespaces.md
[outer scope]: #r-names.resolution.general.scopes
[path-based scope]: ../macros.md#r-macro.invocation.name-resolution
[scope]: ../names/scopes.md
[sub-namespace]: ../names/namespaces.md#r-names.namespaces.sub-namespaces
[type-relative paths]: names.resolution.type-relative
[visibility]: ../visibility-and-privacy.md
