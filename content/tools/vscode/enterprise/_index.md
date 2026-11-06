+++
title = "7 企业"
date = 2026-11-06T07:53:25+08:00
weight = 7
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++


> 原文链接: [https://code.visualstudio.com/docs/enterprise/overview](https://code.visualstudio.com/docs/enterprise/overview)

# 7 企业

　　Visual Studio Code 可用作各种规模企业团队的开发工具。作为 IT 管理员，你可以配置 VS Code，以在整个组织中实现一致性和合规性。

　　若要部署 AI，请先从[7.2 管理 AI 设置](7.2-ManageAISettings/)开始。选择组织需要的控制项，用有代表性的开发工作流进行测试，并告知开发者哪些功能可用以及如何申请访问权限。

> **注意**：如果你是使用受管理设备的开发者，请从 [2.8.2.1 故障排除](../ai-in-vs-code/reference-and-help/troubleshooting/2.8.2.1-Troubleshooting/#start-with-basic-checks)开始。如果某项设置由组织管理，请联系管理员，而不要尝试覆盖策略。

## 企业策略 {#enterprise-policies}

　　VS Code 支持集中管理的策略，这些策略会覆盖受管理设备上的用户设置。可以通过 Microsoft Intune、Active Directory 组策略或 macOS 上的 MDM 解决方案等设备管理解决方案部署策略。

　　可用策略可控制：

* [7.2 管理 AI 设置](7.2-ManageAISettings/)：智能体模式、MCP 服务器和工具审批。
* [7.3 扩展管理](7.3-Extensions/)：允许的扩展和私有市场。
* [7.4 遥测](7.4-Telemetry/)：数据收集级别和反馈机制。
* [7.5 更新](7.5-Updates/)：控制 VS Code 何时以及如何更新。

　　完整可用策略列表请参阅[7.1 企业策略](7.1-Policies/)。

## 扩展管理 {#extension-management}

　　组织可以管理 VS Code 中的扩展安装和启用，并托管私有扩展市场。

* **允许的扩展**：按发布者、扩展 ID、版本或平台配置 VS Code 允许用户安装和启用的扩展。
* **私有市场**：在组织内部托管和分发内部及公共扩展。

　　详细了解[7.3 扩展管理](7.3-Extensions/)。

## 网络配置 {#network-configuration}

　　VS Code 的若干功能需要网络访问权限，包括自动更新、扩展市场和遥测。对于网络访问受限或使用代理服务器的环境，可能需要配置：

* **防火墙允许列表**：为 VS Code 功能允许特定主机名。
* **代理服务器**：VS Code 默认使用系统代理设置。
* **SSL 证书**：为 HTTPS 代理配置受信任的证书。

　　详细的网络配置请参阅 [9.6 网络连接](../advanced-setup/9.6-Network/)。

### 常用主机名 {#common-hostnames}

　　如果防火墙需要允许列表，应包括以下关键主机名：

* `update.code.visualstudio.com`：更新
* `marketplace.visualstudio.com`：扩展市场
* `*.gallery.vsassets.io`：扩展资产
* `vscode.download.prss.microsoft.com`：下载

　　完整主机名列表请参阅网络文档中的[9.6 网络连接](../advanced-setup/9.6-Network/#common-hostnames)。

## 预装扩展 {#preinstalled-extensions}

　　你可以准备包含 VS Code 和一组预装扩展的计算机映像或虚拟机。用户首次启动 VS Code 时，扩展会自动安装。详细了解[7.3 扩展管理](7.3-Extensions/#preinstall-extensions)。

## 相关资源 {#related-resources}

* [7.1 企业策略](7.1-Policies/)：完整策略列表。
* [9.6 网络连接](../advanced-setup/9.6-Network/)：代理和防火墙配置。
* [3.3.5 设置同步](../editor/3.3-ConfigureTheEditor/3.3.5-SettingsSync/)：在设备之间同步设置。
