+++
title = "9.2 策略"
date = 2026-08-11T11:30:00+08:00
weight = 563
type = "docs"
description = "02-策略 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/unsafe-deep-dive/ffi/strategies.html](https://google.github.io/comprehensive-rust/unsafe-deep-dive/ffi/strategies.html)

# 9.2 策略

直接共享数据结构与符号非常困难：

```bob
╭────────────╮                                          ╭────────────╮
│            │                                          │            │
│            │ <--------------------------------------> │            │
│            │                                          │            │
╰────────────╯                                          ╰────────────╯
     Rust                                                    "C++"
```

通过 C ABI 进行 FFI 要可行得多：

```bob
╭────────────╮          ╭───╮           ╭───╮          ╭────────────╮
│            │          │   │           │   │          │            │
│            │ <----->  │   │ <~~~~~~~> │   │ <------> │            │ 
│            │          │   │           │   │          │            │
╰────────────╯          ╰───╯           ╰───╯          ╰────────────╯
    Rust                  C               C                 "C++"
```

其他策略：

- 分布式系统（RPC）
- 自定义 ABI（例如 WebAssembly Interface Types）

> _高保真互操作_
>
> 理想场景目前仍处于实验阶段。
>
> 探索这一方向的两个项目是 [crubit](https://github.com/google/crubit) 与 [Zngur](https://hkalbasi.github.io/zngur/)。前者在两侧提供胶水代码，使兼容类型能在域之间无缝工作；后者依赖动态分发，将 C++ 对象作为 trait 对象导入 Rust。
>
> _低保真互操作_ 通过 C API 实现。
>
> 互操作的典型策略是以 C 语言作为接口。C 是一种有损编解码器。该策略通常会在两侧都产生复杂的代码。
>
> _其他策略_ 在零成本环境中可行性较低。
>
> _分布式系统_ 会引入运行时开销。
>
> 调用外部库中的方法需要经过序列化、传输、反序列化的往返，开销显著。一般而言，透明的 RPC 并不是好主意——中间隔着网络。
>
> _自定义 ABI_（例如 wasm）需要运行时或大量实现成本。

