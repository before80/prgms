+++
title = "2.8-比较函数"
date = 2026-08-22T20:00:00+08:00
weight = 10
type = "docs"
description = "比较多个函数的性能"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Criterion.rs Documentation](https://bheisler.github.io/criterion.rs/book/)

# 比较函数 {#comparing-functions}


> 原文链接: [https://bheisler.github.io/criterion.rs/book/user_guide/comparing_functions.html](https://bheisler.github.io/criterion.rs/book/user_guide/comparing_functions.html)


Criterion.rs 可以自动对函数的多种实现进行基准测试，并生成汇总图表以展示它们之间的性能差异。首先，让我们创建一个对比基准测试。我们还可以将其与对一系列输入进行基准测试结合起来。

```rust
use criterion::{criterion_group, criterion_main, Criterion, BenchmarkId};
use std::hint::black_box;

fn fibonacci_slow(n: u64) -> u64 {
    match n {
        0 => 1,
        1 => 1,
        n => fibonacci_slow(n-1) + fibonacci_slow(n-2),
    }
}

fn fibonacci_fast(n: u64) -> u64 {
    let mut a = 0;
    let mut b = 1;

    match n {
        0 => b,
        _ => {
            for _ in 0..n {
                let c = a + b;
                a = b;
                b = c;
            }
            b
        }
    }
}


fn bench_fibs(c: &mut Criterion) {
    let mut group = c.benchmark_group("Fibonacci");
    for i in [20u64, 21u64].iter() {
        group.bench_with_input(BenchmarkId::new("Recursive", i), i, 
            |b, i| b.iter(|| fibonacci_slow(*i)));
        group.bench_with_input(BenchmarkId::new("Iterative", i), i, 
            |b, i| b.iter(|| fibonacci_fast(*i)));
    }
    group.finish();
}

criterion_group!(benches, bench_fibs);
criterion_main!(benches);
```

这两个斐波那契函数与 [入门](../../getting-started/) 页面中的相同。

```rust
fn bench_fibs(c: &mut Criterion) {
    let mut group = c.benchmark_group("Fibonacci");
    for i in [20u64, 21u64].iter() {
        group.bench_with_input(BenchmarkId::new("Recursive", i), i, 
            |b, i| b.iter(|| fibonacci_slow(black_box(*i))));
        group.bench_with_input(BenchmarkId::new("Iterative", i), i, 
            |b, i| b.iter(|| fibonacci_fast(black_box(*i))));
    }
    group.finish();
}
```

与先前对一系列输入进行基准测试的示例一样，我们创建一个基准测试组并遍历输入。要比较多个函数，只需在循环内多次调用 `bench_with_input`。Criterion 会为每个单独的基准测试/输入对生成报告，以及每个基准测试（跨所有输入）和每个输入（跨所有基准测试）的汇总报告，还有整个基准测试组的总体汇总。

当然，基准测试组同样可以轻松用于对非参数化函数进行基准测试。

## 小提琴图

![Violin Plot](../../images/violin_plot.svg)

[小提琴图](https://en.wikipedia.org/wiki/Violin_plot) 展示各实现的中位时间及其 PDF。

## 折线图

![Line Chart](../../images/lines.svg)

折线图展示随着输入或输入规模增大时不同函数之间的对比，可通过 `Criterion::benchmark_group` 生成。
