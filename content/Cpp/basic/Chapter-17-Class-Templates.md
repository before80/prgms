+++
title = "第17章 类模板"
weight = 170
date = "2026-03-29T21:03:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++
# 第17章 类模板

想象一下，你是快餐店的点餐员。如果每个顾客来你都要重新设计一套点餐系统——汉堡工程师、薯条工程师、可乐工程师——那这个世界早就乱套了。好在类模板（Class Template）就是程序员的"通用点餐系统"，一份代码，服务所有类型！

## 17.1 类模板的定义与使用

### 什么是类模板？

类模板，简单来说就是**类的蓝图工厂**。普通的类就像是只卖一种汉堡的店，而类模板则是能生产各种口味汉堡的全能厨房。你声明一次，编译器帮你生成int版本、string版本、甚至自定义版本的"汉堡"。

> 类模板允许你编写与类型无关的代码。在声明时使用 `template<typename T>` 或 `template<class T>`，其中的 T 就像是一个占位符，具体类型由使用时指定。

### 为什么需要类模板？

假设你要实现一个栈（Stack）数据结构：
- 用 `int` 时需要一套代码
- 用 `string` 时又需要另一套
- 用自定义类时还得再来一套

这简直是**Ctrl+C/V 程序员的噩梦**！类模板帮你解决这个问题——**一次编写，到处实例化**。

```cpp
#include <iostream>
#include <vector>
#include <stdexcept>
#include <string>      // Stack<std::string> 需要它

// 类模板：让类与类型参数无关
// template<typename T> 告诉编译器：T是一个类型参数，稍后填充
template<typename T>
class Stack {
private:
    static const int MAX_SIZE = 100;  // 栈的最大容量，防止无限膨胀
    T data_[MAX_SIZE];                // 用类型 T 的数组存储数据
    int top_;                         // 栈顶指针，-1表示空栈

public:
    // 构造函数：初始化空栈
    Stack() : top_(-1) {}

    // push: 把元素压入栈顶
    void push(const T& value) {
        if (top_ >= MAX_SIZE - 1) {
            // 栈满了！就像往已经装满的行李箱里硬塞东西
            throw std::overflow_error("Stack overflow!");
        }
        data_[++top_] = value;  // 先移动指针，再存数据
    }

    // pop: 弹出栈顶元素并返回
    T pop() {
        if (top_ < 0) {
            // 栈空了还要弹？想象从空冰箱里拿牛奶...
            throw std::underflow_error("Stack underflow!");
        }
        return data_[top_--];  // 返回顶部数据，然后指针下移
    }

    // peek: 查看栈顶元素（但不弹出）
    T peek() const {
        if (top_ < 0) {
            throw std::underflow_error("Stack is empty!");
        }
        return data_[top_];
    }

    bool empty() const { return top_ == -1; }   // 判断栈是否为空
    int size() const { return top_ + 1; }     // 返回元素个数
};

int main() {
    // 实例化不同类型的Stack
    // 就像点餐：intStack是巨无霸套餐，stringStack是蔬菜沙拉
    Stack<int> intStack;
    Stack<std::string> stringStack;

    // intStack 的操作
    intStack.push(10);   // 压入10
    intStack.push(20);   // 压入20
    intStack.push(30);   // 压入30，此时栈顶是30

    std::cout << "intStack.pop() = " << intStack.pop() << std::endl;  // 输出: 30
    std::cout << "intStack.peek() = " << intStack.peek() << std::endl;  // 输出: 20

    // stringStack 的操作
    stringStack.push("Hello");
    stringStack.push("World");

    std::cout << "stringStack.pop() = " << stringStack.pop() << std::endl;  // 输出: World

    return 0;
}
```

运行结果：
```text
intStack.pop() = 30
intStack.peek() = 20
stringStack.pop() = World
```

> 💡 **小贴士**：类模板本身不是类，它是生成类的"模具"。当你写 `Stack<int>` 时，编译器才会真正生成一个 `Stack` 类。这个过程叫做**实例化**（Instantiation）。

### 类模板的工作原理

Mermaid 图表的魅力在于能让复杂的事情变简单（就像我们的类模板）：

```mermaid
graph LR
    A["template&lt;typename T&gt;<br/>class Stack"] --> B["Stack&lt;int&gt;"]
    A --> C["Stack&lt;string&gt;"]
    A --> D["Stack&lt;double&gt;"]
    B --> E["int 类型的栈"]
    C --> F["string 类型的栈"]
    D --> G["double 类型的栈"]
```

## 17.2 类模板的成员函数

