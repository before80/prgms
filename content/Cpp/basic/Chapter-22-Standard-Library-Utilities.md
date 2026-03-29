+++
title = "第22章 标准库工具类"
weight = 220
date = "2026-03-29T21:03:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++
# 第22章 标准库工具类

想象一下，你走进一家超市，发现购物车只能装一样东西——要么是苹果，要么是橘子，但不能同时装两种。这也太反人类了吧！C++的标准库工具类就是来拯救你的，它们让你的"购物车"能装下各种奇奇怪怪的东西，而且井井有条。

本章我们将探索一系列"收纳神器"：`std::pair`、`std::tuple`让你打包出售两个或多个对象；`std::optional`表示"可能有也可能没有"的薛定谔的值；`std::variant`让你在一个变量里装下多种人格；`std::any`则是个什么都能装的万能口袋……哦对了，还有时间管理大师`std::chrono`。准备好了吗？让我们一起进入C++的收纳哲学！

## 22.1 std::pair

`std::pair`是C++标准库中最简单的"容器"——它只能装**两个**东西，而且这两个东西可以是完全不同的类型。比如一个`int`和一个`string`，或者一个`double`和一个自定义类。pair就像是你去民政局领的那个红本本——一男一女（或者任意两性别的组合），一辈子绑定在一起，不离不弃。

```cpp
#include <iostream>
#include <utility>

int main() {
    // std::pair：存储两个异构对象的容器
    // 想象一下：这就像是一张火车票——座位号和乘客名
    std::pair<int, std::string> p1(1, "one");  // 传统写法
    std::pair p2{2, "two"};  // C++17 CTAD，编译器自动推断类型，偷懒神器！

    std::cout << "p1: (" << p1.first << ", " << p1.second << ")" << std::endl;
    // 输出: p1: (1, one)

    // 比较操作——字典序比较，先比first，再比second
    // 就像按姓氏排序电话本，先看姓再看名
    std::pair<int, int> a(1, 2);
    std::pair<int, int> b(1, 3);

    std::cout << "(1,2) < (1,3): " << (a < b) << std::endl;  // 输出: 1 (true)
    // 因为first相等(1==1)，所以比较second，2 < 3，所以a < b

    // make_pair便捷函数——不用写类型，编译器帮你猜
    auto p3 = std::make_pair(3, "three");

    // 结构化绑定（C++17）——这是史诗级特性！
    // 想象一下拆快递：不用先打开再看里面是什么，直接一次性拆开验货
    auto [num, str] = p1;
    std::cout << "num=" << num << ", str=" << str << std::endl;  // 输出: num=1, str=one

    return 0;
}
```

> **💡 小知识**：pair的比较是字典序的，就像英语词典排序单词一样。先比较第一元素，如果相等才比较第二元素。`std::pair`常用于`std::map`的键值对，想象一下字典里每个词条就是pair——单词是first，解释是second。

## 22.2 std::tuple（C++11）

如果说`std::pair`是一对情侣，那`std::tuple`就是一个课题组——可以容纳**任意多个**成员，而且每个成员可以是不同类型。tuple在C++11引入，终于让你不用为了返回多个值而绞尽脑汁地发明各种"结构体炸弹"。

### tuple的使用场景

tuple就像是个**临时拼凑小分队**，适合那些"我就用一次，不需要专门定义一个结构体"的场景。比如你要返回一个函数的多个结果，或者把一堆乱七八糟的数据打包传递。

```cpp
#include <iostream>
#include <tuple>
#include <string>

int main() {
    // std::tuple：存储多个异构对象的容器
    // 想象一下：tuple就像是一个多功能的工具箱，里面可以有锤子、螺丝刀、香蕉
    std::tuple<int, double, std::string, char> t(1, 3.14, "hello", 'c');

    // 访问元素——必须用编译时索引，像是在问"第0个抽屉里是什么？"
    std::cout << "get<0>: " << std::get<0>(t) << std::endl;  // 输出: 1
    std::cout << "get<2>: " << std::get<2>(t) << std::endl;  // 输出: hello
    // 注意：get的模板参数必须是常量表达式，get<变量>是不行的！

    // 结构化绑定（C++17）——拆快递神器升级版！
    auto [i, d, s, c] = t;  // i=1, d=3.14, s="hello", c='c'
    std::cout << "i=" << i << ", d=" << d << ", s=" << s << std::endl;
    // 输出: i=1, d=3.14, s=hello

    // 比较（字典序）——和pair一样的比较规则
    std::tuple<int, int> t1(1, 2);
    std::tuple<int, int> t2(1, 3);
    std::cout << "(1,2) < (1,3): " << (t1 < t2) << std::endl;  // 输出: 1
    // t1和t2的first都是1，相等；然后比较second，2 < 3

    // 链接两个tuple——把两个tuple焊接在一起！
    auto t3 = std::tuple_cat(t1, std::make_tuple(3));
    // t3现在有3个元素：(1, 2, 3)
    std::cout << "Concatenated tuple size: " << std::tuple_size<decltype(t3)>::value << std::endl;
    // 输出: Concatenated tuple size: 3

    return 0;
}
```

