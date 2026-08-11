+++
title = "05-GPIO"
date = 2026-08-01T10:38:00+08:00
weight = 127
type = "docs"
description = "GPIO"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Embedded Rust Book](https://doc.rust-lang.org/stable/embedded-book/)

# GPIO 接口建议 {#recommendations-for-gpio-interfaces}


> 原文链接: [https://doc.rust-lang.org/stable/embedded-book/design-patterns/hal/gpio.html](https://doc.rust-lang.org/stable/embedded-book/design-patterns/hal/gpio.html)


<a id="c-zst-pin"></a>
## 引脚类型默认为零大小类型（C-ZST-PIN） {#pin-types-are-zero-sized-by-default-c-zst-pin}

HAL 暴露的 GPIO 接口应为每个接口或端口上的每个引脚提供专用的零大小类型（ZST），从而在所有引脚分配在静态可知时实现零成本 GPIO 抽象。

每个 GPIO 接口或端口应实现 `split` 方法，返回包含每个引脚的结构体。

示例：

```rust
pub struct PA0;
pub struct PA1;
// ...

pub struct PortA;

impl PortA {
    pub fn split(self) -> PortAPins {
        PortAPins {
            pa0: PA0,
            pa1: PA1,
            // ...
        }
    }
}

pub struct PortAPins {
    pub pa0: PA0,
    pub pa1: PA1,
    // ...
}
```

<a id="c-erased-pin"></a>
## 引脚类型提供擦除引脚与端口的方法（C-ERASED-PIN） {#pin-types-provide-methods-to-erase-pin-and-port-c-erased-pin}

引脚应提供类型擦除方法，将其属性从编译期移到运行期，从而为应用提供更大灵活性。

示例：

```rust
/// 端口 A，引脚 0。
pub struct PA0;

impl PA0 {
    pub fn erase_pin(self) -> PA {
        PA { pin: 0 }
    }
}

/// 端口 A 上的一个引脚。
pub struct PA {
    /// 引脚编号。
    pin: u8,
}

impl PA {
    pub fn erase_port(self) -> Pin {
        Pin {
            port: Port::A,
            pin: self.pin,
        }
    }
}

pub struct Pin {
    port: Port,
    pin: u8,
    // （这些字段可以打包以减小内存占用）
}

enum Port {
    A,
    B,
    C,
    D,
}
```

<a id="c-pin-state"></a>
## 引脚状态应编码为类型参数（C-PIN-STATE） {#pin-state-should-be-encoded-as-type-parameters-c-pin-state}

引脚可按芯片或系列配置为具有不同特性的输入或输出。该状态应编码进类型系统，以防止在错误状态下使用引脚。

额外的芯片特定状态（例如驱动强度）也可以用同样方式编码，通过增加类型参数实现。

改变引脚状态的方法应提供为 `into_input` 与 `into_output`。

此外，还应提供 `with_{input,output}_state` 方法，以便在不移动引脚的情况下临时将其重配置为不同状态。

以下方法应为每种引脚类型提供（也就是说，已擦除与未擦除的引脚类型应提供相同的 API）：

* `pub fn into_input<N: InputState>(self, input: N) -> Pin<N>`
* `pub fn into_output<N: OutputState>(self, output: N) -> Pin<N>`
* ```ignore
  pub fn with_input_state<N: InputState, R>(
      &mut self,
      input: N,
      f: impl FnOnce(&mut PA1<N>) -> R,
  ) -> R
  ```
* ```ignore
  pub fn with_output_state<N: OutputState, R>(
      &mut self,
      output: N,
      f: impl FnOnce(&mut PA1<N>) -> R,
  ) -> R
  ```


引脚状态应由密封 trait（sealed trait）约束。HAL 的用户不应需要添加自己的状态。这些 trait 可以提供实现引脚状态 API 所需的 HAL 特定方法。

示例：

```rust
# use std::marker::PhantomData;
mod sealed {
    pub trait Sealed {}
}

pub trait PinState: sealed::Sealed {}
pub trait OutputState: sealed::Sealed {}
pub trait InputState: sealed::Sealed {
    // ...
}

pub struct Output<S: OutputState> {
    _p: PhantomData<S>,
}

impl<S: OutputState> PinState for Output<S> {}
impl<S: OutputState> sealed::Sealed for Output<S> {}

pub struct PushPull;
pub struct OpenDrain;

impl OutputState for PushPull {}
impl OutputState for OpenDrain {}
impl sealed::Sealed for PushPull {}
impl sealed::Sealed for OpenDrain {}

pub struct Input<S: InputState> {
    _p: PhantomData<S>,
}

impl<S: InputState> PinState for Input<S> {}
impl<S: InputState> sealed::Sealed for Input<S> {}

pub struct Floating;
pub struct PullUp;
pub struct PullDown;

impl InputState for Floating {}
impl InputState for PullUp {}
impl InputState for PullDown {}
impl sealed::Sealed for Floating {}
impl sealed::Sealed for PullUp {}
impl sealed::Sealed for PullDown {}

pub struct PA1<S: PinState> {
    _p: PhantomData<S>,
}

impl<S: PinState> PA1<S> {
    pub fn into_input<N: InputState>(self, input: N) -> PA1<Input<N>> {
        todo!()
    }

    pub fn into_output<N: OutputState>(self, output: N) -> PA1<Output<N>> {
        todo!()
    }

    pub fn with_input_state<N: InputState, R>(
        &mut self,
        input: N,
        f: impl FnOnce(&mut PA1<N>) -> R,
    ) -> R {
        todo!()
    }

    pub fn with_output_state<N: OutputState, R>(
        &mut self,
        output: N,
        f: impl FnOnce(&mut PA1<N>) -> R,
    ) -> R {
        todo!()
    }
}

// `PA`、`Pin` 以及其它引脚类型同理。
```