### 成员函数也是模板？

没错！在类模板中，不仅数据成员的类型是 T，连**成员函数也可以是模板**。这就像是汉堡店不仅卖不同口味的汉堡，还卖不同口味的薯条。

### 在类内定义 vs 在类外定义

```cpp
#include <iostream>

template<typename T>
class Wrapper {
private:
    T value_;  // 包装的值

public:
    // 普通成员函数：类内定义
    Wrapper(const T& value) : value_(value) {}

    void print() const {
        std::cout << "Wrapper value: " << value_ << std::endl;
    }

    T get() const { return value_; }      // getter

    void set(const T& value) { value_ = value; }  // setter

    // 模板成员函数：在类外定义
    // 这个函数厉害了——它能把 T 转成任意类型 U！
    template<typename U>
    U convert() const;
};

// 模板成员函数的类外定义语法：
// 必须同时声明两个 template 参数
template<typename T>
template<typename U>
U Wrapper<T>::convert() const {
    // static_cast<U>(value_) 尝试把 value_ 转成 U 类型
    return static_cast<U>(value_);
}

int main() {
    Wrapper<int> w(42);  // 包装了一个 int 类型的 42

    w.print();  // 输出: Wrapper value: 42

    // convert<double>() 会把 int 转成 double
    std::cout << "As double: " << w.convert<double>() << std::endl;  // 输出: 42

    return 0;
}
```

输出：
```text
Wrapper value: 42
As double: 42
```

> 🔍 **专业术语解析**：
> - **模板成员函数**：成员函数本身也是模板，可以独立于类模板参数使用
> - **双层模板**：在类外定义模板成员函数时，需要两个 `template<>` 声明

### 为什么需要模板成员函数？

想象这样一个场景：你有一个 `Wrapper<int>`，但你需要把它转成 `double`、`string`（如果支持的话）或者其他任何类型。普通的成员函数做不到，但模板成员函数可以！

## 17.3 类模板的特化

### 全特化

有时候，通用模板对某些特定类型不太适用。比如你想比较两个 `const char*`（C风格字符串），通用版本会比较指针地址，而不是字符串内容。这就像是比较两个房子的地址，而不是房子里的内容！

```cpp
#include <iostream>
#include <cstring>

// 通用版本：适用于大多数类型
template<typename T>
class Comparator {
public:
    static bool equal(const T& a, const T& b) {
        return a == b;  // 直接用 == 比较
    }
};

// 全特化：为 const char* 提供特殊实现
// template<> 告诉编译器：这是个"特例"，不跟你讲道理
template<>
class Comparator<const char*> {
public:
    static bool equal(const char* a, const char* b) {
        // C风格字符串比较地址？那是菜鸟干的事！
        // 正确的做法是用 strcmp 比较内容
        return strcmp(a, b) == 0;
    }
};

int main() {
    // int 类型的比较：使用通用版本
    std::cout << "Comparator<int>::equal(1, 1) = "
              << Comparator<int>::equal(1, 1) << std::endl;  // 输出: 1 (true)
    std::cout << "Comparator<int>::equal(1, 2) = "
              << Comparator<int>::equal(1, 2) << std::endl;  // 输出: 0 (false)

    // const char* 类型的比较：使用全特化版本
    std::cout << "Comparator<const char*>::equal(\"hello\", \"hello\") = "
              << Comparator<const char*>::equal("hello", "hello") << std::endl;  // 输出: 1
    std::cout << "Comparator<const char*>::equal(\"hello\", \"world\") = "
              << Comparator<const char*>::equal("hello", "world") << std::endl;  // 输出: 0

    return 0;
}
```

输出：
```text
Comparator<int>::equal(1, 1) = 1
Comparator<int>::equal(1, 2) = 0
Comparator<const char*>::equal("hello", "hello") = 1
Comparator<const char*>::equal("hello", "world") = 0
```

> 📝 **全特化**：当模板参数全部确定时，为特定类型提供特殊实现。就像是通用汉堡配方对"鱼排汉堡"不适用，得专门写个配方。

### 偏特化

偏特化是全特化的"温柔版"。全特化是"这个类型我专门处理"，偏特化是"这类情况我稍微调整一下"。

