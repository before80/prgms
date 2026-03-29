+++
title = "第24章 C++14特性"
weight = 240
date = "2026-03-29T21:03:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++
# 第24章 C++14特性

如果说C++11是C++的文艺复兴，那C++14就是这场运动的"配套设施完善年"。功能还是那些功能，但用起来更顺手了，就像是你家楼下终于开了家便利店——你不需要再跑五公里买泡面了。本章我们就来聊聊C++14那些让人会心一笑的小改进。

## 24.1 泛型Lambda

### 什么是Lambda？

在聊泛型Lambda之前，先给Lambda（匿名函数）下个定义。顾名思义，Lambda就是没有名字的函数——就像你点了份外卖，不需要知道厨师叫什么，只需要知道味道好不好吃就行了。

Lambda的基本语法是这样的：

```cpp
[capture](parameters) -> return_type { body }
```

其中`capture`是捕获列表（决定你能访问哪些外部变量），`parameters`是参数，`return_type`是返回类型，`body`是函数体。

### C++11 vs C++14：参数类型的进化

在C++11中，Lambda的参数必须是明确指定的类型，比如：

```cpp
// C++11风格的Lambda，参数类型必须写死
auto add = [](int a, int b) {
    return a + b;
};
```

这样就只能做整数加法了，想做浮点数加法？对不起，再写一个。

但到了C++14，参数类型可以用`auto`声明，编译器会自动帮你推导类型。就像一个万能钥匙，能开多种锁：

```cpp
#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    // C++14: Lambda参数可以使用auto
    // 编译器会根据传入的参数自动推断a和b的类型
    auto add = [](auto a, auto b) {
        return a + b;
    };
    
    // 整数加法
    std::cout << "add(1, 2) = " << add(1, 2) << std::endl;  // 输出: 3
    
    // 浮点数加法
    std::cout << "add(1.5, 2.5) = " << add(1.5, 2.5) << std::endl;  // 输出: 4
    
    // 字符串拼接（重载了+运算符）
    std::cout << "add(std::string(\"a\"), std::string(\"b\")) = " 
              << add(std::string("a"), std::string("b")) << std::endl;  // 输出: ab
    
    // 甚至可以用在STL算法中！
    std::vector<int> nums = {1, 2, 3, 4, 5};
    std::for_each(nums.begin(), nums.end(), [](auto& n) {
        n *= 2;  // 每个元素翻倍
    });
    
    return 0;
}
```

### 工作原理

`auto`在Lambda参数中的原理其实很朴素：编译器会为每种不同的类型生成一份专门的函数实例。这叫做**模板实例化**——想象一下，编译器是个超级复制粘贴机器人，你写一个`auto`参数，它会根据实际调用生成N个版本。

> 💡 **为什么不用模板函数？**
> 
> 直接写模板函数当然也行，但Lambda更简洁，而且可以就地定义、就地使用，不用先跑到别处声明一个模板函数再回来调用。

### 实际应用场景

泛型Lambda在STL算法中使用频率极高，比如排序自定义、查找过滤、批量转换等等：

```cpp
#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::vector<double> prices = {99.9, 199.9, 299.9, 399.9, 499.9};
    
    // 泛型Lambda配合for_each打折
    double discount = 0.8;  // 八折
    std::for_each(prices.begin(), prices.end(), [discount](auto& price) {
        price *= discount;
    });
    
    // 打印打折后的价格
    for (const auto& price : prices) {
        std::cout << price << " ";  // 输出: 79.92 159.92 239.92 319.92 399.92 
    }
    std::cout << std::endl;
    
    return 0;
}
```

### 幽默一刻

想象你走进一家餐厅：
- **C++11的服务员**："您好，请问您要点什么？"
- 你："来份加法。"
- 服务员："好的，请问是整数加法还是浮点数加法？"
- 你："...我只是想算1+1。"

- **C++14的服务员**："您好，请问您要点什么？"
- 你："来份加法，随便什么类型都行。"
- 服务员："好的，1+1=2，您的外卖已准备好！"

泛型Lambda就是那个能读懂你心思的服务员。

---

## 24.2 变量模板

### 模板的进化：从函数到变量

C++的模板最初是为了实现泛型编程，但很长一段时间里，模板只能用在函数和类上。到了C++14，模板家族迎来了新成员——**变量模板**（Variable Template）。

简单来说，变量模板就是用模板定义的变量。就像类模板生成类、函数模板生成函数一样，变量模板生成一系列相关的变量。

### 语法很简单

```cpp
template<typename T>
constexpr 类型 变量名 = 表达式;
```

