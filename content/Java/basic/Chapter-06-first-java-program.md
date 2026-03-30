+++
title = "第6章 第一个 Java 程序与代码结构"
weight = 60
date = "2026-03-30T14:33:56.881+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++
# 第六章 第一个 Java 程序与代码结构

> "Talk is cheap, show me the code." — 这句话在 Java 世界里尤其正确。再多理论也比不上亲手跑通一个程序带来的成就感。准备好了吗？让我们从那句经典的 `Hello World` 开始，正式踏入 Java 的大门。

---

## 6.1 Hello World 完整解析——逐行讲解每一句代码

让我们先来看一个完整可运行的 Java 程序，然后像拆解精密机械一样，一行一行地剖析它。

```java
public class HelloWorld {
    public static void main(String[] args) {
        // 在屏幕上打印 Hello World
        System.out.println("Hello World");
    }
}
```

把它保存为 `HelloWorld.java`，然后在命令行执行：

```bash
javac HelloWorld.java   # 编译
java HelloWorld         # 运行
```

输出结果：

```
Hello World
```

恭喜！你刚刚完成了一个 Java 程序的编译和运行。不过，你真的理解每一行代码的含义了吗？让我们继续往下拆解。

### 6.1.1 `public class HelloWorld { }` 是什么意思？

这一行声明了一个**类**（class）。类是什么？你可以把它想象成一个"容器"，用来装代码。在 Java 的世界里，**一切皆为对象**，而类就是对象的蓝图（blueprint）。

- `public`：这是**访问修饰符**（access modifier），表示这个类是"公开的"，谁都可以用。没有这个关键字的话，类就只能被同包的代码访问。
- `class`：关键字，告诉编译器"我要定义一个类"。
- `HelloWorld`：类的名字。这个名字可不是随便起的——Java 规定，**类名必须和文件名一致**，否则编译会报错（关于这条规则，我们会在 6.2.2 节详细说）。

所以，`public class HelloWorld { }` 的意思是："我要定义一个公开的类，名字叫 HelloWorld，它的内容用一对花括号包裹。"

> 💡 **类命名规范**：类名采用 **PascalCase** 风格，即每个单词的首字母大写，如 `HelloWorld`、`MyFirstProgram`、`AccountService`。

### 6.1.2 `public static void main(String[] args) { }` 每一部分的作用

这一行是整个 Java 程序的**入口**（entry point）。程序运行时，JVM（Java 虚拟机）会从 `main` 方法开始执行。没有 `main` 方法？程序根本不知道该从哪里开始！

让我们逐个拆解这行代码的每个组成部分：

```java
public static void main(String[] args)
```

| 组成部分 | 含义 | 作用 |
|---|---|---|
| `public` | 访问修饰符 | 告诉 JVM，这个方法任何代码都可以调用 |
| `static` | 静态关键字 | 表示这个方法属于类本身，而不是某个对象；JVM 可以直接通过类名调用，无需先创建对象 |
| `void` | 返回类型 | 表示这个方法执行完毕后不返回任何值 |
| `main` | 方法名 | JVM 规定死了的名字，必须是 `main` |
| `String[] args` | 参数 | 接收命令行传入的字符串数组 |

> 💡 **为什么 `main` 必须是 `static`？** 因为 JVM 在启动程序时，还没有创建任何对象。如果 `main` 不是静态的，JVM 就得先实例化一个对象才能调用 `main`——但这本身就需要先执行 `main`！这是一个"先有鸡还是先有蛋"的问题。`static` 关键字打破了这一僵局，让 JVM 可以在不创建对象的情况下直接运行代码。

### 6.1.3 `System.out.println("Hello World");` 怎么工作的？

这行代码干了一件核心的事：在屏幕上打印一行文字。

我们来分解它：

```
System.out.println("Hello World");
```

- `System`：Java 标准库提供的类，代表系统运行环境。
- `.`（点操作符）：用来访问对象（或类）内部的属性和方法。
- `out`：System 类的一个静态属性，它是一个**输出流**对象，指向标准输出（通常是你的屏幕）。
- `println`：这个方法的名字是 "print line" 的缩写，意思是"打印这一行"。每调用一次，会在输出后面加一个换行符（`\n`），这样下一次打印会从新的一行开始。
- `"Hello World"`：要打印的字符串内容，用**双引号**包裹。引号内的内容会原样输出，不会被当作代码处理。

如果你不想换行，可以用 `print`（没有 `ln`）：

