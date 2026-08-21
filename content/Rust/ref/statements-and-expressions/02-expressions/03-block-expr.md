+++
title = "03-块表达式"
date = 2026-08-18T08:45:00+08:00
weight = 46
type = "docs"
description = "块表达式 — The Rust Reference"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Reference](https://doc.rust-lang.org/reference/)

> 原文链接: [https://doc.rust-lang.org/reference/expressions/block-expr.html](https://doc.rust-lang.org/reference/expressions/block-expr.html)

r[expr.block]
# 块表达式

r[expr.block.syntax]
```grammar,expressions
BlockExpression ->
    `{`
        InnerAttribute*
        Statements?
    `}`

BlockExpressionNoInnerAttributes ->
    `{`
        Statements?
    `}`

Statements ->
      Statement+
    | Statement+ ExpressionWithoutBlock
    | ExpressionWithoutBlock
```

r[expr.block.intro]
*块表达式*（*block expression*），或称*块*（*block*），是一种控制流表达式，同时也是项与变量声明的匿名命名空间作用域。

r[expr.block.sequential-evaluation]
作为控制流表达式，块会依次执行其组成中的非项声明语句，然后执行其可选的最终表达式。

r[expr.block.namespace]
作为匿名命名空间作用域，项声明仅在块自身内部可见；由 `let` 语句声明的变量从下一条语句起直至块末尾可见。更多细节见[作用域][scopes]章节。

r[expr.block.inner-attributes]
块的语法为 `{`，接着任意数量的[内部属性][inner attributes]，再接着任意数量的[语句][statements]，然后是一个可选的表达式（称为最终操作数），最后以 `}` 结束。

r[expr.block.statements]
语句通常需要后跟分号，但有两种例外：

1. 项声明语句不需要后跟分号。
2. 表达式语句通常需要后跟分号，除非其外层表达式是控制流表达式。

r[expr.block.null-statement]
此外，语句之间允许出现多余的分号，但这些分号不影响语义。

r[expr.block.evaluation]
求值块表达式时，除项声明语句外，每条语句都会按顺序执行。

r[expr.block.result]
然后，若给定了最终操作数，则执行该最终操作数。

r[expr.block.value-trailing-expr]
当块包含[最终操作数][final operand]时，块具有该最终操作数的类型与值。

```rust
let x: u8 = { 0u8 }; // `0u8` 是最终操作数。
assert_eq!(x, 0);
let x: u8 = { (); 0u8 }; // 同上。
assert_eq!(x, 0);
```

r[expr.block.value-no-trailing-expr]
当块不包含[最终操作数][final operand]且该块不发散时，块具有[单元类型][unit type]与[单元值][unit value]。

```rust
let x: () = {}; // 没有最终操作数。
assert_eq!(x, ());
let x: () = { 0u8; }; // 同上。
assert_eq!(x, ());
```

r[expr.block.value-diverges-no-trailing-expr]
当块不包含[最终操作数][final operand]且该块[发散][diverges]时，块具有[never 类型][never type]，且没有最终值（因为其类型是[不可居留][uninhabited]的）。

```rust
fn f() -> ! { loop {}; } // 发散且没有最终操作数。
//          ^^^^^^^^^^^^
// 函数体是一个块表达式。
```

> **注意**
> 请注意，没有最终操作数的块，与具有显式单元类型最终操作数的块是不同的。例如，即使下面的块发散，该块的类型也是[单元][unit]而非[never][never]。
>
> ```rust
> fn f() -> ! { loop {}; () } // ERROR: Mismatched types.
> //          ^^^^^^^^^^^^^^^ 此块具有单元类型。
> ```

> **注意**
> 作为控制流表达式，若块表达式是表达式语句的外层表达式，除非其后立即跟有分号，否则期望类型为 `()`。

r[expr.block.diverging]
若所有可达的控制流路径都包含发散表达式，则认为该块是[发散][divergence]的，除非该表达式是未被读取的[位置表达式][place expression]。

```rust
## #![ feature(never_type) ]
fn no_control_flow() -> ! {
    // 没有条件语句，因此整个函数体都是发散的。
    loop {}
}

fn control_flow_diverging() -> ! {
    // 所有路径都发散，因此整个函数体都是发散的。
    if true {
        loop {}
    } else {
        loop {}
    }
}

fn control_flow_not_diverging() -> () {
    // 有些路径不发散，因此整个块不发散。
    if true {
        ()
    } else {
        loop {}
    }
}

// 注意：此处使用了不稳定的 never 类型，仅在 Rust 的 nightly
// 通道上可用。这样做是为了便于说明。在稳定版 Rust 中也可能
// 遇到这种情形，但需要更迂回的示例。
struct Foo {
    x: !,
}

fn make<T>() -> T { loop {} }

fn diverging_place_read() -> ! {
    let foo = Foo { x: make() };
    // 读取位置表达式会产生发散的块。
    let _x = foo.x;
}
```

```rust
## #![ feature(never_type) ]
## fn make<T>() -> T { loop {} }
## struct Foo {
##     x: !,
## }
fn diverging_place_not_read() -> ! {
    let foo = Foo { x: make() };
    // 赋值给 `_` 表示该位置未被读取。
    let _ = foo.x;
} // ERROR: Mismatched types.
```

r[expr.block.value]
块始终是[值表达式][value expressions]，并在值表达式上下文中求值最后一个操作数。

> **注意**
> 这可用于在确实需要时强制移动值。例如，下面的例子在调用 `consume_self` 时失败，因为结构体已在块表达式中从 `s` 移出。
>
> ```rust
> struct Struct;
>
> impl Struct {
>     fn consume_self(self) {}
>     fn borrow_self(&self) {}
> }
>
> fn move_by_block_expression() {
>     let s = Struct;
>
>     // 在块表达式中将值从 `s` 移出。
>     (&{ s }).borrow_self();
>
>     // 因 `s` 已被移出而无法执行。
>     s.consume_self();
> }
> ```

r[expr.block.async]
## `async` 块

r[expr.block.async.syntax]
```grammar,expressions
AsyncBlockExpression -> `async` `move`? BlockExpression
```

r[expr.block.async.intro]
*async 块*是块表达式的一种变体，其求值结果为一个 future。

r[expr.block.async.future-result]
若块存在最终表达式，则该表达式决定 future 的结果值。

r[expr.block.async.anonymous-type]
执行 async 块类似于执行闭包表达式：其直接效果是产生并返回一个匿名类型。

r[expr.block.async.future]
不过，闭包返回的类型实现一个或多个 [`std::ops::Fn`] trait，而 async 块返回的类型则实现 [`std::future::Future`] trait。

r[expr.block.async.layout-unspecified]
该类型的实际数据格式未指定。

> **注意**
> rustc 生成的 future 类型大致等价于一个枚举，每个 `await` 点对应一个变体，每个变体存储从对应点恢复所需的数据。

r[expr.block.async.edition2018]
> [!EDITION-2018]
> Async 块仅从 Rust 2018 起可用。

r[expr.block.async.capture]
### 捕获模式

Async 块使用与闭包相同的[捕获模式][capture modes]从其环境中捕获变量。与闭包类似，写成 `async { .. }` 时，每个变量的捕获模式会根据块的内容进行推断。而 `async move { .. }` 块则会将所有引用的变量移动到结果 future 中。

r[expr.block.async.context]
### Async 上下文

由于 async 块会构造 future，它们定义了一个**async 上下文**，其中又可包含 [`await` 表达式][`await` expressions]。Async 上下文由 async 块以及 async 函数体建立；async 函数体的语义是用 async 块来定义的。

r[expr.block.async.function]
### 控制流运算符

r[expr.block.async.function.intro]
Async 块的行为像函数边界，与闭包非常相似。

r[expr.block.async.function.return-try]
因此，`?` 运算符与 `return` 表达式都会影响 future 的输出，而不是包围它的函数或其他上下文。也就是说，在 async 块内使用 `return <expr>` 会将 `<expr>` 的结果作为该 future 的输出返回。类似地，若 `<expr>?` 传播了错误，该错误会作为 future 的结果被传播。

r[expr.block.async.function.control-flow]
最后，不能使用 `break` 和 `continue` 关键字从 async 块中跳出。因此，下面的代码是非法的：

```rust
loop {
    async move {
        break; // error[E0267]: `break` inside of an `async` block
    }
}
```

r[expr.block.const]
## `const` 块

r[expr.block.const.syntax]
```grammar,expressions
ConstBlockExpression -> `const` BlockExpression
```

r[expr.block.const.intro]
*const 块*是块表达式的一种变体，其主体在编译期而非运行时求值。

r[expr.block.const.context]
Const 块允许你在不必定义新的[常量项][constant items]的情况下定义常量值，因此有时也被称为*内联常量*（*inline consts*）。它还支持类型推断，因此与[常量项][constant items]不同，无需指定类型。

r[expr.block.const.generic-params]
与[自由][free item]常量项不同，const 块能够引用作用域中的泛型参数。它们会被脱糖为带有作用域中泛型参数的常量项（类似于关联常量，但没有与之关联的 trait 或类型）。例如，这段代码：

```rust
fn foo<T>() -> usize {
    const { std::mem::size_of::<T>() + 1 }
}
```

等价于：

```rust
fn foo<T>() -> usize {
    {
        struct Const<T>(T);
        impl<T> Const<T> {
            const CONST: usize = std::mem::size_of::<T>() + 1;
        }
        Const::<T>::CONST
    }
}
```

r[expr.block.const.evaluation]

若 const 块表达式在运行时被执行，则该常量保证会被求值，即使其返回值被忽略：

```rust
fn foo<T>() -> usize {
    // 若这段代码曾被执行，则断言一定已在编译期求值。
    const { assert!(std::mem::size_of::<T>() > 0); }
    // 此处可以有依赖该类型非零大小的 unsafe 代码。
    /* ... */
    42
}
```

r[expr.block.const.not-executed]

若 const 块表达式在运行时未被执行，则它可能被求值，也可能不被求值：
```rust
if false {
    // 构建程序时 panic 可能发生，也可能不发生。
    const { panic!(); }
}
```

r[expr.block.unsafe]
## `unsafe` 块

r[expr.block.unsafe.syntax]
```grammar,expressions
UnsafeBlockExpression -> `unsafe` BlockExpression
```

r[expr.block.unsafe.intro]
_关于何时使用 `unsafe`，详见 [`unsafe` 块][`unsafe` blocks]。_

可以在代码块前加上 `unsafe` 关键字，以允许[不安全操作][unsafe operations]。示例：

```rust
unsafe {
    let b = [13u8, 17u8];
    let a = &b[0] as *const u8;
    assert_eq!(*a, 13);
    assert_eq!(*a.offset(1), 17);
}

## unsafe fn an_unsafe_fn() -> i32 { 10 }
let a = unsafe { an_unsafe_fn() };
```

r[expr.block.label]
## 带标签的块表达式

带标签的块表达式记载于[循环与其他可 break 的表达式][Loops and other breakable expressions]一节。

r[expr.block.attributes]
## 块表达式上的属性

r[expr.block.attributes.inner-attributes]
在以下情形中，允许在块表达式的开括号之后直接使用[内部属性][Inner attributes]：

* [函数][Function]与[方法][method]体。
* 循环体（[`loop`]、[`while`] 与 [`for`]）。
* 用作[语句][statement]的块表达式。
* 作为[数组表达式][array expressions]、[元组表达式][tuple expressions]、[调用表达式][call expressions]以及元组风格[结构体][struct]表达式元素的块表达式。
* 作为另一块表达式尾部表达式的块表达式。
<!-- Keep list in sync with expressions.md -->

r[expr.block.attributes.valid]
对块表达式有意义的属性是 [`cfg`] 与[lint 检查属性][the lint check attributes]。

例如，此函数在 unix 平台上返回 `true`，在其他平台上返回 `false`。

```rust
fn is_unix_platform() -> bool {
    #[cfg(unix)] { true }
    #[cfg(not(unix))] { false }
}
```

[`await` expressions]: await-expr.md
[`cfg`]: ../conditional-compilation.md
[`for`]: loop-expr.md#iterator-loops
[`loop`]: loop-expr.md#infinite-loops
[`unsafe` blocks]: ../unsafe-keyword.md#unsafe-blocks-unsafe-
[`while`]: loop-expr.md#predicate-loops
[array expressions]: array-expr.md
[call expressions]: call-expr.md
[capture modes]: ../types/closure.md#capture-modes
[constant items]: ../items/constant-items.md
[diverges]: expr.block.diverging
[final operand]: expr.block.inner-attributes
[free item]: ../glossary.md#free-item
[function]: ../items/functions.md
[inner attributes]: ../attributes.md
[method]: ../items/associated-items.md#methods
[mutable reference]: ../types/pointer.md#mutables-references-
[never type]: type.never
[never]: type.never
[place expression]: expr.place-value.place-memory-location
[scopes]: ../names/scopes.md
[shared references]: ../types/pointer.md#shared-references-
[statement]: ../statements.md
[statements]: ../statements.md
[struct]: struct-expr.md
[the lint check attributes]: ../attributes/diagnostics.md#lint-check-attributes
[tuple expressions]: tuple-expr.md
[uninhabited]: glossary.uninhabited
[unit type]: type.tuple.unit
[unit value]: type.tuple.unit
[unit]: type.tuple.unit
[unsafe operations]: ../unsafety.md
[value expressions]: ../expressions.md#place-expressions-and-value-expressions
[Loops and other breakable expressions]: expr.loop.block-labels
