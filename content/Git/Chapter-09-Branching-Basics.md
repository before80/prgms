+++
title = "第9章：分支基础 —— Git 的杀手锏"
weight = 90
date = 2026-04-03T19:36:48+08:00
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++
# 第9章：分支基础 —— Git 的杀手锏

> 如果 Git 只有一个功能值得炫耀，那一定是分支。其他版本控制系统（如 SVN）的分支又慢又重，而 Git 的分支轻如鸿毛、快如闪电。这一章，我们来揭开 Git 分支的神秘面纱。

---

## 9.1 什么是分支？代码的平行宇宙

想象一下：你正在写代码，突然需要同时做两件事——修复一个紧急 Bug，同时开发一个新功能。怎么办？复制整个项目到另一个文件夹？太笨了！Git 分支就是解决方案。

### 分支的比喻

**比喻1：平行宇宙**
- 主宇宙（main 分支）：稳定运行的代码
- 平行宇宙 A（feature 分支）：开发新功能
- 平行宇宙 B（hotfix 分支）：修复紧急 Bug
- 每个宇宙独立发展，互不干扰

**比喻2：游戏存档**
- main 分支：主存档
- feature 分支：尝试新玩法的存档
- 随时可以切换回主存档
- 新玩法成功了，可以合并回主存档

**比喻3：树枝**
- 主干（main）：树的 trunk
- 分支：从主干分出的树枝
- 树枝可以独立生长
- 最终可以合并回主干

### 分支的本质

Git 的分支本质上是一个**指向提交的指针**。创建分支就是创建一个指向当前提交的指针，切换分支就是移动 HEAD 指针。

```
创建分支前：

A --- B --- C (HEAD -> main)

创建 feature 分支后：

A --- B --- C (HEAD -> main, feature)

在 feature 分支上提交 D 后：

A --- B --- C (main)
      \
       D (HEAD -> feature)

切换回 main，提交 E 后：

A --- B --- C --- E (HEAD -> main)
      \
       D (feature)
```

---

## 9.2 为什么需要分支？老板突然让你修 Bug 怎么办

没有分支的世界：
- 你在写新功能，代码改了一半
- 老板突然说："线上出 Bug 了，马上修复！"
- 你："等我先把这堆代码注释掉..."
- 修复完 Bug，再取消注释，继续写功能
- 一团糟！

有分支的世界：
- 你在 feature 分支写新功能
- 老板："线上出 Bug 了！"
- 你：`git switch main`，`git switch -c hotfix`
- 修复 Bug，合并，部署
- 切回 feature 分支，继续写功能
- 井井有条！

### 分支的典型使用场景

**场景1：功能开发**
```bash
# 每个功能一个分支
feature/user-login
feature/payment
feature/dashboard
```

**场景2：Bug 修复**
```bash
# 紧急修复
hotfix/critical-bug

# 普通修复
fix/login-error
```

**场景3：版本发布**
```bash
# 准备发布
release/v1.0.0
release/v1.1.0
```

**场景4：实验性代码**
```bash
# 尝试新想法
experiment/new-algorithm
experiment/refactor
```

**场景5：代码审查**
```bash
# 审查时创建的分支
review/fix-memory-leak
```

### 分支的好处

1. **隔离开发**：不同功能互不影响
2. **并行工作**：多人同时开发不同功能
3. **安全实验**：尝试新想法，失败了直接删除分支
4. **版本管理**：维护多个版本
5. **代码审查**：通过 Pull Request 审查代码

---

## 9.3 分支的本质：只是一个 41 字节的指针

Git 的分支为什么这么快？因为它本质上只是一个文件，里面存着一个 40 字符的 SHA-1 哈希值。

### 分支的物理存储

```bash
# 查看分支文件
ls .git/refs/heads/
# 输出：main feature hotfix

# 查看分支内容
cat .git/refs/heads/main
# 输出：a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9

# 查看文件大小
ls -la .git/refs/heads/main
# 输出：41 字节（40 字符 + 换行符）
```

### 创建分支有多快？

```bash
# 创建分支只需写入 41 字节
# 时间复杂度：O(1)
# 实际时间：< 1 毫秒

git branch new-feature
# 瞬间完成！

# 对比 SVN：
# SVN 创建分支需要复制整个目录
# 时间复杂度：O(n)，n 是文件数量
# 实际时间：几秒到几分钟
```

