title = "第35章 编码规范——程序员的'交通规则'"
weight = 350
date = "2026-03-29T21:03:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false

+++

# 第35章 编码规范——程序员的"交通规则"

想象一下，如果你开车上路，所有的车都不靠右行驶、不打转向灯、红灯直接闯过去——那将是一场灾难。代码世界也是如此。如果没有一套大家共同遵守的编码规范，团队协作就像一群人在没有红绿灯的十字路口"自由发挥"，结局往往是代码"车祸现场"。

本章，我们将深入探讨C++编码规范——那些让你的代码从"个人作品"升级为"团队资产"的黄金法则。这些规范不是用来扼杀创造力的，而是让你的创造力在有序的框架内发挥到极致。毕竟，真正的艺术大师从不拒绝规则——他们只是在规则之内找到了自由。

> **本章适合谁**：所有想要写出"让人看了想给你点赞"而不是"看了想给你烧香"的C++代码的程序员。无论是独自奋战的独行侠，还是在团队中摸爬滚打的上班族，这章都能让你受益匪浅。

## 35.1 命名规范——给变量起个好名字

### 35.1.1 命名的艺术：为什么 `x` 不是个好名字

给变量起名字，是程序员每天都在做的事，但很多人却把它当成一件"随便应付"的小事。让我告诉你一个残酷的真相：**代码是写给人看的，顺便给机器执行**。一个叫 `x`、`tmp`、`data` 的变量，就像你给宠物取名"那个谁"——短期凑合，长期灾难。

好的命名应该像一封清晰的情书，让人一眼就知道你的意图：

```cpp
// ❌ 糟糕的命名：看完了你也不知道这是干嘛的
int x;
int tmp;
double data;
bool flag;
std::string str;
int* p;

// ✅ 优秀的命名：一目了然
int userAge;
int maxRetryCount;
double accountBalance;
bool isUserLoggedIn;
std::string userEmailAddress;
int* userPointer;           // 指针变量同样可以取见名知意的名字
```

### 35.1.2 命名风格：下划线还是驼峰？

C++界有两大气宗流派：**下划线派**（snake_case）和**驼峰派**（camelCase/PascalCase）。就像豆腐脑的甜咸之争，这场战争从未停歇，但更重要的是——**选择一个风格，全团队统一**。

```cpp
// ==================== 下划线风格（Linux/Google C++ Style）====================
// 变量和函数：全小写，单词之间用下划线分隔
int user_age;
int max_connection_count;
void send_user_data();
class user_account_manager;

// 类的成员变量：以下划线结尾（避免与参数/局部变量冲突）
class Circle {
private:
    double radius_;
    double center_x_;
    double center_y_;
};

// 常量和宏：全大写，下划线分隔
const int MAX_BUFFER_SIZE = 4096;
constexpr int DEFAULT_TIMEOUT_MS = 3000;
#define MAX_RETRY_COUNT 3

// ==================== 驼峰风格（Microsoft/C# Style）====================
// 变量和函数：首字母小写，后续单词首字母大写
int userAge;
int maxConnectionCount;
void sendUserData();
class UserAccountManager;

// 类的成员变量：m_ 前缀（Microsoft常用）
class Circle {
private:
    double m_radius;
    double m_centerX;
    double m_centerY;
};

// 另一种：下划线后缀 + PascalCase类名（我个人最爱）
class CircleAreaCalculator {
public:
    double calculate(const Circle& circle);
private:
    double pi_ = 3.14159265358979;  // 成员变量以下划线结尾
};
```

> **小明的踩坑日记**：小明写了一个函数叫 `doWork()`，另一个叫 `DoWork()`，还有一个叫 `do_work()`。在Windows上，文件系统不区分大小写，所以他花了整整一个下午debug那个神秘的"函数未定义"错误。从那以后他发誓：只用一个命名风格，绝不混用！

### 35.1.3 命名规则：禁忌与建议

有些名字是C++里的"雷区"，碰了轻则编译警告，重则身心受创：

```cpp
// ❌ 绝对不要这样做——和标准库/关键字撞车
int std;          // 跟命名空间std同名
int class;        // 关键字
int my-include;   // 包含非法字符（横杠是减号！）

// ❌ 极度不建议——下划线开头的名字在某些上下文里有特殊含义
int _reserved;    // 编译器可能用的名字
int __magic;      // 双下划线更是禁区中的禁区

// ❌ 单字母除了循环计数器和模板参数外，慎用！
// for (int i = 0; i < n; ++i) {}  // 循环里的 i 可以接受
// 但 int x, y, z; 就不太能接受了（除非是坐标轴）

// ✅ 推荐的命名
template<typename T>
class SmartPtr {
public:
    void reset(T* ptr) { /* ... */ }
    T* get() const { return ptr_; }
private:
    T* ptr_ = nullptr;  // 成员变量以下划线结尾
};

// 对于模板参数，用有意义的单个字母是可以接受的
// T (Type), K (Key), V (Value), R (Return), Container, Iterator
template<typename Container, typename Iterator>
Iterator find_in_container(const Container& c, const typename Container::value_type& v) {
    return std::find(c.begin(), c.end(), v);
}
```

### 35.1.4 命名的一致性：团队的灵魂

命名规范最重要的不是"哪个更好"，而是"大家都一样"。就像红绿灯，重要的是"红灯停、绿灯行"这套规则，而不是红色和绿色本身。

