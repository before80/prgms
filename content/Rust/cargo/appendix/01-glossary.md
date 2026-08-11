+++
title = "01-术语表"
date = 2026-07-30T14:49:00+08:00
weight = 71
type = "docs"
description = "Cargo 相关术语表"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Cargo Book](https://doc.rust-lang.org/cargo/)

# 术语表 {#glossary}


> 原文链接: [https://doc.rust-lang.org/cargo/appendix/glossary.html](https://doc.rust-lang.org/cargo/appendix/glossary.html)


## Artifact（产物） {#artifact}
*产物（artifact）* 是编译过程创建的文件或文件集合。包括可链接的库、可执行二进制文件，
以及生成的文档。

## Cargo {#cargo}
*Cargo* 是 Rust 的[*包管理器（package manager）*](#package-manager)，也是本手册的主题。

## Cargo.lock {#cargolock}
见[*锁文件（lock file）*](#lock-file)。

## Cargo.toml {#cargotoml}
见[*清单（manifest）*](#manifest)。

## Crate {#crate}
一个 Rust *crate* 要么是库，要么是可执行程序，分别称为
*库 crate（library crate）* 或 *二进制 crate（binary crate）*。

为 Cargo [包（package）](#package) 定义的每个[目标（target）](#target)都是一个 *crate*。

宽泛地说，术语 *crate* 既可指目标的源代码，也可指该目标生成的已编译产物。
它也可以指从[注册表（registry）](#registry)获取的压缩包。

给定 crate 的源代码可再划分为[*模块（modules）*](#module)。

## Edition（版本 / 版本纪元） {#edition}
*Rust edition* 是 Rust 语言发展的里程碑。
[包的 edition][edition-field] 在 `Cargo.toml`
[清单](#manifest)中指定，各个目标也可指定自己使用的 edition。
更多信息见 [Edition 指南][edition guide]。

## Feature（特性） {#feature}
*feature* 的含义取决于上下文：

- [*特性（feature）*][feature] 是一个命名标志，用于条件编译。特性可以指可选依赖，
  或在 `Cargo.toml` [清单](#manifest)中定义、可在源代码中检查的任意名称。

- Cargo 有[*不稳定特性标志*][cargo-unstable]，用于启用 Cargo 自身的实验性行为。

- Rust 编译器与 Rustdoc 也有各自的不稳定特性标志（见
  [The Unstable Book][unstable-book] 与 [The Rustdoc
  Book][rustdoc-unstable]）。

- CPU 目标有[*目标特性（target features）*][target-feature]，用于指定 CPU 能力。

## Index（索引） {#index}
*索引（index）* 是[*注册表*](#registry)中[*crate*](#crate) 的可搜索列表。

## Lock file（锁文件） {#lock-file}
`Cargo.lock` *锁文件* 会记录[*工作空间*](#workspace)或
[*包*](#package)中所用每个依赖的确切版本。由 Cargo 自动生成。见
[Cargo.toml 与 Cargo.lock]。

## Manifest（清单） {#manifest}
[*清单*][manifest] 是以 `Cargo.toml` 文件描述[包](#package)或
[工作空间](#workspace)的说明。

[*虚拟清单（virtual manifest）*][virtual] 是只描述工作空间、不包含包的 `Cargo.toml` 文件。

## Member（成员） {#member}
*成员（member）* 是属于[*工作空间*](#workspace)的[*包*](#package)。

## Module（模块） {#module}
Rust 的模块系统用于将代码组织成称为 *模块* 的逻辑单元，
在代码中提供隔离的命名空间。

给定 [crate](#crate) 的源代码可再划分为一个或多个独立模块。通常这样做是为了
按相关功能组织代码，或控制源码中符号（结构体、函数等）的可见范围（公有/私有）。

[`Cargo.toml`](#manifest) 文件主要关心它所定义的[包](#package)、其 crate，
以及它们依赖的 crate 所属的包。不过你在使用 Rust 时会经常看到“模块”一词，
因此应理解它与给定 crate 的关系。

## Package（包） {#package}
*包（package）* 是一组源文件加上描述该包的 `Cargo.toml`
[*清单*](#manifest)文件。包有名称与版本，用于指定包之间的依赖关系。

一个包包含多个[*目标*](#target)，每个目标都是一个
[*crate*](#crate)。`Cargo.toml` 描述包内 crate 的类型
（二进制或库），以及每个目标的一些元数据——如何构建、直接依赖是什么等，
如本手册通篇所述。

*包根（package root）* 是包的 `Cargo.toml` 清单所在目录。
（对比[*工作空间根*](#workspace)。）

[*包 ID 规范*][pkgid-spec]，或称 *SPEC*，是用于唯一引用
特定来源、特定版本包的字符串。

中小型 Rust 项目通常只需要一个包，尽管常见情况是一个包含有多个 crate。

较大项目可能涉及多个包，此时可用 Cargo
[*工作空间*](#workspace) 管理各包之间的共用依赖及其他相关元数据。

## Package manager（包管理器） {#package-manager}
宽泛地说，*包管理器* 是软件生态中用于自动化获取、安装与升级产物的程序
（或一组相关程序）。在编程语言生态中，包管理器是面向开发者的工具，
其主要功能是从某个中心仓库下载库产物及其依赖；这一能力常与执行软件构建
（通过调用语言特定编译器）相结合。

[*Cargo*](#cargo) 是 Rust 生态中的包管理器。Cargo 会下载你的 Rust
[包](#package)的依赖（称为 [*crate*](#crate) 的[*产物*](#artifact)）、
编译你的包、制作可分发包，并（可选地）上传到
[crates.io][]——Rust 社区的[*包注册表*](#registry)。

## Package registry（包注册表） {#package-registry}
见[*注册表*](#registry)。

## Project（项目） {#project}
[包](#package)的另一称呼。

## Registry（注册表） {#registry}
*注册表* 是包含一批可下载 [*crate*](#crate) 的服务，这些 crate 可被安装或用作
[*包*](#package)的依赖。Rust 生态中的默认注册表是
[crates.io](https://crates.io)。注册表有一个[*索引*](#index)，
包含所有 crate 的列表，并告诉 Cargo 如何下载所需 crate。

## Source（源） {#source}
*源（source）* 是可提供作为[*包*](#package)依赖的 [*crate*](#crate) 的提供者。
有几类源：

- **注册表源** --- 见[注册表](#registry)。
- **本地注册表源** --- 以压缩文件形式存放在文件系统上的一组 crate。见[本地注册表源]。
- **目录源** --- 以未压缩文件形式存放在文件系统上的一组 crate。见[目录源]。
- **路径源** --- 位于文件系统上的单个包（例如[路径依赖]）或一组包（例如[路径覆盖]）。
- **Git 源** --- 位于 git 仓库中的包（例如 [git 依赖][git dependency] 或 [git 源][git source]）。

更多信息见[源替换]。

## Spec {#spec}
见[包 ID 规范](#package)。

## Target（目标） {#target}
术语 *target* 的含义取决于上下文：

- **Cargo 目标** --- Cargo [*包*](#package) 由对应于将要生成的[*产物*](#artifact)的
  *目标* 组成。包可以有库、二进制、示例、测试与基准测试目标。
  [目标列表][targets] 在 `Cargo.toml` [*清单*](#manifest)中配置，
  通常可根据源文件的[目录布局]自动推断。
- **目标目录（Target Directory）** --- Cargo 将构建产物放在 *target* 目录中。
  默认是[*工作空间*](#workspace)根下名为 `target` 的目录，
  若不使用工作空间则为包根。可用 `--target-dir` 命令行选项、
  `CARGO_TARGET_DIR` [环境变量]，或 `build.target-dir` [配置选项][config option] 更改该目录。
  更多信息见[构建缓存]文档。
- **目标架构（Target Architecture）** --- 构建产物的操作系统与机器架构通常称为 *target*。
- **目标三元组（Target Triple）** --- 三元组是指定目标架构的特定格式。
  可称为 *target triple*（产物架构）与 *host triple*（编译器运行所在架构）。
  目标三元组可通过 `--target` 命令行选项或 `build.target`
  [配置选项][config option] 指定。三元组的一般格式为
  `<arch><sub>-<vendor>-<sys>-<abi>`，其中：

  - `arch` = 基础 CPU 架构，例如 `x86_64`、`i686`、`arm`、
    `thumb`、`mips` 等。
  - `sub` = CPU 子架构，例如 `arm` 有 `v7`、`v7s`、
    `v5te` 等。
  - `vendor` = 厂商，例如 `unknown`、`apple`、`pc`、`nvidia` 等。
  - `sys` = 系统名，例如 `linux`、`windows`、`darwin` 等。
    无操作系统的裸机通常用 `none`。
  - `abi` = ABI，例如 `gnu`、`android`、`eabi` 等。

  某些参数可省略。运行 `rustc --print target-list` 可查看受支持的目标列表。

## Test Targets（测试目标） {#test-targets}
Cargo 的 *测试目标* 生成有助于验证代码正确运行与正确性的二进制文件。有两类测试产物：

* **单元测试（Unit test）** --- *单元测试* 是直接从库或二进制目标编译出的可执行二进制。
  它包含库或二进制代码的全部内容，并运行带 `#[test]` 注解的函数，用于验证各个代码单元。
* **集成测试目标（Integration test target）** --- [*集成测试目标*][integration-tests]
  是从 *测试目标* 编译出的可执行二进制；该测试目标是独立的 [*crate*](#crate)，
  源码位于 `tests` 目录，或由 `Cargo.toml` [*清单*](#manifest)中的
  [`[[test]]` 表][targets] 指定。它旨在仅测试库的公共 API，或执行二进制以验证其运行。

## Workspace（工作空间） {#workspace}
[*工作空间*][workspace] 是一个或多个[*包*](#package)的集合，它们共享依赖解析
（共享同一个 `Cargo.lock` [*锁文件*](#lock-file)）、输出目录，以及配置文件等各类设置。

[*虚拟工作空间（virtual workspace）*][virtual] 是根 `Cargo.toml`
[*清单*](#manifest)不定义包、只列出工作空间[*成员*](#member)的工作空间。

*工作空间根（workspace root）* 是工作空间的 `Cargo.toml` 清单所在目录。
（对比[*包根*](#package)。）


[Cargo.toml 与 Cargo.lock]: ../../cargo-guide/06-cargo-toml-vs-cargo-lock/
[目录源]: ../../cargo-reference/specifying-dependencies/02-source-replacement/#directory-sources
[本地注册表源]: ../../cargo-reference/specifying-dependencies/02-source-replacement/#local-registry-sources
[源替换]: ../../cargo-reference/specifying-dependencies/02-source-replacement/
[构建缓存]: ../../cargo-reference/09-build-cache/
[cargo-unstable]: ../../cargo-reference/17-unstable-features/
[config option]: ../../cargo-reference/06-configuration/
[crates.io]: https://crates.io/
[directory layout]: ../../cargo-guide/05-package-layout/
[edition guide]: https://doc.rust-lang.org/edition-guide/
[edition-field]: ../../cargo-reference/the-manifest-format/#the-edition-field
[environment variable]: ../../cargo-reference/07-environment-variables/
[feature]: ../../cargo-reference/features/
[git dependency]: ../../cargo-reference/specifying-dependencies/#specifying-dependencies-from-git-repositories
[git source]: ../../cargo-reference/specifying-dependencies/02-source-replacement/
[integration-tests]: ../../cargo-reference/the-manifest-format/01-cargo-targets/#integration-tests
[manifest]: ../../cargo-reference/the-manifest-format/
[path dependency]: ../../cargo-reference/specifying-dependencies/#specifying-path-dependencies
[path overrides]: ../../cargo-reference/specifying-dependencies/01-overriding-dependencies/#paths-overrides
[pkgid-spec]: ../../cargo-reference/10-package-id-specifications/
[rustdoc-unstable]: https://doc.rust-lang.org/nightly/rustdoc/unstable-features.html
[target-feature]: https://doc.rust-lang.org/reference/attributes/codegen.html#the-target_feature-attribute
[targets]: ../../cargo-reference/the-manifest-format/01-cargo-targets/#configuring-a-target
[unstable-book]: https://doc.rust-lang.org/nightly/unstable-book/index.html
[virtual]: ../../cargo-reference/02-workspaces/
[workspace]: ../../cargo-reference/02-workspaces/