### 与struct的选择

这是一个哲学问题！tuple和struct就像**外卖盒**和**家用餐具**的区别。

```cpp
#include <iostream>
#include <tuple>

// 选择tuple的场景：
// - 快速原型，不需要命名（"我只是想临时打包几个值，别让我取名字！"）
// - 返回多个值（函数返回值不够用？tuple来凑！）
// - 作为map的键（需要异构键的时候）
// - 泛型代码（模板元编程里tuple是常客）

// 选择struct的场景：
// - 需要清晰的语义命名（Point3D比tuple<double,double,double>好理解一万倍）
// - 需要文档说明（成员变量名就是最好的注释）
// - 代码可读性更重要（团队合作时struct更友好）
// - 需要稳定ABI（struct的内存布局是确定的，tuple可不一定）
// - 需要成员函数（struct可以有方法！）

struct Point3D {
    double x, y, z;  // 这三个字母胜过千言万语
};

int main() {
    // tuple适合快速返回多个值——就像点外卖不需要知道厨房怎么运作
    std::tuple<int, int, int> getRGB() {
        return {255, 128, 64};  // 橙色的RGB值
    }

    auto [r, g, b] = getRGB();  // 结构化绑定直接拆包
    std::cout << "RGB: " << r << "," << g << "," << b << std::endl;
    // 输出: RGB: 255,128,64

    // struct适合需要清晰命名的情况——就像家里的调料盒
    Point3D p{1.0, 2.0, 3.0};
    std::cout << "Point: (" << p.x << "," << p.y << "," << p.z << ")" << std::endl;
    // 输出: Point: (1,2,3)

    return 0;
}
```

> **💡 经验法则**：问自己一个问题——"三个月后我能看懂这段代码吗？"如果不能，就用struct。tuple是给那些"用完就扔"的临时数据准备的。

## 22.3 std::optional（C++17）

你有没有遇到过这种情况——你去问服务员"你们这有WiFi吗？"，服务员说"可能有吧，我也不太确定"？`std::optional`就是编程世界里的"可能有，可能没有"。

`std::optional<T>`表示一个**可能存在，也可能不存在**的值。它是C++17引入的，解决了多年来"用什么表示'没有值'"的难题。以前你可能用过-1、0、NULL、特殊的异常……现在，统一用`std::nullopt`表示"没有值"。

### 空值检查

optional就像是**薛定谔的盒子**——在打开（检查）之前，你不知道里面有没有值。

```cpp
#include <iostream>
#include <optional>
#include <string>

// 在字符串中查找字符，返回索引（如果找到）或空optional
std::optional<int> findIndex(const std::string& str, char target) {
    for (int i = 0; i < static_cast<int>(str.size()); ++i) {
        if (str[i] == target) {
            return i;  // 隐式构造optional，相当于 std::optional<int>(i)
        }
    }
    return std::nullopt;  // 明确表示"没有值"
}

int main() {
    // std::optional：表示"可能有值"的类型
    // 替代方案们：返回特殊值（-1表示没找到）、返回指针、抛出异常
    // optional比这些方案都更语义化——代码读起来就知道"可能有，可能没有"

    auto index = findIndex("hello", 'l');  // 'l'在索引2和3的位置，但只返回第一个

    // 方法1：has_value() + value()
    if (index.has_value()) {
        std::cout << "Found at index: " << index.value() << std::endl;
        // 输出: Found at index: 2
    } else {
        std::cout << "Not found" << std::endl;
    }

    // 方法2：value_or()——如果有值就用，没有就给默认值
    // 这就像是"如果冰箱里有啤酒就喝啤酒，否则喝可乐"
    int result = index.value_or(-1);
    std::cout << "Result with default: " << result << std::endl;  // 输出: 2

    // 找不存在的字符
    auto notFound = findIndex("hello", 'z');
    std::cout << "Not found value_or: " << notFound.value_or(-1) << std::endl;
    // 输出: -1（因为没找到，所以用默认值-1）

    // 方法3：直接当bool用——这是最简洁的写法
    if (auto idx = findIndex("world", 'o')) {  // 'o'在索引1
        std::cout << "Found 'o' at " << *idx << std::endl;  // 输出: Found 'o' at 1
    }

    return 0;
}
```

