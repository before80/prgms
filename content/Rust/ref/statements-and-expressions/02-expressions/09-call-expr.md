+++
title = "09-调用表达式"
date = 2026-08-18T08:45:00+08:00
weight = 52
type = "docs"
description = "调用表达式 — The Rust Reference"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Reference](https://doc.rust-lang.org/reference/)

> 原文链接: [https://doc.rust-lang.org/reference/expressions/call-expr.html](https://doc.rust-lang.org/reference/expressions/call-expr.html)

r[expr.call]
# 调用表达式

r[expr.call.syntax]
```grammar,expressions
CallExpression -> Expression `(` CallParams? `)`

CallParams -> Expression ( `,` Expression )* `,`?
```

r[expr.call.intro]
*调用表达式*用于调用函数。调用表达式的语法是一个表达式（称为*函数操作数*），后跟一个由圆括号括起、以逗号分隔的表达式列表（称为*实参操作数*）。

r[expr.call.convergence]
若函数最终返回，则该表达式完成。

r[expr.call.trait]
对于[非函数类型][non-function types]，表达式 `f(...)` 会根据函数操作数使用下列某个 trait 上的方法：

- [`Fn`] 或 [`AsyncFn`] —— 共享引用。
- [`FnMut`] 或 [`AsyncFnMut`] —— 可变引用。
- [`FnOnce`] 或 [`AsyncFnOnce`] —— 值。

r[expr.call.autoref-deref]
必要时会自动进行借用。函数操作数也会按需[自动解引用][automatically dereferenced]。

调用表达式的一些示例：

```rust
## fn add(x: i32, y: i32) -> i32 { 0 }
let three: i32 = add(1i32, 2i32);
let name: &'static str = (|| "Rust")();
```

r[expr.call.desugar]
## 消除函数调用歧义

r[expr.call.desugar.fully-qualified]
所有函数调用都是更显式的[完全限定语法][fully-qualified syntax]的语法糖。

r[expr.call.desugar.ambiguity]
根据作用域中的项所造成的歧义，函数调用可能需要写成完全限定形式。

> **注意**
> 过去在文档、issue、RFC 及其它社区文字中曾使用过 “Unambiguous Function Call Syntax”、“Universal Function Call Syntax” 或 “UFCS” 等术语。不过这些术语描述力不足，还可能把问题本身搞混。此处提及它们是为了便于检索。

r[expr.call.desugar.limits]
经常会出现若干导致方法或关联函数调用的接收者或指称对象产生歧义的情况。这些情况可能包括：

* 多个在作用域内的 trait 为相同类型定义了同名方法
* 不希望发生自动 `deref`；例如，需要区分智能指针自身上的方法与指针所指对象上的方法
* 不接受参数的方法，如 [`default()`]，以及返回类型属性的函数，如 [`size_of()`]

r[expr.call.desugar.explicit-path]
为消除歧义，程序员可以使用更具体的路径、类型或 trait 来指称想要的方法或函数。

例如，

```rust
trait Pretty {
    fn print(&self);
}

trait Ugly {
    fn print(&self);
}

struct Foo;
impl Pretty for Foo {
    fn print(&self) {}
}

struct Bar;
impl Pretty for Bar {
    fn print(&self) {}
}
impl Ugly for Bar {
    fn print(&self) {}
}

fn main() {
    let f = Foo;
    let b = Bar;

    // 可以这样写，因为对 `Foo` 只有一个名为 `print` 的项
    f.print();
    // 更显式；对 `Foo` 而言并非必需
    Foo::print(&f);
    // 如果你并不追求简洁
    <Foo as Pretty>::print(&f);

    // b.print(); // 错误：找到多个 `print`
    // Bar::print(&b); // 仍然是错误：找到多个 `print`

    // 因为作用域中有多个定义 `print` 的项，所以必须这样写
    <Bar as Pretty>::print(&b);
}
```

更多细节与动机见 [RFC 132]。

[RFC 132]: https://github.com/rust-lang/rfcs/blob/master/text/0132-ufcs.md
[`default()`]: std::default::Default::default
[`size_of()`]: std::mem::size_of
[automatically dereferenced]: field-expr.md#automatic-dereferencing
[fully-qualified syntax]: ../paths.md#qualified-paths
[non-function types]: ../types/function-item.md
