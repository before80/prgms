+++
title = "3.1 `Box<T>`"
date = 2026-08-11T11:30:00+08:00
weight = 134
type = "docs"
description = "01-`Box<T>` — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/smart-pointers/box.html](https://google.github.io/comprehensive-rust/smart-pointers/box.html)

# 3.1 `Box<T>`

[`Box`](https://doc.rust-lang.org/std/boxed/struct.Box.html) 是指向堆上数据的拥有型指针：

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
fn main() {
    let five = Box::new(5);
    println!("five: {}", *five);
}
```

```bob
 Stack                     Heap
.- - - - - - -.     .- - - - - - -.
:             :     :             :
:    five     :     :             :
:   +-----+   :     :   +-----+   :
:   | o---|---+-----+-->|  5  |   :
:   +-----+   :     :   +-----+   :
:             :     :             :
:             :     :             :
`- - - - - - -'     `- - - - - - -'
```

`Box<T>` 实现了 `Deref<Target = T>`，因此你可以
[直接在 `Box<T>` 上调用 `T` 的方法](https://doc.rust-lang.org/std/ops/trait.Deref.html#more-on-deref-coercion)。

递归数据类型或大小动态的数据类型，若不通过指针间接存储就无法内联存放。`Box` 提供了这种间接：

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
#[derive(Debug)]
enum List<T> {
    /// 非空列表：第一个元素以及列表的其余部分。
    Element(T, Box<List<T>>),
    /// 空列表。
    Nil,
}

fn main() {
    let list: List<i32> =
        List::Element(1, Box::new(List::Element(2, Box::new(List::Nil))));
    println!("{list:?}");
}
```

```bob
 Stack                           Heap
.- - - - - - - - - - - - - - .     .- - - - - - - - - - - - - - - - - - - - - - - - -.
:                            :     :                                                 :
:    list                    :     :                                                 :
:   +---------+----+----+    :     :    +---------+----+----+    +------+----+----+  :
:   | Element | 1  | o--+----+-----+--->| Element | 2  | o--+--->| Nil  | // | // |  :
:   +---------+----+----+    :     :    +---------+----+----+    +------+----+----+  :
:                            :     :                                                 :
:                            :     :                                                 :
'- - - - - - - - - - - - - - '     '- - - - - - - - - - - - - - - - - - - - - - - - -'
```

> - `Box` 类似 C++ 的 `std::unique_ptr`，但保证不为空。
> - `Box` 在以下情况很有用：
>   - 类型的大小在编译期无法知道，但 Rust 编译器需要确切大小。
>   - 想转移大量数据的所有权。为避免在栈上拷贝大量数据，把数据放在堆上的 `Box` 中，这样移动的只是指针。
>
> - 若不用 `Box`、试图把 `List` 直接嵌入 `List`，编译器将无法为该结构计算出固定内存大小（`List` 会变成无限大小）。
>
> - `Box` 解决了这个问题：它与普通指针大小相同，只是指向堆上 `List` 的下一个元素。
>
> - 去掉 `List` 定义中的 `Box` 并展示编译错误。会得到「recursive without indirection」之类的信息，因为数据递归必须使用间接——某种 `Box` 或引用——而不能直接存储值。
>
> - 尽管 `Box` 看起来像 C++ 的 `std::unique_ptr`，它不能为空/null。这使得 `Box` 成为允许编译器优化某些枚举存储的类型之一（「niche optimization」）。

