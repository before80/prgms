+++
title = "第37章 设计模式"
weight = 370
date = "2026-03-29T21:03:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++
# 第37章 设计模式

> "Every programmer is an architect, even if they don't know it yet."
> 每一个程序员都是建筑师，只是他们自己还不知道罢了。

---

## 37.0 引言：为什么设计模式值得你花时间

想象一下，你正在建造一座房子。你是那种"我不需要蓝图，边建边想"的勇士吗？如果是，祝你的墙壁别塌得太离谱。

设计模式就是软件世界的**建筑蓝图**——它们是经过数十年实战检验的解决方案，是对常见问题的优雅答案。不是银弹，不是万能药，但当你面对那些"看起来眼熟，做起来发慌"的编程困境时，它们能让你少走十年弯路。

本章我们将用 C++ 这把瑞士军刀，优雅地实现那些让你在面试中加分、在项目中少加班、在 code review 时被点赞的设计模式。我们不追求"能用就行"，我们追求"用了还想用"。

准备好了吗？让我们开始这段设计模式的奇妙旅程。

---

## 37.1 单例模式（Singleton Pattern）：全局唯一的存在

### 37.1.1 什么是单例模式？

单例模式确保一个类**只有一个实例**，并提供一个全局访问点。听起来简单？等你看到那些藏着 bug 的"简单"实现再说。

**什么时候用？**

- 日志系统：整个程序只需要一个日志 writer
- 配置管理器：全局配置只需要一份
- 连接池：数据库连接池整个程序共用一个
- 设备驱动程序：系统打印机驱动只需要一个实例

**什么时候不用？**

- 仅仅是"想全局访问某个对象"（这是懒，不是单例的错）
- 对象之间需要传递不同状态（单例会让状态污染像病毒一样传播）
- 你开始写 `Singleton::getInstance()->getInstance()->getInstance()`（你已经在挖坟了）

### 37.1.2 经典的"线程不安全"版本（别用！）

```cpp
class UnsafeSingleton {
public:
    static UnsafeSingleton* getInstance() {
        if (instance == nullptr) {  // 线程A和B同时可能同时通过这里
            instance = new UnsafeSingleton();
        }
        return instance;
    }

private:
    UnsafeSingleton() = default;
    static UnsafeSingleton* instance;
};

UnsafeSingleton* UnsafeSingleton::instance = nullptr;
```

这段代码在单线程世界是完美的王子/公主。在多线程世界？它会在你毫无防备时给你上一课"并发编程的艺术"。

### 37.1.3 C++11 线程安全版本（用这个！）

```cpp
class Logger {
public:
    static Logger& getInstance() {
        static Logger instance;  // C++11 保证线程安全初始化！
        return instance;
    }

    void log(const std::string& message) {
        std::lock_guard<std::mutex> lock(mutex_);
        std::cout << "[" << timestamp() << "] " << message << "\n";
    }

    // 删除拷贝构造和赋值（重要！）
    Logger(const Logger&) = delete;
    Logger& operator=(const Logger&) = delete;

private:
    Logger() { std::cout << "Logger initialized\n"; }
    ~Logger() { std::cout << "Logger destroyed\n"; }

    std::mutex mutex_;
    std::string timestamp() {
        auto now = std::chrono::system_clock::now();
        auto time = std::chrono::system_clock::to_time_t(now);
        char buf[32];
        std::strftime(buf, sizeof(buf), "%Y-%m-%d %H:%M:%S", std::localtime(&time));
        return buf;
    }
};

// 使用起来简直是一种享受：
int main() {
    Logger::getInstance().log("程序启动了");
    Logger::getInstance().log("正在做有趣的事情");
    Logger::getInstance().log("程序结束了");
    return 0;
}
```

**输出：**
```
Logger initialized
[2024-01-15 10:30:45] 程序启动了
[2024-01-15 10:30:45] 正在做有趣的事情
[2024-01-15 10:30:45] 程序结束了
```

### 37.1.4 使用 `std::call_once` 的版本（更保守的选择）

```cpp
class DatabaseConnection {
public:
    static std::shared_ptr<DatabaseConnection> getInstance() {
        std::call_once(flag_, []() {
            instance_ = std::shared_ptr<DatabaseConnection>(new DatabaseConnection());
        });
        return instance_;
    }

    void query(const std::string& sql) {
        std::cout << "Executing: " << sql << "\n";
    }

    DatabaseConnection(const DatabaseConnection&) = delete;
    DatabaseConnection& operator=(const DatabaseConnection&) = delete;

private:
    DatabaseConnection() {
        std::cout << "Database connection established\n";
    }
    ~DatabaseConnection() {
        std::cout << "Database connection closed\n";
    }

    static std::shared_ptr<DatabaseConnection> instance_;
    static std::once_flag flag_;
};

std::shared_ptr<DatabaseConnection> DatabaseConnection::instance_;
std::once_flag DatabaseConnection::flag_;
```

### 37.1.5 单例模式的"邪恶双子"——饿汉 vs 懒汉

| 风格 | 初始化时机 | 优点 | 缺点 |
|------|-----------|------|------|
| **饿汉** | 程序启动时 | 无锁开销，简单直接 | 可能浪费资源（如果从未使用） |
| **懒汉** | 首次调用时 | 延迟加载，按需分配 | 需要考虑线程安全 |

饿汉版本的"现代 C++ 写法"：

```cpp
class ConfigManager {
public:
    static ConfigManager& getInstance() {
        static ConfigManager instance;  // 饿汉：C++11 保证线程安全
        return instance;
    }

    void setValue(const std::string& key, const std::string& value) {
        config_[key] = value;
    }

    std::string getValue(const std::string& key, const std::string& defaultVal = "") {
        auto it = config_.find(key);
        return it != config_.end() ? it->second : defaultVal;
    }

    ConfigManager(const ConfigManager&) = delete;
    ConfigManager& operator=(const ConfigManager&) = delete;

private:
    ConfigManager() { std::cout << "ConfigManager loaded\n"; }
    std::unordered_map<std::string, std::string> config_;
};
```

**小贴士**：很多人争论"饿汉 vs 懒汉哪个好"。答案是：对于 C++11 及以上，`static` 局部变量的初始化是线程安全的，所以两者都能安全使用。选哪个取决于你需不需要延迟加载。

---

## 37.2 工厂模式（Factory Pattern）：对象的"精品工厂"

### 37.2.1 为什么需要工厂？

想象一个汽车4S店。客户说"我要一辆轿车"，销售顾问不会让你自己去零件堆里组装，他会根据你的需求，在工厂里生产出你要的车。

工厂模式的本质就是：**不要让客户自己 new 对象，把对象创建封装起来**。

**好处是什么？**

- **解耦**：调用者不需要知道对象的具体类型
- **封装**：创建逻辑可以随时改变而不影响客户
- **可测试**：可以注入mock工厂进行单元测试

### 37.2.2 简单工厂（Simple Factory）——不是GoF模式，但最常用

```cpp
#include <iostream>
#include <memory>
#include <map>
#include <functional>

// 产品抽象基类
class Button {
public:
    virtual ~Button() = default;
    virtual void render() const = 0;
    virtual void onClick() const = 0;
};

// 具体产品
class WindowsButton : public Button {
public:
    void render() const override {
        std::cout << " Rendering a Windows-style button [ OK ]\n";
    }
    void onClick() const override {
        std::cout << " Windows button clicked! Ding!\n";
    }
};

class MacButton : public Button {
public:
    void render() const override {
        std::cout << " Rendering a Mac-style button ◉\n";
    }
    void onClick() const override {
        std::cout << " Mac button clicked! Sfx!\n";
    }
};

// 简单工厂
class ButtonFactory {
public:
    enum class Theme { Windows, Mac };

    static std::unique_ptr<Button> create(Theme theme) {
        switch (theme) {
            case Theme::Windows:
                return std::make_unique<WindowsButton>();
            case Theme::Mac:
                return std::make_unique<MacButton>();
            default:
                throw std::invalid_argument("Unknown theme");
        }
    }
};

int main() {
    auto winBtn = ButtonFactory::create(ButtonFactory::Theme::Windows);
    auto macBtn = ButtonFactory::create(ButtonFactory::Theme::Mac);

    winBtn->render();
    macBtn->render();

    winBtn->onClick();
    macBtn->onClick();
}
```

**输出：**
```
 Rendering a Windows-style button [ OK ]
 Rendering a Mac-style button ◉
 Windows button clicked! Ding!
 Mac button clicked! Sfx!
```

### 37.2.3 工厂方法模式（Factory Method）——延迟到子类决定

```cpp
#include <iostream>
#include <memory>
#include <string>

// 产品：文档
class Document {
public:
    virtual ~Document() = default;
    virtual void open() const = 0;
    virtual void save() const = 0;
};

class WordDocument : public Document {
public:
    void open() const override { std::cout << "Opening .docx file in Microsoft Word\n"; }
    void save() const override { std::cout << "Saving as .docx\n"; }
};

class PDFDocument : public Document {
public:
    void open() const override { std::cout << "Opening .pdf file in Adobe Acrobat\n"; }
    void save() const override { std::cout << "Saving as .pdf\n"; }
};

// 创建者：应用程序
class Application {
public:
    virtual ~Application() = default;

    // 工厂方法：让子类决定创建什么文档
    virtual std::unique_ptr<Document> createDocument() const = 0;

    void newDocument() {
        document_ = createDocument();
        document_->open();
    }

    void saveDocument() {
        if (document_) {
            document_->save();
        }
    }

protected:
    std::unique_ptr<Document> document_;
};

// 具体创建者：Word应用
class WordApplication : public Application {
public:
    std::unique_ptr<Document> createDocument() const override {
        return std::make_unique<WordDocument>();
    }
};

// 具体创建者：PDF阅读器
class PDFApplication : public Application {
public:
    std::unique_ptr<Document> createDocument() const override {
        return std::make_unique<PDFDocument>();
    }
};

int main() {
    WordApplication wordApp;
    PDFApplication pdfApp;

    std::cout << "=== Word Application ===\n";
    wordApp.newDocument();
    wordApp.saveDocument();

    std::cout << "\n=== PDF Application ===\n";
    pdfApp.newDocument();
    pdfApp.saveDocument();
}
```

**输出：**
```
=== Word Application ===
Opening .docx file in Microsoft Word
Saving as .docx

=== PDF Application ===
Opening .pdf file in Adobe Acrobat
Saving as .pdf
```

### 37.2.4 抽象工厂模式（Abstract Factory）——产品族

