+++
title = "02-Git 身份验证"
date = 2026-07-30T14:49:00+08:00
weight = 72
type = "docs"
description = "Cargo 使用 Git 依赖时的身份验证"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Cargo Book](https://doc.rust-lang.org/cargo/)

# Git 身份验证 {#git-authentication}


> 原文链接: [https://doc.rust-lang.org/cargo/appendix/git-authentication.html](https://doc.rust-lang.org/cargo/appendix/git-authentication.html)


Cargo 在使用 git 依赖与注册表时支持某些形式的身份验证。本附录介绍如何以
与 Cargo 兼容的方式设置 git 身份验证。

若你需要其他身份验证方法，可设置 [`net.git-fetch-with-cli`]
配置值，使 Cargo 执行 `git` 可执行文件来获取远程仓库，而不是使用内置支持。
也可通过环境变量 `CARGO_NET_GIT_FETCH_WITH_CLI=true` 启用。

> **注意：** 公共 git 依赖不需要身份验证；
> 若在此情境下看到身份验证失败，请确认 URL 是否正确。

## HTTPS 身份验证 {#https-authentication}
HTTPS 身份验证需要 [`credential.helper`] 机制。有多种凭证助手，
你在全局 git 配置文件中指定要使用的那一个。

```ini
# ~/.gitconfig
[credential]
helper = store
```

Cargo 不会询问密码，因此对大多数助手，你需要在运行 Cargo 之前先向助手提供初始用户名/密码。
一种做法是对私有 git 仓库运行 `git clone` 并输入用户名/密码。

> **提示：**<br>
> macOS 用户可考虑使用 osxkeychain 助手。<br>
> Windows 用户可考虑使用 [GCM] 助手。

> **注意：** Windows 用户需确保 `sh` shell 在 `PATH` 中可用。
> 这通常随 Git for Windows 安装一并提供。

## SSH 身份验证 {#ssh-authentication}
SSH 身份验证需要 `ssh-agent` 正在运行以获取 SSH 密钥。
确保设置了适当的环境变量（在大多数类 Unix 系统上为 `SSH_AUTH_SOCK`），
并用 `ssh-add` 添加了正确的密钥。

Windows 可以使用 Pageant（[PuTTY] 的一部分）或 `ssh-agent`。
要使用 `ssh-agent`，Cargo 需要使用 Windows 自带分发的 OpenSSH，
因为 Cargo 不支持 MinGW 或 Cygwin 使用的模拟 Unix 域套接字。
更多 Windows 安装信息见 [Microsoft 安装文档]，
[密钥管理]页面有关于如何启动 `ssh-agent` 与添加密钥的说明。

> **注意：** Cargo 不支持 git 的简写 SSH URL，例如
> `git@example.com:user/repo.git`。请使用完整 SSH URL，例如
> `ssh://git@example.com/user/repo.git`。

> **注意：** SSH 配置文件（如 OpenSSH 的 `~/.ssh/config`）不会被
> Cargo 的内置 SSH 库使用。更高级的需求应使用
> [`net.git-fetch-with-cli`]。

### SSH Known Hosts {#ssh-known-hosts}
连接到 SSH 主机时，Cargo 必须使用“known hosts”（已知主机，即主机密钥列表）
验证主机身份。Cargo 可在其标准位置查找 OpenSSH 风格的 `known_hosts` 文件
（主目录下的 `.ssh/known_hosts`，或类 Unix 平台上的
`/etc/ssh/ssh_known_hosts`，或 Windows 上的
`%PROGRAMDATA%\ssh\ssh_known_hosts`）。更多信息见 [sshd 手册页]。
也可以在 Cargo 配置文件中用 [`net.ssh.known-hosts`] 配置密钥。

在尚未配置 known hosts 时连接 SSH 主机，Cargo 会显示错误信息，指导你如何添加主机密钥。
其中还包括“指纹（fingerprint）”——主机密钥的较小哈希，更便于目视核对。
服务器管理员可对公钥运行 `ssh-keygen` 获取指纹（例如
`ssh-keygen -l -f /etc/ssh/ssh_host_ecdsa_key.pub`）。知名站点可能在网上公布指纹；
例如 GitHub 发布在
<https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/githubs-ssh-key-fingerprints>。

Cargo 内置了 [github.com](https://github.com) 的主机密钥。
若这些密钥发生变化，你可以把新密钥添加到配置或 known_hosts 文件中。

> **注意：** Cargo 不支持 `known_hosts` 文件中的 `@cert-authority` 或 `@revoked`
> 标记。若要使用这些功能，请使用
> [`net.git-fetch-with-cli`]。若 Cargo 的 SSH 客户端行为不符合预期，这也是一个好建议。

[`credential.helper`]: https://git-scm.com/book/en/v2/Git-Tools-Credential-Storage
[`net.git-fetch-with-cli`]: ../../cargo-reference/06-configuration/#netgit-fetch-with-cli
[`net.ssh.known-hosts`]: ../../cargo-reference/06-configuration/#netsshknown-hosts
[GCM]: https://github.com/microsoft/Git-Credential-Manager-Core/
[PuTTY]: https://www.chiark.greenend.org.uk/~sgtatham/putty/
[Microsoft 安装文档]: https://docs.microsoft.com/en-us/windows-server/administration/openssh/openssh_install_firstuse
[密钥管理]: https://docs.microsoft.com/en-us/windows-server/administration/openssh/openssh_keymanagement
[sshd 手册页]: https://man.openbsd.org/sshd#SSH_KNOWN_HOSTS_FILE_FORMAT
