+++
title = "03-类型布局"
date = 2026-08-18T08:45:00+08:00
weight = 86
type = "docs"
description = "类型布局 — The Rust Reference"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Reference](https://doc.rust-lang.org/reference/)

> 原文链接: [https://doc.rust-lang.org/reference/type-layout.html](https://doc.rust-lang.org/reference/type-layout.html)

r[layout]
# 类型布局

r[layout.intro]
类型的布局是其大小、对齐，以及其字段的相对偏移。对于枚举，判别式如何布局和解释也是类型布局的一部分。

r[layout.guarantees]
类型布局可以随每次编译而改变。我们不会试图精确记录实际做了什么，而只记录今天所保证的内容。

注意，即使布局相同的类型，在跨越函数边界传递时仍可能不同。关于类型的函数调用 ABI 兼容性，参见[此处][fn-abi-compatibility]。

r[layout.properties]
## 大小与对齐

所有值都有对齐和大小。

r[layout.properties.align]
值的 *对齐* 指定哪些地址可以合法地存储该值。对齐为 `n` 的值必须只存储在是 n 的倍数的地址上。例如，对齐为 2 的值必须存储在偶数地址上，而对齐为 1 的值可以存储在任何地址。对齐以字节度量，必须至少为 1，并且总是 2 的幂。值的对齐可以用 [`align_of_val`] 函数检查。

r[layout.properties.size]
值的 *大小* 是具有该元素类型的数组中相继元素之间以字节计的偏移，包括对齐填充。值的大小总是其对齐的倍数。注意有些类型是[零大小][zero-sized]的；0 被视为任何对齐的倍数（例如，在某些平台上，类型 `[u16; 0]` 的大小为 0、对齐为 2）。值的大小可以用 [`size_of_val`] 函数检查。

r[layout.properties.sized]
所有值都具有相同大小和对齐、且二者在编译时已知的类型实现 [`Sized`] trait，并且可以用 [`size_of`] 和 [`align_of`] 函数检查。不是 [`Sized`] 的类型称为[动态大小类型][dynamically sized types]。由于 `Sized` 类型的所有值共享相同的大小和对齐，我们将这些共享值分别称为该类型的大小和该类型的对齐。

r[layout.primitive]
## 原始数据布局

r[layout.primitive.size]
下表给出了大多数原始类型的大小。

| 类型              | `size_of::<Type>()`|
|--                 |--                  |
| `bool`            | 1                  |
| `u8` / `i8`       | 1                  |
| `u16` / `i16`     | 2                  |
| `u32` / `i32`     | 4                  |
| `u64` / `i64`     | 8                  |
| `u128` / `i128`   | 16                 |
| `usize` / `isize` | 见下文             |
| `f32`             | 4                  |
| `f64`             | 8                  |
| `char`            | 4                  |

r[layout.primitive.size-minimum]
`usize` 和 `isize` 的大小足以包含目标平台上的每个地址。例如，在 32 位目标上为 4 字节，在 64 位目标上为 8 字节。

r[layout.primitive.size-align]
`usize` 和 `isize` 具有相同的大小和对齐。

r[layout.primitive.platform-specific-alignment]
原始类型的对齐是平台相关的。在大多数情况下，它们的对齐等于其大小，但也可能更小。特别是，`i128` 和 `u128` 尽管大小为 16，却常常对齐到 4 或 8 字节；并且在许多 32 位平台上，`i64`、`u64` 和 `f64` 只对齐到 4 字节，而不是 8。

r[layout.primitive.integer-alignment]
保证相同标称大小的定宽有符号和无符号整数变体具有相同的对齐——也就是说，对于给定大小 `N`，`align_of::<uN>() == align_of::<iN>()`。

r[layout.pointer]
## 指针与引用的布局

r[layout.pointer.intro]
指针和引用具有相同的布局。指针或引用的可变性不改变布局。

r[layout.pointer.thin]
指向有大小类型的指针与 `usize` 具有相同的大小和对齐。

r[layout.pointer.unsized]
指向不定大小类型的指针是有大小的。指向不定大小类型的指针的大小和对齐各自保证大于或等于指向有大小类型的指针的大小和对齐。

> **注意**
> 尽管你不应依赖这一点，目前所有指向 <abbr title="Dynamically Sized Types">DST</abbr> 的指针都是 `usize` 大小的两倍，并且具有相同的对齐。

r[layout.array]
## 数组布局

`[T; N]` 类型的数组大小为 `size_of::<T>() * N`，对齐与 `T` 相同。数组的布局使得从 0 开始计数的第 `n` 个元素相对数组起始的偏移为 `n * size_of::<T>()` 字节。

r[layout.slice]
## 切片布局

切片与它们所切出的那一段数组具有相同的布局。

> **注意**
> 这说的是原始 `[T]` 类型，而不是指向切片的指针（`&[T]`、`Box<[T]>` 等）。

r[layout.str]
## `str` 布局

字符串切片是字符的 UTF-8 表示，与 `[u8]` 类型的切片具有相同布局。引用 `&str` 与引用 `&[u8]` 具有相同布局。

r[layout.tuple]
## 元组布局

r[layout.tuple.def]
元组按照 [`Rust` 表示][`Rust`]布局。

r[layout.tuple.unit]
例外是单元元组（`()`），它作为[零大小类型][zero-sized type]保证大小为 0、对齐为 1。

r[layout.trait-object]
## Trait 对象布局

Trait 对象与该 trait 对象所对应的值具有相同的布局。

> **注意**
> 这说的是原始 trait 对象类型，而不是指向 trait 对象的指针（`&dyn Trait`、`Box<dyn Trait>` 等）。

r[layout.closure]
## 闭包布局

闭包没有布局保证。

r[layout.repr]
## 表示

r[layout.repr.intro]
所有用户定义的复合类型（`struct`、`enum` 和 `union`）都有一种 *表示*，指定该类型的布局。

r[layout.repr.kinds]
一个类型可能的表示有：

- [`Rust`]（默认）
- [`C`]
- [原始表示][primitive representations]
- [`transparent`]

r[layout.repr.attribute]
可以通过对该类型应用 `repr` 属性来改变其表示。下面的例子展示了一个具有 `C` 表示的结构体。

```rust
#[repr(C)]
struct ThreeInts {
    first: i16,
    second: i8,
    third: i32
}
```

r[layout.repr.align-packed]
对齐可以分别用 `align` 和 `packed` 修饰符提高或降低。它们会改变属性中指定的表示。若未指定表示，则改变默认表示。

```rust
// 默认表示，对齐降低到 2。
#[repr(packed(2))]
struct PackedStruct {
    first: i16,
    second: i8,
    third: i32
}

// C 表示，对齐提高到 8
#[repr(C, align(8))]
struct AlignedStruct {
    first: i16,
    second: i8,
    third: i32
}
```

> **注意**
> 由于表示是项上的属性，表示不依赖于泛型参数。任何两个同名类型都具有相同的表示。例如，`Foo<Bar>` 和 `Foo<Baz>` 具有相同的表示。

r[layout.repr.inter-field]
类型的表示可以改变字段之间的填充，但不会改变字段自身的布局。例如，具有 `C` 表示、其中包含具有 `Rust` 表示的结构体 `Inner` 的结构体，不会改变 `Inner` 的布局。

<a id="the-default-representation"></a>
r[layout.repr.rust]
### `Rust` 表示

r[layout.repr.rust.intro]
`Rust` 表示是没有 `repr` 属性的名义类型的默认表示。通过 `repr` 属性显式使用此表示，保证与完全省略该属性相同。

r[layout.repr.rust.layout]
此表示所做的数据布局保证仅限于可靠性所要求的那些。它们是：

 1. 字段的偏移可被该字段的对齐整除。
 2. 类型的对齐至少是其字段的最大对齐。

r[layout.repr.rust.layout.struct]
对于[结构体][structs]，进一步保证字段互不重叠。也就是说，可以将字段排序，使得任何字段的偏移加大小小于或等于该排序中下一个字段的偏移。该排序不必与类型声明中指定字段的顺序相同。

请注意，这一保证并不意味着字段具有不同的地址：[零大小类型][zero-sized types]可能与同一结构体中的其他字段具有相同的地址。

r[layout.repr.rust.struct-zst]
对于没有字段或所有字段都是[零大小][zero sized]的[结构体][structs]，进一步保证这些结构体自身是[零大小][zero sized]的。

r[layout.repr.rust.enum-empty-zst]
（未指定[原始表示][primitive representation]的）没有变体的[枚举][Enums]是[零大小][zero sized]的。

> **注意**
> 此类枚举是[无居住值][uninhabited]的。

r[layout.repr.rust.enum-struct-like-zst]
对于（未指定[原始表示][primitive representation]的）只有一个[类字段结构体变体][field-struct-like variant]、一个[类单元结构体变体][unit-struct-like variant]或一个[类元组结构体变体][tuple-struct-like variant]，且该类似结构体的东西没有字段或所有字段都是[零大小][zero sized]的[枚举][enums]，这些枚举自身是[零大小][zero sized]的。

r[layout.repr.rust.unspecified]
此表示没有做出其他数据布局保证。

r[layout.repr.c]
### `C` 表示

r[layout.repr.c.intro]
`C` 表示设计用于双重目的。一个目的是创建可与 C 语言互操作的类型。第二个目的是创建你可以可靠地对其执行依赖数据布局的操作（例如将值重新解释为不同的类型）的类型。

由于这一双重目的，有可能创建对与 C 编程语言交互并无用处的类型。

r[layout.repr.c.constraint]
此表示可以应用于结构体、联合体和枚举。例外是[零变体枚举][zero-variant enums]，对其使用 `C` 表示是错误。

r[layout.repr.c.struct]
#### `#[repr(C)]` 结构体

r[layout.repr.c.struct.align]
结构体的对齐是其中对齐最大的字段的对齐，若没有字段则为 1。

r[layout.repr.c.struct.size-field-offset]
字段的大小和偏移由以下算法确定。

从当前偏移 0 字节开始。

对于结构体中按声明顺序的每个字段，首先确定该字段的大小和对齐。若当前偏移不是该字段对齐的倍数，则向当前偏移添加填充字节，直到它成为该字段对齐的倍数。该字段的偏移即为此时的当前偏移。然后将当前偏移增加该字段的大小。

最后，结构体的大小是将当前偏移向上舍入到结构体对齐的最近倍数。

以下是该算法：

```rust
## /// 结构体的一个字段。
## #[derive(Debug)]
struct Field {
    alignment: usize,
    size: usize,
}
## /// 用户定义结构体的布局。
## #[derive(Debug)]
struct MockLayout {
##     /// 按声明顺序存储的字段。
    fields: Vec<Field>,
##     /// 每个字段相对结构体起始的偏移。
    field_offsets: Vec<usize>,
##     /// 总体对齐。
    alignment: usize,
##     /// 总体大小。
    size: usize,
}

impl MockLayout {
    /// 返回在 `offset` 之后需要多少填充，以确保
    /// 随后的地址将按 `alignment` 对齐。
    fn padding_needed_for(offset: usize, alignment: usize) -> usize {
        let misalignment = offset % alignment;
        if misalignment > 0 {
            // 向上舍入到 `alignment` 的下一个倍数。
            alignment - misalignment
        } else {
            // 已经是 `alignment` 的倍数。
            0
        }
    }

    /// 字段必须按声明顺序。到此时，它们的对齐和
    /// 大小已经计算完毕。
    pub fn from_fields(fields: Vec<Field>) -> Self {
        // 「结构体的对齐是其中对齐最大的字段的对齐，
        // 若没有字段则为 1。」
        let alignment = fields
            .iter()
            .map(|field| field.alignment)
            .max()
            .unwrap_or(1);

        // 「从当前偏移 0 字节开始。」
        let mut current_offset = 0;

        let mut field_offsets = vec![];
        for field in &fields {
            // 「若当前偏移不是该字段对齐的倍数，
            // 则向当前偏移添加填充字节，直到它成为
            // 该字段对齐的倍数。」
            current_offset += Self::padding_needed_for(
                current_offset,
                field.alignment
            );

            // 「该字段的偏移即为此时的当前偏移。」
            field_offsets.push(current_offset);

            // 「然后将当前偏移增加该字段的大小。」
            current_offset += field.size;
        }

        // 「最后，结构体的大小是将当前偏移向上舍入到
        // 结构体对齐的最近倍数。」
        let size = current_offset + Self::padding_needed_for(
            current_offset,
            alignment
        );

        MockLayout { fields, field_offsets, alignment, size }
    }
}
#
## #[repr(C)]
## struct Demo {
##     first: u8,
##     second: u32,
##     third: u64,
## }
## macro_rules! fields {
##     ( $( $t:ty ),+ ) => {
##         vec![
##             $( Field {
##                 alignment: std::mem::align_of::<$t>(),
##                 size: std::mem::size_of::<$t>(),
##             }),+
##         ]
##     }
## }
## let fields = fields![u8, u32, u64];
## let demo_layout = MockLayout::from_fields(fields);
## assert_eq!(std::mem::align_of::<Demo>(), demo_layout.alignment);
## assert_eq!(std::mem::size_of::<Demo>(), demo_layout.size);
```

> **警告**
> 此模拟实现使用忽略溢出问题的朴素算法，以便清晰说明。要在实际代码中执行内存布局计算，请使用 [`Layout`]。

> **注意**
> 此算法可以产生[零大小][zero-sized]结构体。在 C 中，像 `struct Foo { }` 这样的空结构体声明是非法的。然而，gcc 和 clang 都支持启用此类结构体的选项，并给它们大小 0。相比之下，C++ 给空结构体大小 1，除非它们被继承，或它们是具有 `[[no_unique_address]]` 属性的字段，在这种情况下它们不增加结构体的总体大小。

r[layout.repr.c.union]
#### `#[repr(C)]` 联合体

r[layout.repr.c.union.intro]
用 `#[repr(C)]` 声明的联合体将与目标平台上 C 语言中等价的 C 联合体声明具有相同的大小和对齐。

r[layout.repr.c.union.size-align]
该联合体的大小为其所有字段最大大小按其对齐舍入后的值，对齐为其所有字段的最大对齐。这些最大值可能来自不同字段。每个字段都位于相对联合体起始的字节偏移 0 处。

```rust
#[repr(C)]
union Union {
    f1: u16,
    f2: [u8; 4],
}

assert_eq!(std::mem::size_of::<Union>(), 4);  // 来自 f2
assert_eq!(std::mem::align_of::<Union>(), 2); // 来自 f1

assert_eq!(std::mem::offset_of!(Union, f1), 0);
assert_eq!(std::mem::offset_of!(Union, f2), 0);

#[repr(C)]
union SizeRoundedUp {
   a: u32,
   b: [u16; 3],
}

assert_eq!(std::mem::size_of::<SizeRoundedUp>(), 8);  // 来自 b 的大小 6，
                                                      // 按 a 的对齐
                                                      // 向上舍入到 8。
assert_eq!(std::mem::align_of::<SizeRoundedUp>(), 4); // 来自 a

assert_eq!(std::mem::offset_of!(SizeRoundedUp, a), 0);
assert_eq!(std::mem::offset_of!(SizeRoundedUp, b), 0);
```

r[layout.repr.c.enum]
#### `#[repr(C)]` 无字段枚举

对于[无字段枚举][field-less enums]，`C` 表示具有目标平台 C ABI 的默认 `enum` 大小和对齐。

> **注意**
> C 中的枚举表示是实现定义的，因此这其实是「最佳猜测」。特别是，当相关的 C 代码用某些标志编译时，这可能不正确。

> **警告**
> C 语言中的 `enum` 与具有此表示的 Rust [无字段枚举][field-less enums]之间有关键差异。C 中的 `enum` 大体上是 `typedef` 加上一些具名常量；换句话说，`enum` 类型的对象可以保存任何整数值。例如，这在 `C` 中常用于位标志。相比之下，Rust 的[无字段枚举][field-less enums]只能合法地保存判别式值，其他一切都是[未定义行为][undefined behavior]。因此，在 FFI 中用无字段枚举来建模 C `enum` 常常是错误的。

r[layout.repr.c.adt]
#### `#[repr(C)]` 带字段的枚举

r[layout.repr.c.adt.intro]
带字段的 `repr(C)` 枚举的表示是一个带有两个字段的 `repr(C)` 结构体，在 C 中也称为「带标签的联合体」：

r[layout.repr.c.adt.tag]
- 去掉所有字段后的该枚举的 `repr(C)` 版本（「标签」）

r[layout.repr.c.adt.fields]
- 每个曾有字段的变体的字段所组成的 `repr(C)` 结构体的 `repr(C)` 联合体（「载荷」）

> **注意**
> 由于 `repr(C)` 结构体和联合体的表示，若一个变体只有单个字段，将该字段直接放入联合体或将其包在结构体中没有区别；任何希望操作此类 `enum` 表示的系统因此可以使用对他们更方便或更一致的形式。

```rust
// 此 Enum 与 ... 具有相同的表示
#[repr(C)]
enum MyEnum {
    A(u32),
    B(f32, u64),
    C { x: u32, y: u8 },
    D,
 }

// ... 这个结构体。
#[repr(C)]
struct MyEnumRepr {
    tag: MyEnumDiscriminant,
    payload: MyEnumFields,
}

// 这是判别式枚举。
#[repr(C)]
enum MyEnumDiscriminant { A, B, C, D }

// 这是变体联合体。
#[repr(C)]
union MyEnumFields {
    A: MyAFields,
    B: MyBFields,
    C: MyCFields,
    D: MyDFields,
}

#[repr(C)]
#[derive(Copy, Clone)]
struct MyAFields(u32);

#[repr(C)]
#[derive(Copy, Clone)]
struct MyBFields(f32, u64);

#[repr(C)]
#[derive(Copy, Clone)]
struct MyCFields { x: u32, y: u8 }

// 此结构体可以省略（它是零大小类型），并且它必须出现在
// C/C++ 头文件中。
#[repr(C)]
#[derive(Copy, Clone)]
struct MyDFields;
```

r[layout.repr.primitive]
### 原始表示

r[layout.repr.primitive.intro]
*原始表示* 是与原始整数类型同名的表示。即：`u8`、`u16`、`u32`、`u64`、`u128`、`usize`、`i8`、`i16`、`i32`、`i64`、`i128` 和 `isize`。

r[layout.repr.primitive.constraint]
原始表示只能应用于枚举，并且根据枚举有无字段而有不同行为。为[零变体枚举][zero-variant enums]指定原始表示是错误。将两种原始表示组合在一起是错误。

r[layout.repr.primitive.enum]
#### 无字段枚举的原始表示

对于[无字段枚举][field-less enums]，原始表示将大小和对齐设置为与同名原始类型相同。例如，具有 `u8` 表示的无字段枚举的判别式只能在 0 到 255（含）之间。

r[layout.repr.primitive.adt]
#### 带字段枚举的原始表示

原始表示枚举的表示是每个带字段变体的 `repr(C)` 结构体组成的 `repr(C)` 联合体。联合体中每个结构体的第一个字段是去掉所有字段后该枚举的原始表示版本（「标签」），其余字段是该变体的字段。

> **注意**
> 若将标签作为联合体的独立成员给出，此表示不变，若这使操作对你更清晰（尽管要遵循 C++ 标准，标签成员应包在 `struct` 中）。

> **注意**
> 此表示与带字段枚举的 `repr(C)` 相当不同。

```rust
// 此枚举与 ... 具有相同的表示
#[repr(u8)]
enum MyEnum {
    A(u32),
    B(f32, u64),
    C { x: u32, y: u8 },
    D,
 }

// ... 这个联合体。
#[repr(C)]
union MyEnumRepr {
    A: MyVariantA,
    B: MyVariantB,
    C: MyVariantC,
    D: MyVariantD,
}

// 这是判别式枚举。
#[repr(u8)]
#[derive(Copy, Clone)]
enum MyEnumDiscriminant { A, B, C, D }

#[repr(C)]
#[derive(Clone, Copy)]
struct MyVariantA(MyEnumDiscriminant, u32);

#[repr(C)]
#[derive(Clone, Copy)]
struct MyVariantB(MyEnumDiscriminant, f32, u64);

#[repr(C)]
#[derive(Clone, Copy)]
struct MyVariantC { tag: MyEnumDiscriminant, x: u32, y: u8 }

#[repr(C)]
#[derive(Clone, Copy)]
struct MyVariantD(MyEnumDiscriminant);
```

r[layout.repr.primitive-c]
#### 将带字段枚举的原始表示与 `#[repr(C)]` 组合

对于带字段的枚举，也可以将 `repr(C)` 与原始表示组合（例如 `repr(C, u8)`）。这通过将判别式枚举的表示改为所选的原始类型来修改 [`repr(C)`]。因此，若你选择 `u8` 表示，则判别式枚举的大小和对齐将为 1 字节。

> **注意**
> 这意味着 `repr(C, u8)` 与 `repr(u8)` 相当不同！
> 前者是带有两个字段（标签和变体联合体）的结构体，后者是每个字段都以标签开头的联合体。

[先前][`repr(C)`]例子中的判别式枚举于是变为：

```rust
#[repr(C, u8)] // 添加了 `u8`
enum MyEnum {
    A(u32),
    B(f32, u64),
    C { x: u32, y: u8 },
    D,
 }

// ...

#[repr(u8)] // 因此这里使用 `u8` 而不是 `C`
enum MyEnumDiscriminant { A, B, C, D }

// ...
```

例如，对于 `repr(C, u8)` 枚举，不可能有 257 个唯一判别式（「标签」），而同样的枚举若只有 `repr(C)` 属性则可以毫无问题地编译。

在 `repr(C)` 之外再使用原始表示可以改变枚举相对 `repr(C)` 形式的大小：

```rust
#[repr(C)]
enum EnumC {
    Variant0(u8),
    Variant1,
}

#[repr(C, u8)]
enum Enum8 {
    Variant0(u8),
    Variant1,
}

#[repr(C, u16)]
enum Enum16 {
    Variant0(u8),
    Variant1,
}

// C 表示的大小取决于平台
assert_eq!(std::mem::size_of::<EnumC>(), 8);
// Enum8::Variant0 中一字节给判别式，一字节给值
assert_eq!(std::mem::size_of::<Enum8>(), 2);
// Enum16::Variant0 中两字节给判别式，一字节给值
// 外加一字节填充。
assert_eq!(std::mem::size_of::<Enum16>(), 4);
```

[`repr(C)`]: #reprc-enums-with-fields

r[layout.repr.alignment]
### 对齐修饰符

r[layout.repr.alignment.intro]
`align` 和 `packed` 修饰符可以分别用于提高或降低 `struct` 和 `union` 的对齐。`packed` 也可能改变字段之间的填充（尽管它不会改变任何字段内部的填充）。单独使用时，`align` 和 `packed` 不提供关于结构体布局中字段顺序或枚举变体布局的保证，尽管它们可以与提供此类保证的表示（如 `C`）组合。

r[layout.repr.alignment.constraint-alignment]
对齐以整数参数的形式指定，如 `#[repr(align(x))]` 或 `#[repr(packed(x))]`。对齐值必须是从 1 到 2<sup>29</sup> 的 2 的幂。对于 `packed`，若未给出值，如 `#[repr(packed)]`，则值为 1。

r[layout.repr.alignment.align]
对于 `align`，若指定的对齐小于没有 `align` 修饰符时该类型的对齐，则对齐不受影响。

r[layout.repr.alignment.packed]
对于 `packed`，若指定的对齐大于没有 `packed` 修饰符时该类型的对齐，则对齐和布局不受影响。

r[layout.repr.alignment.packed-fields]
为定位字段之目的，每个字段的对齐是指定对齐与该字段类型对齐中较小的那个。

r[layout.repr.alignment.packed-padding]
字段间填充保证为满足每个字段（可能被改变的）对齐所需的最小值（尽管注意，单独使用时 `packed` 不提供关于字段顺序的任何保证）。这些规则的一个重要后果是，具有 `#[repr(packed(1))]`（或 `#[repr(packed)]`）的类型将没有字段间填充。

r[layout.repr.alignment.constraint-exclusive]
`align` 和 `packed` 修饰符不能应用于同一类型，并且 `packed` 类型不能传递性地包含另一个带 `align` 的类型。`align` 和 `packed` 只能应用于 [`Rust`] 和 [`C`] 表示。

r[layout.repr.alignment.enum]
`align` 修饰符也可以应用于 `enum`。当如此时，对 `enum` 对齐的影响与将该 `enum` 包在具有相同 `align` 修饰符的 newtype `struct` 中相同。

> **注意**
> 不允许引用未对齐的字段，因为这是[未定义行为][undefined behavior]。当字段因对齐修饰符而未对齐时，考虑以下使用引用和解引用的选项：
>
> ```rust
> #[repr(packed)]
> struct Packed {
>     f1: u8,
>     f2: u16,
> }
> let mut e = Packed { f1: 1, f2: 2 };
> // 不要创建指向字段的引用，而是将值复制到局部变量。
> let x = e.f2;
> // 或者在像 `println!` 这样会创建引用的情形中，使用花括号
> // 将其改为值的副本。
> println!("{}", {e.f2});
> // 或者若你需要指针，使用未对齐的读写方法，
> // 而不是直接解引用该指针。
> let ptr: *const u16 = &raw const e.f2;
> let value = unsafe { ptr.read_unaligned() };
> let mut_ptr: *mut u16 = &raw mut e.f2;
> unsafe { mut_ptr.write_unaligned(3) }
> ```

r[layout.repr.transparent]
### `transparent` 表示

r[layout.repr.transparent.constraint-field]
`transparent` 表示只能用于 [`struct`][structs] 或只有单个变体的 [`enum`][enumerations]，该变体具有：
- 任意数量大小为 0、对齐为 1 的字段（例如 [`PhantomData<T>`]），以及
- 至多一个其他字段。

r[layout.repr.transparent.layout-abi]
具有此表示的结构体和枚举与唯一那个非大小 0、非对齐 1 的字段（若存在）具有相同的布局和 ABI，否则与单元类型相同。

这与 `C` 表示不同，因为具有 `C` 表示的结构体将始终具有 `C` `struct` 的 ABI，而例如具有 `transparent` 表示且带有原始类型字段的结构体将具有该原始类型字段的 ABI。

r[layout.repr.transparent.constraint-exclusive]
由于此表示将类型布局委托给另一种类型，它不能与任何其他表示一起使用。

[`align_of_val`]: std::mem::align_of_val
[`size_of_val`]: std::mem::size_of_val
[`align_of`]: std::mem::align_of
[`size_of`]: std::mem::size_of
[`Sized`]: std::marker::Sized
[`Copy`]: std::marker::Copy
[dynamically sized types]: dynamically-sized-types.md
[enums]: items/enumerations.md
[field-less enums]: items/enumerations.md#field-less-enum
[field-struct-like variant]: EnumVariantStruct
[fn-abi-compatibility]: ../core/primitive.fn.md#abi-compatibility
[enumerations]: items/enumerations.md
[zero-variant enums]: items/enumerations.md#zero-variant-enums
[undefined behavior]: behavior-considered-undefined.md
[zero sized]: glossary.zst
[zero-sized]: glossary.zst
[zero-sized type]: glossary.zst
[zero-sized types]: glossary.zst
[`PhantomData<T>`]: special-types-and-traits.md#phantomdatat
[`Rust`]: #the-rust-representation
[`C`]: #the-c-representation
[primitive representation]: #primitive-representations
[primitive representations]: #primitive-representations
[structs]: items/structs.md
[`transparent`]: #the-transparent-representation
[tuple-struct-like variant]: EnumVariantTuple
[unit-struct-like variant]: EnumVariant
[`Layout`]: std::alloc::Layout
[uninhabited]: glossary.uninhabited
