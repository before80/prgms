+++
title = "第8章 函数基础"
weight = 80
date = "2026-03-29T21:03:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++
# 第8章 函数基础

想象一下，如果你每天都要亲自去超市买每一颗菜、亲自洗每一颗米、亲自切每一块肉才能做一顿饭——你可能会疯掉。函数（Function）就是编程世界里的"预制菜"：你把一套操作打包好，取个名字，下次想吃的时候直接"加热"就行，不用每次都从头开始折腾。这就是代码复用（Code Reuse）的精髓，也是程序员偷懒（划掉）高效编程的必备技能。

## 8.1 函数的定义与声明

函数就像一个神奇的盒子：你往里面扔点东西（参数），它可能给你返回点东西（返回值），中间的过程你不用操心。编译器需要提前知道这个盒子的存在，这就是**函数声明**（Function Declaration），也叫**函数原型**（Function Prototype）；实际的工作内容在**函数定义**（Function Definition）中完成。

```cpp
#include <iostream>

// 函数声明（函数原型）：告诉编译器这个函数存在
// 格式：返回类型 函数名(参数类型列表);
// 就像超市的价签，先标好价格，顾客才知道这东西卖多少钱
int add(int a, int b);                     // 声明：我要做加法
double divide(double x, double y);         // 声明：我要做除法，小心别除以零
void greet(const std::string& name);       // 声明：我要打招呼，不返回任何东西

// 函数定义：实际实现
int add(int a, int b) {
    return a + b;  // 返回两个整数的和
}

double divide(double x, double y) {
    if (y == 0.0) {
        std::cerr << "Error: division by zero!" << std::endl;  // cerr是错误输出流
        return 0.0;  // 防止灾难性后果，返回一个安全值
    }
    return x / y;
}

void greet(const std::string& name) {
    std::cout << "Hello, " << name << "!" << std::endl;  // void表示"啥都不返回"
}

int main() {
    int sum = add(10, 20);  // 调用函数，就像按下微波炉的启动键
    std::cout << "10 + 20 = " << sum << std::endl;  // 输出: 10 + 20 = 30
    
    double result = divide(10.0, 3.0);
    std::cout << "10.0 / 3.0 = " << result << std::endl;  // 输出: 10.0 / 3.0 = 3.33333
    
    greet("Alice");  // 输出: Hello, Alice!
    
    return 0;  // 程序正常退出的"通关文牒"
}
```

> 小张：为什么C++要区分声明和定义？
> 
> 老王：声明就像你先告诉朋友"我请你吃火锅"，定义是你真的去买了锅底和菜。编译器就像你的钱包——它需要提前知道你要花多少钱（占用多少资源），但实际付钱（分配内存）可以等到真正调用的时候。

## 8.2 函数参数传递方式

函数的参数传递方式就像是送快递的选择：你可以亲自把包裹送到对方手上（值传递）、把包裹的地址写在一张纸上寄过去（指针传递）、或者直接给对方家里的备用钥匙让他们自己拿（引用传递）。每种方式都有自己的用武之地。

### 值传递

**值传递**（Pass by Value）就像复印机：复制一份给你，原件纹丝不动。函数内部操作的是参数的副本，对原始变量毫无影响。

```cpp
#include <iostream>

// 值传递：x是num的副本，修改x不会影响num
void increment(int x) {
    x++;  // 修改的是副本，原变量不变
    std::cout << "Inside increment: x = " << x << std::endl;  // 输出: Inside increment: x = 11
}

int main() {
    int num = 10;
    increment(num);  // num被"复印"了一份传进去
    std::cout << "After increment: num = " << num << std::endl;  // 输出: After increment: num = 10
    
    // 图示：想象一下
    // main:     num ──→ [10]（原始变量）
    // increment: x ──→ [10]（副本，和num长得一样但是独立的）
    // increment内部: x = 11（副本变了）
    // 回到main: num仍然是10（原件纹丝不动）
    
    return 0;
}
```

> 想象你把PPT文件发邮件给同事，你在那份PPT上做修改——同事手里那份会变吗？不会！值传递就是这个道理。

### 指针传递

**指针传递**（Pass by Pointer）就像是把"地址"写在纸上寄给对方。对方拿着地址找上门，才能真正修改原变量。这给了函数"穿越"到原变量所在位置的能力。

```cpp
#include <iostream>

// 指针传递：通过地址间接修改原变量
void incrementPtr(int* ptr) {  // ptr是指向int的指针
    if (ptr) {  // 安全检查：防止传入nullptr（空指针）
        (*ptr)++;  // 解引用：找到ptr指向的内存，把里面的值加1
        std::cout << "Inside incrementPtr: *ptr = " << *ptr << std::endl;  // 输出: Inside incrementPtr: *ptr = 11
    }
}

int main() {
    int num = 10;
    incrementPtr(&num);  // &是取地址符，把num的"家门地址"传过去
    std::cout << "After incrementPtr: num = " << num << std::endl;  // 输出: After incrementPtr: num = 11
    
    // 图示：
    // main:         num ──→ [10]（住在地址0x1000的变量）
    // incrementPtr: ptr ──→ [0x1000]（拿着地址找上门）
    // incrementPtr: *ptr = 11（通过钥匙打开门，把里面的东西改了）
    // 回到main: num变成11（原件被改了！）
    
    incrementPtr(nullptr);  // 安全检查生效，不会崩溃
    
    return 0;
}
```

> 指针传递的"副作用"（Side Effect）：函数居然能修改外面的变量！这是好事也是坏事——好是因为效率高（不用复制大对象），坏是因为可能造成意想不到的bug。

### 引用传递

**引用传递**（Pass by Reference）更像是给变量起了个别名（Alias）。函数内部操作的就是原变量，没有副本，没有解引用，简单粗暴！

