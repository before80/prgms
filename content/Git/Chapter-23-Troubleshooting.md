+++
title = "第23章：Git 故障排查 —— 当事情搞砸时"
weight = 230
date = 2026-04-03T19:36:48+08:00
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++
# 第23章：Git 故障排查 —— 当事情搞砸时

> Git 用久了，总会遇到各种奇怪的问题。这一章，我们准备了一个"急救包"，帮你解决最常见的 Git 故障。记住：冷静，Git 总有办法！

---

## 23.1 `git fsck`：检查仓库完整性

**场景**：Git 行为异常，怀疑仓库损坏。

**你的心情**：😰 → 🤔 → 💡 → ✅

> "Git 突然抽风了，提交失败，提示一些看不懂的错误...是不是仓库坏了？"

### 什么是 `git fsck`？

**`git fsck`**（File System Check）是 Git 的"体检医生"，它会检查 Git 对象数据库的完整性，找出损坏或丢失的对象。

```bash
# 基础检查
git fsck

# 详细输出
git fsck --verbose

# 显示所有对象（包括不可达的）
git fsck --unreachable --no-reflogs
```

### 常见输出解读

```bash
# 悬空 blob（正常）
dangling blob abc1234...
# 含义：有文件内容没有被任何提交引用

# 悬空 commit（需要注意）
dangling commit def5678...
# 含义：有提交没有被任何分支引用，可以用 reflog 找回

# 丢失的对象（严重！）
missing tree 7890abc...
# 含义：Git 找不到这个对象了，需要重新克隆
```

### 修复损坏的仓库

```bash
# 方法1：从远程重新克隆（最简单）
cd ..
mv my-project my-project-corrupted
git clone https://github.com/user/repo.git my-project

# 方法2：使用 git reflog 恢复
git reflog
git reset --hard HEAD@{1}
```

### 幽默一刻

> 你："Git 报错了，说 missing tree！"
> 
> Git："别担心，我只是找不到一个对象。"
> 
> 你："那怎么办？"
> 
> Git："重新克隆吧，从远程下载一个新的我。"

记住：**git fsck 是 Git 的"体检医生"——定期体检，早发现早治疗！**

---

## 23.2 修复损坏的仓库：从绝望中恢复

**场景**：.git 目录损坏，Git 完全无法工作。

**你的心情**：😱 → 😰 → 🤔 → 💪 → ✅

> "完了完了，.git 目录好像坏了，所有 Git 命令都报错！"

### 冷静！代码很可能还在！

```bash
# 检查工作区文件
ls src/
# 文件都在！太好了！

# 重新克隆仓库
git clone https://github.com/user/repo.git my-project-new

# 复制工作区的更改
cp my-project-backup/src/modified-file.js my-project-new/src/

# 提交更改
cd my-project-new
git add .
git commit -m "restore: 从损坏仓库恢复更改"
```

### 幽默一刻

> 你：".git 目录坏了，我完了！"
> 
> Git："冷静，你的代码文件还在吗？"
> 
> 你："在！"
> 
> Git："那就好，重新 clone，复制文件，提交，搞定。"

记住：**仓库损坏不是世界末日——代码在工作区，远程有备份，总有办法恢复！**

---

## 23.3 detached HEAD 状态：怎么办？

**场景**：checkout 了一个提交，现在 HEAD 是 detached 状态。

**你的心情**：😰 → 🤔 → 💡 → ✅

> "我 checkout 了一个旧的提交，现在 Git 提示 'detached HEAD'，这是什么鬼？"

### 什么是 detached HEAD？

**detached HEAD** 是指 HEAD 直接指向一个提交，而不是指向一个分支。

```bash
# 查看当前状态
git status
# HEAD detached at abc1234

# 创建新分支保存当前状态
git checkout -b new-feature

# 或者回到原来的分支
git checkout main
```

### 幽默一刻

> 你："HEAD detached 了，怎么办？"
> 
> Git："别担心，只是 HEAD 没有依附分支。"
> 
> 你："那我的代码呢？"
> 
> Git："代码安全，但如果你切换分支，这些代码可能就'飘'了。"

记住：**detached HEAD 不是错误——它是 Git 的"观景台"，看完记得回到分支上！**

---

## 23.4 合并冲突无法解决：终极方案

**场景**：冲突太复杂，无法解决。

```bash
# 方法1：放弃合并
git merge --abort

# 方法2：使用合并工具
git mergetool

# 方法3：手动选择一方
git checkout --ours file.txt    # 保留当前分支
git checkout --theirs file.txt  # 保留合并分支

# 方法4：重置到合并前
git reset --hard HEAD
```

### 幽默一刻

> 你："冲突太复杂了，我解决不了！"
> 
> Git："那就放弃吧，merge --abort，世界恢复平静。"
> 
> 你："那我的工作呢？"
> 
> Git："重新来过，有时候撤退是最明智的选择。"

