+++
title = "5-Async 与 await"
date = 2026-08-22T19:00:00+08:00
weight = 7
type = "docs"
description = "Async 与 await"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Asynchronous Programming in Rust](https://rust-lang.github.io/async-book/)

# Async 与 await {#async-and-await}


> 原文链接: [https://rust-lang.github.io/async-book/part-guide/async-await.html](https://rust-lang.github.io/async-book/part-guide/async-await.html)


本章我们将开始在 Rust 中进行异步编程，并介绍 `async` 和 `await` 关键字。

`async` 是函数（以及 traits 等其他项，后面会讲到）上的注解；`await` 是表达式中使用的运算符。但在深入这些关键字之前，我们需要涵盖 Rust 异步编程的几个核心概念，这承接上一章的讨论，此处我们将直接与 Rust 编程联系起来。

## Rust 异步概念

### 运行时

异步任务必须被管理和调度。通常任务数多于可用核心，因此不能全部同时运行。一个停止执行时，必须挑选另一个执行。若任务在等待 IO 或其他事件，则不应被调度，但该事件完成时应被调度。这需要与 OS 交互并管理 IO 工作。

许多编程语言提供运行时。通常，该运行时做的远不止管理异步任务——可能管理内存（包括垃圾回收）、参与异常处理、提供 OS 抽象层，甚至是一个完整的虚拟机。Rust 是低级语言，力求最小运行时开销。因此异步运行时的范围比许多其他语言的运行时有限得多。设计和实现异步运行时的方式也很多，所以 Rust 让你根据需求选择，而非只提供一个。这意味着入门异步编程需要额外一步。

除了运行和调度任务，运行时还必须与 OS 交互以管理异步 IO。还必须向任务提供定时器功能（与 IO 管理相交）。对运行时如何组织没有严格规则，但一些术语和职责划分很常见：

- *reactor*、*event loop* 或 *driver*（等价术语）：分发 IO 和定时器事件，与 OS 交互，做最低层的执行推进，
- *scheduler*（调度器）：决定任务何时、在哪个 OS 线程上执行，
- *executor* 或 *runtime*：结合 reactor 和 scheduler，是运行异步任务面向用户的 API；*runtime* 也指整个功能库（例如 Tokio crate 中的全部内容，而不只是由 [`Runtime`](https://docs.rs/tokio/latest/tokio/runtime/struct.Runtime.html) 类型表示的 Tokio executor）。

除上述 executor 外，运行时 crate 通常还包含许多实用 trait 和函数。可能包括 trait（如 `AsyncRead`）及 IO 实现、网络或文件系统等常见 IO 任务的功能、锁、通道及其他同步原语、定时工具、与 OS 协作的工具（如信号处理）、处理 future 和 stream（异步迭代器）的实用函数，或监控与观测工具。本指南会涵盖其中许多内容。

可选的异步运行时很多。有些调度策略非常不同，或针对特定任务或领域优化。本指南大部分使用 [Tokio](https://tokio.rs/) 运行时。它是通用运行时，是生态中最流行的。入门和生产都很合适。某些情况下，换用其他运行时可能性能更好或代码更简单。本指南后面会讨论其他可用运行时及选择理由，甚至如何自己编写。

要尽快上手，只需少量样板代码。需要在 Cargo.toml 中将 Tokio crate 列为依赖（与其他 crate 一样）：

```
[dependencies]
tokio = { version = "1", features = ["full"] }
```

并在 `main` 函数上使用 `tokio::main` 注解，使其可以成为 async 函数（否则 Rust 不允许）：

```rust,norun
#[tokio::main]
async fn main() { ... }
```

就是这样！可以开始写异步代码了！

`#[tokio::main]` 注解初始化 Tokio 运行时，并启动一个异步任务来运行 `main` 中的代码。本指南后面会更详细解释该注解的作用，以及如何不用它来使用异步代码（会给你更多灵活性）。

### Futures-rs 与生态

TODO 背景与历史，futures-rs 的用途——曾广泛使用，现在可能不需要，与 Tokio 及其他运行时的重叠（有时语义细微不同），为何可能需要（直接处理 future，尤其自己编写时、stream、一些工具）

其他生态内容——Yosh 的 crate、替代运行时、实验性内容等？

### Future 与任务

Rust 中异步并发的基本单位是 *future*。future 只是实现了 ['Future'](https://doc.rust-lang.org/std/future/trait.Future.html) trait 的普通 Rust 对象（通常是 struct 或 enum）。future 表示延迟计算，即在未来某时刻会就绪的计算。

本指南会大量讨论 future，但入门时不必过分担心。接下来几节会多次提到，但要到后面才真正定义并直接使用。future 的一个重要方面是可以组合成新的、更「大」的 future（后面会大量讨论*如何*组合）。

我在上一章和本章中相当非正式地用过「异步任务」一词。我用它表示逻辑上的执行序列；类似线程，但在程序内部管理而非由 OS 外部管理。用任务来思考往往有用，但 Rust 本身没有任务概念，该术语含义各异！更糟的是，运行时确实有任务概念，不同运行时对任务的理解略有不同。

从此处起，我会尽量精确使用任务相关术语。单独说「任务」时，指可能与其他任务并发发生的一段计算这一抽象概念。说「异步任务」时，与上述相同，但与作为 OS 线程实现的任务相对。说「运行时的任务」时，指某运行时所设想的那种任务；说「tokio 任务」（或其他具体运行时）时，指 Tokio 对任务的理解。

Rust 中的异步任务就是 future（通常是组合许多其他 future 而成的「大」future）。换言之，任务是正在执行的 future。然而，有时 future 被「执行」却不是运行时的任务。这类 future 直觉上是*任务*，但不是*运行时的任务*。遇到例子时我会更明确说明。


## 异步函数

`async` 关键字是函数声明上的修饰符。例如可写 `pub async fn send_to_server(...)`。async 函数就是使用 `async` 关键字声明的函数，意味着它可以异步执行，换言之调用者*可以选择不*在函数完成前就做别的事。

更机械地说，调用 async 函数时，函数体不会像普通函数那样执行。而是将函数体及其参数打包成 future，代替真实结果返回。调用者再决定如何处理该 future（若调用者想「立刻」得到结果，就会 `await` 该 future，见下一节）。

在 async 函数内，代码以通常的顺序方式执行[^preempt]，是 async 并无区别。可以从 async 函数调用同步函数，执行照常进行。async 函数内多出来的是可以用 `await` 等待其他 async 函数（或 future），这*可能*导致让出控制权，使另一个任务得以执行。

[^preempt]: 与其他线程一样，运行 async 函数的线程可能被 OS 抢占并暂停，让其他线程工作。但从函数角度看，若不检查可能被其他线程修改的数据（且其他线程可能在当前线程未暂停时并行修改），这是不可观察的。

## `await`

上文说 future 是在未来某时刻会就绪的计算。要得到该计算的结果，使用 `await` 关键字。若结果立即可用或无需等待即可计算，则 `await` 直接完成计算得到结果。但若结果未就绪，`await` 将控制权交给调度器，让另一个任务继续（即上一章提到的协作式多任务）。

在 Rust 中，await 的语法是 `some_future.await`，即与 `.` 运算符一起使用的后缀关键字。因此可以在方法调用链和字段访问中人体工学地使用。这与 Python 或 JavaScript 等语言不同，那里的 `await` 是放在表达式前的运算符，如 `await some_function()`。

为说明后缀 await 为何往往更人体工学，假设调用发起网络请求的 async 函数并想访问响应的状态码。用前缀 `await` 语法，需要在 `fetch()` 前加 `await`，再用括号包裹表达式以用 `?` 传播错误，然后访问状态码，如 `(await fetch())?.status_code`。后缀语法可写 `fetch().await?.status_code`。更长的链尤其有帮助。例如两个前缀 await 的表达式像 `(await (await fetch())?.json())?.data`，而后缀等价是 `fetch().await?.json().await?.data`，读起来更自然。

现在看 `async` 和 `await` 的实践。考虑以下函数：

```rust,norun
// 异步函数，但不需要等待任何东西。
async fn add(a: u32, b: u32) -> u32 {
  a + b
}

async fn wait_to_add(a: u32, b: u32) -> u32 {
  sleep(1000).await;
  a + b
}
```

若调用 `add(15, 3).await`，会立即返回结果 `18`。若调用 `wait_to_add(15, 3).await`，最终得到相同答案，但等待期间另一个任务有机会运行。

在这个简单例子中，对 `sleep` 的调用代表必须等待结果的长时间任务。通常是 IO 操作，结果是自外部源读取的数据或写入外部目标成功的确认。读取类似 `let data = read(...).await?`。此时 `await` 会使当前任务在读取进行时等待。读取完成后任务恢复（读取任务等待时其他任务可以工作）。读取结果可能是成功读到的数据或错误（由 `?` 处理）。

注意，若调用 `add`、`wait_to_add` 或 `read` 而不使用 `.await`，不会得到任何答案！

什么？

调用 async 函数返回 future，不会立即执行函数内代码。此外，future 在被 await 之前不做任何工作[^poll]。这与某些其他语言不同，那里的 async 函数返回会立即开始执行的 future。

这是 Rust 异步编程的重要一点。熟悉之后会成为本能，但常让初学者困惑，尤其有在其他语言中异步编程经验的人。

Rust 中 future 的一个重要直觉是：它们是惰性对象。要完成任何工作，必须由外部力量（通常是异步运行时）驱动前进。

我们从操作角度描述了 `await`（运行 future 产生结果），但上一章讨论了异步任务和并发，`await` 如何融入该心智模型？首先考虑纯顺序代码：逻辑上，调用函数就是执行函数内代码（带变量赋值）。换言之，当前任务继续执行由函数定义的下一「块」代码。类似地，在异步上下文中，调用非 async 函数就是继续用该函数执行。调用 async 函数找到要运行的代码，但不运行。`await` 是继续执行当前任务的运算符；若当前任务此刻不能继续，则让另一个任务有机会继续。

`await` 只能在异步上下文中使用，目前指 async 函数内（后面会看到更多异步上下文）。要理解原因，记住 `await` 可能把控制权交给运行时，让另一个任务执行。只有在异步上下文中才有可交出的运行时。目前可以把运行时想象成只在 async 函数中可访问的全局变量，后面会解释实际机制。

最后，再从另一个角度看 `await`：前面提到 future 可以组合成更「大」的 future。`async` 函数是定义 future 的一种方式，`await` 是组合 future 的一种方式。对 future 使用 `await` 会把该 future 组合进使用它的 async 函数所产生的 future 中。后面会更详细讨论这一视角及其他组合 future 的方式。

[^poll]: 或被 poll，是比 `await` 更低层的操作，使用 `await` 时在幕后发生。讨论 future 细节时会讲到 polling。

## 一些 async/await 示例

先从我们的「hello, world!」例子回顾：

```rust,edition2021
// 定义一个异步函数。
async fn say_hello() {
    println!("hello, world!");
}

#[tokio::main] // 样板代码，让我们可以写 `async fn main`，稍后解释。
async fn main() {
    // 调用异步函数并 await 其结果。
    say_hello().await;
}
```

你现在应能认出 `main` 周围的样板代码。用于初始化 Tokio 运行时并创建初始任务来运行 async `main` 函数。

`say_hello` 是 async 函数，调用它时必须后跟 `.await` 才能作为当前任务的一部分运行。注意若去掉 `.await`，运行程序什么也不做！调用 `say_hello` 返回 future，但从未执行，因此 `println` 永远不会被调用（编译器至少会警告你）。

下面是一个稍更实际的例子，来自 [Tokio 教程](https://tokio.rs/tokio/tutorial/hello-tokio)。

```rust,norun
#[tokio::main]
async fn main() -> Result<()> {
    // 连接到 mini-redis 地址。
    let mut client = client::connect("127.0.0.1:6379").await?;

    // 将键 "hello" 设为值 "world"
    client.set("hello", "world".into()).await?;

    // 获取键 "hello"
    let result = client.get("hello").await?;

    println!("got value from the server; result={:?}", result);

    Ok(())
}
```

代码更有趣一些，但本质上在做同样的事——调用 async 函数然后 await 执行结果。这次用 `?` 做错误处理——与同步 Rust 中一样。

尽管前面大量讨论并发、并行和异步，这两个例子都是 100% 顺序的。仅调用并 await async 函数不会引入任何并发，除非在等待任务等待时有其他任务可调度。为自证这一点，看另一个简单（但刻意构造的）例子：

```rust,edition2021
use std::io::{stdout, Write};
use tokio::time::{sleep, Duration};

async fn say_hello() {
    print!("hello, ");
    // 刷新 stdout，以便立即看到上面 `print` 的效果。
    stdout().flush().unwrap();
}

async fn say_world() {
    println!("world!");
}

#[tokio::main]
async fn main() {
    say_hello().await;
    // 异步 sleep 函数，让当前任务休眠 1 秒。
    sleep(Duration::from_millis(1000)).await;
    say_world().await;
}
```

在打印 "hello" 和 "world" 之间，让当前任务睡眠[^async-sleep]一秒。观察运行程序时发生什么：先打印 "hello"，什么都不做一秒，再打印 "world"。因为执行单个任务是纯顺序的。若有并发，那一秒的睡眠会是做其他工作（如打印 "world"）的绝佳机会。下一节会看到如何做。

[^async-sleep]: 注意这里用的是异步 sleep 函数，若用 std 的 [`sleep`](https://doc.rust-lang.org/std/thread/fn.sleep.html) 会让整个线程睡眠。在这个玩具例子里没区别，但在真实程序中意味着该段时间内其他任务无法在该线程上调度。这非常糟糕。


## 生成任务

我们把 async 和 await 作为在异步任务中运行代码的方式讨论过。也说 `await` 可以在等待 IO 或其他事件时让当前任务睡眠。那时另一个任务可以运行，但那些其他任务从何而来？就像用 `std::thread::spawn` 生成新任务，可以用 [`tokio::spawn`](https://docs.rs/tokio/latest/tokio/task/fn.spawn.html) 生成新异步任务。注意 `spawn` 是 Tokio（运行时）的函数，不是 Rust 标准库的，因为任务纯粹是运行时概念。

下面是用 `spawn` 在单独任务上运行 async 函数的小例子：

```rust,edition2021
use tokio::{spawn, time::{sleep, Duration}};

async fn say_hello() {
    // 打印前稍等片刻，让竞态更有趣。
    sleep(Duration::from_millis(100)).await;
    println!("hello");
}

async fn say_world() {
    sleep(Duration::from_millis(100)).await;
    println!("world!");
}

#[tokio::main]
async fn main() {
    spawn(say_hello());
    spawn(say_world());
    // 稍等片刻，给任务运行时间。
    sleep(Duration::from_millis(1000)).await;
}
```

与上个例子类似，有两个函数打印 "hello" 和 "world!"。但这次是并发（且并行）而非顺序运行。多运行几次程序，应看到两种打印顺序——有时 "hello" 先，有时 "world!" 先。经典的并发竞态！

深入看这里发生什么。有三个概念：future、任务和线程。`spawn` 函数接受一个 future（记住可以由许多更小的 future 组成）并将其作为新的 Tokio 任务运行。任务是 Tokio 运行时调度和管理的概念（不是单个 future）。Tokio（默认配置下）是多线程运行时，意味着生成新任务时，该任务可能在不同于生成它的任务的 OS 线程上运行（可能在同一线程，也可能先在一个线程上后来移到另一个）。

因此，future 作为任务 spawn 时，与生成它的任务及任何其他任务*并发*运行。若调度在不同线程上，也可能与那些任务*并行*运行。

总结：在 Rust 中写两条相继的语句时，它们是顺序执行的（无论是否 async）。写 `await` 不会改变顺序语句的并发性。例如 `foo(); bar();` 严格顺序——先调用 `foo`，之后调用 `bar`。无论 `foo` 和 `bar` 是否 async 函数都如此。`foo().await; bar().await;` 也严格顺序，`foo` 完全求值后 `bar` 完全求值。两种情况下另一个线程可能与顺序执行交错，第二种情况下另一个异步任务可能在 await 点交错，但两种情况下两条语句*彼此相对*仍是顺序执行的。

若使用 `thread::spawn` 或 `tokio::spawn`，就引入了并发和潜在的并行，前者在线程间，后者在任务间。

本指南后面会看到并发执行 future 但永不并行的情况。


### 联结任务

若要得到 spawn 任务的执行结果，生成任务可以等待其完成并使用结果，这称为*join*（联结）任务（类似[联结](https://doc.rust-lang.org/std/thread/struct.JoinHandle.html#method.join)线程，联结 API 也类似）。

任务 spawn 时，spawn 函数返回 [`JoinHandle`](https://docs.rs/tokio/latest/tokio/task/struct.JoinHandle.html)。若只想让任务自己执行，可以丢弃 `JoinHandle`（丢弃 `JoinHandle` 不影响已 spawn 的任务）。但若希望生成任务等待被生成任务完成再用结果，可以 `await` 该 `JoinHandle`。

例如，再回顾一次「Hello, world!」例子：


```rust,edition2021
use tokio::{spawn, time::{sleep, Duration}};

async fn say_hello() {
    // 打印前稍等片刻，让竞态更有趣。
    sleep(Duration::from_millis(100)).await;
    println!("hello");
}

async fn say_world() {
    sleep(Duration::from_millis(100)).await;
    println!("world");
}

#[tokio::main]
async fn main() {
    let handle1 = spawn(say_hello());
    let handle2 = spawn(say_world());
    
    let _ = handle1.await;
    let _ = handle2.await;

    println!("!");
}
```

代码与上次类似，但不只是调用 `spawn`，我们保存返回的 `JoinHandle` 并稍后 `await` 它们。因为退出 `main` 前等待这些任务完成，不再需要在 `main` 里 `sleep`。

两个 spawn 的任务仍在并发执行。多运行几次应看到两种顺序。然而，被 `await` 的 join handle 是对并发的限制：最后的感叹号（'!'）*永远*最后打印（可以试试把 `println!("!");` 相对于 `await` 移动位置，可能还要改 sleep 时间才能观察到效果）。

若立即 `await` 第一个 `spawn` 的 `JoinHandle` 而非保存稍后 `await`（即写 `spawn(say_hello()).await;`），会 spawn 另一个任务运行 'hello' future，但生成任务会等它完成才做别的。换言之，不可能有并发！几乎永远不该这样做（既然要 spawn，直接写顺序代码就好）。

### `JoinHandle`

我们快速更深入看 `JoinHandle`。能 `await` `JoinHandle` 说明 `JoinHandle` 本身也是 future。`spawn` 不是 `async` 函数，是返回 future（`JoinHandle`）的普通函数。它在返回 future 前做了一些工作（调度任务），因此*不必* `await` `spawn`。await `JoinHandle` 会等待 spawn 的任务完成然后返回结果。上例没有结果，只等了任务完成。`JoinHandle` 是泛型类型，类型参数是被 spawn 任务返回的类型。上例类型是 `JoinHandle<()>`，返回 `String` 的 future 会产生 `JoinHandle<String>`。

`await` `JoinHandle` 返回 `Result`（因此上例用 `let _ = ...`，避免未使用 `Result` 的警告）。若 spawn 的任务成功完成，任务结果在 `Ok` 变体中。若任务 panic 或被 abort（一种[取消](../../part-reference/16-cancellation-and-cancellation-safety/)形式），结果是包含 [`JoinError` docs](https://docs.rs/tokio/latest/tokio/task/struct.JoinError.html) 的 `Err`。若项目中不用 `abort` 做取消，对 `JoinHandle.await` 的结果 `unwrap` 是合理做法，因为相当于把 spawn 任务的 panic 传播到生成任务。
