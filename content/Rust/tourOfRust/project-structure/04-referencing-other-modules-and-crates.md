+++
title = "04-引用其他模块和 crate"
date = 2026-08-17T22:00:00+08:00
weight = 111
type = "docs"
description = "引用其他模块和 crate — Rust 语言之旅"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Tour of Rust / Rust 语言之旅](https://github.com/richardanaya/tour_of_rust)

> 原文链接: [https://tourofrust.com/109_zh-cn.html](https://tourofrust.com/109_zh-cn.html)

# 引用其他模块和 crate

你可以使用完整的模块路径路径引用模块中的项目： `std::f64::consts::PI`。

更简单的方法是使用**use**关键字。此关键字可以让我们在代码中使用模块中的项目而无需指定完整路径。例如 `use std::f64::consts::PI`
这样我在 main 函数中只需要写 `PI` 就可以了。

**std** 是 Rust 的**标准库**。这个库中包含了大量有用的数据结构和与操作系统交互的函数。

由社区创建的 crate 的搜索索引可以在这里找到： [https://crates.io](https://crates.io/).

## 示例代码

```rust
use std::f64::consts::PI;

fn main() {
    println!("欢迎来到练习场！");
    println!("我想要一块 {}！", PI);
}
```
