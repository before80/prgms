+++
title = "09-析构器"
date = 2026-08-18T08:45:00+08:00
weight = 92
type = "docs"
description = "析构器 — The Rust Reference"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Reference](https://doc.rust-lang.org/reference/)

> 原文链接: [https://doc.rust-lang.org/reference/destructors.html](https://doc.rust-lang.org/reference/destructors.html)

r[destructors]
# 析构器

r[destructors.intro]
当[已初始化][initialized]的[变量][variable]或[临时值][temporary]离开[作用域](#drop-scopes)时，会运行其 *析构器*，或者说它被 *drop*。[赋值][Assignment]也会运行其左操作数的析构器（若它已初始化）。若变量只被部分初始化，则只 drop 其已初始化的字段。

r[destructors.operation]
类型 `T` 的析构器包括：

1. 若 `T: Drop`，调用 [`<T as core::ops::Drop>::drop`](core::ops::Drop::drop)
2. 递归运行其所有字段的析构器。
    * [结构体][struct]的字段按声明顺序 drop。
    * 活动[枚举变体][enum variant]的字段按声明顺序 drop。
    * [元组][tuple]的字段按顺序 drop。
    * [数组][array]或拥有所有权的[切片][slice]的元素从第一个元素到最后一个元素 drop。
    * [闭包][closure]按移动捕获的变量以未指定的顺序 drop。
    * [Trait 对象][Trait objects]运行底层类型的析构器。
    * 其他类型不会导致任何进一步的 drop。

r[destructors.drop_in_place]
若必须手动运行析构器，例如在实现你自己的智能指针时，可以使用 [`core::ptr::drop_in_place`]。

一些例子：

```rust
struct PrintOnDrop(&'static str);

impl Drop for PrintOnDrop {
    fn drop(&mut self) {
        println!("{}", self.0);
    }
}

let mut overwritten = PrintOnDrop("drops when overwritten");
overwritten = PrintOnDrop("drops when scope ends");

let tuple = (PrintOnDrop("Tuple first"), PrintOnDrop("Tuple second"));

let moved;
// 赋值时不运行析构器。
moved = PrintOnDrop("Drops when moved");
// 现在被 drop，但随后未初始化。
moved;

// 未初始化的不会被 drop。
let uninitialized: PrintOnDrop;

// 部分移动之后，只 drop 剩余字段。
let mut partial_move = (PrintOnDrop("first"), PrintOnDrop("forgotten"));
// 执行部分移动，只留下 `partial_move.0` 已初始化。
core::mem::forget(partial_move.1);
// 当 partial_move 的作用域结束时，只 drop 第一个字段。
```

r[destructors.scope]
## Drop 作用域

r[destructors.scope.intro]
每个变量或临时值都关联到一个 *drop 作用域*。当控制流离开某个 drop 作用域时，所有关联到该作用域的变量按声明的相反顺序（对变量）或创建的相反顺序（对临时值）被 drop。

r[destructors.scope.desugaring]
可以通过将 [`for`]、[`if`] 和 [`while`] 表达式替换为使用 [`match`]、[`loop`] 和 `break` 的等价表达式来确定 drop 作用域。

r[destructors.scope.operators]
重载运算符与内建运算符不加区分，并且不考虑[绑定模式][binding modes]。

r[destructors.scope.list]
给定一个函数或闭包，存在以下 drop 作用域：

r[destructors.scope.function]
* 整个函数

r[destructors.scope.statement]
* 每个[语句][statement]

r[destructors.scope.expression]
* 每个[表达式][expression]

r[destructors.scope.block]
* 每个块，包括函数体
    * 对于[块表达式][block expression]，块的作用域与该表达式的作用域是同一作用域。

r[destructors.scope.match-arm]
* `match` 表达式的每个分支

r[destructors.scope.nesting]
Drop 作用域按如下方式相互嵌套。当同时离开多个作用域时，例如从函数返回时，变量从内向外被 drop。

r[destructors.scope.nesting.function]
* 整个函数作用域是最外层作用域。

r[destructors.scope.nesting.function-body]
* 函数体块包含在整个函数的作用域之内。

r[destructors.scope.nesting.expr-statement]
* 表达式语句中表达式的父作用域是该语句的作用域。

r[destructors.scope.nesting.let-initializer]
* [`let` 语句][`let` statement]初始化表达式的父作用域是该 `let` 语句的作用域。

r[destructors.scope.nesting.statement]
* 语句作用域的父作用域是包含该语句的块的作用域。

r[destructors.scope.nesting.match-guard]
* `match` 守卫表达式的父作用域是该守卫所属分支的作用域。

r[destructors.scope.nesting.match-arm]
* `match` 表达式中 `=>` 之后表达式的父作用域是它所在分支的作用域。

r[destructors.scope.nesting.match]
* 分支作用域的父作用域是它所属的 `match` 表达式的作用域。

r[destructors.scope.nesting.other]
* 所有其他作用域的父作用域是紧邻外围表达式的作用域。

r[destructors.scope.params]
### 函数参数的作用域

所有函数参数都处于整个函数体的作用域中，因此在求值该函数时最后被 drop。每个实际函数参数在该参数模式中引入的任何绑定之后被 drop。

```rust
## struct PrintOnDrop(&'static str);
## impl Drop for PrintOnDrop {
##     fn drop(&mut self) {
##         println!("drop({})", self.0);
##     }
## }
// 先 drop `y`，然后是第二个参数，然后是 `x`，然后是第一个参数
fn patterns_in_parameters(
    (x, _): (PrintOnDrop, PrintOnDrop),
    (_, y): (PrintOnDrop, PrintOnDrop),
) {}

// drop 顺序是 3 2 0 1
patterns_in_parameters(
    (PrintOnDrop("0"), PrintOnDrop("1")),
    (PrintOnDrop("2"), PrintOnDrop("3")),
);
```

r[destructors.scope.bindings]
### 局部变量的作用域

r[destructors.scope.bindings.let]
在 `let` 语句中声明的局部变量关联到包含该 `let` 语句的块的作用域。

```rust
## struct PrintOnDrop(&'static str);
## impl Drop for PrintOnDrop {
##     fn drop(&mut self) {
##         println!("drop({})", self.0);
##     }
## }
let declared_first = PrintOnDrop("Dropped last in outer scope");
{
    let declared_in_block = PrintOnDrop("Dropped in inner scope");
}
let declared_last = PrintOnDrop("Dropped first in outer scope");
```

r[destructors.scope.bindings.match-arm]
在 `match` 表达式或模式匹配的 `match` 守卫中声明的局部变量关联到它们所声明于的 `match` 分支的分支作用域。

```rust
## #![allow(irrefutable_let_patterns)]
## struct PrintOnDrop(&'static str);
## impl Drop for PrintOnDrop {
##     fn drop(&mut self) {
##         println!("drop({})", self.0);
##     }
## }
match PrintOnDrop("Dropped last in the first arm's scope") {
    // 当守卫求值成功时，控制流留在该分支中，
    // 值可以从被匹配者移动到该分支的绑定中，
    // 导致它们在该分支的作用域中被 drop。
    x if let y = PrintOnDrop("Dropped second in the first arm's scope")
        && let z = PrintOnDrop("Dropped first in the first arm's scope") =>
    {
        let declared_in_block = PrintOnDrop("Dropped in inner scope");
        // 模式匹配守卫的绑定和临时值按相反顺序 drop，
        // 每个守卫条件操作数的绑定在其临时值之前 drop。
        // 最后，由该分支模式绑定的变量被 drop。
    }
    _ => unreachable!(),
}

match PrintOnDrop("Dropped in the enclosing temporary scope") {
    // 当守卫求值失败时，控制流离开该分支作用域，
    // 导致较早的模式匹配守卫条件操作数中的绑定和临时值被 drop。
    // 这发生在求值下一个分支的守卫或函数体之前。
    _ if let y = PrintOnDrop("Dropped in the first arm's scope")
        && false => unreachable!(),
    // 当因自重叠的或模式而多次执行守卫时，
    // 守卫失败时控制流离开该分支作用域，
    // 并在再次执行守卫之前重新进入该分支作用域。
    _ | _ if let y = PrintOnDrop("Dropped in the second arm's scope twice")
        && false => unreachable!(),
    _ => {},
}
```

r[destructors.scope.bindings.patterns]
模式中的变量按模式内声明的相反顺序 drop。

```rust
## struct PrintOnDrop(&'static str);
## impl Drop for PrintOnDrop {
##     fn drop(&mut self) {
##         println!("drop({})", self.0);
##     }
## }
let (declared_first, declared_last) = (
    PrintOnDrop("Dropped last"),
    PrintOnDrop("Dropped first"),
);
```

r[destructors.scope.bindings.or-patterns]
就 drop 顺序而言，[或模式][or-patterns]按第一个子模式给出的顺序声明绑定。

```rust
## struct PrintOnDrop(&'static str);
## impl Drop for PrintOnDrop {
##     fn drop(&mut self) {
##         println!("drop({})", self.0);
##     }
## }
// 先 drop `x` 再 drop `y`。
fn or_pattern_drop_order<T>(
    (Ok([x, y]) | Err([y, x])): Result<[T; 2], [T; 2]>
//   ^^^^^^^^^^   ^^^^^^^^^^^ 这是第二个子模式。
//   |
//   这是第一个子模式。
//
//   在第一个子模式中，`x` 在 `y` 之前声明。由于它是
//   第一个子模式，即使匹配的是第二个子模式
//   （其中绑定以相反顺序声明），也使用该顺序。
) {}

// 此处我们匹配第一个子模式，drop 按照
// 第一个子模式中的声明顺序发生。
or_pattern_drop_order(Ok([
    PrintOnDrop("Declared first, dropped last"),
    PrintOnDrop("Declared last, dropped first"),
]));

// 此处我们匹配第二个子模式，drop 仍然按照
// 第一个子模式中的声明顺序发生。
or_pattern_drop_order(Err([
    PrintOnDrop("Declared last, dropped first"),
    PrintOnDrop("Declared first, dropped last"),
]));
```

r[destructors.scope.temporary]
### 临时值作用域

r[destructors.scope.temporary.intro]
表达式的 *临时值作用域* 是当该表达式用在[位置上下文][place context]中时，用于保存该表达式结果的临时变量所使用的作用域，除非它被[提升][promoted]。

r[destructors.scope.temporary.enclosing]
除生命周期延长外，表达式的临时值作用域是包含该表达式且为以下之一的最小作用域：

* 整个函数。
* 一个语句。
* [`if`]、[`while`] 或 [`loop`] 表达式的函数体。
* `if` 表达式的 `else` 块。
* `if` 或 `while` 表达式的非模式匹配条件表达式，或非模式匹配的 `match` [守卫条件操作数][guard condition operand]。
* `match` 分支的模式匹配守卫（若存在）以及函数体表达式。
* [惰性布尔表达式][lazy boolean expression]的每个操作数。
* [`if`] 的模式匹配条件以及相应的函数体（[destructors.scope.temporary.edition2024]）。
* [`while`] 的模式匹配条件和循环体。
* 块的尾表达式的整体（[destructors.scope.temporary.edition2024]）。

> **注意**
> `match` 表达式的[被匹配者][scrutinee]不是临时值作用域，因此被匹配者中的临时值可以在 `match` 表达式之后被 drop。例如，`match 1 { ref mut z => z };` 中 `1` 的临时值存活到该语句结束。

> **注意**
> [解构赋值][destructuring assignment]的脱糖会限制其被赋值为操作数（RHS）的临时值作用域。细节参见 [expr.assign.destructure.tmp-scopes]。

r[destructors.scope.temporary.edition2024]
> [!EDITION-2024]
> 2024 edition 添加了两条新的临时值作用域收窄规则：`if let` 的临时值在 `else` 块之前被 drop，块的尾表达式的临时值在尾表达式求值之后立即被 drop。

一些例子：

```rust
## #![allow(irrefutable_let_patterns)]
## struct PrintOnDrop(&'static str);
## impl Drop for PrintOnDrop {
##     fn drop(&mut self) {
##         println!("drop({})", self.0);
##     }
## }
let local_var = PrintOnDrop("local var");

// 一旦条件求值完毕就被 drop
if PrintOnDrop("If condition").0 == "If condition" {
    // 在块结束时 drop
    PrintOnDrop("If body").0
} else {
    unreachable!()
};

if let "if let scrutinee" = PrintOnDrop("if let scrutinee").0 {
    PrintOnDrop("if let consequent").0
    // `if let consequent` 在此处 drop
}
// `if let scrutinee` 在此处 drop
else {
    PrintOnDrop("if let else").0
    // `if let else` 在此处 drop
};

while let x = PrintOnDrop("while let scrutinee").0 {
    PrintOnDrop("while let loop body").0;
    break;
    // `while let loop body` 在此处 drop。
    // `while let scrutinee` 在此处 drop。
}

// 在第一个 || 之前 drop
(PrintOnDrop("first operand").0 == ""
// 在 ) 之前 drop
|| PrintOnDrop("second operand").0 == "")
// 在 ; 之前 drop
|| PrintOnDrop("third operand").0 == "";

// 被匹配者在函数结束时、局部变量之前 drop
// （因为这是函数体块的尾表达式）。
match PrintOnDrop("Matched value in final expression") {
    // 非模式匹配守卫的临时值一旦条件
    // 求值完毕就被 drop
    _ if PrintOnDrop("guard condition").0 == "" => (),
    // 模式匹配守卫的临时值在离开该
    // 分支作用域时 drop
    _ if let "guard scrutinee" = PrintOnDrop("guard scrutinee").0 => {
        let _ = &PrintOnDrop("lifetime-extended temporary in inner scope");
        // `lifetime-extended temporary in inner scope` 在此处 drop
    }
    // `guard scrutinee` 在此处 drop
    _ => (),
}
```

r[destructors.scope.operands]
### 操作数

也会创建临时值来在求值其他操作数时保存表达式某个操作数的结果。这些临时值关联到带有该操作数的表达式的作用域。由于这些临时值在表达式求值后被移出，除非表达式的某个操作数跳出该表达式、返回或 [panic][panic]，drop 它们没有效果。

```rust
## struct PrintOnDrop(&'static str);
## impl Drop for PrintOnDrop {
##     fn drop(&mut self) {
##         println!("drop({})", self.0);
##     }
## }
loop {
    // 元组表达式未完成求值，因此操作数按相反顺序 drop
    (
        PrintOnDrop("Outer tuple first"),
        PrintOnDrop("Outer tuple second"),
        (
            PrintOnDrop("Inner tuple first"),
            PrintOnDrop("Inner tuple second"),
            break,
        ),
        PrintOnDrop("Never created"),
    );
}
```

r[destructors.scope.const-promotion]
### 常量提升

当值表达式可以写在常量中并被借用，并且该借用可以在原先书写该表达式的地方被解引用而不改变运行时行为时，会发生将该表达式提升到 `'static` 槽位。也就是说，被提升的表达式可以在编译时求值，并且结果值不包含[内部可变性][interior mutability]或[析构器][destructors]（这些性质尽可能根据值来确定，例如 `&None` 总是具有类型 `&'static Option<_>`，因为它不包含任何不允许的内容）。

r[destructors.scope.lifetime-extension]
### 临时值生命周期延长

> **注意**
> 临时值生命周期延长的确切规则可能会改变。这里只描述当前行为。

r[destructors.scope.lifetime-extension.let]
`let` 语句中表达式的临时值作用域有时会被 *延长* 到包含该 `let` 语句的块的作用域。当通常的临时值作用域太小、基于某些语法规则时会这样做。例如：

```rust
let x = &mut 0;
// 通常临时值到现在会被 drop，但 `0` 的临时值
// 存活到块结束。
println!("{}", x);
```

r[destructors.scope.lifetime-extension.static]
生命周期延长也适用于 `static` 和 `const` 项，它使临时值存活到程序结束。例如：

```rust
const C: &Vec<i32> = &Vec::new();
// 通常这将是悬垂引用，因为 `Vec` 只会
// 存在于 `C` 的初始化表达式内部，但借用
// 被生命周期延长，因此它实际上具有 `'static` 生命周期。
println!("{:?}", C);
```

r[destructors.scope.lifetime-extension.sub-expressions]
若[借用][borrow]、[解引用][dereference expression]、[字段][field expression]或[元组索引表达式][tuple indexing expression]具有延长的临时值作用域，则其操作数也具有。若[索引表达式][indexing expression]具有延长的临时值作用域，则被索引的表达式也具有延长的临时值作用域。

r[destructors.scope.lifetime-extension.patterns]
#### 基于模式的延长

r[destructors.scope.lifetime-extension.patterns.extending]
*延长模式* 是以下之一：

* 按引用或可变引用绑定的[标识符模式][identifier pattern]。

  ```rust
  # fn temp() {}
  let ref x = temp(); // 按引用绑定。
  # x;
  let ref mut x = temp(); // 按可变引用绑定。
  # x;
  ```

* [结构体][struct pattern]、[元组][tuple pattern]、[元组结构体][tuple struct pattern]、[切片][slice pattern]或[或模式][or-patterns]，其中至少一个直接子模式是延长模式。

  ```rust
  # use core::sync::atomic::{AtomicU64, Ordering::Relaxed};
  # static X: AtomicU64 = AtomicU64::new(0);
  struct W<T>(T);
  # impl<T> Drop for W<T> { fn drop(&mut self) { X.fetch_add(1, Relaxed); } }
  let W { 0: ref x } = W(()); // 结构体模式。
  # x;
  let W(ref x) = W(()); // 元组结构体模式。
  # x;
  let (W(ref x),) = (W(()),); // 元组模式。
  # x;
  let [W(ref x), ..] = [W(())]; // 切片模式。
  # x;
  let (Ok(W(ref x)) | Err(&ref x)) = Ok(W(())); // 或模式。
  # x;
  //
  // 上面所有临时值在此处仍然存活。
  # assert_eq!(0, X.load(Relaxed));
  ```

因此 `ref x`、`V(ref x)` 和 `[ref x, y]` 都是延长模式，但 `x`、`&ref x` 和 `&(ref x,)` 不是。

r[destructors.scope.lifetime-extension.patterns.let]
若 `let` 语句中的模式是延长模式，则初始化表达式的临时值作用域被延长。

```rust
## fn temp() {}
// 这是延长模式，因此临时值作用域被延长。
let ref x = *&temp(); // 正确
## x;
```

```rust
## fn temp() {}
// 这既不是延长模式也不是延长表达式，
// 因此临时值在分号处被 drop。
let &ref x = *&&temp(); // 错误
## x;
```

```rust
## fn temp() {}
// 这不是延长模式，但是延长表达式，
// 因此临时值存活到 `let` 语句之后。
let &ref x = &*&temp(); // 正确
## x;
```

r[destructors.scope.lifetime-extension.exprs]
#### 基于表达式的延长

r[destructors.scope.lifetime-extension.exprs.extending]
对于带有初始化表达式的 let 语句，*延长表达式* 是以下之一的表达式：

* 初始化表达式。
* 延长[借用][borrow]表达式的操作数。
* 延长[超宏调用][super macro call]表达式的[超操作数][super operands]。
* 延长[数组][array expression]、[强制转换][cast expression]、[带花括号的结构体][struct expression]或[元组][tuple expression]表达式的操作数。
* 延长[元组结构体][tuple struct]或[元组枚举变体][tuple enum variant]构造表达式的实参。
* 延长[块表达式][block expression]的最终表达式，[async 块表达式][async block expression]除外。
* 延长 [`if`] 表达式的 then、`else if` 或 `else` 块的最终表达式。
* 延长 [`match`] 表达式的分支表达式。

> **注意**
> [解构赋值][destructuring assignment]的脱糖使其被赋值为操作数（RHS）在新引入的块内成为延长表达式。细节参见 [expr.assign.destructure.tmp-ext]。

因此 `&mut 0`、`(&1, &mut 2)` 和 `Some(&mut 3)` 中的借用表达式都是延长表达式。`&0 + &1` 和 `f(&mut 0)` 中的借用不是。

r[destructors.scope.lifetime-extension.exprs.borrows]
延长[借用][borrow]表达式的操作数具有被[延长][extended]的[临时值作用域][temporary scope]。

r[destructors.scope.lifetime-extension.exprs.super-macros]
延长[超宏调用][super macro call]表达式的[超临时值][super temporaries]具有被[延长][extended]的[作用域][temporary scopes]。

> **注意**
> `rustc` 不将延长[数组][array]表达式的[数组重复操作数][array repeat operands]视为延长表达式。是否应当如此是一个未决问题。
>
> 细节参见 [Rust issue #146092](https://github.com/rust-lang/rust/issues/146092)。

#### 示例

以下是一些表达式具有延长临时值作用域的例子：

```rust
## use core::pin::pin;
## use core::sync::atomic::{AtomicU64, Ordering::Relaxed};
## static X: AtomicU64 = AtomicU64::new(0);
## #[derive(Debug)] struct S;
## impl Drop for S { fn drop(&mut self) { X.fetch_add(1, Relaxed); } }
## const fn temp() -> S { S }
let x = &temp(); // 借用的操作数。
## x;
let x = &raw const *&temp(); // 裸借用的操作数。
## assert_eq!(X.load(Relaxed), 0);
let x = &temp() as &dyn Send; // 强制转换的操作数。
## x;
let x = (&*&temp(),); // 元组构造器的操作数。
## x;
struct W<T>(T);
let x = W(&temp()); // 元组结构体构造器的实参。
## x;
let x = Some(&temp()); // 元组枚举变体构造器的实参。
## x;
let x = { [Some(&temp())] }; // 块的最终表达式。
## x;
let x = const { &temp() }; // `const` 块的最终表达式。
## x;
let x = unsafe { &temp() }; // `unsafe` 块的最终表达式。
## x;
let x = if true { &temp() } else { &temp() };
//              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
//           `if`/`else` 块的最终表达式。
## x;
let x = match () { _ => &temp() }; // `match` 分支表达式。
## x;
let x = pin!(temp()); // 超宏调用表达式的超操作数。
## x;
let x = pin!({ &mut temp() }); // 同上。
## x;
let x = format_args!("{:?}", temp()); // 同上。
## x;
//
// 上面所有临时值在此处仍然存活。
## assert_eq!(0, X.load(Relaxed));
```

以下是一些表达式不具有延长临时值作用域的例子：

```rust
## fn temp() {}
// 函数调用的实参不是延长表达式。
// 临时值在分号处被 drop。
let x = core::convert::identity(&temp()); // 错误
## x;
```

```rust
## fn temp() {}
## trait Use { fn use_temp(&self) -> &Self { self } }
## impl Use for () {}
// 方法调用的接收者不是延长表达式。
let x = (&temp()).use_temp(); // 错误
## x;
```

```rust
## fn temp() {}
// match 表达式的被匹配者不是延长表达式。
let x = match &temp() { x => x }; // 错误
## x;
```

```rust
## fn temp() {}
// `async` 块的最终表达式不是延长表达式。
let x = async { &temp() }; // 错误
## x;
```

```rust
## fn temp() {}
// 闭包的最终表达式不是延长表达式。
let x = || &temp(); // 错误
## x;
```

```rust
## fn temp() {}
// 循环 break 的操作数不是延长表达式。
let x = loop { break &temp() }; // 错误
## x;
```

```rust
## fn temp() {}
// 跳转到标签的 break 的操作数不是延长表达式。
let x = 'a: { break 'a &temp() }; // 错误
## x;
```

```rust
## use core::pin::pin;
## fn temp() {}
// `pin!` 的实参仅当该调用是延长表达式时
// 才是延长表达式。由于它不是，内部块不是
// 延长表达式，因此其尾表达式中的临时值
// 被立即 drop。
pin!({ &temp() }); // 错误
```

```rust
## fn temp() {}
// 同上。
format_args!("{:?}", { &temp() }); // 错误
```

r[destructors.forget]
## 不运行析构器

r[destructors.manually-suppressing]
### 手动抑制析构器

可以使用 [`core::mem::forget`] 阻止运行变量的析构器，[`core::mem::ManuallyDrop`] 提供了一个包装器来阻止变量或字段被自动 drop。

> **注意**
> 即使类型不是 `'static`，通过 [`core::mem::forget`] 或其他方式阻止运行析构器也是安全的。除本文档所定义的保证会运行析构器的位置外，类型 *不得* 为了可靠性而安全地依赖析构器被运行。

r[destructors.process-termination]
### 不展开地终止进程

有一些不经[展开][unwinding]而终止进程的方式，在这种情况下不会运行析构器。

标准库提供 [`std::process::exit`] 和 [`std::process::abort`] 来显式这样做。此外，若 [panic 处理程序][panic.panic_handler.std] 设置为 `abort`，panic 将总是终止进程而不运行析构器。

还有一种额外情形需要注意：当 panic 到达[不展开的 ABI 边界][non-unwinding ABI boundary]时，要么不运行任何析构器，要么运行直到该 ABI 边界为止的所有析构器。

[Assignment]: expressions/operator-expr.md#assignment-expressions
[binding modes]: patterns.md#binding-modes
[closure]: types/closure.md
[destructors]: destructors.md
[destructuring assignment]: expr.assign.destructure
[expression]: expressions.md
[guard condition operand]: expressions/match-expr.md#match-guard-chains
[identifier pattern]: patterns.md#identifier-patterns
[initialized]: glossary.md#initialized
[interior mutability]: interior-mutability.md
[lazy boolean expression]: expressions/operator-expr.md#lazy-boolean-operators
[non-unwinding ABI boundary]: items/functions.md#unwinding
[panic]: panic.md
[place context]: expressions.md#place-expressions-and-value-expressions
[promoted]: destructors.md#constant-promotion
[scrutinee]: glossary.md#scrutinee
[statement]: statements.md
[temporary]: expressions.md#temporaries
[unwinding]: panic.md#unwinding
[variable]: variables.md

[array]: types/array.md
[enum variant]: types/enum.md
[slice]: types/slice.md
[struct]: types/struct.md
[Trait objects]: types/trait-object.md
[tuple]: types/tuple.md

[or-patterns]: patterns.md#or-patterns
[slice pattern]: patterns.md#slice-patterns
[struct pattern]: patterns.md#struct-patterns
[tuple pattern]: patterns.md#tuple-patterns
[tuple struct pattern]: patterns.md#tuple-struct-patterns
[tuple struct]: type.struct.tuple
[tuple enum variant]: type.enum.declaration

[array expression]: expressions/array-expr.md#array-expressions
[array repeat operands]: expr.array.repeat-operand
[async block expression]: expr.block.async
[block expression]: expressions/block-expr.md
[borrow]: expr.operator.borrow
[cast expression]: expressions/operator-expr.md#type-cast-expressions
[dereference expression]: expressions/operator-expr.md#the-dereference-operator
[extended]: destructors.scope.lifetime-extension
[field expression]: expressions/field-expr.md
[indexing expression]: expressions/array-expr.md#array-and-slice-indexing-expressions
[struct expression]: expressions/struct-expr.md
[super macro call]: expr.super-macros
[super operands]: expr.super-macros
[super temporaries]: expr.super-macros
[temporary scope]: destructors.scope.temporary
[temporary scopes]: destructors.scope.temporary
[tuple expression]: expressions/tuple-expr.md#tuple-expressions
[tuple indexing expression]: expressions/tuple-expr.md#tuple-indexing-expressions

[`for`]: expressions/loop-expr.md#iterator-loops
[`if let`]: expressions/if-expr.md#if-let-patterns
[`if`]: expressions/if-expr.md#if-expressions
[`let` statement]: statements.md#let-statements
[`loop`]: expressions/loop-expr.md#infinite-loops
[`match`]: expressions/match-expr.md
[`while let`]: expressions/loop-expr.md#while-let-patterns
[`while`]: expressions/loop-expr.md#predicate-loops
