+++
title = "4 共享状态"
date = 2026-08-23T16:54:00+08:00
weight = 5
type = "docs"
description = ""
isCJKLanguage = true
draft = false

+++


> 原文链接: [https://tokio.rs/tokio/tutorial/shared-state](https://tokio.rs/tokio/tutorial/shared-state)

到目前为止，我们有一个可以工作的键值服务器。然而，有一个重大缺陷：状态不会在连接之间共享。我们将在本文中修复这个问题。


在 Tokio 中有几种不同的共享状态的方式。

1. 使用 Mutex 保护共享状态。
2. 生成一个任务来管理状态，并使用消息传递来操作它。

通常，对于简单数据你想使用第一种方法，对于需要异步工作（如 I/O 原语）的事物则使用第二种方法。在本章中，共享状态是一个 `HashMap`，操作是 `insert` 和 `get`。这两个操作都不是异步的，所以我们将使用 `Mutex`。

后一种方法在下一章中介绍。

# 添加 `bytes` 依赖

Mini-Redis crate 使用来自 [`bytes`] crate 的 `Bytes`，而不是 `Vec<u8>`。`Bytes` 的目标是为网络编程提供一个健壮的字节数组结构。相比 `Vec<u8>`，它最大的特性是浅克隆。换句话说，对 `Bytes` 实例调用 `clone()` 不会复制底层数据。相反，`Bytes` 实例是对某些底层数据的引用计数句柄。`Bytes` 类型大致相当于 `Arc<Vec<u8>>`，但具有一些额外的能力。

要依赖 `bytes`，在 `Cargo.toml` 的 `[dependencies]` 部分添加以下内容：

```toml
bytes = "1"
```

[`bytes`]: https://docs.rs/bytes/1/bytes/struct.Bytes.html

# 初始化 `HashMap`

`HashMap` 将在许多任务之间共享，可能还在许多线程之间共享。为了支持这一点，它被包装在 `Arc<Mutex<_>>` 中。

首先，为了方便，在 `use` 语句之后添加以下类型别名。

```rust
use bytes::Bytes;
use std::collections::HashMap;
use std::sync::{Arc, Mutex};

type Db = Arc<Mutex<HashMap<String, Bytes>>>;
```

然后，更新 `main` 函数以初始化 `HashMap`，并将 `Arc` **句柄**传递给 `process` 函数。使用 `Arc` 允许 `HashMap` 被许多任务并发引用，这些任务可能运行在许多线程上。在 Tokio 中，术语**句柄**用于引用提供对某些共享状态访问的值。

```rust
use tokio::net::TcpListener;
use std::collections::HashMap;
use std::sync::{Arc, Mutex};

# fn dox() {
#[tokio::main]
async fn main() {
    let listener = TcpListener::bind("127.0.0.1:6379").await.unwrap();

    println!("Listening");

    let db = Arc::new(Mutex::new(HashMap::new()));

    loop {
        let (socket, _) = listener.accept().await.unwrap();
        // 克隆 hash map 的句柄。
        let db = db.clone();

        println!("Accepted");
        tokio::spawn(async move {
            process(socket, db).await;
        });
    }
}
# }
# type Db = Arc<Mutex<HashMap<(), ()>>>;
# async fn process(_: tokio::net::TcpStream, _: Db) {}
```

## 关于使用 `std::sync::Mutex` 和 `tokio::sync::Mutex`

请注意，我们使用的是 `std::sync::Mutex`，而**不是** `tokio::sync::Mutex` 来保护 `HashMap`。一个常见的错误是在异步代码中无条件地使用 `tokio::sync::Mutex`。异步互斥锁是一种在调用 `.await` 时保持锁定的互斥锁。

同步互斥锁在等待获取锁时会阻塞当前线程。这反过来会阻塞其他任务的处理。切换到 `tokio::sync::Mutex` 会导致任务将控制权交还给执行器，但这通常不会有助于性能，因为异步互斥锁内部使用同步互斥锁。

作为经验法则，只要争用保持较低且锁不在调用 `.await` 时持有，在异步代码中使用同步互斥锁是可以的。

# 更新 `process()`

`process` 函数不再初始化 `HashMap`。相反，它接受 `HashMap` 的共享句柄作为参数。它还需要在使用 `HashMap` 之前对其加锁。请记住，`HashMap` 中值的类型现在是 `Bytes`（可以廉价克隆），所以这也需要更改。

```rust
use tokio::net::TcpStream;
use mini_redis::{Connection, Frame};
# use std::collections::HashMap;
# use std::sync::{Arc, Mutex};
# type Db = Arc<Mutex<HashMap<String, bytes::Bytes>>>;

async fn process(socket: TcpStream, db: Db) {
    use mini_redis::Command::{self, Get, Set};

    // 由 `mini-redis` 提供的 Connection 负责从套接字解析帧
    let mut connection = Connection::new(socket);

    while let Some(frame) = connection.read_frame().await.unwrap() {
        let response = match Command::from_frame(frame).unwrap() {
            Set(cmd) => {
                let mut db = db.lock().unwrap();
                db.insert(cmd.key().to_string(), cmd.value().clone());
                Frame::Simple("OK".to_string())
            }           
            Get(cmd) => {
                let db = db.lock().unwrap();
                if let Some(value) = db.get(cmd.key()) {
                    Frame::Bulk(value.clone())
                } else {
                    Frame::Null
                }
            }
            cmd => panic!("unimplemented {:?}", cmd),
        };

        // 将响应写回客户端
        connection.write_frame(&response).await.unwrap();
    }
}
```

# 在 `.await` 期间持有 `MutexGuard`

你可能会写出如下代码：
```rust
use std::sync::{Mutex, MutexGuard};

async fn increment_and_do_stuff(mutex: &Mutex<i32>) {
    let mut lock: MutexGuard<i32> = mutex.lock().unwrap();
    *lock += 1;

    do_something_async().await;
} // lock 在此处离开作用域
# async fn do_something_async() {}
```
当你尝试生成调用此函数的内容时，会遇到以下错误消息：
```text
error: future cannot be sent between threads safely
   --> src/lib.rs:13:5
    |
13  |     tokio::spawn(async move {
    |     ^^^^^^^^^^^^ future created by async block is not `Send`
    |
   ::: /playground/.cargo/registry/src/github.com-1ecc6299db9ec823/tokio-0.2.21/src/task/spawn.rs:127:21
    |
127 |         T: Future + Send + 'static,
    |                     ---- required by this bound in `tokio::task::spawn::spawn`
    |
    = help: within `impl std::future::Future`, the trait `std::marker::Send` is not implemented for `std::sync::MutexGuard<'_, i32>`
note: future is not `Send` as this value is used across an await
   --> src/lib.rs:7:5
    |
4   |     let mut lock: MutexGuard<i32> = mutex.lock().unwrap();
    |         -------- has type `std::sync::MutexGuard<'_, i32>` which is not `Send`
...
7   |     do_something_async().await;
    |     ^^^^^^^^^^^^^^^^^^^^^^^^^^ await occurs here, with `mut lock` maybe used later
8   | }
    | - `mut lock` is later dropped here
