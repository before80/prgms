+++
title = "03-Deref 多态"
date = 2026-08-18T22:10:00+08:00
weight = 45
type = "docs"
description = "Deref 多态 — Rust Design Patterns"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Rust Design Patterns](https://rust-unofficial.github.io/patterns/)

> 原文链接: [https://rust-unofficial.github.io/patterns/anti_patterns/deref.html](https://rust-unofficial.github.io/patterns/anti_patterns/deref.html)

# Deref 多态

## 描述 {#description}

滥用 `Deref` trait 来模拟结构体之间的继承，从而复用方法。

## 示例 {#example}

有时我们想模拟 Java 等 OO 语言中的如下常见模式：

```java
class Foo {
    void m() { ... }
}

class Bar extends Foo {}

public static void main(String[] args) {
    Bar b = new Bar();
    b.m();
}
```

我们可以用 Deref 多态这一反模式来做到：

```rust
use std::ops::Deref;

struct Foo {}

impl Foo {
    fn m(&self) {
        //..
    }
}

struct Bar {
    f: Foo,
}

impl Deref for Bar {
    type Target = Foo;
    fn deref(&self) -> &Foo {
        &self.f
    }
}

fn main() {
    let b = Bar { f: Foo {} };
    b.m();
}
```

Rust 没有结构体继承。我们改用组合，在 `Bar` 中包含一个 `Foo` 实例（由于该字段是值，它以内联方式存储，因此若有字段，其内存布局可能与 Java 版本相同（若想确定，应使用 `#[repr(C)]`））。

为了让方法调用生效，我们为 `Bar` 实现以 `Foo` 为目标的 `Deref`（返回嵌入的 `Foo` 字段）。这意味着当我们解引用一个 `Bar`（例如使用 `*`）时，会得到一个 `Foo`。这相当怪异。解引用通常是从对 `T` 的引用得到 `T`，这里却是两个无关的类型。然而，由于点运算符会做隐式解引用，方法调用会同时在 `Foo` 和 `Bar` 上查找方法。

## 优点 {#advantages}

能少写一点样板代码，例如：

```rust,ignore
impl Bar {
    fn m(&self) {
        self.f.m()
    }
}
```

## 缺点 {#disadvantages}

最重要的是，这是一种令人意外的惯用法——将来读到这段代码的程序员不会预期会发生这种事。因为我们在滥用 `Deref` trait，而不是按设计意图（以及文档等）使用它。这也因为这里的机制完全是隐式的。

这种模式不会像 Java 或 C++ 的继承那样在 `Foo` 与 `Bar` 之间引入子类型关系。此外，`Foo` 实现的 trait 不会自动为 `Bar` 实现，因此该模式与边界检查以及泛型编程的配合很差。

使用这种模式时，关于 `self` 的语义与多数 OO 语言略有不同。通常 `self` 仍是对子类的引用；而用这种模式时，它会是定义该方法的那个「类」。

最后，这种模式只支持单继承，且没有接口、基于类的可见性或其他与继承相关的概念。因此，对习惯 Java 继承等的程序员来说，体验会微妙地令人意外。

## 讨论 {#discussion}

没有一种放之四海而皆准的替代方案。视具体情形而定，可能更适合用 trait 重新实现，或写出门面方法手动分派到 `Foo`。我们确实打算为 Rust 加入类似于此的继承机制，但很可能还要一段时间才能进入稳定版 Rust。更多细节见这些[博文](http://aturon.github.io/blog/2015/09/18/reuse/)
[文章](http://smallcultfollowing.com/babysteps/blog/2015/10/08/virtual-structs-part-4-extended-enums-and-thin-traits/)
以及此 [RFC issue](https://github.com/rust-lang/rfcs/issues/349)。

`Deref` trait 是为自定义指针类型的实现而设计的。其意图是把指向 `T` 的指针变成 `T`，而不是在不同的类型之间转换。可惜这一点并未（或许也无法）由 trait 定义强制约束。

Rust 试图在显式与隐式机制之间谨慎平衡，并倾向于类型之间的显式转换。点运算符中的自动解引用是一个人体工学强烈偏向隐式机制的例子，但其意图是将其限制在间接层级上，而不是任意类型之间的转换。

## 参见 {#see-also}

- [集合是智能指针惯用法](../idioms/05-collections-are-smart-pointers/)。
- 可减少样板代码的委托 crate，例如
  [delegate](https://crates.io/crates/delegate) 或
  [ambassador](https://crates.io/crates/ambassador)
- [`Deref` trait 文档](https://doc.rust-lang.org/std/ops/trait.Deref.html)。