```java
System.out.print("Hello ");
System.out.print("World");
```

输出：`Hello World`（不换行，两个词连在一起）

> 💡 **还有 `printf`？** 是的，类似 C 语言的格式化输出：`System.out.printf("我的名字是 %s，年龄是 %d%n", "张三", 25);` 其中 `%s` 表示字符串占位符，`%d` 表示整数占位符，`%n` 是跨平台的换行符（在 Windows 上输出 `\r\n`，在 Linux/Mac 上输出 `\n`）。

### 6.1.4 `args` 参数是干什么的？

`String[] args` 是 `main` 方法接收外部参数的入口。

当你从命令行运行程序时，可以附加一些额外的信息：

```bash
java HelloWorld Alice 2024
```

这些信息（`Alice` 和 `2024`）会被当作**字符串数组**存入 `args` 参数中。

```java
public class CommandLineDemo {
    public static void main(String[] args) {
        // 打印传入的所有参数
        for (int i = 0; i < args.length; i++) {
            System.out.println("第 " + i + " 个参数: " + args[i]);
        }
    }
}
```

运行 `java CommandLineDemo Alice 2024`，输出：

```
第 0 个参数: Alice
第 1 个参数: 2024
```

> 💡 **小技巧**：`args` 这个名字是可以改的，比如 `String[] arguments` 或者 `String[] argv`，但 `args` 是 Java 社区约定俗成的惯例。参数名字无关紧要，关键是它的类型 `String[]`。

---

## 6.2 Java 代码的基本规则——这些规则必须遵守

Java 是一门"强规则"语言。编译器（compiler）是一个极度较真的裁判——你少写一个分号，它就罢工；你大小写写错了，它就报错。理解这些规则，是写好 Java 代码的第一步。

### 6.2.1 Java 是大小写敏感的语言——`String` 和 `string` 不一样！

Java 对大小写**极其敏感**。这意味着：

- `String` 是一个合法的类名（Java 标准库中的字符串类）
- `string` 编译器压根不认识，会报 `cannot find symbol` 错误
- `System` 和 `system` 是完全不同的东西

```java
// 正确
String name = "Java";
System.out.println(name);

// 错误！编译报错
string name = "Java";  // ❌ cannot find symbol
system.out.println(name);  // ❌ cannot find symbol
```

> ⚠️ **新手最容易踩的坑之一**：很多语言对大小写比较宽容（比如 PHP、JavaScript 的某些场景），但 Java 不一样。变量名、方法名、类名，每一个字符的大小写都要写对。建议在写代码时开启 IDE（集成开发环境，如 IntelliJ IDEA 或 VS Code）的实时错误提示，能帮你第一时间发现这类问题。

### 6.2.2 类名必须和文件名一致——HelloWorld.java

在 Java 中，**如果一个类是 public（公开的），它必须保存在与类名同名的文件中**。

- 类名 `HelloWorld` → 文件名 `HelloWorld.java`
- 类名 `MyFirstProgram` → 文件名 `MyFirstProgram.java`

```java
// 文件名：HelloWorld.java
public class HelloWorld {
    // ...
}
```

如果文件名和类名不匹配，编译直接报错：

```plaintext
HelloWorld.java:1: error: class HelloWorld is public, should be declared in a file named HelloWorld.java
public class HelloWorld {
       ^
```

> 💡 **那一个 .java 文件里可以有多个类吗？** 可以！但至多只能有一个 `public` 类，且 `public` 类的名字必须和文件名一致。其他非 `public` 的类可以随意命名（虽然不推荐）。详细内容见 6.2.5 节。

### 6.2.3 每条语句以分号结尾——忘了分号会怎样？

在 Java 中，**几乎所有的语句都必须以分号（`;`）结尾**。分号是编译器的"句子结束标志"，告诉它"这句话说完了"。

```java
int age = 25;        // ✅ 正确
int score = 100      // ❌ 编译错误：需要 ';' （missing ';'）
```

漏写分号是最常见的初学者错误之一。好消息是，IDE 会用红色波浪线标出这类错误，一目了然。

> 💡 **例外情况**：方法声明、条件语句、循环语句等结构化语句的结尾不需要分号，因为它们以 `{ }` 结束。但这些结构内部的**具体操作语句**仍然需要分号。

### 6.2.4 代码块用花括号 `{ }` 包裹——Python 用缩进，Java 用括号

Java 使用**花括号** `{}` 来划分代码块（code block），而不是依赖缩进。

