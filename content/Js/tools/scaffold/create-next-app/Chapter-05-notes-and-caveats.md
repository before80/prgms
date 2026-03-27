
+++
title = "第5章   Create Next App注意事项"
weight = 50
date = "2026-03-27T21:12:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 第五章 · 注意事项

> "学开车不难，难的是知道什么时候该踩刹车。"
> 同样地，用 create-next-app 创建一个 Next.js 项目不难，
> 难的是知道创建之后要注意什么。
> 这一章，我们就来聊聊那些「哦，原来如此」的时刻。

---

## 5.1 版本与兼容性

> 你有没有遇到过这种情况：兴冲冲地打开了教程，准备大干一场，
> 结果一个「Node.js 版本不对」的报错，让你当场石化在原地？
> 别担心，你不是一个人——这是 Next.js 新手村出镜率最高的 Bug 之一。
> 在开始之前，让我们先把这个「拦路虎」给收拾了。

### 5.1.1 Node.js 版本要求

**Node.js** 是什么？简单来说，它是一个运行 JavaScript 代码的环境。
你可以把它想象成 JavaScript 的「超级英雄变身器」——没有它，你的 JavaScript 代码只能在浏览器里小打小闹；
有了它，你的 JavaScript 就能上天入地、读写文件、连接数据库，甚至给你煮咖啡（如果硬件允许的话）。

Next.js 14 及以上版本，要求 **Node.js 18.17.0 或更高版本**。
为什么是 18？因为 Next.js 使用了一些比较新的 JavaScript 特性，
而这些特性需要较新版本的 Node.js 才能支持。就像你不能指望用 iPhone 4 来运行 iOS 17一样，
旧版本的 Node.js 也带不动新版本的 Next.js。

如何检查你的 Node.js 版本？

```bash
node --version
```

如果输出的版本号低于 18.17.0，那就意味着你该升级了。升级 Node.js 的方法有很多种：

- **手动下载**：去 Node.js 官网（https://nodejs.org）下载最新 LTS 版本，然后像安装普通软件一样一路「下一步」。
- **使用 nvm（Node Version Manager）**：这是一个专门管理 Node.js 版本的工具，有了它，你可以在不同版本之间自由切换，就像换衣服一样方便。
- **使用 nvm-windows**：如果你在 Windows 上，那 nvm-windows 就是你的好帮手（注意，nvm-windows 和 macOS/Linux 上的 nvm 不是同一个项目，但功能类似）。

```bash
# 使用 nvm 安装 Node.js 18（如果你已经安装了 nvm）
nvm install 18
nvm use 18

# 检查版本，确认升级成功
node --version  # 输出：v18.17.0 或更高版本
npm --version   # 检查 npm 版本（通常是随 Node.js 一起安装的）
```

> 💡 **温馨提示**：如果你使用的是公司的老旧项目，可能需要维护旧版本的 Node.js。这种情况下，nvm 就派上大用场了——你可以同时安装多个版本的 Node.js，需要哪个项目就用哪个版本，互不干扰，堪称「版本管理界的瑞士军刀」。

### 5.1.2 create-next-app 版本号与 Next.js 版本号对应关系

create-next-app 和 Next.js 是「秤不离砣」的关系。
每次 create-next-app 发布新版本，它打包的 Next.js 版本也会相应更新。

简单来说：

| create-next-app 版本 | Next.js 版本 | 说明 |
|---------------------|-------------|------|
| 14.x.x | Next.js 14.x | 当前主流版本，稳定可靠 |
| 13.x.x | Next.js 13.x | 上一代版本，已引入 App Router |
| 12.x.x | Next.js 12.x | 较老版本，主要使用 Pages Router |

为什么会这样？因为 create-next-app 本质上是一个「脚手架工具」，
它的主要任务就是帮你创建一个包含正确依赖和配置的 Next.js 项目。
所以当 Next.js 发布新版本时，create-next-app 也需要更新，
以便它能创建出基于新版本的项目。

```bash
# 查看当前使用的 create-next-app 版本
npx create-next-app --version

# 查看当前项目的 Next.js 版本
cat package.json | grep next
```

> 📝 **小知识**：create-next-app 的版本号和 Next.js 的版本号通常是对齐的，
> 但这并不意味着 create-next-app 本身有什么复杂的功能。
> 它的主要工作就是「生成文件」，所以版本对齐更多是为了方便管理。
> 你可以把 create-next-app 想象成一个「模具制造机」，
> 它会根据你指定的 Next.js 版本，生产出相应配置的「模具」（项目结构）。

### 5.1.3 如何指定特定版本

有时候，你可能需要使用特定版本的 Next.js，而不是最新的稳定版。
比如：

- 你的公司项目还在使用 Next.js 13，你不想升级
- 你想体验还没正式发布的新功能（canary 版本）
- 你在排查一个特定版本才有的 bug

这时候，你就需要知道如何指定版本了。

```bash
# 使用最新的稳定版（默认行为）
npx create-next-app@latest my-project

# 指定 Next.js 14.x 版本
npx create-next-app@14 my-project

# 指定 Next.js 13.x 版本
npx create-next-app@13 my-project

# 使用 canary 版本（最新开发版，可能不稳定）
npx create-next-app@canary my-project

# 指定具体版本号
npx create-next-app@14.0.0 my-project
```

其中：

- **`@latest`**：最新稳定版，这是默认选项，适合大多数项目
- **`@14`**：指定主版本号，会安装该主版本下的最新稳定版（14.x.y 中的最新版本）
- **`@canary`**：canary 版本是每日构建的开发版，包含最新的实验性功能。
  适合那些「喜欢冒险」的开发者，但**不建议**在生产环境使用。
  想象一下，canary 就是「煤矿里的金丝雀」——它能提前告诉你前方是否有危险。

```bash
# 如果你想指定具体的小版本号（比如你想复现一个 14.0.0 的 bug）
npx create-next-app@14.0.0 my-bug-reproduction-project

# 如果你想用 Next.js 15 的 canary 版本来尝鲜
npx create-next-app@canary my-next15-preview
```

> ⚠️ **警告**：canary 版本可能会遇到各种奇奇怪怪的问题，比如功能突然被移除、
> API 发生 breaking change、甚至你的电脑突然开始播放诡异的音乐（好吧，最后一条不太可能）。
> 总之，在生产环境，请务必使用稳定版。

### 5.1.4 npm / yarn / pnpm 版本对依赖安装的影响

**npm**、**yarn**、**pnpm** 都是 JavaScript 的包管理器，
你可以把它们想象成「应用商店」——只不过它们管理的是代码库和依赖包，而不是手机 App。

- **npm**：Node.js 自带的包管理器，历史悠久，用户基数大。
  它的标志是一只小盒子（官方 logo 是一只放东西的箱子）。
- **yarn**：Facebook 出品的包管理器，曾经是 npm 的强力挑战者。
  它的特点是速度快、支持离线安装、而且安装过程更加「优雅」。
- **pnpm**：新一代的包管理器，它使用了「硬链接」和「符号链接」的黑科技，
  能够极大地节省磁盘空间，而且安装速度飞快。
  它的名字是「performant npm」的缩写，意为「高性能的 npm」。

