+++
title = "2 构建配置"
date = 2026-08-23T13:57:00+08:00
weight = 3
type = "docs"
description = "编译器与链接器选项"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Rust Performance Book](https://nnethercote.github.io/perf-book/)

# 构建配置 {#build-configuration}


> 原文链接: [https://nnethercote.github.io/perf-book/build-configuration.html](https://nnethercote.github.io/perf-book/build-configuration.html)


你可以在不修改代码的情况下，仅通过更改构建配置来大幅改变 Rust 程序的性能。每个 Rust 程序都有许多可能的构建配置。所选配置会影响编译后代码的多种特性，例如编译时间、运行时速度、内存占用、二进制体积、可调试性、可分析性以及编译后的程序可在哪些架构上运行。

大多数配置选择会改善一种或多种特性，同时恶化一种或多种其他特性。例如，常见的权衡是接受更长的编译时间以换取更高的运行时速度。对你的程序而言，正确的选择取决于你的需求和程序的具体情况，与性能相关的选择（其中大多数属于此类）应通过基准测试来验证。

值得仔细阅读本章以了解所有构建配置选项。不过，对于急躁或健忘的读者，[`cargo-wizard`] 封装了这些信息，可帮助你选择合适的构建配置。

请注意，Cargo 只查看工作区根目录 `Cargo.toml` 文件中的 profile 设置。依赖项中定义的 profile 设置会被忽略。因此，这些选项主要与二进制 crate 相关，而非库 crate。

[`cargo-wizard`]: https://github.com/Kobzol/cargo-wizard

## Release 构建

最重要的构建配置选择很简单，但[容易被忽视][easy to overlook]：当你需要高性能时，确保使用 [release 构建][release build]而非 [dev 构建][dev build]。这通常通过在 Cargo 中指定 `--release` 标志来完成。

[easy to overlook]: https://users.rust-lang.org/t/why-my-rust-program-is-so-slow/47764/5
[release build]: https://doc.rust-lang.org/cargo/reference/profiles.html#release
[dev build]: https://doc.rust-lang.org/cargo/reference/profiles.html#dev

Dev 构建是默认的。它们适合调试，但未经过优化。运行 `cargo build` 或 `cargo run` 时会生成。（或者，不带额外选项运行 `rustc` 也会生成未优化的构建。）

考虑以下 `cargo build` 运行的最后一行输出。
```text
Finished dev [unoptimized + debuginfo] target(s) in 29.80s
```
此输出表明已生成 dev 构建。编译后的代码将放在 `target/debug/` 目录中。`cargo run` 将运行 dev 构建。

相比之下，release 构建经过更多优化，省略调试断言和整数溢出检查，并省略调试信息。相比 dev 构建，10–100 倍的加速很常见！运行 `cargo build --release` 或 `cargo run --release` 时会生成。（或者，`rustc` 有多种优化构建选项，例如 `-O` 和 `-C opt-level`。）由于额外的优化，这通常比 dev 构建耗时更长。

考虑以下 `cargo build --release` 运行的最后一行输出。
```text
Finished release [optimized] target(s) in 1m 01s
```
此输出表明已生成 release 构建。编译后的代码将放在 `target/release/` 目录中。`cargo run --release` 将运行 release 构建。

有关 dev 构建（使用 `dev` profile）与 release 构建（使用 `release` profile）之间差异的更多详情，请参阅 [Cargo profile 文档][Cargo profile documentation]。

[Cargo profile documentation]: https://doc.rust-lang.org/cargo/reference/profiles.html

release 构建中使用的默认构建配置在上述编译时间、运行时速度和二进制体积等特性之间提供了良好的平衡。但还有许多可能的调整，如下各节所述。

## 最大化运行时速度

以下构建配置选项主要用于最大化运行时速度。其中一些还可能减小二进制体积。

### 代码生成单元

Rust 编译器将 crate 拆分为多个[代码生成单元][codegen units]以并行化（从而加速）编译。然而，这可能导致编译器错过一些潜在的优化。你可以通过将单元数设置为 1 来改善运行时速度并减小二进制体积，代价是增加编译时间。在 `Cargo.toml` 文件中添加以下行：
```toml
[profile.release]
codegen-units = 1
```
<!-- Using `https` for this link triggers "potential security risk" warnings due
to a certificate problem. -->
[**示例 1**](http://likebike.com/posts/How_To_Write_Fast_Rust_Code.html#emit-asm)，
[**示例 2**](https://github.com/rust-lang/rust/pull/115554#issuecomment-1742192440)。

[codegen units]: https://doc.rust-lang.org/cargo/reference/profiles.html#codegen-units

### 链接时优化

[链接时优化][Link-time optimization]（LTO）是一种全程序优化技术，可将运行时速度提高 10–20% 或更多，同时减小二进制体积，代价是更长的编译时间。它有多种形式。

[Link-time optimization]: https://doc.rust-lang.org/cargo/reference/profiles.html#lto

第一种 LTO 形式是*瘦本地 LTO*（thin local LTO），一种轻量级 LTO。默认情况下，编译器对任何涉及非零优化级别的构建使用此形式，包括 release 构建。要显式请求此 LTO 级别，在 `Cargo.toml` 文件中添加以下行：
```toml
[profile.release]
lto = false
```

第二种 LTO 形式是*瘦 LTO*（thin LTO），稍微更激进，可能改善运行时速度并减小二进制体积，同时增加编译时间。在 `Cargo.toml` 中使用 `lto = "thin"` 来启用。

第三种 LTO 形式是*胖 LTO*（fat LTO），更加激进，可能进一步改善性能并减小二进制体积（但[并非总是如此][not always]），同时再次增加构建时间。在 `Cargo.toml` 中使用 `lto = "fat"` 来启用。

[not always]: https://github.com/rust-lang/rust/pull/103453

最后，可以完全禁用 LTO，这可能会降低运行时速度并增加二进制体积，但会减少编译时间。在 `Cargo.toml` 中使用 `lto = "off"`。注意，这与 `lto = false` 选项不同，如上所述，`lto = false` 仍保留瘦本地 LTO。

### 替代分配器 {#alternative-allocators}

可以将 Rust 程序使用的默认（系统）堆分配器替换为替代分配器。确切效果取决于具体程序和所选的替代分配器，但实践中已观察到运行时速度的大幅改善和内存占用的大幅减少。效果也因平台而异，因为每个平台的系统分配器各有优劣。使用替代分配器也可能增加二进制体积和编译时间。

#### jemalloc

Linux 和 Mac 上一种流行的替代分配器是 [jemalloc]，可通过 [`tikv-jemallocator`] crate 使用。要使用它，在 `Cargo.toml` 文件中添加依赖：
```toml
[dependencies]
tikv-jemallocator = "0.5"
```
然后在 Rust 代码中添加以下内容，例如在 `src/main.rs` 顶部：
```rust
#[global_allocator]
static GLOBAL: tikv_jemallocator::Jemalloc = tikv_jemallocator::Jemalloc;
```

此外，在 Linux 上，jemalloc 可配置为使用[透明大页][THP]（THP）。这可以进一步加速程序，但可能以增加内存占用为代价。

[THP]: https://www.kernel.org/doc/html/next/admin-guide/mm/transhuge.html

在构建程序之前，通过适当设置 `MALLOC_CONF` 环境变量（或 [`_RJEM_MALLOC_CONF`]）来实现，例如：
```bash
MALLOC_CONF="thp:always,metadata_thp:always" cargo build --release
```
运行编译后程序的系统也必须配置为支持 THP。更多详情见[这篇博客文章][this blog post]。

[`_RJEM_MALLOC_CONF`]: https://github.com/tikv/jemallocator/issues/65
[this blog post]: https://kobzol.github.io/rust/rustc/2023/10/21/make-rust-compiler-5percent-faster.html

#### mimalloc

另一种适用于许多平台的替代分配器是 [mimalloc]，可通过 [`mimalloc`] crate 使用。要使用它，在 `Cargo.toml` 文件中添加依赖：
```toml
[dependencies]
mimalloc = "0.1"
```
然后在 Rust 代码中添加以下内容，例如在 `src/main.rs` 顶部：
```rust
#[global_allocator]
static GLOBAL: mimalloc::MiMalloc = mimalloc::MiMalloc;
```

[jemalloc]: https://github.com/jemalloc/jemalloc
[`tikv-jemallocator`]: https://crates.io/crates/tikv-jemallocator
[better performance]: https://github.com/rust-lang/rust/pull/83152
[mimalloc]: https://github.com/microsoft/mimalloc
[`mimalloc`]: https://crates.io/crates/mimalloc

### 特定 CPU 指令

如果你不关心二进制在较旧（或其他类型）处理器上的兼容性，可以告诉编译器为[特定 CPU 架构][certain CPU architecture]生成最新（可能最快）的指令，例如为 x86-64 CPU 生成 AVX SIMD 指令。

[certain CPU architecture]: https://doc.rust-lang.org/rustc/codegen-options/index.html#target-cpu

要从命令行请求这些指令，使用 `-C target-cpu=native` 标志。例如：
```bash
RUSTFLAGS="-C target-cpu=native" cargo build --release
```

或者，要从 [`config.toml`] 文件（对一个或多个项目）请求这些指令，添加以下行：
```toml
[build]
rustflags = ["-C", "target-cpu=native"]
```
[`config.toml`]: https://doc.rust-lang.org/cargo/reference/config.html

这可以改善运行时速度，尤其是当编译器在代码中发现向量化机会时。

如果你不确定 `-C target-cpu=native` 是否工作正常，比较 `rustc --print cfg` 和 `rustc --print cfg -C target-cpu=native` 的输出，看后者是否正确检测到 CPU 特性。如果没有，可以使用 `-C target-feature` 来针对特定特性。

### 配置文件引导优化

配置文件引导优化（PGO）是一种编译模型：先编译程序，在示例数据上运行并收集性能分析数据，然后使用该数据引导程序的第二次编译。这可将运行时速度提高 10% 或更多。
[**示例 1**](https://blog.rust-lang.org/inside-rust/2020/11/11/exploring-pgo-for-the-rust-compiler.html)，
[**示例 2**](https://github.com/rust-lang/rust/pull/96978)。

这是一项需要一定设置工作的高级技术，但在某些情况下值得投入。详情见 [rustc PGO 文档][rustc PGO documentation]。此外，[`cargo-pgo`] 命令使使用 PGO（以及类似的 [BOLT]）优化 Rust 二进制文件更加容易。

遗憾的是，PGO 不支持托管在 crates.io 上并通过 `cargo install` 分发的二进制文件，这限制了其可用性。

[rustc PGO documentation]: https://doc.rust-lang.org/rustc/profile-guided-optimization.html
[`cargo-pgo`]: https://github.com/Kobzol/cargo-pgo
[BOLT]: https://github.com/llvm/llvm-project/tree/main/bolt

## 最小化二进制体积

以下构建配置选项主要用于最小化二进制体积。它们对运行时速度的影响各不相同。

### 优化级别

你可以通过在 `Cargo.toml` 文件中添加以下行来请求以最小化二进制体积为目标的[优化级别][optimization level]：
```toml
[profile.release]
opt-level = "z"
```
[optimization level]: https://doc.rust-lang.org/cargo/reference/profiles.html#opt-level

这也可能降低运行时速度。

另一种选择是 `opt-level = "s"`，以稍不激进的方式针对最小二进制体积。与 `opt-level = "z"` 相比，它允许[稍多内联][slightly more inlining]以及循环向量化。

[slightly more inlining]: https://doc.rust-lang.org/rustc/codegen-options/index.html#inline-threshold

### 在 `panic!` 时中止

如果你不需要在 panic 时展开栈，例如因为程序不使用 [`catch_unwind`]，可以告诉编译器在 panic 时直接[中止][abort on panic]。panic 时程序仍会产生回溯。

[`catch_unwind`]: https://doc.rust-lang.org/std/panic/fn.catch_unwind.html
[abort on panic]: https://doc.rust-lang.org/cargo/reference/profiles.html#panic

这可能略微减小二进制体积并略微提高运行时速度，甚至可能略微减少编译时间。在 `Cargo.toml` 文件中添加以下行：
```toml
[profile.release]
panic = "abort"
```

### 剥离符号

你可以通过在 `Cargo.toml` 中添加以下行，告诉编译器从 release 构建中[剥离][strip]符号：
```toml
[profile.release]
strip = "symbols"
```
[strip]: https://doc.rust-lang.org/cargo/reference/profiles.html#strip

[**示例**](https://github.com/nnethercote/counts/commit/53cab44cd09ff1aa80de70a6dbe1893ff8a41142)。

然而，剥离符号可能使编译后的程序更难调试和分析。例如，如果剥离了符号的程序 panic，产生的回溯可能包含比正常情况更少的有用信息。确切效果取决于平台。

release 构建不需要剥离调试信息。默认情况下，本地 release 构建不生成调试信息，标准库的调试信息在 release 构建中[自 Rust 1.77 起][since Rust 1.77]已自动剥离。

[since Rust 1.77]: https://blog.rust-lang.org/2024/03/21/Rust-1.77.0.html#enable-strip-in-release-profiles-by-default

### 其他思路

有关更高级的二进制体积最小化技术，请参阅优秀的 [`min-sized-rust`] 仓库中的全面文档。

[`min-sized-rust`]: https://github.com/johnthagen/min-sized-rust

## 最小化编译时间

以下构建配置选项主要用于最小化编译时间。

### 链接

编译时间的很大一部分实际上是链接时间，尤其是在小幅修改后重新构建程序时。在某些平台上，可以选择比默认更快的链接器。

一种选择是 [lld]，在 Linux 和 Windows 上可用。lld 自 [Rust 1.90 起][since Rust 1.90]在 Linux 上已成为默认链接器。在 Windows 上尚未成为默认，但对大多数用例应该有效。

[since Rust 1.90]: https://blog.rust-lang.org/2025/09/01/rust-lld-on-1.90.0-stable/

要从命令行指定 lld，使用 `-C link-arg=-fuse-ld=lld` 标志。例如：
```bash
RUSTFLAGS="-C link-arg=-fuse-ld=lld" cargo build --release
```

[lld]: https://lld.llvm.org/

或者，要从 [`config.toml`] 文件（对一个或多个项目）指定 lld，添加以下行：
```toml
[build]
rustflags = ["-C", "link-arg=-fuse-ld=lld"]
```
[`config.toml`]: https://doc.rust-lang.org/cargo/reference/config.html

有一个 [GitHub Issue] 跟踪对 lld 的完整支持。

[GitHub Issue]: https://github.com/rust-lang/rust/issues/39915#issuecomment-618726211

另一种选择是 [mold]，目前在 Linux 上可用。只需在上述说明中将 `lld` 替换为 `mold`。mold 通常比 lld 更快。
[**示例**](https://davidlattimore.github.io/posts/2024/02/04/speeding-up-the-rust-edit-build-run-cycle.html)。
它也更新，可能在某些情况下无法工作。

[mold]: https://github.com/rui314/mold

最后一种选择是 [wild]，目前仅在 Linux 上可用。它可能比 mold 更快，但成熟度较低。

[wild]: https://github.com/davidlattimore/wild

在 Mac 上，不需要替代链接器，因为系统链接器已经很快。

与本章其他选项不同，选择另一个链接器没有权衡。只要链接器对你的程序工作正常——除非你做一些不寻常的事情，否则这很可能是真的——替代链接器可以大幅加速而没有任何缺点。

### 禁用调试信息生成

尽管 release 构建提供最佳性能，许多人在开发时使用 dev 构建，因为它们构建更快。如果你使用 dev 构建但不常使用调试器，考虑禁用 debuginfo。这可以显著改善 dev 构建时间，最多可达 20–40%。
[**示例。**](https://kobzol.github.io/rust/rustc/2025/05/20/disable-debuginfo-to-improve-rust-compile-times.html)

要禁用调试信息生成，在 `Cargo.toml` 文件中添加以下行：
```toml
[profile.dev]
debug = false
```
注意，这意味着堆栈跟踪将不包含行信息。如果你想保留行信息，但不需要调试器的完整信息，可以使用 `debug = "line-tables-only"`，这仍能带来大部分编译时间收益。

### 实验性并行前端

如果你使用 nightly Rust，可以启用实验性的[并行前端][parallel front-end]。它可能以减少编译时间为代价增加编译时内存占用。它不会影响生成代码的质量。

[parallel front-end]: https://blog.rust-lang.org/2023/11/09/parallel-rustc.html

可以通过向 RUSTFLAGS 添加 `-Zthreads=N` 来实现，例如：
```bash
RUSTFLAGS="-Zthreads=8" cargo build --release
```

或者，要从 [`config.toml`] 文件（对一个或多个项目）启用并行前端，添加以下行：
```toml
[build]
rustflags = ["-Z", "threads=8"]
```
[`config.toml`]: https://doc.rust-lang.org/cargo/reference/config.html

可以使用 `8` 以外的值，但 `8` 往往是效果最好的数字。

在最佳情况下，实验性并行前端可将编译时间减少最多 50%。但效果差异很大，取决于代码及其构建配置的特性，对某些程序则没有编译时间改善。

### Cranelift 代码生成后端

如果你使用 nightly Rust，可以在[某些平台][some platforms]上启用 Cranelift 代码生成后端。它可能以减少生成代码质量为代价减少编译时间，因此建议用于 dev 构建而非 release 构建。

首先，用此 `rustup` 命令安装后端：
```bash
rustup component add rustc-codegen-cranelift-preview --toolchain nightly
```

要从命令行选择 Cranelift，使用 `-Zcodegen-backend=cranelift` 标志。例如：
```bash
RUSTFLAGS="-Zcodegen-backend=cranelift" cargo +nightly build
```

或者，要从 [`config.toml`] 文件（对一个或多个项目）指定 Cranelift，添加以下行：
```toml
[unstable]
codegen-backend = true

[profile.dev]
codegen-backend = "cranelift"
```
[`config.toml`]: https://doc.rust-lang.org/cargo/reference/config.html

更多信息请参阅 [Cranelift 文档][Cranelift documentation]。

[some platforms]: https://github.com/rust-lang/rustc_codegen_cranelift#platform-support
[Cranelift documentation]: https://github.com/rust-lang/rustc_codegen_cranelift

## 自定义 profile

除了 `dev` 和 `release` profile 外，Cargo 还支持[自定义 profile][custom profiles]。例如，如果你发现 dev 构建的运行时速度不足，而 release 构建的编译时间对日常开发来说太慢，创建一个介于 `dev` 和 `release` 之间的自定义 profile 可能很有用。

[custom profiles]: https://doc.rust-lang.org/cargo/reference/profiles.html#custom-profiles

## 总结

构建配置方面有许多选择。以下要点将上述信息总结为一些建议。

- 如果你想最大化运行时速度，考虑以下所有选项：`codegen-units = 1`、`lto = "fat"`、替代分配器以及 `panic = "abort"`。
- 如果你想最小化二进制体积，考虑 `opt-level = "z"`、`codegen-units = 1`、`lto = "fat"`、`panic = "abort"` 以及 `strip = "symbols"`。
- 无论哪种情况，如果不需要广泛的架构支持，考虑 `-C target-cpu=native`；如果与你的分发机制兼容，考虑 `cargo-pgo`。
- 如果你在支持更快链接器的平台上，始终使用更快的链接器，因为这样做没有任何缺点。
- 如果你需要额外帮助来做这些选择，使用 `cargo-wizard`。
- 对所有更改逐一进行基准测试，确保它们产生预期效果。

最后，[此 issue][this issue] 跟踪 Rust 编译器自身构建配置的演变。Rust 编译器的构建系统比大多数 Rust 程序更奇特、更复杂。尽管如此，此 issue 可能有助于展示如何将构建配置选择应用于大型程序。

[this issue]: https://github.com/rust-lang/rust/issues/103595
