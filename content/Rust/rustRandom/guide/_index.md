+++
title = "3 用户指南"
date = 2026-08-23T16:44:00+08:00
weight = 20
type = "docs"
description = ""
isCJKLanguage = true
draft = false

+++


> 原文链接: [https://rust-random.github.io/book/guide.html](https://rust-random.github.io/book/guide.html)

本节尝试解释本库中使用的一些概念。

1.  [在新 crate 中入门](3.1-getting-started/)
1.  [什么是随机数据？什么是随机性？](3.2-random-data/)
1.  [有哪些类型的随机生成器？](3.3-types-of-generators/)
1.  [Rand 提供了哪些随机数生成器？](3.4-our-rngs/)
1.  [PRNG 播种与可复现性](3.5-seeding-rngs/)
1.  [并行 RNG](3.6-parallel-rngs/)
1.  [将随机数据转换为有用的值](3.7-random-values/)
1.  [分布：更精细地控制随机值](3.8-random-distributions/)
1.  [随机过程：无放回抽样](3.9-random-processes/)
1.  [序列](3.10-sequences/)
1.  [错误处理](3.11-error-handling/)
1.  [测试使用 RNG 的函数](3.12-testing-randomized-functions/)

## 导入项（prelude）

从 Rand 导入项最便捷的方式是使用 [`prelude`]。
它包含了 Rand 最重要的部分，且仅包含不太可能引起命名冲突的项。

请注意，相对于旧版本，Rand 0.5 显著改变了模块组织与内容。在可能的情况下保留了旧名称（但在文档中已隐藏），不过这些名称将来会被移除。因此我们建议在导入时迁移到使用 prelude 或新的模块组织。


## 更多示例

如需一些灵感，请参阅以下示例应用：

- [蒙特卡洛估算 π](
  https://github.com/rust-random/rand/blob/master/examples/monte-carlo.rs)
- [蒙提霍尔问题](
   https://github.com/rust-random/rand/blob/master/examples/monty-hall.rs)

[`prelude`]: https://docs.rs/rand/latest/rand/prelude/