create-next-app 支持这三种包管理器。你可以在创建项目时通过 `--use-npm`、
`--use-yarn` 或 `--use-pnpm` 参数来指定使用哪个。

```bash
# 使用 npm（默认）
npx create-next-app my-project --use-npm

# 使用 yarn
npx create-next-app my-project --use-yarn

# 使用 pnpm
npx create-next-app my-project --use-pnpm
```

不过，有一个重要的事情需要提醒：不同的包管理器安装的依赖可能会有细微差异。
这是因为它们在处理依赖版本、目录结构、以及锁文件格式上有一些不同。
如果你在团队中工作，**务必确保所有成员使用相同的包管理器**。
否则，可能会出现「在我电脑上明明好好的，在你电脑上就不行了」的经典剧情。

```bash
# 检查你当前的包管理器版本
npm --version   # npm 的版本
yarn --version  # yarn 的版本
pnpm --version  # pnpm 的版本

# 如果你想切换包管理器，建议先删除 node_modules 和锁文件，然后重新安装
rm -rf node_modules package-lock.json  # npm 的锁文件
rm -rf node_modules yarn.lock         # yarn 的锁文件
rm -rf node_modules pnpm-lock.yaml    # pnpm 的锁文件
```

> 📝 **小知识**：为什么 pnpm 能节省磁盘空间？因为它使用了「pnpm store」。
> 所有安装的包都被存储在一个全局目录下，然后通过硬链接或符号链接的方式被项目引用。
> 打个比方：如果 npm 和 yarn 是每次都复印一本书给不同的项目，
> 那么 pnpm 就是建立了一个「图书馆」，所有项目都来借阅同一本书。
> 这样一来，磁盘空间自然就省下来了。
>
> 💡 **额外提示**：`next-env.d.ts` 文件是 Next.js 自动生成的，**请不要手动创建或修改它**。
> 每当你运行 `npm run dev` 或 `npm run build` 时，Next.js 会重新生成这个文件。
> 如果你删除了它，Next.js 会自动重新创建。

---

## 5.2 创建时的常见问题

> 创建项目的时候，总会遇到一些意想不到的「惊喜」。
> 有时候是目录已经存在，有时候是网络抽风，有时候是磁盘突然喊「我满了」。
> 这一节，我们就来聊聊这些常见问题，以及如何优雅地解决它们。

### 5.2.1 目标目录已存在

当你兴冲冲地执行 `npx create-next-app my-project` 时，
如果 `my-project` 目录已经存在，create-next-app 会毫不客气地报错并拒绝工作。
这是因为它不想覆盖你已有的文件，怕把你的心血结晶给弄丢了。

错误信息通常长这样：

```bash
Error: Target directory is not empty. Please specify an empty directory or use the --force flag.
```

翻译成人话就是：「这个目录不是空的，你得给我一个空目录，
或者加个 `--force` 参数让我强制覆盖。」

解决方案：

```bash
# 方案一：换一个空的目录名
npx create-next-app my-fresh-project

# 方案二：先删除已有目录，然后重新创建
rm -rf my-project
npx create-next-app my-project

# 方案三：手动清空目录中的文件（更安全的做法）
cd my-project
rm -rf *  # 删除目录内所有文件（但保留目录本身）
npx create-next-app .  # 在当前空目录创建项目
```

> ⚠️ **友情提示**：方案三的 `--force` 参数会直接覆盖已有目录，
> 如果你之前在这个目录里有什么重要的文件，那就全没了。
> 所以在使用之前，请务必确认目录里的文件都是可以丢弃的。
> **重要的事情说三遍：备份！备份！备份！**

### 5.2.2 网络问题导致依赖下载失败

在中国大陆访问 npm 的官方源，有时候会慢得像蜗牛爬树，
甚至完全无法连接。这时候，依赖下载就会失败，错误信息可能长这样：

```bash
npm ERR! network ETIMEDOUT 104.16.17.35:443
npm ERR! network This is a problem related to network connectivity.
```

翻译成人话就是：「网络连接超时了，我找不到服务器，请检查你的网络。」

解决方案：配置国内镜像源。国内常用的 npm 镜像源有：

- 淘宝镜像：https://registry.npmmirror.com
- 腾讯云镜像：https://mirrors.cloud.tencent.com/npm/
- 华为云镜像：https://repo.huaweicloud.com/repository/npm/

```bash
# 设置淘宝镜像（推荐，速度快，稳定性好）
npm config set registry https://registry.npmmirror.com

# 验证设置是否成功
npm config get registry
# 输出：https://registry.npmmirror.com

# 注意：create-next-app 不支持 --registry 参数
# 如果 npm 安装缓慢，请先执行上面的 npm config set registry
# 然后再运行 create-next-app
```

如果你使用的是 yarn 或 pnpm，也有对应的配置方法：

```bash
# yarn 配置镜像源
yarn config set registry https://registry.npmmirror.com

# pnpm 配置镜像源
pnpm config set registry https://registry.npmmirror.com
```

> 💡 **温馨提示**：淘宝镜像的同步频率大约是每 10 分钟一次，
> 所以有时候最新的包可能还没来得及同步过去。
> 如果你需要最新版本的包，可能需要切换回官方源。
> 另外，如果你发现自己下载的包版本不对，可以先检查一下镜像源是否同步了最新版本。

### 5.2.3 磁盘空间不足

这可能是最让人哭笑不得的问题了。
当你看到「No space left on device」这样的错误时，
就知道你的硬盘已经「弹尽粮绝」了。

```bash
Error: ENOSPC: no space left on device, write
```

翻译成人话就是：「磁盘满了，写不进去了，
要不你先删点东西？」

解决方案：

```bash
# 首先检查磁盘空间
df -h  # Linux/macOS
# 或
wmic logicaldisk get size,freespace,caption  # Windows

# 清理 npm/yarn/pnpm 的缓存
npm cache clean --force
yarn cache clean
pnpm store prune

# 删除不需要的大文件，比如：
# - node_modules（如果之前有安装过其他项目）
# - 各种临时文件
# - 旧的下载文件
```

> 📝 **小知识**：npm、yarn、pnpm 都会缓存下载过的包，
> 以便下次安装时加快速度。但是，随着时间的推移，
> 这个缓存目录可能会变得越来越大，像一只贪吃蛇一样吞噬你的磁盘空间。
> 所以，定期清理缓存是一个好习惯。
> 另外，如果你使用的是 pnpm，它的存储机制本身就比 npm 和 yarn 节省空间，
> 所以如果你经常受磁盘空间困扰，可以考虑切换到 pnpm。

### 5.2.4 权限错误

在 Linux、macOS 或 WSL（Windows Subsystem for Linux）环境下，
有时候会因为权限问题导致依赖安装失败。
错误信息可能长这样：

```bash
npm ERR! Error: EACCES: permission denied, access '/usr/local/lib/node_modules'
```

翻译成人话就是：「权限不够，我进不去这个目录，
你是不是没有管理员权限？」