```cpp
#include <iostream>

// 引用传递：ref是num的别名，操作ref就是操作num
void incrementRef(int& ref) {  // &表示ref是引用
    ref++;  // 直接操作原变量，不需要解引用
    std::cout << "Inside incrementRef: ref = " << ref << std::endl;  // 输出: Inside incrementRef: ref = 11
}

int main() {
    int num = 10;
    incrementRef(num);  // 直接传变量，不用取地址符
    std::cout << "After incrementRef: num = " << num << std::endl;  // 输出: After incrementRef: num = 11
    
    // 图示：
    // main:          num ──→ [10]（真名）
    // incrementRef: ref ──→ [10]（别名，但指的是同一块内存！）
    // incrementRef: ref = 11（改别名就是改真名）
    // 回到main: num变成11
    
    return 0;
}
```

> 引用vs指针：引用是"跆拳道"——简单直接；指针是"太极拳"——要绕一下但更灵活。现代C++代码中，引用传递是修改参数的首选方式。

### 选择建议

参数传递方式那么多，到底选哪个？别纠结，一张图告诉你：

```cpp
#include <iostream>
#include <vector>
#include <string>

// 选择建议：
// 1. 基本类型（int, double, char等）：值传递即可，开销小得像吃一颗米
void processInt(int x) { /* 放心改，原始变量不受影响 */ }

// 2. 大对象（std::vector, std::string, 自定义大结构体等）：const引用传递
//    避免复制巨大的内存块，省时省空间
void processVector(const std::vector<int>& v) { /* 只读访问，不修改 */ }

// 3. 需要修改的对象：引用传递
//    相当于"出口"，把修改后的结果带出去
void modifyVector(std::vector<int>& v) { v.push_back(42); }

// 4. 指针用于可选参数或C风格API
//    nullptr表示"我不想要这个功能"，像插座不插电
void optionalCallback(void (*callback)(int) = nullptr) {
    if (callback) callback(10);  // 如果提供了回调函数，就调用它
}

int main() {
    int small = 1;
    processInt(small);  // 值传递，small不会被修改
    
    std::vector<int> big(1000000, 1);  // 100万个元素的大对象
    processVector(big);  // 引用传递，避免复制100万个int
    
    modifyVector(big);  // 修改原对象
    
    std::cout << "Vector size after modify: " << big.size() << std::endl;
    // 输出: Vector size after modify: 1000001（多了个42）
    
    return 0;
}
```

> 记忆口诀：**小东西值传递，大东西引用传，只读加const，要改去引用，指针留给C和可选参数**。

## 8.3 函数返回值

函数的返回值就像是餐厅的"取餐号"——你点完菜（调用函数），厨房做好后会给你一个结果（返回值）。C++提供了多种返回值的姿势，让你优雅地处理各种场景。

### 返回类型推导（C++14）

C++14带来了**返回类型推导**（Return Type Deduction），让编译器自动帮你算出函数的返回类型。就像你点菜时说"随便来"，服务员自己决定给你什么。

```cpp
#include <iostream>

// C++14: 返回类型推导
// 编译器会根据return语句自动推断返回类型
// 注意：函数体必须只有一个return语句，或者所有路径都返回相同类型
auto add2(int a, int b) {
    return a + b;  // 编译器推导返回类型为int
}

// C++11就支持的尾随返回类型（Trailing Return Type）
// auto后面跟的是"->"指定的返回类型
auto multiply(double x, double y) -> double {
    return x * y;
}

int main() {
    std::cout << "add2(3, 4) = " << add2(3, 4) << std::endl;  // 输出: add2(3, 4) = 7
    std::cout << "multiply(2.5, 3.0) = " << multiply(2.5, 3.0) << std::endl;  // 输出: multiply(2.5, 3.0) = 7.5
    
    // 注意：不要返回局部变量的引用！
    // auto bad() -> int& {
    //     int x = 10;           // x是局部变量，生于函数，死于函数结束
    //     return x;             // 危险！x在函数结束后被销毁，这是悬空引用（ dangling reference）
    // }
    // 想象你把朋友的电话号码存在便利贴上，结果朋友搬家了，你还拿着便利贴——打电话给谁呢？
    
    return 0;
}
```

> 老程序员忠告：返回引用一时爽，内存销毁火葬场。除非你非常清楚自己在做什么（比如返回静态变量或传入的引用参数），否则老老实实返回值。

### 多返回值技术

有时候一个函数需要返回多个值——比如做除法时既想知道商，又想知道余数，还想知道除数本身。C++提供了三种"多胞胎"返回技术。

```cpp
#include <iostream>
#include <tuple>
#include <utility>

// 方式1：std::pair（两个返回值）
// pair就像一个"二人转"组合，只能装两个元素
std::pair<int, int> minMax(const int a, const int b) {
    return (a < b) ? std::make_pair(a, b) : std::make_pair(b, a);
}

// 方式2：std::tuple（多个返回值）
// tuple是"多胎家庭"，可以装任意多个元素
std::tuple<int, int, int> divMod(int dividend, int divisor) {
    return std::make_tuple(dividend / divisor, dividend % divisor, divisor);
}

// 方式3：结构化绑定作为输出参数（C++17）
// 用引用参数"带回"额外的值
void process(int x, int y, int& out_min, int& out_max) {
    out_min = (x < y) ? x : y;
    out_max = (x > y) ? x : y;
}

int main() {
    // pair用法：C++17的结构化绑定让取出多个值变得优雅
    auto [minVal, maxVal] = minMax(10, 5);  // 像拆快递一样，一个个打开
    std::cout << "min=" << minVal << ", max=" << maxVal << std::endl;  // 输出: min=5, max=10
    
    // tuple用法：返回三个值
    auto [quotient, remainder, divisor] = divMod(17, 5);
    std::cout << "17 / 5 = " << quotient << " remainder " << remainder << std::endl;
    // 输出: 17 / 5 = 3 remainder 2
    
    // 结构化绑定作为输出参数
    int mn, mx;  // 先准备好"空盒子"
    process(100, 50, mn, mx);  // 函数往盒子里塞东西
    std::cout << "process: min=" << mn << ", max=" << mx << std::endl;  // 输出: process: min=50, max=100
    
    // 直接返回tuple
    std::tuple<std::string, int, double> getPerson() {
        return {"Alice", 25, 1.68};  // 返回一个人的信息：名字、年龄、身高（米）
    }
    auto [name, age, height] = getPerson();
    std::cout << name << " is " << age << " years old, " << height << "m tall" << std::endl;
    // 输出: Alice is 25 years old, 1.68m tall
    
    return 0;
}
```

