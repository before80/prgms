+++
title = "第11章 类与对象基础"
weight = 110
date = "2026-03-29T21:03:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++
# 第11章 类与对象基础

## 11.1 面向对象编程概述

嘿，未来的C++大师！在正式踏入类的世界之前，咱们先来聊聊面向对象编程（Object-Oriented Programming，简称OOP）这个听起来很高大上的概念。别担心，我会把它解释得连你家的猫都能听懂——如果你的猫恰好会编程的话。

### 类与对象的概念

想象一下，你是一个烘焙师，你要做一批小熊饼干。你会怎么做？首先要有一个模具对吧？用这个模具，你可以压出无数个一模一样的小熊饼干。这个**模具**就是**类（Class）**，而用这个模具压出来的**每一个饼干**就是**对象（Object）**。

类，就好比是一份神奇的蓝图。它告诉你："嘿，这只熊有圆圆的脑袋、两只耳朵、还有一个傻乎乎的微笑。"而对象，就是按照这个蓝图真实制造出来的实物，有自己的名字（比如"R2-D2熊"），自己的电池电量，等等。

在C++中，`class`关键字就是用来定义这种蓝图的。蓝图里包含了两大宝贝：

- **成员变量（Member Variables）**：也叫属性，就是描述对象长什么样的数据。比如熊的名字、颜色、电量。
- **成员函数（Member Functions）**：也叫方法，就是对象能干什么。比如熊能自我介绍、能充电。

```cpp
#include <iostream>
#include <string>

// 类：抽象的数据类型，定义对象的"蓝图"
// 对象：类的实例，具体的存在
// 简单理解：类就是模具，对象就是用模具压出来的饼干！

class Robot {
public:
    // 成员变量（属性）- 描述机器人长什么样/有什么数据
    std::string name;      // 名字：R2-D2、大白、或者"笨笨"
    int battery_level;     // 电量：0-100，别让TA饿着
    bool is_active;        // 是否正在工作
    
    // 成员函数（方法）- 描述机器人能干什么
    void introduce() {
        std::cout << "I am " << name << "!" << std::endl;
    }
    
    void charge() {
        battery_level = 100;
        std::cout << name << " is fully charged!" << std::endl;
    }
};

int main() {
    // 创建对象（类的实例）- 用模具压出真实的小熊饼干！
    Robot r2d2;
    
    // 访问成员变量 - 给这个机器人设置属性
    r2d2.name = "R2-D2";
    r2d2.battery_level = 75;
    r2d2.is_active = true;
    
    // 调用成员函数 - 让机器人干活！
    r2d2.introduce();  // 输出: I am R2-D2!
    r2d2.charge();      // 输出: R2-D2 is fully charged!
    
    return 0;
}
```

运行结果：

```
I am R2-D2!
R2-D2 is fully charged!
```

> 小提示：创建对象的过程叫做**实例化（Instantiation）**，就像工厂里流水线生产产品一样，只不过这里的产品都是数据结构的"复制品"。

### 封装、继承、多态

如果说类是面向对象大厦的砖头，那么**封装、继承、多态**就是这三块砖头之间永恒的三角恋关系。咳咳，我是说，这三大特性是面向对象编程的核心支柱。

**1. 封装（Encapsulation）** - 把东西打包卖，顾客不需要知道里面是什么

想象你去买手机。你按下开机键，屏幕亮了。但你并不需要知道手机内部CPU怎么运作、内存怎么读写、屏幕像素怎么排列——这些细节都被"封装"在手机内部了。你只需要关心按钮在哪、屏幕多大、电池能用多久。

在C++中，封装就是用`public`和`private`关键字把数据和操作包装在一起，对外只暴露必要的接口，隐藏内部实现细节。就像一个自动贩卖机，你只管投钱按按钮，不需要知道里面齿轮怎么转、弹簧怎么弹。

**2. 继承（Inheritance）** - 龙生龙，凤生凤，老鼠的儿子会打洞

生物学里，狗妈妈生出小狗，小狗会"继承"狗妈妈的一些特征：四条腿、一条尾巴、见到骨头就走不动道。编程里的继承也是这样！

你可以从一个"基类"（也叫父类）派生出"派生类"（也叫子类）。派生类会自动获得父类的所有特性，还能添加自己独有的东西。就像"动物"是一个父类，"狗"继承它就有了"能叫"的能力，"猫"继承它就有了"傲娇"的能力。

**3. 多态（Polymorphism）** - 同一个动作，不同的表现

"叫一声！"这个命令对狗和猫有不同的效果：狗"汪！"，猫"喵~"。同一个消息（叫一声），不同的对象有不同的响应——这就是多态。

在C++中，多态通过**虚函数（virtual function）**来实现。就像一张遥控器（基类指针），你按播放键，它会根据实际遥控的是电视还是音响来执行不同的操作。

```cpp
#include <iostream>
#include <string>

// 面向对象三大特性：
// 1. 封装(Encapsulation)：把数据和操作包装在一起，对外隐藏细节
//    就像外卖打包，你不需要知道厨师怎么炒菜的
// 2. 继承(Inheritance)：从已有类创建新类，复用代码
//    就像儿子继承父亲的房产和秃头基因
// 3. 多态(Polymorphism)：不同对象对同一消息有不同响应
//    就像不同乐器演奏同一个音符，声音各不相同

class Animal {
protected:  // protected: 派生类可以访问，外部不能访问
    // 为什么用protected而不是private？因为派生类需要访问啊！
    std::string name_;  // 名字
    int age_;           // 年龄
    
public:
    // 构造函数：创建动物对象时必须提供名字和年龄
    Animal(const std::string& name, int age) : name_(name), age_(age) {}
    
    // 虚函数：派生类可以重写（override）
    // virtual关键字就像是给编译器一个"提示"：这个函数可能会被改写
    virtual void speak() const {
        std::cout << name_ << " makes a sound" << std::endl;
    }
    
    // 虚析构函数：确保删除派生类对象时能正确调用析构函数
    // 这是C++的"安全带"，不系可能会有生命危险（内存泄漏）
    virtual ~Animal() {}
};

class Dog : public Animal {
public:
    // 派生类的构造函数需要调用基类的构造函数
    Dog(const std::string& name, int age) : Animal(name, age) {}
    
    // 重写父类的speak方法 - 汪汪汪！
    void speak() const override {
        std::cout << name_ << " says: Woof!" << std::endl;
    }
};

class Cat : public Animal {
public:
    Cat(const std::string& name, int age) : Animal(name, age) {}
    
    // 重写父类的speak方法 - 喵喵喵！
    void speak() const override {
        std::cout << name_ << " says: Meow!" << std::endl;
    }
};

int main() {
    Dog buddy("Buddy", 3);       // 创建一个叫Buddy的3岁狗狗
    Cat whiskers("Whiskers", 2); // 创建一个叫Whiskers的2岁猫咪
    
    // 多态的经典用法：用基类指针数组管理不同派生类对象
    Animal* animals[] = {&buddy, &whiskers};
    
    std::cout << "=== 多态演示 ===" << std::endl;
    for (auto* animal : animals) {
        animal->speak();  // 多态：不同对象调用同一方法有不同行为
    }
    // 输出:
    // Buddy says: Woof!
    // Whiskers says: Meow!
    
    std::cout << "\n=== 解释 ===" << std::endl;
    std::cout << "同样是调用speak()，狗和猫的反应完全不同！" << std::endl;
    std::cout << "这就是多态的魅力：一个接口，多种形态。" << std::endl;
    
    return 0;
}
```

运行结果：

```
=== 多态演示 ===
Buddy says: Woof!
Whiskers says: Meow!

=== 解释 ===
同样是调用speak()，狗和猫的反应完全不同！
这就是多态的魅力：一个接口，多种形态。
```

> 对比一下：如果没有多态，你可能需要写一堆if-else来判断对象类型，然后再调用对应的函数。有了多态，代码简洁得像诗一样！

### 类不变式（Class Invariant）

想象一下，你有一个榨汁机。这个榨汁机有个规矩：桶里最多放10个水果，不能超过。超过了他就炸给你看（抛出异常）。这就是这个榨汁机的"使用规则"。

在编程里，**类不变式（Class Invariant）**就是对象从诞生（构造）到消亡（析构）整个生命周期都必须满足的条件。它就像是对象对自己立下的"誓言"：只要我还活着，我就保证满足这些条件。

拿我们熟悉的`Stack`（栈）来举例。一个栈的不变式包括：

- 元素数量永远在0到capacity之间
- `top_`指针（指向栈顶）永远在有效范围内
- 栈空时`top_`是-1，栈满时`top_`是MAX_SIZE-1

