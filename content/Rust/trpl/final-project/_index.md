+++
title = "第21章 最终项目：构建多线程 Web 服务器"
date = 2026-08-05T08:44:00+08:00
weight = 100
type = "docs"
description = "用线程池构建能说 Hello 的多线程 Web 服务器"
isCJKLanguage = true
draft = false
rust_version = "1.97.1"

+++

> 译文 · 基于 [The Rust Programming Language](https://doc.rust-lang.org/stable/book/)（rustc 1.97.1）

# 最终项目：构建多线程 Web 服务器 {#final-project-building-a-multithreaded-web-server}


> 原文链接: [https://doc.rust-lang.org/stable/book/ch21-00-final-project-a-web-server.html](https://doc.rust-lang.org/stable/book/ch21-00-final-project-a-web-server.html)


　　漫长的旅程即将结束——我们到了本书的最后一章。这一章里，我们会再一起做一个项目，演示前面几章讲过的概念，并回顾一些更早的知识点。

　　最终项目是一个会说 “Hello!” 的 Web 服务器；在浏览器里打开时，效果如图 21-1。

　　构建这台服务器的计划如下：

1. 先了解一点 TCP 与 HTTP。
2. 在套接字上监听 TCP 连接。
3. 解析少量 HTTP 请求。
4. 构造规范的 HTTP 响应。
5. 用线程池提升服务器吞吐量。

<img alt="浏览器访问 127.0.0.1:8080，页面显示 “Hello! Hi from Rust”" src="img/trpl21-01.png" class="center" style="width: 50%;" />

<span class="caption">图 21-1：我们的最终合作项目</span>

　　动手之前有两点说明。第一，我们这里用的方法并不是用 Rust 做 Web 服务器的最佳实践。社区已经在 [crates.io](https://crates.io/) 上发布了许多可用于生产的 crate，它们提供的 Web 服务器与线程池实现比我们要写的完整得多。不过本章的目的是帮你学习，而不是走捷径。正因为 Rust 是系统编程语言，我们可以自己选择抽象层级，也可以下沉到其他语言里不现实或做不到的底层。

　　第二，这里不会使用 async 和 await。光是实现线程池就已经够有挑战了，不必再额外搭一套异步运行时！不过我们会指出，本章遇到的一些问题在哪些地方可以改用 async 和 await。正如第 17 章所说，许多异步运行时本身也用线程池来调度工作。

　　因此我们会手写基础的 HTTP 服务器和线程池，好让你掌握将来使用那些 crate 时背后的通用思路与技巧。
