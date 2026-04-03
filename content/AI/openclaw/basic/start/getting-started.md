+++
title = "快速开始"
date = 2026-04-02T17:08:40+08:00
weight = 10
type = "docs"
description = ""
isCJKLanguage = true
draft = false

+++

# Getting Started

Install OpenClaw, run onboarding, and chat with your AI assistant — all in about 5 minutes. By the end you will have a running Gateway, configured auth, and a working chat session.

​	安装 OpenClaw、完成新手引导并与你的 AI 助手聊天——整个过程大约只需 5 分钟。完成后，你将拥有一个运行中的Gateway、已配置的身份验证，以及一个可正常使用的聊天会话。

## What you need

- **Node.js** — Node 24 recommended (Node 22.14+ also supported)
- **An API key** from a model provider (Anthropic, OpenAI, Google, etc.) — onboarding will prompt you



Check your Node version with `node --version`. **Windows users:** both native Windows and WSL2 are supported. WSL2 is more stable and recommended for the full experience. See [Windows](https://docs.openclaw.ai/platforms/windows). Need to install Node? See [Node setup](https://docs.openclaw.ai/install/node).

​	使用 `node --version` 查看你的 Node 版本。**Windows 用户：**原生 Windows 和 WSL2 均受支持。WSL2 更稳定，推荐用于获得完整体验。详见 [Windows](https://docs.openclaw.ai/platforms/windows)。需要安装 Node 吗？详见 [Node 安装设置](https://docs.openclaw.ai/install/node)。

## Quick setup

1) Install OpenClaw

{{< tabpane text=true persist=disabled >}}

{{% tab "macOS | Linux" %}}

```sh
curl -fsSL https://openclaw.ai/install.sh | bash
```

![Install Script Process](./getting-started_img/install-script.svg)

{{% /tab %}}

{{% tab "Windows (PowerShell)" %}}

```sh
iwr -useb https://openclaw.ai/install.ps1 | iex
```



{{% /tab %}}

{{< /tabpane >}}



> Other install methods (Docker, Nix, npm): [Install](https://docs.openclaw.ai/install).
>
> ​	其他安装方式（Docker、Nix、npm）：[安装](/AI/openclaw/basic/install)。

2) Run onboarding

```sh
openclaw onboard --install-daemon
```

The wizard walks you through choosing a model provider, setting an API key, and configuring the Gateway. It takes about 2 minutes.See [Onboarding (CLI)](https://docs.openclaw.ai/start/wizard) for the full reference.

​	该向导将引导你选择模型提供商、设置 API 密钥并配置网关。整个过程大约需要 2 分钟。

3) Verify the Gateway is running

```sh
openclaw gateway status
```

You should see the Gateway listening on port 18789.

4) Open the dashboard

```sh
openclaw dashboard
```

This opens the Control UI in your browser. If it loads, everything is working.

​	这会在你的浏览器中打开控制界面。如果界面加载成功，说明一切正常。

5) Send your first message

Type a message in the Control UI chat and you should get an AI reply.Want to chat from your phone instead? The fastest channel to set up is [Telegram](https://docs.openclaw.ai/channels/telegram) (just a bot token). See [Channels](https://docs.openclaw.ai/channels) for all options.

​	在 Control UI 聊天框中输入一条消息，你就会收到一条 AI 回复。想改用手机聊天吗？最快的设置渠道是[Telegram](https://docs.openclaw.ai/channels/telegram)（只需一个机器人令牌）。查看[渠道](https://docs.openclaw.ai/channels)了解所有选项。



## What to do next



### Connect a channel

WhatsApp, Telegram, Discord, iMessage, and more.



### Pairing and safety

Control who can message your agent.

​	控制谁可以给你的智能体发消息。

### Configure the Gateway

Models, tools, sandbox, and advanced settings.

​	模型、工具、沙箱以及高级设置。

### Browse tools

Browser, exec, web search, skills, and plugins.

​	浏览器、执行程序、网络搜索、技能和插件

> Advanced: environment variables
>
> If you run OpenClaw as a service account or want custom paths:
>
> ​	如果你将 OpenClaw 作为服务账户运行，或者想要自定义路径：
>
> - `OPENCLAW_HOME` — home directory for internal path resolution  用于内部路径解析的主目录
> - `OPENCLAW_STATE_DIR` — override the state directory  覆盖状态目录
> - `OPENCLAW_CONFIG_PATH` — override the config file path 覆盖配置文件路径
>
> Full reference: [Environment variables](https://docs.openclaw.ai/help/environment).
>
> ​	完整参考：[环境变量](https://docs.openclaw.ai/help/environment)。

