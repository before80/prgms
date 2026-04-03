+++
title = "Installer Internals"
date = 2026-04-03T11:29:30+08:00
weight = 1
type = "docs"
description = ""
isCJKLanguage = true
draft = false

+++

# Installer Internals

OpenClaw ships three installer scripts, served from `openclaw.ai`.

​	OpenClaw 附带三个安装脚本，均从 `openclaw.ai` 提供。

| Script                                                       | Platform             | What it does                                                 |
| :----------------------------------------------------------- | :------------------- | :----------------------------------------------------------- |
| [`install.sh`](https://docs.openclaw.ai/install/installer#installsh) | macOS / Linux / WSL  | Installs Node if needed, installs OpenClaw via npm (default) or git, and can run onboarding. 如有需要则安装 Node，通过 npm（默认）或 git 安装 OpenClaw，并可运行onboarding流程。 |
| [`install-cli.sh`](https://docs.openclaw.ai/install/installer#install-clish) | macOS / Linux / WSL  | Installs Node + OpenClaw into a local prefix (`~/.openclaw`). No root required. 将 Node 与 OpenClaw 安装到本地前缀（`~/.openclaw`）。无需 root 权限。 |
| [`install.ps1`](https://docs.openclaw.ai/install/installer#installps1) | Windows (PowerShell) | Installs Node if needed, installs OpenClaw via npm (default) or git, and can run onboarding. 如有需要则安装 Node，通过 npm（默认）或 git 安装 OpenClaw，并可运行onboarding流程。 |

## Quick commands

{{< tabpane text=true persist=disabled >}}

{{% tab "install.sh" %}}

```sh
curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install.sh | bash
```

```sh
curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install.sh | bash -s -- --help
```

{{% /tab %}}

{{% tab "install-cli.sh" %}}

```sh
curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install-cli.sh | bash
```

```sh
curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install-cli.sh | bash -s -- --help
```

{{% /tab %}}

{{% tab "install.ps1" %}}

```sh
iwr -useb https://openclaw.ai/install.ps1 | iex
```

```sh
& ([scriptblock]::Create((iwr -useb https://openclaw.ai/install.ps1))) -Tag beta -NoOnboard -DryRun
```

{{% /tab %}}

{{< /tabpane >}}



> If install succeeds but `openclaw` is not found in a new terminal, see [Node.js troubleshooting](https://docs.openclaw.ai/install/node#troubleshooting).
>
> ​	如果安装成功但在新终端中未找到`openclaw`，请查看[Node.js 故障排除](https://docs.openclaw.ai/install/node#troubleshooting)。



------



## install.sh

> Recommended for most interactive installs on macOS/Linux/WSL.
>
> ​	适用于 macOS/Linux/WSL 上大多数交互式安装。

### Flow (install.sh)

1) Detect OS 检测操作系统

Supports macOS and Linux (including WSL). If macOS is detected, installs Homebrew if missing.

​	支持 macOS 和 Linux（包括 WSL）。若检测到 macOS 系统，会在 Homebrew 缺失时进行安装。

2) Ensure Node.js 24 by default 默认确保安装 Node.js 24

Checks Node version and installs Node 24 if needed (Homebrew on macOS, NodeSource setup scripts on Linux apt/dnf/yum). OpenClaw still supports Node 22 LTS, currently `22.14+`, for compatibility.

​	检查 Node 版本，必要时安装 Node 24（macOS 上使用 Homebrew，Linux 上使用 NodeSource 配置脚本，适配 apt/dnf/yum）。为保证兼容性，OpenClaw 仍支持 Node 22 长期支持版，当前要求为`22.14+`。

3) Ensure Git

Installs Git if missing.

​	若缺少 Git，则安装 Git。

4) Install OpenClaw

- `npm` method (default): global npm install `npm` 方法（默认）：全局 npm 安装
- `git` method: clone/update repo, install deps with pnpm, build, then install wrapper at `~/.local/bin/openclaw`  `git` 方法：克隆/更新代码仓库，使用 pnpm 安装依赖项，进行构建，然后在 `~/.local/bin/openclaw` 安装包装器

5) Post-install tasks 安装后任务