### 单态操作（C++23）

C++23给optional配备了一系列**链式操作**（monadic operations），让你可以像搭积木一样连续转换optional的值，而不需要一堆if语句。

```cpp
#include <iostream>
#include <optional>

int main() {
    // C++23: optional的单态操作（monadic operations）
    // 想象一下：这些操作就像是optional的"变形金刚"，可以连续变身

    std::cout << "C++23 optional monadic operations:" << std::endl;

    std::optional<int> opt = 42;

    // map: 转换值——如果有值，就对它进行转换
    // opt.map([](int x) { return x * 2; });  // 返回 optional<int>，值为84

    // transform: 类似map但更灵活
    // std::transform(opt, [](int x) { return x * 2; });

    // and_then: 链式操作——如果都有值，就继续执行
    // opt.and_then([](int x) { return std::optional<int>(x * 2); });

    // or_else: 提供默认值——如果没有值，执行这个 lambda
    // opt.or_else([] { return std::optional<int>(0); });

    std::cout << "std::optional has map/and_then/transform/or_else in C++23" << std::endl;

    return 0;
}
```

### 与指针的选择

什么时候用`std::optional<T>`，什么时候用指针`T*`？这是一个好问题！

```cpp
#include <iostream>
#include <optional>

// optional vs 指针的选择：
// ┌─────────────────┬────────────────────────┐
//│    optional     │         指针            │
// ├─────────────────┼────────────────────────┤
//│ 值语义，不涉及   │ 指向外部对象，可能被    │
//│ 所有权问题       │ 别人修改或释放           │
//│ 语义更清晰：     │ 语义模糊：              │
//│ "可能有值"       │ "可能指向某物"或"没有   │
//│                 │ 指向"                   │
//│ 适合返回值       │ 适合输入参数（out参数）  │
//│ 不能重新绑定     │ 可以重新指向别的对象     │
//└─────────────────┴────────────────────────┘

// 解析字符串为整数——成功返回数字，失败返回空optional
std::optional<int> parseInt(const std::string& s) {
    try {
        return std::stoi(s);  // 成功，包装成optional
    } catch (...) {
        return std::nullopt;  // 失败，返回空
    }
}

int main() {
    auto val = parseInt("123");
    if (val) {
        std::cout << "Parsed: " << *val << std::endl;  // 输出: Parsed: 123
    }

    auto invalid = parseInt("not a number");
    if (!invalid) {
        std::cout << "Failed to parse" << std::endl;  // 输出: Failed to parse
    }

    return 0;
}
```

> **💡 实战建议**：如果函数要返回"可能有，可能没有"的值，优先选择`std::optional`。如果你要传递一个"可能不存在的对象"，用optional；如果你要传递一个"可能修改的外部对象"，用指针。

## 22.4 std::variant（C++17）

想象一下一个人有多重人格——在同一时间，他只能是其中一个人格，但你可以问他"你现在是谁？"`std::variant`就是这么一种类型安全的人格分裂症患者。

`std::variant`是**类型安全的联合体**（union）。在C语言里，union可以存任何类型，但你不知道当前存的是什么——全靠程序员自己记着。C++的variant帮你记住了，而且如果你的访问方式不对，它会**明确地告诉你错了**（抛异常）。

### 访问者模式

variant最酷的功能是可以使用**访问者模式**（visitor pattern）——定义一个"访问者"来处理每种可能的情况。

