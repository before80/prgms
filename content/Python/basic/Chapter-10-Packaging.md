+++
title = "第10章 打包发布"
weight = 100
date = "2026-04-08T13:22:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 第十章：Python 代码运行与打包

> 本章我们将化身为"代码快递员"，学会如何把 Python 代码送到用户手上——无论是自己运行、命令行调用，还是打包成.exe发给不懂代码的七大姑八大姨。

想象一下：你写了一个超棒的程序，现在想让全世界人民都能用它。问题来了——不是每个人都有 Python 环境，也不是每个人都愿意在终端里敲 `python script.py`。这时候，你就需要打包了。

在这一章里，我们从最基础的"怎么运行 Python 代码"开始，一路升级到"怎么把代码变成双击就运行的程序"，再到"怎么把代码发布到 PyPI 让全世界 `pip install` 你"。

准备好，上车！

---

## 10.1 Python 代码运行方式

你知道吗，Python 代码有 N 种运行方式，比奶茶的配料表还多。让我们一种一种来看。

### 10.1.1 脚本文件运行

脚本文件运行，就是最传统、最常见、最"朴实无华"的方式。

#### 10.1.1.1 python script.py

这是 Python 世界里的"Hello World"级别的操作。

```python
# hello.py
print("你好，世界！我是最普通的 Python 脚本！")
# 运行：python hello.py
# 输出：你好，世界！我是最普通的 Python 脚本！
```

直接在终端输入：

```bash
python hello.py
```

> 小知识：这里的 `python` 其实是个程序，它负责读取你写的代码，然后一行一行解释执行。Python 解释器就是干这个的——就像翻译员，你说什么它就帮你翻译成机器能懂的语言。

#### 10.1.1.2 Windows 双击运行

在 Windows 上，如果你想让脚本像普通软件一样双击就能跑，有几个小技巧：

**方法一：创建快捷方式**

1. 右键点击 `hello.py` → 创建快捷方式
2. 右键快捷方式 → 属性
3. 在"目标"栏里改成 `C:\Python312\python.exe "C:\你的路径\hello.py"`
4. 改个好看的图标，大功告成！

**方法二：改文件关联（适合冒险家）**

```bash
# 打开注册表...（好吧，这太复杂了，我们不推荐）
```

**方法三：加一个批处理文件**

创建一个 `run.bat`：

```batch
@echo off
python "%~dp0hello.py"
pause
```

双击 `run.bat`，黑窗口一闪而过，你就能看到输出了！

> 小贴士：如果你想让窗口跑完后停留，加上 `pause`；如果想隐藏黑窗口，可以用 VBScript——但这都是雕虫小技，我们继续往下看正经方法。

### 10.1.2 模块运行

模块（Module）运行，这是一种更"组织化"的运行方式。想象你有一个项目，里面有多个 `.py` 文件，每个文件负责不同的功能。

#### 10.1.2.1 python -m module_name

`-m` 的意思是"以模块方式运行"。

假设你的项目结构是这样的：

```
myproject/
├── __init__.py    # 空文件，但告诉 Python 这是一个包
└── main.py
```

```python
# myproject/main.py
def run():
    print("模块运行成功！")

if __name__ == "__main__":
    run()
```

运行它：

```bash
cd myproject
python -m main
```

> 小知识：`__name__` 这个变量很神奇。当文件被直接运行时，它的值是 `"__main__"`；当被作为模块导入时，它的值是模块名。这行 `if __name__ == "__main__":` 的意思是"只有直接运行这个文件时才执行"，常用于写测试代码。

#### 10.1.2.2 python -m package.module

运行包里的特定模块：

```bash
python -m myproject.main
```

这比直接 `python myproject/main.py` 更好，因为：
- Python 能正确找到模块（不会有路径问题）
- 包会被正确初始化（`__init__.py` 会先执行）

### 10.1.3 包运行

有时候你想直接运行一个包，而不是某个模块。比如很多 CLI 工具（命令行工具）就是这样设计的。

#### 10.1.3.1 python -m package

假设你有一个包叫 `myapp`：

```
myapp/
├── __init__.py
└── __main__.py    # 这是关键！
```

```python
# myapp/__main__.py
print("包直接运行成功！来自 __main__.py 的问候！")
```

```bash
python -m myapp
# 输出：包直接运行成功！来自 __main__.py 的问候！
```

> 小知识：`__main__.py` 是个约定。当用 `python -m 包名` 运行一个包时，Python 会自动找这个包里的 `__main__.py` 并执行它。就像每个电影剧组都有一个"开场"的角色，`__main__.py` 就是包的"开场"。

### 10.1.4 -c 参数（直接运行字符串代码）

有时候你只想快速测试一行代码，或者验证某个函数的结果，不想新建文件——`-c` 参数就是你的瑞士军刀！

```bash
python -c "print('我不需要文件也能运行！')"
# 输出：我不需要文件也能运行！
```

计算一下：

```bash
python -c "import math; print(math.sqrt(16))"
# 输出：4.0
```

批量操作也行：

```bash
python -c "
import random
for i in range(5):
    print(random.randint(1, 100))
"
# 输出（每次都不一样）：
# 42
# 87
# 23
# 91
# 15
```

> 小贴士：`-c` 在写 Shell 脚本时特别有用，可以内嵌 Python 代码片段。但要注意引号嵌套，Windows 的 CMD 和 PowerShell 还有区别，小心别把自己绕晕了。

### 10.1.5 -i 参数（运行后进入交互模式）

`-i` 的意思是"交互模式"（interactive）。脚本运行完毕后，不退出 Python 解释器，而是留下一个交互式环境让你继续操作。

```python
# test_i.py
name = "小明"
age = 18
print(f"我是{name}，今年{age}岁")
```

```bash
python -i test_i.py
# 输出：我是小明，今年18岁
# 然后你会看到 >>> 提示符，可以继续输入：
# >>> print(name)
# 小明
# >>> age + 1
# 19
```

> 适用场景：调试的时候超级有用！你可以在脚本里设置好各种变量，然后进入交互模式慢慢测试各个函数，不用一遍遍重新运行脚本。

### 10.1.6 shebang 行

