+++
title = "MacBook Pro（M4）快捷键速查表"
date = 2026-09-16T21:00:00+08:00
weight = 2
type = "docs"
description = "macOS 26 + Apple Silicon：系统、Finder、文本、截图、触控板、终端与 Xcode 的快捷键"
isCJKLanguage = true
draft = false

+++

# MacBook Pro（M4）快捷键速查表 ⌨️

> 按 **MacBook Pro 14 英寸（Mac16,1，Apple M4）+ macOS 26.6.2** 的默认键位整理，假设你没改过任何设置。

先说清楚这份表里的字是从哪来的，免得你怀疑我在编：

| 部分 | 来源 |
| --- | --- |
| 系统 / Finder / 文本 / 截图 | macOS 默认键位，菜单栏里逐条能对上 |
| **终端** | 直接从 `Terminal.app` 自己的菜单资源（`MainMenu.nib`）里读出来的原始键位 ✅ |
| **zsh 行编辑** | 用 `bindkey` 在本机交互式 zsh 里查的绑定 ✅ |
| **Xcode** | ⚠️ 只列长期稳定的菜单默认值。Xcode 的菜单是运行时构建的，读不到键位资源，**请以 `Xcode → Settings → Key Bindings` 为准** |

记住一句话：**任何快捷键都能在菜单栏里看到自己的键位**；看不到的（比如触控板手势、行编辑键），本文会点明它藏在哪个设置面板。

---

## 🔤 认键名

这份表不用 Apple 那套几何符号：键名一律写英文简写，多个键一起按时用 `+` 连起来，比如 `Shift + Cmd + 4`。修饰键的顺序统一按 `Ctrl` → `Option` → `Shift` → `Cmd` 排，所以看到 `Cmd + Q`，就是按住 `Cmd` 再按 `Q`。

| 简写 | 键 | 简写 | 键 |
| --- | --- | --- | --- |
| `Cmd` | Command | `Delete` | 退格删除 |
| `Option` | Option / Alt | `Forward Delete` | 前向删除（笔记本上按 `Fn + Delete`） |
| `Ctrl` | Control | `Return` | 回车 |
| `Shift` | Shift | `Enter` | 小键盘回车（笔记本上按 `Fn + Return`） |
| `Caps Lock` | 大写锁定 | `Tab` | 制表符 |
| `Fn` | 功能键（键盘左下角，键帽上带地球图标） | `Backtab` | 反向制表（等于 `Shift + Tab`） |
| `Esc` | 退出键 | `Backtick` | 反引号（`Esc` 下面、数字 `1` 左边那个键） |
| `Left` `Right` `Up` `Down` | 方向键 | `Page Up` `Page Down` | 翻页（笔记本上按 `Fn + Up` / `Fn + Down`） |
| `Home` `End` | 行首 / 行尾（笔记本上按 `Fn + Left` / `Fn + Right`） | `Clear` `Eject` | 外接键盘才有；Apple Silicon 机型没有 `Eject` 键 |

💡 三个结论记一下：修饰键就 `Cmd` / `Option` / `Ctrl` / `Shift` 四个；笔记本上没有独立的 `Home` / `End` / `Page Up` / `Page Down`，都得借 `Fn`；按住 `Fn` 的同时按功能键，得到的是标准 `F1`–`F12`。

### 那三个"不是键位"的键

| 键 | 按一下 | 长按 / 连按 |
| --- | --- | --- |
| **电源键 = Touch ID 键** | 睡眠 / 唤醒（轻按可解锁、Apple Pay、切换用户） | 约 10 秒：**强制关机**（死机时的最后一招） |
| **`Fn` / `Globe` 键** | 看 `系统设置 → 键盘 → "按下 Globe 键"` 里选了啥（切换输入法／调出表情符号，两者都是常见默认值） | 连按两下：**听写**；按住不放（再按功能键）：得到标准 `F1`–`F12` |
| **功能键行 `F1`–`F12`** | 见下表，默认是"系统功能"而不是 F 键 | 想当标准 F 键用：按住 `Fn`，或去 系统设置 → 键盘 → 键盘快捷键 → 功能键 里改 |

```text
F1/F2  降低/提高亮度      F7/F8/F9  上一曲 / 播放暂停 / 下一曲
F3     调度中心            F10/F11/F12  静音 / 音量- / 音量+
F4     搜索（老机型是启动台）
F5/F6  听写 / 专注模式（近几年的 macOS 默认值，随版本略有出入）
```

---

## 🔧 系统全局