### 分支 vs 提交

```bash
# 提交（commit）包含完整信息
# - 作者、时间、提交信息
# - 父提交指针
# - 文件树快照
# 大小：几百字节到几 MB

# 分支（branch）只包含一个指针
# - 指向某个提交
# 大小：41 字节
```

### 分支的存储结构

```
.git/
├── refs/
│   └── heads/
│       ├── main          # 内容：a1b2c3d...
│       ├── feature       # 内容：b2c3d4e...
│       └── hotfix        # 内容：c3d4e5f...
├── HEAD                  # 内容：ref: refs/heads/main
└── ...
```

### 为什么这么快？

1. **创建分支**：写入 41 字节
2. **切换分支**：更新 HEAD 文件
3. **合并分支**：找到共同祖先，应用差异

都是 O(1) 或 O(n) 操作，n 是差异的文件数，不是总文件数。

---

## 9.4 HEAD 是什么？当前位置的指南针

HEAD 是 Git 中最重要的概念之一，它指向你当前所在的位置。

### HEAD 的本质

HEAD 是一个**指向当前分支的指针**（或者指向某个具体的提交）。

```bash
# 查看 HEAD
cat .git/HEAD
# 输出：ref: refs/heads/main

# 这意味着 HEAD 指向 main 分支
# main 分支又指向某个提交
```

### HEAD 的两种状态

**状态1：指向分支（正常状态）**
```
HEAD -> main -> a1b2c3d
```

```bash
# 查看当前分支
git branch --show-current
# 输出：main
```

**状态2：指向具体提交（分离 HEAD 状态）**
```
HEAD -> a1b2c3d
```

```bash
# 切换到某个提交
git checkout a1b2c3d

# 查看 HEAD
cat .git/HEAD
# 输出：a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9

# 警告：你处于分离 HEAD 状态
```

### 分离 HEAD 状态

```bash
# 进入分离 HEAD 状态
git checkout a1b2c3d

# 在这个状态下提交
git commit -m "实验性改动"

# 新提交没有分支指向它！
# 如果切换回 main，这个提交就"丢失"了
# 需要用 git reflog 找回

# 解决方案：创建一个分支
git checkout -b experiment
```

### HEAD 的相对引用

```bash
# HEAD 的父提交
git show HEAD~1

# HEAD 的祖父提交
git show HEAD~2

# HEAD 的第一个父提交（用于合并提交）
git show HEAD^1

# HEAD 的第二个父提交（用于合并提交）
git show HEAD^2

# 组合使用
git show HEAD~2^2  # 祖父的第二个父提交
```

### 实际应用

```bash
# 撤销最后一次提交（保留改动）
git reset --soft HEAD~1

# 查看上次提交改了什么
git show HEAD

# 比较上次提交和这次提交的差异
git diff HEAD~1 HEAD

# 回到上次提交的状态
git checkout HEAD~1
```

---

## 9.5 创建分支：`git branch` vs `git switch -c`

创建分支有两种方式，老派和新派，效果一样，但新派更清晰。

### 老派：`git branch`

```bash
# 创建分支
git branch feature-x

# 注意：创建后不会自动切换
git branch
# * main      # 当前还在 main
#   feature-x # 新分支已创建

# 需要手动切换
git checkout feature-x
```

### 新派：`git switch -c`

Git 2.23 引入的新命令，职责更清晰：

```bash
# 创建并切换分支
git switch -c feature-x

# -c 是 --create 的缩写

# 查看当前分支
git branch
#   main
# * feature-x  # 已经切换过来了
```

### 对比

| 操作 | 老派 | 新派 |
|------|------|------|
| 创建分支 | `git branch name` | `git switch -c name` |
| 创建并切换 | `git checkout -b name` | `git switch -c name` |
| 切换分支 | `git checkout name` | `git switch name` |

### 基于特定提交创建分支

```bash
# 基于某个提交创建分支
git branch feature-x a1b2c3d

# 基于某个标签创建分支
git branch release-v1.0 v1.0.0

# 基于远程分支创建分支
git branch feature-x origin/feature-x
```

### 创建空分支（无历史）

```bash
# 创建一个没有提交历史的分支
git checkout --orphan empty-branch

# 删除所有文件
git rm -rf .

# 添加新文件
git add README.md
git commit -m "Initial commit"

# 这个分支没有历史，适合发布文档等场景
```