```cpp
// 一致性的反面教材——让人精神分裂的命名
class UserManager {
public:
    void AddUser(const User& u);          // 大写开头
    void deleteUser(int id);              // 小写开头
    void ModifyUserEmail(int ID);         // 参数ID大写
    int GetUserCount() const;             // 大写开头
    void clear();                        // 小写，没下划线
    void reset_all();                    // 下划线，但全小写
};

// 改进后的版本——风格统一，看着就舒服
class UserManager {
public:
    void addUser(const User& user);
    void deleteUser(int user_id);
    void modifyUserEmail(int user_id, const std::string& new_email);
    int getUserCount() const;
    void clear();
    void resetAll();
};
```

## 35.2 代码格式化——代码的"门面工程"

### 35.2.1 缩进：Tab还是空格？

这是C++社区最"容易引发友谊破裂"的话题之一。让我用一句话总结：**选空格，用4个，全团队统一**。

- Tab的问题是：不同编辑器的Tab宽度不一样（2、4、8...），你的"整齐排列"在别人那里可能是"乱成一锅粥"
- 空格的优点是：所见即所得，在任何编辑器都一模一样

```cpp
// 如果你用空格缩进（标准做法）
class MyClass {
public:             // 4空格
    void myMethod() {
        if (condition) {   // 4空格
            doSomething();  // 8空格
        }
    }
};

// 现代IDE（CLion、VS Code等）都可以设置：
// Tab键插入空格，而不是实际的Tab字符
// 推荐设置：Indent using spaces, 4 spaces per indent
```

### 35.2.2 行长度：别让滚动条成为你的噩梦

每行代码的理想长度是**不超过80或120个字符**。超过这个限制的代码行，在代码审查、多窗口编辑、甚至打印时都会造成各种不便。

```cpp
// ❌ 一行太长的代码——读起来像在跑马拉松
if (user_ptr != nullptr && user_ptr->isActive() && user_ptr->getLevel() >= required_level && user_ptr->hasPermission(permission_bits)) {

// ✅ 拆分成多行——逻辑清晰，可读性满分
if (user_ptr != nullptr
    && user_ptr->isActive()
    && user_ptr->getLevel() >= required_level
    && user_ptr->hasPermission(permission_bits)) {

// 或者用变量先过滤，让条件更易读
const bool has_valid_pointer = (user_ptr != nullptr);
const bool meets_level = user_ptr->getLevel() >= required_level;
const bool has_permission = user_ptr->hasPermission(permission_bits);

if (has_valid_pointer && user_ptr->isActive() && meets_level && has_permission) {
    // ...
}
```

### 35.2.3 花括号：对齐的艺术

关于花括号的位置，C++社区也有不同的流派：

```cpp
// ==================== K&R风格（Kernighan & Ritchie，最经典）====================
// 括号在控制语句同一行，函数开括号单独一行
void myFunction() {
    if (condition) {
        doSomething();
    } else {
        doOtherThing();
    }
}

// ==================== Allman风格（更清晰，IDE友好）====================
// 括号单独一行，更容易定位代码块
void myFunction()
{
    if (condition)
    {
        doSomething();
    }
    else
    {
        doOtherThing();
    }
}

// ==================== 1TBS风格（也广受欢迎）====================
// K&R变体，else与右括号同行——这是Linux内核和Google采用的风格
void myFunction() {
    if (condition) {
        doSomething();
    } else {
        doOtherThing();
    }
}

// ==================== 到底用哪个？====================
// 答案：看你们团队用什么。然后保持一致。
// 如果你一个人写代码——选K&R 1TBS，这是C/C++世界最主流的约定。
```

### 35.2.4 空格与空行：让代码"呼吸"

代码不是挤在一起的文字，它需要"呼吸"——适当的空格和空行能让逻辑结构一目了然。

```cpp
// ❌ 密度过高——阅读体验像在读密电码
if(x>0&&y<100){for(int i=0;i<x;i++){sum+=i;}}

// ✅ 适当留白——逻辑清晰，阅读愉快
if (x > 0 && y < 100) {
    for (int i = 0; i < x; ++i) {
        sum += i;
    }
}

// ==================== 操作符周围的空格 ====================
int a = b + c;           // 赋值和运算周围加空格
int* ptr = &value;      // 取地址和指针符号周围不加空格
ptr = &some_value;
a = b * c + d * e;       // 乘除优先于加减，适当用括号更清晰

// ==================== 冒号周围（作用域/继承/三元）====================
class Base {
public:
    virtual ~Base() = default;
};

class Derived : public Base {  // 冒号前后有空格
private:
    int value_ = 0;            // 成员初始化列表的冒号后有空格
public:
    explicit MyClass(int v) : value_(v) {}

    int getValue() const {     // const 前后有空格
        return value_;
    }
};

// ==================== 空行的使用 ====================
// 同一逻辑块内部不放空行，不同逻辑块之间放一个空行
void processUserData(const User& user) {
    validateUser(user);        // 验证——逻辑组1

    auto profile = loadProfile(user.id);  // 数据加载——空行分隔
    updateStatistics(profile);

    saveToDatabase(profile);   // 保存——空行分隔
    notifyObservers(user.id);
}
```

### 35.2.5 工具的力量：clang-format

手动格式化代码是一件极其无聊且容易出错的事情。幸好，现代C++有 `clang-format` 这个神器——你只需要定义一次规则，它帮你搞定一切。

