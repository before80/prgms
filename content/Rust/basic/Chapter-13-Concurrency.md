+++
title = "第 13 章 并发编程"
weight = 130
date = "2026-03-27T17:24:46+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 第 13 章 并发编程（Concurrency）

> "并发，就是同时处理多件事的能力；并行，就是同时做多件事。听起来像绕口令？但如果你想在 Rust 里玩转多线程，这两个概念你必须分清楚——就像你必须分清楚'我想吃火锅'和'我正在吃火锅'一样。"

在编程的世界里，并发一直是个让人又爱又恨的东西。爱它，是因为它能让程序跑得飞快——想象你有一个厨房，你可以同时炒菜和煮饭，而不是等饭熟了再去炒菜。恨它，是因为并发带来的bug往往神出鬼没——竞态条件、死锁、数据竞争……这些问题在没有经验的厨师手里，能把整个厨房炸了。

Rust 的并发模型就像一个**超级严格的厨房安全规则**——它不允许你把锅放在火上然后离开，也不允许你同时用同一把刀切不同的菜。编译器就是那个站在旁边的安全监督员，只要它觉得你的操作有危险，就会毫不客气地阻止你。

这一章，我们就来学习如何在 Rust 的厨房里安全地做菜——啊不对，是安全地写并发代码。

---

## 13.1 并发基础概念

### 13.1.1 进程、线程、协程

#### 13.1.1.1 进程隔离（内存隔离 / 独立地址空间）

**进程**是操作系统分配资源的基本单位。每个进程都有自己独立的内存空间——就像每个家庭都有自己的房子，别人不能随便进来。

```rust
use std::process;

fn main() {
    // 创建一个新进程
    let child = process::Command::new("rustc")
        .arg("--version")
        .spawn()
        .expect("启动子进程失败");
    
    let output = child
        .wait_with_output()
        .expect("等待子进程失败");
    
    println!("子进程输出: {}", String::from_utf8_lossy(&output.stdout));
    // 子进程输出: rustc 1.XX.X (xxx 2026-01-01)
}
```

> **生活类比**：进程就像独立的房子，每个房子都有自己的地址（内存空间），你在自己房子里干什么都不会直接影响隔壁邻居。

#### 13.1.1.2 线程调度（OS 调度 / 抢占式）

**线程**是进程内的执行单元，多个线程共享同一个进程的内存空间——就像同一个房子里的室友。

```rust
use std::thread;
use std::time::Duration;

fn main() {
    println!("主线程开始");
    
    // 创建新线程
    let handle = thread::spawn(|| {
        println!("新线程开始执行");
        thread::sleep(Duration::from_millis(100));
        println!("新线程完成");
    });
    
    println!("主线程继续执行");
    
    // 等待新线程完成
    handle.join().expect("线程 panic 了");
    
    println!("所有线程结束");
}
```

输出：
```
主线程开始
主线程继续执行
新线程开始执行
新线程完成
所有线程结束
```

> **调度方式**：操作系统决定哪个线程在什么时候执行。**抢占式调度**意味着操作系统可以随时强制暂停一个线程，切换到另一个线程。这可能导致"不公平"的情况——就像你正在做饭，突然被要求去接电话一样。

#### 13.1.1.3 协程（用户态调度 / 协作式，如 async）

**协程**是一种更轻量的并发单位，它**自己决定什么时候让出控制权**（协作式调度）。这跟线程的"被操作系统强制打断"完全不同。

```rust
// 这是一个 async/await 的简单例子（详细内容在第14章）
// 这里先剧透一下：协程是"我干完这一步，觉得可以了，就自己让给你"

fn main() {
    // 协程的特点：
    // 1. 创建成本低（比线程低很多）
    // 2. 由用户态程序调度，不是操作系统
    // 3. 协作式让出（必须主动 await，不像线程会被强制抢走）
    
    println!("协程是 async/await 的基础...");
    println!("详细内容请看第14章！");
}
```

> **对比**：
> - 线程：操作系统抢占式调度，可能会突然被打断
> - 协程：用户态协作式调度，自己决定什么时候让出
> - Rust 的 async/await 就是基于协程的

---

### 13.1.2 Rust 的并发模型

#### 13.1.2.1 线程是并发的基础

在 Rust 标准库中，并发的基本单位是**线程**：

```rust
use std::thread;

fn main() {
    // thread::spawn 创建新线程
    let handle = thread::spawn(|| {
        // 这是新线程执行的代码
        println!("我在新线程里！");
    });
    
    // 主线程继续执行
    println!("我在主线程里！");
    
    // 等待新线程完成
    handle.join().unwrap();
}
```

#### 13.1.2.2 消息传递（channel / mpsc）

Rust 推崇"不要共享内存，要共享消息"的并发哲学。通过**通道（Channel）**实现线程间的消息传递：

```rust
use std::thread;
use std::sync::mpsc;

fn main() {
    // 创建通道
    let (tx, rx) = mpsc::channel();
    
    // 创建新线程发送消息
    let tx_clone = tx.clone();
    thread::spawn(move || {
        tx_clone.send("Hello from thread!".to_string()).unwrap();
    });
    
    // 主线程接收消息
    let received = rx.recv().unwrap();
    println!("收到: {}", received); // 收到: Hello from thread!
}
```

#### 13.1.2.3 共享状态（Mutex / RwLock / Arc）

当多个线程需要访问同一份数据时，Rust 使用**锁**来保证安全：

```rust
use std::sync::{Arc, Mutex};
use std::thread;

fn main() {
    // Arc: 原子引用计数，允许多个线程拥有所有权
    // Mutex: 互斥锁，一次只允许一个线程访问
    let counter = Arc::new(Mutex::new(0));
    
    let mut handles = vec![];
    
    for _ in 0..10 {
        let counter = Arc::clone(&counter);
        let handle = thread::spawn(move || {
            let mut num = counter.lock().unwrap();
            *num += 1;
        });
        handles.push(handle);
    }
    
    for handle in handles {
        handle.join().unwrap();
    }
    
    println!("最终计数: {}", *counter.lock().unwrap()); // 最终计数: 10
}
```

