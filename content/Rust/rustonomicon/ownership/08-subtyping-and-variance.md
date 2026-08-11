+++
title = "3.8 子类型与型变"
date = 2026-08-06T17:08:00+08:00
weight = 18
type = "docs"
description = "子类型关系与型变"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [The Rustonomicon](https://doc.rust-lang.org/nomicon/)

# 子类型与型变


> 原文链接: [https://doc.rust-lang.org/nomicon/subtyping.html](https://doc.rust-lang.org/nomicon/subtyping.html)


　　Rust 用生命周期追踪借用与所有权之间的关系。
　　然而，生命周期的朴素实现要么过于严格，要么允许未定义行为。

　　为了在允许灵活使用生命周期的同时防止误用，Rust 采用**子类型**（subtyping）和**型变**（variance）。

　　先看一个例子。

```rust
// 注意：debug 期望两个具有*相同*生命周期的参数
fn debug<'a>(a: &'a str, b: &'a str) {
    println!("a = {a:?} b = {b:?}");
}

fn main() {
    let hello: &'static str = "hello";
    {
        let world = String::from("world");
        let world = &world; // 'world 的生命周期短于 'static
        debug(hello, world);
    }
}
```

　　在保守的生命周期实现中，由于 `hello` 和 `world` 生命周期不同，我们可能看到如下错误：

```text
error[E0308]: mismatched types
 --> src/main.rs:10:16
   |
10 |         debug(hello, world);
   |                      ^
   |                      |
   |                      expected `&'static str`, found struct `&'world str`
```

　　这相当不幸。此例中，我们希望接受任何*至少与* `'world` 一样长*的类型。
　　让我们尝试在生命周期上使用子类型。

## 子类型

　　子类型是指一种类型可以在另一种类型的位置上使用。

　　设 `Sub` 是 `Super` 的子类型（本章用记号 `Sub <: Super`）。

　　这意味着 `Super` 定义的*全部*要求都被 `Sub` 满足。`Sub` 还可以有额外要求。

　　要在生命周期上使用子类型，需要先定义生命周期的要求：

> `'a` 定义一段代码区域。

　　有了生命周期的要求集合，就可以定义它们之间的关系：

> `'long <: 'short` 当且仅当 `'long` 定义的代码区域**完全包含** `'short`。

　　`'long` 可以比 `'short` 定义更大的区域，这仍符合上述定义。

> 如本章其余部分所示，子类型远比这复杂微妙，
> 但这一简单规则足以提供 99% 的直觉。
> 除非你写 unsafe 代码，编译器会自动处理所有边角情况。

> 但这是 Rustonomicon。我们在写 unsafe 代码，
> 因此需要理解这些机制的真实运作方式，以及我们如何搞砸它们。

　　回到上面的例子，可以说 `'static <: 'world`。
　　暂且接受生命周期子类型可以通过引用传递
　　（详见[型变](#variance)），
　　_例如_ `&'static str` 是 `&'world str` 的子类型，于是可以把 `&'static str`「降级」为 `&'world str`。
　　这样上面的例子就能编译：

```rust
fn debug<'a>(a: &'a str, b: &'a str) {
    println!("a = {a:?} b = {b:?}");
}

fn main() {
    let hello: &'static str = "hello";
    {
        let world = String::from("world");
        let world = &world; // 'world 的生命周期短于 'static
        debug(hello, world); // hello 静默地从 `&'static str` 降级为 `&'world str`
    }
}
```

## 型变

　　上面我们略过了 `'static <: 'b` 意味着 `&'static T <: &'b T` 这一事实。这用到称为*型变*的性质。
　　不过并不总是这么简单。为理解这一点，把例子再扩展一点：

```rust,compile_fail,E0597
fn assign<T>(input: &mut T, val: T) {
    *input = val;
}

fn main() {
    let mut hello: &'static str = "hello";
    {
        let world = String::from("world");
        assign(&mut hello, &world);
    }
    println!("{hello}"); // use after free 😿
}
```

　　在 `assign` 中，我们让 `hello` 引用指向 `world`。
　　但 `world` 在后续 `println!` 使用 `hello` 之前就出了作用域！

　　这是典型的 use-after-free 错误！

　　第一反应可能是怪 `assign` 的实现，但其实这里没有问题。
　　把 `T` 赋给 `T` 并不令人意外。

　　问题在于，一旦 `&'static str` 藏在 `&mut` 引用后面，就不能再假设它能降级为 `&'world str` 来满足 `T`。
　　这意味着 `&mut &'static str` **不能**是 `&mut &'world str` 的*子类型*，
　　即便 `'static` 是 `'world` 的子类型。

　　型变是 Rust 用来定义泛型参数如何通过子类型关系传递的概念。

> 注：为方便起见，我们定义泛型类型 `F<T>`，
> 以便轻松讨论 `T`。希望上下文足够清晰。

　　类型 `F` 的*型变*是指其输入的子类型关系如何影响其输出的子类型关系。Rust 中有三种型变。给定 `Sub` 和 `Super`，且 `Sub` 是 `Super` 的子类型：

* `F` 是**协变**（covariant）的，若 `F<Sub>` 是 `F<Super>` 的子类型（子类型性质传递）
* `F` 是**逆变**（contravariant）的，若 `F<Super>` 是 `F<Sub>` 的子类型（子类型性质「反转」）
* 否则 `F` 是**不变**（invariant）的（不存在子类型关系）

　　回顾上面的例子，
　　若 `'a <: 'b`，则可以把 `&'a T` 当作 `&'b T` 的子类型，
　　因此可以说 `&'a T` 对 `'a` 是*协变*的。

　　另外，不能把 `&mut &'a T` 当作 `&mut &'b T` 的子类型，
　　因此可以说 `&mut T` 对 `T` 是*不变*的。

　　下面是一些其他泛型类型及其型变的表格：

|                 |     'a    |         T         |     U     |
|-----------------|:---------:|:-----------------:|:---------:|
| `&'a T `        | covariant | covariant         |           |
| `&'a mut T`     | covariant | invariant         |           |
| `Box<T>`        |           | covariant         |           |
| `Vec<T>`        |           | covariant         |           |
| `UnsafeCell<T>` |           | invariant         |           |
| `Cell<T>`       |           | invariant         |           |
| `fn(T) -> U`    |           | **contra**variant | covariant |
| `*const T`      |           | covariant         |           |
| `*mut T`        |           | invariant         |           |

　　其中一些可相对其他类型简单解释：

* `Vec<T>` 及所有其他 owning 指针和集合与 `Box<T>` 逻辑相同
* `Cell<T>` 及所有其他内部可变性类型与 `UnsafeCell<T>` 逻辑相同
* `UnsafeCell<T>` 的内部可变性使其与 `&mut T` 具有相同型变性质
* `*const T` 遵循 `&T` 的逻辑
* `*mut T` 遵循 `&mut T`（或 `UnsafeCell<T>`）的逻辑

　　更多类型见 reference 的 [「Variance」章节][variance-table]。

[variance-table]: ../reference/subtyping.html#variance

> 注：语言中*唯一*的逆变来源是函数参数，因此实践中很少遇到。
> 触发逆变需要高阶编程：函数指针接受具有特定生命周期的引用（而非通常的「任意生命周期」，
> 后者涉及高阶生命周期，与子类型独立运作）。

　　有了更形式化的型变理解，我们再详细看几个例子。

```rust,compile_fail,E0597
fn assign<T>(input: &mut T, val: T) {
    *input = val;
}

fn main() {
    let mut hello: &'static str = "hello";
    {
        let world = String::from("world");
        assign(&mut hello, &world);
    }
    println!("{hello}");
}
```

　　运行会得到什么？

```text
error[E0597]: `world` does not live long enough
  --> src/main.rs:9:28
   |
6  |     let mut hello: &'static str = "hello";
   |                    ------------ type annotation requires that `world` is borrowed for `'static`
...
9  |         assign(&mut hello, &world);
   |                            ^^^^^^ borrowed value does not live long enough
10 |     }
   |     - `world` dropped here while still borrowed
```

　　很好，编译不过！下面详细分解发生了什么。

　　先看 `assign` 函数：

```rust
fn assign<T>(input: &mut T, val: T) {
    *input = val;
}
```

　　它只是取可变引用和值，用后者覆盖前者。
　　此函数重要的是它建立了类型相等约束：签名明确要求被引用对象与值必须是*完全相同*的类型。

　　调用方传入 `&mut &'static str` 和 `&'world str`。

　　由于 `&mut T` 对 `T` 不变，编译器结论是无法对第一个参数应用任何子类型，因此 `T` 必须是 `'static str`。

　　这与 `&T` 的情况相反：

```rust
fn debug<T: std::fmt::Debug>(a: T, b: T) {
    println!("a = {a:?} b = {b:?}");
}
```

　　这里 `a` 和 `b` 同样必须有相同类型 `T`。
　　但由于 `&'a T` 对 `'a` *是*协变的，允许进行子类型转换。
　　编译器判定 `&'static str` 可变为 `&'b str`，当且仅当
　　`&'static str` 是 `&'b str` 的子类型，即 `'static <: 'b` 成立。
　　这成立，编译器便继续编译。

　　事实证明，Box（以及 Vec、HashMap 等）协变的理由与生命周期协变类似：一旦把它们放进可变引用等位置，就继承不变性，从而阻止做坏事。

　　不过 Box 更容易聚焦我们部分略过的引用的按值方面。

　　与许多语言允许值随时自由别名不同，Rust 有严格规则：若允许你修改（mutate）或 move 某值，则保证你是唯一访问者。

　　考虑以下代码：

```rust,ignore
let hello: Box<&'static str> = Box::new("hello");

let mut world: Box<&'b str>;
world = hello;
```

　　我们「忘记」`hello` 曾存活 `'static` 完全没问题，
　　因为一旦把 `hello` move 到只知道它存活 `'b` 的变量，
　　**我们就销毁了宇宙中唯一记得它活得更久的东西**！

　　还剩一点：函数指针。

　　要理解 `fn(T) -> U` 为何对 `U` 协变，考虑如下签名：

```rust,ignore
fn get_str() -> &'a str;
```

　　此函数声称产生由某生命周期 `'a` 约束的 `str`。因此完全可以用如下签名替代：

```rust,ignore
fn get_static() -> &'static str;
```

　　调用时，调用方只期望得到至少存活 `'a` 的 `&str`，
　　实际活得更久并无妨。

　　然而同样逻辑不适用于*参数*。尝试满足：

```rust,ignore
fn store_ref(&'a str);
```

　　用：

```rust,ignore
fn store_static(&'static str);
```

　　第一个函数可接受任何至少存活 `'a` 的字符串引用，
　　第二个却不能接受存活短于 `'static` 的引用，会产生冲突。
　　协变在这里行不通。但若反过来，*确实*可行！若需要能处理 `&'static str` 的函数，能处理*任意*引用生命周期的函数当然也没问题。

　　实践中看：

```rust,compile_fail
# use std::cell::RefCell;
thread_local! {
    pub static StaticVecs: RefCell<Vec<&'static str>> = RefCell::new(Vec::new());
}

/// 将给定输入保存到线程局部的 `Vec<&'static str>` 中
fn store(input: &'static str) {
    StaticVecs.with_borrow_mut(|v| v.push(input));
}

/// 用其输入调用函数（必须具有相同生命周期！）
fn demo<'a>(input: &'a str, f: fn(&'a str)) {
    f(input);
}

fn main() {
    demo("hello", store); // "hello" 是 'static，可正常调用 `store`

    {
        let smuggle = String::from("smuggle");

        // `&smuggle` 不是 static。若用 `&smuggle` 调用 `store`，
        // 会把无效生命周期 push 进 `StaticVecs`。
        // 因此 `fn(&'static str)` 不能是 `fn(&'a str)` 的子类型
        demo(&smuggle, store);
    }

    // use after free 😿
    StaticVecs.with_borrow(|v| println!("{v:?}"));
}
```

　　这就是为什么函数类型与语言中其他一切不同，对其参数是**逆**变的。

　　以上对标准库类型的讨论已足够，但*你*定义的类型如何确定型变？非正式地说，结构体继承其字段的型变。若结构体 `MyType`
　　的泛型参数 `A` 用在字段 `a` 中，则 `MyType` 对 `A` 的型变与 `a` 对 `A` 的型变完全一致。

　　若 `A` 用在多个字段中：

* 若 `A` 的所有用法都是协变的，则 `MyType` 对 `A` 协变
* 若 `A` 的所有用法都是逆变的，则 `MyType` 对 `A` 逆变
* 否则 `MyType` 对 `A` 不变

```rust
use std::cell::Cell;

struct MyType<'a, 'b, A: 'a, B: 'b, C, D, E, F, G, H, In, Out, Mixed> {
    a: &'a A,     // 对 'a 和 A 协变
    b: &'b mut B, // 对 'b 协变，对 B 不变

    c: *const C,  // 对 C 协变
    d: *mut D,    // 对 D 不变

    e: E,         // 对 E 协变
    f: Vec<F>,    // 对 F 协变
    g: Cell<G>,   // 对 G 不变

    h1: H,        // 本可对 H 协变，但……
    h2: Cell<H>,  // 对 H 不变，因为不变性在冲突中总是胜出

    i: fn(In) -> Out,       // 对 In 逆变，对 Out 协变

    k1: fn(Mixed) -> usize, // 本可对 Mixed 逆变，但……
    k2: Mixed,              // 对 Mixed 不变，因为不变性在冲突中总是胜出
}
```