---

## 9.6 切换分支：`git switch` 与 `git checkout` 的爱恨情仇

切换分支是日常操作，但 Git 提供了多种方式，容易让人困惑。

### 老派：`git checkout`

```bash
# 切换分支
git checkout feature-x

# 创建并切换
git checkout -b feature-y

# 切换到远程分支
git checkout -b feature-x origin/feature-x
# 或者简写
git checkout --track origin/feature-x
```

### 新派：`git switch`

```bash
# 切换分支
git switch feature-x

# 创建并切换
git switch -c feature-y

# 切换到远程分支
git switch -c feature-x origin/feature-x
# 或者
git switch --track origin/feature-x
```

### 为什么推荐 `git switch`？

`git checkout` 功能太多，职责不清：
- 切换分支：`git checkout branch`
- 恢复文件：`git checkout -- file`
- 创建分支：`git checkout -b branch`

`git switch` 只做一件事：切换分支。更清晰，更安全。

### 切换分支时的冲突

```bash
# 如果工作区有未提交的改动，与目标分支冲突
git switch feature-x
# error: Your local changes to the following files would be overwritten by checkout:
#         src/main.js
# Please commit your changes or stash them before you switch branches.

# 解决方案1：提交改动
git add .
git commit -m "WIP: 临时提交"
git switch feature-x

# 解决方案2：暂存改动
git stash push -m "切换分支前的改动"
git switch feature-x

# 解决方案3：强制切换（会丢失改动！）
git switch -f feature-x  # 危险！
```

### 切换到远程分支

```bash
# 获取远程分支列表
git fetch origin

# 查看远程分支
git branch -r

# 切换到远程分支（创建本地跟踪分支）
git switch -c feature-x origin/feature-x

# 或者简写
git switch --track origin/feature-x
```

---

## 9.7 切换分支前的注意事项：未提交修改怎么办？

切换分支前，Git 会检查工作区和暂存区。如果有未提交的改动，可能会阻止切换。

### Git 的检查逻辑

```bash
# 情况1：改动与目标分支不冲突
# 文件 A 在工作区修改了
# 目标分支的文件 A 与当前分支相同
# 结果：可以切换，改动会保留

git switch feature-x
# 成功，改动还在

# 情况2：改动与目标分支冲突
# 文件 A 在工作区修改了
# 目标分支的文件 A 与当前分支不同
# 结果：阻止切换，要求处理

git switch feature-x
# error: 无法切换
```

### 处理未提交改动的 4 种方法

**方法1：提交改动**
```bash
# 如果改动已经完成
git add .
git commit -m "feat: 完成功能 X"
git switch feature-x
```

**方法2：暂存改动（推荐）**
```bash
# 如果改动还没完成
git stash push -m "功能 X 进行中"
git switch feature-x

# 处理完其他事情后，切回来
git switch main
git stash pop  # 恢复改动
```

**方法3：放弃改动**
```bash
# 如果改动不重要
git restore .
git switch feature-x
```

**方法4：强制切换（危险）**
```bash
# 会丢失未提交的改动！
git switch -f feature-x
```

### `git stash` 详解

```bash
# 暂存当前改动
git stash push -m "描述信息"

# 查看 stash 列表
git stash list
# stash@{0}: On main: 描述信息
# stash@{1}: On feature-x: 另一个描述

# 恢复最近的 stash
git stash pop

# 恢复指定的 stash
git stash pop stash@{1}

# 应用但不删除 stash
git stash apply

# 删除 stash
git stash drop stash@{0}

# 清空所有 stash
git stash clear
```

---

## 9.8 查看所有分支：`git branch -a`、`-r`、`-vv`

管理分支的前提是先知道有哪些分支。

### 查看本地分支

```bash
# 查看本地分支
git branch

# 带详细信息
git branch -v

# 带上游分支信息
git branch -vv
```

输出示例：
```
  feature-x                a1b2c3d 添加功能 X
  feature-y                b2c3d4e 添加功能 Y
* main                     c3d4e5f [origin/main] 修复 Bug
  experiment               d4e5f6g 实验性改动
```

### 查看远程分支

```bash
# 查看远程分支
git branch -r

# 输出示例：
# origin/main
# origin/feature-x
# origin/hotfix-login
```

