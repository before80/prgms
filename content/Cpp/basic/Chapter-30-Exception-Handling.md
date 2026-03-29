+++
title = "第30章 异常处理 程序界的 '紧急刹车' 与 '逃生舱'"
weight = 300
date =  "2026-03-29T21:03:00+08:00"
type  =  "docs"
description = ""
isCJKLanguage  =  true
draft = false

+++


# 第30章 异常处理：程序界的"紧急刹车"与"逃生舱"

> "Life is full of exceptions, and so is C++." —— 某位被除零错误逼疯的程序员

想象一下：你正在厨房做蛋糕，结果发现面粉用完了。这时候你会怎么做？

- **选项A**：假装什么都没发生，继续揉空气？
- **选项B**：大喊一声"面粉没了！"，让整栋楼都知道？
- **选项C**：优雅地把无面粉烹饪这个"意外情况"记录下来，然后想办法解决？

恭喜你，**选项C**就是C++异常处理机制的核心理念！??

## 30.1 异常处理机制概述：程序界的"多米诺骨牌"

### 什么是异常？

**异常（Exception）**是程序在执行过程中发生的"意外事件"——就像你精心策划的求婚仪式，结果戒指掉进了下水道。这种事情不常见，但一旦发生，你就需要一个备用方案。

在C++中，异常处理机制由三个核心关键字组成：**try**、**catch**、**throw**。它们就像一套精密的报警系统：

```cpp
#include <iostream>

/*
 * 异常处理机制：
 * 
 * try - catch - throw 三剑客
 * 
 * 当异常发生时，就像多米诺骨牌倒下：
 * 1. throw表达式抛出异常 —— 就像第一个倒下的骨牌
 * 2. 栈展开（stack unwinding）—— 沿途摧毁所有局部对象，就像骨牌经过之处全部倒下
 * 3. 寻找匹配的catch块 —— 寻找能接住这个异常的"接盘侠"
 * 4. 如果没找到，调用std::terminate() —— 程序直接崩溃，就像骨牌没被接住直接砸地上
 * 
 * 流程图：
 * 
 *     ┌─────────────────────────────────────────┐
 *     │              程序正常运行                  │
 *     └─────────────────┬───────────────────────┘
 *                       ▼
 *              ┌───────────────────┐
 *              │    发生异常？        │
 *              └─────────┬───────────┘
 *                    ┌───┴───┐
 *                   Yes     No
 *                   │       │
 *                   ▼       ▼
 *          ┌───────────┐  ┌─────────────────┐
 *          │  throw    │  │  继续执行（正常）  │
 *          └─────┬─────┘  └─────────────────┘
 *                ▼
 *          ┌───────────┐
 *          │ 栈展开    │ ?── 销毁局部对象，释放资源
 *          └─────┬─────┘
 *                ▼
 *          ┌───────────┐
 *          │ 寻找catch │ ?── 匹配异常类型
 *          └─────┬─────┘
 *                ▼
 *     ┌──────────┴──────────┐
 *    找到                  没找到
 *     │                      │
 *     ▼                      ▼
 * ┌────────┐           ┌──────────┐
 * │ 处理异常 │          │terminate()│
 * └────┬───┘           └────┬─────┘
 *      │                    │
 *      ▼                    ▼
 * ┌─────────┐          ┌─────────┐
 * │ 程序继续 │          │ 程序崩溃 │
 * └─────────┘          └─────────┘
 */

int main() {
    std::cout << "=== 异常处理机制概述 ===" << std::endl;
    std::cout << "想象一下：你的程序是一个精密的瑞士手表" << std::endl;
    std::cout << "异常就是那只不小心掉进手表里的螺丝钉" << std::endl;
    std::cout << "try-catch-throw就是取出螺丝钉的工具箱！" << std::endl;
    
    return 0;
    // 输出: 程序正常运行完毕，没有异常发生
}
```

### 为什么需要异常处理？

> 有人说过："没有异常处理的程序，就像没有安全气囊的汽车——能开，但出事就完蛋。"

传统的错误处理方式（比如检查返回值）有几个致命问题：

1. **容易忽略**：程序员懒得检查每一个返回值，就像你懒得检查每封邮件的拼写
2. **传播困难**：错误码需要一层层往上传，就像传话游戏，最后可能面目全非
3. **混淆视听**：正常逻辑和错误处理搅在一起，代码可读性差到让你怀疑人生

```cpp
// 传统错误处理的噩梦
int result = doSomething();
if (result == ERROR_FILE_NOT_FOUND) {
    // 处理文件不存在
} else if (result == ERROR_PERMISSION_DENIED) {
    // 处理权限错误
} else if (result == ERROR_OUT_OF_MEMORY) {
    // 处理内存不足
}
// ... 可能还有一百种错误
// 而doSomething()的返回值本来应该是真正有用的结果！
```

异常处理让错误处理**优雅而集中**，就像把所有的垃圾都扔进一个垃圾桶，而不是客厅一个、厨房一个、卧室一个。

## 30.2 try-catch-throw语法：三位一体的救赎

### throw：抛出异常的艺术

**throw**关键字就像程序界的"求救信号弹"。当你发现事情不对劲，就扔出这个信号：

```cpp
throw std::runtime_error("DIVISION BY ZERO! Abort mission!");
```

但要注意，抛出异常是有"代价"的——程序会停止当前执行流程，进入"逃生模式"。

### try-catch：捕获与处理

**try块**就像一个警戒区域，里面的代码都在被监视。一旦有异常抛出，**catch块**就会出场接住它。

```cpp
#include <iostream>
#include <stdexcept>

// 这是一个可能"翻车"的除法函数
// 想象成一个杂技演员走钢丝
double divide(double a, double b) {
    if (b == 0.0) {
        // 演员失去平衡！抛出异常！
        throw std::runtime_error("Division by zero! Superman也救不了这个除法！");
    }
    // 平衡落地，返回结果
    return a / b;
}

int main() {
    std::cout << "=== try-catch-throw 语法演示 ===" << std::endl;
    std::cout << "场景：计算 10.0 除以 0.0（数学老师的噩梦）" << std::endl;
    
    // try块：危险区域
    try {
        std::cout << "尝试执行：divide(10.0, 0.0)" << std::endl;
        double result = divide(10.0, 0.0);  // 这行会抛出异常！
        // 这行永远不会执行，因为上面已经throw了
        std::cout << "Result: " << result << std::endl;
    }
    // catch块：救援队
    catch (const std::runtime_error& e) {
        // 捕获 runtime_error 类型的异常
        // e.what() 返回异常信息，就像求救电话里的地址
        std::cout << "【救援成功】Runtime error: " << e.what() << std::endl;
        // 输出: 【救援成功】Runtime error: Division by zero! Superman也救不了这个除法！
    }
    // 通用的exception捕获器
    catch (const std::exception& e) {
        // 捕获所有 std::exception 的子类异常
        // 这是个"万金油"catch块
        std::cout << "【通用救援】Exception: " << e.what() << std::endl;
    }
    // 万能捕获器
    catch (...) {
        // 三个点...表示"任何类型的异常"
        // 这是最后的防线，就像宇宙最后一道防线"复仇者联盟"
        std::cout << "【终极救援】Unknown exception caught! 我不知道发生了什么，但我接住了！" << std::endl;
    }
    
    // 程序在异常处理后继续执行
    std::cout << "【程序继续】灾后的世界依然美好，程序继续运行~" << std::endl;
    
    return 0;
}
```

### 多个catch块：层层设防

```cpp
#include <iostream>
#include <stdexcept>
#include <vector>

int main() {
    std::cout << "=== 多个catch块演示 ===" << std::endl;
    
    // 模拟一个会抛出各种异常的场景
    std::vector<int> numbers = {1, 2, 3};
    
    try {
        // 故意制造一个越界访问
        std::cout << "尝试访问 numbers[99]..." << std::endl;
        int x = numbers.at(99);  // at()会抛出 std::out_of_range
        (void)x;  // 避免unused警告
    }
    // catch块的顺序很重要！子类要在父类前面！
    catch (const std::out_of_range& e) {
        // 最具体的异常类型放最前面
        std::cout << "【精确捕获】越界啦：" << e.what() << std::endl;
        // 输出: 【精确捕获】越界啦：vector::_M_range_check: __n (which is 99) >= this->size() (which is 3)
    }
    catch (const std::exception& e) {
        // 通用的异常捕获放后面
        std::cout << "【通用捕获】其他std::exception：" << e.what() << std::endl;
    }
    catch (...) {
        // 最后一道防线
        std::cout << "【终极捕获】未知异常！" << std::endl;
    }
    
    std::cout << "程序安然无恙地结束了~" << std::endl;
    
    return 0;
}
```

