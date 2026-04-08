+++
title = "第15章 进阶语法"
weight = 150
date = "2026-04-08T13:22:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 第十五章：Python 高级语法

> 🎭 欢迎来到 Python 的"成人区"！前面十四章你学会了走路，这一章我们要学跑酷、漂移、甚至飞檐走壁！
>
> 别怕，我会像教小孩用筷子一样耐心地解释每一个知识点。幽默、风趣、深入浅出——这就是我们的风格！

---

## 15.1 类型提示完整教程

### 15.1.1 基本类型标注（x: int）

**类型提示**（Type Hint）是 Python 3.5 引入的特性，它允许你给变量、函数参数和返回值标注期望的类型。这不是强制的——Python 还是那个自由的 Python，但标注后，IDE 能给你智能提示，静态检查工具能帮你提前发现 bug。

```python
# 基本类型标注，格式：变量名: 类型
name: str = "张三"
age: int = 25
height: float = 1.75
is_student: bool = True

# 函数参数和返回值标注
def greet(name: str) -> str:
    """向某人打招呼"""
    return f"你好，{name}！"

print(greet("小明"))  # 你好，小明！
print(greet(123))    # 运行时不报错，但类型检查器会报警告！
```

> 💡 **这是什么感觉？** 就像你给外卖小哥说了你的地址，他就能精准送餐。类型提示就是给 Python 解释器的"地址标签"！

```python
# 没有类型提示时，Python 像一个佛系的外卖小哥
# "您的意思是...让我猜？"
# 有了类型提示后，他变成了一个GPS精确定位的老司机
```

**小白的疑问**：加了类型提示会不会变慢？

**答**：完全不会！类型提示是**编译时**（实际上我们叫"书写时"）检查的，运行时 Python 根本不 care 它。类型提示就像注释，只有人类阅读，解释器直接忽略。

---

### 15.1.2 Union 类型（Union[int, str] / int | str）

**Union 类型**表示"可以是几种类型中的任意一种"。就像你上班用的交通工具，可以是地铁、公交、或者骑共享单车。

```python
from typing import Union

# Union[A, B] 表示"可以是 A 类型或者 B 类型"
def process_value(value: Union[int, str]) -> str:
    """处理整数或字符串"""
    return f"收到：{value}"

print(process_value(42))      # 收到：42
print(process_value("hello")) # 收到：hello
# print(process_value([1, 2]))  # 类型检查器会报错！
```

**Python 3.10+ 现代写法**：

```python
# 使用 | 操作符，更直观！
def process_value(value: int | str) -> str:
    """处理整数或字符串 - 现代写法"""
    return f"收到：{value}"

print(process_value(42))      # 收到：42
print(process_value("hello")) # 收到：hello
```

> 🎯 **什么时候用 Union？** 当一个东西"不只有一个可能的类型"时。比如用户ID，可能是整数（直接输入），也可能是字符串（扫码）。

---

### 15.1.3 Optional 类型（Optional[str] / str | None）

**Optional 类型**是 Union 的语法糖，专门表示"可以是某种类型，也可以是 None"。想象一个可选的停车场——要么有车停，要么什么都没有（None）。

```python
from typing import Optional

# Optional[str] 等价于 Union[str, None]
def find_user(user_id: int) -> Optional[str]:
    """根据ID查找用户名，找不到返回None"""
    users = {1: "张三", 2: "李四", 3: "王五"}
    return users.get(user_id)  # 找不到返回 None

result1 = find_user(1)
print(result1)   # 张三
result2 = find_user(99)  # 不存在的ID
print(result2)  # None
```

**Python 3.10+ 现代写法**：

```python
# 使用 | None 更直观
def find_user(user_id: int) -> str | None:
    """查找用户 - 现代写法"""
    users = {1: "张三", 2: "李四"}
    return users.get(user_id)

print(find_user(99))  # None
```

> 🤔 **Optional vs Union[str, None]**：功能完全一样！Optional 只是更语义化的写法，读起来像"可选的"。

---

### 15.1.4 Any 类型

**Any 类型**是类型系统中的"全能选手"，它表示"可以是任何类型"。使用 Any 等于告诉类型检查器："这玩意儿啥类型都有可能，别检查了！"

```python
from typing import Any

def printanything(obj: Any) -> None:
    """打印任何东西"""
    print(f"类型是 {type(obj).__name__}，值是 {obj}")

printanything(42)        # 类型是 int，值是 42
printanything("hello")  # 类型是 str，值是 hello
printanything([1, 2, 3])  # 类型是 list，值是 [1, 2, 3]
```

**重要原则**：Any 是"万金油"，但也是"偷懒神器"。滥用 Any 会让类型提示形同虚设，就像你给医生说"随便给我开点药"一样。

```python
# ❌ 滥用 Any - 类型提示毫无意义
def process(data: Any) -> Any:
    return data

# ✅ 尽量具体 - 告诉 Python 你要什么
def process(data: int | str | list) -> int | str | list:
    return data
```

> 💀 **警告**：如果你写 `x: Any = 10`，然后 `x.split()`，类型检查器不报错，但运行时你会得到 `AttributeError: 'int' object has no attribute 'split'`！这就像你告诉警察"我没违法"然后继续做坏事——迟早翻车。

---

### 15.1.5 Callable 类型

**Callable 类型**表示"可调用的东西"——函数、方法、lambda 表达式都可以是 Callable。就像"能吃的东西"可以包括米饭、面条、包子一样。

```python
from typing import Callable

# Callable[[参数类型1, 参数类型2], 返回类型]
def apply_func(func: Callable[[int, int], int], a: int, b: int) -> int:
    """应用一个双参数函数"""
    return func(a, b)

def add(x: int, y: int) -> int:
    return x + y

def multiply(x: int, y: int) -> int:
    return x * y

print(apply_func(add, 3, 4))       # 7
print(apply_func(multiply, 3, 4))  # 12

# 使用 lambda
print(apply_func(lambda x, y: x - y, 10, 3))  # 7
```

**无参数 Callable**：

```python
from typing import Callable

def call_twice(func: Callable[[], None]) -> None:
    """调用一个无参数函数两次"""
    func()
    func()

def say_hello() -> None:
    print("你好！")

call_twice(say_hello)
# 你好！
# 你好！
```

> 🎪 **Callable 的应用场景**：回调函数、事件处理、策略模式。想象你有个"万能按钮"，你不知道按下去会发生什么，但你知道它能被"按"（调用）。

---

### 15.1.6 List / Dict / Set / Tuple 泛型标注

**泛型**（Generic）听起来高大上，其实就是"带参数的类型"。就像"水果"是类型，"苹果"、"香蕉"是具体的泛型参数。

```python
from typing import List, Dict, Set, Tuple

# List[int] - 整数列表
def sum_list(numbers: List[int]) -> int:
    """求列表所有元素之和"""
    return sum(numbers)

print(sum_list([1, 2, 3, 4, 5]))  # 15

# Dict[str, int] - 键是字符串，值是整数
def word_count(text: str) -> Dict[str, int]:
    """统计单词出现次数"""
    words = text.split()
    return {word: words.count(word) for word in set(words)}

print(word_count("hello world hello"))  # {'hello': 2, 'world': 1}

# Set[int] - 整数集合
def unique_squares(nums: Set[int]) -> Set[int]:
    """返回不重复的平方数"""
    return {x ** 2 for x in nums}

print(unique_squares({1, 2, 2, 3}))  # {1, 4, 9}

# Tuple[int, str, float] - 元组类型，每个位置的类型必须匹配
def get_user_info() -> Tuple[str, int, float]:
    """返回用户信息元组"""
    return ("张三", 25, 1.75)

name, age, height = get_user_info()
print(f"{name}，{age}岁，身高{height}m")  # 张三，25岁，身高1.75m
```

> 🌟 **元组 vs 列表**：列表是"可变队列"（长度可变），元组是"固定容器"（像火车车厢，一节一节固定好）。元组用 `Tuple` 标注时，每个位置的类型都要写清楚。

---

### 15.1.7 内置类型泛型（list[int]，Python 3.9+）

Python 3.9 之前，我们必须用 `List[int]`、`Dict[str, int]` 这种写法。3.9 之后，你可以直接用内置类型作为泛型——更简洁、更直观！

```python
# Python 3.9+ 现代写法
def sum_list(numbers: list[int]) -> int:
    """求列表元素和"""
    return sum(numbers)

def word_count(text: str) -> dict[str, int]:
    """统计单词"""
    words = text.split()
    return {word: words.count(word) for word in set(words)}

def get_coords() -> tuple[int, int]:
    """返回坐标"""
    return (100, 200)

print(sum_list([1, 2, 3]))  # 6
```

> ✅ **推荐**：如果你用 Python 3.9+，直接用内置类型泛型！`list[int]` 比 `List[int]` 更简洁、更好看！

**新旧写法对比**：

