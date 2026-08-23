+++
title = "04-发布新版本"
date = 2026-08-22T18:00:00+08:00
weight = 824
type = "docs"
description = "Clippy 发布流程"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Clippy Documentation](https://doc.rust-lang.org/nightly/clippy/)

# 发布新版本 {#release}


> 原文链接: [https://doc.rust-lang.org/nightly/clippy/development/infrastructure/release.html](https://doc.rust-lang.org/nightly/clippy/development/infrastructure/release.html)


> _注意：_ 本文可能仅对与 Clippy 团队成员相关。

Clippy 与 Rust stable 发布一起发布。发布日期见 [Rust Forge]。本文说明创建 Clippy 发布所需的步骤。

1. [定义远程](#定义远程)
1. [提升版本号](#提升版本号)
1. [找到 Clippy 提交](#找到-clippy-提交)
1. [更新 `beta` 分支](#更新-beta-分支)
1. [更新 `stable` 分支](#更新-stable-分支)
1. [为 stable 提交打标签](#为-stable-提交打标签)
1. [更新 `CHANGELOG.md`](#更新-changelogmd)

[Rust Forge]: https://forge.rust-lang.org/

## 定义远程

可为 Clippy 项目定义 `upstream` 远程以简化后续步骤。此为可选，也可用完整 URL 替代 `upstream`。

```bash
git remote add upstream git@github.com:rust-lang/rust-clippy
```

## 提升版本号

需要发布时，若 `Cargo.toml` 中的版本不正确，`cargo test` 会失败。该同步期间需提升版本号，运行：

```bash
cargo dev release bump_version
```

这会增加每个相关 `Cargo.toml` 文件的版本号。然后提交更新文件：

```bash
git commit -m "Bump Clippy version -> 0.1.XY" **/*Cargo.toml
```

将 `XY` 替换为对应版本号。

## 找到 Clippy 提交

更新 `beta` 与 `stable` 分支的第一步，都是找到相应 Rust 分支中最后一次 Clippy 同步的 Clippy 提交。

在 **Rust 仓库**中运行以下命令可获取指定 `<branch>` 的提交：

```bash
git switch <branch>
SHA=$(git log --oneline -- src/tools/clippy/ | grep -o "Merge commit '[a-f0-9]*' into .*" | head -1 | sed -e "s/Merge commit '\([a-f0-9]*\)' into .*/\1/g")
```

其中 `<branch>` 为 `stable`、`beta` 或 `master` 之一。

## 更新 `beta` 分支

获取 `beta` 分支的提交后，可更新 Clippy 仓库的 `beta` 分支。

```bash
git checkout beta
git reset --hard $SHA
git push upstream beta
```

## 更新 `stable` 分支

获取 `stable` 分支的提交后，可更新 Clippy 仓库的 `stable` 分支。

```bash
git checkout stable
git reset --hard $SHA
git push upstream stable
```

## 为 `stable` 提交打标签

更新 `stable` 分支后，为 HEAD 提交打标签并推送到 Clippy 仓库。

```bash
git tag rust-1.XX.0               # 将 XX 替换为对应版本
git push upstream rust-1.XX.0     # `upstream` 是 `rust-lang/rust-clippy` 远程
```

之后发布应出现在 Clippy [标签页][tags page]。

[tags page]: https://github.com/rust-lang/rust-clippy/tags

## 发布 `clippy_utils`

`clippy_utils` crate 发布到 `crates.io`，不提供稳定性保证。在[同步][sync]与发布完成后，切回 `upstream/master` 分支并发布 `clippy_utils`：

> 注意：提升 nightly 与 Clippy 版本的 Rustup PR **必须**在操作前合并。

```bash
git switch master && git pull upstream master
cargo publish --manifest-path clippy_utils/Cargo.toml
```

[sync]: sync.md

## 更新 `CHANGELOG.md`

详见[如何更新 changelog] 文档。

若暂时无法完成完整 changelog 更新，至少更新以下部分：

- 从新 stable 版本中移除 `(beta)`：

  ```markdown
  ## Rust 1.XX (beta) -> ## Rust 1.XX
  ```

- 更新新 stable 版本的发布日期行：

  ```markdown
  Current beta, release 20YY-MM-DD -> Current stable, released 20YY-MM-DD
  ```

- 更新上一 stable 版本的发布日期行：

  ```markdown
  Current stable, released 20YY-MM-DD -> Released 20YY-MM-DD
  ```

[how to update the changelog]: changelog_update.md
