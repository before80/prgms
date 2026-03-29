+++
title = "第36章 测试与调试：让你的代码从"能用"到"靠谱""
weight = 360
date = "2026-03-29T21:03:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++
# 第36章 测试与调试：让你的代码从"能用"到"靠谱"

> *"调试（debugging）这个名字来源于一只真正的bug——1947年，一只飞蛾被卡在Harvard Mark II的继电器里，导致系统故障。程序员Grace Hopper和她团队把那只蛾子贴在了日志本上，还写道："First actual case of bug being found." 从此，"debug"这个词就诞生了。所以下次你对着屏幕debug到凌晨三点时，至少你可以告诉自己：你在追随Grace Hopper的足迹——只不过那只飞蛾是看不见的。"*
> —— 编程野史（Programming Folklore）

## 36.1 为什么测试和调试如此重要

你知道软件开发中最大的讽刺是什么吗？**一个经验丰富的程序员，最引以为傲的技能，往往是他们花时间最多的技能**——也就是修复bug。没有人会在简历上写"擅长写bug然后花三周找它"，但事实是，每个程序员每天都在和bug搏斗。

C++更是bug的重灾区。指针操作、内存管理、模板元编程的诡异报错、undefined behavior的玄学表现……可以说，C++是那种"给你足够自由，然后让你为自由付出代价"的语言。

本章我们将讨论：
- 如何通过**测试**在代码写完之前就抓住bug（主动防御）
- 如何通过**调试**在bug出现后高效定位它（事后补救）
- 两者结合，让你的代码从"祈祷它能跑"进化到"我知道它能跑"

### 36.1.1 测试 vs 调试：先分清这对兄弟

很多初学者把测试和调试混为一谈，理由是"都是让代码出问题嘛"。错！它们的区别就像**预防医学**和**急诊室**的区别：

| 维度 | 测试 (Testing) | 调试 (Debugging) |
|------|--------------|-----------------|
| **时机** | bug出现之前 | bug出现之后 |
| **目的** | 验证功能正确性，发现缺陷 | 定位缺陷根因，修复之 |
| **方法** | 设计测试用例，执行测试 | 分析症状，使用工具追踪 |
| **心态** | "我要证明代码有问题" | "我已知有问题，我要找它" |
| **自动化** | 高度自动化，可重复 | 往往需要人工介入 |

简单说：**测试是质量门卫，调试是故障维修**。优秀的项目有强大的测试覆盖，让调试变成稀有事件；糟糕的项目几乎不写测试，调试成了日常——就像一个人从不做体检，只等病倒了去急诊。

### 36.1.2 C++测试的现状：好消息与坏消息

**好消息**：C++生态中有大量优秀的测试框架：
- **Google Test (gtest)**：工业级标准，Google出品必属精品
- **Catch2**：现代C++14/17编写，语法简洁到令人发指
- **Boost.Test**：Boost大家庭成员，适合Boost重度用户
- **Doctest**：号称"最轻量的C++测试框架"，编译速度极快

**坏消息**：很多C++项目（特别是老项目）几乎没有任何测试。原因是多方面的：
1. C++项目往往历史悠久（遗产代码），加测试的成本高
2. 很多C++程序员是"硬核派"，觉得写测试是"软蛋才干的事"
3. C++的某些特性（如模板、宏、条件编译）让测试有一定门槛

好消息是，现在C++20/23引入了更多元编程工具，测试框架也越来越现代化，这个状况正在改善。

## 36.2 单元测试：最小单位的质量守护

### 36.2.1 什么是单元测试？

**单元测试（Unit Testing）**是对软件中的**最小可测试单元**进行验证。在C++中，这个最小单元通常是**一个函数**或**一个类的方法**。

单元测试的核心原则：
- **Isolation（隔离）**：每个测试独立运行，不依赖其他测试
- **Repeatability（可重复）**：同样的测试，跑了1000次结果都一样
- **Fast（快速）**：一个单元测试通常毫秒级完成
- **Self-contained（自包含）**：测试自己设置数据，自己清理资源

```cpp
// 不经过单元测试的代码 vs 经过单元测试的代码
// 区别就像:
// 没测试: "我确信这段代码是对的" —— 盲目自信
// 有测试: "我证明了这段代码是对的" —— 证据说话
```

### 36.2.2 手写单元测试：最原始也最直接的开始

在有测试框架之前，人们是怎么测代码的？—— 用`main`函数！虽然土，但理解这个过程很重要：

```cpp
// math_utils.h
#pragma once

int add(int a, int b) {
    return a + b;
}

int divide(int a, int b) {
    if (b == 0) {
        throw std::runtime_error("Division by zero");
    }
    return a / b;
}

// factorial 函数（正确实现）
int factorial(int n) {
    if (n < 0) {
        throw std::invalid_argument("Negative input");
    }
    int result = 1;
    for (int i = 2; i <= n; ++i) {
        result *= i;
    }
    return result;
}

// 手动测试驱动开发（TDD）—— 先写测试再写实现
int main() {
    // 测试 add
    if (add(2, 3) != 5) {
        std::cerr << "FAIL: add(2, 3) expected 5" << std::endl;
        return 1;
    }
    if (add(-1, 1) != 0) {
        std::cerr << "FAIL: add(-1, 1) expected 0" << std::endl;
        return 1;
    }
    std::cout << "PASS: add tests" << std::endl;

    // 测试 divide
    if (divide(10, 2) != 5) {
        std::cerr << "FAIL: divide(10, 2) expected 5" << std::endl;
        return 1;
    }
    try {
        divide(10, 0);
        std::cerr << "FAIL: divide(10, 0) should throw" << std::endl;
        return 1;
    } catch (const std::runtime_error&) {
        std::cout << "PASS: divide exception test" << std::endl;
    }

    // 测试 factorial
    if (factorial(5) != 120) {
        std::cerr << "FAIL: factorial(5) expected 120, got " << factorial(5) << std::endl;
        return 1;
    }
    std::cout << "PASS: factorial(5) = 120" << std::endl;

    std::cout << "\nAll manual tests passed!" << std::endl;
    return 0;
}
```

**问题在哪？** 这种手写测试：
1. 没法自动化运行（需要人眼盯着）
2. 没有汇总报告
3. 测试多了`main`函数会爆炸
4. 没有隔离——一个失败可能导致其他测试也失败

所以，**请使用专业的测试框架**。

### 36.2.3 Google Test：工业级测试框架

Google Test（gtest）是C++世界最流行的测试框架。它的设计哲学是：**测试应该是独立的、可组合的、可读的**。

#### 安装与引入

```bash
# 使用 vcpkg 安装
vcpkg install gtest

# 或者下载源码编译
git clone https://github.com/google/googletest.git
cd googletest && cmake -B build && cmake --build build
```

#### Google Test快速上手