```cpp
#include <iostream>
#include <variant>
#include <string>

int main() {
    // std::variant：类型安全的联合体
    // 想象一下：这就像是一个神奇的盒子，可以装任何东西，但同一时间只能装一种
    // 而且每次打开盒子，盒子都会告诉你里面装的是什么

    std::variant<int, double, std::string> v;  // 可以是int、double或string

    v = 42;  // 现在装的是int
    std::cout << "int variant: " << std::get<int>(v) << std::endl;  // 输出: 42

    v = 3.14;  // 现在装的是double
    std::cout << "double variant: " << std::get<double>(v) << std::endl;  // 输出: 3.14

    v = "hello";  // 现在装的是string
    std::cout << "string variant: " << std::get<std::string>(v) << std::endl;  // 输出: hello

    // 检查当前类型——就像问"你现在是人格几？"
    if (std::holds_alternative<std::string>(v)) {
        std::cout << "Variant holds a string" << std::endl;
        // 输出: Variant holds a string
    }

    // 尝试安全获取——如果类型不对，返回nullptr而不是抛异常
    if (auto* str = std::get_if<std::string>(&v)) {
        std::cout << "Got string: " << *str << std::endl;
        // 输出: Got string: hello
    }

    return 0;
}
```

### std::get与std::get_if

variant提供了两种访问方式——**直接访问**和**安全访问**，就像保险箱的两种打开方式。

```cpp
#include <iostream>
#include <variant>

int main() {
    std::variant<int, double, char> v = 100;  // 当前类型是int，值是100

    // std::get: 直接访问——如果类型对，拿值；如果类型错，抛异常
    // 就像用钥匙开门，错了就报警
    try {
        int val = std::get<int>(v);
        std::cout << "std::get<int>: " << val << std::endl;  // 输出: 100

        // 如果你想看double？门都没有！
        // std::get<double>(v);  // 抛 std::bad_variant_access 异常！
    } catch (const std::bad_variant_access& e) {
        std::cout << "Wrong type! Variant doesn't hold a double." << std::endl;
    }

    // std::get_if: 安全访问——如果类型对，返回指针；如果类型错，返回nullptr
    // 就像门禁卡，不对就安静地告诉你"没权限"
    if (auto* ptr = std::get_if<int>(&v)) {
        std::cout << "std::get_if<int>: " << *ptr << std::endl;  // 输出: 100
    }

    // 尝试获取double类型——返回nullptr
    if (auto* ptr = std::get_if<double>(&v)) {
        std::cout << "Should not reach here" << std::endl;
    } else {
        std::cout << "std::get_if<double>: nullptr (wrong type)" << std::endl;
        // 输出: std::get_if<double>: nullptr (wrong type)
    }

    return 0;
}
```

> **💡 选择建议**：如果你确定variant里是什么类型，用`std::get`（配合try-catch或`std::holds_alternative`检查）。如果你不确定，用`std::get_if`（更安全，返回nullptr）。

## 22.5 std::any（C++17）

如果说variant是"有限多重人格"，那`std::any`就是**无限可能**——它可以存储任何类型，就像一个真正的大胃王，什么都能吃。

`std::any`使用**类型擦除**（type erasure）技术，把各种类型都转成统一的"any"形态存储，提取时再变回来。这就像是把各种食材都打成浆放进冰箱，拿出来的时候再想办法还原——虽然麻烦，但确实什么都能装。

### 类型擦除

类型擦除听起来很玄乎，其实就像是**给东西拍X光片**——不管你原来是什么，X光片只看得到骨骼轮廓。any也是这样，不管你存的是int、string还是自定义类，any只记录"这里有个东西"和"它原来是什么类型"。

```cpp
#include <iostream>
#include <any>
#include <string>

int main() {
    // std::any：类型擦除的容器，可以存储任意类型
    // 就像一个神奇的垃圾桶，什么都能扔进去，但取出来时得知道原来是什么

    std::any a = 42;              // 扔进去一个int
    std::any b = 3.14;            // 扔进去一个double
    std::any c = std::string("hello");  // 扔进去一个string

    // std::any_cast 提取值——必须知道原来是什么类型！
    // 方式1：指针版本，类型错了返回nullptr
    int* intPtr = std::any_cast<int>(&a);
    if (intPtr) {
        std::cout << "any_cast<int>: " << *intPtr << std::endl;  // 输出: 42
    }

    // 方式2：值版本，类型错了抛 std::bad_any_cast 异常
    int val = std::any_cast<int>(a);
    std::cout << "any_cast<int>(a): " << val << std::endl;  // 输出: 42

    // 如果你记错了类型……那就尴尬了
    try {
        double d = std::any_cast<double>(a);  // a实际上是int，抛异常！
    } catch (const std::bad_any_cast& e) {
        std::cout << "bad_any_cast caught! You lied about the type." << std::endl;
    }

    // 检查有没有值
    std::any empty;
    std::cout << "empty.has_value(): " << empty.has_value() << std::endl;  // 输出: 0

    // reset——扔掉里面的东西
    a.reset();
    std::cout << "After reset, a.has_value(): " << a.has_value() << std::endl;  // 输出: 0

    return 0;
}
```

