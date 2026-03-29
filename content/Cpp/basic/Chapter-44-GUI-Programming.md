+++
title = "第44章 GUI编程：让C++穿上漂亮的外衣"
weight = 440
date = "2026-03-29T21:03:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++
# 第44章 GUI编程：让C++穿上漂亮的外衣

## 44.1 GUI编程前世今生：从命令行到图形界面

### 那些年我们追过的命令行

想象一下1980年代的程序员：他们面对的是一个黑漆漆的屏幕，上面只有绿色的字符在闪烁。没有按钮可以点，没有窗口可以拖拽，一切都靠键盘敲命令。那个时候的程序员，大概做梦都在背命令参数吧。

```bash
# 1970年代的经典操作
$ format a:
# 你以为格式化磁盘很容易？先记住参数顺序再说！

$ del *.* /s /q /f
# 这个命令下去，同事三年的论文没了
```

直到1984年，**Macintosh**推出了第一台大众化的图形界面电脑，1985年**Windows 1.0**问世（虽然丑得像个草稿），1986年**X Window System**让Unix也有了GUI——程序员们终于可以不用再死记硬背那些奇怪的命令了。

### GUI编程的本质：事件驱动

GUI程序和命令行程序最大的区别在于：**谁说了算**。

- **命令行程序**：你掌控一切，程序按照你的逻辑顺序执行
- **GUI程序**：用户掌控一切，程序像个乖巧的服务员，等待用户的每一个动作

这种编程范式叫做**事件驱动编程（Event-Driven Programming）**。用户点击按钮是一个事件，移动鼠标是一个事件，调整窗口大小也是一个事件。你的程序就是一台精密的事件处理机器：

```cpp
// 事件驱动伪代码
while (程序在运行) {
    事件 event = 等待下一个事件();  // 阻塞在这里，直到用户操作
    switch (event.type) {
        case 按钮被点击:
            处理按钮点击();
            break;
        case 窗口被关闭:
            清理资源并退出();
            break;
        case 滑块被拖动:
            更新显示数值();
            break;
        // ... 无数种可能的事件
    }
}
```

> 有人说事件驱动编程就像养猫：你不能命令猫做什么，你只能在猫做某件事的时候做出反应。GUI编程就是这样，你得对用户的每一个动作做出恰当的响应。

### C++在GUI领域的江湖地位

很多人以为C++只适合做"后台"、"底层"、"服务器"这类不见天日的工作。但实际上，C++在桌面GUI领域可是老牌劲旅：

| 框架名称 | 年龄 | 特色 | 适合场景 |
|---------|------|------|---------|
| **Qt** | 1991年生 | 跨平台最强、生态完整 | 商业软件、跨平台应用 |
| **wxWidgets** | 1992年生 | 原生外观、使用原生控件 | 需要原生look的应用 |
| **GTKmm** | 1998年生 | GNOME家族御用 | Linux桌面开发 |
| **FLTK** | 1998年生 | 轻量级、快速 | 小型工具、轻量级应用 |
| **Win32 API** | 1993年生 | Windows亲儿子 | Windows专属开发 |

本章我们将重点介绍**Qt**——因为它最成熟、最跨平台、生态最完善学会了Qt，走遍天下都不怕（夸张但不离谱）。

---

## 44.2 Qt框架：C++ GUI编程的瑞士军刀

### Qt是谁？凭什么这么火？

**Qt**（读作"cute"，不是"Q-t"）最初由挪威的Trolltech公司开发（1991年），后来经历了Nokia收购（2008年）、Digia收购（2012年），最终被Qt公司接管至今。它不仅仅是一个GUI框架，而是一个**全能型应用开发框架**。

Qt的口号大概是：**"一次编写，到处编译——而且看起来还挺像那么回事。"**

Qt的强项：
- ✅ 真正的跨平台（Windows、macOS、Linux、Android、iOS、WebAssembly）
- ✅ 信号与槽机制——优雅的事件处理
- ✅ 完整的工具链（Qt Designer可视化设计、Qt Creator IDE）
- ✅ 丰富的模块（网络、数据库、图形、音频……）
- ✅ 商业友好的许可证（GPL/LGPL/Commercial）

> 有趣的是，Qt最初被命名为"Qt"是因为Trolltech的工程师们觉得"OOP"（面向对象）和"X"（Unix）合起来很酷，但"OOX"听起来像个洗衣机。所以他们决定用"Qt"——既是"cute"的谐音，也暗示着比C++多了一个"+"。

### 信号与槽：Qt的灵魂所在

如果说C++的类是Qt的肉体，那**信号与槽（Signal & Slot）**就是Qt的灵魂。这个机制让对象之间的通信变得既类型安全又灵活多变。

**信号（Signal）**：当某个事情发生时，对象发出的"广播"
**槽（Slot）**：接收信号的"处理函数"

```cpp
#include <QCoreApplication>
#include <QDebug>
#include <QObject>

// 闹钟类：发出信号
class AlarmClock : public QObject {
    Q_OBJECT  // Qt元对象系统必备！没有这个，信号槽就是摆设
public:
    AlarmClock(QObject *parent = nullptr) : QObject(parent) {}

    // 触发闹铃的方法
    void ring() {
        qDebug() << "🔔 叮铃铃~ 该起床了！";
        emit alarmTriggered("早上好！已经7点了！");  // emit发出信号
    }

signals:  // signals部分声明的函数会自动生成元对象代码
    void alarmTriggered(const QString &message);  // 带参数的信号
};

// 起床服务类：接收信号并处理
class WakeUpService : public QObject {
    Q_OBJECT
public:
    WakeUpService(QObject *parent = nullptr) : QObject(parent) {}

public slots:  // slots部分声明的函数会响应信号
    void handleAlarm(const QString &message) {
        qDebug() << "😴 收到闹铃信号: " << message;
        qDebug() << "🤧 伸个懒腰，挣扎着起床...";
        qDebug() << "☕ 开始煮咖啡...";
    }
};

int main() {
    QCoreApplication app(argc, argv);

    AlarmClock clock;
    WakeUpService service;

    // 连接信号与槽：闹铃响 -> 触发起床服务
    QObject::connect(&clock, &AlarmClock::alarmTriggered,
                     &service, &WakeUpService::handleAlarm);

    qDebug() << "⏰ 设置闹铃，等待触发...";
    clock.ring();  // 触发信号

    return 0;
}
```

**信号与槽的高级玩法：**

```cpp
// 1. Lambda表达式作为槽（C++11+）
QPushButton *button = new QPushButton("点我");
connect(button, &QPushButton::clicked, []() {
    qDebug() << "Lambda槽：按钮被点击了！";
});

// 2. 一个信号连接多个槽（广播）
connect(button, &QPushButton::clicked, this, &MyClass::onButtonClicked);
connect(button, &QPushButton::clicked, this, &MyClass::updateUI);
connect(button, &QPushButton::clicked, []() { saveData(); });

// 3. 信号连接信号（链式）
connect(checkbox, &QCheckBox::toggled, button, &QPushButton::setEnabled);

// 4. 断开连接
QObject::disconnect(button, &QPushButton::clicked, nullptr, nullptr);
```

### 第一个Qt GUI程序

让我们写一个完整的、可以运行的Qt程序：

```cpp
#include <QApplication>
#include <QPushButton>
#include <QWidget>
#include <QVBoxLayout>
#include <QLabel>
#include <QSlider>
#include <QSpinBox>

int main(int argc, char *argv[]) {
    QApplication app(argc, argv);

    // 创建主窗口
    QWidget window;
    window.setWindowTitle("Hello Qt - 我的第一个GUI程序");
    window.setMinimumSize(400, 300);

    // 创建布局管理器
    QVBoxLayout *layout = new QVBoxLayout(&window);

    // 创建标签
    QLabel *label = new QLabel("Hello GUI World! 🌍");
    label->setAlignment(Qt::AlignCenter);
    label->setStyleSheet("font-size: 24px; color: #2c3e50; font-weight: bold;");
    layout->addWidget(label);

    // 创建按钮
    QPushButton *button = new QPushButton("点我! 🚀");
    button->setStyleSheet(R"(
        QPushButton {
            background-color: #3498db;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 12px 24px;
            font-size: 16px;
        }
        QPushButton:hover {
            background-color: #2980b9;
        }
        QPushButton:pressed {
            background-color: #1a5276;
        }
    )");
    layout->addWidget(button);

    // 创建数值选择器组合（滑块 + 数字输入）
    QSpinBox *spinBox = new QSpinBox();
    spinBox->setRange(0, 100);
    spinBox->setValue(50);
    spinBox->setPrefix("值: ");
    layout->addWidget(spinBox);

    QSlider *slider = new QSlider(Qt::Horizontal);
    slider->setRange(0, 100);
    slider->setValue(50);
    layout->addWidget(slider);

    // 信号槽连接：滑块和数字输入同步
    QObject::connect(slider, &QSlider::valueChanged, spinBox, &QSpinBox::setValue);
    QObject::connect(spinBox, QOverload<int>::of(&QSpinBox::valueChanged), slider, &QSlider::setValue);

    // 按钮点击事件
    int clickCount = 0;
    QObject::connect(button, &QPushButton::clicked, [&label, &clickCount]() {
        clickCount++;
        label->setText(QString("按钮被点击了 %1 次! 🎉").arg(clickCount));
    });

    // 显示窗口
    window.show();

    return app.exec();
}
```

**CMakeLists.txt配置：**

```cmake
cmake_minimum_required(VERSION 3.16)
project(HelloQt VERSION 1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_AUTOMOC ON)  # 自动处理元对象代码

find_package(Qt6 COMPONENTS Widgets REQUIRED)

add_executable(HelloQt main.cpp)
target_link_libraries(HelloQt PRIVATE Qt6::Widgets)
```

编译运行：
```bash
mkdir build && cd build
cmake .. -G Ninja
ninja
./HelloQt  # Linux/macOS
HelloQt.exe  # Windows
```

### Qt的布局管理系统

Qt提供了强大的布局管理器，让你的界面能够**自适应窗口大小变化**和**不同屏幕分辨率**。

