+++
title = "8-并发组合 Future"
date = 2026-08-22T19:00:00+08:00
weight = 10
type = "docs"
description = "并发组合 Future"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Asynchronous Programming in Rust](https://rust-lang.github.io/async-book/)

# 并发组合 Future {#composing-futures-concurrently}


> 原文链接: [https://rust-lang.github.io/async-book/part-guide/concurrency-primitives.html](https://rust-lang.github.io/async-book/part-guide/concurrency-primitives.html)


本章涵盖 future 组合的更多方式。特别是一些新的、可并发（但不并行）执行 future 的方式。表面上，本章介绍的新函数/宏很简单，但底层概念可能相当微妙。我们会先回顾 future、并发与并行，但你可能也想重读较早比较[并发与并行](../04-concurrent-programming/#concurrency-and-parallelism)的一节。

future 是延迟计算。可用 `await` 推进 future，将控制权交给运行时，使当前任务等待计算结果。若 `a` 和 `b` 是 future，可顺序组合（即组合成先完整执行 `a` 再完整执行 `b` 的 future），先 await 一个再 await 另一个：`async { a.await; b.await}`。

我们也见过用 `spawn` 并行组合 future：`async { let a = spawn(a); let b = spawn(b); (a.await, b.await)}` 并行运行两个 future。注意元组中的 `await` 不是 await future 本身，而是 await `JoinHandle` 以在 future 完成时获取结果。

本章介绍两种并发但不并行组合 future 的方式：`join` 和 `select`/`race`。两种情况下，future 通过时间片并发运行；每个被组合的 future 轮流执行，然后下一个获得机会。这*不涉及异步运行时*（因此没有多个 OS 线程，也没有并行可能）。组合构造在本地交错 future。可以把这些构造想成在单个异步任务内执行其组件 future 的迷你 executor。

join 与 select/race 的根本区别在于如何处理 future 完成工作：join 在所有 future 完成时结束，select/race 在一个 future 完成时结束（其余被取消）。两者也有处理错误的变体。

这些构造（或类似概念）常与 stream 一起使用，下文会略提，更多在 [stream 一章](../../streams/)讨论。

若要并行（或不明确不要并行），spawn 任务往往是这些组合构造的更简单替代。spawn 通常更少出错、更通用，性能更可预测。另一方面，spawn 本质上更少[结构化](../../part-reference/18-structured-concurrency/)，生命周期和资源管理更难推理。

值得更深入考虑性能问题。并发组合的潜在性能问题是时间共享的公平性。若程序有 100 个任务，通常最优资源共享是每个任务获得 1% 处理器时间（或若任务都在等待，则每个有相同被唤醒机会）。若 spawn 100 个任务，通常大致如此。但若 spawn 两个任务并在其中一个上 join 99 个 future，调度器只知道两个任务，一个任务得 50% 时间，99 个 future 各得 0.5%。

通常任务分布没那么偏颇，且我们常把 join/select 等用于超时等，这种行为实际是可取的。但值得考虑以确保程序有你想要的性能特征。


## Join

Tokio 的 [`join` 宏](https://docs.rs/tokio/latest/tokio/macro.join.html) 接受 future 列表并并发运行它们全部至完成（将所有结果作为元组返回）。所有 future 完成时返回。future 始终在同一线程上执行（并发但不并行）。

简单例子：

```rust,norun
async fn main() {
  let (result_1, result_2) = join!(do_a_thing(), do_a_thing());
  // 使用 `result_1` 和 `result_2`。
}
```

这里两次 `do_a_thing` 并发发生，两者都完成时结果就绪。注意我们不必 `await` 获取结果。`join!` 隐式 await 其 future 并产生值。它不创建 future。仍需在异步上下文中使用（例如从 async 函数内）。

虽然上例看不出来，`join!` 接受求值为 future 的表达式[^into]。`join` 不在其体内创建异步上下文，不应 `await` 传给 `join` 的 future（否则会在被 join 的 future 之前求值）。

因所有 future 在同一线程执行，若任一 future 阻塞线程，则都无法取得进展。若使用互斥锁或其他锁，一个 future 等待另一个持有的锁时很容易死锁。

[`join`](https://docs.rs/tokio/latest/tokio/macro.join.html) 不关心 future 的结果。特别地，若 future 被取消或返回错误，不影响其他——它们继续执行。若要「快速失败」行为，用 [`try_join`](https://docs.rs/tokio/latest/tokio/macro.try_join.html)。`try_join` 与 `join` 类似，但若任一 future 返回 `Err`，则取消所有其他 future 并立即返回错误。

回到较早的 [async/await](../../async-await/) 一章，我们用「join」谈联结 spawn 的任务。顾名思义，联结 future 与任务相关：联结意味着并发执行多个 future 并在继续前等待结果。语法不同：用 `JoinHandle` vs `join` 宏，但思想类似。关键区别是联结任务时任务并发且并行执行，而用 `join!` 时 future 并发但不并行。此外，spawn 的任务由运行时的调度器调度，而用 `join!` 时 future 在本地「调度」（同一任务上、在宏执行的时间范围内）。另一区别是 spawn 的任务 panic 时由运行时捕获，而 `join` 中的 future panic 则整个任务 panic。


### 替代方案

并发运行 future 并收集结果是常见需求。除非有好理由（即明确不要并行，即使那时也可能更偏好 [`spawn_local`](https://docs.rs/tokio/latest/tokio/task/fn.spawn_local.html)），应 probably 用 `spawn` 和 `JoinHandle`。 [`JoinSet`](https://docs.rs/tokio/latest/tokio/task/struct.JoinSet.html) 抽象以类似 `join!` 的方式管理此类 spawn 的任务。

大多数运行时（及 [futures.rs](https://docs.rs/futures/latest/futures/macro.join.html)）有与 Tokio `join` 宏等价的实现，行为大多相同。也有 `join` 函数，与宏类似但稍欠灵活。例如 futures.rs 有 [`join`](https://docs.rs/futures/latest/futures/future/fn.join.html) 联结两个 future，[`join3`](https://docs.rs/futures/latest/futures/future/fn.join3.html)、[`join4`](https://docs.rs/futures/latest/futures/future/fn.join4.html)、[`join5`](https://docs.rs/futures/latest/futures/future/fn.join5.html) 联结对应数量，[join_all](https://docs.rs/futures/latest/futures/future/fn.join_all.html) 联结 future 集合（以及各自的 `try_` 变体）。

[Futures-concurrency](https://docs.rs/futures-concurrency/latest) 也提供 join（和 try_join）功能。在 futures-concurrency 风格中，这些操作是 future 组（如元组、`Vec` 或数组）上的 trait 方法。例如联结两个 future 写 `(fut1, fut2).join().await`（注意这里 `await` 是显式的）。

若要联结的 future 集合动态变化（例如网络输入到来时创建新 future），或想在 future 完成时而非全部完成时得到结果，需要用 stream 及 [`FuturesUnordered`](https://docs.rs/futures/latest/futures/stream/struct.FuturesUnordered.html) 或 [`FuturesOrdered`](https://docs.rs/futures/latest/futures/stream/struct.FuturesOrdered.html) 功能。[stream 一章](../../streams/)会涵盖。


[^into]: 表达式类型必须实现 `IntoFuture`。表达式由宏求值并转换为 future。即它们不必实际求值为 future，而是可转换为 future 的东西，但这是很小的区别。表达式本身在任何结果 future 执行之前顺序求值。


## Race/select

与联结 future 相对的是竞速（aka select）。race/select 时 future 并发执行，但不是等所有 future 完成，只等第一个完成然后取消其余。虽然听起来与 join 相似，但显著更有趣（有时更易出错），因为现在必须推理取消。

使用 Tokio [`select`](https://docs.rs/tokio/latest/tokio/macro.select.html) 宏的例子：

```rust,norun
async fn main() {
  select! {
    result = do_a_thing() => {
      println!("computation completed and returned {result}");
    }
    _ = timeout() => {
      println!("computation timed-out");
    }
  }
}
```

你会注意到比 `join` 宏更有趣，因为我们在 `select` 宏内处理 future 的结果。有点像 `match` 表达式，但 `select` 时所有分支并发运行，最先完成的分支体以其结果执行（其他分支不执行，future 通过 `drop` 取消）。例中 `do_a_thing` 和 `timeout` 并发执行，先完成的执行其块（即只有一个 `println` 会运行），另一个 future 被取消。与 `join` 宏一样，await future 是隐式的。

Tokio 的 `select` 宏支持许多特性：

- 模式匹配：每分支 `=` 左侧语法可以是模式，仅当 future 结果匹配模式时才执行块。若不匹配，future 不再被 poll（但其他 future 会）。对可选返回值的 future 有用，例如 `Some(x) = do_a_thing() => { ... }`。
- `if` 守卫：每分支可有 `if` 守卫。`select` 宏运行时，每表达式求值为 future 后求值 `if` 守卫，仅守卫为真时才 poll future。例如 `x = = do_a_thing() if false => { ... }` 永远不会被 poll。注意 `if` 守卫在 polling 期间不重新求值，仅在宏初始化时。
- `else` 分支：`select` 可有 `else` 分支 `else => { ... }`，所有 future 停止且没有块被执行时执行。若无 `else` 分支发生这种情况，`select` 会 panic。

`select!` 宏的值是所执行分支的值（像 `match`），因此所有分支必须有相同类型。例如若要在 `select` 外使用上例结果，这样写：

```rust,norun
async fn main() {
  let result = select! {
    result = do_a_thing() => {
      Some(result)
    }
    _ = timeout() => {
      None
    }
  };

  // 使用 `result`
}
```

与 `join!` 一样，`select!` 不以特殊方式处理 `Result`（除前述模式匹配外），若分支以错误完成，则取消所有其他分支，错误作为 select 的结果（与分支成功完成相同方式）。

`select` 宏内在使用取消，因此若程序要避免取消，必须避免 `select!`。事实上 `select` 常常是异步程序中取消的主要来源。如[别处](../../part-reference/16-cancellation-and-cancellation-safety/)讨论，取消有许多微妙问题可导致 bug。特别注意 `select` 通过简单 drop future 来取消。不会通知被 drop 的 future 或触发任何取消令牌等。

`select!` 常在循环中处理 stream 或其他 future 序列。这增加一层复杂性和 bug 机会。简单情况下每次循环迭代创建新的独立 future，事情不太复杂。但这很少是所需。通常要在迭代间保留一些状态。常与 stream 在循环中用 `select`，每次迭代处理 stream 的一个结果。例如：

```rust,norun
async fn main() {
  let mut stream = ...;

  loop {
    select! {
      result = stream.next() => {
        match result {
          Some(x) => println!("received: {x}"),
          None => break,
        }
      }
      _ = timeout() => {
        println!("time out!");
        break;
      }
    }
  }
}
```

此例从 `stream` 读取值并打印，直到没有剩余或等待结果超时。超时情况下 stream 中剩余数据的命运取决于 stream 实现（可能丢失！或重复！）。这是取消面前行为为何重要（且棘手）的例子。

我们可能想在迭代间重用 future，不只是 stream。例如可能想与超时 future 竞速，超时适用于所有迭代而非每次迭代新超时。可在循环外创建 future 并引用它：

```rust,norun
async fn main() {
  let mut stream = ...;
  let mut timeout = timeout();

  loop {
    select! {
      result = stream.next() => {
        match result {
          Some(x) => println!("received: {x}"),
          None => break,
        }
      }
      // 创建对 `timeout` 的引用而非移动它。
      _ = &mut timeout => {
        println!("time out!");
        break;
      }
    }
  }
}
```

在循环中用 `select!` 及在 `select!` 外创建的 future 或 stream 时，有几个重要细节。这些是 `select` 工作方式的根本后果，我会用上例中的 `timeout` 逐步说明。

- `timeout` 在循环外创建并以某倒计时初始化。
- 每次循环迭代，`select` 创建对 `timeout` 的引用，但不改变其状态。
- `select` 执行时 poll `timeout`，有时间剩余时返回 `Pending`，时间到时返回 `Ready`，此时执行其块。

上例中 `timeout` 就绪时我们 `break` 出循环。若不这样做呢？`select` 会再次 poll `timeout`，而 `Future` [文档](https://doc.rust-lang.org/std/future/trait.Future.html#tymethod.poll) 说不应发生！`select` 帮不了这个，迭代间没有状态决定 `timeout` 是否应被 poll。取决于 `timeout` 如何编写，可能导致 panic、逻辑错误或某种崩溃。

可用几种方式防止此类 bug：

- 使用 [fused](../12-futures/#fusing) [future](https://docs.rs/futures/latest/futures/future/trait.FutureExt.html#method.fuse) 或 [stream](https://docs.rs/futures/latest/futures/stream/trait.StreamExt.html#method.fuse)，使重新 poll 安全。
- 确保代码结构使 future 永不重新 poll，例如跳出循环（如上例），或用 `if` 守卫。

现在考虑 `&mut timeout` 的类型。假设 `timeout()` 返回实现 `Future` 的类型，可能是 async 函数的匿名类型，或像 `Timeout` 的具名类型。假设后者因为例子更容易（但逻辑两种情况都适用）。给定 `Timeout` 实现 `Future`，`&mut Timeout` 会实现 `Future` 吗？不一定！有 [blanket `impl`](https://doc.rust-lang.org/std/future/trait.Future.html#impl-Future-for-%26mut+F) 使之为真，但仅当 `Timeout` 实现 `Unpin`。并非所有 future 都如此，因此写类似上例的代码常会类型错误。用 `pin` 宏很容易修复，例如 `let mut timeout = pin!(timeout());`

循环中用 `select` 取消是微妙 bug 的丰富来源。通常发生在 future 包含涉及某些数据的状态但不包含数据本身时。future 因取消被 drop 时，该状态丢失但底层数据未更新。可能导致数据丢失或多次处理。


### 替代方案

Futures.rs 有自己的 [`select` 宏](https://docs.rs/futures/latest/futures/macro.select.html)，futures-concurrency 有 [Race trait](https://docs.rs/futures-concurrency/latest/futures_concurrency/future/trait.Race.html)，是 Tokio `select` 宏的替代。两者核心语义相同：并发竞速多个 future，处理第一个的结果并取消其余，但语法不同，细节有差异。

Futures.rs 的 `select` 表面上与 Tokio 相似；概括差异，futures.rs 版本：

- Future 必须始终 fused（类型检查强制）。
- `select` 有 `default` 和 `complete` 分支，而非 `else` 分支。
- `select` 不支持 `if` 守卫。

Futures-concurrency 的 `Race` 语法非常不同，类似其 `join` 版本，例如 `(future_a, future_b).race().await`（也适用于 `Vec` 和数组以及元组）。语法不如宏灵活，但融入大多数异步代码很好。注意若在循环内用 `race`，仍可能有与 `select` 相同的问题。

与 `join` 一样，spawn 任务并让它们并行执行常常是 `select` 的好替代。但第一个完成后取消其余任务需要额外工作。可用通道或取消令牌。无论哪种，取消需要被取消任务采取行动，意味着任务可以做清理或其他优雅关闭。

`select` 的常见用途（尤其在循环内）是处理 stream。有些 stream 组合子方法可替代部分 `select` 用法。例如 futures-concurrency 的 [`merge`](https://docs.rs/futures-concurrency/latest/futures_concurrency/stream/trait.Merge.html) 是合并多个 stream 的好替代。


## 结语

本节讨论了并发运行 future 组的两种方式。联结 future 意味着等它们全部完成；选择（aka 竞速）future 意味着等第一个完成。与 spawn 任务对比，这些组合不使用并行。

`join` 和 `select` 都作用于事先已知的 future 集合（常在写程序时而非运行时）。有时要组合的 future 事先未知——必须在执行过程中向组合集合添加 future。为此需要 [stream](../../streams/)，它们有自己的组合操作。

值得重申：虽然这些组合运算符强大且表达力强，用任务和 spawn 往往更简单更合适：并行通常可取，取消或阻塞相关的 bug 更少，资源分配通常更公平（或至少更简单）且更可预测。