```cpp
// gtest_demo.cpp
#include <gtest/gtest.h>
#include <gmock/gmock.h>

// 被测试的代码
int add(int a, int b) {
    return a + b;
}

double divide(double a, double b) {
    if (b == 0.0) {
        throw std::runtime_error("Division by zero");
    }
    return a / b;
}

std::string greet(const std::string& name) {
    if (name.empty()) {
        return "Hello, Stranger!";
    }
    return "Hello, " + name + "!";
}

// ========== 测试用例 ==========

// TEST(测试套件名, 测试用例名)
// 套件名和用例名必须是有效的C++标识符（不能有空格）
TEST(MathBasic, AddPositive) {
    EXPECT_EQ(add(2, 3), 5);
    EXPECT_EQ(add(0, 0), 0);
    EXPECT_EQ(add(-5, 5), 0);
}

TEST(MathBasic, AddBoundary) {
    EXPECT_EQ(add(INT_MAX, 0), INT_MAX);
    EXPECT_EQ(add(INT_MIN, 0), INT_MIN);
    // 注意：add(INT_MAX, 1) 会溢出，这是undefined behavior
    // 在测试中我们要么避开边界，要么明确知道溢出行为
}

TEST(MathBasic, Divide) {
    EXPECT_DOUBLE_EQ(divide(10.0, 2.0), 5.0);
    EXPECT_DOUBLE_EQ(divide(1.0, 3.0), 1.0 / 3.0);  // divide返回1.0/3.0，与字面量1.0/3.0比较；注意两者求值路径可能不同，这里仅作示例
}

TEST(MathBasic, DivideByZero) {
    // EXPECT_THROW: 期望抛出指定异常
    EXPECT_THROW(divide(10.0, 0.0), std::runtime_error);
    // EXPECT_ANY_THROW: 期望抛出任何异常
    EXPECT_ANY_THROW(divide(1.0, 0.0));
}

TEST(StringUtil, Greet) {
    EXPECT_EQ(greet("World"), "Hello, World!");
    EXPECT_EQ(greet("C++"), "Hello, C++!");
}

TEST(StringUtil, GreetEmpty) {
    EXPECT_EQ(greet(""), "Hello, Stranger!");
}

// ========== 测试夹具（Fixture）==========
// 当多个测试需要共享相同的数据设置时，使用TEST_F

class StackTest : public ::testing::Test {
protected:
    // SetUp: 每个测试用例运行前调用
    void SetUp() override {
        stack.push(1);
        stack.push(2);
        stack.push(3);
    }

    // TearDown: 每个测试用例运行后调用
    void TearDown() override {
        // 清理资源（如果需要）
    }

    std::stack<int> stack;
};

TEST_F(StackTest, InitialSize) {
    EXPECT_EQ(stack.size(), 3);
}

TEST_F(StackTest, Pop) {
    stack.pop();
    EXPECT_EQ(stack.size(), 2);
    EXPECT_EQ(stack.top(), 2);
}

TEST_F(StackTest, PopAll) {
    while (!stack.empty()) {
        stack.pop();
    }
    EXPECT_TRUE(stack.empty());
}

// ========== 参数化测试 ==========
// 当你需要用不同参数测试同一个逻辑时

class IsPrimeTest : public ::testing::TestWithParam<int> {
};

// 被测试函数
bool isPrime(int n) {
    if (n < 2) return false;
    for (int i = 2; i <= std::sqrt(n); ++i) {
        if (n % i == 0) return false;
    }
    return true;
}

TEST_P(IsPrimeTest, CheckPrimes) {
    int n = GetParam();
    EXPECT_TRUE(isPrime(n)) << "Failed for n = " << n;
}

// 定义测试参数
INSTANTIATE_TEST_SUITE_P(
    PrimeValues,
    IsPrimeTest,
    ::testing::Values(2, 3, 5, 7, 11, 13, 17, 19, 23, 29)
);

INSTANTIATE_TEST_SUITE_P(
    NonPrimeValues,
    IsPrimeTest,
    ::testing::Values(0, 1, 4, 6, 8, 9, 10, 12, 15)
);

int main(int argc, char **argv) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}
```

编译运行：
```bash
g++ -std=c++17 gtest_demo.cpp -lgtest -lgtest_main -pthread -o gtest_demo
./gtest_demo
```

输出示例：
```
[==========] Running 13 tests from 3 test suites.
[----------] Global test environment set-up.
[----------] 3 tests from MathBasic
[----------] 3 tests from MathBasic (0 ms total)
[----------] 2 tests from StringUtil
[----------] 2 tests from StringUtil (0 ms total)
...
[----------] 13 tests from 3 test suites. (0 ms total)
[==========] 13 tests from 3 test suites ran. (0 ms total)
[  PASSED  ] 13 tests.
```

#### Google Test核心断言宏

Google Test提供了丰富的断言宏，分为两类：

**致命断言**（返回后当前函数立即终止）：
- `ASSERT_EQ(val1, val2)`
- `ASSERT_NE(val1, val2)`
- `ASSERT_TRUE(condition)`
- `ASSERT_FALSE(condition)`
- `ASSERT_THROW(statement, exception_type)`

**非致命断言**（失败后继续执行）：
- `EXPECT_EQ(val1, val2)`
- `EXPECT_NE(val1, val2)`
- `EXPECT_TRUE(condition)`
- `EXPECT_FALSE(condition)`
- `EXPECT_THROW(statement, exception_type)`

**原则**：能用`EXPECT_*`就不用`ASSERT_*`，除非你确定失败后继续没有意义。

**浮点数比较**：
```cpp
EXPECT_DOUBLE_EQ(a, b);      // 精度约15位
EXPECT_FLOAT_EQ(a, b);       // 精度约7位
EXPECT_NEAR(a, b, abs_error); // 允许绝对误差
```

### 36.2.4 Catch2：现代C++的优雅测试

Catch2是一个现代的C++测试框架（官方自称"modern test framework for C++14+"），它的设计目标是**最小化测试代码的视觉噪音**。

```cpp
// catch2_demo.cpp
#define CATCH_CONFIG_MAIN
#include <catch2/catch_test_macros.hpp>
#include <catch2/catch_approx.hpp>

int add(int a, int b) { return a + b; }
int subtract(int a, int b) { return a - b; }

using Catch::Approx;

// ========== 基本测试 ==========

TEST_CASE("add function", "[math]") {
    REQUIRE(add(2, 3) == 5);
    REQUIRE(add(-1, 1) == 0);
    REQUIRE(add(0, 0) == 0);
}

TEST_CASE("subtract function", "[math]") {
    CHECK(subtract(5, 3) == 2);
    CHECK(subtract(3, 5) == -2);
    CHECK(subtract(0, 0) == 0);
}

// ========== SECTION: 共享setup的不同路径 ==========

struct StatResult {
    int sum;
    double average;
};

StatResult calcStats(const std::vector<int>& vals) {
    if (vals.empty()) {
        return {0, 0.0};
    }
    int sum = 0;
    for (int v : vals) sum += v;
    return {sum, static_cast<double>(sum) / vals.size()};
}

TEST_CASE("calcStats", "[stats]") {
    StatResult r;

    SECTION("empty vector") {
        r = calcStats({});
        CHECK(r.sum == 0);
        CHECK(r.average == 0.0);
    }

    SECTION("single element") {
        r = calcStats({42});
        CHECK(r.sum == 42);
        CHECK(r.average == 42.0);
    }

    SECTION("multiple elements") {
        r = calcStats({1, 2, 3, 4, 5});
        CHECK(r.sum == 15);
        CHECK(r.average == 3.0);
    }

    SECTION("negative numbers") {
        r = calcStats({-5, -3, -1});
        CHECK(r.sum == -9);
        CHECK(r.average == Approx(-3.0));
    }
}

// ========== 浮点数近似比较 ==========

double quadraticRoot(double a, double b, double c) {
    double discriminant = b * b - 4 * a * c;
    if (discriminant < 0) return 0;
    return (-b + std::sqrt(discriminant)) / (2 * a);
}

TEST_CASE("quadratic equation solver", "[math]") {
    SECTION("x^2 - 4 = 0 has roots x=2 and x=-2") {
        // 只测试正根
        double root = quadraticRoot(1, 0, -4);
        CHECK(root == Approx(2.0).margin(1e-10));
    }

    SECTION("x^2 + 1 = 0 has no real roots") {
        double root = quadraticRoot(1, 0, 1);
        CHECK(root == 0);
    }
}

// ========== 异常测试 ==========

int divide_throw(int a, int b) {
    if (b == 0) throw std::invalid_argument("divisor is zero");
    return a / b;
}

TEST_CASE("divide throws on zero", "[exceptions]") {
    CHECK_THROWS_AS(divide_throw(10, 0), std::invalid_argument);
    CHECK_THROWS_WITH(divide_throw(10, 0), "divisor is zero");
    CHECK_NOTHROW(divide_throw(10, 2));  // 不应抛出
}

// ========== 标签和过滤 ==========

TEST_CASE("vector operations", "[container][vector]") {
    std::vector<int> v{1, 2, 3};
    
    SECTION("push_back") {
        v.push_back(4);
        REQUIRE(v.size() == 4);
        REQUIRE(v[3] == 4);
    }
    
    SECTION("pop_back") {
        v.pop_back();
        REQUIRE(v.size() == 2);
    }
}

TEST_CASE("string operations", "[container][string]") {
    std::string s = "hello";
    REQUIRE(s.length() == 5);
}
```

