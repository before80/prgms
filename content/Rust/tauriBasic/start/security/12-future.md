+++
title = "12 未来工作"
date = 2026-09-25T21:31:08+08:00
weight = 12
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

> 原文链接: [https://tauri.app/security/future/](https://tauri.app/security/future/)

本节介绍我们已着手或希望在未来处理的主题，目的是让 Tauri 应用更加安全。
如果你对这些主题感兴趣，或者已有相关知识，我们随时欢迎通过 GitHub 或 Discord 等社区平台加入新的贡献者和建议。

### 二进制分析

为了让渗透测试人员、审计人员和自动化安全检查能够正常开展工作，即便只是从编译后的二进制文件中提供洞察也非常有价值。并非所有公司都开源，或愿意为审计、红队和其它安全测试提供源代码。

另一个常被忽视的点是：提供内置元数据能让你的应用用户大规模地审计自身系统中的已知漏洞，而不必投入大量时间和精力。

如果你的威胁模型依赖“隐匿式安全”，本节提供的一些工具和观点或许能让你重新考虑。

对 Rust 来说，有 `cargo-auditable` 可以生成 [SBOM](https://en.wikipedia.org/wiki/Software_supply_chain)，并在不破坏可复现构建的前提下提供二进制文件精确的 crate 版本与依赖。

对前端技术栈，我们尚未发现类似的方案，因此从二进制文件中提取前端资源应当是一个直接的过程。之后应当可以使用 `npm audit` 之类的工具。已经有[博客文章](https://infosecwriteups.com/reverse-engineering-a-native-desktop-application-tauri-app-5a2d92772da5)介绍这个过程，但还没有简单易用的工具。

我们计划在启用某些特性编译 Tauri 应用时提供这类工具，或让资源提取变得更容易。

要使用 [Burpsuite](https://portswigger.net/burp)、[Zap](https://www.zaproxy.org/) 或 [Caido](https://caido.io/) 之类的渗透测试工具，必须能拦截来自 webview 的流量并让它经过测试代理。目前 Tauri 没有内置方式做到这一点，但已有工作在推进以简化该流程。

所有这些工具都能在无法访问源代码的情况下对 Tauri 应用进行恰当的测试与检查，在构建 Tauri 应用时都应加以考虑。

我们计划在未来进一步支持并实现相关特性。

### WebView 加固

在 Tauri 当前的威胁模型和边界下，我们无法为 WebView 自身添加更多安全约束。由于它是我们技术栈中最大的一块，而且是用内存不安全的语言编写的，我们计划研究并考虑进一步沙箱化和隔离 webview 进程的方法。

我们将评估内置与外部的沙箱化方法，以降低攻击影响并强制系统访问只能走 IPC 桥。我们相信这部分技术栈是薄弱环节，不过当前一代 WebView 在加固和漏洞利用韧性方面正在改善。

### 模糊测试

为了更高效并简化对 Tauri 应用进行模糊测试的流程，我们打算进一步实现 mock 运行时和其它工具，让针对单个 Tauri 应用的配置与构建更容易。

Tauri 支持众多操作系统和 CPU 架构，而应用通常只有很少甚至没有可能内存不安全的代码。
现有的模糊测试工具与库都不支持这些不常见的用例，因此我们需要自行实现，并支持 [libAFL](https://github.com/AFLplusplus/LibAFL) 等现有库，来构建 Tauri 模糊测试框架。

目标是让 Tauri 应用开发者能够方便高效地进行模糊测试。
