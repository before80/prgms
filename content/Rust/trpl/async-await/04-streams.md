+++
title = "17.4 Stream：序列中的 Future"
date = 2026-08-05T08:44:00+08:00
weight = 83
type = "docs"
description = "介绍 Stream：随时间产生一系列值的异步序列，及其与迭代器的关系"
isCJKLanguage = true
draft = false
rust_version = "1.97.1"

+++

> 译文 · 基于 [The Rust Programming Language](https://doc.rust-lang.org/stable/book/)（rustc 1.97.1）

# Stream：序列中的 Future {#stream-future}


> 原文链接: [https://doc.rust-lang.org/stable/book/ch17-04-streams.html](https://doc.rust-lang.org/stable/book/ch17-04-streams.html)


## Stream：序列中的 Future {#composing-streams}

　　回想本章前面[「消息传递」][17-02-messages]一节中异步通道接收端的用法。异步的 `recv` 方法会随时间产生一系列项。这正是一种更一般模式——*流*（stream）——的实例。许多概念天然适合用流表示：队列中陆续可用的项、完整数据过大而无法一次装入内存时从文件系统增量拉取的数据块，或随时间从网络到达的数据。因为流也是 Future，我们可以把它们与其他任何 Future 一起使用，并以有趣的方式组合：例如批量处理事件以避免过多网络调用、为长时间运行的操作序列设置超时，或节流界面事件以避免无谓工作。

　　我们在第 13 章[「`Iterator` Trait 与 `next` 方法」][iterator-trait]一节中见过项的序列，但迭代器与异步通道接收端有两处不同。第一是时间：迭代器是同步的，而通道接收端是异步的。第二是 API：直接使用 `Iterator` 时调用的是同步的 `next` 方法；而对 `trpl::Receiver` 流，我们调用的是异步的 `recv`。除此之外，这些 API 感觉非常相似，而这并非巧合。流就像异步形式的迭代。不过 `trpl::Receiver` 专门等待接收消息，而通用的流 API 更宽：它像 `Iterator` 那样提供下一项，但是异步地提供。

　　Rust 中迭代器与流的相似性意味着，我们实际上可以从任意迭代器创建流。与迭代器一样，可以通过调用流的 `next` 方法再等待其输出，如示例 17-21 所示——该代码目前还不能编译。

**文件名：`src/main.rs`**
```rust
        let values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
        let iter = values.iter().map(|n| n * 2);
        let mut stream = trpl::stream_from_iter(iter);

        while let Some(value) = stream.next().await {
            println!("The value was: {value}");
        }
```

**示例 17-21：从迭代器创建流并打印其值**

　　我们从数字数组出发，先转成迭代器，再调用 `map` 把所有值加倍，然后用 `trpl::stream_from_iter` 把迭代器转成流。接着用 `while let` 循环在项到达时遍历流中的项。

　　不幸的是，尝试运行时无法编译，而是报告没有可用的 `next` 方法：


```text
error[E0599]: no method named `next` found for struct `tokio_stream::iter::Iter` in the current scope
  --> src/main.rs:10:40
   |
10 |         while let Some(value) = stream.next().await {
   |                                        ^^^^
   |
   = help: items from traits can only be used if the trait is in scope
help: the following traits which provide `next` are implemented but not in scope; perhaps you want to import one of them
   |
1  + use crate::trpl::StreamExt;
   |
1  + use futures_util::stream::stream::StreamExt;
   |
1  + use std::iter::Iterator;
   |
1  + use std::str::pattern::Searcher;
   |
help: there is a method `try_next` with a similar name
   |
10 |         while let Some(value) = stream.try_next().await {
   |                                        ~~~~~~~~
```

　　如输出所示，编译错误的原因是：要用 `next` 方法，需要把正确的 trait 引入作用域。按目前的讨论，你可能会合理地以为那个 trait 是 `Stream`，实际上却是 `StreamExt`。`Ext` 是 *extension*（扩展）的缩写，在 Rust 社区中是用一个 trait 扩展另一个 trait 的常见模式。

　　`Stream` trait 定义了一个底层接口，实际上把 `Iterator` 与 `Future` 的能力合在一起。`StreamExt` 在 `Stream` 之上提供更高层的一组 API，包括 `next` 方法，以及其他类似 `Iterator` trait 所提供的工具方法。`Stream` 与 `StreamExt` 尚未进入 Rust 标准库，但生态中大多数 crate 使用类似的定义。

　　修复编译错误的方法是为 `trpl::StreamExt` 添加 `use` 语句，如示例 17-22 所示。

**文件名：`src/main.rs`**
```rust
use trpl::StreamExt;

fn main() {
    trpl::block_on(async {
        let values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
        // --snip--
```

**示例 17-22：成功地以迭代器作为流的基础**

　　把这些拼在一起后，代码就能按我们期望的方式工作了！而且，一旦 `StreamExt` 在作用域中，我们就可以像使用迭代器那样使用它的全部工具方法。

[17-02-messages]: ../02-concurrency-with-async/#message-passing
[iterator-trait]: ../../functional-features/02-iterators/#the-iterator-trait-and-the-next-method
