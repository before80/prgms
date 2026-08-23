+++
title = "16-取消与取消安全性"
date = 2026-08-22T19:00:00+08:00
weight = 19
type = "docs"
description = "取消与取消安全性"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Asynchronous Programming in Rust](https://rust-lang.github.io/async-book/)

# 取消与取消安全性 {#cancellation-and-cancellation-safety}


> 原文链接: [https://rust-lang.github.io/async-book/part-reference/cancellation.html](https://rust-lang.github.io/async-book/part-reference/cancellation.html)


内部取消 vs 外部取消
线程 vs future
  drop = 取消
  仅在 await 点
  有用特性
  仍然有些突兀且令人意外
其他取消机制
  abort
  cancellation token（取消令牌）

## 取消安全性

不是内存安全问题或竞态条件
  数据丢失或其他逻辑错误
不同定义/名称
  tokio 的定义
  一般定义/停机安全性（halt safety）
  应用复制 future 的思想
简单的数据丢失
恢复（resumption）
在循环中使用 select 或类似机制时的问题
将状态拆分到 future 与 context 之间作为根本原因