- Runs `openclaw doctor --non-interactive` on upgrades and git installs (best effort) 在升级和通过 git 安装时，运行 `openclaw doctor --non-interactive`（尽最大努力执行）
- Attempts onboarding when appropriate (TTY available, onboarding not disabled, and bootstrap/config checks pass) 在适当情况下尝试onboarding （TTY 可用、未禁用onboarding 且引导/配置检查通过）
- Defaults `SHARP_IGNORE_GLOBAL_LIBVIPS=1` 默认设置 `SHARP_IGNORE_GLOBAL_LIBVIPS=1`

### Source checkout detection 源检出检测

If run inside an OpenClaw checkout (`package.json` + `pnpm-workspace.yaml`), the script offers:

​	如果在 OpenClaw 检出目录（`package.json` + `pnpm-workspace.yaml`）中运行，该脚本会提供：

- use checkout (`git`), or  使用源码仓库（`git`），或者
- use global install (`npm`) 使用全局安装（`npm`）

If no TTY is available and no install method is set, it defaults to `npm` and warns. The script exits with code `2` for invalid method selection or invalid `--install-method` values.

​	如果没有可用的 TTY 且未设置安装方式，脚本将默认使用`npm`并发出警告。 当选择的方法无效或 `--install-method` 的值无效时，脚本将以 `2` 退出码退出。

###  Examples (install.sh)

{{< tabpane text=true persist=disabled >}}

{{% tab "Default" %}}

```sh
curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install.sh | bash
```

{{% /tab %}}

{{% tab "Skip onboarding" %}}

```sh
curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install.sh | bash -s -- --no-onboard
```

{{% /tab %}}

{{% tab "Git install" %}}

```sh
curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install.sh | bash -s -- --install-method git
```

{{% /tab %}}

{{% tab "GitHub main via npm" %}}

```sh
curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install.sh | bash -s -- --version main
```

{{% /tab %}}

{{% tab "Dry run" %}}

```sh
curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install.sh | bash -s -- --dry-run
```

{{% /tab %}}

{{< /tabpane >}}

### Flags reference

| Flag                                | Description                                                  |
| :---------------------------------- | :----------------------------------------------------------- |
| `--install-method npm|git`          | Choose install method (default: `npm`). Alias: `--method`  选择安装方式（默认：`npm`）。别名：`--method` |
| `--npm`                             | Shortcut for npm method  npm 方法的快捷方式                  |
| `--git`                             | Shortcut for git method. Alias: `--github ` Git 方法的快捷方式。别名：`--github` |
| `--version <version|dist-tag|spec>` | npm version, dist-tag, or package spec (default: `latest`) npm 版本、dist-tag 或包规范（默认：`latest`） |
| `--beta`                            | Use beta dist-tag if available, else fallback to `latest` 如果有 beta 版本标签则使用，否则回退到`latest` |
| `--git-dir <path>`                  | Checkout directory (default: `~/openclaw`). Alias: `--dir` 检出目录（默认：`~/openclaw`）。别名：`--dir` |
| `--no-git-update`                   | Skip `git pull` for existing checkout 跳过现有检出的 `git pull` |
| `--no-prompt`                       | Disable prompts 禁用提示                                     |
| `--no-onboard`                      | Skip onboarding 跳过onboarding                               |
| `--onboard`                         | Enable onboarding 启用onboarding                             |
| `--dry-run`                         | Print actions without applying changes  仅打印操作但不应用更改 |
| `--verbose`                         | Enable debug output (`set -x`, npm notice-level logs) 启用调试输出（`set -x`、npm 通知级别日志） |
| `--help`                            | Show usage (`-h`) 显示使用说明 (`-h`)                        |

### Environment variables reference 环境变量参考

| Variable                                            | Description                                                  |
| :-------------------------------------------------- | :----------------------------------------------------------- |
| `OPENCLAW_INSTALL_METHOD=git|npm`                   | Install method 安装方式                                      |
| `OPENCLAW_VERSION=latest|next|main|<semver>|<spec>` | npm version, dist-tag, or package spec npm 版本、dist-tag 或包规范 |
| `OPENCLAW_BETA=0|1`                                 | Use beta if available 有可用的测试版则使用测试版             |
| `OPENCLAW_GIT_DIR=<path>`                           | Checkout directory 检出目录                                  |
| `OPENCLAW_GIT_UPDATE=0|1`                           | Toggle git updates 切换 Git 更新                             |
| `OPENCLAW_NO_PROMPT=1`                              | Disable prompts 禁用提示                                     |
| `OPENCLAW_NO_ONBOARD=1`                             | Skip onboarding                                              |
| `OPENCLAW_DRY_RUN=1`                                | Dry run mode 试运行模式                                      |
| `OPENCLAW_VERBOSE=1`                                | Debug mode 调试模式                                          |
| `OPENCLAW_NPM_LOGLEVEL=error|warn|notice`           | npm log level npm 日志级别                                   |
| `SHARP_IGNORE_GLOBAL_LIBVIPS=0|1`                   | Control sharp/libvips behavior (default: `1`) 控制 sharp/libvips 行为（默认值：`1`） |