```cpp
// .clang-format 配置文件示例（放在项目根目录）
---
Language: Cpp
BasedOnStyle: Google          // 以Google风格为基础，按需调整
IndentWidth: 4               // 缩进宽度
ColumnLimit: 100             // 每行最多100字符
UseTab: Never                // 不用Tab，只用空格
PointerAlignment: Left        // 指针/引用符号靠左：int* p
AccessModifierOffset: -4      // private/public 缩短缩进
NamespaceIndentation: None   // namespace 不额外缩进
AllowShortFunctionsOnASingleLine: Inline   // 短函数可以放一行
BreakBeforeBraces: Attach     // K&R 风格
IndentCaseLabels: true       // case 标签再缩进一次
SortIncludes: true            // 自动排序 #include
---

// 使用方法：
// $ clang-format -i src/*.cpp    // 就地格式化
// $ clang-format src/main.cpp    // 输出到stdout
```

> **格式化工具推荐**：
>
> - `clang-format`：C++最强大的格式化工具，LLVM/Google/clang都在用
> - `cmake-format`：如果你用CMake，它能帮你格式化CMakeLists.txt
> - IDE插件：CLion自带格式化，VS Code + C++扩展也可以，配置`.clang-format`后一键美化

## 35.3 注释与文档——代码的"说明书"

### 35.3.1 注释的哲学：为什么写注释比不写更糟糕

等等，你没看错标题。**好的注释是财富，坏的注释是灾难**。注释写得不对，不仅没有帮助，还会误导后来人（或者两年后的你自己）。

```cpp
// ❌ 废话型注释——浪费屏幕，侮辱读者智商
int x = 10;  // 给x赋值为10
if (condition) {  // 如果条件为真
    doSomething();  // 做点事
}

// ❌ 过时型注释——代码改了，注释没改，比没注释还害人
// 注释说返回最大值，但实现偷偷改成了返回最小值
// 读注释的人：哦，返回最大值，懂了
// 实际运行：返回的是最小值，bug定位中...
// 函数名也有问题——findExtremeValue 可以是最大值也可以是最小值，应该叫 findMinimum
int findMinimum(const std::vector<int>& v) {
    return *std::min_element(v.begin(), v.end());  // 注释：返回最大值
}

// ❌ 解释"是什么"而非"为什么"的注释
// ❌ 注释的是代码逻辑，而不是意图和背景
// 这些事情代码本身就能说清楚！

// ✅ 好的注释——解释"为什么"，解释代码说不清楚的东西

// 为什么：处理货币计算时需要精确到分，不走浮点数路线
// 这是财务合规要求，审计发现的Issue #4521
// 浮点数在这个场景下会产生舍入误差（比如0.1 + 0.2 != 0.3）
const long long cents = static_cast<long long>(amount * 100 + 0.5);

// 为什么：这个接口有线程安全问题，不能并发调用
// 历史教训：Issue #1023，并发调用导致用户余额丢失
// TODO(#2019): 移除这个互斥锁，改为无锁设计
std::mutex balance_mutex_;
double getBalance() const {
    std::lock_guard<std::mutex> lock(balance_mutex_);
    return balance_;
}
```

### 35.3.2 注释的类型与写法

好的代码注释分为几类，每类有不同的写法：

```cpp
// ==================== 1. 文件头注释 ====================
// @file   payment_processor.cpp
// @brief  支付处理模块，负责对接第三方支付渠道
// @author 张三（zhangsan@example.com）
// @date   2024-01-15
//
// 支持的支付渠道：
//   - 支付宝（Alipay）
//   - 微信支付（WeChat Pay）
//   - 银联（UnionPay）
//
// 注意事项：
//   - 所有支付操作必须记录审计日志
//   - 失败重试次数上限为3次
//   - 交易超时时间为30秒
//
// =============================================

// ==================== 2. 函数/类文档注释 ====================
/// @brief 计算两点之间的欧几里得距离
/// @param p1 第一个点的坐标
/// @param p2 第二个点的坐标
/// @return 两点之间的距离（double类型）
///
/// @note 如果你需要的是曼哈顿距离，请使用 manhattanDistance() 函数
///
/// @example
/// @code
/// Point a{0, 0}, b{3, 4};
/// double d = euclideanDistance(a, b);  // 返回 5.0
/// @endcode
double euclideanDistance(const Point& p1, const Point& p2) {
    const double dx = p2.x - p1.x;
    const double dy = p2.y - p1.y;
    return std::sqrt(dx * dx + dy * dy);
}

// 或者用更现代的doxygen风格
/**
 * @class UserService
 * @brief 用户管理服务类
 *
 * 负责处理所有与用户相关的业务逻辑，包括：
 * - 用户注册与登录
 * - 用户信息查询与修改
 * - 用户权限管理
 *
 * @note 该类是线程安全的，所有public方法都是const或自带锁
 * @warning 不要直接构造，使用 UserService::getInstance() 获取单例
 */
class UserService {
    // ...
};

// ==================== 3. 行内注释（用于解释复杂逻辑） ====================
double double_compensation = base_salary
    * (1.0 + performance_factor)   // 绩效系数：0.0 ~ 2.0
    * (1.0 + years_of_service / 100.0);  // 年资奖励：每年加1%，封顶20%

// 使用括号把注释和代码绑定，即使代码被移动也不容易出错
```

### 35.3.3 TODO和标记的规范使用

项目中常见的特殊注释标记，也要规范使用：

```cpp
// TODO：需要实现的功能
// TODO(#issue号): 具体描述
// TODO(low): 优化建议（low/medium/high表示优先级）

// FIXME：已知的bug，需要修复
// FIXME(critical): 严重的内存泄漏问题（critical/high/medium/low）
// FIXME(#1234): 关联特定issue

// HACK：临时的变通方案，不够优雅但能工作
// HACK: 这个逻辑在JDK 8有bug，需要等升级后重写

// NOTE：给代码审查者的备注
// NOTE: 这个函数是线程安全的，调用者不需要加锁

// 如果你用IDE（如CLion），这些TODO会自动高亮并收集
// 推荐统一使用这种带优先级和issue号的格式，方便追踪
```