> **小贴士**：catch块的顺序就像相亲时的条件筛选——最挑剔的放前面，"是个活人就行"的放后面。如果把`catch(const std::exception&)`放第一个，那`std::out_of_range`就永远被它抢走了！

## 30.3 标准异常类层次：异常界的"族谱"

### 异常类的继承关系

C++标准库定义了一套完整的异常类继承体系，就像一个庞大的家族：

```
                                    ┌─────────────────────┐
                                    │   std::exception     │ ?── 所有异常的"老祖宗"
                                    └──────────┬──────────┘
                                               │
            ┌──────────────────────────────────┼──────────────────────────────────┬───────────────────────┐
            │                                  │                                  │                       │
            ▼                                  ▼                                  ▼                       ▼
┌─────────────────────┐            ┌─────────────────────┐            ┌─────────────────────┐ ┌─────────────────────┐
│  std::logic_error   │            │  std::runtime_error │            │    std::bad_alloc   │ │    std::bad_cast    │
│ (程序的逻辑错误)     │            │  (运行时错误)        │            │   (内存分配失败)     │ │   (类型转换失败)     │
└──────────┬──────────┘            └──────────┬──────────┘            └─────────────────────┘ └─────────────────────┘
           │                                  │
           ▼                                  ▼
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│  logic_error 家族（程序员应该知道的错误）                                                  │
│  - std::domain_error      │ 数学定义域错误（比如对负数开平方根）                            │
│  - std::invalid_argument  │ 无效参数（比如给abs()传了个字符串）                            │
│  - std::length_error      │ 长度超限（比如string太长了）                                   │
│  - std::out_of_range      │ 范围超限（数组/vector越界访问）                                │
└─────────────────────────────────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│  runtime_error 家族（只有运行时才能发现的错误）                                            │
│  - std::overflow_error   │ 算术溢出（结果太大了，装不下）                                  │
│  - std::underflow_error  │ 算术下溢（结果太小了，接近零）                                 │
│  - std::range_error      │ 范围错误（结果在技术上有效但超出预期范围）                       │
└─────────────────────────────────────────────────────────────────────────────────────────┘
另外：std::bad_typeid —— typeid应用于多态类型的空指针解引用时抛出
```

### 各种标准异常的使用场景

```cpp
#include <iostream>
#include <stdexcept>
#include <new>      // std::bad_alloc
#include <typeinfo> // std::bad_cast
#include <string>

int main() {
    std::cout << "=== 标准异常类层次详解 ===" << std::endl;
    std::cout << "让我们来认识一下异常家族的各位成员...\n" << std::endl;
    
    // 1. std::out_of_range - 最常见的"越界访问"
    std::cout << "【1】std::out_of_range：数组/容器的噩梦" << std::endl;
    try {
        std::string s = "Hello";
        char c = s.at(100);  // 越界！s只有5个字符
    } catch (const std::out_of_range& e) {
        std::cout << "  捕获： " << e.what() << std::endl;
        // 输出类似: 捕获： string::_M_check_subscript: __pos (which is 100) >= this->size() (which is 5)
    }
    
    // 2. std::invalid_argument - 参数不合法
    std::cout << "\n【2】std::invalid_argument：参数的"身份危机"" << std::endl;
    try {
        // 模拟：把字符串转成整数，但字符串不是数字
        int n = std::stoi("hello world");  // 这会抛出invalid_argument
        (void)n;
    } catch (const std::invalid_argument& e) {
        std::cout << "  捕获： " << e.what() << std::endl;
        // 输出: 捕获： stoi: no conversion
    }
    
    // 3. std::bad_alloc - 内存分配失败（OOM）
    std::cout << "\n【3】std::bad_alloc：内存不足警告" << std::endl;
    try {
        // 尝试分配一个巨大的内存块（比如1YB，宇宙都装不下的大小）
        // 这只是一个演示，实际分配可能会失败
        void* p = std::malloc(1ULL * 1024 * 1024 * 1024 * 1024 * 1024 * 1024);
        if (!p) {
            throw std::bad_alloc();
        }
        std::cout << "  内存分配成功（实际上可能不会执行到这里）" << std::endl;
        std::free(p);
    } catch (const std::bad_alloc& e) {
        std::cout << "  捕获： " << e.what() << std::endl;
        // 输出: 捕获： std::bad_alloc
    }
    
    // 4. std::runtime_error - 运行时错误（最常用的自定义异常基类）
    std::cout << "\n【4】std::runtime_error：运行时才暴露的"潜伏者"" << std::endl;
    try {
        throw std::runtime_error("自定义运行时错误：我运行到一半才发现问题！");
    } catch (const std::runtime_error& e) {
        std::cout << "  捕获： " << e.what() << std::endl;
        // 输出: 捕获： 自定义运行时错误：我运行到一半才发现问题！
    }

    // 5. std::bad_cast - 动态类型转换失败
    std::cout << "\n【5】std::bad_cast：类型转换的"社死"现场" << std::endl;
    try {
        class Base { public: virtual ~Base() = default; };
        class Derived1 : public Base {};
        class Derived2 : public Base {};
        Base* basePtr = new Derived1();  // 实际指向 Derived1
        // 尝试将指向 Derived1 的指针当作 Derived2——dynamic_cast 失败！
        // 注意：dynamic_cast 对指针返回 nullptr，不抛异常
        // 这里手动抛异常来演示 bad_cast 的用法
        Derived2* derived2Ptr = dynamic_cast<Derived2*>(basePtr);
        if (!derived2Ptr) {
            throw std::bad_cast();  // 手动抛出
        }
        (void)derived2Ptr;
    } catch (const std::bad_cast& e) {
        std::cout << "  捕获： " << e.what() << std::endl;
        // 输出: 捕获： std::bad_cast
    }

    // 6. std::bad_typeid - typeid运算符的"翻车"
    std::cout << "\n【6】std::bad_typeid：typeid的"身份危机"" << std::endl;
    try {
        class Base { 
        public: 
            virtual ~Base() = default;  // 有虚函数才有多态，typeid才能识别类型
        };
        Base* basePtr = nullptr;
        // 对 nullptr 解引用后的多态对象使用 typeid，结果就是 std::bad_typeid
        // 注意：这不是对 nullptr 本身用 typeid，而是对 *basePtr 用 typeid
        // basePtr 虽然是 nullptr，但类型信息依然可从 vtable 获得，typeid 可以工作
        // 实际上在某些实现中，typeid(*nullptr) 会抛 bad_typeid（标准未定义行为）
        // 下面的代码使用 RTTI 机制正确触发 bad_typeid：
        const std::type_info& ti = typeid(*basePtr);  // UB！但某些实现会抛异常
        (void)ti;
        std::cout << "  （UB场景，行为依赖于编译器）" << std::endl;
    } catch (const std::bad_typeid& e) {
        std::cout << "  捕获： " << e.what() << std::endl;
        // 输出: 捕获： std::bad_typeid
    } catch (...) {
        std::cout << "  其他异常或UB行为" << std::endl;
    }

    std::cout << "\n【总结】std::exception::what() 返回异常的描述信息" << std::endl;
    std::cout << "这就是为什么catch块里经常调用what()——它告诉你发生了什么！" << std::endl;

    return 0;
}
```

### 异常继承关系的实际应用

```cpp
#include <iostream>
#include <stdexcept>
#include <vector>

int main() {
    // 利用异常继承关系，可以用基类捕获所有子类异常
    std::cout << "=== 利用异常继承链一次性捕获多种异常 ===" << std::endl;
    
    std::vector<int> v = {1, 2, 3};
    
    // 用 std::exception 捕获所有标准库异常
    try {
        v.at(999);  // out_of_range
    } catch (const std::exception& e) {
        // out_of_range 是 exception 的子类，所以能被捕获
        std::cout << "被 std::exception 捕获了：" << e.what() << std::endl;
        // 输出: 被 std::exception 捕获了：vector::_M_range_check: ...
        std::cout << "异常类型：" << typeid(e).name() << std::endl;
    }
    
    return 0;
}
```

