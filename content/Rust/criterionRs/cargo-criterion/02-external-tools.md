+++
title = "3.2-外部工具"
date = 2026-08-22T20:00:00+08:00
weight = 23
type = "docs"
description = "与外部工具集成"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Criterion.rs Documentation](https://bheisler.github.io/criterion.rs/book/)

# 外部工具 {#external-tools}


> 原文链接: [https://bheisler.github.io/criterion.rs/book/cargo_criterion/external_tools.html](https://bheisler.github.io/criterion.rs/book/cargo_criterion/external_tools.html)


cargo-criterion 提供机器可读的输出流，其他工具可以消费该流以收集有关 Criterion.rs 基准测试的信息。

要启用此输出流，请在运行 cargo-criterion 时传入 `--message-format` 参数。

## JSON 消息

当传入 `--message-format=json` 时，cargo-criterion 将输出以下信息：

* 基准测试，包括测量值的基本统计信息
* 基准测试组

输出写入 stdout，每行一个 JSON 对象。`reason` 字段用于区分不同类型的消息。

未来可能会在输出中添加更多消息或字段。

### 基准测试完成消息

"benchmark-complete" 消息包含来自单个 Criterion.rs 基准测试的测量值和基本统计信息。消息格式如下：

```json
{
  /* "reason" 表示这是哪种类型的消息。 */
  "reason": "benchmark-complete",
  /* id 是该基准测试的标识符 */
  "id": "norm",
  /* 包含该基准测试报告的目录路径 */
  "report_directory": "target/criterion/reports/norm",
  /* 整数迭代次数列表 */
  "iteration_count": [
    30,
    /* ... */
    3000
  ],
  /* 浮点测量值列表（例如时间、CPU 周期），
  来自基准测试 */
  "measured_values": [
    124200.0,
    /* ... */
    9937100.0
  ],
  /* 与 measured_values 关联的单位。 */
  "unit": "ns",
  /* 与此基准测试关联的吞吐量值。可用于
  计算吞吐量速率，例如每秒字节数或元素数。 */
  "throughput": [
    {
      "per_iteration": 1024,
      "unit": "elements"
    }
  ],
  /* cargo-criterion 计算的基本统计量的置信区间。 */
  /* 
  "typical" 为斜率（若可用）或均值（若不可用）。它是
  函数典型性能的良好通用估计值。
  */
  "typical": {
    "estimate": 3419.4923993891925,
    "lower_bound": 3375.24221103098,
    "upper_bound": 3465.458469579234,
    "unit": "ns"
  },
  "mean": {
    "estimate": 3419.5340743105917,
    "lower_bound": 3374.4765622217083,
    "upper_bound": 3474.096214164006,
    "unit": "ns"
  },
  "median": {
    "estimate": 3362.8249818445897,
    "lower_bound": 3334.259259259259,
    "upper_bound": 3387.5146198830407,
    "unit": "ns"
  },
  "median_abs_dev": {
    "estimate": 130.7846461816652,
    "lower_bound": 96.55619525548211,
    "upper_bound": 161.1643711235156,
    "unit": "ns"
  },
  
  /* 请注意，并非所有基准测试都能测量斜率，因此该字段
  可能缺失。 */
  "slope": {
    "estimate": 3419.4923993891925,
    "lower_bound": 3375.24221103098,
    "upper_bound": 3465.458469579234,
    "unit": "ns"
  },

  /* "change" 包含有关本次运行与上次运行之间差异的
  一些额外统计信息 */
  "change": {
    /* 均值和中位数值的百分比差异 */
    "mean": {
      "estimate": 0.014278477848724602,
      "lower_bound": -0.01790259435189548,
      "upper_bound": 0.03912764721581533,
      "unit": "%"
    },
    "median": {
      "estimate": 0.012211662837601445,
      "lower_bound": -0.0005448009516478807,
      "upper_bound": 0.024243170768727857,
      "unit": "%"
    },
    /* 
    指示 cargo-criterion 是否检测到统计上显著的变化。
    取值为 NoChange、Improved 或 Regressed
    */
    "change": "NoChange"
  }
}
```

### 组完成消息

当基准测试组完成时，cargo-criterion 会发出 "group-complete" 消息，其中包含有关该组的一些信息。

```json
{
  "reason": "group-complete",
  /* 基准测试组的名称 */
  "group_name": "throughput",
  /* 该组中基准测试 ID 的列表 */
  "benchmarks": [
    "throughput/Bytes",
    "throughput/Bytes",
    "throughput/Elem"
  ],
  /* 包含该组报告的目录路径 */
  "report_directory": "target/criterion/reports/throughput"
}
```
