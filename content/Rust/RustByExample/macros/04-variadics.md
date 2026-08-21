+++
title = "04-可变参数接口"
date = 2026-08-20T21:20:00+08:00
weight = 137
type = "docs"
description = "可变参数接口 — Rust By Example"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Rust By Example](https://doc.rust-lang.org/stable/rust-by-example/)

> 原文链接: [https://doc.rust-lang.org/stable/rust-by-example/macros/variadics.html](https://doc.rust-lang.org/stable/rust-by-example/macros/variadics.html)

# 可变参数接口

可变参数接口可以接受任意数目的参数。比如说 `println` 就可以，其参数的数目是由格式化字符串指定的。

我们可以把之前的 `calculate!` 宏改写成可变参数接口：

```rust
macro_rules! calculate {
    // 单个 `eval` 的模式
    (eval $e:expr) => {
        {
            let val: usize = $e; // Force types to be integers
            println!("{} = {}", stringify!{$e}, val);
        }
    };

    // 递归地拆解多重的 `eval`
    (eval $e:expr, $(eval $es:expr),+) => {{
        calculate! { eval $e }
        calculate! { $(eval $es),+ }
    }};
}

fn main() {
    calculate! { // 妈妈快看，可变参数的 `calculate!`！
        eval 1 + 2,
        eval 3 + 4,
        eval (2 * 3) + 1
    }
}
```
输出：

```txt
1 + 2 = 3
3 + 4 = 7
(2 * 3) + 1 = 7
```
