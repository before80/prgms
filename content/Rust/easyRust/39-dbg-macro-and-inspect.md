+++
title = "39-dbg! 宏和 .inspect"
date = 2026-08-21T12:46:00+08:00
weight = 40
type = "docs"
description = "dbg! 宏和 .inspect — Easy Rust 中文译本"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Easy Rust](https://dhghomon.github.io/easy_rust/)

> 原文链接: [https://dhghomon.github.io/easy_rust/Chapter_38.html](https://dhghomon.github.io/easy_rust/Chapter_38.html)

> 中文参考：[kumakichi/easy_rust_chs](https://kumakichi.github.io/easy_rust_chs/)

# dbg! 宏和 .inspect

`dbg!`是一个非常有用的宏，可以快速打印信息。它是 `println!` 的一个很好的替代品，因为它的输入速度更快，提供的信息更多。

```rust
fn main() {
    let my_number = 8;
    dbg!(my_number);
}
```

这样就可以打印出`[src\main.rs:4] my_number = 8`。

但实际上，你可以把`dbg!`放在其他很多地方，甚至可以把代码包在里面。比如看这段代码。

```rust
fn main() {
    let mut my_number = 9;
    my_number += 10;

    let new_vec = vec![8, 9, 10];

    let double_vec = new_vec.iter().map(|x| x * 2).collect::<Vec<i32>>();
}
```

这段代码创建了一个新的可变数字，并改变了它。然后创建一个vec，并使用`iter`和`map`以及`collect`创建一个新的vec。在这段代码中，我们几乎可以把`dbg!`放在任何地方。`dbg!`问编译器："此刻你在做什么？"，然后告诉你:

```rust
fn main() {
    let mut my_number = dbg!(9);
    dbg!(my_number += 10);

    let new_vec = dbg!(vec![8, 9, 10]);

    let double_vec = dbg!(new_vec.iter().map(|x| x * 2).collect::<Vec<i32>>());

    dbg!(double_vec);
}
```

所以这个打印:

```text
[src\main.rs:3] 9 = 9
```

和：

```text
[src\main.rs:4] my_number += 10 = ()
```

和：

```text
[src\main.rs:6] vec![8, 9, 10] = [
    8,
    9,
    10,
]
```

而这个，甚至可以显示出表达式的值。

```text
[src\main.rs:8] new_vec.iter().map(|x| x * 2).collect::<Vec<i32>>() = [
    16,
    18,
    20,
]
```

和：

```text
[src\main.rs:10] double_vec = [
    16,
    18,
    20,
]
```


`.inspect` 与 `dbg!` 有点类似，就像在迭代器中使用`map`一样使用它。它给了你迭代项，你可以打印它或者做任何你想做的事情。例如，我们再看看我们的 `double_vec`。

```rust
fn main() {
    let new_vec = vec![8, 9, 10];

    let double_vec = new_vec
        .iter()
        .map(|x| x * 2)
        .collect::<Vec<i32>>();
}
```

我们想知道更多关于代码的信息。所以我们在两个地方添加`inspect()`。

```rust
fn main() {
    let new_vec = vec![8, 9, 10];

    let double_vec = new_vec
        .iter()
        .inspect(|first_item| println!("The item is: {}", first_item))
        .map(|x| x * 2)
        .inspect(|next_item| println!("Then it is: {}", next_item))
        .collect::<Vec<i32>>();
}
```

这个打印:

```text
The item is: 8
Then it is: 16
The item is: 9
Then it is: 18
The item is: 10
Then it is: 20
```

而且因为`.inspect`采取的是封闭式，所以我们可以随意写。

```rust
fn main() {
    let new_vec = vec![8, 9, 10];

    let double_vec = new_vec
        .iter()
        .inspect(|first_item| {
            println!("The item is: {}", first_item);
            match **first_item % 2 { // first_item 是 &&i32，所以用 **
                0 => println!("It is even."),
                _ => println!("It is odd."),
            }
            println!("In binary it is {:b}.", first_item);
        })
        .map(|x| x * 2)
        .collect::<Vec<i32>>();
}
```

这个打印:

```text
The item is: 8
It is even.
In binary it is 1000.
The item is: 9
It is odd.
In binary it is 1001.
The item is: 10
It is even.
In binary it is 1010.
```
