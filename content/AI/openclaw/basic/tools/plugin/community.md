+++
title = "Community Plugins"
date = 2026-04-03T12:57:43+08:00
weight = 1
type = "docs"
description = ""
isCJKLanguage = true
draft = false

+++

# Community Plugins

Community plugins are third-party packages that extend OpenClaw with new channels, tools, providers, or other capabilities. They are built and maintained by the community, published on [ClawHub](https://docs.openclaw.ai/tools/clawhub) or npm, and installable with a single command.

​	社区插件是为 OpenClaw 扩展新渠道、工具、提供程序或其他功能的第三方包。它们由社区开发和维护，发布在 [ClawHub](https://docs.openclaw.ai/tools/clawhub) 或 npm 上，可通过一条命令完成安装。

```sh
openclaw plugins install <package-name>
```

OpenClaw checks ClawHub first and falls back to npm automatically.)

​	OpenClaw 会先检查 ClawHub，然后自动回退到 npm。

## Listed plugins 已列出的插件

### Codex App Server Bridge Codex 应用服务器桥接器

Independent OpenClaw bridge for Codex App Server conversations. Bind a chat to a Codex thread, talk to it with plain text, and control it with chat-native commands for resume, planning, review, model selection, compaction, and more.

​	为 Codex 应用服务器对话设计的独立 OpenClaw 桥接器。将聊天绑定到 Codex 线程，通过纯文本与之交流，并借助聊天原生命令对其进行控制，包括恢复、规划、复盘、模型选择、压缩等操作。

- **npm:** `openclaw-codex-app-server`
- **repo:** [github.com/pwrdrvr/openclaw-codex-app-server](https://github.com/pwrdrvr/openclaw-codex-app-server)

```sh
openclaw plugins install openclaw-codex-app-server
```

### DingTalk

Enterprise robot integration using Stream mode. Supports text, images, and file messages via any DingTalk client.

​	使用流式模式集成企业机器人。支持通过任意钉钉客户端收发文本、图片及文件消息。

- **npm:** `@largezhou/ddingtalk`
- **repo:** [github.com/largezhou/openclaw-dingtalk](https://github.com/largezhou/openclaw-dingtalk)

```sh
openclaw plugins install @largezhou/ddingtalk
```

### Lossless Claw (LCM)

Lossless Context Management plugin for OpenClaw. DAG-based conversation summarization with incremental compaction — preserves full context fidelity while reducing token usage.

​	适用于 OpenClaw 的无损上下文管理插件。基于有向无环图的对话摘要与增量压缩技术——在减少令牌使用量的同时保留完整的上下文保真度。

- **npm:** `@martian-engineering/lossless-claw`
- **repo:** [github.com/Martian-Engineering/lossless-claw](https://github.com/Martian-Engineering/lossless-claw)

```
openclaw plugins install @martian-engineering/lossless-claw
```

### Opik

Official plugin that exports agent traces to Opik. Monitor agent behavior, cost, tokens, errors, and more.

​	将智能体追踪导出至 Opik 的官方插件。可监控智能体行为、成本、令牌数、错误等信息。

- **npm:** `@opik/opik-openclaw`
- **repo:** [github.com/comet-ml/opik-openclaw](https://github.com/comet-ml/opik-openclaw)

```sh
openclaw plugins install @opik/opik-openclaw
```

### QQbot

Connect OpenClaw to QQ via the QQ Bot API. Supports private chats, group mentions, channel messages, and rich media including voice, images, videos, and files.

​	通过 QQ 机器人接口将 OpenClaw 连接至 QQ。支持私聊、群聊提及、频道消息，以及语音、图片、视频和文件等富媒体内容。

- **npm:** `@tencent-connect/openclaw-qqbot`
- **repo:** [github.com/tencent-connect/openclaw-qqbot](https://github.com/tencent-connect/openclaw-qqbot)

```sh
openclaw plugins install @tencent-connect/openclaw-qqbot
```

### wecom

WeCom channel plugin for OpenClaw by the Tencent WeCom team. Powered by WeCom Bot WebSocket persistent connections, it supports direct messages & group chats, streaming replies, proactive messaging, image/file processing, Markdown formatting, built-in access control, and document/meeting/messaging skills.

​	腾讯企业微信团队为 OpenClaw 打造的企业微信渠道插件。依托企业微信机器人 WebSocket 长连接能力，该插件支持单聊与群聊、流式回复、主动消息、图片/文件处理、Markdown 格式展示、内置访问控制，以及文档/会议/消息相关技能。

- **npm:** `@wecom/wecom-openclaw-plugin`
- **repo:** [github.com/WecomTeam/wecom-openclaw-plugin](https://github.com/WecomTeam/wecom-openclaw-plugin)

```sh
openclaw plugins install @wecom/wecom-openclaw-plugin
```

## Submit your plugin 提交你的插件

We welcome community plugins that are useful, documented, and safe to operate.

​	我们欢迎实用、有文档说明且可安全运行的社区插件。

1) Publish to ClawHub or npm 发布到 ClawHub 或 npm

Your plugin must be installable via `openclaw plugins install \<package-name\>`. Publish to [ClawHub](https://docs.openclaw.ai/tools/clawhub) (preferred) or npm. See [Building Plugins](https://docs.openclaw.ai/plugins/building-plugins) for the full guide.

​	你的插件必须可通过 `openclaw plugins install \<package-name\>` 安装。发布到 [ClawHub](https://docs.openclaw.ai/tools/clawhub)（首选）或 npm。完整指南请参阅 [构建插件](https://docs.openclaw.ai/plugins/building-plugins)。

2) Host on GitHub 托管于 GitHub

Source code must be in a public repository with setup docs and an issue tracker.

​	源代码必须存放在带有设置文档和问题跟踪器的公共代码仓库中。

3) Open a PR 提交拉取请求

Add your plugin to this page with:

​	将你的插件添加到此页面，需包含：

- Plugin name
- npm package name
- GitHub repository URL
- One-line description 单行描述
- Install command

## Quality bar 质量指标

| Requirement                                          | Why                                                          |
| :--------------------------------------------------- | :----------------------------------------------------------- |
| Published on ClawHub or npm 在 ClawHub 或 npm 上发布 | Users need `openclaw plugins install` to work 用户需要使用`openclaw plugins install`才能正常使用 |
| Public GitHub repo 公开的 GitHub 代码仓库            | Source review, issue tracking, transparency 源代码审查、问题跟踪与透明度 |
| Setup and usage docs 安装与使用文档                  | Users need to know how to configure it 用户需要了解如何配置它 |
| Active maintenance 活跃维护                          | Recent updates or responsive issue handling 近期更新或及时的问题处理 |

Low-effort wrappers, unclear ownership, or unmaintained packages may be declined.

​	低投入的封装、归属不明确或未维护的包可能会被拒绝。

## Related

- [Install and Configure Plugins](https://docs.openclaw.ai/tools/plugin) — how to install any plugin
- [Building Plugins](https://docs.openclaw.ai/plugins/building-plugins) — create your own
- [Plugin Manifest](https://docs.openclaw.ai/plugins/manifest) — manifest schema