---

### 13.1.3 Send 与 Sync Trait

#### 13.1.3.1 Send：值可安全在线程间传递（所有权转移）

如果一个类型实现了 `Send`，意味着它可以**安全地**从一个线程转移到另一个线程：

```rust
// 实现了 Send 的类型例子
fn is_send<T: Send>() {}

fn main() {
    is_send::<i32>();     // OK: i32 是 Send
    is_send::<String>();  // OK: String 是 Send
    is_send::<&str>();    // OK: &str 是 Send
    
    println!("所有基本类型都是 Send！");
}
```

#### 13.1.3.2 Sync：值可安全跨线程引用（&T: Send）

如果一个类型实现了 `Sync`，意味着它可以**安全地**被多个线程同时持有引用：

```rust
fn is_sync<T: Sync>() {}

fn main() {
    is_sync::<i32>();     // OK: i32 是 Sync
    is_sync::<String>();  // OK: String 是 Sync
    
    println!("所有基本类型都是 Sync！");
}
```

#### 13.1.3.3 T: Sync 意味着 &T: Send

这个规则是 Rust 类型系统的基本定律：

```rust
// 如果 T 是 Sync，那么 &T 就是 Send
// 这意味着你可以安全地把 &T 传给另一个线程
fn sync_implies_shareable_ref<T: Sync>() {}

fn main() {
    // i32 是 Sync，所以 &i32 是 Send
    let x: i32 = 42;
    let x_ref = &x;
    
    // 编译时断言：验证 i32 是 Sync（所以 &i32 是 Send）
    sync_implies_shareable_ref::<i32>();
    
    println!("&i32 可以安全地跨线程传递！");
}
```

#### 13.1.3.4 基本类型默认 Send + Sync（i32 / bool / char 等）

Rust 的基本类型默认都是 `Send` 和 `Sync`：

```rust
fn check_basic_types() {
    fn assert_send<T: Send>() {}
    fn assert_sync<T: Sync>() {}
    
    assert_send::<i32>();
    assert_sync::<i32>();
    
    assert_send::<bool>();
    assert_sync::<bool>();
    
    assert_send::<char>();
    assert_sync::<char>();
    
    assert_send::<f64>();
    assert_sync::<f64>();
    
    // i32、bool、char、f64 等基本类型都实现了 Send + Sync
    // 编译器自动为所有可安全跨线程使用的类型实现这两个 trait
    println!("常见基本类型（i32/bool/char/f64 等）都是 Send + Sync！");
}

fn main() {
    check_basic_types();
}
```

#### 13.1.3.5 手动实现 Send / Sync（unsafe impl Send for MyType）

某些特殊类型需要手动实现 `Send` 或 `Sync`（用 `unsafe`）：

```rust
// 裸指针天生不是线程安全的
// 因为谁都可以拿着指针到处传
struct RawPtr(*mut i32);

unsafe impl Send for RawPtr {}
// 我们告诉编译器："我保证这个指针只会在一个线程里用"

unsafe impl Sync for RawPtr {}
// 我们告诉编译器："我保证不会有数据竞争"
```

> **警告**：手动实现 `Send/Sync` 要格外小心。你必须100%确保你的承诺是正确的，否则可能会引发未定义行为（UB）。

---

## 13.2 线程

### 13.2.1 thread::spawn 创建线程

#### 13.2.1.1 thread::spawn(|| closure)（创建新线程执行闭包）

```rust
use std::thread;

fn main() {
    // thread::spawn 接收一个闭包（或者实现了 FnOnce 的东西）
    let handle = thread::spawn(|| {
        println!("新线程正在执行");
    });
    
    println!("主线程继续执行");
    
    // 等待新线程完成
    let result = handle.join();
    println!("线程执行结果: {:?}", result.is_ok()); // true
}
```

#### 13.2.1.2 线程命名：thread::Builder::name().spawn(...)

```rust
use std::thread;

fn main() {
    let handle = thread::Builder::new()
        .name("my-worker-thread".to_string())
        .spawn(|| {
            println!("线程名: {:?}", thread::current().name());
        })
        .unwrap();
    
    handle.join().unwrap();
    // 线程名: Some("my-worker-thread")
}
```

#### 13.2.1.3 thread::spawn_scoped（可借用栈变量，跨线程借用）

```rust
use std::thread;

fn main() {
    let data = vec![1, 2, 3];
    
    // spawn_scoped 允许借用当前作用域的变量
    // 因为我们可以确保所有线程在 data 离开作用域前完成
    thread::scope(|scope| {
        scope.spawn(|| {
            println!("借用 data: {:?}", data);
        });
        
        scope.spawn(|| {
            println!("再次借用 data: {:?}", data);
        });
    });
    
    println!("所有 scoped 线程都已完成");
}
```

---

### 13.2.2 JoinHandle 与线程等待

#### 13.2.2.1 JoinHandle::join（等待线程完成并获取返回值）

```rust
use std::thread;

fn main() {
    let handle = thread::spawn(|| {
        42 // 线程返回值
    });
    
    // join() 会阻塞直到线程完成，返回 Result
    let result = handle.join().unwrap();
    println!("线程返回值: {}", result); // 42
}
```

#### 13.2.2.2 线程 panic 处理（panic 不会终止其他线程）

```rust
use std::thread;

fn main() {
    let handle = thread::spawn(|| {
        panic!("新线程 panic 了！");
    });
    
    // join() 会返回 Err
    let result = handle.join();
    println!("线程是否正常结束: {:?}", result.is_ok()); // false
    println!("主线程继续运行！");
}
```