```cpp
#include <iostream>

// 通用版本：两个模板参数，没有限制
template<typename T, typename U>
class Pair {
public:
    static const char* type() { return "Pair<T, U>"; }
};

// 偏特化1：两个类型相同
// 当 T 和 U 相同时，使用这个版本
template<typename T>
class Pair<T, T> {
public:
    static const char* type() { return "Pair<T, T> (same type)"; }
};

// 偏特化2：第二个类型是 int
// 即使 T 和 U 不同，但 U 是 int 的话...
template<typename T>
class Pair<T, int> {
public:
    static const char* type() { return "Pair<T, int>"; }
};

// 偏特化3：两个都是指针类型
template<typename T>
class Pair<T*, T*> {
public:
    static const char* type() { return "Pair<T*, T*> (both pointers)"; }
};

int main() {
    Pair<double, double> p1;  // 匹配偏特化1：Pair<T, T>
    Pair<double, int> p2;     // 匹配偏特化2：Pair<T, int>
    Pair<int*, int*> p3;      // 匹配偏特化3：Pair<T*, T*>
    Pair<double, char> p4;    // 匹配通用版本：Pair<T, U>

    std::cout << "p1: " << decltype(p1)::type() << std::endl;
    std::cout << "p2: " << decltype(p2)::type() << std::endl;
    std::cout << "p3: " << decltype(p3)::type() << std::endl;
    std::cout << "p4: " << decltype(p4)::type() << std::endl;

    return 0;
}
```

输出：
```text
p1: Pair<T, T> (same type)
p2: Pair<T, int>
p3: Pair<T*, T*> (both pointers)
p4: Pair<T, U>
```

> ⚠️ **编译器选老婆的规则**：
> 编译器选择模板版本时，遵循"越具体越好"原则。就像找对象：
> - 通用模板：要求不高，但可能被更具体的版本"截胡"
> - 偏特化：条件更具体，优先匹配
> - 全特化：完全确定，直接"领证"

### 全特化 vs 偏特化

```mermaid
graph TD
    A["template<typename T, typename U><br/>class Pair"] --> B["全特化<br/>template<><br/>class Pair<int, double>"]
    A --> C["偏特化1<br/>template<typename T><br/>class Pair<T, T>"]
    A --> D["偏特化2<br/>template<typename T><br/>class Pair<T*, T*>"]
```

## 17.4 模板嵌套与模板模板参数

### 模板模板参数？嵌套模板？这名字听着就头疼！

别慌！让我们用点餐系统来理解。你走进一家餐厅：
- 普通模板参数：`int`、`string` 是具体的食材
- 模板模板参数：`vector`、`list` 是**装食材的容器类型**本身

```cpp
#include <iostream>
#include <vector>

// 模板模板参数：Container 本身是一个模板
// 语法：template<typename> class Container
// 含义：Container 是一个"只吃一个类型参数"的类模板
template<typename T, template<typename> class Container>
class Repository {
private:
    Container<T> data_;   // 用 Container<T> 作为底层存储

public:
    void add(const T& value) {
        data_.push_back(value);   // 要求 Container 有 push_back
    }

    void print() const {
        for (auto it = data_.begin(); it != data_.end(); ++it) {
            if (it != data_.begin()) std::cout << " ";
            std::cout << *it;
        }
        std::cout << std::endl;
    }
};

int main() {
    // C++17 起（P0522R0，被各家编译器当作缺陷修复回溯应用）：
    // 即使 std::vector 声明的是 template<typename T, typename Alloc = ...>，
    // 也能匹配"只吃一个参数"的模板模板参数——只要多出来的参数带默认值。
    Repository<int, std::vector> repo;
    repo.add(1);
    repo.add(2);
    repo.add(3);
    repo.print();   // 输出: 1 2 3

    return 0;
}
```

输出：
```text
1 2 3
```

> ⚠️ **这段历史值得单独说一句**：在 C++11/14 时代，上面的代码**是编译不过的**。
> 当时的规则要求"模板模板实参和模板模板形参的形参列表必须完全一致"，而 `std::vector` 有两个参数
> （`T` 和 `Alloc`，后者有默认值），`template<typename> class Container` 只有一个，于是匹配失败——
> "带默认值"也救不了它，因为当时只看形参列表的**形状**。
>
> 后来 **P0522R0**（*Matching of template template-parameters to template template-arguments*）
> 放宽了这条规则：多出来的参数只要有默认值，就允许匹配。这条修改被当作**缺陷修复**回溯应用，
> GCC / Clang / MSVC 现在在所有标准模式下都按新规则办事。本节代码用 Apple clang 21 实测，
> 从 `-std=c++11` 到 `-std=c++23` 全部通过。

### `typename...` 版本：更保险，也更常见的写法

既然 `template<typename>` 已经能匹配 `std::vector` 了，为什么还会看到
`template<typename, typename...> class Container` 这种写法？

