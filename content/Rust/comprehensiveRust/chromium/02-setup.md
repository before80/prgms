+++
title = "2 环境准备"
date = 2026-08-11T11:30:00+08:00
weight = 257
type = "docs"
description = "02-环境准备 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/chromium/setup.html](https://google.github.io/comprehensive-rust/chromium/setup.html)

# 2 环境准备

确保你能构建并运行 Chromium。任何平台与构建标志组合都可以，只要你的代码相对较新（提交位置 1223636 起，对应 2023 年 11 月）：

```shell
gn gen out/Debug
autoninja -C out/Debug chrome
out/Debug/chrome # 或在 Mac 上：out/Debug/Chromium.app/Contents/MacOS/Chromium
```

（推荐使用 component、debug 构建以获得最快的迭代时间。这是默认配置！）

若你还没到这一步，请参阅
[How to build Chromium](https://www.chromium.org/developers/how-tos/get-the-code/)。
警告：配置 Chromium 构建环境需要时间。

也建议安装 Visual Studio Code。

# 关于练习

本部分课程有一系列彼此衔接的练习。我们会把它们分散在整门课中完成，而不是只放在最后。如果某部分没有时间做完，别担心：可以在下一个时段赶上。
