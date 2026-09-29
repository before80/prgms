+++
title = "RustRover macOS 快捷键速查表"
date = 2026-09-29T11:05:00+08:00
weight = 1
type = "docs"
description = "RustRover 2026.2（macOS 键位表）常用快捷键：编辑、搜索、导航、重构、运行调试、Cargo、Git 与工具窗口"
isCJKLanguage = true
draft = false

+++

# RustRover macOS 快捷键速查表 ⌨️

> 按 **RustRover 2026.2.3（build RR-262.10968.75）+ macOS** 的默认 **macOS 键位表** 整理，假设你没改过键位、也没导入过别人的键位表。

先说清楚这些键位是从哪来的，免得你怀疑我在编：

| 部分 | 来源 |
| --- | --- |
| **本文全部键位** | 直接从本机 `/Applications/RustRover.app` 里读出的键位表（`keymaps/Mac OS X 10.5+.xml`，也就是 `Settings → Keymap` 里显示为 **macOS** 的那一套）✅ |
| **动作中文名** | 取自 RustRover 官方简体中文语言包（你的 IDE 语言就是简体中文）✅ |
| **Rust / Cargo 相关动作** | 扫描了 IDE 里全部插件描述符：**2026.2 里它们没有默认键位** ✅（见第 9 节） |
| **双击 Shift / 双击 Ctrl** | 属于「连击手势」，不在键位表里，来自 JetBrains 官方帮助文档 |

一句话原则：**任何动作的键位都能在菜单栏或 `Shift + Cmd + A` 的列表里看到**；看不到键位的（手势、鼠标操作），本文会点明。

---

## 🔤 认键名

本文不用 Apple 那套几何符号：键名一律写英文简写，多键同按用 `+` 连接，修饰键顺序统一按 `Ctrl` → `Option` → `Shift` → `Cmd` 排。所以看到 `Shift + Cmd + Z`，就是按住 `Shift` 和 `Cmd` 再按 `Z`。

| 简写 | 键 | 简写 | 键 |
| --- | --- | --- | --- |
| `Cmd` | Command（⌘） | `Delete` | 退格删除（⌫） |
| `Option` | Option / Alt（⌥） | `Forward Delete` | 前向删除（⌦，笔记本上按 `Fn + Delete`） |
| `Ctrl` | Control（⌃） | `Return` | 回车 |
| `Shift` | Shift（⇧） | `Tab` | 制表符 |
| `Fn` | 功能键（键盘左下角） | `Esc` | 退出键 |
| `Insert` | 插入键（笔记本上没有这个键，一般用 `Fn + Enter` 代替） | `Home` / `End` | 行首 / 行尾（笔记本上按 `Fn + Left` / `Fn + Right`） |

💡 两个 Mac 上必踩的前提：

- **`F1`–`F12` 默认是系统功能键**（亮度、音量…）。不带修饰键的 F 键（`F2`、`F7`、`F12`…）默认会被系统截走，得按住 `Fn`；带 `Cmd` / `Option` / `Shift` 的一般能直接送达（如 `Shift + F6`、`Cmd + F8`），个别系统版本仍会拦截，按了没反应就补个 `Fn`。想一劳永逸就去 `系统设置 → 键盘 → 键盘快捷键 → 功能键` 勾上「将 F1、F2 等键用作标准功能键」。本文里所有 `F1`–`F12` 都按已勾选的情况写。
- **`Cmd + Space` 是 Spotlight**，所以 JetBrains 的补全用的是 `Ctrl + Space`；如果你把输入法切换也设成了 `Ctrl + Space`，补全会失灵，去 `系统设置 → 键盘 → 键盘快捷键 → 输入法` 改掉。

---

## 🎯 最该先记住的 12 个

