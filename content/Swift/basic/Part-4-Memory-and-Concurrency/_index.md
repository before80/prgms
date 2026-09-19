+++
title = "第四篇 内存与并发"
weight = 40
date = "2026-09-14T22:30:00+08:00"
type = "docs"
description = "值语义与写时复制、ARC、循环引用、所有权，以及 async/await 与 actor"
isCJKLanguage = true
draft = false
+++

# 第四篇：内存与并发

> 前半篇回答“这个值到底有几个副本”，后半篇回答“谁能同时碰它”。

这两件事其实是同一个问题的两面。值语义、写时复制和 ARC 决定了数据在内存里的样子；所有权决定了它是被借走还是被搬走；到了并发，这些规则直接变成编译器能替你检查的安全性——actor 隔离和 `Sendable` 不是语法装饰，而是把数据竞争提前到编译期暴露的手段。

这是全书更新最快、也最容易过时的一部分。书里以 Swift 6.3 为基准，凡涉及语言模式差异的地方都会点明；遇到报错别慌，先把报错归到“隔离”还是“所有权”上，方向就清楚了一半。

## 本篇章节

1. [值语义、写时复制与 ARC]({{< relref "Chapter-27-Value-Semantics-COW-and-ARC.md" >}})
2. [循环引用]({{< relref "Chapter-28-Reference-Cycles.md" >}})
3. [内存安全与所有权]({{< relref "Chapter-29-Memory-Safety-and-Ownership.md" >}})
4. [并发（一）：async/await 与结构化并发]({{< relref "Chapter-30-Concurrency-Part-1.md" >}})
5. [并发（二）：隔离域、actor 与 Sendable]({{< relref "Chapter-31-Concurrency-Part-2.md" >}})
6. [并发（三）：迁移与 Approachable Concurrency]({{< relref "Chapter-32-Concurrency-Part-3.md" >}})

## 读完你应该能

- 解释“赋值即复制”的语义与写时复制在性能上做了什么。
- 用 `weak`、`unowned` 和捕获列表打断循环引用，并说出各自的适用条件。
- 读懂 `borrowing`、`consuming`、`~Copyable`、`Span` 这些所有权工具。
- 用 `async/await`、任务组和 actor 写并发代码，并看懂 Swift 6 的并发报错。