```cpp
#include <iostream>
#include <stdexcept>

// 类不变式：对象从构造到销毁必须始终满足的条件
// 就像宪法是国家的不变式，任何法律都不能违反宪法
// 类不变式是类的"宪法"，成员函数必须维护它

// 例如：Stack类的不变式是"top_始终在[-1, MAX_SIZE-1)范围内"
class Stack {
private:
    static const int MAX_SIZE = 100;  // 最大容量
    int data_[MAX_SIZE];               // 存储数据的数组
    int top_;  // 栈顶指针，不变式：top_始终在[-1, MAX_SIZE-1)范围内，栈空时为-1
    
public:
    // 构造函数：初始化为空栈
    // invariant: top_ = -1 表示空栈
    Stack() : top_(-1) {}
    
    // 判断栈是否为空
    bool empty() const { return top_ == -1; }
    
    // 判断栈是否已满
    bool full() const { return top_ == MAX_SIZE - 1; }
    
    // 入栈：添加元素到栈顶
    void push(int value) {
        if (full()) {
            throw std::overflow_error("Stack overflow! 别塞了，桶满了！");
        }
        data_[++top_] = value;  // 先递增top_，再存入数据
        // push后：top_增加了，但仍然在有效范围内，不变式保持！
    }
    
    // 出栈：移除并返回栈顶元素
    int pop() {
        if (empty()) {
            throw std::underflow_error("Stack underflow! 桶是空的，拿个锤子！");
        }
        // pop前top_有效，pop后top_有效（减1了），不变式保持
        return data_[top_--];  // 先返回数据，再递减top_
    }
    
    // 查看栈顶元素（不移除）
    int peek() const {
        if (empty()) {
            throw std::underflow_error("Stack is empty! 空的，一滴都没有！");
        }
        return data_[top_];
    }
};

int main() {
    Stack s;
    
    std::cout << "=== 栈操作演示 ===" << std::endl;
    
    s.push(10);
    std::cout << "Pushed: 10" << std::endl;
    
    s.push(20);
    std::cout << "Pushed: 20" << std::endl;
    
    s.push(30);
    std::cout << "Pushed: 30" << std::endl;
    
    std::cout << "\nTop element: " << s.peek() << std::endl;  // 输出: Top: 30
    std::cout << "Pop: " << s.pop() << std::endl;   // 输出: Pop: 30
    std::cout << "Pop: " << s.pop() << std::endl;   // 输出: Pop: 20
    
    std::cout << "\n=== 不变式检查 ===" << std::endl;
    std::cout << "栈空? " << (s.empty() ? "是滴" : "不是") << std::endl;
    
    return 0;
}
```

运行结果：

```
=== 栈操作演示 ===
Pushed: 10
Pushed: 20
Pushed: 30

Top element: 30
Pop: 30
Pop: 20

=== 不变式检查 ===
栈空? 是滴
```

> 不变式的好处：它让你对对象的状态有信心。只要你遵守规则（调用方法前检查边界），对象就永远处于合法状态，程序就不会出现奇怪的bug。就像只要你按时吃饭，你的胃就会正常工作一样。

## 11.2 类的定义与对象的创建

现在你已经了解了面向对象的基本概念，是时候学习如何在C++中实际定义一个类并创建对象了。这一节我们会像建筑师一样，画出蓝图，然后按照蓝图建造房子。

### 在栈上创建对象 vs 在堆上创建对象

在C++中，创建对象有两种方式：

1. **栈上创建**（也叫自动存储期）：就像在栈上叠盘子，快速、 automatic（自动析构），但生命周期受作用域限制。
2. **堆上创建**（也叫动态存储期）：就像租仓库存货，用完得手动清理（`delete`），但生命周期你说了算。

```cpp
#include <iostream>
#include <string>

// 定义一个简单的Point类（点）
class Point {
public:
    // 成员变量：点的坐标
    double x;  // 横坐标
    double y;  // 纵坐标
    
    // 成员函数：设置坐标
    void setCoordinates(double xVal, double yVal) {
        x = xVal;  // 设置横坐标
        y = yVal;  // 设置纵坐标
    }
    
    // 成员函数：打印点的坐标
    void print() const {
        std::cout << "(" << x << ", " << y << ")" << std::endl;
    }
};

int main() {
    std::cout << "=== 栈上创建对象 ===" << std::endl;
    
    // 栈上创建对象 - 就像在桌子上放一个杯子
    Point p1;  // 创建一个Point对象p1，在栈上分配内存
    p1.x = 3.0;  // 设置x坐标
    p1.y = 4.0;  // 设置y坐标
    p1.print();  // 输出: (3, 4)
    
    std::cout << "\n=== 使用成员函数初始化 ===" << std::endl;
    
    // 另一种初始化方式：使用成员函数
    Point p2;  // 又在栈上创建一个Point对象
    p2.setCoordinates(5.0, 6.0);  // 调用成员函数设置坐标
    p2.print();  // 输出: (5, 6)
    
    std::cout << "\n=== 堆上创建对象 ===" << std::endl;
    
    // 堆上创建对象 - 就像租用一个仓库
    // new关键字：从堆（heap）分配内存
    Point* p3 = new Point();  // 在堆上分配一个Point对象，返回指针
    p3->x = 7.0;  // 用->访问成员变量（指针专用语法）
    p3->y = 8.0;  // 就像 (*p3).y = 8.0 的简写
    p3->print();  // 输出: (7, 8)
    
    // 重要：堆上的对象不会自动销毁，必须手动delete！
    delete p3;  // 释放堆上的内存，避免内存泄漏
    p3 = nullptr;  // 指针设为空，避免野指针
    
    std::cout << "\n=== 小结 ===" << std::endl;
    std::cout << "栈上对象：自动管理，作用域结束自动销毁" << std::endl;
    std::cout << "堆上对象：手动管理，必须delete，否则内存泄漏" << std::endl;
    
    return 0;
}
```

运行结果：

```
=== 栈上创建对象 ===
(3, 4)

=== 使用成员函数初始化 ===
(5, 6)

=== 堆上创建对象 ===
(7, 8)

=== 小结 ===
栈上对象：自动管理，作用域结束自动销毁
堆上对象：手动管理，必须delete，否则内存泄漏
```

> 内存泄漏就像是租了房子不交租金也不退房，最终你的程序会把系统内存吃光光。所以堆上创建的对象，用完一定要记得`delete`。当然，更现代的做法是使用**智能指针（smart pointer）**，TA会自动帮你收拾烂摊子。

## 11.3 成员变量与成员函数

类的两大组成部分我们已经见过了，现在让我们深入了解一下它们的特性和用法。

### 成员变量（Member Variables）—— 类的"身份证信息"

成员变量就是描述对象状态的数据。每个对象都有自己独立的一份，互不影响。就像每个学生都有自己的学号、姓名、成绩一样。

### 成员函数（Member Functions）—— 类的"技能包"

成员函数就是对象能执行的操作。它们可以访问对象的成员变量，读取或者修改状态。就像学生能"考试"（修改成绩）、"自我介绍"（读取信息）一样。

```cpp
#include <iostream>
#include <string>

// 定义一个矩形类
class Rectangle {
public:
    // ========== 成员变量（属性）==========
    // 矩形的宽度和高度
    double width;   // 宽度
    double height;  // 高度
    
    // ========== 成员函数（方法）==========
    
    // 计算面积：宽 × 高
    double area() const {
        // const表示这个函数不会修改成员变量
        // 就像一个只读的查询操作
        return width * height;
    }
    
    // 计算周长：2 × (宽 + 高)
    double perimeter() const {
        return 2 * (width + height);
    }
    
    // 判断是否是正方形
    bool isSquare() const {
        return width == height;
    }
    
    // 设置尺寸
    void setDimensions(double w, double h) {
        width = w;
        height = h;
    }
};

int main() {
    std::cout << "=== 矩形类演示 ===" << std::endl;
    
    // 创建一个矩形对象
    Rectangle rect;
    rect.setDimensions(5.0, 3.0);  // 设置宽5，高3
    
    std::cout << "宽度: " << rect.width << std::endl;    // 输出: 宽度: 5
    std::cout << "高度: " << rect.height << std::endl;   // 输出: 高度: 3
    std::cout << "面积: " << rect.area() << std::endl;    // 输出: 面积: 15
    std::cout << "周长: " << rect.perimeter() << std::endl;  // 输出: 周长: 16
    std::cout << "是正方形? " << (rect.isSquare() ? "Yes" : "No") << std::endl;
    // 输出: 是正方形? No
    
    std::cout << "\n=== 尝试正方形 ===" << std::endl;
    rect.setDimensions(4.0, 4.0);  // 变成正方形
    std::cout << "是正方形? " << (rect.isSquare() ? "Yes" : "No") << std::endl;
    // 输出: 是正方形? Yes
    std::cout << "面积: " << rect.area() << std::endl;  // 输出: 面积: 16
    
    return 0;
}
```

运行结果：

```
=== 矩形类演示 ===
宽度: 5
高度: 3
面积: 15
周长: 16
是正方形? No

=== 尝试正方形 ===
是正方形? Yes
面积: 16
```

