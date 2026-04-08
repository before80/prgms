+++
title = "第1章 欢迎来到Python的世界"
weight = 10
date = "2026-04-08T13:22:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 第一章：Python 的前世今生

> 本章将带你穿越时光隧道，从荷兰的某个小隔间出发，一路狂奔到 2025 年，看看 Python 是如何从一条"小蛇"长成一条吞天巨蟒的。我们会讲历史、聊八卦、挖坟技术，顺便让你明白为什么 Python 能让全世界的程序员都忍不住喊出"真香"。

---

# 1.1 Python 诞生背景

话说天下大势，分久必合，合久必分。20 世纪 80 年代末的编程语言江湖，正处于一个群雄并起的乱世——C 语言独领风骚，C++ 虎视眈眈，Pascal 余威尚存，而 Lisp 和 Scheme 这对函数式兄弟则在学术圈里自得其乐。

就在这看似岁月静好的表象下，一位荷兰程序员悄悄拿起了键盘……

## 1.1.1 创始人 Guido van Rossum 简介

![Guido van Rossum](https://upload.wikimedia.org/wikipedia/commons/6/66/Guido_van_Rossum_OSCON_2006.jpg)

**Guido van Rossum**（中文昵称"龟叔"），1956 年出生于荷兰小镇代尔夫特（Delft）。要说这哥们儿的人生有多离谱——他本来是个十足的数学爱好者，结果一头扎进了计算机的世界，最后还顺手创造了一门被全球数千万程序员使用的语言。

Guido 的履历表大概是这样的：

- **教育背景**：阿姆斯特丹大学数学和计算机科学双料硕士（这背景一看就是学霸）
- **职业生涯**：曾在荷兰 CWI 研究所、NASA（你没看错，就是那个 NASA）、Google、Dropbox、微软等公司工作
- **江湖地位**：Python 之父，BDFL（Benevolent Dictator For Life，终身仁慈独裁者）——这是程序员圈子里最霸气的 title，没有之一
- **花名**：除了"龟叔"，他还被戏称为"Python 之父"、"蟒蛇驯化师"，以及"那个让缩进变成语法的男人"

Guido 本人曾说过一句经典的话："我是在圣诞假期无聊的时候创造了 Python。"——这话听起来像是"我在百无聊赖中织了一件毛衣"，结果这件"毛衣"后来温暖了全世界的程序员。

> 彩蛋：Guido 在 Dropbox 工作期间，有一次内部调查显示公司 50% 的服务器端代码都是 Python 写的。这大概就是"我不是针对谁，我是说在座各位写的代码都是我的"的最佳诠释吧。

## 1.1.2 诞生时间：1991 年 12 月

1991 年 12 月，对于绝大多数人来说，可能只是一个普通的年末——苏联刚刚解体，美国正在打海湾战争，香港还没回归中国。

但对于编程语言历史来说，这是一个值得被铭记的时刻。

就在这个寒冷的冬日，Guido van Rossum 在 CWI（后面会详细介绍这个机构）正式发布了 **Python 0.9.0**。

如果要给这一刻加一个特效字幕，大概是：

```
                                _                              
                              /  \    🐍 Python 0.9.0 诞生！   
                         \   \__/                            
                          \__/                               
```

你可能会问：为什么是 0.9.0 而不是 1.0.0？答案很简单——Guido 觉得还没准备好，要先让社区试试水。这种"先发布再迭代"的思路，和互联网时代的 MVP（最小可行产品）不谋而合，Guido 领先了业界至少二十年。

## 1.1.3 诞生地点：荷兰 CWI（国家数学与计算机科学研究所）

**CWI** 的全称是 Centrum Wiskunde & Informatica，中文翻译过来是"国家数学与计算机科学研究所"。这名字听起来就很正经，确实，它就是一个正经的荷兰国家级研究机构。

CWI 位于荷兰阿姆斯特丹，成立于 1946 年，专门研究数学和计算机科学。你可以把 CWI 理解为荷兰的"中科院数学与计算机科学分院"。在这个机构里，诞生过不少改变世界的东西：

- **Algol 68** 编译器——编程语言史上的老祖宗之一
- **ABC 语言**——Python 的"前世情人"（后面会详细讲）
- **Python** ——今天的主角

Guido 在 CWI 工作期间，参与了 ABC 语言的开发。虽然 ABC 最终没能成为主流，但它为 Python 的诞生积累了宝贵的经验。所以下次你写 Python 代码时，可以心怀感激地想到：CWI，这个荷兰小院里，埋着 Python 的种子。

> 八卦：Guido 后来离开 CWI 去美国闯荡，但在 2013 年又回到了荷兰，加入了 Dropbox 的欧洲分部。他说："我只是想在家门口吃顿荷兰薯条。"——好吧，这是我自己脑补的，但荷兰薯条确实好吃。

## 1.1.4 起源语言：ABC 语言（Guido 参与过 ABC 语言开发）

在讲 ABC 语言之前，先科普一个冷知识：**Python 的基因里，有一半来自 ABC。**

ABC 是 CWI 在 1980 年代初期开发的一种教学语言。Guido 当时就参与了这个项目，负责一些模块和文档的工作。ABC 的设计目标是"让非程序员也能轻松学会编程"，它的语法简洁、优雅、没有分号和大括号，用缩进来表示代码块。

听起来很眼熟？没错，Python 继承了这些特性。

但 ABC 最终失败了，原因是多方面的：它太"理想主义"了——没有文件 I/O（不能读写文件！）、不能系统调用、甚至连错误信息都过于"友好"以至于程序员无法调试。

Guido 总结了 ABC 失败的经验教训，决定在 Python 中避免这些坑。他的思路大概是：

| ABC 的问题 | Python 的解决方案 |
|------------|------------------|
| 不能读写文件 | 内置 `open()` 函数，文件操作轻松愉快 |
| 没有系统调用 | `import` 模块，想调啥调啥 |
| 错误信息太模糊 | 异常机制，精确打击错误 |
| 不能扩展 | C API 敞开大门，随便折腾 |

所以 **Python 本质上是 ABC 的"修正版"**——Guido 从 ABC 的失败中汲取了教训，创造了一门真正能干活、能让程序员开心的语言。

这段历史告诉我们一个道理：失败是成功他妈，但前提是你得从失败里学到东西。

## 1.1.5 Python 名字的由来：Monty Python 的 Flying Circus

终于到了八卦时间！

你一定好奇：Python 明明是一种蛇的名字，为什么这门编程语言会叫"Python"？

答案要从 Guido 的私生活说起——他是一个 **Monty Python's Flying Circus**（蒙提·派森的飞行马戏团）的忠实粉丝。

Monty Python 是英国 BBC 的一档喜剧节目，1969 年首播，1974 年结束。这个节目有多火？火到 Guido 在 1991 年创造编程语言的时候，第一个想到的名字就是它。

Guido 本人在一次访谈中回忆说：

> "我想选一个简短、独特、略带神秘感的名字。我和同事们讨论过几个选项：'CPython'、'Magic'、'Boost'……最后我想到了 Monty Python，然后就觉得'Python'这个名字简直完美。"

所以你现在明白了——**Python 和蛇没有半毛钱关系**（至少在命名阶段没有）。蛇是后来才被附会上去的吉祥物logo。

> 等等，那我之前的"吞天巨蟒"形容是怎么回事？——那是 Python 发展壮大了之后的事了，马后炮式的联想而已。

Monty Python 的喜剧风格是荒诞、超现实、无厘头的。Python 语言的设计哲学里，其实也隐隐约约有这种气质——比如"应该有且仅有一种显而易见的实现方式"（虽然后来被各种奇技淫巧打脸），比如错误信息要友好，比如代码要优雅。

如果你想了解 Monty Python，建议去看看《The Ministry of Silly Walks》（愚蠢走路的部门），保证笑到肚子疼。

## 1.1.6 Python 的设计哲学：简洁、易读、可扩展

Guido 在设计 Python 之初，就定下了三条核心原则：

**1. 简洁（Simple）**
Python 的语法简单到了令人发指的地步。打印一个"Hello, World"只需要一行：

```python
print("Hello, World")  # Hello, World
```

对比一下 C 语言的"Hello, World"：

```c
#include <stdio.h>

int main() {
    printf("Hello, World\n");
    return 0;
}
```

没有比较就没有伤害——Python 让你专注于"说什么"，而不是"怎么说"。

**2. 易读（Readable）**
Python 代码读起来就像伪代码（pseudo-code）。看一下这个例子：

```python
# 判断一个数是不是质数
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

print(is_prime(17))  # True
```

就算你没学过 Python，光靠猜也能看懂这段代码在干什么。这就是"可读性"的力量。

**3. 可扩展（Extensible）**
Python 底层是用 C 写的，所以你可以用 C 或 C++ 编写扩展模块，Python 代码可以直接调用。想象一下，你用 Python 写业务逻辑，用 C 写性能关键代码，两全其美。

> 彩蛋：Python 还有一个著名的**"电池包含"**（Batteries Included）哲学——Python 解释器自带的标准库非常丰富，号称"安装即用"。这和某些语言" Hello World 都要先装三个包"形成了鲜明对比。

---

# 1.2 Python 发展史关键里程碑

## 1.2.1 Python 0.9.0（1991 年）—— 出生

1991 年 12 月，Python 0.9.0 正式发布！这是一个值得所有 Python 程序员纪念的日子——就像人类第一次登月一样，只不过 Python 登的是"编程语言之月"。

### 1.2.1.1 类（class）的引入

Python 0.9.0 就已经支持**面向对象编程**（Object-Oriented Programming，简称 OOP）的核心概念——类（class）。

什么是类？类就是一种"把数据和操作数据的方法打包在一起"的机制。你可以把它理解为一个"模具"，用模具可以批量生产"对象"（instance）。

```python
# 定义一个类
class Dog:
    def __init__(self, name):  # 构造函数，创建对象时自动调用
        self.name = name       # self 就是"这个对象本身"
    
    def bark(self):            # 方法（method），类里面的函数
        print(f"{self.name} 说：汪汪汪！")

# 创建一个 Dog 类的对象（实例化）
d = Dog("旺财")
d.bark()  # 旺财 说：汪汪汪！
```

在当时，大多数脚本语言（如 Perl、Bash）都不支持面向对象，Python 0.9.0 能做到这一点，确实很有远见。

### 1.2.1.2 异常处理（try/except）

**异常处理**（Exception Handling）是一种"出错了怎么办"的机制。传统的做法是检查返回值，但这种方式既繁琐又容易遗漏。Python 借鉴了 ABC 语言的异常机制，引入了 `try/except` 语法：

```python
try:
    result = 10 / 0  # 除以零会触发 ZeroDivisionError
except ZeroDivisionError:
    print("哎呀，除数不能为零！")  # 哎呀，除数不能为零！
```

这段代码里，`try` 块里放的是"可能出错"的代码，`except` 块里放的是"出错后怎么办"。

> 为什么要用异常而不是检查返回值？想象一下：如果每次调用函数都要检查返回值，代码会变成什么样？——大概会和金字塔一样高。

### 1.2.1.3 函数（def）

**函数**（Function）是组织代码的基本单元。把一段逻辑封装成函数，给它起个名字，以后想用这段逻辑就直接"叫名字"。

```python
def greet(name):
    """这是一个问候函数"""
    return f"你好，{name}！欢迎学习 Python！"

print(greet("小明"))  # 你好，小明！欢迎学习 Python！
```

`def` 是"define"（定义）的缩写，非常直观。在 Python 里，函数是一等公民（first-class citizen）——也就是说，函数可以赋值给变量、作为参数传递、从函数里返回。这为后面的装饰器（decorator）和函数式编程埋下了伏笔。

### 1.2.1.4 列表（list）、字符串、格式化

Python 的**列表**（list）是一种动态数组，可以存储任意类型的数据：

```python
fruits = ["苹果", "香蕉", "樱桃"]  # 创建列表
fruits.append("橙子")             # 添加元素
print(fruits[0])                   # 苹果（索引从0开始）
print(fruits[-1])                  # 橙子（负索引从后往前数）
```

**字符串**（string）则提供了丰富的操作方法：

```python
s = "Hello, Python!"
print(s.upper())      # HELLO, PYTHON!（转大写）
print(s.replace("Python", "World"))  # Hello, World!
print(s.split(","))   # ['Hello', ' Python!']（按分隔符拆分成列表）
```

**字符串格式化**（String Formatting）允许把变量嵌入到字符串里：

```python
name = "小明"
age = 8
# 方式1：f-string（Python 3.6+，最推荐）
print(f"我叫{name}，今年{age}岁")  # 我叫小明，今年8岁

# 方式2：format 方法
print("我叫{}，今年{}岁".format(name, age))  # 我叫小明，今年8岁

# 方式3：% 格式化（Python 2 风格，老派但还有人用）
print("我叫%s，今年%d岁" % (name, age))  # 我叫小明，今年8岁
```

### 1.2.1.5 模块系统（import）

**模块**（module）就是"把代码分文件存放"的机制。你可以把相关的函数、类、常量放到一个 `.py` 文件里，然后其他文件通过 `import` 来使用它。

```python
# 新建一个文件叫 utils.py，内容如下：
# def add(a, b):
#     return a + b

# 在另一个文件里使用：
import utils

result = utils.add(1, 2)
print(result)  # 3
```

Python 还有一个强大的**标准库**（Standard Library），就是安装 Python 时自带的那些模块。比如 `math` 模块提供数学函数，`random` 模块提供随机数功能：

```python
import math
import random

print(math.pi)          # 3.141592653589793
print(math.sqrt(16))    # 4.0
print(random.randint(1, 10))  # 随机整数，1到10之间
```

> 小结：Python 0.9.0 虽然是"出生版"，但已经具备了类、异常处理、函数、列表、字符串格式化和模块系统这些核心特性。这就好比一个婴儿出生时就已经包含了未来长大的所有基因——不愧是天选之子。

---

## 1.2.2 Python 1.0（1994 年）—— 函数式特性加入

1994 年 1 月，Python 1.0 正式发布。从 0.9.0 到 1.0，花了大约三年时间——主要是 Guido 在不断完善语言特性，同时还要应付日常工作。

这一版本最大的亮点是引入了**函数式编程**（Functional Programming，简称 FP）的一些特性。函数式编程是一种"像数学函数一样写代码"的编程范式——没有副作用，函数只依赖输入，输出完全可预测。

### 1.2.2.1 lambda 表达式

**lambda** 表达式就是"匿名函数"——一种不需要命名、直接定义的函数。它通常用在需要函数作为参数的场合。

```python
# 普通函数
def square(x):
    return x * x

# lambda 表达式，等价于上面的函数
square = lambda x: x * x

print(square(5))  # 25
```

lambda 的语法是：`lambda 参数: 返回值`

它为什么叫 lambda？这要追溯到 Lisp 语言，Lisp 用 lambda 表示匿名函数，而 lambda 来自数学里的 λ 演算——这是一个很深奥的概念，你可以简单理解为"一个表示函数的希腊字母"。

### 1.2.2.2 map()、filter()、reduce()

这三个函数是函数式编程的经典工具，在 Python 1.0 中作为内置函数引入（`reduce` 在 Python 3 中被移至 functools 模块）。

- **`map()`**：对序列中的每个元素执行某个操作，返回迭代器

```python
numbers = [1, 2, 3, 4, 5]

# 把每个数平方
squared = list(map(lambda x: x * x, numbers))
print(squared)  # [1, 4, 9, 16, 25]
```

- **`filter()`**：筛选序列中满足条件的元素

```python
# 筛选偶数
evens = list(filter(lambda x: x % 2 == 0, numbers))
print(evens)  # [2, 4]
```

- **`reduce()`**：对序列中的元素进行累积操作（在 Python 3 中移至 functools 模块）

```python
from functools import reduce

# 计算阶乘：1*2*3*4*5
product = reduce(lambda x, y: x * y, [1, 2, 3, 4, 5])
print(product)  # 120
```

> 不过实话实说，现在 Python 社区更推荐用**列表推导式**（List Comprehension）来做这些事情，因为更直观、更 Pythonic。关于列表推导式，我们后面讲 Python 2.0 时会详细介绍。

### 1.2.2.3 复数支持

**复数**（Complex Number）就是形如 `a + bi` 的数，其中 `i` 是虚数单位，`i² = -1`。Python 从 1.0 就开始支持复数了，比某些"直到 2020 年还在争论要不要加这个特性"的语言不知道高到哪里去了。

```python
# 复数的创建
z1 = 3 + 4j       # Python 用 j 表示虚数（而不是 i）
z2 = complex(5, 6)

# 复数运算
print(z1 + z2)   # (8+10j)
print(z1 * z2)   # (-9+38j)
print(abs(z1))   # 5.0（模长）
print(z1.conjugate())  # (3-4j)（共轭复数）
```

复数在科学计算、信号处理、电气工程等领域非常有用。Python 的复数支持让它在这些领域有了用武之地。

> 小结：Python 1.0 通过引入函数式特性，大大扩展了语言的表达能力。虽然这些特性在今天看来已经是"基操"，但在 1994 年，这代表了一种先进的编程思想。

---

## 1.2.3 Python 2.0（2000 年）—— 社区时代

2000 年 10 月 16 日，Python 2.0 发布。这是 Python 发展史上的一个重要转折点——**开源社区正式登场**。

在 Python 2.0 之前，Python 的发展基本靠 Guido 和少数几个贡献者推动。2.0 采用了 **SourceForge** 上的开源项目模式，设立了 Python 核心开发团队，开始接受全球开发者的贡献。

### 1.2.3.1 列表推导式（List Comprehension）

**列表推导式**（List Comprehension）是 Python 最受欢迎的特性之一，没有之一。它是一种"用一行代码创建列表"的简洁语法。

传统方式创建一个平方数列表：

```python
numbers = [1, 2, 3, 4, 5]
squared = []
for n in numbers:
    squared.append(n * n)
print(squared)  # [1, 4, 9, 16, 25]
```

用列表推导式，一行搞定：

```python
numbers = [1, 2, 3, 4, 5]
squared = [n * n for n in numbers]
print(squared)  # [1, 4, 9, 16, 25]
```

还可以加条件筛选：

```python
# 只保留偶数的平方
evens_squared = [n * n for n in numbers if n % 2 == 0]
print(evens_squared)  # [4, 16]
```

这种语法借鉴了数学里的集合定义符号 `{x² | x ∈ N, x < 6}`，所以读起来非常自然。

> 列表推导式在 Python 社区引发了"到底要不要用它"的讨论。有人觉得它简洁优雅，有人觉得嵌套超过两层就不可读了。Guido 的态度是：能用就用，不能用就别勉强。

### 1.2.3.2 垃圾回收机制（Garbage Collection）

在编程中，**内存管理**（Memory Management）是一个让人头疼的问题。你分配了一块内存，用完了要释放，否则就会"内存泄漏"（Memory Leak）——程序越跑越慢，最后崩溃。

Python 2.0 引入了**垃圾回收机制**（Garbage Collection，简称 GC），自动处理内存管理。简单来说，Python 会在后台监控哪些对象不再被使用了，自动把它们占用的内存释放掉。

```python
def create_objects():
    big_list = [i for i in range(100000)]  # 创建一个巨大的列表
    return big_list

create_objects()  # 函数结束后，那个大列表就没人用了
# Python 的 GC 会自动回收它占用的内存
# 你什么都不用做！
```

Python 的垃圾回收主要基于**引用计数**（Reference Counting）——每个对象都有一个计数器，记录有多少个变量在引用它。当计数器变成 0 时，对象就被回收了。

> 但引用计数有个致命问题：**循环引用**会导致内存泄漏。什么是循环引用？想象两个对象互相引用对方，虽然外部已经没有引用它们了，但引用计数都不是 0。Python 用"分代回收"（Generational GC）来解决这个问题——定期检查所有对象，清除那些"已死"但还没被回收的循环引用对象。

### 1.2.3.3 Unicode 支持

在计算机里，文字是用数字编码存储的。早期最流行的编码是 **ASCII**——它只能表示英文字母、数字和一些符号，总共 128 个字符。对于英语国家来说够用了，但中文有上万个汉字，根本装不下。

**Unicode**（统一码）是一种"给世界上所有文字都分配唯一编号"的编码标准，最多可以表示 100 多万个字符。Python 2.0 开始正式支持 Unicode。

```python
# Python 2 风格的 Unicode 字符串（需要加 u 前缀）
s = u"你好，世界！"
print(s)  # 你好，世界！

# Python 3 里，str 默认就是 Unicode，不需要前缀
# s = "你好，世界！"
```

Unicode 支持让 Python 终于可以愉快地处理各种语言了。中国程序员终于不用看到乱码了（虽然 Python 2 时代还是有一些坑，但比之前好多了）。

> 吐槽：Python 2 时代，Unicode 和 bytes 的关系曾经让无数人头疼。很多人写代码时遇到 `UnicodeDecodeError` 或 `UnicodeEncodeError`，简直欲仙欲死。Python 3 在这方面做了大刀阔斧的改革，我们后面再讲。

### 1.2.3.4 PEP（Python Enhancement Proposal）提案机制诞生

**PEP** 的全称是 Python Enhancement Proposal，翻译过来就是"Python 增强提案"。你可以把它理解为"Python 的 RFC"（Request For Comments）——一种让社区参与语言设计讨论的机制。

2000 年，随着 Python 2.0 的发布，PEP 提案机制正式登场。所有的 Python 语言改动、新特性、决策都要先写成 PEP，经过社区讨论和核心团队审批后才能实施。

著名的 PEP 列表：

| PEP 编号 | 标题 | 意义 |
|---------|------|------|
| PEP 8 | Style Guide for Python Code | 代码风格指南，Python 程序员的"宪法" |
| PEP 20 | The Zen of Python | Python 之禅 |
| PEP 257 | Docstring Conventions | 文档字符串规范 |

你可以在 [https://peps.python.org/](https://peps.python.org/) 查看所有 PEP。

> 有趣的事实：PEP 的编号是单调递增的，所以有时候你会看到一些"占位 PEP"——有人提议了一个想法，写了 PEP，但最后被拒绝了或者放弃了。PEP 编号就成了"历史的遗迹"。比如 PEP 401 曾经是"关于 Python 4.0 的恶搞 PEP"（现在已经失效）。

---

## 1.2.4 Python 2.4（2004 年）—— 协程与生成器

2004 年 11 月 30 日，Python 2.4 发布。这是 Python 2 系列的一个重要版本，引入了两个影响深远的特性：**生成器**（Generator）和**装饰器**（Decorator）语法糖。

### 1.2.4.1 生成器（yield 关键字）

**生成器**是一种"懒加载"的序列。普通列表是把所有元素都计算好、存到内存里；生成器则是"你需要什么我才计算什么"，像流水线一样，边用边生产。

创建生成器的两种方式：

```python
# 方式1：用函数 + yield
def count_up_to(n):
    count = 1
    while count <= n:
        yield count   # yield 就是"暂停并返回值"
        count += 1

gen = count_up_to(5)
print(list(gen))  # [1, 2, 3, 4, 5]

# 方式2：生成器表达式（类似列表推导式，但用圆括号）
gen = (x * x for x in range(5))
print(list(gen))  # [0, 1, 4, 9, 16]
```

生成器的优势在哪里？**省内存**！

想象一下你要处理一个超大文件，有 100 万行。如果用列表读取所有行，内存直接爆了。但用生成器，你可以一次读一行，内存占用几乎为零：

```python
def read_large_file(filename):
    """读取大文件的生成器函数"""
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            yield line.strip()

# 每次只读取一行，不会把整个文件加载到内存
for line in read_large_file("huge_file.txt"):
    print(line)
```

### 1.2.4.2 decorators（@decorator 语法糖引入）

**装饰器**（Decorator）是 Python 中一种"给函数或类增加额外功能"的语法糖。简单来说，就是"包装"一个函数，让它在执行前后做一些额外的事情。

```python
# 定义一个装饰器
def my_decorator(func):
    """这是一个打印函数执行时间的装饰器"""
    def wrapper(*args, **kwargs):
        print("函数开始执行...")
        result = func(*args, **kwargs)
        print("函数执行完毕！")
        return result
    return wrapper

# 使用装饰器（@ 符号）
@my_decorator
def say_hello(name):
    print(f"你好，{name}！")

say_hello("小明")
# 函数开始执行...
# 你好，小明！
# 函数执行完毕！
```

装饰器的应用场景非常广泛：日志记录、性能测量、权限检查、缓存……几乎每个 Python Web 框架（Flask、Django）都用装饰器来定义路由。

> 为什么叫"装饰器"？因为它就像给一个礼物包上漂亮的外包装——礼物本身没变，但外面多了一层装饰。

---

## 1.2.5 Python 2.7（2010 年）—— Python 2 最后一版

2010 年 7 月，Python 2.7 发布。这是 Python 2.x 系列的**最后一个版本**，也是一个"缝缝补补又三年"的版本——为了照顾大量还在用 Python 2 的用户，2.7 吸收了一些 Python 3 的特性。

### 1.2.5.1 argparse 命令行模块

**argparse** 是 Python 标准库里处理命令行参数的模块。在 argparse 出现之前，程序员通常用 `sys.argv`（一个简陋的字符串列表）来接收命令行参数，或者用 `getopt` 这种"反人类"的模块。

```python
import argparse

# 创建解析器
parser = argparse.ArgumentParser(description="这是一个加法计算器")

# 添加参数
parser.add_argument("a", type=int, help="第一个加数")
parser.add_argument("b", type=int, help="第二个加数")
parser.add_argument("--verbose", "-v", action="store_true", help="显示详细输出")

# 解析参数
args = parser.parse_args()

if args.verbose:
    print(f"{args.a} + {args.b} = {args.a + args.b}")
else:
    print(args.a + args.b)
```

运行效果：

```bash
$ python calc.py 3 5
8

$ python calc.py 3 5 --verbose
3 + 5 = 8
```

### 1.2.5.2 更多的 Python 2 兼容特性

Python 2.7 作为 Python 2 的最终版本，还吸收了一些 Python 3 的特性，为平滑迁移做准备。例如，新增了 `str.format()` 方法的更多功能支持，以及一些之前只在 Python 3 中可用的标准库改进。

```python
# Python 2.7 的 str.format() 示例
name = "小明"
age = 8
print("我叫{}，今年{}岁".format(name, age))  # 我叫小明，今年8岁
```

这主要是为了和 Python 3 的字符串格式化保持兼容。但说实话，用处不大，因为 Python 3 里所有字符串默认就是 Unicode，格式化也更统一。

### 1.2.5.3 Python 2.7 生命周期结束（2020 年）

2020 年 1 月 1 日，Python 2.7 正式**停止维护**。这标志着 Python 2 时代的彻底终结。

想象一下那天 Python 2.7 的内心独白：

> "我为 Python 社区服务了 20 年。20 年啊！够一个婴儿长成程序员了。从最初的 CGI 脚本到后来的 Web 开发，从数据处理到科学计算，我见证了 Python 从一条小蛇成长为巨蟒……好了，不说了，该退休了。让位给 Python 3 吧。"

不过说实话，Python 2 的"遗产"至今还有很多项目在用（比如某些老旧的 Django 1.x 版本、某些公司的祖传代码库）。所以迁移到 Python 3 这件事，直到今天依然在进行中。

> 彩蛋：Guido 曾经说过一句名言："Python 2 的寿命比我预期的要长得多。"——这句话大概可以用来解释为什么很多 Python 3 的新特性推进得那么慢，因为 Guido 自己对破坏性升级是有心理阴影的。

---

## 1.2.6 Python 3.0（2008 年）—— 划时代变革

2008 年 12 月 3 日，Python 3.0 发布。这大概是 Python 历史上**最具争议**的一个版本——因为它**完全不兼容 Python 2**。

Python 3 的设计目标非常明确：**修复 Python 2 的设计缺陷，让语言更优雅、更一致**。代价是——所有 Python 2 代码都要"翻译"才能在 Python 3 上运行。

这波操作，用现在的话说就是：** breaking change（破坏性变更）**。

### 1.2.6.1 print 成为函数（print()）

在 Python 2 里，`print` 是一个**语句**（statement），语法是这样的：

```python
# Python 2 风格
print "Hello, World!"           # 直接打印
print "Hello,", "Python!"       # 逗号分隔，输出空格
print "Number:", 42             # 打印数字
```

Python 3 把 `print` 变成了一个**函数**（function）：

```python
# Python 3 风格
print("Hello, World!")          # 函数调用
print("Hello,", "Python!")     # 逗号分隔，输出空格
print("Number:", 42)            # 打印数字
print("No newline", end="")     # 不换行
print("Overwritten")            # 覆盖上一行
```

为什么要改？因为函数比语句更灵活。比如你想把输出重定向到文件，`print` 语句就做不到，但 `print()` 函数可以：

```python
with open("output.txt", "w") as f:
    print("写入文件的内容", file=f)
```

这个改动虽然小，但当时引发了 Python 社区的激烈讨论——很多人觉得 `print` 语句简洁明了，干嘛非要改成函数？

Guido 的回应大概是：**优雅是有代价的，但代价是值得的。**

### 1.2.6.2 Unicode 默认（str 为 Unicode，bytes 为字节）

Python 2 的字符串处理是出了名的坑：

```python
# Python 2 时代
s1 = "你好"        # 这是字节串（bytes），不是 Unicode
s2 = u"你好"       # 这是 Unicode 字符串，需要加 u 前缀
```

Python 3 直接"拨乱反正"：

```python
# Python 3 时代
s1 = "你好"        # 默认就是 Unicode 字符串
s2 = b"你好"       # 如果要字节串，加 b 前缀
```

在 Python 3 里：
- `str` = Unicode 字符串（你想处理的文本）
- `bytes` = 原始字节（你想读写文件、网络传输时用）

```python
# 字符串和字节的转换
text = "Hello, Python!"          # str: Unicode
data = text.encode("utf-8")      # 编码成 bytes
print(data)                      # b'Hello, Python!'

recovered = data.decode("utf-8")  # 解码回 str
print(recovered)                  # Hello, Python!
```

### 1.2.6.3 整数除法：/ 返回浮点数，// 返回整数

Python 2 的除法行为让人窒息：

```python
# Python 2
result = 5 / 2   # 结果是 2（整数除法），不是 2.5！
```

Python 3 修复了这个问题：

```python
# Python 3
result = 5 / 2   # 2.5（浮点数除法）
floor_result = 5 // 2  # 2（整数除法，向下取整）
negative = -5 // 2     # -3（向下取整，不是 -2！）
```

> 这就是"地板除"（floor division）——总是向下取整。对于正数，`/` 和 `//` 结果相同；对于负数，就不一样了。

### 1.2.6.4 xrange 消失，range 优化

Python 2 有两个"范围"相关的类型：

```python
# Python 2
r1 = range(10)    # 返回列表 [0,1,2,3,4,5,6,7,8,9]
r2 = xrange(1000000000)  # 返回一个"懒加载"对象，不占内存
```

Python 3 合并了这两个：`range()` 就是"懒加载"的，不需要 `xrange` 了：

```python
# Python 3
r = range(10)           # range 对象，自动支持大范围
print(list(r))          # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
print(100 in r)         # False
```

### 1.2.6.5 异常链语法：raise ... from ...

Python 3 引入了**异常链**（Exception Chaining），让你可以"追踪异常的来源"：

```python
try:
    int("abc")
except ValueError as e:
    raise TypeError("类型错误") from e

# 运行结果：
# Traceback (most recent call last):
#   File "<stdin>", line 2, in <module>
# ValueError: invalid literal for int() with base 10: 'abc'
#
# The above exception was the direct cause of the following exception:
#
# Traceback (most recent call last):
#   File "<stdin>", line 4, in <module>
# TypeError: 类型错误
```

为什么要保留异常链？因为有时候你捕获了一个异常后，需要抛出另一个异常，但同时想保留原始异常的信息。`raise ... from ...` 可以做到这一点。

> 顺便说一句，Python 3.11 还引入了异常组（Exception Group），用 `except*` 来同时捕获多个异常，详见 1.2.15。

### 1.2.6.6 long 类型与 int 类型统一

Python 2 有两种整数类型：
- `int`：普通整数（有范围限制，通常是 32 位或 64 位）
- `long`：长整数（没有范围限制，但占用更多内存）

```python
# Python 2
a = 42        # int
b = 42L       # long
```

Python 3 统一成了一种 `int`——没有上限，想多大就多大：

```python
# Python 3
a = 42
b = 42 ** 1000  # 这是一个巨大的整数，照样能算
print(b)         # 写不下，自己试试
```

### 1.2.6.7 经典类（old-style class）被移除

Python 2 有两种类：**新式类**（new-style class）和**经典类**（old-style class）。

- 新式类：继承自 `object`，支持描述符（descriptor）、属性（property）等高级特性
- 经典类：不继承任何东西，功能受限

```python
# Python 2 经典类（不推荐）
class OldDog:
    def bark(self):
        print("汪汪！")

# Python 2 新式类
class NewDog(object):
    def bark(self):
        print("汪汪！")

# Python 3（所有类都是新式类，不需要写 object）
class Dog:
    def bark(self):
        print("汪汪！")
```

Python 3 移除了经典类，所有类默认继承自 `object`。这简化了语言，也避免了类型系统里的一些坑。

### 1.2.6.8 与 Python 2 不兼容（破坏性升级）

这是 Python 3 最重要的特点，也是最"臭名昭著"的特点——**Python 3 不兼容 Python 2**。

为什么要有这么大的破坏性？因为 Guido 认为，有些设计缺陷如果不做破坏性变更，就永远改不掉。比如 Unicode 和 bytes 的混乱关系、`print` 语句的局限性、整数除法的反人类行为……这些问题如果继续修修补补，代码会越来越难看。

> Guido 的原话大概是："我宁愿让 100 万行代码升级痛苦，也不愿让未来 20 年的语言设计继续背历史包袱。"

Python 社区为迁移付出了巨大代价：
- 大量库需要重写
- 迁移工具 `2to3.py` 被广泛使用
- 有些项目至今还在 Python 2 上运行

但回过头看，这波操作是值得的。Python 3 让语言更优雅、更一致、更适合未来。

---

## 1.2.7 Python 3.3（2012 年）—— 虚拟环境与命名空间包

2012 年 9 月，Python 3.3 发布。这个版本带来了两个重要特性：**虚拟环境**（venv）和**命名空间包**（namespace package）。

### 1.2.7.1 venv 模块引入

**虚拟环境**（Virtual Environment）是一种"隔离的 Python 运行环境"。它的作用是：每个项目用不同的 Python 版本、不同的第三方库，互不干扰。

举个例子：项目 A 需要 Django 2.0，项目 B 需要 Django 4.0，怎么办？虚拟环境就是解决方案。

```bash
# 创建虚拟环境
python -m venv myenv

# 激活虚拟环境（Windows）
myenv\Scripts\activate.bat

# 激活虚拟环境（Linux/Mac）
source myenv/bin/activate

# 安装包（只在虚拟环境里安装）
pip install django

# 退出虚拟环境
deactivate
```

在 `venv` 出现之前，Python 社区用的是 `virtualenv` 这个第三方工具。`venv` 是 Python 3.3 内置的，等于把"最佳实践"写进了标准库。

> 面试题预警：如果面试官问你"Python 虚拟环境是用来干什么的"，标准答案是："隔离项目依赖，避免版本冲突。"——这句话一定要背下来。

### 1.2.7.2 命名空间包（namespace package）

**命名空间包**（namespace package）是一种"多个目录可以贡献同一个包"的结构。听起来很抽象，举个例子：

传统的包结构：

```
mypackage/
    __init__.py
    module1.py
    module2.py
```

命名空间包结构：

```
namespacepkg/
    package1/
        __init__.py
    package2/
        __init__.py
```

使用命名空间包，你可以让 `package1` 和 `package2` 分属不同的团队开发、不同的地方存放，但最后合并成同一个命名空间。

```python
# package1/__init__.py
# 可以是空的，甚至不需要文件

# package2/__init__.py
# 也可以是空的

# 最后可以这样用：
from namespacepkg import package1, package2
```

---

## 1.2.8 Python 3.4（2014 年）—— 异步与打包

2014 年 3 月，Python 3.4 发布。这个版本带来了 `asyncio` 模块（异步编程）和 pip 的推广。

### 1.2.8.1 asyncio 模块引入

**asyncio** 是 Python 的异步 I/O 框架。异步 I/O 就是"不等 I/O 操作完成，先去干别的事"。

想象你去餐厅吃饭。**同步**模式下：你点了菜，要一直等到菜上齐才能吃。**异步**模式下：你点了菜，服务员去通知厨房，你就先玩手机，菜好了服务员叫你。

```python
import asyncio

async def fetch_data():
    """模拟异步获取数据（IO操作）"""
    print("开始获取数据...")
    await asyncio.sleep(2)  # 模拟等待 2 秒
    print("数据获取完成！")
    return {"data": "Python 3.4"}

async def main():
    result = await fetch_data()
    print(f"结果：{result}")

# 运行异步程序
asyncio.run(main())

# 输出：
# 开始获取数据...
# （等待 2 秒）
# 数据获取完成！
# 结果：{'data': 'Python 3.4'}
```

> `asyncio` 在 Python 3.4 是实验性的，Python 3.5 引入了 `async/await` 语法糖，才算正式成熟。

### 1.2.8.2 pip 成为推荐包管理器

**pip** 是 Python 的包管理器，全称是"Pip Installs Packages"（递归缩写，和 GNU 一样）。

在 pip 出现之前，Python 的包管理简直是噩梦：
- 不同操作系统安装方式不同
- 依赖关系混乱
- 没有统一的仓库

pip 的出现统一了一切：

```bash
# 安装包
pip install requests

# 安装指定版本
pip install flask==2.0.0

# 安装 requirements.txt 里的所有包
pip install -r requirements.txt

# 升级包
pip install --upgrade numpy

# 卸载包
pip uninstall numpy
```

Python 3.4 把 pip 设为推荐工具，并内置了 `ensurepip`（自动安装 pip）。

### 1.2.8.3 ensurepip（自动安装 pip）

`ensurepip` 是一个"如果没 pip 就自动安装 pip"的模块。

```bash
# 如果 pip 没安装
python -m ensurepip

# 指定 pip 源（国内加速）
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple some-package
```

> 国内用户常用清华、阿里云、中科大等镜像源来加速 pip 下载。

---

## 1.2.9 Python 3.5（2015 年）—— 类型提示元年

2015 年 9 月，Python 3.5 发布。这个版本在 Python 历史上具有里程碑意义——**类型提示**（Type Hints）正式登场。

### 1.2.9.1 typing 模块引入

**类型提示**（Type Hints）让你可以在代码里标注变量的类型、函数的参数类型和返回值类型。

```python
def greet(name: str) -> str:
    """带类型提示的问候函数"""
    return f"你好，{name}！欢迎学习 Python！"

print(greet("小明"))  # 你好，小明！欢迎学习 Python！
```

为什么要加类型提示？因为：

1. **代码更易读**：看到 `name: str` 就知道 name 应该是字符串
2. **IDE 提示更准确**：PyCharm、VS Code 可以给你更准确的自动补全
3. **静态检查工具**（如 mypy）可以帮你发现类型错误

```python
# typing 模块提供的类型
from typing import List, Dict, Optional, Union

def process_data(
    items: List[int],
    lookup: Dict[str, str],
    optional_name: Optional[str] = None
) -> Union[str, int]:
    # ...
    pass
```

> 类型提示是"可选的"——加了类型提示的代码和不加的代码运行起来完全一样。Python 不会因为类型不匹配就报错（除非你用 mypy 等静态检查工具）。

### 1.2.9.2 async/await 原生协程语法

Python 3.5 引入了 `async` 和 `await` 关键字，让协程（Coroutine）成为 Python 的一等公民。

```python
import asyncio

async def fetch_user(user_id: int) -> str:
    """模拟异步获取用户信息"""
    await asyncio.sleep(1)  # 模拟网络请求
    return f"用户{user_id}"

async def fetch_users_parallel(user_ids: list):
    """并发获取多个用户"""
    tasks = [fetch_user(uid) for uid in user_ids]
    results = await asyncio.gather(*tasks)
    return results

# 运行
users = asyncio.run(fetch_users_parallel([1, 2, 3]))
print(users)  # ['用户1', '用户2', '用户3']
```

`async` 用来定义一个"协程函数"（coroutine function），`await` 用来"等待"一个协程完成。这比 Python 3.4 的 `@asyncio.coroutine` 装饰器写法优雅多了。

### 1.2.9.3 matrix multiplication operator（@）

Python 3.5 引入了 `@` 运算符，专门用于**矩阵乘法**。

```python
import numpy as np

A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])

# 用 @ 做矩阵乘法
C = A @ B
print(C)
# [[19 22]
#  [43 50]]

# 对比：用 * 只是逐元素相乘
print(A * B)
# [[ 5 12]
#  [21 32]]
```

`@` 运算符可以被任何类重载（实现 `__matmul__` 方法），所以不只是 numpy 可以用。你也可以在自己的类里定义矩阵乘法的行为。

### 1.2.9.4 可迭代对象解包：*iterable

Python 3.5 引入了**可迭代对象解包**（Iterable Unpacking）的增强语法。

```python
# 合并多个列表
first = [1, 2, 3]
second = [4, 5, 6]
combined = [*first, *second]
print(combined)  # [1, 2, 3, 4, 5, 6]

# 合并字典（Python 3.9 更进一步，支持 | 运算符）
d1 = {"a": 1, "b": 2}
d2 = {"c": 3, "d": 4}
combined = {**d1, **d2}
print(combined)  # {'a': 1, 'b': 2, 'c': 3, 'd': 4}

# 函数调用时解包
numbers = [1, 2, 3]
print(*numbers)  # 1 2 3（输出 1 2 3）
```

---

## 1.2.10 Python 3.6（2016 年）—— f-string 时代

2016 年 12 月，Python 3.6 发布。这个版本带来了 **f-string**（格式化字符串字面量）——这大概是 Python 3 最受欢迎的特性之一。

### 1.2.10.1 f-string 格式化字符串（f"{}"）

**f-string** 是一种在字符串前面加 `f` 或 `F` 前缀，支持在字符串内部直接嵌入表达式的语法。

```python
name = "小明"
age = 8
city = "北京"

# f-string 格式化
print(f"我叫{name}，今年{age}岁，住在{city}。")  
# 我叫小明，今年8岁，住在北京。

# 表达式可以直接写在 {} 里
print(f"明年我就{age + 1}岁了！")  # 明年我就9岁了！

# 调用方法
print(f"{name.upper()} = {name.lower()}")  # 小明 = 小明

# 格式化数字
import math
print(f"π 约等于 {math.pi:.2f}")  # π 约等于 3.14
print(f"10000 用千位分隔符: {10000:,}")  # 10,000
```

对比之前的格式化方式，你就知道 f-string 有多优雅：

```python
# % 格式化（旧派）
print("我叫%s，今年%d岁" % (name, age))

# format 方法（中等）
print("我叫{}，今年{}岁".format(name, age))

# f-string（现代）
print(f"我叫{name}，今年{age}岁")
```

### 1.2.10.2 变量注解（Variable Annotations：x: int = 5）

Python 3.6 引入了**变量注解**（Variable Annotations），让你可以给变量加类型提示。

```python
# 变量注解
name: str = "小明"
age: int = 8
height: float = 1.35
is_student: bool = True

# 注解不影响运行，纯粹是给 IDE 和静态检查工具看的
print(name)  # 小明
```

变量注解和函数注解（Python 3.5 引入的）一起，构成了 Python 的"类型提示"体系。

### 1.2.10.3 异步生成器

Python 3.6 还支持了**异步生成器**（Async Generator）——在生成器里使用 `await`。

```python
import asyncio

async def async_generator():
    """异步生成器：每 yield 一个值就 await 一下"""
    for i in range(3):
        await asyncio.sleep(0.5)
        yield i

async def main():
    async for value in async_generator():
        print(f"获取到值: {value}")

asyncio.run(main())
# 获取到值: 0
# （等待 0.5 秒）
# 获取到值: 1
# （等待 0.5 秒）
# 获取到值: 2
```

### 1.2.10.4 secrets 模块

Python 3.6 引入了 **secrets** 模块，专门用于生成**密码学安全的随机数**。

```python
import secrets

# 生成随机字节
random_bytes = secrets.token_bytes(16)
print(random_bytes)  # b'\xa3\xf1...'

# 生成十六进制字符串（适合做令牌）
token = secrets.token_hex(32)
print(token)  # a3f1b2c4d5...

# 生成 URL 安全的令牌
url_token = secrets.token_urlsafe(32)
print(url_token)  # a3f1B2C4D5...

# 安全随机整数
random_int = secrets.randbelow(100)  # 0-99 的随机整数
print(random_int)
```

为什么要专门搞一个 `secrets` 模块？因为 `random` 模块生成的随机数**不是**密码学安全的，不能用于安全相关的场景（如生成密码、令牌、密钥）。

---

## 1.2.11 Python 3.7（2018 年）—— dataclass 与上下文

2018 年 6 月，Python 3.7 发布。这个版本带来了 `@dataclass` 装饰器和一些协程相关的改进。

### 1.2.11.1 @dataclass 装饰器

**dataclass**（数据类）是一种自动生成 `__init__`、`__repr__`、`__eq__` 等方法的类。简单来说，就是让你少写很多样板代码（boilerplate）。

传统写法：

```python
class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
    
    def __repr__(self):
        return f"Point(x={self.x}, y={self.y})"
    
    def __eq__(self, other):
        if not isinstance(other, Point):
            return False
        return self.x == other.x and self.y == other.y

p1 = Point(1.0, 2.0)
p2 = Point(1.0, 2.0)
print(p1)  # Point(x=1.0, y=2.0)
print(p1 == p2)  # True
```

dataclass 写法：

```python
from dataclasses import dataclass

@dataclass
class Point:
    x: float
    y: float

p1 = Point(1.0, 2.0)
p2 = Point(1.0, 2.0)
print(p1)  # Point(x=1.0, y=2.0)
print(p1 == p2)  # True（自动生成 __eq__）
```

一行顶七行，不香吗？

### 1.2.11.2 contextvars（上下文变量）

**contextvars** 模块提供了**上下文变量**（Context Variable）的支持。这在异步编程中特别有用——每个异步任务可以有自己的变量副本，互不干扰。

```python
from contextvars import ContextVar

# 创建一个上下文变量
request_id = ContextVar('request_id', default='no-request')

# 在某个"上下文"里设置值
import contextvars

request_id.set('req-123')

def get_request_id():
    return request_id.get()

print(get_request_id())  # req-123
```

在 Flask、Django 等 Web 框架里，上下文变量被用来存储"当前请求"相关的信息，这样在异步代码里也能正确获取。

### 1.2.11.3 asyncio.run()

Python 3.7 简化了 asyncio 程序的启动方式——用 `asyncio.run()` 即可。

```python
# Python 3.7 之前
import asyncio

@asyncio.coroutine
def main():
    pass

loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(main())
finally:
    loop.close()

# Python 3.7+（一行搞定）
import asyncio

async def main():
    pass

asyncio.run(main())  # 就这一行！
```

### 1.2.11.4 Data Classes 简化

dataclass 的设计目标是"存储数据的类"。它自动生成了：
- `__init__`：构造函数
- `__repr__`：字符串表示
- `__eq__`：相等比较
- `__hash__`：可哈希（如果设置了 `frozen=True`）

```python
from dataclasses import dataclass, field
from typing import List

@dataclass
class Student:
    name: str
    age: int
    grades: List[float] = field(default_factory=list)  # 默认值工厂
    
    def average_grade(self) -> float:
        return sum(self.grades) / len(self.grades) if self.grades else 0.0

s = Student("小明", 8, [95, 92, 88])
print(s)  # Student(name='小明', age=8, grades=[95, 92, 88])
print(s.average_grade())  # 91.6666...
```

---

## 1.2.12 Python 3.8（2019 年）—— 赋值表达式

2019 年 10 月，Python 3.8 发布。这个版本最"炸裂"的新特性是**海象运算符**（Walrus Operator）`:=`。

### 1.2.12.1 赋值表达式：:=（海象运算符）

**海象运算符**（:=）允许在表达式内部赋值变量。它的名字来源于 ":=" 两个符号组合起来像海象的象牙。

传统写法（先赋值再使用）：

```python
data = get_data()
if data is not None:
    print(f"数据长度: {len(data)}")
    process(data)
```

海象运算符写法（赋值和使用合二为一）：

```python
if (data := get_data()) is not None:
    print(f"数据长度: {len(data)}")
    process(data)
```

再比如读文件直到某行出现：

```python
# 传统写法
while True:
    line = f.readline()
    if not line:
        break
    print(line.strip())

# 海象运算符写法
while (line := f.readline()):
    print(line.strip())
```

> 注意：海象运算符的优先级很低，使用时经常需要加括号，否则可能产生意外结果。Guido 自己也承认这是"有争议的"特性，但最终还是加了。

### 1.2.12.2 位置参数仅限关键字（/ 分隔符）

Python 3.8 引入了**位置参数仅限关键字**（Keyword-Only Arguments）的增强语法——在函数定义时用 `/` 分隔。

```python
def f(a, b, /, c, d, *, e, f):
    """只允许位置参数的参数用 / 分隔"""
    print(a, b, c, d, e, f)

f(1, 2, 3, 4, e=5, f=6)  # 正确
# f(a=1, b=2, 3, 4, e=5, f=6)  # 错误！a 和 b 必须按位置传递
```

为什么要这样做？好处是：
- 强制某些参数按位置传递，避免用关键字传参时拼写错误
- 让 API 更灵活，未来可以改参数名而不破坏调用代码

### 1.2.12.3 f-string 支持 = 说明符

Python 3.8 让 f-string 可以更方便地调试了——支持 `=` 说明符：

```python
x = 42

# 之前的调试写法
print(f"x = {x}")  # x = 42

# Python 3.8+ 的写法
print(f"{x = }")   # x = 42
print(f"{x * 2 = }")  # x * 2 = 84
```

这比手动写 `f"x = {x}"` 方便多了，特别适合调试时打印变量值。

### 1.2.12.4 Reversible protocols

Python 3.8 引入了一些新的协议（Protocol），比如 `Reversible`（可逆）和 `Coroutine`。

### 1.2.12.5 typing.Final

Python 3.8 在 `typing` 模块里添加了 `Final`，用来标记"不能再重新赋值"的变量：

```python
from typing import Final

PI: Final = 3.14159          # 常量，一旦赋值就不能再改
MAX_SIZE: Final = 1000       # 加上类型检查更规范

PI = 3.14  # 类型检查器会报错：Cannot assign to a Final
```

---

## 1.2.13 Python 3.9（2020 年）—— 字典合并运算符

2020 年 10 月，Python 3.9 发布。这个版本带来了字典合并运算符和类型提示泛型的语法改进。

### 1.2.13.1 字典合并运算符：| 和 |=

终于，Python 字典可以用 `|` 和 `|=` 来合并了！

```python
d1 = {"a": 1, "b": 2}
d2 = {"b": 3, "c": 4}
d3 = {"c": 5, "d": 6}

# 合并字典（| 运算符）
merged = d1 | d2 | d3
print(merged)  # {'a': 1, 'b': 3, 'c': 5, 'd': 6}
# 注意：b 取了 d2 的值 3，说明后者覆盖前者

# 就地合并（|= 运算符）
d1 |= d2
print(d1)  # {'a': 1, 'b': 3, 'c': 4}
```

之前合并字典的方法：

```python
# 方式1：用 update（会修改原字典）
d1 = {"a": 1, "b": 2}
d2 = {"b": 3, "c": 4}
d1.update(d2)
print(d1)  # {'a': 1, 'b': 3, 'c': 4}

# 方式2：用字典解包
merged = {**d1, **d2, **d3}
```

现在 `|` 运算符比解包写法直观多了。

### 1.2.13.2 类型提示泛型（内置类型作为泛型：list[str]）

Python 3.9 之前，泛型类型必须从 `typing` 模块导入：

```python
# Python 3.8 及之前
from typing import List, Dict, Tuple

def process(items: List[int]) -> Dict[str, int]:
    return {str(i): i for i in items}
```

Python 3.9 允许直接用内置类型作为泛型：

```python
# Python 3.9+
def process(items: list[int]) -> dict[str, int]:
    return {str(i): i for i in items}
```

注意：`list[str]` 比 `List[int]` 简洁多了！目前 Python 3.10+ 已经完全支持这种写法。

> 目前 Python 官方推荐使用内置类型写法（`list[int]`），`typing.List` 等仍在支持，但最终会被弃用。

### 1.2.13.3 字符串方法：removeprefix()、removesuffix()

Python 3.9 给字符串添加了两个新方法，专门用于去除前缀和后缀：

```python
filename = "report_2024.pdf"

# 去除前缀
print(filename.removeprefix("report_"))  # 2024.pdf

# 去除后缀
print(filename.removesuffix(".pdf"))  # report_2024

# 对比旧方法
print(filename[7:])   # 2024.pdf（要数索引，容易错）
print(filename[:-4])  # report_2024（要记得减4）
```

这两个方法让"去掉文件扩展名"和"去掉路径前缀"的代码更可读、更不容易出错。

### 1.2.13.4 ZoneInfo（时区模块）

Python 3.9 引入了 **ZoneInfo** 模块，用于处理时区信息：

```python
from zoneinfo import ZoneInfo
from datetime import datetime

# 指定时区的时间
dt = datetime(2024, 1, 1, 12, 0, tzinfo=ZoneInfo("Asia/Shanghai"))
print(dt)  # 2024-01-01 12:00:00+08:00

# 转换为不同时区
dt_tokyo = dt.astimezone(ZoneInfo("Asia/Tokyo"))
print(dt_tokyo)  # 2024-01-01 13:00:00+09:00

# 当前时区
now_utc = datetime.now(ZoneInfo("UTC"))
print(now_utc)
```

之前处理时区要用 `pytz` 这个第三方库，现在标准库就能搞定了。

---

## 1.2.14 Python 3.10（2021 年）—— match 语句

2021 年 10 月，Python 3.10 发布。这个版本最吸引眼球的是**结构化模式匹配**（Structural Pattern Matching），即 `match...case` 语句。

### 1.2.14.1 match...case 结构化模式匹配

`match...case` 是一种"根据数据结构匹配不同分支"的语法。它借鉴自函数式语言（如 Haskell、Scala）和一些系统语言（如 Rust）。

```python
def http_status(status_code: int) -> str:
    match status_code:
        case 200:
            return "OK"
        case 301 | 302:  # 多个值匹配同一个分支
            return "Redirect"
        case 400:
            return "Bad Request"
        case 404:
            return "Not Found"
        case 500:
            return "Internal Server Error"
        case _ if status_code < 0:  # 带条件的匹配
            return "Invalid code"
        case _:
            return f"Unknown status: {status_code}"

print(http_status(200))  # OK
print(http_status(404))  # Not Found
print(http_status(-1))   # Invalid code
```

match 还可以匹配**数据结构**（不仅仅是值）：

```python
def describe_point(point: tuple):
    match point:
        case (0, 0):
            return "原点"
        case (x, 0):
            return f"X轴上的点，x={x}"
        case (0, y):
            return f"Y轴上的点，y={y}"
        case (x, y):
            return f"平面上的点，x={x}, y={y}"

print(describe_point((0, 0)))   # 原点
print(describe_point((5, 0)))   # X轴上的点，x=5
print(describe_point((3, 4)))   # 平面上的点，x=3, y=4
```

match 还可以匹配**带类的结构**（ dataclass、namedtuple 等）：

```python
from dataclasses import dataclass

@dataclass
class Point:
    x: float
    y: float

def describe_shape(shape):
    match shape:
        case []:
            return "空列表"
        case [Point(0, 0), *rest]:  # 第一个点是原点
            return f"从原点开始的多边形，共{len(rest)+1}个点"
        case _:
            return "其他形状"

print(describe_shape([]))  # 空列表
print(describe_shape([Point(0, 0), Point(1, 1)]))  # 从原点开始的多边形，共2个点
```

> match...case 是 Python 3.10 才有的语法，别在 Python 3.9 上试，否则会报 `SyntaxError`。

### 1.2.14.2 精确错误信息（Better Error Messages）

Python 3.10 大幅改进了错误提示信息，让调试更轻松。

```python
# 之前（Python 3.9）
# TypeError: unsupported operand type(s) for +: 'int' and 'str'

# 现在（Python 3.10+）
# TypeError: unsupported operand type(s) for +: 'int' and 'str'. Did you mean 'int' + 'int' or 'str' + 'str'?
```

```python
# 之前
# SyntaxError: invalid syntax

# 现在
# SyntaxError: expected ':'
```

### 1.2.14.3 zip() 增加 strict 参数

Python 3.10 给 `zip()` 函数添加了 `strict` 参数。

```python
names = ["Alice", "Bob", "Charlie"]
scores = [95, 88]

# 默认行为：短的优先，到头就停
print(list(zip(names, scores)))  # [('Alice', 95), ('Bob', 88)]

# strict=True：长度不一致直接报错
try:
    print(list(zip(names, scores, strict=True)))
except ValueError as e:
    print(f"错误: {e}")  # ValueError: zip() argument 2 is shorter than argument 1
```

### 1.2.14.4 Union 类型简化：X | Y

Python 3.10 简化了联合类型的写法：

```python
# Python 3.9 及之前
from typing import Union
def process(x: Union[int, str]) -> Union[int, str]:
    return x

# Python 3.10+
def process(x: int | str) -> int | str:
    return x
```

`int | str` 比 `Union[int, str]` 直观多了。这也是类型提示语法的自然进化。

---

## 1.2.15 Python 3.11（2022 年）—— 异常组

2022 年 10 月，Python 3.11 发布。这个版本带来了异常组（Exception Group）和更友好的错误提示。

### 1.2.15.1 except* 异常组语法

**异常组**（Exception Group）是 Python 3.11 引入的新特性，用 `except*` 来同时捕获多个异常。

```python
try:
    raise ExceptionGroup("group1", [
        ValueError("无效值"),
        TypeError("类型错误"),
        RuntimeError("运行时错误"),
    ])
except* ValueError as e:
    print(f"捕获到 ValueError: {e}")
except* TypeError as e:
    print(f"捕获到 TypeError: {e}")
except* Exception as e:
    print(f"捕获到其他异常: {e}")

# 输出：
# 捕获到 ValueError: 无效值
# 捕获到 TypeError: 类型错误
```

`except*` 是"捕获异常组中匹配的类型"，而不是"同时捕获多个异常"。它的设计主要是为了异步编程中的并发任务——多个任务可能同时抛出异常，需要统一处理。

### 1.2.15.2 更友好的错误提示

Python 3.11 的错误提示进一步优化，增加了"代码片段"和"箭头指向"：

```
Traceback (most recent call last):
  File "demo.py", line 1, in <module>
    if x = 3:  # 注意这里是 = 而不是 ==
               #
               # SyntaxError: invalid assignment expression
```

### 1.2.15.3 启动速度提升 10~25%

Python 3.11 对解释器做了大量优化，启动速度比 3.10 快了 10%~25%。

这听起来不多，但想象一下：如果你每天运行 100 次 Python 脚本，每次节省 0.1 秒，一年就能省下将近 1 个小时。

### 1.2.15.4 异步任务组：TaskGroup

Python 3.11 引入了 `TaskGroup`，让异步并发任务的管理更方便：

```python
import asyncio

async def task(name: str, seconds: float):
    print(f"{name} 开始")
    await asyncio.sleep(seconds)
    print(f"{name} 完成")
    return f"{name} 结果"

async def main():
    async with asyncio.TaskGroup() as tg:
        t1 = tg.create_task(task("任务A", 1.0))
        t2 = tg.create_task(task("任务B", 0.5))
    
    print(f"任务A结果: {t1.result()}")
    print(f"任务B结果: {t2.result()}")

asyncio.run(main())
# 任务A 开始
# 任务B 开始
# 任务B 完成
# 任务A 完成
# 任务A结果: 任务A 结果
# 任务B结果: 任务B 结果
```

`TaskGroup` 确保所有任务完成后才退出 `async with` 块，如果有任何任务抛出异常，会统一收集并再次抛出。

---

## 1.2.16 Python 3.12（2023 年）—— 解释器优化

2023 年 10 月，Python 3.12 发布。这个版本继续打磨解释器性能，并大幅改进了 f-string 和错误提示。

### 1.2.16.1 解释器启动速度进一步提升

Python 3.12 的解释器启动速度比 3.11 再快 5%~15%。此外，运行速度也有小幅提升（得益于更高效的字节码）。

### 1.2.16.2 f-string 重大改进（支持调试）

Python 3.12 的 f-string 终于支持更强大的调试语法了！

```python
x = 42
name = "小明"

# Python 3.8+：= 说明符可以直接打印变量名和值
print(f"{x = }")       # x = 42
print(f"{name = }")    # name = 小明

# Python 3.12+：= 说明符更简洁，且支持在表达式中使用
print(f"{x=}")         # x=42
print(f"{name=}")      # name='小明'
print(f"{x + 5 = }")   # x + 5 = 47
```

> 注意：Python 3.12 修复了 f-string 里不能写 `f"{"hello"}"` 这种嵌套引用的限制（之前会报 `SyntaxError`）。

### 1.2.16.3 更清晰的错误信息

Python 3.12 的错误信息继续改进，增加了更多"猜测性建议"：

```
>>> from collections import Iterable
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
    from collections import Iterable
ImportError: cannot import name 'Iterable' from 'collections'. 
Instead of 'from collections import Iterable', use 'from collections.abc import Iterable'.
```

### 1.2.16.4 typing 模块改进

Python 3.12 对 `typing` 模块做了多处改进，包括但不限于：

- **`typing.TypeIs`**（PEP 742）：比 `typing.TypeGuard` 更精确的类型收窄标记
- **`typing.TypeAlias`** 的改进，使显式类型别名更清晰
- 更完善的泛型语法支持

这些改进让静态类型检查更精确，也减少了运行时开销。

---

## 1.2.17 Python 3.13（2024 年）—— 实验性 JIT

2024 年 10 月，Python 3.13 发布。这个版本带来了一个重磅特性：**实验性 JIT 编译器**。

### 1.2.17.1 实验性 JIT 编译器（启用方式）

**JIT**（Just-In-Time Compiler，即时编译器）是一种"在运行时把热点代码编译成机器码"的技术。和静态编译器（如 C 语言）不同，JIT 可以根据运行时信息动态优化代码。

Python 3.13 引入了一个实验性的 JIT——但需要手动启用：

```bash
# 编译 Python 时需要加 --enable-experimental-jit
# 或者设置环境变量
export PYTHON_JIT=1
python your_script.py
```

> 注意：Python 3.13 的 JIT 还是实验性的，不建议在生产环境使用。目前 CPython 的默认解释器还是 bytecode interpreter（字节码解释器）。

### 1.2.17.2 解释器启动速度再提升

Python 3.13 的解释器启动速度继续优化，据说比 3.12 再快 10%。

### 1.2.17.3 改进的 GIL 讨论

**GIL**（Global Interpreter Lock，全局解释器锁）是 Python 历史上最"臭名昭著"的设计之一。GIL 的意思是：在任意时刻，只有一个线程可以执行 Python 字节码。

这意味着什么？意味着 Python 的多线程**不能真正利用多核 CPU**。如果你想用多核做并行计算，Python 的多线程基本没用。

Python 社区为了解决这个问题，尝试了各种方法：

- **multiprocessing**：用进程代替线程，每个进程有自己的 GIL
- **asyncio**：单线程异步，避免 GIL 的并发问题
- **C 扩展**：把性能关键代码用 C 写，绕过 GIL
- **PEP 703**：提议移除 GIL，但目前还在讨论中

Python 3.13 改进了 GIL 相关的一些内部机制，但没有移除 GIL。PEP 703 的进展值得关注。

### 1.2.17.4 交互式解释器改进（默认彩色输出）

Python 3.13 的交互式解释器（REPL）终于支持**彩色输出了**！

```bash
$ python
>>> [1, 2, 3]
[1, 2, 3]  # 之前是黑白输出，现在是有颜色的！
>>> {"a": 1}
{'a': 1}   # 有颜色！
```

此外，错误信息也有了更好的颜色区分。

---

## 1.2.18 Python 3.14（2025 年）—— 更快的解释器

> 📅 按照 Python 每年 10 月发布一个新版本的节奏，Python 3.14.0 预计在 2025 年 10 月发布。以下内容基于已公开的 PEP 和开发进度，属于"合理预期"而非最终定论。

### 1.2.18.1 解释器性能提升

Python 3.14 继续聚焦解释器优化。多项内部改进使得字节码执行更高效。

### 1.2.18.2 typing 模块增强

- **typing.ReadOnly**（PEP 826）：新增只读类型标记，用于更精确地描述"不允许修改"的类型
- 泛型语法的持续完善

### 1.2.18.3 标准库改进

- **`jiter` 模块**（PEP 738）：提供更高效的迭代器实现，减少内存拷贝
- **`asyncio`**：异步生态继续壮大
- **`typing`**：更多类型工具加入

### 1.2.18.4 CPython 实现层面

- **JIT 编译器进一步完善**：experimental JIT 正在走向成熟
- **PEP 703 自由线程模式**：无 GIL 的 CPython 仍在积极开发中，未来版本可能会更稳定
- **模块加载速度**：持续打磨

---

# 1.3 Python 两大版本分支的告别

## 1.3.1 Python 2.7 的最终停更（2020 年 1 月 1 日）

2020 年 1 月 1 日，Python 2.7 正式**停止维护**。这一天，全球无数还在跑 Python 2 代码的服务器同时打了个喷嚏。

从 2000 年 Python 2.0 发布，到 2020 年 Python 2.7 停更，Python 2 系列服务了**整整 20 年**。

20 年是什么概念？2000 年的时候：
- iPhone 还没诞生
- Google 刚成立两年
- 中国加入 WTO 还没加入
- Windows 98 还是主流操作系统

然后 Python 2 就这样"从出生到停更"跨越了整个移动互联网时代。

> 据说 Guido 在 Python 2.7 停更那天发了一条推特："Python 2 的时代正式结束了。感谢大家这 20 年的陪伴。现在，去拥抱 Python 3 吧，它在等你。"

## 1.3.2 迁移工具：2to3.py 的使用

Python 社区为迁移 Python 2 到 Python 3 开发了一个官方工具：**`2to3.py`**。

这个工具会自动扫描 Python 2 代码，尝试把它翻译成 Python 3 代码：

```bash
# 基本用法
2to3 your_script.py

# 直接修改文件（而不是输出到 stdout）
2to3 -w your_script.py

# 查看所有可修复的问题
2to3 --list-fixes

# 常用的修复项
2to3 -f imports -f idioms -w your_script.py
```

`2to3` 能自动修复很多常见的不兼容问题，比如：

```python
# Python 2
print "Hello"
raw_input("Enter: ")
unicode("hello")
[ x for x in range(10) if x % 2 == 0 ]

# 自动转换成 Python 3
print("Hello")
input("Enter: ")
"hello"
[x for x in range(10) if x % 2 == 0]
```

但 `2to3` 不是万能的——它只能处理**语法层面的不兼容**，无法处理**语义层面**（比如依赖库没有 Python 3 版本）的问题。

> 最佳实践：先用 `2to3` 跑一遍，然后用手动 review，最后全面测试。迁移是痛苦的，但 Python 3 的好处是长远的。

## 1.3.3 Python 2 兼容代码示例与 Python 3 对比

让我们看一些 Python 2 和 Python 3 的典型差异对比：

| 特性 | Python 2 | Python 3 |
|------|---------|---------|
| print 语句 | `print "hello"` | `print("hello")` |
| 字符串类型 | `str` = bytes，`unicode` = Unicode | `str` = Unicode，`bytes` = 字节 |
| 除法 | `/` 整数除法（截断） | `/` 浮点除法，`//` 整数除法 |
| input | `input()` 等同 `eval(raw_input())` | `input()` 等同 `raw_input()` |
| range | `range()` 返回列表，`xrange()` 懒加载 | `range()` 就是懒加载 |
| 类继承 | 默认经典类 | 默认新式类 |
| 异常语法 | `raise TypeError, "msg"` | `raise TypeError("msg")` |
| 异常捕获 | `except TypeError, e:` | `except TypeError as e:` |

一个完整的对比示例：

```python
# Python 2
# -*- coding: utf-8 -*-
from __future__ import print_function

print "Hello, Python 2!"

class OldStyleClass:
    pass

import sys
sys.stdout.write("Output without newline")
print 42 / 5  # 输出 8（整数除法）
```

```python
# Python 3
# -*- coding: utf-8 -*-

print("Hello, Python 3!")

class NewStyleClass(object):  # 继承 object 是多余的，但更明确
    pass

import sys
sys.stdout.write("Output without newline\n")
print(42 / 5)  # 输出 8.4（浮点除法）
print(42 // 5) # 输出 8（整数除法）
```

## 1.3.4 为什么 Python 3 不兼容 Python 2

这个问题值得深入探讨。Python 3 为什么宁可"得罪"整个社区，也要做一个破坏性升级？

Guido 在多个场合解释过这个问题，总结起来有以下几点：

**1. Unicode 字符串的混乱是"根本性错误"**

Python 2 的字符串设计是"历史包袱"的产物。在互联网时代之前，ASCII 够用；但到了 Unicode 时代，Python 2 的 `str` 是字节串、`unicode` 是 Unicode 的设计简直是"反人类"。如果不彻底改变，就永远是这个烂摊子。

**2. print 语句限制了语言的表达能力**

`print` 作为语句不能作为参数传递、不能作为返回值、不能重定向到文件。这限制了 Python 的表达能力。

**3. 整数除法的反直觉行为**

`5 / 2 = 2` 在数学上是不正确的（应该是 2.5）。虽然这有历史原因（性能考量），但确实坑害了无数新手。

**4. 保持向后兼容的代价太大**

如果继续在 Python 2.x 里打补丁，语言会越来越臃肿、越来越不一致。Guido 选择了"长痛不如短痛"。

> Guido 的原话（大致意思）："我知道这会伤害很多人，但 Python 3 是正确的选择。20 年后再回头看，人们会理解的。"

---

# 1.4 Python 的哲学思想

## 1.4.1 The Zen of Python（import this）全文解读

Python 有一首著名的"诗"——**The Zen of Python**（Python 之禅）。只要在 Python 解释器里输入 `import this`，就会显示出来：

```python
>>> import this
```

输出来源存放在 `this.py` 文件里，其中有一行著名的文字：

```python
s = """Gur Mra bs Clguba, ol Gvz Crgref

Ornhgvshy vf orggre guna htyl.
Rkcyvpvg vf orggre guna vzcyvpvg.
Fvzcyr = orggre guna pbzcyrk.
Pbzcyrk = orggre guna fvzcyr."""
# （这是 ROT13 加密后的 Python 之禅）
```

解开之后，就是下面这段话了。

**The Zen of Python 全文：**

```
The Zen of Python, by Tim Peters

Beautiful is better than ugly.
Explicit is better than implicit.
Simple is better than complex.
Complex is better than complicated.
Flat is better than nested.
Sparse is better than dense.
Readability counts.
Special cases aren't special enough to break the rules.
Although practicality beats purity.
Errors should never pass silently.
Unless explicitly silenced.
In the face of ambiguity, refuse the temptation to guess.
There should be one-- and preferably only one --obvious way to do it.
Although that way may not be obvious at first unless you're Dutch.
Now is better than never.
Although never is often better than *right* now.
If the implementation is hard to explain, it's a bad idea.
If the implementation is easy to explain, it may be a good idea.
Namespaces are one honking great idea -- let's do more of those!
```

下面，让我们一句一句来解读。

### 1.4.1.1 Beautiful is better than ugly.

**美优于丑。**

代码不仅要让机器执行，还要让人类阅读。漂亮的代码让人愉悦，丑陋的代码让人头疼。Python 追求的是"第一眼就让人心动"的美感。

```python
# 丑（ Ugly）
def processData(data):
    result=[]
    for item in data:
        if item["active"]==True:
            result.append(item["value"])
    return result

# 美（Beautiful）
def get_active_values(data):
    return [
        item["value"]
        for item in data
        if item["active"]
    ]
```

### 1.4.1.2 Explicit is better than implicit.

**显优于隐。**

代码应该清晰明了地表达意图，而不是靠"约定俗成"或"魔法"来运作。显式的代码更容易理解、调试和维护。

```python
# 隐式：依赖全局变量
total = 0
def add_to_total(x):
    global total
    total += x
    return total

# 显式：参数和返回值一目了然
def add(a, b):
    return a + b
```

### 1.4.1.3 Simple is better than complex.

**简单优于复杂。**

能用简单方法解决的问题，就不要搞复杂。如果你的代码里有一堆设计模式、抽象层、中间件，但本质就是"把 A 转成 B"，那这个设计就是失败的。

```python
# 复杂
class Calculator:
    @staticmethod
    def compute(operation_type, a, b):
        if operation_type == "add":
            return a + b
        elif operation_type == "subtract":
            return a - b
        ...

calc = Calculator()
result = calc.compute("add", 1, 2)

# 简单
result = 1 + 2
```

### 1.4.1.4 Complex is better than complicated.

**复杂优于一团糟。**

有时候问题本身就是复杂的，不能硬要把复杂问题简化，否则会丢失重要信息。Python 并不追求"最小化代码"，而是追求"不过度设计"。如果你的业务逻辑确实复杂，就让它复杂——但要有条理地复杂。

### 1.4.1.5 Flat is better than nested.

**扁平优于嵌套。**

嵌套层次太深，代码就难读、难改、难调试。Python 之禅建议：能用一层解决的不用两层，能用两层解决的不用三层。

```python
# 深层嵌套
def process(data):
    if data is not None:
        if isinstance(data, dict):
            if "items" in data:
                items = data["items"]
                if isinstance(items, list):
                    for item in items:
                        if item.get("active"):
                            do_something(item)

# 扁平化
def process(data):
    if data is None:
        return
    if not isinstance(data, dict):
        return
    items = data.get("items")
    if not isinstance(items, list):
        return
    for item in items:
        if item.get("active"):
            do_something(item)
```

### 1.4.1.6 Sparse is better than dense.

**稀疏优于密集。**

代码要有呼吸感，留白很重要。密度高的代码虽然"省纸张"，但可读性差。给代码留点空间，让它"喘口气"。

```python
# 密集（让人窒息）
def greet(names): return [f"Hello, {n}!" for n in names if n.strip()]

# 稀疏（有呼吸感）
def greet(names):
    return [
        f"Hello, {name}!"
        for name in names
        if name.strip()
    ]
```

### 1.4.1.7 Readability counts.

**可读性很重要。**

代码是给人看的，顺便给机器执行。变量的命名、注释、代码结构，都应该为可读性服务。

```python
# 不可读
p = 3.14159
r = 5
c = 2 * p * r

# 可读
PI = 3.14159
radius = 5
circumference = 2 * PI * radius
```

### 1.4.1.8 Special cases aren't special enough to break the rules.

**特殊不足以打破规则。**

规则是团队协作的基础。偶尔一次"就特殊一下"可能带来技术债务的积累，最终导致规则形同虚设。

### 1.4.1.9 Although practicality beats purity.

**实用优于纯粹。**

规则是死的，代码是活的。完全遵守规则但做不出有用的东西，那规则还有什么意义？Python 鼓励务实——规则是指导方针，不是枷锁。

### 1.4.1.10 Errors should never pass silently.

**错误不应静默通过。**

吞掉错误信息是程序员最常见的错误之一。程序出了错，就应该大声喊出来，而不是悄悄跳过。

```python
# 错误：静默忽略异常
try:
    result = dangerous_operation()
except:
    pass  # 什么都不知道...

# 正确：至少记录日志
import logging
try:
    result = dangerous_operation()
except Exception as e:
    logging.error(f"操作失败: {e}")
    raise
```

### 1.4.1.11 Unless explicitly silenced.

**除非显式地沉默。**

有些错误是可以忽略的，但这种忽略必须是**显式的**——用代码告诉后来者"我知道这里可能出错，但我选择忽略它"。

```python
# 用 empty except 块+注释说明原因
try:
    result = config.get("optional_key")
except KeyError:
    pass  # optional_key 不存在是正常的，使用默认值即可
```

### 1.4.1.12 In the face of ambiguity, refuse the temptation to guess.

**面对歧义时，拒绝猜测的诱惑。**

如果代码的行为不确定，不要靠"猜测"来写，而是要搞清楚逻辑、查阅文档、问清楚需求。猜测是 bug 的温床。

### 1.4.1.13 There should be one-- and preferably only one --obvious way to do it.

**应该有一种——最好只有一种——显而易见的实现方式。**

Python 追求"唯一正确答案"。同样一个功能，应该只有一种最 Pythonic 的写法。这减少了团队内部的分歧，也让代码更容易维护。

```python
# Pythonic：一种明显的方式
result = [x for x in items if x > 0]

# 非 Pythonic：可以用很多种方式，但都不如上面直观
result = []
for x in items:
    if x > 0:
        result.append(x)
```

### 1.4.1.14 Although that way may not be obvious at first unless you're Dutch.

**虽然除非你是荷兰人，否则那种方式一开始可能并不明显。**

这是 Guido van Rossum 的"私货"——因为他是荷兰人。这句话的意思是：Python 的设计哲学有时候需要一段时间才能理解，但一旦理解，就会觉得"嗯，确实是这样"。

### 1.4.1.15 Now is better than never.

**现在优于永远不做。**

与其等到"完美方案"出现，不如现在就开始做。迭代比等待更重要。

### 1.4.1.16 Although never is often better than *right* now.

**但永远不做通常优于仓促行动。**

做之前要想清楚。冲动编码是另一个极端——有时候"不动"比"乱动"更明智。

这两句话看似矛盾，其实是一个**平衡**：不要永远不做，也不要冲动去做。

### 1.4.1.17 If the implementation is hard to explain, it's a bad idea.

**如果实现很难解释，它就是个坏主意。**

好的设计应该是"显而易见的"。如果你需要长篇大论来解释你的实现，说明这个设计有问题——或者你根本就没想清楚。

### 1.4.1.18 If the implementation is easy to explain, it may be a good idea.

**如果实现很容易解释，它可能是个好主意。**

好的想法通常是简单的。如果你发现自己的想法/实现可以用三句话解释清楚，那大概率是个好想法。

### 1.4.1.19 Namespaces are one honking great idea -- let's do more of those!

**命名空间是一个绝妙的主意——让我们多用它！**

**命名空间**（Namespace）就是"把名字隔离在特定区域"的机制。比如 `math.pi` 和 `mymodule.pi` 是两个不同的 `pi`，因为它们在不同的命名空间里。

```python
import math
import mymodule

print(math.pi)       # 3.141592653589793
print(mymodule.pi)   # 可能是 3.14，或者别的什么
```

命名空间的好处是：避免名字冲突，让代码模块化。

## 1.4.2 Python 之禅在编码实践中的应用

Python 之禅不是挂在墙上的标语，而是可以落实到每一行代码的指导原则。以下是一些实践例子：

**实践 1：让代码"自我解释"**

```python
# 不好的写法
if status == 200 and not error and data is not None:
    process(data)

# 好的写法（利用函数提取意图）
def is_success(response):
    return response.status == 200 and not response.error and response.data is not None

if is_success(response):
    process(response.data)
```

**实践 2：显式优于隐式**

```python
# 不好：隐式依赖
def calculate_stats(numbers):
    global total
    total = sum(numbers)
    return total / len(numbers)

# 好：显式参数和返回值
def calculate_stats(numbers):
    total = sum(numbers)
    count = len(numbers)
    return total / count if count > 0 else 0
```

**实践 3：简单优先，但不过度简化**

```python
# 过度简化（反而更难懂）
result = dict(zip(keys, map(lambda x: x*2, values)))

# 平衡的写法
doubled_values = [v * 2 for v in values]
result = dict(zip(keys, doubled_values))
```

---

# 1.5 Python 的应用领域

Python 的应用领域广泛到让人怀疑它是不是"万金油"——但它确实就是这么厉害。让我来一一介绍。

## 1.5.1 Web 后端开发（Django、Flask、FastAPI）

Python 有三大 Web 框架：

- **Django**：大型 Web 框架，"MTV"（Model-Template-View）架构，自带 admin 管理后台、ORM、表单处理等。适合快速开发大型网站。Instagram、Pinterest、Disqus 都是 Django 的代表作。
- **Flask**：微型框架，核心简单，扩展丰富。Flask 的哲学是"给你基本的功能，剩下的你来选"。适合小型应用、原型开发、微服务。
- **FastAPI**：新生代框架，基于类型提示、自动文档、异步支持三大杀手锏。FastAPI 的性能逼近 Node.js 和 Go，是现代 API 开发的热门选择。

```python
# Flask 最简单的 Web 应用
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, Python Web!"

if __name__ == "__main__":
    app.run(debug=True)
```

```python
# FastAPI 示例
from fastapi import FastAPI

app = FastAPI()

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
```

## 1.5.2 数据科学与数据分析（NumPy、Pandas、Matplotlib）

Python 是**数据科学领域**的霸主。这三剑客分工明确：

- **NumPy**（Numerical Python）：提供高性能的多维数组（ndarray）和数学运算函数。是几乎所有科学计算库的基础。
- **Pandas**：提供 DataFrame（二维表格数据）和 Series（一维数据）数据结构，以及强大的数据清洗、聚合、统计分析功能。
- **Matplotlib**：最流行的 Python 可视化库，画折线图、柱状图、热力图都不在话下。

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# NumPy：数值计算
arr = np.array([[1, 2, 3], [4, 5, 6]])
print(arr.sum(axis=1))  # [ 6 15]

# Pandas：数据分析
df = pd.DataFrame({
    "姓名": ["小明", "小红", "小李"],
    "数学": [95, 88, 92],
    "语文": [90, 85, 88]
})
print(df["数学"].mean())  # 91.6666...

# Matplotlib：可视化
df.plot(kind="bar", x="姓名", y=["数学", "语文"])
plt.title("成绩对比")
plt.show()
```

## 1.5.3 人工智能与机器学习（TensorFlow、PyTorch、scikit-learn）

Python 在 AI/ML 领域是绝对的王者：

- **TensorFlow**：Google 出品的深度学习框架，适合生产环境部署。
- **PyTorch**：Facebook 出品的深度学习框架，动态计算图让研究更灵活。PyTorch 近年来在学术界越来越受欢迎。
- **scikit-learn**：经典机器学习库，提供分类、回归、聚类、降维等算法。

```python
# PyTorch 简单示例
import torch

x = torch.tensor([[1.0], [2.0], [3.0]])
y = torch.tensor([[2.0], [4.0], [6.0]])

# 线性回归模型
model = torch.nn.Linear(1, 1)
optimizer = torch.optim.SGD(model.parameters(), lr=0.01)

for epoch in range(1000):
    pred = model(x)
    loss = torch.nn.functional.mse_loss(pred, y)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

print(model.weight.item(), model.bias.item())  # 接近 2.0 和 0.0
```

## 1.5.4 大语言模型（LLM）与 AI Agent（LangChain、OpenAI SDK）

2023 年开始，AI 大模型爆发，Python 凭借其生态优势成为 **LLM 应用开发**的首选语言：

- **OpenAI SDK**：调用 GPT 系列模型的最官方工具。
- **LangChain**：构建 LLM 应用的框架，提供 Agent、Chain、Memory 等抽象。
- **LlamaIndex**：知识检索增强（RAG）的利器。
- **transformers**：Hugging Face 的模型库，托管了数万预训练模型。

```python
# OpenAI SDK 简单示例
from openai import OpenAI

client = OpenAI(api_key="your-api-key")

response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "你是 Python 助手"},
        {"role": "user", "content": "解释一下什么是装饰器"}
    ]
)
print(response.choices[0].message.content)
```

```python
# LangChain 示例（简版）
from langchain_openai import ChatOpenAI
from langchain.agents import AgentType, initialize_agent, load_tools

