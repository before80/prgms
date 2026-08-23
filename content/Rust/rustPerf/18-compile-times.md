+++
title = "18 编译时间"
date = 2026-08-23T13:57:00+08:00
weight = 19
type = "docs"
description = "缩短编译时间"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Rust Performance Book](https://nnethercote.github.io/perf-book/)

# 编译时间 {#compile-times}


> 原文链接: [https://nnethercote.github.io/perf-book/compile-times.html](https://nnethercote.github.io/perf-book/compile-times.html)


虽然本书主要关注提升 Rust 程序的运行性能，本节讨论缩短 Rust 程序的编译时间，因为这是许多人关心的相关话题。

[缩短编译时间]一节讨论了通过构建配置选择来缩短编译时间的方法。本节其余部分讨论需要修改程序代码才能缩短编译时间的方式。

[缩短编译时间]: ../2-build-configuration/#minimizing-compile-times
更多缩短编译时间的技巧，请参阅 Corrode 整理的[加快 Rust 编译时间的技巧][Tips] 完整列表。

[Tips]: https://corrode.dev/blog/tips-for-faster-rust-compile-times/

## 可视化

Cargo 提供可视化程序编译过程的功能。使用以下命令构建：
```text
cargo build --timings
```
完成后会打印一个 HTML 文件名。在网页浏览器中打开该文件。其中包含[甘特图]，展示程序中各 crate 之间的依赖关系。这能显示 crate 图中的并行程度，并提示是否应将拖慢编译的大型 crate 拆分。详见[文档][timings]。

[甘特图]: https://en.wikipedia.org/wiki/Gantt_chart
[timings]: https://doc.rust-lang.org/nightly/cargo/reference/timings.html

## 宏

有些宏会生成大量代码，这些代码随后需要编译时间。Rust 编译器的 `-Zmacro-stats` 标志有助于识别此类情况。

例如，若只想测量项目中的叶子 crate：
```text
cargo +nightly rustc -- -Zmacro-stats
```
编译器会打印过程宏和声明宏所生成代码量的信息。前者通常更值得关注。

或者，若要测量项目中所有 crate：
```text
RUSTFLAGS="-Zmacro-stats" cargo +nightly build
```
要查看生成的代码本身，可以使用 [cargo-expand]。

[cargo-expand]: https://github.com/dtolnay/cargo-expand

不必为生成少量代码的宏操心，但若某宏生成的代码量与手写代码相当，或许可以完全去掉该宏，或换成更轻量的替代方案。
[**示例**](https://nnethercote.github.io/2025/06/26/how-much-code-does-that-proc-macro-generate.html)。

或者，可以修改宏以生成更少代码。
[**示例 1**](https://github.com/bevyengine/bevy/issues/19873)，
[**示例 2**](https://nnethercote.github.io/2025/08/16/speed-wins-when-fuzzing-rust-code-with-derive-arbitrary.html)。

## LLVM IR

Rust 编译器使用 [LLVM] 作为后端。LLVM 的执行可能占编译时间的很大部分，尤其是当前端生成大量 [IR]、LLVM 优化耗时很长时。

[LLVM]: https://llvm.org/
[IR]: https://en.wikipedia.org/wiki/Intermediate_representation

可用 [`cargo llvm-lines`] 诊断这些问题，它会显示哪些 Rust 函数生成了最多 LLVM IR。泛型函数往往最重要，因为在大型程序中可能被实例化数十次甚至数百次。

[`cargo llvm-lines`]: https://github.com/dtolnay/cargo-llvm-lines/

若泛型函数导致 IR 膨胀，有几种修复方式。最简单的是让函数更小。
[**示例 1**](https://github.com/rust-lang/rust/pull/72166/commits/5a0ac0552e05c079f252482cfcdaab3c4b39d614)，
[**示例 2**](https://github.com/rust-lang/rust/pull/91246/commits/f3bda74d363a060ade5e5caeb654ba59bfed51a4)。

另一种方式是把函数的非泛型部分移到单独的非泛型函数中，该函数只会被实例化一次。是否可行取决于泛型函数的具体细节。可行时，非泛型函数常可整洁地写成泛型函数内的内部函数，如 [`std::fs::read`] 的代码所示：
```rust
pub fn read<P: AsRef<Path>>(path: P) -> io::Result<Vec<u8>> {
    fn inner(path: &Path) -> io::Result<Vec<u8>> {
        let mut file = File::open(path)?;
        let size = file.metadata().map(|m| m.len()).unwrap_or(0);
        let mut bytes = Vec::with_capacity(size as usize);
        io::default_read_to_end(&mut file, &mut bytes)?;
        Ok(bytes)
    }
    inner(path.as_ref())
}
```
[`std::fs::read`]: https://doc.rust-lang.org/std/fs/fn.read.html

[**示例**](https://github.com/rust-lang/rust/pull/72013/commits/68b75033ad78d88872450a81745cacfc11e58178)。

有时像 [`Option::map`] 和 [`Result::map_err`] 这样的通用工具函数会被多次实例化。用等价的 `match` 表达式替换它们有助于缩短编译时间。

[`Option::map`]: https://doc.rust-lang.org/std/option/enum.Option.html#method.map
[`Result::map_err`]: https://doc.rust-lang.org/std/result/enum.Result.html#method.map_err

这类改动对编译时间的影响通常较小，但偶尔可能很大。
[**示例**](https://github.com/servo/servo/issues/26585)。

此类改动也能减小二进制体积。