因为它**不依赖上面那条放宽规则**，在老编译器上也能工作，是写库时更稳的选择：

```cpp
#include <iostream>
#include <set>
#include <vector>

// 写法：只要"至少一个类型参数"，后面的额外参数（如 Alloc、Compare）全部吸收
template<typename T, template<typename, typename...> class Container>
struct Repo {
    Container<T> data_;
    void add(const T& v) { data_.push_back(v); }
};

int main() {
    Repo<int, std::vector> a;
    a.add(1);          // ✅ vector 有 push_back

    Repo<int, std::set> b;   // ⚠️ 这一行本身能编译过！
    // b.add(2);            // ❌ 一旦调用 add()，才会报错：
    //                      //    'std::set<int>' has no member named 'push_back'

    std::cout << "模板模板参数只检查形状，不检查成员\n";

    (void)b;
    return 0;
}
```

输出：
```text
模板模板参数只检查形状，不检查成员
```

> 🎯 **两个关键结论**：
> 1. **模板模板参数只匹配"形状"**——参数个数对不对、类型对不对，编译器一看就知道；
>    但"容器有没有 `push_back`"这种**成员层面的要求，编译器不会提前检查**。
> 2. 类模板的成员函数**只有被用到时才实例化**。所以 `Repo<int, std::set> b;` 能编过，
>    `b.add(2)` 才会爆炸。这就是模板报错经常"又长又难懂"的根源：错误发生的时机，离你写错的地方很远。
>
> **实用建议**：写库、要求新老编译器通吃，就用 `template<typename, typename...> class`；
> 只面向 C++17 及以后的现代编译器，`template<typename> class` 更简洁易读。

## 17.5 类型萃取与SFINAE

### SFINAE：模板界的"备胎"机制

SFINAE 全称是 **Substitution Failure Is Not An Error**——翻译成中文就是"替换失败不算错"。这名字简直是程序员式的绕口令！

想象你写了一个函数，可以计算任何数字的绝对值：
```cpp
template<typename T>
T my_abs(T value) {
    return value < 0 ? -value : value;
}
```

但如果有人传了 `"hello"` 字符串呢？编译器不会报错，而是会**跳过这个重载，去找其他版本**。就像追求者A说"我不会做饭"，你不会生气（大概吧），而是优雅地转向下一个追求者——这就是 SFINAE 的精髓：**此路不通，另寻他路，编译器绝不崩溃**。

> ⚠️ **注意这里的函数名**：上面故意用了 `my_abs` 而不是 `abs`。因为 `<cstdlib>` / `<cmath>` 里已经有一个全局的 `::abs(int)`，你如果也定义全局的 `abs`，非模板版本会在重载决议里赢过你的模板，SFINAE 的演示效果就被"截胡"了。**给模板函数起个专属名字，是避免这类意外最省事的办法。**

```cpp
#include <iostream>
#include <type_traits>

// SFINAE: Substitution Failure Is Not An Error
// 模板替换失败不算错误，编译器会选择其他重载
// 如果 T 是整数类型，用这个版本
template<typename T>
typename std::enable_if<std::is_integral<T>::value, T>::type
my_abs(T value) {
    return value < 0 ? -value : value;
}

// 如果 T 是浮点类型，用这个版本
template<typename T>
typename std::enable_if<std::is_floating_point<T>::value, T>::type
my_abs(T value) {
    return value < 0 ? -value : value;
}

// C++14简化写法：enable_if_t 是 enable_if::type 的别名
template<typename T>
std::enable_if_t<std::is_integral_v<T>, T>
square(T value) {
    return value * value;
}

// C++17: if constexpr 在编译期选择分支
// 这比 SFINAE 直观多了！
template<typename T>
auto describe(T value) {
    if constexpr (std::is_integral_v<T>) {
        return "integer";  // 整数类型
    } else if constexpr (std::is_floating_point_v<T>) {
        return "floating point";  // 浮点类型
    } else {
        return "other";  // 其他类型
    }
}

int main() {
    std::cout << "my_abs(-5) = " << my_abs(-5) << std::endl;  // 输出: 5
    std::cout << "my_abs(-3.14) = " << my_abs(-3.14) << std::endl;  // 输出: 3.14

    std::cout << "square(7) = " << square(7) << std::endl;  // 输出: 49

    std::cout << "describe(42) = " << describe(42) << std::endl;
    std::cout << "describe(3.14) = " << describe(3.14) << std::endl;
    std::cout << "describe(\"hello\") = " << describe("hello") << std::endl;

    return 0;
}
```