#### 13.2.2.3 thread::Result<T> = Result<T, Box<dyn Any + Send>>

```rust
use std::thread;

fn main() {
    let handle = thread::spawn(|| {
        "success".to_string()
    });
    
    match handle.join() {
        Ok(value) => println!("成功: {}", value), // 成功: success
        Err(panic_info) => {
            println!("线程 panic: {:?}", panic_info.downcast_ref::<&str>());
        }
    }
}
```

---

### 13.2.3 线程局部存储

#### 13.2.3.1 thread_local! 宏（声明线程局部变量）

```rust
use std::cell::RefCell;

thread_local! {
    // 每个线程都有自己独立的 counter
    static COUNTER: RefCell<i32> = RefCell::new(0);
}

fn main() {
    COUNTER.with(|c| {
        *c.borrow_mut() = 10;
        println!("主线程初始值: {}", *c.borrow()); // 10
    });
    
    let handle = thread::spawn(|| {
        COUNTER.with(|c| {
            *c.borrow_mut() = 20;
            println!("新线程初始值: {}", *c.borrow()); // 20
        });
    });
    
    handle.join().unwrap();
    
    COUNTER.with(|c| {
        println!("主线程最终值: {}", *c.borrow()); // 10（不受新线程影响）
    });
}
```

#### 13.2.3.2 ThreadLocal<T>（线程局部智能指针）

```rust
use std::cell::RefCell;

thread_local! {
    // 每个线程都有自己独立的 ID
    static THREAD_ID: RefCell<u64> = RefCell::new(0);
}

fn main() {
    THREAD_ID.with(|id| {
        // 在主线程中，ID 是 0
        println!("主线程 ID: {}", *id.borrow()); // 主线程 ID: 0
    });
    
    std::thread::spawn(|| {
        THREAD_ID.with(|id| {
            // 在新线程中，ID 是不同的
            println!("新线程 ID: {}", *id.borrow());
        });
    }).join().unwrap();
}
```

#### 13.2.3.3 with 方法（访问线程局部变量）

```rust
use std::cell::RefCell;

thread_local! {
    static VALUE: RefCell<String> = RefCell::new(String::new());
}

fn main() {
    // 用 with 获取值
    VALUE.with(|v| {
        println!("初始值: {:?}", v.borrow()); // ""
    });
    
    // 用 with 修改值
    VALUE.with(|v| {
        *v.borrow_mut() = "hello".to_string();
    });
    
    VALUE.with(|v| {
        println!("修改后: {:?}", v.borrow()); // "hello"
    });
}
```

---

## 13.3 消息传递

### 13.3.1 mpsc 通道

#### 13.3.1.1 mpsc::channel()（创建发送端和接收端）

**mpsc** = Multiple Producers, Single Consumer（多生产者，单消费者）

```rust
use std::sync::mpsc;
use std::thread;

fn main() {
    // 创建通道
    let (tx, rx) = mpsc::channel();
    
    // 发送端 Sender 可以 clone（多生产者）
    let tx2 = tx.clone();
    
    // 线程1发送
    thread::spawn(move || {
        tx.send(1).unwrap();
    });
    
    // 线程2发送
    thread::spawn(move || {
        tx2.send(2).unwrap();
    });
    
    // 主线程接收（单消费者）
    println!("收到: {:?}", rx.recv()); // Ok(1) 或 Ok(2)
    println!("收到: {:?}", rx.recv()); // 另一个
}
```

#### 13.3.1.2 Sender::send（发送，返回 Result）

```rust
use std::sync::mpsc;

fn main() {
    let (tx, rx) = mpsc::channel();
    
    // send() 返回 Result
    // 如果接收端已经 drop 了，返回 Err
    match tx.send("hello") {
        Ok(()) => println!("发送成功"),
        Err(e) => println!("发送失败: {}", e),
    }
    
    // 接收
    println!("收到: {}", rx.recv().unwrap()); // hello
}
```

#### 13.3.1.3 Receiver::recv（接收，阻塞等待）

```rust
use std::sync::mpsc;
use std::time::Duration;

fn main() {
    let (tx, rx) = mpsc::channel();
    
    // recv() 会阻塞，直到收到消息或通道关闭
    println!("等待消息...");
    
    // 用 timeout 设置超时
    let result = rx.recv_timeout(Duration::from_secs(1));
    match result {
        Ok(msg) => println!("收到: {}", msg),
        Err(e) => println!("超时或错误: {:?}", e),
    }
}
```

#### 13.3.1.4 单生产者多消费者

```rust
use std::sync::mpsc;
use std::thread;

fn main() {
    let (tx, rx) = mpsc::channel();
    
    // 多个消费者？需要 Arc<Mutex<Receiver>>
    use std::sync::{Arc, Mutex};
    let rx = Arc::new(Mutex::new(rx));
    
    for i in 0..3 {
        let rx = Arc::clone(&rx);
        thread::spawn(move || {
            let rx = rx.lock().unwrap();
            println!("消费者 {} 收到: {:?}", i, rx.recv());
        });
    }
    
    tx.send("hello").unwrap();
}
```

---

### 13.3.2 通道的关闭与停止

#### 13.3.2.1 Sender::drop（发送端 Drop 后，recv 返回 None）

```rust
use std::sync::mpsc;

fn main() {
    let (tx, rx) = mpsc::channel();
    
    // tx 被 drop，通道关闭
    drop(tx);
    
    // recv() 返回 None
    let result = rx.recv();
    println!("结果: {:?}", result); // Err(RecvError)
}
```

#### 13.3.2.2 recv 返回 None 的时机（发送端全部 Drop）

