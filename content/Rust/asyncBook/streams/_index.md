+++
title = "22-Stream"
date = 2026-08-22T19:00:00+08:00
weight = 34
type = "docs"
description = "Stream"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Asynchronous Programming in Rust](https://rust-lang.github.io/async-book/)

# Stream {#streams}


> 原文链接: [https://rust-lang.github.io/async-book/05_streams/01_chapter.html](https://rust-lang.github.io/async-book/05_streams/01_chapter.html)


`Stream` trait 与 `Future` 类似，但可在完成前产生多个值，类似于标准库中的 `Iterator` trait：

```rust,ignore
trait Stream {
    /// The type of the value yielded by the stream.
    type Item;

    /// Attempt to resolve the next item in the stream.
    /// Returns `Poll::Pending` if not ready, `Poll::Ready(Some(x))` if a value
    /// is ready, and `Poll::Ready(None)` if the stream has completed.
    fn poll_next(self: Pin<&mut Self>, cx: &mut Context<'_>)
        -> Poll<Option<Self::Item>>;
}
```

`Stream` 的一个常见示例是 `futures` crate 中 channel 类型的 `Receiver`。每当从 `Sender` 端发送值时，它会产生 `Some(val)`；当 `Sender` 被丢弃且所有待处理消息已接收后，会产生 `None`：

```rust,edition2018,ignore
async fn send_recv() {
    const BUFFER_SIZE: usize = 10;
    let (mut tx, mut rx) = mpsc::channel::<i32>(BUFFER_SIZE);

    tx.send(1).await.unwrap();
    tx.send(2).await.unwrap();
    drop(tx);

    // `StreamExt::next` is similar to `Iterator::next`, but returns a
    // type that implements `Future<Output = Option<T>>`.
    assert_eq!(Some(1), rx.next().await);
    assert_eq!(Some(2), rx.next().await);
    assert_eq!(None, rx.next().await);
}
```