输出：
```text
my_abs(-5) = 5
my_abs(-3.14) = 3.14
square(7) = 49
describe(42) = integer
describe(3.14) = floating point
describe("hello") = other
```

> 📚 **类型萃取（Type Traits）**：`<type_traits>` 头文件提供了一系列工具，用来在编译期查询和操作类型信息。比如 `std::is_integral<T>` 可以在编译期判断 T 是否是整数类型。

### SFINAE vs if constexpr

```mermaid
graph LR
    A["SFINAE"] --> B["enable_if<br/>控制函数是否存在"]
    A --> C["编译期选择<br/>通过重载决议"]
    D["if constexpr"] --> E["编译期选择<br/>直接控制分支"]
    D --> F["更直观<br/>C++17+"]
```

> 💡 **实战建议**：
> - C++17 之前：使用 SFINAE + `enable_if`
> - C++17 及之后：`if constexpr` 是更好的选择，代码更清晰

## 17.6 概念与约束（C++20）

### requires子句

C++20 引入了**概念（Concept）**这个重磅特性。如果说 SFINAE 是"暗箱操作"，那概念就是"明码标价"——你可以直接告诉编译器："这个模板参数必须满足这些条件！"

```cpp
#include <iostream>
#include <concepts>

// 概念定义：约束模板参数必须满足的条件
// Numeric 概念：T 必须是整数或浮点数
template<typename T>
concept Numeric = std::integral<T> || std::floating_point<T>;

// 方式1：requires 子句
template<typename T>
    requires Numeric<T>  // T 必须满足 Numeric 概念
T add(T a, T b) {
    return a + b;
}

// 方式2：concept 作为类型约束（更简洁）
template<std::integral T>  // T 必须是整数类型
T multiply(T a, T b) {
    return a * b;
}

// 方式3：requires 表达式（更复杂条件）
// sizeof(T) >= 4 表示 T 至少是 4 字节
template<typename T>
    requires std::is_integral_v<T> && (sizeof(T) >= 4)
T bigMultiply(T a, T b) {
    return a * b;
}

int main() {
    std::cout << "add(1, 2) = " << add(1, 2) << std::endl;  // 输出: 3
    std::cout << "add(1.5, 2.5) = " << add(1.5, 2.5) << std::endl;  // 输出: 4

    std::cout << "multiply(6, 7) = " << multiply(6, 7) << std::endl;  // 输出: 42

    return 0;
}
```

输出：
```text
add(1, 2) = 3
add(1.5, 2.5) = 4
multiply(6, 7) = 42
```

> 🎉 **概念的好处**：
> 1. **更清晰的错误信息**：如果传了不满足条件的类型，编译器会直接告诉你缺少什么——而不是扔给你一页天书般的模板错误
> 2. **更易读的代码**：`std::integral<T>` 比 `typename std::enable_if<...>::type` 直观多了，谁看谁知道
> 3. **编译期检查**：错误在编译期就被发现，而不是运行时莫名其妙崩溃，然后你对着 core dump 怀疑人生

### 概念定义

标准库提供了一些内置概念，但你也可以定义自己的概念。定义概念的语法就像写数学公式一样优雅：

```cpp
#include <iostream>
#include <concepts>
#include <string>
#include <functional>   // std::hash

// 自定义概念：Addable
// 语法：requires (T a, T b) { 表达式 }
// 如果 a + b 能编译通过，就说明 T 满足 Addable
template<typename T>
concept Addable = requires(T a, T b) {
    a + b;  // T必须支持+运算符
};

// 自定义概念：Printable
// 检查 std::cout << a 能否编译
template<typename T>
concept Printable = requires(T a) {
    std::cout << a;  // T必须能打印
};

// 自定义概念：Hashable
// 检查 std::hash<T>{}(a) 能否编译
template<typename T>
concept Hashable = requires(T a) {
    std::hash<T>{}(a);  // T必须能被哈希
};

// 使用概念作为模板约束
template<Addable T>
T sum(T a, T b) {
    return a + b;
}

template<Printable T>
void print(T value) {
    std::cout << value << std::endl;
}

int main() {
    std::cout << "sum(1, 2) = " << sum(1, 2) << std::endl;  // 输出: 3
    std::cout << "sum(1.5, 2.5) = " << sum(1.5, 2.5) << std::endl;  // 输出: 4

    print("Hello, concepts!");  // 输出: Hello, concepts!
    print(42);  // 输出: 42

    return 0;
}
```

