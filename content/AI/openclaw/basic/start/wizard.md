+++
title = "Onboarding (CLI)"
date = 2026-04-02T19:48:32+08:00
weight = 30
type = "docs"
description = ""
isCJKLanguage = true
draft = false

+++

# Onboarding (CLI)

CLI onboarding is the **recommended** way to set up OpenClaw on macOS, Linux, or Windows (via WSL2; strongly recommended). It configures a local Gateway or a remote Gateway connection, plus channels, skills, and workspace defaults in one guided flow.

​	CLI onboarding  接入是在 macOS、Linux 或 Windows（通过 WSL2；强烈推荐）上设置 OpenClaw 的**推荐**方式。它可在一个引导流程中配置本地 Gateway 或远程 Gateway 连接，以及 channels、skills 和 workspace 默认设置。

```sh
openclaw onboard
```



> Fastest first chat: open the Control UI (no channel setup needed). Run `openclaw dashboard` and chat in the browser. Docs: [Dashboard](https://docs.openclaw.ai/web/dashboard).
>
> ​	最快首次聊天：打开控制界面（无需设置频道）。运行`openclaw dashboard`并在浏览器中聊天。文档：[仪表板](https://docs.openclaw.ai/web/dashboard)。

To reconfigure later:

​	后续如需重新配置：

```sh
openclaw configure
openclaw agents add <name>
```



> `--json` does not imply non-interactive mode. For scripts, use `--non-interactive`.
>
> ​	`--json` 并不代表非交互模式。对于脚本，请使用 `--non-interactive`。



> CLI onboarding includes a web search step where you can pick a provider (Perplexity, Brave, Gemini, Grok, or Kimi) and paste your API key so the agent can use `web_search`. You can also configure this later with `openclaw configure --section web`. Docs: [Web tools](https://docs.openclaw.ai/tools/web).
>
> ​	CLI onboarding 包含一个网页搜索步骤，你可以在此步骤中选择一个服务商（Perplexity、Brave、Gemini、Grok 或 Kimi）并粘贴你的 API 密钥，以便智能体使用`web_search`功能。你也可以后续通过`openclaw configure --section web`进行配置。文档：[Web tools](https://docs.openclaw.ai/tools/web)。

## QuickStart vs Advanced

Onboarding starts with **QuickStart** (defaults) vs **Advanced** (full control).

​	首次设置以**QuickStart**（默认设置）和**Advanced**（完全自定义）两种方式开始。

{{< tabpane text=true persist=disabled >}}

{{% tab "QuickStart (defaults)" %}}

- Local gateway (loopback)
- Workspace default (or existing workspace)
- Gateway port **18789**
- Gateway auth **Token** (auto‑generated, even on loopback)
- Tool policy default for new local setups: `tools.profile: "coding"` (existing explicit profile is preserved)
- 本地环境的工具策略默认值：`tools.profile: "coding"`（现有的显式配置文件将保留）
- DM isolation default: local onboarding writes `session.dmScope: "per-channel-peer"` when unset. Details: [CLI Setup Reference](https://docs.openclaw.ai/start/wizard-cli-reference#outputs-and-internals)
- DM(**Direct Message（私信 / 私聊）**) 隔离默认值：未设置时，本地登录会写入 `session.dmScope: "per-channel-peer"`。详细信息：[CLI Setup Reference](https://docs.openclaw.ai/start/wizard-cli-reference#outputs-and-internals)
- Tailscale exposure **Off**
- Tailscale 暴露 **关闭**
- Telegram + WhatsApp DMs default to **allowlist** (you’ll be prompted for your phone number)
- Telegram 和 WhatsApp 私信默认采用**白名单**模式（系统会提示你输入电话号码）

{{% /tab %}}

{{% tab "Windows (PowerShell)" %}}

- Exposes every step (mode, workspace, gateway, channels, daemon, skills)

{{% /tab %}}

{{< /tabpane >}}

## What onboarding configures

**Local mode (default)** walks you through these steps:

​	**本地模式（默认）** 将引导您完成以下步骤：

1. **Model/Auth** — choose any supported provider/auth flow (API key, OAuth, or setup-token), including Custom Provider (OpenAI-compatible, Anthropic-compatible, or Unknown auto-detect). Pick a default model. Security note: if this agent will run tools or process webhook/hooks content, prefer the strongest latest-generation model available and keep tool policy strict. Weaker/older tiers are easier to prompt-inject. For non-interactive runs, `--secret-input-mode ref` stores env-backed refs in auth profiles instead of plaintext API key values. In non-interactive `ref` mode, the provider env var must be set; passing inline key flags without that env var fails fast. In interactive runs, choosing secret reference mode lets you point at either an environment variable or a configured provider ref (`file` or `exec`), with a fast preflight validation before saving.

   **模型/身份验证**——选择任意受支持的提供商/身份验证流程（API 密钥、OAuth 或设置令牌），包括自定义提供商（兼容 OpenAI、兼容 Anthropic 或未知自动检测）。选择一个默认模型。安全说明：如果该代理将运行工具或处理webhook/hooks内容，优先使用可用的最新一代最强模型，并严格执行工具策略。较弱/较旧的模型更容易受到提示注入攻击。对于非交互式运行，`--secret-input-mode ref`会将环境变量支持的引用存储在身份验证配置文件中，而非明文 API 密钥值。在非交互式`ref`模式下，必须设置提供商环境变量；未设置该环境变量而直接传入密钥标志会立即失败。在交互式运行中，选择秘密引用模式可指向环境变量或已配置的提供商引用（`file`或`exec`），并在保存前进行快速预检验证。

2. **Workspace** — Location for agent files (default `~/.openclaw/workspace`). Seeds bootstrap files.

   **工作区** — 代理文件的存放位置（默认值 `~/.openclaw/workspace`）。包含引导文件。

3. **Gateway** — Port, bind address, auth mode, Tailscale exposure. In interactive token mode, choose default plaintext token storage or opt into SecretRef. Non-interactive token SecretRef path: `--gateway-token-ref-env <ENV_VAR>`.

   **网关** — 端口、绑定地址、认证模式、Tailscale 暴露。在交互式令牌模式下，选择默认的明文令牌存储或启用 SecretRef。非交互式令牌 SecretRef 路径：`--gateway-token-ref-env <ENV_VAR>`。

4. **Channels** — WhatsApp, Telegram, Discord, Google Chat, Mattermost, Signal, BlueBubbles, or iMessage.

   **Channels**——WhatsApp、Telegram、Discord、Google Chat、Mattermost、Signal、BlueBubbles 或 iMessage。

5. **Daemon** — Installs a LaunchAgent (macOS) or systemd user unit (Linux/WSL2). If token auth requires a token and `gateway.auth.token` is SecretRef-managed, daemon install validates it but does not persist the resolved token into supervisor service environment metadata. If token auth requires a token and the configured token SecretRef is unresolved, daemon install is blocked with actionable guidance. If both `gateway.auth.token` and `gateway.auth.password` are configured and `gateway.auth.mode` is unset, daemon install is blocked until mode is set explicitly.

   **守护进程** — 会安装 LaunchAgent（macOS 系统）或 systemd 用户单元（Linux/WSL2 系统）。如果令牌身份验证需要令牌，且`gateway.auth.token`由 SecretRef 管理，守护进程安装会对其进行验证，但不会将解析后的令牌持久化到 supervisor 服务的环境元数据中。如果令牌身份验证需要令牌，且配置的令牌 SecretRef 未解析，守护进程安装将被阻止，并提供可操作的指导。如果同时配置了`gateway.auth.token`和`gateway.auth.password`，且`gateway.auth.mode`未设置，守护进程安装将被阻止，直到显式设置该模式。

6. **Health check** — Starts the Gateway and verifies it’s running.

   **健康检查** — 启动网关并验证其是否正在运行。

7. **Skills** — Installs recommended skills and optional dependencies.

   **技能** — 安装推荐的技能和可选依赖项。



> Re-running onboarding does **not** wipe anything unless you explicitly choose **Reset** (or pass `--reset`). CLI `--reset` defaults to config, credentials, and sessions; use `--reset-scope full` to include workspace. If the config is invalid or contains legacy keys, onboarding asks you to run `openclaw doctor` first.
>
> ​	重新运行onboarding 流程**不会**删除任何内容，除非你明确选择**Reset**（或传入`--reset`）。CLI `--reset`默认重置配置、凭证和会话；使用`--reset-scope full`可包含工作区。如果配置无效或包含旧版密钥，onboarding 流程会要求你先运行`openclaw doctor`。

**Remote mode** only configures the local client to connect to a Gateway elsewhere. It does **not** install or change anything on the remote host.

​	**远程模式**仅配置本地客户端连接到其他位置的网关。它不会在远程主机上**安装**或更改任何内容。

## Add another agent

Use `openclaw agents add <name>` to create a separate agent with its own workspace, sessions, and auth profiles. Running without `--workspace` launches onboarding. What it sets:

​	使用 `openclaw agents add <name>` 可创建一个独立的智能体，它拥有自己的工作空间、会话和身份验证配置文件。不带 `--workspace` 运行时会启动 onboarding 流程。它所设置的内容：

- `agents.list[].name`
- `agents.list[].workspace`
- `agents.list[].agentDir`

Notes:

- Default workspaces follow `~/.openclaw/workspace-<agentId>`.
- Add `bindings` to route inbound messages (onboarding can do this).
- 添加`bindings`以路由入站消息（onboarding  流程可完成此操作）。
- Non-interactive flags: `--model`, `--agent-dir`, `--bind`, `--non-interactive`.
- 非交互式标志：`--model`、`--agent-dir`、`--bind`、`--non-interactive`。

## reference

For detailed step-by-step breakdowns and config outputs, see [CLI Setup Reference](https://docs.openclaw.ai/start/wizard-cli-reference). For non-interactive examples, see [CLI Automation](https://docs.openclaw.ai/start/wizard-cli-automation). For the deeper technical reference, including RPC details, see [Onboarding Reference](https://docs.openclaw.ai/reference/wizard).

​	如需详细的分步说明和配置输出，请参阅[CLI Setup Reference](https://docs.openclaw.ai/start/wizard-cli-reference)。非交互式示例请参阅[CLI Automation](https://docs.openclaw.ai/start/wizard-cli-automation)。包含 RPC 详细信息的深入技术参考请参阅[Onboarding Reference](https://docs.openclaw.ai/reference/wizard)。

## docs

- CLI command reference: [`openclaw onboard`](https://docs.openclaw.ai/cli/onboard)

- Onboarding overview: [Onboarding Overview](https://docs.openclaw.ai/start/onboarding-overview)

- macOS app onboarding: [Onboarding](https://docs.openclaw.ai/start/onboarding)

- Agent first-run ritual: [Agent Bootstrapping](https://docs.openclaw.ai/start/bootstrapping)

  代理首次启动流程：[代理引导](https://docs.openclaw.ai/start/bootstrapping)
