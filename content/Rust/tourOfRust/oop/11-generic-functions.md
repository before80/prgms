+++
title = "11-泛型函数"
date = 2026-08-17T22:00:00+08:00
weight = 86
type = "docs"
description = "泛型函数 — Rust 语言之旅"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Tour of Rust / Rust 语言之旅](https://github.com/richardanaya/tour_of_rust)

> 原文链接: [https://tourofrust.com/84_zh-cn.html](https://tourofrust.com/84_zh-cn.html)

# 泛型函数

Rust中的泛型与 Trait 是相辅相成的。 当我们描述一个参数化类型 `T` 时，我们可以通过列出参数必须实现的 Trait 来限制哪些类型可以作为参数使用。

在以下例子中，类型 `T` 必须实现 `Foo` 这个 Trait：
```rust
fn my_function<T>(foo: T)
where
    T:Foo
{
    ...
}
```

通过使用泛型，我们在编译时创建静态类型的函数，这些函数有已知的类型和大小，允许我们对其执行静态调度，并存储为有已知大小的值。

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

fn generic_make_noise<T>(creature: &T)
where
    T: NoiseMaker,
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
