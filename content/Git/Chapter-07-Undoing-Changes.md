+++
title = "第7章：后悔药系列 —— Git 让你永不后悔"
weight = 70
date = 2026-04-03T19:36:48+08:00
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++
# 第7章：后悔药系列 —— Git 让你永不后悔

> 人非圣贤，孰能无过？写代码更是如此。好消息是，Git 提供了各种各样的"后悔药"，让你可以撤销几乎任何操作。坏消息是...药太多，容易吃错。本章就是 Git 后悔药使用说明书，请按医嘱服用。

---

## 7.1 改崩了代码？`git restore` 一键还原

你正在愉快地写代码，突然手一抖，删错了一大片，或者改得面目全非，想要回到之前的状态。这时候 `git restore` 就是你的救命稻草。

### `git restore` 是什么？

**`git restore`** 是 Git 2.23 版本引入的新命令，专门用来恢复文件。它取代了原来 `git checkout` 的一部分功能，职责更清晰。

### 恢复工作区的改动

```bash
# 恢复单个文件到上次提交的状态
#（丢弃工作区的所有改动）
git restore path/to/file.js

# 恢复多个文件
git restore file1.js file2.js

# 恢复整个目录
git restore src/

# 恢复所有文件（慎用！）
git restore .
```

**⚠️ 警告：** 这个操作会**永久丢失**工作区的改动，无法撤销！使用前请三思。

### 实际场景

**场景1：改了半天发现方向错了**
```bash
# 你在 src/feature.js 上改了半天，发现完全走偏了
# 一键恢复，从头再来
git restore src/feature.js
# 文件回到了上次 commit 的状态，你的改动全部消失
```

**场景2：误删了文件内容**
```bash
# 你不小心删光了 config.js 的内容并保存了
# 恢复它
git restore config.js
# 文件内容回来了！
```

### 恢复特定来源

```bash
# 从暂存区恢复（取消工作区的改动，保留暂存区）
git restore --staged --worktree path/to/file.js

# 从某个提交恢复
git restore --source=HEAD~3 path/to/file.js

# 从某个分支恢复
git restore --source=feature-branch path/to/file.js
```

### 安全模式：`--patch`

如果你不想全部恢复，只想恢复部分改动：

```bash
# 交互式选择要恢复的内容
git restore --patch path/to/file.js

# Git 会逐个显示改动块，问你：
# Apply this hunk [y,n,q,a,d,j,J,g,/,e,?]? 
# y = yes（恢复这个块）
# n = no（保留这个块）
# q = quit（退出）
# ? = help（查看帮助）
```

### 与 `git checkout` 的区别

| 功能 | 旧命令 | 新命令 |
|------|--------|--------|
| 恢复文件 | `git checkout -- file` | `git restore file` |
| 切换分支 | `git checkout branch` | `git switch branch` |
| 创建并切换分支 | `git checkout -b branch` | `git switch -c branch` |

Git 2.23+ 推荐使用 `git restore` 和 `git switch`，职责更清晰。

---

## 7.2 暂存区加错东西？`git restore --staged` 救命

你执行了 `git add`，突然发现有不该提交的文件被加进去了，或者某个文件加错了版本。这时候需要把文件从暂存区"撤下来"。

### 从暂存区移除文件

```bash
# 将文件从暂存区移除，但保留工作区的改动
git restore --staged path/to/file.js

# 移除多个文件
git restore --staged file1.js file2.js

# 移除所有文件
git restore --staged .
```

### 发生了什么？

```
执行前：
工作区：修改后的文件
暂存区：修改后的文件（已 git add）
仓库：上次提交的文件

执行 git restore --staged 后：
工作区：修改后的文件（保留）
暂存区：上次提交的文件（恢复）
仓库：上次提交的文件
```

### 实际场景

**场景1：不小心把配置文件加进去了**
```bash
# 你修改了 config.js，但里面包含敏感信息
# 不小心执行了 git add config.js

# 从暂存区移除
git restore --staged config.js

# 现在 config.js 还在工作区，但不在暂存区了
# 你可以把它加到 .gitignore，或者恢复工作区的改动
git restore config.js  # 如果你也想丢弃工作区的改动
```

**场景2：想拆分提交**
```bash
# 你修改了 3 个文件，但想分成两次提交
# 不小心一次性都 add 了

git add .

# 把其中一个文件从暂存区移除
git restore --staged file3.js

# 现在暂存区只有 file1.js 和 file2.js
git commit -m "feat: 添加功能 A"

# 再提交 file3.js
git add file3.js
git commit -m "feat: 添加功能 B"
```