## 35.4 类与结构体设计规范

### 35.4.1 类的结构组织：成员按逻辑分组

一个设计良好的类，成员变量的排列应该遵循固定的顺序，访问权限从public到private，让阅读者一步步深入细节：

```cpp
// 推荐：按 public -> protected -> private 排列
// 每个区块内，按以下顺序组织：
// 1. 类型别名（using/typedef）
// 2. 静态常量/静态变量
// 3. 构造函数和析构函数
// 4. 普通成员函数
// 5. 数据成员

/// @brief 线程安全的消息队列
/// @tparam T 队列中元素的类型
template<typename T>
class ThreadSafeQueue {
public:
    // ==================== 公开接口 ====================
    using value_type = T;
    using size_type = std::size_t;

    /// @brief 默认构造函数
    ThreadSafeQueue() = default;

    /// @brief 禁止拷贝（队列不支持跨线程共享拷贝）
    ThreadSafeQueue(const ThreadSafeQueue&) = delete;
    ThreadSafeQueue& operator=(const ThreadSafeQueue&) = delete;

    /// @brief 移动语义支持
    ThreadSafeQueue(ThreadSafeQueue&& other) noexcept;
    ThreadSafeQueue& operator=(ThreadSafeQueue&& other) noexcept;

    // 普通成员函数（public API）
    void push(const T& value);
    void push(T&& value);

    /// @brief 尝试弹出一个元素
    /// @param out 输出的目标变量
    /// @return 是否成功弹出（false表示队列为空）
    bool tryPop(T& out);

    /// @brief 检查队列是否为空
    bool empty() const {
        std::lock_guard<std::mutex> lock(mutex_);
        return queue_.empty();
    }

    size_type size() const;

protected:
    // ==================== 派生类可用 ====================
    /// @brief 派生类可覆盖的清理钩子
    virtual void onClear() {}

private:
    // ==================== 实现细节 ====================
    mutable std::mutex mutex_;
    std::queue<T> queue_ GUARDED_BY(mutex_);  // GUARDED_BY是线程安全标注

    // 内部辅助函数
    void notifyNotEmpty();
};
```

### 35.4.2 构造函数的设计原则

```cpp
// ❌ 构造函数做太多事——违反单一职责
class User {
public:
    User(const std::string& name, const std::string& email) {
        // 又是验证，又是数据库操作，又是发邮件...
        // 这让类难以测试，难以复用
        validateName(name);
        validateEmail(email);
        saveToDatabase(name, email);  // 为什么要在这里连数据库？
        sendWelcomeEmail(email);       // 为什么要在这里发邮件？
    }
};

// ✅ 现代C++构造函数的最佳实践

class User {
public:
    // 1. 使用成员初始化列表（效率更高）
    // 2. 构造函数尽量简单，只做"赋值"而非"计算"
    // 3. 用explicit防止隐式转换
    // 4. 提供委托构造函数减少代码重复

    // 主要构造函数：验证在单独的工厂函数里做
    explicit User(std::string name, std::string email)
        : name_(std::move(name))
        , email_(std::move(email))
    {}

    // 静态工厂方法：构造逻辑集中在这里
    static std::optional<User> create(std::string name, std::string email) {
        if (!validateName(name) || !validateEmail(email)) {
            return std::nullopt;
        }
        return User(std::move(name), std::move(email));
    }

    // 默认构造函数：总是显式写出，即使等于default
    User() = default;

    // 移动语义
    User(User&&) = default;
    User& operator=(User&&) = default;

private:
    std::string name_;
    std::string email_;

    static bool validateName(const std::string& name);
    static bool validateEmail(const std::string& email);
};
```

### 35.4.3 访问控制与封装

**让成员变量 private，给成员函数 public**——这是封装的金科玉律。如果你的类有一堆 public 成员变量，那它本质上就是一个"带函数的struct"，失去了类的封装意义。

```cpp
// ❌ "裸体"的类——数据完全暴露，外界可以随意修改
struct Point {
    double x;   // 任何人可以直接改
    double y;   // 没人知道这个值什么时候是合法的
};
point.x = 1000000;  // 野值！谁负责验证？

// ✅ "穿好衣服"的类——数据受保护，接口定义行为
class Point {
public:
    // 构造函数确保对象从一开始就是合法的
    Point(double x, double y) : x_(x), y_(y) {}

    // 只读的访问器
    double x() const { return x_; }
    double y() const { return y_; }

    // 受控的修改接口——可以在这里加验证
    void setX(double x) {
        if (x < -1000 || x > 1000) {
            throw std::out_of_range("X coordinate out of range");
        }
        x_ = x;
    }

    void setY(double y) {
        if (y < -1000 || y > 1000) {
            throw std::out_of_range("Y coordinate out of range");
        }
        y_ = y;
    }

private:
    double x_;
    double y_;
};
```

### 35.4.4 五大特殊成员函数：Rule of Five

在C++11及以后，如果你的类需要自定义析构函数、拷贝或移动操作，通常需要全部五个（C++11前是三个——Rule of Three）。忘记这一点是常见的bug来源：