```python
# 旧时代 (Python 3.5 - 3.8)
from typing import List, Dict, Set, Tuple

def old_style(items: List[int], mapping: Dict[str, int]) -> Tuple[int, str]:
    pass

# 新时代 (Python 3.9+)
def new_style(items: list[int], mapping: dict[str, int]) -> tuple[int, str]:
    pass
```

---

### 15.1.8 TypeVar 类型变量

**TypeVar**（类型变量）就像一个"类型世界的变量"，它让泛型函数更灵活。想象你有个万能模具，往里面倒什么材料就出什么产品。

```python
from typing import TypeVar

# 定义一个类型变量
T = TypeVar('T')

def first_element(lst: list[T]) -> T | None:
    """返回列表第一个元素"""
    return lst[0] if lst else None

# T 被推导为 str
result1 = first_element(["a", "b", "c"])
print(result1)  # a

# T 被推导为 int
result2 = first_element([1, 2, 3])
print(result2)  # 1

# T 被推导为 float
result3 = first_element([1.5, 2.5])
print(result3)  # 1.5
```

**多类型变量**：

```python
from typing import TypeVar

K = TypeVar('K')
V = TypeVar('V')

def get_value(d: dict[K, V], key: K) -> V | None:
    """从字典获取值"""
    return d.get(key)

ages = {"张三": 25, "李四": 30}
print(get_value(ages, "张三"))  # 25
print(get_value(ages, "王五"))  # None
```

> 🎭 **TypeVar 的精髓**：它让你写出的函数能"自动适应"不同类型，而不是写死类型。就像一个万能钥匙，能开多种锁。

---

### 15.1.9 Protocol 结构化子类型

**Protocol**（协议）是 Python 3.8 引入的特性，用于定义"结构化子类型"——简单说就是"只要你有这些方法，你就是我的菜"，而不要求继承关系。

```python
from typing import Protocol

# 定义一个协议 - "能画的东西"
class Drawable(Protocol):
    def draw(self) -> None: ...
    def get_color(self) -> str: ...

# 不需要继承！只要有 draw 和 get_color 方法就行
class Circle:
    def __init__(self, radius: float):
        self.radius = radius
        self.color = "红色"

    def draw(self) -> None:
        print(f"画一个半径为 {self.radius} 的{self.color}圆")

    def get_color(self) -> str:
        return self.color

class Square:
    def __init__(self, side: float):
        self.side = side
        self.color = "蓝色"

    def draw(self) -> None:
        print(f"画一个边长为 {self.side} 的{self.color}正方形")

    def get_color(self) -> str:
        return self.color

# 任何实现了 Drawable 协议的类型都可以传进来
def render_all(drawables: list[Drawable]) -> None:
    """渲染所有能画的东西"""
    for d in drawables:
        d.draw()

circle = Circle(5)
square = Square(10)
render_all([circle, square])
# 画一个半径为 5.0 的红色圆
# 画一个边长为 10.0 的蓝色正方形
```

> 🎯 **Protocol vs 继承**：继承是"我是你的一部分"，Protocol 是"你有我需要的能力"。Protocol 更灵活，更符合"鸭子类型"（Duck Typing）的哲学——"只要它走路像鸭子，叫起来像鸭子，那它就是鸭子"。

---

### 15.1.10 泛型类与泛型函数

**泛型类**：类定义时使用类型变量，让类能操作多种类型。

```python
from typing import TypeVar

T = TypeVar('T')

class Stack:
    """泛型栈 - 什么类型都能装"""
    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        """压入元素"""
        self._items.append(item)

    def pop(self) -> T | None:
        """弹出元素"""
        return self._items.pop() if self._items else None

    def peek(self) -> T | None:
        """查看栈顶元素"""
        return self._items[-1] if self._items else None

# int 栈
int_stack = Stack[int]()
int_stack.push(1)
int_stack.push(2)
print(int_stack.pop())  # 2

# str 栈
str_stack = Stack[str]()
str_stack.push("hello")
str_stack.push("world")
print(str_stack.pop())  # world
```

**泛型函数**：

```python
from typing import TypeVar

T = TypeVar('T')

def reverse(lst: list[T]) -> list[T]:
    """反转列表"""
    return lst[::-1]

print(reverse([1, 2, 3]))        # [3, 2, 1]
print(reverse(["a", "b", "c"]))  # ['c', 'b', 'a']
print(reverse([1.5, 2.5, 3.5]))  # [3.5, 2.5, 1.5]
```

> 🏭 **泛型的意义**：想象你是个工厂老板，你要生产"能装东西的盒子"。如果你为每种类型单独建厂（int盒厂、str盒厂），成本太高。泛型就是"万能工厂"，一套模具，什么类型都能生产！

---

### 15.1.11 @overload 函数重载

**@overload** 装饰器允许你为同一个函数定义多个"签名"，让类型检查器能精确知道不同参数组合会返回什么类型。

```python
from typing import overload

@overload
def process(x: int) -> int: ...
@overload
def process(x: str) -> str: ...
@overload
def process(x: list[int]) -> int: ...

def process(x):
    """实际实现 - 只有一个函数体，overload 只是给类型检查器看的"""
    if isinstance(x, int):
        return x * 2
    elif isinstance(x, str):
        return x.upper()
    elif isinstance(x, list):
        return sum(x)
    return x

print(process(5))          # 10
print(process("hello"))     # HELLO
print(process([1, 2, 3]))   # 6
```

> ⚠️ **注意**：`@overload` 只是给类型检查器看的，实际实现只能有一个函数体。Python 运行时根本不在乎 overload，它只看得到最后的 `def process(x)`。

---

### 15.1.12 TypeAlias 类型别名

**TypeAlias** 让你给复杂类型起个好名字，提高代码可读性。就像给人起绰号——"那个特别能吃的家伙"比"体重200斤的程序员"更好记。

```python
from typing import TypeAlias, Union

# 给复杂类型起别名
Vector: TypeAlias = list[float]
Matrix: TypeAlias = list[list[float]]
UserId: TypeAlias = Union[int, str]
Response: TypeAlias = dict[str, Union[str, int, bool]]

def calculate_norm(vector: Vector) -> float:
    """计算向量模长"""
    return sum(x ** 2 for x in vector) ** 0.5

def process_response(response: Response) -> str:
    """处理API响应"""
    return f"状态：{response.get('status', 'unknown')}"

vector: Vector = [3.0, 4.0]
print(calculate_norm(vector))  # 5.0
```

> 📝 **TypeAlias vs 变量**：在 Python 3.10 之前，TypeAlias 是显式的（需要 `TypeAlias`），之后可以用简单的 `=` 赋值。不过为了兼容性，推荐用 `TypeAlias`。

---

### 15.1.13 typing.Self（Python 3.11+）

**Self** 用于标注方法返回当前类实例的类型，让你不用写死类名，继承时更灵活。

```python
class Person:
    def __init__(self, name: str) -> None:
        self.name = name

    # Python 3.11+ 用 Self
    def rename(self, new_name: str) -> Self:
        """重命名，返回自身"""
        self.name = new_name
        return self

    # 旧写法（Python 3.10 及之前）
    def clone(self: 'Person', name: str) -> 'Person':
        """创建副本"""
        return Person(name)

# Self 让你在继承时更方便
class Student(Person):
    def __init__(self, name: str, grade: int) -> None:
        super().__init__(name)
        self.grade = grade

student = Student("张三", 3)
renamed = student.rename("李四")
print(renamed.name)  # 李四
print(renamed.grade)  # 3（类型检查器知道这是 Student）
```

> 🎯 **为什么需要 Self？** 如果你用 `def rename(self, new_name: str) -> Person`，返回类型会是 `Person`。但实际对象可能是 `Student`，类型检查器就会"不高兴"。`Self` 让类型检查器知道"返回的跟调用者一样"。

---

### 15.1.14 类型提示最佳实践

```
┌─────────────────────────────────────────────────────────┐
│                  类型提示避坑指南 🧭                      │
├─────────────────────────────────────────────────────────┤
│  ✅ DO                                                │
│  ─────────────────────────────────────────────────────  │
│  • 用 Python 3.9+ 时，优先用内置泛型 list[int]           │
│  • 优先用 str | None 而不是 Optional[str]（更直观）     │
│  • 给公共 API 加类型提示，便于他人调用                   │
│  • 用 TypeAlias 给复杂类型起别名                        │
│  • 泛型函数用 TypeVar，让类型自动推导                   │
├─────────────────────────────────────────────────────────┤
│  ❌ DON'T                                             │
│  ─────────────────────────────────────────────────────  │
│  • 不要滥用 Any，它会让类型检查形同虚设                 │
│  • 不要给私有/局部变量加类型提示（没必要）              │
│  • 不要过度工程：小脚本不需要严格类型提示               │
│  • 不要忽略类型检查器的警告                             │
└─────────────────────────────────────────────────────────┘
```

**一个完整示例**：