### 对比 `git rm --cached`

| 命令 | 效果 |
|------|------|
| `git restore --staged file` | 文件从暂存区移除，但 Git 继续跟踪这个文件 |
| `git rm --cached file` | 文件从暂存区移除，Git 不再跟踪这个文件（相当于删除） |

如果你只是想"撤下"文件，用 `git restore --staged`；如果你想让 Git 完全不再跟踪这个文件，用 `git rm --cached`。

---

## 7.3 提交错了？三种 `git reset` 模式详解

你已经 `git commit` 了，但突然发现有文件忘加了、提交信息写错了，或者干脆这次提交就不该存在。这时候 `git reset` 出场了。

### `git reset` 是做什么的？

**`git reset`** 用于移动 HEAD 和当前分支的指针，同时可以选择性地影响暂存区和工作区。它有三种模式，威力从弱到强。

### 三种模式对比

```
┌─────────────────────────────────────────────────────────────┐
│                     git reset 三种模式                      │
├──────────────┬──────────────┬──────────────┬────────────────┤
│     模式     │    HEAD      │   暂存区     │    工作区      │
├──────────────┼──────────────┼──────────────┼────────────────┤
│ --soft       │    移动      │    保留      │    保留        │
│ --mixed      │    移动      │    重置      │    保留        │
│ --hard       │    移动      │    重置      │    重置        │
└──────────────┴──────────────┴──────────────┴────────────────┘
```

### 模式1：`--soft`（最温和）

```bash
# 撤销提交，但保留改动在暂存区
git reset --soft HEAD~1
```

**效果：**
- HEAD 移动到上一个提交
- 暂存区保留你刚才提交的改动
- 工作区完全不变

**使用场景：** 提交信息写错了，想重新提交

```bash
# 刚才的提交信息写错了
git commit -m "fix: 修复了 bug"
# 突然想起来，应该写 "fix: 修复登录失败的 bug"

# 撤销提交，但保留改动
git reset --soft HEAD~1

# 重新提交
git commit -m "fix: 修复登录失败的 bug"
```

### 模式2：`--mixed`（默认，中等）

```bash
# 撤销提交，改动退回到工作区
git reset --mixed HEAD~1
# 或者简写（--mixed 是默认模式）
git reset HEAD~1
```

**效果：**
- HEAD 移动到上一个提交
- 暂存区清空（改动从暂存区移除）
- 工作区保留改动

**使用场景：** 提交后发现漏了文件，想重新整理

```bash
# 提交后发现漏了 utils.js
git commit -m "feat: 添加新功能"

# 撤销提交，改动回到工作区
git reset HEAD~1

# 现在所有改动都在工作区，重新 add
git add src/feature.js utils.js
git commit -m "feat: 添加新功能（包含工具函数）"
```

### 模式3：`--hard`（最危险）

```bash
# 彻底撤销提交，所有改动消失
git reset --hard HEAD~1
```

**效果：**
- HEAD 移动到上一个提交
- 暂存区清空
- 工作区重置（所有未提交的改动**永久丢失**）

**⚠️ 警告：** 这是核武器级别操作，一旦执行，无法撤销！除非你之前用 `git stash` 保存过，或者有其他备份。

**使用场景：** 你真的确定这次提交完全错了，不想要任何改动

```bash
# 你提交了一堆实验性的代码，现在决定不要了
git commit -m "WIP: 实验性功能"

# 彻底删除这次提交和所有改动
git reset --hard HEAD~1

# 世界清净了，就像什么都没发生过
```

### 回到特定提交

```bash
# 回到某个特定的提交
git reset --hard a1b2c3d

# 回到某个标签
git reset --hard v1.0.0

# 回到某个分支的最新提交
git reset --hard feature-branch
```

---

## 7.4 `--soft`、`--mixed`、`--hard`：选错模式后果很严重

上一节介绍了三种模式，这一节我们来深入对比，确保你不会吃错药。

### 三种模式图解

假设你有以下状态：

```
提交历史：A --- B --- C (HEAD)

工作区：修改了 file1.js 和 file2.js
暂存区：file1.js 已 add，file2.js 未 add
```

#### 执行 `git reset --soft HEAD~1` 后：

```
提交历史：A --- B (HEAD)

工作区：file1.js 和 file2.js 都还在
暂存区：file1.js（之前提交的改动 + 新的改动都在暂存区）
```

