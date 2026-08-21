+++
title = "第1章 项"
date = 2026-08-18T22:00:00+08:00
weight = 20
type = "docs"
description = "项 — The Rust Style Guide"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Style Guide](https://doc.rust-lang.org/nightly/style-guide/)

> 原文链接: [https://doc.rust-lang.org/nightly/style-guide/items.html](https://doc.rust-lang.org/nightly/style-guide/items.html)

# 项

项由模块顶层所允许的那一类构造组成。
不过，Rust 也允许某些项出现在其他类型的项内部，例如出现在函数中。无论项出现在模块层级还是另一项内部，都适用相同的格式约定。

`extern crate` 语句必须放在文件最前面。它们必须按字母顺序排列。

`use` 语句以及模块*声明*（`mod foo;`，而非 `mod { ... }`）必须位于其他项之前。导入放在模块声明之前。
各自按版本排序，但 `self` 和 `super` 必须排在任何其他名称之前。

不要自动移动带有 `#[macro_use]` 注解的模块声明，因为这可能会改变语义。

## 函数定义 {#function-definitions}

在 Rust 中，人们常常通过搜索 `fn [function-name]` 来查找函数，因此函数定义的格式必须支持这种搜索方式。

正确的顺序与空格如下：

```rust
[pub] [unsafe] [extern ["ABI"]] fn foo(arg1: i32, arg2: i32) -> i32 {
    ...
}
```

避免在签名内部写注释。

若函数签名无法放在一行，则在开括号之后、闭括号之前换行，并将每个参数放在各自的块缩进行上。例如：

```rust
fn foo(
    arg1: i32,
    arg2: i32,
) -> i32 {
    ...
}
```

注意最后一个参数上的尾随逗号。

## 元组与元组结构体 {#tuples-and-tuple-structs}

类型列表的写法与函数参数列表相同。

构造元组或元组结构体的方式与调用函数相同。

### 单行 {#single-line}

```rust
struct Bar(Type1, Type2);

let x = Bar(11, 22);
let y = (11, 22, 33);
```

## 枚举 {#enums}

在声明中，将每个变体放在各自一行，并使用块缩进。

将每个变体相应地格式化为结构体（但不带 `struct` 关键字）、元组结构体，或标识符（标识符不需要特殊格式）：

```rust
enum FooBar {
    First(u32),
    Second,
    Error {
        err: Box<Error>,
        line: u32,
    },
}
```

若结构体变体是[*小型*](../introduction/#small-items)的，则将其格式化为一行。此时，字段列表不要使用尾随逗号，但要在每个花括号两侧加上空格：

```rust
enum FooBar {
    Error { err: Box<Error>, line: u32 },
}
```

在包含多个结构体变体的枚举中，若任一结构体变体写成多行，则所有结构体变体都使用多行格式。不过，这种情况可能表明你应当把该变体的字段提取成独立的结构体。

## 结构体与联合体 {#structs-and-unions}

结构体名称与 `struct` 关键字位于同一行；当开括号仍能落在右边界内时，开括号也放在同一行。所有结构体字段缩进一级，并以尾随逗号结尾。闭括号不缩进，独占一行。

```rust
struct Foo {
    a: A,
    b: B,
}
```

当且仅当字段的类型无法落在右边界内时，才将其下移到单独一行并再缩进一级。

```rust
struct Foo {
    a: A,
    long_name:
        LongType,
}
```

优先使用单元结构体（例如 `struct Foo;`），而不是空结构体（例如 `struct Foo();` 或 `struct Foo {}`，后者仅用于简化代码生成）；但若必须使用空结构体，则保持一行，括号之间不加空格：`struct Foo();` 或 `struct Foo {}`。

无标签联合体声明使用相同的准则。

```rust
union Foo {
    a: A,
    b: B,
    long_name:
        LongType,
}
```

## 元组结构体 {#tuple-structs}

尽可能将整个结构体放在一行。括号内的类型用逗号加空格分隔。单行元组结构体不要使用尾随逗号。括号或分号两侧不要加空格：

```rust
pub struct Foo(String, u8);
```

优先使用单元结构体而非空元组结构体（后者仅用于简化代码生成），例如用 `struct Foo;` 而不是 `struct Foo();`。

若字段不止几个（尤其是元组结构体无法放在一行时），优先使用带有命名字段的正规结构体。

对于多行元组结构体，用块格式排列字段，每行一个字段，并带尾随逗号：

```rust
pub struct Foo(
    String,
    u8,
);
```

## Trait {#traits}

对 trait 项使用块缩进。若没有项，将 trait（包括其 `{}`）格式化为一行。否则，在开括号之后、闭括号之前换行：

```rust
trait Foo {}

pub trait Bar {
    ...
}
```

若 trait 有约束，在冒号之后加空格、之前不加空格，并在每个 `+` 两侧加空格，例如：

```rust
trait Foo: Debug + Bar {}
```

尽可能不要在约束中换行（可考虑使用 `where` 子句）。优先在约束之间换行，而不是拆开任何一个单独的约束。若必须拆开约束，将每个约束（包括第一个）放在各自的块缩进行上，在 `+` 之前换行，并将开括号独占一行：

```rust
pub trait IndexRanges:
    Index<Range<usize>, Output=Self>
    + Index<RangeTo<usize>, Output=Self>
    + Index<RangeFrom<usize>, Output=Self>
    + Index<RangeFull, Output=Self>
{
    ...
}
```

## Impl {#impls}

对 impl 项使用块缩进。若没有项，将 impl（包括其 `{}`）格式化为一行。否则，在开括号之后、闭括号之前换行：

```rust
impl Foo {}

impl Bar for Foo {
    ...
}
```

尽可能避免在签名中换行。若非固有 impl 必须换行，则紧挨着 `for` 之前换行，对具体类型使用块缩进，并将开括号独占一行：

```rust
impl Bar
    for Foo
{
    ...
}
```

## extern crate {#extern-crate}

`extern crate foo;`

关键字两侧加空格，分号两侧不加空格。

## 模块 {#modules}

```rust
mod foo {
}
```

```rust
mod foo;
```

关键字两侧以及开括号之前加空格，分号两侧不加空格。

## `macro_rules!` {#macro-rules}

宏的完整定义使用 `{}`。

```rust
macro_rules! foo {
}
```

## 泛型 {#generics}

优先将泛型子句放在一行。宁可拆开项声明的其他部分，也不要拆开泛型子句。若泛型子句大到必须换行，则优先改用 `where` 子句。

不要在 `<` 之前或之后、也不要在 `>` 之前加空格。仅当 `>` 后面跟的是单词或开花括号（而非开圆括号）时，才在 `>` 之后加空格。每个逗号之后加空格。单行泛型子句不要使用尾随逗号。

```rust
fn foo<T: Display, U: Debug>(x: Vec<T>, y: Vec<U>) ...

impl<T: Display, U: Debug> SomeType<T, U> { ...
```

若泛型子句必须跨多行格式化，将每个参数放在各自的块缩进行上，在开 `<` 之后、闭 `>` 之前换行，并使用尾随逗号。

```rust
fn foo<
    T: Display,
    U: Debug,
>(x: Vec<T>, y: Vec<U>) ...
```

若在泛型类型中绑定关联类型，在 `=` 两侧加空格：

```rust
<T: Example<Item = u32>>
```

优先为泛型参数使用单字母名称。

## `where` 子句 {#where-clauses}

这些规则适用于任何项上的 `where` 子句。

若紧跟在任意种类的闭括号之后，将关键字 `where` 写在同一行，并在其前面加空格。

否则，将 `where` 放在新的一行，缩进级别相同。将 `where` 子句的每个组成部分放在各自一行，并使用块缩进。使用尾随逗号，除非该子句以分号结束。若 `where` 子句后面跟的是代码块（或赋值），则将该代码块另起一行。例如：

```rust
fn function<T, U>(args)
where
    T: Bound,
    U: AnotherBound,
{
    body
}

fn foo<T>(
    args
) -> ReturnType
where
    T: Bound,
{
    body
}

fn foo<T, U>(
    args,
) where
    T: Bound,
    U: AnotherBound,
{
    body
}

fn foo<T, U>(
    args
) -> ReturnType
where
    T: Bound,
    U: AnotherBound;  // 注意：没有尾随逗号。

// 注意：`type` 别名上的 where 子句不会被强制执行，因此不应
// 使用。
type Foo<T>
where
    T: Bound
= Bar<T>;
```

若 `where` 子句非常短，优先在类型参数上使用内联约束。

若 `where` 子句的某一组成部分放不下且包含 `+`，则在每个 `+` 之前换行，并对续行使用块缩进。将每个约束放在各自一行。例如：

```rust
impl<T: ?Sized, Idx> IndexRanges<Idx> for T
where
    T: Index<Range<Idx>, Output = Self::Output>
        + Index<RangeTo<Idx>, Output = Self::Output>
        + Index<RangeFrom<Idx>, Output = Self::Output>
        + Index<RangeInclusive<Idx>, Output = Self::Output>
        + Index<RangeToInclusive<Idx>, Output = Self::Output>
        + Index<RangeFull>,
```

## 类型别名 {#type-aliases}

当类型别名能放得下时保持一行。必要时换行，则在 `=` 之前断开，并对右侧使用块缩进：

```rust
pub type Foo = Bar<T>;

// 若必须多行
type VeryLongType<T, U: SomeBound>
    = AnEvenLongerType<T, U, Foo<T>>;
```

当类型之后有尾随的 `where` 子句、且类型之前没有 `where` 子句时，在 `=` 之前换行并缩进。然后在 `where` 关键字之前换行，并按常规格式化这些子句，例如：

```rust
// 仅有尾随 where 子句
type VeryLongType<T, U>
    = AnEvenLongerType<T, U, Foo<T>>
where
    T: U::AnAssociatedType,
    U: SomeBound;
```

当类型之前有 `where` 子句时，按常规格式化，并在最后一个子句之后换行。不要在 `=` 之前缩进，以使其在视觉上区别于前面已缩进的子句。若类型之后另外还有 `where` 子句，则在 `where` 关键字之前换行，并按常规格式化这些子句。

```rust
// 仅有前置 where 子句。
type WithPrecedingWC<T, U>
where
    T: U::AnAssociatedType,
    U: SomeBound,
= AnEvenLongerType<T, U, Foo<T>>;

// 或者同时有前置和尾随 where 子句。
type WithPrecedingWC<T, U>
where
    T: U::AnAssociatedType,
    U: SomeBound,
= AnEvenLongerType<T, U, Foo<T>>
where
    T: U::AnAssociatedType2,
    U: SomeBound2;
```

## 关联类型 {#associated-types}

关联类型的格式与类型别名相同。当关联类型有约束时，在冒号之后加空格、之前不加空格：

```rust
pub type Foo: Bar;
```

## extern 项 {#extern-items}

编写 extern 项（例如 `extern "C" fn`）时，始终指定 ABI。
例如，写 `extern "C" fn foo ...` 或 `unsafe extern "C" { ...}`，
避免写 `extern fn foo ...` 和 `unsafe extern { ... }`。

## 导入（`use` 语句） {#imports-use-statements}

尽可能将导入格式化为一行。花括号两侧不要加空格。

```rust
use a::b::c;
use a::b::d::*;
use a::b::{foo, bar, baz};
```

### 大型列表导入 {#large-list-imports}

优先使用多个导入，而不是一个多行导入。不过，工具默认不应拆分导入。

若导入确实需要多行（或因单个名称列表无法落在最大宽度内，或因下文嵌套导入的规则），则在开括号之后、闭括号之前换行，使用尾随逗号，并对名称使用块缩进。

```rust
// 首选
foo::{long, list, of, imports};
foo::{more, imports};

// 必要时
foo::{
    long, list, of, imports, more,
    imports,  // 注意尾随逗号
};
```

### 导入的排序 {#ordering-of-imports}

导入的一个*组*是位于同一行或连续行上的一组导入。一个或多个空行或其他项（例如函数）将导入组隔开。

在同一导入组内，导入必须按版本排序。导入组不得合并或重新排序。

例如，输入：

```rust
use d;
use c;

use b;
use a;
```

输出：

```rust
use c;
use d;

use a;
use b;
```

由于 `macro_use`，属性也必须开启一个新组并阻止重新排序。

### 列表导入的排序 {#ordering-list-import}

列表导入中的名称必须按版本排序，但有以下例外：
- 若存在 `self` 和 `super`，它们始终排在最前，并且
- 若存在组和 glob 导入，它们始终排在最后。

此规则递归适用。例如，`a::*` 排在 `b::a` 之前，但 `a::b` 排在 `a::*` 之前。例如：`use foo::bar::{a, b::c, b::d, b::d::{x, y, z},
b::{self, r, s}};`。

### 规范化 {#normalisation}

工具必须递归地进行以下规范化：

- `use a::self;` -> `use a;`
- `use a::{};` -> （无）
- `use a::{b};` -> `use a::b;`

除此之外，工具不得合并或拆分导入列表，也不得调整 glob 导入（除非有显式选项）。

### 嵌套导入 {#nested-imports}

若列表导入中存在任何嵌套导入，则使用多行形式，即使该导入能放在一行。每个嵌套导入必须独占一行，但非嵌套导入必须尽量分组到尽可能少的行上。

例如：

```rust
use a::b::{
    x, y, z,
    u::{...},
    w::{...},
};
```

### 合并/拆分导入 {#mergingun-merging-imports}

例如：

```rust
// 未合并
use a::b;
use a::c::d;

// 已合并
use a::{b, c::d};
```

工具默认不得合并或拆分导入。它们可以将合并或拆分作为选项提供。