```
这是因为 `std::sync::MutexGuard` 类型**不是** `Send`。这意味着你不能将互斥锁锁发送到另一个线程，而错误发生是因为 Tokio 运行时可以在每个 `.await` 处将任务移动到另一个线程。为避免这种情况，你应该重构代码，使互斥锁锁的析构函数在 `.await` 之前运行。
```rust
# use std::sync::{Mutex, MutexGuard};
// 这样可以！
async fn increment_and_do_stuff(mutex: &Mutex<i32>) {
    {
        let mut lock: MutexGuard<i32> = mutex.lock().unwrap();
        *lock += 1;
    } // lock 在此处离开作用域

    do_something_async().await;
}
# async fn do_something_async() {}
```
请注意，这样不行：
```rust
use std::sync::{Mutex, MutexGuard};

// 这样也会失败。
async fn increment_and_do_stuff(mutex: &Mutex<i32>) {
    let mut lock: MutexGuard<i32> = mutex.lock().unwrap();
    *lock += 1;
    drop(lock);

    do_something_async().await;
}
# async fn do_something_async() {}
```
这是因为编译器目前仅根据作用域信息来计算 future 是否为 `Send`。编译器有望在未来更新以支持显式 drop，但目前你必须显式使用作用域。

请注意，这里讨论的错误也在[生成任务章节的 Send 约束部分][send-bound]中讨论过。

你不应该试图通过以不需要 `Send` 的方式生成任务来规避此问题，因为如果 Tokio 在任务持有锁时在 `.await` 处挂起你的任务，另一个任务可能会被调度到同一线程上运行，而这个其他任务也可能尝试锁定该互斥锁，这将导致死锁，因为等待锁定互斥锁的任务会阻止持有互斥锁的任务释放互斥锁。

请记住，一些互斥锁 crate 为其 MutexGuard 实现了 `Send`。在这种情况下，即使你在 `.await` 期间持有 MutexGuard，也不会有编译器错误。代码可以编译，但会死锁！

我们将在下面讨论一些避免这些问题的方法：

[send-bound]: ../3-spawning/#send-bound
## 重构代码，避免在 `.await` 期间持有锁

处理互斥锁最安全的方法是将它包装在一个结构体中，并且只在该结构体的非 async 方法内部锁定互斥锁。
```rust
use std::sync::Mutex;

struct CanIncrement {
    mutex: Mutex<i32>,
}
impl CanIncrement {
    // 此函数未标记为 async。
    fn increment(&self) {
        let mut lock = self.mutex.lock().unwrap();
        *lock += 1;
    }
}

