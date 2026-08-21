+++
title = "36-链式方法"
date = 2026-08-21T12:46:00+08:00
weight = 37
type = "docs"
description = "链式方法 — Easy Rust 中文译本"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Easy Rust](https://dhghomon.github.io/easy_rust/)

> 原文链接: [https://dhghomon.github.io/easy_rust/Chapter_35.html](https://dhghomon.github.io/easy_rust/Chapter_35.html)

> 中文参考：[kumakichi/easy_rust_chs](https://kumakichi.github.io/easy_rust_chs/)

# 链式方法

Rust是一种系统编程语言，就像C和C++一样，它的代码可以写成独立的命令，单独成行，但它也有函数式风格。两种风格都可以，但函数式通常比较短。下面以非函数式(称为 "命令式")为例，让`Vec`从1到10。

```rust
fn main() {
    let mut new_vec = Vec::new();
    let mut counter = 1;

    while counter < 11 {
        new_vec.push(counter);
        counter += 1;
    }

    println!("{:?}", new_vec);
}
```

这个打印`[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]`。

而这里是函数式风格的例子:

```rust
fn main() {
    let new_vec = (1..=10).collect::<Vec<i32>>();
    // 也可以这样写：
    // let new_vec: Vec<i32> = (1..=10).collect();
    println!("{:?}", new_vec);
}
```

`.collect()`可以为很多类型做集合，所以我们要告诉它类型。

用函数式可以链接方法。"链接方法"的意思是把很多方法放在一个语句中。下面是一个很多方法链在一起的例子。

```rust
fn main() {
    let my_vec = vec![0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

    let new_vec = my_vec.into_iter().skip(3).take(4).collect::<Vec<i32>>();

    println!("{:?}", new_vec);
}
```

这样就创建了一个`[3, 4, 5, 6]`的Vec。这一行的信息量很大，所以把每个方法放在新的一行上会有帮助。让我们这样做，以使其更容易阅读。

```rust
fn main() {
    let my_vec = vec![0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

    let new_vec = my_vec
        .into_iter() // 对元素做“迭代”（iterate = 逐个处理）。into_iter() 给出所有权，不是引用
        .skip(3) // 跳过三个元素：0、1 和 2
        .take(4) // 取接下来四个：3、4、5 和 6
        .collect::<Vec<i32>>(); // 放进新的 Vec<i32>

    println!("{:?}", new_vec);
}
```

当你了解闭包和迭代器时，你可以最好地使用这种函数式。所以我们接下来将学习它们。