```java
public class BraceDemo {
    public static void main(String[] args) {
        if (true) {
            // if 语句的代码块
            System.out.println("条件为真，执行这里");
        } // ← 右花括号后面不需要分号

        for (int i = 0; i < 3; i++) {
            System.out.println("第 " + i + " 次循环");
        }
    }
}
```

对比 Python（使用缩进）：

```python
# Python 用缩进来区分代码块
if True:
    print("条件为真")
    for i in range(3):
        print(f"第 {i} 次循环")
```

> 💡 **两种风格各有优劣**：Java 的 `{}` 风格更显式，即使代码缩进乱了，逻辑结构依然清晰；Python 的缩进风格更简洁，但一旦缩进出错，程序逻辑就乱了。**无论哪种风格，保持一致的缩进都是良好编程习惯。**

### 6.2.5 一个 .java 文件可以有多个类——但 public 类只能有一个

Java 允许在一个 `.java` 文件中定义多个类，但这背后有一套规则：

```java
// 文件名：Company.java

public class Company {
    // 公开类，文件名必须是 Company.java
}

class Employee {
    // 包级私有类，文件内可以任意命名
}

class Department {
    // 另一个包级私有类
}
```

规则总结：

| 条件 | 规则 |
|---|---|
| `public` 类 | **最多只能有一个**，且文件名必须与此类名一致 |
| 非 `public` 类 | 可以有任意多个，类名不需要和文件名一致 |
| `public` 类 | 整个包（package）内可见 |
| 非 `public` 类 | 仅在同一文件内可见（类似"文件私有"的含义） |

> 💡 **实际建议**：虽然在技术上允许，但**强烈不推荐**在一个文件中放多个类。这会让代码难以维护，降低可读性。最佳实践是：**一个 `.java` 文件，一个 `public` 类，类名即文件名。**

### 6.2.6 Java 的入口是 main 方法

当你在命令行输入 `java HelloWorld` 时，JVM 会启动，查找 `HelloWorld` 类中签名为以下的方法：

```java
public static void main(String[] args)
```

然后从这一行开始执行代码。**没有 `main` 方法，程序无法独立运行**（除非通过其他方式调用，比如单元测试框架，但那属于特例）。

> ⚠️ **注意**：`main` 方法的签名必须完全一致，包括大小写、`String` 而非 `string`、`args` 变量名可改但类型不能变。以下都是错误的：
> - `public static void Main(String[] args)` — `Main` 不是 `main`，JVM 不认
> - `public void main(String[] args)` — 缺少 `static`，JVM 找不到入口
> - `public static void main()` — 缺少参数 `String[] args`，不匹配

---

## 6.3 Java 注释的写法——给自己和同伴留的便签

代码是写给人看的，顺便给机器执行。注释（comment）是你留给未来自己和其他开发者的便签——提醒"这里为什么这么做"。

### 6.3.1 单行注释：`// 这里写注释`

用双斜杠 `//` 开头的注释，只对当前行有效。

```java
int year = 2024;  // 声明一个变量，表示年份

// 以下代码计算圆的面积
double radius = 5.0;
double area = Math.PI * radius * radius;
```

> 💡 **快捷键**：在 IntelliJ IDEA / Android Studio 中，选中一行或多行代码，按 `Ctrl + /` 可以快速添加或移除单行注释。

### 6.3.2 多行注释：`/* 多行注释 */`

用 `/*` 开始，用 `*/` 结束，中间可以跨越多行。

```java
/*
 * 这是一个多行注释示例
 * 通常用于：
 *   - 方法的功能说明
 *   - 复杂的业务逻辑解释
 *   - 临时禁用某段代码（注释掉）
 */
public class MultiLineComment {
    public static void main(String[] args) {
        System.out.println("多行注释常用于大段说明");
    }
}
```

> 💡 **IDE 自动补全**：输入 `/*` 后按回车，很多 IDE 会自动补上 `*` 并换行，让你的多行注释看起来整齐美观。

### 6.3.3 文档注释：`/** 这是文档注释，可以生成 API 文档 */`

以 `/**` 开头的是**文档注释**（Javadoc），这是 Java 特有的注释格式。工具可以提取这种注释，生成 API 文档网页。

```java
/**
 * 计算两个整数的和。
 *
 * @param a 第一个整数
 * @param b 第二个整数
 * @return 两个整数的和
 */
public static int add(int a, int b) {
    return a + b;
}
```

