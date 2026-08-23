+++
title = "20-底层原理：执行 Future 与 Task"
date = 2026-08-22T19:00:00+08:00
weight = 31
type = "docs"
description = "底层原理：执行 Future 与 Task"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Asynchronous Programming in Rust](https://rust-lang.github.io/async-book/)

# 底层原理：执行 Future 与 Task {#under-the-hood-executing-future-s-and-tasks}


> 原文链接: [https://rust-lang.github.io/async-book/02_execution/01_chapter.html](https://rust-lang.github.io/async-book/02_execution/01_chapter.html)


本节将介绍 `Future` 和异步任务如何被调度的底层结构。若你只想学习如何使用现有 `Future` 类型编写高层代码，而不关心 `Future` 类型的工作原理，可以跳到 `async`/`await` 章节。不过，本章讨论的若干主题对于理解 `async`/`await` 代码如何工作、理解其运行时与性能特性，以及构建新的异步原语都很有用。若现在跳过本节，不妨收藏以便日后回顾。

那么，我们来谈谈 `Future` trait。
