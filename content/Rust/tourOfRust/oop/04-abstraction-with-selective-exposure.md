+++
title = "04-抽象与选择性暴露"
date = 2026-08-17T22:00:00+08:00
weight = 79
type = "docs"
description = "抽象与选择性暴露 — Rust 语言之旅"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Tour of Rust / Rust 语言之旅](https://github.com/richardanaya/tour_of_rust)

> 原文链接: [https://tourofrust.com/77_zh-cn.html](https://tourofrust.com/77_zh-cn.html)

# 抽象与选择性暴露

Rust 可以隐藏对象的内部实现细节。

默认情况下，字段和方法只有它们所属的模块才可访问。

`pub` 关键字可以将字段和方法暴露给模块外的访问者。

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

fn main() {
    let creature = SeaCreature {
        name: String::from("Ferris"),
        noise: String::from("blub"),
    };
    println!("{}", creature.get_sound());
}
```
