+++
title = "23.2-select!"
date = 2026-08-22T19:00:00+08:00
weight = 36
type = "docs"
description = "select!"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Asynchronous Programming in Rust](https://rust-lang.github.io/async-book/)

# select! {#select}


> 原文链接: [https://rust-lang.github.io/async-book/06_multiple_futures/03_select.html](https://rust-lang.github.io/async-book/06_multiple_futures/03_select.html)


`futures::select` 宏同时运行多个 future，允许用户在任意 future 完成时立即响应。

```rust,edition2018
use futures::{
    future::FutureExt, // for `.fuse()`
    pin_mut,
    select,
};

async fn task_one() { /* ... */ }
async fn task_two() { /* ... */ }

async fn race_tasks() {
    let t1 = task_one().fuse();
    let t2 = task_two().fuse();

    pin_mut!(t1, t2);

    select! {
        () = t1 => println!("task one completed first"),
        () = t2 => println!("task two completed first"),
    }
}
```

上面的函数将并发运行 `t1` 和 `t2`。当 `t1` 或 `t2` 完成时，对应的处理程序会调用 `println!`，函数会结束而不完成剩余任务。

`select` 的基本语法是 `<pattern> = <expression> => <code>,`，根据需要 `select` 的 future 数量重复。

## `default => ...` 与 `complete => ...`

`select` 还支持 `default` 和 `complete` 分支。

当正在 `select` 的 future 都尚未完成时，会运行 `default` 分支。带有 `default` 分支的 `select` 因此总会立即返回，因为若其他 future 都未就绪，将运行 `default`。

`complete` 分支可用于处理正在 `select` 的所有 future 都已完成且不再推进的情况。在 `select!` 循环中这通常很有用。

```rust,edition2018
use futures::{future, select};

async fn count() {
    let mut a_fut = future::ready(4);
    let mut b_fut = future::ready(6);
    let mut total = 0;

    loop {
        select! {
            a = a_fut => total += a,
            b = b_fut => total += b,
            complete => break,
            default => unreachable!(), // never runs (futures are ready, then complete)
        };
    }
    assert_eq!(total, 10);
}
```

## 与 `Unpin` 和 `FusedFuture` 的交互

你可能在第一个示例中注意到，必须对两个 `async fn` 返回的 future 调用 `.fuse()`，并用 `pin_mut` 固定它们。这两个调用都是必要的，因为 `select` 中使用的 future 必须同时实现 `Unpin` trait 和 `FusedFuture` trait。

需要 `Unpin` 是因为 `select` 使用的 future 不是按值获取，而是按可变引用。不取得 future 的所有权，未完成的 future 可在 `select` 调用后再次使用。

类似地，需要 `FusedFuture` trait，因为 `select` 不得在 future 完成后再次 poll 它。`FusedFuture` 由跟踪是否已完成的 future 实现。这使得可以在循环中使用 `select`，只 poll 尚未完成的 future。这可在上面的示例中看到，`a_fut` 或 `b_fut` 在第二次循环时已完成。由于 `future::ready` 返回的 future 实现了 `FusedFuture`，它能告知 `select` 不要再次 poll 它。

请注意，流有对应的 `FusedStream` trait。实现该 trait 或通过 `.fuse()` 包装的流，其 `.next()` / `.try_next()` 组合子会产生 `FusedFuture` future。

```rust,edition2018
use futures::{
    stream::{Stream, StreamExt, FusedStream},
    select,
};

async fn add_two_streams(
    mut s1: impl Stream<Item = u8> + FusedStream + Unpin,
    mut s2: impl Stream<Item = u8> + FusedStream + Unpin,
) -> u8 {
    let mut total = 0;

    loop {
        let item = select! {
            x = s1.next() => x,
            x = s2.next() => x,
            complete => break,
        };
        if let Some(next_num) = item {
            total += next_num;
        }
    }

    total
}
```

## 在 `select` 循环中使用 `Fuse` 和 `FuturesUnordered` 的并发任务

一个不太显眼但很方便的函数是 `Fuse::terminated()`，它允许构造一个已终止的空 future，之后可填入需要运行的 future。

当需要在 `select` 循环期间运行、但在 `select` 循环内部创建的任务时，这很有用。

请注意 `.select_next_some()` 函数的用法。可与 `select` 配合使用，只为流返回的 `Some(_)` 值运行分支，忽略 `None`。

```rust,edition2018
use futures::{
    future::{Fuse, FusedFuture, FutureExt},
    stream::{FusedStream, Stream, StreamExt},
    pin_mut,
    select,
};

async fn get_new_num() -> u8 { /* ... */ 5 }

async fn run_on_new_num(_: u8) { /* ... */ }

async fn run_loop(
    mut interval_timer: impl Stream<Item = ()> + FusedStream + Unpin,
    starting_num: u8,
) {
    let run_on_new_num_fut = run_on_new_num(starting_num).fuse();
    let get_new_num_fut = Fuse::terminated();
    pin_mut!(run_on_new_num_fut, get_new_num_fut);
    loop {
        select! {
            () = interval_timer.select_next_some() => {
                // 定时器已到期。若尚未运行则启动新的 `get_new_num_fut`
                // 若尚未在运行。
                if get_new_num_fut.is_terminated() {
                    get_new_num_fut.set(get_new_num().fuse());
                }
            },
            new_num = get_new_num_fut => {
                // 新数字到达——启动新的 `run_on_new_num_fut`，
                // 丢弃旧的。
                run_on_new_num_fut.set(run_on_new_num(new_num).fuse());
            },
            // 运行 `run_on_new_num_fut`
            () = run_on_new_num_fut => {},
            // 若全部完成则 panic，因为 `interval_timer` 应
            // 无限期持续产生值。
            complete => panic!("`interval_timer` completed unexpectedly"),
        }
    }
}
```

当需要同时运行许多相同 future 的副本时，使用 `FuturesUnordered` 类型。下面的示例与上面类似，但会将 `run_on_new_num_fut` 的每个副本运行至完成，而不是在创建新副本时中止它们。它还会打印 `run_on_new_num_fut` 返回的值。

```rust,edition2018
use futures::{
    future::{Fuse, FusedFuture, FutureExt},
    stream::{FusedStream, FuturesUnordered, Stream, StreamExt},
    pin_mut,
    select,
};

async fn get_new_num() -> u8 { /* ... */ 5 }

async fn run_on_new_num(_: u8) -> u8 { /* ... */ 5 }

async fn run_loop(
    mut interval_timer: impl Stream<Item = ()> + FusedStream + Unpin,
    starting_num: u8,
) {
    let mut run_on_new_num_futs = FuturesUnordered::new();
    run_on_new_num_futs.push(run_on_new_num(starting_num));
    let get_new_num_fut = Fuse::terminated();
    pin_mut!(get_new_num_fut);
    loop {
        select! {
            () = interval_timer.select_next_some() => {
                // 定时器已到期。若尚未运行则启动新的 `get_new_num_fut`
                // 若尚未在运行。
                if get_new_num_fut.is_terminated() {
                    get_new_num_fut.set(get_new_num().fuse());
                }
            },
            new_num = get_new_num_fut => {
                // 新数字到达——启动新的 `run_on_new_num_fut`。
                run_on_new_num_futs.push(run_on_new_num(new_num));
            },
            // 运行 `run_on_new_num_futs` 并检查是否有完成的
            res = run_on_new_num_futs.select_next_some() => {
                println!("run_on_new_num_fut returned {:?}", res);
            },
            // 若全部完成则 panic，因为 `interval_timer` 应
            // 无限期持续产生值。
            complete => panic!("`interval_timer` completed unexpectedly"),
        }
    }
}
```
