+++
title = "07-枚举"
date = 2026-08-18T08:45:00+08:00
weight = 24
type = "docs"
description = "枚举 — The Rust Reference"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Reference](https://doc.rust-lang.org/reference/)

> 原文链接: [https://doc.rust-lang.org/reference/items/enumerations.html](https://doc.rust-lang.org/reference/items/enumerations.html)

r[items.enum]
# 枚举

r[items.enum.syntax]
```grammar,items
Enumeration ->
    `enum` IDENTIFIER GenericParams? WhereClause? `{` EnumVariants? `}`

EnumVariants -> EnumVariant ( `,` EnumVariant )* `,`?

EnumVariant ->
    OuterAttribute* Visibility?
    IDENTIFIER ( EnumVariantTuple | EnumVariantStruct )? EnumVariantDiscriminant?

EnumVariantTuple -> `(` TupleFields? `)`

EnumVariantStruct -> `{` StructFields? `}`

EnumVariantDiscriminant -> `=` Expression
```

r[items.enum.intro]
*枚举*（enumeration），也称 *enum*，同时定义一个名义[枚举类型][enumerated type]以及一组*构造器*，这些构造器可用于创建或模式匹配相应枚举类型的值。

r[items.enum.decl]
枚举用关键字 `enum` 声明。

r[items.enum.namespace]
`enum` 声明在其所在模块或块的[类型命名空间][type namespace]中定义枚举类型。

`enum` 项及其使用的一个例子：

```rust
enum Animal {
    Dog,
    Cat,
}

let mut a: Animal = Animal::Dog;
a = Animal::Cat;
```

r[items.enum.constructor]
枚举构造器可以具有具名字段或匿名字段：

```rust
enum Animal {
    Dog(String, f64),
    Cat { name: String, weight: f64 },
}

let mut a: Animal = Animal::Dog("Cocoa".to_string(), 37.2);
a = Animal::Cat { name: "Spotty".to_string(), weight: 2.7 };
```

在此例中，`Cat` 是*类结构体枚举变体*，而 `Dog` 通常就称为枚举变体。

r[items.enum.fieldless]
没有构造器包含字段的枚举称为*<span id="field-less-enum">无字段枚举</span>*。例如，这是一个无字段枚举：

```rust
enum Fieldless {
    Tuple(),
    Struct{},
    Unit,
}
```

r[items.enum.unit-only]
若无字段枚举只包含单元变体，则该枚举称为*<span id="unit-only-enum">仅单元变体枚举</span>*。例如：

```rust
enum Enum {
    Foo = 3,
    Bar = 2,
    Baz = 1,
}
```

r[items.enum.constructor-names]
变体构造器类似于[结构体][struct]定义，并可通过从枚举名出发的路径引用，包括在 [use 声明][use declarations]中。

r[items.enum.constructor-namespace]
每个变体在[类型命名空间][type namespace]中定义其类型，不过该类型不能用作类型说明符。类元组和类单元变体还在[值命名空间][value namespace]中定义一个构造器。

r[items.enum.struct-expr]
类结构体变体可以用[结构体表达式][struct expression]实例化。

r[items.enum.tuple-expr]
类元组变体可以用[调用表达式][call expression]或[结构体表达式][struct expression]实例化。

r[items.enum.path-expr]
类单元变体可以用[路径表达式][path expression]或[结构体表达式][struct expression]实例化。例如：

```rust
enum Examples {
    UnitLike,
    TupleLike(i32),
    StructLike { value: i32 },
}

use Examples::*; // 为所有变体创建别名。
let x = UnitLike; // 常量项的路径表达式。
let x = UnitLike {}; // 结构体表达式。
let y = TupleLike(123); // 调用表达式。
let y = TupleLike { 0: 123 }; // 使用整数字段名的结构体表达式。
let z = StructLike { value: 123 }; // 结构体表达式。
```

<span id="custom-discriminant-values-for-fieldless-enumerations"></span>
r[items.enum.discriminant]
## 判别值

r[items.enum.discriminant.intro]
每个枚举实例都有一个*判别值*：在逻辑上与之关联的整数，用于确定它持有哪个变体。

r[items.enum.discriminant.repr-rust]
在 [`Rust` 表示][`Rust` representation]下，判别值被解释为 `isize` 值。不过，编译器在实际内存布局中允许使用更小的类型（或其他区分变体的手段）。

### 指定判别值

r[items.enum.discriminant.explicit]
#### 显式判别值

r[items.enum.discriminant.explicit.intro]
在两种情况下，可以通过在变体名后跟随 `=` 和一个[常量表达式][constant expression]来显式设置变体的判别值：

r[items.enum.discriminant.explicit.unit-only]
1. 若该枚举是“[仅单元变体][unit-only]”的。

r[items.enum.discriminant.explicit.primitive-repr]
2. 若使用了[原始表示][primitive representation]。例如：

   ```rust
   #[repr(u8)]
   enum Enum {
       Unit = 3,
       Tuple(u16),
       Struct {
           a: u8,
           b: u16,
       } = 1,
   }
   ```

r[items.enum.discriminant.implicit]
#### 隐式判别值

若未指定变体的判别值，则将其设为声明中前一个变体的判别值加一。若声明中第一个变体的判别值未指定，则将其设为零。

```rust
enum Foo {
    Bar,            // 0
    Baz = 123,      // 123
    Quux,           // 124
}

let baz_discriminant = Foo::Baz as u32;
assert_eq!(baz_discriminant, 123);
```

r[items.enum.discriminant.restrictions]
#### 限制

r[items.enum.discriminant.restrictions.same-discriminant]
两个变体共享同一判别值是错误的。

```rust
enum SharedDiscriminantError {
    SharedA = 1,
    SharedB = 1,
}

enum SharedDiscriminantError2 {
    Zero,       // 0
    One,        // 1
    OneToo = 1, // 1（与前一个冲突！）
}
```

r[items.enum.discriminant.restrictions.above-max-discriminant]
在前一个判别值已是该判别值大小所能表示的最大值时仍使用未指定的判别值，也是错误的。

```rust
#[repr(u8)]
enum OverflowingDiscriminantError {
    Max = 255,
    MaxPlusOne, // 本应为 256，但会使枚举溢出。
}

#[repr(u8)]
enum OverflowingDiscriminantError2 {
    MaxMinusOne = 254, // 254
    Max,               // 255
    MaxPlusOne,        // 本应为 256，但会使枚举溢出。
}
```

r[items.enum.discriminant.restrictions.generics]
显式的枚举判别值初始化器不得使用外围枚举的泛型参数。

```rust
#[repr(u32)]
enum E<'a, T, const N: u32> {
    Lifetime(&'a T) = {
        let a: &'a (); // 错误。
        1
    },
    Type(T) = {
        let x: T; // 错误。
        2
    },
    Const = N, // 错误。
}
```

### 访问判别值

#### 通过 `mem::discriminant`

r[items.enum.discriminant.access-opaque]

[`std::mem::discriminant`] 返回对枚举值判别值的不透明引用，可以进行比较。这不能用于获取判别值的数值。

r[items.enum.discriminant.coercion]
#### 强制转换

r[items.enum.discriminant.coercion.intro]
若枚举是[仅单元变体][unit-only]的（没有元组和结构体变体），则其判别值可以通过[数值强制转换][numeric cast]直接访问；例如：

```rust
enum Enum {
    Foo,
    Bar,
    Baz,
}

assert_eq!(0, Enum::Foo as isize);
assert_eq!(1, Enum::Bar as isize);
assert_eq!(2, Enum::Baz as isize);
```

r[items.enum.discriminant.coercion.fieldless]
[无字段枚举][Field-less enums]可以强制转换，前提是它们没有显式判别值，或者只有单元变体是显式指定的。

```rust
enum Fieldless {
    Tuple(),
    Struct{},
    Unit,
}

assert_eq!(0, Fieldless::Tuple() as isize);
assert_eq!(1, Fieldless::Struct{} as isize);
assert_eq!(2, Fieldless::Unit as isize);

#[repr(u8)]
enum FieldlessWithDiscriminants {
    First = 10,
    Tuple(),
    Second = 20,
    Struct{},
    Unit,
}

assert_eq!(10, FieldlessWithDiscriminants::First as u8);
assert_eq!(11, FieldlessWithDiscriminants::Tuple() as u8);
assert_eq!(20, FieldlessWithDiscriminants::Second as u8);
assert_eq!(21, FieldlessWithDiscriminants::Struct{} as u8);
assert_eq!(22, FieldlessWithDiscriminants::Unit as u8);
```

#### 指针强制转换

r[items.enum.discriminant.access-memory]

若枚举指定了[原始表示][primitive representation]，则可以通过不安全的指针强制转换可靠地访问判别值：

```rust
#[repr(u8)]
enum Enum {
    Unit,
    Tuple(bool),
    Struct{a: bool},
}

impl Enum {
    fn discriminant(&self) -> u8 {
        unsafe { *(self as *const Self as *const u8) }
    }
}

let unit_like = Enum::Unit;
let tuple_like = Enum::Tuple(true);
let struct_like = Enum::Struct{a: false};

assert_eq!(0, unit_like.discriminant());
assert_eq!(1, tuple_like.discriminant());
assert_eq!(2, struct_like.discriminant());
```

r[items.enum.empty]
## 零变体枚举

r[items.enum.empty.intro]
没有变体的枚举称为*零变体枚举*。由于它们没有合法值，因此不能被实例化。

```rust
enum ZeroVariants {}
```

r[items.enum.empty.uninhabited]
零变体枚举等价于 [never 类型][never type]，但不能被强制转换为其他类型。

```rust
## enum ZeroVariants {}
let x: ZeroVariants = panic!();
let y: u32 = x; // 类型不匹配错误
```

r[items.enum.variant-visibility]
## 变体可见性

枚举变体在语法上允许 [Visibility] 注解，但在验证枚举时会被拒绝。这使项可以在不同使用上下文中以统一语法被解析。

```rust
macro_rules! mac_variant {
    ($vis:vis $name:ident) => {
        enum $name {
            $vis Unit,

            $vis Tuple(u8, u16),

            $vis Struct { f: u8 },
        }
    }
}

// 允许空的 `vis`。
mac_variant! { E }

// 这是允许的，因为它在验证之前就被移除了。
#[cfg(false)]
enum E {
    pub U,
    pub(crate) T(u8),
    pub(super) T { f: String },
}
```

[`C` representation]: ../type-layout.md#the-c-representation
[call expression]: ../expressions/call-expr.md
[constant expression]: ../const_eval.md#constant-expressions
[enumerated type]: ../types/enum.md
[Field-less enums]: #field-less-enum
[never type]: ../types/never.md
[numeric cast]: ../expressions/operator-expr.md#semantics
[path expression]: ../expressions/path-expr.md
[primitive representation]: ../type-layout.md#primitive-representations
[`Rust` representation]: ../type-layout.md#the-rust-representation
[struct expression]: ../expressions/struct-expr.md
[struct]: structs.md
[type namespace]: ../names/namespaces.md
[unit-only]: #unit-only-enum
[use declarations]: use-declarations.md
[value namespace]: ../names/namespaces.md
