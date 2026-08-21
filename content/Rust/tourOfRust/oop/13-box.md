+++
title = "13-Box"
date = 2026-08-17T22:00:00+08:00
weight = 88
type = "docs"
description = "Box — Rust 语言之旅"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Tour of Rust / Rust 语言之旅](https://github.com/richardanaya/tour_of_rust)

> 原文链接: [https://tourofrust.com/86_zh-cn.html](https://tourofrust.com/86_zh-cn.html)

# Box

`Box` 是一个允许我们将数据从栈上移到堆上的数据结构。

`Box` 是一个被称为*智能指针*的结构，它持有指向我们在堆上的数据的指针。

由于 `Box` 是一个已知大小的结构体（因为它只是持有一个指针）， 因此它经常被用在一个必须知道其字段大小的结构体中存储对某个目标的引用。

`Box` 非常常见，它几乎可以被用在任何地方：

```rust
Box::new(Foo { ... })
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

struct Ocean {
    animals: Vec<Box<dyn NoiseMaker>>,
}

fn main() {
    let ferris = SeaCreature {
        name: String::from("Ferris"),
        noise: String::from("咕噜"),
    };
    let sarah = SeaCreature {
        name: String::from("Sarah"),
        noise: String::from("哧溜"),
    };
    let ocean = Ocean {
        animals: vec![Box::new(ferris), Box::new(sarah)],
    };
    for a in ocean.animals.iter() {
        a.make_noise();
    }
}
```
