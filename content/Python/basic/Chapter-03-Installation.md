+++
title = "第3章 安装Python"
weight = 30
date = "2026-04-08T13:22:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 第三章：Python 3.14 安装指南——让你的电脑穿上"蟒蛇"新装

> 🎉 恭喜你！从这一刻起，你正式踏上了 Python 编程的征程。接下来的内容将手把手教你如何把 Python 3.14 请进你的电脑。准备好了吗？让我们开始吧！

想象一下：你刚刚下载了一个神秘的安装包，双击运行，一通"Next"、"Next"、"Install"之后——咦？居然安装成功了！🎊 但作为一个有追求的程序员，你当然不满足于"居然成功了"，你还要知道"为什么成功"、"怎么验证成功"、"万一不成功怎么办"。

本章就是你的"Python 安装全攻略"，覆盖 Windows、macOS、Linux 三大桌面系统，以及 Android 和 iOS 两个移动平台。无论你是用的是十年老古董笔记本，还是最新款的 MacBook Pro，抑或是揣在兜里的 iPhone——统统给你安排明白！

---

## 3.1 Python 3.14 新特性一览

在动手安装之前，我们先来了解一下 Python 3.14 到底带来了哪些新花样。毕竟，知其然还要知其所以然——当你知道 Python 3.14 为什么值得安装之后，敲命令的手指都会更有力！

> 💡 **Python 3.14 是什么？** Python 3.14 是 Python 语言的第 14 个大版本更新（别数了，确实是从 3.0 开始的），于 2024 年发布。相比前几个版本，3.14 在语法、速度、标准库方面都有不少值得关注的变化。

### 3.1.1 新增语法特性（详细列表）

Python 3.14 为程序员们带来了一系列语法层面的"小惊喜"。虽然不是那种颠覆性的革命，但每一个都切实地让代码写起来更优雅、更不容易出错。

#### 1. `match-case` 模式匹配的改进

还记得 Python 3.10 引入的 `match-case` 吗？Python 3.14 对其进行了进一步优化，改进了类型标注在 match 语句中的处理方式。当你写这样的代码时：

```python
from typing import TypeAlias

Shape: TypeAlias = "Circle | Square | Triangle"

def describe(shape: Shape) -> str:
    match shape:
        case {"type": "circle", "radius": r} if r > 0:
            return f"半径为 {r} 的完美圆"
        case {"type": "square", "side": s}:
            return f"边长为 {s} 的方正地块"
        case _:
            return "不明飞行物形状"
```

Python 3.14 让这类结构化模式匹配的编译效率更高了。

#### 2. `__debug` 预定义常量可以设为 `False`

这是 Python 历史上一个**巨大的语法变化**！在 Python 3.14 之前，`__debug__` 是一个只读常量，你永远无法在运行时改变它。但从 3.14 开始，如果你用 `-O`（大写字母 O）参数运行解释器，`__debug__` 可以被设为 `False`，从而让所有 `assert` 语句彻底消失于字节码之中。

```python
# 在普通模式下运行：
# python script.py
# __debug__ = True
assert 1 + 1 == 2, "数学没问题"  # 通过

# 用 -O 参数运行：
# python -O script.py
# __debug__ = False
# 整个 assert 就像从没存在过，字节码里找不到它
```

> ⚠️ 注意：`__debug__`（两个下划线）和 `debug` 是不同的，后者就是你随便定义的普通变量！

#### 3. 异步迭代器中 `yield` 和 `yield from` 在错误消息中更友好

Python 3.14 改进了某些语法错误的报错信息，当你在异步生成器中误用 `yield` 时，解释器会给出更清晰的提示，而不是抛出一个让人摸不着头脑的 `SyntaxError`。

#### 4. f-string 表达式允许使用 `=` 自引用（PEP 701 延续）

虽然 f-string 在 Python 3.12 就已经大幅改进了（终于可以在 f-string 里写注释和多行表达式了），3.14 继续打磨细节，提升了 f-string 在复杂表达式下的解析正确性。

```python
name = "小明"
score = 95

# Python 3.14 中 f-string 的高级用法
print(f"学生 {name} 的成绩是 {score}，等级：{'A' if score >= 90 else 'B'}")
# 学生 小明 的成绩是 95，等级：A
```

#### 5. `type` 类的改进

`type.__set_name__` 在自定义类中的行为更加一致。

---

### 3.1.2 标准库改进

Python 3.14 的标准库也迎来了一波升级，很多常用的模块都有了新功能或者性能提升。

#### `typing` 模块的增强

- `typing.TypeAlias` 更加稳定，成为正式特性
- `typing.ReadOnly` 用于标记只读类型变量，在类型检查中更精确

#### `asyncio` 模块的改进

- `asyncio.Task` 的调度更加高效
- 新增 `asyncio.TaskGroup` 的更多支持，让并发编程更安全

#### `sqlite3` 模块

- 默认启用了 WAL（Write-Ahead Logging）模式，提升并发读写性能

```python
import sqlite3

conn = sqlite3.connect("demo.db", check_same_thread=False)
# Python 3.14 中，SQLite 默认使用 WAL 模式，性能更好
cursor = conn.cursor()
```

#### `io` 模块

- `io.TextIOWrapper` 在处理 `encoding="locale"` 时更加高效

#### `cmath` 和 `math` 模块

- 新增若干数学常数和函数

#### `zipfile` 模块

- 支持新的压缩算法和更大的文件处理

#### `pathlib` 模块增强

```python
from pathlib import Path

# Python 3.14 中 pathlib 的新方法
p = Path("example.txt")
# 新增的方法让路径操作更流畅
print(p.suffix)        # .txt
print(p.stem)          # example
print(p.parent.name)   # 上级目录名
```

---

### 3.1.3 解释器性能提升细节

Python 3.14 的执行速度又双叒叕变快了！官方数据显示，Python 3.14 相比 3.13 平均提速约 **5%-10%**，在某些特定基准测试中甚至可以达到 **15%** 的提升。这是怎么做到的？让我们来一探究竟。

#### 1. 字节码优化

Python 3.14 重新设计了一批常用字节码指令（bytecodes），减少了解释器在执行时需要做的"查表"次数。举个例子，`LOAD_ATTR`、`CALL_FUNCTION` 等高频指令的内部实现被简化了，CPU 在跑这些指令时能少跳几次。

```python
# 这段简单的代码在 Python 3.14 中执行得更快
def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

print(fibonacci(1000))
# 在 3.14 中，同样的代码比 3.13 快大约 10%
```

#### 2. 内存分配器改进

Python 的 `pymalloc` 分配器在 3.14 版本中针对小对象（小于 256 字节）的分配做了大量优化。新分配器的锁竞争更少，在多线程场景下性能提升尤为明显。

#### 3. 帧栈优化

Python 3.14 减少了每个函数调用在帧（frame）层面的开销。函数调用是 Python 程序中最频繁的操作之一，哪怕每个调用只省下几个 CPU 周期，累积起来效果也是相当可观的。

#### 4. 内联缓存（Inline Caching）增强

还记得 Python 3.11 引入的"自适应解释器"吗？3.14 在这个基础上进一步扩展了内联缓存的覆盖范围，让更多类型的操作能够享受缓存带来的提速。

#### 5. 启动速度优化

`Precompile standard library`（标准库预编译）功能在 Python 3.14 中得到了更好的默认支持，首次启动 Python 时会自动将核心标准库模块编译成 `.pyc` 文件并缓存起来。

> 📊 **性能提升小结**（来源：Python 官方 benchmark）
>
> | 测试场景 | 3.12 → 3.14 提升 |
> |---------|----------------|
> | django_template | ~10% |
> | nbody | ~8% |
> | float | ~12% |
> | pickle benchmark | ~5% |
> | call_simple | ~15% |

