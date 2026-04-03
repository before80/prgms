+++
title = "第6章：查看历史与对比 —— Git 时光机与照妖镜"
weight = 60
date = 2026-04-03T19:36:48+08:00
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++
# 第6章：查看历史与对比 —— Git 时光机与照妖镜

> 想象一下，你是一位时间旅行者，可以穿越回代码的任何一个历史时刻，看看当时发生了什么。Git 就是你的时光机，而 `git log`、`git diff`、`git blame` 这些命令就是你的照妖镜——让代码的过去无所遁形。

---

## 6.1 `git log`：穿越时光的机器

`git log` 是 Git 中最常用的命令之一，它就像一台时光机，带你回顾项目的演变历程。每一次提交（commit）都是时光长河中的一个节点，记录着谁在什么时候做了什么改动。

### 基础用法

```bash
# 查看提交历史（默认格式）
git log

# 限制显示最近的 N 条记录
git log -5

# 显示每次提交的统计信息
git log --stat

# 显示每次提交的文件改动内容
git log -p
```

### 输出格式解析

当你运行 `git log` 时，会看到类似这样的输出：

```
commit a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9
Author: 张三 <zhangsan@example.com>
Date:   Mon Mar 16 10:00:00 2026 +0800

    修复登录页面的样式问题

    - 调整了按钮的圆角
    - 修复了移动端适配问题
```

**各部分的含义：**
- **commit**：提交的 SHA-1 哈希值（唯一标识），就像每个提交的身份证号
- **Author**：作者信息，告诉你这行代码是谁写的（方便找人算账😏）
- **Date**：提交时间，精确到秒
- **提交信息**：描述这次改动的内容

### 实用技巧

```bash
# 按作者过滤
git log --author="张三"

# 按日期过滤
git log --since="2026-03-01" --until="2026-03-16"

# 按文件过滤（只看某个文件的修改历史）
git log -- path/to/file.js

# 搜索提交信息中的关键词
git log --grep="bug"

# 查看某个文件的修改历史（包括重命名）
git log --follow -- path/to/file.js
```

### 小提示

`git log` 的输出默认会进入分页模式（类似 `less` 命令），你可以：
- 按 `j` 向下滚动，`k` 向上滚动
- 按 `q` 退出
- 按 `/` 搜索，按 `n` 跳到下一个匹配

---

## 6.2 单行显示与图形化：让历史一目了然

默认的 `git log` 输出像是一篇篇小作文，信息量大但阅读起来有点累。这时候就需要一些格式化技巧，让历史记录变得清爽易读。

### 单行显示：`--oneline`

```bash
# 每条提交只占一行，简洁明了
git log --oneline
```

输出示例：
```
a1b2c3d 修复登录页面的样式问题
b2c3d4e 添加用户注册功能
c3d4e5f 初始化项目
```

### 自定义格式：`--pretty=format`

Git 允许你像搭积木一样自定义输出格式：

```bash
# 常用格式组合
git log --pretty=format:"%h - %an, %ar : %s"

# 带颜色的版本（更美观）
git log --pretty=format:"%C(yellow)%h%C(reset) - %C(green)%an%C(reset), %C(blue)%ar%C(reset) : %s"
```

**常用占位符说明：**

| 占位符 | 含义 |
|--------|------|
| `%H` | 完整哈希值 |
| `%h` | 简短哈希值（7位） |
| `%an` | 作者名字 |
| `%ae` | 作者邮箱 |
| `%ad` | 作者日期 |
| `%ar` | 相对日期（如 "2 days ago"） |
| `%s` | 提交信息标题 |
| `%b` | 提交信息正文 |
| `%d` | 分支和标签引用 |

### 图形化显示：`--graph`

当项目有多个分支、合并操作时，纯文本的历史记录就像一团乱麻。`--graph` 选项用 ASCII 字符画出分支合并图，让历史结构一目了然。

```bash
# 图形化显示 + 单行格式
git log --oneline --graph

# 图形化 + 完整信息 + 所有分支
git log --oneline --graph --all

# 终极组合：图形化 + 单行 + 分支名 + 装饰
git log --oneline --graph --decorate --all
```

