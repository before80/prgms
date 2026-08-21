+++
title = "13-简便的文档初始化"
date = 2026-08-18T22:10:00+08:00
weight = 20
type = "docs"
description = "简便的文档初始化 — Rust Design Patterns"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Rust Design Patterns](https://rust-unofficial.github.io/patterns/)

> 原文链接: [https://rust-unofficial.github.io/patterns/idioms/rustdoc-init.html](https://rust-unofficial.github.io/patterns/idioms/rustdoc-init.html)

# 简便的文档初始化

## 描述 {#description}

如果在写文档时初始化某个结构体很费功夫，用一个以该结构体为参数的辅助函数把示例包起来会更快。

## 动机 {#motivation}

有时结构体带有多个或复杂的参数，以及若干方法。这些方法各自都应当有示例。

例如：

````rust,ignore
struct Connection {
    name: String,
    stream: TcpStream,
}

impl Connection {
    /// 通过该连接发送请求。
    ///
    /// # 示例
    /// ```no_run
    /// # // 需要样板代码才能让示例跑起来。
    /// # let stream = TcpStream::connect("127.0.0.1:34254");
    /// # let connection = Connection { name: "foo".to_owned(), stream };
    /// # let request = Request::new("RequestId", RequestType::Get, "payload");
    /// let response = connection.send_request(request);
    /// assert!(response.is_ok());
    /// ```
    fn send_request(&self, request: Request) -> Result<Status, SendErr> {
        // ...
    }

    /// 糟糕，所有这些样板代码都得在这里再写一遍！
    fn check_status(&self) -> Status {
        // ...
    }
}
````

## 示例 {#example}

与其敲下所有这些样板代码来创建 `Connection` 和
`Request`，不如写一个包装辅助函数，把它们作为参数传入，这样更轻松：

````rust,ignore
struct Connection {
    name: String,
    stream: TcpStream,
}

impl Connection {
    /// 通过该连接发送请求。
    ///
    /// # 示例
    /// ```
    /// # fn call_send(connection: Connection, request: Request) {
    /// let response = connection.send_request(request);
    /// assert!(response.is_ok());
    /// # }
    /// ```
    fn send_request(&self, request: Request) -> Result<Status, SendErr> {
        // ...
    }
}
````

**注意**：在上面的示例中，`assert!(response.is_ok());` 这一行在测试时实际上不会运行，因为它位于一个从未被调用的函数内部。

## 优点 {#advantages}

这样简洁得多，并且避免了示例中的重复代码。

## 缺点 {#disadvantages}

由于示例位于函数中，这段代码不会被实际测试。不过在运行 `cargo test` 时仍会检查它能否编译。因此，当你需要 `no_run` 时，这一模式最有用。有了它，你就不必再加 `no_run`。

## 讨论 {#discussion}

如果不需要断言，这一模式效果很好。

如果需要断言，一种替代做法是创建一个用于构造辅助实例的公开方法，并用 `#[doc(hidden)]` 标注（这样用户看不到它）。然后该方法可以在 rustdoc 中调用，因为它是 crate 公开 API 的一部分。
