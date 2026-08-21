+++
title = "54-Box"
date = 2026-08-21T12:46:00+08:00
weight = 55
type = "docs"
description = "Box — Easy Rust 中文译本"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Easy Rust](https://dhghomon.github.io/easy_rust/)

> 原文链接: [https://dhghomon.github.io/easy_rust/Chapter_53.html](https://dhghomon.github.io/easy_rust/Chapter_53.html)

> 中文参考：[kumakichi/easy_rust_chs](https://kumakichi.github.io/easy_rust_chs/)

# Box

`Box` 是 Rust 中一个非常方便的类型。当你使用`Box`时，你可以把一个类型放在堆上而不是栈上。要创建一个新的 `Box`，只需使用 `Box::new()` 并将元素放在里面即可。

```rust
fn just_takes_a_variable<T>(item: T) {} // 接受任意类型并丢弃。

fn main() {
    let my_number = 1; // 这是 i32
    just_takes_a_variable(my_number);
    just_takes_a_variable(my_number); // 调用两次没问题，因为它是 Copy

    let my_box = Box::new(1); // 这是 Box<i32>
    just_takes_a_variable(my_box.clone()); // 没有 .clone() 的话，第二次调用会报错
    just_takes_a_variable(my_box); // 因为 Box 不是 Copy
}
```

一开始很难想象在哪里使用它，但你在Rust中经常使用它。你记得`&`是用于`str`的，因为编译器不知道`str`的大小:它可以是任何长度。但是`&`的引用总是相同的长度，所以编译器可以使用它。`Box`也是类似的。另外，你也可以在`Box`上使用`*`来获取值，就像使用`&`一样。

```rust
fn main() {
    let my_box = Box::new(1); // 这是 Box<i32>
    let an_integer = *my_box; // 这是 i32
    println!("{:?}", my_box);
    println!("{:?}", an_integer);
}
```

这就是为什么Box被称为 "智能指针"的原因，因为它就像`&`的引用(指针的一种)，但可以做更多的事情。

你也可以使用Box来创建里面有相同结构的结构体。这些结构被称为*递归*，这意味着在Struct A里面也许是另一个Struct A，有时你可以使用Box来创建链表，尽管这在Rust中并不十分流行。但如果你想创建一个递归结构，你可以使用`Box`。如果你试着不用 `Box` 会发生什么:


```rust
struct List {
    item: Option<List>, // ⚠️
}
```

这个简单的`List`有一项，可能是`Some<List>`(另一个列表)，也可能是`None`。因为你可以选择`None`，所以它不会永远递归。但是编译器还是不知道大小。

```text
error[E0072]: recursive type `List` has infinite size
  --> src\main.rs:16:1
   |
16 | struct List {
   | ^^^^^^^^^^^ recursive type has infinite size
17 |     item: Option<List>,
   |     ------------------ recursive without indirection
   |
   = help: insert indirection (e.g., a `Box`, `Rc`, or `&`) at some point to make `List` representable
```

你可以看到，它甚至建议尝试`Box`。所以我们用`Box`把List包裹起来。

```rust
struct List {
    item: Option<Box<List>>,
}
fn main() {}
```

现在编译器用`List`就可以了，因为所有的东西都在`Box`后面，而且它知道`Box`的大小。那么一个非常简单的列表可能是这样的:

```rust
struct List {
    item: Option<Box<List>>,
}

impl List {
    fn new() -> List {
        List {
            item: Some(Box::new(List { item: None })),
        }
    }
}

fn main() {
    let mut my_list = List::new();
}
```

即使没有数据也有点复杂，Rust并不怎么使用这种类型的模式。这是因为Rust对借用和所有权有严格的规定，你知道的。但如果你想启动一个这样的列表(链表)，`Box`可以帮助你。

`Box`还可以让你在上面使用`std::mem::drop`，因为它在堆上。这有时会很方便。