llm = ChatOpenAI(model="gpt-4")
tools = load_tools(["serpapi"])
agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION)
agent.run("2024 年诺贝尔物理学奖得主是谁？")
```

## 1.5.5 自动化测试（pytest、Selenium、Playwright）

Python 是测试工程师的最爱：

- **pytest**：最流行的 Python 测试框架，支持断言、fixture、参数化、插件生态。
- **Selenium**：浏览器自动化测试工具，可以模拟用户在浏览器里的操作。
- **Playwright**：微软出品的现代浏览器自动化工具，比 Selenium 更强大、更快。

```python
# pytest 示例
import pytest

def add(a, b):
    return a + b

def test_add_positive():
    assert add(1, 2) == 3

def test_add_negative():
    assert add(-1, -1) == -2

def test_add_mixed():
    assert add(-1, 1) == 0
```

```python
# Selenium 示例
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get("https://www.python.org")
search_box = driver.find_element(By.NAME, "q")
search_box.send_keys("python")
search_box.submit()
print(driver.title)
driver.quit()
```

## 1.5.6 浏览器自动化与爬虫（Selenium、Playwright、Scrapy）

Python 是**爬虫领域的传统豪强**：

- **Scrapy**：最专业的 Python 爬虫框架，支持异步、分布式、中间件管道。
- **Selenium/Playwright**：JS 渲染页面的克星——遇到"这是 JavaScript 生成的，我们拿不到数据"的时候，它们就是救星。
- **BeautifulSoup + Requests**：轻量级爬虫组合，适合简单的页面抓取。

```python
# Scrapy 示例（scrapy startproject 后在 spiders 里写）
import scrapy