| 快捷键 | 功能 |
| --- | --- |
| `Cmd + Space` | Spotlight 搜索（本机最该记住的一个） |
| `Option + Cmd + Space` | 打开 Finder 搜索窗口 |
| `Ctrl + Cmd + Space` | 表情与符号面板（emoji 全靠它） |
| `Ctrl + Space` / `Ctrl + Option + Space` | 切换上一个 / 下一个输入法 |
| `Ctrl + Cmd + Q` | 锁定屏幕（离开工位的第一动作） |
| `Shift + Cmd + Q` | 退出登录（会问你要不要保留窗口） |
| `Option + Shift + Cmd + Q` | 立刻退出登录，不询问 |
| `Option + Cmd + Esc` | 强制退出 App（"程序无响应"对话框） |
| `Ctrl + Cmd + F` | 当前窗口进入 / 退出全屏 |
| `Option + Cmd + D` | 显示 / 隐藏 Dock |
| `Shift + Cmd + /` | 打开当前 App 的"帮助"菜单搜索框（比翻菜单快） |
| `Cmd + ,` | 打开当前 App 的设置 |
| `Cmd + H` / `Option + Cmd + H` | 隐藏当前 App / 隐藏其他所有 App |
| `Cmd + M` / `Option + Cmd + M` | 最小化当前窗口 / 最小化所有窗口 |
| `Cmd + Q` | 退出当前 App（`Cmd + W` 只是关窗口，别搞混） |

### 电源、睡眠与"我彻底卡住了"

这些要用 **电源键（Touch ID 键）** 配合：

| 快捷键 | 功能 |
| --- | --- |
| `Option + Cmd + Power` | 睡眠 |
| `Ctrl + Shift + Power` | 只让显示器睡眠（下载继续跑） |
| `Ctrl + Cmd + Power` | 强制重启（不给 App 保存的机会） |
| `Ctrl + Option + Cmd + Power` | 关机 |
| 长按电源键约 10 秒 | 强制关机（真死机时） |

---

## 🪟 窗口与应用切换

| 快捷键 | 功能 |
| --- | --- |
| `Cmd + Tab` / `Shift + Cmd + Tab` | 在 App 之间前 / 后切换 |
| `Cmd + Backtick` | 同一个 App 的多个窗口之间轮换（Chrome、终端、Finder 全靠它） |
| `Ctrl + Up` | 调度中心（Mission Control）：看全部窗口和桌面 |
| `Ctrl + Down` | 只看当前 App 的所有窗口（App Exposé） |
| `Ctrl + Left` / `Ctrl + Right` | 切换上一个 / 下一个桌面（空间） |
| `Ctrl + Cmd + F` | 全屏（再按一次退出） |
| `Cmd + W` / `Shift + Cmd + W` | 关闭当前标签页或窗口 / 关闭整个窗口 |
| `Cmd + =` / `Cmd + -` / `Cmd + 0` | 放大 / 缩小 / 恢复原大小（大部分 App 通用） |

💡 分屏（Split View）：把鼠标移到窗口左上角绿色按钮上**按住不放**，会弹出"左半屏 / 右半屏 / 移到另一桌面"的菜单；macOS 15 之后也可以在窗口拖到屏幕边缘时自动吸附。

---

## 📂 Finder 与文件

Finder 是 macOS 里快捷键密度最高的 App，也是最值钱的一批：

| 快捷键 | 功能 |
| --- | --- |
| `Cmd + N` / `Shift + Cmd + N` | 新建窗口 / **新建文件夹** |
| `Cmd + T` | 新建标签页（Finder 也有标签页） |
| `Cmd + Delete` / `Shift + Cmd + Delete` | 移到废纸篓 / **清空废纸篓**（会弹一次确认框） |
| `Option + Shift + Cmd + Delete` | 清空废纸篓，**连确认框都省了**——清完就找不回来，手别抖 |
| `Return` | 重命名选中项 🔥 |
| `Space` / `Cmd + Y` | 快速查看（Quick Look）预览，选中一堆文件时最好用；菜单里写的那个是 `Cmd + Y` |
| `Cmd + O` / `Cmd + Down` | 打开选中项 |
| `Cmd + Up` | 回上一层文件夹 |
| `Cmd + [` / `Cmd + ]` | 后退 / 前进 |
| `Shift + Cmd + G` | **前往文件夹**（输入路径直达） |
| `Cmd + 1` / `Cmd + 2` / `Cmd + 3` / `Cmd + 4` | 图标 / 列表 / 分栏 / 画廊视图 |
| `Cmd + J` | 查看显示选项（排序、图标大小） |
| `Cmd + I` / `Option + Cmd + I` | 显示简介 / 显示检查器（右侧面板） |
| `Shift + Cmd + .` | **显示 / 隐藏隐藏文件** 🔥 |
| `Shift + Cmd + D` / `Shift + Cmd + H` | 跳到桌面 / 个人文件夹 |
| `Shift + Cmd + A` / `Shift + Cmd + U` | 跳到"应用程序" / "实用工具" |
| `Shift + Cmd + R` | 跳到 AirDrop |
| `Option + Cmd + L` | 跳到"下载" |
| `Option + Cmd + P` | 显示 / 隐藏路径栏（底部那条路径） |
| `Option + Cmd + S` / `Option + Cmd + T` | 显示 / 隐藏边栏 / 工具栏 |
| `Option + Cmd + V` | **移动**文件到当前位置（先 `Cmd + C` 再按它，等于"剪切粘贴"） |
| `Cmd + Z` / `Shift + Cmd + Z` | 撤销文件操作 / 重做（删错、改错名的后悔药） |
| `Cmd + F` | 在当前位置搜索 |

