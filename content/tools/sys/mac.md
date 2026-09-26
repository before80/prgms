+++
title = "macOS"
date = 2026-09-24T16:45:56+08:00
weight = 1
type = "docs"
description = ""
isCJKLanguage = true
draft = false

+++

## 新 macOS 相关设置提升效率

​	可参见以下视频：

{{<youtube "q3-jUJZpC0o">}}



## macOS Gatekeeper（门卫）简介

​	Gatekeeper 是 macOS 内置安全机制，**用来限制未经过 Apple 公证的程序直接运行**，从 OS X 10.11 El Capitan 引入。

### 核心原理

​	当你从浏览器、聊天软件下载文件时，macOS 自动给文件打上扩展属性：`com.apple.quarantine`（隔离标记）。 带有这个标记的程序启动前，Gatekeeper 会做两件校验：

1. 检查应用是否有**开发者签名**；
2. 检查签名是否经过 **Apple 公证（Notarization）**。

​	校验通过 → 正常打开； 校验失败 → 弹出提示：**无法打开，因为 Apple 无法检查其是否包含恶意软件**，直接阻止运行。

> 本地拷贝、U 盘内部复制的文件，默认**不会**添加隔离标记，不会触发 Gatekeeper 校验。

### 系统安全选项（系统设置 → 隐私与安全性）

三个运行策略：

1. **App Store**：只允许 App Store 下载的应用
2. **App Store 和已识别的开发者**（默认）：允许 App Store + 有正规签名 + 公证的第三方开发者软件，这是日常默认选项
3. **任何来源**：新版 macOS 默认隐藏该选项，开启后 Gatekeeper 不拦截（不推荐长期开启）

### 绕过校验的几种方式

1. 单次放行：弹出阻止提示后，在「隐私与安全性」页面点**仍要打开**，本次放行，系统记住该 App
2. 命令删除隔离标记：就是刚才的 `xattr -rd com.apple.quarantine`，**移除 quarantine 标记后，Gatekeeper 不再校验这个 App**
3. 临时全局关闭 Gatekeeper（不推荐）

```bash
# 关闭
sudo spctl --master-disable
# 开启
sudo spctl --master-enable
```

### 关键区分

- Gatekeeper：**控制应用能不能启动**，做签名 + 公证检查
- XProtect：macOS 内置恶意软件检测，**就算绕过 Gatekeeper，XProtect 依然会扫描恶意代码**
- FileQuarantine：就是那个`com.apple.quarantine`标记，是 Gatekeeper 的触发开关，**不是病毒标记**

### 局限与风险

- Gatekeeper **不是杀毒软件**，它只能校验签名和公证，不能保证程序本身无后门；
- 公证只是证明安装包提交给 Apple 扫描过，**不代表 Apple 认证软件绝对安全**；
- 删除隔离标记，只是去掉触发 Gatekeeper 的开关，**不会关闭系统其他安全防护**。

MacOS快捷键

​	参见[CheatSheet/macShortcutKey](/CheatSheet/macShortcutKey/)

## 安装 `Homebrew`

```bash
# 国内需要科学上网才可以
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 安装后，重开终端，查看版本
# 或者
# brew --version
brew -v 

# 查看帮助文档
# 或者
# brew --help
brew -h

# brew 环境变量
# 打开 ~/.zshrc
nano ~/.zshrc

# 添加以下一行到文件末尾
eval "$(/opt/homebrew/bin/brew shellenv)"

# `Ctrl+O` → 回车保存 → `Ctrl+X` -> 退出
# 加载~/.zshrc 中的配置使其在当前终端中立即生效
source ~/.zshrc
```

​	`eval "$(/opt/homebrew/bin/brew shellenv)"` 执行后，主要会设置这些环境变量：

| 变量                  | 作用                                                      |
| :-------------------- | :-------------------------------------------------------- |
| `HOMEBREW_PREFIX`     | Homebrew 安装根目录，Apple Silicon 为 `/opt/homebrew`     |
| `HOMEBREW_CELLAR`     | Homebrew 软件包安装目录，通常是 `/opt/homebrew/Cellar`    |
| `HOMEBREW_REPOSITORY` | Homebrew 仓库目录                                         |
| `PATH`                | 把 `/opt/homebrew/bin` 和 `/opt/homebrew/sbin` 加到最前面 |
| `MANPATH`             | 让 `man` 能查到 Homebrew 安装的命令的手册                 |
| `INFOPATH`            | 让 `info` 能查到 Homebrew 的 info 文档                    |

​	其中最重要的是 `PATH`。它让终端优先使用 `Homebrew` 安装的命令，例如：

```bash
/opt/homebrew/bin/git
/opt/homebrew/bin/go
/opt/homebrew/bin/python3
```

而不是系统自带的旧版本。

​	更多关于`brew`的内容，参见[brew](/Tools/brew)

## 为自带终端`zsh`安装命令实时提示

1. **zsh-autosuggestions：灰色历史命令实时提示（输入时后面灰色预填，最常用）**
2. **zsh-syntax-highlighting：语法高亮，命令对错变色**

