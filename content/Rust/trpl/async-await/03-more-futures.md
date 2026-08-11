+++
title = "17.3 处理任意数量的 Future"
date = 2026-08-05T08:44:00+08:00
weight = 82
type = "docs"
description = "向运行时让出控制权，并组合 Future 构建 timeout 等异步抽象"
isCJKLanguage = true
draft = false
rust_version = "1.97.1"

+++

> 译文 · 基于 [The Rust Programming Language](https://doc.rust-lang.org/stable/book/)（rustc 1.97.1）

# 处理任意数量的 Future {#working-with-any-number-of-futures}


> 原文链接: [https://doc.rust-lang.org/stable/book/ch17-03-more-futures.html](https://doc.rust-lang.org/stable/book/ch17-03-more-futures.html)


### 向运行时让出控制权

　　回想[「我们的第一个异步程序」][async-program]一节：在每个 await 点，若正在等待的 Future 尚未就绪，Rust 会给运行时一个机会暂停该任务并切换到另一个。反过来也成立：Rust *只*在 await 点暂停异步块并把控制权交还给运行时。await 点之间的一切都是同步的。

　　这意味着，若你在异步块里做了大量工作却没有 await 点，那个 Future 就会挡住其他 Future 取得进展。有时这被称为一个 Future *饿死*（starving）其他 Future。有些情况下这也许无妨。但若你在做某种昂贵的初始化或长时间运行的工作，或有一个会无限做某事的 Future，就需要考虑何时、何处把控制权交还给运行时。

　　我们先模拟一个长时间运行的操作来说明饿死问题，再探索如何解决。示例 17-14 引入了 `slow` 函数。

**文件名：`src/main.rs`**
```rust
fn slow(name: &str, ms: u64) {
    thread::sleep(Duration::from_millis(ms));
    println!("'{name}' ran for {ms}ms");
}
```

**示例 17-14：用 `thread::sleep` 模拟慢操作**

　　这段代码使用 `std::thread::sleep` 而非 `trpl::sleep`，因此调用 `slow` 会阻塞当前线程若干毫秒。我们可以用 `slow` 代替现实中既长时间运行又阻塞的操作。

　　在示例 17-15 中，我们用 `slow` 模拟在一对 Future 里做这类 CPU 密集型工作。

**文件名：`src/main.rs`**
```rust
        let a = async {
            println!("'a' started.");
            slow("a", 30);
            slow("a", 10);
            slow("a", 20);
            trpl::sleep(Duration::from_millis(50)).await;
            println!("'a' finished.");
        };

        let b = async {
            println!("'b' started.");
            slow("b", 75);
            slow("b", 10);
            slow("b", 15);
            slow("b", 350);
            trpl::sleep(Duration::from_millis(50)).await;
            println!("'b' finished.");
        };

        trpl::select(a, b).await;
```

**示例 17-15：调用 `slow` 函数模拟慢操作**

　　每个 Future 只有在完成一堆慢操作*之后*才把控制权交还给运行时。若运行此代码，会看到如下输出：


```text
'a' started.
'a' ran for 30ms
'a' ran for 10ms
'a' ran for 20ms
'b' started.
'b' ran for 75ms
'b' ran for 10ms
'b' ran for 15ms
'b' ran for 350ms
'a' finished.
```

　　与示例 17-5 中用 `trpl::select` 竞速两个抓取 URL 的 Future 一样，`select` 仍会在 `a` 完成后立刻结束。不过两个 Future 里对 `slow` 的调用之间没有交错：`a` Future 一直干到等待 `trpl::sleep`，然后 `b` Future 一直干到等待它自己的 `trpl::sleep`，最后 `a` Future 完成。要让两个 Future 在各自的慢任务之间都能推进，我们需要 await 点，以便把控制权交还给运行时。也就是说，我们需要有东西可以等待！

　　我们其实已经在示例 17-15 里看到这种交接：若去掉 `a` Future 末尾的 `trpl::sleep`，它会在 `b` Future *根本不运行*的情况下完成。我们先试着用 `trpl::sleep` 作为让各操作轮流推进的起点，如示例 17-16 所示。

**文件名：`src/main.rs`**
```rust
        let one_ms = Duration::from_millis(1);

        let a = async {
            println!("'a' started.");
            slow("a", 30);
            trpl::sleep(one_ms).await;
            slow("a", 10);
            trpl::sleep(one_ms).await;
            slow("a", 20);
            trpl::sleep(one_ms).await;
            println!("'a' finished.");
        };

        let b = async {
            println!("'b' started.");
            slow("b", 75);
            trpl::sleep(one_ms).await;
            slow("b", 10);
            trpl::sleep(one_ms).await;
            slow("b", 15);
            trpl::sleep(one_ms).await;
            slow("b", 350);
            trpl::sleep(one_ms).await;
            println!("'b' finished.");
        };
```

**示例 17-16：用 `trpl::sleep` 让各操作轮流推进**

　　我们在每次调用 `slow` 之间加入了带 await 点的 `trpl::sleep`。现在两个 Future 的工作交错起来了：


```text
'a' started.
'a' ran for 30ms
'b' started.
'b' ran for 75ms
'a' ran for 10ms
'b' ran for 10ms
'a' ran for 20ms
'b' ran for 15ms
'a' finished.
```

　　`a` Future 在把控制权交给 `b` 之前仍会先跑一会儿，因为它在调用 `trpl::sleep` 之前就调用了 `slow`；但之后，每当一方碰到 await 点，两个 Future 就会来回切换。本例中我们在每次 `slow` 之后都这样做，但也可以按最合理的方式拆分工作。

　　不过我们其实并不想在这里*睡眠*：我们希望尽可能快地推进，只是需要把控制权交还给运行时。可以直接用 `trpl::yield_now` 做到这一点。在示例 17-17 中，我们把那些 `trpl::sleep` 全部换成 `trpl::yield_now`。

**文件名：`src/main.rs`**
```rust
        let a = async {
            println!("'a' started.");
            slow("a", 30);
            trpl::yield_now().await;
            slow("a", 10);
            trpl::yield_now().await;
            slow("a", 20);
            trpl::yield_now().await;
            println!("'a' finished.");
        };

        let b = async {
            println!("'b' started.");
            slow("b", 75);
            trpl::yield_now().await;
            slow("b", 10);
            trpl::yield_now().await;
            slow("b", 15);
            trpl::yield_now().await;
            slow("b", 350);
            trpl::yield_now().await;
            println!("'b' finished.");
        };
```

**示例 17-17：用 `yield_now` 让各操作轮流推进**

　　这段代码既更清楚地表达了真实意图，也可能比使用 `sleep` 快得多，因为 `sleep` 所用的计时器往往对粒度有限制。例如我们使用的 `sleep` 版本，即使传入一纳秒的 `Duration`，也总会至少睡一毫秒。再说一次，现代计算机*很快*：一毫秒里能做很多事！

　　这意味着，即便对计算密集型任务，async 也可能有用——取决于程序其余部分在做什么——因为它为组织程序不同部分之间的关系提供了有用工具（代价是异步状态机的开销）。这是一种*协作式多任务*（cooperative multitasking）：每个 Future 有权通过 await 点决定何时交出控制，因而也有责任避免阻塞过久。在某些基于 Rust 的嵌入式操作系统中，这甚至是*唯一*的多任务方式！

　　在真实代码中，你当然不会通常在每一行都交替函数调用与 await 点。以这种方式让出控制相对便宜，但并非免费。很多时候，试图拆分计算密集型任务反而会显著变慢，因此有时为了*整体*性能，让操作短暂阻塞更好。务必测量，看清代码真正的性能瓶颈。不过若你看到大量本应并发却串行发生的工作，记住背后的这一动态很重要！

### 构建我们自己的异步抽象 {#building-our-own-async-abstractions}

　　我们也可以把 Future 组合起来形成新模式。例如，可以用已有的异步构建块实现 `timeout` 函数。完成后，结果又会成为可用于构建更多异步抽象的积木。

　　示例 17-18 展示了我们期望这个 `timeout` 如何与一个慢 Future 配合工作。

**文件名：`src/main.rs`**
```rust
        let slow = async {
            trpl::sleep(Duration::from_secs(5)).await;
            "Finally finished"
        };

        match timeout(slow, Duration::from_secs(2)).await {
            Ok(message) => println!("Succeeded with '{message}'"),
            Err(duration) => {
                println!("Failed after {} seconds", duration.as_secs())
            }
        }
```

**示例 17-18：用设想中的 `timeout` 在时限内运行慢操作**

　　来实现它！首先想想 `timeout` 的 API：

- 它本身需要是异步函数，以便我们可以等待它。
- 第一个参数应是要运行的 Future。可以做成泛型，以便适用于任意 Future。
- 第二个参数是最长等待时间。若使用 `Duration`，就很容易再传给 `trpl::sleep`。
- 它应返回 `Result`。若 Future 成功完成，`Result` 为带有该 Future 产出值的 `Ok`；若超时先到，`Result` 为带有超时所等待时长的 `Err`。

　　示例 17-19 展示了这一声明。


**文件名：`src/main.rs`**
```rust
async fn timeout<F: Future>(
    future_to_try: F,
    max_time: Duration,
) -> Result<F::Output, Duration> {
    // Here is where our implementation will go!
}
```

**示例 17-19：定义 `timeout` 的签名**

　　这满足了我们对类型的目标。现在想想所需的*行为*：我们要把传入的 Future 与时长竞速。可以用 `trpl::sleep` 从时长做出计时 Future，再用 `trpl::select` 把该计时器与调用方传入的 Future 一起运行。

　　在示例 17-20 中，我们通过对等待 `trpl::select` 的结果做匹配来实现 `timeout`。

**文件名：`src/main.rs`**
```rust
use trpl::Either;

// --snip--


async fn timeout<F: Future>(
    future_to_try: F,
    max_time: Duration,
) -> Result<F::Output, Duration> {
    match trpl::select(future_to_try, trpl::sleep(max_time)).await {
        Either::Left(output) => Ok(output),
        Either::Right(_) => Err(max_time),
    }
}
```

**示例 17-20：用 `select` 与 `sleep` 定义 `timeout`**

　　`trpl::select` 的实现并不公平：它总是按传入参数的顺序轮询（其他 `select` 实现会随机选择先轮询哪个参数）。因此我们把 `future_to_try` 作为第一个参数传给 `select`，这样即便 `max_time` 很短，它也有机会完成。若 `future_to_try` 先完成，`select` 返回带有其输出的 `Left`；若 `timer` 先完成，`select` 返回带有计时器输出 `()` 的 `Right`。

　　若 `future_to_try` 成功并得到 `Left(output)`，我们返回 `Ok(output)`。若睡眠计时器先到期并得到 `Right(())`，我们用 `_` 忽略 `()`，改为返回 `Err(max_time)`。

　　至此，我们用另外两个异步辅助工具拼出了一个可用的 `timeout`。运行代码时，会在超时后打印失败模式：

```text
Failed after 2 seconds
```

　　因为 Future 可以与其他 Future 组合，你可以用更小的异步积木构建非常强大的工具。例如，可以用同样的思路把超时与重试组合，再用于网络调用等操作（如示例 17-5 中的那些）。

　　实践中，你通常主要直接使用 `async` 与 `await`，其次才用 `select` 这类函数以及 `join!` 这类宏来控制最外层 Future 如何执行。

　　我们已经见过多种同时处理多个 Future 的方式。接下来将看到如何用*流*（stream）处理随时间依次出现的多个 Future。

[async-program]: ../01-futures-and-syntax/#our-first-async-program
