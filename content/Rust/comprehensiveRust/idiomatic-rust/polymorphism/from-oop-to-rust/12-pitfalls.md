+++
title = "4.2.12 陷阱：过早伸手拿 `dyn Trait`"
date = 2026-08-11T11:30:00+08:00
weight = 492
type = "docs"
description = "12-陷阱：过早伸手拿 `dyn Trait` — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/idiomatic/polymorphism/from-oop-to-rust/dynamic-dispatch/pitfalls.html](https://google.github.io/comprehensive-rust/idiomatic/polymorphism/from-oop-to-rust/dynamic-dispatch/pitfalls.html)

# 4.2.12 陷阱：过早伸手拿 `dyn Trait`

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
use std::any::Any;

pub trait AddDyn: Any {
    fn add_dyn(&self, rhs: &dyn AddDyn) -> Box<dyn AddDyn>;
}

impl AddDyn for i32 {
    fn add_dyn(&self, rhs: &dyn AddDyn) -> Box<dyn AddDyn> {
        if let Some(downcast) = (rhs as &dyn Any).downcast_ref::<Self>() {
            Box::new(self + downcast)
        } else {
            Box::new(*self)
        }
    }
}

fn main() {
    let i: &dyn AddDyn = &42;
    let j: &dyn AddDyn = &64;
    let k: Box<dyn AddDyn> = i.add_dyn(j);
    dbg!((k.as_ref() as &dyn Any).is::<i32>());
    dbg!((k.as_ref() as &dyn Any).downcast_ref::<i32>());
}
```

> - 有 OOP 背景时，尽早伸手拿这个动态分发工具是可以理解的。
>
> - 但这不是首选做法：trait 对象会让我们用灵活性去换掉开发者与编译器原本对类型的了解。
>
> - 上例把事情推到荒谬的地步：若加法也绑在动态分发流程上，几乎什么都做不成。
>
>   但动态分发在许多编程语言中往往是隐藏的；这里则更显式。
>
>   在 `i32` 的 `AddDyn` 实现中，我们首先需要尝试把 `rhs` 向下转型为与 `i32` 相同的类型，若不是则静默失败。
>
>   然后需要把新值分配到堆上，因为若要继续留在动态分发的世界里，就必须如此。
>
>   两个值相加之后，若想查看结果，又必须再次向下转型成「真正」的类型才能打印——因为到目前为止操作所绑定的 trait 约束就是这样。
>
> - 向学员提问：为什么不能在 `main` 里直接加 Display 约束，好原样打印？
>
>   答案：因为 `add_dyn` 只返回 `dyn AddDyn`，从参数类型到返回类型之间我们丢失了类型实现哪些 trait 的信息。即便输入实现了 `Display`，返回类型也并不实现。
>
> - 这会导致性能更差、更难理解的代码。

