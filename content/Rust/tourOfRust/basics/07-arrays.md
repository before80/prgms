+++
title = "07-数组"
date = 2026-08-17T22:00:00+08:00
weight = 10
type = "docs"
description = "数组 — Rust 语言之旅"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Tour of Rust / Rust 语言之旅](https://github.com/richardanaya/tour_of_rust)

> 原文链接: [https://tourofrust.com/08_zh-cn.html](https://tourofrust.com/08_zh-cn.html)

# 数组

*数组*是所有相同类型数据元素的固定长度集合。

一个*数组*的数据类型是 `[T;N]`，其中 T 是元素的类型，N 是编译时已知的固定长度。

可以使用 `[x]` 运算符提取单个元素，其中 *x* 是所需元素的 *usize* 索引（从 0 开始）。

## 示例代码

```rust
fn main() {
    let nums: [i32; 3] = [1, 2, 3];
    println!("{:?}", nums);
    println!("{}", nums[1]);
}
```