解决方案：

```bash
# 方案一：使用 sudo 提升权限（不推荐长期使用）
sudo npx create-next-app my-project

# 方案二：配置 npm 的全局目录到用户目录（推荐）
mkdir ~/.npm-global  # 创建一个用户目录用于存放全局包
npm config set prefix '~/.npm-global'  # 设置 npm 的全局目录

# 将路径添加到 PATH 环境变量（编辑 ~/.bashrc 或 ~/.zshrc）
export PATH=~/.npm-global/bin:$PATH

# 使配置生效
source ~/.bashrc  # 如果你使用的是 bash
# 或
source ~/.zshrc   # 如果你使用的是 zsh

# 方案三：在 WSL 中，确保 Windows 磁盘挂载的目录有正确权限
# WSL 访问 Windows 磁盘文件时，可能会有权限问题
# 建议在 WSL 的本地文件系统中创建项目，而不是在 /mnt/c/ 下
cd ~  # 切换到 WSL 的主目录
mkdir projects
cd projects
npx create-next-app my-project
```

> ⚠️ **友情提示**：使用 `sudo` 来安装全局包虽然方便，但可能会带来安全隐患。
> 因为 `sudo` 意味着以管理员权限运行，任何代码都能获得最高权限。
> 如果你安装的某个包包含恶意代码，后果不堪设想。
> 所以，建议使用方案二，将 npm 的全局目录配置到用户目录下，
> 这样就不需要管理员权限了。

### 5.2.5 Windows 路径问题

Windows 的路径格式和 Unix（Linux/macOS）不一样。
Windows 使用反斜杠 `\` 作为路径分隔符，而 Unix 使用正斜杠 `/`。
这看起来是个小差异，但有时候会引发大问题。

```bash
# Windows 风格路径
C:\Users\longx\Projects\my-app

# Unix 风格路径
/home/longx/projects/my-app
```

此外，Windows 的命令行工具（CMD、PowerShell）和 Unix 的 shell（bash、zsh）
也有很多差异。如果你是一个 Windows 用户，我们**强烈推荐**你使用以下方案之一：

**方案一：使用 PowerShell 7+**

PowerShell 7 是 PowerShell 的最新版本，它在性能和兼容性上都有很大提升。
你可以在 Microsoft Store 或 GitHub 上下载安装。

**方案二：使用 WSL2（Windows Subsystem for Linux 2）**

WSL2 让你可以在 Windows 里跑一个真正的 Linux 内核，
这样你就能使用 Linux 的工具链，同时还能访问 Windows 的文件。
简直是「鱼和熊掌兼得」的完美方案。

```powershell
# 在 PowerShell 中创建项目（确保使用 PowerShell 7+）
npx create-next-app my-project

# 使用 WSL2（推荐）
# 首先打开 WSL2 终端
wsl  # 进入默认的 WSL 发行版
cd ~/projects  # 进入 Linux 主目录
npx create-next-app my-project  # 创建项目
```

```bash
# 在 WSL2 中，你还可以访问 Windows 的磁盘
cd /mnt/c/Users/longx/Projects  # 访问 Windows 的用户目录
# 但是，建议还是在 WSL2 的本地目录下工作，这样速度更快
cd ~/projects
npx create-next-app my-project
```

> 💡 **温馨提示**：如果你使用的是 VS Code，配合 WSL2 使用会有绝佳体验。
> 你只需要在 WSL2 终端中输入 `code .`，VS Code 就会自动打开并连接到 WSL2 环境。
> 你甚至可以在 VS Code 的左下角看到当前连接的是 WSL2。
> 这种「Windows 外观 + Linux 内心」的双重享受，你值得拥有。

---

## 5.3 创建后必做事项

> 恭喜你！你的第一个 Next.js 项目已经创建成功了。
> 但是，等等！在庆祝之前，还有一些事情需要你马上去做。
> 这些事情就像是「新房装修后的验收」——看似简单，但至关重要。

### 5.3.1 立即初始化 Git 仓库

**Git** 是什么？Git 是一个版本控制系统，
你可以把它想象成一个「时光机」——它能记录你的每一次修改，
让你可以随时回到过去的某个版本。
没有了 Git，你的代码就像是没有存档的游戏——
一旦改坏了，就只能欲哭无泪地看着屏幕发呆。

在你开始写代码之前，第一件事就是要初始化 Git 仓库：

```bash
# 进入项目目录
cd my-project

# 初始化 Git 仓库（这会创建一个 .git 目录，用于存储版本信息）
git init

# 查看当前状态
git status
# 输出：
# On branch main
# No commits yet
# Untracked files:
#   (use "git add <file>..." to include in what will be committed)
#   .eslintrc.json
#   .gitignore
#   .next/
#   package-lock.json
#   package.json
#   ...
```

> 📝 **小知识**：为什么要在写代码之前就初始化 Git？
> 因为 Git 会跟踪所有的文件变更。
> 如果你先写了很多代码，然后再初始化 Git，Git 就会把所有的文件都标记为「新增」，
> 你就看不到之前的修改历史了。
> 所以，养成「创建项目 -> 初始化 Git -> 开始写代码」的好习惯，会让你的开发工作更加有条不紊。

### 5.3.2 确认 .gitignore 已生成且包含 node_modules、.env.local

**`.gitignore`** 文件是什么？顾名思义，它就是告诉 Git「忽略」哪些文件的配置文件。
你肯定不想把 `node_modules`（成千上万的依赖包）提交到代码仓库，
那样会让仓库变得巨大无比，每次 clone 都要下载半天。

create-next-app 在创建项目时，会自动生成一个 `.gitignore` 文件，
里面已经包含了常见的需要忽略的文件和目录。

```bash
# 查看 .gitignore 文件的内容
cat .gitignore

# 输出示例：
# dependencies
# /node_modules
# /.pnp
# .pnp.js

# testing
# /coverage

# Next.js
# /.next/
# /out/

# production
# /build

# misc
# .DS_Store
# *.pem

# debug
# npm-debug.log*
# yarn-debug.log*
# yarn-error.log*

# local env files
# .env*.local
# .env

# vercel
# .vercel