### std::is_integral_v 的前世今生

在C++11/14中，有一个经典的需求：判断一个类型是否是整数类型。通常你会这么写：

```cpp
// C++11风格
std::is_integral<int>::value  // 返回true
std::is_integral<double>::value  // 返回false
```

这玩意儿又臭又长，每次写都要敲半天。到了C++14，人们决定给它起个绰号（别名模板），于是：

```cpp
// C++14风格
std::is_integral_v<int>  // 更简洁，效果一样
```

这个`_v`后缀就是变量模板的约定。下面我们来看完整例子：

```cpp
#include <iostream>
#include <type_traits>

// C++14: 变量模板
// 语法：template<typename T> constexpr 类型 变量名 = 初始值;

// 判断T是否是整数类型，结果是一个编译期常量bool
template<typename T>
constexpr bool is_integral_v = std::is_integral<T>::value;

// 获取T类型的大小（字节数），结果是一个编译期常量size_t
template<typename T>
constexpr size_t type_size_v = sizeof(T);

int main() {
    std::cout << std::boolalpha;  // 输出true/false而不是1/0
    
    // 判断各种类型是否是整数
    std::cout << "is_integral_v<int> = " << is_integral_v<int> << std::endl;  // 输出: true
    std::cout << "is_integral_v<double> = " << is_integral_v<double> << std::endl;  // 输出: false
    std::cout << "is_integral_v<char> = " << is_integral_v<char> << std::endl;  // 输出: true (char也是整数类型)
    std::cout << "is_integral_v<bool> = " << is_integral_v<bool> << std::endl;  // 输出: true
    
    std::cout << std::endl;
    
    // 获取各种类型的大小
    std::cout << "type_size_v<int> = " << type_size_v<int> << std::endl;  // 输出: 4
    std::cout << "type_size_v<double> = " << type_size_v<double> << std::endl;  // 输出: 8
    std::cout << "type_size_v<char> = " << type_size_v<char> << std::endl;  // 输出: 1
    std::cout << "type_size_v<long long> = " << type_size_v<long long> << std::endl;  // 输出: 8
    
    return 0;
}
```

### 背后的原理

变量模板的本质是：每当你用不同的类型参数去访问这个变量时，编译器会生成一个对应类型的专门版本：

```cpp
// 你写了:
template<typename T>
constexpr bool is_integral_v = std::is_integral<T>::value;

// 编译器生成类似这样的东西（伪代码）:
constexpr bool is_integral_v_int = std::is_integral<int>::value;      // true
constexpr bool is_integral_v_double = std::is_integral<double>::value;  // false
constexpr bool is_integral_v_char = std::is_integral<char>::value;     // true
```

### 常见标准库变量模板

C++14之后，标准库提供了大量的`_v`变量模板（到了C++17还有`_nv`等变体）：

| 变量模板 | 判断的类型 |
|---------|-----------|
| `is_integral_v<T>` | T是否是整数类型 |
| `is_floating_point_v<T>` | T是否是浮点类型 |
| `is_array_v<T>` | T是否是数组类型 |
| `is_pointer_v<T>` | T是否是指针类型 |
| `is_enum_v<T>` | T是否是枚举类型 |

### 幽默一刻

变量模板的命名约定其实是个悲伤的故事：

1. C++11：写`::value`
2. C++14：写`_v`
3. C++17：写`::value_v`（不，等等，标准没采纳）
4. 最终共识：`_v`就是标准答案

所以你记住：看到`_v`，就知道这是个C++14的变量模板；看到`::value`，就知道这是C++11的元编程遗产。

---

## 24.3 放宽的constexpr限制

### constexpr：从"编译期计算"到"更自由的编译期计算"

**constexpr**是C++11引入的关键字，意思是"常量表达式"，告诉编译器"这个值可以在编译期算出来"。C++11对constexpr的限制非常严格——它只允许很简单的单行表达式，不许有局部变量，不许有循环，不许有多条语句。

这就好比你去相亲，对象说："我可以和你一起吃饭，但只允许用筷子夹一粒米，不许嚼，不许咽，不许说话。"

到了C++14，这些限制被大幅放宽了。

### C++11 vs C++14：constexpr的限制对比

| 特性 | C++11 constexpr | C++14 constexpr |
|-----|----------------|-----------------|
| 局部变量 | ❌ 不允许 | ✅ 允许 |
| 局部静态变量 | ❌ 不允许 | ❌ 不允许 |
| 循环语句 | ❌ 不允许 | ✅ 允许 |
| if语句 | ❌ 不允许（只能用三元运算符） | ✅ 允许 |
| 多个return | ❌ 不允许 | ✅ 允许 |
| try/catch | ❌ 不允许 | ❌ 不允许 |

