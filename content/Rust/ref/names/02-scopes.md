+++
title = "02-作用域"
date = 2026-08-18T08:45:00+08:00
weight = 97
type = "docs"
description = "作用域 — The Rust Reference"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Reference](https://doc.rust-lang.org/reference/)

> 原文链接: [https://doc.rust-lang.org/reference/names/scopes.html](https://doc.rust-lang.org/reference/names/scopes.html)

r[names.scopes]
# 作用域

r[names.scopes.intro]
*作用域*是源文本中可以用该名称引用具名[实体][entity]的区域。以下各节详细说明作用域规则与行为，它们取决于实体的种类及其声明位置。名称如何解析到实体的过程在[名称解析][name resolution]一章中描述。更多关于用于运行析构器的“析构作用域”的信息，可见[析构器][destructors]一章。

r[names.scopes.items]
## 项作用域

r[names.scopes.items.module]
直接在[模块][module]中声明的[项][items]的名称，其作用域从模块开始延伸到模块结束。这些项也是模块的成员，可以通过从其模块出发的[路径][path]引用。

r[names.scopes.items.statement]
作为[语句][statement]声明的项的名称，其作用域从该项语句所在块的开始延伸到该块的结束。

r[names.scopes.items.duplicate]
在同一模块或块内的同一[命名空间][namespace]中，引入与另一项重名的项是错误的。[星号 glob 导入][Asterisk glob imports]在处理重复名称与遮蔽方面有特殊行为，详见所链接章节。

r[names.scopes.items.shadow-prelude]
模块中的项可以遮蔽[prelude](#prelude-scopes)中的项。

r[names.scopes.items.nested-modules]
外层模块的项名称不在嵌套模块的作用域内。可以使用[路径][path]引用另一模块中的项。

r[names.scopes.associated-items]
### 关联项作用域

r[names.scopes.associated-items.scope]
[关联项][Associated items]没有作用域，只能通过从其关联的类型或 trait 出发的[路径][path]引用。[方法][Methods]也可以通过[调用表达式][call expressions]引用。

r[names.scopes.associated-items.duplicate]
与模块或块中的项类似，在 trait 或实现中引入与该 trait 或 impl 在同一命名空间中另一项重名的项是错误的。

r[names.scopes.pattern-bindings]
## 模式绑定作用域

局部变量[模式][pattern]绑定的作用域取决于其使用位置：

r[names.scopes.pattern-bindings.let]
* [`let` 语句][`let` statement]绑定的范围从紧接 `let` 语句之后到其声明所在块的末尾。
r[names.scopes.pattern-bindings.parameter]
* [函数参数][Function parameter]绑定位于函数体内。
r[names.scopes.pattern-bindings.closure]
* [闭包参数][Closure parameter]绑定位于闭包体内。
r[names.scopes.pattern-bindings.loop]
* [`for`] 绑定位于循环体内。
r[names.scopes.pattern-bindings.let-chains]
* [`if let`] 与 [`while let`] 绑定在后续条件以及结果块中有效。
r[names.scopes.pattern-bindings.match-arm]
* [`match` 臂][`match` arms]绑定位于[match 守卫][match guard]与 match 臂表达式内。
r[names.scopes.pattern-bindings.match-guard-let]
* [`match` 守卫 `let`][`match` guard `let`]绑定在后续守卫条件与 match 臂表达式中有效。

r[names.scopes.pattern-bindings.items]
局部变量作用域不会延伸到项声明中。
<!-- Not entirely, see https://github.com/rust-lang/rust/issues/33118 -->

### 模式绑定遮蔽

r[names.scopes.pattern-bindings.shadow]
模式绑定允许遮蔽作用域中的任何名称，但下列情况除外（这些是错误）：

* [常量泛型参数][Const generic parameters]
* [静态项][Static items]
* [常量项][Const items]
* [结构体][structs]与[枚举][enums]的构造函数

下列示例说明局部绑定如何遮蔽项声明：

```rust
fn shadow_example() {
    // 由于作用域中尚无局部变量，这会解析到函数。
    foo(); // 打印 `function`
    let foo = || println!("closure");
    fn foo() { println!("function"); }
    // 这会解析到局部闭包，因为它遮蔽了该项。
    foo(); // 打印 `closure`
}
```

r[names.scopes.generic-parameters]
## 泛型参数作用域

r[names.scopes.generic-parameters.param-list]
泛型参数在 [GenericParams] 列表中声明。泛型参数的作用域位于声明它的项内。

r[names.scopes.generic-parameters.order-independent]
无论声明顺序如何，所有参数都在泛型参数列表的作用域内。以下展示了一些参数可在声明之前被引用的例子：

```rust
// 'b 约束在声明之前被引用。
fn params_scope<'a: 'b, 'b>() {}

## trait SomeTrait<const Z: usize> {}
// 常量 N 在 trait 约束中于声明之前被引用。
fn f<T: SomeTrait<N>, const N: usize>() {}
```

r[names.scopes.generic-parameters.bounds]
泛型参数也在类型约束与 where 子句的作用域内，例如：

```rust
## trait SomeTrait<'a, T> {}
// `SomeTrait` 的 <'a, U> 指 `bounds_scope` 的 'a 与 U 参数。
fn bounds_scope<'a, T: SomeTrait<'a, U>, U>() {}

fn where_scope<'a, T, U>()
    where T: SomeTrait<'a, U>
{}
```

r[names.scopes.generic-parameters.inner-items]
函数内部声明的[项][items]引用其外层作用域的泛型参数是错误的。

```rust
fn example<T>() {
    fn inner(x: T) {} // 错误：不能使用外层函数的泛型参数
}
```

### 泛型参数遮蔽

r[names.scopes.generic-parameters.shadow]
遮蔽泛型参数是错误的，例外是函数内声明的项允许遮蔽该函数的泛型参数名。

```rust
fn example<'a, T, const N: usize>() {
    // 函数内的项允许遮蔽作用域中的泛型参数。
    fn inner_lifetime<'a>() {} // 可以
    fn inner_type<T>() {} // 可以
    fn inner_const<const N: usize>() {} // 可以
}
```

```rust
trait SomeTrait<'a, T, const N: usize> {
    fn example_lifetime<'a>() {} // 错误：'a 已在使用
    fn example_type<T>() {} // 错误：T 已在使用
    fn example_const<const N: usize>() {} // 错误：N 已在使用
    fn example_mixed<const T: usize>() {} // 错误：T 已在使用
}
```

r[names.scopes.lifetimes]
### 生命周期作用域

生命周期参数在 [GenericParams] 列表与[高阶 trait 约束][hrtb]中声明。

r[names.scopes.lifetimes.special]
`'static` 生命周期与[占位符生命周期][placeholder lifetime] `'_` 具有特殊含义，不能声明为参数。

#### 生命周期泛型参数作用域

r[names.scopes.lifetimes.generic]
[常量][Constant]与[静态][static]项以及[常量上下文][const contexts]只允许 `'static` 生命周期引用，因此它们内部不能有其他生命周期在作用域中。[关联常量][Associated consts]确实允许引用其 trait 或实现中声明的生命周期。

#### 高阶 trait 约束作用域

r[names.scopes.lifetimes.higher-ranked]
作为[高阶 trait 约束][hrtb]声明的生命周期参数的作用域取决于其使用场景。

* 作为 [TypeBoundWhereClauseItem] 时，所声明的生命周期在类型与类型约束的作用域内。
* 作为 [TraitBound] 时，所声明的生命周期在约束类型路径的作用域内。
* 作为 [BareFunctionType] 时，所声明的生命周期在函数参数与返回类型的作用域内。

```rust
## trait Trait<'a>{}

fn where_clause<T>()
    // 'a 在类型与类型约束中都在作用域内。
    where for <'a> &'a T: Trait<'a>
{}

fn bound<T>()
    // 'a 在约束内的作用域中。
    where T: for <'a> Trait<'a>
{}

## struct Example<'a> {
##     field: &'a u32
## }

// 'a 在参数与返回类型中都在作用域内。
type FnExample = for<'a> fn(x: Example<'a>) -> Example<'a>;
```

#### Impl trait 限制

r[names.scopes.lifetimes.impl-trait]
[Impl trait] 类型只能引用在函数或实现上声明的生命周期。

<!-- not able to demonstrate the scope error because the compiler panics
     https://github.com/rust-lang/rust/issues/67830
-->
```rust
## trait Trait1 {
##     type Item;
## }
## trait Trait2<'a> {}
#
## struct Example;
#
## impl Trait1 for Example {
##     type Item = Element;
## }
#
## struct Element;
## impl<'a> Trait2<'a> for Element {}
#
// 这里的 `impl Trait2` 不允许引用 'b，但允许
// 引用 'a。
fn foo<'a>() -> impl for<'b> Trait1<Item = impl Trait2<'a> + use<'a>> {
    // ...
##    Example
}
```

r[names.scopes.loop-label]
## 循环标签作用域

r[names.scopes.loop-label.scope]
[循环标签][Loop labels]可由[循环表达式][loop expression]声明。循环标签的作用域从其声明点到循环表达式的末尾。该作用域不会延伸到[项][items]、[闭包][closures]、[异步块][async blocks]、[常量参数][const arguments]、[常量上下文][const contexts]，以及定义它的 [`for` 循环][`for` loop]的迭代器表达式中。

```rust
'a: for n in 0..3 {
    if n % 2 == 0 {
        break 'a;
    }
    fn inner() {
        // 在这里使用 'a 会是错误。
        // break 'a;
    }
}

// 标签在 `while` 循环的表达式中处于作用域内。
'a: while break 'a {}         // 循环不会运行。
'a: while let _ = break 'a {} // 循环不会运行。

// 标签在定义它的 `for` 循环中不在作用域内：
'a: for outer in 0..5 {
    // 这会跳出外层循环，跳过内层循环并停止
    // 外层循环。
    'a: for inner in { break 'a; 0..1 } {
        println!("{}", inner); // 这不会运行。
    }
    println!("{}", outer); // 这也不会运行。
}

```

r[names.scopes.loop-label.shadow]
循环标签可以遮蔽外层作用域中的同名标签。对标签的引用指向最近的定义。

```rust
// 循环标签遮蔽示例。
'a: for outer in 0..5 {
    'a: for inner in 0..5 {
        // 这会终止内层循环，但外层循环继续运行。
        break 'a;
    }
}
```

r[names.scopes.prelude]
## Prelude 作用域

r[names.scopes.prelude.intro]
[Prelude][Preludes]将实体带入每个模块的作用域。这些实体不是模块的成员，但在[名称解析][name resolution]期间会被隐式查询。

r[names.scopes.prelude.shadow]
prelude 名称可被模块中的声明遮蔽。

r[names.scopes.prelude.layers]
prelude 是分层的，若包含同名实体，则一层可遮蔽另一层。prelude 可遮蔽其他 prelude 的顺序如下，靠前的条目可遮蔽靠后的条目：

1. [外部 prelude][Extern prelude]
2. [工具 prelude][Tool prelude]
3. [`macro_use` prelude]
4. [标准库 prelude][Standard library prelude]
5. [语言 prelude][Language prelude]

r[names.scopes.macro_rules]
## `macro_rules` 作用域

`macro_rules` 宏的作用域在[示例宏][Macros By Example]一章中描述。其行为取决于 [`macro_use`] 与 [`macro_export`] 属性的使用。

r[names.scopes.derive]
## 派生宏助手属性

r[names.scopes.derive.scope]
[派生宏助手属性][Derive macro helper attributes]在其对应 [`derive` 属性][`derive` attribute]所指定的项中处于作用域内。作用域从紧接 `derive` 属性之后延伸到该项的末尾。 <!-- Note: Not strictly true, see https://github.com/rust-lang/rust/issues/79202, but this is the intention. -->

r[names.scopes.derive.shadow]
助手属性会遮蔽作用域中同名的其他属性。

r[names.scopes.self]
## `Self` 作用域

r[names.scopes.self.intro]
尽管 [`Self`] 是具有特殊含义的关键字，它与名称解析的交互方式类似于普通名称。

r[names.scopes.self.def-scope]
[结构体][struct]、[枚举][enum]、[联合体][union]、[trait][trait]或[实现][implementation]定义中的隐式 `Self` 类型，其处理方式类似于[泛型参数](#generic-parameter-scopes)，并以与泛型类型参数相同的方式处于作用域内。

r[names.scopes.self.impl-scope]
[实现][implementation]的值[命名空间][namespace]中的隐式 `Self` 构造函数，在实现体（实现的[关联项][associated items]）内处于作用域中。

```rust
// 结构体定义中的 Self 类型。
struct Recursive {
    f1: Option<Box<Self>>
}

// 泛型参数中的 Self 类型。
struct SelfGeneric<T: Into<Self>>(T);

// 实现中的 Self 值构造函数。
struct ImplExample();
impl ImplExample {
    fn example() -> Self { // Self 类型
        Self() // Self 值构造函数
    }
}
```

[`derive` attribute]: ../attributes/derive.md
[`for` loop]: ../expressions/loop-expr.md#iterator-loops
[`for`]: ../expressions/loop-expr.md#iterator-loops
[`if let`]: ../expressions/if-expr.md#if-let-patterns
[`while let`]: ../expressions/loop-expr.md#while-let-patterns
[`let` statement]: ../statements.md#let-statements
[`macro_export`]: ../macros-by-example.md#the-macro_export-attribute
[`macro_use` prelude]: preludes.md#macro_use-prelude
[`macro_use`]: ../macros-by-example.md#the-macro_use-attribute
[`match` arms]: ../expressions/match-expr.md
[`match` guard `let`]: expr.match.guard.let
[`Self`]: ../paths.md#self-1
[Associated consts]: ../items/associated-items.md#associated-constants
[associated items]: ../items/associated-items.md
[Asterisk glob imports]: ../items/use-declarations.md
[async blocks]: ../expressions/block-expr.md#async-blocks
[call expressions]: ../expressions/call-expr.md
[Closure parameter]: ../expressions/closure-expr.md
[closures]: ../expressions/closure-expr.md
[const arguments]: ../items/generics.md#const-generics
[const contexts]: ../const_eval.md#const-context
[Const generic parameters]: ../items/generics.md#const-generics
[Const items]: ../items/constant-items.md
[Constant]: ../items/constant-items.md
[Derive macro helper attributes]: ../procedural-macros.md#derive-macro-helper-attributes
[destructors]: ../destructors.md
[entity]: ../names.md
[enum]: ../items/enumerations.mdr
[enums]: ../items/enumerations.md
[Extern prelude]: preludes.md#extern-prelude
[Function parameter]: ../items/functions.md#function-parameters
[hrtb]: ../trait-bounds.md#higher-ranked-trait-bounds
[Impl trait]: ../types/impl-trait.md
[implementation]: ../items/implementations.md
[items]: ../items.md
[Language prelude]: preludes.md#language-prelude
[loop expression]: ../expressions/loop-expr.md
[Loop labels]: ../expressions/loop-expr.md#loop-labels
[Macros By Example]: ../macros-by-example.md
[match guard]: ../expressions/match-expr.md#match-guards
[methods]: ../items/associated-items.md#methods
[module]: ../items/modules.md
[name resolution]: name-resolution.md
[namespace]: namespaces.md
[path]: ../paths.md
[pattern]: ../patterns.md
[placeholder lifetime]: ../lifetime-elision.md
[preludes]: preludes.md
[Standard library prelude]: preludes.md#standard-library-prelude
[statement]: ../statements.md
[Static items]: ../items/static-items.md
[static]: ../items/static-items.md
[struct]: ../items/structs.md
[structs]: ../items/structs.md
[Tool prelude]: preludes.md#tool-prelude
[trait]: ../items/traits.md
[union]: ../items/unions.md