```cpp
#include <QApplication>
#include <QWidget>
#include <QPushButton>
#include <QBoxLayout>
#include <QGridLayout>
#include <QLabel>
#include <QLineEdit>
#include <QTextEdit>

// 演示各种布局管理器的使用
class LayoutDemo : public QWidget {
    Q_OBJECT
public:
    LayoutDemo(QWidget *parent = nullptr) : QWidget(parent) {
        setWindowTitle("Qt布局管理器演示");

        // ==================== 垂直布局 ====================
        // QVBoxLayout：所有子部件垂直排列，像叠罗汉一样
        QVBoxLayout *vbox = new QVBoxLayout();
        vbox->addWidget(new QLabel("📌 垂直布局示例"));
        vbox->addWidget(new QPushButton("按钮1"));
        vbox->addWidget(new QPushButton("按钮2"));
        vbox->addWidget(new QPushButton("按钮3"));

        // 设置按钮的固定高度，展示stretch的作用
        // addStretch()在按钮之前添加一个可伸缩空间
        vbox->addStretch();  // 把按钮"挤"到上方
        vbox->addWidget(new QPushButton("永远在底部"));

        // ==================== 水平布局 ====================
        // QHBoxLayout：所有子部件水平排列
        QHBoxLayout *hbox = new QHBoxLayout();
        hbox->addWidget(new QLabel("用户名:"));
        hbox->addWidget(new QLineEdit());  // 单行输入框
        hbox->addWidget(new QPushButton("登录"));

        // ==================== 网格布局 ====================
        // QGridLayout：用表格形式排列部件
        QGridLayout *grid = new QGridLayout();
        grid->addWidget(new QLabel("计算器"), 0, 0, 1, 3);  // 行, 列, 行跨度, 列跨度

        QStringList buttonLabels = {"7", "8", "9", "/",
                                     "4", "5", "6", "*",
                                     "1", "2", "3", "-",
                                     "0", ".", "=", "+"};
        for (int i = 0; i < buttonLabels.size(); ++i) {
            int row = 1 + i / 4;
            int col = i % 4;
            QPushButton *btn = new QPushButton(buttonLabels[i]);
            btn->setFixedSize(50, 50);  // 固定按钮大小
            grid->addWidget(btn, row, col);
        }

        // ==================== 表单布局 ====================
        // QFormLayout：专门用于"标签-输入框"配对的布局
        QFormLayout *form = new QFormLayout();
        form->addRow("姓名:", new QLineEdit());
        form->addRow("邮箱:", new QLineEdit());
        form->addRow("电话:", new QLineEdit());
        form->addRow("备注:", new QTextEdit());  // 多行文本框

        // ==================== 嵌套布局 ====================
        // 将多个布局组合使用
        QVBoxLayout *mainLayout = new QVBoxLayout(this);
        mainLayout->addLayout(vbox);      // 嵌套垂直布局
        mainLayout->addLayout(hbox);      // 嵌套水平布局
        mainLayout->addLayout(grid);      // 嵌套网格布局
        mainLayout->addLayout(form);      // 嵌套表单布局

        // 设置窗口最小大小
        setMinimumSize(400, 600);
    }
};

int main(int argc, char *argv[]) {
    QApplication app(argc, argv);
    LayoutDemo window;
    window.show();
    return app.exec();
}
```

### Qt Designer：可视化界面设计

对于懒人（啊不对，是效率专家）来说，手写UI代码未免太累了。Qt提供了**Qt Designer**——一个所见即所得的界面设计工具。

使用方法：
```bash
# 在Qt Creator中：File -> New File or Project -> Qt -> Qt Designer Form
# 或者命令行启动
designer
```

Qt Designer生成的`.ui`文件是XML格式，可以被`uic`工具转换为C++代码，或者在运行时动态加载。

```xml
<!-- calculator.ui -->
<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>Calculator</class>
 <widget class="QWidget" name="Calculator">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>300</width>
    <height>400</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>计算器</string>
  </property>
  <widget class="QPushButton" name="btn0">
   <property name="geometry">
    <rect>
     <x>10</x>
     <y>310</y>
     <width>131</width>
     <height>41</height>
    </rect>
   </property>
   <property name="text">
    <string>0</string>
   </property>
  </widget>
  <!-- ... 更多控件 ... -->
 </widget>
 <resources/>
 <connections/>
</ui>
```

在代码中加载UI：
```cpp
#include <QUiLoader>
#include <QFile>

// 方法一：运行时加载UI文件
void loadUiFile(QWidget *parent) {
    QFile file(":/forms/calculator.ui");  // Qt资源系统路径
    file.open(QFile::ReadOnly);

    QUiLoader loader;
    QWidget *ui = loader.load(&file, parent);
    ui->show();
}

// 方法二：使用uic生成的代码
// 在CMakeLists.txt中添加：set(CMAKE_AUTORCC ON) set(CMAKE_AUTOUIC ON)
// 然后直接包含生成的头文件
// #include "ui_calculator.h"
// ui.setupUi(this);
```

---

## 44.3 常用Qt控件详解

### 按钮系列：QPushButton、QToolButton、QRadioButton、QCheckBox

按钮是GUI中最基本也最常用的控件。Qt提供了多种按钮类型：

```cpp
#include <QApplication>
#include <QWidget>
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QPushButton>
#include <QRadioButton>
#include <QCheckBox>
#include <QButtonGroup>
#include <QLabel>
#include <QMessageBox>

class ButtonDemo : public QWidget {
    Q_OBJECT
public:
    ButtonDemo(QWidget *parent = nullptr) : QWidget(parent) {
        setWindowTitle("按钮控件演示");
        QVBoxLayout *mainLayout = new QVBoxLayout(this);

        // 普通按钮
        QPushButton *normalBtn = new QPushButton("普通按钮 👆");
        connect(normalBtn, &QPushButton::clicked, []() {
            QMessageBox::information(nullptr, "提示", "普通按钮被点击了！");
        });
        mainLayout->addWidget(normalBtn);

        // 带图标的按钮
        QPushButton *iconBtn = new QPushButton("带图标 📁");
        iconBtn->setIcon(QIcon::fromTheme("folder"));  // 使用系统主题图标
        iconBtn->setIconSize(QSize(24, 24));
        mainLayout->addWidget(iconBtn);

        // 默认按钮（按回车会触发）
        QPushButton *defaultBtn = new QPushButton("默认按钮 (按回车触发) ⏎");
        defaultBtn->setDefault(true);
        mainLayout->addWidget(defaultBtn);

        // 可切换按钮（像开关一样）
        QPushButton *toggleBtn = new QPushButton("开关按钮 🔌");
        toggleBtn->setCheckable(true);  // 可切换
        toggleBtn->setChecked(false);
        QLabel *toggleLabel = new QLabel("状态: OFF");
        connect(toggleBtn, &QPushButton::toggled, [toggleLabel](bool checked) {
            toggleLabel->setText(QString("状态: %1").arg(checked ? "ON" : "OFF"));
        });
        mainLayout->addWidget(toggleLabel);
        mainLayout->addWidget(toggleBtn);

        // 分隔线
        mainLayout->addSpacing(20);
        mainLayout->addWidget(new QLabel("单选按钮组（互斥）:"));

        // 单选按钮组
        QButtonGroup *radioGroup = new QButtonGroup(this);
        QRadioButton *radio1 = new QRadioButton("选项 A ☕");
        QRadioButton *radio2 = new QRadioButton("选项 B 🍵");
        QRadioButton *radio3 = new QRadioButton("选项 C 🥤");

        radioGroup->addButton(radio1, 1);
        radioGroup->addButton(radio2, 2);
        radioGroup->addButton(radio3, 3);
        radio1->setChecked(true);  // 默认选中第一个

        QLabel *radioLabel = new QLabel("当前选择: 选项 A");
        connect(radioGroup, QOverload<int>::of(&QButtonGroup::buttonClicked),
                [radioLabel](int id) {
            radioLabel->setText(QString("当前选择: 选项 %1").arg(
                id == 1 ? "A" : id == 2 ? "B" : "C"));
        });

        mainLayout->addWidget(radio1);
        mainLayout->addWidget(radio2);
        mainLayout->addWidget(radio3);
        mainLayout->addWidget(radioLabel);

        // 分隔线
        mainLayout->addSpacing(20);
        mainLayout->addWidget(new QLabel("复选框（非互斥）:"));

        // 复选框
        QCheckBox *check1 = new QCheckBox("篮球 🏀");
        QCheckBox *check2 = new QCheckBox("足球 ⚽");
        QCheckBox *check3 = new QCheckBox("乒乓球 🏓");

        QLabel *checkLabel = new QLabel("爱好: 无");
        auto updateCheckLabel = [check1, check2, check3, checkLabel]() {
            QStringList hobbies;
            if (check1->isChecked()) hobbies << "篮球";
            if (check2->isChecked()) hobbies << "足球";
            if (check3->isChecked()) hobbies << "乒乓球";
            checkLabel->setText(hobbies.isEmpty() ? "爱好: 无" : "爱好: " + hobbies.join(", "));
        };

        connect(check1, &QCheckBox::toggled, updateCheckLabel);
        connect(check2, &QCheckBox::toggled, updateCheckLabel);
        connect(check3, &QCheckBox::toggled, updateCheckLabel);

        mainLayout->addWidget(check1);
        mainLayout->addWidget(check2);
        mainLayout->addWidget(check3);
        mainLayout->addWidget(checkLabel);

        mainLayout->addStretch();  // 填充剩余空间
    }
};

int main(int argc, char *argv[]) {
    QApplication app(argc, argv);
    ButtonDemo window;
    window.setMinimumSize(350, 500);
    window.show();
    return app.exec();
}
```

### 输入控件：QLineEdit、QTextEdit、QSpinBox、QComboBox

用户与程序交互的重要桥梁：

