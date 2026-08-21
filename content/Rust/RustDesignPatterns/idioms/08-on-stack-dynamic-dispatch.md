+++
title = "08-栈上动态分发"
date = 2026-08-18T22:10:00+08:00
weight = 12
type = "docs"
description = "栈上动态分发 — Rust Design Patterns"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Rust Design Patterns](https://rust-unofficial.github.io/patterns/)

> 原文链接: [https://rust-unofficial.github.io/patterns/idioms/on-stack-dyn-dispatch.html](https://rust-unofficial.github.io/patterns/idioms/on-stack-dyn-dispatch.html)

# 栈上动态分发

## 描述 {#description}

我们可以对多个值进行动态分发，但为此需要声明多个变量，以绑定不同类型的对象。
为了按需延长生命周期，我们可以使用延迟条件初始化，如下所示：

## 示例 {#example}

```rust
use std::io;
use std::fs;

# fn main() -> Result<(), Box<dyn std::error::Error>> {
# let arg = "-";

// 我们需要标明类型才能得到动态分发。
let readable: &mut dyn io::Read = if arg == "-" {
    &mut io::stdin()
} else {
    &mut fs::File::open(arg)?
};

// 在此处从 `readable` 读取。

# Ok(())
# }
```

## 动机 {#motivation}

Rust 默认会将代码单态化。这意味着会为所用的每种类型生成一份代码副本，并分别优化。
这固然能让热路径上的代码非常快，但也会在性能并不关键的地方膨胀代码，从而耗费编译时间和缓存。

幸运的是，Rust 允许我们使用动态分发，但我们必须显式请求它。

## 优点 {#advantages}

我们不需要在堆上分配任何东西。也不需要初始化稍后不会用到的东西，
更不需要把后续整段代码单态化，以便同时适用于 `File` 或 `Stdin`。

## 缺点 {#disadvantages}

在 Rust 1.79.0 之前，这段代码需要两个带延迟初始化的 `let` 绑定，
比基于 `Box` 的版本有更多活动部件：

```rust,ignore
// 我们仍需标明类型才能得到动态分发。
let readable: Box<dyn io::Read> = if arg == "-" {
    Box::new(io::stdin())
} else {
    Box::new(fs::File::open(arg)?)
};
// 在此处从 `readable` 读取。
```

幸运的是，这一缺点现已不复存在。太好了！

## 讨论 {#discussion}

自 Rust 1.79.0 起，编译器会在函数作用域内尽可能延长 `&` 或 `&mut` 中临时值的生命周期。

这意味着我们可以在这里直接使用 `&mut` 值，而不必担心把内容放到某个 `let` 绑定中
（那是延迟初始化所需要的，也是该变更之前所用的解决方案）。

我们仍然为每个值准备了一个位置（即便该位置是临时的），编译器知道每个值的大小，
且每个被借用的值都比从它借出的所有引用活得更久。

## 参见 {#see-also}

- [析构器中的收尾](06-finalisation-in-destructors/) 和
  [RAII 守卫](../design-patterns/01-behavioural/04-raii-guards/) 可以从对生命周期的精细控制中获益。
- 对于有条件填充的（可变）引用 `Option<&T>`，可以直接初始化一个 `Option<T>`，
  并使用其 [`.as_ref()`] 方法得到可选引用。

[`.as_ref()`]: https://doc.rust-lang.org/std/option/enum.Option.html#method.as_ref
