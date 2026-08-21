+++
title = "06-术语表"
date = 2026-08-18T08:45:00+08:00
weight = 121
type = "docs"
description = "术语表 — The Rust Reference"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Reference](https://doc.rust-lang.org/reference/)

> 原文链接: [https://doc.rust-lang.org/reference/glossary.html](https://doc.rust-lang.org/reference/glossary.html)

# 术语表

r[glossary.ast]
### 抽象语法树（Abstract syntax tree）

“抽象语法树”（abstract syntax tree，简称 AST）是编译器在编译程序时所用的程序结构的中间表示。

### 对齐（Alignment）

值的对齐指定了值更倾向于从哪些地址开始。始终是 2 的幂。对值的引用必须已对齐。[更多][alignment]。

r[glossary.abi]
### 应用二进制接口（ABI）

*应用二进制接口*（ABI）定义了编译后的代码如何与其他编译后的代码交互。对于 [`extern` 块][`extern` blocks] 与 [`extern fn`]，*ABI 字符串*影响：

- **调用约定**：函数实参如何传递、值如何返回（例如在寄存器中或在栈上），以及谁负责清理栈。
- **展开**：是否允许栈展开。例如，`"C-unwind"` ABI 允许跨 FFI 边界展开，而 `"C"` ABI 不允许。

### 元数（Arity）

元数指函数或运算符所取实参的个数。例如，`f(2, 3)` 与 `g(4, 6)` 的元数为 2，而 `h(8, 2, 6)` 的元数为 3。`!` 运算符的元数为 1。

### 数组（Array）

数组有时也称为固定大小数组或内联数组，是描述元素集合的值，每个元素由程序可在运行时计算的索引选出。它占据一块连续的内存区域。

### 关联项（Associated item）

关联项是与另一项相关联的项。关联项在[实现][implementations]中定义，在 [trait][traits] 中声明。只有函数、常量与类型别名可以是关联的。与[自由项][free item]相对。

### Blanket 实现（Blanket implementation）

任何类型以[未覆盖](#uncovered-type)形式出现的实现。`impl<T> Foo for T`、`impl<T> Bar<T> for T`、`impl<T> Bar<Vec<T>> for T` 以及 `impl<T> Bar<T> for Vec<T>` 被视为 blanket impl。然而，`impl<T> Bar<Vec<T>> for Vec<T>` 不是 blanket impl，因为出现在此 `impl` 中的所有 `T` 实例都被 `Vec` 覆盖。

### 约束（Bound）

约束是对类型或 trait 的限制。例如，若对函数所取的实参施加约束，则传入该函数的类型必须遵守该限制。

### 组合子（Combinator）

组合子是高阶函数，仅应用函数与先前定义的组合子，以从其实参得到结果。它们可用于以模块化方式管理控制流。

### Crate

Crate 是编译与链接的单位。存在不同类型的 [crate][types of crates]，如库或可执行文件。Crate 可以链接并引用其他库 crate，称为外部 crate。Crate 具有自包含的[模块][modules]树，从称为 crate 根的未命名根模块开始。可通过在 crate 根中将[项][Items]标记为公开（包括经由公开模块的[路径][paths]）使其对其他 crate 可见。[更多][crate]。

### 分派（Dispatch）

分派是在涉及多态时确定实际运行哪一具体版本代码的机制。分派的两种主要形式是静态分派与动态分派。Rust 通过使用 [trait 对象][type.trait-object] 支持动态分派。

### 动态大小类型（Dynamically sized type）

动态大小类型（DST）是没有静态已知大小或对齐的类型。

### 实体（Entity）

[*实体*][*entity*] 是可以在源程序中以某种方式被引用的语言构造，通常经由[路径][paths]。实体包括[类型][types]、[项][items]、[泛型参数][generic parameters]、[变量绑定][variable bindings]、[循环标签][loop labels]、[生命周期][lifetimes]、[字段][fields]、[属性][attributes]以及 [lint][lints]。

### 表达式（Expression）

表达式是值、常量、变量、运算符与函数的组合，求值为单个值，可带或不带副作用。

例如，`2 + (3 * 4)` 是返回值 14 的表达式。

### 自由项（Free item）

不是[实现][implementation]成员的[项][item]，例如*自由函数*或*自由常量*。与[关联项][associated item]相对。

### 基础 trait（Fundamental traits）

基础 trait 是为其已有类型添加 impl 会构成破坏性变更的 trait。`Fn` trait 与 `Sized` 是基础的。

### 基础类型构造器（Fundamental type constructors）

基础类型构造器是在其上实现 [blanket 实现](#blanket-implementation) 会构成破坏性变更的类型。`&`、`&mut`、`Box` 与 `Pin` 是基础的。

每当类型 `T` 被视为[局部](#local-type)时，`&T`、`&mut T`、`Box<T>` 与 `Pin<T>` 也被视为局部。基础类型构造器不能[覆盖](#uncovered-type)其他类型。每当使用术语“被覆盖类型”时，`&T`、`&mut T`、`Box<T>` 与 `Pin<T>` 中的 `T` 不被视为被覆盖。

### 有居民（Inhabited）

若类型具有构造函数因而可被实例化，则该类型是有居民的。有居民类型在可以存在该类型的值这一意义上并非“空”。与[无居民](#uninhabited)相对。

### 固有实现（Inherent implementation）

应用于名义类型、而非 trait-类型对的[实现][implementation]。[更多][inherent implementation]。

### 固有方法（Inherent method）

在[固有实现][inherent implementation]中定义、而非在 trait 实现中定义的[方法][method]。

### 已初始化（Initialized）

若变量已被赋予一个值且此后未被从中移出，则该变量已初始化。所有其他内存位置都被假定为未初始化。只有不安全的 Rust 才能在未初始化的情况下创建内存位置。

### 局部 trait（Local trait）

在当前 crate 中定义的 `trait`。Trait 定义是否局部与所应用的类型实参无关。给定 `trait Foo<T, U>`，无论为 `T` 与 `U` 替换何种类型，`Foo` 始终是局部的。

### 局部类型（Local type）

在当前 crate 中定义的 `struct`、`enum` 或 `union`。这不受所应用类型实参的影响。`struct Foo` 被视为局部，但 `Vec<Foo>` 不是。`LocalType<ForeignType>` 是局部的。类型别名不影响局部性。

### 模块（Module）

模块是容纳零个或多个[项][items]的容器。模块组织成一棵树，从根部称为 crate 根或根模块的未命名模块开始。可使用[路径][Paths]引用其他模块中的项，这可能受到[可见性规则][visibility rules]的限制。[更多][modules]

### 名称（Name）

[*名称*][*name*] 是引用[*实体*](#entity)的[标识符][identifier]或[生命周期或循环标签][lifetime or loop label]。*名称绑定*是实体声明引入与该实体相关联的标识符或标签时发生的事。[路径][Paths]、标识符与标签用于引用实体。

### 名称解析（Name resolution）

[*名称解析*][*Name resolution*] 是将[路径][paths]、[标识符][identifiers]与[标签][labels]绑定到[*实体*](#entity)声明的编译期过程。

### 命名空间（Namespace）

*命名空间* 是根据名称所引用[*实体*](#entity)的种类，对已声明[名称](#name)的逻辑分组。命名空间允许一个命名空间中出现的名称不与另一命名空间中的同名冲突。

在命名空间内，名称按层次组织，层次的每一级都有其自己的命名实体集合。

### 名义类型（Nominal types）

可以直接由路径引用的类型。具体而言是[枚举][enums]、[结构体][structs]、[联合体][unions]以及 [trait 对象类型][trait object types]。

### Dyn 兼容 trait（Dyn-compatible traits）

可用于 [trait 对象类型][trait object types]（`dyn Trait`）的 [Trait][Traits]。只有遵循特定[规则][dyn compatibility]的 trait 才是 *dyn 兼容*的。

这些以前称为*对象安全* trait。

### 路径（Path）

[*路径*][*path*] 是由一个或多个路径段组成的序列，用于在当前作用域或[命名空间](#namespace)层次的其他层级中引用[*实体*](#entity)。

### Prelude

Prelude，或称 The Rust Prelude，是一小部分项的集合——主要是 trait——它们被导入每个 crate 的每个模块。Prelude 中的 trait 无处不在。

### 作用域（Scope）

[*作用域*][*scope*] 是源文本中可用该名称引用某一命名[*实体*](#entity)的区域。

### 被匹配表达式（Scrutinee）

被匹配表达式是在 `match` 表达式及类似模式匹配构造中被匹配的表达式。例如，在 `match x { A => 1, B => 2 }` 中，表达式 `x` 是被匹配表达式。

### 大小（Size）

值的大小有两个定义。

第一个是必须分配多少内存来存储该值。

第二个是具有该元素类型的数组中相继元素之间以字节计的偏移。

它是对齐的倍数，包括零。大小可能因编译器版本（随着新优化的出现）与目标平台（类似于 `usize` 因平台而异）而变化。

[更多][alignment]。

### 切片（Slice）

切片是对连续序列的动态大小视图，写作 `[T]`。

它常以其借用形式出现，可变或共享均可。共享切片类型是 `&[T]`，而可变切片类型是 `&mut [T]`，其中 `T` 表示元素类型。

### 语句（Statement）

语句是命令计算机执行某一动作的编程语言中最小的独立元素。

### 字符串字面量（String literal）

字符串字面量是直接存储在最终二进制文件中的字符串，因此在 `'static` 持续时间内有效。

其类型是 `'static` 持续时间的借用字符串切片，`&'static str`。

### 字符串切片（String slice）

字符串切片是 Rust 中最原始的字符串类型，写作 `str`。它常以其借用形式出现，可变或共享均可。共享字符串切片类型是 `&str`，而可变字符串切片类型是 `&mut str`。

字符串切片始终是有效的 UTF-8。

### Trait

Trait 是用于描述类型必须提供哪些功能的语言项。它允许类型就其行为作出某些承诺。

泛型函数与泛型结构体可以使用 trait 来约束它们所接受的类型。

### Turbofish

表达式中带有泛型参数的路径必须在开括号前加上 `::`。与泛型的尖括号相结合，这看起来像一条鱼 `::<>`。因此，此语法通俗地称为 turbofish 语法。

示例：

```rust
let ok_num = Ok::<_, ()>(5);
let vec = [1, 2, 3].iter().map(|n| n * 2).collect::<Vec<_>>();
```

此 `::` 前缀是必需的，以便在逗号分隔列表中有多次比较时消除泛型路径的歧义。关于若不加此前缀会有歧义的例子，见 [turbofish 的堡垒][turbofish test]。

### 未覆盖类型（Uncovered type）

不以另一类型的实参形式出现的类型。例如，`T` 是未覆盖的，但 `Vec<T>` 中的 `T` 是被覆盖的。这仅与类型实参相关。

### 未定义行为（Undefined behavior）

未被指定的编译期或运行时行为。这可能导致（但不限于）：进程终止或损坏；不当、不正确或非预期的计算；或平台特定的结果。[更多][undefined-behavior]。

r[glossary.uninhabited]
### 无居民（Uninhabited）

若类型没有构造函数因而永远无法被实例化，则该类型是无居民的。无居民类型在不存在该类型的值这一意义上是“空”的。无居民类型的典型例子是[永不类型][never type] `!`，或没有变体的枚举 `enum Never { }`。与[有居民](#inhabited)相对。

> **注意**
> 无居民类型不一定是[零大小][zero sized]。例如，`enum Never { }` 是无居民且零大小的，但 `(u8, Never)` 是无居民且非零大小的。

r[glossary.zst]
### 零大小类型（ZST）

若类型的大小为 0，则它是零大小的（ZST）。此类类型最多有一个可能的值。示例包括：

- [单元类型][unit type]（见 [layout.tuple.unit]）。
- [函数项][Function items]（见 [type.fn-item.intro]）。
- [类元组结构体][tuple-like structs]的构造函数（见 [type.fn-item.intro]）。
- [类元组枚举变体][tuple-like enum variants]的构造函数（见 [type.fn-item.intro]）。
- 没有字段或所有字段都为零大小的 `repr(Rust)` [结构体][structs]（见 [layout.repr.rust.struct-zst]）。
- 没有字段或所有字段都为零大小的 `repr(C)` [结构体][structs]（见 [layout.repr.c.struct.size-field-offset]）。
- 没有字段或所有字段都为零大小的 `repr(transparent)` [结构体][structs]（见 [layout.repr.transparent.layout-abi]）。
- 没有变体的 `repr(Rust)` [枚举][enums]（未指定[原语表示][primitive representation]）（见 [layout.repr.rust.enum-empty-zst]）。
- 具有单个[字段结构体式变体][field-struct-like variant]、单个[单元结构体式变体][unit-struct-like variant]或单个[元组结构体式变体][tuple-struct-like variant]，且该结构体式部分没有字段或所有字段都为零大小的 `repr(Rust)` [枚举][enums]（未指定[原语表示][primitive representation]）（见 [layout.repr.rust.enum-struct-like-zst]）。
- 零大小类型的[数组][Arrays]（见 [layout.array]）。
- 长度为零的[数组][Arrays]（见 [layout.array]）。
- 零大小类型的[联合体][Unions]（见 [items.union.common-storage]）。

```rust
## use core::mem::{size_of, size_of_val};
fn f() {}
struct S(u8);
enum E { V(u8) }
struct UnitLike;
struct NoFields {}
struct OnlyZST {
    f1: (),
    f2: [(); 10],
    f3: [u8; 0],
}
#[repr(C)]
struct C1 {}
#[repr(C)]
struct C2 {
    f1: (),
    f2: [(); 10],
    f3: [u8; 0],
    f4: C1,
}
#[repr(transparent)]
struct T1 {}
#[repr(transparent)]
struct T2 {
    f1: (),
    f2: [(); 10],
    f3: [u8; 0],
}
union U {
    f1: (),
    f2: [(); 10],
    f3: [u8; 0],
}
## /// 具有单个字段结构体式变体、且所有字段
## /// 都是 ZST 的枚举。
enum E2 {
    V1 { f1: (), f2: [(); 10] },
}
## /// 具有单个无字段的字段结构体式变体的枚举。
enum E3 {
    V1 {},
}
## /// 具有单个单元结构体式变体的枚举。
enum E4 {
    V1,
}
## /// 具有单个元组结构体式变体、且所有字段
## /// 都是 ZST 的枚举。
enum E5 {
    V1 ((), [(); 10]),
}
## /// 具有单个无字段的元组结构体式变体的枚举。
enum E6 {
    V1 (),
}
## /// 没有变体的枚举。
enum E7 {}

assert_eq!(0, size_of::<()>());
assert_eq!(0, size_of_val(&f));
assert_eq!(0, size_of_val(&S));
assert_eq!(0, size_of_val(&E::V));
assert_eq!(0, size_of::<UnitLike>());
assert_eq!(0, size_of::<NoFields>());
assert_eq!(0, size_of::<OnlyZST>());
assert_eq!(0, size_of::<C1>());
assert_eq!(0, size_of::<C2>());
assert_eq!(0, size_of::<T1>());
assert_eq!(0, size_of::<T2>());
assert_eq!(0, size_of::<[(); 10]>());
assert_eq!(0, size_of::<[u8; 0]>());
assert_eq!(0, size_of::<U>());
assert_eq!(0, size_of::<E2>());
assert_eq!(0, size_of::<E3>());
assert_eq!(0, size_of::<E4>());
assert_eq!(0, size_of::<E5>());
assert_eq!(0, size_of::<E6>());
assert_eq!(0, size_of::<E7>());
```

[`extern` blocks]: items.extern
[`extern fn`]: items.fn.extern
[alignment]: type-layout.md#size-and-alignment
[arrays]: type.array
[associated item]: #associated-item
[attributes]: attributes.md
[*entity*]: names.md
[crate]: crates-and-source-files.md
[dyn compatibility]: items/traits.md#dyn-compatibility
[enums]: items/enumerations.md
[field-struct-like variant]: EnumVariantStruct
[fields]: expressions/field-expr.md
[free item]: #free-item
[function items]: type.fn-item
[generic parameters]: items/generics.md
[identifier]: identifiers.md
[identifiers]: identifiers.md
[implementation]: items/implementations.md
[implementations]: items/implementations.md
[inherent implementation]: items/implementations.md#inherent-implementations
[item]: items.md
[items]: items.md
[labels]: tokens.md#lifetimes-and-loop-labels
[lifetime or loop label]: tokens.md#lifetimes-and-loop-labels
[lifetimes]: tokens.md#lifetimes-and-loop-labels
[lints]: attributes/diagnostics.md#lint-check-attributes
[loop labels]: tokens.md#lifetimes-and-loop-labels
[method]: items/associated-items.md#methods
[modules]: items/modules.md
[*Name resolution*]: names/name-resolution.md
[*name*]: names.md
[*namespace*]: names/namespaces.md
[never type]: types/never.md
[*path*]: paths.md
[Paths]: paths.md
[primitive representation]: layout.repr.primitive
[*scope*]: names/scopes.md
[structs]: items/structs.md
[tuple-like enum variants]: items.enum.constructor-namespace
[tuple-like structs]: items.struct.tuple
[tuple-struct-like variant]: EnumVariantTuple
[trait object types]: types/trait-object.md
[traits]: items/traits.md
[turbofish test]: https://github.com/rust-lang/rust/blob/1.58.0/src/test/ui/parser/bastion-of-the-turbofish.rs
[types of crates]: linkage.md
[types]: types.md
[undefined-behavior]: behavior-considered-undefined.md
[unions]: items/unions.md
[unit type]: type.tuple.unit
[unit-struct-like variant]: EnumVariant
[variable bindings]: patterns.md
[visibility rules]: visibility-and-privacy.md
[zero sized]: glossary.zst
