+++
title = "15-出错时归还已消耗的参数"
date = 2026-08-18T22:10:00+08:00
weight = 22
type = "docs"
description = "出错时归还已消耗的参数 — Rust Design Patterns"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Rust Design Patterns](https://rust-unofficial.github.io/patterns/)

> 原文链接: [https://rust-unofficial.github.io/patterns/idioms/return-consumed-arg-on-error.html](https://rust-unofficial.github.io/patterns/idioms/return-consumed-arg-on-error.html)

# 出错时归还已消耗的参数

## 描述 {#description}

如果一个可能失败的函数会消耗（移动）某个参数，请在错误中把该参数归还回去。

## 示例 {#example}

```rust
pub fn send(value: String) -> Result<(), SendError> {
    println!("using {value} in a meaningful way");
    // 模拟非确定性的可能失败的操作。
    use std::time::SystemTime;
    let period = SystemTime::now()
        .duration_since(SystemTime::UNIX_EPOCH)
        .unwrap();
    if period.subsec_nanos() % 2 == 1 {
        Ok(())
    } else {
        Err(SendError(value))
    }
}

pub struct SendError(String);

fn main() {
    let mut value = "imagine this is very long string".to_string();

    let success = 's: {
        // 尝试发送 value 两次。
        for _ in 0..2 {
            value = match send(value) {
                Ok(()) => break 's true,
                Err(SendError(value)) => value,
            }
        }
        false
    };

    println!("success: {success}");
}
```

## 动机 {#motivation}

出错时，你可能想尝试其他途径，或者在非确定性函数的情况下重试该操作。但如果参数总是被消耗，你就被迫在每次调用时克隆它，这不太高效。

标准库在例如 `String::from_utf8` 方法中使用了这种方法。当给定的 vector 不包含有效 UTF-8 时，会返回 `FromUtf8Error`。你可以用 `FromUtf8Error::into_bytes` 方法取回原来的 vector。

## 优点 {#advantages}

尽可能移动参数，因而性能更好。

## 缺点 {#disadvantages}

错误类型稍复杂一些。
