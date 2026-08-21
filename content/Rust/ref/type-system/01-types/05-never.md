+++
title = "05-Never 类型"
date = 2026-08-18T08:45:00+08:00
weight = 70
type = "docs"
description = "Never 类型 — The Rust Reference"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Reference](https://doc.rust-lang.org/reference/)

> 原文链接: [https://doc.rust-lang.org/reference/types/never.html](https://doc.rust-lang.org/reference/types/never.html)

r[type.never]
# Never 类型

r[type.never.syntax]
```grammar,types
NeverType -> `!`
```

r[type.never.intro]
Never 类型 `!` 是没有值的类型，表示永不完成的计算的结果。

r[type.never.coercion]
类型为 `!` 的表达式可以被强制转换为任何其他类型。

r[type.never.constraint]
目前 `!` 类型**只能**出现在函数返回类型中，表示这是一个永不返回的发散函数。

```rust
fn foo() -> ! {
    panic!("This call never returns.");
}
```

```rust
unsafe extern "C" {
    pub safe fn no_return_extern_func() -> !;
}
```