```cpp
// ❌ Rule of Three/Five被遗忘的典型案例
class ResourceHandle {
public:
    ResourceHandle() {
        resource_ = allocateResource();
    }

    ~ResourceHandle() {
        freeResource(resource_);
    }

    // 没有声明拷贝/移动构造和赋值运算符
    // 编译器会生成浅拷贝版本，导致双重释放！
private:
    Resource* resource_;
};

// 某天某人在代码里写了：
void process(ResourceHandle h) { /* ... */ }  // 传值，触发拷贝
ResourceHandle handle;
process(handle);  // handle被拷贝，resource被释放两次！
// 💥 灾难发生

// ✅ 正确做法：Rule of Five/C++11版本
class ResourceHandle {
public:
    ResourceHandle() : resource_(allocateResource()) {}

    ~ResourceHandle() {
        freeResource(resource_);
    }

    // 显式删除拷贝（持有独占资源，禁止共享）
    ResourceHandle(const ResourceHandle&) = delete;
    ResourceHandle& operator=(const ResourceHandle&) = delete;

    // 支持移动语义
    ResourceHandle(ResourceHandle&& other) noexcept
        : resource_(other.resource_) {
        other.resource_ = nullptr;  // 转移所有权
    }

    ResourceHandle& operator=(ResourceHandle&& other) noexcept {
        if (this != &other) {
            freeResource(resource_);
            resource_ = other.resource_;
            other.resource_ = nullptr;
        }
        return *this;
    }

    // 如果你用智能指针，上面的都可以简化：
    // std::unique_ptr<Resource> resource_;  // 自动Rule of Five
    // 移动语义由unique_ptr自动提供，拷贝被隐式删除

private:
    Resource* resource_;
};
```

### 35.4.5 继承与组合：优先组合

**"组合优先于继承"** 是面向对象设计的黄金法则之一。继承会让类之间形成强耦合，而且容易被滥用。

```cpp
// ❌ 滥用继承的典型例子
class Dog : public Animal {
public:
    void bark() { /* ... */ }
    // Dog is-a Animal? 合理
};

class RobotDog : public Dog {
    // RobotDog is-a Dog is-a Animal?
    // 机器人会吃东西吗？需要呼吸吗？
    // 继承链越来越长，行为越来越难理解
};

// ✅ 优先用组合——"has-a" 优于 "is-a"
// 注意：基类标记为 final，因为没有类会进一步继承它
class BarkBehavior final {
public:
    virtual ~BarkBehavior() = default;
    virtual void bark() const = 0;
};

class LoudBark : public BarkBehavior {
public:
    void bark() const override { std::cout << "WOOF! WOOF!\n"; }
};

class QuietBark : public BarkBehavior {
public:
    void bark() const override { std::cout << "yip...\n"; }
};

class RobotDog {
public:
    explicit RobotDog(std::unique_ptr<BarkBehavior> bark_behavior)
        : bark_behavior_(std::move(bark_behavior)) {}

    void performBark() const {
        if (bark_behavior_) {
            bark_behavior_->bark();
        }
    }

private:
    std::unique_ptr<BarkBehavior> bark_behavior_;  // 组合
};

// 组合的优势：
// 1. 运行时可以切换行为（RobotDog可以"换"叫声）
// 2. 类之间的耦合更松
// 3. 更容易测试（可以注入mock的BarkBehavior）
```

## 35.5 函数设计规范

### 35.5.1 函数的单一职责：一个函数只做一件事

**函数的第一天条**：一个函数只做一件事，而且要做得漂亮。超过20-30行的函数就应该考虑拆分了。

```cpp
// ❌ "万能函数"——一个函数干了十件事
void processUser(const User& user) {
    // 1. 验证
    if (user.name.empty()) return;
    if (user.age < 0 || user.age > 150) return;
    // 2. 格式化
    std::string formatted = user.name;
    formatted[0] = toupper(formatted[0]);
    // 3. 保存到数据库
    db.execute("INSERT ...", ...);
    // 4. 发送邮件通知
    email.send(user.email, "Welcome!");
    // 5. 更新缓存
    cache.set(user.id, user);
    // 6. 记录日志
    logger.info("User processed: " + user.id);
    // ... 越来越长，越来越难维护
}

// ✅ 拆分成多个小函数——每个函数只做一件事
void processUser(const User& user) {
    validateUser(user);           // 只验证
    auto formatted = formatUserName(user.name);  // 只格式化名字
    saveToDatabase(user);        // 只操作数据库
    sendWelcomeNotification(user);  // 只发送通知
    updateUserCache(user);        // 只更新缓存
}

// ✅ 现代C++用std::optional让错误处理更优雅
std::optional<UserError> validateUser(const User& user) {
    if (user.name.empty()) {
        return UserError::EmptyName;
    }
    if (user.age < 0 || user.age > 150) {
        return UserError::InvalidAge;
    }
    return std::nullopt;  // 验证通过
}

void processUser(const User& user) {
    if (auto error = validateUser(user)) {
        handleValidationError(*error);
        return;
    }
    // 验证通过，继续处理
}
```

### 35.5.2 参数传递规范：传值还是传引用？

这是C++最让人纠结的话题之一。让我用一个简单的规则解决它：**对于输入参数，用 `const T&`；对于输出参数，用 `T*` 或 `T&`**。对于内置类型（int、double等），直接传值。