### 查看所有分支（本地 + 远程）

```bash
# 查看所有分支
git branch -a

# 输出示例：
#   feature-x
#   feature-y
# * main
#   remotes/origin/main
#   remotes/origin/feature-x
#   remotes/origin/feature-y
```

### 分支信息解读

```bash
# -v 显示最后一次提交
git branch -v
# feature-x  a1b2c3d 添加功能 X

# -vv 显示上游分支关系
git branch -vv
# feature-x  a1b2c3d [origin/feature-x: ahead 2] 添加功能 X
#                                         ↑
#                                         本地领先远程 2 个提交
```

### 过滤分支

```bash
# 查看已合并到当前分支的分支
git branch --merged

# 查看未合并到当前分支的分支
git branch --no-merged

# 查看已合并到 main 的分支
git branch --merged main

# 查看包含某个提交的分支
git branch --contains a1b2c3d
```

---

## 9.9 删除分支：用完就扔，保持整洁

分支用完就该删除，保持仓库整洁。Git 提供了安全的删除方式。

### 删除本地分支

```bash
# 删除已合并的分支
git branch -d feature-x

# 强制删除未合并的分支（会丢失提交！）
git branch -D feature-x
# 等同于 git branch --delete --force feature-x
```

### 删除远程分支

```bash
# 方法1：push 空分支
git push origin --delete feature-x

# 方法2：使用冒号
git push origin :feature-x

# 方法3：先删除本地跟踪分支，再删除远程分支
git branch -d -r origin/feature-x
git push origin --delete feature-x
```

### 删除已合并的本地分支

```bash
# 批量删除已合并到 main 的本地分支
git branch --merged main | grep -v "^\*" | grep -v "main" | xargs git branch -d

# 解释：
# git branch --merged main  # 列出已合并到 main 的分支
# grep -v "^\*"             # 排除当前分支
# grep -v "main"            # 排除 main 分支
# xargs git branch -d       # 逐个删除
```

### 清理远程已删除的分支

```bash
# 远程分支已被删除，但本地还有引用
git branch -a
#   remotes/origin/feature-x  # 这个分支在远程已删除

# 清理本地引用
git remote prune origin

# 或者获取时自动清理
git fetch --prune origin
```

---

## 9.10 分支重命名：改个更合适的名字

分支命名不规范？想改个更合适的名字？Git 支持重命名分支。

### 重命名本地分支

```bash
# 重命名当前分支
git branch -m new-name

# 重命名指定分支
git branch -m old-name new-name
```

### 重命名远程分支

Git 没有直接重命名远程分支的命令，需要间接操作：

```bash
# 1. 重命名本地分支
git branch -m old-name new-name

# 2. 删除远程旧分支
git push origin --delete old-name

# 3. 推送新分支到远程
git push origin new-name

# 4. 设置上游分支
git push --set-upstream origin new-name
```

### 批量重命名

```bash
# 将所有 fix/ 开头的分支改为 bugfix/
for branch in $(git branch --list "fix/*"); do
    newname=$(echo $branch | sed 's/fix\//bugfix\//')
    git branch -m "$branch" "$newname"
done
```

---

## 9.11 查看分支历史：分支的演变过程

了解分支的创建和演变过程，有助于理解项目的开发历史。

### 图形化查看分支历史

```bash
# 查看所有分支的图形历史
git log --oneline --graph --all

# 查看特定分支的历史
git log --oneline --graph main feature-x

# 查看分支合并关系
git log --oneline --graph --decorate --all
```

### 查看分支从哪分叉

```bash
# 查看 feature-x 是从哪个提交分叉的
git merge-base main feature-x

# 查看分叉点的详细信息
git log --oneline $(git merge-base main feature-x)
```

### 查看分支之间的关系

```bash
# 查看 feature-x 有但 main 没有的提交
git log main..feature-x --oneline

# 查看两个分支的差异提交
git log main...feature-x --oneline
```

---

## 9.12 分支命名规范：让人一眼看懂你在干嘛

好的分支命名规范，能让团队一眼看出分支的用途和状态。

### 推荐命名格式

```
<type>/<description>
```

**类型（type）：**
- `feature/`：新功能
- `fix/`：Bug 修复
- `hotfix/`：紧急修复
- `release/`：发布准备
- `experiment/`：实验性代码
- `docs/`：文档更新
- `refactor/`：重构