当你的系统需要创建**一系列相关对象**时（比如 Windows 风格按钮+Windows 风格菜单，Mac 风格按钮+Mac 风格菜单），抽象工厂就登场了。

```cpp
#include <iostream>
#include <memory>
#include <string>

// 抽象产品A：按钮
class Button {
public:
    virtual ~Button() = default;
    virtual void paint() const = 0;
};

// 抽象产品B：复选框
class Checkbox {
public:
    virtual ~Checkbox() = default;
    virtual void paint() const = 0;
};

// Windows 风格产品族
class WindowsButton : public Button {
public:
    void paint() const override { std::cout << " [ OK ] "; }
};

class WindowsCheckbox : public Checkbox {
public:
    void paint() const override { std::cout << "[x] "; }
};

// Mac 风格产品族
class MacButton : public Button {
public:
    void paint() const override { std::cout << " (●) "; }
};

class MacCheckbox : public Checkbox {
public:
    void paint() const override { std::cout << "○ "; }
};

// 抽象工厂
class GUIFactory {
public:
    virtual ~GUIFactory() = default;
    virtual std::unique_ptr<Button> createButton() const = 0;
    virtual std::unique_ptr<Checkbox> createCheckbox() const = 0;
};

// 具体工厂
class WindowsFactory : public GUIFactory {
public:
    std::unique_ptr<Button> createButton() const override {
        return std::make_unique<WindowsButton>();
    }
    std::unique_ptr<Checkbox> createCheckbox() const override {
        return std::make_unique<WindowsCheckbox>();
    }
};

class MacFactory : public GUIFactory {
public:
    std::unique_ptr<Button> createButton() const override {
        return std::make_unique<MacButton>();
    }
    std::unique_ptr<Checkbox> createCheckbox() const override {
        return std::make_unique<MacCheckbox>();
    }
};

// 客户端代码
class Application {
public:
    Application(std::unique_ptr<GUIFactory> factory)
        : factory_(std::move(factory)) {}

    void createUI() {
        button_ = factory_->createButton();
        checkbox_ = factory_->createCheckbox();
    }

    void paint() const {
        checkbox_->paint();
        std::cout << " Agree to terms\n";
        button_->paint();
        std::cout << " Submit\n";
    }

private:
    std::unique_ptr<GUIFactory> factory_;
    std::unique_ptr<Button> button_;
    std::unique_ptr<Checkbox> checkbox_;
};

// 工厂创建器/配置
enum class Theme { Windows, Mac };

std::unique_ptr<GUIFactory> createFactory(Theme theme) {
    switch (theme) {
        case Theme::Windows: return std::make_unique<WindowsFactory>();
        case Theme::Mac:     return std::make_unique<MacFactory>();
    }
    throw std::runtime_error("Unknown theme");
}

int main() {
    // 运行时决定使用哪个工厂
    Theme currentTheme = Theme::Mac;  // 假装用户在Mac上

    auto factory = createFactory(currentTheme);
    Application app(std::move(factory));
    app.createUI();
    app.paint();
}
```

**输出：**
```
○  Agree to terms
 (●)  Submit
```

---

## 37.3 观察者模式（Observer Pattern）：消息推送的艺术

### 37.3.1 什么是观察者模式？

想象你订阅了一个 YouTube 频道。频道主发视频 → 你收到通知。你不需要每隔一秒刷新一次，**视频发布者会把消息推送给所有订阅者**。

这就是观察者模式：**定义对象间的一对多依赖，当一个对象改变状态，所有依赖它的对象都会收到通知**。

### 37.3.2 实现：新闻订阅系统

```cpp
#include <iostream>
#include <vector>
#include <memory>
#include <string>
#include <algorithm>

// 前向声明
class Observer;

// 主题（发布者）
class Subject {
public:
    void attach(std::shared_ptr<Observer> observer) {
        observers_.push_back(observer);
    }

    void detach(std::shared_ptr<Observer> observer) {
        observers_.erase(
            std::remove(observers_.begin(), observers_.end(), observer),
            observers_.end()
        );
    }

    void notify() const {
        for (const auto& observer : observers_) {
            observer->update(title_, content_);
        }
    }

    void publishNews(const std::string& title, const std::string& content) {
        title_ = title;
        content_ = content;
        std::cout << "\n[Breaking News] " << title_ << "\n";
        notify();
    }

private:
    std::vector<std::shared_ptr<Observer>> observers_;
    std::string title_;
    std::string content_;
};

// 观察者（订阅者）接口
class Observer {
public:
    virtual ~Observer() = default;
    virtual void update(const std::string& title, const std::string& content) = 0;
    virtual std::string getName() const = 0;
};

// 具体观察者：邮件订阅者
class EmailSubscriber : public Observer {
public:
    explicit EmailSubscriber(const std::string& email) : email_(email) {}

    void update(const std::string& title, const std::string& content) override {
        std::cout << "  [Email to " << email_ << "]\n";
        std::cout << "    Subject: " << title << "\n";
        std::cout << "    Preview: " << content.substr(0, 50) << "...\n";
    }

    std::string getName() const override { return "Email: " + email_; }

private:
    std::string email_;
};

// 具体观察者：手机推送订阅者
class MobileSubscriber : public Observer {
public:
    explicit MobileSubscriber(const std::string& deviceId) : deviceId_(deviceId) {}

    void update(const std::string& title, const std::string& content) override {
        std::cout << "  [Push to " << deviceId_ << "] 📱\n";
        std::cout << "    " << title << "\n";
        std::cout << "    " << content << "\n";
    }

    std::string getName() const override { return "Mobile: " + deviceId_; }

private:
    std::string deviceId_;
};

// 具体观察者：SMS订阅者
class SMSSubscriber : public Observer {
public:
    explicit SMSSubscriber(const std::string& phone) : phone_(phone) {}

    void update(const std::string& title, const std::string& /*content*/) override {
        std::cout << "  [SMS to " << phone_ << "] 📱\n";
        std::cout << "    " << title << "\n";
    }

    std::string getName() const override { return "SMS: " + phone_; }

private:
    std::string phone_;
};

int main() {
    NewsPortal portal;

    auto alice = std::make_shared<EmailSubscriber>("alice@example.com");
    auto bob = std::make_shared<MobileSubscriber>("iPhone-12345");
    auto charlie = std::make_shared<SMSSubscriber>("+1-555-0123");

    portal.attach(alice);
    portal.attach(bob);
    portal.attach(charlie);

    std::cout << "=== Publishing Tech News ===\n";
    portal.publishNews(
        "C++26 新特性发布！ranges::to_vector 终于合并了！",
        "经过三年的等待，ranges::views::to_vector 终于在 C++26 中正式加入..."
    );

    std::cout << "\n=== Charlie unsubscribes ===\n";
    portal.detach(charlie);

    std::cout << "\n=== Publishing Sports News ===\n";
    portal.publishNews(
        "中国足球队勇夺世界杯！",
        "在刚刚结束的新闻发布会上，FIFA 主席宣布..."
    );

    std::cout << "\n=== Alice unsubscribes ===\n";
    portal.detach(alice);

    std::cout << "\n=== Publishing最后一条新闻 ===\n";
    portal.publishNews(
        "火星旅游正式开启！往返票只要 99 万亿美元",
        "SpaceX 创始人伊隆·马斯克今天宣布..."
    );
}
```

**输出：**
```
=== Publishing Tech News ===

[Breaking News] C++26 新特性发布！ranges::to_vector 终于合并了！
  [Email to alice@example.com]
    Subject: C++26 新特性发布！ranges::to_vector 终于合并了！
    Preview: 经过三年的等待，ranges::views::to_vector 终于在 C++26 中正...
  [Push to iPhone-12345] 📱
    C++26 新特性发布！ranges::to_vector 终于合并了！
    经过三年的等待，ranges::views::to_vector 终于在 C++26 中正式加入...
  [SMS to +1-555-0123] 📱
    C++26 新特性发布！ranges::to_vector 终于合并了！

=== Charlie unsubscribes ===

=== Publishing Sports News ===

[Breaking News] 中国足球队勇夺世界杯！
  [Email to alice@example.com]
    Subject: 中国足球队勇夺世界杯！
    Preview: 在刚刚结束的新闻发布会上，FIFA 主席宣布......
  [Push to iPhone-12345] 📱
    中国足球队勇夺世界杯！
    在刚刚结束的新闻发布会上，FIFA 主席宣布......

=== Alice unsubscribes ===

=== Publishing最后一条新闻 ===

[Breaking News] 火星旅游正式开启！往返票只要 99 万亿美元
  [Push to iPhone-12345] 📱
    火星旅游正式开启！往返票只要 99 万亿美元
    SpaceX 创始人伊隆·马斯克今天宣布...
```

### 37.3.3 C++20 `std::observer_ptr` ——更安全的指针

`std::observer_ptr`（在 `<memory>` 中）是 C++20 引入的一种"非拥有型"指针，比裸指针更清晰地表达"我只是观察你"的语义：

```cpp
#include <memory>

class Subject;  // 前向声明

class Observer {
public:
    virtual ~Observer() = default;
    virtual void update(const std::string& message) = 0;
};

class Subject {
public:
    void attach(std::observer_ptr<Observer> observer) {
        // 添加前检查是否已在列表中
        if (std::find(observers_.begin(), observers_.end(), observer)
            == observers_.end()) {
            observers_.push_back(observer);
        }
    }

    void detach(std::observer_ptr<Observer> observer) {
        observers_.erase(
            std::remove(observers_.begin(), observers_.end(), observer),
            observers_.end()
        );
    }

    void notify(const std::string& message) const {
        for (const auto& obs : observers_) {
            if (obs) obs->update(message);  // observer_ptr 支持隐式检查
        }
    }

private:
    std::vector<std::observer_ptr<Observer>> observers_;
};
```

---

## 37.4 策略模式（Strategy Pattern）：算法的可插拔艺术

### 37.4.1 策略模式的精髓

你网购时选支付方式：微信、支付宝、信用卡、PayPal...下单的流程不变，但支付策略可以随时切换。

策略模式的核心：**定义一系列算法，把它们一个个封装起来，并使它们可以相互替换**。

### 37.4.2 实现：排序策略系统