输出示例：
```
* a1b2c3d (HEAD -> main, origin/main) 修复登录页面的样式问题
*   b2c3d4e 合并分支 'feature/login'
|\
| * c3d4e5f 添加登录表单验证
| * d4e5f6g 创建登录页面
* | e5f6g7h 更新依赖
|/
* f6g7h8i 初始化项目
```

**图形符号解读：**
- `*` 表示一个提交节点
- `|` 表示分支线
- `/` 和 `\` 表示分支的分离和合并
- `(HEAD -> main)` 表示当前所在的分支
- `(origin/main)` 表示远程分支的位置

### 配置别名：懒人必备

把这些常用组合设置成别名，以后打字更轻松：

```bash
# 在全局配置中添加别名
git config --global alias.lg "log --color --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit"

# 现在只需要输入
git lg

# 再来一个简洁版
git config --global alias.ls "log --oneline --graph --decorate"
```

### 实用组合推荐

```bash
# 查看最近10条，图形化显示
git log --oneline --graph -10

# 查看所有分支的历史
git log --oneline --graph --all

# 查看某个文件的历史（单行格式）
git log --oneline -- path/to/file.js

# 查看某个作者的提交（带图形）
git log --oneline --graph --author="张三"
```

---

## 6.3 按条件过滤：查查同事干了啥

项目大了，提交记录成千上万，找一条特定的提交就像在沙子里淘金。这时候就需要各种过滤条件来精准定位。

### 按作者过滤

```bash
# 查看某个作者的所有提交
git log --author="张三"

# 支持正则匹配（查找姓张的所有作者）
git log --author="^张"

# 按邮箱过滤（更精确）
git log --author="zhangsan@example.com"
```

**小贴士：** 作者信息是提交时 Git 记录的，任何人都可以伪装成别人提交（虽然不建议这么做）。如果想查"真正的"提交者，可以用 `--committer` 参数：

```bash
# 查看提交者（执行 git commit 的人）
git log --committer="张三"
```

### 按时间过滤

```bash
# 查看最近一周的提交
git log --since="1 week ago"

# 查看某个日期之后的提交
git log --since="2026-03-01"

# 查看某个日期范围内的提交
git log --since="2026-03-01" --until="2026-03-16"

# 查看昨天到今天凌晨的提交
git log --since="yesterday" --until="today"

# 查看特定日期的提交
git log --after="2026-03-15 00:00" --before="2026-03-16 00:00"
```

**时间格式支持：**
- 具体日期：`2026-03-16`
- 相对时间：`1 week ago`, `3 days ago`, `yesterday`
- 带时间的日期：`2026-03-16 10:00:00`

### 按提交信息过滤

```bash
# 搜索提交信息中包含 "bug" 的提交
git log --grep="bug"

# 忽略大小写
git log --grep="bug" -i

# 使用正则表达式
git log --grep="fix.*bug" -E

# 搜索多个关键词（满足任意一个）
git log --grep="bug" --grep="fix" --all-match

# 只搜索合并提交的提交信息
git log --grep="Merge" --merges

# 排除合并提交
git log --grep="feature" --no-merges
```

### 按文件过滤

```bash
# 查看某个文件的修改历史
git log -- path/to/file.js

# 查看多个文件
git log -- file1.js file2.js

# 查看某个目录下的所有修改
git log -- src/

# 查看包含某个文件改动的提交（显示统计）
git log --stat -- path/to/file.js

# 查看某个文件的详细改动内容
git log -p -- path/to/file.js
```

### 按提交范围过滤

```bash
# 查看两个提交之间的历史
git log commit1..commit2

# 查看从某个提交到当前 HEAD 的历史
git log a1b2c3d..HEAD

# 查看两个分支之间的差异提交
git log main..feature-branch

# 查看只在 feature-branch 中但不在 main 中的提交
git log main...feature-branch
```

**注意：** `..` 和 `...` 的区别：
- `A..B`：在 B 中但不在 A 中的提交
- `A...B`：在 A 或 B 中但不在两者交集中的提交（对称差）

### 组合过滤：终极查询

```bash
# 查看张三最近一周修复 bug 的提交
git log --author="张三" --since="1 week ago" --grep="fix" --grep="bug" --all-match

# 查看某个文件在特定日期范围内的修改
git log --since="2026-03-01" --until="2026-03-16" -- path/to/file.js