```bash
# 安装两个插件
brew install zsh-autosuggestions zsh-syntax-highlighting

# 打开 ~/.zshrc
nano ~/.zshrc

# 在文件末尾粘贴以下内容
source $(brew --prefix)/share/zsh-autosuggestions/zsh-autosuggestions.zsh
source $(brew --prefix)/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh

# `Ctrl+O` → 回车保存 → `Ctrl+X`  -> 退出
# 加载~/.zshrc 中的配置使其在当前终端中立即生效
source ~/.zshrc
```

## 为自带终端`zsh`添加时间显示

**常用时间标记**

- `%T` → 24 小时 时：分（`15:30`）
- `%*` → 24 小时 时：分: 秒（`15:30:22`，推荐，开发记录执行耗时很方便）
- `%D` → 日期 `2026-09-16`
- `%t` → 12 小时制 AM/PM

```bash
# 打开 ~/.zshrc
nano ~/.zshrc

# 在文件最末尾粘贴一行，
PROMPT='[%*] %n@%m %1~ %# '
# `Ctrl+O` → 回车保存 → `Ctrl+X`  -> 退出

# 加载配置，立刻生效
source ~/.zshrc

# 效果预览：
# [15:30:22] lx@lxdeMacBook-Pro prgms %
```



## 安装 `openInTerminal`

​	**在 Finder（访达）和终端（或代码编辑器）之间建立快捷通道**，让你无需手动输入冗长的 `cd` 路径命令，就能直接在终端或编辑器中打开当前所在的文件夹。

​	`openInTerminal`支持的终端有哪些？

OpenInTerminal 支持的终端列表在不断更新中，以下是它兼容的主流终端：

- **系统内置**：Apple 的 **Terminal.app**
- **主流第三方终端**：**iTerm2**, **Hyper**, **Alacritty**, **kitty**, **Warp**, **WezTerm**, **Tabby**
- **其他**：**Ghostty**, **cmux** 等

> **注意**
>
> ​	前提是需要自己提前安装这些终端（除了系统内置的 Teminal ）。
>
> ​	点击打开 `OpenInTerminal.app` 可选择使用哪个终端！

```bash
brew install --cask openinterminal

# 在设置中启用 Finder 扩展
# 依次进入 系统设置 -> 通用 -> 登录项与扩展 -> OpenInTerminal Extensions，然后启用 File Provider。
# 在访达工具栏点击“显示” -> “自定义工具栏”将 “Open in Termimal”图标拖拽到访达窗口中工具栏位置上。
# 这样在访达中，右键会出现“终端”， 窗口中的工具栏也可以打开“终端”！
```

## 覆盖默认`git`

​	在 macOS 上，**不建议直接卸载系统自带的 Git**。因为它与 Xcode 命令行工具（Command Line Tools）深度绑定，位于受系统完整性保护（SIP）的 `/usr/bin/git` 目录，强行删除可能会破坏系统其他功能。

​	正确的做法是：**通过 Homebrew 安装最新版 Git，并调整 Shell 的 `PATH` 环境变量，让你的终端优先使用 Homebrew 安装的版本**。

```bash
brew install git

# 若之前在安装 brew 之后有在 ~/.zshrc 中添加 eval "$(/opt/homebrew/bin/brew shellenv)"
# 则，当前的git命令就是使用 通过brew安装的git

# 查看 git 版本
git --version
# [11:03:07] lx@lxdeMacBook-Pro ~ % git --version 
# git version 2.55.0

# 查看 git 程序的位置
where git
# [10:56:42] lx@lxdeMacBook-Pro ~ % where git
# /opt/homebrew/bin/git
# /usr/bin/git
# /opt/homebrew/bin/git

# 查看系统自带git的版本
/usr/bin/git --version
# [11:02:23] lx@lxdeMacBook-Pro ~ % /usr/bin/git --version
# git version 2.54.0 (Apple Git-157)

```

## 安装 `tree`命令

```bash
brew install tree

# 查看版本
tree --version

# 卸载
brew uninstall tree
```



## 安装 `go`

​	Go 语言的完整开发工具链， 包括：

- `go` 命令：编译、运行、测试、下载依赖、管理模块等。
- `gofmt`：Go 官方代码格式化工具。
- Go 标准库。
- Go 编译器。
- 其他内置工具，比如 `go vet`、`go doc` 等。

```bash
brew install go

# 安装后，查看版本
go --version

# 查看配置
go env

# 配置，例如：
# 1. 设置国内代理（最常用的配置，解决模块下载慢的问题）
go env -w GOPROXY=“https://goproxy.cn,direct”

# 2. 撤销 GOPROXY 的设置，恢复为官方默认值
go env -u GOPROXY
```

## 安装 `Rust`

```bash
# 安装 rustup，即 Rust 官方的工具链管理器
# 不推荐使用 brew install rust 来安装 rustc+cargo+rustup
curl --proto '=https' --tlsv1.2 https://sh.rustup.rs -sSf | sh

# 安装后，重开终端，才能使用相关命令： rustup、 cargo、rustc

# 卸载
rustup self uninstall

```