编译运行：
```bash
# Catch2 v3 方式
g++ -std=c++17 -I/path/to/catch2/include catch2_demo.cpp -o catch2_demo
./catch2_demo

# 只运行带 [math] 标签的测试
./catch2_demo "[math]"

# 运行除 [exceptions] 外的所有测试
./catch2_demo "~[exceptions]"
```

Catch2的亮点：
- **单头文件**：只要引入一个头文件就能开始测试
- **BDD风格语法**：`SCENARIO`, `GIVEN`, `WHEN`, `THEN`（如果你喜欢）
- **SECTION机制**：在同一个TEST_CASE里共享setup但测试不同路径
- **优雅的输出**：失败的测试会显示完整上下文

### 36.2.5 测试替身（Test Doubles）：当被测代码需要依赖其他组件时

单元测试的核心原则之一是**隔离**。但现实中的代码往往有各种依赖：

```
+----------------+      +----------------+
|  被测代码       | ---> |  依赖组件       |
|  (Unit under   |      |  (Database,    |
|   test)        |      |   Network,     |
+----------------+      |   FileSystem)  |
                        +----------------+
```

如果你的单元测试需要连接真实数据库，那测试就会：
1. 变慢
2. 可能因为网络问题失败
3. 每次运行结果可能不同（数据库数据变了）

**测试替身**就是用来替代真实依赖的模拟对象。

```cpp
// ============== 接口 ==============
struct IDatabase {
    virtual ~IDatabase() = default;
    virtual User findUserById(int id) const = 0;
    virtual bool saveUser(const User& user) = 0;
    virtual int countUsers() const = 0;
};

struct User {
    int id;
    std::string name;
    std::string email;
};

// ============== 真实实现（生产用）==============
class RealDatabase : public IDatabase {
    std::map<int, User> users_;
public:
    User findUserById(int id) const override {
        auto it = users_.find(id);
        if (it == users_.end()) throw std::runtime_error("User not found");
        return it->second;
    }
    bool saveUser(const User& user) override {
        users_[user.id] = user;
        return true;
    }
    int countUsers() const override { return users_.size(); }
};

// ============== 模拟实现（测试用）==============
#include <gmock/gmock.h>

class MockDatabase : public IDatabase {
public:
    mutable std::map<int, User> users_;
    mutable std::vector<std::pair<std::string, std::any>> calls_;  // 记录调用

    MOCK_METHOD(User, findUserById, (int id), (const, override));
    MOCK_METHOD(bool, saveUser, (const User&), (override));  // 注意：参数名省略，避免EXPECT_CALL匹配问题
    MOCK_METHOD(int, countUsers, (), (const, override));

    // 便捷的预设行为
    void addUser(const User& user) {
        users_[user.id] = user;
    }
};

// ============== 使用mock测试 ============

class UserService {
    IDatabase& db_;
public:
    explicit UserService(IDatabase& db) : db_(db) {}

    std::string getUserDisplayName(int id) {
        User u = db_.findUserById(id);
        return u.name + " (" + u.email + ")";
    }

    bool registerUser(const std::string& name, const std::string& email) {
        if (name.empty() || email.empty()) return false;
        int nextId = db_.countUsers() + 1;
        User u{nextId, name, email};
        return db_.saveUser(u);
    }
};

TEST(UserServiceTest, GetUserDisplayName) {
    MockDatabase mock;
    User testUser{1, "Alice", "alice@example.com"};
    mock.addUser(testUser);

    EXPECT_CALL(mock, findUserById(1))
        .Times(1)
        .WillOnce(testing::Return(testUser));

    UserService service(mock);
    std::string display = service.getUserDisplayName(1);

    EXPECT_EQ(display, "Alice (alice@example.com)");
}

TEST(UserServiceTest, RegisterUser) {
    MockDatabase mock;
    EXPECT_CALL(mock, countUsers()).WillOnce(testing::Return(0));
    EXPECT_CALL(mock, saveUser(testing::_)).WillOnce(testing::Return(true));

    UserService service(mock);
    bool result = service.registerUser("Bob", "bob@example.com");

    EXPECT_TRUE(result);
}
```

**测试替身的五种类型**：
| 类型 | 用途 | 特点 |
|------|------|------|
| **Dummy** | 填充参数列表 | 从不使用 |
| **Fake** | 有简化实现（如内存数据库） | 轻量但不是真实行为 |
| **Stub** | 预设响应 | 返回你预设的值 |
| **Spy** | 记录调用信息 | 让你验证调用是否发生 |
| **Mock** | 严格验证期望 | GMock/GTest的主要用途 |

### 36.2.6 测试驱动开发（TDD）：红-绿-重构循环

**TDD（Test-Driven Development）**是一种软件开发方法论，核心是**先写测试，再写实现**。流程是：

```
1. 写一个会失败的测试（红）
2. 写最少的代码让测试通过（绿）
3. 重构代码（改进设计），保持测试通过
4. 重复
```

```cpp
// TDD示例：为"计算器"写测试和实现

// Step 1: 先写测试（此时Calculator类还不存在）
TEST_CASE("calculator basic operations", "[tdd]") {
    Calculator calc;

    SECTION("add") {
        REQUIRE(calc.add(2, 3) == 5);
        REQUIRE(calc.add(-1, 1) == 0);
    }

    SECTION("subtract") {
        REQUIRE(calc.sub(5, 3) == 2);
        REQUIRE(calc.sub(3, 5) == -2);
    }
}

// 编译后会报错：Calculator类不存在（红）

// Step 2: 最少代码让测试通过
class Calculator {
public:
    int add(int a, int b) { return a + b; }
    int sub(int a, int b) { return a - b; }
};
// 现在测试通过了（绿）

// Step 3: 发现add(2,3)返回5是对的，但add(-1,1)呢？
// 实现里直接return a + b其实已经处理了（这步比较简单）
// 但TDD的精妙在于：你只实现了"被测试要求的功能"，
// 不会过度设计
```