class PythonDocsSpider(scrapy.Spider):
    name = "python_docs"
    start_urls = ["https://docs.python.org/3/"]
    
    def parse(self, response):
        for title in response.css("h2::text").getall():
            yield {"title": title.strip()}
```

```python
# Playwright 示例
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://example.com")
    print(page.title())
    browser.close()
```

## 1.5.7 网络编程与 API 开发（asyncio、aiohttp、FastAPI）

Python 3.5+ 的 `asyncio` 让高并发网络编程变得简单：

- **asyncio**：Python 内置的异步 I/O 框架，单线程高并发。
- **aiohttp**：异步 HTTP 客户端和服务端框架。
- **FastAPI**：基于 Starlette 的异步 Web 框架，性能极高。

```python
# aiohttp 异步 HTTP 客户端
import aiohttp
import asyncio

async def fetch_all(urls):
    async with aiohttp.ClientSession() as session:
        async def fetch(url):
            async with session.get(url) as response:
                return await response.text()
        
        tasks = [fetch(url) for url in urls]
        return await asyncio.gather(*tasks)

urls = ["https://httpbin.org/get", "https://httpbin.org/ip"]
results = asyncio.run(fetch_all(urls))
print(len(results))  # 2
```

## 1.5.8 脚本与系统工具开发（Click、Typer、Rich）

Python 是写**系统脚本**的好帮手：

- **Click**：命令行应用构建框架，比 argparse 更优雅。
- **Typer**：基于类型提示的命令行框架，用法接近 FastAPI。
- **Rich**：终端美化库，可以输出彩色文字、表格、进度条。

```python
# Click 示例
import click

