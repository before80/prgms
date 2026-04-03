+++
title = "第8章：.gitignore —— 眼不见心不烦"
weight = 80
date = 2026-04-03T19:36:48+08:00
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++
# 第8章：.gitignore —— 眼不见心不烦

> 有些东西，看见了就心烦。比如编译生成的文件、依赖目录、配置文件里的密码...Git 很聪明，但它不会读心术，不知道哪些文件不该提交。这时候，`.gitignore` 文件就是你的"黑名单"——告诉 Git：这些文件，请假装看不见。

---

## 8.1 哪些文件不该提交：密码、依赖、编译产物

在把文件加入 Git 之前，先问问自己：这个文件真的需要版本控制吗？有些东西提交上去，轻则污染仓库，重则泄露机密。

### 不该提交的文件类型

**1. 依赖目录**
```
node_modules/      # Node.js 依赖
vendor/            # PHP Composer 依赖
__pycache__/       # Python 缓存
```
- 为什么：依赖可以从 package.json 重新安装，没必要提交
- 后果：仓库体积爆炸，clone 慢到怀疑人生

**2. 编译产物**
```
dist/              # 构建输出
build/             # 编译结果
*.exe              # 可执行文件
*.dll              # 动态链接库
```
- 为什么：源代码才是真理，编译产物随时可生成
- 后果：冲突频发，仓库臃肿

**3. 配置文件（含敏感信息）**
```
.env               # 环境变量
config.local.js    # 本地配置
secrets.json       # 密钥文件
```
- 为什么：包含密码、API 密钥等敏感信息
- 后果：密码泄露，被黑客问候

**4. 日志文件**
```
*.log              # 日志文件
logs/              # 日志目录
npm-debug.log*     # 调试日志
```
- 为什么：日志随时在变化，没必要版本控制
- 后果：无意义的提交记录

**5. 操作系统生成的文件**
```
.DS_Store          # macOS
Thumbs.db          # Windows
desktop.ini        # Windows
```
- 为什么：系统文件，与项目无关
- 后果：跨平台协作时互相干扰

**6. IDE/编辑器配置**
```
.idea/             # JetBrains
.vscode/           # VS Code
*.swp              # Vim 交换文件
```
- 为什么：个人偏好，不应强加给团队
- 后果：每个人的 IDE 配置不同，互相覆盖

### 提交前的检查清单

```bash
# 提交前，先看看会提交什么
git status

# 检查是否有不该提交的文件
git diff --name-only --cached

# 如果发现了不该提交的文件...
git rm --cached 不该提交的文件
echo "不该提交的文件" >> .gitignore
```

---

## 8.2 `node_modules`：永远不要提交的庞然大物

`node_modules` 是 Node.js 项目的依赖目录，它是 Git 仓库的头号公敌。

### 为什么不要提交 node_modules？

**1. 体积巨大**
```bash
# 一个普通的 React 项目
ls -lh node_modules | wc -l
# 输出：3000+ 个文件

du -sh node_modules
# 输出：200M

# 而 package.json 只有 2KB
```

**2. 文件数量爆炸**
```bash
# 有些包会创建深层嵌套的目录
node_modules/a/node_modules/b/node_modules/c/...

# Windows 下路径过长会导致问题
```

**3. 平台差异**
```bash
# 有些包包含平台特定的二进制文件
# macOS 的不能在 Windows 上运行
# 提交上去也没用
```

**4. 可以重建**
```bash
# 只要有 package.json，随时可以重建
npm install
# 或者
yarn install
```

### 正确做法

```bash
# 1. 创建 .gitignore
echo "node_modules/" >> .gitignore

# 2. 从 Git 中移除（如果已经提交了）
git rm -r --cached node_modules

# 3. 提交 .gitignore
git add .gitignore
git commit -m "chore: 忽略 node_modules"

# 4. 提交 package.json（必须！）
git add package.json package-lock.json
git commit -m "chore: 添加依赖配置"
```

