+++
title = "2.9-CSV 输出"
date = 2026-08-22T20:00:00+08:00
weight = 11
type = "docs"
description = "导出 CSV 格式基准数据"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Criterion.rs Documentation](https://bheisler.github.io/criterion.rs/book/)

# CSV 输出 {#csv-output}


> 原文链接: [https://bheisler.github.io/criterion.rs/book/user_guide/csv_output.html](https://bheisler.github.io/criterion.rs/book/user_guide/csv_output.html)


注意：CSV 输出正在逐步弃用。对于机器可读输出，建议使用 cargo-criterion 的 `--message-format=json` 选项——参见[外部工具](../../cargo-criterion/02-external-tools/)。CSV 输出将在 Criterion.rs 0.4.0 中成为可选功能。

Criterion.rs 将其测量结果保存在多个文件中，如下所示：

```
$BENCHMARK/
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
```

所有 JSON 文件均被视为 Criterion.rs 的私有实现细节，其结构可能随时更改且不作警告。

然而，需要某种稳定且机器可读的输出，以便 [lolbench](https://github.com/anp/lolbench) 等项目能够保留历史数据或对测量结果进行额外分析。因此，Criterion.rs 还会写入 `raw.csv` 文件。该文件的格式预计在不同版本的 Criterion.rs 之间保持稳定，因此适合外部工具依赖。

`raw.csv` 的格式如下：

```
group,function,value,throughput_num,throughput_type,sample_measured_value,unit,iteration_count
Fibonacci,Iterative,,,,915000,ns,110740
Fibonacci,Iterative,,,,1964000,ns,221480
Fibonacci,Iterative,,,,2812000,ns,332220
Fibonacci,Iterative,,,,3767000,ns,442960
Fibonacci,Iterative,,,,4785000,ns,553700
Fibonacci,Iterative,,,,6302000,ns,664440
Fibonacci,Iterative,,,,6946000,ns,775180
Fibonacci,Iterative,,,,7815000,ns,885920
Fibonacci,Iterative,,,,9186000,ns,996660
Fibonacci,Iterative,,,,9578000,ns,1107400
Fibonacci,Iterative,,,,11206000,ns,1218140
...
```

这些数据来自以下基准测试代码：

```rust
fn compare_fibonaccis(c: &mut Criterion) {
    let mut group = c.benchmark_group("Fibonacci");
    group.bench_with_input("Recursive", 20, |b, i| b.iter(|| fibonacci_slow(*i)));
    group.bench_with_input("Iterative", 20, |b, i| b.iter(|| fibonacci_fast(*i)));
    group.finish();
}
```

`raw.csv` 包含以下列：
 - `group` — 对应函数组名称，在本例中为上文代码中的 "Fibonacci"。这是传给 `Criterion::bench` 函数的参数。
 - `function` — 对应函数名称，在本例中为 "Iterative"。比较多个函数时，每个函数使用不同名称。否则为空字符串。
 - `value` — 使用参数化基准测试时传给被测函数的参数。本例无参数，因此值为空字符串。
 - `throughput_num` — 基准测试上配置的 Throughput 的数值（如有）
 - `throughput_type` — "bytes" 或 "elements"，对应基准测试上配置的 Throughput 变体（如有）
 - `iteration_count` — 该样本中基准测试的迭代次数。
 - `sample_measured_value` — 该样本的测量值。注意这是整个样本的测量值，而非每次迭代的时间（更多细节参见[分析过程](../../analysis/#measurement)）。要计算每次迭代的时间，使用 `sample_measured_value/iteration_count`。
 - `unit` — 表示测量值单位的字符串。对于默认的 `WallTime` 测量，为 "ns"（纳秒）。

如上所示，这是 Criterion.rs 基准测试过程采集的原始测量数据。每个样本一条记录，每个基准测试一个文件。

Criterion.rs 对这些测量结果的分析目前无法以机器可读形式获取。如需访问这些信息，请提交 issue 描述你的用例。
