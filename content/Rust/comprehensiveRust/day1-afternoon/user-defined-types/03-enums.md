+++
title = "4.3 枚举"
date = 2026-08-11T11:30:00+08:00
weight = 57
type = "docs"
description = "03-枚举 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/user-defined-types/enums.html](https://google.github.io/comprehensive-rust/user-defined-types/enums.html)

# 4.3 枚举

`enum` 关键字可以创建具有若干不同变体（variant）的类型：

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
#[derive(Debug)]
enum Direction {
    Left,
    Right,
}

#[derive(Debug)]
enum PlayerMove {
    Pass,                        // 简单变体
    Run(Direction),              // 元组变体
    Teleport { x: u32, y: u32 }, // 结构体变体
}

fn main() {
    let dir = Direction::Left;
    let player_move: PlayerMove = PlayerMove::Run(dir);
    println!("On this turn: {player_move:?}");
}
```

> 要点：
>
> - 枚举可以把一组值归集到同一类型下。
> - `Direction` 是带有变体的类型。它有两个值：`Direction::Left` 和
>   `Direction::Right`。
> - `PlayerMove` 是带有三个变体的类型。除了各变体携带的数据外，Rust 还会存储一个判别式（discriminant），以便在运行时知道某个 `PlayerMove` 值属于哪个变体。
> - 这时可以比较结构体与枚举：
>   - 两者都可以有无字段的简单形式（单元结构体 / 单元变体），或带不同类型字段的形式（变体载荷）。
>   - 你也可以用多个独立结构体来实现枚举的不同变体，但那样它们就不是同一类型；而在同一个枚举中定义时则是同一类型。
> - Rust 用尽量少的空间存储判别式。
>   - 必要时会存储所需最小尺寸的整数。
>   - 若允许的变体值并未覆盖所有位模式，会用无效位模式来编码判别式（「niche 优化」）。例如，`Option<&u8>` 要么存储指向整数的指针，要么用 `NULL` 表示 `None` 变体。
>   - 需要时可以控制判别式（例如为了与 C 兼容）：
>
>         ```rust
>     // Copyright 2023 Google LLC
>     // SPDX-License-Identifier: Apache-2.0
>     #
>     #[repr(u32)]
>     enum Bar {
>         A, // 0
>         B = 10000,
>         C, // 10001
>     }
>
>     fn main() {
>         println!("A: {}", Bar::A as u32);
>         println!("B: {}", Bar::B as u32);
>         println!("C: {}", Bar::C as u32);
>     }
>     ```
>
>     没有 `repr` 时，判别式类型占 2 字节，因为 10001 能放进 2 字节。
>
> ## 延伸阅读
>
> Rust 有多种优化，可以让枚举占用更少空间。
>
> - 空指针优化：对
>   [某些类型](https://doc.rust-lang.org/std/option/#representation)，Rust
>   保证 `size_of::<T>()` 等于 `size_of::<Option<T>>()`。
>
>   若想展示位表示在实践中*可能*长什么样，可用下面的示例代码。务必注意：编译器对此表示不做任何保证，因此这段代码完全是 unsafe 的。
>
>     ```rust
>   // Copyright 2023 Google LLC
>   // SPDX-License-Identifier: Apache-2.0
>   #
>   use std::mem::transmute;
>
>   macro_rules! dbg_bits {
>       ($e:expr, $bit_type:ty) => {
>           println!("- {}: {:#x}", stringify!($e), transmute::<_, $bit_type>($e));
>       };
>   }
>
>   fn main() {
>       unsafe {
>           println!("bool:");
>           dbg_bits!(false, u8);
>           dbg_bits!(true, u8);
>
>           println!("Option<bool>:");
>           dbg_bits!(None::<bool>, u8);
>           dbg_bits!(Some(false), u8);
>           dbg_bits!(Some(true), u8);
>
>           println!("Option<Option<bool>>:");
>           dbg_bits!(Some(Some(false)), u8);
>           dbg_bits!(Some(Some(true)), u8);
>           dbg_bits!(Some(None::<bool>), u8);
>           dbg_bits!(None::<Option<bool>>, u8);
>
>           println!("Option<&i32>:");
>           dbg_bits!(None::<&i32>, usize);
>           dbg_bits!(Some(&0i32), usize);
>       }
>   }
>   ```