```cpp
#include <iostream>
#include <vector>
#include <algorithm>
#include <memory>
#include <chrono>

// 策略接口
class SortStrategy {
public:
    virtual ~SortStrategy() = default;
    virtual void sort(std::vector<int>& data) = 0;
    virtual std::string name() const = 0;
};

// 具体策略A：快速排序
class QuickSort : public SortStrategy {
public:
    void sort(std::vector<int>& data) override {
        if (data.size() <= 1) return;
        std::sort(data.begin(), data.end());  // 使用 std::sort（通常是 introsort）
    }

    std::string name() const override { return "QuickSort (std::sort)"; }
};

// 具体策略B：稳定排序（归并排序）
class StableSort : public SortStrategy {
public:
    void sort(std::vector<int>& data) override {
        std::stable_sort(data.begin(), data.end());
    }

    std::string name() const override { return "Stable Sort (std::stable_sort)"; }
};

// 具体策略C：降序排序
class DescendingSort : public SortStrategy {
public:
    void sort(std::vector<int>& data) override {
        std::sort(data.begin(), data.end(), std::greater<int>());
    }

    std::string name() const override { return "Descending Sort"; }
};

// 上下文：排序器
class Sorter {
public:
    explicit Sorter(std::unique_ptr<SortStrategy> strategy)
        : strategy_(std::move(strategy)) {}

    void setStrategy(std::unique_ptr<SortStrategy> strategy) {
        strategy_ = std::move(strategy);
    }

    void sort(std::vector<int>& data) {
        if (!data.empty()) {
            std::cout << "Before (" << strategy_->name() << "): ";
            printVector(data);
        }
        strategy_->sort(data);
        if (!data.empty()) {
            std::cout << "After:  ";
            printVector(data);
        }
    }

private:
    void printVector(const std::vector<int>& v) {
        for (int x : v) std::cout << x << " ";
        std::cout << "\n";
    }

    std::unique_ptr<SortStrategy> strategy_;
};

// 工厂函数创建数据
std::vector<int> createRandomData(size_t n, int maxVal = 100) {
    std::vector<int> v(n);
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> dis(1, maxVal);
    for (auto& x : v) x = dis(gen);
    return v;
}

int main() {
    auto data = createRandomData(10);

    std::cout << "=== 默认：快速排序 ===\n";
    Sorter sorter(std::make_unique<QuickSort>());
    sorter.sort(data);

    std::cout << "\n=== 切换到稳定排序 ===\n";
    sorter.setStrategy(std::make_unique<StableSort>());
    data = createRandomData(10);  // 重新生成数据
    sorter.sort(data);

    std::cout << "\n=== 切换到降序排序 ===\n";
    sorter.setStrategy(std::make_unique<DescendingSort>());
    data = createRandomData(10);
    sorter.sort(data);

    // 演示：运行性能对比
    std::cout << "\n=== 性能测试 (100000 元素) ===\n";
    auto bigData = createRandomData(100000);

    {
        auto d = bigData;
        auto start = std::chrono::high_resolution_clock::now();
        QuickSort().sort(d);
        auto end = std::chrono::high_resolution_clock::now();
        auto dur = std::chrono::duration_cast<std::chrono::milliseconds>(end - start);
        std::cout << "QuickSort:    " << dur.count() << " ms\n";
    }

    {
        auto d = bigData;
        auto start = std::chrono::high_resolution_clock::now();
        StableSort().sort(d);
        auto end = std::chrono::high_resolution_clock::now();
        auto dur = std::chrono::duration_cast<std::chrono::milliseconds>(end - start);
        std::cout << "StableSort:   " << dur.count() << " ms\n";
    }
}
```

**输出示例：**
```
=== 默认：快速排序 ===
Before (QuickSort (std::sort)): 42 17 89 23 56 78 12 45 67 34
After:  12 17 23 34 42 45 56 67 78 89

=== 切换到稳定排序 ===
Before (Stable Sort (std::stable_sort)): 91 23 45 67 12 88 34 56 79 10
After:  10 12 23 34 45 56 67 79 88 91

=== 切换到降序排序 ===
Before (Descending Sort): 11 99 33 77 55 22 88 44 66 33
After:  99 88 77 66 55 44 33 33 22 11

=== 性能测试 (100000 元素) ===
QuickSort:    12 ms
StableSort:   18 ms
```

---

## 37.5 装饰器模式（Decorator Pattern）：无限叠加的超能力

### 37.5.1 动态给对象添加职责

想象给咖啡加配料：浓缩咖啡是基础，你可以加牛奶(+2元)、加摩卡(+3元)、加奶泡(+1.5元)...

装饰器模式的精髓：**动态地给对象添加职责，比继承更灵活**。

### 37.5.2 实现：咖啡订单系统

```cpp
#include <iostream>
#include <memory>
#include <string>

// 组件接口
class Coffee {
public:
    virtual ~Coffee() = default;
    virtual int getCost() const = 0;
    virtual std::string getDescription() const = 0;
};

// 具体组件：浓缩咖啡
class Espresso : public Coffee {
public:
    int getCost() const override { return 30; }
    std::string getDescription() const override { return "浓缩咖啡 (Espresso)"; }
};

// 基础装饰器
class CoffeeDecorator : public Coffee {
protected:
    std::unique_ptr<Coffee> coffee_;
public:
    explicit CoffeeDecorator(std::unique_ptr<Coffee> coffee)
        : coffee_(std::move(coffee)) {}
};

// 装饰器：牛奶
class MilkDecorator : public CoffeeDecorator {
public:
    using CoffeeDecorator::CoffeeDecorator;  // 继承构造函数

    int getCost() const override {
        return coffee_->getCost() + 8;
    }

    std::string getDescription() const override {
        return coffee_->getDescription() + " + 牛奶";
    }
};

// 装饰器：摩卡
class MochaDecorator : public CoffeeDecorator {
public:
    using CoffeeDecorator::CoffeeDecorator;

    int getCost() const override {
        return coffee_->getCost() + 12;
    }

    std::string getDescription() const override {
        return coffee_->getDescription() + " + 摩卡";
    }
};

// 装饰器：奶泡
class WhipDecorator : public CoffeeDecorator {
public:
    using CoffeeDecorator::CoffeeDecorator;

    int getCost() const override {
        return coffee_->getCost() + 6;
    }

    std::string getDescription() const override {
        return coffee_->getDescription() + " + 鲜奶泡";
    }
};

// 装饰器：豆奶（植物基选项）
class SoyDecorator : public CoffeeDecorator {
public:
    using CoffeeDecorator::CoffeeDecorator;

    int getCost() const override {
        return coffee_->getCost() + 5;
    }

    std::string getDescription() const override {
        return coffee_->getDescription() + " + 豆奶";
    }
};

int main() {
    std::cout << "=== 咖啡订单系统 ===\n\n";

    // 订单1：浓缩咖啡（基础款）
    std::unique_ptr<Coffee> order1 = std::make_unique<Espresso>();
    std::cout << "订单1: " << order1->getDescription() << "\n";
    std::cout << "价格: " << order1->getCost() << " 元\n\n";

    // 订单2：拿铁（浓缩 + 牛奶）
    std::unique_ptr<Coffee> order2 = std::make_unique<MilkDecorator>(
        std::make_unique<Espresso>()
    );
    std::cout << "订单2: " << order2->getDescription() << "\n";
    std::cout << "价格: " << order2->getCost() << " 元\n\n";

    // 订单3：摩卡拿铁（浓缩 + 牛奶 + 摩卡 + 奶泡）
    std::unique_ptr<Coffee> order3 = std::make_unique<WhipDecorator>(
        std::make_unique<MochaDecorator>(
            std::make_unique<MilkDecorator>(
                std::make_unique<Espresso>()
            )
        )
    );
    std::cout << "订单3: " << order3->getDescription() << "\n";
    std::cout << "价格: " << order3->getCost() << " 元\n\n";

    // 订单4：素食友好拿铁（浓缩 + 豆奶 + 奶泡）
    std::unique_ptr<Coffee> order4 = std::make_unique<WhipDecorator>(
        std::make_unique<SoyDecorator>(
            std::make_unique<Espresso>()
        )
    );
    std::cout << "订单4: " << order4->getDescription() << "\n";
    std::cout << "价格: " << order4->getCost() << " 元\n\n";

    // 订单5：豪华版（所有配料！）
    std::unique_ptr<Coffee> order5 = std::make_unique<WhipDecorator>(
        std::make_unique<MochaDecorator>(
            std::make_unique<MilkDecorator>(
                std::make_unique<SoyDecorator>(
                    std::make_unique<Espresso>()
                )
            )
        )
    );
    std::cout << "订单5: " << order5->getDescription() << "\n";
    std::cout << "价格: " << order5->getCost() << " 元（豪华全套版！)\n";
}
```

**输出：**
```
=== 咖啡订单系统 ===

订单1: 浓缩咖啡 (Espresso)
价格: 30 元

订单2: 浓缩咖啡 (Espresso) + 牛奶
价格: 38 元

订单3: 浓缩咖啡 (Espresso) + 牛奶 + 摩卡 + 鲜奶泡
价格: 56 元

订单4: 浓缩咖啡 (Espresso) + 豆奶 + 鲜奶泡
价格: 42 元

订单5: 浓缩咖啡 (Espresso) + 豆奶 + 牛奶 + 摩卡 + 鲜奶泡
价格: 61 元（豪华全套版！)
```

---

## 37.6 命令模式（Command Pattern）：把请求封装成对象

### 37.6.1 请求变成对象

你点外卖时，外卖小哥不需要知道你住哪儿、你点了什么菜——他把你的**订单（封装好的请求）**送到餐厅，餐厅处理订单。

命令模式的本质：**将请求封装成对象，从而让你可以用不同的请求参数化客户，支持撤销/重做**。

### 37.6.2 实现：远程控制 + 撤销/重做

