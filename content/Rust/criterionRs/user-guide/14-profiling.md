+++
title = "2.14-性能分析"
date = 2026-08-22T20:00:00+08:00
weight = 16
type = "docs"
description = "与性能分析工具集成"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Criterion.rs Documentation](https://bheisler.github.io/criterion.rs/book/)

# 性能分析 {#profiling}


> 原文链接: [https://bheisler.github.io/criterion.rs/book/user_guide/profiling.html](https://bheisler.github.io/criterion.rs/book/user_guide/profiling.html)


优化代码时，对其进行性能分析往往有助于理解其产生所测性能特征的原因。Criterion.rs 提供多项功能以协助对基准测试进行性能分析。

### 关于直接运行基准测试可执行文件的说明

由于 Cargo 在运行基准测试时传递某些命令行参数的方式（更多细节参见 FAQ），Criterion.rs 基准测试可执行文件期望命令行上有 `--bench` 参数。Cargo 会自动添加，但在直接运行可执行文件时（例如在性能分析器中），你需要自行添加 `--bench` 参数。

### `--profile-time`

Criterion.rs 基准测试可执行文件接受 `--profile-time <num_seconds>` 参数。若在某次运行中提供此参数，基准测试可执行文件将尝试在约给定秒数内迭代基准测试，但不会执行其常规分析或保存任何结果。这样，Criterion.rs 的分析代码不会出现在性能分析测量中。

对于使用 Linux perf 等外部性能分析器的用户，只需在喜欢的性能分析器下运行基准测试可执行文件，并传入 profile-time 参数。对于使用 Google `cpuprofiler` 等进程内性能分析器的用户，请继续阅读。

### 实现进程内性能分析钩子

对于希望使用现有 crate 提供的性能分析钩子的开发者，请跳至下文[「启用进程内性能分析」](#enabling-in-process-profiling)。

自 0.3.0 版本起，Criterion.rs 支持添加钩子以启动和停止进程内性能分析器，例如 [cpuprofiler](https://crates.io/crates/cpuprofiler)。该钩子以 trait `criterion::profiler::Profiler` 的形式提供。

```rust
pub trait Profiler {
    fn start_profiling(&mut self, benchmark_id: &str, benchmark_dir: &Path);
    fn stop_profiling(&mut self, benchmark_id: &str, benchmark_dir: &Path);
}
```

在 `--profile-time` 模式下，这些函数会在每个基准测试前后被调用；在其他情况下不会被调用。这使得在需要时轻松将进程内性能分析集成到基准测试中，同时避免性能分析插桩影响常规基准测试测量。

### 启用进程内性能分析

一旦你（或外部 crate）定义了性能分析钩子，使用它相对简单。你需要通过 `with_profiler` 函数提供自己的 profiler 来覆盖默认 `ExternalProfiler` 的 `Criterion` 结构体，并覆盖默认 `Criterion` 对象配置。

```rust
extern crate my_custom_profiler;
use my_custom_profiler::MyCustomProfiler;

fn fibonacci_profiled(criterion: &mut Criterion) {
    // 在此照常使用 criterion 结构体。
}

fn profiled() -> Criterion {
    Criterion::default().with_profiler(MyCustomProfiler)
}

criterion_group! {
    name = benches;
    config = profiled();
    targets = fibonacci_profiled
}
```

性能分析钩子仅在 `--profile-time` 模式下生效。