### 特殊情况：提交部分依赖

有时候确实需要提交某些依赖：

```bash
# 方法1：使用 npm 的 bundledDependencies
# 在 package.json 中配置

# 方法2：提交特定目录，忽略其他
# .gitignore 内容：
node_modules/*
!node_modules/some-special-package/
```

---

## 8.3 `.env` 文件：你的秘密，别让全世界知道

`.env` 文件用于存储环境变量，通常包含数据库密码、API 密钥等敏感信息。这是**绝对不能提交**的文件。

### 为什么 .env 如此危险？

**真实案例：**
- 2016年，某公司将 AWS 密钥提交到 GitHub，被黑客利用，损失数万美元
- 某开发者将数据库密码提交到公共仓库，数据库被勒索

### 正确的环境变量管理

**1. 创建 .env.example（模板）**
```bash
# .env.example - 提交这个
DATABASE_URL=postgresql://user:password@localhost:5432/mydb
API_KEY=your_api_key_here
SECRET_KEY=your_secret_key_here
```

**2. 创建 .env（真实配置，不提交）**
```bash
# .env - 不提交这个
DATABASE_URL=postgresql://admin:real_password@prod-db:5432/mydb
API_KEY=sk_live_1234567890abcdef
SECRET_KEY=super_secret_key_12345
```

**3. 配置 .gitignore**
```bash
# .gitignore
.env
.env.local
.env.*.local
```

**4. 团队 onboarding 流程**
```bash
# 新成员加入时
cp .env.example .env
# 然后手动填入真实值
```

### 如果已经提交了 .env

```bash
# 1. 立即撤销提交（如果还没 push）
git reset --soft HEAD~1
git rm --cached .env
git commit -m "fix: 移除敏感信息"

# 2. 如果已经 push，需要更复杂的操作
# 见 8.9 节：敏感信息泄露后的紧急处理
```

---

## 8.4 大文件陷阱：Git LFS 处理大文件

Git 不适合管理大文件（>100MB），但有时候确实需要版本控制一些大文件（如图片、视频、二进制资源）。这时候 Git LFS（Large File Storage）登场了。

### 什么是 Git LFS？

**Git LFS** 是 Git 的扩展，它将大文件存储在单独的服务器上，仓库中只保存指向这些文件的指针。

### 安装 Git LFS

```bash
# macOS
brew install git-lfs

# Ubuntu/Debian
sudo apt-get install git-lfs

# Windows
# 下载安装包：https://git-lfs.github.com/

# 初始化
git lfs install
```

### 配置 Git LFS

```bash
# 追踪所有 .psd 文件
git lfs track "*.psd"

# 追踪特定目录
git lfs track "assets/images/*"

# 追踪特定文件
git lfs track "design/mockup.sketch"

# 查看追踪规则
git lfs track
```

这会创建 `.gitattributes` 文件：
```
*.psd filter=lfs diff=lfs merge=lfs -text
assets/images/* filter=lfs diff=lfs merge=lfs -text
```

### 使用 Git LFS

```bash
# 正常使用 git add/commit/push
git add design.psd
git commit -m "add: 添加设计稿"
git push origin main

# 大文件会被自动上传到 LFS 服务器
```

### 迁移现有大文件到 LFS

```bash
# 如果仓库已经有大文件，需要迁移
git lfs migrate import --include="*.psd,*.zip"

# 这会重写历史，需要 force push
git push --force origin main
```

### Git LFS 的替代方案

| 方案 | 适用场景 | 优点 | 缺点 |
|------|----------|------|------|
| Git LFS | 大文件版本控制 | 与 Git 集成好 | 需要额外服务器 |
| 云存储 | 静态资源 | 便宜、快速 | 不在版本控制中 |
| CDN | 分发资源 | 全球加速 | 只读 |
| 专用资产管理 | 游戏/设计资源 | 专业功能 | 额外工具 |

---

