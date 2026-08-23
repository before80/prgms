+++
title = "23-同时执行多个 Future"
date = 2026-08-22T19:00:00+08:00
weight = 38
type = "docs"
description = "同时执行多个 Future"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Asynchronous Programming in Rust](https://rust-lang.github.io/async-book/)

# 同时执行多个 Future {#executing-multiple-futures-at-a-time}


> 原文链接: [https://rust-lang.github.io/async-book/06_multiple_futures/01_chapter.html](https://rust-lang.github.io/async-book/06_multiple_futures/01_chapter.html)


到目前为止，我们主要通过 `.await` 执行 future，这会阻塞当前任务直到特定 `Future` 完成。然而，真正的异步应用通常需要并发执行多种不同操作。

本章将介绍同时执行多个异步操作的几种方式：

- `join!`：等待所有 future 完成
- `select!`：等待多个 future 中的任意一个完成
- Spawning：创建在后台将 future 运行至完成的顶层任务
- `FuturesUnordered`：一组 future，产生每个子 future 的结果
