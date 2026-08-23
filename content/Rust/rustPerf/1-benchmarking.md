+++
title = "1 基准测试"
date = 2026-08-23T13:57:00+08:00
weight = 2
type = "docs"
description = "测量与比较性能"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Rust Performance Book](https://nnethercote.github.io/perf-book/)

# 基准测试 {#benchmarking}


> 原文链接: [https://nnethercote.github.io/perf-book/benchmarking.html](https://nnethercote.github.io/perf-book/benchmarking.html)


基准测试通常涉及比较两个或多个完成相同任务的程序的性能。有时这可能涉及比较两个或多个不同的程序，例如 Firefox 与 Safari 与 Chrome。有时则涉及比较同一程序的不同版本。后一种情况让我们能够可靠地回答「这次改动是否加快了速度？」这一问题。

基准测试是一个复杂的话题，全面覆盖超出了本书的范围，但以下是一些基础知识。

首先，你需要可测量的工作负载。理想情况下，你应拥有多种能代表程序实际使用场景的工作负载。使用真实世界输入的工作负载最佳，但适度使用[微基准测试]和[压力测试]也很有用。

[微基准测试]: https://stackoverflow.com/questions/2842695/what-is-microbenchmarking
[压力测试]: https://en.wikipedia.org/wiki/Stress_testing_(software)

其次，你需要一种运行工作负载的方式，这也会决定所使用的指标。
- Rust 内置的[基准测试][benchmark tests]是一个简单的起点，但它们使用不稳定特性，因此只能在 nightly Rust 上使用。
- [Criterion] 和 [Divan] 是更成熟的替代方案。
- [Hyperfine] 是一款出色的通用基准测试工具。
- [Bencher] 可在 CI（包括 GitHub CI）上进行持续基准测试。
- [Gungraun] 提供 `cargo bench` 集成，可进行高精度测量。
- 也可以构建自定义基准测试框架。例如，[rustc-perf] 是用于对 Rust 编译器进行基准测试的框架。

[benchmark tests]: https://doc.rust-lang.org/nightly/unstable-book/library-features/test.html
[Criterion]: https://github.com/bheisler/criterion.rs
[Divan]: https://github.com/nvzqz/divan
[Hyperfine]: https://github.com/sharkdp/hyperfine
[Bencher]: https://github.com/bencherdev/bencher
[Gungraun]: https://github.com/gungraun/gungraun
[rustc-perf]: https://github.com/rust-lang/rustc-perf/

在指标方面，选择很多，合适的指标取决于被基准测试程序的性质。例如，对批处理程序有意义的指标可能对交互式程序没有意义。在许多情况下，墙钟时间（wall-time）是一个显而易见的选择，因为它对应于用户的感知。然而，它可能具有较高的方差。特别是，内存布局的微小变化可能导致显著但短暂的性能波动。因此，方差较低的指标（如周期数或指令数）可能是合理的替代方案。

汇总多个工作负载的测量结果也是一个挑战，有多种方法可以做到这一点，没有一种方法明显最优。

做好基准测试很难。话虽如此，不必过分纠结于完美的基准测试环境，尤其是在你开始优化程序时。平庸的基准测试远胜于没有基准测试。对你正在测量的内容保持开放心态，随着时间推移，随着你对程序性能特性的了解加深，可以逐步改进基准测试。
