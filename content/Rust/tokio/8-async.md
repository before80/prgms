+++
title = "8 深入 async"
date = 2026-08-23T16:54:00+08:00
weight = 9
type = "docs"
description = ""
isCJKLanguage = true
draft = false

+++


> 原文链接: [https://tokio.rs/tokio/tutorial/async](https://tokio.rs/tokio/tutorial/async)

至此，我们已经相当全面地游览了异步 Rust 和 Tokio。现在我们将更深入地探讨 Rust 的异步运行时模型。在教程最开始，我们暗示异步 Rust 采取了一种独特的方式。现在，我们来解释这意味着什么。


作为快速回顾，来看一个非常基础的异步函数。与教程到目前为止所讲的内容相比，这里没有什么新东西。

```rust
use tokio::net::TcpStream;

async fn my_async_fn() {
    println!("hello from async");
    let _socket = TcpStream::connect("127.0.0.1:3000").await.unwrap();
    println!("async TCP operation complete");
}
```

我们调用该函数，它返回某个值。我们对该值调用 `.await`。

```rust
# async fn my_async_fn() {}
#[tokio::main]
async fn main() {
    let what_is_this = my_async_fn();
    // 此时还没有任何输出
    what_is_this.await;
    // 文本已打印，套接字已建立并关闭
}
```

`my_async_fn()` 返回的值是一个 future。future 是实现了标准库提供的 [`std::future::Future`][trait] trait 的值。它们包含进行中的异步计算。

[`std::future::Future`][trait] trait 的定义是：

```rust
use std::pin::Pin;
use std::task::{Context, Poll};

pub trait Future {
    type Output;

    fn poll(self: Pin<&mut Self>, cx: &mut Context)
        -> Poll<Self::Output>;
}
```

[关联类型][assoc] `Output` 是 future 完成后产生的类型。[`Pin`][pin] 类型是 Rust 能够在 `async` 函数中支持借用的方式。更多细节请参阅[标准库][pin]文档。

与其他语言中 future 的实现不同，Rust 的 future 并不表示在后台进行的计算，Rust 的 future **就是**计算本身。future 的所有者负责通过轮询 future 来推进计算。这是通过调用 `Future::poll` 完成的。

## 实现 `Future`

让我们实现一个非常简单的 future。这个 future 将：

1. 等待到某个特定时刻。
2. 向 STDOUT 输出一些文本。
3. 产出一个字符串。

```rust
use std::future::Future;
use std::pin::Pin;
use std::task::{Context, Poll};
use std::time::{Duration, Instant};

struct Delay {
    when: Instant,
}

impl Future for Delay {
    type Output = &'static str;

    fn poll(self: Pin<&mut Self>, cx: &mut Context<'_>)
        -> Poll<&'static str>
    {
        if Instant::now() >= self.when {
            println!("Hello world");
            Poll::Ready("done")
        } else {
            // 暂时忽略这一行
            cx.waker().wake_by_ref();
            Poll::Pending
        }
    }
}

#[tokio::main]
async fn main() {
    let when = Instant::now() + Duration::from_millis(10);
    let future = Delay { when };

    let out = future.await;
    assert_eq!(out, "done");
}
```

## 异步函数作为 Future

在 main 函数中，我们实例化 future 并对它调用 `.await`。在 async 函数中，我们可以对任何实现了 `Future` 的值调用 `.await`。反过来，调用 `async` 函数会返回一个实现了 `Future` 的匿名类型。对于 `async fn main()`，生成的 future 大致是：

```rust
use std::future::Future;
use std::pin::Pin;
use std::task::{Context, Poll};
use std::time::{Duration, Instant};

enum MainFuture {
    // 已初始化，从未被 poll
    State0,
    // 正在等待 `Delay`，即 `future.await` 那一行
    State1(Delay),
    // future 已完成
    Terminated,
}
# struct Delay { when: Instant };
# impl Future for Delay {
#     type Output = &'static str;
#     fn poll(self: Pin<&mut Self>, _: &mut Context<'_>) -> Poll<&'static str> {
#         unimplemented!();
#     }
# }

impl Future for MainFuture {
    type Output = ();

    fn poll(mut self: Pin<&mut Self>, cx: &mut Context<'_>)
        -> Poll<()>
    {
        use MainFuture::*;

        loop {
            match *self {
                State0 => {
                    let when = Instant::now() +
                        Duration::from_millis(10);
                    let future = Delay { when };
                    *self = State1(future);
                }
                State1(ref mut my_future) => {
                    match Pin::new(my_future).poll(cx) {
                        Poll::Ready(out) => {
                            assert_eq!(out, "done");
                            *self = Terminated;
                            return Poll::Ready(());
                        }
                        Poll::Pending => {
                            return Poll::Pending;
                        }
                    }
                }
                Terminated => {
                    panic!("future polled after completion")
                }
            }
        }
    }
}
```

Rust 的 future 是**状态机**。这里 `MainFuture` 表示为 future 可能状态的 `enum`。future 从 `State0` 状态开始。调用 `poll` 时，future 会尽可能推进其内部状态。如果 future 能够完成，则返回包含异步计算输出的 `Poll::Ready`。

如果 future **无法**完成，通常是因为它等待的资源尚未就绪，则返回 `Poll::Pending`。收到 `Poll::Pending` 向调用者表明 future 将在稍后完成，调用者应稍后再次调用 `poll`。

我们还看到 future 由其他 future 组成。对外层 future 调用 `poll` 会导致调用内层 future 的 `poll` 函数。

# 执行器

异步 Rust 函数返回 future。必须对 future 调用 `poll` 才能推进其状态。future 由其他 future 组成。那么，谁会对最外层的 future 调用 `poll` 呢？

回想一下，要运行异步函数，必须将它们传给 `tokio::spawn`，或者使用带 `#[tokio::main]` 注解的 main 函数。这会将生成的外层 future 提交给 Tokio 执行器。执行器负责对最外层 future 调用 `Future::poll`，驱动异步计算直至完成。

## Mini Tokio

为了更好地理解这一切如何配合，让我们实现自己的 Tokio 最小版本！完整代码见[这里][mini-tokio]。

```rust
use std::collections::VecDeque;
use std::future::Future;
use std::pin::Pin;
use std::task::{Context, Poll};
use std::time::{Duration, Instant};
use futures::task;

fn main() {
    let mut mini_tokio = MiniTokio::new();

    mini_tokio.spawn(async {
        let when = Instant::now() + Duration::from_millis(10);
        let future = Delay { when };

        let out = future.await;
        assert_eq!(out, "done");
    });

    mini_tokio.run();
}
# struct Delay { when: Instant }
# impl Future for Delay {
#     type Output = &'static str;
#     fn poll(self: Pin<&mut Self>, _: &mut Context<'_>) -> Poll<&'static str> {
#         Poll::Ready("done")
#     }
# }

struct MiniTokio {
    tasks: VecDeque<Task>,
}

type Task = Pin<Box<dyn Future<Output = ()> + Send>>;

impl MiniTokio {
    fn new() -> MiniTokio {
        MiniTokio {
            tasks: VecDeque::new(),
        }
    }

    /// 将 future spawn 到 mini-tokio 实例上
    fn spawn<F>(&mut self, future: F)
    where
        F: Future<Output = ()> + Send + 'static,
    {
        self.tasks.push_back(Box::pin(future));
    }

    fn run(&mut self) {
        let waker = task::noop_waker();
        let mut cx = Context::from_waker(&waker);

        while let Some(mut task) = self.tasks.pop_front() {
            if task.as_mut().poll(&mut cx).is_pending() {
                self.tasks.push_back(task);
            }
        }
    }
}
```

这会运行 async 块。创建了一个带有所需延迟的 `Delay` 实例并对其 await。然而，我们目前的实现有一个重大**缺陷**。执行器从不休眠。执行器持续循环**所有**已 spawn 的 future 并对它们 poll。大多数时候 future 尚未准备好执行更多工作，会再次返回 `Poll::Pending`。这个过程会消耗 CPU 周期，通常效率很低。

理想情况下，我们希望在 future 能够取得进展时才 poll 它。当任务阻塞的资源变为可以执行所请求操作的就绪状态时，就会发生这种情况。如果任务想从 TCP 套接字读取数据，我们只希望在 TCP 套接字收到数据时才 poll 该任务。在我们的例子中，任务阻塞在等待给定的 `Instant` 到达。理想情况下，mini-tokio 只应在那个时刻过去后才 poll 该任务。

为实现这一点，当资源被 poll 且资源**未**就绪时，资源会在转变为就绪状态时发送一次通知。

# Waker

Waker 就是缺失的那一块。这是资源能够通知等待任务「资源已就绪，可以继续某项操作」的机制。

再看一次 `Future::poll` 的定义：

```rust
fn poll(self: Pin<&mut Self>, cx: &mut Context)
    -> Poll<Self::Output>;
```

`poll` 的 `Context` 参数有 `waker()` 方法。该方法返回绑定到当前任务的 [`Waker`]。[`Waker`] 有 `wake()` 方法。调用该方法向执行器发出信号，表示关联任务应被调度执行。资源在转变为就绪状态时会调用 `wake()`，通知执行器 poll 该任务将能够取得进展。

## 更新 `Delay`

我们可以更新 `Delay` 以使用 waker：

```rust
use std::future::Future;
use std::pin::Pin;
use std::task::{Context, Poll};
use std::time::{Duration, Instant};
use std::thread;

struct Delay {
    when: Instant,
}

impl Future for Delay {
    type Output = &'static str;

    fn poll(self: Pin<&mut Self>, cx: &mut Context<'_>)
        -> Poll<&'static str>
    {
        if Instant::now() >= self.when {
            println!("Hello world");
            Poll::Ready("done")
        } else {
            // 获取当前任务的 waker 句柄
            let waker = cx.waker().clone();
            let when = self.when;

            // spawn 一个定时器线程
            thread::spawn(move || {
                let now = Instant::now();

                if now < when {
                    thread::sleep(when - now);
                }

                waker.wake();
            });

            Poll::Pending
        }
    }
}
```

现在，一旦请求的持续时间过去，调用任务就会收到通知，执行器可以确保任务再次被调度。下一步是更新 mini-tokio 以监听 wake 通知。

我们的 `Delay` 实现仍有一些遗留问题。我们稍后会修复它们。

> **warning**
> 当 future 返回 `Poll::Pending` 时，它**必须**确保在某个时刻发出 waker 信号。忘记这样做会导致任务无限期挂起。
>
> 在返回 `Poll::Pending` 后忘记 wake 任务是常见的 bug 来源。

回想 `Delay` 的第一版。当时的 future 实现是：

```rust
# use std::future::Future;
# use std::pin::Pin;
# use std::task::{Context, Poll};
# use std::time::Instant;
# struct Delay { when: Instant }
impl Future for Delay {
    type Output = &'static str;

    fn poll(self: Pin<&mut Self>, cx: &mut Context<'_>)
        -> Poll<&'static str>
    {
        if Instant::now() >= self.when {
            println!("Hello world");
            Poll::Ready("done")
        } else {
            // 暂时忽略这一行
            cx.waker().wake_by_ref();
            Poll::Pending
        }
    }
}
```

在返回 `Poll::Pending` 之前，我们调用了 `cx.waker().wake_by_ref()`。这是为了满足 future 契约。返回 `Poll::Pending` 意味着我们负责发出 waker 信号。因为我们尚未实现定时器线程，所以内联发出了 waker 信号。这样做会导致 future 被立即重新调度、再次执行，并且很可能仍未准备好完成。

注意，允许比必要更频繁地发出 waker 信号。在这个特定例子中，我们发出 waker 信号，尽管我们根本还没准备好继续操作。除了浪费一些 CPU 周期外，这没有问题。然而，这个特定实现会导致忙循环。

## 更新 Mini Tokio

下一步是更新 Mini Tokio 以接收 waker 通知。我们希望执行器只在任务被 wake 时运行它们。为此，Mini Tokio 将提供自己的 waker。当 waker 被调用时，其关联任务会被排队等待执行。Mini-Tokio 在 poll future 时会将这个 waker 传给 future。

更新后的 Mini Tokio 将使用 channel 存储已调度的任务。channel 允许从任何线程将任务排队等待执行。Waker 必须是 `Send` 和 `Sync`。

> **info**
> `Send` 和 `Sync` trait 是与 Rust 提供的并发相关的标记 trait。可以**发送**到不同线程的类型是 `Send`。大多数类型都是 `Send`，但像 [`Rc`] 这样的类型不是。可以通过不可变引用**并发**访问的类型是 `Sync`。类型可以是 `Send` 但不是 `Sync`——[`Cell`] 就是一个好例子，它可以通过不可变引用修改，因此并发访问不安全。
>
> 更多细节请参阅 Rust 书中相关[章节][ch]。

[`Rc`]: https://doc.rust-lang.org/std/rc/struct.Rc.html
[`Cell`]: https://doc.rust-lang.org/std/cell/struct.Cell.html
[ch]: https://doc.rust-lang.org/book/ch16-04-extensible-concurrency-sync-and-send.html

更新 `MiniTokio` 结构体。

```rust
use std::sync::mpsc;
use std::sync::Arc;

struct MiniTokio {
    scheduled: mpsc::Receiver<Arc<Task>>,
    sender: mpsc::Sender<Arc<Task>>,
}

struct Task {
    // 很快就会填充
}
```

Waker 是 `Sync` 的且可以克隆。调用 `wake` 时，必须将任务调度执行。为实现这一点，我们有一个 channel。在 waker 上调用 `wake()` 时，任务被推入 channel 的发送端。我们的 `Task` 结构将实现 wake 逻辑。为此，它需要同时包含已 spawn 的 future 和 channel 发送端。我们将 future 放在 `TaskFuture` 结构体中， alongside 一个 `Poll` enum 来跟踪最新的 `Future::poll()` 结果，这对于处理虚假唤醒是必需的。更多细节见 `TaskFuture` 中 `poll()` 方法的实现。

```rust
# use std::future::Future;
# use std::pin::Pin;
# use std::sync::mpsc;
# use std::task::Poll;
use std::sync::{Arc, Mutex};

/// 持有 future 及其 `poll` 方法
/// 最近一次调用结果的结构体
struct TaskFuture {
    future: Pin<Box<dyn Future<Output = ()> + Send>>,
    poll: Poll<()>,
}

struct Task {
    // `Mutex` 用于使 `Task` 实现 `Sync`。在任意时刻
    // 只有一个线程访问 `task_future`。
    // 就正确性而言 `Mutex` 并非必需。真正的 Tokio
    // 在这里不使用 mutex，但真正的 Tokio 的代码行数
    // 超过单页教程能容纳的范围。
    task_future: Mutex<TaskFuture>,
    executor: mpsc::Sender<Arc<Task>>,
}

impl Task {
    fn schedule(self: &Arc<Self>) {
        self.executor.send(self.clone());
    }
}
```

要调度任务，克隆 `Arc` 并通过 channel 发送。现在，我们需要将 `schedule` 函数与 [`std::task::Waker`][`Waker`] 挂钩。标准库提供了使用[手动 vtable 构造][vtable]的低级 API。这种策略为实现者提供最大灵活性，但需要大量 unsafe 样板代码。我们不直接使用 [`RawWakerVTable`][vtable]，而是使用 [`futures`] crate 提供的 [`ArcWake`] 工具。这允许我们实现一个简单的 trait，将 `Task` 结构体暴露为 waker。

在 `Cargo.toml` 中添加以下依赖以引入 `futures`：

```toml
futures = "0.3"
```

然后实现 [`futures::task::ArcWake`][`ArcWake`]。

```rust
use futures::task::{self, ArcWake};
use std::sync::Arc;
# struct Task {}
# impl Task {
#     fn schedule(self: &Arc<Self>) {}
# }
impl ArcWake for Task {
    fn wake_by_ref(arc_self: &Arc<Self>) {
        arc_self.schedule();
    }
}
```

当上面的定时器线程调用 `waker.wake()` 时，任务被推入 channel。接下来，我们在 `MiniTokio::run()` 函数中实现接收和执行任务。

```rust
# use std::sync::mpsc;
# use futures::task::{self, ArcWake};
# use std::future::Future;
# use std::pin::Pin;
# use std::sync::{Arc, Mutex};
# use std::task::{Context, Poll};
# struct MiniTokio {
#   scheduled: mpsc::Receiver<Arc<Task>>,
#   sender: mpsc::Sender<Arc<Task>>,
# }
# struct TaskFuture {
#     future: Pin<Box<dyn Future<Output = ()> + Send>>,
#     poll: Poll<()>,
# }
# struct Task {
#   task_future: Mutex<TaskFuture>,
#   executor: mpsc::Sender<Arc<Task>>,
# }
# impl ArcWake for Task {
#   fn wake_by_ref(arc_self: &Arc<Self>) {}
# }
impl MiniTokio {
    fn run(&self) {
        while let Ok(task) = self.scheduled.recv() {
            task.poll();
        }
    }

    /// 初始化新的 mini-tokio 实例
    fn new() -> MiniTokio {
        let (sender, scheduled) = mpsc::channel();

        MiniTokio { scheduled, sender }
    }

    /// 将 future spawn 到 mini-tokio 实例上
    ///
    /// 给定的 future 用 `Task` 包装并推入
    /// `scheduled` 队列。调用 `run` 时将执行该 future
    fn spawn<F>(&self, future: F)
    where
        F: Future<Output = ()> + Send + 'static,
    {
        Task::spawn(future, &self.sender);
    }
}

impl TaskFuture {
    fn new(future: impl Future<Output = ()> + Send + 'static) -> TaskFuture {
        TaskFuture {
            future: Box::pin(future),
            poll: Poll::Pending,
        }
    }

    fn poll(&mut self, cx: &mut Context<'_>) {
        // 允许虚假唤醒，即使在 future 已
        // 返回 `Ready` 之后也是如此。但是，对已
        // 返回 `Ready` 的 future 再次 poll 是
        // *不允许*的。因此我们需要在调用之前
        // 检查 future 是否仍处于 pending 状态。
        // 不这样做可能导致 panic。
        if self.poll.is_pending() {
            self.poll = self.future.as_mut().poll(cx);
        }
    }
}

impl Task {
    fn poll(self: Arc<Self>) {
        // 从 `Task` 实例创建 waker。
        // 使用上面的 `ArcWake` 实现。
        let waker = task::waker(self.clone());
        let mut cx = Context::from_waker(&waker);

        // 没有其他线程尝试锁定 task_future
        let mut task_future = self.task_future.try_lock().unwrap();

        // poll 内部 future
        task_future.poll(&mut cx);
    }

    // 用给定 future spawn 新任务。
    //
    // 初始化包含给定 future 的新 Task 包装，
    // 并将其推入 `sender`。channel 的接收端
    // 会获取任务并执行。
    fn spawn<F>(future: F, sender: &mpsc::Sender<Arc<Task>>)
    where
        F: Future<Output = ()> + Send + 'static,
    {
        let task = Arc::new(Task {
            task_future: Mutex::new(TaskFuture::new(future)),
            executor: sender.clone(),
        });

        let _ = sender.send(task);
    }
}
```

这里发生了多件事。首先实现了 `MiniTokio::run()`。该函数在循环中从 channel 接收已调度的任务。由于任务在被 wake 时推入 channel，执行这些任务时它们能够取得进展。

此外，`MiniTokio::new()` 和 `MiniTokio::spawn()` 调整为使用 channel 而非 `VecDeque`。spawn 新任务时，会给它们一份 channel 发送端的克隆，任务可以用它将自己调度到运行时上。

`Task::poll()` 函数使用 `futures` crate 的 [`ArcWake`] 工具创建 waker。waker 用于创建 `task::Context`。该 `task::Context` 被传给 `poll`。

# 总结

我们现在已经看到了异步 Rust 如何端到端工作的完整示例。Rust 的 `async/await` 特性由 trait 支撑。这使得 Tokio 等第三方 crate 能够提供执行细节。

* 异步 Rust 操作是惰性的，需要调用者 poll 它们。
* Waker 被传给 future，将 future 与调用它的任务关联起来。
* 当资源**未**准备好完成操作时，返回 `Poll::Pending`，并记录任务的 waker。
* 当资源变为就绪时，通知任务的 waker。
* 执行器收到通知并调度任务执行。
* 再次 poll 任务，此时资源已就绪，任务取得进展。

# 一些遗留问题

回想实现 `Delay` future 时，我们说还有几件事要修复。Rust 的异步模型允许单个 future 在执行过程中迁移到不同任务。考虑以下情况：

```rust
use futures::future::poll_fn;
use std::future::Future;
use std::pin::Pin;
# use std::task::{Context, Poll};
# use std::time::{Duration, Instant};
# struct Delay { when: Instant }
# impl Future for Delay {
#   type Output = ();
#   fn poll(self: Pin<&mut Self>, _cx: &mut Context<'_>) -> Poll<()> {
#       Poll::Pending
#   }
# }

#[tokio::main]
async fn main() {
    let when = Instant::now() + Duration::from_millis(10);
    let mut delay = Some(Delay { when });

    poll_fn(move |cx| {
        let mut delay = delay.take().unwrap();
        let res = Pin::new(&mut delay).poll(cx);
        assert!(res.is_pending());
        tokio::spawn(async move {
            delay.await;
        });

        Poll::Ready(())
    }).await;
}
```

`poll_fn` 函数使用闭包创建 `Future` 实例。上面的片段创建了一个 `Delay` 实例，poll 一次，然后将 `Delay` 实例发送到新任务中 await。在这个例子中，`Delay::poll` 被用**不同**的 `Waker` 实例调用了多次。发生这种情况时，你必须确保对*最近一次* `poll` 调用传入的 `Waker` 调用 `wake`。

实现 future 时，必须假设每次 `poll` 调用**可能**提供不同的 `Waker` 实例。`poll` 函数必须用新的 waker 更新之前记录的 waker。

我们之前对 `Delay` 的实现每次被 poll 都会 spawn 一个新线程。这没问题，但如果 poll 过于频繁（例如，如果你 `select!` 该 future 和另一个 future，每当任一者有事件时两者都会被 poll），可能非常低效。一种做法是先记住是否已 spawn 线程，只有尚未 spawn 时才 spawn 新线程。然而如果这样做，必须确保在后续 `poll` 调用时更新线程的 `Waker`，否则你就没有 wake 最新的 `Waker`。

要修复我们之前的实现，可以这样做：

```rust
use std::future::Future;
use std::pin::Pin;
use std::sync::{Arc, Mutex};
use std::task::{Context, Poll, Waker};
use std::thread;
use std::time::{Duration, Instant};

struct Delay {
    when: Instant,
    // 已 spawn 线程时为 Some，否则为 None
    waker: Option<Arc<Mutex<Waker>>>,
}

impl Future for Delay {
    type Output = ();

    fn poll(mut self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<()> {
        // 检查当前时刻。如果持续时间已过，
        // 则该 future 已完成，返回 `Poll::Ready`
        if Instant::now() >= self.when {
            return Poll::Ready(());
        }

        // 持续时间尚未过去。如果是 future 第一次
        // 被调用，则 spawn 定时器线程。如果定时器
        // 线程已在运行，确保存储的 `Waker` 与
        // 当前任务的 waker 一致
        if let Some(waker) = &self.waker {
            let mut waker = waker.lock().unwrap();

            // 检查存储的 waker 是否与当前任务的 waker 一致。
            // 这是必要的，因为 `Delay` future 实例可能在
            // 两次 `poll` 调用之间移动到不同任务。如果发生
            // 这种情况，给定 `Context` 中的 waker 会不同，
            // 我们必须更新存储的 waker 以反映这一变化
            if !waker.will_wake(cx.waker()) {
                *waker = cx.waker().clone();
            }
        } else {
            let when = self.when;
            let waker = Arc::new(Mutex::new(cx.waker().clone()));
            self.waker = Some(waker.clone());

            // 这是 `poll` 第一次被调用，spawn 定时器线程
            thread::spawn(move || {
                let now = Instant::now();

                if now < when {
                    thread::sleep(when - now);
                }

                // 持续时间已过。通过调用 waker
                // 通知调用者
                let waker = waker.lock().unwrap();
                waker.wake_by_ref();
            });
        }

        // 此时 waker 已存储，定时器线程已启动。
        // 持续时间尚未过去（回想我们最先检查了这一点），
        // 因此 future 尚未完成，必须返回 `Poll::Pending`。
        //
        // `Future` trait 契约要求：返回 `Pending` 时，
        // future 必须确保在应再次 poll 时发出给定 waker
        // 的信号。在本例中，通过在这里返回 `Pending`，
        // 我们承诺在请求的持续时间过去后，会调用
        // `Context` 参数中包含的 waker。我们通过上面
        // spawn 定时器线程来保证这一点。
        //
        // 如果忘记调用 waker，任务将无限期挂起
        Poll::Pending
    }
}
```

这有点复杂，但思路是：每次 `poll` 时，future 检查传入的 waker 是否与之前记录的 waker 一致。如果一致，则无需做其他事。如果不一致，则必须更新记录的 waker。

## `Notify` 工具

我们演示了如何用手写 waker 实现 `Delay` future。Waker 是异步 Rust 工作方式的基础。通常不必降到那个层次。例如，对于 `Delay`，我们可以完全用 `async/await` 实现，使用 [`tokio::sync::Notify`][notify] 工具。该工具提供基本的任务通知机制。它处理 waker 的细节，包括确保记录的 waker 与当前任务一致。

使用 [`Notify`][notify]，我们可以这样用 `async/await` 实现 `delay` 函数：

```rust
use tokio::sync::Notify;
use std::sync::Arc;
use std::time::{Duration, Instant};
use std::thread;

async fn delay(dur: Duration) {
    let when = Instant::now() + dur;
    let notify = Arc::new(Notify::new());
    let notify_clone = notify.clone();

    thread::spawn(move || {
        let now = Instant::now();

        if now < when {
            thread::sleep(when - now);
        }

        notify_clone.notify_one();
    });


    notify.notified().await;
}
```

[assoc]: https://doc.rust-lang.org/book/ch19-03-advanced-traits.html#specifying-placeholder-types-in-trait-definitions-with-associated-types
[trait]: https://doc.rust-lang.org/std/future/trait.Future.html
[pin]: https://doc.rust-lang.org/std/pin/index.html
[`Waker`]: https://doc.rust-lang.org/std/task/struct.Waker.html
[mini-tokio]: https://github.com/tokio-rs/website/blob/master/tutorial-code/mini-tokio/src/main.rs
[vtable]: https://doc.rust-lang.org/std/task/struct.RawWakerVTable.html
[`ArcWake`]: https://docs.rs/futures/0.3/futures/task/trait.ArcWake.html
[`futures`]: https://docs.rs/futures/
[notify]: https://docs.rs/tokio/1/tokio/sync/struct.Notify.html
