+++
title = "第4章：Linux 桌面环境入门"
weight = 40
date = "2026-03-23T08:39:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 第四章：Linux 桌面环境入门

## 4.1 什么是桌面环境（Desktop Environment）？

装好了 Linux 系统，打开电脑，满心期待地等着看一个漂亮的图形界面——结果你看到的是什么？

**命令行终端**（黑屏白字那种）！就像电影里黑客敲代码的那种界面。

如果你觉得"这也太原始了吧"，那你绝对需要认识一下**桌面环境（Desktop Environment）**。

桌面环境就是 Linux 的"外壳"——一套帮你把命令行包装成图形界面的软件。它给你提供：图标、窗口、任务栏、桌面壁纸、文件管理器、壁纸设置、主题配色……一句话，把 Linux 从"黑客专用"变成"普通人也能用"的东西。

---

### 没有桌面环境的 Linux 是什么样的？

没有桌面环境的 Linux，你只能对着黑屏幕敲命令。这对服务器来说很正常（服务器不需要图形界面，命令行反而更省资源、更稳定），但对桌面用户来说，简直是折磨。

举几个例子，感受一下差距：

| 操作 | 没有桌面环境 | 有桌面环境 |
|------|-------------|-----------|
| 打开文件 | `cd /home/liming/Documents && ls` | 双击桌面图标 |
| 调节音量 | `amixer set Master 50%` | 拖动任务栏音量滑块 |
| 切换 Wi-Fi | `nmcli d wifi connect xxx` | 点击网络图标 → 选择 Wi-Fi |
| 截图 | `gnome-screenshot` | 按截图快捷键 |
| 关闭窗口 | `killall 程序名` 或 `pkill 程序名` | 点窗口右上角 ✕ |

没有桌面环境，你得记一堆命令；有桌面环境，点点鼠标就搞定了。

---

### 桌面环境包含哪些组件？

一个完整的桌面环境可不是一个软件，而是一整套软件包，通常包括：

**1. 窗口管理器（Window Manager）**
负责控制窗口的：最大、最小、关闭、移动、切换。桌面环境的心脏。

**2. 文件管理器（File Manager）**
帮你浏览文件夹、复制粘贴文件、挂载 U 盘等。比如 GNOME 的 "Files"（Nautilus），KDE 的 "Dolphin"。

**3. 面板/任务栏（Panel/Dock）**
桌面顶部或底部的条条，显示时间、打开的程序、系统托盘等。

**4. 桌面（Desktop）**
你看到的背景图，以及可以放图标、文件快捷方式的那块区域。

**5. 设置工具（Settings）**
调节屏幕分辨率、Wi-Fi、电源、键盘快捷键等。

**6. 桌面搜索（Search）**
快速找到文件、应用、设置的搜索工具。

**7. 控制中心（Control Center）**
所有设置的集中入口，类似 Windows 的"控制面板"。

---

### 桌面环境 vs 窗口管理器

这里有个常见的混淆：**桌面环境 ≠ 窗口管理器**。

- **窗口管理器**（Window Manager）只管窗口的显示和操作，专注于"怎么摆放窗口"，不包括文件管理器、面板、桌面等。
- **桌面环境**（Desktop Environment）是窗口管理器的"豪华升级版"，把窗口管理器 + 文件管理器 + 面板 + 设置工具 + 桌面全部打包在一起。

打个比方：

- **窗口管理器** = 毛坯房（只解决了"有没有窗户"的问题）
- **桌面环境** = 精装修房（窗户、地板、空调、沙发全给你配好）

常见的窗口管理器有：**i3**、**sway**、**awesome**、**Openbox**。这些适合极客，普通人直接用桌面环境就好。

---

### 主流桌面环境一览

Linux 世界里有好几个桌面环境，各有特色：

| 桌面环境 | 特色 | 推荐指数 |
|----------|------|----------|
| **GNOME** | 现代感强，界面简洁，功能丰富，Ubuntu 默认 | ⭐⭐⭐⭐⭐ |
| **KDE Plasma** | 功能最强大，高度可定制，界面华丽 | ⭐⭐⭐⭐⭐ |
| **Xfce** | 轻量级，老旧电脑也能跑，适合低配机器 | ⭐⭐⭐⭐ |
| **MATE** | 经典 GNOME 2 风格，稳定，老用户熟悉 | ⭐⭐⭐ |
| **LXQt** | 另一个轻量级选手，基于 Qt，比 Xfce 还轻 | ⭐⭐⭐ |
| **Deepin** | 国产之光，界面美观，国产用户爱用 | ⭐⭐⭐⭐ |

下一节开始，我们就一个一个来详细介绍！

---

### 小结

桌面环境是 Linux 的"图形化外套"，让 Linux 从"命令行黑客"变成"普通人也能用"的操作系统。

**记住以下关键点：**

1. 桌面环境 = 窗口管理器 + 文件管理器 + 面板 + 桌面 + 设置工具的豪华套餐
2. 服务器通常不需要桌面环境（省资源）
3. 桌面用户必备桌面环境（GNOME 和 KDE 最流行）
4. 窗口管理器是桌面环境的一部分，但不是全部

好了，了解了基本概念，让我们开始深入了解各大桌面环境吧！🚀

---

## 4.2 GNOME 桌面环境详解（Ubuntu 默认）

说到 Linux 桌面环境，**GNOME**（发音：guh-NOH-mee）是当之无愧的老大。

GNOME 诞生于 1999 年，由红帽（Red Hat）公司的几位程序员发起，目标是做一个"简单、人性化、accessible（所有人都能用的）"的 Linux 桌面环境。发展了二十多年，如今 GNOME 已经成为**应用最广泛的 Linux 桌面环境**——Ubuntu、Fedora、Debian 默认都用它。

GNOME 的设计哲学是：**简洁至上**。它的界面非常干净，没有多余的装饰，用起来有种"苹果味"——简单、高效、优雅。

---

### 4.2.1 活动概览（Activities）：应用菜单、工作区

GNOME 最大的特色就是这个"活动概览"（Activities Overview）。

**怎么打开？**

- 方法一：鼠标移动到屏幕左上角（或者点击"Activities"按钮）
- 方法二：按键盘上的 `Super` 键（就是 Windows 键 ⌘ 或 macOS 的 Command 键）
- 方法三：按 `Alt + F1`

打开之后，你会看到：

