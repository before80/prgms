+++
title = "2.11-Bencher 兼容层"
date = 2026-08-22T20:00:00+08:00
weight = 13
type = "docs"
description = "与 libtest Bencher API 兼容"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Criterion.rs Documentation](https://bheisler.github.io/criterion.rs/book/)

# Bencher 兼容层 {#bencher-compatibility}


> 原文链接: [https://bheisler.github.io/criterion.rs/book/user_guide/bencher_compatibility.html](https://bheisler.github.io/criterion.rs/book/user_guide/bencher_compatibility.html)


Criterion.rs 提供了一个小型 crate，可作为 `bencher` 大多数常见用法的即插即用替代，便于现有 `bencher` 用户试用 Criterion.rs。本页展示如何使用该 crate 的示例。

## 示例

我们从 `bencher` 的示例基准测试开始：

```rust
use bencher::{benchmark_group, benchmark_main, Bencher};

fn a(bench: &mut Bencher) {
    bench.iter(|| {
        (0..1000).fold(0, |x, y| x + y)
    })
}

fn b(bench: &mut Bencher) {
    const N: usize = 1024;
    bench.iter(|| {
        vec![0u8; N]
    });

    bench.bytes = N as u64;
}

benchmark_group!(benches, a, b);
benchmark_main!(benches);
```

第一步是编辑 Cargo.toml，将 bencher 依赖替换为 `criterion_bencher_compat`：

将：

```toml
[dev-dependencies]
bencher = "0.1"
```

改为：

```toml
[dev-dependencies]
criterion_bencher_compat = "0.4"
```

然后更新基准测试文件本身，将：

```rust
use bencher::{benchmark_group, benchmark_main, Bencher};
```

改为：

```rust
use criterion_bencher_compat as bencher;
use bencher::{benchmark_group, benchmark_main, Bencher};
```

就这么简单！现在运行 `cargo bench`：

```text
     Running target/release/deps/bencher_example-d865087781455bd5
a                       time:   [234.58 ps 237.68 ps 241.94 ps]
Found 9 outliers among 100 measurements (9.00%)
  4 (4.00%) high mild
  5 (5.00%) high severe

b                       time:   [23.972 ns 24.218 ns 24.474 ns]
Found 4 outliers among 100 measurements (4.00%)
  4 (4.00%) high mild
```

## 限制

`criterion_bencher_compat` 未实现 `bencher` crate 的完整 API，仅覆盖最常用子集。若你的基准测试依赖 `bencher` 中未支持的部分，在试用 Criterion.rs 时可能需要暂时禁用它们。

`criterion_bencher_compat` 无法访问 Criterion.rs 的大多数高级功能。若 Criterion.rs 基准测试对你适用，建议将基准测试改为直接使用 Criterion.rs 接口。更多信息参见[从 libtest 迁移](../01-migrating-from-libtest/)。
