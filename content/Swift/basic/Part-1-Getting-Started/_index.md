+++
title = "第一篇 起步"
weight = 10
date = "2026-09-14T22:30:00+08:00"
type = "docs"
description = "装好 Swift 6.3 工具链、看懂源码结构、建出第一个 SwiftPM 项目"
isCJKLanguage = true
draft = false
+++

# 第一篇：起步

> 别急着背语法，先让第一行代码真的跑起来。能跑通，后面的一切才有落脚点。

这一篇只解决三件事：把 Swift 6.3 工具链装好并且知道该敲哪条命令；看懂一段 `.swift` 源码由哪些零件组成（注释、标识符、关键字、字面量、特殊指令）；用 SwiftPM 建出第一个正经项目，把代码拆进 target、加上依赖、顺手跑起测试。

做完这三步，后面每一章的示例你都能自己复现，而不是只会点头。

## 本篇章节

1. [装上 Swift 6.3，把第一行代码跑起来]({{< relref "Chapter-01-Install-and-First-Code.md" >}})
2. [一段 Swift 源码的解剖]({{< relref "Chapter-02-Anatomy-of-Source-Code.md" >}})
3. [SwiftPM 与第一个项目]({{< relref "Chapter-03-SwiftPM-and-First-Project.md" >}})

## 读完你应该能

- 说清 `swift`、`swiftc`、`swift run` 分别在什么时候用。
- 说清 Swift 源文件为什么必须是 UTF-8，以及遇到编码报错时从哪查起。
- 解释 `@main`、`main.swift` 与顶层代码三种入口的区别，并知道单个文件为什么不能写 `@main`。
- 独立新建一个包、加一个依赖、跑一次测试。

准备好了就往下走：第二篇开始进入语言主干，从 `let` 和 `var` 讲起。