**改动去向：** 提交被撤销，但所有改动都保留在暂存区，可以直接重新提交。

#### 执行 `git reset --mixed HEAD~1` 后：

```
提交历史：A --- B (HEAD)

工作区：file1.js 和 file2.js 都还在
暂存区：空的（file1.js 被退回到工作区）
```

**改动去向：** 提交被撤销，改动退回到工作区，需要重新 add。

#### 执行 `git reset --hard HEAD~1` 后：

```
提交历史：A --- B (HEAD)

工作区：空的（file1.js 和 file2.js 的改动全部消失）
暂存区：空的
```

**改动去向：** 提交被撤销，所有改动永久丢失。

### 选择指南

| 场景 | 推荐模式 | 原因 |
|------|----------|------|
| 提交信息写错了 | `--soft` | 直接重新提交，不用重新 add |
| 漏了文件，想重新整理 | `--mixed` | 改动回工作区，重新选择要 add 的文件 |
| 实验性代码，完全不要了 | `--hard` | 彻底清理，不留痕迹 |
| 回退到某个稳定版本 | `--hard` | 完全回到那个版本的状态 |

### 安全建议

**1. 不确定时，先用 `--mixed`**
```bash
# 如果不确定要不要保留改动，先用 --mixed
git reset --mixed HEAD~1

# 如果发现还需要某些改动，可以重新 add
# 如果确实都不需要，再执行 --hard
git reset --hard HEAD
```

**2. 重要改动先用 `git stash` 备份**
```bash
# 提交前，如果改动很重要，先 stash 一下
git stash push -m "备份：实验性功能"

# 然后放心地 reset
git reset --hard HEAD~1

# 如果后悔了，可以恢复
git stash pop
```

**3. 使用 `git reflog` 作为后悔药**
```bash
# 即使执行了 reset --hard，也可以用 reflog 找回
git reflog
# 找到 reset 之前的提交哈希
git reset --hard a1b2c3d  # 回到那个提交
```

### 常见错误

**错误1：用了 `--hard` 发现还有文件需要**
```bash
# 完蛋，执行了 --hard，但发现还有文件需要
# 解决方案：用 reflog 找回
git reflog
# 找到执行 reset --hard 之前的提交
git reset --hard HEAD@{1}
```

**错误2：想撤销 `git add`，却用了 `git reset --hard`**
```bash
# 错误：想从暂存区移除文件，结果用了 --hard
# 工作区的改动也没了！

# 正确做法：
git restore --staged file.js  # 从暂存区移除
git restore file.js          # 如果要丢弃工作区的改动
```

**错误3：在公共分支上 `git reset`**
```bash
# 你在 main 分支上 reset 了已经 push 的提交
# 这会改变历史，导致团队成员困惑

# 解决方案：用 git revert 代替（见下一节）
```

---

## 7.5 已推送的提交怎么撤销？`git revert` 安全方案

你已经 `git push` 了，突然发现提交有问题。这时候不能用 `git reset`，因为会改变历史，让队友抓狂。这时候 `git revert` 是安全的选择。

### `git revert` 是什么？

**`git revert`** 用于撤销某次提交的改动，但它不会删除那次提交，而是创建一个新的提交，这个提交的内容正好"抵消"原来的改动。

### 为什么用 `revert` 而不是 `reset`？

```
场景：你已经 push 到了远程仓库

用 git reset：
本地：A --- B --- C (HEAD)
远程：A --- B --- C

执行 git reset --hard B 后：
本地：A --- B (HEAD)
远程：A --- B --- C

下次 push 时：
! [rejected]        main -> main (non-fast-forward)
# 拒绝推送，因为远程有 C，而本地没有

用 git revert：
本地：A --- B --- C --- D (HEAD)
                     ↑
                     D 是 C 的反向提交

推送后：
本地：A --- B --- C --- D
远程：A --- B --- C --- D
# 完美同步，历史完整保留
```

### 基本用法

```bash
# 撤销某次提交
git revert a1b2c3d

# 撤销最近的提交
git revert HEAD

# 撤销前两次提交（分别创建两个 revert 提交）
git revert HEAD~2..HEAD

# 撤销但不自动提交（手动处理）
git revert --no-commit HEAD
```

### 实际场景

**场景1：撤销已 push 的 Bug 提交**
```bash
# 你发现提交 a1b2c3d 引入了 Bug，已经 push 到远程

# 安全地撤销
git revert a1b2c3d

# 编辑器会打开，让你编辑 revert 的提交信息
# 保存后，Git 会创建一个新的提交

# 推送到远程
git push origin main
```