> 面试题：为什么不直接返回数组？
> 
> 因为C++不能返回C风格数组（编译器不知道数组多大），但可以返回std::array或std::vector。另外，用pair/tuple返回多个值比用输出参数更符合直觉。

### 隐式移动简化（C++23）

C++23进一步简化了返回值的移动操作——编译器会自动帮你把局部对象"搬"出去，不用你手动写std::move了。

```cpp
#include <iostream>
#include <vector>
#include <utility>

// 隐式移动：返回值自动优化
std::vector<int> createAndReturn() {
    std::vector<int> v = {1, 2, 3, 4, 5};  // 局部vector
    return v;  // C++17起，编译器自动优化为移动而不是复制
}

// 显式移动：以前的写法
std::vector<int> createAndReturnExplicit() {
    std::vector<int> v = {1, 2, 3, 4, 5};
    return std::move(v);  // C++17之前必须手动move，否则可能触发复制
}

int main() {
    auto v1 = createAndReturn();
    std::cout << "v1 size: " << v1.size() << std::endl;  // 输出: v1 size: 5
    
    auto v2 = createAndReturnExplicit();
    std::cout << "v2 size: " << v2.size() << std::endl;  // 输出: v2 size: 5
    
    // 隐式移动的好处：
    // 1. 代码更简洁，不用到处写std::move
    // 2. 减少人为失误（比如在不该move的地方move了）
    // 3. 性能一样好，编译器会处理
    
    return 0;
}
```

> 移动语义（Move Semantics）就像是搬家公司：你不用把家具拆了再装，而是直接连人带东西一起搬走。隐式移动让这个过程全自动——你只管打包，搬家公司自动处理。

### 返回值优化（RVO/NRVO）

**返回值优化**（Return Value Optimization，RVO）和**命名返回值优化**（Named Return Value Optimization，NRVO）是编译器的高级魔法：直接在调用者的内存中构造返回值，省去复制/移动的开销。

```cpp
#include <iostream>
#include <vector>

// RVO: Return Value Optimization
// 编译器优化：在调用者的内存中直接构造返回值，避免复制和移动

struct BigObject {
    int data[1000];  // 假设这占用4KB内存
    BigObject() {
        std::cout << "Default Constructor called - 分配了4KB内存!" << std::endl;
    }
    BigObject(const BigObject&) {
        std::cout << "Copy Constructor called - 糟糕，要复制4KB！" << std::endl;
    }
    BigObject(BigObject&&) noexcept {
        std::cout << "Move Constructor called - 搬走4KB，稍微快点" << std::endl;
    }
};

// 命名返回值优化（NRVO）
// 函数内有个命名对象，编译器可能直接把它构造到调用者的内存中
BigObject createNRVO() {
    BigObject obj;  // 命名对象
    return obj;     // 编译器可能直接省略复制/移动
}

// 匿名临时对象的RVO
// 返回临时对象时，编译器可以直接在调用者内存构造
BigObject createRVO() {
    return BigObject();  // 匿名临时对象
}

int main() {
    std::cout << "Creating with RVO:" << std::endl;
    BigObject obj1 = createRVO();  // 理想情况：只有构造函数调用
    
    std::cout << "\nCreating with NRVO:" << std::endl;
    BigObject obj2 = createNRVO();  // 理想情况：只有构造函数调用
    
    // C++17强制启用复制消除（Mandatory Copy Elision）
    // 即使构造函数有副作用（如打印日志），在某些情况下也必须消除
    
    return 0;
}
```

> 编译器优化有多强？
> 
> 在启用优化的编译下（-O2或-O3），RVO/NRVO可能完全消除复制操作。想象你网购一件家具，卖家直接在你要收货的地方生产，而不是先在仓库做好再运过来——这就是RVO的原理。

## 8.4 函数重载

**函数重载**（Function Overloading）是C++的多态（Polymorphism）特性之一：同一个名字，不同的参数表，编译器会根据你传入的参数自动选择合适的版本。就像"托尼老师"——他可以是理发师、可以是老师、也可以是你的好基友，取决于你找他干嘛。

### 重载解析规则

函数重载的关键是**参数列表**必须不同——可以是参数个数不同，也可以是参数类型不同。返回类型不算在内！

```cpp
#include <iostream>

// 函数重载：同名函数，参数列表不同
// 编译器根据调用时提供的参数选择最匹配的版本

int add(int a, int b) {  // 处理整数加法
    std::cout << "int version" << std::endl;
    return a + b;
}

double add(double a, double b) {  // 处理浮点数加法
    std::cout << "double version" << std::endl;
    return a + b;
}

std::string add(const std::string& a, const std::string& b) {  // 处理字符串拼接
    std::cout << "string version" << std::endl;
    return a + b;
}

int main() {
    std::cout << add(1, 2) << std::endl;  // 输出: int version\n3
    std::cout << add(1.5, 2.5) << std::endl;  // 输出: double version\n4
    std::cout << add("Hello, ", "World!") << std::endl;  // 输出: string version\nHello, World!
    
    // 注意：返回类型不同不能重载！
    // double add(int a, int b);  // 编译错误！只有返回类型不同，不算重载
    // 编译器会一脸问号：我就想知道你传了什么参数，你怎么光告诉我返回值？
    
    return 0;
}
```

> 编译器选择重载版本的过程就像相亲：
> 
> 1. **精确匹配**：对方要求的条件你完美符合，直接牵手
> 2. **类型提升**：你稍微"升级"了一下（比如int升级为double），勉强接受
> 3. **标准转换**：需要一些"化妆"（如int转double），也可以接受
> 4. **用户自定义转换**：需要"整容"，成功率降低
> 5. **匹配失败**：对不起，我们不合适

### 陷阱与注意事项

函数重载看起来很美好，但有几个坑你需要知道。

