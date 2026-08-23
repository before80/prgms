+++
title = "23.1-join!"
date = 2026-08-22T19:00:00+08:00
weight = 35
type = "docs"
description = "join!"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Asynchronous Programming in Rust](https://rust-lang.github.io/async-book/)

# join! {#join}


> 原文链接: [https://rust-lang.github.io/async-book/06_multiple_futures/02_join.html](https://rust-lang.github.io/async-book/06_multiple_futures/02_join.html)


`futures::join` 宏可以在并发执行多个不同 future 的同时等待它们全部完成。

## `join!`

执行多个异步操作时，很容易简单地依次 `.await` 它们：

```rust,edition2018,ignore
async fn get_book_and_music() -> (Book, Music) {
    let book = get_book().await;
    let music = get_music().await;
    (book, music)
}
```

然而，这比必要的更慢，因为在 `get_book` 完成之前不会开始尝试 `get_music`。在其他一些语言中，future 会在环境中自动运行至完成，因此可以先调用每个 `async fn` 启动 future，然后同时 await 它们：

```rust,edition2018,ignore
// 错误——不要这样做
async fn get_book_and_music() -> (Book, Music) {
    let book_future = get_book();
    let music_future = get_music();
    (book_future.await, music_future.await)
}
```

然而，Rust future 在被主动 `.await` 之前不会做任何工作。这意味着上面两个代码片段都会串行运行 `book_future` 和 `music_future`，而非并发运行。要正确并发运行两个 future，请使用 `futures::join!`：

```rust,edition2018,ignore
use futures::join;

async fn get_book_and_music() -> (Book, Music) {
    let book_fut = get_book();
    let music_fut = get_music();
    join!(book_fut, music_fut)
}
```

`join!` 返回的值是包含传入的每个 `Future` 输出的元组。

## `try_join!`

对于返回 `Result` 的 future，考虑使用 `try_join!` 而非 `join!`。由于 `join!` 仅在所有子 future 完成后才完成，即使某个子 future 已返回 `Err`，它仍会继续处理其他 future。

与 `join!` 不同，`try_join!` 会在某个子 future 返回错误时立即完成。

```rust,edition2018,ignore
use futures::try_join;

async fn get_book() -> Result<Book, String> { /* ... */ Ok(Book) }
async fn get_music() -> Result<Music, String> { /* ... */ Ok(Music) }

async fn get_book_and_music() -> Result<(Book, Music), String> {
    let book_fut = get_book();
    let music_fut = get_music();
    try_join!(book_fut, music_fut)
}
```

请注意，传给 `try_join!` 的 future 必须具有相同的错误类型。考虑使用 `futures::future::TryFutureExt` 中的 `.map_err(|e| ...)` 和 `.err_into()` 函数来统一错误类型：

```rust,edition2018,ignore
use futures::{
    future::TryFutureExt,
    try_join,
};

async fn get_book() -> Result<Book, ()> { /* ... */ Ok(Book) }
async fn get_music() -> Result<Music, String> { /* ... */ Ok(Music) }

async fn get_book_and_music() -> Result<(Book, Music), String> {
    let book_fut = get_book().map_err(|()| "Unable to get book".to_string());
    let music_fut = get_music();
    try_join!(book_fut, music_fut)
}
```
