+++
title = "2.16-基准测试异步函数"
date = 2026-08-22T20:00:00+08:00
weight = 18
type = "docs"
description = "对 async 函数进行基准测试"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Criterion.rs Documentation](https://bheisler.github.io/criterion.rs/book/)

# 基准测试异步函数 {#benchmarking-async}


> 原文链接: [https://bheisler.github.io/criterion.rs/book/user_guide/benchmarking_async.html](https://bheisler.github.io/criterion.rs/book/user_guide/benchmarking_async.html)


## 异步函数基准测试

自 0.3.4 版本起，Criterion.rs 可选支持对异步函数进行基准测试。对异步函数的基准测试与常规函数相同，只是调用方必须提供 futures 执行器来运行基准测试。

### 示例：

```rust
use criterion::BenchmarkId;
use criterion::Criterion;
use criterion::{criterion_group, criterion_main};

// 此结构体告诉 Criterion.rs 使用 "futures" crate 的 current-thread 执行器
use criterion::async_executor::FuturesExecutor;

// 待基准测试的异步函数
async fn do_something(size: usize) {
    // 用 size 执行某些异步操作
}

fn from_elem(c: &mut Criterion) {
    let size: usize = 1024;

    c.bench_with_input(BenchmarkId::new("input_example", size), &size, |b, &s| {
        // 调用 `to_async` 将 bencher 转换为异步模式。
        // 计时循环与常规 bencher 相同。
        b.to_async(FuturesExecutor).iter(|| do_something(s));
    });
}

criterion_group!(benches, from_elem);
criterion_main!(benches);
```

如上代码所示，要对异步函数进行基准测试，我们必须向 bencher 提供异步运行时。运行时结构体见下表。

### 启用异步基准测试

要启用异步基准测试支持，Criterion.rs 必须根据你要基准测试的 futures 执行器编译一个或多个以下特性。建议使用与生产环境相同的执行器。若你的执行器未列于此，可为其实现 `criterion::async_executor::AsyncExecutor` trait 以添加支持，或提交 pull request。

| Crate     | Feature                       | Executor Struct                                                    |
| --------- | ----------------------------- | ------------------------------------------------------------------ |
| Tokio     | "async_tokio"                 | In `tokio::runtime`, `Runtime`, `&Runtime`, `Handle`, or `&Handle` |
| async-std | "async_std" (note underscore) | `AsyncStdExecutor`                                                 |
| Smol      | "async_smol"                  | `SmolExecutor`                                                     |
| futures   | "async_futures"               | `FuturesExecutor`                                                  |
| Other     | "async"                       |                                                                    |

### 异步函数基准测试的注意事项

异步函数自然比同步函数产生更多测量开销。建议在可能时优先对同步函数进行基准测试，尤其是小函数。