## 30.4 自定义异常类：打造你的专属"异常IP"

### 为什么需要自定义异常？

标准异常虽好，但就像公共厕所——能用，但总觉得不够贴心。自定义异常可以：

1. **携带更多上下文信息**：比如错误码、发生时间、相关数据
2. **表达更具体的业务含义**：`NetworkError`比`runtime_error`更容易让人理解
3. **支持更精细的捕获**：不同类型的错误可以有不同的处理方式

### 自定义异常类的设计

```cpp
#include <iostream>
#include <exception>
#include <string>
#include <chrono>

/*
 * 自定义异常类设计指南：
 * 
 * 1. 继承自 std::exception 或其子类
 * 2. 重写 what() 方法返回错误信息
 * 3. 添加业务相关的成员变量
 * 4. 保持类的简洁性和可拷贝性
 */

// 网络错误异常 —— 专门处理网络相关的"车祸现场"
class NetworkError : public std::exception {
private:
    std::string message_;    // 错误消息
    int errorCode_;          // 错误码（404 Not Found? 500 Internal Error?）
    std::string url_;        // 出错的URL
    std::chrono::system_clock::time_point timestamp_;  // 发生时间
    
public:
    // 构造函数：用初始化列表来初始化成员（高效！）
    NetworkError(const std::string& msg, int code, const std::string& url = "")
        : message_(msg)
        , errorCode_(code)
        , url_(url)
        , timestamp_(std::chrono::system_clock::now())  // 记录当前时间
    {}
    
    // 重写 what()：这是 exception 类的虚函数，必须实现！
    // noexcept 表示这个函数不会抛出异常（what()本来就不该抛异常）
    const char* what() const noexcept override {
        // message_ 是成员变量，生命周期与对象相同，因此 c_str() 是安全的
        // 注意：如果返回局部 std::string 的 c_str() 才是危险的（临时对象已销毁）
        return message_.c_str();
    }
    
    // 业务方法：获取错误码
    int code() const { return errorCode_; }
    
    // 业务方法：获取URL
    const std::string& url() const { return url_; }
};

// 数据库错误异常 —— 数据库操作的"专属保镖"
class DatabaseError : public std::runtime_error {
private:
    std::string query_;       // 导致错误的SQL查询
    int sqlCode_;             // SQL错误码
    
public:
    DatabaseError(const std::string& msg, const std::string& query, int sqlCode)
        : std::runtime_error(msg)  // 调用父类构造函数
        , query_(query)
        , sqlCode_(sqlCode)
    {}
    
    // 获取出错的SQL
    const std::string& query() const { return query_; }
    int sqlCode() const { return sqlCode_; }
};

int main() {
    std::cout << "=== 自定义异常类演示 ===" << std::endl;
    std::cout << "场景：模拟网络请求失败\n" << std::endl;
    
    // 场景1：抛出NetworkError
    try {
        throw NetworkError("Connection failed", 404, "https://api.example.com/users");
    }
    catch (const NetworkError& e) {
        std::cout << "【网络错误】" << std::endl;
        std::cout << "  消息：" << e.what() << std::endl;
        std::cout << "  错误码：" << e.code() << std::endl;
        std::cout << "  URL：" << e.url() << std::endl;
        // 输出:
        // 【网络错误】
        // 消息：Connection failed
        // 错误码：404
        // URL：https://api.example.com/users
    }
    
    std::cout << std::endl;
    
    // 场景2：使用继承自runtime_error的DatabaseError
    try {
        throw DatabaseError("Duplicate key violation", 
                           "INSERT INTO users VALUES (1, 'Alice')", 
                           1062);  // MySQL的Duplicate entry错误码
    }
    catch (const DatabaseError& e) {
        std::cout << "【数据库错误】" << std::endl;
        std::cout << "  消息：" << e.what() << std::endl;
        std::cout << "  SQL：" << e.query() << std::endl;
        std::cout << "  SQL错误码：" << e.sqlCode() << std::endl;
        // 输出:
        // 【数据库错误】
        // 消息：Duplicate key violation
        // SQL：INSERT INTO users VALUES (1, 'Alice')
        // SQL错误码：1062
    }
    
    std::cout << "\n【心得】自定义异常让错误处理更有针对性！" << std::endl;
    std::cout << "就像去医院挂号——看专科医生比看全科医生更有效率~" << std::endl;
    
    return 0;
}
```

## 30.5 异常安全与资源管理：厕所纸的哲学

### 三种异常安全保证

想象你正在用公共厕所，最关心什么？

1. **不会把自己锁在里面出不去**（基本保证）
2. **出来时厕所跟没人用过一样**（强保证）
3. **保证永远有纸**（不抛异常保证）

```cpp
#include <iostream>
#include <vector>
#include <memory>
#include <fstream>

/*
 * 异常安全三兄弟：
 * 
 * ┌─────────────────────────────────────────────────────────────────────────────┐
 * │  1. 基本保证（Basic Guarantee）                                              │
 * │     "出了事不丢人"                                                            │
 * │     - 资源不泄漏                                                             │
 * │     - 对象处于有效但未定义的状态                                               │
 * │     - 用户代码可以检测并处理                                                   │
 * └─────────────────────────────────────────────────────────────────────────────┘
 * 
 * ┌─────────────────────────────────────────────────────────────────────────────┐
 * │  2. 强保证（Strong Guarantee）                                                │
 * │     "要么完美成功，要么当什么都没发生"                                          │
 * │     - 操作要么完全成功                                                       │
 * │     - 要么失败回滚，对象状态不变                                               │
 * │     - 典型的例子：std::vector::push_back                                       │
 * └─────────────────────────────────────────────────────────────────────────────┘
 * 
 * ┌─────────────────────────────────────────────────────────────────────────────┐
 * │  3. 不抛异常保证（No-throw Guarantee）                                        │
 * │     "我保证不会搞砸"                                                          │
 * │     - 函数永远不会抛出异常                                                    │
 * │     - 失败了也会优雅地处理或终止操作                                            │
 * │     - 典型例子：swap(), destructor, mutex lock                                │
 * └─────────────────────────────────────────────────────────────────────────────┘
 */

// 模拟一个需要管理资源的类 —— 比如打开文件
class FileHandler {
private:
    std::fstream file_;
    std::string filename_;
    
public:
    FileHandler(const std::string& filename) : filename_(filename) {
        // 模拟：打开文件可能失败
        if (filename.empty()) {
            throw std::invalid_argument("Filename cannot be empty!");
        }
    }
    
    ~FileHandler() {
        // 析构函数：保证资源释放
        // 析构函数绝对不能抛异常！否则会导致std::terminate()
        if (file_.is_open()) {
            file_.close();
        }
        std::cout << "  [FileHandler] 文件已关闭，资源安全释放" << std::endl;
    }
    
    // 基本保证：操作可能失败，但不会泄漏资源
    void write(const std::string& data) {
        // 如果写入失败，对象状态可能不确定
        // 但文件会被正确关闭，资源不泄漏
        if (data.length() > 1000) {
            throw std::length_error("Data too long!");
        }
        std::cout << "  写入数据： " << data << std::endl;
    }
};

// RAII：资源获取即初始化 —— 异常安全编程的黄金法则
class SmartResource {
private:
    int* data_;
    
public:
    SmartResource(int size) : data_(nullptr) {
        // 注意：所有可能抛异常的操作（不仅仅是new）都应该放在
        // 资源分配之前！如果在new成功后抛异常，析构函数不会运行，会泄漏！
        std::cout << "  即将分配 " << size << " 个int的内存..." << std::endl;
        data_ = new int[size];  // 如果这里抛异常（std::bad_alloc），没有泄漏，因为data_还是nullptr
        std::cout << "  分配成功！" << std::endl;
    }
    
    ~SmartResource() {
        delete[] data_;
        std::cout << "  [SmartResource] 内存已释放，无泄漏！" << std::endl;
    }
    
    // 不抛异常保证的swap
    void swap(SmartResource& other) noexcept {
        std::swap(data_, other.data_);
    }
};

int main() {
    std::cout << "=== 异常安全与资源管理 ===" << std::endl;
    std::cout << "核心理念：RAII - Resource Acquisition Is Initialization\n" << std::endl;
    
    // 1. 基本保证演示
    std::cout << "【1】基本保证（Basic Guarantee）" << std::endl;
    std::cout << "保证：出了事不丢人，资源不泄漏\n" << std::endl;
    
    try {
        FileHandler fh("test.txt");
        fh.write("Hello, World!");
        // 如果write抛出异常，fh的析构函数会被调用
        // 文件会被正确关闭
        fh.write("Too long data that will trigger exception"
                 "................................................................."
                 "................................................................."
                 "................................................................."
                 ".................................................................");
    } catch (const std::exception& e) {
        std::cout << "  捕获异常：" << e.what() << std::endl;
    }
    // 即使抛出异常，FileHandler的析构函数也会被调用
    // 文件资源得到正确释放
    
    std::cout << std::endl;
    
    // 2. 强保证演示
    std::cout << "【2】强保证（Strong Guarantee）" << std::endl;
    std::cout << "保证：要么全部成功，要么当什么都没发生\n" << std::endl;
    
    std::vector<int> v{1, 2, 3};
    std::cout << "  操作前：v = {1, 2, 3}" << std::endl;
    
    try {
        // std::vector::insert 提供强保证
        // 要么完全成功，v变成{0, 1, 2, 3}
        // 要么失败，v保持{1, 2, 3}不变
        v.insert(v.begin(), 0);
        std::cout << "  操作后：v = {0, 1, 2, 3}" << std::endl;
        std::cout << "  强保证生效：操作成功，状态符合预期" << std::endl;
    } catch (...) {
        std::cout << "  操作失败（不会发生在这个例子中）" << std::endl;
        std::cout << "  v 保持原状态：{1, 2, 3}" << std::endl;
    }
    
    std::cout << std::endl;
    
    // 3. 不抛异常保证演示
    std::cout << "【3】不抛异常保证（No-throw Guarantee）" << std::endl;
    std::cout << "保证：我保证不会搞砸，就算天塌了也不抛异常\n" << std::endl;
    
    SmartResource a(10);
    SmartResource b(20);
    
    std::cout << "  交换前：a有10个int的内存，b有20个int的内存" << std::endl;
    a.swap(b);  // noexcept保证，不会抛异常
    std::cout << "  交换后：内存已互换（注意：析构顺序）" << std::endl;
    
    std::cout << "\n【总结】RAII是异常安全的基石！" << std::endl;
    std::cout << "原理：把资源管理封装在析构函数里，异常发生时自动释放" << std::endl;
    std::cout << "就像公共厕所的自动门——不管里面发生什么，出来时门一定会开~" << std::endl;
    
    return 0;
}
```