### 命名示例

```bash
# 功能分支
feature/user-login
feature/payment-integration
feature/dark-mode

# 修复分支
fix/login-error
fix/memory-leak
fix/null-pointer

# 紧急修复
hotfix/security-vulnerability
hotfix/critical-bug

# 发布分支
release/v1.0.0
release/v1.1.0-beta

# 实验分支
experiment/new-algorithm
experiment/vue3-migration
```

### 命名原则

1. **简短但有描述性**：`feature/login` 比 `feature/implement-user-authentication-system` 好
2. **使用连字符分隔**：`feature/user-login` 比 `feature/userLogin` 好
3. **避免特殊字符**：只使用字母、数字、连字符、斜杠
4. **包含 issue 编号**：`feature/123-user-login`（如果团队使用 issue 追踪）

---

## 9.13 实战：一个完整的分支开发流程

让我们通过一个完整的例子，演示分支的实际使用。

### 场景设定

- 你在开发一个电商网站
- 需要添加用户登录功能
- 同时需要修复一个结算页面的 Bug

### 步骤1：创建功能分支

```bash
# 确保在主分支上，且代码是最新的
git switch main
git pull origin main

# 创建功能分支
git switch -c feature/user-login

# 开始开发...
```

### 步骤2：开发过程中需要修复 Bug

```bash
# 暂存当前改动
git stash push -m "登录功能：添加表单验证"

# 切换回 main
git switch main

# 创建修复分支
git switch -c hotfix/checkout-bug

# 修复 Bug...
git add .
git commit -m "hotfix: 修复结算页面计算错误"

# 合并到 main
git switch main
git merge hotfix/checkout-bug

# 推送到远程
git push origin main

# 删除修复分支
git branch -d hotfix/checkout-bug
git push origin --delete hotfix/checkout-bug

# 切换回功能分支继续开发
git switch feature/user-login
git stash pop
```

### 步骤3：完成功能开发

```bash
# 完成功能开发
git add .
git commit -m "feat: 添加用户登录功能"

# 获取 main 的最新更新
git fetch origin

# 如果有冲突，先解决冲突
git rebase origin/main

# 推送到远程
git push origin feature/user-login

# 创建 Pull Request 进行代码审查
# ...

# 审查通过后，合并到 main
# （在 GitHub/GitLab 上操作，或手动合并）
git switch main
git merge feature/user-login

# 推送
git push origin main

# 删除功能分支
git branch -d feature/user-login
git push origin --delete feature/user-login
```

### 完整流程图

```
main:     A --- B --- C --- F --- G
                \         /
feature:         D --- E

hotfix:              C --- F
```

### 常用命令速查

```bash
# 创建并切换分支
git switch -c feature/x

# 暂存改动
git stash push -m "描述"

# 恢复暂存
git stash pop

# 合并分支
git merge feature/x

# 删除分支
git branch -d feature/x

# 推送分支
git push origin feature/x
```

---

## 本章小结

本章我们学习了 Git 分支的基础知识：

| 主题 | 要点 |
|------|------|
| 分支的本质 | 只是一个 41 字节的指针 |
| 为什么用分支 | 隔离开发、并行工作、安全实验 |
| HEAD | 指向当前位置的指南针 |
| 创建分支 | `git switch -c name` |
| 切换分支 | `git switch name` |
| 查看分支 | `git branch -vv` |
| 删除分支 | `git branch -d name` |
| 命名规范 | `type/description` 格式 |

**关键要点：**
1. Git 分支轻量快速，鼓励频繁使用
2. 功能开发、Bug 修复、实验性代码都应该用分支
3. 切换分支前处理好未提交的改动（stash 或 commit）
4. 保持分支命名规范，方便团队协作
5. 用完的分支及时删除，保持整洁

**记忆口诀：**
- 新功能 → `feature/`
- 修 Bug → `fix/` 或 `hotfix/`
- 要发布 → `release/`
- 做实验 → `experiment/`

**练习建议：**
1. 创建一个测试仓库，练习创建、切换、删除分支
2. 模拟实际场景：开发功能时突然需要修复 Bug
3. 制定团队的分支命名规范

下一章，我们将学习分支合并——让平行宇宙重新交汇！
