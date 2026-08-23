+++
title = "2.1-从 libtest 迁移"
date = 2026-08-22T20:00:00+08:00
weight = 3
type = "docs"
description = "将 libtest 基准测试迁移到 Criterion.rs"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Criterion.rs Documentation](https://bheisler.github.io/criterion.rs/book/)

# 从 libtest 迁移 {#migrating-from-libtest}


> 原文链接: [https://bheisler.github.io/criterion.rs/book/user_guide/migrating_from_libtest.html](https://bheisler.github.io/criterion.rs/book/user_guide/migrating_from_libtest.html)


本页展示如何将 libtest 或 bencher 基准测试迁移为使用 Criterion.rs。

## The Benchmark

以下面的基准测试为例：

```rust
#![feature(test)]
extern crate test;
use test::Bencher;
use test::black_box;

fn fibonacci(n: u64) -> u64 {
    match n {
        0 => 1,
        1 => 1,
        n => fibonacci(n-1) + fibonacci(n-2),
    }
}

#[bench]
fn bench_fib(b: &mut Bencher) {
    b.iter(|| fibonacci(black_box(20)));
}
```

## The Migration

首先要更新 `Cargo.toml`，禁用 libtest 基准测试 harness：

```toml
[[bench]]
name = "example"
harness = false
```

还需要在 `Cargo.toml` 的 `dev-dependencies` 中加入 Criterion.rs：

```toml
[dev-dependencies]
criterion = "0.5.1"
```

下一步更新 import：

```rust
use criterion::{criterion_group, criterion_main, Criterion};
use std::hint::black_box;
```

然后修改 `bench_fib` 函数：去掉 `#[bench]`，将参数改为 `&mut Criterion`。函数体也需要调整：

```rust
fn bench_fib(c: &mut Criterion) {
    c.bench_function("fib 20", |b| b.iter(|| fibonacci(black_box(20))));
}
```

最后需要调用宏生成 main 函数，因为不再有 libtest 提供：

```rust
criterion_group!(benches, bench_fib);
criterion_main!(benches);
```

完成！完整迁移后的基准测试代码如下：

```rust
use criterion::{criterion_group, criterion_main, Criterion};
use std::hint::black_box;

fn fibonacci(n: u64) -> u64 {
    match n {
        0 => 1,
        1 => 1,
        n => fibonacci(n-1) + fibonacci(n-2),
    }
}

fn bench_fib(c: &mut Criterion) {
    c.bench_function("fib 20", |b| b.iter(|| fibonacci(black_box(20))));
}

criterion_group!(benches, bench_fib);
criterion_main!(benches);
```
