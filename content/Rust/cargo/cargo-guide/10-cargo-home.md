+++
title = "10-Cargo 主目录"
date = 2026-07-30T14:49:00+08:00
weight = 30
type = "docs"
description = "CARGO_HOME 目录结构与缓存位置"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Cargo Book](https://doc.rust-lang.org/cargo/)

# Cargo 主目录 {#cargo-home}


> 原文链接: [https://doc.rust-lang.org/cargo/guide/cargo-home.html](https://doc.rust-lang.org/cargo/guide/cargo-home.html)


「Cargo 主目录」用作下载与源码缓存。构建 [crate][def-crate] 时，Cargo 会把下载的构建依赖存储在 Cargo 主目录中。你可以通过设置 `CARGO_HOME` [环境变量][env]来改变 Cargo 主目录的位置。若需要在 Rust crate 内获取该位置，[home](https://crates.io/crates/home) crate 提供了相应 API。默认情况下，Cargo 主目录位于 `$HOME/.cargo/`。

请注意，Cargo 主目录的内部结构尚未稳定，可能随时变更。

Cargo 主目录由以下组成部分构成：

## 文件： {#files}
* `config.toml`
	Cargo 的全局配置文件，参见参考中的[配置条目][config]。

* `credentials.toml`
 	来自 [`cargo login`] 的私有登录凭证，用于登录[注册表][def-registry]。

* `.crates.toml`、`.crates2.json`
	这些隐藏文件包含通过 [`cargo install`] 安装的 crate 的[包][def-package]信息。请勿手工编辑！

## 目录： {#directories}
* `bin`
bin 目录包含通过 [`cargo install`] 或 [`rustup`](https://rust-lang.github.io/rustup/) 安装的 crate 可执行文件。要使这些二进制文件可访问，请将该目录路径添加到 `$PATH` 环境变量。

 *  `git`
	Git 源存储于此：

    * `git/db`
		当 crate 依赖某个 git 仓库时，Cargo 会将该仓库作为裸仓库克隆到此目录，并在必要时更新。

    * `git/checkouts`
		若使用 git 源，会从 `git/db` 内的裸仓库检出所需提交到此目录。这为编译器提供该依赖所指定提交的仓库中的实际文件。同一仓库不同提交的多次检出是可能的。

* `registry`
	crate 注册表（如 [crates.io](https://crates.io/)）的包与元数据位于此处。

  * `registry/index`
		索引是一个裸 git 仓库，包含注册表中所有可用 crate 的元数据（版本、依赖等）。

  *  `registry/cache`
		下载的依赖存储在缓存中。crate 是带有 `.crate` 扩展名的压缩 gzip 归档。

  * `registry/src`
		若某个包需要已下载的 `.crate` 归档，会将其解压到 `registry/src` 文件夹，rustc 会在那里找到 `.rs` 文件。


## 在 CI 中缓存 Cargo 主目录 {#caching-the-cargo-home-in-ci}
为避免在持续集成中重新下载所有 crate 依赖，你可以缓存 `$CARGO_HOME` 目录。然而，缓存整个目录通常效率不高，因为它会包含两份已下载的源码。若我们依赖诸如 `serde 1.0.92` 的 crate 并缓存整个 `$CARGO_HOME`，实际上会缓存两份源码：`registry/cache` 中的 `serde-1.0.92.crate`，以及 `registry/src` 中解压出的 serde `.rs` 文件。这可能不必要地拖慢构建，因为下载、解压、重新压缩并把缓存重新上传到 CI 服务器可能花费一些时间。

若希望缓存用 [`cargo install`] 安装的二进制文件，需要缓存 `bin/` 文件夹以及 `.crates.toml` 与 `.crates2.json` 文件。

跨构建缓存以下文件与文件夹应已足够：

* `.crates.toml`
* `.crates2.json`
* `bin/`
* `registry/index/`
* `registry/cache/`
* `git/db/`



## 供应商化项目的所有依赖 {#vendoring-all-dependencies-of-a-project}
参见 [`cargo vendor`] 子命令。



## 清理缓存 {#clearing-the-cache}
理论上，你随时可以移除缓存的任何部分，若某个 crate 需要它们，Cargo 会尽力通过重新解压归档、从裸仓库检出，或直接从网络重新下载源码来恢复。

或者，[cargo-cache](https://crates.io/crates/cargo-cache) crate 提供了一个简单的 CLI 工具，可仅清理缓存的选定部分，或在命令行中显示其各组成部分的大小。

[`cargo install`]: ../../cargo-commands/package-commands/02-cargo-install/
[`cargo login`]: ../../cargo-commands/publishing-commands/01-cargo-login/
[`cargo vendor`]: ../../cargo-commands/manifest-commands/10-cargo-vendor/
[config]: ../../cargo-reference/06-configuration/
[def-crate]:     ../../appendix/01-glossary/#crate     '"crate" (glossary entry)'
[def-package]:   ../../appendix/01-glossary/#package   '"package" (glossary entry)'
[def-registry]:  ../../appendix/01-glossary/#registry  '"registry" (glossary entry)'
[env]: ../../cargo-reference/07-environment-variables/
