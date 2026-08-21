+++
title = "13-静态生命周期"
date = 2026-08-17T22:00:00+08:00
weight = 57
type = "docs"
description = "静态生命周期 — Rust 语言之旅"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Tour of Rust / Rust 语言之旅](https://github.com/richardanaya/tour_of_rust)

> 原文链接: [https://tourofrust.com/55_zh-cn.html](https://tourofrust.com/55_zh-cn.html)

# 静态生命周期

一个**静态**变量是一个在编译期间即被创建并存在于整个程序始末的内存资源。他们必须被明确指定类型。 一个**静态生命周期**是指一段内存资源无限期地延续到程序结束。需要注意的一点是，在此定义之下，一些静态生命周期的资源也可以在运行时被创建。 拥有静态生命周期的资源会拥有一个特殊的生命周期注解 `'static`。 `'static` 资源永远也不会被 **drop** 释放。 如果静态生命周期资源包含了引用，那么这些引用的生命周期也一定是 `'static` 的。（任何缺少了此注解的引用都不会达到同样长的存活时间）

内存细节：
* 因为静态变量可以全局性地被任何人访问读取而潜在地引入数据争用，所以修改它具有内在的危险性。我们会在稍后讨论使用全局数据的一些挑战。
* Rust 允许使用 `unsafe { ... }` 代码块来进行一些无法被编译器担保的内存操作。The [<span style="color:red; font-weight: bold;">R̸͉̟͈͔̄͛̾̇͜U̶͓͖͋̅Ṡ̴͉͇̃̉̀T̵̻̻͔̟͉́͆Ơ̷̥̟̳̓͝N̶̨̼̹̲͛Ö̵̝͉̖̏̾̔M̶̡̠̺̠̐͜Î̷̛͓̣̃̐̏C̸̥̤̭̏͛̎͜O̶̧͚͖͔̊͗̇͠N̸͇̰̏̏̽̃</span>](https://doc.rust-lang.org/nomicon/)（常见的中文翻译为：Rust 死灵书）在讨论时应该被严肃地看待，

## 示例代码

```rust
static PI: f64 = 3.1415;

fn main() {
    // 静态变量的范围也可以被限制在一个函数内
    static mut SECRET: &'static str = "swordfish";

    // 字符串字面值拥有 'static 生命周期
    let msg: &'static str = "Hello World!";
    let p: &'static f64 = &PI;
    println!("{} {}", msg, p);

    // 你可以打破一些规则，但是必须是显式地
    unsafe {
        // 我们可以修改 SECRET 到一个字符串字面值因为其同样是 'static 的
        SECRET = "abracadabra";
        println!("{}", SECRET);
    }
}
```

​	以上需要将`Cargo.toml` 中的 `edition`修改为`2021`或`2018`或`2015`才可以编译通过!
