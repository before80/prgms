+++
title = "3.3 拥有型 Trait 对象"
date = 2026-08-11T11:30:00+08:00
weight = 136
type = "docs"
description = "03-拥有型 Trait 对象 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/smart-pointers/trait-objects.html](https://google.github.io/comprehensive-rust/smart-pointers/trait-objects.html)

# 3.3 拥有型 Trait 对象

我们之前见过 trait 对象如何与引用一起使用，例如 `&dyn Pet`。也可以把 trait 对象与 `Box` 等智能指针结合，创建拥有型 trait 对象：`Box<dyn Pet>`。

```rust
// Copyright 2024 Google LLC
// SPDX-License-Identifier: Apache-2.0
struct Dog {
    name: String,
    age: i8,
}
struct Cat {
    lives: i8,
}

trait Pet {
    fn talk(&self) -> String;
}

impl Pet for Dog {
    fn talk(&self) -> String {
        format!("Woof, my name is {}!", self.name)
    }
}

impl Pet for Cat {
    fn talk(&self) -> String {
        String::from("Miau!")
    }
}

fn main() {
    let pets: Vec<Box<dyn Pet>> = vec![
        Box::new(Cat { lives: 9 }),
        Box::new(Dog { name: String::from("Fido"), age: 5 }),
    ];
    for pet in pets {
        println!("Hello, who are you? {}", pet.talk());
    }
}
```

分配 `pets` 之后的内存布局：

```bob
 Stack                             Heap
.- - - - - - - - - - - - - - - -.     .- - - - - - - - - - - - - - - - - - - - - - -.
:                               :     :                                             :
:    "pets: Vec<Box<dyn Pet>>"  :     :   "data: Cat"         +----+----+----+----+ :
:   +-----------+-------+       :     :  +-------+-------+    | F  | i  | d  | o  | :
:   | ptr       |   o---+-------+--.  :  | lives |     9 |    +----+----+----+----+ :
:   | len       |     2 |       :  |  :  +-------+-------+      ^                   :
:   | capacity  |     2 |       :  |  :       ^                 |                   :
:   +-----------+-------+       :  |  :       |                 '-------.           :
:                               :  |  :       |               data:"Dog"|           :
:                               :  |  :       |              +-------+--|-------+   :
`- - - - - - - - - - - - - - - -'  |  :   +---|-+-----+      | name  |  o, 4, 4 |   :
                                   `--+-->| o o | o o-|----->| age   |        5 |   :
                                      :   +-|---+-|---+      +-------+----------+   :
                                      :     |     |                                 :
                                      `- - -| - - |- - - - - - - - - - - - - - - - -'
                                            |     |
                                            |     |                      "Program text"
                                      .- - -| - - |- - - - - - - - - - - - - - - - -.
                                      :     |     |       vtable                    :
                                      :     |     |      +----------------------+   :
                                      :     |     `----->| "<Dog as Pet>::talk" |   :
                                      :     |            +----------------------+   :
                                      :     |             vtable                    :
                                      :     |            +----------------------+   :
                                      :     '----------->| "<Cat as Pet>::talk" |   :
                                      :                  +----------------------+   :
                                      :                                             :
                                      '- - - - - - - - - - - - - - - - - - - - - - -'
```

> - 实现同一 trait 的类型可能大小不同。这使得上面例子中不可能有 `Vec<dyn Pet>` 这类东西。
> - `dyn Pet` 是告诉编译器：这是一个实现了 `Pet` 的动态大小类型。
> - 在本例中，`pets` 分配在栈上，向量数据在堆上。两个向量元素都是_胖指针_：
>   - 胖指针是双倍宽度的指针。它有两个组成部分：指向实际对象的指针，以及指向该对象特定 `Pet` 实现的[虚方法表]（vtable）的指针。
>   - 名为 Fido 的 `Dog` 的数据是 `name` 与 `age` 字段。`Cat` 有一个 `lives` 字段。
> - 比较上面例子中的这些输出：
>   ```rust
>   // Copyright 2024 Google LLC
>   // SPDX-License-Identifier: Apache-2.0
>   #
>   println!("{} {}", std::mem::size_of::<Dog>(), std::mem::size_of::<Cat>());
>   println!("{} {}", std::mem::size_of::<&Dog>(), std::mem::size_of::<&Cat>());
>   println!("{}", std::mem::size_of::<&dyn Pet>());
>   println!("{}", std::mem::size_of::<Box<dyn Pet>>());
>   ```
>
> [虚方法表]: https://en.wikipedia.org/wiki/Virtual_method_table

