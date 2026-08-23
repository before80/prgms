+++
title = "01-2021 路线图"
date = 2026-08-22T18:00:00+08:00
weight = 831
type = "docs"
description = "2021 年路线图"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Clippy Documentation](https://doc.rust-lang.org/nightly/clippy/)

# 2021 路线图 {#roadmap-2021}


> 原文链接: [https://doc.rust-lang.org/nightly/clippy/development/proposals/roadmap-2021.html](https://doc.rust-lang.org/nightly/clippy/development/proposals/roadmap-2021.html)


## 摘要

本路线图阐述了 Clippy 在 2021 年的计划：

- 提升可用性与可靠性
- 改善贡献者与维护者的体验
- 制定并明确流程

Clippy 团队成员将被分配来自上述一个或多个主题的任务。被分配任务的成员负责完成这些任务，可以通过亲自实现，或为感兴趣的贡献者提供指导来完成。

## 动机

随着 Rust 语言及其整个生态的持续成长，Clippy 的用户和贡献者也在不断增加。这对项目是好事，但也带来了挑战。其中一些挑战包括：

- 越来越多关于可靠性或可用性的问题出现
- 对一个小团队来说，流量难以应对
- 由于缺乏流程和/或团队成员的时间，较大的项目无法完成

此外，根据 [Rust Roadmap 2021]，每个团队都应定义清晰的流程，并在各团队之间统一。本路线图是迈向这一目标的第一步。

[Rust Roadmap 2021]: https://github.com/rust-lang/rfcs/pull/3037

## 说明

本节将说明 2021 年应完成的事项。需要指出的是，本文档聚焦于「做什么」，而非「怎么做」。后者将在后续的跟踪 issue 中处理，并分配给一位团队成员。

以下内容分为两个主要部分。第一部分涵盖面向用户的计划，第二部分涵盖内部计划。

### 面向用户

Clippy 应尽可能易于使用和配置。本节涵盖为改善 Clippy 在此方面状况而需实施的计划。

#### 可用性

以下介绍提升可用性的计划。

##### 在 `cargo check` 之后无输出

目前，在 `cargo check` 之后运行 `cargo clippy` 时不会产生任何输出。这尤其成问题，因为 `rust-analyzer` 正在兴起，它使用 `cargo check` 来检查代码。修复方案已经实现，但仍需推进至完成。这还包括稳定 `cargo clippy --fix` 命令，或在 `rustfix` 中支持多 span 建议。

- [#4612](https://github.com/rust-lang/rust-clippy/issues/4612)

##### `lints.toml` 配置

这是时不时会有人提起的需求：一个可复用的配置文件，用于定义 lint 级别。相关讨论往往没有具体结论，或止于「这需要一份 RFC」。而这正是需要做的：与 Cargo 团队一起撰写 RFC，并在某处以某种方式实现这样的配置文件。

- [#3164](https://github.com/rust-lang/rust-clippy/issues/3164)
- [cargo#5034](https://github.com/rust-lang/cargo/issues/5034)
- [IRLO](https://internals.rust-lang.org/t/proposal-cargo-lint-configuration/9135/8)

##### Lint 分组

越来越多关于在 Clippy 中管理 lint 的 issue 出现。lint 很难在确保无/少量误报（FP）的前提下实现。解决思路之一可能是引入更多 lint 分组，让用户能更好地管理 lint；或改进 lint 分类流程，使因误报而禁用 lint 的情况变得罕见。需要指出的是，Clippy 的 lint 比 `rustc` 的 lint 更不保守，这一点在未来不会改变。

- [#5537](https://github.com/rust-lang/rust-clippy/issues/5537)
- [#6366](https://github.com/rust-lang/rust-clippy/issues/6366)

#### 可靠性

以下介绍提升可靠性的计划。

##### 误报率

最坏情况下，新 lint 在 nightly 上最多只可用约 2 周，就会进入 beta，最终进入 stable。加之如今使用 nightly Rust 的人更少，带有大量误报的 lint 进入 stable 的概率更高。这会导致用户不满——最好情况下他们会禁用这些新 lint，最坏情况下他们会停止使用 Clippy。应制定并实施流程，防止这种情况发生。

- [#6429](https://github.com/rust-lang/rust-clippy/issues/6429)

### 内部

2020 年（末）表明，Clippy 必须考虑可用资源，尤其是项目的管理与维护。本节涉及影响团队成员和贡献者的问题。

#### 管理

2020 年 Clippy 的 open issue 超过 1000 个，open PR 通常在 25–35 个之间。这既是胜利也是负担。更多 issue 和 PR 意味着更多人对 Clippy 感兴趣并愿意贡献；另一方面，对团队成员意味着更多工作，对贡献者意味着更长的审阅等待时间。以下将描述如何改善团队成员和贡献者处境的计划。

##### 对团队成员的明确期望

根据 [Rust Roadmap 2021]，应产出一份说明成为团队成员意味着什么文档。这不应给团队成员施加更大压力，而应帮助他们和感兴趣的人了解期望是什么。有了这份文档，也更容易招募新团队成员，并可能鼓励有意加入的人主动联系。

##### 扩大团队规模

人越多，每个人的负担越轻。与团队成员期望文档一起，还应产出一份定义如何加入团队的流程文档。这也能提高团队的稳定性，以应对现有成员（暂时）退出。团队中也可以有不同角色，例如负责分诊的人与负责审阅的人。

##### 定期会议

其他团队有定期会议。Clippy 已足够大，值得也这样做。尤其是更多人加入团队后，同步会很重要。除了异步沟通（对各自独立开发 lint 很有效）之外，会议在固定时间提供同步交流的替代方式。当需要讨论较大事项（例如本路线图中的项目）时尤其有用。起步时，在 Rust sync 之前每两周开一次会可能比较合适。

##### 分诊

为应对 open issue 的涌入，应制定 issue 和 PR 的分诊流程。正式而言，Clippy 遵循 Rust 的分诊流程，但目前无人强制执行。可以通过跨项目共享分诊团队，或实现简化分诊的仪表盘/工具来改进。

#### 开发

改善开发者与贡献者体验是 Clippy 团队持续在做的事。不过，有些事项可能需要特别关注与规划。以下列出这些主题。

##### 新旧 Lint 的流程

如上所述，对新 lint 进行分类相当困难，因为有问题的 lint 进入 stable 的概率相当高。应实施如何对 lint 分类的流程。此外，应开发测试体系，找出哪些 lint 在真实代码中目前有问题，以便修复或禁用。

- [#6429 (comment)](https://github.com/rust-lang/rust-clippy/issues/6429#issuecomment-741056379)
- [#6429 (comment)](https://github.com/rust-lang/rust-clippy/issues/6429#issuecomment-741153345)

##### 流程

与上一点相关，应实施提出和讨论重大变更的流程。lint 何时默认启用或禁用也没有明确定义。上文提到的测试体系也能在这方面有所帮助。

##### 开发工具

已有 `cargo dev`，使 Clippy 开发更轻松、更愉快。仍可扩展，以覆盖开发流程的更多环节。

- [#5394](https://github.com/rust-lang/rust-clippy/issues/5394)

##### 贡献者指南

类似于介绍如何使用 Clippy 的 Clippy Book，一本关于如何为 Clippy 做贡献的书可能对新老贡献者都有帮助。Clippy 仓库中已有 `doc` 目录，可以将其转为 `mdbook`。

##### `rustc` 集成

最近 Clippy 通过 `git subtree` 集成进了 `rust-lang/rust` 仓库，使两个仓库之间的同步更容易。仍待改进的事项（`#[non_exhaustive]` 列表）包括：

1. 使用与 `rustc` 相同的 `rustfmt` 版本和配置。
2. 让 `cargo dev` 在 Rust 仓库中也能像在 Clippy 仓库中一样工作，例如 `cargo dev bless` 或 `cargo dev update_lints`。甚至为 Rust 仓库添加更多有用功能，例如 `cargo dev deprecate`。
3. 更简便的同步流程。当前的 `subtree` 方案并不理想。

### 优先级

对 Clippy 用户而言，最紧迫的当然是面向用户的问题。因此应优先处理这些问题，但不要忽视本文档中列出的内部事项。

将 warn/deny-by-default lint 的误报率控制住应拥有最高优先级。其他面向用户的问题也应高优先级，但不应阻碍处理内部问题。

为更好地管理即将到来的项目，基本的内部流程（如会议、跟踪 issue 和文档）应尽早建立。它们甚至可能是妥善管理面向用户项目所必需的。

## 先例

### Rust 路线图

Rust 的路线图流程由 [RFC 1728] 于 2016 年建立。此后每年都会发布一份路线图，定义未来数年的更大计划。今年的路线图见[此处][Rust Roadmap 2021]。

[RFC 1728]: https://rust-lang.github.io/rfcs/1728-north-star.html

## 缺点

### 路线图过大

本路线图相当庞大，本文档中列出的并非所有事项都能在 2021 年内完成。由于这是 Clippy 的第一份路线图，2021 年末仍有未完成任务是可以接受的，但应在 2022 路线图中重新审阅。