async fn increment_and_do_stuff(can_incr: &CanIncrement) {
    can_incr.increment();
    do_something_async().await;
}
# async fn do_something_async() {}
```
这种模式保证你不会遇到 `Send` 错误，因为互斥锁守卫不会出现在任何 async 函数中。当使用其 `MutexGuard` 实现 `Send` 的 crate 时，它也能保护你免受死锁。

你可以在[这篇博客文章][shared-mutable-state-blog-post]中找到更详细的示例。

## 生成任务来管理状态，并使用消息传递来操作它

这是本章开头提到的第二种方法，当共享资源是 I/O 资源时经常使用。详见下一章。

## 使用 Tokio 的异步互斥锁

也可以使用 Tokio 提供的 [`tokio::sync::Mutex`] 类型。Tokio 互斥锁的主要特性是可以在 `.await` 期间持有它而不会有任何问题。也就是说，异步互斥锁比普通互斥锁更昂贵，通常最好使用其他两种方法之一。
```rust
use tokio::sync::Mutex; // 注意！这里使用的是 Tokio 互斥锁

// 这可以编译！
// （但在这种情况下重构代码会更好）
async fn increment_and_do_stuff(mutex: &Mutex<i32>) {
    let mut lock = mutex.lock().await;
    *lock += 1;

    do_something_async().await;
} // lock 在此处离开作用域
# async fn do_something_async() {}
```

[`tokio::sync::Mutex`]: https://docs.rs/tokio/1/tokio/sync/struct.Mutex.html

# 任务、线程和争用

当争用最小时，使用阻塞互斥锁来保护短临界区是一种可接受的策略。当锁发生争用时，执行任务的线程必须阻塞并等待互斥锁。这不仅会阻塞当前任务，还会阻塞调度在当前线程上的所有其他任务。

默认情况下，Tokio 运行时使用多线程调度器。任务被调度到运行时管理的任意数量的线程上。如果大量任务被调度执行且它们都需要访问互斥锁，就会发生争用。另一方面，如果使用 [`current_thread`][current_thread] 运行时风格，则互斥锁永远不会发生争用。

> **info**
> [`current_thread` 运行时风格][basic-rt]是一种轻量级的单线程运行时。当只生成少量任务并打开少量套接字时，这是一个不错的选择。例如，在异步客户端库之上提供同步 API 桥接时，此选项效果很好。

[basic-rt]: https://docs.rs/tokio/1/tokio/runtime/struct.Builder.html#method.new_current_thread

如果同步互斥锁上的争用成为问题，最好的修复方法很少是切换到 Tokio 互斥锁。相反，可以考虑的选项有：

- 让专用任务管理状态并使用消息传递。
- 对互斥锁进行分片。
- 重构代码以避免互斥锁。

## 互斥锁分片

在我们的情况下，由于每个*键*是独立的，互斥锁分片效果很好。为此，我们不是拥有一个 `Mutex<HashMap<_, _>>` 实例，而是引入 `N` 个不同的实例。

```rust
# use std::collections::HashMap;
# use std::sync::{Arc, Mutex};
type ShardedDb = Arc<Vec<Mutex<HashMap<String, Vec<u8>>>>>;

fn new_sharded_db(num_shards: usize) -> ShardedDb {
    let mut db = Vec::with_capacity(num_shards);
    for _ in 0..num_shards {
        db.push(Mutex::new(HashMap::new()));
    }
    Arc::new(db)
}
```

然后，查找任何给定键的单元格成为一个两步过程。首先，使用键来确定它属于哪个分片。然后，在 `HashMap` 中查找该键。

```rust
let shard = db[hash(key) % db.len()].lock().unwrap();
shard.insert(key, value);
```

上面概述的简单实现需要使用固定数量的分片，并且在创建分片 map 后无法更改分片数量。

[dashmap] crate 提供了更复杂的分片 hash map 实现。你可能还想看看 [leapfrog] 和 [flurry] 等并发哈希表实现，后者是 Java `ConcurrentHashMap` 数据结构的移植。

在你开始使用这些 crate 中的任何一个之前，请确保你的代码结构使得你不能在 `.await` 期间持有 `MutexGuard`。如果不这样做，你会遇到编译器错误（对于非 Send 守卫的情况）或代码死锁（对于 Send 守卫的情况）。在[这篇博客文章][shared-mutable-state-blog-post]中查看完整示例和更多上下文。

[current_thread]: https://docs.rs/tokio/1/tokio/runtime/index.html#current-thread-scheduler
[dashmap]: https://docs.rs/dashmap
[leapfrog]: https://docs.rs/leapfrog
[flurry]: https://docs.rs/flurry
[shared-mutable-state-blog-post]: https://draft.ryhl.io/blog/shared-mutable-state/
