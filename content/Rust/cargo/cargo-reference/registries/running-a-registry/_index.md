+++
title = "02-运行注册表"
date = 2026-07-30T14:49:00+08:00
weight = 52
type = "docs"
description = "自建包注册表概览"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Cargo Book](https://doc.rust-lang.org/cargo/)

# 运行注册表 {#running-a-registry}


> 原文链接: [https://doc.rust-lang.org/cargo/reference/running-a-registry.html](https://doc.rust-lang.org/cargo/reference/running-a-registry.html)


可通过包含索引的 git 仓库，以及存放由 [`cargo package`] 创建的压缩 `.crate` 文件的服务器，实现一个最小注册表。用户无法用 Cargo 向其发布，但在封闭环境中这可能已足够。索引格式见 [注册表索引][Registry Index]。

支持发布的功能完备注册表还需要有符合 Cargo 所用 API 的 Web API 服务。Web API 见 [注册表 Web API][Registry Web API]。

有商业与社区项目可用于构建和运行注册表。可用列表见 <https://github.com/rust-lang/cargo/wiki/Third-party-registries>。

[Registry Web API]: 02-registry-web-api/
[Registry Index]: 01-registry-index/
[`cargo publish`]: ../../../cargo-commands/publishing-commands/05-cargo-publish/
[`cargo package`]: ../../../cargo-commands/publishing-commands/04-cargo-package/