## install-cli.sh



> Designed for environments where you want everything under a local prefix (default `~/.openclaw`) and no system Node dependency.
>
> ​	专为以下环境设计：你希望所有内容都位于本地前缀下（默认 `~/.openclaw`），且无需系统级 Node 依赖。

### Flow (install-cli.sh)

1) Install local Node runtime 安装本地 Node 运行时

Downloads a pinned supported Node LTS tarball (the version is embedded in the script and updated independently) to `<prefix>/tools/node-v<version>` and verifies SHA-256.

​	将固定支持的 Node LTS 压缩包下载到`<prefix>/tools/node-v<version>`（版本内嵌于脚本中并独立更新），并验证 SHA-256 哈希值。

2) Ensure Git

If Git is missing, attempts install via apt/dnf/yum on Linux or Homebrew on macOS.

​	如果缺少 Git，会尝试在 Linux 系统上通过 apt/dnf/yum 安装，或在 macOS 系统上通过 Homebrew 安装。

3) Install OpenClaw under prefix

Installs with npm using `--prefix <prefix>`, then writes wrapper to `<prefix>/bin/openclaw`.

​	使用 npm 并通过 `--prefix <prefix>` 进行安装，然后将包装器写入 `<prefix>/bin/openclaw`。

### Examples (install-cli.sh)

{{< tabpane text=true persist=disabled >}}

{{% tab "Default" %}}

```sh
curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install-cli.sh | bash
```

{{% /tab %}}

{{% tab "Custom prefix + version" %}}

```sh
curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install-cli.sh | bash -s -- --prefix /opt/openclaw --version latest
```

{{% /tab %}}

{{% tab "Automation JSON output" %}}

```sh
curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install-cli.sh | bash -s -- --json --prefix /opt/openclaw
```

{{% /tab %}}

{{% tab "Run onboarding" %}}

```sh
curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install-cli.sh | bash -s -- --onboard
```

{{% /tab %}}

{{< /tabpane >}}

### Flags reference

| Flag                   | Description                                                  |
| :--------------------- | :----------------------------------------------------------- |
| `--prefix <path>`      | Install prefix (default: `~/.openclaw`) 安装前缀（默认值：`~/.openclaw`） |
| `--version <ver>`      | OpenClaw version or dist-tag (default: `latest`) OpenClaw 版本或 dist 标签（默认：`latest`） |
| `--node-version <ver>` | Node version (default: `22.22.0`) Node 版本（默认值：`22.22.0`） |
| `--json`               | Emit NDJSON events 输出 NDJSON 事件                          |
| `--onboard`            | Run `openclaw onboard` after install 安装后运行 `openclaw onboard` |
| `--no-onboard`         | Skip onboarding (default)                                    |
| `--set-npm-prefix`     | On Linux, force npm prefix to `~/.npm-global` if current prefix is not writable 在 Linux 系统上，如果当前的 npm 前缀目录不可写，则将其强制设置为 `~/.npm-global` |
| `--help`               | Show usage (`-h`) 显示使用说明 (`-h`)                        |

### Environment variables reference 环境变量参考

| Variable                                  | Description                                                  |
| :---------------------------------------- | :----------------------------------------------------------- |
| `OPENCLAW_PREFIX=<path>`                  | Install prefix  安装前缀                                     |
| `OPENCLAW_VERSION=<ver>`                  | OpenClaw version or dist-tag - OpenClaw 版本或 dist 标签     |
| `OPENCLAW_NODE_VERSION=<ver>`             | Node version Node 版本                                       |
| `OPENCLAW_NO_ONBOARD=1`                   | Skip onboarding                                              |
| `OPENCLAW_NPM_LOGLEVEL=error|warn|notice` | npm log level  - npm 日志级别                                |
| `OPENCLAW_GIT_DIR=<path>`                 | Legacy cleanup lookup path (used when removing old `Peekaboo` submodule checkout) 旧版清理查找路径（用于移除旧的 `Peekaboo` 子模块检出） |
| `SHARP_IGNORE_GLOBAL_LIBVIPS=0|1`         | Control sharp/libvips behavior (default: `1`) 控制 sharp/libvips 行为（默认值：`1`） |