> ```bash
> [9:16:01] lx@lxdeMacBook-Pro ~ % curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
> info: downloading installer
> 
> Welcome to Rust!
> 
> This will download and install the official compiler for the Rust
> programming language, and its package manager, Cargo.
> 
> Rustup metadata and toolchains will be installed into the Rustup
> home directory, located at:
> 
>   /Users/lx/.rustup
> 
> This can be modified with the RUSTUP_HOME environment variable.
> 
> The Cargo home directory is located at:
> 
>   /Users/lx/.cargo
> 
> This can be modified with the CARGO_HOME environment variable.
> 
> The cargo, rustc, rustup and other commands will be added to
> Cargo's bin directory, located at:
> 
>   /Users/lx/.cargo/bin
> 
> This path will then be added to your PATH environment variable by
> modifying the profile files located at:
> 
>   /Users/lx/.profile
>   /Users/lx/.zshenv
>   /Users/lx/.tcshrc
> 
> You can uninstall at any time with rustup self uninstall and
> these changes will be reverted.
> 
> Current installation options:
> 
> 
>     default host tuple: aarch64-apple-darwin
>      default toolchain: stable (default)
>                profile: default
>   modify PATH variable: yes
> 
> 1) Proceed with standard installation (default - just press enter)
> 2) Customize installation
> 3) Cancel installation
> >1
> 
> info: profile set to default
> info: default host tuple is aarch64-apple-darwin
> info: syncing channel updates for stable-aarch64-apple-darwin
> info: latest update on 2026-09-03 for version 1.98.1 (48a229cea 2026-09-01)
> info: downloading 6 components
>         cargo installed                        8.49 MiB                                                                        clippy installed                        2.78 MiB                                                                     rust-docs installed                       23.01 MiB                                                                      rust-std installed                       28.38 MiB                                                                         rustc installed                       46.68 MiB                                                                       rustfmt installed                        1.43 MiB                                                                 info: default toolchain set to stable-aarch64-apple-darwin
> 
>   stable-aarch64-apple-darwin installed - rustc 1.98.1 (48a229cea 2026-09-01)
> 
> 
> Rust is installed now. Great!
> 
> To get started you may need to restart your current shell.
> This would reload your PATH environment variable to include
> Cargo's bin directory ($HOME/.cargo/bin).
> 
> To configure your current shell, you need to source the
> corresponding env file under $HOME/.cargo.
> 
> Consider running the right command for your shell (note the leading DOT):
> . "$HOME/.cargo/env"           # For sh/ash/dash/pdksh/zsh
> source "$HOME/.cargo/env.tcsh" # For tcsh
> ```
>
> **重开终端**后
>
> ```bash
> Last login: Sat Sep 26 09:16:01 on ttys003
> [9:26:54] lx@lxdeMacBook-Pro ~ % rustup --version
> rustup 1.29.1 (d95a37b6a 2026-08-13)
> info: This is the version for the rustup toolchain manager, not the rustc compiler.
> info: the currently active `rustc` version is `rustc 1.98.1 (48a229cea 2026-09-01)`
> [9:27:03] lx@lxdeMacBook-Pro ~ % cargo --version     
> cargo 1.98.1 (797e8a9bc 2026-08-05)
> [9:29:30] lx@lxdeMacBook-Pro ~ % rustc --version 
> rustc 1.98.1 (48a229cea 2026-09-01)
> [9:29:36] lx@lxdeMacBook-Pro ~ % 
> ```
>
> **不重开终端**也可以这样：
>
> ```bash
> source ~/.zshenv
> ```
>
> ​	原因在于，执行`curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh`后，会在 `~/.zshenv` 文件的末尾添加一行：
>
> ```bash
> . "$HOME/.cargo/env"
> ```
>
> 



> `rustup self uninstall`执行后会提示确认，输入 `y` 回车即可。 这条命令会自动删除：
>
> - rustup 程序
> - Rust、cargo、所有已安装的工具链 (stable/beta/nightly)
> - `~/.cargo`、`~/.rustup` 目录
>
> ```bash
> [9:11:47] lx@lxdeMacBook-Pro ~ % rustup self uninstall
> 
> 
> Thanks for hacking in Rust!
> 
> This will uninstall all Rust toolchains and data, and remove
> $HOME/.cargo/bin from your PATH environment variable.
> 
> Continue? (y/N) y
> 
> info: removing toolchains
> info: uninstalling toolchain stable-aarch64-apple-darwin
> info: toolchain stable-aarch64-apple-darwin uninstalled
> info: uninstalling toolchain nightly-aarch64-apple-darwin
> info: toolchain nightly-aarch64-apple-darwin uninstalled
> info: removing rustup home
> info: removing cargo home
> info: removing rustup binaries
> info: rustup is uninstalled
> [9:12:42] lx@lxdeMacBook-Pro ~ % 
> [9:13:25] lx@lxdeMacBook-Pro ~ % rustup --version     
> zsh: command not found: rustup
> [9:15:02] lx@lxdeMacBook-Pro ~ % rustc --version 
> zsh: command not found: rustc
> [9:15:33] lx@lxdeMacBook-Pro ~ % cargo --version     
> zsh: command not found: cargo
> ```
>
> 

