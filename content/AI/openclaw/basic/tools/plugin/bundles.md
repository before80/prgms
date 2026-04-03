+++
title = "bundles"
date = 2026-04-03T15:15:56+08:00
weight = 1
type = "docs"
description = ""
isCJKLanguage = true
draft = false

+++

# Plugin Bundles

OpenClaw can install plugins from three external ecosystems: **Codex**, **Claude**, and **Cursor**. These are called **bundles** — content and metadata packs that OpenClaw maps into native features like skills, hooks, and MCP tools.

​	OpenClaw 可以从三个外部生态系统安装插件：**Codex**、**Claude** 和 **Cursor**。这些被称为 **插件包**——OpenClaw 会将其中的内容和元数据包映射为技能、钩子和 MCP 工具等原生功能。

> Bundles are **not** the same as native OpenClaw plugins. Native plugins run in-process and can register any capability. Bundles are content packs with selective feature mapping and a narrower trust boundary.
>
> ​	捆绑包与原生 OpenClaw 插件**不同**。原生插件在进程内运行，可注册任何功能。捆绑包是带有选择性功能映射且信任边界更窄的内容包。

## Why bundles exist 为何需要捆绑包

Many useful plugins are published in Codex, Claude, or Cursor format. Instead of requiring authors to rewrite them as native OpenClaw plugins, OpenClaw detects these formats and maps their supported content into the native feature set. This means you can install a Claude command pack or a Codex skill bundle and use it immediately.

​	许多实用的插件以 Codex、Claude 或 Cursor 格式发布。OpenClaw 无需要求开发者将其重写为原生 OpenClaw 插件，而是能识别这些格式并将其支持的内容映射到原生功能集。这意味着你可以安装 Claude 命令包或 Codex 技能包并立即使用。

## Install a bundle 安装插件包

1) Install from a directory, archive, or marketplace

​	从目录、归档文件或应用市场安装

```sh
# Local directory
openclaw plugins install ./my-bundle

# Archive
openclaw plugins install ./my-bundle.tgz

# Claude marketplace
openclaw plugins marketplace list <marketplace-name>
openclaw plugins install <plugin-name>@<marketplace-name>
```

2) Verify detection

​	验证检测

```sh
openclaw plugins list
openclaw plugins inspect <id>
```

Bundles show as `Format: bundle` with a subtype of `codex`, `claude`, or `cursor`.

​	捆绑包显示为`Format: bundle`，子类型为`codex`、`claude`或`cursor`。

3) Restart and use

​	重启并使用

```sh
openclaw gateway restart
```

Mapped features (skills, hooks, MCP tools) are available in the next session.

​	已映射的功能（技能、钩子、MCP 工具）将在下一个会话中可用。

## What OpenClaw maps from bundles OpenClaw 从捆绑包中映射的内容

Not every bundle feature runs in OpenClaw today. Here is what works and what is detected but not yet wired.

​	并非所有的捆绑包功能如今都能在 OpenClaw 中运行。以下是可正常使用的功能，以及已被检测到但尚未配置的功能。

### Supported now

| Feature       | How it maps                                                  | Applies to     |
| :------------ | :----------------------------------------------------------- | :------------- |
| Skill content | Bundle skill roots load as normal OpenClaw skills 将技能根目录作为普通 OpenClaw 技能加载 | All formats    |
| Commands      | `commands/` and `.cursor/commands/` treated as skill roots `commands/` 和 `.cursor/commands/` 被视为技能根目录 | Claude, Cursor |
| Hook packs    | OpenClaw-style `HOOK.md` + `handler.ts` layouts              | Codex          |
| MCP tools     | Bundle MCP config merged into embedded Pi settings; supported stdio and HTTP servers loaded 将 MCP 配置打包合并到嵌入式 Pi 设置中；加载支持的标准输入输出和 HTTP 服务器 | All formats    |
| Settings      | Claude `settings.json` imported as embedded Pi defaults - Claude 的 `settings.json` 已作为嵌入式 Pi 默认值导入 | Claude         |

#### Skill content 技能内容

- bundle skill roots load as normal OpenClaw skill roots
  - 将技能根目录打包加载，与正常的 OpenClaw 技能根目录加载方式一致

- Claude `commands` roots are treated as additional skill roots
  - Claude 的 `commands` 根被视为额外的技能根

- Cursor `.cursor/commands` roots are treated as additional skill roots
  - Cursor `.cursor/commands` 根被视为额外的技能根


This means Claude markdown command files work through the normal OpenClaw skill loader. Cursor command markdown works through the same path.

​	这意味着 Claude 的 Markdown 命令文件通过标准的 OpenClaw 技能加载器运行。光标命令 Markdown 也通过相同的路径运行。

#### Hook packs

- bundle hook roots work **only** when they use the normal OpenClaw hook-pack layout. Today this is primarily the Codex-compatible case: 仅当使用标准 OpenClaw 挂钩包布局时，捆绑挂钩根目录才起作用。目前这主要适用于与 Codex 兼容的情况：
  - `HOOK.md`
  - `handler.ts` or `handler.js`