### 阶乘和斐波那契：经典constexpr案例

```cpp
#include <iostream>

// C++14: constexpr函数限制放宽
// 可以在constexpr函数中使用：
// - 局部变量
// - 循环语句
// - 改变量语句（虽然这个例子没用到）
// - if-else分支

// 计算阶乘：5! = 5*4*3*2*1 = 120
constexpr int factorial(int n) {
    int result = 1;  // 局部变量，C++11不允许！
    for (int i = 2; i <= n; ++i) {  // 循环，C++11不允许！
        result *= i;
    }
    return result;
}

// 计算斐波那契数列第n项
constexpr int fibonacci(int n) {
    // C++14允许使用if分支了！
    if (n <= 1) return n;
    
    int a = 0, b = 1;  // 局部变量
    for (int i = 2; i <= n; ++i) {  // 循环
        int c = a + b;
        a = b;
        b = c;
    }
    return b;
}

int main() {
    // constexpr变量：编译期就计算出结果
    constexpr int fact5 = factorial(5);  // 编译期计算，结果是120
    constexpr int fib10 = fibonacci(10);  // 编译期计算，结果是55
    
    // 普通变量：运行时计算
    int runtime_fact = factorial(6);  // 运行时计算
    
    std::cout << "factorial(5) = " << fact5 << std::endl;  // 输出: 120
    std::cout << "fibonacci(10) = " << fib10 << std::endl;  // 输出: 55
    std::cout << "factorial(6) (runtime) = " << runtime_fact << std::endl;  // 输出: 720
    
    return 0;
}
```

### 编译期计算的优势

为什么要在编译期计算？因为这样可以：

1. **提升性能**：结果直接嵌入二进制，不需要每次运行都算一遍
2. **用于数组大小**：编译期常量可以作为数组维度
3. **用于模板参数**：模板参数必须是编译期常量

```cpp
#include <iostream>

constexpr int factorial(int n) {
    int result = 1;
    for (int i = 2; i <= n; ++i) {
        result *= i;
    }
    return result;
}

int main() {
    // 编译期常量：可以作为数组维度
    constexpr int SIZE = factorial(5);  // SIZE = 120
    int arr[SIZE] = {0};  // 合法！数组大小必须是编译期常量
    
    std::cout << "数组大小是编译期计算的: " << SIZE << std::endl;  // 输出: 120
    std::cout << "数组arr的元素个数: " << (sizeof(arr) / sizeof(arr[0])) << std::endl;  // 输出: 120
    
    return 0;
}
```

### 幽默一刻

C++11的constexpr就像是一个完美的石膏像——漂亮但一动不动。你想让它循环？不行。想让它分支判断？不行。想让它存个中间结果？更不行。

C++14的constexpr终于允许你"动"了，但仍然有些事情做不到——比如try/catch（编译期异常处理太复杂）、比如动态内存分配。所以constexpr函数里不能`new`一个对象出来——这大概就是"戴着镣铐跳舞"吧。

---

## 24.4 二进制字面量

### 什么是字面量（Literal）？

**字面量**就是代码里直接写出来的值，比如`42`、`3.14`、`"hello"`。它们就像是语言的基本词汇——你不需要定义，直接使用。

在C++14之前，我们有十进制字面量（`42`）、十六进制字面量（`0x2A`）、八进制字面量（`052`），但就是没有**二进制字面量**。

### 二进制字面量：程序员的"0和1"情怀

程序员喜欢说"一切都是0和1"，但C++11之前你却没法直接在代码里写二进制数。你得手动算：`0b1010`在C++11之前是不存在的，你得写`10`（十进制）或者`0xA`（十六进制）。

这就好比一个中世纪铁匠说"我天天和火打交道"，但却不让他直接点火，必须用火柴慢慢磨。

C++14终于带来了`0b`前缀，让你直接写二进制：