💡 三个"按住 `Option` 才会出现"的菜单项，Mac 上到处适用：在 Finder 或文件对话框里按住 `Option` 打开"编辑"菜单，"拷贝"会变成**"拷贝…为路径名称"**（拿文件路径最快的方式）；右键菜单里按住 `Option` 也会多出几项。

💡 拖动文件时按住 `Option` 是**复制**，按住 `Cmd` 是**移动**（同一磁盘内默认移动，跨磁盘默认复制）。

⚠️ "移到废纸篓 / 清空废纸篓"这一串是 **Finder 的菜单快捷键**，得 Finder 在前台才生效——在别的 App 里按 `Shift + Cmd + Delete` 是没反应的。拿不准哪个键此刻真的管用，就点开 Finder 的 **文件** 菜单看一眼：菜单项右边印着的才是真正生效的键位（菜单栏永远比速查表可信）。

---

## ✏️ 文本编辑与输入

### 光标与选择（所有输入框、所有 App 通用）

| 快捷键 | 功能 |
| --- | --- |
| `Option + Left` / `Option + Right` | 按**词**左右移动 |
| `Cmd + Left` / `Cmd + Right` | 到**行首 / 行尾** |
| `Cmd + Up` / `Cmd + Down` | 到**文档开头 / 结尾** |
| 上面的键 + `Shift` | 一边移一边选（`Option + Shift + Right` 按词选） |
| `Option + Delete` | 删除前一个词 |
| `Cmd + Delete` | 删除到行首 |
| `Ctrl + K` | 删除到行尾（Emacs 血统） |
| `Ctrl + Y` | 粘回刚删掉的内容 |
| `Cmd + A` / `Cmd + C` / `Cmd + V` / `Cmd + X` | 全选 / 拷贝 / 粘贴 / 剪切 |
| `Option + Shift + Cmd + V` | 粘贴并匹配样式（支持该命令的 App 里很好用） |
| `Cmd + Z` / `Shift + Cmd + Z` | 撤销 / 重做 |
| `Cmd + F` / `Cmd + G` / `Shift + Cmd + G` | 查找 / 下一个 / 上一个 |

### Emacs 那一套（macOS 文本系统原生支持）

不用装任何东西，macOS 的输入框天生认这些 `Ctrl` 组合——手不离主键区就能移动光标：

| 快捷键 | 功能 | 快捷键 | 功能 |
| --- | --- | --- | --- |
| `Ctrl + A` / `Ctrl + E` | 行首 / 行尾 | `Ctrl + B` / `Ctrl + F` | 左移 / 右移一个字符 |
| `Ctrl + N` / `Ctrl + P` | 下一行 / 上一行 | `Ctrl + D` | 删除光标右边的字符 |
| `Ctrl + K` | 删到行尾 | `Ctrl + T` | 交换光标两侧的两个字符 |

### 打不出想要的那个字符

| 我想 | 怎么做 |
| --- | --- |
| 打 `é ü ñ ç à ê` | 长按字母键，等弹出候选框再按数字；老系统里长按是重复输入，需在"键盘"设置里开启 |
| 敲出重音符号 | 用 `Option` 死键：`Option + E` 再按 `e` → `é`；`Option + U` 再按 `u` → `ü`；`Option + N` 再按 `n` → `ñ`；`Option + C` → `ç` |
| emoji / 特殊符号 | `Ctrl + Cmd + Space` 打开表情与符号面板 |
| 中文输入时切换中英 | 一般按 `⇪`（Caps Lock）或 `Shift`；具体在 输入法设置 里可改 |
| 语音输入 | 连按两下 `Fn` / `Globe` 键，再说（说完再按一下结束） |

---

## 🖼️ 截图与录屏

