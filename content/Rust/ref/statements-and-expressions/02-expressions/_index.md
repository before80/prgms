+++
title = "02-表达式"
date = 2026-08-18T08:45:00+08:00
weight = 43
type = "docs"
description = "表达式 — The Rust Reference"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Reference](https://doc.rust-lang.org/reference/)

> 原文链接: [https://doc.rust-lang.org/reference/expressions.html](https://doc.rust-lang.org/reference/expressions.html)

r[expr]
# 表达式

r[expr.syntax]
```grammar,expressions
Expression ->
      ExpressionWithoutBlock
    | ExpressionWithBlock

ExpressionWithoutBlock ->
    OuterAttribute* ExpressionWithoutBlockNoAttrs

ExpressionWithoutBlockNoAttrs ->
      LiteralExpression
    | PathExpression
    | OperatorExpression
    | GroupedExpression
    | ArrayExpression
    | AwaitExpression
    | IndexExpression
    | TupleExpression
    | TupleIndexingExpression
    | StructExpression
    | CallExpression
    | MethodCallExpression
    | FieldExpression
    | ClosureExpression
    | AsyncBlockExpression
    | ContinueExpression
    | BreakExpression
    | RangeExpression
    | ReturnExpression
    | UnderscoreExpression
    | MacroInvocation

ExpressionWithBlock ->
    OuterAttribute* ExpressionWithBlockNoAttrs

ExpressionWithBlockNoAttrs ->
      BlockExpression
    | ConstBlockExpression
    | UnsafeBlockExpression
    | LoopExpression
    | IfExpression
    | MatchExpression
```

r[expr.intro]
表达式可以有两种角色：它总是产生一个*值*，并且可能具有*效果*（也称为“副作用”）。

r[expr.evaluation]
表达式*求值为*一个值，并在*求值*期间产生效果。

r[expr.operands]
许多表达式包含子表达式，称为该表达式的*操作数*。

r[expr.behavior]
每种表达式的含义规定了若干事项：

* 求值该表达式时是否求值其操作数
* 求值操作数的顺序
* 如何组合操作数的值以得到该表达式的值

r[expr.structure]
如此，表达式的结构决定了执行的结构。块只是另一种表达式，因此块、语句、表达式以及块可以彼此递归嵌套到任意深度。

> **注意**
> 我们为表达式的操作数命名以便讨论，但这些名称并不稳定，可能会更改。

r[expr.precedence]
## 表达式优先级

Rust 运算符和表达式的优先级按如下顺序从强到弱排列。同一优先级的二元运算符按其结合性所给出的顺序分组。

| 运算符/表达式         | 结合性       |
|-----------------------------|---------------------|
| [路径][expr.path]          |                     |
| [方法调用][expr.method] |                     |
| [字段表达式][expr.field] | 从左到右   |
| [函数调用][expr.call]，[数组索引][expr.array.index] | |
| [`?`][expr.try]             |                     |
| 一元 [`-`][expr.negate] [`!`][expr.negate] [`*`][expr.deref] [借用][expr.operator.borrow] | |
| [`as`][expr.as]             | 从左到右       |
| [`*`][expr.arith-logic] [`/`][expr.arith-logic] [`%`][expr.arith-logic] | 从左到右       |
| [`+`][expr.arith-logic] [`-`][expr.arith-logic] | 从左到右       |
| [`<<`][expr.arith-logic] [`>>`][expr.arith-logic] | 从左到右     |
| [`&`][expr.arith-logic]     | 从左到右       |
| [`^`][expr.arith-logic]     | 从左到右       |
| [<code>&#124;</code>][expr.arith-logic] | 从左到右       |
| [`==`][expr.cmp] [`!=`][expr.cmp] [`<`][expr.cmp] [`>`][expr.cmp] [`<=`][expr.cmp] [`>=`][expr.cmp] | 需要括号 |
| [`&&`][expr.bool-logic]     | 从左到右       |
| [<code>&#124;&#124;</code>][expr.bool-logic] | 从左到右       |
| [`..`][expr.range] [`..=`][expr.range] | 需要括号 |
| [`=`][expr.assign] [`+=`][expr.compound-assign] [`-=`][expr.compound-assign] [`*=`][expr.compound-assign] [`/=`][expr.compound-assign] [`%=`][expr.compound-assign] <br> [`&=`][expr.compound-assign] [<code>&#124;=</code>][expr.compound-assign] [`^=`][expr.compound-assign] [`<<=`][expr.compound-assign] [`>>=`][expr.compound-assign] | 从右到左 |
| [`return`][expr.return] [`break`][expr.loop.break] [闭包][expr.closure]  | |

r[expr.operand-order]
## 操作数的求值顺序

r[expr.operand-order.default]
下列表达式都以相同方式求值其操作数，如列表之后所述。其他表达式要么没有操作数，要么按各自页面所述有条件地求值操作数。

* 解引用表达式
* 错误传播表达式
* 取反表达式
* 算术与逻辑二元运算符
* 比较运算符
* 类型转换表达式
* 分组表达式
* 数组表达式
* await 表达式
* 索引表达式
* 元组表达式
* 元组索引表达式
* 结构体表达式
* 调用表达式
* 方法调用表达式
* 字段表达式
* break 表达式
* 区间表达式
* return 表达式

r[expr.operand-order.operands-before-primary]
这些表达式的操作数在应用该表达式的效果之前求值。接受多个操作数的表达式按源代码中书写的顺序从左到右求值。

> **注意**
> 哪些子表达式是某表达式的操作数，由上一节的表达式优先级决定。

例如，两次 `next` 方法调用总是按相同顺序进行：

```rust
## // 使用 vec 而非数组以避免引用，
## // 因为编写此示例时还没有稳定的
## // 拥有所有权的数组迭代器。
let mut one_two = vec![1, 2].into_iter();
assert_eq!(
    (1, 2),
    (one_two.next().unwrap(), one_two.next().unwrap())
);
```

> **注意**
> 由于这是递归应用的，这些表达式也从最内层到最外层求值，在没有更内层的子表达式之前会忽略兄弟表达式。

r[expr.place-value]
## 位置表达式与值表达式

r[expr.place-value.intro]
表达式分为两大类：位置表达式和值表达式；还有第三类较小的范畴，称为赋值目标表达式。在每个表达式内部，操作数同样可能出现在位置上下文或值上下文中。表达式的求值既取决于它自身的类别，也取决于它所处的上下文。

r[expr.place-value.place-memory-location]
*位置表达式*是表示内存位置的表达式。

r[expr.place-value.place-expr-kinds]
这些表达式是引用局部变量的[路径][paths]、[静态变量][static variables]、[解引用][deref]（`*expr`）、[数组索引][array indexing]表达式（`expr[expr]`）、[字段][field]引用（`expr.f`）以及圆括号括起的位置表达式。

r[expr.place-value.value-expr-kinds]
所有其他表达式都是值表达式。

r[expr.place-value.value-result]
*值表达式*是表示实际值的表达式。

r[expr.place-value.place-context]
下列上下文是*位置表达式*上下文：

* [复合赋值][compound assignment]表达式的左操作数。
* 一元[借用][borrow]、[裸借用][raw borrow]或[解引用][deref]运算符的操作数。
* [字段表达式][field expression]的操作数。
* [数组索引表达式][array indexing expression]中被索引的操作数。
* [元组索引表达式][tuple indexing expression]的元组操作数。
* 任何[隐式借用][implicit borrow]的操作数。
* [`let` 语句][let statement]的初始化器。
* [`if let`]、[`match`][match] 或 [`while let`] 表达式的[被检视表达式][scrutinee]。
* [函数式更新][functional update]结构体表达式的基值。

> **注意**
> 历史上，位置表达式曾被称为 *lvalue*（左值），值表达式曾被称为 *rvalue*（右值）。

r[expr.place-value.assignee]
*赋值目标表达式*是出现在[赋值][assign]表达式左操作数中的表达式。具体而言，赋值目标表达式是：

- 位置表达式。
- [下划线][Underscores]。
- 由赋值目标表达式组成的[元组][Tuples]。
- 由赋值目标表达式组成的[切片][expr.array.index]。
- 由赋值目标表达式组成的[元组结构体][Tuple structs]。
- 由赋值目标表达式组成的[结构体][Structs]（字段可选具名）。
- [单元结构体][Unit structs]

r[expr.place-value.parenthesis]
赋值目标表达式内部允许任意加括号。

r[expr.move]
### 移动与复制的类型

r[expr.move.intro]
当位置表达式在值表达式上下文中被求值，或在模式中按值绑定，它表示该内存位置_中_所持有的值。

r[expr.move.copy]
若该值的类型实现了 [`Copy`]，则该值会被复制。

r[expr.move.requires-sized]
在其余情况下，若该类型是 [`Sized`]，则可能可以移动该值。

r[expr.move.movable-place]
只有下列位置表达式可以从中移出：

* 当前未被借用的[变量][Variables]。
* [临时值](#temporaries)。
* 可被移出且未实现 [`Drop`] 的位置表达式的[字段][field]。
* [解引用][deref]类型为 [`Box<T>`] 的表达式的结果，且该表达式本身也可以被移出。

r[expr.move.deinitialization]
从求值为局部变量的位置表达式中移出之后，该位置被去初始化，在重新初始化之前不能再读取。

r[expr.move.place-invalid]
在所有其他情况下，试图在值表达式上下文中使用位置表达式都是错误。

r[expr.mut]
### 可变性

r[expr.mut.intro]
位置表达式要被[赋值][assign]、可变[借用][borrow]、[隐式可变借用][implicitly mutably borrowed]，或绑定到含 `ref mut` 的模式，它必须是_可变的_。我们称这些为*可变位置表达式*。相对地，其他位置表达式称为*不可变位置表达式*。

r[expr.mut.valid-places]
下列表达式可以成为可变位置表达式上下文：

* 当前未被借用的可变[变量][Variables]。
* [可变 `static` 项][Mutable `static` items]。
* [临时值][Temporary values]。
* [字段][field]：这会在可变位置表达式上下文中求值子表达式。
* 对 `*mut T` 指针的[解引用][deref]。
* 对类型为 `&mut T` 的变量或其字段的解引用。注意：这是下一条规则要求的例外。
* 对实现了 `DerefMut` 的类型的解引用：这进而要求被解引用的值在可变位置表达式上下文中求值。
* 对实现了 `IndexMut` 的类型的[数组索引][Array indexing]：这会在可变位置表达式上下文中求值被索引的值，但不求值索引。

r[expr.temporary]
### 临时值

当在大多数位置表达式上下文中使用值表达式时，会创建一个未命名的临时内存位置，并初始化为该值。表达式求值为该位置，除非它被[提升][promoted]为 `static`。该临时值的[drop 作用域][drop scope]通常是包围语句的末尾。

r[expr.super-macros]
### 超宏

r[expr.super-macros.intro]
某些内置宏可能创建其[作用域][temporary scopes]可被[延长][extended]的[临时值][temporaries]。这些临时值是*超临时值*，这些宏是*超宏*。这些宏的[调用][macro invocations]是*超宏调用表达式*。这些宏的实参可能是*超操作数*。

> **注意**
> 当超宏调用表达式是[延长表达式][extending expression]时，其超操作数是[延长表达式][extending expressions]，且超临时值的[作用域][temporary scopes]会被[延长][extended]。见 [destructors.scope.lifetime-extension.exprs]。

r[expr.super-macros.format_args]
#### `format_args!`

r[expr.super-macros.format_args.super-operands]
除格式字符串实参外，传给 [`format_args!`] 的所有实参都是*超操作数*。

```rust
## fn temp() -> String { String::from("") }
// 由于该调用是延长表达式，且该实参是超操作数，
// 内部块也是延长表达式，因此其尾表达式中
// 创建的临时值的作用域被延长。
let _ = format_args!("{}", { &temp() }); // 正确
```

r[expr.super-macros.format_args.super-temporaries]
[`format_args!`] 的超操作数会被[隐式借用][implicitly borrowed]，因此是[位置表达式上下文][place expression contexts]。当以[值表达式][value expression]作为实参传入时，会创建一个*超临时值*。

```rust
## fn temp() -> String { String::from("") }
let x = format_args!("{}", temp());
x; // <-- 临时值被延长，因而可以在此处使用。
```

对 [`format_args!`] 的调用展开有时会创建其他内部*超临时值*。

```rust
let x = {
    // 此次调用会创建一个内部临时值。
    let x = format_args!("{:?}", 0);
    x // <-- 临时值被延长，因而可以在此处使用。
}; // <-- 临时值在此处被 drop。
x; // 错误
```

```rust
// 此次调用不会创建内部临时值。
let x = { let x = format_args!("{}", 0); x };
x; // 正确
```

> **注意**
> [`format_args!`] 何时会或不创建内部临时值的细节目前尚未规定。

r[expr.super-macros.pin]
#### `pin!`

r[expr.super-macros.pin.super-operands]
[`pin!`] 的实参是*超操作数*。

```rust
## use core::pin::pin;
## fn temp() {}
// 与上文 `format_args!` 的情况相同。
let _ = pin!({ &temp() }); // 正确
```

r[expr.super-macros.pin.super-temporaries]
[`pin!`] 的实参是[值表达式上下文][value expression context]，并创建一个*超临时值*。

```rust
## use core::pin::pin;
## fn temp() {}
// 该实参被求值到一个超临时值中。
let x = pin!(temp());
// 临时值被延长，因而可以在此处使用。
x; // 正确
```

r[expr.implicit-borrow]
### 隐式借用

r[expr.implicit-borrow-intro]
某些表达式会通过隐式借用把一个表达式当作位置表达式。例如，可以直接比较两个不定大小的[切片][slice]是否相等，因为 `==` 运算符会隐式借用其操作数：

```rust
## let c = [1, 2, 3];
## let d = vec![1, 2, 3];
let a: &[i32];
let b: &[i32];
## a = &c;
## b = &d;
// ...
*a == *b;
// 等价形式：
::std::cmp::PartialEq::eq(&*a, &*b);
```

r[expr.implicit-borrow.application]
下列表达式中可能发生隐式借用：

* [方法调用][method-call]表达式中的左操作数。
* [字段][field]表达式中的左操作数。
* [调用表达式][call expressions]中的左操作数。
* [数组索引][array indexing]表达式中的左操作数。
* [解引用运算符][deref]（`*`）的操作数。
* [比较][comparison]的操作数。
* [复合赋值][compound assignment]的左操作数。
* [`format_args!`] 的实参，格式字符串除外。

r[expr.overload]
## 重载 trait

下列许多运算符和表达式也可以通过 `std::ops` 或 `std::cmp` 中的 trait 为其他类型重载。这些 trait 在 `core::ops` 和 `core::cmp` 中也以相同名称存在。

r[expr.attr]
## 表达式属性

r[expr.attr.restriction]
表达式之前的[外部属性][Outer attributes]仅在少数特定情况下允许：

* 用作[语句][statement]的表达式之前。
* [数组表达式][array expressions]、[元组表达式][tuple expressions]、[调用表达式][call expressions]以及类元组[结构体][struct]表达式的元素。
* [块表达式][block expressions]的尾表达式。
<!-- Keep list in sync with block-expr.md -->

r[expr.attr.never-before]
它们从不允许出现在下列位置之前：
* [区间][Range]表达式。
* 二元运算符表达式（[ArithmeticOrLogicalExpression]、[ComparisonExpression]、[LazyBooleanExpression]、[TypeCastExpression]、[AssignmentExpression]、[CompoundAssignmentExpression]）。

[`Box<T>`]:             special-types-and-traits.md#boxt
[`Copy`]:               special-types-and-traits.md#copy
[`Drop`]:               special-types-and-traits.md#drop
[`if let`]:             expressions/if-expr.md#if-let-patterns
[`format_args!`]:       core::format_args
[`pin!`]:               core::pin::pin
[`Sized`]:              special-types-and-traits.md#sized
[`while let`]:          expressions/loop-expr.md#while-let-patterns
[array expressions]:    expressions/array-expr.md
[array indexing]:       expressions/array-expr.md#array-and-slice-indexing-expressions
[array indexing expression]: expr.array.index
[assign]:               expressions/operator-expr.md#assignment-expressions
[block expressions]:    expressions/block-expr.md
[borrow]:               expressions/operator-expr.md#borrow-operators
[call expressions]:     expressions/call-expr.md
[comparison]:           expressions/operator-expr.md#comparison-operators
[compound assignment]:  expressions/operator-expr.md#compound-assignment-expressions
[deref]:                expressions/operator-expr.md#the-dereference-operator
[destructors]:          destructors.md
[drop scope]:           destructors.md#drop-scopes
[extended]:             destructors.scope.lifetime-extension
[extending expression]: destructors.scope.lifetime-extension.exprs
[extending expressions]: destructors.scope.lifetime-extension.exprs
[field]:                expressions/field-expr.md
[field expression]:     expr.field
[functional update]:    expressions/struct-expr.md#functional-update-syntax
[implicit borrow]:      #implicit-borrows
[implicitly borrowed]:  expr.implicit-borrow
[implicitly mutably borrowed]: #implicit-borrows
[interior mutability]:  interior-mutability.md
[let statement]:        statements.md#let-statements
[macro invocations]:    macro.invocation
[match]:                expressions/match-expr.md
[method-call]:          expressions/method-call-expr.md
[Mutable `static` items]: items/static-items.md#mutable-statics
[Outer attributes]:     attributes.md
[paths]:                expressions/path-expr.md
[place expression contexts]: expr.place-value
[promoted]:             destructors.md#constant-promotion
[Range]:                expressions/range-expr.md
[raw borrow]:           expressions/operator-expr.md#raw-borrow-operators
[scrutinee]:            glossary.md#scrutinee
[slice]:                types/slice.md
[statement]:            statements.md
[static variables]:     items/static-items.md
[struct]:               expressions/struct-expr.md
[Structs]:              expr.struct
[temporaries]:          expr.temporary
[temporary scopes]:     destructors.scope.temporary
[Temporary values]:     #temporaries
[tuple expressions]:    expressions/tuple-expr.md
[tuple indexing expression]: expr.tuple-index
[Tuple structs]:        items.struct.tuple
[Tuples]:               expressions/tuple-expr.md
[Underscores]:          expressions/underscore-expr.md
[Unit structs]:         items.struct.unit
[value expression context]: expr.place-value
[value expression]:     expr.place-value
[Variables]:            variables.md
