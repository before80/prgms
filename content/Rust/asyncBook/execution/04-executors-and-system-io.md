+++
title = "20.4-执行器与系统 IO"
date = 2026-08-22T19:00:00+08:00
weight = 30
type = "docs"
description = "执行器与系统 IO"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Asynchronous Programming in Rust](https://rust-lang.github.io/async-book/)

# 执行器与系统 IO {#executors-and-system-io}


> 原文链接: [https://rust-lang.github.io/async-book/02_execution/05_io.html](https://rust-lang.github.io/async-book/02_execution/05_io.html)


在上一节[《`Future` Trait》]中，我们讨论了这个在套接字上执行异步读取的 future 示例：

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

该 future 会读取套接字上的可用数据；若无数据可用，它会向执行器让出，请求在套接字再次可读时唤醒其任务。然而，从此示例并不清楚 `Socket` 类型如何实现，特别是 `set_readable_callback` 函数如何工作。我们如何在套接字可读时安排调用 `wake()`？一种选择是让线程持续检查 `socket` 是否可读，并在适当时调用 `wake()`。但这效率很低，每个被阻塞的 IO future 都需要单独线程，会大大降低异步代码的效率。

实践中，此问题通过与 IO 感知的系统阻塞原语集成来解决，例如 Linux 上的 `epoll`、FreeBSD 和 Mac OS 上的 `kqueue`、Windows 上的 IOCP，以及 Fuchsia 上的 `port`（均通过跨平台 Rust crate [`mio`] 暴露）。这些原语都允许线程阻塞在多个异步 IO 事件上，在某个事件完成时返回。实践中，这些 API 通常类似如下：

```rust,ignore
struct IoBlocker {
    /* ... */
}

struct Event {
    // 唯一标识发生且被监听的事件的 ID。
    id: usize,

    // 要等待或已发生的信号集合。
    signals: Signals,
}

impl IoBlocker {
    /// 创建新的异步 IO 事件集合以供阻塞等待。
    fn new() -> Self { /* ... */ }

    /// 表达对特定 IO 事件的兴趣。
    fn add_io_event_interest(
        &self,

        /// 将发生事件的对象
        io_object: &IoObject,

        /// 可能在 `io_object` 上出现、应触发事件的信号集合，
        /// 以及由此兴趣产生的事件 ID。
        event: Event,
    ) { /* ... */ }

    /// 阻塞直到其中一个事件发生。
    fn block(&self) -> Event { /* ... */ }
}

let mut io_blocker = IoBlocker::new();
io_blocker.add_io_event_interest(
    &socket_1,
    Event { id: 1, signals: READABLE },
);
io_blocker.add_io_event_interest(
    &socket_2,
    Event { id: 2, signals: READABLE | WRITABLE },
);
let event = io_blocker.block();

// 例如若 socket 1 变为可读，则打印 "Socket 1 is now READABLE"。
println!("Socket {:?} is now {:?}", event.id, event.signals);
```

Future 执行器可使用这些原语提供异步 IO 对象（如套接字），可配置在特定 IO 事件发生时运行的回调。在我们上面的 `SocketRead` 示例中，`Socket::set_readable_callback` 函数可能类似以下伪代码：

```rust,ignore
impl Socket {
    fn set_readable_callback(&self, waker: Waker) {
        // `local_executor` 是对本地执行器的引用。
        // 可在创建套接字时提供，但实践中许多执行器实现
        // 为方便起见通过线程局部存储传递。
        let local_executor = self.local_executor;

        // 此 IO 对象的唯一 ID。
        let id = self.id;

        // 将本地 waker 存储在执行器的映射中，以便 IO 事件到达时可调用。
        local_executor.event_map.insert(id, waker);
        local_executor.add_io_event_interest(
            &self.socket_file_descriptor,
            Event { id, signals: READABLE },
        );
    }
}
```

我们现在可以只有一个执行器线程，接收并将任何 IO 事件分派给适当的 `Waker`，唤醒对应任务，使执行器在返回检查更多 IO 事件之前驱动更多任务完成（循环继续……）。

[The `Future` Trait]: ../01-the-future-trait/
[`mio`]: https://github.com/tokio-rs/mio
