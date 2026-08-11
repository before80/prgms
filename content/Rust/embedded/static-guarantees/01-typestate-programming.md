+++
title = "01-类型状态编程"
date = 2026-08-01T10:38:00+08:00
weight = 69
type = "docs"
description = "类型状态编程（Typestate Programming）"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Embedded Rust Book](https://doc.rust-lang.org/stable/embedded-book/)

# 类型状态编程 {#typestate-programming}


> 原文链接: [https://doc.rust-lang.org/stable/embedded-book/static-guarantees/typestate-programming.html](https://doc.rust-lang.org/stable/embedded-book/static-guarantees/typestate-programming.html)


[类型状态（typestate）][typestates] 的概念是把关于对象当前状态的信息编码进该对象的类型中。虽然这听起来有点晦涩，但如果你在 Rust 中用过 [Builder Pattern]，你就已经开始使用类型状态编程了！

[typestates]: https://en.wikipedia.org/wiki/Typestate_analysis
[Builder Pattern]: https://doc.rust-lang.org/1.0.0/style/ownership/builders.html

```rust
pub mod foo_module {
    #[derive(Debug)]
    pub struct Foo {
        inner: u32,
    }

    pub struct FooBuilder {
        a: u32,
        b: u32,
    }

    impl FooBuilder {
        pub fn new(starter: u32) -> Self {
            Self {
                a: starter,
                b: starter,
            }
        }

        pub fn double_a(self) -> Self {
            Self {
                a: self.a * 2,
                b: self.b,
            }
        }

        pub fn into_foo(self) -> Foo {
            Foo {
                inner: self.a + self.b,
            }
        }
    }
}

fn main() {
    let x = foo_module::FooBuilder::new(10)
        .double_a()
        .into_foo();

    println!("{:#?}", x);
}
```

在这个例子中，没有直接创建 `Foo` 对象的方式。我们必须创建 `FooBuilder`，并正确初始化它，然后才能得到想要的 `Foo` 对象。

这个最小例子编码了两种状态：

* `FooBuilder`，表示「未配置」或「配置进行中」状态
* `Foo`，表示「已配置」或「就绪可用」状态

## 强类型 {#strong-types}

因为 Rust 有[强类型系统（Strong Type System）][Strong Type System]，没有简单办法凭空变出 `Foo` 的实例，也不能在不调用 `into_foo()` 方法的情况下把 `FooBuilder` 变成 `Foo`。此外，调用 `into_foo()` 会消费原来的 `FooBuilder` 结构体，意味着若不创建新实例就无法复用它。

[Strong Type System]: https://en.wikipedia.org/wiki/Strong_and_weak_typing

这让我们能用类型表示系统状态，并把状态转换所需的动作包含进把一种类型换成另一种类型的方法中。通过创建 `FooBuilder`，并把它换成 `Foo` 对象，我们就走完了一个基本状态机的各个步骤。
