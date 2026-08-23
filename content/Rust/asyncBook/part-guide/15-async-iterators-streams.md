+++
title = "15-异步迭代器（Stream）"
date = 2026-08-22T19:00:00+08:00
weight = 17
type = "docs"
description = "异步迭代器（Stream）"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Asynchronous Programming in Rust](https://rust-lang.github.io/async-book/)

# 异步迭代器（Stream） {#async-iterators-streams}


> 原文链接: [https://rust-lang.github.io/async-book/part-guide/streams.html](https://rust-lang.github.io/async-book/part-guide/streams.html)


- Stream 作为异步迭代器或作为多个 future
- 编写中
  - 当前状态
  - futures 和 Tokio Stream traits
  - nightly trait
- 像同步迭代器一样惰性
- 固定与流（前向引用到固定章节）
- 熔断流

## 消费异步迭代器

- while let 与 async next
- for_each、for_each_concurrent
- collect
- into_future、buffered

## Stream 组合器

- 接受 future 而非闭包
- 一些示例组合器
- unordered 变体
- StreamGroup

### 与流一起使用 join/select/race

- 在循环中使用 select 的隐患
- 熔断
- 与仅使用 future 的区别
- 这些的替代方案
  - Stream::merge 等

## 实现异步迭代器

- 实现 trait
- 实用性与工具函数
- async_iter stream 宏

## Sink

- https://docs.rs/futures/latest/futures/sink/index.html

## 未来工作

- 当前状态
  - https://rust-lang.github.io/rfcs/2996-async-iterator.html
- async next vs poll
- async 迭代语法
- （async）生成器
- 借用迭代器
