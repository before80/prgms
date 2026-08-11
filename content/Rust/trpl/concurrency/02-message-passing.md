+++
title = "16.2 用消息传递在线程间传送数据"
date = 2026-08-05T08:44:00+08:00
weight = 76
type = "docs"
description = "用通道在线程间安全地传递消息与所有权"
isCJKLanguage = true
draft = false
rust_version = "1.97.1"

+++

> 译文 · 基于 [The Rust Programming Language](https://doc.rust-lang.org/stable/book/)（rustc 1.97.1）

# 用消息传递在线程间传送数据


> 原文链接: [https://doc.rust-lang.org/stable/book/ch16-02-message-passing.html](https://doc.rust-lang.org/stable/book/ch16-02-message-passing.html)


## 用消息传递在线程间传送数据

　　确保安全并发的一种日益流行的方法是消息传递：线程或 actor 通过彼此发送包含数据的消息来通信。[Go 语言文档](https://golang.org/doc/effective_go.html#concurrency)中有一句口号概括了这一想法：“不要通过共享内存来通信；相反，通过通信来共享内存。”

　　为实现消息发送式并发，Rust 标准库提供了通道（channel）的实现。**通道**是一种通用编程概念，用于把数据从一个线程发送到另一个线程。

　　可以把编程中的通道想象成有方向的水道，例如溪流或河流。若把橡皮鸭之类的东西放进河里，它会顺流而下到达水道尽头。

　　通道有两端：发送端（transmitter）与接收端（receiver）。发送端是上游——你把橡皮鸭放进河里的地方；接收端是下游——橡皮鸭最终到达的地方。代码的一部分对发送端调用方法并传入要发送的数据，另一部分则检查接收端是否有到达的消息。若发送端或接收端任一端被丢弃，就称通道已**关闭**（closed）。

　　这里我们逐步写出一个程序：一个线程生成值并沿通道发送，另一个线程接收这些值并打印出来。我们用通道在线程间发送简单值来说明该功能。熟悉这一技巧后，就可以把通道用于任何需要彼此通信的线程，例如聊天系统，或许多线程各自完成计算的一部分、再把结果发给一个线程汇总的系统。

　　首先，在示例 16-6 中，我们创建通道但暂不使用它。注意这段代码目前还无法编译，因为 Rust 无法判断我们想通过通道发送什么类型的值。

**文件名：`src/main.rs`**
```rust
use std::sync::mpsc;

fn main() {
    let (tx, rx) = mpsc::channel();
}
```

**示例 16-6：创建通道，并把两端分别赋给 `tx` 与 `rx`**

　　我们用 `mpsc::channel` 函数创建新通道；`mpsc` 表示**多个生产者、单个消费者**（multiple producer, single consumer）。简言之，Rust 标准库实现的通道可以有多个**发送**端产生值，但只有一个**接收**端消费这些值。想象多条溪流汇入一条大河：沿任一溪流发送的东西最终都会进入同一条河。我们先从一个生产者开始，等例子能工作后再加入多个生产者。

　　`mpsc::channel` 函数返回一个元组：第一个元素是发送端——transmitter，第二个元素是接收端——receiver。许多领域传统上用缩写 `tx` 与 `rx` 分别表示 transmitter 与 receiver，因此我们也这样命名变量以标明两端。我们使用带模式的 `let` 语句解构元组；第 19 章会讨论 `let` 中的模式与解构。目前只需知道：这样用 `let` 是提取 `mpsc::channel` 返回元组各部分的便捷做法。

　　接下来把发送端移入派生线程，并让它发送一个字符串，使派生线程与主线程通信，如示例 16-7 所示。这就像在上游把橡皮鸭放进河里，或从一个线程向另一个线程发送聊天消息。

**文件名：`src/main.rs`**
```rust
use std::sync::mpsc;
use std::thread;

fn main() {
    let (tx, rx) = mpsc::channel();

    thread::spawn(move || {
        let val = String::from("hi");
        tx.send(val).unwrap();
    });
}
```

**示例 16-7：把 `tx` 移入派生线程并发送 `\**

　　我们再次用 `thread::spawn` 创建新线程，并用 `move` 把 `tx` 移入闭包，使派生线程拥有 `tx`。派生线程需要拥有发送端，才能通过通道发送消息。

　　发送端有一个 `send` 方法，接受我们想发送的值。`send` 方法返回 `Result<T, E>` 类型，因此若接收端已被丢弃、无处可发送值，发送操作会返回错误。本例中我们调用 `unwrap`，在出错时 panic。但在真实应用中应妥善处理：回到第 9 章复习恰当的错误处理策略。

　　在示例 16-8 中，我们在主线程从接收端取得值。这就像在河的尽头取出橡皮鸭，或接收一条聊天消息。

**文件名：`src/main.rs`**
```rust
use std::sync::mpsc;
use std::thread;

fn main() {
    let (tx, rx) = mpsc::channel();

    thread::spawn(move || {
        let val = String::from("hi");
        tx.send(val).unwrap();
    });

    let received = rx.recv().unwrap();
    println!("Got: {received}");
}
```

**示例 16-8：在主线程接收值 `\**

　　接收端有两个有用的方法：`recv` 与 `try_recv`。我们使用的是 `recv`（_receive_ 的缩写），它会阻塞主线程的执行，等待有值沿通道发送过来。一旦有值发送过来，`recv` 会在 `Result<T, E>` 中返回它。当发送端关闭时，`recv` 会返回错误，表示不会再有更多值到来。

　　`try_recv` 方法不会阻塞，而是立即返回 `Result<T, E>`：若有消息可用则为持有消息的 `Ok`，若这次没有消息则为 `Err`。若该线程在等待消息时还有其他工作要做，`try_recv` 就很有用：可以写一个循环，不时调用 `try_recv`，有消息就处理，否则先做一会儿其他工作再检查。

　　本例为简单起见使用了 `recv`；主线程除了等待消息外没有其他工作，因此阻塞主线程是合适的。

　　运行示例 16-8 的代码时，会看到主线程打印出该值：


```text
Got: hi
```

　　完美！

### 通过通道转移所有权

　　所有权规则在消息发送中扮演关键角色，因为它们帮助你写出安全的并发代码。在整个 Rust 程序中始终思考所有权，其优势就在于能防止并发编程中的错误。我们做一个实验，展示通道与所有权如何协作防止问题：在派生线程中把 `val` 值沿通道发送**之后**再尝试使用它。试着编译示例 16-9 的代码，看看为何不被允许。

**文件名：`src/main.rs`**
```rust
use std::sync::mpsc;
use std::thread;

fn main() {
    let (tx, rx) = mpsc::channel();

    thread::spawn(move || {
        let val = String::from("hi");
        tx.send(val).unwrap();
        println!("val is {val}");
    });

    let received = rx.recv().unwrap();
    println!("Got: {received}");
}
```

**示例 16-9：尝试在把 `val` 沿通道发送后再使用它**

　　这里我们在通过 `tx.send` 把 `val` 沿通道发送后再尝试打印它。若允许这样做会很糟糕：值一旦发送到另一个线程，那个线程可能在我们再次使用该值之前就修改或丢弃它。潜在地，另一线程的修改可能因数据不一致或不存在而导致错误或意外结果。然而，若尝试编译示例 16-9 的代码，Rust 会给出错误：

```console
$ cargo run
   Compiling message-passing v0.1.0 (file:///projects/message-passing)
error[E0382]: borrow of moved value: `val`
  --> src/main.rs:10:27
   |
 8 |         let val = String::from("hi");
   |             --- move occurs because `val` has type `String`, which does not implement the `Copy` trait
 9 |         tx.send(val).unwrap();
   |                 --- value moved here
10 |         println!("val is {val}");
   |                           ^^^ value borrowed here after move

For more information about this error, try `rustc --explain E0382`.
error: could not compile `message-passing` (bin "message-passing") due to 1 previous error
```

　　我们的并发失误造成了编译期错误。`send` 函数取得其参数的所有权，值被移动后由接收端取得所有权。这阻止我们在发送后再意外使用该值；所有权系统会检查一切是否妥当。

### 发送多个值

　　示例 16-8 的代码能编译并运行，但并未清楚表明是两个独立线程在通过通道交谈。

　　在示例 16-10 中，我们做了一些修改，以证明示例 16-8 的代码在并发运行：派生线程现在会发送多条消息，并在每条消息之间暂停一秒。

**文件名：`src/main.rs`**
```rust
use std::sync::mpsc;
use std::thread;
use std::time::Duration;

fn main() {
    let (tx, rx) = mpsc::channel();

    thread::spawn(move || {
        let vals = vec![
            String::from("hi"),
            String::from("from"),
            String::from("the"),
            String::from("thread"),
        ];

        for val in vals {
            tx.send(val).unwrap();
            thread::sleep(Duration::from_secs(1));
        }
    });

    for received in rx {
        println!("Got: {received}");
    }
}
```

**示例 16-10：发送多条消息，并在每条之间暂停**

　　这次，派生线程有一个想发给主线程的字符串向量。我们遍历它们，逐个发送，并在每次之间调用 `thread::sleep`，传入一秒的 `Duration`。

　　在主线程中，我们不再显式调用 `recv` 函数：而是把 `rx` 当作迭代器。每收到一个值就打印它。通道关闭时，迭代结束。

　　运行示例 16-10 的代码时，应看到如下输出，每行之间有一秒暂停：


```text
Got: hi
Got: from
Got: the
Got: thread
```

　　因为主线程的 `for` 循环中没有任何暂停或延迟的代码，可以看出主线程在等待从派生线程接收值。

### 创建多个生产者

　　前面提到 `mpsc` 是**多个生产者、单个消费者**的缩写。下面实际使用 `mpsc`，扩展示例 16-10 的代码，创建多个线程，都向同一个接收端发送值。做法是克隆发送端，如示例 16-11 所示。

**文件名：`src/main.rs`**
```rust
    // --snip--

    let (tx, rx) = mpsc::channel();

    let tx1 = tx.clone();
    thread::spawn(move || {
        let vals = vec![
            String::from("hi"),
            String::from("from"),
            String::from("the"),
            String::from("thread"),
        ];

        for val in vals {
            tx1.send(val).unwrap();
            thread::sleep(Duration::from_secs(1));
        }
    });

    thread::spawn(move || {
        let vals = vec![
            String::from("more"),
            String::from("messages"),
            String::from("for"),
            String::from("you"),
        ];

        for val in vals {
            tx.send(val).unwrap();
            thread::sleep(Duration::from_secs(1));
        }
    });

    for received in rx {
        println!("Got: {received}");
    }

    // --snip--
```

**示例 16-11：从多个生产者发送多条消息**

　　这次，在创建第一个派生线程之前，我们对发送端调用 `clone`。这会给我们一个可传给第一个派生线程的新发送端。我们把原来的发送端传给第二个派生线程。这样我们就有两个线程，各自向同一个接收端发送不同消息。

　　运行代码时，输出应大致如下：


```text
Got: hi
Got: more
Got: from
Got: messages
Got: for
Got: the
Got: thread
Got: you
```

　　取决于你的系统，你可能看到不同顺序的值。这正是并发既有趣又困难之处。若用不同的值在不同线程上试验 `thread::sleep`，每次运行都会更不确定，并产生不同输出。

　　既然已经看过通道如何工作，下面看看另一种并发方法。
