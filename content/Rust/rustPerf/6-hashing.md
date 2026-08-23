+++
title = "6 哈希"
date = 2026-08-23T13:57:00+08:00
weight = 7
type = "docs"
description = "哈希算法与 Hasher"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Rust Performance Book](https://nnethercote.github.io/perf-book/)

# 哈希 {#hashing}


> 原文链接: [https://nnethercote.github.io/perf-book/hashing.html](https://nnethercote.github.io/perf-book/hashing.html)


`HashSet` 和 `HashMap` 是两种广泛使用的类型，有办法使它们更快。

## 替代哈希算法

默认哈希算法未作规定，但截至撰写时，默认算法是称为 [SipHash 1-3] 的算法。该算法质量高——提供强大的防碰撞保护——但相对较慢，尤其是对整数等短键而言。

[SipHash 1-3]: https://en.wikipedia.org/wiki/SipHash

如果性能分析显示哈希是热点，且 [HashDoS 攻击][HashDoS attacks]对你的应用不构成威胁，使用具有更快哈希算法的哈希表可以带来显著的速度提升。
- [`rustc-hash`] 提供 `FxHashSet` 和 `FxHashMap` 类型，可作为 `HashSet` 和 `HashMap` 的直接替代。其哈希算法质量较低但非常快，尤其对整数键而言，在 rustc 内部的表现优于所有其他哈希算法。（[`fxhash`] 是同一算法和类型的较旧、维护较少的实现。）
- [`fnv`] 提供 `FnvHashSet` 和 `FnvHashMap` 类型。其哈希算法质量高于 `rustc-hash`，但稍慢一些。
- [`ahash`] 提供 `AHashSet` 和 `AHashMap`。其哈希算法可利用部分处理器上可用的 AES 指令支持。

[HashDoS attacks]: https://en.wikipedia.org/wiki/Collision_attack
[`rustc-hash`]: https://crates.io/crates/rustc-hash
[`fxhash`]: https://crates.io/crates/fxhash
[`fnv`]: https://crates.io/crates/fnv
[`ahash`]: https://crates.io/crates/ahash

如果哈希性能对你的程序很重要，值得尝试多种替代方案。例如，在 rustc 中观察到以下结果。
- 从 `fnv` 切换到 `fxhash` 带来了[最高 6% 的加速][fnv2fx]。
- 尝试从 `fxhash` 切换到 `ahash` 导致了 [1–4% 的减速][fx2a]。
- 尝试从 `fxhash` 切换回默认哈希器导致了 [4–84% 的减速][fx2default]！

[fnv2fx]: https://github.com/rust-lang/rust/pull/37229/commits/00e48affde2d349e3b3bfbd3d0f6afb5d76282a7
[fx2a]: https://github.com/rust-lang/rust/issues/69153#issuecomment-589504301
[fx2default]: https://github.com/rust-lang/rust/issues/69153#issuecomment-589338446

如果你决定普遍使用某种替代方案，例如 `FxHashSet`/`FxHashMap`，很容易在某些地方误用 `HashSet`/`HashMap`。你可以[使用 Clippy][use Clippy]来避免此问题。

[use Clippy]: ../3-linting/#disallowing-types
有些类型不需要哈希。例如，你可能有一个包装整数的新类型，且整数值是随机的或接近随机的。对于此类类型，哈希值的分布与值本身的分布不会有太大差异。在这种情况下，[`nohash_hasher`] crate 可能很有用。

[`nohash_hasher`]: https://crates.io/crates/nohash-hasher

哈希函数设计是一个复杂的话题，超出了本书的范围。[`ahash` 文档][`ahash` documentation]中有很好的讨论。

[`ahash` documentation]: https://github.com/tkaitchuck/aHash/blob/master/compare/readme.md

## 按字节哈希

当你用 `#[derive(Hash)]` 标注类型时，生成的 `hash` 方法会分别哈希每个字段。对于某些哈希函数，将类型转换为原始字节并将字节作为流进行哈希可能更快。这对于满足某些属性（例如没有填充字节）的类型是可行的。

[`zerocopy`] 和 [`bytemuck`] crate 都提供 `#[derive(ByteHash)]` 宏，生成执行此类按字节哈希的 `hash` 方法。[`derive_hash_fast`] crate 的 README 对此技术有更多细节。

[`zerocopy`]: https://crates.io/crates/zerocopy
[`bytemuck`]: https://crates.io/crates/bytemuck
[`derive_hash_fast`]: https://crates.io/crates/derive_hash_fast

这是一项高级技术，性能影响高度依赖于哈希函数和被哈希类型的确切结构。请仔细测量。