```python
from typing import TypeVar, Protocol, Self

T = TypeVar('T')

class Drawable(Protocol):
    def draw(self) -> None: ...

class Circle:
    def __init__(self, radius: float) -> None:
        self.radius = radius

    def draw(self) -> None:
        print(f"🔴 画圆，半径 {self.radius}")

    def resize(self, factor: float) -> Self:
        self.radius *= factor
        return self

class Rectangle:
    def __init__(self, width: float, height: float) -> None:
        self.width = width
        self.height = height

    def draw(self) -> None:
        print(f"🟧 画矩形 {self.width}x{self.height}")

    def resize(self, factor: float) -> Self:
        self.width *= factor
        self.height *= factor
        return self

def render_all(drawables: list[Drawable]) -> None:
    """渲染所有可绘制图形"""
    for d in drawables:
        d.draw()

# 使用
c = Circle(5)
r = Rectangle(10, 5)
render_all([c, r])
c.resize(2).draw()  # 方法链式调用
```

> 🎉 **类型提示总结**：类型提示是给人类和工具看的，Python 运行时完全不在乎。但它能帮你——写代码时知道该传什么，调试时快速定位问题，重构时不怕改坏。养成加类型提示的习惯，你会感谢未来的自己！

---

## 15.2 match...case 结构化模式匹配（Python 3.10+）

### 15.2.1 基本 match 用法

**match...case** 是 Python 3.10 引入的结构化模式匹配语法。你可以把它理解为"高级 switch...case"，但它远比 switch 强大——能解构数据结构、绑定变量、做条件判断。

```python
def http_status(status: int) -> str:
    """根据HTTP状态码返回描述"""
    match status:
        case 200:
            return "OK - 请求成功"
        case 301:
            return "Moved Permanently - 永久重定向"
        case 404:
            return "Not Found - 页面不存在"
        case 500:
            return "Internal Server Error - 服务器错误"
        case _:
            return f"Unknown status: {status}"

print(http_status(200))  # OK - 请求成功
print(http_status(404))  # Not Found - 页面不存在
print(http_status(999))  # Unknown status: 999
```

> 🎯 **为什么需要 match...case？** 想象你在玩"角色扮演游戏"，你需要根据玩家职业决定他能做什么。`if...elif...elif` 就像一长串"如果是战士、如果是法师、如果是刺客..."，而 `match...case` 让你更优雅地表达这种逻辑。

---

### 15.2.2 case 字面量模式

字面量模式就是精确匹配具体的值——数字、字符串、布尔值等。

```python
def get_day_type(day: str) -> str:
    """判断日期类型"""
    match day:
        case "Saturday" | "Sunday":  # 或模式
            return "周末 - 躺平日"
        case "Monday" | "Tuesday" | "Wednesday" | "Thursday" | "Friday":
            return "工作日 - 打工魂燃烧"
        case _:
            return "未知日期"

print(get_day_type("Saturday"))  # 周末 - 躺平日
print(get_day_type("Monday"))   # 工作日 - 打工魂燃烧
```

**常量模式**：

```python
from enum import Enum

class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3

def get_color_name(color: Color) -> str:
    """获取颜色名称"""
    match color:
        case Color.RED:
            return "🔴 红色"
        case Color.GREEN:
            return "🟢 绿色"
        case Color.BLUE:
            return "🔵 蓝色"
        case _:
            return "未知颜色"

print(get_color_name(Color.RED))   # 🔴 红色
print(get_color_name(Color.GREEN)) # 🟢 绿色
```

---

### 15.2.3 case 变量模式（通配）

下划线 `_` 是通配符，匹配"任何东西"。也可以用变量名捕获匹配到的值。

```python
def classify(value) -> str:
    """分类值"""
    match value:
        case 0:
            return "零"
        case _:
            return f"非零值：{value}"

print(classify(0))     # 零
print(classify(42))   # 非零值：42

# 用变量捕获（但不限制类型）
def describe(value) -> str:
    """描述任意值"""
    match value:
        case int() as x if x > 0:
            return f"正整数：{x}"
        case int() as x if x < 0:
            return f"负整数：{x}"
        case 0:
            return "零"
        case str() as s:
            return f"字符串：{s}"
        case _:
            return f"其他类型：{type(value).__name__}"

print(describe(42))     # 正整数：42
print(describe(-5))    # 负整数：-5
print(describe("hi"))  # 字符串：hi
```

> 🤔 **as 关键字**：后面会详细讲。简单说 `case int() as x` 就是"匹配 int 类型，并把这个 int 值存到变量 x 里"。

---

### 15.2.4 case as 模式（别名绑定）

**as 模式**让你给匹配到的值起个别名，方便后续使用。

```python
def process_point(point: tuple) -> str:
    """处理坐标点"""
    match point:
        case (0, 0) as origin:
            return f"原点 {origin}"
        case (x, 0) as on_x_axis:
            return f"在X轴上：{on_x_axis}，x={x}"
        case (0, y) as on_y_axis:
            return f"在Y轴上：{on_y_axis}，y={y}"
        case (x, y) as anywhere:
            return f"普通点：{anywhere}，x={x}, y={y}"

print(process_point((0, 0)))      # 原点 (0, 0)
print(process_point((5, 0)))      # 在X轴上：(5, 0)，x=5
print(process_point((3, 4)))     # 普通点：(3, 4)，x=3, y=4
```

---

### 15.2.5 case | 模式或组合

使用 `|` 可以匹配多个可能值，就像"或者"的关系。

```python
def get_grade(score: int) -> str:
    """根据分数评级"""
    match score:
        case 100:
            return "🏆 满分！学神！"
        case 90 | 91 | 92 | 93 | 94 | 95 | 96 | 97 | 98 | 99:
            return "🎉 A - 优秀"
        case 80 | 81 | 82 | 83 | 84 | 85 | 86 | 87 | 88 | 89:
            return "👍 B - 良好"
        case 70 | 71 | 72 | 73 | 74 | 75 | 76 | 77 | 78 | 79:
            return "🙂 C - 中等"
        case _ if 0 <= score < 70:
            return "😢 D/F - 需努力"
        case _:
            return "❓ 无效分数"

print(get_grade(100))  # 🏆 满分！学神！
print(get_grade(85))   # 👍 B - 良好
```

---

### 15.2.6 序列模式（[x, y] / [x, *rest]）

序列模式让你解构列表、元组等序列类型。

```python
def process_command(cmd: list) -> str:
    """处理命令"""
    match cmd:
        case ["quit"]:
            return "👋 退出程序"
        case ["echo", *args]:
            return f"📢 回显：{' '.join(args)}"
        case ["print", msg]:
            return f"🖨️ 打印：{msg}"
        case ["add", x, y]:
            result = int(x) + int(y)
            return f"➕ 加法结果：{result}"
        case _:
            return f"❓ 未知命令：{cmd}"

print(process_command(["quit"]))
print(process_command(["echo", "hello", "world"]))
print(process_command(["print", "test message"]))
print(process_command(["add", "3", "5"]))
```

**解构嵌套序列**：

```python
def describe_matrix(matrix: list[list[int]]) -> str:
    """描述矩阵"""
    match matrix:
        case []:
            return "空矩阵"
        case [[x]]:
            return f"1x1 矩阵，值={x}"
        case [[x, y], [z, w]] as m2x2:
            return f"2x2 矩阵：{m2x2}"
        case [[_, _], [_, _], [_, _]] as m3x2:
            return f"3x2 矩阵：{m3x2}"
        case _:
            return "其他尺寸矩阵"

print(describe_matrix([]))
print(describe_matrix([[1]]))
print(describe_matrix([[1, 2], [3, 4]]))
```

---

### 15.2.7 映射模式（{"name": name, "age": age}）

映射模式让你解构字典，而且可以提取特定键的值。

```python
def describe_user(user: dict) -> str:
    """描述用户信息"""
    match user:
        case {"name": name, "age": age} if age >= 18:
            return f"👤 {name}，{age}岁，成年人"
        case {"name": name, "age": age}:
            return f"👤 {name}，{age}岁，未成年"
        case {"name": name}:
            return f"👤 {name}，年龄未知"
        case {"email": email}:
            return f"📧 邮箱用户：{email}"
        case _:
            return "❓ 未知用户格式"

print(describe_user({"name": "张三", "age": 25}))
print(describe_user({"name": "小明", "age": 15}))
print(describe_user({"name": "小红"}))
print(describe_user({"email": "test@example.com"}))
```

**星号捕捉剩余键**：

```python
def extract_info(data: dict) -> str:
    """提取信息"""
    match data:
        case {"user": name, **rest}:
            return f"用户：{name}，其他信息：{rest}"

print(extract_info({"user": "张三", "age": 25, "city": "北京"}))
# 用户：张三，其他信息：{'age': 25, 'city': '北京'}
```

---

### 15.2.8 类模式（Point(x, y)）