```
┌─────────────────────────────────────────────────────────┐
│  Activities                              [时间] [网络]  │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐               │
│   │ 📁   │ │ 🌐   │ │ ⚙️   │ │ 📧   │  ← 工作区里的窗口 │
│   │文件   │ │ 浏览器│ │ 设置 │ │ 邮件 │               │
│   └──────┘ └──────┘ └──────┘ └──────┘               │
│                                                         │
│   ┌─────────────────────────────────────┐             │
│   │     🔍 搜索...                       │  ← 搜索栏   │
│   └─────────────────────────────────────┘             │
│                                                         │
│   [Dash 快捷启动栏 - 常用应用图标]                     │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**活动概览里可以做的事：**

1. **切换窗口**：点击工作区里的窗口缩略图，快速切换
2. **搜索应用/文件**：在顶部搜索栏输入关键词，瞬间找到
3. **管理工作区**：右侧可以看到虚拟工作区，拖拽窗口到不同工作区
4. **快速启动应用**：点击 Dash 栏里的图标

---

### 顶部面板：系统托盘、时间、菜单

GNOME 默认在屏幕顶部有一条面板，包含：

**左边：Activities 按钮**
点击或移到左上角 → 打开活动概览。

**中间：时间**
显示当前时间，点击可以看日历和最近事件。

**右边：系统托盘图标**
- 🔔 网络/音量/电池图标
- ⚙️ 设置齿轮 → 快速设置面板
- 🔒 锁屏按钮
- ⚡ 电源按钮（关机/重启）

**快速设置面板**（点右上角齿轮图标）：

```
┌─────────────────────────────────────────┐
│  🔒  夜间模式    省电模式              │
│  🌐 Wi-Fi: 已连接 (MyWiFi)    →       │
│  🔊 音量: ████████░░ 80%              │
│  🔋 电池: ██████████ 95%              │
│  ⚡ 蓝牙: 关闭                          │
│                                         │
│  ⚙️  设置                             │
│  🔌  电源设置                          │
└─────────────────────────────────────────┘
```

---

### 4.2.3 工作区与窗口管理：窗口操作、虚拟桌面

GNOME 支持**虚拟工作区**（Workspace）——把不同的窗口放到不同的工作区，互不干扰。

**典型场景：**

- 工作区 1：浏览器 + 笔记
- 工作区 2：代码编辑器 + 终端
- 工作区 3：音乐播放器 + 聊天窗口

**工作区操作：**

| 操作 | 快捷键 |
|------|--------|
| 打开活动概览 | `Super` |
| 切换到上一个工作区 | `Super + Page Up` |
| 切换到下一个工作区 | `Super + Page Down` |
| 把窗口移到上一个工作区 | `Super + Shift + Page Up` |
| 把窗口移到下一个工作区 | `Super + Shift + Page Down` |

**窗口操作快捷键：**

| 操作 | 快捷键 |
|------|--------|
| 关闭窗口 | `Alt + F4` 或 `Super + Q` |
| 最大化窗口 | `Super + ↑` |
| 最小化窗口 | `Super + H` |
| 恢复窗口 | `Alt + Tab` |
| 切换窗口 | `Alt + Tab`（循环切换）/ `Alt + Esc`（直接切换）|
| 移动窗口（抓取） | `Alt + 鼠标左键拖动` |
| 调整窗口大小 | `Alt + 鼠标右键拖动` |

---

### 4.2.4 GNOME 扩展（Extensions）：安装与管理

GNOME 有一个强大的**扩展（Extensions）**系统，允许用户给 GNOME 添加各种小功能。

**什么是 GNOME 扩展？**

就像浏览器插件（Chrome 扩展）一样，GNOME 扩展是给 GNOME 桌面环境增加额外功能的插件。比如：添加天气插件、任务栏改进、系统监控小工具等。

**去哪里找扩展？**

访问 [https://extensions.gnome.org/](https://extensions.gnome.org/)，这是 GNOME 扩展的官方网站。

**安装扩展的方法：**

**方法一：浏览器安装（推荐）**

1. 先安装浏览器连接插件（Chrome/Firefox 都需要）：
```bash
sudo apt install chrome-gnome-shell
```
2. 用 Firefox 或 Chrome 打开 [https://extensions.gnome.org/](https://extensions.gnome.org/)
3. 首次使用会提示安装浏览器插件，点允许
4. 打开想装的扩展页面，点开关按钮"ON"
5. 浏览器插件会自动安装到你的系统

**方法二：命令行安装**

```bash
# 安装 gnome-extensions-app（图形化管理工具）
sudo apt install gnome-extensions-app

# 安装一个常用扩展（举例）
sudo apt install gnome-shell-extensions
```

**常用扩展推荐：**

| 扩展名 | 功能 |
|--------|------|
| **Dash to Dock** | 把 Dash 变成独立 Dock，比自带的更好用 |
| **Arc Menu** | 给 GNOME 添加开始菜单 |
| **NetSpeed** | 状态栏显示网速 |
| **Top Icons Plus** | 把应用图标放到状态栏 |
| **Coverflow Alt-Tab** | 让 Alt+Tab 变成 macOS 风格的 Coverflow 切换 |

---

### 4.2.5 主题（Themes）：深色/浅色模式

GNOME 支持完全自定义外观，包括主题、图标、桌面壁纸等。

**快速切换深色/浅色模式：**

1. 打开"设置" → "外观"（Appearance）
2. 选择"浅色"或"深色"
3. 或者：点右上角时间 → 打开快速设置 → 找夜间模式开关

**安装第三方主题：**

GNOME 默认主题叫 **Adwaita**（分为浅色版和深色版）。如果你想换换口味：

```bash
# 安装 GNOME Tweaks（主题管理工具）
sudo apt install gnome-tweaks

# 安装用户主题扩展
sudo apt install gnome-shell-extensions

# 打开 GNOME Tweaks
gnome-tweaks
```

在 GNOME Tweaks 里：

```
应用程序 → 外壳主题 → 选择你安装的主题
应用程序 → 图标主题 → 选择图标包
```

**热门主题推荐：**

| 主题名 | 风格 |
|--------|------|
| **Arc** | 扁平化半透明，清晰干净 |
| **Adwaita Dark** | GNOME 官方深色版 |
| **Yaru** | Ubuntu 风格，橙色主题 |
| **Catppuccin** | 马卡龙色系，可爱风 |
| **Orchis** | 现代简约，图标风格 |

**热门图标主题：**

| 图标名 | 风格 |
|--------|------|
| **Papirus** | 扁平化，颜色鲜艳 |
| **Numix** | 简洁圆形，现代感 |
| **Adwaita** | GNOME 官方默认 |

---

### 小结

GNOME 是 Ubuntu 默认的桌面环境，以简洁、现代、功能丰富著称。它的"活动概览"是最大亮点，虚拟工作区和搜索功能也非常实用。

**记住以下关键点：**

1. 按 `Super` 打开活动概览，是 GNOME 的核心入口
2. 虚拟工作区可以把不同任务隔离开，提高效率
3. GNOME 扩展可以给桌面增加各种小功能
4. 用 GNOME Tweaks 管理主题和图标
5. 深色/浅色模式在快速设置里一键切换

---

## 4.3 KDE Plasma 桌面环境（功能丰富，界面美观，高度定制）

如果说 GNOME 是"苹果风"——简洁、统一、有逼格，那 **KDE Plasma** 就是"安卓风"——开放、自由、什么都能改。

KDE 是一个完全不同的设计哲学：**把控制权交给用户**。KDE 几乎每一个细节都可以定制——面板位置、窗口动画、桌面特效、快捷键、主题、图标……全都可以按你的喜好来。喜欢折腾的玩家最爱 KDE。

KDE 的全称是 **K Desktop Environment**，现在正式名称叫 **Plasma**。它诞生于 1996 年，是 Linux 桌面环境中历史最悠久的项目之一。

KDE 默认使用 **Qt** 作为开发框架（这也是它和 GNOME 的根本区别——GNOME 用 GTK），所以 KDE 应用和 GNOME 风格不太一样，但都很漂亮。

---

### 4.3.1 Plasma 桌面组件

KDE Plasma 的界面由多个组件构成，每个都可以独立替换：

**1. 桌面面板（Panel）**
类似 Windows 的任务栏，位于屏幕底部，显示开始菜单、打开的应用图标、系统托盘、时钟等。

**2. 桌面组件（Desktop Widgets）**
KDE 可以在桌面上放各种小工具（Widgets），比如：日历、时钟、天气、系统监控、便签、磁盘使用率……

添加方法：在桌面上右键 → "添加组件" → 选择你喜欢的小工具。

**3. 开始菜单（K Menu）**
点击左下角 KDE 图标，弹出开始菜单，显示所有应用、设置、关机选项。

**4. 活动（Activities）**
KDE 也有"活动"概念，可以创建不同的活动，每个活动有自己独特的桌面配置。

```
┌─────────────────────────────────────────────────────────┐
│  KDE Plasma 桌面概览                                  │
│                                                         │
│  顶部面板 ──────── 日历、时钟、系统托盘、用户菜单     │
│                                                         │
│  ┌──────────────────────────────────────────────────┐ │
│  │ 🕐 桌面小工具：天气 │ 日历 │ 磁盘使用率        │ │
│  └──────────────────────────────────────────────────┘ │
│                                                         │
│  底部面板 ──────── 开始菜单、应用图标、任务栏         │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

### 4.3.2 KDE 应用生态：Konqueror、Dolphin、KWrite

KDE 不仅仅是一个桌面环境，还有一整套自带的 KDE 应用，这些应用和 Plasma 整合得非常好。

**文件管理器：Dolphin**

KDE 自带的文件管理器，功能强大又好看。

```bash
# 在终端打开当前目录的 Dolphin
dolphin .

# 以管理员权限打开（系统文件管理）
kdesu dolphin
```

Dolphin 的特点：
- 内置拆分视图（左右两个窗格）
- 标签页支持（像浏览器一样多标签）
- 彩色文件夹（根据文件类型自动着色）
- 多种视图模式（图标、列表、详情）

**浏览器：Konqueror**

KDE 的网页浏览器，也是文件管理器，定位是"全能型选手"。不过 Firefox 和 Chrome 更流行，Konqueror 更多用来浏览本地文件。

**文本编辑器：Kate**

KDE 自带的代码编辑器，支持语法高亮、多标签、代码折叠、功能丰富。

```bash
# 打开 Kate
kate filename.txt
```

**终端模拟器：Konsole**

KDE 自带的终端，功能比 GNOME 的 Terminal 更强大，支持多标签、分屏、内嵌。

```bash
# 打开 Konsole
konsole
```

**其他 KDE 应用：**