**场景2：撤销合并提交**
```bash
# 撤销一个合并提交需要指定父分支
# 通常 -m 1 表示保留 main 分支的改动，撤销 feature 分支的改动
git revert -m 1 a1b2c3d
```

**场景3：批量撤销多个提交**
```bash
# 撤销最近 3 个提交（创建 3 个 revert 提交）
git revert HEAD~3..HEAD

# 或者合并成一个提交
git revert --no-commit HEAD~3..HEAD
git commit -m "revert: 撤销最近 3 个实验性提交"
```

### 处理冲突

如果被撤销的提交之后还有其他提交修改了相同的文件，可能会产生冲突：

```bash
# revert 时遇到冲突
git revert a1b2c3d
# Auto-merging src/feature.js
# CONFLICT (content): Merge conflict in src/feature.js
# error: could not revert a1b2c3d... 添加新功能
# hint: after resolving the conflicts, mark them with
# hint: "git add/rm <pathspec>", then run
# hint: "git revert --continue"
# hint: you can abort the revert with
# hint: "git revert --abort"

# 解决冲突后
git add src/feature.js
git revert --continue
```

### `revert` vs `reset` 对比

| 特性 | `git revert` | `git reset` |
|------|--------------|-------------|
| 是否改变历史 | 否（添加新提交） | 是（删除提交） |
| 是否安全用于已 push 的提交 | 是 | 否 |
| 是否需要 force push | 否 | 是 |
| 队友是否会困惑 | 不会 | 会 |
| 适用场景 | 公共分支 | 本地分支 |

### 选择建议

- **本地分支，未 push**：用 `git reset`，更干净
- **公共分支，已 push**：用 `git revert`，更安全
- **不确定是否已 push**：用 `git revert`，不会错

---

## 7.6 彻底搞砸了？`git reflog` 救命稻草

你已经 `git reset --hard` 了，或者执行了其他危险操作，发现重要的提交不见了。别慌，`git reflog` 是你的救命稻草。

### 什么是 `reflog`？

**`reflog`**（Reference Log，引用日志）是 Git 的"黑匣子"，它记录了 HEAD 和分支引用的每一次变动。无论你做了什么操作，reflog 都默默记下来了。

### reflog 能救什么？

- ✅ 被 `git reset --hard` 删除的提交
- ✅ 被 `git rebase` 改写的提交
- ✅ 被删除的分支
- ✅ 被 `git commit --amend` 覆盖的提交
- ✅ 被 `git stash drop` 删除的 stash

### 基本用法

```bash
# 查看 HEAD 的变动历史
git reflog

# 查看某个分支的变动历史
git reflog show main

# 查看相对时间
git reflog --date=relative
```

### 输出格式解析

```
a1b2c3d (HEAD -> main) HEAD@{0}: commit: 修复登录 bug
b2c3d4e HEAD@{1}: reset: moving to HEAD~1
c3d4e5f HEAD@{2}: commit: WIP: 实验性功能
d4e5f6g HEAD@{3}: checkout: moving from feature-x to main
e5f6g7h HEAD@{4}: commit: 添加功能 X
```

**各列含义：**
- `a1b2c3d`：那次操作后的提交哈希
- `HEAD@{0}`：引用日志的索引，0 表示最近一次
- `commit:` / `reset:` / `checkout:`：操作类型
- 最后的文字：提交信息或操作说明

### 实战：找回被 reset 的提交

```bash
# 1. 查看 reflog，找到 reset 之前的提交
git reflog
# 输出：
# b2c3d4e HEAD@{0}: reset: moving to HEAD~1
# c3d4e5f HEAD@{1}: commit: WIP: 实验性功能  ← 这就是我们要找的

# 2. 确认这就是你要找的提交
git show c3d4e5f

# 3. 恢复这个提交
git reset --hard c3d4e5f

# 或者，如果你想保留当前状态，创建一个分支
git checkout -b recovered-work c3d4e5f
```

### 实战：找回被删除的分支

```bash
# 你不小心删除了 feature-x 分支

# 1. 在 reflog 中找 feature-x 的最后一次提交
git reflog
# 输出：
# d4e5f6g HEAD@{3}: checkout: moving from feature-x to main
# e5f6g7h HEAD@{4}: commit: 添加功能 X  ← feature-x 的最后一次提交

# 2. 恢复分支
git checkout -b feature-x e5f6g7h

# feature-x 分支复活了！
```

