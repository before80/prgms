+++
title = "50-TCP/UDP 与套接字"
date = 2026-07-28T14:49:00+08:00
weight = 500
type = "docs"
description = "面向 Go 用户讲清 std::net / tokio::net 的 TCP UDP、超时半关闭与并发 accept"
isCJKLanguage = true
draft = false

+++

# TCP / UDP 与套接字 (TCP, UDP and Sockets)

> 面向 **Rust 1.97.1** (stable, 2026-07)。本篇假设你熟悉 Go，凡有可比性处均给出 🐹 Go 对比。
>
> 热度: `hot` 高频 | `common` 常见 | `occasional` 偶尔 | `advanced` 进阶少见

**本篇能解决什么：**
- 你是否习惯 `net.Listen` / `net.Dial`，一进 Rust 就找「标准库 HTTP」，却忘了先会套接字？
- 你是否分不清 `TcpListener` / `TcpStream` / `UdpSocket`，以及阻塞 `std::net` 和 `tokio::net` 怎么选？
- 你是否想设读超时、半关闭、缓冲读写，却对不上 Go 的 `SetDeadline` / `CloseWrite`？
- 你是否写并发 accept 循环时不知道该 `thread::spawn` 还是 `tokio::spawn`？
- 你是否疑惑：TLS / HTTP 该接在哪一层，还是直接上 axum？

**术语速查表：**
| 术语 / 缩略词 | 全称 / 读法 | 中文 | 一句话解释 | Go 里的近亲 |
|---|---|---|---|---|
| socket | — | 套接字 | 进程与网络端点之间的通信句柄 | `net.Conn` / `PacketConn` |
| TCP | Transmission Control Protocol | 传输控制协议 | 面向连接、可靠字节流 | `net.TCP*` |
| UDP | User Datagram Protocol | 用户数据报协议 | 无连接、按报文收发 | `net.UDP*` |
| `TcpListener` | — | TCP 监听器 | `bind` + `accept` 接连接 | `net.Listener` |
| `TcpStream` | — | TCP 流 | 已连接的双向字节流 | `net.TCPConn` / `Conn` |
| `UdpSocket` | — | UDP 套接字 | 收发数据报 | `net.UDPConn` |
| backlog | — | 积压队列 | 尚未 `accept` 的半连接/全连接队列深度 | `Listen` 的 backlog |
| deadline / timeout | — | 截止时间 / 超时 | 读写在时限内必须完成 | `SetDeadline` / `SetReadDeadline` |
| half-close | — | 半关闭 | 只关写或只关读，另一方向仍可通 | `CloseWrite` / `CloseRead` |
| `ToSocketAddrs` | — | 地址解析 trait | 主机名/端口 → 一组 `SocketAddr` | `net.Resolve*` / `Dial` 内部解析 |
| `tokio::net` | — | Tokio 网络模块 | 异步非阻塞套接字 | 自研 async 或 `net` + goroutine |
| TLS | Transport Layer Security | 传输层安全 | 在 TCP 上加密；常经 rustls 等 | `crypto/tls` |
| SO_REUSEADDR | — | 地址复用选项 | 允许快速重绑同一本地地址 | `SO_REUSEADDR` |

> 说明：本表覆盖本篇出现的所有专业名词与缩略词；正文首次出现时仍会就地解释一次。