TDD的争议一直很大：
- **支持者**：代码质量高，测试覆盖完整，设计更好
- **反对者**：速度慢，对于UI或不确定的需求不适用

**现实建议**：不必100% TDD，但在关键算法和核心逻辑上使用TDD会让你受益匪浅。

## 36.3 集成测试与系统测试：从小到大，从部分到整体

### 36.3.1 测试金字塔

你知道软件测试最好的策略是什么吗？**测试应该是一个金字塔**：

```
          /\
         /  \
        / E2E \        <-- 少量：端到端测试（慢，昂贵，但最接近真实）
       /------\
      /集成测试\      <-- 中量：集成测试（中等速度）
     /----------\
    /  单元测试  \    <-- 大量：单元测试（快，廉价，精准）
   /------------\
```

- **单元测试（Unit Tests）**：多，快速，失败时精确指出问题
- **集成测试（Integration Tests）**：中等，验证组件之间的交互
- **端到端测试（E2E Tests）**：少，慢，模拟真实用户场景

很多团队犯的错误是**倒金字塔**——大量E2E测试，少量单元测试。结果就是：测试跑一个小时，失败时根本不知道是哪里的问题。

### 36.3.2 集成测试：从两个组件开始

**集成测试**验证多个组件一起工作是否正确。在C++中，集成测试通常：

```cpp
// integration_test.cpp
// 假设我们有：
//   - DatabaseManager: 管理数据库连接
//   - UserRepository:  用户数据的CRUD操作
//   - UserService:     业务逻辑层

#include <catch2/catch_test_macros.hpp>
#include "DatabaseManager.h"
#include "UserRepository.h"
#include "UserService.h"

TEST_CASE("UserService + UserRepository integration", "[integration]") {
    // 使用测试数据库（而不是生产数据库）
    auto dbManager = std::make_unique<DatabaseManager>("test.db");
    dbManager->connect();
    dbManager->createTables();  // 初始化表结构

    UserRepository repo(*dbManager);
    UserService service(repo);

    SECTION("create and retrieve user") {
        bool created = service.createUser("Alice", "alice@example.com");
        REQUIRE(created == true);

        auto user = service.findUserByName("Alice");
        REQUIRE(user.has_value() == true);
        CHECK(user->email == "alice@example.com");
    }

    SECTION("duplicate email rejected") {
        service.createUser("Alice", "alice@example.com");
        bool duplicate = service.createUser("Bob", "alice@example.com");
        CHECK(duplicate == false);  // 业务逻辑应该拒绝重复email
    }

    // 测试结束后清理
    dbManager->dropTables();
    dbManager->disconnect();
}
```

**关键点**：集成测试应该使用**测试数据库**（通常是SQLite的临时文件，或内存数据库），而不是连接真实的开发/生产数据库。

### 36.3.3 冒烟测试（Sanity Check）：快速的"是死是活"

冒烟测试来源于硬件测试——如果电路板冒烟了，那就别测了，直接回去修。

在软件中，冒烟测试是**一组核心功能的快速检查**，确保系统"还活着"：

```cpp
TEST_CASE("smoke tests - system is alive", "[smoke]") {
    Config config("config.json");
    REQUIRE(config.load() == true);  // 能加载配置

    DatabaseManager db("test.db");
    REQUIRE_NOTHROW(db.connect());   // 能连接数据库

    UserService service(db);
    REQUIRE(service.isHealthy() == true);  // 服务健康

    Logger logger("app.log");
    REQUIRE_NOTHROW(logger.info("Smoke test passed"));  // 日志正常
}
```

冒烟测试通常在**每次提交后自动运行**，快速反馈"这个提交没把系统弄死"。

### 36.3.4 模糊测试（Fuzzing）：让随机数据找到你的bug

**模糊测试（Fuzzing）**是一种自动化测试技术，用随机或半随机数据不断"轰炸"你的程序，试图让它们崩溃或产生未定义行为。

```cpp
// fuzzer_demo.cpp - 简单模糊测试示例
#include <iostream>
#include <random>
#include <cstring>

// 假设这是你要测试的解析函数
struct ParseResult {
    bool success;
    int value;
    std::string error;
};

ParseResult parseConfig(const std::string& input) {
    // 简单解析格式: "key=value"
    auto eqPos = input.find('=');
    if (eqPos == std::string::npos) {
        return {false, 0, "Missing '='"};
    }

    std::string key = input.substr(0, eqPos);
    std::string val = input.substr(eqPos + 1);

    if (key != "port") {
        return {false, 0, "Unknown key"};
    }

    // stoi可能抛异常！
    try {
        int port = std::stoi(val);
        if (port < 0 || port > 65535) {
            return {false, 0, "Port out of range"};
        }
        return {true, port, ""};
    } catch (...) {
        return {false, 0, "Invalid number"};
    }
}

// 简单模糊测试器
void fuzzTest(int iterations = 10000) {
    std::mt19937 rng(42);  // 固定种子以便复现
    std::uniform_int_distribution<int> charDist(32, 126);  // 可打印ASCII

    int crashCount = 0;
    int successCount = 0;

    for (int i = 0; i < iterations; ++i) {
        // 生成随机字符串
        int len = std::uniform_int_distribution<int>(1, 50)(rng);
        std::string input;
        input.reserve(len);
        for (int j = 0; j < len; ++j) {
            input += static_cast<char>(charDist(rng));
        }

        // 测试解析
        auto result = parseConfig(input);
        if (result.success) {
            successCount++;
            std::cout << "[OK] \"" << input << "\" -> port=" << result.value << std::endl;
        }
    }

    std::cout << "\nFuzzing complete: " << successCount << " successes out of " << iterations << std::endl;
}

// ========== 使用libFuzzer（更专业的模糊测试）==========
// libFuzzer是LLVM项目的一部分，配合AddressSanitizer效果更佳

extern "C" int LLVMFuzzerTestOneInput(const uint8_t* data, size_t size) {
    // 将data转换为string
    std::string input(reinterpret_cast<const char*>(data), size);

    // 调用你要测试的函数
    auto result = parseConfig(input);

    // 如果你想触发crash来发现bug，可以这样做：
    // 但对于parseConfig，我们更关心返回值

    // LibFuzzer会自动变异输入，发现各种边界情况
    return 0;  // 返回0表示一切正常
}
```

使用libFuzzer编译：
```bash
# 假设parseConfig相关代码在fuzz_target.cpp中
clang++ -fsanitize=fuzzer,address -g fuzz_target.cpp -o fuzz_target
./fuzz_target -max_total_time=60  # 运行60秒
```

模糊测试在C++中特别有价值，因为C++程序处理原始输入时很容易出现：
- 缓冲区溢出
- 未定义行为
- 内存泄漏

## 36.4 调试技术：当bug出现时如何找到它

> *"调试时，打印语句是最被低估的工具。IDE的调试器固然强大，但有时候一个`std::cout << "here"`就能解决问题。"*
> —— 某位不愿意透露姓名的程序员