> 小技巧：在成员函数后面加`const`是一个好习惯，它告诉编译器"这个函数只是看看，不会乱改东西"。这就像是给函数贴了个"只读"标签，编译器会帮你检查是否有意外修改。如果你不小心写了会修改成员的代码，编译器会报错："嘿，这个函数是const的，不能改东西！"

## 11.4 访问控制：public、private、protected

这一节我们来聊聊类的"门禁系统"。想象一下，有些房间是公共区域（public），任何人都能进；有些是员工专属（protected），只有特定的人能进；还有些是老板的私人办公室（private），连门都没有。

### 访问控制关键字详解

在C++中，有三个访问控制级别：

| 关键字 | 访问级别 | 谁可以访问 |
|--------|----------|------------|
| `public` | 公有 | 任何人，任何地方 |
| `protected` | 受保护 | 本类 + 派生类 |
| `private` | 私有 | 只有本类 |

```cpp
#include <iostream>
#include <string>

// 银行账户类 - 演示三种访问控制
class BankAccount {
private:  // 私有：只有本类成员可以访问
    // 这些是敏感信息，不能让外人直接看到！
    std::string account_number_;  // 账号：保密！
    double balance_;              // 余额：更保密！
    
    // 私有成员函数：验证金额是否合法
    // 这是内部工具，外部不需要知道
    bool isValidAmount(double amount) const {
        return amount >= 0;  // 存款不能是负数，这是规矩
    }
    
public:  // 公有：任何代码都可以访问
    std::string owner_name_;  // 户主名：这个可以公开
    
    // 构造函数
    BankAccount(const std::string& owner, const std::string& accNum, double initialBalance) 
        : owner_name_(owner), account_number_(accNum), balance_(initialBalance) {}
    
    // 公有接口：存款
    void deposit(double amount) {
        if (!isValidAmount(amount)) {
            std::cout << "Invalid amount! 金额不能是负数！" << std::endl;
            return;
        }
        balance_ += amount;
        std::cout << "Deposited " << amount << ". New balance: " << balance_ << std::endl;
    }
    
    // 公有接口：取款
    void withdraw(double amount) {
        if (!isValidAmount(amount)) {
            std::cout << "Invalid amount! 金额不能是负数！" << std::endl;
            return;
        }
        if (amount > balance_) {
            std::cout << "Insufficient funds! 余额不足！" << std::endl;
            return;
        }
        balance_ -= amount;
        std::cout << "Withdrew " << amount << ". New balance: " << balance_ << std::endl;
    }
    
    // 公有接口：查询余额（只读）
    double getBalance() const {
        return balance_;
    }
    
protected:  // 受保护：派生类可以访问
    // 这个方法派生类需要用到，但外部不应该调用
    void printAccountInfo() const {
        std::cout << "Account: " << account_number_ << ", Owner: " << owner_name_ << std::endl;
    }
};

int main() {
    std::cout << "=== 访问控制演示 ===" << std::endl;
    
    // 创建账户
    BankAccount account("Alice", "123456789", 1000.0);
    
    // 尝试访问私有成员 - 这些都是错误写法！
    // account.account_number_;  // 错误！private成员不能直接访问
    // account.balance_;          // 错误！private成员不能直接访问
    // 编译器的反应：Access denied! 你没有权限！
    
    std::cout << "\n=== 通过公有接口操作 ===" << std::endl;
    
    // 通过public方法操作 - 正确姿势
    account.deposit(500.0);   // OK: public方法，存款500
    account.withdraw(200.0);  // OK: public方法，取款200
    
    // 查询余额
    std::cout << "Current balance: " << account.getBalance() << std::endl;
    // 输出: Current balance: 1300
    
    // 尝试调用protected方法 - 错误！
    // account.printAccountInfo();  // 错误！protected方法不能从外部调用
    // 编译器：这是内部方法，外部不能调用！
    
    std::cout << "\n=== 小结 ===" << std::endl;
    std::cout << "private: 藏在保险箱里，只有自己能访问" << std::endl;
    std::cout << "protected: 放在家里，子女（派生类）可以继承" << std::endl;
    std::cout << "public: 挂在门口的牌子，大家都能看" << std::endl;
    
    return 0;
}
```

运行结果：

```
=== 访问控制演示 ===

=== 通过公有接口操作 ===
Deposited 500. New balance: 1500
Withdrew 200. New balance: 1300
Current balance: 1300

=== 小结 ===
private: 藏在保险箱里，只有自己能访问
protected: 放在家里，子女（派生类）可以继承
public: 挂在门口的牌子，大家都能看
```

> 封装的好处：为什么要把数据藏起来？因为如果你随便让人改余额，银行的系统不就乱套了吗？通过公有接口（方法）来访问，可以确保所有的修改都是经过验证的、安全的。就像自动取款机，你只能按按钮取钱，不能直接伸手进机器里抓钱。

## 11.5 构造函数

构造函数（Constructor）是类的"出生证明办理处"。每当你创建一个对象，构造函数就会自动被调用，负责初始化对象的状态。打个比方，就像你出生时护士给你称体重、量身高一样。

### 默认构造函数

**默认构造函数**就是没有参数的构造函数。如果你没有定义任何构造函数，编译器会帮你自动生成一个——就像政府给你发了个默认的身份证。

```cpp
#include <iostream>
#include <string>

class Robot {
private:
    std::string name_;      // 机器人名字
    int battery_level_;     // 电量
    
public:
    // 默认构造函数：无参数
    // 当你不提供任何参数时，这个构造函数会被调用
    Robot() : name_("Unknown"), battery_level_(0) {
        std::cout << "Robot created: " << name_ << std::endl;
    }
    
    // 带参构造函数：有一个名字参数
    Robot(const std::string& name) : name_(name), battery_level_(100) {
        std::cout << "Robot created with name: " << name_ << std::endl;
    }
    
    // 打印机器人信息
    void info() const {
        std::cout << "Name: " << name_ << ", Battery: " << battery_level_ << "%" << std::endl;
    }
};

int main() {
    std::cout << "=== 创建第一个机器人 ===" << std::endl;
    Robot r1;  // 调用默认构造函数，不传参数
    
    std::cout << "\n=== 创建第二个机器人 ===" << std::endl;
    Robot r2("R2-D2");  // 调用带参构造函数，传递名字
    
    std::cout << "\n=== 机器人信息 ===" << std::endl;
    r1.info();  // 输出: Name: Unknown, Battery: 0%
    r2.info();  // 输出: Name: R2-D2, Battery: 100%
    
    return 0;
}
```

运行结果：

```
=== 创建第一个机器人 ===
Robot created: Unknown

=== 创建第二个机器人 ===
Robot created with name: R2-D2

=== 机器人信息 ===
Name: Unknown, Battery: 0%
Name: R2-D2, Battery: 100%
```

> 小提示：如果你定义了带参数的构造函数，但仍然想要无参数创建对象，你就必须显式地定义一个默认构造函数。否则`Robot r;`会编译报错——编译器可不是万能的！

### 带参构造函数

**带参构造函数**让你在创建对象时就能指定初始状态。这就像是给宝宝办出生证明时直接填好名字、出生时间一样。

```cpp
#include <iostream>

class Point {
private:
    double x_;
    double y_;
    
public:
    // 初始化列表：更高效的初始化方式
    // 这种写法直接初始化成员变量，而不是先默认构造再赋值
    // 就像一步到位，不用先画格子再填内容
    Point(double x, double y) : x_(x), y_(y) {
        std::cout << "Point(" << x_ << ", " << y_ << ") created" << std::endl;
    }
    
    void print() const {
        std::cout << "(" << x_ << ", " << y_ << ")" << std::endl;
    }
};

// 矩形类：包含两个Point成员
class Rectangle {
private:
    Point bottom_left_;   // 左下角点
    Point top_right_;     // 右上角点
    
public:
    // 构造函数：使用初始化列表初始化成员对象
    // 成员对象的构造在函数体之前执行
    Rectangle(double x1, double y1, double x2, double y2)
        : bottom_left_(x1, y1), top_right_(x2, y2) {
        std::cout << "Rectangle created" << std::endl;
    }
    
    void print() const {
        std::cout << "Bottom-left: ";
        bottom_left_.print();
        std::cout << "Top-right: ";
        top_right_.print();
    }
};

int main() {
    std::cout << "=== 创建点 ===" << std::endl;
    Point p1(3.0, 4.0);  // 调用带参构造函数
    p1.print();  // 输出: (3, 4)
    
    std::cout << "\n=== 创建矩形 ===" << std::endl;
    Rectangle rect(0, 0, 5, 3);  // 矩形左下角(0,0)，右上角(5,3)
    rect.print();
    
    return 0;
}
```

运行结果：

```
=== 创建点 ===
Point(3, 4) created
(3, 4)

=== 创建矩形 ===
Point(0, 0) created
Point(5, 3) created
Rectangle created
Bottom-left: (0, 0)
Top-right: (5, 3)
```

