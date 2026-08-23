+++
title = "13-运行时"
date = 2026-08-22T19:00:00+08:00
weight = 15
type = "docs"
description = "运行时"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Asynchronous Programming in Rust](https://rust-lang.github.io/async-book/)

# 运行时 {#runtimes}


> 原文链接: [https://rust-lang.github.io/async-book/part-guide/runtimes.html](https://rust-lang.github.io/async-book/part-guide/runtimes.html)


## 运行 async 代码

- 显式启动 vs async main
- tokio 上下文概念
- block_on
- 代码中反映的运行时（Runtime、Handle）
- 运行时关闭

## 线程与任务

- 默认工作窃取、多线程
  - 回顾 Send + 'static 约束
- yield
- spawn-local
- spawn-blocking（回顾）、block-in-place
- tokio 特有的让出到其他线程、本地 vs 全局队列等内容

## 配置选项

- 线程池大小
- 单线程、每核心一线程等

## 替代运行时

- 为什么你想使用不同的运行时或实现自己的
- 高层设计中存在哪些变化
- 前向引用到高级章节