# 查看最近10条非合并提交，单行显示
git log --oneline --no-merges -10

# 查看某个作者在特定分支上的提交
git log feature-branch --author="李四" --oneline
```

### 实际应用场景

**场景1：查同事今天做了什么**
```bash
git log --since="today" --author="同事名字" --oneline
```

**场景2：找某个功能是什么时候添加的**
```bash
git log --all --grep="功能名称" --oneline
```

**场景3：查某段时间内谁最活跃**
```bash
git log --since="1 month ago" --pretty=format:"%an" | sort | uniq -c | sort -rn
```

---

## 6.4 `git diff`：找茬神器，看看改了啥

`git diff` 是 Git 中最强大的"找茬"工具，它能精确地告诉你：哪里改了、怎么改的、改了多少行。就像玩"找不同"游戏，Git 会高亮显示所有差异。

### 什么是 diff？

**diff**（difference 的缩写）是一种显示两个文件或版本之间差异的格式。它用特殊的符号标记出：
- `-` 开头的行：被删除的内容
- `+` 开头的行：新增的内容
- 没有符号的行：上下文（帮助理解改动的位置）

### 基本用法

```bash
# 查看工作区与暂存区的差异
#（即：你改了但还没 git add 的内容）
git diff

# 查看暂存区与最新提交的差异
#（即：你 git add 了但还没 git commit 的内容）
git diff --staged
# 或者
git diff --cached

# 查看工作区与最新提交的差异
#（即：所有未提交的改动）
git diff HEAD
```

### diff 输出格式解析

```diff
diff --git a/README.md b/README.md
index 1234567..abcdefg 100644
--- a/README.md
+++ b/README.md
@@ -1,5 +1,5 @@
 # 我的项目

-这是一个简单的示例项目。
+这是一个超级棒的示例项目！

 ## 功能列表
```

**格式解读：**
- `diff --git a/README.md b/README.md`：显示对比的文件
- `--- a/README.md`：旧版本（a 代表 before）
- `+++ b/README.md`：新版本（b 代表 after）
- `@@ -1,5 +1,5 @@`：差异块的位置信息
  - `-1,5`：旧文件从第1行开始，共5行
  - `+1,5`：新文件从第1行开始，共5行
- `-` 开头的行：被删除的内容
- `+` 开头的行：新增的内容

### 查看特定文件的差异

```bash
# 只查看某个文件的差异
git diff path/to/file.js

# 查看多个文件的差异
git diff file1.js file2.js

# 查看某个目录下所有文件的差异
git diff src/
```

### 查看已暂存的差异

```bash
# 查看已暂存（staged）的内容
git diff --staged

# 查看特定文件已暂存的内容
git diff --staged path/to/file.js

# 查看已暂存内容的统计信息
git diff --staged --stat
```

### 实用选项

```bash
# 只显示文件名（不显示具体改动）
git diff --name-only

# 显示统计信息（改了多少文件、多少行）
git diff --stat

# 显示更详细的统计（包括增减行数）
git diff --shortstat

# 忽略空白字符的差异
git diff -w
# 或
git diff --ignore-all-space

# 忽略行尾空白字符
git diff --ignore-space-at-eol

# 以单词为单位显示差异（更精确）
git diff --word-diff

# 只查看新增的文件
git diff --diff-filter=A

# 只查看删除的文件
git diff --diff-filter=D

# 只查看修改的文件
git diff --diff-filter=M
```

### 彩色输出配置

默认情况下 Git 会用颜色区分差异，如果颜色没了可以这样恢复：

```bash
# 开启彩色输出
git config --global color.ui auto

# 或者针对 diff 单独配置
git config --global color.diff auto
```

### 小技巧

**1. 查看某个文件的改动行数**
```bash
git diff --stat path/to/file.js
```

**2. 查看改动中是否包含某个关键词**
```bash
git diff | grep "关键词"
```

**3. 将 diff 输出保存到文件**
```bash
git diff > my-changes.patch
```

**4. 查看 diff 时不显示上下文（只显示改动的行）**
```bash
git diff -U0
```
（`-U` 参数控制上下文的行数，0 表示不显示上下文）

---

## 6.5 `git diff` 进阶：对比不同分支、不同提交

基础的 `git diff` 已经很强大了，但真正的威力在于可以对比任意两个版本——无论是分支、标签还是具体的提交。

### 对比两个分支

```bash
# 查看 feature-branch 与 main 分支的差异
#（显示 feature-branch 中有但 main 中没有的内容）
git diff main..feature-branch

