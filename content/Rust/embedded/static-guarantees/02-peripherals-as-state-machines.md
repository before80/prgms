+++
title = "02-作为状态机的外设"
date = 2026-08-01T10:38:00+08:00
weight = 70
type = "docs"
description = "作为状态机的外设（Peripherals as State Machines）"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Embedded Rust Book](https://doc.rust-lang.org/stable/embedded-book/)

# 作为状态机的外设 {#peripherals-as-state-machines}


> 原文链接: [https://doc.rust-lang.org/stable/embedded-book/static-guarantees/state-machines.html](https://doc.rust-lang.org/stable/embedded-book/static-guarantees/state-machines.html)


微控制器的外设可以被看作一组状态机。例如，一个简化的 [GPIO 引脚][GPIO pin] 的配置可以表示为如下状态树：

[GPIO pin]: https://en.wikipedia.org/wiki/General-purpose_input/output

* Disabled（禁用）
* Enabled（启用）
    * Configured as Output（配置为输出）
        * Output: High（输出：高）
        * Output: Low（输出：低）
    * Configured as Input（配置为输入）
        * Input: High Resistance（输入：高阻）
        * Input: Pulled Low（输入：下拉）
        * Input: Pulled High（输入：上拉）

若外设从 `Disabled` 模式开始，要移到 `Input: High Resistance` 模式，必须执行以下步骤：

1. 禁用（Disabled）
2. 启用（Enabled）
3. 配置为输入（Configured as Input）
4. 输入：高阻（Input: High Resistance）

若想从 `Input: High Resistance` 移到 `Input: Pulled Low`，必须执行以下步骤：

1. 输入：高阻（Input: High Resistance）
2. 输入：下拉（Input: Pulled Low）

类似地，若想把 GPIO 引脚从 `Input: Pulled Low` 配置移到 `Output: High`，必须执行以下步骤：

1. 输入：下拉（Input: Pulled Low）
2. 配置为输入（Configured as Input）
3. 配置为输出（Configured as Output）
4. 输出：高（Output: High）

## 硬件表示 {#hardware-representation}

通常，上面列出的状态是通过向映射到 GPIO 外设的给定寄存器写入值来设置的。我们定义一个假想的 GPIO 配置寄存器来说明这一点：

| 名称         | 位编号        | 值    | 含义      | 说明 |
| ---:         | ------------: | ----: | ------:   | ----: |
| enable       | 0             | 0     | disabled  | 禁用 GPIO |
|              |               | 1     | enabled   | 启用 GPIO |
| direction    | 1             | 0     | input     | 将方向设为输入 |
|              |               | 1     | output    | 将方向设为输出 |
| input_mode   | 2..3          | 00    | hi-z      | 将输入设为高阻 |
|              |               | 01    | pull-low  | 输入引脚下拉 |
|              |               | 10    | pull-high | 输入引脚上拉 |
|              |               | 11    | n/a       | 无效状态，请勿设置 |
| output_mode  | 4             | 0     | set-low   | 输出引脚驱动为低 |
|              |               | 1     | set-high  | 输出引脚驱动为高 |
| input_status | 5             | x     | in-val    | 输入 < 1.5v 时为 0，输入 >= 1.5v 时为 1 |

我们*可以*在 Rust 中暴露如下结构体来控制这个 GPIO：

```rust,ignore
/// GPIO 接口
struct GpioConfig {
    /// 由 svd2rust 生成的 GPIO 配置结构
    periph: GPIO_CONFIG,
}

impl GpioConfig {
    pub fn set_enable(&mut self, is_enabled: bool) {
        self.periph.modify(|_r, w| {
            w.enable().set_bit(is_enabled)
        });
    }

    pub fn set_direction(&mut self, is_output: bool) {
        self.periph.modify(|_r, w| {
            w.direction().set_bit(is_output)
        });
    }

    pub fn set_input_mode(&mut self, variant: InputMode) {
        self.periph.modify(|_r, w| {
            w.input_mode().variant(variant)
        });
    }

    pub fn set_output_mode(&mut self, is_high: bool) {
        self.periph.modify(|_r, w| {
            w.output_mode.set_bit(is_high)
        });
    }

    pub fn get_input_status(&self) -> bool {
        self.periph.read().input_status().bit_is_set()
    }
}
```

然而，这会允许我们修改某些没有意义的寄存器。例如，当 GPIO 配置为输入时设置 `output_mode` 字段会发生什么？

总的来说，使用这个结构体会让我们到达上面状态机未定义的状态：例如被下拉的输出，或被设为高的输入。对某些硬件这可能无关紧要。在其他硬件上，它可能导致意外或未定义行为！

虽然这个接口写起来方便，但它并不强制执行硬件实现所设定的设计契约。