测试是主动防御，调试是事后补救。当测试没能抓住bug，或者用户在使用过程中发现bug时，调试就登场了。

### 36.4.1 科学的调试方法论

很多程序员调试的方式是"暴力枚举"——改一行代码，运行一下，不行再改。这不是调试，这是**碰运气**。

**科学的调试方法**：
1. **复现（Reproduce）**：让bug稳定复现。如果一个bug不能稳定复现，那说明你对它的理解还不够
2. **定位（Localize）**：二分查找，找到bug大概在哪个模块/函数
3. **假设（Hypothesize）**：根据症状提出假设
4. **验证（Verify）**：设计实验验证/否定假设
5. **修复（Fix）**：实施修复
6. **确认（Confirm）**：运行测试，确认修复有效

```
Bug的症状 ──> 缩小范围 ──> 提出假设 ──> 验证 ──> 找到根因 ──> 修复
     ^                                                           │
     └─────────────────── 验证修复 ──────────────────────────────┘
```

### 36.4.2 GDB：命令行的力量

GDB是GNU Debugger，C++程序员的"瑞士军刀"。虽然IDE的调试器越来越好用，但GDB在某些场景下不可替代：
- 服务器环境（没有GUI）
- 远程调试嵌入式设备
- 调试core dump文件

```cpp
// bug_demo.cpp - 有bug的程序
#include <iostream>
#include <vector>
#include <memory>

class Widget {
public:
    int id;
    std::string name;
    Widget(int i, const std::string& n) : id(i), name(n) {
        std::cout << "Widget " << id << " created\n";
    }
    ~Widget() {
        std::cout << "Widget " << id << " destroyed\n";
    }
};

double average(const std::vector<int>& vals) {
    // BUG: 没有检查vals是否为空！
    double sum = 0;
    for (int v : vals) {
        sum += v;
    }
    return sum / vals.size();  // 除以0！NaN！
}

void processWidgets() {
    std::vector<std::unique_ptr<Widget>> widgets;

    widgets.push_back(std::make_unique<Widget>(1, "Alpha"));
    widgets.push_back(std::make_unique<Widget>(2, "Beta"));

    // BUG: 迭代器失效！对vector添加元素后，之前的迭代器可能失效
    for (auto it = widgets.begin(); it != widgets.end(); ++it) {
        std::cout << "Processing " << (*it)->name << "\n";
        if ((*it)->id == 1) {
            widgets.push_back(std::make_unique<Widget>(3, "Gamma"));  // 可能导致迭代器失效！
        }
    }

    std::cout << "Widget count: " << widgets.size() << "\n";
}

int main() {
    std::cout << "=== Average test ===\n";
    std::vector<int> empty;
    std::cout << "Average of empty: " << average(empty) << "\n";  // NaN

    std::vector<int> nums{1, 2, 3, 4, 5};
    std::cout << "Average of 1..5: " << average(nums) << "\n";

    std::cout << "\n=== Widget test ===\n";
    processWidgets();

    std::cout << "\n=== Done ===\n";
    return 0;
}
```

使用GDB调试：
```bash
# 编译带调试信息的版本
g++ -g -O0 -std=c++17 bug_demo.cpp -o bug_demo

# 启动GDB
gdb ./bug_demo

# 在GDB中：
(gdb) break main              # 在main函数设置断点
(gdb) run                     # 运行程序
(gdb) break average           # 在average函数设置断点
(gdb) continue                # 继续运行到下一个断点
(gdb) print vals              # 打印vals变量
(gdb) print vals.size()       # 打印size
(gdb) next                    # 执行下一行（不进入函数）
(gdb) step                    # 执行下一行（进入函数）
(gdb) backtrace               # 打印调用栈
(gdb) frame 1                 # 切换到栈帧1
(gdb) watch vals.size()       # 当vals.size()改变时暂停
(gdb) delete breakpoints      # 删除所有断点
(gdb) quit                    # 退出GDB
```

**GDB常用命令**：

| 命令 | 缩写 | 说明 |
|------|------|------|
| `break function` | `b` | 在函数入口设断点 |
| `break file:line` | `b file:line` | 在指定文件行设断点 |
| `run args` | `r` | 启动程序 |
| `continue` | `c` | 继续运行 |
| `next` | `n` | 单步执行（不进入函数） |
| `step` | `s` | 单步执行（进入函数） |
| `print expr` | `p` | 打印表达式值 |
| `info locals` | `i locals` | 显示当前栈帧的局部变量 |
| `backtrace` | `bt` | 显示调用栈 |
| `watch expr` | | 当表达式值改变时暂停 |
| `condition bp-id expr` | | 给断点加条件 |

**条件断点**：
```
(gdb) break average if vals.empty()   # vals为空时才断住
(gdb) break 15 if result != result     # NaN检测！NaN != NaN为true
```

### 36.4.3 LLDB：macOS上的选择

在macOS上，LLDB是Xcode默认的调试器，命令和GDB非常相似：

```bash
lldb ./bug_demo
(lldb) break set -n average
(lldb) run
(lldb) frame variable vals  # 显示局部变量
(lldb) thread info         # 当前线程信息
(lldb) process continue
```

### 36.4.4 IDE调试器：可视化调试

虽然GDB/LLDB很强大，但IDE调试器在以下场景更高效：
- 查看复杂数据结构的可视化表示（STL容器、类对象等）
- 条件断点的图形化配置
- 多线程调试的线程视图

**Visual Studio调试C++**：
- F5: 开始调试
- F9: 切换断点
- F10: 单步跳过
- F11: 单步进入
- Shift+F5: 停止调试
- Ctrl+Shift+F9: 删除所有断点
- Debug > Windows > Watch: 添加监视窗口

**VS Code + C++扩展**：
```json
// .vscode/launch.json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "(gdb) Launch",
            "type": "cppdbg",
            "request": "launch",
            "program": "${workspaceFolder}/a.out",
            "args": [],
            "stopAtEntry": true,
            "cwd": "${workspaceFolder}",
            "environment": [],
            "externalConsole": false,
            "MIMode": "gdb",
            "preLaunchTask": "build"
        }
    ]
}
```

## 36.5 内存错误检测：让C++的内存问题无处遁形

C++最臭名昭著的bug来源是什么？**内存错误**。指针、堆内存、栈内存——任何一个不小心，就会导致：
- 段错误（Segmentation Fault）
- 内存泄漏（Memory Leak）
- 数据竞争（Data Race）
- 缓冲区溢出（Buffer Overflow）

好消息是，有很多工具可以帮助你检测这些问题。

### 36.5.1 AddressSanitizer（ASan）：编译器内置的内存错误检测器

AddressSanitizer是LLVM/Clang和GCC内置的内存检测工具，编译时加一个flag就能用：

```bash
# 编译时启用ASan
g++ -fsanitize=address -g -O1 bug_demo.cpp -o bug_demo_asan

# 运行，ASan会自动检测内存错误
./bug_demo_asan
```

ASan能检测：
- **Use-after-free**：访问已释放的内存
- **Double-free**：重复释放同一块内存
- **Heap buffer overflow**：堆缓冲区溢出
- **Stack buffer overflow**：栈缓冲区溢出
- **Global buffer overflow**：全局数组溢出
- **Use-after-scope**：离开作用域后仍使用局部变量
- **Memory leaks**：内存泄漏（需要配合`ASAN_OPTIONS=detect_leaks=1`）