```cpp
#include <iostream>

// 陷阱1：const参数的重载
// void print(int x) 和 void print(const int x) 不是重载！
// 因为const修饰参数时，参数本身是局部变量，const对调用者没有意义
void print(int x) {
    std::cout << "non-const: " << x << std::endl;  // 输出: non-const: 10
}

void print(const int x) {  // 这不是重载！编译器会把它当作重复声明
    std::cout << "const: " << x << std::endl;
}

// 正确做法：用指针或引用来区分const
void printPtr(int* x) {  // 指向非const的指针
    std::cout << "int*: " << *x << std::endl;
}

void printPtr(const int* x) {  // 指向const的指针，这才是真正的重载
    std::cout << "const int*: " << *x << std::endl;
}

int main() {
    int a = 10;
    const int b = 20;
    
    print(a);  // 调用non-const版本，输出: non-const: 10
    // print(b);  // 编译错误！两个print函数被编译器认为是同一个
    
    printPtr(&a);  // 调用int*版本，a可以被修改
    printPtr(&b);  // 调用const int*版本，b不能被修改
    
    return 0;
}
```

> 记忆口诀：**值传递的const不算数，指针引用才算数**。

## 8.5 默认参数

**默认参数**（Default Arguments）就像是餐厅的套餐——你可以只点"套餐A"，服务员知道你还要配米饭和饮料；也可以详细说"套餐A，不要辣，多加肉"。省略的参数使用默认值，省时省力。

```cpp
#include <iostream>
#include <string>

// 默认参数：调用时可以省略某些参数，使用默认值
void connect(const std::string& host, int port = 80, bool ssl = false) {
    // 连接主机，端口默认80，ssl默认关闭
    std::cout << "Connecting to " << host << ":" << port;
    if (ssl) std::cout << " (SSL)";
    std::cout << std::endl;
}

// 注意事项：
// 1. 默认参数必须放在参数列表最右边
void example(int a, int b = 10, int c = 20) {}  // OK！默认参数在右边
// void bad(int a = 10, int b, int c = 20) {}   // 错误！b在中间没有默认值
// 想象点菜：服务员问你要不要辣，你说"随便"，然后再问你要不要米饭——这不扯淡吗？

// 2. 默认值只能指定一次（在声明或定义中，不要两处都指定）
void declared(std::string& name);  // 声明：说有这个函数
void defined(std::string& name) {  // 定义：说它具体干嘛，但不重复指定默认值
    std::cout << name << std::endl;
}

int main() {
    connect("example.com");  // 使用所有默认值: example.com:80
    connect("example.com", 443);  // port=443, ssl=false
    connect("example.com", 443, true);  // 全指定
    
    // 对应输出:
    // Connecting to example.com:80
    // Connecting to example.com:443
    // Connecting to example.com:443 (SSL)
    
    std::string name = "Alice";
    defined(name);  // 输出: Alice
    
    return 0;
}
```

### 默认参数陷阱

默认参数和函数重载在一起时，可能产生意想不到的"化学反应"。

```cpp
#include <iostream>

// 陷阱：默认参数与函数重载可能产生歧义
int compute(int x, int y = 10) {  // 可以省略y
    return x + y;
}

int compute(int x) {  // 另一个重载版本
    return x * 2;
}

int main() {
    // compute(5) 会调用哪个？
    // compute(int x, int y=10) 可以通过省略y来匹配
    // compute(int x) 精确匹配
    // 编译器内心OS：精确匹配优先，所以选compute(int x)
    std::cout << compute(5) << std::endl;  // 输出: 10 (5 * 2)，调的是第二个！
    
    // 但如果写成这样：
    // compute(5, 10) -> 第一个（无歧义）
    // compute(5) -> 精确匹配优先，选择compute(int x)，无歧义！
    // 真正的歧义需要更复杂的场景，比如添加另一个接受float的重载
    
    return 0;
}
```

> 最佳实践：当你同时使用默认参数和函数重载时，确保每个重载版本在调用时都能被**唯一**识别。如果有歧义，编译器会报错——虽然报错信息可能让你一头雾水。

## 8.6 内联函数

**内联函数**（Inline Function）就像是给你的代码贴上"请勿打扰，直接插入"的标签。它建议编译器在调用点展开函数体，而不是真正地"调用"。省去了函数调用的开销（跳转、栈操作等），但会增加编译出来的代码体积。这是**空间换时间**的经典案例。

```cpp
#include <iostream>

// 内联函数：建议编译器在调用处展开函数体
// 适用于小而频繁调用的函数，避免函数调用开销
inline int max(int a, int b) {
    return (a > b) ? a : b;  // 小函数，内联收益高
}

// C++17: constexpr隐含inline，所以不用写inline
constexpr int min(int a, int b) {
    return (a < b) ? a : b;
}

int main() {
    int result = max(10, 20);
    std::cout << "max(10, 20) = " << result << std::endl;  // 输出: max(10, 20) = 20
    
    // 编译器可能展开为：int result = (10 > 20) ? 10 : 20;
    // 完全没有函数调用，直接算答案
    
    // 注意：inline只是"建议"，编译器可以选择忽略
    // 对于大函数或递归函数，编译器通常不会内联
    // inline更像是"希望"，而不是"命令"
    
    return 0;
}
```

> 什么时候用内联？
> 
> - 函数体很小（1-3行）
> - 被频繁调用（成千上万次）
> - 不是递归函数
> 
> 什么时候不用？
> - 函数体很大（几十行以上）
> - 递归函数
> - 有复杂控制流（switch、异常等）

## 8.7 constexpr函数（C++11）与consteval（C++20）

**constexpr**是C++11引入的关键字，意思是"常量表达式"。它告诉编译器：这个函数可以在编译期就算出来！如果条件允许，编译器会在编译时就把结果算好，而不是等到程序运行时再算。这就像是提前做好的功课，不用每次考试都重新学一遍。

**consteval**是C++20新增的关键字，比constexpr更"狠"——它**强制**必须在编译期计算，如果做不到就编译错误。