```cpp
#include <QApplication>
#include <QWidget>
#include <QVBoxLayout>
#include <QFormLayout>
#include <QLineEdit>
#include <QTextEdit>
#include <QSpinBox>
#include <QDoubleSpinBox>
#include <QComboBox>
#include <QSlider>
#include <QLabel>

class InputDemo : public QWidget {
    Q_OBJECT
public:
    InputDemo(QWidget *parent = nullptr) : QWidget(parent) {
        setWindowTitle("输入控件演示");

        QVBoxLayout *mainLayout = new QVBoxLayout(this);

        // ========== 单行输入框 ==========
        QFormLayout *form = new QFormLayout();

        // 姓名输入
        QLineEdit *nameEdit = new QLineEdit();
        nameEdit->setPlaceholderText("请输入姓名...");
        nameEdit->setMaxLength(50);
        form->addRow("姓名:", nameEdit);

        // 密码输入
        QLineEdit *passEdit = new QLineEdit();
        passEdit->setPlaceholderText("请输入密码...");
        passEdit->setEchoMode(QLineEdit::Password);  // 显示为密码样式
        form->addRow("密码:", passEdit);

        // 邮箱输入
        QLineEdit *emailEdit = new QLineEdit();
        emailEdit->setPlaceholderText("example@domain.com");
        // 输入验证器：限制只能输入邮箱格式
        QValidator *emailValidator = new QRegularExpressionValidator(
            QRegularExpression("^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"), this);
        emailEdit->setValidator(emailValidator);
        form->addRow("邮箱:", emailEdit);

        mainLayout->addLayout(form);

        // ========== 多行文本编辑器 ==========
        QLabel *multiLabel = new QLabel("多行文本编辑:");
        mainLayout->addWidget(multiLabel);

        QTextEdit *textEdit = new QTextEdit();
        textEdit->setPlaceholderText("在这里输入多行文本...\n支持富文本格式!");
        textEdit->setMaximumHeight(100);
        mainLayout->addWidget(textEdit);

        // 实时字数统计
        QLabel *charCountLabel = new QLabel("字符数: 0");
        connect(textEdit, &QTextEdit::textChanged, [textEdit, charCountLabel]() {
            charCountLabel->setText(QString("字符数: %1").arg(textEdit->toPlainText().length()));
        });
        mainLayout->addWidget(charCountLabel);

        // ========== 数字输入 ==========
        QFormLayout *numberForm = new QFormLayout();

        // 整数微调框
        QSpinBox *intSpin = new QSpinBox();
        intSpin->setRange(0, 1000);
        intSpin->setValue(100);
        intSpin->setPrefix("数量: ");
        intSpin->setSuffix(" 件");
        intSpin->setSingleStep(10);  // 步进值
        numberForm->addRow("整数:", intSpin);

        // 浮点数微调框
        QDoubleSpinBox *doubleSpin = new QDoubleSpinBox();
        doubleSpin->setRange(0.0, 100.0);
        doubleSpin->setValue(3.14);
        doubleSpin->setPrefix("价格: ¥");
        doubleSpin->setDecimals(2);  // 2位小数
        numberForm->addRow("浮点数:", doubleSpin);

        mainLayout->addLayout(numberForm);

        // ========== 下拉选择框 ==========
        QFormLayout *comboForm = new QFormLayout();

        QComboBox *countryCombo = new QComboBox();
        countryCombo->addItem("🇨🇳 中国", "CN");
        countryCombo->addItem("🇺🇸 美国", "US");
        countryCombo->addItem("🇯🇵 日本", "JP");
        countryCombo->addItem("🇬🇧 英国", "GB");
        countryCombo->addItem("🇩🇪 德国", "DE");
        comboForm->addRow("国家:", countryCombo);

        QComboBox *colorCombo = new QComboBox();
        colorCombo->addItems({"红色 🔴", "绿色 🟢", "蓝色 🔵", "黄色 🟡"});
        colorCombo->setEditable(true);  // 可编辑
        comboForm->addRow("颜色:", colorCombo);

        mainLayout->addLayout(comboForm);

        // ========== 滑块 ==========
        QLabel *sliderLabel = new QLabel("音量: 50");
        mainLayout->addWidget(sliderLabel);

        QSlider *volumeSlider = new QSlider(Qt::Horizontal);
        volumeSlider->setRange(0, 100);
        volumeSlider->setValue(50);
        mainLayout->addWidget(volumeSlider);

        connect(volumeSlider, &QSlider::valueChanged, [sliderLabel](int value) {
            sliderLabel->setText(QString("音量: %1").arg(value));
        });

        // 滑块和微调框同步
        QSpinBox *sliderSyncSpin = new QSpinBox();
        sliderSyncSpin->setRange(0, 100);
        sliderSyncSpin->setValue(50);
        mainLayout->addWidget(sliderSyncSpin);

        connect(volumeSlider, &QSlider::valueChanged, sliderSyncSpin, &QSpinBox::setValue);
        connect(sliderSyncSpin, QOverload<int>::of(&QSpinBox::valueChanged),
                volumeSlider, &QSlider::setValue);

        // ========== 结果汇总 ==========
        QPushButton *submitBtn = new QPushButton("提交 📤");
        connect(submitBtn, &QPushButton::clicked, [=]() {
            QString info = QString(
                "姓名: %1\n"
                "密码: %2\n"
                "邮箱: %3\n"
                "多行文本: %4\n"
                "整数: %5\n"
                "浮点数: %6\n"
                "国家: %7\n"
                "颜色: %8\n"
                "音量: %9"
            ).arg(nameEdit->text())
             .arg(QString("*").repeated(passEdit->text().length()))
             .arg(emailEdit->text())
             .arg(textEdit->toPlainText())
             .arg(intSpin->value())
             .arg(doubleSpin->value())
             .arg(countryCombo->currentText())
             .arg(colorCombo->currentText())
             .arg(volumeSlider->value());

            QMessageBox::information(this, "输入汇总", info);
        });
        mainLayout->addWidget(submitBtn);
    }
};

int main(int argc, char *argv[]) {
    QApplication app(argc, argv);
    InputDemo window;
    window.setMinimumSize(400, 700);
    window.show();
    return app.exec();
}
```

### 容器控件：QTabWidget、QGroupBox、QStackedWidget

组织复杂界面的利器：

```cpp
#include <QApplication>
#include <QWidget>
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QTabWidget>
#include <QGroupBox>
#include <QStackedWidget>
#include <QListWidget>
#include <QLabel>
#include <QPushButton>
#include <QTableWidget>
#include <QHeaderView>

class ContainerDemo : public QWidget {
    Q_OBJECT
public:
    ContainerDemo(QWidget *parent = nullptr) : QWidget(parent) {
        setWindowTitle("容器控件演示");
        setMinimumSize(600, 400);

        QVBoxLayout *mainLayout = new QVBoxLayout(this);

        // ==================== QTabWidget: 标签页 ====================
        QTabWidget *tabWidget = new QTabWidget();
        tabWidget->setTabPosition(QTabWidget::North);  // 标签位置: 上/下/左/右

        // Tab 1: 分组框示例
        QWidget *groupBoxTab = new QWidget();
        QVBoxLayout *groupBoxLayout = new QVBoxLayout(groupBoxTab);

        // 第一个分组
        QGroupBox *basicGroup = new QGroupBox("基本设置 ⚙️");
        basicGroup->setCheckable(true);  // 可勾选
        basicGroup->setChecked(true);
        QVBoxLayout *basicLayout = new QVBoxLayout(basicGroup);
        basicLayout->addWidget(new QLabel("启用自动保存: ✓"));
        basicLayout->addWidget(new QLabel("显示状态栏: ✓"));
        basicLayout->addWidget(new QLabel("启用快捷键: ✓"));
        groupBoxLayout->addWidget(basicGroup);

        // 第二个分组
        QGroupBox *advanceGroup = new QGroupBox("高级设置 🔧");
        QVBoxLayout *advanceLayout = new QVBoxLayout(advanceGroup);
        advanceLayout->addWidget(new QLabel("调试模式: 关闭"));
        advanceLayout->addWidget(new QLabel("内存限制: 2GB"));
        advanceLayout->addWidget(new QLabel("缓存大小: 500MB"));
        advanceLayout->addStretch();  // 填充空白
        groupBoxLayout->addWidget(advanceGroup);

        tabWidget->addTab(groupBoxTab, "设置");

        // Tab 2: 表格示例
        QTableWidget *table = new QTableWidget(5, 4);  // 5行4列
        table->setHorizontalHeaderLabels({"姓名", "年龄", "职业", "城市"});
        table->verticalHeader()->setVisible(false);  // 隐藏行号

        // 填充数据
        QList<QList<QString>> data = {
            {"张三", "28", "软件工程师", "北京"},
            {"李四", "35", "产品经理", "上海"},
            {"王五", "42", "架构师", "深圳"},
            {"赵六", "25", "前端开发", "杭州"},
            {"钱七", "31", "数据科学家", "广州"}
        };

        for (int i = 0; i < data.size(); ++i) {
            for (int j = 0; j < data[i].size(); ++j) {
                table->setItem(i, j, new QTableWidgetItem(data[i][j]));
            }
        }

        // 设置列宽自适应
        table->horizontalHeader()->setSectionResizeMode(QHeaderView::Stretch);
        tabWidget->addTab(table, "数据表格 📊");

        // Tab 3: 堆叠窗口示例
        QWidget *stackedTab = new QWidget();
        QHBoxLayout *stackedLayout = new QHBoxLayout(stackedTab);

        // 左侧：导航列表
        QListWidget *navList = new QListWidget();
        navList->addItem(new QListWidgetItem(QIcon::fromTheme("user-home"), "首页"));
        navList->addItem(new QListWidgetItem(QIcon::fromTheme("user"), "用户管理"));
        navList->addItem(new QListWidgetItem(QIcon::fromTheme("emblem-system"), "系统设置"));
        navList->addItem(new QListWidgetItem(QIcon::fromTheme("help-about"), "关于"));

        // 右侧：堆叠的页面
        QStackedWidget *stackedWidget = new QStackedWidget();

        // 页面1: 首页
        QLabel *homePage = new QLabel("🏠 欢迎来到主页！\n\n这是Qt容器控件的演示程序。\n点击左侧导航可以切换页面。");
        homePage->setAlignment(Qt::AlignCenter);
        homePage->setStyleSheet("font-size: 18px; padding: 20px;");
        stackedWidget->addWidget(homePage);

        // 页面2: 用户管理
        QLabel *userPage = new QLabel("👥 用户管理页面\n\n这里可以管理用户信息。");
        userPage->setAlignment(Qt::AlignCenter);
        userPage->setStyleSheet("font-size: 18px; padding: 20px;");
        stackedWidget->addWidget(userPage);

        // 页面3: 系统设置
        QLabel *systemPage = new QLabel("⚙️ 系统设置页面\n\n在这里配置系统参数。");
        systemPage->setAlignment(Qt::AlignCenter);
        systemPage->setStyleSheet("font-size: 18px; padding: 20px;");
        stackedWidget->addWidget(systemPage);

        // 页面4: 关于
        QLabel *aboutPage = new QLabel("ℹ️ 关于\n\nQt GUI编程示例\n版本: 1.0.0");
        aboutPage->setAlignment(Qt::AlignCenter);
        aboutPage->setStyleSheet("font-size: 18px; padding: 20px;");
        stackedWidget->addWidget(aboutPage);

        // 列表切换时切换页面
        connect(navList, &QListWidget::currentRowChanged,
                stackedWidget, &QStackedWidget::setCurrentIndex);

        stackedLayout->addWidget(navList, 1);  // 左侧列表占1份
        stackedLayout->addWidget(stackedWidget, 3);  // 右侧页面占3份

        tabWidget->addTab(stackedTab, "导航切换 🧭");

        mainLayout->addWidget(tabWidget);
    }
};

int main(int argc, char *argv[]) {
    QApplication app(argc, argv);
    ContainerDemo window;
    window.show();
    return app.exec();
}
```

---

## 44.4 菜单栏、工具栏与对话框

### 菜单栏和工具栏：应用的"指挥中心"