#### MCP for Pi

- enabled bundles can contribute MCP server config
  - 已启用的捆绑包可提供 MCP 服务器配置

- OpenClaw merges bundle MCP config into the effective embedded Pi settings as `mcpServers`
  - OpenClaw 将捆绑包的 MCP 配置合并到有效的嵌入式 Pi 配置中，作为`mcpServers`

- OpenClaw exposes supported bundle MCP tools during embedded Pi agent turns by launching stdio servers or connecting to HTTP servers
  - OpenClaw 在嵌入式 Pi 代理运行期间，通过启动标准输入输出服务器或连接 HTTP 服务器，公开受支持的捆绑式 MCP 工具

- project-local Pi settings still apply after bundle defaults, so workspace settings can override bundle MCP entries when needed
  - 捆绑包默认值生效后，项目本地的 Pi 设置仍然适用，因此工作区设置可在需要时覆盖捆绑包的 MCP 条目


##### Transports

MCP servers can use stdio or HTTP transport: **Stdio** launches a child process:

​	MCP 服务器可使用标准输入输出或超文本传输协议传输方式：**标准输入输出** 启动一个子进程：

```json
{
  "mcp": {
    "servers": {
      "my-server": {
        "command": "node",
        "args": ["server.js"],
        "env": { "PORT": "3000" }
      }
    }
  }
}
```

**HTTP** connects to a running MCP server over `sse` by default, or `streamable-http` when requested:

​	**HTTP** 默认通过 `sse` 连接到正在运行的 MCP 服务器，或在请求时使用 `streamable-http` 连接：

```json
{
  "mcp": {
    "servers": {
      "my-server": {
        "url": "http://localhost:3100/mcp",
        "transport": "streamable-http",
        "headers": {
          "Authorization": "Bearer ${MY_SECRET_TOKEN}"
        },
        "connectionTimeoutMs": 30000
      }
    }
  }
}
```

- `transport` may be set to `"streamable-http"` or `"sse"`; when omitted, OpenClaw uses `sse`
  - `transport`可设置为`"streamable-http"`或`"sse"`；若省略，OpenClaw将使用`sse`

- only `http:` and `https:` URL schemes are allowed
  - 仅允许 `http:` 和 `https:` 协议的 URL

- `headers` values support `${ENV_VAR}` interpolation
  - `headers`的值支持`${ENV_VAR}`插值

- a server entry with both `command` and `url` is rejected
  - 同时包含`command`和`url`的服务器条目将被拒绝

- URL credentials (userinfo and query params) are redacted from tool descriptions and logs
  - URL 凭据（用户信息和查询参数）会从工具描述和日志中进行脱敏处理

- `connectionTimeoutMs` overrides the default 30-second connection timeout for both stdio and HTTP transports
  - `connectionTimeoutMs` 会覆盖标准输入输出和 HTTP 传输的默认 30 秒连接超时时间


##### Tool naming

OpenClaw registers bundle MCP tools with provider-safe names in the form `serverName__toolName`. For example, a server keyed `"vigil-harbor"` exposing a `memory_search` tool registers as `vigil-harbor__memory_search`.

​	OpenClaw 以`serverName__toolName`的形式为工具包 MCP 工具注册提供方安全名称。例如，一个键为`"vigil-harbor"`的服务器公开了`memory_search`工具，其注册名称为`vigil-harbor__memory_search`。

- characters outside `A-Za-z0-9_-` are replaced with `-`
  - 不在 `A-Za-z0-9_-` 范围内的字符将被替换为 `-`

- server prefixes are capped at 30 characters
  - 服务器前缀最多限制为30个字符

- full tool names are capped at 64 characters
  - 工具名称的完整名称最多为64个字符

- empty server names fall back to `mcp`
  - 空服务器名称将回退到`mcp`

- colliding sanitized names are disambiguated with numeric suffixes
  - 冲突的规范化名称会通过数字后缀进行区分


#### Embedded Pi settings

- Claude `settings.json` is imported as default embedded Pi settings when the bundle is enabled
  - 启用捆绑包后，Claude 的 `settings.json` 会作为默认的嵌入式 Pi 设置导入

- OpenClaw sanitizes shell override keys before applying them
  - OpenClaw 会在应用外壳覆盖密钥前对其进行清理


Sanitized keys:

​	已清理的键值：

- `shellPath`
- `shellCommandPrefix`

### Detected but not executed 已检测但未执行

These are recognized and shown in diagnostics, but OpenClaw does not run them:

​	这些已在诊断信息中识别并显示，但 OpenClaw 不会运行它们：

- Claude `agents`, `hooks.json` automation, `lspServers`, `outputStyles`
- Cursor `.cursor/agents`, `.cursor/hooks.json`, `.cursor/rules`
- Codex inline/app metadata beyond capability reporting
  - Codex 内联/应用元数据超出功能报告范围


## Bundle formats

#### Codex bundles

Markers: `.codex-plugin/plugin.json`

Optional content: `skills/`, `hooks/`, `.mcp.json`, `.app.json` 