> **shebang**（发音：shi-bang，不是"死棒"）：也叫 hashbang，就是脚本第一行的 `#!`，告诉系统这个脚本应该用什么程序来执行。类 Unix 系统（Linux、macOS）专用，Windows 用户可能会困惑——但别担心，PyInstaller 会帮你搞定的。

#### 10.1.6.1 #!/usr/bin/env python3

```python
#!/usr/bin/env python3
# 这是个使用 shebang 的脚本

print("Hello from shebang!")
```

shebang 的几种写法：

```python
#!/usr/bin/python      # 直接指定 Python 路径（不推荐，不够灵活）
#!/usr/bin/env python3 # 灵活版，让系统自己去 PATH 里找 python3
#!/usr/bin/env python  # 找 python（可能指向 python2，慎用！）
```

> 小知识：`/usr/bin/env` 是个程序，它的任务是"在 PATH 环境变量里找程序"。所以 `#!/usr/bin/env python3` 的意思是：去 PATH 里找 python3，然后用它来运行这个脚本。这种方式比硬编码路径好，因为不同系统 Python 安装位置可能不一样。

#### 10.1.6.2 chmod +x script.py 后直接运行

在 Linux/macOS 上：

```bash
chmod +x hello.py    # 赋予执行权限
./hello.py           # 直接运行（不需要 python 前缀）
```

> 等等！Windows 用户别走！Windows 不认识 shebang，它看到 `#!` 会以为这是注释，根本不鸟你。不过没关系，等我们学到 PyInstaller 的时候，Windows 用户就能笑着看 Linux 用户了——因为 PyInstaller 打包出来的 .exe，Windows 和 Linux 都能用！

### 10.1.7 python 命令行参数速查

Python 解释器有一大堆命令行参数，下面几个最常用：

#### 10.1.7.1 -B：阻止写入 .pyc 文件

Python 运行时会生成 `.pyc` 文件（编译后的字节码），用来加速下次启动。加 `-B` 可以阻止这件事：

```bash
python -B script.py
```

> 什么？你不想看到满桌子的 `__pycache__` 文件夹？`-B` 就是你的清洁工！

#### 10.1.7.2 -v：verbose，详细输出导入信息

```bash
python -v script.py
```

这会打印出每一个模块导入的详细信息。输出超级多，但超级有用——当你不知道为什么程序找不到某个模块的时候，用 `-v` 看看它到底在哪些路径里翻箱倒柜：

```
import 'sys' # <_frozen_importlib.SourceFileLoader...>
import 'os' # <_frozen_importlib.SourceFileLoader...>
# ... 一大堆 ...
```

#### 10.1.7.3 -W：Warning 控制

Python 的警告（Warning）控制系统，有时候警告太多烦死人，可以用 `-W` 来过滤：

```bash
python -W ignore script.py          # 忽略所有警告
python -W error script.py           # 把警告当错误处理
python -W default script.py         # 默认行为
python -W ignore::DeprecationWarning script.py  # 只忽略特定警告
```

> 实用场景：很多库会抛出 FutureWarning 或 DeprecationWarning，但你暂时不想管。加 `-W ignore` 眼不见为净！

---

## 10.2 命令行参数解析

现在你的脚本可以运行了。但问题是：如果你的脚本需要接收用户输入的文件名、开关选项、数字参数呢？你总不能每次都改代码吧！

这就要说到命令行参数解析了。

### 10.2.1 sys.argv：最原始的参数获取

`sys.argv` 是最简单、最直接的方式，就像用筷子吃饭——能吃饱，但不够优雅。

#### 10.2.1.1 sys.argv[0] 是脚本名，sys.argv[1:] 是参数

```python
# greet.py
import sys

print(f"脚本自己叫：{sys.argv[0]}")           # 脚本名
print(f"参数列表是：{sys.argv[1:]}")           # 所有参数
print(f"第一个参数是：{sys.argv[1] if len(sys.argv) > 1 else '没有！'}")

# 用循环打印每个参数
for i, arg in enumerate(sys.argv):
    print(f"  argv[{i}] = {arg}")
```

运行：

```bash
python greet.py Alice 42 "Hello World"
```

输出：

```
脚本自己叫：greet.py
参数列表是：['Alice', '42', 'Hello World']
第一个参数是：Alice
  argv[0] = greet.py
  argv[1] = Alice
  argv[2] = 42
  argv[3] = Hello World
```

> 小问题：`sys.argv` 的返回值都是**字符串**！所以 `42` 你拿到手是 `'42'`，不是 `42`，需要自己转换类型。

```python
age = int(sys.argv[1])  # 字符串转整数
```

> 缺点：没有帮助信息，没有类型检查，没有默认值，没有 `-h` 自动生成使用说明。用 `sys.argv` 就是自己手工切菜——可以，但不是大厨的做法。

### 10.2.2 argparse：标准库完整参数解析

`argparse` 是 Python 标准库，专门用来处理命令行参数。用它你可以轻松做出专业的 CLI 工具——带帮助信息、类型检查、默认值、子命令，应有尽有。

#### 10.2.2.1 基础用法

```python
# basic_argparse.py
import argparse

# 创建解析器
parser = argparse.ArgumentParser(description="这是一个演示程序")

# 添加参数
parser.add_argument("name", help="你的名字")
parser.add_argument("--age", type=int, default=18, help="你的年龄（默认18）")
parser.add_argument("-v", "--verbose", action="store_true", help="显示详细信息")

# 解析参数
args = parser.parse_args()

print(f"你好，{args.name}！")
print(f"你{args.age}岁了。")
if args.verbose:
    print("（这是详细信息：程序运行成功！）")
```

运行看看：

```bash
python basic_argparse.py --help
```

```
usage: basic_argparse.py [-h] [--age AGE] [-v] name

这是一个演示程序

positional arguments:
  name            你的名字

options:
  -h, --help      显示帮助信息
  --age AGE       你的年龄（默认18）
  -v, --verbose   显示详细信息
```

```bash
python basic_argparse.py 小明 --age 20 -v
```

```
你好，小明！
你20岁了。
（这是详细信息：程序运行成功！）
```

> 小知识：`--help` 是自动生成的！`argparse` 会根据你的参数定义自动生成使用说明和帮助文档，不用你手动写。

#### 10.2.2.2 add_argument 参数详解

