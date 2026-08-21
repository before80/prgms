+++
title = "08-动态调度和静态调度"
date = 2026-08-17T22:00:00+08:00
weight = 83
type = "docs"
description = "动态调度和静态调度 — Rust 语言之旅"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Tour of Rust / Rust 语言之旅](https://github.com/richardanaya/tour_of_rust)

> 原文链接: [https://tourofrust.com/81_zh-cn.html](https://tourofrust.com/81_zh-cn.html)

# 动态调度和静态调度

方法的执行有两种方式：
* 静态调度——当实例类型已知时，我们直接知道要调用什么函数。
* 动态调度——当实例类型未知时，我们必须想方法来调用正确的函数。

Trait 类型 `&dyn MyTrait` 给我们提供了使用动态调度间接处理对象实例的能力。

当使用动态调度时，Rust 会鼓励你在你的 trait 类型前加上`dyn`，以便其他人知道你在做什么。

内存细节：
* 动态调度的速度稍慢，因为要追寻指针以找到真正的函数调用。

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

fn static_make_noise(creature: &SeaCreature) {
    // 我们知道真实类型
    creature.make_noise();
}

fn dynamic_make_noise(noise_maker: &dyn NoiseMaker) {
    // 我们不知道真实类型
    noise_maker.make_noise();
}

fn main() {
    let creature = SeaCreature {
        name: String::from("Ferris"),
        noise: String::from("咕噜"),
    };
    static_make_noise(&creature);
    dynamic_make_noise(&creature);
}
```
