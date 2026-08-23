+++
title = "1.1-入门"
date = 2026-08-22T20:00:00+08:00
weight = 2
type = "docs"
description = "为现有 crate 添加 Criterion.rs 基准测试"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Criterion.rs Documentation](https://bheisler.github.io/criterion.rs/book/)

# 入门 {#getting-started}


> 原文链接: [https://bheisler.github.io/criterion.rs/book/getting_started.html](https://bheisler.github.io/criterion.rs/book/getting_started.html)


本文是向现有 crate 添加 Criterion.rs 基准测试的快速入门。

假设我们有一个名为 `mycrate` 的 crate，其 `lib.rs` 包含以下代码：

```rust
#[inline]
pub fn fibonacci(n: u64) -> u64 {
    match n {
        0 => 1,
        1 => 1,
        n => fibonacci(n-1) + fibonacci(n-2),
    }
}
```

### Step 1 - Add Dependency to Cargo.toml ###

要启用 Criterion.rs 基准测试，请在 `Cargo.toml` 中添加以下内容：

```toml
[dev-dependencies]
criterion = "0.5.1"

[[bench]]
name = "my_benchmark"
harness = false
```

这会在开发依赖中加入 Criterion.rs，并声明一个名为 `my_benchmark` 的基准测试，且不使用标准基准测试 harness。禁用标准 harness 很重要，因为稍后我们会添加自己的 harness，避免冲突。

### Step 2 - Add Benchmark ###

作为示例，我们将对斐波那契函数的实现进行基准测试。在 `$PROJECT/benches/my_benchmark.rs` 创建基准测试文件，内容如下（代码说明见下文「详情」一节）：

```rust
use criterion::{criterion_group, criterion_main, Criterion};
use std::hint::black_box;
use mycrate::fibonacci;

fn criterion_benchmark(c: &mut Criterion) {
    c.bench_function("fib 20", |b| b.iter(|| fibonacci(black_box(20))));
}

criterion_group!(benches, criterion_benchmark);
criterion_main!(benches);
```

### Step 3 - Run Benchmark ###

运行该基准测试，使用以下命令：

`cargo bench`

输出应类似：

```
     Running target/release/deps/example-423eedc43b2b3a93
Benchmarking fib 20
Benchmarking fib 20: Warming up for 3.0000 s
Benchmarking fib 20: Collecting 100 samples in estimated 5.0658 s (188100 iterations)
Benchmarking fib 20: Analyzing
fib 20                  time:   [26.029 us 26.251 us 26.505 us]
Found 11 outliers among 99 measurements (11.11%)
  6 (6.06%) high mild
  5 (5.05%) high severe
slope  [26.029 us 26.505 us] R^2            [0.8745662 0.8728027]
mean   [26.106 us 26.561 us] std. dev.      [808.98 ns 1.4722 us]
median [25.733 us 25.988 us] med. abs. dev. [234.09 ns 544.07 ns]
```

### Details ###

下面更详细地说明这段基准测试代码。

```rust
use criterion::{criterion_group, criterion_main, Criterion};
use std::hint::black_box;
use mycrate::fibonacci;
```

首先声明 criterion crate，并导入 [Criterion 类型](http://bheisler.github.io/criterion.rs/criterion/struct.Criterion.html)。Criterion 是 Criterion.rs 库的主要类型，提供配置和定义基准测试组的方法。我们还导入了 `black_box`，稍后说明。

此外，我们将 `mycrate` 声明为外部 crate，并从中导入 fibonacci 函数。Cargo 编译基准测试时（至少 `/benches` 下的那些），会把每个基准测试当作与主 crate 分离的独立 crate。因此需要把库 crate 作为外部 crate 导入，且只能对公开函数做基准测试。

```rust
fn criterion_benchmark(c: &mut Criterion) {
```

这里创建一个函数来容纳基准测试代码。函数名不重要，但应清晰易懂。

```rust
    c.bench_function("fib 20", |b| b.iter(|| fibonacci(black_box(20))));
}
```

这是实际工作所在。`bench_function` 方法用名称和闭包定义基准测试。名称在项目的所有基准测试中应唯一。闭包必须接受一个参数：[Bencher](http://bheisler.github.io/criterion.rs/criterion/struct.Bencher.html)。bencher 执行基准测试——此处它在循环中调用 `fibonacci`。还有其他基准测试方式，包括带参数测试以及比较两个函数的性能。详见 API 文档中的各类选项。`black_box` 可防止编译器把整个函数常量折叠并替换为常量。

你可能记得我们把 `fibonacci` 标为 `#[inline]`，这样它可以在不同 crate 间内联。由于基准测试在技术上是一个独立 crate，因此可以内联进基准测试，提升性能。

```rust
criterion_group!(benches, criterion_benchmark);
criterion_main!(benches);
```

这里调用 `criterion_group!` [宏](http://bheisler.github.io/criterion.rs/criterion/macro.criterion_group.html)，生成名为 benches 的基准测试组，包含前面定义的 `criterion_benchmark`。最后调用 `criterion_main!` [宏](http://bheisler.github.io/criterion.rs/criterion/macro.criterion_main.html)，生成执行 `benches` 组的 main 函数。有关这些宏的更多信息见 API 文档。

### Step 4 - Optimize ###

这个斐波那契函数效率较低，可以改进：

```rust
fn fibonacci(n: u64) -> u64 {
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
```

再次运行基准测试，输出类似：

```
     Running target/release/deps/example-423eedc43b2b3a93
Benchmarking fib 20
Benchmarking fib 20: Warming up for 3.0000 s
Benchmarking fib 20: Collecting 100 samples in estimated 5.0000 s (13548862800 iterations)
Benchmarking fib 20: Analyzing
fib 20                  time:   [353.59 ps 356.19 ps 359.07 ps]
                        change: [-99.999% -99.999% -99.999%] (p = 0.00 < 0.05)
                        Performance has improved.
Found 6 outliers among 99 measurements (6.06%)
  4 (4.04%) high mild
  2 (2.02%) high severe
slope  [353.59 ps 359.07 ps] R^2            [0.8734356 0.8722124]
mean   [356.57 ps 362.74 ps] std. dev.      [10.672 ps 20.419 ps]
median [351.57 ps 355.85 ps] med. abs. dev. [4.6479 ps 10.059 ps]
```

可见，Criterion 在统计上确信优化带来了提升。若引入性能回归，Criterion 会打印相应提示。