> 为什么用初始化列表？效率高！如果用赋值的方式，成员变量会先被默认构造（int就变成0，string变成空字符串），然后再被赋值。等于是做了两次工作。初始化列表直接一步到位，妙不妙？

### 拷贝构造函数

**拷贝构造函数**是用一个已有对象来创建新对象。就像复印机一样，复制出一份一模一样的内容。

```cpp
#include <iostream>
#include <string>

class Person {
private:
    std::string name_;  // 姓名
    int age_;            // 年龄
    
public:
    // 普通构造函数
    Person(const std::string& name, int age) : name_(name), age_(age) {
        std::cout << "Person(\"" << name_ << "\", " << age_ << ") created" << std::endl;
    }
    
    // 拷贝构造函数：用已有对象初始化新对象
    // 参数必须是 const 引用！这是语法的硬性要求
    Person(const Person& other) : name_(other.name_), age_(other.age_) {
        std::cout << "Person copy constructor called for " << name_ << std::endl;
    }
    
    void print() const {
        std::cout << name_ << ", age " << age_ << std::endl;
    }
};

int main() {
    std::cout << "=== 直接创建Alice ===" << std::endl;
    Person alice("Alice", 25);  // 调用普通构造函数
    
    std::cout << "\n=== 拷贝构造Bob（用alice初始化）===" << std::endl;
    Person bob(alice);  // 拷贝构造：从alice复制一个新的bob
    
    std::cout << "\n=== 拷贝构造Charlie（另一种语法）===" << std::endl;
    Person charlie = alice;  // 也是拷贝构造！等价于 Person charlie(alice);
    
    std::cout << "\n=== 打印结果 ===" << std::endl;
    alice.print();  // 输出: Alice, age 25
    bob.print();    // 输出: Alice, age 25（和alice一样的信息）
    charlie.print(); // 输出: Alice, age 25
    
    return 0;
}
```

运行结果：

```
=== 直接创建Alice ===
Person("Alice", 25) created

=== 拷贝构造Bob（用alice初始化）===
Person copy constructor called for Alice

=== 拷贝构造Charlie（另一种语法）===
Person copy constructor called for Alice

=== 打印结果 ===
Alice, age 25
Alice, age 25
Alice, age 25
```

> 拷贝构造什么时候会被调用？三种情况：
> 1. 用一个对象初始化另一个对象：`Person bob(alice);`
> 2. 传对象给函数（值传递）：`void foo(Person p); foo(alice);`
> 3. 返回对象（值返回）：`Person foo() { return alice; }`

### 移动构造函数（C++11）

**移动构造函数**是C++11引入的黑科技。它的作用是"偷取"临时对象占用的资源，而不是复制一份。这就像是搬家时，你直接告诉快递公司"把那个柜子搬过来"，而不是"把柜子复制一份"。

为什么要移动？因为有些对象很大（比如装了一百万个元素的vector），复制一次要花很多时间和内存。而移动只是转交所有权，快得像闪电！

```cpp
#include <iostream>
#include <vector>
#include <string>

class BigObject {
public:
    std::string data;                  // 字符串数据
    std::vector<int> numbers;          // 大量整数
    
    // 普通构造函数
    BigObject(const std::string& d, size_t n) : data(d), numbers(n, 0) {
        std::cout << "BigObject constructed: " << data << std::endl;
    }
    
    // 移动构造函数
    // 特点：参数是右值引用(T&&)
    // noexcept告诉编译器：这个函数不会抛出异常，可以放心优化
    BigObject(BigObject&& other) noexcept 
        : data(std::move(other.data)),       // 移动字符串
          numbers(std::move(other.numbers)) { // 移动vector
        std::cout << "BigObject moved: " << other.data << std::endl;
    }
    
    void print() const {
        std::cout << "data=" << data << ", size=" << numbers.size() << std::endl;
    }
};

int main() {
    std::cout << "=== 创建大对象 ===" << std::endl;
    BigObject obj1("heavy", 1000000);  // 创建一个有大数据的对象
    std::cout << "obj1内存占用：numbers有" << obj1.numbers.size() << "个元素" << std::endl;
    
    std::cout << "\n=== 移动构造obj2 ===" << std::endl;
    // std::move把obj1变成右值，触发移动构造函数
    // 移动后obj1的data和numbers变成空！
    BigObject obj2(std::move(obj1));
    
    std::cout << "\n=== 检查obj2 ===" << std::endl;
    obj2.print();
    
    std::cout << "\n=== 检查obj1（已被移动）===" << std::endl;
    std::cout << "obj1.data现在是: \"" << obj1.data << "\"" << std::endl;
    std::cout << "obj1.numbers大小: " << obj1.numbers.size() << std::endl;
    
    return 0;
}
```

运行结果：

```
=== 创建大对象 ===
BigObject constructed: heavy
obj1内存占用：numbers有1000000个元素

=== 移动构造obj2 ===
BigObject moved: heavy

=== 检查obj2 ===
data=heavy, size=1000000

=== 检查obj1（已被移动）===
obj1.data现在是: ""
obj1.numbers大小: 0
```

> `std::move`本身不移动任何东西，它只是把参数转成右值引用，告诉编译器"你可以偷这个对象的资源了"。移动之后，原对象就变成了一个"空壳"——数据成员都被掏空了。这很危险，所以移动之后原对象最好不要使用了（或者至少要重新赋值后再使用）。

### 委托构造函数（C++11）

**委托构造函数**允许一个构造函数调用同一个类的另一个构造函数。这就像是老板把任务委托给下属，自己就不用亲自干了。

```cpp
#include <iostream>
#include <string>

class Employee {
private:
    std::string name_;
    int id_;
    double salary_;
    std::string department_;
    
public:
    // 主构造函数（目标构造函数）
    // 这是真正干活的构造函数，所有参数都齐全
    Employee(const std::string& name, int id, double salary, const std::string& dept)
        : name_(name), id_(id), salary_(salary), department_(dept) {
        std::cout << "Main constructor: " << name_ << std::endl;
    }
    
    // 委托构造函数：委托给主构造函数
    // 只提供name和id，使用默认值salary=50000, dept="General"
    Employee(const std::string& name, int id)
        : Employee(name, id, 50000.0, "General") {  // 委托！
        // 这里不需要再初始化任何东西了
    }
    
    // 委托构造函数：只提供name
    // 使用默认值 id=0, salary=30000, dept="Intern"
    Employee(const std::string& name)
        : Employee(name, 0, 30000.0, "Intern") {  // 委托！
    }
    
    // 委托构造函数：无参数
    // 使用默认值 name="Unnamed", id=-1, salary=0, dept="None"
    Employee() : Employee("Unnamed", -1, 0.0, "None") {}  // 委托！
    
    void print() const {
        std::cout << "Employee: " << name_ << ", ID: " << id_ 
                  << ", Salary: " << salary_ << ", Dept: " << department_ << std::endl;
    }
};

int main() {
    std::cout << "=== 全参数构造 ===" << std::endl;
    Employee e1("Alice", 1001, 75000.0, "Engineering");
    
    std::cout << "\n=== 两个参数构造（委托）===" << std::endl;
    Employee e2("Bob", 1002);  // 使用委托
    
    std::cout << "\n=== 一个参数构造（委托）===" << std::endl;
    Employee e3("Charlie");    // 使用委托
    
    std::cout << "\n=== 无参数构造（委托）===" << std::endl;
    Employee e4;                // 使用委托
    
    std::cout << "\n=== 打印所有员工 ===" << std::endl;
    e1.print();
    e2.print();
    e3.print();
    e4.print();
    
    return 0;
}
```

运行结果：

```
=== 全参数构造 ===
Main constructor: Alice

=== 两个参数构造（委托）===
Main constructor: Bob

=== 一个参数构造（委托）===
Main constructor: Charlie

=== 无参数构造（委托）===
Main constructor: Unnamed

=== 打印所有员工 ===
Employee: Alice, ID: 1001, Salary: 75000, Dept: Engineering
Employee: Bob, ID: 1002, Salary: 50000, Dept: General
Employee: Charlie, ID: 0, Salary: 30000, Dept: Intern
Employee: Unnamed, ID: -1, Salary: 0, Dept: None
```

> 委托构造的好处：代码不重复！想象一下如果没有委托，每个构造函数都要写一堆初始化代码，那得多乱啊。委托让代码简洁又清晰。

### explicit构造函数

**explicit**关键字用来防止隐式类型转换。就像是一个"显眼的告示牌"：请勿在此隐式转换！

