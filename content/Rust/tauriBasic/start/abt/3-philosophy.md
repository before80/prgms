+++
title = "3 Tauri 理念"
date = 2026-09-25T21:31:08+08:00
weight = 3
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

> 原文链接: [https://tauri.app/about/philosophy/](https://tauri.app/about/philosophy/)

Tauri 是一个工具包，帮助开发者为主流桌面平台开发应用——几乎可以使用现存任何前端框架。核心用 Rust 构建，CLI 借助 Node.js，使 Tauri 成为真正多语言（polyglot）的方式来创建和维护优秀的应用。

<iframe
    style="width: 100%; aspect-ratio: 16/9;"
    src="https://www.youtube-nocookie.com/embed/UxTJeEbZX-0?si=mwQUzXb6mmCg7aom"
    title="YouTube video player"
    frameborder="0"
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
    allowfullscreen
></iframe>

## 安全第一

在当今世界，任何诚实的威胁模型都假定用户的设备已被攻破。这让应用开发者陷入复杂的处境：如果设备已经有风险，软件又如何能被信任？

我们采取的做法是纵深防御。我们希望你能够采取一切可能的预防措施，把暴露给攻击者的面积降到最小。Tauri 让你可以选择发布哪些 API 端点、是否要在应用中内置 localhost 服务器，它甚至在运行时随机化功能句柄。这些以及其它技术构成了一个安全基线，为你和你的用户赋能。

让静态攻击变得极其困难、让系统彼此隔离，从而拖慢攻击者，这就是我们的目标。如果你来自 Electron 生态——请放心——Tauri 默认只发布二进制文件，不发布 ASAR 文件。

通过选择以安全为指导思想来构建 Tauri，我们让你有充分的机会采取主动的安全姿态。

## 多语言，而非孤岛

大多数当代框架使用单一语言范式，因而被困在知识与惯用法的气泡中。这对某些细分应用或许可行，但它也滋生了一种部落主义。

这可以从 React、Angular 和 Vue 开发社区各自抱团于自己技术栈的方式中看到，最终几乎没有交叉融合。

同样的情况也出现在 Rust、Node、C++ 的战场上：强硬派各持立场，拒绝跨社区协作。

今天，Tauri 的后端使用 Rust——但在不远的将来，Go、Nim、Python、C# 等其它后端也会成为可能。这是因为我们维护着 [webview](https://github.com/webview) 组织的官方 Rust 绑定，并计划让你按需替换后端。由于我们的 API 可以用任何支持 C 互操作的语言实现，完全兼容只差一个 PR。

## 诚实的开源

没有社区，这一切都无从谈起。今天的软件社区是了不起的地方，人们互相帮助并创造出色的东西——开源是其中非常重要的一部分。

开源对不同的人意味着不同的东西，但大多数人都会同意，它服务于支持自由。当软件不尊重你的权利时，它就可能显得不公平，并可能以不道德的方式运作，从而损害你的自由。

这就是为什么我们很自豪：FLOSS 支持者可以用 Tauri 构建“可认证地”开源、并能被纳入 FSF 认可的 GNU/Linux 发行版的应用。

## 未来

Tauri 的未来取决于你的参与和贡献。试用它、提 issue、加入某个工作组，或者捐赠——每一份贡献都很重要。无论如何，都请与我们联系！！！
