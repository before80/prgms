+++
title = "21.2 从单线程到多线程服务器"
date = 2026-08-05T08:44:00+08:00
weight = 102
type = "docs"
description = "用线程池把单线程服务器升级为多线程服务器"
isCJKLanguage = true
draft = false
rust_version = "1.97.1"

+++

> 译文 · 基于 [The Rust Programming Language](https://doc.rust-lang.org/stable/book/)（rustc 1.97.1）

# 从单线程到多线程服务器


> 原文链接: [https://doc.rust-lang.org/stable/book/ch21-02-multithreaded.html](https://doc.rust-lang.org/stable/book/ch21-02-multithreaded.html)


## 从单线程到多线程服务器

　　眼下服务器会依次处理每个请求，也就是说在第一个连接处理完之前，不会处理第二个连接。若服务器收到越来越多的请求，这种串行执行会越来越不理想。若服务器收到一个要花很长时间处理的请求，后续请求就得等到这个长请求结束——哪怕新请求其实可以很快处理完。我们需要修好这一点，但先亲眼看看问题。

### 模拟慢请求

　　我们来看看处理缓慢的请求会如何影响对当前服务器实现发起的其他请求。示例 21-10 实现对 */sleep* 的请求处理：用模拟的慢响应让服务器在响应前睡眠五秒。

**文件名：`src/main.rs`**
```rust
use std::{
    fs,
    io::{BufReader, prelude::*},
    net::{TcpListener, TcpStream},
    thread,
    time::Duration,
};
// --snip--

fn handle_connection(mut stream: TcpStream) {
    // --snip--


    let (status_line, filename) = match &request_line[..] {
        "GET / HTTP/1.1" => ("HTTP/1.1 200 OK", "hello.html"),
        "GET /sleep HTTP/1.1" => {
            thread::sleep(Duration::from_secs(5));
            ("HTTP/1.1 200 OK", "hello.html")
        }
        _ => ("HTTP/1.1 404 NOT FOUND", "404.html"),
    };

    // --snip--

}
```

**示例 21-10：通过睡眠五秒模拟慢请求**

　　现在有三种情况，我们从 `if` 换成了 `match`。需要显式匹配 `request_line` 的切片才能与字符串字面量做模式匹配；`match` 不会像相等方法那样自动引用与解引用。

　　第一个分支与示例 21-9 的 `if` 块相同。第二个分支匹配对 */sleep* 的请求。收到该请求时，服务器会先睡眠五秒，再渲染成功的 HTML 页面。第三个分支与示例 21-9 的 `else` 块相同。

　　可以看出我们的服务器有多简陋：真正的库识别多种请求的方式会简洁得多！

　　用 `cargo run` 启动服务器。然后打开两个浏览器窗口：一个访问 *http://127.0.0.1:7878*，另一个访问 *http://127.0.0.1:7878/sleep*。若像之前一样多访问几次 */* URI，会看到响应很快。但若先打开 */sleep* 再加载 */*，你会看到 */* 要等到 `sleep` 睡满整整五秒后才会加载。

　　有多种技巧可以避免请求堵在慢请求后面，包括像第 17 章那样使用 async；我们要实现的是线程池。

### 用线程池提升吞吐量

　　*线程池*（thread pool）是一组已生成、就绪并等待处理任务的线程。程序收到新任务时，就把池中某个线程分配给该任务，由该线程处理。当第一个线程在处理时，池中其余线程仍可处理随后到来的其他任务。第一个线程处理完任务后，会回到空闲线程池，准备处理新任务。线程池让你能并发处理连接，从而提高服务器吞吐量。

　　我们会把池中线程数限制为较小的数字，以免遭受 DoS 攻击；若程序为每个到来的请求都新建线程，有人向服务器发起一千万次请求，就可能耗尽服务器全部资源，使请求处理陷入停顿。

　　因此我们不会无限制地生成线程，而是让固定数量的线程在池中等待。到来的请求被送入池中处理。池会维护一个传入请求的队列。池中每个线程从该队列弹出一个请求、处理它，然后再向队列要下一个请求。按这种设计，我们可以并发处理最多 *`N`* 个请求，其中 *`N`* 是线程数。若每个线程都在响应长时间运行的请求，后续请求仍可能在队列中积压，但我们提高了在到达该临界点之前能处理的长时间请求数量。

　　这种技巧只是提升 Web 服务器吞吐量的众多方式之一。你还可以探索 fork/join 模型、单线程异步 I/O 模型，以及多线程异步 I/O 模型。若对这个话题感兴趣，可以阅读其他方案并尝试实现；以 Rust 这样的底层语言，这些选项都可行。

　　在开始实现线程池之前，先谈谈使用这个池时应该长什么样。设计代码时，先写客户端接口有助于引导设计。先把代码的 API 写成你希望调用的结构；然后在该结构内实现功能，而不是先实现功能再设计公共 API。

　　与第 12 章项目中使用测试驱动开发类似，这里我们将使用编译器驱动开发。我们会先写调用所需函数的代码，再根据编译器错误决定下一步该改什么才能让代码工作。不过在此之前，我们先探索一下不打算采用的起点技巧。

#### 为每个请求生成一个线程

　　首先看看：若为每个连接都新建一个线程，代码会是什么样。如前所述，由于可能无限制地生成线程，这不是最终方案，但它是先让多线程服务器跑起来的起点。然后我们再把线程池作为改进加入，对比两种方案会更容易。

　　示例 21-11 展示对 `main` 的改动：在 `for` 循环内为每个流生成新线程来处理。

**文件名：`src/main.rs`**
```rust
fn main() {
    let listener = TcpListener::bind("127.0.0.1:7878").unwrap();

    for stream in listener.incoming() {
        let stream = stream.unwrap();

        thread::spawn(|| {
            handle_connection(stream);
        });
    }
}
```

**示例 21-11：为每个流生成一个新线程**

　　正如第 16 章所学，`thread::spawn` 会创建新线程，然后在新线程中运行闭包里的代码。若运行这段代码，在浏览器中加载 */sleep*，再在另外两个标签页加载 */*，你确实会看到对 */* 的请求不必等 */sleep* 结束。不过正如我们提到的，这最终会压垮系统，因为你会无限制地创建新线程。

　　你可能还记得第 17 章：这正是 async 和 await 特别适合的场景！在构建线程池时请记住这一点，并想想若改用 async，哪些地方会不同、哪些会相同。

#### 创建有限数量的线程 {#creating-a-finite-number-of-threads}

　　我们希望线程池以类似、熟悉的方式工作，这样从线程换成线程池时，使用我们 API 的代码不必大改。示例 21-12 展示我们希望用来替代 `thread::spawn` 的 `ThreadPool` 结构体的假想接口。

**文件名：`src/main.rs`**
```rust
fn main() {
    let listener = TcpListener::bind("127.0.0.1:7878").unwrap();
    let pool = ThreadPool::new(4);

    for stream in listener.incoming() {
        let stream = stream.unwrap();

        pool.execute(|| {
            handle_connection(stream);
        });
    }
}
```

**示例 21-12：我们理想中的 `ThreadPool` 接口**

　　我们用 `ThreadPool::new` 创建一个可配置线程数的新线程池，这里是四个。然后在 `for` 循环中，`pool.execute` 的接口与 `thread::spawn` 类似：接受一个闭包，由池为每个流运行。我们需要实现 `pool.execute`，使它接受闭包并交给池中某个线程运行。这段代码目前还不能编译，但我们会先试着编译，让编译器指引我们如何修复。

#### 用编译器驱动开发构建 `ThreadPool`

　　把示例 21-12 的改动做到 *src/main.rs*，然后用 `cargo check` 的编译器错误驱动开发。我们得到的第一个错误是：

```console
$ cargo check
    Checking hello v0.1.0 (file:///projects/hello)
error[E0433]: cannot find type `ThreadPool` in this scope
  --> src/main.rs:11:16
   |
11 |     let pool = ThreadPool::new(4);
   |                ^^^^^^^^^^ use of undeclared type `ThreadPool`

For more information about this error, try `rustc --explain E0433`.
error: could not compile `hello` (bin "hello") due to 1 previous error
```

　　很好！这个错误告诉我们需要 `ThreadPool` 类型或模块，于是现在就来构建一个。我们的 `ThreadPool` 实现与 Web 服务器具体在做什么工作无关。因此，把 `hello` crate 从二进制 crate 改成库 crate，以容纳 `ThreadPool` 实现。改成库 crate 之后，我们也可以把这个独立的线程池库用于任何想用线程池做的工作，而不仅是服务 Web 请求。

　　创建包含如下内容的 *src/lib.rs* 文件，这是我们目前能给出的最简单的 `ThreadPool` 结构体定义：

**文件名：`src/lib.rs`**
```rust
pub struct ThreadPool;
```

　　然后编辑 *main.rs*，通过在 *src/main.rs* 顶部加入下列代码，从库 crate 把 `ThreadPool` 引入作用域：

**文件名：`src/main.rs`**
```rust
use hello::ThreadPool;
```

　　这段代码仍无法工作，但我们再检查一次，以得到下一个需要处理的错误：

```console
$ cargo check
    Checking hello v0.1.0 (file:///projects/hello)
error[E0599]: no associated function or constant named `new` found for struct `ThreadPool` in the current scope
  --> src/main.rs:12:28
   |
12 |     let pool = ThreadPool::new(4);
   |                            ^^^ associated function or constant not found in `ThreadPool`

For more information about this error, try `rustc --explain E0599`.
error: could not compile `hello` (bin "hello") due to 1 previous error
```

　　这个错误表明接下来需要为 `ThreadPool` 创建一个名为 `new` 的关联函数。我们也知道 `new` 需要有一个能接受 `4` 作为参数的参数，并应返回一个 `ThreadPool` 实例。让我们实现具备这些特征的最简单的 `new` 函数：

**文件名：`src/lib.rs`**
```rust
pub struct ThreadPool;

impl ThreadPool {
    pub fn new(size: usize) -> ThreadPool {
        ThreadPool
    }
}
```

　　我们把 `size` 参数的类型选为 `usize`，因为负数个线程毫无意义。我们也知道会把这个 `4` 用作线程集合中的元素个数，而这正是 `usize` 类型的用途，正如第 3 章[「整数类型」][integer-types]一节所讨论的。

　　再检查一次代码：

```console
$ cargo check
    Checking hello v0.1.0 (file:///projects/hello)
error[E0599]: no method named `execute` found for struct `ThreadPool` in the current scope
  --> src/main.rs:17:14
   |
17 |         pool.execute(|| {
   |         -----^^^^^^^ method not found in `ThreadPool`

For more information about this error, try `rustc --explain E0599`.
error: could not compile `hello` (bin "hello") due to 1 previous error
```

　　现在错误是因为 `ThreadPool` 上没有 `execute` 方法。回想[「创建有限数量的线程」](#creating-a-finite-number-of-threads)一节，我们决定线程池应有与 `thread::spawn` 类似的接口。此外，我们将实现 `execute` 函数，使它接受给定的闭包，并交给池中某个空闲线程运行。

　　我们将在 `ThreadPool` 上定义 `execute` 方法，接受一个闭包作为参数。回想第 13 章[「从闭包中移出被捕获的值」][moving-out-of-closures]，我们可以用三种不同特征把闭包当作参数：`Fn`、`FnMut` 和 `FnOnce`。这里需要决定使用哪种闭包。我们知道最终会做与标准库 `thread::spawn` 实现类似的事，因此可以看看 `thread::spawn` 签名对其参数有哪些约束。文档显示如下：

```rust
pub fn spawn<F, T>(f: F) -> JoinHandle<T>
    where
        F: FnOnce() -> T,
        F: Send + 'static,
        T: Send + 'static,
```

　　这里我们关心的是类型参数 `F`；类型参数 `T` 与返回值有关，我们不关心。可以看到 `spawn` 对 `F` 使用了 `FnOnce` 作为特征约束。我们多半也想要这个，因为最终会把在 `execute` 中得到的参数传给 `spawn`。我们还可以更有把握地认为应使用 `FnOnce`：运行请求的线程只会执行该请求的闭包一次，这与 `FnOnce` 中的 `Once` 相符。

　　类型参数 `F` 还有特征约束 `Send` 和生命周期约束 `'static`，这在我们的场景中很有用：需要 `Send` 才能把闭包从一个线程传到另一个，需要 `'static` 是因为我们不知道线程要执行多久。让我们在 `ThreadPool` 上创建一个 `execute` 方法，接受带有这些约束的泛型参数 `F`：

**文件名：`src/lib.rs`**
```rust
impl ThreadPool {
    // --snip--

    pub fn execute<F>(&self, f: F)
    where
        F: FnOnce() + Send + 'static,
    {
    }
}
```

　　我们仍在 `FnOnce` 后面使用 `()`，因为这个 `FnOnce` 表示不接受参数并返回单元类型 `()` 的闭包。与函数定义一样，签名中可以省略返回类型，但即使没有参数，仍需要括号。

　　同样，这是 `execute` 方法最简单的实现：它什么也不做，我们只是想让代码能编译。再检查一次：

```console
$ cargo check
    Checking hello v0.1.0 (file:///projects/hello)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.24s
```

　　编译通过了！但注意若你尝试 `cargo run` 并在浏览器中发请求，仍会看到本章开头那种浏览器错误。我们的库实际上还没有调用传给 `execute` 的闭包！

> 注意：关于 Haskell、Rust 这类带严格编译器的语言，你可能听过一句话：「代码能编译，就能工作。」但这话并不普遍成立。我们的项目能编译，却完全什么都不做！若在构建真实、完整的项目，这时很适合开始写单元测试，检查代码既能编译 *又* 具有我们想要的行为。

　　想一想：若我们要执行的是 future 而不是闭包，这里会有什么不同？

#### 在 `new` 中校验线程数

　　我们还没有对 `new` 和 `execute` 的参数做任何事。让我们按想要的行为实现这些函数体。先从 `new` 想起。此前我们为 `size` 参数选了无符号类型，因为负数个线程的池毫无意义。然而零个线程的池同样毫无意义，而零却是完全合法的 `usize`。我们将加入代码，在返回 `ThreadPool` 实例之前检查 `size` 大于零；若收到零，就用 `assert!` 宏让程序 panic，如示例 21-13 所示。

**文件名：`src/lib.rs`**
```rust
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

        ThreadPool
    }

    // --snip--

}
```

**示例 21-13：实现 `ThreadPool::new`，在 `size` 为零时 panic**

　　我们还用文档注释为 `ThreadPool` 加了一些文档。注意我们遵循了良好的文档实践，增加了说明函数在哪些情况下会 panic 的小节，正如第 14 章所讨论的。试着运行 `cargo doc --open` 并点击 `ThreadPool` 结构体，看看为 `new` 生成的文档长什么样！

　　我们也可以不像这里这样加 `assert!` 宏，而是把 `new` 改成 `build` 并返回 `Result`，就像 I/O 项目示例 12-9 中的 `Config::build` 那样。但在这个例子里，我们认定尝试创建没有线程的线程池应是不可恢复的错误。若你有兴致，可以试着写一个名为 `build`、带有如下签名的函数，与 `new` 函数对比：

```rust
pub fn build(size: usize) -> Result<ThreadPool, PoolCreationError> {
```

#### 为存储线程腾出空间

　　现在我们有办法确认要存入池中的线程数有效，就可以在返回结构体之前创建这些线程并把它们存进 `ThreadPool` 结构体。但我们如何「存储」一个线程？再看一眼 `thread::spawn` 的签名：

```rust
pub fn spawn<F, T>(f: F) -> JoinHandle<T>
    where
        F: FnOnce() -> T,
        F: Send + 'static,
        T: Send + 'static,
```

　　`spawn` 函数返回 `JoinHandle<T>`，其中 `T` 是闭包返回的类型。我们也试试用 `JoinHandle`，看看会发生什么。在我们的例子中，传给线程池的闭包会处理连接且不返回任何东西，因此 `T` 将是单元类型 `()`。

　　示例 21-14 中的代码能编译，但还不会创建任何线程。我们改了 `ThreadPool` 的定义，使其保存 `thread::JoinHandle<()>` 实例的向量，用容量 `size` 初始化该向量，设置一个将运行某些代码以创建线程的 `for` 循环，并返回包含它们的 `ThreadPool` 实例。

**文件名：`src/lib.rs`**
```rust
use std::thread;

pub struct ThreadPool {
    threads: Vec<thread::JoinHandle<()>>,
}

impl ThreadPool {
    // --snip--

    pub fn new(size: usize) -> ThreadPool {
        assert!(size > 0);

        let mut threads = Vec::with_capacity(size);

        for _ in 0..size {
            // create some threads and store them in the vector
        }

        ThreadPool { threads }
    }
    // --snip--

}
```

**示例 21-14：创建供 `ThreadPool` 保存线程的向量**

　　我们在库 crate 中把 `std::thread` 引入了作用域，因为要把 `thread::JoinHandle` 用作 `ThreadPool` 中向量元素的类型。

　　一旦收到有效的 size，我们的 `ThreadPool` 就创建一个能容纳 `size` 个元素的新向量。`with_capacity` 函数与 `Vec::new` 完成相同任务，但有一个重要差别：它会预先分配向量中的空间。因为我们知道需要在向量中存储 `size` 个元素，提前做这次分配比使用会在插入元素时自行调整大小的 `Vec::new` 略高效一些。

　　再运行 `cargo check` 时，它应能成功。

#### 把代码从 `ThreadPool` 发送到线程

　　我们在示例 21-14 的 `for` 循环里留了一条关于创建线程的注释。这里来看如何真正创建线程。标准库提供 `thread::spawn` 作为创建线程的方式，而 `thread::spawn` 期望在线程创建时就拿到线程应运行的一些代码。但在我们的例子中，我们希望创建线程并让它们 *等待* 我们稍后发送的代码。标准库的线程实现没有提供这样做的方式；我们必须手动实现。

　　我们将通过在 `ThreadPool` 与线程之间引入一个新的数据结构来管理这种新行为，从而实现这一点。我们把这个数据结构叫做 *Worker*（工作者），这是池化实现中的常用术语。`Worker` 领取需要运行的代码，并在自己的线程中运行。

　　可以想想餐厅厨房里的人：工作者等到顾客点单到来，然后负责接下这些订单并完成。

　　我们不再在线程池中存储 `JoinHandle<()>` 实例的向量，而是存储 `Worker` 结构体的实例。每个 `Worker` 会存储一个 `JoinHandle<()>` 实例。然后我们在 `Worker` 上实现一个方法，接受要运行的代码闭包，并把它发送到已经在运行的线程去执行。我们还会给每个 `Worker` 一个 `id`，以便在日志或调试时区分池中不同的 `Worker` 实例。

　　创建 `ThreadPool` 时将发生的新流程如下。我们会在按这种方式建好 `Worker` 之后，再实现把闭包发送到线程的代码：

1. 定义保存 `id` 与 `JoinHandle<()>` 的 `Worker` 结构体。
2. 把 `ThreadPool` 改为保存 `Worker` 实例的向量。
3. 定义 `Worker::new` 函数，接受一个 `id` 编号，并返回保存该 `id`、以及用空闭包生成的线程的 `Worker` 实例。
4. 在 `ThreadPool::new` 中，用 `for` 循环计数器生成 `id`，用该 `id` 创建新的 `Worker`，并把 `Worker` 存入向量。

　　若你想挑战一下，可以先自己尝试实现这些改动，再看示例 21-15 中的代码。

　　准备好了吗？示例 21-15 给出了完成上述修改的一种方式。

**文件名：`src/lib.rs`**
```rust
use std::thread;

pub struct ThreadPool {
    workers: Vec<Worker>,
}

impl ThreadPool {
    // --snip--

    pub fn new(size: usize) -> ThreadPool {
        assert!(size > 0);

        let mut workers = Vec::with_capacity(size);

        for id in 0..size {
            workers.push(Worker::new(id));
        }

        ThreadPool { workers }
    }
    // --snip--

}

struct Worker {
    id: usize,
    thread: thread::JoinHandle<()>,
}

impl Worker {
    fn new(id: usize) -> Worker {
        let thread = thread::spawn(|| {});

        Worker { id, thread }
    }
}
```

**示例 21-15：修改 `ThreadPool`，使其保存 `Worker` 实例而不是直接保存线程**

　　我们把 `ThreadPool` 上字段的名字从 `threads` 改成了 `workers`，因为它现在保存的是 `Worker` 实例而不是 `JoinHandle<()>` 实例。我们把 `for` 循环中的计数器作为参数传给 `Worker::new`，并把每个新的 `Worker` 存入名为 `workers` 的向量。

　　外部代码（如 *src/main.rs* 中的服务器）不需要知道在 `ThreadPool` 内使用 `Worker` 结构体的实现细节，因此我们把 `Worker` 结构体及其 `new` 函数设为私有。`Worker::new` 函数使用我们给出的 `id`，并存储通过用空闭包生成新线程而创建的 `JoinHandle<()>` 实例。

> 注意：若操作系统因系统资源不足而无法创建线程，`thread::spawn` 会 panic。那会使整个服务器 panic，即便部分线程的创建可能已经成功。为简单起见，这种行为可以接受，但在生产级线程池实现中，你多半会想用 [`std::thread::Builder`][builder] 及其返回 `Result` 的 [`spawn`][builder-spawn] 方法。

　　这段代码能编译，并会存储我们作为参数传给 `ThreadPool::new` 的数量的 `Worker` 实例。但我们 *仍然* 没有处理在 `execute` 中得到的闭包。接下来看看如何做到。

#### 通过通道把请求发送到线程

　　接下来要解决的问题是：传给 `thread::spawn` 的闭包完全什么也不做。目前我们在 `execute` 方法中得到想要执行的闭包。但我们需要在创建 `ThreadPool` 时为每个 `Worker` 创建时，就给 `thread::spawn` 一个要运行的闭包。

　　我们希望刚创建的 `Worker` 结构体从 `ThreadPool` 持有的队列中取要运行的代码，并把该代码发送到自己的线程去运行。

　　第 16 章学过的通道——在两个线程间通信的简单方式——非常适合这个用例。我们将用通道充当任务队列，`execute` 会从 `ThreadPool` 向 `Worker` 实例发送任务，再由 `Worker` 把任务送到自己的线程。计划如下：

1. `ThreadPool` 创建一条通道并持有发送端。
2. 每个 `Worker` 持有接收端。
3. 我们将创建一个新的 `Job` 结构体，用来保存要通过通道发送的闭包。
4. `execute` 方法通过发送端发送它想要执行的任务。
5. 在其线程中，`Worker` 循环遍历其接收端，并执行收到的任何任务的闭包。

　　先从在 `ThreadPool::new` 中创建通道、并把发送端保存在 `ThreadPool` 实例中开始，如示例 21-16 所示。`Job` 结构体目前不保存任何东西，但会是我们通过通道发送的项的类型。

**文件名：`src/lib.rs`**
```rust
use std::{sync::mpsc, thread};

pub struct ThreadPool {
    workers: Vec<Worker>,
    sender: mpsc::Sender<Job>,
}

struct Job;

impl ThreadPool {
    // --snip--

    pub fn new(size: usize) -> ThreadPool {
        assert!(size > 0);

        let (sender, receiver) = mpsc::channel();

        let mut workers = Vec::with_capacity(size);

        for id in 0..size {
            workers.push(Worker::new(id));
        }

        ThreadPool { workers, sender }
    }
    // --snip--

}
```

**示例 21-16：修改 `ThreadPool`，使其存储发送 `Job` 实例的通道发送端**

　　在 `ThreadPool::new` 中，我们创建新通道并让池持有发送端。这会成功编译。

　　试着在线程池创建通道时，把通道的接收端传给每个 `Worker`。我们知道要在 `Worker` 实例生成的线程中使用接收端，因此会在闭包中引用 `receiver` 参数。示例 21-17 中的代码还不能完全编译。

**文件名：`src/lib.rs`**
```rust
impl ThreadPool {
    // --snip--

    pub fn new(size: usize) -> ThreadPool {
        assert!(size > 0);

        let (sender, receiver) = mpsc::channel();

        let mut workers = Vec::with_capacity(size);

        for id in 0..size {
            workers.push(Worker::new(id, receiver));
        }

        ThreadPool { workers, sender }
    }
    // --snip--

}

// --snip--


impl Worker {
    fn new(id: usize, receiver: mpsc::Receiver<Job>) -> Worker {
        let thread = thread::spawn(|| {
            receiver;
        });

        Worker { id, thread }
    }
}
```

**示例 21-17：把接收端传给每个 `Worker`**

　　我们做了一些小而直接的改动：把接收端传入 `Worker::new`，然后在闭包内使用它。

　　尝试检查这段代码时，我们得到这个错误：

```console
$ cargo check
    Checking hello v0.1.0 (file:///projects/hello)
error[E0382]: use of moved value: `receiver`
  --> src/lib.rs:26:42
   |
21 |         let (sender, receiver) = mpsc::channel();
   |                      -------- move occurs because `receiver` has type `std::sync::mpsc::Receiver<Job>`, which does not implement the `Copy` trait
...
25 |         for id in 0..size {
   |         ----------------- inside of this loop
26 |             workers.push(Worker::new(id, receiver));
   |                                          ^^^^^^^^ value moved here, in previous iteration of loop
   |
note: consider changing this parameter type in method `new` to borrow instead if owning the value isn't necessary
  --> src/lib.rs:47:33
   |
47 |     fn new(id: usize, receiver: mpsc::Receiver<Job>) -> Worker {
   |        --- in this method       ^^^^^^^^^^^^^^^^^^^ this parameter takes ownership of the value

For more information about this error, try `rustc --explain E0382`.
error: could not compile `hello` (lib) due to 1 previous error
```

　　代码正试图把 `receiver` 传给多个 `Worker` 实例。这行不通，正如你从第 16 章记得的：Rust 提供的通道实现是多 *生产者*、单 *消费者*。这意味着我们不能只靠克隆通道的消费端来修好这段代码。我们也不想把同一条消息多次发给多个消费者；我们想要一份消息列表、多个 `Worker` 实例，使每条消息只被处理一次。

　　此外，从通道队列取走任务涉及修改 `receiver`，因此线程需要一种安全方式共享并修改 `receiver`；否则可能出现竞态条件（如第 16 章所述）。

　　回想第 16 章讨论的线程安全智能指针：要在多个线程间共享所有权并允许线程修改值，需要使用 `Arc<Mutex<T>>`。`Arc` 类型让多个 `Worker` 实例拥有接收端，而 `Mutex` 确保同一时间只有一个 `Worker` 从接收端取得任务。示例 21-18 展示需要做的改动。

**文件名：`src/lib.rs`**
```rust
use std::{
    sync::{Arc, Mutex, mpsc},
    thread,
};
// --snip--


impl ThreadPool {
    // --snip--

    pub fn new(size: usize) -> ThreadPool {
        assert!(size > 0);

        let (sender, receiver) = mpsc::channel();

        let receiver = Arc::new(Mutex::new(receiver));

        let mut workers = Vec::with_capacity(size);

        for id in 0..size {
            workers.push(Worker::new(id, Arc::clone(&receiver)));
        }

        ThreadPool { workers, sender }
    }

    // --snip--

}

// --snip--


impl Worker {
    fn new(id: usize, receiver: Arc<Mutex<mpsc::Receiver<Job>>>) -> Worker {
        // --snip--

    }
}
```

**示例 21-18：用 `Arc` 与 `Mutex` 在各 `Worker` 实例间共享接收端**

　　在 `ThreadPool::new` 中，我们把接收端放进 `Arc` 和 `Mutex`。对每个新的 `Worker`，我们克隆 `Arc` 以增加引用计数，好让各 `Worker` 实例共享接收端的所有权。

　　有了这些改动，代码能编译了！我们快成功了！

#### 实现 `execute` 方法

　　终于来实现 `ThreadPool` 上的 `execute` 方法。我们也会把 `Job` 从结构体改成类型别名，指向保存 `execute` 所接收闭包类型的特征对象。正如第 20 章[「类型同义词与类型别名」][type-aliases]一节所讨论的，类型别名让我们可以把冗长类型写得更短以便使用。见示例 21-19。

**文件名：`src/lib.rs`**
```rust
// --snip--

type Job = Box<dyn FnOnce() + Send + 'static>;

impl ThreadPool {
    // --snip--

    pub fn execute<F>(&self, f: F)
    where
        F: FnOnce() + Send + 'static,
    {
        let job = Box::new(f);

        self.sender.send(job).unwrap();
    }
}

// --snip--
```

**示例 21-19：为保存每个闭包的 `Box` 创建 `Job` 类型别名，然后把任务发入通道**

　　用在 `execute` 中得到的闭包创建新的 `Job` 实例后，我们通过通道的发送端发送该任务。我们对 `send` 调用 `unwrap`，以应对发送失败的情况。例如，若我们停止了所有线程的执行，接收端就会停止接收新消息，就可能发生这种情况。目前我们还不能停止线程执行：只要池存在，线程就会继续执行。我们使用 `unwrap` 是因为我们知道失败情况不会发生，但编译器并不知道。

　　但我们还没完全做完！在 `Worker` 中，传给 `thread::spawn` 的闭包仍然只是 *引用* 通道的接收端。我们需要闭包永远循环，向通道接收端索取任务，并在拿到时运行任务。让我们对 `Worker::new` 做示例 21-20 所示的改动。

**文件名：`src/lib.rs`**
```rust
// --snip--

impl Worker {
    fn new(id: usize, receiver: Arc<Mutex<mpsc::Receiver<Job>>>) -> Worker {
        let thread = thread::spawn(move || {
            loop {
                let job = receiver.lock().unwrap().recv().unwrap();

                println!("Worker {id} got a job; executing.");

                job();
            }
        });

        Worker { id, thread }
    }
}
```

**示例 21-20：在 `Worker` 实例的线程中接收并执行任务**

　　这里我们先对 `receiver` 调用 `lock` 以获取互斥锁，再调用 `unwrap` 以便在有任何错误时 panic。若互斥锁处于 *中毒*（poisoned）状态——可能发生在其他线程持有锁时 panic 而没有释放锁——获取锁可能失败。在这种情况下，调用 `unwrap` 让本线程也 panic 是正确做法。你可以随意把这个 `unwrap` 改成带有对你有意义的错误消息的 `expect`。

　　若拿到了互斥锁，我们就调用 `recv` 从通道接收一个 `Job`。这里最后还有一个 `unwrap` 用以跳过任何错误，错误可能发生在持有发送端的线程已关闭时，类似于接收端关闭时 `send` 方法返回 `Err`。

　　对 `recv` 的调用会阻塞，因此若还没有任务，当前线程会等到有任务可用。`Mutex<T>` 确保同一时间只有一个 `Worker` 线程在尝试请求任务。

　　我们的线程池现在处于可工作状态了！运行 `cargo run` 并发一些请求：


```console
$ cargo run
   Compiling hello v0.1.0 (file:///projects/hello)
warning: field `workers` is never read
 --> src/lib.rs:7:5
  |
6 | pub struct ThreadPool {
  |            ---------- field in this struct
7 |     workers: Vec<Worker>,
  |     ^^^^^^^
  |
  = note: `#[warn(dead_code)]` on by default

warning: fields `id` and `thread` are never read
  --> src/lib.rs:48:5
   |
47 | struct Worker {
   |        ------ fields in this struct
48 |     id: usize,
   |     ^^
49 |     thread: thread::JoinHandle<()>,
   |     ^^^^^^

warning: `hello` (lib) generated 2 warnings
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 4.91s
     Running `target/debug/hello`
Worker 0 got a job; executing.
Worker 2 got a job; executing.
Worker 1 got a job; executing.
Worker 3 got a job; executing.
Worker 0 got a job; executing.
Worker 2 got a job; executing.
Worker 1 got a job; executing.
Worker 3 got a job; executing.
Worker 0 got a job; executing.
Worker 2 got a job; executing.
```

　　成功了！我们现在有了一个异步执行连接的线程池。创建的线程永远不会超过四个，因此即使服务器收到大量请求，系统也不会过载。若我们请求 */sleep*，服务器也能让另一个线程运行其他请求来继续服务。

> 注意：若你在多个浏览器窗口中同时打开 */sleep*，它们可能每隔五秒依次加载。一些 Web 浏览器出于缓存原因会按顺序执行同一请求的多个实例。这一限制并非由我们的 Web 服务器造成。

　　这是个很好的停顿点，想想若用 future 而不是闭包作为要完成的工作，示例 21-18、21-19 和 21-20 中的代码会有何不同。哪些类型会变？方法签名会如何不同（如果有的话）？代码的哪些部分会保持不变？

　　在第 17 章和第 19 章学过 `while let` 循环之后，你可能想知道为什么我们没有把 `Worker` 线程代码写成示例 21-21 那样。

**文件名：`src/lib.rs`**
```rust
// --snip--

impl Worker {
    fn new(id: usize, receiver: Arc<Mutex<mpsc::Receiver<Job>>>) -> Worker {
        let thread = thread::spawn(move || {
            while let Ok(job) = receiver.lock().unwrap().recv() {
                println!("Worker {id} got a job; executing.");

                job();
            }
        });

        Worker { id, thread }
    }
}
```

**示例 21-21：用 `while let` 实现 `Worker::new` 的另一种写法**

　　这段代码能编译并运行，但不会得到想要的线程行为：慢请求仍会导致其他请求等待处理。原因有些微妙：`Mutex` 结构体没有公开的 `unlock` 方法，因为锁的所有权基于 `lock` 方法返回的 `LockResult<MutexGuard<T>>` 中 `MutexGuard<T>` 的生命周期。在编译期，借用检查器可以据此强制执行规则：除非我们持有锁，否则不能访问受 `Mutex` 保护的资源。然而，若我们不留意 `MutexGuard<T>` 的生命周期，这种实现也可能导致持锁时间比预期更长。

　　示例 21-20 中使用 `let job = receiver.lock().unwrap().recv().unwrap();` 的代码之所以有效，是因为有了 `let`，等号右侧表达式中使用的任何临时值都会在 `let` 语句结束时立即被丢弃。然而，`while let`（以及 `if let` 和 `match`）要到相关块结束才会丢弃临时值。在示例 21-21 中，在调用 `job()` 的整个期间都会持有锁，意味着其他 `Worker` 实例无法接收任务。

[type-aliases]: ../../advanced-features/03-advanced-types/#type-synonyms-and-type-aliases
[integer-types]: ../../common-programming-concepts/02-data-types/#integer-types
[moving-out-of-closures]: ../../functional-features/01-closures/#moving-captured-values-out-of-closures
[builder]: https://doc.rust-lang.org/stable/std/thread/struct.Builder.html
[builder-spawn]: https://doc.rust-lang.org/stable/std/thread/struct.Builder.html#method.spawn
