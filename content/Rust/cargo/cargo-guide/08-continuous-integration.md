+++
title = "08-持续集成"
date = 2026-07-30T14:49:00+08:00
weight = 28
type = "docs"
description = "在 CI 中使用 Cargo 的常见做法"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Cargo Book](https://doc.rust-lang.org/cargo/)

# 持续集成 {#continuous-integration}


> 原文链接: [https://doc.rust-lang.org/cargo/guide/continuous-integration.html](https://doc.rust-lang.org/cargo/guide/continuous-integration.html)


## 入门 {#getting-started}
基本的 CI 会构建并测试你的项目：

### GitHub Actions {#github-actions}
要在 GitHub Actions 上测试你的包，下面是一个示例 `.github/workflows/ci.yml` 文件：

```yaml
name: Cargo Build & Test

on:
  push:
  pull_request:

env: 
  CARGO_TERM_COLOR: always

jobs:
  build_and_test:
    name: Rust project - latest
    runs-on: ubuntu-latest
    strategy:
      matrix:
        toolchain:
          - stable
          - beta
          - nightly
    steps:
      - uses: actions/checkout@v6
      - run: rustup update ${{ matrix.toolchain }} && rustup default ${{ matrix.toolchain }}
      - run: cargo build --verbose
      - run: cargo test --verbose
  
```

这会在全部三个发行通道上测试（注意任一工具链版本失败都会导致整个作业失败）。你也可以在 GitHub UI 中点击 `"Actions" > "new workflow"` 并选择 Rust，将[默认配置](https://github.com/actions/starter-workflows/blob/main/ci/rust.yml)添加到仓库。更多信息参见 [GitHub Actions 文档](https://docs.github.com/en/actions)。

### GitLab CI {#gitlab-ci}
要在 GitLab CI 上测试你的包，下面是一个示例 `.gitlab-ci.yml` 文件：

```yaml
stages:
  - build

rust-latest:
  stage: build
  image: rust:latest
  script:
    - cargo build --verbose
    - cargo test --verbose

rust-nightly:
  stage: build
  image: rustlang/rust:nightly
  script:
    - cargo build --verbose
    - cargo test --verbose
  allow_failure: true
```

这会在稳定通道与 nightly 通道上测试，但 nightly 上的任何破坏都不会导致整体构建失败。更多信息请参见 [GitLab CI 文档](https://docs.gitlab.com/ce/ci/yaml/index.html)。

### builds.sr.ht {#buildssrht}
要在 sr.ht 上测试你的包，下面是一个示例 `.build.yml` 文件。请务必将 `<your repo>` 与 `<your project>` 改为要克隆的仓库以及克隆后的目录。

```yaml
image: archlinux
packages:
  - rustup
sources:
  - <your repo>
tasks:
  - setup: |
      rustup toolchain install nightly stable
      cd <your project>/
      rustup run stable cargo fetch
  - stable: |
      rustup default stable
      cd <your project>/
      cargo build --verbose
      cargo test --verbose
  - nightly: |
      rustup default nightly
      cd <your project>/
      cargo build --verbose ||:
      cargo test --verbose  ||:
  - docs: |
      cd <your project>/
      rustup run stable cargo doc --no-deps
      rustup run nightly cargo doc --no-deps ||:
```

这会在稳定通道与 nightly 通道上测试并构建文档，但 nightly 上的任何破坏都不会导致整体构建失败。更多信息请参见 [builds.sr.ht 文档](https://man.sr.ht/builds.sr.ht/)。


### CircleCI {#circleci}
要在 CircleCI 上测试你的包，下面是一个示例 `.circleci/config.yml` 文件：

```yaml
version: 2.1
jobs:
  build:
    docker:
      # 查看 https://circleci.com/developer/images/image/cimg/rust#image-tags 获取最新镜像
      - image: cimg/rust:1.77.2
    steps:
      - checkout
      - run: cargo test
```

要运行更复杂的流水线，包括不稳定测试检测、缓存与产物管理，请参见 [CircleCI 配置参考](https://circleci.com/docs/configuration-reference/)。

## 验证最新依赖 {#verifying-latest-dependencies}
在 `Cargo.toml` 中[指定依赖](../../cargo-reference/specifying-dependencies/)时，它们通常匹配一个版本范围。穷尽测试所有版本组合不切实际。至少验证最新版本，可以对运行 [`cargo add`] 或 [`cargo install`] 的用户进行覆盖。

测试最新版本时需考虑：
- 尽量减少影响本地开发或 CI 的外部因素
- 新依赖发布的频率
- 项目愿意承担的风险水平
- CI 成本，包括间接成本，例如 CI 服务对并行运行器有上限，达到上限时新作业会被串行化

一些可能的方案包括：
- [不把 `Cargo.lock` 纳入版本控制](../../05-faq/#why-have-cargolock-in-version-control)
  - 取决于 PR 速度，许多版本可能未经测试
  - 代价是失去确定性
- 用 CI 作业验证最新依赖，但将其标记为「失败时继续」
  - 取决于 CI 服务，失败可能并不明显
  - 取决于 PR 速度，可能比必要情况消耗更多资源
- 用定时 CI 作业验证最新依赖
  - 托管 CI 服务可能对长时间未改动的仓库禁用定时作业，影响被动维护的包
  - 取决于 CI 服务，通知可能无法送达能处理失败的人
  - 若未与依赖发布频率平衡，可能测试的版本不够，或做了冗余测试
- 通过 PR 定期更新依赖，例如使用 [Dependabot] 或 [RenovateBot]
  - 可将依赖隔离到各自的 PR，或汇总到单个 PR
  - 只使用必要的资源
  - 可配置频率，以平衡 CI 资源与依赖版本覆盖

用 GitHub Actions 验证最新依赖的示例 CI 作业：
```yaml
jobs:
  latest_deps:
    name: Latest Dependencies
    runs-on: ubuntu-latest
    continue-on-error: true
    env:
      CARGO_RESOLVER_INCOMPATIBLE_RUST_VERSIONS: allow
    steps:
      - uses: actions/checkout@v6
      - run: rustup update stable && rustup default stable
      - run: cargo update --verbose
      - run: cargo build --verbose
      - run: cargo test --verbose
```
说明：
- 设置 [`CARGO_RESOLVER_INCOMPATIBLE_RUST_VERSIONS`](../../cargo-reference/06-configuration/#resolverincompatible-rust-versions)，以确保[解析器](../../cargo-reference/specifying-dependencies/03-dependency-resolution/)不会因项目的 [Rust 版本](../../cargo-reference/the-manifest-format/02-rust-version/)而限制所选依赖。

对于按平台或按 Rust 版本失败风险较高的项目，可能需要测试更多组合。

## 验证 `rust-version` {#verifying-rust-version}
发布指定了 [`rust-version`](../../cargo-reference/the-manifest-format/#the-rust-version-field) 的包时，验证该字段的正确性很重要。

可提供帮助的一些第三方工具包括：
- [`cargo-msrv`](https://crates.io/crates/cargo-msrv)
- [`cargo-hack`](https://crates.io/crates/cargo-hack)

用 GitHub Actions 实现的一种方式示例：
```yaml
jobs:
  msrv:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v6
    - uses: taiki-e/install-action@cargo-hack
    - run: cargo hack check --rust-version --workspace --all-targets --ignore-private
```
这试图在彻底性与周转时间之间取得平衡：
- 使用单一平台，因为大多数项目与平台无关，并信任平台相关依赖自行验证行为。
- 使用 `cargo check`，因为贡献者遇到的大多数问题是 API 可用性而非行为。
- 跳过未发布的包，因为假定只有通过注册表消费已验证项目的用户才会关心 `rust-version`。

## 检查警告 {#checking-for-warnings}
通常，项目希望在官方分支上「无警告」，同时对本地开发更宽松。可以使用 [`build.warnings = "deny"`] 在存在警告时让 CI 作业失败。

用 GitHub Actions 检查警告的示例 CI 作业：
```yaml
jobs:
  warnings:
    runs-on: ubuntu-latest
    env:
      CARGO_BUILD_WARNINGS: deny
    steps:
      - uses: actions/checkout@v6
      - run: rustup update stable && rustup default stable
      - run: rustup component add clippy
      - run: cargo clippy --all-targets --all-features --keep-going
```

注意事项：
- CI 可能因新的工具链版本而失败，因为警告周围的兼容性保证有限。可考虑固定工具链版本，并用自动化作业在新版本发布时创建升级工具链的 PR。
- 在选择要检查的平台、特性与包/构建目标组合时，平衡穷尽性与周转时间
- 某些 CI 系统对报告 lint 有直接集成，例如在 GitHub 上使用 [`clippy-sarif`]

[`build.warnings = "deny"`]: ../../cargo-reference/06-configuration/#buildwarnings
[`cargo add`]: ../../cargo-commands/manifest-commands/01-cargo-add/
[`cargo install`]: ../../cargo-commands/package-commands/02-cargo-install/
[`clippy-sarif`]: https://crates.io/crates/clippy-sarif
[Dependabot]: https://docs.github.com/en/code-security/dependabot/working-with-dependabot
[RenovateBot]: https://renovatebot.com/