```rust
use std::sync::mpsc;
use std::thread;

fn main() {
    let (tx, rx) = mpsc::channel();
    
    let tx1 = tx.clone();
    let tx2 = tx.clone();
    
    thread::spawn(move || tx1.send(1).unwrap());
    thread::spawn(move || tx2.send(2).unwrap());
    
    // drop 原始 tx
    drop(tx);
    
    // tx1, tx2 会在离开作用域时自动 drop
    // 当所有发送端都 drop 后，rx.recv() 会返回 Err
    
    for msg in rx {
        println!("收到: {}", msg); // 1, 2
    }
    
    println!("通道已关闭");
}
```

#### 13.3.2.3 for value in receiver（迭代器接口自动处理）

```rust
use std::sync::mpsc;
use std::thread;

fn main() {
    let (tx, rx) = mpsc::channel();
    
    thread::spawn(move || {
        for i in 0..5 {
            tx.send(i).unwrap();
        }
        // tx 在这里 drop，通道关闭
    });
    
    // 用 for 循环自动处理
    for value in rx {
        println!("收到: {}", value);
    }
    
    println!("所有消息已处理");
}
```

---

### 13.3.3 多生产者通道

#### 13.3.3.1 Sender::clone（克隆发送端，实现多生产者）

```rust
use std::sync::mpsc;
use std::thread;

fn main() {
    let (tx, rx) = mpsc::channel();
    
    // 克隆发送端
    let tx2 = tx.clone();
    
    let handle1 = thread::spawn(move || {
        tx.send("from thread 1").unwrap();
    });
    
    let handle2 = thread::spawn(move || {
        tx2.send("from thread 2").unwrap();
    });
    
    handle1.join().unwrap();
    handle2.join().unwrap();
    
    // 消息顺序不确定，取决于线程调度
    while let Ok(msg) = rx.recv() {
        println!("收到: {}", msg);
    }
}
```

#### 13.3.3.2 克隆后需要 Drop 所有发送端才能让 recv 停止

```rust
use std::sync::mpsc;
use std::thread;

fn main() {
    let (tx, rx) = mpsc::channel();
    
    // 创建多个发送端
    let senders: Vec<_> = (0..3)
        .map(|_| tx.clone())
        .collect();
    
    // 所有发送端都需要 drop
    // 这里我们手动 drop 原始 tx，然后等 senders 离开作用域
    
    drop(tx); // 立即 drop 原始 tx
    
    thread::spawn(move || {
        for sender in senders {
            sender.send("hello").unwrap();
            // sender 在这里 drop
        }
    });
    
    // rx 会一直等待，直到所有发送端都 drop
    for msg in rx {
        println!("收到: {}", msg);
    }
}
```

---

### 13.3.4 select 多路复用

#### 13.3.4.1 std::sync::mpsc::Select（同步 select）

```rust
use std::sync::mpsc;

fn main() {
    let (tx1, rx1) = mpsc::channel();
    let (tx2, rx2) = mpsc::channel();
    
    // std::sync::mpsc::Select 可以监听多个通道
    use std::sync::mpsc::Select;
    
    let sel = Select::new();
    
    // 注意：标准库的 Select API 比较底层
    // 实际项目中，async/await 的 tokio::select! 更常用
    println!("标准库 mpsc 的 Select API 较底层");
    println!("建议使用 async/await + tokio::select!");
}
```

#### 13.3.4.2 tokio::select!（异步多路复用）

```rust
// 这是 async/await 的 select（在第14章详细讲解）
// 先剧透一下
async fn example_select() {
    tokio::select! {
        _ = tokio::time::sleep(std::time::Duration::from_secs(1)) => {
            println!("超时");
        }
        msg = some_channel.recv() => {
            println!("收到: {:?}", msg);
        }
    }
}

fn main() {
    println!("详细内容请看第14章！");
}
```

#### 13.3.4.3 随机选择分支（避免饥饿）

`tokio::select!` 默认随机选择分支，避免某个分支被"饿死"：

```rust
// 详细代码在第14章
// 这里先记住 select! 的特点：随机选择 + 一次只执行一个分支
```

---

## 13.4 锁与同步原语

### 13.4.1 Mutex<T>

#### 13.4.1.1 std::sync::Mutex（互斥锁）

```rust
use std::sync::Mutex;

fn main() {
    let m = Mutex::new(0);
    
    {
        // lock() 返回 MutexGuard
        let mut guard = m.lock().unwrap();
        *guard += 1;
    } // guard 在这里 drop，锁自动释放
    
    println!("mutex 值: {}", *m.lock().unwrap()); // 1
}
```

#### 13.4.1.2 MutexGuard（离开作用域自动释放）

```rust
use std::sync::Mutex;

fn main() {
    let m = Mutex::new(String::from("hello"));
    
    {
        let mut s = m.lock().unwrap();
        s.push_str(", world");
        // MutexGuard 在作用域结束时自动 drop
        // 锁被释放
    }
    
    println!("{}", *m.lock().unwrap()); // hello, world
}
```

#### 13.4.1.3 lock() -> MutexGuard（借用，非获取所有权）

```rust
use std::sync::Mutex;

fn main() {
    let m = Mutex::new(42);
    
    // lock() 返回 MutexGuard，它是对内部数据的借用
    let guard = m.lock().unwrap();
    
    // deref 后可以得到 i32
    let x = *guard;
    println!("x = {}", x); // x = 42
    
    // MutexGuard 实现了 Deref，返回 &i32
    // 所以可以直接使用，像使用 i32 一样
}
```

#### 13.4.1.4 PoisonError（线程 panic 后锁进入 poison 状态）

```rust
use std::sync::Mutex;

fn main() {
    let m = Mutex::new(0);
    
    // 模拟线程 panic
    let handle = std::thread::spawn(move || {
        let mut g = m.lock().unwrap();
        *g = 100;
        panic!("线程 panic 了！");
    });
    
    let result = handle.join();
    
    // lock() 现在会返回 PoisonError
    match m.lock() {
        Ok(_) => println!("锁正常工作"),
        Err(poisoned) => {
            println!("锁被污染了");
            let guard = poisoned.into_inner();
            println!("原始值: {}", guard); // 100
        }
    }
}
```

