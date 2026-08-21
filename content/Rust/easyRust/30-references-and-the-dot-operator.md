+++
title = "30-引用和点运算符"
date = 2026-08-21T12:46:00+08:00
weight = 31
type = "docs"
description = "引用和点运算符 — Easy Rust 中文译本"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Easy Rust](https://dhghomon.github.io/easy_rust/)

> 原文链接: [https://dhghomon.github.io/easy_rust/Chapter_29.html](https://dhghomon.github.io/easy_rust/Chapter_29.html)

> 中文参考：[kumakichi/easy_rust_chs](https://kumakichi.github.io/easy_rust_chs/)

# 引用和点运算符

我们了解到，当你有一个引用时，你需要使用`*`来获取值。引用是一种不同的类型，所以这是无法运行的:

```rust
fn main() {
    let my_number = 9;
    let reference = &my_number;

    println!("{}", my_number == reference); // ⚠️
}
```

编译器打印。

```text
error[E0277]: can't compare `{integer}` with `&{integer}`
 --> src\main.rs:5:30
  |
5 |     println!("{}", my_number == reference);
  |                              ^^ no implementation for `{integer} == &{integer}`
```

所以我们把第5行改成`println!("{}", my_number == *reference);`，现在打印的是`true`，因为现在是`i32` == `i32`，而不是`i32` == `&i32`。这就是所谓的解引用。

但是当你使用一个方法时，Rust会为你解除引用。方法中的 `.` 被称为点运算符，它可以免费进行递归。

首先，让我们创建一个有一个 `u8` 字段的结构。然后，我们将对它进行引用，并尝试进行比较。它将无法工作。

```rust
struct Item {
    number: u8,
}

fn main() {
    let item = Item {
        number: 8,
    };

    let reference_number = &item.number; // reference_number 的类型是 &u8

    println!("{}", reference_number == 8); // ⚠️ &u8 和 u8 不能比较
}
```

为了让它工作，我们需要取消定义。`println!("{}", *reference_number == 8);`.

但如果使用点运算符，我们不需要`*`。例如

```rust
struct Item {
    number: u8,
}

fn main() {
    let item = Item {
        number: 8,
    };

    let reference_item = &item;

    println!("{}", reference_item.number == 8); // 不必写 *reference_item.number
}
```

现在让我们为 `Item` 创建一个方法，将 `number` 与另一个数字进行比较。我们不需要在任何地方使用 `*`。

```rust
struct Item {
    number: u8,
}

impl Item {
    fn compare_number(&self, other_number: u8) { // 接收对 self 的引用
        println!("Are {} and {} equal? {}", self.number, other_number, self.number == other_number);
            // 不必写 *self.number
    }
}

fn main() {
    let item = Item {
        number: 8,
    };

    let reference_item = &item; // 类型是 &Item
    let reference_item_two = &reference_item; // 类型是 &&Item

    item.compare_number(8); // 方法可以调用
    reference_item.compare_number(8); // 这里也能用
    reference_item_two.compare_number(8); // 这里也行

}
```

所以只要记住:当你使用`.`运算符时，你不需要担心`*`。