```cpp
#include <iostream>
#include <string>

class String {
private:
    std::string data_;
    
public:
    // explicit：禁止隐式转换从const char*构造String
    explicit String(const char* str) : data_(str) {
        std::cout << "String created from C-string" << std::endl;
    }
    
    // explicit：禁止隐式转换从int构造String
    explicit String(int n) : data_(n, 'X') {
        std::cout << "String created from int" << std::endl;
    }
    
    // 没有explicit：可以从std::string隐式转换
    String(const std::string& str) : data_(str) {
        std::cout << "String created from std::string" << std::endl;
    }
    
    const std::string& get() const { return data_; }
};

void processString(const String& s) {
    std::cout << "Processing: " << s.get() << std::endl;
}

int main() {
    std::cout << "=== explicit演示 ===" << std::endl;
    
    // String s1 = "Hello";  // 错误！explicit禁止隐式转换
    // 编译器的内心OS：你想隐式转换？没门！
    
    String s2("Hello");  // OK：直接构造，不涉及隐式转换
    String s3 = String("Hello");  // OK：显式构造
    
    std::cout << "\n=== 函数调用 ===" << std::endl;
    
    // processString("Test");  // 错误！不能隐式转换const char*到String
    processString(String("Test"));  // OK：显式构造临时对象
    
    // String s4 = 10;  // 错误！explicit禁止隐式转换int到String
    String s5(10);  // OK：显式构造 "XXXXXXXXXX"
    
    std::cout << "\n=== 成功！ ===" << std::endl;
    std::cout << "explicit关键字成功阻止了隐式转换" << std::endl;
    
    return 0;
}
```

运行结果：

```
=== explicit演示 ===
String created from C-string
String created from C-string

=== 函数调用 ===
String created from C-string
Processing: Test
String created from int

=== 成功！ ===
explicit关键字成功阻止了隐式转换
```

> 为什么要阻止隐式转换？因为有时候隐式转换会带来意想不到的bug。比如你写了一个`String`的构造函数`String(int n)`，如果允许隐式转换，那`myString = 5;`就会悄悄创建一个`"XXXXX"`字符串，而不是报错。这种沉默的错误最可怕了。

### 构造函数异常安全

构造函数里如果发生异常，已经分配的资源怎么办？这就要靠**构造函数异常安全**来处理了。

```cpp
#include <iostream>
#include <stdexcept>

// 模拟某种资源（文件句柄、内存等）
class Resource {
public:
    Resource() { 
        std::cout << "Resource acquired" << std::endl;
    }
    
    ~Resource() { 
        std::cout << "Resource released" << std::endl;
    }
};

class Widget {
private:
    Resource* r1;  // 资源1
    Resource* r2;  // 资源2
    
public:
    // 构造函数：初始化列表中分配资源
    Widget() try : r1(new Resource()), r2(new Resource()) {
        // try块语法：构造函数的函数体变成try块的一部分
        std::cout << "Widget constructed successfully" << std::endl;
    } catch (...) {
        // 如果构造函数抛出异常，进入这个catch块
        std::cout << "Constructor exception - cleanup!" << std::endl;
        delete r1;  // 手动清理已经分配的资源
        // r2不需要清理，因为分配r2时抛出异常，r2还是nullptr
        throw;  // 重新抛出异常，让调用者知道构造失败了
    }
    
    ~Widget() {
        delete r2;
        delete r1;
        std::cout << "Widget destroyed" << std::endl;
    }
};

int main() {
    std::cout << "=== 正常构造 ===" << std::endl;
    Widget w;
    
    std::cout << "\n=== 退出作用域 ===" << std::endl;
    // w的析构函数会被调用，释放资源
    
    std::cout << "\n=== 注意 ===" << std::endl;
    std::cout << "实际应用中应使用智能指针(std::unique_ptr)避免手动清理" << std::endl;
    
    return 0;
}
```

运行结果：

```
=== 正常构造 ===
Resource acquired
Resource acquired
Widget constructed successfully

=== 退出作用域 ===
Widget destroyed
Resource released
Resource released
```

> 现代C++建议：构造函数try块虽然能处理异常，但代码复杂、容易出错。更现代、更安全的方法是使用**智能指针（`std::unique_ptr`或`std::shared_ptr`）**来管理资源，它们会在析构函数中自动释放。记住：资源获取即初始化（RAII）！

## 11.6 析构函数

析构函数（Destructor）是构造函数的"收尾工作"。当对象生命周期结束时（比如离开作用域或被delete），析构函数就会被自动调用，做一些清理工作，比如释放资源、关闭文件、断开网络连接等等。

### 析构函数不应抛出异常

这是非常重要的一条规则：**析构函数不应该抛出异常**。为什么？

想象一下：如果析构函数在清理资源时抛出异常，而C++运行时正在处理另一个异常（或者正在stack unwinding过程中），程序就会调用`std::terminate()`直接崩溃。这就像是火警时你又拉响了地震警报，整个应急系统就傻眼了。

```cpp
#include <iostream>
#include <stdexcept>

// 模拟数据库连接
class Connection {
public:
    Connection(const std::string& name) : name_(name) {
        std::cout << "Connection " << name_ << " opened" << std::endl;
    }
    
    // 析构函数：关闭连接
    // noexcept关键字：承诺不抛出异常
    // 这是析构函数的默认修饰符！
    ~Connection() noexcept {
        std::cout << "Closing connection " << name_ << "..." << std::endl;
        
        // 最佳实践：析构函数不应抛出异常
        // 如果close()可能失败，使用try-catch吞掉异常
        try {
            close();  // 假设这个函数可能抛出异常
        } catch (...) {
            // 吞掉异常，避免terminate()
            // 记录日志，但不重新抛出
            std::cerr << "Exception during close in destructor" << std::endl;
        }
        
        std::cout << "Connection " << name_ << " closed" << std::endl;
    }
    
    void close() {
        throw std::runtime_error("Close failed!");
    }
    
private:
    std::string name_;
};

int main() {
    std::cout << "=== 创建连接 ===" << std::endl;
    Connection conn("Database");
    
    std::cout << "\n=== 退出作用域 ===" << std::endl;
    // 析构函数会被调用，即使close()抛出异常也会被捕获
    // 不会导致terminate()！
    
    std::cout << "\n=== 程序正常结束 ===" << std::endl;
    
    return 0;
}
```

运行结果：

```
=== 创建连接 ===
Connection Database opened

=== 退出作用域 ===
Closing connection Database...
Exception during close in destructor
Connection Database closed

=== 程序正常结束 ===
```

> 黄金法则：析构函数要么不抛出异常（用`noexcept`），要么就在内部用try-catch把所有异常都吞掉。永远不要让异常逃离析构函数！

## 11.7 赋值运算符重载

赋值运算符（`operator=`）用于给已存在的对象赋予新的值。这和拷贝构造函数不同：拷贝构造是用一个对象创建一个新对象（对象还不存在），而赋值运算是给一个已存在的对象重新赋值。

### 拷贝赋值

**拷贝赋值运算符**处理的是"两个对象都已经存在"的情况。它需要先释放旧资源，再复制新资源。

```cpp
#include <iostream>
#include <cstring>

class String {
private:
    char* data_;    // 字符数组指针
    size_t length_; // 字符串长度
    
public:
    // 普通构造函数
    String(const char* str) {
        length_ = strlen(str);
        data_ = new char[length_ + 1];
        strcpy(data_, str);
        std::cout << "String created: " << data_ << std::endl;
    }
    
    // 拷贝赋值运算符
    // 当你写 s2 = s1 时，这个函数被调用
    String& operator=(const String& other) {
        std::cout << "Copy assignment called for: " << other.data_ << std::endl;
        
        // 重要！自赋值检查！
        // 如果 s1 = s1; 这种情况，不做任何操作直接返回
        if (this != &other) {
            delete[] data_;  // 释放旧资源！否则内存泄漏！
            
            length_ = other.length_;  // 复制长度
            data_ = new char[length_ + 1];  // 分配新内存
            strcpy(data_, other.data_);  // 复制内容
        }
        
        return *this;  // 返回自身，支持链式赋值 s3 = s2 = s1;
    }
    
    const char* c_str() const { return data_; }
    
    ~String() {
        std::cout << "String destroyed: " << (void*)data_ << std::endl;
        delete[] data_;
    }
};

int main() {
    std::cout << "=== 创建字符串 ===" << std::endl;
    String s1("Hello");
    String s2("World");
    
    std::cout << "\n=== 拷贝赋值 ===" << std::endl;
    s2 = s1;  // 将s1的值拷贝赋值给s2
    
    std::cout << "s2 = " << s2.c_str() << std::endl;
    
    std::cout << "\n=== 自赋值 ===" << std::endl;
    s1 = s1;  // 自赋值，应该安全处理（不崩溃、不出错）
    
    return 0;
}
```

运行结果：

```
=== 创建字符串 ===
String created: Hello
String created: World

=== 拷贝赋值 ===
Copy assignment called for: Hello
String destroyed: 0x...  // 释放s2原来的"World"

s2 = Hello

=== 自赋值 ===
Copy assignment called for: Hello
// 自赋值检查阻止了危险操作！
```

> 拷贝赋值三步曲：1. 检查自赋值 2. 释放旧资源 3. 分配新资源并复制。三步缺一不可！忘了释放旧资源会导致内存泄漏，忘了检查自赋值会导致`delete[] data_`把自己删了然后访问野指针。

