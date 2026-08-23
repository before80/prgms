+++
title = "6-更多 async/await 主题"
date = 2026-08-22T19:00:00+08:00
weight = 8
type = "docs"
description = "更多 async/await 主题"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Asynchronous Programming in Rust](https://rust-lang.github.io/async-book/)

# 更多 async/await 主题 {#more-async-await-topics}


> 原文链接: [https://rust-lang.github.io/async-book/part-guide/more-async-await.html](https://rust-lang.github.io/async-book/part-guide/more-async-await.html)


## 单元测试

如何对异步代码做单元测试？问题是你只能在异步上下文中 await，而 Rust 的单元测试不是 async。好在大多数运行时提供类似 `async main` 的测试便利属性。使用 Tokio 时如下：

```rust,norun
#[tokio::test]
async fn test_something() {
  // 在这里写测试，包括任意数量的 `await`。
}
```

配置测试的方式很多，详见[文档](https://docs.rs/tokio/latest/tokio/attr.test.html)。

测试异步代码还有一些更高级主题（如测试竞态条件、死锁等），本指南[后面]()会涵盖其中一些。


## 阻塞与取消

使用 async Rust 编程时，阻塞和取消很重要。这些概念不局限于某个特性或函数，而是你必须理解才能写出正确代码的、遍布系统的性质。

### 阻塞 IO

我们说线程（注意这里指 OS 线程，不是异步任务）被阻塞，是指它无法取得任何进展。通常因为它在等 OS 代其完成某项任务（通常是 I/O）。重要的是，线程阻塞时 OS 知道不应调度它，以便其他线程取得进展。在多线程程序中这没问题，因为阻塞线程等待时其他线程可以工作。但在异步程序中，同一 OS 线程上还有其他应被调度的任务，OS 不知道这些，会让整个线程一直等待。这意味着不是单个任务等自己的 I/O 完成（这可以接受），而是许多任务都要等（这不行）。

我们很快会讨论非阻塞/异步 I/O。目前只需知道：非阻塞 I/O 是异步运行时知晓的 I/O，因此只有当前任务等待；线程本身不被阻塞。从异步任务中只应使用非阻塞 I/O，绝不要用阻塞 I/O（Rust 标准库只提供这一种）。

### 阻塞计算

你也可以通过计算阻塞线程（这与阻塞 I/O 不完全相同，因为不涉及 OS，但效果类似）。若有长时间计算（无论是否含阻塞 I/O）且未向运行时让出控制权，该任务永远不会给运行时的调度器调度其他任务的机会。记住异步编程使用协作式多任务。这里任务不协作，其他任务就没机会工作。后面会讨论缓解方法。

阻塞整个线程的方式还有很多，本指南会多次回到阻塞话题。

### 取消

取消指停止 future（或任务）的执行。在 Rust 中（与许多其他 async/await 系统对比），future 必须由外部力量（如异步运行时）驱动前进，若 future 不再被驱动，就不会继续执行。若 future 被 drop（记住，future 只是普通 Rust 对象），就永远无法再取得进展，即被取消。

取消可以通过几种方式发起：

- 直接 drop future（若你拥有它）。
- 对任务的 `JoinHandle`（或 `AbortHandle`）调用 [`abort`](https://docs.rs/tokio/latest/tokio/task/struct.JoinHandle.html#method.abort)。
- 通过 [`CancellationToken`](https://docs.rs/tokio-util/latest/tokio_util/sync/struct.CancellationToken.html)（需要被取消的 future 注意到令牌并协作式取消自己）。
- 隐式地，通过 [`select`](https://docs.rs/tokio/latest/tokio/macro.select.html) 等函数或宏。

中间两种是 Tokio 特有的，但大多数运行时提供类似设施。使用 `CancellationToken` 需要被取消 future 的协作，其他则不需要。这些情况下，被取消的 future 不会收到取消通知，也没有清理机会（除析构函数外）。注意即使 future 有取消令牌，仍可通过其他方式取消，且不会触发取消令牌。

从编写异步代码（async 函数、块、future 等）的角度，代码可能在任意 `await`（包括宏中隐藏的）处停止执行且永不恢复。为使代码正确（具体是*取消安全*），无论正常完成还是在任意 await 点终止都必须正确工作[^cfThreads]。

```rust,norun
async fn some_function(input: Option<Input>) {
    let Some(input) = input else {
        return;           // 可能在此终止（`return`）。
    };

    let x = foo(input)?;  // 可能在此终止（`?`）。

    let y = bar(x).await; // 可能在此终止（`await`）。

    // ...

    //                       可能在此终止（隐式 return）。
}
```

一个会出错的例子：async 函数把数据读入内部缓冲区，然后 await 下一条数据。若读取是破坏性的（即无法从原始源重读）且 async 函数被取消，内部缓冲区会被 drop，其中数据丢失。考虑 future 及其触及的数据在取消 future、重启 future 或启动触及相同数据的新 future 时会如何受影响，很重要。

本指南会多次回到取消与取消安全性，参考部分有整章[讨论该主题]()。

[^cfThreads]: 将异步编程中的取消与取消线程对比很有趣。取消线程是可能的（例如 C 中用 `pthread_cancel`，Rust 没有直接方式），但几乎总是非常糟糕的想法，因为被取消的线程可能在任意处终止。相比之下，取消异步任务只能在 await 点发生。因此，不终止整个进程就取消 OS 线程非常罕见，程序员通常不必担心。但在 async Rust 中，取消是*可能*发生的。我们会随进展讨论如何应对。

## 异步块

普通块（`{ ... }`）在源码中把代码分组，并为名称创建封装作用域。运行时，块按顺序执行，求值为最后表达式的值（若无尾部表达式则为单元类型 `()`）。

与 async 函数类似，async 块是普通块的延迟版本。async 块把代码和名称作用域在一起，但运行时不会立即执行，求值为 future。要执行块并得到结果，必须 `await` 它。例如：

```rust,norun
let s1 = {
    let a = 42;
    format!("The answer is {a}")
};

let s2 = async {
    let q = question().await;
    format!("The question is {q}")
};
```

若执行这段代码，`s1` 是可打印的字符串，但 `s2` 是 future；`question()` 不会被调用。要打印 `s2`，必须先 `s2.await`。

async 块是启动异步上下文并创建 future 的最简单方式。常用于创建只在一处使用的小 future。

不幸的是，async 块的控制流有点古怪。因为 async 块创建 future 而非直接执行，相对控制流它更像函数而非普通块。`break` 和 `continue` 不能像普通块那样「穿过」async 块；必须用 `return`：

```rust,norun
loop {
    {
        if ... {
            // 可以
            continue;
        }
    }

    async {
        if ... {
            // 不行
            // continue;

            // 可以——继续 `loop` 的下一次执行，但注意若 loop 中 async 块之后还有代码会执行那些代码。
            return;
        }
    }.await
}
```

要实现 `break` 需要测试块的值（常见惯用法是用 [`ControlFlow`](https://doc.rust-lang.org/std/ops/enum.ControlFlow.html) 作为块的值，也允许使用 `?`）。

同样，async 块内的 `?` 会在出错时终止 future 的执行，使被 `await` 的块取错误值，但不会退出外围函数（普通块中的 `?` 会）。`await` 之后还需要另一个 `?`：

```rust,norun
async {
    let x = foo()?;   // 这个 `?` 只退出 async 块，不退出外围函数。
    consume(x);
    Ok(())
}.await?
```

烦人的是，这常让编译器困惑，因为（与函数不同）async 块的「返回」类型没有显式声明。可能需要在变量上加类型注解或用 turbofish 类型，例如上例用 `Ok::<_, MyError>(())` 代替 `Ok(())`。

返回 async 块的函数与 async 函数相当相似。写 `async fn foo() -> ... { ... }` 大致等价于 `fn foo() -> ... { async { ... } }`。事实上，从调用者角度看两者等价，从一种形式换成另一种不是破坏性变更。此外，实现 async trait 时可以用另一种覆盖一种（见下文）。但必须调整类型，在 async 块版本中显式写出 `Future`：`async fn foo() -> Foo` 变成 `fn foo() -> impl Future<Output = Foo>`（可能还需显式其他边界，如 `Send` 和 `'static`）。

通常更偏好 async 函数版本，因为更简单清晰。但 async 块版本更灵活，可以在函数被调用时执行一些代码（写在 async 块外），在结果被 await 时执行一些代码（async 块内的代码）。


## 异步闭包

- 闭包
  - 即将推出（https://github.com/rust-lang/rust/pull/132706, https://blog.rust-lang.org/inside-rust/2024/08/09/async-closures-call-for-testing.html）
  - 闭包中的 async 块 vs async 闭包


## 生命周期与借用

- 上文提到了 `'static` 生命周期
- future 上的生命周期边界（`Future + '_` 等）
- 跨 await 点的借用
- 我不确定，async 函数肯定还有更多生命周期问题……


## Future 上的 `Send + 'static` 边界

- 为何存在，多线程运行时
- 用 spawn local 避免
- 什么使 async fn 成为 `Send + 'static` 以及如何修复相关 bug


## 异步 trait

- 语法
  - `Send + 'static` 问题及规避
    - trait_variant
    - 显式 future
    - 返回类型记号（https://blog.rust-lang.org/inside-rust/2024/09/26/rtn-call-for-testing.html）
- 覆盖
  - 方法的 future vs async 记号
- 对象安全
- 捕获规则（https://blog.rust-lang.org/2024/09/05/impl-trait-capture-rules.html）
- 历史与 async-trait crate


## 递归

- 允许（相对较新），但需要显式装箱
  - 前向引用 future、pinning
  - https://rust-lang.github.io/async-book/07_workarounds/04_recursion.html
  - https://blog.rust-lang.org/2024/03/21/Rust-1.77.0.html#support-for-recursion-in-async-fn
  - async-recursion 宏（https://docs.rs/async-recursion/latest/async_recursion/）
