+++
title = "15.6 引用循环可能导致内存泄漏"
date = 2026-08-05T08:44:00+08:00
weight = 73
type = "docs"
description = "理解引用循环如何泄漏内存，并用 Weak<T> 避免它们"
isCJKLanguage = true
draft = false
rust_version = "1.97.1"

+++

> 译文 · 基于 [The Rust Programming Language](https://doc.rust-lang.org/stable/book/)（rustc 1.97.1）

# 引用循环可能导致内存泄漏


> 原文链接: [https://doc.rust-lang.org/stable/book/ch15-06-reference-cycles.html](https://doc.rust-lang.org/stable/book/ch15-06-reference-cycles.html)


## 引用循环可能导致内存泄漏

　　Rust 的内存安全保证让你很难、但并非不可能意外创建永远不会被清理的内存（称为**内存泄漏**，memory leak）。完全防止内存泄漏并不是 Rust 的保证之一，这意味着在 Rust 中内存泄漏仍属内存安全。通过使用 `Rc<T>` 与 `RefCell<T>` 可以看到 Rust 允许内存泄漏：可以创建各项彼此引用的循环引用。这会造成内存泄漏，因为循环中每一项的引用计数永远到不了 0，值也就永远不会被丢弃。

### 创建引用循环

　　我们来看引用循环可能如何发生，以及如何防止，从示例 15-25 中的 `List` 枚举定义与 `tail` 方法开始。

**文件名：`src/main.rs`**

```rust
use crate::List::{Cons, Nil};
use std::cell::RefCell;
use std::rc::Rc;

#[derive(Debug)]
enum List {
    Cons(i32, RefCell<Rc<List>>),
    Nil,
}

impl List {
    fn tail(&self) -> Option<&RefCell<Rc<List>>> {
        match self {
            Cons(_, item) => Some(item),
            Nil => None,
        }
    }
}
```

**示例 15-25**


　　我们使用示例 15-5 中 `List` 定义的又一种变体。`Cons` 变体中的第二个元素现在是 `RefCell<Rc<List>>`，意味着：与示例 15-24 中修改 `i32` 值不同，我们想修改 `Cons` 变体所指向的 `List` 值。我们还添加了 `tail` 方法，以便在有 `Cons` 变体时方便访问第二项。

　　在示例 15-26 中，我们添加使用示例 15-25 定义的 `main` 函数。这段代码在 `a` 中创建一个列表，在 `b` 中创建一个指向 `a` 的列表。然后修改 `a` 中的列表，使其指向 `b`，从而形成引用循环。过程中穿插 `println!`，以展示各阶段的引用计数。

**文件名：`src/main.rs`**
```rust
fn main() {
    let a = Rc::new(Cons(5, RefCell::new(Rc::new(Nil))));

    println!("a initial rc count = {}", Rc::strong_count(&a));
    println!("a next item = {:?}", a.tail());

    let b = Rc::new(Cons(10, RefCell::new(Rc::clone(&a))));

    println!("a rc count after b creation = {}", Rc::strong_count(&a));
    println!("b initial rc count = {}", Rc::strong_count(&b));
    println!("b next item = {:?}", b.tail());

    if let Some(link) = a.tail() {
        *link.borrow_mut() = Rc::clone(&b);
    }

    println!("b rc count after changing a = {}", Rc::strong_count(&b));
    println!("a rc count after changing a = {}", Rc::strong_count(&a));

    // Uncomment the next line to see that we have a cycle;
    // it will overflow the stack.
    // println!("a next item = {:?}", a.tail());
}
```

**示例 15-26：创建两个彼此指向的 `List` 值，形成引用循环**

　　我们创建保存 `List` 值的 `Rc<List>` 实例赋给变量 `a`，初始列表为 `5, Nil`。然后创建另一个保存 `List` 值的 `Rc<List>` 实例赋给变量 `b`，其中包含值 `10` 并指向 `a` 中的列表。

　　我们修改 `a`，使它指向 `b` 而不是 `Nil`，从而形成循环。做法是用 `tail` 方法取得 `a` 中 `RefCell<Rc<List>>` 的引用，放进变量 `link`。然后对 `RefCell<Rc<List>>` 调用 `borrow_mut`，把内部值从持有 `Nil` 的 `Rc<List>` 改为 `b` 中的 `Rc<List>`。

　　运行这段代码时（暂时保持最后一条 `println!` 被注释），会得到如下输出：

```console
$ cargo run
   Compiling cons-list v0.1.0 (file:///projects/cons-list)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.53s
     Running `target/debug/cons-list`
a initial rc count = 1
a next item = Some(RefCell { value: Nil })
a rc count after b creation = 2
b initial rc count = 1
b next item = Some(RefCell { value: Cons(5, RefCell { value: Nil }) })
b rc count after changing a = 2
a rc count after changing a = 2
```

　　把 `a` 中的列表改为指向 `b` 之后，`a` 与 `b` 中 `Rc<List>` 实例的引用计数都是 2。在 `main` 结束时，Rust 丢弃变量 `b`，把 `b` 的 `Rc<List>` 实例的引用计数从 2 减到 1。此时堆上 `Rc<List>` 的内存不会被丢弃，因为引用计数是 1 而不是 0。然后 Rust 丢弃 `a`，把 `a` 的 `Rc<List>` 实例的引用计数从 2 也减到 1。该实例的内存同样无法丢弃，因为另一个 `Rc<List>` 实例仍引用着它。为列表分配的内存将永远不会被回收。为可视化这一引用循环，我们绘制了图 15-4。

<img alt="标为 a 的矩形指向包含整数 5 的矩形。标为 b 的矩形指向包含整数 10 的矩形。包含 5 的矩形指向包含 10 的矩形，包含 10 的矩形又指回包含 5 的矩形，形成循环。" src="img/trpl15-04.svg" class="center" />

<span class="caption">图 15-4：列表 `a` 与 `b` 彼此指向形成的引用循环</span>

　　若取消注释最后一条 `println!` 并运行程序，Rust 会尝试打印这个循环：`a` 指向 `b`，`b` 指向 `a`，如此往复，直到栈溢出。

　　与真实程序相比，本例中创建引用循环的后果并不严重：创建循环后程序很快就结束了。然而，若更复杂的程序在循环中分配大量内存并长时间持有，程序会使用超出所需的内存，并可能压垮系统，导致可用内存耗尽。

　　创建引用循环并不容易，但也并非不可能。若你有包含 `Rc<T>` 值的 `RefCell<T>`，或类似的“内部可变性 + 引用计数”嵌套类型组合，就必须确保不创建循环；不能指望 Rust 会抓住它们。创建引用循环属于程序中的逻辑 bug，应通过自动化测试、代码审查及其他软件开发实践来尽量减少。

　　避免引用循环的另一种办法是重组数据结构，使一部分引用表达所有权，另一部分不表达。这样你就可以有由部分所有权关系与部分非所有权关系组成的循环，而只有所有权关系会影响值能否被丢弃。在示例 15-25 中，我们始终希望 `Cons` 变体拥有其列表，因此无法重组数据结构。下面看一个由父节点与子节点组成的图的例子，了解何时用非所有权关系来防止引用循环是合适的。

### 用 `Weak<T>` 防止引用循环 {#preventing-reference-cycles-turning-an-rct-into-a-weakt}

　　到目前为止我们已经说明：调用 `Rc::clone` 会增加 `Rc<T>` 实例的 `strong_count`，且只有当 `strong_count` 为 0 时才会清理 `Rc<T>` 实例。你也可以通过调用 `Rc::downgrade` 并传入对 `Rc<T>` 的引用，创建指向 `Rc<T>` 实例内值的弱引用。**强引用**（strong reference）是共享 `Rc<T>` 实例所有权的方式。**弱引用**（weak reference）不表达所有权关系，其计数也不影响何时清理 `Rc<T>` 实例。它们不会造成引用循环，因为一旦相关值的强引用计数变为 0，任何包含弱引用的循环都会被打断。

　　调用 `Rc::downgrade` 时，你会得到类型为 `Weak<T>` 的智能指针。调用 `Rc::downgrade` 不会把 `Rc<T>` 实例的 `strong_count` 加 1，而是把 `weak_count` 加 1。`Rc<T>` 类型用 `weak_count` 跟踪存在多少个 `Weak<T>` 引用，这与 `strong_count` 类似。区别在于：清理 `Rc<T>` 实例并不要求 `weak_count` 为 0。

　　因为 `Weak<T>` 所引用的值可能已被丢弃，要对 `Weak<T>` 指向的值做任何事，都必须先确认该值仍然存在。做法是对 `Weak<T>` 实例调用 `upgrade` 方法，它会返回 `Option<Rc<T>>`。若 `Rc<T>` 值尚未被丢弃，会得到 `Some`；若已被丢弃，会得到 `None`。因为 `upgrade` 返回 `Option<Rc<T>>`，Rust 会确保处理 `Some` 与 `None` 两种情形，从而不会出现无效指针。

　　作为例子，我们不再使用“各项只知道下一项”的列表，而是创建一棵树：各项既知道其子项，也知道其父项。

#### 创建树形数据结构

　　首先，我们构建一棵节点知道其子节点的树。创建一个名为 `Node` 的结构体，保存它自己的 `i32` 值，以及对子 `Node` 值的引用：

<span class="filename">文件名：src/main.rs</span>

```rust
use std::cell::RefCell;
use std::rc::Rc;

#[derive(Debug)]
struct Node {
    value: i32,
    children: RefCell<Vec<Rc<Node>>>,
}
```

　　我们希望 `Node` 拥有其子节点，并希望与变量共享该所有权，以便能直接访问树中每个 `Node`。为此，我们把 `Vec<T>` 的元素定义为 `Rc<Node>` 类型的值。我们还希望能修改哪些节点是另一节点的子节点，因此在 `children` 中用 `RefCell<T>` 包住 `Vec<Rc<Node>>`。

　　接下来使用该结构体定义，创建一个值为 `3`、没有子节点的 `Node` 实例 `leaf`，以及值为 `5`、以 `leaf` 为子节点之一的实例 `branch`，如示例 15-27 所示。

**文件名：`src/main.rs`**
```rust
fn main() {
    let leaf = Rc::new(Node {
        value: 3,
        children: RefCell::new(vec![]),
    });

    let branch = Rc::new(Node {
        value: 5,
        children: RefCell::new(vec![Rc::clone(&leaf)]),
    });
}
```

**示例 15-27：创建没有子节点的 `leaf` 节点，以及以 `leaf` 为子节点之一的 `branch` 节点**

　　我们克隆 `leaf` 中的 `Rc<Node>` 并存进 `branch`，意味着 `leaf` 中的 `Node` 现在有两个所有者：`leaf` 与 `branch`。可以通过 `branch.children` 从 `branch` 到达 `leaf`，但从 `leaf` 无法到达 `branch`。原因是 `leaf` 没有对 `branch` 的引用，也不知道它们有关联。我们希望 `leaf` 知道 `branch` 是它的父节点。接下来就做这件事。

#### 从子节点添加指向父节点的引用

　　为让子节点知道其父节点，需要在 `Node` 结构体定义中添加 `parent` 字段。麻烦在于决定 `parent` 应是什么类型。我们知道它不能包含 `Rc<T>`，因为那会形成引用循环：`leaf.parent` 指向 `branch`，`branch.children` 指向 `leaf`，会使它们的 `strong_count` 永远到不了 0。

　　换个角度想关系：父节点应拥有其子节点——若父节点被丢弃，子节点也应被丢弃。然而，子节点不应拥有其父节点——若丢弃子节点，父节点仍应存在。弱引用正好适用于这种情况！

　　因此，我们不用 `Rc<T>`，而让 `parent` 的类型使用 `Weak<T>`，具体是 `RefCell<Weak<Node>>`。现在 `Node` 结构体定义如下：

<span class="filename">文件名：src/main.rs</span>

```rust
use std::cell::RefCell;
use std::rc::{Rc, Weak};

#[derive(Debug)]
struct Node {
    value: i32,
    parent: RefCell<Weak<Node>>,
    children: RefCell<Vec<Rc<Node>>>,
}
```

　　节点将能够引用其父节点，但不拥有父节点。在示例 15-28 中，我们更新 `main` 以使用这一定义，使 `leaf` 节点有办法引用其父节点 `branch`。

**文件名：`src/main.rs`**
```rust
fn main() {
    let leaf = Rc::new(Node {
        value: 3,
        parent: RefCell::new(Weak::new()),
        children: RefCell::new(vec![]),
    });

    println!("leaf parent = {:?}", leaf.parent.borrow().upgrade());

    let branch = Rc::new(Node {
        value: 5,
        parent: RefCell::new(Weak::new()),
        children: RefCell::new(vec![Rc::clone(&leaf)]),
    });

    *leaf.parent.borrow_mut() = Rc::downgrade(&branch);

    println!("leaf parent = {:?}", leaf.parent.borrow().upgrade());
}
```

**示例 15-28：带有指向父节点 `branch` 的弱引用的 `leaf` 节点**

　　创建 `leaf` 节点与示例 15-27 类似，区别在于 `parent` 字段：`leaf` 起初没有父节点，因此我们创建一个新的空 `Weak<Node>` 引用实例。

　　此时，若用 `upgrade` 方法尝试取得 `leaf` 的父节点引用，会得到 `None`。第一条 `println!` 的输出可以看到这一点：

```text
leaf parent = None
```

　　创建 `branch` 节点时，其 `parent` 字段也会有一个新的 `Weak<Node>` 引用，因为 `branch` 没有父节点。我们仍然把 `leaf` 作为 `branch` 的子节点之一。一旦有了 `branch` 中的 `Node` 实例，就可以修改 `leaf`，给它一个指向父节点的 `Weak<Node>` 引用。我们对 `leaf` 的 `parent` 字段中的 `RefCell<Weak<Node>>` 调用 `borrow_mut`，然后用 `Rc::downgrade` 从 `branch` 中的 `Rc<Node>` 创建指向 `branch` 的 `Weak<Node>` 引用。

　　再次打印 `leaf` 的父节点时，这次会得到持有 `branch` 的 `Some` 变体：现在 `leaf` 可以访问其父节点了！打印 `leaf` 时，我们也避免了示例 15-26 中最终导致栈溢出的那种循环；`Weak<Node>` 引用会被打印为 `(Weak)`：

```text
leaf parent = Some(Node { value: 5, parent: RefCell { value: (Weak) },
children: RefCell { value: [Node { value: 3, parent: RefCell { value: (Weak) },
children: RefCell { value: [] } }] } })
```

　　没有无限输出，表明这段代码没有创建引用循环。通过查看调用 `Rc::strong_count` 与 `Rc::weak_count` 得到的值，也能看出这一点。

#### 观察 `strong_count` 与 `weak_count` 的变化

　　我们通过新建内部作用域、并把 `branch` 的创建移入该作用域，来观察 `Rc<Node>` 实例的 `strong_count` 与 `weak_count` 如何变化。这样就能看到创建 `branch`、以及它离开作用域被丢弃时会发生什么。修改如示例 15-29 所示。

**文件名：`src/main.rs`**
```rust
fn main() {
    let leaf = Rc::new(Node {
        value: 3,
        parent: RefCell::new(Weak::new()),
        children: RefCell::new(vec![]),
    });

    println!(
        "leaf strong = {}, weak = {}",
        Rc::strong_count(&leaf),
        Rc::weak_count(&leaf),
    );

    {
        let branch = Rc::new(Node {
            value: 5,
            parent: RefCell::new(Weak::new()),
            children: RefCell::new(vec![Rc::clone(&leaf)]),
        });

        *leaf.parent.borrow_mut() = Rc::downgrade(&branch);

        println!(
            "branch strong = {}, weak = {}",
            Rc::strong_count(&branch),
            Rc::weak_count(&branch),
        );

        println!(
            "leaf strong = {}, weak = {}",
            Rc::strong_count(&leaf),
            Rc::weak_count(&leaf),
        );
    }

    println!("leaf parent = {:?}", leaf.parent.borrow().upgrade());
    println!(
        "leaf strong = {}, weak = {}",
        Rc::strong_count(&leaf),
        Rc::weak_count(&leaf),
    );
}
```

**示例 15-29：在内部作用域创建 `branch`，并检查强引用与弱引用计数**

　　创建 `leaf` 之后，其 `Rc<Node>` 的强引用计数为 1，弱引用计数为 0。在内部作用域中，我们创建 `branch` 并把它与 `leaf` 关联；此时打印计数时，`branch` 中的 `Rc<Node>` 强引用计数为 1，弱引用计数为 1（因为 `leaf.parent` 用 `Weak<Node>` 指向 `branch`）。打印 `leaf` 的计数时，会看到强引用计数为 2——因为 `branch` 现在在 `branch.children` 中存有 `leaf` 的 `Rc<Node>` 的克隆——弱引用计数仍为 0。

　　内部作用域结束时，`branch` 离开作用域，`Rc<Node>` 的强引用计数减到 0，于是其 `Node` 被丢弃。来自 `leaf.parent` 的弱引用计数 1 不影响 `Node` 是否被丢弃，因此我们不会发生内存泄漏！

　　若在作用域结束后尝试访问 `leaf` 的父节点，会再次得到 `None`。在程序结束时，`leaf` 中的 `Rc<Node>` 强引用计数为 1、弱引用计数为 0，因为变量 `leaf` 又成了对该 `Rc<Node>` 的唯一引用。

　　管理计数与值丢弃的全部逻辑都内建于 `Rc<T>`、`Weak<T>` 及其对 `Drop` 特征的实现中。通过在 `Node` 的定义中指定“从子节点到父节点的关系应是 `Weak<T>` 引用”，你就能让父节点指向子节点、子节点也指向父节点，而不会创建引用循环与内存泄漏。

## 小结

　　本章介绍了如何用智能指针做出与 Rust 默认对常规引用所做保证不同的权衡。`Box<T>` 类型具有已知大小，并指向分配在堆上的数据。`Rc<T>` 类型跟踪指向堆上数据的引用数量，从而使数据可以有多个所有者。带有内部可变性的 `RefCell<T>` 让我们在需要“外表不可变、却要改内部值”的类型时可以使用它；它还在运行时而不是编译期强制执行借用规则。

　　我们也讨论了 `Deref` 与 `Drop` 特征，它们支撑了智能指针的许多功能。我们探索了可能导致内存泄漏的引用循环，以及如何用 `Weak<T>` 防止它们。

　　若本章激起了你的兴趣，想自己实现智能指针，可查阅 [《Rustonomicon》][nomicon] 获取更多有用信息。

　　接下来，我们将讨论 Rust 中的并发。你甚至还会学到几种新的智能指针。

[nomicon]: https://doc.rust-lang.org/nomicon/index.html
