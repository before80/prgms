+++
title = "16.1 用线程同时运行代码"
date = 2026-08-05T08:44:00+08:00
weight = 75
type = "docs"
description = "用 thread::spawn 创建线程，并用 join 与 move 闭包管理它们"
isCJKLanguage = true
draft = false
rust_version = "1.97.1"

+++

> 译文 · 基于 [The Rust Programming Language](https://doc.rust-lang.org/stable/book/)（rustc 1.97.1）

# 用线程同时运行代码


> 原文链接: [https://doc.rust-lang.org/stable/book/ch16-01-threads.html](https://doc.rust-lang.org/stable/book/ch16-01-threads.html)


## 用线程同时运行代码

　　在多数现代操作系统中，已执行程序的代码运行在一个**进程**（process）中，操作系统会同时管理多个进程。在一个程序内部，也可以有同时运行的独立部分。运行这些独立部分的功能称为**线程**（thread）。例如，Web 服务器可以有多个线程，以便同时响应不止一个请求。

　　把程序中的计算拆到多个线程上同时执行多项任务，可以提升性能，但也会增加复杂性。因为线程可以同时运行，不同线程上各段代码的运行顺序没有固有保证。这可能导致问题，例如：

- 竞态条件（race condition）：线程以不一致的顺序访问数据或资源
- 死锁（deadlock）：两个线程彼此等待，导致两者都无法继续
- 只在特定情形下出现、难以可靠复现与修复的 bug

　　Rust 试图减轻使用线程的负面影响，但在多线程上下文中编程仍需仔细思考，并要求与单线程程序不同的代码结构。

　　编程语言以几种不同方式实现线程，许多操作系统也提供可供语言调用以创建新线程的 API。Rust 标准库采用 **1:1** 的线程实现模型，即程序中每个语言线程对应一个操作系统线程。也有 crate 实现其他线程模型，与 1:1 模型做出不同权衡。（下一章会看到的 Rust 异步系统，也提供了另一种并发途径。）

### 用 `spawn` 创建新线程 {#creating-a-new-thread-with-spawn}

　　要创建新线程，我们调用 `thread::spawn` 函数，并传入一个闭包（第 13 章讨论过闭包），其中包含想在新线程中运行的代码。示例 16-1 从主线程打印一些文本，从新线程打印另一些文本。

**文件名：`src/main.rs`**
```rust
use std::thread;
use std::time::Duration;

fn main() {
    thread::spawn(|| {
        for i in 1..10 {
            println!("hi number {i} from the spawned thread!");
            thread::sleep(Duration::from_millis(1));
        }
    });

    for i in 1..5 {
        println!("hi number {i} from the main thread!");
        thread::sleep(Duration::from_millis(1));
    }
}
```

**示例 16-1：创建新线程打印一件事，同时主线程打印另一件事**

　　注意：当 Rust 程序的主线程结束时，所有已派生的线程都会被关闭，无论它们是否已运行完毕。该程序的输出每次可能略有不同，但大致会类似如下：


```text
hi number 1 from the main thread!
hi number 1 from the spawned thread!
hi number 2 from the main thread!
hi number 2 from the spawned thread!
hi number 3 from the main thread!
hi number 3 from the spawned thread!
hi number 4 from the main thread!
hi number 4 from the spawned thread!
hi number 5 from the spawned thread!
```

　　对 `thread::sleep` 的调用会强制线程短暂停止执行，从而允许另一个线程运行。线程很可能会轮流执行，但这并无保证：取决于操作系统如何调度线程。在这次运行中，尽管派生线程的打印语句在代码中出现在前，主线程却先打印了。而且尽管我们让派生线程打印直到 `i` 为 `9`，主线程关闭前它只打印到了 `5`。

　　若运行这段代码只看到主线程的输出，或看不到任何交错，可尝试增大范围中的数字，给操作系统更多在线程间切换的机会。

### 等待所有线程结束 {#waiting-for-all-threads-to-finish}

　　示例 16-1 的代码不仅多数时候会因主线程结束而过早停止派生线程，而且由于线程运行顺序没有保证，我们甚至无法保证派生线程一定能运行！

　　把 `thread::spawn` 的返回值保存在变量中，可以修复派生线程未运行或过早结束的问题。`thread::spawn` 的返回类型是 `JoinHandle<T>`。`JoinHandle<T>` 是一个被拥有的值：对其调用 `join` 方法时，会等待其线程结束。示例 16-2 展示如何使用示例 16-1 中所创建线程的 `JoinHandle<T>`，以及如何调用 `join`，确保派生线程在 `main` 退出前完成。

**文件名：`src/main.rs`**

```rust
use std::thread;
use std::time::Duration;

fn main() {
    let handle = thread::spawn(|| {
        for i in 1..10 {
            println!("hi number {i} from the spawned thread!");
            thread::sleep(Duration::from_millis(1));
        }
    });

    for i in 1..5 {
        println!("hi number {i} from the main thread!");
        thread::sleep(Duration::from_millis(1));
    }

    handle.join().unwrap();
}
```

**示例 16-2**


　　对句柄调用 `join` 会阻塞当前正在运行的线程，直到句柄所代表的线程终止。**阻塞**（blocking）线程意味着阻止该线程执行工作或退出。因为我们把对 `join` 的调用放在主线程的 `for` 循环之后，运行示例 16-2 应产生类似如下的输出：


```text
hi number 1 from the main thread!
hi number 2 from the main thread!
hi number 1 from the spawned thread!
hi number 3 from the main thread!
hi number 2 from the spawned thread!
hi number 4 from the main thread!
hi number 3 from the spawned thread!
hi number 4 from the spawned thread!
hi number 5 from the spawned thread!
hi number 6 from the spawned thread!
hi number 7 from the spawned thread!
hi number 8 from the spawned thread!
hi number 9 from the spawned thread!
```

　　两个线程继续交替，但主线程因调用了 `handle.join()` 而等待，直到派生线程结束后才结束。

　　但若把 `handle.join()` 移到 `main` 中的 `for` 循环之前，会发生什么呢？像这样：

**文件名：`src/main.rs`**
```rust
use std::thread;
use std::time::Duration;

fn main() {
    let handle = thread::spawn(|| {
        for i in 1..10 {
            println!("hi number {i} from the spawned thread!");
            thread::sleep(Duration::from_millis(1));
        }
    });

    handle.join().unwrap();

    for i in 1..5 {
        println!("hi number {i} from the main thread!");
        thread::sleep(Duration::from_millis(1));
    }
}
```

　　主线程会等待派生线程结束，然后再运行自己的 `for` 循环，因此输出不再交错，如下所示：


```text
hi number 1 from the spawned thread!
hi number 2 from the spawned thread!
hi number 3 from the spawned thread!
hi number 4 from the spawned thread!
hi number 5 from the spawned thread!
hi number 6 from the spawned thread!
hi number 7 from the spawned thread!
hi number 8 from the spawned thread!
hi number 9 from the spawned thread!
hi number 1 from the main thread!
hi number 2 from the main thread!
hi number 3 from the main thread!
hi number 4 from the main thread!
```

　　诸如在何处调用 `join` 这类小细节，会影响线程是否同时运行。

### 在线程中使用 `move` 闭包 {#using-move-closures-with-threads}

　　传给 `thread::spawn` 的闭包常会使用 `move` 关键字，因为这样闭包就会取得它从环境中使用的值的所有权，从而把这些值的所有权从一个线程转移到另一个线程。第 13 章[「捕获引用或转移所有权」](/trpl/functional-features/01-closures/#capturing-references-or-moving-ownership)在闭包语境中讨论过 `move`。现在我们更关注 `move` 与 `thread::spawn` 的互动。

　　注意示例 16-1 中传给 `thread::spawn` 的闭包不接受任何参数：我们没有在派生线程的代码中使用主线程的任何数据。要在派生线程中使用主线程的数据，派生线程的闭包必须捕获它需要的值。示例 16-3 展示了在主线程中创建向量并在派生线程中使用它的尝试。不过这还行不通，稍后你会看到。

**文件名：`src/main.rs`**
```rust
use std::thread;

fn main() {
    let v = vec![1, 2, 3];

    let handle = thread::spawn(|| {
        println!("Here's a vector: {v:?}");
    });

    handle.join().unwrap();
}
```

**示例 16-3：尝试在另一个线程中使用主线程创建的向量**

　　闭包使用了 `v`，因此会捕获 `v` 并使之成为闭包环境的一部分。因为 `thread::spawn` 在新线程中运行这个闭包，我们应能在那个新线程中访问 `v`。但编译这个例子时，会得到如下错误：

```console
$ cargo run
   Compiling threads v0.1.0 (file:///projects/threads)
error[E0373]: closure may outlive the current function, but it borrows `v`, which is owned by the current function
 --> src/main.rs:6:32
  |
6 |     let handle = thread::spawn(|| {
  |                                ^^ may outlive borrowed value `v`
7 |         println!("Here's a vector: {v:?}");
  |                                     - `v` is borrowed here
  |
note: function requires argument type to outlive `'static`
 --> src/main.rs:6:18
  |
6 |       let handle = thread::spawn(|| {
  |  __________________^
7 | |         println!("Here's a vector: {v:?}");
8 | |     });
  | |______^
help: to force the closure to take ownership of `v` (and any other referenced variables), use the `move` keyword
  |
6 |     let handle = thread::spawn(move || {
  |                                ++++

For more information about this error, try `rustc --explain E0373`.
error: could not compile `threads` (bin "threads") due to 1 previous error
```

　　Rust **推断**如何捕获 `v`；因为 `println!` 只需要 `v` 的引用，闭包就尝试借用 `v`。然而有个问题：Rust 无法知道派生线程会运行多久，因此不知道对 `v` 的引用是否始终有效。

　　示例 16-4 给出了更可能出现“对 `v` 的引用无效”的场景。

**文件名：`src/main.rs`**
```rust
use std::thread;

fn main() {
    let v = vec![1, 2, 3];

    let handle = thread::spawn(|| {
        println!("Here's a vector: {v:?}");
    });

    drop(v); // oh no!

    handle.join().unwrap();
}
```

**示例 16-4：线程中的闭包试图捕获对 `v` 的引用，而主线程会丢弃 `v`**

　　若 Rust 允许我们运行这段代码，派生线程有可能立刻被放进后台而根本不运行。派生线程内部有对 `v` 的引用，但主线程立刻用第 15 章讨论过的 `drop` 函数丢弃了 `v`。然后当派生线程开始执行时，`v` 已不再有效，对它的引用也无效。糟糕！

　　要修复示例 16-3 中的编译错误，可以采纳错误信息的建议：


```text
help: to force the closure to take ownership of `v` (and any other referenced variables), use the `move` keyword
  |
6 |     let handle = thread::spawn(move || {
  |                                ++++
```

　　在闭包前加上 `move` 关键字，会强制闭包取得它正在使用的值的所有权，而不是让 Rust 推断应借用这些值。示例 16-5 对示例 16-3 的修改会按我们的意图编译并运行。

**文件名：`src/main.rs`**
```rust
use std::thread;

fn main() {
    let v = vec![1, 2, 3];

    let handle = thread::spawn(move || {
        println!("Here's a vector: {v:?}");
    });

    handle.join().unwrap();
}
```

**示例 16-5：使用 `move` 关键字强制闭包取得所用值的所有权**

　　我们可能想用同样办法、通过 `move` 闭包修复示例 16-4 中主线程调用 `drop` 的代码。然而这一修复行不通，因为示例 16-4 试图做的事因另一原因而不被允许。若给闭包加上 `move`，就会把 `v` 移入闭包的环境，主线程中就再也无法对它调用 `drop`。我们反而会得到这样的编译错误：

```console
$ cargo run
   Compiling threads v0.1.0 (file:///projects/threads)
error[E0382]: use of moved value: `v`
  --> src/main.rs:10:10
   |
 4 |     let v = vec![1, 2, 3];
   |         - move occurs because `v` has type `Vec<i32>`, which does not implement the `Copy` trait
 5 |
 6 |     let handle = thread::spawn(move || {
   |                                ------- value moved into closure here
 7 |         println!("Here's a vector: {v:?}");
   |                                     - variable moved due to use in closure
...
10 |     drop(v); // oh no!
   |          ^ value used here after move
   |
help: consider cloning the value before moving it into the closure
   |
 6 ~     let value = v.clone();
 7 ~     let handle = thread::spawn(move || {
 8 ~         println!("Here's a vector: {value:?}");
   |

For more information about this error, try `rustc --explain E0382`.
error: could not compile `threads` (bin "threads") due to 1 previous error
```

　　Rust 的所有权规则再次救了我们！示例 16-3 的代码报错，是因为 Rust 保守地只为线程借用 `v`，这意味着主线程理论上可能使派生线程的引用失效。通过告诉 Rust 把 `v` 的所有权移给派生线程，我们向 Rust 保证主线程不会再使用 `v`。若以同样方式改示例 16-4，则在主线程中再使用 `v` 就会违反所有权规则。`move` 关键字覆盖了 Rust“默认借用”的保守行为；它并不允许我们违反所有权规则。

　　既然已经介绍了什么是线程，以及线程 API 提供的方法，下面看看一些可以使用线程的情形。

[capture]: /trpl/functional-features/01-closures/#capturing-references-or-moving-ownership
