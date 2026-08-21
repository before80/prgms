+++
title = "04-冻结"
date = 2026-08-20T21:20:00+08:00
weight = 25
type = "docs"
description = "冻结 — Rust By Example"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Rust By Example](https://doc.rust-lang.org/stable/rust-by-example/)

> 原文链接: [https://doc.rust-lang.org/stable/rust-by-example/variable_bindings/freeze.html](https://doc.rust-lang.org/stable/rust-by-example/variable_bindings/freeze.html)

# 冻结

当数据被相同的名称不变地绑定时，它还会**冻结**（freeze）。在不可变绑定超出作用域之前，无法修改已冻结的数据：

```rust
fn main() {
    let mut _mutable_integer = 7i32;

    {
        // 被不可变的 `_mutable_integer` 遮蔽
        let _mutable_integer = _mutable_integer;

        // 报错！`_mutable_integer` 在本作用域被冻结
        _mutable_integer = 50;
        // 改正 ^ 注释掉上面这行

        // `_mutable_integer` 离开作用域
    }

    // 正常运行！ `_mutable_integer` 在这个作用域没有冻结
    _mutable_integer = 3;
}
```
