+++
title = "04-Default Trait"
date = 2026-08-18T22:10:00+08:00
weight = 8
type = "docs"
description = "Default Trait — Rust Design Patterns"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Rust Design Patterns](https://rust-unofficial.github.io/patterns/)

> 原文链接: [https://rust-unofficial.github.io/patterns/idioms/default.html](https://rust-unofficial.github.io/patterns/idioms/default.html)

# Default Trait

## 描述 {#description}

Rust 中许多类型都有[构造器][constructor]。不过，这是类型*特有*的；Rust 无法对「一切带有 `new()` 方法的东西」进行抽象。
为了允许这种抽象，人们构想了 [`Default`] trait，它可用于容器和其他泛型类型（例如参见 [`Option::unwrap_or_default()`]）。
值得注意的是，一些容器在适用处已经实现了它。

不仅像 `Cow`、`Box` 或 `Arc` 这样的单元素容器会为所含的 `Default` 类型实现 `Default`，
还可以为所有字段都实现了该 trait 的结构体自动 `#[derive(Default)]`，因此实现 `Default` 的类型越多，它就越有用。

另一方面，构造器可以接受多个参数，而 `default()` 方法则不能。甚至可以有多个不同名称的构造器，
但每个类型只能有一个 `Default` 实现。

## 示例 {#example}

```rust
use std::{path::PathBuf, time::Duration};

// 注意这里我们可以直接自动派生 Default。
#[derive(Default, Debug, PartialEq)]
struct MyConfiguration {
    // Option 默认为 None
    output: Option<PathBuf>,
    // Vec 默认为空向量
    search_path: Vec<PathBuf>,
    // Duration 默认为零时长
    timeout: Duration,
    // bool 默认为 false
    check: bool,
}

impl MyConfiguration {
    // 在此添加 setter
}

fn main() {
    // 用默认值构造新实例
    let mut conf = MyConfiguration::default();
    // 在此对 conf 做些操作
    conf.check = true;
    println!("conf = {conf:#?}");

    // 使用默认值进行部分初始化，创建出相同的实例
    let conf1 = MyConfiguration {
        check: true,
        ..Default::default()
    };
    assert_eq!(conf, conf1);
}
```

## 参见 {#see-also}

- [构造器][constructor]惯用法是生成实例的另一种方式，这些实例可能是也可能不是「默认」的
- [`Default`] 文档（向下滚动可查看实现者列表）
- [`Option::unwrap_or_default()`]
- [`derive(new)`]

[constructor]: ctor.md
[`Default`]: https://doc.rust-lang.org/stable/std/default/trait.Default.html
[`Option::unwrap_or_default()`]: https://doc.rust-lang.org/stable/std/option/enum.Option.html#method.unwrap_or_default
[`derive(new)`]: https://crates.io/crates/derive-new/
