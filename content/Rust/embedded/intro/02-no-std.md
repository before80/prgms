+++
title = "02-no_std"
date = 2026-08-01T10:38:00+08:00
weight = 13
type = "docs"
description = "no_std（`no_std`）"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Embedded Rust Book](https://doc.rust-lang.org/stable/embedded-book/)

# no_std {#a-no_std-rust-environment}


> 原文链接: [https://doc.rust-lang.org/stable/embedded-book/intro/no-std.html](https://doc.rust-lang.org/stable/embedded-book/intro/no-std.html)


“嵌入式编程”这一术语涵盖了非常广泛的编程类别。
从只有几 KB RAM 与 ROM 的 8 位 MCU（如 [ST72325xx](https://www.st.com/resource/en/datasheet/st72325j6.pdf)），
到像 Raspberry Pi（[Model B 3+](https://en.wikipedia.org/wiki/Raspberry_Pi#Specifications)）这样拥有 32/64 位
4 核 Cortex-A53 @ 1.4 GHz 与 1GB RAM 的系统。根据目标与用例的不同，编写代码时会面临不同的限制。

嵌入式编程大体有两类：

## 托管环境（Hosted Environments） {#hosted-environments}

这类环境接近普通 PC 环境。
这意味着你会得到某种系统接口（[例如 POSIX](https://en.wikipedia.org/wiki/POSIX)），
它提供与文件系统、网络、内存管理、线程等各类系统交互的原语。
标准库通常依赖这些原语来实现其功能。
你也可能有某种 sysroot，以及对 RAM/ROM 使用的限制，或许还有一些特殊硬件或 I/O。
整体感觉就像在专用 PC 环境上编码。

## 裸机环境（Bare Metal Environments） {#bare-metal-environments}

在裸机环境中，在你的程序之前没有任何代码被加载。
没有操作系统提供的软件，我们就无法加载标准库。
程序及其所用的 crate 只能依靠硬件（裸机）来运行。
要阻止 Rust 加载标准库，请使用 `no_std`。
标准库中与平台无关的部分可通过 [libcore](https://doc.rust-lang.org/core/) 使用。
libcore 也排除了在嵌入式环境中并不总是可取的功能。
其中之一是用于动态内存分配的内存分配器。
若你需要它或其它功能，通常有 crate 可以提供。

### libstd 运行时 {#the-libstd-runtime}

如前所述，使用 [libstd](https://doc.rust-lang.org/std/) 需要某种系统集成，但这不仅因为
[libstd](https://doc.rust-lang.org/std/) 只是提供访问 OS 抽象的通用方式，它还提供运行时。
该运行时会负责设置栈溢出保护、处理命令行参数，并在程序的 main 函数被调用前生成主线程等。
在 `no_std` 环境中，这个运行时同样不可用。

## 小结 {#summary}

`#![no_std]` 是一个 crate 级属性，表示该 crate 将链接到 core crate 而不是 std crate。
[libcore](https://doc.rust-lang.org/core/) crate 则是 std crate 的平台无关子集，
不对程序将运行其上的系统做任何假设。
因此，它为浮点数、字符串与切片等语言原语提供 API，也暴露原子操作与 SIMD 指令等处理器特性。
但它缺少任何涉及平台集成的 API。
正因这些特性，no\_std 与 [libcore](https://doc.rust-lang.org/core/) 代码可用于任何引导（stage 0）代码，
如引导加载程序、固件或内核。

### 概览 {#overview}

| 功能 | no\_std | std |
|------|--------|-----|
| 堆（动态内存） | * | ✓ |
| 集合（Vec、BTreeMap 等） | ** | ✓ |
| 栈溢出保护 | ✘ | ✓ |
| 在 main 前运行初始化代码 | ✘ | ✓ |
| 可用 libstd | ✘ | ✓ |
| 可用 libcore | ✓ | ✓ |
| 编写固件、内核或引导加载程序代码 | ✓ | ✘ |

\* 仅当你使用 `alloc` crate，并使用合适的分配器（如 [alloc-cortex-m]）时。

\*\* 仅当你使用 `collections` crate 并配置全局默认分配器时。

\*\* 由于缺少安全的随机数生成器，HashMap 与 HashSet 不可用。

[alloc-cortex-m]: https://github.com/rust-embedded/alloc-cortex-m

## 另见 {#see-also}

* [RFC-1184](https://github.com/rust-lang/rfcs/blob/master/text/1184-stabilize-no_std.md)