# typescript
# *.tsbuildinfo
# next-env.d.ts
```

你应该确保 `.gitignore` 文件包含以下关键条目：

- **`node_modules`**：依赖包目录，体积巨大（通常有几百 MB 到几 GB）
- **`.env.local`**：包含敏感信息的本地环境变量文件，比如数据库密码、API 密钥等
- **`.next`**：Next.js 的构建产物目录，下次构建会重新生成
- **`package-lock.json`** 或 **`pnpm-lock.yaml`**：锁文件（这个有争议，有些项目会提交锁文件）

> ⚠️ **特别提醒**：`.env.local` 文件通常包含敏感信息，比如：
>
> ```
> DATABASE_URL=postgres://user:password@localhost:5432/mydb
> API_SECRET_KEY=sk-1234567890abcdef
> ```
>
> 如果你不小心把 `.env.local` 提交到了 GitHub，
> 全世界的黑客都会知道你的数据库密码和 API 密钥。
> 然后你的账户可能会被用来挖矿、发送垃圾邮件，
> 或者做一些更糟糕的事情。
> 所以，**永远不要把 `.env.local` 提交到版本库**！

### 5.3.3 确认 package.json 中的 scripts 和依赖版本

**`package.json`** 是 Node.js 项目的核心配置文件，
它记录了项目的基本信息、依赖列表、以及可执行的脚本命令。

```bash
# 查看 package.json 文件的内容
cat package.json
```

```json
{
  "name": "my-project",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint"
  },
  "dependencies": {
    "next": "14.2.5",
    "react": "^18.3.1",
    "react-dom": "^18.3.1"
  },
  "devDependencies": {
    "@types/node": "^20",
    "@types/react": "^18",
    "@types/react-dom": "^18",
    "eslint": "^8",
    "eslint-config-next": "14.2.5",
    "postcss": "^8",
    "tailwindcss": "^3.4.1",
    "typescript": "^5"
  }
}
```

解释一下各个字段：

- **`scripts`**：定义了你可以在终端中运行的命令
  - `npm run dev`：启动开发服务器
  - `npm run build`：构建生产版本
  - `npm run start`：启动生产服务器
  - `npm run lint`：运行代码检查
- **`dependencies`**：生产环境依赖，项目运行时必需的包
- **`devDependencies`**：开发环境依赖，仅在开发时使用的工具

你应该检查以下几点：

1. **scripts 是否完整**：确保有 `dev`、`build`、`start` 这些常用脚本。如果少了 `lint`，那可要小心了——你的代码风格可能会像脱缰的野马一样放飞自我。
2. **依赖版本是否合理**：特别是 `next` 的版本，是否符合你的预期。看到 `^` 或 `~` 开头的版本号了吗？它们可不是什么密码，而是 npm 的「版本范围魔法」。
3. **是否有缺失的依赖**：如果某些你需要的包没有安装，需要手动添加。

> 💡 **温馨提示**：如果你发现某个依赖的版本号前面有 `^`（比如 `"^18.3.1"`），
> 这意味着 npm 安装时会使用「兼容的最新版本」。
> 具体来说，`^18.3.1` 表示可以安装 18.3.1 到 18.x.x 之间的最新版本，
> 但不会安装 19.0.0 或更高版本。
> 这种方式的好处是可以自动获取 bug 修复和安全更新，
> 坏处是可能会引入一些意外的变化。
> 如果你想锁定精确版本，去掉 `^` 符号即可。

### 5.3.4 首次运行 npm run dev 检查是否正常启动

这是你最不应该跳过的一步！
在你开始写代码之前，先确保开发服务器能正常启动。
如果现在就出问题，至少你知道是新项目的问题，
而不是你之后写的代码导致的。

```bash
# 进入项目目录
cd my-project

# 安装依赖
npm install
# 输出示例：
# added 312 packages in 5s
# 245 packages are looking for funding
#   run `npm fund` for details

# 启动开发服务器
npm run dev
# 输出示例：
#   ▲ Next.js 14.2.5
#   - Local:        http://localhost:3000
#   - Ready in  1.2s
```

然后，打开浏览器，访问 http://localhost:3000。
如果你看到了 Next.js 的默认页面（一个带有「Welcome to Next.js!」的页面），
那么恭喜你，一切正常！

如果你看到了错误信息，那就要仔细阅读错误内容了。
常见的问题包括：

- **端口被占用**：如果 3000 端口已经被其他程序占用，Next.js 会尝试使用 3001 端口
- **依赖缺失**：某些依赖可能没有安装成功
- **配置错误**：可能是 `.eslintrc.json` 或 `next.config.js` 有语法错误

```bash
# 如果你想使用其他端口，可以这样：
npm run dev -- --port 3005
# 输出：
#   ▲ Next.js 14.2.5
#   - Local:        http://localhost:3005
#   - Ready in  1.2s
```

> 🎉 **庆祝时刻**：当你看到「Ready in 1.2s」这样的字样时，
> 意味着你的 Next.js 项目已经成功启动了。
> 此时此刻，你已经完成了一个前端工程师最基本的操作：
> 创建项目、配置环境、启动服务器。
> 给自己鼓个掌吧！你已经迈出了重要的一步！

---

## 5.4 App Router 与 Pages Router 的选择

> 这是你面临的第一个重大抉择：App Router 还是 Pages Router？
> 这个问题，几乎每个 Next.js 新手都会纠结。
> 让我们来详细分析一下，帮助你做出正确的选择。

首先，让我用一个图来解释 Next.js 的两种路由架构：

```mermaid
graph TB
    subgraph "Pages Router（传统方式）"
        P1["pages/"]
        P2["pages/index.tsx"]
        P3["pages/about.tsx"]
        P4["pages/blog/[id].tsx"]
    end

    subgraph "App Router（新方式）"
        A1["app/"]
        A2["app/page.tsx"]
        A3["app/about/page.tsx"]
        A4["app/blog/[id]/page.tsx"]
        A5["app/layout.tsx"]
        A6["app/template.tsx"]
    end

    style P1 fill:#f5f5f5,stroke:#999,stroke-width:2px
    style A1 fill:#e6f7ff,stroke:#1890ff,stroke-width:2px
