+++
title = "02-数学功能"
date = 2026-08-01T10:38:00+08:00
weight = 161
type = "docs"
description = "数学功能（Performing Math Functionality）"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Embedded Rust Book](https://doc.rust-lang.org/stable/embedded-book/)

# 在 `#[no_std]` 下执行数学功能 {#performing-math-functionality-with-no_std}


> 原文链接: [https://doc.rust-lang.org/stable/embedded-book/unsorted/math.html](https://doc.rust-lang.org/stable/embedded-book/unsorted/math.html)


若你想执行与数学相关的功能，例如计算平方根或指数，并且有完整的标准库可用，代码可能如下所示：

```rs
//! 在有标准库支持时的一些数学函数

fn main() {
    let float: f32 = 4.82832;
    let floored_float = float.floor();

    let sqrt_of_four = floored_float.sqrt();

    let sinus_of_four = floored_float.sin();

    let exponential_of_four = floored_float.exp();
    println!("Floored test float {} to {}", float, floored_float);
    println!("The square root of {} is {}", floored_float, sqrt_of_four);
    println!("The sinus of four is {}", sinus_of_four);
    println!(
        "The exponential of four to the base e is {}",
        exponential_of_four
    )
}
```

没有标准库支持时，这些函数不可用。
可以改用像 [`libm`](https://crates.io/crates/libm) 这样的外部 crate。示例代码将如下所示：

```rs
#![no_main]
#![no_std]

use panic_halt as _;

use cortex_m_rt::entry;
use cortex_m_semihosting::{debug, hprintln};
use libm::{exp, floorf, sin, sqrtf};

#[entry]
fn main() -> ! {
    let float = 4.82832;
    let floored_float = floorf(float);

    let sqrt_of_four = sqrtf(floored_float);

    let sinus_of_four = sin(floored_float.into());

    let exponential_of_four = exp(floored_float.into());
    hprintln!("Floored test float {} to {}", float, floored_float).unwrap();
    hprintln!("The square root of {} is {}", floored_float, sqrt_of_four).unwrap();
    hprintln!("The sinus of four is {}", sinus_of_four).unwrap();
    hprintln!(
        "The exponential of four to the base e is {}",
        exponential_of_four
    )
    .unwrap();
    // 退出 QEMU
    // 注意：不要在硬件上运行；它可能破坏 OpenOCD 状态
    // debug::exit(debug::EXIT_SUCCESS);

    loop {}
}
```

若需要在 MCU 上执行更复杂的操作，例如 DSP 信号处理或高级线性代数，以下 crate 可能有帮助：

- [CMSIS DSP library binding](https://github.com/jacobrosenthal/cmsis-dsp-sys)
- [`constgebra`](https://crates.io/crates/constgebra)
- [`micromath`](https://github.com/tarcieri/micromath)
- [`microfft`](https://crates.io/crates/microfft)
- [`nalgebra`](https://github.com/dimforge/nalgebra)
