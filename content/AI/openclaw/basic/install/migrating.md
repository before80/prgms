+++
title = "Migrating"
date = 2026-04-03T11:12:24+08:00
weight = 1
type = "docs"
description = ""
isCJKLanguage = true
draft = false

+++

# Migration Guide 迁移指南

This guide moves an OpenClaw gateway to a new machine without redoing onboarding.

​	本指南可将 OpenClaw gateway 迁移到新机器，且无需重新完成 onboarding配置。

## What Gets Migrated 需要迁移的内容

When you copy the **state directory** (`~/.openclaw/` by default) and your **workspace**, you preserve:

​	当你复制 **state 目录**（默认情况下为 `~/.openclaw/`）和你的 **工作区** 时，你会保留：

- **Config** — `openclaw.json` and all gateway settings
  - **配置** — `openclaw.json` 以及所有gateway 设置
- **Auth** — API keys, OAuth tokens, credential profiles
  - **认证** — API 密钥、OAuth 令牌、凭证配置文件
- **Sessions** — conversation history and agent state
  - **会话** — 对话历史与 agent 状态
- **Channel state** — WhatsApp login, Telegram session, etc.
  - **Channel 状态** — WhatsApp 登录、Telegram 会话等
- **Workspace files** — `MEMORY.md`, `USER.md`, skills, and prompts
  - **工作区文件** — `MEMORY.md`、`USER.md`、技能和提示词



> Run `openclaw status` on the old machine to confirm your state directory path. Custom profiles use `~/.openclaw-<profile>/` or a path set via `OPENCLAW_STATE_DIR`.
>
> ​	在旧机器上运行`openclaw status`以确认你的 state 目录路径。自定义配置文件使用`~/.openclaw-<profile>/`或通过`OPENCLAW_STATE_DIR`设置的路径。

## Migration Steps 迁移步骤

1) Stop the gateway and back up 停止 gateway 并进行备份

On the **old** machine, stop the gateway so files are not changing mid-copy, then archive:

​	在旧机器上，停止 gateway 以防止文件在复制过程中发生变化，然后进行归档：

```sh
openclaw gateway stop
cd ~
tar -czf openclaw-state.tgz .openclaw
```

If you use multiple profiles (e.g. `~/.openclaw-work`), archive each separately.

​	如果你使用多个配置文件（例如 `~/.openclaw-work`），请分别对每个进行归档。

2) Install OpenClaw on the new machine 在新机器上安装 OpenClaw

[Install](https://docs.openclaw.ai/install) the CLI (and Node if needed) on the new machine. It is fine if onboarding creates a fresh `~/.openclaw/` — you will overwrite it next.

​	在新机器上[安装](https://docs.openclaw.ai/install)命令行界面（如需，同时安装 Node）。如果 onboarding 过程新建了一个全新的 `~/.openclaw/` 目录也没关系——你接下来会覆盖它。

3) Copy state directory and workspace 复制状态目录和工作区

Transfer the archive via `scp`, `rsync -a`, or an external drive, then extract:

​	通过 `scp`、`rsync -a` 或外部驱动器传输归档文件，然后进行解压：

```sh
cd ~
tar -xzf openclaw-state.tgz
```

Ensure hidden directories were included and file ownership matches the user that will run the gateway.

​	确保已包含隐藏目录，且文件所有者与将运行网关的用户一致。

4) Run doctor and verify 运行 doctor 并进行验证

On the new machine, run [Doctor](https://docs.openclaw.ai/gateway/doctor) to apply config migrations and repair services:

​	在新机器上运行 [Doctor](https://docs.openclaw.ai/gateway/doctor) 以应用配置迁移并修复服务：

```sh
openclaw doctor
openclaw gateway restart
openclaw status
```

## Common Pitfalls 常见问题

### Profile or state-dir mismatch 配置文件或 state目录不匹配

If the old gateway used `--profile` or `OPENCLAW_STATE_DIR` and the new one does not, channels will appear logged out and sessions will be empty. Launch the gateway with the **same** profile or state-dir you migrated, then rerun `openclaw doctor`.

​	如果旧 gateway 使用了 `--profile` 或 `OPENCLAW_STATE_DIR` 而新gateway 未使用，通道会显示为已注销状态，且会话将为空。使用迁移时所用的 **相同** 配置文件或状态目录启动网关，然后重新运行 `openclaw doctor`。

### Copying only openclaw.json

The config file alone is not enough. Credentials live under `credentials/`, and agent state lives under `agents/`. Always migrate the **entire** state directory.

​	仅靠配置文件是不够的。凭证存放在`credentials/`目录下，agent  状态存放在`agents/`目录下。请始终迁移**整个 **state 目录。

### Permissions and ownership 权限与所有权

If you copied as root or switched users, the gateway may fail to read credentials. Ensure the state directory and workspace are owned by the user running the gateway.

​	如果你以 root 用户身份复制或切换了用户，网关可能无法读取凭据。请确保 state 目录和工作区归运行 gateway的用户所有。

### Remote mode

If your UI points at a **remote** gateway, the remote host owns sessions and workspace. Migrate the gateway host itself, not your local laptop. See [FAQ](https://docs.openclaw.ai/help/faq#where-things-live-on-disk).

​	如果你的用户界面指向一个**远程** gateway，那么远程主机拥有会话和工作区。请迁移 gateway主机本身，而非你的本地笔记本电脑。请查看[常见问题解答](https://docs.openclaw.ai/help/faq#where-things-live-on-disk)。

### Secrets in backups 备份中的密钥

The state directory contains API keys, OAuth tokens, and channel credentials. Store backups encrypted, avoid insecure transfer channels, and rotate keys if you suspect exposure.

​	state 目录包含API密钥、OAuth令牌和频道凭据。对备份进行加密处理，避免使用不安全的传输 channels，若怀疑密钥泄露请及时轮换密钥。

## Verification Checklist 验证清单

On the new machine, confirm:

​	在新设备上，请确认：

-  `openclaw status` shows the gateway running `openclaw status` 显示gateway 正在运行
-  Channels are still connected (no re-pairing needed) Channels 仍保持连接（无需重新配对）
-  The dashboard opens and shows existing sessions 仪表板可正常打开并显示现有会话
-  Workspace files (memory, configs) are present 工作区文件（内存、配置）均存在