```cpp
#include <QApplication>
#include <QMainWindow>
#include <QMenuBar>
#include <QMenu>
#include <QAction>
#include <QToolBar>
#include <QStatusBar>
#include <QDialog>
#include <QVBoxLayout>
#include <QLabel>
#include <QPushButton>
#include <QMessageBox>
#include <QInputDialog>
#include <QFileDialog>
#include <QColorDialog>
#include <QFontDialog>
#include <QDir>  // for QDir::homePath()

class MenuDemo : public QMainWindow {
    Q_OBJECT
public:
    MenuDemo(QWidget *parent = nullptr) : QMainWindow(parent) {
        setWindowTitle("菜单栏和工具栏演示");
        resize(700, 500);

        // ========== 创建中心部件 ==========
        QWidget *centralWidget = new QWidget();
        QVBoxLayout *centralLayout = new QVBoxLayout(centralWidget);
        QLabel *statusLabel = new QLabel("📋 就绪");
        statusLabel->setAlignment(Qt::AlignCenter);
        centralLayout->addWidget(statusLabel);
        setCentralWidget(centralWidget);

        // ========== 创建菜单栏 ==========
        QMenuBar *menuBar = new QMenuBar(this);
        setMenuBar(menuBar);

        // 文件菜单
        QMenu *fileMenu = menuBar->addMenu("文件(&F)");  // &F表示快捷键Alt+F
        QAction *newAction = fileMenu->addAction(QIcon::fromTheme("document-new"), "新建(&N)");
        newAction->setShortcut(QKeySequence::New);  // Ctrl+N
        connect(newAction, &QAction::triggered, [statusLabel]() {
            statusLabel->setText("📄 新建文件");
        });

        QAction *openAction = fileMenu->addAction(QIcon::fromTheme("document-open"), "打开(&O)...");
        openAction->setShortcut(QKeySequence::Open);
        connect(openAction, &QAction::triggered, this, &MenuDemo::openFile);

        fileMenu->addSeparator();

        QAction *saveAction = fileMenu->addAction(QIcon::fromTheme("document-save"), "保存(&S)");
        saveAction->setShortcut(QKeySequence::Save);
        connect(saveAction, &QAction::triggered, [statusLabel]() {
            statusLabel->setText("💾 文件已保存");
        });

        fileMenu->addSeparator();

        QAction *exitAction = fileMenu->addAction("退出(&X)");
        exitAction->setShortcut(QKeySequence::Quit);
        connect(exitAction, &QAction::triggered, this, &QMainWindow::close);

        // 编辑菜单
        QMenu *editMenu = menuBar->addMenu("编辑(&E)");
        editMenu->addAction("撤销(&U)", QKeySequence::Undo);
        editMenu->addAction("重做(&R)", QKeySequence::Redo);
        editMenu->addSeparator();
        editMenu->addAction("剪切(&T)", QKeySequence::Cut);
        editMenu->addAction("复制(&C)", QKeySequence::Copy);
        editMenu->addAction("粘贴(&V)", QKeySequence::Paste);

        // 视图菜单
        QMenu *viewMenu = menuBar->addMenu("视图(&V)");
        QAction *fullscreenAction = viewMenu->addAction("全屏(&F)");
        fullscreenAction->setShortcut(QKeySequence::FullScreen);
        connect(fullscreenAction, &QAction::triggered, [this, fullscreenAction]() {
            if (isFullScreen()) {
                showNormal();
                fullscreenAction->setText("全屏(&F)");
            } else {
                showFullScreen();
                fullscreenAction->setText("退出全屏(&F)");
            }
        });

        // 工具菜单
        QMenu *toolMenu = menuBar->addMenu("工具(&T)");
        toolMenu->addAction("颜色选择器", this, &MenuDemo::showColorPicker);
        toolMenu->addAction("字体选择器", this, &MenuDemo::showFontPicker);

        // 帮助菜单
        QMenu *helpMenu = menuBar->addMenu("帮助(&H)");
        QAction *aboutAction = helpMenu->addAction("关于(&A)...");
        connect(aboutAction, &QAction::triggered, []() {
            QMessageBox::about(nullptr, "关于",
                "🎓 Qt GUI编程示例\n\n"
                "这是一个演示菜单栏、工具栏和对话框的程序。\n"
                "版本: 1.0.0\n"
                "作者: C++学习者");
        });

        QAction *helpAction = helpMenu->addAction("使用帮助(&H)");
        helpAction->setShortcut(QKeySequence::HelpContents);
        connect(helpAction, &QAction::triggered, []() {
            QMessageBox::information(nullptr, "帮助",
                "📖 使用帮助\n\n"
                "1. 使用菜单栏访问各种功能\n"
                "2. 工具栏提供快速操作\n"
                "3. 状态栏显示当前操作信息\n\n"
                "祝您使用愉快！🎉");
        });

        // ========== 创建工具栏 ==========
        QToolBar *toolbar = addToolBar("主工具栏");
        toolbar->setMovable(false);  // 固定位置

        toolbar->addAction(newAction);
        toolbar->addAction(openAction);
        toolbar->addAction(saveAction);
        toolbar->addSeparator();

        QAction *undoAction = toolbar->addAction(QIcon::fromTheme("edit-undo"), "撤销");
        connect(undoAction, &QAction::triggered, [statusLabel]() {
            statusLabel->setText("↩️ 撤销操作");
        });

        QAction *redoAction = toolbar->addAction(QIcon::fromTheme("edit-redo"), "重做");
        connect(redoAction, &QAction::triggered, [statusLabel]() {
            statusLabel->setText("↪️ 重做操作");
        });

        toolbar->addSeparator();

        // 自定义工具栏按钮
        QPushButton *colorBtn = new QPushButton("🎨");
        colorBtn->setToolTip("选择颜色");
        connect(colorBtn, &QPushButton::clicked, this, &MenuDemo::showColorPicker);
        toolbar->addWidget(colorBtn);

        // ========== 创建状态栏 ==========
        QStatusBar *statusbar = statusBar();
        statusbar->showMessage("就绪", 3000);  // 显示3秒后消失
        statusbar->addPermanentWidget(new QLabel("🔔 通知已开启"));
    }

private slots:
    void openFile() {
        // 文件对话框示例
        QString fileName = QFileDialog::getOpenFileName(
            this,
            "打开文件",
            QDir::homePath(),
            "文本文件 (*.txt);;所有文件 (*.*)"
        );

        if (!fileName.isEmpty()) {
            QMessageBox::information(this, "打开文件",
                QString("📂 您选择了文件:\n%1").arg(fileName));
        }
    }

    void showColorPicker() {
        QColor initialColor = Qt::blue;
        QColor color = QColorDialog::getColor(initialColor, this, "选择颜色");

        if (color.isValid()) {
            QMessageBox::information(this, "颜色选择",
                QString("🎨 选择的颜色:\n"
                       "RGB: (%1, %2, %3)\n"
                       "HEX: %4").arg(
                    color.red()).arg(color.green()).arg(color.blue()).arg(
                    color.name().toUpper()));
        }
    }

    void showFontPicker() {
        bool ok;
        QFont font = QFontDialog::getFont(&ok, QFont("Arial", 12), this, "选择字体");

        if (ok) {
            QMessageBox::information(this, "字体选择",
                QString("🔤 选择的字体:\n%1, %2pt").arg(
                    font.family()).arg(font.pointSize()));
        }
    }
};

int main(int argc, char *argv[]) {
    QApplication app(argc, argv);
    MenuDemo window;
    window.show();
    return app.exec();
}
```

### 标准对话框：一站式用户交互

Qt提供了丰富的标准对话框，让常见交互变得简单：

```cpp
#include <QApplication>
#include <QWidget>
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QPushButton>
#include <QLabel>
#include <QTextEdit>
#include <QInputDialog>
#include <QMessageBox>
#include <QFileDialog>
#include <QColorDialog>
#include <QFontDialog>
#include <QProgressDialog>
#include <QColor>
#include <QThread>  // for QThread::msleep

class DialogDemo : public QWidget {
    Q_OBJECT
public:
    DialogDemo(QWidget *parent = nullptr) : QWidget(parent) {
        setWindowTitle("标准对话框演示");
        QVBoxLayout *mainLayout = new QVBoxLayout(this);

        QLabel *resultLabel = new QLabel("结果将在此显示...");
        resultLabel->setStyleSheet("padding: 10px; background: #f0f0f0; border-radius: 5px;");
        mainLayout->addWidget(resultLabel);

        // ========== 消息框 ==========
        QPushButton *infoBtn = new QPushButton("信息消息框 ℹ️");
        connect(infoBtn, &QPushButton::clicked, []() {
            QMessageBox::information(nullptr, "信息", "这是一条普通的信息消息！");
        });
        mainLayout->addWidget(infoBtn);

        QPushButton *warnBtn = new QPushButton("警告消息框 ⚠️");
        connect(warnBtn, &QPushButton::clicked, []() {
            QMessageBox::warning(nullptr, "警告", "这是一个警告消息！\n请注意您的操作！");
        });
        mainLayout->addWidget(warnBtn);

        QPushButton *errorBtn = new QPushButton("错误消息框 ❌");
        connect(errorBtn, &QPushButton::clicked, []() {
            QMessageBox::critical(nullptr, "错误", "发生了一个严重错误！\n程序可能需要退出。");
        });
        mainLayout->addWidget(errorBtn);

        QPushButton *quesBtn = new QPushButton("询问消息框 ❓");
        connect(quesBtn, &QPushButton::clicked, [resultLabel]() {
            QMessageBox::StandardButton reply = QMessageBox::question(
                nullptr, "确认",
                "您确定要继续吗？",
                QMessageBox::Yes | QMessageBox::No | QMessageBox::Cancel);

            QString result;
            if (reply == QMessageBox::Yes) result = "用户选择了: Yes ✅";
            else if (reply == QMessageBox::No) result = "用户选择了: No ❌";
            else result = "用户选择了: Cancel ⏸️";

            resultLabel->setText(result);
        });
        mainLayout->addWidget(quesBtn);

        // ========== 输入对话框 ==========
        QPushButton *textInputBtn = new QPushButton("文本输入对话框 📝");
        connect(textInputBtn, &QPushButton::clicked, [resultLabel]() {
            bool ok;
            QString text = QInputDialog::getText(nullptr, "输入文本",
                "请输入您的名字:", QLineEdit::Normal, "张三", &ok);

            if (ok && !text.isEmpty()) {
                resultLabel->setText(QString("您好, %1! 👋").arg(text));
            }
        });
        mainLayout->addWidget(textInputBtn);

        QPushButton *intInputBtn = new QPushButton("整数输入对话框 🔢");
        connect(intInputBtn, &QPushButton::clicked, [resultLabel]() {
            bool ok;
            int value = QInputDialog::getInt(nullptr, "输入整数",
                "请输入您的年龄:", 25, 0, 150, 1, &ok);

            if (ok) {
                QString category = value < 18 ? "青少年" :
                                   value < 30 ? "青年" :
                                   value < 60 ? "中年" : "老年";
                resultLabel->setText(QString("年龄: %1 (%2)").arg(value).arg(category));
            }
        });
        mainLayout->addWidget(intInputBtn);

        QPushButton *itemInputBtn = new QPushButton("选择输入对话框 📋");
        connect(itemInputBtn, &QPushButton::clicked, [resultLabel]() {
            QStringList items = {"苹果 🍎", "香蕉 🍌", "橙子 🍊", "葡萄 🍇"};
            bool ok;
            QString item = QInputDialog::getItem(nullptr, "选择水果",
                "请选择您最喜欢的水果:", items, 0, false, &ok);

            if (ok && !item.isEmpty()) {
                resultLabel->setText(QString("您选择了: %1").arg(item));
            }
        });
        mainLayout->addWidget(itemInputBtn);

        // ========== 文件对话框 ==========
        QPushButton *openFileBtn = new QPushButton("打开文件对话框 📂");
        connect(openFileBtn, &QPushButton::clicked, [resultLabel]() {
            QString fileName = QFileDialog::getOpenFileName(nullptr,
                "打开文件", QDir::homePath(),
                "图片文件 (*.png *.jpg *.jpeg *.gif);;文本文件 (*.txt);;所有文件 (*.*)");

            if (!fileName.isEmpty()) {
                resultLabel->setText(QString("打开文件: %1").arg(fileName));
            } else {
                resultLabel->setText("未选择文件");
            }
        });
        mainLayout->addWidget(openFileBtn);

        QPushButton *saveFileBtn = new QPushButton("保存文件对话框 💾");
        connect(saveFileBtn, &QPushButton::clicked, [resultLabel]() {
            QString fileName = QFileDialog::getSaveFileName(nullptr,
                "保存文件", QDir::homePath() + "/untitled.txt",
                "文本文件 (*.txt);;所有文件 (*.*)");

            if (!fileName.isEmpty()) {
                resultLabel->setText(QString("保存到: %1").arg(fileName));
            } else {
                resultLabel->setText("未选择保存位置");
            }
        });
        mainLayout->addWidget(saveFileBtn);

        // ========== 颜色和字体对话框 ==========
        QPushButton *colorBtn = new QPushButton("颜色选择对话框 🎨");
        connect(colorBtn, &QPushButton::clicked, [resultLabel]() {
            QColor color = QColorDialog::getColor(Qt::blue, nullptr, "选择颜色");

            if (color.isValid()) {
                resultLabel->setText(QString("颜色: RGB(%1, %2, %3)").arg(
                    color.red()).arg(color.green()).arg(color.blue()));
                resultLabel->setStyleSheet(
                    QString("padding: 10px; background: %1; border-radius: 5px; color: white;").arg(
                    color.name()));
            }
        });
        mainLayout->addWidget(colorBtn);

        QPushButton *fontBtn = new QPushButton("字体选择对话框 🔤");
        connect(fontBtn, &QPushButton::clicked, [resultLabel]() {
            bool ok;
            QFont font = QFontDialog::getFont(&ok, QFont("Arial", 12), nullptr, "选择字体");

            if (ok) {
                resultLabel->setText(QString("字体: %1, %2pt").arg(
                    font.family()).arg(font.pointSize()));
                resultLabel->setFont(font);
            }
        });
        mainLayout->addWidget(fontBtn);

        // ========== 进度对话框 ==========
        QPushButton *progressBtn = new QPushButton("进度对话框 ⏳");
        connect(progressBtn, &QPushButton::clicked, []() {
            QProgressDialog *progressDialog = new QProgressDialog(
                "正在下载文件...", "取消", 0, 100);
            progressDialog->setWindowTitle("下载进度");
            progressDialog->setMinimumDuration(0);  // 立即显示

            for (int i = 0; i <= 100; i += 10) {
                QThread::msleep(200);  // 模拟耗时操作
                progressDialog->setValue(i);
                if (progressDialog->wasCanceled()) {
                    QMessageBox::information(nullptr, "提示", "下载已取消");
                    break;
                }
            }
            progressDialog->setValue(100);
            QMessageBox::information(nullptr, "完成", "下载完成！🎉");
        });
        mainLayout->addWidget(progressBtn);

        mainLayout->addStretch();
    }
};

int main(int argc, char *argv[]) {
    QApplication app(argc, argv);
    DialogDemo window;
    window.setMinimumSize(400, 600);
    window.show();
    return app.exec();
}
```