### 性能考虑

any虽好，但**不是所有场景都适合用它**。它就像是一个功能强大的万能工具，但有时候杀鸡焉用牛刀。

```cpp
#include <iostream>
#include <any>
#include <chrono>

int main() {
    // std::any的性能考虑：
    // ┌──────────────────────────────────────────────────────────────┐
    //│                      any 的 缺 点                              │
    // ├──────────────────────────────────────────────────────────────┤
    //│ 1. 堆分配：如果存的东西比较大（比如大字符串、vector），          │
    //│    需要在堆上分配内存，小东西可能有 SSO（短字符串优化）         │
    //│                                                              │
    //│ 2. 类型信息存储：any要记录"你原来是什么类型"，有额外开销        │
    //│                                                              │
    //│ 3. 类型检查：any_cast时要做运行时类型检查，比静态类型转换慢       │
    //│                                                              │
    //│ 4. 无法内联：因为类型擦除，编译器很难内联优化                   │
    //└──────────────────────────────────────────────────────────────┘

    std::cout << "std::any performance considerations:" << std::endl;
    std::cout << "- Small Object Optimization: typically small objects stored inline" << std::endl;
    std::cout << "- Type erasure overhead" << std::endl;
    std::cout << "- Runtime type checking" << std::endl;
    std::cout << "- Hard to optimize (no static type info)" << std::endl;

    // 什么时候用 any vs variant？
    // - 已知所有可能的类型 → 用 variant（类型安全+无额外开销）
    // - 类型完全未知/动态 → 用 any（灵活性至上）
    // - 已知类型，但很多/不想用模板 → 用 any

    return 0;
}
```

> **💡 性能优化建议**：能用`std::variant`就别用`std::any`，因为variant是静态类型的，编译器可以更好地优化。any是真正的动态类型，适合"类型完全未知"的场景（比如脚本引擎、序列化框架等）。

## 22.6 std::expected（C++23）

终于！C++23给我们带来了`std::expected`——这是一个专门用来处理**错误**的工具。

你有没有遇到过这种代码？

```cpp
std::optional<int> parseNumber(const std::string& s) {
    try {
        return std::stoi(s);
    } catch (...) {
        return std::nullopt;  // 失败了就返回"什么都没有"
    }
}
```

问题在于：`std::nullopt`只告诉你"失败了"，但不告诉你**为什么失败**！比如用户输入了"abc"，你只知道"解析失败"，但不知道具体原因。

`std::expected<T, E>`就是来解决这个问题的——它要么包含一个**正确的值**（T），要么包含一个**错误原因**（E）。就像你去银行办事：要么你拿到钱（成功），要么你拿到一张错误单据上面写着失败原因（失败+原因）。

### 错误处理

```cpp
#include <iostream>
#include <expected>
#include <string>

// C++23: std::expected 表示"可能成功返回某值，或失败返回错误"
// 模板参数：第一个是成功值的类型，第二个是错误类型
// std::expected<int, std::string> 表示：成功返回int，失败返回string错误信息

std::expected<int, std::string> parseNumber(const std::string& s) {
    try {
        return std::stoi(s);  // 成功，返回值
    } catch (...) {
        // 失败，返回错误原因
        return std::unexpected("Failed to parse: " + s);
    }
}

int main() {
    // 成功的例子
    auto result1 = parseNumber("42");
    if (result1) {  // expected可以当bool用
        std::cout << "Parsed: " << result1.value() << std::endl;
        // 输出: Parsed: 42
    }

    // 失败的例子
    auto result2 = parseNumber("not a number");
    if (!result2) {
        std::cout << "Error: " << result2.error() << std::endl;
        // 输出: Error: Failed to parse: not a number
    }

    // value_or的替代方案——用value_or提供默认值
    int withDefault = result2.value_or(0);
    std::cout << "With default: " << withDefault << std::endl;
    // 输出: With default: 0

    return 0;
}
```

### 单态操作（C++23）

和`std::optional`一样，`std::expected`也有单态操作，让你可以链式处理错误。

