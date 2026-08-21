+++
title = "03-使用方法进行封装"
date = 2026-08-17T22:00:00+08:00
weight = 78
type = "docs"
description = "使用方法进行封装 — Rust 语言之旅"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Tour of Rust / Rust 语言之旅](https://github.com/richardanaya/tour_of_rust)

> 原文链接: [https://tourofrust.com/76_zh-cn.html](https://tourofrust.com/76_zh-cn.html)

# 使用方法进行封装

Rust 支持*对象*的概念。“对象”是一个与一些函数（也称为*方法*）相关联的结构体。

任何方法的第一个参数必须是与方法调用相关联的实例的引用。(例如 `instanceOfObj.foo()`)。Rust 使用：
* `&self` —— 对实例的不可变引用。
* `&mut self` —— 对实例的可变引用。

方法是在一个有 `impl` 关键字的实现块中定义的：
```rust
impl MyStruct { 
    ...
    fn foo(&self) {
        ...
    }
}
```

## 示例代码

```rust
struct SeaCreature {
    noise: String,
}

impl SeaCreature {
    fn get_sound(&self) -> &str {
        &self.noise
    }
}

fn main() {
    let creature = SeaCreature {
        noise: String::from("blub"),
    };
    println!("{}", creature.get_sound());
}
```
