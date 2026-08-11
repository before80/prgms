+++
title = "17.1 Future 与 async 语法"
date = 2026-08-05T08:44:00+08:00
weight = 80
type = "docs"
description = "讲解 Future、async/await 语法，并用运行时编写第一个异步程序"
isCJKLanguage = true
draft = false
rust_version = "1.97.1"

+++

> 译文 · 基于 [The Rust Programming Language](https://doc.rust-lang.org/stable/book/)（rustc 1.97.1）

# Future 与 async 语法 {#futures-and-syntax}


> 原文链接: [https://doc.rust-lang.org/stable/book/ch17-01-futures-and-syntax.html](https://doc.rust-lang.org/stable/book/ch17-01-futures-and-syntax.html)


## Future 与 async 语法

　　Rust 异步编程的关键要素是 *Future* 以及 Rust 的 `async` 与 `await` 关键字。

　　*Future* 是一个现在可能尚未就绪、但将来某时刻会就绪的值。（同一概念出现在许多语言中，有时也叫 *task* 或 *promise*。）Rust 提供 `Future` trait 作为构建块，使不同异步操作可用不同数据结构实现，却共享统一接口。在 Rust 中，Future 就是实现了 `Future` trait 的类型。每个 Future 都保存自己关于已取得进展以及何谓“就绪”的信息。

　　可以把 `async` 关键字用于块与函数，以标明它们可被打断并恢复。在异步块或异步函数内，可用 `await` 关键字去*等待一个 Future*（也就是等它变为就绪）。在异步块或函数内等待 Future 的任何位置，都是该块或函数可能暂停与恢复的潜在点。向 Future 查询其值是否已可用的过程称为*轮询*（polling）。

　　另一些语言，如 C# 与 JavaScript，也用 `async` 与 `await` 关键字做异步编程。若你熟悉那些语言，可能会注意到 Rust 处理语法的若干显著不同。这是有充分理由的，我们稍后会看到！

　　编写异步 Rust 时，多数时间我们使用 `async` 与 `await` 关键字。Rust 会把它们编译成使用 `Future` trait 的等价代码，就像把 `for` 循环编译成使用 `Iterator` trait 的等价代码一样。不过因为 Rust 提供了 `Future` trait，需要时你也可以为自己的数据类型实现它。本章中我们将看到的许多函数都会返回带有各自 `Future` 实现的类型。本章末尾我们会回到该 trait 的定义并深入其工作方式，但目前这些细节已足够继续前进。

　　这一切可能仍有些抽象，那就来写我们的第一个异步程序：一个小爬虫。我们从命令行传入两个 URL，并发抓取两者，并返回先完成的那个结果。这个例子会有不少新语法，别担心——我们会边走边解释你需要知道的一切。

## 我们的第一个异步程序 {#our-first-async-program}

　　为把本章重点放在学习 async 而非折腾生态里的各种零件，我们创建了 `trpl` crate（`trpl` 是 “The Rust Programming Language” 的缩写）。它主要从 [`futures`][futures-crate] 与 [`tokio`][tokio] crate 再导出你需要的全部类型、trait 与函数。`futures` crate 是 Rust 异步代码实验的官方家园，`Future` trait 最初也是在那里设计的。Tokio 是当今 Rust 中使用最广的异步运行时，尤其在 Web 应用中。还有其他优秀的运行时，可能更适合你的用途。我们在 `trpl` 底层使用 `tokio`，因为它经过充分测试且广泛使用。

　　有些情况下，`trpl` 也会重命名或包装原始 API，好让你专注于与本章相关的细节。若想了解该 crate 做了什么，建议查看[其源码][crate-source]。你能看到每个再导出分别来自哪个 crate，我们也留下了大量注释解释 crate 的行为。

　　创建一个名为 `hello-async` 的新二进制项目，并添加 `trpl` 依赖：

```console
$ cargo new hello-async
$ cd hello-async
$ cargo add trpl
```

　　现在可以用 `trpl` 提供的各种部件编写第一个异步程序。我们将做一个小命令行工具：抓取两个网页，从各自抽出 `<title>` 元素，并打印先完成整个流程的那个页面的标题。

### 定义 page_title 函数

　　先写一个函数：接受一个页面 URL，向其发请求，并返回 `<title>` 元素的文本（见示例 17-1）。

**文件名：`src/main.rs`**
```rust
use trpl::Html;

async fn page_title(url: &str) -> Option<String> {
    let response = trpl::get(url).await;
    let response_text = response.text().await;
    Html::parse(&response_text)
        .select_first("title")
        .map(|title| title.inner_html())
}
```

**示例 17-1：定义异步函数以获取 HTML 页面中的 title 元素**

　　首先定义名为 `page_title` 的函数并用 `async` 关键字标记。然后用 `trpl::get` 抓取传入的 URL，并加上 `await` 关键字等待响应。要得到 `response` 的文本，调用其 `text` 方法，并再次用 `await` 等待。这两步都是异步的。对 `get` 函数，我们必须等待服务器发回响应的第一部分，其中包含 HTTP 头、cookie 等，且可以与响应体分开送达。尤其当响应体很大时，全部到达可能要一些时间。因为我们必须等待响应的*全部*内容到达，`text` 方法也是异步的。

　　我们必须显式等待这两个 Future，因为 Rust 中的 Future 是*惰性*的：在你用 `await` 关键字要求之前，它们什么都不做。（实际上，若你不使用某个 Future，Rust 会给出编译器警告。）这或许会让你想起第 13 章[「用迭代器处理一系列项」][iterators-lazy]一节中对迭代器的讨论。迭代器在你调用其 `next` 方法之前什么都不做——无论是直接调用，还是通过使用底层会调用 `next` 的 `for` 循环或 `map` 等方法。同样，Future 在你显式要求之前什么都不做。这种惰性使 Rust 能避免在真正需要之前运行异步代码。

> 注意：这与我们在第 16 章[「用 spawn 创建新线程」][thread-spawn]一节中使用 `thread::spawn` 时看到的行为不同：传给另一线程的闭包会立即开始运行。这也与许多其他语言处理 async 的方式不同。但对 Rust 而言，这对其提供性能保证很重要，就像对迭代器一样。

　　有了 `response_text` 后，可以用 `Html::parse` 把它解析成 `Html` 类型的实例。我们不再只有原始字符串，而是有了可把 HTML 当作更丰富数据结构来处理的类型。具体来说，可以用 `select_first` 方法查找给定 CSS 选择器的第一个匹配。传入字符串 `"title"`，就会得到文档中第一个 `<title>` 元素（若存在）。因为可能没有匹配元素，`select_first` 返回 `Option<ElementRef>`。最后使用 `Option::map` 方法：若 `Option` 中有值就可对其操作，没有则什么都不做。（这里也可以用 `match` 表达式，但 `map` 更惯用。）在提供给 `map` 的函数体中，对 `title` 调用 `inner_html` 获取其内容，类型为 `String`。最终我们得到 `Option<String>`。

　　注意 Rust 的 `await` 关键字放在你所等待的表达式*之后*，而不是之前。也就是说，它是*后缀*关键字。若你在其他语言中用过 `async`，这可能与你习惯的不同，但在 Rust 中它让方法链好用得多。因此，我们可以把 `page_title` 的函数体改成用夹在中间的 `await` 把 `trpl::get` 与 `text` 调用链起来，如示例 17-2 所示。

**文件名：`src/main.rs`**
```rust
    let response_text = trpl::get(url).await.text().await;
```

**示例 17-2：用 `await` 关键字串联调用**

　　至此，我们成功写出了第一个异步函数！在向 `main` 添加调用它的代码之前，先多谈谈我们已经写了什么、意味着什么。

　　当 Rust 看到标有 `async` 关键字的*块*时，会把它编译成实现了 `Future` trait 的唯一匿名数据类型。当 Rust 看到标有 `async` 的*函数*时，会把它编译成一个非异步函数，其函数体是一个异步块。异步函数的返回类型就是编译器为该异步块创建的那个匿名数据类型的类型。

　　因此，写 `async fn` 等价于写一个返回“该返回类型的 Future”的函数。对编译器而言，示例 17-1 中的 `async fn page_title` 这类函数定义，大致等价于如下定义的非异步函数：

```rust
# extern crate trpl; // required for mdbook test
use std::future::Future;
use trpl::Html;

fn page_title(url: &str) -> impl Future<Output = Option<String>> {
    async move {
        let text = trpl::get(url).await.text().await;
        Html::parse(&text)
            .select_first("title")
            .map(|title| title.inner_html())
    }
}
```

　　我们逐部分看这个变换后的版本：

- 它使用了我们在第 10 章[「Trait 作为参数」][impl-trait]一节讨论过的 `impl Trait` 语法。
- 返回值实现了关联类型为 `Output` 的 `Future` trait。注意 `Output` 类型是 `Option<String>`，与原来 `async fn` 版 `page_title` 的返回类型相同。
- 原函数体中调用的全部代码被包在一个 `async move` 块里。记住块是表达式。整个块就是函数返回的表达式。
- 这个异步块产生类型为 `Option<String>` 的值，正如刚描述的那样。该值与返回类型中的 `Output` 类型匹配。这与你见过的其他块一样。
- 新函数体是 `async move` 块，是因为它对 `url` 参数的使用方式。（本章稍后会更多讨论 `async` 与 `async move`。）

　　现在我们可以在 `main` 中调用 `page_title` 了。

### 用运行时执行异步函数

　　我们先获取单个页面的标题，如示例 17-3 所示。不幸的是，这段代码目前还不能编译。

**文件名：`src/main.rs`**
```rust
async fn main() {
    let args: Vec<String> = std::env::args().collect();
    let url = &args[1];
    match page_title(url).await {
        Some(title) => println!("The title for {url} was {title}"),
        None => println!("{url} had no title"),
    }
}
```

**示例 17-3：在 `main` 中用用户提供的参数调用 `page_title` 函数**

　　我们沿用第 12 章[「接受命令行参数」][cli-args]一节中获取命令行参数的同一模式。然后把 URL 参数传给 `page_title` 并等待结果。因为 Future 产生的值是 `Option<String>`，我们用 `match` 表达式打印不同消息，以区分页面是否有 `<title>`。

　　唯一能使用 `await` 关键字的地方是异步函数或块，而 Rust 不允许把特殊的 `main` 函数标为 `async`。


```text
error[E0752]: `main` function is not allowed to be `async`
 --> src/main.rs:6:1
  |
6 | async fn main() {
  | ^^^^^^^^^^^^^^^ `main` function is not allowed to be `async`
```

　　`main` 不能标为 `async` 的原因是：异步代码需要*运行时*——一个管理执行异步代码细节的 Rust crate。程序的 `main` 函数可以*初始化*运行时，但它本身不是运行时。（稍后会更多看到为何如此。）每个执行异步代码的 Rust 程序，都至少有一处设置运行时来执行 Future。

　　多数支持 async 的语言会捆绑运行时，但 Rust 不会。相反，有许多不同的异步运行时可用，各自做出适合其目标用例的不同取舍。例如，拥有许多 CPU 核心与大量 RAM 的高吞吐 Web 服务器，与只有单核、少量 RAM 且无法堆分配的微控制器，需求截然不同。提供这些运行时的 crate 也常常提供文件或网络 I/O 等常见功能的异步版本。

　　这里以及本章其余部分，我们将使用 `trpl` crate 的 `block_on` 函数：它接受一个 Future 作为参数，并阻塞当前线程直到该 Future 运行完成。在幕后，调用 `block_on` 会用 `tokio` crate 设置运行时来运行传入的 Future（`trpl` crate 的 `block_on` 行为与其他运行时 crate 的 `block_on` 函数类似）。Future 完成后，`block_on` 返回该 Future 产生的值。

　　我们可以把 `page_title` 返回的 Future 直接传给 `block_on`，完成后像示例 17-3 中试图做的那样对得到的 `Option<String>` 做匹配。不过，对本章中的大多数例子（以及现实世界中的大多数异步代码），我们做的不止一次异步函数调用，因此改为传入一个 `async` 块并显式等待 `page_title` 调用的结果，如示例 17-4 所示。

**文件名：`src/main.rs`**

```rust
fn main() {
    let args: Vec<String> = std::env::args().collect();

    trpl::block_on(async {
        let url = &args[1];
        match page_title(url).await {
            Some(title) => println!("The title for {url} was {title}"),
            None => println!("{url} had no title"),
        }
    })
}
```

**示例 17-4：用 `trpl::block_on` 等待一个异步块**

　　运行这段代码时，会得到我们最初期望的行为：


```console
$ cargo run -- "https://www.rust-lang.org"
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.05s
     Running `target/debug/async_await 'https://www.rust-lang.org'`
The title for https://www.rust-lang.org was
            Rust Programming Language
```

　　呼——我们终于有了可运行的异步代码！但在添加让两个站点竞速的代码之前，先简要回到 Future 如何工作。

　　每个 *await 点*——也就是代码使用 `await` 关键字的每一处——都代表把控制权交还给运行时的位置。为使这能工作，Rust 需要跟踪异步块中涉及的状态，以便运行时可以启动其他工作，并在准备好再次推进第一个时回来。这是一个无形的状态机，就好像你手写了这样一个枚举，在每个 await 点保存当前状态：

```rust
enum PageTitleFuture<'a> {
    Initial { url: &'a str },
    GetAwaitPoint { url: &'a str },
    TextAwaitPoint { response: trpl::Response },
}
```

　　不过，手写在各状态之间转换的代码会既繁琐又易错，尤其是以后还要给代码增加更多功能与更多状态时。幸好，Rust 编译器会自动为异步代码创建并管理状态机数据结构。围绕数据结构的正常借用与所有权规则仍然适用，而且编译器也会为我们检查这些规则，并提供有用的错误信息。本章稍后会处理其中的几个。

　　最终，必须有东西来执行这个状态机，那个东西就是运行时。（这就是你在研究运行时时常会遇到 *executor*（执行器）一词的原因：执行器是运行时中负责执行异步代码的部分。）

　　现在你能明白，为何编译器在示例 17-3 中阻止我们把 `main` 本身做成异步函数。若 `main` 是异步函数，就需要别的东西来管理 `main` 所返回 Future 的状态机，但 `main` 是程序的起点！相反，我们在 `main` 中调用 `trpl::block_on` 来设置运行时，并运行 `async` 块返回的 Future 直到结束。

> 注意：有些运行时提供宏，使你*可以*写异步 `main` 函数。那些宏会把 `async fn main() { ... }` 改写成普通的 `fn main`，其做法与我们在示例 17-4 中手工做的相同：调用一个像 `trpl::block_on` 那样把 Future 跑到完成的函数。

　　现在把这些拼在一起，看看如何编写并发代码。

### 并发地让两个 URL 竞速

　　在示例 17-5 中，我们对命令行传入的两个不同 URL 调用 `page_title`，并通过选择先完成的 Future 来让它们竞速。

**文件名：`src/main.rs`**

```rust
use trpl::{Either, Html};

fn main() {
    let args: Vec<String> = std::env::args().collect();

    trpl::block_on(async {
        let title_fut_1 = page_title(&args[1]);
        let title_fut_2 = page_title(&args[2]);

        let (url, maybe_title) =
            match trpl::select(title_fut_1, title_fut_2).await {
                Either::Left(left) => left,
                Either::Right(right) => right,
            };

        println!("{url} returned first");
        match maybe_title {
            Some(title) => println!("Its page title was: '{title}'"),
            None => println!("It had no title."),
        }
    })
}

async fn page_title(url: &str) -> (&str, Option<String>) {
    let response_text = trpl::get(url).await.text().await;
    let title = Html::parse(&response_text)
        .select_first("title")
        .map(|title| title.inner_html());
    (url, title)
}
```

**示例 17-5：对两个 URL 调用 `page_title` 看哪个先返回**

　　我们先对用户提供的每个 URL 调用 `page_title`，把得到的 Future 存为 `title_fut_1` 与 `title_fut_2`。记住，它们此刻什么都不做，因为 Future 是惰性的，我们还没有等待它们。然后把这些 Future 传给 `trpl::select`，它返回一个值，标明传给它的哪个 Future 先完成。

> 注意：在底层，`trpl::select` 建立在 `futures` crate 中定义的更通用的 `select` 函数之上。`futures` crate 的 `select` 能做许多 `trpl::select` 做不到的事，但也有一些额外复杂性，我们现在可以跳过。

　　任一 Future 都可以合理地“获胜”，因此返回 `Result` 没有意义。相反，`trpl::select` 返回我们尚未见过的类型 `trpl::Either`。`Either` 类型有点像 `Result`，也有两个分支。但与 `Result` 不同，`Either` 并不内建成功或失败的概念。相反，它用 `Left` 与 `Right` 表示“二者之一”：

```rust
enum Either<A, B> {
    Left(A),
    Right(B),
}
```

　　若第一个参数获胜，`select` 函数返回带有该 Future 输出的 `Left`；若*第二个* Future 参数获胜，则返回带有其输出的 `Right`。这与调用函数时参数出现的顺序一致：第一个参数在第二个参数的左边。

　　我们还更新了 `page_title`，让它返回传入的同一个 URL。这样，即便先返回的页面没有可解析的 `<title>`，我们仍能打印有意义的消息。有了这些信息，我们收尾时更新 `println!` 输出，同时标明哪个 URL 先完成，以及该 URL 对应网页的 `<title>`（若有）。

　　你现在已经做出了一个可工作的小爬虫！挑几个 URL 运行这个命令行工具。你可能会发现有些站点一贯更快，而另一些情况下更快的站点每次运行都会变。更重要的是，你已经学会了使用 Future 的基础，现在可以更深入地探索我们能用 async 做什么。

[impl-trait]: ../../generics/02-traits/#traits-as-parameters
[iterators-lazy]: ../../functional-features/02-iterators/
[thread-spawn]: ../../concurrency/01-threads/#creating-a-new-thread-with-spawn
[cli-args]: ../../an-io-project/01-accepting-command-line-arguments/


[crate-source]: https://github.com/rust-lang/book/tree/main/packages/trpl
[futures-crate]: https://crates.io/crates/futures
[tokio]: https://tokio.rs