## 安装 `python`

### 安装方式

#### 方式1： 直接安装

```bash
# `python` 永远指向最新稳定 Python3；
brew install python

# 卸载
# brew uninstall python

# 安装指定版本
brew install python@3.14

# 卸载
# brew uninstall python@3.14

# 查看版本
python3 --version
pip3 --version 
```

> Mac 默认没有 `python` 命令，只有 `python3`；可以加别名方便使用，写入 `~/.zshrc`：
>
> ```bash
> alias python="python3"
> alias pip="pip3"
> ```
>
> 保存，重启终端，之后直接敲 `python` 就可以。

#### 方式2： 通过`pyenv`

​	pyenv 是一个 **Python 版本管理工具**。它让你可以：

- 在同一台机器上安装多个 Python 版本（如 3.9、3.10、3.11、3.12、3.13、3.14）。
- 为不同项目指定不同的 Python 版本。
- 通过 `.python-version` 文件自动切换版本。
- 避免污染系统自带的 Python。

```bash
brew install pyenv

# 卸载 pyenv
# brew uninstall pyenv
# 若后续有安装pyenv-virtualenv，则需要先执行 brew install pyenv-virtualenv， 才可以卸载成功！

# 打开 ~/.zshrc
nano ~/.zshrc

# 在文件末尾添加以下两行
eval "$(pyenv init --path)"
eval "$(pyenv init -)"

# `Ctrl+O` → 回车保存 → `Ctrl+X` -> 退出
# 加载~/.zshrc 中的配置使其在当前终端中立即生效
source ~/.zshrc

# 查看版本
pyenv --version
# [12:55:46] lx@lxdeMacBook-Pro ~ % pyenv --version
# pyenv 2.8.5
```



> 解释下：
>
> ```bash
> pyenv init --path
> pyenv init -
> ```
>
> 一、`pyenv init --path` 的输出
>
> ```bash
> PATH="$(bash --norc -ec 'IFS=:; paths=($PATH); 
> for i in ${!paths[@]}; do 
> if [[ ${paths[i]} == "''/Users/lx/.pyenv/shims''" ]]; then unset '\''paths[i]'\''; 
> fi; done; 
> echo "${paths[*]}"')"
> export PATH="/Users/lx/.pyenv/shims:${PATH}"
> command pyenv rehash
> ```
>
> 
>
> 1. **第一段：清理 PATH 中重复的 shims 路径**
>
> ```bash
> PATH="$(bash --norc -ec 'IFS=:; paths=($PATH); 
> for i in ${!paths[@]}; do 
> if [[ ${paths[i]} == "''/Users/lx/.pyenv/shims''" ]]; then unset '\''paths[i]'\''; 
> fi; done; 
> echo "${paths[*]}"')"
> ```
>
> - 它启动一个**干净的 bash**（`--norc` 不读取任何 bash 配置），用 `-e` 让错误退出，`-c` 执行后面的脚本。
> - 把当前的 `PATH` 按冒号 `:` 分割成数组 `paths`。
> - 遍历数组，如果某个元素等于 `/Users/lx/.pyenv/shims`，就把它从数组中删除。
> - 最后用 `echo "${paths[*]}"` 重新用空格拼接？注意这里 `IFS=:` 被设置，所以 `${paths[*]}` 会用冒号连接，输出新的 PATH 字符串。
> - 外层用 `PATH="$(...)"` 把清理后的 PATH 赋值回去。
>
> **目的**：防止多次执行 `pyenv init` 导致 `/Users/lx/.pyenv/shims` 在 PATH 中重复出现。
>
> 2. **第二段：把 shims 目录加到 PATH 最前面**
>
> ```bash
> export PATH="/Users/lx/.pyenv/shims:${PATH}"
> ```
>
> - 将 pyenv 的 shims 目录放到 `PATH` 的最前面。
> - 这样 `python`、`pip` 等命令会优先调用 `~/.pyenv/shims` 下的代理脚本，由 pyenv 决定实际使用哪个 Python 版本。
>
> 3. 第三段：重新生成 shims
>
> ```bash
> command pyenv rehash
> ```
>
> - `command` 表示直接调用外部 `pyenv` 命令，而不是 shell 函数。
> - `pyenv rehash` 会扫描已安装的 Python 版本，在 `~/.pyenv/shims` 下重新生成所有可执行文件的代理脚本。
> - 确保新安装的 Python 或工具能立即通过 shims 调用。
>
> ------
>
> 二、`pyenv init -` 的输出
>
> ```bash
> PATH="$(bash --norc -ec 'IFS=:; paths=($PATH); 
> for i in ${!paths[@]}; do 
> if [[ ${paths[i]} == "''/Users/lx/.pyenv/shims''" ]]; then unset '\''paths[i]'\''; 
> fi; done; 
> echo "${paths[*]}"')"
> export PATH="/Users/lx/.pyenv/shims:${PATH}"
> export PYENV_SHELL=zsh
> source '/opt/homebrew/Cellar/pyenv/2.8.5/completions/pyenv.zsh'
> command pyenv rehash
> pyenv() {
>   local command=${1:-}
>   [ "$#" -gt 0 ] && shift
>   case "$command" in
>   rehash|shell)
>     eval "$(pyenv "sh-$command" "$@")"
>     ;;
>   *)
>     command pyenv "$command" "$@"
>     ;;
>   esac
> }
> ```
>
> 它比 `--path` 多了以下内容：
>
> 1. **设置 `PYENV_SHELL`**
>
> ```bash
> export PYENV_SHELL=zsh
> ```
>
> - 告诉 pyenv 当前使用的 shell 是 zsh，便于 pyenv 内部根据 shell 类型调整行为。
>
> 2. **加载 zsh 补全脚本**
>
> ```bash
> source '/opt/homebrew/Cellar/pyenv/2.8.5/completions/pyenv.zsh'
> ```
>
> - 加载 pyenv 提供的 zsh 补全功能。
> - 这样你在输入 `pyenv` 命令时，按 Tab 键可以自动补全子命令、版本号等。
> - 路径来自 Homebrew 安装的 pyenv 版本（2.8.5）。
>
> 3. **定义 `pyenv` shell 函数**
>
> ```bash
> pyenv() {
>   local command=${1:-}
>   [ "$#" -gt 0 ] && shift
>   case "$command" in
>   rehash|shell)
>     eval "$(pyenv "sh-$command" "$@")"
>     ;;
>   *)
>     command pyenv "$command" "$@"
>     ;;
>   esac
> }
> ```
>
> - 这个函数**覆盖**了直接调用外部 `pyenv` 命令的行为。
> - 当执行 `pyenv rehash` 或 `pyenv shell` 时：
>   - 会调用 `pyenv sh-rehash` 或 `pyenv sh-shell`。
>   - 这两个内部命令会输出一段 shell 代码，然后通过 `eval` 在当前 shell 中执行。
>   - 因为 `pyenv shell` 需要修改当前 shell 的环境变量（如 `PYENV_VERSION`），直接运行外部命令无法影响父 shell，所以必须用 `eval` 执行它输出的代码。
> - 对于其他子命令（如 `pyenv install`、`pyenv versions`），则直接转发给真正的 `pyenv` 命令（用 `command pyenv` 避免递归调用函数）。
>
> 4. **仍然包含 `--path` 中的 PATH 清理、添加和 rehash**
>
> 所以 `pyenv init -` 的输出实际上**包含了 `--path` 的所有功能**，并额外增加了 shell 集成。

