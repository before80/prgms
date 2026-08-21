+++
title = "07-`mem::{take(_), replace(_)}`"
date = 2026-08-18T22:10:00+08:00
weight = 11
type = "docs"
description = "`mem::{take(_), replace(_)}` — Rust Design Patterns"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Rust Design Patterns](https://rust-unofficial.github.io/patterns/)

> 原文链接: [https://rust-unofficial.github.io/patterns/idioms/mem-replace.html](https://rust-unofficial.github.io/patterns/idioms/mem-replace.html)

# `mem::{take(_), replace(_)}`

## 描述 {#description}

假设我们有一个 `&mut MyEnum`，它至少有两个变体：
`A { name: String, x: u8 }` 和 `B { name: String }`。现在我们想在 `x` 为零时把
`MyEnum::A` 改成 `B`，同时保持 `MyEnum::B` 不变。

我们可以在不克隆 `name` 的情况下做到这一点。

## 示例 {#example}

```rust
use std::mem;

enum MyEnum {
    A { name: String, x: u8 },
    B { name: String },
}

fn a_to_b(e: &mut MyEnum) {
    if let MyEnum::A { name, x: 0 } = e {
        // 这会取出我们的 `name`，并放入一个空 String 作为替换
        // （注意空字符串不会分配）。
        // 然后构造新的枚举变体（它将被
        // 赋给 `*e`）。
        *e = MyEnum::B {
            name: mem::take(name),
        }
    }
}
```

这对更多变体同样有效：

```rust
use std::mem;

enum MultiVariateEnum {
    A { name: String },
    B { name: String },
    C,
    D,
}

fn swizzle(e: &mut MultiVariateEnum) {
    use MultiVariateEnum::*;
    *e = match e {
        // 所有权规则不允许按值取出 `name`，但我们不能
        // 从可变引用中取出值，除非我们替换它：
        A { name } => B {
            name: mem::take(name),
        },
        B { name } => A {
            name: mem::take(name),
        },
        C => D,
        D => C,
    }
}
```

## 动机 {#motivation}

处理枚举时，我们可能想就地改变枚举值，也许改成另一个变体。这通常分两个阶段进行，
以使借用检查器满意。第一阶段，我们观察现有值并查看其各部分，以决定接下来做什么。
第二阶段，我们可能有条件地改变该值（如上面的例子）。

借用检查器不允许我们从枚举中取出 `name`（因为*必须有东西*待在那里。）
我们当然可以 `.clone()` name，并把克隆放入 `MyEnum::B`，但那会成为
[为通过借用检查器而 Clone](../anti-patterns/01-clone-to-satisfy-the-borrow-checker/)
反模式的实例。无论如何，我们只需通过可变借用改变 `e`，就能避免额外分配。

`mem::take` 让我们换出该值，用其默认值替换，并返回原先的值。对 `String` 而言，
默认值是空 `String`，无需分配。结果是，我们得到作为*所有权值*的原始 `name`。
然后我们可以把它包进另一个枚举。

**注意：** `mem::replace` 非常相似，但允许我们指定用什么来替换该值。
与我们的 `mem::take` 那一行等价的写法是
`mem::replace(name, String::new())`。

不过请注意，如果我们使用的是 `Option` 并想用 `None` 替换其值，
`Option` 的 `take()` 方法提供了更短、更符合惯用法的替代方案。

## 优点 {#advantages}

看，完全不用分配！做这件事时，你可能还会觉得自己像印第安纳·琼斯。

## 缺点 {#disadvantages}

这会显得有些啰嗦。反复弄错会让你讨厌借用检查器。编译器可能无法优化掉两次存储，
从而导致性能不如在不安全语言中的做法。

此外，被取出的类型需要实现
[`Default` trait](04-the-default-trait/)。不过，如果你正在处理的类型
没有实现它，可以改用 `mem::replace`。

## 讨论 {#discussion}

这种模式只在 Rust 中有意义。在带 GC 的语言中，你默认会取得该值的引用（GC 会跟踪引用），
而在 C 等其他底层语言中，你只需给指针起个别名，稍后再把事情理顺。

然而在 Rust 中，我们得多做一点工作。所有权值只能有一个所有者，因此要把它取出来，
我们就需要放回某种东西——就像印第安纳·琼斯用一袋沙子换走神器那样。

## 参见 {#see-also}

这在特定情形下消除了
[为通过借用检查器而 Clone](../anti-patterns/01-clone-to-satisfy-the-borrow-checker/)
反模式。