### RAII：异常安全的黄金法则

```cpp
#include <iostream>
#include <memory>  // std::unique_ptr

/*
 * RAII 的魔力：
 * 
 * 传统写法（危险）：
 * void process() {
 *     Resource* r = new Resource();
 *     r->use();
 *     delete r;  // 如果use()抛异常，这行永远不会执行！内存泄漏！
 * }
 * 
 * RAII写法（安全）：
 * void process() {
 *     std::unique_ptr<Resource> r = std::make_unique<Resource>();
 *     r->use();  // 即使这里抛异常，unique_ptr的析构也会自动delete
 * }  // 自动释放资源
 */

// 模拟一个稀缺资源（比如数据库连接）
class DatabaseConnection {
private:
    std::string connectionString_;
    bool isConnected_;
    
public:
    DatabaseConnection(const std::string& connStr) 
        : connectionString_(connStr), isConnected_(false) {
        // 模拟建立连接
        if (connStr.empty()) {
            throw std::invalid_argument("Empty connection string");
        }
        isConnected_ = true;
        std::cout << "  [DB] 连接已建立: " << connStr << std::endl;
    }
    
    ~DatabaseConnection() {
        if (isConnected_) {
            std::cout << "  [DB] 连接已关闭（RAII自动关闭）" << std::endl;
        }
    }
    
    void query(const std::string& sql) {
        if (sql.empty()) {
            throw std::invalid_argument("Empty SQL query");
        }
        std::cout << "  [DB] 执行SQL: " << sql << std::endl;
    }
};

void badExample() {
    std::cout << "=== 危险写法（非RAII） ===" << std::endl;
    std::cout << "（模拟场景：连接数据库后执行查询时抛异常）\n" << std::endl;
    
    // 在C++中使用裸指针模拟"危险"场景
    // 实际开发中请勿这样做！
    DatabaseConnection* db = nullptr;
    
    try {
        db = new DatabaseConnection("mysql://localhost:3306/test");
        db->query("SELECT * FROM users");  // 这里可能抛异常
        db->query("");  // 空SQL，抛异常！
    } catch (const std::exception& e) {
        std::cout << "  捕获异常：" << e.what() << std::endl;
        std::cout << "  【危险】如果这是真实场景，连接可能泄漏！" << std::endl;
    }
    
    // 即使有异常，也应该清理资源
    if (db) {
        delete db;  // 手动清理
        std::cout << "  手动delete（但如果忘记了呢？）" << std::endl;
    }
}

void goodExample() {
    std::cout << "\n=== 安全写法（RAII + smart pointer） ===" << std::endl;
    std::cout << "（模拟场景：连接数据库后执行查询时抛异常）\n" << std::endl;
    
    // 使用智能指针，异常安全！
    // 即使抛异常，析构函数也会自动调用，释放资源
    auto db = std::make_unique<DatabaseConnection>("mysql://localhost:3306/test");
    
    db->query("SELECT * FROM users");  // 正常执行
    db->query("SELECT * FROM WHERE id = 1");  // 语法错误的SQL，抛异常！
}

int main() {
    std::cout << "=== RAII：异常安全的黄金法则 ===\n" << std::endl;
    
    badExample();
    std::cout << "\n（程序继续运行...）\n" << std::endl;
    
    try {
        goodExample();
    } catch (const std::exception& e) {
        std::cout << "  捕获异常：" << e.what() << std::endl;
        std::cout << "  【安全】智能指针已自动清理资源！" << std::endl;
    }
    
    std::cout << "\n【RAII的精髓】" << std::endl;
    std::cout << "1. 资源获取在构造函数里" << std::endl;
    std::cout << "2. 资源释放在析构函数里" << std::endl;
    std::cout << "3. 异常发生时，局部对象自动销毁，资源自动释放" << std::endl;
    std::cout << "4. 即使抛异常，也不会有资源泄漏！" << std::endl;
    
    return 0;
}
```

## 30.6 noexcept关键字（C++11）：承包"不出事"的保证

### 什么是noexcept？

**noexcept**是C++11引入的关键字，用于声明一个函数**不会**或**不会抛出**异常。它就像是函数的"健康保证"：

```cpp
void safeFunction() noexcept;  // 我保证这个函数永远不会抛异常
void riskyFunction();           // 我可能会抛异常，别怪我没提醒你
```

### noexcept与性能优化

