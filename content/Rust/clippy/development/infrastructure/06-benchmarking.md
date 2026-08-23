+++
title = "06-基准测试"
date = 2026-08-22T18:00:00+08:00
weight = 826
type = "docs"
description = "Clippy 性能基准"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Clippy Documentation](https://doc.rust-lang.org/nightly/clippy/)

# Clippy 基准测试 {#benchmarking}


> 原文链接: [https://doc.rust-lang.org/nightly/clippy/development/infrastructure/benchmarking.html](https://doc.rust-lang.org/nightly/clippy/development/infrastructure/benchmarking.html)


对 Clippy 做基准测试与使用 Lintcheck 工具类似，事实上用的就是同一工具！只需加上 `--perf` 标志，Lintcheck 就会变成非常简单而强大的基准测试工具！

需要安装 [`perf` 工具][perf]，因为实际在底层对 Clippy 进行性能分析的是 `perf`。

lintcheck 的 `--perf` 工具会在 `target/lintcheck/sources/<package>-<version>` 目录下生成一系列 `perf.data`。每个 `perf.data` 对应其中包含的包。

Lintcheck 使用 `-g` 标志，意味着你可以获得栈跟踪以进行更丰富的分析，包括使用 [flamegraph][flamegraph-perf]（或 [`flamegraph-rs`][flamegraph-rs]）等工具。

目前我们只测量指令数，因为这是最可复现的指标，且 [rustc-perf][rustc-perf] 也将其作为主要关注数字。

## 对 PR 做基准测试

将基准测试工具直接集成到 lintcheck 中，使我们能够对任意 PR 做前后对比基准测试。

以下是在任意 PR 上检出、基准测试，再对 `master` 基准测试的方式。

第一个 `perf.data` 不会附加数字，但后续基准会写入 `perf.data.number`，数字从 0 递增。
所有基准都会压缩，以便你

```bash
git fetch upstream pull/<PR_NUMBER>/head:<BRANCH_NAME>
git switch BRANCHNAME

# 基准测试
cargo lintcheck --perf

# 获取最近公共提交并检出
LAST_COMMIT=$(git log BRANCHNAME..master --oneline | tail -1 | cut -c 1-11)
git switch -c temporary $LAST_COMMIT

# 现在在 master 上

# 基准测试
cargo lintcheck --perf
perf diff ./target/lintcheck/sources/CRATE/perf.data ./target/lintcheck/sources/CRATE/perf.data.0
```


[perf]: https://perfwiki.github.io/main/
[flamegraph-perf]: https://github.com/brendangregg/FlameGraph
[flamegraph-rs]: https://github.com/flamegraph-rs/flamegraph
[rustc-perf]: https://github.com/rust-lang/rustc-perf
