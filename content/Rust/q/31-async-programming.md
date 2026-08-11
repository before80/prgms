+++
title = "31-异步编程"
date = 2026-07-28T14:49:00+08:00
weight = 310
type = "docs"
description = "面向 Go 开发者讲清 Rust async、future、executor 与常见跨 await 报错"
isCJKLanguage = true
draft = false

+++

# 异步编程 (Async Programming)

> 面向 **Rust 1.97.1** (stable, 2026-07)。本篇假设你熟悉 Go，凡有可比性处均给出 🐹 Go 对比。
>
> 热度: `hot` 高频 | `common` 常见 | `occasional` 偶尔 | `advanced` 进阶少见

**本篇能解决什么：**

- 你是否把 Rust `async` 当成了 Go goroutine，结果发现“怎么一个 `.await` 不写就什么都没跑”？
- 你是否想知道 `Future`、`executor`、`wake`、`pin` 这些词到底分别扮演什么角色？
- 你是否被 `future cannot be sent between threads safely`、`borrowed value does not live long enough` 这类跨 `await` 报错绊住过？
- 你是否分不清 `tokio::spawn`、`spawn_local`、`join!`、`select!`、`spawn_blocking` 分别该在什么场景用？
- 你是否担心把 stable、nightly 和“只是概念示意”的内容混到一起？

**术语速查表：**

| 术语 / 缩略词 | 全称 / 读法 | 中文 | 一句话解释 | Go 里的近亲 |
|---|---|---|---|---|
| async | — | 异步 | 函数不立即执行，而是先返回 future | goroutine 启动前的任务描述，不完全等价 |
| await | — | 等待挂起点 | 把当前 future 交回运行时，等条件满足后再继续 | channel/IO 阻塞点，概念接近 |
| future | — | 未来值 | 一个“以后可能产生结果”的状态机对象 | goroutine + result channel，不完全等价 |
| executor | — | 执行器 | 负责反复 poll future 的调度器 | runtime 调度器 |
| runtime | — | 运行时 | 提供执行器、定时器、异步 IO 等基础设施 | Go runtime |
| poll | — | 轮询 | 询问 future 现在是否完成 | 调度器检查任务进度 |
| `Poll::Pending` | — | 未就绪 | 还没完成，稍后再 poll | 任务阻塞 |
| `Poll::Ready` | — | 已就绪 | 结果已准备好 | 任务完成 |
| wake | — | 唤醒 | 通知执行器“可以再来 poll 我了” | 运行时重新调度 |
| `Waker` | — | 唤醒器 | future 用来通知执行器重试的句柄 | 调度回调 |
| pin | — | 固定地址 | 承诺值在内存中的地址不再被安全移动 | Go 无直接对应 |
| `Send` | — | 可跨线程转移 | 一个值能安全地从一个线程搬到另一个线程 | 可并发共享/转移的近似 |
| `LocalSet` | — | 本地任务集合 | Tokio 中专门跑 `!Send` future 的单线程执行环境 | 单线程事件循环 |
| AFIT | Async Function In Trait | trait 中异步函数 | 在 trait 里直接写 `async fn` 的能力 | interface 方法里返回 future，概念接近 |
| Stream | — | 流 | 异步产生多个值的序列，可反复 `poll_next` | 读 channel 的 `for range`，部分近似 |
| CancellationToken | — | 取消令牌 | 协作式取消信号，收到后任务自行停下 | `context.WithCancel`，部分近似 |
| `JoinSet` | — | 动态任务集合 | Tokio 里动态 spawn 一批任务并等待/收集结果 | `errgroup` / WaitGroup + 结果收集，部分近似 |

> 说明：本表覆盖本篇出现的所有专业名词与缩略词；正文首次出现时仍会就地解释一次。

**热度索引：**

