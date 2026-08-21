+++
title = "06-Trait 自带方法"
date = 2026-08-17T22:00:00+08:00
weight = 81
type = "docs"
description = "Trait 自带方法 — Rust 语言之旅"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Tour of Rust / Rust 语言之旅](https://github.com/richardanaya/tour_of_rust)

> 原文链接: [https://tourofrust.com/79_zh-cn.html](https://tourofrust.com/79_zh-cn.html)

# Trait 自带方法

Trait 可以有已实现的方法。

这些函数并不能直接访问结构体的内部字段，但它可以在许多 trait 实现者之间共享行为。

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
    
    fn make_alot_of_noise(&self){
        self.make_noise();
        self.make_noise();
        self.make_noise();
    }
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
    creature.make_alot_of_noise();
}
```
