+++
title = "Node.js"
date = 2026-04-03T12:29:05+08:00
weight = 1
type = "docs"
description = ""
isCJKLanguage = true
draft = false

+++

OpenClaw requires **Node 22.14 or newer**. **Node 24 is the default and recommended runtime** for installs, CI, and release workflows. Node 22 remains supported via the active LTS line. The [installer script](https://docs.openclaw.ai/install#alternative-install-methods) will detect and install Node automatically — this page is for when you want to set up Node yourself and make sure everything is wired up correctly (versions, PATH, global installs).

​	OpenClaw 需要 **Node 22.14 或更高版本**。**Node 24 是安装、持续集成（CI）和发布工作流的默认且推荐运行时**。Node 22 仍通过长期支持（LTS）主线获得支持。[安装脚本](https://docs.openclaw.ai/install#alternative-install-methods)会自动检测并安装 Node —— 本页面适用于你想手动设置 Node 并确保所有配置（版本、环境变量 PATH、全局安装）均正确的情况。

## Check your version 检查版本

```sh
node -v
```

If this prints `v24.x.x` or higher, you’re on the recommended default. If it prints `v22.14.x` or higher, you’re on the supported Node 22 LTS path, but we still recommend upgrading to Node 24 when convenient. If Node isn’t installed or the version is too old, pick an install method below.

​	如果此命令输出 `v24.x.x` 或更高版本，说明你使用的是推荐的默认版本。如果输出 `v22.14.x` 或更高版本，说明你处于受支持的 Node 22 长期支持版路径，但我们仍建议你在方便时升级到 Node 24。如果未安装 Node 或版本过旧，请从下方选择一种安装方式。

## Install Node

{{< tabpane text=true persist=disabled >}}

{{% tab "macOS" %}}

**Homebrew** (recommended):

```sh
brew install node
```

{{% /tab %}}

{{% tab "Linux" %}}

**Ubuntu / Debian:**

```sh
curl -fsSL https://deb.nodesource.com/setup_24.x | sudo -E bash -
sudo apt-get install -y nodejs
```

**Fedora / RHEL:**

```sh
sudo dnf install nodejs
```

{{% /tab %}}

{{% tab "Windows" %}}

**winget** (recommended):

```sh
winget install OpenJS.NodeJS.LTS
```

**Chocolatey:**

```sh
choco install nodejs-lts
```

{{% /tab %}}

{{< /tabpane >}}

Or download the Windows installer from [nodejs.org](https://nodejs.org/).

​	或者从 [nodejs.org](https://nodejs.org/) 下载 Windows 安装程序。

> Using a version manager (nvm, fnm, mise, asdf) 使用版本管理器（nvm、fnm、mise、asdf）
>
> Version managers let you switch between Node versions easily. Popular options:
>
> ​	版本管理器可让你轻松切换 Node 版本。常用选项包括：
>
> - [**fnm**](https://github.com/Schniz/fnm) — fast, cross-platform 速度快，跨平台
> - [**nvm**](https://github.com/nvm-sh/nvm) — widely used on macOS/Linux 在 macOS/Linux 上广泛使用
> - [**mise**](https://mise.jdx.dev/) — polyglot (Node, Python, Ruby, etc.) 多语言（Node、Python、Ruby等）
>
> Example with fnm:
>
> ​	使用 fnm 的示例：
>
> ```sh
> fnm install 24
> fnm use 24
> ```
>
> > Make sure your version manager is initialized in your shell startup file (`~/.zshrc` or `~/.bashrc`). If it isn’t, `openclaw` may not be found in new terminal sessions because the PATH won’t include Node’s bin directory.
> >
> > ​	确保你的版本管理器已在 shell 启动文件（`~/.zshrc` 或 `~/.bashrc`）中初始化。如果未初始化，`openclaw` 在新的终端会话中可能无法被找到，因为 PATH 不会包含 Node 的 bin 目录。

## Troubleshooting 故障排除

### `openclaw: command not found`

This almost always means npm’s global bin directory isn’t on your PATH.

​	这几乎总是意味着 npm 的全局 bin 目录不在你的 PATH 环境变量中。

1) Find your global npm prefix

找到你的全局 npm 前缀

```
npm prefix -g
```

2) Check if it's on your PATH

检查它是否在你的 PATH 环境变量中

```
echo "$PATH"
```

Look for `<npm-prefix>/bin` (macOS/Linux) or `<npm-prefix>` (Windows) in the output.

​	在输出结果中查找`<npm-prefix>/bin`（适用于macOS/Linux）或`<npm-prefix>`（适用于Windows）。

3) Add it to your shell startup file 将其添加到你的 shell 启动文件中

{{< tabpane text=true persist=disabled >}}

{{% tab "macOS / Linux" %}}

Add to `~/.zshrc` or `~/.bashrc`:

​	添加到 `~/.zshrc` 或 `~/.bashrc` 文件中：

```txt
export PATH="$(npm prefix -g)/bin:$PATH"
```

Then open a new terminal (or run `rehash` in zsh / `hash -r` in bash).

​	然后打开一个新的终端（或在 zsh 中运行 `rehash` / 在 bash 中运行 `hash -r`）。

{{% /tab %}}

{{% tab "Windows" %}}

Add the output of `npm prefix -g` to your system PATH via Settings → System → Environment Variables.

​	通过设置 → 系统 → 环境变量，将 `npm prefix -g` 的输出添加到你的系统 PATH 中。

{{% /tab %}}

{{< /tabpane >}}

### Permission errors on `npm install -g` (Linux)

If you see `EACCES` errors, switch npm’s global prefix to a user-writable directory:

​	如果你看到 `EACCES` 错误，请将 npm 的全局前缀切换到用户可写入的目录：

```sh
mkdir -p "$HOME/.npm-global"
npm config set prefix "$HOME/.npm-global"
export PATH="$HOME/.npm-global/bin:$PATH"
```

Add the `export PATH=...` line to your `~/.bashrc` or `~/.zshrc` to make it permanent.

​	将 `export PATH=...` 这一行添加到你的 `~/.bashrc` 或 `~/.zshrc` 文件中，以使其永久生效。

## Related

- [Install Overview](https://docs.openclaw.ai/install) — all installation methods
- [Updating](https://docs.openclaw.ai/install/updating) — keeping OpenClaw up to date
- [Getting Started](https://docs.openclaw.ai/start/getting-started) — first steps after install