```cpp
#include <iostream>

int main() {
    // C++14: 二进制字面量
    // 语法：0b + 二进制数字串（或0B也行，大小火鸡均可）
    
    int bin1 = 0b1010;       // 二进制1010 = 十进制10
    int bin2 = 0b11111111;   // 二进制11111111 = 十进制255
    
    std::cout << "0b1010 = " << bin1 << std::endl;  // 输出: 10
    std::cout << "0b11111111 = " << bin2 << std::endl;  // 输出: 255
    
    // 也可以用大写B
    int bin3 = 0B1010;  // 效果一样
    
    // 和位运算组合使用——这是二进制字面量的主战场！
    int flags = 0b1100 | 0b0011;  // 按位或 = 0b1111 = 15
    std::cout << "0b1100 | 0b0011 = " << flags << std::endl;  // 输出: 15
    
    // 权限控制示例
    const int READ = 0b0001;    // 读权限
    const int WRITE = 0b0010;   // 写权限
    const int EXECUTE = 0b0100; // 执行权限
    const int ADMIN = 0b1000;   // 管理员权限
    
    int user_permissions = READ | WRITE;  // 普通用户：读+写
    int admin_permissions = READ | WRITE | EXECUTE | ADMIN;  // 管理员：全部
    
    // 检查权限
    bool can_read = (user_permissions & READ) != 0;  // true
    bool can_execute = (user_permissions & EXECUTE) != 0;  // false
    
    std::cout << "普通用户能否读: " << std::boolalpha << can_read << std::endl;  // 输出: true
    std::cout << "普通用户能否执行: " << can_execute << std::endl;  // 输出: false
    
    return 0;
}
```

### 典型应用场景

二进制字面量在底层编程、位掩码、权限控制、硬件寄存器操作等场景非常有用：

```cpp
#include <iostream>

// 网络协议中的标志位
struct TCPFlags {
    static constexpr int FIN = 0b00000001;
    static constexpr int SYN = 0b00000010;
    static constexpr int RST = 0b00000100;
    static constexpr int PSH = 0b00001000;
    static constexpr int ACK = 0b00010000;
    static constexpr int URG = 0b00100000;
};

int main() {
    // 构建一个SYN-ACK包
    int packet = TCPFlags::SYN | TCPFlags::ACK;
    
    std::cout << "TCP包标志位: " << std::endl;
    std::cout << "  SYN: " << ((packet & TCPFlags::SYN) != 0) << std::endl;  // 输出: 1 (true)
    std::cout << "  ACK: " << ((packet & TCPFlags::ACK) != 0) << std::endl;  // 输出: 1 (true)
    std::cout << "  FIN: " << ((packet & TCPFlags::FIN) != 0) << std::endl;  // 输出: 0 (false)
    
    return 0;
}
```

### 幽默一刻

二进制字面量的命名之争也很有意思。2008年有人提议用`0b`前缀，遭到了C语言委员会的反对，他们坚持要用`B`开头的写法——比如`B1010`。理由是"不能和十六进制的`0x`太像"。

最后C++14还是选择了`0b`（和`0x`保持队形）。现在看来这是个正确的决定——统一的美才是真的美。

---

## 24.5 数字分隔符

### 顾名思义的特性

**数字分隔符**（Digit Separator）允许在数字字面量中插入单引号，让长数字更容易阅读。`1'000'000`就是100万，比`1000000`好看多了。

这个特性的灵感来自Pascal语言（用点作为分隔符）和Fortran语言（用空格），但C++选择了单引号——大概是因为程序员对单引号最熟悉。

### 语法规则

1. 单引号可以放在数字之间的任意位置
2. 可以连续放多个（比如`0b1111'0000'1111'0000`）
3. 不能放在数字开头或结尾
4. 进制前缀（`0x`、`0b`）后面可以直接跟数字

```cpp
#include <iostream>
#include <cstdint>

int main() {
    // C++14: 数字分隔符（单引号）
    // 目的：让长数字更易读，完全不影响数值！
    
    // 十进制：千位分隔
    int million = 1'000'000;          // 一百万
    int credit = 4'999'999;           // 信用卡号？不，这只是五百万减一
    int population = 1'400'000'000;    // 十四亿
    
    // 二进制：每4位一组（符合人类的阅读习惯）
    int mask = 0b1111'0000'1111'0000;  // 高低四位都是1
    
    // 十六进制：每2位一组
    int color = 0xFF'00'00;  // 纯红色（ARGB格式）
    
    // long long：天文数字也能readably
    long long big = 9'223'372'036'854'775'807LL;  // LLONG_MAX
    
    std::cout << "million = " << million << std::endl;  // 输出: 1000000
    std::cout << "credit = " << credit << std::endl;  // 输出: 4999999
    std::cout << "population = " << population << std::endl;  // 输出: 1400000000
    
    std::cout << std::hex;  // 切换到十六进制输出
    std::cout << "mask = 0x" << mask << std::endl;  // 输出: mask = 0xf0f0
    std::cout << "color = 0x" << color << std::endl;  // 输出: color = 0xff0000
    
    std::cout << std::dec;  // 切回十进制
    std::cout << "big = " << big << std::endl;  // 输出: 9223372036854775807
    
    return 0;
}
```