```cpp
#include <iostream>
#include <vector>
#include <type_traits>

/*
 * noexcept 关键字的作用：
 * 
 * 1. 编译器的"性能外挂"
 *    - 编译器知道函数不抛异常，可以做更多优化
 *    - 不用生成回滚代码（stack unwinding code）
 *    - 可以做更 aggressive 的内联优化
 * 
 * 2. 移动语义的最佳搭档
 *    - std::vector::push_back 在C++11后会优先使用移动构造
 *    - 但移动构造函数必须保证不抛异常
 *    - 因此 noexcept 是触发移动构造的重要条件！
 * 
 * 3. 接口契约
 *    - 告诉使用者：这个函数不会乱来（不抛异常）
 *    - 就像食物包装上的"不含人工添加剂"
 */

// 不抛异常的函数
void definitelySafe() noexcept {
    std::cout << "  [noexcept] 我是安全的，不会抛异常！" << std::endl;
    // 这里可以做一些"危险"的操作，但不会抛异常
}

// 可能抛异常的函数
void mightThrow() {
    throw std::runtime_error("哎呀，我抛了个异常！");
}

// 使用noexcept运算符查询函数是否会抛异常
template<typename T>
void checkNoexcept() {
    std::cout << "  [noexcept检查] ";
    std::cout << std::boolalpha;
    // 注意区分两个标准库类型 trait：
    // - std::is_nothrow_constructible：类型 T 的对象是否可构造且不抛异常
    // - std::is_nothrow_destructible：类型 T 的对象是否可析构且不抛异常
    std::cout << "is_nothrow_constructible: " 
              << std::is_nothrow_constructible<T>::value << std::endl;
    std::cout << "is_nothrow_destructible: "
              << std::is_nothrow_destructible<T>::value << std::endl;
}

int main() {
    // 使用checkNoexcept检查类型
    std::cout << "【类型检查】int 类型：" << std::endl;
    checkNoexcept<int>();
    std::cout << std::endl;
    std::cout << "=== noexcept关键字演示 ===" << std::endl;
    std::cout << "noexcept = '我保证不惹事' 宣言\n" << std::endl;
    
    // 1. 基本用法
    std::cout << "【1】noexcept基本用法" << std::endl;
    definitelySafe();  // 调用noexcept函数
    
    // 2. noexcept运算符
    // 2. noexcept运算符
    std::cout << "\n【2】noexcept运算符" << std::endl;
    std::cout << "  definitelySafe 是否承诺不抛异常？ " 
              << noexcept(definitelySafe()) << std::endl;  // 输出: true (1)
    std::cout << "  mightThrow 是否承诺不抛异常？ " 
              << noexcept(mightThrow()) << std::endl;       // 输出: false (0)
    
    // 3. 移动语义与noexcept
    std::cout << "\n【3】noexcept与移动语义" << std::endl;
    std::cout << "  移动构造函数标记为noexcept可以让vector更高效地重新分配内存\n" << std::endl;
    
    std::vector<std::string> v1;
    v1.push_back("Hello");  // 第一次：分配
    v1.push_back("World");  // 第二次：重新分配+移动
    v1.push_back("Exception");  // 第三次：再次重新分配+移动
    
    std::cout << "  vector内容：";
    for (const auto& s : v1) {
        std::cout << s << " ";
    }
    std::cout << std::endl;
    
    // 4. 自定义移动构造函数
    std::cout << "\n【4】noexcept移动构造函数的威力" << std::endl;
    
    class HeavyResource {
    private:
        int* data_;
        size_t size_;
        
    public:
        // 普通构造函数
        HeavyResource(size_t size) : data_(new int[size]), size_(size) {
            std::cout << "  [普通构造] 分配了 " << size << " 个int" << std::endl;
        }
        
        // noexcept移动构造函数 —— 推荐！
        HeavyResource(HeavyResource&& other) noexcept 
            : data_(other.data_), size_(other.size_) {
            other.data_ = nullptr;
            other.size_ = 0;
            std::cout << "  [移动构造] 资源转移（noexcept保证）" << std::endl;
        }
        
        // noexcept移动赋值运算符
        HeavyResource& operator=(HeavyResource&& other) noexcept {
            if (this != &other) {
                delete[] data_;
                data_ = other.data_;
                size_ = other.size_;
                other.data_ = nullptr;
                other.size_ = 0;
            }
            std::cout << "  [移动赋值] 资源转移（noexcept保证）" << std::endl;
            return *this;
        }
        
        ~HeavyResource() {
            delete[] data_;
            std::cout << "  [析构] 资源释放" << std::endl;
        }
    };
    
    std::cout << "  创建第一个对象..." << std::endl;
    HeavyResource r1(1000);
    
    std::cout << "\n  移动构造第二个对象..." << std::endl;
    HeavyResource r2(std::move(r1));  // 调用noexcept移动构造
    
    std::cout << "\n【noexcept总结】" << std::endl;
    std::cout << "1. 给编译器提供优化线索：'放心优化，我保证不乱跑'" << std::endl;
    std::cout << "2. 移动语义的最佳搭档：标记为noexcept的移动操作更可能被调用" << std::endl;
    std::cout << "3. 析构函数应该永远标记为noexcept（默认就是这个）" << std::endl;
    std::cout << "4. 除非你的函数真的可能抛异常，否则大胆加noexcept！\n" << std::endl;
    
    return 0;
}
```

### noexcept的深入理解

```cpp
#include <iostream>
#include <type_traits>
#include <string>

/*
 * noexcept 详解：
 * 
 * 1. noexcept(bool_expr)
 *    - 可以指定条件：noexcept(sizeof(T) < 8) 
 *    - 表示只有满足条件时才承诺不抛异常
 * 
 * 2. 隐式noexcept
 *    - 析构函数默认是noexcept的
 *    - 默认构造函数、拷贝构造、拷贝赋值默认是noexcept的
 *    - 某些constexpr函数也是隐式noexcept的
 * 
 * 3. 违反noexcept的后果
 *    - 如果noexcept函数真的抛出了异常
 *    - 会直接调用 std::terminate()
 *    - 程序直接崩溃，没有商量余地！
 */

// 有条件的noexcept
template<typename T>
struct Wrapper {
    T value;
    
    // 只有T可以被拷贝时，swap才是noexcept的
    void swap(Wrapper& other) noexcept(std::is_nothrow_copy_constructible<T>::value 
                                        && std::is_nothrow_swappable<T>::value) {
        std::swap(value, other.value);
    }
};

void demonstrateNoexceptCondition() {
    std::cout << "=== 条件noexcept ===" << std::endl;
    
    // int 是 trivially copyable 的，所以swap是noexcept的
    Wrapper<int> w1{1}, w2{2};
    std::cout << "  Wrapper<int> 的swap是noexcept的吗？ " 
              << noexcept(w1.swap(w2)) << std::endl;  // true
    
    // std::string 的swap可能抛异常（需要检查实现）
    Wrapper<std::string> ws1{"Hello"}, ws2{"World"};
    std::cout << "  Wrapper<std::string> 的swap是noexcept的吗？ " 
              << noexcept(ws1.swap(ws2)) << std::endl;  // false（可能）
}

int main() {
    std::cout << "=== noexcept深入理解 ===\n" << std::endl;
    
    demonstrateNoexceptCondition();
    
    std::cout << "\n【重要警告】" << std::endl;
    std::cout << "如果noexcept函数真的抛出了异常..." << std::endl;
    std::cout << "后果很严重！std::terminate()会被调用！" << std::endl;
    std::cout << "程序：'你骗我！我不跟你玩了！' *崩溃*" << std::endl;
    
    return 0;
}
```

## 30.7 异常规格说明（已废弃）：历史遗留的"反面教材"

### 动态异常规格的兴衰史

```cpp
#include <iostream>
#include <exception>

/*
 * 异常规格说明的"黑历史"：
 * 
 * 在 C++98/03 时代，有个叫做"动态异常规格"的东西：
 * 
 * void func() throw(std::runtime_error);  // 只能抛出runtime_error
 * void func() throw();                      // 不抛出任何异常
 * 
 * 但这货有严重问题：
 * 1. 运行时检查，性能开销大
 * 2. 如果函数抛出了不该抛的异常，调用 std::unexpected()
 * 3. std::unexpected() 默认调用 std::terminate()
 * 4. 程序员发现这玩意比不用还糟糕
 * 
 * 所以 C++11 直接把它标记为 deprecated（废弃）
 * C++17 彻底移除了动态异常规格（除了throw()，它被保留为noexcept的别名）
 * 
 * 教训：不是所有"听起来不错"的设计都是好设计！
 */

int main() {
    std::cout << "=== 异常规格说明（历史回顾） ===" << std::endl;
    std::cout << "这是一段C++的'黑历史'...\n" << std::endl;
    
    std::cout << "【C++98/03】动态异常规格" << std::endl;
    std::cout << "  void risky() throw(ExceptionType);" << std::endl;
    std::cout << "  问题：运行时检查、性能开销、吓人的std::unexpected()\n" << std::endl;
    
    std::cout << "【C++11】noexcept横空出世" << std::endl;
    std::cout << "  void safe() noexcept;" << std::endl;
    std::cout << "  优势：编译时检查、无运行时开销、语义清晰\n" << std::endl;
    
    std::cout << "【C++17】彻底告别" << std::endl;
    std::cout << "  throw() 变成了 noexcept 的别名" << std::endl;
    std::cout << "  其他动态异常规格被移除\n" << std::endl;
    
    std::cout << "【现代C++编程准则】" << std::endl;
    std::cout << "  ? 使用 noexcept 标记不抛异常的函数" << std::endl;
    std::cout << "  ? 不要使用 throw(...) 动态异常规格" << std::endl;
    std::cout << "  ? 如果函数可能抛异常，就不要加任何异常规格" << std::endl;
    std::cout << "  ? 记住：throw() 约等于 noexcept\n" << std::endl;
    
    std::cout << "【为什么废弃？】" << std::endl;
    std::cout << "  想象你写了个库，函数声明 throw(std::runtime_error)" << std::endl;
    std::cout << "  后来你想升级，函数需要抛出更多异常" << std::endl;
    std::cout << "  但你不能改声明，否则破坏二进制兼容性！" << std::endl;
    std::cout << "  于是你被自己挖的坑埋了...\n" << std::endl;
    
    std::cout << "【结论】noexcept是现代C++的唯一选择！" << std::endl;
    
    return 0;
}
```

