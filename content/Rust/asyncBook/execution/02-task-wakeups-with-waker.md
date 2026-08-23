+++
title = "20.2-使用 Waker 唤醒 Task"
date = 2026-08-22T19:00:00+08:00
weight = 28
type = "docs"
description = "使用 Waker 唤醒 Task"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Asynchronous Programming in Rust](https://rust-lang.github.io/async-book/)

# 使用 Waker 唤醒 Task {#task-wakeups-with-waker}


> 原文链接: [https://rust-lang.github.io/async-book/02_execution/03_wakeups.html](https://rust-lang.github.io/async-book/02_execution/03_wakeups.html)


Future 在第一次被 `poll` 时往往无法完成。此时，future 需要确保在准备好继续推进时再次被 poll。这通过 `Waker` 类型完成。

每次 poll future 时，它都是作为「任务」的一部分被 poll 的。任务是已提交给执行器的顶层 future。

`Waker` 提供 `wake()` 方法，可用于告知执行器应唤醒关联任务。当 `wake()` 被调用时，执行器知道与 `Waker` 关联的任务已准备好推进，应再次 poll 其 future。

`Waker` 还实现了 `clone()`，因此可以复制并在各处存储。

让我们尝试使用 `Waker` 实现一个简单的定时器 future。

## 实践：构建定时器

为示例起见，我们仅在创建定时器时启动新线程，休眠所需时间，然后在时间窗口结束后通知定时器 future。

首先，用 `cargo new --lib timer_future` 启动新项目，并在 `src/lib.rs` 中添加我们需要的导入：

```rust
use std::{
    future::Future,
    pin::Pin,
    sync::{Arc, Mutex},
    task::{Context, Poll, Waker},
    thread,
    time::Duration,
};
```

首先定义 future 类型本身。我们的 future 需要一种方式让线程通信定时器已到期、future 应完成。我们将使用共享的 `Arc<Mutex<..>>` 值在线程与 future 之间通信。

```rust,ignore
pub struct TimerFuture {
    shared_state: Arc<Mutex<SharedState>>,
}

/// Shared state between the future and the waiting thread
struct SharedState {
    /// Whether or not the sleep time has elapsed
    completed: bool,

    /// The waker for the task that `TimerFuture` is running on.
    /// The thread can use this after setting `completed = true` to tell
    /// `TimerFuture`'s task to wake up, see that `completed = true`, and
    /// move forward.
    waker: Option<Waker>,
}
```

现在，我们来编写 `Future` 实现！

```rust,ignore
impl Future for TimerFuture {
    type Output = ();
    fn poll(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Self::Output> {
        // Look at the shared state to see if the timer has already completed.
        let mut shared_state = self.shared_state.lock().unwrap();
        if shared_state.completed {
            Poll::Ready(())
        } else {
            // Set waker so that the thread can wake up the current task
            // when the timer has completed, ensuring that the future is polled
            // again and sees that `completed = true`.
            //
            // It's tempting to do this once rather than repeatedly cloning
            // the waker each time. However, the `TimerFuture` can move between
            // tasks on the executor, which could cause a stale waker pointing
            // to the wrong task, preventing `TimerFuture` from waking up
            // correctly.
            //
            // N.B. it's possible to check for this using the `Waker::will_wake`
            // function, but we omit that here to keep things simple.
            shared_state.waker = Some(cx.waker().clone());
            Poll::Pending
        }
    }
}
```

很简单，对吧？若线程已将 `shared_state.completed = true`，我们就完成了！否则，我们克隆当前任务的 `Waker` 并传给 `shared_state.waker`，以便线程可以唤醒任务。

重要的是，我们必须在每次 poll future 时更新 `Waker`，因为 future 可能已移动到具有不同 `Waker` 的另一任务。当 future 在被 poll 后在任务之间传递时会发生这种情况。

最后，我们需要实际构造定时器并启动线程的 API：

```rust,ignore
impl TimerFuture {
    /// Create a new `TimerFuture` which will complete after the provided
    /// timeout.
    pub fn new(duration: Duration) -> Self {
        let shared_state = Arc::new(Mutex::new(SharedState {
            completed: false,
            waker: None,
        }));

        // Spawn the new thread
        let thread_shared_state = shared_state.clone();
        thread::spawn(move || {
            thread::sleep(duration);
            let mut shared_state = thread_shared_state.lock().unwrap();
            // Signal that the timer has completed and wake up the last
            // task on which the future was polled, if one exists.
            shared_state.completed = true;
            if let Some(waker) = shared_state.waker.take() {
                waker.wake()
            }
        });

        TimerFuture { shared_state }
    }
}
```

太好了！构建简单定时器 future 所需的就这些了。现在，要是我们有个执行器来运行该 future 就好了……
