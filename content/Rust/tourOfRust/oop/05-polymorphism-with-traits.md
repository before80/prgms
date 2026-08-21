+++
title = "05-使用 Trait 实现多态"
date = 2026-08-17T22:00:00+08:00
weight = 80
type = "docs"
description = "使用 Trait 实现多态 — Rust 语言之旅"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Tour of Rust / Rust 语言之旅](https://github.com/richardanaya/tour_of_rust)

> 原文链接: [https://tourofrust.com/78_zh-cn.html](https://tourofrust.com/78_zh-cn.html)

# 使用 Trait 实现多态

Rust 支持多态的特性。Trait 允许我们将一组方法与结构类型关联起来。

我们首先在 Trait 里面定义函数签名：

```
trait MyTrait {
    fn foo(&self);
    ...
}
```

当一个结构体实现一个 trait 时，它便建立了一个契约，允许我们通过 trait 类型与结构体进行间接交互（例如 `&dyn MyTrait`），而不必知道其真实的类型。

结构体实现 Trait 方法是在实现块中定义要实现的方法：

```rust
impl MyTrait for MyStruct { 
    fn foo(&self) {
        ...
    }
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

fn main() {
    let creature = SeaCreature {
        name: String::from("Ferris"),
        noise: String::from("blub"),
    };
    creature.make_noise();
}
```