### throw() vs noexcept

```cpp
#include <iostream>

/*
 * throw() 和 noexcept 的区别：
 * 
 * 相同点：
 * - 都表示函数不会抛出异常
 * - 违反时都调用 std::terminate()
 * 
 * 不同点：
 * - throw() 是旧的动态异常规格（C++98）
 * - noexcept 是新的编译时规格（C++11）
 * - throw() 会在运行时做一些额外检查（有轻微开销）
 * - noexcept 是纯编译时声明（零运行时开销）
 * 
 * 现代代码应该使用 noexcept
 */

void oldStyle() throw() {  // C++98风格，等同于noexcept
    std::cout << "  oldStyle() - throw()声明" << std::endl;
}

void newStyle() noexcept {  // C++11风格，推荐
    std::cout << "  newStyle() - noexcept声明" << std::endl;
}

int main() {
    std::cout << "=== throw() vs noexcept ===\n" << std::endl;
    
    std::cout << "【结论】在C++17及以后，throw()就是noexcept的语法糖" << std::endl;
    std::cout << "但为了代码清晰和符合现代C++风格，请使用 noexcept！\n" << std::endl;
    
    oldStyle();
    newStyle();
    
    return 0;
}
```

## 30.8 std::expected错误处理（C++23）：不用异常的"备胎方案"

### 为什么要std::expected？

```cpp
#include <iostream>
#include <expected>  // C++23
#include <string>
#include <optional>

/*
 * std::expected：C++23引入的"错误处理神器"
 * 
 * 问题：异常虽好，但有以下问题：
 * 1. 性能开销：抛出和捕获异常有成本
 * 2. 不可忽视的异常：有些场景下异常是不可接受的
 * 3. 错误处理不明确：调用者可能忘记处理异常
 * 
 * 解决方案：
 * 1. 返回错误码 —— 可行但丑陋
 * 2. std::optional —— 只能表示"有无"，不能带错误信息
 * 3. std::expected —— 结合两者优点！
 * 
 * std::expected<T, E> 语义：
 * - 要么包含一个 T 类型的值
 * - 要么包含一个 E 类型的错误
 * - 调用者必须检查！编译器的"强制性"比异常更直接
 */

// 使用std::expected的除法函数
// 返回值要么是正确结果（int），要么是错误信息（std::string）
std::expected<int, std::string> safeDivide(int a, int b) {
    if (b == 0) {
        // 返回错误：用 std::unexpected 包装错误值
        return std::unexpected("Division by zero! Even calculators give up!");
    }
    return a / b;  // 返回正确值
}

// 模拟文件读取
std::expected<std::string, std::string> readFile(const std::string& filename) {
    if (filename.empty()) {
        return std::unexpected("Filename cannot be empty!");
    }
    if (filename == "nonexistent.txt") {
        return std::unexpected("File not found: " + filename);
    }
    if (filename == "forbidden.txt") {
        return std::unexpected("Permission denied: " + filename);
    }
    return "File content: Hello from " + filename;  // 模拟读取成功
}

int main() {
    std::cout << "=== std::expected错误处理（C++23） ===" << std::endl;
    std::cout << "这是异常处理的'备胎方案' —— 不用异常也能优雅地处理错误\n" << std::endl;
    
    // 1. 基本用法
    std::cout << "【1】safeDivide的基本用法" << std::endl;
    
    // 成功情况
    auto result1 = safeDivide(10, 2);
    if (result1.has_value()) {  // 或者简单地：if (result1)
        std::cout << "  10 / 2 = " << result1.value() << std::endl;
        // 也可以直接解引用：*result1
        std::cout << "  直接解引用：*result1 = " << *result1 << std::endl;
        // 输出: 10 / 2 = 5
        // 输出: 直接解引用：*result1 = 5
    }
    
    // 失败情况
    auto result2 = safeDivide(10, 0);
    if (!result2.has_value()) {
        std::cout << "  10 / 0 = 错误: " << result2.error() << std::endl;
        // 输出: 10 / 0 = 错误: Division by zero! Even calculators give up!
    }
    
    std::cout << "\n【2】使用value_or提供默认值" << std::endl;
    auto result3 = safeDivide(10, 0);
    int safeValue = result3.value_or(-1);  // 如果失败，返回-1作为默认值
    std::cout << "  安全值（失败时返回-1）：" << safeValue << std::endl;
    // 输出: 安全值（失败时返回-1）：-1
    
    std::cout << "\n【3】and_then链式操作（函数式风格）" << std::endl;
    // 假设我们要做 (10 / 2) * 3
    auto step1 = safeDivide(10, 2);
    if (step1) {
        int intermediate = *step1 * 3;
        std::cout << "  (10 / 2) * 3 = " << intermediate << std::endl;
        // 输出: (10 / 2) * 3 = 15
    }
    
    std::cout << "\n【4】map转换结果类型" << std::endl;
    // 将int结果转换为string描述
    auto result4 = safeDivide(20, 4);
    if (result4) {
        auto description = result4.map([](int v) {
            return "The result is: " + std::to_string(v);
        });
        std::cout << "  " << *description << std::endl;
        // 输出: The result is: 5
    }
    
    std::cout << "\n【5】map_error转换错误类型" << std::endl;
    auto result5 = safeDivide(10, 0);
    if (!result5) {
        // 将错误从string转换为int错误码
        auto errorCode = result5.map_error([](const std::string& err) {
            if (err.find("zero") != std::string::npos) {
                return -1;  // 除零错误码
            }
            return -999;  // 未知错误码
        });
        std::cout << "  错误码： " << errorCode.error() << std::endl;
        // 输出: 错误码： -1
    }
    
    std::cout << "\n【6】文件读取示例" << std::endl;
    std::cout << "  读取 'example.txt'..." << std::endl;
    auto file1 = readFile("example.txt");
    std::cout << "  结果: " << (file1 ? *file1 : "错误: " + file1.error()) << std::endl;
    // 输出: 结果: File content: Hello from example.txt
    
    std::cout << "  读取 'nonexistent.txt'..." << std::endl;
    auto file2 = readFile("nonexistent.txt");
    std::cout << "  结果: " << (file2 ? *file2 : "错误: " + file2.error()) << std::endl;
    // 输出: 结果: 错误: File not found: nonexistent.txt
    
    std::cout << "\n【std::expected vs 异常】" << std::endl;
    std::cout << "┌────────────────┬────────────────────┐" << std::endl;
    std::cout << "│    std::expected    │       异常         │" << std::endl;
    std::cout << "├────────────────┼────────────────────┤" << std::endl;
    std::cout << "│ 编译时知道错误  │ 运行时发现错误     │" << std::endl;
    std::cout << "│ 必须检查返回值  │ 可以忽略（危险）   │" << std::endl;
    std::cout << "│ 无性能开销      │ 有性能开销         │" << std::endl;
    std::cout << "│ 适合频繁错误    │ 适合罕见错误       │" << std::endl;
    std::cout << "│ C++23可用       │ C++98就支持        │" << std::endl;
    std::cout << "└────────────────┴────────────────────┘" << std::endl;
    
    std::cout << "\n【总结】std::expected是异常的安全替代品！" << std::endl;
    std::cout << "想象异常是'大喊大叫的报警器'" << std::endl;
    std::cout << "那std::expected就是'安静的返回值' —— 礼貌但必须处理！" << std::endl;
    
    return 0;
}
```

### std::expected的深入用法