## 8.5 .gitignore 语法：从入门到精通

`.gitignore` 文件使用特定的模式匹配语法，掌握这些语法，你可以精确控制哪些文件被忽略。

### 基础语法

```bash
# 注释以 # 开头
# 这是注释

# 忽略特定文件
secret.txt

# 忽略特定目录
node_modules/

# 使用通配符
*.log          # 忽略所有 .log 文件
*.tmp          # 忽略所有 .tmp 文件

# 忽略特定类型的文件
build/         # 忽略 build 目录（包括子目录中的）
/build         # 只忽略根目录的 build 目录
```

### 通配符规则

| 通配符 | 含义 | 示例 |
|--------|------|------|
| `*` | 匹配任意字符（除 /） | `*.log` 匹配 a.log, b.log |
| `?` | 匹配单个字符 | `?.txt` 匹配 a.txt, b.txt |
| `**` | 匹配任意目录 | `**/temp` 匹配所有 temp 目录 |
| `[abc]` | 匹配括号内任一字符 | `[ab].txt` 匹配 a.txt, b.txt |
| `[0-9]` | 匹配范围 | `file[0-9].txt` 匹配 file1.txt |
| `!` | 取反（不忽略） | `!important.log` |

### 高级用法

```bash
# 忽略所有 .txt 文件，但不忽略 readme.txt
*.txt
!readme.txt

# 忽略所有 .log 文件，但不忽略 keep/ 目录下的
*.log
!keep/*.log

# 忽略所有 .log 文件，但不忽略 keep/ 及其子目录下的
*.log
!keep/

# 忽略 build 目录，但不忽略 build/important.js
build/
!build/important.js
# 注意：这样写不生效，因为 build/ 已经忽略了整个目录
# 正确写法：
build/*
!build/important.js

# 忽略 temp 目录及其所有内容
temp/

# 只忽略根目录的 temp 目录
/temp/

# 忽略所有名为 temp 的目录
**/temp/
```

### 双星号 `**` 的用法

```bash
# 匹配任意层级的目录
**/node_modules/     # 匹配任何位置的 node_modules

# 匹配特定模式
**/*.min.js         # 匹配任何位置的 .min.js 文件

# 匹配特定路径
**/build/output/    # 匹配任何 build/output 目录
```

### 注释和空行

```bash
# 这是注释

# 空行会被忽略

# 可以用反斜杠转义特殊字符
\#not-a-comment.txt  # 忽略名为 "#not-a-comment.txt" 的文件
\!important.txt      # 忽略名为 "!important.txt" 的文件
```

---

## 8.6 常用模板：Node.js、Python、Java、Go、Rust 一键复制

不同技术栈有不同的忽略模式。以下是常用模板，直接复制粘贴即可。

### Node.js 项目

```gitignore
# Dependencies
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Production build
dist/
build/

# Environment variables
.env
.env.local
.env.*.local

# IDE
.idea/
.vscode/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Testing
coverage/
.nyc_output/

# Logs
logs/
*.log
```

### Python 项目

```gitignore
# Byte-compiled
__pycache__/
*.py[cod]
*$py.class

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
ENV/
env/
.venv

# IDE
.idea/
.vscode/
*.swp

# Environment variables
.env
.env.local

# Testing
.pytest_cache/
.coverage
htmlcov/

# OS
.DS_Store
Thumbs.db
```

### Java 项目

```gitignore
# Compiled class files
*.class

# Package files
*.jar
*.war
*.ear

# Maven
target/
pom.xml.tag
pom.xml.releaseBackup
pom.xml.versionsBackup
pom.xml.next
release.properties

# Gradle
.gradle/
build/

# IDE
.idea/
*.iml
*.ipr
*.iws
.classpath
.project
.settings/

# OS
.DS_Store
Thumbs.db
```

### Go 项目

