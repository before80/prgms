+++
title = "附录 C 常用命令速查"
weight = 1020
date = "2026-03-25T12:54:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 附录 C 常用命令速查

> 磨刀不误砍柴工。Vue 3 开发涉及很多工具——Vite、npm/pnpm、Git、Vue Router、Pinia 等。每个工具都有一套自己的命令，靠脑子记肯定记不住。这一章把最常用的命令整理成速查表，方便随时查阅。

## C.1 Vite / npm / pnpm / yarn 常用命令

### Vite 命令

```bash
# 创建项目
pnpm create vite@latest my-app --template vue
pnpm create vite@latest my-app --template vue-ts  # TypeScript 版本

# 开发模式（启动开发服务器）
pnpm dev
npm run dev

# 构建生产版本
pnpm build

# 预览构建产物（本地测试）
pnpm preview

# 预览构建产物（指定端口）
pnpm preview --port 3000
```

### npm 命令

```bash
# 初始化项目
npm init -y

# 安装依赖
npm install              # 安装 package.json 中的所有依赖
npm install vue          # 安装单个包
npm install -D typescript # 安装到 devDependencies
npm install -g @vue/cli  # 全局安装

# 更新依赖
npm update vue
npm update               # 更新所有依赖

# 删除依赖
npm uninstall vue
npm remove vue

# 查看
npm list                # 查看已安装的包
npm list --depth=0      # 只看顶层依赖
npm view vue versions   # 查看某个包的所有版本

# 运行脚本
npm run dev
npm run build
npm run test

# 缓存
npm cache clean --force  # 清除 npm 缓存
```

### pnpm 命令

```bash
# 安装
pnpm install            # 安装所有依赖
pnpm add vue           # 安装单个包
pnpm add -D typescript  # 安装到 devDependencies
pnpm add -g pnpm       # 全局安装

# 更新
pnpm update
pnpm up vue

# 删除
pnpm remove vue
pnpm rm vue

# 其他
pnpm list              # 查看已安装包
pnpm store status      # 查看 pnpm 全局 store 状态
pnpm store prune        # 清理未引用的包
pnpm init              # 初始化项目（相当于 npm init -y）
```

### yarn 命令

```bash
# 安装
yarn install            # 安装所有依赖
yarn add vue           # 安装单个包
yarn add -D typescript # 安装到 devDependencies

# 更新
yarn upgrade
yarn up vue

# 删除
yarn remove vue

# 其他
yarn list              # 查看已安装包
yarn init              # 初始化项目
```

## C.2 Pinia / Vue Router 命令

### Pinia

Pinia 没有独立的 CLI 命令，主要是代码层面的 API：

```typescript
// 创建 store
import { defineStore } from 'pinia'
export const useCounterStore = defineStore('counter', {
  state: () => ({ count: 0 }),
  actions: { increment() { this.count++ } }
})

// 使用 store
const store = useCounterStore()
store.increment()
console.log(store.count)

// $reset() 重置 state（选项式写法）
store.$reset()

// $patch 批量修改
store.$patch({ count: 10, name: '新名字' })

// $subscribe 订阅 state 变化
store.$subscribe((mutation, state) => {
  console.log('state 变了')
})

// $onAction 监听 actions
store.$onAction(({ name, args }) => {
  console.log(`action ${name} 被调用，参数：`, args)
})
```

### Vue Router

```typescript
// 编程式导航
router.push('/user/123')          // 跳转（留下历史记录）
router.replace('/about')           // 替换（不留下历史记录）
router.go(-1)                     // 后退
router.go(1)                     // 前进

// 获取当前路由
const route = useRoute()
console.log(route.params.id)     // 动态路由参数
console.log(route.query.page)     // query 参数
console.log(route.path)           // 当前路径

// 动态添加路由
router.addRoute({ path: '/new', component: NewPage })

// 动态删除路由
router.removeRoute('UserDetail')
```

## C.3 Git 常用命令

### 基础配置

```bash
# 设置用户名和邮箱
git config --global user.name "小明"
git config --global user.email "xiaoming@example.com"

# 生成 SSH 密钥
ssh-keygen -t ed25519 -C "xiaoming@example.com"

# 查看配置
git config --list
git config user.name
```

