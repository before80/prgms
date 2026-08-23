+++
title = "4-Iai"
date = 2026-08-22T20:00:00+08:00
weight = 27
type = "docs"
description = "Iai 指令计数基准测试"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Criterion.rs Documentation](https://bheisler.github.io/criterion.rs/book/)

# Iai {#iai}


> 原文链接: [https://bheisler.github.io/criterion.rs/book/iai/iai.html](https://bheisler.github.io/criterion.rs/book/iai/iai.html)


[Iai](https://github.com/bheisler/iai) 是一个实验性基准测试框架，使用 Cachegrind 对 Rust 代码进行极其精确的单次测量。它旨在作为 Criterion.rs 的补充；除其他用途外，它还适用于在 CI 中进行可靠的基准测试。

## API 文档 ##

除本书外，你可能还希望阅读 [API 文档](https://docs.rs/iai/)。
