+++
title = "07-类型强制转换"
date = 2026-08-18T08:45:00+08:00
weight = 90
type = "docs"
description = "类型强制转换 — The Rust Reference"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Reference](https://doc.rust-lang.org/reference/)

> 原文链接: [https://doc.rust-lang.org/reference/type-coercions.html](https://doc.rust-lang.org/reference/type-coercions.html)

r[coerce]
# 类型强制转换

r[coerce.intro]
**类型强制转换**是隐式改变值的类型的操作。它们在特定位置自动发生，并且实际会发生强制转换的类型受到严格限制。

r[coerce.as]
强制转换所允许的任何转换也可以由[类型转换运算符][type cast operator] `as` 显式执行。

强制转换最初在 [RFC 401] 中定义，并在 [RFC 1558] 中扩展。

r[coerce.site]
## 强制转换位点

r[coerce.site.intro]
强制转换只能发生在程序中的某些强制转换位点；这些通常是期望类型显式给出、或可以从显式类型传播得出（无需类型推断）的地方。可能的强制转换位点有：

r[coerce.site.let]
* 给出了显式类型的 `let` 语句。

   例如，在下面的代码中，`&mut 42` 被强制转换为类型 `&i8`：

   ```rust
   let _: &i8 = &mut 42;
   ```

r[coerce.site.value]
* `static` 和 `const` 项声明（类似于 `let` 语句）。

r[coerce.site.argument]
* 函数调用的实参

  被强制转换的值是实际参数，它被强制转换为形式参数的类型。

  例如，在下面的代码中，`&mut 42` 被强制转换为类型 `&i8`：

  ```rust
  fn bar(_: &i8) { }

  fn main() {
      bar(&mut 42);
  }
  ```

  对于方法调用，接收者（`self` 参数）类型的强制转换方式不同，细节参见[方法调用表达式][method-call expressions]的文档。

r[coerce.site.constructor]
* 结构体、联合体或枚举变体字段的实例化

  例如，在下面的代码中，`&mut 42` 被强制转换为类型 `&i8`：

  ```rust
  struct Foo<'a> { x: &'a i8 }

  fn main() {
      Foo { x: &mut 42 };
  }
  ```

r[coerce.site.return]
* 函数结果——块的最后一行（若不以分号结尾），或 `return` 语句中的任何表达式

  例如，在下面的代码中，`x` 被强制转换为类型 `&dyn Display`：

  ```rust
  use std::fmt::Display;
  fn foo(x: &u32) -> &dyn Display {
      x
  }
  ```

r[coerce.site.assignment]
* 赋值表达式中的被赋值为操作数

  例如，在下面的代码中，`y` 被强制转换为类型 `&i8`：
  ```rust
  let mut x = &0i8;
  let y = &mut 42i8;
  x = y;
  ```

r[coerce.site.subexpr]
若这些强制转换位点中的表达式是强制转换传播表达式，则该表达式中的相关子表达式也是强制转换位点。传播会从这些新的强制转换位点递归进行。传播表达式及其相关子表达式是：

r[coerce.site.array]
* 数组字面量，其中数组类型为 `[U; n]`。数组字面量中的每个子表达式都是向类型 `U` 强制转换的位点。

r[coerce.site.repeat]
* 使用重复语法的数组字面量，其中数组类型为 `[U; n]`。被重复的子表达式是向类型 `U` 强制转换的位点。

r[coerce.site.tuple]
* 元组，其中元组是向类型 `(U_0, U_1, ..., U_n)` 强制转换的位点。每个子表达式是向相应类型强制转换的位点，例如第零个子表达式是向类型 `U_0` 强制转换的位点。

r[coerce.site.parenthesis]
* 括号括起的子表达式（`(e)`）：若该表达式的类型为 `U`，则该子表达式是向 `U` 强制转换的位点。

r[coerce.site.block]
* 块：若块的类型为 `U`，则块中的最后一个表达式（若不以分号结尾）是向 `U` 强制转换的位点。这包括作为控制流语句一部分的块，例如 `if`/`else`，若该块具有已知类型。

r[coerce.types]
## 强制转换类型

r[coerce.types.intro]
以下类型之间允许强制转换：

r[coerce.types.reflexive]
* 若 `T` 是 `U` 的[子类型][subtype]，则 `T` 到 `U`（*自反情形*）

r[coerce.types.transitive]
* `T_1` 到 `T_3`，其中 `T_1` 强制转换为 `T_2` 且 `T_2` 强制转换为 `T_3`（*传递情形*）

    注意这尚未得到完全支持。

r[coerce.types.mut-reborrow]
* `&mut T` 到 `&T`

r[coerce.types.mut-pointer]
* `*mut T` 到 `*const T`

r[coerce.types.ref-to-pointer]
* `&T` 到 `*const T`

r[coerce.types.mut-to-pointer]
* `&mut T` 到 `*mut T`

r[coerce.types.deref]
* 若 `T` 实现 `Deref<Target = U>`，则 `&T` 或 `&mut T` 到 `&U`。例如：

  ```rust
  use std::ops::Deref;

  struct CharContainer {
      value: char,
  }

  impl Deref for CharContainer {
      type Target = char;

      fn deref<'a>(&'a self) -> &'a char {
          &self.value
      }
  }

  fn foo(arg: &char) {}

  fn main() {
      let x = &mut CharContainer { value: 'y' };
      foo(x); //&mut CharContainer 被强制转换为 &char。
  }
  ```

r[coerce.types.deref-mut]
* 若 `T` 实现 `DerefMut<Target = U>`，则 `&mut T` 到 `&mut U`。

r[coerce.types.unsize]
* TyCtor(`T`) 到 TyCtor(`U`)，其中 TyCtor(`T`) 是以下之一
    - `&T`
    - `&mut T`
    - `*const T`
    - `*mut T`
    - `Box<T>`

    并且 `U` 可以通过[不定大小强制转换](#unsized-coercions)从 `T` 得到。

    <!--将来，coerce_inner 将递归地扩展到元组和
    结构体。此外，将添加从子 trait 到超 trait 的强制转换。
    更多细节参见 [RFC 401]。-->

r[coerce.types.fn]
* 函数项类型到 `fn` 指针

r[coerce.types.closure]
* 不捕获的闭包到 `fn` 指针

r[coerce.types.never]
* `!` 到任何 `T`

r[coerce.unsize]
### 不定大小强制转换

r[coerce.unsize.intro]
以下强制转换称为 `unsized coercions`（不定大小强制转换），因为它们涉及将类型转换为不定大小类型，并且在上述少数其他强制转换不允许的情形中也是允许的。它们仍然可以发生在任何其他可以发生强制转换的地方。

r[coerce.unsize.trait]
两个 trait，[`Unsize`] 和 [`CoerceUnsized`]，用于辅助这一过程并将其暴露给库使用。以下强制转换是内建的，并且若 `T` 可以通过其中之一强制转换为 `U`，则会为 `T` 提供 `Unsize<U>` 的实现：

r[coerce.unsize.slice]
* `[T; n]` 到 `[T]`。

r[coerce.unsize.trait-object]
* `T` 到 `dyn U`，当 `T` 实现 `U + Sized`，且 `U` 是 [dyn 兼容][dyn compatible]的。

r[coerce.unsize.trait-upcast]
* `dyn T` 到 `dyn U`，当 `U` 是 `T` 的[超 trait][supertraits]之一。
    * 这允许去掉自动 trait，即允许 `dyn T + Auto` 到 `dyn U`。
    * 若主 trait 将自动 trait 作为超 trait，则这允许添加自动 trait，即给定 `trait T: U + Send {}`，允许 `dyn T` 到 `dyn T + Send` 或到 `dyn U + Send` 的强制转换。

r[coerce.unsized.composite]
* `Foo<..., T, ...>` 到 `Foo<..., U, ...>`，当：
    * `Foo` 是结构体。
    * `T` 实现 `Unsize<U>`。
    * `Foo` 的最后一个字段的类型涉及 `T`。
    * 若该字段的类型为 `Bar<T>`，则 `Bar<T>` 实现 `Unsize<Bar<U>>`。
    * T 不是任何其他字段类型的一部分。

r[coerce.unsized.pointer]
此外，当 `T` 实现 `Unsize<U>` 或 `CoerceUnsized<Foo<U>>` 时，类型 `Foo<T>` 可以实现 `CoerceUnsized<Foo<U>>`。这使它可以提供到 `Foo<U>` 的不定大小强制转换。

> **注意**
> 尽管不定大小强制转换的定义及其实现已经稳定，这些 trait 本身尚未稳定，因此还不能在稳定版 Rust 中直接使用。

r[coerce.least-upper-bound]
## 最小上界强制转换

r[coerce.least-upper-bound.intro]
在某些上下文中，编译器必须将多种类型强制转换到一起，以尝试找到最一般的类型。这称为「最小上界」（Least Upper Bound）强制转换。LUB 强制转换仅用于以下情形：

+ 为一系列 if 分支找到公共类型。
+ 为一系列 match 分支找到公共类型。
+ 为数组元素找到公共类型。
+ 在 break 操作数和最终块操作数之间，为[带标签块表达式][labeled block expression]找到公共类型。
+ 在 break 操作数之间，为[带 break 表达式的 `loop` 表达式][`loop` expression with break expressions]找到公共类型。
+ 为带有多个 return 语句的闭包确定返回类型。
+ 为带有多个 return 语句的函数检查返回类型。

r[coerce.least-upper-bound.target]
在每一种这样的情形中，都有一组类型 `T0..Tn` 需要被共同强制转换为某个起始时未知的目标类型 `T_t`。

r[coerce.least-upper-bound.computation]
LUB 强制转换的计算是迭代进行的。目标类型 `T_t` 开始时为类型 `T0`。对于每个新类型 `Ti`，我们考虑

r[coerce.least-upper-bound.computation-identity]
+ 若 `Ti` 可以强制转换为当前目标类型 `T_t`，则不做改变。

r[coerce.least-upper-bound.computation-replace]
+ 否则，检查 `T_t` 是否可以强制转换为 `Ti`；若可以，则将 `T_t` 改为 `Ti`。（此检查还取决于到目前为止所考虑的所有源表达式是否具有隐式强制转换。）

r[coerce.least-upper-bound.computation-unify]
+ 若不可以，则尝试计算 `T_t` 和 `Ti` 的共同超类型，它将成为新的目标类型。

### 示例：

```rust
## let (a, b, c) = (0, 1, 2);
// 对于 if 分支
let bar = if true {
    a
} else if false {
    b
} else {
    c
};

// 对于 match 分支
let baw = match 42 {
    0 => a,
    1 => b,
    _ => c,
};

// 对于数组元素
let bax = [a, b, c];

// 对于带有多个 return 语句的闭包
let clo = || {
    if true {
        a
    } else if false {
        b
    } else {
        c
    }
};
let baz = clo();

// 对于带有多个 return 语句的函数的类型检查
fn foo() -> i32 {
    let (a, b, c) = (0, 1, 2);
    match 42 {
        0 => a,
        1 => b,
        _ => c,
    }
}
```

在这些例子中，`ba*` 的类型通过 LUB 强制转换找到。并且编译器在处理函数 `foo` 时检查 `a`、`b`、`c` 的 LUB 强制转换结果是否为 `i32`。

### 注意事项

这一描述显然是非正式的。使其更精确预计将作为更精确地规定 Rust 类型检查器的总体工作的一部分进行。

[RFC 401]: https://github.com/rust-lang/rfcs/blob/master/text/0401-coercions.md
[RFC 1558]: https://github.com/rust-lang/rfcs/blob/master/text/1558-closure-to-fn-coercion.md
[subtype]: subtyping.md
[dyn compatible]: items/traits.md#dyn-compatibility
[type cast operator]: expressions/operator-expr.md#type-cast-expressions
[`Unsize`]: std::marker::Unsize
[`CoerceUnsized`]: std::ops::CoerceUnsized
[labeled block expression]: expr.loop.block-labels
[`loop` expression with break expressions]: expr.loop.break-value
[method-call expressions]: expressions/method-call-expr.md
[supertraits]: items/traits.md#supertraits