```cpp
// asan_demo.cpp
#include <cstdlib>
#include <cstring>

void useAfterFree() {
    char* buf = new char[10];
    strcpy(buf, "hello");
    delete[] buf;
    // BUG: use after free
    char c = buf[0];  // ASan会在这里报错！
}

void heapOverflow() {
    char* buf = new char[10];
    // BUG: heap buffer overflow
    strcpy(buf, "this string is longer than 10 characters!");  // ASan会报错
    delete[] buf;
}

void stackOverflow() {
    char buf[10];
    // BUG: stack buffer overflow
    memset(buf, 'A', 100);  // 写到栈边界外了！
}

int main() {
    std::cout << "Testing ASan...\n";
    // 选择一个测试
    useAfterFree();
    // heapOverflow();
    // stackOverflow();
    return 0;
}
```

运行：
```bash
g++ -fsanitize=address -g -O1 asan_demo.cpp -o asan_demo
./asan_demo
```

ASan输出示例：
```
=================================================================
==12345==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x602000000030
WRITE of size 35 at 0x602000000030 thread T0
    #0 0x7ffff7a8b2a1 in __asan_report_store
    #1 0x401346 in heapOverflow() asan_demo.cpp:13
    ...
```

### 36.5.2 Valgrind：老牌内存检测工具

Valgrind是Linux下历史最悠久的内存检测工具（虽然它不只是内存检测器）。

```bash
# 在没有ASan的情况下使用Valgrind
valgrind --leak-check=full --show-leak-kinds=all ./bug_demo
```

Valgrind的`memcheck`工具能检测：
- 内存泄漏
- 使用未初始化内存
- 使用已释放内存
- 读写越界

```cpp
// valgrind_demo.cpp
#include <stdlib.h>

void leakMemory() {
    void* p = malloc(100);
    // BUG: forgot to free(p)!
}

int main() {
    leakMemory();
    return 0;
}
```

```bash
g++ -g -O0 valgrind_demo.cpp -o valgrind_demo
valgrind --leak-check=full ./valgrind_demo
```

输出：
```
==12346== Memcheck, a memory error detector
...
==12346== 100 bytes in 1 blocks are definitely lost in loss record 1 of 1
   at 0x4A06A68: malloc (vg_replace_malloc.c:...)
   by 0x400715: leakMemory() in valgrind_demo.cpp:5
   by 0x40072B: main in valgrind_demo.cpp:10
```

### 36.5.3 LeakSanitizer（LSan）：进程退出时的内存泄漏检测

LSan是ASan家族的一员，专门检测内存泄漏，比Valgrind快很多：

```bash
g++ -fsanitize=leak -g leak_demo.cpp -o leak_demo
./leak_demo
```

### 36.5.4 UndefinedBehaviorSanitizer（UBSan）：未定义行为检测

C++的很多操作是"undefined behavior"（未定义行为），编译器可能做出任何事——包括"看似正确但实际随机"：

```cpp
// ubsan_demo.cpp
#include <cstdint>

int main() {
    // 有符号整数溢出 - UB！
    int x = INT_MAX;
    x = x + 1;  // UB: signed integer overflow

    // 空指针解引用
    int* p = nullptr;
    // int y = *p;  // UB: null pointer dereference

    // 数组越界访问
    int arr[5];
    // arr[10] = 0;  // UB: array out of bounds

    return 0;
}
```

```bash
g++ -fsanitize=undefined -g ubsan_demo.cpp -o ubsan_demo
./ubsan_demo
```

UBSan输出：
```
ubsan_demo.cpp:5: runtime error: signed integer overflow: 2147483647 + 1 cannot be represented in type 'int'
```

### 36.5.5 ThreadSanitizer（TSan）：数据竞争检测

多线程程序的噩梦——**数据竞争（data race）**。两个线程同时访问同一内存，至少有一个是写操作，且没有任何同步：

```cpp
// tsan_demo.cpp
#include <thread>
#include <atomic>
#include <iostream>

// BUG: 数据竞争！
int counter = 0;  // 全局变量
std::mutex mtx;

void increment() {
    for (int i = 0; i < 100000; ++i) {
        // 没有锁保护的多线程写操作 - 数据竞争！
        counter++;  // 读-改-写操作，不是原子的！
    }
}

int main() {
    std::thread t1(increment);
    std::thread t2(increment);
    t1.join();
    t2.join();
    // counter应该是200000，但很可能不是！
    std::cout << "Counter: " << counter << " (expected 200000)\n";
    return 0;
}
```

```bash
g++ -fsanitize=thread -g -O1 tsan_demo.cpp -lpthread -o tsan_demo
./tsan_demo
```

TSan会检测到数据竞争并报告：
```
WARNING: ThreadSanitizer: data race (pid=12345)
  Write of size 4 at 0x... by thread T1:
    #0 increment() tsan_demo.cpp:12
  Previous write of size 4 at 0x... by thread T2:
    #0 increment() tsan_demo.cpp:12
```

**正确的多线程代码**：
```cpp
// 使用原子变量或互斥锁
std::atomic<int> counter(0);  // 原子类型

void increment() {
    for (int i = 0; i < 100000; ++i) {
        counter.fetch_add(1, std::memory_order_relaxed);  // 原子操作
    }
}
```

## 36.6 日志与断言：调试的好帮手

### 36.6.1 日志系统：让程序自己告诉你发生了什么

日志是调试的"黑匣子"。当程序崩溃时，日志能告诉你最后发生了什么。

```cpp
// logger_demo.cpp
#include <iostream>
#include <fstream>
#include <sstream>
#include <chrono>
#include <iomanip>
#include <mutex>
#include <thread>

enum class LogLevel { DEBUG, INFO, WARNING, ERROR, FATAL };

class Logger {
public:
    static Logger& instance() {
        static Logger instance;
        return instance;
    }

    void setLevel(LogLevel level) { minLevel_ = level; }

    void log(LogLevel level, const std::string& file, int line, const std::string& msg) {
        if (level < minLevel_) return;

        std::lock_guard<std::mutex> lock(mutex_);
        auto now = std::chrono::system_clock::now();
        auto time = std::chrono::system_clock::to_time_t(now);
        auto ms = std::chrono::duration_cast<std::chrono::milliseconds>(
            now.time_since_epoch()) % 1000;

        std::cout << "[" << levelToString(level) << "] "
                  << std::put_time(std::localtime(&time), "%Y-%m-%d %H:%M:%S")
                  << "." << std::setfill('0') << std::setw(3) << ms.count()
                  << " [" << std::this_thread::get_id() << "] "
                  << file << ":" << line << " - " << msg << "\n";
    }

private:
    Logger() : minLevel_(LogLevel::DEBUG) {}

    std::string levelToString(LogLevel level) {
        switch (level) {
            case LogLevel::DEBUG: return "DEBUG";
            case LogLevel::INFO:  return "INFO ";
            case LogLevel::WARNING: return "WARN ";
            case LogLevel::ERROR: return "ERROR";
            case LogLevel::FATAL: return "FATAL";
        }
        return "UNKNOWN";
    }

    LogLevel minLevel_;
    std::mutex mutex_;
};

// 便捷宏
#define LOG_DEBUG(msg) Logger::instance().log(LogLevel::DEBUG, __FILE__, __LINE__, msg)
#define LOG_INFO(msg)  Logger::instance().log(LogLevel::INFO,  __FILE__, __LINE__, msg)
#define LOG_WARN(msg)  Logger::instance().log(LogLevel::WARNING, __FILE__, __LINE__, msg)
#define LOG_ERROR(msg) Logger::instance().log(LogLevel::ERROR, __FILE__, __LINE__, msg)
#define LOG_FATAL(msg) Logger::instance().log(LogLevel::FATAL, __FILE__, __LINE__, msg)

class NetworkManager {
public:
    bool connect(const std::string& host, int port) {
        LOG_INFO("Connecting to " + host + ":" + std::to_string(port));
        if (host.empty()) {
            LOG_ERROR("Host cannot be empty");
            return false;
        }
        // 模拟连接
        LOG_DEBUG("Connection established");
        return true;
    }

    bool send(const std::string& data) {
        if (data.empty()) {
            LOG_WARN("Sending empty data");
            return false;
        }
        LOG_DEBUG("Sent " + std::to_string(data.size()) + " bytes");
        return true;
    }
};

int main() {
    Logger::instance().setLevel(LogLevel::DEBUG);

    LOG_INFO("Application started");
    LOG_DEBUG("Debug mode enabled");

    NetworkManager net;
    net.connect("example.com", 8080);
    net.send("Hello, World!");
    net.connect("", 80);  // 会触发错误日志
    net.send("");         // 会触发警告日志

    LOG_INFO("Application finished");
    return 0;
}
```

