+++
title = "Install"
date = 2026-04-02T16:32:21+08:00
weight = 20
type = "docs"
description = ""
isCJKLanguage = true
draft = false

+++

# Install

## Recommended: installer script

The fastest way to install. It detects your OS, installs Node if needed, installs OpenClaw, and launches onboarding.

​	最快的安装方式。它会检测你的操作系统，在需要时安装 Node，安装 OpenClaw 并启动入门引导。

{{< tabpane text=true persist=disabled >}}

{{% tab "macOS | Linux" %}}

```sh
curl -fsSL https://openclaw.ai/install.sh | bash
```

{{% /tab %}}

{{% tab "Windows (PowerShell)" %}}

```sh
iwr -useb https://openclaw.ai/install.ps1 | iex
```

{{% /tab %}}

{{< /tabpane >}}



To install without running onboarding:

​	要在不运行onboarding的情况下安装：

{{< tabpane text=true persist=disabled >}}

{{% tab "macOS | Linux" %}}

```sh
curl -fsSL https://openclaw.ai/install.sh | bash -s -- --no-onboard
```

{{% /tab %}}

{{% tab "Windows (PowerShell)" %}}

```sh
& ([scriptblock]::Create((iwr -useb https://openclaw.ai/install.ps1))) -NoOnboard
```

{{% /tab %}}

{{< /tabpane >}}

For all flags and CI/automation options, see [Installer internals](https://docs.openclaw.ai/install/installer).

​	有关所有标志和CI/自动化选项，请参阅[Installer internals](https://docs.openclaw.ai/install/installer)。

## System requirements

- **Node 24** (recommended) or Node 22.14+ — the installer script handles this automatically
  - **Node 24**（推荐）或 Node 22.14 及以上版本 — 安装脚本会自动完成这一步
- **macOS, Linux, or Windows** — both native Windows and WSL2 are supported; WSL2 is more stable. See [Windows](https://docs.openclaw.ai/platforms/windows).
  - **macOS、Linux 或 Windows**——同时支持原生 Windows 和 WSL2；WSL2 更稳定。请参见[Windows](https://docs.openclaw.ai/platforms/windows)。
- `pnpm` is only needed if you build from source
  - `pnpm` 仅在从源码构建时需要

## Alternative install methods

### npm or pnpm

If you already manage Node yourself:

​	如果你已经自行管理 Node 环境：

{{< tabpane text=true persist=disabled >}}

{{% tab "npm"%}}

```sh
npm install -g openclaw@latest
openclaw onboard --install-daemon
```

{{% /tab %}}

{{% tab "npm"%}}

```sh
pnpm add -g openclaw@latest
pnpm approve-builds -g
openclaw onboard --install-daemon
```

> pnpm requires explicit approval for packages with build scripts. Run `pnpm approve-builds -g` after the first install.
>
> ​	pnpm 对带有构建脚本的包需要显式批准。首次安装后请运行 `pnpm approve-builds -g`。

{{% /tab %}}

{{< / tabpane>}}

> Troubleshooting: sharp build errors (npm)
>
> ​	故障排除：sharp 构建错误（npm）
>
> If `sharp` fails due to a globally installed libvips:
>
> ​	如果 `sharp` 因全局安装的 libvips 而失败：
>
> ```sh
> SHARP_IGNORE_GLOBAL_LIBVIPS=1 npm install -g openclaw@latest
> ```

### From source

For contributors or anyone who wants to run from a local checkout:

​	面向贡献者或希望从本地签出版本运行的人员：

```sh
git clone https://github.com/openclaw/openclaw.git
cd openclaw
pnpm install && pnpm ui:build && pnpm build
pnpm link --global
openclaw onboard --install-daemon
```

Or skip the link and use `pnpm openclaw ...` from inside the repo. See [Setup](https://docs.openclaw.ai/start/setup) for full development workflows.

​	或者跳过链接，在仓库中使用`pnpm openclaw ...`。查看[Setup](https://docs.openclaw.ai/start/setup)了解完整的开发工作流程。

### Install from GitHub main



```sh
npm install -g github:openclaw/openclaw#main
```

## Containers and package managers

###  Docker

Containerized or headless deployments.



### Podman

Rootless container alternative to Docker.

​	替代 Docker 的无 root 容器。

### Nix

Declarative install via Nix flake.

​	通过 Nix flake 进行声明式安装。

### Ansible

Automated fleet provisioning.

​	自动化集群配置。

### Bun

CLI-only usage via the Bun runtime.

​	仅通过 Bun 运行时进行 CLI 模式使用

## Verify the install

```sh
openclaw --version      # confirm the CLI is available
openclaw doctor         # check for config issues
openclaw gateway status # verify the Gateway is running
```

## Hosting and deployment 托管与部署

Deploy OpenClaw on a cloud server or VPS:

​	在云服务器或虚拟专用服务器上部署 OpenClaw：

### VPS

Any Linux VPS

### Docker VM

Shared Docker steps

### Kubernetes

K8s

### Fly.io

Fly.io

### Hetzner

Hetzner

### GCP

Google Cloud

### Azure

Azure

### Railway

Railway

### Render

Render

## Northflank

Northflank

## Update, migrate, or uninstall 更新、迁移或卸载



### Updating

Keep OpenClaw up to date.

​	保持 OpenClaw 为最新版本。

### Migrating

Move to a new machine.

​	迁移到新设备。

### Uninstall

Remove OpenClaw completely.

​	彻底卸载 OpenClaw。

## Troubleshooting: `openclaw` not found

If the install succeeded but `openclaw` is not found in your terminal:

​	如果安装成功但终端中未找到`openclaw`：

```sh
node -v           # Node installed?
npm prefix -g     # Where are global packages?
echo "$PATH"      # Is the global bin dir in PATH?
```

If `$(npm prefix -g)/bin` is not in your `$PATH`, add it to your shell startup file (`~/.zshrc` or `~/.bashrc`):

​	如果 `$(npm prefix -g)/bin` 不在你的 `$PATH` 中，请将其添加到 shell 启动文件（`~/.zshrc` 或 `~/.bashrc`）中：

```sh
export PATH="$(npm prefix -g)/bin:$PATH"
```

Then open a new terminal. See [Node setup](https://docs.openclaw.ai/install/node) for more details.

​	然后打开一个新的终端。有关更多详细信息，请参阅[Node setup](https://docs.openclaw.ai/install/node)。
