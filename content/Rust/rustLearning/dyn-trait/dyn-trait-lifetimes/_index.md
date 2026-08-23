+++
title = "4.5 dyn Trait 生命周期"
date = 2026-08-23T10:16:00+08:00
weight = 51
type = "docs"
description = ""
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Learning Rust](https://quinedot.github.io/rust-learning/)

# dyn Trait 生命周期 {#dyn-trait-lifetimes}


> 原文链接: [https://quinedot.github.io/rust-learning/dyn-trait-lifetime.html](https://quinedot.github.io/rust-learning/dyn-trait-lifetime.html)


如前所述，每个 `dyn Trait` 都有一个「trait 对象生命周期」。尽管常被省略，生命周期始终存在。

生命周期是必要的，因为实现 `Trait` 的类型未必在所有地方都有效。例如，`&'s String` 对任意生命周期 `'s` 都实现 `Display`。若将 `&'s String` 类型擦除为 `dyn Display`，Rust 需要跟踪该生命周期，以免在引用失效后仍尝试打印该值。

因此可以将 `&'s String` 强制转换为 `dyn Display + 's`，但不能转换为 `dyn Display + 'static`。

看几个例子：
```rust
# use core::fmt::Display;
fn fails() -> Box<dyn Display + 'static> {
    let local = String::new();
    // 该引用不能长于函数体
    let borrow = &local;
    // 可以强制转换为 `dyn Display`...
    let bx: Box<dyn Display + '_> = Box::new(borrow);
    // 但生命周期不能是 `'static`，因此这是错误
    bx
}
```
```rust
# use core::fmt::Display;
// 根据函数生命周期省略规则，这没问题：`dyn Display + '_` 的生命周期
// 与 `&String` 相同，且我们知道引用在该时长内有效，否则无法调用该函数。
fn works(s: &String) -> Box<dyn Display + '_> {
    Box::new(s)
}
```

## 涉及多个生命周期时 {#when-multiple-lifetimes-are-involved}

再试一个生命周期更复杂的 `struct` 例子。
```rust
trait Trait {}

// 使用 `*mut` 使生命周期不变
struct MultiRef<'a, 'b>(*mut &'a str, *mut &'b str);

impl Trait for MultiRef<'_, '_> {}

fn foo<'a, 'b>(mr: MultiRef<'a, 'b>) {
    let _: Box<dyn Trait + '_> = Box::new(mr);
}
```

这能编译，但 `'a` 可能比 `'b` 长，或 `'b` 可能比 `'a` 长，都没有限制。那么 `dyn Trait` 的生命周期是什么？不能是 `'a` 或 `'b`：
```rust
# trait Trait {}
# #[derive(Copy, Clone)] struct MultiRef<'a, 'b>(*mut &'a str, *mut &'b str);
# impl Trait for MultiRef<'_, '_> {}
// 两者都失败
fn foo<'a, 'b>(mr: MultiRef<'a, 'b>) {
    let _: Box<dyn Trait + 'a> = Box::new(mr);
    let _: Box<dyn Trait + 'b> = Box::new(mr);
}
```

此时编译器推断某个生命周期，记为 `'c`，使得 `'a` 和 `'b` 在 `'c` 的整个期间都有效。

即 `'c` 位于 `'a` 和 `'b` 的*交集*中。

任何 `'a` 和 `'b` 都有效的生命周期都可以：
```rust
# trait Trait {}
# struct MultiRef<'a, 'b>(*mut &'a str, *mut &'b str);
# impl Trait for MultiRef<'_, '_> {}
// `'c` 必须在 `'a` 和 `'b` 的交集内
fn foo<'a: 'c, 'b: 'c, 'c>(mr: MultiRef<'a, 'b>) {
    let _: Box<dyn Trait + 'c> = Box::new(mr);
}
```

注意这与 `'a + 'b` 不同——那是 `'a` 和 `'b` 的*并集*。遗憾的是，没有简洁语法表示 `'a` 和 `'b` 的交集。
