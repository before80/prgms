+++
title = "04-函数"
date = 2026-08-18T08:45:00+08:00
weight = 21
type = "docs"
description = "函数 — The Rust Reference"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Reference](https://doc.rust-lang.org/reference/)

> 原文链接: [https://doc.rust-lang.org/reference/items/functions.html](https://doc.rust-lang.org/reference/items/functions.html)

r[items.fn]
# 函数

r[items.fn.syntax]
```grammar,items
Function ->
    FunctionQualifiers `fn` IDENTIFIER GenericParams?
        `(` FunctionParameters? `)`
        FunctionReturnType? WhereClause?
        ( BlockExpression | `;` )

FunctionQualifiers -> `const`? `async`?[^async-edition] ItemSafety?[^extern-qualifiers] (`extern` Abi?)?

ItemSafety -> `safe`[^extern-safe] | `unsafe`

Abi -> STRING_LITERAL | RAW_STRING_LITERAL

FunctionParameters ->
      SelfParam `,`?
    | (SelfParam `,`)? FunctionParam (`,` FunctionParam)* `,`?

SelfParam -> OuterAttribute* ( ShorthandSelf | TypedSelf )

ShorthandSelf -> (`&` | `&` Lifetime)? `mut`? `self`

TypedSelf -> `mut`? `self` `:` Type

FunctionParam -> OuterAttribute* ( FunctionParamPattern | `...` | Type[^fn-param-2015] )

FunctionParamPattern -> PatternNoTopAlt `:` ( Type | `...` )

FunctionReturnType -> `->` Type
```

[^async-edition]: 2015 edition 不允许使用 `async` 限定符。

[^extern-safe]: `safe` 函数限定符在语义上只允许出现在 `extern` 块内。

[^extern-qualifiers]: *适用于早于 Rust 2024 的 edition*：在 `extern` 块内，只有当 `extern` 被限定为 `unsafe` 时，才允许使用 `safe` 或 `unsafe` 函数限定符。

[^fn-param-2015]: 仅有类型的函数参数只允许出现在 2015 edition 中 [trait 项][trait item]的关联函数里。

r[items.fn.intro]
*函数*由一个[块][block]（即函数的*函数体*）、一个名称、一组参数以及一个输出类型组成。除名称外，这些都是可选的。

r[items.fn.namespace]
函数用关键字 `fn` 声明，它在其所在模块或块的[值命名空间][value namespace]中定义给定名称。

r[items.fn.signature]
函数可以声明一组作为参数的*输入*[变量][variables]，调用者通过它们把实参传入函数，以及函数完成时返回给调用者的值的*输出*[类型][type]。

r[items.fn.implicit-return]
若未显式声明输出类型，则为[单元类型][unit type]。

r[items.fn.fn-item-type]
被引用时，*函数*产生对应[零大小][zero-sized][*函数项类型*][*function item type*]的一等*值*；调用该值会直接调用该函数。

例如，这是一个简单函数：

```rust
fn answer_to_life_the_universe_and_everything() -> i32 {
    return 42;
}
```

r[items.fn.safety-qualifiers]
`safe` 函数在语义上只允许在 [`extern` 块][`extern` block]中使用。

r[items.fn.params]
## 函数参数

r[items.fn.params.intro]
函数参数是不可反驳[模式][patterns]，因此任何在无 `else` 的 `let` 绑定中合法的模式也可以作为参数：

```rust
fn first((value, _): (i32, i32)) -> i32 { value }
```

r[items.fn.params.self-pat]
若第一个参数是 [SelfParam]，则表明该函数是一个[方法][method]。

r[items.fn.params.self-restriction]
带有 self 参数的函数只能作为 [trait] 或[实现][implementation]中的[关联函数][associated function]出现。

r[items.fn.params.varargs]
带有 `...` token 的参数表示 [C 可变参数函数][C-variadic function]，并且只能用作最后一个参数。在 [`extern` 块][`extern` block]中的函数声明里，C 可变参数可以带有模式，例如 `ap: ...`；而在 [C 可变参数函数][C-variadic function]定义或 trait 定义中的 C 可变参数关联函数声明里，模式是强制的。

```rust
unsafe extern "C" {
    unsafe fn f1(...);
    unsafe fn f2(ap: ...);
}

unsafe extern "C" fn f3(ap: ...) {}

trait Tr {
    unsafe extern "C" fn f4(ap: ...);
}
```

```rust
unsafe extern "C" fn f(...) {} // 错误：缺少模式。
```

```rust
trait Tr {
    unsafe extern "C" fn f(...); // 错误：缺少模式。
}
```

r[items.fn.body]
## 函数体

r[items.fn.body.intro]
函数的函数体块在概念上被包在另一个块中，该块首先绑定参数模式，然后 `return` 函数体的值。这意味着若求值了该块的尾表达式，其结果最终会返回给调用者。与往常一样，函数体内的显式 return 表达式若被执行，会短路该隐式返回。

例如，上面的函数表现得就好像写成：

<!-- ignore: example expansion -->
```rust
// argument_0 是调用者传入的实际第一个实参
let (value, _) = argument_0;
return {
    value
};
```

r[items.fn.body.bodyless]
没有函数体块的函数以分号结束。这种形式只能出现在 [trait] 或[外部块][external block]中。

r[items.fn.generics]
## 泛型函数

r[items.fn.generics.intro]
*泛型函数*允许一个或多个*参数化类型*出现在其签名中。每个类型参数都必须在函数名之后、用尖括号括起并以逗号分隔的列表中显式声明。

```rust
// foo 在 A 和 B 上是泛型的

fn foo<A, B>(x: A, y: B) {
## }
```

r[items.fn.generics.param-names]
在函数签名和函数体内，类型参数的名称可以用作类型名。

r[items.fn.generics.param-bounds]
可以为类型参数指定 [trait][Trait] 约束，以允许在该类型的值上调用该 trait 的方法。这使用 `where` 语法指定：

```rust
## use std::fmt::Debug;
fn foo<T>(x: T) where T: Debug {
## }
```

r[items.fn.generics.mono]
引用泛型函数时，会根据引用的上下文实例化其类型。例如，调用这里的 `foo` 函数：

```rust
use std::fmt::Debug;

fn foo<T>(x: &[T]) where T: Debug {
    // 细节省略
}

foo(&[1, 2]);
```

会将类型参数 `T` 实例化为 `i32`。

r[items.fn.generics.explicit-arguments]
类型参数也可以在函数名之后的尾随[路径][path]分量中显式提供。若没有足够的上下文来确定类型参数，这可能是必要的。例如，`mem::size_of::<u32>() == 4`。

r[items.fn.extern]
## Extern 函数限定符

r[items.fn.extern.intro]
`extern` 函数限定符允许提供可以用特定 ABI 调用的函数*定义*：

<!-- ignore: fake ABI -->
```rust
extern "ABI" fn foo() { /* ... */ }
```

r[items.fn.extern.def]
它们经常与[外部块][external block]项组合使用，后者提供可以在不提供*定义*的情况下调用函数的函数*声明*：

<!-- ignore: fake ABI -->
```rust
unsafe extern "ABI" {
  unsafe fn foo(); /* 没有函数体 */
  safe fn bar(); /* 没有函数体 */
}
unsafe { foo() };
bar();
```

r[items.fn.extern.default-abi]
当函数项的 `FunctionQualifiers` 中省略 `"extern" Abi?*` 时，会指定 ABI `"Rust"`。例如：

```rust
fn foo() {}
```

等价于：

```rust
extern "Rust" fn foo() {}
```

r[items.fn.extern.foreign-call]
函数可以被外部代码调用；使用与 Rust 不同的 ABI 可以例如提供能从 C 等其他编程语言调用的函数：

```rust
// 声明一个带有 "C" ABI 的函数
extern "C" fn new_i32() -> i32 { 0 }

// 声明一个带有 "stdcall" ABI 的函数
## #[cfg(any(windows, target_arch = "x86"))]
extern "stdcall" fn new_i32_stdcall() -> i32 { 0 }
```

r[items.fn.extern.default-extern]
与[外部块][external block]一样，当使用 `extern` 关键字而省略 `"ABI"` 时，所用 ABI 默认为 `"C"`。也就是说，这段：

```rust
extern fn new_i32() -> i32 { 0 }
let fptr: extern fn() -> i32 = new_i32;
```

等价于：

```rust
extern "C" fn new_i32() -> i32 { 0 }
let fptr: extern "C" fn() -> i32 = new_i32;
```

r[items.fn.extern.unwind]
### 展开

r[items.fn.extern.unwind.intro]
大多数 ABI 字符串有两种变体，一种带 `-unwind` 后缀，一种不带。`Rust` ABI 始终允许展开，因此没有 `Rust-unwind` ABI。ABI 的选择，连同运行时 [panic 处理函数][panic handler]，决定了从函数中展开时的行为。

r[items.fn.extern.unwind.behavior]
下表指出展开操作到达每种 ABI 边界（使用相应 ABI 字符串的函数声明或定义）时的行为。注意，Rust 运行时不受完全发生在另一语言运行时内部的任何展开影响，也无法对其产生影响，也就是说，那些被抛出并捕获、而未到达 Rust ABI 边界的展开。

`panic`-unwind 列指通过 `panic!` 宏及类似标准库机制进行的 [panic][panicking]，以及导致 panic 的任何其他 Rust 操作，例如数组越界索引或整数溢出。

“可展开” ABI 类别指 `"Rust"`（未标记 `extern` 的 Rust 函数的隐式 ABI）、`"C-unwind"`，以及名称中带 `-unwind` 的任何其他 ABI。“不可展开” ABI 类别指所有其他 ABI 字符串，包括 `"C"` 和 `"stdcall"`。

原生展开按目标定义。在支持抛出和捕获 C++ 异常的目标上，它指用于实现该特性的机制。某些平台实现一种称为[“强制展开”][forced-unwinding]的展开形式；Windows 上的 `longjmp` 和 `glibc` 中的 `pthread_exit` 以这种方式实现。强制展开被明确排除在表中“原生展开”列之外。

| panic 运行时   | ABI           | `panic`-unwind                        | 原生展开（非强制）       |
| -------------- | ------------  | ------------------------------------- | -----------------------  |
| `panic=unwind` | 可展开        | 展开                                  | 展开                     |
| `panic=unwind` | 不可展开      | 中止（见下方注释）                    | [未定义行为][undefined behavior] |
| `panic=abort`  | 可展开        | `panic` 中止而不展开                  | 中止                     |
| `panic=abort`  | 不可展开      | `panic` 中止而不展开                  | [未定义行为][undefined behavior] |

r[items.fn.extern.abort]
在 `panic=unwind` 下，当 `panic` 因不可展开的 ABI 边界而变成中止时，要么不会运行任何析构器（`Drop` 调用），要么会运行直到 ABI 边界为止的所有析构器。这两种行为中会发生哪一种未指定。

关于跨越 FFI 边界展开的其他考虑和限制，参见 [Panic 文档中的相关章节][panic-ffi]。

r[items.fn.extern.custom]
### Extern "custom"

r[items.fn.extern.custom.intro]
`extern "custom"` 函数具有未知的自定义 ABI。调用此类函数的唯一方式是通过[内联汇编][inline assembly]。

> [!EXAMPLE]
> ```rust
> # #[cfg(target_arch = "x86_64")] {
> # use core::arch::{asm, naked_asm};
> #
> /// 将 `rax` 加 1。
> ///
> /// 此函数使用自定义调用约定：实参
> /// 在 `rax` 中传入，结果在 `rax` 中返回，标志寄存器可能
> /// 被破坏，所有其他寄存器保持不变。
> #[unsafe(naked)]
> unsafe extern "custom" fn increment() {
>     naked_asm!(
>         "add rax, 1",
>         "ret",
>     )
> }
>
> let mut x: u64 = 41;
> // 安全性：内联汇编遵守 `increment` 的调用约定：
> // 实参在 `rax` 中传入，结果从 `rax` 读取，
> // 且不影响其他寄存器。
> unsafe {
>     asm!(
>         "call {}",
>         sym increment,
>         inout("rax") x,
>     );
> }
> assert_eq!(x, 42);
> # }
> ```

r[items.fn.extern.custom.signature]
`extern "custom"` 函数必须：

- 是 `unsafe` 的。
- 没有任何参数。
- 返回[单元类型][unit type]，返回类型要么省略，要么显式写为 `()`。

> **注意**
> 该规则是语法性的。返回类型不能是类型别名，即使该别名定义为[单元类型][unit type]。
>
> ```rust
> type Unit = ();
>
> #[unsafe(naked)]
> unsafe extern "custom" fn f() -> Unit { // 错误：不是显式的 `()`。
>     core::arch::naked_asm!("ret")
> }
> ```

r[items.fn.extern.custom.naked]
`extern "custom"` 函数定义必须是[裸函数][naked function]。

[forced-unwinding]: https://rust-lang.github.io/rfcs/2945-c-unwind-abi.html#forced-unwinding
[panic handler]: ../panic.md#the-panic_handler-attribute
[panic-ffi]: ../panic.md#unwinding-across-ffi-boundaries
[panicking]: ../panic.md
[undefined behavior]: ../behavior-considered-undefined.md

r[items.fn.const]
## Const 函数

const 函数的定义参见 [const 函数][const functions]。

r[items.fn.async]
## Async 函数

r[items.fn.async.intro]
函数可以被限定为 async，也可以与 `unsafe` 限定符组合：

```rust
async fn regular_example() { }
async unsafe fn unsafe_example() { }
```

r[items.fn.async.future]
调用 async 函数时不会做任何工作：相反，它们把实参捕获到一个 future 中。当该 future 被轮询时，才会执行函数体。

r[items.fn.async.desugar-brief]
async 函数大致等价于一个返回 [`impl Future`] 且函数体为 [`async move` 块][async-blocks]的函数：

```rust
// 源码
async fn example(x: &str) -> usize {
    x.len()
}
```

大致等价于：

```rust
## use std::future::Future;
// 脱糖后
fn example<'a>(x: &'a str) -> impl Future<Output = usize> + 'a {
    async move { x.len() }
}
```

r[items.fn.async.desugar]
实际的脱糖更复杂：

r[items.fn.async.lifetime-capture]
- 脱糖后的返回类型被假定会捕获来自 `async fn` 声明的所有生命周期参数。这可以在上面脱糖后的例子中看到，它显式地长于、因而捕获了 `'a`。

r[items.fn.async.param-capture]
- 函数体中的 [`async move` 块][async-blocks]会捕获所有函数参数，包括未使用的或绑定到 `_` 模式的参数。这确保函数参数的析构顺序与该函数不是 async 时相同，只不过析构发生在返回的 future 被完全 await 之时。

关于 async 的效果的更多信息，参见 [`async` 块][async-blocks]。

[async-blocks]: ../expressions/block-expr.md#async-blocks
[`impl Future`]: ../types/impl-trait.md

r[items.fn.async.edition2018]
> [!EDITION-2018]
> Async 函数仅从 Rust 2018 开始可用。

r[items.fn.async.safety]
### 组合 `async` 和 `unsafe`

r[items.fn.async.safety.intro]
声明既是 async 又是 unsafe 的函数是合法的。得到的函数调用时是不安全的，并且（与任何 async 函数一样）返回一个 future。该 future 只是普通的 future，因此 “await” 它并不需要 `unsafe` 上下文：

```rust
// 返回一个 future，在被 await 时解引用 `x`。
//
// 可靠性条件：在所得 future 完成之前，
// `x` 必须可以安全地解引用。
async unsafe fn unsafe_example(x: *const i32) -> i32 {
  *x
}

async fn safe_example() {
    // 最初调用该函数需要 `unsafe` 块：
    let p = 22;
    let future = unsafe { unsafe_example(&p) };

    // 但这里不需要 `unsafe` 块。这将
    // 读取 `p` 的值：
    let q = future.await;
}
```

注意，这种行为是脱糖为返回 `impl Future` 的函数的结果——在此情况下，我们脱糖到的函数是 `unsafe` 函数，但返回值保持不变。

在 async 函数上使用 unsafe 的方式与在其他函数上完全相同：它表明该函数对其调用者施加了额外义务以确保可靠性。与任何其他 unsafe 函数一样，这些条件可能延伸到最初的调用本身之外——例如在上面的片段中，`unsafe_example` 函数接受指针 `x` 作为实参，然后（在被 await 时）解引用该指针。这意味着 `x` 必须一直有效直到 future 执行完毕，而这是调用者的责任。

r[items.fn.c-variadic]
## C 可变参数函数

r[items.fn.c-variadic.intro]
*C 可变参数*函数接受可变参数列表 `pat: ...` 作为其最后一个参数。

```rust
unsafe extern "C" fn f(mut ap: ...) -> f64 {
    unsafe { ap.next_arg::<f64>() }
}
```

```rust
unsafe extern "C" fn f(ap: ..., _: ()) {} // 错误：`...` 必须位于最后。
```

该参数代表调用者可能传入的任意数量的实参。

r[items.fn.c-variadic.parameter-type]
函数体中 `pat` 的类型是 [`VaList<'_>`]。

```rust
## use core::ffi::VaList;
unsafe extern "C" fn f(ap: ...) {
    let _: VaList<'_> = ap;
}
```

r[items.fn.c-variadic.lifetime]
C 可变参数函数定义对其可变参数的生命周期是隐式泛型的，就好像该参数具有类型 `VaList<'x>`，其中 `'x` 是一个新的、不可命名的生命周期。因为该函数必须对任何这样的生命周期都合法，所以无法证明 `VaList` 长于任何调用者提供的生命周期（因而不能逃逸出这次调用），也无法证明任何调用者提供的生命周期长于它。

```rust
## use core::ffi::VaList;
fn b_outlives_a<'a, 'b: 'a>(_: &mut VaList<'a>, _: &mut &'b mut u8) {}
unsafe extern "C" fn f(mut r: &mut u8, mut ap: ...) {
    b_outlives_a(&mut ap, &mut r); // 错误：可能活得不够长。
}
```

```rust
## use core::ffi::VaList;
fn a_outlives_b<'a: 'b, 'b>(_: &mut VaList<'a>, _: &mut &'b mut u8) {}
unsafe extern "C" fn f(mut r: &mut u8, mut ap: ...) {
    a_outlives_b(&mut ap, &mut r); // 错误：可能活得不够长。
}
```

> **注意**
> 这与数据是栈变量的情况不同：任何调用者提供的生命周期都可以被证明长于对被调用者栈变量的借用。
>
> ```rust
> struct MockVaList<'data>(&'data u8);
> fn b_outlives_a<'a, 'b: 'a>(_: &mut MockVaList<'a>, _: &mut &'b mut u8) {}
> unsafe extern "C" fn f(mut r: &mut u8) {
>     let data = 0;
>     let mut ap = MockVaList(&data);
>     b_outlives_a(&mut ap, &mut r); // 可以。
> }
> ```

r[items.fn.c-variadic.desugar-brief]
C 可变参数函数定义大致等价于操作 [`VaList`] 的函数。

```rust
unsafe extern "C" fn f(mut ap: ...) -> i32 {
    unsafe { ap.next_arg::<i32>() }
}
```

大致脱糖为：

<!-- no_run: conceptual desugaring -->
```rust
## #![ feature(core_intrinsics) ]
## #![allow(internal_features)]
## use core::ffi::VaList;
## use core::mem::MaybeUninit;
use core::intrinsics::{va_arg, va_end};
// `va_start` 是魔法，没有对应的 intrinsic。
fn va_start(ap: *mut VaList<'_>) { /* 魔法 */ }
unsafe extern "C" fn f() -> i32 {
    unsafe {
        let mut ap: MaybeUninit<VaList<'_>> = MaybeUninit::uninit();
        va_start(ap.as_mut_ptr());
        let mut ap = ap.assume_init();
        let x = va_arg::<i32>(&mut ap);
        va_end(&mut ap);
        x
    }
}
```

> **注意**
> 在实际的 C 可变参数函数定义中，`VaList<'_>` 中的生命周期与这段代码所暗示的不同。参见 [items.fn.c-variadic.lifetime]。

r[items.fn.c-variadic.next-arg-safety]
调用 `VaList::next_arg` 读取类型为 `T` 的实参，仅当满足以下全部条件时才是安全的：

- 还有另一个 C 可变参数可以读取。
- 实参的实际类型 `U` 与 `T` 兼容（如下定义）。
- 若 `U` 和 `T` 都是整数类型，则调用者传入的值必须
在两种类型中都可以表示。

当下列之一为真时，类型 `T` 和 `U` 兼容：

- `T` 和 `U` 是同一类型（直至自由生命周期）。
- `T` 和 `U` 是相同大小的整数类型。
- `T` 和 `U` 都是指针，且它们的目标类型兼容。
- `T` 是指向 `c_void` 的指针且 `U` 是指向 `i8` 或 `u8` 的指针，或反之。

兼容类型的例子有：

- `u32` 和 `i32` —— 但若值在目标类型中不可表示，仍可能发生 UB。
- `u64` 和 `usize` —— 在 64 位平台上。
- `*const &'a u32` 和 `*mut &'static u32` —— 这些类型直至自由生命周期是相等的。

不兼容类型的例子有：

- `usize` 和 `*const _` —— 指针和整数不兼容。
- `*const fn(&'static ())` 和 `*const for<'a> fn(&'a ())` —— 这些类型直至自由生命周期并不相等。

r[items.fn.c-variadic.abi-compatibility]
[`VaList`] 与 C 的 `va_list` 类型 ABI 兼容。

```rust
## use core::ffi::{c_char, c_int, VaList};
unsafe extern "C" {
    // C 的 `vprintf` 函数是：
    //
    //     int vprintf(const char *format, va_list ap);
    //
    unsafe fn vprintf(fmt: *const c_char, ap: VaList<'_>) -> c_int;
}

unsafe extern "C" fn print(fmt: *const c_char, ap: ...) -> c_int {
    // `VaList` 被直接传给 C 函数。
    unsafe { vprintf(fmt, ap) }
}
```

r[items.fn.c-variadic.abi]
除[裸函数][naked functions]外，只有 `extern "C"` 和 `extern "C-unwind"` 函数定义可以接受可变参数列表。

```rust
unsafe fn f(ap: ...) {} // 错误：不支持。
```

```rust
unsafe extern "sysv64" fn f(ap: ...) {} // 错误：不支持。
```

裸函数只有在其 ABI 字符串在 [items.extern.variadic.conventions] 下被接受时，才能接受可变参数列表。

```rust
## #[cfg(target_arch = "x86_64")] {
/// 计算 `n` 维向量 `v`（以 `n` 个 C 可变参数 `f64`
/// 传入）与向量 `(c, ..., c)` 的点积。
/// 也就是计算 `c * (v1 + ... + vn)`。
///
/// # 安全性
///
/// 调用者必须传入范围为 `1..=7` 的 `n`，后跟恰好
/// `n` 个类型为 `f64` 的值。
// 安全性：函数体遵守 "sysv64" 调用约定，履行
// 签名，并且不会落入。
#[unsafe(naked)]
unsafe extern "sysv64" fn dot(n: u64, c: f64, v: ...) -> f64 {
    core::arch::naked_asm!(
        // "sysv64" 调用约定将 `n` 放在 `rdi` 中，将 `c` 放在
        // `xmm0` 中，并将各坐标按顺序放在 `xmm1` 到 `xmm7`
        // 中。（调用者还将所用向量寄存器的数量放在 `al` 中。）
        //
        // 求和取下面这条链中最后 `n - 1` 次加法。
        // 每条 `addsd` 恰好编码为 4 字节，因此我们在
        // `mulsd` 之前 `4 * (n - 1)` 字节处进入该链。
        "neg rdi", // 即 `rdi = -n`。
        "lea rax, [rip + 2f]", // 即 `rax` = 标签 2 的地址。
        "lea rax, [rax + rdi*4 + 4]", // 即 `rax -= 4 * (n - 1)`。
        "jmp rax",
        "addsd xmm6, xmm7", // 当 `n` 为 7 时进入。
        "addsd xmm5, xmm6", // ……当 `n` 至少为 6 时。
        "addsd xmm4, xmm5",
        "addsd xmm3, xmm4",
        "addsd xmm2, xmm3",
        "addsd xmm1, xmm2", // ……当 `n` 至少为 2 时。
        "2:",
        "mulsd xmm0, xmm1", // 结果在 `xmm0` 中返回。
        "ret",
    )
}

// 安全性：每次调用都向 `dot` 传入 `n` 个可变参数 `f64`。
let dot2 = unsafe { dot(2, 10.0, 3.0, 4.0) };
assert_eq!(dot2, 70.0);
let dot7 = unsafe { dot(7, 2.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0) };
assert_eq!(dot7, 56.0);
## }
```

r[items.fn.c-variadic.safety]
当签名中使用可变参数列表时：

- 函数定义必须是 `unsafe` 的。
- trait 定义中的函数声明必须是 `unsafe` 的。
- `extern` 块中的函数声明可以是 `safe` 的。

```rust
extern "C" fn f(ap: ...) {} // 错误：必须是 `unsafe`。
```

```rust
trait Tr {
    extern "C" fn f(ap: ...); // 错误：必须是 `unsafe`。
}
```

```rust
unsafe extern "C" {
    safe fn f(ap: ...); // 可以。
}
```

> **注意**
> 关于 `extern` 块中的 `safe` 函数声明，参见 [items.extern.variadic] 中的警告。

r[items.fn.c-variadic.async]
C 可变参数函数不能是 `async` 的。

```rust
async unsafe extern "C" fn f(ap: ...) {} // 错误：不能是 `async`。
```

r[items.fn.c-variadic.const]
C 可变参数函数不能是 `const` 的。

```rust
const unsafe extern "C" fn f(ap: ...) {} // 错误：不能是 `const`。
```

r[items.fn.c-variadic.stable-targets]
在以下目标架构上，对 C 可变参数函数定义的支持是稳定的：

- x86 和 x86-64
- ARM
- AArch64 和 Arm64EC
- RISC-V 32 位和 64 位（使用 ilp32e ABI 时除外）
- LoongArch 32 位和 64 位
- s390x
- PowerPC 和 PowerPC64
- AMDGPU 和 NVPTX
- Wasm32 和 Wasm64
- C-SKY
- Xtensa
- Hexagon
- SPARC64
- MIPS

> **注意**
> 某些目标架构（例如 BPF）不支持 C 可变参数函数定义。若在不受支持的目标上使用此类定义，编译器会发出错误。

r[items.fn.attributes]
## 函数上的属性

r[items.fn.attributes.intro]
函数上允许[外部属性][attributes]。[内部属性][attributes]允许直接出现在其函数体[块][block]内的 `{` 之后。

此例展示函数上的内部属性。该函数的文档只有单词 “Example”。

```rust
fn documented() {
    #![doc = "Example"]
}
```

> **注意**
> 除 lint 外，惯用法是只在函数项上使用外部属性。

r[items.fn.attributes.builtin-attributes]
在函数上有意义的属性有：

- [`cfg_attr`]
- [`cfg`]
- [`cold`]
- [`deprecated`]
- [`doc`]
- [`export_name`]
- [`inline`]
- [`link_section`]
- [`must_use`]
- [`no_mangle`]
- [Lint 检查属性][Lint check attributes]
- [过程宏属性][Procedural macro attributes]
- [测试属性][Testing attributes]

r[items.fn.param-attributes]
## 函数参数上的属性

r[items.fn.param-attributes.intro]
函数参数上允许[外部属性][attributes]，所允许的[内置属性][built-in attributes]仅限于 `cfg`、`cfg_attr`、`allow`、`warn`、`deny` 和 `forbid`。

```rust
fn len(
    #[cfg(windows)] slice: &[u16],
    #[cfg(not(windows))] slice: &[u8],
) -> usize {
    slice.len()
}
```

r[items.fn.param-attributes.parsed-attributes]
应用于项的过程宏属性所使用的惰性辅助属性也是允许的，但要注意不要把这些惰性属性包含在最终的 `TokenStream` 中。

例如，下列代码定义了一个并未在任何地方正式定义的惰性 `some_inert_attribute` 属性，由 `some_proc_macro_attribute` 过程宏负责检测其存在并从输出 token 流中移除它。

<!-- ignore: requires proc macro -->
```rust
#[some_proc_macro_attribute]
fn foo_oof(#[some_inert_attribute] arg: u8) {
}
```

[const contexts]: ../const_eval.md#const-context
[const functions]: ../const_eval.md#const-functions
[external block]: external-blocks.md
[path]: ../paths.md
[block]: ../expressions/block-expr.md
[variables]: ../variables.md
[type]: ../types.md#type-expressions
[unit type]: ../types/tuple.md
[*function item type*]: ../types/function-item.md
[Trait]: traits.md
[attributes]: ../attributes.md
[`cfg`]: ../conditional-compilation.md#the-cfg-attribute
[`cfg_attr`]: ../conditional-compilation.md#the-cfg_attr-attribute
[lint check attributes]: ../attributes/diagnostics.md#lint-check-attributes
[procedural macro attributes]: macro.proc.attribute
[testing attributes]: ../attributes/testing.md
[`cold`]: ../attributes/codegen.md#the-cold-attribute
[`inline`]: ../attributes/codegen.md#the-inline-attribute
[naked function]: ../attributes/codegen.md#the-naked-attribute
[`deprecated`]: ../attributes/diagnostics.md#the-deprecated-attribute
[`doc`]: ../../rustdoc/the-doc-attribute.html
[`must_use`]: ../attributes/diagnostics.md#the-must_use-attribute
[patterns]: ../patterns.md
[`export_name`]: ../abi.md#the-export_name-attribute
[`link_section`]: ../abi.md#the-link_section-attribute
[`no_mangle`]: ../abi.md#the-no_mangle-attribute
[built-in attributes]: ../attributes.md#built-in-attributes-index
[trait item]: traits.md
[method]: associated-items.md#methods
[associated function]: associated-items.md#associated-functions-and-methods
[implementation]: implementations.md
[value namespace]: ../names/namespaces.md
[C-variadic function]: items.fn.c-variadic.intro
[`extern` block]: external-blocks.md
[`VaList<'_>`]: lang-types.va-list
[`VaList`]: lang-types.va-list
[zero-sized]: glossary.zst
[inline assembly]: ../inline-assembly.md
[naked functions]: attributes.codegen.naked