#### 13.4.1.5 tokio::sync::Mutex（async 上下文的互斥锁）

```rust
// tokio::sync::Mutex 用于 async 上下文
// 与 std::sync::Mutex 不同的是，它的 lock() 返回 Future

#[tokio::main]
async fn main() {
    let m = tokio::sync::Mutex::new(0);
    
    {
        // await lock()
        let mut guard = m.lock().await;
        *guard += 1;
    }
    
    println!("tokio mutex: {}", *m.lock().await);
}
```

---

### 13.4.2 RwLock<T>

#### 13.4.2.1 读写锁语义（多个读或单一写）

**读写锁**允许**多个读者**同时访问，或者**一个写者**独占访问：

```rust
use std::sync::RwLock;

fn main() {
    let rw = RwLock::new(5);
    
    // 多个读锁可以同时持有
    {
        let r1 = rw.read().unwrap();
        let r2 = rw.read().unwrap();
        println!("同时读: {}, {}", r1, r2); // 5, 5
    }
    
    // 写锁是独占的
    {
        let mut w = rw.write().unwrap();
        *w = 10;
        println!("写入: {}", *w); // 10
    }
    
    println!("最终值: {}", *rw.read().unwrap()); // 10
}
```

#### 13.4.2.2 read() / write() 方法

```rust
use std::sync::RwLock;

fn main() {
    let lock = RwLock::new(vec![1, 2, 3]);
    
    // 读操作
    {
        let guard = lock.read().unwrap();
        for v in guard.iter() {
            println!("读: {}", v);
        }
    }
    
    // 写操作
    {
        let mut guard = lock.write().unwrap();
        guard.push(4);
        guard.push(5);
    }
    
    println!("{:?}", *lock.read().unwrap()); // [1, 2, 3, 4, 5]
}
```

#### 13.4.2.3 RwLockReadGuard / RwLockWriteGuard

```rust
use std::sync::RwLock;

fn main() {
    let lock = RwLock::new(42);
    
    // read() 返回 RwLockReadGuard，实现了 Deref
    {
        let read_guard = lock.read().unwrap();
        println!("读取: {}", *read_guard); // 读取: 42
    } // read_guard drop，锁释放
    
    // write() 返回 RwLockWriteGuard
    {
        let mut write_guard = lock.write().unwrap();
        *write_guard = 100;
        println!("写入: {}", *write_guard); // 写入: 100
    }
}
```

---

### 13.4.3 Arc<T>

#### 13.4.3.1 Arc::new（原子引用计数，堆上分配）

**Arc** = Atomically Reference Counted

```rust
use std::sync::Arc;

fn main() {
    // Arc 在堆上分配数据，并记录引用计数
    let data = Arc::new(vec![1, 2, 3]);
    
    println!("Arc 数据: {:?}", data); // [1, 2, 3]
}
```

#### 13.4.3.2 Arc::clone（cheap，递增计数，返回新的 Arc）

```rust
use std::sync::Arc;
use std::thread;

fn main() {
    let data = Arc::new(vec![1, 2, 3]);
    
    // clone() 不复制数据，只增加引用计数
    let data2 = Arc::clone(&data);
    
    println!("原始 ref count: {}", Arc::strong_count(&data)); // 2
    
    let handle = thread::spawn(move || {
        println!("线程中访问: {:?}", data2);
    });
    
    handle.join().unwrap();
    
    println!("线程结束后 ref count: {}", Arc::strong_count(&data)); // 1
}
```

#### 13.4.3.3 Arc::make_mut（获取可变借用，写时复制）

```rust
use std::sync::Arc;

fn main() {
    let data = Arc::new(vec![1, 2, 3]);
    
    // 创建另一个 Arc 共享数据（ref_count 变为 2）
    let data2 = Arc::clone(&data);
    println!("共享数据时 ref count: {}", Arc::strong_count(&data)); // 2
    
    // make_mut 在 ref_count > 1 时会克隆底层数据（写时复制）
    // 克隆操作发生在 data2 身上（最后创建的那个 Arc），返回其可变引用
    let data_clone = Arc::clone(&data); // 再克隆一个，ref_count = 3
    let mutable_ref = Arc::make_mut(&mut data_clone); // 触发克隆，data_clone 获得独立副本
    mutable_ref.push(4);
    
    // data、data2 仍共享原始数据 [1, 2, 3]
    // data_clone 获得了新的独立数据 [1, 2, 3, 4]
    println!("原始共享数据: {:?}", data); // [1, 2, 3]
    println!("另一份共享数据: {:?}", data2); // [1, 2, 3]
    println!("克隆后独立数据: {:?}", data_clone); // [1, 2, 3, 4]
}
```

#### 13.4.3.4 Arc::downgrade / Weak<T>（弱引用）

**Weak** 是一种"不增加引用计数"的引用，用于**避免循环引用**：

```rust
use std::sync::{Arc, Weak};

fn main() {
    let data = Arc::new(vec![1, 2, 3]);
    
    // 创建弱引用
    let weak: Weak<Vec<i32>> = Arc::downgrade(&data);
    
    println!("Arc ref count: {}", Arc::strong_count(&data)); // 1
    println!("Weak upgradeable: {}", weak.upgrade().is_some()); // true
    
    drop(data);
    
    // data drop 后，upgrade 返回 None
    println!("Weak upgradeable: {}", weak.upgrade().is_some()); // false
}
```

---

### 13.4.4 Barrier

#### 13.4.4.1 std::sync::Barrier（阻塞直到所有线程到达）

**Barrier** 就像一个"集合点"，所有线程必须都到达后才能一起继续：

