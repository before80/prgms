+++
title = "02-源替换"
date = 2026-07-30T14:49:00+08:00
weight = 37
type = "docs"
description = "用 source.crates-io.replace-with 等替换源"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Cargo Book](https://doc.rust-lang.org/cargo/)

# 源替换 {#source-replacement}


> 原文链接: [https://doc.rust-lang.org/cargo/reference/source-replacement.html](https://doc.rust-lang.org/cargo/reference/source-replacement.html)


本文档关于将与[注册表][registries]或基于 [git 的依赖][git-based dependencies]仓库的通信重定向到另一个数据源，例如镜像原始注册表的服务器或精确的本地副本。

若你想给个别依赖打补丁，见本文档的[覆盖依赖][overriding dependencies]一节。若你想控制 Cargo 如何发出网络请求，见 [`[http]`](../../06-configuration/#http) 与 [`[net]`](../../06-configuration/#net) 配置。

*源（source）* 是包含可能作为包依赖包含的 crate 的提供者。Cargo 支持**用一个源替换另一个源**的能力，以表达如下策略：

* 供应商化（Vendoring）—— 可定义表示本地文件系统上 crate 的自定义源。这些源是它们所替换源的子集，必要时可检入包中。

* 镜像（Mirroring）—— 源可被等价版本替换，该版本充当 crates.io 本身的缓存。

Cargo 对源替换有一个核心假设：两个源的源代码完全相同。注意这也意味着替换源不允许有原始源中不存在的 crate。

因此，源替换不适用于给依赖打补丁或私有注册表等情况。Cargo 通过使用 [`[patch]` 键][overriding dependencies]支持给依赖打补丁，私有注册表支持在[注册表章节][registries]中描述。

使用源替换时，运行需要直接联系注册表的命令[^1]需要传递 `--registry` 选项。这有助于避免关于联系哪个注册表的任何歧义，并将使用指定注册表的认证令牌。

[^1]: 此类命令的示例见[发布命令][Publishing Commands]。

[Publishing Commands]: ../../../cargo-commands/publishing-commands/
[overriding dependencies]: ../01-overriding-dependencies/
[registries]: ../../registries/

## 配置 {#configuration}
替换源的配置通过 [`.cargo/config.toml`][config] 完成，可用键的完整集合为：

```toml
# `source` 表是所有与源替换相关的键的存放处。
[source]

# 在 `source` 表下有若干其他表，其键是相关源的名称。
# 例如本节定义了一个新源，名为 `my-vendor-source`，
# 它来自相对于包含此 `.cargo/config.toml` 文件的目录的 `vendor` 目录
[source.my-vendor-source]
directory = "vendor"

# crates 的 crates.io 默认源可在名称 "crates-io" 下获得，
# 这里我们使用 `replace-with` 键表明它被上面的源替换。
# `replace-with` 键也可以引用在 `[registries]` 表中定义的替代注册表名称。
[source.crates-io]
replace-with = "my-vendor-source"

# 每个源都有自己的表，键是源的名称
[source.the-source-name]

# 表明 `the-source-name` 将被别处定义的 `another-source` 替换
replace-with = "another-source"

# 可以指定几种源（下文有更详细描述）：
registry = "https://example.com/path/to/index"
local-registry = "path/to/registry"
directory = "path/to/vendor"

# Git 源还可以选择性地指定 branch/tag/rev
git = "https://example.com/path/to/repo"
# branch = "master"
# tag = "v1.0.1"
# rev = "313f44e8"
```

[config]: ../../06-configuration/

## 注册表源 {#registry-sources}
「注册表源」是像 crates.io 本身一样工作的源。它是一个符合 https://doc.rust-lang.org/cargo/reference/registry-index.html 规范的索引，并带有指示从何处下载 crate 的配置文件。

注册表源可使用 [git 或稀疏 HTTP 协议][protocols]：

```toml
# Git 协议
registry = "ssh://git@example.com/path/to/index.git"

# 稀疏 HTTP 协议
registry = "sparse+https://example.com/path/to/index"

# HTTPS git 协议
registry = "https://example.com/path/to/index"
```

[protocols]: ../../registries/#registry-protocols

[crates.io index]: ../../registries/running-a-registry/01-registry-index/

## 本地注册表源 {#local-registry-sources}
「本地注册表源」旨在成为另一注册表源的子集，但在本地文件系统上可用（即供应商化）。本地注册表会提前下载，通常与 `Cargo.lock` 同步，并由一组 `*.crate` 文件以及与普通注册表类似的索引组成。

管理与创建本地注册表源的主要方式是通过 [`cargo-local-registry`][cargo-local-registry] 子命令，[可在 crates.io 上获得][cargo-local-registry]，并可用 `cargo install cargo-local-registry` 安装。

[cargo-local-registry]: https://crates.io/crates/cargo-local-registry

本地注册表包含在一个目录中，并包含从 crates.io 下载的若干 `*.crate` 文件，以及一个与 crates.io-index 项目格式相同的 `index` 目录（仅填充存在的那些 crate 的条目）。

## 目录源 {#directory-sources}
「目录源」类似于本地注册表源，它包含本地文件系统上可用的若干 crate，适合供应商化依赖。目录源主要由 `cargo vendor` 子命令管理。

目录源与本地注册表的区别在于它们包含 `*.crate` 文件的解包版本，在某些情况下更适合将所有内容检入源代码控制。目录源就是一个包含若干其他目录的目录，这些其他目录包含 crate 的源代码（`*.crate` 文件的解包版本）。目前对每个目录的名称没有限制。

目录源中的每个 crate 还有一个关联的元数据文件 `.cargo-checksum.json`，以防止意外修改。
它不是安全机制，也不能防止恶意更改。

## Git 源 {#git-sources}
Git 源表示[基于 git 的依赖][git-based dependencies]所使用的仓库。它们用于指定哪些基于 git 的依赖应被替代源替换。

Git 源与 [git 注册表][protocols]*无关*，
不能用于替换注册表源。

[git-based dependencies]: ../../#specifying-dependencies-from-git-repositories