##### pyenv的使用

```bash
# 查看可安装的版本
# 或者 pyenv install --list
pyenv install -l

# 安装指定版本
pyenv install 3.14.7
# 安装自由线程版（无 GIL，实验性）：
# pyenv install 3.14.7t

# 卸载
pyenv uninstall 3.14.7

# 查看已安装的版本
pyenv versions

# 切换 Python 版本
# 1. 仅当前终端会话, 关闭终端即失效
pyenv shell 3.14.7 

# 2. 当前目录及其子目录,写入 .python-version 文件，持久有效
pyenv local 3.14.7

# 3. 全局默认，写入 ~/.pyenv/version，持久有效
pyenv global 3.14.7

# 4. 使用操作系统自带的 Python
# system 是 pyenv 的一个特殊关键字，不是具体的版本号。
# 将 system 作为内容写入 ~/.pyenv/version，持久有效
# 若要 system 有效，则不能在 ~/.zshrc 中写入： eval "$(pyenv init --path)" 和 eval "$(pyenv init -)"
pyenv global system

# 取消设置
pyenv global system
pyenv local --unset
pyenv shell --unset


# 查看当前活跃版本及来源
pyenv version

# 查看全局版本
pyenv global

# 查看当前目录的本地版本
pyenv local

# 当前 python 的真实路径
pyenv which python

# 当前 pip 的真实路径
pyenv which pip

# pyenv 根目录
pyenv root

# 安装新版本或通过 pip install 安装了带命令行入口的工具后，需要重建 shims：
# 通常 pyenv install 会自动执行，但 pip install 不会，所以手动运行。
pyenv rehash

# 更新 pyenv
brew upgrade pyenv
# 或使用 pyenv 自带命令（部分安装方式支持）
pyenv update
```

#### 方式3:（推荐）通过`uv`

​	`uv` 是一个用 Rust 编写的、速度极快的现代 Python 包与项目管理工具，旨在用一个统一的工具替代 `pip`、`venv`、`pyenv`、`pip-tools`、`pipx` 等多个传统工具

