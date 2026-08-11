+++
title = "21.3 优雅停机与清理"
date = 2026-08-05T08:44:00+08:00
weight = 103
type = "docs"
description = "为线程池实现 Drop、停止接任务与优雅停机"
isCJKLanguage = true
draft = false
rust_version = "1.97.1"

+++

> 译文 · 基于 [The Rust Programming Language](https://doc.rust-lang.org/stable/book/)（rustc 1.97.1）

# 优雅停机与清理


> 原文链接: [https://doc.rust-lang.org/stable/book/ch21-03-graceful-shutdown-and-cleanup.html](https://doc.rust-lang.org/stable/book/ch21-03-graceful-shutdown-and-cleanup.html)


## 优雅停机与清理

　　示例 21-20 中的代码正如我们所愿，通过线程池异步响应请求。我们收到一些关于 `workers`、`id` 和 `thread` 字段未被直接使用的警告，这提醒我们还没有清理任何东西。当我们用不那么优雅的 <kbd>ctrl</kbd>-<kbd>C</kbd> 方式停掉主线程时，其他线程也会立即停止，哪怕它们正处在服务某个请求的中途。

　　接下来，我们将实现 `Drop` 特征，对池中每个线程调用 `join`，使它们能在关闭前完成正在处理的请求。然后，我们再实现一种方式，告诉线程应停止接受新请求并关闭。为了看到这段代码实际运行，我们会修改服务器，使其在优雅关闭线程池之前只接受两个请求。

　　一路上请注意：这些都不会影响执行闭包的那部分代码，因此即便我们把线程池用于异步运行时，这里的一切也会相同。

### 在 `ThreadPool` 上实现 `Drop` 特征

　　先从在线程池上实现 `Drop` 开始。当池被丢弃时，我们的线程都应 join，以确保它们完成工作。示例 21-22 展示 `Drop` 实现的第一次尝试；这段代码还不能完全工作。

**文件名：`src/lib.rs`**
```rust
impl Drop for ThreadPool {
    fn drop(&mut self) {
        for worker in &mut self.workers {
            println!("Shutting down worker {}", worker.id);

            worker.thread.join().unwrap();
        }
    }
}
```

**示例 21-22：线程池离开作用域时 join 每个线程**

　　首先，我们遍历线程池的每个 `workers`。这里使用 `&mut`，因为 `self` 是可变引用，我们也需要能修改 `worker`。对每个 `worker`，我们打印一条消息，说明这个特定的 `Worker` 实例正在关闭，然后对该 `Worker` 实例的线程调用 `join`。若对 `join` 的调用失败，我们使用 `unwrap` 让 Rust panic，并进入不优雅的关闭。

　　编译这段代码时得到的错误如下：

```console
$ cargo check
    Checking hello v0.1.0 (file:///projects/hello)
error[E0507]: cannot move out of `worker.thread` which is behind a mutable reference
  --> src/lib.rs:52:13
   |
52 |             worker.thread.join().unwrap();
   |             ^^^^^^^^^^^^^ ------ `worker.thread` moved due to this method call
   |             |
   |             move occurs because `worker.thread` has type `JoinHandle<()>`, which does not implement the `Copy` trait
   |
note: `JoinHandle::<T>::join` takes ownership of the receiver `self`, which moves `worker.thread`
  --> /rustc/2d8144b7880597b6e6d3dfd63a9a9efae3f533d3/library/std/src/thread/join_handle.rs:149:16

For more information about this error, try `rustc --explain E0507`.
error: could not compile `hello` (lib) due to 1 previous error
```

　　错误告诉我们不能调用 `join`，因为我们只有对每个 `worker` 的可变借用，而 `join` 会取得其参数的所有权。要解决这个问题，需要把线程从拥有 `thread` 的 `Worker` 实例中移出，好让 `join` 能消费该线程。一种做法是采用示例 18-15 中的相同思路。若 `Worker` 持有 `Option<thread::JoinHandle<()>>`，我们就可以对 `Option` 调用 `take` 方法，把值从 `Some` 变体中移出，并在原处留下 `None` 变体。换句话说，正在运行的 `Worker` 会在 `thread` 中有一个 `Some` 变体；当我们想清理某个 `Worker` 时，就把 `Some` 换成 `None`，使该 `Worker` 不再有可运行的线程。

　　然而，这种情况 *唯一* 会出现的时机就是丢弃 `Worker` 时。作为交换，我们在任何访问 `worker.thread` 的地方都得对付 `Option<thread::JoinHandle<()>>`。惯用的 Rust 会大量使用 `Option`，但当你发现自己只是为了绕过问题、把明知始终存在的东西包进 `Option` 时，最好寻找替代方案，让代码更干净、更不易出错。

　　在这个例子中，有更好的替代：`Vec::drain` 方法。它接受一个范围参数，指定要从向量中移除哪些项，并返回这些项的迭代器。传入 `..` 范围语法会移除向量中的 *每一个* 值。

　　因此，我们需要像这样更新 `ThreadPool` 的 `drop` 实现：

**文件名：`src/lib.rs`**
```rust
impl Drop for ThreadPool {
    fn drop(&mut self) {
        for worker in self.workers.drain(..) {
            println!("Shutting down worker {}", worker.id);

            worker.thread.join().unwrap();
        }
    }
}
```

　　这就解决了编译器错误，也不需要对代码做其他改动。注意，因为 drop 可能在 panic 时被调用，unwrap 也可能再 panic 并导致双重 panic，从而立即崩溃程序并中断正在进行的清理。对示例程序来说这可以接受，但不建议用于生产代码。

### 向线程发出信号，停止监听任务

　　有了我们做的全部改动，代码已能无警告地编译。然而坏消息是，这段代码的行为还不是我们想要的。关键在于 `Worker` 实例的线程所运行的闭包中的逻辑：此刻我们调用了 `join`，但这并不会关闭线程，因为它们在永远 `loop` 寻找任务。若用当前的 `drop` 实现尝试丢弃 `ThreadPool`，主线程会永远阻塞，等待第一个线程结束。

　　要修好这个问题，需要改 `ThreadPool` 的 `drop` 实现，再改 `Worker` 的循环。

　　首先，我们改 `ThreadPool` 的 `drop` 实现，在等待线程结束之前显式丢弃 `sender`。示例 21-23 展示对 `ThreadPool` 的改动，以显式丢弃 `sender`。与线程不同，这里我们 *确实* 需要用 `Option`，才能用 `Option::take` 把 `sender` 从 `ThreadPool` 中移出。

**文件名：`src/lib.rs`**
```rust
pub struct ThreadPool {
    workers: Vec<Worker>,
    sender: Option<mpsc::Sender<Job>>,
}
// --snip--

impl ThreadPool {

    pub fn new(size: usize) -> ThreadPool {
        // --snip--


        ThreadPool {
            workers,
            sender: Some(sender),
        }
    }

    pub fn execute<F>(&self, f: F)
    where
        F: FnOnce() + Send + 'static,
    {
        let job = Box::new(f);

        self.sender.as_ref().unwrap().send(job).unwrap();
    }
}

impl Drop for ThreadPool {
    fn drop(&mut self) {
        drop(self.sender.take());

        for worker in self.workers.drain(..) {
            println!("Shutting down worker {}", worker.id);

            worker.thread.join().unwrap();
        }
    }
}
```

**示例 21-23：在 join `Worker` 线程之前显式丢弃 `sender`**

　　丢弃 `sender` 会关闭通道，表明不会再发送更多消息。发生这种情况时，`Worker` 实例在无限循环中对 `recv` 的所有调用都会返回错误。在示例 21-24 中，我们改 `Worker` 循环，在那种情况下优雅地退出循环，这意味着当 `ThreadPool` 的 `drop` 实现对它们调用 `join` 时，线程就会结束。

**文件名：`src/lib.rs`**
```rust
impl Worker {
    fn new(id: usize, receiver: Arc<Mutex<mpsc::Receiver<Job>>>) -> Worker {
        let thread = thread::spawn(move || {
            loop {
                let message = receiver.lock().unwrap().recv();

                match message {
                    Ok(job) => {
                        println!("Worker {id} got a job; executing.");

                        job();
                    }
                    Err(_) => {
                        println!("Worker {id} disconnected; shutting down.");
                        break;
                    }
                }
            }
        });

        Worker { id, thread }
    }
}
```

**示例 21-24：当 `recv` 返回错误时显式跳出循环**

　　为了看到这段代码实际运行，我们按示例 21-25 修改 `main`，使其在优雅关闭服务器之前只接受两个请求。

**文件名：`src/main.rs`**
```rust
fn main() {
    let listener = TcpListener::bind("127.0.0.1:7878").unwrap();
    let pool = ThreadPool::new(4);

    for stream in listener.incoming().take(2) {
        let stream = stream.unwrap();

        pool.execute(|| {
            handle_connection(stream);
        });
    }

    println!("Shutting down.");
}
```

**示例 21-25：通过退出循环，在服务两个请求后关闭服务器**

　　你不会希望真实世界的 Web 服务器只服务两个请求就关闭。这段代码只是演示优雅停机与清理已能正常工作。

　　`take` 方法定义在 `Iterator` 特征中，最多把迭代限制为前两项。`ThreadPool` 会在 `main` 结束时离开作用域，并运行 `drop` 实现。

　　用 `cargo run` 启动服务器并发起三个请求。第三个请求应会出错，终端中你应能看到类似这样的输出：


```console
$ cargo run
   Compiling hello v0.1.0 (file:///projects/hello)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.41s
     Running `target/debug/hello`
Worker 0 got a job; executing.
Shutting down.
Shutting down worker 0
Worker 3 got a job; executing.
Worker 1 disconnected; shutting down.
Worker 2 disconnected; shutting down.
Worker 3 disconnected; shutting down.
Worker 0 disconnected; shutting down.
Shutting down worker 1
Shutting down worker 2
Shutting down worker 3
```

　　你可能看到不同顺序的 `Worker` ID 与打印消息。从这些消息可以看出代码如何工作：`Worker` 实例 0 和 3 拿到了前两个请求。服务器在第二个连接之后停止接受连接，并且 `ThreadPool` 上的 `Drop` 实现甚至在 `Worker 3` 开始其任务之前就开始执行。丢弃 `sender` 会断开所有 `Worker` 实例并告诉它们关闭。各 `Worker` 实例在断开时各自打印一条消息，然后线程池调用 `join` 等待每个 `Worker` 线程结束。

　　注意这次特定执行中一个有趣的方面：`ThreadPool` 丢弃了 `sender`，而在任何 `Worker` 收到错误之前，我们就尝试 join `Worker 0`。`Worker 0` 尚未从 `recv` 得到错误，因此主线程阻塞，等待 `Worker 0` 结束。与此同时，`Worker 3` 收到了一个任务，然后所有线程都收到了错误。当 `Worker 0` 结束后，主线程等待其余 `Worker` 实例结束。那时，它们都已退出循环并停止。

　　恭喜！我们现在完成了项目；我们有了一个用线程池异步响应的基础 Web 服务器。我们能够对服务器执行优雅停机，清理池中的所有线程。

　　以下是完整代码供参考：

**文件名：`src/main.rs`**
```rust
use hello::ThreadPool;
use std::{
    fs,
    io::{BufReader, prelude::*},
    net::{TcpListener, TcpStream},
    thread,
    time::Duration,
};

fn main() {
    let listener = TcpListener::bind("127.0.0.1:7878").unwrap();
    let pool = ThreadPool::new(4);

    for stream in listener.incoming().take(2) {
        let stream = stream.unwrap();

        pool.execute(|| {
            handle_connection(stream);
        });
    }

    println!("Shutting down.");
}

fn handle_connection(mut stream: TcpStream) {
    let buf_reader = BufReader::new(&stream);
    let request_line = buf_reader.lines().next().unwrap().unwrap();

    let (status_line, filename) = match &request_line[..] {
        "GET / HTTP/1.1" => ("HTTP/1.1 200 OK", "hello.html"),
        "GET /sleep HTTP/1.1" => {
            thread::sleep(Duration::from_secs(5));
            ("HTTP/1.1 200 OK", "hello.html")
        }
        _ => ("HTTP/1.1 404 NOT FOUND", "404.html"),
    };

    let contents = fs::read_to_string(filename).unwrap();
    let length = contents.len();

    let response =
        format!("{status_line}\r\nContent-Length: {length}\r\n\r\n{contents}");

    stream.write_all(response.as_bytes()).unwrap();
}
```

**文件名：`src/lib.rs`**
```rust
use std::{
    sync::{Arc, Mutex, mpsc},
    thread,
};

pub struct ThreadPool {
    workers: Vec<Worker>,
    sender: Option<mpsc::Sender<Job>>,
}

type Job = Box<dyn FnOnce() + Send + 'static>;

impl ThreadPool {
    /// Create a new ThreadPool.
    ///
    /// The size is the number of threads in the pool.
    ///
    /// # Panics
    ///
    /// The `new` function will panic if the size is zero.
    pub fn new(size: usize) -> ThreadPool {
        assert!(size > 0);

        let (sender, receiver) = mpsc::channel();

        let receiver = Arc::new(Mutex::new(receiver));

        let mut workers = Vec::with_capacity(size);

        for id in 0..size {
            workers.push(Worker::new(id, Arc::clone(&receiver)));
        }

        ThreadPool {
            workers,
            sender: Some(sender),
        }
    }

    pub fn execute<F>(&self, f: F)
    where
        F: FnOnce() + Send + 'static,
    {
        let job = Box::new(f);

        self.sender.as_ref().unwrap().send(job).unwrap();
    }
}

impl Drop for ThreadPool {
    fn drop(&mut self) {
        drop(self.sender.take());

        for worker in &mut self.workers {
            println!("Shutting down worker {}", worker.id);

            if let Some(thread) = worker.thread.take() {
                thread.join().unwrap();
            }
        }
    }
}

struct Worker {
    id: usize,
    thread: Option<thread::JoinHandle<()>>,
}

impl Worker {
    fn new(id: usize, receiver: Arc<Mutex<mpsc::Receiver<Job>>>) -> Worker {
        let thread = thread::spawn(move || {
            loop {
                let message = receiver.lock().unwrap().recv();

                match message {
                    Ok(job) => {
                        println!("Worker {id} got a job; executing.");

                        job();
                    }
                    Err(_) => {
                        println!("Worker {id} disconnected; shutting down.");
                        break;
                    }
                }
            }
        });

        Worker {
            id,
            thread: Some(thread),
        }
    }
}
```

　　我们还能做更多！若你想继续增强这个项目，这里有一些想法：

- 为 `ThreadPool` 及其公共方法补充更多文档。
- 为库的功能添加测试。
- 把对 `unwrap` 的调用改成更稳健的错误处理。
- 用 `ThreadPool` 执行服务 Web 请求以外的任务。
- 在 [crates.io](https://crates.io/) 上找一个线程池 crate，改用该 crate 实现类似的 Web 服务器。然后把它的 API 与稳健性与我们实现的线程池做比较。

## 小结

　　干得好！你已经读到本书的结尾了！感谢你与我们一同走完这段 Rust 之旅。你现在已准备好实现自己的 Rust 项目，并帮助他人的项目。请记住：还有一个热情欢迎的 Rustacean 社区，乐于在你的 Rust 旅途中帮你应对遇到的任何挑战。
