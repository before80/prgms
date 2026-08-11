+++
title = "12-注册表"
date = 2026-07-30T14:49:00+08:00
weight = 49
type = "docs"
description = "使用与配置包注册表"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Cargo Book](https://doc.rust-lang.org/cargo/)

# 注册表


> 原文链接: [https://doc.rust-lang.org/cargo/reference/registries.html](https://doc.rust-lang.org/cargo/reference/registries.html)


Cargo 从「注册表（registry）」安装 crate 并获取依赖。默认注册表是 [crates.io]。注册表包含一个「索引（index）」，其中有可搜索的可用 crate 列表。注册表还可提供 Web API，以支持直接从 Cargo 发布新 crate。

> 注意：若你有兴趣镜像或供应商化（vendoring）现有注册表，请参阅 [源替换][Source Replacement]。

若你在实现注册表服务器，请参阅 [运行注册表][Running a Registry]，了解 Cargo 与注册表之间的协议细节。

若你使用需要认证的注册表，请参阅 [注册表认证][Registry Authentication]。
若你在实现凭证提供者，请参阅 [凭证提供者协议][Credential Provider Protocol] 了解细节。

## 使用备用注册表 {#using-an-alternate-registry}
要使用 [crates.io] 以外的注册表，必须将该注册表的名称与索引 URL 添加到 [`.cargo/config.toml` 文件][config] 中。`registries` 表为每个注册表设一个键，例如：

```toml
[registries]
my-registry = { index = "https://my-intranet:8080/git/index" }
```

`index` 键应为指向注册表索引的 git 仓库 URL，或以 `sparse+` 前缀开头的 Cargo 稀疏注册表 URL。

随后，crate 可通过在 `Cargo.toml` 的依赖条目中指定 `registry` 键及其注册表名称，来依赖另一注册表中的 crate：

```toml
# 示例 Cargo.toml
[package]
name = "my-project"
version = "0.1.0"
edition = "2024"

[dependencies]
other-crate = { version = "1.0", registry = "my-registry" }
```

与大多数配置值一样，索引也可用环境变量代替配置文件指定。例如，设置以下环境变量可达到与定义配置文件相同的效果：

```ignore
CARGO_REGISTRIES_MY_REGISTRY_INDEX=https://my-intranet:8080/git/index
```

> 注意：[crates.io] 不接受依赖其他注册表中 crate 的包。

## 发布到备用注册表 {#publishing-to-an-alternate-registry}
若注册表支持 Web API 访问，则可直接从 Cargo 将包发布到该注册表。Cargo 的若干命令（如 [`cargo publish`]）接受 `--registry` 命令行标志以指明使用哪个注册表。例如，要发布当前目录中的包：

1. `cargo login --registry=my-registry`

    这只需做一次。你必须输入从注册表网站获取的密钥 API token。也可将 token 通过 `--token` 命令行标志直接传给 `publish` 命令，或通过以注册表命名的环境变量（如 `CARGO_REGISTRIES_MY_REGISTRY_TOKEN`）传递。

2. `cargo publish --registry=my-registry`

不必总是传递 `--registry` 命令行选项，可在 [`.cargo/config.toml`][config] 中用 `registry.default` 键设置默认注册表。例如：

```toml
[registry]
default = "my-registry"
```

在 `Cargo.toml` 清单中设置 `package.publish` 键可限制包允许发布到哪些注册表。这有助于防止将闭源包意外发布到 [crates.io]。其值可以是注册表名称列表，例如：

```toml
[package]
# ...
publish = ["my-registry"]
```

`publish` 的值也可以是 `false`，以禁止一切发布，效果与空列表相同。

[`cargo login`] 保存的认证信息存放在 Cargo 主目录（默认 `$HOME/.cargo`）下的 `credentials.toml` 文件中。它为每个注册表设有独立的表，例如：

```toml
[registries.my-registry]
token = "854DvwSlUwEHtIo3kWy6x7UCPKHfzCmy"
```

## 注册表协议 {#registry-protocols}
Cargo 支持两种远程注册表协议：`git` 与 `sparse`。若注册表索引 URL 以 `sparse+` 开头，Cargo 使用稀疏协议；否则使用 `git` 协议。

`git` 协议将索引元数据存放在 git 仓库中，要求 Cargo 克隆整个仓库。

`sparse` 协议使用普通 HTTP 请求获取各个元数据文件。由于 Cargo 只下载相关 crate 的元数据，`sparse` 协议可显著节省时间与带宽。

[crates.io] 注册表同时支持两种协议。crates.io 所用的协议由 [`registries.crates-io.protocol`] 配置键控制。

[Source Replacement]: ../specifying-dependencies/02-source-replacement/
[Running a Registry]: running-a-registry/
[Credential Provider Protocol]: registry-authentication/01-credential-provider-protocol/
[Registry Authentication]: registry-authentication/
[`cargo publish`]: ../../cargo-commands/publishing-commands/05-cargo-publish/
[`cargo package`]: ../../cargo-commands/publishing-commands/04-cargo-package/
[`cargo login`]: ../../cargo-commands/publishing-commands/01-cargo-login/
[config]: ../06-configuration/
[crates.io]: https://crates.io/
[`registries.crates-io.protocol`]: ../06-configuration/#registriescrates-ioprotocol
