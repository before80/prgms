+++
title = "13 日志与调试"
date = 2026-08-23T13:57:00+08:00
weight = 14
type = "docs"
description = "日志对性能的影响"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Rust Performance Book](https://nnethercote.github.io/perf-book/)

# 日志与调试 {#logging-and-debugging}


> 原文链接: [https://nnethercote.github.io/perf-book/logging-and-debugging.html](https://nnethercote.github.io/perf-book/logging-and-debugging.html)


有时日志代码或调试代码会显著拖慢程序。可能是日志/调试代码本身慢，也可能是为日志/调试收集数据的代码慢。请确保在未启用日志/调试时，不为日志/调试做不必要的工作。
[**示例 1**](https://github.com/rust-lang/rust/pull/50246/commits/2e4f66a86f7baa5644d18bb2adc07a8cd1c7409d)，
[**示例 2**](https://github.com/rust-lang/rust/pull/75133/commits/eeb4b83289e09956e0dda174047729ca87c709fe)，
[**示例 3**](https://github.com/rust-lang/rust/pull/147293/commits/cb0f969b623a7e12a0d8166c9a498e17a8b5a3c4)。

注意 [`assert!`] 调用总是会执行，而 [`debug_assert!`] 仅在开发构建中执行。若有处于热点但并非安全所必需的断言，可考虑改为 `debug_assert!`。
[**示例 1**](https://github.com/rust-lang/rust/pull/58210/commits/f7ed6e18160bc8fccf27a73c05f3935c9e8f672e)，
[**示例 2**](https://github.com/rust-lang/rust/pull/90746/commits/580d357b5adef605fc731d295ca53ab8532e26fb)。

[`assert!`]: https://doc.rust-lang.org/std/macro.assert.html
[`debug_assert!`]: https://doc.rust-lang.org/std/macro.debug_assert.html