### 实际应用

数字分隔符在以下场景特别有用：

```cpp
#include <iostream>

int main() {
    // 物理/数学常数
    const double AVOGADRO = 6.022'140'76e23;  // 阿伏伽德罗常数
    const double PLANCK = 6.626'070'15e-34;   // 普朗克常数
    
    // 金额（会计领域）
    long double price = 1'999'999.99;  // 将近两百万
    long double tax = 199'999.90;      // 约二十万税
    
    // 字节数
    const size_t KB = 1'024;           // 1KB = 1024字节
    const size_t MB = 1'048'576;       // 1MB = 1024*1024
    const size_t GB = 1'073'741'824;   // 1GB = 1024^3
    const size_t TB = 1'099'511'627'776;  // 1TB
    
    std::cout << "1KB = " << KB << " bytes" << std::endl;  // 输出: 1KB = 1024 bytes
    std::cout << "1MB = " << MB << " bytes" << std::endl;  // 输出: 1MB = 1048576 bytes
    std::cout << "1GB = " << GB << " bytes" << std::endl;  // 输出: 1GB = 1073741824 bytes
    
    return 0;
}
```

### 幽默一刻

数字分隔符的灵感来源其实很有趣：

- Pascal：用点（`1.000.000`）——但这和浮点数小数点冲突了
- Ada：用下划线（`1_000_000`）——C++也曾考虑过这个
- Fortran：用空格（`1 000 000`）——但空格在代码里经常被忽略
- 最终C++：用单引号（`1'000'000`）

为什么选单引号？因为它是键盘上唯一"不属于数字、运算符或标识符"的字符。所以当你写`int x = 0b1010'0101;`时，编译器可以明确知道分隔符只是用来提升可读性的，不会影响实际数值。

---

## 24.6 返回类型推导

### 什么是返回类型推导？

**返回类型推导**（Return Type Deduction）允许编译器自动推断函数的返回类型，你不需要显式写出返回值类型。这就像是点菜时说"来个招牌菜"，服务员会根据你的口味推荐具体是哪道。

### 语法

```cpp
auto 函数名(参数) { return 表达式; }
// 或者
decltype(auto) 函数名(参数) { return 表达式; }
```

### auto vs decltype(auto)

这两者有什么区别？

| 形式 | 行为 |
|-----|------|
| `auto` | 推导返回值类型，会丢掉引用和const |
| `decltype(auto)` | 推导返回值类型，保持引用和const |

```cpp
#include <iostream>

// C++14: 函数返回类型推导
// 使用auto作为返回类型，编译器会自动推断

auto add(int a, int b) {
    return a + b;  // 编译器推导返回类型为int
}

// 使用decltype(auto)保持表达式的类型语义
decltype(auto) multiply(int a, int b) {
    return a * b;  // 保持表达式类型，这里是int
}

// 引用类型演示
int x = 10;
auto get_x() { return x; }           // 返回int，不是int&
// decltype(auto) get_x_ref() { return x; }  // 返回int&

int main() {
    std::cout << "add(3, 4) = " << add(3, 4) << std::endl;  // 输出: 7
    std::cout << "multiply(5, 6) = " << multiply(5, 6) << std::endl;  // 输出: 30
    
    // 验证返回类型
    std::cout << "sizeof(add(3,4)) = " << sizeof(add(3, 4)) << std::endl;  // 输出: 4 (int的大小)
    
    return 0;
}
```

### decltype规则简介

`decltype`会根据表达式推导类型，规则如下：

- 如果表达式是标识符或类成员访问，返回该对象的类型
- 如果表达式是函数调用，返回该函数的声明返回类型
- 其他情况，返回该表达式的类型

```cpp
#include <iostream>
#include <type_traits>

int global_var = 42;
int& get_ref() { return global_var; }
const int const_val = 100;

int main() {
    // decltype(auto)的行为演示
    
    // 返回int（标识符规则）
    decltype(auto) a = global_var;  // int
    
    // 返回int&（引用规则）
    decltype(auto) b = get_ref();   // int&
    
    // 返回const int（常量规则）
    decltype(auto) c = const_val;   // const int
    
    std::cout << std::boolalpha;
    std::cout << "is_same<decltype(a), int>: " 
              << std::is_same<decltype(a), int>::value << std::endl;  // 输出: true
    std::cout << "is_same<decltype(b), int&>: " 
              << std::is_same<decltype(b), int&>::value << std::endl;  // 输出: true
    std::cout << "is_same<decltype(c), const int>: " 
              << std::is_same<decltype(c), const int>::value << std::endl;  // 输出: true
    
    return 0;
}
```

