+++
title = "快速开始概览"
date = 2026-04-02T18:58:41+08:00
weight = 20
type = "docs"
description = ""
isCJKLanguage = true
draft = false

+++

# Onboarding Overview

OpenClaw has two onboarding paths. Both configure auth, the Gateway, and optional channels — they just differ in how you interact with the setup.

​	OpenClaw 有两种 onboarding 路径。两者都会配置身份验证、网关以及可选的通道——它们的区别仅在于与设置交互的方式。

## Which path should I use?

|                | CLI onboarding                         | macOS app onboarding      |
| :------------- | :------------------------------------- | :------------------------ |
| **Platforms**  | macOS, Linux, Windows (native or WSL2) | macOS only                |
| **Interface**  | Terminal wizard 终端向导               | Guided UI in the app      |
| **Best for**   | Servers, headless, full control        | Desktop Mac, visual setup |
| **Automation** | `--non-interactive` for scripts        | Manual only               |
| **Command**    | `openclaw onboard`                     | Launch the app            |

Most users should start with **CLI onboarding** — it works everywhere and gives you the most control.

​	大多数用户应从**CLI onboarding**开始——它适用于所有环境，还能为你提供最大的控制权。

## What onboarding configures 

Regardless of which path you choose, onboarding sets up:

​	无论你选择哪种方式，onboarding 都会完成以下配置：

1. **Model provider and auth** — API key, OAuth, or setup token for your chosen provider 你所选提供商的 API 密钥、OAuth 授权或设置令牌
2. **Workspace** — directory for agent files, bootstrap templates, and memory 存放智能体文件、引导模板和记忆体的目录
3. **Gateway** — port, bind address, auth mode 端口、绑定地址、认证模式
4. **Channels** (optional) — WhatsApp, Telegram, Discord, and more
5. **Daemon** (optional) — background service so the Gateway starts automatically 让Gateway 自动启动的后台服务

## CLI onboarding

Run in any terminal:

​	在任意终端中运行：

```sh
openclaw onboard
```

Add `--install-daemon` to also install the background service in one step.

​	添加 `--install-daemon` 还可一步完成后台服务的安装。

Full reference: [Onboarding (CLI)](https://docs.openclaw.ai/start/wizard) CLI command docs: [`openclaw onboard`](https://docs.openclaw.ai/cli/onboard)

​	完整参考文档：[Onboarding (CLI)](https://docs.openclaw.ai/start/wizard)命令行工具文档：[`openclaw onboard`](https://docs.openclaw.ai/cli/onboard)

## macOS app onboarding

Open the OpenClaw app. The first-run wizard walks you through the same steps with a visual interface.

​	打开 OpenClaw 应用程序。首次运行向导会通过可视化界面引导你完成相同的步骤。

Full reference: [Onboarding (macOS App)](https://docs.openclaw.ai/start/onboarding)

​	完整参考资料：[Onboarding (macOS App)](https://docs.openclaw.ai/start/onboarding)

## Custom or unlisted providers 自定义或未列出的提供商

If your provider is not listed in onboarding, choose **Custom Provider** and enter:

​	如果你的服务商未在首次使用向导中列出，请选择**Custom Provider**商并输入：

- API compatibility mode (OpenAI-compatible, Anthropic-compatible, or auto-detect)
- API 兼容模式（兼容 OpenAI、兼容 Anthropic 或自动检测）
- Base URL and API key
- 基础URL和API密钥
- Model ID and optional alias
- 模型ID及可选别名

Multiple custom endpoints can coexist — each gets its own endpoint ID.

​	多个自定义终端节点可以共存——每个终端节点都会拥有专属的终端节点 ID。