| 快捷键 | 干什么 |
| --- | --- |
| `Shift + Shift`（双击） | 随处搜索：文件、符号、动作、设置…万能入口 |
| `Shift + Cmd + A` | 查找操作：想不起键位就搜动作名 |
| `Cmd + B` | 前往声明或用法（也能 `Cmd + 单击`） |
| `Cmd + E` | 最近的文件 |
| `Shift + Cmd + F` | 在整个项目里搜文本 |
| `Option + F7` | 查找用法 |
| `Shift + F6` | 重命名（安全改名，会连带改引用） |
| `Option + Cmd + L` | 重新格式化代码 |
| `Ctrl + R` / `Ctrl + D` | 运行 / 调试 |
| `Shift + Cmd + K` | 推送到远端（Git） |
| `Cmd + K` | 提交（Git） |
| `Option + F12` | 打开终端 |

---

## 1️⃣ 全局：搜索、设置与布局

| 快捷键 | 动作 | 说明 |
| --- | --- | --- |
| `Shift + Shift` | 随处搜索 | 连按两下 Shift；文件 / 符号 / 动作 / 设置一起搜 |
| `Ctrl + Ctrl` | 运行任何内容 | 连按两下 Ctrl；可跑 Cargo 命令、启动配置、命令行工具 |
| `Shift + Cmd + A` | 查找操作… | 搜命令，可在列表里按 `Option + Return` 直接加键位 |
| `Cmd + E` | 最近的文件 | 再按 `Cmd + E` 可只显示「已更改的文件」 |
| `Shift + Cmd + E` | 最近的位置 | 最近跳转过的位置 |
| `Shift + Cmd + F12` | 隐藏所有工具窗口 | 全屏写代码 |
| `Shift + F12` | 恢复当前布局 | 把工具窗口摆回来 |
| `Shift + Esc` | 隐藏当前工具窗口 | 焦点回到编辑器 |
| `Shift + Cmd + '` | 最大化 / 还原工具窗口 | |
| `F12` | 跳转到上一个工具窗口 | |
| `Cmd + ,` | 设置 | |
| `Cmd + ;` | 项目结构… | |
| `Ctrl + Backtick` | 快速切换方案… | 主题、键位表、代码样式、视图模式 |
| `Ctrl + Cmd + F` | 切换全屏 | |
| `Ctrl + Option + =` / `Ctrl + Option + -` | 放大 / 缩小 IDE | `Ctrl + Option + 0` 重置缩放 |
| `Cmd + S` | 全部保存 | IDE 本来就自动保存，这个键实际是「Save All」 |
| `Option + Cmd + Y` | 从磁盘全部重新加载 | 外部改了文件、IDE 不同步时用 |
| `Cmd + Q` | 退出 | |

## 2️⃣ 编辑：文本与代码

