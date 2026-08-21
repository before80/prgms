+++
title = "06-优雅地错误处理"
date = 2026-08-17T22:00:00+08:00
weight = 40
type = "docs"
description = "优雅地错误处理 — Rust 语言之旅"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Tour of Rust / Rust 语言之旅](https://github.com/richardanaya/tour_of_rust)

> 原文链接: [https://tourofrust.com/38_zh-cn.html](https://tourofrust.com/38_zh-cn.html)

# 优雅地错误处理

`Result` 如此常见以至于 Rust 有个强大的操作符 `?` 来与之配合。
以下两个表达式是等价的：

```
do_something_that_might_fail()?
```

```
match do_something_that_might_fail() {
    Ok(v) => v,
    Err(e) => return Err(e),
}
```

## 示例代码

```rust
fn do_something_that_might_fail(i: i32) -> Result<f32, String> {
    if i == 42 {
        Ok(13.0)
    } else {
        Err(String::from("this is not the right number"))
    }
}

fn main() -> Result<(), String> {
    // 看看我们节省了多少代码！
    let v = do_something_that_might_fail(42)?;
    println!("found {}", v);
    Ok(())
}
```
