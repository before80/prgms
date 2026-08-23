+++
title = "3 生成任务"
date = 2026-08-23T16:54:00+08:00
weight = 4
type = "docs"
description = ""
isCJKLanguage = true
draft = false

+++


> 原文链接: [https://tokio.rs/tokio/tutorial/spawning](https://tokio.rs/tokio/tutorial/spawning)

我们要转换方向，开始编写 Redis 服务器。

首先，将上一节中的客户端 `SET`/`GET` 代码移到一个示例文件中。这样我们就可以针对自己的服务器运行它。

```bash
$ mkdir -p examples
$ mv src/main.rs examples/hello-redis.rs
```

然后创建一个新的、空的 `src/main.rs` 并继续。


我们的 Redis 服务器首先要做的是接受入站的 TCP 套接字。
这通过将 [`tokio::net::TcpListener`][tcpl] 绑定到端口 **6379** 来完成。

> **info**
> Tokio 的许多类型与其在 Rust 标准库中的同步对应类型同名。在合理的情况下，Tokio 会暴露与 `std` 相同的 API，但使用的是 `async fn`。

然后在循环中接受套接字。每个套接字被处理后关闭。
目前，我们会读取命令，将其打印到 stdout，并返回一个错误。

`src/main.rs`

```rust
use tokio::net::{TcpListener, TcpStream};
use mini_redis::{Connection, Frame};

# fn dox() {
#[tokio::main]
async fn main() {
    // 将监听器绑定到地址
    let listener = TcpListener::bind("127.0.0.1:6379").await.unwrap();

    loop {
        // 第二个元素包含新连接的 IP 和端口。
        let (socket, _) = listener.accept().await.unwrap();
        process(socket).await;
    }
}
# }

async fn process(socket: TcpStream) {
    // `Connection` 让我们读写 redis **帧**，而不是字节流。
    // `Connection` 类型由 mini-redis 定义。
    let mut connection = Connection::new(socket);

    if let Some(frame) = connection.read_frame().await.unwrap() {
        println!("GOT: {:?}", frame);

        // 返回错误
        let response = Frame::Error("unimplemented".to_string());
        connection.write_frame(&response).await.unwrap();
    }
}
```

现在，运行这个 accept 循环：

```bash
$ cargo run
```

在另一个终端窗口中，运行 `hello-redis` 示例（上一节的 `SET`/`GET` 命令，它扮演 Redis 客户端的角色）：

```bash
$ cargo run --example hello-redis
```

输出应为：

```text
Error: "unimplemented"
```

在服务器终端中，输出为：

```text
GOT: Array([Bulk(b"set"), Bulk(b"hello"), Bulk(b"world")])
```

[tcpl]: https://docs.rs/tokio/1/tokio/net/struct.TcpListener.html

# 并发

我们的服务器有一个小问题（除了只返回错误之外）。它一次只处理一个入站请求。当接受一个连接时，服务器会一直停留在 accept 循环块内，直到响应完全写入套接字。

我们希望 Redis 服务器能**同时**处理**许多**并发请求。为此，我们需要添加一些并发能力。

> **info**
> 并发和并行不是一回事。如果你在两个任务之间交替执行，那么你是在并发地处理这两个任务，但并不是并行地处理。要算作并行，你需要两个人，每人专门负责一个任务。
>
> 使用 Tokio 的优势之一是，异步代码允许你并发地处理许多任务，而无需使用普通线程并行地处理它们。事实上，Tokio 可以在单个线程上并发运行许多任务！

要并发处理连接，需要为每个入站连接生成一个新任务。连接在该任务上被处理。

accept 循环变为：

```rust
use tokio::net::TcpListener;

# fn dox() {
#[tokio::main]
async fn main() {
    let listener = TcpListener::bind("127.0.0.1:6379").await.unwrap();

    loop {
        let (socket, _) = listener.accept().await.unwrap();
        // 为每个入站套接字生成一个新任务。套接字被
        // 移动到新任务中并在那里处理。
        tokio::spawn(async move {
            process(socket).await;
        });
    }
}
# }
# async fn process(_: tokio::net::TcpStream) {}
```

## 任务

Tokio 任务是一种异步绿色线程。它们通过将 `async` 块传递给 `tokio::spawn` 来创建。`tokio::spawn` 函数返回一个 `JoinHandle`，调用者可以用它与生成的任务交互。`async` 块可以有一个返回值。调用者可以通过在 `JoinHandle` 上调用 `.await` 来获取返回值。

例如：

```rust
#[tokio::main]
async fn main() {
    let handle = tokio::spawn(async {
        // 执行一些异步工作
        "return value"
    });

    // 执行一些其他工作

    let out = handle.await.unwrap();
    println!("GOT {}", out);
}
```

在 `JoinHandle` 上 await 会返回一个 `Result`。当任务在执行过程中遇到错误时，`JoinHandle` 会返回 `Err`。这发生在任务 panic，或者任务被运行时关闭而强制取消时。

任务是调度器管理的执行单元。生成任务会将其提交给 Tokio 调度器，调度器随后确保任务在有工作要做时执行。生成的任务可以在生成它的同一线程上执行，也可以在不同的运行时线程上执行。任务在生成后也可以在各线程之间移动。

Tokio 中的任务非常轻量。在底层，它们只需要一次分配和 64 字节的内存。应用程序可以放心地生成数千甚至数百万个任务。

## `'static` 约束

当你在 Tokio 运行时上生成任务时，其类型的生命周期必须是 `'static`。这意味着生成的任务不能包含对任务外部所拥有的数据的任何引用。

> **info**
> 一个常见的误解是 `'static` 总是意味着"永远存活"，但事实并非如此。一个值是 `'static` 并不意味着你有内存泄漏。你可以在 [Common Rust Lifetime Misconceptions][common-lifetime] 中阅读更多内容。

[common-lifetime]: https://github.com/pretzelhammer/rust-blog/blob/master/posts/common-rust-lifetime-misconceptions.md#2-if-t-static-then-t-must-be-valid-for-the-entire-program

例如，以下代码将无法编译：

```rust
use tokio::task;

#[tokio::main]
async fn main() {
    let v = vec![1, 2, 3];

    task::spawn(async {
        println!("Here's a vec: {:?}", v);
    });
}
```

尝试编译会产生以下错误：

```text
error[E0373]: async block may outlive the current function, but
              it borrows `v`, which is owned by the current function
 --> src/main.rs:7:23
  |
7 |       task::spawn(async {
  |  _______________________^
8 | |         println!("Here's a vec: {:?}", v);
  | |                                        - `v` is borrowed here
9 | |     });
  | |_____^ may outlive borrowed value `v`
  |
note: function requires argument type to outlive `'static`
 --> src/main.rs:7:17
  |
7 |       task::spawn(async {
  |  _________________^
8 | |         println!("Here's a vector: {:?}", v);
9 | |     });
  | |_____^
help: to force the async block to take ownership of `v` (and any other
      referenced variables), use the `move` keyword
  |
7 |     task::spawn(async move {
8 |         println!("Here's a vec: {:?}", v);
9 |     });
  |
```

这是因为默认情况下，变量不会被**移动**到 async 块中。
`v` 向量仍由 `main` 函数拥有。`println!` 行借用了 `v`。Rust 编译器友好地向我们解释了这一点，甚至建议了修复方法！
将第 7 行改为 `task::spawn(async move {` 会指示编译器将 `v` **移动**到生成的任务中。现在，任务拥有其所有数据，使其成为 `'static`。

如果单个数据必须被多个任务并发访问，则必须使用 `Arc` 等同步原语来共享它。

请注意，错误消息说的是参数类型*比* `'static` 生命周期*活得更久*。这个术语可能相当令人困惑，因为 `'static` 生命周期持续到程序结束，所以如果它比 `'static` 活得更久，难道不会有内存泄漏吗？解释是，必须是*类型*，而不是*值*，比 `'static` 生命周期活得更久，而值可以在其类型不再有效之前被销毁。

当我们说一个值是 `'static` 时，这意味着将它永远保留在身边并不会是错误的。这很重要，因为编译器无法推断新生成的任务会存活多久。我们必须确保任务被允许永远存活，这样 Tokio 才能让任务按需运行。

前面 info 框中链接的文章使用术语"受 `'static` 约束"，而不是"其类型比 `'static` 活得更久"或"该值是 `'static`"，来指代 `T: 'static`。这些说法含义相同，但与 `&'static T` 中的"标注了 `'static`"不同。

## `Send` 约束

由 `tokio::spawn` 生成的任务**必须**实现 `Send`。这允许 Tokio 运行时在任务在 `.await` 处挂起时在各线程之间移动任务。

当**所有**在 `.await` 调用**之间**持有的数据都是 `Send` 时，任务就是 `Send` 的。这有点微妙。当调用 `.await` 时，任务将控制权交还给调度器。下次执行任务时，它从上次让出的位置恢复。为此，**在** `.await` **之后**使用的所有状态都必须由任务保存。如果该状态是 `Send` 的，即可以跨线程移动，那么任务本身也可以跨线程移动。反之，如果状态不是 `Send` 的，任务也不是。

例如，这样可以工作：

```rust
use tokio::task::yield_now;
use std::rc::Rc;

#[tokio::main]
async fn main() {
    tokio::spawn(async {
        // 作用域强制 `rc` 在 `.await` 之前被 drop。
        {
            let rc = Rc::new("hello");
            println!("{}", rc);
        }

        // `rc` 不再被使用。当任务让出给调度器时，
        // 它**不会**被保留
        yield_now().await;
    });
}
```

这样不行：

```rust
use tokio::task::yield_now;
use std::rc::Rc;

#[tokio::main]
async fn main() {
    tokio::spawn(async {
        let rc = Rc::new("hello");

        // `rc` 在 `.await` 之后被使用。它必须被持久化到
        // 任务的状态中。
        yield_now().await;

        println!("{}", rc);
    });
}
```

尝试编译该代码片段会产生：

```text
error: future cannot be sent between threads safely
   --> src/main.rs:6:5
    |
6   |     tokio::spawn(async {
    |     ^^^^^^^^^^^^ future created by async block is not `Send`
    | 
   ::: [..]spawn.rs:127:21
    |
127 |         T: Future + Send + 'static,
    |                     ---- required by this bound in
    |                          `tokio::task::spawn::spawn`
    |
    = help: within `impl std::future::Future`, the trait
    |       `std::marker::Send` is not  implemented for
    |       `std::rc::Rc<&str>`
note: future is not `Send` as this value is used across an await
   --> src/main.rs:10:9
    |
7   |         let rc = Rc::new("hello");
    |             -- has type `std::rc::Rc<&str>` which is not `Send`
...
10  |         yield_now().await;
    |         ^^^^^^^^^^^^^^^^^ await occurs here, with `rc` maybe
    |                           used later
11  |         println!("{}", rc);
12  |     });
    |     - `rc` is later dropped here
```

我们将在[下一章][mutex-guard]更深入地讨论这种错误的一个特殊情况。

[mutex-guard]: ../4-shared-state/#holding-a-mutexguard-across-an-await
# 存储值

我们现在将实现 `process` 函数来处理传入的命令。我们将使用 `HashMap` 来存储值。`SET` 命令会插入到 `HashMap` 中，`GET` 命令会从中加载值。此外，我们将使用循环来接受每个连接的多个命令。

```rust
use tokio::net::TcpStream;
use mini_redis::{Connection, Frame};

async fn process(socket: TcpStream) {
    use mini_redis::Command::{self, Get, Set};
    use std::collections::HashMap;

    // 使用 hashmap 存储数据
    let mut db = HashMap::new();

    // 由 `mini-redis` 提供的 Connection 负责从套接字解析帧
    let mut connection = Connection::new(socket);

    // 使用 `read_frame` 从连接接收命令。
    while let Some(frame) = connection.read_frame().await.unwrap() {
        let response = match Command::from_frame(frame).unwrap() {
            Set(cmd) => {
                // 值存储为 `Vec<u8>`
                db.insert(cmd.key().to_string(), cmd.value().to_vec());
                Frame::Simple("OK".to_string())
            }
            Get(cmd) => {
                if let Some(value) = db.get(cmd.key()) {
                    // `Frame::Bulk` 期望数据类型为 `Bytes`。该类型
                    // 将在教程后面介绍。目前，使用 `into()` 将
                    // `&Vec<u8>` 转换为 `Bytes`。
                    Frame::Bulk(value.clone().into())
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

现在，启动服务器：

```bash
$ cargo run
```

在另一个终端窗口中，再次运行 `hello-redis` 客户端示例：

```bash
$ cargo run --example hello-redis
```

现在，客户端的输出为：

```text
got value from the server; result=Some(b"world")
```

我们现在可以获取和设置值了，但有一个问题：值不会在连接之间共享。如果另一个套接字连接并尝试 `GET` `hello` 键，它将找不到任何内容。

你可以在[这里][full]找到完整代码。

在下一节中，我们将实现为所有套接字持久化数据。

[full]: https://github.com/tokio-rs/website/blob/master/tutorial-code/spawning/src/main.rs
