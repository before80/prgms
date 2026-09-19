+++
title = "第五篇 工程与质量"
weight = 50
date = "2026-09-14T22:30:00+08:00"
type = "docs"
description = "包与依赖、资源与 C 互操作、Swift Testing 与 XCTest、调试与性能"
isCJKLanguage = true
draft = false
+++

# 第五篇：工程与质量

> 语法够用了，接下来是把代码组织成别人敢改、未来敢升级的样子。

这一篇讲的全是“团队协作的语言”：包清单怎么写才不埋雷、依赖版本怎么约束、资源怎么放、怎么在 Swift 里调用 C、测试用 Swift Testing 还是 XCTest、出了问题是先加日志还是先上断点、性能到底该不该优化。

一个提醒：测试不是“写完再补”的仪式。它和类型系统一样，是你敢重构的前提。

## 本篇章节

1. [包与工程]({{< relref "Chapter-33-Packages-and-Engineering.md" >}})
2. [测试]({{< relref "Chapter-34-Testing.md" >}})
3. [调试与性能]({{< relref "Chapter-35-Debugging-and-Performance.md" >}})

## 读完你应该能

- 从一个空目录搭出结构清楚、依赖可控的包，并知道每个文件为什么存在。
- 用 Swift Testing 写测试，也能读懂和迁移旧的 XCTest 代码。
- 在断言、日志、断点、计时和优化属性之间做出合适的选择，而不是凭感觉优化。