```rust
use std::sync::{Arc, Barrier};
use std::thread;

fn main() {
    let barrier = Arc::new(Barrier::new(3));
    
    let handles: Vec<_> = (0..3)
        .map(|i| {
            let barrier = Arc::clone(&barrier);
            thread::spawn(move || {
                println!("线程 {} 到达前", i);
                barrier.wait(); // 阻塞，直到所有线程都到达
                println!("线程 {} 继续执行", i);
            })
        })
        .collect();
    
    for handle in handles {
        handle.join().unwrap();
    }
    
    println!("所有线程同步完成！");
}
```

输出（顺序可能略有不同）：
```
线程 0 到达前
线程 1 到达前
线程 2 到达前
线程 1 继续执行
线程 0 继续执行
线程 2 继续执行
所有线程同步完成！
```

---

### 13.4.5 Condvar（条件变量）

#### 13.4.5.1 std::sync::Condvar

**条件变量**用于"等待某个条件为真"的场景：

```rust
use std::sync::{Arc, Mutex, Condvar};

fn main() {
    let pair = Arc::new((Mutex::new(false), Condvar::new()));
    let pair2 = Arc::clone(&pair);
    
    // 等待线程
    let waiter = thread::spawn(move || {
        let (lock, cvar) = &*pair2;
        let mut started = lock.lock().unwrap();
        
        while !*started {
            // wait() 会释放锁并阻塞，直到被 notify
            started = cvar.wait(started).unwrap();
        }
        
        println!("等待线程：条件满足了！");
    });
    
    // 通知线程
    let pair3 = Arc::clone(&pair);
    let notifier = thread::spawn(move || {
        let (lock, cvar) = &*pair3;
        let mut started = lock.lock().unwrap();
        *started = true;
        cvar.notify_one(); // 通知一个等待的线程
        // 或者 cvar.notify_all() 通知所有
    });
    
    waiter.join().unwrap();
    notifier.join().unwrap();
}
```

#### 13.4.5.2 wait / notify_one / notify_all

```rust
use std::sync::{Mutex, Condvar};

fn main() {
    let pair = Arc::new((Mutex::new(0), Condvar::new()));
    
    // wait() 释放锁并阻塞，直到被通知
    // 返回新的 MutexGuard
    
    // notify_one() 唤醒一个等待线程
    // notify_all() 唤醒所有等待线程
}
```

#### 13.4.5.3 条件变量的使用模式（等待条件满足）

条件变量总是配合 `Mutex` 使用，基本模式如下：

```rust
use std::sync::{Arc, Mutex, Condvar};

// 等待者
fn wait_for_flag(flag: &Arc<Mutex<bool>>, cvar: &Condvar) {
    let mut guard = flag.lock().unwrap();
    while !*guard {
        // wait() 会释放锁并阻塞，直到被 notify
        // 返回后重新获取锁，guard 仍是 MutexGuard<bool>
        guard = cvar.wait(guard).unwrap();
    }
    // guard 离开作用域时锁自动释放
}

// 设置者
fn set_flag(flag: &Arc<Mutex<bool>>, cvar: &Condvar) {
    let mut guard = flag.lock().unwrap();
    *guard = true;
    cvar.notify_all(); // 通知所有等待者
}
```

> **注意**：条件变量可能被虚假唤醒（spurious wakeup），所以必须用 `while` 循环而非 `if` 来检查条件。

---

### 13.4.6 Once / OnceCell / OnceLock

#### 13.4.6.1 Once（只执行一次，thread::spawn 同步）

```rust
use std::sync::Once;

static INIT: Once = Once::new();

fn main() {
    INIT.call_once(|| {
        println!("这段代码只会被执行一次！");
    });
    
    INIT.call_once(|| {
        println!("这行不会打印，因为 Once 已经执行过了");
    });
    
    println!("主函数继续执行");
}
```

#### 13.4.6.2 OnceCell<T>（惰性单次初始化，非同步）

```rust
use std::cell::OnceCell;

fn main() {
    let cell = OnceCell::new();
    
    // get_or_init 只有第一次调用时执行初始化
    let value = cell.get_or_init(|| {
        println!("初始化中..."); // 这行只打印一次
        42
    });
    println!("value: {}", value); // 42
    
    // 第二次调用不会执行初始化闭包
    let value2 = cell.get_or_init(|| {
        panic!("这不会发生");
    });
    println!("value2: {}", value2); // 42，没有打印 "这不会发生"
}
```

#### 13.4.6.3 OnceLock<T>（同步惰性初始化，线程安全）

```rust
use std::sync::OnceLock;

static CELL: OnceLock<i32> = OnceLock::new();

fn get_value() -> &'static i32 {
    CELL.get_or_init(|| {
        println!("初始化中（线程安全）...");
        42
    })
}

fn main() {
    println!("{:?}", get_value()); // 初始化中（线程安全）...\n42
    println!("{:?}", get_value()); // 42（不再初始化）
}
```

#### 13.4.6.4 get_or_init（惰性初始化方法）

```rust
use std::sync::{Arc, OnceLock};

static COMPUTED: OnceLock<i32> = OnceLock::new();

fn expensive_computation() -> i32 {
    println!("执行耗时计算...");
    42
}

fn main() {
    let result = COMPUTED.get_or_init(expensive_computation);
    println!("结果: {}", result); // 42
}
```

---

### 13.4.7 Atomic<T> 原子类型

#### 13.4.7.1 AtomicBool / AtomicI32 / AtomicU32 / AtomicPtr 等

```rust
use std::sync::atomic;

fn main() {
    let counter = atomic::AtomicI32::new(0);
    
    println!("初始值: {}", counter.load(atomic::Ordering::SeqCst)); // 0
}
```

#### 13.4.7.2 load / store / swap（基本操作）

