+++
title = "4 性能分析"
date = 2026-08-23T13:57:00+08:00
weight = 5
type = "docs"
description = "剖析与定位热点"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Rust Performance Book](https://nnethercote.github.io/perf-book/)

# 性能分析 {#profiling}


> 原文链接: [https://nnethercote.github.io/perf-book/profiling.html](https://nnethercote.github.io/perf-book/profiling.html)


优化程序时，你还需要一种方法来确定程序的哪些部分是「热点」（执行频率足以影响运行时）且值得修改。最好通过性能分析来完成。

## 分析器

有许多不同的分析器可用，各有优劣。以下是在 Rust 程序上成功使用过的分析器的不完整列表。
- [perf] 是使用硬件性能计数器的通用分析器。[Hotspot] 和 [Firefox Profiler] 适合查看 perf 记录的数据。适用于 Linux。
- [Instruments] 是 macOS 上随 Xcode 提供的通用分析器。
- [Intel VTune Profiler] 是通用分析器。适用于 Windows、Linux 和 macOS。
- [AMD μProf] 是通用分析器。适用于 Windows 和 Linux。
- [samply] 是采样分析器，生成的 profile 可在 Firefox Profiler 中查看。适用于 Mac、Linux 和 Windows。
- [flamegraph] 是一个 Cargo 命令，使用 perf/DTrace 分析代码并以火焰图显示结果。适用于 Linux 以及所有支持 DTrace 的平台（macOS、FreeBSD、NetBSD，可能还有 Windows）。
- [Cachegrind] 和 [Callgrind] 提供全局、按函数和按源代码行的指令计数以及模拟的缓存和分支预测数据。适用于 Linux 和一些其他 Unix 系统。
- [DHAT] 适合找出代码中哪些部分导致大量分配，并提供峰值内存占用的洞察。也可用于识别对 `memcpy` 的热点调用。适用于 Linux 和一些其他 Unix 系统。[dhat-rs] 是实验性替代方案，功能稍弱且需要对 Rust 程序做少量修改，但适用于所有平台。
- [heaptrack] 和 [bytehound] 是堆分析工具。适用于 Linux。
- [`counts`] 支持临时性能分析，将 `eprintln!` 语句与基于频率的后处理相结合，适合深入了解代码的特定领域部分。适用于所有平台。
- [Coz] 执行*因果性能分析*以测量优化潜力，通过 [coz-rs] 提供 Rust 支持。适用于 Linux。

[perf]: https://perf.wiki.kernel.org/index.php/Main_Page
[Hotspot]: https://github.com/KDAB/hotspot
[Firefox Profiler]: https://profiler.firefox.com/
[Instruments]: https://developer.apple.com/forums/tags/instruments
[Intel VTune Profiler]: https://www.intel.com/content/www/us/en/developer/tools/oneapi/vtune-profiler.html
[AMD μProf]: https://developer.amd.com/amd-uprof/
[samply]: https://github.com/mstange/samply/
[flamegraph]: https://github.com/flamegraph-rs/flamegraph
[Cachegrind]: https://www.valgrind.org/docs/manual/cg-manual.html
[Callgrind]: https://www.valgrind.org/docs/manual/cl-manual.html
[DHAT]: https://www.valgrind.org/docs/manual/dh-manual.html
[dhat-rs]: https://github.com/nnethercote/dhat-rs/
[Valgrind]: https://valgrind.org/
[heaptrack]: https://github.com/KDE/heaptrack
[bytehound]: https://github.com/koute/bytehound
[`counts`]: https://github.com/nnethercote/counts/
[Coz]: https://github.com/plasma-umass/coz
[coz-rs]: https://github.com/plasma-umass/coz/tree/master/rust

## 调试信息

要有效分析 release 构建，你可能需要启用源代码行调试信息。为此，在 `Cargo.toml` 文件中添加以下行：
```toml
[profile.release]
debug = "line-tables-only"
```
有关 `debug` 设置的更多详情，请参阅 [Cargo 文档][Cargo documentation]。

[Cargo documentation]: https://doc.rust-lang.org/cargo/reference/profiles.html#debug

遗憾的是，即使完成上述步骤，你也不会获得标准库代码的详细分析信息。这是因为发布的 Rust 标准库版本未使用调试信息构建。

最可靠的方法是自己构建编译器和标准库，按照[这些说明][these instructions]操作，并在仓库根目录的 `bootstrap.toml` 文件中添加以下行：
 ```toml
[rust]
debuginfo-level = 1
```
这比较麻烦，但在某些情况下可能值得投入。

[these instructions]: https://github.com/rust-lang/rust

或者，不稳定的 [build-std] 特性让你将标准库作为程序正常编译的一部分进行编译，使用相同的构建配置。然而，标准库调试信息中的文件名不会指向源代码文件，因为此特性不会同时下载标准库源代码。因此，此方法对需要源代码才能完全工作的分析器（如 Cachegrind 和 samply）没有帮助。

[build-std]: https://doc.rust-lang.org/cargo/reference/unstable.html#build-std

## 帧指针

Rust 编译器可能优化掉帧指针，这会降低堆栈跟踪等分析信息的质量。要强制编译器使用帧指针，使用 `-C force-frame-pointers=yes` 标志。例如：
```bash
RUSTFLAGS="-C force-frame-pointers=yes" cargo build --release
```

或者，要从 [`config.toml`] 文件（对一个或多个项目）强制使用帧指针，添加以下行：
```toml
[build]
rustflags = ["-C", "force-frame-pointers=yes"]
```
[`config.toml`]: https://doc.rust-lang.org/cargo/reference/config.html

## 符号还原

Rust 使用一种名称修饰形式在编译代码中编码函数名。如果分析器不知道这一点，其输出可能包含以 `_ZN` 或 `_R` 开头的符号名，例如 `_ZN3foo3barE` 或
`_ZN28_$u7b$$u7b$closure$u7d$$u7d$E` 或
`_RMCsno73SFvQKx_1cINtB0_3StrKRe616263_E`

可以使用 [`rustfilt`] 手动还原此类名称。

[`rustfilt`]: https://crates.io/crates/rustfilt

如果你在分析时遇到符号还原问题，可能值得将[名称修饰格式][mangling format]从默认的旧格式更改为较新的 v0 格式。

[mangling format]: https://doc.rust-lang.org/rustc/codegen-options/index.html#symbol-mangling-version

要从命令行使用 v0 格式，使用 `-C symbol-mangling-version=v0` 标志。例如：
```bash
RUSTFLAGS="-C symbol-mangling-version=v0" cargo build --release
```

或者，要从 [`config.toml`] 文件（对一个或多个项目）请求这些设置，添加以下行：
```toml
[build]
rustflags = ["-C", "symbol-mangling-version=v0"]
```
[`config.toml`]: https://doc.rust-lang.org/cargo/reference/config.html
