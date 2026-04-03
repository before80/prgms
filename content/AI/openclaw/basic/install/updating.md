+++
title = "Updating"
date = 2026-04-03T09:36:17+08:00
weight = 1
type = "docs"
description = ""
isCJKLanguage = true
draft = false

+++

# Updating

Keep OpenClaw up to date.

## Recommended: `openclaw update`

The fastest way to update. It detects your install type (npm or git), fetches the latest version, runs `openclaw doctor`, and restarts the gateway.

​	最快的更新方式。它会检测你的安装类型（npm 或 git），获取最新版本，运行 `openclaw doctor` 并重启网关。

```sh
openclaw update
```

To switch channels or target a specific version:

​	要切换渠道或指定特定版本：

```sh
openclaw update --channel beta
openclaw update --tag main
openclaw update --dry-run   # preview without applying
```

See [Development channels](https://docs.openclaw.ai/install/development-channels) for channel semantics.

​	有关版本通道的含义，请参阅[Development channels](https://docs.openclaw.ai/install/development-channels)。

## Alternative: re-run the installer 另一种方式：重新运行安装程序

```sh
curl -fsSL https://openclaw.ai/install.sh | bash
```

Add `--no-onboard` to skip onboarding. For source installs, pass `--install-method git --no-onboard`.

​	添加 `--no-onboard` 可跳过初始设置。对于源码安装，请传递 `--install-method git --no-onboard`。

> 即:
>
> ```sh
> curl -fsSL https://openclaw.ai/install.sh | bash -s -- --no-onboard
> ```
>
> 和
>
> ```sh
> curl -fsSL https://openclaw.ai/install.sh | bash -s -- --install-method git --no-onboard
> ```
>
> 

> 在Windows上的相关命令如下:
>
> ```sh
> irm https://openclaw.ai/install.ps1 | iex -Args --no-onboard
> ```
>
> 和
>
> ```sh
> irm https://openclaw.ai/install.ps1 | iex -Args --install-method,git,--no-onboard
> ```
>
> 

## Alternative: manual npm or pnpm 替代方案：手动使用 npm 或 pnpm

```sh
npm i -g openclaw@latest
```



```sh
pnpm add -g openclaw@latest
```

## Auto-updater

The auto-updater is off by default. Enable it in `~/.openclaw/openclaw.json`:

​	自动更新程序默认处于关闭状态。请在 `~/.openclaw/openclaw.json` 中启用它：

```json
{
  update: {
    channel: "stable",
    auto: {
      enabled: true,
      stableDelayHours: 6,
      stableJitterHours: 12,
      betaCheckIntervalHours: 1,
    },
  },
}
```

| Channel  | Behavior                                                     |
| :------- | :----------------------------------------------------------- |
| `stable` | Waits `stableDelayHours`, then applies with deterministic jitter across `stableJitterHours` (spread rollout). 等待`stableDelayHours`，然后在`stableJitterHours`范围内应用确定性抖动（分批发布）。 |
| `beta`   | Checks every `betaCheckIntervalHours` (default: hourly) and applies immediately. 每`betaCheckIntervalHours`（默认：每小时）检查一次并立即应用。 |
| `dev`    | No automatic apply. Use `openclaw update` manually. 无自动应用。请手动使用 `openclaw update`。 |

The gateway also logs an update hint on startup (disable with `update.checkOnStart: false`).

​	gateway 在启动时还会记录更新提示（可通过 `update.checkOnStart: false` 禁用）。

## After updating

1) Run doctor

   ```sh
   openclaw doctor
   ```

2) Migrates config, audits DM policies, and checks gateway health. Details: [Doctor](https://docs.openclaw.ai/gateway/doctor)

   迁移配置、审核私信策略并检查网关健康状态。详情：[Doctor](https://docs.openclaw.ai/gateway/doctor)

3) Restart the gateway

   ```sh
   openclaw gateway restart
   ```

4) Verify

   ```sh
   openclaw health
   ```

   

## Rollback 回滚

### Pin a version (npm) 固定版本（npm）

```sh
npm i -g openclaw@<version>
openclaw doctor
openclaw gateway restart
```

Tip: `npm view openclaw version` shows the current published version.

​	提示：`npm view openclaw version` 会显示当前已发布的版本。

### Pin a commit (source) 固定提交（源代码）

```sh
git fetch origin
git checkout "$(git rev-list -n 1 --before=\"2026-01-01\" origin/main)"
pnpm install && pnpm build
openclaw gateway restart
```

To return to latest: `git checkout main && git pull`.

​	回到最新版本：`git checkout main && git pull`。

## If you are stuck 遇到问题时

- Run `openclaw doctor` again and read the output carefully.
  - 再次运行 `openclaw doctor` 并仔细阅读输出内容。
- Check: [Troubleshooting](https://docs.openclaw.ai/gateway/troubleshooting)
- Ask in Discord: https://discord.gg/clawd

## Related

- [Install Overview](https://docs.openclaw.ai/install) — all installation methods
- [Doctor](https://docs.openclaw.ai/gateway/doctor) — health checks after updates
- [Migrating](https://docs.openclaw.ai/install/migrating) — major version migration guides
