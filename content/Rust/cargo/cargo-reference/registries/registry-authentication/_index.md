+++
title = "01-注册表认证"
date = 2026-07-30T14:49:00+08:00
weight = 50
type = "docs"
description = "私有注册表登录与凭证"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Cargo Book](https://doc.rust-lang.org/cargo/)

# 注册表认证 {#registry-authentication}


> 原文链接: [https://doc.rust-lang.org/cargo/reference/registry-authentication.html](https://doc.rust-lang.org/cargo/reference/registry-authentication.html)


Cargo 通过凭证提供者（credential provider）向注册表认证。这些凭证提供者是 Cargo 用来存储与检索凭证的外部可执行文件或内置提供者。

对需要认证的备用注册表，*必须*配置凭证提供者，以免在不知不觉中将未加密凭证存到磁盘上。出于历史原因，公开（无需认证）的注册表不要求配置凭证提供者；若未配置任何提供者，则使用 `cargo:token` 提供者。

Cargo 还包含使用操作系统安全存储 token 的平台专用提供者。同时包含 `cargo:token` 提供者，它将凭证以未加密明文形式存储在 [credentials](../../06-configuration/#credentials) 文件中。

## 推荐配置 {#recommended-configuration}
建议在 `$CARGO_HOME/config.toml` 中配置全局凭证提供者列表，默认路径为：
* Windows：`%USERPROFILE%\.cargo\config.toml`
* Unix：`~/.cargo/config.toml`

此推荐配置使用操作系统提供者，并回退到 `cargo:token`，以查找 Cargo 的 [credentials](../../06-configuration/#credentials) 文件或环境变量：
```toml
# ~/.cargo/config.toml
[registry]
global-credential-providers = ["cargo:token", "cargo:libsecret", "cargo:macos-keychain", "cargo:wincred"]
```
*注意：靠后的条目优先级更高。
更多细节见 [`registry.global-credential-providers`](../../06-configuration/#registryglobal-credential-providers)。*

某些私有注册表也可能推荐特定于该注册表的凭证提供者。请查阅你的注册表文档确认是否如此。

## 内置提供者 {#built-in-providers}
Cargo 包含若干内置凭证提供者。可用的内置提供者可能在未来的 Cargo 版本中变更（目前尚无此计划）。

### `cargo:token` {#cargotoken}
使用 Cargo 的 [credentials](../../06-configuration/#credentials) 文件以未加密明文存储 token。
检索 token 时，会检查 `CARGO_REGISTRIES_<NAME>_TOKEN` 环境变量。
若未列出此凭证提供者，则 `*_TOKEN` 环境变量将不起作用。

### `cargo:wincred` {#cargowincred}
使用 Windows 凭据管理器存储 token。

凭证在凭据管理器的「Windows 凭据」下以 `cargo-registry:<index-url>` 形式存储。

### `cargo:macos-keychain` {#cargomacos-keychain}
使用 macOS 钥匙串存储 token。

可用「钥匙串访问」应用查看已存储的 token。

### `cargo:libsecret` {#cargolibsecret}
使用 [libsecret](https://wiki.gnome.org/Projects/Libsecret) 存储 token。

任何支持 libsecret 的密码管理器都可用于查看已存储的 token。以下是若干示例（非穷尽）：

- [GNOME Keyring](https://wiki.gnome.org/Projects/GnomeKeyring)
- [KDE Wallet Manager](https://apps.kde.org/kwalletmanager5/)（自 KDE Frameworks 5.97.0 起）
- [KeePassXC](https://keepassxc.org/)（自 2.5.0 起）

### `cargo:token-from-stdout <command> <args>` {#cargotoken-from-stdout-command-args}
启动一个子进程，从 stdout 返回 token。会去除换行。
* 该进程继承用户的 stdin 与 stderr。
* 成功时应退出码为 0，出错时为非零。
* 不支持 [`cargo login`] 与 [`cargo logout`]，若使用会返回错误。

将向被执行的命令提供以下环境变量：

* `CARGO` —— 执行该命令的 `cargo` 二进制文件路径。
* `CARGO_REGISTRY_INDEX_URL` —— 注册表索引的 URL。
* `CARGO_REGISTRY_NAME_OPT` —— 注册表的可选名称。不应作为查找键使用。

参数会传递给子命令。

[`cargo login`]: ../../../cargo-commands/publishing-commands/01-cargo-login/
[`cargo logout`]: ../../../cargo-commands/publishing-commands/02-cargo-logout/

## 凭证插件 {#credential-plugins}
对于遵循 Cargo [凭证提供者协议](01-credential-provider-protocol/) 的凭证提供者插件，配置值应为可执行文件路径的字符串（若在 `PATH` 上，则为可执行文件名）。

例如，要从 crates.io 安装 [cargo-credential-1password](https://crates.io/crates/cargo-credential-1password)，可按如下操作：

用 `cargo install cargo-credential-1password` 安装该提供者

在配置中添加到（或创建）`registry.global-credential-providers`：
```toml
[registry]
global-credential-providers = ["cargo:token", "cargo-credential-1password --account my.1password.com"]
```

`global-credential-providers` 中的值按空格拆分为路径与命令行参数。若要定义路径或参数中包含空格的全局凭证提供者，请使用 [`[credential-alias]` 表](../../06-configuration/#credential-alias)。
