+++
title = "2.13-自定义测量"
date = 2026-08-22T20:00:00+08:00
weight = 15
type = "docs"
description = "实现自定义测量后端"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Criterion.rs Documentation](https://bheisler.github.io/criterion.rs/book/)

# 自定义测量 {#custom-measurements}


> 原文链接: [https://bheisler.github.io/criterion.rs/book/user_guide/custom_measurements.html](https://bheisler.github.io/criterion.rs/book/user_guide/custom_measurements.html)


默认情况下，Criterion.rs 测量基准测试的挂钟时间。然而，测量函数性能还有许多其他方式，例如硬件性能计数器或 POSIX 的 CPU 时间。自 0.3.0 版本起，Criterion.rs 支持接入替代计时测量。本页说明如何定义和使用这些自定义测量。

请注意，截至 0.3.0 版本，仅支持计时测量，且一个基准测试只能使用一种测量。这些限制可能在未来版本中放宽。

### 定义自定义测量

对于希望使用现有 crate 提供的自定义测量的开发者，请跳至下文[「使用自定义测量」](#using-custom-measurements)。

自定义测量由一对 trait 定义，均在 `criterion::measurement` 中。

#### Measurement

首先看主 trait `Measurement`。

```rust
pub trait Measurement {
    type Intermediate;
    type Value: MeasuredValue;

    fn start(&self) -> Self::Intermediate;
    fn end(&self, i: Self::Intermediate) -> Self::Value;

    fn add(&self, v1: &Self::Value, v2: &Self::Value) -> Self::Value;
    fn zero(&self) -> Self::Value;
    fn to_f64(&self, val: &Self::Value) -> f64;

    fn formatter(&self) -> &dyn ValueFormatter;
}
```

这里最重要的方法是 `start` 和 `end` 及其关联类型 `Intermediate` 和 `Value`。`start` 用于开始测量，`end` 用于完成测量。例如，挂钟时间测量的 `start` 方法返回调用 `start` 时刻的系统时钟值。该起始时间随后传给 `end` 函数，`end` 再次读取系统时钟并计算两次调用之间的耗时。这种在基准测试前后读取系统计数器并报告差值的模式，是性能测量的常见方式。

接下来的 `add` 和 `zero` 相当简单；Criterion.rs 有时需要将样本拆分为可相加的批次（例如在 `Bencher::iter_batched` 中），因此需要一种方式计算各批次测量值之和以得到样本的总体值。

`to_f64` 用于将测量值转换为 `f64`，以便 Criterion 进行分析。截至 0.3.0，每个基准测试只能返回一个值用于分析。由于 `f64` 不携带单位信息，实现者应谨慎选择单位，避免极大或极小的值导致浮点精度问题。对于挂钟时间，我们转换为纳秒。

最后是 `formatter`，它返回 `ValueFormatter` 的 trait 对象引用（下文详述）。

对于我们的半秒测量，这一切相当直接；我们仍在测量挂钟时间，因此可以像 `WallTime` 一样使用 `Instant` 和 `Duration`：

```rust
/// 以半秒为单位报告挂钟时间的「测量」示例。
struct HalfSeconds;
impl Measurement for HalfSeconds {
    type Intermediate = Instant;
    type Value = Duration;

    fn start(&self) -> Self::Intermediate {
        Instant::now()
    }
    fn end(&self, i: Self::Intermediate) -> Self::Value {
        i.elapsed()
    }
    fn add(&self, v1: &Self::Value, v2: &Self::Value) -> Self::Value {
        *v1 + *v2
    }
    fn zero(&self) -> Self::Value {
        Duration::from_secs(0)
    }
    fn to_f64(&self, val: &Self::Value) -> f64 {
        let nanos = val.as_secs() * NANOS_PER_SEC + u64::from(val.subsec_nanos());
        nanos as f64
    }
    fn formatter(&self) -> &dyn ValueFormatter {
        &HalfSecFormatter
    }
}
```

#### ValueFormatter

下一个 trait 是 `ValueFormatter`，定义测量结果如何展示给用户。

```rust
pub trait ValueFormatter {
    fn format_value(&self, value: f64) -> String {...}
    fn format_throughput(&self, throughput: &Throughput, value: f64) -> String {...}
    fn scale_values(&self, typical_value: f64, values: &mut [f64]) -> &'static str;
    fn scale_throughputs(&self, typical_value: f64, throughput: &Throughput, values: &mut [f64]) -> &'static str;
    fn scale_for_machines(&self, values: &mut [f64]) -> &'static str;
}
```

这些函数都接受 f64 形式的待格式化值；传入的值与 `to_f64` 返回值的尺度相同，但可能不是完全相同的数值。也就是说，若 `to_f64` 返回按「千周期」缩放的值，传给 `format_value` 等函数的值将使用相同单位，但可能是不同数字（例如所有样本时间的均值）。

实现者应尽量以人类易读的方式格式化值。「1,500,000 ns」令人困惑，而「1.5 ms」更清晰。如有可能，尝试使用 SI 前缀简化数字。一种简单方式是使用如下条件序列：

```rust
if ns < 1.0 {  // ns = 每次迭代的纳秒时间
    format!("{:>6} ps", ns * 1e3)
} else if ns < 10f64.powi(3) {
    format!("{:>6} ns", ns)
} else if ns < 10f64.powi(6) {
    format!("{:>6} us", ns / 1e3)
} else if ns < 10f64.powi(9) {
    format!("{:>6} ms", ns / 1e6)
} else {
    format!("{:>6} s", ns / 1e9)
}
```

限制浮点输出精度也是好主意——几位数字之后数值不再重要，却增加视觉噪声并使结果更难解读。例如，很少有人关心 `10.2896653s` 与 `10.2896654s` 的差异——更重要的是函数「每次迭代约 10.290 秒」。

`format_value` 相当直接。`format_throughput` 也不太难；匹配 `Throughput::Bytes` 或 `Throughput::Elements` 并生成适当描述。对于挂钟时间，可能形如「bytes per second」，而读取 CPU 性能计数器的测量可能希望以「cycles per byte」显示吞吐量。注意 `format_value` 和 `format_throughput` 提供了使用 `scale_values` 和 `scale_throughputs` 的默认实现，但可按需覆盖。

`scale_values` 稍复杂。它接受 Criterion.rs 选择的「典型」值，以及待缩放的可变切片。该函数应根据典型值选择合适单位，并将切片中所有值转换为该单位，同时返回表示所选单位的字符串。例如，对于以纳秒为测量值的挂钟时间，若要在毫秒中显示图表，我们将所有输入值乘以 `10.0f64.powi(-6)` 并返回 `"ms"`，因为纳秒乘以 10^-6 得到毫秒。`scale_throughputs` 做同样的事，只是将测量值切片转换为对应的缩放吞吐量值。

`scale_for_machines` 类似于 `scale_values`，但用于生成机器可读输出。它不接受典型值，因为该函数应始终返回相同单位的值。

我们的半秒测量格式化器如下：

```rust
struct HalfSecFormatter;
impl ValueFormatter for HalfSecFormatter {
    fn format_value(&self, value: f64) -> String {
        // 值将以纳秒为单位，需转换为半秒。
        format!("{} s/2", value * 2f64 * 10f64.powi(-9))
    }

    fn format_throughput(&self, throughput: &Throughput, value: f64) -> String {
        match *throughput {
            Throughput::Bytes(bytes) => format!(
                "{} b/s/2",
                f64::from(bytes) / (value * 2f64 * 10f64.powi(-9))
            ),
            Throughput::Elements(elems) => format!(
                "{} elem/s/2",
                f64::from(elems) / (value * 2f64 * 10f64.powi(-9))
            ),
        }
    }

    fn scale_values(&self, ns: f64, values: &mut [f64]) -> &'static str {
        for val in values {
            *val *= 2f64 * 10f64.powi(-9);
        }

        "s/2"
    }

    fn scale_throughputs(
        &self,
        _typical: f64,
        throughput: &Throughput,
        values: &mut [f64],
    ) -> &'static str {
        match *throughput {
            Throughput::Bytes(bytes) => {
                // 将纳秒/迭代转换为字节/半秒。
                for val in values {
                    *val = (bytes as f64) / (*val * 2f64 * 10f64.powi(-9))
                }

                "b/s/2"
            }
            Throughput::Elements(elems) => {
                for val in values {
                    *val = (elems as f64) / (*val * 2f64 * 10f64.powi(-9))
                }

                "elem/s/2"
            }
        }
    }

    fn scale_for_machines(&self, values: &mut [f64]) -> &'static str {
        // 将纳秒值转换为半秒。
        for val in values {
            *val *= 2f64 * 10f64.powi(-9);
        }

        "s/2"
    }
}
```

### 使用自定义测量

一旦你（或外部 crate）定义了自定义测量，使用它相对简单。你需要通过 `with_measurement` 函数提供自己的测量来覆盖默认 `WallTime` 的 `Criterion` 结构体，并覆盖默认 `Criterion` 对象配置。你的基准测试函数也需要声明它们使用的测量类型。

```rust
fn fibonacci_cycles(criterion: &mut Criterion<HalfSeconds>) {
    // 在此照常使用 criterion 结构体。
}

fn alternate_measurement() -> Criterion<HalfSeconds> {
    Criterion::default().with_measurement(HalfSeconds)
}

criterion_group! {
    name = benches;
    config = alternate_measurement();
    targets = fibonacci_cycles
}
```