```cpp
#include <iostream>
#include <expected>

int main() {
    // C++23: expected的单态操作
    // 和optional一样的链式操作能力，但专门为错误处理设计

    std::cout << "C++23 expected monadic operations:" << std::endl;
    std::cout << "- and_then: 链式操作，成功就继续，失败就传递错误" << std::endl;
    std::cout << "- map: 转换值，成功时对值做转换" << std::endl;
    std::cout << "- transform: 类似map但更灵活" << std::endl;
    std::cout << "- or_else: 失败时提供替代的expected" << std::endl;

    // 使用场景示例：
    // auto result = parseNumber("42")
    //     .and_then([](int n) { return validate(n); })
    //     .map([](int n) { return n * 2; });

    return 0;
}
```

> **💡 expected vs optional**：如果失败只需要知道"有没有"，用optional；如果失败需要知道"为什么"，用expected。就像问"你吃了吗？"回答"没吃"vs回答"没吃，因为我在减肥"。

## 22.7 std::bitset与位操作（C++20）

`std::bitset`是C++的**位图大师**——它让你以极其节省空间的方式操作位序列。想象一下，你要在内存中存储一亿个布尔值，用`bool`需要1亿字节，但用`bitset`只需要1250万字节——**省8倍内存**！

```cpp
#include <iostream>
#include <bitset>

int main() {
    // std::bitset：固定大小的位序列
    // 模板参数是位数，一旦定义就不能改变（和array一样）
    // 适合做标志位、掩码、集合等

    std::bitset<8> bits(0b10110011);  // 8位，初始值二进制10110011

    std::cout << "bits: " << bits << std::endl;  // 输出: 10110011

    // 位运算——和整数位运算一样，但结果是bitset
    std::cout << "bits << 2: " << (bits << 2) << std::endl;  // 输出: 11001100
    std::cout << "bits | 0b00001111: " << (bits | 0b00001111) << std::endl;
    // 输出: 10111111

    // 测试和设置位
    std::cout << "bits[0]: " << bits[0] << std::endl;  // 输出: 1（最后一位）
    std::cout << "bits.test(1): " << bits.test(1) << std::endl;  // 输出: 1（第二位）
    std::cout << "bits.all(): " << bits.all() << std::endl;  // 输出: 0（不是全1）
    std::cout << "bits.any(): " << bits.any() << std::endl;  // 输出: 1（有1存在）

    // 设置和翻转
    bits.set(0, 0);  // 设置第0位为0
    bits.flip();     // 所有位取反
    std::cout << "After set(0,0) and flip: " << bits << std::endl;
    // 原来是10110011，set(0,0)后10110010，flip后01001101

    return 0;
}
```

> **💡 常见应用场景**：
> - 权限标志：读、写、执行，用一个bitset就能表示8种权限组合
> - 网络协议：TCP标志位（URG、ACK、PSH、RST、SYN、FIN）
> - 筛法求素数：用bitset做埃拉托斯特尼筛法，内存效率极高

## 22.8 std::byteswap（C++23）

`std::byteswap`是C++23的新玩具，专门用来**交换字节序**。

什么叫字节序？比如你有一个32位整数`0x12345678`，在内存中它的字节是怎么排列的？
- **大端序**（Big Endian）：高位在前，`12 34 56 78`
- **小端序**（Little Endian）：低位在前，`78 56 34 12`

x86架构是小端序，而网络协议通常是大端序。所以当你需要在不同系统间通信时，字节序转换是常事。

```cpp
#include <iostream>
#include <bit>

int main() {
    // C++23: std::byteswap 交换字节序
    // 就像是把乐高块的顺序反过来拼

    unsigned int value = 0x12345678;  // 假设这是小端序
    auto swapped = std::byteswap(value);  // 变成大端序

    std::cout << "Original: 0x" << std::hex << value << std::endl;  // 输出: Original: 0x12345678
    std::cout << "Swapped: 0x" << swapped << std::endl;            // 输出: Swapped: 0x78563412

    // 典型应用：
    // - 网络编程：发送数据前转换字节序
    // - 文件格式：有些文件格式要求特定字节序
    // - 序列化/反序列化：和外部系统交互时

    return 0;
}
```

## 22.9 std::to_underlying（C++23）

`std::to_underlying`是C++23的另一个小工具，专门用来**获取枚举值的底层整数值**。

