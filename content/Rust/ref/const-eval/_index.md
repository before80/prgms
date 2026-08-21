+++
title = "第18章 常量求值"
date = 2026-08-18T08:45:00+08:00
weight = 112
type = "docs"
description = "常量求值 — The Rust Reference"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Reference](https://doc.rust-lang.org/reference/)

> 原文链接: [https://doc.rust-lang.org/reference/const_eval.html](https://doc.rust-lang.org/reference/const_eval.html)

r[const-eval]
# 常量求值

r[const-eval.intro]
常量求值是在编译期间计算[表达式][expressions]结果的过程。只有全部表达式的一个子集可以在编译期求值。

r[const-eval.const-expr]
## 常量表达式

r[const-eval.const-expr.intro]
某些形式的表达式称为常量表达式，可以在编译期求值。

r[const-eval.const-expr.const-context]
[常量上下文][const context]中的表达式必须是常量表达式。

r[const-eval.const-expr.evaluation]
常量上下文中的表达式总是在编译期求值。

r[const-eval.const-expr.runtime-context]
在常量上下文之外，常量表达式*可以*在编译期求值，但不保证如此。

r[const-eval.const-expr.error]
诸如越界[数组索引][array indexing]或[溢出][overflow]之类的行为，若该值必须在编译期求值（即在常量上下文中），则为编译器错误。否则，这些行为是警告，但很可能在运行时 panic。

r[const-eval.const-expr.list]
下列表达式是常量表达式，只要其任何操作数也是常量表达式，并且不会导致运行任何 [`Drop::drop`][destructors] 调用。

r[const-eval.const-expr.literal]
* [字面量][Literals]。

r[const-eval.const-expr.parameter]
* [常量参数][Const parameters]。

r[const-eval.const-expr.path-item]
* 指向[函数][functions]与[常量][constants]的[路径][Paths]。不允许递归定义常量。

r[const-eval.const-expr.path-static]
* 指向[静态项][statics]的路径，带有以下限制：
  * 在任何常量求值上下文中都不允许对 `static` 项写入。
  * 在任何常量求值上下文中都不允许从 `extern` 静态项读取。
  * 若求值*并非*在 `static` 项的初始化器中进行，则不允许从任何可变 `static` 读取。可变 `static` 是 `static mut` 项，或具有内部可变类型的 `static` 项。

  这些要求仅在常量被求值时检查。换言之，只要此类访问从未被执行，就允许它们在常量上下文中语法上出现。

r[const-eval.const-expr.tuple]
* [元组表达式][Tuple expressions]。

r[const-eval.const-expr.array]
* [数组表达式][Array expressions]。

r[const-eval.const-expr.constructor]
* [结构体表达式][Struct expressions]。

r[const-eval.const-expr.block]
* [块表达式][Block expressions]，包括 `unsafe` 与 `const` 块。
    * [let 语句][let statements]以及因此不可反驳的[模式][patterns]，包括可变绑定
    * [赋值表达式][assignment expressions]
    * [复合赋值表达式][compound assignment expressions]
    * [表达式语句][expression statements]

r[const-eval.const-expr.field]
* [字段表达式][Field expressions]。

r[const-eval.const-expr.index]
* [数组与切片索引表达式][array indexing]，其中索引为 `usize`。

r[const-eval.const-expr.range]
* [范围表达式][Range expressions]。

r[const-eval.const-expr.closure]
* 不从环境捕获变量的[闭包表达式][Closure expressions]。

r[const-eval.const-expr.builtin-arith-logic]
* 用于整数与浮点类型、`bool` 以及 `char` 的内建[取反][negation]、[算术][arithmetic]、[逻辑][logical]、[比较][comparison]或[惰性布尔][lazy boolean]运算符。

r[const-eval.const-expr.borrows]
* 所有形式的[借用][borrow]，包括裸借用，但下列情形除外：临时作用域会被延长（见[临时生命周期延长][temporary lifetime extension]）至程序结束，并且该借用是：
  * 可变借用。
  * 对结果具有[内部可变性][interior mutability]的值的共享借用。

  ```rust,compile_fail,E0764
  // 由于处于尾部位置，此借用会将该临时值的作用域
  // 延长至程序结束。由于该借用是可变的，
  // 这在常量表达式中是不允许的。
  const C: &u8 = &mut 0; // ERROR not allowed
  ```

  ```rust,compile_fail,E0764
  // Const 块类似于 `const` 项的初始化器。
  let _: &u8 = const { &mut 0 }; // ERROR not allowed
  ```

  ```rust,compile_fail,E0492
  # use core::sync::atomic::AtomicU8;
  // 这是不允许的，因为 1) 临时作用域被延长至
  // 程序结束，且 2) 该临时值具有内部可变性。
  const C: &AtomicU8 = &AtomicU8::new(0); // ERROR not allowed
  ```

  ```rust,compile_fail,E0492
  # use core::sync::atomic::AtomicU8;
  // 同上。
  let _: &_ = const { &AtomicU8::new(0) }; // ERROR not allowed
  ```

  ```rust
  # #![allow(static_mut_refs)]
  // 即便此借用是可变的，它也不是临时值的借用，
  // 因此是允许的。
  const C: &u8 = unsafe { static mut S: u8 = 0; &mut S }; // OK
  ```

  ```rust
  # use core::sync::atomic::AtomicU8;
  // 即便此借用是对具有内部可变性的值的借用，
  // 它也不是临时值的借用，因此是允许的。
  const C: &AtomicU8 = {
      static S: AtomicU8 = AtomicU8::new(0); &S // OK
  };
  ```

  ```rust
  # use core::sync::atomic::AtomicU8;
  // 对内部可变临时值的此共享借用是允许的，
  // 因为其作用域未被延长。
  const C: () = { _ = &AtomicU8::new(0); }; // OK
  ```

  ```rust
  // 即便该借用是可变的，且由于提升该临时值存活至
  // 程序结束，这也是允许的，因为该借用不在尾部位置，
  // 因此临时值的作用域不会经由临时生命周期延长而被延长。
  const C: () = { let _: &'static mut [u8] = &mut []; }; // OK
  //                                              ~~
  //                                     被提升的临时值。
  ```

  > [!NOTE]
  > 换言之——关注允许什么而非不允许什么——在[常量上下文][const context]中，对内部可变数据的共享借用以及可变借用，仅当被借用的[place 表达式][place expression]是*瞬态的*、*间接的*或*静态的*时才被允许。
  >
  > 若 place 表达式是当前常量上下文的局部变量，或其临时作用域包含在当前常量上下文内的表达式，则它是*瞬态的*。
  >
  > ```rust
  > // 该借用是对初始化器局部变量的借用，因此
  > // 此 place 表达式是瞬态的。
  > const C: () = { let mut x = 0; _ = &mut x; };
  > ```
  >
  > ```rust
  > // 该借用是对作用域未被延长的临时值的借用，
  > // 因此此 place 表达式是瞬态的。
  > const C: () = { _ = &mut 0u8; };
  > ```
  >
  > ```rust
  > // 当临时值被提升但生命周期未延长时，其
  > // place 表达式仍被视为瞬态。
  > const C: () = { let _: &'static mut [u8] = &mut []; };
  > ```
  >
  > 若 place 表达式是[解引用表达式][dereference expression]，则它是*间接的*。
  >
  > ```rust
  > const C: () = { _ = &mut *(&mut 0); };
  > ```
  >
  > 若 place 表达式是 `static` 项，则它是*静态的*。
  >
  > ```rust
  > # #![allow(static_mut_refs)]
  > const C: &u8 = unsafe { static mut S: u8 = 0; &mut S };
  > ```

  > [!NOTE]
  > 这些规则的一个令人惊讶的后果是我们允许这样，
  >
  > ```rust
  > const C: &[u8] = { let x: &mut [u8] = &mut []; x }; // OK
  > //                                    ~~~~~~~
  > // 空数组即便在可变借用之后也会被提升。
  > ```
  >
  > 但禁止类似的代码：
  >
  > ```rust,compile_fail,E0764
  > const C: &[u8] = &mut []; // ERROR
  > //               ~~~~~~~
  > //           尾部表达式。
  > ```
  >
  > 二者的区别在于：在前者中，空数组被[提升][promoted]，但其作用域不经历[临时生命周期延长][temporary lifetime extension]，因此我们将[place 表达式][place expression]视为瞬态（即便提升之后该 place 确实存活至程序结束）。在后者中，空数组临时值的作用域确实经历生命周期延长，因此因对生命周期已延长的临时值的可变借用（从而借用了非瞬态 place 表达式）而被拒绝。
  >
  > 效果令人惊讶，因为在这种情况下，临时生命周期延长反而使能通过编译的代码变少。
  >
  > 更多细节见 [issue #143129](https://github.com/rust-lang/rust/issues/143129)。

r[const-eval.const-expr.deref]
* [解引用表达式][Dereference expressions]。

  ```rust,no_run
  # use core::cell::UnsafeCell;
  const _: u8 = unsafe {
      let x: *mut u8 = &raw mut *&mut 0;
      //                        ^^^^^^^
      //             可变引用的解引用。
      *x = 1; // 可变指针的解引用。
      *(x as *const u8) // 常量指针的解引用。
  };
  const _: u8 = unsafe {
      let x = &UnsafeCell::new(0);
      *x.get() = 1; // 内部可变值的变异。
      *x.get()
  };
  ```

r[const-eval.const-expr.group]

* [分组][Grouped]表达式。

r[const-eval.const-expr.cast]
* [强制转换][Cast]表达式，但下列除外：
  * 指针到地址的强制转换，以及
  * 函数指针到地址的强制转换。

r[const-eval.const-expr.const-fn]
* [常量函数][const functions]与常量方法的调用。

r[const-eval.const-expr.loop]
* [loop] 与 [while] 表达式。

r[const-eval.const-expr.if-match]
* [if] 与 [match] 表达式。

r[const-eval.const-context]
## 常量上下文
[const context]: #const-context

r[const-eval.const-context.def]
_常量上下文_ 是下列之一：

r[const-eval.const-context.array-length]
* [数组类型长度表达式][Array type length expressions]

r[const-eval.const-context.repeat-length]
* [数组重复长度表达式][array expressions]

r[const-eval.const-context.init]
* 下列项的初始化器
  * [常量][constants]
  * [静态项][statics]
  * [枚举判别式][enum discriminants]

r[const-eval.const-context.generic]
* [常量泛型实参][const generic argument]

r[const-eval.const-context.block]
* [const 块][const block]

r[const-eval.const-context.outer-generics]
数组类型长度表达式、数组重复长度表达式以及常量泛型实参在使用外部泛型参数方面受到限制：此类表达式必须要么是单个常量泛型参数，要么是不引用任何泛型参数的表达式。

r[const-eval.const-fn]
## 常量函数

r[const-eval.const-fn.intro]
_常量函数_ 是可以从常量上下文调用的函数。它用 `const` 限定符定义，也包括[元组结构体][tuple struct]与[元组枚举变体][tuple enum variant]构造函数。

> [!EXAMPLE]
> ```rust
> const fn square(x: i32) -> i32 { x * x }
>
> const VALUE: i32 = square(12);
> ```

r[const-eval.const-fn.const-context]
从常量上下文调用时，常量函数由编译器在编译期解释。解释发生在编译目标的环境中，而非宿主环境。因此，若你针对 `32` 位系统编译，则 `usize` 是 `32` 位，与你是在 `64` 位还是 `32` 位系统上构建无关。

r[const-eval.const-fn.outside-context]
当从常量上下文之外调用常量函数时，其行为与没有 `const` 限定符时相同。

r[const-eval.const-fn.body-restriction]
常量函数的函数体只能使用[常量表达式][constant expressions]。

r[const-eval.const-fn.async]
不允许常量函数是 [async] 的。

r[const-eval.const-fn.type-restrictions]
常量函数的参数类型与返回类型受限于与常量上下文兼容的那些类型。
<!-- TODO: Define the type restrictions. -->

[arithmetic]:           expressions/operator-expr.md#arithmetic-and-logical-binary-operators
[array expressions]:    expressions/array-expr.md
[array indexing]:       expressions/array-expr.md#array-and-slice-indexing-expressions
[array type length expressions]: types/array.md
[assignment expressions]: expressions/operator-expr.md#assignment-expressions
[async]:                items/functions.md#async-functions
[compound assignment expressions]: expressions/operator-expr.md#compound-assignment-expressions
[block expressions]:    expressions/block-expr.md
[borrow]:               expressions/operator-expr.md#borrow-operators
[cast]:                 expressions/operator-expr.md#type-cast-expressions
[closure expressions]:  expressions/closure-expr.md
[comparison]:           expressions/operator-expr.md#comparison-operators
[const block]:          expressions/block-expr.md#const-blocks
[const functions]:      items/functions.md#const-functions
[const generic argument]: items/generics.md#const-generics
[const generic parameters]: items/generics.md#const-generics
[constant expressions]: #constant-expressions
[constants]:            items/constant-items.md
[Const parameters]:     items/generics.md
[dereference expression]: expr.deref
[dereference expressions]: expr.deref
[destructors]:          destructors.md
[enum discriminants]:   items/enumerations.md#discriminants
[expression statements]: statements.md#expression-statements
[expressions]:          expressions.md
[`extern` statics]:     items/external-blocks.md#statics
[field expressions]:    expressions/field-expr.md
[functions]:            items/functions.md
[grouped]:              expressions/grouped-expr.md
[interior mutability]:  interior-mutability.md
[if]:                   expressions/if-expr.md#if-expressions
[lazy boolean]:         expressions/operator-expr.md#lazy-boolean-operators
[let statements]:       statements.md#let-statements
[literals]:             expressions/literal-expr.md
[logical]:              expressions/operator-expr.md#arithmetic-and-logical-binary-operators
[loop]:                 expressions/loop-expr.md#infinite-loops
[match]:                expressions/match-expr.md
[negation]:             expressions/operator-expr.md#negation-operators
[overflow]:             expressions/operator-expr.md#overflow
[paths]:                expressions/path-expr.md
[patterns]:             patterns.md
[place expression]:     expr.place-value.place-memory-location
[promoted expression]:  destructors.md#constant-promotion
[promoted]:             destructors.md#constant-promotion
[range expressions]:    expressions/range-expr.md
[statics]:              items/static-items.md
[Struct expressions]:   expressions/struct-expr.md
[temporary lifetime extension]: destructors.scope.lifetime-extension
[tuple enum variant]:   items/enumerations.md
[tuple expressions]:    expressions/tuple-expr.md
[tuple struct]:         items/structs.md
[while]:                expressions/loop-expr.md#predicate-loops
