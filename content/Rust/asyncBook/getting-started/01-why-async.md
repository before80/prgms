+++
title = "19.1-为何使用异步？"
date = 2026-08-22T19:00:00+08:00
weight = 23
type = "docs"
description = "为何使用异步？"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Asynchronous Programming in Rust](https://rust-lang.github.io/async-book/)

# 为何使用异步？ {#why-async}


> 原文链接: [https://rust-lang.github.io/async-book/01_getting_started/02_why_async.html](https://rust-lang.github.io/async-book/01_getting_started/02_why_async.html)


我们都喜欢 Rust 让我们能够编写快速、安全的软件。但异步编程如何融入这一愿景？

异步编程（简称 async）是一种**并发编程模型**，得到越来越多编程语言的支持。它让你能在少量 OS 线程上运行大量并发任务，同时通过 `async/await` 语法保留普通同步编程的大部分外观与手感。

## 异步与其他并发模型

并发编程不如常规顺序编程成熟和「标准化」。因此，我们表达并发的方式会因语言所支持的并发模型而异。简要概览最流行的几种并发模型，有助于理解异步编程在更广泛并发编程领域中的位置：

- **OS 线程**不需要改变编程模型，因此很容易表达并发。但线程间同步可能很困难，且性能开销较大。线程池可缓解部分成本，但仍不足以支撑大规模 IO 密集型工作负载。
- **事件驱动编程**配合**回调**可以非常高效，但往往导致冗长、「非线性」的控制流。数据流与错误传播通常难以追踪。
- **协程**与线程一样，不需要改变编程模型，因此易于使用。与 async 类似，它们也能支持大量任务。但它们抽象掉了对系统编程和自定义运行时实现者很重要的底层细节。
- **Actor 模型**将所有并发计算划分为称为 actor 的单元，通过可能失败的消息传递通信，类似于分布式系统。Actor 模型可以高效实现，但对许多实际问题（如流控与重试逻辑）缺乏答案。

总之，异步编程允许在 Rust 这类底层语言上实现高性能，同时提供线程和协程的大部分易用性优势。

## Rust 中的异步与其他语言

尽管许多语言都支持异步编程，但实现细节各有不同。Rust 的 async 实现在若干方面与大多数语言不同：

- 在 Rust 中，**Future 是惰性的**，只有在被 poll 时才会推进。丢弃 Future 会阻止其继续推进。
- 在 Rust 中，**异步是零成本的**，意味着你只为实际使用的内容付费。具体而言，你可以在不进行堆分配和动态分发的情况下使用 async，这对性能非常有益！这也让你能在嵌入式系统等受限环境中使用 async。
- Rust **不提供内置运行时**。运行时由社区维护的 crate 提供。
- Rust 中既有**单线程**也有**多线程**运行时，各有优劣。

## Rust 中异步与线程

在 Rust 中，async 的主要替代方案是使用 OS 线程，可直接通过 [`std::thread`](https://doc.rust-lang.org/std/thread/)，或通过线程池间接使用。从线程迁移到 async 或反之，通常需要大量重构，无论是在实现层面，还是（若你正在构建库）任何对外公开的接口。因此，尽早选择适合需求的模型可以节省大量开发时间。

**OS 线程**适合任务数量较少的场景，因为线程会带来 CPU 和内存开销。创建线程以及在线程间切换成本很高，即使空闲线程也会消耗系统资源。线程池库可缓解部分成本，但不能全部消除。不过，线程让你能在不大改代码的情况下复用现有同步代码——不需要特定的编程模型。在某些操作系统中，你还可以更改线程优先级，这对驱动程序和其他延迟敏感的应用很有用。

**Async** 显著降低 CPU 和内存开销，尤其对大量 IO 密集型任务（如服务器和数据库）的工作负载。在其他条件相同的情况下，你可以拥有比 OS 线程多几个数量级的任务，因为异步运行时用少量（昂贵的）线程处理大量（廉价的）任务。不过，由于 async 函数生成的状态机，以及每个可执行文件都捆绑了异步运行时，异步 Rust 往往会产生更大的二进制文件。

最后一点，异步编程并不比线程**更好**，只是**不同**。若你不需要 async 带来的性能优势，线程往往是更简单的选择。

### 示例：并发下载

在本示例中，我们的目标是并发下载两个网页。在典型的多线程应用中，需要创建线程来实现并发：

```rust,ignore
fn get_two_sites() {
    // Spawn two threads to do work.
    let thread_one = thread::spawn(|| download("https://www.foo.com"));
    let thread_two = thread::spawn(|| download("https://www.bar.com"));

    // Wait for both threads to complete.
    thread_one.join().expect("thread one panicked");
    thread_two.join().expect("thread two panicked");
}
```

然而，下载网页是小任务；为如此少量工作创建线程相当浪费。对更大型的应用，这很容易成为瓶颈。在异步 Rust 中，我们可以在不创建额外线程的情况下并发运行这些任务：

```rust,ignore
async fn get_two_sites_async() {
    // Create two different "futures" which, when run to completion,
    // will asynchronously download the webpages.
    let future_one = download_async("https://www.foo.com");
    let future_two = download_async("https://www.bar.com");

    // Run both futures to completion at the same time.
    join!(future_one, future_two);
}
```

这里不会创建额外线程。此外，所有函数调用都是静态分发的，且没有堆分配！不过，我们首先需要把代码写成异步的，本书将帮助你做到这一点。

## Rust 中的自定义并发模型

最后一点，Rust 并不强迫你在线程和 async 之间二选一。你可以在同一个应用中使用两种模型，这在混合了线程和异步依赖时很有用。实际上，你甚至可以完全使用不同的并发模型，例如事件驱动编程，只要你找到实现它的库即可。