​	更多内容，请参见[uv官方文档](https://docs.astral.sh/uv/)。

```bash
brew install uv

# 也可以通过如下方式安装：
# 独立安装脚本：curl -LsSf https://astral.sh/uv/install.sh | sh
# 通过 pip：pip install uv
# 通过 pipx：pipx install uv
```

##### uv的使用

```bash
# 管理 Python 版本
# 查看已安装的 Python 版本
uv python list --only-installed
# 查看可安装的 Python 版本
uv python list --only-downloads

# 安装指定版本（可安装多个：3.13 3.14）
# 默认安装 CPython 编译器的 Python 版本
uv python install 3.14.7
# 等价于 uv python install cpython@3.14.7
# uv python install pypy@3.12.14 则是安装 PyPy 编译器的 Python 版本
# CPython、PyPy、GraalPy 都是 Python 语言的具体实现，
# 可以理解为“不同厂家用不同技术做的 Python 解释器/运行时”。它们不是单纯的编译器，
# 而是包含编译器、解释器、运行时环境、标准库等完整组件的软件。

# 一次安装多个版本
# uv python install 3.14.7 3.13.15
# 不指定版本，则安装最新稳定版
# uv python install

# 卸载指定版本
uv python uninstall 3.14.7
# 即 uv python uninstall cpython@3.14.7

# uv python uninstall pypy@3.12.14

# 指定默认 Python 版本
# 即使该版本已经安装，这条命令也会重新将其设置为默认版本，
# 并创建或更新指向该版本的 python 和 python3 可执行文件
uv python --default 3.14.7

# 配置 shell，即将： export PATH="$HOME/.local/bin:$PATH" 加入到 ./zshenv 文件中
uv python update-shell

# 在当前终端，立即生效
source ~/.zshenv

# 为当前项目固定 Python 版本，生成：.python-version 文件
uv python pin 3.14.7

# 当执行 uv venv 或 uv run 等命令时，如果所需 Python 版本不存在，uv 会自动下载


# 查看 Python 实际路径
uv python find 3.14.7

# 创建新项目
uv init myproject
# 或，在 /path/to/parent/ 下创建 myproject 目录，与先 cd 再 uv init myproject 效果类似
uv init --directory /path/to/parent  myproject
cd myproject


# 安装单个包
uv pip install flask
```

###### uvx的使用

> 使用 `uvx`（即 `uv tool run` 的别名）在临时环境中运行工具：



### 创建虚拟环境

#### 使用python自带的`venv`

> 适合场景：简单项目、单环境

```bash
# 创建虚拟环境， 其中.venv 是目录名
python -m venv .venv
# 激活虚拟环境
source .venv/bin/activate
# 若是Windows系统，则使用 .venv\Scripts\activate 来激活虚拟环境
# 激活后，终端提示符通常会显示 (.venv)

# 验证是否已经处于虚拟环境中
which python
which pip
python --version
# 只显示该环境安装的包
pip list 

# 应该指向 .venv/bin/python 和 .venv/bin/pip。

# 退出虚拟环境
deactivate

# 虚拟环境本质上就是一个目录，删除目录即可：
deactivate
rm -rf .venv

# 建议把 .venv/ 加入 .gitignore，不要提交到 Git：
# 即在 .gitignore 文件中添加以下内容
.venv/
__pyche__/
*.pyc
```

#### 使用`pyenv-virtualenv`

> 适合场景：多环境、频繁切换、集中管理

```bash
# 安装 pyenv-virtualenv
brew install pyenv-virtualenv

# 在 ~/.zshrc 中加入：
eval "$(pyenv virtualenv-init -)"

# `Ctrl+O` → 回车保存 → `Ctrl+X` -> 退出
# 加载~/.zshrc 中的配置使其在当前终端中立即生效
source ~/.zshrc

# 基于 pyenv 已安装的 Python 3.14.7，创建一个名为 myapp-env 的虚拟环境，并由 pyenv 统一管理。
# 其中 myapp-env 也是目录名
# 在 ~/.pyenv/versions/ 下创建： ~/.pyenv/versions/myapp-env/
pyenv virtualenv 3.14.7 myapp-env
# 也可以省略版本，基于当前活跃版本创建：
# pyenv virtualenv myapp-env

# 手动激活指定的虚拟环境
# 激活后，你的终端提示符前会出现 (myapp-env) 标识
pyenv activate myapp-env

# 或者，绑定到项目，自动激活
cd ~/projects/myapp
pyenv local myapp-env

# 退出虚拟环境
pyenv deactivate

# 列出所有虚拟环境
pyenv virtualenvs


# 删除指定的虚拟环境
# 删除后，~/.pyenv/versions/myapp-env 目录会被移除
pyenv virtualenv-delete myapp-env

```

#### 使用`uv`

```bash
# 在当前目录创建 .venv 虚拟环境
uv venv

# 创建名为 my-env 的虚拟环境
uv venv my-env

# 创建使用特定 Python 版本（如 3.14）的虚拟环境
uv venv --python 3.14


# 手动激活 .venv 虚拟环境
source .venv/bin/activate
# 激活后，你的终端提示符前会出现 (.venv) 标识，此时即可使用 uv pip 安装包

# 若使用 my-env 虚拟环境，则需要使用
source my-env/bin/activate
# 激活后，你的终端提示符前会出现 (my-venv) 标识，此时即可使用 uv pip 安装包

```



## 安装 `Nginx`

```bash
brew install nginx
# 查看版本确认
nginx -v

# 后台常驻（开机自启）推荐
brew services start nginx
brew services stop nginx
brew services restart nginx

# nginx原生命令
nginx -t                  # ✅校验配置语法，修改配置一定要先跑这个！
nginx -s reload           # 平滑重载配置，不中断服务
nginx -s stop             # 立刻停止
nginx -s quit             # 优雅停止

# 在 /opt/homebrew/etc/nginx/servers/目录下为新站点新建配置文件，例如：prgm.conf，
touch /opt/homebrew/etc/nginx/servers/prgm.conf

# 该文件的内容如下：
server {
    listen 80;
    server_name prgm.cn;

    # 网站根目录，替换成你的网站文件夹
    root /Users/lx/Hugos/prgms/public;
    index index.html index.htm;

    # 前端SPA路由（Vue/React单页应用必须加，刷新404修复）
    location / {
        try_files $uri $uri/ /index.html;
    }

    # 日志（可选）
    access_log /opt/homebrew/var/log/nginx/prgm.cnaccess.log;
    error_log /opt/homebrew/var/log/nginx/prgm.cn.error.log;
}

# 检查配置语法
nginx -t
# 重载配置
nginx -s reload

# 本地域名解析
# 修改 /etc/hosts文件
# 例如，新增 127.0.0.1 prgm.cn
nano /etc/hosts

# nano 相关操作
# `Ctrl + O`：保存
# `Ctrl + X`：退出
# `Ctrl + W`：搜索文字
# `Ctrl + K`：剪切当前一行
# `Ctrl + U`：粘贴

# 查看 /etc/hosts中的内容
cat /etc/hosts  
##
# Host Database
#
# localhost is used to configure the loopback interface
# when the system is booting.  Do not change this entry.
##
127.0.0.1	localhost
255.255.255.255	broadcasthost
::1             localhost
127.0.0.1	prgm.cn
```

## 安装 `hugo`

```bash
# 默认安装最新的 extended 版本，该版本支持 Sass，是做 Hugo 站点的首选
brew install hugo
# 重复执行，遇到有新版本，相当于更新版本

# 查看安装版本
hugo version
# 例如： hugo v0.165.0+extended+withdeploy darwin/arm64 BuildDate=2026-08-12T14:26:28Z VendorInfo=Homebrew

# 更新 hugo 版本
brew upgrade hugo

# 锁定 hugo 版本
brew pin hugo

# 取消锁定
brew unpin hugo

```

## 安装 `stats`

​	项目：[https://github.com/exelban/stats](https://link.wtturl.cn/?target=https%3A%2F%2Fgithub.com%2Fexelban%2Fstats&scene=im&aid=582478&lang=zh)，MIT 开源，社区维护多年，菜单栏实时显示 CPU、内存、GPU、温度、网速，**完全无广告、无订阅**，非常适合开发者。

```bash
# 安装
brew install --cask stats

# 卸载
brew uninstall --cask stats

# 配置
open /Applications/Stats.app
```

## 安装 `visual-studio-code`

```bash
brew install --cask visual-studio-code

# 安装后查看版本
code --version

# 或从命令行直接打开
open -a "Visual Studio Code"
# 或，指定打开某个文件
code ~/.zshrc
```

## 安装 `Xcode`

​	进入 `App Store`, 搜索 `Xcode`,进行安装!

## 安装 `Android Studio`

```bash
# 到 https://developer.android.com/studio?hl=zh-cn 下载最新版 Android Studio
# 点击 Android Studio.dmg 打开后拖入 Applications
# 执行以下命令，递归删除 Android Studio 整个 App 包里所有文件的网络隔离标记
xattr -rd com.apple.quarantine /Applications/Android\ Studio.app 

# 之后打开，同意协议，安装一些组件
Preparing "Install Sources for Android 37.0 (revision 2)".
Downloading https://dl.google.com/android/repository/source-37.0_r02.zip
"Install Sources for Android 37.0 (revision 2)" ready.
Installing Sources for Android 37.0 in /Users/lx/Library/Android/sdk/sources/android-37.0
"Install Sources for Android 37.0 (revision 2)" complete.
"Install Sources for Android 37.0 (revision 2)" finished.
Preparing "Install Android SDK Build-Tools 36 v.36.0.0".
Downloading https://dl.google.com/android/repository/build-tools_r36_macosx.zip
"Install Android SDK Build-Tools 36 v.36.0.0" ready.
Installing Android SDK Build-Tools 36 in /Users/lx/Library/Android/sdk/build-tools/36.0.0
"Install Android SDK Build-Tools 36 v.36.0.0" complete.
"Install Android SDK Build-Tools 36 v.36.0.0" finished.
Preparing "Install Android SDK Platform 37.0 (revision 2)".
Downloading https://dl.google.com/android/repository/platform-37.0_r02.zip
"Install Android SDK Platform 37.0 (revision 2)" ready.
Installing Android SDK Platform 37.0 in /Users/lx/Library/Android/sdk/platforms/android-37.0
"Install Android SDK Platform 37.0 (revision 2)" complete.
"Install Android SDK Platform 37.0 (revision 2)" finished.
Preparing "Install Android SDK Platform-Tools v.37.0.1".
Downloading https://dl.google.com/android/repository/platform-tools_r37.0.1-darwin.zip
"Install Android SDK Platform-Tools v.37.0.1" ready.
Installing Android SDK Platform-Tools in /Users/lx/Library/Android/sdk/platform-tools
"Install Android SDK Platform-Tools v.37.0.1" complete.
"Install Android SDK Platform-Tools v.37.0.1" finished.
Preparing "Install Android Emulator v.37.1.11".
Downloading https://dl.google.com/android/repository/emulator-darwin_aarch64-15917651.zip
"Install Android Emulator v.37.1.11" ready.
Installing Android Emulator in /Users/lx/Library/Android/sdk/emulator
"Install Android Emulator v.37.1.11" complete.
"Install Android Emulator v.37.1.11" finished.
SDK Manager found the following installed packages: build-tools;36.0.0 emulator platform-tools platforms;android-37.0 sources;android-37.0
Android SDK is up to date.
```



## 安装 Easydict

​	一个简洁优雅的词典翻译 macOS App。开箱即用，支持离线 OCR 识别，支持有道词典，🍎 苹果系统词典，🍎 苹果系统翻译，OpenAI，Gemini，DeepL，Google，Bing，腾讯，百度，阿里，小牛，彩云和火山翻译。

```bash
# 到 https://github.com/tisfeng/Easydict/releases 下载最新版 Easydict.dmg
# 点击 Easydict.dmg 打开后拖入 Applications
# 执行以下命令，递归删除 Easydict 整个 App 包里所有文件的网络隔离标记
xattr -rd com.apple.quarantine /Applications/Easydict.app
```



## 安装 QuickRecorder

用来录屏

```bash
brew install lihaoyun6/tap/quickrecorder
```



## 安装 Navicat Premium Lite

用来访问数据库

```bash
# 访问 https://www.navicat.com/en/download/navicat-premium-lite
# 下载安装包
# 打开安装包，拖拽到 Applications
# 执行以下命令，递归删除 Navicat Premium Lite 整个 App 包里所有文件的网络隔离标记
# 下载的 Navicat 打开时，macOS 提示：
# “Navicat Premium Lite” 无法打开，因为 Apple 无法检查其是否包含恶意软件。
# 原理：macOS 检测到文件带有`com.apple.quarantine`标记，
# 触发 Gatekeeper 安全校验；如果软件未公证 / 签名，直接阻止运行。
# 执行这条命令相当于告诉系统：你信任这个程序，不再做隔离校验
xattr -rd com.apple.quarantine /Applications/Navicat\ Premium\ Lite.app 
# 使用临时邮箱注册账号
# 验证邮箱
# 登录账号
# 访问数据库
```

## 安装 `Chrome`

```bash
# 到官网 https://www.google.com/chrome/dr/download/ 下载 Chrome 的最新安装包
# 打开安装包，拖拽到 Applications
# 执行以下命令
xattr -rd com.apple.quarantine /Applications/Google\ Chrome.app 
```



## 撤销`git commit -m "提交信息"`

```bash
# 前提没有提交到远程仓库
# 推荐：撤销本次commit，代码保留在暂存区（最安全，不会丢代码）
# `HEAD^` = 上一个提交节点，回退 HEAD 指针，
# 文件改动还在 add 后的暂存状态，可以重新写 message 再 commit
git reset --soft HEAD^

# 或者
# 撤销本次commit，代码保留在工作区（取消add，需要重新git add）
# 等价 git reset --mixed HEAD^ （mixed是reset默认模式）
git reset HEAD^

# 如果你只是想修改这次空的 commit message，而不是撤销提交，直接：
git commit --amend -m "正确的提交信息"

```



## 撤销`git add -A`

​	`git add -A`：把**所有修改、删除、新增文件**全部加入暂存区（index）。撤销的本质：**取消暂存，代码保留在本地文件，不会丢失**。

```bash
git reset HEAD
# 等价于 git reset --mixed HEAD
```

​	执行后：

- 暂存区清空，所有文件回到**工作区未 add 状态**
- ✅ 本地修改**完全保留**，文件内容不变
- 执行 `git status` 就能看到：不再是 `Changes to be committed`

```bash
git restore --staged .
```

​	效果和 `git reset HEAD` 一模一样。

### 只撤销单个文件（不想全部取消）

```bash
git reset HEAD 文件名
# 示例：git reset HEAD src/main.rs
```

