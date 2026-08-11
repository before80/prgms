+++
title = "16.3 共享状态并发"
date = 2026-08-05T08:44:00+08:00
weight = 77
type = "docs"
description = "用 Mutex 与 Arc 在多线程间安全共享可变状态"
isCJKLanguage = true
draft = false
rust_version = "1.97.1"

+++

> 译文 · 基于 [The Rust Programming Language](https://doc.rust-lang.org/stable/book/)（rustc 1.97.1）

# 共享状态并发


> 原文链接: [https://doc.rust-lang.org/stable/book/ch16-03-shared-state.html](https://doc.rust-lang.org/stable/book/ch16-03-shared-state.html)


## 共享状态并发

　　消息传递是处理并发的好方法，但不是唯一方法。另一种方法是让多个线程访问同一份共享数据。再想想 Go 语言文档中那句口号的一部分：“不要通过共享内存来通信。”

　　通过共享内存来通信会是什么样子？此外，为何消息传递的拥护者会告诫不要使用内存共享？

　　在某种意义上，任何编程语言中的通道都类似单一所有权：一旦把值沿通道传出去，就不该再使用该值。共享内存并发则类似多重所有权：多个线程可以同时访问同一内存位置。正如你在第 15 章所见，智能指针使多重所有权成为可能，而多重所有权可能增加复杂性，因为这些不同所有者需要管理。Rust 的类型系统与所有权规则在很大程度上帮助我们正确完成这种管理。作为例子，我们来看互斥锁（mutex）——共享内存中较常见的并发原语之一。

### 用互斥锁控制访问

　　**Mutex** 是 **mutual exclusion**（互斥）的缩写，意思是互斥锁在任意给定时刻只允许一个线程访问某些数据。要访问互斥锁中的数据，线程必须先通过请求获取互斥锁的锁（lock）来表示想访问。**锁**是互斥锁的一部分数据结构，用于跟踪当前谁拥有对数据的独占访问。因此，人们说互斥锁通过锁定系统**守护**它所持有的数据。

　　互斥锁以难以使用著称，因为你必须记住两条规则：

1. 使用数据之前必须尝试获取锁。
2. 用完互斥锁所守护的数据后，必须解锁数据，以便其他线程能获取锁。

　　用现实世界比喻互斥锁：想象会议上只有一支麦克风的小组讨论。小组成员发言前，必须请求或示意想使用麦克风。拿到麦克风后，他们想说多久就说多久，然后把麦克风交给下一位请求发言的成员。若有人说完却忘记交出麦克风，其他人就无法发言。若对共享麦克风的管理出了问题，小组讨论就不会按计划进行！

　　把互斥锁管理对极其棘手，这也是许多人热衷于通道的原因。然而，得益于 Rust 的类型系统与所有权规则，你不会把加锁与解锁搞错。

#### `Mutex<T>` 的 API

　　作为如何使用互斥锁的例子，我们先在单线程上下文中使用互斥锁，如示例 16-12 所示。

**文件名：`src/main.rs`**

```rust
use std::sync::Mutex;

fn main() {
    let m = Mutex::new(5);

    {
        let mut num = m.lock().unwrap();
        *num = 6;
    }

    println!("m = {m:?}");
}
```

**示例 16-12**


　　与许多类型一样，我们用关联函数 `new` 创建 `Mutex<T>`。要访问互斥锁内部的数据，使用 `lock` 方法获取锁。这次调用会阻塞当前线程，使它在轮到我们持有锁之前无法做任何工作。

　　若另一持有锁的线程 panic 了，对 `lock` 的调用会失败。那种情况下永远不会再有人能拿到锁，因此我们选择 `unwrap`，若处于那种情形就让本线程 panic。

　　获取锁之后，可以把返回值（本例中名为 `num`）当作指向内部数据的可变引用。类型系统确保我们在使用 `m` 中的值之前先获取锁。`m` 的类型是 `Mutex<i32>` 而不是 `i32`，因此**必须**调用 `lock` 才能使用其中的 `i32` 值。我们忘不了；否则类型系统就不让我们访问内部的 `i32`。

　　对 `lock` 的调用返回名为 `MutexGuard` 的类型，包在我们用 `unwrap` 处理过的 `LockResult` 里。`MutexGuard` 类型实现了 `Deref` 以指向内部数据；该类型还实现了 `Drop`，在 `MutexGuard` 离开作用域时（发生在内部作用域结束时）自动释放锁。因此，我们不会冒忘记释放锁、从而阻塞互斥锁被其他线程使用的风险，因为锁的释放是自动发生的。

　　丢弃锁之后，我们可以打印互斥锁的值，并看到已成功把内部的 `i32` 改为 `6`。

#### 在多个线程间共享访问 `Mutex<T>` {#sharing-a-mutext-between-multiple-threads}

　　现在尝试用 `Mutex<T>` 在多个线程之间共享一个值。我们将启动 10 个线程，让它们各自把计数器加 1，使计数器从 0 增到 10。示例 16-13 会有编译错误，我们将利用该错误进一步了解如何使用 `Mutex<T>`，以及 Rust 如何帮助我们正确使用它。

**文件名：`src/main.rs`**

```rust
use std::sync::Mutex;
use std::thread;

fn main() {
    let counter = Mutex::new(0);
    let mut handles = vec![];

    for _ in 0..10 {
        let handle = thread::spawn(move || {
            let mut num = counter.lock().unwrap();

            *num += 1;
        });
        handles.push(handle);
    }

    for handle in handles {
        handle.join().unwrap();
    }

    println!("Result: {}", *counter.lock().unwrap());
}
```

**示例 16-13**


　　我们创建变量 `counter`，在 `Mutex<T>` 中保存一个 `i32`，与示例 16-12 相同。接下来通过遍历一个数字范围创建 10 个线程。我们使用 `thread::spawn`，并给所有线程同一个闭包：把计数器移入线程，通过对 `Mutex<T>` 调用 `lock` 获取锁，然后给互斥锁中的值加 1。线程运行完其闭包后，`num` 会离开作用域并释放锁，以便另一线程获取它。

　　在主线程中，我们收集所有 join 句柄。然后像示例 16-2 那样，对每个句柄调用 `join`，确保所有线程结束。那时主线程会获取锁并打印本程序的结果。

　　我们提示过这个例子无法编译。现在来看看为什么！

```console
$ cargo run
   Compiling shared-state v0.1.0 (file:///projects/shared-state)
error[E0382]: borrow of moved value: `counter`
  --> src/main.rs:21:29
   |
 5 |     let counter = Mutex::new(0);
   |         ------- move occurs because `counter` has type `std::sync::Mutex<i32>`, which does not implement the `Copy` trait
...
 8 |     for _ in 0..10 {
   |     -------------- inside of this loop
 9 |         let handle = thread::spawn(move || {
   |                                    ------- value moved into closure here, in previous iteration of loop
...
21 |     println!("Result: {}", *counter.lock().unwrap());
   |                             ^^^^^^^ value borrowed here after move

For more information about this error, try `rustc --explain E0382`.
error: could not compile `shared-state` (bin "shared-state") due to 1 previous error
```

　　错误信息指出 `counter` 值在循环的前一次迭代中已被移动。Rust 告诉我们：不能把锁住的 `counter` 的所有权移入多个线程。我们用第 15 章讨论过的多重所有权方法来修复这个编译错误。

#### 多线程下的多重所有权

　　第 15 章中，我们用智能指针 `Rc<T>` 创建引用计数值，从而把一个值交给多个所有者。这里做同样的事，看看会发生什么。在示例 16-14 中把 `Mutex<T>` 包在 `Rc<T>` 里，并在把所有权移给线程之前克隆该 `Rc<T>`。

**文件名：`src/main.rs`**

```rust
use std::rc::Rc;
use std::sync::Mutex;
use std::thread;

fn main() {
    let counter = Rc::new(Mutex::new(0));
    let mut handles = vec![];

    for _ in 0..10 {
        let counter = Rc::clone(&counter);
        let handle = thread::spawn(move || {
            let mut num = counter.lock().unwrap();

            *num += 1;
        });
        handles.push(handle);
    }

    for handle in handles {
        handle.join().unwrap();
    }

    println!("Result: {}", *counter.lock().unwrap());
}
```

**示例 16-14**


　　再次编译，得到……不同的错误！编译器教会了我们很多：

```console
$ cargo run
   Compiling shared-state v0.1.0 (file:///projects/shared-state)
error[E0277]: `Rc<std::sync::Mutex<i32>>` cannot be sent between threads safely
  --> src/main.rs:11:36
   |
11 |           let handle = thread::spawn(move || {
   |                        ------------- ^------
   |                        |             |
   |  ______________________|_____________within this `{closure@src/main.rs:11:36: 11:43}`
   | |                      |
   | |                      required by a bound introduced by this call
12 | |             let mut num = counter.lock().unwrap();
13 | |
14 | |             *num += 1;
15 | |         });
   | |_________^ `Rc<std::sync::Mutex<i32>>` cannot be sent between threads safely
   |
   = help: within `{closure@src/main.rs:11:36: 11:43}`, the trait `Send` is not implemented for `Rc<std::sync::Mutex<i32>>`
note: required because it's used within this closure
  --> src/main.rs:11:36
   |
11 |         let handle = thread::spawn(move || {
   |                                    ^^^^^^^
note: required by a bound in `spawn`
  --> /rustc/2d8144b7880597b6e6d3dfd63a9a9efae3f533d3/library/std/src/thread/functions.rs:125:0

For more information about this error, try `rustc --explain E0277`.
error: could not compile `shared-state` (bin "shared-state") due to 1 previous error
```

　　哇，错误信息很长！需要关注的重要部分是：`` `Rc<Mutex<i32>>` cannot be sent between threads safely ``。编译器还告诉我们原因：`` the trait `Send` is not implemented for `Rc<Mutex<i32>>` ``。下一节会讨论 `Send`：它是确保我们与线程一起使用的类型适合并发情形的特征之一。

　　遗憾的是，`Rc<T>` 不能安全地跨线程共享。当 `Rc<T>` 管理引用计数时，每次调用 `clone` 就加计数，每个克隆被丢弃时就减计数。但它不使用任何并发原语来确保对计数的修改不会被另一线程打断。这可能导致错误的计数——隐蔽的 bug，进而可能导致内存泄漏，或在我们用完之前就丢弃了值。我们需要的是与 `Rc<T>` 完全类似、但以线程安全方式修改引用计数的类型。

#### 用 `Arc<T>` 做原子引用计数

　　幸运的是，`Arc<T>` **就是**那种可在并发情形下安全使用的类似 `Rc<T>` 的类型。字母 *a* 代表 *atomic*，意思是**原子引用计数**（atomically reference-counted）类型。原子操作是我们在此不详细介绍的另一类并发原语：更多细节见标准库文档 [`std::sync::atomic`][atomic]。此刻你只需知道：原子类型的行为类似原始类型，但可以安全地跨线程共享。

　　你可能想问：为何并非所有原始类型都是原子的，为何标准库类型默认不实现为使用 `Arc<T>`。原因是线程安全带有性能代价，你只想在真正需要时付出。若只在单线程内对值做操作，不必强制执行原子类型所提供的保证，代码可以跑得更快。

　　回到我们的例子：`Arc<T>` 与 `Rc<T>` 有相同的 API，因此我们通过修改 `use` 行、对 `new` 的调用以及对 `clone` 的调用来修复程序。示例 16-15 的代码终于可以编译并运行。

**文件名：`src/main.rs`**

```rust
use std::sync::{Arc, Mutex};
use std::thread;

fn main() {
    let counter = Arc::new(Mutex::new(0));
    let mut handles = vec![];

    for _ in 0..10 {
        let counter = Arc::clone(&counter);
        let handle = thread::spawn(move || {
            let mut num = counter.lock().unwrap();

            *num += 1;
        });
        handles.push(handle);
    }

    for handle in handles {
        handle.join().unwrap();
    }

    println!("Result: {}", *counter.lock().unwrap());
}
```

**示例 16-15**


　　这段代码会打印：


```text
Result: 10
```

　　成功了！我们从 0 数到了 10，这看起来或许并不惊人，但确实教给了我们许多关于 `Mutex<T>` 与线程安全的知识。你也可以用这个程序的结构做比给计数器加一更复杂的操作。用这种策略，可以把计算分成独立部分，把这些部分分到各线程上，再用 `Mutex<T>` 让每个线程用自己的那部分更新最终结果。

　　注意：若只是做简单数值运算，[`std::sync::atomic` 模块][atomic]提供了比 `Mutex<T>` 更简单的类型。这些类型提供对原始类型的安全、并发、原子访问。本例选择对原始类型使用 `Mutex<T>`，是为了把注意力集中在 `Mutex<T>` 如何工作上。

### 比较 `RefCell<T>`/`Rc<T>` 与 `Mutex<T>`/`Arc<T>`

　　你可能注意到 `counter` 是不可变的，但我们仍能得到指向其内部值的可变引用；这意味着 `Mutex<T>` 提供了内部可变性，正如 `Cell` 家族那样。正如第 15 章用 `RefCell<T>` 允许我们修改 `Rc<T>` 内部的内容，我们用 `Mutex<T>` 修改 `Arc<T>` 内部的内容。

　　另一点需要注意：使用 `Mutex<T>` 时，Rust 无法保护你免受所有种类的逻辑错误。回想第 15 章：使用 `Rc<T>` 有创建引用循环的风险——两个 `Rc<T>` 值彼此引用会导致内存泄漏。类似地，`Mutex<T>` 有造成**死锁**的风险。当某操作需要锁定两种资源，而两个线程各自已获取其中一把锁、从而永远彼此等待时，就会发生死锁。若对死锁感兴趣，可尝试编写一个有死锁的 Rust 程序；然后研究任意语言中针对互斥锁的死锁缓解策略，并试着在 Rust 中实现它们。标准库中 `Mutex<T>` 与 `MutexGuard` 的 API 文档提供了有用信息。

　　我们将以讨论 `Send` 与 `Sync` 特征、以及如何把它们用于自定义类型来收尾本章。

[atomic]: https://doc.rust-lang.org/std/sync/atomic/index.html
