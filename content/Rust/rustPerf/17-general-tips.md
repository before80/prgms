+++
title = "17 通用技巧"
date = 2026-08-23T13:57:00+08:00
weight = 18
type = "docs"
description = "跨语言通用原则"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Rust Performance Book](https://nnethercote.github.io/perf-book/)

# 通用技巧 {#general-tips}


> 原文链接: [https://nnethercote.github.io/perf-book/general-tips.html](https://nnethercote.github.io/perf-book/general-tips.html)


本书前面各节讨论了 Rust 特有的技巧。本节简要概述一些通用的性能原则。

只要避免明显陷阱（例如[使用非 release 构建]），Rust 代码通常既快又省内存，尤其若你习惯 Python、Ruby 等动态类型语言，或 Java、C# 等带垃圾回收的静态类型语言。

[使用非 release 构建]: ../2-build-configuration/
优化后的代码往往更复杂，编写也比未优化代码更费力。因此，只值得优化热点代码。

最大的性能提升往往来自算法或数据结构的改动，而非底层微优化。
[**示例 1**](https://github.com/rust-lang/rust/pull/53383/commits/5745597e6195fe0591737f242d02350001b6c590)，
[**示例 2**](https://github.com/rust-lang/rust/pull/54318/commits/154be2c98cf348de080ce951df3f73649e8bb1a6)。

编写能良好利用现代硬件的代码并不总是容易，但值得努力。例如，尽可能减少缓存未命中和分支预测失败。

多数优化只带来小幅加速。虽然单次小幅加速不易察觉，但若做得足够多，累积效果会很明显。

不同性能分析器各有长处，使用多种工具是好的做法。

当性能分析表明某函数是热点时，有两种常见加速方式：(a) 让该函数更快，和/或 (b) 减少调用次数。

消除愚蠢的拖慢往往比引入巧妙的加速更容易。

避免不必要的计算。惰性/按需计算常常是赢家。
[**示例 1**](https://github.com/rust-lang/rust/pull/36592/commits/80a44779f7a211e075da9ed0ff2763afa00f43dc)，
[**示例 2**](https://github.com/rust-lang/rust/pull/50339/commits/989815d5670826078d9984a3515eeb68235a4687)。

复杂的一般情况往往可以通过乐观地检查更简单、更常见的特殊情况来避免。
[**示例 1**](https://github.com/rust-lang/rust/pull/68790/commits/d62b6f204733d255a3e943388ba99f14b053bf4a)，
[**示例 2**](https://github.com/rust-lang/rust/pull/53733/commits/130e55665f8c9f078dec67a3e92467853f400250)，
[**示例 3**](https://github.com/rust-lang/rust/pull/65260/commits/59e41edcc15ed07de604c61876ea091900f73649)。
尤其当小尺寸占主导时，专门处理 0、1 或 2 个元素的集合往往是赢家。
[**示例 1**](https://github.com/rust-lang/rust/pull/50932/commits/2ff632484cd8c2e3b123fbf52d9dd39b54a94505)，
[**示例 2**](https://github.com/rust-lang/rust/pull/64627/commits/acf7d4dcdba4046917c61aab141c1dec25669ce9)，
[**示例 3**](https://github.com/rust-lang/rust/pull/64949/commits/14192607d38f5501c75abea7a4a0e46349df5b5f)，
[**示例 4**](https://github.com/rust-lang/rust/pull/64949/commits/d1a7bb36ad0a5932384eac03d3fb834efc0317e5)。

类似地，处理重复数据时，常可用简单的数据压缩：为常见值使用紧凑表示，对异常值回退到辅助表。
[**示例 1**](https://github.com/rust-lang/rust/pull/54420/commits/b2f25e3c38ff29eebe6c8ce69b8c69243faa440d)，
[**示例 2**](https://github.com/rust-lang/rust/pull/59693/commits/fd7f605365b27bfdd3cd6763124e81bddd61dd28)，
[**示例 3**](https://github.com/rust-lang/rust/pull/65750/commits/eea6f23a0ed67fd8c6b8e1b02cda3628fee56b2f)。

当代码处理多种情况时，测量各情况频率并优先处理最常见的情况。

处理具有高局部性的查找时，在数据结构前加一个小缓存可能有效。

优化后的代码往往结构不直观，因此说明性注释很有价值，尤其是引用性能分析测量结果的注释。像「该向量 99% 的时间只有 0 或 1 个元素，因此先处理这些情况」这样的注释很有启发性。
