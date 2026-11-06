+++
title = "2 VS Code 中的 AI"
date = 2026-11-06T07:53:25+08:00
weight = 2
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++


> 原文链接: [https://code.visualstudio.com/docs/agents/overview](https://code.visualstudio.com/docs/agents/overview)

# 2 VS Code 中的 AI

　　根据任务需要，在 Visual Studio Code 中使用尽可能多或尽可能少的 AI。可以在输入时获取建议，在代码旁与智能体协作，或在智能体窗口中协调跨项目任务。随着工作变化，可以组合这些方式。

　　可以从多个提供商选择模型，并使用 GitHub Copilot、Claude 或 Codex 智能体运行框架，支持使用现有账户或自己的 API 密钥。自定义和插件可帮助智能体适应你的工作。

　　连续性让你在受支持的界面之间继续智能体工作，而无需重新开始。可以通过 GitHub Environments 连接到你自己计算机上的会话，或使用云会话而无需保持本地主机在线。

## 尝试第一个智能体任务 {#try-your-first-agent-task}

　　构建并验证一个小应用，然后审查结果。快速入门使用 GitHub Copilot 运行框架和推荐默认值，因此无需先配置每个选项。请参阅[2.1.3 智能体快速入门](getting-started/2.1.3-AgentsQuickstart/)。

* **已经使用智能体**：在你自己的仓库中按照[2.1.1 查找指南](getting-started/2.1.1-FindAGuide/#experienced-agent-fast-track)操作。
* **不熟悉 VS Code**：先[1 快速开始](../get-started/)。

## 选择你的工作方式 {#choose-how-you-work}

　　根据任务在不同体验之间切换，并[跨界面继续智能体会话](#continue-across-interfaces-and-machines)以从上次中断处继续。

* [2.2.1 内联建议](work-with-ai/2.2.1-InlineSuggestions/)：在输入时获取内联建议，包括下一次编辑建议。
* [2.2.2 聊天视图](work-with-ai/2.2.2-ChatView/)：在聊天视图中与智能体协作，专注于当前工作区以及编辑器、终端、测试和调试器。
* [2.2.3 智能体窗口](work-with-ai/2.2.3-AgentsWindow/)：在智能体窗口中跨项目分配任务并管理智能体会话。

　　[2.7.1 智能体](concepts/2.7.1-Agents/)使用模型和工具查找相关代码、进行更改并运行检查。聊天视图和智能体窗口都可以运行智能体。你设定目标、指导工作并审查结果。

　　对于日常任务，可以将提示词保存为[2.2.10.5 自动化](work-with-ai/plan-and-run-tasks/2.2.10.5-Automations/)，在本地按计划运行，或使用云自动化进行按计划或事件触发的仓库工作。启用重复工作之前，请先审查手动运行结果。

　　对于专注编辑，可以使用[2.2.4 内联聊天和快速聊天](work-with-ai/2.2.4-InlineChatAndQuickChat/)，无需离开代码。要针对特定任务比较功能，请使用 [2.8.1.1 AI 功能速查表](reference-and-help/reference/2.8.1.1-CheatSheet/#choose-a-feature)。

## 选择模型、智能体和工具 {#choose-your-models-agents-and-tools}

　　对于第一个智能体任务，[2.1.3 智能体快速入门](getting-started/2.1.3-AgentsQuickstart/)即可，无需配置所有选项。你可以根据需要调整：

| 选择 | 选项 |
|--------|---------|
| **模型** | 通过 GitHub Copilot 选择[2.3.1 选择和配置模型](choose-models-and-agents/2.3.1-ChooseAndConfigureModels/)，或使用自己的 [2.3.1 选择和配置模型](choose-models-and-agents/2.3.1-ChooseAndConfigureModels/#bring-your-own-language-model-key)或受支持的本地模型。 |
| **智能体运行框架** | 根据[2.3.2 选择智能体运行框架](choose-models-and-agents/2.3.2-ChooseAnAgentHarness/#compare-agent-harnesses)，在 GitHub Copilot、Anthropic Claude 或 OpenAI Codex 之间选择。 |
| **访问和计费** | 使用现有的 GitHub Copilot 套餐、受支持的提供商账户或 API 密钥。检查[2.3.2 选择智能体运行框架](choose-models-and-agents/2.3.2-ChooseAnAgentHarness/#requirements-and-setup)。 |
| **自定义** | 使用[2.4.2 插件](customize-and-extend/2.4.2-Plugins/)、[2.6.10 调整智能体以适应项目](tutorials-and-guides/2.6.10-AdaptAgentsToYourProject/)和[2.4.3 智能体技能](customize-and-extend/2.4.3-AgentSkills/)调整智能体。通过 [2.4.7 添加 MCP 服务器](customize-and-extend/2.4.7-AddMCPServers/)连接外部工具。 |

## 跨界面和计算机继续 {#continue-across-interfaces-and-machines}

　　连续性意味着在受支持的界面和计算机之间继续智能体工作，而无需重新开始。选择与智能体交互的位置，工作区和执行仍保留在主机上。会话支持和要求因运行框架和目的地而异。

| 工作位置 | 从这里开始 |
|------------------------|------------|
| **跨 GitHub Copilot 应用和设备** | 使用 [2.5.2 远程智能体会话](work-across-apps-and-machines/2.5.2-RemoteAgentSessions/#github-environments-preview)注册开发计算机，并从 VS Code、GitHub Copilot 应用、Copilot CLI、GitHub.com 或 GitHub Mobile 继续其智能体会话。可用操作因客户端而异。 |
| **在受管理的云计算资源上** | 使用[2.5.3 云会话](work-across-apps-and-machines/2.5.3-CloudSessions/)进行交互式智能体工作，而无需让自己的计算机保持在线。重新打开现有云会话即可继续对话。 |
| **编辑器或智能体窗口** | 在 VS Code 中使用 Copilot、Claude 或 Codex 运行框架，并[2.2.11.1 管理会话](work-with-ai/sessions/2.2.11.1-ManageSessions/#continue-between-the-chat-view-and-agents-window)。 |
| **另一台计算机上的 VS Code** | 使用 VS Code 专用远程连接：[2.5.2 远程智能体会话](work-across-apps-and-machines/2.5.2-RemoteAgentSessions/#connect-via-ssh)或[2.5.2 远程智能体会话](work-across-apps-and-machines/2.5.2-RemoteAgentSessions/#connect-via-dev-tunnel)。开发隧道还支持基于浏览器的智能体窗口。 |

　　对于在你自己的计算机上运行的会话，请保持主机运行并可访问。云会话使用受管理的计算资源。在云中开始工作，然后重新打开该会话来继续。

　　使用自己的私有仓库，可以[2.1.5 云连续性教程](getting-started/2.1.5-CloudContinuityTutorial/)（实验性）。

　　工具运行位置和模型托管位置是两个独立选择。智能体可以在你的计算机上编辑文件，同时将模型请求发送给托管提供商。

## 保持控制 {#stay-in-control}

　　AI 可能生成错误代码或误解你的意图。你仍然负责决定哪些更改进入代码库。

* **整合前审查。**智能体可以直接将编辑保存到会话文件夹或工作树。提交或合并更改之前，请[2.2.8 审查和还原更改](work-with-ai/2.2.8-ReviewAndRevertChanges/)。
* **控制操作并重定向工作。**使用[2.2.12.1 审批和权限](work-with-ai/permissions-and-security/2.2.12.1-ApprovalsAndPermissions/)决定哪些操作需要确认。可以[2.2.5 使用聊天](work-with-ai/2.2.5-UseChat/#send-messages-while-a-request-is-running)，但停止不会撤销已完成的操或对外部服务的更改。
* **理解隔离。**Git 工作树可将代码更改分开，但不是安全边界。有关智能体运行终端命令的文件系统和网络限制，请参阅[2.2.12.2 智能体沙盒](work-with-ai/permissions-and-security/2.2.12.2-AgentSandboxing/)。

　　在现有项目中使用智能体之前，请查看[2.2.12.3 AI 安全](work-with-ai/permissions-and-security/2.2.12.3-AISecurity/#recommended-security-baseline)。在受管理设备上，组织可能通过[7.2 管理 AI 设置](../enterprise/7.2-ManageAISettings/)限制可用的智能体、模型和工具。如果智能体未出现在聊天中，请查看[2.8.2.4 常见问题](reference-and-help/troubleshooting/2.8.2.4-FAQ/#agents-are-not-available-in-chat)。

　　对于键盘、屏幕阅读器和低视力工作流，请了解如何使用[3.3.9.1 辅助功能](../editor/3.3-ConfigureTheEditor/3.3.9-Accessibility/3.3.9.1-Accessibility/#accessible-view)。

## 后续步骤 {#next-steps}

* [2.1.6 最佳实践](getting-started/2.1.6-BestPractices/)。
* [2.6.14 减少 AI 点数使用量](tutorials-and-guides/2.6.14-ReduceCreditUsage/)。