```cpp
class Rectangle {
public:
    // ❌ 错误：函数没有标记 const，意味着调用者需要担心"这个函数会不会偷偷改我的 Rectangle"
    double computeArea(double width, double height);

    // ✅ 正确：对于类类型用 const&，对于内置类型直接传值
    double computeArea(double width, double height) const {
        return width * height;  // 内置类型直接传值即可，无需加 const
    }

    // ❌ 糟糕：没有标记const，意味着调用者需要担心"我的对象被改了吗？"
    void setColor(Color c);

    // ✅ 好：const成员函数承诺不修改对象状态
    void setColor(Color c) { color_ = c; }
    Color getColor() const { return color_; }  // get也要const——不修改状态

    // ==================== 输出参数 vs 返回值 ====================
    // ❌ 用输出参数返回值（老C风格）
    bool findUser(int id, User& out_user);

    // ✅ 直接返回（现代C++风格，更清晰）
    std::optional<User> findUser(int id);

    // 如果返回多个值，有三种选择：
    // 1. std::tuple<std::string, int, double>
    // 2. struct/class（推荐：给返回值命名）
    // 3. std::pair（勉强可以接受，但字段含义不明确，需要注释说明）
    // pair语义示例：{bool 成功标志, string 成功时为解析结果/失败时为错误信息}
    std::pair<bool, std::string> tryParse(const std::string& input);

    // 更好的做法——用结构体给返回值命名
    struct ParseResult {
        bool success;
        std::string error_message;
        int parsed_value;
    };

    ParseResult parseInput(const std::string& input);
    // 调用时：auto [ok, err, val] = parseInput(input); // C++17结构化绑定
};
```

### 35.5.3 返回值规范：RAII与错误处理

```cpp
// ❌ 返回裸指针——调用者不知道是否需要delete
Widget* createWidget() {
    return new Widget();
}

// ✅ 返回智能指针——内存管理自动完成
std::unique_ptr<Widget> createWidget() {
    return std::make_unique<Widget>();
}

// ✅ 或者直接返回值（C++17的优化让移动更高效）
// 对于小对象，直接返回比用unique_ptr更高效
struct Point { double x, y; };
Point createPoint(double x, double y) {
    return Point{x, y};  // 编译器优化：直接构造在调用者的内存里
}

// ==================== 错误处理规范 ====================
// 1. 用std::optional表示"可能有值，也可能没有"
std::optional<User> findUserById(int id);

// 2. 用std::expected (C++23) 表示"要么成功返回值，要么失败"
std::expected<User, std::string> authenticate(const std::string& name,
                                               const std::string& password);

// 3. 用异常表示"真正的异常情况"（不是正常流程分支）
//    正常流程分支不要用异常！
//    异常 = 真正意外的错误（内存不足、文件丢失）
//    返回值 = 正常的业务逻辑结果（用户不存在、密码错误）

// ❌ 滥用异常——把异常当返回值用
try {
    auto user = findUserById(id);
    if (!user) {
        throw std::runtime_error("User not found");  // 业务错误不用异常
    }
} catch (const std::runtime_error& e) {
    // User not found 是正常情况，不应该用异常！
}

// ✅ 正确用法：业务错误用返回值，异常留给真正的意外
auto result = authenticate(username, password);
if (!result) {
    std::cerr << "认证失败: " << result.error() << "\n";  // 处理正常错误
    return;
}

try {
    auto data = loadCriticalData();  // 磁盘坏了、网络断了——这是异常
} catch (const std::exception& e) {
    // 真正无法恢复的错误，做兜底处理
}
```

## 35.6 内存管理规范

### 35.6.1 优先使用智能指针而非裸指针

这是现代C++最重要的规范之一。在C++11及以后，**永远不要用 `new` 和 `delete`**——让智能指针帮你处理内存。

```cpp
// ❌ 裸指针的危险：谁负责delete？什么时候delete？
Widget* p = new Widget();
processWidget(p);
// ... 代码越来越长，p的delete淹没在代码海洋里...
delete p;  // 如果有人提前return了怎么办？如果抛异常了怎么办？

// ✅ 用智能指针——delete自动搞定，异常安全
void goodFunction() {
    auto widget = std::make_unique<Widget>();  // 独占所有权
    processWidget(*widget);  // 解引用获取对象
    // 函数结束，widget自动销毁，无需手动delete
}

// ==================== std::unique_ptr vs std::shared_ptr ====================
// std::unique_ptr：独占语义，轻量，无引用计数开销
// 首选！除非你需要共享所有权，才考虑shared_ptr
std::unique_ptr<Config> loadConfig(const std::string& path) {
    return std::make_unique<Config>(path);
}

// std::shared_ptr：共享所有权，有引用计数（原子操作，有性能成本）
// 只有在"确实需要多个owner"时才用
class Node {
public:
    void addChild(std::shared_ptr<Node> child) {
        children_.push_back(child);
        child->parent_ = shared_from_this();  // 需要被shared_ptr管理才能用
    }
private:
    std::vector<std::shared_ptr<Node>> children_;
    std::weak_ptr<Node> parent_;  // 用weak_ptr打破循环引用
};

// ❌ 永远不要这样用shared_ptr——不知道所有权归谁
void process(shared_ptr<Widget> p);  // 这个函数会复制引用计数
void process(Widget* p);  // 裸指针，不知道是不是shared_ptr管理的

// ✅ 推荐：用裸指针作为观察，用unique_ptr作为所有者
class Owner {
public:
    explicit Owner(std::unique_ptr<Widget> w) : widget_(std::move(w)) {}

    // 允许外界观察widget，但不允许拥有
    Widget* getWidget() const { return widget_.get(); }
    const Widget* peekWidget() const { return widget_.get(); }  // 只读观察

    // 更好的做法：用引用代替观察用的指针
    const Widget& widget() const { return *widget_; }  // 不返回指针，避免垂空

private:
    std::unique_ptr<Widget> widget_;  // 唯一owner
};

```