### 限制和注意事项

返回类型推导不是万能的：

1. **前向声明问题**：如果你声明了返回类型推导的函数，在定义之前调用它，编译器可能无法正确处理
2. **多返回值的函数**：如果函数有多个return语句且返回类型不一致，编译器会报错
3. **虚函数**：虚函数不能使用返回类型推导

```cpp
#include <iostream>

// 错误示例：多个返回类型不一致
// auto wrong(int flag) {
//     if (flag > 0) return 1;      // int
//     else return 2.0;             // double - 冲突！
// }

// 正确示例：多个return但类型一致
auto absolute(int n) {
    if (n >= 0) return n;     // 返回int
    else return -n;           // 返回int，类型一致
}

int main() {
    std::cout << "absolute(-5) = " << absolute(-5) << std::endl;  // 输出: 5
    
    return 0;
}
```

### 幽默一刻

返回类型推导有一个著名的"陷阱"：

```cpp
auto make_int() { return 1; }
```

你觉得返回类型是什么？`int`？恭喜你，答对了。

但如果是：

```cpp
const int& foo();
auto bar() { return foo(); }
```

`bar()`的返回类型是什么？`int`？还是`const int&`？

答案是`int`——因为`auto`会丢掉引用和const修饰符。如果你想要保留`const int&`，得用`decltype(auto)`。

所以记住：`auto`是"差不多就行"，`decltype(auto)`是"原汁原味"。

---

## 24.7 std::make_unique

### 智能指针的进化史

在C++11之前，管理动态内存是一项技术活——`new`和`delete`配对使用，稍有不慎就会内存泄漏。到了C++11，标准库引入了**智能指针**，让内存管理变得自动化。

C++11有`std::shared_ptr`（共享所有权）和`std::unique_ptr`（独占所有权），但有个问题：`std::make_shared`早就有了，`std::make_unique`却迟迟没有加入标准库。

这就好比餐厅提供打包盒（shared），但不提供外卖袋（unique）——你得自己找袋子装。

C++14终于补上了这个漏洞。

### std::make_unique是什么？

**std::make_unique**是一个辅助函数，用于创建`std::unique_ptr`对象。它比直接使用`new`构造更安全、更简洁。

```cpp
#include <iostream>
#include <memory>

// 定义一个Widget类来演示构造和析构
struct Widget {
    Widget() { std::cout << "Widget constructed" << std::endl; }
    ~Widget() { std::cout << "Widget destructed" << std::endl; }
};

int main() {
    // C++14: std::make_unique（之前只有make_shared）
    // 语法：std::make_unique<T>(构造参数...)
    
    // 创建单个对象
    auto up1 = std::make_unique<int>(42);
    std::cout << "Value: " << *up1 << std::endl;  // 输出: 42
    
    // 创建数组（C++14支持数组形式的make_unique）
    auto upArr = std::make_unique<int[]>(5);
    upArr[0] = 10;
    upArr[1] = 20;
    std::cout << "upArr[0] = " << upArr[0] << std::endl;  // 输出: 10
    std::cout << "upArr[1] = " << upArr[1] << std::endl;  // 输出: 20
    
    // 异常安全演示
    // make_unique在构造前分配内存，更安全
    // 如果构造过程中抛出异常，已分配的内存会被自动释放
    auto w = std::make_unique<Widget>();  // 会打印 "Widget constructed"
    
    std::cout << "Widget正在发挥作用..." << std::endl;
    
    // 函数结束时，w会自动销毁，打印 "Widget destructed"
    
    return 0;
}
```

### 为什么推荐使用make_unique？

1. **异常安全**：直接用`new`构造时，如果构造函数抛出异常，内存可能泄漏
2. **代码简洁**：不需要重复写类型名
3. **性能优化**：`make_unique`可以一次性分配对象和引用计数块（对于shared_ptr）

```cpp
#include <iostream>
#include <memory>

struct Resource {
    Resource() { std::cout << "Resource acquired" << std::endl; }
    ~Resource() { std::cout << "Resource released" << std::endl; }
};

void process_with_raw_pointer() {
    // 危险！如果do_something()抛出异常，内存泄漏
    Resource* r = new Resource();
    // do_something();  // 假设这里抛出异常
    delete r;  // 永远不会执行到
}

void process_with_unique_ptr() {
    // 安全！即使do_something()抛出异常，unique_ptr也会释放资源
    auto r = std::make_unique<Resource>();
    // do_something();  // 假设这里抛出异常
    // r会自动销毁
}

int main() {
    std::cout << "=== 使用裸指针 ===" << std::endl;
    // process_with_raw_pointer();
    
    std::cout << "=== 使用unique_ptr ===" << std::endl;
    process_with_unique_ptr();
    
    return 0;
}
```