```cpp
#include <iostream>
#include <type_traits>

// 强类型枚举（enum class）不会隐式转换为int
enum class Color : int { Red = 1, Green = 2, Blue = 3 };

int main() {
    // C++23: std::to_underlying 获取枚举的底层整数值
    // 就像是给强类型枚举"脱马甲"，露出真面目

    Color c = Color::Green;
    int underlying = std::to_underlying(c);  // C++23之前需要 static_cast<int>(c)

    std::cout << "to_underlying(Color::Green) = " << underlying << std::endl;
    // 输出: 2

    return 0;
}
```

> **💡 为什么需要这个？** C++11的`enum class`是强类型枚举，不会隐式转换成int，这本来是好事（防止不小心把枚举当整数用）。但有时候你确实需要获取底层值，以前只能用`static_cast<int>`，现在有了更语义化的`std::to_underlying`。

## 22.10 std::unreachable（C++23）

`std::unreachable`是C++23的**性能优化神器**——它告诉编译器"这行代码永远不会执行到"，让编译器可以做出更激进的优化。

这听起来有点违反直觉——为什么要写一段永远不会执行的代码？主要用在一些**不可能到达的分支**：

```cpp
#include <iostream>
#include <utility>

void switchExample(int value) {
    switch (value) {
        case 1:
            std::cout << "One" << std::endl;
            break;
        case 2:
            std::cout << "Two" << std::endl;
            break;
        default:
            // 如果我们知道value只可能是1或2，那default永远不会到
            // 用 std::unreachable() 告诉编译器这一点
            std::unreachable();  // C++23: 告诉编译器这行不会执行
    }
}

int main() {
    switchExample(1);  // 输出: One

    std::cout << "std::unreachable tells compiler this code is unreachable" << std::endl;

    // 注意：如果误用了 unreachable，比如实际上会执行到那里
    // 行为是未定义的（undefined behavior）！
    // 所以用之前一定要确保真的不会执行到

    return 0;
}
```

> **⚠️ 警告**：调用`std::unreachable()`后如果代码真的执行到了，**行为是未定义的**（UB）。所以用它之前一定要100%确定这个分支不可能到达。常见的用法是`std::unreachable()`前加断言（assert）检查。

## 22.11 std::chrono时间库

`std::chrono`是C++的时间管理大师，帮你处理各种时间相关的计算。它有三个核心概念：

- **时间点**（time point）：表示"某个时刻"，比如"下午3点整"
- **时间段**（duration）：表示"一段时间"，比如"30分钟"
- **时钟**（clock）：提供时间点的方式

chrono的设计非常巧妙——它把时间单位也做成了类型（编译时类型），让你在进行时间计算时不容易出错。

### 时间点与时间段

```cpp
#include <iostream>
#include <chrono>
#include <thread>

int main() {
    using namespace std::chrono;
    using namespace std::chrono_literals;  // 启用时间字面量（1s, 90s, 100ms等）

    // ┌─────────────────────────────────────────────────────────────┐
    //│                    时间段 (duration)                          │
    //│  就像一个苹果，可以是"1个苹果"，也可以是"半个苹果"              │
    //└─────────────────────────────────────────────────────────────┘

    duration<int> seconds(5);                              // 5秒
    duration<double, std::milli> milliseconds(100.5);      // 100.5毫秒

    std::cout << "seconds.count(): " << seconds.count() << std::endl;  // 输出: 5
    std::cout << "milliseconds.count(): " << milliseconds.count() << std::endl;  // 输出: 100.5

    // ┌─────────────────────────────────────────────────────────────┐
    //│                    时间点 (time point)                        │
    //│  就像日历上的一个具体日期                                       │
    //└─────────────────────────────────────────────────────────────┘

    auto now = system_clock::now();  // 获取当前时刻
    auto later = now + 1s;          // 加1秒（C++14的字面量）

    // ┌─────────────────────────────────────────────────────────────┐
    //│                    duration_cast                              │
    //│  转换时间单位，就像换算货币                                      │
    //└─────────────────────────────────────────────────────────────┘

    auto mins = duration_cast<minutes>(90s);  // 把90秒转换成分钟
    std::cout << "90 seconds = " << mins.count() << " minutes" << std::endl;  // 输出: 1

    // ┌─────────────────────────────────────────────────────────────┐
    //│                    时间字面量 (C++14)                          │
    //│  10h, 5min, 3s, 100ms, 50us, 7ns                               │
    //└─────────────────────────────────────────────────────────────┘

    auto delay = 100ms;  // 100毫秒
    std::cout << "delay = " << delay.count() << " ms" << std::endl;  // 输出: 100

    // ┌─────────────────────────────────────────────────────────────┐
    //│                    睡眠                                        │
    //│  让程序"睡一会"，就像你午休一样                                  │
    //└─────────────────────────────────────────────────────────────┘

    std::cout << "Sleeping for 10ms..." << std::endl;
    std::this_thread::sleep_for(10ms);  // 睡眠10毫秒
    std::cout << "Awake!" << std::endl;

    return 0;
}
```

