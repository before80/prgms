+++
title = "2.17-快速模式"
date = 2026-08-22T20:00:00+08:00
weight = 19
type = "docs"
description = "快速基准测试模式"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Criterion.rs Documentation](https://bheisler.github.io/criterion.rs/book/)

# 快速模式 {#quick-mode}


> 原文链接: [https://bheisler.github.io/criterion.rs/book/user_guide/quick_mode.html](https://bheisler.github.io/criterion.rs/book/user_guide/quick_mode.html)


## 快速模式

快速模式通过 `--quick` 标志启用，指示 criterion 在显著性水平低于某个值（默认 5%，参见 `--significance-level` 标志）后提前停止基准测试。

criterion 中的快速模式与 `tasty-bench` 的工作方式完全相同，后者有大量细节说明：https://github.com/Bodigrim/tasty-bench

### 统计模型

1. 设 n ← 1。
1. 测量 n 次迭代的执行时间 tₙ 和 2n 次迭代的执行时间 t₂ₙ。
1. 找到使 (nt, 2nt) 与 (tₙ, t₂ₙ) 偏差最小的 t，即 t ← (tₙ + 2t₂ₙ) / 5n。
1. 若偏差足够小（参见 `--significance-level`）或时间已用尽（参见 `--measurement-time`），将 t 作为平均执行时间返回。
1. 否则设 n ← 2n 并回到步骤 2。

### 免责声明

统计学是棘手的问题，没有放之四海而皆准的方法。在缺乏良好理论时，简单方法与晦涩方法一样（不）可靠。追求统计严谨性的人应自行收集原始数据，并使用合适的统计工具箱处理。criterion 在快速模式下报告的数据仅具有指示性和对比意义。
