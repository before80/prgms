+++
title = "Uninstall"
date = 2026-04-03T09:40:49+08:00
weight = 1
type = "docs"
description = ""
isCJKLanguage = true
draft = false

+++

# Uninstall

Two paths:

​	两种方法：

- **Easy path** if `openclaw` is still installed.
  - **简易方法**（前提是 `openclaw` 仍已安装）

- **Manual service removal** if the CLI is gone but the service is still running.
  - **手动移除服务**，适用于 CLI 已消失但服务仍在运行的情况。


## Easy path (CLI still installed)

Recommended: use the built-in uninstaller:

​	推荐使用内置卸载程序：

```sh
openclaw uninstall
```

Non-interactive (automation / npx):

​	非交互式（自动化 / npx 模式）：

```sh
openclaw uninstall --all --yes --non-interactive
npx -y openclaw uninstall --all --yes --non-interactive
```

Manual steps (same result):

​	手动步骤（结果相同）：

1. Stop the gateway service: 停止网关服务：

```sh
openclaw gateway stop
```

2) Uninstall the gateway service (launchd/systemd/schtasks):

```sh
openclaw gateway uninstall
```

3) Delete state + config: 删除状态和配置：

```sh
rm -rf "${OPENCLAW_STATE_DIR:-$HOME/.openclaw}"
```

If you set `OPENCLAW_CONFIG_PATH` to a custom location outside the state dir, delete that file too.

​	如果你将 `OPENCLAW_CONFIG_PATH` 设置为状态 state 之外的自定义位置，请也删除该文件。

4) Delete your workspace (optional, removes agent files): 删除你的工作区（可选，会删除 agent 文件）：

```sh
rm -rf ~/.openclaw/workspace
```

5) Remove the CLI install (pick the one you used):  卸载 CLI 安装程序（选择你使用的安装方式）：

```sh
npm rm -g openclaw
pnpm remove -g openclaw
bun remove -g openclaw
```

6) If you installed the macOS app: 如果你安装了 macOS 应用：

```sh
rm -rf /Applications/OpenClaw.app
```

> Notes:
>
> - If you used profiles (`--profile` / `OPENCLAW_PROFILE`), repeat step 3 for each state dir (defaults are `~/.openclaw-<profile>`).
>   - 如果你使用了配置文件（`--profile` / `OPENCLAW_PROFILE`），请对每个 state 目录重复步骤 3（默认目录为 `~/.openclaw-<profile>`）
>
> - In remote mode, the state dir lives on the **gateway host**, so run steps 1-4 there too.
>   - 在远程模式下，state 目录位于**gateway 主机**上，因此也请在该主机上执行第 1 至 4 步。
>
>

## Manual service removal (CLI not installed)

> 这里的CLI, 就是通过 `npm install -g openclaw`、`pnpm add -g openclaw` 或 `bun install -g openclaw` 全局安装的那个!

Use this if the gateway service keeps running but `openclaw` is missing.

​	如果 gateway 服务持续运行但缺少 `openclaw`，请使用此方法。

### macOS (launchd)

Default label is `ai.openclaw.gateway` (or `ai.openclaw.<profile>`; legacy `com.openclaw.*` may still exist):

​	默认标签为 `ai.openclaw.gateway`（或 `ai.openclaw.<profile>`；旧版 `com.openclaw.*` 可能仍存在）：

```sh
launchctl bootout gui/$UID/ai.openclaw.gateway
rm -f ~/Library/LaunchAgents/ai.openclaw.gateway.plist
```

If you used a profile, replace the label and plist name with `ai.openclaw.<profile>`. Remove any legacy `com.openclaw.*` plists if present.

​	如果你使用了配置文件，请将标签和 plist 名称替换为`ai.openclaw.<profile>`。如果存在任何旧版的`com.openclaw.*` plist，请将其删除。

### Linux (systemd user unit)

Default unit name is `openclaw-gateway.service` (or `openclaw-gateway-<profile>.service`):

​	默认单元名称为 `openclaw-gateway.service`（或 `openclaw-gateway-<profile>.service`）：

```sh
systemctl --user disable --now openclaw-gateway.service
rm -f ~/.config/systemd/user/openclaw-gateway.service
systemctl --user daemon-reload
```

### Windows (Scheduled Task) （计划任务）

Default task name is `OpenClaw Gateway` (or `OpenClaw Gateway (<profile>)`). The task script lives under your state dir.

​	默认任务名称为 `OpenClaw Gateway`（或 `OpenClaw Gateway (<profile>)`）。任务脚本位于你的 state 目录下。

```sh
schtasks /Delete /F /TN "OpenClaw Gateway"
Remove-Item -Force "$env:USERPROFILE\.openclaw\gateway.cmd"
```

If you used a profile, delete the matching task name and `~\.openclaw-<profile>\gateway.cmd`.

​	如果你使用了配置文件，请删除对应的任务名称和 `~\.openclaw-<profile>\gateway.cmd`。

## Normal install vs source checkout 常规安装与源码检出对比

### Normal install (install.sh / npm / pnpm / bun)

If you used `https://openclaw.ai/install.sh` or `install.ps1`, the CLI was installed with `npm install -g openclaw@latest`. Remove it with `npm rm -g openclaw` (or `pnpm remove -g` / `bun remove -g` if you installed that way).

​	如果你使用了 `https://openclaw.ai/install.sh` 或 `install.ps1`，则 CLI 是通过 `npm install -g openclaw@latest` 安装的。可使用 `npm rm -g openclaw`（若通过其他方式安装，可使用 `pnpm remove -g` 或 `bun remove -g`）将其卸载。

### Source checkout (git clone)

If you run from a repo checkout (`git clone` + `openclaw ...` / `bun run openclaw ...`):

​	如果你从仓库签出运行（`git clone` + `openclaw ...` / `bun run openclaw ...`）：

1. Uninstall the gateway service **before** deleting the repo (use the easy path above or manual service removal).

   在删除仓库之前**卸载 ** gateway 服务（使用上方的简易步骤或手动删除服务）。

2. Delete the repo directory.

3. Remove state + workspace as shown above.

   按上述步骤删除 state 和工作区。
