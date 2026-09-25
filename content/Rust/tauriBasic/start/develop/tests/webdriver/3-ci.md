+++
title = "3 持续集成"
date = 2026-09-25T21:31:08+08:00
weight = 3
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

> 原文链接: [https://tauri.app/develop/tests/webdriver/ci/](https://tauri.app/develop/tests/webdriver/ci/)

你可以在 CI 上使用 [`tauri-driver`](https://crates.io/crates/tauri-driver) 运行 [WebDriver](https://www.w3.org/TR/webdriver/) 测试。下面的示例使用我们[之前一起构建的](../example/2-webdriverio/) [WebdriverIO](https://webdriver.io/) 示例，以及 GitHub Actions。

WebDriver 测试在 Linux 上通过创建虚拟显示来执行。
某些 CI 系统（例如 GitHub Actions）也支持在 Windows 上运行 WebDriver 测试。

## GitHub Actions

下面的 GitHub Actions 假设：

1. Tauri 应用位于 `src-tauri` 文件夹中。
2. [WebdriverIO](https://webdriver.io/) 测试运行器位于 `e2e-tests` 目录，并在该目录下使用 `yarn test` 运行。

```yaml
on: [push]

# 我们 workflow 的名称
name: WebDriver

jobs:
  # 名为 test 的单个 job
  test:
    # 测试 job 的显示名称
    name: WebDriverIO Test Runner

    # 在矩阵平台上运行
    runs-on: ${{ matrix.platform }}
    strategy:
      # 某个矩阵运行失败时不要让其它运行也失败
      fail-fast: false
      # 设置测试应当运行的所有平台
      matrix:
        platform: [ubuntu-latest, windows-latest]

    # job 按**顺序**运行的步骤
    steps:
      # 在 workflow 运行器上检出代码
      - uses: actions/checkout@v4

      # 安装 Tauri 在 Linux 上编译所需的系统依赖。
      # 注意 `tauri-driver` 运行所需的额外依赖：`webkit2gtk-driver` 和 `xvfb`
      - name: Tauri dependencies
        if: matrix.platform == 'ubuntu-latest'
        run: |
          sudo apt-get update &&
          sudo apt-get install -y \
          libwebkit2gtk-4.1-dev \
          libayatana-appindicator3-dev \
          webkit2gtk-driver \
          xvfb

      # 使用 msedgedriver-tool 安装匹配的 Microsoft Edge Driver 版本
      - name: install msdgedriver (Windows)
        if: matrix.platform == 'windows-latest'
        run: |
          cargo install --git https://github.com/chippers/msedgedriver-tool
          & "$HOME/.cargo/bin/msedgedriver-tool.exe"
          $PWD.Path >> $env:GITHUB_PATH

      # 安装最新的稳定版 Rust
      - name: Setup rust-toolchain stable
        uses: dtolnay/rust-toolchain@stable

      # 为 Rust target 文件夹设置缓存
      - name: Setup Rust cache
        uses: Swatinem/rust-cache@v2
        with:
          workspaces: src-tauri

      # 在 webdriver 测试之前先运行 Rust 测试，避免测试一个已经损坏的应用
      - name: Cargo test
        run: cargo test

      # 安装撰写时的最新稳定版 node
      - name: Node 24
        uses: actions/setup-node@v4
        with:
          node-version: 24
          cache: 'yarn'

      # 用 Yarn 安装应用的 Node.js 依赖
      - name: Yarn install
        run: yarn install --frozen-lockfile

      # 用 Yarn 安装 e2e-tests 的 Node.js 依赖
      - name: Yarn install
        run: yarn install --frozen-lockfile
        working-directory: e2e-tests

      # 安装最新版本的 `tauri-driver`。
      # 注意：tauri-driver 的版本独立于其它任何 Tauri 版本
      - name: Install tauri-driver
        run: cargo install tauri-driver --locked

      # 在 Linux 上运行 WebdriverIO 测试套件。
      # 我们通过 `xvfb-run`（之前安装的依赖）运行它，以获得一个虚拟显示服务器，
      # 让应用无需修改代码就能无头运行
      - name: WebdriverIO (Linux)
        if: matrix.platform == 'ubuntu-latest'
        run: xvfb-run yarn test
        working-directory: e2e-tests

      # 在 Windows 上运行 WebdriverIO 测试套件。
      # 这种情况下我们可以直接运行测试。
      - name: WebdriverIO (Windows)
        if: matrix.platform == 'windows-latest'
        run: yarn test
        working-directory: e2e-tests
```
