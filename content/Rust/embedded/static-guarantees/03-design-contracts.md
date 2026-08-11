+++
title = "03-设计契约"
date = 2026-08-01T10:38:00+08:00
weight = 71
type = "docs"
description = "设计契约（Design Contracts）"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Embedded Rust Book](https://doc.rust-lang.org/stable/embedded-book/)

# 设计契约 {#design-contracts}


> 原文链接: [https://doc.rust-lang.org/stable/embedded-book/static-guarantees/design-contracts.html](https://doc.rust-lang.org/stable/embedded-book/static-guarantees/design-contracts.html)


在上一章中，我们写了一个*没有*强制执行设计契约的接口。让我们再看一眼假想的 GPIO 配置寄存器：

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

若我们改为在使用底层硬件前检查状态，在运行时强制执行设计契约，代码可能看起来像这样：

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

    pub fn set_direction(&mut self, is_output: bool) -> Result<(), ()> {
        if self.periph.read().enable().bit_is_clear() {
            // 必须先启用才能设置方向
            return Err(());
        }

        self.periph.modify(|r, w| {
            w.direction().set_bit(is_output)
        });

        Ok(())
    }

    pub fn set_input_mode(&mut self, variant: InputMode) -> Result<(), ()> {
        if self.periph.read().enable().bit_is_clear() {
            // 必须先启用才能设置输入模式
            return Err(());
        }

        if self.periph.read().direction().bit_is_set() {
            // 方向必须是输入
            return Err(());
        }

        self.periph.modify(|_r, w| {
            w.input_mode().variant(variant)
        });

        Ok(())
    }

    pub fn set_output_status(&mut self, is_high: bool) -> Result<(), ()> {
        if self.periph.read().enable().bit_is_clear() {
            // 必须先启用才能设置输出状态
            return Err(());
        }

        if self.periph.read().direction().bit_is_clear() {
            // 方向必须是输出
            return Err(());
        }

        self.periph.modify(|_r, w| {
            w.output_mode.set_bit(is_high)
        });

        Ok(())
    }

    pub fn get_input_status(&self) -> Result<bool, ()> {
        if self.periph.read().enable().bit_is_clear() {
            // 必须先启用才能获取状态
            return Err(());
        }

        if self.periph.read().direction().bit_is_set() {
            // 方向必须是输入
            return Err(());
        }

        Ok(self.periph.read().input_status().bit_is_set())
    }
}
```

因为需要强制执行对硬件的限制，我们最终做了大量浪费时间和资源的运行时检查，而且这段代码对开发者来说用起来也没那么愉快。

## 类型状态 {#type-states}

但如果我们改用 Rust 的类型系统来强制执行状态转换规则呢？看这个例子：

```rust,ignore
/// GPIO 接口
struct GpioConfig<ENABLED, DIRECTION, MODE> {
    /// 由 svd2rust 生成的 GPIO 配置结构
    periph: GPIO_CONFIG,
    enabled: ENABLED,
    direction: DIRECTION,
    mode: MODE,
}

// GpioConfig 中 MODE 的类型状态
struct Disabled;
struct Enabled;
struct Output;
struct Input;
struct PulledLow;
struct PulledHigh;
struct HighZ;
struct DontCare;

/// 这些函数可用于任意 GPIO 引脚
impl<EN, DIR, IN_MODE> GpioConfig<EN, DIR, IN_MODE> {
    pub fn into_disabled(self) -> GpioConfig<Disabled, DontCare, DontCare> {
        self.periph.modify(|_r, w| w.enable.disabled());
        GpioConfig {
            periph: self.periph,
            enabled: Disabled,
            direction: DontCare,
            mode: DontCare,
        }
    }

    pub fn into_enabled_input(self) -> GpioConfig<Enabled, Input, HighZ> {
        self.periph.modify(|_r, w| {
            w.enable.enabled()
             .direction.input()
             .input_mode.high_z()
        });
        GpioConfig {
            periph: self.periph,
            enabled: Enabled,
            direction: Input,
            mode: HighZ,
        }
    }

    pub fn into_enabled_output(self) -> GpioConfig<Enabled, Output, DontCare> {
        self.periph.modify(|_r, w| {
            w.enable.enabled()
             .direction.output()
             .input_mode.set_high()
        });
        GpioConfig {
            periph: self.periph,
            enabled: Enabled,
            direction: Output,
            mode: DontCare,
        }
    }
}

/// 此函数可用于输出引脚
impl GpioConfig<Enabled, Output, DontCare> {
    pub fn set_bit(&mut self, set_high: bool) {
        self.periph.modify(|_r, w| w.output_mode.set_bit(set_high));
    }
}

/// 这些方法可用于任意已启用的输入 GPIO
impl<IN_MODE> GpioConfig<Enabled, Input, IN_MODE> {
    pub fn bit_is_set(&self) -> bool {
        self.periph.read().input_status.bit_is_set()
    }

    pub fn into_input_high_z(self) -> GpioConfig<Enabled, Input, HighZ> {
        self.periph.modify(|_r, w| w.input_mode().high_z());
        GpioConfig {
            periph: self.periph,
            enabled: Enabled,
            direction: Input,
            mode: HighZ,
        }
    }

    pub fn into_input_pull_down(self) -> GpioConfig<Enabled, Input, PulledLow> {
        self.periph.modify(|_r, w| w.input_mode().pull_low());
        GpioConfig {
            periph: self.periph,
            enabled: Enabled,
            direction: Input,
            mode: PulledLow,
        }
    }

    pub fn into_input_pull_up(self) -> GpioConfig<Enabled, Input, PulledHigh> {
        self.periph.modify(|_r, w| w.input_mode().pull_high());
        GpioConfig {
            periph: self.periph,
            enabled: Enabled,
            direction: Input,
            mode: PulledHigh,
        }
    }
}
```

现在看看使用它的代码会是什么样：

```rust,ignore
/*
 * 示例 1：从未配置到高阻输入
 */
let pin: GpioConfig<Disabled, _, _> = get_gpio();

// 做不到，引脚尚未启用！
// pin.into_input_pull_down();

// 现在把引脚从未配置转为高阻输入
let input_pin = pin.into_enabled_input();

// 从引脚读取
let pin_state = input_pin.bit_is_set();

// 做不到，输入引脚没有这个接口！
// input_pin.set_bit(true);

/*
 * 示例 2：从高阻输入到下拉输入
 */
let pulled_low = input_pin.into_input_pull_down();
let pin_state = pulled_low.bit_is_set();

/*
 * 示例 3：从下拉输入到输出，并置高
 */
let output_pin = pulled_low.into_enabled_output();
output_pin.set_bit(true);

// 做不到，输出引脚没有这个接口！
// output_pin.into_input_pull_down();
```

这确实是存储引脚状态的便捷方式，但为什么要这样做？为什么这比在 `GpioConfig` 结构体内部用 `enum` 存储状态更好？

## 编译期功能安全 {#compile-time-functional-safety}

因为我们完全在编译期强制执行设计约束，所以不会产生运行时开销。当你持有输入模式的引脚时，不可能设置输出模式。相反，你必须通过状态逐步转换：先把它转成输出引脚，再设置输出模式。因此，在执行函数前检查当前状态不会带来运行时惩罚。

而且，因为这些状态由类型系统强制执行，该接口的使用者不再有犯错的空间。若他们尝试执行非法状态转换，代码将无法编译！
