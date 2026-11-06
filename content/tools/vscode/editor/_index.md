+++
title = "3 编辑器"
date = 2026-11-06T07:53:25+08:00
weight = 3
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++


> 原文链接: [https://code.visualstudio.com/docs/editing/getting-started/overview](https://code.visualstudio.com/docs/editing/getting-started/overview)

# 3 编辑器

　　Visual Studio Code 是一个跨平台代码编辑器，将专注的编辑体验与开发生命周期所需的工具结合在一起。无论是快速修改单个文件，还是打开完整项目并从编辑进入运行、调试、测试和源代码管理，都无需切换应用程序。

　　本概述介绍核心编辑器功能背后的概念，并指引你查阅工作流各部分的详细文档。

## 一个编辑器满足你的开发工作流 {#one-editor-for-your-development-workflow}

　　VS Code 不限定编程语言、操作系统或开发工具集，而是提供一个适应项目的统一工作台：

* **在一个位置工作。**从同一窗口访问文件、代码智能、终端、源代码管理、调试器和测试。这些工具共享项目上下文，减少在编写代码和验证更改之间切换的阻力。
* **使用你的工具和技术栈。**使用现有编译器、命令行工具、shell 和源代码管理工作流。安装扩展即可为几乎任何编程语言、框架或服务添加丰富支持。
* **在代码运行的地方工作。**在本地计算机上开发，连接到[8 远程](../remote/)，或使用 [8.1 VS Code for the Web](../remote/8.1-VSCodeForTheWeb/)进行轻量级更改。
* **让编辑器成为你自己的。**自定义布局、键盘快捷键和行为，然后使用配置文件在不同项目或任务之间切换配置。

## 探索核心功能 {#explore-the-core-capabilities}

* [3.2.1 基本编辑](3.2-WriteCode/3.2.1-BasicEditing/)：在语言感知辅助下编写、导航和重构代码。
* [6.1 调试代码](../debugging-and-testing/6.1-Debugging/)：无需离开编辑器即可构建并验证更改。
* [4 源代码管理](../source-control/)：以 Git 审查更改、使用分支并协作。
* [5.2 终端基础](../terminal/5.2-TerminalBasics/)：在代码旁边运行 shell 和命令行工具。
* [3.3.4 设置](3.3-ConfigureTheEditor/3.3.4-Settings/)：通过设置、配置文件和扩展调整编辑器。
* [2 VS Code 中的 AI](../ai-in-vs-code/)：委派编码任务，同时保持对更改的控制。

## 熟悉环境 {#get-oriented}

　　VS Code 窗口称为工作台。[3.1.2 用户界面](3.1-GettingStarted/3.1.2-UserInterface/)以编辑器为中心，并为文件、搜索、源代码管理、运行和调试以及扩展提供专用视图。活动栏在这些视图之间切换，而面板承载终端、问题视图和调试控制台等辅助工具。

　　[3.2.8.1 工作区概述](3.2-WriteCode/3.2.8-Workspaces/3.2.8.1-Overview/)表示你打开的项目。工作区可以包含一个或多个文件夹，并为 VS Code 提供上下文，以恢复打开的文件和布局、应用项目专用设置以及存储任务和调试配置。不需要项目上下文时，也可以打开单个文件。

## 编辑代码 {#edit-code}

　　编辑器结合通用文本编辑功能和语言感知辅助。可以在任何文本文件中使用[3.2.1 基本编辑](3.2-WriteCode/3.2.1-BasicEditing/)功能，例如多光标、搜索替换和自动保存。对于受支持的编程语言，[3.2.2 IntelliSense](3.2-WriteCode/3.2.2-IntelliSense/)会使用代码信息提供补全、参数信息和内联文档。

　　[3.2.5 代码导航](3.2-WriteCode/3.2.5-CodeNavigation/)帮助你在项目中的定义、引用和符号之间移动。可以使用语言感知的[3.2.6 重构](3.2-WriteCode/3.2.6-Refactoring/)转换代码，并使用[3.2.7 代码片段](3.2-WriteCode/3.2.7-Snippets/)复用常用代码。这些功能来自内置语言支持和扩展，因此具体功能因语言而异。请访问[10 语言与运行时](../languages-and-runtimes/10.1-Overview/)设置技术支持。

## 运行、调试和测试 {#run-debug-and-test}

　　在更改过程中，运行、调试和测试形成连续循环。VS Code 将这些活动带入工作台，同时继续使用项目中的工具和运行时。

　　使用[6.3 任务](../debugging-and-testing/6.3-Tasks/)自动执行构建、脚本和其他重复命令。使用[6.1 调试代码](../debugging-and-testing/6.1-Debugging/)通过断点控制程序执行、单步执行代码并检查应用程序状态。[6.4 测试](../debugging-and-testing/6.4-Testing/)使用测试扩展发现测试，并允许你在代码旁运行、调试和审查结果。

## 管理源代码 {#manage-source-control}

　　集成[4 源代码管理](../source-control/)让项目的历史记录和状态紧邻代码。查看哪些文件已更改、审查行内差异，并在编辑和源代码管理操作之间切换而不丢失上下文。

　　VS Code 包含 Git 支持，可[4.3 暂存与提交](../source-control/4.3-StagingCommits/)、[4.5 分支与工作树](../source-control/4.5-BranchesWorktrees/)以及[4.6 解决合并冲突](../source-control/4.6-MergeConflicts/)。你也可以[4.7 在 GitHub 上协作](../source-control/4.7-CollaborateOnGitHub/)，扩展还可以添加其他源代码管理系统支持。

## 使用集成终端 {#use-the-integrated-terminal}

　　[5.2 终端基础](../terminal/5.2-TerminalBasics/)在工作台中运行完整 shell，因此可以使用与外部终端相同的命令行工具和工作流。新终端在工作区上下文中启动，可以保持多个终端打开、拆分它们或移到编辑器区域。

　　使用[5.3 终端配置文件](../terminal/5.3-TerminalProfiles/)选择和配置首选 shell。[5.4 终端命令集成](../terminal/5.4-ShellIntegration/)增加对命令及其输出的感知，用于导航、命令状态和其他编辑器功能。还可以个性化[5.5 终端外观](../terminal/5.5-Appearance/)。

## 自定义和扩展编辑器 {#customize-and-extend-the-editor}

　　VS Code 以有用的默认值开始，但允许你控制编辑器的外观和行为。更改[3.3.2 布局](3.3-ConfigureTheEditor/3.3.2-Layout/)、重新映射[3.3.3 键盘快捷键](3.3-ConfigureTheEditor/3.3.3-KeyboardShortcuts/)，并全局或为特定工作区配置[3.3.4 设置](3.3-ConfigureTheEditor/3.3.4-Settings/)。

　　[3.3.6.1 扩展概述](3.3-ConfigureTheEditor/3.3.6-Extensions/3.3.6.1-Overview/)添加语言、调试器、源代码管理提供程序以及与外部工具和服务的连接。创建[3.3.8 配置文件](3.3-ConfigureTheEditor/3.3.8-Profiles/)，在不同项目或任务的扩展、设置和 UI 自定义集之间切换。使用[3.3.5 设置同步](3.3-ConfigureTheEditor/3.3.5-SettingsSync/)在设备之间共享配置。

## 后续步骤 {#next-steps}

* 按照[3.1.1 编辑器教程](3.1-GettingStarted/3.1.1-EditorTutorial/)完成引导式入门。
* 查看[3.1.3 提示和技巧](3.1-GettingStarted/3.1.3-TipsAndTricks/)，提高工作效率。
* 了解如何在[8 远程](../remote/)开发。
