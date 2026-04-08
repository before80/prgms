+++
title = "第6章 VSCode和Python"
weight = 60
date = "2026-04-08T13:22:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 第六章：VS Code——Python 开发者的高配游戏房

> 🎮 "VS Code 不只是编辑器，它是 Python 程序员的车载导航 + 游戏手柄 + 空调出风口香薰的豪华套餐。"

想象一下，你有一间豪华游戏房，里面摆满了各种神器手柄、4K 大屏、人体工学椅——而隔壁的「记事本」同学还在用着黑白电视搓手柄。这一章，我们就把你的"游戏房"——VS Code——彻底装修成 Python 开发者的天堂。

准备好了吗？Let's go! 🚀

---

## 6.1 VS Code 下载与安装

### 6.1.1 下载地址

首先，你得把这尊"神器"请回家。

**下载地址：** [https://code.visualstudio.com/Download](https://code.visualstudio.com/Download)

打开页面，你会看到三个肤色（划掉）三个版本：

| 系统 | 下载选项 | 适合人群 |
|------|----------|----------|
| **Windows** | User Installer / System Installer / .zip | 普通用户 / 管理员 / 极客 |
| **macOS** | .zip / .dmg | 苹果粉丝 |
| **Linux** | .deb / .rpm / .tar.gz | 企鹅爱好者 |

> 💡 **小贴士**：Windows 用户推荐下载 **User Installer**（绿色环保版），装在自己用户目录下，不需要管理员权限。System Installer 则是装到 Program Files，全局可用。.zip 版本解压即用，适合"随身携带版"。

**校验 SHA256（可选但推荐）：**

下载完成后，如果你是强迫症患者，可以去验证一下文件完整性：

```powershell
# Windows PowerShell
certutil -hashfile VSCodeUserSetup-x64-1.XX.X.exe SHA256
```

去官网对着看看哈希值对不对——这感觉就像拆快递前确认封条完好无损。📦

---

### 6.1.2 安装后首次运行设置

装好 VS Code 后，第一次打开它，你会看到这样的界面：

```
┌─────────────────────────────────────────────────┐
│  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  │
│  ░░░░░░░░░ VS Code 欢迎界面 ░░░░░░░░░░░░░░░░░░░  │
│  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  │
│  欢迎使用 VS Code！                              │
│  开始：打开文件夹 / 新建文件 / 安装扩展          │
│  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  │
└─────────────────────────────────────────────────┘
```

此时恭喜你，你拿到了毛坯房钥匙，接下来我们要开始装修了。

---

#### 6.1.2.1 安装中文语言包（Chinese (Simplified)）

默认情况下，VS Code 像个ABC一样跟你说英语。别慌，咱给它安排一个中文输入法——语言包扩展。

**操作步骤：**

1. 按下 `Ctrl + Shift + P`（或 `Cmd + Shift + P` on macOS），调出**命令面板**
2. 输入 `Configure Display Language`
3. 选择 `Install Additional Languages`
4. 在扩展商店里找到 **Chinese (Simplified)**，点击安装

或者更暴力的方法——直接搜索扩展：

```
Ctrl + Shift + X  →  搜索 "chinese"
```

找到 Microsoft 官方的 `Chinese (Simplified)`，install，然后 **reload**。

> 😆 **工程师的笑话**：有人说"编程5分钟，配环境3小时"。其实配 VS Code 也差不多——你花了10分钟安装语言包，感觉自己像个真正的国际化工程师。

---

#### 6.1.2.2 设置主题（Dark / Light）

VS Code 默认是深色主题（Dark+），看起来很酷，但有时候你可能想在白天用浅色主题保护眼睛。

**操作步骤：**

1. `Ctrl + Shift + P` → 输入 `theme`
2. 选择 `Preferences: Color Theme`
3. 在下拉列表里选一个你喜欢的

**常见主题推荐：**

| 主题名称 | 风格 | 推荐指数 |
|----------|------|----------|
| **Dark+ (default dark)** | 经典深色 | ⭐⭐⭐⭐ |
| **Light+ (default light)** | 经典浅色 | ⭐⭐⭐ |
| **Monokai** | 程序员的浪漫 | ⭐⭐⭐⭐⭐ |
| **One Dark Pro** | 护眼深色 | ⭐⭐⭐⭐⭐ |
| **GitHub Dark** | GitHub 风格 | ⭐⭐⭐⭐ |
| **Solarized Light** | 经典浅色 | ⭐⭐⭐ |

> 🎨 **设计师的碎碎念**：选主题就像选衣服——不用太纠结，反正你迟早会换到下一个。但别用默认主题，那感觉就像穿着睡衣出门上班。

**图标主题（可选）：**

`Ctrl + Shift + P` → `Preferences: File Icon Theme`

推荐 **Material Icon Theme**，文件夹和文件类型一目了然，妈妈再也不用担心我找不到 `.py` 文件了。

---

#### 6.1.2.3 设置字体

代码字体是有讲究的！不是说宋体不行，而是等宽字体（Monospace）才是程序员的最爱——每个字符占的宽度一样，代码对不齐会逼死强迫症。

**推荐字体：**

| 字体 | 特点 | 好感度 |
|------|------|--------|
| **JetBrains Mono** | 专为代码设计，免费开源 | ❤️❤️❤️❤️❤️ |
| **Fira Code** | 带连字（ligatures），酷炫 | ❤️❤️❤️❤️ |
| **Consolas** | Windows 自带，够用 | ❤️❤️❤️ |
| **Source Code Pro** | Adobe 出品，清晰 | ❤️❤️❤️❤️ |
| **Cascadia Code** | 微软官方 Code 字体 | ❤️❤️❤️❤️ |

> 🔤 **等宽字体的好处**：想象一下用比例字体（比如宋体）对齐代码——`iii` 和 `mmm` 宽度不同，你的代码会歪得像比萨斜塔。等宽字体让世界从此整齐。

**设置步骤：**

1. `Ctrl + ,` 打开设置
2. 搜索 `font`
3. 在 **Font Family** 里填写你喜欢的字体，记住要用引号包起来

```json
// settings.json
{
    "editor.fontFamily": "'JetBrains Mono', 'Fira Code', Consolas, 'Courier New', monospace",
    // "'Courier New' 是备胎，monospace 是最后的保险"
}
```

> 🔗 **连字（Ligatures）**：Fira Code 和 JetBrains Mono 支持连字——把 `->` 显示成箭头 `→`，`!=` 显示成真正的"不等于"符号。酷是酷，但看久了可能不习惯调试时的原始符号。

---

#### 6.1.2.4 设置字号

同样的，在设置里搜索 `Font Size`：

```json
// settings.json
{
    "editor.fontSize": 14,
    // 14 号字体是个不错的起点
    // 眼睛累？调大！18 也常见
    // 想塞下更多代码？12 也行，看你心情
}
```

> 👴 **老法师的建议**：别把字号设太大，不然你看一个2000行的文件要滚10次鼠标。也别太小，不然你会在眯眼看代码的过程中悟出人生哲学。14-16是黄金区间。

---

## 6.2 必装插件清单（详细说明）

> 🛒 **Warning**：VS Code 的扩展商店有超过30,000个插件。装太多会让你开机像启动《变形金刚》。这里只推荐**真正改变你人生**的必备插件。

### 6.2.1 Python 扩展（Microsoft 官方）

**插件名称：** Python（by Microsoft）

**安装方式：**

```
Ctrl + Shift + X  →  搜索 "python"  →  选择 Microsoft 官方 Python 扩展  →  Install
```

#### 6.2.1.1 功能：智能提示、调试、代码导航、单元测试

这货是 VS Code 里的 Python 大当家。没有它，VS Code 就是个带语法高亮的记事本。

**功能清单：**

- **IntelliSense（智能提示）**：输入 `str.` 之后，你会看到一整面的方法列表——`upper()`, `split()`, `replace()` 等等，不用背了，用就完了。
- **Lint 检查**：实时告诉你代码哪里可能出错（比如 `undefined name 'foo'`）
- **调试**：图形化断点调试（下一节会细讲）
- **代码导航**：跳转到定义（Go to Definition）、查找引用（Find References）
- **单元测试**：支持 `unittest`、`pytest`、`nose2`，一键运行测试用例

> 🧠 **IntelliSense 是什么？**：可以理解为"超级自动补全"。不是简单的敲什么补什么，而是能理解你代码的上下文，猜你想写什么。堪称编程界的读心术。

#### 6.2.1.2 安装后 reload

安装完 Python 扩展后，VS Code 会提示你 **reload**（重载窗口）。别愣着，点它！

有时候 reload 后还在右下角弹个小窗说"需要安装 Python 解释器"——这是正常现象，点进去选择你的 Python 路径即可。

```
右下角弹窗：「需要安装 Python 扩展才能进行 Python 调试。...」
→ 点 "Install"，VS Code 会引导你装
→ 或者手动：Ctrl + Shift + P → Python: Select Interpreter
```

---

### 6.2.2 Pylance

**插件名称：** Pylance（by Microsoft）

**安装方式：**

```
Ctrl + Shift + X  →  搜索 "pylance"  →  Install
```

#### 6.2.2.1 功能：静态类型检查、语义分析、超高速补全

Pylance 是 Python 扩展的**灵魂伴侣**。它是基于 Pyright（微软的 Python 类型检查器）构建的，性能爆表。

**三大核心能力：**

1. **静态类型检查**：如果你写了带类型注解的代码，Pylance 会实时检查类型错误。比如你声明 `x: int = "hello"`，它会立刻给你一个红色的波浪线。
2. **语义分析**：理解代码的深层含义，不只是语法
3. **超高速补全**：基于语义分析而非纯文本匹配，补全速度快到离谱

> ⚡ **静态类型检查**：Python 本身是动态类型语言——变量类型是运行时才确定的。但加了类型注解（Type Hints）后，Pylance 就能在写代码时就发现类型错误，而不用等到运行。比如 `def greet(name: str) -> str: return 2024` 会被报错，因为返回类型声明是 `str` 但实际返回了 `int`。

#### 6.2.2.2 与 Python 扩展配合使用

**Python 扩展 + Pylance = 王炸组合。**

实际上，当你安装 Python 扩展时，VS Code 有时会**自动**推荐你安装 Pylance。如果没有，就手动装上。

```
Python 扩展负责：运行、调试、测试
Pylance 负责：智能提示、类型检查、代码理解
```

二者分工明确，珠联璧合。

---

### 6.2.3 Ruff

**插件名称：** Ruff（by Astral Software）

**安装方式：**

```
Ctrl + Shift + X  →  搜索 "ruff"  →  Install
```

#### 6.2.3.1 功能：Lint（代码检查）+ Format（格式化），极速

Ruff 是用 Rust 写的 Python Lint + Format 工具。快到什么程度？比传统的 `flake8 + black + isort` 快 **10-100倍**。

**Lint（代码检查）**：检查代码中的潜在错误和风格问题
- 未使用的变量
- 导入顺序混乱
- 过长函数
- 等等……

**Format（格式化）**：自动把你的代码排版成"标准格式"，不用再纠结"这行缩进用 Tab 还是空格"这种哲学问题。

#### 6.2.3.2 替代 flake8 + black + isort 的三合一工具

在 Ruff 出现之前，Python 程序员需要安装三个工具：

```
flake8   →  代码检查
black    →  代码格式化
isort    →  import 排序
```

现在一个 Ruff 全搞定，而且速度是这三个加起来的几十倍。

> 😂 **程序员的黑话**：以前有人说"我的代码能跑"是自信的表现。现在有了 Ruff，"我的代码格式正确、导入整齐、还没有 lint 警告"才是真自信。

#### 6.2.3.3 安装后启用 format provider

装完 Ruff 后，还需要配置一下让它提供格式化服务：

**settings.json 配置：**

```json
// settings.json
{
    // Ruff 格式化与 Lint 配置（对所有语言生效）
    "ruff.formatter.preview": true,              // 启用 Ruff 自带的格式化器（推荐！）
    "ruff.lint.args": ["--config=pyproject.toml"], // 告诉 Ruff 去哪里找配置文件

    // Python 文件专属设置
    "[python]": {
        "editor.defaultFormatter": "charliermarsh.ruff",
        // Ruff 负责格式化
        "editor.formatOnSave": true,              // 保存时自动格式化
        "editor.codeActionsOnSave": {
            "source.fix.all": "explicit",
            // 保存时自动修复 lint 问题
            "source.organizeImports": "explicit"
            // 保存时自动整理 import
        }
    }
}
```

**Ruff 配置文件（pyproject.toml）示例：**

```toml
# pyproject.toml
[tool.ruff]
# 启用 lint 规则
rule_select = [
    "E",    # pycodestyle errors
    "W",    # pycodestyle warnings
    "F",    # Pyflakes
    "I",    # isort
    "N",    # pep8-naming
    "UP",   # pyupgrade
]
ignore = [
    "E501", # 行太长（由 formatter 处理）
]

[tool.ruff.format]
# 使用 Ruff 自带的 formatter（已通过 ruff.formatter.preview = true 启用）
```

---

### 6.2.4 Black Formatter

**插件名称：** Black（by Microsoft）

**安装方式：**

```
Ctrl + Shift + X  →  搜索 "black"  →  Install（Microsoft 出品）
```

#### 6.2.4.1 功能：固执己见的代码格式化

Black 是 Python 社区最流行的格式化工具。它的口号是：**"不妥协的 Python 代码格式化"**。

所谓"固执己见"——Black **本身不提供风格配置选项**！缩进用4个空格？行长度限制88字符？就这样，不接受反驳。（但你可以在 VS Code 中选择用它来格式化代码，见 6.3.3.1 节。）

好处是：团队里再也没人因为"你用的是单引号还是双引号"打起来了。

> 🎭 **Black 的哲学**：格式化代码是为了减少认知负担。当格式完全统一，代码审查时你只需要关注"逻辑"而不是"风格"。Black 让 Python 代码像高铁一样整齐有序。

#### 6.2.4.2 替代方案：Ruff Formatter（更快）

Ruff 也有自己的 formatter，而且比 Black **快10倍**。如果你追求速度，可以考虑：

```json
// settings.json
{
    "[python]": {
        "editor.defaultFormatter": "charliermarsh.ruff"
        // 用 Ruff 替代 Black 做格式化
    }
}
```

两者格式化结果**几乎一样**（都遵循 PEP 8），只是 Ruff 更快。如果你之前用的是 Black，保持现状也完全没问题。

---

### 6.2.5 autoDocstring - Python Docstring Generator

**插件名称：** autoDocstring - Python Docstring Generator（by Nils Werner）

**安装方式：**

```
Ctrl + Shift + X  →  搜索 "autodocstring"  →  Install
```

#### 6.2.5.1 功能：自动生成 docstring 模板

Docstring 就是函数/类上面的那个多行字符串，用来描述它是干什么的：

```python
def add(a, b):
    """
    计算两个数的和。

    Args:
        a: 第一个数
        b: 第二个数

    Returns:
        两个数的和
    """
    return a + b
```

有了 autoDocstring，你只需要敲三个引号 `"""`，然后按一下 `Tab`，它就会自动生成模板！

#### 6.2.5.2 支持 Google / NumPy / Sphinx docstring 风格

autoDocstring 支持多种 docstring 风格：

| 风格 | 说明 | 使用场景 |
|------|------|----------|
| **Google** | 简洁易读，社区主流 | 大多数项目 |
| **NumPy** | 详细严谨，适合科学计算 | NumPy, SciPy |
| **Sphinx** | reStructuredText 格式 | 文档生成工具 Sphinx |

**切换风格：**

```json
// settings.json
{
    "autoDocstring.docstringFormat": "google"
    // 可选值: "google" | "numpy" | "sphinx"
}
```

#### 6.2.5.3 使用方法

1. 在函数/类/方法的**第一行**输入 `"""` 或 `'''`
2. 按 `Tab` 或 `Enter`，自动生成模板
3. 填充参数描述

```
def calculate_area(radius):
    """Calculate the area of a circle.

    Args:
        radius (float): The radius of the circle.

    Returns:
        float: The area of the circle.
    """
    return 3.14159 * radius ** 2
#   ↑ 光标自动跳到这里等你填
```

> 📝 **Docstring 有多重要**：没有 docstring 的函数，就像没有说明书的产品——能用，但你不知道咋用。好的 docstring 让协作者（包括未来的你）不用猜谜。

---

### 6.2.6 Python Debugger

**插件名称：** Python Debugger（by Microsoft）

**安装方式：**

```
Ctrl + Shift + X  →  搜索 "python debugger"  →  Install
```

#### 6.2.6.1 功能：图形化调试（替代旧的 ptvsd）

这货是新一代 Python 调试器，替代了已经退役的旧版 `ptvsd`。基于 `debugpy` 开发，功能更强大，配置更简单。

**图形化调试是什么概念？**

- 传统调试：print 大法——满屏 print，输出信息看得眼花缭乱
- 图形调试：断点 + 变量面板 + 调用堆栈 = 开着透视镜打游戏

#### 6.2.6.2 支持断点、条件断点、变量监视

- **断点（Breakpoint）**：代码跑到某一行自动暂停
- **条件断点**：只有满足某个条件才暂停（比如 `count > 10`）
- **变量监视（Watch）**：盯着某个变量，它变你就知道
- **调用堆栈（Call Stack）**：看到当前执行到哪了、从哪调过来的

> 🕹️ **打游戏的比喻**：断点就像游戏里的暂停键（Pause），Watch 就像小地图上的敌人位置显示，Call Stack 就像游戏里的"从哪里来的"导航。

---

### 6.2.7 Jupyter

**插件名称：** Jupyter（by Microsoft）

**安装方式：**

```
Ctrl + Shift + X  →  搜索 "jupyter"  →  Install
```

#### 6.2.7.1 功能：Jupyter Notebook 支持

Jupyter Notebook 是数据科学家的最爱，`.ipynb` 文件格式。你可以直接在 VS Code 里编辑和运行它，而不用开浏览器。

#### 6.2.7.2 .ipynb 文件编辑和运行

安装 Jupyter 插件后：

1. 打开 `.ipynb` 文件
2. 代码单元格左侧会有 **Run** 按钮 ▶️
3. 按 `Shift + Enter` 运行当前格并跳到下一格
4. 变量会在右侧 **Jupyter Variables** 面板中实时显示

> 🔬 **数据科学家的日常**：以前写 Python 验证一个想法要：新建 .py → 写代码 → 运行 → 看报错 → 修改 → 重复。现在用 Jupyter，代码分段执行，所见即所得，效率翻倍。

---

### 6.2.8 Python Environment Manager

**插件名称：** Python Environment Manager（by Microsoft）

**安装方式：**

```
Ctrl + Shift + X  →  搜索 "python environment manager"  →  Install
```

#### 6.2.8.1 功能：管理多个 Python 环境

你可能在同一台机器上装了很多个 Python：

- 系统 Python 3.9
- Anaconda Python 3.11
- 自己编译的 Python 3.12
- 某个项目的虚拟环境 `.venv`

这个插件让你**一键切换**，不用每次都 `which python` 找半天。

#### 6.2.8.2 一键切换虚拟环境

**使用方法：**

1. `Ctrl + Shift + P` → `Python: Select Interpreter`
2. 下拉列表显示所有可用的 Python 环境
3. 点哪个，哪个就是当前运行环境

```
🥒 Conda 环境: base, tensorflow, pytorch
🐍 系统 Python: /usr/bin/python3.9
📦 venv 环境: ./venv/bin/python
🎯 项目专用: /home/dev/my-project/.venv/bin/python
```

> 🌿 **虚拟环境有多重要**：假设项目A用 Django 4.0，项目B用 Django 3.2——不隔离环境的话，装了4.0就毁了3.2。虚拟环境就是每个项目的"独立宇宙"，各玩各的，互不干扰。

---

### 6.2.9 GitHub Copilot / GitHub Copilot Chat

**插件名称：** GitHub Copilot + GitHub Copilot Chat（by GitHub）

**安装方式：**

```
Ctrl + Shift + X  →  搜索 "copilot"  →  Install
```

> ⚠️ **注意**：Copilot 是付费服务（新用户有60天免费试用）。如果你有 GitHub 学生身份，可以免费使用。

#### 6.2.9.1 AI 代码补全

Copilot 会根据你写的上下文**自动生成代码建议**。你写了函数名和注释，它就能猜出你要写什么。

```
def fibonacci(n):
    """生成斐波那契数列的前 n 项"""
    if n <= 0:
        return []
    # Copilot 自动补全后面所有代码！
```

#### 6.2.9.2 AI 代码问答

Copilot Chat 更是神器——你在 VS Code 里直接问它问题：

```
"这段正则表达式是干嘛的？"
"帮我优化这个慢查询"
"解释一下这个函数的逻辑"
```

不用切换到浏览器问 ChatGPT，VS Code 里直接搞定。

> 🤖 **AI 会取代程序员吗**：Copilot 的定位是"副驾驶"（Copilot），不是"自动驾驶"。它帮你写样板代码，但架构设计、问题排查还是得靠你。善用 AI，卷死那些不会用 AI 的同事。😏

---

### 6.2.10 Error Lens

**插件名称：** Error Lens（by Alexander）

**安装方式：**

```
Ctrl + Shift + X  →  搜索 "error lens"  →  Install
```

#### 6.2.10.1 功能：代码错误直接高亮显示

这货把代码错误/警告**直接打在代码旁边**——不用 hover 去看 tooltip，一眼就看到问题在哪。

```
✖ 划时代错误：你写的代码让宇宙秩序混乱了
│  File "app.py", line 15
│    print("hello)
                 ^^^^^ SyntaxError: EOL while scanning string literal
```

> 👓 **懒人福音**：以前你要把鼠标悬停在红色波浪线上等 tooltip，现在是贴脸输出。Error Lens 让错误无处藏身。

---

### 6.2.11 Thunder Client

**插件名称：** Thunder Client（by Thunder Extension）

**安装方式：**

```
Ctrl + Shift + X  →  搜索 "thunder client"  →  Install
```

#### 6.2.11.1 功能：轻量级 API 测试工具（类似 Postman）

Thunder Client 是 VS Code 里的轻量级 HTTP 客户端，用来测试 API 接口。

Postman 要单独装一个 App，Thunder Client 直接装在 VS Code 里，**更轻、更快、更极简**。

#### 6.2.11.2 .http 文件直接在 VS Code 测试 API

Thunder Client 支持 `.http` 文件格式——这是一种纯文本的 HTTP 请求描述语言：

```http
### 获取用户列表
GET https://api.example.com/users
Content-Type: application/json

### 创建新用户
POST https://api.example.com/users
Content-Type: application/json

{
    "name": "张三",
    "email": "zhangsan@example.com"
}

### 登录
POST https://api.example.com/login
Content-Type: application/x-www-form-urlencoded

username=admin&password=123456
```

打开 `.http` 文件，点击发送按钮，就能测试 API。

> 📡 **后端工程师的日常**：写完一个 API，要不要用 Postman 测试一下？Thunder Client 让你在编辑器里直接搞定，不用切来切去。

---

### 6.2.12 REST Client

**插件名称：** REST Client（by Huachao Mao）

**安装方式：**

```
Ctrl + Shift + X  →  搜索 "rest client"  →  Install
```

#### 6.2.12.1 功能：发送 HTTP 请求，测试 API

REST Client 和 Thunder Client 功能类似，也是 `.http` 文件驱动。它的特点是可以直接在编辑器里看到响应，不需要额外的 UI。

```http
### 简单的 GET 请求
GET https://httpbin.org/get

### 带查询参数
GET https://httpbin.org/get?key=value&name=test

### 发送 JSON
POST https://httpbin.org/post
Content-Type: application/json

{
    "username": "admin",
    "password": "secret"
}
```

> 🔧 **选 Thunder Client 还是 REST Client**：两者都能发 HTTP 请求。Thunder Client 有 UI（点击发送），REST Client 是纯文本驱动（写完直接点上面的 "Send Request"）。喜欢哪个用哪个，不打架。

---

### 6.2.13 GitLens

**插件名称：** GitLens — Git supercharged（by GitLens）

**安装方式：**

```
Ctrl + Shift + X  →  搜索 "gitlens"  →  Install
```

#### 6.2.13.1 功能：Git 增强，显示代码行提交历史

GitLens 把 Git 的力量直接灌进你的编辑器。每一行代码旁边都会显示：

```
最后是谁改的？ → "李四，2天前"
改了啥？       → hover 一下就能看到 diff
为什么改？     → 查看提交信息
```

以前想知道某行代码的历史，要 `git log -p`，现在**直接看**。

> 🕐 **考古学家工具**：当代码出现诡异行为时，GitLens 能帮你快速定位——这行代码是谁改的、什么时候改的、为什么改的。追查 bug 的效率提升100%。

---

### 6.2.14 Git History

**插件名称：** Git History（by Don Jayamanne）

**安装方式：**

```
Ctrl + Shift + X  →  搜索 "git history"  →  Install
```

#### 6.2.14.1 功能：查看文件修改历史、提交图

Git History 提供了可视化的 Git 历史图形界面：

- 查看某个文件的完整修改历史
- 查看分支图（Branch visualization）
- 比较不同提交之间的差异

```
Ctrl + Shift + P → Git History: View File History
或者右键文件 → View File History
```

> 🌳 **Git 分支图**：当你有一堆 feature branch、hotfix branch 在一起时，用 Git History 看到的图形化分支图比命令行输出的日志清晰一万倍。

---

### 6.2.15 Remote - SSH

**插件名称：** Remote - SSH（by Microsoft）

**安装方式：**

```
Ctrl + Shift + X  →  搜索 "remote ssh"  →  Install
```

#### 6.2.15.1 功能：远程服务器编辑代码

Remote - SSH 让你在本地 VS Code 里**直接编辑远程服务器上的文件**。

**使用场景：**

- 你的代码要跑在 Linux 服务器上
- 本地是 Windows，但服务器是 Linux
- 服务器有 GPU，你要在上面训练模型

#### 6.2.15.2 配合远程服务器上的 Python 环境

连接上远程服务器后，VS Code 会自动检测服务器上的 Python 环境，你可以：

1. 在远程服务器上安装 Python 扩展（VS Code 会提示）
2. 选择远程的 Python 解释器
3. 直接在本地断点调试远程代码！

```
连接步骤：
1. Ctrl + Shift + P → Remote-SSH: Connect to Host
2. 输入服务器地址：user@192.168.1.100
3. 输入密码或配置 SSH Key
4. 等待 VS Code Server 在服务器上安装
5. Done！远程文件尽在眼前
```

> 🖥️ **云端开发体验**：想象一下，你在咖啡厅用 MacBook，但代码跑在带 RTX 4090 的远程服务器上。Remote SSH 让你"本地手感 + 服务器算力"兼得。唯一的问题是——网断了就全断了。

---

## 6.3 settings.json 核心配置

> ⚙️ **settings.json 是什么？**：VS Code 的所有设置都保存在一个 JSON 文件里。你可以点 GUI 设置右上角那个 `{ }` 图标打开 raw JSON 编辑。直接改 JSON 比点点点更精确、更方便批量配置。

### 6.3.1 打开设置（settings.json）

**方法一：图形界面**

```
Ctrl + ,  →  右上角有个 { } 图标  →  点击它
```

**方法二：命令面板**

```
Ctrl + Shift + P  →  搜索 "Preferences: Open Settings (JSON)"  →  回车
```

**方法三：直接找文件**

```
# Windows
%APPDATA%\Code\User\settings.json

# macOS
~/Library/Application Support/Code/User/settings.json

# Linux
~/.config/Code/User/settings.json
```

> 📁 **settings.json 的作用域**：VS Code 有三层配置——默认（无法修改）、用户（全局）、工作区（当前项目）。工作区配置会覆盖用户配置。用工作区配置的好处是：项目 clone 到别的机器上，设置跟着走。

---

### 6.3.2 Python 解释器路径配置

#### 6.3.2.1 python.defaultInterpreterPath 配置

如果你想让 VS Code 每次打开都用同一个 Python 解释器，可以指定路径：

```json
// settings.json
{
    "python.defaultInterpreterPath": "C:/Python311/python.exe"
    // Windows 路径要用正斜杠或者双反斜杠
    // 或者 "C:\\Python311\\python.exe"
}
```

> 🐍 **解释器路径是什么**：Python 解释器就是那个能执行 `.py` 文件的程序。不同项目可能用不同版本——这个配置告诉 VS Code "用这个 Python 来跑我的代码"。

#### 6.3.2.2 自动选择当前工作区的虚拟环境

更好的做法是让 VS Code **自动检测**当前项目的虚拟环境：

```json
// settings.json
{
    "python.analysis.autoSearchPaths": true,
    "python.analysis.extraPaths": [],
    // 自动把当前目录加到 Python 路径中

    "python.venvFolders": [".venv", "venv", "env", ".env"],
    // VS Code 会自动在这些目录里找虚拟环境

    "python.testing.pytestEnabled": true,
    "python.testing.unittestEnabled": false,
    // 启用 pytest，关闭 unittest（根据你的使用习惯）
    "python.testing.pytestArgs": ["tests/"]
    // pytest 扫描 tests/ 目录
}
```

---

### 6.3.3 格式化工具配置

#### 6.3.3.1 python.formatting.provider 配置

指定用哪个工具来格式化 Python 代码：

如果你用 **Black** 格式化（传统方案）：

```json
// settings.json
{
    "python.formatting.provider": "black"
    // 可选: "black" | "yapf" | "autopep8"
}
```

如果你用 **Ruff Formatter**（推荐，比 Black 快 10 倍）：

```json
// settings.json
{
    // 不需要设置 python.formatting.provider
    // Ruff formatter 通过 [python].editor.defaultFormatter 配置（见下节）
}
```

#### 6.3.3.2 editor.formatOnSave 保存自动格式化

开启保存自动格式化，**妈妈再也不用担心我的代码风格不一致了**：

```json
// settings.json
{
    "editor.formatOnSave": true,
    // 保存时自动格式化

    "[python]": {
        "editor.formatOnSave": true
        // Python 文件专属：保存时自动格式化
    }
}
```

> 💾 **formatOnSave 的利与弊**：利——每次保存代码都是干净的，不用手动调格式。弊——如果 formatter 和 linter 有冲突，可能会有意外的 diff。建议配合 `.editorconfig` 或 `pyproject.toml` 精确定义格式化规则。

#### 6.3.3.3 editor.defaultFormatter 默认格式化器

设置默认的格式化器（对所有文件类型生效，你也可以专门为 Python 设置）：

```json
// settings.json
{
    // Python 文件用 Ruff 格式化（推荐，比 Black 快 10 倍）
    "[python]": {
        "editor.defaultFormatter": "charliermarsh.ruff"
    }
}
```

---

### 6.3.4 Lint 检查器配置

#### 6.3.4.1 python.linting.enabled

开启/关闭 Lint 功能：

```json
// settings.json
{
    "python.linting.enabled": true
    // true = 开启 lint（强烈推荐开启！）
    // false = 关闭（自断双臂行为）
}
```

#### 6.3.4.2 python.linting.ruffEnabled

启用 Ruff 作为 Lint 工具：

```json
// settings.json
{
    "python.linting.enabled": true,
    "python.linting.ruffEnabled": true,
    // 开启 Ruff lint

    "python.linting.flake8Enabled": false,
    // 如果用 Ruff，可以关闭 flake8（避免重复检查）

    "python.linting.pylintEnabled": false,
    // 如果用 Ruff，可以关闭 pylint

    "python.linting.banditEnabled": false
    // 如果用 Ruff，可以关闭 bandit（安全检查已被 Ruff 覆盖）
}
```

#### 6.3.4.3 python.linting.pylintEnabled

如果你更习惯用 pylint（传统老牌 lint），可以这样配置：

```json
// settings.json
{
    "python.linting.pylintEnabled": true,
    "python.linting.ruffEnabled": false,
    "python.linting.pylintArgs": [
        "--max-line-length=120",
        "--disable=missing-docstring",
        "--disable=C0114",
        "--disable=C0116"
        // 禁用你不需要的规则
    ]
}
```

> ⚖️ **Ruff vs Pylint**：Ruff 速度快（Rust 写的），规则多（900+ 条），但不支持自定义规则（固执己见风格）。Pylint 速度慢，可配置性极强，能写插件。日常开发用 Ruff 做快速检查，要深度分析时用 Pylint。

---

### 6.3.5 Pylance 高级选项

#### 6.3.5.1 python.analysis.typeCheckingMode

控制类型检查的严格程度：

```json
// settings.json
{
    "python.analysis.typeCheckingMode": "basic"
    // 可选值:
    // "off"    = 完全关闭类型检查（不推荐）
    // "basic"  = 基础检查，适合大多数项目（推荐）
    // "strict" = 严格检查，所有类型注解必须正确
}
```

#### 6.3.5.2 python.analysis.autoImportCompletions

自动导入补全——当你输入一个函数名但还没 import 时，Pylance 会自动补全 import 语句：

```json
// settings.json
{
    "python.analysis.autoImportCompletions": true,
    // 输入 "pandas" → 自动提示 import pandas
    // Tab 一下，import 就加上去了！

    "python.analysis.addImportStrategy": "full"
    // "full" = 完整导入（from xxx import yyy）
    // "shortest" = 最短导入（import xxx）
}
```

#### 6.3.5.3 python.analysis.diagnosticSeverityOverride

自定义某些诊断信息的严重程度（报错还是警告还是忽略）：

```json
// settings.json
{
    "python.analysis.diagnosticSeverityOverride": {
        // 把某些类型的诊断改成不同的严重级别
        "reportMissingTypeStubs": "none"
        // "none" = 完全忽略
        // "information" = 信息提示（灰色）
        // "warning" = 警告（黄色）
        // "error" = 错误（红色）
    }
}
```

---

### 6.3.6 代码风格配置

#### 6.3.6.1 editor.rulers（配合 Black）

Rulers 是在编辑器里显示的垂直参考线，帮助你控制代码行长度。Black 默认把行长度限制在 **88 字符**：

```json
// settings.json
{
    "editor.rulers": [88, 120]
    // 显示两条垂直参考线：88字符（Black 标准）和 120字符（自定义宽松线）
    // 超过 88 字符的那一行，右侧会有淡淡的竖线提醒你"太长了"

    // 建议配合 Black formatter 使用：
    "[python]": {
        "editor.rulers": [88]
        // Python 文件只显示 Black 的 88 字符线
    }
}
```

> 📏 **88 字符的由来**：Black 使用 88 字符是因为它比 PEP 8 的 79 字符更宽松一些，但又比无限长更克制。这是 Python 社区多年实践的折中值。

#### 6.3.6.2 files.trimTrailingWhitespace

去掉行尾的空格（这些空格在 Git 里经常造成无意义的 diff）：

```json
// settings.json
{
    "files.trimTrailingWhitespace": true,
    // 保存时自动去掉行尾空格

    "files.insertFinalNewline": true,
    // 文件末尾自动加一个空行（POSIX 规范）

    "files.trimFinalNewlines": true
    // 去掉文件末尾多余的空行
}
```

#### 6.3.6.3 editor.tabSize

缩进大小（Python 标准是 4 个空格）：

```json
// settings.json
{
    "editor.tabSize": 4,
    // Tab 键产生的空格数

    "editor.insertSpaces": true,
    // 按 Tab 时插入空格而不是 Tab 字符（强烈推荐！）

    "editor.detectIndentation": false
    // 禁用自动检测缩进（有些项目用 2 空格，防止被干扰）
}
```

---

### 6.3.7 Jupyter 配置

```json
// settings.json
{
    "jupyter.askForKernelRestart": false,
    // 当内核需要重启时，直接重启而不询问

    "jupyter.enableExtendedWindowForCellExecution": true,
    // 在 VS Code 窗口内执行代码格，而不是弹出新窗口

    "jupyter.sendSelectionToInteractiveWindow": true,
    // 选中代码段后，发送选区到 Jupyter 执行

    "jupyter.allowUnauthorizedCertificates": true
    // 允许 Jupyter 连接使用未认证证书的服务器（测试环境用）
}
```

---

## 6.4 launch.json 调试配置（完整配置项）

> 🎯 **launch.json 是什么？**：VS Code 调试的启动配置文件。它告诉 VS Code"怎么启动你的程序"、"用什么参数"、"从哪里开始跑"。类比游戏里的"游戏存档"——每个调试场景都是一个独立的 launch 配置。

### 6.4.1 打开调试配置

**步骤：**

1. 点击左侧 **运行和调试** 图标（或者按 `Ctrl + Shift + D`）
2. 点击 **创建 launch.json 文件**
3. 选择 **Python**
4. VS Code 会自动在 `.vscode/` 目录下创建 `launch.json`

```
.vscode/
└── launch.json
```

### 6.4.2 当前文件调试

#### 6.4.2.1 name、type、request、program、console 配置项

最基本的调试配置——直接跑当前打开的 `.py` 文件：

```json
// launch.json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "🐍 当前文件 (Current File)",
            "type": "debugpy",
            // debugpy 是 Python 调试器的引擎

            "request": "launch",
            // "launch" = 启动一个新进程
            // "attach" = 附加到已运行的进程

            "program": "${file}",
            // ${file} 是 VS Code 的魔法变量，代表当前打开的文件
            // 调试哪个文件，就打开哪个文件，然后按 F5

            "console": "integratedTerminal",
            // "integratedTerminal" = VS Code 内置终端
            // "externalTerminal"   = 外部系统终端窗口
            // "internalConsole"    = 调试控制台（不推荐，不支持输入）

            "cwd": "${workspaceFolder}",
            // cwd = current working directory，运行目录

            "justMyCode": true
            // true = 只在自己的代码里调试，不进标准库
            // false = 可以 step into 库文件（比如 Django 源码）
        }
    ]
}
```

> 🔮 **VS Code 魔法变量**： `${file}` = 当前文件，`${workspaceFolder}` = 当前工作区根目录，`${relativeFile}` = 相对路径。记住这些，写配置时事半功倍。

---

### 6.4.3 模块调试

#### 6.4.3.1 module 参数配置

调试一个**模块**（通过 `python -m module_name` 启动）：

```json
// launch.json
{
    "configurations": [
        {
            "name": "📦 模块调试 (Module)",
            "type": "debugpy",
            "request": "launch",

            "module": "uvicorn",
            // 用 python -m uvicorn 启动
            // 相当于命令行: python -m uvicorn main:app --reload

            "args": [
                "main:app",
                "--host", "0.0.0.0",
                "--port", "8000",
                "--reload"
            ],
            // 传给模块的命令行参数

            "console": "integratedTerminal"
        }
    ]
}
```

---

### 6.4.4 传入命令行参数与环境变量

#### 6.4.4.1 args 参数配置

通过 `args` 数组传递命令行参数（每个空格分隔的参数是一个独立字符串）：

```json
// launch.json
{
    "configurations": [
        {
            "name": "🎯 带参数的调试",
            "type": "debugpy",
            "request": "launch",

            "program": "${workspaceFolder}/main.py",

            "args": [
                "--input", "data.csv",
                "--output", "result.json",
                "--verbose",
                "--limit", "100"
            ],
            // 相当于: python main.py --input data.csv --output result.json --verbose --limit 100

            "console": "integratedTerminal"
        }
    ]
}
```

#### 6.4.4.2 env 环境变量配置

通过 `env` 传递环境变量：

```json
// launch.json
{
    "configurations": [
        {
            "name": "🌍 带环境变量的调试",
            "type": "debugpy",
            "request": "launch",

            "program": "${workspaceFolder}/main.py",

            "env": {
                "DEBUG": "true",
                "DATABASE_URL": "postgresql://localhost:5432/mydb",
                "LOG_LEVEL": "DEBUG",
                "PYTHONPATH": "${workspaceFolder}"
            },
            // 环境变量在代码里可以通过 os.environ 获取:
            // import os
            // debug_mode = os.environ.get("DEBUG", "false")

            "console": "integratedTerminal"
        }
    ]
}
```

> 🌿 **环境变量 vs 命令行参数**：环境变量适合放配置（数据库连接、API Key），命令行参数适合放运行时参数（输入文件、模式切换）。生产环境用 `.env` 文件 + `python-dotenv`，开发环境用 launch.json 的 env。

---

### 6.4.5 远程调试配置

#### 6.4.5.1 host、port 配置

调试远程服务器上正在运行的 Python 进程（需要目标机器开放端口）：

```json
// launch.json
{
    "configurations": [
        {
            "name": "🌐 远程调试 (Remote Attach)",
            "type": "debugpy",
            "request": "attach",

            "host": "192.168.1.100",
            // 远程服务器 IP 或主机名

            "port": 5678,
            // 远程开放 debugpy 端口

            "localRoot": "${workspaceFolder}",
            // 本地代码目录（映射用）

            "remoteRoot": "/home/deploy/app",
            // 远程服务器上对应的代码目录

            "justMyCode": false
            // 远程调试通常要进标准库，所以关掉 justMyCode
        }
    ]
}
```

**在远程服务器上启动 debugpy 监听：**

```bash
# 在远程服务器上运行你的脚本
python -m debugpy --listen 0.0.0.0:5678 my_script.py
# --listen 0.0.0.0:5678 表示监听所有网卡的 5678 端口
```

> 🕵️ **远程调试的用途**：当你的代码在服务器上跑跟本地不一样的时候，或者你需要调试一个长期运行的服务器进程时，远程调试是神器。注意安全：只在测试环境开放 debug 端口。

---

### 6.4.6 pytest 调试配置

#### 6.4.6.1 module 设置为 pytest

调试单个测试文件或测试函数：

```json
// launch.json
{
    "configurations": [
        {
            "name": "🧪 pytest 调试",
            "type": "debugpy",
            "request": "launch",

            "module": "pytest",
            // 用 python -m pytest 启动

            "args": [
                "tests/test_auth.py::test_login",
                "-v",
                "-s"
            ],
            // 只运行 tests/test_auth.py 里的 test_login 测试
            // -v = verbose，显示详细输出
            // -s = 捕获输出（不停用 print）

            "cwd": "${workspaceFolder}",
            "console": "integratedTerminal",

            "python": "${command:python.interpreterPath}"
            // 使用当前选中的 Python 解释器运行 pytest
        }
    ]
}
```

> 🎪 **pytest 的约定**：通常测试文件放在 `tests/` 目录下，文件名以 `test_` 开头，测试函数也以 `test_` 开头。pytest 会自动发现并运行它们。

---

### 6.4.7 Django 调试配置

#### 6.4.7.1 program 指向 manage.py

Django 项目的标准调试配置：

```json
// launch.json
{
    "configurations": [
        {
            "name": "🎸 Django 调试",
            "type": "debugpy",
            "request": "launch",

            "program": "${workspaceFolder}/manage.py",
            // Django 项目的入口文件

            "args": [
                "runserver",
                "8000",
                "--noreload"
            ],
            // runserver 启动开发服务器
            // --noreload = 禁用自动重载（方便调试）

            "django": true,
            // VS Code 会识别这是 Django 项目，启用 Django 特定调试功能

            "console": "integratedTerminal"
        }
    ]
}
```

> 🎸 **Django + VS Code = 绝配**：有了 Django 调试配置，你可以在 VS Code 里打断点，然后访问你的网站——代码停在你设的断点处，变量一览无余，比 `print('here')` 高端100倍。

---

### 6.4.8 FastAPI 调试配置

#### 6.4.8.1 module 设置为 uvicorn

FastAPI 基于 uvicorn（ASGI 服务器）运行：

```json
// launch.json
{
    "configurations": [
        {
            "name": "⚡ FastAPI 调试 (Uvicorn)",
            "type": "debugpy",
            "request": "launch",

            "module": "uvicorn",
            // python -m uvicorn

            "args": [
                "main:app",
                "--host", "0.0.0.0",
                "--port", "8000",
                "--reload"
            ],
            // main:app → main.py 里的 app 对象

            "console": "integratedTerminal",

            "justMyCode": false
            // 关闭 justMyCode，方便进 uvicorn 源码调试
        }
    ]
}
```

> ⚡ **FastAPI + debugpy**：FastAPI 是现代 Python Web 框架的代表，性能高，支持自动生成 API 文档（Swagger UI）。用上面的配置断点调试，`http://localhost:8000/docs` 还能看交互式 API 文档。

---

### 6.4.9 Flask 调试配置

#### 6.4.9.1 module 设置为 flask

Flask 调试配置：

```json
// launch.json
{
    "configurations": [
        {
            "name": "🎸 Flask 调试",
            "type": "debugpy",
            "request": "launch",

            "module": "flask",
            // python -m flask

            "env": {
                "FLASK_APP": "main.py",
                // 告诉 Flask 哪个是 app 文件

                "FLASK_ENV": "development",
                // 开启 development 模式（热重载）

                "FLASK_DEBUG": "1"
                // 开启调试模式
            },

            "args": [
                "run",
                "--host", "0.0.0.0",
                "--port", "5000",
                "--no-debugger"
            ],
            // --no-debugger 在 debugpy 模式下用
            // 注意：这里不用 --reload，因为 debugpy 接管了调试会话，
            // Flask 自带的重载器会干扰断点调试

            "console": "integratedTerminal",

            "justMyCode": false
        }
    ]
}
```

> 🍃 **Flask vs Django**：Flask 是"微框架"——核心简单，扩展自己加。Django 是"全栈框架"——自带 ORM、Admin、认证系统。如果你的项目不复杂，Flask 足够用；如果你是大型项目，Django 更省心。

---

## 6.5 断点调试全攻略

> 🕹️ **断点调试是什么感觉？**：想象你玩 GTA 游戏，突然时间暂停了——你能看到所有NPC在干嘛、速度是0、周围一切静止。这就是断点调试：你让程序在你指定的地方"暂停"，然后你可以慢慢审视它的每一个"器官"。

### 6.5.1 设置断点

#### 6.5.1.1 点击代码行号左侧红点

最简单的方法：

1. 打开你的 `.py` 文件
2. 找到你想暂停的那一行
3. **点击行号左侧的空白区域**
4. 出现一个红色的圆点——断点就设置好了！

```
     1  │ def calculate_sum(numbers):
     2  │     total = 0
     3  │     for num in numbers:
     4  │ ●    total += num
     5  │     return total
     ← 点击这里
```

#### 6.5.1.2 快捷键 F9

选中一行代码（光标在该行），按 `F9`，断点就出现了。再按一次 `F9`，断点消失。

> 💡 **熟练使用 F9**：这是调试的最高频操作。设断点 → F5 跑起来 → F9 切换断点。记住 F9，调bug的效率直接翻倍。

#### 6.5.1.3 条件断点配置

普通断点 = 代码执行到这里就停。

**条件断点** = 只有满足特定条件才停。

**设置方法：**

1. 右键断点（红色的那个点）
2. 选择 **Edit Condition**
3. 输入条件表达式

```
条件: count > 10
含义: 只有当 count 变量大于 10 时才停
```

或者用 **表达式断点**（Python 支持）——这行代码被执行一次就停一次：

```
条件: i == 5
含义: 当循环到第6次时才停（i=5 时，0-indexed）
```

---

### 6.5.2 条件断点

#### 6.5.2.1 条件表达式设置

条件断点的表达式可以是任何 Python 表达式：

| 条件表达式 | 含义 |
|-----------|------|
| `count > 100` | count 大于 100 时停止 |
| `user is not None` | user 不是 None 时停止 |
| `len(items) == 0` | items 为空时停止 |
| `isinstance(x, int)` | x 是整数时停止 |
| `'error' in message` | message 包含 'error' 时停止 |

#### 6.5.2.2 日志断点配置

**日志断点**（Logpoints）——不断代码，而是让程序执行到这里时**打印一条日志**。

**设置方法：**

1. 右键断点
2. 选择 **Logpoint**
3. 输入日志信息

```
日志断点: `count = {count}, total = {total}`
含义: 每次循环到这里，都在 Debug Console 打印这两个变量的值
```

> 📝 **日志断点 vs print 大法**：以前你要在循环里加 `print(f"count={count}")`，然后满屏输出，眼睛瞎了。日志断点只在 Debug Console 里输出，不污染正常输出，而且不需要改代码！

---

### 6.5.3 变量监视（Watch）

#### 6.5.3.1 Add Expression 添加监视表达式

在调试面板的 **WATCH** 窗口（左侧）：

1. 点击 **+** 号
2. 输入你要监视的表达式

#### 6.5.3.2 输入要监视的变量名或表达式

```
count
→ 监视变量 count 的值

total / len(numbers)
→ 监视计算结果

data['user']['name']
→ 字典嵌套访问（Watch 也能用！）

[ x for x in items if x > 0 ]
→ 列表推导式——实时看过滤结果
```

> 👁️ **Watch 的精髓**：不是所有变量都要加 Watch，只加那些你"担心它出问题"的。比如循环里 `total` 的累加过程诡异，就 Watch 它；或者某个函数返回值不对，就 Watch 返回值。

---

### 6.5.4 调用堆栈（Call Stack）分析

#### 6.5.4.1 CALL STACK 面板

在调试模式下，左侧面板会有一个 **CALL STACK** 区域：

```
▼ Call Stack
  ▶ Thread 0 (Running)
    ▶ main.py:15 in calculate()
      main.py:8 in <module>()
```

它展示的是：**代码执行到当前位置的完整调用链**。

`calculate()` 是 `main.py` 第15行调用的，而 `main.py` 第8行又调用了 `calculate()`——这就是调用堆栈。

#### 6.5.4.2 点击任意帧跳转到对应代码

**点击堆栈里的任意一帧**（比如 `main.py:8 in <module>`），VS Code 会**跳转到那个文件的对应行**。

> 🪜 **调用堆栈有什么用**：当你在一个被很多地方调用的函数里设了断点，但不确定是哪个调用方触发的——看 Call Stack 就知道了。它告诉你"是谁把你叫到这里的"。

---

### 6.5.5 debug console 实时表达式计算

#### 6.5.5.1 REPL view → debug console

VS Code 调试时，底部会打开 **DEBUG CONSOLE** 面板：

```
Variables                          Watches
├─ total: 0                        ├─ count
├─ numbers: [1, 2, 3]             └─ len(numbers)
│
CALL STACK
│
───────────────────────────────
DEBUG CONSOLE                    ← 在这里输入表达式
> _
```

#### 6.5.5.2 直接输入表达式即时计算

在 DEBUG CONSOLE 里，**可以直接输入 Python 表达式**，VS Code 会用当前的变量上下文计算结果：

```
> total
0

> total + 100
100

> [x * 2 for x in numbers]
[2, 4, 6]

> import os; os.getenv('PATH', '')
'C:\\Python311\\Scripts;...'
```

> 🎮 **Debug Console = Python REPL**：它就是带变量上下文（当前作用域里的变量都能用）的 Python 交互式解释器。相当于你在断点处暂停，然后有一个带内存快照的 Python Shell 供你探索。

---

### 6.5.6 异常断点

#### 6.5.6.1 Raised Exceptions / Uncaught Exceptions 配置

VS Code 可以在**任何异常发生时**自动暂停，不管你有没有在那行代码上设断点。

**打开异常断点：**

1. 左侧 **BREAKPOINTS** 面板
2. 勾选以下选项：
   - ☑️ **Raised Exceptions**（抛出的异常）
   - ☑️ **Uncaught Exceptions**（未捕获的异常）

```
BREAKPOINTS 面板:
☑️ Raised Exceptions (Always Break)
☑️ Uncaught Exceptions (Always Break)
☐ Handled Exceptions
```

- **Raised Exceptions**：任何 `raise` 语句（包括你主动抛出的）都会停
- **Uncaught Exceptions**：只有没人处理的异常才停（推荐！）

> ⚠️ **选哪个**：如果你的代码有 `try/except` 包裹，不想在每个被捕获的异常处都停，选 **Uncaught Exceptions**。这能帮你找到"意外漏网"的 bug。

#### 6.5.6.2 Handled Exceptions 配置

- **Handled Exceptions**：即使被 `try/except` 捕获了也会停（开这个会导致满屏停，不推荐日常用）

> 🐛 **异常断点 vs 普通断点**：普通断点是你主动设的"停车点"，异常断点是系统级别的"事故录像"——任何异常发生你就停车，然后看 Call Stack 和变量，快速定位 crash 原因。

---

## 6.6 高级调试技巧

### 6.6.1 多线程调试

#### 6.6.1.1 THREAD 面板查看所有线程

当你的程序创建了多个线程时，调试面板会出现 **THREADS** 面板：

```
▼ Threads
  Thread 1 (Current) ← 标记当前在哪个线程
  Thread 2
  Thread 3
  MainThread
```

#### 6.6.1.2 线程列表切换

点击不同线程，调试器会跳转到那个线程的当前执行位置。

> 🧵 **多线程调试的痛点**：线程切换是随机的，bug 可能只在特定线程、特定时机才出现。用 `threading.current_thread().name` 打印线程名，或者在 Watch 里添加 `"当前线程: " + threading.current_thread().name`，配合断点，揪出线程bug。

---

### 6.6.2 异步调试（asyncio）

#### 6.6.2.1 asyncio 代码调试与普通代码相同

asyncio 异步代码的调试方式**跟普通代码完全一样**——设断点 → F5 → 停。

```python
import asyncio

async def fetch_data():
    result = await some_async_api()  # ← 断点设在这里
    return result

async def main():
    data = await fetch_data()        # ← 断点设在这里
    print(data)

asyncio.run(main())
```

#### 6.6.2.2 协程任务在 Call Stack 中显示

asyncio 的协程在 Call Stack 中会显示为：

```
Call Stack:
  ▶ asyncio.run() in <module>
    ▶ main() in <module>
      ▶ fetch_data() in <module>
        ▶ some_async_api() ← 协程调用
```

> ⚡ **async/await 调试注意点**：在 `await` 处停下时，Call Stack 会显示整个调用链。你也可以 Watch `asyncio.current_task()` 来查看当前协程对象。

---

### 6.6.3 外部控制台窗口调试

#### 6.6.3.1 console 设置为 externalTerminal

有些场景下（比如需要交互式输入），内置终端不够用，需要弹出一个独立窗口：

```json
// launch.json
{
    "configurations": [
        {
            "name": "🖥️ 外部终端调试",
            "type": "debugpy",
            "request": "launch",
            "program": "${workspaceFolder}/input_demo.py",

            "console": "externalTerminal",
            // 改为 externalTerminal，会弹出系统终端窗口

            "externalConsole": true
            // Windows 专用：使用 cmd/PowerShell 窗口
        }
    ]
}
```

> 🖥️ **什么时候用外部终端**：当你的程序需要 `input()` 交互输入，或者需要实时看到完整终端输出（颜色、清屏等）时，外部终端更方便。

---

### 6.6.4 调试中修改变量值

#### 6.6.4.1 VARIABLES 面板右键变量 → Set Value

在调试过程中，你可以**直接修改变量的值**，不用重启程序：

1. 在 **VARIABLES** 面板找到你想改的变量
2. **右键** → **Set Value**
3. 输入新值，回车

```
原本:
count = 5
→ Set Value → 改为 100
→ 程序继续运行，使用 count = 100
```

> 🔧 **这个功能的用途**：测试边界条件——比如你想测试"当 count=0 时程序会不会崩溃"，不用重启程序改代码，直接在调试时把 count 改成 0，continue 看结果。

---

### 6.6.5 跳过（Step Over）某些代码

断点停在某行时，你有以下几种"走法"：

#### 6.6.5.1 Step Over：F10

**逐过程**：执行当前行，**不进入**函数调用。如果当前行调用了一个函数，直接执行完整个函数，停在下一行。

```
  1 │ def triple(x):
  2 │     return x * 3
  3 │
  4 │ a = 10
  5 │ b = triple(a)  ← 断点在这里，F10 会直接跳到第6行
  6 │ c = b + 1
```

#### 6.6.5.2 Step Into：F11

**逐语句**：执行当前行，如果当前行调用了函数，**进入**函数内部，停在函数的第一行。

```
  1 │ def triple(x):
  2 │     return x * 3      ← F11 会跳到这里
  3 │
  4 │ a = 10
  5 │ b = triple(a)  ← F11 会进入 triple() 函数
  6 │ c = b + 1
```

#### 6.6.5.3 Step Out：Shift+F11

**跳出**：如果当前在函数内部，按 Shift+F11 会**执行完整个函数**，停在调用该函数的下一行。

```
  1 │ def triple(x):
  2 │     return x * 3      ← 光标在这里
  3 │                         ← Shift+F11 跳到这里
  4 │ a = 10
  5 │ b = triple(a)
  6 │ c = b + 1
```

> 🎮 **三剑客的使用口诀**：
> - F10（Step Over）：这行代码不感兴趣，直接略过
> - F11（Step Into）：这行代码调用的函数有鬼，我要进去看看
> - Shift+F11（Step Out）：函数看完了，不想继续在里面逛，出来

---

## 本章小结

这一章我们把 VS Code 打造成了 Python 开发者的"豪华游戏房"，涵盖了以下核心技能：

### 🎯 基础设施
- VS Code 下载安装，设置中文语言包、主题、字体、字号
- 打造舒适的编程环境

### 🔌 必装插件全家桶
- **Python + Pylance**：智能提示 + 类型检查的黄金组合
- **Ruff**：Lint + Format 二合一，极速选手
- **Black Formatter**：固执己见的代码格式化
- **autoDocstring**：自动生成 docstring 模板
- **Python Debugger**：图形化断点调试
- **Jupyter**：Notebook 支持
- **Python Environment Manager**：多环境一键切换
- **GitHub Copilot**：AI 副驾驶
- **Error Lens**：错误高亮
- **Thunder Client / REST Client**：API 测试
- **GitLens / Git History**：Git 可视化
- **Remote - SSH**：远程开发

### ⚙️ 配置艺术
- `settings.json` 核心配置：解释器路径、格式化、lint、代码风格
- `launch.json` 调试配置：覆盖所有常见场景（普通脚本、模块、pytest、Django、FastAPI、Flask、远程调试）

### 🕹️ 调试大师
- 断点、条件断点、日志断点
- 变量监视、调用堆栈分析
- Debug Console 实时计算
- 异常断点
- 多线程、asyncio 调试
- 修改变量值、Step Over/Into/Out

> 🚀 **学完这章，你已经是一个"VS Code + Python"的全栈工程师了。** 编辑器、插件、配置、调试——这些工具将伴随你整个 Python 开发生涯。掌握它们，让工具为你服务，而不是被工具折腾。

---

*下一章我们将学习虚拟环境和包管理，继续打造你的 Python 兵器库！*