---

## 44.5 绘图与自定义控件

### Qt的绘图系统：QPainter

Qt的绘图系统基于**QPainter**，它就像一位画家，可以在任何`QPaintDevice`上作画——无论是窗口、图像还是打印设备。

```cpp
#include <QApplication>
#include <QWidget>
#include <QPainter>
#include <QPen>
#include <QBrush>
#include <QFont>
#include <QGradient>
#include <QTransform>
#include <QRandomGenerator>
#include <QLabel>
#include <QVBoxLayout>

// 自定义绘图窗口
class PaintDemo : public QWidget {
    Q_OBJECT
public:
    PaintDemo(QWidget *parent = nullptr) : QWidget(parent) {
        setWindowTitle("Qt绘图演示");
        setMinimumSize(800, 600);
    }

protected:
    void paintEvent(QPaintEvent *event) override {
        QPainter painter(this);
        painter.setRenderHint(QPainter::Antialiasing);  // 抗锯齿
        painter.setRenderHint(QPainter::TextAntialiasing);

        int w = width();
        int h = height();

        // ========== 1. 基本几何图形 ==========
        // 画线
        QPen linePen(Qt::red, 3);
        painter.setPen(linePen);
        painter.drawLine(20, 20, 200, 20);
        painter.drawText(20, 40, "直线");

        // 画矩形
        QBrush rectBrush(Qt::blue);
        painter.setBrush(rectBrush);
        painter.drawRect(20, 60, 100, 60);
        painter.drawText(130, 90, "矩形");

        // 画椭圆
        QBrush ellipseBrush(QColor(0, 200, 0));
        painter.setBrush(ellipseBrush);
        painter.drawEllipse(20, 140, 100, 60);
        painter.drawText(130, 170, "椭圆");

        // 画圆
        QColor circleColor(200, 0, 200);
        painter.setBrush(circleColor);
        painter.drawEllipse(20, 200, 60, 60);
        painter.drawText(90, 230, "圆");

        // 画多边形
        QVector<QPointF> triangle;
        triangle << QPointF(20, 280) << QPointF(100, 280) << QPointF(60, 320);
        painter.setBrush(QColor(255, 165, 0));
        painter.drawPolygon(triangle);
        painter.drawText(110, 305, "三角形");

        // ========== 2. 渐变填充 ==========
        // 线性渐变
        QLinearGradient linearGrad(20, 350, 200, 350);
        linearGrad.setColorAt(0, Qt::red);
        linearGrad.setColorAt(0.5, Qt::yellow);
        linearGrad.setColorAt(1, Qt::green);
        painter.setBrush(linearGrad);
        painter.drawRect(20, 350, 180, 50);
        painter.drawText(210, 380, "线性渐变");

        // 径向渐变
        QRadialGradient radialGrad(100, 450, 50, 100, 450);
        radialGrad.setColorAt(0, Qt::white);
        radialGrad.setColorAt(0.5, Qt::cyan);
        radialGrad.setColorAt(1, Qt::blue);
        painter.setBrush(radialGrad);
        painter.drawEllipse(50, 400, 100, 100);
        painter.drawText(160, 455, "径向渐变");

        // ========== 3. 文本绘制 ==========
        painter.setPen(Qt::black);
        QFont titleFont("Arial", 16, QFont::Bold);
        painter.setFont(titleFont);
        painter.drawText(w/2 + 50, 30, "Qt绘图示例 🖌️");

        QFont normalFont("Consolas", 12);
        painter.setFont(normalFont);
        painter.setPen(Qt::darkBlue);
        painter.drawText(w/2 + 50, 60, "字体: Consolas, 12pt");

        // 带背景的文本
        QRectF textRect(w/2 + 50, 80, 200, 40);
        painter.fillRect(textRect, QColor(255, 255, 200));
        painter.drawRect(textRect);
        painter.drawText(textRect, Qt::AlignCenter, "带背景的文本 📝");

        // ========== 4. 变换操作 ==========
        painter.save();  // 保存画笔状态

        // 平移
        painter.translate(w/2 + 50, 160);
        painter.setBrush(Qt::darkMagenta);
        painter.drawRect(-30, -30, 60, 60);
        painter.drawText(0, 50, "平移");

        painter.restore();  // 恢复画笔状态

        // 旋转
        painter.save();
        painter.translate(w/2 + 150, 160);
        painter.rotate(45);
        painter.setBrush(Qt::darkCyan);
        painter.drawRect(-30, -30, 60, 60);
        painter.drawText(0, 50, "旋转45°");
        painter.restore();

        // 缩放
        painter.save();
        painter.translate(w/2 + 250, 160);
        painter.scale(1.5, 0.8);
        painter.setBrush(Qt::darkYellow);
        painter.drawRect(-30, -30, 60, 60);
        painter.drawText(0, 50, "缩放1.5x");
        painter.restore();

        // ========== 5. 高级绘图: 画家的艺术 🎨 ==========
        // 绘制饼图
        painter.save();
        painter.translate(100, h - 180);

        QVector<QPair<QString, double>> data = {
            {"苹果", 30},
            {"香蕉", 25},
            {"橙子", 20},
            {"葡萄", 15},
            {"其他", 10}
        };

        QVector<QColor> colors = {
            Qt::red, Qt::yellow, Qt::orange, Qt::darkMagenta, Qt::gray
        };

        double total = 0;
        for (auto &item : data) total += item.second;

        double startAngle = 0;
        int centerX = 80, centerY = 80, radius = 70;

        for (int i = 0; i < data.size(); ++i) {
            double spanAngle = (data[i].second / total) * 360 * 16;  // 16分之一度
            painter.setBrush(colors[i]);
            painter.drawPie(-radius, -radius, radius*2, radius*2,
                           startAngle, spanAngle);
            startAngle += spanAngle;
        }

        // 绘制图例
        painter.setPen(Qt::black);
        painter.setBrush(Qt::NoBrush);
        for (int i = 0; i < data.size(); ++i) {
            int legendY = 100 + i * 20;
            painter.setBrush(colors[i]);
            painter.drawRect(w/2 - 80, legendY - 10, 15, 15);
            painter.drawText(w/2 - 55, legendY + 3,
                QString("%1: %2%").arg(data[i].first).arg(data[i].second, 0, 'f', 0));
        }

        painter.restore();

        // ========== 6. 贝塞尔曲线 ==========
        painter.save();
        painter.translate(w/2 + 50, h - 180);

        QPainterPath path;
        path.moveTo(0, 100);
        path.cubicTo(50, 0, 150, 200, 200, 100);

        painter.setPen(QPen(Qt::blue, 3));
        painter.setBrush(Qt::NoBrush);
        painter.drawPath(path);

        // 绘制控制点
        painter.setBrush(Qt::red);
        painter.drawEllipse(0, 95, 10, 10);    // 起点
        painter.drawEllipse(50, -5, 10, 10);   // 控制点1
        painter.drawEllipse(150, 195, 10, 10); // 控制点2
        painter.drawEllipse(195, 95, 10, 10);  // 终点

        painter.setPen(Qt::black);
        painter.drawText(0, 130, "贝塞尔曲线");
        painter.restore();

        // ========== 7. 绘制时钟 ==========
        painter.save();
        painter.translate(w - 120, h - 120);

        // 表盘
        painter.setBrush(Qt::white);
        painter.setPen(QPen(Qt::black, 3));
        painter.drawEllipse(-80, -80, 160, 160);

        // 刻度
        for (int i = 0; i < 12; ++i) {
            painter.save();
            painter.rotate(i * 30);
            painter.drawLine(0, -70, 0, -60);
            painter.restore();
        }

        // 时针
        QDateTime now = QDateTime::currentDateTime();
        double hourAngle = (now.time().hour() % 12 + now.time().minute() / 60.0) * 30;
        painter.save();
        painter.rotate(hourAngle);
        painter.setPen(QPen(Qt::black, 5));
        painter.drawLine(0, 0, 0, -40);
        painter.restore();

        // 分针
        double minuteAngle = now.time().minute() * 6;
        painter.save();
        painter.rotate(minuteAngle);
        painter.setPen(QPen(Qt::darkBlue, 3));
        painter.drawLine(0, 0, 0, -55);
        painter.restore();

        // 秒针
        double secondAngle = now.time().second() * 6;
        painter.save();
        painter.rotate(secondAngle);
        painter.setPen(QPen(Qt::red, 2));
        painter.drawLine(0, 0, 0, -60);
        painter.restore();

        painter.restore();

        painter.setPen(Qt::darkGray);
        painter.drawText(w - 200, h - 10, "🕐 当前时间");
    }
};

int main(int argc, char *argv[]) {
    QApplication app(argc, argv);
    PaintDemo window;
    window.show();
    return app.exec();
}
```