| 快捷键 | 动作 |
| --- | --- |
| `Cmd + C` / `Cmd + X` / `Cmd + V` | 复制 / 剪切 / 粘贴 |
| `Shift + Cmd + V` | 从历史记录粘贴… |
| `Option + Shift + Cmd + V` | 粘贴为纯文本 |
| `Cmd + Z` / `Shift + Cmd + Z` | 撤消 / 重做 |
| `Cmd + A` | 全选 |
| `Cmd + D` | 重复行或选区 |
| `Cmd + Delete` | 删除行 |
| `Option + Delete` / `Option + Forward Delete` | 删除到词首 / 词尾 |
| `Cmd + /` | 行注释（再按一次取消） |
| `Option + Cmd + /` | 块注释（`Shift + Cmd + /` 亦可） |
| `Shift + Cmd + U` | 切换大小写 |
| `Ctrl + Shift + J` | 连接行 |
| `Cmd + Return` | 拆分行 |
| `Shift + Return` | 开始新行 |
| `Option + Cmd + Return` | 在当前行之前开始新行 |
| `Shift + Cmd + Return` | 补全当前语句（自动补分号、括号等） |
| `Option + Cmd + L` | 重新设置代码格式 |
| `Option + Shift + Cmd + L` | 重新设置文件格式…（弹对话框选范围） |
| `Ctrl + Option + O` | 优化 import |
| `Ctrl + Option + I` | 自动缩进行 |
| `Tab` / `Shift + Tab` | 缩进 / 取消缩进 |
| `Shift + Cmd + Up` / `Shift + Cmd + Down` | 向上 / 向下移动语句 |
| `Option + Shift + Up` / `Option + Shift + Down` | 上移 / 下移行 |
| `Option + Shift + Cmd + Left` / `Right` | 向左 / 向右移动元素 |
| `Option + Up` / `Option + Down` | 扩展 / 收缩选区 |
| `Option + Shift + G` | 在所选行的行尾添加光标（多行同时编辑） |
| `Shift + Cmd + 8` | 列选择模式 |
| `Option + Cmd + [` / `Option + Cmd + ]` | 移到代码块开始 / 结束 |
| `Cmd + -` / `Cmd + +` | 折叠 / 展开当前区域 |
| `Shift + Cmd + -` / `Shift + Cmd + +` | 全部折叠 / 全部展开 |
| `Cmd + .` / `Shift + Cmd + .` | 折叠选区/移除区域 / 折叠代码块 |
| `Option + Cmd + .` | 自定义折叠… |
| `Shift + Cmd + Delete` | 上一个编辑位置（跳回刚改过的地方） |
| `Option + /` | 循环扩展词（按已出现过的词补全） |
| `Option + Shift + Cmd + Delete` | 解包/移除…（去掉外层包裹） |
| `Ctrl + M` | 移到匹配的括号 |
| `Ctrl + Shift + P` | 类型信息 |
| `Shift + Cmd + C` / `Option + Shift + Cmd + C` | 复制路径 / 复制引用 |
| `Cmd + J` | 插入实时模板… |
| `Option + Cmd + J` | 使用实时模板包围… |
| `Option + Cmd + T` | 环绕方式…（if / match / loop 等） |

## 3️⃣ 光标移动与选区

| 快捷键 | 动作 |
| --- | --- |
| `Cmd + Left` / `Cmd + Right` | 移到行首 / 行尾（`Ctrl + A` / `Ctrl + E` 也行） |
| `Option + Left` / `Option + Right` | 按词左移 / 右移 |
| `Cmd + Up` | 跳转到导航栏 |
| `Cmd + Down` | 跳转到源（`F4` 亦可） |
| `Cmd + Home` / `Cmd + End` | 移到文本开始 / 结束 |
| `Cmd + Page Up` / `Cmd + Page Down` | 移到页面顶部 / 底部 |
| `Option + Cmd + Up` / `Option + Cmd + Down` | 上一个 / 下一个匹配项 |
| `Ctrl + Shift + Up` / `Ctrl + Shift + Down` | 上一个 / 下一个方法 |
| `Ctrl + Option + Up` / `Ctrl + Option + Down` | 上一个 / 下一个高亮用法 |
| `F2` / `Shift + F2` | 下一个 / 上一个高亮错误 |
| `Cmd + [` / `Cmd + ]` | 后退 / 前进（`Option + Cmd + Left` / `Right` 亦可） |
| `Ctrl + Shift + Left` / `Ctrl + Shift + Right` | 多编辑器文件里切上一个 / 下一个标签页 |
| `Ctrl + L` | 滚动到中心 |

## 4️⃣ 补全、生成与模板

| 快捷键 | 动作 | 说明 |
| --- | --- | --- |
| `Ctrl + Space` | 基本补全 | 与系统输入法切换冲突时要改系统设置 |
| `Ctrl + Shift + Space` | 类型匹配补全 | 只补类型对得上的 |
| `Ctrl + Option + Space` | 第二基本补全 | 把 `String::new()` 之类补全成完整形式 |
| `Option + Return` | 显示上下文操作 | 快速修复（quick fix）+ 意图动作 |
| `Option + Cmd + Return` | 显示快速操作弹出窗口 | |
| `Cmd + N` | 生成… / 新建… | 编辑器内是「生成」（Getter、构造函数…），项目树里是「新建」 |
| `Ctrl + Return` | 生成… | `Cmd + N` 的备选 |
| `Ctrl + Option + N` | 在当前目录中新建… | |
| `Ctrl + O` / `Ctrl + I` | 重写方法… / 实现方法… | Rust 里对应 `impl` 补全 |
| `Cmd + P` | 形参信息 | 看函数签名 |
| `Tab` / `Shift + Tab` | 下一个 / 上一个形参 | 补全弹窗或形参提示里用 |
| `Shift + Cmd + N` | 临时文件（Scratch File） | 随手写代码不用建文件 |

