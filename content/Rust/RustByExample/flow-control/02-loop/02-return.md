+++
title = "02-从 loop 循环返回"
date = 2026-08-20T21:20:00+08:00
weight = 40
type = "docs"
description = "从 loop 循环返回 — Rust By Example"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Rust By Example](https://doc.rust-lang.org/stable/rust-by-example/)

> 原文链接: [https://doc.rust-lang.org/stable/rust-by-example/flow_control/loop/return.html](https://doc.rust-lang.org/stable/rust-by-example/flow_control/loop/return.html)

# 从 loop 循环返回

`loop` 有个用途是尝试一个操作直到成功为止。若操作返回一个值，则可能需要将其传递给代码的其余部分：将该值放在 `break` 之后，它就会被 `loop` 表达式返回。

```rust
fn main() {
    let mut counter = 0;

    let result = loop {
        counter += 1;

        if counter == 10 {
            break counter * 2;
        }
    };

    assert_eq!(result, 20);
}
```