类模式让你匹配对象的具体结构，就像"如果它是 Point 类型，并且有 x、y 属性"。

```python
from dataclasses import dataclass

@dataclass
class Point:
    x: float
    y: float

@dataclass
class Circle:
    center: Point
    radius: float

def describe_shape(shape) -> str:
    """描述形状"""
    match shape:
        case Point(0, 0):
            return "📍 原点"
        case Point(x, 0):
            return f"📍 在X轴上，x={x}"
        case Point(0, y):
            return f"📍 在Y轴上，y={y}"
        case Point(x, y):
            return f"📍 普通点 ({x}, {y})"
        case Circle(Point(cx, cy), r):
            return f"⭕ 圆心({cx}, {cy})，半径={r}"
        case _:
            return "❓ 未知形状"

p1 = Point(0, 0)
p2 = Point(5, 3)
c = Circle(Point(1, 1), 5)

print(describe_shape(p1))
print(describe_shape(p2))
print(describe_shape(c))
```

---

### 15.2.9 guard 守卫条件（if x > 0）

**guard（守卫）**是在 case 后面加的 `if` 条件，让匹配更精确。

```python
def classify_number(n: int) -> str:
    """分类数字"""
    match n:
        case n if n > 0 and n % 2 == 0:
            return f"✅ 正偶数：{n}"
        case n if n > 0 and n % 2 != 0:
            return f"🔵 正奇数：{n}"
        case 0:
            return "⚪ 零"
        case n if n < 0 and n % 2 == 0:
            return f"❄️ 负偶数：{n}"
        case n if n < 0:
            return f"🔴 负奇数：{n}"

print(classify_number(4))   # ✅ 正偶数：4
print(classify_number(7))   # 🔵 正奇数：7
print(classify_number(0))   # ⚪ 零
print(classify_number(-6))  # ❄️ 负偶数：-6
```

**结合类模式和守卫**：

```python
from dataclasses import dataclass

@dataclass
class User:
    name: str
    age: int
    role: str

def check_access(user: User, resource: str) -> str:
    """检查用户访问权限"""
    match (user, resource):
        case (User(name, age, "admin"), _):
            return f"👑 {name}（管理员）可以访问所有资源"
        case (User(name, age, "moderator"), "forum" | "comments"):
            return f"🛡️ {name}（版主）可以访问 {resource}"
        case (User(name, age, role), _) if age >= 18:
            return f"✅ {name}（{role}）已成年，可以访问 {resource}"
        case (User(name, age, role), _) if age < 18:
            return f"⛔ {name}（{role}）未成年，无法访问 {resource}"
        case _:
            return "❓ 未知情况"

admin = User("张三", 30, "admin")
teen = User("小明", 16, "member")
adult = User("李四", 25, "member")

print(check_access(admin, "users"))
print(check_access(teen, "forum"))
print(check_access(adult, "profile"))
```

---

### 15.2.10 实战：HTTP 路由、JSON 解析、命令解析

#### HTTP 路由

```python
from dataclasses import dataclass

@dataclass
class Request:
    method: str
    path: str
    body: dict | None = None

def route(request: Request) -> str:
    """简单的HTTP路由"""
    match (request.method, request.path):
        case ("GET", "/"):
            return "🏠 首页"
        case ("GET", "/users"):
            return "👥 用户列表"
        case ("GET", "/users/" + str(user_id)):
            return f"👤 用户 {user_id} 的详情"
        case ("POST", "/users") if request.body:
            return f"➕ 创建用户：{request.body.get('name', '未知')}"
        case ("PUT", "/users/" + str(user_id)) if request.body:
            return f"✏️ 更新用户 {user_id}：{request.body}"
        case ("DELETE", "/users/" + str(user_id)):
            return f"🗑️ 删除用户 {user_id}"
        case (method, path):
            return f"❌ 404 - {method} {path} 未找到"

# 测试
reqs = [
    Request("GET", "/"),
    Request("GET", "/users"),
    Request("GET", "/users/42"),
    Request("POST", "/users", {"name": "新用户"}),
]

for req in reqs:
    print(f"{req.method} {req.path} -> {route(req)}")
```

#### JSON 解析

```python
def parse_json_value(data) -> str:
    """解析JSON值"""
    match data:
        case None:
            return "null"
        case bool() as b:
            return f"布尔值：{b}"
        case int() as i:
            return f"整数：{i}"
        case float() as f:
            return f"浮点数：{f}"
        case str() as s:
            return f"字符串：{s}"
        case list() as arr:
            items = ", ".join(parse_json_value(item) for item in arr[:3])
            suffix = "..." if len(arr) > 3 else ""
            return f"数组[{len(arr)}]：[{items}{suffix}]"
        case dict() as obj:
            keys = ", ".join(obj.keys())
            return f"对象{{{len(obj)}}个键：{keys}}"
        case _:
            return "未知类型"

import json
json_str = '{"name": "张三", "age": 25, "scores": [90, 85, 92], "active": true}'
data = json.loads(json_str)
print(parse_json_value(data))
# 对象{4个键：name, age, scores, active}
```

#### 命令行命令解析

```python
from dataclasses import dataclass

@dataclass
class Command:
    name: str
    args: list[str]
    flags: dict[str, bool]

def parse_command(input_str: str) -> Command:
    """解析命令行输入"""
    parts = input_str.strip().split()
    name = parts[0] if parts else ""
    args = []
    flags = {}

    for part in parts[1:]:
        if part.startswith("--"):
            flags[part[2:]] = True
        elif part.startswith("-"):
            for c in part[1:]:
                flags[c] = True
        else:
            args.append(part)

    return Command(name, args, flags)

def execute(cmd: Command) -> str:
    """执行命令"""
    match cmd:
        case Command("ls", [], flags) if flags.get("l"):
            return "📋 详细列表模式"
        case Command("ls", [], _):
            return "📄 普通列表模式"
        case Command("ls", path, _):
            return f"📂 列出目录：{path}"
        case Command("git", ["commit"], flags) if flags.get("m"):
            return "📝 提交（带消息）"
        case Command("git", ["commit"], _):
            return "📝 提交（无消息）"
        case Command("git", ["push"], _):
            return "⬆️ 推送到远程"
        case Command("rm", files, flags) if flags.get("r") and flags.get("f"):
            return f"💀 强制递归删除：{files}"
        case Command("rm", files, _):
            return f"⚠️ 删除文件（确认）：{files}"
        case _:
            return f"❓ 未知命令：{cmd.name}"

cmds = [
    "ls -la",
    "ls /home",
    "git commit -m 'fix bug'",
    "git push",
    "rm -rf /tmp/test",
]

for cmd_str in cmds:
    cmd = parse_command(cmd_str)
    print(f"$ {cmd_str}")
    print(f"  -> {execute(cmd)}\n")
```

> 🎉 **match...case 总结**：它是 Python 史上最重要的语法添加之一（仅次于 `with` 语句）。它让你用声明式的方式处理各种情况，比一堆 `if...elif` 优雅一万倍！

---

## 15.3 with 语句与上下文管理器

### 15.3.1 with 语句的作用

**with 语句**是 Python 的"自动 cleanup"机制。想象你租了一间酒店房间，无论你正常退房还是出了故障临时走人，都需要有人帮你收拾。with 就是那个"自动收拾房间的服务员"。

```python
# with 之前：手动管理资源
file = open("test.txt", "w")
file.write("Hello")
file.close()  # 忘了 close 就麻烦了！

# with 之后：自动管理资源
with open("test.txt", "w") as file:
    file.write("Hello")
# 出了 with 块，文件自动关闭，无论是否发生异常
```

**为什么需要 with？**

```
┌─────────────────────────────────────────────────────────┐
│                    资源管理生命周期                        │
├─────────────────────────────────────────────────────────┤
│  1. 获取资源（打开文件、连接数据库、获取锁）                  │
│  2. 使用资源（读写文件、查询数据、加锁操作）                  │
│  3. 释放资源（关闭文件、断连、释放锁）← with 自动帮你做       │
└─────────────────────────────────────────────────────────┘
```

> 💡 **核心概念**：实现 `__enter__` 和 `__exit__` 方法的 对象就是"上下文管理器"。with 语句会在进入时调用 `__enter__`，在退出时调用 `__exit__`。

---

### 15.3.2 文件操作的 with 写法

```python
# 写入文件
with open("example.txt", "w", encoding="utf-8") as f:
    f.write("第一行\n")
    f.write("第二行\n")
# 文件自动关闭

# 读取文件
with open("example.txt", "r", encoding="utf-8") as f:
    content = f.read()
    print(content)
# 文件自动关闭

# 按行读取
with open("example.txt", "r", encoding="utf-8") as f:
    for line in f:
        print(line.strip())
```

**同时管理多个资源**：

