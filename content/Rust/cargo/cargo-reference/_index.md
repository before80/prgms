+++
title = "03-Cargo 参考"
date = 2026-07-30T14:49:00+08:00
weight = 30
type = "docs"
description = "Cargo 各领域细节的参考文档"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Cargo Book](https://doc.rust-lang.org/cargo/)

# Cargo 参考 {#cargo-reference}


> 原文链接: [https://doc.rust-lang.org/cargo/reference/index.html](https://doc.rust-lang.org/cargo/reference/index.html)


本参考涵盖 Cargo 各个领域的细节。

* [Manifest 格式](the-manifest-format/)
    * [Cargo 目标](the-manifest-format/01-cargo-targets/)
    * [Rust 版本](the-manifest-format/02-rust-version/)
* [工作空间](02-workspaces/)
* [指定依赖](specifying-dependencies/)
    * [覆盖依赖](specifying-dependencies/01-overriding-dependencies/)
    * [源替换](specifying-dependencies/02-source-replacement/)
    * [依赖解析](specifying-dependencies/03-dependency-resolution/)
* [特性（Features）](features/)
    * [Features 示例](features/01-features-examples/)
* [配置文件（Profiles）](05-profiles/)
* [配置](06-configuration/)
* [环境变量](07-environment-variables/)
* [构建脚本](build-scripts/)
    * [构建脚本示例](build-scripts/01-build-script-examples/)
* [构建缓存](09-build-cache/)
* [包 ID 规范](10-package-id-specifications/)
* [外部工具](11-external-tools/)
* [注册表](registries/)
    * [注册表认证](registries/registry-authentication/)
        * [凭证提供者协议](registries/registry-authentication/01-credential-provider-protocol/)
    * [运行注册表](registries/running-a-registry/)
        * [注册表索引](registries/running-a-registry/01-registry-index/)
        * [注册表 Web API](registries/running-a-registry/02-registry-web-api/)
* [SemVer 兼容性](13-semver-compatibility/)
* [未来不兼容报告](14-future-incompat-report/)
* [报告构建耗时](15-reporting-build-timings/)
* [Lint](16-lints/)
* [不稳定特性](17-unstable-features/)