# 或者反过来（显示 main 中有但 feature-branch 中没有的内容）
git diff feature-branch..main

# 查看两个分支的共同祖先之后的差异（更常用）
git diff main...feature-branch
```

**`..` 和 `...` 的区别：**
- `A..B`：显示 B 有但 A 没有的提交带来的改动
- `A...B`：显示从 A 和 B 的共同祖先之后，两者的差异（三方对比）

### 对比特定提交

```bash
# 对比两个提交
git diff commit1 commit2

# 使用简短哈希
git diff a1b2c3d e5f6g7h

# 对比某个提交与当前 HEAD
git diff a1b2c3d HEAD

# 对比某个提交与其父提交（即那次提交改了什么）
git diff a1b2c3d^ a1b2c3d
# 或者更简洁的写法
git diff a1b2c3d^
```

### 对比特定文件在不同版本中的差异

```bash
# 查看某个文件在两个分支中的差异
git diff main feature-branch -- path/to/file.js

# 查看某个文件在两个提交中的差异
git diff a1b2c3d e5f6g7h -- path/to/file.js

# 查看某个文件在当前分支与另一个分支中的差异
git diff feature-branch -- path/to/file.js
```

### 对比标签

```bash
# 对比两个标签之间的差异
git diff v1.0.0 v2.0.0

# 查看从 v1.0.0 到 v2.0.0 改动了哪些文件
git diff v1.0.0 v2.0.0 --stat

# 查看某个文件在两个版本之间的具体改动
git diff v1.0.0 v2.0.0 -- src/main.js
```

### 对比工作区与任意版本

```bash
# 查看工作区与某个提交的差异
git diff a1b2c3d

# 查看暂存区与某个提交的差异
git diff --staged a1b2c3d

# 查看工作区与某个分支的差异
git diff feature-branch
```

### 只查看文件名

当你只想知道改了哪些文件，而不关心具体内容时：

```bash
# 对比两个分支，只显示文件名
git diff --name-only main..feature-branch

# 对比两个提交，只显示文件名
git diff --name-only a1b2c3d e5f6g7h

# 显示改动的文件列表（带状态：A=新增, M=修改, D=删除）
git diff --name-status main..feature-branch
```

### 生成补丁文件

```bash
# 将差异保存为补丁文件
git diff main..feature-branch > feature.patch

# 生成包含二进制文件的补丁
git diff --binary main..feature-branch > feature.patch

# 生成可以发送邮件的补丁格式
git diff --patch-with-stat main..feature-branch > feature.patch
```

### 实用场景

**场景1：代码审查前预览改动**
```bash
# 在提交 PR 前，先看看自己的分支与主分支的差异
git diff main...feature-branch
```

**场景2：找某个功能是什么时候改的**
```bash
# 对比两个版本，看某个文件的改动
git diff v1.0.0 v1.1.0 -- src/core.js
```

**场景3：检查合并会不会有冲突**
```bash
# 预览合并 feature-branch 到 main 会有什么改动
git diff main...feature-branch
```

---

## 6.6 `git show`：单次提交的放大镜

有时候你不需要对比两个版本，只想看看某一次提交具体改了什么。`git show` 就是专门干这个的——它把某次提交的信息和改动内容一次性展示给你。

### 基本用法

```bash
# 查看某次提交的详细信息
git show a1b2c3d

# 查看最新提交（HEAD）
git show

# 查看某次提交的某个文件
git show a1b2c3d -- path/to/file.js

# 查看某次提交的统计信息
git show a1b2c3d --stat
```

### 输出内容解析

`git show` 的输出包含三部分：
1. **提交元数据**：作者、日期、提交信息等
2. **diff 内容**：这次提交的具体改动
3. **文件统计**：改动了多少文件、多少行

```
commit a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9
Author: 张三 <zhangsan@example.com>
Date:   Mon Mar 16 10:00:00 2026 +0800

    修复登录页面的样式问题

    - 调整了按钮的圆角
    - 修复了移动端适配问题