## 5️⃣ 代码导航

| 快捷键 | 动作 |
| --- | --- |
| `Cmd + B` | 前往声明或用法（等价 `Cmd + 单击`） |
| `Option + Cmd + B` | 转到实现 |
| `Shift + Cmd + B` | 转到类型声明（`Ctrl + Shift + B` 亦可） |
| `Cmd + U` | 转到 Super 方法 |
| `Cmd + O` | 转到类… |
| `Shift + Cmd + O` | 转到文件… |
| `Option + Cmd + O` | 转到符号… |
| `Cmd + L` | 转到行:列… |
| `Ctrl + Cmd + Up` | 相关符号… |
| `Option + Space` | 快速定义（`Cmd + Y` 亦可） |
| `F1` | 快速文档（`Ctrl + J` 亦可；MacBook 上按 `Fn + F1`） |
| `Cmd + F1` | 错误描述 |
| `Cmd + F12` | 文件结构（当前文件里的项、函数、结构体…） |
| `Option + Cmd + F12` | 文件路径 |
| `Option + F1` | 选择位置…（在项目树 / 终端 / Finder 里定位当前文件） |
| `F3` | 切换书签 |
| `Cmd + F3` | 显示书签… |
| `Option + F3` | 切换书签助记符… |
| `Ctrl + 1` … `Ctrl + 9` | 跳到编号书签 |
| `Ctrl + Shift + 1` … `Ctrl + Shift + 9` | 设置编号书签 |
| `Option + Tab` / `Option + Shift + Tab` | 跳到下一个 / 上一个拆分器 |

## 6️⃣ 查找、替换与用法

| 快捷键 | 动作 |
| --- | --- |
| `Cmd + F` / `Cmd + R` | 查找… / 替换… |
| `Cmd + G` / `Shift + Cmd + G` | 下一个 / 上一个匹配项 |
| `Shift + Cmd + F` / `Shift + Cmd + R` | 在文件中查找… / 在文件中替换… |
| `Ctrl + Option + E` | 仅在选区内搜索 |
| `Option + Down` | 显示搜索历史记录（在查找框里） |
| `Option + F7` | 查找用法（全项目） |
| `Cmd + F7` | 在文件中查找用法 |
| `Option + Cmd + F7` | 显示用法（弹窗预览） |
| `Shift + Cmd + F7` | 高亮显示文件中的用法 |
| `Option + Shift + Cmd + F7` | 查找用法设置… |
| `Ctrl + G` | 将下一个匹配项添加到选择（多光标） |
| `Ctrl + Cmd + G` | 选择所有匹配项 |
| `Ctrl + Shift + G` | 取消选择匹配项 |
| `Ctrl + H` | 类型层次结构 |
| `Shift + Cmd + H` | 方法层次结构 |
| `Ctrl + Option + H` | 调用层次结构 |

## 7️⃣ 重构

| 快捷键 | 动作 |
| --- | --- |
| `Ctrl + T` | 重构…（重构菜单，想不起来就按它） |
| `Shift + F6` | 重命名… |
| `Cmd + F6` / `Shift + Cmd + F6` | 更改签名… / 类型迁移… |
| `Option + Cmd + M` | 提取方法… |
| `Option + Cmd + V` | 引入变量… |
| `Option + Cmd + F` | 引入字段… |
| `Option + Cmd + C` | 引入常量… |
| `Option + Cmd + P` | 引入形参… |
| `Option + Cmd + N` | 内联… |
| `Cmd + Forward Delete` | 安全删除…（MacBook 上先按住 `Cmd`，再按 `Fn + Delete`） |
| `F5` / `F6` | 复制… / 移动… |
| `Option + Cmd + T` | 环绕方式… |