| 应用 | 功能 |
|------|------|
| **Okular** | PDF/电子书阅读器，支持注释 |
| **Spectacle** | 截图工具，比系统自带的好用 |
| **Ark** | 压缩/解压工具，支持 zip、tar、7z 等 |
| **KGet** | 下载管理器 |
| **KMail / Kontact** | 邮件客户端 |
| **KDevelop** | C/C++ IDE（程序员专属） |

---

### 4.3.3 桌面特效与动画

KDE 的一个亮点就是**桌面特效**——窗口动画、桌面切换动画、模糊效果、磨砂玻璃……只要你的显卡够强，KDE 可以把桌面变成炫酷的视觉盛宴。

**怎么开启动画？**

打开"系统设置" → "工作区行为" → "桌面特效"：

```
┌─────────────────────────────────────────────────────────┐
│  桌面特效                                            │
│                                                         │
│  窗口开启动画 ──────                                   │
│    ○ 无                                               │
│    ● 翻转      ← 窗口打开时翻转效果                  │
│    ○ 溶解                                           │
│    ○ 弹跳                                           │
│                                                         │
│  ☑ 窗口最小化/最大化动画                            │
│  ☑ 活动切换动画                                     │
│  ☑ 桌面切换动画                                     │
│                                                         │
│  模糊背景 ──────────                                 │
│    ☑ 面板模糊          ← 磨砂玻璃效果               │
│    ☑ Alt+Tab 模糊背景                               │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**如果你的电脑有点老**，担心动画太耗性能，可以在"系统设置 → 工作空间行为 → 桌面特效"里关掉一些动画。

**窗口特效：**

| 特效 | 说明 |
|------|------|
| **模糊（Blur）** | 窗口后面的背景变成磨砂玻璃效果 |
| **阴影（Shadow）** | 窗口有阴影，更有层次感 |
| **窗口预览（Window Thumbnails）** | Alt+Tab 时显示窗口缩略图 |
| **桌面立方体** | 切换虚拟桌面时旋转立方体效果（需要 3D 加速）|

**低配置机器建议：**

如果你的电脑是 10 年前的配置，用 KDE 可能会卡。建议：

1. 关掉所有桌面特效
2. 选择轻量级面板布局（像 Windows 那种简单面板）
3. 或者考虑用 Xfce（比 KDE 轻量很多）

---

### KDE 的高度定制性

KDE 被誉为"最像 Windows 的 Linux 桌面"，如果你从 Windows 刚转过来，KDE 可能是最容易上手的选择。

**可以定制的部分（几乎无所不包）：**

- 面板位置（顶部/底部/左侧/右侧/多个面板）
- 开始菜单样式（传统风格/现代风格/隐藏）
- 窗口装饰（标题栏按钮位置、边框样式）
- 主题（全局主题、颜色、图标、鼠标指针）
- 字体（选择任意字体，调整大小、渲染方式）
- 快捷键（自定义每一个操作的快捷键）
- 文件关联（什么文件用什么程序打开）

**KDE 系统设置界面一览：**

```
系统设置
├── 工作区行为
│   ├── 桌面特效
│   ├── 工作区
│   ├── 快捷键
│   └── 启动和关机
├── 外观
│   ├── 全局主题
│   ├── 应用风格
│   ├── 窗口装饰
│   ├── 图标主题
│   └── 字体
├── 网络和连接
│   ├── Wi-Fi
│   ├── 蓝牙
│   └── VPN
├── 显示和显示器
│   ├── 分辨率
│   ├── 缩放
│   └── 多显示器
└── 硬件
    ├── 电源管理
    ├── 音频
    └── 输入设备
```

---

### 小结

KDE Plasma 是一个功能极其丰富、高度可定制的桌面环境。如果你喜欢折腾、喜欢把系统打扮成自己喜欢的样子，KDE 是你的最佳选择。

**记住以下关键点：**

1. KDE 基于 Qt 框架，界面华丽，和 GNOME 风格不同
2. Dolphin 是 KDE 自带的文件管理器，功能强大
3. KDE 自带大量应用（Konsole、Kate、Okular 等）
4. 桌面特效很华丽，但老电脑要悠着点开
5. KDE 的定制性几乎无所不能，适合爱折腾的用户

---

## 4.4 Xfce 轻量级桌面（适合老旧电脑，资源占用低）

GNOME 和 KDE 都挺好，但有一个问题：**吃内存**。一台只有 2GB 内存的老爷机，跑 GNOME 卡成翔，跑 KDE 风扇呼呼转。

这时候 **Xfce** 就是救星！

**Xfce**（发音：eks-eff-see-ee）是一个"轻量级"桌面环境，核心理念是：**快速、省资源、稳定**。它的内存占用只有 GNOME 的三分之一，CPU 占用也低很多。

Xfce 最早发布于 1996 年，界面风格有点"复古"——看起来有点像 Windows XP 时代的感觉，但这恰恰是它的魅力：简洁、朴素、不花哨。

---

### 4.4.1 Xfce 面板与菜单

Xfce 的界面和 GNOME/KDE 都不太一样，更接近传统的"面板+菜单"风格。

**顶部面板：**

- 左边：应用菜单（类似 Windows 开始菜单）
- 中间：打开的窗口按钮（和 Windows 任务栏一样）
- 右边：系统托盘（音量、网络、电源、时钟）

**桌面：**

- 桌面可以放文件图标（双击打开）
- 右键桌面 → 可以更改壁纸、创建启动器等

```
┌─────────────────────────────────────────────────────────┐
│  [Xfce 应用菜单]  [窗口1] [窗口2]    [🔊][🌐][⚡]14:30 │
├─────────────────────────────────────────────────────────┤
│                                                         │
│    🖥️ 我的电脑    📁 主文件夹    🗑️ 回收站            │
│                                                         │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**应用菜单：**

点击左上角 Xfce 图标，弹出应用菜单，按分类显示所有已安装的应用。

**设置管理器：**

Xfce 自带一个"设置管理器"，集中管理所有设置：

```bash
# 打开 Xfce 设置管理器（图形界面）
xfce4-settings-manager
```

---

### 4.4.2 窗口管理器配置

Xfce 的窗口管理器叫 **xfwm4**，轻量但功能也不少。

**窗口操作快捷键：**

| 操作 | 快捷键 |
|------|--------|
| 关闭窗口 | `Alt + F4` |
| 最大化 | `Alt + F10` |
| 最小化 | `Alt + F9` |
| 移动窗口 | `Alt + 鼠标左键拖动` |
| 调整大小 | `Alt + 鼠标右键拖动` |
| 切换窗口 | `Alt + Tab` |
| 显示桌面 | `Ctrl + Alt + D` |

**窗口对贴（Tiling）：**

Xfce 支持简单的窗口对贴（把两个窗口自动左右排列）。开启方法：

1. 打开"设置管理器" → "窗口管理器"
2. 找"对贴"（Tiling）选项
3. 启用"启用窗口对贴"

启用后，拖动窗口贴到屏幕边缘，窗口会自动占满半边屏幕。

**主题设置：**

Xfce 自带几个主题，也可以安装第三方主题：

```bash
# 安装主题
sudo apt install xfce4-goodies  # 包含额外主题和插件

# 更改主题：设置管理器 → 窗口管理器 → 风格
```

---

### Xfce 的资源占用对比

为什么要用 Xfce？因为它真的**超级省资源**！

| 桌面环境 | 内存占用（空载） | 最低内存要求 |
|----------|-----------------|-------------|
| GNOME | ~800MB - 1GB | 2GB+ |
| KDE | ~600MB - 900MB | 2GB+ |
| **Xfce** | ~200MB - 300MB | 512MB |
| LXQt | ~150MB - 250MB | 512MB |

实测数据（虚拟机，空载桌面）：

```
桌面环境     内存占用     CPU (空载)
─────────────────────────────────
GNOME        980 MB      1-2%
KDE          720 MB      1-3%
Xfce         280 MB      <1%
LXQt         220 MB      <1%
```

如果你有一台旧笔记本电脑，Xfce 可以让它"焕发第二春"！

---

### 小结

Xfce 是一个轻量级桌面环境，资源占用极低，适合老旧电脑和低配置机器。

**记住以下关键点：**

1. Xfce 内存占用只有 GNOME 的三分之一
2. 界面风格传统，类似 Windows XP
3. 自带窗口对贴功能
4. 老电脑/低配置首选 Xfce

---

## 4.5 MATE 桌面环境（经典 GNOME 2 风格）

**MATE** 是一个很有意思的桌面环境——它是 GNOME 2 的"精神续作"。

