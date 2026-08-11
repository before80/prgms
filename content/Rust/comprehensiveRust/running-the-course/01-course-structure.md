+++
title = "1 课程结构"
date = 2026-08-11T11:30:00+08:00
weight = 3
type = "docs"
description = "01-课程结构 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/running-the-course/course-structure.html](https://google.github.io/comprehensive-rust/running-the-course/course-structure.html)

# 1 课程结构

> 本页面向课程讲师。

## Rust 基础（Rust Fundamentals）

前四天构成 [Rust 基础](../welcome-day-1.md)。节奏较快，覆盖面很广！

课程安排：

- Day 1 Morning（2 小时 10 分钟，含休息）

| 小节 | 时长 |
| --- | --- |
| 欢迎 | 5 分钟 |
| 你好，世界 | 15 分钟 |
| 类型与值 | 40 分钟 |
| 控制流基础 | 45 分钟 |


- Day 1 Afternoon（2 小时 45 分钟，含休息）

| 小节 | 时长 |
| --- | --- |
| 元组与数组 | 35 分钟 |
| 引用 | 55 分钟 |
| 用户自定义类型 | 1 小时 |


- Day 2 Morning（2 小时 50 分钟，含休息）

| 小节 | 时长 |
| --- | --- |
| 欢迎 | 3 分钟 |
| 模式匹配 | 50 分钟 |
| 方法与 Trait | 45 分钟 |
| 泛型 | 50 分钟 |


- Day 2 Afternoon（2 小时 50 分钟，含休息）

| 小节 | 时长 |
| --- | --- |
| 闭包 | 30 分钟 |
| 标准库类型 | 1 小时 |
| 标准库 Trait | 1 小时 |


- Day 3 Morning（2 小时 20 分钟，含休息）

| 小节 | 时长 |
| --- | --- |
| 欢迎 | 3 分钟 |
| 内存管理 | 1 小时 |
| 智能指针 | 55 分钟 |


- Day 3 Afternoon（2 小时 30 分钟，含休息）

| 小节 | 时长 |
| --- | --- |
| 借用 | 1 小时 15 分钟 |
| 生命周期 | 1 小时 5 分钟 |


- Day 4 Morning（2 小时 50 分钟，含休息）

| 小节 | 时长 |
| --- | --- |
| 欢迎 | 3 分钟 |
| 迭代器 | 55 分钟 |
| 模块 | 45 分钟 |
| 测试 | 45 分钟 |


- Day 4 Afternoon（2 小时 20 分钟，含休息）

| 小节 | 时长 |
| --- | --- |
| 错误处理 | 55 分钟 |
| Unsafe Rust | 1 小时 15 分钟 |


## 专题深入（Deep Dives）

除四天的 Rust 基础课外，我们还覆盖一些更专门的主题：

### Rust in Android

[Rust in Android](../android.md) 专题为半天课程，介绍在 Android 平台开发中使用 Rust，包括与 C、C++ 和 Java 的互操作。

你需要一份 [AOSP checkout][1]。在同一台机器上检出
[课程仓库][2]，并把 `src/android/` 目录移到 AOSP checkout 的根目录。这样 Android 构建系统才能看到 `src/android/` 中的 `Android.bp` 文件。

确保 `adb sync` 能与模拟器或真机正常工作，并用 `src/android/build_all.sh` 预先构建全部 Android 示例。阅读该脚本，确认其中命令在你手动执行时也能成功。

[1]: https://source.android.com/docs/setup/download/downloading
[2]: https://github.com/google/comprehensive-rust

### Rust in Chromium

[Rust in Chromium](../chromium.md) 专题为半天课程，介绍在 Chromium 浏览器中使用 Rust，包括在 Chromium 的 `gn` 构建系统中使用 Rust、引入第三方库（crate），以及与 C++ 的互操作。

你需要能构建 Chromium——为速度起见，[建议](../chromium/setup.md)使用 debug、component 构建，但任意构建均可。确保能运行你构建出的 Chromium 浏览器。

### 裸机 Rust（Bare-Metal Rust）

[裸机 Rust](../bare-metal.md) 专题为一整天课程，介绍在裸机（嵌入式）开发中使用 Rust，涵盖微控制器与应用处理器。

微控制器部分需要提前购买
[BBC micro:bit](https://microbit.org/) v2 开发板。每位学员还需按
[欢迎页](../bare-metal.md) 所述安装若干软件包。

### Rust 中的并发（Concurrency in Rust）

[Rust 中的并发](../concurrency/welcome.md) 专题为一整天课程，涵盖经典并发以及 `async`/`await` 并发。

你需要准备一个新的 crate，并事先下载好依赖。之后可以把示例复制到 `src/main.rs` 中实验：

```shell
cargo init concurrency
cd concurrency
cargo add tokio --features full
cargo run
```

课程安排：

- Morning（3 小时 20 分钟，含休息）

| 小节 | 时长 |
| --- | --- |
| 线程 | 30 分钟 |
| 通道 | 20 分钟 |
| `Send` 与 `Sync` | 15 分钟 |
| 共享状态 | 30 分钟 |
| 练习 | 1 小时 10 分钟 |


- Afternoon（3 小时 30 分钟，含休息）

| 小节 | 时长 |
| --- | --- |
| 异步基础 | 40 分钟 |
| 通道与控制流 | 20 分钟 |
| 陷阱 | 55 分钟 |
| 练习 | 1 小时 10 分钟 |


### 惯用 Rust（Idiomatic Rust）

[惯用 Rust](../idiomatic/welcome.md) 专题为两天课程，介绍 Rust 惯用法与模式。

开始本专题前，你应已熟悉
[Rust 基础](../welcome-day-1.md) 中的材料。

课程安排：

- Morning（14 小时 10 分钟，含休息）

| 小节 | 时长 |
| --- | --- |
| API 设计基础 | 3 小时 15 分钟 |
| 利用类型系统 | 7 小时 30 分钟 |
| 多态 | 3 小时 5 分钟 |


### Unsafe（进行中）

[Unsafe](../unsafe-deep-dive/welcome.md) 专题为两天课程，介绍 *unsafe* Rust。内容涵盖 Rust 安全保证的基础、`unsafe` 的动机、`unsafe` 代码的评审流程、FFI 基础，以及构建借用检查器通常会拒绝的数据结构。

课程安排：

- Unsafe Deep Dive（6 小时 40 分钟，含休息）

| 小节 | 时长 |
| --- | --- |
| 环境准备 | 2 分钟 |
| 简介 | 1 小时 10 分钟 |
| 安全前置条件 | 25 分钟 |
| 游戏规则 | 45 分钟 |
| 初始化 | 25 分钟 |
| Pinning（固定） | 1 小时 20 分钟 |
| 外部函数接口（FFI） | 1 小时 35 分钟 |


## 授课形式

本课程强调互动，我们建议让问题驱动对 Rust 的探索！