## 8️⃣ 运行与调试

| 快捷键 | 动作 | 说明 |
| --- | --- | --- |
| `Ctrl + R` | 运行 | 注意不是 `Cmd + R` |
| `Ctrl + D` | 调试 | |
| `Ctrl + Shift + R` | 运行上下文配置 | 直接跑光标所在的 `main` / 测试 |
| `Ctrl + Shift + D` | 调试上下文配置 | |
| `Ctrl + Option + R` / `Ctrl + Option + D` | 运行… / 调试… | 弹出配置列表让你选 |
| `Cmd + F9` / `Shift + Cmd + F9` | 构建项目 / 重新构建 | |
| `Cmd + F2` | 停止 | |
| `Shift + Cmd + F2` | 停止后台进程… | |
| `Cmd + R` | 重新运行 | 焦点在运行工具窗口时；编辑器里 `Cmd + R` 是「替换」 |
| `Cmd + F8` | 切换行断点 | |
| `Option + Shift + Cmd + F8` | 切换临时行断点 | |
| `Shift + Cmd + F8` | 查看断点… | |
| `Option + Cmd + R` | 恢复程序 | `F9` 亦可 |
| `F7` / `F8` / `Shift + F8` | 步入 / 步过 / 步出 | |
| `Shift + F7` | 智能步入 | 一个表达式里有多个方法时让你选 |
| `Option + Shift + F7` / `Option + Shift + F8` | 强制步入 / 强制步过 | 会跟进标准库、依赖库源码 |
| `Option + F9` / `Option + Cmd + F9` | 运行到光标处 / 强制运行到光标 | |
| `Option + F8` | 对表达式求值… | |
| `Option + Cmd + F8` | 对表达式快速求值 | 选中表达式直接看值 |
| `Option + F10` | 显示执行点 | 断点停住后跳回当前行 |
| `Insert` | 新建监视… | 笔记本上没有 `Insert` 键，先试 `Fn + Enter` |
| `F2` | 设置值… | 调试器里改变量 |
| `Option + Shift + F5` | 附加到进程… | |
| `Ctrl + Cmd + R` / `Option + Shift + R` | 重新运行测试 | |
| `Ctrl + Shift + Down` | 显示标签页列表 | 打开的编辑器太多时 |

## 9️⃣ Rust / Cargo 专属

把 IDE 里全部插件描述符扫了一遍，结论很明确：**RustRover 2026.2 里 Rust / Cargo 相关的动作一个默认键位都没有**——JetBrains 只给了菜单项和工具窗口，没给键位。所以下面这些得自己绑（`Shift + Cmd + A` 搜到动作 → 在列表里按 `Option + Return` → 按下你想要的键）：

| 动作（`Shift + Cmd + A` 里搜） | 干什么 |
| --- | --- |
| 运行 Cargo 命令 | 弹出 Cargo 命令输入框（`cargo test`、`cargo clippy`…） |
| 刷新 Cargo 项目 | 更新 Cargo 项目信息、下载新依赖 |
| 使用 Rustfmt 重新设置文件格式 | 用 rustfmt 格式化当前文件 |
| 使用 Rustfmt 重新设置 Cargo 项目的格式 | 整个项目跑 rustfmt |
| 显示宏展开 / 显示递归宏展开 | 看 `macro_rules!` / 派生宏展开了什么 |
| 即时运行外部 Linter (Cargo Check/Clippy) | 打开 on-the-fly 外部 linter |
| 新建 Rust 文件 / Cargo Crate | 新建文件 / crate |
| 附加 Cargo 项目 / 分离 Cargo 项目 | 多 crate 工作区里手动挂载 |
| Rust REPL | 打开 Rust 交互式解释器 |