```python
# 同时打开多个文件
with open("input.txt", "r", encoding="utf-8") as infile, \
     open("output.txt", "w", encoding="utf-8") as outfile:
    content = infile.read()
    outfile.write(content.upper())

# Python 3.10+ 更优雅的写法
with open("input.txt", "r") as infile, open("output.txt", "w") as outfile:
    outfile.write(infile.read().upper())
```

> 🎯 **好处**：即使读写时发生异常，with 也会确保文件被正确关闭。不用担心"文件被占用"、"资源泄露"的问题。

---

### 15.3.3 @contextmanager 装饰器

`@contextmanager` 让你用生成器的方式创建上下文管理器，不用写一个完整的类。

```python
from contextlib import contextmanager

@contextmanager
def managed_resource(name: str):
    """一个简单的上下文管理器"""
    print(f"🔓 获取资源：{name}")
    resource = f"[资源：{name}]"
    try:
        yield resource  # 暂停，把控制权交给 with 块
    finally:
        print(f"🔒 释放资源：{name}")

# 使用
with managed_resource("数据库连接") as res:
    print(f"使用 {res} 做操作...")
    print("操作完成")

# 输出：
# 🔓 获取资源：数据库连接
# 使用 [资源：数据库连接] 做操作...
# 操作完成
# 🔒 释放资源：数据库连接
```

**异常处理**：

```python
@contextmanager
def transaction(account: str):
    """模拟事务"""
    print(f"💰 开始事务：{account}")
    try:
        yield "事务ID-123"
        print("✅ 提交事务")
    except Exception as e:
        print(f"❌ 回滚事务：{e}")
        raise

# 正常情况
with transaction("账户A") as tx:
    print(f"执行 {tx}")

# 异常情况
print("\n--- 异常情况 ---")
try:
    with transaction("账户B") as tx:
        raise ValueError("余额不足")
except ValueError:
    print("异常被捕获了")
```

**计时上下文管理器**：

```python
import time
from contextlib import contextmanager

@contextmanager
def timer(label: str = "操作"):
    """计时器"""
    start = time.time()
    yield
    elapsed = time.time() - start
    print(f"⏱️ {label} 耗时：{elapsed:.4f}秒")

with timer("排序数组"):
    data = [3, 1, 4, 1, 5, 9, 2, 6]
    sorted_data = sorted(data)

with timer("查找元素"):
    target = 999999
    found = target in range(1000000)
```

> 🎪 **@contextmanager 原理**：它把生成器函数变成一个上下文管理器。`yield` 之前的代码相当于 `__enter__`，`yield` 之后的代码相当于 `__exit__`。`try...finally` 确保 yield 之后的代码总是执行。

---

### 15.3.4 contextlib 模块工具（closing / suppress / redirect_stdout）

#### closing - 为没有 close 方法的对象创建上下文管理器

```python
from contextlib import closing
import urllib.request

# urllib.request.urlopen 返回的对象有 close 方法
with closing(urllib.request.urlopen("https://www.example.com")) as response:
    html = response.read()
    print(f"获取了 {len(html)} 字节的页面")
```

#### suppress - 忽略指定异常

```python
from contextlib import suppress

# 忽略 FileNotFoundError
with suppress(FileNotFoundError):
    with open("不存在.txt", "r") as f:
        content = f.read()

# 等价于
try:
    with open("不存在.txt", "r") as f:
        content = f.read()
except FileNotFoundError:
    pass  # 什么都不做

print("程序继续运行，没有崩溃！")
```

#### redirect_stdout - 重定向标准输出

```python
import io
from contextlib import redirect_stdout, redirect_stderr

# 重定向 stdout 到 StringIO
buffer = io.StringIO()
with redirect_stdout(buffer):
    print("这条消息不会显示在终端")
    print("而是进入缓冲区")

output = buffer.getvalue()
print(f"捕获到：{output.strip()}")

# 重定向 stderr
error_buffer = io.StringIO()
with redirect_stderr(error_buffer):
    import sys
    print("这是错误输出", file=sys.stderr)

print(f"错误缓冲：{error_buffer.getvalue().strip()}")
```

#### 组合使用

```python
from contextlib import suppress, redirect_stdout

# 忽略异常 + 重定向输出
with suppress(FileNotFoundError), redirect_stdout(open("log.txt", "a")):
    with open("data.txt", "r") as f:
        print(f.read())
```

> 🎉 **contextlib 工具箱**：这些都是帮你少写代码的语法糖。`closing` 让任何对象都能用于 with，`suppress` 让你优雅地忽略异常，`redirect_stdout/stderr` 让你捕获或重定向输出。

---

## 15.4 异常处理

### 15.4.1 异常层次结构

Python 的异常有一个精心设计的继承体系：

```
BaseException
├── SystemExit              # sys.exit() 调用
├── KeyboardInterrupt       # Ctrl+C 中断
├── GeneratorExit          # 生成器关闭
└── Exception              # 所有常规异常的基类
    ├── StopIteration
    ├── ArithmeticError
    │   ├── FloatingPointError
    │   ├── OverflowError
    │   └── ZeroDivisionError
    ├── LookupError
    │   ├── IndexError
    │   └── KeyError
    ├── OSError (IOError)
    │   ├── FileNotFoundError
    │   ├── PermissionError
    │   └── TimeoutError
    ├── TypeError
    ├── ValueError
    ├── RuntimeError
    ├── NameError
    └── ... (还有好多)
```

```python
# 试试捕获不同层级的异常
def demonstrate_exceptions():
    # 触发各种异常
    try:
        x = 1 / 0  # ZeroDivisionError
    except Exception as e:
        print(f"捕获 Exception: {type(e).__name__}")

    try:
        d = {"a": 1}
        _ = d["nonexistent"]  # KeyError
    except LookupError as e:  # 捕获 LookupError 及其子类
        print(f"捕获 LookupError: {type(e).__name__}")

demonstrate_exceptions()
# 捕获 Exception: ZeroDivisionError
# 捕获 LookupError: KeyError
```

> 🎯 **理解异常层次很重要**：捕获基类（如 `Exception`）会捕获所有子类异常。精确捕获（如 `KeyError`）更好——你想处理特定错误，而不是"所有错误"。

---

### 15.4.2 try / except / else / finally 结构

完整的异常处理结构：

```python
try:
    # 尝试执行的代码
    x = int(input("输入一个整数："))
    result = 10 / x
except ValueError:
    # 捕获 ValueError（输入不是整数）
    print("❌ 输入无效，不是整数")
except ZeroDivisionError:
    # 捕获 ZeroDivisionError（除以零）
    print("❌ 不能除以零")
else:
    # 只有在没有异常时执行
    print(f"✅ 计算结果：{result}")
finally:
    # 无论是否有异常都执行
    print("🔄 清理工作")
```

**各部分执行时机**：

```
┌─────────────────────────────────────────────────────────┐
│                    执行流程图                             │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   try:                                                  │
│       A                                                  │
│       B  ──── 正常 ────> else:                          │
│       C                D                                │
│       │                │                                │
│       └──── 异常 ──────┘                                │
│             │                                          │
│      except:                                            │
│        E                                               │
│        │                                               │
│   finally:                                             │
│     F                                                  │
│                                                         │
│   A -> B -> C -> D -> F  (正常)                        │
│   A -> B -> except: E -> F (异常)                      │
└─────────────────────────────────────────────────────────┘
```

**实战示例**：

```python
def read_config(filename: str) -> dict:
    """读取配置文件"""
    config = {}
    line_num = 0  # 确保在 except 块中可用
    try:
        with open(filename, "r", encoding="utf-8") as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    key, value = line.split("=", 1)
                    config[key.strip()] = value.strip()
    except FileNotFoundError:
        print(f"⚠️ 配置文件 {filename} 不存在，使用默认配置")
        config = {"debug": "false", "port": "8080"}
    except PermissionError:
        print(f"❌ 没有权限读取 {filename}")
        raise
    except Exception as e:
        print(f"❌ 读取配置文件出错（第{line_num}行）：{e}")
        raise
    else:
        print(f"✅ 成功读取 {len(config)} 个配置项")
    finally:
        print("🔄 配置读取完成")

    return config

# 测试
result = read_config("config.txt")
print(f"配置：{result}")
```

---

### 15.4.3 except* 异常组（Python 3.11+）

Python 3.11 引入了**异常组**（Exception Groups），让你能优雅地处理多个同时发生的异常。

```python
# Python 3.11+ 使用 except* 处理异常组
def demo_exception_group():
    try:
        raise ExceptionGroup("多个问题", [
            ValueError("无效值"),
            TypeError("类型错误"),
            KeyError("找不到键"),
        ])
    except* ValueError as e:
        print(f"💧 ValueError: {e}")
    except* TypeError as e:
        print(f"🔧 TypeError: {e}")
    except* KeyError as e:
        print(f"🔑 KeyError: {e}")
    except* Exception as e:
        print(f"❓ 其他异常: {e}")

demo_exception_group()
# 💧 ValueError: 1 exception(s) in ExceptionGroup
# 🔧 TypeError: 1 exception(s) in ExceptionGroup
# 🔑 KeyError: 1 exception(s) in ExceptionGroup
```