### 移动赋值（C++11）

**移动赋值运算符**类似于移动构造函数，但用于已存在的对象。它需要先释放旧资源，再偷取新资源的所有权。

```cpp
#include <iostream>
#include <utility>
#include <cstring>

class String {
private:
    char* data_;
    size_t length_;
    
public:
    // 普通构造函数
    String(const char* str) {
        length_ = strlen(str);
        data_ = new char[length_ + 1];
        strcpy(data_, str);
    }
    
    // 移动赋值运算符
    // 当你写 s2 = std::move(s1) 时，这个函数被调用
    String& operator=(String&& other) noexcept {
        std::cout << "Move assignment called" << std::endl;
        
        if (this != &other) {  // 仍然要检查自赋值
            delete[] data_;  // 释放旧资源！
            
            data_ = other.data_;  // 偷取资源！
            length_ = other.length_;
            
            other.data_ = nullptr;  // 源对象置空，防止析构时释放我们的数据
            other.length_ = 0;
        }
        
        return *this;
    }
    
    const char* c_str() const { 
        return data_ ? data_ : "(null)"; 
    }
    
    bool isEmpty() const { return data_ == nullptr; }
    
    ~String() {
        delete[] data_;
    }
};

int main() {
    String s1("Hello");
    String s2("World");
    
    std::cout << "Before move: s1=" << s1.c_str() << ", s2=" << s2.c_str() << std::endl;
    
    std::cout << "\n=== 移动赋值 ===" << std::endl;
    s2 = std::move(s1);  // s2的旧资源("World")被释放，s1的资源被"偷"给s2
    
    std::cout << "\n=== 移动后 ===" << std::endl;
    std::cout << "After move: s1=" << s1.c_str() << ", s2=" << s2.c_str() << std::endl;
    
    return 0;
}
```

运行结果：

```
Before move: s1=Hello, s2=World

=== 移动赋值 ===
Move assignment called

=== 移动后 ===
After move: s1=(null), s2=Hello
```

> 移动赋值的精髓：旧的不去，新的不来。先`delete[]`自己的旧资源，再"接管"别人的资源。这样就避免了一次昂贵的数据复制！

## 11.8 深拷贝与浅拷贝

这是C++中一个超级重要的概念，也是新手最容易踩坑的地方之一。

**浅拷贝（Shallow Copy）**：只拷贝指针的值（地址），不拷贝指针指向的数据。就像是复制了一张"藏宝图"，原图和副本都指向同一个宝藏。

**深拷贝（Deep Copy）**：不仅拷贝指针，还拷贝指针指向的数据。就像是真正复制了宝藏本身，现在有两份独立的宝藏了。

```cpp
#include <iostream>
#include <cstring>

// 危险的浅拷贝类
class shallow_ptr {
public:
    char* data;  // 原始指针
    
    shallow_ptr(const char* str) {
        data = new char[strlen(str) + 1];
        strcpy(data, str);
    }
    
    // 显式声明浅拷贝：默认拷贝构造函数只做简单的位拷贝
    // 也就是说，拷贝后两个对象的data指针指向同一块内存！
    shallow_ptr(const shallow_ptr&) = default;  // 浅拷贝！
    shallow_ptr& operator=(const shallow_ptr&) = default;  // 浅拷贝！
    
    ~shallow_ptr() {
        std::cout << "Destroying: " << (void*)data << " -> " << (data ? data : "null") << std::endl;
        delete[] data;  // 这里会导致double delete！
    }
};

// 安全的深拷贝类
class deep_ptr {
public:
    char* data;
    
    deep_ptr(const char* str) {
        data = new char[strlen(str) + 1];
        strcpy(data, str);
    }
    
    // 拷贝构造函数：深拷贝！
    // 真正复制一份数据，而不是只复制指针
    deep_ptr(const deep_ptr& other) {
        std::cout << "Deep copy of: " << other.data << std::endl;
        data = new char[strlen(other.data) + 1];
        strcpy(data, other.data);
    }
    
    // 移动构造函数
    deep_ptr(deep_ptr&& other) noexcept : data(other.data) {
        other.data = nullptr;  // 源对象置空
    }
    
    // 赋值运算符：深拷贝
    deep_ptr& operator=(const deep_ptr& other) {
        if (this != &other) {
            std::cout << "Deep assignment of: " << other.data << std::endl;
            delete[] data;  // 先释放自己的资源
            data = new char[strlen(other.data) + 1];
            strcpy(data, other.data);
        }
        return *this;
    }
    
    const char* get() const { return data ? data : "(null)"; }
    
    ~deep_ptr() {
        std::cout << "Destroying: " << (data ? data : "null") << std::endl;
        delete[] data;
    }
};

int main() {
    std::cout << "=== 深拷贝演示 ===" << std::endl;
    
    deep_ptr d1("Hello");
    deep_ptr d2("World");
    
    std::cout << "\n=== 赋值操作 ===" << std::endl;
    d2 = d1;  // 深拷贝赋值
    
    std::cout << "\n=== 验证 ===" << std::endl;
    std::cout << "d1=" << d1.get() << ", d2=" << d2.get() << std::endl;
    std::cout << "不同内存地址? " << (d1.get() != d2.get() ? "Yes!" : "No!") << std::endl;
    
    std::cout << "\n=== 作用域结束，析构 ===" << std::endl;
    
    return 0;
}
```

运行结果：

```
=== 深拷贝演示 ===
Deep copy of: Hello
Deep assignment of: Hello
Destroying: Hello
Destroying: Hello

=== 验证 ===
d1=Hello, d2=Hello
不同内存地址? Yes!

=== 作用域结束，析构 ===
Destroying: Hello
Destroying: Hello
```

> 浅拷贝的危险：如果你用`shallow_ptr`，拷贝构造函数只复制指针，两个对象指向同一块内存。析构时，`delete[]`被调用两次——这就是经典的**double free**问题，会导致程序崩溃！所以当类管理动态内存时，一定要实现深拷贝！

## 11.9 三五法则与零法则

这一节我们来聊聊C++类的特殊成员函数之间的"铁律"。

### 三法则（The Rule of Three）

如果你的类需要**手动管理资源**（比如动态内存、文件句柄、网络连接等），并且你自定义了以下任一操作，那你通常需要自定义**所有三个**：

1. **析构函数** - 负责释放资源
2. **拷贝构造函数** - 需要深拷贝
3. **拷贝赋值运算符** - 需要深拷贝

为什么？因为如果你自定义了析构函数（比如要释放某些特殊资源），那默认的拷贝操作很可能是不安全的（会浅拷贝那些资源）。

### 五法则（The Rule of Five）

C++11引入了移动语义，所以三法则扩展成了**五法则**：

1. 析构函数
2. 拷贝构造函数
3. 拷贝赋值运算符
4. **移动构造函数**
5. **移动赋值运算符**

如果你需要自定义移动操作，那拷贝操作通常应该被禁用（`= delete`）。

### 零法则（The Rule of Zero）

**最佳实践**：如果你能避免手动管理资源（使用`std::string`、`std::vector`等RAII类型），那就让编译器自动生成这些特殊成员函数。这就是**零法则**——你不需要定义任何特殊成员函数！

```cpp
#include <iostream>
#include <cstring>

// ============ 零法则 ============
// 如果类中没有手动管理资源（使用string等RAII类型）
// 编译器会自动生成拷贝构造、拷贝赋值、移动构造、移动赋值、析构
// 完美！不需要写任何代码！
class RuleOfZero {
    std::string data_;  // 资源由成员自己管理（string内部自己处理内存）
public:
    RuleOfZero(const std::string& d) : data_(d) {}
    // 五大特殊成员函数全部使用编译器自动生成的版本
    // 不用担心内存泄漏，不用担心浅拷贝！
};

// ============ 五法则 ============
// 如果类中手动管理资源（用raw指针），就必须实现全部5个函数
class RuleOfFive {
    char* data_;    // 手动管理的原始指针
    size_t len_;    // 字符串长度
    
public:
    // 普通构造函数
    RuleOfFive(const char* str) {
        len_ = strlen(str);
        data_ = new char[len_ + 1];
        strcpy(data_, str);
    }
    
    // 1. 析构函数：释放资源
    ~RuleOfFive() { 
        delete[] data_; 
        std::cout << "RuleOfFive destroyed" << std::endl;
    }
    
    // 2. 拷贝构造函数：深拷贝
    RuleOfFive(const RuleOfFive& other) {
        len_ = other.len_;
        data_ = new char[len_ + 1];
        strcpy(data_, other.data_);
    }
    
    // 3. 移动构造函数：偷取资源
    RuleOfFive(RuleOfFive&& other) noexcept : data_(other.data_), len_(other.len_) {
        other.data_ = nullptr;  // 源对象置空
        other.len_ = 0;
    }
    
    // 4. 拷贝赋值运算符
    RuleOfFive& operator=(const RuleOfFive& other) {
        if (this != &other) {
            delete[] data_;  // 释放旧资源
            len_ = other.len_;
            data_ = new char[len_ + 1];
            strcpy(data_, other.data_);
        }
        return *this;
    }
    
    // 5. 移动赋值运算符
    RuleOfFive& operator=(RuleOfFive&& other) noexcept {
        if (this != &other) {
            delete[] data_;  // 释放旧资源
            data_ = other.data_;  // 偷取资源
            len_ = other.len_;
            other.data_ = nullptr;
            other.len_ = 0;
        }
        return *this;
    }
    
    const char* get() const { return data_ ? data_ : "(null)"; }
};

int main() {
    std::cout << "=== 五法则演示 ===" << std::endl;
    RuleOfFive r1("Hello");
    RuleOfFive r2("World");
    
    std::cout << "\n=== 移动赋值 ===" << std::endl;
    r2 = std::move(r1);  // 使用移动赋值
    
    std::cout << "After move: " << r2.get() << std::endl;
    
    std::cout << "\n=== 作用域结束 ===" << std::endl;
    
    return 0;
}
```