Codex bundles fit OpenClaw best when they use skill roots and OpenClaw-style hook-pack directories (`HOOK.md` + `handler.ts`).

​	当 Codex 捆绑包使用技能根目录和 OpenClaw 风格的钩子包目录（`HOOK.md` + `handler.ts`）时，最适合 OpenClaw。

### Claude bundles

Two detection modes:

​	两种检测模式：

- **Manifest-based:** `.claude-plugin/plugin.json`
- **Manifestless:** default Claude layout (`skills/`, `commands/`, `agents/`, `hooks/`, `.mcp.json`, `settings.json`)

Claude-specific behavior:

​	Claude 专属行为：

- `commands/` is treated as skill content
  - `commands/` 被视为技能内容

- `settings.json` is imported into embedded Pi settings (shell override keys are sanitized)
  - `settings.json`会被导入到嵌入式 Pi 的设置中（外壳覆盖键会经过清理）

- `.mcp.json` exposes supported stdio tools to embedded Pi
  - `.mcp.json` 向嵌入式 Pi 暴露受支持的标准输入输出工具

- `hooks/hooks.json` is detected but not executed
  - `hooks/hooks.json` 会被检测到但不会被执行

- Custom component paths in the manifest are additive (they extend defaults, not replace them)
  - 清单中的自定义组件路径是累加性的（它们扩展默认路径，而非替换默认路径）


#### Cursor bundles

Markers: `.cursor-plugin/plugin.json`

Optional content: `skills/`, `.cursor/commands/`, `.cursor/agents/`, `.cursor/rules/`, `.cursor/hooks.json`, `.mcp.json`

- `.cursor/commands/` is treated as skill content
  - `.cursor/commands/` 被视为技能内容

- `.cursor/rules/`, `.cursor/agents/`, and `.cursor/hooks.json` are detect-only
  - `.cursor/rules/`、`.cursor/agents/`和`.cursor/hooks.json`仅用于检测


## Detection precedence 检测优先级

OpenClaw checks for native plugin format first:

​	OpenClaw 优先检查原生插件格式：

1. `openclaw.plugin.json` or valid `package.json` with `openclaw.extensions` — treated as **native plugin**

   `openclaw.plugin.json` 或包含 `openclaw.extensions` 的有效 `package.json` — 被视为 **原生插件**

2. Bundle markers (`.codex-plugin/`, `.claude-plugin/`, or default Claude/Cursor layout) — treated as **bundle**

   捆绑标记（`.codex-plugin/`、`.claude-plugin/` 或默认的 Claude/Cursor 布局）—— 视为**捆绑**

If a directory contains both, OpenClaw uses the native path. This prevents dual-format packages from being partially installed as bundles.

​	如果一个目录同时包含这两种文件，OpenClaw 会使用原生路径。这可避免双格式软件包作为捆绑包被部分安装。

## Security 安全

Bundles have a narrower trust boundary than native plugins:

​	捆绑包的信任边界比原生插件更窄：

- OpenClaw does **not** load arbitrary bundle runtime modules in-process
  - OpenClaw 不会在进程内加载任意的捆绑包运行时模块

- Skills and hook-pack paths must stay inside the plugin root (boundary-checked)
  - 技能和钩子包路径必须保留在插件根目录内（已进行边界检查）

- Settings files are read with the same boundary checks
  - 设置文件的读取也会执行相同的边界检查

- Supported stdio MCP servers may be launched as subprocesses
  - 支持的标准输入输出 MCP 服务器可作为子进程启动


This makes bundles safer by default, but you should still treat third-party bundles as trusted content for the features they do expose.

​	这使捆绑包默认更安全，但你仍应将第三方捆绑包视为其公开功能所对应的可信内容。



## Troubleshooting 故障排除

### Bundle is detected but capabilities do not run

Run `openclaw plugins inspect <id>`. If a capability is listed but marked as not wired, that is a product limit — not a broken install.

​	运行 `openclaw plugins inspect <id>`。如果某个功能已列出但标记为未连接，则这是产品限制 — 而非安装损坏。

### Claude command files do not appear

Make sure the bundle is enabled and the markdown files are inside a detected `commands/` or `skills/` root.

​	确保已启用捆绑包，且 Markdown 文件位于检测到的`commands/`或`skills/`根目录下。

### Claude settings do not apply

Only embedded Pi settings from `settings.json` are supported. OpenClaw does not treat bundle settings as raw config patches.

​	仅支持来自`settings.json`的嵌入式 Pi 设置。OpenClaw 不会将捆绑包设置视为原始配置补丁。

### Claude hooks do not execute

`hooks/hooks.json` is detect-only. If you need runnable hooks, use the OpenClaw hook-pack layout or ship a native plugin.

​	`hooks/hooks.json` 仅用于检测。若需要可运行的钩子，请使用 theOpenClaw 钩子包布局或发布原生插件。

## Related

- [Install and Configure Plugins](https://docs.openclaw.ai/tools/plugin)
- [Building Plugins](https://docs.openclaw.ai/plugins/building-plugins) — create a native plugin
- [Plugin Manifest](https://docs.openclaw.ai/plugins/manifest) — native manifest schema
