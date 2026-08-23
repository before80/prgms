+++
title = "3 教程：实现聊天程序"
date = 2026-08-23T16:35:00+08:00
weight = 20
type = "docs"
description = ""
isCJKLanguage = true
draft = false

+++


> 原文链接: [https://book.async.rs/tutorial/index.html](https://book.async.rs/tutorial/index.html)

创建聊天服务器再简单不过了，对吧？
其实不然，聊天服务器会让你直面异步编程中所有那些「有趣」的挑战：

服务器如何并发处理客户端连接？

如何处理客户端断开连接？

如何分发消息？

本教程介绍如何使用 `async-std` 编写聊天服务器。

你也可以在[我们的代码仓库](https://github.com/async-rs/async-std/blob/HEAD/examples/a-chat)中找到本教程。
