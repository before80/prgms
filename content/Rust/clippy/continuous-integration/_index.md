+++
title = "06-持续集成"
date = 2026-08-22T18:00:00+08:00
weight = 60
type = "docs"
description = "在 CI 中运行 Clippy"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Clippy Documentation](https://doc.rust-lang.org/nightly/clippy/)

# 持续集成 {#continuous-integration}


> 原文链接: [https://doc.rust-lang.org/nightly/clippy/continuous_integration/index.html](https://doc.rust-lang.org/nightly/clippy/continuous_integration/index.html)


建议在 CI 中使用 `-Dwarnings` 运行 Clippy，使 Clippy lint 导致 CI 无法通过。若要对所有 `cargo` 命令（而不仅是 `cargo clippy`）将警告视为错误，可设置环境变量 `RUSTFLAGS="-Dwarnings"`。

建议使用与编译 crate 相同的工具链中的 Clippy，以获得最大兼容性。例如，若 crate 使用 `stable` 工具链编译，也应使用 `stable` 版 Clippy。

> 注意：新的 Clippy lint 会首先添加到 `nightly` 工具链。若你希望帮助改进 Clippy 且 CI 资源充足，请考虑在 CI 中添加 `nightly` Clippy 检查，并将误报等问题反馈给我们。这样我们可以在 bug 进入 stable 之前尽早修复。

本章概述如何在不同常用 CI 提供商上使用 Clippy。
