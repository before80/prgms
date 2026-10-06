+++
title = "第五部分：进阶实战1 - Web服务器"
date = 2026-10-06T16:45:00+08:00
weight = 1
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

> 原文链接: [https://beatai.org/rust-course/advance-practice1/intro](https://beatai.org/rust-course/advance-practice1/intro)

# 第五部分：进阶实战1 - Web服务器

　一般来说，现代化的 web 服务器往往都基于更加轻量级的协程或 async/await 等模式实现，但是基于本章的内容，我们还是采取较为传统的多线程的方式来实现，即：一个请求连接分配一个线程去独立处理，当然还有升级版的线程池。

　在本章中你将了解：

1. 学习一点 TCP 和 HTTP
2. 在套接字 socket 上监听进入的 TCP 连接
3. 解析 HTTP 请求
4. 创建合适的 HTTP 应答
5. 使用线程池来提升 web 服务器的吞吐量

> 本章的实现方法并不是在 Rust 中实现 Web 服务器的最佳方法，后续章节的 async/await 会更加适合!