| 热度 | 题目 |
|------|------|
| `hot` | [Q1](#q1), [Q2](#q2), [Q3](#q3), [Q4](#q4), [Q5](#q5), [Q8](#q8), [Q13](#q13), [Q14](#q14), [Q23](#q23) |
| `common` | [Q6](#q6), [Q7](#q7), [Q9](#q9), [Q10](#q10), [Q15](#q15), [Q16](#q16), [Q17](#q17), [Q18](#q18), [Q19](#q19), [Q20](#q20), [Q21](#q21), [Q22](#q22), [Q24](#q24), [Q25](#q25) |
| `occasional` | [Q11](#q11) |
| `advanced` | [Q12](#q12) |

---

## Q1. Rust `async` 和 Go goroutine 最本质的区别是什么？ {#q1}
**Tags:** `hot` `async` `goroutine`
**适用版本:** Rust 1.39+（`async`/`await` stable）

**一句话答案：**

Go 的 goroutine 一启动就会被 runtime 调度执行；Rust 的 `async fn` 先返回一个 **future**（未来值，状态机对象），只有被 `.await` 或交给 executor 轮询后才会真正推进。

**解答：**

本题示例会用到 Tokio 和 `futures`。先加依赖（二选一即可）：

```bash
cargo add tokio --features macros,rt-multi-thread
cargo add futures
```

或在 `Cargo.toml` 里写：

```toml
[dependencies]
tokio = { version = "1", features = ["macros", "rt-multi-thread"] }
futures = "0.3"
```

先看 Rust：

```rust
async fn work() -> i32 {
    42
}

#[tokio::main]
async fn main() {
    let fut = work(); // 这里只是创建 future
    let n = fut.await; // 到这里才开始把它跑完
    assert_eq!(n, 42);
}
```

如果你创建了 future 却不 `.await`，它通常什么都不会做：

```rust
async fn log_it() {
    println!("run");
}

async fn demo() {
    log_it();
    // warning: unused implementer of `Future` that must be used
    // note: futures do nothing unless you `.await` or poll them
}

fn main() {}
```

```rust
use futures::executor::block_on;

async fn work() -> i32 {
    7
}

fn main() {
    assert_eq!(block_on(work()), 7);
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	go fmt.Println("run") // 一启动就会被调度
}
```

- **Go 怎么做**：`go f()` 立刻把任务交给 runtime。
- **Rust 为什么不同**：Rust 想把异步任务表达成零成本状态机，调度与执行显式交给 executor。
- **Go 程序员易踩的坑**：把 `async fn` 调用当成 `go f()`；Rust 里它更像“先拿到一张待执行任务单”。

**记忆点：**

- goroutine 是“立刻调度”。
- future 是“惰性对象”，不 `.await` 就不推进。
- Rust async 不是“更轻量 goroutine”，而是完全不同的模型。

---

## Q2. `async fn` 返回的到底是什么？ {#q2}
**Tags:** `hot` `future`
**适用版本:** Rust 1.39+

**一句话答案：**

`async fn foo() -> T` 的真实含义接近 `fn foo() -> impl Future<Output = T>`；返回的是编译器生成的匿名状态机类型，不是线程、不是协程栈。

**解答：**

语法糖版：

```rust
async fn add_one(x: i32) -> i32 {
    x + 1
}

fn main() {}
```

大致等价的心智模型：

```rust
use std::future::Future;

fn add_one_desugared(x: i32) -> impl Future<Output = i32> {
    async move { x + 1 }
}

fn main() {}
```

```rust
use futures::executor::block_on;

async fn add_one(x: i32) -> i32 {
    x + 1
}

fn main() {
    let fut = add_one(41);
    assert_eq!(block_on(fut), 42);
}
```

**Go 对比：**

```go
package main

func addOne(x int) int {
	return x + 1
}

func main() {
	_ = addOne(1)
}
```

- **Go 怎么做**：普通函数直接算出结果；并发通常靠 goroutine 或 channel 包起来。
- **Rust 为什么不同**：Rust 把“以后才能拿到结果”显式建模成 `Future<Output = T>`。
- **Go 程序员易踩的坑**：future 不是“后台线程句柄”，它本身只是状态机对象。

**记忆点：**

- `async fn` 的真正返回值是 future。
- future 的具体类型不可名，所以常写 `impl Future`。

---

## Q3. 为什么标准库不够，还要 Tokio 这类 executor / runtime？ {#q3}
**Tags:** `hot` `runtime` `executor`
**适用版本:** Rust 1.39+；Tokio 1.x stable

**一句话答案：**

标准库只给了 future 协议，没有给你完整的异步 IO、定时器和任务调度；Tokio 之类的 runtime 把这些“跑起来需要的基础设施”补齐。

**解答：**

Tokio 示例先加依赖：

```toml
[dependencies]
tokio = { version = "1", features = ["macros", "rt-multi-thread", "time"] }
```

然后才能这样写：

```rust
#[tokio::main]
async fn main() {
    tokio::time::sleep(std::time::Duration::from_millis(10)).await;
    println!("done");
}
```

没有 runtime 时，你只能拿到 future，却没人持续 poll 它：

```rust
async fn work() {}

fn main() {
    let _fut = work();
}
```

```rust
use futures::executor::block_on;

async fn work() {}

fn main() {
    block_on(work());
}
```

**Go 对比：**

```go
package main

import "time"

func main() {
	time.Sleep(10 * time.Millisecond)
}
```

- **Go 怎么做**：调度器和很多并发能力是语言/runtime 一体化提供的。
- **Rust 为什么不同**：Rust 标准库把抽象层拆开，让你可选 Tokio、smol 等不同 runtime。
- **Go 程序员易踩的坑**：觉得“语言既然有 async，就应该自动有网络事件循环”；Rust 故意没把这层绑死。

**记忆点：**

- `Future` 是协议。
- executor 负责 poll。
- runtime = executor + timer + IO + task 管理等配套设施。

---

## Q4. `poll`、`wake`、`Waker` 分别是什么角色？ {#q4}
**Tags:** `hot` `poll` `wake`
**适用版本:** Rust 1.36+（`Future` 入 `std`）

**一句话答案：**

executor 会调用 `poll` 问 future“你完成了吗”；future 若还没好，就返回 `Pending`，并用 `Waker` 约定“条件到了我会 wake 你，再来 poll”。

**解答：**

心智模型签名是：

```rust
use std::future::Future;
use std::pin::Pin;
use std::task::{Context, Poll};

trait MyFuture {
    type Output;
    fn poll(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Self::Output>;
}
```

真实业务代码通常不手写 `poll`，但你要理解 `.await` 背后的规则：

```rust
#[tokio::main]
async fn main() {
    tokio::time::sleep(std::time::Duration::from_millis(10)).await;
    println!("awake");
}
```

```rust
use std::task::Poll;

fn main() {
    let state = Poll::<i32>::Pending;
    assert!(matches!(state, Poll::Pending));
}
```

**Go 对比：**

```go
package main

import "time"

func main() {
	time.Sleep(10 * time.Millisecond)
}
```

- **Go 怎么做**：调度和唤醒大多由 runtime 隐式处理，程序员几乎不接触这层协议。
- **Rust 为什么不同**：future 是库级协议，所以 poll/wake 合约需要被明确定义。
- **Go 程序员易踩的坑**：以为 executor 会“自动忙等重试”；其实 future 返回 `Pending` 时必须安排好 wake。

**记忆点：**

- `poll` = 问一次。
- `Pending` = 现在没好。
- `wake` = 好了再叫我。

---

## Q5. `pin` 到底在保护什么？ {#q5}
**Tags:** `hot` `pin`
**适用版本:** Rust 1.33+（`Pin` stable）

**一句话答案：**

`Pin`（固定地址）保护的是“某些 future 内部可能自引用”；一旦 future 开始被 poll，它的内存地址就不能再被安全移动，否则内部指针可能失效。

**解答：**

你日常最常见的是“用而不深究”：

```rust
use std::pin::pin;

async fn work() -> i32 {
    1
}

fn main() {
    let fut = work();
    let _pinned = pin!(fut);
}
```

更重要的是知道：这不是“性能优化”，而是安全约束。

```rust
fn main() {
    // 对初学者来说，记住这句话就够了：
    // future 一旦被 poll，就要假设它可能依赖稳定地址。
}
```

```rust
use std::pin::Pin;

async fn work() -> i32 {
    1
}

fn main() {
    let mut fut = Box::pin(work());
    let _: Pin<&mut _> = fut.as_mut();
}
```

**Go 对比：**

```go
package main

func main() {}
```

- **Go 怎么做**：Go 没把这种“对象地址能否安全移动”的约束暴露给普通并发代码。
- **Rust 为什么不同**：Rust 把底层状态机与内存安全直接连接起来，`Pin` 是这套契约的一部分。
- **Go 程序员易踩的坑**：把 `Pin` 当成“性能小技巧”；它本质上是内存安全工具。

**记忆点：**

- `Pin` 不是 async 专属，但 async 里最常见。
- 初学时先记住它在防止“被 poll 后再移动”。

---

## Q6. 为什么跨 `await` 会冒出借用和生命周期错误？ {#q6}
**Tags:** `common` `lifetime`
**适用版本:** Rust 1.39+

**一句话答案：**

因为一旦值跨过 `.await` 还活着，它就会成为 future 状态机的一部分；这会放大借用期、所有权和 `Send` 约束。

**解答：**

能过的写法：

```rust
#[tokio::main]
async fn main() {
    let s = String::from("hi");
    println!("{}", s);
    tokio::time::sleep(std::time::Duration::from_millis(1)).await;
}
```

常见坏味道是“借了一个局部，再想把它活到 await 后”：

```rust
async fn bad() -> &str {
    let s = String::from("hi");
    // tokio::time::sleep(std::time::Duration::from_millis(1)).await;
    // &s
    // error[E0515]: cannot return reference to local variable `s`
    ""
}

fn main() {}
```

**Go 对比：**

```go
package main

func main() {}
```

- **Go 怎么做**：goroutine 栈与 GC 帮你兜很多生命周期细节。
- **Rust 为什么不同**：Rust 需要在编译期证明 future 里保存的借用始终有效。
- **Go 程序员易踩的坑**：不要把 `.await` 前后的代码想成“还是同一个普通栈帧”。

**记忆点：**

- 跨 `await` 的值会进状态机。
- 一旦进状态机，生命周期要求就变严。

---

## Q7. 什么是 `!Send` future？为什么 `tokio::spawn` 不收它？ {#q7}
**Tags:** `common` `send`
**适用版本:** Tokio 1.x stable

**一句话答案：**

如果 future 在某个 `.await` 两侧都持有一个 `!Send` 值，比如 `Rc`，那整个 future 也会变成 `!Send`；而 `tokio::spawn` 默认可能把任务挪到别的线程，所以要求 `Send + 'static`。

**解答：**

会报错的最小例子：

```rust
use std::rc::Rc;

async fn bad() {
    let rc = Rc::new(1);
    tokio::time::sleep(std::time::Duration::from_millis(1)).await;
    let _ = *rc;
}

fn main() {}
```

对应典型报错是：

```rust
fn main() {
    // tokio::spawn(bad());
    // error[E0277]: future cannot be sent between threads safely
}
```

修法之一是让 `Rc` 不跨 await：

```rust
use std::rc::Rc;

async fn good() {
    {
        let rc = Rc::new(1);
        let _ = *rc;
    }
    tokio::time::sleep(std::time::Duration::from_millis(1)).await;
}

fn main() {}
```

**Go 对比：**

```go
package main

func main() {
	go func() {
		// Go 不会在类型层面阻止你把对象从一个 goroutine 传到另一个 goroutine
	}()
}
```

- **Go 怎么做**：共享是否安全主要靠约定、锁和 race detector。
- **Rust 为什么不同**：Rust 把“能不能跨线程转移”做成 `Send` 约束，提前在编译期拦住。
- **Go 程序员易踩的坑**：看到 `spawn` 失败时，不要只盯 `spawn`；真正问题常是某个值活过了 `.await`。

**记忆点：**

- `!Send` 的根源通常是“某个值跨 await 了”。
- 想修复，先缩小作用域，再考虑换 `Arc` 等类型。

---

## Q8. `tokio::spawn`、`join!`、`select!` 各自像什么？ {#q8}
**Tags:** `hot` `tokio`
**适用版本:** Tokio 1.x stable；`join!` / `select!` 为 Tokio 宏，stable

**一句话答案：**

`tokio::spawn` 是“把任务交给 runtime 独立调度”；`join!` 是“并发等待多个 future 都完成”；`select!` 是“谁先完成先处理谁”。

**解答：**

`spawn`：

```rust
#[tokio::main]
async fn main() {
    let handle = tokio::spawn(async { 1 + 1 });
    assert_eq!(handle.await.unwrap(), 2);
}
```

`join!`：

```rust
#[tokio::main]
async fn main() {
    let a = async { 1 };
    let b = async { 2 };
    let (x, y) = tokio::join!(a, b);
    assert_eq!((x, y), (1, 2));
}
```

`select!`：

```rust
#[tokio::main]
async fn main() {
    let out = tokio::select! {
        v = async { 1 } => v,
        v = async { 2 } => v,
    };
    assert!(out == 1 || out == 2);
}
```

**Go 对比：**

```go
package main

func main() {
	// goroutine 更像 tokio::spawn
	// select 更像 tokio::select!
}
```

- **Go 怎么做**：`go` 和 `select` 是语言内建。
- **Rust 为什么不同**：Rust 把这层放在 runtime/宏里，不同生态可有不同策略。
- **Go 程序员易踩的坑**：`join!` 不会自动把 future 丢到后台线程，它只是并发轮询当前几个 future。

**记忆点：**

- `spawn` = 独立任务。
- `join!` = 都等完。
- `select!` = 谁先好用谁。

---

## Q9. 什么场景该用 `spawn_blocking`？ {#q9}
**Tags:** `common` `blocking`
**适用版本:** Tokio 1.x stable

**一句话答案：**

凡是会长时间阻塞线程的同步工作，比如压缩、大 JSON 解析、老式阻塞库、CPU 重活，都别直接塞进 async 任务里；用 `spawn_blocking` 把它丢到专门的阻塞线程池。

**解答：**

错误思路：

```rust
#[tokio::main]
async fn main() {
    std::thread::sleep(std::time::Duration::from_secs(1));
}
```

更合适的写法：

```rust
#[tokio::main]
async fn main() {
    let n = tokio::task::spawn_blocking(|| {
        std::thread::sleep(std::time::Duration::from_millis(10));
        42
    })
    .await
    .unwrap();

    assert_eq!(n, 42);
}
```

**Go 对比：**

```go
package main

import "time"

func main() {
	go func() {
		time.Sleep(time.Second)
	}()
}
```

- **Go 怎么做**：goroutine 阻塞时由 runtime 负责调度其它 goroutine。
- **Rust 为什么不同**：async 任务通常共享较少线程，直接阻塞会拖慢整个 executor。
- **Go 程序员易踩的坑**：把 Rust async 任务当 goroutine，用阻塞库时却不做隔离。

**记忆点：**

- async 线程不等于可以随便阻塞。
- 阻塞工作用 `spawn_blocking`。

---

## Q10. `spawn_local` 和 `LocalSet` 是干什么的？ {#q10}
**Tags:** `common` `local`
**适用版本:** Tokio 1.x stable

**一句话答案：**

当你的 future 明确是 `!Send`，又确实要跨 `.await` 保存这些值时，可以在单线程环境里用 `LocalSet` + `spawn_local` 跑它。

**解答：**

最小示意：

```rust
use std::rc::Rc;

#[tokio::main(flavor = "current_thread")]
async fn main() {
    let local = tokio::task::LocalSet::new();
    local
        .run_until(async {
            tokio::task::spawn_local(async {
                let rc = Rc::new(1);
                tokio::time::sleep(std::time::Duration::from_millis(1)).await;
                assert_eq!(*rc, 1);
            })
            .await
            .unwrap();
        })
        .await;
}
```

它和 `tokio::spawn` 的差别就在于：不再要求把任务安全搬去别的线程。

```rust
fn main() {
    // 看到 !Send future 时，先问：
    // 我能不能缩小作用域改成 Send？
    // 真不行，再考虑 LocalSet。
}
```

**Go 对比：**

```go
package main

func main() {}
```

- **Go 怎么做**：Go 没有“这个 goroutine 只能待在线程本地执行器里”的常见用户态 API。
- **Rust 为什么不同**：Rust 把线程转移安全性做成类型约束，所以要给 !Send future 一个明确的运行场所。
- **Go 程序员易踩的坑**：不要一看到 `!Send` 就直接上 `LocalSet`；更常见的正确修法是缩短值跨 await 的生存期。

**记忆点：**

- `spawn_local` 不是更快版 `spawn`。
- 它是“明确只在本地线程跑”的工具。

---

## Q11. trait 里能直接写 `async fn` 吗？AFIT 现在算 stable 吗？ {#q11}
**Tags:** `occasional` `afit`
**适用版本:** Rust 1.75+（AFIT stable）；Rust 1.97.1 可用

**一句话答案：**

可以。AFIT（**Async Function In Trait**，trait 中异步函数）在稳定版已经可用；但如果你要做复杂的对象安全设计、公开库 API 或跨版本兼容，仍需小心签名与 trait object 限制。

**解答：**

稳定写法：

```rust
trait Fetcher {
    async fn fetch(&self) -> String;
}

struct Demo;

impl Fetcher for Demo {
    async fn fetch(&self) -> String {
        "ok".to_string()
    }
}
```

调用端：

```rust
#[tokio::main]
async fn main() {
    let d = Demo;
    assert_eq!(d.fetch().await, "ok");
}
```

要特别说明的是：

- **stable**：trait 里直接 `async fn`。
- **不是这题重点、但常与它混淆**：把复杂 async trait 做成各种对象安全组合，仍要谨慎。

**Go 对比：**

```go
package main

type Fetcher interface {
	Fetch() string
}

func main() {}
```

- **Go 怎么做**：interface 方法直接返回结果；异步通常交给 goroutine 或 channel。
- **Rust 为什么不同**：Rust 把“以后返回结果”做成 future，所以 trait 里的 async 方法也会生成隐藏 future 类型。
- **Go 程序员易踩的坑**：别把 AFIT 理解成“trait object 上一切 async 都自然工作”；对象安全问题仍然存在。

**记忆点：**

- AFIT 在 Rust 1.97.1 stable。
- stable 不代表“所有配套高级玩法都自动简单”。

---

## Q12. 哪些 async 相关点是 stable，哪些是 nightly，哪些只是概念示意？ {#q12}
**Tags:** `advanced` `stability`
**适用版本:** Rust 1.97.1

**一句话答案：**

你日常写业务最常用的 async 能力基本都在 stable；nightly 主要集中在更底层、实验性或特殊抽象上。学习时要先把“能稳定用的主干”站稳。

**解答：**

按稳定性分成三份清单，学习时不要混着记：

**stable（生产主线可直接用）：**

- `async fn` / `async {}` / `.await`
- `async move {}`、async closure
- AFIT（trait 里 `async fn`，Rust 1.75+）
- Tokio 等 runtime 的 `spawn` / `join!` / `select!` / `spawn_blocking` / `LocalSet`

```rust
async fn stable_async() -> i32 {
    1
}

trait T {
    async fn f(&self) -> i32;
}

fn main() {}
```

**概念示意（帮助理解，不必当日常写法）：**

- 手写 `Future::poll`
- 手写 `Pin` / `Waker` / `Context` 细节
- 把 future 想成“状态机对象”的教学拆解

```rust
use std::task::Poll;

fn main() {
    // 概念示意：Poll 是协议结果，不是日常业务 API
    let _ = Poll::<i32>::Pending;
}
```

**nightly / 实验向（不要当生产默认）：**

- 依赖 `#![feature(...)]` 的底层 async 实验特性
- 高度特化、尚未稳定的 async trait / executor 实验抽象
- 博客里的“今晚刚合进 nightly”的新语法

```rust
fn main() {
    // 看到需要 #![feature(...)] 才能编过的 async 实验能力：
    // 先当学习材料，不要默认写进生产 crate。
}
```

**Go 对比：**

```go
package main

func main() {}
```

- **Go 怎么做**：Go 并发主干更集中，语言层心智负担更小。
- **Rust 为什么不同**：Rust 把 async 做成可组合的库级协议，因此术语更多，但可控性也更高。
- **Go 程序员易踩的坑**：一上来就钻 `poll`/`Pin` 底层，把主线 API 学习顺序打乱。

**记忆点：**

- 先学 stable 主线：`async fn`、`.await`、Tokio。
- 再学概念示意：`Future`、`Pin`、`Waker`。
- nightly 实验特性不要当生产默认。

---

## Q13. `#[tokio::main]` 到底帮我干了啥？ {#q13}
**Tags:** `hot` `tokio` `runtime`
**适用版本:** Tokio 1.x stable

**一句话答案：**

它帮你建一个 Tokio runtime，再在上面 `block_on` 你的 `async fn main`；没有它，你手里只有 future，没人持续 `poll`。

**解答：**

宏展开后的心智模型接近：

```text
// 伪展开（示意，不是让你手写）：
fn main() {
    tokio::runtime::Runtime::new()
        .unwrap()
        .block_on(async_main())
}

async fn async_main() { /* 你写的 async main 体 */ }
```

依赖与最常见写法：

```text
cargo add tokio --features macros,rt-multi-thread

#[tokio::main]
async fn main() {
    // 这里面的 .await 才有 executor 在驱动
}
```

没有 runtime 时，`async fn` 只是造出一个惰性 future（见 [Q1](#q1)、[Q3](#q3)）：

```rust
async fn work() -> i32 {
    1
}

fn main() {
    let _fut = work(); // 创建了，但没人 poll
}
```

```rust
fn main() {
    // 手工等价物要自己建 runtime 再 block_on；
    // #[tokio::main] 就是把这层样板代码藏掉。
}
```

常用变体：`#[tokio::main(flavor = "current_thread")]` 单线程；多线程默认更像“Go 启动时已有调度器”的体验。

**Go 对比：**

```go
package main

func main() {
	// Go 程序一启动就有 runtime；没有“先挂宏再建调度器”这一步
}
```

- **Go 怎么做**：runtime 是语言内建，`main` 天然可并发。
- **Rust 为什么不同**：async 是库级协议，runtime 要显式接入。
- **Go 程序员易踩的坑**：以为写了 `async fn main` 就自动跑；缺 `#[tokio::main]` 或等价 `block_on` 时通常编不过或什么都不发生。

**记忆点：**

- `#[tokio::main]` ≈ 建 runtime + `block_on`。
- 它不把 `async` 变成 goroutine，只是把执行器接上。

---

## Q14. 为什么 `Mutex` 不该跨 `await` 一直握着？ {#q14}
**Tags:** `hot` `mutex` `await`
**适用版本:** Rust 1.39+；Tokio 1.x stable

**一句话答案：**

跨 `.await` 握锁会把“等 IO / 等别的 future”的时间也算进临界区：同步 `Mutex` 还会占住 executor 线程；就算是异步锁，也会让别的任务长时间进不来。

**解答：**

坏味道（同步锁跨 await）：

```text
// 反模式示意（依赖 tokio）：
let guard = mutex.lock().unwrap(); // std::sync::Mutex
do_io().await;                     // 锁还握着
use_data(&*guard);
```

更好的形状：锁内只做短同步工作，`.await` 前后再拿数据：

```rust
use std::sync::{Arc, Mutex};

fn bump(counter: &Mutex<i32>) -> i32 {
    let mut g = counter.lock().unwrap();
    *g += 1;
    *g
}

fn main() {
    let c = Arc::new(Mutex::new(0));
    assert_eq!(bump(&c), 1);
}
```

```rust
fn main() {
    // 心智模型：
    // 1) 进临界区拿/改数据
    // 2) drop 锁
    // 3) 再 .await
    // 4) 如需再改，重新加锁
}
```

若临界区本身必须跨异步点，再用 `tokio::sync::Mutex`，并尽量缩到最短；别把“整个请求处理”都包在一把锁里。

**Go 对比：**

```go
package main

import "sync"

func main() {
	var mu sync.Mutex
	mu.Lock()
	// 在 Go 里跨 channel 接收握锁也容易饿死别人；同样不推荐
	mu.Unlock()
}
```

- **Go 怎么做**：锁住再 `select`/阻塞，一样会拖垮并发；靠约定尽快解锁。
- **Rust 为什么不同**：async 任务常共享少量线程，同步锁跨 await 的伤害更直接。
- **Go 程序员易踩的坑**：把 `MutexGuard` 当“请求级上下文”一直带着。

**记忆点：**

- 锁要短；`.await` 前先放下。
- 同步锁跨 await ≈ 卡住调度线程。

---

## Q15. 任务取消了，future 还会继续跑吗？`CancellationToken` / Drop 取消直觉 {#q15}
**Tags:** `common` `cancellation`
**适用版本:** Tokio 1.x；`CancellationToken` 常见于 `tokio-util`

**一句话答案：**

Rust async 是**协作式取消**：future 被 drop / 不再被 poll 后就不会继续推进；但它不会像杀线程那样强行中断——正在跑的同步代码、未检查取消点的逻辑仍可能跑完当前片段。

**解答：**

核心直觉：

```rust
fn main() {
    // 1) future 被 drop => 不再 poll => 异步推进停止
    // 2) 若 Drop 实现会关 socket / 释资源，取消常靠这条路径
    // 3) 没有“操作系统级杀掉这段 async 机器码”的默认开关
}
```

```rust
struct Work {
    done: bool,
}

impl Drop for Work {
    fn drop(&mut self) {
        self.done = true; // 取消时常靠 Drop 做清理
    }
}

fn main() {
    let w = Work { done: false };
    drop(w); // 类似“不再持有这个 future”
}
```

Tokio 任务：

```text
let handle = tokio::spawn(async { /* ... */ });
handle.abort(); // 请求取消：下次轮到它时以取消方式结束
// 仅 drop JoinHandle 默认不 abort 任务（任务可能继续在后台跑）
```

显式取消信号（`CancellationToken`，取消令牌）常见写法：

```text
// cargo add tokio-util --features rt
let token = CancellationToken::new();
let child = token.child_token();
tokio::spawn(async move {
    tokio::select! {
        _ = child.cancelled() => { /* 收到取消 */ }
        _ = do_work() => { /* 正常完成 */ }
    }
});
token.cancel();
```

这很像 Go 的 `context.Context`：取消是信号，业务要在 await / select 点响应。

**Go 对比：**

```go
package main

import (
	"context"
	"fmt"
)

func main() {
	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()
	select {
	case <-ctx.Done():
		fmt.Println("cancelled")
	default:
	}
}
```

- **Go 怎么做**：`context` + `select` 协作取消；也没有“杀掉 goroutine”的正规 API。
- **Rust 为什么不同**：取消往往落在“停 poll + Drop 清理”，再加显式 token/`abort`。
- **Go 程序员易踩的坑**：以为 `drop(handle)` 等于取消；Tokio 里常常要 `abort` 或自己传 token。

**记忆点：**

- 取消 = 不再 poll，不是杀线程。
- 需要可传播取消时，用 token / `abort` / `select!`。

---

## Q16. 超时、带截止时间的异步怎么写？（`tokio::time::timeout` 级说明） {#q16}
**Tags:** `common` `timeout`
**适用版本:** Tokio 1.x（需 `time` feature）

**一句话答案：**

用 runtime 的超时包装 future：超时到了就停止等待该 future（通常伴随 drop）；需要“整条调用链共享截止时间”时，再配合取消令牌或自己把 deadline 往下传。

**解答：**

最常见是 `timeout`：

```text
cargo add tokio --features macros,rt-multi-thread,time

use std::time::Duration;
use tokio::time::timeout;

let result = timeout(Duration::from_secs(1), do_work()).await;
match result {
    Ok(Ok(v)) => { /* 在时限内完成 */ }
    Ok(Err(e)) => { /* 业务错误 */ }
    Err(_elapsed) => { /* 超时：内层 future 已被 drop */ }
}
```

`select!` 也能手写“超时竞速”：

```text
tokio::select! {
    v = do_work() => { /* 完成 */ }
    _ = tokio::time::sleep(Duration::from_secs(1)) => { /* 超时分支 */ }
}
```

无依赖时，只记住协议层含义：超时就是“另一个先完成的 future 赢了，输家被 drop”。

```rust
fn main() {
    // 超时 ≠ 线程 sleep 打断
    // 超时 = 不再等待那个 future，并依赖 Drop 做清理
}
```

```rust
use std::time::Duration;

fn main() {
    let d = Duration::from_millis(10);
    assert!(d.as_millis() == 10);
}
```

**Go 对比：**

```go
package main

import (
	"context"
	"time"
)

func main() {
	ctx, cancel := context.WithTimeout(context.Background(), time.Second)
	defer cancel()
	_ = ctx
}
```

- **Go 怎么做**：`context.WithTimeout` / `WithDeadline` 向下传递。
- **Rust 为什么不同**：常用局部 `timeout(fut)`；跨多层时要自己传 token 或 deadline。
- **Go 程序员易踩的坑**：以为超时后后台逻辑一定立刻停；若内层在跑阻塞代码，仍可能拖一会儿。

**记忆点：**

- `timeout` / `select!` = 竞速取消。
- 超时后靠 drop 停止推进，不靠杀线程。

---

## Q17. `Stream` 和 Go 里读 channel 循环像不像？何时用？ {#q17}
**Tags:** `common` `stream`
**适用版本:** `futures` / Tokio 生态中的 Stream（非 std 内建日常 API）

**一句话答案：**

像：都是“异步地一个接一个取值直到结束”。Rust 的 **Stream**（流）是可组合的异步序列抽象；适合事件流、分块 IO、多值异步来源，不适合硬把“一次性 future”硬拧成流。

**解答：**

和 Go 的对应直觉：

```go
package main

func main() {
	ch := make(chan int)
	go func() {
		ch <- 1
		ch <- 2
		close(ch)
	}()
	for v := range ch {
		_ = v
	}
}
```

Rust 侧常见消费形状（依赖示意）：

```text
// futures / tokio_stream 一类 API：
while let Some(item) = stream.next().await {
    // 处理 item
}
// 或：stream.map(...).filter(...).try_collect().await
```

什么时候用 Stream：

- 多个异步值随时间到达（消息、帧、目录条目、订阅推送）
- 想对异步序列做 `map` / `filter` / `buffered` 这类组合

什么时候别用：

- 只要一个结果 → 普通 `async fn` / `Future` 就够
- 纯同步集合 → `Iterator`

```rust
fn main() {
    // Future：0 或 1 个结果
    // Stream：0 到多个结果，按时间展开
    // Iterator：多个结果，但拉取是同步的
}
```

```rust
fn main() {
    let items = vec![1, 2, 3];
    for x in items {
        assert!(x >= 1);
    }
}
```

**Go 对比：**

```go
package main

func main() {
	// for range ch  ≈ 消费 Stream
	// 但 Go 没有同等地位的“异步迭代器组合子库”作为语言默认
}
```

- **Go 怎么做**：channel + `for range` 是多值异步消费的默认故事。
- **Rust 为什么不同**：把“异步多值序列”做成 Stream trait，方便组合子。
- **Go 程序员易踩的坑**：把所有 channel 场景都翻译成 Stream；有时 `mpsc` + `recv().await` 循环更直白。

**记忆点：**

- Stream ≈ 异步版多值序列。
- 单次结果用 Future；多值异步序列才上 Stream。

---

## Q18. `multi_thread` 和 `current_thread` runtime 差在哪？`block_on` 能嵌套吗？ {#q18}
**Tags:** `common` `tokio` `runtime`
**适用版本:** Tokio 1.x stable

**一句话答案：**

`multi_thread` 用工作线程池调度 `Send` 任务；`current_thread` 只在当前线程跑。`block_on` 在已在 runtime 上下文里再嵌套调用，容易死锁或 panic，应改用 `.await` / `spawn`。

**解答：**

选型直觉：

- 默认服务、要并行 CPU/IO 任务 → `multi_thread`（`#[tokio::main]` 常见默认）
- 嵌入式、测试、明确单线程、或配合 `LocalSet` → `current_thread`

```text
// cargo add tokio --features macros,rt-multi-thread
#[tokio::main] // 默认 multi_thread
async fn main() {}

#[tokio::main(flavor = "current_thread")]
async fn main_single() {}
```

`block_on` 嵌套是高频坑：已在 async 任务里又 `Handle::current().block_on(...)`，可能占住工作线程等自己，形成死锁。正确姿势是直接 `.await`；同步代码要驱动 future，在**外面**建 runtime 再 `block_on` 一次（见 [Q13](#q13)、[Q21](#q21)）。

```rust
fn main() {
    // 心智模型：
    // multi_thread  = 线程池 + 可迁移任务
    // current_thread = 单线程事件循环
    // block_on 只在“同步边界”用一次，不要在 async 里再套
}
```

```rust
async fn add(a: i32, b: i32) -> i32 {
    a + b
}

fn main() {
    let n = futures::executor::block_on(add(1, 2));
    assert_eq!(n, 3);
}
```

**Go 对比：**

```go
package main

func main() {
	// Go 只有一套 runtime；没有 multi_thread / current_thread 口味选择
	// 也很少在“已在 goroutine 里”再手动嵌套一层调度入口
}
```

- **Go 怎么做**：语言内建调度，用户不选 flavor。
- **Rust 为什么不同**：runtime 是库，线程模型要显式选。
- **Go 程序员易踩的坑**：在 async 里再 `block_on`，相当于在已跑着的调度器里又卡死一层。

**记忆点：**

- 多线程池 vs 单线程循环，先按部署模型选。
- `block_on` 不嵌套；async 内用 `.await`。

---

## Q19. `std::sync::Mutex` 和 `tokio::sync::Mutex` 该怎么选？ {#q19}
**Tags:** `common` `mutex` `tokio`
**适用版本:** Rust 1.0+；Tokio 1.x stable

**一句话答案：**

临界区短、纯同步、不跨 `.await` → 用 `std::sync::Mutex`；必须在持锁期间 `.await` → 用 `tokio::sync::Mutex`，并尽量把锁持有缩到最短（见 [Q14](#q14)）。

**解答：**

同步锁在 async 里的危险：锁住后 `.await`，工作线程可能被占着睡，别的任务也跑不动。异步锁会在等待时交出线程，但价格更高，也更容易把“整段业务”糊进一把锁。

```rust
use std::sync::Mutex;

fn bump(m: &Mutex<i32>) -> i32 {
    let mut g = m.lock().unwrap();
    *g += 1;
    *g
}

fn main() {
    let m = Mutex::new(0);
    assert_eq!(bump(&m), 1);
}
```

```text
// 需要跨 await 时（依赖 tokio sync feature）：
// let guard = async_mutex.lock().await;
// do_io().await;
// drop(guard);
//
// 更推荐：
// let snapshot = { mutex.lock().unwrap().clone() }; // std 锁，短临界区
// do_io(snapshot).await;
```

**Go 对比：**

```go
package main

import "sync"

func main() {
	var mu sync.Mutex
	mu.Lock()
	// 尽快 Unlock；跨 channel 长时间持锁同样有害
	mu.Unlock()
}
```

- **Go 怎么做**：主要是一把 `sync.Mutex`；没有“async 专用 Mutex”的常用二分。
- **Rust 为什么不同**：executor 线程少，同步锁跨 await 伤害更大。
- **Go 程序员易踩的坑**：凡共享状态就上 `tokio::Mutex`；很多场景短同步锁更合适。

**记忆点：**

- 不跨 await → `std` Mutex。
- 必须跨 await → `tokio` Mutex，且锁要短。

---

## Q20. Tokio 的 `mpsc` / `oneshot` / `watch` 怎么选？ {#q20}
**Tags:** `common` `channel` `tokio`
**适用版本:** Tokio 1.x stable

**一句话答案：**

多消息队列用 `mpsc`；一次性请求/响应用 `oneshot`；“最新值广播给多个读者”用 `watch`。

**解答：**

对照选型：

| 通道 | 典型语义 | 像 Go 的什么 |
|------|----------|--------------|
| `mpsc` | 多生产者单消费者消息流 | 带缓冲/无缓冲 channel |
| `oneshot` | 只发送一次的结果槽 | 容量 1 的回复 channel |
| `watch` | 存一份最新状态，读者看最新 | 不太像；更接近“原子配置 + 变更通知” |

```text
// mpsc：任务间流水线
let (tx, mut rx) = tokio::sync::mpsc::channel(16);
tx.send(1).await?;
let v = rx.recv().await;

// oneshot：RPC 式一次回复
let (tx, rx) = tokio::sync::oneshot::channel();
tx.send(42)?;
let v = rx.await?;

// watch：配置/状态最新值
let (tx, mut rx) = tokio::sync::watch::channel("init");
tx.send("next")?;
rx.changed().await?;
let current = *rx.borrow();
```

```rust
fn main() {
    // 记忆口诀：
    // 很多消息 → mpsc
    // 一次结果 → oneshot
    // 只要最新 → watch
}
```

**Go 对比：**

```go
package main

func main() {
	ch := make(chan int, 16) // ≈ mpsc
	reply := make(chan int, 1)
	_ = ch
	_ = reply
}
```

- **Go 怎么做**：一个 `chan` 类型打天下，靠容量与约定区分用途。
- **Rust 为什么不同**：按通信模式拆成不同类型，减少误用。
- **Go 程序员易踩的坑**：用 `mpsc` 硬模拟“只回一次”或“只关心最新配置”，类型上更别扭。

**记忆点：**

- 流式消息 `mpsc`，一次性 `oneshot`，最新状态 `watch`。

---

## Q21. 同步代码里调异步、异步里调同步，正确姿势是什么？ {#q21}
**Tags:** `common` `blocking` `bridge`
**适用版本:** Tokio 1.x stable

**一句话答案：**

同步 → 异步：在边界建 runtime 并 `block_on`（或跑在已有 runtime 的 `Handle` 上）；异步 → 同步阻塞：用 `spawn_blocking`，不要直接在 async 里堵线程。

**解答：**

两条边界：

1. **同步调用异步**：`Runtime::new().block_on(fut)`，或 `Handle::current().block_on`（仅当你确定当前不在 async 任务里占着会自锁的线程）。库若可能在 async 上下文被调用，优先提供 `async fn`，别逼用户嵌套 `block_on`（见 [Q18](#q18)）。
2. **异步调用同步阻塞**：`tokio::task::spawn_blocking(|| heavy())`，再 `.await` 结果（见 [Q9](#q9)）。纯 CPU 短计算可以直接跑；长时间 sleep、文件大口同步读写、老阻塞 SDK 必须隔离。

```text
// 同步边界驱动 async：
let rt = tokio::runtime::Runtime::new().unwrap();
let v = rt.block_on(async { 1 + 1 });

// async 里跑阻塞：
let v = tokio::task::spawn_blocking(|| {
    std::thread::sleep(std::time::Duration::from_millis(10));
    7
})
.await
.unwrap();
```

```rust
async fn pure_async(x: i32) -> i32 {
    x + 1
}

fn main() {
    let n = futures::executor::block_on(pure_async(1));
    assert_eq!(n, 2);
}
```

**Go 对比：**

```go
package main

func main() {
	// Go 里同步函数直接调；阻塞时 runtime 仍会调度其它 goroutine
	// Rust async 线程更“贵”，阻塞要显式隔离
}
```

- **Go 怎么做**：同步/异步边界模糊，阻塞代价由 runtime 消化一部分。
- **Rust 为什么不同**：少量 worker 跑很多任务，阻塞会放大成全局卡顿。
- **Go 程序员易踩的坑**：在 `async fn` 里直接调阻塞 SDK，或在回调里嵌套 `block_on`。

**记忆点：**

- 同步入口 `block_on` 一次；异步里阻塞走 `spawn_blocking`。

---

## Q22. 为什么 `async fn` 里不能用 `std::thread::sleep`，该用 `tokio::time::sleep`？ {#q22}
**Tags:** `common` `sleep` `blocking`
**适用版本:** Tokio 1.x（`time` feature）

**一句话答案：**

`std::thread::sleep` 会把当前 OS 线程整段卡住，executor 上其它任务也跑不了；`tokio::time::sleep(...).await` 只让当前任务挂起，线程还能去跑别人。

**解答：**

这和 [Q9](#q9) 的阻塞原则是同一件事：async 任务共享有限线程。睡眠是最常见的“无意阻塞”。定时等待、超时、节流都应使用 runtime 定时器。

```text
// cargo add tokio --features macros,rt-multi-thread,time

#[tokio::main]
async fn main() {
    // 正确：异步睡眠
    tokio::time::sleep(std::time::Duration::from_millis(10)).await;
}

// 错误：堵住工作线程
// std::thread::sleep(std::time::Duration::from_secs(1));
```

```rust
use std::time::Duration;

fn main() {
    let d = Duration::from_millis(10);
    assert_eq!(d.as_millis(), 10);
    // 同步代码里用 thread::sleep 没问题；
    // 问题出在把它放进 async 任务共享的线程上。
}
```

若第三方 API 只能阻塞等待，把它包进 `spawn_blocking`，不要假装“睡一下没关系”。

**Go 对比：**

```go
package main

import "time"

func main() {
	time.Sleep(10 * time.Millisecond) // goroutine 睡，其它 goroutine 仍可被调度
}
```

- **Go 怎么做**：`time.Sleep` 阻塞的是当前 goroutine，runtime 会继续跑其它 goroutine。
- **Rust 为什么不同**：默认不是每个任务一条栈/线程；睡线程 ≈ 睡调度器份额。
- **Go 程序员易踩的坑**：把 `time.Sleep` 习惯原样换成 `std::thread::sleep`。

**记忆点：**

- async 里等时间 → `tokio::time::sleep().await`。
- `thread::sleep` 只留给真正的同步/阻塞线程。

---

## Q23. 为什么 async 里不该直接用 `std::fs`？该用什么？ {#q23}
**Tags:** `hot` `blocking` `filesystem`
**适用版本:** Tokio 1.x（`fs` / `rt` feature）

**一句话答案：**

`std::fs` 是同步阻塞 IO：会把当前 worker 线程卡住，和 [Q22](#q22) 的 `thread::sleep` 同一类坑。异步路径用 `tokio::fs`（或等价异步 API）；必须调用阻塞 SDK 时再用 `spawn_blocking`（见 [Q9](#q9)）。

**解答：**

async 任务通常很多、worker 线程很少。磁盘读写一旦同步卡住，那条线程上排队的其它 future 也推进不了——延迟会“传染”。网络用了 `async`、文件还用 `std::fs::read`，是高频翻车组合。

`std::fs` 是同步 API：调用会占用当前 OS 线程直到返回。

```rust
fn read_sync(path: &str) -> std::io::Result<Vec<u8>> {
    std::fs::read(path) // 阻塞到读完或出错
}

fn main() {
    // 同步 main / 专用线程里用没问题；问题出在塞进 async 任务共享的 worker
    let _ = read_sync;
}
```

把“阻塞读”收成普通闭包，便于丢进 `spawn_blocking`（示意边界，仍不引入 Tokio）：

```rust
fn blocking_read(path: String) -> std::io::Result<Vec<u8>> {
    std::fs::read(path)
}

fn main() {
    let job = || blocking_read("config.toml".into());
    let _ = job; // 真正异步里：spawn_blocking(job).await
}
```

异步路径正确方向（text 示意，需 Tokio）：

```text
// cargo add tokio --features macros,rt-multi-thread,fs

// ✅ 异步文件 API
// let data = tokio::fs::read("config.toml").await?;

// ✅ 逃不掉的阻塞库 / 大段同步逻辑
// let data = tokio::task::spawn_blocking(|| std::fs::read("config.toml"))
//     .await??;

// ❌ 直接在 async 任务里堵线程
// let data = std::fs::read("config.toml")?;
```

再强调一次“别在 async 里直接阻塞”的形状（可编译对照，与 [Q22](#q22) 同类）：

```rust
fn main() {
    // 这些都是“占住当前线程”的同步调用：
    // std::fs::read(...);
    // std::thread::sleep(...);
    // 在 async worker 上用它们会拖累同线程其它任务。
    assert!(true);
}
```

怎么选：

1. 有异步文件 API → 优先 `tokio::fs`（或 `async-std` 等，看你的 runtime）。
2. 只有同步 API / 计算很重 → `spawn_blocking`，再 `.await` 结果。
3. 极短、极少、且你清楚不会挤爆 runtime 的读——工程上仍不推荐当默认；默认按阻塞处理更安全。

这和“async 里别 `std::thread::sleep`”是同一条原则：别在异步调度线程上做会长时间占用 OS 线程的事。

**Go 对比：**

```go
package main

import "os"

func main() {
	_, _ = os.ReadFile("config.toml") // 阻塞当前 goroutine；其它 goroutine 仍可跑
}
```

- **Go 怎么做**：`os.ReadFile` 阻塞当前 goroutine，runtime 仍调度别人。
- **Rust 为什么不同**：默认 async 模型更“珍惜”线程；同步 fs 成本放大。
- **Go 程序员易踩的坑**：把 `os.ReadFile` 习惯原样换成 `std::fs::read` 塞进 `async fn`。

**记忆点：**

- async 读文件 → `tokio::fs` 或 `spawn_blocking`。
- `std::fs` 留给真正的同步上下文。

---

## Q24. `JoinSet` 适合干什么？和 `join!` / 多次 `spawn` 怎么选？ {#q24}
**Tags:** `common` `JoinSet` `spawn`
**适用版本:** Tokio 1.x（`rt` feature）

**一句话答案：**

`JoinSet`（动态任务集合）适合**运行期数量不固定**、要边 spawn 边收割结果/错误的一批任务；`join!` 适合编译期固定的少数几个 future；“只 fire-and-forget”用多次 `tokio::spawn` 也行，但收结果/统一取消时 `JoinSet` 更顺手。

**解答：**

`join!(a, b, c)` 要你在写法上就摆好三个 future；任务个数来自 `Vec`、配置、请求列表时就别硬掰。固定少数个时，先想 `join!`：

```rust
async fn two_steps() -> (i32, i32) {
    // 真实项目：tokio::join!(a(), b())
    // 这里用手写顺序示意“固定数量”的形状
    let a = async { 1 }.await;
    let b = async { 2 }.await;
    (a, b)
}

fn main() {
    let _ = two_steps;
}
```

动态 N 个时，用列表驱动更自然（仍不绑 Tokio 类型）：

```rust
async fn fanout(n: usize) -> Vec<usize> {
    let mut out = Vec::with_capacity(n);
    for i in 0..n {
        out.push(async { i }.await);
    }
    out
}

fn main() {
    let _ = fanout;
}
```

真正的 `JoinSet` API（text，需 Tokio）：

```text
// 概念示意（需 Tokio runtime）：
use tokio::task::JoinSet;

// let mut set = JoinSet::new();
// for i in 0..n {
//     set.spawn(async move { do_work(i).await });
// }
// while let Some(res) = set.join_next().await {
//     let _ = res?; // JoinError 或任务返回值
// }
```

怎么挑：

| 场景 | 更合适 |
|------|--------|
| 固定 2～3 个异步步骤 | `join!` / `try_join!`（见 [Q8](#q8)） |
| 动态 N 个、要收齐结果 | `JoinSet` |
| 只要丢进 runtime、偶尔 `JoinHandle` | 多次 `tokio::spawn` |
| 要抢第一个完成 / 取消其它 | `select!` 或自行组合取消（见 [Q8](#q8)、[Q15](#q15)） |

`JoinSet` 还能在 drop 时中止未完成任务（具体行为以当前 Tokio 文档为准）；写“请求扇出再汇总”时，它比手搓 `Vec<JoinHandle<_>>` 少很多样板。

**Go 对比：**

```go
package main

import "sync"

func main() {
	var wg sync.WaitGroup
	// 或 errgroup：动态开 goroutine，再 Wait 收错误
	_ = wg
}
```

- **Go 怎么做**：`WaitGroup` / `errgroup` 管动态一批 goroutine。
- **Rust 为什么不同**：future 要显式挂到 runtime；`JoinSet` 把 spawn + 收割绑在一起。
- **Go 程序员易踩的坑**：用固定参数的 `join!` 硬拼动态任务列表。

**记忆点：**

- 动态一批任务 → `JoinSet`。
- 固定少数 future → `join!`。
- 和 `spawn` / 取消语义一起看，别只当“WaitGroup”。

---

## Q25. `StreamExt::next` 从哪来？为什么光有 `Stream` 不够？ {#q25}
**Tags:** `common` `Stream` `StreamExt` `futures`
**适用版本:** `futures` / `tokio-stream` 等生态（非 std 内建）

**一句话答案：**
`next()` **不是** `Stream` trait 上的方法，而是 **`StreamExt`**（流扩展 trait）提供的异步便利方法。只 `use` 了实现 `Stream` 的类型、却没导入 `StreamExt`，就会发现写不出 `stream.next().await`。HTTP 响应体分块等场景见 [40-http-client-and-server](40-http-client-and-server.md)。

**解答：**
分工可以记成：

| 角色 | 做什么 |
|------|--------|
| `Stream` | 核心：`poll_next`（底层轮询下一个元素） |
| `StreamExt` | 糖：`next`、`map`、`filter`、`collect`… 把 poll 包成 `.await` 友好 API |

概念用法（text，需 futures / tokio_stream）：

```text
// 常见：
use futures::stream::StreamExt; // 或 tokio_stream::StreamExt
// while let Some(item) = my_stream.next().await { ... }

// 只有 Stream、没有 StreamExt 时：
// my_stream.next()  ← 方法不存在（除非别处也提供了 next）
```

和 [Q17](#q17) 的关系：Q17 讲“何时用 Stream”；本题讲“为什么示例里总要多 `use ...StreamExt`”。

无依赖对照——同步世界里 `Iterator` 与方法的关系类似“trait 提供能力，prelude/扩展提供常用方法”，但 async 侧扩展往往**不在 prelude**，要自己 `use`：

```rust
fn main() {
    let mut it = [1, 2, 3].into_iter();
    // Iterator::next 在 prelude 里够用
    assert_eq!(it.next(), Some(1));
}
```

```rust
fn main() {
    // 异步多值 ≈ Stream；同步多值 ≈ Iterator
    // 差别：Stream 的“取下一个”要 .await，且 next 常来自 Ext
    let v = vec![10, 20];
    assert_eq!(v.iter().copied().sum::<i32>(), 30);
}
```

**Go 对比：**

```go
package main

func main() {
	ch := make(chan int, 1)
	ch <- 1
	close(ch)
	for v := range ch {
		_ = v // 语言内建，没有“再 import 一个 Ext”
	}
}
```

- **Go 怎么做**：`for range` channel 是语法级支持。
- **Rust 为什么不同**：`Stream` 保持最小；组合子放在 `StreamExt`，按需导入。
- **Go 程序员易踩的坑**：复制了 `while let Some(x) = s.next().await`，漏了 `use StreamExt`，编译器报 `next` 找不到。

**记忆点：**
- 要 `.next().await` → `use StreamExt`（futures 或 tokio_stream）。
- `Stream` 负责 poll；`StreamExt` 负责好用的异步 API。

---
