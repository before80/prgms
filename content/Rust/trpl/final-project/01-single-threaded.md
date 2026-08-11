+++
title = "21.1 构建单线程 Web 服务器"
date = 2026-08-05T08:44:00+08:00
weight = 101
type = "docs"
description = "用 TCP 与 HTTP 构建单线程 Web 服务器"
isCJKLanguage = true
draft = false
rust_version = "1.97.1"

+++

> 译文 · 基于 [The Rust Programming Language](https://doc.rust-lang.org/stable/book/)（rustc 1.97.1）

# 构建单线程 Web 服务器 {#web}


> 原文链接: [https://doc.rust-lang.org/stable/book/ch21-01-single-threaded.html](https://doc.rust-lang.org/stable/book/ch21-01-single-threaded.html)


## 构建单线程 Web 服务器

　　我们先让单线程 Web 服务器跑起来。动手之前，先快速看一眼构建 Web 服务器会涉及的协议。这些协议的细节超出本书范围，但简要概述能给你所需的信息。

　　Web 服务器涉及的两个主要协议是 *超文本传输协议*（*HTTP*）和 *传输控制协议*（*TCP*）。二者都是 *请求–响应* 协议，意思是 *客户端* 发起请求，*服务器* 监听请求并向客户端提供响应。请求与响应的内容由协议定义。

　　TCP 是较低层的协议，描述信息如何从一台服务器传到另一台，但不规定信息是什么。HTTP 建立在 TCP 之上，定义请求与响应的内容。技术上也可以把 HTTP 用在其他协议上，但绝大多数情况下，HTTP 通过 TCP 发送数据。我们将直接处理 TCP 与 HTTP 请求和响应的原始字节。

### 监听 TCP 连接

　　Web 服务器需要监听 TCP 连接，所以我们先做这部分。标准库提供了 `std::net` 模块来完成这件事。按通常方式新建一个项目：

```console
$ cargo new hello
     Created binary (application) `hello` project
$ cd hello
```

　　现在把示例 21-1 中的代码写入 *src/main.rs* 开始。这段代码会在本地地址 `127.0.0.1:7878` 监听传入的 TCP 流。收到传入流时，它会打印 `Connection established!`。

**文件名：`src/main.rs`**
```rust
use std::net::TcpListener;

fn main() {
    let listener = TcpListener::bind("127.0.0.1:7878").unwrap();

    for stream in listener.incoming() {
        let stream = stream.unwrap();

        println!("Connection established!");
    }
}
```

**示例 21-1：监听传入的流，并在收到流时打印消息**

　　用 `TcpListener`，我们可以在地址 `127.0.0.1:7878` 监听 TCP 连接。地址中冒号前的部分是表示你的计算机的 IP 地址（每台计算机上都一样，并不特指作者的电脑），`7878` 是端口。我们选这个端口有两个原因：HTTP 通常不在这个端口接受连接，因此我们的服务器不太会与你机器上可能运行的其他 Web 服务器冲突；而且 7878 在电话键盘上正好能敲出 *rust*。

　　在这种场景下，`bind` 函数的作用类似 `new`：它会返回一个新的 `TcpListener` 实例。之所以叫 `bind`，是因为在网络中，连接到某个端口以进行监听被称为「绑定到端口」。

　　`bind` 函数返回 `Result<T, E>`，表明绑定可能失败——例如，如果我们运行了两个本程序实例，就会有两个程序监听同一端口。因为我们只是写一个用于学习的基础服务器，暂不操心这类错误处理；出错时用 `unwrap` 停止程序即可。

　　`TcpListener` 上的 `incoming` 方法返回一个迭代器，依次给出一连串流（更具体地说，是类型为 `TcpStream` 的流）。单个 *流* 表示客户端与服务器之间的一条打开连接。*连接* 指完整的请求与响应过程：客户端连上服务器，服务器生成响应，然后服务器关闭连接。因此，我们会从 `TcpStream` 读取客户端发来的内容，再把响应写入该流以把数据发回客户端。总体而言，这个 `for` 循环会依次处理每个连接，并产生一系列供我们处理的流。

　　目前对流的处理只是调用 `unwrap`：若流有任何错误就终止程序；若没有错误，程序就打印一条消息。下一示例中我们会为成功情况添加更多功能。客户端连上服务器时，`incoming` 方法仍可能返回错误，原因是我们实际上并不是在迭代「连接」，而是在迭代 *连接尝试*。连接可能因多种原因失败，其中许多与操作系统有关。例如，许多操作系统对同时打开的连接数有上限；超过该数量的新连接尝试会产生错误，直到部分打开的连接被关闭。

　　来运行这段代码试试！在终端调用 `cargo run`，然后在浏览器中打开 *127.0.0.1:7878*。浏览器应会显示类似「Connection reset」的错误，因为服务器目前没有发回任何数据。但看终端时，你应能看到浏览器连上服务器时打印的若干条消息！

```text
     Running `target/debug/hello`
Connection established!
Connection established!
Connection established!
```

　　有时一次浏览器请求会打印多条消息；原因可能是浏览器既在请求页面，也在请求其他资源，比如浏览器标签上显示的 *favicon.ico* 图标。

　　也可能是因为服务器没有返回任何数据，浏览器在多次尝试连接。当 `stream` 在循环末尾离开作用域并被丢弃时，连接会作为 `drop` 实现的一部分被关闭。浏览器有时会通过重试来应对关闭的连接，因为问题可能是暂时的。

　　浏览器有时也会在未发送任何请求的情况下打开多条到服务器的连接，以便稍后 *真的* 发送请求时能更快完成。发生这种情况时，我们的服务器会看到每一条连接，无论其上是否有请求。例如许多基于 Chrome 的浏览器会这样做；可以用隐私浏览模式或换用其他浏览器来关闭该优化。

　　重要的是：我们已经成功拿到了 TCP 连接的句柄！

　　跑完某一版代码后，记得按 <kbd>ctrl</kbd>-<kbd>C</kbd> 停止程序。然后在每组代码改动之后再调用 `cargo run` 重启，确保运行的是最新代码。

### 读取请求

　　接下来实现从浏览器读取请求的功能！为了把「先拿到连接」和「再对连接采取行动」分开，我们会新建一个处理连接的函数。在这个新的 `handle_connection` 函数里，我们从 TCP 流读取数据并打印出来，以便查看浏览器发来的数据。把代码改成示例 21-2 的样子。

**文件名：`src/main.rs`**
```rust
use std::{
    io::{BufReader, prelude::*},
    net::{TcpListener, TcpStream},
};

fn main() {
    let listener = TcpListener::bind("127.0.0.1:7878").unwrap();

    for stream in listener.incoming() {
        let stream = stream.unwrap();

        handle_connection(stream);
    }
}

fn handle_connection(mut stream: TcpStream) {
    let buf_reader = BufReader::new(&stream);
    let http_request: Vec<_> = buf_reader
        .lines()
        .map(|result| result.unwrap())
        .take_while(|line| !line.is_empty())
        .collect();

    println!("Request: {http_request:#?}");
}
```

**示例 21-2：从 `TcpStream` 读取数据并打印**

　　我们把 `std::io::BufReader` 和 `std::io::prelude` 引入作用域，以获得读写流所需的特征与类型。在 `main` 函数的 `for` 循环里，我们不再打印「已建立连接」的消息，而是调用新的 `handle_connection` 函数并把 `stream` 传给它。

　　在 `handle_connection` 中，我们创建一个新的 `BufReader` 实例，包装对 `stream` 的引用。`BufReader` 通过替我们管理对 `std::io::Read` 特征方法的调用，来增加缓冲。

　　我们创建名为 `http_request` 的变量，用来收集浏览器发往服务器的请求各行。通过加上 `Vec<_>` 类型标注，表明我们希望把这些行收集到一个向量中。

　　`BufReader` 实现了 `std::io::BufRead` 特征，该特征提供 `lines` 方法。`lines` 方法在看到换行字节时分割数据流，返回 `Result<String, std::io::Error>` 的迭代器。为得到每个 `String`，我们对每个 `Result` 做 `map` 并 `unwrap`。若数据不是有效的 UTF-8，或从流读取时出了问题，`Result` 可能是错误。同样，生产环境程序应更优雅地处理这些错误，但为简单起见，我们选择在出错时停止程序。

　　浏览器通过连续发送两个换行符来表示 HTTP 请求结束，因此要从流中取出一个请求，我们会一直取行，直到得到空字符串那一行为止。把各行收集到向量后，我们用美化调试格式把它们打印出来，以便查看 Web 浏览器发给服务器的指令。

　　来试试这段代码！再启动程序并在浏览器中发一次请求。注意浏览器里仍会看到错误页，但终端中程序的输出现在会类似这样：


```console
$ cargo run
   Compiling hello v0.1.0 (file:///projects/hello)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.42s
     Running `target/debug/hello`
Request: [
    "GET / HTTP/1.1",
    "Host: 127.0.0.1:7878",
    "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:99.0) Gecko/20100101 Firefox/99.0",
    "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language: en-US,en;q=0.5",
    "Accept-Encoding: gzip, deflate, br",
    "DNT: 1",
    "Connection: keep-alive",
    "Upgrade-Insecure-Requests: 1",
    "Sec-Fetch-Dest: document",
    "Sec-Fetch-Mode: navigate",
    "Sec-Fetch-Site: none",
    "Sec-Fetch-User: ?1",
    "Cache-Control: max-age=0",
]
```

　　取决于浏览器，输出可能略有不同。既然已经在打印请求数据，就可以通过看请求第一行 `GET` 后面的路径，弄清为什么一次浏览器请求会产生多条连接。若重复连接都在请求 */*，就知道浏览器因为没有从我们的程序得到响应，而在反复抓取 */*。

　　接下来拆解这些请求数据，弄清浏览器在向我们的程序要什么。

### 更仔细地看 HTTP 请求

　　HTTP 是基于文本的协议，请求采用这种格式：

```text
Method Request-URI HTTP-Version CRLF
headers CRLF
message-body
```

　　第一行是 *请求行*，保存客户端在请求什么的信息。请求行的第一部分表示所用方法，例如 `GET` 或 `POST`，描述客户端如何发起这次请求。我们的客户端用了 `GET` 请求，表示它在请求信息。

　　请求行的下一部分是 */*，表示客户端请求的 *统一资源标识符*（*URI*）：URI 与 *统一资源定位符*（*URL*）几乎相同，但不完全一样。URI 与 URL 的区别对本章目的并不重要，但 HTTP 规范使用术语 *URI*，因此这里你可以在脑中把 *URI* 换成 *URL*。

　　最后一部分是客户端使用的 HTTP 版本，然后请求行以 CRLF 序列结束。（*CRLF* 代表 *回车* 与 *换行*，是打字机时代的说法！）CRLF 序列也可以写成 `\r\n`，其中 `\r` 是回车，`\n` 是换行。*CRLF 序列* 把请求行与其余请求数据分开。注意打印 CRLF 时，我们看到的是新的一行开始，而不是 `\r\n`。

　　看目前运行程序收到的请求行数据：`GET` 是方法，*/* 是请求 URI，`HTTP/1.1` 是版本。

　　请求行之后，从 `Host:` 开始的其余各行是头部。`GET` 请求没有正文。

　　试着换一个浏览器发请求，或请求不同地址（例如 *127.0.0.1:7878/test*），看看请求数据如何变化。

　　既然知道了浏览器在要什么，就来发回一些数据吧！

### 写入响应

　　接下来实现响应客户端请求并发送数据。响应采用如下格式：

```text
HTTP-Version Status-Code Reason-Phrase CRLF
headers CRLF
message-body
```

　　第一行是 *状态行*，包含响应所用的 HTTP 版本、概括请求结果的数字状态码，以及对状态码的文字描述（原因短语）。CRLF 序列之后是任意头部，再一个 CRLF 序列，然后是响应正文。

　　下面是一个示例响应：使用 HTTP 1.1，状态码 200，原因短语 OK，没有头部，也没有正文：

```text
HTTP/1.1 200 OK\r\n\r\n
```

　　状态码 200 是标准的成功响应。这段文本是一个极小的成功 HTTP 响应。让我们把它写入流，作为对成功请求的响应！从 `handle_connection` 函数中删掉打印请求数据的 `println!`，换成示例 21-3 中的代码。

**文件名：`src/main.rs`**
```rust
fn handle_connection(mut stream: TcpStream) {
    let buf_reader = BufReader::new(&stream);
    let http_request: Vec<_> = buf_reader
        .lines()
        .map(|result| result.unwrap())
        .take_while(|line| !line.is_empty())
        .collect();

    let response = "HTTP/1.1 200 OK\r\n\r\n";

    stream.write_all(response.as_bytes()).unwrap();
}
```

**示例 21-3：向流写入一个极小的成功 HTTP 响应**

　　第一行新代码定义了保存成功消息数据的 `response` 变量。然后对 `response` 调用 `as_bytes`，把字符串数据转成字节。`stream` 上的 `write_all` 方法接受 `&[u8]`，并把这些字节直接发到连接上。因为 `write_all` 操作可能失败，我们像之前一样对任何错误结果使用 `unwrap`。同样，在真实应用中你应在这里加入错误处理。

　　有了这些改动，运行代码并发一次请求。我们不再向终端打印任何数据，因此除了 Cargo 的输出外看不到别的。在浏览器中打开 *127.0.0.1:7878* 时，你应会看到空白页而不是错误。你刚刚手写完成了接收 HTTP 请求并发送响应！

### 返回真正的 HTML

　　接下来实现返回不止空白页的功能。在项目根目录（不是 *src* 目录）新建文件 *hello.html*。你可以输入任意 HTML；示例 21-4 给出了一种可能。

**文件名：`hello.html`**
```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Hello!</title>
  </head>
  <body>
    <h1>Hello!</h1>
    <p>Hi from Rust</p>
  </body>
</html>
```

**示例 21-4：作为响应返回的示例 HTML 文件**

　　这是一个带有标题和一些文本的最小 HTML5 文档。要在收到请求时从服务器返回它，我们按示例 21-5 修改 `handle_connection`：读取 HTML 文件，把它作为正文加入响应并发送。

**文件名：`src/main.rs`**
```rust
use std::{
    fs,
    io::{BufReader, prelude::*},
    net::{TcpListener, TcpStream},
};
// --snip--


fn handle_connection(mut stream: TcpStream) {
    let buf_reader = BufReader::new(&stream);
    let http_request: Vec<_> = buf_reader
        .lines()
        .map(|result| result.unwrap())
        .take_while(|line| !line.is_empty())
        .collect();

    let status_line = "HTTP/1.1 200 OK";
    let contents = fs::read_to_string("hello.html").unwrap();
    let length = contents.len();

    let response =
        format!("{status_line}\r\nContent-Length: {length}\r\n\r\n{contents}");

    stream.write_all(response.as_bytes()).unwrap();
}
```

**示例 21-5：把 *hello.html* 的内容作为响应正文发送**

　　我们在 `use` 语句中加入了 `fs`，以把标准库的文件系统模块引入作用域。把文件内容读成字符串的代码应看起来很眼熟；在 I/O 项目的示例 12-4 中读文件内容时我们就用过。

　　接下来用 `format!` 把文件内容作为成功响应的正文。为确保 HTTP 响应有效，我们加入 `Content-Length` 头部，其值设为响应正文的大小——这里就是 `hello.html` 的大小。

　　用 `cargo run` 运行这段代码，并在浏览器中打开 *127.0.0.1:7878*；你应能看到渲染后的 HTML！

　　目前我们忽略了 `http_request` 中的请求数据，无条件地发回 HTML 文件内容。这意味着若你在浏览器中请求 *127.0.0.1:7878/something-else*，仍会得到同一份 HTML 响应。此刻我们的服务器非常有限，并不像多数 Web 服务器那样工作。我们希望按请求定制响应，并且只在对 */* 的格式正确的请求时才发回 HTML 文件。

### 校验请求并有选择地响应

　　眼下无论客户端请求什么，我们的 Web 服务器都会返回文件中的 HTML。让我们加上功能：在返回 HTML 文件之前检查浏览器是否在请求 */*，若请求其他内容则返回错误。为此需要按示例 21-6 修改 `handle_connection`。这段新代码把收到的请求内容与我们所知的对 */* 的请求进行比对，并用 `if` 与 `else` 块区别处理请求。

**文件名：`src/main.rs`**
```rust
// --snip--

fn handle_connection(mut stream: TcpStream) {
    let buf_reader = BufReader::new(&stream);
    let request_line = buf_reader.lines().next().unwrap().unwrap();

    if request_line == "GET / HTTP/1.1" {
        let status_line = "HTTP/1.1 200 OK";
        let contents = fs::read_to_string("hello.html").unwrap();
        let length = contents.len();

        let response = format!(
            "{status_line}\r\nContent-Length: {length}\r\n\r\n{contents}"
        );

        stream.write_all(response.as_bytes()).unwrap();
    } else {
        // some other request
    }
}
```

**示例 21-6：对 */* 的请求与其他请求区别处理**

　　我们只会查看 HTTP 请求的第一行，因此不再把整个请求读入向量，而是调用 `next` 从迭代器取第一项。第一个 `unwrap` 处理 `Option`，若迭代器没有项就停止程序。第二个 `unwrap` 处理 `Result`，效果与示例 21-2 中加在 `map` 里的 `unwrap` 相同。

　　接下来检查 `request_line` 是否等于对 */* 路径的 GET 请求行。若是，`if` 块就返回我们的 HTML 文件内容。

　　若 `request_line` *不* 等于对 */* 路径的 GET 请求，说明我们收到了其他请求。稍后会在 `else` 块中加入代码以响应所有其他请求。

　　现在运行这段代码并请求 *127.0.0.1:7878*；你应得到 *hello.html* 中的 HTML。若发起任何其他请求，例如 *127.0.0.1:7878/something-else*，你会得到与运行示例 21-1 和示例 21-2 时类似的连接错误。

　　现在把示例 21-7 的代码加入 `else` 块，返回状态码为 404 的响应，表示未找到请求的内容。我们还会返回一些 HTML，以便在浏览器中渲染页面，把响应告知最终用户。

**文件名：`src/main.rs`**
```rust
    // --snip--
    } else {
        let status_line = "HTTP/1.1 404 NOT FOUND";
        let contents = fs::read_to_string("404.html").unwrap();
        let length = contents.len();

        let response = format!(
            "{status_line}\r\nContent-Length: {length}\r\n\r\n{contents}"
        );

        stream.write_all(response.as_bytes()).unwrap();
    }
```

**示例 21-7：若请求的不是 */*，则用状态码 404 与错误页响应**

　　这里，响应的状态行带有状态码 404 和原因短语 `NOT FOUND`。响应正文是文件 *404.html* 中的 HTML。你需要在 *hello.html* 旁边创建 *404.html* 作为错误页；同样可以用任意 HTML，或使用示例 21-8 中的示例 HTML。

**文件名：`404.html`**
```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Hello!</title>
  </head>
  <body>
    <h1>Oops!</h1>
    <p>Sorry, I don't know what you're asking for.</p>
  </body>
</html>
```

**示例 21-8：随任意 404 响应发回的页面示例内容**

　　有了这些改动，再次运行服务器。请求 *127.0.0.1:7878* 应返回 *hello.html* 的内容；任何其他请求（如 *127.0.0.1:7878/foo*）应返回 *404.html* 中的错误 HTML。

### 重构

　　目前 `if` 与 `else` 块有很多重复：二者都在读文件，并把文件内容写入流。唯一差别是状态行与文件名。我们可以通过把这些差别抽到单独的 `if` 与 `else` 行中，把状态行和文件名赋给变量，从而让代码更简洁；然后在读文件和写响应的代码里无条件地使用这些变量。示例 21-9 展示了替换掉大块 `if` 与 `else` 之后的结果。

**文件名：`src/main.rs`**
```rust
// --snip--

fn handle_connection(mut stream: TcpStream) {
    // --snip--

    let (status_line, filename) = if request_line == "GET / HTTP/1.1" {
        ("HTTP/1.1 200 OK", "hello.html")
    } else {
        ("HTTP/1.1 404 NOT FOUND", "404.html")
    };

    let contents = fs::read_to_string(filename).unwrap();
    let length = contents.len();

    let response =
        format!("{status_line}\r\nContent-Length: {length}\r\n\r\n{contents}");

    stream.write_all(response.as_bytes()).unwrap();
}
```

**示例 21-9：重构 `if` 与 `else` 块，使其只包含两种情况之间有差异的代码**

　　现在 `if` 与 `else` 块只在一个元组中返回状态行与文件名的合适值；然后我们用解构，在 `let` 语句的模式中把这两个值赋给 `status_line` 和 `filename`，正如第 19 章所讨论的。

　　原先重复的代码现在位于 `if` 与 `else` 块之外，并使用 `status_line` 与 `filename` 变量。这样更容易看出两种情况的差别，也意味着若要改读写文件与写响应的方式，只需改一处。示例 21-9 中的代码行为与示例 21-7 相同。

　　太好了！我们现在用大约 40 行 Rust 代码就有了一个简单的 Web 服务器：对一种请求返回内容页，对其余请求返回 404 响应。

　　目前服务器在单线程中运行，意味着一次只能服务一个请求。我们先通过模拟一些慢请求来看看这会带来什么问题，然后再修好它，让服务器能同时处理多个请求。