运行结果：

```
=== 五法则演示 ===

=== 移动赋值 ===
RuleOfFive destroyed  // r2原来的资源被释放

After move: Hello

=== 作用域结束 ===
RuleOfFive destroyed  // r2被销毁
```

> 实用建议：尽量使用`std::string`、`std::vector`等RAII类型，它们帮你自动处理内存管理。这样你就可以遵循零法则，代码简洁又安全！

## 11.10 =default与=delete（C++11）

C++11引入了两个特殊的语法：`=default`和`=delete`。它们就像是类的"快捷键"，让你可以显式地要求编译器生成默认实现，或者彻底禁用某个函数。

### =default：使用默认实现

有时候你自定义了构造函数，但希望其他特殊成员函数使用编译器自动生成的版本。这时可以用`=default`显式声明。

### =delete：禁用某个函数

有时候你想禁止某些操作（比如禁止拷贝某个类），这时可以用`=delete`显式删除函数。

```cpp
#include <iostream>

// 不可拷贝的类 - 使用=delete禁用拷贝操作
class NonCopyable {
private:
    int id_;  // 私有，让它更"私密"
    
public:
    NonCopyable(int id) : id_(id) {}
    
    // 显式删除拷贝构造函数：禁止任何形式的拷贝
    // 任何拷贝该对象的代码都会编译报错！
    NonCopyable(const NonCopyable&) = delete;
    
    // 显式删除拷贝赋值运算符
    NonCopyable& operator=(const NonCopyable&) = delete;
    
    // 移动操作：使用=default使用默认实现
    // 移动后对象可以被"掏空"
    NonCopyable(NonCopyable&&) = default;
    NonCopyable& operator=(NonCopyable&&) = default;
    
    int getId() const { return id_; }
};

// 使用=default的类
class DefaultDemo {
    int value_;
    
public:
    DefaultDemo(int v) : value_(v) {}
    
    // 显式default析构函数
    // 告诉编译器：虽然有自定义构造函数，但析构函数用默认的就行
    ~DefaultDemo() = default;
    
    // 其他特殊成员函数编译器会自动生成
};

int main() {
    std::cout << "=== =delete演示 ===" << std::endl;
    
    NonCopyable nc1(1);
    std::cout << "nc1.id = " << nc1.getId() << std::endl;
    
    // 下面这些都会编译报错：
    // NonCopyable nc2(nc1);  // 错误！拷贝构造被删除
    // NonCopyable nc3 = nc1;  // 错误！拷贝赋值被删除
    
    NonCopyable nc4(4);
    NonCopyable nc5(std::move(nc4));  // OK！移动构造是default的
    std::cout << "nc5.id = " << nc5.getId() << std::endl;
    
    std::cout << "\n=== =default演示 ===" << std::endl;
    
    DefaultDemo d1(10);
    DefaultDemo d2(d1);  // OK！默认拷贝构造
    std::cout << "d2.value = " << d2.value_ << std::endl;
    
    std::cout << "\n=default and =delete demo 成功！" << std::endl;
    
    return 0;
}
```

运行结果：

```
=== =delete演示 ===
nc1.id = 1
nc5.id = 4

=== =default演示 ===
d2.value = 10

=default and =delete demo 成功！
```

> 应用场景：
> - `=delete`：当你设计一个类不想被拷贝时（比如文件句柄、线程等），或者想禁用某些不合理的操作（比如`NonCopyable nc = 1;`）。
> - `=default`：当你想让编译器生成默认实现，但又要明确表达你的意图时。这比完全不写要好，因为更清晰。

## 11.11 聚合类与聚合初始化

**聚合类（Aggregate Class）**是一种特殊的类，可以直接用花括号初始化，就像初始化数组一样。聚合初始化是C++最早期就有的特性，C++20又给它加了新花样。

简单来说，聚合类就是：
- 没有用户定义的构造函数
- 没有`private`或`protected`的非静态成员变量
- 没有`virtual`函数
- 不是`union`

### 指定初始化器（C++20）

C++20引入了一种新语法：可以按名字初始化成员变量，而不是按顺序。这就像是点外卖时说"我要一份不辣的多加葱的"，而不是"我按顺序说：饭、葱、否、加"。

```cpp
#include <iostream>

struct Point3D {
    double x = 0.0;  // 默认值为0.0
    double y = 0.0;
    double z = 0.0;
};

int main() {
    std::cout << "=== C++20 指定初始化器 ===" << std::endl;
    
    // C++20新特性：按名字初始化，顺序可以打乱！
    Point3D p1 = {.x = 1.0, .y = 2.0, .z = 3.0};
    std::cout << "p1: (" << p1.x << ", " << p1.y << ", " << p1.z << ")" << std::endl;
    // 输出: p1: (1, 2, 3)
    
    // 部分指定，只初始化x，y和z使用默认值
    Point3D p2 = {.x = 5.0};
    std::cout << "p2: (" << p2.x << ", " << p2.y << ", " << p2.z << ")" << std::endl;
    // 输出: p2: (5, 0, 0)
    
    // 顺序打乱也没关系
    Point3D p3 = {.z = 9.0, .x = 7.0, .y = 8.0};
    std::cout << "p3: (" << p3.x << ", " << p3.y << ", " << p3.z << ")" << std::endl;
    // 输出: p3: (7, 8, 9)
    
    // C++20也支持花括号形式
    Point3D p4{.x = 10.0, .z = 12.0};
    std::cout << "p4: (" << p4.x << ", " << p4.y << ", " << p4.z << ")" << std::endl;
    // 输出: p4: (10, 0, 12)
    
    return 0;
}
```

运行结果：

```
=== C++20 指定初始化器 ===
p1: (1, 2, 3)
p2: (5, 0, 0)
p3: (7, 8, 9)
p4: (10, 0, 12)
```

> 指定初始化器的好处：代码可读性更好！当初始化一个有很多成员的结构体时，`{.x=1, .y=2}`比`{1, 2}`清晰多了，尤其是在只初始化部分成员时。

### 括号聚合初始化（C++20）

C++20还简化了聚合初始化的语法，现在可以用圆括号`()`来初始化聚合类了！

```cpp
#include <iostream>

struct Color {
    int r = 0;  // 红色分量
    int g = 0;  // 绿色分量
    int b = 0;  // 蓝色分量
};

int main() {
    std::cout << "=== C++20 括号聚合初始化 ===" << std::endl;
    
    // C++20: 括号聚合初始化
    Color c1{255, 0, 0};  // 完全初始化，红色
    std::cout << "c1: RGB(" << c1.r << "," << c1.g << "," << c1.b << ")" << std::endl;
    
    // 部分初始化，没指定的用默认值
    Color c2{0, 255};  // 只有r和g，b=0
    std::cout << "c2: RGB(" << c2.r << "," << c2.g << "," << c2.b << ")" << std::endl;
    
    // 只初始化r
    Color c3{128};
    std::cout << "c3: RGB(" << c3.r << "," << c3.g << "," << c3.b << ")" << std::endl;
    
    return 0;
}
```

运行结果：

```
=== C++20 括号聚合初始化 ===
c1: RGB(255,0,0)
c2: RGB(0,255,0)
c3: RGB(128,0,0)
```

> 聚合初始化的限制：必须按顺序初始化，不能跳过中间的成员。如果你想只初始化第一个和第三个成员，对不起，不行——这是聚合初始化的规矩。

## 11.12 成员声明顺序强制（C++23）

C++23引入了一个重要的规则：**构造函数初始化列表中的成员初始化顺序必须与成员声明顺序一致**。虽然这条规则在之前的C++标准中已经是建议性的，但C++23把它变成了强制性的编译器规则。

