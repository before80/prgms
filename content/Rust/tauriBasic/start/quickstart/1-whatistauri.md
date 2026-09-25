+++
title = "1 什么是 Tauri？"
date = 2026-09-25T21:31:08+08:00
weight = 1
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

> 原文链接: [https://tauri.app/start/](https://tauri.app/start/)

Tauri 是一个用于为所有主流桌面平台和移动平台构建小巧、快速二进制文件的框架。开发者可以集成任何能编译为 HTML、JavaScript 和 CSS 的前端框架来构建用户界面，同时在需要时借助 Rust、Swift 和 Kotlin 等语言实现后端逻辑。

使用下面的某一条命令，即可通过 [`create-tauri-app`](https://github.com/tauri-apps/create-tauri-app) 开始构建。请务必按照[前置条件指南](../2-prerequisites/)安装 Tauri 所需的全部依赖。若想了解更详细的步骤，请参阅[创建项目](../3-createaproject/#使用-create-tauri-app)。

{{< tabpane text=true persist=disabled >}}
{{% tab header="Bash" %}}

```sh
sh <(curl https://create.tauri.app/sh)
```

{{% /tab %}}

{{% tab header="PowerShell" %}}

```sh
irm https://create.tauri.app/ps | iex
```

{{% /tab %}}

{{% tab header="Fish" %}}

```sh
sh (curl -sSL https://create.tauri.app/sh | psub)
```

{{% /tab %}}

{{% tab header="npm" %}}

```sh
npm create tauri-app@latest
```

{{% /tab %}}

{{% tab header="Yarn" %}}

```sh
yarn create tauri-app
```

{{% /tab %}}

{{% tab header="pnpm" %}}

```sh
pnpm create tauri-app
```

{{% /tab %}}

{{% tab header="deno" %}}

```sh
deno run -A npm:create-tauri-app
```

{{% /tab %}}

{{% tab header="bun" %}}

```sh
bun create tauri-app
```

{{% /tab %}}

{{% tab header="Cargo" %}}

```sh
cargo install create-tauri-app --locked
cargo create-tauri-app
```

{{% /tab %}}

{{< /tabpane >}}
创建好第一个应用之后，请查看[项目结构](../4-projectstructure/)，了解各个文件的作用。)

或者，从示例项目中探索各种项目配置与功能（[tauri](https://github.com/tauri-apps/tauri/tree/dev/examples) | [plugins-workspace](https://github.com/tauri-apps/plugins-workspace/tree/v2/examples/api)）

## 为什么选择 Tauri？

Tauri 为开发者提供了 3 个主要优势：

- 为构建应用提供安全的基础
- 使用系统原生 webview，带来更小的打包体积
- 灵活性强，开发者可以使用任意前端，并拥有多种语言的绑定

若想进一步了解 Tauri 的设计理念，请参阅 [Tauri 1.0 博客文章](https://tauri.app/blog/tauri-1-0/)。

### 安全的基础

由于构建于 Rust 之上，Tauri 能够利用 Rust 提供的内存安全、线程安全和类型安全。基于 Tauri 构建的应用可以自动获得这些优势，甚至不需要由 Rust 专家来开发。

Tauri 还会在主要版本和次要版本发布时进行安全审计。审计不仅覆盖 Tauri 组织内部的代码，也覆盖 Tauri 依赖的上游依赖。当然，这并不能消除所有风险，但它为开发者提供了一个坚实的构建基础。

请阅读 [Tauri 安全策略](https://github.com/tauri-apps/tauri/security/policy)和 [Tauri 2.0 审计报告](https://github.com/tauri-apps/tauri/blob/dev/audits/Radically_Open_Security-v2-report.pdf)。

### 更小的应用体积

Tauri 应用会利用每个用户系统上已有的 web view。Tauri 应用只包含该应用特有的代码和资源，无需为每个应用都打包一个浏览器引擎。这意味着一个最小的 Tauri 应用体积可以小于 600KB。

若想了解如何创建经过优化的应用，请参阅[应用体积概念](../../concept/5-appsize/)。

### 灵活的架构

由于 Tauri 使用 Web 技术，因此几乎所有前端框架都与 Tauri 兼容。[前端配置指南](../frontend-configuration/)中收录了流行前端框架的常见配置。

开发者可以在 JavaScript 中使用 `invoke` 函数来调用 JavaScript 与 Rust 之间的绑定，而 [Tauri 插件](../../develop/plugins/1-overview/)则提供了 Swift 和 Kotlin 绑定。

[TAO](https://github.com/tauri-apps/tao) 负责 Tauri 的窗口创建，[WRY](https://github.com/tauri-apps/wry) 负责 web view 渲染。这两个库由 Tauri 维护，如果需要在 Tauri 暴露的能力之外进行更深层的系统集成，也可以直接使用它们。

此外，Tauri 还维护了一系列插件来扩展 Tauri 核心所暴露的能力。你可以在[插件章节](../../plugin/1-overview/)中找到这些插件以及社区提供的插件。)
