+++
title = "7-从 0.2.* 迁移到 0.3.*"
date = 2026-08-22T20:00:00+08:00
weight = 30
type = "docs"
description = "Criterion.rs 0.2 到 0.3 迁移指南"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Criterion.rs Documentation](https://bheisler.github.io/criterion.rs/book/)

# 从 0.2.* 迁移到 0.3.* {#migrating-0-2-to-0-3}


> 原文链接: [https://bheisler.github.io/criterion.rs/book/migrating_0_2_to_0_3.html](https://bheisler.github.io/criterion.rs/book/migrating_0_2_to_0_3.html)


## 从 0.2.* 迁移到 0.3.*

Criterion.rs 利用 0.3.0 作为破坏性变更版本的机会，进行了一系列需要修改用户代码的更改。本文档记录了这些更改及其较新的替代方案。

### `Benchmark`、`ParameterizedBenchmark`、`Criterion::bench_functions`、`Criterion::bench_function_over_inputs`、`Criterion::bench` 已弃用。

为尽量减少干扰，这些函数仍然存在且仍可使用。它们被故意从文档中隐藏，不应在新代码中使用。在 0.3.0 系列的某个时间点，它们将被正式弃用并开始产生弃用警告。它们将在 0.4.0 中移除。

所有这些类型和函数都已被 `BenchmarkGroup` 类型取代，后者使用起来更简洁，也更强大、更灵活。

### `cargo bench -- --test` 已弃用。

请改用 `cargo test --benches`。

### `raw.csv` 文件的格式已更改，以支持自定义测量。

`sample_time_nanos` 字段已拆分为 `sample_measured_value` 和 `unit`。对于默认的 `WallTime` 测量，`sample_measured_value` 与之前的 `sample_time_nanos` 相同。

### 外部程序基准测试已移除。

这些在 0.2.6 版本中已弃用，因为使用不够广泛，不足以证明额外的维护工作值得。仍可以使用 `iter_custom` 计时循环对外部程序进行基准测试，但需要一些额外工作。虽然这确实需要基准测试作者付出额外的开发工作，但使用 `iter_custom` 在基准测试与外部进程的通信方式上提供了更大的灵活性，还允许基准测试与自定义测量配合使用，这在以前是不可能的。有关对外部进程进行基准测试的示例，请参阅 Criterion.rs 仓库中的 `benches/external_process.rs` 基准测试。

### 吞吐量（Throughput）已扩展为 `u64`

使用 u32 Throughput 的现有基准测试需要修改。使用 u64 允许 Throughput 扩展到更大的字节数/元素数。
