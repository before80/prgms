+++
title = "3.2.2 父 Trait"
date = 2026-08-11T11:30:00+08:00
weight = 80
type = "docs"
description = "02-父 Trait — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/methods-and-traits/traits/supertraits.html](https://google.github.io/comprehensive-rust/methods-and-traits/traits/supertraits.html)

# 3.2.2 父 Trait

Trait 可以要求实现它的类型也实现其他 trait，称为_父 trait_（supertraits）。这里，任何实现 `Pet` 的类型都必须实现 `Animal`。

```rust
// Copyright 2024 Google LLC
// SPDX-License-Identifier: Apache-2.0
trait Animal {
    fn leg_count(&self) -> u32;
}

trait Pet: Animal {
    fn name(&self) -> String;
}

struct Dog(String);

impl Animal for Dog {
    fn leg_count(&self) -> u32 {
        4
    }
}

impl Pet for Dog {
    fn name(&self) -> String {
        self.0.clone()
    }
}

fn main() {
    let puppy = Dog(String::from("Rex"));
    println!("{} has {} legs", puppy.name(), puppy.leg_count());
}
```

> 这有时被称为「trait 继承」，但学员不应期望它像面向对象继承那样工作。它只是为 trait 的实现增加了额外要求。

