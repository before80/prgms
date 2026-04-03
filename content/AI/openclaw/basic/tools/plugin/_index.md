+++
title = "Plugins"
date = 2026-04-03T12:54:40+08:00
weight = 1
type = "docs"
description = ""
isCJKLanguage = true
draft = false

+++

# Plugins

Plugins extend OpenClaw with new capabilities: channels, model providers, tools, skills, speech, image generation, and more. Some plugins are **core** (shipped with OpenClaw), others are **external** (published on npm by the community).

​	插件为 OpenClaw 扩展了新功能：通道、模型提供商、工具、技能、语音、图像生成等。部分插件为**核心插件**（随 OpenClaw 一同发布），其余为**外部插件**（由社区发布在 npm 上）。

## Quick start

1) See what is loaded 查看已加载的内容

```sh
openclaw plugins list
```

2) Install a plugin 安装插件

```sh
# From npm
openclaw plugins install @openclaw/voice-call

# From a local directory or archive
openclaw plugins install ./my-plugin
openclaw plugins install ./my-plugin.tgz
```

3) Restart the Gateway 重启网关

```
openclaw gateway restart
```

Then configure under `plugins.entries.\<id\>.config` in your config file.

​	然后在你的配置文件中的 `plugins.entries.\<id\>.config` 下进行配置。

If you prefer chat-native control, enable `commands.plugins: true` and use:

​	如果你更偏好原生聊天控制，请启用`commands.plugins: true`并使用：

```sh
/plugin install clawhub:@openclaw/voice-call
/plugin show voice-call
/plugin enable voice-call
```

The install path uses the same resolver as the CLI: local path/archive, explicit `clawhub:<pkg>`, or bare package spec (ClawHub first, then npm fallback).

​	安装路径使用与 CLI 相同的解析器：本地路径/归档文件、显式的`clawhub:<pkg>`，或裸包规范（优先使用 ClawHub，然后回退到 npm）。

## Plugin types 插件类型

OpenClaw recognizes two plugin formats:

​	OpenClaw 支持两种插件格式：

| Format     | How it works                                                 | Examples                                                     |
| :--------- | :----------------------------------------------------------- | :----------------------------------------------------------- |
| **Native** | `openclaw.plugin.json` + runtime module; executes in-process `openclaw.plugin.json` + 运行时模块；在进程内执行 | Official plugins, community npm packages 官方插件、社区 npm 包 |
| **Bundle** | Codex/Claude/Cursor-compatible layout; mapped to OpenClaw features 与 Codex/Claude/Cursor 兼容的布局；映射至 OpenClaw 功能 | `.codex-plugin/`, `.claude-plugin/`, `.cursor-plugin/`       |