## install.ps1

### Flow (install.ps1)

1) Ensure PowerShell + Windows environment 确保 PowerShell + Windows 环境

Requires PowerShell 5+.

​	要求 PowerShell 5.0 及更高版本。

2) Ensure Node.js 24 by default 默认确保安装 Node.js 24

If missing, attempts install via winget, then Chocolatey, then Scoop. Node 22 LTS, currently `22.14+`, remains supported for compatibility.

​	若缺失，将尝试通过 winget、然后 Chocolatey、再然后 Scoop 进行安装。Node 22 长期支持版（当前为 `22.14+`）为保持兼容性仍受支持。

3) Install OpenClaw

- `npm` method (default): global npm install using selected `-Tag` - `npm` 方法（默认）：使用选定的 `-Tag` 进行全局 npm 安装
- `git` method: clone/update repo, install/build with pnpm, and install wrapper at `%USERPROFILE%\.local\bin\openclaw.cmd`  - `git` 方法：克隆/更新代码仓库，使用 pnpm 安装/构建，并将包装器安装到 `%USERPROFILE%\.local\bin\openclaw.cmd`

4) Post-install tasks 安装后任务

Adds needed bin directory to user PATH when possible, then runs `openclaw doctor --non-interactive` on upgrades and git installs (best effort).

​	尽可能将所需的 bin 目录添加到用户 PATH，然后在升级和 Git 安装时运行 `openclaw doctor --non-interactive`（尽力而为）。

### Examples (install.ps1)

{{< tabpane text=true persist=disabled >}}

{{% tab "Default" %}}

```sh
iwr -useb https://openclaw.ai/install.ps1 | iex
```

{{% /tab %}}

{{% tab "Git install" %}}

```sh
& ([scriptblock]::Create((iwr -useb https://openclaw.ai/install.ps1))) -InstallMethod git
```

{{% /tab %}}

{{% tab "GitHub main via npm" %}}

```sh
& ([scriptblock]::Create((iwr -useb https://openclaw.ai/install.ps1))) -Tag main
```

{{% /tab %}}

{{% tab "Custom git directory" %}}

```sh
& ([scriptblock]::Create((iwr -useb https://openclaw.ai/install.ps1))) -InstallMethod git -GitDir "C:\openclaw"
```

{{% /tab %}}

{{% tab "Dry run" %}}

```sh
& ([scriptblock]::Create((iwr -useb https://openclaw.ai/install.ps1))) -DryRun
```

{{% /tab %}}

{{% tab "Debug trace" %}}

```sh
# install.ps1 has no dedicated -Verbose flag yet.
Set-PSDebug -Trace 1
& ([scriptblock]::Create((iwr -useb https://openclaw.ai/install.ps1))) -NoOnboard
Set-PSDebug -Trace 0
```

{{% /tab %}}

{{< /tabpane >}}

### Flags reference

| Flag                      | Description                                                  |
| :------------------------ | :----------------------------------------------------------- |
| `-InstallMethod npm|git`  | Install method (default: `npm`) 安装方式（默认：`npm`）      |
| `-Tag <tag|version|spec>` | npm dist-tag, version, or package spec (default: `latest`)  npm 分发标签、版本或包规范（默认值：`latest`） |
| `-GitDir <path>`          | Checkout directory (default: `%USERPROFILE%\openclaw`)  检出目录（默认：`%USERPROFILE%\openclaw`） |
| `-NoOnboard`              | Skip onboarding                                              |
| `-NoGitUpdate`            | Skip `git pull`                                              |
| `-DryRun`                 | Print actions only 仅打印操作                                |

### Environment variables reference 环境变量参考

