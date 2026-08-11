+++
title = "8.10 练习"
date = 2026-08-11T11:30:00+08:00
weight = 290
type = "docs"
description = "09-练习 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/exercises/chromium/third-party.html](https://google.github.io/comprehensive-rust/exercises/chromium/third-party.html)

# 8.10 练习

把 [uwuify][0] 加到 Chromium，并关闭该 crate 的[默认 features][1]。假设该 crate 将用于发布版 Chromium，但不会用于处理不可信输入。

（下一个练习我们将从 Chromium 使用 uwuify，但若你愿意，可以跳过先行完成。或者，你可以创建一个使用 `uwuify` 的新 [`rust_executable` 目标][2]。）

> 学员将需要下载大量传递依赖。
>
> 总共需要的 crate 是：
>
> - `instant`，
> - `lock_api`，
> - `parking_lot`，
> - `parking_lot_core`，
> - `redox_syscall`，
> - `scopeguard`，
> - `smallvec`，以及
> - `uwuify`。
>
> 若学员下载的比这还多，他们很可能忘记关闭默认 features。
>
> 感谢 [Daniel Liu][3] 提供此 crate！


[0]: https://crates.io/crates/uwuify
[1]: https://doc.rust-lang.org/cargo/reference/features.html#the-default-feature
[2]: https://source.chromium.org/chromium/chromium/src/+/main:build/rust/rust_executable.gni
[3]: https://github.com/Daniel-Liu-c0deb0t
