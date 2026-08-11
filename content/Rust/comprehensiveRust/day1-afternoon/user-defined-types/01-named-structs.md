+++
title = "4.1 具名结构体"
date = 2026-08-11T11:30:00+08:00
weight = 55
type = "docs"
description = "01-具名结构体 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/user-defined-types/named-structs.html](https://google.github.io/comprehensive-rust/user-defined-types/named-structs.html)

# 4.1 具名结构体

与 C 和 C++ 一样，Rust 也支持自定义结构体（struct）：

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
struct Person {
    name: String,
    age: u8,
}

fn describe(person: &Person) {
    println!("{} is {} years old", person.name, person.age);
}

fn main() {
    let mut peter = Person {
        name: String::from("Peter"),
        age: 27,
    };
    describe(&peter);

    peter.age = 28;
    describe(&peter);

    let name = String::from("Avery");
    let age = 39;
    let avery = Person { name, age };
    describe(&avery);
}
```

> 要点：
>
> - 结构体的用法与 C 或 C++ 类似。
>   - 与 C++ 一样、与 C 不同：定义类型时不需要 typedef。
>   - 与 C++ 不同：结构体之间没有继承。
> - 这时可以向学员说明 Rust 有多种结构体形式。
>   - 零大小结构体（例如 `struct Foo;`）常用于在某类型上实现 trait，但值本身不需要存储数据。
>   - 下一页会介绍元组结构体（tuple struct），适用于字段名不重要的场景。
> - 若已有同名字段的变量，可以用字段初始化简写语法创建结构体。
> - 结构体字段不支持默认值。默认值通过实现 `Default` trait 指定，后面会讲到。
>
> ## 延伸阅读
>
> - 此处也可以演示结构体更新语法（struct update syntax）：
>
>   ```rust
>   // Copyright 2023 Google LLC
>   // SPDX-License-Identifier: Apache-2.0
>   #
>   let jackie = Person { name: String::from("Jackie"), ..avery };
>   ```
>
> - 它允许从旧结构体复制大部分字段，而不必逐一写出。该语法必须始终放在最后一个元素。
>
> - 它主要与 `Default` trait 结合使用。结构体更新语法会在讲 `Default` trait 的页面更详细讨论；除非学员主动问起，这里不必展开。

