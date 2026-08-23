+++
title = "01-同步变更"
date = 2026-08-22T18:00:00+08:00
weight = 821
type = "docs"
description = "与 rustc 仓库同步"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Clippy Documentation](https://doc.rust-lang.org/nightly/clippy/)

# 在 Clippy 与 rust-lang/rust 之间同步变更 {#sync}


> 原文链接: [https://doc.rust-lang.org/nightly/clippy/development/infrastructure/sync.html](https://doc.rust-lang.org/nightly/clippy/development/infrastructure/sync.html)


Clippy 目前使用固定的 nightly 版本构建。

在 rustc 所在的 `rust-lang/rust` 仓库中，有一份 Clippy 副本，编译器开发者会不时修改它以适配编译器不稳定 API 的变更。

我们需要定期将这些变更同步回本仓库，同时本仓库期间的变更也需同步到 `rust-lang/rust`。

为避免淹没 `rust-lang/rust` 的 PR 队列，若无紧急变更，这一双向同步每两周进行一次。从 Rust 稳定版发布当日开始，此后每隔一周进行一次。这样可保证本仓库与最新编译器 API 同步，且 Clippy 的每项功能在进入 beta 前可在 nightly 上可用两周。参考：按此节奏进行的首次同步于 2020-08-27 完成。

以下各节详细说明该流程。关于 Rust 仓库中 `subtree` 的一般信息见 [rustc-dev-guide][subtree]。

[subtree]: https://rustc-dev-guide.rust-lang.org/external-repos.html#external-dependencies-subtree

## 修补 git-subtree 以支持大型仓库

目前 `git-subtree` 存在一个 bug，导致无法与 [`rust-lang/rust`] 仓库正常协作。有修复 PR，但已停滞。继续以下步骤前，需手动将修复应用到本地 `git-subtree` 副本。

可从[此处][gitgitgadget-pr]获取修补版 `git-subtree`。
将该文件放到 `/usr/lib/git-core`（备份原文件），并确保权限正确：

```bash
sudo cp --backup /path/to/patched/git-subtree.sh /usr/lib/git-core/git-subtree
sudo chmod --reference=/usr/lib/git-core/git-subtree~ /usr/lib/git-core/git-subtree
sudo chown --reference=/usr/lib/git-core/git-subtree~ /usr/lib/git-core/git-subtree
```

> _注意：_ 首次运行 `git subtree push` 需构建缓存。
> 这会遍历 Clippy 完整历史一次。为此需增大栈限制，可用 `ulimit -s
> 60000`。请在与调用 git subtree 相同的 shell 会话中运行 `ulimit`。

> _注意：_ 若你是 Debian 用户，脚本默认使用 `dash` 而非 `sh`。
> 该 shell 硬编码递归限制为 1,000。为使流程工作，需强制脚本使用 `bash`。
> 可编辑 `git-subtree` 脚本首行，将 `sh` 改为 `bash`。

> 注意：以下各节假设你已按[定义远程][defining remotes]说明配置远程。

[gitgitgadget-pr]: https://github.com/gitgitgadget/git/pull/493
[defining remotes]: release.md#定义远程

## 从 [`rust-lang/rust`] 同步到 Clippy

以下是同步流程的 TL;DR（以下命令均在 `rust` 目录内运行）：

1. 克隆 [`rust-lang/rust`] 仓库或确保其为最新。
2. 检出最新可用 nightly 对应的提交。可用 `rustup check` 获取。
3. 将 rust 副本中的 Clippy 变更同步到你的 Clippy fork：
    ```bash
    # 务必使用全新分支（如 `rustup`），或事先删除该分支
    # 因为变更无法快进，需重新运行此命令
    git subtree push -P src/tools/clippy clippy-local rustup
    ```

    > _注意：_ 多数时候需在 `rust-clippy` 仓库（非 rust 副本）创建 merge commit：
    ```bash
    git fetch upstream  # 假设 upstream 是 rust-lang/rust 远程
    git switch rustup
    git merge upstream/main --no-ff
    ```
    > 注意：这是 PR 中少数允许 merge commit 的情况之一。
4. 在 Clippy 仓库中提升 nightly 版本，运行：
   ```bash
   cargo dev sync update_nightly
   git commit -m "Bump nightly version -> YYYY-MM-DD" rust-toolchain.toml clippy_utils/README.md
   ```
5. 向 `rust-lang/rust-clippy` 开 PR 并等待合并（可在 PR 中 ping `@rust-lang/clippy` 团队，和/或在 [Zulip] 频道询问以加快流程。）

[Zulip]: https://rust-lang.zulipchat.com/#narrow/stream/clippy
[`rust-lang/rust`]: https://github.com/rust-lang/rust

## 从 Clippy 同步到 [`rust-lang/rust`]

以下命令均在 `rust` 目录内运行。

1. 确保已检出 `rust-lang/rust` 最新 `main`。
2. 将 `rust-lang/rust-clippy` master 同步到 rust 副本中的 Clippy：
    ```bash
    git switch -c clippy-subtree-update
    git subtree pull -P src/tools/clippy clippy-upstream master
    ```
3. 向 [`rust-lang/rust`] 开 PR