### 实战：找回被 drop 的 stash

```bash
# 你不小心执行了 git stash drop

# 1. 查看 stash 的 reflog
git reflog show stash

# 2. 恢复 stash
git stash store a1b2c3d -m "恢复的 stash"

# 或者直接用那个提交创建分支
git checkout -b recovered-stash a1b2c3d
```

### reflog 的保存期限

reflog 不是永久保存的：
- 默认保存 90 天（对于可达的提交）
- 默认保存 30 天（对于不可达的提交）

```bash
# 查看 reflog 过期时间配置
git config gc.reflogExpire

# 修改过期时间（不推荐，除非你知道在做什么）
git config gc.reflogExpire "180 days"
```

### 注意事项

1. **reflog 是本地的**：它只记录你本地仓库的操作，不会同步到远程
2. **reflog 会过期**：默认 90 天后旧的记录会被清理
3. **克隆的仓库没有原仓库的 reflog**：如果你克隆了一个仓库，新仓库的 reflog 是空的

---

## 7.7 误删文件恢复：从绝望到希望

你不小心用 `rm` 删除了文件，或者用 `git rm` 删除了文件并提交了。怎么恢复？

### 场景1：只删除了文件，未提交

```bash
# 你不小心 rm 了重要文件
rm important.js

# 文件还在工作区，用 restore 恢复
git restore important.js

# 如果文件已经被 git add 过，也可以用 checkout
git checkout -- important.js
```

### 场景2：删除了文件并 git add

```bash
# 你执行了 git rm 或 rm + git add
git rm important.js

# 文件在暂存区标记为删除，但还没 commit
# 从暂存区移除删除标记
git restore --staged important.js

# 恢复文件内容
git restore important.js
```

### 场景3：删除了文件并 commit

```bash
# 你已经提交了删除操作
git rm important.js
git commit -m "删除 important.js"

# 方案1：用 revert 撤销删除提交
git revert HEAD

# 方案2：从之前的提交恢复文件
git checkout HEAD~1 -- important.js
git commit -m "恢复 important.js"
```

### 场景4：彻底删除了文件（包括历史）

```bash
# 你执行了 git filter-branch 或 git filter-repo 彻底删除了文件
# 这种情况比较复杂...

# 如果你有其他备份（比如其他克隆的仓库、CI/CD 缓存等），从备份恢复

# 如果没有备份... 祈祷吧 🙏
# 下次记得：重要文件要多重备份！
```

### 预防胜于治疗

```bash
# 1. 使用 trash 命令代替 rm（可恢复）
trash file.js  # 而不是 rm file.js

# 2. 删除前确认
git status  # 看看会删除什么

# 3. 重要操作前创建分支
git checkout -b backup-before-dangerous-operation

# 4. 定期 push 到远程
# 即使本地彻底删除，远程还有备份
```

---

## 7.8 后悔药使用指南：什么情况下用什么药

Git 提供了这么多"后悔药"，到底什么时候用哪个？这一节给你一张速查表。

### 后悔药速查表

| 症状 | 诊断 | 药方 | 命令 |
|------|------|------|------|
| 改崩了工作区的代码 | 工作区乱了 | `git restore` | `git restore file.js` |
| 不小心 git add 了文件 | 暂存区有误 | `git restore --staged` | `git restore --staged file.js` |
| 提交信息写错了 | 刚 commit 发现错 | `git commit --amend` | `git commit --amend` |
| 漏了文件没提交 | 刚 commit 发现漏 | `git reset --soft` | `git reset --soft HEAD~1` |
| 这次提交完全错了 | 本地未 push | `git reset --mixed` | `git reset HEAD~1` |
| 这次提交完全不要了 | 本地未 push | `git reset --hard` | `git reset --hard HEAD~1` |
| 已 push 的提交有问题 | 已 push | `git revert` | `git revert HEAD` |
| 彻底搞砸了 | 各种情况 | `git reflog` | `git reflog` |
| 误删了文件 | 文件没了 | `git restore` / `git checkout` | `git restore file.js` |

### 决策流程图

```
发现问题
   ↓
是否已经 commit？
   ├── 否 → 是否 git add？
   │          ├── 否 → git restore file.js
   │          └── 是 → git restore --staged file.js
   │
   └── 是 → 是否已 push？
              ├── 否 → 是否想保留改动？
              │          ├── 是 → git reset --soft HEAD~1
              │          └── 否 → git reset --hard HEAD~1
              │
              └── 是 → git revert HEAD
```

### 安全操作原则

