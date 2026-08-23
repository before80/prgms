+++
title = "2.2-命令行输出"
date = 2026-08-22T20:00:00+08:00
weight = 4
type = "docs"
description = "基准测试命令行报告解读"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Criterion.rs Documentation](https://bheisler.github.io/criterion.rs/book/)

# 命令行输出 {#command-line-output}


> 原文链接: [https://bheisler.github.io/criterion.rs/book/user_guide/command_line_output.html](https://bheisler.github.io/criterion.rs/book/user_guide/command_line_output.html)


本页输出由运行 `cargo bench -- --verbose` 产生。`cargo bench` 会省略部分信息。注意：若 `cargo bench` 因未知参数失败，请参阅 [FAQ](../../faq/#cargo-bench-gives-unrecognized-option-errors-for-valid-command-line-options)。

每个 Criterion.rs 基准测试会根据测量迭代计算统计量，并生成类似下面的报告：

```
Benchmarking alloc
Benchmarking alloc: Warming up for 1.0000 s
Benchmarking alloc: Collecting 100 samples in estimated 13.354 s (5050 iterations)
Benchmarking alloc: Analyzing
alloc                   time:   [2.5094 ms 2.5306 ms 2.5553 ms]
                        thrpt:  [391.34 MiB/s 395.17 MiB/s 398.51 MiB/s]
                        change: [-38.292% -37.342% -36.524%] (p = 0.00 < 0.05)
                        Performance has improved.
Found 8 outliers among 100 measurements (8.00%)
  4 (4.00%) high mild
  4 (4.00%) high severe
slope  [2.5094 ms 2.5553 ms] R^2            [0.8660614 0.8640630]
mean   [2.5142 ms 2.5557 ms] std. dev.      [62.868 us 149.50 us]
median [2.5023 ms 2.5262 ms] med. abs. dev. [40.034 us 73.259 us]
```

## Warmup

每个 Criterion.rs 基准测试会在可配置的预热期内自动迭代被测函数（默认 3 秒）。对 Rust 函数基准测试而言，这是为了预热处理器缓存以及（如适用）文件系统缓存。

## Collecting Samples

Criterion 以变化的迭代次数运行被测函数，估计每次迭代耗时。样本数量可配置。它还会根据预热阶段的每次迭代时间，打印采样过程预计耗时。

## Time
```
time:   [2.5094 ms 2.5306 ms 2.5553 ms]
thrpt:  [391.34 MiB/s 395.17 MiB/s 398.51 MiB/s]
```

这显示该基准测试每次迭代测量时间的置信区间。左右值为置信区间下界与上界，中间值为 Criterion.rs 对每次迭代耗时的最佳估计。

置信水平可配置。更高的置信水平（如 99%）会拉宽区间，因而对真实斜率的信息更少；较低的置信区间（如 90%）会收窄区间，但你对区间包含真实斜率的信心更低。95% 通常是较好的折中。

Criterion.rs 使用 [bootstrap 重采样](https://en.wikipedia.org/wiki/Bootstrapping_(statistics)) 生成这些置信区间。bootstrap 样本数可配置，默认 100,000。

可选地，Criterion.rs 还能以字节/秒或元素/秒报告被测代码的吞吐量。

## Change

运行 Criterion.rs 基准测试时，会在 `target/criterion` 目录保存统计信息。后续运行会加载这些数据，与当前样本比较，展示代码变更的影响。


```
change: [-38.292% -37.342% -36.524%] (p = 0.00 < 0.05)
Performance has improved.
```

这显示本次运行与上次运行之间差异的置信区间，以及测得差异可能纯属偶然的概率。若无法读取该基准测试的已保存数据，这些行会省略。

第二行是简要摘要。若 Criterion.rs 有充分统计证据表明性能提升或回归，会相应提示；也可能表示变化在噪声阈值内。Criterion.rs 会尽量降低噪声影响，但基准环境差异（如其他进程负载、内存使用等）仍会影响结果。对高度确定的基准测试，Criterion.rs 可能敏感到能检测这些小幅波动，因此与 `+-noise_threshold` 范围重叠的结果视为噪声、不具显著性。噪声阈值可配置，默认为 `+-2%`。

更多示例：

```
alloc                   time:   [1.2421 ms 1.2540 ms 1.2667 ms]
                        change: [+40.772% +43.934% +47.801%] (p = 0.00 < 0.05)
                        Performance has regressed.
```

```
alloc                   time:   [1.2508 ms 1.2630 ms 1.2756 ms]
                        change: [-1.8316% +0.9121% +3.4704%] (p = 0.52 > 0.05)
                        No change in performance detected.
```

```
benchmark               time:   [442.92 ps 453.66 ps 464.78 ps]
                        change: [-0.7479% +3.2888% +7.5451%] (p = 0.04 > 0.05)
                        Change within noise threshold.
```

## Detecting Outliers

```
Found 8 outliers among 100 measurements (8.00%)
  4 (4.00%) high mild
  4 (4.00%) high severe
```

Criterion.rs 会尝试检测异常偏高或偏低的样本，并报告为离群值。大量离群值说明结果噪声较大，应谨慎看待。此处可见部分样本明显长于正常，可能由运行基准的计算机负载不可预测、线程/进程调度，或被测代码单次耗时不规律等引起。

为获得可靠结果，应在空闲机器上运行基准测试，并设计为每次迭代做大致相同的工作量。若做不到，可增加测量时间以降低离群值影响（代价是更长的基准测试时间）。也可延长预热期（确保 JIT 等已预热），或在其他循环中做每次基准前的设置，避免设置影响测量结果。

## Additional Statistics

```
slope  [2.5094 ms 2.5553 ms] R^2            [0.8660614 0.8640630]
mean   [2.5142 ms 2.5557 ms] std. dev.      [62.868 us 149.50 us]
median [2.5023 ms 2.5262 ms] med. abs. dev. [40.034 us 73.259 us]
```

这显示基于其他统计量的额外置信区间。

Criterion.rs 进行线性回归以计算每次迭代时间。第一行显示线性回归斜率的置信区间，R^2 区域显示该置信区间上下界的拟合优度。若 R^2 较低，可能表示基准测试在每次迭代中工作量不一致。可查看绘图输出并改进基准例程的一致性。

第二行显示每次迭代时间均值与标准差（朴素计算）的置信区间。若标准差相对上文时间值很大，说明基准测试噪声大，可能需要调整基准以降低噪声。

median/med. abs. dev. 行与 mean/std. dev. 类似，但使用中位数与 [中位数绝对偏差](https://en.wikipedia.org/wiki/Median_absolute_deviation)。与标准差一样，若 med. abs. dev. 很大，表示基准测试噪声大。

## A Note Of Caution

Criterion.rs 设计为在可能时产生稳健统计，但无法涵盖一切。例如，上文示例中的性能提升与回归，仅通过把笔记本从电池供电切换到市电产生，而非改动被测代码。务必在相近条件下运行基准测试，才能得到有意义的结果。