### 基础操作

```bash
# 初始化仓库
git init

# 克隆仓库
git clone https://github.com/username/repo.git
git clone -b dev https://github.com/username/repo.git  # 克隆指定分支

# 添加文件到暂存区
git add .              # 添加所有文件
git add src/App.vue   # 添加指定文件
git add -p            # 交互式添加（选择性地添加修改的某一部分）

# 提交
git commit -m "feat: 添加用户登录功能"
git commit -am "fix: 修复列表翻页bug"  # add + commit 合并（仅限已跟踪的文件）

# 查看状态
git status
git status -s         # 简洁模式

# 查看差异
git diff              # 工作区 vs 暂存区
git diff --staged      # 暂存区 vs 最新提交
git diff HEAD          # 工作区 vs 最新提交
git diff dev..main     # dev 和 main 分支的差异
```

### 分支操作

```bash
# 查看分支
git branch             # 本地分支
git branch -a          # 本地 + 远程分支
git branch -r           # 仅远程分支

# 创建分支
git branch dev          # 创建 dev 分支（不切换）
git checkout -b dev     # 创建并切换到 dev 分支
git switch -c dev       # 同上，git switch 是新语法

# 切换分支
git checkout dev
git switch dev
git checkout -          # 切换到上一个分支

# 合并分支
git merge dev           # 把 dev 合并到当前分支

# 删除分支
git branch -d dev       # 安全删除（已合并才允许删除）
git branch -D dev       # 强制删除
```

### 远程操作

```bash
# 查看远程仓库
git remote -v

# 添加远程仓库
git remote add origin https://github.com/username/repo.git

# 推送
git push origin main     # 推送到远程 main 分支
git push -u origin dev   # -u 设置上游分支，以后可以直接 git push
git push                 # 推送当前分支到上游

# 拉取
git pull origin main     # 拉取并合并
git fetch origin        # 仅获取远程更新，不合并

# 删除远程分支
git push origin --delete dev
```

### 暂存与恢复

```bash
# 暂存当前修改（不提交）
git stash               # 暂存所有修改
git stash save "WIP: 用户模块"
git stash -u            # 包括未跟踪的文件

# 恢复暂存
git stash pop           # 恢复并删除 stash
git stash apply         # 恢复但不删除 stash
git stash list          # 查看 stash 列表
git stash drop          # 删除 stash

# 恢复某个文件到某个版本
git checkout HEAD -- src/App.vue   # 丢弃工作区的修改
git restore src/App.vue            # 同上，git restore 是新语法
```

### 查看历史

```bash
# 查看提交历史
git log
git log --oneline      # 简洁模式
git log --graph         # 图形化显示分支
git log -n 5           # 只看最近 5 条

# 查看某个文件的修改历史
git log -p src/App.vue
git blame src/App.vue   # 按行查看最后修改人
```

### 标签操作

```bash
# 创建标签
git tag v1.0.0
git tag -a v1.0.0 -m "第一个正式版本"

# 推送标签
git push origin v1.0.0
git push origin --tags   # 推送所有标签

# 查看标签
git tag
git show v1.0.0
```

### 撤销操作

```bash
# 撤销暂存
git reset HEAD src/App.vue    # 把暂存区的文件移出暂存

# 撤销提交（保留工作区修改）
git reset --soft HEAD~1       # 撤销上一次提交，修改保留在暂存区
git reset --mixed HEAD~1      # 撤销上一次提交，修改保留在工作区（默认）
git reset --hard HEAD~1       # 撤销上一次提交，所有修改都丢弃（危险！）

# 撤销工作区修改
git checkout -- src/App.vue
git restore src/App.vue

# 反做某个提交
git revert HEAD              # 创建一个新提交来撤销上一个提交
```

---

## 附录小结

本章整理了 Vue 3 开发中最常用的命令速查：

- **Vite**：dev、build、preview
- **npm**：install、update、run
- **pnpm**：add、remove、store
- **Git**：add/commit/push/pull、branch、stash、log、reset、revert

建议把这些命令打印出来贴在工位旁边，用多了自然就记住了。

