+++
title = "07-let-else"
date = 2026-08-20T21:20:00+08:00
weight = 53
type = "docs"
description = "let-else — Rust By Example"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Rust By Example](https://doc.rust-lang.org/stable/rust-by-example/)

> 原文链接: [https://doc.rust-lang.org/stable/rust-by-example/flow_control/let_else.html](https://doc.rust-lang.org/stable/rust-by-example/flow_control/let_else.html)

# let-else

> 🛈 稳定版本：Rust 1.65 起
>
> 🛈 可通过如下方式指定 edition 进行编译：
> `rustc --edition=2021 main.rs`

借助 `let`-`else`，可反驳模式（refutable pattern）可以像普通 `let` 一样在外层作用域中匹配并绑定变量；若模式不匹配，则执行发散操作（例如 `break`、`return`、`panic!`）。

```rust
use std::str::FromStr;

fn get_count_item(s: &str) -> (u64, &str) {
    let mut it = s.split(' ');
    let (Some(count_str), Some(item)) = (it.next(), it.next()) else {
        panic!("Can't segment count item pair: '{s}'");
    };
    let Ok(count) = u64::from_str(count_str) else {
        panic!("Can't parse integer: '{count_str}'");
    };
    (count, item)
}

fn main() {
    assert_eq!(get_count_item("3 chairs"), (3, "chairs"));
}
```
与 `match` 或 `if let`-`else` 表达式相比，名称绑定的作用域是主要差异。以前可以用外层 `let` 加上一些重复代码来近似实现：

```rust
# use std::str::FromStr;
#
# fn get_count_item(s: &str) -> (u64, &str) {
#     let mut it = s.split(' ');
    let (count_str, item) = match (it.next(), it.next()) {
        (Some(count_str), Some(item)) => (count_str, item),
        _ => panic!("Can't segment count item pair: '{s}'"),
    };
    let count = if let Ok(count) = u64::from_str(count_str) {
        count
    } else {
        panic!("Can't parse integer: '{count_str}'");
    };
#     (count, item)
# }
#
# assert_eq!(get_count_item("3 chairs"), (3, "chairs"));
```
### 参见： {#参见}

[option][option]、[match][match]、[if let][if_let]，以及 [let-else RFC][let_else_rfc]。

[match]: 05-match/
[if_let]: 06-if-let/
[let_else_rfc]: https://rust-lang.github.io/rfcs/3137-let-else.html
[option]: ../std/04-option/