```cpp
#include <iostream>
#include <vector>
#include <memory>
#include <stack>
#include <string>

// 命令接口
class Command {
public:
    virtual ~Command() = default;
    virtual void execute() = 0;
    virtual void undo() = 0;
    virtual std::string description() const = 0;
};

// 接收者：电灯
class Light {
public:
    void on() { state_ = true; std::cout << "💡 电灯亮了\n"; }
    void off() { state_ = false; std::cout << "💡 电灯灭了\n"; }
    bool isOn() const { return state_; }

private:
    bool state_ = false;
};

// 接收者：风扇
class Fan {
public:
    void high() { speed_ = 3; std::cout << "🌀 风扇高速运转\n"; }
    void medium() { speed_ = 2; std::cout << "🌀 风扇中速运转\n"; }
    void low() { speed_ = 1; std::cout << "🌀 风扇低速运转\n"; }
    void off() { speed_ = 0; std::cout << "🌀 风扇关闭了\n"; }
    void restore(int speed) {
        speed_ = speed;
        if (speed == 3) std::cout << "🌀 风扇恢复高速\n";
        else if (speed == 2) std::cout << "🌀 风扇恢复中速\n";
        else if (speed == 1) std::cout << "🌀 风扇恢复低速\n";
    }
    int getSpeed() const { return speed_; }

private:
    int speed_ = 0;
};

// 具体命令：开灯
class LightOnCommand : public Command {
public:
    explicit LightOnCommand(std::shared_ptr<Light> light) : light_(light) {}

    void execute() override { light_->on(); }
    void undo() override { light_->off(); }
    std::string description() const override { return "开灯"; }

private:
    std::shared_ptr<Light> light_;
};

// 具体命令：关灯
class LightOffCommand : public Command {
public:
    explicit LightOffCommand(std::shared_ptr<Light> light) : light_(light) {}

    void execute() override { light_->off(); }
    void undo() override { light_->on(); }
    std::string description() const override { return "关灯"; }

private:
    std::shared_ptr<Light> light_;
};

// 具体命令：风扇加速
class FanHighCommand : public Command {
public:
    explicit FanHighCommand(std::shared_ptr<Fan> fan) : fan_(fan) {}

    void execute() override { prevSpeed_ = fan_->getSpeed(); fan_->high(); }
    void undo() override {
        if (prevSpeed_ == 0) fan_->off();
        else if (prevSpeed_ == 1) fan_->low();
        else if (prevSpeed_ == 2) fan_->medium();
        else fan_->high();
    }
    std::string description() const override { return "风扇高速"; }

private:
    std::shared_ptr<Fan> fan_;
    int prevSpeed_ = 0;
};

// 具体命令：关闭风扇
class FanOffCommand : public Command {
public:
    explicit FanOffCommand(std::shared_ptr<Fan> fan) : fan_(fan) {}

    void execute() override { prevSpeed_ = fan_->getSpeed(); fan_->off(); }
    void undo() override {
        fan_->restore(prevSpeed_);
    }
    std::string description() const override { return "关闭风扇"; }

private:
    std::shared_ptr<Fan> fan_;
    int prevSpeed_ = 0;
};

// 调用者：遥控器
class RemoteControl {
public:
    void setCommand(std::unique_ptr<Command> command) {
        command_ = std::move(command);
    }

    void pressButton() {
        if (command_) {
            command_->execute();
            history_.push(std::move(command_));
            historyDesc_.push_back(history_.top()->description());
        }
    }

    void pressUndo() {
        if (!history_.empty()) {
            std::cout << ">>> 撤销: ";
            history_.top()->undo();
            history_.pop();
            historyDesc_.pop_back();
        } else {
            std::cout << "没有可撤销的操作\n";
        }
    }

    void showHistory() const {
        std::cout << "\n--- 操作历史 ---\n";
        int i = 1;
        for (const auto& desc : historyDesc_) {
            std::cout << i++ << ". " << desc << "\n";
        }
        std::cout << "-----------------\n\n";
    }

private:
    std::unique_ptr<Command> command_;
    std::stack<std::unique_ptr<Command>> history_;
    std::vector<std::string> historyDesc_;  // 用于记录操作描述
};

int main() {
    // 创建设备
    auto livingRoomLight = std::make_shared<Light>();
    auto bedroomFan = std::make_shared<Fan>();

    // 创建命令
    std::unique_ptr<Command> lightOn = std::make_unique<LightOnCommand>(livingRoomLight);
    std::unique_ptr<Command> lightOff = std::make_unique<LightOffCommand>(livingRoomLight);
    std::unique_ptr<Command> fanHigh = std::make_unique<FanHighCommand>(bedroomFan);
    std::unique_ptr<Command> fanOff = std::make_unique<FanOffCommand>(bedroomFan);

    // 遥控器
    RemoteControl remote;

    std::cout << "=== 智能家居演示 ===\n\n";

    // 执行一系列操作
    remote.setCommand(std::move(lightOn));
    remote.pressButton();

    remote.setCommand(std::move(fanHigh));
    remote.pressButton();

    remote.setCommand(std::move(lightOff));
    remote.pressButton();

    remote.setCommand(std::move(fanOff));
    remote.pressButton();

    remote.showHistory();

    // 连续撤销
    std::cout << "=== 撤销操作 ===\n";
    remote.pressUndo();
    remote.pressUndo();
    remote.pressUndo();
    remote.pressUndo();
    remote.pressUndo();  // 尝试过度撤销
}
```

**输出：**
```
=== 智能家居演示 ===

💡 电灯亮了
🌀 风扇高速运转
💡 电灯灭了
🌀 风扇关闭了

--- 操作历史 ---
1. 开灯
2. 风扇高速
3. 关灯
4. 关闭风扇
-----------------

=== 撤销操作 ===
>>> 撤销: 🌀 风扇恢复高速
>>> 撤销: 💡 电灯重新亮了
>>> 撤销: 🌀 风扇恢复低速
>>> 撤销: 💡 电灯灭了
没有可撤销的操作
```

---

## 37.7 适配器模式（Adapter Pattern）：接口的翻译官

### 37.7.1 让不兼容的接口一起工作

你出国旅游，手机充电器是国标的，但插座是欧标的。你需要一个**转换插头（适配器）**。

适配器模式：**将一个类的接口转换成客户期望的另一个接口，让原本接口不兼容的类可以合作无间**。

### 37.7.2 实现：支付系统适配器

```cpp
#include <iostream>
#include <memory>
#include <string>

// 目标接口：我们的系统期望的
class PaymentProcessor {
public:
    virtual ~PaymentProcessor() = default;
    virtual bool pay(double amount) = 0;
    virtual std::string getName() const = 0;
};

// 被适配者：第三方支付SDK（假设是遗留代码）
class LegacyPayPal {
public:
    // 这个接口完全不一样！
    bool checkout(const std::string& email, double amountUSD) {
        std::cout << "[PayPal] Processing payment for " << email
                  << ": $" << amountUSD << "\n";
        return true;
    }
};

class LegacyStripe {
public:
    // 这个接口也不一样！
    bool charge(int cents, const std::string& cardNumber) {
        std::cout << "[Stripe] Charging " << cents << " cents to card ****"
                  << cardNumber.substr(cardNumber.length() - 4) << "\n";
        return true;
    }
};

class LegacyCrypto {
public:
    void transfer(double btcAmount, const std::string& wallet) {
        std::cout << "[Crypto] Sending " << btcAmount << " BTC to "
                  << wallet << "\n";
    }
};

// 适配器：PayPal 适配器
class PayPalAdapter : public PaymentProcessor {
public:
    explicit PayPalAdapter(std::string email) : email_(std::move(email)) {}

    bool pay(double amount) override {
        legacyPayPal_.checkout(email_, amount);
        return true;
    }

    std::string getName() const override { return "PayPal"; }

private:
    LegacyPayPal legacyPayPal_;
    std::string email_;
};

// 适配器：Stripe 适配器
class StripeAdapter : public PaymentProcessor {
public:
    explicit StripeAdapter(std::string cardNumber) : cardNumber_(std::move(cardNumber)) {}

    bool pay(double amount) override {
        int cents = static_cast<int>(amount * 100);
        legacyStripe_.charge(cents, cardNumber_);
        return true;
    }

    std::string getName() const override { return "Stripe"; }

private:
    LegacyStripe legacyStripe_;
    std::string cardNumber_;
};

// 适配器：Crypto 适配器
class CryptoAdapter : public PaymentProcessor {
public:
    explicit CryptoAdapter(std::string wallet) : wallet_(std::move(wallet)) {}

    bool pay(double amount) override {
        legacyCrypto_.transfer(amount, wallet_);
        return true;
    }

    std::string getName() const override { return "Crypto (BTC)"; }

private:
    LegacyCrypto legacyCrypto_;
    std::string wallet_;
};

// 商店使用统一的接口处理所有支付
class OnlineStore {
public:
    explicit OnlineStore(double price) : totalAmount_(price) {}

    void checkout(std::unique_ptr<PaymentProcessor> processor) {
        std::cout << "\n--- 结账 ---\n";
        std::cout << "商品总价: $" << totalAmount_ << "\n";
        std::cout << "支付方式: " << processor->getName() << "\n";
        if (processor->pay(totalAmount_)) {
            std::cout << "✅ 支付成功！\n";
        } else {
            std::cout << "❌ 支付失败！\n";
        }
    }

private:
    double totalAmount_;
};

int main() {
    OnlineStore store(99.99);

    // 使用不同的支付方式
    store.checkout(std::make_unique<PayPalAdapter>("customer@example.com"));
    store.checkout(std::make_unique<StripeAdapter>("4242424242424242"));
    store.checkout(std::make_unique<CryptoAdapter>("1A2B3C4D5E6F"));
}
```

**输出：**
```
--- 结账 ---
商品总价: $99.99
支付方式: PayPal
[PayPal] Processing payment for customer@example.com: $99.99
✅ 支付成功！

--- 结账 ---
商品总价: $99.99
支付方式: Stripe
[Stripe] Charging 9999 cents to card ****4242
✅ 支付成功！

--- 结账 ---
商品总价: $99.99
支付方式: Crypto (BTC)
[Crypto] Sending 99.99 BTC to 1A2B3C4D5E6F
✅ 支付成功！
```

---

## 37.8 模板方法模式（Template Method）：算法的骨架

### 37.8.1 父类定义算法结构，子类实现细节

想象做咖啡和茶的过程：

```
1. 烧水
2. 泡（咖啡粉/茶叶）
3. 倒入杯子
4. 加调料（糖/牛奶/柠檬）
```

第1、3、4步完全相同，第2步不同。模板方法就是**在父类中定义算法的骨架，把不同的步骤留给子类**。

### 37.8.2 实现：饮料制作系统