### 自定义控件：打造独一无二的界面组件

```cpp
#include <QApplication>
#include <QWidget>
#include <QPainter>
#include <QPainterPath>
#include <QPropertyAnimation>
#include <QMouseEvent>
#include <QTimer>
#include <QLabel>
#include <QVBoxLayout>
#include <QPushButton>
#include <QtMath>  // for qDegreesToRadians, qRadiansToDegrees
#ifndef M_PI
#define M_PI 3.14159265358979323846  // POSIX M_PI fallback
#endif

// ========== 圆形进度条 ==========
class CircleProgressBar : public QWidget {
    Q_OBJECT
    Q_PROPERTY(double progress READ progress WRITE setProgress NOTIFY progressChanged)
    Q_PROPERTY(QColor progressColor READ progressColor WRITE setProgressColor)
    Q_PROPERTY(QColor backgroundColor READ backgroundColor WRITE setBackgroundColor)

public:
    CircleProgressBar(QWidget *parent = nullptr)
        : QWidget(parent), m_progress(0), m_progressColor(Qt::blue),
          m_backgroundColor(Qt::lightGray) {
        setMinimumSize(150, 150);
    }

    double progress() const { return m_progress; }
    void setProgress(double value) {
        m_progress = qBound(0.0, value, 100.0);
        update();  // 触发重绘
        emit progressChanged(m_progress);
    }

    QColor progressColor() const { return m_progressColor; }
    void setProgressColor(const QColor &color) {
        m_progressColor = color;
        update();
    }

    QColor backgroundColor() const { return m_backgroundColor; }
    void setBackgroundColor(const QColor &color) {
        m_backgroundColor = color;
        update();
    }

signals:
    void progressChanged(double);

protected:
    void paintEvent(QPaintEvent *) override {
        QPainter painter(this);
        painter.setRenderHint(QPainter::Antialiasing);

        int side = qMin(width(), height());
        painter.setViewport((width() - side) / 2, (height() - side) / 2, side, side);
        painter.setWindow(-50, -50, 100, 100);

        // 背景圆
        painter.setBrush(m_backgroundColor);
        painter.setPen(Qt::NoPen);
        painter.drawEllipse(-50, -50, 100, 100);

        // 进度圆弧
        QPainterPath path;
        path.arcMoveTo(-45, -45, 90, 90, -90);
        path.arcTo(-45, -45, 90, 90, -90, m_progress * 3.6);  // 3.6度每百分比

        painter.setPen(QPen(m_progressColor, 8, Qt::RoundCap));
        painter.setBrush(Qt::NoBrush);
        painter.drawPath(path);

        // 中心百分比文字
        painter.setPen(Qt::black);
        QFont font = painter.font();
        font.setPixelSize(16);
        font.setBold(true);
        painter.setFont(font);
        painter.drawText(-20, 6, QString::number(m_progress, 'f', 0) + "%");
    }

private:
    double m_progress;
    QColor m_progressColor;
    QColor m_backgroundColor;
};

// ========== 霓虹按钮 ==========
class NeonButton : public QPushButton {
    Q_OBJECT
public:
    NeonButton(const QString &text, QWidget *parent = nullptr)
        : QPushButton(text, parent) {
        setMinimumHeight(50);
        setMinimumWidth(150);
        setCursor(Qt::PointingHandCursor);
    }

protected:
    void paintEvent(QPaintEvent *event) override {
        QPainter painter(this);
        painter.setRenderHint(QPainter::Antialiasing);

        QRectF rect = QRectF(event->rect()).adjusted(2, 2, -2, -2);

        // 颜色方案
        QColor baseColor = isChecked() ? Qt::cyan : (isDown() ? Qt::yellow : Qt::green);
        QColor glowColor = baseColor.lighter(150);

        // 外发光效果
        for (int i = 3; i > 0; --i) {
            QPen pen(glowColor, 2, Qt::SolidLine);
            pen.setColor(glowColor);
            pen.setColor(glowColor.withAlpha(50 / i));
            painter.setPen(pen);
            painter.drawRoundedRect(rect.adjusted(i*2, i*2, -i*2, -i*2), 10, 10);
        }

        // 主按钮
        painter.setPen(Qt::NoPen);
        QLinearGradient gradient(rect.topLeft(), rect.bottomLeft());
        gradient.setColorAt(0, baseColor.darker(120));
        gradient.setColorAt(0.5, baseColor);
        gradient.setColorAt(1, baseColor.darker(120));
        painter.setBrush(gradient);
        painter.drawRoundedRect(rect, 10, 10);

        // 文字
        painter.setPen(isDown() ? Qt::black : Qt::white);
        QFont font = painter.font();
        font.setPixelSize(14);
        font.setBold(true);
        painter.setFont(font);
        painter.drawText(rect, Qt::AlignCenter, text());
    }
};

// ========== 波浪进度条 ==========
class WaveProgressBar : public QWidget {
    Q_OBJECT
    Q_PROPERTY(double waterLevel READ waterLevel WRITE setWaterLevel NOTIFY waterLevelChanged)

public:
    WaveProgressBar(QWidget *parent = nullptr)
        : QWidget(parent), m_waterLevel(0.5), m_offset(0) {
        setMinimumSize(100, 100);
        m_waveTimer = new QTimer(this);
        connect(m_waveTimer, &QTimer::timeout, [this]() {
            m_offset += 0.1;
            if (m_offset > 2 * M_PI) m_offset = 0;
            update();
        });
        m_waveTimer->start(50);
    }

    double waterLevel() const { return m_waterLevel; }
    void setWaterLevel(double level) {
        m_waterLevel = qBound(0.0, level, 1.0);
        emit waterLevelChanged(m_waterLevel);
        update();
    }

signals:
    void waterLevelChanged(double);

protected:
    void paintEvent(QPaintEvent *) override {
        QPainter painter(this);
        painter.setRenderHint(QPainter::Antialiasing);

        // 背景
        painter.setPen(Qt::NoPen);
        painter.setBrush(QColor(200, 220, 240));
        painter.drawRoundedRect(rect(), 15, 15);

        // 水波
        QPainterPath wavePath;
        wavePath.moveTo(0, height());

        // 第一层波浪
        for (double x = 0; x <= width(); x += 1) {
            double y = height() * (1 - m_waterLevel) +
                       10 * qSin((x / width() * 2 * M_PI) + m_offset);
            wavePath.lineTo(x, y);
        }
        wavePath.lineTo(width(), height());
        wavePath.closeSubpath();

        // 水波颜色渐变
        QLinearGradient gradient(0, 0, 0, height());
        gradient.setColorAt(0, QColor(100, 180, 255, 200));
        gradient.setColorAt(1, QColor(50, 100, 200, 200));
        painter.setBrush(gradient);
        painter.drawPath(wavePath);

        // 百分比文字
        painter.setPen(Qt::white);
        QFont font = painter.font();
        font.setPixelSize(20);
        font.setBold(true);
        painter.setFont(font);
        painter.drawText(rect(), Qt::AlignCenter,
                        QString::number(m_waterLevel * 100, 'f', 0) + "%");
    }

private:
    double m_waterLevel;
    double m_offset;
    QTimer *m_waveTimer;
};

// ========== 演示窗口 ==========
class CustomWidgetDemo : public QWidget {
    Q_OBJECT
public:
    CustomWidgetDemo(QWidget *parent = nullptr) : QWidget(parent) {
        setWindowTitle("自定义控件演示 🎨");
        QVBoxLayout *mainLayout = new QVBoxLayout(this);

        // 圆形进度条
        QLabel *circleLabel = new QLabel("圆形进度条");
        circleLabel->setAlignment(Qt::AlignCenter);
        mainLayout->addWidget(circleLabel);

        CircleProgressBar *circleProgress = new CircleProgressBar();
        circleProgress->setProgressColor(Qt::cyan);
        mainLayout->addWidget(circleProgress);

        // 进度动画
        QPropertyAnimation *progressAnim = new QPropertyAnimation(circleProgress, "progress", this);
        progressAnim->setDuration(3000);
        progressAnim->setStartValue(0);
        progressAnim->setEndValue(100);
        progressAnim->setEasingCurve QEasingCurve::InOutQuad;
        progressAnim->setLoopCount(-1);  // 无限循环
        progressAnim->start();

        // 霓虹按钮
        QLabel *buttonLabel = new QLabel("霓虹按钮（点击切换）");
        buttonLabel->setAlignment(Qt::AlignCenter);
        mainLayout->addWidget(buttonLabel);

        NeonButton *neonBtn = new NeonButton("✨ 点我 ✨");
        mainLayout->addWidget(neonBtn);

        // 波浪进度条
        QLabel *waveLabel = new QLabel("波浪进度条");
        waveLabel->setAlignment(Qt::AlignCenter);
        mainLayout->addWidget(waveLabel);

        WaveProgressBar *waveBar = new WaveProgressBar();
        waveBar->setMinimumHeight(120);
        mainLayout->addWidget(waveBar);

        // 波浪动画
        QPropertyAnimation *waveAnim = new QPropertyAnimation(waveBar, "waterLevel", this);
        waveAnim->setDuration(5000);
        waveAnim->setStartValue(0.1);
        waveAnim->setEndValue(0.9);
        waveAnim->setEasingCurve QEasingCurve::SineCurve);
        waveAnim->setLoopCount(-1);
        waveAnim->setDirection(QAbstractAnimation::Backward);
        waveAnim->start();

        // 调整按钮
        QPushButton *incBtn = new QPushButton("增加进度 ⬆️");
        QPushButton *decBtn = new QPushButton("减少进度 ⬇️");
        QHBoxLayout *btnLayout = new QHBoxLayout();
        btnLayout->addWidget(decBtn);
        btnLayout->addWidget(incBtn);
        mainLayout->addLayout(btnLayout);

        connect(incBtn, &QPushButton::clicked, [circleProgress]() {
            circleProgress->setProgress(circleProgress->progress() + 10);
        });
        connect(decBtn, &QPushButton::clicked, [circleProgress]() {
            circleProgress->setProgress(circleProgress->progress() - 10);
        });

        mainLayout->addStretch();
    }
};

int main(int argc, char *argv[]) {
    QApplication app(argc, argv);
    CustomWidgetDemo window;
    window.setMinimumSize(400, 700);
    window.show();
    return app.exec();
}
```

---

## 44.6 模型/视图架构：优雅的数据展示

当你的数据量达到成百上千条时，手动管理每个数据项就变得不现实了。Qt的**Model/View架构**就是为了解决这个问题而生的。