@click.command()
@click.option("--name", default="World", help="打招呼的名字")
@click.option("--count", "-c", default=1, help="重复次数")
def hello(name, count):
    """一个简单的打招呼命令"""
    for _ in range(count):
        click.echo(f"你好，{name}！")

hello()
```

```python
# Rich 示例
from rich.console import Console
from rich.table import Table

console = Console()

table = Table(title="编程语言排行")
table.add_column("语言", style="cyan")
table.add_column("排名", style="magenta")
table.add_column("分数", justify="right")

table.add_row("Python", "1", "31.62%")
table.add_row("C", "2", "17.09%")
table.add_row("Java", "3", "12.12%")

console.print(table)
```

## 1.5.9 云计算与 DevOps（Docker、Ansible、CI/CD）

Python 在运维领域同样活跃：

- **Ansible**：最流行的自动化运维工具，用 YAML 写 playbook，底层是 Python。
- **Docker SDK for Python**：直接用 Python 操作 Docker 容器。
- **Boto3**：AWS SDK for Python，操作亚马逊云服务。
- **CI/CD**：GitHub Actions、GitLab CI、Jenkins，都支持 Python 脚本。

```python
# boto3 示例（操作 AWS S3）
import boto3

s3 = boto3.client("s3")

# 列出所有 bucket
response = s3.list_buckets()
for bucket in response["Buckets"]:
    print(bucket["Name"])