```cpp
#include <iostream>

// constexpr: 可以在编译期计算，也可以在运行期计算
constexpr int square(int x) {
    return x * x;
}

// C++14: constexpr函数可以有更多语句（if、循环等）
constexpr int factorial(int n) {
    if (n <= 1) return 1;
    return n * factorial(n - 1);  // 递归也是可以的
}

// C++17: constexpr lambda
auto constexprAdd = [](auto a, auto b) constexpr { return a + b; };

// C++20: consteval：强制在编译期计算，运行期调用会编译错误
consteval int compileTimeOnly(int x) {
    return x * x;
}

// C++20: constinit确保变量在编译期初始化
// 如果初始化的值不是常量表达式，编译错误
constinit int compileTimeValue = factorial(5);

int main() {
    // 编译期计算：编译器在编译时就算出答案
    constexpr int sq = square(10);  // 在编译时就计算出是100
    std::cout << "square(10) = " << sq << std::endl;  // 输出: square(10) = 100
    
    constexpr int fact = factorial(5);  // 编译期计算：120
    std::cout << "factorial(5) = " << fact << std::endl;  // 输出: factorial(5) = 120
    
    // 运行时计算：constexpr函数也可以在运行时调用
    int runtimeValue = 20;
    int rt = square(runtimeValue);  // 运行时计算
    std::cout << "square(20) = " << rt << std::endl;  // 输出: square(20) = 400
    
    // consteval：必须能在编译期计算
    constexpr int cto = compileTimeOnly(5);  // OK，编译期就算好了
    std::cout << "compileTimeOnly(5) = " << cto << std::endl;  // 输出: compileTimeOnly(5) = 25
    
    // 下面这行如果取消注释，编译会失败：
    // int rt2 = compileTimeOnly(runtimeValue);  // 错误！runtimeValue不是常量
    // consteval函数不接受运行时的参数，必须在编译期就确定
    
    std::cout << "compileTimeValue = " << compileTimeValue << std::endl;  // 输出: compileTimeValue = 120
    
    return 0;
}
```

> constexpr vs consteval 区别：
> 
> - `constexpr int f(int x) { return x * x; }` → 编译期能算就算，算不了就运行期算
> - `consteval int g(int x) { return x * x; }` → 必须编译期算，否则编译错误

## 8.8 函数递归与递归优化

**递归**（Recursion）就是函数调用自己。就像俄罗斯套娃，打开一个里面还有一个，打开一个里面还有一个，直到最小的那个。递归必须有个"终止条件"（Base Case），否则就是无限递归，栈溢出（Stack Overflow）等着你。

```cpp
#include <iostream>

// 递归：函数调用自身
// 计算阶乘：n! = n * (n-1) * (n-2) * ... * 1
unsigned long long factorial(int n) {
    if (n <= 1) return 1;  // 终止条件：1! = 0! = 1
    return n * factorial(n - 1);  // 递归调用：n! = n * (n-1)!
}

// 计算斐波那契数列（朴素递归，但效率低）
// 1, 1, 2, 3, 5, 8, 13, 21...
long long fibonacci(int n) {
    if (n <= 1) return n;  // 终止条件
    return fibonacci(n - 1) + fibonacci(n - 2);  // 递归调用
    // 问题：fib(5) = fib(4) + fib(3) = (fib(3)+fib(2)) + (fib(2)+fib(1))
    // 有大量重复计算，效率很低
}

// 计算斐波那契数列（带记忆化的递归）
// 用数组记住已经算过的值，避免重复计算
long long fibMemo(int n, long long memo[]) {
    if (n <= 1) return n;
    if (memo[n] != 0) return memo[n];  // 已经算过了，直接返回
    memo[n] = fibMemo(n - 1, memo) + fibMemo(n - 2, memo);  // 算完记下来
    return memo[n];
}

int main() {
    std::cout << "factorial(5) = " << factorial(5) << std::endl;  // 输出: factorial(5) = 120
    
    // 递归深度注意：太深会栈溢出
    // factorial(10000) 可能会让你的程序崩溃
    std::cout << "fibonacci(10) = " << fibonacci(10) << std::endl;  // 输出: fibonacci(10) = 55
    
    // 使用记忆化（Memoization）优化：时间复杂度从O(2^n)降到O(n)
    long long memo[100] = {0};  // 初始化为0，表示"还没算过"
    std::cout << "fibMemo(50) = " << fibMemo(50, memo) << std::endl;
    // 输出: fibMemo(50) = 12586269025（巨大的数字）
    
    // 尾递归优化（Tail Recursion Optimization）
    // 普通递归：return f(n-1) + f(n-2)，需要在返回后做加法
    // 尾递归：return tailCall(...)，没有任何后续操作
    // 编译器可以把尾递归优化成循环，避免栈增长
    
    return 0;
}
```

> 递归的栈深度问题：
> 
> 每次递归调用都会在栈上分配新的栈帧（Stack Frame），包含局部变量、返回地址等。如果递归太深（通常几万层以上），栈空间会耗尽，程序崩溃。这就是著名的"Stack Overflow"（栈溢出）——是的，那个程序员问答网站的名字就来源于此。

## 8.9 main函数参数和环境变量

`main`函数是程序的入口点（Entry Point），它可以接受命令行参数。`argc`和`argv`就像是程序的"早餐"：程序名本身算一个参数（argc至少为1），后面的都是你传进去的参数。

```cpp
#include <iostream>
#include <cstdlib>

// argc: argument count，参数个数（包括程序名本身）
// argv: argument vector，参数列表（字符串数组）
int main(int argc, char* argv[]) {
    // argv[0] 是程序名（可执行文件的路径）
    // argv[1] 到 argv[argc-1] 是传入的参数
    // argv[argc] 是 nullptr（哨兵值，表示参数列表结束）
    
    std::cout << "Program name: " << argv[0] << std::endl;
    std::cout << "Number of arguments: " << argc << std::endl;
    
    for (int i = 1; i < argc; ++i) {
        std::cout << "argv[" << i << "] = " << argv[i] << std::endl;
    }
    
    // 获取环境变量（C风格，不推荐）
    // char* env = std::getenv("PATH");
    // if (env) std::cout << "PATH = " << env << std::endl;
    
    // C++11: getenv_s更安全（推荐使用）
    // size_t len;
    // char pathBuf[1000];
    // errno_t err = getenv_s(&len, pathBuf, sizeof(pathBuf), "PATH");
    // if (err == 0) std::cout << "PATH = " << pathBuf << std::endl;
    
    return 0;  // 0表示正常退出，非0表示异常退出
}
```