---

### 3.1.4 废弃和移除的模块（deprecation）

Python 的哲学是"要有远见地抛弃"（consenting adults）。对于那些确实有问题的旧特性，Python 会给开发者充分的预警时间。Python 3.14 正式宣布了一些模块的倒计时。

#### 正式移除（Removed in 3.14）

以下模块在 Python 3.14 中已被彻底移除，如果你还在用它们，赶紧找替代品：

| 废弃模块 | 替代方案 | 说明 |
|---------|---------|------|
| `imp` | `importlib` | `imp` 模块在 Python 3.4 就被标记为废弃了 |
| `asyncore` | `asyncio` | 古早的异步 I/O 模块 |
| `smtpd` | `aiosmtpd` 或第三方库 | 邮件服务器模块几乎没人用了 |

#### 废弃警告（Deprecated, will be removed in 3.16）

以下模块将在 Python 3.16 中被移除，3.14 只是发出警告：

- `typing.Union` 的某些用法（使用 `X | Y` 替代）
- `cgi` 模块（Web 开发早就不用了）

#### 废弃的功能标志（Pending Removal）

- 某些 `ast` 模块的旧 API
- `locale` 模块中过时的字符集别名

> 🔔 **小贴士**：运行 `python -W default::DeprecationWarning` 可以看到你代码中所有触发 deprecation 警告的地方。

---

### 3.1.5 Python 3.14 与 3.13、3.12 的差异对比表

为了让你一目了然地看到三个版本的差异，我们整理了以下对比表：

| 特性 | Python 3.12 | Python 3.13 | Python 3.14 |
|------|------------|------------|------------|
| **发布时间** | 2023年10月 | 2024年10月 | 2024年10月 |
| **f-string** | 重大改进（可在 f-string 中写多行、注释） | 继续打磨 | 表达式解析进一步优化 |
| **`__debug__` 可设为 False** | ❌ 不支持 | ❌ 不支持 | ✅ 支持（`-O` 参数） |
| **解释器速度** | 比 3.11 快约 25% | 比 3.12 快约 10% | 比 3.13 快约 5-10% |
| **`match-case`** | 基础版本 | 改进 | 进一步优化 |
| **默认哈希种子** | 随机化 | 随机化 | 随机化 + 改进 |
| **`imp` 模块** | 已废弃 | 已废弃 | ✅ 已移除 |
| **`asyncore` 模块** | 已废弃 | 已废弃 | ✅ 已移除 |
| **预编译标准库** | 可选 | 可选 | 更好的默认支持 |
| **Apple Silicon 优化** | 初始支持 | 优化 | 原生支持完善 |
| **WAL 模式 sqlite3** | ❌ 不支持 | ❌ 不支持 | ✅ 支持 |
| **最大字符串长度** | 2GB | 2GB | 增大（取决于平台） |

---

## 3.2 Windows 系统安装 Python 3.14

好了，背景知识铺垫完毕！现在让我们来真刀真枪地安装 Python 3.14。我们从 Windows 开始，因为这是地球上使用人群最多的操作系统。

### 3.2.1 访问官网 python.org 下载页面

首先，打开你的浏览器（别用 IE 了，求你了），在地址栏输入：

```
https://www.python.org/downloads/
```

> 💡 **python.org 是什么？** python.org 是 Python 编程语言的官方网站，由 Python Software Foundation（PSF，Python 软件基金会）维护。这里是下载官方正版 Python 的唯一正确渠道。其他的第三方网站（比如某数字软件管家）可能带有广告插件或者附加软件，一不小心就给你塞个"浏览器导航"。

打开后，你会看到一个醒目的"Download Python 3.14.x"按钮（x 是具体的补丁版本号，比如 3.14.0）。点击它！