```gitignore
# Binaries for programs and plugins
*.exe
*.exe~
*.dll
*.so
*.dylib

# Test binary, built with `go test -c`
*.test

# Output of the go coverage tool
*.out

# Dependency directories
vendor/

# Go workspace file
go.work

# IDE
.idea/
.vscode/
*.swp

# OS
.DS_Store
Thumbs.db
```

### Rust 项目

```gitignore
# Build output
/target/

# Cargo
Cargo.lock

# IDE
.idea/
.vscode/
*.swp

# OS
.DS_Store
Thumbs.db
```

### 通用模板

```gitignore
# IDE
.idea/
.vscode/
*.swp
*.swo
*~

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Logs
*.log
logs/

# Environment variables
.env
.env.local
.env.*.local

# Temporary files
*.tmp
*.temp
tmp/
temp/
```

### 获取官方模板

GitHub 维护了各种语言的官方 .gitignore 模板：

```bash
# 方法1：直接下载
# 访问 https://github.com/github/gitignore

# 方法2：使用 gibo 工具
# 安装 gibo
brew install gibo  # macOS

# 使用
gibo Node Python macOS >> .gitignore
```

---

## 8.7 已提交的文件怎么忽略？`git rm --cached`

文件已经提交了，现在想把它加入 .gitignore，该怎么做？直接加 .gitignore 是不够的，因为 Git 已经在追踪这个文件了。

### 问题现象

```bash
# 1. 添加 .gitignore
echo "config.local.js" >> .gitignore

# 2. 修改 config.local.js
# ...

# 3. 查看状态
git status
# Changes not staged for commit:
#   modified:   config.local.js

# 文件仍然在追踪！
```

### 解决方案

```bash
# 1. 停止追踪文件，但保留本地文件
git rm --cached config.local.js

# 2. 提交 .gitignore 和停止追踪的操作
git add .gitignore
git add config.local.js  # 这会记录 "删除" 操作
git commit -m "chore: 停止追踪 config.local.js，添加到 .gitignore"

# 3. 之后 config.local.js 的改动会被忽略
```

### 详细解释

```bash
# git rm --cached 做了什么？

# 执行前：
仓库：包含 config.local.js
暂存区：包含 config.local.js
工作区：包含 config.local.js

# 执行 git rm --cached 后：
仓库：包含 config.local.js（历史记录还在）
暂存区：标记为删除（下次提交会删除）
工作区：config.local.js 还在（保留本地文件）

# 提交后：
仓库：config.local.js 被删除（不再追踪）
暂存区：空
工作区：config.local.js 还在
```

### 批量处理

```bash
# 停止追踪所有 .log 文件
git rm --cached *.log

# 停止追踪整个目录
git rm -r --cached logs/

# 提交更改
git commit -m "chore: 停止追踪日志文件"
```

### 注意事项

**1. 团队协作时通知大家**
```bash
# 停止追踪配置文件后，其他开发者需要重新创建这个文件
# 最好提供模板：
cp config.local.js.example config.local.js
```

**2. 历史记录还在**
```bash
# git rm --cached 只是停止追踪，历史记录中仍有该文件
# 如果文件包含敏感信息，需要更彻底的处理（见 8.9 节）
```

---

## 8.8 全局 .gitignore：一次配置，所有项目生效

每个项目都有 `.gitignore`，但有些忽略规则是通用的（如 IDE 配置、OS 文件）。你可以配置全局 `.gitignore`，让所有项目自动生效。

### 配置全局 .gitignore

```bash
# 1. 创建全局 .gitignore 文件
touch ~/.gitignore_global

# 2. 配置 Git 使用它
git config --global core.excludesfile ~/.gitignore_global

# 3. 编辑全局 .gitignore
vim ~/.gitignore_global
```

### 推荐的全局配置

```gitignore
# IDE
.idea/
.vscode/
*.swp
*.swo
*~

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Editor
*.sublime-project
*.sublime-workspace
```

### 优先级规则

Git 按以下顺序应用忽略规则（后面的覆盖前面的）：

