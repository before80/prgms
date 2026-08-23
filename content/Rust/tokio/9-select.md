+++
title = "9 Select"
date = 2026-08-23T16:54:00+08:00
weight = 10
type = "docs"
description = ""
isCJKLanguage = true
draft = false

+++


> 原文链接: [https://tokio.rs/tokio/tutorial/select](https://tokio.rs/tokio/tutorial/select)

到目前为止，当我们想为系统增加并发时，会生成一个新任务。接下来我们将介绍一些在 Tokio 中并发执行异步代码的其他方式。


`tokio::select!` 宏允许同时等待多个异步计算，并在**单个**计算完成时返回。

例如：

```rust
use tokio::sync::oneshot;

#[tokio::main]
async fn main() {
    let (tx1, rx1) = oneshot::channel();
    let (tx2, rx2) = oneshot::channel();

    tokio::spawn(async {
        let _ = tx1.send("one");
    });

    tokio::spawn(async {
        let _ = tx2.send("two");
    });

    tokio::select! {
        val = rx1 => {
            println!("rx1 completed first with {:?}", val);
        }
        val = rx2 => {
            println!("rx2 completed first with {:?}", val);
        }
    }
}
```

这里使用了两个 oneshot 通道。任一通道都可能先完成。`select!` 语句会同时等待两个通道，并将 `val` 绑定为任务返回的值。当 `tx1` 或 `tx2` 完成时，执行对应的分支。

**未完成**的分支会被丢弃。在上面的例子中，计算正在等待每个通道的 `oneshot::Receiver`。尚未完成的通道对应的 `oneshot::Receiver` 会被丢弃。

## 取消

在异步 Rust 中，取消是通过丢弃 future 来完成的。回顾 ["深入 async"][async]，异步 Rust 操作通过 future 实现，而 future 是惰性的。只有当 future 被轮询时，操作才会继续。如果 future 被丢弃，操作就无法继续，因为所有相关状态都已丢弃。

不过，有时异步操作会生成后台任务或启动其他在后台运行的操作。例如，在上面的例子中，生成了一个任务来发回消息。通常，该任务会执行一些计算以生成值。

Future 或其他类型可以实现 `Drop` 来清理后台资源。Tokio 的 `oneshot::Receiver` 通过向 `Sender` 半端发送关闭通知来实现 `Drop`。`Sender` 半端可以收到该通知，并通过丢弃自身来中止正在进行的操作。

```rust
use tokio::sync::oneshot;

async fn some_operation() -> String {
    // 在此计算值
# "wut".to_string()
}

#[tokio::main]
async fn main() {
    let (mut tx1, rx1) = oneshot::channel();
    let (tx2, rx2) = oneshot::channel();

    tokio::spawn(async {
        // 在操作和 oneshot 的
        // `closed()` 通知上执行 select。
        tokio::select! {
            val = some_operation() => {
                let _ = tx1.send(val);
            }
            _ = tx1.closed() => {
                // `some_operation()` 被取消，
                // 任务完成且 `tx1` 被丢弃。
            }
        }
    });

    tokio::spawn(async {
        let _ = tx2.send("two");
    });

    tokio::select! {
        val = rx1 => {
            println!("rx1 completed first with {:?}", val);
        }
        val = rx2 => {
            println!("rx2 completed first with {:?}", val);
        }
    }
}
```

[async]: ../8-async/
## `Future` 实现

为了更好地理解 `select!` 的工作原理，让我们看看一个假设的 `Future` 实现会是什么样子。这是简化版本。实际上，`select!` 还包含额外功能，例如随机选择先轮询的分支。

```rust
use tokio::sync::oneshot;
use std::future::Future;
use std::pin::Pin;
use std::task::{Context, Poll};

struct MySelect {
    rx1: oneshot::Receiver<&'static str>,
    rx2: oneshot::Receiver<&'static str>,
}

impl Future for MySelect {
    type Output = ();

    fn poll(mut self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<()> {
        if let Poll::Ready(val) = Pin::new(&mut self.rx1).poll(cx) {
            println!("rx1 completed first with {:?}", val);
            return Poll::Ready(());
        }

        if let Poll::Ready(val) = Pin::new(&mut self.rx2).poll(cx) {
            println!("rx2 completed first with {:?}", val);
            return Poll::Ready(());
        }

        Poll::Pending
    }
}

#[tokio::main]
async fn main() {
    let (tx1, rx1) = oneshot::channel();
    let (tx2, rx2) = oneshot::channel();

    // 使用 tx1 和 tx2
# tx1.send("one").unwrap();
# tx2.send("two").unwrap();

    MySelect {
        rx1,
        rx2,
    }.await;
}
```

`MySelect` future 包含每个分支的 future。当 `MySelect` 被轮询时，先轮询第一个分支。如果它就绪，则使用该值且 `MySelect` 完成。在 `.await` 收到 future 的输出后，该 future 会被丢弃。这会导致两个分支的 future 都被丢弃。由于有一个分支未完成，该操作实际上被取消了。

回顾上一节：

> 当 future 返回 `Poll::Pending` 时，它**必须**确保在未来某个时刻唤醒 waker。忘记这样做会导致任务永远挂起。

`MySelect` 实现中没有显式使用 `Context` 参数。相反，通过将 `cx` 传递给内部 future 来满足 waker 要求。由于内部 future 也必须满足 waker 要求，仅当从内部 future 收到 `Poll::Pending` 时才返回 `Poll::Pending`，`MySelect` 也满足了 waker 要求。

# 语法

`select!` 宏可以处理超过两个的分支。当前上限为 64 个分支。每个分支的结构为：

```text
<pattern> = <async expression> => <handler>,
```

当 `select` 宏被求值时，所有 `<async expression>` 会被聚合并并发执行。当某个表达式完成时，其结果会与 `<pattern>` 进行匹配。如果结果匹配该模式，则所有剩余的异步表达式会被丢弃，并执行 `<handler>`。`<handler>` 表达式可以访问 `<pattern>` 建立的任何绑定。

`<pattern>` 的基本情况是变量名：异步表达式的结果会绑定到该变量名，`<handler>` 可以访问该变量。这就是为什么在最初的例子中，`val` 被用作 `<pattern>`，而 `<handler>` 能够访问 `val`。

如果 `<pattern>` **不**匹配异步计算的结果，则剩余的异步表达式会继续并发执行，直到下一个完成。此时，对那个结果应用相同的逻辑。

由于 `select!` 接受任何异步表达式，可以定义更复杂的计算来进行选择。

这里，我们在 `oneshot` 通道的输出和 TCP 连接上执行 select。

```rust
use tokio::net::TcpStream;
use tokio::sync::oneshot;

#[tokio::main]
async fn main() {
    let (tx, rx) = oneshot::channel();

    // 生成一个通过 oneshot 发送消息的任务
    tokio::spawn(async move {
        tx.send("done").unwrap();
    });

    tokio::select! {
        socket = TcpStream::connect("localhost:3465") => {
            println!("Socket connected {:?}", socket);
        }
        msg = rx => {
            println!("received message first {:?}", msg);
        }
    }
}
```

这里，我们在 oneshot 和从 `TcpListener` 接受套接字上执行 select。

```rust
use tokio::net::TcpListener;
use tokio::sync::oneshot;
use std::io;

#[tokio::main]
async fn main() -> io::Result<()> {
    let (tx, rx) = oneshot::channel();

    tokio::spawn(async move {
        tx.send(()).unwrap();
    });

    let mut listener = TcpListener::bind("localhost:3465").await?;

    tokio::select! {
        _ = async {
            loop {
                let (socket, _) = listener.accept().await?;
                tokio::spawn(async move { process(socket) });
            }

            // 帮助 Rust 类型推断器
            Ok::<_, io::Error>(())
        } => {}
        _ = rx => {
            println!("terminating accept loop");
        }
    }

    Ok(())
}
# async fn process(_: tokio::net::TcpStream) {}
```

接受循环会一直运行，直到遇到错误或 `rx` 收到一个值。`_` 模式表示我们对异步计算的返回值不感兴趣。

# 返回值

`tokio::select!` 宏返回所求值的 `<handler>` 表达式的结果。

```rust
async fn computation1() -> String {
    // .. 计算
# unimplemented!();
}

async fn computation2() -> String {
    // .. 计算
# unimplemented!();
}

# fn dox() {
#[tokio::main]
async fn main() {
    let out = tokio::select! {
        res1 = computation1() => res1,
        res2 = computation2() => res2,
    };

    println!("Got = {}", out);
}
# }
```

因此，**每个**分支的 `<handler>` 表达式必须求值为相同类型。如果不需要 `select!` 表达式的输出，良好的做法是让表达式求值为 `()`。

# 错误

使用 `?` 运算符会将错误从表达式中传播出去。具体行为取决于 `?` 是在异步表达式中还是在处理器中使用。在异步表达式中使用 `?` 会将错误从异步表达式中传播出去，从而使异步表达式的输出变为 `Result`。在处理器中使用 `?` 会立即将错误从 `select!` 表达式中传播出去。让我们再次看看接受循环的例子：

```rust
use tokio::net::TcpListener;
use tokio::sync::oneshot;
use std::io;

#[tokio::main]
async fn main() -> io::Result<()> {
    // [设置 `rx` oneshot 通道]
# let (tx, rx) = oneshot::channel();
# tx.send(()).unwrap();

    let listener = TcpListener::bind("localhost:3465").await?;

    tokio::select! {
        res = async {
            loop {
                let (socket, _) = listener.accept().await?;
                tokio::spawn(async move { process(socket) });
            }

            // 帮助 Rust 类型推断器
            Ok::<_, io::Error>(())
        } => {
            res?;
        }
        _ = rx => {
            println!("terminating accept loop");
        }
    }

    Ok(())
}
# async fn process(_: tokio::net::TcpStream) {}
```

注意 `listener.accept().await?`。`?` 运算符会将错误从该表达式传播到 `res` 绑定。出错时，`res` 会被设为 `Err(_)`。然后在处理器中再次使用 `?` 运算符。`res?` 语句会将错误从 `main` 函数中传播出去。

# 模式匹配

回顾一下，`select!` 宏分支的语法定义为：

```text
<pattern> = <async expression> => <handler>,
```

到目前为止，我们仅将变量绑定用作 `<pattern>`。然而，可以使用任何 Rust 模式。例如，假设我们从多个 MPSC 通道接收，可以这样做：

```rust
use tokio::sync::mpsc;

#[tokio::main]
async fn main() {
    let (mut tx1, mut rx1) = mpsc::channel(128);
    let (mut tx2, mut rx2) = mpsc::channel(128);

    tokio::spawn(async move {
        // 对 `tx1` 和 `tx2` 做些操作
# tx1.send(1).await.unwrap();
# tx2.send(2).await.unwrap();
    });

    tokio::select! {
        Some(v) = rx1.recv() => {
            println!("Got {:?} from rx1", v);
        }
        Some(v) = rx2.recv() => {
            println!("Got {:?} from rx2", v);
        }
        else => {
            println!("Both channels closed");
        }
    }
}
```

在这个例子中，`select!` 表达式等待从 `rx1` 和 `rx2` 接收值。如果通道关闭，`recv()` 返回 `None`。这与模式**不**匹配，该分支会被禁用。`select!` 表达式会继续等待剩余的分支。

注意这个 `select!` 表达式包含 `else` 分支。`select!` 表达式必须求值为一个值。使用模式匹配时，有可能**没有任何**分支匹配其关联的模式。如果发生这种情况，则求值 `else` 分支。

# 借用

生成任务时，被生成的异步表达式必须拥有其所有数据。`select!` 宏没有这个限制。每个分支的异步表达式可以借用数据并并发运行。遵循 Rust 的借用规则，多个异步表达式可以不可变地借用同一份数据，**或者**单个异步表达式可以可变地借用一份数据。

让我们看几个例子。这里，我们同时将相同的数据发送到两个不同的 TCP 目标。

```rust
use tokio::io::AsyncWriteExt;
use tokio::net::TcpStream;
use std::io;
use std::net::SocketAddr;

async fn race(
    data: &[u8],
    addr1: SocketAddr,
    addr2: SocketAddr
) -> io::Result<()> {
    tokio::select! {
        Ok(_) = async {
            let mut socket = TcpStream::connect(addr1).await?;
            socket.write_all(data).await?;
            Ok::<_, io::Error>(())
        } => {}
        Ok(_) = async {
            let mut socket = TcpStream::connect(addr2).await?;
            socket.write_all(data).await?;
            Ok::<_, io::Error>(())
        } => {}
        else => {}
    };

    Ok(())
}
# fn main() {}
```

`data` 变量被两个异步表达式**不可变**借用。当其中一个操作成功完成时，另一个会被丢弃。由于我们在 `Ok(_)` 上进行模式匹配，如果某个表达式失败，另一个会继续执行。

对于每个分支的 `<handler>`，`select!` 保证只有一个 `<handler>` 会运行。因此，每个 `<handler>` 都可以可变地借用同一份数据。

例如，下面在两个处理器中都修改 `out`：

```rust
use tokio::sync::oneshot;

#[tokio::main]
async fn main() {
    let (tx1, rx1) = oneshot::channel();
    let (tx2, rx2) = oneshot::channel();

    let mut out = String::new();

    tokio::spawn(async move {
        // 在 `tx1` 和 `tx2` 上发送值。
# let _ = tx1.send("one");
# let _ = tx2.send("two");
    });

    tokio::select! {
        _ = rx1 => {
            out.push_str("rx1 completed");
        }
        _ = rx2 => {
            out.push_str("rx2 completed");
        }
    }

    println!("{}", out);
}
```

# 循环

`select!` 宏经常在循环中使用。本节将通过一些示例展示在循环中使用 `select!` 宏的常见方式。我们从在多个通道上执行 select 开始：

```rust
use tokio::sync::mpsc;

#[tokio::main]
async fn main() {
    let (tx1, mut rx1) = mpsc::channel(128);
    let (tx2, mut rx2) = mpsc::channel(128);
    let (tx3, mut rx3) = mpsc::channel(128);
# tx1.clone().send("hello").await.unwrap();
# drop((tx1, tx2, tx3));

    loop {
        let msg = tokio::select! {
            Some(msg) = rx1.recv() => msg,
            Some(msg) = rx2.recv() => msg,
            Some(msg) = rx3.recv() => msg,
            else => { break }
        };

        println!("Got {:?}", msg);
    }

    println!("All channels have been closed.");
}
```

这个例子在三个通道接收端上执行 select。当任一通道收到消息时，会写入 STDOUT。当通道关闭时，`recv()` 返回 `None`。通过模式匹配，`select!` 宏会继续等待剩余的通道。当所有通道都关闭时，会求值 `else` 分支并终止循环。

`select!` 宏会随机选择先检查就绪状态的分支。当多个通道都有待处理值时，会随机选择一个通道来接收。这是为了处理接收循环处理消息的速度慢于消息被推入通道的速度、导致通道开始填满的情况。如果 `select!` **不**随机选择先检查的分支，在每次循环迭代时都会先检查 `rx1`。如果 `rx1` 始终包含新消息，其余通道就永远不会被检查。

> **info**
> 当 `select!` 被求值时，如果多个通道都有待处理消息，只有一个通道会弹出一个值。其余通道保持不变，其消息会留在通道中直到下一次循环迭代。不会丢失任何消息。

## 恢复异步操作

现在我们将展示如何在多次调用 `select!` 的过程中运行异步操作。在这个例子中，我们有一个元素类型为 `i32` 的 MPSC 通道和一个异步函数。我们希望运行该异步函数，直到它完成或在通道上收到一个偶数。

```rust
async fn action() {
    // 一些异步逻辑
}

#[tokio::main]
async fn main() {
    let (mut tx, mut rx) = tokio::sync::mpsc::channel(128);    
#   tokio::spawn(async move {
#       let _ = tx.send(1).await;
#       let _ = tx.send(2).await;
#   });
    
    let operation = action();
    tokio::pin!(operation);
    
    loop {
        tokio::select! {
            _ = &mut operation => break,
            Some(v) = rx.recv() => {
                if v % 2 == 0 {
                    break;
                }
            }
        }
    }
}
```

注意，我们不是在对 `action()` 的调用放在 `select!` 宏内部，而是在循环**外部**调用。`action()` 的返回值赋给 `operation`，**没有**调用 `.await`。然后我们对 `operation` 调用 `tokio::pin!`。

在 `select!` 循环内部，传入的不是 `operation`，而是 `&mut operation`。`operation` 变量跟踪正在进行的异步操作。每次循环迭代都使用同一个操作，而不是再次调用 `action()`。

`select!` 的另一个分支从通道接收消息。如果消息是偶数，我们就结束循环。否则，再次开始 `select!`。

这是我们第一次使用 `tokio::pin!`。我们暂时不会深入固定（pinning）的细节。需要记住的是，要对引用 `.await`，被引用的值必须被固定或实现 `Unpin`。

如果我们删除 `tokio::pin!` 这一行并尝试编译，会得到以下错误：

```text
error[E0599]: no method named `poll` found for struct
     `std::pin::Pin<&mut &mut impl std::future::Future>`
     in the current scope
  --> src/main.rs:16:9
   |
16 | /         tokio::select! {
17 | |             _ = &mut operation => break,
18 | |             Some(v) = rx.recv() => {
19 | |                 if v % 2 == 0 {
...  |
22 | |             }
23 | |         }
   | |_________^ method not found in
   |             `std::pin::Pin<&mut &mut impl std::future::Future>`
   |
   = note: the method `poll` exists but the following trait bounds
            were not satisfied:
           `impl std::future::Future: std::marker::Unpin`
           which is required by
           `&mut impl std::future::Future: std::future::Future`
```

尽管我们在 [上一章][async] 中讲过 `Future`，这个错误仍然不太直观。如果你在尝试对**引用**调用 `.await` 时遇到关于 `Future` 未实现的此类错误，那么该 future 很可能需要被固定。

在[标准库][pin]中阅读更多关于 [`Pin`][pin] 的内容。

[pin]: https://doc.rust-lang.org/std/pin/index.html

## 修改分支

让我们看一个稍复杂的循环。我们有：

1. 一个 `i32` 值的通道。
2. 一个对 `i32` 值执行的异步操作。

我们希望实现的逻辑是：

1. 在通道上等待一个**偶数**。
2. 使用该偶数作为输入启动异步操作。
3. 等待该操作完成，同时继续在通道上监听更多偶数。
4. 如果在现有操作完成之前收到新的偶数，则中止现有操作并用新偶数重新启动。

```rust
async fn action(input: Option<i32>) -> Option<String> {
    // 如果输入是 `None`，返回 `None`。
    // 也可以写成 `let i = input?;`
    let i = match input {
        Some(input) => input,
        None => return None,
    };
    // 异步逻辑在此
#   Some(i.to_string())
}

#[tokio::main]
async fn main() {
    let (mut tx, mut rx) = tokio::sync::mpsc::channel(128);
    
    let mut done = false;
    let operation = action(None);
    tokio::pin!(operation);
    
    tokio::spawn(async move {
        let _ = tx.send(1).await;
        let _ = tx.send(3).await;
        let _ = tx.send(2).await;
    });
    
    loop {
        tokio::select! {
            res = &mut operation, if !done => {
                done = true;

                if let Some(v) = res {
                    println!("GOT = {}", v);
                    return;
                }
            }
            Some(v) = rx.recv() => {
                if v % 2 == 0 {
                    // `.set` 是 `Pin` 上的方法。
                    operation.set(action(Some(v)));
                    done = false;
                }
            }
        }
    }
}
```

我们采用与上一个例子类似的策略。异步函数在循环外调用并赋给 `operation`。`operation` 变量被固定。循环同时在 `operation` 和通道接收端上执行 select。

注意 `action` 接受 `Option<i32>` 作为参数。在收到第一个偶数之前，我们需要将 `operation` 初始化为某个值。我们让 `action` 接受 `Option` 并返回 `Option`。如果传入 `None`，则返回 `None`。第一次循环迭代时，`operation` 会立即以 `None` 完成。

这个例子使用了一些新语法。第一个分支包含 `, if !done`。这是分支前置条件。在解释其工作原理之前，让我们看看省略前置条件会发生什么。去掉 `, if !done` 并运行示例会得到以下输出：

```text
thread 'main' panicked at '`async fn` resumed after completion', src/main.rs:1:55
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
```

这个错误发生在尝试在 `operation` **已经**完成后再次使用它时。通常，使用 `.await` 时，被等待的值会被消费。在这个例子中，我们等待的是引用。这意味着 `operation` 在完成后仍然存在。

为避免此 panic，我们必须注意在 `operation` 完成后禁用第一个分支。`done` 变量用于跟踪 `operation` 是否已完成。`select!` 分支可以包含**前置条件**。该前置条件在 `select!` 等待该分支**之前**被检查。如果条件求值为 `false`，则该分支被禁用。`done` 变量初始化为 `false`。当 `operation` 完成时，`done` 被设为 `true`。下一次循环迭代会禁用 `operation` 分支。当从通道收到偶数消息时，`operation` 被重置且 `done` 被设为 `false`。

# 每个任务内的并发

`tokio::spawn` 和 `select!` 都能运行并发的异步操作。然而，它们运行并发操作所采用的策略不同。`tokio::spawn` 函数接受一个异步操作并生成新任务来运行它。任务是 Tokio 运行时调度的对象。两个不同的任务由 Tokio 独立调度。它们可能在不同的操作系统线程上同时运行。因此，生成的任务与生成的线程有相同的限制：不能借用。

`select!` 宏在**同一个任务**上并发运行所有分支。由于 `select!` 宏的所有分支都在同一任务上执行，它们**永远不会**同时运行。`select!` 宏在单个任务上对异步操作进行多路复用。
