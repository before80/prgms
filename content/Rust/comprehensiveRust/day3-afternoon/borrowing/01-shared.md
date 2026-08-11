+++
title = "2.1 借用一个值"
date = 2026-08-11T11:30:00+08:00
weight = 142
type = "docs"
description = "01-借用一个值 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/borrowing/shared.html](https://google.github.io/comprehensive-rust/borrowing/shared.html)

# 2.1 借用一个值

如前所述，调用函数时可以不转移所有权，而是让函数_借用_（borrow）该值：

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
#[derive(Debug)]
struct Point(i32, i32);

fn add(p1: &Point, p2: &Point) -> Point {
    Point(p1.0 + p2.0, p1.1 + p2.1)
}

fn main() {
    let p1 = Point(3, 4);
    let p2 = Point(10, 20);
    let p3 = add(&p1, &p2);
    println!("{p1:?} + {p2:?} = {p3:?}");
}
```

- `add` 函数_借用_两个点并返回一个新点。
- 调用方保留对输入的所有权。

> 本页是对第 1 天引用材料的回顾，略作扩展，涵盖函数参数与返回值。
>
> # 延伸阅读
>
> 关于栈返回与内联的说明：
>
> - 演示 `add` 的返回很便宜，因为编译器可以通过把对 `add` 的调用内联到 `main` 中来消除拷贝。把上面的代码改成打印栈地址，在 [Playground] 上运行，或在 [Godbolt](https://rust.godbolt.org/) 中查看汇编。在「DEBUG」优化级别下地址应会变化，而切换到「RELEASE」后地址保持相同：
>
>     ```rust
>   // Copyright 2023 Google LLC
>   // SPDX-License-Identifier: Apache-2.0
>   #
>   #[derive(Debug)]
>   struct Point(i32, i32);
>
>   fn add(p1: &Point, p2: &Point) -> Point {
>       let p = Point(p1.0 + p2.0, p1.1 + p2.1);
>       println!("&p.0: {:p}", &p.0);
>       p
>   }
>
>   pub fn main() {
>       let p1 = Point(3, 4);
>       let p2 = Point(10, 20);
>       let p3 = add(&p1, &p2);
>       println!("&p3.0: {:p}", &p3.0);
>       println!("{p1:?} + {p2:?} = {p3:?}");
>   }
>   ```
> - Rust 编译器可以自动内联；可用 `#[inline(never)]` 在函数级别禁用。
> - 禁用后，在所有优化级别下打印的地址都会变化。查看 Godbolt 或 Playground 可以看到，此时值的返回取决于 ABI，例如在 amd64 上，组成该点的两个 i32 会通过两个寄存器（eax 与 edx）返回。


[Playground]: https://play.rust-lang.org/?version=stable&mode=release&edition=2024&gist=0cb13be1c05d7e3446686ad9947c4671
