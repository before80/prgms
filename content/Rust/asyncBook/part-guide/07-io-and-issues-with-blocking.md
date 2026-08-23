+++
title = "7-IO 与阻塞问题"
date = 2026-08-22T19:00:00+08:00
weight = 9
type = "docs"
description = "IO 与阻塞问题"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Asynchronous Programming in Rust](https://rust-lang.github.io/async-book/)

# IO 与阻塞问题 {#io-and-issues-with-blocking}


> 原文链接: [https://rust-lang.github.io/async-book/part-guide/io.html](https://rust-lang.github.io/async-book/part-guide/io.html)


高效处理 IO（输入/输出）是异步编程的主要动机之一，大多数异步程序会做大量 IO。归根结底，IO 的问题在于它比计算慢几个数量级，因此干等 IO 完成而不做其他工作极其低效。理想情况下，异步编程让程序在等待 IO 时能做其他工作。

本章介绍异步语境下的 IO。我们会涵盖阻塞与非阻塞 IO 的重要区别，以及阻塞 IO 与异步编程为何不能混用（至少不经一些思考和努力不行）。我们会讲如何使用非阻塞 IO，然后看 IO 与异步编程可能出现的一些问题。还会看 OS 如何处理 IO，并略窥 io_uring 等替代 IO 方法。

最后涵盖阻塞异步任务的其他方式（这很糟糕），以及如何正确将异步编程与阻塞 IO 或长时间 CPU 密集型代码混合使用。


## 阻塞与非阻塞 IO

IO 由操作系统实现；IO 工作在独立进程和/或专用硬件中进行，无论哪种情况都在程序进程之外。IO 可以是同步或异步的（分别 aka 阻塞和非阻塞）。同步 IO 意味着程序（或至少线程）在 IO 进行时等待（aka 阻塞），直到 IO 完成并从 OS 收到结果才开始处理。异步 IO 意味着程序在 IO 进行时可以继续取得进展，稍后再取结果。两种 IO 都有许多不同的 OS API，异步方面种类更多。

异步 IO 与异步编程并非内在绑定。然而，异步编程便于人体工学且高性能的异步 IO，这是异步编程的主要动机之一。因同步 IO 导致的阻塞是异步编程性能问题的主要来源，必须小心避免（下文详述）。

Rust 标准库包含阻塞 IO 的函数和 trait。非阻塞 IO 必须使用专用库，通常是异步运行时的一部分，例如 Tokio 的 [`io`](https://docs.rs/tokio/latest/tokio/io/index.html) 模块。

快速看一个例子（改编自 Tokio 文档）：

```rust
use tokio::{io::AsyncWriteExt, net::TcpStream};

async fn write_hello() -> Result<(), Box<dyn std::error::Error>> {
    let mut stream = TcpStream::connect("127.0.0.1:8080").await?;
    stream.write_all(b"hello world!").await?;

    Ok(())
}
```

`write_all` 是向 `stream` 写入数据的异步 IO 方法。这可能立即完成，但更可能需一些时间，因此 `stream.write_all(...).await` 会使当前任务在等待 OS 处理写入时暂停。调度器会运行其他任务，写入完成后唤醒该任务并调度其继续工作。

然而，若使用标准库的写入函数，异步调度器不会参与，OS 会在 IO 完成时暂停整个线程，意味着不仅当前任务暂停，该线程上也无法执行其他任务。若运行时线程池中的所有线程都发生这种情况（某些情况下可能只有一个线程），整个程序停止，无法取得进展。这称为阻塞线程（或程序），对性能非常糟糕。绝不要在异步程序中阻塞线程，因此应避免在异步任务中使用阻塞 IO。

阻塞线程也可能由长时间运行的任务或等待锁引起，以及阻塞 IO。本章[末尾](#other-blocking-operations)会更多讨论。

反复读取或写入是常见模式，stream 和 sink（aka 异步迭代器）是方便的机制。[专门一章](../../streams/)会涵盖它们。


## 读取与写入

TODO

- 异步 Read 和 Write trait
  - 运行时的一部分
- 如何使用
- 具体实现
  - 网络 vs 磁盘
    - tcp, udp
    - 文件系统并非真正异步，但有 io_uring（引用该章）
  - 实际例子
  - stdout 等
  - pipe, fd 等


## 内存管理

读取数据需要放在某处，写入数据在写入完成前需要保存在某处。无论哪种情况，内存如何管理都很重要。

TODO


- 缓冲区管理与异步 IO 的问题
- 不同方案及优缺点
  - 零拷贝方案
  - 共享缓冲区方案
- 帮助处理的实用 crate，Bytes 等

## IO 高级主题

TODO


- buf read/write
- Read + Write, split, join
- copy
- simplex and duplex
- cancelation
- 若必须做同步 IO？spawn 线程或用 spawn_blocking（见下文）

## OS 视角下的 IO

TODO

- 不同种类的 IO 与机制，completion IO，高级章节中 completion IO 章的引用
  - 不同运行时可以促进这一点
  - mio 作为底层接口


## 其他阻塞操作 {#other-blocking-operations}

如本章开头所述，不阻塞线程对异步程序性能至关重要。各种阻塞 IO 是常见的阻塞方式，但也可能通过大量计算或以异步调度器未协调的方式等待而阻塞。

等待最常因使用非异步感知的同步机制引起，例如用 `std::sync::Mutex` 而非异步互斥锁，或等待非异步通道。我们会在[通道、锁与同步](../09-channels-locking-and-synchronization/)一章讨论。还有其他阻塞式等待方式，一般需要找到非阻塞或其他异步友好机制，例如用异步 `sleep` 函数而非 std 的。等待也可能是忙等（ effectively 循环空转，aka 自旋锁），最好避免。

### CPU 密集型工作

长时间运行（即 CPU 密集型或 CPU 绑定）的工作会阻止调度器运行其他任务。这*是*一种阻塞，但不如阻塞 IO 或等待糟糕，因为至少程序在取得一些进展。然而（不经细心考虑），按某种度量（如尾延迟）可能对性能欠佳，若无法运行的任务需要在特定时间运行，也可能是正确性问题。有种说法说 CPU 密集型工作根本不该用 async Rust（或 Tokio 等通用异步运行时），但这过于简化。正确的是：若不特殊处理就混合 IO 绑定与 CPU 绑定（或更精确地说，长时间运行与延迟敏感）任务，别指望过得愉快。

本节余下部分假设你有延迟敏感任务和长时间 CPU 密集型任务的混合。若没有任何延迟敏感的东西，情况略有不同（大多更简单）。

运行长时间或阻塞任务本质上三种方案：用运行时内置设施、用单独线程，或用单独运行时。

在 Tokio 中，可用 [`spawn_blocking`](https://docs.rs/tokio/latest/tokio/task/fn.spawn_blocking.html) spawn 可能阻塞的任务。与 [`spawn`](https://docs.rs/tokio/latest/tokio/task/fn.spawn.html) spawn 任务类似，但在为可能阻塞的任务优化的单独线程池中运行（任务很可能在自己的线程上运行）。注意这运行普通同步代码，不是异步任务。意味着任务不能被取消（尽管其 `JoinHandle` 有 `abort` 方法）。其他运行时提供类似功能。

此例用 `spawn_blocking` 通过调用标准库的同步文件系统函数执行阻塞 I/O。注意 [`tokio::fs`](https://docs.rs/tokio/latest/tokio/fs/index.html) 也存在并提供异步文件系统 API；但其底层也用 `spawn_blocking` 包装的阻塞操作。

```rust,norun
use tokio;

#[tokio::main]
async fn main() {
    let contents = tokio::task::spawn_blocking(|| {
		std::fs::read_to_string("file.txt").unwrap()
    })
	.await
	.unwrap();

	// 对 contents 做点什么
}
```

因 `spawn_blocking` spawn 的任务不能被 abort，它用于最终会完成的工作。可能无限期阻塞的任务（如监听传入请求的服务器）最好在专用线程上运行，以免长时间占用 Tokio 阻塞线程池中的线程。可用 [`std::thread::spawn`](https://doc.rust-lang.org/stable/std/thread/fn.spawn.html) 或类似 API 创建。

若需运行大量任务，可能需要某种线程池或工作调度器。若不断 spawn 线程且数量远超可用核心，会牺牲吞吐量。[Rayon](https://github.com/rayon-rs/rayon) 是流行选择，便于运行和管理并行任务。针对工作负载更专门、或对任务有一定了解的方案可能性能更好。

下面是 Tokio 与 Rayon 一起使用的例子。利用 [`tokio::oneshot::channel`](https://docs.rs/tokio/latest/tokio/sync/oneshot/fn.channel.html) 在 Rayon spawn 的任务与 Tokio 当前任务间传递结果。

```rust,norun
use rayon::prelude::*;

#[tokio::main]
async fn main() {
    let data = 1..=10;

    let (send, recv) = tokio::sync::oneshot::channel();
    // 在 rayon 上 spawn 任务以避免阻塞当前任务
    std::thread::spawn(move || {
        // 用 rayon 并行迭代器并行计算结果
        let results = data.into_par_iter().map(compute).collect::<Vec<_>>();
        // 把结果发回 Tokio。
        send.send(results).unwrap();
    });

    // 等待 rayon 任务并获取结果
    let results = recv.await.unwrap();
    println!("Results: {:?}", results);
}

fn compute(input: u64) -> u64 {
    // 通过求和大量整数模拟 CPU 密集型计算。
    let mut sum = 0u64;
    for i in 0..100_000_000 {
        sum = sum.wrapping_add(i * i);
    }
    sum % input
}
```

可为延迟敏感任务和长时间任务使用单独的异步运行时实例。适合 CPU 绑定任务，但长时间任务的运行时仍不应使用阻塞 IO。对 CPU 绑定任务，这是唯一支持长时间任务为异步任务的方案。也灵活（因为可配置运行时以优化其运行的任务类型；要最佳性能确实需投入运行时配置），且能受益于 Tokio 等成熟子系统。甚至可以用两个不同的异步运行时。无论哪种情况，运行时必须在不同线程上运行。

另一方面，需要多思考：必须确保在正确的运行时上运行任务（可能比听起来难），任务间通信可能复杂。下一节讨论同步与异步上下文间的同步，但多个异步运行时之间更棘手。每个运行时是自己独立的小宇宙，调度器完全独立。Tokio 通道和锁*可以*跨运行时使用（甚至非 Tokio），但其他运行时的原语可能不行。

由于每个运行时的调度器不知道其他运行时（OS 也不知道任何异步调度器），调度与工作窃取在运行时间没有协调或共享优先级。因此任务调度可能欠佳（尤其运行时未针对工作负载调优时）。此外，所有调度都是协作式的，长时间任务仍可能饿死资源，延迟受损。长时间任务如何更协作见[下一节](#yielding)。

作为纯调度器，用 Tokio 做 CPU 工作可能比专用同步工作池开销略高。考虑到支持异步编程的额外工作，这不意外。对大多数用户实践中可能不是问题，但若代码极度性能敏感值得考虑。

对上述任一方案，任务会在不同上下文（同步与异步，或不同异步运行时）中运行。若需在任务间通信，需注意使用正确的同步与异步原语组合（通道、互斥锁等）及这些原语上正确的（阻塞或非阻塞）方法。对互斥锁及类似锁，若需跨 await 点持有锁或保护 IO 资源，应 probably 用异步版本（同步上下文可用阻塞锁方法），或保护数据、锁不需跨 await 时用同步版本。Tokio 异步通道可用阻塞方法从同步上下文使用，但详见[这些文档](https://docs.rs/tokio/latest/tokio/sync/mpsc/index.html#communicating-between-sync-and-async-code)何时用同步或异步通道。

那么，上述方案该用哪个？

- 若做阻塞 IO，应 probably 用 `spawn_blocking`。不能用第二个运行时或其他线程池（至少若要最佳性能）。
- 若有永远运行的线程，应用 `std::thread::spawn` 而非任何线程池（否则会占用池中的一个线程）。
- 若做*大量* CPU 工作，应用线程池，专用池或第二个异步运行时。
- 若需运行长时间异步代码，应用第二个运行时。
- 可能因简单且性能满意而选择专用线程或 `spawn_blocking`，尽管更复杂的方案更优。


### 让出 {#yielding}

长时间运行的代码是问题，因为它不给调度器调度其他任务的机会。异步并发是协作式的：调度器不能抢占任务去运行另一个。若长时间任务不向调度器让出，调度器无法停止它。但若长时间代码向调度器让出，其他任务可被调度，任务长时间运行就不是问题。这可作为用另一线程做 CPU 密集型工作，或在自己运行时上做 CPU 密集型工作以（可能）改善性能的替代。

让出很简单，调用运行时的 yield 函数。Tokio 中是 [`yield_now`](https://docs.rs/tokio/latest/tokio/task/fn.yield_now.html)。注意这与标准库的 [`yield_now`](https://doc.rust-lang.org/stable/std/thread/fn.yield_now.html) 和协程的 `yield` 关键字都不同。若当前 future 在 `select` 或 `join` 内运行，调用 `yield_now` 不会让出给调度器（见[并发组合 future](../08-composing-futures-concurrently/)一章）；这可能符合也可能不符合你的意图。

知道何时需要让出更棘手。首先要知程序是否隐式让出。这只能发生在 `.await`，若不 `await` 就不会让出。但 await 不会自动让出给调度器。只有被 `await` 的叶子 future 处于 pending（未就绪），或调用栈某处有显式 `yield` 时才会。Tokio 和大多数异步运行时会在其 IO 和同步函数中这样做，但一般无法不调试或看源码就知道 `await` 是否会让出。

经验法则是：代码在 10–100 微秒内应碰到潜在让出点。

### 参考资料

- [Tokio 关于 CPU 绑定任务与阻塞代码的文档](https://docs.rs/tokio/latest/tokio/index.html#cpu-bound-tasks-and-blocking-code)
- [博客文章：What is Blocking?](https://ryhl.io/blog/async-what-is-blocking/)
- [博客文章：Using Rustlang's Async Tokio Runtime for CPU-Bound Tasks](https://thenewstack.io/using-rustlangs-async-tokio-runtime-for-cpu-bound-tasks/)
