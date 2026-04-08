+++
title = "第8章 其他编辑器"
weight = 80
date = "2026-04-08T13:22:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# Chapter 8: 告别 VS Code？这些编辑器让你装 X 于无形

> 上一章我们学会了在 VS Code 里写 Python，感觉人生已经到达了巅峰。但江湖之大，岂能只有一柄利器？今天咱们就来聊聊那些**让旁门左道肃然起敬**的编辑器们——它们有的靠 AI 加持，有的靠极客血统，有的靠科学气质，总之各怀绝技。

**TL;DR（太长不看版）：**
- Cursor = VS Code 的 AI 升级版，让你写代码像有了一个24小时不睡觉的老司机
- Sublime Text = 编辑器界的保时捷，轻快又骚气
- Vim/Neovim = 键盘侠的终极奥义，一旦学会欲罢不能
- Jupyter = 数据科学家的浪漫，代码和散文交织的美感
- Google Colab = 穷人的福利，免费 GPU/TPU 白嫖指南

---

## 8.1 Cursor（AI 原生编辑器）—— VS Code 失散多年的亲兄弟

> 如果说 VS Code 是 iPhone，那 Cursor 就是 iPhone Pro Max Ultra Plus AI Edition。

Cursor 是什么？它本质上是基于 VS Code 魔改的编辑器，**内置了 AI 基因**。换句话说，你可以在写代码的时候让 AI 帮你补全、解释、甚至直接帮你写一整个函数。想象一下：你键盘还没敲热，AI 已经把代码喂到你嘴边了——这就是 Cursor 的日常。

### 8.1.1 下载安装

Cursor 的安装简单到连你家的猫都能完成（如果它会用鼠标的话）。