macOS 的截图键是一整套，值得单独背：

| 快捷键 | 功能 |
| --- | --- |
| `Shift + Cmd + 3` | **全屏截图**，保存到桌面 |
| `Shift + Cmd + 4` | **选区截图**：拖拽选范围；按一下 `Space` 变成"窗口截图"（点哪个窗口截哪个） |
| `Shift + Cmd + 5` | **截图与录屏工具**：录屏、延时截图、改保存位置都在这里 |
| 上面任意一个 + `Ctrl` | 不存文件，直接进剪贴板（例：`Ctrl + Shift + Cmd + 3`） |
| `Shift + Cmd + 6` | 截取触控栏（Touch Bar）——**M4 机型没有触控栏，这条用不上** |
| 截图时按住 `Option` 拖动 | 以中心点为中心缩放选区；按住 `Shift` 可锁定宽或高 |

💡 录屏：`Shift + Cmd + 5` → 选"录制整个屏幕"或"录制所选部分" → 点"录制"；停止按菜单栏上的停止按钮。想连声音一起录，在同一个面板的"选项"里选麦克风。

💡 截图默认落在桌面。要换成剪贴板或别的文件夹：`Shift + Cmd + 5` → "选项"里改。

---

## 🧭 Safari 与常见 App

Safari：

| 快捷键 | 功能 |
| --- | --- |
| `Cmd + T` / `Shift + Cmd + T` | 新建标签页 / **重开刚关掉的标签页** |
| `Cmd + W` | 关闭当前标签页 |
| `Cmd + L` | 光标跳到地址栏（相当于浏览器里的 `Cmd + Up`） |
| `Cmd + R` | 重新载入 |
| `Cmd + [` / `Cmd + ]` | 后退 / 前进 |
| `Ctrl + Tab` / `Ctrl + Shift + Tab` | 下一个 / 上一个标签页 |
| `Cmd + 1` … `Cmd + 9` | 直接跳到第 1–9 个标签页（`Cmd + 9` 是最后一个） |
| `Shift + Cmd + N` | 新建隐私窗口 |
| `Cmd + D` / `Shift + Cmd + D` | 添加书签 / 添加到阅读列表 |
| `Cmd + F` / `Cmd + G` / `Shift + Cmd + G` | 页面内查找 / 下一个 / 上一个 |
| `Cmd + =` / `Cmd + -` / `Cmd + 0` | 放大 / 缩小 / 实际大小 |

几乎任何 App 都通用的那一批（记一次，受用终身）：

| 快捷键 | 功能 |
| --- | --- |
| `Cmd + N` / `Cmd + O` / `Cmd + S` / `Cmd + P` | 新建 / 打开 / 保存 / 打印 |
| `Cmd + F` | 查找 |
| `Cmd + Z` / `Shift + Cmd + Z` | 撤销 / 重做 |
| `Cmd + ,` | 该 App 的设置 |
| `Cmd + H` / `Option + Cmd + H` | 隐藏自己 / 隐藏别人 |
| `Cmd + Q` | 退出 |

---

## 🖱️ 触控板手势（M4 机型）

MacBook 的效率一半在触控板上。默认设置（系统设置 → 触控板）下：

| 手势 | 效果 |
| --- | --- |
| 单指轻点 | 单击（默认开启"轻点来点按"后可用，不必真按下去） |
| 双指轻点 | 右键 / 辅助点按 |
| 双指上下 / 左右滑 | 滚动 / 横向滚动；在 Safari、Finder 里左右滑是**前进后退** |
| 双指从右边缘向左滑 | 打开通知中心 |
| 双指捏合 / 张开 | 缩放（图片、PDF、地图、网页） |
| 双指旋转 | 旋转图片或 PDF 页面 |
| 三指 / 四指上滑 | 调度中心（Mission Control） |
| 三指 / 四指下滑 | 当前 App 的所有窗口（App Exposé） |
| 三指 / 四指左右滑 | 切换桌面（空间） |
| 拇指 + 三指张开 | **显示桌面**（散开所有窗口，再捏回去复原） |
| 拇指 + 三指捏合 | 打开"启动台"（Launchpad） |
| 用力点按（Force Touch） | 查词、预览链接、快速操作；M4 机型的触控板支持力度感应 |

⚠️ **三指拖移**（拖动窗口、选文本不用按下去）默认是关的，要去 系统设置 → 辅助功能 → 指针控制 → 触控板选项 → 打开"使用三指拖移"。开了它以后，三指滑动的手势会让位给拖移。

💡 触控板"按不动"？系统设置 → 触控板 → "点按"里可以调力度（轻/中/重），Apple Silicon 机型是模拟的触感反馈，不是真的按键弹跳。

