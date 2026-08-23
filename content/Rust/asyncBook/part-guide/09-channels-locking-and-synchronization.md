+++
title = "9-通道、锁与同步"
date = 2026-08-22T19:00:00+08:00
weight = 11
type = "docs"
description = "通道、锁与同步"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Asynchronous Programming in Rust](https://rust-lang.github.io/async-book/)

# 通道、锁与同步 {#channels-locking-and-synchronization}


> 原文链接: [https://rust-lang.github.io/async-book/part-guide/sync.html](https://rust-lang.github.io/async-book/part-guide/sync.html)


关于同步原语与运行时的特定性说明

为什么需要异步原语而不是使用同步原语

## 通道

- 基本上与 std 中的相同，但支持 await
  - 在任务之间通信（同一线程或不同线程）
- 一次性（one shot）
- mpsc
- 其他通道
- 有界与无界通道

## 锁

- 异步 Mutex
  - 对比 std::Mutex——可以在 await 点持有（在 guard 中借用 mutex，guard 是 Send，调度器感知？或只是因为锁是异步的？），锁是异步的（等待锁可用时不会阻塞线程）
    - 甚至有 clippy lint 用于检测在 await 时持有 guard（https://rust-lang.github.io/rust-clippy/master/index.html#await_holding_lock）
  - 更昂贵，因为可以在 await 期间持有
    - 如果可以的话使用 std::Mutex
      - 可以使用 try_lock，或预期 mutex 不会有竞争
  - 让出时锁不会神奇地释放（这正是锁的意义所在！）
  - 在 await 期间持有 mutex 导致死锁
    - 任务死锁，但其他任务可以继续推进，因此在进程统计/工具/OS 中可能看起来不像死锁
    - 通常建议——限制作用域、最小化锁、排序锁、优先使用替代方案
  - 没有 mutex 中毒（poisoning）
  - lock_owned
  - blocking_lock
    - 不能在 async 中使用
  - 适用于其他锁（上述内容是否应在专门讨论 mutex 之前移动？可能是的）
- RWLock
- Semaphore
- 让出（yielding）

## 其他同步原语

- notify、barrier
- OnceCell
- 原子操作
