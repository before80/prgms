+++
title = "04-运算符表达式"
date = 2026-08-18T08:45:00+08:00
weight = 47
type = "docs"
description = "运算符表达式 — The Rust Reference"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Reference](https://doc.rust-lang.org/reference/)

> 原文链接: [https://doc.rust-lang.org/reference/expressions/operator-expr.html](https://doc.rust-lang.org/reference/expressions/operator-expr.html)

r[expr.operator]
# 运算符表达式

r[expr.operator.syntax]
```grammar,expressions
OperatorExpression ->
      BorrowExpression
    | DereferenceExpression
    | TryPropagationExpression
    | NegationExpression
    | ArithmeticOrLogicalExpression
    | ComparisonExpression
    | LazyBooleanExpression
    | TypeCastExpression
    | AssignmentExpression
    | CompoundAssignmentExpression
```

r[expr.operator.intro]
Rust 语言为内建类型定义了运算符。

r[expr.operator.trait]
下列许多运算符也可以使用 `std::ops` 或 `std::cmp` 中的 trait 进行重载。

r[expr.operator.int-overflow]
## 溢出

r[expr.operator.int-overflow.intro]
整数运算符在调试模式下编译时，若溢出则会 panic。编译器标志 `-C debug-assertions` 和 `-C overflow-checks` 可用于更直接地控制这一点。下列情况被视为溢出：

r[expr.operator.int-overflow.binary-arith]
* 当 `+`、`*` 或二元 `-` 产生大于可存储最大值、或小于可存储最小值的值时。

r[expr.operator.int-overflow.unary-neg]
* 对任何有符号整数类型的最小负值应用一元 `-`，除非操作数是[字面量表达式][literal expression]（或单独出现在一层或多层[分组表达式][grouped expression]内的字面量表达式）。

r[expr.operator.int-overflow.div]
* 使用 `/` 或 `%`，且左操作数是有符号整数类型的最小整数、右操作数是 `-1`。由于历史原因，即使禁用了 `-C overflow-checks`，仍会进行这些检查。

r[expr.operator.int-overflow.shift]
* 使用 `<<` 或 `>>`，且右操作数大于或等于左操作数类型的位数，或为负数。

> **注意**
> 一元 `-` 之后的字面量表达式这一例外意味着，诸如 `-128_i8` 或 `let j: i8 = -(128)` 这样的形式永远不会引起 panic，并且具有预期值 -128。
>
> 在这些情况下，字面量表达式已经具有其类型的最小负值（例如，`128_i8` 的值为 -128），因为按[整数字面量表达式][literal expression]中的描述，整数字面量会被截断为其类型。
>
> 由于二进制补码溢出约定，对这些最小负值取负会保持该值不变。
>
> 在 `rustc` 中，这些最小负值表达式也会被 `overflowing_literals` lint 检查忽略。

r[expr.operator.borrow]
## 借用运算符

r[expr.operator.borrow.syntax]
```grammar,expressions
BorrowExpression ->
      (`&`|`&&`) Expression
    | (`&`|`&&`) `mut` Expression
    | (`&`|`&&`) `raw` `const` Expression
    | (`&`|`&&`) `raw` `mut` Expression
```

r[expr.operator.borrow.intro]
`&`（共享借用）和 `&mut`（可变借用）运算符是一元前缀运算符。

r[expr.operator.borrow.result]
当应用于[位置表达式][place expression]时，该表达式产生指向该位置的引用（指针）。

r[expr.operator.borrow.lifetime]
在该引用的持续期间，该内存位置也会进入被借用状态。对于共享借用（`&`），这意味着该位置不可被修改，但可以被读取或再次共享。对于可变借用（`&mut`），在该借用结束之前，不得以任何方式访问该位置。

r[expr.operator.borrow.mut]
`&mut` 在可变位置表达式上下文中求值其操作数。

r[expr.operator.borrow.temporary]
若 `&` 或 `&mut` 运算符应用于[值表达式][value expression]，则会创建一个[临时值][temporary value]。

这些运算符不能被重载。

```rust
{
    // 创建一个值为 7、存活期为此作用域的临时值。
    let shared_reference = &7;
}
let mut array = [-2, 3, 9];
{
    // 在此作用域内可变借用 `array`。
    // `array` 只能通过 `mutable_reference` 使用。
    let mutable_reference = &mut array;
}
```

r[expr.borrow.and-and-syntax]
尽管 `&&` 是单个 token（[惰性「与」运算符](#lazy-boolean-operators)），但在借用表达式的上下文中，它相当于两次借用：

```rust
// 含义相同：
let a = &&  10;
let a = & & 10;

// 含义相同：
let a = &&&&  mut 10;
let a = && && mut 10;
let a = & & & & mut 10;
```

r[expr.borrow.raw]
### 裸借用运算符

r[expr.borrow.raw.intro]
`&raw const` 和 `&raw mut` 是*裸借用运算符*。

r[expr.borrow.raw.place]
这些运算符的操作数表达式在位置表达式上下文中求值。

r[expr.borrow.raw.result]
随后，`&raw const expr` 创建指向给定位置、类型为 `*const T` 的常量裸指针，而 `&raw mut expr` 创建类型为 `*mut T` 的可变裸指针。

r[expr.borrow.raw.invalid-ref]
每当位置表达式可能求值为未正确对齐、或并未按其类型存储有效值的位置时，或者每当创建引用会引入不正确的别名假设时，必须使用裸借用运算符而非借用运算符。在那些情形下，使用借用运算符会因创建无效引用而导致[未定义行为][undefined behavior]，但仍然可以构造裸指针。

以下是通过 `packed` 结构体创建指向未对齐位置的裸指针的示例：

```rust
#[repr(packed)]
struct Packed {
    f1: u8,
    f2: u16,
}

let packed = Packed { f1: 1, f2: 2 };
// `&packed.f2` 会创建未对齐的引用，因而属于未定义行为！
let raw_f2 = &raw const packed.f2;
assert_eq!(unsafe { raw_f2.read_unaligned() }, 2);
```

以下是创建指向不含有效值的位置的裸指针的示例：

```rust
use std::mem::MaybeUninit;

struct Demo {
    field: bool,
}

let mut uninit = MaybeUninit::<Demo>::uninit();
// `&uninit.as_mut().field` 会创建指向未初始化 `bool` 的引用，
// 因而属于未定义行为！
let f1_ptr = unsafe { &raw mut (*uninit.as_mut_ptr()).field };
unsafe { f1_ptr.write(true); }
let init = unsafe { uninit.assume_init() };
```

r[expr.deref]
## 解引用运算符

r[expr.deref.syntax]
```grammar,expressions
DereferenceExpression -> `*` Expression
```

r[expr.deref.intro]
`*`（解引用）运算符也是一元前缀运算符。

r[expr.deref.result]
当应用于[指针](../../type-system/01-types/14-pointer/)或 [`Box`] 时，它表示所指向的位置。

r[expr.deref.mut]
若表达式的类型为 `&mut T`、`*mut T` 或 `Box<T>`，并且它是局部变量、局部变量的（嵌套）字段，或是可变[位置表达式][place expression]，则可以对所得的内存位置进行赋值。

r[expr.deref.box]
当应用于 [`Box`] 时，所得位置可以被[从中移出][moved from]。

r[expr.deref.safety]
解引用裸指针需要 `unsafe`。

r[expr.deref.traits]
对于非指针类型，在[不可变位置表达式上下文](./#mutability)中 `*x` 等价于 `*std::ops::Deref::deref(&x)`，在可变位置表达式上下文中等价于 `*std::ops::DerefMut::deref_mut(&mut x)`，但有一个例外：当 `*x` 发生[临时值生命周期延长][temporary lifetime extension]时，被解引用的表达式 `x` 的[临时作用域][temporary scope]也会被延长。

```rust
## struct NoCopy;
let a = &7;
assert_eq!(*a, 7);
let b = &mut 9;
*b = 11;
assert_eq!(*b, 11);
let c = Box::new(NoCopy);
let d: NoCopy = *c;
```

```rust
// 保存 `String::new()` 结果的临时值会被延长
// 到块的末尾，因此 `x` 可在后续语句中使用。
let x = &*String::new();
## x;
```

```rust
// 保存 `String::new()` 结果的临时值会在语句末尾被丢弃，
// 因此之后使用 `y` 是错误的。
let y = &*std::ops::Deref::deref(&String::new()); // 错误
## y;
```

r[expr.try]
## try 传播表达式

r[expr.try.syntax]
```grammar,expressions
TryPropagationExpression -> Expression `?`
```

r[expr.try.intro]
try 传播表达式使用内部表达式的值以及 [`Try`] trait，来决定是产生一个值（若是，产生何值），还是向调用者返回一个值（若是，返回何值）。

> [!EXAMPLE]
> ```rust
> # use std::num::ParseIntError;
> fn try_to_parse() -> Result<i32, ParseIntError> {
>     let x: i32 = "123".parse()?; // `x` 为 `123`。
>     let y: i32 = "24a".parse()?; // 立即返回 `Err()`。
>     Ok(x + y)                    // 不会执行。
> }
>
> let res = try_to_parse();
> println!("{res:?}");
> # assert!(res.is_err())
> ```
>
> ```rust
> fn try_option_some() -> Option<u8> {
>     let val = Some(1)?;
>     Some(val)
> }
> assert_eq!(try_option_some(), Some(1));
>
> fn try_option_none() -> Option<u8> {
>     let val = None?;
>     Some(val)
> }
> assert_eq!(try_option_none(), None);
> ```
>
> ```rust
> use std::ops::ControlFlow;
>
> pub struct TreeNode<T> {
>     value: T,
>     left: Option<Box<TreeNode<T>>>,
>     right: Option<Box<TreeNode<T>>>,
> }
>
> impl<T> TreeNode<T> {
>     pub fn traverse_inorder<B>(&self, f: &mut impl FnMut(&T) -> ControlFlow<B>) -> ControlFlow<B> {
>         if let Some(left) = &self.left {
>             left.traverse_inorder(f)?;
>         }
>         f(&self.value)?;
>         if let Some(right) = &self.right {
>             right.traverse_inorder(f)?;
>         }
>         ControlFlow::Continue(())
>     }
> }
> #
> # fn main() {
> #     let n = TreeNode {
> #         value: 1,
> #         left: Some(Box::new(TreeNode{value: 2, left: None, right: None})),
> #         right: None,
> #     };
> #     let v = n.traverse_inorder(&mut |t| {
> #         if *t == 2 {
> #             ControlFlow::Break("found")
> #         } else {
> #             ControlFlow::Continue(())
> #         }
> #     });
> #     assert_eq!(v, ControlFlow::Break("found"));
> # }
> ```

> **注意**
> [`Try`] trait 目前不稳定，因此不能为用户类型实现。
>
> try 传播表达式目前大致等价于：
>
> ```rust
> # #![ feature(try_trait_v2) ]
> # fn example() -> Result<(), ()> {
> # let expr = Ok(());
> match core::ops::Try::branch(expr) {
>     core::ops::ControlFlow::Continue(val) => val,
>     core::ops::ControlFlow::Break(residual) =>
>         return core::ops::FromResidual::from_residual(residual),
> }
> # Ok(())
> # }
> ```

> **注意**
> try 传播运算符有时也称为*问号运算符*、*`?` 运算符*，或 *try 运算符*。

r[expr.try.restricted-types]
try 传播运算符可应用于具有以下类型的表达式：

- [`Result<T, E>`]
    - `Result::Ok(val)` 求值为 `val`。
    - `Result::Err(e)` 返回 `Result::Err(From::from(e))`。
- [`Option<T>`]
    - `Option::Some(val)` 求值为 `val`。
    - `Option::None` 返回 `Option::None`。
- [`ControlFlow<B, C>`][core::ops::ControlFlow]
    - `ControlFlow::Continue(c)` 求值为 `c`。
    - `ControlFlow::Break(b)` 返回 `ControlFlow::Break(b)`。
- [`Poll<Result<T, E>>`][core::task::Poll]
    - `Poll::Ready(Ok(val))` 求值为 `Poll::Ready(val)`。
    - `Poll::Ready(Err(e))` 返回 `Poll::Ready(Err(From::from(e)))`。
    - `Poll::Pending` 求值为 `Poll::Pending`。
- [`Poll<Option<Result<T, E>>>`][`core::task::Poll`]
    - `Poll::Ready(Some(Ok(val)))` 求值为 `Poll::Ready(Some(val))`。
    - `Poll::Ready(Some(Err(e)))` 返回 `Poll::Ready(Some(Err(From::from(e))))`。
    - `Poll::Ready(None)` 求值为 `Poll::Ready(None)`。
    - `Poll::Pending` 求值为 `Poll::Pending`。

r[expr.negate]
## 取反运算符

r[expr.negate.syntax]
```grammar,expressions
NegationExpression ->
      `-` Expression
    | `!` Expression
```

r[expr.negate.intro]
这是最后两个一元运算符。

r[expr.negate.results]
下表概括了它们在基本类型上的行为，以及用哪些 trait 为其他类型重载这些运算符。请记住有符号整数始终使用二进制补码表示。所有这些运算符的操作数都在[值表达式上下文][value expression]中求值，因此会被移出或复制。

| 符号 | 整数        | `bool`        | 浮点           | 重载 Trait         |
|--------|-------------|-------------- |----------------|--------------------|
| `-`    | 取负*       |               | 取负           | `std::ops::Neg`    |
| `!`    | 按位取反    | [逻辑非][Logical NOT] |                | `std::ops::Not`    |

\* 仅适用于有符号整数类型。

以下是这些运算符的一些示例。

```rust
let x = 6;
assert_eq!(-x, -6);
assert_eq!(!x, -7);
assert_eq!(true, !false);
```

r[expr.arith-logic]
## 算术与逻辑二元运算符

r[expr.arith-logic.syntax]
```grammar,expressions
ArithmeticOrLogicalExpression ->
      Expression `+` Expression
    | Expression `-` Expression
    | Expression `*` Expression
    | Expression `/` Expression
    | Expression `%` Expression
    | Expression `&` Expression
    | Expression `|` Expression
    | Expression `^` Expression
    | Expression `<<` Expression
    | Expression `>>` Expression
```

r[expr.arith-logic.intro]
二元运算符表达式均以中缀记法书写。

r[expr.arith-logic.behavior]
下表概括了算术与逻辑二元运算符在基本类型上的行为，以及用哪些 trait 为其他类型重载这些运算符。请记住有符号整数始终使用二进制补码表示。所有这些运算符的操作数都在[值表达式上下文][value expression]中求值，因此会被移出或复制。

| 符号 | 整数                    | `bool`        | 浮点           | 重载 Trait         | 重载复合赋值 Trait |
|--------|-------------------------|---------------|----------------|--------------------| ------------------------------------- |
| `+`    | 加法                    |               | 加法           | `std::ops::Add`    | `std::ops::AddAssign`                 |
| `-`    | 减法                    |               | 减法           | `std::ops::Sub`    | `std::ops::SubAssign`                 |
| `*`    | 乘法                    |               | 乘法           | `std::ops::Mul`    | `std::ops::MulAssign`                 |
| `/`    | 除法*†                  |               | 除法           | `std::ops::Div`    | `std::ops::DivAssign`                 |
| `%`    | 余数**†                 |               | 余数           | `std::ops::Rem`    | `std::ops::RemAssign`                 |
| `&`    | 按位与                  | [逻辑与][Logical AND] |                | `std::ops::BitAnd` | `std::ops::BitAndAssign`              |
| `\|` | 按位或 | [逻辑或][Logical OR]  |                | `std::ops::BitOr`  | `std::ops::BitOrAssign`               |
| `^`    | 按位异或                | [逻辑异或][Logical XOR] |                | `std::ops::BitXor` | `std::ops::BitXorAssign`              |
| `<<`   | 左移                    |               |                | `std::ops::Shl`    | `std::ops::ShlAssign`                 |
| `>>`   | 右移***                 |               |                | `std::ops::Shr`    |  `std::ops::ShrAssign`                |

\* 整数除法向零舍入。

\*\* Rust 使用由[截断除法](https://en.wikipedia.org/wiki/Modulo_operation#Variants_of_the_definition)定义的余数。给定 `remainder = dividend % divisor`，余数的符号与被除数相同。

\*\*\* 对有符号整数类型为算术右移，对无符号整数类型为逻辑右移。

† 对于整数类型，除以零会 panic。

以下是这些运算符的使用示例。

```rust
assert_eq!(3 + 6, 9);
assert_eq!(5.5 - 1.25, 4.25);
assert_eq!(-5 * 14, -70);
assert_eq!(14 / 3, 4);
assert_eq!(100 % 7, 2);
assert_eq!(0b1010 & 0b1100, 0b1000);
assert_eq!(0b1010 | 0b1100, 0b1110);
assert_eq!(0b1010 ^ 0b1100, 0b110);
assert_eq!(13 << 3, 104);
assert_eq!(-10 >> 2, -3);
```

r[expr.cmp]
## 比较运算符

r[expr.cmp.syntax]
```grammar,expressions
ComparisonExpression ->
      Expression `==` Expression
    | Expression `!=` Expression
    | Expression `>` Expression
    | Expression `<` Expression
    | Expression `>=` Expression
    | Expression `<=` Expression
```

r[expr.cmp.intro]
比较运算符既为基本类型定义，也为标准库中的许多类型定义。

r[expr.cmp.paren-chaining]
串联比较运算符时需要使用圆括号。例如，表达式 `a == b == c` 是无效的，可以写成 `(a == b) == c`。

r[expr.cmp.trait]
与算术和逻辑运算符不同，用于重载这些运算符的 trait 更普遍地用于表明类型可以如何比较，并且以这些 trait 为约束的函数很可能会假定它们定义了实际的比较。标准库中的许多函数和宏随后可以使用该假定（尽管不是为了确保安全性）。

r[expr.cmp.place]
与上面的算术和逻辑运算符不同，这些运算符隐式地对其操作数进行共享借用，在[位置表达式上下文][place expression]中求值它们：

```rust
## let a = 1;
## let b = 1;
a == b;
// 等价于
::std::cmp::PartialEq::eq(&a, &b);
```

这意味着不必从操作数中移出。

r[expr.cmp.behavior]

| 符号 | 含义                     | 重载方法                   |
|--------|--------------------------|----------------------------|
| `==`   | 等于                     | `std::cmp::PartialEq::eq`  |
| `!=`   | 不等于                   | `std::cmp::PartialEq::ne`  |
| `>`    | 大于                     | `std::cmp::PartialOrd::gt` |
| `<`    | 小于                     | `std::cmp::PartialOrd::lt` |
| `>=`   | 大于或等于               | `std::cmp::PartialOrd::ge` |
| `<=`   | 小于或等于               | `std::cmp::PartialOrd::le` |

以下是比较运算符的使用示例。

```rust
assert!(123 == 123);
assert!(23 != -12);
assert!(12.5 > 12.2);
assert!([1, 2, 3] < [1, 3, 4]);
assert!('A' <= 'B');
assert!("World" >= "Hello");
```

r[expr.bool-logic]
## 惰性布尔运算符

r[expr.bool-logic.syntax]
```grammar,expressions
LazyBooleanExpression ->
      Expression `||` Expression
    | Expression `&&` Expression
```

r[expr.bool-logic.intro]
运算符 `||` 和 `&&` 可应用于布尔类型的操作数。`||` 运算符表示逻辑「或」，`&&` 运算符表示逻辑「与」。

r[expr.bool-logic.conditional-evaluation]
它们与 `|` 和 `&` 的不同之处在于：仅当左操作数尚未决定表达式的结果时，才求值右操作数。也就是说，`||` 仅在左操作数求值为 `false` 时才求值其右操作数，而 `&&` 仅在左操作数求值为 `true` 时才求值其右操作数。

```rust
let x = false || true; // true
let y = false && panic!(); // false，不求值 `panic!()`
```

r[expr.as]
## 类型转换表达式

r[expr.as.syntax]
```grammar,expressions
TypeCastExpression -> Expression `as` TypeNoBounds
```

r[expr.as.intro]
类型转换表达式用二元运算符 `as` 表示。

r[expr.as.result]
执行 `as` 表达式会将左侧的值转换为右侧的类型。

`as` 表达式的一个示例：

```rust
## fn sum(values: &[f64]) -> f64 { 0.0 }
## fn len(values: &[f64]) -> i32 { 0 }
fn average(values: &[f64]) -> f64 {
    let sum: f64 = sum(values);
    let size: f64 = len(values) as f64;
    sum / size
}
```

r[expr.as.coercions]
`as` 可用于显式执行[强制转换](../../type-system/07-type-coercions/)，以及下列额外转换。任何既不符合强制转换规则、也不对应表中某一项的转换都是编译器错误。此处 `*T` 表示 `*const T` 或 `*mut T`。`m` 在引用类型中表示可选的 `mut`，在指针类型中表示 `mut` 或 `const`。

| `e` 的类型            | `U`                   | `e as U` 执行的转换                                   |
|-----------------------|-----------------------|-------------------------------------------------------|
| 整数或浮点类型        | 整数或浮点类型        | [数值转换][expr.as.numeric]                       |
| 枚举                  | 整数类型              | [枚举转换][expr.as.enum]                             |
| `bool` 或 `char`      | 整数类型              | [基本类型到整数转换][expr.as.bool-char-as-int] |
| `u8`                  | `char`                | [`u8` 到 `char` 转换][expr.as.u8-as-char]             |
| `*T`                  | `*V`（当[兼容][expr.as.pointer]时） | [指针到指针转换][expr.as.pointer] |
| `*T` 其中 `T: Sized` | 整数类型              | [指针到地址转换][expr.as.pointer-as-int]     |
| 整数类型              | `*V` 其中 `V: Sized` | [地址到指针转换][expr.as.int-as-pointer]     |
| `&m₁ [T; n]`          | `*m₂ T` [^lessmut]    | 数组到指针转换                                 |
| `*m₁ [T; n]`          | `*m₂ T` [^lessmut]    | 数组到指针转换                                 |
| [函数项][Function item]       | [函数指针][Function pointer]    | 函数项到函数指针转换                |
| [函数项][Function item]       | `*V` 其中 `V: Sized` | 函数项到指针转换                         |
| [函数项][Function item]       | 整数                  | 函数项到地址转换                         |
| [函数指针][Function pointer]    | `*V` 其中 `V: Sized` | 函数指针到指针转换                      |
| [函数指针][Function pointer]    | 整数                  | 函数指针到地址转换                      |
| 闭包 [^no-capture] | 函数指针      | 闭包到函数指针转换                      |

[^lessmut]: 仅当 `m₁` 为 `mut` 或 `m₂` 为 `const` 时。允许将 `mut` 引用/指针转换为 `const` 指针。

[^no-capture]: 只有不捕获任何局部变量的闭包才能转换为函数指针。

### 语义

r[expr.as.numeric]
#### 数值转换

r[expr.as.numeric.int-same-size]
* 在两个相同大小的整数之间转换（例如 i32 -> u32）是无操作（Rust 对定宽整数的负值使用二进制补码）

  ```rust
  assert_eq!(42i8 as u8, 42u8);
  assert_eq!(-1i8 as u8, 255u8);
  assert_eq!(255u8 as i8, -1i8);
  assert_eq!(-1i16 as u16, 65535u16);
  ```

r[expr.as.numeric.int-truncation]
* 从较大整数转换到较小整数（例如 u32 -> u8）会截断

  ```rust
  assert_eq!(42u16 as u8, 42u8);
  assert_eq!(1234u16 as u8, 210u8);
  assert_eq!(0xabcdu16 as u8, 0xcdu8);

  assert_eq!(-42i16 as i8, -42i8);
  assert_eq!(1234u16 as i8, -46i8);
  assert_eq!(0xabcdi32 as i8, -51i8);
  ```

r[expr.as.numeric.int-extension]
* 从较小整数转换到较大整数（例如 u8 -> u32）会
    * 若源是无符号的则进行零扩展
    * 若源是有符号的则进行符号扩展

  ```rust
  assert_eq!(42i8 as i16, 42i16);
  assert_eq!(-17i8 as i16, -17i16);
  assert_eq!(0b1000_1010u8 as u16, 0b0000_0000_1000_1010u16, "Zero-extend");
  assert_eq!(0b0000_1010i8 as i16, 0b0000_0000_0000_1010i16, "Sign-extend 0");
  assert_eq!(0b1000_1010u8 as i8 as i16, 0b1111_1111_1000_1010u16 as i16, "Sign-extend 1");
  ```

r[expr.as.numeric.float-as-int]
* 从浮点数转换到整数会将浮点数向零舍入
    * `NaN` 将返回 `0`
    * 大于整数最大值的值，包括 `INFINITY`，会饱和到该整数类型的最大值。
    * 小于整数最小值的值，包括 `NEG_INFINITY`，会饱和到该整数类型的最小值。

  ```rust
  assert_eq!(42.9f32 as i32, 42);
  assert_eq!(-42.9f32 as i32, -42);
  assert_eq!(42_000_000f32 as i32, 42_000_000);
  assert_eq!(std::f32::NAN as i32, 0);
  assert_eq!(1_000_000_000_000_000f32 as i32, 0x7fffffffi32);
  assert_eq!(std::f32::NEG_INFINITY as i32, -0x80000000i32);
  ```

r[expr.as.numeric.int-as-float]
* 从整数转换到浮点数将产生最接近的可能浮点值 \*
    * 必要时，按 `roundTiesToEven` 模式舍入 \*\*\*
    * 溢出时，产生无穷大（符号与输入相同）
    * 注意：以当前的数值类型集合，溢出只可能发生在 `u128 as f32`，且仅当值大于或等于 `f32::MAX + (0.5 ULP)` 时

  ```rust
  assert_eq!(1337i32 as f32, 1337f32);
  assert_eq!(123_456_789i32 as f32, 123_456_790f32, "Rounded");
  assert_eq!(0xffffffff_ffffffff_ffffffff_ffffffff_u128 as f32, std::f32::INFINITY);
  ```

r[expr.as.numeric.float-widening]
* 从 f32 转换到 f64 是精确且无损的

  ```rust
  assert_eq!(1_234.5f32 as f64, 1_234.5f64);
  assert_eq!(std::f32::INFINITY as f64, std::f64::INFINITY);
  assert!((std::f32::NAN as f64).is_nan());
  ```

r[expr.as.numeric.float-narrowing]
* 从 f64 转换到 f32 将产生最接近的可能 f32 \*\*
    * 必要时，按 `roundTiesToEven` 模式舍入 \*\*\*
    * 溢出时，产生无穷大（符号与输入相同）

  ```rust
  assert_eq!(1_234.5f64 as f32, 1_234.5f32);
  assert_eq!(1_234_567_891.123f64 as f32, 1_234_567_890f32, "Rounded");
  assert_eq!(std::f64::INFINITY as f32, std::f32::INFINITY);
  assert!((std::f64::NAN as f32).is_nan());
  ```

\* 若硬件并不原生支持具有此舍入模式和溢出行为的整数到浮点转换，则这些转换可能会比预期更慢。

\*\* 若硬件并不原生支持具有此舍入模式和溢出行为的 f64 到 f32 转换，则这些转换可能会比预期更慢。

\*\*\* 按 IEEE 754-2008 &sect;4.3.1 的定义：选取最接近的浮点数；若恰好位于两个浮点数正中间，则选取最低有效位为偶数的那个。

r[expr.as.enum]
#### 枚举转换

r[expr.as.enum.discriminant]
将枚举转换为其判别式，必要时再进行数值转换。转换仅限于以下种类的枚举：

* [仅单元变体枚举][Unit-only enums]
* 没有[显式判别式][explicit discriminants]的[无字段枚举][Field-less enums]，或只有单元变体带有显式判别式的无字段枚举

```rust
enum Enum { A, B, C }
assert_eq!(Enum::A as i32, 0);
assert_eq!(Enum::B as i32, 1);
assert_eq!(Enum::C as i32, 2);
```

r[expr.as.enum.no-drop]
若枚举实现了 [`Drop`]，则不允许转换。

r[expr.as.bool-char-as-int]
#### 基本类型到整数转换

* `false` 转换为 `0`，`true` 转换为 `1`
* `char` 转换为其码点的值，必要时再进行数值转换。

```rust
assert_eq!(false as i32, 0);
assert_eq!(true as i32, 1);
assert_eq!('A' as i32, 65);
assert_eq!('Ö' as i32, 214);
```

r[expr.as.u8-as-char]
#### `u8` 到 `char` 转换

转换为具有对应码点的 `char`。

```rust
assert_eq!(65u8 as char, 'A');
assert_eq!(214u8 as char, 'Ö');
```

r[expr.as.pointer-as-int]
#### 指针到地址转换

将裸指针转换为整数会得到所引用内存的机器地址。若整数类型小于指针类型，地址可能被截断；使用 `usize` 可避免这种情况。

r[expr.as.int-as-pointer]
#### 地址到指针转换

将整数转换为裸指针会将该整数解释为内存地址，并产生指向该内存的指针。

> **警告**
> 这会与仍在开发中的 Rust 内存模型产生交互。
> 通过此转换获得的指针，即便按位等于某个有效指针，也可能受到额外限制。
> 若未遵守别名规则，解引用此类指针可能是[未定义行为][undefined behavior]。

一个健全的地址算术的简单示例：

```rust
let mut values: [i32; 2] = [1, 2];
let p1: *mut i32 = values.as_mut_ptr();
let first_address = p1 as usize;
let second_address = first_address + 4; // 4 == size_of::<i32>()
let p2 = second_address as *mut i32;
unsafe {
    *p2 += 1;
}
assert_eq!(values[1], 3);
```

r[expr.as.pointer]
#### 指针到指针转换

r[expr.as.pointer.behavior]
`*const T` / `*mut T` 可以按以下行为转换为 `*const U` / `*mut U`：

r[expr.as.pointer.sized]
- 若 `T` 与 `U` 都是定长的，则原样返回该指针。

  > [!EXAMPLE]
  > ```rust
  > let x: i32 = 42;
  > let p1: *const i32 = &x;
  > let p2: *const u8 = p1 as *const u8;
  > // 指针地址保持不变。
  > assert_eq!(p1 as usize, p2 as usize);
  > ```

r[expr.as.pointer.discard-metadata]
- 若 `T` 是不定长的而 `U` 是定长的，则该转换丢弃补全宽指针 `T` 的全部[元数据][metadata]，并产生由不定长指针的数据部分组成的瘦指针 `U`。

  > [!EXAMPLE]
  > ```rust
  > let slice: &[i32] = &[1, 2, 3];
  > let ptr: *const [i32] = slice as *const [i32];
  > // 从宽指针（*const [i32]）转换到瘦指针（*const i32），
  > // 丢弃长度元数据。
  > let data_ptr: *const i32 = ptr as *const i32;
  > assert_eq!(unsafe { *data_ptr }, 1);
  > ```

r[expr.as.pointer.unsized.unchanged]
- 若 `T` 与 `U` 都是不定长的，则指针同样原样返回。特别是，元数据被精确保留。仅当元数据按下列规则兼容时才能执行该转换：

r[expr.as.pointer.unsized.slice]
- 当 `T` 与 `U` 都是带切片元数据的不定长类型时，它们始终兼容。切片的元数据是元素个数，因此转换 `*[u16] -> *[u8]` 是合法的，但会导致字节数减半。

  > [!EXAMPLE]
  > ```rust
  > let slice: &[u16] = &[1, 2, 3];
  > let ptr: *const [u16] = slice as *const [u16];
  > let byte_ptr: *const [u8] = ptr as *const [u8];
  > assert_eq!(byte_ptr.len(), 3);
  > ```

r[expr.as.pointer.unsized.trait]
- 当 `T` 与 `U` 都是带 trait 对象元数据的不定长类型时，仅当以下全部成立时元数据才兼容：
  1. 主 trait 必须相同。

     > [!EXAMPLE]
     > ```rust,compile_fail,E0606
     > trait Foo {}
     > trait Bar {}
     > impl Foo for i32 {}
     > impl Bar for i32 {}
     >
     > let x: i32 = 42;
     > let ptr_foo: *const dyn Foo = &x as *const dyn Foo;
     > // 不能转换到不同的主 trait。
     > let ptr_bar: *const dyn Bar = ptr_foo as *const dyn Bar; // 错误
     > ```


  2. 可以去掉自动 trait。

     > [!EXAMPLE]
     > ```rust
     > trait Foo {}
     > struct S;
     > impl Foo for S {}
     > unsafe impl Send for S {}
     >
     > let s = S;
     > let ptr_send: *const (dyn Foo + Send) = &s;
     > // 去掉自动 trait。
     > let ptr_no_send: *const dyn Foo = ptr_send as *const dyn Foo;
     > ```


  3. 仅当自动 trait 是主 trait 的超 trait 时才可以添加。

     > [!EXAMPLE]
     > ```rust
     > trait Foo: Send {}
     > struct S;
     > impl Foo for S {}
     > unsafe impl Send for S {}
     >
     > let s = S;
     > let ptr_no_send: *const dyn Foo = &s;
     > // 添加自动 trait。
     > let ptr_send: *const (dyn Foo + Send) = ptr_no_send as *const (dyn Foo + Send);
     > ```
     >
     > ```rust,compile_fail,E0804
     > trait Foo {}
     > # struct S;
     > # impl Foo for S {}
     > # unsafe impl Send for S {}
     > #
     > # let s = S;
     > # let ptr_no_send: *const dyn Foo = &s;
     > // 同上，但 trait Foo 不以 Send 为超 trait。
     > let ptr_send: *const (dyn Foo + Send) = ptr_no_send as *const (dyn Foo + Send); // 错误
     > ```


  4. 尾随生命周期只能缩短。

     > [!EXAMPLE]
     > ```rust
     > trait Foo {}
     >
     > fn shorten_lifetime<'long: 'short, 'short>(
     >     ptr: *const (dyn Foo + 'long),
     > ) -> *const (dyn Foo + 'short) {
     >     // 允许缩短生命周期。
     >     ptr as *const (dyn Foo + 'short)
     > }
     > ```
     >
     > ```rust,compile_fail
     > trait Foo {}
     >
     > fn lengthen_lifetime<'long: 'short, 'short>(
     >     ptr: *const (dyn Foo + 'short),
     > ) -> *const (dyn Foo + 'long) {
     >     // 不允许转换到更长的生命周期。
     >     ptr as *const (dyn Foo + 'long) // 错误
     > }
     > ```

  5. 泛型（包括生命周期）和关联类型必须完全匹配。

     > [!EXAMPLE]
     > ```rust,compile_fail,E0606
     > trait Generic<T> {}
     > impl Generic<i32> for () {}
     > impl Generic<u32> for () {}
     >
     > let x = ();
     > let ptr_i32: *const dyn Generic<i32> = &x;
     > // 不能转换到不同的泛型参数。
     > let ptr_u32: *const dyn Generic<u32> = ptr_i32 as *const dyn Generic<u32>; // 错误
     > ```
     >
     > ```rust
     > trait HasType {
     >     type Output;
     > }
     >
     > trait Generic<'x, T> {}
     >
     > fn cast_via_associated<'a, 'b, A, B>(
     >     ptr: *const dyn Generic<'a, A::Output>,
     > ) -> *const dyn Generic<'b, B::Output>
     > where
     >     'a: 'b,
     >     'b: 'a,
     >     A: HasType,
     >     B: HasType<Output = A::Output>, // 强制相等
     > {
     >     ptr as *const dyn Generic<'b, B::Output>
     > }
     > ```



r[expr.as.pointer.unsized.compound]
- 当 `T` 或 `U` 是最后一个字段为不定长的结构体或元组类型时，它与其最后一个字段具有相同的元数据和兼容性规则。

  > [!EXAMPLE]
  > ```rust
  > struct Wrapper(u32, [u8]);
  >
  > let slice: &[u8] = &[1, 2, 3];
  > let ptr: *const [u8] = slice;
  >
  > // 转换到最后一个字段为不定长类型 `[u8]` 的结构体时，
  > // 元数据（长度 3）被保留。
  > let wrapper_ptr: *const Wrapper = ptr as *const Wrapper;
  >
  > // 再转换回去时同样保留。
  > let ptr_back: *const [u8] = wrapper_ptr as *const [u8];
  > assert_eq!(ptr_back.len(), 3);
  > ```

r[expr.assign]
## 赋值表达式

r[expr.assign.syntax]
```grammar,expressions
AssignmentExpression -> Expression `=` Expression
```

r[expr.assign.intro]
*赋值表达式*将一个值移入指定的位置。

r[expr.assign.assignee]
赋值表达式由一个[可变的][mutable][被赋值表达式][assignee expression]（即*被赋值操作数*）、等号（`=`），以及一个[值表达式][value expression]（即*被赋值为操作数*）组成。

r[expr.assign.behavior-basic]
最基本的形式中，被赋值表达式就是[位置表达式][place expression]，我们先讨论这种情况。

r[expr.assign.behavior-destructuring]
更一般的解构赋值情形在下文讨论，但那种情形总是分解为对位置表达式的依次赋值，后者可视为更根本的情形。

r[expr.assign.basic]
### 基本赋值

r[expr.assign.evaluation-order]
求值赋值表达式从求值其操作数开始。先求值被赋值为操作数，然后求值被赋值表达式。

r[expr.assign.destructuring-order]
对于解构赋值，被赋值表达式的子表达式按从左到右的顺序求值。

> **注意**
> 这与其他表达式不同，因为右操作数在左操作数之前求值。

r[expr.assign.drop-target]
然后，其效果是先[丢弃][dropping]被赋值位置上的值，除非该位置是未初始化的局部变量或局部变量的未初始化字段。

r[expr.assign.behavior]
接着，它将被赋的值[复制或移入][copies or moves]被赋值位置。

r[expr.assign.result]
赋值表达式始终产生[单元值][unit]。

示例：

```rust
let mut x = 0;
let y = 0;
x = y;
```

r[expr.assign.destructure]
### 解构赋值

r[expr.assign.destructure.intro]
解构赋值是变量声明中解构模式匹配的对应物，允许对元组或结构体等复杂值进行赋值。例如，我们可以交换两个可变变量：

```rust
let (mut a, mut b) = (0, 1);
// 使用解构赋值交换 `a` 和 `b`。
(b, a) = (a, b);
```

r[expr.assign.destructure.assignee]
与使用 `let` 的解构声明不同，由于语法歧义，模式不能出现在赋值的左侧。取而代之的是，一组与模式对应的表达式被指定为[被赋值表达式][assignee expression]，并允许出现在赋值的左侧。被赋值表达式随后被脱糖为模式匹配，后接依次赋值。

r[expr.assign.destructure.irrefutable]
脱糖后的模式必须是不可失败的：特别是，这意味着解构赋值只允许长度为编译期已知的切片模式，以及平凡切片 `[..]`。

脱糖方法很直接，最好通过示例来说明。

```rust
## struct Struct { x: u32, y: u32 }
## let (mut a, mut b) = (0, 0);
(a, b) = (3, 4);

[a, b] = [3, 4];

Struct { x: a, y: b } = Struct { x: 3, y: 4};

// 脱糖为：

{
    let (_a, _b) = (3, 4);
    a = _a;
    b = _b;
}

{
    let [_a, _b] = [3, 4];
    a = _a;
    b = _b;
}

{
    let Struct { x: _a, y: _b } = Struct { x: 3, y: 4};
    a = _a;
    b = _b;
}
```

r[expr.assign.destructure.repeat-ident]
并不禁止在单个被赋值表达式中多次使用同一标识符。

r[expr.assign.destructure.discard-value]
[下划线表达式][Underscore expressions]和空的[范围表达式][range expressions]可用于忽略某些值，而不绑定它们。

r[expr.assign.destructure.default-binding]
注意，默认绑定模式不适用于脱糖后的表达式。

r[expr.assign.destructure.tmp-scopes]
> **注意**
> 该脱糖会限制解构赋值中被赋值为操作数（右侧）的[临时作用域][temporary scope]。
>
> 在基本赋值中，[临时值][temporary]在外围临时作用域结束时被丢弃。在下面，那就是该语句。因此，赋值与使用是允许的。
>
> ```rust
> # fn temp() {}
> fn f<T>(x: T) -> T { x }
> let x;
> (x = f(&temp()), x); // 可以
> ```
>
> 相反，在解构赋值中，临时值在脱糖后的 `let` 语句结束时被丢弃。如下面所示，这发生在我们尝试对 `x` 赋值之前，因而失败。
>
> ```rust
> # fn temp() {}
> # fn f<T>(x: T) -> T { x }
> # let x;
> [x] = [f(&temp())]; // 错误
> ```
>
> 这脱糖为：
>
> ```rust
> # fn temp() {}
> # fn f<T>(x: T) -> T { x }
> # let x;
> {
>     let [_x] = [f(&temp())];
>     //                     ^
>     //      临时值在此处被丢弃。
>     x = _x; // 错误
> }
> ```

r[expr.assign.destructure.tmp-ext]
> **注意**
> 由于该脱糖，解构赋值的被赋值为操作数（右侧）是新引入的块内的[延长表达式][extending expression]。
>
> 在下面，由于[临时作用域][temporary scope]被延长到这个引入的块的末尾，赋值是允许的。
>
> ```rust
> # fn temp() {}
> # let x;
> [x] = [&temp()]; // 可以
> ```
>
> 这脱糖为：
>
> ```rust
> # fn temp() {}
> # let x;
> { let [_x] = [&temp()]; x = _x; } // 可以
> ```
>
> 然而，若我们尝试使用 `x`，即便在同一语句内，也会得到错误，因为[临时值][temporary]在这个引入的块结束时被丢弃。
>
> ```rust
> # fn temp() {}
> # let x;
> ([x] = [&temp()], x); // 错误
> ```
>
> 这脱糖为：
>
> ```rust
> # fn temp() {}
> # let x;
> (
>     {
>         let [_x] = [&temp()];
>         x = _x;
>     }, // <-- 临时值在此处被丢弃。
>     x, // 错误
> );
> ```

r[expr.compound-assign]
## 复合赋值表达式

r[expr.compound-assign.syntax]
```grammar,expressions
CompoundAssignmentExpression ->
      Expression `+=` Expression
    | Expression `-=` Expression
    | Expression `*=` Expression
    | Expression `/=` Expression
    | Expression `%=` Expression
    | Expression `&=` Expression
    | Expression `|=` Expression
    | Expression `^=` Expression
    | Expression `<<=` Expression
    | Expression `>>=` Expression
```

r[expr.compound-assign.intro]
*复合赋值表达式*将算术与逻辑二元运算符与赋值表达式相结合。

例如：

```rust
let mut x = 5;
x += 1;
assert!(x == 6);
```

复合赋值的语法是一个[可变][mutable][位置表达式][place expression]（即*被赋值操作数*），然后是运算符之一后接 `=` 组成的单个 token（中间无空白），再然后是一个[值表达式][value expression]（即*修改操作数*）。

r[expr.compound-assign.place]
与其他位置操作数不同，被赋值位置操作数必须是位置表达式。

r[expr.compound-assign.no-value]
尝试使用值表达式会是编译器错误，而不会将其提升为临时值。

r[expr.compound-assign.operand-order]
复合赋值表达式的求值取决于操作数的类型。

r[expr.compound-assign.primitives]
若在单态化之前即可知道两个操作数的类型都是基本类型，则先求值右侧，再求值左侧，然后将运算符应用于两侧的值，以修改左侧求值所得的位置。

```rust
## use core::{num::Wrapping, ops::AddAssign};
#
trait Equate {}
impl<T> Equate for (T, T) {}

fn f1(x: (u8,)) {
    let mut order = vec![];
    // 右侧先求值，因为两个操作数都是基本类型。
    { order.push(2); x }.0 += { order.push(1); x }.0;
    assert!(order.is_sorted());
}

fn f2(x: (Wrapping<u8>,)) {
    let mut order = vec![];
    // 左侧先求值，因为 `Wrapping<_>` 不是基本类型。
    { order.push(1); x }.0 += { order.push(2); (0u8,) }.0;
    assert!(order.is_sorted());
}

fn f3<T: AddAssign<u8> + Copy>(x: (T,)) where (T, u8): Equate {
    let mut order = vec![];
    // 左侧先求值，因为其中一个操作数是泛型参数，
    // 即便由于 where 子句约束，该泛型参数可以与基本类型合一。
    { order.push(1); x }.0 += { order.push(2); (0u8,) }.0;
    assert!(order.is_sorted());
}

fn main() {
    f1((0u8,));
    f2((Wrapping(0u8),));
    // 我们提供基本类型作为泛型实参，但这并不影响
    // `f3` 在单态化时的求值顺序。
    f3::<u8>((0u8,));
}
```

> **注意**
> 这很不寻常。在其他地方，从左到右求值才是常态。
>
> 更多示例见[求值顺序测试][eval order test]。

r[expr.compound-assign.trait]
否则，该表达式是使用该运算符对应 trait（见 [expr.arith-logic.behavior]）并将其方法以左侧为[接收者][receiver]、右侧为下一实参进行调用的语法糖。

例如，以下两条语句等价：

```rust
## use std::ops::AddAssign;
fn f<T: AddAssign + Copy>(mut x: T, y: T) {
    x += y; // 语句 1。
    x.add_assign(y); // 语句 2。
}
```

> **注意**
> 出人意料的是，进一步脱糖为完全限定方法调用并不等价，因为当通过[自动引用][autoref]取得对第一操作数的可变引用时，借用检查器具有特殊行为。
>
> ```rust
> # use std::ops::AddAssign;
> fn f<T: AddAssign + Copy>(mut x: T) {
>     // 此处我们将 `x` 同时用作左侧和右侧。因为调用 trait 方法
>     // 所需的对左侧的可变借用是由自动引用隐式取得的，所以这是可以的。
>     x += x; //~ 可以
>     x.add_assign(x); //~ 可以
> }
> ```
>
> ```rust
> # use std::ops::AddAssign;
> fn f<T: AddAssign + Copy>(mut x: T) {
>     // 我们不能把上面脱糖为下面这样：一旦为传递第一个实参
>     // 而对 `x` 进行可变借用，就不能再按值传递第二个实参 `x`，
>     // 因为该可变引用仍然存活。
>     <T as AddAssign>::add_assign(&mut x, x);
>     //~^ 错误：无法使用 `x`，因为它已被可变借用
> }
> ```
>
> ```rust
> # use std::ops::AddAssign;
> fn f<T: AddAssign + Copy>(mut x: T) {
>     // 同上。
>     (&mut x).add_assign(x);
>     //~^ 错误：无法使用 `x`，因为它已被可变借用
> }
> ```

r[expr.compound-assign.result]
与普通赋值表达式一样，复合赋值表达式始终产生[单元值][unit]。

> **警告**
> 避免编写依赖复合赋值中操作数求值顺序的代码，因为该顺序可能不寻常且令人惊讶。

[`Box`]: ../special-types-and-traits.md#boxt
[`Try`]: core::ops::Try
[autoref]: expr.method.candidate-receivers-refs
[copies or moves]: ../expressions.md#moved-and-copied-types
[dropping]: ../destructors.md
[eval order test]: https://github.com/rust-lang/rust/blob/1.58.0/src/test/ui/expr/compound-assignment/eval-order.rs
[explicit discriminants]: ../items/enumerations.md#explicit-discriminants
[extending expression]: destructors.scope.lifetime-extension.exprs
[field-less enums]: ../items/enumerations.md#field-less-enum
[grouped expression]: grouped-expr.md
[literal expression]: literal-expr.md#integer-literal-expressions
[logical and]: ../types/boolean.md#logical-and
[logical not]: ../types/boolean.md#logical-not
[logical or]: ../types/boolean.md#logical-or
[logical xor]: ../types/boolean.md#logical-xor
[metadata]: dynamic-sized.pointer-types
[moved from]: expr.move.movable-place
[mutable]: ../expressions.md#mutability
[place expression]: ../expressions.md#place-expressions-and-value-expressions
[assignee expression]: ../expressions.md#place-expressions-and-value-expressions
[undefined behavior]: ../behavior-considered-undefined.md
[unit]: ../types/tuple.md
[Unit-only enums]: ../items/enumerations.md#unit-only-enum
[value expression]: ../expressions.md#place-expressions-and-value-expressions
[temporary lifetime extension]: destructors.scope.lifetime-extension
[temporary scope]: destructors.scope.temporary
[temporary value]: ../expressions.md#temporaries
[float-float]: https://github.com/rust-lang/rust/issues/15536
[Function pointer]: ../types/function-pointer.md
[Function item]: ../types/function-item.md
[receiver]: expr.method.intro
[temporary]: expr.temporary
[undefined behavior]: ../behavior-considered-undefined.md
[Underscore expressions]: ./underscore-expr.md
[range expressions]: ./range-expr.md
