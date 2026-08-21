+++
title = "04-用自定义 trait 避免复杂类型约束"
date = 2026-08-18T22:10:00+08:00
weight = 38
type = "docs"
description = "用自定义 trait 避免复杂类型约束 — Rust Design Patterns"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Rust Design Patterns](https://rust-unofficial.github.io/patterns/)

> 原文链接: [https://rust-unofficial.github.io/patterns/patterns/structural/trait-for-bounds.html](https://rust-unofficial.github.io/patterns/patterns/structural/trait-for-bounds.html)

# 用自定义 trait 避免复杂类型约束

## 描述 {#description}

Trait 约束有时会变得相当难用，尤其是当涉及某个 `Fn` trait[^fn-traits]，并对输出类型有特定要求时。在这种情况下，引入一个新 trait 可能有助于减少冗长、消除一些类型参数，从而提高表达力。这样的 trait 可以伴随一个对所有满足原始约束的类型的泛型 `impl`。

## 示例 {#example}

让我们想象某种监控或信息收集系统。系统从各种来源检索不同类型的值。它可能从中推导出某种表示问题的状态。例如，空闲内存总量应高于某个阈值，且 id 为 `0` 的用户应始终名为 “root”。

出于管理原因，我们可能希望在顶层做类型擦除。然而，我们也需要为特定类型的数据源提供具体的（用户可配置的）评估（例如数值类型的阈值与范围）。由于这些值的来源多种多样，我们可能选择以闭包形式提供数据源，在调用时返回值。因为我们很可能从操作系统获取这些值，所以很可能面对可能失败的操作。

于是，我们可能最终采用以下类型与 trait 来处理特定值：

```rust
use std::fmt::Display;

struct Value<G: FnMut() -> Result<T, Error>, S: Fn(&T) -> Status, T: Display> {
    value: Option<T>,
    getter: G,
    status: S,
}

impl<G: FnMut() -> Result<T, Error>, S: Fn(&T) -> Status, T: Display> Value<G, S, T> {
    pub fn update(&mut self) -> Result<(), Error> {
        (self.getter)().map(|v| self.value = Some(v))
    }

    pub fn value(&self) -> Option<&T> {
        self.value.as_ref()
    }

    pub fn status(&self) -> Option<Status> {
        self.value().map(&self.status)
    }
}

// ...

enum Status {
    // ...
}

struct Error {
    // ...
}
```

有了这些类型，我们至少会在几处重复 `G` 的 trait 约束。可读性受损，部分原因是 getter 返回 `Result`。为“getter”引入约束，可以带来更具表达力的约束，并消除其中一个类型参数：

```rust
# use std::fmt::Display;
trait Getter {
    type Output: Display;

    fn get_value(&mut self) -> Result<Self::Output, Error>;
}

impl<F: FnMut() -> Result<T, Error>, T: Display> Getter for F {
    type Output = T;

    fn get_value(&mut self) -> Result<Self::Output, Error> {
        self()
    }
}

struct Value<G: Getter, S: Fn(&G::Output) -> Status> {
    value: Option<G::Output>,
    getter: G,
    status: S,
}

// ...
# enum Status {}
# struct Error;
```

## 优点 {#advantages}

引入新 trait 有助于简化类型约束，尤其是通过消除类型参数。给新 trait 起一个好名字也会使约束更具表达力。作为抽象，新 trait 本身也带来机会，包括：

- 实现该新 trait 的额外、特化类型（例如表示某种恒等），以及其他有用的 trait，如 `Default`，以及
- 额外方法，只要它们能为所有相关类型实现。

## 缺点 {#disadvantages}

引入像 trait 这样的新项意味着我们需要为它找到合适的名称与位置。这也意味着使用原有功能的用户需要多调查一项[^read-docs]。取决于呈现方式，可能不会立刻明显：在上面的示例中，一个简单的闭包就可以用作 `Getter`。

[^fn-traits]: 即 `Fn`、`FnOnce` 和 `FnMut`

[^read-docs]: 意味着他们可能需要阅读更多文档