当年 GNOME 3 大改版，把经典 GNOME 2 的界面完全推倒重来，变成现在的 GNOME Shell 风格。很多老用户不习惯，觉得"变了味道"。于是，一群人决定在 GNOME 2 的代码基础上继续开发，起了个新名字：**MATE**。

**MATE** 这个名字也挺有意思——来自阿根廷的一种植物 **"yerba mate"**（耶巴马黛茶），和 GNOME 的中文名"果纳"形成呼应（果纳 = GNOME = 一种中东真菌名 🌿）。

MATE 的核心理念是：**保持经典，熟悉感强**。如果你用过 Windows XP/Vista 时代的经典界面，MATE 会让你有回家的感觉。

---

### 4.5.1 MATE 组件

MATE 保留了 GNOME 2 时代的经典组件，每个组件都有 GNOME 2 的血统：

| MATE 组件 | 功能 |
|-----------|------|
| **Caja** | 文件管理器（对应 GNOME 2 的 Nautilus）|
| **Pluma** | 文本编辑器（对应 gedit）|
| **Eye of GNOME (eog)** | 图片查看器 |
| **Atril** | PDF 阅读器（对应 evince）|
| **Engrampa** | 压缩/解压工具 |
| **MATE Terminal** | 终端模拟器 |
| **Marco** | 窗口管理器 |
| **Mozo** | 菜单编辑器 |
| **MATE Panel** | 面板（顶部面板+底部面板）|

**MATE 的界面：**

```
┌─────────────────────────────────────────────────────────┐
│ [应用程序] [位置] [系统]     [网络][🔊][📅]14:30 [👤] │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   🖥️ 我的电脑    📁 主文件夹    🗑️ 回收站            │
│                                                         │
│   📄 notes.txt   📄 todo.md                           │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

MATE 默认有两个面板：**顶部面板**（菜单+系统托盘）和**底部面板**（窗口列表+工作区切换器）。

---

### 4.5.2 MATE 桌面环境

MATE 最大的特点就是：**你认识它**。

无论你之前用的是 Windows XP、Windows 7，还是 macOS，MATE 的操作逻辑都不会让你感到陌生。没有 GNOME 那种"激进"的界面变化，也没有 KDE 那种"什么都可改"的复杂度。MATE 就像是 Linux 世界里的"经典老店"，味道始终如一。

**适合人群：**

- 从 Windows 刚转过来的新手（操作逻辑接近 Windows）
- 老机器用户（MATE 资源占用也不高，约 400-500MB）
- 怀念经典 GNOME 2 界面的老用户
- 不喜欢花哨特效，追求稳定实用的用户

**安装 MATE：**

```bash
# Ubuntu/Mint 安装 MATE
sudo apt install mate-desktop-environment

# 安装完整版（推荐）
sudo apt install mate-desktop-environment-extras

# 登录时在 GDM 登录界面选择 MATE 会话
```

**MATE vs GNOME 3 对比：**

| 对比项 | MATE | GNOME 3 |
|--------|------|---------|
| 界面风格 | 经典 Windows 风格 | 现代简洁 |
| 学习成本 | 低 | 中 |
| 资源占用 | ~500MB | ~900MB |
| 可定制性 | 中等 | 中等 |
| 扩展系统 | 有限 | GNOME 扩展 |

---

### 小结

MATE 是 GNOME 2 的精神续作，适合怀念经典界面、不喜欢激进变化的用户。

**记住以下关键点：**

1. MATE 起源于 GNOME 2，界面风格经典
2. 操作逻辑接近 Windows，上手容易
3. 资源占用中等，老机器也能跑
4. 适合从 Windows 转过来的新手

---

## 4.6 窗口管理器：i3、sway、openbox、awesome（极客玩法，键盘驱动）

前面讲的 GNOME、KDE、Xfce、MATE 都是**桌面环境**——它们是一个完整的套件，包含窗口管理器、面板、文件管理器、设置工具等。

但有些"硬核玩家"不需要这些花里胡哨的东西，他们只要：**窗口管理器**。

窗口管理器只负责窗口的摆放和操作，不包含文件管理器、面板、桌面等。没有图形桌面，没有应用菜单，一切从终端开始。

这听起来很疯狂，但一旦习惯了，效率极高——因为**完全不用鼠标**，所有操作靠键盘完成！

---

### 4.6.1 平铺式窗口管理器

**平铺式窗口管理器**（Tiling Window Manager）是窗口管理器里的"异类"——它会自动把窗口铺满屏幕，不需要你手动调整大小。

想象一下：你打开两个窗口，一个左边占一半，一个右边占一半；打开第三个窗口，前两个自动缩小，第三个占下半屏。窗口们像瓦片一样整整齐齐地"贴"在屏幕上。

**代表选手：**

- **i3**：最流行的平铺式窗口管理器，文档完善，社区活跃
- **sway**：i3 的 Wayland 移植版（i3 是 X11，sway 是 Wayland）
- **bspwm**：另一种平铺式窗口管理器，配合 sxhkd 快捷键守护进程使用
- **herbstluftwm**：极简主义者的选择，X11 平台

**i3 的工作原理：**

i3 把屏幕分成多个"容器"（containers），每个容器可以装一个或多个窗口。容器可以嵌套、分割、调整大小。

```
┌─────────────────┬─────────────────┐
│                 │                 │
│    终端 1       │    终端 2       │
│                 │                 │
├─────────────────┼─────────────────┤
│                 │                 │
│    浏览器        │    浏览器        │
│                 │                 │
└─────────────────┴─────────────────┘

用户按 $mod+d → 弹出 dmenu（应用启动器）
按 $mod+Enter → 打开新终端
按 $mod+h/j/k/l → 在窗口间移动焦点
```

**i3 的快捷键（$mod = Mod4，通常是 Win 键）：**

| 快捷键 | 操作 |
|--------|------|
| `$mod + Enter` | 打开新终端 |
| `$mod + d` | 打开 dmenu（输入程序名启动） |
| `$mod + h/j/k/l` | 在窗口间移动焦点 |
| `$mod + Shift + h/j/k/l` | 移动窗口 |
| `$mod + f` | 全屏切换 |
| `$mod + v` | 垂直分割 |
| `$mod + h` | 水平分割 |
| `$mod + r` | 进入调整大小模式 |
| `$mod + e` | 退出 i3（注销）|

---

### 4.6.2 动态窗口管理器

除了平铺式，还有一类**动态窗口管理器**，能够根据窗口状态自动调整布局。

**代表选手：**

- **awesome**：高度可配置的动态窗口管理器，用 Lua 脚本定制一切
- **xmonad**：用 Haskell 配置的窗口管理器，代码即配置
- **labwc**：Wayland 平台的动态窗口管理器

**awesome 的特色：**

awesome 的界面很有个性——窗口浮动在屏幕上，可以自由拖动，也可以自动排列成网格、最大化、居中等状态。

awesome 的配置文件是 Lua 脚本，如果你会编程，可以把 awesome 定制成任何你想要的样子。

```
awesome 界面示例：

