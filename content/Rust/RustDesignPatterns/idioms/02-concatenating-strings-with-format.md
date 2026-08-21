+++
title = "02-用 format! 拼接字符串"
date = 2026-08-18T22:10:00+08:00
weight = 6
type = "docs"
description = "用 format! 拼接字符串 — Rust Design Patterns"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Rust Design Patterns](https://rust-unofficial.github.io/patterns/)

> 原文链接: [https://rust-unofficial.github.io/patterns/idioms/concat-format.html](https://rust-unofficial.github.io/patterns/idioms/concat-format.html)

# 用 format! 拼接字符串

## 描述 {#description}

可以用可变 `String` 上的 `push` 和 `push_str` 方法，或使用它的 `+` 运算符来逐步构建字符串。
不过，使用 `format!` 通常更方便，尤其是在字面量字符串与非字面量字符串混用的场合。

## 示例 {#example}

```rust
fn say_hello(name: &str) -> String {
    // 我们可以手动构造结果字符串。
    // let mut result = "Hello ".to_owned();
    // result.push_str(name);
    // result.push('!');
    // result

    // 但使用 format! 更好。
    format!("Hello {name}!")
}
```

## 优点 {#advantages}

使用 `format!` 通常是组合字符串最简洁、最易读的方式。

## 缺点 {#disadvantages}

它通常不是组合字符串最高效的方式——在可变字符串上执行一系列 `push`
操作通常最高效（尤其是在字符串已按预期大小预分配的情况下）。