记住：**合并冲突不是战斗——有时候放弃合并，重新规划，反而是最高效的选择！**

---

## 23.5 推送被拒绝的各种原因

**场景**：git push 被拒绝。

```bash
# 原因1：非快进推送
git push origin feature
# ! [rejected] non-fast-forward

# 解决：先拉取再推送
git pull origin feature
git push origin feature

# 原因2：权限不足
git push origin main
# ! [remote rejected] main -> main (protected branch)

# 解决：使用 PR/MR 合并

# 原因3：远程有更新
git fetch origin
git rebase origin/main
git push origin main
```

### 幽默一刻

> 你："推送被拒绝了！"
> 
> Git："远程有更新，你先拉取一下。"
> 
> 你："为什么？"
> 
> Git："因为世界在变，你也要跟着变。"

记住：**推送被拒绝不是失败——是 Git 在保护你，避免覆盖他人的工作！**

---

## 23.6 权限问题排查：SSH、Token、权限

**场景**：无法推送，提示权限错误。

```bash
# 检查 SSH 连接
ssh -T git@github.com

# HTTPS 改为 SSH
git remote set-url origin git@github.com:user/repo.git

# 更新 Token
git remote set-url origin https://TOKEN@github.com/user/repo.git
```

### 幽默一刻

> 你："我没有权限推送！"
> 
> Git："检查一下你的 SSH 密钥。"
> 
> 你："密钥是什么？"
> 
> Git："就是你的'身份证'，证明你是你。"

记住：**权限问题是"门卫"问题——要么证明你是谁，要么找有权限的人！**

---

## 23.7 认证失败：HTTPS 凭据问题

**场景**：提示输入用户名密码，或者认证失败。

```bash
# 清除凭据缓存
git config --global --unset credential.helper

# Windows
git credential-manager delete https://github.com

# macOS
git credential-osxkeychain erase host=github.com protocol=https
```

### 幽默一刻

> 你："Git 一直问我要密码！"
> 
> Git："因为我忘了你是谁。"
> 
> 你："那怎么办？"
> 
> Git："重新告诉我，我会记住的。"

记住：**认证失败是"失忆"问题——重新告诉 Git 你是谁，它会记住的！**

---

## 23.8 性能优化：大仓库加速技巧

**场景**：仓库太大，操作很慢。

```bash
# 1. 浅克隆
git clone --depth 1 https://github.com/large/repo.git

# 2. 单分支克隆
git clone --single-branch https://github.com/large/repo.git

# 3. 稀疏检出
git sparse-checkout init --cone
git sparse-checkout set src/

# 4. 定期 gc
git gc --aggressive
```

### 幽默一刻

> 你："克隆要 10 分钟，太慢了！"
> 
> Git："试试浅克隆，只下载最新版本。"
> 
> 你："为什么这么快？"
> 
> Git："因为你不需要 10 年前的代码。"

记住：**大仓库需要"瘦身"——只取你需要的，忽略你不需要的！**

---

## 23.9 仓库瘦身：清理历史大文件

**场景**：仓库太大，需要清理历史中的大文件。

```bash
# 使用 git-filter-repo
pip install git-filter-repo
git filter-repo --strip-blobs-bigger-than 10M
git push origin --force --all
```

### 幽默一刻

> 你："仓库 1GB 了，怎么办？"
> 
> Git："你提交了太多大文件。"
> 
> 你："但我已经删除了！"
> 
> Git："历史里还有，用 filter-repo 清理。"

记住：**仓库瘦身是"减肥"——不仅要少吃，还要运动（清理历史）！**

---

## 23.10 找回丢失的提交：`git reflog` 进阶用法

**场景**：误删了分支，或者 reset 了重要的提交。

```bash
# 查看 reflog
git reflog

# 恢复删除的分支
git checkout -b recovered-branch HEAD@{5}

# 恢复 reset 前的状态
git reset --hard HEAD@{1}
```

### 幽默一刻

> 你："我误删了分支！"
> 
> Git："淡定，reflog 里有记录。"
> 
> 你："找到了！你是我的救命恩人！"
> 
> Git："我是你的时光机，记得定期备份。"

记住：**reflog 是 Git 的"时光机"——几乎所有操作都能找回，只要你记得用它！**

---

## 23.11 本章小结：冷静，Git 总有办法

```markdown
## 故障排查 checklist

- [ ] 保持冷静，不要 panic
- [ ] 使用 git status 查看状态
- [ ] 使用 git reflog 找回丢失的提交
- [ ] 使用 git fsck 检查仓库完整性
- [ ] 使用 --abort 取消当前操作
- [ ] 从远程重新克隆（最后手段）
- [ ] 定期备份重要仓库

## 黄金法则

1. 不要删除 .git 目录
2. 不要 force push 主分支
3. 定期 push 到远程
4. 使用 reflog 作为时光机
5. 冷静，Git 总有办法
```

**冷静，Git 总有办法！** 🚑✨

---

**第23章完**