┌──────────────┐
│ 🏠 桌面 1    │
├──────────────┤
│ ┌────┐ ┌───┐ │
│ │终端│ │浏览器│ │  ← 网格布局
│ └────┘ └───┘ │
│ ┌────────┐   │
│ │ 文件管理器│ │  ← 浮动窗口
│ └────────┘   │
└──────────────┘
```

**适合人群：**

窗口管理器适合：

1. **程序员/运维工程师** — 经常在多个终端和编辑器之间切换，键盘操作效率极高
2. **极客/Geek** — 喜欢折腾，追求极致效率和个性化
3. **屏幕空间紧张的用户** — 笔记本用户，需要最大化利用屏幕

**不适合人群：**

1. **普通桌面用户** — 没有文件管理器、图标桌面，用起来很不习惯
2. **追求美观但不折腾的用户** — 窗口管理器界面朴素，不花哨
3. **新手小白** — 学习曲线陡峭，配置复杂

---

### 小结

窗口管理器是 Linux 世界里的"极客专属"。它们不需要花哨的界面，只需要高效的操作。

**记住以下关键点：**

1. 窗口管理器只负责窗口操作，不包含桌面环境全套组件
2. 平铺式窗口管理器（i3/sway）自动排列窗口，不用鼠标
3. 窗口管理器用键盘操作，效率极高
4. 适合程序员和极客，不适合普通用户

---

## 4.7 桌面基本操作与快捷键

不管你用的是 GNOME、KDE 还是 Xfce，桌面环境的基本操作都是相通的。学会这些快捷键，能让你的操作效率翻倍！

---

### 4.7.1 窗口操作：最大化、最小化、关闭

**通用窗口操作（大多数桌面环境）：**

| 操作 | 快捷键 |
|------|--------|
| 关闭窗口 | `Alt + F4` |
| 最大化窗口 | `Alt + F10` 或 `Super + ↑` |
| 最小化窗口 | `Alt + F9` 或 `Super + H` |
| 恢复窗口 | `Alt + Tab` |
| 全屏切换 | `F11` |

**GNOME 专用：**

| 操作 | 快捷键 |
|------|--------|
| 关闭窗口 | `Super + Q` |
| 最大化 | `Super + ↑` |
| 最小化 | `Super + H` |
| 移动窗口 | `Alt + 鼠标左键拖动` |
| 调整大小 | `Alt + 鼠标右键拖动` |

---

### 4.7.2 工作区切换：Super + Tab

工作区（Workspace）是桌面环境的杀手级功能，可以把不同任务放到不同工作区，互不干扰。

**GNOME 工作区切换：**

| 操作 | 快捷键 |
|------|--------|
| 打开活动概览 | `Super` |
| 切换工作区 | `Super + Page Up/Down` |
| 把窗口移到另一个工作区 | `Super + Shift + Page Up/Down` |
| 显示所有工作区的窗口 | `Super + S` |

**KDE 工作区切换：**

| 操作 | 快捷键 |
|------|--------|
| 切换虚拟桌面 | `Ctrl + F1/F2/F3...` |
| 把窗口移到另一个虚拟桌面 | `Ctrl + Shift + F1/F2...` |

---

### 4.7.3 截图快捷键

Linux 各桌面环境的截图快捷键：

**GNOME：**

| 操作 | 快捷键 |
|------|--------|
| 全屏截图 | `Print Screen` |
| 窗口截图 | `Alt + Print Screen` |
| 区域截图 | `Shift + Print Screen` |
| 截图并复制到剪贴板 | `Ctrl + Print Screen` |

**KDE Plasma：**

| 操作 | 快捷键 |
|------|--------|
| 全屏截图 | `Print Screen` |
| 窗口截图 | `Alt + Print Screen` |
| 区域截图 | `Shift + Print Screen` |
| 延迟截图 | `Ctrl + Print Screen` |

KDE 自带的截图工具叫 **Spectacle**，功能很强大，支持延迟截图、标注、复制到剪贴板等。

**Xfce：**

| 操作 | 快捷键 |
|------|--------|
| 全屏截图 | `Print Screen` |
| 窗口截图 | `Alt + Print Screen` |
| 区域截图 | `Shift + Print Screen` |

---

### 通用截图命令（终端可用）

如果快捷键失灵，或者你想用命令截图：

```bash
# GNOME 环境截图（gnome-screenshot）
gnome-screenshot                          # 全屏截图
gnome-screenshot -w                        # 窗口截图
gnome-screenshot -a                        # 区域截图
gnome-screenshot -w -B                     # 窗口截图（不带边框）

# KDE 环境截图（spectacle）
spectacle                                  # 交互式截图
spectacle -f                               # 全屏
spectacle -w                               # 窗口
spectacle -r                               # 区域

# 通用工具（ImageMagick）
import -window root screenshot.png          # 全屏截图
import screenshot.png                       # 区域截图

# 截图保存位置
# GNOME: ~/Pictures/
# KDE: ~/Pictures/
# Xfce: ~/Pictures/Screenshots/
```

---

### 小结

掌握桌面环境的快捷键是提升效率的关键！花 10 分钟记住常用的快捷键，以后操作快如闪电。

**记住以下关键点：**

1. `Alt + F4` 关闭窗口，`Alt + Tab` 切换窗口（通用）
2. `Super` 是 Linux 的"Windows 键"，是桌面操作的精髓
3. `Print Screen` 全屏截图，`Alt + Print Screen` 窗口截图
4. 工作区可以大幅提高多任务效率

---

## 4.8 系统设置详解

装好了桌面环境，总得调教一番。Linux 的桌面环境都有一套完整的系统设置面板，这一节我们逐一讲解各个设置项。

---

### 4.8.1 网络设置：有线、无线、VPN

网络是 Linux 桌面最核心的功能之一。没有网络，你的浏览器打不开网页，终端更新不了软件包，一切等于零。

**GNOME 网络设置：**

打开"设置" → "网络"（或者点右上角系统托盘的网络图标）：

```
┌─────────────────────────────────────────┐
│  网络设置                               │
│                                         │
│  ┌─────────────────────────────────┐   │
│  │ 🔌 有线（已连接）  ← 插网线了   │   │
│  └─────────────────────────────────┘   │
│                                         │
│  ┌─────────────────────────────────┐   │
│  │ 📶 Wi-Fi              →        │   │
│  └─────────────────────────────────┘   │
│                                         │
│  ┌─────────────────────────────────┐   │
│  │ 🔒 VPN                 →        │   │
│  └─────────────────────────────────┘   │
│                                         │
└─────────────────────────────────────────┘
```

**连接 Wi-Fi：**

1. 点"Wi-Fi" → 开启 Wi-Fi 开关
2. 点"未连接" → 选择你的 Wi-Fi 名
3. 输入密码，点"连接"

**VPN 连接：**

1. 点"VPN" → 点 "+" 添加 VPN
2. 选择 VPN 类型（OpenVPN/L2TP/IPSec）
3. 填入 VPN 服务器地址、用户名、密码
4. 保存后点"连接"

**命令行设置网络（服务器/高级用户）：**

```bash
# 查看网络接口
ip link show
# 或者
nmcli device status

# 连接 Wi-Fi（命令行）
nmcli device wifi list                      # 扫描 Wi-Fi
nmcli device wifi connect "WiFi名称" password "密码"   # 连接

# 断开网络
nmcli device disconnect enp0s3

# 查看 IP 地址
ip addr show
```

---

### 4.8.2 声音设置：音量调节、音频设备

声音设置包括：音量调节、输入/输出设备选择、音频主题等。

**GNOME 声音设置：**

打开"设置" → "声音"：

```
┌─────────────────────────────────────────┐
│  声音设置                               │
│                                         │
│  输出设备 ────────                      │
│  扬声器 (Built-in Audio)      [▓▓▓▓▓░] 80% │
│                                         │
│  输入设备 ────────                      │
│  麦克风 (Built-in Audio)       [▓▓░░░░] 40% │
│                                         │
│  音量级别快捷键                         │
│  🔊 音量: F2                           │
│  🎤 静音: F1                           │
│                                         │
└─────────────────────────────────────────┘
```

**调节音量：**

- 方法一：点击右上角系统托盘的音量图标，拖动滑块
- 方法二：用快捷键 `F1`（静音）、`F2`（减小音量）、`F3`（增大音量）
- 方法三：命令行调节

```bash
# 查看音量级别（pacmd 或 amixer）
amixer get Master

# 设置音量到 50%
amixer set Master 50%

# 静音
amixer set Master mute

# 取消静音
amixer set Master unmute
```

**切换音频输出设备（如果你有多个声卡或蓝牙耳机）：**

```bash
# 查看可用 sinks（输出设备）
pactl list short sinks

# 切换默认输出设备（把 <sink名称> 换成上一步查到的名字）
pactl set-default-sink <sink名称>

# 切换到 HDMI 输出
pactl set-default-sink alsa_output.hdmi-stereo
```

---

### 4.8.3 显示设置：分辨率、缩放、多显示器

显示设置可能是桌面环境里最重要的设置之一——分辨率不对，看起来眼睛会瞎掉的。

**GNOME 显示设置：**

打开"设置" → "显示"：

```
┌─────────────────────────────────────────────────────────┐
│  显示设置                                               │
│                                                         │
│  分辨率 ──────────────────────                         │
│  [ 1920 x 1080 (16:9) ]  ← 当前分辨率             │
│                                                         │
│  缩放 ────────────────────────                         │
│  100%  ●───────────────○  200%                      │
│       125%                                              │
│                                                         │
│  夜间模式 ────────────────────                          │
│  [ 关闭 ]  ●───────────○  开启                        │
│                                                         │
│  方向 ──────────────────────                           │
│  ○ 正常  ● 90°  ○ 180°  ○ 270°                     │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**多显示器设置：**

如果你有外接显示器，打开"显示"设置后会看到两个显示器图标：