```

### 5.4.1 App Router（--app）：Next.js 13+ 默认，代表未来方向

**App Router** 是 Next.js 13 引入的新一代路由系统，
也是 Next.js 团队官方推荐的方式。
你可以把它想象成一次「全面升级」——不仅有更强大的功能，
还有更优雅的 API 设计。
如果说 Pages Router 是「功能机」，那 App Router 就是「智能手机」——
不是不能打电话了，而是时代变了，该升级了。

App Router 的主要特点：

1. **基于文件夹的路由**：你只需要创建一个文件夹和 `page.tsx` 文件，路由就自动生成了
2. **React Server Components（RSC）**：默认情况下，组件是服务端的，这意味着它们可以在服务器上运行，减少客户端的 JavaScript 体积
3. **嵌套布局**：可以轻松创建嵌套的布局结构，比如博客列表页和博客详情页共享一个侧边栏
4. **加载状态（loading.tsx）**：可以优雅地处理加载状态，而不需要手动管理
5. **错误边界（error.tsx）**：可以捕获子路由的错误，并显示友好的错误页面

```bash
# 使用 App Router（默认方式）
npx create-next-app my-app-router-project --app
# 或者不指定，因为 App Router 已经是默认选项
npx create-next-app my-project
```

App Router 的文件结构示例：

```plaintext
my-project/
├── app/
│   ├── layout.tsx          # 根布局（所有页面共享）
│   ├── page.tsx           # 首页（/）
│   ├── about/
│   │   └── page.tsx       # 关于页（/about）
│   ├── blog/
│   │   ├── page.tsx       # 博客列表（/blog）
│   │   └── [slug]/
│   │       └── page.tsx   # 博客详情（/blog/:slug）
│   └── globals.css        # 全局样式
├── public/                 # 静态资源
└── package.json
```

```typescript
// app/layout.tsx
// 这是根布局，所有页面都会包裹在这个布局里
export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="zh-CN">
      <body>
        {/* 这里是全局导航栏，所有页面都会显示 */}
        <header>
          <nav>
            <a href="/">首页</a>
            <a href="/about">关于</a>
            <a href="/blog">博客</a>
          </nav>
        </header>

        {/* children 是当前页面的内容 */}
        <main>{children}</main>

        {/* 这里是全局页脚 */}
        <footer>© 2026 我的博客</footer>
      </body>
    </html>
  )
}
```

```typescript
// app/page.tsx
// 这是首页
export default function HomePage() {
  return (
    <div>
      <h1>欢迎来到我的网站！</h1>
      <p>这是一个使用 App Router 的 Next.js 项目。</p>
    </div>
  )
}
```

### 5.4.2 Pages Router（--no-app）：旧版架构，兼容性优先时使用

**Pages Router** 是 Next.js 传统的路由系统，
从 Next.js 诞生之初就存在了。
如果你需要维护一个老项目，或者你需要使用一些 App Router 还不支持的功能，
Pages Router 仍然是一个可靠的选择。

Pages Router 的主要特点：

1. **基于文件的路由**：每个文件对应一个路由，文件路径就是路由路径
2. **全栈能力**：你可以轻松创建 API 路由（`pages/api/` 目录）
3. **广泛兼容**：大量的教程、插件、第三方库都是基于 Pages Router 的
4. **稳定成熟**：经过多年打磨，bug 少，文档全

```bash
# 显式指定使用 Pages Router
npx create-next-app my-pages-router-project --no-app
```

Pages Router 的文件结构示例：

```plaintext
my-project/
├── pages/
│   ├── _app.tsx           # 全局 App 组件（所有页面共享）
│   ├── _document.tsx      # 文档组件（自定义 HTML 结构）
│   ├── index.tsx          # 首页（/）
│   ├── about.tsx          # 关于页（/about）
│   ├── blog/
│   │   ├── index.tsx      # 博客列表（/blog）
│   │   └── [id].tsx       # 博客详情（/blog/:id）
│   └── api/
│       └── hello.ts       # API 路由（/api/hello）
├── public/                # 静态资源
└── package.json
```

```typescript
// pages/_app.tsx
// 这是全局 App 组件，所有页面都会包裹在这个组件里
import type { AppProps } from 'next/app'
import '../styles/globals.css'

export default function App({ Component, pageProps }: AppProps) {
  return (
    <>
      {/* 这里是全局导航栏 */}
      <header>
        <nav>
          <a href="/">首页</a>
          <a href="/about">关于</a>
          <a href="/blog">博客</a>
        </nav>
      </header>

      {/* Component 是当前页面的组件，pageProps 是页面传递过来的数据 */}
      <Component {...pageProps} />

      {/* 这里是全局页脚 */}
      <footer>© 2026 我的博客</footer>
    </>
  )
}
```

```typescript
// pages/index.tsx
// 这是首页
import type { NextPage } from 'next'

const HomePage: NextPage = () => {
  return (
    <div>
      <h1>欢迎来到我的网站！</h1>
      <p>这是一个使用 Pages Router 的 Next.js 项目。</p>
    </div>
  )
}

export default HomePage
```

### 5.4.3 新项目建议直接选 App Router

作为 Next.js 官方默认且大力推广的路由系统，
**App Router 是未来发展的方向**。
新项目建议直接使用 App Router，原因如下：

1. **官方支持**：Vercel（Next.js 的母公司）正在大力开发 App Router 的新功能
2. **性能优势**：React Server Components 可以显著减少客户端 JavaScript 的体积
3. **现代设计**：App Router 的 API 设计更符合现代 React 的开发理念
4. **长期维护**：随着时间推移，Pages Router 的关注度会逐渐降低

> 💡 **温馨提示**：如果你是一个完全的初学者，
> 可能会发现 App Router 的概念比 Pages Router 难懂一些。
> 但是，请不要因为这个就退缩。
> App Router 虽然概念新，但它其实是更「符合直觉」的设计。
> 想象一下，你要创建一个 `/blog` 路由，只需要创建 `app/blog/page.tsx` 文件就行了，
> 这多么自然！

### 5.4.4 两者不可混用，选择后需按对应方式开发

**重要的事情说一遍**：App Router 和 Pages Router 不能同时使用！

这意味着你必须在项目创建时就做出选择，之后就不能更改了。
虽然 Next.js 允许你在一个项目中同时拥有 `app/` 和 `pages/` 目录，
但它们会被视为两个独立的路由系统，不会互相通信——就像两套平行的宇宙，各玩各的。
如果你尝试在 App Router 的页面中引用 Pages Router 的组件，
可能会遇到各种意想不到的问题，最后只能仰天长叹「我的组件去哪了？」

简单来说：

- 如果你选择了 App Router，就要使用 `app/` 目录来组织代码
- 如果你选择了 Pages Router，就要使用 `pages/` 目录来组织代码
- **不要混用！不要混用！不要混用！**（重要的事情说三遍）

```mermaid
graph LR
    A["创建项目"] --> B{选择路由方式}
    B -->|App Router| C["使用 app/ 目录"]
    B -->|Pages Router| D["使用 pages/ 目录"]
    C --> E["只能使用 app/ 方式开发"]
    D --> F["只能使用 pages/ 方式开发"]
    E --> G["🚀 开始写代码"]
    F --> G

    style C fill:#e6f7ff,stroke:#1890ff,stroke-width:2px
    style D fill:#fff7e6,stroke:#fa8c16,stroke-width:2px
    style G fill:#d9f7be,stroke:#52c41a,stroke-width:2px
```

---

## 5.5 src 目录的使用

> 有时候，你会看到有些项目的代码组织得像「俄罗斯套娃」——
> 一层套一层，文件藏在很深的目录里；
> 而有些项目则「平铺直叙」，所有东西都摆在根目录下一目了然。
> 这一节，我们来聊聊 Next.js 的 `src` 目录，以及它到底是干什么用的。

### 5.5.1 --src-dir 参数的作用

当你创建 Next.js 项目时，create-next-app 会问你一个问题：
「是否使用 `src/` 目录来组织应用程序代码？」

如果你选择「是」，你的项目结构就会变成这样：

```plaintext
my-project/
├── src/                    # 源代码目录（所有的应用代码都放在这里）
│   ├── app/                # App Router 的页面文件
│   │   ├── page.tsx
│   │   └── layout.tsx
│   └── components/         # 组件目录（放置可复用的 React 组件）
│       └── Header.tsx
├── public/                 # 静态资源（图片、字体等）
├── package.json
└── ...
```

如果你选择「否」，你的项目结构就会是这样：

```plaintext
my-project/
├── app/                    # App Router 的页面文件（直接在根目录下）
│   ├── page.tsx
│   └── layout.tsx
├── components/             # 组件目录
│   └── Header.tsx
├── public/                 # 静态资源
├── package.json
└── ...
```

```bash
# 使用 --src-dir 参数
npx create-next-app my-src-project --src-dir