![Python官网下载页面截图](https://www.python.org/static/community_logos/python-logo-master-v3-TM.png)

> 🖥️ **图：python.org 下载页面。点击那个巨大的黄色（或者绿色，取决于季节）下载按钮就行了！**

### 3.2.2 选择正确的安装包（64-bit vs 32-bit vs ARM64）

下载页面会列出多个安装包文件，它们名字里的学问可大了：

```
python-3.14.0-amd64.exe        # 64位 Windows 安装包（最常见）
python-3.14.0.exe              # 32位 Windows 安装包
python-3.14.0-arm64.exe        # Windows ARM 64 安装包（Surface Pro X 等设备）
```

#### 3.2.2.1 如何判断 Windows 系统是 64 位还是 32 位

**方法一：设置查看法（适合所有 Windows）**

1. 按下 `Win + I` 打开"设置"
2. 点击"系统" → "关于"
3. 找到"系统类型"一行

如果显示"64 位操作系统"，就下载 `amd64.exe` 版本；如果显示"32 位操作系统"，就下载不带后缀的 `exe` 版本。

> 💡 **amd64 是什么？** amd64 并不是说你的 CPU 一定是 AMD 的！它是 Intel 和 AMD 共同制定的 64 位处理器架构标准的名字。当年 Intel 想叫它 IA-64，AMD 不同意，于是 AMD 自己搞了个 amd64——结果因为 Intel 后来也采用了这个标准，所以现在大多数 64 位 PC 都用 amd64 这个名字。

**方法二：命令行法（适合喜欢敲命令的程序员）**

```cmd
# 打开命令提示符（CMD），输入：
systeminfo | findstr /B /C:"OS 类型"

# 或者更简单：
echo %PROCESSOR_ARCHITECTURE%
```

输出如果是 `AMD64` 或 `x64`，说明是 64 位系统；如果是 `x86`，说明是 32 位系统。

```cmd
C:\> echo %PROCESSOR_ARCHITECTURE%
AMD64
# 你的 CPU 是 64 位的！
```

**方法三：任务管理器法**

1. 按下 `Ctrl + Shift + Esc` 打开任务管理器
2. 点击"性能"标签
3. 左侧找到"CPU"，右上角就能看到系统类型

#### 3.2.2.2 Windows ARM 64 版本说明

ARM64 版本的 Windows 主要运行在以下设备上：

- **Surface Pro X**：微软推出的 ARM 架构 Surface
- **三星 Galaxy Book Go**
- **联想 Flex 5G**
- **部分惠普、Dell 的 ARM 笔记本**

> ⚠️ **普通用户不需要下载 ARM64 版本！** 如果你不确定自己是不是 ARM 电脑，那 99.9% 的概率你不是。用 `amd64.exe` 就对了。

### 3.2.3 安装向导选项详解

双击安装包，Windows 可能会弹出"用户账户控制"（UAC）的提示，问你"是否允许此应用对你的设备进行更改"。点"是"就行——毕竟安装 Python 确实需要对你的系统做更改。

> 💡 **UAC 是什么？** User Account Control（用户账户控制），是 Windows 的安全机制。它会阻止未经授权的应用对系统关键部分做出更改。Python 安装程序需要向系统目录写入文件，所以需要你的确认。

安装向导打开后，你会看到几个选项。让我一个一个来解释：

#### 3.2.3.1 Install launcher for all users（推荐勾选）

> 💡 **Install launcher 是什么？** Python Launcher 是一个小程序，它能让你在命令行中用 `python` 命令来启动 Python。它还能帮助你在同一台电脑上管理多个 Python 版本。

勾选这个选项的好处是：安装后可以在**任意目录**打开命令提示符，直接输入 `python` 运行 Python。如果不装这个，你在某些目录里可能找不到 `python` 命令。

> ✅ **强烈推荐勾选！** 这个选项不会给你带来任何坏处，反而让命令行操作更方便。

#### 3.2.3.2 Add Python 3.14 to PATH（必须勾选！）

**这是整个安装过程中最重要的一个选项！！！** 如果你不勾选这一条，安装完成后你在命令行里输入 `python`，系统会告诉你"找不到 python 命令"——然后你就会在网上疯狂搜索"python 命令找不到怎么办"。

> ⚠️ **PATH 是什么？** PATH 是 Windows 的一个环境变量，它告诉操作系统"去哪些文件夹里找命令"。当你输入 `python` 时，Windows 会在 PATH 指定的文件夹里一个个地找 `python.exe` 这个文件。如果 Python 的安装目录不在 PATH 里，Windows 就找不到它。

勾选"Add Python 3.14 to PATH"后，安装程序会自动把 Python 的安装目录添加到 PATH 中，省去了你事后手动配置的麻烦。

> ✅ **必须勾选！必须勾选！必须勾选！** 重要的事情说三遍。

#### 3.2.3.3 Customize install location（自定义安装路径）

点击"Customize installation"（自定义安装），可以更改 Python 的安装位置。默认情况下，Python 会被安装到：

```
C:\Users\你的用户名\AppData\Local\Programs\Python\Python314\
```

如果你想装到其他地方（比如 `D:\Python314`），可以在这里修改。

> 💡 **为什么有人要改安装路径？** 常见原因：1. C 盘空间不够；2. 想要统一管理多个 Python 版本；3. 公司电脑有固定的软件安装目录要求。

### 3.2.4 安装过程中的选项

点击"Customize installation"后，会进入一个详细的选项页面。让我来解释每个选项：

#### 3.2.4.1 Install Python 3.14 for all users

勾选这个选项后，Python 会被安装到所有用户都能访问的位置（通常是 `C:\Program Files\Python314`），而不是只安装在当前用户目录下。

> 💡 **适合场景**：如果你是在公司电脑、公共电脑或者家庭共享电脑上安装，想要其他用户也能用 Python，就勾选这个。如果只是自己用，不勾选也没关系。

#### 3.2.4.2 Associate files with Python

这个选项会把 `.py` 文件（Python 源代码文件）和 Python 解释器关联起来。勾选后，双击任意 `.py` 文件，Windows 会自动用 Python 来运行它。

> ✅ **推荐勾选！** 勾了这个，你以后在文件管理器里看到 `.py` 文件，图标会变成 Python 的样子，双击就能运行。

#### 3.2.4.3 Create shortcuts

创建开始菜单快捷方式，包括 Python 解释器、IDLE（Python 自带的编辑器）和 Python 文档的快捷方式。

> ✅ **推荐勾选！** 方便从开始菜单快速启动 Python。

#### 3.2.4.4 Precompile standard library（加速启动）

这个选项会在安装时把 Python 标准库的所有 `.py` 文件预编译成 `.pyc` 字节码文件。这样以后每次启动 Python，导入常用模块会更快。

> ✅ **推荐勾选！** 虽然会稍微延长安装时间（多等几秒钟），但以后每次用 Python 都受益。

所有选项设置好后，点击"Install"，喝口水，等进度条走完就好了！

### 3.2.5 安装验证

安装完成了！🎉 现在让我们来验证 Python 是否正确安装。

#### 3.2.5.1 打开命令提示符（CMD）

**方法一：快捷键法**

按下 `Win + R`，输入 `cmd`，回车！

**方法二：开始菜单法**

点击开始菜单，输入"cmd"或"命令提示符"，回车。

**方法三：在文件夹里打开（适合程序员）**

在文件夹地址栏输入 `cmd`，回车。当前目录就打开了命令提示符。

#### 3.2.5.2 输入 python --version 验证

```cmd
C:\Users\你的用户名> python --version
Python 3.14.0
# 如果显示这个，恭喜你，安装成功了！
```

> 💡 **注意大小写！** 是 `python --version`，不是 `Python --Version`，也不是 `python --VERSION`。Linux/macOS 命令行是区分大小写的（Windows 文件系统虽然不区分，但命令行工具名通常是区分的）。

#### 3.2.5.3 输入 where python 查看安装路径

```cmd
C:\Users\你的用户名> where python
C:\Users\你的用户名\AppData\Local\Programs\Python\Python314\python.exe
# 这就是 Python 的安装位置
```

> 💡 **where 命令是什么？** `where` 是 Windows 自带的命令，它会在 PATH 环境变量指定的目录中搜索指定的程序。如果你装了多个版本的 Python，`where python` 会列出所有找到的 `python.exe`。

#### 3.2.5.4 输入 pip --version 验证 pip 安装

```cmd
C:\Users\你的用户名> pip --version
pip 24.x from C:\Users\你的用户名\AppData\Local\Programs\Python\Python314\lib\site-packages\pip (Python 3.14)
# pip 也成功安装了！
```

> 💡 **pip 是什么？** pip 是 Python 的包管理器（package manager）。你可以把它想象成 Python 的"应用商店"——你想安装第三方库（比如用于数据分析的 pandas、用于Web开发的Django），就用 `pip install` 命令。Python 3.14 自带 pip，无需单独安装。

再测试一下 Python 交互模式：

```cmd
C:\Users\你的用户名> python
Python 3.14.0 (tags/v3.14.0:some-hash, ...) on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> print("Hello, Python 3.14!")
Hello, Python 3.14!
>>> 2 + 2
4
>>> exit()
# 退出 Python 交互模式
```

> 🎉 **完美！** 到这里，你的 Python 3.14 已经在 Windows 上成功运行了！

### 3.2.6 Windows 上安装常见问题

"明明按步骤来了，为什么出问题了？"别慌，让我们来看看那些最常见的问题和解决方案。

#### 3.2.6.1 "安装程序被拒绝"——权限问题（右键以管理员运行）

**错误表现**：
```
Installation aborted - Unable to create process. 
Error code: 5 (Access is denied)
```

**原因**：当前 Windows 账户没有足够的权限向系统目录写入文件。

**解决方案**：

1. 关闭安装程序
2. 找到下载的 `.exe` 文件
3. **右键** → **"以管理员身份运行"**（Run as administrator）
4. 重新进行安装

> 💡 **为什么会有权限问题？** 如果你用的是标准 Windows 用户账户（不是管理员账户），Windows 会阻止应用向 `C:\Program Files` 等受保护的系统目录写入文件。以管理员身份运行就是告诉 Windows"我知道我在干什么，让我来吧"。

#### 3.2.6.2 "0x80072eff"——网络问题（关闭代理或 VPN）

**错误表现**：
```
0x80072eff - The connection with the server was terminated unexpectedly
```

**原因**：安装程序在下载安装组件时网络连接被中断了。这通常发生在使用 VPN 或公司代理网络时。

**解决方案**：

1. 关闭 VPN / 代理
2. 重试安装

> 💡 **为什么 VPN 会导致安装失败？** 某些 VPN 会拦截 HTTPS 连接进行加密检查（Deep Packet Inspection），导致安装程序的下载连接被中断。

#### 3.2.6.3 "Installer's integrity check failed"——文件损坏（重新下载）

**错误表现**：
```
The installer integrity check failed. 
Please try downloading a new copy of the installer.
```

**原因**：安装包文件在下载过程中被损坏（网络中断、磁盘错误等）。

**解决方案**：

1. 删除损坏的安装包
2. 清空浏览器的下载缓存
3. 重新从 [python.org](https://www.python.org/downloads/) 下载
4. 关闭下载软件的断点续传功能试试

#### 3.2.6.4 安装后 python 命令找不到（PATH 未勾选）

**错误表现**：
```
'python' 不是内部或外部命令，也不是可运行的程序或批处理文件。
```

这是最最最常见的问题！没有之一！

**原因**：安装时忘记勾选 "Add Python to PATH"，或者安装路径没有正确添加到系统 PATH。

**快速诊断**：

```cmd
C:\Users\你的用户名> where python
# 如果显示"找不到 python"，就说明 PATH 有问题
```

**解决方案一：重新运行安装程序**

最简单的方法——重新运行 Python 安装程序，选择"Modify"（修改），然后勾选"Add Python to PATH"。

**解决方案二：手动添加 Python 到 PATH（见下节）**

#### 3.2.6.5 手动添加 Python 到 PATH 环境变量

如果安装时忘了勾选，或者有其他原因导致 PATH 没有正确配置，我们需要手动来添加。

**步骤一：找到 Python 的安装路径**

通常是以下之一：

```
C:\Users\你的用户名\AppData\Local\Programs\Python\Python314\
C:\Users\你的用户名\AppData\Local\Programs\Python\Python314\Scripts\
C:\Program Files\Python314\
C:\Program Files\Python314\Scripts\
```

**步骤二：打开环境变量设置**

1. 右键"此电脑"（或"我的电脑"）
2. 选择"属性"
3. 点击"高级系统设置"
4. 点击"环境变量"按钮

**步骤三：编辑 PATH**

1. 在"系统变量"中找到 `Path`（注意大小写）
2. 双击 `Path`，打开编辑窗口
3. 点击"新建"，输入 Python 的安装路径
4. **再新建一条**，输入 Python 安装路径下的 `Scripts` 文件夹路径（因为 pip 在这里）

```cmd
# 例如添加：
C:\Users\longx\AppData\Local\Programs\Python\Python314
C:\Users\longx\AppData\Local\Programs\Python\Python314\Scripts
```

5. 点击"确定"保存

**步骤四：验证**

重新打开一个新的命令提示符窗口（！必须重新打开，环境变量修改对已打开的窗口不生效），输入：

```cmd
C:\Users\你的用户名> python --version
Python 3.14.0
# 成功了！
```

> 💡 **为什么有两个路径？** Python 本身在主安装目录下，但 `pip`（包管理器）以及 `wheel` 等工具安装在 `Scripts` 子目录下。所以两个都要加到 PATH 里。

#### 3.2.6.6 多个 Python 版本冲突问题

**问题表现**：

```cmd
C:\Users\你的用户名> python --version
Python 3.12.0  # 啊哦，这不是我刚装的 3.14！
```

或者：

```cmd
C:\Users\你的用户名> where python
C:\Python312\python.exe          # 旧版本在前面
C:\Users\longx\AppData\Local\Programs\Python\Python314\python.exe  # 新版本在后面
```

**原因**：系统中已经安装了其他版本的 Python，新版本的路径没有排在前面。

**解决方案一：调整 PATH 顺序**

在环境变量设置中，把 Python 3.14 的路径拖动到最上面（或者最前面）。

**解决方案二：使用 python Launcher 指定版本**

Python Launcher 允许你用 `py` 命令来明确指定运行哪个版本：

```cmd
C:\Users\你的用户名> py -3.14 --version
Python 3.14.0

C:\Users\你的用户名> py -3.12 --version
Python 3.12.0
```

**解决方案三：使用全路径运行**

```cmd
C:\Users\longx\AppData\Local\Programs\Python\Python314\python.exe --version
Python 3.14.0
```

> 💡 **建议**：安装多个 Python 版本时，建议用 py Launcher 或者专门的版本管理工具（如 `pyenv-win` for Windows），而不是手动改 PATH。

---

## 3.3 macOS 系统安装 Python 3.14

好了，Windows 用户已经全部搞定！现在让我们来看看 macOS（以前叫 Mac OS X）用户怎么安装 Python 3.14。

### 3.3.1 macOS 自带 Python 2.7 的历史问题

在开始安装之前，让我们先来一段"历史课"——这对你理解 macOS 上的 Python 环境非常重要。

macOS 从娘胎里就自带了 Python 2.7（以及一些其他的编程语言）。这是 Apple 为了保证某些系统脚本能正常运行而设置的。但是 Python 2.7 在 2020 年 1 月 1 日就已经正式"退休"了（end of life），Apple 也意识到了这一点，但出于兼容性考虑，他们既没有移除旧版 Python 2.7，也没有把新版 Python 设为默认。

> ⚠️ **重要提醒**：macOS 自带的 Python 2.7 和任何你手动安装的 Python 3.x **完全是两套独立的系统**！不要尝试升级或修改系统自带的 Python 2.7，否则你可能会搞坏 macOS 的一些系统功能！

所以在 macOS 上，你通常需要：

- 系统 Python 2.7：维持原样，不要动
- 自己安装的 Python 3.14：放心使用，想怎么折腾怎么折腾

### 3.3.2 使用 python.org 官方安装包安装

这是最"官方"、最直接的方式。Apple 官方也推荐这种方式。

#### 3.3.2.1 下载 macOS 64-bit universal2 installer

1. 打开浏览器，访问 [https://www.python.org/downloads/](https://www.python.org/downloads/)
2. 点击"Download Python 3.14.x"按钮
3. 下载一个后缀为 `macosx-*-universal2.pkg` 的安装包

> 💡 **universal2 是什么？** universal2 是 Apple 推出的一种二进制格式，可以在同一份安装包里包含针对两种架构的编译版本：x86_64（Intel Mac）和 arm64（Apple Silicon Mac）。无论你是 Intel 芯片还是 M1/M2/M3/M4 芯片，一个安装包全搞定！

#### 3.3.2.2 运行安装包

1. 双击下载的 `.pkg` 文件
2. 在"简介"页面点击"继续"
3. 阅读许可协议，点击"继续" → "同意"
4. 选择安装位置（默认即可），点击"安装"
5. 输入你的 macOS 用户密码（安装软件需要管理员权限）

安装程序会自动把 Python 安装到 `/Library/Frameworks/Python.framework/Versions/3.14/` 目录下。

> 💡 **这个路径为什么这么深？** Python 在 macOS 上的标准安装位置是 `/Library/Frameworks/Python.framework/Versions/`。Apple 的设计哲学是把所有第三方框架都放在这里，和系统框架分开，互不干扰。

#### 3.3.2.3 验证安装：python3 --version

安装完成后，打开终端（Terminal），输入：

```bash
python3 --version
Python 3.14.0
```

> 💡 **为什么是 `python3` 而不是 `python`？** 在 macOS（和 Linux）上，`python` 命令通常指向系统自带的 Python 2.7。为了避免冲突，你安装的 Python 3.x 被自动链接为 `python3`。这是好事！可以避免你误操作搞坏系统 Python。

### 3.3.3 使用 Homebrew 安装（推荐）

Homebrew 是 macOS 上最流行的包管理器，被称为"macOS 缺失的包管理器"。用 Homebrew 安装 Python 有很多好处：升级方便、卸载干净、依赖管理智能。

#### 3.3.3.1 安装 Homebrew

如果你还没有安装 Homebrew，打开终端，输入：

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

> 💡 **Homebrew 是什么？** Homebrew 是一个开源的 macOS/Linux 软件包管理器。它能让你用简单的命令（`brew install xxx`）来安装各种开发工具和软件，而不用自己去下载 `.dmg` 或 `.pkg` 文件手工安装。它还会自动处理依赖关系。

安装过程中可能需要你输入 macOS 密码，还会提示安装 Xcode Command Line Tools（一套开发工具），全部同意就好。

安装完成后，验证一下：

```bash
brew --version
Homebrew 4.x.x
```

#### 3.3.3.2 更新 Homebrew：brew update

每次安装软件之前，建议先更新一下 Homebrew 的软件仓库索引：

```bash
brew update
# Running `git update`...
# Already up-to-date.
# 或者会显示更新的内容
```

> 💡 **为什么要先 update？** Homebrew 的软件包信息存储在本地（就像一个"软件目录"），`brew update` 会把这个目录更新到最新版本，确保你能安装到最新版的 Python。

#### 3.3.3.3 安装 Python 3.14：brew install python@3.14

```bash
brew install python@3.14
```

Homebrew 会自动下载 Python 3.14 以及它的所有依赖项。下载和编译需要一些时间（Homebrew 从源码编译软件），可以泡杯咖啡等着。

```bash
# 看到类似这样的输出就说明安装成功了：
# ==> Installing Python@3.14...
# ==> Pouring python@3.14--3.14.0.xx.xx.arm64_monterey.bottle.tar.gz
# ==> /opt/homebrew/Cellar/python@3.14/3.14.0: x,xxx files, xxx MB
```

#### 3.3.3.4 验证：python3 --version 和 pip3 --version

```bash
# 验证 Python 版本
python3 --version
Python 3.14.0

# 验证 pip 版本
pip3 --version
pip 24.x from /opt/homebrew/lib/python3.14/site-packages (python 3.14)
```

> 🎉 **完美！** Homebrew 安装的 Python 3.14 可以通过 `python3` 和 `pip3` 命令使用了！

#### 3.3.3.5 Homebrew 安装路径说明

Homebrew 把软件安装到两个不同的位置，取决于你的 Mac 芯片类型：

| 芯片类型 | 安装路径 |
|---------|---------|
| Apple Silicon（M1/M2/M3/M4） | `/opt/homebrew/Cellar/python@3.14/` |
| Intel | `/usr/local/Cellar/python@3.14/` |

Python 的可执行文件在 `bin` 子目录下，会被软链接到：

```bash
# Apple Silicon Mac 上的路径：
/opt/homebrew/bin/python3     -> 实际是 Cellar 中的链接
/opt/homebrew/bin/pip3
```

> 💡 **Cellar 是什么？** Homebrew 的"酒窖"（Cellar），存放所有通过 Homebrew 安装的软件。每个软件一个子目录，井井有条。

### 3.3.4 macOS 多版本共存与切换

很多开发者需要在不同项目中使用不同版本的 Python。macOS 上有几种方式来管理多个 Python 版本。

#### 3.3.4.1 使用 pyenv 管理多版本

`pyenv` 是一个专门用于管理多个 Python 版本的工具，macOS 上非常流行。

**安装 pyenv**：

```bash
brew install pyenv
```

**安装完成后配置 shell**：

```bash
# 把以下内容添加到你的 ~/.zshrc 文件末尾
# （如果你用的是 bash 而不是 zsh，就添加到 ~/.bashrc）

echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init -)"' >> ~/.zshrc

# 让配置生效
source ~/.zshrc
```

**安装多个 Python 版本**：

```bash
pyenv install 3.14.0    # 安装 Python 3.14
pyenv install 3.13.0    # 安装 Python 3.13
pyenv install 3.12.0    # 安装 Python 3.12
```

**切换 Python 版本**：

```bash
# 切换到全局默认版本
pyenv global 3.14.0

# 切换到局部版本（只在当前目录生效）
pyenv local 3.12.0

# 查看当前版本
pyenv version
# 3.12.0 (set by /Users/你的用户名/当前目录/.python-version)
```

**pyenv 工作原理**：

```
当你输入 python3 时，pyenv 会在以下位置按优先级查找：
1. 当前目录的 .python-version 文件
2. 上级目录的 .python-version 文件（一直查到根目录）
3. HOME 目录的 .python-version 文件
4. PYENV_ROOT 指定的全局版本
```

> 💡 **pyenv 为什么不污染系统？** pyenv 通过修改环境变量 `PATH`，把自己放在最前面，从而拦截 `python` 命令。它实际上是在"欺骗"操作系统，让它认为特定版本的 Python 才是"默认"的。这种方式非常干净，不会修改任何系统文件。

#### 3.3.4.2 使用 python.org launcher 切换

如果你用 python.org 官方安装包安装了多个版本，Python Launcher 会自动为你创建一个 `python3.x` 的命令别名：

```bash
python3.14 --version   # Python 3.14
python3.13 --version   # Python 3.13
python3.12 --version   # Python 3.12
```

同时在 Scripts 目录（Windows 风格）或 bin 目录下，你会有对应的可执行文件。

### 3.3.5 Apple Silicon（M1/M2/M3/M4）Mac 注意事项

如果你用的是 2020 年以后发布的 Mac（搭载 Apple M 系列芯片），有以下几点需要特别注意。

#### 3.3.5.1 架构差异：x86_64 vs arm64

**x86_64（也写作 amd64）**：Intel 和 AMD 处理器使用的 64 位架构。2019 年之前的 Mac 都用的是 Intel 芯片。

**arm64**：Apple Silicon 使用的 64 位架构。2020 年以后发布的 Mac 使用的是苹果自研的 M1、M2、M3、M4 芯片。

两者的指令集完全不同，运行在 arm64 Mac 上的软件不能直接运行在 Intel Mac 上，反之亦然。

```bash
# 查看当前 Mac 的架构
uname -m
arm64     # Apple Silicon
# 或者
x86_64   # Intel Mac
```

#### 3.3.5.2 Rosetta 2 转译层说明

**Rosetta 2** 是 Apple 开发的一个动态翻译器，能让 Intel Mac 的软件在 Apple Silicon Mac 上运行。当你在 Apple Silicon Mac 上运行一个 x86_64 程序时，macOS 会自动调用 Rosetta 2 来实时翻译指令。

> 💡 **这意味着什么？** 理论上，你可以在 Apple Silicon Mac 上运行任何 Intel 编译的软件。但因为需要实时翻译，会有一定的性能损失（约 10-20%）。

不过，大多数情况下你不需要担心这个：

- Homebrew 会自动安装 **arm64 原生版本**的软件
- Python 官方安装包提供 **universal2** 版本，自动包含两种架构
- 常见的 Python 库（如 numpy、pandas）都有原生 arm64 编译版本

#### 3.3.5.3 Homebrew 自动选择原生 arm64 版本

Homebrew 非常智能。当你在一台 Apple Silicon Mac 上运行 `brew install python@3.14` 时，它会自动下载并安装 **arm64 原生版本**的 Python，而不是 x86_64 版本。

你可以通过以下方式验证：

```bash
# 查看 Python 是哪种架构
file $(which python3)

# Apple Silicon Mac 输出类似：
# /opt/homebrew/bin/python3: Mach-O 64-bit executable arm64
```

#### 3.3.5.4 验证架构：uname -m

```bash
# 在终端输入：
uname -m

# Apple Silicon Mac 输出：
arm64

# Intel Mac 输出：
x86_64
```

> 💡 **小技巧**：如果你在 Apple Silicon Mac 上发现某个软件是 x86_64 架构的（比如通过 `file $(which xxx)` 发现），可以考虑是否需要安装原生 arm64 版本以获得更好的性能。

### 3.3.6 macOS 安装常见问题

#### 3.3.6.1 zsh: command not found: python（默认命令是 python3）

**错误表现**：

```bash
zsh: command not found: python
```

**原因**：在 macOS 上，Python 3 的命令是 `python3`，而不是 `python`。`python` 命令通常指向系统自带的 Python 2.7（如果有的话）。

**解决方案**：

```bash
# 用 python3 而不是 python
python3 --version

# 如果你非常想用 python 命令，可以创建一个别名：
echo "alias python=python3" >> ~/.zshrc
source ~/.zshrc

# 但不推荐这样做，因为：
# 1. 系统脚本可能依赖 python 命令指向 Python 2
# 2. 你可能会忘记自己在用 Python 3
```

#### 3.3.6.2 homebrew 版本与 python@3.14 冲突

**错误表现**：

```bash
Error: Could not symlink python@3.14 ...
Target already exists.
```

**原因**：Homebrew 发现安装路径上已经有一个文件了，可能是之前安装的残留。

**解决方案**：

```bash
# 方法一：先卸载旧版本
brew uninstall python@3.13
brew install python@3.14

# 方法二：强制覆盖
brew install python@3.14 --force

# 方法三：检查冲突文件并删除
ls -la /opt/homebrew/bin/python*
rm /opt/homebrew/bin/python3  # 如果确认不需要
brew link python@3.14
```

#### 3.3.6.3 SSL 证书问题（安装 certifi 后修复）

**错误表现**：

```bash
>>> import ssl
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/opt/homebrew/Cellar/python@3.14/3.14.0/.../ssl.py", line 99, in <module>
    SSLctl = _ssl._SSLObject()
ssl.SSLError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: self signed certificate in certificate chain
```

**原因**：Python 在 macOS 上需要 SSL 证书来建立安全的网络连接（如访问 HTTPS 网站）。Homebrew 版本的 Python 需要你手动安装证书。

**解决方案**：

```bash
# 方法一：安装 certifi（推荐）
pip3 install certifi

# 方法二：运行 macOS 提供的证书安装脚本
# 这个脚本在 Python 安装目录下
/opt/homebrew/opt/python@3.14/bin/certifiSymlink.py

# 或者直接运行：
/Applications/Python\ 3.14/Install\ Certificates.command
# 会自动打开一个终端窗口并安装证书
```

> 💡 **为什么 macOS 上的 Homebrew Python 需要单独安装证书，而 Windows 版不需要？** 因为 macOS 有自己的证书管理系统（Keychain），Homebrew Python 无法直接访问它。Windows 版的 Python 则直接使用 Windows 的证书存储。

---

## 3.4 Linux 系统安装 Python 3.14

Linux 用户看过来！Linux 是 Python 的"故乡"（Python 最初就是在 Linux 上开发的），在 Linux 上运行 Python 是再自然不过的事情了。

### 3.4.1 源码编译安装完整流程（Ubuntu / Debian）

在 Ubuntu、Debian、Linux Mint、Pop!_OS 等基于 Debian 的发行版上，最标准的安装 Python 3.14 的方式是**从源码编译**。虽然听起来高大上，但其实步骤很清晰，跟着做就行。

> 💡 **为什么 Linux 要从源码编译？** 因为 Python 3.14 太新了，大多数 Linux 发行版的软件仓库（apt）里还没有它。为了获得最新版本的 Python，我们需要自己动手编译源码。

#### 3.4.1.1 更新系统包

第一步，先把系统的软件包列表更新到最新：

```bash
sudo apt update
```

> 💡 **apt 是什么？** apt（Advanced Package Tool）是 Debian/Ubuntu 系列的软件包管理器。你可以把它想象成 Ubuntu 的"应用商店"命令行版。`apt update` 会从互联网上的软件源下载最新的软件包列表。

#### 3.4.1.2 安装编译依赖

Python 是用 C 语言写的，从源码编译 Python 需要一系列开发工具和库。这一步非常重要，缺少依赖会导致编译失败。

```bash
sudo apt install -y \
    build-essential \
    zlib1g-dev \
    libncurses5-dev \
    libgdbm-dev \
    libnss3-dev \
    libssl-dev \
    libreadline-dev \
    libffi-dev \
    libsqlite3-dev \
    wget \
    libbz2-dev \
    liblzma-dev \
    tk-dev \
    uuid-dev \
    libcap-dev \
    dpkg-dev \
    gcc \
    make \
    cmake \
    autoconf \
    automake \
    bison
```

> 💡 **这些包都是干什么的？**
>
> | 包名 | 作用 |
> |------|------|
> | `build-essential` | GCC 编译器、make 等基础编译工具 |
> | `zlib1g-dev` | zlib 压缩库，pip 需要用它来解压安装包 |
> | `libssl-dev` | OpenSSL 开发库，SSL/TLS 网络通信需要 |
> | `libsqlite3-dev` | SQLite 数据库开发库 |
> | `libreadline-dev` | 命令行历史记录功能 |
> | `libffi-dev` | 动态语言运行时需要 |
> | `tk-dev` | Tk GUI 库，IDLE 编辑器需要 |

#### 3.4.1.3 下载 Python 3.14 源码（tgz 包）

去 Python 官方 FTP 下载源码包：

```bash
# 创建并进入工作目录
mkdir -p ~/python-build && cd ~/python-build

# 下载 Python 3.14.0 源码包（tgz 格式）
wget https://www.python.org/ftp/python/3.14.0/Python-3.14.0.tgz
```

> 💡 **tgz 是什么？** `.tgz` 文件就是 `tar.gz` 文件的简写。它是 Unix/Linux 世界最常用的源码分发格式——先把很多文件打包成一个大文件（`.tar`），再用 gzip 压缩（`.gz`）。

#### 3.4.1.4 解压、配置、编译、安装步骤

**第一步：解压源码包**

```bash
tar -xzf Python-3.14.0.tgz
cd Python-3.14.0
```

**第二步：配置（检查系统环境）**

```bash
./configure --enable-optimizations
```

> 💡 **`--enable-optimizations` 是什么？** 这是一个非常重要的选项！它会让编译过程运行一系列基准测试，然后根据你 CPU 的特性生成更高效的字节码。虽然配置时间会变长（可能多花 10-20 分钟），但能让最终的 Python 解释器运行速度提升大约 10-20%。

**第三步：编译（这步最耗时）**

```bash
make -j$(nproc)
```

> 💡 **`-j$(nproc)` 是什么？** 这表示"用所有 CPU 核心并行编译"。`nproc` 命令会输出你电脑的 CPU 核心数。`make -j4` 表示用 4 个核心同时编译，能大大加快速度。

编译需要一段时间，取决于你的电脑性能。可以去泡杯茶或者做一套眼保健操。

**第四步：安装**

```bash
# 注意！这里用的是 make altinstall，而不是 make install！
sudo make altinstall
```

### 3.4.1.5 make altinstall 的重要性（永远不要用 make install）

> ⚠️ **这是整章最重要的一个提示！请认真阅读！**

**为什么不能用 `make install`？**

如果你运行 `sudo make install`，Python 会被安装到系统默认位置（`/usr/local/bin/python3.14`），并**覆盖**系统自带的 Python。

> 💡 **系统 Python 是什么？** Ubuntu/Debian 的很多系统工具（如 `apt`、`dpkg`、`cron`）都是用 Python 写的，它们依赖特定版本的系统 Python。如果你不小心覆盖了系统 Python，`apt` 命令可能会坏掉，你的整个系统都会出问题！这就是为什么 Linux 程序员会说："`make install` 是危险的！"

**`make altinstall` 是什么？**

`make altinstall` 会把新 Python 安装为 `python3.14`（带版本号后缀），而不是覆盖 `python3` 或 `python`。这样：

- 系统自带的 `python3` 命令仍然指向系统 Python（安全）
- 你新装的 Python 用 `python3.14` 命令来运行（独立）

```
# make install 之后的 /usr/bin/python3：
# -> /usr/local/bin/python3.14  （系统 Python 被覆盖了！）

# make altinstall 之后的 /usr/local/bin/python3.14：
# -> 你的新 Python（独立，不影响系统）
# /usr/bin/python3 保持不变，仍然是系统 Python
```

### 3.4.1.6 验证安装

```bash
# 查看版本（注意有版本后缀）
python3.14 --version
Python 3.14.0

# 验证 pip
python3.14 -m pip --version
pip 24.x from /usr/local/lib/python3.14/site-packages (python 3.14)

# 进入交互模式
python3.14
>>> print("Hello from Python 3.14 on Linux!")
Hello from Python 3.14 on Linux!
>>> exit()
```

> 🎉 **完美！** 你已经成功从源码编译安装了 Python 3.14！

### 3.4.2 CentOS / RHEL / Fedora 编译安装

CentOS、RHEL（Red Hat Enterprise Linux）和 Fedora 都是基于 Red Hat 的发行版，它们的包管理器是 `yum` 或 `dnf`（新版本）。

#### 3.4.2.1 安装开发工具

```bash
# CentOS/RHEL 8+ 或 Fedora：
sudo dnf groupinstall -y "Development Tools"

# CentOS/RHEL 7：
sudo yum groupinstall -y "Development Tools"
```

#### 3.4.2.2 安装依赖库

```bash
sudo dnf install -y \
    gcc \
    make \
    wget \
    zlib-devel \
    openssl-devel \
    readline-devel \
    libffi-devel \
    sqlite-devel \
    bzip2-devel \
    xz-devel \
    gdbm-devel \
    ncurses-devel \
    tcl-devel \
    tk-devel \
    uuid-devel \
    libcap-devel \
    kernel-headers \
    dpkg-devel
```

#### 3.4.2.3 编译安装步骤

```bash
# 同样是四步走：
mkdir -p ~/python-build && cd ~/python-build
wget https://www.python.org/ftp/python/3.14.0/Python-3.14.0.tgz
tar -xzf Python-3.14.0.tgz
cd Python-3.14.0

./configure --enable-optimizations
make -j$(nproc)
sudo make altinstall
```

### 3.4.3 Arch Linux 安装

Arch Linux 用户应该是 Linux 玩家中的"技术流"，安装 Python 应该不在话下。但我还是简单说一下。

#### 3.4.3.1 pacman 安装

Arch Linux 的软件仓库通常更新很快，有时候 Python 3.14 一发布就能用 pacman 安装：

```bash
sudo pacman -S python
```

#### 3.4.3.2 AUR 中安装特定版本

如果你非要安装特定版本（比如 3.14.0），可以在 AUR（Arch User Repository）中找包：

```bash
# 使用 yay 或其他 AUR helper
yay -S python314
```

### 3.4.4 make install 与 make altinstall 的区别

为了让你彻底理解这个重要概念，我们来详细对比一下：

#### 3.4.4.1 make install：覆盖系统 Python（危险！）

```bash
# 绝对不要这样做！
sudo make install
# 这会把 Python 安装到 /usr/local/bin/
# 如果 /usr/local/bin 在你的 PATH 中比 /usr/bin 更靠前
# 那么 python 和 python3 命令就会被替换成新版本
# 后果：apt、dpkg、unattended-upgrades 等系统工具可能全部挂掉！
```

#### 3.4.4.2 make altinstall：安装为 python3.14（安全）

```bash
# 正确做法！
sudo make altinstall
# 这会把 Python 安装为 /usr/local/bin/python3.14
# python3 和 python 命令保持不变，仍然指向系统版本
```

#### 3.4.4.3 为什么系统包管理器依赖系统 Python？

```
Ubuntu/Debian 的软件包管理系统架构：

┌─────────────────────────────────────────────────┐
│  dpkg（Debian Package Manager）                  │
│  ↓                                              │
│  apt（Advanced Package Tool）                   │
│  ↓                                              │
│  Python 解释器（系统自带版本，保证兼容性）           │
└─────────────────────────────────────────────────┘

如果你用 make install 替换了系统 Python：
→ apt 命令失效
→ 你无法再使用 apt 安装/卸载任何软件
→ 系统更新停止
→ 如果没有 root 权限之外的包管理方式，你就被"锁"住了！
```

> ⚠️ **经验之谈**：除非你是唯一的管理员并且知道自己在干什么，否则永远不要用 `make install` 安装 Python。

### 3.4.5 Linux 安装常见问题

#### 3.4.5.1 configure 报错：no acceptable C compiler found

**错误表现**：

```
configure: error: no acceptable C compiler found in $PATH
```

**原因**：没有安装 GCC 编译器。

**解决方案**：

```bash
# Ubuntu/Debian:
sudo apt install build-essential

# Fedora:
sudo dnf groupinstall "Development Tools"

# CentOS:
sudo yum groupinstall "Development Tools"
```

#### 3.4.5.2 configure 报错：zlib not available

**错误表现**：

```
configure: error: zlib not available
```

**原因**：没有安装 zlib 开发库。

**解决方案**：

```bash
# Ubuntu/Debian:
sudo apt install zlib1g-dev

# Fedora:
sudo dnf install zlib-devel

# CentOS:
sudo yum install zlib-devel
```

#### 3.4.5.3 make 警告处理

编译过程中可能出现一些警告（warnings），大多数情况下可以忽略，Python 仍然能正常编译和使用。

**常见的无害警告**：

- `attribute 'xxx' in 'xxx' does not exist`（GCC 版本差异）
- `implicit declaration of function 'xxx'`（某些平台特定的警告）

**需要关注的警告**：
如果你看到 `fatal error`（致命错误），而不是 `warning`，那说明编译失败了，需要解决对应的问题。

#### 3.4.5.4 pip 安装包报错：pip is managed by an external package

**错误表现**：

```
WARNING: pip is managed by an external package
```

**原因**：Linux 发行版的系统包管理器（如 apt）也管理着 pip，导致 pip 和系统包管理器之间产生了冲突。

**解决方案**：

```bash
# 方法一：使用 python3.14 -m pip 代替 pip
python3.14 -m pip install numpy

# 方法二：忽略这个警告
# 这个警告是良性的，不影响 pip 的正常使用

# 方法三：给 pip 创建虚拟环境（最佳方案）
python3.14 -m venv myproject
source myproject/bin/activate
pip install numpy  # 在虚拟环境里，警告就不会出现了
```

> 💡 **什么是虚拟环境？** 虚拟环境（Virtual Environment）是一个独立的 Python 运行环境，每个项目有自己的 Python 解释器副本和第三方库，互不干扰。强烈建议每个项目都使用独立的虚拟环境！

---

## 3.5 移动端安装（Android / iOS）

什么？Python 还能在手机上跑？！没错！而且体验还相当不错！虽然手机没法替代电脑进行严肃的 Python 开发，但用来学习、测试小代码、或者做一些轻量级自动化任务是完全够用的。

### 3.5.1 Termux（Android）

Termux 是 Android 上最强大的终端模拟器，它实际上是一个完整的 Linux 环境，运行在 Android 上。有了 Termux，你可以在手机上做几乎所有 Linux 能做的事情，包括安装和使用 Python。

#### 3.5.1.1 Termux 安装（F-Droid 优于 Google Play）

> ⚠️ **强烈建议从 F-Droid 下载 Termux，而不是 Google Play！**

**为什么不用 Google Play 版？**

Google Play 上的 Termux 版本更新很慢，而且由于 Google Play 的应用签名机制问题，Google Play 版的 Termux 无法正常升级。F-Droid 是专门托管开源软件的商店，版本始终是最新的。

**下载地址**：

- F-Droid（推荐）：[https://f-droid.org/en/packages/com.termux/](https://f-droid.org/en/packages/com.termux/)
- Google Play（不推荐）：搜索 "Termux"

安装完成后，打开 Termux，你会看到一个黑色的终端界面——恭喜你，你已经进入了 Linux 的世界！

#### 3.5.1.2 pkg 安装 Python

Termux 有自己的包管理器叫做 `pkg`，用它来安装 Python 非常方便：

```bash
# 更新软件包列表（第一次使用前必须做）
pkg update

# 安装 Python
pkg install python
```

```bash
# 安装完成后验证版本
python --version
Python 3.14.0

# pip 也已经包含在内
pip --version
pip 24.x
```

> 🎉 **太棒了！** 在 Termux 里安装 Python 就是这么简单，全程只需要几个命令！

#### 3.5.1.3 使用 proot-distro 运行完整 Linux

Termux 本身是一个精简的 Linux 环境。如果你想要一个完整的桌面 Linux 发行版（比如 Ubuntu、Debian、Arch Linux），Termux 还提供了 `proot-distro` 功能，可以在不需要 root 权限的情况下运行完整的 Linux 系统。

**安装 proot-distro**：

```bash
pkg install proot-distro
```

**安装一个完整的 Linux 发行版**：

```bash
# 查看可用的发行版
proot-distro list

# 安装 Debian
proot-distro install debian

# 启动 Debian
proot-distro login debian
```

```bash
# 在 Debian 里安装 Python
apt update && apt install python3
python3 --version
# Python 3.11.x 或更高版本（取决于 Debian 版本）
```

> 💡 **proot 是什么？** proot 是一个不需要 root 权限的"伪"chroot 工具。它能让 Linux 程序以为自己运行在一个完整的 Linux 系统中，但实际上还待在 Android 的 Android 里。这项技术叫做"用户态 Linux"（User-mode Linux）。

### 3.5.2 PyDroid3（Android）

PyDroid3 是 Android 上另一款非常流行的 Python IDE/解释器应用。它的特点是开箱即用，不需要配置，非常适合初学者。

#### 3.5.2.1 Google Play 下载

在 Google Play 中搜索 "PyDroid3" 或 "PyDroid"，找到图标是一个橙色 Python 蛇的那个应用，下载安装即可。

> 💡 **PyDroid3 有免费版和付费版（PyDroid3 Premium）**。免费版包含基本的 Python 解释器和编辑器，付费版增加了更好的性能和更多功能。

#### 3.5.2.2 界面介绍与使用方法

PyDroid3 的界面非常直观：

```
┌─────────────────────────────┐
│  PyDroid 3                  │
│  ─────────────────────────  │
│  📁 Projects                 │
│  │  ├── hello.py            │
│  │  └── calculator.py       │
│  ─────────────────────────  │
│  ▶ Run (运行按钮)             │
│  🔧 Editor                   │
│  ─────────────────────────  │
│  >>>                        │
│  print("Hello!")            │
│  # Hello!                   │
└─────────────────────────────┘
```

**使用方法**：

1. 点击 `+` 按钮新建文件
2. 在编辑器中输入 Python 代码
3. 点击绿色的三角按钮（▶）运行
4. 输出会显示在下方

PyDroid3 支持：
- Python 3.10+ 语法
- 自动补全
- 语法高亮
- 直接运行 `.py` 文件
- pip 安装第三方库（付费版支持更完整）

### 3.5.3 Pythonista（iOS）

iOS 用户也有福了！Pythonista 是 iOS 上最专业的 Python 编程应用，专门为 iPhone 和 iPad 优化。

#### 3.5.3.1 App Store 下载

在 App Store 中搜索 "Pythonista"，下载安装。

> ⚠️ **Pythonista 是付费应用**（通常价格在 60-80 元人民币左右）。但考虑到它的功能完整性和便利性，对于认真想学 Python 的 iOS 用户来说，这个价格是值得的。

#### 3.5.3.2 内置编辑器和 console

Pythonista 提供了一个功能完整的代码编辑器：

- **语法高亮**：关键字、字符串、注释都用不同颜色标注
- **自动缩进**：自动保持代码缩进层级
- **代码补全**：输入时会弹出补全建议
- **多光标编辑**：用两个手指在屏幕上拖动可以同时编辑多行
- **文件浏览器**：项目文件夹一目了然

```python
# 在 Pythonista 中运行这个程序
print("Hello from Pythonista on iOS!")
name = input("你叫什么名字？")
print(f"你好，{name}！欢迎来到 Python 的世界！")
```

Console 区域在编辑器下方，可以交互式输入/输出。

#### 3.5.3.3 第三方库安装

Pythonista 预装了很多常用的第三方库：

- `numpy`：数值计算
- `matplotlib`：绘图
- `requests`：HTTP 请求
- `bs4`（BeautifulSoup）：网页解析
- `pil`（Pillow）：图像处理

如果你想安装其他库：

```python
# 在 Pythonista 的 console 中输入：
import pip
pip.main(["install", "库名"])
```

> 💡 **注意**：由于 iOS 的沙盒限制，Pythonista 不能安装所有 Python 库。特别是那些需要编译 C 扩展或者访问系统底层的库，可能无法在 Pythonista 中使用。

---

## 本章小结

恭喜你！你已经完成了 Python 3.14 的全部安装学习！让我们来回顾一下这一章的核心要点：

> 📝 **本章小结**

### Python 3.14 新特性

- `__debug__` 常量在 `-O` 模式下可以为 `False`，`assert` 语句会被彻底移除
- 解释器性能相比 3.13 提升约 5-15%，得益于字节码优化、内存分配器改进和帧栈优化
- `sqlite3` 默认启用 WAL 模式，提升并发性能
- 一些历史遗留模块（如 `asyncore`、`smtpd`）已在 3.14 中移除

### Windows 安装要点

- **必须勾选**：Add Python to PATH（这是最重要的事！）
- 64 位系统下载 `amd64.exe` 安装包
- 验证安装：命令提示符中输入 `python --version`
- PATH 没添加成功会导致 "python 不是内部命令" 错误，手动添加 PATH 即可解决

### macOS 安装要点

- **推荐使用 Homebrew 安装**（`brew install python@3.14`）
- 命令是 `python3` 而不是 `python`（macOS 自带 Python 2.7 不要动）
- Apple Silicon Mac 上 Homebrew 自动安装原生 arm64 版本
- SSL 证书问题需要单独运行 `Install Certificates.command` 修复

### Linux 安装要点

- **必须用 `make altinstall` 而不是 `make install`**（后者会破坏系统！）
- 编译前必须安装开发工具和依赖库（build-essential、zlib-dev 等）
- 多版本管理推荐使用 `pyenv`
- pip 警告可以用虚拟环境解决

### 移动端

- Android：Termux + pkg 是最强大、最灵活的选择
- iOS：Pythonista 是最专业的选择（付费应用）

---

### 安装检查清单

在结束本章之前，请确保你已经完成了以下检查：

- [ ] **Windows**：在 CMD 中运行 `python --version`，看到 `Python 3.14.x`
- [ ] **macOS**：在终端中运行 `python3 --version`，看到 `Python 3.14.x`
- [ ] **Linux**：在终端中运行 `python3.14 --version`，看到 `Python 3.14.0`
- [ ] **移动端**：打开 Termux/Pythonista/PyDroid3，运行 `print("Hello Python!")`
- [ ] **pip**：运行 `pip --version`（或 `pip3 --version`），确认包管理器可用

> 🎊 **恭喜你完成安装！现在你可以开始你的 Python 编程之旅了！**

---

> 📚 **下一章预告**：安装好了 Python，下一章我们将学习 Python 的基础知识，包括变量、数据类型、运算符、条件语句和循环结构。无论你是编程新手还是老手，下一章都会帮你夯实基础，为后续的学习铺平道路。

---

*本章结束*