几个配套事实，省得你到处找：

- **Cargo 工具窗口**（右侧条带上的 `Cargo`）没有数字编号，所以 `Cmd + 1`…`Cmd + 9` 里没有它，用 `Shift + Cmd + A` 搜「Cargo」最快。
- **`Cargo.toml` 改动会自动重新加载 Cargo 变更**，通知气泡里可以「禁用自动重新加载」；手动刷新用上面那条「刷新 Cargo 项目」，Cargo 工具窗工具栏上也有刷新按钮。
- **格式化**：默认格式化键是 `Option + Cmd + L`（走 IDE 内置格式器）。想改用 rustfmt，去 `Settings → Languages & Frameworks → Rust → Rustfmt` 启用；那里还有「保存时配置操作…」，可以把格式化挂到保存动作上。
- ⚠️ 键位表里 `Shift + Cmd + O` 同时挂着「重新加载外部项目（Cargo 刷新）」和「转到文件…」，实际会和 Go to File 撞车——**刷新 Cargo 项目请用 `Shift + Cmd + A` 搜动作名或 Cargo 工具窗**，别指望这个组合键。

## 🔟 Git 与版本控制

| 快捷键 | 动作 |
| --- | --- |
| `Ctrl + V` | VCS 操作弹出窗口…（注意是 `Ctrl` 不是 `Cmd`，Git 的入口） |
| `Cmd + K` | 提交… |
| `Shift + Cmd + K` | 推送… |
| `Cmd + T` | 更新项目（拉取） |
| `Shift + Cmd + M` | 移至另一个更改列表…（行级操作亦可） |
| `Option + Cmd + Z` | 回滚… / 回滚行 |
| `Shift + Cmd + H` | 无提示搁置 |
| `Option + Cmd + U` | 无提示取消搁置 |
| `Shift + Cmd + U` | 取消搁置… |
| `Option + Cmd + A` | 添加到 VCS |
| `Ctrl + Option + M` | 修正提交（Amend） |
| `Ctrl + M` | 提交消息历史记录 |
| `Option + Cmd + N` | 新建分支… |
| `Ctrl + Cmd + A` | 显示所有受影响的文件 |
| `Ctrl + Option + Shift + Down` / `Up` | 下一个 / 上一个更改 |
| `F7` / `Shift + F7` | 下一个 / 上一个差异（差异查看器里） |
| `Cmd + D` | 显示差异（差异/比较上下文里） |
| `Ctrl + Cmd + Right` / `Ctrl + Cmd + Left` | 接受左侧 / 接受右侧 |
| `Cmd + Esc` | 收起文件（组合差异里折叠文件） |
| `F2` / `Shift + F6` | 编辑提交消息 / 重命名分支（上下文相关） |
| `Shift + Cmd + D` | 显示差异设置弹出窗口… |

## 1️⃣1️⃣ 工具窗口、标签页与窗口

| 快捷键 | 工具窗口 |
| --- | --- |
| `Cmd + 0` | 提交 |
| `Cmd + 1` | 项目 |
| `Cmd + 2` | 书签 |
| `Cmd + 3` | 查找 |
| `Cmd + 4` | 运行 |
| `Cmd + 5` | 调试 |
| `Cmd + 6` | 问题 |
| `Cmd + 7` | 结构 |
| `Cmd + 8` | 服务 |
| `Cmd + 9` | 版本控制（Git） |
| `Option + F12` | 终端 |