### 35.6.2 避免内存泄漏的检查清单

```cpp
// ==================== 常见内存泄漏及对策 ====================

// 1. 异常安全：任何可能抛异常的代码，都要考虑异常发生时是否有泄漏
void dangerous() {
    Resource* r = acquireResource();  // 分配了
    process(r);                        // 如果这里抛异常，r就泄漏了！
    releaseResource(r);                // 永远不会执行到
}

// ✅ 用RAII包装资源
void safe() {
    std::unique_ptr<Resource, decltype(&releaseResource)>
        r(acquireResource(), releaseResource);  // 退出作用域自动释放
    process(r.get());
}

// 更好的方式：自己写RAII类或用标准库的锁
void safeWithLock() {
    std::lock_guard<std::mutex> lock(mutex_);
    process();
    // 抛异常？lock_guard保证析构函数被调用，锁被释放
}

// 2. 容器管理：优先用容器而不是手动new数组
// ❌
Widget** widgets = new Widget*[100];
// ...
delete[] widgets;

// ✅
std::vector<std::unique_ptr<Widget>> widgets;
widgets.push_back(std::make_unique<Widget>());

// 3. 循环引用：用weak_ptr打破
// ❌ 循环引用导致泄漏
class Parent;
class Child;
std::shared_ptr<Parent> p = std::make_shared<Parent>();
std::shared_ptr<Child> c = std::make_shared<Child>();
p->child = c;  // Parent持有一个shared_ptr<Child>
c->parent = p; // Child持有一个shared_ptr<Parent>，引用计数永远不为0！

// ✅ 用weak_ptr
c->parent = p;  // weak_ptr不增加引用计数
```

## 35.7 现代C++最佳实践

### 35.7.1 auto：朋友还是敌人？

`auto` 是 C++11 引入的关键字，它让编译器推断类型，省去冗长的类型名。但它也是一把双刃剑——用得好是偷懒神器，用得不好是bug温床。

```cpp
// ✅ auto的合理使用场景
auto i = 42;                          // int
auto d = 3.14;                        // double
auto s = std::string("hello");        // 避免冗长的类型名
auto v = std::vector<int>{1, 2, 3};   // 迭代器类型太长
auto result = computeSomething();     // 返回类型明确时用auto

// ✅ auto在范围for循环中特别有用
std::map<std::string, std::vector<int>> data;
// 不用auto：
for (std::pair<const std::string, std::vector<int>>& kv : data) { ... }
// 用auto：简洁又清晰
for (auto& [key, value] : data) {  // C++17结构化绑定
    // ...
}

// ❌ auto的滥用——类型变得不清晰
auto result = calculate();    // calculate()返回什么？鬼知道！
auto ptr = new char[100];    // char*? 这是故意的吗？
auto x;                      // 编译错误：auto需要初始化

// ❌ auto推断出不是你想要的类型
std::vector<bool> flags{true, false, true};
auto flag = flags[0];        // std::vector<bool>的operator[]返回代理对象！
// flag 实际上是 std::vector<bool>::reference，不是bool！
// 这种情况应该用 auto&& 或 explicit bool

auto&& flag = flags[0];      // ✅ 用auto&&绑定代理对象
bool explicit_flag = static_cast<bool>(flags[0]);  // ✅ 或显式转换

// 总结：auto适合"类型名太长"或"类型显而易见"的场景
// 不要用auto替代"你不知道返回值的类型"的懒人做法
```

### 35.7.2 constexpr：编译时计算

用 `constexpr` 标记可以在编译期计算的常量和函数，让计算"提前完成"：

```cpp
// ❌ 普通const：编译期常量 or 运行期常量？看编译器心情
const int size = 100;            // 编译期常量
const int getSize() { return 100; }           // 运行期const
const int getSize() const { return 100; }     // 运行期const

// ✅ constexpr：明确要求编译期计算
constexpr int ARRAY_SIZE = 100;  // 编译期常量，可以用来定义数组大小
constexpr int factorial(int n) {
    int result = 1;
    for (int i = 2; i <= n; ++i) {
        result *= i;
    }
    return result;
}

int arr[factorial(5)];  // ✅ 编译期就计算出factorial(5)=120，数组大小固定

// ✅ C++17/20的constexpr进化
// C++17: constexpr lambda
constexpr auto add = [](int a, int b) constexpr { return a + b; };

// C++20: constexpr virtual函数和动态内存
// C++23: constexpr try-catch (GCC 14+, Clang 17+)
constexpr int parseInt(const char* s) {
    int result = 0;
    int sign = 1;
    if (*s == '-') { sign = -1; ++s; }
    while (*s) {
        result = result * 10 + (*s - '0');
        ++s;
    }
    return result * sign;
}

static_assert(parseInt("12345") == 12345, "Compile-time parsing works!");
```

### 35.7.3 nullptr vs NULL vs 0

**在C++11及以后，永远用 `nullptr`**。这是最简单的规范，但总有人记不住。

```cpp
// ❌ C风格：用 NULL 或 0 表示空指针
Widget* w1 = NULL;   // 在C++11之前，NULL就是整数0，容易产生重载歧义
Widget* w2 = 0;      // 0可以匹配int重载的函数，导致歧义
void foo(int);
void foo(Widget*);
foo(0);    // 哪个foo？0既可以转int也可以转Widget*！

// ✅ C++11+：用nullptr
Widget* w = nullptr;  // 专门的空指针类型 decltype(nullptr)
foo(nullptr);         // 明确调用Widget*版本

// nullptr的好处：
// 1. 类型安全：不会意外匹配int
// 2. 可读性好：看到nullptr就知道是空指针
// 3. 作用域正确：::nullptr是全局的，NULL可能被宏覆盖
```

