+++
title = "Tokio"
date = 2026-08-23T16:54:00+08:00
weight = 1
type = "docs"
description = ""
isCJKLanguage = true
draft = false

+++


> 原文链接: [https://tokio.rs/tokio/tutorial](https://tokio.rs/tokio/tutorial)

Tokio 是 Rust 编程语言的异步运行时。它提供了编写网络应用所需的构建块，并具备足够的灵活性，可面向从拥有数十个核心的大型服务器到小型嵌入式设备的广泛系统。

从高层次来看，Tokio 提供以下几个主要组件：

 - 用于执行异步代码的多线程运行时。
 - 标准库的异步版本。
 - 庞大的库生态系统。


当你以异步方式编写应用时，可以通过降低同时处理多项任务的成本来显著提升可扩展性。然而，异步 Rust 代码不会自行运行，因此你必须选择一个运行时来执行它。Tokio 库是使用最广泛的运行时，其使用量超过了所有其他运行时的总和。

此外，Tokio 还提供了许多实用工具。编写异步代码时，你不能使用 Rust 标准库提供的普通阻塞 API，而必须使用它们的异步版本。Tokio 提供了这些替代版本，并在合理之处镜像了 Rust 标准库的 API。

# Tokio 的优势

本节将概述 Tokio 的一些优势。

## 快速

Tokio _很快_，它构建在 Rust 编程语言之上，而 Rust 本身也很快。这是本着 Rust 的精神实现的，目标是让你无法通过手写等价代码来提升性能。

Tokio _可扩展_，它构建在 async/await 语言特性之上，而该特性本身也是可扩展的。在处理网络时，由于延迟的存在，单个连接的处理速度是有上限的，因此扩展的唯一方式是同时处理大量连接。借助 async/await 语言特性，增加并发操作的数量变得极其廉价，使你能够扩展到大量并发任务。

## 可靠

Tokio 使用 Rust 构建，Rust 让每个人都能构建可靠且高效的软件。[多项][microsoft][研究][chrome]发现，大约 70% 的高严重性安全漏洞源于内存不安全。使用 Rust 可以在你的应用中消除整类此类漏洞。

Tokio 还非常重视提供一致、可预期的行为。Tokio 的主要目标是让用户能够部署可预测的软件，使其日复一日地稳定运行，响应时间可靠，不会出现不可预测的延迟尖峰。

[microsoft]: https://www.zdnet.com/article/microsoft-70-percent-of-all-security-bugs-are-memory-safety-issues/
[chrome]: https://www.chromium.org/Home/chromium-security/memory-safety

## 简单

借助 Rust 的 async/await 特性，编写异步应用的复杂度已大幅降低。配合 Tokio 的实用工具和活跃的生态系统，编写应用变得轻而易举。

Tokio 在合理之处遵循标准库的命名约定。这使得将仅使用标准库编写的代码转换为使用 Tokio 编写的代码变得容易。凭借 Rust 强大的类型系统，轻松交付正确代码的能力无与伦比。

## 灵活

Tokio 提供多种运行时变体，从多线程、[工作窃取][work-stealing]运行时到轻量级单线程运行时。每种运行时都提供许多可调参数，供用户根据自身需求进行调优。

[work-stealing]: https://en.wikipedia.org/wiki/Work_stealing

# 何时不应使用 Tokio

尽管 Tokio 对许多需要同时处理大量任务的项目很有用，但也有一些用例并不适合使用 Tokio。

 - 通过在多个线程上并行运行来加速 CPU 密集型计算。Tokio 面向 IO 密集型应用，其中每个任务大部分时间都在等待 IO。如果你的应用所做的只是并行运行计算，你应该使用 [rayon]。话虽如此，如果你需要同时做这两件事，仍然可以「混合搭配」。请参阅[这篇博客文章中的实际示例][rayon-example]。
 - 读取大量文件。尽管对于只需读取大量文件的项目，Tokio 似乎很有用，但与普通线程池相比，Tokio 在这里并无优势。这是因为操作系统通常不提供异步文件 API。
 - 发送单个 Web 请求。Tokio 的优势在于你需要同时做很多事情的时候。如果你需要使用面向异步 Rust 的库（例如 [reqwest]），但不需要同时做很多事，应优先使用该库的阻塞版本，这样会使项目更简单。当然，使用 Tokio 仍然可行，但相比阻塞 API 并无实质优势。如果该库不提供阻塞 API，请参阅[与同步代码桥接的章节][bridging]。

[rayon]: https://docs.rs/rayon/
[rayon-example]: https://ryhl.io/blog/async-what-is-blocking/#the-rayon-crate
[reqwest]: https://docs.rs/reqwest/
[bridging]: https://tokio.rs/tokio/topics/bridging
# 获取帮助

任何时候，如果你遇到困难，都可以在 [Discord] 或 [GitHub 讨论区][disc] 寻求帮助。不必担心提出「初学者」问题。我们都是从零开始的，很乐意提供帮助。

[discord]: https://discord.gg/tokio
[disc]: https://github.com/tokio-rs/tokio/discussions