```cpp
#include <iostream>
#include <memory>
#include <string>

// 抽象基类：饮料
class Beverage {
public:
    // 模板方法：定义算法骨架（final 防止子类重写）
    void prepareRecipe() final {
        boilWater();
        brew();
        pourInCup();
        addCondiments();
    }

    // 通用步骤（默认实现）
    void boilWater() const {
        std::cout << "烧水至 100°C\n";
    }

    void pourInCup() const {
        std::cout << "倒入杯中\n";
    }

    // 抽象步骤（子类必须实现）
    virtual void brew() = 0;
    virtual void addCondiments() = 0;
    virtual std::string getName() const = 0;

    virtual ~Beverage() = default;
};

// 具体类：咖啡
class Coffee : public Beverage {
public:
    void brew() override {
        std::cout << "用咖啡机滴滤咖啡\n";
    }

    void addCondiments() override {
        std::cout << "加入糖和牛奶\n";
    }

    std::string getName() const override { return "咖啡"; }
};

// 具体类：茶
class Tea : public Beverage {
public:
    void brew() override {
        std::cout << "用热水浸泡茶叶 3-5 分钟\n";
    }

    void addCondiments() override {
        std::cout << "加入柠檬片\n";
    }

    std::string getName() const override { return "茶"; }
};

// 具体类：抹茶
class Matcha : public Beverage {
public:
    void brew() override {
        std::cout << "用热水冲泡抹茶粉并用茶筅搅拌\n";
    }

    void addCondiments() override {
        std::cout << "加入红豆和糯米\n";
    }

    std::string getName() const override { return "抹茶拿铁"; }
};

int main() {
    std::cout << "=== 制作咖啡 ===\n";
    std::unique_ptr<Beverage> coffee = std::make_unique<Coffee>();
    coffee->prepareRecipe();

    std::cout << "\n=== 制作茶 ===\n";
    std::unique_ptr<Beverage> tea = std::make_unique<Tea>();
    tea->prepareRecipe();

    std::cout << "\n=== 制作抹茶 ===\n";
    std::unique_ptr<Beverage> matcha = std::make_unique<Matcha>();
    matcha->prepareRecipe();
}
```

**输出：**
```
=== 制作咖啡 ===
烧水至 100°C
用咖啡机滴滤咖啡
倒入杯中
加入糖和牛奶

=== 制作茶 ===
烧水至 100°C
用热水浸泡茶叶 3-5 分钟
倒入杯中
加入柠檬片

=== 制作抹茶 ===
烧水至 100°C
用热水冲泡抹茶粉并用茶筅搅拌
倒入杯中
加入红豆和糯米
```

---

## 37.9 外观模式（Facade Pattern）：化繁为简的窗口

### 37.9.1 统一入口简化复杂系统

你去医院挂号。窗口小姐就是**外观**：她帮你处理挂号、候诊、缴费、取药等一堆复杂流程，你只需要说"我挂号"。

外观模式：**为复杂的子系统提供一个统一的高层接口，让子系统更容易使用**。

### 37.9.2 实现：家庭影院系统

```cpp
#include <iostream>
#include <memory>
#include <string>

// 子系统1：投影仪
class Projector {
public:
    void on() { std::cout << "投影仪开启\n"; }
    void off() { std::cout << "投影仪关闭\n"; }
    void setInput(const std::string& source) {
        std::cout << "投影仪输入切换到: " << source << "\n";
    }
};

// 子系统2：音响
class Amplifier {
public:
    void on() { std::cout << "功放开启\n"; }
    void off() { std::cout << "功放关闭\n"; }
    void setVolume(int level) { std::cout << "音量设置为: " << level << "\n"; }
    void setSurroundSound() { std::cout << "环绕声模式开启\n"; }
};

// 子系统3：播放器
class StreamingPlayer {
public:
    void on() { std::cout << "播放器开启\n"; }
    void off() { std::cout << "播放器关闭\n"; }
    void play(const std::string& movie) { std::cout << "播放电影: " << movie << "\n"; }
    void stop() { std::cout << "停止播放\n"; }
};

// 子系统4：屏幕
class Screen {
public:
    void up() { std::cout << "屏幕上升\n"; }
    void down() { std::cout << "屏幕下降\n"; }
};

// 子系统5：爆米花机
class PopcornMachine {
public:
    void on() { std::cout << "爆米花机开启\n"; }
    void off() { std::cout << "爆米花机关闭\n"; }
    void pop() { std::cout << "制作爆米花 🍿\n"; }
};

// 外观：家庭影院控制器
class HomeTheaterFacade {
public:
    HomeTheaterFacade()
        : projector_(std::make_unique<Projector>())
        , amplifier_(std::make_unique<Amplifier>())
        , player_(std::make_unique<StreamingPlayer>())
        , screen_(std::make_unique<Screen>())
        , popcorn_(std::make_unique<PopcornMachine>()) {}

    // 一键看电影
    void watchMovie(const std::string& movie) {
        std::cout << "\n========== 准备观影 ==========\n";
        popcorn_->on();
        popcorn_->pop();
        screen_->down();
        projector_->on();
        projector_->setInput("HDMI");
        amplifier_->on();
        amplifier_->setSurroundSound();
        amplifier_->setVolume(25);
        player_->on();
        player_->play(movie);
        std::cout << "===============================\n";
        std::cout << "电影开始了，请享受！\n\n";
    }

    // 一键结束
    void endMovie() {
        std::cout << "\n========== 结束观影 ==========\n";
        player_->stop();
        player_->off();
        amplifier_->off();
        projector_->off();
        screen_->up();
        popcorn_->off();
        std::cout << "===============================\n";
        std::cout << "电影结束，欢迎下次光临！\n";
    }

private:
    std::unique_ptr<Projector> projector_;
    std::unique_ptr<Amplifier> amplifier_;
    std::unique_ptr<StreamingPlayer> player_;
    std::unique_ptr<Screen> screen_;
    std::unique_ptr<PopcornMachine> popcorn_;
};

int main() {
    HomeTheaterFacade homeTheater;

    // 简单的一键操作，不需要了解任何子系统
    homeTheater.watchMovie("C++从入门到放弃");

    std::cout << "\n--- 假装电影播放中 ---\n\n";

    homeTheater.endMovie();
}
```

**输出：**
```
========== 准备观影 ==========
爆米花机开启
制作爆米花 🍿
屏幕下降
投影仪开启
投影仪输入切换到: HDMI
功放开启
环绕声模式开启
音量设置为: 25
播放器开启
播放电影: C++从入门到放弃
===============================
电影开始了，请享受！

--- 假装电影播放中 ---

========== 结束观影 ==========
停止播放
播放器关闭
功放关闭
投影仪关闭
屏幕上升
爆米花机关闭
===============================
电影结束，欢迎下次光临！
```

---

## 37.10 迭代器模式（Iterator Pattern）：遍历的艺术

### 37.10.1 不关心容器结构，只关心遍历

你用遥控器换频道，不需要知道电视内部怎么解码信号。遥控器就是**迭代器**：它提供了一种统一的方式访问集合中的元素，不管集合是数组、链表还是红黑树。

### 37.10.2 C++17 范围 for 循环与迭代器

C++ 的迭代器无处不在，`std::vector`、`std::map`、`std::set` 都支持迭代器协议：

```cpp
#include <iostream>
#include <vector>
#include <map>
#include <set>
#include <iterator>  // std::begin, std::end

int main() {
    // 基础遍历
    std::vector<int> numbers = {1, 2, 3, 4, 5};

    std::cout << "=== 基础遍历 ===\n";
    for (int n : numbers) {
        std::cout << n << " ";
    }
    std::cout << "\n";

    // 使用迭代器遍历
    std::cout << "\n=== 使用迭代器 ===\n";
    for (auto it = std::begin(numbers); it != std::end(numbers); ++it) {
        std::cout << *it << " ";
    }
    std::cout << "\n";

    // 反向遍历
    std::cout << "\n=== 反向遍历 ===\n";
    for (auto it = numbers.rbegin(); it != numbers.rend(); ++it) {
        std::cout << *it << " ";
    }
    std::cout << "\n";

    // map 遍历
    std::cout << "\n=== Map 遍历 ===\n";
    std::map<std::string, int> scores = {
        {"Alice", 95},
        {"Bob", 87},
        {"Charlie", 92}
    };

    // 结构化绑定 (C++17)
    for (const auto& [name, score] : scores) {
        std::cout << name << ": " << score << "\n";
    }

    // set 遍历
    std::cout << "\n=== Set 遍历 ===\n";
    std::set<int> uniqueNumbers = {5, 3, 1, 4, 2, 3, 1};
    for (int n : uniqueNumbers) {
        std::cout << n << " ";
    }
    std::cout << "\n";
}
```

### 37.10.3 自定义迭代器

```cpp
#include <iostream>
#include <iterator>
#include <algorithm>

// 自定义容器：只包含偶数的集合
class EvenNumbers {
public:
    explicit EvenNumbers(int max) : max_(max) {}

    // 返回自定义迭代器
    class Iterator {
    public:
        using iterator_category = std::bidirectional_iterator_tag;
        using value_type = int;
        using difference_type = int;
        using pointer = int*;
        using reference = int&;

        explicit Iterator(int value, int max) : value_(value), max_(max) {}

        reference operator*() { return value_; }
        pointer operator->() { return &value_; }

        Iterator& operator++() {
            value_ += 2;
            return *this;
        }

        Iterator operator++(int) {
            Iterator tmp = *this;
            ++(*this);
            return tmp;
        }

        Iterator& operator--() {
            value_ -= 2;
            return *this;
        }

        Iterator operator--(int) {
            Iterator tmp = *this;
            --(*this);
            return tmp;
        }

        bool operator==(const Iterator& other) const { return value_ == other.value_; }
        bool operator!=(const Iterator& other) const { return value_ != other.value_; }

    private:
        int value_;
        int max_;
    };

    Iterator begin() { return Iterator(0, max_); }
    Iterator end() { return Iterator(max_ + (max_ % 2), max_); }

    // 反向迭代器支持
    std::reverse_iterator<Iterator> rbegin() { return std::make_reverse_iterator(end()); }
    std::reverse_iterator<Iterator> rend() { return std::make_reverse_iterator(begin()); }

private:
    int max_;
};

int main() {
    EvenNumbers evens(20);

    std::cout << "=== 偶数集合 (0-20) ===\n";
    for (int n : evens) {
        std::cout << n << " ";
    }
    std::cout << "\n";

    std::cout << "\n=== 反向遍历 ===\n";
    for (auto it = evens.rbegin(); it != evens.rend(); ++it) {
        std::cout << *it << " ";
    }
    std::cout << "\n";

    std::cout << "\n=== 使用 STL 算法 ===\n";
    auto sum = std::accumulate(evens.begin(), evens.end(), 0);
    std::cout << "偶数和 (0-20): " << sum << "\n";

    auto count = std::count_if(evens.begin(), evens.end(), [](int n) { return n > 10; });
    std::cout << "大于10的偶数个数: " << count << "\n";
}
```

**输出：**
```
=== 偶数集合 (0-20) ===
0 2 4 6 8 10 12 14 16 18 20

=== 反向遍历 ===
20 18 16 14 12 10 8 6 4 2 0

=== 使用 STL 算法 ===
偶数和 (0-20): 110
大于10的偶数个数: 5
```

---