| 快捷键 | 动作 |
| --- | --- |
| `Cmd + W` | 关闭标签页 |
| `Ctrl + Shift + F4` | 关闭活动标签页（连带分屏） |
| `Shift + Cmd + ]` / `Shift + Cmd + [` | 选择下一个 / 上一个标签页（`Ctrl + Right` / `Left` 亦可） |
| `Ctrl + Tab` | 切换器（按住 `Ctrl` 连按 `Tab`，`Ctrl + Shift + Tab` 反向） |
| `Cmd + Backtick` | 激活下一个窗口 |
| `Shift + Cmd + Backtick` | 激活上一个窗口 |
| `Option + Cmd + Backtick` / `Option + Shift + Cmd + Backtick` | 下一个 / 上一个项目窗口 |

## 1️⃣2️⃣ 终端

| 快捷键 | 动作 |
| --- | --- |
| `Option + F12` | 打开 / 关闭终端 |
| `Cmd + R` | 在命令历史记录中搜索（终端内） |
| `Cmd + Return` | 用 IDE 运行高亮显示的命令 |
| `Cmd + C` / `Cmd + V` | 终端里复制 / 粘贴（`Cmd + Insert` 也能复制） |

## 1️⃣3️⃣ 鼠标与触控板

| 操作 | 效果 |
| --- | --- |
| `Cmd + 单击` | 前往声明或用法 |
| `Option + Cmd + 单击` | 转到实现 |
| `Shift + Cmd + 单击` | 转到类型声明 |
| 中键单击 | 前往声明 |
| `Option + 单击` | 添加 / 移除多光标 |
| `Option + Shift + 拖动` | 矩形选区（列选择） |
| `Option + Shift + 单击` | 对表达式快速求值（调试时） |
| 鼠标侧键（4/5 号键） | 后退 / 前进 |
| 用力点按（Force Touch） | 前往声明；调试时是「运行到光标处」 |

## 1️⃣4️⃣ 几个容易踩的坑

| 坑 | 说明 |
| --- | --- |
| `Cmd + R` 有两个身份 | 编辑器里是「替换…」，焦点在运行工具窗口时是「重新运行」。 |
| 运行 / 调试不是 `Cmd` | 是 `Ctrl + R` / `Ctrl + D`；`Cmd + R` / `Cmd + D` 另有含义。 |
| `Ctrl + Shift + R` ≠ `Shift + Cmd + R` | 前者是「运行上下文配置」，后者是「在文件中替换…」。 |
| `Cmd + Delete` ≠ `Cmd + Forward Delete` | 前者删行，后者是安全删除；笔记本上前向删除要加 `Fn`。 |
| 键位表里有、但需要语言支持的动作 | `Shift + Cmd + T`（转到测试）、`F10`（切换头/源）这类动作在 Rust 里没有对应实现，按了没反应属正常。 |
| 输入法抢键 | 系统若把输入法切换设为 `Ctrl + Space`，补全会失效，去系统设置里改。 |
| 同一个键、不同面板两种含义 | `F2` 在编辑器里是「下一个错误」，在调试器变量表里是「设置值…」；`F7` 在编辑器里是「下一个差异」，调试时是「步入」；`Cmd + D` 在编辑器里是「重复行」，差异视图里是「显示差异」。 |
| `F1`–`F12` 要先按 `Fn` | 不带修饰键的 F 键（`F2`、`F7`、`F12`…）默认被系统截走，触发的是亮度 / 音量 / 播放等；带修饰键的通常能直接送达。 |

## 1️⃣5️⃣ 改键位 / 查当前键位

- 看某个动作的键位：`Shift + Cmd + A` 搜动作名，列表右侧就写着键位；或直接在菜单栏里对。
- 加 / 改键位：`Shift + Cmd + A` 里选中动作按 `Option + Return`；或 `Cmd + ,` → `Keymap`，右键动作 → `Add Keyboard Shortcut`。
- 建议先复制一份键位表再改：`Keymap` 页面右上角齿轮 → `Duplicate`，改坏了可以切回 `macOS`。
- 想看别的编辑器的习惯：JetBrains 市场里有 VS Code / Eclipse / Xcode 等键位表插件。
- 想让 IDE 主动教你键位：装 `Key Promoter X` 插件，用鼠标点命令时会提示对应快捷键。