**输出**：
```
[INFO ] 2026-03-29 15:48:00.123 [12345] logger_demo.cpp:71 - Application started
[DEBUG] 2026-03-29 15:48:00.124 [12345] logger_demo.cpp:72 - Debug mode enabled
[INFO ] 2026-03-29 15:48:00.124 [12345] logger_demo.cpp:79 - Connecting to example.com:8080
[DEBUG] 2026-03-29 15:48:00.125 [12345] logger_demo.cpp:80 - Connection established
[DEBUG] 2026-03-29 15:48:00.125 [12345] logger_demo.cpp:86 - Sent 13 bytes
[ERROR] 2026-03-29 15:48:00.125 [12345] logger_demo.cpp:81 - Host cannot be empty
[WARN ] 2026-03-29 15:48:00.125 [12345] logger_demo.cpp:87 - Sending empty data
[INFO ] 2026-03-29 15:48:00.125 [12345] logger_demo.cpp:91 - Application finished
```

**生产环境建议**：使用成熟的日志库如`spdlog`或`boost.log`，不要重复造轮子。

### 36.6.2 断言：开发期的假设验证

**断言（assertion）**是"这必须为真，否则就是程序bug"的机制。断言只在**调试/开发版本**中生效，**发布版本通常禁用断言**。

```cpp
#include <cassert>
#include <algorithm>

int binarySearch(const std::vector<int>& sorted, int target) {
    assert(std::is_sorted(sorted.begin(), sorted.end()) && 
           "binarySearch requires sorted input!");

    int left = 0, right = sorted.size() - 1;
    while (left <= right) {
        int mid = left + (right - left) / 2;  // 防止(left+right)溢出
        assert(mid >= 0 && mid < static_cast<int>(sorted.size()) &&
               "Mid index out of bounds - logic error!");
        if (sorted[mid] == target) return mid;
        if (sorted[mid] < target) left = mid + 1;
        else right = mid - 1;
    }
    return -1;
}

// 自定义断言宏（带上下文信息）
#define ASSERT_VECTOR_SIZE(v, expected_size) \
    assert((v).size() == (expected_size) && \
           "Vector size mismatch: " #v " has " \
           + std::to_string((v).size()) + " elements, expected " + #expected_size)

int main() {
    std::vector<int> nums{1, 3, 5, 7, 9};

    // NDEBUG定义时，assert失效
    // g++ -DNDEBUG program.cpp  # 禁用assert
    assert(binarySearch(nums, 5) == 2 && "5 should be at index 2");
    assert(binarySearch(nums, 6) == -1 && "6 not in array");

    return 0;
}
```

**断言 vs 异常**：

| 维度 | 断言 (assert) | 异常 (exception) |
|------|--------------|-----------------|
| **目的** | 验证"不可能发生"的事（程序bug） | 捕获"可能发生"的错误（输入、网络等） |
| **调试版** | 启用，失败时终止 | 启用，传播给调用者 |
| **发布版** | 通常禁用 | 启用，需要处理 |
| **失败时** | 程序崩溃 | 可捕获，恢复执行 |

**原则**：
- 断言用于验证**内部不变量**和**程序员假设**
- 异常用于处理**外部错误**（用户错误输入、文件不存在、网络断开）
- 不要用断言处理"正常情况可能发生的错误"

```cpp
// 错误：把用户输入验证写成assert
void processAge(int age) {
    assert(age >= 0);  // 错！年龄负数可能来自用户输入，应该返回错误
}

// 正确：区分断言和异常
void processAge(int age) {
    if (age < 0) {
        throw std::invalid_argument("Age cannot be negative");
    }
    assert(age <= 150);  // 对！如果年龄>150，肯定是程序bug（常量定义错了）
}
```

## 36.7 持续集成与自动化测试：让机器替你守质量门

### 36.7.1 什么是持续集成（CI）？

**持续集成（Continuous Integration）**是一种开发实践：每次代码提交（commit）到版本库时，自动运行构建和测试，及时发现集成错误。

```
开发者A ──> 提交代码 ──> CI服务器 ──> 编译 ──> 测试 ──> 报告结果
                              │
开发者B ──> 提交代码 ──> ──────┘

如果测试失败：开发者会收到邮件/消息通知
```

### 36.7.2 使用CMake + GoogleTest搭建CI

```cmake
# CMakeLists.txt
cmake_minimum_required(VERSION 3.14)
project(MyProject)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# 启用测试
enable_testing()

# GoogleTest
include(FetchContent)
FetchContent_Declare(
    googletest
    GIT_REPOSITORY https://github.com/google/googletest.git
    GIT_TAG        v1.14.0
)
FetchContent_MakeAvailable(googletest)

# 你的库
add_library(mymath src/math.cpp)

# 可执行文件
add_executable(app src/main.cpp)
target_link_libraries(app mymath)

# 测试
add_executable(math_tests tests/math_test.cpp)
target_link_libraries(math_tests mymath gtest_main)
add_test(NAME MathTests COMMAND math_tests)
```

```yaml
# .github/workflows/ci.yml (GitHub Actions)
name: CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  build-and-test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Configure CMake
      run: cmake -B build -DCMAKE_BUILD_TYPE=Release
      
    - name: Build
      run: cmake --build build -j$(nproc)
      
    - name: Run Tests
      run: ctest --output-on-failure --test-dir build
```

### 36.7.3 测试覆盖率：你的测试够全面吗？

测试覆盖率（code coverage）衡量"有多少代码被测试执行过"。

```bash
# 使用gcov（GCC的代码覆盖率工具）
g++ -fprofile-arcs -ftest-coverage -O0 mycode.cpp test.cpp -o myapp
./myapp
gcov mycode.cpp     # 生成mycode.cpp.gcov
gcovr --html-details coverage.html  # 生成HTML报告
```

