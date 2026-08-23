+++
title = "05-Crate 作者可用的属性"
date = 2026-08-22T18:00:00+08:00
weight = 50
type = "docs"
description = "扩展 Clippy 的 crate 属性"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Clippy Documentation](https://doc.rust-lang.org/nightly/clippy/)

# Crate 作者可用的属性 {#attributes-for-crate-authors}


> 原文链接: [https://doc.rust-lang.org/nightly/clippy/attribs.html](https://doc.rust-lang.org/nightly/clippy/attribs.html)


在某些情况下，可以将 Clippy 的检查范围扩展到第三方库。为此，Clippy 提供了可应用于第三方 crate 中条目的属性。

## `#[clippy::format_args]`

_自 Clippy v1.85 起可用_

该属性可添加到支持 `format!`、`println!` 或类似语法的宏上。
它告诉 Clippy 该宏是格式化宏，宏的参数应像 `format!` 的参数一样进行 lint。任何适用于 `format!` 调用的 lint 也会适用于该宏调用。宏可能在格式字符串之前有额外参数，这些参数会被忽略。

### 示例

```rust
/// 若条件为真则打印消息的宏。
#[macro_export]
#[clippy::format_args]
macro_rules! print_if {
    ($condition:expr, $($args:tt)+) => {{
        if $condition {
            println!($($args)+)
        }
    }};
}
```

## `#[clippy::has_significant_drop]`

_自 Clippy v1.60 起可用_

`clippy::has_significant_drop` 属性可添加到 Drop 实现具有重要副作用的类型上，例如解锁互斥锁，使用户能够准确理解其生命周期。
当在 match scrutinee 中的函数调用返回临时值时，其生命周期会持续到 match 块结束，这可能令人意外。

### 示例

```rust
#[clippy::has_significant_drop]
struct CounterWrapper<'a> {
    counter: &'a Counter,
}

impl<'a> Drop for CounterWrapper<'a> {
    fn drop(&mut self) {
        self.counter.i.fetch_sub(1, Ordering::Relaxed);
    }
}
```