### 实际使用场景

```cpp
#include <iostream>
#include <memory>
#include <vector>

class Node {
public:
    int value;
    std::unique_ptr<Node> next;
    
    Node(int v) : value(v), next(nullptr) {
        std::cout << "Node(" << value << ") created" << std::endl;
    }
    
    ~Node() {
        std::cout << "Node(" << value << ") destroyed" << std::endl;
    }
};

int main() {
    // 创建链表
    auto head = std::make_unique<Node>(1);
    head->next = std::make_unique<Node>(2);
    head->next->next = std::make_unique<Node>(3);
    
    // 遍历链表
    std::cout << "链表内容: ";
    for (auto* cur = head.get(); cur != nullptr; cur = cur->next.get()) {
        std::cout << cur->value << " ";
    }
    std::cout << std::endl;
    
    // unique_ptr超出作用域后自动释放所有节点
    
    return 0;
}
```

### 幽默一刻

关于`make_unique`有个趣事：C++11就有`make_shared`，但`make_unique`要等到C++14才加入。有人问Bjarne Stroustrup为什么，他说："呃...我们忘了？"

这大概是标准委员会唯一一次承认"我们忘了一件事"。

---

## 24.8 带初始化捕获的Lambda

### 什么是Lambda捕获？

Lambda表达式可以"捕获"外部变量，使其在Lambda内部可见。但C++11的捕获方式有限：

- `[=]`：按值捕获所有变量
- `[&]`：按引用捕获所有变量
- `[x]`：按值捕获x
- `[&x]`：按引用捕获x

问题来了：**如果我想捕获一个表达式结果，而不是变量本身呢？**比如捕获一个`std::unique_ptr`的移动后的状态。

### C++11的困境：移动捕获的缺失

在C++11中，Lambda不支持移动捕获。如果你想"捕获"一个即将被移动的对象，你只能先复制或移动到局部变量，然后捕获它：

```cpp
// C++11做不到的事情
auto up = std::make_unique<int>(42);
// 想捕获up的移动后的状态？
// [up = std::move(up)]  // C++11: 语法错误！
```

### C++14：初始化捕获

C++14引入了**初始化捕获**（Generalized Lambda Captures），允许你用任意表达式初始化捕获值：

```cpp
[identifier = expression] (params) { body }
```

这解决了两个问题：
1. **移动捕获**：将即将销毁的对象移动到Lambda中
2. **重命名捕获**：给捕获的变量起个新名字

```cpp
#include <iostream>
#include <memory>
#include <vector>
#include <algorithm>
#include <utility>

int main() {
    // C++14: Lambda初始化捕获（移动捕获）
    // 语法：[捕获名 = 表达式]
    
    // 创建unique_ptr
    auto up = std::make_unique<int>(42);
    
    // 初始化捕获：将std::move(up)的结果捕获为value
    // up的所有权被转移给Lambda内部的value
    auto captured = [value = std::move(up)]() {
        return *value;  // 现在unique_ptr在Lambda内部，up变成nullptr
    };
    
    std::cout << "captured() = " << captured() << std::endl;  // 输出: 42
    
    // 更复杂的例子：同时获取最小值和最大值
    std::vector<int> data = {1, 2, 3, 4, 5};
    
    // 使用初始化捕获移动data到Lambda中
    // 然后用结构化绑定(C++17特性，这里是简化的写法)
    auto result = [data = std::move(data)]() {
        auto minmax = std::minmax_element(data.begin(), data.end());
        return std::pair<int, int>(*minmax.first, *minmax.second);
    };
    
    auto [minVal, maxVal] = result();
    std::cout << "min=" << minVal << ", max=" << maxVal << std::endl;  // 输出: min=1, max=5
    
    // data现在已经被移动走了
    std::cout << "data的大小: " << data.size() << std::endl;  // 输出: 0
    
    return 0;
}
```

### 初始化捕获的工作原理

初始化捕获其实是两个步骤的简写：

1. **创建临时变量**：用表达式的结果初始化一个变量
2. **捕获该变量**：按值或按引用捕获这个新变量

