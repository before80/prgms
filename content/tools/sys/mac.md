+++
title = "macOS"
date = 2026-09-24T16:45:56+08:00
weight = 1
type = "docs"
description = ""
isCJKLanguage = true
draft = false

+++

## 新 macOS 相关设置提升效率

​	可参见以下视频：

{<youtube "q3-jUJZpC0o">}



## macOS Gatekeeper（门卫）简介

​	Gatekeeper 是 macOS 内置安全机制，**用来限制未经过 Apple 公证的程序直接运行**，从 OS X 10.11 El Capitan 引入。

### 核心原理

​	当你从浏览器、聊天软件下载文件时，macOS 自动给文件打上扩展属性：`com.apple.quarantine`（隔离标记）。 带有这个标记的程序启动前，Gatekeeper 会做两件校验：

1. 检查应用是否有**开发者签名**；
2. 检查签名是否经过 **Apple 公证（Notarization）**。

​	校验通过 → 正常打开； 校验失败 → 弹出提示：**无法打开，因为 Apple 无法检查其是否包含恶意软件**，直接阻止运行。

> 本地拷贝、U 盘内部复制的文件，默认**不会**添加隔离标记，不会触发 Gatekeeper 校验。

### 系统安全选项（系统设置 → 隐私与安全性）

三个运行策略：

1. **App Store**：只允许 App Store 下载的应用
2. **App Store 和已识别的开发者**（默认）：允许 App Store + 有正规签名 + 公证的第三方开发者软件，这是日常默认选项
3. **任何来源**：新版 macOS 默认隐藏该选项，开启后 Gatekeeper 不拦截（不推荐长期开启）

### 绕过校验的几种方式

1. 单次放行：弹出阻止提示后，在「隐私与安全性」页面点**仍要打开**，本次放行，系统记住该 App
2. 命令删除隔离标记：就是刚才的 `xattr -rd com.apple.quarantine`，**移除 quarantine 标记后，Gatekeeper 不再校验这个 App**
3. 临时全局关闭 Gatekeeper（不推荐）

```bash
# 关闭
sudo spctl --master-disable
# 开启
sudo spctl --master-enable
```

### 关键区分

- Gatekeeper：**控制应用能不能启动**，做签名 + 公证检查
- XProtect：macOS 内置恶意软件检测，**就算绕过 Gatekeeper，XProtect 依然会扫描恶意代码**
- FileQuarantine：就是那个`com.apple.quarantine`标记，是 Gatekeeper 的触发开关，**不是病毒标记**

### 局限与风险

- Gatekeeper **不是杀毒软件**，它只能校验签名和公证，不能保证程序本身无后门；
- 公证只是证明安装包提交给 Apple 扫描过，**不代表 Apple 认证软件绝对安全**；
- 删除隔离标记，只是去掉触发 Gatekeeper 的开关，**不会关闭系统其他安全防护**。

## 安装 Easydict

​	一个简洁优雅的词典翻译 macOS App。开箱即用，支持离线 OCR 识别，支持有道词典，🍎 苹果系统词典，🍎 苹果系统翻译，OpenAI，Gemini，DeepL，Google，Bing，腾讯，百度，阿里，小牛，彩云和火山翻译。

```bash
# 到 https://github.com/tisfeng/Easydict/releases 下载最新版 Easydict.dmg
# 点击 Easydict.dmg 打开后拖入 Applications
# 执行以下命令，递归删除 Easydict 整个 App 包里所有文件的网络隔离标记
xattr -rd com.apple.quarantine /Applications/Easydict.app
```



## 安装 QuickRecorder

用来录屏

```bash
brew install lihaoyun6/tap/quickrecorder
```



## 安装 Navicat Premium Lite

用来访问数据库

```bash
# 访问 https://www.navicat.com/en/download/navicat-premium-lite
# 下载安装包
# 安装
# 执行以下命令，递归删除 Navicat Premium Lite 整个 App 包里所有文件的网络隔离标记
# 下载的 Navicat 打开时，macOS 提示：
# “Navicat Premium Lite” 无法打开，因为 Apple 无法检查其是否包含恶意软件。
# 原理：macOS 检测到文件带有`com.apple.quarantine`标记，
# 触发 Gatekeeper 安全校验；如果软件未公证 / 签名，直接阻止运行。
# 执行这条命令相当于告诉系统：你信任这个程序，不再做隔离校验
xattr -rd com.apple.quarantine /Applications/Navicat\ Premium\ Lite.app 
# 使用临时邮箱注册账号
# 验证邮箱
# 登录账号
# 访问数据库
```



## 撤销`git commit -m "提交信息"`

```bash
# 前提没有提交到远程仓库
# 推荐：撤销本次commit，代码保留在暂存区（最安全，不会丢代码）
# `HEAD^` = 上一个提交节点，回退 HEAD 指针，
# 文件改动还在 add 后的暂存状态，可以重新写 message 再 commit
git reset --soft HEAD^

# 或者
# 撤销本次commit，代码保留在工作区（取消add，需要重新git add）
# 等价 git reset --mixed HEAD^ （mixed是reset默认模式）
git reset HEAD^

# 如果你只是想修改这次空的 commit message，而不是撤销提交，直接：
git commit --amend -m "正确的提交信息"

```



## 撤销`git add -A`

​	`git add -A`：把**所有修改、删除、新增文件**全部加入暂存区（index）。撤销的本质：**取消暂存，代码保留在本地文件，不会丢失**。

```bash
git reset HEAD
# 等价于 git reset --mixed HEAD
```

​	执行后：

- 暂存区清空，所有文件回到**工作区未 add 状态**
- ✅ 本地修改**完全保留**，文件内容不变
- 执行 `git status` 就能看到：不再是 `Changes to be committed`

```bash
git restore --staged .
```

​	效果和 `git reset HEAD` 一模一样。

### 只撤销单个文件（不想全部取消）

```bash
git reset HEAD 文件名
# 示例：git reset HEAD src/main.rs
```

