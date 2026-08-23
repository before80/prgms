+++
title = "2.7-高级配置"
date = 2026-08-22T20:00:00+08:00
weight = 9
type = "docs"
description = "Criterion 高级配置选项"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Criterion.rs Documentation](https://bheisler.github.io/criterion.rs/book/)

# 高级配置 {#advanced-configuration}


> 原文链接: [https://bheisler.github.io/criterion.rs/book/user_guide/advanced_configuration.html](https://bheisler.github.io/criterion.rs/book/user_guide/advanced_configuration.html)


Criterion.rs 为更复杂的用例提供多种配置选项，本文档说明这些选项。

## Configuring Sample Count & Other Statistical Settings

Criterion.rs 允许用户调整部分统计参数。最常见的方式是使用 `BenchmarkGroup` 结构——该结构的文档列出了可用设置。

```rust
use criterion::*;

fn my_function() {
    ...
}

fn bench(c: &mut Criterion) {
    let mut group = c.benchmark_group("sample-size-example");
    // 配置 Criterion.rs 以检测更小的差异，并增大样本量以提高精度、抵消由此产生的噪声
    group.significance_level(0.1).sample_size(500);
    group.bench_function("my-function", |b| b.iter(|| my_function()));
    group.finish();
}

criterion_group!(benches, bench);
criterion_main!(benches);
```

也可通过 `criterion_group` 宏的完整形式修改 Criterion.rs 对这些设置的默认值：

```rust
use criterion::*;

fn my_function() {
    ...
}

fn bench(c: &mut Criterion) {
    let mut group = c.benchmark_group("sample-size-example");
    group.bench_function("my-function", |b| b.iter(|| my_function()));
    group.finish();
}

criterion_group!{
    name = benches;
    // 可以是返回 `Criterion` 对象的任意表达式
    config = Criterion::default().significance_level(0.1).sample_size(500);
    targets = bench
}
criterion_main!(benches);
```

## Throughput Measurements

对某些代码做基准测试时，除每次迭代时间外，测量吞吐量（字节/秒或元素/秒）也很有用。Criterion.rs 可估计基准测试吞吐量，但需知道每次迭代处理多少字节或元素。

吞吐量测量仅在使用 `BenchmarkGroup` 结构时支持；使用较简单的 `bench_function` 接口时不可用。

要测量吞吐量，在 `BenchmarkGroup` 上使用 `throughput` 方法，例如：

```rust
use criterion::*;

fn decode(bytes: &[u8]) {
    // 解码字节
    ...
}

fn bench(c: &mut Criterion) {
    let bytes : &[u8] = ...;

    let mut group = c.benchmark_group("throughput-example");
    group.throughput(Throughput::Bytes(bytes.len() as u64));
    group.bench_function("decode", |b| b.iter(|| decode(bytes));
    group.finish();
}

criterion_group!(benches, bench);
criterion_main!(benches);
```

对参数化基准测试，可在循环内调用 throughput 函数：

```rust
use criterion::*;

type Element = ...;

fn encode(elements: &[Element]) {
    // 编码元素
    ...
}

fn bench(c: &mut Criterion) {
    let elements_1 : &[u8] = ...;
    let elements_2 : &[u8] = ...;

    let mut group = c.benchmark_group("throughput-example");
    for (i, elements) in [elements_1, elements_2].iter().enumerate() {
        group.throughput(Throughput::Elements(elements.len() as u64));
        group.bench_with_input(format!("Encode {}", i), elements, |b, elems| {
            b.iter(||encode(elems))
        });
    }
    group.finish();
}

criterion_group!(benches, bench);
criterion_main!(benches);
```

设置吞吐量后，输出中会出现吞吐量估计：

```
alloc                   time:   [5.9846 ms 6.0192 ms 6.0623 ms]
                        thrpt:  [164.95 MiB/s 166.14 MiB/s 167.10 MiB/s]  
```

## Chart Axis Scaling

默认情况下，Criterion.rs 使用线性坐标轴生成图表。使用参数化基准测试时，输入大小常呈指数增长以覆盖较宽范围。此时用对数坐标轴可能更易读。

与上文吞吐量测量一样，此选项仅在使用 `BenchmarkGroup` 结构时可用。

```rust
use criterion::*;

fn do_a_thing(x: u64) {
    // 做某事
    ...
}

fn bench(c: &mut Criterion) {
    let plot_config = PlotConfiguration::default()
        .summary_scale(AxisScale::Logarithmic);

    let mut group = c.benchmark_group("log_scale_example");
    group.plot_config(plot_config);
    
    for i in [1u64, 10u64, 100u64, 1000u64, 10000u64, 100000u64, 1000000u64].iter() {
        group.bench_function(BenchmarkId::from_parameter(i), i, |b, i| b.iter(|| do_a_thing(i)));
    }
    group.finish();
}

criterion_group!(benches, bench);
criterion_main!(benches);
```

目前坐标轴缩放是 `PlotConfiguration` 结构体上唯一可设置的选项，未来可能增加更多。

## Sampling Mode

默认情况下，Criterion.rs 可良好扩展，处理从皮秒到毫秒量级的基准测试。更长的基准测试也能运行，但往往耗时很长。此前只能减少样本数量来应对。

在 Criterion.rs 0.3.3 中，新增选项可更改采样模式以处理长时间运行的基准测试。基准作者可调用 `BenchmarkGroup::sampling_mode(SamplingMode)` 更改采样模式。

目前有三种选项：
* `SamplingMode::Auto`，从其他选项中自动选择采样模式。这是默认值。
* `SamplingMode::Linear`，面向较快基准测试的原始采样模式。
* `SamplingMode::Flat`，面向长时间运行的基准测试。

平坦采样模式会改变部分统计分析与生成的图表。除非必要，不建议使用 Flat 采样。

```rust
use criterion::*;
use std::time::Duration;

fn my_function() {
    ::std::thread::sleep(Duration::from_millis(10))
}

fn bench(c: &mut Criterion) {
    let mut group = c.benchmark_group("flat-sampling-example");
    group.sampling_mode(SamplingMode::Flat);
    group.bench_function("my-function", |b| b.iter(|| my_function()));
    group.finish();
}

criterion_group!(benches, bench);
criterion_main!(benches);
```