# 不使用 --src-dir 参数（默认）
npx create-next-app my-flat-project
```

### 5.5.2 有 src/ 和无 src/ 目录结构的区别

从功能上来说，两种结构没有任何区别。
`src/` 目录只是一个「包装」，它把所有的源代码都放在一起，
让项目结构更加清晰。

有 `src/` 目录的优势：

1. **代码和配置分离**：配置文件（package.json、tsconfig.json 等）在根目录，
   源代码在 `src/` 目录，职责分明
2. **更清晰的视图**：当你打开项目文件夹时，一眼就能看到「这是配置文件，那是源代码」
3. **方便部署**：某些部署平台可以自动识别 `src/` 目录，并相应地调整构建流程

没有 `src/` 目录的特点：

1. **目录层级更浅**：文件路径更短，比如 `app/page.tsx` vs `src/app/page.tsx`
2. **传统惯例**：很多老的 Node.js 项目都是这样组织的
3. **简单直接**：不需要多一层目录

```mermaid
graph TD
    subgraph "有 src/ 目录"
        A1["my-project/"]
        A2["├── src/"]
        A3["│   ├── app/"]
        A4["│   ├── components/"]
        A5["│   └── lib/"]
        A6["├── public/"]
        A7["└── package.json"]
    end

    subgraph "无 src/ 目录"
        B1["my-project/"]
        B2["├── app/"]
        B3["├── components/"]
        B4["├── lib/"]
        B5["├── public/"]
        B6["└── package.json"]
    end

    style A2 fill:#e6f7ff,stroke:#1890ff,stroke-width:2px
    style B1 fill:#f5f5f5,stroke:#999,stroke-width:2px
```

### 5.5.3 团队内保持统一规范的重要性

无论你选择有 `src/` 还是无 `src/` 目录，**最重要的是团队保持一致**。

想象一下这样的场景：你接手了一个项目，
项目里有 `src/` 目录，但是 `public/` 目录下又有一个 `components/` 目录，
`components/` 目录下又有一个 `src/` 目录...这是什么样的灾难现场？

所以，建议在你的团队中制定以下规范：

1. **统一选择**：项目创建时就决定是否使用 `src/` 目录，并写入项目规范文档
2. **统一命名**：组件目录叫 `components/` 还是 `components/`？工具函数放在 `lib/` 还是 `utils/`？
3. **统一导入路径**：使用相对路径（`../components/Button`）还是绝对路径（`@/components/Button`）？

```json
// tsconfig.json 配置绝对路径别名
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]  // 这样 @/components/Button 就等同于 ./src/components/Button
    }
  }
}
```

> 💡 **温馨提示**：Next.js 默认支持 `src/` 目录，
> 但如果你选择不使用 `src/` 目录，你需要确保你的 `tsconfig.json` 中的路径配置正确。
> create-next-app 会自动帮你处理好这个问题，所以不用担心。

---

## 5.6 环境变量

> 环境变量是软件开发中的「隐藏关卡」。
> 它不在代码中明文出现，却控制着程序的运行方式；
> 它像是程序的「基因」，决定了程序在不同环境下有不同的行为。
> 这一节，我们来揭开环境变量的神秘面纱。

### 5.6.1 .env.local 的创建与使用

在 Next.js 中，**环境变量**通常存储在项目根目录的 `.env.local` 文件中。
这个文件不会被提交到 Git 仓库（因为它在 `.gitignore` 中），
所以你可以安全地存放一些敏感信息。

```bash
# 在项目根目录下创建 .env.local 文件
touch .env.local

# 编辑 .env.local 文件
```

```env
# .env.local 文件示例

# 数据库配置
DATABASE_URL=postgres://user:password@localhost:5432/mydb

# API 密钥（敏感信息！）
API_SECRET_KEY=sk-1234567890abcdef

# 第三方服务配置
STRIPE_PUBLIC_KEY=pk_test_12345678
STRIPE_SECRET_KEY=sk_test_12345678

# 应用配置
NEXT_PUBLIC_APP_NAME=我的博客
NEXT_PUBLIC_API_URL=http://localhost:3000/api
```

然后，在你的代码中这样使用：

```typescript
// 读取环境变量
const databaseUrl = process.env.DATABASE_URL
const apiSecretKey = process.env.API_SECRET_KEY

// 在 TypeScript 中，如果你想获得更好的类型提示，
// 可以在项目根目录创建一个 env.d.ts 文件（注意：不要修改 next-env.d.ts，它由 Next.js 自动生成）
// env.d.ts 示例：
/*
/// <reference types="next" />
/// <reference types="next/image-types/global" />

declare module '*.env' {
  export const DATABASE_URL: string
  export const API_SECRET_KEY: string
  export const NEXT_PUBLIC_APP_NAME: string
  export const NEXT_PUBLIC_API_URL: string
}
*/
```

### 5.6.2 NEXT_PUBLIC_ 前缀的含义与客户端暴露风险

这是 Next.js 环境变量中**最最重要的概念**，没有之一！

在 Next.js 中，以 `NEXT_PUBLIC_` 开头的环境变量**会被嵌入到客户端的 JavaScript 代码中**。
这意味着，任何访问你网站的人都可以在浏览器中看到这些变量的值。

而**不以 `NEXT_PUBLIC_` 开头的变量**，只会在服务器端代码中使用，
不会泄露给客户端。

```env
# .env.local

# 这个变量只在服务器端可用，不会暴露给客户端
DATABASE_URL=postgres://user:password@localhost:5432/mydb
API_SECRET_KEY=sk-1234567890abcdef

# 这个变量会被嵌入到客户端 JavaScript 中，可以被任何人看到
NEXT_PUBLIC_APP_NAME=我的博客

# 这个变量也会被嵌入到客户端 JavaScript 中
NEXT_PUBLIC_API_URL=http://localhost:3000/api
```

```typescript
// app/page.tsx
// 这个组件会在客户端和服务器端都运行

export default function HomePage() {
  // ✅ 安全：这是一个服务器端变量，不会暴露给客户端
  const dbUrl = process.env.DATABASE_URL

  // ✅ 安全但要注意：这个变量会被嵌入到客户端代码中
  // 任何人都可以在浏览器开发者工具中看到它的值
  const appName = process.env.NEXT_PUBLIC_APP_NAME

  // ✅ 安全：这也是一个服务器端变量
  const apiSecret = process.env.API_SECRET_KEY

  return (
    <div>
      <h1>欢迎来到 {appName}！</h1>
      {/* dbUrl 和 apiSecret 不会在客户端代码中出现 */}
      {/* 它们只在服务器端的日志或数据库操作中使用 */}
    </div>
  )
}
```

```typescript
// app/api/hello/route.ts
// 这个文件只在服务器端运行