```cpp
#include <iostream>
#include <expected>
#include <string>

/*
 * std::expected 高级用法：
 * 
 * 1. and_then：链式处理成功值
 * 2. map：转换成功值
 * 3. map_error：转换错误值
 * 4. transform：类似map但用于optional语义
 * 5. or_else：处理错误情况
 */

// 更复杂的例子：嵌套的expected
std::expected<std::expected<int, std::string>, std::string> complexDivide(int a, int b) {
    if (b == 0) {
        return std::unexpected("Division by zero!");
    }
    return safeDivide(a, b);  // 返回 std::expected<int, std::string>
}

// 但实际上，我们更应该flatten：
// std::expected<int, std::string> 就够了

int main() {
    std::cout << "=== std::expected深入用法 ===\n" << std::endl;
    
    // 使用 and_then 进行链式操作
    std::cout << "【and_then链式操作】" << std::endl;
    std::cout << "  场景：计算 ((100 / 2) / 5) / 2\n" << std::endl;
    
    auto step1 = safeDivide(100, 2);
    if (step1) {
        auto step2 = safeDivide(*step1, 5);
        if (step2) {
            auto step3 = safeDivide(*step2, 2);
            if (step3) {
                std::cout << "  最终结果： " << *step3 << std::endl;
                // 输出: 最终结果： 10
            }
        }
    }
    
    // 更优雅的写法（需要C++23的and_then）
    // 等价于上面的嵌套if
    // auto final = safeDivide(100, 2)
    //                 .and_then([](int v) { return safeDivide(v, 5); })
    //                 .and_then([](int v) { return safeDivide(v, 2); });
    
    std::cout << "\n【直接检查模式】" << std::endl;
    auto r = safeDivide(42, 0);
    if (!r) {
        std::cout << "  计算失败：" << r.error() << std::endl;
        // 输出: 计算失败：Division by zero! Even calculators give up!
    }
    
    std::cout << "\n【结论】std::expected让错误处理变得显式而可控！" << std::endl;
    
    return 0;
}
```

## 30.9 异常处理最佳实践：老司机的血泪经验

### 何时使用异常

```cpp
#include <iostream>
#include <stdexcept>
#include <fstream>
#include <string>

/*
 * 异常使用指南：
 * 
 * ? 应该使用异常的情况：
 *   - 真正异常的情况（文件找不到、网络断开）
 *   - 构造函数失败
 *   - 不应该用返回码表示的错误
 *   - 跨调用栈传播错误
 * 
 * ? 不应该使用异常的情况：
 *   - 可预期的错误（用户输入无效）
 *   - 性能关键路径
 *   - 需要频繁处理的错误
 *   - 可以通过检查参数避免的错误
 */

class FileReader {
private:
    std::string filename_;
    std::ifstream file_;
    
public:
    // 构造函数失败应该用异常
    // 因为构造函数不能返回值
    FileReader(const std::string& filename) : filename_(filename) {
        file_.open(filename);
        if (!file_.is_open()) {
            // 文件打不开？抛异常！因为这通常是真正的异常情况
            throw std::runtime_error("Cannot open file: " + filename);
        }
        std::cout << "  文件打开成功: " << filename << std::endl;
    }
    
    // 普通成员函数：可以用异常也可以不用
    // 取决于错误类型
    bool readLine(std::string& out) {
        if (!std::getline(file_, out)) {
            // 读取失败：可能是EOF，也可能是错误
            // 这里返回false更合适，因为EOF不是异常情况
            return false;
        }
        return true;
    }
};

// 验证用户输入：不应该用异常
bool validateUsername(const std::string& username) {
    // 可预期的错误：用户输入无效
    // 用返回值/错误码更合适
    if (username.empty()) {
        return false;  // 返回false表示验证失败
    }
    if (username.length() < 3) {
        return false;
    }
    if (username.length() > 20) {
        return false;
    }
    return true;
}

int main() {
    std::cout << "=== 何时使用异常 ===" << std::endl;
    std::cout << "异常使用的基本原则：'例外'才用异常\n" << std::endl;
    
    // 场景1：构造函数失败 -> 用异常
    std::cout << "【场景1】构造函数失败 -> 应该用异常" << std::endl;
    try {
        FileReader reader("C:/windows/system.ini");  // 这个文件应该存在
        std::string line;
        if (reader.readLine(line)) {
            std::cout << "  读取到: " << line.substr(0, 50) << "..." << std::endl;
        }
    } catch (const std::exception& e) {
        std::cout << "  捕获异常: " << e.what() << std::endl;
    }
    
    // 场景2：用户输入验证 -> 不用异常
    std::cout << "\n【场景2】用户输入验证 -> 不用异常" << std::endl;
    std::string badUsername = "";
    if (!validateUsername(badUsername)) {
        std::cout << "  用户名无效（这是可预期的，用返回码处理）" << std::endl;
        // 输出: 用户名无效（这是可预期的，用返回码处理）
    }
    
    std::string goodUsername = "Alice123";
    if (validateUsername(goodUsername)) {
        std::cout << "  用户名'" << goodUsername << "'验证通过" << std::endl;
        // 输出: 用户名'Alice123'验证通过
    }
    
    std::cout << "\n【异常使用决策树】" << std::endl;
    std::cout << "┌─────────────────────────────────────────────┐" << std::endl;
    std::cout << "│           这个错误是'真正的异常'吗？           │" << std::endl;
    std::cout << "│                                             │" << std::endl;
    std::cout << "│  是（比如文件丢失、网络断开）                  │" << std::endl;
    std::cout << "│    ↓                                        │" << std::endl;
    std::cout << "│  用异常                                     │" << std::endl;
    std::cout << "│                                             │" << std::endl;
    std::cout << "│  否（可预期、能通过检查避免）                  │" << std::endl;
    std::cout << "│    ↓                                        │" << std::endl;
    std::cout << "│  用返回值/错误码                             │" << std::endl;
    std::cout << "└─────────────────────────────────────────────┘" << std::endl;
    
    return 0;
}
```

### 异常与错误码的选择

```cpp
#include <iostream>
#include <expected>
#include <string>
#include <variant>

/*
 * 异常 vs 错误码 vs std::expected 选择指南：
 * 
 * ┌─────────────┬────────────────────────────────────────────────────────┐
 * │   异常       │ ? 罕见、严重、无法提前预知的错误                         │
 * │             │ ? 需要跨多层调用栈传播                                   │
 * │             │ ? 调用者不知道如何处理，让调用者决定                       │
 * │             │ 例子：文件找不到、内存分配失败、严重的数据损坏              │
 * ├─────────────┼────────────────────────────────────────────────────────┤
 * │   错误码     │ ? 频繁、可预期、调用者知道如何处理                        │
 * │             │ ? 只需要返回给直接调用者                                 │
 * │             │ ? 性能关键路径（但现代CPU上这个差异很小）                  │
 * │             │ 例子：参数验证、简单的越界检查                            │
 * ├─────────────┼────────────────────────────────────────────────────────┤
 * │ std::expected│ ? 介于两者之间                                          │
 * │  (C++23)    │ ? 需要返回有意义的结果或错误                             │
 * │             │ ? 调用者必须处理（编译期强制）                            │
 * │             │ 例子：解析结果、数学运算结果                              │
 * └─────────────┴────────────────────────────────────────────────────────┘
 */

// 用错误码的处理方式（古老的C风格）
enum class ErrorCode {
    Success,
    InvalidInput,
    OutOfRange,
    NotFound
};

ErrorCode divideWithErrorCode(int a, int b, int& result) {
    if (b == 0) {
        return ErrorCode::InvalidInput;
    }
    result = a / b;
    return ErrorCode::Success;
}

// 用std::expected的处理方式（现代C++风格）
std::expected<int, std::string> divideWithExpected(int a, int b) {
    if (b == 0) {
        return std::unexpected("Division by zero");
    }
    return a / b;
}

int main() {
    std::cout << "=== 异常 vs 错误码 vs std::expected ===" << std::endl;
    std::cout << "选择正确的错误处理方式，就像选择正确的交通工具\n" << std::endl;
    
    // 错误码风格
    std::cout << "【1】错误码风格（C风格）" << std::endl;
    int result1 = 0;
    ErrorCode err1 = divideWithErrorCode(10, 2, result1);
    if (err1 == ErrorCode::Success) {
        std::cout << "  结果: " << result1 << std::endl;
        // 输出: 结果: 5
    }
    
    ErrorCode err2 = divideWithErrorCode(10, 0, result1);
    if (err2 != ErrorCode::Success) {
        std::cout << "  错误: " << static_cast<int>(err2) << std::endl;
    }
    
    // std::expected风格
    std::cout << "\n【2】std::expected风格（现代C++）" << std::endl;
    auto result3 = divideWithExpected(10, 2);
    if (result3) {
        std::cout << "  结果: " << *result3 << std::endl;
        // 输出: 结果: 5
    }
    
    auto result4 = divideWithExpected(10, 0);
    if (!result4) {
        std::cout << "  错误: " << result4.error() << std::endl;
        // 输出: 错误: Division by zero
    }
    
    std::cout << "\n【3】异常风格（传统C++）" << std::endl;
    try {
        // 模拟除法操作
        auto result5 = divideWithExpected(10, 2);
        if (result5) {
            std::cout << "  结果: " << *result5 << std::endl;
        }
    } catch (const std::exception& e) {
        std::cout << "  错误: " << e.what() << std::endl;
    }
    
    std::cout << "\n【最佳实践总结】" << std::endl;
    std::cout << "1. 库和基础设施代码：优先使用异常" << std::endl;
    std::cout << "2. 应用代码：根据场景选择" << std::endl;
    std::cout << "3. 性能关键代码：考虑std::expected或错误码" << std::endl;
    std::cout << "4. 用户输入验证：使用错误码或返回值" << std::endl;
    std::cout << "5. 跨平台代码：注意异常禁用的情况（如某些嵌入式环境）" << std::endl;
    std::cout << "6. 现代C++23项目：优先考虑std::expected" << std::endl;
    
    return 0;
}
```