diff --git a/src/login.css b/src/login.css
index 1234567..abcdefg 100644
--- a/src/login.css
+++ b/src/login.css
@@ -10,7 +10,7 @@
 .login-button {
-    border-radius: 3px;
+    border-radius: 8px;
     padding: 10px 20px;
 }
```

### 显示特定信息

```bash
# 只显示提交信息（不显示 diff）
git show --no-patch a1b2c3d
# 或者
git show -s a1b2c3d

# 只显示提交信息标题
git show --format="%s" --no-patch a1b2c3d

# 显示提交的作者和日期
git show --format="Author: %an%nDate: %ad" --no-patch a1b2c3d

# 显示提交的文件列表
git show --name-only a1b2c3d

# 显示提交的统计信息
git show --stat a1b2c3d

# 显示提交的简短统计
git show --shortstat a1b2c3d
```

### 格式化输出

```bash
# 自定义格式（类似 git log --pretty=format）
git show --format="%h - %an, %ar : %s" --no-patch a1b2c3d

# 显示带颜色的输出
git show --color a1b2c3d

# 以特定格式显示日期
git show --format="%ad" --date=short --no-patch a1b2c3d
```

### 查看特定类型的对象

`git show` 不仅可以看提交，还可以看其他 Git 对象：

```bash
# 查看某个标签的信息
git show v1.0.0

# 查看某个树对象（目录）
git show main:src/

# 查看某个 blob 对象（文件内容）
git show main:src/index.js

# 查看某个分支的当前状态
git show feature-branch
```

### 与其他命令的组合

```bash
# 查看某次提交中某个文件的最终内容
git show a1b2c3d:path/to/file.js

# 将某次提交中的某个文件导出
git show a1b2c3d:path/to/file.js > old-version.js

# 查看某次提交中改动的文件列表（用于脚本）
git show --name-only --pretty="" a1b2c3d
```

### 实用技巧

**1. 快速查看最新提交的改动**
```bash
git show
# 等同于
git show HEAD
```

**2. 查看某次提交改了哪些文件**
```bash
git show --name-status a1b2c3d
```

**3. 查看某次提交的改动大小**
```bash
git show --stat a1b2c3d
```

**4. 在 pager 中查看（适合长输出）**
```bash
git show a1b2c3d | less
```

---

## 6.7 `git blame`：谁写的这行代码？（别用来甩锅）

`git blame`（责备）这个名字听起来有点攻击性，但它其实是个非常有用的工具——它能告诉你每一行代码是谁写的、什么时候写的、在哪次提交中写的。当然，知道是谁写的之后，你可以选择"友好地"找他讨论，而不是真的去"责备"人家😉。

### 基本用法

```bash
# 查看某个文件的每一行是谁写的
git blame path/to/file.js

# 查看某个文件的特定行范围
git blame -L 10,20 path/to/file.js

