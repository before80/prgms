+++
title = "01-构建器"
date = 2026-08-18T22:10:00+08:00
weight = 32
type = "docs"
description = "构建器 — Rust Design Patterns"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Rust Design Patterns](https://rust-unofficial.github.io/patterns/)

> 原文链接: [https://rust-unofficial.github.io/patterns/patterns/creational/builder.html](https://rust-unofficial.github.io/patterns/patterns/creational/builder.html)

# 构建器

## 描述 {#description}

通过调用构建器辅助对象来构造对象。

## 示例 {#example}

```rust
#[derive(Debug, PartialEq)]
pub struct Foo {
    // 大量复杂字段。
    bar: String,
}

impl Foo {
    // 此方法帮助用户发现构建器
    pub fn builder() -> FooBuilder {
        FooBuilder::default()
    }
}

#[derive(Default)]
pub struct FooBuilder {
    // 可能有大量可选字段。
    bar: String,
}

impl FooBuilder {
    pub fn new(/* ... */) -> FooBuilder {
        // 设置 Foo 最少必需的字段。
        FooBuilder {
            bar: String::from("X"),
        }
    }

    pub fn name(mut self, bar: String) -> FooBuilder {
        // 在构建器自身上设置名称，并按值返回构建器。
        self.bar = bar;
        self
    }

    // 若此处不必消费 Builder，那会是一个优点。
    // 这意味着我们可以把 FooBuilder 当作模板，用来构造许多 Foo。
    pub fn build(self) -> Foo {
        // 从 FooBuilder 创建 Foo，将 FooBuilder 中的所有设置应用到 Foo。
        Foo { bar: self.bar }
    }
}

#[test]
fn builder_test() {
    let foo = Foo {
        bar: String::from("Y"),
    };
    let foo_from_builder: Foo = FooBuilder::new().name(String::from("Y")).build();
    assert_eq!(foo, foo_from_builder);
}
```

## 动机 {#motivation}

当你本来需要许多构造函数，或构造过程有副作用时，此模式很有用。

## 优点 {#advantages}

将构建方法与其他方法分离。

防止构造函数激增。

既可用于一行式初始化，也可用于更复杂的构造。

当你向目标结构体添加新字段时，可以更新构建器，同时保持客户端代码向后兼容。

## 缺点 {#disadvantages}

比直接创建结构体对象或使用简单的构造函数更复杂。

## 讨论 {#discussion}

此模式在 Rust 中出现得比许多其他语言更频繁（即便对象较简单也是如此），因为 Rust 没有函数重载和函数参数默认值。由于同名方法只能有一个，多个构造函数在 Rust 中不如在 C++、Java 等语言中那么优雅。

此模式常用于构建器对象本身就有独立价值、而不只是构建工具的场景。例如，参见
[`std::process::Command`](https://doc.rust-lang.org/std/process/struct.Command.html)
是
[`Child`](https://doc.rust-lang.org/std/process/struct.Child.html)（一个进程）的构建器。
在这些情况下，不会使用 `T` 与 `TBuilder` 的命名模式。

示例中按值接收并返回构建器。更符合人体工程学（也往往更高效）的做法是以可变引用接收并返回构建器。借用检查器会让这种方式自然成立。这种方法的优点是可以写出如下代码：

```rust,ignore
let mut fb = FooBuilder::new();
fb.a();
fb.b();
let f = fb.build();
```

同时也支持 `FooBuilder::new().a().b().build()` 风格。

## 参见 {#see-also}

- [风格指南中的描述](https://web.archive.org/web/20210104103100/https://doc.rust-lang.org/1.12.0/style/ownership/builders.html)
- [derive_builder](https://crates.io/crates/derive_builder)，一个自动实现此模式从而避免样板代码的 crate。
- [构造器](../../idioms/03-constructor/)模式，适用于构造更简单的情况。
- [构建器模式（Wikipedia）](https://en.wikipedia.org/wiki/Builder_pattern)
- [复杂值的构造](https://web.archive.org/web/20210104103000/https://rust-lang.github.io/api-guidelines/type-safety.html#c-builder)