> 💡 **Javadoc 生成**：在命令行运行 `javadoc YourClass.java`，就会生成一份 HTML 格式的 API 文档（当然，实际项目中通常用 Maven/Gradle 的插件自动生成）。

### 6.3.4 好的注释应该怎么写？——注释是解释"为什么"，不是解释"是什么"

这是最容易被忽视但最重要的一条原则。

**❌ 糟糕的注释（解释"是什么"）：**

```java
// 将 count 加 1
count++;

// 声明一个字符串变量 name
String name = "Alice";
```

这类注释是在"翻译代码"，等于把 `count++` 用自然语言重复了一遍。代码本身已经很清楚了，注释只是噪音。

**✅ 好的注释（解释"为什么"）：**

```java
// 由于历史原因，第三方接口要求这里必须 +1
// 具体 issue 参见：https://github.com/example/project/issues/123
count++;

// 使用 name 而非 username，因为这是旧数据库字段名，新系统迁移后应改回 username
String name = getLegacyField("username");
```

好的注释回答的是：**为什么要这样做？有什么特殊原因？有什么坑？**

> 💡 **另一个好建议**：当你发现需要写很多注释来解释代码时，先问问自己——能不能把代码写得**自解释**（self-explanatory）？比如，把魔法数字（magic number）提取成命名常量：
>
> ```java
> // 差的写法：魔法数字
> if (score > 86400) { ... }
>
> // 好的写法：命名常量
> final int SECONDS_PER_DAY = 86400;
> if (score > SECONDS_PER_DAY) { ... }
> ```
>
> 命名良好的变量和方法比长篇注释更有价值。

---

## 6.4 Java 代码的缩进与格式化

代码的可读性很大程度上取决于格式是否规范。整齐的代码让人读起来舒服，出错率也更低。

### 6.4.1 标准的 4 空格缩进

在 Java 社区中，**每嵌套一层代码块，缩进 4 个空格**是约定俗成的标准。

```java
public class IndentDemo {
    public static void main(String[] args) {
        for (int i = 0; i < 3; i++) {
            if (i == 1) {
                System.out.println("i 等于 1 时打印这条信息");
            } else {
                System.out.println("i 不等于 1");
            }
        }
    }
}
```

> ⚠️ **空格还是 Tab？** 很多团队规定使用空格而非 Tab 字符（Tab），因为不同编辑器和终端对 Tab 的显示宽度可能不一致（有的显示为 4 格，有的显示为 8 格）。**统一使用 4 个空格**可以确保所有环境下代码看起来一致。在 IntelliJ IDEA 中，可以设置 `Tab` 键自动插入 4 个空格。

### 6.4.2 IDEA 格式化快捷键 Ctrl+Alt+L

如果你使用的是 IntelliJ IDEA（或 Android Studio），最方便的做法是：**先随便写，格式的事最后交给 IDE**。

选中代码或整个文件，按下 `Ctrl + Alt + L`（Windows/Linux）或 `Cmd + Option + L`（Mac），IDE 会自动帮你把代码格式化得整整齐齐——缩进修正、空格规范化、换行合理化。

> 💡 **建议**：在提交代码前（无论是 Git commit 还是 Code Review），务必格式化一遍代码。这样团队中每个人看到的代码格式都一致，Review 时不会被格式问题分散注意力。可以在 IDEA 中设置"保存时自动格式化"（Settings → Tools → Actions on Save → Reformat code）。

---

## 本章小结

本章我们从经典的 `Hello World` 程序出发，详细拆解了 Java 代码的各个组成部分：

- **`public class HelloWorld`**：以 `public` 类为基本单元组织代码，类名即文件名。
- **`public static void main(String[] args)`**：程序入口方法，`static` 让 JVM 无需实例化即可调用，参数 `args` 接收命令行输入。
- **`System.out.println("...")`**：向标准输出打印文字，`println` 会自动换行。
- **大小写敏感、类名文件名对应、分号结尾、`{}` 划分代码块**等基本规则，是 Java 编译器强制要求的硬性规定，务必牢记。
- **注释的三种写法**（`//`、`/* */`、`/** */`），注释的价值在于解释"为什么"而非"是什么"。
- **4 空格缩进 + IDE 格式化**，保持代码美观整洁是基本职业素养。

学到这里，你已经具备了阅读和编写最简单 Java 程序的能力。下一章，我们将学习 Java 中的**变量、数据类型和运算符**——程序的核心"原材料"。