```
┌──────────────────┐    ┌──────────────────┐
│  内置显示器       │    │  外接显示器      │
│  1920x1080       │    │  1920x1080       │
│  [主显示器 ✓]    │    │                  │
│                  │    │                  │
│  [镜像显示]       │    │                  │
│                  │    │                  │
└──────────────────┘    └──────────────────┘
```

**常用操作：**

| 操作 | 说明 |
|------|------|
| **镜像模式** | 两个屏幕显示相同内容（适合投影） |
| **扩展模式** | 两个屏幕显示不同内容（一个屏幕当副屏） |
| **设为主显示器** | 任务栏、通知显示在哪个屏幕 |
| **分辨率** | 每个屏幕单独设置分辨率 |
| **缩放** | HiDPI（高分屏）缩放比例 |

**命令行设置分辨率（高级用户）：**

```bash
# 查看显示器名称
xrandr --listmonitors

# 设置分辨率为 1920x1080
xrandr --output HDMI-1 --mode 1920x1080

# 设置缩放为 125%
xrandr --output eDP-1 --scale 1.25x1.25

# 关闭某个显示器
xrandr --output HDMI-1 --off
```

---

### 4.8.4 电源管理：节能模式、睡眠

笔记本用户最关心的就是电池续航。Linux 的电源管理可以帮你省电、延长电池使用时间。

**GNOME 电源设置：**

打开"设置" → "电源"：

```
┌─────────────────────────────────────────┐
│  电源设置                               │
│                                         │
│  省电 ─────────                        │
│  [──────────────●──────────────]        │
│  性能优先 ◄──────●──────► 省电优先     │
│                                         │
│  笔记本电池 ──────                     │
│  亮度: [▓▓▓▓▓▓▓░░░] 70%            │
│                                         │
│  睡眠: 插入电源: [从不        ▼]       │
│       电池供电:   [10 分钟    ▼]       │
│                                         │
│  自动挂起 ──────────────────           │
│  ☑ 合上笔记本盖子时挂起                │
│  ☐ 息屏时挂起                         │
│                                         │
└─────────────────────────────────────────┘
```

**命令行电源管理：**

```bash
# 查看当前电源状态
upower -i /org/freedesktop/UPower/devices/battery_BAT0

# 设置屏幕多久后关闭（5分钟后）
gsettings set org.gnome.desktop.session idle-delay 300

# 禁止笔记本盖子合上时休眠
sudo systemctl mask sleep.target suspend.target hibernate.target hybrid-sleep.target

# 允许笔记本盖子合上时休眠
sudo systemctl unmask sleep.target suspend.target hibernate.target hybrid-sleep.target
```

---

### 4.8.5 键盘与鼠标设置

**键盘设置：**

打开"设置" → "键盘"：

```
┌─────────────────────────────────────────┐
│  键盘设置                               │
│                                         │
│  键入 ─────────                        │
│  重复延迟: [短─────────○───长]        │
│  重复速度: [快───────○─────慢]          │
│  光标闪烁: ☑ 启用                      │
│                                         │
│  快捷键 ─────────                      │
│  快捷键可以查看和自定义所有系统快捷键  │
│                                         │
│  [查看快捷键 ▼]                        │
│  [自定义快捷键 ▼]                      │
│                                         │
└─────────────────────────────────────────┘
```

**常用键盘快捷键（GNOME 默认）：**

| 快捷键 | 功能 |
|--------|------|
| `Super` | 打开活动概览 |
| `Alt + Tab` | 切换窗口 |
| `Super + L` | 锁屏 |
| `Super + A` | 显示应用菜单 |
| `Super + Tab` | 在工作区之间切换 |
| `Ctrl + Alt + T` | 打开终端 |
| `Print Screen` | 全屏截图 |

**自定义快捷键：**

1. 打开"设置" → "键盘" → "自定义快捷键"
2. 点 "+" 添加新快捷键
3. 输入名称、命令、设置快捷键

```bash
# 示例：把 Ctrl+Alt+T 设置为打开终端（如果默认不是这个）
# 在"自定义快捷键"里添加：
# 名称: 打开终端
# 命令: gnome-terminal
# 快捷键: Ctrl+Alt+T
```

**鼠标设置：**

打开"设置" → "鼠标与触控板"：

| 设置项 | 说明 |
|--------|------|
| 鼠标速度 | 调节指针移动速度 |
| 触控板速度 | 笔记本触控板灵敏度 |
| 自然滚动 | 滚轮方向（和手机一样） |
| 点击 | 是否开启"轻触点击"（tap-to-click） |
| 鼠标加速 | 鼠标移动的加速度曲线 |

---

### 小结

系统设置是桌面环境的核心，掌握了这些设置项，你就真正掌控了你的 Linux 桌面。

**记住以下关键点：**

1. 网络设置：右上角托盘或"设置 → 网络"
2. 声音设置：调节音量、切换输出设备
3. 显示设置：分辨率、缩放、多显示器
4. 电源管理：笔记本电池续航的关键
5. 键盘快捷键：自定义快捷键可以大幅提高效率

---

## 4.9 主题美化

Linux 桌面环境最大的乐趣之一就是：**想换成什么风格，就换成什么风格**。

Windows 和 macOS 你只能换换壁纸，Linux 可以换主题、换图标、换光标、换字体、换窗口装饰……从"性冷淡风"到"赛博朋克"全凭你心情。

---

### 4.9.1 图标主题：Numix、Papirus

图标主题决定了桌面上各种应用图标的样子。一套好的图标主题可以让桌面看起来焕然一新。

**GNOME 安装图标主题：**

```bash
# 安装 GNOME Tweaks（主题管理必备工具）
sudo apt install gnome-tweaks gnome-shell-extensions

# 安装热门图标主题
sudo apt install papirus-icon-theme      # Papirus 图标主题
sudo apt install numix-icon-theme        # Numix 图标主题

# 打开 GNOME Tweaks
gnome-tweaks
```

在 GNOME Tweaks 里：左侧选"外观" → 右侧找到"图标" → 选择你安装的主题。

**推荐图标主题：**

| 图标主题 | 风格 | 适合人群 |
|----------|------|----------|
| **Papirus** | 扁平化、颜色鲜艳、现代感强 | 喜欢鲜艳色彩的 |
| **Numix** | 简洁圆形、设计感强 | 喜欢简约的 |
| **Adwaita** | GNOME 官方默认，朴素实用 | 喜欢原味的 |
| **Breeze** | KDE 风格，蓝白色调 | KDE 用户 |
| **La Capitaine** | macOS 风格，圆角图标 | 喜欢 macOS 风格的 |

**手动安装图标主题（下载方式）：**

