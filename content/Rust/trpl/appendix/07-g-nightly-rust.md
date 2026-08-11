+++
title = "附录G Rust 是如何打造的与 “Nightly Rust”"
date = 2026-08-05T08:44:00+08:00
weight = 111
type = "docs"
description = "Rust 发布频道、火车模型、不稳定特性与 RFC 流程"
isCJKLanguage = true
draft = false
rust_version = "1.97.1"

+++

> 译文 · 基于 [The Rust Programming Language](https://doc.rust-lang.org/stable/book/)（rustc 1.97.1）

# G - Rust 是如何打造的与 “Nightly Rust” {#g-rust-nightly-rust}


> 原文链接: [https://doc.rust-lang.org/stable/book/appendix-07-nightly-rust.html](https://doc.rust-lang.org/stable/book/appendix-07-nightly-rust.html)


## 附录 G：Rust 是如何打造的与 “Nightly Rust”

　　本附录介绍 Rust 是如何打造的，以及这对你作为 Rust 开发者意味着什么。

### 稳定而不停滞

　　作为一门语言，Rust *非常*在意你的代码稳定性。我们希望 Rust 成为你可以赖以构建的坚实基础；如果一切总在变，那就不可能。与此同时，若不实验新特性，就可能要等到发布之后、再也改不动时，才发现重要缺陷。

　　我们对这个问题的解法，叫做「稳定而不停滞」（stability without stagnation），指导原则是：你永远不必害怕升级到新的稳定版 Rust。每次升级都应轻松，同时带来新功能、更少的缺陷，以及更快的编译。

### 发布频道与“火车”模型

　　Rust 的开发按 *火车时刻表* 运转。也就是说，所有开发都在 Rust 仓库的主分支上进行。发布遵循软件发布火车模型，Cisco IOS 等项目也用过这种模式。Rust 有三个 *发布频道*（release channels）：

- Nightly（每夜版）
- Beta（测试版）
- Stable（稳定版）

　　多数 Rust 开发者主要使用稳定频道；想尝试实验性新特性的人则可能使用 nightly 或 beta。

　　下面用一个例子说明开发与发布流程：假设 Rust 团队正在准备 Rust 1.5 的发布。该版本实际发布于 2015 年 12 月，但这里用它能提供真实的版本号。某个新特性加入了 Rust：一次新提交落到主分支。每天夜里都会产出一个新的 nightly 版 Rust。每一天都是发布日，这些发布由我们的发布基础设施自动创建。于是随着时间推移，每晚的发布看起来像这样：

```text
nightly: * - - * - - *
```

　　每六周，就该准备一次新发布了！Rust 仓库的 `beta` 分支从 nightly 使用的主分支拉出。现在有了两个发布：

```text
nightly: * - - * - - *
                     |
beta:                *
```

　　多数 Rust 用户并不主动使用 beta，但会在 CI 系统中针对 beta 做测试，帮助 Rust 发现可能的回归。与此同时，每晚仍有 nightly 发布：

```text
nightly: * - - * - - * - - * - - *
                     |
beta:                *
```

　　假设发现了回归。幸好我们有时间在回归溜进稳定版之前测试 beta！修复应用到主分支，于是 nightly 修好了；然后该修复被回移植到 `beta` 分支，并产出新的 beta 发布：

```text
nightly: * - - * - - * - - * - - * - - *
                     |
beta:                * - - - - - - - - *
```

　　第一个 beta 创建六周之后，就该出稳定版了！`stable` 分支从 `beta` 分支产生：

```text
nightly: * - - * - - * - - * - - * - - * - * - *
                     |
beta:                * - - - - - - - - *
                                       |
stable:                                *
```

　　好耶！Rust 1.5 完成了！不过我们忘了一件事：六周过去了，还需要 *下一个* 版本 Rust 1.6 的新 beta。因此在 `stable` 从 `beta` 拉出之后，下一版 `beta` 再次从 `nightly` 拉出：

```text
nightly: * - - * - - * - - * - - * - - * - * - *
                     |                         |
beta:                * - - - - - - - - *       *
                                       |
stable:                                *
```

　　之所以叫「火车模型」，是因为每六周就有一趟发布「发车」，但仍须途经 beta 频道，才能抵达稳定发布。

　　Rust 像发条一样每六周发布一次。如果你知道某次 Rust 发布的日期，也就知道下一次：六周之后。按六周排程的一个好处是：下一趟火车很快就来。若某特性错过了某次发布，也不必担心：很快又会有一趟！这有助于减轻在截止日期前硬塞进可能未打磨特性的压力。

　　得益于这一流程，你随时可以试用下一版 Rust，亲自验证升级是否轻松：若 beta 发布表现不如预期，可以向团队报告，并在下一次稳定发布之前修好！Beta 中出现破坏相对少见，但 `rustc` 终究是软件，缺陷确实存在。

### 维护周期

　　Rust 项目支持最新的稳定版。新的稳定版发布后，旧版本即到达生命周期终点（EOL）。这意味着每个版本大约支持六周。

### 不稳定特性 {#unstable-features}

　　这种发布模型还有一点需要说明：不稳定特性。Rust 用一种叫做「特性开关」（feature flags）的技术，决定某个发布中启用哪些特性。若某个新特性仍在积极开发中，它会落到主分支，因而进入 nightly，但会藏在 *特性开关* 后面。作为用户，若想试用尚在进行中的特性，可以这么做，但必须使用 nightly 版 Rust，并在源码中用相应标志选择启用。

　　若使用的是 beta 或稳定版 Rust，就不能使用任何特性开关。这正是我们能在把特性永远标为稳定之前，先获得实际使用反馈的关键：想尝试最前沿的人可以这么做；想要坚如磐石体验的人可以坚守稳定版，并确信代码不会被破坏。稳定而不停滞。

　　本书只包含稳定特性的信息，因为进行中的特性仍在变化，从本书撰写到它们在稳定构建中启用之间，内容肯定会有所不同。仅限 nightly 的特性文档可以在网上找到。

### Rustup 与 Nightly Rust 的角色

　　Rustup 让你很容易在不同的 Rust 发布频道之间切换，既可以全局切换，也可以按项目切换。默认会安装稳定版 Rust。例如要安装 nightly：

```console
$ rustup toolchain install nightly
```

　　也可以用 `rustup` 查看已安装的全部 *工具链*（Rust 发布及其相关组件）。下面是本书作者之一在 Windows 电脑上的例子：

```powershell
> rustup toolchain list
stable-x86_64-pc-windows-msvc (default)
beta-x86_64-pc-windows-msvc
nightly-x86_64-pc-windows-msvc
```

　　可以看到，稳定工具链是默认值。多数 Rust 用户大部分时间使用稳定版。你可能也想大部分时间用稳定版，但在某个特定项目上用 nightly，因为你关心某个前沿特性。为此，可以在该项目目录中使用 `rustup override`，把 nightly 工具链设为你在该目录时 `rustup` 应使用的工具链：

```console
$ cd ~/projects/needs-nightly
$ rustup override set nightly
```

　　现在，只要在 *~/projects/needs-nightly* 里调用 `rustc` 或 `cargo`，`rustup` 就会确保你使用的是 nightly Rust，而不是默认的稳定版。当你有很多 Rust 项目时，这很方便！

### RFC 流程与团队

　　那么，你如何了解这些新特性？Rust 的开发模型遵循 *征求意见（Request For Comments，RFC）流程*。若你希望改进 Rust，可以撰写一份提案，称为 RFC。

　　任何人都可以写 RFC 来改进 Rust；提案由 Rust 团队审阅与讨论，团队由许多主题子团队组成。[Rust 网站](https://www.rust-lang.org/governance)上有完整的团队列表，涵盖项目的各个领域：语言设计、编译器实现、基础设施、文档等等。相应团队会阅读提案与评论，写下自己的意见，最终就接受或拒绝该特性达成共识。

　　若特性被接受，会在 Rust 仓库开一个 issue，然后有人可以实现它。实现的人完全可能不是最初提出特性的人！实现就绪后，它会带着特性开关落到主分支，正如我们在[「不稳定特性」](#unstable-features)一节中讨论的那样。

　　一段时间之后，使用 nightly 的 Rust 开发者试用过新特性，团队成员会讨论该特性、它在 nightly 上的表现，并决定是否应进入稳定版 Rust。若决定推进，就会去掉特性开关，该特性现在视为稳定！它便会纳入新的 Rust 稳定版发布。
