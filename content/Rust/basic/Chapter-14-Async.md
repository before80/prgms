+++
title = "第 14 章 异步编程"
weight = 140
date = "2026-03-27T17:24:46+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 第 14 章 异步编程（Async/Await）

> "如果说多线程是'分身术'，那 async/await 就是'影分身术'——不需要真正的多个身体，只需要一个身体就能同时处理多个任务。它不占用你的查克拉（系统资源），但能让你像孙悟空一样同时变出好几个自己来干活。"

在并发编程的世界里，我们有两种主要方法：

1. **多线程**：真正的并行，每个线程同时执行
2. **异步编程**：协作式并发，多个任务在同一个线程上交替执行

多线程就像**多个厨师同时在厨房里炒菜**，而异步编程就像**一个超级厨师，快速切换着同时管理多口锅**。

异步编程特别适合 **I/O 密集型**任务——比如网络请求、文件读写、数据库查询。这些任务的特点是：**大部分时间都在等待**，而不是在计算。

想象你要烧开水、淘米、洗菜：
- **多线程**的方式：请三个厨师分别做这三件事
- **异步**的方式：一个厨师先烧水，水还没开的时候去淘米，淘完米再回去看水开了没……

Rust 的 async/await 语法就是让你用同步的写法，写出异步的程序。

这一章，我们来揭开 Rust 异步编程的神秘面纱！