**热度索引：**
| 热度 | 题目 |
|------|------|
| `hot` | [Q1](#q1), [Q2](#q2), [Q3](#q3), [Q4](#q4), [Q6](#q6), [Q7](#q7), [Q10](#q10) |
| `common` | [Q5](#q5), [Q8](#q8), [Q9](#q9), [Q11](#q11), [Q12](#q12) |
| `occasional` | — |
| `advanced` | — |

---

## Q1. Rust 的 TCP 监听/连接对应 Go 的哪几个 API？ {#q1}
**Tags:** `hot` `beginner` `TcpListener` `TcpStream` `std::net`
**适用版本:** Rust 1.0+（`std::net`）

**一句话答案：**
`TcpListener::bind` ≈ `net.Listen("tcp", ...)`；`listener.accept()` ≈ `Accept`；`TcpStream::connect` ≈ `net.Dial("tcp", ...)`。类型上监听器与已连接流分开，读写走 `Read`/`Write` trait。

**解答：**
最小服务端：

```rust
use std::io::{Read, Write};
use std::net::TcpListener;

fn main() -> std::io::Result<()> {
    let listener = TcpListener::bind("127.0.0.1:0")?; // 0 = 系统分配端口
    let addr = listener.local_addr()?;
    println!("listening on {addr}");

    // 演示用：只接一条连接
    let (mut stream, peer) = listener.accept()?;
    println!("accepted {peer}");
    let mut buf = [0u8; 64];
    let n = stream.read(&mut buf)?;
    stream.write_all(b"ok\n")?;
    println!("got {} bytes", n);
    Ok(())
}
```

最小客户端：

```rust
use std::io::{Read, Write};
use std::net::TcpStream;

fn main() -> std::io::Result<()> {
    // 把地址换成上面打印的 listening 地址再跑
    let mut stream = TcpStream::connect("127.0.0.1:8080")?;
    stream.write_all(b"hi\n")?;
    let mut buf = [0u8; 64];
    let n = stream.read(&mut buf)?;
    println!("{}", String::from_utf8_lossy(&buf[..n]));
    Ok(())
}
```

对照表：

| Go | Rust (`std::net`) |
|----|-------------------|
| `Listen("tcp", addr)` | `TcpListener::bind(addr)` |
| `Accept()` | `listener.accept()` → `(TcpStream, SocketAddr)` |
| `Dial("tcp", addr)` | `TcpStream::connect(addr)` |
| `conn.Read` / `Write` | `Read` / `Write`（或 `read`/`write_all`） |

**Go 对比：**
```go
ln, _ := net.Listen("tcp", "127.0.0.1:0")
conn, _ := ln.Accept()
```
- **Go 怎么做**：`Listener` + `Conn` 接口，HTTP 建在其上。
- **Rust 为什么不同**：具体类型 `TcpListener`/`TcpStream`，HTTP 在 crates（见 [40-http](../40-http-client-and-server/)）。
- **Go 程序员易踩的坑**：以为 std 里有 `http.ListenAndServe`——没有；先会 TCP，再上框架。

**记忆点：**
- `bind` / `accept` / `connect` 三件套。
- 字节流用 `Read`/`Write`，不是方法名 `Read`/`Write` 钉死在类型上。

---

## Q2. `accept` 返回什么？循环怎么写才像 Go？ {#q2}
**Tags:** `hot` `accept` `loop` `beginner`
**适用版本:** Rust 1.0+

**一句话答案：**
`accept()` → `io::Result<(TcpStream, SocketAddr)>`。常见写法是 `for stream in listener.incoming()`，或 `loop { let (stream, addr) = listener.accept()?; ... }`；每条连接再开线程/`spawn` 处理。

**解答：**
`incoming()` 迭代器版（阻塞）：

```rust
use std::io::Write;
use std::net::TcpListener;

fn main() -> std::io::Result<()> {
    let listener = TcpListener::bind("127.0.0.1:0")?;
    println!("on {}", listener.local_addr()?);

    for conn in listener.incoming() {
        let mut stream = conn?;
        // 生产里通常 thread::spawn / 线程池 / async spawn
        stream.write_all(b"hello\n")?;
    }
    Ok(())
}
```

显式 `loop` + 对端地址：

```rust
use std::net::TcpListener;

fn main() -> std::io::Result<()> {
    let listener = TcpListener::bind("127.0.0.1:0")?;
    loop {
        let (stream, peer) = listener.accept()?;
        println!("peer={peer} local={}", stream.local_addr()?);
        drop(stream); // 演示：立刻关
    }
}
```

「❌ 错误写法」——在单线程里对每条连接做超长阻塞业务，又不 `spawn`：新连接全堵在 `accept` 前的处理里。

**Go 对比：**
```go
for {
    conn, err := ln.Accept()
    go handle(conn)
}
```
- **Go 怎么做**：`Accept` + `go handle`。
- **Rust 为什么不同**：同样模式，但要用 `thread::spawn` 或 async（见 [Q7](#q7)、[29-concurrency](../29-concurrency-and-threads/)）。
- **Go 程序员易踩的坑**：忘了处理 `accept`/`incoming` 的 `Err`（临时错误有时应 continue）。

**记忆点：**
- `incoming()` ≈ 无限 `Accept` 迭代。
- 一连接一任务：线程或 `tokio::spawn`。

---

## Q3. UDP 怎么收发？和 TCP 差在哪？ {#q3}
**Tags:** `hot` `UdpSocket` `datagram`
**适用版本:** Rust 1.0+

**一句话答案：**
`UdpSocket::bind` 后用 `send_to` / `recv_from`（或 `connect` 后再 `send`/`recv`）。UDP 是报文、无连接保证；TCP 是字节流、要自己定帧。

**解答：**
```rust
use std::net::UdpSocket;

fn main() -> std::io::Result<()> {
    let sock = UdpSocket::bind("127.0.0.1:0")?;
    let local = sock.local_addr()?;

    // 自发自收演示（真实场景对端是另一个进程）
    sock.send_to(b"ping", local)?;
    let mut buf = [0u8; 64];
    let (n, from) = sock.recv_from(&mut buf)?;
    assert_eq!(&buf[..n], b"ping");
    println!("from={from}");
    Ok(())
}
```

`connect` 后可省略每次对端地址（仍是 UDP 语义）：

```rust
use std::net::UdpSocket;

fn main() -> std::io::Result<()> {
    let sock = UdpSocket::bind("127.0.0.1:0")?;
    let peer = sock.local_addr()?; // 演示：连到自己
    sock.connect(peer)?;
    sock.send(b"pong")?;
    let mut buf = [0u8; 8];
    let n = sock.recv(&mut buf)?;
    assert_eq!(&buf[..n], b"pong");
    Ok(())
}
```

| | TCP | UDP |
|--|-----|-----|
| 类型 | `TcpStream` | `UdpSocket` |
| 单位 | 字节流 | 数据报 |
| 可靠性 | 有序可靠（协议层） | 可能丢、乱序、重复 |
| 常见坑 | 粘包要定帧 | 一次 `recv` 一包，缓冲不够可能截断 |

**Go 对比：**
```go
c, _ := net.ListenUDP("udp", addr)
c.ReadFromUDP(buf)
c.WriteToUDP(p, addr)
```
- **Go 怎么做**：`UDPConn` + `ReadFrom`/`WriteTo`。
- **Rust 为什么不同**：API 名不同，心智几乎一样。
- **Go 程序员易踩的坑**：把 TCP 的「读到 Eof 结束消息」照搬到 UDP。

**记忆点：**
- UDP：`send_to` / `recv_from`。
- 别用 TCP 粘包思路硬套 UDP。

---

## Q4. 读超时 / 写超时怎么设？（对标 `SetDeadline`） {#q4}
**Tags:** `hot` `timeout` `set_read_timeout` `deadline`
**适用版本:** Rust 1.0+（`std::net` 超时 API）

**一句话答案：**
`TcpStream` / `UdpSocket` 上用 `set_read_timeout` / `set_write_timeout(Some(Duration))`；超时表现为 `io::ErrorKind::TimedOut`（或 `WouldBlock`，视平台/模式）。这是 **std 阻塞套接字** 的做法；async 用 `tokio::time::timeout` 包 `.await`（见 [31-async Q16](../31-async-programming/#q16)）。

**解答：**
```rust
use std::io::{self, Read};
use std::net::{TcpListener, TcpStream};
use std::time::Duration;

fn main() -> io::Result<()> {
    let listener = TcpListener::bind("127.0.0.1:0")?;
    let addr = listener.local_addr()?;

    let mut client = TcpStream::connect(addr)?;
    client.set_read_timeout(Some(Duration::from_millis(50)))?;

    // 服务端故意不写：客户端读应超时
    let (_server, _) = listener.accept()?;
    let mut buf = [0u8; 8];
    match client.read(&mut buf) {
        Err(e) if e.kind() == io::ErrorKind::TimedOut
            || e.kind() == io::ErrorKind::WouldBlock => {
            println!("timeout ok: {e}");
        }
        other => panic!("expected timeout, got {other:?}"),
    }
    Ok(())
}
```

清超时：`set_read_timeout(None)`。

「❌ 错误写法」——在 `#[tokio::main]` 里对 `std::net::TcpStream` 做长时间阻塞读：拖死 worker（见 [Q7](#q7)）。

**Go 对比：**
```go
conn.SetReadDeadline(time.Now().Add(50 * time.Millisecond))
```
- **Go 怎么做**：绝对时间 deadline；可 `SetDeadline` 同时管读写。
- **Rust 为什么不同**：std 给相对 **Duration** 超时；async 另有 `timeout` 包装。
- **Go 程序员易踩的坑**：找 `SetDeadline` 同名方法——名字是 `set_*_timeout`。

**记忆点：**
- 阻塞套接字 → `set_read_timeout`。
- async 套接字 → `tokio::time::timeout`，别混用。

---

## Q5. 为什么 TCP 读要自己定帧？`BufReader` 有什么用？ {#q5}
**Tags:** `common` `framing` `BufReader` `粘包`
**适用版本:** Rust 1.0+

**一句话答案：**
TCP 是字节流：一次 `read` 可能半条消息或多条粘在一起。应用层要定帧（长度前缀、分隔符、HTTP 等）。`BufReader` 减少系统调用、方便 `read_until` / `read_line`，但**不替你定义消息边界语义**。

**解答：**
按行读（简单定帧）：

```rust
use std::io::{BufRead, BufReader, Write};
use std::net::{TcpListener, TcpStream};

fn main() -> std::io::Result<()> {
    let listener = TcpListener::bind("127.0.0.1:0")?;
    let addr = listener.local_addr()?;

    let mut client = TcpStream::connect(addr)?;
    client.write_all(b"hello\n")?;

    let (server, _) = listener.accept()?;
    let mut reader = BufReader::new(server);
    let mut line = String::new();
    reader.read_line(&mut line)?;
    assert_eq!(line, "hello\n");
    Ok(())
}
```

长度前缀直觉（示意）：

```rust
fn main() {
    // 应用层常见帧：[u32 BE 长度][payload]
    let payload = b"hi";
    let mut frame = Vec::new();
    frame.extend_from_slice(&(payload.len() as u32).to_be_bytes());
    frame.extend_from_slice(payload);
    assert_eq!(&frame[4..], b"hi");
}
```

**Go 对比：**
- **Go 怎么做**：同样要 `bufio` + 自定协议；HTTP 由 `net/http` 定帧。
- **Rust 为什么不同**：一样；HTTP 交给 hyper/axum（[40-http](../40-http-client-and-server/)）。
- **Go 程序员易踩的坑**：以为一次 `read` = 一次业务消息。

**记忆点：**
- 流 ≠ 消息；先定帧再解析。
- `BufReader` 是缓冲，不是协议。

---

## Q6. 主机名怎么解析？`ToSocketAddrs` 是什么？ {#q6}
**Tags:** `hot` `DNS` `ToSocketAddrs` `SocketAddr`
**适用版本:** Rust 1.0+

**一句话答案：**
`"host:port"` 字符串常通过 **`ToSocketAddrs`**（可转为套接字地址列表的 trait）解析成多个 `SocketAddr`；`connect`/`bind` 很多重载内部会用它。多地址时 `connect` 通常试到成功或全部失败。

**解答：**
```rust
use std::net::{SocketAddr, ToSocketAddrs};

fn main() -> std::io::Result<()> {
    let addrs: Vec<SocketAddr> = "localhost:80".to_socket_addrs()?.collect();
    assert!(!addrs.is_empty());
    for a in &addrs {
        println!("{a}"); // 可能有 IPv4 / IPv6 多条
    }
    Ok(())
}
```

直接使用 `SocketAddr`，跳过解析：

```rust
use std::net::{IpAddr, Ipv4Addr, SocketAddr, TcpListener};

fn main() -> std::io::Result<()> {
    let addr = SocketAddr::new(IpAddr::V4(Ipv4Addr::LOCALHOST), 0);
    let listener = TcpListener::bind(addr)?;
    println!("{}", listener.local_addr()?);
    Ok(())
}
```

**Go 对比：**
```go
net.ResolveTCPAddr("tcp", "localhost:80")
net.Dial("tcp", "localhost:80") // 内部解析
```
- **Go 怎么做**：`Resolve*` 或 Dial 内嵌解析。
- **Rust 为什么不同**：`ToSocketAddrs` 是统一入口；注意解析可能阻塞（DNS）。
- **Go 程序员易踩的坑**：在 async 里同步解析主机名阻塞 runtime——生产常用 async DNS 或先解析再连。

**记忆点：**
- 字符串地址 → `to_socket_addrs()`。
- 已有 IP → 构造 `SocketAddr` 更直接。

---

## Q7. 什么时候用 `std::net`，什么时候用 `tokio::net`？ {#q7}
**Tags:** `hot` `tokio` `async` `blocking`
**适用版本:** `std::net` 始终可用；`tokio::net` 需 Tokio

**一句话答案：**
短工具、同步脚本、教学 → `std::net`（阻塞）。高并发服务、已在 Tokio 上 → **`tokio::net`**（`TcpListener`/`TcpStream` 的异步版）。切忌在 async 任务里直接阻塞 `std::net` 读写。

**解答：**
选型：

| 场景 | 选择 |
|------|------|
| CLI 探活、一次性 Dial | `std::net` |
| 大量连接、与 axum/reqwest 同进程 | `tokio::net` |
| 偶尔阻塞 DNS/文件 | `spawn_blocking`（见 [31-async Q9](../31-async-programming/#q9)） |

Tokio 侧形状（text，需依赖）：

```text
use tokio::net::TcpListener;
use tokio::io::{AsyncReadExt, AsyncWriteExt};

#[tokio::main]
async fn main() -> std::io::Result<()> {
    let listener = TcpListener::bind("127.0.0.1:0").await?;
    let (mut socket, _) = listener.accept().await?;
    socket.write_all(b"hi\n").await?;
    Ok(())
}
```

```toml
[dependencies]
tokio = { version = "1", features = ["rt-multi-thread", "macros", "net", "io-util"] }
```

**Go 对比：**
- **Go 怎么做**：goroutine + 阻塞 `net` 是默认；网络多路复用在 runtime。
- **Rust 为什么不同**：阻塞与 async 两套类型；混用要自觉。
- **Go 程序员易踩的坑**：把 Go 的「到处 Dial」原样塞进 `async fn`。

**记忆点：**
- async 服务 → `tokio::net` + `.await`。
- 阻塞 `std::net` 别拖死 Tokio worker。

---

## Q8. 半关闭 `shutdown` 怎么用？（对标 `CloseWrite`） {#q8}
**Tags:** `common` `shutdown` `half-close`
**适用版本:** Rust 1.0+

**一句话答案：**
`TcpStream::shutdown(Shutdown::Write)` 表示「我写完了」，对端读到 EOF，但本端仍可读；`Read` / `Both` 同理。用来做请求-响应里「客户端发完再读」的收尾。

**解答：**
```rust
use std::io::{Read, Write};
use std::net::{Shutdown, TcpListener, TcpStream};

fn main() -> std::io::Result<()> {
    let listener = TcpListener::bind("127.0.0.1:0")?;
    let addr = listener.local_addr()?;

    let mut client = TcpStream::connect(addr)?;
    let (mut server, _) = listener.accept()?;

    client.write_all(b"req")?;
    client.shutdown(Shutdown::Write)?; // 对标 CloseWrite

    let mut buf = Vec::new();
    server.read_to_end(&mut buf)?; // 读到 EOF
    assert_eq!(buf, b"req");
    server.write_all(b"resp")?;
    Ok(())
}
```

```rust
fn main() {
    use std::net::Shutdown;
    // 三个方向
    let _ = Shutdown::Write;
    let _ = Shutdown::Read;
    let _ = Shutdown::Both;
}
```

**Go 对比：**
```go
conn.(*net.TCPConn).CloseWrite()
```
- **Go 怎么做**：`CloseWrite` / `CloseRead`。
- **Rust 为什么不同**：统一 `shutdown(Shutdown::...)`。
- **Go 程序员易踩的坑**：`drop(stream)` 是全关，不是半关闭。

**记忆点：**
- 只关写 → `Shutdown::Write`。
- `drop` ≠ 半关闭。

---

## Q9. `SO_REUSEADDR` / 端口占用 `AddrInUse` 怎么办？ {#q9}
**Tags:** `common` `reuse` `AddrInUse` `bind`
**适用版本:** 平台相关；`socket2` 等 crate 更灵活

**一句话答案：**
进程刚退出后立刻重绑，常遇 `ErrorKind::AddrInUse`（地址仍在 TIME_WAIT）。开发期可设 **SO_REUSEADDR**（地址复用）；生产要理解语义差异（尤其 Windows）。需要精细控制时用 `socket2` 建套接字再 `bind`。

**解答：**
```rust
use std::io;
use std::net::TcpListener;

fn main() {
    // 演示：同地址绑两次 → 第二次通常 AddrInUse
    let a = TcpListener::bind("127.0.0.1:0").unwrap();
    let addr = a.local_addr().unwrap();
    // 故意再绑「固定端口」才容易复现；0 端口每次不同
    match TcpListener::bind("127.0.0.1:1") {
        Err(e) if e.kind() == io::ErrorKind::PermissionDenied
            || e.kind() == io::ErrorKind::AddrInUse => {
            println!("bind failed as expected-ish: {e}");
        }
        other => println!("other: {other:?}"),
    }
    drop(a);
    let _ = addr;
}
```

工程上（text）：

```text
# 常见做法
# 1) 换端口 / 等 TIME_WAIT
# 2) socket2::Socket::new(...); set_reuse_address(true); bind; listen;
# 3) 容器/编排里用固定 Service 端口 + 滚动发布
```

**Go 对比：**
- **Go 怎么做**：`ListenConfig` / 裸 syscall 设 reuse；同样受 TIME_WAIT 困扰。
- **Rust 为什么不同**：`std` 暴露有限，细控常靠 `socket2`。
- **Go 程序员易踩的坑**：以为 `bind` 失败就是代码写错——可能是端口占用。

**记忆点：**
- `AddrInUse` 先查端口占用与 TIME_WAIT。
- 精细 reuse → `socket2`。

---

## Q10. 并发处理连接的最小正确姿势是什么？ {#q10}
**Tags:** `hot` `concurrency` `thread` `spawn`
**适用版本:** `std::thread`；或 Tokio（见 [Q7](#q7)）

**一句话答案：**
阻塞模型：`accept` 后 `thread::spawn`（或有界线程池）处理该 `TcpStream`；异步模型：`accept().await` 后 `tokio::spawn`。务必设读超时/空闲断开，并限制最大并发，防止被慢连接拖垮。

**解答：**
```rust
use std::io::{Read, Write};
use std::net::TcpListener;
use std::thread;

fn main() -> std::io::Result<()> {
    let listener = TcpListener::bind("127.0.0.1:0")?;
    println!("{}", listener.local_addr()?);

    for conn in listener.incoming() {
        let mut stream = conn?;
        thread::spawn(move || {
            let mut buf = [0u8; 256];
            let _ = stream.read(&mut buf);
            let _ = stream.write_all(b"ok\n");
        });
    }
    Ok(())
}
```

有界并发直觉：

```rust
fn main() {
    // 生产：用信号量 / 线程池 / JoinSet 限制 in-flight 连接数
    // 无界 spawn = 慢客户端可耗尽线程/内存
    let max_in_flight = 256usize;
    assert!(max_in_flight > 0);
}
```

**Go 对比：**
```go
go handle(conn) // 默认很轻；仍要限流
```
- **Go 怎么做**：goroutine 便宜，但仍要超时与限流。
- **Rust 为什么不同**：OS 线程更重；高并发更常 async。
- **Go 程序员易踩的坑**：无界 `thread::spawn` 当 goroutine 用。

**记忆点：**
- 一连接一任务 + 超时 + 有界并发。
- 线程 vs async：见 [Q7](#q7)。

---

## Q11. TLS 和 HTTP 接在哪一层？还要自己写 TCP 吗？ {#q11}
**Tags:** `common` `TLS` `HTTP` `rustls`
**适用版本:** 生态选型；以 crates.io 为准

**一句话答案：**
日常 Web：**别从裸 TCP 手搓 HTTP**——用 **reqwest** / **axum**（内部 hyper + TLS）。只有自定义协议、代理、教学才停在 `TcpStream`；TLS 常见 **rustls**（或 tokio-rustls）包在 TCP 之上。

**解答：**
分层心智：

```text
应用协议 (HTTP/gRPC/自定义)
        ↑
   TLS (可选, rustls…)
        ↑
   TCP (std::net / tokio::net)
```

```toml
# 多数服务直接从这一层开始，而不是手写 TcpListener 解析 HTTP
# axum + tokio；客户端 reqwest（见 40-http）
```

```rust
fn main() {
    // 本篇教会套接字；HTTP 见专题
    println!("TCP 基础 → 40-http / 45-grpc");
}
```

**Go 对比：**
- **Go 怎么做**：`net/http` + `crypto/tls` 一条龙。
- **Rust 为什么不同**：std 停在套接字附近；协议在生态。
- **Go 程序员易踩的坑**：为了「纯 std」手写 HTTP——维护成本远高于 axum。

**记忆点：**
- 自定义协议 → TCP/UDP 本篇。
- HTTP/HTTPS → [40-http](../40-http-client-and-server/)。

---

## Q12. 和 Go `net` 包整表怎么对照？ {#q12}
**Tags:** `common` `cheatsheet` `Go`
**适用版本:** 概念对照；API 随版本微调

**一句话答案：**
把 Go 的 `Listen`/`Dial`/`Read`/`Write`/`SetDeadline`/`CloseWrite` 映射到 Rust 的 `bind`/`connect`/`Read`/`Write`/`set_*_timeout`/`shutdown`；高并发再换成 `tokio::net`。HTTP 不在这张表里。

**解答：**

| Go | Rust |
|----|------|
| `Listen("tcp", a)` | `TcpListener::bind(a)` |
| `Dial("tcp", a)` | `TcpStream::connect(a)` |
| `Accept` | `accept` / `incoming` |
| `Read` / `Write` | `Read` / `Write` traits |
| `SetReadDeadline` | `set_read_timeout` |
| `CloseWrite` | `shutdown(Shutdown::Write)` |
| `ListenUDP` / `ReadFrom` | `UdpSocket::bind` / `recv_from` |
| `ResolveTCPAddr` | `to_socket_addrs` / `SocketAddr` |
| goroutine per conn | `thread::spawn` 或 `tokio::spawn` |
| `http.ListenAndServe` | axum / hyper（非 std） |

```rust
use std::net::{TcpListener, TcpStream, UdpSocket};

fn main() -> std::io::Result<()> {
    // 只为确认三个类型在 std 里都在：真实端口按需替换
    let _ln = TcpListener::bind("127.0.0.1:0")?;
    let _udp = UdpSocket::bind("127.0.0.1:0")?;
    let _ = std::any::type_name::<TcpStream>();
    Ok(())
}
```

**Go 对比：**
- 概念几乎一一对应；名字与错误类型（`io::Result`）要改口。
- 最大工程差异：HTTP/TLS 默认不在 std。

**记忆点：**
- 先会 `std::net`，再按负载选 Tokio。
- 查 HTTP 去 [40](../40-http-client-and-server/)，查 async 去 [31](../31-async-programming/)。
