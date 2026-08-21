+++
title = "11-向闭包传递变量"
date = 2026-08-18T22:10:00+08:00
weight = 18
type = "docs"
description = "向闭包传递变量 — Rust Design Patterns"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Rust Design Patterns](https://rust-unofficial.github.io/patterns/)

> 原文链接: [https://rust-unofficial.github.io/patterns/idioms/pass-var-to-closure.html](https://rust-unofficial.github.io/patterns/idioms/pass-var-to-closure.html)

# 向闭包传递变量

## 描述 {#description}

默认情况下，闭包通过借用捕获其环境。也可以使用 `move` 闭包来移动整个环境。然而，你常常只想把部分变量移入闭包、给它一份数据的副本、按引用传递，或做其他某种转换。

为此，在单独的作用域中重新绑定变量。

## 示例 {#example}

使用

```rust
use std::rc::Rc;

let num1 = Rc::new(1);
let num2 = Rc::new(2);
let num3 = Rc::new(3);
let closure = {
    // `num1` 被移动
    let num2 = num2.clone();  // `num2` 被克隆
    let num3 = num3.as_ref();  // `num3` 被借用
    move || {
        *num1 + *num2 + *num3;
    }
};
```

而不是

```rust
use std::rc::Rc;

let num1 = Rc::new(1);
let num2 = Rc::new(2);
let num3 = Rc::new(3);

let num2_cloned = num2.clone();
let num3_borrowed = num3.as_ref();
let closure = move || {
    *num1 + *num2_cloned + *num3_borrowed;
};
```

## 优点 {#advantages}

被复制的数据与闭包定义放在一起，因此其用途更清晰；即使闭包没有消耗它们，它们也会立即被丢弃。

无论数据是被复制还是被移动，闭包都使用与周围代码相同的变量名。

## 缺点 {#disadvantages}

闭包体会多一层缩进。