```cpp
#include <iostream>

// C++23: 构造函数体中成员初始化必须按照声明顺序
class OrderedMembers {
public:
    int a;  // 第1个声明
    int b;  // 第2个声明
    int c;  // 第3个声明
    
    OrderedMembers() : a(1), b(2), c(3) {
        // 即使你写成 : c(3), b(2), a(1)
        // 编译器也会强制按声明顺序a,b,c初始化
        // 这是C++23的新规则！
        std::cout << "a=" << a << ", b=" << b << ", c=" << c << std::endl;
    }
};

int main() {
    std::cout << "=== C++23 成员初始化顺序强制 ===" << std::endl;
    
    OrderedMembers obj;
    
    std::cout << "\nC++23: 初始化列表中的顺序必须和声明顺序一致" << std::endl;
    std::cout << "违反的话，编译器会报错！" << std::endl;
    
    return 0;
}
```

运行结果：

```
=== C++23 成员初始化顺序强制 ===
a=1, b=2, c=3

C++23: 初始化列表中的顺序必须和声明顺序一致
违反的话，编译器会报错！
```

> 为什么要有这个规则？因为成员初始化的**实际执行顺序**是按照声明顺序，而不是初始化列表中的顺序。如果两者不一致，而你的代码又依赖于某个特定顺序，就会产生微妙的bug。所以C++23干脆规定：初始化列表的顺序必须和声明顺序一致，否则编译报错！

## 11.13 常见陷阱

C++的类虽好，但其中藏着几个臭名昭著的陷阱。了解它们，才能写出健壮的代码！

### 切片问题

**切片（slicing）**是C++继承体系中一个经典的问题。当派生类对象被赋值给基类对象时（值传递或值赋值），派生类的部分会被"切掉"，只剩下基类部分。这就是所谓的"切片"——就像切蛋糕一样，把上面那层奶油（派生类）给切掉了。

```cpp
#include <iostream>

class Base {
public:
    // 虚函数：派生类可以重写
    virtual void print() const {
        std::cout << "Base::print()" << std::endl;
    }
    
    // 虚析构函数：多态安全的必要条件
    virtual ~Base() {}
};

class Derived : public Base {
public:
    // 重写print方法
    void print() const override {
        std::cout << "Derived::print()" << std::endl;
    }
    
    // 派生类独有的方法
    void extra() const {
        std::cout << "Derived::extra() - 这是派生类独有的！" << std::endl;
    }
};

int main() {
    std::cout << "=== 切片问题演示 ===" << std::endl;
    
    Derived d;
    std::cout << "d创建完毕" << std::endl;
    
    std::cout << "\n--- 切片发生！---" << std::endl;
    Base b = d;  // 切片！Derived部分被"切掉"了！
    b.print();   // 调用的是Base::print()，而不是Derived的！
    
    std::cout << "\n--- 正确做法：用指针或引用 ---" << std::endl;
    
    Base* pb = &d;  // 指向派生类对象
    Base& rb = d;   // 引用到派生类对象
    
    pb->print();  // 调用Derived::print() - 多态生效！
    rb.print();   // 调用Derived::print() - 多态生效！
    
    std::cout << "\n--- 切片的原因 ---" << std::endl;
    std::cout << "b是Base类型的对象，只有Base那么大" << std::endl;
    std::cout << "赋值时只复制了Base部分，Derived部分被丢弃" << std::endl;
    
    return 0;
}
```

运行结果：

```
=== 切片问题演示 ===
d创建完毕

--- 切片发生！---
Base::print()

--- 正确做法：用指针或引用 ---
Derived::print()
Derived::print()

--- 切片的原因 ---
b是Base类型的对象，只有Base那么大
赋值时只复制了Base部分，Derived部分被丢弃
```

> 如何避免切片？
> 1. 用指针或引用代替值传递：`void foo(Base& b)` 或 `void foo(Base* b)`
> 2. 如果必须值传递，考虑使用`virtual clone()`模式
> 3. 传值时三思：这个对象是否真的需要一份副本？

### 构造函数中的虚函数调用

这是另一个经典的"看起来对，实际上错"的陷阱。在基类构造函数中调用虚函数，不会调用到派生类的版本！

为什么会这样？因为在基类构造函数执行时，派生类部分还没有初始化！如果虚函数调用真的派发到派生类，而派生类的虚函数又访问了还没初始化的成员变量——程序就崩溃了。所以C++规定：**在基类构造函数中，虚函数调用不会派发到派生类**。

```cpp
#include <iostream>

class Base {
public:
    Base() {
        std::cout << "Base constructor - calling virtual function" << std::endl;
        print();  // 危险！这里调用的不是派生类的版本！
    }
    
    virtual void print() const {
        std::cout << "Base::print()" << std::endl;
    }
    
    virtual ~Base() {}
};

class Derived : public Base {
private:
    int value_ = 42;  // 派生类独有的成员
    
public:
    Derived() {
        std::cout << "Derived constructor" << std::endl;
    }
    
    // 重写print方法
    void print() const override {
        std::cout << "Derived::print(), value=" << value_ << std::endl;
    }
};

int main() {
    std::cout << "=== 构造函数中的虚函数调用 ===" << std::endl;
    std::cout << "Creating Derived object:" << std::endl;
    
    Derived d;
    
    std::cout << "\n--- 解释 ---" << std::endl;
    std::cout << "在Base构造期间，Derived部分还没初始化！" << std::endl;
    std::cout << "所以虚函数调用不会派发到Derived::print()" << std::endl;
    
    std::cout << "\n--- 对象创建完成后 ---" << std::endl;
    Base* ptr = &d;
    ptr->print();  // 这里会调用派生类的版本，因为对象已经完全构造了
    
    return 0;
}
```

运行结果：

```
=== 构造函数中的虚函数调用 ===
Creating Derived object:
Base constructor - calling virtual function
Base::print()           // 注意！调用的是Base的版本，不是Derived的！

Derived constructor

--- 解释 ---
在Base构造期间，Derived部分还没初始化！
所以虚函数调用不会派发到Derived::print()

--- 对象创建完成后 ---
Derived::print(), value=42
```

> 如何避免这个陷阱？
> 1. 在构造函数中避免调用虚函数
> 2. 如果必须在构造时做些什么，使用两阶段初始化：`init()`函数
> 3. 或者使用工厂模式（Factory Pattern）来控制对象的创建顺序

---

## 本章小结

恭喜你！终于把类与对象基础这一章学完了！让我们来回顾一下都学了什么：

### 核心概念

1. **类与对象**：类是蓝图，对象是按蓝图创建的具体实例。类定义了数据和操作（成员变量和成员函数），对象则是这些定义的具体化。

2. **面向对象三大特性**：
   - **封装**：把数据和方法包装在一起，对外隐藏实现细节，保证数据安全
   - **继承**：从已有类派生出新类，复用代码，实现"is-a"关系
   - **多态**：同一接口不同实现，通过虚函数实现运行时动态绑定

3. **类不变式**：对象生命周期内必须始终满足的条件，是保证对象合法性的"宪法"

### 类的定义与语法

4. **访问控制**：`public`（公有）、`protected`（受保护）、`private`（私有）三级门禁，控制成员的访问权限

5. **构造函数**：对象出生时自动调用的初始化函数
   - 默认构造函数：无参数
   - 带参构造函数：初始化列表更高效
   - 拷贝构造函数：复制一个已有对象
   - 移动构造函数（C++11）："偷取"临时对象资源
   - 委托构造函数（C++11）：构造函数调用其他构造函数
   - `explicit`：防止隐式转换

6. **析构函数**：对象销毁时自动调用的清理函数，**不应该抛出异常**

### 特殊成员函数与规则

7. **赋值运算符重载**：处理已存在对象的赋值操作，需要注意自赋值检查和资源释放

8. **深拷贝 vs 浅拷贝**：浅拷贝只复制指针，深拷贝复制数据。管理动态内存的类必须实现深拷贝！

9. **三五法则与零法则**：
   - 三法则：自定义析构函数、拷贝构造、拷贝赋值之一，就需要自定义全部三个
   - 五法则（C++11）：再加上移动构造和移动赋值
   - 零法则：使用RAII类型，让编译器自动生成特殊成员函数

10. **`=default`与`=delete`**：显式要求编译器生成默认实现，或彻底禁用某个函数

### 现代C++特性

11. **聚合初始化与指定初始化器**：
    - C++20支持`{.x = 1, .y = 2}`形式的指定初始化
    - C++20支持括号形式的聚合初始化

12. **成员初始化顺序强制（C++23）**：初始化列表顺序必须与成员声明顺序一致

### 常见陷阱

13. **切片问题**：值传递/赋值会导致派生类部分被丢弃，用指针或引用避免
14. **构造函数中的虚函数调用**：基类构造期间虚函数不会派发到派生类

---

> 写在最后：类是C++面向对象编程的核心，掌握好这一章的内容，你就迈出了成为C++大师的第一步！但别骄傲，后面的章节还有继承、多态、模板等更精彩的内容等着你。继续加油！
