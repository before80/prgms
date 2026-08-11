+++
title = "03-单例"
date = 2026-08-01T10:38:00+08:00
weight = 58
type = "docs"
description = "单例（Singletons）"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Embedded Rust Book](https://doc.rust-lang.org/stable/embedded-book/)

# 单例 {#singletons}


> 原文链接: [https://doc.rust-lang.org/stable/embedded-book/peripherals/singletons.html](https://doc.rust-lang.org/stable/embedded-book/peripherals/singletons.html)


> 在软件工程中，单例模式是一种设计模式，它把一个类的实例化限制为一个对象。
>
> *Wikipedia: [Singleton Pattern]*

[Singleton Pattern]: https://en.wikipedia.org/wiki/Singleton_pattern


## 但我们为什么不能直接用全局变量？ {#but-why-cant-we-just-use-global-variables}

我们可以把一切都做成公开的 static，像这样：

```rust,ignore
static mut THE_SERIAL_PORT: SerialPort = SerialPort;

fn main() {
    let _ = unsafe {
        THE_SERIAL_PORT.read_speed();
    };
}
```

但这有几个问题。它是可变全局变量，在 Rust 中与它们交互总是不安全的。这些变量在整个程序中也可见，这意味着借用检查器无法帮你跟踪这些变量的引用和所有权。

## 在 Rust 里我们怎么做？ {#how-do-we-do-this-in-rust}

与其只把外设做成全局变量，我们也可以决定做一个结构体，这里叫做 `PERIPHERALS`，其中为每个外设包含一个 `Option<T>`。

```rust,ignore
struct Peripherals {
    serial: Option<SerialPort>,
}
impl Peripherals {
    fn take_serial(&mut self) -> SerialPort {
        let p = replace(&mut self.serial, None);
        p.unwrap()
    }
}
static mut PERIPHERALS: Peripherals = Peripherals {
    serial: Some(SerialPort),
};
```

这个结构体让我们能获得外设的唯一实例。若我们尝试不止一次调用 `take_serial()`，代码就会 panic！

```rust,ignore
fn main() {
    let serial_1 = unsafe { PERIPHERALS.take_serial() };
    // 这会 panic！
    // let serial_2 = unsafe { PERIPHERALS.take_serial() };
}
```

虽然与这个结构体交互是 `unsafe` 的，但一旦我们拿到了其中的 `SerialPort`，就不再需要使用 `unsafe`，也不再需要 `PERIPHERALS` 结构体了。

这有一点运行时开销，因为我们必须把 `SerialPort` 包在 Option 里，并且需要调用一次 `take_serial()`；但这一小笔前期成本，让我们能在程序的其余部分利用借用检查器。

## 现有库支持 {#existing-library-support}

虽然上面我们自己创建了 `Peripherals` 结构体，但你的代码未必需要这样做。`cortex_m` crate 包含一个名为 `singleton!()` 的宏，可以为你完成这一操作。

```rust,ignore
use cortex_m::singleton;

fn main() {
    // 若 `main` 只执行一次则没问题
    let x: &'static mut bool =
        singleton!(: bool = false).unwrap();
}
```

[cortex_m docs](https://docs.rs/cortex-m/latest/cortex_m/macro.singleton.html)

此外，若你使用 [`cortex-m-rtic`](https://github.com/rtic-rs/cortex-m-rtic)，定义并获取这些外设的整个过程都会为你抽象掉，你会得到一个 `Peripherals` 结构体，其中包含你所定义各项的非 `Option<T>` 版本。

```rust,ignore
// cortex-m-rtic v0.5.x
#[rtic::app(device = lm3s6965, peripherals = true)]
const APP: () = {
    #[init]
    fn init(cx: init::Context) {
        static mut X: u32 = 0;
         
        // Cortex-M 外设
        let core: cortex_m::Peripherals = cx.core;
        
        // 设备专用外设
        let device: lm3s6965::Peripherals = cx.device;
    }
}
```

## 但为什么？ {#but-why}

这些单例究竟怎样对我们的 Rust 代码产生可感知的影响？

```rust,ignore
impl SerialPort {
    const SER_PORT_SPEED_REG: *mut u32 = 0x4000_1000 as _;

    fn read_speed(
        &self // <------ 这一点非常、非常重要
    ) -> u32 {
        unsafe {
            ptr::read_volatile(Self::SER_PORT_SPEED_REG)
        }
    }
}
```

这里有两个重要因素：

* 因为我们使用单例，获取 `SerialPort` 结构体只有一种方式或一个地方
* 要调用 `read_speed()` 方法，我们必须拥有 `SerialPort` 结构体的所有权或引用

这两个因素合在一起意味着：只有在我们恰当地满足了借用检查器的要求时，才可能访问硬件，也就是说任何时候我们都不会对同一硬件持有多个可变引用！

```rust,ignore
fn main() {
    // 缺少对 `self` 的引用！行不通。
    // SerialPort::read_speed();

    let serial_1 = unsafe { PERIPHERALS.take_serial() };

    // 你只能读取你有权访问的东西
    let _ = serial_1.read_speed();
}
```

## 把硬件当作数据来对待 {#treat-your-hardware-like-data}

此外，因为有些引用是可变的，有些是不可变的，我们就有可能看出某个函数或方法是否可能修改硬件状态。例如，

这允许改变硬件设置：

```rust,ignore
fn setup_spi_port(
    spi: &mut SpiPort,
    cs_pin: &mut GpioPin
) -> Result<()> {
    // ...
}
```

而这不行：

```rust,ignore
fn read_button(gpio: &GpioPin) -> bool {
    // ...
}
```

这让我们能在**编译期**而不是运行时强制要求代码是否应当修改硬件。需要注意的是，这一般只在单个应用程序内有效；但对裸机系统来说，我们的软件会编译成单个应用程序，所以这通常不是限制。