> **关于本章的代码示例**
>
> Rust 标准库只提供 async/await 的语法和 `Future` trait，**并不自带异步运行时**。本章绝大多数示例都依赖第三方运行时（最常见的是 [tokio](https://tokio.rs)）。
>
> 请先在 `Cargo.toml` 里加上依赖：
>
> ```toml
> [dependencies]
> tokio = { version = "1", features = ["full"] }
> ```
>
> 这些示例在本书中标注为 `rust,ignore`，意思是「需要配合运行时依赖才能编译运行」。直接用 `rustc` 单独编译会报 `unresolved import tokio` 之类的错误，这是正常的。

---

## 14.1 异步编程基础

### 14.1.1 同步 vs 异步编程模型

#### 14.1.1.1 阻塞 I/O（线程等待 I/O 时阻塞）

传统的同步 I/O，当你在等一个网络请求返回时，整个线程都被卡住：

```rust
// 同步阻塞的代码（假设 Data 是已定义的数据结构）
fn fetch_data() -> Data /* Data 为假设的类型 */ {
    let response = blocking_http_get("https://example.com"); // 这行会阻塞整个线程
    // 线程在这里干等，不知道过了多久
    parse(response)
}
```

> **问题**：如果线程在等待时什么都不做，那就是**资源浪费**。一个服务器有成千上万个连接，如果每个连接都占用一个线程，那内存很快就爆了。

#### 14.1.1.2 非阻塞 I/O（I/O 操作立即返回，轮询状态）

非阻塞 I/O 的做法是调用后立刻返回、由程序反复询问是否就绪，逻辑简单但容易空转。

```rust
// 非阻塞 I/O 的伪代码
fn fetch_data() -> Option<Data> {
    // 发起请求，立即返回
    let request = async_http_get("https://example.com");
    
    // 轮询检查是否完成
    loop {
        if request.is_ready() {
            return Some(request.get_result());
        }
        // 继续干别的事，或者短暂等待
    }
}
```

> **问题**：轮询会消耗 CPU，而且代码会变得很丑陋（回调炼狱）。

#### 14.1.1.3 事件驱动 / 回调（JavaScript / Node.js）

事件驱动模型把「等数据」变成「注册回调」，Node.js 正是靠它在单线程里撑起高并发。

```javascript
// JavaScript 风格的回调
function fetchData(callback) {
    http.get("https://example.com", function(response) {
        callback(response);
    });
}

fetchData(function(data) {
    console.log("收到数据:", data);
});
```

> **问题**：回调地狱——当你需要链式调用多个异步操作时，代码会变成：
> ```javascript
> fetchUser(userId, function(user) {
>     fetchPosts(user.id, function(posts) {
>         fetchComments(posts[0].id, function(comments) {
>             // 地狱！
>         });
>     });
> });
> ```

#### 14.1.1.4 async / await（协程模型，同步写法，异步执行）

Rust 的 async/await 让你用同步的风格写代码，但底层是异步执行：

```rust
// 注意：以下为示意代码，Data、http_get、parse 需自行定义
async fn fetch_data() -> Data /* Data 为假设的业务数据类型 */ {
    // 看起来像同步代码
    let response = http_get("https://example.com").await; // 但这里不会阻塞整个线程
    parse(response)
}
```

**await** 的魔法在于：它会让出控制权，允许其他任务执行，直到等待的操作完成。

---

### 14.1.2 Future Trait

#### 14.1.2.1 trait Future { type Output; fn poll(self: Pin<&mut Self>, cx: &mut Context) -> Poll<Self::Output>; }

`Future` 是 Rust 异步的核心：

```rust
// Future trait 的定义（简化版）
pub trait Future {
    type Output;
    
    fn poll(self: Pin<&mut Self>, cx: &mut Context) -> Poll<Self::Output>;
}
```

**poll** 方法的返回值是 `Poll`：

```rust
pub enum Poll<T> {
    Ready(T),   // Future 已完成，结果是 T
    Pending,    // Future 还没完成，需要继续等待
}
```

#### 14.1.2.2 Poll<T> 枚举：Ready(T)（已完成）/ Pending（未完成）

`Poll` 是异步世界的开关：`Ready(T)` 表示算完了，`Pending` 表示稍后再问一次。

```rust
use std::task::{Poll, Context};
use std::pin::Pin;

fn main() {
    // Future 可能返回 Pending 或 Ready
    let poll: Poll<i32> = Poll::Ready(42);
    
    match poll {
        Poll::Ready(value) => println!("完成了: {}", value), // 完成了: 42
        Poll::Pending => println!("还在等待..."),
    }
}
```

#### 14.1.2.3 poll 方法的语义（轮询直到完成）

Future 的工作方式：

1. 当 Future 被调用 `poll` 时，如果能立即完成，返回 `Ready(result)`
2. 如果不能立即完成，返回 `Pending`，并注册 `Waker` 以便稍后被唤醒
3. 当操作完成时，底层系统调用 `Waker.wake()` 通知运行时
4. 运行时再次调用 `poll`，直到返回 `Ready`

---

### 14.1.3 async / await 语法

#### 14.1.3.1 async fn 函数（返回 impl Future）

`async fn` 的返回类型是一个实现了 `Future` 的匿名类型；调用它只是创建 Future，并不会立刻执行。

```rust
// async fn 返回一个 Future
async fn hello() -> String {
    String::from("hello")
}

// 上面的 async fn 大致等价于：
fn hello() -> impl Future<Output = String> {
    async { String::from("hello") }
}
```

#### 14.1.3.2 .await 语法（等待 Future 完成）

`.await` 把推进 Future 的工作交给执行器，直到它返回 `Ready` 才继续往下走。

```rust
// 注意：以下为示意代码，Data、fetch_from_network、parse 需自行定义
async fn get_data() -> Data /* Data 为假设的业务数据类型 */ {
    let response = fetch_from_network().await; // 等待异步操作完成
    parse(response)
}
```

**注意**：`.await` 只能在 `async fn` 或 async 块中使用。

#### 14.1.3.3 async 块：async { ... } / async move { ... }（获取环境变量的所有权）

`async` 块同样返回 Future；加上 `move` 会把用到的变量所有权搬进这个块里。

```rust
use std::future::Future;

fn main() {
    // 匿名 async 块
    let future = async {
        println!("异步块开始");
        // 这里可以 await
        println!("异步块结束");
    };
    
    // async move 块：获取环境变量的所有权
    let data = vec![1, 2, 3];
    let future_with_move = async move {
        // data 的所有权被移入 async 块
        println!("data: {:?}", data);
    };
    
    println!("Future 创建完成");
}
```

---

### 14.1.4 Future 的执行原理

#### 14.1.4.1 轮询（Poll）机制（Future 被 poll 才执行）

Future 是**惰性的**——不调用 `poll`，它就不会执行：

```rust
async fn compute() -> i32 {
    println!("开始计算...");
    42
}

fn main() {
    let future = compute();
    println!("Future 创建了，但还没执行");
    // 注意：compute() 返回的是 Future，不是 i32
    // 如果不用 .await 或 executor，println! 不会打印
}
```

#### 14.1.4.2 运行时（Runtime）驱动轮询

需要一个**执行器（Executor）**来驱动 Future：

```rust,ignore
use tokio;

#[tokio::main]
async fn main() {
    async fn compute() -> i32 {
        println!("开始计算...");
        42
    }
    
    let result = compute().await;
    println!("结果: {}", result); // 结果: 42
}
```

#### 14.1.4.3 Waker 唤醒机制（I/O 完成后调用 wake）

`Waker` 是执行器与 Future 之间的通知渠道：I/O 就绪后调用 `wake`，执行器就会回来再 poll 一次。

```rust
use std::task::{Context, Poll};
use std::future::Future;
use std::pin::Pin;
use std::sync::atomic::{AtomicBool, Ordering};
use std::sync::Arc;
use std::thread;
use std::time::Duration;

// 一个简单的 Future 实现：模拟异步操作
struct MyFuture {
    completed: bool,
    started: Arc<AtomicBool>, // 确保只启动一次后台线程
}

impl Future for MyFuture {
    type Output = i32;
    
    fn poll(mut self: Pin<&mut Self>, cx: &mut Context) -> Poll<Self::Output> {
        if self.completed {
            Poll::Ready(42)
        } else {
            // 防止 poll 被多次调用时重复启动线程
            if self.started.swap(true, Ordering::SeqCst) {
                return Poll::Pending; // 已经在等待了，直接返回
            }
            
            let waker = cx.waker().clone();
            thread::spawn(move || {
                thread::sleep(Duration::from_millis(100));
                waker.wake(); // 通知执行器再次 poll
            });
            Poll::Pending
        }
    }
}
```

---

### 14.1.5 Waker 与任务唤醒

> 🧙‍♂️ **Waker** 是 Rust async 世界里的"闹钟服务员"——Future 告诉它"等事情完成了叫我"，然后就回去睡觉（Pending）。事情完成后，Waker 就过来拍拍你："嘿，醒醒，该继续 poll 了！"

#### 14.1.5.1 Context 参数（包含 Waker）

`poll` 方法接收的 `Context` 包含 `Waker`：

```rust
fn poll(self: Pin<&mut Self>, cx: &mut Context) -> Poll<Self::Output>
```

#### 14.1.5.2 Waker::wake / wake_by_ref（唤醒等待的任务）

`wake` 会消耗 `Waker` 自身，`wake_by_ref` 则保留它，可以重复唤醒。

```rust
use std::task::{Context, Poll, Waker};

fn main() {
    let waker: Waker = todo!(); // 通常由 Context 提供
    
    // 唤醒任务
    waker.wake();
    
    // wake_by_ref 不获取所有权
    let waker_ref: &Waker = &waker;
    waker_ref.wake_by_ref();
}
```

#### 14.1.5.3 Waker 的克隆与存储（跨线程传递）

`Waker` 是 `Send + Sync` 的，可以克隆一份交给别的线程保存，等事件到达时再唤醒。

```rust
use std::task::{Context, Waker};
use std::sync::Arc;

fn main() {
    // Waker 必须实现 Clone，这样才能存储和传递
    let waker1: Waker = todo!();
    let waker2 = waker1.clone();
    
    // 跨线程传递 Waker
    let waker_arc = Arc::new(waker1);
    let waker_for_thread = Arc::clone(&waker_arc);
    
    std::thread::spawn(move || {
        // 注意：Waker::wake(self) 按值接收，不能从 Arc 里移出来，
        // 所以这里用 wake_by_ref。
        waker_for_thread.wake_by_ref();
    });
}
```

---

### 14.1.6 Pin<T> 与自引用结构

#### 14.1.6.1 Pin::new / Pin::new_unchecked / Pin::get_unchecked(&mut self)（获取 &mut T，unsafe，调用处必须保证 T: Unpin）

**Pin** 确保某个值在内存中**不会被移动**——它就像给你的数据上了把锁，防止有人把它从原地搬走。自引用结构最需要这东西，因为一旦移动，指针就指向了垃圾地址，指哪哪爆炸 💥。

```rust
use std::pin::Pin;
use std::marker::PhantomPinned;

fn main() {
    // Pin::new 要求 T: Unpin
    let num = 42;
    let pinned = Pin::new(&num); // OK: i32 是 Unpin
    
    // 对于 !Unpin 类型，需要用 Pin<Box<T>> 来固定
    // 注意：raw pointer 字段本身是 !Unpin，所以包含它的结构体也是 !Unpin
    // PhantomPinned 只是另一种明确标记 !Unpin 的方式
    struct SelfRef {
        data: String,
        _pinned: PhantomPinned, // 有了这个，SelfRef 才变成 !Unpin
    }
    
    impl SelfRef {
        fn new(data: String) -> Self {
            SelfRef {
                data,
                _pinned: PhantomPinned,
            }
        }
    }
    
    let mut sr = SelfRef::new(String::from("hello"));
    // 注意：sr 本身是 !Unpin，不能直接用 Pin::new
    // 必须用 Pin<Box<T>> 来固定它
    let mut pinned_sr = Box::pin(sr);
    // 现在 pinned_sr 被固定了，编译器会阻止你移动它
    // 注意：Box::pin(sr) 后，sr 被移走，无法再使用
}
```

#### 14.1.6.2 Unpin marker trait（可Pin任意位置）

`Unpin` 表示类型可以安全移动；绝大多数类型自动实现它，因此普通 Future 不受 `Pin` 约束。

```rust
fn main() {
    // 大部分类型都是 Unpin，可以随意移动
    fn assert_unpin<T: Unpin>() {}
    
    assert_unpin::<i32>();
    assert_unpin::<String>();
    assert_unpin::<Vec<u8>>();
    
    // !Unpin 的类型：PhantomPinned（以及包含它的结构体）
    // assert_unpin::<PhantomPinned>(); // 编译失败
    
    // ⚠️ 注意：raw pointer 字段本身是 !Unpin！
    // 因此包含 raw pointer 字段的结构体默认也是 !Unpin，
    // 必须显式使用 PhantomPinned（或手动实现 !Unpin）来明确标记。
}
```

#### 14.1.6.3 Pin<&mut T>（固定在内存位置的自引用安全）

`Pin<&mut T>` 保证 `T` 不再被移动，这是自引用结构（例如被 `await` 跨过的局部变量）能安全存在的前提；`PhantomPinned` 用来主动放弃 `Unpin`。

```rust
use std::pin::Pin;   // 注意：不能写成 use std::pin::{Pin, Pin::*}; 这不是合法语法
use std::marker::PhantomPinned;

struct SelfReferential {
    name: String,
    // 自引用字段需要 PhantomPinned 才能成为 !Unpin
    _pinned: PhantomPinned,
}

impl SelfReferential {
    fn new(name: String) -> Self {
        SelfReferential {
            name,
            _pinned: PhantomPinned,
        }
    }
    
    fn get_name(self: Pin<&Self>) -> &str {
        // 注意：这里用 self: Pin<&Self> 而非 &self
        // 因为只有 !Unpin 类型才需要通过 Pin 来安全访问
        &self.get_ref().name
    }
}

fn main() {
    // 自引用结构用 Box::pin 固定，这是 !Unpin 类型正确的方式
    let mut pinned_sr = Box::pin(SelfReferential::new(String::from("hello")));

    // 安全地读取（Pin<&Self> 上的方法）
    println!("name: {}", pinned_sr.as_ref().get_name()); // name: hello

    // 需要 &mut T 时用 unsafe 的 get_unchecked_mut（稳定版可用）
    unsafe {
        let sr_mut = Pin::get_unchecked_mut(pinned_sr.as_mut());
        sr_mut.name.push_str(" world");
        println!("name: {}", sr_mut.name); // name: hello world
    }
}
```

#### 14.1.6.4 async 块中的自引用问题（yield point 前的局部变量）

async 块在 `.await` 点会产生自引用问题：

```rust
async fn problematic() {
    let data = String::from("hello");
    
    // 在 yield point 之前，如果 data 被移走...
    some_async_operation().await;
    
    // ...但 async 块需要保留 data 的引用
    // 这个引用在 await 期间可能失效
}
```

解决方案：把数据放在结构体里，或者使用 `Pin`：

```rust
use std::pin::Pin;

struct AsyncData {
    data: String,
}

impl AsyncData {
    async fn process(self: Pin<&mut Self>) {
        // self 被 Pin 固定，不会移动
        println!("处理: {}", self.data);
    }
}
```

---

## 14.2 异步生态核心

### 14.2.1 Tokio 运行时（最流行的 async 运行时）

#### 14.2.1.1 #[tokio::main] / tokio::spawn

**Tokio** 是 Rust 最流行的异步运行时：

```rust,ignore
#[tokio::main]
async fn main() {
    println!("Tokio 运行时启动了！");
    
    // 创建异步任务
    let handle = tokio::spawn(async {
        println!("在 spawned 任务中");
        42
    });
    
    // 等待任务完成
    let result = handle.await.unwrap();
    println!("结果: {}", result); // 结果: 42
}
```

#### 14.2.1.2 multi_thread vs single_thread（多线程/单线程运行时）

tokio 默认是多线程运行时，任务可以分散到多个工作线程；`single_thread` 则全部在一个线程里跑，适合要求 `!Send` 的场合。

```rust,ignore
// 多线程运行时（默认）
#[tokio::main(flavor = "multi_thread")]
async fn main() {
    println!("线程数: {:?}", tokio::runtime::Handle::current().num_workers());
}

// 单线程运行时
#[tokio::main(flavor = "single_thread")]
async fn main() {
    println!("单线程模式");
}
```

#### 14.2.1.3 Runtime 配置（work-stealing 调度器）

`Builder` 可以精确配置运行时：工作线程数量、调度方式、线程名等。

```rust,ignore
use tokio::runtime::Builder;

fn main() {
    let rt = Builder::new_multi_thread()
        .worker_threads(4)           // 4 个工作线程
        .enable_io()                  // 启用异步 I/O
        .enable_time()                // 启用异步时间
        .thread_name("my-tokio-worker")
        .build()
        .unwrap();
    
    rt.block_on(async {
        println!("自定义 Tokio 运行时！");
    });
}
```

#### 14.2.1.4 任务本地存储：tokio::task::LocalKey

`task_local!` 给每个任务准备一份独立数据，用法类似线程局部存储，但作用域是任务。

```rust,ignore
// ⚠️ 依赖 tokio：Cargo.toml 里需要加 tokio = { version = "1", features = ["full"] }
use tokio::task_local;

task_local! {
    static REQUEST_ID: u32;
}

#[tokio::main]
async fn main() {
    // ⚠️ 无初始值的 task-local 变量只能在 scope() 内部访问。
    // 直接用 .with() 会报「cannot find value REQUEST_ID」。
    REQUEST_ID
        .scope(42, async {
            REQUEST_ID.with(|id| println!("当前任务中的 REQUEST_ID: {}", *id));

            let handle = tokio::spawn(async {
                // 注意：tokio::spawn 出来的新任务不会继承 task-local，
                // 所以这里要用 try_with，它返回 Result 而不是 panic。
                REQUEST_ID
                    .try_with(|id| println!("spawned 任务中: {}", *id))
                    .ok();
            });

            handle.await.unwrap();
        })
        .await;
}
```

---

### 14.2.2 async-std 运行时

#### 14.2.2.1 #[async_std::main] / async_std::spawn

**async-std** 是另一个流行的异步运行时，设计上与标准库 API 对齐：

```rust,ignore
use async_std::task;

fn main() {
    task::block_on(async {
        println!("async-std 运行时！");
        
        let handle = task::spawn(async {
            42
        });
        
        println!("结果: {}", handle.await);
    });
}
```

#### 14.2.2.2 std API 对齐设计（熟悉 std 的开发者友好）

async-std 的设计哲学是"让 async 代码看起来像 sync 代码"：

```rust,ignore
// async-std 的 fs 模块跟 std::fs 很像
use async_std::fs;

async fn read_file() -> std::io::Result<String> {
    fs::read_to_string("Cargo.toml").await
}
```

---

### 14.2.3 smol 轻量级运行时

#### 14.2.3.1 smol 简介（极简设计，可嵌入）

**smol** 是一个极简的异步运行时，设计用于嵌入式系统：

```rust,ignore
use smol::Timer;
use std::time::Duration;

fn main() {
    smol::block_on(async {
        println!("smol 运行时启动！");
        
        // 异步定时器
        Timer::after(Duration::from_secs(1)).await;
        println!("1 秒后...");
    });
}
```

---

## 14.3 异步任务管理

### 14.3.1 tokio::spawn 任务创建

#### 14.3.1.1 JoinHandle<T> 返回值（可等待任务完成）

`tokio::spawn` 返回 `JoinHandle`，`.await` 它就能拿到任务返回值。

```rust,ignore
#[tokio::main]
async fn main() {
    let handle = tokio::spawn(async {
        // 返回值类型会自动推断
        42
    });
    
    // JoinHandle 可以 await
    let result = handle.await.unwrap();
    println!("任务结果: {}", result); // 42
}
```

#### 14.3.1.2 任务的生命周期（spawned 任务独立执行）

被 spawn 出去的任务独立于当前 Future 运行，因此它不能借用栈上的局部变量。

```rust,ignore
#[tokio::main]
async fn main() {
    let handle = tokio::spawn(async {
        tokio::time::sleep(std::time::Duration::from_secs(1)).await;
        println!("任务完成");
        "done"
    });
    
    // 任务在后台独立运行
    println!("主任务继续执行");
    
    // 等待任务完成
    let result = handle.await.unwrap();
    println!("结果: {}", result); // done
}
```

---

### 14.3.2 tokio::join! / try_join!

#### 14.3.2.1 join!（并发执行多个 Future，全部完成后返回结果元组）

`join!` 让多个 Future 并发推进，全部结束后按顺序返回结果元组。

```rust,ignore
#[tokio::main]
async fn main() {
    let (a, b, c) = tokio::join! {
        async { 1 },
        async { 2 },
        async { 3 },
    };
    
    println!("{} + {} + {} = {}", a, b, c, a + b + c); // 1 + 2 + 3 = 6
}
```

#### 14.3.2.2 try_join!（任一 Future 返回 Err 则整体立即返回 Err）

`try_join!` 在任意一个 Future 返回 `Err` 时立刻返回该错误，不再等待剩下的。

```rust,ignore
#[tokio::main]
async fn main() {
    async fn may_fail(succeed: bool) -> Result<i32, &'static str> {
        if succeed {
            Ok(42)
        } else {
            Err("失败了")
        }
    }
    
    // 全部成功
    let (a, b) = tokio::try_join!(
        may_fail(true),
        may_fail(true),
    ).unwrap();
    println!("成功: {}, {}", a, b);
    
    // 其中一个失败
    let result = tokio::try_join!(
        may_fail(true),
        may_fail(false), // 这里会失败
    );
    
    match result {
        Ok(_) => println!("全部成功"),
        Err(e) => println!("失败了: {}", e), // 失败了: 失败了
    }
}
```

---

### 14.3.3 tokio::select! 多路复用

#### 14.3.3.1 select! 基本语法（等待多个 Future 任意一个完成）

`select!` 同时等待多个分支，谁先就绪就执行谁，其余分支被取消。

```rust,ignore
#[tokio::main]
async fn main() {
    tokio::select! {
        _ = tokio::time::sleep(std::time::Duration::from_millis(100)) => {
            println!("超时！");
        }
        _ = async { println!("任务 A 完成"); } => {
            println!("任务 A 最先完成");
        }
        _ = async { println!("任务 B 完成"); } => {
            println!("任务 B 最先完成");
        }
    }
}
```

#### 14.3.3.2 biased（按定义顺序而非随机）

默认情况下 `select!` 随机挑选就绪分支；加上 `biased` 后改为按书写顺序检查。

```rust,ignore
#[tokio::main]
async fn main() {
    tokio::select! {
        biased; // 优先选择前面的分支
        
        _ = task_a() => println!("A 赢了"),
        _ = task_b() => println!("B 赢了"),
        _ = task_c() => println!("C 赢了"),
    }
}
```

#### 14.3.3.3 loop { select! { ... } }（持续多路复用）

把 `select!` 放进 `loop` 就是经典的事件循环：反复等待并处理最先到达的事件。

```rust,ignore
#[tokio::main]
async fn main() {
    let mut counter = 0;
    
    loop {
        tokio::select! {
            _ = tokio::time::sleep(std::time::Duration::from_millis(100)) => {
                counter += 1;
                println!("计数器: {}", counter);
                if counter >= 5 {
                    break;
                }
            }
        }
    }
    
    println!("循环结束");
}
```

#### 14.3.3.4 返回值处理

`select!` 本身也是表达式，各分支返回值类型一致时可以直接把结果接出来。

```rust,ignore
#[tokio::main]
async fn main() {
    let result = tokio::select! {
        v = async { 42 } => v * 2,
        v = async { 100 } => v / 2,
    };
    
    println!("结果: {}", result); // 可能是 84 或 50（随机）
}
```

---

### 14.3.4 任务取消

#### 14.3.4.1 CancellationToken（协作式取消，tokio_util::sync::CancellationToken）

`CancellationToken` 提供协作式取消：一处 `cancel()`，所有监听它的任务都会收到通知。

```rust,ignore
use tokio_util::sync::CancellationToken;

#[tokio::main]
async fn main() {
    let token = CancellationToken::new();
    let child_token = token.child_token();
    
    let handle = tokio::spawn(async {
        tokio::select! {
            _ = tokio::time::sleep(std::time::Duration::from_secs(10)) => {
                println!("睡眠完成");
            }
            _ = child_token.cancelled() => {
                println!("任务被取消！");
            }
        }
    });
    
    // 取消子令牌
    child_token.cancel();
    
    handle.await.unwrap();
}
```

#### 14.3.4.2 select! 中的取消分支

把 token 的 `cancelled()` 写进 `select!` 分支，就能在等待业务 Future 的同时响应取消。

```rust,ignore
#[tokio::main]
async fn main() {
    let operation = tokio::time::sleep(std::time::Duration::from_secs(10));
    
    tokio::select! {
        _ = operation => {
            println!("操作完成");
        }
        // 可以添加取消分支
    }
}
```

#### 14.3.4.3 资源清理（Drop / guard）

任务被取消或 panic 时，栈上变量的 `Drop` 照常执行，因此 RAII 风格的清理依然可靠。

```rust,ignore
// ⚠️ 依赖 tokio：Cargo.toml 里需要加 tokio 依赖。
// 假设有一个需要显式释放的资源类型（RAII 风格）
struct SomeResource;

impl SomeResource {
    fn acquire() -> Self {
        println!("获取资源");
        SomeResource
    }
}

impl Drop for SomeResource {
    fn drop(&mut self) {
        println!("释放资源");
    }
}

#[tokio::main]
async fn main() {
    let guard = SomeResource::acquire();
    
    // 如果这里发生 panic，guard 会在栈展开时自动释放（Drop）
    tokio::time::sleep(std::time::Duration::from_millis(1)).await;
    
    drop(guard); // 显式释放
}
```

---

### 14.3.5 Structured Concurrency（结构化并发）

#### 14.3.5.1 结构化并发的概念（任务层级化）

**结构化并发**的核心思想：子任务的生命周期不应该超过父任务的生命周期。

```rust,ignore
#[tokio::main]
async fn main() {
    // 所有子任务在这个作用域内完成
    async fn parent_task() {
        let child1 = tokio::spawn(async { 1 });
        let child2 = tokio::spawn(async { 2 });
        
        // 等待所有子任务（显式 join，而不是依赖隐式等待）
        let _ = tokio::join!(child1, child2);
        // 注意： Tokio 不会自动等待 spawn 的子任务！
        // 如果不显式 join，父任务结束后子任务可能仍在后台运行（幽灵任务）。
    }
    
    parent_task().await;
}
```

#### 14.3.5.2 JoinSet / AbortHandle（批量任务管理）

`JoinSet` 把一批任务收在一起统一等待，`AbortHandle` 则用来单独取消某个任务。

```rust,ignore
use tokio::task::JoinSet;

#[tokio::main]
async fn main() {
    let mut set = JoinSet::new();
    
    // 添加任务
    for i in 0..5 {
        set.spawn(async move { i * 2 });
    }
    
    // 收集所有结果
    let mut results = vec![];
    while let Some(res) = set.join_next().await {
        results.push(res.unwrap());
    }
    
    println!("结果: {:?}", results); // [0, 2, 4, 6, 8]
}
```

#### 14.3.5.3 嵌套 spawn 的风险

> ⚠️ **警告**：这是 async 编程中的经典"坑"，很多人第一次写 tokio::spawn 时都会踩到。嵌套 spawn 会让任务的生命周期变得像流浪猫一样——生出来容易，收回去难。

```rust,ignore
#[tokio::main]
async fn main() {
    // 危险：不结构化的 spawn
    let handle = tokio::spawn(async {
        let nested = tokio::spawn(async {
            tokio::time::sleep(std::time::Duration::from_secs(10)).await;
            println!("嵌套任务完成");
        });
        // 如果外层任务结束，内层任务可能还在运行！
    });
    
    handle.await.unwrap();
    println!("外层任务结束了，但内层可能还在运行");
}
```

---

## 14.4 异步 I/O

### 14.4.1 异步文件 I/O

#### 14.4.1.1 tokio::fs 模块（异步文件系统操作）

`tokio::fs` 把阻塞的文件操作交给线程池执行，接口与 `std::fs` 基本一致。

```rust,ignore
#[tokio::main]
async fn main() -> std::io::Result<()> {
    // 读取文件
    let content = tokio::fs::read_to_string("Cargo.toml").await?;
    println!("读取了 {} 字节", content.len());
    
    // 写文件
    tokio::fs::write("test.txt", "hello async world").await?;
    println!("写入成功");
    
    // 读取目录
    let mut entries = tokio::fs::read_dir(".").await?;
    while let Some(entry) = entries.next_entry().await? {
        println!("{}", entry.file_name().to_string_lossy());
    }
    
    Ok(())
}
```

#### 14.4.1.2 AsyncRead / AsyncWrite trait

`AsyncRead`/`AsyncWrite` 是 tokio 的异步读写抽象，扩展 trait 提供了 `read`、`write` 等方法。

```rust,ignore
use tokio::io::{AsyncReadExt, AsyncWriteExt};

#[tokio::main]
async fn main() -> std::io::Result<()> {
    // 创建内存中的读写器
    let mut buffer = Vec::new();
    let mut reader = tokio::io::BufReader::new("hello".as_bytes());
    
    // AsyncReadExt
    let mut buf = [0u8; 1024];
    let n = reader.read(&mut buf).await?;
    println!("读取了 {} 字节: {:?}", n, &buf[..n]);
    
    // AsyncWriteExt
    let mut writer = Vec::new();
    writer.write_all(b"hello, ").await?;
    writer.write_all(b"async world!").await?;
    println!("写入内容: {:?}", writer);
    
    Ok(())
}
```

#### 14.4.1.3 BufReader / BufWriter（缓冲 I/O）

`BufReader`/`BufWriter` 通过缓冲减少系统调用次数，`read_line`、`lines` 这类逐行方法都依赖它。

```rust,ignore
use tokio::io::{AsyncBufReadExt, BufReader};
use tokio::fs::File;

#[tokio::main]
async fn main() -> std::io::Result<()> {
    // 读取文件
    let file = File::open("Cargo.toml").await?;
    let reader = BufReader::new(file);
    let mut lines = reader.lines();
    
    // 按行读取
    while let Some(line) = lines.next_line().await? {
        if line.contains("name") {
            println!("{}", line);
        }
    }
    
    Ok(())
}
```

---

### 14.4.2 异步 TCP/UDP

#### 14.4.2.1 tokio::net::TcpStream / TcpListener

tokio 的 TCP 套接字用法与标准库相似，但读写方法都是 `async` 的。

```rust,ignore
use tokio::net::{TcpListener, TcpStream};
use tokio::io::{AsyncReadExt, AsyncWriteExt};

#[tokio::main]
async fn main() -> std::io::Result<()> {
    // 启动服务器
    let listener = TcpListener::bind("127.0.0.1:8080").await?;
    println!("服务器监听在 127.0.0.1:8080");
    
    // 接受连接
    let (mut socket, addr) = listener.accept().await?;
    println!("收到来自 {} 的连接", addr);
    
    // 读写数据
    let mut buf = [0; 1024];
    let n = socket.read(&mut buf).await?;
    println!("收到: {}", String::from_utf8_lossy(&buf[..n]));
    
    socket.write_all(b"Hello from server!").await?;
    
    Ok(())
}
```

#### 14.4.2.2 tokio::net::UdpSocket

`UdpSocket` 面向数据报：一次 `recv_from` 拿到一个完整的包，不会出现 TCP 那样的粘包问题。

```rust,ignore
use tokio::net::UdpSocket;

#[tokio::main]
async fn main() -> std::io::Result<()> {
    // 创建 UDP 套接字
    let socket = UdpSocket::bind("127.0.0.1:0").await?;
    println!("绑定到 {}", socket.local_addr()?);
    
    // 发送数据
    socket.send_to(b"Hello", "127.0.0.1:8080").await?;
    println!("发送了数据");
    
    // 接收数据
    let mut buf = [0; 1024];
    let (len, addr) = socket.recv_from(&mut buf).await?;
    println!("收到来自 {}: {:?}", addr, &buf[..len]);
    
    Ok(())
}
```

#### 14.4.2.3 Unix Domain Socket（Unix only）

Unix 域套接字只在类 Unix 系统上可用，所以要用 `#[cfg(unix)]` 包起来。

```rust,ignore
#[cfg(unix)]
use tokio::net::UnixStream;

#[cfg(unix)]
#[tokio::main]
async fn main() -> std::io::Result<()> {
    use tokio::io::{AsyncReadExt, AsyncWriteExt};
    
    let mut stream = UnixStream::connect("/tmp/my.sock").await?;
    stream.write_all(b"hello").await?;
    
    let mut buf = [0; 1024];
    let n = stream.read(&mut buf).await?;
    println!("收到: {:?}", &buf[..n]);
    
    Ok(())
}
```

---

### 14.4.3 异步超时

#### 14.4.3.1 tokio::time::timeout

`timeout` 给任意 Future 加上时限，超时返回 `Err(Elapsed)`。

```rust,ignore
use tokio::time::{timeout, Duration};

#[tokio::main]
async fn main() {
    let result = timeout(Duration::from_millis(100), async {
        tokio::time::sleep(Duration::from_secs(1)).await;
        "完成"
    }).await;
    
    match result {
        Ok(v) => println!("结果: {}", v),
        Err(_) => println!("超时了！"), // 会打印这个
    }
}
```

#### 14.4.3.2 tokio::time::sleep（延迟）

`sleep` 不会阻塞线程，它只把当前任务挂起，让出执行权给别的任务。

```rust,ignore
#[tokio::main]
async fn main() {
    println!("开始");
    tokio::time::sleep(Duration::from_secs(1)).await;
    println!("1 秒后");
    
    // sleep_until 指定时间点
    let deadline = tokio::time::Instant::now() + Duration::from_secs(2);
    tokio::time::sleep_until(deadline).await;
    println!("又过了 2 秒");
}
```

#### 14.4.3.3 interval（周期定时器）

`interval` 按固定周期反复触发；第一次 tick 会立即完成，需要延后起始时刻可以用 `interval_at`。

```rust,ignore
use tokio::time::{interval, Duration};

#[tokio::main]
async fn main() {
    let mut timer = interval(Duration::from_millis(100));
    
    for i in 0..5 {
        timer.tick().await;
        println!("滴答: {}", i); // 每 100ms 打印一次
    }
}
```

---

### 14.4.4 异步信号处理

#### 14.4.4.1 tokio::signal::ctrl_c（SIGINT 信号）

`ctrl_c()` 返回一个 Future，按下 `Ctrl+C` 才完成，常与 `select!` 搭配做优雅退出。

```rust,ignore
use tokio::signal;

#[tokio::main]
async fn main() {
    println!("按 Ctrl+C 退出...");
    
    // 等待 Ctrl+C
    signal::ctrl_c().await.expect("设置信号处理器失败");
    
    println!("收到退出信号，正在清理...");
}
```

---

## 14.5 异步深入主题

### 14.5.1 异步 trait（Rust 1.75+ 稳定化）

#### 14.5.1.1 async fn in traits（trait 中的异步方法）

Rust 1.75 起 trait 里可以直接写 `async fn`，不必再依赖 `async-trait`（代价是默认不支持动态分发）。

```rust
trait AsyncIterator {
    type Item;
    
    async fn next(&mut self) -> Option<Self::Item>;
}

struct Counter {
    count: u32,
}

impl AsyncIterator for Counter {
    type Item = u32;
    
    async fn next(&mut self) -> Option<Self::Item> {
        if self.count < 5 {
            self.count += 1;
            Some(self.count)
        } else {
            None
        }
    }
}
```

#### 14.5.1.2 dyn AsyncIterator（dyn Future 支持）

带 `async fn` 的 trait 默认不是 dyn 兼容的，想用 `dyn` 需要额外处理，例如让方法返回装箱 Future。

```rust
// 动态分发
trait AsyncIterator {
    type Item;
    async fn next(&mut self) -> Option<Self::Item>;
}

fn collect_all<I>(iter: &mut dyn AsyncIterator<Item = i32>) -> Vec<i32> {
    let mut results = vec![];
    while let Some(item) = iter.next().await {
        results.push(item);
    }
    results
}
```

#### 14.5.1.3 异步 trait 的对象安全

`async fn` 能不能当 trait 对象，取决于方法是否满足对象安全的要求。

```rust
// 异步方法默认是对象安全的
trait MyTrait {
    async fn method(&self);
}

// dyn MyTrait 可以正常工作
fn takes_trait(obj: &dyn MyTrait) {
    // ...
}
```

---

### 14.5.2 async-trait crate

#### 14.5.2.1 #[async_trait] 宏（Rust 1.75 前的解决方案）

在 Rust 1.75 之前，需要用 `async-trait` crate：

```rust
use async_trait::async_trait;

#[async_trait]
trait MyTrait {
    async fn method(&self) -> i32;
}

#[async_trait]
impl MyTrait for MyStruct {
    async fn method(&self) -> i32 {
        42
    }
}
```

#### 14.5.2.2 async_trait 性能开销（Box 存储 Future）

`async-trait` 把 `async fn` 改写成返回 `Pin<Box<dyn Future>>`，换来对象安全，代价是每次调用多一次堆分配。

```rust,ignore
use async_trait::async_trait;

#[async_trait]
trait AsyncFn {
    async fn call(&self, x: i32) -> i32;
}

struct MyStruct {
    value: i32,
}

#[async_trait]
impl AsyncFn for MyStruct {
    async fn call(&self, x: i32) -> i32 {
        self.value + x
    }
}

#[tokio::main]
async fn main() {
    let obj = MyStruct { value: 10 };
    // 注意：async_trait 会使用 Box 存储 Future，有一定开销
    let result = obj.call(5).await;
    println!("结果: {}", result); // 结果: 15
}
```

---

### 14.5.3 异步锁

#### 14.5.3.1 tokio::sync::Mutex（async 上下文的互斥锁）

`tokio::sync::Mutex` 是异步锁：等待锁时挂起任务而不是阻塞线程，因此可以跨 `await` 持有。

```rust,ignore
#[tokio::main]
async fn main() {
    let mutex = tokio::sync::Mutex::new(0);
    
    // lock().await 获取锁
    {
        let mut guard = mutex.lock().await;
        *guard += 1;
    }
    
    println!("计数器: {}", *mutex.lock().await); // 1
}
```

#### 14.5.3.2 tokio::sync::RwLock（异步读写锁）

异步读写锁允许多个读者并发、写者独占，用法与标准库的 `RwLock` 类似。

```rust,ignore
#[tokio::main]
async fn main() {
    let rwlock = tokio::sync::RwLock::new(5);
    
    // 读锁
    {
        let guard = rwlock.read().await;
        println!("读取: {}", *guard); // 5
    }
    
    // 写锁
    {
        let mut guard = rwlock.write().await;
        *guard = 10;
    }
    
    println!("写入后: {}", *rwlock.read().await); // 10
}
```

#### 14.5.3.3 同步锁 vs 异步锁（不要跨 await 持有同步锁）

同步锁不能跨 `await` 持有，否则可能把整个工作线程挡住，这种场合要用异步版本的锁。

```rust,ignore
use std::sync::Mutex as SyncMutex;
use tokio::sync::Mutex as AsyncMutex;

#[tokio::main]
async fn main() {
    // 同步 Mutex：不要在 async 中跨 await 持有
    let sync_mutex = SyncMutex::new(0);
    
    // 危险！跨 await 持有同步锁
    // let guard = sync_mutex.lock().unwrap();
    // some_async_op().await; // 危险！阻塞其他任务
    // drop(guard);
    
    // 正确做法：使用 tokio::sync::Mutex
    let async_mutex = AsyncMutex::new(0);
    let mut guard = async_mutex.lock().await;
    some_async_op().await; // 安全，可以跨 await 持有
    *guard += 1;
    drop(guard);
}

async fn some_async_op() {
    tokio::time::sleep(std::time::Duration::from_millis(1)).await;
}
```

---

### 14.5.4 Stream Trait

#### 14.5.4.1 trait Stream { type Item; fn poll_next(self: Pin<&mut Self>, cx: &mut Context) -> Poll<Option<Self::Item>>; }

**Stream** 是异步的迭代器——想象 `Iterator` 喝了一罐能量饮料，变成了可以异步产值的版本：

```rust
use std::task::{Context, Poll, Pin};
use std::pin::Pin;

trait Stream {
    type Item;
    
    fn poll_next(self: Pin<&mut Self>, cx: &mut Context) -> Poll<Option<Self::Item>>;
}
```

#### 14.5.4.2 StreamExt trait（Stream 的方法扩展）

`StreamExt` 给 `Stream` 补上了 `next`、`map`、`filter` 等一大批方法，相当于异步版的迭代器工具。

```rust,ignore
use tokio_stream::StreamExt;

#[tokio::main]
async fn main() {
    let stream = tokio_stream::iter(vec![1, 2, 3, 4, 5]);
    
    // 使用 StreamExt 的方法
    let double: Vec<i32> = stream.map(|x| x * 2).collect().await;
    println!("{:?}", double); // [2, 4, 6, 8, 10]
    
    // filter
    let stream2 = tokio_stream::iter(vec![1, 2, 3, 4, 5]);
    let evens: Vec<i32> = stream2.filter(|x| x % 2 == 0).collect().await;
    println!("{:?}", evens); // [2, 4]
}
```

#### 14.5.4.3 for_each_concurrent / buffer_unordered

`for_each_concurrent` 与 `buffer_unordered` 用来限制并发度，避免一次打开过多任务。

```rust,ignore
use tokio_stream::StreamExt;

#[tokio::main]
async fn main() {
    let stream = tokio_stream::iter(0..10);
    
    // 并发处理每个元素，最多同时处理 5 个
    stream.for_each_concurrent(5, |i| async move {
        println!("处理: {}", i);
    }).await;
}
```

---

### 14.5.5 Backpressure（背压）

#### 14.5.5.1 背压的概念（消费者速度慢于生产者时的压力传递）

**背压**是指当消费者处理速度慢于生产者时，生产者需要减慢或暂停生产。

> 💡 打个比方：你往10个微信群里同时发消息，但你的手机只能"嗯嗯嗯"地一个个处理——群消息的发送速度就叫"生产者"，你的阅读速度就叫"消费者"。当你处理不过来时，消息就会堆积（channel 缓冲满了），发送者就得等等（背压）。别问我是怎么想到这个例子的。

#### 14.5.5.2 channel 缓冲大小控制

channel 的缓冲区大小决定生产者能领先消费者多少，`0` 表示必须逐一同步交接。

```rust,ignore
use tokio::sync::mpsc;

#[tokio::main]
async fn main() {
    // 创建有缓冲的 channel
    let (tx, mut rx) = mpsc::channel::<i32>(10); // 缓冲 10 个
    
    // 发送者可以发送 10 个而不阻塞
    for i in 0..10 {
        tx.send(i).await.unwrap();
    }
    
    // 第 11 个会阻塞，因为缓冲满了
}
```

#### 14.5.5.3 throttle / rate limiting

限流靠的是在任务之间插入 `sleep`，把单位时间内的请求数量压到阈值以下。

```rust,ignore
use tokio::time::{sleep, Duration};

async fn rate_limited_request(id: u32) {
    println!("请求 {} 被限流", id);
    sleep(Duration::from_millis(100)).await;
}

#[tokio::main]
async fn main() {
    // 简单的 rate limiting
    for i in 0..5 {
        rate_limited_request(i).await;
    }
}
```

---

### 14.5.6 Async Closures（异步闭包，Rust 1.85+）

#### 14.5.6.1 async || { ... } closure 语法（async + 闭包参数 + 块体；async || expr 或 async move || expr；块体是必需的；需要 nightly）

> ⚠️ **nightly 提示**：`async ||` 和 `async move ||` 语法需要 Rust nightly 并开启 `#[feature(async_closure)]`，尚未稳定。本节代码在 stable Rust 上无法编译。

```rust,ignore
#[tokio::main]
async fn main() {
    // 异步闭包：async || body
    let async_closure = async || {
        println!("异步闭包执行");
        42
    };
    
    // 调用
    let result = async_closure().await;
    println!("结果: {}", result); // 42
}
```

#### 14.5.6.2 async 闭包 vs async fn（何时必须用闭包而非函数）

async 闭包 `async || { ... }` 自 **Rust 1.85**（2025-02-20）起已经稳定，不再需要 nightly。它与 `async fn` 的最大区别是能捕获环境变量：

```rust,ignore
// 依赖 tokio，Cargo.toml 里加 tokio = { version = "1", features = ["full"] }
#[tokio::main]
async fn main() {
    // async fn 是命名函数，无法捕获外部变量
    async fn named() -> i32 {
        42
    }

    // async 闭包可以捕获环境变量
    let captured = 10;
    let closure = async move || captured + 32;

    println!("named: {}", named().await);      // 42
    println!("闭包结果: {}", closure().await); // 42
}
```

（这里标 `ignore` 只是因为示例依赖 tokio；语言层面的 async 闭包在稳定版直接可用。）

#### 14.5.6.3 async 闭包实现哪套 trait：AsyncFn / AsyncFnMut / AsyncFnOnce

async 闭包实现的是 `AsyncFnOnce`、`AsyncFnMut`、`AsyncFn` 这三个 trait（自 Rust 1.85 稳定），而不是普通的 `Fn` 系列。写约束时要用脱糖后的名字：

```rust,ignore
// 依赖 tokio
use std::ops::AsyncFn;

async fn call_twice<F: AsyncFn() -> i32>(f: F) -> i32 {
    f().await + f().await
}

#[tokio::main]
async fn main() {
    let outer = 1;
    // 只捕获 &outer，属于 AsyncFn，可以重复调用
    println!("{}", call_twice(async || outer + 41).await); // 84

    // 用 async move 捕获所有权后只能调用一次，属于 AsyncFnOnce
    let owned = String::from("hi");
    let once = async move || owned.len();
    println!("{}", once().await); // 2
}
```

三种写法的稳定性并不相同：

| 写法 | 状态 |
| --- | --- |
| `async \|\| { ... }`（async 闭包） | 稳定（Rust 1.85+） |
| `F: AsyncFn() -> T`（脱糖名） | 稳定（Rust 1.85+） |
| `F: async Fn() -> T`（语法糖） | **仍不稳定**（E0658，跟踪 issue #62290） |

#### 14.5.6.4 为什么不能写成 Box<dyn AsyncFn()>

`AsyncFn` 系列 trait 不是 dyn 兼容的：`call` 返回 `impl Future`，其大小在编译期未知，因此 `Box<dyn AsyncFn() -> i32>` 这样的类型会直接报 E0038。想做动态分发，只能自己定义一个返回装箱 Future 的类型：

```rust
use std::future::Future;
use std::pin::Pin;

// 把「返回装箱 Future 的闭包」收进一个类型别名里
type BoxFuture<T> = Pin<Box<dyn Future<Output = T> + Send>>;
```

#### 14.5.6.5 async 闭包做 trait 对象的替代方案（Box<dyn Fn() -> BoxFuture<T>>）

既然 `dyn AsyncFn` 用不了，就手工装箱。下面这段用 `Box<dyn Fn() -> BoxFuture<i32>>` 存下若干个「可以 `.await` 的闭包」：

```rust,ignore
// 依赖 tokio
use std::future::Future;
use std::pin::Pin;

type BoxFuture<T> = Pin<Box<dyn Future<Output = T> + Send>>;

#[tokio::main]
async fn main() {
    let closures: Vec<Box<dyn Fn() -> BoxFuture<i32> + Send + Sync>> = vec![
        Box::new(|| Box::pin(async { 1 })),
        Box::new(|| Box::pin(async { 2 })),
        Box::new(|| Box::pin(async { 3 })),
    ];

    for (i, c) in closures.iter().enumerate() {
        println!("closure {}: {}", i, c().await); // closure 0: 1 ...
    }
}
```

#### 14.5.6.6 async 闭包与捕获环境（move async ||）

`async move ||` 会把捕获到的变量移动进闭包，闭包创建之后外部就不能再使用这些变量：

```rust,ignore
// 依赖 tokio
#[tokio::main]
async fn main() {
    let data = vec![1, 2, 3];

    // async move 闭包取得数据的所有权
    let closure = async move || {
        println!("data: {:?}", data);
    };

    closure().await;
    // println!("{:?}", data); // 编译错误：data 已被移入闭包
}
```

#### 14.5.6.7 async 闭包做懒求值（创建时不执行）

闭包创建时不会执行内部代码，只有它返回的 Future 被 `.await` 时才真正开始运行，所以「把耗时任务推迟到需要时再执行」变得很自然：

```rust,ignore
// 依赖 tokio
#[tokio::main]
async fn main() {
    let expensive_computation = async || {
        println!("执行耗时计算...");
        tokio::time::sleep(std::time::Duration::from_secs(1)).await;
        42
    };

    println!("闭包创建了，还没执行");

    // 实际需要时才调用
    let result = expensive_computation().await;
    println!("结果: {}", result);
}
```

---

## 本章小结

这一章我们全面学习了 Rust 的异步编程：

1. **Future Trait**：异步计算的核心，`poll` 方法驱动执行
2. **async/await 语法**：用同步风格写异步代码
3. **Pin<T>**：固定内存位置，处理自引用结构
4. **Tokio**：最流行的异步运行时
5. **任务管理**：spawn、join!、select!、CancellationToken
6. **结构化并发**：JoinSet、AbortHandle，避免嵌套 spawn 的风险
7. **异步 I/O**：tokio::fs、tcp/udp、timeout、signal
8. **异步锁**：tokio::sync::Mutex/RwLock，区别于同步锁
9. **Stream**：异步迭代器，StreamExt 提供丰富的方法
10. **背压**：channel 缓冲、rate limiting
11. **Async 闭包**：`async || {}` 以及 `AsyncFn`/`AsyncFnMut`/`AsyncFnOnce` 自 Rust 1.85 起稳定；只有 `async Fn()` 这种语法糖写法仍不稳定

**记住**：async/await 是 Rust 里的"魔法棒"，它让你用最少的代码写出高效的异步程序。但记住：**Future 是惰性的，不驱动就不执行**。你需要 Tokio 或其他运行时来驱动它。

> "在 Rust 的异步世界里，Future 是剧本，await 是演出，运行时是导演。没有导演，剧本永远不会变成观众眼前的戏！"

---

**🎉 恭喜你完成了 Rust 核心教程的所有章节！**

从所有权到生命周期，从模块系统到宏，从并发到异步——你已经掌握了 Rust 编程的核心知识。现在，是时候把这些知识付诸实践了。写代码、造轮子、踩坑、再爬起来……这就是成为一个 Rust 程序员必经之路。

祝你在 Rust 的世界里玩得开心！