`add_argument` 是 `argparse` 的核心，参数超级多：

| 参数 | 说明 | 示例 |
|------|------|------|
| `name` | 位置参数名 | `parser.add_argument("file")` |
| `--name` | 可选参数 | `parser.add_argument("--input", "-i")` |
| `type` | 参数类型 | `type=int`, `type=float`, `type=open` |
| `default` | 默认值 | `default=0` |
| `help` | 帮助说明 | `help="输入文件路径"` |
| `required` | 是否必填 | `required=True` |
| `choices` | 限定选项 | `choices=["A", "B", "C"]` |
| `action` | 动作 | `store_true`（开关） |
| `nargs` | 参数个数 | `nargs="*"`（任意多个），`nargs="?"`（0或1个），`nargs="+"`（至少1个） |

```python
# argument_demo.py
import argparse

parser = argparse.ArgumentParser(description="参数类型演示")

# 位置参数（必需）
parser.add_argument("filename", help="输入文件名")

# 带短选项的可选参数
parser.add_argument("-n", "--number", type=int, default=10, help="重复次数")

# 带限定选项的参数
parser.add_argument("-m", "--mode", choices=["easy", "normal", "hard"], default="normal", help="难度模式")

# 开关参数（不需要值，指定了就是 True）
parser.add_argument("-q", "--quiet", action="store_true", help="安静模式")

# 可变次数参数
parser.add_argument("files", nargs="*", help="多个文件")

args = parser.parse_args()

print(f"主文件：{args.filename}")
print(f"重复次数：{args.number}")
print(f"难度：{args.mode}")
print(f"安静模式：{args.quiet}")
print(f"其他文件：{args.files}")
```

```bash
python argument_demo.py data.txt -n 5 --mode hard file2.txt file3.txt
```

```
主文件：data.txt
重复次数：5
难度：hard
安静模式：False
其他文件：['file2.txt', 'file3.txt']
```

#### 10.2.2.3 互斥组配置

有些参数不能同时使用，比如"显示版本"和"输入模式"——这就叫互斥组（Mutually Exclusive Group）。

```python
# mutex_demo.py
import argparse

parser = argparse.ArgumentParser(description="互斥组演示")

group = parser.add_mutually_exclusive_group()
group.add_argument("-v", "--verbose", action="store_true", help="详细输出")
group.add_argument("-q", "--quiet", action="store_true", help="安静模式")

args = parser.parse_args()

if args.verbose:
    print("详细模式已开启")
elif args.quiet:
    print("安静模式已开启")
else:
    print("普通模式")
```

```bash
python mutex_demo.py -v      # 详细模式已开启
python mutex_demo.py -q      # 安静模式已开启
python mutex_demo.py -v -q   # 错误：不能同时指定 -v 和 -q
```

```
error: argument -q/--quiet: not allowed with argument -v/--verbose
```

#### 10.2.2.4 子命令配置

大项目通常有子命令，像 `git commit`、`git push`、`git pull` 那样。`argparse` 也支持！

```python
# subcommand_demo.py
import argparse

parser = argparse.ArgumentParser(description="文件处理工具")
subparsers = parser.add_subparsers(dest="command", help="子命令")

# 子命令：压缩
compress_parser = subparsers.add_parser("compress", help="压缩文件")
compress_parser.add_argument("input", help="输入文件")
compress_parser.add_argument("-o", "--output", default="output.zip", help="输出文件")

# 子命令：解压
extract_parser = subparsers.add_parser("extract", help="解压文件")
extract_parser.add_argument("file", help="压缩包")
extract_parser.add_argument("-d", "--dir", default=".", help="解压目录")

args = parser.parse_args()

if args.command == "compress":
    print(f"正在压缩 {args.input} -> {args.output}")
elif args.command == "extract":
    print(f"正在解压 {args.file} 到 {args.dir}")
else:
    parser.print_help()
```

```bash
python subcommand_demo.py compress bigfile.txt -o myfile.zip
# 正在压缩 bigfile.txt -> myfile.zip

python subcommand_demo.py extract myfile.zip -d ./output
# 正在解压 myfile.zip 到 ./output

python subcommand_demo.py --help
```

```
usage: file_tool.py [-h] {compress,extract} ...

positional arguments:
  {compress,extract}  子命令
    compress          压缩文件
    extract           解压文件
```

### 10.2.3 click：命令行界面构建框架

`argparse` 很强大，但写起来还是有点繁琐。`click` 是一个更优雅的 CLI 构建库，它用装饰器（Decorator）让代码更简洁、更易读。

#### 10.2.3.1 安装

```bash
pip install click
```

#### 10.2.3.2 @click.command() 和 @click.option()

```python
# click_demo.py
import click

@click.command()                    # 标记这是命令
@click.option("-n", "--name", default="世界", help="打招呼的对象")
@click.option("-c", "--count", default=1, type=int, help="重复次数")
def hello(name, count):
    """这是一个演示 Click 的简单程序"""
    for i in range(count):
        click.echo(f"你好，{name}！")  # click.echo 自动处理编码问题

if __name__ == "__main__":
    hello()
```

```bash
python click_demo.py --help
```

```
Usage: click_demo.py [OPTIONS]

  这是一个演示 Click 的简单程序

Options:
  -n, --name TEXT    打招呼的对象  [default: 世界]
  -c, --count INTEGER  重复次数  [default: 1]
  --help            显示帮助
```

```bash
python click_demo.py -n 小明 -c 3
```

```
你好，小明！
你好，小明！
你好，小明！
```

> 小知识：为什么要用 `click.echo` 而不是 `print`？因为 `print` 在某些 Windows 环境下可能有编码问题，而且 `click.echo` 会自动处理不同平台的换行符。

#### 10.2.3.3 参数类型

click 支持多种参数类型：

```python
# click_types.py
import click
import os

@click.command()
@click.argument("filename", type=click.Path(exists=True))      # 文件路径（可检查是否存在）
@click.argument("number", type=click.INT)                        # 整数
@click.argument("ratio", type=click.FLOAT)                      # 浮点数
@click.argument("mode", type=click.Choice(["A", "B", "C"]))      # 选择
def process(filename, number, ratio, mode):
    click.echo(f"文件：{filename}")
    click.echo(f"数字：{number} (类型：{type(number).__name__})")
    click.echo(f"比例：{ratio}")
    click.echo(f"模式：{mode}")

if __name__ == "__main__":
    process()
```