### 异常安全编程的"葵花宝典"

```cpp
#include <iostream>
#include <vector>
#include <memory>
#include <string>

/*
 * 异常安全编程的七条黄金法则：
 * 
 * 1. RAII是基础
 *    - 用智能指针管理资源
 *    - 析构函数永不抛异常
 * 
 * 2. 构造失败要抛异常
 *    - 构造函数没有返回值
 *    - 失败时只能抛异常
 * 
 * 3. 赋值运算符要提供异常安全
 *    - 使用copy-and-swap idiom
 *    - 或者分两步：先拷贝构造，再swap
 * 
 * 4. 移动比拷贝更安全
 *    - 移动通常不抛异常（如果实现了的话）
 *    - push_back优先使用移动
 * 
 * 5. 了解容器的异常安全保证
 *    - vector::push_back 提供强保证（如果移动不抛异常）
 *    - vector::emplace 提供类似保证
 * 
 * 6. 清理顺序要正确
 *    - 资源按构造的反序释放
 *    - 使用scope guard确保清理
 * 
 * 7. 测试异常路径
 *    - 单元测试要覆盖异常情况
 *    - 混沌测试：随机触发异常
 */

// 法则1：RAII
class Resource {
public:
    Resource() { std::cout << "  [Resource] 分配资源" << std::endl; }
    ~Resource() { std::cout << "  [Resource] 释放资源（析构函数不抛异常！）" << std::endl; }
};

// 法则2：构造函数失败抛异常
class ComplexObject {
private:
    std::unique_ptr<Resource> resource_;
    std::vector<int> data_;
    
public:
    ComplexObject(size_t size) : resource_(std::make_unique<Resource>()) {
        // 如果这里抛异常，resource_的析构会被调用
        // 资源不会泄漏
        if (size > 1000000) {
            throw std::length_error("Size too large!");
        }
        data_.resize(size);
        std::cout << "  [ComplexObject] 构造成功" << std::endl;
    }
    
    ~ComplexObject() {
        std::cout << "  [ComplexObject] 析构" << std::endl;
    }
};

int main() {
    std::cout << "=== 异常安全编程最佳实践 ===" << std::endl;
    std::cout << "遵循这些法则，让你的代码坚如磐石！\n" << std::endl;
    
    // 测试RAII
    std::cout << "【法则1】RAII保证资源安全" << std::endl;
    try {
        ComplexObject obj(100);
        std::cout << "  创建对象成功" << std::endl;
        // obj使用中...
        throw std::runtime_error("模拟异常");
    } catch (const std::exception& e) {
        std::cout << "  捕获异常: " << e.what() << std::endl;
        std::cout << "  资源已自动释放（RAII的功劳！）" << std::endl;
    }
    
    std::cout << "\n【法则3】赋值运算符的异常安全" << std::endl;
    std::cout << "  使用copy-and-swap idiom确保强异常安全\n" << std::endl;
    
    std::vector<int> v1{1, 2, 3};
    std::vector<int> v2{4, 5, 6};
    std::cout << "  v1 = {1, 2, 3}, v2 = {4, 5, 6}" << std::endl;
    
    // swap是noexcept的，所以赋值操作有强保证
    v1.swap(v2);
    std::cout << "  swap后: v1 = {" << v1[0] << ", " << v1[1] << ", " << v1[2] << "}" << std::endl;
    // 输出: v1 = {4, 5, 6}
    
    std::cout << "\n【总结】异常安全编程的精髓" << std::endl;
    std::cout << "1. 相信RAII，它是你最忠实的朋友" << std::endl;
    std::cout << "2. 记住：析构函数、swap、移动操作应该是noexcept的" << std::endl;
    std::cout << "3. 设计类时考虑异常安全性，这是一种责任" << std::endl;
    std::cout << "4. 测试异常路径，确保代码在'天灾人祸'下依然安全\n" << std::endl;
    
    std::cout << "【最后的话】" << std::endl;
    std::cout << "异常处理就像汽车的安全气囊：" << std::endl;
    std::cout << "希望你永远不需要用到，但万一需要时，它必须能正常工作！" << std::endl;
    
    return 0;
}
```

## 本章小结

### 核心概念回顾

| 概念         | 说明                 | 关键字                     |
| ------------ | -------------------- | -------------------------- |
| **异常**     | 程序执行中的意外事件 | `throw`                    |
| **抛出异常** | 发出"求救信号"       | `throw expression`         |
| **捕获异常** | 接收并处理异常       | `catch (exception_type e)` |
| **try块**    | 监视异常的代码区域   | `try { ... }`              |

### 异常处理三步曲

```
┌─────────┐     throw      ┌─────────┐     catch      ┌─────────┐
│  抛出   │ ──────────────?│  捕获   │ ──────────────?│  处理   │
└─────────┘                └─────────┘                └─────────┘
     │                          │                          │
     ▼                          ▼                          ▼
  发出求救              寻找匹配的catch          优雅地处理错误
```

### 标准异常类层次

```
std::exception（所有异常的老祖宗）
├── std::logic_error（程序员能预防的）
│   ├── std::domain_error
│   ├── std::invalid_argument
│   ├── std::length_error
│   └── std::out_of_range
├── std::runtime_error（运行时才暴露的）
│   ├── std::overflow_error
│   ├── std::underflow_error
│   └── std::range_error
├── std::bad_alloc（内存分配失败）
├── std::bad_cast（类型转换失败）
└── std::bad_typeid（typeid失败）
```

### 异常安全三兄弟

| 保证级别         | 承诺                     | 比喻                           |
| ---------------- | ------------------------ | ------------------------------ |
| **基本保证**     | 资源不泄漏               | 厕所用完要冲水                 |
| **强保证**       | 要么成功，要么当没发生过 | 原子弹发射失败，弹头不会掉下来 |
| **不抛异常保证** | 永远不会抛异常           | 僵尸末日时的诺亚方舟           |

### noexcept vs 异常

| 特性     | noexcept           | 异常             |
| -------- | ------------------ | ---------------- |
| 出现版本 | C++11              | C++98            |
| 性能开销 | 零（编译时检查）   | 有（栈展开）     |
| 强制性   | 编译器强制检查     | 可忽略（危险！） |
| 适用场景 | 绝对不抛异常的函数 | 真正的异常情况   |

### std::expected（C++23）

```cpp
std::expected<int, std::string> divide(int a, int b) {
    if (b == 0) return std::unexpected("Division by zero");
    return a / b;
}

// 使用
auto result = divide(10, 2);
if (result) std::cout << *result << std::endl;
else std::cout << result.error() << std::endl;
```

### 最佳实践一句话总结

1. **能用RAII解决的不抛异常**
2. **构造函数失败要抛异常**
3. **析构函数永不抛异常**
4. **移动操作要noexcept**
5. **可预期错误用返回值，罕见错误用异常**
6. **C++23时代，优先考虑std::expected**

---

> "好的代码在正常情况和异常情况下都能正确工作。伟大的代码在异常情况下优雅地失败。"
>
> 祝大家在C++的海洋里乘风破浪，永远不要catch到意料之外的异常！ ??