> 运行示例：
> 
> 假设程序叫`myapp`，在命令行输入：
> ```
> ./myapp hello world 123
> ```
> 
> 输出：
> ```
> Program name: ./myapp
> Number of arguments: 4
> argv[1] = hello
> argv[2] = world
> argv[3] = 123
> ```

## 8.10 Lambda表达式（C++11）

**Lambda表达式**（Lambda Expression）是C++11引入的重磅特性。它让你可以在需要的地方"就地"定义一个函数，而不用费劲去声明、定义、再使用。就像是点外卖——不用自己去菜市场、炒菜、洗碗，一个订单送到嘴边。

### Lambda语法详解

Lambda表达式的基本语法有点像是写一封密信：

```cpp
#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    // Lambda表达式基础语法：
    // [capture list] (parameters) -> return_type { body }
    //    ↑          ↑          ↑            ↑
    //  捕获列表    参数列表   返回类型     函数体
    //  哪些外部变量  接受什么参数  返回什么  具体干什么
    
    // 最简lambda：没有捕获，没有参数
    auto hello = []() { std::cout << "Hello, Lambda!" << std::endl; };
    hello();  // 输出: Hello, Lambda!
    
    // 带参数
    auto add = [](int a, int b) { return a + b; };
    std::cout << "add(3, 4) = " << add(3, 4) << std::endl;  // 输出: add(3, 4) = 7
    
    // 省略返回类型：编译器自动推导（基于return语句）
    auto multiply = [](int a, int b) { return a * b; };  // 推导为int
    std::cout << "multiply(5, 6) = " << multiply(5, 6) << std::endl;  // 输出: multiply(5, 6) = 30
    
    // 显式返回类型：当return语句不明确时需要指定
    auto divide = [](double a, double b) -> double {
        if (b == 0) return 0.0;
        return a / b;
    };
    std::cout << "divide(10.0, 3.0) = " << divide(10.0, 3.0) << std::endl;
    // 输出: divide(10.0, 3.0) = 3.33333
    
    return 0;
}
```

### 捕获列表

Lambda表达式可以"捕获"外部变量，就像给你一把打开外部保险箱的钥匙。捕获方式有很多种：

```cpp
#include <iostream>

int main() {
    int x = 10;
    double y = 3.14;
    
    // 捕获列表用于访问外部变量
    // []          - 不捕获任何变量（最安全，但最没用）
    // [x]         - 按值捕获x（拿到的是副本）
    // [&x]        - 按引用捕获x（拿到的是地址，修改会影响原变量）
    // [=]         - 按值捕获所有外部变量（自动帮你写）
    // [&]         - 按引用捕获所有外部变量（自动帮你写）
    // [=, &x]     - 按值捕获所有，但x按引用
    // [&, x]      - 按引用捕获所有，但x按值
    // [x = expr]  - 初始化捕获（C++14），捕获表达式计算结果
    
    // 按值捕获
    auto lambda1 = [x](int a) { return a + x; };
    std::cout << "lambda1(5) = " << lambda1(5) << std::endl;  // 输出: lambda1(5) = 15
    
    // 按引用捕获
    auto lambda2 = [&x](int a) {
        x = 100;  // 修改外部x
        return a + x;
    };
    std::cout << "lambda2(5) = " << lambda2(5) << std::endl;  // 输出: lambda2(5) = 105
    std::cout << "x after lambda2 = " << x << std::endl;  // 输出: x after lambda2 = 100
    
    // 混合捕获
    auto mixed = [=, &x](int a) {
        // 所有变量按值捕获，但x按引用
        return a + x;
    };
    
    // 初始化捕获（C++14）：捕获表达式计算结果
    auto initCapture = [z = x * 2](int a) { return a + z; };  // z是计算出来的
    std::cout << "initCapture(5) = " << initCapture(5) << std::endl;  // 输出: initCapture(5) = 25
    
    return 0;
}
```

> 捕获方式选择建议：
> 
> - 想只读不写：用`[=]`或`[x]`，安全
> - 想修改外部变量：用`[&]`或`[&x]`，但小心生命周期
> - 想要移动语义（把unique_ptr移进去）：用初始化捕获`[p = std::move(p)]`

### 值捕获与引用捕获

值捕获和引用捕获的区别，就像寄快递的两种方式：值捕获是寄复印件，引用捕获是寄原件的地址。

```cpp
#include <iostream>
#include <vector>
#include <memory>

int main() {
    int count = 10;
    
    // 值捕获：捕获的是变量的副本（快照）
    // 就像拍照，拍完你就变了，但照片不会变
    auto byValue = [count](int n) {
        return n + count;
    };
    count = 20;  // 修改不影响lambda中已经捕获的副本
    std::cout << "byValue(5) = " << byValue(5) << std::endl;  // 输出: byValue(5) = 15
    
    // 引用捕获：捕获的是变量的引用
    // 就像给对方家里的钥匙，对方可以随时进去改东西
    auto byRef = [&count](int n) {
        return n + count;
    };
    count = 20;  // 修改会影响lambda中的引用
    std::cout << "byRef(5) = " << byRef(5) << std::endl;  // 输出: byRef(5) = 25
    
    // 危险：用引用捕获局部变量后返回lambda
    // auto dangerous = [&count]() { return count; };
    // return dangerous;
    // 危险！如果返回的lambda在count作用域外被调用，会发生未定义行为
    // 想象你把朋友的电话号码记在笔记本上，结果朋友搬家了，你还拿着旧号码——打给谁呢？
    
    // 安全：用值捕获或使用shared_ptr
    auto safe = [count]() { return count; };  // count被复制，lambda有自己的副本
    std::cout << "safe() = " << safe() << std::endl;  // 输出: safe() = 20
    
    return 0;
}
```

### 隐式捕获陷阱

隐式捕获（`[=]`或`[&]`）虽然写起来方便，但容易踩坑。

