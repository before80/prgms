+++
title = "02-Rust 版本"
date = 2026-07-30T14:49:00+08:00
weight = 33
type = "docs"
description = "rust-version 字段与 MSRV 相关行为"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Cargo Book](https://doc.rust-lang.org/cargo/)

# Rust 版本


> 原文链接: [https://doc.rust-lang.org/cargo/reference/rust-version.html](https://doc.rust-lang.org/cargo/reference/rust-version.html)


`rust-version` 字段是一个可选键，用于告诉 Cargo 你的包所支持的 Rust 工具链版本。

```toml
[package]
# ...
rust-version = "1.56"
```

Rust 版本必须是至少包含一个组成部分的裸版本号；不能包含 semver 运算符或预发布标识符。检查 Rust 版本时，编译器预发布标识符（如 `-nightly`）会被忽略。

> **MSRV：** 自 1.56 起生效

## 用途 {#uses}
**诊断：**

当你的包在不受支持的工具链上编译时，Cargo 会向用户报告错误。这样能明确支持期望，并避免报告语法无效或标准库功能缺失等较间接的诊断信息。这会影响包中的所有 [Cargo 目标](../01-cargo-targets/)，包括二进制、示例、测试套件、基准测试等。
用户可通过 `--ignore-rust-version` 标志选择在不受支持的工具链上构建包。


**开发辅助：**

`cargo add` 会自动选择与你的 `rust-version` 兼容的最新依赖版本需求。
若那不是最新版本，`cargo add` 会告知用户，以便其决定是保留该选择还是更新 `rust-version`。

[解析器](../../specifying-dependencies/03-dependency-resolution/#rust-version)在挑选依赖时可能会考虑 Rust 版本。

其他工具也可能利用该字段，例如 `cargo clippy` 的
[`incompatible_msrv` lint](https://rust-lang.github.io/rust-clippy/stable/index.html#incompatible_msrv)。

> **注意：** 可使用 `--ignore-rust-version` 选项忽略 `rust-version`。

## 支持期望 {#support-expectations}
以下为一般期望；部分包可能在文档中说明其未遵循这些期望的情况。

**完整（Complete）：**

在每个[特性（feature）](../../features/)下，所有功能（包括二进制与 API）在受支持的 Rust 版本上都可用。

**已验证（Verified）：**

包的功能已在其支持的 Rust 版本上验证，包括自动化测试。
另见我们的
[Rust 版本 CI 指南](../../../cargo-guide/08-continuous-integration/#verifying-rust-version)。

**可打补丁（Patchable）：**

在许可证允许时，
用户可以用你包的 fork [覆盖本地依赖](../../specifying-dependencies/01-overriding-dependencies/)。
在这种情况下，Cargo 可能会为被打补丁的依赖加载整个工作空间，该工作空间应能在受支持的 Rust 版本上工作，即使工作空间中其他包支持的 Rust 版本不同。

**依赖支持（Dependency Support）：**

为支持上述期望，
期望每个依赖的版本需求至少支持一个与你的 `rust-version` 兼容的版本。
然而，
**并不**期望依赖声明排除与你的 `rust-version` 不兼容的版本。
实际上，同时支持两者可让你在支持较旧 Rust 版本的用户与不需要旧版本的用户之间取得平衡。

## 设置与更新 Rust 版本 {#setting-and-updating-rust-version}
支持哪些 Rust 版本是一种权衡，涉及：
- 维护者不使用 Rust 工具链或其依赖的较新特性所付出的成本
- 能从包使用工具链较新特性中受益的用户所付出的成本，例如通过迁移到标准库特性来替代 polyfill 以缩短构建时间
- 支持较旧 Rust 版本的用户能否使用该包

> **注意：** [更改 `rust-version`](../../13-semver-compatibility/#env-new-rust) 被视为次要不兼容

> **建议：** 为支持哪些 Rust 版本以及何时更改制定策略，以便用户能与自身策略比较；
> 若不兼容，
> 再决定损失一般性改进、或存在不会被修复的阻塞性 bug 的风险是否可接受。
>
> 最简单的策略是始终使用最新的 Rust 版本。
>
> 取决于你的风险偏好，次简单的做法是继续支持你包中仍支持较旧 Rust 版本的旧主版本或次版本。

### 选择受支持的 Rust 版本 {#selecting-supported-rust-versions}
你的包的用户最可能按其支持的 Rust 版本跟踪：
- 其 Rust 工具链供应商的支持策略，例如 Rust 项目或某个 Linux 发行版
  - 注意：Rust 项目仅对最新版本提供 bug 修复与安全更新。
- 用户用新工具链重新验证其包的固定日程，例如每年首次发布、每 5 次发布一次。

此外，用户不太可能立即使用新的 Rust 版本，而需要时间发现并重新验证，也可能并未对齐到完全相同的日程。

版本策略示例：
- 「N-2」，表示「最新版本，并留有 2 次发布的更新宽限期」
- 每个偶数次发布，并留有 2 次发布的更新宽限期
- 本日历年内的每个版本，并留有一年更新宽限期

> **注意：** 要查找与当前项目现状兼容的最低 `rust-version`，可以使用第三方工具，例如 [`cargo-msrv`](https://crates.io/crates/cargo-msrv)。

### 更新时间线 {#update-timeline}
当你的策略规定不再需要支持某个 Rust 版本时，可以立即更新 `rust-version`，或在需要时再更新。

允许 `rust-version` 偏离你的策略，
会给用户更多升级宽限期。
然而，这过于不可预测，无法作为与用户所跟踪的 Rust 版本对齐的依据。

`rust-version` 偏离既定策略越远，
用户越可能推断出你并未打算的策略，
从而因期望落空而感到沮丧。

允许偏离时，
就存在「放弃受支持版本需要多充分的正当理由」这一问题。
每个人都可能得出合理但不同的正当理由；
就此展开讨论对相关方可能令人沮丧。
这会削弱希望避免此类冲突的人，
尤其是新贡献者或偶尔贡献者：他们要么觉得自己无权提出问题，
要么担心冲突会影响其变更被合并的机会。

### 工作空间中的多种策略 {#multiple-policies-in-a-workspace}
Cargo 允许在一个工作空间内支持多种策略。

在特定 Rust 版本下验证特定包可能变得复杂。
像 [`cargo-hack`](https://crates.io/crates/cargo-hack) 这样的工具可以提供帮助。

对于跨策略共享的任何依赖，
必须使用最低公共版本，因为 Cargo
[会统一 SemVer 兼容的版本](../../specifying-dependencies/03-dependency-resolution/#semver-compatibility)，
这可能限制 `rust-version` 较高的工作空间成员使用共享依赖的特性。

要允许用户对你某个工作空间成员的依赖打补丁，
工作空间中的每个包都需要能在工作空间所支持的最旧 Rust 版本上加载。

使用 [`incompatible-rust-versions = "fallback"`](../../06-configuration/#resolverincompatible-rust-versions) 时，
一个包的 Rust 版本可能影响为另一个具有不同 Rust 版本的包所选的依赖版本。
详见[解析器](../../specifying-dependencies/03-dependency-resolution/#rust-version)章节。

### 一种或多种策略 {#one-or-more-policies}
减轻支持较旧 Rust 版本弊端的一种方式，是将你的策略应用于你继续支持的包的旧主版本或次版本。
你可能仍需要一套策略，规定开发分支相对这些主/次版本发布分支所支持的 Rust 版本。

仅在「需要」时更新开发分支，有助于减少受支持的发布分支数量。

还存在哪些内容可以回移植到这些发布分支的问题。
在次版本之间回移植新功能时，
下一个可用版本会缺失该功能，这可能被视为破坏性变更，违反 SemVer。
回移植变更也带有引入 bug 的风险。

支持较旧版本是有成本的。
该成本取决于包内 bug 的风险与影响，以及可接受回移植的内容。
按需创建发布分支，并将回移植负担交给社区，是平衡该成本的方式。

目前尚无依赖管理工具能报告「非最新版本仍受支持」，
因而责任落在用户身上，需在文档中注意到这一点。

例如，一套 Rust 版本支持策略可以如下：
- 开发分支跟踪 Rust 项目的最新稳定版发布，在需要时更新
  - 更改 `rust-version` 时提升次版本号
- 项目支持本日历年内的每个版本，并再留一年宽限期
  - 支持某个仍受支持 Rust 版本的最后一个次版本将接收社区提供的 bug 修复
  - 修复必须回移植到开发分支与所需受支持 Rust 版本之间的所有受支持次版本发布
