+++
title = "6 术语表"
date = 2026-08-23T16:35:00+08:00
weight = 50
type = "docs"
description = ""
isCJKLanguage = true
draft = false

+++


> 原文链接: [https://book.async.rs/glossary.html](https://book.async.rs/glossary.html)

### blocking（阻塞）

「blocked」（被阻塞）通常指阻碍任务继续执行工作的条件。例如，任务可能需要客户端先发送数据才能继续。当任务被阻塞时，通常会调度其他任务来执行。

有时你会听到：在异步上下文中绝不应调用「阻塞函数」。这里指的是会阻塞当前线程、且不交出控制权的函数。这会导致执行器无法使用该线程来调度其他任务。