```cpp
#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    int x = 10;
    
    // 隐式捕获
    // [=] - 隐式按值捕获
    // [&] - 隐式按引用捕获
    // 编译器会自动分析你在lambda体中使用了哪些外部变量
    
    auto implicitByValue = [=](int a) {
        return a + x;  // 隐式捕获x（按值）
    };
    
    auto implicitByRef = [&](int a) {
        // x = a;  // 修改外部x
        return a + x;
    };
    
    std::cout << "implicitByValue(5) = " << implicitByValue(5) << std::endl;
    // 输出: implicitByValue(5) = 15
    
    std::cout << "implicitByRef(5) = " << implicitByRef(5) << std::endl;
    // 输出: implicitByRef(5) = 15
    
    // 陷阱：在lambda内修改被值捕获的变量
    // 默认情况下，按值捕获的变量在const lambda中是只读的
    // 如果要修改，需要加mutable
    int multiplier = 2;
    auto mutableLambda = [multiplier](int n) mutable {
        multiplier = 10;  // mutable允许修改副本
        return n * multiplier;  // 返回10*n，而不是2*n
    };
    std::cout << "mutableLambda(5) = " << mutableLambda(5) << std::endl;  // 输出: mutableLambda(5) = 50
    std::cout << "multiplier after = " << multiplier << std::endl;  // 输出: multiplier after = 2（外部不变）
    
    return 0;
}
```

> 现代C++建议：尽量避免隐式捕获，使用显式捕获（`[x]`或`[&x]`）。这样代码更清晰，也更容易发现潜在bug。隐式捕获容易让人迷惑：到底用的是哪个x？

### 泛型Lambda（C++14）

C++14带来了**泛型Lambda**（Generic Lambda），参数可以使用`auto`，让lambda可以接受任何类型。这就像万能钥匙，能开多种锁。

```cpp
#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    // C++14: 泛型Lambda，参数使用auto
    // auto参数会被当作模板参数处理
    auto genericAdd = [](auto a, auto b) {
        return a + b;
    };
    
    std::cout << "genericAdd(1, 2) = " << genericAdd(1, 2) << std::endl;  // 输出: genericAdd(1, 2) = 3
    std::cout << "genericAdd(1.5, 2.5) = " << genericAdd(1.5, 2.5) << std::endl;  // 输出: genericAdd(1.5, 2.5) = 4
    
    // 等价于写了一个模板：
    // struct Closure {
    //     template<typename T, typename U>
    //     auto operator()(T a, U b) { return a + b; }
    // };
    
    // 泛型lambda与容器
    std::vector<int> nums = {3, 1, 4, 1, 5, 9, 2, 6};
    std::sort(nums.begin(), nums.end(), [](auto a, auto b) {
        return a > b;  // 降序排列
    });
    
    std::cout << "Sorted descending: ";
    for (auto n : nums) std::cout << n << " ";  // 输出: Sorted descending: 9 6 5 4 3 2 1 1
    std::cout << std::endl;
    
    return 0;
}
```

### 模板Lambda（C++20）

C++20进一步增强了lambda，允许显式指定模板参数，让代码更加精确。

```cpp
#include <iostream>

int main() {
    // C++20: 模板lambda
    // 语法：auto lambda = []<typename T>(T x) { ... };
    
    // C++14的泛型lambda中，auto参数在语义上是相同类型
    // C++20允许显式指定不同的模板参数
    
    // 示例：类型无关的比较
    auto typeAwareCompare = []<typename T>(const T& a, const T& b) {
        return a < b;
    };
    
    std::cout << "compare(1, 2) = " << typeAwareCompare(1, 2) << std::endl;  // 输出: compare(1, 2) = 1
    std::cout << "compare(1.5, 2.5) = " << typeAwareCompare(1.5, 2.5) << std::endl;
    // 输出: compare(1.5, 2.5) = 1
    
    // 示例：返回类型推导
    auto compute = []<typename T>(T a, T b) -> T {
        return a + b;
    };
    
    std::cout << "compute(10, 20) = " << compute(10, 20) << std::endl;  // 输出: compute(10, 20) = 30
    
    return 0;
}
```

### 初始化捕获（C++14）

**初始化捕获**（Initialized Capture）是C++14引入的特性，让捕获变得更加灵活。你可以捕获表达式的计算结果，甚至可以"移动"那些原本无法捕获的对象（如`unique_ptr`）。

```cpp
#include <iostream>
#include <vector>
#include <memory>

int main() {
    // C++14: 初始化捕获
    // [x = expression] 在捕获列表中直接初始化
    // 这解决了之前无法捕获临时对象或移动对象的问题
    
    std::vector<int> nums = {1, 2, 3, 4, 5};
    
    // 捕获移动后的对象
    // 之前无法捕获move后的对象，因为原对象会变空
    auto p = std::make_unique<int>(42);  // 堆上分配的独一份
    // C++14可以通过初始化捕获解决：
    auto capturedP = [p = std::move(p)]() {
        return *p;
    };
    std::cout << "capturedP() = " << capturedP() << std::endl;  // 输出: capturedP() = 42
    
    // 捕获计算结果
    auto expensive = [result = 10 * 10]() {
        return result;  // result已经被计算好了
    };
    std::cout << "expensive() = " << expensive() << std::endl;  // 输出: expensive() = 100
    
    // 移动捕获vector
    std::vector<int> source = {1, 2, 3};
    auto movedVec = [v = std::move(source)]() {
        return v.size();  // v是source被move后的结果
    };
    std::cout << "movedVec() = " << movedVec() << std::endl;  // 输出: movedVec() = 3
    
    return 0;
}
```

> 为什么要用初始化捕获？
> 
> 假设你想把一个`unique_ptr`捕获到lambda中：
> 
> - `auto bad = [p]` → 编译错误，unique_ptr不能复制
> - `auto bad = [&p]` → 危险，p的unique_ptr被移走后变成空
> - `auto good = [p = std::move(p)]` → 正确，lambda拥有了自己的unique_ptr

### Lambda属性（C++23）

C++23允许在lambda表达式上使用属性（Attributes），让lambda也能享受`[[nodiscard]]`、`[[deprecated]]`等特权。