```cpp
#include <QApplication>
#include <QWidget>
#include <QAbstractItemModel>
#include <QAbstractItemView>
#include <QListView>
#include <QTableView>
#include <QTreeView>
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QPushButton>
#include <QLabel>
#include <QInputDialog>
#include <QMessageBox>
#include <QHeaderView>
#include <QStyledItemDelegate>

// ========== 自定义模型：联系人列表 ==========
class ContactModel : public QAbstractTableModel {
    Q_OBJECT
public:
    ContactModel(QObject *parent = nullptr) : QAbstractTableModel(parent) {
        // 添加一些示例数据
        m_contacts = {
            {"张三", "13800138000", "北京", true},
            {"李四", "13900139000", "上海", false},
            {"王五", "13700137000", "深圳", true},
            {"赵六", "13600136000", "广州", false},
            {"钱七", "13500135000", "杭州", true}
        };
    }

    // 必须实现的虚函数
    int rowCount(const QModelIndex &parent = QModelIndex()) const override {
        if (parent.isValid()) return 0;  // 仅根节点有数据
        return m_contacts.size();
    }

    int columnCount(const QModelIndex &parent = QModelIndex()) const override {
        if (parent.isValid()) return 0;
        return 4;  // 姓名、电话、城市、星标
    }

    QVariant data(const QModelIndex &index, int role = Qt::DisplayRole) const override {
        if (!index.isValid() || index.row() >= m_contacts.size())
            return QVariant();

        const Contact &contact = m_contacts[index.row()];

        if (role == Qt::DisplayRole || role == Qt::EditRole) {
            switch (index.column()) {
                case 0: return contact.name;
                case 1: return contact.phone;
                case 2: return contact.city;
                case 3: return contact.starred ? "⭐" : "";
                default: return QVariant();
            }
        }

        // 对齐方式
        if (role == Qt::TextAlignmentRole) {
            if (index.column() == 3) return Qt::AlignCenter;
            return Qt::AlignLeft | Qt::AlignVCenter;
        }

        // 背景颜色
        if (role == Qt::BackgroundRole) {
            if (contact.starred) return QColor(255, 255, 200);
            if (index.row() % 2 == 0) return QColor(240, 240, 240);
            return QColor(255, 255, 255);
        }

        return QVariant();
    }

    // 可编辑
    Qt::ItemFlags flags(const QModelIndex &index) const override {
        return QAbstractTableModel::flags(index) | Qt::ItemIsEditable;
    }

    // 设置数据
    bool setData(const QModelIndex &index, const QVariant &value, int role = Qt::EditRole) override {
        if (!index.isValid() || index.row() >= m_contacts.size())
            return false;

        if (role == Qt::EditRole) {
            Contact &contact = m_contacts[index.row()];
            switch (index.column()) {
                case 0: contact.name = value.toString(); break;
                case 1: contact.phone = value.toString(); break;
                case 2: contact.city = value.toString(); break;
                case 3: contact.starred = value.toBool(); break;
                default: return false;
            }
            emit dataChanged(index, index, {role});
            return true;
        }
        return false;
    }

    // 表头数据
    QVariant headerData(int section, Qt::Orientation orientation,
                       int role = Qt::DisplayRole) const override {
        if (role != Qt::DisplayRole) return QVariant();

        if (orientation == Qt::Horizontal) {
            switch (section) {
                case 0: return "姓名 👤";
                case 1: return "电话 📞";
                case 2: return "城市 🏙️";
                case 3: return "收藏 ⭐";
                default: return QVariant();
            }
        }
        return QVariant();
    }

    // 添加联系人
    void addContact(const QString &name, const QString &phone,
                   const QString &city, bool starred = false) {
        beginInsertRows(QModelIndex(), m_contacts.size(), m_contacts.size());
        m_contacts.append({name, phone, city, starred});
        endInsertRows();
    }

    // 删除联系人
    void removeContact(int row) {
        if (row < 0 || row >= m_contacts.size()) return;
        beginRemoveRows(QModelIndex(), row, row);
        m_contacts.removeAt(row);
        endRemoveRows();
    }

    // 获取联系人
    Contact getContact(int row) const {
        if (row >= 0 && row < m_contacts.size())
            return m_contacts[row];
        return {"", "", "", false};
    }

private:
    struct Contact {
        QString name;
        QString phone;
        QString city;
        bool starred;
    };
    QVector<Contact> m_contacts;
};

// ========== 自定义委托：美化编辑 ==========
class ContactDelegate : public QStyledItemDelegate {
public:
    ContactDelegate(QObject *parent = nullptr) : QStyledItemDelegate(parent) {}

    // 创建编辑器
    QWidget *createEditor(QWidget *parent, const QStyleOptionViewItem &option,
                         const QModelIndex &index) const override {
        if (index.column() == 1) {  // 电话列用行编辑
            QLineEdit *editor = new QLineEdit(parent);
            editor->setPlaceholderText("请输入11位手机号...");
            return editor;
        }
        return QStyledItemDelegate::createEditor(parent, option, index);
    }

    // 设置编辑器数据
    void setEditorData(QWidget *editor, const QModelIndex &index) const override {
        if (index.column() == 1) {
            QLineEdit *lineEdit = qobject_cast<QLineEdit*>(editor);
            lineEdit->setText(index.model()->data(index, Qt::EditRole).toString());
        } else {
            QStyledItemDelegate::setEditorData(editor, index);
        }
    }

    // 更新模型数据
    void setModelData(QWidget *editor, QAbstractItemModel *model,
                     const QModelIndex &index) const override {
        if (index.column() == 1) {
            QLineEdit *lineEdit = qobject_cast<QLineEdit*>(editor);
            model->setData(index, lineEdit->text(), Qt::EditRole);
        } else {
            QStyledItemDelegate::setModelData(editor, model, index);
        }
    }
};

// ========== 演示窗口 ==========
class ModelViewDemo : public QWidget {
    Q_OBJECT
public:
    ModelViewDemo(QWidget *parent = nullptr) : QWidget(parent) {
        setWindowTitle("模型/视图架构演示 📋");
        setMinimumSize(800, 500);

        QVBoxLayout *mainLayout = new QVBoxLayout(this);

        // 视图选择
        QHBoxLayout *tabLayout = new QHBoxLayout();
        QLabel *viewLabel = new QLabel("视图类型:");
        tabLayout->addWidget(viewLabel);
        tabLayout->addStretch();
        mainLayout->addLayout(tabLayout);

        // 创建模型
        m_model = new ContactModel(this);

        // 创建表格视图
        m_tableView = new QTableView();
        m_tableView->setModel(m_model);
        m_tableView->setItemDelegate(new ContactDelegate(this));
        m_tableView->setSelectionBehavior(QAbstractItemView::SelectRows);  // 整行选中
        m_tableView->setAlternatingRowColors(true);
        m_tableView->horizontalHeader()->setStretchLastSection(true);
        m_tableView->setColumnWidth(0, 120);
        m_tableView->setColumnWidth(1, 150);
        m_tableView->setColumnWidth(2, 120);
        mainLayout->addWidget(m_tableView);

        // 操作按钮
        QHBoxLayout *btnLayout = new QHBoxLayout();

        QPushButton *addBtn = new QPushButton("添加联系人 ➕");
        QPushButton *delBtn = new QPushButton("删除联系人 ➖");
        QPushButton *starBtn = new QPushButton("切换星标 ⭐");
        QPushButton *sortBtn = new QPushButton("按姓名排序 🔤");

        btnLayout->addWidget(addBtn);
        btnLayout->addWidget(delBtn);
        btnLayout->addWidget(starBtn);
        btnLayout->addWidget(sortBtn);
        btnLayout->addStretch();
        mainLayout->addLayout(btnLayout);

        // 选中信息
        QLabel *infoLabel = new QLabel("选中: 无");
        mainLayout->addWidget(infoLabel);

        // 信号连接
        connect(addBtn, &QPushButton::clicked, this, &ModelViewDemo::addContact);
        connect(delBtn, &QPushButton::clicked, this, &ModelViewDemo::deleteContact);
        connect(starBtn, &QPushButton::clicked, this, &ModelViewDemo::toggleStar);
        connect(sortBtn, &QPushButton::clicked, this, &ModelViewDemo::sortByName);

        connect(m_tableView->selectionModel(), &QItemSelectionModel::selectionChanged,
                [this, infoLabel]() {
            QModelIndex current = m_tableView->currentIndex();
            if (current.isValid()) {
                Contact c = m_model->getContact(current.row());
                infoLabel->setText(QString("选中: %1 - %2 (%3)").arg(
                    c.name, c.phone, c.city));
            } else {
                infoLabel->setText("选中: 无");
            }
        });
    }

private slots:
    void addContact() {
        bool ok;
        QString name = QInputDialog::getText(this, "添加联系人", "姓名:",
                                            QLineEdit::Normal, "", &ok);
        if (!ok || name.isEmpty()) return;

        QString phone = QInputDialog::getText(this, "添加联系人", "电话:",
                                            QLineEdit::Normal, "", &ok);
        if (!ok) return;

        QString city = QInputDialog::getText(this, "添加联系人", "城市:",
                                           QLineEdit::Normal, "", &ok);
        if (!ok) return;

        m_model->addContact(name, phone, city);
    }

    void deleteContact() {
        int row = m_tableView->currentIndex().row();
        if (row >= 0) {
            Contact c = m_model->getContact(row);
            QMessageBox::StandardButton reply = QMessageBox::question(
                this, "确认删除",
                QString("确定要删除联系人 %1 吗?").arg(c.name),
                QMessageBox::Yes | QMessageBox::No);

            if (reply == QMessageBox::Yes) {
                m_model->removeContact(row);
            }
        }
    }

    void toggleStar() {
        int row = m_tableView->currentIndex().row();
        if (row >= 0) {
            QModelIndex starIndex = m_model->index(row, 3);
            m_model->setData(starIndex, !m_model->getContact(row).starred);
        }
    }

    void sortByName() {
        m_model->sort(0, Qt::AscendingOrder);
    }

private:
    ContactModel *m_model;
    QTableView *m_tableView;
};

int main(int argc, char *argv[]) {
    QApplication app(argc, argv);
    ModelViewDemo window;
    window.show();
    return app.exec();
}
```

---

## 44.7 综合实战：打造一个计算器应用

让我们用Qt打造一个功能完整的计算器，巩固所学的知识：