**覆盖率指标**：
| 指标 | 含义 |
|------|------|
| **Line Coverage** | 执行过的代码行数 / 总代码行数 |
| **Function Coverage** | 调用过的函数数 / 总函数数 |
| **Branch Coverage** | 执行过的分支数 / 总分支数 |
| **Condition Coverage** | 每个条件的真/假都被测试过 |

**重要提醒**：100%覆盖率不等于没有bug！它只能说明"代码被执行过"，不能说明"执行结果是对的"。覆盖率是**最低质量底线**，不是目标。

## 36.8 常见C++调试场景与解决方案

### 36.8.1 段错误（Segmentation Fault）

段错误是最常见的C++崩溃原因，通常由以下情况引起：

```cpp
// 场景1: 空指针解引用
int* p = nullptr;
*p = 42;  // SIGSEGV!

// 场景2: 野指针（ dangling pointer）
int* p = new int(10);
delete p;
*p = 20;  // SIGSEGV! p现在是野指针

// 场景3: 数组越界
std::vector<int> v(5);
v[10] = 1;  // SIGSEGV!（但vector有边界检查时是抛出异常）

// 场景4: 栈溢出（递归没终止条件）
void infiniteRecursion() {
    infiniteRecursion();  // 栈空间耗尽，SIGSEGV
}

// 场景5: 解引用未初始化的指针
int* p;  // 未初始化，指向随机地址
*p = 42;  // SIGSEGV或更糟（碰巧改了其他数据）
```

**调试方法**：
1. 使用ASan：`g++ -fsanitize=address -g prog.cpp`
2. 使用GDB：`gdb ./prog`，等SIGSEGV后，`bt`查看调用栈
3. 添加打印：`std::cout << "到达这里\n";`

### 36.8.2 内存泄漏

```cpp
// 常见泄漏场景
void leakExample() {
    int* p = new int[100];  // 分配了
    // 忘记 delete[] p;  // 泄漏!

    Widget* w = new Widget();
    delete w;
    // BUG: Widget的析构函数没virtual，但通过基类指针删除
}

// 正确做法：使用智能指针
void noLeakExample() {
    auto p = std::make_unique<int[]>(100);  // 自动释放
    auto w = std::make_unique<Widget>();    // 自动释放
}
```

### 36.8.3 竞争条件（Race Condition）

多线程同时修改共享数据：

```cpp
// BUG: 数据竞争
int counter = 0;
void increment() {
    for (int i = 0; i < 10000; ++i) {
        counter++;  // 非原子操作！读-改-写三步操作可能被中断
    }
}

// FIX 1: 使用互斥锁
std::mutex mtx;
int counter = 0;
void increment() {
    for (int i = 0; i < 10000; ++i) {
        std::lock_guard<std::mutex> lock(mtx);
        counter++;
    }
}

// FIX 2: 使用原子变量
std::atomic<int> counter(0);
void increment() {
    for (int i = 0; i < 10000; ++i) {
        counter.fetch_add(1, std::memory_order_relaxed);
    }
}
```

### 36.8.4 模板错误信息爆炸

C++模板错误信息出了名的难懂，一个简单的错误可能引发几百行的错误信息：

```cpp
// 这个代码在C++17之前可能产生100+行的错误信息
template<typename T>
T maxValue(const std::vector<T>& v) {
    return *std::max_element(v.begin(), v.end());
}

int main() {
    std::vector<std::string> v{"a", "bb", "ccc"};
    auto result = maxValue(v);  // T=std::string，没问题
    // 但如果传入不可比较的类型...
}
```

**调试技巧**：
1. 升级到C++20，使用`std::format`等更友好的错误报告
2. 使用`static_assert`提供更清晰的错误信息
3. GCC的`-fdiagnostics-color`让错误高亮更清晰
4. 使用IDE的"错误解析"功能（通常会折叠模板噪声）

```cpp
// 使用static_assert提供清晰错误信息
template<typename T>
T maxValue(const std::vector<T>& v) {
    static_assert(std::is_same_v<T, int> || 
                  std::is_same_v<T, double> ||
                  std::is_same_v<T, float>,
                  "maxValue only supports int, double, or float");
    return *std::max_element(v.begin(), v.end());
}
```

## 36.9 本章小结

### 核心要点回顾

| 主题 | 关键收获 |
|------|---------|
| **测试的重要性** | 测试是主动防御，调试是事后补救。两者结合才能构建可靠软件 |
| **单元测试** | 使用Google Test或Catch2编写独立、可重复的测试。测试替身隔离依赖 |
| **TDD** | 红-绿-重构循环，先写测试后写实现，让设计从测试需求中涌现 |
| **集成测试** | 测试组件交互，使用测试数据库/环境，介于单元测试和E2E之间 |
| **模糊测试** | 用随机输入发现边界情况和异常输入导致的bug |
| **GDB/LLDB** | 掌握断点、单步、查看变量、调用栈等核心调试操作 |
| **ASan/UBSan/TSan** | 编译器内置工具，零成本发现内存错误和未定义行为 |
| **日志** | 结构化日志是生产环境的"黑匣子"，分层日志级别便于问题定位 |
| **断言** | 断言验证程序员假设（内部不变量），异常处理外部错误 |
| **CI/CD** | 自动化构建和测试，每次提交都运行测试，快速反馈 |

### 关键命令速查

```bash
# 编译测试
g++ -std=c++17 -I/path/to/gtest/include mytest.cpp -lgtest -lgtest_main -pthread -o mytest

# AddressSanitizer
g++ -fsanitize=address -g -O1 program.cpp -o program

# ThreadSanitizer
g++ -fsanitize=thread -g -O1 program.cpp -lpthread -o program

# UndefinedBehaviorSanitizer
g++ -fsanitize=undefined -g program.cpp -o program

# GDB基本命令
gdb ./program
(gdb) break main
(gdb) run
(gdb) next / step / continue
(gdb) print variable
(gdb) backtrace

# Valgrind
valgrind --leak-check=full ./program

# CMake + 测试
cmake -B build -DENABLE_TESTING=ON
cmake --build build
ctest --test-dir build --output-on-failure
```

### 实战建议

1. **从今天开始写测试**：不要想着"等项目完成再补测试"，从第一个函数开始就写测试
2. **遇到bug时先写测试复现**：先写一个会失败的测试用例，再去调试，会让你的调试更聚焦
3. **使用Sanitizers作为标准构建配置**：ASan/UBSan/TSan的开销在开发阶段是可接受的，收益巨大
4. **日志要结构化**：在生产环境，半结构化日志（如JSON）比纯文本更利于查询分析
5. **CI是质量门卫**：每次PR都应通过CI，没有例外
6. **覆盖率是底线不是目标**：追求有意义的测试覆盖，而不是数字上的好看

> *"测不出来的bug不算bug" —— 这句话虽然有点极端，但道理是对的。真正重要的不是你写了多少测试，而是你的测试是否真正验证了代码的正确性。*
> *"调试的艺术在于理解：你的代码不会故意犯错，它只是在做你告诉它做的事。所以当出现bug时，首先怀疑的是你自己的理解，而不是代码。"*

**下一章预告**：第37章将进一步深入**代码审查与重构**——如何通过团队协作和代码改进来预防bug的产生，以及如何识别和改造那些"遗留代码"中的陷阱。

---

*本章完*