1. 打开浏览器，访问 [https://cursor.com](https://cursor.com)
2. 点击那个醒目的 **Download** 按钮
3. 下载对应系统的安装包（Windows/macOS/Linux 全家桶桶桶桶）
4. 双击安装，一路 Next/YES/我同意/Install

```text
安装完成后的界面
┌──────────────────────────────────────────────────────────┐
│  Cursor                                                   │
│                                                          │
│   __                __            __  __                 │
│  /\ \             /\ \__        /\ \/\ \                │
│  \ \ \____  __  __\ \ ,_\     __\ \ \_\ \                │
│   \ \ '__`\/\ \/\ \\ \ \/   /'__`\ \ ,__/               │
│    \ \ \_\ \ \_\ \ \\ \ \_ /\  __/\ \ \_/               │
│     \ \__,_/\/`____ \\ \__\\ \____\\ \__/               │
│      \/__/  `/___/> \\ \__/\\/____/ \/__/                │
│                 /\___/ \ \__/                           │
│                 \/__/  \ \__/                           │
│                          \ \__/                         │
│                           \/__/                         │
│                                                          │
│           "Write code at the speed of thought"           │
│                    —— Cursor 的 Slogan                   │
└──────────────────────────────────────────────────────────┘
```

> **温馨提示：** Cursor 有免费版，但功能受限。如果你想解锁全部 AI 超能力，需要订阅 Pro 版本。当然，免费的已经足够让你在同事面前表演"盲打"了。

### 8.1.2 Python 环境配置

#### 8.1.2.1 Python: Select Interpreter

Cursor 和 VS Code 一样，依赖 `Python: Select Interpreter` 命令来找到你系统里的 Python 解释器。

**操作步骤：**

1. 按下 `Ctrl + Shift + P`（Windows/Linux）或 `Cmd + Shift + P`（macOS）打开命令面板
2. 输入 `Python: Select Interpreter`，选中它
3. 弹出列表，选择你的 Python 解释器路径

```text
命令面板中的效果
┌──────────────────────────────────────────────────────────┐
│ > Python: Select Interpreter                    🔍      │
├──────────────────────────────────────────────────────────┤
│   ✅ Python 3.12.3 64-bit ('venv': Virtual)             │
│     C:\Users\longx\AppData\Local\Programs\Python\       │
│     Python312\python.exe                                 │
│                                                          │
│   🐍 Python 3.11.9 64-bit                                │
│     C:\Python311\python.exe                              │
│                                                          │
│   ⚙️ Enter interpreter path...                          │
└──────────────────────────────────────────────────────────┘
```

> **小贴士：** 如果你看到列表里有 `('venv': Virtual)` 标注的选项，优先选这个！这是 Cursor 在告诉你"这是一个虚拟环境"，隔离性好，不污染全局。

#### 8.1.2.2 选择虚拟环境

虚拟环境（Virtual Environment）是什么？想象一下：你有一个专门给 Python 项目用的"独立房间"，每个房间里的包都是独立的，不会打架。

在 Cursor 里选择虚拟环境有两种方式：

**方式一：自动检测**

Cursor 很聪明，它会自动扫描你的项目文件夹，如果发现 `.venv` 或 `venv` 目录，会自动弹窗问你"要不要用这个？"

**方式二：手动指定**

```bash
# 先创建一个虚拟环境（如果你还没有的话）
python -m venv .venv

# 激活它
# Windows:
.venv\Scripts\activate

# macOS/Linux:
source .venv/bin/activate
```

激活后，Cursor 会自动识别到这个虚拟环境，在 `Python: Select Interpreter` 里选中它即可。

```python
# 验证一下当前使用的 Python 路径
import sys
print(sys.executable)
# 输出类似：C:\Users\longx\project\.venv\Scripts\python.exe
```

### 8.1.3 AI 代码补全

> 这是 Cursor 的核心卖点！它不仅仅是个编辑器，它是一个**会读心术的副驾驶**。

#### 8.1.3.1 Tab 键接受补全

Cursor 的 AI 会在你打字的时候**预测**你接下来要写什么，然后用灰色字体显示建议。按下 `Tab` 键就能接受这个建议。

```python
# 你正在写一个计算圆面积的函数
def calculate_circle_area(radius):
    # AI 预测你接下来要写：
    return 3.14159 * radius ** 2  # ← 这行是 AI 建议，灰色显示
```

此时你只需按下 `Tab` 键，整行代码就被"粘贴"进去了。**快到你的手指还没反应过来，代码已经写完了。**

> **冷笑话时间：** 程序员老王用了 Cursor 后，一天写的代码比之前一个月还多。他媳妇问他："你是不是被外星人绑架了？"他说："没有，是我的 IDE 被外星人升级了。"

#### 8.1.3.2 Cmd/Ctrl + K 手动触发补全

有时候 AI 的自动补全不够精准，或者你遇到一个复杂的函数不知道咋写。这时候你可以**手动召唤 AI**。

- **Windows/Linux：** `Ctrl + K`
- **macOS：** `Cmd + K`

**使用场景：**

```python
# 你想写一个快速排序，但懒得查文档
# 选中要写的代码位置，按下 Ctrl/Cmd + K，然后输入：
# "写一个快速排序算法，用中文注释"

# AI 生成：
def quick_sort(arr):
    """
    快速排序算法
    原理：选择基准值，将数组分为两部分，递归排序
    时间复杂度：平均 O(n log n)，最坏 O(n²)
    """
    if len(arr) <= 1:
        return arr
    
    # 选择中间元素作为基准
    pivot = arr[len(arr) // 2]
    
    # 分区操作
    left = [x for x in arr if x < pivot]      # 小于基准的放左边
    middle = [x for x in arr if x == pivot]   # 等于基准的放中间
    right = [x for x in arr if x > pivot]     # 大于基准的放右边
    
    # 递归排序并合并
    return quick_sort(left) + middle + quick_sort(right)


# 测试一下
numbers = [64, 34, 25, 12, 22, 11, 90]
print(quick_sort(numbers))
# 输出：[11, 12, 22, 25, 34, 64, 90]
```

> **装 X 指南：** 在同事面前，你可以淡定地说："哦，这个快速排序啊，我让 AI 写的，2秒钟的事。"然后优雅地端起咖啡。

### 8.1.4 Composer（多文件 AI 生成）

> 如果说普通补全是"单点爆破"，那 Composer 就是"地毯式轰炸"。

Composer 是 Cursor 的杀手级功能——你可以让它**一次性生成多个文件**，甚至是整个项目结构！

#### 8.1.4.1 Cmd/Ctrl + I 打开 Composer

- **Windows/Linux：** `Ctrl + I`
- **macOS：** `Cmd + I`

**使用姿势：**

1. 按下 `Ctrl/Cmd + I` 打开 Composer 对话框
2. 用自然语言描述你想要的功能，比如："创建一个 Flask Web 应用，包含用户登录、注册功能，使用 SQLite 数据库"
3. AI 会生成多个文件：`app.py`、`models.py`、`templates/login.html` 等
4. 你可以逐个查看、修改、接受

```text
Composer 生成的文件列表
┌──────────────────────────────────────────────────────────┐
│ 📁 my_flask_app/                                         │
│   ├── 📄 app.py              # 主应用文件               │
│   ├── 📄 models.py           # 数据库模型                │
│   ├── 📄 config.py           # 配置文件                  │
│   ├── 📁 templates/                                      │
│   │   ├── 📄 base.html       # 基础模板                 │
│   │   ├── 📄 login.html      # 登录页面                 │
│   │   └── 📄 register.html  # 注册页面                 │
│   └── 📁 static/                                          │
│       ├── 📁 css/                                         │
│       └── 📁 js/                                          │
└──────────────────────────────────────────────────────────┘
```

> **警告：** AI 生成代码虽然快，但别忘了**审查和测试**！AI 写的代码可能有意想不到的 bug，毕竟它不是真正的程序员（虽然它装得很像）。

---

## 8.2 Sublime Text——编辑器界的法拉利

> 如果说 VS Code 是家用轿车，那 Sublime Text 就是跑车——启动快、操控精准、还能漂移。

Sublime Text 是由 Jon Skinner 开发的一款轻量级代码编辑器，以**速度极快、界面骚气**著称。它的 Slogan 是"一个用文本编辑器该有的方式工作的代码编辑器"。翻译成人话就是："老子很快，快到让你怀疑人生。"

### 8.2.1 安装 Python 相关插件

Sublime Text 本身只是个空壳，需要安装插件才能让它支持 Python 开发。这就像买了法拉利还得去加油一样。

#### 8.2.1.1 安装 Package Control

Package Control 是 Sublime Text 的**插件管理器**，相当于 VS Code 的 Marketplace。不安装它，你就没法装其他插件。

**安装步骤：**

1. 打开 Sublime Text
2. 按下 `` Ctrl + ` ``（反引号，在 Tab 键上方）打开控制台
3. 粘贴以下代码（来自官方）：

```python
import urllib.request, sys; exec(urllib.request.urlopen(sys.argv[1]).read())
```

> ⚠️ **安全提醒：** 上述代码会从网络下载并执行代码，存在一定安全风险。保守的做法是直接访问 [packagecontrol.io/installation](https://packagecontrol.io/installation) 复制官方提供的完整安装代码。

等等，这行代码看着有点吓人。官方推荐的方式是访问 https://packagecontrol.io/installation 复制正确的代码。但更简单的方法是：

1. 打开 https://packagecontrol.io/installation
2. 找到 **Sublime Text 3** 的代码
3. 复制粘贴到控制台，按回车

安装成功后，重启 Sublime Text，然后按 `Ctrl + Shift + P` 打开命令面板，输入 `Package Control`，如果能看到一堆选项就说明安装成功了。

```text
命令面板中的 Package Control 选项
┌──────────────────────────────────────────────────────────┐
│ Package Control: Install Package          🔍             │
│ Package Control: Add Repository                          │
│ Package Control: Remove Package                          │
│ Package Control: List Packages                           │
│ Package Control: Upgrade Package                         │
└──────────────────────────────────────────────────────────┘
```

> **冷知识：** Package Control 的图标是一个"正在打开的礼物盒"，寓意是"里面装满了惊喜（插件）"。

#### 8.2.1.2 安装 SublimeLinter + Flake8

**SublimeLinter** 是一个代码检查框架，相当于 Python 的"实时纠错老师"。**Flake8** 是 Python 的代码风格检查工具，会告诉你哪里没按 PEP 8 规范写。

**安装步骤：**

1. `Ctrl + Shift + P` → 输入 `Package Control: Install Package` → 按回车
2. 等待加载完成（看到左下角转圈圈别慌）
3. 输入 `SublimeLinter`，选择它
4. 等待安装完成
5. 重复第 1-3 步，输入 `Flake8`，选择 **SublimeLinter-flake8**

```bash
# 如果你用 pip 安装了 flake8，SublimeLinter 会自动找到它
pip install flake8
```

> **什么是 PEP 8？** PEP 8 是 Python 的代码风格指南，规定了缩进、命名、空行等规范。简单说就是"怎么让 Python 代码看起来更顺眼"的约定。Flake8 就是检查你有没有遵守这个约定的工具。

**验证安装：**

写一段不太规范的 Python 代码试试：

```python
# 这段代码风格有点问题
x=1;y=2;z=x+y
def  badFunc(  ):
    return'no spaces'
```

保存后，Sublime Text 应该在有问题的代码行旁边显示一个小图标（红圈或黄线），提示你这里不对劲。

#### 8.2.1.3 安装 SublimeREPL（交互式编程）

**SublimeREPL** 让你在 Sublime Text 里直接运行 Python 代码，相当于内置了一个交互式解释器。

**安装步骤：**

1. `Ctrl + Shift + P` → `Package Control: Install Package`
2. 输入 `SublimeREPL`，选择它

```text
安装完成后，你会发现在 Tools 菜单下多了个 SublimeREPL 选项
┌──────────────────────────────────────────────────────────┐
│ Tools                                                     │
│   └─ SublimeREPL                                          │
│       ├─ Python                                           │
│       │   ├─ Python                                       │
│       │   ├─ Python - RUN current file                    │
│       │   └─ Python - IPython                             │
│       └─ Eval in Repl                                      │
└──────────────────────────────────────────────────────────┘
```

### 8.2.2 SublimeREPL 使用

SublimeREPL 让你可以在编辑器里直接和 Python 对话，就像 Jupyter 那样。

**方法一：运行当前文件**

1. 打开一个 `.py` 文件
2. `Tools` → `SublimeREPL` → `Python` → `Python - RUN current file`
3. 输出会显示在新的标签页里

**方法二：打开交互式解释器**

`Tools` → `SublimeREPL` → `Python` → `Python`

```python
# 在 SublimeREPL 的交互窗口里试试
>>> name = "小明"
>>> print(f"你好，{name}！欢迎来到 SublimeREPL 的世界！")
# 输出：你好，小明！欢迎来到 SublimeREPL 的世界！
#
>>> 2 ** 10  # 2的10次方
# 输出：1024
```

**方法三：选中代码片段执行**

1. 选中一段代码
2. 右键 → `SublimeREPL` → `Eval in Repl`
3. 这段代码就会被发送到交互式窗口执行

```python
# 在编辑器里选中这段代码，然后 Eval in Repl
for i in range(5):
    print(f"🎉 第 {i} 次循环完成！")

# 输出：
# 🎉 第 0 次循环完成！
# 🎉 第 1 次循环完成！
# 🎉 第 2 次循环完成！
# 🎉 第 3 次循环完成！
# 🎉 第 4 次循环完成！
```

> **搞笑场景：** 某程序员在 SublimeREPL 里输入 `print("Hello, World!")`，然后对旁边的同事说："看，我用 Sublime 写的！"同事凑过来看："就这？"程序员曰："这叫简约，简约而不简单懂不懂？"

### 8.2.3 SublimeLinter + Flake8 配置

光安装还不够，我们还需要配置一下，让 SublimeLinter 按我们想要的方式工作。

**配置方法：**

1. `Preferences` → `Package Settings` → `SublimeLinter` → `Settings`
2. 打开的 JSON 文件里可以配置各种选项

```json
{
    // 用户配置文件示例
    "user": {
        // 代码风格检查规则
        "linters": {
            "flake8": {
                // @ 表示项目根目录
                "args": [
                    "--max-line-length=120",  // 最大行长120字符（默认79太短了）
                    "--ignore=E501,W503"      // 忽略某些不重要的警告
                ]
            }
        },
        // 实时检查模式：save 表示保存时检查，load_save 表示加载和保存时都检查
        "lint_mode": "load_save",
        // 显示风格：在编辑区域 gutter（行号栏）显示图标
        "mark_style": "outline"
    }
}
```

**常用 Flake8 错误代码解释：**

| 代码 | 含义 | 例子 |
|------|------|------|
| E501 | 行太长 | 一行写了 200 个字符 |
| E302 | 函数定义前需要两个空行 | `def foo()` 直接跟了 `def bar()` |
| E231 | 缺少空格 | `x=[1,2,3]` 而不是 `x = [1, 2, 3]` |
| W503 | 行后有空格 | 行尾多了空格 |

```python
# 故意写一段有很多 Flake8 问题的代码来测试

def  bad_function( a,b,c ):              # E501(行太长), E231(缺空格), E302(需空行)
    x=1                                   # E231
    y=2
    result=x+y                            # E231
    return result

# 下面是风格好的版本
def good_function(a, b, c):
    """这是一个风格规范的函数"""
    x = 1
    y = 2
    result = x + y
    return result
```

---

## 8.3 Vim / Neovim——键盘侠的终极奥义

> 江湖上流传着一个传说：学会了 Vim，你的手指就像被赋予了超能力，**不用鼠标就能在代码的海洋里自由冲浪**。当然，代价是你得先经历一周的" Vim 地狱"——每次你想保存文件都会不小心把编辑器关掉。

Vim 是 Unix 系统自带的一款历史悠久的编辑器，以**模式切换**和**快捷键组合**著称。Neovim 是 Vim 的"现代化重制版"，修复了 Vim 的一些历史包袱，增加了插件系统的可扩展性。

> **什么是 LSP？** LSP = Language Server Protocol（语言服务器协议）。它是一种标准化协议，让编辑器可以和"语言服务器"通信，获取代码补全、跳转、错误提示等功能。相当于编辑器和 Python 之间的翻译官。

### 8.3.1 nvim-lspconfig 配置 Python LSP

#### 8.3.1.1 安装 python-lsp-server

python-lsp-server 是 Python 的 Language Server，有了它，Neovim 才能"理解"你的 Python 代码。

```bash
# 用 pip 安装 python-lsp-server
pip install python-lsp-server

# 或者如果你用 uv（更快的包管理器）
uv pip install python-lsp-server

# 可选：安装一些额外的功能（Windows PowerShell 中需要加引号）
pip install "python-lsp-server[all]"
```

> **什么是 pyright？** pyright 是微软开发的 Python 类型检查器，实现了 LSP协议。python-lsp-server 和 pyright 是**两个不同的 LSP 实现**，互不包含。python-lsp-server 相当于"官方默认版"，pyright 相当于"微软增强版"。通过 Mason.nvim 可以方便地安装其中任意一个（甚至两个都装）。

#### 8.3.1.2 配置 lspconfig.pyright

**lspconfig** 是 Neovim 的插件，用来管理各种语言服务器的配置。

**1. 安装插件管理器（如果你还没有的话）**

推荐使用 **lazy.nvim** 或 **packer.nvim**。假设你用 lazy.nvim：

```lua
-- ~/.config/nvim/lua/plugins/lsp.lua
-- 插件配置示例
return {
    {
        -- LSP 配置插件
        'neovim/nvim-lspconfig',
        dependencies = {
            -- 自动安装 LSP 服务器的插件
            'williamboman/mason.nvim',
            'williamboman/mason-lspconfig.nvim',
        },
        config = function()
            local lspconfig = require('lspconfig')
            local mason_lspconfig = require('mason-lspconfig')

            -- 设置 LSP 日志（调试用）
            -- vim.lsp.set_log_level("debug")

            -- Mason 自动安装配置
            mason_lspconfig.setup({
                -- 自动安装列表
                ensure_installed = {
                    'pyright',  -- Python LSP 服务器
                },
            })

            -- Pyright LSP 配置
            lspconfig.pyright.setup({
                -- 设置 Python 解释器路径
                settings = {
                    python = {
                        pythonPath = vim.fn.exepath('python') or 'python',
                        analysis = {
                            -- 类型检查级别
                            -- off: 关闭
                            -- basic: 基本
                            -- full: 完整（最严格）
                            typeCheckingMode = "basic",
                            -- 诊断选项
                            autoSearchPaths = true,
                            useLibraryCodeForTypes = true,
                            -- 指定虚拟环境路径
                            venvPath = vim.fn.getcwd() .. "/.venv",
                        },
                    },
                },
                -- 当 LSP 连接时执行的回调
                on_attach = function(client, bufnr)
                    -- 绑定 LSP 相关快捷键
                    local opts = { noremap = true, silent = true, buffer = bufnr }

                    -- 跳转到定义
                    vim.keymap.set('n', 'gd', vim.lsp.buf.definition, opts)
                    -- 跳转到声明
                    vim.keymap.set('n', 'gD', vim.lsp.buf.declaration, opts)
                    -- 显示悬停文档
                    vim.keymap.set('n', 'K', vim.lsp.buf.hover, opts)
                    -- 列出所有引用
                    vim.keymap.set('n', 'gr', vim.lsp.buf.references, opts)
                    -- 重命名
                    vim.keymap.set('n', '<leader>rn', vim.lsp.buf.rename, opts)
                    -- 代码格式化
                    vim.keymap.set('n', '<leader>f', function()
                        vim.lsp.buf.format({ async = true })
                    end, opts)
                end,
            })
        end,
    }
}
```

**配置完成后，重启 Neovim，按 `:Mason` 查看已安装的 LSP 服务器。**

```text
Mason 面板效果
┌──────────────────────────────────────────────────────────┐
│  Mason - LSP/DAP/Linter Installer                        │
├──────────────────────────────────────────────────────────┤
│  ✓ pyright     [Installed]  Python LSP Server            │
│  □ ruff_lsp    [Not Installed] Ruff LSP Server           │
│  □ debugpy     [Not Installed] Python Debugger           │
└──────────────────────────────────────────────────────────┘
```

### 8.3.2 nvim-dap 调试配置

> **什么是 DAP？** DAP = Debug Adapter Protocol（调试适配器协议）。和 LSP 类似，DAP 是编辑器和调试器之间的"翻译官"。nvim-dap 是 Neovim 的调试插件，让你可以在 Neovim 里单步调试 Python 代码。

#### 8.3.2.1 安装 debugpy

debugpy 是 Python 的调试服务器，实现了 DAP 协议。

```bash
# 安装 debugpy
pip install debugpy
```

#### 8.3.2.2 Dap 配置示例

```lua
-- ~/.config/nvim/lua/plugins/dap.lua
return {
    {
        'mfussenegger/nvim-dap',
        dependencies = {
            -- DAP UI 插件
            'rcarriga/nvim-dap-ui',
            -- DAP 虚拟文本（显示变量值）
            'theHamsta/nvim-dap-virtual-text',
        },
        config = function()
            local dap = require('dap')
            local dapui = require('dapui')

            -- DAP UI 配置
            dapui.setup({
                -- 自动打开 UI
                auto_open = true,
                -- 侧边栏宽度
                sidebar_size = 40,
            })

            -- Python 调试配置
            dap.configurations.python = {
                {
                    -- 类型
                    type = 'python',
                    -- 请求类型
                    request = 'launch',
                    -- 程序入口
                    program = '${file}',
                    -- 工作目录
                    cwd = '${workspaceFolder}',
                    -- 控制台模式
                    console = 'integratedTerminal',
                    -- Python 解释器
                    pythonPath = function()
                        -- 优先使用 .venv 中的 python
                        local venv = vim.fn.getcwd() .. '/.venv/bin/python'
                        if vim.fn.executable(venv) == 1 then
                            return venv
                        end
                        -- 否则用系统 python
                        return vim.fn.exepath('python') or 'python'
                    end,
                },
            }

            -- 快捷键映射
            vim.keymap.set('n', '<F5>', dap.continue, { desc = '开始/继续调试' })
            vim.keymap.set('n', '<F10>', dap.step_over, { desc = '单步跳过' })
            vim.keymap.set('n', '<F11>', dap.step_into, { desc = '单步进入' })
            vim.keymap.set('n', '<F12>', dap.step_out, { desc = '单步退出' })
            vim.keymap.set('n', '<leader>b', dap.toggle_breakpoint, { desc = '切换断点' })
            vim.keymap.set('n', '<leader>B', function()
                dap.set_breakpoint(vim.fn.input('Breakpoint condition: '))
            end, { desc = '设置条件断点' })
            vim.keymap.set('n', '<leader>dt', dapui.toggle, { desc = '切换 DAP UI' })
        end,
    }
}
```

**使用示例：**

```python
# demo.py - 调试示例
def fibonacci(n):
    """计算斐波那契数列第 n 项"""
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


def main():
    result = fibonacci(10)
    print(f"斐波那契第10项是: {result}")

    numbers = [fibonacci(i) for i in range(10)]
    print(f"前10项: {numbers}")


if __name__ == "__main__":
    main()
```

```text
# 调试流程（在 Neovim 中）
1. 打开 demo.py
2. 在第 6 行按 <leader>b 添加断点（断点处会有一个红点）
3. 按 F5 开始调试
4. 程序会停在断点处，屏幕会弹出 DAP UI，显示：
   - 当前变量值（n = 10）
   - 调用栈
   - 调试工具栏
5. 按 F10 单步执行，观察 result 的变化
6. 按 F5 继续执行到结束
```

> **Vim 小技巧：** 在普通模式下按 `/` 可以搜索，`:wq` 是保存退出，`i` 是进入插入模式，`Esc` 是退出插入模式。如果你一不小心进入了 Vim，不知道怎么退出——记住：**按 Esc 几次，然后输入 `:q!` 回车，就能强制退出（不保存）。** 这是每个 Vim 用户的"救命口诀"。

### 8.3.3 python-mode 插件

python-mode 是一个**古老的** Neovim 插件，集成了 Python 开发所需的各种功能：补全、语法检查、跳转、格式化等。它的优点是"一键安装，全家桶"，缺点是配置复杂、容易和 LSP 冲突。

> **推荐：** 如果你已经配置了 LSP（上面 8.3.1 的内容），就不需要再装 python-mode 了。LSP 已经提供了 python-mode 的大部分功能，而且更现代。

如果你执意要装：

```lua
-- ~/.config/nvim/lua/plugins/python-mode.lua
return {
    {
        'python-mode/python-mode',
        config = function()
            -- python-mode 配置
            g.python_mode = {
                -- 补全
                completion = 1,
                -- 语法检查
                lint = 1,
                -- 代码折叠
                fold = 1,
            }
        end,
    }
}
```

---

## 8.4 Jupyter Notebook / JupyterLab——代码界的"活化石"

> 如果说普通的 Python 脚本是一篇**论文**，那 Jupyter Notebook 就是一篇**博客文章**——你可以混着写文字、代码、图表，甚至插入表情包！数据科学家们爱死了它，因为它让"边做实验边记录"成为可能。

**Jupyter 是什么？**

Jupyter 是 **Julia + Python + R** 的缩写（没错，这是个组合词），是一个开源的交互式计算环境。它的核心产品是 **Notebook**——一种可以在浏览器里运行的"活文档"。

### 8.4.1 安装与启动

#### 8.4.1.1 pip install jupyterlab

```bash
# 安装 JupyterLab（推荐，新版）
pip install jupyterlab

# 或者安装经典版 Jupyter Notebook
pip install notebook
```

> **JupyterLab vs Jupyter Notebook：** JupyterLab 是 Notebook 的升级版，界面更像一个完整的 IDE，可以同时打开多个笔记本、查看文件、调试。而经典 Notebook 界面比较简单，像是"单页应用"。**推荐用 JupyterLab。**

#### 8.4.1.2 jupyter lab 或 jupyter notebook

安装完成后，在终端里运行：

```bash
# 启动 JupyterLab（推荐）
jupyter lab

# 或者启动经典 Notebook
jupyter notebook
```

```text
# 终端会显示类似这样的输出：
[I 2024-01-15 10:30:00.000 ServerApp] jupyterlab preview running at:
[I 2024-01-15 10:30:00.000 ServerApp] http://localhost:8888/lab

# 然后浏览器会自动打开这个地址
# 如果没自动打开，手动复制网址到浏览器也行
```

```text
JupyterLab 界面布局
┌────────────────────────────────────────────────────────────┐
│ JupyterLab                                                │
├──────────┬─────────────────────────────────────────────────┤
│ File     │  Untitled.ipynb                                 │
│ Browser  │                                                 │
│          │  ┌──────────────────────────────────────────┐  │
│ 📁 Home  │  │ In [ ]: print("Hello, Jupyter!")        │  │
│  📄 a.py │  │                                          │  │
│  📄 b.py │  │ Out[ ]: Hello, Jupyter!                  │  │
│          │  └──────────────────────────────────────────┘  │
│          │  ┌──────────────────────────────────────────┐  │
│          │  │ In [ ]: import matplotlib.pyplot as plt │  │
│          │  │     plt.plot([1,2,3], [4,5,6])          │  │
│          │  │     plt.show()                           │  │
│          │  └──────────────────────────────────────────┘  │
├──────────┴─────────────────────────────────────────────────┤
│ Kernel: Python 3                                          │
└────────────────────────────────────────────────────────────┘
```

> **小技巧：** 如果你在服务器上运行 Jupyter，想从本地浏览器访问，需要加 `--ip=0.0.0.0` 和 `--port=8888` 参数，并注意防火墙设置。

### 8.4.2 常用快捷键

Jupyter 有两种模式：**编辑模式**（单元格在编辑状态）和**命令模式**（单元格被选中但不在编辑状态）。

#### 8.4.2.1 Shift + Enter：运行当前单元格

最常用的快捷键！运行当前单元格，然后自动选中下一个单元格。如果没有下一个单元格，会自动创建一个新的。

```python
# 选中这个单元格，按 Shift + Enter
print("运行我！")
# 输出：运行我！
```

#### 8.4.2.2 Esc：命令模式

按 `Esc` 键进入**命令模式**，此时你的键盘快捷键会变成操作单元格的指令，而不是输入文字。

> **命令模式 vs 编辑模式：** 命令模式下，按键是"命令"（如删除单元格、切换单元格类型）；编辑模式下，按键是"输入"（往单元格里打字）。记住：**只要不在打字，就是在命令模式。**

#### 8.4.2.3 A / B：在上方/下方插入单元格

- `A`：Above，在当前单元格**上方**插入新单元格
- `B`：Below，在当前单元格**下方**插入新单元格

```text
# 假设你有这样的单元格序列：
# [ ]: # 单元格1
# [ ]: # 单元格2

# 选中"单元格2"，按 A
# 结果：
# [ ]: # 单元格1
# [ ]: # 新单元格（上方插入）
# [ ]: # 单元格2
```

#### 8.4.2.4 DD：删除单元格

连续按两次 `D` 可以删除当前单元格。**这是一个危险的操作！** 如果你不小心删了，可以按 `Z` 撤销。

```text
# 假设有3个单元格
# [1]: print("第一")
# [2]: print("第二")  ← 你选中了这个
# [3]: print("第三")

# 按 DD 删除
# 结果：
# [1]: print("第一")
# [2]: print("第三")
# "第二"被删除了！😭

# 按 Z 撤销
# "第二"回来了！🎉
```

**更多常用快捷键汇总：**

| 快捷键 | 功能 | 模式 |
|--------|------|------|
| `Enter` | 进入编辑模式 | 命令模式 |
| `Esc` | 进入命令模式 | 编辑模式 |
| `Shift + Enter` | 运行单元格，选中下一个 | 命令模式 |
| `Ctrl + Enter` | 运行单元格，保持选中 | 命令模式 |
| `A` | 上方插入单元格 | 命令模式 |
| `B` | 下方插入单元格 | 命令模式 |
| `DD` | 删除单元格 | 命令模式 |
| `M` | 转为 Markdown | 命令模式 |
| `Y` | 转为代码 | 命令模式 |
| `Z` | 撤销删除 | 命令模式 |
| `H` | 显示快捷键帮助 | 命令模式 |

```markdown
# 演示：Notebook 里的 Markdown 单元格

## 这是一个标题

这是一个**加粗**的文本，这是一个*斜体*的文本。

- 列表项 1
- 列表项 2
- 列表项 3

> 引用块：Jupyter 让代码不再孤单！

```python
# 代码块也可以放在 Markdown 里
print("看，我是一段代码！")
```
```

### 8.4.3 插件安装

JupyterLab 的插件系统允许你安装各种扩展，增强功能。

#### 8.4.3.1 pip install jupyter_contrib_nbextensions

jupyter_contrib_nbextensions 是经典 Notebook 的扩展包，提供了一些很有用的功能。

```bash
# 安装扩展
pip install jupyter_contrib_nbextensions

# 安装 Javascript 和 CSS 文件
jupyter contrib nbextension install --user
```

> **注意：** 这个扩展包目前主要针对经典 Jupyter Notebook，JupyterLab 3+ 有自己的扩展系统（`jupyter labextension install`）。如果你用 JupyterLab，优先找对应的 Lab 扩展。

**JupyterLab 安装扩展的方法：**

```bash
# 方式一：使用 pip
pip install jupyterlab-git        # Git 集成
pip install jupyterlab-lsp         # LSP 支持（代码补全）

# 方式二：使用 jupyter labextension
jupyter labextension install @jupyterlab/github
```

#### 8.4.3.2 启用代码格式化、目录等插件

**代码格式化插件（jupyterlab-lsp）：**

```bash
# 安装 jupyterlab-lsp 和格式化后端
pip install jupyterlab-lsp
pip install python-lsp-server
pip install ruff  # 或 black

# ruff 配置（在 pyproject.toml 或 .ruff.toml）
```

**目录插件（jupyterlab-toc）：**

```bash
pip install jupyterlab-toc
```

```text
# 启用插件后，JupyterLab 界面会增加：
# - 左侧边栏的目录树（自动根据 Markdown 标题生成）
# - 代码补全（类似 VS Code 的体验）
# - 悬停文档
# - 跳转到定义
```

### 8.4.4 Voila：Jupyter 转 Web 应用

> **Voila 是什么？** 它可以把 Jupyter Notebook 转换成**独立的 Web 应用**！不需要用户懂代码，只需要会操作网页就行。这对于做数据可视化展示、仪表盘、机器学习模型展示等场景非常有用。

**安装 Voila：**

```bash
pip install voila
```

**使用方法：**

```bash
# 方式一：直接在 JupyterLab 里打开 Voila
# 在 Notebook 的菜单里：File → Save and Export Notebook As → Voila

# 方式二：命令行启动
voila my_notebook.ipynb

# 方式三：作为 JupyterLab 扩展
pip install voila
jupyter server extension enable --sys-prefix voila
```

**示例：创建一个简单的 Voila 应用**

```python
# 首先安装 ipywidgets（Voila 的 UI 组件）
pip install ipywidgets

# 创建一个有交互组件的 Notebook
import ipywidgets as widgets
from IPython.display import display

# 创建一个滑块
slider = widgets.FloatSlider(
    value=5.0,
    min=1.0,
    max=10.0,
    step=0.1,
    description='输入数字:',
    style={'description_width': 'initial'}
)

# 创建输出区域
output = widgets.Output()

# 定义计算函数
def calculate(change):
    output.clear_output()
    with output:
        n = change['new']
        result = n ** 2  # 计算平方
        print(f"{n} 的平方是 {result}")

# 绑定事件
slider.observe(calculate, names='value')

# 显示组件
display(slider, output)
```

```text
# 保存这个 Notebook，然后用 Voila 打开
# 用户会看到一个滑块网页
# 拖动滑块，网页会实时显示计算结果

# 滑块效果：
┌──────────────────────────────────────────────────────────┐
│                    我的计算器                             │
│                                                          │
│    输入数字: ○──────────●──────────○                    │
│                       5.0                                │
│                                                          │
│    ┌──────────────────────────────────────┐              │
│    │  5.0 的平方是 25.0                    │              │
│    └──────────────────────────────────────┘              │
│                                                          │
│    (拖动滑块，下面的结果会实时更新)                       │
└──────────────────────────────────────────────────────────┘
```

> **应用场景：** Voila 常用于数据科学家的"成果汇报"——他们训练完模型后，不需要给甲方演示代码，只需要展示一个网页，让对方输入参数，就能看到结果。**优雅，太优雅了。**

---

## 8.5 Google Colab——穷人的 AI 超算

> 如果说 Jupyter Notebook 是数据科学家的浪漫，那 Google Colab 就是**穷人的法拉利**——免费GPU/TPU、白嫖谷歌的计算资源、还能和同事实时协作。唯一的代价是：你得忍受偶尔的"正在分配资源"弹窗。

**Google Colab** 是谷歌提供的基于云端的 Jupyter Notebook 环境，运行在谷歌的服务器上。你只需要一个 Google 账号，就能在浏览器里写 Python 代码，而且**完全免费**！

> **限制：** 免费版有使用时长限制（通常每次会话最多 12 小时），而且 GPU/TPU 资源需要"抢"，不是你想用就能用。但对于学习和小项目来说，已经足够了。

### 8.5.1 免费 GPU / TPU 使用

#### 8.5.1.1 Runtime → Change runtime type → GPU / TPU

**步骤：**

1. 打开 [https://colab.research.google.com](https://colab.research.google.com)
2. 新建一个笔记本（或打开已有的）
3. 点击菜单：`Runtime` → `Change runtime type`
4. 在弹出的对话框里，选择 `Hardware accelerator`：

```text
Runtime Configuration 对话框
┌──────────────────────────────────────────────────────────┐
│ Notebook Settings                                         │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  Hardware accelerator:  ○ None                          │
│                           ● GPU                          │
│                           ○ TPU                          │
│                                                          │
│  Run on connected devices:                               │
│    ☑ Connect to a hosted runtime                        │
│                                                          │
│                                  [Cancel]  [Save]        │
└──────────────────────────────────────────────────────────┘
```

> **GPU vs TPU：** GPU（图形处理器）适合大多数深度学习任务；TPU（张量处理器）是谷歌自研的 AI 加速器，适合超大规模训练。普通学习用 GPU 就够了。

**验证 GPU 是否启用：**

```python
# 在 Colab 的单元格里运行这段代码
import tensorflow as tf

# 打印 TensorFlow 版本
print(f"TensorFlow 版本: {tf.__version__}")

# 检查 GPU 是否可用
print(f"GPU 可用: {tf.config.list_physical_devices('GPU')}")

# 如果输出类似 [PhysicalDevice(name='/physical_device:GPU:0', device_type='GPU')]
# 说明 GPU 已经成功启用！
```

```text
# 输出示例：
TensorFlow 版本: 2.15.0
GPU 可用: [PhysicalDevice(name='/physical_device:GPU:0', device_type='GPU')]
```

**一个更完整的 GPU 测试：**

```python
import torch

# PyTorch 测试
print(f"PyTorch 版本: {torch.__version__}")
print(f"CUDA 可用: {torch.cuda.is_available()}")
print(f"GPU 数量: {torch.cuda.device_count()}")
if torch.cuda.is_available():
    print(f"GPU 名称: {torch.cuda.get_device_name(0)}")
```

```text
# 输出示例：
PyTorch 版本: 2.1.0
CUDA 可用: True
GPU 数量: 1
GPU 名称: Tesla T4
```

> **Tesla T4** 是谷歌 Colab 免费版常用的 GPU 之一，性能还不错，至少比你的 CPU 快多了。

### 8.5.2 Google Drive 挂载

Colab 的存储空间是临时的（会话结束就清空），如果你想保存文件，需要把 Google Drive 挂载到 Colab 的文件系统中。

```python
# 运行这段代码，会显示一个授权链接，点击授权后会得到一个密钥
from google.colab import drive

# 挂载 Google Drive
drive.mount('/content/drive')
```

```text
# 输出：
Mounted at /content/drive
# 现在 /content/drive 就是你的 Google Drive 根目录了
```

```text
Colab 文件浏览器效果
┌──────────────────────────────────────────────────────────┐
│ 📁 文件                                                  │
│   ├─ /content/              # Colab 临时存储            │
│   │   └─ drive/                                       │
│   │       └─ My Drive/      # 你的 Google Drive        │
│   │           ├─ 📁 我的项目                            │
│   │           │   └─ 📄 model.pth                       │
│   │           └─ 📄 data.csv                            │
│   └─ /sample_data/          # Colab 示例数据           │
└──────────────────────────────────────────────────────────┘
```

**完整示例：保存和加载模型**

```python
import os

# 创建保存目录
save_dir = '/content/drive/My Drive/colab_models'
os.makedirs(save_dir, exist_ok=True)

# 假设你训练了一个模型
import torch
model = torch.nn.Linear(10, 2)  # 一个简单的线性层

# 保存模型到 Google Drive
model_path = os.path.join(save_dir, 'my_model.pth')
torch.save(model.state_dict(), model_path)
print(f"模型已保存到: {model_path}")

# 重新加载模型
loaded_model = torch.nn.Linear(10, 2)
loaded_model.load_state_dict(torch.load(model_path))
print("模型加载成功！")
```

```python
# 读取 Google Drive 里的数据
import pandas as pd

data_path = '/content/drive/My Drive/data.csv'
df = pd.read_csv(data_path)
print(f"数据形状: {df.shape}")
print(df.head())
```

> **注意事项：**
> 1. Google Drive 有 15GB 免费空间（和你的谷歌账号共享）
> 2. 挂载操作每个会话只需要执行一次
> 3. 大文件建议用 `.pth`/`.h5` 等格式保存，避免 Google Drive 显示"存储空间不足"

---

## 本章小结

本章我们探索了 **5 种非 VS Code 的 Python 编辑器**，每一种都有其独特的魅力和使用场景：

### 🎯 核心要点回顾

| 编辑器 | 适合人群 | 核心优势 |
|--------|----------|----------|
| **Cursor** | 想要 AI 加持的开发者 | Tab 补全、Composer 多文件生成 |
| **Sublime Text** | 追求速度的极客 | 启动飞快、界面骚气 |
| **Vim/Neovim** | 键盘侠、Terminal 爱好者 | 全键盘操作、LSP/DAP 强大定制 |
| **Jupyter** | 数据科学家、研究人员 | 交互式编程、图表展示 |
| **Google Colab** | 学生党、穷开发者 | 免费 GPU/TPU、云端协作 |

### 📝 关键概念

1. **LSP（Language Server Protocol）**：编辑器与语言服务器之间的通信协议，让编辑器能提供代码补全、跳转、错误提示等功能
2. **DAP（Debug Adapter Protocol）**：调试器适配协议，实现编辑器的调试功能
3. **虚拟环境**：独立的 Python 环境，隔离项目依赖
4. **Package Control / Mason**：编辑器的插件管理器

### 🔧 实战建议

- **日常开发**：VS Code 或 Cursor（Cursor 的 AI 补全更强）
- **服务器运维**：Vim/Neovim（远程 SSH 必备技能）
- **数据科学/实验**：Jupyter Notebook/Lab（边写边看图）
- **深度学习学习**：Google Colab（免费 GPU 不香吗？）
- **轻量编辑**：Sublime Text（打开速度快到离谱）

### 🎭 彩蛋

> 据说每个程序员都会经历以下几个阶段：
> 1. **用什么编辑器都行**（小白阶段）
> 2. **VS Code 天下第一**（入门阶段）
> 3. **试试 Sublime Text 吧**（进阶阶段）
> 4. **还是 Vim 香，键盘就是力量**（中二阶段）
> 5. **算了，最后还是用 VS Code**（返璞归真阶段）
>
> 所以，别纠结用哪个编辑器了，**能把代码写出来的就是好编辑器**。😎

---

*下一章我们将深入探讨 Python 的模块和包管理，让你的代码也能"拿来主义"，站在巨人的肩膀上写代码！*