| Variable                          | Description             |
| :-------------------------------- | :---------------------- |
| `OPENCLAW_INSTALL_METHOD=git|npm` | Install method 安装方式 |
| `OPENCLAW_GIT_DIR=<path>`         | Checkout directory      |
| `OPENCLAW_NO_ONBOARD=1`           | Skip onboarding         |
| `OPENCLAW_GIT_UPDATE=0`           | Disable git pull        |
| `OPENCLAW_DRY_RUN=1`              | Dry run mode 试运行模式 |

> If `-InstallMethod git` is used and Git is missing, the script exits and prints the Git for Windows link.
>
> ​	如果使用了`-InstallMethod git`且Git缺失，脚本将退出并打印Git for Windows的下载链接。

## CI and automation

Use non-interactive flags/env vars for predictable runs.

​	使用非交互式标志/环境变量以实现可预测的运行。

{{< tabpane text=true persist=disabled >}}

{{% tab "install.sh (non-interactive npm)" %}}

```sh
curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install.sh | bash -s -- --no-prompt --no-onboard
```

{{% /tab %}}

{{% tab "install.sh (non-interactive git)" %}}

```sh
OPENCLAW_INSTALL_METHOD=git OPENCLAW_NO_PROMPT=1 \
  curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install.sh | bash
```

{{% /tab %}}

{{% tab "install-cli.sh (JSON)" %}}

```sh
curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install-cli.sh | bash -s -- --json --prefix /opt/openclaw
```

{{% /tab %}}

{{% tab "install.ps1 (skip onboarding)" %}}

```sh
& ([scriptblock]::Create((iwr -useb https://openclaw.ai/install.ps1))) -NoOnboard
```

{{% /tab %}}

{{< /tabpane >}}

## Troubleshooting

### Why is Git required? 为什么需要 Git？

​	Git is required for `git` install method. For `npm` installs, Git is still checked/installed to avoid `spawn git ENOENT` failures when dependencies use git URLs.

​	`git` 安装方式需要用到 Git。对于 `npm` 安装，仍会检查并安装 Git，以避免依赖项使用 git 链接时出现 `spawn git ENOENT` 错误。

### Why does npm hit EACCES on Linux? 为什么 npm 在 Linux 上会出现 EACCES 错误？

​	Some Linux setups point npm global prefix to root-owned paths. `install.sh` can switch prefix to `~/.npm-global` and append PATH exports to shell rc files (when those files exist).

​	部分 Linux 系统将 npm 全局前缀指向了 root 拥有的路径。`install.sh` 可以将前缀切换为 `~/.npm-global`，并将 PATH 导出命令追加到 shell 配置文件中（前提是这些文件存在）。

### sharp/libvips issues 

The scripts default `SHARP_IGNORE_GLOBAL_LIBVIPS=1` to avoid sharp building against system libvips. To override:

​	脚本默认将 `SHARP_IGNORE_GLOBAL_LIBVIPS=1` 设置为 1，以避免 sharp 针对系统 libvips 进行构建。如需覆盖此设置：

```sh
SHARP_IGNORE_GLOBAL_LIBVIPS=0 curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install.sh | bash
```

### Windows: "npm error spawn git / ENOENT"

Install Git for Windows, reopen PowerShell, rerun installer.

​	安装 Git for Windows，重新打开 PowerShell，然后重新运行安装程序。

### Windows: "openclaw is not recognized"

Run `npm config get prefix` and add that directory to your user PATH (no `\bin` suffix needed on Windows), then reopen PowerShell.

​	运行 `npm config get prefix` 并将该目录添加到你的用户 PATH 中（在 Windows 上不需要 `\bin` 后缀），然后重新打开 PowerShell。

### Windows: how to get verbose installer output

`install.ps1` does not currently expose a `-Verbose` switch. Use PowerShell tracing for script-level diagnostics:

​	`install.ps1` 当前未公开 `-Verbose` 开关。请使用 PowerShell 跟踪获取脚本级诊断信息：

```sh
Set-PSDebug -Trace 1
& ([scriptblock]::Create((iwr -useb https://openclaw.ai/install.ps1))) -NoOnboard
Set-PSDebug -Trace 0
```

### openclaw not found after install

Usually a PATH issue. See [Node.js troubleshooting](https://docs.openclaw.ai/install/node#troubleshooting).

​	通常是 PATH 问题。请查看[Node.js 故障排除](https://docs.openclaw.ai/install/node#troubleshooting)。