输出：
```text
sum(1, 2) = 3
sum(1.5, 2.5) = 4
Hello, concepts!
42
```

> 🔬 **requires 表达式**中的检查项：
> - `a + b`：检查加法是否有效
> - `std::cout << a`：检查是否可输出
> - `std::hash<T>{}(a)`：检查是否可哈希
>
> 这些检查都在**编译期**进行，不会产生任何运行时开销！

### 标准概念库

C++20 的 `<concepts>` 头文件提供了一系列标准概念，比你自己写的更完善、更标准：

```cpp
#include <iostream>
#include <concepts>
#include <vector>
#include <list>

// std::integral：整数类型（char, int, long, short 等）
template<std::integral T>
T factorial(T n) {
    if (n <= 1) return 1;
    return n * factorial(n - 1);
}

// std::floating_point：浮点类型（float, double, long double）
template<std::floating_point T>
T circleArea(T radius) {
    return 3.14159 * radius * radius;
}

// std::movable：可以移动的类型
template<std::movable T>
void takeOwnership(T&& obj) {
    // T必须可以移动
    // 实现了移动构造函数和移动赋值运算符
}

// std::copyable：可以拷贝的类型
template<std::copyable T>
T clone(const T& obj) {
    // T必须可以拷贝
    return obj;
}

// std::regular："正规"类型
// 定义：std::regular<T> = std::semiregular<T> && std::equality_comparable<T>
// 而 semiregular = copyable && default_initializable
// 也就是说，它要求：可默认构造、可拷贝、可移动、可赋值，并且能用 == 比较
// （注意重点是最后的"可比较"——这正是 regular 比 copyable 更严格的地方）
template<std::regular T>
class Container {
    // T必须是regular类型：
    // - 默认构造函数
    // - 拷贝构造函数
    // - 移动构造函数
    // - 拷贝赋值运算符
    // - 移动赋值运算符
    // - 相等比较运算符（operator== / operator!=）
};

int main() {
    std::cout << "factorial(5) = " << factorial(5) << std::endl;  // 输出: 120
    // 注意：默认输出精度是 6 位有效数字，所以是 12.5664 而不是 12.56636
    std::cout << "circleArea(2.0) = " << circleArea(2.0) << std::endl;  // 输出: 12.5664

    // std::vector<int> 满足 std::regular，所以可以实例化 Container
    Container<std::vector<int>> c1;   // ✅ 编译通过

    // 反例：定义一个没写 operator== 的类，就通不过 std::regular 约束
    //   struct NoEq { int x; };
    //   Container<NoEq> bad;   // ❌ error: constraints not satisfied
    //                          //    （因为 NoEq 不满足 equality_comparable）
    (void)c1;

    std::vector<int> v1 = {1, 2, 3};
    std::vector<int> v2 = v1;  // 拷贝操作

    std::cout << "v1.size() = " << v1.size() << ", v2.size() = " << v2.size() << std::endl;
    // 输出: v1.size() = 3, v2.size() = 3

    std::cout << "Container<std::vector<int>> 实例化成功" << std::endl;

    return 0;
}
```

输出：
```text
factorial(5) = 120
circleArea(2.0) = 12.5664
v1.size() = 3, v2.size() = 3
Container<std::vector<int>> 实例化成功
```

> 🏛️ **标准概念一览**：
> | 概念 | 含义 |
> |------|------|
> | `std::integral` | 整数类型 |
> | `std::floating_point` | 浮点类型 |
> | `std::movable` | 可移动 |
> | `std::copyable` | 可拷贝 |
> | `std::default_initializable` | 可默认初始化 |
> | `std::equality_comparable` | 可相等比较 |
> | `std::regular` | "正规"类型 |

## 17.7 类模板参数推导CTAD（C++17）

### 自动推导模板参数

在 C++17 之前，你必须这样写：
```cpp
std::pair<int, double> p(1, 2.5);  // 累死了，还得自己写类型
```

C++17 引入了 **CTAD（Class Template Argument Deduction）**，编译器能自动帮你推导——**懒人福音，类型推断它全包了**：
```cpp
std::pair p(1, 2.5);  // 自动推导为 pair<int, double>！连写两遍的痛苦谁用谁知道
```

