+++
title = "17.6 Future、任务与线程"
date = 2026-08-05T08:44:00+08:00
weight = 85
type = "docs"
description = "综合比较 Future、任务与线程，说明何时选用以及如何组合"
isCJKLanguage = true
draft = false
rust_version = "1.97.1"

+++

> 译文 · 基于 [The Rust Programming Language](https://doc.rust-lang.org/stable/book/)（rustc 1.97.1）

# Future、任务与线程 {#future}


> 原文链接: [https://doc.rust-lang.org/stable/book/ch17-06-futures-tasks-threads.html](https://doc.rust-lang.org/stable/book/ch17-06-futures-tasks-threads.html)


## 综合起来：Future、任务与线程

　　正如我们在[第 16 章][ch16]所见，线程是实现并发的一种途径。本章又看到了另一种：用 async 配合 Future 与 Stream。若你在想何时该选哪一种，答案是：视情况而定！而且在许多情况下，选择并不是线程*或* async，而是线程*与* async。

　　几十年来，许多操作系统都提供了基于线程的并发模型，许多编程语言也因此予以支持。但这些模型并非没有取舍。在许多操作系统上，每个线程都会占用不少内存。而且只有在操作系统与硬件支持时，线程才是可行选项。与主流桌面和移动电脑不同，有些嵌入式系统根本没有操作系统，因而也没有线程。

　　异步模型提供了另一套——最终是互补的——取舍。在异步模型中，并发操作不必各自拥有线程。相反，它们可以运行在任务（task）上，正如我们在流一节中用 `trpl::spawn_task` 从同步函数启动工作时那样。任务类似线程，但不是由操作系统管理，而是由库级代码——运行时——管理。

　　派生线程与派生任务的 API 如此相似，是有原因的。线程是一组同步操作的边界；并发发生在线程*之间*。任务是一组*异步*操作的边界；并发既可以发生在任务*之间*，也可以发生在任务*内部*，因为任务可以在其体内的 Future 之间切换。最后，Future 是 Rust 最细粒度的并发单位，每个 Future 都可能代表由其他 Future 组成的树。运行时——具体说是它的执行器（executor）——管理任务，任务再管理 Future。就此而言，任务类似由运行时管理的轻量级线程，并因由运行时而非操作系统管理而具备额外能力。

　　这并不意味着异步任务总是优于线程（或反过来）。用线程做并发，在某些方面比用 `async` 做并发的编程模型更简单。这既可以是优点也可以是缺点。线程有几分“点火即忘”：它们没有与 Future 对等的原生概念，因此除非被操作系统本身打断，否则会一直跑到完成。

　　而且事实证明，线程与任务常常配合得很好，因为任务（至少在某些运行时中）可以在线程之间迁移。实际上，我们一直在用的运行时——包括 `spawn_blocking` 与 `spawn_task` 函数——默认就是多线程的！许多运行时采用称为*工作窃取*（work stealing）的做法，根据各线程当前的利用率，透明地在线程之间迁移任务，以提升系统整体性能。那种做法实际上同时需要线程*与*任务，因而也需要 Future。

　　在考虑何时用哪种方法时，可以参考这些经验法则：

- 若工作*高度可并行*（也就是 CPU 密集型），例如处理一大批可分开处理的数据，线程往往更好。
- 若工作*高度并发*（也就是 I/O 密集型），例如处理来自许多不同来源、可能以不同间隔或速率到达的消息，async 往往更好。

　　若你同时需要并行与并发，不必在线程与 async 之间二选一。你可以自由地一起使用它们，让各自发挥所长。例如，示例 17-25 展示了现实世界 Rust 代码中相当常见的一种混合。

**文件名：`src/main.rs`**
```rust
use std::{thread, time::Duration};

fn main() {
    let (tx, mut rx) = trpl::channel();

    thread::spawn(move || {
        for i in 1..11 {
            tx.send(i).unwrap();
            thread::sleep(Duration::from_secs(1));
        }
    });

    trpl::block_on(async {
        while let Some(message) = rx.recv().await {
            println!("{message}");
        }
    });
}
```

**示例 17-25：在线程中用阻塞代码发送消息，并在异步块中等待这些消息**

　　我们先创建异步通道，再派生一个线程，用 `move` 关键字取得通道发送端的所有权。在线程内发送数字 1 到 10，每次间隔睡眠一秒。最后，像本章通篇那样，把一个异步块创建的 Future 传给 `trpl::block_on` 运行。在该 Future 中，我们等待这些消息，就像此前其他消息传递例子一样。

　　回到本章开头的场景：想象用专用线程跑一组视频编码任务（因为视频编码是计算密集型的），但通过异步通道通知 UI 这些操作已完成。现实用例中，这类组合数不胜数。

## 小结

　　这不是本书中你最后一次见到并发。[第 21 章][ch21]的项目会在比这里更贴近现实的情境中应用这些概念，并更直接地比较用线程与用任务和 Future 来解题。

　　无论选择哪种途径，Rust 都提供了编写安全、快速、并发代码所需的工具——无论是面向高吞吐 Web 服务器，还是嵌入式操作系统。

　　接下来，我们将讨论在 Rust 程序变大时，如何用惯用方式建模问题并组织解法。此外，我们也会讨论 Rust 的惯用法与你可能从面向对象编程中熟悉的那些惯用法之间的关系。

[ch16]: ../../concurrency/
[combining-futures]: ../03-more-futures/#building-our-own-async-abstractions
[streams]: ../04-streams/#composing-streams
[ch21]: ../../final-project/
