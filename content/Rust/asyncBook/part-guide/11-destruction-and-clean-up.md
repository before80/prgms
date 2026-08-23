+++
title = "11-析构与清理"
date = 2026-08-22T19:00:00+08:00
weight = 13
type = "docs"
description = "析构与清理"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Asynchronous Programming in Rust](https://rust-lang.github.io/async-book/)

# 析构与清理 {#destruction-and-clean-up}


> 原文链接: [https://rust-lang.github.io/async-book/part-guide/dtors.html](https://rust-lang.github.io/async-book/part-guide/dtors.html)


- 对象析构与 Drop 回顾
- 软件中一般的清理需求
- Async 相关问题
  - 清理期间可能想异步执行某些操作，例如发送最终消息
  - 可能需要清理仍在异步使用中的内容
  - 可能想在异步任务完成或取消时清理，且无法捕获该情况
  - 清理阶段运行时的状态（尤其是我们正在 panic 等情况时）
  - 没有 async Drop
    - 编写中
  - 前向引用到 completion io 主题

## 取消

- 如何发生（回顾 more-async-await.md）
  - drop 一个 future
  - 取消令牌（cancellation token）
  - abort 函数
- 关于"捕获"取消我们可以做什么
  - 记录或监控取消
- 取消如何影响其他 future/任务（前向引用到取消安全性章节，这里只是提醒）

## Panic 与 async

- panic 跨任务传播（spawn 结果）
- panic 导致数据不一致（tokio mutex）
- 在 panic 时调用 async 代码（确保不要这样做）

## 清理模式

- 避免需要清理（abort/重启）
- 不使用 async 进行清理，也不必过于担心
- async 清理方法 + dtor bomb（即，将清理与析构分离）
- 在单独的任务、线程或监督对象/进程中集中/外包清理
- https://tokio.rs/tokio/topics/shutdown

## 为什么还没有 async Drop

- 注意这是高级章节，不必阅读
- 为什么 async Drop 很难
- 可能的解决方案及其问题
- 当前状态
