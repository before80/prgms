+++
title = "2.15-自定义测试框架"
date = 2026-08-22T20:00:00+08:00
weight = 17
type = "docs"
description = "使用自定义测试框架运行基准"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Criterion.rs Documentation](https://bheisler.github.io/criterion.rs/book/)

# 自定义测试框架 {#custom-test-framework}


> 原文链接: [https://bheisler.github.io/criterion.rs/book/user_guide/custom_test_framework.html](https://bheisler.github.io/criterion.rs/book/user_guide/custom_test_framework.html)


Rust 编译器的 nightly 版本支持自定义测试框架。Criterion.rs 提供了自定义测试框架的实验性实现，这意味着你可以使用 `#[criterion]` 属性标记基准测试，而无需使用常规的 `criterion_group!` / `criterion_main!` 宏。目前这需要一些不稳定特性，但未来某个时候 `criterion_group!` / `criterion_main!` 将被弃用，`#[criterion]` 将成为定义 Criterion.rs 基准测试的标准方式。若想提前试用此功能，请参阅下文文档。

## 使用 `#[criterion]`

由于自定义测试框架仍不稳定，你需要使用较新的 nightly 编译器。安装后，在 Cargo.toml 中添加依赖：

```toml
[dev-dependencies]
criterion = "0.5"
criterion-macro = "0.4"
```

请注意，对于 `#[criterion]` 基准测试，我们不需要像常规 Criterion.rs 基准测试那样禁用正常测试 harness。

来看一个示例基准测试（注意此示例假设你使用 Rust 2018）：

```rust
#![feature(custom_test_frameworks)]
#![test_runner(criterion::runner)]

use criterion::Criterion;
use criterion_macro::criterion;
use std::hint::black_box;

fn fibonacci(n: u64) -> u64 {
    match n {
        0 | 1 => 1,
        n => fibonacci(n - 1) + fibonacci(n - 2),
    }
}

fn custom_criterion() -> Criterion {
    Criterion::default()
        .sample_size(50)
}

#[criterion]
fn bench_simple(c: &mut Criterion) {
    c.bench_function("Fibonacci-Simple", |b| b.iter(|| fibonacci(black_box(10))));
}

#[criterion(custom_criterion())]
fn bench_custom(c: &mut Criterion) {
    c.bench_function("Fibonacci-Custom", |b| b.iter(|| fibonacci(black_box(20))));
}
```

首先要注意的是，我们启用 `custom_test_framework` 特性并声明使用 `criterion::runner` 作为测试运行器。我们还导入 `criterion_macro::criterion`，即 `#[criterion]` 宏本身。未来版本可能会从 `criterion` crate 重新导出以便从那里导入，但目前必须从 `criterion_macro` 导入。

之后我们定义老朋友斐波那契函数和基准测试。使用 `#[criterion]` 创建基准测试，只需将属性附加到接受 `&mut Criterion` 的函数上。要提供自定义 Criterion 对象（覆盖默认设置等），可使用 `#[criterion(<返回 criterion 对象的表达式>)]`——这里我们调用 `custom_criterion` 函数。就这么简单！

请记住，除了构建在不稳定编译器特性之上，Criterion.rs 及其测试框架的 API 设计仍处于实验阶段。宏子 crate 会遵守 SemVer，但未来很可能会有破坏性变更。
