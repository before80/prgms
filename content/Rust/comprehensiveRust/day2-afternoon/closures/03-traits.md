+++
title = "2.3 闭包 Trait"
date = 2026-08-11T11:30:00+08:00
weight = 99
type = "docs"
description = "03-闭包 Trait — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/closures/traits.html](https://google.github.io/comprehensive-rust/closures/traits.html)

# 2.3 闭包 Trait

闭包或 lambda 表达式的类型无法命名。不过它们实现了特殊的
[`Fn`](https://doc.rust-lang.org/std/ops/trait.Fn.html)、
[`FnMut`](https://doc.rust-lang.org/std/ops/trait.FnMut.html) 与
[`FnOnce`](https://doc.rust-lang.org/std/ops/trait.FnOnce.html) trait：

特殊类型 `fn(..) -> T` 指函数指针——要么是函数地址，要么是不捕获任何东西的闭包。

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
fn apply_and_log(
    func: impl FnOnce(&'static str) -> String,
    func_name: &'static str,
    input: &'static str,
) {
    println!("Calling {func_name}({input}): {}", func(input))
}

fn main() {
    let suffix = "-itis";
    let add_suffix = |x| format!("{x}{suffix}");
    apply_and_log(&add_suffix, "add_suffix", "senior");
    apply_and_log(&add_suffix, "add_suffix", "appendix");

    let mut v = Vec::new();
    let mut accumulate = |x| {
        v.push(x);
        v.join("/")
    };
    apply_and_log(&mut accumulate, "accumulate", "red");
    apply_and_log(&mut accumulate, "accumulate", "green");
    apply_and_log(&mut accumulate, "accumulate", "blue");

    let take_and_reverse = |prefix| {
        let mut acc = String::from(prefix);
        acc.push_str(&v.into_iter().rev().collect::<Vec<_>>().join("/"));
        acc
    };
    apply_and_log(take_and_reverse, "take_and_reverse", "reversed: ");
}
```

> `Fn`（例如 `add_suffix`）既不消费也不修改捕获的值。调用它只需要对闭包的共享引用，因此闭包可以反复执行，甚至并发执行。
>
> `FnMut`（例如 `accumulate`）可能会修改捕获的值。闭包对象通过独占引用访问，因此可以反复调用，但不能并发。
>
> 若你有一个 `FnOnce`（例如 `take_and_reverse`），只能调用一次。这样做会消费闭包以及按移动捕获的任何值。
>
> `FnMut` 是 `FnOnce` 的子类型。`Fn` 是 `FnMut` 与 `FnOnce` 的子类型。也就是说，需要 `FnOnce` 的地方可以用 `FnMut`，需要 `FnMut` 或 `FnOnce` 的地方可以用 `Fn`。
>
> 定义接收闭包的函数时，若可以（即只调用一次）应取 `FnOnce`，否则取 `FnMut`，最后才是 `Fn`。这给调用方最大的灵活性。
>
> 相反，当你自己有一个闭包时，最灵活的是 `Fn`（可以传给三种闭包 trait 中任何一种的消费者），然后是 `FnMut`，最后是 `FnOnce`。
>
> 编译器还会根据闭包捕获的内容推断 `Copy`（例如 `add_suffix`）与 `Clone`（例如 `take_and_reverse`）。函数指针（对 `fn` 项的引用）实现 `Copy` 与 `Fn`。

