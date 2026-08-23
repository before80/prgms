+++
title = "4.2-与 Criterion.rs 对比"
date = 2026-08-22T20:00:00+08:00
weight = 26
type = "docs"
description = "Iai 与 Criterion.rs 对比"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Criterion.rs Documentation](https://bheisler.github.io/criterion.rs/book/)

# 与 Criterion.rs 对比 {#comparison-to-criterion}


> 原文链接: [https://bheisler.github.io/criterion.rs/book/iai/comparison.html](https://bheisler.github.io/criterion.rs/book/iai/comparison.html)


### 与 Criterion-rs 对比

我希望 Iai 成为 Criterion-rs 的补充，而非竞争对手。这两个项目以不同方式测量不同事物，各有优缺点和限制，因此对大多数项目而言，最佳做法是两者兼用。

以下是重要差异的概览：
- **临时缺点：** 目前 Iai 缺少 Criterion-rs 的许多功能，包括报告和任何形式的配置。
    - 当前计划是为 [Cargo-criterion] 添加对 Iai 基准测试进行配置和报告的支持。
- **优点：** Iai 能够可靠地检测到比 Criterion-rs 小得多的性能变化。
- **优点：** Iai 可以在嘈杂的 CI 环境甚至 GitHub Actions 或 Travis-CI 等云 CI 提供商中可靠工作，而 Criterion-rs 则无法做到。
- **优点：** Iai 还能在无需额外工作的情况下生成基准测试的性能分析输出。
- **优点：** 尽管 Cachegrind 会带来相当大的运行时开销，但每个基准测试仅运行一次通常仍比 Criterion-rs 的统计测量更快。
- **混合：** 由于 Iai 能检测到如此小的变化，它可能会报告由函数在内存中的顺序及其他编译器细节变化引起的性能差异。
- **缺点：** Iai 的测量值仅与挂钟时间（wall-clock time，这通常才是你真正关心的）相关，而 Criterion-rs 直接测量挂钟时间。
- **缺点：** Iai 无法将设置代码从测量中排除，而 Criterion-rs 可以。
- **缺点：** 由于 Cachegrind 不测量系统调用，IO 时间无法被准确测量。
- **缺点：** 由于 Iai 仅运行一次基准测试，它无法测量性能波动，例如由操作系统线程调度或哈希表随机化引起的波动。
- **限制：** Iai 只能在 Valgrind 支持的平台使用。值得注意的是，这不包括 Windows。

对于在 CI 中运行的基准测试（尤其是如果你在云 CI 的拉取请求中检查性能回归），应使用 Iai。对于在 Windows 或 Valgrind 不支持的其他平台上进行基准测试，应使用 Criterion-rs。对于其他情况，我建议两者兼用。Iai 提供更高精度，且能更好地扩展到更大的基准测试；Criterion-rs 则允许排除设置时间，并提供有关代码实际耗时以及线程或哈希表随机化等非确定性因素对其影响程度的信息。不过，如果你绝对只能二选一，Iai 可能是更合适的选择。

[Cargo-criterion]: https://github.com/bheisler/cargo-criterion
