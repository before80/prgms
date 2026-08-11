+++
title = "15.1 用 Box<T> 指向堆上的数据"
date = 2026-08-05T08:44:00+08:00
weight = 68
type = "docs"
description = "用 Box<T> 在堆上存储数据，并实现递归类型"
isCJKLanguage = true
draft = false
rust_version = "1.97.1"

+++

> 译文 · 基于 [The Rust Programming Language](https://doc.rust-lang.org/stable/book/)（rustc 1.97.1）

# 用 Box<T> 指向堆上的数据 {#box-t}


> 原文链接: [https://doc.rust-lang.org/stable/book/ch15-01-box.html](https://doc.rust-lang.org/stable/book/ch15-01-box.html)


## 用 `Box<T>` 指向堆上的数据

　　最直白的智能指针是 box，其类型写作 `Box<T>`。**Box** 让你把数据存放在堆上而不是栈上；留在栈上的只是指向堆数据的指针。可回顾第 4 章关于栈与堆的区别。

　　除了把数据放在堆上而非栈上之外，box 几乎没有性能开销，额外能力也不多。你最常在这些情形下使用它们：

- 有一个编译期无法得知大小的类型，却想在要求确切大小的上下文中使用该类型的值
- 有大量数据，想转移所有权，同时又要确保转移时不会复制这些数据
- 想拥有一个值，并且只关心它实现了某个特定特征，而不关心具体是哪种类型

　　第一种情形会在 [「用 Box 启用递归类型」](#enabling-recursive-types-with-boxes) 中演示。第二种情形里，转移大量数据的所有权可能很耗时，因为数据会在栈上被来回复制。为提升性能，可以把大量数据放进 box、存到堆上；此后在栈上复制的只是很小的指针，它所引用的数据则固定留在堆上某一处。第三种情形称为**特征对象**（trait object），第 18 章的 [「用 trait 对象抽象共享行为」](/trpl/oop/02-trait-objects/) 整节都在讲这个话题。所以你在这里学到的内容，后面还会再用到！

### 在堆上存储数据

　　在讨论 `Box<T>` 的堆存储用例之前，我们先看语法，以及如何与存放在 `Box<T>` 里的值交互。

　　示例 15-1 展示如何用 box 把一个 `i32` 值存到堆上。

**文件名：`src/main.rs`**
```rust
fn main() {
    let b = Box::new(5);
    println!("b = {b}");
}
```

**示例 15-1：用 box 在堆上存储一个 `i32` 值**

　　我们定义变量 `b`，其值为一个指向 `5` 的 `Box`，而 `5` 分配在堆上。这个程序会打印 `b = 5`；此时访问 box 里的数据，方式与数据在栈上时类似。和任何被拥有的值一样，当 box 离开作用域时（这里是 `main` 结束时的 `b`），它会被释放。释放既包括栈上的 box 本身，也包括它所指向的堆上数据。

　　单独把一个值放到堆上并不特别有用，所以你很少会这样单独使用 box。像单个 `i32` 这样的值，多数情况下更适合放在默认所在的栈上。下面来看一种情形：有了 box，我们才能定义出否则无法定义的类型。

### 用 Box 启用递归类型 {#enabling-recursive-types-with-boxes}

　　**递归类型**（recursive type）的值可以把另一个同类型的值作为自身的一部分。递归类型有个问题：Rust 需要在编译期知道类型占用多少空间；而递归类型的嵌套理论上可以无限继续，Rust 就无法得知值需要多少空间。因为 box 的大小是已知的，我们就可以在递归类型定义里插入一个 box，从而启用递归类型。

　　作为递归类型的例子，我们来看 cons list。这是函数式语言中常见的数据结构。我们要定义的 cons list 类型除了递归之外很直接；因此这个例子里的概念，在你遇到更复杂的递归类型时也会有用。

#### 理解 Cons List

　　**cons list** 是源自 Lisp 及其方言的数据结构，由嵌套的序对构成，相当于 Lisp 版的链表。名字来自 Lisp 中的 `cons` 函数（_construct function_ 的缩写），它用两个参数构造一个新序对。对“一个值 + 另一个序对”再调用 `cons`，就可以构造出由递归序对组成的 cons list。

　　例如，包含列表 `1, 2, 3` 的 cons list 可用如下伪代码表示（每个序对用括号）：

```text
(1, (2, (3, Nil)))
```

　　cons list 中每一项包含两个元素：当前项的值，以及下一项。列表最后一项只有一个称为 `Nil` 的值，没有下一项。通过递归调用 `cons` 函数可以生成 cons list。表示递归基线情形的规范名称是 `Nil`。注意这与第 6 章讨论的 “null” 或 “nil” 概念不同——后者表示无效或缺失的值。

　　cons list 在 Rust 中并不常用。多数时候若有一组项，用 `Vec<T>` 更好。其他更复杂的递归数据类型在各种场景中**确实**有用；本章从 cons list 入手，可以在较少干扰的情况下探索 box 如何让我们定义递归数据类型。

　　示例 15-2 给出了表示 cons list 的枚举定义。注意这段代码目前还无法编译，因为 `List` 类型没有已知大小——我们马上会说明。

**文件名：`src/main.rs`**
```rust
enum List {
    Cons(i32, List),
    Nil,
}
```

**示例 15-2：首次尝试用枚举定义存放 `i32` 值的 cons list 数据结构**

> 说明：本例中我们实现的是只保存 `i32` 的 cons list。也可以像第 10 章那样用泛型，定义能存储任意类型值的 cons list。

　　用 `List` 类型存储列表 `1, 2, 3` 会像示例 15-3 那样。

**文件名：`src/main.rs`**
```rust
// --snip--

use crate::List::{Cons, Nil};

fn main() {
    let list = Cons(1, Cons(2, Cons(3, Nil)));
}
```

**示例 15-3：用 `List` 枚举存储列表 `1, 2, 3`**

　　第一个 `Cons` 值保存 `1` 和另一个 `List` 值。这个 `List` 又是一个保存 `2` 和另一个 `List` 的 `Cons`。再下一个 `Cons` 保存 `3` 和一个最终为 `Nil` 的 `List`——`Nil` 是非递归变体，表示列表结束。

　　若尝试编译示例 15-3 的代码，会得到示例 15-4 所示的错误。

```console
$ cargo run
   Compiling cons-list v0.1.0 (file:///projects/cons-list)
error[E0072]: recursive type `List` has infinite size
 --> src/main.rs:1:1
  |
1 | enum List {
  | ^^^^^^^^^
2 |     Cons(i32, List),
  |               ---- recursive without indirection
  |
help: insert some indirection (e.g., a `Box`, `Rc`, or `&`) to break the cycle
  |
2 |     Cons(i32, Box<List>),
  |               ++++    +

For more information about this error, try `rustc --explain E0072`.
error: could not compile `cons-list` (bin "cons-list") due to 1 previous error
```

**示例 15-4：尝试定义递归枚举时得到的错误**

　　错误显示该类型“具有无限大小”。原因是我们定义的 `List` 有一个直接持有另一个自身值的递归变体。结果是 Rust 无法算出存储一个 `List` 值需要多少空间。下面拆解为何会得到这个错误。先看 Rust 如何决定非递归类型的值需要多少空间。

#### 计算非递归类型的大小

　　回想第 6 章讨论枚举定义时，示例 6-2 中的 `Message` 枚举：

```rust
enum Message {
    Quit,
    Move { x: i32, y: i32 },
    Write(String),
    ChangeColor(i32, i32, i32),
}
```

　　为确定给 `Message` 值分配多少空间，Rust 会检查每个变体，看哪个需要最多空间。Rust 会看到 `Message::Quit` 不需要空间，`Message::Move` 需要存放两个 `i32` 的空间，以此类推。因为同一时刻只会使用一个变体，`Message` 值所需的最大空间就是其最大变体所需的空间。

　　对比之下，当 Rust 试图确定示例 15-2 中像 `List` 这样的递归类型需要多少空间时：编译器先看 `Cons` 变体，它持有一个 `i32` 和一个 `List`。因此 `Cons` 需要的空间等于一个 `i32` 的大小加上一个 `List` 的大小。而为了弄清 `List` 需要多少内存，编译器又去看各个变体，从 `Cons` 开始——`Cons` 又持有 `i32` 和 `List`——这个过程会无限继续下去，如图 15-1 所示。

<img alt="无限的 Cons 列表：标为 Cons 的矩形被分成两个更小的矩形。第一个小矩形标为 i32，第二个小矩形标为 Cons，并包含一个更小版本的外层 Cons 矩形。Cons 矩形不断包含越来越小的自身，直到最小的矩形中出现无穷符号，表示这种重复永不停止。" src="img/trpl15-01.svg" class="center" style="width: 50%;" />

<span class="caption">图 15-1：由无限多个 `Cons` 变体组成的无限 `List`</span>

#### 获得具有已知大小的递归类型

　　因为 Rust 无法算出递归定义类型该分配多少空间，编译器会给出错误，并附上这条有用的建议：


```text
help: insert some indirection (e.g., a `Box`, `Rc`, or `&`) to break the cycle
  |
2 |     Cons(i32, Box<List>),
  |               ++++    +
```

　　这里的**间接**（indirection）意味着：不要直接存储值，而应改变数据结构，改为间接存储——即存储指向该值的指针。

　　因为 `Box<T>` 是指针，Rust 始终知道 `Box<T>` 需要多少空间：指针大小不随它所指向的数据量而改变。这意味着我们可以在 `Cons` 变体里放一个 `Box<T>`，而不是直接再放一个 `List` 值。`Box<T>` 会指向下一个位于堆上的 `List` 值，而不是把它嵌在 `Cons` 变体内部。概念上我们仍然有一个由列表持有其他列表构成的列表，但实现上更像是把各项彼此相邻放置，而不是彼此嵌套。

　　我们可以把示例 15-2 中 `List` 的定义以及示例 15-3 中的用法改成示例 15-5 的代码，这样就能编译了。

**文件名：`src/main.rs`**

```rust
enum List {
    Cons(i32, Box<List>),
    Nil,
}

use crate::List::{Cons, Nil};

fn main() {
    let list = Cons(1, Box::new(Cons(2, Box::new(Cons(3, Box::new(Nil))))));
}
```

**示例 15-5**


　　`Cons` 变体需要一个 `i32` 的大小，外加存放 box 指针数据的空间。`Nil` 变体不存任何值，因此在栈上比 `Cons` 占用更少空间。现在我们知道：任意 `List` 值占用的空间等于一个 `i32` 加上一个 box 指针数据的大小。通过使用 box，我们打断了无限递归链，编译器就能算出存储 `List` 值所需的大小。图 15-2 展示了现在的 `Cons` 变体形态。

<img alt="标为 Cons 的矩形被分成两个更小的矩形。第一个小矩形标为 i32，第二个小矩形标为 Box，内部还有一个标为 usize 的矩形，表示 box 指针的有限大小。" src="img/trpl15-02.svg" class="center" />

<span class="caption">图 15-2：不再具有无限大小的 `List`，因为 `Cons` 持有一个 `Box`</span>

　　Box 只提供间接与堆分配；它们没有我们后面会看到的其他智能指针类型的那些特殊能力。它们也没有那些特殊能力带来的性能开销，因此在像 cons list 这样只需要间接的场景里很有用。第 18 章还会看到更多 box 的用例。

　　`Box<T>` 之所以是智能指针，是因为它实现了 `Deref` 特征，从而可以把 `Box<T>` 值当作引用对待。当 `Box<T>` 值离开作用域时，由于实现了 `Drop` 特征，box 所指向的堆数据也会被清理。这两个特征对本章后续讨论的其他智能指针功能更加重要。接下来我们更详细地探讨这两个特征。

[trait-objects]: /trpl/oop/02-trait-objects/#using-trait-objects-to-abstract-over-shared-behavior