# 上传文件
s3.upload_file("local_file.txt", "my-bucket", "remote_file.txt")
```

## 1.5.10 游戏开发（Pygame、Godot-Python）

Python 在游戏开发领域也有存在感：

- **Pygame**：最流行的 Python 游戏库，适合 2D 小游戏、教学演示、原型开发。
- **Godot-Python**：在 Godot 游戏引擎里使用 Python 脚本。
- **Panda3D**：3D 游戏引擎，支持 Python。
- **PyOgre**：Python 绑定 OGRE 3D 渲染引擎。

```python
# Pygame 最简单的窗口示例
import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("我的第一个 Pygame 窗口")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.flip()
```

## 1.5.11 图形界面开发（PyQt、Tkinter）

Python 可以开发桌面 GUI 应用：

- **Tkinter**：Python 内置的 GUI 库，最简单，但界面比较朴素。
- **PyQt/PySide**：Qt 框架的 Python 绑定，功能强大，界面美观。商业项目常用。
- **wxPython**：wxWidgets 的 Python 绑定，跨平台原生外观。
- **Kivy**：跨平台 GUI 框架，支持触摸操作，可以打包成移动 APP。

```python
# Tkinter 最简单的 GUI
import tkinter as tk

root = tk.Tk()
root.title("我的第一个 GUI 程序")
root.geometry("300x200")

