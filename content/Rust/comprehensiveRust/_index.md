+++
title = "Comprehensive Rust"
date = 2026-08-11T11:30:00+08:00
weight = 1
type = "docs"
description = "Comprehensive Rust（全面的 Rust）— Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/](https://google.github.io/comprehensive-rust/)

# 导言

[![Build workflow](https://img.shields.io/github/actions/workflow/status/google/comprehensive-rust/build.yml?style=flat-square)](https://github.com/google/comprehensive-rust/actions/workflows/build.yml?query=branch%3Amain)
[![GitHub contributors](https://img.shields.io/github/contributors/google/comprehensive-rust?style=flat-square)](https://github.com/google/comprehensive-rust/graphs/contributors)
[![GitHub stars](https://img.shields.io/github/stars/google/comprehensive-rust?style=flat-square)](https://github.com/google/comprehensive-rust/stargazers)

这是一门由 Google Android 团队开发的免费 Rust 课程。课程覆盖 Rust 的完整光谱，从基础语法到泛型、错误处理等进阶主题。

> 课程最新版本见
> <https://google.github.io/comprehensive-rust/>。若你在别处阅读，请到该地址查看更新。
>
> 课程提供多种语言版本。可在页面右上角选择偏好语言，或查看
> [翻译](running-the-course/translations.md) 页面了解全部可用译文。
>
> 课程也提供 [PDF 版本](comprehensive-rust.pdf)。

课程目标是教会你 Rust。我们假定你对 Rust 一无所知，并希望：

- 让你全面理解 Rust 的语法与语言特性。
- 使你能够修改现有程序，并用 Rust 编写新程序。
- 向你展示常见的 Rust 惯用法。

我们把前四天称为 Rust 基础（Rust Fundamentals）。

在此之上，欢迎深入一个或多个专题：

- [Android](android.md)：半天课程，介绍在 Android 平台开发（AOSP）中使用 Rust，包括与 C、C++ 和 Java 的互操作。
- [Chromium](chromium.md)：半天课程，介绍在基于 Chromium 的浏览器中使用 Rust，包括与 C++ 的互操作，以及如何在 Chromium 中引入第三方 crate。
- [裸机（Bare-metal）](bare-metal.md)：一整天课程，介绍在裸机（嵌入式）开发中使用 Rust，涵盖微控制器与应用处理器。
- [并发（Concurrency）](concurrency/welcome.md)：一整天课程，介绍 Rust 中的并发。既涵盖经典并发（用线程与互斥锁做抢占式调度），也涵盖 async/await 并发（用 future 做协作式多任务）。

## 非目标

Rust 是一门庞大的语言，几天内无法覆盖全部内容。本课程的部分非目标包括：

- 学习如何开发宏：请参阅
  [《The Rust Book》](https://doc.rust-lang.org/book/) 与
  [Rust by Example](https://doc.rust-lang.org/rust-by-example/macros.html)。

## 先修假定

课程假定你已具备编程经验。Rust 是静态类型语言，我们有时会与 C 和 C++ 对比，以便更好地解释或对照 Rust 的做法。

如果你熟悉 Python 或 JavaScript 等动态类型语言，也能顺利跟上。

> 这是一条*讲师备注*示例。我们用这类备注在幻灯片中补充额外信息，可以是讲师应强调的要点，也可以是课堂上常见问题的答案。

