+++
title = "02-回溯移植"
date = 2026-08-22T18:00:00+08:00
weight = 822
type = "docs"
description = "向稳定分支回溯"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Clippy Documentation](https://doc.rust-lang.org/nightly/clippy/)

# 回溯移植变更 {#backport}


> 原文链接: [https://doc.rust-lang.org/nightly/clippy/development/infrastructure/backport.html](https://doc.rust-lang.org/nightly/clippy/development/infrastructure/backport.html)


有时需要将变更回溯移植到 Clippy 的 beta 版本。
Clippy 的回溯移植很少见，需经 Clippy 团队批准。例如修复关键 ICE，或 lint 损坏到必须在进入 stable 前禁用时，会进行回溯移植。

> 注意：若认为某 PR 应回溯移植，可打上 `beta-nominated` 标签。须在发布前一周的周四之前完成。

## 筛选待回溯移植的 PR

首先用[此筛选器][beta-accepted-prs]查找所有已打标签的 PR。

然后逐个查看 PR。其中几项需要解释且较主观，需要良好判断。

1. **修复是否值得回溯移植？**

   这很主观。ICE 修复通常值得。将 lint 移到*更低*分组（从 warn 默认改为 allow 默认）通常也值得。单独的 FP 修复通常不值得（但若反正要做回溯移植，可一并包含 FP 修复）。若 PR 变更很多，须更谨慎考虑回溯移植。

2. **PR 修复的问题是否已在 `beta` 中？**

   PR 修复的问题可能尚未进入 Rust 仓库的 `beta` 分支。若如此且修复已同步到 Rust 仓库，则无需回溯移植，修复会与引入问题的提交一起进入 stable。若修复 PR 尚未同步，需将修复 PR「回溯移植」到 Rust `master`，或在下一轮回溯周期移植到 `beta`。

3. **确保修复已在 `master` 上再移植到 `beta`**

   修复必须已同步到 Rust `master` 分支，否则下一轮 `beta` 会再次缺失该修复。若尚未在 `master`，通常不应回溯移植。若回溯移植非常重要，先做周期外同步；但周期外同步应尽量小，因为其中变更会直接进入 `beta`，未经 `nightly` 测试。

[beta-accepted-prs]: https://github.com/rust-lang/rust-clippy/issues?q=label%3Abeta-nominated

## 准备工作

> 注意：本章所有命令在 Rust 克隆中运行。

按[定义远程][defining remotes]在 Rust 仓库中定义 `clippy-upstream` 远程。

然后拉取该远程：

```bash
git fetch clippy-upstream master
```

切换到 `beta` 分支：

```bash
git switch beta
git fetch upstream
git reset --hard upstream/beta
```

[defining remotes]: release.md#定义远程

## 回溯移植变更

PR 通过 GitHub merge queue 合并时，会以如下消息关闭：

> \<PR title\> (#\<PR number\>)

需要回溯移植该提交。找到该提交的 `<sha1>`，
在 **Rust 仓库**克隆中运行：

```bash
git cherry-pick -m 1 `<sha1>`
```

对所有应回溯移植的 PR 重复此操作。

## 在 Rust 仓库开 PR

接下来为回溯移植开 PR。确保 PR 指向 `beta` 分支而非 `master`。PR 描述应类似：

```
[beta] Clippy backports

r? @Mark-Simulacrum

Backports:
- <Link to the Clippy PR>
- ...

<Short summary of what is backported and why>
```

Mark 来自发布团队，须在分支新 `beta` 版本前合并该 PR。请 @ 他处理回溯移植。
然后列出所有回溯移植，并简短说明回溯内容与原因。

## 为已回溯移植的 PR 重新打标签

PR 回溯移植到 Rust `beta` 后，为该 PR 打上 `beta-accepted` 标签。
[编写 changelog] 时会收录这些 PR。

[writing the changelog]: changelog_update.md#4-包含-beta-accepted-pr