label = tk.Label(root, text="你好，Python GUI！", font=("Arial", 20))
label.pack(pady=50)

button = tk.Button(root, text="点我", command=lambda: label.config(text="你点了我！"))
button.pack()

root.mainloop()
```

## 1.5.12 区块链与密码学（web3.py、cryptography）

Python 在区块链和密码学领域也有应用：

- **web3.py**：以太坊区块链交互库，可以读写智能合约、发送交易。
- **cryptography**：最通用的密码学库，提供对称加密、非对称加密、哈希、签名等功能。
- **PyCryptodome**：另一个密码学库，比 cryptography 更轻量。

```python
# web3.py 简单示例
from web3 import Web3

w3 = Web3(Web3.HTTPProvider("https://mainnet.infura.io/v3/YOUR_PROJECT_ID"))
print(f"最新区块号: {w3.eth.block_number}")

# 获取某个地址的 ETH 余额
balance = w3.eth.get_balance("0x742d35Cc6634C0532925a3b844Bc9e7595f8dE21")
print(f"余额（ETH）: {w3.fromWei(balance, 'ether')}")
```

```python
# cryptography 示例
from cryptography.fernet import Fernet

# 生成密钥
key = Fernet.generate_key()
cipher = Fernet(key)

# 加密
encrypted = cipher.encrypt(b"Python 密码学真有趣！")
print(f"加密后: {encrypted}")

