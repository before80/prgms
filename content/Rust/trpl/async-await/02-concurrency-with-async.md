+++
title = "17.2 用 async 实现并发"
date = 2026-08-05T08:44:00+08:00
weight = 81
type = "docs"
description = "用 async 任务、join 与消息传递解决与线程类似的并发问题"
isCJKLanguage = true
draft = false
rust_version = "1.97.1"

+++

> 译文 · 基于 [The Rust Programming Language](https://doc.rust-lang.org/stable/book/)（rustc 1.97.1）

# 用 async 实现并发 {#async}


> 原文链接: [https://doc.rust-lang.org/stable/book/ch17-02-concurrency-with-async.html](https://doc.rust-lang.org/stable/book/ch17-02-concurrency-with-async.html)


## 用 Async 应用并发

　　本节我们将把 async 应用到第 16 章用线程解决过的一些同类并发挑战上。因为那里已经谈过许多关键思想，本节将聚焦线程与 Future 之间的差异。

　　许多情况下，用 async 做并发的 API 与用线程的 API 非常相似。另一些情况下则相当不同。即便线程与 async 的 API *看起来*相似，它们的行为也常常不同——而且几乎总是有不同的性能特征。

### 用 `spawn_task` 创建新任务

　　我们在第 16 章[「用 `spawn` 创建新线程」][thread-spawn]一节中处理的第一个操作，是在两个独立线程上计数。现在用 async 做同样的事。`trpl` crate 提供了看起来与 `thread::spawn` API 非常相似的 `spawn_task` 函数，以及作为 `thread::sleep` API 异步版本的 `sleep` 函数。我们可以把它们合在一起实现计数例子，如示例 17-6 所示。

**文件名：`src/main.rs`**
```rust
use std::time::Duration;

fn main() {
    trpl::block_on(async {
        trpl::spawn_task(async {
            for i in 1..10 {
                println!("hi number {i} from the first task!");
                trpl::sleep(Duration::from_millis(500)).await;
            }
        });

        for i in 1..5 {
            println!("hi number {i} from the second task!");
            trpl::sleep(Duration::from_millis(500)).await;
        }
    });
}
```

**示例 17-6：创建新任务打印一件事，同时主任务打印另一件事**

　　作为起点，我们用 `trpl::block_on` 设置 `main` 函数，以便顶层函数可以是异步的。

> 注意：从本章此处起，每个例子都会在 `main` 中包含与这完全相同的用 `trpl::block_on` 包装的代码，因此我们常常会像省略 `main` 一样省略它。记住在你的代码里要包含它！

　　然后我们在该块内写两个循环，各自包含一次 `trpl::sleep` 调用，等待半秒（500 毫秒）再发送下一条消息。我们把一个循环放在 `trpl::spawn_task` 的函数体里，另一个放在顶层 `for` 循环里。我们也在 `sleep` 调用之后加上 `await`。

　　这段代码的行为与基于线程的实现类似——包括你在自己终端运行时可能看到消息以不同顺序出现：


```text
hi number 1 from the second task!
hi number 1 from the first task!
hi number 2 from the first task!
hi number 2 from the second task!
hi number 3 from the first task!
hi number 3 from the second task!
hi number 4 from the first task!
hi number 4 from the second task!
hi number 5 from the first task!
```

　　这个版本在主异步块体内的 `for` 循环一结束就停止，因为由 `spawn_task` 派生的任务会在 `main` 函数结束时被关闭。若希望它一直跑到任务完成，就需要用 join 句柄等待第一个任务完成。对线程，我们用 `join` 方法“阻塞”直到线程运行完毕。在示例 17-7 中，我们可以用 `await` 做同样的事，因为任务句柄本身就是一个 Future。其 `Output` 类型是 `Result`，因此在等待之后还要对其解包。

**文件名：`src/main.rs`**
```rust
        let handle = trpl::spawn_task(async {
            for i in 1..10 {
                println!("hi number {i} from the first task!");
                trpl::sleep(Duration::from_millis(500)).await;
            }
        });

        for i in 1..5 {
            println!("hi number {i} from the second task!");
            trpl::sleep(Duration::from_millis(500)).await;
        }

        handle.await.unwrap();
```

**示例 17-7：对 join 句柄使用 `await` 以把任务跑到完成**

　　这个更新版会一直运行到*两个*循环都结束：


```text
hi number 1 from the second task!
hi number 1 from the first task!
hi number 2 from the first task!
hi number 2 from the second task!
hi number 3 from the first task!
hi number 3 from the second task!
hi number 4 from the first task!
hi number 4 from the second task!
hi number 5 from the first task!
hi number 6 from the first task!
hi number 7 from the first task!
hi number 8 from the first task!
hi number 9 from the first task!
```

　　到目前为止，看起来 async 与线程给出了相似的结果，只是语法不同：用 `await` 代替对 join 句柄调用 `join`，以及对 `sleep` 调用进行等待。

　　更大的差异在于：我们不必为此再派生另一个操作系统线程。实际上，这里甚至不必派生任务。因为异步块会编译成匿名 Future，我们可以把每个循环放进一个异步块，再用 `trpl::join` 函数让运行时把两者都跑到完成。

　　在第 16 章[「等待所有线程结束」][join-handles]一节中，我们展示了如何对调用 `std::thread::spawn` 时返回的 `JoinHandle` 类型使用 `join` 方法。`trpl::join` 函数类似，但面向 Future。当你给它两个 Future 时，它会产生一个新的 Future，其输出是一个元组，包含你传入的每个 Future 在*两者都*完成后各自的输出。因此在示例 17-8 中，我们用 `trpl::join` 等待 `fut1` 与 `fut2` 都结束。我们*不*等待 `fut1` 与 `fut2`，而是等待 `trpl::join` 产生的新 Future。我们忽略输出，因为它只是包含两个单元值的元组。

**文件名：`src/main.rs`**
```rust
        let fut1 = async {
            for i in 1..10 {
                println!("hi number {i} from the first task!");
                trpl::sleep(Duration::from_millis(500)).await;
            }
        };

        let fut2 = async {
            for i in 1..5 {
                println!("hi number {i} from the second task!");
                trpl::sleep(Duration::from_millis(500)).await;
            }
        };

        trpl::join(fut1, fut2).await;
```

**示例 17-8：用 `trpl::join` 等待两个匿名 Future**

　　运行时，我们会看到两个 Future 都跑到完成：


```text
hi number 1 from the first task!
hi number 1 from the second task!
hi number 2 from the first task!
hi number 2 from the second task!
hi number 3 from the first task!
hi number 3 from the second task!
hi number 4 from the first task!
hi number 4 from the second task!
hi number 5 from the first task!
hi number 6 from the first task!
hi number 7 from the first task!
hi number 8 from the first task!
hi number 9 from the first task!
```

　　现在，你会每次看到完全相同的顺序，这与我们用线程以及示例 17-7 中用 `trpl::spawn_task` 时看到的非常不同。那是因为 `trpl::join` 函数是*公平*的：它会以相近的频率轮询每个 Future，在它们之间交替执行，且不会让某个任务在另一个已就绪时一直独占执行。对线程而言，由操作系统决定检查哪个线程以及让它运行多久；对异步 Rust，则由运行时决定检查哪个任务。（实践中细节会更复杂：异步运行时在内部可能借助操作系统线程来管理并发，因此实现公平调度对运行时可能是额外负担——但仍然可以做到！）运行时不必为每种操作都保证公平，它们也常常提供不同的 API，供你按需选择是否需要公平调度。

　　试着对这些等待 Future 的方式做一些变化，看看会发生什么：

- 去掉任一或两个循环外的异步块。
- 在定义每个异步块后立刻等待它。
- 只把第一个循环包在异步块里，并在第二个循环体之后等待得到的 Future。

　　作为额外挑战，看看你能否在运行代码*之前*推断出每种情况下的输出！

<a id="message-passing"></a>

### 用消息传递在两个任务间发送数据 {#sending-data-between-two-tasks-using-message-passing}

　　在 Future 之间共享数据也会让人感到熟悉：我们再次使用消息传递，但这次用的是类型与函数的异步版本。我们将走一条与第 16 章[「用消息传递在线程间传数据」][message-passing-threads]一节略有不同的路径，以说明基于线程与基于 Future 的并发之间的若干关键差异。在示例 17-9 中，我们从单个异步块开始——*不*像派生独立线程那样派生独立任务。

**文件名：`src/main.rs`**
```rust
        let (tx, mut rx) = trpl::channel();

        let val = String::from("hi");
        tx.send(val).unwrap();

        let received = rx.recv().await.unwrap();
        println!("received '{received}'");
```

**示例 17-9：创建异步通道并把两端分别赋给 `tx` 与 `rx`**

　　这里我们使用 `trpl::channel`，它是第 16 章中与线程一起使用的多生产者、单消费者通道 API 的异步版本。异步版 API 与基于线程的版本只有一点不同：它使用可变而非不可变的接收端 `rx`，并且其 `recv` 方法产生需要等待的 Future，而不是直接产生值。现在我们可以从发送端向接收端发消息。注意我们不必派生独立线程甚至任务；只需等待 `rx.recv` 调用。

　　`std::mpsc::channel` 中同步的 `Receiver::recv` 方法会阻塞直到收到消息。`trpl::Receiver::recv` 不会，因为它是异步的。它不阻塞，而是把控制权交还给运行时，直到收到消息或通道的发送端关闭。相比之下，我们不等待 `send` 调用，因为它不阻塞。它也不需要阻塞，因为我们向其发送的通道是无界的。

> 注意：因为所有这些异步代码都运行在传给 `trpl::block_on` 的异步块中，其中的一切都可以避免阻塞。不过，它*之外*的代码会在 `block_on` 函数返回时阻塞。这正是 `trpl::block_on` 函数的全部意义：让你*选择*在何处阻塞于某组异步代码，从而选择在何处在同步与异步代码之间切换。

　　注意这个例子的两点。第一，消息会立刻到达。第二，尽管这里用了 Future，但还没有并发。示例中的一切都按顺序发生，就像根本没有 Future 参与一样。

　　我们先处理第一部分：发送一系列消息，并在它们之间睡眠，如示例 17-10 所示。


**文件名：`src/main.rs`**
```rust
        let (tx, mut rx) = trpl::channel();

        let vals = vec![
            String::from("hi"),
            String::from("from"),
            String::from("the"),
            String::from("future"),
        ];

        for val in vals {
            tx.send(val).unwrap();
            trpl::sleep(Duration::from_millis(500)).await;
        }

        while let Some(value) = rx.recv().await {
            println!("received '{value}'");
        }
```

**示例 17-10：通过异步通道发送并接收多条消息，并在每条消息之间用 `await` 睡眠**

　　除了发送消息，我们还需要接收它们。本例中，因为我们知道会有多少条消息到来，可以手动调用四次 `rx.recv().await`。但在现实世界中，我们通常会等待某个*未知*数量的消息，因此需要一直等待，直到确定没有更多消息。

　　在示例 16-10 中，我们用 `for` 循环处理从同步通道收到的全部项。然而 Rust 还没有办法对*异步产生*的一系列项使用 `for` 循环，因此需要使用一种我们尚未见过的循环：`while let` 条件循环。这是第 6 章[「用 `if let` 与 `let...else` 简化控制流」][if-let]一节中见过的 `if let` 构造的循环版本。只要它所指定的模式继续匹配该值，循环就会继续执行。

　　`rx.recv` 调用产生一个 Future，我们等待它。运行时会暂停该 Future 直到它就绪。一旦有消息到达，Future 就会解析为 `Some(message)`，有多少条消息就解析多少次。当通道关闭时，无论*是否*有任何消息到达过，Future 都会改为解析为 `None`，以表明没有更多值了，因此我们应停止轮询——也就是停止等待。

　　`while let` 循环把这一切串起来。若调用 `rx.recv().await` 的结果是 `Some(message)`，我们就得到该消息并可在循环体中使用它，就像用 `if let` 一样。若结果是 `None`，循环结束。每次循环完成，都会再次碰到 await 点，于是运行时再次暂停它，直到另一条消息到达。

　　代码现在成功发送并接收了全部消息。不幸的是，仍有几个问题。其一，消息并非以半秒间隔到达。它们在程序启动 2 秒（2,000 毫秒）后一口气全部到达。其二，这个程序也永不退出！相反，它永远等待新消息。你需要用 <kbd>ctrl</kbd>-<kbd>C</kbd> 关闭它。

#### 单个异步块内的代码线性执行

　　我们先弄清为何消息在完整延迟之后一口气到来，而不是在每条之间带延迟。在给定异步块内，代码中 `await` 关键字出现的顺序，也就是程序运行时它们被执行的顺序。

　　示例 17-10 中只有一个异步块，因此其中的一切都线性运行。仍然没有并发。所有 `tx.send` 调用发生完毕，其间夹杂所有 `trpl::sleep` 调用及其相关 await 点。只有在那之后，`while let` 循环才开始走过 `recv` 调用上的任何 await 点。

　　要得到我们想要的行为——睡眠延迟发生在每条消息之间——需要把 `tx` 与 `rx` 操作分别放进各自的异步块，如示例 17-11 所示。然后运行时可以用 `trpl::join` 分别执行它们，就像示例 17-8 一样。我们再次等待调用 `trpl::join` 的结果，而不是各个 Future。若我们按顺序等待各个 Future，就会又回到顺序流——这正是我们试图*避免*的。


**文件名：`src/main.rs`**
```rust
        let tx_fut = async {
            let vals = vec![
                String::from("hi"),
                String::from("from"),
                String::from("the"),
                String::from("future"),
            ];

            for val in vals {
                tx.send(val).unwrap();
                trpl::sleep(Duration::from_millis(500)).await;
            }
        };

        let rx_fut = async {
            while let Some(value) = rx.recv().await {
                println!("received '{value}'");
            }
        };

        trpl::join(tx_fut, rx_fut).await;
```

**示例 17-11：把 `send` 与 `recv` 分到各自的 `async` 块中，并等待这些块的 Future**

　　有了示例 17-11 中更新后的代码，消息会以 500 毫秒的间隔打印，而不是在 2 秒后一窝蜂出现。

#### 把所有权移入异步块

　　不过程序仍然永不退出，原因在于 `while let` 循环与 `trpl::join` 的交互方式：

- `trpl::join` 返回的 Future 只有在传给它的*两个* Future 都完成后才会完成。
- `tx_fut` Future 在发送完 `vals` 中最后一条消息并睡眠结束后完成。
- `rx_fut` Future 直到 `while let` 循环结束才会完成。
- `while let` 循环直到等待 `rx.recv` 产生 `None` 才会结束。
- 等待 `rx.recv` 只有在通道另一端关闭时才会返回 `None`。
- 通道只有在我们调用 `rx.close`，或当发送端 `tx` 被丢弃时才会关闭。
- 我们没有在任何地方调用 `rx.close`，而 `tx` 直到传给 `trpl::block_on` 的最外层异步块结束才会被丢弃。
- 该块无法结束，因为它阻塞在等待 `trpl::join` 完成上，于是我们又回到本列表顶部。

　　眼下，发送消息的异步块只是*借用* `tx`，因为发送消息并不需要所有权；但若我们能把 `tx` *移入*该异步块，它就会在该块结束时被丢弃。在第 13 章[「捕获引用或转移所有权」][capture-or-move]一节中，你学过如何对闭包使用 `move` 关键字；正如第 16 章[「在线程中使用 `move` 闭包」][move-threads]一节所讨论的，与线程打交道时我们常常需要把数据移入闭包。同样的基本动态也适用于异步块，因此 `move` 关键字对异步块的作用与对闭包一样。

　　在示例 17-12 中，我们把用于发送消息的块从 `async` 改成 `async move`。

**文件名：`src/main.rs`**
```rust
        let (tx, mut rx) = trpl::channel();

        let tx_fut = async move {
            // --snip--
```

**示例 17-12：对示例 17-11 的修订：完成后能正确关闭**

　　运行*这个*版本的代码时，它会在最后一条消息发送并接收后优雅关闭。接下来看看要从多个 Future 发送数据需要改什么。

#### 用 `join!` 宏连接任意数量的 Future

　　这个异步通道也是多生产者通道，因此若要从多个 Future 发送消息，可以对 `tx` 调用 `clone`，如示例 17-13 所示。

**文件名：`src/main.rs`**
```rust
        let (tx, mut rx) = trpl::channel();

        let tx1 = tx.clone();
        let tx1_fut = async move {
            let vals = vec![
                String::from("hi"),
                String::from("from"),
                String::from("the"),
                String::from("future"),
            ];

            for val in vals {
                tx1.send(val).unwrap();
                trpl::sleep(Duration::from_millis(500)).await;
            }
        };

        let rx_fut = async {
            while let Some(value) = rx.recv().await {
                println!("received '{value}'");
            }
        };

        let tx_fut = async move {
            let vals = vec![
                String::from("more"),
                String::from("messages"),
                String::from("for"),
                String::from("you"),
            ];

            for val in vals {
                tx.send(val).unwrap();
                trpl::sleep(Duration::from_millis(1500)).await;
            }
        };

        trpl::join!(tx1_fut, tx_fut, rx_fut);
```

**示例 17-13：在异步块中使用多个生产者**

　　首先，我们克隆 `tx`，在第一个异步块外创建 `tx1`。我们像之前对 `tx` 那样把 `tx1` 移入该块。然后稍后把原来的 `tx` 移入一个*新*的异步块，在那里以稍慢的延迟发送更多消息。我们碰巧把这个新异步块放在接收消息的异步块之后，但放在前面也完全可以。关键在于各 Future 被等待的顺序，而不是被创建的顺序。

　　两个发送消息的异步块都需要是 `async move` 块，以便 `tx` 与 `tx1` 在那些块结束时被丢弃。否则我们又会回到一开始的无限循环。

　　最后，我们从 `trpl::join` 换成 `trpl::join!` 来处理额外的 Future：`join!` 宏可以等待任意数量的 Future，只要我们在编译期知道 Future 的数量。本章稍后会讨论等待数量未知的 Future 集合。

　　现在我们会看到来自两个发送 Future 的全部消息；又因为发送 Future 在发送后使用略有不同的延迟，消息也会以那些不同的间隔被接收：


```text
received 'hi'
received 'more'
received 'from'
received 'the'
received 'messages'
received 'future'
received 'for'
received 'you'
```

　　我们已经探索了如何用消息传递在 Future 之间发送数据、异步块内的代码如何顺序运行、如何把所有权移入异步块，以及如何连接多个 Future。接下来讨论如何以及为何告诉运行时它可以切换到另一个任务。

[thread-spawn]: ../../concurrency/01-threads/#creating-a-new-thread-with-spawn
[join-handles]: ../../concurrency/01-threads/#waiting-for-all-threads-to-finish
[message-passing-threads]: ../../concurrency/02-message-passing/
[if-let]: ../../enums/03-if-let/
[capture-or-move]: ../../functional-features/01-closures/#capturing-references-or-moving-ownership
[move-threads]: ../../concurrency/01-threads/#using-move-closures-with-threads
