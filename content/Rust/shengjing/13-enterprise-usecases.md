+++
title = "13-企业落地实践"
date = 2026-07-28T14:49:00+08:00
weight = 130
type = "docs"
description = "Rust 降本增效案例：AWS、Tenable、Discord 实践精要"
isCJKLanguage = true
draft = false

+++

> 精要笔记 · 基于 [Rust语言圣经](https://beatai.org/rust-course/)「企业落地实践」

# Rust 的使用案例

Rust 基金会成立后，全球落地案例快速增长。本章通过精选案例说明：**Rust 能解决哪些企业痛点，以及落地时可期待的收益**。

## 用 Rust 节约企业成本

> 参考 AWS 博文：[Sustainability with Rust](https://aws.amazon.com/cn/blogs/opensource/sustainability-with-rust/)（译文已精简）

2020 年起 Rust 基金会（AWS、Google、华为、Microsoft、Mozilla 等）推动生态发展。AWS 内部 Rust 已是 **first-class** 语言，用于：

- [Firecracker](https://firecracker-microvm.github.io/) — Lambda 等无服务器计算的虚拟化底座
- S3、EC2、CloudFront 等核心服务
- [Bottlerocket](https://aws.amazon.com/bottlerocket/) — 容器专用 Linux 发行版

### 云计算与能源效率

全球数据中心年耗电约 **200 TWh**（≈全球 1%）。总量近十年未暴涨，得益于能效提升与 workload 向云迁移；但 AI/ML 等负载增长使「继续优化」仍紧迫。

除可再生能源外，**选用高能效语言重写基础软件**是重要杠杆。

### 编程语言能效对比

[学术研究](https://greenlab.di.uminho.pt/wp-content/uploads/2017/10/sleFinal.pdf) 对 27 种语言、10 个场景测试：**C 与 Rust 能效显著领先**（相对 Java 约省 98%，相对 Python 约 76 倍）。

为何不选 C？Linus Torvalds 称 C「像拿着链锯玩耍」；Rust 已入 Linux 内核官方语言（此前仅 C）。同思路下，约 **70%+** 的 C/C++ 高危 CVE 可在 Rust 中规避；ISRG 正推动 curl 等基础设施迁移。

性能上 Rust 与 C 接近，且显著快于多数托管语言。

### 成功案例

#### Tenable

[用 Rust 优化 sidecar agent](https://medium.com/tenable-techblog/optimizing-700-cpus-away-with-rust-dc7a000dbdb2)：原 JavaScript 方案在业务增长后性能下降；Rust 重写后**延迟降约 50%**，CPU/内存占用大幅下降 → 硬件与能耗成本双降。

#### Discord

[从 Go 迁移关键服务到 Rust](https://discord.com/blog/why-discord-is-switching-from-go-to-rust)：Go GC 在对象频繁分配时造成尾延迟尖峰；Rust 版消除 GC 抖动，**P99 响应时间降一个数量级以上**，并减少服务器数量。

**共性**：为性能选型 Rust，同时意外获得能效与成本收益。

## 落地启示

| 维度 | Rust 价值 |
|------|-----------|
| 性能 | 接近 C，无 GC 停顿 |
| 安全 | 编译期消除大量内存/并发 bug |
| 成本 | 更低 CPU/内存 → 更少机器与电费 |
| 适用场景 | 基础设施、Sidecar、高并发网络服务 |

更多案例见源码：`shengJing/_src/src/usecases/`。