```cpp
#include <QApplication>
#include <QWidget>
#include <QGridLayout>
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QLabel>
#include <QPushButton>
#include <QLineEdit>
#include <QMessageBox>
#include <QFont>
#include <QPalette>
#include <QKeyEvent>

class Calculator : public QWidget {
    Q_OBJECT
public:
    Calculator(QWidget *parent = nullptr) : QWidget(parent) {
        setWindowTitle("科学计算器 🧮");
        setFixedSize(350, 500);
        setStyleSheet("background-color: #1e1e1e;");

        // ========== 主布局 ==========
        QVBoxLayout *mainLayout = new QVBoxLayout(this);
        mainLayout->setSpacing(10);
        mainLayout->setContentsMargins(15, 15, 15, 15);

        // ========== 显示区域 ==========
        // 表达式显示
        m_expressionLabel = new QLabel("");
        m_expressionLabel->setAlignment(Qt::AlignRight | Qt::AlignVCenter);
        m_expressionLabel->setStyleSheet(
            "color: #888; font-size: 16px; padding: 5px;");
        m_expressionLabel->setMinimumHeight(30);
        mainLayout->addWidget(m_expressionLabel);

        // 结果显示
        m_resultLabel = new QLabel("0");
        m_resultLabel->setAlignment(Qt::AlignRight | Qt::AlignVCenter);
        m_resultLabel->setStyleSheet(
            "color: white; font-size: 48px; font-weight: bold; "
            "background-color: #2d2d2d; border-radius: 10px; "
            "padding: 15px; margin-bottom: 10px;");
        m_resultLabel->setMinimumHeight(80);
        mainLayout->addWidget(m_resultLabel);

        // ========== 按钮区域 ==========
        QGridLayout *buttonLayout = new QGridLayout();
        buttonLayout->setSpacing(8);

        // 按钮样式定义
        QString btnStyle = R"(
            QPushButton {
                background-color: #3d3d3d;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 20px;
                font-weight: bold;
                padding: 15px;
            }
            QPushButton:hover {
                background-color: #4d4d4d;
            }
            QPushButton:pressed {
                background-color: #2d2d2d;
            }
        )";

        QString opStyle = R"(
            QPushButton {
                background-color: #ff9500;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 20px;
                font-weight: bold;
                padding: 15px;
            }
            QPushButton:hover {
                background-color: #ffaa33;
            }
            QPushButton:pressed {
                background-color: #cc7700;
            }
        )";

        QString funcStyle = R"(
            QPushButton {
                background-color: #505050;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                padding: 15px;
            }
            QPushButton:hover {
                background-color: #606060;
            }
            QPushButton:pressed {
                background-color: #404040;
            }
        )";

        // 按钮布局: [行, 列, 行跨度, 列跨度]
        // 第一行: 功能键
        createButton("C", 0, 0, 1, 2, buttonLayout, funcStyle);
        createButton("⌫", 0, 2, 1, 1, buttonLayout, funcStyle);
        createButton("÷", 0, 3, 1, 1, buttonLayout, opStyle);

        // 第二行
        createButton("7", 1, 0, 1, 1, buttonLayout, btnStyle);
        createButton("8", 1, 1, 1, 1, buttonLayout, btnStyle);
        createButton("9", 1, 2, 1, 1, buttonLayout, btnStyle);
        createButton("×", 1, 3, 1, 1, buttonLayout, opStyle);

        // 第三行
        createButton("4", 2, 0, 1, 1, buttonLayout, btnStyle);
        createButton("5", 2, 1, 1, 1, buttonLayout, btnStyle);
        createButton("6", 2, 2, 1, 1, buttonLayout, btnStyle);
        createButton("-", 2, 3, 1, 1, buttonLayout, opStyle);

        // 第四行
        createButton("1", 3, 0, 1, 1, buttonLayout, btnStyle);
        createButton("2", 3, 1, 1, 1, buttonLayout, btnStyle);
        createButton("3", 3, 2, 1, 1, buttonLayout, btnStyle);
        createButton("+", 3, 3, 1, 1, buttonLayout, opStyle);

        // 第五行
        createButton("±", 4, 0, 1, 1, buttonLayout, funcStyle);
        createButton("0", 4, 1, 1, 1, buttonLayout, btnStyle);
        createButton(".", 4, 2, 1, 1, buttonLayout, btnStyle);
        createButton("=", 4, 3, 1, 1, buttonLayout, opStyle);

        mainLayout->addLayout(buttonLayout);
    }

    // 键盘事件支持
    void keyPressEvent(QKeyEvent *event) override {
        QString key = event->text();

        if (event->key() == Qt::Key_Return || event->key() == Qt::Key_Enter) {
            onButtonClicked("=");
        } else if (event->key() == Qt::Key_Backspace) {
            onButtonClicked("⌫");
        } else if (event->key() == Qt::Key_Escape) {
            onButtonClicked("C");
        } else if (key >= "0" && key <= "9") {
            onButtonClicked(key);
        } else if (key == ".") {
            onButtonClicked(".");
        } else if (key == "+" || key == "-" || key == "*" || key == "/") {
            QString op = key;
            op.replace("*", "×").replace("/", "÷");
            onButtonClicked(op);
        }
    }

private slots:
    void onButtonClicked(const QString &text) {
        if (text == "C") {
            // 清空
            m_expression = "";
            m_currentNumber = "0";
            m_resultLabel->setText("0");
            m_expressionLabel->setText("");
            m_lastResult = 0;
            m_waitingForOperand = false;
        }
        else if (text == "⌫") {
            // 退格
            if (!m_waitingForOperand && !m_currentNumber.isEmpty()) {
                m_currentNumber.chop(1);
                if (m_currentNumber.isEmpty() || m_currentNumber == "-") {
                    m_currentNumber = "0";
                }
                displayResult();
            }
        }
        else if (text == "±") {
            // 正负切换
            if (m_currentNumber.startsWith("-")) {
                m_currentNumber = m_currentNumber.mid(1);
            } else if (m_currentNumber != "0") {
                m_currentNumber = "-" + m_currentNumber;
            }
            displayResult();
        }
        else if (text == ".") {
            // 小数点
            if (m_waitingForOperand) {
                m_currentNumber = "0";
                m_waitingForOperand = false;
            }
            if (!m_currentNumber.contains(".")) {
                m_currentNumber += ".";
                displayResult();
            }
        }
        else if (text == "+" || text == "-" || text == "×" || text == "÷") {
            // 运算符
            double operand = m_currentNumber.toDouble();

            if (!m_pendingOperator.isEmpty()) {
                // 计算之前的表达式
                double result = calculate(m_lastResult, operand, m_pendingOperator);
                m_currentNumber = QString::number(result, 'g', 15);
                m_lastResult = result;
                displayResult();
            } else {
                m_lastResult = operand;
            }

            m_pendingOperator = text;
            m_expression = QString::number(m_lastResult, 'g', 15) + " " + text;
            m_expressionLabel->setText(m_expression);
            m_waitingForOperand = true;
        }
        else if (text == "=") {
            // 计算结果
            if (!m_pendingOperator.isEmpty()) {
                double operand = m_currentNumber.toDouble();
                double result = calculate(m_lastResult, operand, m_pendingOperator);

                m_expression = QString::number(m_lastResult, 'g', 15) + " " +
                              m_pendingOperator + " " +
                              QString::number(operand, 'g', 15) + " =";
                m_expressionLabel->setText(m_expression);

                m_currentNumber = QString::number(result, 'g', 15);
                displayResult();

                m_lastResult = result;
                m_pendingOperator.clear();
                m_waitingForOperand = true;
            }
        }
        else if (text >= "0" && text <= "9") {
            // 数字
            if (m_waitingForOperand) {
                m_currentNumber = text;
                m_waitingForOperand = false;
            } else {
                if (m_currentNumber == "0") {
                    m_currentNumber = text;
                } else {
                    m_currentNumber += text;
                }
            }
            displayResult();
        }
    }

private:
    double calculate(double a, double b, const QString &op) {
        if (op == "+") return a + b;
        if (op == "-") return a - b;
        if (op == "×") return a * b;
        if (op == "÷") return (b != 0) ? a / b : 0;
        return b;
    }

    void displayResult() {
        // 格式化显示
        double value = m_currentNumber.toDouble();
        QString display;

        if (qAbs(value) >= 1e10 || (qAbs(value) < 1e-6 && value != 0)) {
            display = QString::number(value, 'e', 8);
        } else {
            display = QString::number(value, 'f', 8);
            // 移除尾部零
            while (display.contains(".") && display.endsWith("0")) {
                display.chop(1);
            }
            if (display.endsWith(".")) display.chop(1);
        }

        m_resultLabel->setText(display);
    }

    void createButton(const QString &text, int row, int col,
                     int rowSpan, int colSpan,
                     QGridLayout *layout, const QString &style) {
        QPushButton *button = new QPushButton(text);
        button->setMinimumSize(0, 50);
        layout->addWidget(button, row, col, rowSpan, colSpan);
        button->setStyleSheet(style);
        connect(button, &QPushButton::clicked, [this, text]() {
            onButtonClicked(text);
        });
    }

    QLabel *m_expressionLabel;
    QLabel *m_resultLabel;
    QString m_currentNumber = "0";
    QString m_expression;
    QString m_pendingOperator;
    double m_lastResult = 0;
    bool m_waitingForOperand = false;
};

int main(int argc, char *argv[]) {
    QApplication app(argc, argv);
    Calculator window;
    window.show();
    return app.exec();
}
```

---

## 44.8 本章小结

本章我们一起探索了C++ GUI编程的精彩世界，让我们来回顾一下学到的知识点：

### 核心概念

1. **事件驱动编程**：GUI程序与命令行程序最大的区别在于控制流——GUI程序等待用户的动作（事件），然后做出响应。这种范式要求程序员换一种思维方式。

2. **信号与槽机制**：Qt框架的核心创新，通过`signals`和`slots`实现对象间的松耦合通信，比传统的回调函数更加类型安全且易于维护。

3. **模型/视图架构**：将数据（模型）、展示（视图）和交互（控制器）分离，使得处理大量数据变得优雅而高效。

### Qt框架要点

| 模块 | 用途 |
|------|------|
| `Qt Core` | 核心功能（信号槽、元对象系统） |
| `Qt Widgets` | 经典桌面GUI组件 |
| `Qt GUI` | 低级图形绘制 |
| `Qt Network` | 网络编程 |
| `Qt SQL` | 数据库访问 |
| `Qt Multimedia` | 音频视频处理 |

### 常用控件一览

- **按钮**：`QPushButton`、`QRadioButton`、`QCheckBox`、`QToolButton`
- **输入**：`QLineEdit`、`QTextEdit`、`QSpinBox`、`QSlider`、`QComboBox`
- **容器**：`QTabWidget`、`QGroupBox`、`QStackedWidget`、`QSplitter`
- **展示**：`QLabel`、`QTableWidget`、`QTreeWidget`、`QListWidget`

### 布局管理

```cpp
QVBoxLayout *vbox = new QVBoxLayout();   // 垂直排列
QHBoxLayout *hbox = new QHBoxLayout();   // 水平排列
QGridLayout *grid = new QGridLayout();   // 网格排列
QFormLayout *form = new QFormLayout();   // 表单排列
```

### 绘图三要素

1. **QPainter**：画家，负责绘制
2. **QPen**：画笔，决定线条样式
3. **QBrush**：画刷，决定填充样式

### 学习建议

- **多动手**：GUI编程，光看不练等于没学
- **看文档**：Qt的官方文档是学习Qt最好的资源
- **模仿**：从简单的界面开始，逐步增加复杂度
- **调试**：善用`qDebug()`输出调试信息

### 继续探索的方向

- **Qt Quick/QML**：声明式UI，适合现代跨平台应用
- **Qt Quick Controls 2**：Material Design风格的组件
- **QML和C++混合编程**：发挥两者各自的优势
- **平台特定API**：如Windows的Win32、macOS的Cocoa

> 🎓 "GUI编程就像烹饪——你知道再多的菜谱，如果不亲自下厨，永远做不出美味佳肴。拿起你的Qt锅铲，开始烹饪吧！"

```cpp
// 本章终极彩蛋：一句代码启动Qt应用
// 学会了这些，你已经从"Hello World"级别的程序员
// 进化成了"Hello GUI"级别的程序员！
// 继续加油，桌面应用开发者！💪

QApplication app(argc, argv);
// 接下来... 就是你的表演了！
```

---

*本章结束，愿你的按钮永远有点击响应，你的窗口永远在最前面！* 🎉
