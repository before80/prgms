+++
title = "3.1-配置 cargo-criterion"
date = 2026-08-22T20:00:00+08:00
weight = 22
type = "docs"
description = "cargo-criterion 配置选项"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Criterion.rs Documentation](https://bheisler.github.io/criterion.rs/book/)

# 配置 cargo-criterion {#configuring-cargo-criterion}


> 原文链接: [https://bheisler.github.io/criterion.rs/book/cargo_criterion/configuring_cargo_criterion.html](https://bheisler.github.io/criterion.rs/book/cargo_criterion/configuring_cargo_criterion.html)


cargo-criterion 可以通过在 crate 中（与 `Cargo.toml` 并列）放置 `Criterion.toml` 文件进行配置。

可用设置如下：

```toml
# 用于覆盖 cargo-criterion 保存数据和生成报告的目录。
criterion_home = "./target/criterion"

# 用于配置 cargo-criterion 命令行输出的格式。
# 可选值：
# criterion：打印测量值和吞吐量的置信区间，
#   并指示与上次运行相比是否检测到变化。默认值。
# quiet：与 criterion 类似，但不指示变化。适用于仅展示输出数字，
#   例如在库的 README 中。
# verbose：与 criterion 类似，但会打印额外统计信息。
# bencher：模拟 bencher crate 和仅 nightly 的 libtest 基准测试的输出格式。
output_format = "criterion"

# 用于配置 cargo-criterion 使用的绘图后端。
# 可选值为 "gnuplot" 和 "plotters"，或 "auto"（若 gnuplot 可用则使用 gnuplot，否则使用 plotters）。
plotting_backend = "auto"

# colors 表允许用户配置 cargo-criterion 生成的图表所使用的颜色。
[colors]
# 这些颜色在许多图表中用于将当前测量值与上一次测量值进行比较。
current_sample = {r = 31, g = 120, b = 180}
previous_sample = {r = 7, g = 26, b = 28}

# 这些颜色用于完整 PDF 图表，以突出显示哪些样本是异常值。
not_an_outlier = {r = 31, g = 120, b = 180}
mild_outlier = {r = 5, g = 127, b = 0}
severe_outlier = {r = 7, g = 26, b = 28}

# 这些颜色用于折线图，以比较多个不同的函数。
comparison_colors = [
    {r = 8, g = 34, b = 34},
    {r = 6, g = 139, b = 87},
    {r = 0, g = 139, b = 139},
    {r = 5, g = 215, b = 0},
    {r = 0, g = 0, b = 139},
    {r = 0, g = 20, b = 60},
    {r = 9, g = 0, b = 139},
    {r = 0, g = 255, b = 127},
]

```