### 时钟类型

C++定义了三种主要时钟，每种都有不同的用途：

```cpp
#include <iostream>
#include <chrono>

int main() {
    using namespace std::chrono;

    // ┌─────────────────────────────────────────────────────────────┐
    //│                system_clock: 系统实时时钟                      │
    //│  用途：获取当前时间，转换成日历时间                              │
    //│  特点：可以回拨（系统时间调整时），不适合测量时间间隔             │
    //└─────────────────────────────────────────────────────────────┘

    auto sys_now = std::chrono::system_clock::now();
    std::time_t sys_time = std::chrono::system_clock::to_time_t(sys_now);
    std::cout << "System time: " << std::ctime(&sys_time) << std::endl;

    // ┌─────────────────────────────────────────────────────────────┐
    //│                steady_clock: 单调时钟                          │
    //│  用途：测量时间间隔                                             │
    //│  特点：时间只往前走，不会回拨，保证测量准确性                    │
    //│  推荐：测量时间间隔时用这个！                                    │
    //└─────────────────────────────────────────────────────────────┘

    auto steady_now = std::chrono::steady_clock::now();

    // ┌─────────────────────────────────────────────────────────────┐
    //│                high_resolution_clock: 高精度时钟              │
    //│  用途：需要最高精度时                                            │
    //│  特点：可能是 system_clock 或 steady_clock 的别名              │
    //│  注意：别依赖它的稳定性，steady_clock更可靠                     │
    //└─────────────────────────────────────────────────────────────┘

    auto hr_now = std::chrono::high_resolution_clock::now();

    // ┌─────────────────────────────────────────────────────────────┐
    //│                实战：测量代码执行时间                          │
    //└─────────────────────────────────────────────────────────────┘

    auto start = steady_clock::now();  // 开始计时

    long long sum = 0;
    for (int i = 0; i < 1000000; ++i) sum += i;  // 干点活

    auto end = steady_clock::now();    // 结束计时
    auto elapsed = duration_cast<microseconds>(end - start);  // 计算差值

    std::cout << "Sum: " << sum << ", Time: " << elapsed.count() << " us" << std::endl;
    // 输出: Sum: 499999500000, Time: xxx us（取决于CPU）

    return 0;
}
```

> **💡 时钟选择指南**：
> - **测量时间间隔** → 用 `steady_clock`（不会因为系统时间调整而受影响）
> - **获取日历时间** → 用 `system_clock`（比如日志时间戳、文件修改时间）
> - **需要高精度** → 可以尝试 `high_resolution_clock`，但要验证它确实是高精度的

## 本章小结

本章我们探索了C++标准库中的一系列"收纳神器"，它们各有所长：

| 工具 | 用途 | 特点 |
|------|------|------|
| `std::pair` | 打包两个异构对象 | 简单直接，map的键值对就是它 |
| `std::tuple` | 打包多个异构对象 | tuple是pair的升级版，适合临时数据打包 |
| `std::optional` | 表示"可能有值" | 优雅处理空值，比返回-1/NULL高级多了 |
| `std::variant` | 类型安全的union | 固定几种类型，类型安全是它的招牌 |
| `std::any` | 什么都能装的万能口袋 | 类型擦除，适合动态类型场景 |
| `std::expected` | 要么返回值，要么返回错误 | 错误处理新范式，比异常更轻量 |
| `std::bitset` | 位操作神器 | 省内存，适合标志位、位图 |
| `std::byteswap` | 字节序转换 | 网络编程、文件格式处理必备 |
| `std::to_underlying` | 获取枚举底层值 | 比static_cast更语义化 |
| `std::unreachable` | 告诉编译器不可能到达 | 性能优化，但用错会UB |
| `std::chrono` | 时间管理大师 | 时间点、时间段、时钟，一应俱全 |

**核心思想**：这些工具类都是为了让你用**更清晰的语义**表达**更复杂的数据结构**。能静态确定的类型就别用动态的，能用编译时检查的就别等到运行时。选择合适的工具，能让你的代码更安全、更易读、更高效。
