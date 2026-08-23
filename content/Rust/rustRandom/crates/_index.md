+++
title = "2 crate 家族"
date = 2026-08-23T16:44:00+08:00
weight = 10
type = "docs"
description = ""
isCJKLanguage = true
draft = false

+++


> 原文链接: [https://rust-random.github.io/book/crates.html](https://rust-random.github.io/book/crates.html)

<pre><code class="language-plain">                                           ┌ <a href="https://docs.rs/statrs/">statrs</a>
                                           ├ <a href="https://docs.rs/rand_distr/">rand_distr</a>
          <a href="https://docs.rs/rand_core/">rand_core</a> ┬───────────────┬ <a href="https://docs.rs/rand/">rand</a> ┘
                    ├ <a href="https://docs.rs/chacha20/">chacha20</a> ─────┤
                    ├ <a href="https://docs.rs/getrandom/">getrandom</a> ────┘
                    ├ <a href="https://docs.rs/rand_chacha/">rand_chacha</a>
                    ├ <a href="https://docs.rs/rand_hc/">rand_hc</a>
                    ├ <a href="https://docs.rs/rand_isaac/">rand_isaac</a>
                    ├ <a href="https://docs.rs/rand_jitter/">rand_jitter</a>
                    ├ <a href="https://docs.rs/rand_pcg/">rand_pcg</a>
                    ├ <a href="https://docs.rs/rand_sfc/">rand_sfc</a>
                    ├ <a href="https://docs.rs/rand_seeder/">rand_seeder</a>
                    ├ <a href="https://docs.rs/rand_xorshift/">rand_xorshift</a>
                    └ <a href="https://docs.rs/rand_xoshiro/">rand_xoshiro</a>
</code></pre>

## 接口

[`rand_core`] 定义了 [`RngCore`] 及其他核心 trait，以及若干用于实现 RNG 的辅助工具。

[`getrandom`] crate 提供了围绕平台特定随机数源的低级 API。

## 伪随机生成器

以下 crate 实现了伪随机数生成器（参见[我们的 RNG](../guide/3.4-our-rngs/)）：

-   [`chacha20`] 提供使用 ChaCha 密码的生成器（通过 `chacha` 特性在 [`rand`] 内部使用）
-   [`rand_chacha`] 也提供 ChaCha 密码生成器（为此目的的 `chacha20` 前身；为兼容性而保留）
-   [`rand_hc`] 实现使用 HC-128 密码的生成器
-   [`rand_isaac`] 实现 ISAAC 生成器
-   [`rand_pcg`] 实现一小部分 PCG 生成器
-   [`rand_sfc`] 实现 SFC（Small Fast Counter）生成器
-   [`rand_xorshift`] 实现基本的 Xorshift 生成器
-   [`rand_xoshiro`] 实现 SplitMix 和 Xoshiro 生成器

例外地，[`SmallRng`] 直接在 [`rand`] 中实现。

此外，[`rand_jitter`] 提供基于抖动的熵源，[`rand_seeder`] 从任意可哈希数据派生种子（用作[播种 RNG](../guide/3.5-seeding-rngs/) 中的构建块）。

## rand（主 crate）

[`rand`] crate 旨在方便使用常见的随机数功能。这涉及多个方面：

-   [`rngs`] 模块提供若干便捷的生成器
-   [`distr`] 模块涉及随机值的采样
-   [`seq`] 模块涉及从序列中采样和打乱
-   [`Rng`] trait 提供若干生成随机值的便捷方法
-   [`random`] 函数提供一次调用即可生成的便捷方式

## 分布

[`rand`] crate 仅实现从最常见的随机数分布中采样：均匀分布和加权采样。对于其他一切，

-   [`rand_distr`] 提供从多种其他分布中快速采样，包括正态（高斯）、二项、泊松、单位圆等
-   [`statrs`] 是 C# Math.NET 库的移植，实现了许多相同的分布（或多或少），以及 PDF 和 CDF 函数、*error*、*beta*、*gamma* 和 *logistic* 特殊函数，外加若干实用工具。（为清晰起见，[`statrs`] 不是 Rand 库的一部分。）


[`rand_core`]: https://docs.rs/rand_core/
[`rand`]: https://docs.rs/rand/
[`rand_distr`]: https://docs.rs/rand_distr/
[`statrs`]: https://docs.rs/statrs/
[`getrandom`]: https://docs.rs/getrandom/
[`chacha20`]: https://docs.rs/chacha20/
[`rand_pcg`]: https://docs.rs/rand_pcg/
[`rand_xoshiro`]: https://docs.rs/rand_xoshiro/
[`log`]: https://docs.rs/log/
[`serde`]: https://serde.rs/
[`rand_chacha`]: https://docs.rs/rand_chacha/
[`rand_hc`]: https://docs.rs/rand_hc/
[`rand_isaac`]: https://docs.rs/rand_isaac/
[`rand_jitter`]: https://docs.rs/rand_jitter/
[`rand_sfc`]: https://docs.rs/rand_sfc/
[`rand_seeder`]: https://docs.rs/rand_seeder/
[`rand_xorshift`]: https://docs.rs/rand_xorshift/

[`RngCore`]: https://docs.rs/rand_core/latest/rand_core/trait.RngCore.html

[`rngs`]: https://docs.rs/rand/latest/rand/rngs/
[`distr`]: https://docs.rs/rand/latest/rand/distr/
[`seq`]: https://docs.rs/rand/latest/rand/seq/
[`Rng`]: https://docs.rs/rand/latest/rand/trait.Rng.html
[`random`]: https://docs.rs/rand/latest/rand/fn.random.html

[`SmallRng`]: https://docs.rs/rand/latest/rand/rngs/struct.SmallRng.html
