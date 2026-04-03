+++
title = "Tools & Plugins"
date = 2026-04-02T16:32:56+08:00
weight = 50
type = "docs"
description = ""
isCJKLanguage = true
draft = false

+++

# Tools and Plugins

Everything the agent does beyond generating text happens through **tools**. Tools are how the agent reads files, runs commands, browses the web, sends messages, and interacts with devices.

​	agent 除生成文本外的所有操作都通过**工具**完成。工具是 agent 读取文件、运行命令、浏览网页、发送消息以及与设备交互的方式。

## Tools, skills, and plugins

OpenClaw has three layers that work together:

​	OpenClaw 有三个协同工作的层级：

1) Tools are what the agent calls 工具是 agent 所调用的对象

A tool is a typed function the agent can invoke (e.g. `exec`, `browser`, `web_search`, `message`). OpenClaw ships a set of **built-in tools** and plugins can register additional ones. The agent sees tools as structured function definitions sent to the model API. 工具是智能体可调用的带类型函数（例如 `exec`、`browser`、`web_search`、`message`）。OpenClaw 自带一组 **内置工具**，插件可注册额外的工具。 智能体将工具视为发送至模型 API 的结构化函数定义。

2) Skills teach the agent when and how - Skills 教会智能体何时以及如何行动

A skill is a markdown file (`SKILL.md`) injected into the system prompt. Skills give the agent context, constraints, and step-by-step guidance for using tools effectively. Skills live in your workspace, in shared folders, or ship inside plugins.

​	技能是一个注入到系统提示词中的 Markdown 文件（`SKILL.md`）。技能为智能体提供上下文、约束条件，以及有效使用工具的分步指导。技能可以存放在你的工作区、共享文件夹中，也可以内置在插件里。

[Skills reference](https://docs.openclaw.ai/tools/skills) | [Creating skills](https://docs.openclaw.ai/tools/creating-skills) 

3) Plugins package everything together 插件将所有内容整合在一起

A plugin is a package that can register any combination of capabilities: channels, model providers, tools, skills, speech, image generation, and more. Some plugins are **core** (shipped with OpenClaw), others are **external** (published on npm by the community).

​	插件是一个可以注册任意功能组合的包：channels、模型提供商、工具、skills、语音、图像生成等等。一些插件是**核心**插件（随 OpenClaw 一同发布），另一些是**外部**插件（由社区发布在 npm 上）。