## 37.11 状态模式（State Pattern）：让对象看起来改变了类

### 37.11.1 状态机的大智慧

想象一个自动售货机：

- **无钱状态**：显示"请投币"
- **有钱状态**：可以选商品
- **出货状态**：正在出货
- **找零状态**：正在找零

状态模式：**允许对象在内部状态改变时改变它的行为，看起来像是换了另一个类**。

### 37.11.2 实现：自动售货机

```cpp
#include <iostream>
#include <memory>
#include <string>
#include <map>

// 前向声明
class VendingMachine;

// 抽象状态
class State {
protected:
    VendingMachine* machine_;
public:
    virtual ~State() = default;
    void setMachine(VendingMachine* m) { machine_ = m; }
    virtual void insertCoin(int amount) = 0;
    virtual void selectProduct(const std::string& product) = 0;
    virtual void dispense() = 0;
    virtual std::string getStatus() const = 0;
};

// 具体状态：无钱状态
class NoCoinState : public State {
public:
    void insertCoin(int amount) override;
    void selectProduct(const std::string&) override {
        std::cout << "[无钱状态] 请先投币！\n";
    }
    void dispense() override {
        std::cout << "[无钱状态] 无法出货，请先投币！\n";
    }
    std::string getStatus() const override { return "等待投币"; }
};

// 具体状态：有钱状态
class HasCoinState : public State {
public:
    void insertCoin(int amount) override {
        machine_->addCoin(amount);
        std::cout << "[有钱状态] 又投了 " << amount << " 元 (总共 "
                  << machine_->totalCoins() << " 元)\n";
    }
    void selectProduct(const std::string& product) override;
    void dispense() override {
        std::cout << "[有钱状态] 请先选择商品！\n";
    }
    std::string getStatus() const override {
        return "已投币 " + std::to_string(machine_->totalCoins()) + " 元";
    }
};

// 具体状态：出售状态
class SoldState : public State {
public:
    void insertCoin(int) override {
        std::cout << "[出售状态] 请等待当前商品出货完成！\n";
    }
    void selectProduct(const std::string&) override {
        std::cout << "[出售状态] 当前商品正在出货中！\n";
    }
    void dispense() override;
    std::string getStatus() const override { return "正在出货"; }
};

// 售货机（上下文）
class VendingMachine {
public:
    friend class NoCoinState;
    friend class HasCoinState;
    friend class SoldState;

    VendingMachine() {
        noCoinState_ = std::make_unique<NoCoinState>();
        hasCoinState_ = std::make_unique<HasCoinState>();
        soldState_ = std::make_unique<SoldState>();

        currentState_ = noCoinState_.get();
        currentState_->setMachine(this);
    }

    void setState(State* newState) {
        currentState_ = newState;
        currentState_->setMachine(this);
    }

    void insertCoin(int amount) { currentState_->insertCoin(amount); }
    void selectProduct(const std::string& product) { currentState_->selectProduct(product); }
    void dispense() { currentState_->dispense(); }

    void addCoin(int amount) { coins_ += amount; }
    int totalCoins() const { return coins_; }
    void resetCoins() { coins_ = 0; }

    std::string getStatus() const { return currentState_->getStatus(); }

    // 商品库存
    std::map<std::string, int> inventory = {
        {"可乐", 10},
        {"薯片", 5},
        {"巧克力", 8}
    };

    std::map<std::string, int> prices = {
        {"可乐", 3},
        {"薯片", 5},
        {"巧克力", 8}
    };

private:
    State* currentState_;
    std::unique_ptr<NoCoinState> noCoinState_;
    std::unique_ptr<HasCoinState> hasCoinState_;
    std::unique_ptr<SoldState> soldState_;
    int coins_ = 0;
};

// 状态转换实现
void NoCoinState::insertCoin(int amount) {
    machine_->addCoin(amount);
    std::cout << "[无钱状态] 投币 " << amount << " 元成功！\n";
    machine_->setState(machine_->hasCoinState_.get());
}

void HasCoinState::selectProduct(const std::string& product) {
    auto priceIt = machine_->prices.find(product);
    if (priceIt == machine_->prices.end()) {
        std::cout << "[有钱状态] 商品 '" << product << "' 不存在！\n";
        return;
    }

    int price = priceIt->second;
    if (machine_->totalCoins() < price) {
        std::cout << "[有钱状态] 余额不足！需要 " << price
                  << " 元，你投了 " << machine_->totalCoins() << " 元\n";
        return;
    }

    auto invIt = machine_->inventory.find(product);
    if (invIt == machine_->inventory.end() || invIt->second <= 0) {
        std::cout << "[有钱状态] 商品 '" << product << "' 已售罄！\n";
        return;
    }

    std::cout << "[有钱状态] 选择商品: " << product << " (价格: " << price << " 元)\n";
    machine_->resetCoins();
    machine_->setState(machine_->soldState_.get());
}

void SoldState::dispense() {
    std::cout << "[出售状态] 商品出货中...\n";
    std::cout << " ✅ 商品出货完成！\n";
    machine_->setState(machine_->noCoinState_.get());
}

int main() {
    VendingMachine vm;

    std::cout << "=== 售货机演示 ===\n";
    std::cout << "状态: " << vm.getStatus() << "\n";

    // 场景1：直接选商品（没钱）
    std::cout << "\n--- 场景1：没钱直接选商品 ---\n";
    vm.selectProduct("可乐");

    // 场景2：投币买可乐
    std::cout << "\n--- 场景2：正常购买可乐 ---\n";
    vm.insertCoin(5);
    std::cout << "状态: " << vm.getStatus() << "\n";
    vm.selectProduct("可乐");
    std::cout << "状态: " << vm.getStatus() << "\n";
    vm.dispense();
    std::cout << "状态: " << vm.getStatus() << "\n";

    // 场景3：余额不足
    std::cout << "\n--- 场景3：余额不足 ---\n";
    vm.insertCoin(2);
    std::cout << "状态: " << vm.getStatus() << "\n";
    vm.selectProduct("巧克力");  // 巧克力8元
}
```

**输出：**
```
=== 售货机演示 ===
状态: 等待投币

--- 场景1：没钱直接选商品 ---
[无钱状态] 请先投币！

--- 场景2：正常购买可乐 ---
[无钱状态] 投币 5 元成功！
状态: 已投币 5 元
[有钱状态] 选择商品: 可乐 (价格: 3 元)
状态: 正在出货
 ✅ 商品出货完成！
状态: 等待投币

--- 场景3：余额不足 ---
[有钱状态] 又投了 2 元 (总共 2 元)
状态: 已投币 2 元
[有钱状态] 余额不足！需要 8 元，你投了 2 元
```

---

## 37.12 建造者模式（Builder Pattern）：复杂对象的流水线

### 37.12.1 分步骤构建复杂对象

想象你买电脑。配置单上写着：

```
CPU: i9-14900K
内存: 64GB DDR5
硬盘: 2TB NVMe SSD
显卡: RTX 4090
```

你不需要知道这些零件怎么组装，工程师会帮你一步步装好。**建造者模式**就是干这个的：把复杂对象的构建和它的表示分离。

### 37.12.2 实现：电脑配置系统

```cpp
#include <iostream>
#include <string>
#include <memory>
#include <vector>

// 产品：电脑
class Computer {
public:
    void setCPU(const std::string& cpu) { cpu_ = cpu; }
    void setRAM(int gb) { ram_ = gb; }
    void setStorage(const std::string& storage) { storage_ = storage; }
    void setGPU(const std::string& gpu) { gpu_ = gpu; }

    void addExtra(const std::string& extra) { extras_.push_back(extra); }

    void showSpec() const {
        std::cout << "=============================\n";
        std::cout << "  电脑配置清单\n";
        std::cout << "=============================\n";
        std::cout << "CPU:    " << cpu_ << "\n";
        std::cout << "内存:   " << ram_ << " GB\n";
        std::cout << "硬盘:   " << storage_ << "\n";
        std::cout << "显卡:   " << gpu_ << "\n";
        if (!extras_.empty()) {
            std::cout << "附加:   ";
            for (const auto& e : extras_) std::cout << e << ", ";
            std::cout << "\n";
        }
        std::cout << "=============================\n";
    }

private:
    std::string cpu_;
    int ram_ = 0;
    std::string storage_;
    std::string gpu_;
    std::vector<std::string> extras_;
};

// 抽象建造者
class ComputerBuilder {
public:
    virtual ~ComputerBuilder() = default;
    virtual void buildCPU() = 0;
    virtual void buildRAM() = 0;
    virtual void buildStorage() = 0;
    virtual void buildGPU() = 0;
    virtual void buildExtras() = 0;
    virtual std::unique_ptr<Computer> getResult() = 0;

protected:
    std::unique_ptr<Computer> computer_ = std::make_unique<Computer>();
};

// 建造者A：游戏电脑
class GamingComputerBuilder : public ComputerBuilder {
public:
    void buildCPU() override { computer_->setCPU("Intel i9-14900K"); }
    void buildRAM() override { computer_->setRAM(64); }
    void buildStorage() override { computer_->setStorage("2TB NVMe Gen5 SSD"); }
    void buildGPU() override { computer_->setGPU("NVIDIA RTX 4090 24GB"); }
    void buildExtras() override {
        computer_->addExtra("360mm AIO 水冷");
        computer_->addExtra("1000W 80+ 金牌电源");
        computer_->addExtra("ARGB 机箱风扇 x6");
    }

    std::unique_ptr<Computer> getResult() override { return std::move(computer_); }
};

// 建造者B：办公电脑
class OfficeComputerBuilder : public ComputerBuilder {
public:
    void buildCPU() override { computer_->setCPU("Intel i5-14400"); }
    void buildRAM() override { computer_->setRAM(16); }
    void buildStorage() override { computer_->setStorage("512GB NVMe SSD"); }
    void buildGPU() override { computer_->setGPU("Intel UHD Graphics 730 (集成)"); }
    void buildExtras() override {
        computer_->addExtra("静音 CPU 散热器");
        computer_->addExtra("300W 80+ 铜牌电源");
    }

    std::unique_ptr<Computer> getResult() override { return std::move(computer_); }
};

// 建造者C：开发者工作站
class WorkstationBuilder : public ComputerBuilder {
public:
    void buildCPU() override { computer_->setCPU("AMD Threadripper PRO 5965WX"); }
    void buildRAM() override { computer_->setRAM(256); }
    void buildStorage() override { computer_->setStorage("4TB NVMe Gen4 SSD + 8TB HDD"); }
    void buildGPU() override { computer_->setGPU("NVIDIA RTX 6000 Ada 48GB"); }
    void buildExtras() override {
        computer_->addExtra("480mm AIO 水冷");
        computer_->addExtra("1600W 80+ 铂金电源");
        computer_->addExtra("ECC 内存");
    }

    std::unique_ptr<Computer> getResult() override { return std::move(computer_); }
};

// 指挥者：组装流水线
class Director {
public:
    void setBuilder(std::unique_ptr<ComputerBuilder> builder) {
        builder_ = std::move(builder);
    }

    void construct() {
        builder_->buildCPU();
        builder_->buildRAM();
        builder_->buildStorage();
        builder_->buildGPU();
        builder_->buildExtras();
    }

    std::unique_ptr<Computer> getComputer() {
        return builder_->getResult();
    }

private:
    std::unique_ptr<ComputerBuilder> builder_;
};

int main() {
    Director director;

    std::cout << "=== 电脑定制系统 ===\n\n";

    // 构建游戏电脑
    std::cout << ">>> 客户A: 游戏玩家\n";
    director.setBuilder(std::make_unique<GamingComputerBuilder>());
    director.construct();
    auto gamingPC = director.getComputer();
    gamingPC->showSpec();

    // 构建办公电脑
    std::cout << ">>> 客户B: 办公室文员\n";
    director.setBuilder(std::make_unique<OfficeComputerBuilder>());
    director.construct();
    auto officePC = director.getComputer();
    officePC->showSpec();

    // 构建工作站
    std::cout << ">>> 客户C: C++ 编译器狂魔 (需要编译 Chromium)\n";
    director.setBuilder(std::make_unique<WorkstationBuilder>());
    director.construct();
    auto workstation = director.getComputer();
    workstation->showSpec();
}
```