```bash
# 假设当前目录有 test.txt
python click_types.py test.txt 42 3.14 A
```

```
文件：test.txt
数字：42 (类型：int)
比例：3.14
模式：A
```

#### 10.2.3.4 命令组

和 argparse 的子命令类似，click 也有命令组：

```python
# click_commands.py
import click

@click.group()  # 创建命令组
def cli():
    """文件处理工具集"""
    pass

@cli.command()  # 添加子命令
@click.argument("filename")
def compress(filename):
    """压缩文件"""
    click.echo(f"正在压缩 {filename}...")

@cli.command()
@click.argument("filename")
def extract(filename):
    """解压文件"""
    click.echo(f"正在解压 {filename}...")

@cli.command()
@click.argument("filename")
def info(filename):
    """查看文件信息"""
    click.echo(f"文件信息：{filename}")

if __name__ == "__main__":
    cli()
```

```bash
python click_commands.py --help
```

```
Usage: click_commands.py [OPTIONS] COMMAND [ARGS]...

  文件处理工具集

Commands:
  compress   压缩文件
  extract    解压文件
  info       查看文件信息
```

```bash
python click_commands.py compress bigfile.zip
# 正在压缩 bigfile.zip...
```

### 10.2.4 Typer（Click 进阶版，FastAPI 团队出品）

Typer 是基于 Click 开发的，语法更简洁，特别适合已经熟悉 Python 类型提示的人。

#### 10.2.4.1 安装

```bash
pip install typer
```

#### 10.2.4.2 @app.command()

```python
# typer_demo.py
import typer

app = typer.Typer()

@app.command()
def greet(name: str = "世界", times: int = 1):
    """打招呼程序"""
    for _ in range(times):
        typer.echo(f"你好，{name}！")

if __name__ == "__main__":
    app()
```

```bash
python typer_demo.py --help
```

```
Usage: typer_demo.py [OPTIONS] NAME [TIMES]

  打招呼程序

Arguments:
  name  [default: 世界]
  times  [default: 1]

Options:
  --help  显示帮助
```

```bash
python typer_demo.py 小明 3
```

```
你好，小明！
你好，小明！
你好，小明！
```

> 小知识：Typer 利用了 Python 3.6+ 的类型提示（Type Hints）功能。参数类型直接写在函数签名里，不用额外配置，Typer 自动帮你生成 CLI 参数类型。代码即配置，简洁到飞起！

#### 10.2.4.3 自动生成 CLI 文档

Typer 能自动生成 Bash 和 Fish 的自动补全脚本：

```python
# typer_completion.py
import typer

app = typer.Typer()

@app.command()
def run(name: str):
    typer.echo(f"运行 {name}...")

if __name__ == "__main__":
    app()
```

```bash
# 生成 Bash 补全脚本
typer --install-completion typer_completion.py
```

> 这个功能对于写给团队使用的工具来说特别有用——有了自动补全，用户体验直接提升一个档次！

### 10.2.5 fire：自动生成 CLI

Google 出品的 fire 更激进——它可以自动把任何 Python 程序、函数、类生成 CLI，完全零配置！

#### 10.2.5.1 安装

```bash
pip install fire
```

#### 10.2.5.2 任何 Python 函数自动生成 CLI

```python
# fire_demo.py
import fire

def greet(name="世界", times=1):
    """打招呼函数"""
    for i in range(times):
        print(f"你好，{name}！（第{i+1}次）")

def add(a=0, b=0):
    """加法函数"""
    return a + b

class Calculator:
    """计算器类"""
    def add(self, a, b):
        return a + b
    
    def multiply(self, a, b):
        return a * b

if __name__ == "__main__":
    fire.fire()
```

```bash
# 直接运行模块
python fire_demo.py greet --name 小明 --times 3
```

```
你好，小明！（第1次）
你好，小明！（第2次）
你好，小明！（第3次）
```

```bash
# 调用函数
python fire_demo.py add --a 10 --b 20
# 30
```

```bash
# 使用类
python fire_demo.py Calculator.multiply --a 6 --b 7
# 42
```

```bash
# 查看帮助
python fire_demo.py --help
```

> fire 的哲学：**最少的代码，最大的效果**。你不需要额外写任何 CLI 代码，只要导入 fire，调用 `fire.fire()`，它就会自动把你定义的所有函数、类生成命令行工具。懒人必备！

---

## 10.3 打包为可执行文件

好了，现在你能熟练运行和配置 Python 代码了。但问题是——**你的用户可能连 Python 都没安装**。总不能让大妈运行 `pip install numpy` 吧？

这时候就需要把 Python 代码打包成可执行文件（.exe），让任何人都能双击运行！

### 10.3.1 PyInstaller：跨平台打包

PyInstaller 是最流行的 Python 打包工具，能把 Python 程序打包成单个可执行文件或整个目录。

#### 10.3.1.1 安装

```bash
pip install pyinstaller
```

#### 10.3.1.2 基本打包命令

先写一个简单的程序：

```python
# hello_packaged.py
import sys

def main():
    print("=" * 50)
    print("  🎉 恭喜！打包成功！")
    print("=" * 50)
    print(f"Python 版本：{sys.version}")
    print(f"当前平台：{sys.platform}")
    print("现在你可以把这个程序发给任何人了！")
    print("（只要他们的电脑能跑 Windows/Mac/Linux 就行）")

if __name__ == "__main__":
    main()
```

##### 10.3.1.2.1 --onefile 单文件模式

打包成**单个文件**：

```bash
pyinstaller --onefile hello_packaged.py
```

打包完成后，`dist/` 目录下会出现一个 `hello_packaged.exe`（Windows）或 `hello_packaged`（Linux/Mac）。

> 优点：只有一个文件，方便分发。
> 缺点：启动较慢，因为每次运行都要先解压。

##### 10.3.1.2.2 --onedir 目录模式

打包成**整个目录**：

```bash
pyinstaller --onedir hello_packaged.py
```

`dist/hello_packaged/` 目录下会有：
- 主程序（`hello_packaged.exe`）
- 依赖的 DLL 和资源文件
- Python 运行时

