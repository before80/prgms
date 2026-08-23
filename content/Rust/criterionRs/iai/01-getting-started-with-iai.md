+++
title = "4.1-Iai 入门"
date = 2026-08-22T20:00:00+08:00
weight = 25
type = "docs"
description = "开始使用 Iai"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Criterion.rs Documentation](https://bheisler.github.io/criterion.rs/book/)

# Iai 入门 {#getting-started-with-iai}


> 原文链接: [https://bheisler.github.io/criterion.rs/book/iai/getting_started.html](https://bheisler.github.io/criterion.rs/book/iai/getting_started.html)


## 入门

Iai 的接口设计力求与 Criterion.rs 相似，因此使用起来很方便。要开始使用，请在 `Cargo.toml` 中添加以下内容：

```toml
[dev-dependencies]
iai = "0.1"

[[bench]]
name = "my_benchmark"
harness = false
```

接下来，在 `$PROJECT/benches/my_benchmark.rs` 创建文件并定义基准测试，内容如下：

```rust
use iai::{black_box, main};

fn fibonacci(n: u64) -> u64 {
    match n {
        0 => 1,
        1 => 1,
        n => fibonacci(n-1) + fibonacci(n-2),
    }
}

fn iai_benchmark_short() -> u64 {
    fibonacci(black_box(10))
}

fn iai_benchmark_long() -> u64 {
    fibonacci(black_box(30))
}


iai::main!(iai_benchmark_short, iai_benchmark_long);
```

最后，使用 `cargo bench` 运行此基准测试。你应该会看到类似以下的输出：

```
     Running target/release/deps/test_regular_bench-8b173c29ce041afa

bench_fibonacci_short
  Instructions:                1735
  L1 Accesses:                 2364
  L2 Accesses:                    1
  RAM Accesses:                   1
  Estimated Cycles:            2404

bench_fibonacci_long
  Instructions:            26214735
  L1 Accesses:             35638623
  L2 Accesses:                    2
  RAM Accesses:                   1
  Estimated Cycles:        35638668
```
