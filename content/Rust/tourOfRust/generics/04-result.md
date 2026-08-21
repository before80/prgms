+++
title = "04-Result"
date = 2026-08-17T22:00:00+08:00
weight = 38
type = "docs"
description = "Result — Rust 语言之旅"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Tour of Rust / Rust 语言之旅](https://github.com/richardanaya/tour_of_rust)

> 原文链接: [https://tourofrust.com/36_zh-cn.html](https://tourofrust.com/36_zh-cn.html)

# Result

Rust 有一个内置的泛型枚举叫做 `Result`，它可以让我们返回一个可能包含错误的值。
这是编程语言进行错误处理的惯用方法。

```
enum Result<T, E> {
    Ok(T),
    Err(E),
}
```

注意我们的泛型有多个用逗号分隔的*参数化的类型*。

这个枚举很常见，使用关键字 `Ok` 和 `Err` 可以在任何地方创建其实例。

## 示例代码

```rust
fn do_something_that_might_fail(i:i32) -> Result<f32,String> {
    if i == 42 {
        Ok(13.0)
    } else {
        Err(String::from("this is not the right number"))   
    }
}

fn main() {
    let result = do_something_that_might_fail(12);

    // match 让我优雅地解构 Rust，并且确保我们处理了所有情况！
    match result {
        Ok(v) => println!("found {}", v),
        Err(e) => println!("Error: {}",e),
    }
}
```