```cpp
#include <iostream>

template<typename T, typename U>
struct Pair {
    T first;
    U second;

    // 构造函数帮助推导
    Pair(const T& f, const U& s) : first(f), second(s) {}
};

int main() {
    // C++17: 类模板参数推导（CTAD）
    // 不需要显式指定模板参数
    // 编译器会根据构造函数的参数类型自动推导
    Pair p1(10, 20.5);  // 推导为 Pair<int, double>

    // 推导过程：
    // 构造函数 Pair(const T&, const U&)
    // 参数 10 的类型是 int → T = int
    // 参数 20.5 的类型是 double → U = double

    std::cout << "p1.first = " << p1.first << ", p1.second = " << p1.second << std::endl;
    // 输出: p1.first = 10, p1.second = 20.5

    // 显式指定（当自动推导不满足需求时）
    Pair<int, int> p2(1, 2);

    std::cout << "p2.first = " << p2.first << ", p2.second = " << p2.second << std::endl;
    // 输出: p2.first = 1, p2.second = 2

    return 0;
}
```

输出：
```text
p1.first = 10, p1.second = 20.5
p2.first = 1, p2.second = 2
```

> 🚀 **CTAD 的推导规则**：
> 编译器会拿构造函数（或自定义推导指南）的**形参模式**去匹配实参类型，逐个把模板参数解出来。
> 关键点：这是**逐参数的"一对一"匹对**，不存在"取共同超类型"这回事——
> `Pair p(10, 20.5)` 推出来的是 `Pair<int, double>`，**不是** `Pair<double, double>`。
> 另外要记住：**CTAD 只发生在类模板的构造/初始化**，而且推导失败时不会自动"退一步"去做类型转换。

### 自定义推导指南

有时候自动推导的结果不是你想要的，这时可以写**自定义推导指南**（Deduction Guide）来"接管"推导过程。

最常见的场景：字符串字面量的类型是 `const char[N]`，直接推导会得到一个存 `const char*` 的对象，而你想要的是 `std::string`：

```cpp
#include <iostream>
#include <string>
#include <type_traits>

template<typename T>
struct Box {
    T value;
    Box(T v) : value(v) {}
};

// 自定义推导指南：遇到字符串字面量时，推导成 Box<std::string>
// 语法：类名(形参列表) -> 你要的实例类型;
Box(const char*) -> Box<std::string>;

int main() {
    Box b1(42);        // 没有匹配的自定义指南，走隐式指南 → Box<int>
    Box b2("hello");   // 命中自定义指南            → Box<std::string>

    static_assert(std::is_same_v<decltype(b2), Box<std::string>>);

    std::cout << "b1 = " << b1.value << std::endl;          // 输出: b1 = 42
    std::cout << "b2 = " << b2.value << std::endl;          // 输出: b2 = hello
    std::cout << "b2.value.size() = " << b2.value.size() << std::endl;  // 输出: b2.value.size() = 5

    // 如果没有那条指南，b2 会是 Box<const char*>，
    // 下面这行就会编译失败（Box<const char*> 里没有 size()）：
    // std::cout << b2.value.size() << std::endl;

    return 0;
}
```

输出：
```text
b1 = 42
b2 = hello
b2.value.size() = 5
```

> ⚠️ **一个常见的误解**：很多人以为"用了 `std::initializer_list` 构造函数就一定要写推导指南"。
> 其实不用——编译器会从构造函数自动生成隐式指南，比如对一个
> `Container(std::initializer_list<T>)` 构造函数，`Container c = {1, 2, 3};` 本来就能推出 `Container<int>`。
> 自定义指南是为了**改变**推导结果（比如把 `const char*` 变成 `std::string`），不是为了"让它能编过"。

## 17.8 概念和变量模板的模板参数（C++26）

### 概念作为模板参数

C++26 正式采纳了一项提案（P2841R7《Concept and variable-template template-parameters》），让**概念本身可以当作模板参数**传进来——这在以前是做不到的，你只能传一个"类模板"（模板模板参数），不能传一个"约束"。

```cpp
// 📎 可用性说明：Apple clang 21 的 libc++/clang 尚未实现这个语法。
//    下面保留标准写法，供理解用途。

// 以前只能传"类模板"：
template<template<typename> class Container>
struct Old { /* ... */ };

// C++26 起可以传"概念"：
template<template<typename> concept C, typename T>
    requires C<T>
struct Wrapper {
    T value;
};

// 使用：第一个实参是一个"概念"的名字，而不是类模板的名字
Wrapper<std::integral, int> w{42};   // ✅
// Wrapper<std::integral, double> w2; // ❌ double 不满足 integral
```

