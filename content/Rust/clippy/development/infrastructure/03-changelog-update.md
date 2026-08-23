+++
title = "03-更新变更日志"
date = 2026-08-22T18:00:00+08:00
weight = 823
type = "docs"
description = "维护 CHANGELOG"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Clippy Documentation](https://doc.rust-lang.org/nightly/clippy/)

# 更新变更日志 {#changelog-update}


> 原文链接: [https://doc.rust-lang.org/nightly/clippy/development/infrastructure/changelog_update.html](https://doc.rust-lang.org/nightly/clippy/development/infrastructure/changelog_update.html)


若要协助更新 [changelog]，你来对地方了。

## 何时更新

拼写错误等小修复/补充*始终*欢迎。

为新的 Rust 发布更新 changelog 时需特别小心。为此目的，理想情况下在即将发布的 stable 版发布前一周内更新 changelog。发布日期见 [Rust Forge][forge]。

多数时候我们只需为 Rust 小版本发布更新 changelog。
Clippy 变更纳入补丁发布的情况非常罕见。

## Changelog 更新 walkthrough

### 1. 找到相关 Clippy 提交

每次 Rust 发布都附带自己的 Clippy 版本。Clippy subtree 位于 Rust 仓库的 `tools` 目录。

根据当前时间与具体更新目标，以下要点可能有帮助：

* 撰写**即将发布的 stable 版**发布说明时，需检出当前 Rust `beta` 分支的 Clippy 提交。
  [链接][rust_beta_tools]
* 撰写**即将发布的 beta 版**发布说明时，需检出当前 Rust `main` 的 Clippy 提交。
  [链接][rust_main_tools]
* 撰写**过往 stable 版**（遗漏的）发布说明时，需检出该 stable 发布的 Rust 发布标签。
  [链接][rust_stable_tools]

通常你要写的是**即将发布的 stable 版** changelog。但请确认 Rust 仓库中 `beta` 已分支。

要找到提交哈希，在 `rust-lang/rust` 检出中（多数时候在 `upstream/beta` 分支）运行：
```
git log --oneline -- src/tools/clippy/ | grep -o "Merge commit '[a-f0-9]*' into .*" | head -1 | sed -e "s/Merge commit '\([a-f0-9]*\)' into .*/\1/g"
```

### 2. 获取这些提交之间的 PR

得到正确提交范围后，运行

```
util/fetch_prs_between.sh start_commit end_commit > changes.txt
```

其中 `end_commit` 是上一条命令的提交哈希，`start_commit`
是 [CHANGELOG 中当前 beta 小节][beta_section] 的提交哈希。
用你选择的编辑器打开 `changes.txt`。

### 3. 撰写最终 changelog

上述脚本应已将所有相关 PR 导出到你指定的文件，且已过滤大部分无关 PR，但建议手动清理并挑选有价值的 PR。
若对某些 PR 不确定，可保留待审阅并请反馈。

筛选 PR 后，将每个 PR 的 `changelog: ` 内容移到 `CHANGELOG.md`，按需调整措辞，但尽量保持连贯。

章节顺序大致为：

```
### New Lints
* Added [`LINT`] to `GROUP`

### Moves and Deprecations
* Moved [`LINT`] to `GROUP` (From `GROUP`, now LEVEL-by-default)
* Renamed `LINT` to [`LINT`]

### Enhancements
### False Positive Fixes
### ICE Fixes
### Documentation Improvements
### Others
```

请务必更新顶部的 [`Unreleased/Beta/In Rust Nightly` 小节][beta_section]，填入相关提交范围，并添加带发布日期与 PR 范围的 `Rust <version>` 小节。

### 4. 包含 `beta-accepted` PR

查找 [`beta-accepted`] 标签，确保 changelog 中也包含带该标签的 PR。若可以，在 changelog PR 合并**之后**移除 `beta-accepted` 标签。

> _注意：_ 其中部分 PR 甚至可能回溯移植到上一版 `beta`。
> 那些须纳入*上一版*发布的 changelog。

### 5. 更新 `clippy::version` 属性

接下来确保新增 lint 的 `#[clippy::version]` 属性包含正确版本。
要找到需要更新版本的 lint，浏览「New Lints」小节中的 lint，对每个 lint 名称运行：

```
grep -rB1 "pub $LINT_NAME" .
```

显示的版本应与撰写 changelog 的发布版本一致。否则将版本更新为 changelog 版本。

[changelog]: https://github.com/rust-lang/rust-clippy/blob/master/CHANGELOG.md
[forge]: https://forge.rust-lang.org/
[rust_main_tools]: https://github.com/rust-lang/rust/tree/HEAD/src/tools/clippy
[rust_beta_tools]: https://github.com/rust-lang/rust/tree/beta/src/tools/clippy
[rust_stable_tools]: https://github.com/rust-lang/rust/releases
[`beta-accepted`]: https://github.com/rust-lang/rust-clippy/issues?q=label%3Abeta-accepted+
[beta_section]: https://github.com/rust-lang/rust-clippy/blob/master/CHANGELOG.md#unreleased--beta--in-rust-nightly