1. **系统级**（很少用）
2. **全局**（`core.excludesfile`）
3. **项目级**（`.gitignore`）
4. **子目录**（子目录的 `.gitignore`）

### 查看配置

```bash
# 查看全局 .gitignore 路径
git config --global core.excludesfile

# 查看所有生效的忽略规则
git check-ignore -v filename
```

---

## 8.9 .gitignore 失效排查：为什么还是提交了？

有时候明明配置了 .gitignore，文件还是被提交了。这是怎么回事？

### 常见原因1：文件已被追踪

```bash
# 问题：文件已经在 Git 中，.gitignore 对追踪的文件无效

# 解决：停止追踪
git rm --cached 文件
git commit -m "停止追踪文件"
```

### 常见原因2：规则写错了

```bash
# 错误：缺少斜杠
node_modules    # 只忽略文件名为 node_modules 的文件
node_modules/   # 正确：忽略 node_modules 目录

# 错误：多余的斜杠
/build/         # 只忽略根目录的 build
build/          # 忽略任何位置的 build 目录

# 错误：模式不匹配
*.js.log        # 匹配 a.js.log
*.log           # 不匹配 a.js.log
```

### 常见原因3：规则被后面的覆盖

```bash
# .gitignore
*.log           # 忽略所有 .log 文件
!important.log  # 不忽略 important.log
app.log         # 这行无效！因为 important.log 已经匹配了 *.log

# 正确写法：
*.log
!important.log
!app.log         # 要放在后面
```

### 常见原因4：缓存未刷新

```bash
# 有时候 Git 缓存了忽略规则

# 清除缓存，重新应用 .gitignore
git rm -r --cached .
git add .
git commit -m "刷新 .gitignore"
```

### 调试 .gitignore

```bash
# 检查某个文件为什么被忽略/没被忽略
git check-ignore -v 文件路径

# 示例输出（被忽略）：
# .gitignore:3:*.log    app.log
# 表示：.gitignore 第 3 行的 *.log 规则忽略了 app.log

# 示例输出（没被忽略）：
# （无输出）
```

### 检查清单

- [ ] 文件是否已被追踪？（`git ls-files | grep 文件名`）
- [ ] 规则语法是否正确？
- [ ] 是否有取反规则（`!`）覆盖了前面的规则？
- [ ] 路径是否正确（是否以 `/` 开头）？
- [ ] 是否需要清除缓存？

---

## 8.10 本章小结：提交前检查，别做那个泄露密码的人

本章我们学习了 `.gitignore` 的各种知识：

| 主题 | 要点 |
|------|------|
| 不该提交的文件 | 依赖、编译产物、配置文件、日志、OS/IDE 文件 |
| node_modules | 永远不要提交，用 package.json 重建 |
| .env 文件 | 包含敏感信息，绝对不能提交 |
| Git LFS | 管理大文件的解决方案 |
| 语法 | `*` `?` `**` `!` 等通配符的用法 |
| 模板 | 各语言有官方模板，可以直接使用 |
| 停止追踪 | 用 `git rm --cached` |
| 全局配置 | `core.excludesfile` 配置全局 .gitignore |
| 失效排查 | 用 `git check-ignore -v` 调试 |

**安全原则：**
1. **提交前检查**：`git status` 看看会提交什么
2. **敏感信息绝不提交**：密码、密钥、token
3. **提供模板**：用 `.env.example` 代替 `.env`
4. **定期审计**：检查仓库是否包含敏感信息

**记忆口诀：**
- 依赖目录 → 忽略
- 编译产物 → 忽略
- 配置文件 → 忽略
- 日志文件 → 忽略
- OS/IDE 文件 → 忽略

**练习建议：**
1. 检查你的项目，看看 .gitignore 是否完整
2. 使用 `git check-ignore -v` 调试几个文件
3. 配置全局 .gitignore，管理 IDE 和 OS 文件

下一章，我们将进入 Git 的核心特性——分支管理！
