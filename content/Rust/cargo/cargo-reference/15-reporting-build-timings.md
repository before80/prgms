+++
title = "15-报告构建耗时"
date = 2026-07-30T14:49:00+08:00
weight = 57
type = "docs"
description = "cargo build --timings 性能报告"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Cargo Book](https://doc.rust-lang.org/cargo/)

# 报告构建耗时 {#reporting-build-timings}


> 原文链接: [https://doc.rust-lang.org/cargo/reference/timings.html](https://doc.rust-lang.org/cargo/reference/timings.html)


`--timings` 选项可给出各次编译耗时的信息，并跟踪随时间变化的并发信息。

```sh
cargo build --timings
```

这会在 `target/cargo-timings/cargo-timing.html` 写入一份 HTML 报告。同时也会在同一目录写入一份文件名带时间戳的报告副本，以便查看较旧的运行结果。

## 阅读图表 {#reading-the-graphs}
输出中有两张表与两张图。

第一张表显示项目的构建信息，包括构建的单元数、最大并发数、构建时间，以及当前所用编译器的版本信息。

![build-info](../_src/images/build-info.png)

「unit」图显示每个单元随时间的持续时间。一个「单元（unit）」是一次编译器调用。图中有线条显示某个单元完成时「解锁」了哪些额外单元。也就是说，它显示因依赖全部完成而现在允许运行的新单元。将鼠标悬停在某个单元上可高亮这些线条。这有助于可视化依赖的关键路径。不同次运行之间可能有所变化，因为各单元可能以不同顺序完成。

「codegen」时间以淡紫色高亮。在某些情况下，构建流水线允许单元在其依赖执行代码生成时就开始。此信息并不总是显示（例如，二进制单元不会显示代码生成何时开始）。

「custom build」单元是 `build.rs` 脚本；运行时以橙色高亮。

![build-unit-time](../_src/images/build-unit-time.png)

第二张图显示 Cargo 随时间的并发情况。背景表示 CPU 使用率。三条线为：
- 「Waiting」（红色）——等待 CPU 槽位空出的单元数。
- 「Inactive」（蓝色）——等待其依赖完成的单元数。
- 「Active」（绿色）——当前正在运行的单元数。

![cargo-concurrency-over-time](../_src/images/cargo-concurrency-over-time.png)

注意：这并不显示编译器自身内部的并发。`rustc` 通过「job server」与 Cargo 协调，以保持在并发限制之内。这目前主要适用于代码生成阶段。

缩短编译时间的提示：
- 关注缓慢的依赖。
    - 检查它们是否有你可能希望禁用的特性（feature）。
    - 考虑尝试完全移除该依赖。
- 关注以不同版本多次构建的 crate。尝试从依赖图中移除较旧版本。
- 将大型 crate 拆成更小的部分。
- 若大量 crate 都被单个 crate 卡住，集中精力改进那一个 crate 以提高并行度。

最后一张表列出每个单元花费的总时间与「codegen」时间，以及各单元编译时启用的特性。