```cpp
#include <iostream>

int main() {
    // C++23: Lambda可以有自己的属性
    // [[nodiscard]] auto getLambda = []() { return 42; };
    // 如果调用者忽略了返回值，编译器会警告
    
    // 示例：deprecated lambda
    [[deprecated("Use newVersion() instead")]]
    auto oldFunctionality = [](int x) { return x * 2; };
    
    // 可以在lambda调用时使用
    // int result = oldFunctionality(10);  // 编译警告：使用了已废弃的lambda
    
    // C++23还支持更多属性在lambda上的使用
    std::cout << "Lambda with attributes demo (C++23 features)" << std::endl;
    
    return 0;
}
```

### Lambda可选括号简化（C++23）

C++23带来了一个微小但贴心的简化：空参数列表的lambda可以省略`()`。

```cpp
#include <iostream>

int main() {
    // C++23: 空参数列表的lambda可以省略()
    // 之前：auto f = []() { return 42; };
    // C++23：auto f = [] { return 42; };
    
    auto noParams = [] { return 42; };  // C++23简化语法
    std::cout << "noParams() = " << noParams() << std::endl;  // 输出: noParams() = 42
    
    // 注意：这仅适用于空参数列表
    // 如果有参数，仍然需要括号
    auto withParams = [](int x) { return x * 2; };
    std::cout << "withParams(21) = " << withParams(21) << std::endl;  // 输出: withParams(21) = 42
    
    // C++23还简化了泛型lambda的语法
    // auto generic = []<typename T>(T x) { return x; };
    
    return 0;
}
```

### 静态Lambda（C++23）

C++23允许在lambda内部声明静态变量，这在之前是不可能的。

```cpp
#include <iostream>

int main() {
    // C++23: 静态lambda
    // 语法：static lambda 和普通lambda一样，但内部可以有静态成员
    
    auto staticLambda = []() {
        static int counter = 0;  // C++23允许在lambda内声明静态变量
        ++counter;
        return counter;
    };
    
    std::cout << "Call 1: " << staticLambda() << std::endl;  // 输出: Call 1: 1
    std::cout << "Call 2: " << staticLambda() << std::endl;  // 输出: Call 2: 2
    std::cout << "Call 3: " << staticLambda() << std::endl;  // 输出: Call 3: 3
    
    // 之前lambda内不能有静态变量，因为lambda本质是类的operator()
    // C++23放开这个限制，但这更像是语法糖
    // 实际上等价于在类里声明了一个静态成员
    
    return 0;
}
```

### 生命周期陷阱

Lambda虽好，但捕获有风险。如果捕获了局部变量的引用，然后返回这个lambda——你可能会收获一个"悬空引用"（Dangling Reference），程序行为变成未定义。

```cpp
#include <iostream>
#include <functional>

int main() {
    // 陷阱1：捕获局部变量的引用并返回lambda
    // auto badLambda = [&x]() { return x; };
    // return badLambda;
    // 危险！x在作用域结束后销毁，lambda里的引用变成了悬空引用
    // 运行这段代码可能会：打印垃圾值、程序崩溃、或者看起来"正常"但实际有问题
    
    // 陷阱2：lambda捕获了临时对象的引用
    // auto bad = [&str = std::string("temp")]() { return str; };
    // 危险！临时string在构造后立即销毁
    // 生命周期陷阱比上面的更难发现，因为语法看起来是合法的
    
    // 安全做法：用值捕获
    int localValue = 10;
    auto safeLambda = [localValue]() { return localValue; };
    // localValue被复制了一份到lambda中，原变量销毁不受影响
    
    // 安全做法2：用移动捕获（C++14）
    auto safeMove = [captured = std::vector<int>{1, 2, 3}](int index) {
        if (index >= 0 && index < captured.size()) {
            return captured[index];
        }
        return 0;
    };
    std::cout << "safeMove(1) = " << safeMove(1) << std::endl;  // 输出: safeMove(1) = 2
    
    // 最佳实践：使用std::function时要注意
    std::function<int()> f;
    {
        int x = 5;
        // f = [x]() { return x; };  // OK，x被复制，生命周期安全
        // f = [&x]() { return x; };  // 危险！x销毁后f无效，调用会出事
    }
    // 当离开这个作用域，x被销毁
    // 如果f持有的是[&x]的lambda，现在f就是一颗定时炸弹
    
    return 0;
}
```

> 黄金法则：如果lambda会存活超过创建它的作用域，**永远不要捕获局部变量的引用**。用值捕获，或者用移动语义转移所有权。

## 本章小结

本章我们深入探索了C++函数的方方面面，从基础的定义与声明，到参数传递的各种方式，再到返回值、多返回值技术、函数重载、默认参数、内联函数、constexpr/consteval、递归、main函数参数，以及强大的Lambda表达式。

**核心要点回顾：**

| 概念 | 关键点 |
|------|--------|
| 函数定义与声明 | 声明告诉编译器"有这个人"，定义说"这个人是干什么的" |
| 值传递 | 传递副本，原变量不受影响，适合小数据 |
| 指针传递 | 传递地址，可修改原变量，需要注意空指针 |
| 引用传递 | 给变量起别名，直接操作原变量，现代C++首选 |
| 返回类型推导 | auto关键字让编译器自动推断返回类型 |
| 多返回值 | pair、tuple、结构化绑定，三种武器任你选 |
| RVO/NRVO | 编译器优化，省去返回值复制的开销 |
| 函数重载 | 同名不同参，编译器自动匹配最合适的版本 |
| 默认参数 | 省略参数使用默认值，但要注意重载歧义 |
| 内联函数 | 以空间换时间，小函数高频调用场景适用 |
| constexpr | 编译期计算，constexpr是"能算就算" |
| consteval | 强制编译期计算，"必须现在就算好" |
| 递归 | 函数调用自己，注意终止条件防止栈溢出 |
| Lambda | 就地定义函数，捕获列表是关键 |
| 值捕获vs引用捕获 | 值是快照，引用是钥匙，生命周期要小心 |

> 学习C++就像修仙，函数是各种功法，lambda是速成功法，constexpr是预知未来。路漫漫其修远兮，吾将上下而求索！