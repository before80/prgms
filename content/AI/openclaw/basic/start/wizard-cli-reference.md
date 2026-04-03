+++
title = "CLI Setup Reference"
date = 2026-04-02T20:15:18+08:00
weight = 50
type = "docs"
description = ""
isCJKLanguage = true
draft = false

+++

# CLI Setup Reference

This page is the full reference for `openclaw onboard`. For the short guide, see [Onboarding (CLI)](https://docs.openclaw.ai/start/wizard).

​	此页面是`openclaw onboard`的完整参考资料。如需简短指南，请参阅[Onboarding (CLI)](https://docs.openclaw.ai/start/wizard)。

## What the wizard does 向导的功能

Local mode (default) walks you through:

​	本地模式（默认）会引导你完成以下步骤：

- Model and auth setup (OpenAI Code subscription OAuth, Anthropic API key or setup token, plus MiniMax, GLM, Ollama, Moonshot, and AI Gateway options)

  模型与身份验证设置（OpenAI Code 订阅 OAuth、Anthropic API key 或令牌设置，以及 MiniMax、GLM、Ollama、Moonshot 与 AI Gateway 选项）

- Workspace location and bootstrap files

  工作区位置与引导文件

- Gateway settings (port, bind, auth, tailscale)

  Gateway 设置（端口、绑定、身份验证、Tailscale）

- Channels and providers (Telegram, WhatsApp, Discord, Google Chat, Mattermost plugin, Signal)

  Channels 和 providers （Telegram、WhatsApp、Discord、Google 聊天、Mattermost 插件、Signal）

- Daemon install (LaunchAgent or systemd user unit)

  守护程序安装（LaunchAgent 或 systemd 用户单元）

- Health check

- Skills setup

Remote mode configures this machine to connect to a gateway elsewhere. It does not install or modify anything on the remote host.

​	远程模式将本机配置为连接到其他位置的 gateway 。它不会在远程主机上安装或修改任何内容。

## Local flow details

1) Existing config detection 现有配置检测

- If `~/.openclaw/openclaw.json` exists, choose Keep, Modify, or Reset.
- Re-running the wizard does not wipe anything unless you explicitly choose Reset (or pass `--reset`).
- CLI `--reset` defaults to `config+creds+sessions`; use `--reset-scope full` to also remove workspace.
- If config is invalid or contains legacy keys, the wizard stops and asks you to run `openclaw doctor` before continuing.
- Reset uses `trash` and offers scopes:
  - Config only
  - Config + credentials + sessions
  - Full reset (also removes workspace)

2) Model and auth 模型与身份验证

- Full option matrix is in [Auth and model options](https://docs.openclaw.ai/start/wizard-cli-reference#auth-and-model-options).

3) Workspace 工作区

- Default `~/.openclaw/workspace` (configurable). 
- Seeds workspace files needed for first-run bootstrap ritual.
- Workspace layout: [Agent workspace](https://docs.openclaw.ai/concepts/agent-workspace).

4) Gateway

- Prompts for port, bind, auth mode, and tailscale exposure. 提示输入端口、绑定地址、认证模式以及 Tailscale 暴露设置。
- Recommended: keep token auth enabled even for loopback so local WS clients must authenticate. 建议：即使是回环连接也保持令牌认证启用，这样本地的 WebSocket 客户端就必须进行身份验证。
- In token mode, interactive setup offers: 在令牌模式下，交互式设置会提供以下选项：
  - **Generate/store plaintext token** (default) **生成/存储明文令牌**（默认）
  - **Use SecretRef** (opt-in) **使用 SecretRef**（可选启用）
- In password mode, interactive setup also supports plaintext or SecretRef storage. 在密码模式下，交互式设置也支持明文或 SecretRef 存储。
- Non-interactive token SecretRef path: `--gateway-token-ref-env <ENV_VAR>`. 非交互式令牌 SecretRef 路径：`--gateway-token-ref-env <ENV_VAR>`。
  - Requires a non-empty env var in the onboarding process environment. 需要在onboarding 流程环境中使用非空的环境变量。
  - Cannot be combined with `--gateway-token`. 不可与`--gateway-token`同时使用。
