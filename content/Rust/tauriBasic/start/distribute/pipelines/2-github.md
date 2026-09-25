+++
title = "2 GitHub"
date = 2026-09-25T21:31:08+08:00
weight = 2
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

> 原文链接: [https://tauri.app/distribute/pipelines/github/](https://tauri.app/distribute/pipelines/github/)

本指南将展示如何在 [GitHub Actions](https://docs.github.com/en/actions) 中使用 [tauri-action](https://github.com/tauri-apps/tauri-action) 轻松构建并上传你的应用，以及如何让 Tauri 的更新器查询新建的 GitHub release 以获取更新。

最后，它还会展示如何为 Linux Arm AppImage 配置更复杂的构建流水线。

{{% alert title="代码签名" %}}

要在 workflow 中为 Windows 和 macOS 设置代码签名，请遵循各平台的专门指南：

- [Windows 代码签名](../../sign/3-windows/)
- [macOS 代码签名](../../sign/1-macos/)

如果你在没有 Apple 签名证书的情况下构建 macOS 应用，请配置
[ad-hoc 签名身份](../../sign/1-macos/#ad-hoc-签名)。这可以避免 macOS 把从 GitHub release 下载的 Apple Silicon 构建视为已损坏。

{{% /alert %}}

## 入门

要设置 `tauri-action`，你必须先准备一个 GitHub 仓库。你也可以在尚未配置 Tauri 的仓库上使用该 action，因为它可以自动为你初始化 Tauri，必要的配置选项请参阅[该 action 的 readme](https://github.com/tauri-apps/tauri-action/#project-initialization)。

前往你 GitHub 项目页面的 Actions 标签，选择 “New workflow”，然后选择 “Set up a workflow yourself”。用[下面](#示例-workflow)的 workflow 或[该 action 的示例](https://github.com/tauri-apps/tauri-action/tree/dev/examples)之一替换该文件。

## 配置

所有可用配置选项请参阅 `tauri-action` 的 [readme](https://github.com/tauri-apps/tauri-action/#inputs)。

当你的应用不在仓库根目录时，请使用 `projectPath` 输入项。

你可以随意修改 workflow 名称、更改它的触发条件，并添加更多步骤，例如 `npm run lint` 或 `npm run test`。重要的是把下面这一行保留在 workflow 末尾，因为它会运行构建脚本并发布你的应用。

### 如何触发

下面展示的、以及 `tauri-action` 示例中的发布 workflow，是通过推送到 `release` 分支触发的。该 action 会使用应用版本自动创建 git tag 和 GitHub release 的标题。

再举一个例子，你也可以把触发条件改为推送形如 `app-v0.7.0` 的版本 git tag：

```yaml
name: 'publish'

on:
  push:
    tags:
      - 'app-v*'
```

关于触发配置的完整列表，请查看 [GitHub 官方文档](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows)。

## 示例 workflow

下面是一个示例 workflow，它被配置为每次你推送到 `release` 分支时运行。

该 workflow 会为 Windows x64、Linux x64、Linux Arm64、macOS x64 和 macOS Arm64（M1 及以上）构建并发布你的应用。

它执行的步骤是：

1. 使用 `actions/checkout@v7` 检出仓库。
2. 安装构建应用所需的 Linux 系统依赖。
3. 使用 `actions/setup-node@v6` 配置 Node.js LTS 以及全局 npm/yarn/pnpm 包数据的缓存。
4. 使用 `dtolnay/rust-toolchain@stable` 和 `swatinem/rust-cache@v2` 配置 Rust 以及 Rust 构建产物的缓存。
5. 安装前端依赖，如果未配置为 [`beforeBuildCommand`](https://tauri.app/reference/config/#beforebuildcommand)，则运行 Web 应用的构建脚本。
6. 最后，使用 `tauri-apps/tauri-action@v1` 运行 `tauri build`、生成产物并创建 GitHub release。

```yaml
name: 'publish'

on:
  workflow_dispatch:
  push:
    branches:
      - release

jobs:
  publish-tauri:
    permissions:
      contents: write
    strategy:
      fail-fast: false
      matrix:
        include:
          - platform: 'macos-latest' # 面向基于 Arm 的 mac（M1 及以上）。
            args: '--target aarch64-apple-darwin'
          - platform: 'macos-latest' # 面向基于 Intel 的 mac。
            args: '--target x86_64-apple-darwin'
          - platform: 'ubuntu-22.04'
            args: ''
          - platform: 'ubuntu-22.04-arm' # 仅在公开仓库可用。
            args: ''
          - platform: 'windows-latest'
            args: ''

    runs-on: ${{ matrix.platform }}
    steps:
      - uses: actions/checkout@v7

      - name: install dependencies (ubuntu only)
        if: matrix.platform == 'ubuntu-22.04' || matrix.platform == 'ubuntu-22.04-arm' # 必须与上面定义的 platform 值匹配。
        run: |
          sudo apt-get update
          sudo apt-get install -y libwebkit2gtk-4.1-dev libappindicator3-dev librsvg2-dev patchelf xdg-utils

      - name: setup node
        uses: actions/setup-node@v6
        with:
          node-version: lts/*
          cache: 'npm' # 设为 npm、yarn 或 pnpm。

      - name: install Rust stable
        uses: dtolnay/rust-toolchain@stable
        with:
          # 那些 target 只在 macos runner 上使用，因此放在 `if` 里以略微加快 windows 和 linux 构建。
          targets: ${{ matrix.platform == 'macos-latest' && 'aarch64-apple-darwin,x86_64-apple-darwin' || '' }}

      - name: Rust cache
        uses: swatinem/rust-cache@v2
        with:
          # 这与 tauri 的默认项目结构一致。如果你的结构不同请修改。
          workspaces: './src-tauri -> target'

      - name: install frontend dependencies
        # 如果你没有配置 `beforeBuildCommand`，你可能也想在这里构建前端。
        run: npm install # 根据你使用的包管理器改成 npm、yarn 或 pnpm。

      - uses: tauri-apps/tauri-action@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          tagName: app-v__VERSION__ # 该 action 会自动把 __VERSION__ 替换为应用版本。
          releaseName: 'App v__VERSION__'
          releaseBody: 'See the assets to download this version and install.'
          releaseDraft: true
          prerelease: false
          args: ${{ matrix.args }}
```

更多配置选项请查看 [`tauri-action`](https://github.com/tauri-apps/tauri-action) 仓库及其[示例](https://github.com/tauri-apps/tauri-action/blob/dev/examples/)。

{{% alert title="警告" color="warning" %}}

请仔细阅读 GitHub Actions 的[使用限制、计费与管理](https://docs.github.com/en/actions/learn-github-actions/usage-limits-billing-and-administration)文档。

{{% /alert %}}

## Arm Runner 编译

{{% alert title="2025 年 8 月更新" %}}
GitHub 已经[发布](https://github.blog/changelog/2025-08-07-arm64-hosted-runners-for-public-repositories-are-now-generally-available/#get-started)了公开可用的 `ubuntu-22.04-arm` 和 `ubuntu-24.04-arm` runner。你可以在公开仓库中使用上面的 workflow 示例，用它们为 Arm64 构建应用。
{{% /alert %}}

该 workflow 使用 [`pguyot/arm-runner-action`](https://github.com/pguyot/arm-runner-action) 直接在模拟的 Arm runner 上编译。它弥补了 AppImage 工具链缺失跨架构构建支持的空缺。

{{% alert title="危险" color="warning" %}}
`arm-runner-action` **远比** GitHub 的标准 runner 慢，因此在按构建分钟计费的私有仓库中要小心。一个全新的 `create-tauri-app` 项目在无缓存构建时需要约 1 小时。
{{% /alert %}}

```yaml
name: 'Publish Linux Arm builds'

on:
  workflow_dispatch:
  push:
    branches:
      - release

jobs:
  build:
    runs-on: ubuntu-22.04

    strategy:
      matrix:
        arch: [aarch64, armv7l]
        include:
          - arch: aarch64
            cpu: cortex-a72
            base_image: https://dietpi.com/downloads/images/DietPi_RPi5-ARMv8-Bookworm.img.xz
            deb: arm64
            rpm: aarch64
            appimage: aarch64
          - arch: armv7l
            cpu: cortex-a53
            deb: armhfp
            rpm: arm
            appimage: armhf
            base_image: https://dietpi.com/downloads/images/DietPi_RPi-ARMv7-Bookworm.img.xz

    steps:
      - uses: actions/checkout@v3

      - name: Cache rust build artifacts
        uses: Swatinem/rust-cache@v2
        with:
          workspaces: src-tauri
          cache-on-failure: true

      - name: Build app
        uses: pguyot/arm-runner-action@v2.6.5
        with:
          base_image: ${{ matrix.base_image }}
          cpu: ${{ matrix.cpu }}
          bind_mount_repository: true
          image_additional_mb: 10240
          optimize_image: no
          #exit_on_fail: no
          commands: |
            # 防止 Rust 抱怨 $HOME 与 eid home 不一致
            export HOME=/root

            # 规避 CI worker 卡在 Updating crates.io index 的问题
            export CARGO_REGISTRIES_CRATES_IO_PROTOCOL=sparse

            # 安装前置依赖
            apt-get update -y --allow-releaseinfo-change
            apt-get autoremove -y
            apt-get install -y --no-install-recommends --no-install-suggests curl libwebkit2gtk-4.1-dev build-essential libssl-dev libgtk-3-dev libayatana-appindicator3-dev librsvg2-dev patchelf libfuse2 file
            curl https://sh.rustup.rs -sSf | sh -s -- -y
            . "$HOME/.cargo/env"
            curl -fsSL https://deb.nodesource.com/setup_lts.x | bash
            apt-get install -y nodejs

            # 安装前端依赖
            npm install

            # 构建应用
            npm run tauri build -- --verbose

      - name: Get app version
        run: echo "APP_VERSION=$(jq -r .version src-tauri/tauri.conf.json)" >> $GITHUB_ENV

      # TODO：把这一步与基础 workflow 合并，并把文件上传到 Release。
      - name: Upload deb bundle
        uses: actions/upload-artifact@v3
        with:
          name: Debian Bundle
          path: ${{ github.workspace }}/src-tauri/target/release/bundle/deb/appname_${{ env.APP_VERSION }}_${{ matrix.deb }}.deb

      - name: Upload rpm bundle
        uses: actions/upload-artifact@v3
        with:
          name: RPM Bundle
          path: ${{ github.workspace }}/src-tauri/target/release/bundle/rpm/appname-${{ env.APP_VERSION }}-1.${{ matrix.rpm }}.rpm

      - name: Upload appimage bundle
        uses: actions/upload-artifact@v3
        with:
          name: AppImage Bundle
          path: ${{ github.workspace }}/src-tauri/target/release/bundle/appimage/appname_${{ env.APP_VERSION }}_${{ matrix.appimage }}.AppImage
```

## 故障排除

### GitHub 环境令牌

GitHub Token 由 GitHub 在每次 workflow 运行时自动签发，无需额外配置，因此没有密钥泄露的风险。但该 token 默认只有读权限，运行 workflow 时你可能会遇到 “Resource not accessible by integration” 错误。如果出现这种情况，你可能需要为该 token 添加写权限。做法是进入 GitHub 项目设置，选择 `Actions`，向下滚动到 `Workflow permissions`，勾选 “Read and write permissions”。

你可以通过 workflow 中的这一行看到传给 workflow 的 GitHub Token：

```yaml
env:
  GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```
