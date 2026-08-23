+++
title = "5 安全实践"
date = 2026-08-23T16:35:00+08:00
weight = 40
type = "docs"
description = ""
isCJKLanguage = true
draft = false

+++


> 原文链接: [https://book.async.rs/security/index.html](https://book.async.rs/security/index.html)

编写高性能的异步核心库，不可避免地会涉及一些 `unsafe` 代码。

我们对 `async-std` 中包含的所有 `unsafe` 代码都经过严格审查，并遵循普遍认可的最佳实践。

若你发现本库存在与安全相关的问题，请通过我们的[安全联络方式][security-policy]与我们联系。

欢迎在我们的 [GitHub 组织][github] 上提交改进库健壮性或测试配置的补丁。

[security-policy]: 5.1-policy/
[github]: https://github.com/async-rs
