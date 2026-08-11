+++
title = "01-优化：速度与体积的权衡"
date = 2026-08-01T10:38:00+08:00
weight = 160
type = "docs"
description = "优化：速度与体积的权衡（Optimizations: The speed size tradeoff）"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Embedded Rust Book](https://doc.rust-lang.org/stable/embedded-book/)

# 优化：速度与体积的权衡 {#optimizations-the-speed-size-tradeoff}


> 原文链接: [https://doc.rust-lang.org/stable/embedded-book/unsorted/speed-vs-size.html](https://doc.rust-lang.org/stable/embedded-book/unsorted/speed-vs-size.html)


人人都希望程序又快又小，但通常无法两者兼得。本节讨论 `rustc` 提供的不同优化级别，以及它们如何影响程序的执行时间与二进制体积。

## 无优化 {#no-optimizations}

这是默认情况。当你调用 `cargo build` 时，使用的是开发（即 `dev`）配置。该配置针对调试进行优化，因此会启用调试信息，并且 *不* 启用任何优化，即使用 `-C opt-level = 0`。

至少对裸机开发而言，调试信息是零成本的：它不会占用 Flash / ROM 空间，因此我们实际上建议你在 release 配置中启用调试信息——默认是关闭的。这样你就可以在调试 release 构建时使用断点。

``` toml
[profile.release]
# 符号很有用，而且不会增加 Flash 上的体积
debug = true
```

无优化非常适合调试，因为单步执行代码感觉像是在逐语句执行程序，而且你可以在 GDB 中 `print` 栈变量与函数参数。当代码被优化后，尝试打印变量会得到 `$0 = <value optimized out>`。

`dev` 配置最大的缺点是生成的二进制文件会又大又慢。体积通常更成问题，因为未优化的二进制可能占用数十 KiB 的 Flash，而目标设备可能没有那么多——结果是：未优化的二进制装不进设备！

我们能否得到更小、又对调试器友好的二进制？可以，有一个技巧。

### 优化依赖 {#optimizing-dependencies}

Cargo 有一个名为 [`profile-overrides`] 的功能，可让你覆盖依赖的优化级别。你可以用它把所有依赖按体积优化，同时保持顶层 crate 未优化且对调试器友好。

请注意，泛型代码有时会与其实例化所在的 crate 一起优化，而不是与定义它的 crate 一起。如果你在应用中创建了泛型结构体的实例，并发现它拉入了占用很大的代码，那么提高相关依赖的优化级别可能毫无效果。

[`profile-overrides`]: https://doc.rust-lang.org/cargo/reference/profiles.html#overrides

示例如下：

``` toml
# Cargo.toml
[package]
name = "app"
# ..

[profile.dev.package."*"] # +
opt-level = "z" # +
```

未使用覆盖时：

``` text
$ cargo size --bin app -- -A
app  :
section               size        addr
.vector_table         1024   0x8000000
.text                 9060   0x8000400
.rodata               1708   0x8002780
.data                    0  0x20000000
.bss                     4  0x20000000
```

使用覆盖后：

``` text
$ cargo size --bin app -- -A
app  :
section               size        addr
.vector_table         1024   0x8000000
.text                 3490   0x8000400
.rodata               1100   0x80011c0
.data                    0  0x20000000
.bss                     4  0x20000000
```

Flash 占用减少了约 6 KiB，且顶层 crate 的可调试性没有任何损失。如果你单步进入某个依赖，又会开始看到那些 `<value optimized out>` 消息，但通常你想调试的是顶层 crate 而不是依赖。如果你 *确实* 需要调试某个依赖，可以用 `profile-overrides` 功能把特定依赖排除在优化之外。见下面的例子：

``` toml
# ..

# 不要优化 `cortex-m-rt` crate
[profile.dev.package.cortex-m-rt] # +
opt-level = 0 # +

# 但要优化所有其它依赖
[profile.dev.package."*"]
codegen-units = 1 # 更好的优化
opt-level = "z"
```

现在顶层 crate 与 `cortex-m-rt` 都对调试器友好了！

## 为速度优化 {#optimize-for-speed}

截至 2018-09-18，`rustc` 支持三个「为速度优化」的级别：`opt-level = 1`、`2` 和 `3`。当你运行 `cargo build --release` 时，使用的是 release 配置，默认 `opt-level = 3`。

`opt-level = 2` 与 `3` 都会以二进制体积为代价优化速度，但级别 `3` 比级别 `2` 做更多的向量化与内联。特别是，你会看到在 `opt-level` 等于或大于 `2` 时，LLVM 会展开循环。循环展开在 Flash / ROM 方面代价相当高（例如，把一个清零数组的循环从 26 字节变为 194 字节），但在合适条件下（例如迭代次数足够大）也能把执行时间减半。

目前无法在 `opt-level = 2` 与 `3` 中禁用循环展开，因此如果你承担不起其代价，就应按体积优化程序。

## 为体积优化 {#optimize-for-size}

截至 2018-09-18，`rustc` 支持两个「为体积优化」的级别：`opt-level = "s"` 与 `"z"`。这些名称继承自 clang / LLVM，并不太直观，但 `"z"` 意在表明它比 `"s"` 产生更小的二进制。

若希望 release 二进制按体积优化，请如下所示更改 `Cargo.toml` 中的 `profile.release.opt-level` 设置。

``` toml
[profile.release]
# 或 "z"
opt-level = "s"
```

这两个优化级别会大幅降低 LLVM 的内联阈值（inline threshold）——用于决定是否内联函数的度量。Rust 的原则之一是零成本抽象；这些抽象往往使用大量 newtype 与小函数来保持不变量（例如借用内部值的函数，如 `deref`、`as_ref`），因此较低的内联阈值可能让 LLVM 错过优化机会（例如消除死分支、内联对闭包的调用）。

按体积优化时，你可以尝试提高内联阈值，看看对二进制体积是否有影响。推荐的更改方式是把 `-C inline-threshold` 标志追加到 `.cargo/config.toml` 中的其它 rustflags。

``` toml
# .cargo/config.toml
# 假定你使用的是 cortex-m-quickstart 模板
[target.'cfg(all(target_arch = "arm", target_os = "none"))']
rustflags = [
  # ..
  "-C", "inline-threshold=123", # +
]
```

该用什么值？[截至 1.29.0，不同优化级别使用的内联阈值如下][inline-threshold]：

[inline-threshold]: https://github.com/rust-lang/rust/blob/1.29.0/src/librustc_codegen_llvm/back/write.rs#L2105-L2122

- `opt-level = 3` 使用 275
- `opt-level = 2` 使用 225
- `opt-level = "s"` 使用 75
- `opt-level = "z"` 使用 25

按体积优化时应尝试 `225` 与 `275`。