### 35.7.4 override和final：显式标记继承语义

```cpp
class Base {
public:
    virtual void draw() const;
    virtual ~Base() = default;
};

class Derived : public Base {
public:
    // ❌ 没加override——不知道这个函数是override的
    // 以后重构Base时如果改了签名，这里不会报错
    void draw();  // 悄悄变成了重载而不是覆盖！危险！

    // ✅ 加了override——编译器帮你检查
    void draw() const override {
        // 正确：Base::draw()就是const void draw()
        Base::draw();
    }
};

// ==================== final：禁止继续继承/重写 ====================
class NonInheritable : public Base {
public:
    void draw() const override final {  // 禁止Derived继续重写draw
        // ...
    }
};

// class FinalClass final { ... };  // 禁止任何类继承FinalClass

// final的好处：
// 1. 编译器可以据此做更激进的优化
// 2. 明确表达设计意图："这个不要改了"
// 3. 防止意外继承导致的问题
```

## 35.8 代码审查与团队协作

### 35.8.1 提交信息规范

Git提交信息是代码的" ChangeLog"，好的提交信息让你一年后还能快速定位问题：

```bash
# ❌ 糟糕的提交信息
$ git commit -m "fix"
$ git commit -m "update"
$ git commit -m "changes"
$ git commit -m "asdfghjkl"  # 键盘打滑？

# ✅ 规范的提交信息（Angular风格）
$ git commit -m "fix(auth): 修复登录页在Safari下无法输入的问题"
$ git commit -m "feat(payment): 新增微信支付V3接口支持"
$ git commit -m "refactor(user): 重构UserService.extractAvatar()为独立函数"
$ git commit -m "docs(readme): 更新编译说明文档"
$ git commit -m "perf(cache): 用LRU缓存替换FIFO，命中提升40%"

# 格式：<type>(<scope>): <subject>
# type: feat/fix/docs/style/refactor/test/perf/chore
# scope: 影响范围（模块名/文件名）
# subject: 简短描述（不超过50字，动词开头）
```

### 35.8.2 提交前的自检清单

在提交代码前，用这个清单过一遍：

```cpp
// 1. 代码能编译吗？✅
// 2. 所有测试通过了吗？✅
// 3. 新代码有对应的单元测试吗？✅
// 4. 命名是否与项目规范一致？✅
// 5. 是否有新的编译警告？✅
// 6. 注释是否更新了？✅
// 7. TODO/FIXME标记是否处理了？✅
// 8. 敏感信息（密码/密钥）是否移除了？✅
// 9. 代码格式化工具跑了吗？✅
// 10. 提交信息符合规范吗？✅

// 推荐：设置pre-commit hook（Git hooks）自动检查
// .git/hooks/pre-commit 示例（检查编译+格式+测试）
#!/bin/bash
set -e
cmake --build build --target all  # 编译
cmake --build build --target test # 测试
clang-format --dry-run --Werror src/*.cpp  # 格式检查
```

## 本章小结

本章我们系统地学习了C++编码规范的核心内容，这些规范是无数前人踩坑后总结出来的经验教训：

1. **命名规范**：变量名、函数名、类名要有意义；选择一个命名风格（推荐snake_case或camelCase），全团队统一；避免单字母、含义模糊的名称；特别注意下划线开头的名字是编译器保留区域。

2. **代码格式化**：缩进统一用空格（4空格），控制每行长度不超过100字符；选择一种花括号风格（推荐K&R 1TBS）并严格遵循；善用空行分隔逻辑块；使用 `clang-format` 自动化格式化。

3. **注释与文档**：注释解释"为什么"而非"是什么"；保持注释与代码同步，过时的注释比没注释更有害；用标准格式（Doxygen）写API文档；统一使用 `TODO`、`FIXME`、`NOTE` 等标记。

4. **类设计**：按 `public -> protected -> private` 顺序组织成员；数据成员永远 `private`；遵守 Rule of Five/C++11 Rule of Zero；优先组合而非继承。

5. **函数设计**：每个函数只做一件事；输入参数用 `const T&`，输出用 `T*`/`T&` 或直接返回值；用 `std::optional` 和 `std::expected` 处理"可能失败"的场景。

6. **内存管理**：永远用智能指针代替裸 `new`/`delete`；`std::unique_ptr` 优先，`std::shared_ptr` 慎用；用 `weak_ptr` 打破循环引用；优先栈上分配而非堆分配。

7. **现代C++最佳实践**：用 `auto` 但别滥用；用 `constexpr` 做编译期计算；永远用 `nullptr` 而非 `NULL` 或 `0`；用 `override`/`final` 显式标记虚函数行为。

8. **团队协作**：提交信息遵循规范格式；提交前自检；善用pre-commit hooks自动化检查。

> **最后的忠告**：编码规范不是圣经，不要为了"符合规范"而把代码改得面目全非。规范的目的是**让代码更易读、易维护、易协作**——如果某条规范在你的场景下反而降低了可读性，那就勇敢地打破它，然后记录下为什么。
>
> 但在那之前，先学会规则、了解规则的意图。只有理解了"为什么"，你才有资格说"这个场景下例外"。

记住：**好的代码规范，让团队协作像跳舞；坏的代码规范，让团队协作像踩踏**。愿你的代码永远整洁优雅，永不成为后人的噩梦！🎉