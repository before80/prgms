+++
title = "1.8 在 Windows 上模糊测试"
date = 2026-08-23T13:50:00+08:00
weight = 18
type = "docs"
description = "Windows 与 MSVC AddressSanitizer"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Rust Fuzz Book](https://rust-fuzz.github.io/book/)

# 在 Windows 上模糊测试 {#windows}


> 原文链接: [https://rust-fuzz.github.io/book/cargo-fuzz/windows.html](https://rust-fuzz.github.io/book/cargo-fuzz/windows.html)


[cargo-fuzz](https://github.com/rust-fuzz/cargo-fuzz) 可用于模糊测试 Windows 程序，这得益于 [MSVC AddressSanitizer](https://learn.microsoft.com/en-us/cpp/sanitizers/asan)。请继续阅读，了解如何在 Windows 与 PowerShell 环境中配置构建与模糊测试。