**实际应用场景**（asyncio.TaskGroup，Python 3.11+）：

```python
import asyncio

async def task(n: int) -> int:
    if n == 2:
        raise ValueError("2是不允许的")
    if n == 5:
        raise TypeError("5的类型不对")
    return n * 2

async def parallel_tasks():
    """并发执行多个任务，异常会被收集到 ExceptionGroup"""
    try:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(task(1))
            tg.create_task(task(2))  # ValueError
            tg.create_task(task(3))
            tg.create_task(task(5))  # TypeError
    except* ValueError as eg:
        for e in eg.exceptions:
            print(f"处理 ValueError: {e}")
    except* TypeError as eg:
        for e in eg.exceptions:
            print(f"处理 TypeError: {e}")

# asyncio.run(parallel_tasks())
# 输出：
# 处理 ValueError: 2是不允许的
# 处理 TypeError: 5的类型不对
```

---

### 15.4.4 raise 语法（raise ValueError / raise ... from ...）

```python
# 基本 raise
def validate_age(age: int) -> None:
    if age < 0:
        raise ValueError("年龄不能是负数")
    if age > 150:
        raise ValueError("年龄太大了吧")
    print(f"有效年龄：{age}")

validate_age(25)  # 有效年龄：25
# validate_age(-5)  # ValueError: 年龄不能是负数

# raise 抛出现有异常
try:
    try:
        result = 1 / 0
    except ZeroDivisionError:
        raise ValueError("除法失败") from None  # from None 抑制原异常
except ValueError as e:
    print(f"ValueError: {e}")

# raise ... from ... 链式异常
try:
    try:
        int("not a number")
    except ValueError as ve:
        raise RuntimeError("转换失败") from ve  # 保留原异常
except RuntimeError as e:
    print(f"RuntimeError: {e}")
    if e.__cause__:
        print(f"  原因: {e.__cause__}")
```

**异常链的含义**：

```python
# __cause__ = 显式异常链（用 "from" 明确指定）
# __context__ = 隐式异常链（捕获时自动设置）

def level1():
    raise ValueError("原始错误")

def level2():
    try:
        level1()
    except ValueError as e:
        raise RuntimeError("中层包装") from e  # __cause__ 被设置

def level3():
    try:
        level2()
    except RuntimeError as e:
        print(f"异常: {e}")
        print(f"显式原因 __cause__: {e.__cause__}")
        print(f"隐式上下文 __context__: {e.__context__}")
        import traceback
        traceback.print_exc()

level3()
```

> 📝 **什么时候用异常链？** 当你想保留"根本原因"时。就像交通事故报告：直接原因是"刹车失灵"，根本原因是"轮胎老化"。

---

### 15.4.5 自定义异常类

```python
# 基本自定义异常
class ValidationError(Exception):
    """验证错误"""
    pass

def validate_username(username: str) -> None:
    if len(username) < 3:
        raise ValidationError("用户名至少3个字符")
    if len(username) > 20:
        raise ValidationError("用户名最多20个字符")
    print(f"✅ 用户名 {username} 有效")

try:
    validate_username("ab")
except ValidationError as e:
    print(f"❌ 验证失败：{e}")

# 带额外信息的自定义异常
class APIError(Exception):
    """API错误"""
    def __init__(self, message: str, status_code: int, endpoint: str):
        super().__init__(message)
        self.status_code = status_code
        self.endpoint = endpoint

    def __str__(self):
        return f"{self.message} (HTTP {self.status_code} @ {self.endpoint})"

def call_api(endpoint: str) -> None:
    if endpoint == "/invalid":
        raise APIError("端点不存在", 404, endpoint)
    if endpoint == "/error":
        raise APIError("服务器错误", 500, endpoint)
    print(f"✅ API调用成功: {endpoint}")

try:
    call_api("/invalid")
except APIError as e:
    print(f"API错误：{e}")
    print(f"  状态码：{e.status_code}")
    print(f"  端点：{e.endpoint}")
```

**异常层次设计**：

```python
class AppError(Exception):
    """应用异常基类"""
    pass

class ValidationError(AppError):
    """验证错误"""
    pass

class DatabaseError(AppError):
    """数据库错误"""
    pass

class NetworkError(AppError):
    """网络错误"""
    pass

def handle_error(error: AppError) -> str:
    """统一错误处理"""
    match error:
        case ValidationError():
            return "输入验证失败，请检查输入"
        case DatabaseError():
            return "数据库操作失败，请稍后重试"
        case NetworkError():
            return "网络连接失败，请检查网络"
        case _:
            return "未知错误"

print(handle_error(ValidationError("格式不对")))
print(handle_error(DatabaseError("连接超时")))
```

---

### 15.4.6 常见内置异常（NameError / TypeError / ValueError / KeyError 等）

| 异常 | 什么时候触发 | 例子 |
|------|-------------|------|
| `NameError` | 访问不存在的变量 | `print(x)` 其中 x 未定义 |
| `TypeError` | 类型不匹配 | `"str" + 123` |
| `ValueError` | 值不合法 | `int("abc")` |
| `KeyError` | 字典键不存在 | `d = {}; d["x"]` |
| `IndexError` | 索引越界 | `[1,2][10]` |
| `AttributeError` | 属性不存在 | `"str".foo` |
| `FileNotFoundError` | 文件不存在 | `open("no.txt")` |
| `ZeroDivisionError` | 除以零 | `1/0` |
| `ImportError` | 导入失败 | `import no_such_module` |

```python
def demo_errors():
    """演示各种错误"""
    errors = []

    # NameError
    try:
        print(undefined_var)
    except NameError:
        errors.append("NameError: 变量不存在")

    # TypeError
    try:
        result = "hello" + 123
    except TypeError:
        errors.append("TypeError: 类型不匹配")

    # ValueError
    try:
        num = int("not a number")
    except ValueError:
        errors.append("ValueError: 值格式错误")

    # KeyError
    try:
        d = {"a": 1}
        _ = d["b"]
    except KeyError:
        errors.append("KeyError: 键不存在")

    # IndexError
    try:
        lst = [1, 2, 3]
        _ = lst[99]
    except IndexError:
        errors.append("IndexError: 索引越界")

    # AttributeError
    try:
        "str".nonexistent_method()
    except AttributeError:
        errors.append("AttributeError: 属性不存在")

    for e in errors:
        print(f"  {e}")

demo_errors()
```

---

### 15.4.7 异常处理的最佳实践

```
┌─────────────────────────────────────────────────────────┐
│                   异常处理避坑指南 🧭                      │
├─────────────────────────────────────────────────────────┤
│  ✅ DO                                                │
│  ─────────────────────────────────────────────────────  │
│  • 捕获具体异常，不要 bare except:                       │
│    ❌ except:                                          │
│    ✅ except ValueError:                               │
│  • 异常处理要精确，能修复就修复，不能修复就向上抛           │
│  • 使用 finally 做清理工作（关闭文件、释放锁）            │
│  • 异常要有信息量，让人知道发生了什么                       │
│  • 记录异常用 logging，不要用 print                       │
├─────────────────────────────────────────────────────────┤
│  ❌ DON'T                                             │
│  ─────────────────────────────────────────────────────  │
│  • 不要用异常做流程控制（别用 except 代替 if）           │
│  • 不要捕获所有异常后默默忽略                             │
│  • 不要在循环里捕获异常而不 break                         │
│  • 不要抛出太宽泛的异常（Exception 太笼统）              │
└─────────────────────────────────────────────────────────┘
```

```python
# ❌ 错误示例：bare except 吞掉所有异常
try:
    risky_operation()
except:
    pass  # 天哪，发生什么都不知道！

# ✅ 正确示例：精确捕获 + 记录
import logging

try:
    risky_operation()
except ValueError as e:
    logging.error(f"值错误: {e}")
    raise  # 或者做其他处理
except Exception as e:
    logging.exception(f"Unexpected error: {e}")  # 包含 traceback
    raise
```

**EAFP vs LBYL**：

```python
# EAFP (Easier to Ask Forgiveness than Permission)
# "先斩后奏" - 假设没问题，出问题再处理
try:
    data = data["key"]["subkey"]
except (KeyError, TypeError):
    data = None

# LBYL (Look Before You Leap)
# "三思后行" - 先检查再行动
if "key" in data and isinstance(data["key"], dict):
    data = data["key"].get("subkey")
else:
    data = None
```

> 💡 **Pythonic 选择**：Python 社区更推荐 EAFP 风格。写起来更简洁，逻辑更清晰。

---

### 15.4.8 异常链与 __cause__ / __context__