Both show up under `openclaw plugins list`. See [Plugin Bundles](https://docs.openclaw.ai/plugins/bundles) for bundle details.If you are writing a native plugin, start with [Building Plugins](https://docs.openclaw.ai/plugins/building-plugins) and the [Plugin SDK Overview](https://docs.openclaw.ai/plugins/sdk-overview).

​	两者都会显示在`openclaw plugins list`中。有关插件包的详细信息，请参阅[插件包](https://docs.openclaw.ai/plugins/bundles)。如果你正在编写原生插件，请从[构建插件](https://docs.openclaw.ai/plugins/building-plugins)和[插件 SDK 概述](https://docs.openclaw.ai/plugins/sdk-overview)开始。

##  Official plugins  官方插件

### Installable (npm)  可安装（npm）

| Plugin          | Package                | Docs                                                         |
| :-------------- | :--------------------- | :----------------------------------------------------------- |
| Matrix          | `@openclaw/matrix`     | [Matrix](https://docs.openclaw.ai/channels/matrix)           |
| Microsoft Teams | `@openclaw/msteams`    | [Microsoft Teams](https://docs.openclaw.ai/channels/msteams) |
| Nostr           | `@openclaw/nostr`      | [Nostr](https://docs.openclaw.ai/channels/nostr)             |
| Voice Call      | `@openclaw/voice-call` | [Voice Call](https://docs.openclaw.ai/plugins/voice-call)    |
| Zalo            | `@openclaw/zalo`       | [Zalo](https://docs.openclaw.ai/channels/zalo)               |
| Zalo Personal   | `@openclaw/zalouser`   | [Zalo Personal](https://docs.openclaw.ai/plugins/zalouser)   |

###  Core (shipped with OpenClaw) 核心（随 OpenClaw 附带）

### Model providers (enabled by default)

`anthropic`, `byteplus`, `cloudflare-ai-gateway`, `github-copilot`, `google`, `huggingface`, `kilocode`, `kimi-coding`, `minimax`, `mistral`, `modelstudio`, `moonshot`, `nvidia`, `openai`, `opencode`, `opencode-go`, `openrouter`, `qianfan`, `synthetic`, `together`, `venice`, `vercel-ai-gateway`, `volcengine`, `xiaomi`, `zai`

### Memory plugins

- `memory-core` — bundled memory search (default via `plugins.slots.memory`) 内置内存搜索（默认通过 `plugins.slots.memory` 调用）
- `memory-lancedb` — install-on-demand long-term memory with auto-recall/capture (set `plugins.slots.memory = "memory-lancedb"`) 按需安装的长期记忆功能，支持自动回忆/捕获（设置 `plugins.slots.memory = "memory-lancedb"`）

### Speech providers (enabled by default)

`elevenlabs`, `microsoft`

### Other

- `browser` — bundled browser plugin for the browser tool, `openclaw browser` CLI, `browser.request` gateway method, browser runtime, and default browser control service (enabled by default; disable before replacing it) 适用于浏览器工具的捆绑式浏览器插件、`openclaw browser`命令行界面、`browser.request`网关方法、浏览器运行时以及默认浏览器控制服务（默认启用；替换前请先禁用）
- `copilot-proxy` — VS Code Copilot Proxy bridge (disabled by default) VS Code 副驾驶代理桥（默认禁用）

Looking for third-party plugins? See [Community Plugins](https://docs.openclaw.ai/plugins/community).)

​	寻找第三方插件？请查看[社区插件](https://docs.openclaw.ai/plugins/community)。

## Configuration  配置



```json
{
  plugins: {
    enabled: true,
    allow: ["voice-call"],
    deny: ["untrusted-plugin"],
    load: { paths: ["~/Projects/oss/voice-call-extension"] },
    entries: {
      "voice-call": { enabled: true, config: { provider: "twilio" } },
    },
  },
}
```

| Field            | Description                                                  |
| :--------------- | :----------------------------------------------------------- |
| `enabled`        | Master toggle (default: `true`) 总开关（默认：`true`）       |
| `allow`          | Plugin allowlist (optional) 插件白名单（可选）               |
| `deny`           | Plugin denylist (optional; deny wins) 插件拒绝列表（可选；拒绝规则优先级更高） |
| `load.paths`     | Extra plugin files/directories 额外的插件文件/目录           |
| `slots`          | Exclusive slot selectors (e.g. `memory`, `contextEngine`) 专属插槽选择器（例如 `memory`、`contextEngine`） |
| `entries.\<id\>` | Per-plugin toggles + config 单插件开关 + 配置                |

Config changes **require a gateway restart**. If the Gateway is running with config watch + in-process restart enabled (the default `openclaw gateway` path), that restart is usually performed automatically a moment after the config write lands.

​	配置更改**需要重启网关**。如果网关在启用了配置监控+进程内重启的情况下运行（默认的`openclaw gateway`路径），该重启通常会在配置写入完成后立即自动执行。

> Plugin states: disabled vs missing vs invalid 插件状态：已禁用、缺失或无效
>
> - **Disabled**: plugin exists but enablement rules turned it off. Config is preserved. 
>   - 插件存在，但启用规则将其关闭。配置已保留。
> - **Missing**: config references a plugin id that discovery did not find. 
>   - 配置引用了一个未被发现机制找到的插件 ID。
> - **Invalid**: plugin exists but its config does not match the declared schema.
>   - 插件存在，但其配置与声明的架构不匹配。

## Discovery and precedence 发现与优先级

OpenClaw scans for plugins in this order (first match wins):

​	OpenClaw 按以下顺序扫描插件（第一个匹配项生效）：

1) Config paths 配置路径

`plugins.load.paths` — explicit file or directory paths. 明确的文件或目录路径。

2) Workspace extensions 工作区扩展

`\<workspace\>/.openclaw/<plugin-root>/*.ts` and `\<workspace\>/.openclaw/<plugin-root>/*/index.ts`.

3) Global extensions 全局扩展

`~/.openclaw/<plugin-root>/*.ts` and `~/.openclaw/<plugin-root>/*/index.ts`.

4) Bundled plugins 捆绑插件

Shipped with OpenClaw. Many are enabled by default (model providers, speech). Others require explicit enablement.

​	随 OpenClaw 一同预装。其中多项默认启用（模型提供商、语音功能），其余则需手动启用。

### Enablement rules 启用规则

- `plugins.enabled: false` disables all plugins  禁用所有插件
- `plugins.deny` always wins over allow 的优先级始终高于插件允许
- `plugins.entries.\<id\>.enabled: false` disables that plugin 会禁用该插件
- Workspace-origin plugins are **disabled by default** (must be explicitly enabled) 
  - 工作区来源的插件默认**处于禁用状态**（必须手动启用）

- Bundled plugins follow the built-in default-on set unless overridden
  - 除非被覆盖，否则捆绑插件遵循内置的默认启用设置

- Exclusive slots can force-enable the selected plugin for that slot
  - 专属插槽可强制为该插槽启用选定的插件


## Plugin slots (exclusive categories) 插件槽（排他性类别）

Some categories are exclusive (only one active at a time):

​	部分类别为互斥状态（同一时间仅能有一个处于激活状态）：

```json
{
  plugins: {
    slots: {
      memory: "memory-core", // or "none" to disable
      contextEngine: "legacy", // or a plugin id
    },
  },
}
```

| Slot            | What it controls      | Default             |
| :-------------- | :-------------------- | :------------------ |
| `memory`        | Active memory plugin  | `memory-core`       |
| `contextEngine` | Active context engine | `legacy` (built-in) |

## CLI reference



```sh
openclaw plugins list                    # compact inventory
openclaw plugins inspect <id>            # deep detail
openclaw plugins inspect <id> --json     # machine-readable
openclaw plugins status                  # operational summary
openclaw plugins doctor                  # diagnostics

openclaw plugins install <package>        # install (ClawHub first, then npm)
openclaw plugins install clawhub:<pkg>   # install from ClawHub only
openclaw plugins install <path>          # install from local path
openclaw plugins install -l <path>       # link (no copy) for dev
openclaw plugins install <spec> --dangerously-force-unsafe-install
openclaw plugins update <id>             # update one plugin
openclaw plugins update --all            # update all

openclaw plugins enable <id>
openclaw plugins disable <id>
```

`--dangerously-force-unsafe-install` is a break-glass override for false positives from the built-in dangerous-code scanner. It allows installs to continue past built-in `critical` findings, but it still does not bypass plugin `before_install` policy blocks or scan-failure blocking.

​	`--dangerously-force-unsafe-install` 是用于覆盖内置危险代码扫描工具误报的紧急覆盖选项。它允许安装程序跳过内置的 `critical` 发现项，但仍无法绕过插件的 `before_install` 策略阻止或扫描失败阻止。

This CLI flag applies to plugin installs only. Gateway-backed skill dependency installs use the matching `dangerouslyForceUnsafeInstall` request override instead, while `openclaw skills install` remains the separate ClawHub skill download/install flow.

​	此 CLI 标志仅适用于插件安装。依赖网关的技能安装改用匹配的 ``dangerouslyForceUnsafeInstall`` 请求覆盖，而 ``openclaw skills install`` 仍是独立的 ClawHub 技能下载/安装流程。

See [`openclaw plugins` CLI reference](https://docs.openclaw.ai/cli/plugins) for full details.

​	请查看[`openclaw plugins`命令行界面参考](https://docs.openclaw.ai/cli/plugins)以获取完整详细信息。

## Plugin API overview 插件 API 概述

Plugins export either a function or an object with `register(api)`:

​	插件要么导出一个函数，要么导出一个包含 `register(api)` 的对象：

```ts
export default definePluginEntry({
  id: "my-plugin",
  name: "My Plugin",
  register(api) {
    api.registerProvider({
      /* ... */
    });
    api.registerTool({
      /* ... */
    });
    api.registerChannel({
      /* ... */
    });
  },
});
```

Common registration methods:

​	常用注册方法：

| Method                               | What it registers    |
| :----------------------------------- | :------------------- |
| `registerProvider`                   | Model provider (LLM) |
| `registerChannel`                    | Chat channel         |
| `registerTool`                       | Agent tool           |
| `registerHook` / `on(...)`           | Lifecycle hooks      |
| `registerSpeechProvider`             | Text-to-speech / STT |
| `registerMediaUnderstandingProvider` | Image/audio analysis |
| `registerImageGenerationProvider`    | Image generation     |
| `registerWebSearchProvider`          | Web search           |
| `registerHttpRoute`                  | HTTP endpoint        |
| `registerCommand` / `registerCli`    | CLI commands         |
| `registerContextEngine`              | Context engine       |
| `registerService`                    | Background service   |

Hook guard behavior for typed lifecycle hooks:

​	针对类型化生命周期钩子的钩子保护行为：

- `before_tool_call`: `{ block: true }` is terminal; lower-priority handlers are skipped.
  - `before_tool_call`：`{ block: true }` 为终端；低优先级的处理程序将被跳过。

- `before_tool_call`: `{ block: false }` is a no-op and does not clear an earlier block.
  - `before_tool_call`：`{ block: false }` 是无操作指令，且不会清除先前的阻止状态。

- `before_install`: `{ block: true }` is terminal; lower-priority handlers are skipped.
  - `before_install`：`{ block: true }` 为终止状态；低优先级处理程序将被跳过。

- `before_install`: `{ block: false }` is a no-op and does not clear an earlier block.
  - `before_install`：`{ block: false }` 是无操作指令，且不会清除先前的阻塞设置。

- `message_sending`: `{ cancel: true }` is terminal; lower-priority handlers are skipped.
  - `message_sending`：`{ cancel: true }` 为终端状态；将跳过低优先级的处理程序。

- `message_sending`: `{ cancel: false }` is a no-op and does not clear an earlier cancel.
  - `message_sending`：`{ cancel: false }` 是无操作指令，不会清除先前的取消操作。


For full typed hook behavior, see [SDK Overview](https://docs.openclaw.ai/plugins/sdk-overview#hook-decision-semantics).

​	有关完整的类型化钩子行为，请参阅[SDK 概述](https://docs.openclaw.ai/plugins/sdk-overview#hook-decision-semantics)。

## Related

- [Building Plugins](https://docs.openclaw.ai/plugins/building-plugins) — create your own plugin 创建你自己的插件
- [Plugin Bundles](https://docs.openclaw.ai/plugins/bundles) — Codex/Claude/Cursor bundle compatibility - Codex/Claude/Cursor 包兼容性
- [Plugin Manifest](https://docs.openclaw.ai/plugins/manifest) — manifest schema 清单架构
- [Registering Tools](https://docs.openclaw.ai/plugins/building-plugins#registering-agent-tools) — add agent tools in a plugin 在插件中添加智能体工具
- [Plugin Internals](https://docs.openclaw.ai/plugins/architecture) — capability model and load pipeline 能力模型与加载流程
- [Community Plugins](https://docs.openclaw.ai/plugins/community) — third-party listings 第三方列表