- Disable auth only if you fully trust every local process. 只有在你完全信任每一个本地进程时，才能禁用身份验证。
- Non-loopback binds still require auth. 非回环绑定仍需身份验证。

5) Channels

- [WhatsApp](https://docs.openclaw.ai/channels/whatsapp): optional QR login 可选二维码登录
- [Telegram](https://docs.openclaw.ai/channels/telegram): bot token
- [Discord](https://docs.openclaw.ai/channels/discord): bot token
- [Google Chat](https://docs.openclaw.ai/channels/googlechat): service account JSON + webhook audience
- [Mattermost](https://docs.openclaw.ai/channels/mattermost) plugin: bot token + base URL
- [Signal](https://docs.openclaw.ai/channels/signal): optional `signal-cli` install + account config
- [BlueBubbles](https://docs.openclaw.ai/channels/bluebubbles): recommended for iMessage; server URL + password + webhook
- [iMessage](https://docs.openclaw.ai/channels/imessage): legacy `imsg` CLI path + DB access
- DM security: default is pairing. First DM sends a code; approve via `openclaw pairing approve <channel> <code>` or use allowlists. 私信安全：默认配对模式。首次私信会发送验证码；可通过`openclaw pairing approve <channel> <code>`进行批准，或使用白名单。

6) Daemon install

- macOS: LaunchAgent
  - Requires logged-in user session; for headless, use a custom LaunchDaemon (not shipped). 需要登录用户会话；若要无头运行，请使用自定义的 LaunchDaemon（未随附）。
- Linux and Windows via WSL2: systemd user unit 通过 WSL2 在 Linux 和 Windows 上使用：systemd 用户单元
  - Wizard attempts `loginctl enable-linger <user>` so gateway stays up after logout.
    - 安装程序会尝试执行 `loginctl enable-linger <user>`，以便用户登出后网关仍保持运行。
  - May prompt for sudo (writes `/var/lib/systemd/linger`); it tries without sudo first.
    - 可能会要求输入 sudo 密码（会写入 `/var/lib/systemd/linger`）；程序会先尝试无需 sudo 的方式。
- Runtime selection: Node (recommended; required for WhatsApp and Telegram). Bun is not recommended.
  - 运行时选择：Node（推荐；为 WhatsApp 和 Telegram 所必需）。不推荐使用 bun。

7) Health check

- Starts gateway (if needed) and runs `openclaw health`.
  - 启动 gateway （如有需要）并运行 `openclaw health`。
- `openclaw status --deep` adds gateway health probes to status output.
  - `openclaw status --deep`会在状态输出中添加 gateway 健康探测项。

8) Skills

- Reads available skills and checks requirements.
  - 读取可用 skill 并检查相关要求。
- Lets you choose node manager: npm or pnpm (bun not recommended).
  - 允许你选择节点管理器：npm 或 pnpm（不推荐使用 bun）
- Installs optional dependencies (some use Homebrew on macOS).
  - 安装可选依赖项（在 macOS 上部分依赖项使用 Homebrew）。

9) Finish

- Summary and next steps, including iOS, Android, and macOS app options.
  - 摘要与后续步骤，包括 iOS、Android 以及 macOS 应用相关选项。



> If no GUI is detected, the wizard prints SSH port-forward instructions for the Control UI instead of opening a browser. If Control UI assets are missing, the wizard attempts to build them; fallback is `pnpm ui:build` (auto-installs UI deps).
>
> ​	如果未检测到图形用户界面（GUI），向导会打印控制界面（Control UI）的SSH端口转发说明，而非打开浏览器。若控制界面资源缺失，向导会尝试构建这些资源；备用命令为`pnpm ui:build`（自动安装界面依赖项）。

## Remote mode details

Remote mode configures this machine to connect to a gateway elsewhere.

​	远程模式会将本机配置为连接到其他位置的 gateway 。

> Remote mode does not install or modify anything on the remote host.
>
> ​	远程模式不会在远程主机上安装或修改任何内容。

What you set:

​	你所设置的内容：

- Remote gateway URL (`ws://...`)
  - 远程网关 URL（`ws://...`）
- Token if remote gateway auth is required (recommended)
  - 如果远程 gateway 需要身份验证，则输入令牌（推荐）



> - If gateway is loopback-only, use SSH tunneling or a tailnet.
>   - 如果 gateway 仅支持回环访问，请使用 SSH 隧道或 tailnet。
> - Discovery hints: 发现提示：
>   - macOS: Bonjour (`dns-sd`)
>   - Linux: Avahi (`avahi-browse`)

## Auth and model options 身份验证与模型选项

### Anthropic API key

Uses `ANTHROPIC_API_KEY` if present or prompts for a key, then saves it for daemon use.

​	如果存在`ANTHROPIC_API_KEY`则使用该密钥，否则会提示输入密钥，随后将其保存以供守护进程使用。

### Anthropic Claude CLI

Reuses a local Claude CLI login on the gateway host and switches model selection to `claude-cli/...`.

​	在 gateway 主机上复用本地 Claude CLI 登录，并将模型选择切换为 `claude-cli/...`。

- macOS: checks Keychain item “Claude Code-credentials”
  - macOS：检查 Keychain 项“Claude Code-credentials”
- Linux and Windows: reuses `~/.claude/.credentials.json` if present
  - Linux 和 Windows 系统：如果存在 `~/.claude/.credentials.json` 文件，则复用该文件

On macOS, choose “Always Allow” so launchd starts do not block.

​	在 macOS 系统上，选择“Always Allow”，这样 launchd 启动程序就不会被阻止。

### Anthropic token (setup-token paste)

Run `claude setup-token` on any machine, then paste the token. You can name it; blank uses default.

​	在任意机器上运行`claude setup-token`，然后粘贴令牌。你可以为其命名；留空则使用默认值。

### OpenAI Code subscription (Codex CLI reuse)

If `~/.codex/auth.json` exists, the wizard can reuse it.

​	如果 `~/.codex/auth.json` 文件存在，向导可以复用它。

### OpenAI Code subscription (OAuth)

Browser flow; paste `code#state`.

​	浏览器流程；粘贴 `code#state`。

Sets `agents.defaults.model` to `openai-codex/gpt-5.4` when model is unset or `openai/*`.

​	当模型未设置或为 `openai/*` 时，将 `agents.defaults.model` 设置为 `openai-codex/gpt-5.4`。

### OpenAI API key

Uses `OPENAI_API_KEY` if present or prompts for a key, then stores the credential in auth profiles. 

​	如果存在则使用 `OPENAI_API_KEY`，否则提示输入密钥，然后将凭据存储在身份验证配置文件中。

Sets `agents.defaults.model` to `openai/gpt-5.4` when model is unset, `openai/*`, or `openai-codex/*`.

​	当模型未设置、为`openai/*`或`openai-codex/*`时，将`agents.defaults.model`设置为`openai/gpt-5.4`。

### xAI (Grok) API key

Prompts for `XAI_API_KEY` and configures xAI as a model provider.

​	提示输入 `XAI_API_KEY` 并将 xAI 配置为模型提供商。

### OpenCode

Prompts for `OPENCODE_API_KEY` (or `OPENCODE_ZEN_API_KEY`) and lets you choose the Zen or Go catalog. Setup URL: [opencode.ai/auth](https://opencode.ai/auth).

​	提示输入`OPENCODE_API_KEY`（或 `OPENCODE_ZEN_API_KEY`），并让你选择 Zen 还是 Go 类目。设置网址：[opencode.ai/auth](https://opencode.ai/auth)。

### API key (generic)

Stores the key for you.

​	为你存储 key 。

### Vercel AI Gateway

Prompts for `AI_GATEWAY_API_KEY`. More detail: [Vercel AI Gateway](https://docs.openclaw.ai/providers/vercel-ai-gateway).

​	提示输入 `AI_GATEWAY_API_KEY`。更多详情：[Vercel AI Gateway](https://docs.openclaw.ai/providers/vercel-ai-gateway)。

### Cloudflare AI Gateway

Prompts for account ID, gateway ID, and `CLOUDFLARE_AI_GATEWAY_API_KEY`. More detail: [Cloudflare AI Gateway](https://docs.openclaw.ai/providers/cloudflare-ai-gateway).

​	提示输入账户 ID、gateway  ID 和 `CLOUDFLARE_AI_GATEWAY_API_KEY`。更多详情：[Cloudflare AI Gateway](https://docs.openclaw.ai/providers/cloudflare-ai-gateway)。

### MiniMax

Config is auto-written. Hosted default is `MiniMax-M2.7`. More detail: [MiniMax](https://docs.openclaw.ai/providers/minimax).

​	配置自动生成。托管默认值为 `MiniMax-M2.7`。更多详情：[MiniMax](https://docs.openclaw.ai/providers/minimax)。

### Synthetic (Anthropic-compatible)

Prompts for `SYNTHETIC_API_KEY`. More detail: [Synthetic](https://docs.openclaw.ai/providers/synthetic).

​	要求输入`SYNTHETIC_API_KEY`。更多详情：[Synthetic](https://docs.openclaw.ai/providers/synthetic)。

### Ollama (Cloud and local open models)

Prompts for base URL (default `http://127.0.0.1:11434`), then offers Cloud + Local or Local mode. Discovers available models and suggests defaults. More detail: [Ollama](https://docs.openclaw.ai/providers/ollama).

​	提示基础 URL（默认 `http://127.0.0.1:11434`），然后提供云端+本地或本地模式。检测可用模型并给出默认值。更多详情：[Ollama](https://docs.openclaw.ai/providers/ollama)。

### Moonshot and Kimi Coding

Moonshot (Kimi K2) and Kimi Coding configs are auto-written. More detail: [Moonshot AI (Kimi + Kimi Coding)](https://docs.openclaw.ai/providers/moonshot).

​	Moonshot（Kimi K2）和Kimi Coding配置已自动写入。更多详情：[Moonshot AI（Kimi + Kimi Coding）](https://docs.openclaw.ai/providers/moonshot)。

### Custom provider

Works with OpenAI-compatible and Anthropic-compatible endpoints. 

​	支持与 OpenAI 兼容和与 Anthropic 兼容的端点。

Interactive onboarding supports the same API key storage choices as other provider API key flows:

​	交互式入门流程与其他服务商的API密钥流程支持相同的API密钥存储选项：

- **Paste API key now** (plaintext) **现在粘贴API密钥**（明文）
- **Use secret reference** (env ref or configured provider ref, with preflight validation) **使用密钥引用**（环境变量引用或已配置的提供商引用，附带预检验证）

Non-interactive flags:

​	非交互式标志：

- `--auth-choice custom-api-key`
- `--custom-base-url`
- `--custom-model-id`
- `--custom-api-key` (optional; falls back to `CUSTOM_API_KEY`)
- `--custom-provider-id` (optional)
- `--custom-compatibility <openai|anthropic>` (optional; default `openai`)

### Skip

Leaves auth unconfigured.

​	保持身份验证未配置。





Model behavior: 模型行为：

- Pick default model from detected options, or enter provider and model manually.
  - 从检测到的选项中选择默认模型，或手动输入服务商和模型。
- Wizard runs a model check and warns if the configured model is unknown or missing auth.
  - 向导会运行模型检查，如果配置的模型未知或缺少身份验证，则会发出警告。

Credential and profile paths:

​	凭据和配置文件路径：

- OAuth credentials: `~/.openclaw/credentials/oauth.json`
  - OAuth 凭证：`~/.openclaw/credentials/oauth.json`
- Auth profiles (API keys + OAuth): `~/.openclaw/agents/<agentId>/agent/auth-profiles.json`
  - 授权配置文件（API keys  + OAuth）：`~/.openclaw/agents/<agentId>/agent/auth-profiles.json`

Credential storage mode:

​	凭据存储模式：

- Default onboarding behavior persists API keys as plaintext values in auth profiles.
  - 默认的首次设置行为会将 API 密钥以明文形式保存在身份验证配置文件中。
- `--secret-input-mode ref` enables reference mode instead of plaintext key storage. In interactive setup, you can choose either: `--secret-input-mode ref` 启用引用模式，而非明文密钥存储。在交互式设置中，你可以选择以下任一方式：
  - environment variable ref (for example `keyRef: { source: "env", provider: "default", id: "OPENAI_API_KEY" }`)
    - 环境变量引用（例如 `keyRef: { source: "env", provider: "default", id: "OPENAI_API_KEY" }`）
  - configured provider ref (`file` or `exec`) with provider alias + id
    - 已配置的提供程序引用（`file` 或 `exec`），带有提供程序别名 + ID
- Interactive reference mode runs a fast preflight validation before saving. 交互式引用模式会在保存前运行快速的预检验证。
  - Env refs: validates variable name + non-empty value in the current onboarding environment.
    - 环境引用：在当前的入职环境中验证变量名称以及非空值。
  - Provider refs: validates provider config and resolves the requested id.
    - 提供商引用：验证提供商配置并解析请求的 ID。
  - If preflight fails, onboarding shows the error and lets you retry.
    - 如果预检失败，入职流程会显示错误并允许你重试。
- In non-interactive mode, `--secret-input-mode ref` is env-backed only. 在非交互模式下，`--secret-input-mode ref` 仅支持环境变量支持。
  - Set the provider env var in the onboarding process environment.
    - 在onboarding 流程环境中设置提供商环境变量。
  - Inline key flags (for example `--openai-api-key`) require that env var to be set; otherwise onboarding fails fast.
    - 内联 key 标志（例如 `--openai-api-key`）要求设置对应的环境变量；否则 onboarding 流程会立即失败。
  - For custom providers, non-interactive `ref` mode stores `models.providers.<id>.apiKey` as `{ source: "env", provider: "default", id: "CUSTOM_API_KEY" }`.
    - 对于自定义提供程序，非交互式 `ref` 模式会将 `models.providers.<id>.apiKey` 存储为 `{ source: "env", provider: "default", id: "CUSTOM_API_KEY" }`。
  - In that custom-provider case, `--custom-api-key` requires `CUSTOM_API_KEY` to be set; otherwise onboarding fails fast.
    - 在自定义提供程序的情况下，`--custom-api-key` 需要设置 `CUSTOM_API_KEY`；否则 onboarding 会立即失败。
- Gateway auth credentials support plaintext and SecretRef choices in interactive setup: Gateway 身份验证凭据在交互式设置中支持明文和 SecretRef 两种选择：
  - Token mode: **Generate/store plaintext token** (default) or **Use SecretRef**.
    - 令牌模式：**生成/存储明文令牌**（默认）或 **使用 SecretRef**。
  - Password mode: plaintext or SecretRef.
    - 密码模式：明文或 SecretRef。
- Non-interactive token SecretRef path: `--gateway-token-ref-env <ENV_VAR>`.
  - 非交互式令牌 SecretRef 路径：`--gateway-token-ref-env <ENV_VAR>`。
- Existing plaintext setups continue to work unchanged.
  - 现有的明文设置将继续保持不变运行。



> Headless and server tip: complete OAuth on a machine with a browser, then copy `~/.openclaw/credentials/oauth.json` (or `$OPENCLAW_STATE_DIR/credentials/oauth.json`) to the gateway host.
>
> ​	无头模式和服务器提示：在带有浏览器的机器上完成 OAuth 授权，然后将`~/.openclaw/credentials/oauth.json`（或 `$OPENCLAW_STATE_DIR/credentials/oauth.json`）复制到网关节点主机。

## Outputs and internals 输出与内部组件

Typical fields in `~/.openclaw/openclaw.json`:

​	~/.openclaw/openclaw.json 中的典型字段：

- `agents.defaults.workspace`
- `agents.defaults.model` / `models.providers` (if Minimax chosen)
- `tools.profile` (local onboarding defaults to `"coding"` when unset; existing explicit values are preserved)
  - `tools.profile`（本地初始设置未设置时默认为 `"coding"`；现有的显式值将保留）
- `gateway.*` (mode, bind, auth, tailscale)
- `session.dmScope` (local onboarding defaults this to `per-channel-peer` when unset; existing explicit values are preserved)
  - `session.dmScope`（本地注册在未设置时会将其默认设为 `per-channel-peer`；现有的显式值会保留）
- `channels.telegram.botToken`, `channels.discord.token`, `channels.matrix.*`, `channels.signal.*`, `channels.imessage.*`
- Channel allowlists (Slack, Discord, Matrix, Microsoft Teams) when you opt in during prompts (names resolve to IDs when possible)
  - Channel 白名单（Slack、Discord、Matrix、Microsoft Teams）：在提示环节选择加入时（名称会尽可能解析为 ID）
- `skills.install.nodeManager`
- `wizard.lastRunAt`
- `wizard.lastRunVersion`
- `wizard.lastRunCommit`
- `wizard.lastRunCommand`
- `wizard.lastRunMode`

`openclaw agents add` writes `agents.list[]` and optional `bindings`.

​	`openclaw agents add` 会写入 `agents.list[]` 以及可选的 `bindings`。

WhatsApp credentials go under `~/.openclaw/credentials/whatsapp/<accountId>/`. Sessions are stored under `~/.openclaw/agents/<agentId>/sessions/`.

​	WhatsApp 凭据存放在 `~/.openclaw/credentials/whatsapp/<accountId>/` 目录下。会话存放在 `~/.openclaw/agents/<agentId>/sessions/` 目录下。



> Some channels are delivered as plugins. When selected during setup, the wizard prompts to install the plugin (npm or local path) before channel configuration.
>
> ​	部分channels 以插件形式提供。在安装过程中选择该channel 时，安装向导会提示先安装插件（npm 或本地路径），再进行 channel 配置。

Gateway wizard RPC:

​	Gateway 向导远程过程调用：

- `wizard.start`
- `wizard.next`
- `wizard.cancel`
- `wizard.status`

Clients (macOS app and Control UI) can render steps without re-implementing onboarding logic. Signal setup behavior:

​	客户端（macOS 应用程序和控制界面）可渲染步骤，无需重新实现 onboarding 流程逻辑。 Signal 安装设置行为：

- Downloads the appropriate release asset
  - 下载相应的发布资源
- Stores it under `~/.openclaw/tools/signal-cli/<version>/`
  - 将其存储在 `~/.openclaw/tools/signal-cli/<version>/` 目录下
- Writes `channels.signal.cliPath` in config
  - 在配置中写入 `channels.signal.cliPath`
- JVM builds require Java 21
  - JVM 构建需要 Java 21
- Native builds are used when available
  - 有可用的原生构建时则使用原生构建
- Windows uses WSL2 and follows Linux signal-cli flow inside WSL
  - Windows 使用 WSL2，并在 WSL 内部遵循 Linux 版本的 signal-cli 流程

## Related docs

- Onboarding hub: [Onboarding (CLI)](https://docs.openclaw.ai/start/wizard)
- Automation and scripts: [CLI Automation](https://docs.openclaw.ai/start/wizard-cli-automation)
- Command reference: [`openclaw onboard`](https://docs.openclaw.ai/cli/onboard)