```python
def demonstrate_exception_chaining():
    """演示异常链"""

    # 情况1：显式异常链 from
    print("=== 显式异常链 ===")
    try:
        try:
            raise ValueError("原始错误")
        except ValueError as e:
            raise RuntimeError("包装错误") from e
    except RuntimeError as e:
        print(f"异常: {e}")
        print(f"  __cause__: {e.__cause__}")  # 原始错误
        print(f"  __context__: {e.__context__}")  # 原始错误的上下文

    # 情况2：隐式异常链
    print("\n=== 隐式异常链 ===")
    try:
        try:
            raise ValueError("原始错误")
        except ValueError:
            # 不显式处理，直接抛新异常
            raise RuntimeError("包装错误")
    except RuntimeError as e:
        print(f"异常: {e}")
        print(f"  __cause__: {e.__cause__}")  # None（不是 from）
        print(f"  __context__: {e.__context__}")  # 自动设置！

    # 情况3：抑制异常链 from None
    print("\n=== 抑制异常链 ===")
    try:
        try:
            raise ValueError("原始错误")
        except ValueError as e:
            raise RuntimeError("包装错误") from None
    except RuntimeError as e:
        print(f"异常: {e}")
        print(f"  __cause__: {e.__cause__}")  # None
        print(f"  __context__: {e.__context__}")  # None!

demonstrate_exception_chaining()
```

> 📊 **总结**：`__cause__` = 显式设置（from），`__context__` = 隐式设置（捕获时自动），`from None` = 两者都抑制。

---

## 15.5 生成器与协程

### 15.5.1 生成器函数（yield 关键字）

**生成器**是 Python 中"惰性计算"（Lazy Evaluation）的实现。它不像列表一样一次性生成所有元素，而是"按需生产"——你问一个，它给你一个。

```python
def count_up_to(n: int):
    """数数生成器"""
    i = 1
    while i <= n:
        yield i  # yield = "产出"，暂停等待下次调用
        i += 1

# 创建生成器对象（不执行函数体）
generator = count_up_to(5)
print(generator)  # <generator object count_up_to at 0x...>

# 迭代获取值
print(next(generator))  # 1
print(next(generator))  # 2
print(next(generator))  # 3
print(next(generator))  # 4
print(next(generator))  # 5
# print(next(generator))  # StopIteration 异常！

# 或者用 for 循环（自动处理 StopIteration）
for num in count_up_to(3):
    print(num)
```

**yield 的工作原理**：

```
┌─────────────────────────────────────────────────────────┐
│                 生成器执行流程                             │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  调用 gen = count_up_to(3)                              │
│       ↓                                                 │
│  函数暂停在 yield，不执行，返回生成器对象                  │
│                                                         │
│  next(gen)                                              │
│       ↓                                                 │
│  函数从 yield 处继续执行到下一个 yield                    │
│       ↓                                                 │
│  暂停，返回 yield 的值                                   │
│       ↓                                                 │
│  ... 重复 ...                                           │
│       ↓                                                 │
│  函数结束，抛出 StopIteration                            │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**经典例子：斐波那契数列**：

```python
def fibonacci():
    """无限斐波那契数列生成器"""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

# 获取前10个斐波那契数
fib = fibonacci()
for i in range(10):
    print(next(fib), end=" ")
# 0 1 1 2 3 5 8 13 21 34

# 或者用 islice 限制数量
from itertools import islice
print("\n前20个：", list(islice(fibonacci(), 20)))
```

---

### 15.5.2 生成器表达式（惰性求值）

**生成器表达式**类似列表推导式，但用圆括号，返回生成器而不是列表。

```python
# 列表推导式 - 立即生成所有元素
 squares_list = [x**2 for x in range(10)]
 print(squares_list)  # [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

# 生成器表达式 - 惰性求值
squares_gen = (x**2 for x in range(10))
print(squares_gen)  # <generator object ...>
print(next(squares_gen))  # 0
print(next(squares_gen))  # 1

# 惰性的好处：内存效率
def expensive_computation(n):
    print(f"计算 {n}")
    return n * 2

# ❌ 列表推导式：立即计算所有值
result_list = [expensive_computation(i) for i in range(5)]
# 计算 0
# 计算 1
# 计算 2
# 计算 3
# 计算 4

# ✅ 生成器表达式：按需计算
result_gen = (expensive_computation(i) for i in range(5))
print("生成器已创建，还没计算")
next(result_gen)  # 现在才计算
# 计算 0
next(result_gen)  # 继续计算
# 计算 1
```

**生成器表达式的使用场景**：

```python
# 读取大文件 - 一行一行处理，不会把整个文件加载到内存
def process_large_file(filename):
    with open(filename, "r", encoding="utf-8") as f:
        lines = (line.strip() for line in f if line.strip())
        for line in lines:
            yield line

# 求和时不创建完整列表
total = sum(x**2 for x in range(1000000))
print(f"总和: {total}")

# 找出第一个匹配的（找到就停）
matches = (x for x in range(1000000) if x % 1000 == 0 and x > 5000)
first_match = next(matches)
print(f"第一个符合条件的: {first_match}")
```

> 💰 **内存对比**：生成 0-9999 的立方，列表需要约 80KB 内存，生成器只需要几百字节！对大数据集，这是生死之别。

---

### 15.5.3 yield from（委托生成器）

**yield from** 用于"委托"给另一个生成器，让代码更简洁。

```python
# 不使用 yield from
def chain(*iterables):
    """链接多个可迭代对象"""
    result = []
    for it in iterables:
        for item in it:
            result.append(item)
    return result

# 使用 yield from
def chain_with_yield_from(*iterables):
    """用 yield from 链接"""
    for it in iterables:
        yield from it  # 委托给 it

print(list(chain([1, 2], [3, 4], [5, 6])))
print(list(chain_with_yield_from([1, 2], [3, 4], [5, 6])))

# 经典应用：生成器树的遍历
def flatten(nested):
    """扁平化嵌套列表"""
    for item in nested:
        if isinstance(item, list):
            yield from flatten(item)  # 递归委托
        else:
            yield item

nested = [1, [2, 3], [[4, 5], 6], 7]
print(list(flatten(nested)))  # [1, 2, 3, 4, 5, 6, 7]
```

**yield from 的更多用法**：

```python
# 双向通信：生成器和调用者之间传递值
def counter(initial=0):
    """计数器，可以接收重置值"""
    count = initial
    while True:
        increment = yield count  # 产出并等待接收值
        if increment is None:
            count += 1
        else:
            count += increment

c = counter(10)
print(next(c))    # 10（产出）
print(next(c))    # 11（默认+1）
print(c.send(5))  # 16（+5）
print(c.send(10)) # 26（+10）
c.close()         # 关闭生成器
```

---

### 15.5.4 协程与 async/await

**协程**（Coroutine）是"可以暂停和恢复的函数"。与生成器类似，但用于异步编程。

```python
# Python 3.5+ 协程语法
async def fetch_data(url: str) -> str:
    """异步获取数据（模拟）"""
    print(f"开始获取 {url}")
    await asyncio.sleep(1)  # 模拟网络延迟
    return f"数据 from {url}"

async def main():
    """主协程"""
    result = await fetch_data("https://example.com")
    print(result)

# 运行
import asyncio
asyncio.run(main())
# 开始获取 https://example.com
# (等待1秒)
# 数据 from https://example.com
```

**为什么需要 async/await？**

```
┌─────────────────────────────────────────────────────────┐
│                同步 vs 异步对比                           │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  同步：                                                   │
│    请求1 ──────────────────> (等待)                      │
│    请求2 ──────────────────> (等待)                      │
│    请求3 ──────────────────> (等待)                      │
│    总时间 = 3 × 请求时间                                  │
│                                                         │
│  异步：                                                   │
│    请求1 ─> 等待 ─────────────> 完成                     │
│    请求2 ─────────> 等待 ──────> 完成                    │
│    请求3 ─────────────> 等待 ──> 完成                   │
│    总时间 ≈ max(各请求时间)                               │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**并发执行多个协程**：

```python
import asyncio

async def fetch(url: str, delay: float) -> str:
    """模拟异步请求"""
    print(f"开始: {url}")
    await asyncio.sleep(delay)
    print(f"完成: {url}")
    return f"{url} 数据"

async def main():
    # 顺序执行
    # r1 = await fetch("url1", 1)
    # r2 = await fetch("url2", 1)
    # print(r1, r2)  # 总耗时约2秒

    # 并发执行
    results = await asyncio.gather(
        fetch("url1", 1),
        fetch("url2", 0.5),
        fetch("url3", 1.5),
    )
    print(f"全部完成: {results}")

asyncio.run(main())
# 开始: url1
# 开始: url2
# 开始: url3
# 完成: url2      # 0.5秒
# 完成: url1      # 1秒
# 完成: url3      # 1.5秒
# 全部完成: ['url1 数据', 'url2 数据', 'url3 数据']
```

---

### 15.5.5 asyncio 事件循环

**事件循环**是异步编程的核心，它负责调度和执行协程。

