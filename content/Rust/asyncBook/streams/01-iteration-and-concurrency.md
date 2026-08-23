+++
title = "22.1-迭代与并发"
date = 2026-08-22T19:00:00+08:00
weight = 33
type = "docs"
description = "迭代与并发"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Asynchronous Programming in Rust](https://rust-lang.github.io/async-book/)

# 迭代与并发 {#iteration-and-concurrency}


> 原文链接: [https://rust-lang.github.io/async-book/05_streams/02_iteration_and_concurrency.html](https://rust-lang.github.io/async-book/05_streams/02_iteration_and_concurrency.html)


与同步 `Iterator` 类似，有多种方式迭代和处理 `Stream` 中的值。有组合子风格的方法如 `map`、`filter` 和 `fold`，以及遇错即退的对应方法 `try_map`、`try_filter` 和 `try_fold`。

遗憾的是，`for` 循环不能用于 `Stream`，但对于命令式代码，可以使用 `while let` 以及 `next`/`try_next` 函数：

```rust,edition2018,ignore
async fn sum_with_next(mut stream: Pin<&mut dyn Stream<Item = i32>>) -> i32 {
    use futures::stream::StreamExt; // for `next`
    let mut sum = 0;
    while let Some(item) = stream.next().await {
        sum += item;
    }
    sum
}

async fn sum_with_try_next(
    mut stream: Pin<&mut dyn Stream<Item = Result<i32, io::Error>>>,
) -> Result<i32, io::Error> {
    use futures::stream::TryStreamExt; // for `try_next`
    let mut sum = 0;
    while let Some(item) = stream.try_next().await? {
        sum += item;
    }
    Ok(sum)
}
```

然而，若我们一次只处理一个元素，可能错失并发机会——毕竟这是我们编写异步代码的原因。要并发处理流中的多个项，请使用 `for_each_concurrent` 和 `try_for_each_concurrent` 方法：

```rust,edition2018,ignore
async fn jump_around(
    mut stream: Pin<&mut dyn Stream<Item = Result<u8, io::Error>>>,
) -> Result<(), io::Error> {
    use futures::stream::TryStreamExt; // for `try_for_each_concurrent`
    const MAX_CONCURRENT_JUMPERS: usize = 100;

    stream.try_for_each_concurrent(MAX_CONCURRENT_JUMPERS, |num| async move {
        jump_n_times(num).await?;
        report_n_jumps(num).await?;
        Ok(())
    }).await?;

    Ok(())
}
```
