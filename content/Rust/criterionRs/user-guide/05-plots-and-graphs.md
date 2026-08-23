+++
title = "2.5-图表"
date = 2026-08-22T20:00:00+08:00
weight = 7
type = "docs"
description = "Criterion.rs 生成的图表说明"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Criterion.rs Documentation](https://bheisler.github.io/criterion.rs/book/)

# 图表 {#plots-and-graphs}


> 原文链接: [https://bheisler.github.io/criterion.rs/book/user_guide/plots_and_graphs.html](https://bheisler.github.io/criterion.rs/book/user_guide/plots_and_graphs.html)


Criterion.rs 可生成多种有用的图表，便于更好理解基准测试行为。默认使用 [gnuplot](http://www.gnuplot.info/) 生成，若不可用则回退到 `plotters` crate。以下示例由 gnuplot 后端生成，plotters 版本类似。

请注意，在较旧版本的 criterion.rs 中 HTML 报告默认启用。新版本为绘图与 HTML 生成引入了 cargo feature。要启用 HTML 报告生成，请确保 `Cargo.toml` 中启用了该 feature：

```toml
criterion = { version = "0.5", features = ["html_reports"] }
```

## File Structure

图表与保存的数据位于 `target/criterion/$BENCHMARK_NAME/`。目录结构示例如下：

```
$BENCHMARK_NAME/
├── base/
│  ├── raw.csv
│  ├── estimates.json
│  ├── sample.json
│  └── tukey.json
├── change/
│  └── estimates.json
├── new/
│  ├── raw.csv
│  ├── estimates.json
│  ├── sample.json
│  └── tukey.json
└── report/
   ├── both/
   │  ├── pdf.svg
   │  ├── regression.svg
   │  └── iteration_times.svg
   ├── change/
   │  ├── mean.svg
   │  ├── median.svg
   │  └── t-test.svg
   ├── index.html
   ├── MAD.svg
   ├── mean.svg
   ├── median.svg
   ├── pdf.svg
   ├── pdf_small.svg
   ├── regression.svg (optional)
   ├── regression_small.svg (optional)
   ├── iteration_times.svg (optional)
   ├── iteration_times_small.svg (optional)
   ├── relative_pdf_small.svg
   ├── relative_regression_small.svg (optional)
   ├── relative_iteration_times_small.svg (optional)
   ├── SD.svg
   └── slope.svg
```

`new` 文件夹包含最近一次基准运行的统计，`base` 文件夹包含 `base` 基线上一次运行的统计（有关基线的更多信息见 [命令行选项](../03-command-line-options/#baselines)）。图表在 `report` 文件夹中。Criterion.rs 仅保留最近一次运行的历史数据。`report/both` 文件夹包含在同一张图上显示两次运行的图表，`report/change` 包含显示最近两次运行差异的图表。本示例展示默认 `bench_function` 基准方法产生的图表。其他方法可能产生额外图表，将在各自页面说明。

## MAD/Mean/Median/SD/Slope

![Mean Chart](../../images/mean.svg)

这些是 Criterion.rs 生成的最简单图表，显示给定统计量的 bootstrap 分布与置信区间。

## Regression

![Regression Chart](../../images/regression.svg)

回归图在 X-Y 平面上绘制每个数据点，横轴为迭代次数，纵轴为耗时。同时显示 Criterion.rs 对每次迭代时间的最佳拟合直线。良好的基准测试应使数据点紧密沿直线分布。若数据点分散很广，说明噪声大，基准可能不可靠。若数据点呈一致趋势但与直线不符（例如曲线或多段折线），说明基准测试随迭代次数做不同工作量，Criterion.rs 无法生成准确统计，可能需要重做基准。

`report/both` 中的合并回归图仅显示回归线，是两次运行性能差异的有用视觉指标。

回归图仅在 Criterion.rs 使用线性采样模式时可显示。在平坦采样模式下，会改为显示迭代时间图。

## Iteration Times

![Iteration Times Chart](../../images/iteration_times.svg)

迭代时间图显示平均迭代时间的集合。不如回归图有用，但由于平坦采样模式下无法显示回归图，因此会显示此图。

## PDF

![PDF Chart](../../images/pdf.svg)

PDF 图显示样本的概率分布函数，并显示用于将样本分类为离群值的范围。在本示例（与上文回归示例相同）中，可见性能趋势在约 35 次迭代以下有明显变化，值得进一步调查。
