+++
title = "03-互操作性"
date = 2026-08-01T10:38:00+08:00
weight = 125
type = "docs"
description = "互操作性（Interoperability）"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Embedded Rust Book](https://doc.rust-lang.org/stable/embedded-book/)

# 互操作性 {#interoperability}


> 原文链接: [https://doc.rust-lang.org/stable/embedded-book/design-patterns/hal/interoperability.html](https://doc.rust-lang.org/stable/embedded-book/design-patterns/hal/interoperability.html)


<a id="c-free"></a>
## 包装类型提供析构方法（C-FREE） {#wrapper-types-provide-a-destructor-method-c-free}

HAL 提供的任何非 `Copy` 包装类型都应提供 `free` 方法：消费该包装类型，并返回创建它时所用的原始外设（以及可能的其它对象）。

该方法应在必要时关闭并复位外设。使用 `free` 返回的原始外设再次调用 `new` 时，不应因外设处于意外状态而失败。

若构造 HAL 类型还需要其它非 `Copy` 对象（例如 I/O 引脚），`free` 也应释放并返回这些对象。此时 `free` 应返回元组。

例如：

```rust
# pub struct TIMER0;
pub struct Timer(TIMER0);

impl Timer {
    pub fn new(periph: TIMER0) -> Self {
        Self(periph)
    }

    pub fn free(self) -> TIMER0 {
        self.0
    }
}
```

<a id="c-reexport-pac"></a>
## HAL 再导出其寄存器访问 crate（C-REEXPORT-PAC） {#hals-reexport-their-register-access-crate-c-reexport-pac}

HAL 可以基于 [svd2rust] 生成的 PAC 编写，也可以基于其它提供原始寄存器访问的 crate。HAL 应始终在 crate 根再导出其所依赖的寄存器访问 crate。

无论实际 crate 名称如何，PAC 都应再导出为 `pac`：HAL 的名称本身已能表明访问的是哪个 PAC。

[svd2rust]: https://github.com/rust-embedded/svd2rust

<a id="c-hal-traits"></a>
## 类型实现 `embedded-hal` trait（C-HAL-TRAITS） {#types-implement-the-embedded-hal-traits-c-hal-traits}

HAL 提供的类型应实现 [`embedded-hal`] crate 中所有适用的 trait。

同一类型可以实现多个 trait。

[`embedded-hal`]: https://github.com/rust-embedded/embedded-hal
