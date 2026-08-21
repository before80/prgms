+++
title = "05-可失败的主函数"
date = 2026-08-17T22:00:00+08:00
weight = 39
type = "docs"
description = "可失败的主函数 — Rust 语言之旅"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Tour of Rust / Rust 语言之旅](https://github.com/richardanaya/tour_of_rust)

> 原文链接: [https://tourofrust.com/37_zh-cn.html](https://tourofrust.com/37_zh-cn.html)

# 可失败的主函数

`main` 函数有可以返回 `Result` 的能力！

## 示例代码

```rust
fn do_something_that_might_fail(i: i32) -> Result<f32, String> {
    if i == 42 {
        Ok(13.0)
    } else {
        Err(String::from("this is not the right number"))
    }
}

// 主函数不返回值，但可能返回一个错误！
fn main() -> Result<(), String> {
    let result = do_something_that_might_fail(12);

    match result {
        Ok(v) => println!("found {}", v),
        Err(_e) => {
            // 优雅地处理错误
            
            // 返回一个说明发生了什么的新错误！
            return Err(String::from("something went wrong in main!"));
        }
    }

    // Notice we use a unit value inside a Result Ok
    // to represent everything is fine
    Ok(())
}
```