export async function GET() {
  // ✅ 安全：这是服务器端代码，没有人能在浏览器中看到这些值
  const dbUrl = process.env.DATABASE_URL
  const apiSecret = process.env.API_SECRET_KEY

  // 可以在服务器端安全地使用这些敏感信息
  console.log('数据库连接字符串是：', dbUrl)  // 只会打印在服务器日志中
  console.log('API 密钥是：', apiSecret)  // 只会打印在服务器日志中

  return Response.json({ message: 'Hello!' })
}
```

> ⚠️ **灵魂拷问**：我怎么知道哪些信息可以客户端使用？
>
> 简单来说：
> - **可以被公开的信息**：应用名称、API 基础 URL、公共配置等 → 使用 `NEXT_PUBLIC_`
> - **绝对不能公开的信息**：数据库密码、API 密钥、私钥等 → **绝对不要加 `NEXT_PUBLIC_`**
>
> 想象一下，如果你的 API 密钥被坏人获取了，
> 他们就可以用你的密钥访问付费 API，把你的账户刷爆。
> 所以，**永远不要**把敏感信息暴露给客户端！
>
> 💡 **一个简单的判断标准**：如果你把这个变量值发到微博上都无所谓，那就用 `NEXT_PUBLIC_`；
> 如果你发出去会后悔到想把键盘吞掉，那就老老实实当服务器端变量。

### 5.6.3 不要将 .env.local 提交到版本库

前面已经强调过了，但让我们再强调一遍：

**`.env.local 文件包含敏感信息，绝对不能提交到 Git！`**

为了确保安全，你需要：

1. 确保 `.gitignore` 文件中包含 `.env.local`（create-next-app 会自动帮你处理）
2. 创建一个 `.env.local.example` 文件作为模板（不包含真实值）
3. 在项目文档中说明如何创建 `.env.local` 文件

```bash
# .gitignore 应该包含这些内容
.env.local
.env.*.local
```

```env
# .env.local.example（这是模板，不包含真实值）

# 数据库配置（请替换为你自己的值）
DATABASE_URL=你的数据库连接字符串

# API 密钥（请替换为你自己的值）
API_SECRET_KEY=你的API密钥

# 第三方服务配置
STRIPE_PUBLIC_KEY=你的公开密钥
STRIPE_SECRET_KEY=你的私有密钥

# 应用配置
NEXT_PUBLIC_APP_NAME=你的应用名称
NEXT_PUBLIC_API_URL=你的API地址
```

```bash
# 团队新成员的正确流程：
# 1. 克隆项目
git clone https://github.com/your-org/your-project.git

# 2. 复制模板文件
cp .env.local.example .env.local

# 3. 填写真实值
# 编辑 .env.local 文件，填入自己的配置
```

### 5.6.4 .env.local.example 的参考作用

`.env.local.example` 是一个「参考文件」，
它列出了项目需要的所有环境变量，但不包含真实的值。
它的作用是：

1. **告诉开发者需要哪些环境变量**：新加入项目的开发者一看就知道需要配置什么
2. **提供默认值**：某些变量可能有默认值，可以直接使用
3. **方便团队协作**：即使不分享真实的敏感信息，也能让团队成员了解项目的配置需求

```env
# .env.local.example

# ===================
# 必填配置
# ===================

# 数据库连接字符串
# 格式：postgres://用户名:密码@主机:端口/数据库名
DATABASE_URL=postgres://user:password@localhost:5432/mydb

# ===================
# 可选配置（有默认值）
# ===================

# 应用的公开名称（前端显示用）
NEXT_PUBLIC_APP_NAME=我的博客

# API 基础地址
NEXT_PUBLIC_API_URL=http://localhost:3000/api

# ===================
# 敏感配置（需要从外部获取）
# ===================

# 第三方支付密钥（请向财务申请）
STRIPE_SECRET_KEY=sk_live_xxxxx

# 发送邮件的服务商 API Key（请向运维申请）
MAILGUN_API_KEY=key-xxxxx
```

> 💡 **温馨提示**：`.env.local.example` 文件是可以提交到 Git 的，
> 因为它不包含任何真实的敏感信息。
> 它就像是一个「配置清单」，告诉未来的自己和团队成员：
> 「这个项目需要这些环境变量，你准备好了吗？」

---

## 5.7 生产部署

> 开发环境就像是「练车场」，生产环境才是「真实道路」。
> 在练车场里，你可以慢慢开、随便停、甚至撞了也不怕。
> 但到了真实道路上，你就得打起十二分精神了。
> 这一节，我们来聊聊如何把你的 Next.js 应用「开上」生产环境。

### 5.7.1 npm run dev 仅用于开发，禁止用于生产

**`npm run dev`** 是开发模式的命令，
它会启动一个带有「热重载」功能的开发服务器。
当你修改代码时，页面会自动刷新，让你立刻看到效果。

但是，这个命令**绝对不能用于生产环境**！

为什么？

1. **性能差**：开发服务器没有做任何优化，每次请求都会重新编译代码
2. **不安全**：开发服务器会显示详细的错误信息和源代码
3. **不稳定**：开发服务器设计用于开发，可能会遇到各种问题

```bash
# ❌ 错误：在生产服务器上运行 dev 命令
npm run dev
# 你的老板/客户/用户：为什么网站这么慢？
# 你：...

# ✅ 正确：先构建，再启动生产服务器
npm run build
npm start
```

> 🚨 **血的教训**：曾经有开发者在生产服务器上运行了 `npm run dev`，
> 结果网站的响应时间达到了「感人」的 10 秒，
> 而且任何访问者都能看到完整的错误堆栈信息。
> 这个故事告诉我们：开发命令是用来开发的，生产环境要用生产命令。

### 5.7.2 生产构建：npm run build + npm start

Next.js 的生产部署分为两步：

1. **构建（build）**：将你的代码编译成高性能的生产版本
2. **启动（start）**：运行构建后的生产服务器

```bash
# 第一步：构建生产版本
npm run build
# 输出示例：
#   ✓ Compiled successfully
#   ✓ Collecting page data
#   ✓ Generating static pages (for static export)
#   ✓ Build completed successfully
#
#   Output directory: .next
#   ✓ Collect optimizations
```

```bash
# 第二步：启动生产服务器
npm start
# 输出示例：
#   ▲ Next.js 14.2.5
#   - Local:        http://localhost:3000
#   - production   http://your-domain.com
```

> 📝 **小知识**：构建过程中，Next.js 会做很多事情：
> - **编译 TypeScript/JavaScript**：将你的代码编译成浏览器可以执行的 JavaScript
> - **优化图片**：压缩图片、生成响应式图片
> - **代码分割**：将代码分割成小块，按需加载
> - **预取优化**：预取用户可能访问的页面
> - **静态生成**：对于不依赖用户数据的页面，直接生成静态 HTML

### 5.7.3 Vercel 部署（官方推荐，零配置）

**Vercel** 是 Next.js 的「娘家」——
Next.js 就是由 Vercel 的团队开发和维护的。
因此，Vercel 对 Next.js 的支持是最好的，部署过程也是最简单的。

你可以把 Vercel 理解为一个「专门为 Next.js 优化的云平台」，
它能自动识别 Next.js 项目，并提供最佳的部署体验。

部署步骤：

1. **推送代码到 GitHub/GitLab/Bitbucket**
2. **登录 Vercel**（https://vercel.com）
3. **点击「Add New Project」**
4. **选择你的代码仓库**
5. **点击「Deploy」**

```bash
# 或者使用 Vercel CLI 进行部署
# 首先安装 Vercel CLI
npm install -g vercel

