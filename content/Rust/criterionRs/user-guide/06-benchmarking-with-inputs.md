+++
title = "2.6-带输入的基准测试"
date = 2026-08-22T20:00:00+08:00
weight = 8
type = "docs"
description = "对不同输入规模进行基准测试"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Criterion.rs Documentation](https://bheisler.github.io/criterion.rs/book/)

# 带输入的基准测试 {#benchmarking-with-inputs}


> 原文链接: [https://bheisler.github.io/criterion.rs/book/user_guide/benchmarking_with_inputs.html](https://bheisler.github.io/criterion.rs/book/user_guide/benchmarking_with_inputs.html)


Criterion.rs 可使用一个或多个不同输入值运行基准测试，以研究性能如何随输入变化。

## Benchmarking With One Input

若函数只有一个输入，可使用 `Criterion` 结构体上的简单接口运行该基准测试。

```rust
use criterion::BenchmarkId;
use criterion::Criterion;
use criterion::{criterion_group, criterion_main};

fn do_something(size: usize) {
    // 使用 size 做某事
}

fn from_elem(c: &mut Criterion) {
    let size: usize = 1024;

    c.bench_with_input(BenchmarkId::new("input_example", size), &size, |b, &s| {
        b.iter(|| do_something(s));
    });
}

criterion_group!(benches, from_elem);
criterion_main!(benches);
```

这样很方便：会自动将输入经 `black_box` 传递，无需直接调用。还会在基准描述中包含 size。

## Benchmarking With A Range Of Values

Criterion.rs 可使用 `BenchmarkGroup` 比较函数在一系列输入上的性能。

```rust
use std::iter;

use criterion::BenchmarkId;
use criterion::Criterion;
use criterion::Throughput;

fn from_elem(c: &mut Criterion) {
    static KB: usize = 1024;

    let mut group = c.benchmark_group("from_elem");
    for size in [KB, 2 * KB, 4 * KB, 8 * KB, 16 * KB].iter() {
        group.throughput(Throughput::Bytes(*size as u64));
        group.bench_with_input(BenchmarkId::from_parameter(size), size, |b, &size| {
            b.iter(|| iter::repeat(0u8).take(size).collect::<Vec<_>>());
        });
    }
    group.finish();
}

criterion_group!(benches, from_elem);
criterion_main!(benches);
```

本示例对将产生 N 字节序列的迭代器 collect 到 `Vec` 的耗时做基准测试。首先创建基准组，告诉 Criterion.rs 一组基准彼此相关；Criterion.rs 会为基准组生成额外摘要页。然后在所需输入集合上迭代；也可以手动展开循环、生成特定大小的输入等。

在循环内调用 `throughput`，告知 Criterion.rs 每次迭代处理 `size` 字节，用于估计每秒可处理的字节数。接着调用 `bench_with_input`，提供唯一基准 ID（此处仅为 size，也可按需生成自定义字符串），传入 size 以及接受 size 与 `Bencher` 并执行实际测量的闭包。

最后 `finish` 基准组，为该组生成摘要页。建议显式调用 `finish`；若忘记，在组被 drop 时会自动调用。

![Line Chart](../../images/line.svg)

可见迭代器长度与 collect 到 Vec 的耗时大致呈线性关系。