```python
import asyncio

# asyncio.run() - 高级 API（Python 3.7+）
async def simple_task():
    print("任务执行中...")
    await asyncio.sleep(0.5)
    print("任务完成")

# asyncio.run(simple_task())

# 手动管理事件循环（了解即可）
def manual_event_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(simple_task())
    finally:
        loop.close()

# 常用 asyncio 工具
async def demo_tools():
    # asyncio.create_task() - 创建任务（后台执行）
    task1 = asyncio.create_task(fetch("任务1", 1))
    task2 = asyncio.create_task(fetch("任务2", 0.5))

    # await 两个任务
    r1, r2 = await asyncio.gather(task1, task2)
    print(f"结果: {r1}, {r2}")

    # asyncio.wait_for() - 超时控制
    try:
        await asyncio.wait_for(asyncio.sleep(3), timeout=1)
    except asyncio.TimeoutError:
        print("操作超时！")

    # asyncio.shield() - 保护任务不被取消
    async def cancellable():
        await asyncio.sleep(10)

    task = asyncio.create_task(cancellable())
    await asyncio.sleep(0.1)
    task.cancel()
    try:
        await asyncio.shield(task)
    except asyncio.CancelledError:
        print("任务被取消了（但被 shield 保护）")

asyncio.run(demo_tools())
```

**实战：异步 HTTP 请求**：

```python
import asyncio
import aiohttp  # 需要安装: pip install aiohttp

async def fetch_all(urls: list[str]) -> list[str]:
    """并发获取多个 URL"""
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url) for url in urls]
        return await asyncio.gather(*tasks)

async def fetch_url(session, url: str) -> str:
    async with session.get(url) as response:
        return f"{url}: {response.status}"

# asyncio.run(fetch_all(["https://python.org", "https://example.com"]))
```

> 🚀 **总结**：async/await 是 Python 异步编程的核心语法。`async def` 定义协程，`await` 等待协程完成，`asyncio.gather()` 并发执行多个协程，`asyncio.create_task()` 创建后台任务。

---

## 15.6 赋值表达式（:= 海象运算符）

### 15.6.1 海象运算符含义

**海象运算符**（Walrus Operator）`:=` 因为长相像海象的两个牙而得名。它允许你在表达式内部赋值变量，让代码更简洁。

```python
# ❌ 传统写法：先赋值再使用
n = 10
if n > 5:
    print(f"n={n} 超过5了")

# ✅ 海象运算符：在表达式内部赋值
if (n := 10) > 5:
    print(f"n={n} 超过5了")

# 对比
# 传统: result = some_computation(); if result: ...
# 海象: if (result := some_computation()): ...
```

---

### 15.6.2 适用场景

#### 场景1：while 循环读取数据

```python
# ❌ 传统写法：重复调用
while True:
    line = read_line()
    if not line:
        break
    process(line)

# ✅ 海象写法：一次调用
while (line := read_line()):
    process(line)

# 实际例子：读取文件直到找到特定行
def find_target_line(filename: str, target: str) -> str | None:
    with open(filename, "r", encoding="utf-8") as f:
        while (line := f.readline()):
            if target in line:
                return line.strip()
    return None
```

#### 场景2：列表推导式中的重复计算

```python
import re

# ❌ 传统写法：重复计算
text = "hello world hello"
matches = re.findall(r'\w+', text)
# 判断最长单词
longest = max(len(w) for w in matches)
print(f"最长单词长度: {longest}")

# ✅ 海象写法：在推导式中同时捕获
if (longest := max(len(w) for w in re.findall(r'\w+', text))) > 5:
    print(f"发现长单词！长度={longest}")
```

#### 场景3：条件表达式中使用

```python
data = [1, 2, 3, 4, 5]

# ❌ 传统写法：先判断再使用
result = compute_expensive(data)
if len(result) > 0:
    print(f"结果: {result}")
else:
    print("没有结果")

# ✅ 海象写法：一步到位
if (result := compute_expensive(data)) and len(result) > 0:
    print(f"结果: {result}")

# 或者更优雅
if (result := compute_expensive(data)):
    print(f"结果: {result}")
```

#### 场景4：match...case 中使用

```python
def process_command(cmd: str) -> str:
    match cmd.split():
        case ["get", name] if (value := cache.get(name)) is not None:
            return f"缓存命中: {value}"
        case ["get", name]:
            return f"缓存未命中: {name}"
        case ["set", name, value]:
            cache[name] = value
            return f"已设置: {name}={value}"

cache = {}
print(process_command("get foo"))
print(process_command("set foo 123"))
print(process_command("get foo"))
```

---

### 15.6.3 滥用危害与最佳实践

```
┌─────────────────────────────────────────────────────────┐
│               海象运算符使用指南 ⚠️                        │
├─────────────────────────────────────────────────────────┤
│  ✅ 适合使用                                             │
│  ─────────────────────────────────────────────────────  │
│  • while 循环中的条件判断                                │
│  • 避免重复计算或重复方法调用                            │
│  • 列表推导式中需要中间变量                              │
│  • match...case 中的 guard 条件                         │
├─────────────────────────────────────────────────────────┤
│  ❌ 不适合使用                                           │
│  ─────────────────────────────────────────────────────  │
│  • 简单赋值：x := 5（可读性差）                          │
│  • 嵌套过深：((a := 1) + (b := 2))（令人费解）           │
│  • 副作用不明显：func(x := 5)（不知道 x 被修改）         │
│  • 变量名过长：(total_price := calculate()) 尽量简短    │
└─────────────────────────────────────────────────────────┘
```

**滥用示例**：

```python
# ❌ 滥用：可读性差
if (x := 5) and (y := 10) and (z := x + y):
    print(f"结果: {z}")

# ❌ 滥用：副作用不明确
result = [x := i*2 for i in range(10)]  # x 最后是 18

# ❌ 滥用：嵌套过深
if (a := 1) and (b := 2) and (c := 3):
    pass

# ✅ 适度使用：更简洁，但不牺牲可读性
data = [1, 2, 3, 4, 5]
if (avg := sum(data) / len(data)) > 3:
    print(f"平均值 {avg} 超过 3")

# ✅ 适合的场景：while 循环读取
def read_lines():
    yield from ["line1", "line2", ""]

while (line := next(read_lines(), "")):
    if not line:
        break
    print(line)
```

> 🎯 **原则**：海象运算符是工具，不是玩具。它让某些代码更简洁，但滥用会让代码变成"只写代码"（write-only code）。可读性永远是第一位的！

---

## 本章小结

本章我们深入探讨了 Python 的高级语法特性，这些是成为 Python 高手必经之路。让我们来回顾一下：

### 1. 类型提示（Type Hints）
- 类型提示是给 IDE 和静态检查工具看的"注释"，运行时完全不影响性能
- 从 Python 3.9+ 开始，可以用内置类型泛型如 `list[int]` 代替 `List[int]`
- `TypeVar` 让泛型函数更灵活，`Protocol` 实现结构化子类型
- `Self`（Python 3.11+）让方法返回类型更精确

### 2. match...case 结构化模式匹配
- Python 3.10+ 引入，取代繁琐的 if...elif 链
- 支持字面量匹配、序列解构、映射解构、类模式、guard 条件
- 是现代 Python 的标志性语法

### 3. with 语句与上下文管理器
- `with` 确保资源正确获取和释放，无论是否发生异常
- 实现 `__enter__` 和 `__exit__` 即可创建自定义上下文管理器
- `@contextmanager` 装饰器让创建上下文管理器更简单
- `contextlib` 提供 `closing`、`suppress`、`redirect_stdout` 等实用工具

### 4. 异常处理
- Python 异常有严格的继承体系，捕获时应尽量精确
- `try/except/else/finally` 完整结构应对各种场景
- `raise ... from ...` 建立异常链，保留根本原因
- Pythonic 的错误处理哲学：EAFP（先斩后奏）vs LBYL（先检查）

### 5. 生成器与协程
- 生成器用 `yield` 实现惰性求值，内存效率极高
- `yield from` 委托给子生成器，实现代码复用
- `async/await` 是 Python 异步编程的核心
- `asyncio` 事件循环管理协程调度，`gather` 实现并发执行

### 6. 海象运算符（:=）
- 在表达式内部赋值，让某些代码更简洁
- 适合 while 循环、避免重复计算等场景
- 滥用会降低可读性，要适度使用

---

> 🎓 **学完这一章，你已经掌握了 Python 的大部分"高阶技能"！**
>
> 这些知识点不是孤立的，它们经常一起出现——比如在异步代码中，你会同时用到 `async/await`（协程）、`with`（上下文管理器）、类型提示、以及异常处理。
>
> 建议：动手实践！光是看概念不够，写代码才能真正理解这些特性的威力。下次遇到问题，想想这些工具能不能帮上忙。

---

*祝你 Python 之旅愉快！ 🚀*
