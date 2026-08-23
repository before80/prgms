+++
title = "10 流"
date = 2026-08-23T16:54:00+08:00
weight = 11
type = "docs"
description = ""
isCJKLanguage = true
draft = false

+++


> 原文链接: [https://tokio.rs/tokio/tutorial/streams](https://tokio.rs/tokio/tutorial/streams)

流（stream）是一系列异步产生的值。它是 Rust [`std::iter::Iterator`][iter] 的异步等价物，由 [`Stream`] trait 表示。流可以在 `async` 函数中迭代，也可以使用适配器进行转换。Tokio 在 [`StreamExt`] trait 上提供了许多常用适配器。

<!--
TODO: bring back once true again?
Tokio provides stream support under the `stream` feature flag. When depending on
Tokio, include either `stream` or `full` to get access to this functionality.
-->

Tokio 在单独的 crate `tokio-stream` 中提供流支持。

```toml
tokio-stream = "0.1"
```

> **info**
> 目前，Tokio 的 Stream 工具位于 `tokio-stream` crate 中。
> 一旦 `Stream` trait 在 Rust 标准库中稳定，`tokio` crate 将承载 Tokio 的流工具。

<!--
TODO: uncomment this once it is true again.
A number of types we've already seen also implement [`Stream`]. For example, the
receive half of a [`mpsc::Receiver`][rx] implements [`Stream`]. The
[`AsyncBufReadExt::lines()`] method takes a buffered I/O reader and returns a
[`Stream`] where each value represents a line of data.
-->


目前，Rust 编程语言不支持异步 `for` 循环。
相反，迭代流使用 `while let` 循环配合 [`StreamExt::next()`][next]。

```rust
use tokio_stream::StreamExt;

#[tokio::main]
async fn main() {
    let mut stream = tokio_stream::iter(&[1, 2, 3]);

    while let Some(v) = stream.next().await {
        println!("GOT = {:?}", v);
    }
}
```

与迭代器类似，`next()` 方法返回 `Option<T>`，其中 `T` 是流的值类型。收到 `None` 表示流迭代已结束。

## Mini-Redis 广播

让我们通过一个使用 Mini-Redis 客户端的稍复杂示例来说明。

完整代码见[此处][full]。

[full]: https://github.com/tokio-rs/website/blob/master/tutorial-code/streams/src/main.rs

```rust
use tokio_stream::StreamExt;
use mini_redis::client;

async fn publish() -> mini_redis::Result<()> {
    let mut client = client::connect("127.0.0.1:6379").await?;

    // 发布一些数据
    client.publish("numbers", "1".into()).await?;
    client.publish("numbers", "two".into()).await?;
    client.publish("numbers", "3".into()).await?;
    client.publish("numbers", "four".into()).await?;
    client.publish("numbers", "five".into()).await?;
    client.publish("numbers", "6".into()).await?;
    Ok(())
}

async fn subscribe() -> mini_redis::Result<()> {
    let client = client::connect("127.0.0.1:6379").await?;
    let subscriber = client.subscribe(vec!["numbers".to_string()]).await?;
    let messages = subscriber.into_stream();

    tokio::pin!(messages);

    while let Some(msg) = messages.next().await {
        println!("got = {:?}", msg);
    }

    Ok(())
}

# fn dox() {
#[tokio::main]
async fn main() -> mini_redis::Result<()> {
    tokio::spawn(async {
        publish().await
    });

    subscribe().await?;

    println!("DONE");

    Ok(())
}
# }
```

一个任务被生成，向 Mini-Redis 服务器的 "numbers" 通道发布消息。然后，在主任务上，我们订阅 "numbers" 通道并显示收到的消息。

订阅后，对返回的 subscriber 调用 [`into_stream()`]。这会消费 `Subscriber`，返回一个在消息到达时产生消息的流。在开始迭代消息之前，注意该流使用 [`tokio::pin!`] 被[固定][pin]到栈上。对流调用 `next()` 要求流被[固定][pin]。`into_stream()` 函数返回的流*未*被固定，我们必须显式固定它才能迭代。

> **info**
> 当 Rust 值在内存中不能再被移动时，它就被「固定」了。固定值的一个关键性质是，可以取得指向固定数据的指针，且调用方可以确信该指针保持有效。`async/await` 利用这一特性来支持在 `.await` 点之间借用数据。

如果我们忘记固定流，会得到类似这样的错误：

```text
error[E0277]: `from_generator::GenFuture<[static generator@Subscriber::into_stream::{closure#0} for<'r, 's, 't0, 't1, 't2, 't3, 't4, 't5, 't6> {ResumeTy, &'r mut Subscriber, Subscriber, impl Future, (), std::result::Result<Option<Message>, Box<(dyn std::error::Error + Send + Sync + 't0)>>, Box<(dyn std::error::Error + Send + Sync + 't1)>, &'t2 mut async_stream::yielder::Sender<std::result::Result<Message, Box<(dyn std::error::Error + Send + Sync + 't3)>>>, async_stream::yielder::Sender<std::result::Result<Message, Box<(dyn std::error::Error + Send + Sync + 't4)>>>, std::result::Result<Message, Box<(dyn std::error::Error + Send + Sync + 't5)>>, impl Future, Option<Message>, Message}]>` cannot be unpinned
  --> streams/src/main.rs:29:36
   |
29 |     while let Some(msg) = messages.next().await {
   |                                    ^^^^ within `tokio_stream::filter::_::__Origin<'_, impl Stream, [closure@streams/src/main.rs:22:17: 25:10]>`, the trait `Unpin` is not implemented for `from_generator::GenFuture<[static generator@Subscriber::into_stream::{closure#0} for<'r, 's, 't0, 't1, 't2, 't3, 't4, 't5, 't6> {ResumeTy, &'r mut Subscriber, Subscriber, impl Future, (), std::result::Result<Option<Message>, Box<(dyn std::error::Error + Send + Sync + 't0)>>, Box<(dyn std::error::Error + Send + Sync + 't1)>, &'t2 mut async_stream::yielder::Sender<std::result::Result<Message, Box<(dyn std::error::Error + Send + Sync + 't3)>>>, async_stream::yielder::Sender<std::result::Result<Message, Box<(dyn std::error::Error + Send + Sync + 't4)>>>, std::result::Result<Message, Box<(dyn std::error::Error + Send + Sync + 't5)>>, impl Future, Option<Message>, Message}]>`
   |
   = note: required because it appears within the type `impl Future`
   = note: required because it appears within the type `async_stream::async_stream::AsyncStream<std::result::Result<Message, Box<(dyn std::error::Error + Send + Sync + 'static)>>, impl Future>`
   = note: required because it appears within the type `impl Stream`
   = note: required because it appears within the type `tokio_stream::filter::_::__Origin<'_, impl Stream, [closure@streams/src/main.rs:22:17: 25:10]>`
   = note: required because of the requirements on the impl of `Unpin` for `tokio_stream::filter::Filter<impl Stream, [closure@streams/src/main.rs:22:17: 25:10]>`
   = note: required because it appears within the type `tokio_stream::map::_::__Origin<'_, tokio_stream::filter::Filter<impl Stream, [closure@streams/src/main.rs:22:17: 25:10]>, [closure@streams/src/main.rs:26:14: 26:40]>`
   = note: required because of the requirements on the impl of `Unpin` for `tokio_stream::map::Map<tokio_stream::filter::Filter<impl Stream, [closure@streams/src/main.rs:22:17: 25:10]>, [closure@streams/src/main.rs:26:14: 26:40]>`
   = note: required because it appears within the type `tokio_stream::take::_::__Origin<'_, tokio_stream::map::Map<tokio_stream::filter::Filter<impl Stream, [closure@streams/src/main.rs:22:17: 25:10]>, [closure@streams/src/main.rs:26:14: 26:40]>>`
   = note: required because of the requirements on the impl of `Unpin` for `tokio_stream::take::Take<tokio_stream::map::Map<tokio_stream::filter::Filter<impl Stream, [closure@streams/src/main.rs:22:17: 25:10]>, [closure@streams/src/main.rs:26:14: 26:40]>>`
```

如果你遇到类似这样的错误消息，试试固定该值！

在运行之前，先启动 Mini-Redis 服务器：

```bash
$ mini-redis-server
```

然后尝试运行代码。我们会看到消息输出到 STDOUT。

```text
got = Ok(Message { channel: "numbers", content: b"1" })
got = Ok(Message { channel: "numbers", content: b"two" })
got = Ok(Message { channel: "numbers", content: b"3" })
got = Ok(Message { channel: "numbers", content: b"four" })
got = Ok(Message { channel: "numbers", content: b"five" })
got = Ok(Message { channel: "numbers", content: b"6" })
```

由于订阅和发布之间存在竞争，一些早期消息可能会丢失。程序永远不会退出。对 Mini-Redis 通道的订阅会一直保持活跃，直到服务器仍在运行。

让我们看看如何使用流来扩展这个程序。

# 适配器

接受 [`Stream`] 并返回另一个 [`Stream`] 的函数通常称为「流适配器」，它们是「适配器模式」的一种形式。常见的流适配器包括 [`map`]、[`take`] 和 [`filter`]。

让我们更新 Mini-Redis 示例以便程序能够退出。收到三条消息后，停止迭代消息。这通过 [`take`] 实现。该适配器将流限制为**最多**产生 `n` 条消息。

```rust
# use mini_redis::client;
# use tokio_stream::StreamExt;
# async fn subscribe() -> mini_redis::Result<()> {
#    let client = client::connect("127.0.0.1:6379").await?;
#    let subscriber = client.subscribe(vec!["numbers".to_string()]).await?;
let messages = subscriber
    .into_stream()
    .take(3);
#     Ok(())
# }
```

再次运行程序，我们会得到：

```text
got = Ok(Message { channel: "numbers", content: b"1" })
got = Ok(Message { channel: "numbers", content: b"two" })
got = Ok(Message { channel: "numbers", content: b"3" })
```

这次程序会结束。

现在，让我们将流限制为个位数。我们通过检查消息长度来判断。我们使用 [`filter`] 适配器丢弃任何不匹配谓词的消息。

```rust
# use mini_redis::client;
# use tokio_stream::StreamExt;
# async fn subscribe() -> mini_redis::Result<()> {
#    let client = client::connect("127.0.0.1:6379").await?;
#    let subscriber = client.subscribe(vec!["numbers".to_string()]).await?;
let messages = subscriber
    .into_stream()
    .filter(|msg| match msg {
        Ok(msg) if msg.content.len() == 1 => true,
        _ => false,
    })
    .take(3);
#     Ok(())
# }
```

再次运行程序，我们会得到：

```text
got = Ok(Message { channel: "numbers", content: b"1" })
got = Ok(Message { channel: "numbers", content: b"3" })
got = Ok(Message { channel: "numbers", content: b"6" })
```

注意适配器应用的顺序很重要。先 `filter` 再 `take` 与先 `take` 再 `filter` 是不同的。

最后，我们通过剥离输出中的 `Ok(Message { ... })` 部分来整理输出。这通过 [`map`] 完成。由于这是在 `filter` **之后**应用的，我们知道消息是 `Ok`，因此可以使用 `unwrap()`。

```rust
# use mini_redis::client;
# use tokio_stream::StreamExt;
# async fn subscribe() -> mini_redis::Result<()> {
#    let client = client::connect("127.0.0.1:6379").await?;
#    let subscriber = client.subscribe(vec!["numbers".to_string()]).await?;
let messages = subscriber
    .into_stream()
    .filter(|msg| match msg {
        Ok(msg) if msg.content.len() == 1 => true,
        _ => false,
    })
    .map(|msg| msg.unwrap().content)
    .take(3);
#     Ok(())
# }
```

现在，输出为：

```text
got = b"1"
got = b"3"
got = b"6"
```

另一种选择是使用 [`filter_map`] 将 [`filter`] 和 [`map`] 步骤合并为一次调用。

还有更多可用适配器。完整列表见[此处][`StreamExt`]。

# 实现 `Stream`

[`Stream`] trait 与 [`Future`] trait 非常相似。

```rust
use std::pin::Pin;
use std::task::{Context, Poll};

pub trait Stream {
    type Item;

    fn poll_next(
        self: Pin<&mut Self>, 
        cx: &mut Context<'_>
    ) -> Poll<Option<Self::Item>>;

    fn size_hint(&self) -> (usize, Option<usize>) {
        (0, None)
    }
}
```

`Stream::poll_next()` 函数很像 `Future::poll`，只不过它可以被反复调用以从流中接收多个值。正如我们在 [深入 async][async] 中所见，当流**尚未**准备好返回值时，会返回 `Poll::Pending`。任务的 waker 会被注册。一旦流应该再次被轮询，waker 会收到通知。

`size_hint()` 方法的用法与[迭代器][iter]中的相同。

通常，手动实现 `Stream` 是通过组合 future 和其他流来完成的。作为示例，让我们在 [深入 async][async] 中实现的 `Delay` future 基础上构建。我们将把它转换为一个流，以 10 ms 的间隔产生三次 `()`。

```rust
use tokio_stream::Stream;
# use std::future::Future;
use std::pin::Pin;
use std::task::{Context, Poll};
use std::time::Duration;
# use std::time::Instant;

struct Interval {
    rem: usize,
    delay: Delay,
}
# struct Delay { when: Instant }
# impl Future for Delay {
#   type Output = ();
#   fn poll(self: Pin<&mut Self>, _cx: &mut Context<'_>) -> Poll<()> {
#       Poll::Pending
#   }  
# }

impl Interval {
    fn new() -> Self {
        Self {
            rem: 3,
            delay: Delay { when: Instant::now() }
        }
    }
}

impl Stream for Interval {
    type Item = ();

    fn poll_next(mut self: Pin<&mut Self>, cx: &mut Context<'_>)
        -> Poll<Option<()>>
    {
        if self.rem == 0 {
            // 没有更多延迟
            return Poll::Ready(None);
        }

        match Pin::new(&mut self.delay).poll(cx) {
            Poll::Ready(_) => {
                let when = self.delay.when + Duration::from_millis(10);
                self.delay = Delay { when };
                self.rem -= 1;
                Poll::Ready(Some(()))
            }
            Poll::Pending => Poll::Pending,
        }
    }
}
```

## `async-stream`

使用 [`Stream`] trait 手动实现流可能很繁琐。
遗憾的是，Rust 编程语言尚不支持用于定义流的 `async/await` 语法。相关工作正在进行，但尚未就绪。

[`async-stream`] crate 可作为临时解决方案。该 crate 提供 `stream!` 宏，将输入转换为流。使用这个 crate，上面的 interval 可以这样实现：

```rust
use async_stream::stream;
# use std::future::Future;
# use std::pin::Pin;
# use std::task::{Context, Poll};
# use tokio_stream::StreamExt;
use std::time::{Duration, Instant};

# struct Delay { when: Instant }
# impl Future for Delay {
#   type Output = ();
#   fn poll(self: Pin<&mut Self>, _cx: &mut Context<'_>) -> Poll<()> {
#       Poll::Pending
#   }
# }
# async fn dox() {
# let stream =
stream! {
    let mut when = Instant::now();
    for _ in 0..3 {
        let delay = Delay { when };
        delay.await;
        yield ();
        when += Duration::from_millis(10);
    }
}
# ;
# tokio::pin!(stream);
# while let Some(_) = stream.next().await { }
# }
```

[iter]: https://doc.rust-lang.org/book/ch13-02-iterators.html
[`Stream`]: https://docs.rs/futures-core/0.3/futures_core/stream/trait.Stream.html
[`Future`]: https://doc.rust-lang.org/std/future/trait.Future.html
[`StreamExt`]: https://docs.rs/tokio-stream/0.1/tokio_stream/trait.StreamExt.html
[next]: https://docs.rs/tokio-stream/0.1/tokio_stream/trait.StreamExt.html#method.next
[`map`]: https://docs.rs/tokio-stream/0.1/tokio_stream/trait.StreamExt.html#method.map
[`take`]: https://docs.rs/tokio-stream/0.1/tokio_stream/trait.StreamExt.html#method.take
[`filter`]: https://docs.rs/tokio-stream/0.1/tokio_stream/trait.StreamExt.html#method.filter
[`filter_map`]: https://docs.rs/tokio-stream/0.1/tokio_stream/trait.StreamExt.html#method.filter_map
[pin]: https://doc.rust-lang.org/std/pin/index.html
[async]: ../8-async/
[`async-stream`]: https://docs.rs/async-stream
[`into_stream()`]: https://docs.rs/mini-redis/0.4/mini_redis/client/struct.Subscriber.html#method.into_stream
[`tokio::pin!`]: https://docs.rs/tokio/1/tokio/macro.pin.html