# 解密
decrypted = cipher.decrypt(encrypted)
print(f"解密后: {decrypted}")  # b'Python 密码学真有趣！'
```

---

# 本章小结

恭喜你完成了"Python 的前世今生"这一章的学习！让我们来回顾一下本章的核心要点：

## 核心要点总结

### 1. Python 的诞生
- **创始人**：Guido van Rossum（龟叔），荷兰程序员，数学和计算机双料硕士
- **诞生时间**：1991 年 12 月，起点是 Python 0.9.0
- **诞生地点**：荷兰 CWI（国家数学与计算机科学研究所）
- **名字由来**：Monty Python's Flying Circus（Guido 最喜欢的 BBC 喜剧节目），和蛇没关系
- **设计哲学**：简洁、易读、可扩展——这三条至今没变

### 2. Python 发展史里程碑
- **1991**：Python 0.9.0 诞生——类、异常、函数、列表、模块系统
- **1994**：Python 1.0——引入 lambda、map/filter/reduce、复数
- **2000**：Python 2.0——列表推导式、垃圾回收、Unicode、PEP 机制
- **2004**：Python 2.4——生成器（yield）、装饰器语法糖
- **2008**：Python 3.0——破坏性升级，print 函数、Unicode 默认、除法改革
- **2012**：Python 3.3——venv 虚拟环境、命名空间包
- **2014**：Python 3.4——asyncio、pip 成为推荐包管理器
- **2015**：Python 3.5——typing 模块、async/await、@ 运算符
- **2016**：Python 3.6——f-string、变量注解、secrets 模块
- **2018**：Python 3.7——dataclass、asyncio.run()、contextvars
- **2019**：Python 3.8——海象运算符 :=、f-string = 说明符、位置关键字分隔符
- **2020**：Python 3.9——字典合并运算符 |、内置类型泛型、ZoneInfo
- **2021**：Python 3.10——match...case、精确错误提示
- **2022**：Python 3.11——异常组（except*）、TaskGroup、启动速度优化
- **2023**：Python 3.12——JIT 进展、f-string 调试改进
- **2024**：Python 3.13——实验性 JIT、交互式解释器彩色输出
- **2025**：Python 3.14——持续优化中

### 3. Python 2 vs Python 3
- Python 2.7 于 **2020 年 1 月 1 日**正式停更
- Python 3 是破坏性升级，不兼容 Python 2
- `2to3.py` 是官方迁移工具，但不能解决所有问题
- Unicode 默认化、print 函数化、除法改革是最核心的变动

### 4. Python 之禅（The Zen of Python）
最核心的几条：
- **美优于丑**（Beautiful is better than ugly）
- **显优于隐**（Explicit is better than implicit）
- **简单优于复杂**（Simple is better than complex）
- **可读性很重要**（Readability counts）
- **错误不应静默**（Errors should never pass silently）
- **应该只有一种显而易见的方式**（There should be one-- and preferably only one --obvious way to do it）

### 5. Python 的应用领域
Python 的应用领域非常广泛：Web 后端、数据科学、AI/ML、LLM/Agent、自动化测试、爬虫、网络编程、脚本工具、DevOps、游戏、GUI开发区块链……几乎无所不能。

> 一句话总结：Python 从 1991 年的一条小蛇，已经成长为 2026 年吞天巨蟒。它用简洁优雅的语法、强大的标准库、活跃的社区，服务了全球数千万开发者。Python 的故事还在继续，而你，正在成为这个故事的一部分。

**下一章，我们将正式开始学习 Python 语法，从环境搭建开始，一步步成为 Python 高手！准备好了吗？**