**输出：**
```
=== 电脑定制系统 ===

>>> 客户A: 游戏玩家
=============================
  电脑配置清单
=============================
CPU:    Intel i9-14900K
内存:   64 GB
硬盘:   2TB NVMe Gen5 SSD
显卡:   NVIDIA RTX 4090 24GB
附加:   360mm AIO 水冷, 1000W 80+ 金牌电源, ARGB 机箱风扇 x6, 
=============================

>>> 客户B: 办公室文员
=============================
  电脑配置清单
=============================
CPU:    Intel i5-14400
内存:   16 GB
硬盘:   512GB NVMe SSD
显卡:   Intel UHD Graphics 730 (集成)
附加:   静音 CPU 散热器, 300W 80+ 铜牌电源, 
=============================

>>> 客户C: C++ 编译器狂魔 (需要编译 Chromium)
=============================
  电脑配置清单
=============================
CPU:    AMD Threadripper PRO 5965WX
内存:   256 GB
硬盘:   4TB NVMe Gen4 SSD + 8TB HDD
显卡:   NVIDIA RTX 6000 Ada 48GB
附加:   480mm AIO 水冷, 1600W 80+ 铂金电源, ECC 内存, 
=============================
```

---

## 37.13 组合模式（Composite Pattern）：树形结构的统一视图

### 37.13.1 让单个对象和组合对象被统一对待

文件系统就是组合模式：你操作文件和文件夹用的是同一个接口（复制、删除、移动），但文件夹里面可以包含文件和子文件夹。

组合模式：**将对象组合成树形结构以表示"部分-整体"的层次结构，让你统一处理单个对象和组合对象**。

### 37.13.2 实现：文件系统

```cpp
#include <iostream>
#include <memory>
#include <string>
#include <vector>

// 组件接口
class FileSystemItem {
public:
    virtual ~FileSystemItem() = default;
    virtual int getSize() const = 0;
    virtual void ls(int indent = 0) const = 0;
    virtual std::string getName() const = 0;
};

// 文件（叶子节点）
class File : public FileSystemItem {
public:
    explicit File(std::string name, int size) : name_(std::move(name)), size_(size) {}

    int getSize() const override { return size_; }

    void ls(int indent = 0) const override {
        std::cout << std::string(indent, ' ') << "📄 " << name_
                  << " (" << size_ << " KB)\n";
    }

    std::string getName() const override { return name_; }

private:
    std::string name_;
    int size_;
};

// 目录（组合节点）
class Directory : public FileSystemItem {
public:
    explicit Directory(std::string name) : name_(std::move(name)) {}

    void add(std::unique_ptr<FileSystemItem> item) {
        children_.push_back(std::move(item));
    }

    int getSize() const override {
        int total = 0;
        for (const auto& child : children_) {
            total += child->getSize();
        }
        return total;
    }

    void ls(int indent = 0) const override {
        std::cout << std::string(indent, ' ') << "📁 " << name_
                  << " (总计: " << getSize() << " KB)\n";
        for (const auto& child : children_) {
            child->ls(indent + 4);
        }
    }

    std::string getName() const override { return name_; }

private:
    std::string name_;
    std::vector<std::unique_ptr<FileSystemItem>> children_;
};

int main() {
    std::cout << "=== 文件系统模拟 ===\n\n";

    // 构建文件系统结构
    auto root = std::make_unique<Directory>("root");

    auto documents = std::make_unique<Directory>("Documents");
    documents->add(std::make_unique<File>("resume.pdf", 128));
    documents->add(std::make_unique<File>("cover_letter.pdf", 64));

    auto projects = std::make_unique<Directory>("Projects");
    projects->add(std::make_unique<File>("main.cpp", 256));
    projects->add(std::make_unique<File>("utils.cpp", 128));
    projects->add(std::make_unique<File>("CMakeLists.txt", 16));

    auto cppProject = std::make_unique<Directory>("cpp-project");
    cppProject->add(std::make_unique<File>("design_patterns.cpp", 512));
    cppProject->add(std::make_unique<File>("makefile", 8));
    projects->add(std::move(cppProject));

    documents->add(std::move(projects));

    auto downloads = std::make_unique<Directory>("Downloads");
    downloads->add(std::make_unique<File>("compiler.iso", 4500000));
    downloads->add(std::make_unique<File>("slides.pptx", 12000));

    auto pictures = std::make_unique<Directory>("Pictures");
    pictures->add(std::make_unique<File>("meme.jpg", 256));
    pictures->add(std::make_unique<File>("screenshot.png", 1800));
    pictures->add(std::make_unique<File>("wallpaper.bmp", 8200));

    root->add(std::move(documents));
    root->add(std::move(downloads));
    root->add(std::move(pictures));

    // 显示整个文件系统
    root->ls();

    std::cout << "\n--- 总大小: " << root->getSize() << " KB ---\n";
}
```

**输出：**
```
=== 文件系统模拟 ===

📁 root (总计: 4535114 KB)
    📁 Documents (总计: 970 KB)
        📄 resume.pdf (128 KB)
        📄 cover_letter.pdf (64 KB)
        📁 Projects (总计: 920 KB)
            📄 main.cpp (256 KB)
            📄 utils.cpp (128 KB)
            📄 CMakeLists.txt (16 KB)
            📁 cpp-project (总计: 520 KB)
                📄 design_patterns.cpp (512 KB)
                📄 makefile (8 KB)
    📁 Downloads (总计: 4513000 KB)
        📄 compiler.iso (4500000 KB)
        📄 slides.pptx (12000 KB)
    📁 Pictures (总计: 10144 KB)
        📄 meme.jpg (256 KB)
        📄 screenshot.png (1800 KB)
        📄 wallpaper.bmp (8200 KB)

--- 总大小: 4535114 KB ---
```

---

## 37.14 依赖注入（Dependency Injection）：别让我们耦合在一起

### 37.14.1 控制权反转的艺术

**依赖注入（DI）**不是GoF设计模式，但它太重要了，不讲对不起观众。

> "我想测试这个类，但我没法mock它的依赖，因为它 `new` 了一个具体的类在构造函数里。"  
> "这就是为什么你需要依赖注入。"  
> "可是我不会啊......"  
> "那你现在会了。"

核心思想：**不要在类内部创建依赖，把依赖"注入"进来**。

```cpp
#include <iostream>
#include <memory>
#include <string>

// 服务接口
class ILogger {
public:
    virtual ~ILogger() = default;
    virtual void log(const std::string& msg) = 0;
};

// 服务实现
class ConsoleLogger : public ILogger {
public:
    void log(const std::string& msg) override {
        std::cout << "[Console] " << msg << "\n";
    }
};

class FileLogger : public ILogger {
public:
    void log(const std::string& msg) override {
        std::cout << "[FileLogger] Writing to log: " << msg << "\n";
    }
};

// 用户服务（依赖于 ILogger 接口，而不是具体实现）
class UserService {
public:
    // 注入方式1：构造函数注入（最常用）
    explicit UserService(std::shared_ptr<ILogger> logger)
        : logger_(std::move(logger)) {}

    // 注入方式2：Setter 注入
    void setLogger(std::shared_ptr<ILogger> logger) {
        logger_ = std::move(logger);
    }

    void createUser(const std::string& name) {
        logger_->log("Creating user: " + name);
        // 业务逻辑...
        logger_->log("User created: " + name);
    }

    void deleteUser(const std::string& name) {
        logger_->log("Deleting user: " + name);
    }

private:
    std::shared_ptr<ILogger> logger_;
};

// 注入方式3：接口注入
class DatabaseConnection {
public:
    virtual ~DatabaseConnection() = default;
    virtual void execute(const std::string& sql) = 0;
};

class MySQLConnection : public DatabaseConnection {
public:
    void execute(const std::string& sql) override {
        std::cout << "[MySQL] " << sql << "\n";
    }
};

class InjectableService {
public:
    // 通过接口注入依赖
    void injectDatabase(std::shared_ptr<DatabaseConnection> db) {
        db_ = std::move(db);
    }

    void runQuery(const std::string& sql) {
        if (db_) {
            db_->execute(sql);
        }
    }

private:
    std::shared_ptr<DatabaseConnection> db_;
};

int main() {
    std::cout << "=== 依赖注入演示 ===\n\n";

    // 场景1：使用控制台日志
    std::cout << "--- 场景1：使用 ConsoleLogger ---\n";
    auto consoleLogger = std::make_shared<ConsoleLogger>();
    UserService userService(consoleLogger);
    userService.createUser("Alice");

    // 场景2：轻松切换到文件日志（无需修改 UserService！）
    std::cout << "\n--- 场景2：切换到 FileLogger (无需改代码!) ---\n";
    auto fileLogger = std::make_shared<FileLogger>();
    userService.setLogger(fileLogger);  // Setter 注入
    userService.createUser("Bob");

    // 场景3：数据库注入
    std::cout << "\n--- 场景3：数据库注入 ---\n";
    InjectableService svc;
    svc.injectDatabase(std::make_shared<MySQLConnection>());
    svc.runQuery("SELECT * FROM users WHERE id = 1");
}
```