```rust
use std::sync::atomic::{AtomicI32, Ordering};

fn main() {
    let num = AtomicI32::new(100);
    
    // load 读取
    println!("读取: {}", num.load(Ordering::SeqCst)); // 100
    
    // store 写入
    num.store(200, Ordering::SeqCst);
    println!("写入后: {}", num.load(Ordering::SeqCst)); // 200
    
    // swap 交换
    let old = num.swap(300, Ordering::SeqCst);
    println!("交换了 {}, 现在是 {}", old, num.load(Ordering::SeqCst)); // 交换了 200, 现在是 300
}
```

#### 13.4.7.3 fetch_add / fetch_sub / fetch_and / fetch_or / fetch_xor（原子 RMW）

**RMW** = Read-Modify-Write

```rust
use std::sync::atomic::{AtomicI32, Ordering};

fn main() {
    let num = AtomicI32::new(10);
    
    // fetch_add 原子加，返回旧值
    let old = num.fetch_add(5, Ordering::SeqCst);
    println!("旧值: {}, 新值: {}", old, num.load(Ordering::SeqCst)); // 旧值: 10, 新值: 15
    
    // fetch_sub 原子减
    let old = num.fetch_sub(3, Ordering::SeqCst);
    println!("旧值: {}, 新值: {}", old, num.load(Ordering::SeqCst)); // 旧值: 15, 新值: 12
    
    // fetch_or 位或
    let num2 = AtomicI32::new(0b1100);
    let old = num2.fetch_or(0b0011, Ordering::SeqCst);
    println!("旧值: {:04b}, 新值: {:04b}", old, num2.load(Ordering::SeqCst)); // 旧值: 1100, 新值: 1111
}
```

#### 13.4.7.4 compare_exchange（CAS 操作）

**CAS** = Compare-And-Swap

```rust
use std::sync::atomic::{AtomicI32, Ordering};

fn main() {
    let num = AtomicI32::new(10);
    
    // compare_exchange: 如果当前值等于预期，就设置为新值
    // 返回 (旧值, 是否成功)
    
    // 成功的情况
    let (old, ok) = num.compare_exchange(10, 20, Ordering::SeqCst, Ordering::SeqCst).unwrap_or((0, false));
    println!("成功: ok={}, 旧值={}, 新值={}", ok, old, num.load(Ordering::SeqCst));
    // 成功: ok=true, 旧值=10, 新值=20
    
    // 失败的情况（值已被其他线程修改）
    let (old, ok) = num.compare_exchange(10, 30, Ordering::SeqCst, Ordering::SeqCst).unwrap_or((0, false));
    println!("失败: ok={}, 旧值={}", ok, old);
    // 失败: ok=false, 旧值=20
}
```

#### 13.4.7.5 Ordering（Relaxed / Release / Acquire / AcqRel / SeqCst）

```rust
use std::sync::atomic::{AtomicI32, Ordering};

fn main() {
    // Relaxed: 不保证跨线程顺序，只保证原子性
    // 最宽松，适用于计数器
    let counter = AtomicI32::new(0);
    let old = counter.fetch_add(1, Ordering::Relaxed);
    println!("Relaxed: 旧值={}, 新值={}", old, counter.load(Ordering::Relaxed));
    
    // Release: 之前的读写操作在释放前完成
    // 配合 Acquire 使用
    // Acquire: 之后的读写操作在获取后开始
    // 适合用于锁的释放和获取
    
    // AcqRel: 同时是 Acquire 和 Release
    
    // SeqCst: 顺序一致性，最强保证，性能最差
    // 除非你确定需要最强的保证，否则用 SeqCst
    let num = AtomicI32::new(0);
    num.store(42, Ordering::SeqCst);
    println!("SeqCst: {}", num.load(Ordering::SeqCst)); // 42
}
```

---

### 13.4.8 死锁避免原则

#### 13.4.8.1 避免嵌套锁（多个锁时固定顺序获取）

```rust
use std::sync::Mutex;

fn main() {
    let a = Mutex::new(1);
    let b = Mutex::new(2);
    
    // 死锁场景：两个线程分别持有锁 a 和 b，等待对方的锁
    // 线程1: lock(a) -> lock(b)
    // 线程2: lock(b) -> lock(a)
    
    // 解决方案：固定获取顺序，或者用单锁代替多锁
    
    // 正确做法：总是按锁的地址顺序获取
    let a_addr = &a as *const _ as usize;
    let b_addr = &b as *const _ as usize;
    
    if a_addr < b_addr {
        let _a = a.lock().unwrap();
        let _b = b.lock().unwrap();
        println!("顺序: a 先, b 后");
    } else {
        let _b = b.lock().unwrap();
        let _a = a.lock().unwrap();
        println!("顺序: b 先, a 后");
    }
}
```

#### 13.4.8.2 固定顺序获取锁（字典序 / 层次顺序）

```rust
use std::sync::{Arc, Mutex};

fn process_in_order(data: &(i32, i32)) {
    let (a, b) = data;
    // 总是先处理编号较小的
    println!("处理: {}, {}", a, b);
}

fn main() {
    let lock1 = Arc::new(Mutex::new(1));
    let lock2 = Arc::new(Mutex::new(2));
    
    // 字典序：按地址排序
    let (first, second) = if lock1.as_ref() as *const _ as usize 
        < lock2.as_ref() as *const _ as usize {
        (lock1.clone(), lock2.clone())
    } else {
        (lock2.clone(), lock1.clone())
    };
    
    let _g1 = first.lock().unwrap();
    let _g2 = second.lock().unwrap();
    println!("按固定顺序获取锁成功！");
}
```

#### 13.4.8.3 超时锁（try_lock / try_lock_for）

标准库的 `Mutex` 不直接支持超时，但可以用 `try_lock` 配合循环实现：

