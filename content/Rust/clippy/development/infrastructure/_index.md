+++
title = "12-基础设施"
date = 2026-08-22T18:00:00+08:00
weight = 82
type = "docs"
description = "Clippy 项目基础设施"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Clippy Documentation](https://doc.rust-lang.org/nightly/clippy/)

# 基础设施 {#infrastructure}


> 原文链接: [https://doc.rust-lang.org/nightly/clippy/development/infrastructure/index.html](https://doc.rust-lang.org/nightly/clippy/development/infrastructure/index.html)


要通过 `rustup` 分发 Clippy，需要一定的基础设施。本章说明为达成这一目标需要维护的 Clippy 基础设施各部分。

最重要的部分是 `rust-lang/rust` 仓库与 Clippy 仓库之间每两周进行一次的同步。该流程在[在 Clippy 与 `rust-lang/rust` 之间同步变更](sync.md)一节中说明。

新的 Clippy 版本与每次 Rust 稳定版发布一起发布，即每六周一次。发布流程见[发布新版 Clippy](release.md)一节。在发布周期中，还需为下一版撰写 changelog 条目，格式与做法见[更新变更日志](changelog_update.md)一节。

> _注意：_ Clippy CI 也应在本章说明，但目前仍为 TODO。