**1. 不确定时，先备份**
```bash
# 重要改动前先 stash
git stash push -m "备份"

# 或者创建分支
git checkout -b backup
```

**2. 先用 `--mixed` 试探**
```bash
# 不确定要不要保留改动时
git reset --mixed HEAD~1

# 这样改动还在工作区，可以检查
# 确定不要了再执行 --hard
```

**3. 公共分支用 `revert`**
```bash
# 在 main、develop 等公共分支上
# 永远用 revert 代替 reset
git revert HEAD
```

**4. 定期 push**
```bash
# 经常 push 到远程
# 即使本地彻底删除，远程还有备份
git push origin main
```

---

## 7.9 安全操作原则：操作前备份，操作后验证

Git 的后悔药虽然强大，但最好的策略是不让自己陷入需要后悔的境地。这一节总结一些安全操作原则。

### 原则1：操作前备份

```bash
# 重要改动前，先 stash
git stash push -m "WIP: 重构前的备份"

# 或者创建备份分支
git branch backup-before-refactor

# 或者 push 到远程
git push origin feature-branch
```

### 原则2：使用 `--patch` 模式

```bash
# 恢复前，先看看要恢复什么
git restore --patch file.js

# 提交前，再确认一下要提交什么
git add --patch file.js
```

### 原则3：小步提交

```bash
# 不要积累大量改动再提交
# 小步提交，即使出问题也容易恢复

# 不好：
git add .
git commit -m "做了很多改动"

# 好：
git add src/feature.js
git commit -m "feat: 添加用户登录功能"

git add tests/
git commit -m "test: 添加登录功能测试"
```

### 原则4：验证后再 push

```bash
# commit 后，先验证
git log --oneline -3  # 看看提交历史
git show HEAD         # 看看最后一次提交的内容

# 确认无误后再 push
git push origin main
```

### 原则5：了解你的操作

```bash
# 不确定命令的作用？先查文档
git reset --help

# 或者用 --dry-run（如果支持）
# 虽然 git reset 不支持 --dry-run，但你可以：
git log HEAD~3..HEAD  # 看看会丢失什么提交
```

### 原则6：团队协作规范

```bash
# 个人分支：随意 reset/rebase
# 公共分支：只用 revert

# 强制 push 前，通知团队
# 使用 --force-with-lease 代替 --force
git push --force-with-lease origin main
```

### 原则7：定期清理和检查

```bash
# 定期查看 reflog，了解最近的操作
git reflog --date=relative

# 定期运行 fsck 检查仓库健康
git fsck

# 定期备份重要仓库
# 可以 push 到多个远程，或者打包备份
git bundle create backup.bundle --all
```

---

## 本章小结

本章我们学习了 Git 的各种"后悔药"：

| 命令 | 用途 | 威力 | 危险性 |
|------|------|------|--------|
| `git restore` | 恢复工作区文件 | ⭐⭐ | 低 |
| `git restore --staged` | 从暂存区移除 | ⭐⭐ | 低 |
| `git reset --soft` | 撤销提交，保留暂存区 | ⭐⭐⭐ | 中 |
| `git reset --mixed` | 撤销提交，改动回工作区 | ⭐⭐⭐ | 中 |
| `git reset --hard` | 彻底撤销提交和改动 | ⭐⭐⭐⭐⭐ | 高 |
| `git revert` | 安全撤销已 push 的提交 | ⭐⭐⭐ | 低 |
| `git reflog` | 找回丢失的提交 | ⭐⭐⭐⭐⭐ | 低 |

**关键要点：**
1. `git restore` 用于恢复工作区和暂存区的文件
2. `git reset` 有三种模式，威力递增：`--soft` < `--mixed` < `--hard`
3. 已 push 的提交用 `git revert`，不要改变公共历史
4. `git reflog` 是最后的救命稻草，能找回几乎所有丢失的提交
5. 安全原则：操作前备份，操作后验证

**记忆口诀：**
- 工作区乱了 → `restore`
- 暂存区错了 → `restore --staged`
- 刚 commit 想改 → `reset --soft`
- 本地彻底不要 → `reset --hard`
- 已 push 要撤销 → `revert`
- 彻底搞砸了 → `reflog`

**练习建议：**
1. 创建一个测试仓库，练习各种 reset 模式
2. 故意"丢失"一个提交，然后用 reflog 找回
3. 在测试分支上练习 revert 和解决冲突

下一章，我们将学习 `.gitignore`——让不该提交的文件眼不见心不烦！