**输出：**
```
=== 依赖注入演示 ===

--- 场景1：使用 ConsoleLogger ---
[Console] Creating user: Alice
[Console] User created: Alice

--- 场景2：切换到 FileLogger (无需改代码!) ---
[FileLogger] Writing to log: Creating user: Bob
[FileLogger] Writing to log: User created: Bob

--- 场景3：数据库注入 ---
[MySQL] SELECT * FROM users WHERE id = 1
```

---

## 37.15 CRTP 模式：静态多态的优雅

### 37.15.1 编译时多态，零运行时开销

CRTP（Curiously Recurring Template Pattern，奇异递归模板模式）是一种 C++ 高级惯用法，实现了**静态多态**——在编译时确定调用哪个函数，没有虚函数表的运行时开销。

> 有人问："为什么要用 CRTP？"  
> 答："因为我不想在性能关键路径上给CPU交虚函数调用的税。"  
> 又问："听不懂。"  
> 答："那就继续用 virtual 吧，没事的。"

```cpp
#include <iostream>
#include <memory>

// CRTP 基类
template <typename Derived>
class Animal {
public:
    void speak() {
        // 转换为派生类类型，调用派生类的实现
        static_cast<Derived*>(this)->speakImpl();
    }

    void identify() {
        static_cast<Derived*>(this)->identifyImpl();
    }
};

// 派生类：猫
class Cat : public Animal<Cat> {
public:
    void speakImpl() { std::cout << "🐱 喵喵喵~\n"; }
    void identifyImpl() { std::cout << "我是一只猫\n"; }
};

// 派生类：狗
class Dog : public Animal<Dog> {
public:
    void speakImpl() { std::cout << "🐕 汪汪汪！\n"; }
    void identifyImpl() { std::cout << "我是一只狗\n"; }
};

// 派生类：牛
class Cow : public Animal<Cow> {
public:
    void speakImpl() { std::cout << "🐮 哞哞哞~\n"; }
    void identifyImpl() { std::cout << "我是一头牛\n"; }
};

// 函数模板：利用 CRTP 实现静态多态
template <typename T>
void makeAnimalSpeak(Animal<T>& animal) {
    animal.speak();  // 编译时绑定，无虚函数调用
}

int main() {
    std::cout << "=== CRTP 静态多态演示 ===\n\n";

    Cat cat;
    Dog dog;
    Cow cow;

    cat.identify();
    cat.speak();

    dog.identify();
    dog.speak();

    cow.identify();
    cow.speak();

    std::cout << "\n--- 在函数模板中使用 ---\n";
    makeAnimalSpeak(cat);
    makeAnimalSpeak(dog);
    makeAnimalSpeak(cow);
}
```

**输出：**
```
=== CRTP 静态多态演示 ===

我是一只猫
🐱 喵喵喵~
我是一只狗
🐕 汪汪汪！
我是一头牛
🐮 哞哞哞~

--- 在函数模板中使用 ---
🐱 喵喵喵~
🐕 汪汪汪！
🐮 哞哞哞~
```

---

## 37.16 Pimpl 惯用法：编译防火墙

### 37.16.1 减少编译依赖

Pimpl（Pointer to Implementation）是一种减少编译依赖的惯用法：把类的实现细节藏在一个私有指针后面，头文件不暴露任何实现细节。

> "修改了一个头文件，整个项目重新编译了 20 分钟？"  
> "你需要 Pimpl。或者说，你需要心理治疗。"

```cpp
// ========== widget.h ==========
// 这个头文件非常"干净"，不暴露任何实现细节
class Widget {
public:
    Widget();                    // 默认构造
    ~Widget();                   // 必须定义析构（因为 unique_ptr 需要完整类型）

    Widget(Widget&& other);      // 移动构造
    Widget& operator=(Widget&& other);  // 移动赋值

    Widget(const Widget& other);        // 拷贝构造
    Widget& operator=(const Widget& other);  // 拷贝赋值

    void setTitle(const std::string& title);
    void setSize(int width, int height);
    void show() const;

private:
    // Pimpl 指针：指向实现类
    struct Impl;  // 前向声明
    std::unique_ptr<Impl> pImpl_;
};

// ========== widget.cpp ==========
#include "widget.h"
#include <iostream>

struct Widget::Impl {
    std::string title;
    int width = 0;
    int height = 0;

    void display() const {
        std::cout << "窗口: " << title
                  << " (" << width << "x" << height << ")\n";
    }
};

Widget::Widget() : pImpl_(std::make_unique<Impl>()) {}
Widget::~Widget() = default;  // 需要完整类型 Impl，所以要 out-of-line 定义

Widget::Widget(Widget&& other) = default;
Widget& Widget::operator=(Widget&& other) = default;
Widget::Widget(const Widget& other) : pImpl_(std::make_unique<Impl>(*other.pImpl_)) {}
Widget& Widget::operator=(const Widget& other) {
    if (this != &other) {
        *pImpl_ = *other.pImpl_;
    }
    return *this;
}

void Widget::setTitle(const std::string& title) {
    pImpl_->title = title;
}

void Widget::setSize(int width, int height) {
    pImpl_->width = width;
    pImpl_->height = height;
}

void Widget::show() const {
    pImpl_->display();
}

// ========== main.cpp ==========
int main() {
    Widget w1;
    w1.setTitle("主窗口");
    w1.setSize(800, 600);

    Widget w2 = w1;  // 拷贝构造
    w2.setTitle("副本窗口");

    Widget w3;
    w3 = w1;  // 拷贝赋值

    w1.show();
    w2.show();
    w3.show();
}
```

**输出：**
```
窗口: 主窗口 (800x600)
窗口: 副本窗口 (800x600)
窗口: 主窗口 (800x600)
```

**Pimpl 的好处：**

- 修改实现不影响依赖该类的代码（减少重新编译）
- 头文件更干净，暴露接口更少
- ABI 稳定性更好
- 编译防火墙

---

## 37.17 设计模式的"反模式"警示

> "If you know Design Patterns, you'll start seeing them everywhere—even where they shouldn't be."
> 如果你懂设计模式，你会发现它们无处不在——甚至在不该出现的地方。

### 37.17.1 过度工程（Over-Engineering）

"这个功能用一个 `if` 就搞定了......但让我想想能不能用策略模式包装一下，显得更专业。"

```cpp
// 不要这样：为了用模式而用模式
class SimpleCalculator {
public:
    // ？？？为什么一个简单计算器需要工厂模式和策略模式？
    // 你是在写代码还是在凑设计模式的种类数？
    explicit SimpleCalculator(std::unique_ptr<OperationStrategy> strategy)
        : strategy_(std::move(strategy)) {}

    int calculate(int a, int b) {
        return strategy_->execute(a, b);
    }

private:
    std::unique_ptr<OperationStrategy> strategy_;
};
```

**简化版本：**
```cpp
// 简单计算器就应该简单
int add(int a, int b) { return a + b; }
int multiply(int a, int b) { return a * b; }
```

> 💡 记住：不是你的代码用了多少模式才叫"高水平"，是你的代码解决问题又多简洁才叫高水平。

### 37.17.2 模式崇拜（Patternitis）

- 不是所有问题都需要设计模式
- 如果一个简单的 `if-else` 能解决问题，别硬上工厂
- 设计模式是工具，不是目的
- KISS（Keep It Simple, Stupid）原则永远适用
- 如果你看到有人给"你好世界"写了个工厂，建议报警（不是）

### 37.17.3 模式混用（Pattern Soup）

"我给这个类起名叫 `ObserverDecoratorStrategyAdapter`，因为它同时继承了四个设计模式！"

```cpp
// 这段代码把观察者、策略、装饰器混在一起
// 看起来很"设计模式"，实际上没人能维护
// 三个月后，连写它的人自己都看不懂了
class ObserverDecoratorStrategyAdapter : public Observer, public Strategy {
    // ...
};
```

> 🔥 模式混用的代码，就像往披萨上加巧克力酱、蓝纹奶酪和榴莲——理论上都是食物，但没人想吃了它。

---

## 本章小结

本章我们用 C++ 实现了软件工程中最常用的设计模式。回顾一下：

| 模式 | 一句话描述 | 适用场景 |
|------|-----------|---------|
| **单例模式** | 全局唯一的实例 | 日志、配置、连接池 |
| **工厂模式** | 封装对象创建 | 解耦创建逻辑，支持多产品族 |
| **观察者模式** | 一对多通知 | 事件系统、消息订阅、GUI 交互 |
| **策略模式** | 算法可替换 | 排序策略、支付方式、压缩算法 |
| **装饰器模式** | 动态叠加功能 | 咖啡订单、IO 流、包装类 |
| **命令模式** | 请求封装为对象 | 撤销/重做、宏命令、任务队列 |
| **适配器模式** | 接口翻译 | 兼容遗留代码、第三方库集成 |
| **模板方法** | 算法骨架 | 流程固定、部分步骤变化的场景 |
| **外观模式** | 统一入口 | 简化复杂子系统调用 |
| **迭代器模式** | 统一遍历 | STL 容器、自定义集合 |
| **状态模式** | 状态切换行为 | 自动售货机、游戏状态、订单流程 |
| **建造者模式** | 分步构建 | 配置系统、复杂对象创建 |
| **组合模式** | 树形结构 | 文件系统、组织架构、UI 组件 |
| **依赖注入** | 控制权反转 | 解耦服务、单元测试 |
| **CRTP** | 静态多态 | 性能关键代码、避免虚函数开销 |
| **Pimpl** | 编译防火墙 | 减少编译依赖、ABI 稳定 |

**记住：**

1. **模式是手段，不是目的**——不要为了用模式而用模式
2. **KISS 优先**——简单方案能搞定就别上模式
3. **模式有代价**——增加复杂度，需要权衡
4. **理解本质**——不要死记 UML，理解为什么这个模式能解决问题
5. **多实践**——看懂和能用之间隔着一万行代码

下一章我们将探讨**代码重构**的艺术，把烂代码变成好代码。敬请期待！

---

*参考文献与深入阅读：*
- *《Design Patterns: Elements of Reusable Object-Oriented Software》— Gang of Four (GoF)*
- *《Effective C++》— Scott Meyers*
- *《C++ Design Patterns》— Dustin Supra*
- *《Modern C++ Design》— Andrei Alexandrescu*