```rust
use std::sync::{Arc, Mutex};
use std::time::{Duration, Instant};

fn main() {
    let lock = Arc::new(Mutex::new(()));
    
    // try_lock: 尝试获取锁，立即返回
    let _g1 = lock.lock().unwrap();
    
    // 尝试获取第二个锁（非阻塞）
    match lock.try_lock() {
        Ok(_) => println!("获取了锁"),
        Err(_) => println!("锁已被持有，稍后再试"),
    }
    
    // 模拟带超时的获取
    let lock2 = Arc::new(Mutex::new(()));
    let lock2_clone = lock2.clone();
    
    std::thread::spawn(move || {
        let _g = lock2_clone.lock().unwrap();
        std::thread::sleep(Duration::from_secs(1));
    });
    
    let start = Instant::now();
    let timeout = Duration::from_millis(500);
    
    loop {
        match lock2.try_lock() {
            Ok(_) => {
                println!("获取锁成功");
                break;
            }
            Err(_) => {
                if start.elapsed() > timeout {
                    println!("等待超时: {:?}", start.elapsed());
                    break;
                }
                std::thread::sleep(Duration::from_millis(10));
            }
        }
    }
}
```

> **提示**：在真实项目中，推荐使用 `tokio::sync::Mutex` 的 `try_lock_for(Duration)` 方法，它直接支持超时等待，不需要自己写循环。

---

## 13.5 Send / Sync 与安全保证

### 13.5.1 哪些类型是 Send / Sync

#### 13.5.1.1 基本类型和常见标准库类型：Send + Sync

```rust
fn assert_send_sync<T: Send + Sync>() {}

fn main() {
    // 语言基本类型
    assert_send_sync::<i32>();
    assert_send_sync::<i64>();
    assert_send_sync::<f32>();
    assert_send_sync::<f64>();
    assert_send_sync::<bool>();
    assert_send_sync::<char>();
    
    // 常见的标准库类型
    assert_send_sync::<String>();
    assert_send_sync::<&str>();
    assert_send_sync::<Vec<i32>>();
    
    println!("基本类型和常见标准库类型都是 Send + Sync！");
}
```

#### 13.5.1.2 &T：T: Sync 时 Send，&mut T：T: Send 时 Send

```rust
fn main() {
    // &T (共享引用) 是 Send 当且仅当 T 是 Sync
    fn assert<T: Send>() {}
    
    // i32 是 Sync，所以 &i32 是 Send
    assert::<&i32>();
    
    // &mut T (可变引用) 是 Send 当且仅当 T 是 Send
    // i32 是 Send，所以 &mut i32 是 Send
    
    println!("引用的 Send/Sync 规则清楚了！");
}
```

#### 13.5.1.3 Rc<T>：非 Send / 非 Sync（单线程引用计数）

```rust
use std::rc::Rc;

fn main() {
    // Rc 不是线程安全的，因为它只是简单引用计数
    // 在多线程环境中使用 Rc 会导致数据竞争
    fn assert<T: Send>() {}
    
    // 这行会编译失败
    // assert::<Rc<i32>>();
    
    println!("Rc 不是 Send/Sync，只能用于单线程！");
}
```

#### 13.5.1.4 Arc<T>：Send + Sync（线程安全引用计数）

```rust
use std::sync::Arc;

fn main() {
    fn assert<T: Send + Sync>() {}
    
    // Arc 是线程安全的引用计数
    assert::<Arc<i32>>();
    
    println!("Arc 是 Send + Sync，可以安全跨线程使用！");
}
```

---

### 13.5.2 手动实现 Send / Sync

#### 13.5.2.1 unsafe impl Send for MyType（需要保证内部数据安全）

```rust
// 自定义线程安全的类型
struct ThreadSafeBuffer {
    data: Vec<u8>,
    // 内部有锁
    lock: std::sync::Mutex<()>,
}

// 手动实现 Send，表示可以跨线程移动
unsafe impl Send for ThreadSafeBuffer {}

// 手动实现 Sync，表示可以跨线程引用
unsafe impl Sync for ThreadSafeBuffer {}

fn main() {
    println!("ThreadSafeBuffer 是 Send + Sync！");
}
```

#### 13.5.2.2 裸指针 *const T / *mut T：非 Send / 非 Sync

```rust
fn main() {
    // 裸指针不是 Send 或 Sync，因为编译器无法追踪它们的访问
    // 你必须手动保证使用裸指针的线程安全性
    
    fn assert<T: Send>() {}
    // assert::<*const i32>(); // 编译失败
    // assert::<*mut i32>();   // 编译失败
    
    println!("裸指针不是 Send/Sync，需要 unsafe 包装！");
}
```

---

## 本章小结

这一章我们深入学习了 Rust 的并发编程：

1. **进程、线程、协程**：三种不同的并发/并行单位，各有特点
2. **Rust 并发模型**：线程为基础，消息传递 + 共享状态两种模式
3. **Send / Sync**：Rust 保证线程安全的核心 trait
4. **thread::spawn**：创建新线程，JoinHandle 等待完成
5. **线程局部存储**：`thread_local!` 宏
6. **消息传递**：mpsc channel，多生产者单消费者
7. **Mutex**：互斥锁，MutexGuard 自动释放
8. **RwLock**：读写锁，多读单写
9. **Arc**：原子引用计数，多线程共享所有权
10. **Barrier**：线程同步点
11. **Condvar**：条件变量，等待某个条件
12. **Once / OnceCell / OnceLock**：一次性初始化
13. **Atomic**：原子操作，无锁并发
14. **死锁避免**：固定顺序获取锁、超时锁

**记住**：Rust 的并发安全靠的是类型系统，而不是运行时检查。编译器会阻止你写出不安全的并发代码——虽然有时候你会觉得它过于严格，但相信我，比起在生产环境里遇到数据竞争，编译器的唠叨根本不算什么。

> "在 Rust 的世界里，没有数据竞争，只有编译器的唠叨和你的耐心。学会跟编译器打交道，你就掌握了并发编程的金钥匙！"

