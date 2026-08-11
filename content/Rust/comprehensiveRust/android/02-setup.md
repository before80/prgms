+++
title = "2 环境准备"
date = 2026-08-11T11:30:00+08:00
weight = 210
type = "docs"
description = "02-环境准备 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/android/setup.html](https://google.github.io/comprehensive-rust/android/setup.html)

# 2 环境准备

我们将使用 Cuttlefish Android 虚拟设备来测试代码。请确保你已能访问一台，或用以下命令新建：

```shell
source build/envsetup.sh
lunch aosp_cf_x86_64_phone-trunk_staging-userdebug
acloud create
```

详情请参阅
[Android Developer Codelab](https://source.android.com/docs/setup/start)。

后续页面中的代码可在课程材料的
[`src/android/` 目录](https://github.com/google/comprehensive-rust/tree/main/src/android)
中找到。请 `git clone` 该仓库以便跟着操作。

> 要点：
>
> - Cuttlefish 是面向通用 Linux 桌面设计的参考 Android 设备。也计划支持 MacOS。
>
> - Cuttlefish 系统镜像对真实设备保持高度保真，是运行许多 Rust 用例的理想模拟器。