---

## 🚀 启动、恢复与排障（Apple Silicon 专用）

⚠️ 这一节和 Intel Mac 完全不是一套，网上很多老教程是错的。

| 我想 | 怎么做 |
| --- | --- |
| 进入**启动选项**（选启动磁盘） | 关机 → **按住电源键不放**，直到看到"正在载入启动选项" |
| 进入**恢复模式** | 启动选项里选"选项" → 继续 |
| 进入**安全模式** | 关机 → 按住电源键进启动选项 → 按住 `Shift` 选择要启动的磁盘 |
| 抹掉重装系统 | 恢复模式 → 磁盘工具（先抹盘）→ 退出 → 重新安装 macOS |
| DFU 恢复 | 需要另一台 Mac + Apple Configurator，属于"最后手段" |
| 重置 NVRAM / SMC | ❌ **Apple Silicon 不需要**，也没有对应的按键组合，系统自己管 |

📘 上面每一步的官方图文步骤在 [Apple 支持](https://support.apple.com/zh-cn/guide/mac-help/welcome/mac) 里，涉及抹盘的操作请对着官方页面做。

---

## 💻 终端（Terminal.app）

先说明：下表的键位是我从 `Terminal.app` 自己的菜单资源里读出来的**当前真实绑定**，不是抄的。菜单名放在方括号里，方便你在菜单栏对照。

{{< tabpane text=true persist=disabled >}}

{{% tab header="窗口与标签" %}}

| 快捷键 | 功能 |
| --- | --- |
| `Cmd + N` | 新建窗口 |
| `Ctrl + Cmd + N` | 用**同一条命令**再开一个窗口 |
| `Shift + Cmd + N` | 新建命令窗口（New Command）：先填命令再开窗 |
| `Cmd + T` | 新建标签页 |
| `Ctrl + Cmd + T` | 用**同一条命令**再开一个标签页 |
| `Cmd + D` / `Shift + Cmd + D` | 分屏（左右）/ 关闭分屏 |
| `Shift + Cmd + T` | 显示 / 隐藏标签栏 |
| `Cmd + Backtick` | 在终端窗口之间轮换 |
| `Cmd + W` / `Cmd + M` / `Cmd + Q` | 关闭窗口 / 最小化 / 退出终端 |
| `Ctrl + Cmd + F` | 全屏 |
| `Cmd + ,` | 终端设置（字体、配色、描述文件） |

{{% /tab %}}

{{% tab header="输出与查找" %}}

| 快捷键 | 功能 |
| --- | --- |
| `Cmd + K` | Clear to Start：把光标之前的内容全部清掉（Terminal 里最顺手的清屏键） |
| `Ctrl + Cmd + L` | Clear Screen：只管当前这一屏 |
| `Option + Cmd + K` | Clear Scrollback：连滚上去的历史一起清掉——想彻底干净按它 |
| `Cmd + F` / `Cmd + G` / `Shift + Cmd + G` | 查找 / 下一个 / 上一个 |
| `Cmd + E` | 把当前选中的内容放进查找框 |
| `Cmd + J` | 跳到所选内容 |
| `Cmd + =` / `Cmd + -` / `Cmd + 0` | 放大 / 缩小 / 恢复默认字号 |
| `Option + Cmd + C` | 复制为纯文本（**去掉颜色转义**，粘到别处不会一团乱码） |
| `Ctrl + Cmd + C` | 复制（不带背景色） |
| `Ctrl + Cmd + V` | 转义粘贴（粘贴转义过的文本） |
| `Cmd + S` | 把终端输出导出为文本文件 🔥 留下编译日志很方便 |
| `Cmd + P` | 打印 |
| `Shift + Cmd + Enter` | 发送回车但**不做标记**（在 REPL 里更自然） |
| `Cmd + Enter` | 标记该行并发送回车 |

{{% /tab %}}

{{% tab header="跳转与救急" %}}

| 快捷键 | 功能 |
| --- | --- |
| `Cmd + Up` / `Cmd + Down` | 跳到上一个 / 下一个标记 |
| `Option + Cmd + Up` / `Option + Cmd + Down` | 跳到上一个 / 下一个书签 |
| `Cmd + Home` / `Cmd + End` | 滚到最顶 / 最底（笔记本上 `Home`/`End` 就是 `Fn + Left` / `Fn + Right`，所以实际按 `Cmd + Fn + Left` / `Cmd + Fn + Right`） |
| `Cmd + Page Up` / `Cmd + Page Down` | 向上 / 向下翻一页（同理：`Cmd + Fn + Up` / `Cmd + Fn + Down`） |
| `Ctrl + Option + Cmd + L` | Fill Screen：让内容铺满窗口（把滚动条也藏掉） |
| `Option + Cmd + R` | 重置终端（输出乱码、光标错位时的急救） |
| `Ctrl + Option + Cmd + R` | 硬重置 |
| `Option + Cmd + O` | **使用 Option 键作为 Meta 键**（想用 `Option + B`/`Option + F` 按词跳就得开它） |
| `Cmd + I` / `Option + Cmd + I` | 编辑标题 / 编辑背景色 |

祝你好运，`Option + Cmd + R` 救过很多人。

{{% /tab %}}

{{< /tabpane >}}

💡 终端里最值钱的三个操作，跟快捷键无关但更常用：`Cmd + E` 选中即搜索、`Cmd + K` 一键清屏、`Cmd + S` 把整段输出存文件。

---

## 🐚 zsh 行编辑（任何终端里都能用）

这些是 **shell 层**的绑定，与 Terminal.app 还是 iTerm2 无关。本机 zsh 实测确认（`bindkey`）：

| 快捷键 | 功能 | 备注 |
| --- | --- | --- |
| `Ctrl + A` / `Ctrl + E` | 行首 / 行尾 | 实测绑定 |
| `Ctrl + B` / `Ctrl + F` | 左 / 右移一个字符 | 实测绑定 |
| `Option + B` / `Option + F` | 按词左 / 右移 | 需要先开 `Option + Cmd + O`（Option as Meta） |
| `Ctrl + W` | 删掉前一个词 | 实测绑定（`backward-kill-word`） |
| `Ctrl + U` | 删掉整行 | 实测绑定（`kill-whole-line`） |
| `Ctrl + K` | 删到行尾 | 实测绑定 |
| `Ctrl + Y` | 粘回刚删掉的内容 | |
| `Ctrl + R` | **反向搜索历史**（再按 `Ctrl + R` 继续往前翻） | 实测绑定，最常用 🔥 |
| `Ctrl + P` / `Ctrl + N` | 上一条 / 下一条历史命令 | |
| `Ctrl + L` | 清屏 | 实测绑定 |
| `Ctrl + C` | 中断当前命令 | |
| `Ctrl + D` | 结束输入 / 退出 shell（空行时按） | |
| `Ctrl + Z` | 挂起到后台，用 `fg` 捞回来 | |
| `Ctrl + T` | 交换光标两侧两个字符 | 打错字时的救命键 |
| `Esc` `.` | 插入上一条命令的**最后一个参数** | 类似 `!$`，但不用敲回车 |

历史展开（交互式 shell 里实测可用）：

| 写法 | 展开成 |
| --- | --- |
| `!!` | 上一条完整命令 |
| `!$` | 上一条命令的最后一个参数 |
| `!^` | 上一条命令的第一个参数 |
| `!pip` | 最近一条以 `pip` 开头的命令 |

💡 想用 `$EDITOR` 编辑当前这条长命令，zsh 里默认没绑键，需要自己加两行：

```zsh
autoload -Uz edit-command-line
zle -N edit-command-line
bindkey '^X^E' edit-command-line     # 之后按 Ctrl + X 再 Ctrl + E 就会打开编辑器
```

---

## 🛠️ Xcode

> 🚧 **先说清楚**：Terminal 的键位能从 App 资源里读出来，Xcode 不行——它的菜单是**运行时用代码搭出来的**。本机实测：`Xcode.app/Contents/Resources/en.lproj/MainMenu.nib` 只有 920 字节、10 个对象，里面只有 App 委托和一个字体管理器，连一个菜单项都没有，纯粹是个空壳。
> 所以下面列的是 Xcode 长期稳定的默认值，**请以菜单栏和 `Xcode → Settings → Key Bindings` 为准**：那里的搜索框既能按动作名搜、也能直接按快捷键搜，冲突会标黄，还能导出成 `.idekeybindings` 文件。
> （本机 `~/Library/Developer/Xcode/UserData/KeyBindings/Default.idekeybindings` 是空的 `{}`，说明你用的是内置默认键位集，没改过。）

{{< tabpane text=true persist=disabled >}}

{{% tab header="构建 / 运行 / 调试" %}}

| 快捷键 | 功能 |
| --- | --- |
| `Cmd + B` | 构建（Build） |
| `Cmd + R` | 运行（Run） |
| `Cmd + U` | 测试（Test） |
| `Cmd + .` | 停止当前操作 |
| `Shift + Cmd + K` | **清理构建目录**（Clean Build Folder）——编译结果诡异时的第一招 |
| `Cmd + K` | 清空控制台输出（Clear Console） |
| `Cmd + I` | Profile：用 Instruments 跑性能分析 |
| `Shift + Cmd + B` | 静态分析（Analyze），查内存与逻辑隐患 |
| `Cmd + \` | 在光标所在行添加 / 移除断点 |
| `F6` / `F7` / `F8` | 单步跳过 / 单步进入 / 单步跳出 |

⚠️ `F6`–`F8` 这些调试键要在调试会话里才有用，而且 MacBook 的功能键行默认是系统功能——所以实际按的是 **`Fn + F6`**，或者去 系统设置 → 键盘 → 键盘快捷键 → 功能键 里把功能键改回标准 `F1`–`F12`。

{{% /tab %}}

{{% tab header="导航与搜索" %}}

| 快捷键 | 功能 |
| --- | --- |
| `Shift + Cmd + O` | **快速打开**：输文件名、类型名、方法名都能直达 🔥 |
| `Shift + Cmd + J` | 在项目导航器里定位当前文件 |
| `Ctrl + Cmd + Left` / `Ctrl + Cmd + Right` | 后退 / 前进（在跳转历史里穿梭） |
| `Cmd + L` | 跳到指定行 |
| `Cmd + 0` | 显示 / 隐藏左侧导航器 |
| `Cmd + 1` … `Cmd + 9` | 切换各类导航器（项目、源代码管理、符号、查找、问题、测试、调试、断点、报告） |
| `Option + Cmd + 0` | 显示 / 隐藏右侧检查器 |
| `Shift + Cmd + Y` | 显示 / 隐藏底部调试区（编译输出、日志都在这儿） |
| `Shift + Cmd + 0` | 打开开发者文档 |
| `Cmd + F` / `Option + Cmd + F` | 当前文件内查找 / 查找并替换 |
| `Shift + Cmd + F` / `Option + Shift + Cmd + F` | 整个工作区查找 / 查找并替换 🔥 |
| `Cmd + G` / `Shift + Cmd + G` | 下一个 / 上一个查找结果 |

💡 日常最高频的组合是 `Shift + Cmd + O` 跳文件 + `Shift + Cmd + F` 全项目搜索 + `Shift + Cmd + Y` 看日志，三个键就能覆盖大半导航需求。

{{% /tab %}}

{{% tab header="写代码" %}}

| 快捷键 | 功能 |
| --- | --- |
| `Cmd + /` | 注释 / 取消注释选中行 🔥 |
| `Cmd + [` / `Cmd + ]` | 减少 / 增加缩进 |
| `Option + Cmd + [` / `Option + Cmd + ]` | 把当前行上移 / 下移 |
| `Ctrl + I` | 重新缩进（Re-indent） |
| `Cmd + A` / `Cmd + C` / `Cmd + V` / `Cmd + X` | 全选 / 拷贝 / 粘贴 / 剪切 |
| `Cmd + Z` / `Shift + Cmd + Z` | 撤销 / 重做 |
| `Cmd + S` | 保存（Xcode 也会自动保存，但手按一下更安心） |

💡 选中多行再按 `Cmd + /` 是批量注释；`Option + Cmd + [` 挪代码块比剪切粘贴体面得多。

{{% /tab %}}

{{% tab header="窗口与面板" %}}

| 快捷键 | 功能 |
| --- | --- |
| `Cmd + ,` | Xcode 设置（Key Bindings 就在这里面） |
| `Cmd + W` | 关闭当前编辑器或标签页 |
| `Ctrl + Cmd + W` | 关闭整个项目窗口（Close Project） |
| `Ctrl + Cmd + F` | 全屏 |
| `Cmd + Backtick` | 在多个 Xcode 窗口之间轮换 |
| `Cmd + 0` / `Option + Cmd + 0` / `Shift + Cmd + Y` | 三个面板开关：导航器 / 检查器 / 调试区 |

💭 编辑区太窄时，`Cmd + 0` + `Option + Cmd + 0` 一起按下去，就得到一个"纯代码"窗口。

{{% /tab %}}

{{< /tabpane >}}

### 改键与查键（两分钟就能上手）

1. `Xcode → Settings…`（`Cmd + ,`）→ 选 **Key Bindings** 标签页。
2. 顶部搜索框：**既可以搜动作名**（比如输入 `comment`），**也可以直接按一下快捷键**，它会列出所有占用这个组合的命令。
3. 冲突的命令会被标黄，双击右侧的键位列就能重新录制。
4. 左下角可以切换预设（Xcode Default、Sublime Text、BBEdit、Vim…）；右侧齿轮里能 **Export** 成 `.idekeybindings` 文件，团队可以共享同一份。

💡 在任何 App 的菜单栏里**按住 `Option` 打开菜单**，经常会看到菜单项换了个名字（比如"关闭窗口"变成"关闭所有窗口"）——这是 macOS 的隐藏菜单机制，值得时不时按一下看看。

💡 Xcode 里能按的键，命令行基本也有对应物：`xcodebuild -scheme 名字 build`、`xcodebuild test`、`xcrun simctl`。CI 上跑的就是它们。

---

## ⚙️ 自定义、冲突与排查

| 我想 | 去哪儿 |
| --- | --- |
| 改系统快捷键 | 系统设置 → 键盘 → 键盘快捷键（左边分类，右边逐条改） |
| 改修饰键（比如 Caps Lock 换 Esc、换 Control） | 系统设置 → 键盘 → 键盘快捷键 → **修饰键…** |
| 给某个 App 单独加键 | 系统设置 → 键盘 → 键盘快捷键 → **App 快捷键** → `+` → 选 App、**原样输入菜单项名字**、按下组合键 |
| 让 Tab 键能在按钮/文本框之间跳 | 系统设置 → 键盘 → 打开"键盘导航" |
| 看系统符号键位的底层配置 | 终端里跑 `defaults read com.apple.symbolichotkeys AppleSymbolicHotKeys` |
| 某个组合被"抢"了 | 一般是**最前面那个 App + 菜单顺序靠前的项**赢；先看当前 App 的菜单栏，再查上面那张表的 App 快捷键里有没有重复 |
| 把系统快捷键恢复默认 | ⚠️ 删掉 `~/Library/Preferences/com.apple.symbolichotkeys.plist` 后重启（会丢掉你所有的自定义键位，慎用） |
| 想更狠地改键 | Karabiner-Elements（改键盘底层映射）、Raycast（`Option + Space` 之类启动器）、Hammerspoon（用 Lua 写自动化） |

⚠️ 一条经验：**别急着装改键工具**。系统自带的"修饰键 + App 快捷键"两层已经能解决 90% 的需求，剩下 10% 再用 Karabiner 这类工具，否则换一台机器你就不会打字了。

---

## 🔍 按场景反查

忘了具体键位时从这一栏找：

| 我想…… | 按 |
| --- | --- |
| 搜索任何东西 | `Cmd + Space` |
| 打 emoji | `Ctrl + Cmd + Space` |
| 锁屏走人 | `Ctrl + Cmd + Q` |
| 截个图 | `Shift + Cmd + 4`（选区）/ `Shift + Cmd + 3`（全屏） |
| 录屏 | `Shift + Cmd + 5` |
| 强制退出卡死的 App | `Option + Cmd + Esc` |
| 关掉卡死的整个系统 | 长按电源键约 10 秒 |
| 看隐藏文件 | `Shift + Cmd + .` |
| 拿文件路径 | 选中文件 → 按住 `Option` 打开"编辑"菜单 → "拷贝…为路径名称" |
| 新建文件夹 | `Shift + Cmd + N`（Finder 里） |
| 删文件 / 清空废纸篓 | `Cmd + Delete` / `Shift + Cmd + Delete` |
| 重命名 | 选中 → `Return` |
| 预览文件 | 选中 → `Space` |
| 后悔刚才的操作 | `Cmd + Z` |
| 在当前 App 里换窗口 | `Cmd + Backtick` |
| 在 App 之间换 | `Cmd + Tab` |
| 看所有窗口 | `Ctrl + Up` |
| 换桌面 | `Ctrl + Left` / `Ctrl + Right` |
| 关浏览器标签 | `Cmd + W` |
| 找回刚关掉的标签 | `Shift + Cmd + T` |
| 跳地址栏 | `Cmd + L` |
| 终端里搜历史命令 | `Ctrl + R` |
| 终端里清屏 | `Cmd + K` |
| 终端卡住/乱码 | `Option + Cmd + R` |
| 把终端输出存成文件 | `Cmd + S` |
| Xcode 跳文件 | `Shift + Cmd + O` |
| Xcode 全项目搜索 | `Shift + Cmd + F` |
| Xcode 注释 | `Cmd + /` |
| Xcode 跑起来 | `Cmd + R` |
| Xcode 看日志 | `Shift + Cmd + Y` |

---

> 最后一句：这份表不用背。**记住 `Cmd + Space`（搜索）、`Ctrl + Cmd + Q`（锁屏）、`Cmd + /`（注释）、`Ctrl + R`（搜历史）、`Shift + Cmd + O`（Xcode 跳文件）这五个**，其余的在需要的时候回来查——查三次自然就记住了。
