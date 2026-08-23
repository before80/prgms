+++
title = "2.3-命令行选项"
date = 2026-08-22T20:00:00+08:00
weight = 5
type = "docs"
description = "cargo bench 与 Criterion 命令行参数"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Criterion.rs Documentation](https://bheisler.github.io/criterion.rs/book/)

# 命令行选项 {#command-line-options}


> 原文链接: [https://bheisler.github.io/criterion.rs/book/user_guide/command_line_options.html](https://bheisler.github.io/criterion.rs/book/user_guide/command_line_options.html)


**注意：若 `cargo bench` 因未知参数失败，请参阅 [FAQ](../../faq/#cargo-bench-gives-unrecognized-option-errors-for-valid-command-line-options)。**

Criterion.rs 基准测试接受多种自定义命令行参数。以下是最常用选项的列表。运行 `cargo bench -- -h` 可查看完整列表。

* 要过滤基准测试，使用 `cargo bench -- <filter>`，其中 `<filter>` 为匹配基准 ID 的正则表达式。例如，运行 `cargo bench -- fib_20` 只会运行 ID 包含 `fib_20` 的基准，而 `cargo bench -- fib_\d+` 也会匹配 `fib_300`。
* 要打印更详细的输出，使用 `cargo bench -- --verbose`
* 要禁用彩色输出，使用 `cargo bench -- --color never`
* 要禁用绘图生成，使用 `cargo bench -- --noplot`
* 要对每个基准测试固定时长迭代，且不保存、分析或绘图，使用 `cargo bench -- --profile-time <num_seconds>`。这在分析基准测试时很有用，可减少分析结果中的无关干扰，并避免 Criterion.rs 正常的动态采样逻辑大幅延长基准运行时间。
* 要保存基线，使用 `cargo bench -- --save-baseline <name>`。要与已有基线比较，使用 `cargo bench -- --baseline <name>`。有关基线的更多信息见下文。
* 要测试基准能否成功运行而不进行测量或分析（例如在 CI 中），使用 `cargo test --benches`。
* 要覆盖默认绘图后端，使用 `cargo bench -- --plotting-backend gnuplot` 或 `cargo bench --plotting-backend plotters`。若已安装 gnuplot，默认使用 gnuplot。
* 要更改 CLI 输出格式，使用 `cargo bench -- --output-format <name>`。支持的输出格式有：
  * `criterion` - 使用 Criterion 的正常输出格式
  * `bencher` - 与 `bencher` crate 或 nightly `libtest` 基准测试类似的输出格式。虽然信息少于 `criterion` 格式，但便于支持能解析该输出的外部工具。
* 要更快运行基准测试但统计保证较低，使用 `cargo bench -- --quick`

## Baselines

默认情况下，Criterion.rs 会将测量结果与上一次运行（如有）比较。有时需要保留多轮运行的测量集。例如，你可能在多次修改代码时仍要与 master 分支比较。对此，Criterion.rs 支持自定义基线。

* `--save-baseline <name>` 会与命名基线比较，然后覆盖它。
* `--baseline <name>` 会与命名基线比较但不覆盖。若指定基线缺少任何基准结果则会失败。
* `--baseline-lenient <name>` 会与命名基线比较但不覆盖。若指定基线缺少任何基准结果也不会失败。适用于在 CI 中自动比较各分支的基准结果。
* `--load-baseline <name>` 会将命名基线加载为新数据集，而非使用上一次基线。

借助这些选项，可管理多组基线测量。例如，若要与 master 分支这样的静态参考点比较，可以运行：

```sh
git checkout master
cargo bench -- --save-baseline master
git checkout feature
cargo bench -- --save-baseline feature
git checkout optimizations

# Some optimization work here

# Measure again
cargo bench
# Now compare against the stored baselines without overwriting it or re-running the measurements
cargo bench -- --load-baseline new --baseline master
cargo bench -- --load-baseline new --baseline feature
```
