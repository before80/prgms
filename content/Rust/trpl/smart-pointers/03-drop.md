+++
title = "15.3 用 Drop Trait 在清理时运行代码"
date = 2026-08-05T08:44:00+08:00
weight = 70
type = "docs"
description = "实现 Drop 特征以自定义值离开作用域时的清理逻辑"
isCJKLanguage = true
draft = false
rust_version = "1.97.1"

+++

> 译文 · 基于 [The Rust Programming Language](https://doc.rust-lang.org/stable/book/)（rustc 1.97.1）

# 用 Drop Trait 在清理时运行代码 {#drop-trait}


> 原文链接: [https://doc.rust-lang.org/stable/book/ch15-03-drop.html](https://doc.rust-lang.org/stable/book/ch15-03-drop.html)


## 用 `Drop` 特征在清理时运行代码

　　对智能指针模式同样重要的第二个特征是 `Drop`：它让你可以自定义值即将离开作用域时发生什么。你可以在任意类型上实现 `Drop`，其中的代码可用于释放文件或网络连接等资源。

　　我们在智能指针的语境中介绍 `Drop`，是因为实现智能指针时几乎总会用到 `Drop` 的功能。例如，当 `Box<T>` 被丢弃时，它会释放 box 所指向的堆空间。

　　在某些语言里，对某些类型，程序员每次用完实例都必须调用代码来释放内存或资源，例如文件句柄、套接字和锁。若忘记调用，系统可能过载甚至崩溃。在 Rust 中，你可以指定每当值离开作用域时就运行某一段代码，编译器会自动插入这段代码。于是，你不必在程序各处小心翼翼地放置“某个类型的实例用完了”的清理代码——仍然不会泄漏资源！

　　通过实现 `Drop` 特征来指定值离开作用域时要运行的代码。`Drop` 要求实现一个名为 `drop` 的方法，它接受对 `self` 的可变引用。为观察 Rust 何时调用 `drop`，我们先用 `println!` 来实现它。

　　示例 15-14 展示了一个 `CustomSmartPointer` 结构体：它唯一的自定义行为是在实例离开作用域时打印 `Dropping CustomSmartPointer!`，以此展示 Rust 何时运行 `drop` 方法。

**文件名：`src/main.rs`**
```rust
struct CustomSmartPointer {
    data: String,
}

impl Drop for CustomSmartPointer {
    fn drop(&mut self) {
        println!("Dropping CustomSmartPointer with data `{}`!", self.data);
    }
}

fn main() {
    let c = CustomSmartPointer {
        data: String::from("my stuff"),
    };
    let d = CustomSmartPointer {
        data: String::from("other stuff"),
    };
    println!("CustomSmartPointers created");
}
```

**示例 15-14：实现了 `Drop` 特征的 `CustomSmartPointer`，清理代码就放在这里**

　　`Drop` 特征已包含在 prelude 中，无需额外 `use` 导入。我们在 `CustomSmartPointer` 上实现 `Drop`，并在 `drop` 方法中调用 `println!`。`drop` 方法体里写的就是你希望类型实例离开作用域时执行的逻辑。这里打印一些文字，是为了直观展示 Rust 何时调用 `drop`。

　　在 `main` 中，我们创建两个 `CustomSmartPointer` 实例，然后打印 `CustomSmartPointers created`。在 `main` 结束时，这些实例会离开作用域，Rust 会调用我们写在 `drop` 方法里的代码，打印最后的消息。注意我们并不需要显式调用 `drop` 方法。

　　运行该程序会看到如下输出：

```console
$ cargo run
   Compiling drop-example v0.1.0 (file:///projects/drop-example)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.60s
     Running `target/debug/drop-example`
CustomSmartPointers created
Dropping CustomSmartPointer with data `other stuff`!
Dropping CustomSmartPointer with data `my stuff`!
```

　　当实例离开作用域时，Rust 自动为我们调用了 `drop`，执行我们指定的代码。变量按创建的**相反**顺序被丢弃，因此 `d` 在 `c` 之前被丢弃。本例的目的是直观展示 `drop` 方法如何工作；通常你会指定类型真正需要运行的清理代码，而不是打印消息。

　　遗憾的是，禁用自动 `drop` 并不直接。通常也不需要禁用；`Drop` 特征的意义就在于它会自动完成清理。不过偶尔你可能想提前清理某个值。例如使用管理锁的智能指针时：你可能想强制调用释放锁的 `drop` 方法，好让同一作用域中的其他代码也能获取锁。Rust 不允许你手动调用 `Drop` 特征的 `drop` 方法；若想在作用域结束前强制丢弃某个值，应调用标准库提供的 `std::mem::drop` 函数。

　　若修改示例 15-14 的 `main`，尝试手动调用 `Drop` 特征的 `drop` 方法，将无法工作，如示例 15-15 所示。

**文件名：`src/main.rs`**
```rust
fn main() {
    let c = CustomSmartPointer {
        data: String::from("some data"),
    };
    println!("CustomSmartPointer created");
    c.drop();
    println!("CustomSmartPointer dropped before the end of main");
}
```

**示例 15-15：尝试手动调用 `Drop` 特征的 `drop` 方法以提前清理**

　　尝试编译这段代码时会得到如下错误：

```console
$ cargo run
   Compiling drop-example v0.1.0 (file:///projects/drop-example)
error[E0040]: explicit use of destructor method
  --> src/main.rs:16:7
   |
16 |     c.drop();
   |       ^^^^ explicit destructor calls not allowed
   |
help: consider using `drop` function
   |
16 -     c.drop();
16 +     drop(c);
   |

For more information about this error, try `rustc --explain E0040`.
error: could not compile `drop-example` (bin "drop-example") due to 1 previous error
```

　　错误信息指出不允许显式调用 `drop`。信息里用了术语**析构函数**（destructor），这是编程中清理实例的函数的通用称呼。析构函数对应于创建实例的**构造函数**（constructor）。Rust 中的 `drop` 函数就是一种特定的析构函数。

　　Rust 不允许我们显式调用 `drop`，因为到了 `main` 结束时，Rust 仍会自动对值调用 `drop`。那样会对同一值清理两次，导致双重释放错误。

　　我们既不能在值离开作用域时禁用自动插入的 `drop`，也不能显式调用 `drop` 方法。因此，若需要强制提前清理某个值，就使用 `std::mem::drop` 函数。

　　`std::mem::drop` 函数不同于 `Drop` 特征中的 `drop` 方法。调用时把想强制丢弃的值作为参数传入。该函数在 prelude 中，因此可以把示例 15-15 的 `main` 改成调用 `drop` 函数，如示例 15-16 所示。

**文件名：`src/main.rs`**
```rust
fn main() {
    let c = CustomSmartPointer {
        data: String::from("some data"),
    };
    println!("CustomSmartPointer created");
    drop(c);
    println!("CustomSmartPointer dropped before the end of main");
}
```

**示例 15-16：调用 `std::mem::drop`，在值离开作用域前显式丢弃它**

　　运行这段代码会打印：

```console
$ cargo run
   Compiling drop-example v0.1.0 (file:///projects/drop-example)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.73s
     Running `target/debug/drop-example`
CustomSmartPointer created
Dropping CustomSmartPointer with data `some data`!
CustomSmartPointer dropped before the end of main
```

　　文本 ``Dropping CustomSmartPointer with data `some data`!`` 出现在 `CustomSmartPointer created` 与 `CustomSmartPointer dropped before the end of main` 之间，说明此时调用了 `drop` 方法来丢弃 `c`。

　　你可以多种方式利用 `Drop` 实现中的代码，让清理既方便又安全：例如，可以用它创建自己的内存分配器！有了 `Drop` 特征与 Rust 的所有权系统，你不必记住去清理，因为 Rust 会自动完成。

　　你也不必担心误清理仍在使用的值：保证引用始终有效的所有权系统，同样会确保只在值不再被使用时调用一次 `drop`。

　　既然我们已经看过 `Box<T>` 以及智能指针的一些特性，接下来看看标准库中定义的另外几种智能指针。