[Install and configure plugins](https://docs.openclaw.ai/tools/plugin) | [Build your own](https://docs.openclaw.ai/plugins/building-plugins)

## Built-in tools 内置工具

These tools ship with OpenClaw and are available without installing any plugins:

​	这些工具随 OpenClaw 一同提供，无需安装任何插件即可使用：

| Tool                                    | What it does                                                 | Page                                                         |
| :-------------------------------------- | :----------------------------------------------------------- | :----------------------------------------------------------- |
| `exec` / `process`                      | Run shell commands, manage background processes 运行 Shell 命令，管理后台进程 | [Exec](https://docs.openclaw.ai/tools/exec)                  |
| `code_execution`                        | Run sandboxed remote Python analysis 运行沙箱化的远程 Python 分析 | [Code Execution](https://docs.openclaw.ai/tools/code-execution) |
| `browser`                               | Control a Chromium browser (navigate, click, screenshot) 控制 Chromium 浏览器（导航、点击、截图） | [Browser](https://docs.openclaw.ai/tools/browser)            |
| `web_search` / `x_search` / `web_fetch` | Search the web, search X posts, fetch page content 搜索网页、搜索 X 平台帖子、获取页面内容 | [Web](https://docs.openclaw.ai/tools/web)                    |
| `read` / `write` / `edit`               | File I/O in the workspace 工作区中的文件输入输出             |                                                              |
| `apply_patch`                           | Multi-hunk file patches 多块文件补丁                         | [Apply Patch](https://docs.openclaw.ai/tools/apply-patch)    |
| `message`                               | Send messages across all channels 跨所有channels 发送消息    | [Agent Send](https://docs.openclaw.ai/tools/agent-send)      |
| `canvas`                                | Drive node Canvas (present, eval, snapshot) 驱动节点画布（展示、执行、快照） |                                                              |
| `nodes`                                 | Discover and target paired devices  发现并定位配对设备       |                                                              |
| `cron` / `gateway`                      | Manage scheduled jobs, restart gateway 管理计划任务，重启网关 |                                                              |
| `image` / `image_generate`              | Analyze or generate images 分析或生成图片                    |                                                              |
| `sessions_*` / `agents_list`            | Session management, sub-agents 会话管理、子智能体            | [Sub-agents](https://docs.openclaw.ai/tools/subagents)       |

For image work, use `image` for analysis and `image_generate` for generation or editing. If you target `openai/*`, `google/*`, `fal/*`, or another non-default image provider, configure that provider’s auth/API key first.

​	对于图像相关操作，使用 `image` 进行分析，使用 `image_generate` 进行生成或编辑。如果你的目标是 `openai/*`、`google/*`、`fal/*` 或其他非默认图像提供商，请先配置该提供商的身份auth/API key。

### Plugin-provided tools 插件提供的工具

Plugins can register additional tools. Some examples:

​	插件可以注册额外的工具。以下是一些示例：

- [Lobster](https://docs.openclaw.ai/tools/lobster) — typed workflow runtime with resumable approvals 支持可恢复审批的强类型工作流运行时
- [LLM Task](https://docs.openclaw.ai/tools/llm-task) — JSON-only LLM step for structured output 仅输出 JSON 格式的大语言模型步骤，用于生成结构化结果
- [Diffs](https://docs.openclaw.ai/tools/diffs) — diff viewer and renderer 差异查看与渲染工具
- [OpenProse](https://docs.openclaw.ai/prose) — markdown-first workflow orchestration 以Markdown为核心的工作流编排

## Tool configuration

### Allow and deny lists 允许列表与拒绝列表

Control which tools the agent can call via `tools.allow` / `tools.deny` in config. Deny always wins over allow.

​	在配置中通过 `tools.allow` / `tools.deny` 控制智能体可调用的工具。拒绝规则的优先级始终高于允许规则。

```json
{
  tools: {
    allow: ["group:fs", "browser", "web_search"],
    deny: ["exec"],
  },
}
```

### Tool profiles 工具配置

`tools.profile` sets a base allowlist before `allow`/`deny` is applied. Per-agent override: `agents.list[].tools.profile`.

​	`tools.profile` 在应用 `allow`/`deny` 之前设置基础允许列表。单代理覆盖：`agents.list[].tools.profile`。

| Profile     | What it includes                                             |
| :---------- | :----------------------------------------------------------- |
| `full`      | All tools (default) 所有工具（默认）<- 现在默认应该是`coding` |
| `coding`    | File I/O, runtime, sessions, memory, image 文件输入/输出、运行时、会话、内存、镜像 |
| `messaging` | Messaging, session list/history/send/status 消息传递、会话列表/历史记录/发送/状态 |
| `minimal`   | `session_status` only                                        |

### Tool groups 工具组

Use `group:*` shorthands in allow/deny lists:

​	在允许/拒绝列表中使用 `group:*` 简写：

| Group              | Tools                                                        |
| :----------------- | :----------------------------------------------------------- |
| `group:runtime`    | exec, bash, process, code_execution                          |
| `group:fs`         | read, write, edit, apply_patch                               |
| `group:sessions`   | sessions_list, sessions_history, sessions_send, sessions_spawn, sessions_yield, subagents, session_status |
| `group:memory`     | memory_search, memory_get                                    |
| `group:web`        | web_search, x_search, web_fetch                              |
| `group:ui`         | browser, canvas                                              |
| `group:automation` | cron, gateway                                                |
| `group:messaging`  | message                                                      |
| `group:nodes`      | nodes                                                        |
| `group:openclaw`   | All built-in OpenClaw tools (excludes plugin tools) 所有内置的 OpenClaw 工具（不包含插件工具） |

### Provider-specific restrictions 提供商特定限制

Use `tools.byProvider` to restrict tools for specific providers without changing global defaults:

​	使用 `tools.byProvider` 来限制特定提供商的工具，而不更改全局默认值：

```json
{
  tools: {
    profile: "coding",
    byProvider: {
      "google-antigravity": { profile: "minimal" },
    },
  },
}
```
