+++
title = "CLI Automation"
date = 2026-04-02T20:15:41+08:00
weight = 60
type = "docs"
description = ""
isCJKLanguage = true
draft = false

+++

# CLI Automation

Use `--non-interactive` to automate `openclaw onboard`.

​	使用`--non-interactive`来自动化执行`openclaw onboard`。

> `--json` does not imply non-interactive mode. Use `--non-interactive` (and `--workspace`) for scripts.
>
> ​	`--json` 并不意味着非交互模式。在脚本中请使用 `--non-interactive`（以及 `--workspace`）。

## Baseline non-interactive example



```sh
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice apiKey \
  --anthropic-api-key "$ANTHROPIC_API_KEY" \
  --secret-input-mode plaintext \
  --gateway-port 18789 \
  --gateway-bind loopback \
  --install-daemon \
  --daemon-runtime node \
  --skip-skills
```

Add `--json` for a machine-readable summary.

​	添加 `--json` 以获取机器可读的摘要。

Use `--secret-input-mode ref` to store env-backed refs in auth profiles instead of plaintext values. Interactive selection between env refs and configured provider refs (`file` or `exec`) is available in the onboarding flow.

​	使用 `--secret-input-mode ref` 将环境变量支持的引用存储在身份验证配置文件中，而非明文值。在onboarding 流程中可在环境变量引用与已配置的 provider 引用（`file` 或 `exec`）之间进行交互式选择。

In non-interactive `ref` mode, provider env vars must be set in the process environment. Passing inline key flags without the matching env var now fails fast. Example:

​	在非交互式`ref`模式下，提供程序的环境变量必须在进程环境中设置。现在，若在未匹配对应环境变量的情况下传入内联密钥标志，会立即失败。示例：

```sh
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice openai-api-key \
  --secret-input-mode ref \
  --accept-risk
```

## Provider-specific examples

### Gemini example

```sh
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice gemini-api-key \
  --gemini-api-key "$GEMINI_API_KEY" \
  --gateway-port 18789 \
  --gateway-bind loopback
```

### Z.AI example

```sh
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice zai-api-key \
  --zai-api-key "$ZAI_API_KEY" \
  --gateway-port 18789 \
  --gateway-bind loopback
```

### Vercel AI Gateway example

```sh
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice ai-gateway-api-key \
  --ai-gateway-api-key "$AI_GATEWAY_API_KEY" \
  --gateway-port 18789 \
  --gateway-bind loopback
```

### Cloudflare AI Gateway example

```sh
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice cloudflare-ai-gateway-api-key \
  --cloudflare-ai-gateway-account-id "your-account-id" \
  --cloudflare-ai-gateway-gateway-id "your-gateway-id" \
  --cloudflare-ai-gateway-api-key "$CLOUDFLARE_AI_GATEWAY_API_KEY" \
  --gateway-port 18789 \
  --gateway-bind loopback
```

### Moonshot example

```sh
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice moonshot-api-key \
  --moonshot-api-key "$MOONSHOT_API_KEY" \
  --gateway-port 18789 \
  --gateway-bind loopback
```

### Mistral example

```sh
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice mistral-api-key \
  --mistral-api-key "$MISTRAL_API_KEY" \
  --gateway-port 18789 \
  --gateway-bind loopback
```

### Synthetic example

```sh
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice synthetic-api-key \
  --synthetic-api-key "$SYNTHETIC_API_KEY" \
  --gateway-port 18789 \
  --gateway-bind loopback
```



### OpenCode example

```sh
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice opencode-zen \
  --opencode-zen-api-key "$OPENCODE_API_KEY" \
  --gateway-port 18789 \
  --gateway-bind loopback
```

Swap to `--auth-choice opencode-go --opencode-go-api-key "$OPENCODE_API_KEY"` for the Go catalog.

​	切换到`--auth-choice opencode-go --opencode-go-api-key "$OPENCODE_API_KEY"`以使用 Go 目录。

### Ollama example

```sh
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice ollama \
  --custom-model-id "qwen3.5:27b" \
  --accept-risk \
  --gateway-port 18789 \
  --gateway-bind loopback
```

### Custom provider example

```sh
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice custom-api-key \
  --custom-base-url "https://llm.example.com/v1" \
  --custom-model-id "foo-large" \
  --custom-api-key "$CUSTOM_API_KEY" \
  --custom-provider-id "my-custom" \
  --custom-compatibility anthropic \
  --gateway-port 18789 \
  --gateway-bind loopback
```

`--custom-api-key` is optional. If omitted, onboarding checks `CUSTOM_API_KEY`.

​	`--custom-api-key`为可选参数。如果省略该参数，onboarding  流程会检查 `CUSTOM_API_KEY`。

Ref-mode variant:

​	参考模式变体：

```sh
export CUSTOM_API_KEY="your-key"
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice custom-api-key \
  --custom-base-url "https://llm.example.com/v1" \
  --custom-model-id "foo-large" \
  --secret-input-mode ref \
  --custom-provider-id "my-custom" \
  --custom-compatibility anthropic \
  --gateway-port 18789 \
  --gateway-bind loopback
```

In this mode, onboarding stores `apiKey` as `{ source: "env", provider: "default", id: "CUSTOM_API_KEY" }`.

​	在此模式下，onboarding  流程会将 `apiKey` 配置为 `{ source: "env", provider: "default", id: "CUSTOM_API_KEY" }`。

## Add another agent

Use `openclaw agents add <name>` to create a separate agent with its own workspace, sessions, and auth profiles. Running without `--workspace` launches the wizard.

​	使用 `openclaw agents add <name>` 创建一个独立的智能体，它拥有自己的工作区、会话和身份验证配置文件。不带 `--workspace` 运行将启动配置向导。

```sh
openclaw agents add work \
  --workspace ~/.openclaw/workspace-work \
  --model openai/gpt-5.2 \
  --bind whatsapp:biz \
  --non-interactive \
  --json
```

What it sets:

​	它所设置的内容：

- `agents.list[].name`
- `agents.list[].workspace`
- `agents.list[].agentDir`

Notes:

- Default workspaces follow `~/.openclaw/workspace-<agentId>`.
- Add `bindings` to route inbound messages (the wizard can do this).
  - 添加`bindings`以路由入站消息（向导可完成此操作）。
- Non-interactive flags: `--model`, `--agent-dir`, `--bind`, `--non-interactive`.
  - 非交互式标志：`--model`、`--agent-dir`、`--bind`、`--non-interactive`。

## Related docs

- Onboarding hub: [Onboarding (CLI)](/AI/openclaw/basic/start/wizard)
- Full reference: [CLI Setup Reference](wizard-cli-reference)
- Command reference: [`openclaw onboard`](https://docs.openclaw.ai/cli/onboard)
