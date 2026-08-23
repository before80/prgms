+++
title = "20.1-Future trait"
date = 2026-08-22T19:00:00+08:00
weight = 27
type = "docs"
description = "Future trait"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Asynchronous Programming in Rust](https://rust-lang.github.io/async-book/)

# Future trait {#the-future-trait}


> 原文链接: [https://rust-lang.github.io/async-book/02_execution/02_future.html](https://rust-lang.github.io/async-book/02_execution/02_future.html)


`Future` trait 是 Rust 异步编程的核心。`Future` 是一种可产生值（该值可能为空，例如 `()`）的异步计算。*简化版*的 future trait 可能如下所示：

```rust
trait SimpleFuture {
    type Output;
    fn poll(&mut self, wake: fn()) -> Poll<Self::Output>;
}

enum Poll<T> {
    Ready(T),
    Pending,
}
```

可以通过调用 `poll` 函数来推进 Future，该函数会尽可能将 future 驱动至完成。若 future 完成，则返回 `Poll::Ready(result)`。若 future 尚无法完成，则返回 `Poll::Pending`，并安排在该 `Future` 准备好继续推进时调用 `wake()`。当 `wake()` 被调用时，驱动该 `Future` 的执行器会再次调用 `poll`，使 `Future` 继续推进。

没有 `wake()`，执行器将无法知道某个 future 何时可以推进，只能不断 poll 每一个 future。有了 `wake()`，执行器能准确知道哪些 future 已准备好被 `poll`。

例如，考虑从可能已有或尚无可用数据的套接字读取的情况。若有数据，我们可以读取并返回 `Poll::Ready(data)`；若无数据就绪，我们的 future 被阻塞，无法继续推进。当无数据可用时，我们必须注册在套接字上有数据就绪时调用 `wake`，以告知执行器我们的 future 已准备好推进。一个简单的 `SocketRead` future 可能如下所示：

```rust,ignore
pub struct SocketRead<'a> {
    socket: &'a Socket,
}

impl SimpleFuture for SocketRead<'_> {
    type Output = Vec<u8>;

    fn poll(&mut self, wake: fn()) -> Poll<Self::Output> {
        if self.socket.has_data_to_read() {
            // The socket has data -- read it into a buffer and return it.
            Poll::Ready(self.socket.read_buf())
        } else {
            // The socket does not yet have data.
            //
            // Arrange for `wake` to be called once data is available.
            // When data becomes available, `wake` will be called, and the
            // user of this `Future` will know to call `poll` again and
            // receive data.
            self.socket.set_readable_callback(wake);
            Poll::Pending
        }
    }
}
```

这种 `Future` 模型允许组合多个异步操作而无需中间分配。同时运行多个 future 或将 future 链接在一起，可通过无分配的状态机实现，例如：

```rust,ignore
/// A SimpleFuture that runs two other futures to completion concurrently.
///
/// Concurrency is achieved via the fact that calls to `poll` each future
/// may be interleaved, allowing each future to advance itself at its own pace.
pub struct Join<FutureA, FutureB> {
    // Each field may contain a future that should be run to completion.
    // If the future has already completed, the field is set to `None`.
    // This prevents us from polling a future after it has completed, which
    // would violate the contract of the `Future` trait.
    a: Option<FutureA>,
    b: Option<FutureB>,
}

impl<FutureA, FutureB> SimpleFuture for Join<FutureA, FutureB>
where
    FutureA: SimpleFuture<Output = ()>,
    FutureB: SimpleFuture<Output = ()>,
{
    type Output = ();
    fn poll(&mut self, wake: fn()) -> Poll<Self::Output> {
        // Attempt to complete future `a`.
        if let Some(a) = &mut self.a {
            if let Poll::Ready(()) = a.poll(wake) {
                self.a.take();
            }
        }

        // Attempt to complete future `b`.
        if let Some(b) = &mut self.b {
            if let Poll::Ready(()) = b.poll(wake) {
                self.b.take();
            }
        }

        if self.a.is_none() && self.b.is_none() {
            // Both futures have completed -- we can return successfully
            Poll::Ready(())
        } else {
            // One or both futures returned `Poll::Pending` and still have
            // work to do. They will call `wake()` when progress can be made.
            Poll::Pending
        }
    }
}
```

这表明多个 future 如何在不需单独分配的情况下同时运行，从而实现更高效的异步程序。类似地，多个顺序 future 可以一个接一个运行，例如：

```rust,ignore
/// A SimpleFuture that runs two futures to completion, one after another.
//
// Note: for the purposes of this simple example, `AndThenFut` assumes both
// the first and second futures are available at creation-time. The real
// `AndThen` combinator allows creating the second future based on the output
// of the first future, like `get_breakfast.and_then(|food| eat(food))`.
pub struct AndThenFut<FutureA, FutureB> {
    first: Option<FutureA>,
    second: FutureB,
}

impl<FutureA, FutureB> SimpleFuture for AndThenFut<FutureA, FutureB>
where
    FutureA: SimpleFuture<Output = ()>,
    FutureB: SimpleFuture<Output = ()>,
{
    type Output = ();
    fn poll(&mut self, wake: fn()) -> Poll<Self::Output> {
        if let Some(first) = &mut self.first {
            match first.poll(wake) {
                // We've completed the first future -- remove it and start on
                // the second!
                Poll::Ready(()) => self.first.take(),
                // We couldn't yet complete the first future.
                // Notice that we disrupt the flow of the `poll` function with the `return` statement.
                Poll::Pending => return Poll::Pending,
            };
        }
        // Now that the first future is done, attempt to complete the second.
        self.second.poll(wake)
    }
}
```

这些示例展示了 `Future` trait 如何表达异步控制流，而无需多个已分配对象和深层嵌套回调。基本控制流介绍完毕，我们来谈谈真正的 `Future` trait 及其差异。

```rust,ignore
trait Future {
    type Output;
    fn poll(
        // Note the change from `&mut self` to `Pin<&mut Self>`:
        self: Pin<&mut Self>,
        // and the change from `wake: fn()` to `cx: &mut Context<'_>`:
        cx: &mut Context<'_>,
    ) -> Poll<Self::Output>;
}
```

你注意到的第一个变化是 `self` 类型不再是 `&mut Self`，而是变为 `Pin<&mut Self>`。我们将在后续章节更详细地讨论 pinning；目前只需知道它允许我们创建不可移动的 future。不可移动对象可以在其字段之间存储指针，例如 `struct MyFut { a: i32, ptr_to_a: *const i32 }`。Pinning 是启用 async/await 所必需的。

其次，`wake: fn()` 已变为 `&mut Context<'_>`。在 `SimpleFuture` 中，我们使用函数指针（`fn()`）告知 future 执行器应 poll 该 future。然而，由于 `fn()` 只是函数指针，它无法存储有关*哪个* `Future` 调用了 `wake` 的数据。

在实际场景中，像 Web 服务器这样的复杂应用可能有数千个不同连接，其唤醒需要分别管理。`Context` 类型通过提供对 `Waker` 类型值的访问来解决此问题，`Waker` 可用于唤醒特定任务。