1. 去 [https://www.gnome-look.org/](https://www.gnome-look.org/) 下载图标包（`.tar.xz` 格式）
2. 解压到 `~/.local/share/icons/` 或 `/usr/share/icons/`（需要 root）

```bash
# 解压并安装图标主题（以 Papirus 为例）
cd ~/Downloads
tar -xf Papirus.tar.xz
mv Papirus ~/.local/share/icons/
```

---

### 4.9.2 GTK 主题：Adwaita、Arc

**GTK 主题** 决定了窗口边框、按钮、滚动条、输入框等 UI 元素的外观。

**安装热门 GTK 主题：**

```bash
# 安装 Arc 主题（最流行的第三方 GTK 主题之一）
sudo apt install arc-theme

# 安装 Adwaita 主题（GNOME 默认）
sudo apt install gnome-themes-extra

# 安装 Flat-Plat 主题
sudo add-apt-repository ppa:noobslab/themes
sudo apt update
sudo apt install flat-plat
```

**在 GNOME Tweaks 里切换主题：**

1. 打开 GNOME Tweaks → "外观"
2. 找到"应用程序" → 选择窗口边框主题
3. 找到"Shell" → 选择 Shell 主题

**推荐 GTK 主题：**

| 主题名 | 风格 | 特点 |
|--------|------|------|
| **Arc** | 扁平半透明 | 清晰透明，极简风格 |
| **Adwaita** | GNOME 官方 | 朴素实用 |
| **Yaru** | Ubuntu 风格 | 橙色调，Ubuntu 同款 |
| **Vimix** | 现代扁平 | 多色可选 |
| **Ant** | 深色主题 | 适合夜猫子 |

---

### 4.9.3 桌面壁纸

桌面壁纸应该是最简单、最直接的美化方式了。

**更换桌面壁纸：**

1. 右键桌面空白处 → "更改桌面背景"
2. 或者打开"设置" → "背景"

**壁纸来源推荐：**

| 网站 | 说明 |
|------|------|
| [Unsplash](https://unsplash.com) | 免费高清摄影图，质量极高 |
| [Wallhaven](https://wallhaven.cc) | 壁纸社区，图多质量高 |
| [Reddit r/wallpaper](https://reddit.com/r/wallpaper) | 社区精选壁纸 |
| [GNOME Wiki](https://wiki.gnome.org/Artwork) | GNOME 官方艺术作品 |

**命令行设置壁纸（GNOME）：**

```bash
# 设置壁纸（用 gsettings）
gsettings set org.gnome.desktop.background picture-uri 'file:///home/liming/Pictures/wallpaper.jpg'
gsettings set org.gnome.desktop.background picture-uri-dark 'file:///home/liming/Pictures/wallpaper-dark.jpg'

# 查看当前壁纸设置
gsettings get org.gnome.desktop.background picture-uri
```

---

### 4.9.4 GNOME Tweaks 工具

**GNOME Tweaks** 是 GNOME 桌面环境必备的美化工具，没有它，很多主题和扩展无法生效。

**安装：**

```bash
sudo apt install gnome-tweaks
```

**GNOME Tweaks 能做的事：**

```
GNOME Tweaks
├── 外观
│   ├── 主题
│   │   ├── 应用程序 (GTK 主题)
│   │   ├── 窗口装饰 (窗口边框主题)
│   │   ├── Shell (GNOME Shell 主题)
│   │   └── 图标
│   ├── 壁纸
│   └── 锁屏界面
├── 字体
│   ├── 字体
│   ├── 窗口标题
│   └── 缩放
├── 扩展
│   └── 管理 GNOME 扩展
├── 电源
│   └── 电源按钮行为
├── 键盘和鼠标
│   ├── 鼠标
│   ├── 触控板
│   └── 快捷键
└── 虚拟键盘
    └── 屏幕键盘设置
```

**Top 10 必须装的 GNOME 扩展（配合 Tweaks 使用）：**

| 扩展名 | 功能 |
|--------|------|
| **Dash to Dock** | 把 Dash 变成独立 Dock |
| **User Themes** | 允许用户加载第三方 Shell 主题 |
| **NetSpeed** | 状态栏显示网速 |
| **Clipboard Indicator** | 剪贴板历史记录 |
| **OpenWeather** | 状态栏显示天气 |
| **Desktop Icons NG** | 桌面图标（替代 GNOME 原生） |
| **Coverflow Alt-Tab** | Alt+Tab 变成 Coverflow 效果 |
| **Hide Top Bar** | 全屏时自动隐藏顶栏 |
| **Blur My Shell** | 给 Shell 添加模糊效果 |
| **Vitals** | 显示 CPU、内存、磁盘、温度等系统信息 |

---

### 小结

Linux 桌面美化是门艺术，也是乐趣。主题、图标、壁纸、扩展……组合起来，可以让桌面变成全世界独一无二的样子。

**记住以下关键点：**

1. GNOME Tweaks 是美化必备工具
2. 图标主题改应用图标，GTK 主题改窗口样式
3. 去 gnome-look.org 和 wallhaven.cc 下载主题和壁纸
4. GNOME 扩展可以给桌面增加各种有趣功能

---

## 4.10 常用软件安装

装好了桌面环境，下一步就是安装日常使用的软件了。和 Windows 不同，Linux 的软件安装方式有很多种，每种都有自己的适用场景。

---

### 4.10.1 浏览器：Firefox、Chrome、Chromium

Linux 上最常用的浏览器有三个：

**Firefox（火狐）** — Linux 默认预装的浏览器，开源、隐私保护强、内置开发者工具。

```bash
# Firefox 通常预装了（Ubuntu 22.04 默认是 Snap 版）
# 如果你想手动安装 deb 版（非 Snap）：
sudo snap install firefox

# 或者通过 PPA 安装（非 Snap 版）：
sudo add-apt-repository ppa:mozillateam/ppa
sudo apt update
sudo apt install firefox
```

**Google Chrome** — 功能最全，生态最丰富，和 Google 账号同步。

```bash
# 下载 Chrome（去官网下载 .deb 包）
# https://www.google.com/chrome/

# 或者用命令行下载：
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb

# 安装 .deb 包
sudo dpkg -i google-chrome-stable_current_amd64.deb

# 如果遇到依赖问题，修复：
sudo apt install -f
```

**Chromium** — Chrome 的开源版，功能和 Chrome 类似，但没有 Google 的一些专有组件。

```bash
# 安装 Chromium（Ubuntu 22.04+ 包名是 chromium）
sudo apt install chromium

# 或者通过 Snap：
sudo snap install chromium
```

**三浏览器对比：**

| 浏览器 | 优点 | 缺点 |
|--------|------|------|
| Firefox | 开源、隐私保护强 | Google 同步不原生 |
| Chrome | Google 生态完善、性能强 | 闭源 |
| Chromium | 开源、接近 Chrome | 没有 Widevine（看 Netflix 需额外配置）|

---

### 4.10.2 办公软件：LibreOffice、WPS Office

**LibreOffice** — Linux 上最流行的免费办公套件，Word/Excel/PPT 全能。

```bash
# 安装 LibreOffice（Ubuntu 通常预装了）
sudo apt install libreoffice

# 安装完整版（含所有语言包）
sudo apt install libreoffice-full
```

**WPS Office** — 国产办公软件，界面美观，兼容 Microsoft Office 格式。

```bash
# WPS 没有 apt 包，需要去官网下载 .deb
# 官网: https://www.wps.com/

# 下载后安装：
sudo dpkg -i wps-office_*.deb
```

> ⚠️ WPS 安装后可能会提示缺少字体（主要是微软雅黑等 Windows 字体），可以自己从 Windows 系统拷贝字体到 `/usr/share/fonts/`。

**Microsoft Office 替代方案总结：**

| 软件 | 格式兼容度 | 费用 |
|------|-----------|------|
| LibreOffice | ⭐⭐⭐⭐ 高 | 免费 |
| WPS Office | ⭐⭐⭐⭐⭐ 极高 | 免费（有广告） |
| Google Docs | ⭐⭐⭐⭐ 在线 | 免费 |

---

### 4.10.3 多媒体：VLC、Audacity、GIMP

**VLC 播放器** — 视频播放器里的"瑞士军刀"，几乎什么格式都能放。

```bash
sudo apt install vlc
```

**Audacity** — 音频编辑器，录音、降噪、剪辑全能。

```bash
sudo apt install audacity
```

**GIMP** — 图片编辑器，Linux 版的 Photoshop，免费开源。

```bash
sudo apt install gimp
```

**其他多媒体推荐：**

| 软件 | 功能 | 安装命令 |
|------|------|----------|
| **Shotcut** | 视频剪辑 | `sudo apt install shotcut` |
| **Blender** | 3D 建模/动画 | `sudo snap install blender` |
| **HandBrake** | 视频格式转换 | `sudo apt install handbrake` |
| **OBS Studio** | 屏幕录制/直播 | `sudo apt install obs-studio` |
| **Audacity** | 音频编辑 | `sudo apt install audacity` |
| **Rhythmbox** | 音乐播放 | `sudo apt install rhythmbox` |
| **Picard** | 音乐封面/元数据 | `sudo apt install picard` |

---

### 4.10.4 开发工具：VS Code、JetBrains

**Visual Studio Code** — 微软出品的代码编辑器，轻量、可扩展、插件丰富。

```bash
# 方法一：通过官方 apt 仓库安装（推荐）
wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg
sudo install -o root -g root -m 644 packages.microsoft.gpg /usr/share/keyrings/
sudo sh -c 'echo "deb [arch=amd64 signed-by=/usr/share/keyrings/packages.microsoft.gpg] https://packages.microsoft.com/repos/vscode stable main" > /etc/apt/sources.list.d/vscode.list'
sudo apt update
sudo apt install code

# 方法二：通过 Snap 安装
sudo snap install --classic code
```

**JetBrains 全家桶** — 最好用的 IDE 系列，PyCharm、IntelliJ、WebStorm……

```bash
# JetBrains Toolbox App（管理所有 JetBrains IDE 的工具）
# 下载地址: https://www.jetbrains.com/toolbox-app/

# 或者通过 Snap 安装单个 IDE：
sudo snap install pycharm-community --classic
sudo snap install intellij-idea-community --classic
sudo snap install webstorm --classic
sudo snap install clion --classic
```

**Linux 上常见的开发工具：**

| 软件 | 类型 | 安装 |
|------|------|------|
| **VS Code** | 代码编辑器 | apt/snap |
| **Vim/Neovim** | 终端编辑器 | 预装/ apt |
| **Emacs** | 神的编辑器 | `sudo apt install emacs` |
| **Git** | 版本控制 | 预装 |
| **Docker** | 容器 | `curl -fsSL https://get.docker.com | sh` |
| **Postman** | API 测试 | `sudo snap install postman` |

---

### 小结

Linux 的软件生态已经非常丰富了，日常使用的软件基本都能找到替代品。

**记住以下关键点：**

1. 大多数软件通过 `sudo apt install 软件名` 安装
2. .deb 包用 `sudo dpkg -i 包名.deb` 安装
3. 专有软件（如 Chrome、WPS）去官网下载 .deb 安装
4. Snap 是另一种软件分发格式，用 `sudo snap install 软件名` 安装

---

## 4.11 远程桌面

有时候你需要从一台电脑控制另一台电脑，这就是**远程桌面**。Linux 支持多种远程桌面协议，最常用的三种是：VNC、RDP、SSH 图形转发。

---

### 4.11.1 VNC：Virtual Network Computing

**VNC** 是最通用的远程桌面协议，跨平台（Windows、macOS、Linux、Android、iOS 都能用），免费开源。

**原理：** VNC 在被控制的电脑上运行一个 VNC 服务器，远程用户通过 VNC 客户端连接，看到的是远程电脑的实时画面。

**Ubuntu 安装 VNC 服务器（GNOME 桌面）：**

```bash
# 安装 x11vnc（最稳定的 VNC 服务器之一）
sudo apt install x11vnc

# 设置 VNC 密码（密码文件存放位置）
sudo x11vnc -storepasswd /etc/x11vnc.passwd

# 启动 VNC 服务器（-display :0 表示当前桌面）
sudo x11vnc -display :0 -auth /home/liming/.Xauthority -forever -rfbauth /etc/x11vnc.passwd -shared -bg

# 参数说明：
# -forever    保持运行（不断开连接也继续）
# -rfbauth    指定密码文件
# -shared     允许多个客户端同时连接
# -bg         后台运行
```

**在另一台电脑上用 VNC Viewer 连接：**

1. 下载 VNC Viewer：[https://www.realvnc.com/en/connect/download/viewer/](https://www.realvnc.com/en/connect/download/viewer/)
2. 打开 VNC Viewer，输入 `服务器IP:5900`
3. 输入密码，连接成功！

**或者用 Remmina（Linux 图形 VNC 客户端）：**

```bash
sudo apt install remmina remmina-plugin-vnc
```

---

### 4.11.2 RDP：Remote Desktop Protocol（XRDP）

**RDP** 是微软的远程桌面协议，Windows 原生支持。Linux 上用 **xrdp** 实现 RDP 服务。

**为什么用 RDP 而不是 VNC？**

- RDP 体验更流畅，压缩算法更好
- RDP 支持远程登录（和本地登录是两个会话），VNC 看到的是本地同一画面
- Windows/macOS 原生支持 RDP，不需要额外装客户端

**安装 xrdp：**

```bash
# 安装 xrdp
sudo apt install xrdp

# 启动 xrdp 服务
sudo systemctl start xrdp
sudo systemctl enable xrdp

# 查看状态
sudo systemctl status xrdp

# xrdp 默认使用 3389 端口，确认防火墙开放了
sudo ufw allow 3389/tcp
```

**从 Windows 连接：**

1. 打开 Windows 的"远程桌面连接"（搜索"mstsc"）
2. 输入 Linux 电脑的 IP 地址
3. 输入用户名和密码
4. 点"连接"！

```
远程桌面连接
计算机: 192.168.1.100
用户名: liming
密码: ********
```

**从 macOS 连接：**

macOS 自带 Microsoft Remote Desktop，去 App Store 搜索下载，配置相同。

---

### 4.11.3 SSH 图形转发

**SSH 图形转发**是一种"轻量级"远程桌面方式——不需要在服务器上运行完整的桌面环境，只需要把单个图形程序的窗口显示到本地。

**原理：** SSH 开启 X11 转发后，远程的程序会通过 SSH 隧道把图形界面显示到你的本地电脑，就像在本机运行一样。

**本地电脑设置（Linux）：**

SSH 默认支持 X11 转发，不需要额外配置。确保本地安装了 X11 服务器：

```bash
# Debian/Ubuntu 安装 X11 服务器
sudo apt install x11-apps
```

**远程服务器设置：**

```bash
# 安装 X11 应用（如果需要运行图形程序的话）
sudo apt install x11-apps

# SSH 配置确认（/etc/ssh/sshd_config）
# 确保有这两行：
# X11Forwarding yes
# X11DisplayOffset 10
```

**连接时启用 X11 转发：**

```bash
# -X 开启 X11 转发（小写 X）
ssh -X liming@服务器IP

# 或者用更安全的 -Y（信任模式，渲染更快）
ssh -Y liming@服务器IP
```

连接成功后，你就可以在 SSH 会话里运行图形程序了：

```bash
# 在服务器上运行 Firefox，窗口会显示在你本地电脑上
firefox &

# 或者运行gedit
gedit filename.txt &

# 查看 DISPLAY 变量
echo $DISPLAY
# 应该显示：localhost:10.0 或类似的值
```

**SSH 图形转发 vs VNC/RDP 对比：**

| 方式 | 适用场景 | 带宽占用 | 设置复杂度 |
|------|----------|----------|-----------|
| SSH X11转发 | 运行单个图形程序 | 低 | 低 |
| VNC | 看到远程完整桌面 | 中 | 中 |
| RDP | Windows 用户，流畅体验 | 中 | 低 |

---

### 小结

Linux 的远程桌面方案非常成熟，VNC、RDP、SSH X11转发各有优劣。

**记住以下关键点：**

1. VNC 通用性最强，跨平台，连接的是当前桌面
2. xrdp 适合 Windows 用户，体验更流畅，支持独立会话
3. SSH X11 转发适合临时运行单个图形程序，不需要装桌面
4. 远程连接记得开放防火墙端口！

---

## 本章小结

第四章我们系统地学习了 Linux 桌面环境，从基础概念到各大桌面环境的特点，从系统设置到软件安装再到远程桌面，内容相当丰富。

---

### 知识点回顾

**1. 桌面环境 vs 窗口管理器**

| 类型 | 例子 | 特点 |
|------|------|------|
| 桌面环境 | GNOME、KDE、Xfce、MATE | 一站式全套解决方案 |
| 窗口管理器 | i3、sway、awesome、openbox | 极客专属，高效键盘驱动 |

**2. 四大主流桌面环境**

| 桌面环境 | 特色 | 推荐指数 | 适合人群 |
|----------|------|----------|----------|
| GNOME | 简洁现代，活动概览功能强大 | ⭐⭐⭐⭐⭐ | 追求简洁的用户 |
| KDE Plasma | 功能丰富，高度可定制 | ⭐⭐⭐⭐⭐ | 爱折腾的极客 |
| Xfce | 轻量级，老旧电脑首选 | ⭐⭐⭐⭐ | 低配置机器 |
| MATE | 经典 GNOME 2 风格 | ⭐⭐⭐ | 怀念老界面的用户 |

**3. 系统设置要点**

| 设置项 | 重要操作 |
|--------|----------|
| 网络 | 有线/无线/VPN，命令行用 `nmcli` |
| 声音 | 音量调节，`amixer`/`pactl` |
| 显示 | 分辨率/缩放/多显示器，`xrandr` |
| 电源 | 睡眠/息屏/省电模式 |
| 键盘 | 快捷键自定义，`gsettings` |

**4. 美化三要素**

- 图标主题：Papirus、Numix（用 GNOME Tweaks 管理）
- GTK 主题：Arc、Adwaita
- 桌面壁纸：Unsplash/Wallhaven

**5. 常用软件安装**

- 浏览器：Chrome（.deb）/ Firefox（apt）
- 办公：LibreOffice / WPS Office
- 开发：VS Code（apt）/ JetBrains（Snap）
- 娱乐：VLC、GIMP、Audacity

**6. 远程桌面方案**

| 方案 | 端口 | 适用场景 |
|------|------|----------|
| VNC | 5900 | 跨平台通用 |
| RDP/xrdp | 3389 | Windows 用户 |
| SSH X11转发 | 22 | 单个图形程序 |

---

### 下章预告

到这里，桌面环境就告一段落了。接下来的章节我们将深入到 Linux 的"内核"——学习命令行、文件系统、权限管理、进程管理、网络配置等核心知识。

Linux 的真正力量在于命令行。准备好了吗？让我们继续！

---

