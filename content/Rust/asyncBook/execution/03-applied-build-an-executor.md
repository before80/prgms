+++
title = "20.3-实践：构建执行器"
date = 2026-08-22T19:00:00+08:00
weight = 29
type = "docs"
description = "实践：构建执行器"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Asynchronous Programming in Rust](https://rust-lang.github.io/async-book/)

# 实践：构建执行器 {#applied-build-an-executor}


> 原文链接: [https://rust-lang.github.io/async-book/02_execution/04_executor.html](https://rust-lang.github.io/async-book/02_execution/04_executor.html)


Rust 的 `Future` 是惰性的：除非被主动驱动至完成，否则不会做任何事。将 future 驱动至完成的一种方式是在 `async` 函数内 `.await` 它，但这只是把问题上移一层：谁来运行顶层 `async` 函数返回的 future？答案是我们需要 `Future` 执行器。

`Future` 执行器接收一组顶层 `Future`，并在 `Future` 可以推进时通过调用 `poll` 将它们运行至完成。通常，执行器会先 poll 一次 future 以启动。当 `Future` 通过调用 `wake()` 表明已准备好推进时，它们会被放回队列并再次 poll，如此重复直到 `Future` 完成。

本节中，我们将编写自己的简单执行器，能够并发地将大量顶层 future 运行至完成。

在本示例中，我们依赖 `futures` crate 的 `ArcWake` trait，它提供了一种简便方式构造 `Waker`。编辑 `Cargo.toml` 添加新依赖：

```toml
[package]
name = "timer_future"
version = "0.1.0"
authors = ["XYZ Author"]
edition = "2021"

[dependencies]
futures = "0.3"
```

接下来，我们需要在 `src/main.rs` 顶部添加以下导入：

```rust,ignore
use futures::{
    future::{BoxFuture, FutureExt},
    task::{waker_ref, ArcWake},
};
use std::{
    future::Future,
    sync::mpsc::{sync_channel, Receiver, SyncSender},
    sync::{Arc, Mutex},
    task::Context,
    time::Duration,
};
// The timer we wrote in the previous section:
use timer_future::TimerFuture;
```

我们的执行器通过通道发送要运行的任务来工作。执行器从通道取出事件并运行它们。当任务准备好做更多工作（被唤醒）时，它可以通过将自己放回通道来安排再次被 poll。

在此设计中，执行器本身只需要任务通道的接收端。用户将获得发送端以便生成新 future。任务本身只是可以重新调度自己的 future，因此我们将它们存储为 future 与任务可用于重新入队的 sender 的配对。

```rust,ignore
/// Task executor that receives tasks off of a channel and runs them.
struct Executor {
    ready_queue: Receiver<Arc<Task>>,
}

/// `Spawner` spawns new futures onto the task channel.
#[derive(Clone)]
struct Spawner {
    task_sender: SyncSender<Arc<Task>>,
}

/// A future that can reschedule itself to be polled by an `Executor`.
struct Task {
    /// In-progress future that should be pushed to completion.
    ///
    /// The `Mutex` is not necessary for correctness, since we only have
    /// one thread executing tasks at once. However, Rust isn't smart
    /// enough to know that `future` is only mutated from one thread,
    /// so we need to use the `Mutex` to prove thread-safety. A production
    /// executor would not need this, and could use `UnsafeCell` instead.
    future: Mutex<Option<BoxFuture<'static, ()>>>,

    /// Handle to place the task itself back onto the task queue.
    task_sender: SyncSender<Arc<Task>>,
}

fn new_executor_and_spawner() -> (Executor, Spawner) {
    // Maximum number of tasks to allow queueing in the channel at once.
    // This is just to make `sync_channel` happy, and wouldn't be present in
    // a real executor.
    const MAX_QUEUED_TASKS: usize = 10_000;
    let (task_sender, ready_queue) = sync_channel(MAX_QUEUED_TASKS);
    (Executor { ready_queue }, Spawner { task_sender })
}
```

让我们也为 spawner 添加一个方法，以便轻松生成新 future。该方法接收 future 类型，将其装箱，并创建包含它的新 `Arc<Task>`，可入队到执行器上。

```rust,ignore
impl Spawner {
    fn spawn(&self, future: impl Future<Output = ()> + 'static + Send) {
        let future = future.boxed();
        let task = Arc::new(Task {
            future: Mutex::new(Some(future)),
            task_sender: self.task_sender.clone(),
        });
        self.task_sender.try_send(task).expect("too many tasks queued");
    }
}
```

要 poll future，我们需要创建 `Waker`。如[任务唤醒一节]所讨论，`Waker` 负责在调用 `wake` 后安排任务再次被 poll。请记住，`Waker` 告知执行器恰好哪个任务已就绪，使它们能只 poll 已准备好推进的 future。创建新 `Waker` 的最简单方式是实现 `ArcWake` trait，然后使用 `waker_ref` 或 `.into_waker()` 将 `Arc<impl ArcWake>` 转为 `Waker`。让我们为任务实现 `ArcWake`，使它们可转为 `Waker` 并被唤醒：

```rust,ignore
impl ArcWake for Task {
    fn wake_by_ref(arc_self: &Arc<Self>) {
        // Implement `wake` by sending this task back onto the task channel
        // so that it will be polled again by the executor.
        let cloned = arc_self.clone();
        arc_self
            .task_sender
            .try_send(cloned)
            .expect("too many tasks queued");
    }
}
```

当从 `Arc<Task>` 创建 `Waker` 时，对其调用 `wake()` 会导致 `Arc` 的副本被发送到任务通道。我们的执行器随后需要取出任务并 poll 它。我们来实现这一点：

```rust,ignore
impl Executor {
    fn run(&self) {
        while let Ok(task) = self.ready_queue.recv() {
            // Take the future, and if it has not yet completed (is still Some),
            // poll it in an attempt to complete it.
            let mut future_slot = task.future.lock().unwrap();
            if let Some(mut future) = future_slot.take() {
                // Create a `LocalWaker` from the task itself
                let waker = waker_ref(&task);
                let context = &mut Context::from_waker(&waker);
                // `BoxFuture<T>` is a type alias for
                // `Pin<Box<dyn Future<Output = T> + Send + 'static>>`.
                // We can get a `Pin<&mut dyn Future + Send + 'static>`
                // from it by calling the `Pin::as_mut` method.
                if future.as_mut().poll(context).is_pending() {
                    // We're not done processing the future, so put it
                    // back in its task to be run again in the future.
                    *future_slot = Some(future);
                }
            }
        }
    }
}
```

恭喜！我们现在有了一个可用的 future 执行器。我们甚至可以用它运行 `async/.await` 代码和自定义 future，例如我们之前编写的 `TimerFuture`：

```rust,edition2018,ignore
fn main() {
    let (executor, spawner) = new_executor_and_spawner();

    // Spawn a task to print before and after waiting on a timer.
    spawner.spawn(async {
        println!("howdy!");
        // Wait for our timer future to complete after two seconds.
        TimerFuture::new(Duration::new(2, 0)).await;
        println!("done!");
    });

    // Drop the spawner so that our executor knows it is finished and won't
    // receive more incoming tasks to run.
    drop(spawner);

    // Run the executor until the task queue is empty.
    // This will print "howdy!", pause, and then print "done!".
    executor.run();
}
```

[task wakeups section]: ../02-task-wakeups-with-waker/