# 登录 Vercel
vercel login

# 进入项目目录并部署
cd my-project
vercel

# 按照提示操作：
# ? Set up and deploy? [Y/n] y
# ? Which scope? your-username
# ? Link to existing project? [y/N] n
# ? What's your project's name? my-project
# ? In which directory is your code located? ./
# ? Want to override the settings? [y/N] n
```

Vercel 的优势：

- **零配置**：不需要写 Dockerfile、不需要配置服务器
- **自动 HTTPS**：自动配置 SSL 证书
- **全球 CDN**：让你的网站在全球各地都能快速访问
- **预览部署**：每次 PR 都会自动生成一个预览链接，方便审核
- **免费额度**：个人项目和小型项目基本免费使用

> 💡 **温馨提示**：Vercel 的免费额度对于个人项目和小型项目来说是非常充足的。
> 每个月有 100GB 的带宽、100GB 的服务器时间，
> 对于大多数个人博客和小型应用来说足够了。
> 当然，如果你需要更高的额度，Vercel 也提供了付费计划。

### 5.7.4 其他部署平台（Railway / Fly.io / Docker）

虽然 Vercel 是 Next.js 的「官方首选」，
但有时候你可能需要将应用部署到其他平台。

**Railway**：

Railway 是一个现代化的部署平台，它的特点是「简单粗暴」。
你只需要连接 GitHub 仓库，它就会自动检测并部署。
支持多种语言和框架，包括 Next.js。

```bash
# Railway CLI 安装
npm install -g @railway/cli

# 登录
railway login

# 部署
cd my-project
railway init
railway up
```

**Fly.io**：

Fly.io 是一个专注于「全球分布式部署」的平台。
它会在全球多个地区部署你的应用，并根据用户的地理位置，
自动选择最近的服务器进行响应。

```bash
# Fly.io CLI 安装
curl -L https://fly.io/install.sh | sh

# 登录
fly auth login

# 创建应用
cd my-project
fly launch

# 部署
fly deploy
```

**Docker**：

Docker 是一个容器化平台，它可以把你的应用和所有依赖打包成一个「容器」，
然后在任何支持 Docker 的环境中运行。
这是最传统的部署方式，也是最灵活的。

### 5.7.5 Docker 部署注意事项

如果你选择使用 Docker 来部署 Next.js，以下几点需要注意：

1. **多阶段构建**：为了减小镜像体积，建议使用多阶段构建
2. **Node.js 版本**：确保生产环境的 Node.js 版本与开发环境一致
3. **环境变量**：不要把敏感信息硬编码到 Dockerfile 中，使用环境变量

```dockerfile
# Dockerfile（多阶段构建）

# 阶段一：构建
FROM node:18-alpine AS builder
WORKDIR /app

# 复制依赖文件
COPY package*.json ./

# 安装依赖（包括 devDependencies，因为构建需要 TypeScript 等工具）
RUN npm ci

# 复制源代码
COPY . .

# 构建生产版本
RUN npm run build

# 阶段二：运行
FROM node:18-alpine AS runner
WORKDIR /app

# 创建一个非 root 用户（更安全）
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

# 复制构建产物
COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

# 切换到非 root 用户
USER nextjs

# 暴露端口
EXPOSE 3000

# 启动命令
ENV PORT=3000
ENV HOSTNAME="0.0.0.0"

CMD ["node", "server.js"]
```

> ⚠️ **特别提醒**：上面的 Dockerfile 使用了 standalone 模式。
> 在 standalone 模式下，Next.js 会生成一个独立的 `server.js` 文件，
> 你只需要用 `node server.js` 就可以启动，无需安装 Next.js 本身。
> 要启用这个模式，需要在 `next.config.js` 中添加配置：

```javascript
// next.config.js
/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',  // 启用 standalone 模式，只打包运行时必需的文件
}

module.exports = nextConfig
```

```bash
# 构建 Docker 镜像
docker build -t my-nextjs-app .

# 运行容器
docker run -p 3000:3000 my-nextjs-app

# 或者使用 docker-compose
# docker-compose.yml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "3000:3000"
    environment:
      - DATABASE_URL=postgres://user:password@db:5432/mydb
      - API_SECRET_KEY=your-secret-key
    depends_on:
      - db
  db:
    image: postgres:15
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=mydb
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  pgdata:
```

> 📝 **小知识**：为什么要使用多阶段构建？
> 因为如果你在一个镜像中同时包含源代码、依赖和构建工具，
> 镜像体积会非常大（可能有几 GB）。
> 而多阶段构建可以让最终的镜像只包含运行所需的文件（几百 MB），
> 大大加快部署速度和减少磁盘占用。
> 想象一下，如果你的镜像是 2GB，你需要上传到服务器，
> 那得等多久？但如果只有 200MB，那就快多了。

---

## 本章小结

本章我们详细介绍了使用 create-next-app 创建 Next.js 项目后的各种注意事项：

1. **版本与兼容性**：Node.js 18+ 是 Next.js 14+ 的最低要求，create-next-app 和 Next.js 版本号通常对齐，可以通过 `@latest`、`@14`、`@canary` 等方式指定版本，同时注意 npm/yarn/pnpm 的差异。

2. **创建时的常见问题**：目标目录已存在需要使用空目录或 `--force` 参数，网络问题可以配置国内镜像源，磁盘空间不足需要清理缓存，权限错误需要配置用户目录权限，Windows 用户推荐使用 PowerShell 7+ 或 WSL2。

3. **创建后必做事项**：立即初始化 Git 仓库，确认 .gitignore 包含必要条目，检查 package.json 的 scripts 和依赖版本，以及首次运行 `npm run dev` 确认一切正常。

4. **App Router 与 Pages Router**：App Router 是新一代路由系统（Next.js 13+ 默认），代表未来方向，适合新项目；Pages Router 是传统架构，适合维护老项目或需要兼容的场景，两者不可混用。

5. **src 目录**：使用 `--src-dir` 参数可以将代码组织到 `src/` 目录中，使项目结构更清晰，但团队内部需要保持统一规范。

6. **环境变量**：`.env.local` 用于存储环境变量，`NEXT_PUBLIC_` 前缀的变量会暴露给客户端，需要特别注意安全性，不要将 `.env.local` 提交到 Git，`.env.local.example` 作为模板供参考。

7. **生产部署**：`npm run dev` 仅用于开发，生产需要使用 `npm run build` + `npm start`，Vercel 是官方推荐的部署平台，也可以使用 Railway、Fly.io 或 Docker 进行部署，Docker 部署需要使用多阶段构建并注意安全配置。

> 🎉 **恭喜你完成了第五章的学习！**
> 现在你已经掌握了 create-next-app 的各种「隐藏技巧」和「最佳实践」。
> 下一章，我们将深入探讨 Next.js 的配置和高级用法，
> 让你从一个「会用」Next.js 的开发者，变成一个「用好」Next.js 的开发者。
> 准备好了吗？让我们继续前进！