```cpp
#include <iostream>
#include <memory>
#include <string>

int main() {
    // [x = expr] 相当于：
    // 1. 用expr初始化一个隐藏的变量
    // 2. 按值捕获这个变量
    
    // 例子：捕获计算结果
    auto compute_and_capture = [result = 1 + 2 + 3]() {
        return result;  // 返回6
    };
    std::cout << "计算结果: " << compute_and_capture() << std::endl;  // 输出: 6
    
    // 例子：捕获字符串的一部分
    std::string full_name = "John Doe";
    auto last_name = [name = full_name.substr(5)]() {  // substr返回" Doe"
        return name;
    };
    std::cout << "姓氏: '" << last_name() << "'" << std::endl;  // 输出: ' Doe'
    
    // 例子：按引用初始化捕获
    int counter = 0;
    auto increment = [&cnt = counter]() {
        ++cnt;  // 修改外部的counter
    };
    increment();
    std::cout << "计数器: " << counter << std::endl;  // 输出: 1
    
    return 0;
}
```

### 实际应用场景

```cpp
#include <iostream>
#include <memory>
#include <functional>

class Database {
public:
    int query(const char* sql) {
        std::cout << "执行SQL: " << sql << std::endl;
        return 42;
    }
};

int main() {
    // 场景1：绑定移动后的对象
    auto conn = std::make_unique<Database>();
    
    // 移动conn到Lambda中，外部的conn变为空
    auto query_func = [db = std::move(conn)](const char* sql) {
        return db->query(sql);
    };
    
    // 场景2：创建带状态的回调
    int invocation_count = 0;
    auto counting_callback = [count = 0]() mutable {
        ++count;  // mutable允许修改按值捕获的变量
        return count;
    };
    
    std::cout << "第1次调用: " << counting_callback() << std::endl;  // 输出: 1
    std::cout << "第2次调用: " << counting_callback() << std::endl;  // 输出: 2
    std::cout << "第3次调用: " << counting_callback() << std::endl;  // 输出: 3
    
    // 注意：每次调用创建新的count，因为Lambda是按值捕获的
    // 这是"拷贝"不是"引用"，所以不会影响外部的invocation_count
    
    return 0;
}
```

### 幽默一刻

初始化捕获的语法刚出来的时候，很多人吐槽："这不就是把赋值语句塞进中括号里吗？"

没错，确实是这样。但就是这么一个简单的语法扩展，解决了C++元编程中的一大痛点。

想象一下没有初始化捕获的世界：你有一个`unique_ptr`，想把它移动到Lambda里，怎么办？你得先`std::move`到一个局部变量，然后捕获那个变量。但问题是——那个局部变量本身就是个累赘。

有了初始化捕获，一行搞定：`[ptr = std::move(original_ptr)]()`。

---

## 本章小结

C++14是C++11之后的一次重要补丁更新，它不是在开创新的范式，而是在完善已有的功能。本章我们学习了C++14的八大特性：

### 24.1 泛型Lambda
- **核心变化**：`auto`可以用于Lambda参数
- **解决的问题**：同一个Lambda可以处理不同类型的参数
- **应用场景**：STL算法、回调函数、泛型编程

### 24.2 变量模板
- **核心变化**：模板可以用于定义变量
- **解决的问题**：类型特征（type traits）的`::value`可以简写为`_v`
- **应用场景**：编译期类型查询、类型大小判断

### 24.3 放宽的constexpr限制
- **核心变化**：constexpr函数中可以使用局部变量和循环
- **解决的问题**：更强大的编译期计算能力
- **应用场景**：编译期数学计算、查表优化

### 24.4 二进制字面量
- **核心变化**：`0b`前缀可以直接写二进制数
- **解决的问题**：不需要手动转换进制
- **应用场景**：位掩码、权限控制、硬件编程

### 24.5 数字分隔符
- **核心变化**：数字字面量中可以用单引号分隔
- **解决的问题**：长数字的可读性
- **应用场景**：金额、字节数、科学常数

### 24.6 返回类型推导
- **核心变化**：`auto`可以推导函数返回类型
- **解决的问题**：简化函数声明
- **注意事项**：区分`auto`和`decltype(auto)`的类型推导规则

### 24.7 std::make_unique
- **核心变化**：`make_unique`加入标准库
- **解决的问题**：创建`unique_ptr`更安全、更简洁
- **应用场景**：独占所有权的资源管理

### 24.8 带初始化捕获的Lambda
- **核心变化**：捕获列表可以使用表达式初始化
- **解决的问题**：移动捕获、重命名捕获
- **应用场景**：移动语义与Lambda结合

> 📝 **学习建议**：C++14的特性虽然看起来简单，但都是"用时方恨少"的实用工具。建议读者在实践中多使用这些特性，感受它们带来的便利。