# 查看从第10行到文件末尾
git blame -L 10, path/to/file.js
```

### 输出格式解析

```
^a1b2c3d (张三 2026-03-01 10:00:00 +0800 1) import React from 'react';
^a1b2c3d (张三 2026-03-01 10:00:00 +0800 2) import './App.css';
b2c3d4e5 (李四 2026-03-05 14:30:00 +0800 3) import { useState } from 'react';
c3d4e5f6 (王五 2026-03-10 09:15:00 +0800 4)
c3d4e5f6 (王五 2026-03-10 09:15:00 +0800 5) function App() {
```

**各列的含义：**
1. **提交哈希**：那行代码最后一次修改的提交
2. **作者名字**：谁写的
3. **日期时间**：什么时候写的
4. **行号**：在文件中的行号
5. **代码内容**：实际的代码

**注意：** `^` 符号表示这行代码从文件的第一次提交就存在了（初始版本）。

### 忽略空白字符的改动

有时候你只是格式化了代码（比如调整了缩进），并不想因此"抢走"别人的"功劳"。可以用 `-w` 参数忽略空白字符的变化：

```bash
# 忽略空白字符的改动
git blame -w path/to/file.js
```

### 显示作者邮箱

```bash
# 显示作者邮箱而不是名字
git blame -e path/to/file.js
```

### 显示更短的时间

```bash
# 显示相对时间（如 "2 weeks ago"）
git blame --date=relative path/to/file.js

# 只显示日期，不显示时间
git blame --date=short path/to/file.js
```

### 显示提交信息

```bash
# 在作者信息后显示提交信息的第一行
git blame -s path/to/file.js
```

### 实用技巧

**1. 快速定位某行代码的改动历史**
```bash
# 先 blame 找到提交哈希
git blame path/to/file.js
# 然后用 git show 查看那次提交的详细信息
git show a1b2c3d
```

**2. 查看某行代码为什么被修改**
```bash
# 找到那行代码的提交哈希
git blame -L 42,42 path/to/file.js
# 查看那次提交的信息
git show a1b2c3d
```

**3. 统计谁贡献的代码最多**
```bash
git blame path/to/file.js | awk '{print $2}' | sort | uniq -c | sort -rn
```

### 注意事项

1. **别用来甩锅**：`git blame` 是为了理解代码的历史，不是为了找人背锅。代码出问题，团队共同负责。

2. **作者不一定是责任人**：有时候代码是复制粘贴的，或者经过多人修改，最初的作者可能已经不是最了解这段代码的人了。

3. **结合其他命令使用**：`git blame` 通常只是第一步，找到提交后，用 `git show` 查看详细信息，用 `git log` 查看上下文。

---

## 6.8 `git bisect`：二分查找，快速定位 Bug 真凶

想象一下：你的项目有 1000 次提交，突然发现一个 Bug，但你不知道是哪次提交引入的。手动检查 1000 次提交？那得检查到猴年马月！这时候 `git bisect` 就派上用场了——它用二分查找算法，帮你快速定位问题提交。

### 什么是二分查找？

**二分查找**（Binary Search）是一种高效的查找算法：
- 每次将搜索范围缩小一半
- 1000 次提交，最多只需要检查 10 次（因为 2^10 = 1024）
- 10000 次提交，最多只需要检查 14 次（因为 2^14 = 16384）

### 基本流程

`git bisect` 的工作流程就像在玩"猜数字"游戏：

```
开始
  ↓
标记一个"好"版本（没有 Bug）
  ↓
标记一个"坏"版本（有 Bug）
  ↓
Git 自动检出中间版本
  ↓
你测试这个版本
  ↓
告诉 Git 这是"好"还是"坏"
  ↓
Git 继续缩小范围...
  ↓
直到找到引入 Bug 的提交
```

### 实战演示

假设你发现当前代码有 Bug，但一周前的版本是好的：

```bash
# 1. 开始二分查找
git bisect start

# 2. 标记当前版本为"坏"
git bisect bad

# 3. 标记一周前的版本为"好"（假设提交哈希是 a1b2c3d）
git bisect good a1b2c3d

# Git 会自动检出中间版本，你会看到类似这样的输出：
# Bisecting: 50 revisions left to test after this (roughly 6 steps)
# [b2c3d4e...] 某个中间的提交

# 4. 测试当前版本
# 运行你的测试，或者手动检查 Bug 是否存在

# 5. 如果 Bug 存在，标记为"坏"
git bisect bad

# 6. 如果 Bug 不存在，标记为"好"
git bisect good

# 7. 重复步骤 4-6，直到 Git 找到问题提交
# 你会看到类似这样的输出：
# a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9 is the first bad commit
# commit a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9
# Author: 张三 <zhangsan@example.com>
# Date:   Mon Mar 10 15:30:00 2026 +0800
#
#     添加新功能 X

# 8. 结束二分查找，回到原来的分支
git bisect reset
```

### 自动化测试

如果你有自动化测试脚本，可以让 `git bisect` 自动运行：

```bash
# 开始二分查找
git bisect start

# 标记坏版本
git bisect bad HEAD

# 标记好版本
git bisect good v1.0.0

# 运行自动化测试
# 如果测试通过（返回 0），Git 认为是"好"
# 如果测试失败（返回非 0），Git 认为是"坏"
git bisect run ./test.sh

# Git 会自动完成整个二分查找过程
```

### 跳过某些提交

有时候某些提交无法测试（比如编译失败），可以跳过：

```bash
# 跳过当前版本
git bisect skip

# 跳过某个范围的提交
git bisect skip a1b2c3d..b2c3d4e
```

### 可视化二分查找过程

```bash
# 查看二分查找的日志
git bisect log

# 将日志保存到文件（可以手动编辑后重放）
git bisect log > bisect-log.txt

# 从日志文件重放
git bisect replay bisect-log.txt
```

### 实际应用场景

**场景1：定位性能回归**
```bash
# 发现性能下降，但不知道是哪次提交导致的
git bisect start
git bisect bad HEAD  # 当前版本性能差
git bisect good v1.0.0  # 1.0.0 版本性能好
git bisect run ./performance-test.sh
```

**场景2：定位功能 Bug**
```bash
# 发现某个功能失效了
git bisect start
git bisect bad HEAD
git bisect good a1b2c3d  # 上次发布时的版本
git bisect run ./e2e-test.sh
```

**场景3：手动测试**
```bash
# 没有自动化测试，只能手动测试
git bisect start
git bisect bad HEAD
git bisect good v1.0.0
# Git 会不断检出中间版本，你手动测试后标记 good/bad
```

### 注意事项

1. **确保"好"和"坏"的定义明确**：有时候 Bug 不是每次都能复现，这会让二分查找变得困难。

2. **跳过无法测试的提交**：如果某个提交编译失败或无法运行，及时用 `git bisect skip` 跳过。

3. **记得重置**：二分查找结束后，一定要用 `git bisect reset` 回到原来的状态。

---

## 6.9 Git 历史可视化：图形工具让历史更直观

虽然命令行工具功能强大，但有时候图形化的界面更直观。Git 有很多图形化工具，让你用鼠标点点就能查看历史。

### Git 自带的图形工具

Git 自带了一个简单的图形工具 `gitk`（需要单独安装）：

```bash
# 启动 gitk
gitk

# 查看所有分支
gitk --all

# 查看某个文件的历史
gitk path/to/file.js
```

### VS Code 内置的 Git 图形界面

如果你用 VS Code，它已经内置了强大的 Git 支持：

1. **源代码管理面板**：左侧活动栏的 Git 图标
2. **提交历史**：右键点击文件 → "查看文件历史"
3. **分支图**：安装 Git Graph 插件后，点击状态栏的 Git Graph 按钮

### 推荐的 Git 图形工具

**1. GitKraken（跨平台，免费版功能丰富）**
- 漂亮的分支图
- 拖拽式合并
- 内置冲突解决工具
- 官网：https://www.gitkraken.com/

**2. SourceTree（免费，功能强大）**
- Atlassian 出品
- 支持 Git Flow
- 强大的搜索和过滤
- 官网：https://www.sourcetreeapp.com/

**3. Fork（Mac/Windows，付费但值得）**
- 界面简洁美观
- 性能优秀
- 冲突解决工具好用
- 官网：https://git-fork.com/

**4. GitHub Desktop（免费，简单易用）**
- GitHub 官方出品
- 适合新手
- 与 GitHub 集成好
- 官网：https://desktop.github.com/

**5. TortoiseGit（Windows，资源管理器集成）**
- 右键菜单集成
- 适合习惯 Windows 操作的用户
- 官网：https://tortoisegit.org/

### 选择建议

| 工具 | 适用场景 | 价格 |
|------|----------|------|
| GitKraken | 专业开发，需要美观界面 | 免费版够用 |
| SourceTree | 功能全面，免费 | 免费 |
| Fork | 追求性能和体验 | 付费 |
| GitHub Desktop | 新手入门，简单使用 | 免费 |
| TortoiseGit | Windows 用户，习惯右键 | 免费 |

### 命令行 vs 图形工具

**命令行优势：**
- 速度快，不依赖 GUI
- 远程服务器也能用
- 可以写脚本自动化
- 精确控制每个参数

**图形工具优势：**
- 直观，一目了然
- 分支图可视化
- 冲突解决更方便
- 适合新手学习

**建议：** 命令行和图形工具结合使用，日常用命令行，复杂操作用图形工具。

---

## 6.10 实战案例：代码崩了，怎么找凶手？

假设你早上来到公司，发现生产环境崩溃了。日志显示是某个函数抛出了异常。怎么办？别慌，按照下面的步骤来：

### 场景设定

- 生产环境版本：`v2.0.0`（标签）
- 上次正常版本：`v1.9.0`（标签）
- 异常函数：`calculateTotal()` 在 `src/utils.js` 第 42 行

### 步骤1：确定问题范围

```bash
# 查看两个版本之间有哪些提交
git log v1.9.0..v2.0.0 --oneline

# 统计一下有多少次提交
git log v1.9.0..v2.0.0 --oneline | wc -l
# 输出：50
```

有 50 次提交，手动检查太麻烦了，用 `git bisect`！

### 步骤2：准备测试脚本

创建一个测试脚本 `test-bug.sh`：

```bash
#!/bin/bash
# test-bug.sh

# 安装依赖
npm install

# 运行测试
npm test -- --grep "calculateTotal"

# 检查测试结果
if [ $? -eq 0 ]; then
    exit 0  # 测试通过，返回 0（好）
else
    exit 1  # 测试失败，返回 1（坏）
fi
```

### 步骤3：运行二分查找

```bash
# 开始二分查找
git bisect start

# 标记 v2.0.0 为坏版本（有 Bug）
git bisect bad v2.0.0

# 标记 v1.9.0 为好版本（正常）
git bisect good v1.9.0

# 运行自动化测试
git bisect run ./test-bug.sh
```

Git 会自动运行测试，大约 6 步后（因为 log2(50) ≈ 6），你会看到：

```
a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9 is the first bad commit
commit a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9
Author: 李四 <lisi@example.com>
Date:   Fri Mar 13 16:45:00 2026 +0800

    重构 calculateTotal 函数，优化性能

    - 使用新的算法计算总价
    - 添加缓存机制
```

### 步骤4：查看具体改动

```bash
# 查看那次提交改了什么
git show a1b2c3d

# 重点看 src/utils.js 的改动
git show a1b2c3d -- src/utils.js
```

发现第 42 行的除法运算没有处理除数为 0 的情况！

### 步骤5：修复 Bug

```bash
# 回到主分支
git bisect reset
git checkout main

# 创建修复分支
git checkout -b hotfix/divide-by-zero

# 修复代码（添加除数检查）
# ...

# 提交修复
git add src/utils.js
git commit -m "fix: 修复 calculateTotal 除数为 0 的问题"

# 推送到远程
git push origin hotfix/divide-by-zero

# 创建 PR，合并到 main 和 release 分支
```

### 步骤6：验证修复

```bash
# 运行测试
npm test

# 手动验证边界情况
node -e "const { calculateTotal } = require('./src/utils'); console.log(calculateTotal(100, 0));"
```

### 总结

| 步骤 | 命令 | 目的 |
|------|------|------|
| 1 | `git log v1.9.0..v2.0.0` | 确定问题范围 |
| 2 | 编写测试脚本 | 自动化测试 |
| 3 | `git bisect` | 快速定位问题提交 |
| 4 | `git show` | 查看具体改动 |
| 5 | 修复并提交 | 解决问题 |
| 6 | 运行测试 | 验证修复 |

通过这个案例，你会发现 Git 的历史查看工具不仅能"看"历史，还能帮你"破案"！

---

## 本章小结

本章我们学习了 Git 的各种"时光机"和"照妖镜"：

| 命令 | 用途 | 记忆口诀 |
|------|------|----------|
| `git log` | 查看提交历史 | 时光机 |
| `git diff` | 对比差异 | 找茬神器 |
| `git show` | 查看单次提交 | 放大镜 |
| `git blame` | 查看每行代码的作者 | 别甩锅 |
| `git bisect` | 二分查找 Bug | 真凶探测器 |

**关键要点：**
1. `git log` 的各种过滤条件可以帮你快速找到需要的提交
2. `git diff` 不仅能看工作区的改动，还能对比任意两个版本
3. `git blame` 是理解代码历史的好帮手，但别用来甩锅
4. `git bisect` 是定位 Bug 的核武器，配合自动化测试效果更佳
5. 图形工具可以作为命令行的补充，让历史更直观

**练习建议：**
1. 在你的项目中运行 `git log --oneline --graph --all`，看看分支图
2. 找一个文件，用 `git blame` 看看每行代码是谁写的
3. 如果有自动化测试，尝试用 `git bisect` 定位一个已知的问题

下一章，我们将学习 Git 的"后悔药"——如何撤销各种操作！