> 优点：启动快。
> 缺点：文件多，散落一地。

#### 10.3.1.3 图标配置

给程序加个图标，看起来更专业！

```bash
pyinstaller --onefile --icon=myapp.ico hello_packaged.py
```

> 图标格式要求：
> - Windows: `.ico` 格式
> - Linux: `.png` 或 `.ico`
> - macOS: `.icns` 格式

没有图标？可以去 [iconifier.net](https://iconifier.net) 或 [favicon.io](https://favicon.io/) 之类的网站生成。

#### 10.3.1.4 隐藏依赖配置

有些库（比如 `torch`、`tensorflow`、`cv2`）在导入时非常隐蔽，PyInstaller 看不到它们的依赖关系。这时候需要手动指定。

```bash
pyinstaller --onefile --hidden-import=sklearn hello.py
```

多个隐藏依赖：

```bash
pyinstaller --onefile \
    --hidden-import=numpy.core._multiarray_umath \
    --hidden-import=sklearn \
    --hidden-import=cv2 \
    hello.py
```

#### 10.3.1.5 spec 文件详解

PyInstaller 的配置都存在 `.spec` 文件里。第一次打包会自动生成，之后你可以手动编辑它。

```python
# hello.spec
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['hello_packaged.py'],           # 主脚本
    pathex=[],                        # 额外搜索路径
    binaries=[],                      # 二进制文件
    datas=[('assets/', 'assets/')],   # 附加数据文件
    hiddenimports=[],                 # 隐藏导入
    hookspath=[],                     # hook 路径
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],                      # 排除的模块
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='hello_packaged',            # 输出文件名
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,                    # True=有黑窗口，False=无黑窗口（GUI程序）
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='myapp.ico'                  # 图标
)
```

打包命令：

```bash
pyinstaller hello.spec
```

##### 10.3.1.5.1 Analysis、PYZ、EXE、COLLECT 阶段

PyInstaller 打包分四个阶段：

```mermaid
flowchart LR
    A["源文件<br/>hello.py"] --> B["Analysis<br/>分析阶段"]
    B --> C["PYZ<br/>压缩阶段"]
    C --> D["EXE<br/>生成可执行文件"]
    D --> E["COLLECT<br/>收集资源"]
    E --> F["dist/<br/>最终产物"]
```

| 阶段 | 类 | 作用 |
|------|-----|------|
| **Analysis** | `Analysis` | 分析脚本，递归找出所有导入的模块 |
| **PYZ** | `PYZ` | 把所有 Python 模块压缩成 `.pz` 格式 |
| **EXE** | `EXE` | 生成最终的可执行文件 |
| **COLLECT** | `COLLECT` | 收集资源文件（图片、配置文件等）|

##### 10.3.1.5.2 datas 配置

如果你的程序需要读取外部文件（图片、配置、音频等），需要用 `datas` 配置把它们打包进去：

```python
a = Analysis(
    ['hello.py'],
    datas=[
        ('./config.json', 'config/'),      # 把 config.json 放到 config/ 目录
        ('./images/*.png', 'images/'),       # 把所有 png 放到 images/ 目录
        ('./assets', 'assets'),              # 把整个 assets 目录放进去
    ],
    ...
)
```

运行时读取：

```python
import sys
import os

# 获取资源文件路径（打包后也能正常工作）
def resource_path(relative_path):
    if getattr(sys, 'frozen', False):  # 打包后
        base_path = sys._MEIPASS
    else:  # 开发时
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

# 使用
config_path = resource_path('config/config.json')
with open(config_path, 'r') as f:
    config = f.read()
```

##### 10.3.1.5.3 hiddenimports 配置

当代码使用 `importlib`、`plugins`、`__getattr__` 等动态导入时，PyInstaller 可能会漏掉某些依赖，需要手动声明：

```python
a = Analysis(
    ['hello.py'],
    hiddenimports=[
        'numpy',
        'sklearn',
        'my_custom_module',
    ],
    ...
)
```

#### 10.3.1.6 常见问题与解决

**问题一：打包后运行报错 "Failed to execute script"**

```bash
# 加上 --console 和 --debug 重新打包，看具体错误
pyinstaller --console --debug=imports hello.py
```

常见原因：
- 缺少 `--hidden-import`（漏掉了动态导入的模块）
- `datas` 配置不对（找不到资源文件）
- 编码问题（Windows 控制台默认 GBK）

**问题二：打包后文件太大**

```bash
# 排除不需要的模块
pyinstaller --onefile --exclude-module tkinter hello.py
```

或者用虚拟环境只安装需要的包：

```bash
python -m venv myenv
myenv\Scripts\activate
pip install pyinstaller
pip install your-package
pyinstaller --onefile hello.py
```

**问题三：Windows 下打包有黑色控制台窗口**

GUI 程序不需要黑窗口：

```bash
pyinstaller --onefile --windowed hello.py
# 或
pyinstaller --onefile --noconsole hello.py
```

**问题四：杀毒软件报毒**

打包后的 .exe 是从零开始生成的，杀毒软件不认识它，就可能报警。这是正常现象（尤其是加了 UPX 压缩的）。

解决：
- 申请代码签名证书，给 exe 签名
- 提交给杀毒软件厂商白名单（如 Microsoft SmartScreen）
- 使用开源打包工具（PyInstaller 本身是开源的，可以审查代码）

### 10.3.2 Nuitka：将 Python 编译为 C 再编译为可执行文件

PyInstaller 是"打包"，Nuitka 是"编译"。Nuitka 把 Python 代码编译成 C 代码，再用 C 编译器编译成机器码——性能更高！

#### 10.3.2.1 安装

```bash
pip install nuitka
```

#### 10.3.2.2 基本命令

```bash
# 单文件模式
nuitka --standalone --onefile hello.py

# 输出：hello.exe
```

#### 10.3.2.3 性能优化选项

```bash
# 启用所有优化
nuitka --standalone --onefile --optimize=3 hello.py

# --remove-output 完成后删除中间文件
# --lint 启用代码检查
# --python-flag=no_site 排除 site-packages（减小体积）
```

#### 10.3.2.4 C 编译器选择

Nuitka 需要 C 编译器：

| 系统 | 编译器 |
|------|--------|
| Windows | MinGW64（会自动下载）或 MSVC |
| Linux | gcc |
| macOS | clang |

```bash
# 指定使用 MSVC
nuitka --standalone --onefile --msvc=latest hello.py

# 指定使用 MinGW
nuitka --standalone --onefile --mingw64=on hello.py
```

#### 10.3.2.5 Nuitka vs PyInstaller vs cx_Freeze 对比

| 特性 | PyInstaller | Nuitka | cx_Freeze |
|------|-------------|--------|-----------|
| 原理 | 打包字节码 | 编译成 C | 打包字节码 |
| 性能 | 解释执行 | 编译执行 | 解释执行 |
| 体积 | 较大 | 中等 | 中等 |
| 启动速度 | 慢（单文件需解压） | 快 | 中等 |
| 代码保密 | 差（.pyz 可解压） | 好（编译后难以反编译）| 差 |
| 依赖管理 | 手动配置 | 自动检测 | 需配置 |
| 学习曲线 | 低 | 中 | 低 |
| 适用场景 | 快速分发 | 追求性能/保密 | 跨平台分发 |

> 选择建议：
> - 快速分享给不懂技术的用户 → **PyInstaller**
> - 追求运行性能或代码保密 → **Nuitka**
> - 需要跨平台（Windows/Mac/Linux）统一打包 → **cx_Freeze** 或 **PyInstaller**

### 10.3.3 cx_Freeze：跨平台打包

cx_Freeze 又是一个打包工具，语法和 PyInstaller 类似。

#### 10.3.3.1 安装

```bash
pip install cx_Freeze
```

#### 10.3.3.2 setup.py 配置

```python
# setup.py
from cx_Freeze import setup, Executable

build_exe_options = {
    "packages": ["numpy", "pandas"],        # 要包含的包
    "excludes": ["tkinter"],                # 排除的包
    "include_files": [("config.json", "config.json")],  # 附加文件
}

setup(
    name="HelloApp",
    version="1.0",
    description="我的第一个打包应用",
    options={"build_exe": build_exe_options},
    executables=[
        Executable(
            "hello.py",
            base="Win32GUI",   # Windows 下设为 Win32GUI 就没有控制台窗口
            icon="myapp.ico",
            target_name="HelloApp.exe"
        )
    ]
)
```

打包：

```bash
python setup.py build
```

输出在 `build/` 目录下。

### 10.3.4 briefcase：BeeWare 项目打包工具

briefcase 是 [BeeWare](https://beeware.org/) 项目的一部分，主要用于打包 Python 应用到各个平台。

#### 10.3.4.1 安装

```bash
pip install briefcase
```

#### 10.3.4.2 支持平台

| 平台 | 输出格式 |
|------|---------|
| Windows | `.msi` 安装包 / `.exe` |
| macOS | `.app` 应用 / `.dmg` 安装包 |
| Linux | `.deb`, `.rpm`, `.appimage` |
| iOS | ~~Xcode 项目~~（已弃用，BeeWare 目前暂停了 iOS 支持） |
| Android | APK（通过 Python 标准库）|

```bash
# 创建项目
briefcase new
# 回答几个问题，项目就创建好了

# 打包
briefcase build windows    # Windows
briefcase build macOS      # macOS
briefcase build linux      # Linux
```

> briefcase 的特点是生成的应用程序看起来和原生应用一样（有自己的窗口、图标、菜单），而不是带黑窗口的控制台程序。如果你做的是 GUI 应用，briefcase 是很好的选择。

---

## 10.4 Python 包发布

现在你已经会打包了，接下来是——**把包发布到 PyPI，让全世界都能 `pip install 你的包`！**

> **PyPI**（Python Package Index）：Python 官方的第三方包仓库，类似 npm 之于 JavaScript，crates.io 之于 Rust。全世界的人都在这里分享自己的 Python 包。

### 10.4.1 setup.py / setup.cfg 详解

`setup.py` 是 Python 打包的"老前辈"，虽然新标准推荐用 `pyproject.toml`，但理解 setup.py 对了解打包历史很有帮助。

#### 10.4.1.1 setup() 函数参数详解

```python
# setup.py
from setuptools import setup, find_packages

setup(
    name="mypackage",                    # 包名（PyPI 上的名字）
    version="1.0.0",                     # 版本号
    author="张三",                        # 作者
    author_email="zhangsan@example.com", # 作者邮箱
    description="这是一个演示包",         # 简短描述（一行）
    long_description=open("README.md").read(),  # 详细描述（从 README 读取）
    long_description_content_type="text/markdown",  # README 格式
    url="https://github.com/zhangsan/mypackage",  # 项目地址
    packages=find_packages(),           # 自动找所有包
    classifiers=[                       # 分类标签
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",            # Python 版本要求
    install_requires=[                  # 运行时依赖
        "requests>=2.25.0",
        "numpy>=1.20.0",
    ],
)
```

#### 10.4.1.2 find_packages() 用法

`find_packages()` 会自动在当前目录下找所有包含 `__init__.py` 的目录，当作包：

```
mypackage/
├── __init__.py
├── module1.py
├── subpackage/
│   ├── __init__.py
│   └── module2.py
└── tests/
    ├── __init__.py
    └── test_module1.py
```

```python
from setuptools import find_packages

packages = find_packages(exclude=["tests*"])  # 排除 tests 目录
```

#### 10.4.1.3 install_requires 依赖声明

`install_requires` 声明的是**运行时依赖**，用户在 `pip install` 时会自动安装：

```python
install_requires=[
    "requests>=2.25.0",      # 大于等于某个版本
    "numpy>=1.20.0,<2.0.0", # 范围限定
    "colorama",              # 不限版本（用已安装的最新版）
]
```

可选依赖（用户需要时额外安装）：

```python
extras_require={
    "dev": ["pytest", "black", "flake8"],    # 开发依赖
    "doc": ["sphinx"],                        # 文档依赖
    "gpu": ["cupy-cuda11x"],                  # GPU 支持
}
```

用户安装方式：

```bash
pip install mypackage[dev]     # 安装 + 开发依赖
pip install mypackage[gpu]     # 安装 + GPU 支持
pip install mypackage[dev,gpu]  # 全都要
```

### 10.4.2 pyproject.toml：现代打包标准（PEP 517/518/621）

`pyproject.toml` 是现代 Python 打包的标准格式，取代了老旧的 `setup.py`。所有新项目都应该用它！

#### 10.4.2.1 [build-system] 构建系统配置

告诉 pip 使用什么工具来构建这个包：

```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]  # 构建依赖
build-backend = "setuptools.build_meta"   # 使用 setuptools 作为构建后端
```

#### 10.4.2.2 [project] 项目元数据配置

```toml
[project]
name = "mypackage"
version = "1.0.0"
description = "这是一个超棒的 Python 包"
readme = "README.md"                          # 详细描述从这里读取
requires-python = ">=3.8"                     # Python 版本要求
license = {text = "MIT"}                       # 许可证
authors = [
    {name = "张三", email = "zhangsan@example.com"}
]
keywords = ["demo", "example", "tutorial"]
classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
]

dependencies = [
    "requests>=2.25.0",
    "numpy>=1.20.0",
]
```

#### 10.4.2.3 [project.optional-dependencies] 可选依赖

```toml
[project.optional-dependencies]
dev = ["pytest", "black", "flake8"]
doc = ["sphinx", "sphinx-rtd-theme"]
gpu = ["cupy-cuda11x"]
```

#### 10.4.2.4 [project.scripts] 命令行入口

这是非常强大的功能——定义命令行入口，安装后用户可以直接在终端调用：

```toml
[project.scripts]
myapp = "mypackage.cli:main"          # 安装后：myapp 命令
greet = "mypackage.greet:main"        # 安装后：greet 命令
```

```python
# mypackage/cli.py
def main():
    print("Hello from myapp!")

# mypackage/greet.py
def main():
    print("Greetings!")
```

安装这个包后，用户就能直接运行 `myapp` 和 `greet` 命令了！

完整的 `pyproject.toml` 示例：

```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "mypackage"
version = "1.0.0"
description = "这是一个超棒的 Python 包"
readme = "README.md"
requires-python = ">=3.8"
license = {text = "MIT"}
authors = [{name = "张三", email = "zhangsan@example.com"}]
keywords = ["demo", "example"]
classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
]
dependencies = [
    "requests>=2.25.0",
    "numpy>=1.20.0",
]

[project.optional-dependencies]
dev = ["pytest", "black", "flake8"]

[project.scripts]
myapp = "mypackage.cli:main"
```

### 10.4.3 build 工具：打包

#### 10.4.3.1 安装

```bash
pip install build
```

#### 10.4.3.2 python -m build 生成 dist/ 目录

```bash
# 进入项目目录
cd myproject

# 清理旧构建
rm -rf dist build *.egg-info

# 构建
python -m build
```

构建完成后，`dist/` 目录下会有：

```
dist/
├── mypackage-1.0.0-py3-none-any.whl   # wheel 包（pip install 用这个）
└── mypackage-1.0.0.tar.gz             # 源码包
```

### 10.4.4 twine：安全上传到 PyPI

为什么不用 `python setup.py upload`？因为它是明文上传密码，极其不安全。twine 使用 HTTPS，更安全！

#### 10.4.4.1 安装

```bash
pip install twine
```

#### 10.4.4.2 twine upload 上传命令

```bash
# 上传到 PyPI
twine upload dist/*

# 上传到 Test PyPI（测试用）
twine upload --repository testpypi dist/*
```

#### 10.4.4.3 PyPI 账号和 API Token 配置

**第一步：去 PyPI.org 注册账号**

访问 https://pypi.org/account/register/，填写用户名、密码、邮箱。

**第二步：生成 API Token**

1. 登录 PyPI
2. 进入 Account Settings → API tokens
3. 点击 "Add API token"
4. 复制生成的 token（格式：`pypi-xxxxxxxxxxxx`）

**第三步：配置 ~/.pypirc**

在用户目录下创建或编辑 `.pypirc` 文件（Windows 是 `C:\Users\你的用户名\`）：

```ini
[pypi]
username = __token__
password = pypi-xxxxxxxxxxxx（你的 token）

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-xxxxxxxxxxxx（你的 test token）
```

> 小贴士：`username = __token__` 不是让你填用户名，而是字面量 `__token__`，密码才是你的 token。Token 本身就是密码的意思，这样设计更安全。

### 10.4.5 版本号管理

版本号不是随便写的，有一套标准叫 **语义化版本（Semantic Versioning）**。

#### 10.4.5.1 Semantic Versioning（语义化版本）

格式：`主版本.次版本.修订号`

```
1.0.0
 ↑ ↑ ↑
 | | └── 补丁版本：修复 bug，小改动
 | └──── 次版本：新增功能（向后兼容）
 └────── 主版本：不兼容的重大改动
```

| 场景 | 例子 |
|------|------|
| 首次发布 | 1.0.0 |
| 修复 bug | 1.0.1 |
| 新功能（向后兼容）| 1.1.0 |
| 破坏性更新 | 2.0.0 |

#### 10.4.5.2 Alpha / Beta / RC 版本标注

正式发布前，会有几个测试阶段：

| 阶段 | 标注 | 说明 |
|------|------|------|
| Alpha | `1.0.0a1` 或 `1.0.0a` | 内部测试版，很不稳定 |
| Beta | `1.0.0b1` 或 `1.0.0b` | 公开测试，功能差不多了 |
| Release Candidate | `1.0.0rc1` | 候选发布，大概率就是正式版了 |
| 正式版 | `1.0.0` | 稳定版 |

```toml
# pyproject.toml 中
version = "1.0.0a1"    # Alpha
version = "1.0.0b2"    # Beta
version = "1.0.0rc3"   # RC
version = "1.0.0"      # 正式版
```

### 10.4.6 发布到 Test PyPI

正式发布前，先去 Test PyPI 练练手，避免污染真实的 PyPI。

#### 10.4.6.1 --repository testpypi 配置

```bash
# 先注册 Test PyPI 账号（和 PyPI 分开的）
# https://test.pypi.org/account/register/

# 上传
twine upload --repository testpypi dist/*
```

#### 10.4.6.2 测试安装方式

```bash
# 从 Test PyPI 安装（需要指定 --index-url）
pip install --index-url https://test.pypi.org/simple/ mypackage

# 或者同时保留正常 PyPI 作为备用源
pip install mypackage \
    --index-url https://test.pypi.org/simple/ \
    --trusted-host test.pypi.org
```

### 10.4.7 自动发布

每次发布都要手动 `twine upload`？太累了！用 GitHub Actions 自动发布！

#### 10.4.7.1 GitHub Actions + PyPI 配置

在 GitHub 仓库里创建 `.github/workflows/release.yml`：

```yaml
name: Release

on:
  push:
    tags:
      - 'v*'        # 当推送 v 开头的标签时触发

jobs:
  build-and-publish:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: 设置 Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          
      - name: 安装依赖
        run: |
          python -m pip install --upgrade pip
          pip install build twine
          
      - name: 构建包
        run: python -m build
        
      - name: 发布到 PyPI
        env:
          TWINE_USERNAME: __token__
          TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}  # 在 GitHub 仓库设置里配置
        run: twine upload dist/*
```

然后：

1. 在 GitHub 仓库 → Settings → Secrets → Actions，添加 `PYPI_API_TOKEN`（值为 PyPI 的 API Token）
2. 推送一个 tag：

```bash
git tag v1.0.0
git push origin v1.0.0
```

GitHub Actions 会自动构建并发布到 PyPI！

---

## 10.5 分发依赖与环境

代码打包发布了，但如果别人想**开发**你的项目呢？或者你想在新电脑上继续开发？这就需要正确地分发和管理依赖。

### 10.5.1 requirements.txt 正确用法

`requirements.txt` 是 Python 项目最常用的依赖声明文件。

```txt
# requirements.txt
requests>=2.25.0
numpy>=1.20.0
pandas>=1.3.0
scikit-learn>=0.24.0
matplotlib>=3.4.0
```

安装：

```bash
pip install -r requirements.txt
```

> 格式说明：
> - `package` — 任意版本
> - `package==1.0.0` — 精确版本
> - `package>=1.0.0` — 最低版本要求
> - `package~=1.4.0` — 兼容版本（>=1.4.0, <1.5.0）
> - `package[extra]==1.0.0` — 带可选依赖

常见问题：requirements.txt 放在项目根目录：

```
myproject/
├── requirements.txt    # 在这里
├── README.md
├── pyproject.toml
└── src/
    └── mypackage/
```

### 10.5.2 pip freeze vs poetry export

**pip freeze** 把当前环境里所有包的精确版本导出：

```bash
pip freeze > requirements.txt
```

生成的格式：

```
certifi==2023.7.22
charset-normalizer==3.2.0
idna==3.4
numpy==1.24.3
requests==2.31.0
urllib3==2.0.4
```

> 优点：精确重现环境。
> 缺点：包含所有 transitive dependencies（传递依赖），比如 `certifi`、`idna` 这些你其实不需要关心的小包。

**poetry export** 是 Poetry 用户的专属，能导出兼容格式：

```bash
pip install poetry-plugin-export
poetry export -o requirements.txt --without-hashes
```

可以排除开发依赖：

```bash
poetry export -o requirements.txt --with dev  # 包含开发依赖
poetry export -o requirements.txt --without dev  # 不包含开发依赖
```

### 10.5.3 conda 环境导出与重建

如果你用的是 conda（Anaconda/Miniconda），依赖管理方式稍有不同：

**导出环境：**

```bash
conda env export > environment.yml
```

生成的 `environment.yml`：

```yaml
name: myenv
channels:
  - defaults
  - conda-forge
dependencies:
  - python=3.11
  - numpy=1.24.3
  - pandas=2.0.3
  - pip
  - pip:
    - some-pip-package==1.0.0
```

**重建环境：**

```bash
conda env create -f environment.yml
```

或者从零开始创建：

```bash
conda create -n myenv python=3.11 numpy pandas
conda activate myenv
```

> 小贴士：conda 和 pip 可以混合使用。conda 负责 conda 自己的包（编译好的二进制包），pip 负责 pip 包（纯 Python 包）。但要注意冲突检测——两边都装了同一个包的不同版本可能会出问题。

---

## 本章小结

### 核心要点回顾

1. **Python 代码运行方式**
   - `python script.py` 是最基础的运行方式
   - `python -m module` 以模块方式运行
   - `python -m package` 直接运行包（需要 `__main__.py`）
   - `-c` 参数可以直接运行字符串代码
   - `-i` 参数运行后进入交互模式
   - shebang 行 (`#!/usr/bin/env python3`) 让脚本可以直接执行

2. **命令行参数解析**
   - `sys.argv` 是最原始的方式，需要自己处理一切
   - `argparse` 是标准库，功能完整，适合复杂 CLI
   - `click` 用装饰器简化 CLI 开发，用户体验好
   - `typer` 基于 click，类型提示友好
   - `fire` 自动生成 CLI，零配置，适合原型开发

3. **打包为可执行文件**
   - **PyInstaller**：最流行，一行命令搞定，适合大多数场景
   - **Nuitka**：编译成 C，性能更好，代码更保密
   - **cx_Freeze**：跨平台，配置灵活
   - **briefcase**：BeeWare 生态，原生应用体验
   - 打包流程：`pyinstaller --onefile script.py` → `dist/` 下找 exe

4. **Python 包发布**
   - `setup.py` 是老方式，`pyproject.toml` 是现代标准
   - `build` 工具生成 wheel 和源码包
   - `twine` 安全上传到 PyPI
   - API Token 比密码更安全
   - Test PyPI 用来测试发布流程
   - GitHub Actions 可以自动化发布

5. **分发依赖与环境**
   - `requirements.txt` 是最通用的依赖声明方式
   - `pip freeze` 导出精确版本
   - `poetry export` 可以更智能地导出
   - conda 用 `environment.yml` 管理环境

### 实战路线图

```
写代码 → 命令行参数 → 打包 exe → 发布到 PyPI
           ↓              ↓            ↓
      argparse/click   PyInstaller   twine upload
```

记住：**能运行、能打包、能发布**，才是一个完整的 Python 项目闭环。你现在拥有了把代码送到全世界手上的能力！

> 下一步建议：选一个你自己的小项目，尝试用 PyInstaller 打包成 exe，或者发布到 Test PyPI 试试水。实战出真知！
