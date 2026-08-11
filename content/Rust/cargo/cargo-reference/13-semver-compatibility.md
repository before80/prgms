+++
title = "13-SemVer 兼容性"
date = 2026-07-30T14:49:00+08:00
weight = 55
type = "docs"
description = "Cargo 视角下的语义化版本兼容规则"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Cargo Book](https://doc.rust-lang.org/cargo/)

# SemVer 兼容性


> 原文链接: [https://doc.rust-lang.org/cargo/reference/semver.html](https://doc.rust-lang.org/cargo/reference/semver.html)


本章详细说明对于包的新发布，按惯例什么被视为兼容或破坏性的 SemVer 变更。关于 SemVer 是什么，以及 Cargo 如何用它来确保库的兼容性，见 [SemVer 兼容性][SemVer compatibility] 一节。

这些只是*指南*，未必是所有项目都会遵守的硬性规则。[变更类别][Change categories] 一节说明本指南如何对变更的级别与严重程度分类。本指南大部分聚焦于会使 `cargo` 与 `rustc` 无法构建先前可工作内容的变更。几乎每项变更都有一定风险会负面影响运行时行为；对这些情况，是否属于 SemVer 不兼容变更通常由项目维护者判断。

[Change categories]: #change-categories
[SemVer compatibility]: ../specifying-dependencies/03-dependency-resolution/#semver-compatibility

## 变更类别 {#change-categories}
下列所有策略按变更级别分类：

* **主版本变更（Major change）**：需要提升 SemVer 主版本号的变更。
* **次版本变更（Minor change）**：仅需提升 SemVer 次版本号的变更。
* **可能破坏性变更（Possibly-breaking change）**：有些项目视为主版本、有些视为次版本的变更。

「可能破坏性」类别涵盖在更新时*有可能*破坏、但不一定造成破坏的变更。应仔细考虑这些变更的影响。具体性质取决于变更本身以及项目维护者的原则。

有些项目可能选择在次版本变更时只提升补丁号。鼓励遵循 SemVer 规范，仅在补丁发布中应用 bug 修复。不过，bug 修复可能需要标注为「次版本变更」的 API 变更，且不应影响兼容性。本指南不对每个单独的「次版本变更」应如何处理表态，因为次版本与补丁变更的差异是取决于变更性质的约定。

有些变更被标为「次版本」，即使它们带有破坏构建的潜在风险。这适用于潜在风险极低、且可能破坏的代码不太可能以惯用 Rust 写出、或被明确劝阻使用的情况。

本指南使用「主版本」与「次版本」术语时，假定对应「1.0.0」及之后的发布。以「0.y.z」开头的初始开发发布可将「y」的变更视为主版本发布，「z」视为次版本发布。「0.0.z」发布始终是主版本变更。这是因为 Cargo 约定：仅最左侧非零分量的变更被视为不兼容。

* API 兼容性
    * 项（Items）
        * [主版本变更：重命名/移动/移除任何公共项](#item-remove)
        * [次版本变更：添加新的公共项](#item-new)
    * 类型
        * [主版本变更：更改定义良好类型的对齐、布局或大小](#type-layout)
    * 结构体
        * [主版本变更：在当前字段均为公共时添加私有结构体字段](#struct-add-private-field-when-public)
        * [主版本变更：在不存在私有字段时添加公共字段](#struct-add-public-field-when-no-private)
        * [次版本变更：在已至少有一个私有字段时添加或移除私有字段](#struct-private-fields-with-private)
        * [次版本变更：从字段全部私有（且至少有一个字段）的元组结构体变为普通结构体，或反之](#struct-tuple-normal-with-private)
    * 枚举
        * [主版本变更：添加新的枚举变体（无 `non_exhaustive`）](#enum-variant-new)
        * [主版本变更：向枚举变体添加新字段](#enum-fields-new)
    * Trait
        * [主版本变更：添加无默认实现的 trait 项](#trait-new-item-no-default)
        * [主版本变更：对 trait 项签名的任何更改](#trait-item-signature)
        * [可能破坏性：添加有默认实现的 trait 项](#trait-new-default-item)
        * [主版本变更：添加使 trait 非对象安全的 trait 项](#trait-object-safety)
        * [主版本变更：添加无默认值的类型参数](#trait-new-parameter-no-default)
        * [次版本变更：添加有默认值的 trait 类型参数](#trait-new-parameter-default)
    * 实现
        * [可能破坏性变更：添加任何固有项](#impl-item-new)
    * 泛型
        * [主版本变更：收紧泛型约束](#generic-bounds-tighten)
        * [次版本变更：放宽泛型约束](#generic-bounds-loosen)
        * [次版本变更：添加有默认值的类型参数](#generic-new-default)
        * [次版本变更：将类型泛化以使用泛型（类型相同）](#generic-generalize-identical)
        * [主版本变更：将类型泛化以使用泛型（类型可能不同）](#generic-generalize-different)
        * [次版本变更：将泛型类型改为更泛型的类型](#generic-more-generic)
        * [主版本变更：在 RPIT 中捕获更多泛型参数](#generic-rpit-capture)
    * 函数
        * [主版本变更：添加/移除函数参数](#fn-change-arity)
        * [可能破坏性：引入新的函数类型参数](#fn-generic-new)
        * [次版本变更：将函数泛化以使用泛型（支持原类型）](#fn-generalize-compatible)
        * [主版本变更：将函数泛化以使用泛型但类型不匹配](#fn-generalize-mismatch)
        * [次版本变更：将 `unsafe` 函数改为安全](#fn-unsafe-safe)
    * 属性
        * [主版本变更：从支持 `no_std` 转为需要 `std`](#attr-no-std-to-std)
        * [主版本变更：向已有枚举、变体或无私有字段的结构体添加 `non_exhaustive`](#attr-adding-non-exhaustive)
* 工具与环境兼容性
    * [可能破坏性：更改所需的最低 Rust 版本](#env-new-rust)
    * [可能破坏性：更改平台与环境要求](#env-change-requirements)
    * [次版本变更：引入新的 lint](#new-lints)
    * Cargo
        * [次版本变更：添加新的 Cargo 特性](#cargo-feature-add)
        * [主版本变更：移除 Cargo 特性](#cargo-feature-remove)
        * [主版本变更：若会改变功能或公共项，则从特性列表中移除特性](#cargo-feature-remove-another)
        * [可能破坏性：移除可选依赖](#cargo-remove-opt-dep)
        * [次版本变更：更改依赖的特性](#cargo-change-dep-feature)
        * [次版本变更：添加依赖](#cargo-dep-add)
* [应用程序兼容性](#application-compatibility)

## API 兼容性 {#api-compatibility}
以下所有示例都包含三部分：原始代码、修改后的代码，以及可能出现在另一项目中的代码使用示例。在次版本变更中，示例用法应能在变更前后两个版本上成功构建。

### 主版本变更：重命名/移动/移除任何公共项 {#item-remove}

公开暴露的 [项][items] 不存在会导致对该项的任何使用无法编译。

```rust,ignore
// 主版本变更

///////////////////////////////////////////////////////////
// 变更前
pub fn foo() {}

///////////////////////////////////////////////////////////
// 变更后
// ... 项已被移除

///////////////////////////////////////////////////////////
// 将会破坏的示例用法。
fn main() {
    updated_crate::foo(); // Error: cannot find function `foo`
}
```

这包括添加任何可基于[条件编译][conditional compilation]改变可用项或行为的 [`cfg` 属性][`cfg` attribute]。

缓解策略：
* 将待移除的项标为 [deprecated]，然后在之后的 SemVer 破坏性发布中再移除它们。
* 将重命名的项标为 [deprecated]，并用 [`pub use`] 项重新导出到旧名称。

### 次版本变更：添加新的公共项 {#item-new}

添加新的公共 [项][items] 是次版本变更。

```rust,ignore
// 次版本变更

///////////////////////////////////////////////////////////
// 变更前
// ... 该项不存在

///////////////////////////////////////////////////////////
// 变更后
pub fn foo() {}

///////////////////////////////////////////////////////////
// 可安全工作的库使用示例。
// 未使用 `foo`，因为它先前不存在。
```

注意：在某些罕见情况下，由于通配导入，这可能是**破坏性变更**。例如，若你添加新 trait，而某项目使用了将该 trait 引入作用域的通配导入，且新 trait 引入了与其实现类型上已有项冲突的关联项，则可能因歧义导致编译时错误。示例：

```rust,ignore
// 破坏性变更示例

///////////////////////////////////////////////////////////
// 变更前
// ... 该 trait 不存在

///////////////////////////////////////////////////////////
// 变更后
pub trait NewTrait {
    fn foo(&self) {}
}

impl NewTrait for i32 {}

///////////////////////////////////////////////////////////
// 将会破坏的示例用法。
use updated_crate::*;

pub trait LocalTrait {
    fn foo(&self) {}
}

impl LocalTrait for i32 {}

fn main() {
    123i32.foo(); // Error:  multiple applicable items in scope
}
```

这不被视为主版本变更，因为按惯例通配导入是已知的前向兼容性风险。应避免从外部 crate 通配导入项。

### 主版本变更：更改定义良好类型的对齐、布局或大小 {#type-layout}

更改一个先前已定义良好（well-defined）的类型的对齐、布局或大小，属于破坏性变更。

一般来说，使用[默认表示][the default representation]的类型并没有定义良好的对齐、布局或大小。
编译器可以自由改变其对齐、布局或大小，因此代码不应对此作任何假定。

> **注意**：即使某类型的对齐、布局或大小并非定义良好，外部 crate 若对其作出假定，仍有可能被破坏。
> 这不被视为 SemVer 破坏性变更，因为本就不应作出这些假定。

以下是一些*不属于*破坏性变更的示例（前提是未违反本指南中的其他规则）：

* 以符合本指南其他规则的方式，添加、移除、重排或更改默认表示的结构体、联合体或枚举的字段（例如，使用 `non_exhaustive` 以允许这些变更，或更改本就私有的字段）。
  见 [struct-add-private-field-when-public](#struct-add-private-field-when-public)、[struct-add-public-field-when-no-private](#struct-add-public-field-when-no-private)、[struct-private-fields-with-private](#struct-private-fields-with-private)、[enum-fields-new](#enum-fields-new)。
* 若枚举使用了 `non_exhaustive`，向默认表示的枚举添加变体。
  这可能改变该枚举的对齐或大小，但它们本就不是定义良好的。
  见 [enum-variant-new](#enum-variant-new)。
* 在遵循本指南其他规则的前提下，添加、移除、重排或更改 `repr(C)` 结构体、联合体或枚举的私有字段（例如，使用 `non_exhaustive`，或在已存在其他私有字段时添加私有字段）。
  见 [repr-c-private-change](#repr-c-private-change)。
* 若枚举使用了 `non_exhaustive`，向 `repr(C)` 枚举添加变体。
  见 [repr-c-enum-variant-new](#repr-c-enum-variant-new)。
* 为默认表示的结构体、联合体或枚举添加 `repr(C)`。
  见 [repr-c-add](#repr-c-add)。
* 为枚举添加 `repr(<int>)`（[原始表示][primitive representation]）。
  见 [repr-int-enum-add](#repr-int-enum-add)。
* 为默认表示的结构体或枚举添加 `repr(transparent)`。
  见 [repr-transparent-add](#repr-transparent-add)。

对于使用 [`repr` 属性][`repr` attribute]的类型，可以认为其对齐与布局在某种程度上是有定义的，代码可能会据此作出某些假定，而更改该类型可能会破坏这些假定。

在某些情况下，带 `repr` 属性的类型的对齐、布局或大小仍可能不是定义良好的。
此时对这些类型作出更改可能是安全的，不过仍应谨慎。
例如，若类型带有私有字段，且未另行文档化其对齐、布局或大小的保证，则外部 crate 无法依赖它们，因为其公共 API 并未完整定义该类型的对齐、布局或大小。

带*私有*字段却仍属定义良好的一个常见例子是：使用 `repr(transparent)`、且只有单个泛型类型私有字段的类型，同时文档正文说明了它对该泛型类型是透明的。
例如可参见 [`UnsafeCell`]。

以下是一些破坏性变更的示例：

* 为结构体或联合体添加 `repr(packed)`。
  见 [repr-packed-add](#repr-packed-add)。
* 为结构体、联合体或枚举添加 `repr(align)`。
  见 [repr-align-add](#repr-align-add)。
* 从结构体或联合体移除 `repr(packed)`。
  见 [repr-packed-remove](#repr-packed-remove)。
* 更改 `repr(packed(N))` 中的 N 值，且该更改改变了对齐或布局。
  见 [repr-packed-n-change](#repr-packed-n-change)。
* 更改 `repr(align(N))` 中的 N 值，且该更改改变了对齐。
  见 [repr-align-n-change](#repr-align-n-change)。
* 从结构体、联合体或枚举移除 `repr(align)`。
  见 [repr-align-remove](#repr-align-remove)。
* 更改 `repr(C)` 类型中公共字段的顺序。
  见 [repr-c-shuffle](#repr-c-shuffle)。
* 从结构体、联合体或枚举移除 `repr(C)`。
  见 [repr-c-remove](#repr-c-remove)。
* 从枚举移除 `repr(<int>)`。
  见 [repr-int-enum-remove](#repr-int-enum-remove)。
* 更改 `repr(<int>)` 枚举的原始表示。
  见 [repr-int-enum-change](#repr-int-enum-change)。
* 从结构体或枚举移除 `repr(transparent)`。
  见 [repr-transparent-remove](#repr-transparent-remove)。

[the default representation]: https://doc.rust-lang.org/reference/type-layout.html#the-default-representation
[primitive representation]: https://doc.rust-lang.org/reference/type-layout.html#primitive-representations
[`repr` attribute]: https://doc.rust-lang.org/reference/type-layout.html#representations
[`std::mem::transmute`]: https://doc.rust-lang.org/std/mem/fn.transmute.html
[`UnsafeCell`]: https://doc.rust-lang.org/std/cell/struct.UnsafeCell.html#memory-layout

#### 次版本变更：为 `repr(C)` 类型添加、移除或更改私有字段 {#repr-c-private-change}

在遵循本指南其他准则的前提下（见 [struct-add-private-field-when-public](#struct-add-private-field-when-public)、[struct-add-public-field-when-no-private](#struct-add-public-field-when-no-private)、[struct-private-fields-with-private](#struct-private-fields-with-private)、[enum-fields-new](#enum-fields-new)），为 `repr(C)` 结构体、联合体或枚举添加、移除或更改私有字段通常是安全的。

例如，只有在已存在其他私有字段、或该类型是 `non_exhaustive` 的情况下，才能添加私有字段。
若存在私有字段、或该类型是 `non_exhaustive`，且添加不会改变其他字段的布局，则可以添加公共字段。

不过，这可能改变该类型的大小与对齐。
若大小或对齐发生变化，应格外小心。
除非类型已文档化其大小或对齐，否则代码不应对带私有字段或 `non_exhaustive` 的类型的大小或对齐作出假定。

```rust,ignore
// 次版本变更

///////////////////////////////////////////////////////////
// 变更前
#[derive(Default)]
#[repr(C)]
pub struct Example {
    pub f1: i32,
    f2: i32, // 私有字段
}

///////////////////////////////////////////////////////////
// 变更后
#[derive(Default)]
#[repr(C)]
pub struct Example {
    pub f1: i32,
    f2: i32,
    f3: i32, // 新字段
}

///////////////////////////////////////////////////////////
// 可安全工作的库使用示例。
fn main() {
    // 注意：用户不应假定大小或对齐
    // 因为它们未文档化。
    let f = updated_crate::Example::default();
}
```

#### 次版本变更：为 `repr(C)` 枚举添加变体 {#repr-c-enum-variant-new}

若枚举使用了 `non_exhaustive`，则向 `repr(C)` 枚举添加变体通常是安全的。
更多讨论见 [enum-variant-new](#enum-variant-new)。

注意，由于这会改变该类型的大小与对齐，因此也可能构成破坏性变更。
类似的注意事项见 [repr-c-private-change](#repr-c-private-change)。

```rust,ignore
// 次版本变更

///////////////////////////////////////////////////////////
// 变更前
#[repr(C)]
#[non_exhaustive]
pub enum Example {
    Variant1 { f1: i16 },
    Variant2 { f1: i32 },
}

///////////////////////////////////////////////////////////
// 变更后
#[repr(C)]
#[non_exhaustive]
pub enum Example {
    Variant1 { f1: i16 },
    Variant2 { f1: i32 },
    Variant3 { f1: i64 }, // 已添加
}

///////////////////////////////////////////////////////////
// 可安全工作的库使用示例。
fn main() {
    // 注意：用户不应假定大小或对齐
    // 因为它们未指定。例如，这使大小从 8
    // 增加到 16 字节。
    let f = updated_crate::Example::Variant2 { f1: 123 };
}
```

#### 次版本变更：为默认表示的类型添加 `repr(C)` {#repr-c-add}

为采用[默认表示][the default representation]的结构体、联合体或枚举添加 `repr(C)` 是安全的。
之所以安全，是因为用户不应对采用默认表示的类型的对齐、布局或大小作出假定。

```rust,ignore
// 次版本变更

///////////////////////////////////////////////////////////
// 变更前
pub struct Example {
    pub f1: i32,
    pub f2: i16,
}

///////////////////////////////////////////////////////////
// 变更后
#[repr(C)] // 已添加
pub struct Example {
    pub f1: i32,
    pub f2: i16,
}

///////////////////////////////////////////////////////////
// 可安全工作的库使用示例。
fn main() {
    let f = updated_crate::Example { f1: 123, f2: 456 };
}
```

#### 次版本变更：为枚举添加 `repr(<int>)` {#repr-int-enum-add}

为采用[默认表示][the default representation]的枚举添加 `repr(<int>)`（[原始表示][primitive representation]）是安全的。
之所以安全，是因为用户不应对采用默认表示的枚举的对齐、布局或大小作出假定。

```rust,ignore
// 次版本变更

///////////////////////////////////////////////////////////
// 变更前
pub enum E {
    Variant1,
    Variant2(i32),
    Variant3 { f1: f64 },
}

///////////////////////////////////////////////////////////
// 变更后
#[repr(i32)] // 已添加
pub enum E {
    Variant1,
    Variant2(i32),
    Variant3 { f1: f64 },
}

///////////////////////////////////////////////////////////
// 可安全工作的库使用示例。
fn main() {
    let x = updated_crate::E::Variant3 { f1: 1.23 };
}
```

#### 次版本变更：为默认表示的结构体或枚举添加 `repr(transparent)` {#repr-transparent-add}

为采用[默认表示][the default representation]的结构体或枚举添加 `repr(transparent)` 是安全的。
之所以安全，是因为用户不应对采用默认表示的结构体或枚举的对齐、布局或大小作出假定。

```rust,ignore
// 次版本变更

///////////////////////////////////////////////////////////
// 变更前
#[derive(Default)]
pub struct Example<T>(T);

///////////////////////////////////////////////////////////
// 变更后
#[derive(Default)]
#[repr(transparent)] // 已添加
pub struct Example<T>(T);

///////////////////////////////////////////////////////////
// 可安全工作的库使用示例。
fn main() {
    let x = updated_crate::Example::<i32>::default();
}
```

#### 主版本变更：为结构体或联合体添加 `repr(packed)` {#repr-packed-add}

为结构体或联合体添加 `repr(packed)` 属于破坏性变更。
将类型标为 `repr(packed)` 会带来可能破坏代码的变化，例如无法合法地取字段的引用，或导致闭包的不相交捕获（disjoint closure captures）被截断。

<!-- TODO: If all fields are private, should this be safe to do? -->

```rust,ignore
// 主版本变更

///////////////////////////////////////////////////////////
// 变更前
pub struct Example {
    pub f1: u8,
    pub f2: u16,
}

///////////////////////////////////////////////////////////
// 变更后
#[repr(packed)] // 已添加
pub struct Example {
    pub f1: u8,
    pub f2: u16,
}

///////////////////////////////////////////////////////////
// 将会破坏的示例用法。
fn main() {
    let f = updated_crate::Example { f1: 1, f2: 2 };
    let x = &f.f2; // Error: error[E0793]: reference to field of packed struct is unaligned
}
```

```rust,ignore
// 主版本变更

///////////////////////////////////////////////////////////
// 变更前
pub struct Example(pub i32, pub i32);

///////////////////////////////////////////////////////////
// 变更后
#[repr(packed)]
pub struct Example(pub i32, pub i32);

///////////////////////////////////////////////////////////
// 将会破坏的示例用法。
fn main() {
    let mut f = updated_crate::Example(123, 456);
    let c = || {
        // 没有 repr(packed) 时，闭包精确捕获 `&f.0`。
        // 有 repr(packed) 时，闭包捕获 `&f` 以避免未定义行为。
        let a = f.0;
    };
    f.1 = 789; // Error: cannot assign to `f.1` because it is borrowed
    c();
}
```

#### 主版本变更：为结构体、联合体或枚举添加 `repr(align)` {#repr-align-add}

为结构体、联合体或枚举添加 `repr(align)` 属于破坏性变更。
将类型标为 `repr(align)` 会破坏在 `repr(packed)` 类型中对该类型的任何使用，因为这种组合是不被允许的。

<!-- TODO: This seems like it should be extraordinarily rare. Should there be any exceptions carved out for this? -->

```rust,ignore
// 主版本变更

///////////////////////////////////////////////////////////
// 变更前
pub struct Aligned {
    pub a: i32,
}

///////////////////////////////////////////////////////////
// 变更后
#[repr(align(8))] // 已添加
pub struct Aligned {
    pub a: i32,
}

///////////////////////////////////////////////////////////
// 将会破坏的示例用法。
use updated_crate::Aligned;

#[repr(packed)]
pub struct Packed { // Error: packed type cannot transitively contain a `#[repr(align)]` type
    f1: Aligned,
}

fn main() {
    let p = Packed {
        f1: Aligned { a: 123 },
    };
}
```

#### 主版本变更：从结构体或联合体移除 `repr(packed)` {#repr-packed-remove}

从结构体或联合体移除 `repr(packed)` 属于破坏性变更。
这可能改变外部 crate 所依赖的对齐或布局。

如果存在公共字段，移除 `repr(packed)` 可能改变闭包不相交捕获的行为方式。
在某些情况下这会破坏代码，类似于[版次指南][edition-closures]中所述的情形。

[edition-closures]: https://doc.rust-lang.org/edition-guide/rust-2021/disjoint-capture-in-closures.html

```rust,ignore
// 主版本变更

///////////////////////////////////////////////////////////
// 变更前
#[repr(C, packed)]
pub struct Packed {
    pub a: u8,
    pub b: u16,
}

///////////////////////////////////////////////////////////
// 变更后
#[repr(C)] // 已移除 packed
pub struct Packed {
    pub a: u8,
    pub b: u16,
}

///////////////////////////////////////////////////////////
// 将会破坏的示例用法。
use updated_crate::Packed;

fn main() {
    let p = Packed { a: 1, b: 2 };
    // 关于该类型大小的某种假定。
    // 没有 `packed` 时会失败，因为大小为 4。
    const _: () = assert!(std::mem::size_of::<Packed>() == 3); // Error: assertion failed
}
```

```rust,ignore
// 主版本变更

///////////////////////////////////////////////////////////
// 变更前
#[repr(C, packed)]
pub struct Packed {
    pub a: *mut i32,
    pub b: i32,
}
unsafe impl Send for Packed {}

///////////////////////////////////////////////////////////
// 变更后
#[repr(C)] // 已移除 packed
pub struct Packed {
    pub a: *mut i32,
    pub b: i32,
}
unsafe impl Send for Packed {}

///////////////////////////////////////////////////////////
// 将会破坏的示例用法。
use updated_crate::Packed;

fn main() {
    let mut x = 123;

    let p = Packed {
        a: &mut x as *mut i32,
        b: 456,
    };

    // 结构体 packed 时，闭包捕获 `p`（它是 Send）。
    // 移除 `packed` 后，最终捕获的是非 Send 的 `p.a`。
    std::thread::spawn(move || unsafe {
        *(p.a) += 1; // Error: cannot be sent between threads safely
    });
}
```

#### 主版本变更：更改 `repr(packed(N))` 的 N 值且改变了对齐或布局 {#repr-packed-n-change}

若更改 `repr(packed(N))` 的 N 值改变了对齐或布局，则属于破坏性变更。
这可能改变外部 crate 所依赖的对齐或布局。

若把 `N` 降到低于某个公共字段的对齐值，就会破坏任何试图取该字段引用的代码。

注意，对 `N` 的某些更改可能并不改变对齐或布局，例如当前值已等于该类型的自然对齐时再调大它。

```rust,ignore
// 主版本变更

///////////////////////////////////////////////////////////
// 变更前
#[repr(packed(4))]
pub struct Packed {
    pub a: u8,
    pub b: u32,
}

///////////////////////////////////////////////////////////
// 变更后
#[repr(packed(2))] // 已改为 2
pub struct Packed {
    pub a: u8,
    pub b: u32,
}

///////////////////////////////////////////////////////////
// 将会破坏的示例用法。
use updated_crate::Packed;

fn main() {
    let p = Packed { a: 1, b: 2 };
    let x = &p.b; // Error: error[E0793]: reference to field of packed struct is unaligned
}
```

#### 主版本变更：更改 `repr(align(N))` 的 N 值且改变了对齐 {#repr-align-n-change}

若更改 `repr(align(N))` 的 `N` 值改变了对齐，则属于破坏性变更。
这可能改变外部 crate 所依赖的对齐。

如果该类型按[类型布局](#type-layout)一节的讨论并非定义良好（例如含有私有字段且未文档化其对齐或布局），那么作此更改应当是安全的。

注意，对 `N` 的某些更改可能并不改变对齐或布局，例如当前值已等于或小于该类型的自然对齐时再调小它。

```rust,ignore
// 主版本变更

///////////////////////////////////////////////////////////
// 变更前
#[repr(align(8))]
pub struct Packed {
    pub a: u8,
    pub b: u32,
}

///////////////////////////////////////////////////////////
// 变更后
#[repr(align(4))] // 已改为 4
pub struct Packed {
    pub a: u8,
    pub b: u32,
}

///////////////////////////////////////////////////////////
// 将会破坏的示例用法。
use updated_crate::Packed;

fn main() {
    let p = Packed { a: 1, b: 2 };
    // 关于该类型大小的某种假定。
    // 对齐已从 8 变为 4。
    const _: () = assert!(std::mem::align_of::<Packed>() == 8); // Error: assertion failed
}
```

#### 主版本变更：从结构体、联合体或枚举移除 `repr(align)` {#repr-align-remove}

若结构体、联合体或枚举的布局是定义良好的，从中移除 `repr(align)` 属于破坏性变更。
这可能改变外部 crate 所依赖的对齐或布局。

如果该类型按[类型布局](#type-layout)一节的讨论并非定义良好（例如含有私有字段且未文档化其对齐），那么作此更改应当是安全的。

```rust,ignore
// 主版本变更

///////////////////////////////////////////////////////////
// 变更前
#[repr(C, align(8))]
pub struct Packed {
    pub a: u8,
    pub b: u32,
}

///////////////////////////////////////////////////////////
// 变更后
#[repr(C)] // 已移除 align
pub struct Packed {
    pub a: u8,
    pub b: u32,
}

///////////////////////////////////////////////////////////
// 将会破坏的示例用法。
use updated_crate::Packed;

fn main() {
    let p = Packed { a: 1, b: 2 };
    // 关于该类型大小的某种假定。
    // 对齐已从 8 变为 4。
    const _: () = assert!(std::mem::align_of::<Packed>() == 8); // Error: assertion failed
}
```

#### 主版本变更：更改 `repr(C)` 类型中公共字段的顺序 {#repr-c-shuffle}

更改 `repr(C)` 类型中公共字段的顺序属于破坏性变更。
外部 crate 可能依赖这些字段的特定顺序。

```rust,ignore,run-fail
// 主版本变更

///////////////////////////////////////////////////////////
// 变更前
#[repr(C)]
pub struct SpecificLayout {
    pub a: u8,
    pub b: u32,
}

///////////////////////////////////////////////////////////
// 变更后
#[repr(C)]
pub struct SpecificLayout {
    pub b: u32, // 已更改顺序
    pub a: u8,
}

///////////////////////////////////////////////////////////
// 将会破坏的示例用法。
use updated_crate::SpecificLayout;

unsafe extern "C" {
    // 此 C 函数假定了 C 头文件中定义的特定布局。
    fn c_fn_get_b(x: &SpecificLayout) -> u32;
}

fn main() {
    let p = SpecificLayout { a: 1, b: 2 };
    unsafe { assert_eq!(c_fn_get_b(&p), 2) } // Error: value not equal to 2
}

# mod cdep {
# // 这里模拟的是通常由构建脚本引入的内容。
# // 该定义原本位于某个 C 头文件中。
# #[repr(C)]
# pub struct SpecificLayout {
# pub a: u8,
# pub b: u32,
# }
# #[no_mangle]
# pub fn c_fn_get_b(x: &SpecificLayout) -> u32 {
# x.b
# }
# }
```

#### 主版本变更：从结构体、联合体或枚举移除 `repr(C)` {#repr-c-remove}

从结构体、联合体或枚举移除 `repr(C)` 属于破坏性变更。
外部 crate 可能依赖该类型的特定布局。

```rust,ignore
// 主版本变更

///////////////////////////////////////////////////////////
// 变更前
#[repr(C)]
pub struct SpecificLayout {
    pub a: u8,
    pub b: u32,
}

///////////////////////////////////////////////////////////
// 变更后
// 已移除 repr(C)
pub struct SpecificLayout {
    pub a: u8,
    pub b: u32,
}

///////////////////////////////////////////////////////////
// 将会破坏的示例用法。
use updated_crate::SpecificLayout;

unsafe extern "C" {
    // 此 C 函数假定了 C 头文件中定义的特定布局。
    fn c_fn_get_b(x: &SpecificLayout) -> u32; // Error: is not FFI-safe
}

fn main() {
    let p = SpecificLayout { a: 1, b: 2 };
    unsafe { assert_eq!(c_fn_get_b(&p), 2) }
}

# mod cdep {
# // 这里模拟的是通常由构建脚本引入的内容。
# // 该定义原本位于某个 C 头文件中。
# #[repr(C)]
# pub struct SpecificLayout {
# pub a: u8,
# pub b: u32,
# }
# #[no_mangle]
# pub fn c_fn_get_b(x: &SpecificLayout) -> u32 {
# x.b
# }
# }
```

#### 主版本变更：从枚举移除 `repr(<int>)` {#repr-int-enum-remove}

从枚举移除 `repr(<int>)` 属于破坏性变更。
外部 crate 可能假定判别值（discriminant）具有特定大小。
例如，对枚举执行 [`std::mem::transmute`] 可能会失败。

```rust,ignore
// 主版本变更

///////////////////////////////////////////////////////////
// 变更前
#[repr(u16)]
pub enum Example {
    Variant1,
    Variant2,
    Variant3,
}

///////////////////////////////////////////////////////////
// 变更后
// 已移除 repr(u16)
pub enum Example {
    Variant1,
    Variant2,
    Variant3,
}

///////////////////////////////////////////////////////////
// 将会破坏的示例用法。

fn main() {
    let e = updated_crate::Example::Variant2;
    let i: u16 = unsafe { std::mem::transmute(e) }; // Error: cannot transmute between types of different sizes
}
```

#### 主版本变更：更改 `repr(<int>)` 枚举的原始表示 {#repr-int-enum-change}

更改 `repr(<int>)` 枚举的原始表示属于破坏性变更。
外部 crate 可能假定判别值（discriminant）具有特定大小。
例如，对枚举执行 [`std::mem::transmute`] 可能会失败。

```rust,ignore
// 主版本变更

///////////////////////////////////////////////////////////
// 变更前
#[repr(u16)]
pub enum Example {
    Variant1,
    Variant2,
    Variant3,
}

///////////////////////////////////////////////////////////
// 变更后
#[repr(u8)] // 已更改 repr 大小
pub enum Example {
    Variant1,
    Variant2,
    Variant3,
}

///////////////////////////////////////////////////////////
// 将会破坏的示例用法。

fn main() {
    let e = updated_crate::Example::Variant2;
    let i: u16 = unsafe { std::mem::transmute(e) }; // Error: cannot transmute between types of different sizes
}
```

#### 主版本变更：从结构体或枚举移除 `repr(transparent)` {#repr-transparent-remove}

从结构体或枚举移除 `repr(transparent)` 属于破坏性变更。
外部 crate 可能依赖该类型具有其透明字段的对齐、布局或大小。

```rust,ignore
// 主版本变更

///////////////////////////////////////////////////////////
// 变更前
#[repr(transparent)]
pub struct Transparent<T>(T);

///////////////////////////////////////////////////////////
// 变更后
// 已移除 repr
pub struct Transparent<T>(T);

///////////////////////////////////////////////////////////
// 将会破坏的示例用法。
#![deny(improper_ctypes)]
use updated_crate::Transparent;

unsafe extern "C" {
    fn c_fn() -> Transparent<f64>; // Error: is not FFI-safe
}

fn main() {}
```

### 主版本变更：在当前字段均为公共时添加私有结构体字段 {#struct-add-private-field-when-public}

当向一个此前字段全为公共的结构体添加私有字段时，
任何试图用[结构体字面量][struct literal]构造它的代码都会被破坏。

```rust,ignore
// 主版本变更

///////////////////////////////////////////////////////////
// 变更前
pub struct Foo {
    pub f1: i32,
}

///////////////////////////////////////////////////////////
// 变更后
pub struct Foo {
    pub f1: i32,
    f2: i32,
}

///////////////////////////////////////////////////////////
// 将会破坏的示例用法。
fn main() {
    let x = updated_crate::Foo { f1: 123 }; // Error: cannot construct `Foo`
}
```

缓解策略：
* 不要向字段全为公共的结构体添加新字段。
* 在首次引入结构体时就将其标记为 [`#[non_exhaustive]`][non_exhaustive]，
  以阻止用户使用结构体字面量语法，转而提供构造方法和/或 [Default] 实现。

### 主版本变更：在不存在私有字段时添加公共字段 {#struct-add-public-field-when-no-private}

当向一个字段全为公共的结构体添加公共字段时，
任何试图用[结构体字面量][struct literal]构造它的代码都会被破坏。

```rust,ignore
// 主版本变更

///////////////////////////////////////////////////////////
// 变更前
pub struct Foo {
    pub f1: i32,
}

///////////////////////////////////////////////////////////
// 变更后
pub struct Foo {
    pub f1: i32,
    pub f2: i32,
}

///////////////////////////////////////////////////////////
// 将会破坏的示例用法。
fn main() {
    let x = updated_crate::Foo { f1: 123 }; // Error: missing field `f2`
}
```

缓解策略：
* 不要向字段全为公共的结构体添加新字段。
* 在首次引入结构体时就将其标记为 [`#[non_exhaustive]`][non_exhaustive]，
  以阻止用户使用结构体字面量语法，转而提供构造方法和/或 [Default] 实现。

### 次版本变更：在已至少有一个私有字段时添加或移除私有字段 {#struct-private-fields-with-private}

当结构体已至少有一个私有字段时，向其添加或从中移除私有字段是安全的。

```rust,ignore
// 次版本变更

///////////////////////////////////////////////////////////
// 变更前
#[derive(Default)]
pub struct Foo {
    f1: i32,
}

///////////////////////////////////////////////////////////
// 变更后
#[derive(Default)]
pub struct Foo {
    f2: f64,
}

///////////////////////////////////////////////////////////
// 可安全工作的库使用示例。
fn main() {
    // 无法访问私有字段。
    let x = updated_crate::Foo::default();
}
```

这是安全的，因为已有代码既不能用[结构体字面量][struct literal]构造它，
也不能穷尽匹配其内容。

注意，对于元组结构体，如果元组中含有公共字段，且添加或移除私有字段改变了
任何公共字段的索引，那么这就是**主版本变更**。

```rust,ignore
// 主版本变更

///////////////////////////////////////////////////////////
// 变更前
#[derive(Default)]
pub struct Foo(pub i32, i32);

///////////////////////////////////////////////////////////
// 变更后
#[derive(Default)]
pub struct Foo(f64, pub i32, i32);

///////////////////////////////////////////////////////////
// 将会破坏的示例用法。
fn main() {
    let x = updated_crate::Foo::default();
    let y = x.0; // Error: is private
}
```

### 次版本变更：从字段全部私有（且至少有一个字段）的元组结构体变为普通结构体，或反之 {#struct-tuple-normal-with-private}

如果所有字段都是私有的，把元组结构体改为普通结构体（或反之）是安全的。

```rust,ignore
// 次版本变更

///////////////////////////////////////////////////////////
// 变更前
#[derive(Default)]
pub struct Foo(i32);

///////////////////////////////////////////////////////////
// 变更后
#[derive(Default)]
pub struct Foo {
    f1: i32,
}

///////////////////////////////////////////////////////////
// 可安全工作的库使用示例。
fn main() {
    // 无法访问私有字段。
    let x = updated_crate::Foo::default();
}
```

这是安全的，因为已有代码既不能用[结构体字面量][struct literal]构造它，
也不能匹配其内容。

### 主版本变更：添加新的枚举变体（无 `non_exhaustive`） {#enum-variant-new}

如果枚举没有使用 [`#[non_exhaustive]`][non_exhaustive] 属性，
那么为其添加新变体属于破坏性变更。

```rust,ignore
// 主版本变更

///////////////////////////////////////////////////////////
// 变更前
pub enum E {
    Variant1,
}

///////////////////////////////////////////////////////////
// 变更后
pub enum E {
    Variant1,
    Variant2,
}

///////////////////////////////////////////////////////////
// 将会破坏的示例用法。
fn main() {
    use updated_crate::E;
    let x = E::Variant1;
    match x { // Error: `E::Variant2` not covered
        E::Variant1 => {}
    }
}
```

缓解策略：
* 在引入枚举时就将其标记为 [`#[non_exhaustive]`][non_exhaustive]，
  以强制用户使用[通配模式][wildcard patterns]来涵盖新变体。

### 主版本变更：向枚举变体添加新字段 {#enum-fields-new}

向枚举变体添加新字段属于破坏性变更，因为其所有字段都是公共的，
构造与匹配都会编译失败。

```rust,ignore
// 主版本变更

///////////////////////////////////////////////////////////
// 变更前
pub enum E {
    Variant1 { f1: i32 },
}

///////////////////////////////////////////////////////////
// 变更后
pub enum E {
    Variant1 { f1: i32, f2: i32 },
}

///////////////////////////////////////////////////////////
// 将会破坏的示例用法。
fn main() {
    use updated_crate::E;
    let x = E::Variant1 { f1: 1 }; // Error: missing f2
    match x {
        E::Variant1 { f1 } => {} // Error: missing f2
    }
}
```

缓解策略：
* 在引入枚举时就将变体标记为 [`non_exhaustive`][non_exhaustive]，
  使其在不使用通配模式的情况下无法被构造或匹配。
  ```rust,ignore,skip
  pub enum E {
      #[non_exhaustive]
      Variant1{f1: i32}
  }
  ```
* 在引入枚举时，使用显式的结构体作为值，这样你就能控制字段的可见性。
  ```rust,ignore,skip
  pub struct Foo {
     f1: i32,
     f2: i32,
  }
  pub enum E {
      Variant1(Foo)
  }
  ```

### 主版本变更：添加无默认实现的 trait 项 {#trait-new-item-no-default}

向 trait 添加没有默认实现的项属于破坏性变更。这会破坏该 trait 的所有实现者。

```rust,ignore
// 主版本变更

///////////////////////////////////////////////////////////
// 变更前
pub trait Trait {}

///////////////////////////////////////////////////////////
// 变更后
pub trait Trait {
    fn foo(&self);
}

///////////////////////////////////////////////////////////
// 将会破坏的示例用法。
use updated_crate::Trait;
struct Foo;

impl Trait for Foo {}  // Error: not all trait items implemented
```

缓解策略：
* 始终为新的关联 trait 项提供默认实现或默认值。
* 在引入 trait 时，使用[密封 trait（sealed trait）][sealed trait]技巧，
  以阻止 crate 外部的用户实现该 trait。

### 主版本变更：对 trait 项签名的任何更改 {#trait-item-signature}

对 trait 项签名作出任何更改都属于破坏性变更。这可能破坏该 trait 的外部实现者。

```rust,ignore
// 主版本变更

///////////////////////////////////////////////////////////
// 变更前
pub trait Trait {
    fn f(&self, x: i32) {}
}

///////////////////////////////////////////////////////////
// 变更后
pub trait Trait {
    // 对于密封 trait 或普通函数，这属于次版本变更，
    // 因为用泛型作泛化只会严格扩大可用范围。
    // 但在此处，trait 的实现必须使用相同的签名。
    fn f<V>(&self, x: V) {}
}

///////////////////////////////////////////////////////////
// 将会破坏的示例用法。
use updated_crate::Trait;
struct Foo;

impl Trait for Foo {
    fn f(&self, x: i32) {}  // Error: trait declaration has 1 type parameter
}
```

缓解策略：
* 通过引入带默认实现的新项来承载新功能，而不是修改已有项。
* 在引入 trait 时，使用[密封 trait（sealed trait）][sealed trait]技巧，
  以阻止 crate 外部的用户实现该 trait。

### 可能破坏性变更：添加有默认实现的 trait 项 {#trait-new-default-item}

添加带默认实现的 trait 项通常是安全的。不过，这有时会导致编译错误。
例如，若另一个 trait 中存在同名方法，就可能引入歧义。

```rust,ignore
// 破坏性变更示例

///////////////////////////////////////////////////////////
// 变更前
pub trait Trait {}

///////////////////////////////////////////////////////////
// 变更后
pub trait Trait {
    fn foo(&self) {}
}

///////////////////////////////////////////////////////////
// 将会破坏的示例用法。
use updated_crate::Trait;
struct Foo;

trait LocalTrait {
    fn foo(&self) {}
}

impl Trait for Foo {}
impl LocalTrait for Foo {}

fn main() {
    let x = Foo;
    x.foo(); // Error: multiple applicable items in scope
}
```

注意，对于[固有实现（inherent implementations）][inherent
implementations]上的名字冲突，*不存在*这种歧义，因为它们优先于 trait 项。

添加 trait 项时需要考虑的一个特殊情况，见 [trait-object-safety](#trait-object-safety)。

缓解策略：
* 有些项目可能认为这种破坏是可接受的，尤其当新项的名字不太可能与现有代码冲突时。
  请谨慎选择名字以帮助避免这类冲突。此外，也可以认为在更新依赖时，
  要求下游用户添加[消歧语法][disambiguation syntax]来选择正确的函数是可接受的。

### 主版本变更：添加使 trait 非对象安全的 trait 项 {#trait-object-safety}

添加会让 trait 不再[对象安全（object safe）][object safe]的 trait 项属于破坏性变更。

```rust,ignore
// 主版本变更

///////////////////////////////////////////////////////////
// 变更前
pub trait Trait {}

///////////////////////////////////////////////////////////
// 变更后
pub trait Trait {
    // 关联常量会使该 trait 不再是对象安全的。
    const CONST: i32 = 123;
}

///////////////////////////////////////////////////////////
// 将会破坏的示例用法。
use updated_crate::Trait;
struct Foo;

impl Trait for Foo {}

fn main() {
    let obj: Box<dyn Trait> = Box::new(Foo); // Error: the trait `updated_crate::Trait` is not dyn compatible
}
```

反过来做（把非对象安全的 trait 变成对象安全的）则是安全的。

### 主版本变更：添加无默认值的类型参数 {#trait-new-parameter-no-default}

向 trait 添加没有默认值的类型参数属于破坏性变更。

```rust,ignore
// 主版本变更

///////////////////////////////////////////////////////////
// 变更前
pub trait Trait {}

///////////////////////////////////////////////////////////
// 变更后
pub trait Trait<T> {}

///////////////////////////////////////////////////////////
// 将会破坏的示例用法。
use updated_crate::Trait;
struct Foo;

impl Trait for Foo {}  // Error: missing generics
```

缓解策略：
* 见[添加有默认值的 trait 类型参数](#trait-new-parameter-default)。

### 次版本变更：添加有默认值的 trait 类型参数 {#trait-new-parameter-default}

只要类型参数带有默认值，向 trait 添加它就是安全的。
外部实现者会使用该默认值，无需指定这个参数。

```rust,ignore
// 次版本变更

///////////////////////////////////////////////////////////
// 变更前
pub trait Trait {}

///////////////////////////////////////////////////////////
// 变更后
pub trait Trait<T = i32> {}

///////////////////////////////////////////////////////////
// 可安全工作的库使用示例。
use updated_crate::Trait;
struct Foo;

impl Trait for Foo {}
```

### 可能破坏性变更：添加任何固有项 {#impl-item-new}

通常向实现中添加固有项应当是安全的，因为固有项优先于 trait 项。
不过在某些情况下，若其名字与某个已实现的、签名不同的 trait 项相同，
这种冲突就会引发问题。

```rust,ignore
// 破坏性变更示例

///////////////////////////////////////////////////////////
// 变更前
pub struct Foo;

///////////////////////////////////////////////////////////
// 变更后
pub struct Foo;

impl Foo {
    pub fn foo(&self) {}
}

///////////////////////////////////////////////////////////
// 将会破坏的示例用法。
use updated_crate::Foo;

trait Trait {
    fn foo(&self, x: i32) {}
}

impl Trait for Foo {}

fn main() {
    let x = Foo;
    x.foo(1); // Error: this method takes 0 arguments but 1 argument was supplied
}
```

注意，如果签名相同，就不会有编译期错误，
但可能造成运行时行为的悄然变化（因为现在执行的是另一个函数）。

缓解策略：
* 有些项目可能认为这种破坏是可接受的，尤其当新项的名字不太可能与现有代码冲突时。
  请谨慎选择名字以帮助避免这类冲突。此外，也可以认为在更新依赖时，
  要求下游用户添加[消歧语法][disambiguation syntax]来选择正确的函数是可接受的。

### 主版本变更：收紧泛型约束 {#generic-bounds-tighten}

收紧类型上的泛型约束属于破坏性变更，因为这会破坏那些依赖更宽松约束的用户。

```rust,ignore
// 主版本变更

///////////////////////////////////////////////////////////
// 变更前
pub struct Foo<A> {
    pub f1: A,
}

///////////////////////////////////////////////////////////
// 变更后
pub struct Foo<A: Eq> {
    pub f1: A,
}

///////////////////////////////////////////////////////////
// 将会破坏的示例用法。
use updated_crate::Foo;

fn main() {
    let s = Foo { f1: 1.23 }; // Error: the trait bound `{float}: Eq` is not satisfied
}
```

### 次版本变更：放宽泛型约束 {#generic-bounds-loosen}

放宽类型上的泛型约束是安全的，因为这只会扩大被允许的范围。

```rust,ignore
// 次版本变更

///////////////////////////////////////////////////////////
// 变更前
pub struct Foo<A: Clone> {
    pub f1: A,
}

///////////////////////////////////////////////////////////
// 变更后
pub struct Foo<A> {
    pub f1: A,
}

///////////////////////////////////////////////////////////
// 可安全工作的库使用示例。
use updated_crate::Foo;

fn main() {
    let s = Foo { f1: 123 };
}
```

### 次版本变更：添加有默认值的类型参数 {#generic-new-default}

只要类型参数带有默认值，向类型添加它就是安全的。
所有已有的引用都会使用该默认值，无需指定这个参数。

```rust,ignore
// 次版本变更

///////////////////////////////////////////////////////////
// 变更前
#[derive(Default)]
pub struct Foo {}

///////////////////////////////////////////////////////////
// 变更后
#[derive(Default)]
pub struct Foo<A = i32> {
    f1: A,
}

///////////////////////////////////////////////////////////
// 可安全工作的库使用示例。
use updated_crate::Foo;

fn main() {
    let s: Foo = Default::default();
}
```

### 次版本变更：将类型泛化以使用泛型（类型相同） {#generic-generalize-identical}

结构体或枚举的字段可以从具体类型改为泛型类型参数，
前提是该变更对所有现有用例都产生相同的类型。例如，下面的变更是允许的：

```rust,ignore
// 次版本变更

///////////////////////////////////////////////////////////
// 变更前
pub struct Foo(pub u8);

///////////////////////////////////////////////////////////
// 变更后
pub struct Foo<T = u8>(pub T);

///////////////////////////////////////////////////////////
// 可安全工作的库使用示例。
use updated_crate::Foo;

fn main() {
    let s: Foo = Foo(123);
}
```

这是因为对 `Foo` 的既有使用其实是 `Foo<u8>` 的简写，二者产生相同的字段类型。

### 主版本变更：将类型泛化以使用泛型（类型可能不同） {#generic-generalize-different}

如果类型可能发生改变，那么把结构体或枚举字段从具体类型改为泛型类型参数就可能造成破坏。

```rust,ignore
// 主版本变更

///////////////////////////////////////////////////////////
// 变更前
pub struct Foo<T = u8>(pub T, pub u8);

///////////////////////////////////////////////////////////
// 变更后
pub struct Foo<T = u8>(pub T, pub T);

///////////////////////////////////////////////////////////
// 将会破坏的示例用法。
use updated_crate::Foo;

fn main() {
    let s: Foo<f32> = Foo(3.14, 123); // Error: mismatched types
}
```

### 次版本变更：将泛型类型改为更泛型的类型 {#generic-more-generic}

把泛型类型改得更泛型是安全的。例如，下面添加了一个默认为原类型的泛型参数，
这是安全的，因为所有已有用户对两个字段使用的都是同一类型，
无需指定这个带默认值的参数。

```rust,ignore
// 次版本变更

///////////////////////////////////////////////////////////
// 变更前
pub struct Foo<T>(pub T, pub T);

///////////////////////////////////////////////////////////
// 变更后
pub struct Foo<T, U = T>(pub T, pub U);

///////////////////////////////////////////////////////////
// 可安全工作的库使用示例。
use updated_crate::Foo;

fn main() {
    let s: Foo<f32> = Foo(1.0, 2.0);
}
```

### 主版本变更：在 RPIT 中捕获更多泛型参数 {#generic-rpit-capture}

在 [RPIT]（return-position impl trait，返回位置的 impl trait）中捕获额外的泛型参数属于破坏性变更。

```rust,ignore
// 主版本变更

///////////////////////////////////////////////////////////
// 变更前
pub fn f<'a, 'b>(x: &'a str, y: &'b str) -> impl Iterator<Item = char> + use<'a> {
    x.chars()
}

///////////////////////////////////////////////////////////
// 变更后
pub fn f<'a, 'b>(x: &'a str, y: &'b str) -> impl Iterator<Item = char> + use<'a, 'b> {
    x.chars().chain(y.chars())
}

///////////////////////////////////////////////////////////
// 将会破坏的示例用法。
fn main() {
    let a = String::new();
    let b = String::new();
    let iter = updated_crate::f(&a, &b);
    drop(b); // Error: cannot move out of `b` because it is borrowed
}
```

向 RPIT 添加泛型参数会对结果类型的使用方式施加额外约束。

注意，未指定 `use<>` 语法时存在隐式捕获。在 Rust 2021 及更早的版次中，只有当生命周期参数在语法上出现在 RPIT 类型签名的某个约束中时才会被捕获。从 Rust 2024 开始，所有生命周期参数都会被无条件捕获。这意味着从 Rust 2024 起，默认行为是最大程度兼容的；若你想少捕获一些，就必须显式写明，而这是一项 SemVer 承诺。

关于 RPIT 捕获的更多信息，见[版次指南][rpit-capture-guide]与[参考手册][rpit-reference]。

在 RPIT 中捕获更少的泛型参数属于次版本变更。

> 注意：所有在作用域内的类型泛型参数与常量泛型参数，要么全部隐式捕获（未指定 `+ use<…>`），要么显式捕获（必须列在 `+ use<…>` 中），因此目前不允许更改这两类泛型的捕获情况。

[RPIT]: https://doc.rust-lang.org/reference/types/impl-trait.md#abstract-return-types
[rpit-capture-guide]: https://doc.rust-lang.org/edition-guide/rust-2024/rpit-lifetime-capture.html
[rpit-reference]: https://doc.rust-lang.org/reference/types/impl-trait.md#capturing

### 主版本变更：添加/移除函数参数 {#fn-change-arity}

更改函数的元数（参数个数）属于破坏性变更。

```rust,ignore
// 主版本变更

///////////////////////////////////////////////////////////
// 变更前
pub fn foo() {}

///////////////////////////////////////////////////////////
// 变更后
pub fn foo(x: i32) {}

///////////////////////////////////////////////////////////
// 将会破坏的示例用法。
fn main() {
    updated_crate::foo(); // Error: this function takes 1 argument
}
```

缓解策略：
* 引入一个使用新签名的新函数，并可将旧函数标记为[弃用][deprecated]。
* 引入接收结构体参数的函数，该结构体通过构建者（builder）模式构造。
  这样将来就可以向该结构体添加新字段。

### 可能破坏性变更：引入新的函数类型参数 {#fn-generic-new}

通常，添加没有默认值的类型参数是安全的，但在某些情况下它会是破坏性变更：

```rust,ignore
// 破坏性变更示例

///////////////////////////////////////////////////////////
// 变更前
pub fn foo<T>() {}

///////////////////////////////////////////////////////////
// 变更后
pub fn foo<T, U>() {}

///////////////////////////////////////////////////////////
// 将会破坏的示例用法。
use updated_crate::foo;

fn main() {
    foo::<u8>(); // Error: function takes 2 generic arguments but 1 generic argument was supplied
}
```

不过，这类显式调用足够罕见（而且通常可以用其他方式书写），
因此这种破坏通常是可接受的。你应当权衡相关函数被以显式类型实参调用的可能性有多大。

### 次版本变更：将函数泛化以使用泛型（支持原类型） {#fn-generalize-compatible}

函数参数的类型或其返回值的类型可以被*泛化*为使用泛型（包括引入新的类型参数），
只要它能被实例化为原来的类型即可。例如，下列变更是允许的：

```rust,ignore
// 次版本变更

///////////////////////////////////////////////////////////
// 变更前
pub fn foo(x: u8) -> u8 {
    x
}
pub fn bar<T: Iterator<Item = u8>>(t: T) {}

///////////////////////////////////////////////////////////
// 变更后
use std::ops::Add;
pub fn foo<T: Add>(x: T) -> T {
    x
}
pub fn bar<T: IntoIterator<Item = u8>>(t: T) {}

///////////////////////////////////////////////////////////
// 可安全工作的库使用示例。
use updated_crate::{bar, foo};

fn main() {
    foo(1);
    bar(vec![1, 2, 3].into_iter());
}
```

这是因为所有既有用法都是新签名的实例化。

也许有些出人意料的是，泛化同样适用于 trait 对象，因为每个 trait 都实现了它自身：

```rust,ignore
// 次版本变更

///////////////////////////////////////////////////////////
// 变更前
pub trait Trait {}
pub fn foo(t: &dyn Trait) {}

///////////////////////////////////////////////////////////
// 变更后
pub trait Trait {}
pub fn foo<T: Trait + ?Sized>(t: &T) {}

///////////////////////////////////////////////////////////
// 可安全工作的库使用示例。
use updated_crate::{foo, Trait};

struct Foo;
impl Trait for Foo {}

fn main() {
    let obj = Foo;
    foo(&obj);
}
```

（`?Sized` 的使用至关重要；否则你无法还原出原来的签名。）

以这种方式引入泛型有可能造成类型推断失败。
这种情况通常很罕见，且对某些项目而言是可接受的破坏，因为它可以通过添加类型标注来修复。

```rust,ignore
// 破坏性变更示例

///////////////////////////////////////////////////////////
// 变更前
pub fn foo() -> i32 {
    0
}

///////////////////////////////////////////////////////////
// 变更后
pub fn foo<T: Default>() -> T {
    Default::default()
}

///////////////////////////////////////////////////////////
// 将会破坏的示例用法。
use updated_crate::foo;

fn main() {
    let x = foo(); // Error: type annotations needed
}
```

### 主版本变更：将函数泛化以使用泛型但类型不匹配 {#fn-generalize-mismatch}

如果泛型类型对先前允许的类型施加了约束或改变了它们，
那么更改函数参数或返回类型就属于破坏性变更。例如，下面添加了一个现有代码可能不满足的泛型约束：

```rust,ignore
// 主版本变更

///////////////////////////////////////////////////////////
// 变更前
pub fn foo(x: Vec<u8>) {}

///////////////////////////////////////////////////////////
// 变更后
pub fn foo<T: Copy + IntoIterator<Item = u8>>(x: T) {}

///////////////////////////////////////////////////////////
// 将会破坏的示例用法。
use updated_crate::foo;

fn main() {
    foo(vec![1, 2, 3]); // Error: `Copy` is not implemented for `Vec<u8>`
}
```

### 次版本变更：将 `unsafe` 函数改为安全 {#fn-unsafe-safe}

可以把原本 `unsafe` 的函数改为安全函数而不破坏代码。

但要注意，这可能像下面的示例那样触发 [`unused_unsafe`][unused_unsafe] lint，
从而使指定了 `#![deny(warnings)]` 的本地 crate 无法继续编译。
按照[引入新的 lint](#new-lints) 一节的说明，更新时引入新的警告是被允许的。

反过来做（把安全函数改为 `unsafe`）则属于破坏性变更。

```rust,ignore
// 次版本变更

///////////////////////////////////////////////////////////
// 变更前
pub unsafe fn foo() {}

///////////////////////////////////////////////////////////
// 变更后
pub fn foo() {}

///////////////////////////////////////////////////////////
// 会触发 lint 的库使用示例。
use updated_crate::foo;

unsafe fn bar(f: unsafe fn()) {
    f()
}

fn main() {
    unsafe { foo() }; // 这里会触发 `unused_unsafe` lint
    unsafe { bar(foo) };
}
```

把结构体/枚举上原本 `unsafe` 的关联函数或方法改为安全的，同样属于次版本变更；
但对 trait 上的关联函数则不然（见[对 trait 项签名的任何更改](#trait-item-signature)）。

### 主版本变更：从支持 `no_std` 转为需要 `std` {#attr-no-std-to-std}

如果你的库明确支持 [`no_std`] 环境，那么发布一个需要 `std` 的新版本属于破坏性变更。

```rust,ignore,skip
// 主版本变更

///////////////////////////////////////////////////////////
// 变更前
#![no_std]
pub fn foo() {}

///////////////////////////////////////////////////////////
// 变更后
pub fn foo() {
    std::time::SystemTime::now();
}

///////////////////////////////////////////////////////////
// 将会破坏的示例用法。
// 对于 no_std 目标，这会链接失败，因为它们没有 `std` crate。
#![no_std]
use updated_crate::foo;

fn example() {
    foo();
}
```

缓解策略：
* 避免这种情况的常见惯用做法是提供一个 `std` [Cargo 特性][Cargo feature]，
  用于可选地启用 `std` 支持；当该特性关闭时，该库可用于 `no_std` 环境。

### 主版本变更：向已有枚举、变体或无私有字段的结构体添加 `non_exhaustive` {#attr-adding-non-exhaustive}

把项标记为 [`#[non_exhaustive]`][non_exhaustive] 会改变它们在定义所在 crate 之外的使用方式：

- 非穷尽（non-exhaustive）的结构体与枚举变体不能用[结构体字面量][struct literal]语法构造，
  也包括[函数式更新语法][functional update syntax]。
- 对非穷尽结构体进行模式匹配需要写 `..`，而对枚举的匹配不计入穷尽性判断。
- 不允许用 `as` 把枚举变体转换为其判别值。

无论是否使用 [`#[non_exhaustive]`][non_exhaustive]，带私有字段的结构体都无法用
[结构体字面量][struct literal]语法构造。
因此，为这类结构体添加 [`#[non_exhaustive]`][non_exhaustive] 不属于破坏性变更。

```rust,ignore
// 主版本变更

///////////////////////////////////////////////////////////
// 变更前
pub struct Foo {
    pub bar: usize,
}

pub enum Bar {
    X,
    Y(usize),
    Z { a: usize },
}

pub enum Quux {
    Var,
}

///////////////////////////////////////////////////////////
// 变更后
#[non_exhaustive]
pub struct Foo {
    pub bar: usize,
}

pub enum Bar {
    #[non_exhaustive]
    X,

    #[non_exhaustive]
    Y(usize),

    #[non_exhaustive]
    Z { a: usize },
}

#[non_exhaustive]
pub enum Quux {
    Var,
}

///////////////////////////////////////////////////////////
// 将会破坏的示例用法。
use updated_crate::{Bar, Foo, Quux};

fn main() {
    let foo = Foo { bar: 0 }; // Error: cannot create non-exhaustive struct using struct expression

    let bar_x = Bar::X; // Error: unit variant `X` is private
    let bar_y = Bar::Y(0); // Error: tuple variant `Y` is private
    let bar_z = Bar::Z { a: 0 }; // Error: cannot create non-exhaustive variant using struct expression

    let q = Quux::Var;
    match q {
        Quux::Var => 0,
        // Error: non-exhaustive patterns: `_` not covered
    };
}
```

缓解策略：
* 在首次引入结构体、枚举与枚举变体时就将其标记为
  [`#[non_exhaustive]`][non_exhaustive]，而不是之后再添加
  [`#[non_exhaustive]`][non_exhaustive]。

## 工具与环境兼容性 {#tooling-and-environment-compatibility}
### 可能破坏性变更：更改所需的最低 Rust 版本 {#env-new-rust}

开始使用某个新版 Rust 中的新特性，可能会破坏那些仍在使用旧版 Rust 的项目。
这也包括使用新版 Cargo 的新特性，以及在原本可在 stable 上工作的 crate 中
要求使用仅 nightly 可用的特性。

出于[多种原因][msrv-is-minor]，通常建议把这类变更视为次版本变更而非主版本变更。
升级到较新版本的 Rust 一般相对容易。Rust 还有快速的 6 周发布周期，
有些项目会在一个发布窗口内提供兼容性（例如当前 stable 版本加上此前 N 个版本）。
只是要记住，某些大型项目可能无法快速更新其 Rust 工具链。

缓解策略：
* 通过设置 [`package.rust-version`] 来记录你的包所支持的最低 Rust 版本，
  从而让 Cargo 的依赖解析在需要时尝试[选择你的包的旧版本][select older versions of your package]。
  这样做时请务必考虑[支持预期][support expectations]。
* 使用 [Cargo 特性][Cargo features]让新功能改为按需启用（opt-in）。
* 为旧版本提供较长的支持窗口。
* 如果可能，复制新标准库项的源码，这样你既能继续使用旧版本，又能享用新特性。
* 为较旧的次版本发布提供单独的分支，以便回合（backport）重要的 bug 修复。
* 关注 [`[cfg(version(..))]`][cfg-version] 与
  [`#[cfg(accessible(..))]`][cfg-accessible] 特性，它们为新特性提供了按需启用的机制。
  这些目前尚不稳定，仅在 nightly 通道可用。

[select older versions of your package]: ../specifying-dependencies/03-dependency-resolution/#rust-version
[support expectations]: ../the-manifest-format/02-rust-version/#support-expectations

### 可能破坏性变更：更改平台与环境要求 {#env-change-requirements}

库会对其运行环境作出范围极广的假定，例如宿主平台、操作系统版本、
可用服务、文件系统支持等等。如果你发布的新版本收紧了此前支持的范围，
例如要求更新版本的操作系统，那么这可能是破坏性变更。
这类变更可能难以追踪，因为你未必总能知道某个变更是否会在未被自动测试的环境中造成破坏。

有些项目可能认为这种破坏是可接受的，尤其当破坏对大多数用户不太可能发生、
或项目没有资源支持所有环境时。另一个值得注意的情形是：
当供应商停止支持某些硬件或操作系统时，项目也可能认为随之停止支持是合理的。

缓解策略：
* 明确记录你所支持的平台与环境。
* 在 CI 中于广泛的环境上测试你的代码。

### 次版本变更：引入新的 lint {#new-lints}

对库的某些更改可能导致该库的使用者触发新的 lint。
这通常应被视为兼容的变更。

```rust,ignore,dont-deny
// 次版本变更

///////////////////////////////////////////////////////////
// 变更前
pub fn foo() {}

///////////////////////////////////////////////////////////
// 变更后
#[deprecated]
pub fn foo() {}

///////////////////////////////////////////////////////////
// 可安全工作的库使用示例。

fn main() {
    updated_crate::foo(); // Warning: use of deprecated function
}
```

需要注意的是，如果用户显式地把该警告设为 deny，且被更新的 crate 是直接依赖，
那么严格来说这确实可能导致项目构建失败。
把警告设为 deny 时应当谨慎，并理解随着时间推移可能会引入新的 lint。
不过，库作者在引入新警告时也应保持审慎，并考虑其对用户的潜在影响。

以下 lint 是更新依赖时可能被引入的一些例子：

* [`deprecated`][deprecated-lint] —— 当依赖为你正在使用的项添加 [`#[deprecated]` 属性][deprecated] 时引入。
* [`unused_must_use`] —— 当依赖为某个项添加 [`#[must_use]` 属性][must-use-attr]，而你并未使用其结果时引入。
* [`unused_unsafe`] —— 当依赖*移除*了某个函数的 `unsafe` 限定，且它是某个 unsafe 块中调用的唯一 unsafe 函数时引入。

此外，将 `rustc` 更新到新版本也可能引入新的 lint。

引入新 lint 的传递依赖通常不会导致失败，因为 Cargo 使用 [`--cap-lints`](https://doc.rust-lang.org/rustc/lints/levels.html#capping-lints) 抑制依赖中的所有 lint。

缓解策略：
* 如果你在构建时把警告设为 deny，请理解每次更新依赖时你都可能需要处理新出现的警告。
  若通过 RUSTFLAGS 传入 `-Dwarnings`，也请加上 `-A` 标志来允许那些容易引发问题的 lint，例如 `-Adeprecated`。
* 把弃用（deprecation）放在某个[特性][Cargo features]之后引入。
  例如 `#[cfg_attr(feature = "deprecated", deprecated="use bar instead")]`。
  这样，当你计划在未来某个 SemVer 破坏性变更中移除某项时，可以告知用户：
  在更新之前*先*启用 `deprecated` 特性，以清除对已弃用项的使用。
  这让用户可以自行选择何时响应弃用，而无需立刻处理。
  缺点是，向用户说明他们需要采取这些手动步骤来为主版本更新做准备可能比较困难。

[`unused_must_use`]: https://doc.rust-lang.org/rustc/lints/listing/warn-by-default.html#unused-must-use
[deprecated-lint]: https://doc.rust-lang.org/rustc/lints/listing/warn-by-default.html#deprecated
[must-use-attr]: https://doc.rust-lang.org/reference/attributes/diagnostics.html#the-must_use-attribute
[`unused_unsafe`]: https://doc.rust-lang.org/rustc/lints/listing/warn-by-default.html#unused-unsafe

### Cargo {#cargo}
#### 次版本变更：添加新的 Cargo 特性 {#cargo-feature-add}

添加新的 [Cargo 特性][Cargo features]通常是安全的。如果该特性带来的新变化会造成破坏性变更，
则可能给对向后兼容性要求更严格的项目带来困扰。在这种情况下，
应避免把该特性加入 "default" 列表，并考虑在文档中说明启用该特性的后果。

```toml
# 次版本变更
###########################################################
# 变更前
[features]
# ..空
###########################################################
# 变更后
[features]
std = []
```

#### 主版本变更：移除 Cargo 特性 {#cargo-feature-remove}

移除 [Cargo 特性][Cargo features]通常属于破坏性变更。这会让任何启用了该特性的项目报错。

```toml
# 主版本变更
###########################################################
# 变更前
[features]
logging = []

###########################################################
# 变更后
[dependencies]
# ..已移除 logging
```

缓解策略：
* 清晰地记录你的特性。如果某个特性属于内部或实验性质，请明确标注，
  以便用户了解该特性的状态。
* 把旧特性保留在 `Cargo.toml` 中，但移除其功能。
  在文档中说明该特性已弃用，并在未来的 SemVer 主版本发布中移除它。

#### 主版本变更：若会改变功能或公共项，则从特性列表中移除特性 {#cargo-feature-remove-another}

如果从另一个特性中移除某个特性，而已有用户期望通过该特性获得相应功能，
那么这会破坏他们的使用。

```toml
# 破坏性变更示例
###########################################################
# 变更前
[features]
default = ["std"]
std = []

###########################################################
# 变更后
[features]
default = []  # 若某些包期望 std 被启用，这可能导致它们失败。
std = []
```

#### 可能破坏性变更：移除可选依赖 {#cargo-remove-opt-dep}

移除[可选依赖][opt-dep]可能破坏使用你的库的项目，
因为其他项目可能通过 [Cargo 特性][Cargo features]启用了该依赖。

当存在可选依赖时，cargo 会隐式定义一个同名特性，
以提供启用该依赖以及检查其是否被启用的机制。
可以通过在 `[features]` 表中使用 `dep:` 语法来避免这个问题，它会禁用这个隐式特性。
使用 `dep:` 可以把可选依赖的存在隐藏在语义上更贴切、也更便于安全修改的名字之下。

```toml
# 破坏性变更示例
###########################################################
# 变更前
[dependencies]
curl = { version = "0.4.31", optional = true }

###########################################################
# 变更后
[dependencies]
# ..已移除 curl
```

```toml
# 次版本变更
# 此示例展示如何用可选依赖避免破坏性变更。
###########################################################
# 变更前
[dependencies]
curl = { version = "0.4.31", optional = true }

[features]
networking = ["dep:curl"]

###########################################################
# 变更后
[dependencies]
# 此处用另一个可选依赖替换了一个可选依赖。
hyper = { version = "0.14.27", optional = true }

[features]
networking = ["dep:hyper"]
```

缓解策略：
* 在 `[features]` 表中使用 `dep:` 语法，从一开始就避免暴露可选依赖。
  更多信息见[可选依赖][opt-dep]。
* 清晰地记录你的特性。如果某个可选依赖未被列入已文档化的特性列表，
  那么你可以认为更改这些未文档化的条目是安全的。
* 保留该可选依赖，只是不在你的库中使用它。
* 用一个什么也不做的 [Cargo 特性][Cargo feature]替代该可选依赖，并在文档中说明它已弃用。
* 使用能启用可选依赖的高层特性，并把它们作为启用扩展功能的推荐方式写入文档。
  例如，如果你的库对「网络（networking）」之类的功能提供可选支持，
  可以创建一个通用的特性名 "networking"，由它启用实现「网络」所需的可选依赖，
  然后为 "networking" 特性撰写文档。

[opt-dep]: ../features/#optional-dependencies

#### 次版本变更：更改依赖的特性 {#cargo-change-dep-feature}

只要该特性不引入破坏性变更，更改依赖上启用的特性通常是安全的。

```toml
# 次版本变更
###########################################################
# 变更前
[dependencies]
rand = { version = "0.7.3", features = ["small_rng"] }


###########################################################
# 变更后
[dependencies]
rand = "0.7.3"
```

#### 次版本变更：添加依赖 {#cargo-dep-add}

只要新依赖不会引入导致破坏性变更的新要求，添加新依赖通常是安全的。
例如，在原本可在 stable 上工作的项目中添加一个需要 nightly 的新依赖，属于主版本变更。

```toml
# 次版本变更
###########################################################
# 变更前
[dependencies]
# ..空
###########################################################
# 变更后
[dependencies]
log = "0.4.11"
```

## 应用程序兼容性 {#application-compatibility}
Cargo 项目也可能包含具有自身接口的可执行二进制文件（例如 CLI 接口、
与操作系统层面的交互等）。由于它们是 Cargo 包的一部分，
通常与包共用同一个版本号。你需要决定在对应用程序所作的变更中，
是否以及如何与用户建立 SemVer 契约。应用程序可能出现的破坏性变更与兼容变更多到无法一一列举，
因此建议你以 [SemVer] 规范的精神为指引，决定如何为你的应用程序应用版本管理，
或者至少把你的承诺明确记录下来。

[`cfg` attribute]: https://doc.rust-lang.org/reference/conditional-compilation.md#the-cfg-attribute
[`no_std`]: https://doc.rust-lang.org/reference/names/preludes.html#the-no_std-attribute
[`package.rust-version`]: ../the-manifest-format/02-rust-version/
[`pub use`]: https://doc.rust-lang.org/reference/items/use-declarations.html
[Cargo feature]: ../features/
[Cargo features]: ../features/
[cfg-accessible]: https://github.com/rust-lang/rust/issues/64797
[cfg-version]: https://github.com/rust-lang/rust/issues/64796
[conditional compilation]: https://doc.rust-lang.org/reference/conditional-compilation.md
[Default]: https://doc.rust-lang.org/std/default/trait.Default.html
[deprecated]: https://doc.rust-lang.org/reference/attributes/diagnostics.html#the-deprecated-attribute
[disambiguation syntax]: https://doc.rust-lang.org/reference/expressions/call-expr.html#disambiguating-function-calls
[functional update syntax]: https://doc.rust-lang.org/reference/expressions/struct-expr.html#functional-update-syntax
[inherent implementations]: https://doc.rust-lang.org/reference/items/implementations.html#inherent-implementations
[items]: https://doc.rust-lang.org/reference/items.html
[non_exhaustive]: https://doc.rust-lang.org/reference/attributes/type_system.html#the-non_exhaustive-attribute
[object safe]: https://doc.rust-lang.org/reference/items/traits.html#object-safety
[rust-feature]: https://doc.rust-lang.org/nightly/unstable-book/
[sealed trait]: https://rust-lang.github.io/api-guidelines/future-proofing.html#sealed-traits-protect-against-downstream-implementations-c-sealed
[SemVer]: https://semver.org/
[struct literal]: https://doc.rust-lang.org/reference/expressions/struct-expr.html
[wildcard patterns]: https://doc.rust-lang.org/reference/patterns.html#wildcard-pattern
[unused_unsafe]: https://doc.rust-lang.org/rustc/lints/listing/warn-by-default.html#unused-unsafe
[msrv-is-minor]: https://github.com/rust-lang/api-guidelines/discussions/231
