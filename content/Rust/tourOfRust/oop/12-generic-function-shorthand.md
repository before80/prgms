+++
title = "12-泛型函数简写"
date = 2026-08-17T22:00:00+08:00
weight = 87
type = "docs"
description = "泛型函数简写 — Rust 语言之旅"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Tour of Rust / Rust 语言之旅](https://github.com/richardanaya/tour_of_rust)

> 原文链接: [https://tourofrust.com/85_zh-cn.html](https://tourofrust.com/85_zh-cn.html)

# 泛型函数简写

Rust 为由 Trait 限制的泛型函数提供了简写形式：

```rust
fn my_function(foo: impl Foo) {
    ...
}
```

这段代码等价于：

```rust
fn my_function<T>(foo: T)
where
    T:Foo
{
    ...
}
```

## 示例代码

```rust
struct SeaCreature {
    pub name: String,
    noise: String,
}

impl SeaCreature {
    pub fn get_sound(&self) -> &str {
        &self.noise
    }
}

trait NoiseMaker {
    fn make_noise(&self);
}

impl NoiseMaker for SeaCreature {
    fn make_noise(&self) {
        println!("{}", &self.get_sound());
    }
}

fn generic_make_noise(creature: &impl NoiseMaker)
{
    // 我们在编译期就已经知道其真实类型
    creature.make_noise();
}

fn main() {
    let creature = SeaCreature {
        name: String::from("Ferris"),
        noise: String::from("咕噜"),
    };
    generic_make_noise(&creature);
}
```