> 📎 **可用性说明**：这项特性（P2841R7）由 GCC 16 / 更新的编译器逐步实现，**Apple clang 21 还不支持**，写 `template<template<typename> concept C>` 会报
> `error: template template parameter requires 'class' or 'typename' after the parameter list`。
> 上面用 `text` 代码块展示写法，请勿直接当作可编译代码。
>
> 💡 **什么时候有用**：当你写的类模板需要"接受一个约束、并把它转发给内部类型"时，比如实现自己的容器适配器、序列化框架、或者约束组合器。

### 变量模板

变量模板是 C++14 引入的特性，让你可以定义**编译期的常量**：

```cpp
#include <iostream>
#include <cstddef>
#include <type_traits>

// 自己写一个变量模板（注意：别起名成 is_pointer_v，那会和 std::is_pointer_v 撞脸）
template<typename T>
inline constexpr bool my_is_pointer_v = std::is_pointer_v<T>;

template<typename T>
inline constexpr std::size_t type_size = sizeof(T);

int main() {
    std::cout << std::boolalpha;  // 打印 true/false 而不是 1/0
    std::cout << "my_is_pointer_v<int>: " << my_is_pointer_v<int> << std::endl;   // false
    std::cout << "my_is_pointer_v<int*>: " << my_is_pointer_v<int*> << std::endl; // true

    std::cout << "type_size<char>: " << type_size<char> << std::endl;  // 1
    // LP64 平台（macOS / Linux 64 位）上 long 是 8 字节；Windows 上是 4 字节
    std::cout << "type_size<long>: " << type_size<long> << std::endl;  // macOS: 8

    return 0;
}
```

> ⚡ **变量模板的用途**：
> - 标准库的 `std::is_integral_v<T>` 是 `std::is_integral<T>::value` 的简写（少了 `::value` 的烦恼）
>   注意：**变量模板这个语言特性是 C++14**，但标准库里那一大批 `_v` 后缀（`is_integral_v`、`is_pointer_v`…）
>   是 **C++17** 才补上的。在 C++14 里你只能用自己写的变量模板。
> - 提供编译期类型信息查询
> - 替代宏定义的编译期常量（比 `#define` 安全一万倍）

## 本章小结

本章我们深入探索了 C++ 类模板的精彩世界，以下是核心知识点回顾：

### 📌 类模板基础
- **类模板定义**：使用 `template<typename T>` 声明类型参数
- **实例化**：编译器根据具体类型生成对应的类代码
- **应用场景**：数据结构（Stack、Queue）、智能指针、容器等

### 📌 成员函数与特化
- **模板成员函数**：在类外定义时需要双层 `template` 声明
- **全特化**：`template<>` 为特定类型提供完整特殊实现
- **偏特化**：为部分类型参数提供特殊实现

### 📌 模板模板参数
- **定义**：让"模板参数本身也是一个模板"，例如 `template<typename T, template<typename> class Container>`
- **语法**：`template<typename T, template<typename> class Container>`；需要更保险时写 `template<typename, typename...> class`
- **注意**：C++17 起（P0522R0）带默认参数的容器模板（如 `std::vector`）可以直接匹配 `template<typename> class`
- **关键结论**：模板模板参数只检查"形状"，容器有没有某个成员函数要等真正调用时才会报错

### 📌 SFINAE 与类型萃取
- **SFINAE**：模板替换失败不算错误，编译器自动选择其他重载
- **enable_if**：控制函数是否参与重载决议
- **type_traits**：编译期类型查询（is_integral、is_floating_point 等）
- **if constexpr**：C++17 引入的编译期分支选择

### 📌 概念与约束（C++20）
- **概念**：对模板参数的类型约束，明码标价
- **requires 子句**：将概念应用于模板参数
- **标准概念库**：`std::integral`、`std::floating_point`、`std::movable` 等

### 📌 CTAD（C++17）
- **类模板参数推导**：编译器自动推断模板参数类型
- **推导指南**：自定义推导规则

### 📌 展望 C++26
- **概念作为模板参数**：C++26 正式采纳（P2841R7），可以写 `template<template<typename> concept C, typename T>`（Apple clang 21 尚未实现）
- **变量模板**：C++14 引入的编译期常量定义；标准库里成批的 `_v` 后缀是 C++17 才补上的

> 🎯 **学习建议**：模板是 C++ 最强大的特性之一，也是最难掌握的部分。建议多动手实践，从简单的 Stack 类开始，逐步实现更复杂的模板元编程技巧。记住，编译器是最好的老师——遇到错误时，仔细阅读错误信息，它会告诉你哪里出了问题！

---

*"在 C++ 中，只有两种语言：一种是让人骂娘的语言，另一种是没人用的语言。"* —— 类模板属于前者，但相信我，它是值得的！ 😄
