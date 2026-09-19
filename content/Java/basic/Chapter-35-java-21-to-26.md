+++
title = "第35章 Java 21～26 新特性全景"
weight = 350
date = "2026-03-30T14:33:56.919+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++
# 第三十五章 Java 21～26 新特性全景

> "Java 21 是继 Java 8 之后最重要的 LTS（长期支持版）版本，没有之一。" —— 当你第一次用虚拟线程跑满一万并发的时候，你就会明白这句话的分量。

从 2023 年 9 月 Java 21 正式发布，到 2026 年 3 月 Java 26 呱呱坠地，Java 这门"老语言"迎来了史上最密集的现代化改造。这三年里，我们见证了虚拟线程正式转正、字符串模板从预览走向**被撤回**、Scoped Values 一路预览到 Java 25 才转正、结构化并发至今仍在预览……每一项都值得了解，其中不少还带着"别急着上生产"的标签。

> ⚠️ **读这一章前请记住一句话**：Java 的**预览特性**（preview feature）默认是关着的，要用 `--enable-preview` 才能编译运行，而且**随时可能改语法、甚至被删掉**。本章会明确标注每个特性的当前状态，避免你照着写却在项目里编译不过。

本章，我们就来一次**新特性全景巡礼**，把 Java 21～26 中那些真正值得你花时间了解的特性讲透。

## 特性发布时间线

在开始之前，先来看一张总览图：

```mermaid
timeline
    title Java 21~26 特性演进（含预览状态）
    2023-09 : Java 21（LTS）
            : 虚拟线程 JEP 444 正式
            : switch 模式匹配 JEP 441 正式
            : Record Patterns JEP 440 正式
            : 字符串模板 JEP 430 预览一
            : Scoped Values / 结构化并发 / 隐式声明类 均首次预览
    2024-03 : Java 22
            : FFM API JEP 454 正式
            : 未命名变量与模式 JEP 456 正式
            : 字符串模板 JEP 459 预览二
            : Stream Gatherers JEP 461 首次预览
    2024-09 : Java 23
            : 字符串模板 JEP 465 被撤回
            : 模块导入声明 JEP 476 预览一
            : Markdown 文档注释 JEP 467 转正
            : Gatherers / Scoped Values / 结构化并发 各自再预览一轮
    2025-03 : Java 24
            : Stream Gatherers JEP 485 转正
            : Class-File API JEP 484 转正
            : 虚拟线程去固定 JEP 491
            : Scoped Values、结构化并发仍为预览
    2025-09 : Java 25（LTS）
            : Scoped Values JEP 506 转正
            : 紧凑源文件与实例 main JEP 512 转正
            : 模块导入声明 JEP 511 转正
            : 结构化并发 JEP 505 第五次预览
    2026-03 : Java 26
            : 结构化并发 JEP 525 第六次预览
            : 惰性常量 JEP 526 第二次预览
            : HTTP/3 JEP 517
            : Applet API 正式移除 JEP 504
```

> 📌 **什么是 LTS？** LTS 是 "Long-Term Support"（长期支持版）的缩写，Oracle 等厂商会提供多年的安全更新。**目前的 LTS 是 Java 25（2025 年 9 月发布），上一个 LTS 是 Java 21**；两者之间（22、23、24）和之后的 26、27 都是"半年一版"的非 LTS 版本。

下面，让我们逐一拆解这些特性。

---

## 35.1 虚拟线程正式发布

### 35.1.1 概念解释：什么是虚拟线程？

**虚拟线程（Virtual Threads）** 是 Java 21 最大的明星，也是 JVM 历史上最重要的并发模型革新。它的 JEP 编号是 JEP 444，属于正式版特性（不是预览）。

在说虚拟线程之前，先回忆一下传统的线程模型。我们知道，Java 的并发基础是 `Thread`。每当你 new 一个 `Thread`，JVM 就会在操作系统层面创建一个真实的线程（也叫**平台线程 / Platform Thread**）。平台线程和 OS 线程是一一对应的，**一个线程大约占用 1MB（1～2MB）的堆外内存**，而且创建和切换成本都很高。

这就导致了两个经典问题：

- **电商大促时**：假设你有 10000 个并发用户，用平台线程的话，你需要 10000 个 OS 线程——光内存就要用掉 10GB+，这还没算上下文切换的开销，CPU 全耗在切换上了。
- **BIO 阻塞时**：在传统的同步 I/O 模型下，一个线程在等待数据库返回结果时会**一直阻塞**，占着坑不干活，白白浪费资源。

虚拟线程的出现，就是为了解决这两个问题。

**虚拟线程**是 JVM 层面的轻量级线程，它**不直接对应 OS 线程**。多个虚拟线程会"搭乘"少量的平台线程（也叫**载体线程 / Carrier Thread**）来运行。打个比方：

- **平台线程** = 公交车
- **虚拟线程** = 乘客
- 一个公交车可以坐很多乘客（虚拟线程）
- 当某个乘客在等红灯（I/O 等待）时，公交车可以换下一个乘客上车

虚拟线程的**内存占用大约只有 200～300 字节**，而不是 1MB。这意味着你可以轻松创建**数百万个**虚拟线程。

### 35.1.2 第一个示例：Hello 虚拟线程

创建虚拟线程非常简单，和创建普通线程几乎一样：

```java
// Chapter35VirtualThreads.java
public class Chapter35VirtualThreads {

    public static void main(String[] args) {
        // 使用 Thread.ofVirtual() 创建虚拟线程
        Thread virtualThread = Thread.ofVirtual()
                .name("my-virtual-thread")
                .start(() -> {
                    // 这是一个虚拟线程
                    System.out.println("我是虚拟线程，我运行了！");
                    System.out.println("我的线程名: " + Thread.currentThread());
                });

        // 等待虚拟线程结束
        try {
            virtualThread.join();
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            System.err.println("线程被中断了");
        }

        System.out.println("主线程也完成了");
    }
}
```

运行这段代码（需要 Java 21+）：

```
我是虚拟线程，我运行了！
我的线程名: Thread[#30/my-virtual-thread,1,CarrierThreads]
主线程也完成了
```

注意看输出中的 `CarrierThreads` —— 这说明虚拟线程运行在载体线程上。

### 35.1.3 百万并发不是梦

这是虚拟线程最震撼的演示——创建 10000 个虚拟线程同时执行 I/O 操作：

```java
// Chapter35VirtualThreadsMillion.java
import java.time.Duration;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class Chapter35VirtualThreadsMillion {

    public static void main(String[] args) throws InterruptedException {
        int count = 10000;  // 创建 10000 个虚拟线程
        System.out.println("开始创建 " + count + " 个虚拟线程...");

        long start = System.currentTimeMillis();

        try (ExecutorService executor = Executors.newVirtualThreadPerTaskExecutor()) {
            // 为每个任务创建一个虚拟线程
            for (int i = 0; i < count; i++) {
                final int taskId = i;
                executor.submit(() -> {
                    // 模拟 I/O 操作：sleep 模拟网络请求
                    try {
                        Thread.sleep(Duration.ofSeconds(1));
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                    }
                    return "任务 " + taskId + " 完成";
                });
            }
            // 所有任务提交完毕，executor 关闭后自动等待完成
        } // executor 关闭后，所有虚拟线程任务完成

        long duration = System.currentTimeMillis() - start;
        System.out.println(count + " 个任务全部完成，耗时: " + duration + "ms");
        // 如果用平台线程，10000 个线程同时运行几乎不可能；
        // 虚拟线程则可以轻松应对，因为它们共享少量载体线程
    }
}
```

输出类似：

```
开始创建 10000 个虚拟线程...
10000 个任务全部完成，耗时: 1072ms
```

> 🔑 **关键点**：这 10000 个任务"同时"Sleep 了 1 秒，但整个程序只用了约 1 秒多就完成了。这意味着数千个虚拟线程**同时挂起**，而只用了很少的载体线程（可能只有几个 CPU 核心数那么多）。这就是虚拟线程的威力：**以极低的资源开销，实现极高的并发量**。

### 35.1.4 虚拟线程 vs 平台线程：核心对比

| 特性 | 平台线程 | 虚拟线程 |
|------|---------|---------|
| 创建成本 | 高（约 1MB 内存） | 低（约 200～300 字节） |
| 创建速度 | 慢 | 快 |
| 并发数量上限 | 数百到数千 | 数万到数百万 |
| 与 OS 线程的关系 | 一一对应 | 多路复用多个载体线程 |
| 是否需要修改现有代码 | — | 几乎不需要（同步代码自动受益） |
| `ThreadLocal` 支持 | 完整支持 | 支持，但需注意生命周期 |

### 35.1.5 注意事项：这些坑不要踩！

虚拟线程虽好，但有几个**禁忌**，踩了性能反而更差：

1. **禁止在线程池中使用虚拟线程**：不要把虚拟线程提交给 `Executors.newFixedThreadPool()` 或 `ForkJoinPool`，这叫"反向套娃"。应该用 `Executors.newVirtualThreadPerTaskExecutor()` —— 每个任务一个虚拟线程。
2. **禁止对虚拟线程使用 `Thread.stop()`/`Thread.suspend()` 等老旧 API**：这些 API 压根就不支持虚拟线程。
3. **`ThreadLocal` 使用要谨慎**：如果每个虚拟线程都需要独立的 ThreadLocal 值，内存开销会变大。Java 22 引入的 **Scoped Values** 专门解决了这个问题。

---

## 35.2 String Templates（字符串模板）——已被 Java 撤回

> ❌ **先说最重要的事**：字符串模板**最终没有被 Java 采纳**。它在 Java 21 以 JEP 430 预览、Java 22 以 JEP 459 第二次预览，原计划在 Java 23 第三次预览并转正的 JEP 465 **被撤回（Withdrawn）**。今天的正式版 JDK（包括 25、26）里，`java.lang.StringTemplate` 这个类型**根本不存在**——你在网上看到的 `STR."..."` 写法，现在在任何正式版 JDK 上都编译不过。

### 35.2.1 它当初想解决什么问题？

Java 拼字符串经历过三个阶段：

1. **`+` 号拼接**：`"Hello " + name + "，年龄 " + age`，可读性差、括号容易漏。
2. **`String.format()` / `MessageFormat`**：比 `+` 好一点，但插值位置不直观。
3. **`StringBuilder`**：性能好，但 `append` 一大堆，写起来啰嗦。

字符串模板想用 `\{...}` 插值配合"模板处理器"，一次性解决类型安全、可读性和转义问题——目标很好，但设计反馈不佳，最终被撤回。

### 35.2.2 历史语法长什么样（仅作考古，编译不过）

```java,ignore
// ⚠️ 这段是历史资料：JDK 23 起该特性已被撤回。
//    在任何正式版 JDK 上都会报错（找不到 STR，或者 illegal escape character）。
public class Chapter35StringTemplates {
    public static void main(String[] args) {
        String name = "阿柴";
        int age = 18;

        // Java 21 的预览写法：STR 是内置的"模板处理器"
        String s = STR."""
                姓名: \{name}
                年龄: \{age}
                """;
        System.out.println(s);
    }
}
```

`STR` 是当时的字符串处理器，`FMT` 负责格式化，`RAW` 什么都不做；`StringTemplate` 是模板对象，可以取到 `fragments()`（字面片段）和 `values()`（插值结果）。这套 API 现在都用不上了。

### 35.2.3 今天应该怎么写？

老老实实用回久经考验的 API（下面这段在 JDK 25 上可以直接跑）：

```java
// Chapter35StringAlternatives.java
public class Chapter35StringAlternatives {

    public static void main(String[] args) {
        String name = "阿柴";
        int age = 18;
        double score = 98.765;

        // 1) 最常用：String.format / String::formatted
        String s1 = String.format("姓名: %s，年龄: %d，成绩: %.2f", name, age, score);
        String s2 = "姓名: %s，年龄: %d".formatted(name, age);
        System.out.println(s1);
        System.out.println(s2);

        // 2) 多行模板：文本块 + formatted，最舒服的写法
        String s3 = """
                姓名: %s
                年龄: %d
                两年后: %d
                """.formatted(name, age, age + 2);
        System.out.println(s3);

        // 3) 需要位置参数或本地化时，用 MessageFormat
        String s4 = java.text.MessageFormat.format("你好，{0}！你今年 {1} 岁。", name, age);
        System.out.println(s4);
    }
}
```

输出：

```text
姓名: 阿柴，年龄: 18，成绩: 98.77
姓名: 阿柴，年龄: 18
姓名: 阿柴
年龄: 18
两年后: 20

你好，阿柴！你今年 18 岁。
```

> 💡 文本块里以 `%` 开头的格式串要注意：文本块本身不做格式化，必须显式调用 `.formatted(...)` 或 `String.format(...)` 才会替换占位符。

### 35.2.4 那"安全拼 SQL"怎么办？

字符串模板主打的卖点之一是"把用户输入安全地拼进 SQL"。它没了之后，旧办法依然可靠：

- **首选**：用 `PreparedStatement` 的占位符 `?`，值永远走参数绑定，不进 SQL 文本；
- **表名/列名**这类不能用占位符的地方，用**白名单校验**（只允许事先约定好的几个标识符）；
- 权限上再收一道：数据库账号只给最小权限，别用 root。

> 📌 **小结**：字符串模板属于 Java 的"被撤回的尝试"，不必学它的语法。日常拼字符串用 `String.format` / `formatted()` / 文本块，拼 SQL 用 `PreparedStatement`。

## 35.3 Pattern Matching for switch 正式版

### 35.3.1 从枚举到模式匹配

`switch` 语句在 Java 中历史悠久，但一直有个痛点：**只能匹配常量**，不能匹配更复杂的条件。

```java
// 传统 switch：只能匹配常量
switch (day) {
    case MONDAY, FRIDAY, SUNDAY -> System.out.println("6点");
    case TUESDAY -> System.out.println("7点");
    // ...
}
```

Pattern Matching for switch（JEP 441）将**模式匹配**和 `switch` 结合起来，让 `case` 不再局限于常量，而是可以匹配**类型、范围、甚至是带条件的模式**。

### 35.3.2 模式匹配基础用法

```java
// Chapter35PatternMatchingSwitch.java
public class Chapter35PatternMatchingSwitch {

    public static void main(String[] args) {
        Object[] values = {
                42,
                3.14159,
                "Hello",
                true,
                null,
                'X',
                new int[]{1, 2, 3}
        };

        for (Object value : values) {
            String result = switch (value) {
                // null 需要单独处理（否则 NPE）
                case null -> "空值（null）";
                // 匹配 Integer 类型并绑定为 i
                case Integer i -> "整数: " + i + "（绝对值：" + Math.abs(i) + "）";
                // 匹配 Double 类型，范围判断
                case Double d when d > 0 -> "正小数: " + d;
                case Double d -> "非正小数: " + d;
                // 匹配字符串
                case String s -> "字符串: \"" + s + "\"（长度：" + s.length() + "）";
                // 匹配布尔值
                case Boolean b -> "布尔值: " + b;
                // 匹配字符
                case Character c -> "字符: " + c;
                // 默认分支
                default -> "未知类型: " + value.getClass().getName();
            };
            System.out.println(result);
        }
    }
}
```

输出：

```
整数: 42（绝对值：42）
正小数: 3.14159
字符串: "Hello"（长度：5）
布尔值: true
空值（null）
字符: X
未知类型: [I
```

### 35.3.3 关键语法解析

1. **类型模式（Type Pattern）**：`case Integer i` —— 匹配 Integer 类型，并将值绑定到变量 `i`
2. **Guard 条件（when 子句）**：`case Double d when d > 0` —— 在类型匹配的基础上加条件判断
3. **null 处理**：必须显式处理 `null`，否则运行时会抛 NPE
4. **穷尽性检查**：编译器会检查 switch 是否覆盖了所有可能的情况，如果漏了会报错

### 35.3.4 Record 模式与 switch 的结合

Record 模式（见 35.4 节）可以和 switch 结合，做嵌套匹配：

```java
// Chapter35RecordPatternSwitch.java
public class Chapter35RecordPatternSwitch {

    // 定义一个 Record
    record Point(int x, int y) {}

    public static void main(String[] args) {
        Object[] shapes = {
                new Point(0, 0),
                new Point(3, 4),
                "circle",
                new int[]{1, 2},
                new Point(-1, -1)
        };

        for (Object shape : shapes) {
            String result = switch (shape) {
                // 匹配 Record 并同时解构（x, y）
                case Point(int x, int y) when x == 0 && y == 0 -> "原点 " + shape;
                case Point(int x, int y) when x == y -> "对角线点（x=y=" + x + "）";
                case Point(int x, int y) -> "普通点: (" + x + ", " + y + ")";
                case String s -> "字符串: " + s;
                case null -> "空对象";
                default -> "其他图形";
            };
            System.out.println(result);
        }
    }
}
```

输出：

```
原点 Point[x=0, y=0]
普通点: (3, 4)
字符串: circle
其他图形
对角线点（x=y=-1）
```

---

## 35.4 Record Patterns

### 35.4.1 什么是 Record？

**Record**（记录类型）是 Java 16 正式引入的特性（JEP 395），它的设计目的是让 Java 也能优雅地表示"**不可变数据载体**"。

传统的 Java 类写法：

```java
// 传统 POJO： getters、setters、equals、hashCode、toString... 一大堆模板代码
public class Person {
    private final String name;
    private final int age;
    public Person(String name, int age) { this.name = name; this.age = age; }
    public String getName() { return name; }
    public int getAge() { return age; }
    // equals, hashCode, toString... 省略 50 行
}
```

Record 的写法：

```java
// 一行搞定！编译器自动生成：构造函数、getters、equals、hashCode、toString
public record Person(String name, int age) {}
```

### 35.4.2 Record Patterns（记录模式）

Record Pattern 让你可以在**解构** Record 的同时直接提取字段，并结合 `instanceof`、`for` 循环、lambda 参数等场景使用。

```java
// Chapter35RecordPatterns.java
public class Chapter35RecordPatterns {

    // 定义几个 Record
    record Person(String name, int age) {}
    record Address(String city, String district) {}
    record Employee(Person person, Address address, double salary) {}

    public static void main(String[] args) {
        Employee emp = new Employee(
                new Person("阿柴", 18),
                new Address("杭州", "西湖区"),
                25000.50
        );

        // 场景1：在 instanceof 中使用 Record Pattern（Java 16+）
        if (emp.person() instanceof Person(String n, int a)) {
            System.out.println("instanceof 解构: " + n + "，今年 " + a + " 岁");
        }

        // 场景2：嵌套 Record Pattern（Java 21+）
        if (emp instanceof Employee(Person(String name, int age), Address(String city, _), double salary)) {
            System.out.println("嵌套解构:");
            System.out.println("  姓名: " + name);
            System.out.println("  年龄: " + age);
            System.out.println("  城市: " + city);
            System.out.println("  薪资: " + salary);
        }

        // 场景3：在 for 循环中使用 Record Pattern（需借助 instanceof）
        Person[] people = {
                new Person("小明", 20),
                new Person("小红", 22),
                new Person("小张", 19)
        };
        System.out.println("\n遍历解构：");
        for (Person p : people) {
            if (p instanceof Person(String n, int a)) {
                System.out.println("  " + n + " -> " + a + "岁");
            }
        }
    }
}
```

输出：

```
instanceof 解构: 阿柴，今年 18 岁
嵌套解构:
  姓名: 阿柴
  年龄: 18
  城市: 杭州
  薪资: 25000.5

遍历解构：
  小明 -> 20岁
  小红 -> 22岁
  小张 -> 19岁
```

### 35.4.3 Record 的注意事项

- Record 是**隐式 final** 的，字段不可修改（适合作为纯数据载体）
- Record 可以实现**接口**、可以有**静态成员**、可以定义**静态工厂方法**
- Record **不支持 extends**，但可以实现接口
- Record 可以有**实例方法**、**非 record 字段**（但必须是 static 的）

---

## 35.5 Scoped Values

### 35.5.1 背景：ThreadLocal 的痛

在 Java 并发编程中，`ThreadLocal` 是用来在**线程内**共享数据的经典手段。比如 Spring 框架就用 `ThreadLocal` 存储当前请求的用户信息。

但 `ThreadLocal` 有两个问题：

1. **内存泄漏风险**：`ThreadLocal` 变量在线程池中如果忘记 `remove()`，就会一直占用内存。
2. **跨虚拟线程传递困难**：虚拟线程会被**成千上万次挂起和恢复**，其内部的 `ThreadLocal` 值在恢复时可能不一致。

### 35.5.2 Scoped Values 登场

**Scoped Values（作用域变量）** 是 Java 21 引入的预览特性（JEP 446），此后在 Java 22（JEP 464）、Java 23（JEP 481）、Java 24（JEP 487）持续预览打磨，最终在 **Java 25（JEP 506）正式转正**。它提供了一种**安全、可继承、可复用的线程内数据共享**机制。

核心思想：**数据绑定到一段代码的作用域，而不是整个线程的生命周期**。

```java
// Chapter35ScopedValues.java
public class Chapter35ScopedValues {

    // 定义一个 Scoped Value（类似于 ThreadLocal，但更安全）
    private static final ScopedValue<String> CURRENT_USER = ScopedValue.newInstance();

    public static void main(String[] args) throws Exception {
        System.out.println("主线程直接读取（未设置）: " + CURRENT_USER.orElse("未登录"));

        // 在作用域内设置和读取 Scoped Value
        ScopedValue.where(CURRENT_USER, "阿柴").run(() -> {
            System.out.println("作用域内读取: " + CURRENT_USER.get());
            doSomething(); // 嵌套调用也能读取到
        });

        System.out.println("作用域外读取: " + CURRENT_USER.orElse("未登录"));

        // Scoped Value 天然支持虚拟线程
        Thread.ofVirtual().start(() -> {
            ScopedValue.where(CURRENT_USER, "虚拟线程用户").run(() -> {
                System.out.println("虚拟线程中: " + CURRENT_USER.get());
            });
        }).join();
    }

    // 嵌套方法也能读到 Scoped Value（跨方法传递无需参数）
    private static void doSomething() {
        System.out.println("  [嵌套] 读取到用户: " + CURRENT_USER.get());
    }
}
```

输出：

```
主线程直接读取（未设置）: 未登录
作用域内读取: 阿柴
  [嵌套] 读取到用户: 阿柴
作用域外读取: 未登录
虚拟线程中: 虚拟线程用户
```

### 35.5.3 Scoped Value vs ThreadLocal

| 特性 | ThreadLocal | Scoped Value |
|------|------------|-------------|
| 生命周期 | 线程整个生命周期 | 作用域代码块内 |
| 继承性 | 不可继承（子线程默认看不到） | 可选继承（子作用域可见） |
| 虚拟线程安全 | 存在风险（挂起恢复后值可能丢失） | 安全（设计即考虑虚拟线程） |
| 内存管理 | 需手动 remove() | 作用域结束后自动释放 |
| API | `set()`/`get()` | `ScopedValue.where()` |

---

## 35.6 Foreign Function & Memory API

### 35.6.1 背景：JNI 的痛与 Java 的野心

Java 诞生之初就喊出"**一次编写，到处运行**"的口号。但现实是，很多高性能场景必须调用 native 代码（C/C++）。传统的方案是 **JNI（Java Native Interface）**，但 JNI 写起来极其繁琐：

1. 要写 Java 端的 native 方法声明
2. 要写 C 端的实现
3. 要编译成 `.dll`/`.so` 文件
4. 要用 `System.loadLibrary()` 加载
5. 一旦出错，调试困难，内存管理混乱

**Foreign Function & Memory API（外部函数与内存 API，JEP 454）** 就是为了彻底解决这个问题。它让你用**纯 Java 代码**，就能安全地调用 native 库和操作 native 内存。

### 35.6.2 第一个示例：调用 C 标准库的 `strlen`

```java
// Chapter35ForeignMemory.java
import java.lang.foreign.Arena;
import java.lang.foreign.FunctionDescriptor;
import java.lang.foreign.Linker;
import java.lang.foreign.MemorySegment;
import java.lang.foreign.SymbolLookup;
import java.lang.foreign.ValueLayout;
import java.lang.invoke.MethodHandle;
import java.nio.charset.StandardCharsets;

public class Chapter35ForeignMemory {

    public static void main(String[] args) throws Throwable {
        Linker linker = Linker.nativeLinker();

        // 获取 C 运行时的符号查找器：
        // defaultLookup() 会查找当前平台默认的 C 库（macOS/Linux 上是 libc，Windows 上是 C 运行时）。
        // 若要从任意动态库查找，可改用 SymbolLookup.libraryLookup("libc.dylib", Arena.global())。
        SymbolLookup stdlib = linker.defaultLookup();

        // 找到 strlen 函数的地址
        MemorySegment strlenAddr = stdlib.find("strlen")
                .orElseThrow(() -> new RuntimeException("找不到 strlen 函数"));

        // 描述 C 函数签名：size_t strlen(const char* str)
        // size_t 是平台相关的无符号整数，64 位平台上用 JAVA_LONG 表示；指针用 ADDRESS 表示。
        FunctionDescriptor strlenDescriptor = FunctionDescriptor.of(
                ValueLayout.JAVA_LONG,   // 返回值 size_t
                ValueLayout.ADDRESS      // 参数 const char*
        );

        // 创建方法句柄（downcall handle 负责把 Java 调用翻译成 native 调用）
        MethodHandle strlenHandle = linker.downcallHandle(strlenAddr, strlenDescriptor);

        String testString = "你好，Java FFM!";
        try (Arena arena = Arena.ofConfined()) {
            // 将 Java 字符串按 UTF-8 复制到 native 内存（末尾自动补 '\0'）
            MemorySegment nativeString = arena.allocateFrom(testString, StandardCharsets.UTF_8);

            // 调用 strlen 获取字节长度
            long length = (long) strlenHandle.invoke(nativeString);
            System.out.println("C strlen 结果: " + length);
            System.out.println("Java 字符串字节数: " + testString.getBytes(StandardCharsets.UTF_8).length);
        }
    }
}
```

输出（macOS/Linux 上与 Java 侧的字节数一致，因为二者都按 UTF-8 统计）：

```
C strlen 结果: 18
Java 字符串字节数: 18
```

> 📌 **注意 1**：早期草案里的 `Linker.Option.interner()`、`Arena.openConfined()` 等写法**并不属于正式 API**，正式版的 Arena 工厂方法是 `Arena.ofConfined()` / `ofShared()` / `ofAuto()`，返回类型用 `ValueLayout.JAVA_LONG`、`ValueLayout.ADDRESS` 描述。
>
> 📌 **注意 2**：在 Windows 上 C 运行时库是 `msvcrt.dll`，在 Linux/macOS 上是 `libc.so` / `libc.dylib`。用 `Linker.nativeLinker().defaultLookup()` 可以跨平台自动定位，无需硬编码库名。
>
> 📌 **注意 3**：调用外部函数属于“受限操作”，Java 24 起如果模块未开启 native 访问会打印警告（未来版本可能直接禁止）。正式运行请加上参数：`java --enable-native-access=ALL-UNNAMED Chapter35ForeignMemory`。

### 35.6.3 Native 内存管理：安全第一

传统 JNI 中，native 内存需要手动管理，忘记释放就会内存泄漏。Foreign Function & Memory API 通过**Arena（竞技场）** 来自动管理内存：

```java
// Chapter35MemoryManagement.java
import java.lang.foreign.Arena;
import java.lang.foreign.MemorySegment;
import java.lang.foreign.MemoryLayout;
import java.lang.foreign.ValueLayout;

public class Chapter35MemoryManagement {

    public static void main(String[] args) {
        // Arena 有三种工厂方法：
        // 1. Arena.ofConfined() - 只能被创建它的线程使用，关闭后释放
        // 2. Arena.ofShared()   - 可被多线程共享，所有使用者退出后释放
        // 3. Arena.ofAuto()     - 交给 GC 自动管理，无需手动关闭

        try (Arena arena = Arena.ofConfined()) {
            // 分配 100 字节
            MemorySegment segment = arena.allocate(100);
            System.out.println("分配的内存段: " + segment);
            System.out.println("大小: " + segment.byteSize());

            // 分配并写入一个 int 数组（allocateFrom 会把 Java 值直接拷进 native 内存）
            MemorySegment intArray = arena.allocateFrom(ValueLayout.JAVA_INT, 1, 2, 3, 4, 5);
            System.out.println("int 数组长度: " + intArray.byteSize() / 4); // 每个 int 4 字节

            // 定义结构体内存布局（模拟 C 的 struct { int age; long address; }）
            // 注意 C 的对齐规则：int 后面需要 4 字节填充，long 才能 8 字节对齐，
            // 因此必须显式插入 paddingLayout(4)，否则 structLayout 会直接抛异常。
            MemoryLayout personLayout = MemoryLayout.structLayout(
                    ValueLayout.JAVA_INT.withName("age"),
                    MemoryLayout.paddingLayout(4),
                    ValueLayout.JAVA_LONG.withName("address")
            );
            MemorySegment person = arena.allocate(personLayout);
            System.out.println("person 结构体布局: " + personLayout);
            // 按字段偏移量读写结构体成员
            person.set(ValueLayout.JAVA_INT,
                    personLayout.byteOffset(MemoryLayout.PathElement.groupElement("age")), 18);
            person.set(ValueLayout.JAVA_LONG,
                    personLayout.byteOffset(MemoryLayout.PathElement.groupElement("address")), 1000L);
            int age = person.get(ValueLayout.JAVA_INT,
                    personLayout.byteOffset(MemoryLayout.PathElement.groupElement("age")));
            long address = person.get(ValueLayout.JAVA_LONG,
                    personLayout.byteOffset(MemoryLayout.PathElement.groupElement("address")));
            System.out.println("age = " + age + ", address = " + address);
        } // Arena 关闭后，所有分配的内存自动释放 —— 无需手动 free！
    }
}
```

输出：

```
分配的内存段: MemorySegment{ kind: native, address: 0x..., byteSize: 100 }
大小: 100
int 数组长度: 5
person 结构体布局: [i4(age)x4j8(address)]
age = 18, address = 1000
```

> 🔑 **核心优势**：所有的 native 内存分配都通过 Arena 管理，**无需手动释放**，Arena 关闭时自动清理。这意味着 JNI 中最常见的内存泄漏问题被彻底消灭了。

---

## 35.7 Stream Gatherers

### 35.7.1 背景：Stream 的局限

Java 的 Stream API 非常强大，但你是否遇到过这样的尴尬：

```java
// 想要：取前5个、相邻两两配对、扁平化
List<String> result = list.stream()
    .takeWhile(...)
    .dropWhile(...)
    // ... 没有直接的"相邻配对"操作
    // 必须自己写 collector 或者用第三方库
```

**Stream Gatherers（流收集器）** 是一组内置的 Stream 操作扩展，它让 Stream 处理流水线更加强大。它先在 Java 22（JEP 461）和 Java 23（JEP 473）两轮预览，最终在 **Java 24（JEP 485）正式转正**，使用内置收集器时不再需要 `--enable-preview`。

### 35.7.2 内置 Gatherers

JDK 的 `java.util.stream.Gatherers` 工具类提供了几个开箱即用的收集器：

```java
// Chapter35StreamGatherers.java
import java.util.List;
import java.util.stream.Gatherers;

public class Chapter35StreamGatherers {

    public static void main(String[] args) {
        List<Integer> numbers = List.of(1, 2, 3, 4, 5, 6, 7, 8, 9, 10);

        // 1. windowFixed(n) - 固定大小窗口
        System.out.println("=== windowFixed(3) ===");
        numbers.stream()
                .gather(Gatherers.windowFixed(3))
                .forEach(window -> System.out.println(window));
        // 输出: [1,2,3], [4,5,6], [7,8,9], [10]

        // 2. windowSliding(n) - 滑动窗口
        System.out.println("\n=== windowSliding(3) ===");
        numbers.stream()
                .gather(Gatherers.windowSliding(3))
                .forEach(window -> System.out.println(window));
        // 输出: [1,2,3], [2,3,4], [3,4,5], ...

        // 3. fold(initialSupplier, folder) - 折叠成单个结果（注意第一个参数是"初始值工厂"）
        System.out.println("\n=== fold - 累加 ===");
        List<Integer> summed = numbers.stream()
                .gather(Gatherers.fold(() -> 0, Integer::sum))
                .toList();
        System.out.println("累加结果: " + summed); // [55]

        // 4. scan(initialSupplier, scanner) - 前缀累积（类似 Haskell 的 scanl）
        System.out.println("\n=== scan - 前缀累积 ===");
        numbers.stream()
                .limit(5)
                .gather(Gatherers.scan(() -> 0, Integer::sum))
                .forEach(n -> System.out.print(n + " ")); // 1 3 6 10 15

        // 5. mapConcurrent - 并发映射（正式功能，用虚拟线程并发执行映射函数）
        System.out.println("\n\n=== mapConcurrent(3) ===");
        List<String> names = List.of("Alice", "Bob", "Charlie", "David");
        names.stream()
                .gather(Gatherers.mapConcurrent(3, String::toUpperCase))
                .forEach(name -> System.out.println(name));
    }
}
```

输出：

```
=== windowFixed(3) ===
[1, 2, 3]
[4, 5, 6]
[7, 8, 9]
[10]
=== windowSliding(3) ===
[1, 2, 3]
[2, 3, 4]
[3, 4, 5]
[4, 5, 6]
[5, 6, 7]
[6, 7, 8]
[7, 8, 9]
[8, 9, 10]

=== fold - 累加 ===
累加结果: [55]

=== scan - 前缀累积 ===
1 3 6 10 15

=== mapConcurrent(3) ===
ALICE
BOB
CHARLIE
DAVID
```

### 35.7.3 自定义 Gatherer

你还可以自定义 Gatherer，实现更复杂的流处理逻辑：

```java
// Chapter35CustomGatherer.java
import java.util.ArrayList;
import java.util.List;
import java.util.function.Supplier;
import java.util.stream.Gatherer;
import java.util.stream.Gatherer.Integrator;

public class Chapter35CustomGatherer {

    // 自定义 Gatherer：去除连续重复元素
    // 例如: [1, 1, 2, 2, 2, 3, 1, 1] -> [1, 2, 3, 1]
    public static <T> Gatherer<T, ?, T> distinctConsecutive() {
        return Gatherer.ofSequential(
                // 状态初始化器：流开始时创建一份状态，这里用一个列表记录"已经输出过的最后一个元素"
                (Supplier<List<T>>) ArrayList::new,
                // 整合器：每来一个元素调用一次，需要时把结果 push 给下游
                (Integrator<List<T>, T, T>) (state, element, downstream) -> {
                    if (state.isEmpty() || !state.get(state.size() - 1).equals(element)) {
                        state.add(element);
                        return downstream.push(element); // 输出这个元素
                    }
                    return true; // 与上一个相同，跳过，继续处理下一个
                });
    }

    public static void main(String[] args) {
        List<Integer> data = List.of(1, 1, 1, 2, 2, 3, 3, 3, 3, 4, 4, 5, 5, 5);
        System.out.println("去重相邻: " + data.stream()
                .gather(distinctConsecutive())
                .toList());
        // 输出: [1, 2, 3, 4, 5]
    }
}
```

输出：

```
去重相邻: [1, 2, 3, 4, 5]
```

> 📌 **注意**：早期资料里常见的 `Gatherer.of(静态状态, 累加器, 下游消费者, 合并器)` 四参数写法容易踩坑——`Supplier<List<T>>::new` 这种写法无法确定泛型类型，会直接编译失败。自定义收集器推荐从 `Gatherer.ofSequential(初始器, 整合器)` 起步，需要并行处理时再补上 `combiner` 换成带合并器的重载。

---

## 35.8 Structured Concurrency（结构化并发）

### 35.8.1 为什么需要结构化并发？

传统的并发编程中，如果你启动了一个线程（或者 Future），然后主线程崩溃了，子线程会继续"孤儿般"地运行，你甚至不知道它们是否完成。这就是所谓的"**线程泄漏**"。

```java
// 传统写法：线程的启动和生命周期管理是分离的
void process() {
    ExecutorService executor = Executors.newFixedThreadPool(4);
    Future<?> f1 = executor.submit(task1);  // 提交后就没有结构化保证
    Future<?> f2 = executor.submit(task2);
    // 如果这里抛异常，executor 还没 shutdown，后台线程还在跑！
    executor.shutdown();
}
```

**Structured Concurrency（结构化并发）** 的核心思想是：**一个方法内启动的所有子任务，应该在该方法返回之前全部完成**。如果方法异常退出，所有子任务应该被**自动取消**。

> ⚠️ **状态说明**：结构化并发自 Java 21（JEP 453）起一直在预览，到 Java 24 是第四轮（JEP 499）、Java 25 是第五轮（JEP 505）、Java 26 是第六轮（JEP 525），**至今（JDK 25/26）仍是预览特性**，使用时要加 `--enable-preview`。请勿把它当成已经转正的正式 API。

### 35.8.2 StructuredTaskScope 使用演示

```java
// Chapter35StructuredConcurrency.java
import java.util.concurrent.StructuredTaskScope;
import java.util.concurrent.StructuredTaskScope.Joiner;

public class Chapter35StructuredConcurrency {

    public static void main(String[] args) throws Exception {
        System.out.println("=== 结构化并发示例 ===\n");
        basicExample();
        failureExample();
        anySuccessExample();
    }

    // 示例1：基础使用
    static void basicExample() throws InterruptedException {
        System.out.println("示例1: 基础结构化并发");
        // open() 使用默认的 Joiner（等待所有子任务成功完成）
        try (var scope = StructuredTaskScope.open()) {
            // fork 两个子任务
            var future1 = scope.fork(() -> {
                Thread.sleep(100);
                return "任务1完成";
            });
            var future2 = scope.fork(() -> {
                Thread.sleep(200);
                return "任务2完成";
            });

            // 等待所有 fork 的任务完成（blocking）
            scope.join();

            // 获取结果（任务已保证完成）
            System.out.println("  " + future1.get());
            System.out.println("  " + future2.get());
        }
        System.out.println("  作用域结束，所有子任务自动收尾\n");
    }

    // 示例2：任一失败即取消其余任务
    static void failureExample() throws Exception {
        System.out.println("示例2: 任一失败，全部取消");
        // Joiner.awaitAllSuccessfulOrThrow()：只要有一个子任务失败，
        // 就取消其他仍在运行的任务，join() 时抛出异常。
        try (var scope = StructuredTaskScope.open(Joiner.<String>awaitAllSuccessfulOrThrow())) {
            scope.fork(() -> {
                Thread.sleep(50);
                return "快速任务";
            });
            scope.fork(() -> {
                throw new RuntimeException("模拟任务失败");
            });

            scope.join(); // 有失败则在这里抛出
            System.out.println("  全部成功！");
        } catch (Exception e) {
            System.out.println("  捕获到异常: " + e.getCause().getMessage());
        }
        System.out.println();
    }

    // 示例3：取第一个成功的结果（竞速）
    static void anySuccessExample() throws Exception {
        System.out.println("示例3: 取第一个成功的结果（竞速谁最快）");
        // Joiner.anySuccessfulResultOrThrow()：谁先成功就用谁的结果，
        // join() 直接返回该结果，其余任务自动取消。
        try (var scope = StructuredTaskScope.open(Joiner.<String>anySuccessfulResultOrThrow())) {
            scope.fork(() -> {
                Thread.sleep(300);
                return "服务器A（慢）";
            });
            scope.fork(() -> {
                Thread.sleep(100);
                return "服务器B（快）";
            });
            scope.fork(() -> {
                Thread.sleep(200);
                return "服务器C（中）";
            });

            String winner = scope.join();
            System.out.println("  竞速冠军: " + winner);
        } catch (Exception e) {
            System.out.println("  全部失败: " + e);
        }
    }
}
```

运行方式（结构化并发在 JDK 25 仍是预览特性，两个参数缺一不可）：

```bash
javac --release 25 --enable-preview Chapter35StructuredConcurrency.java
java --enable-preview Chapter35StructuredConcurrency
```

输出：

```
=== 结构化并发示例 ===

示例1: 基础结构化并发
  任务1完成
  任务2完成
  作用域结束，所有子任务自动收尾

示例2: 任一失败，全部取消
  捕获到异常: 模拟任务失败

示例3: 取第一个成功的结果（竞速谁最快）
  竞速冠军: 服务器B（快）
```

> 📌 **注意**：旧版教程里出现的 `new StructuredTaskScope.ShutdownOnFailure()` / `ShutdownOnSuccess()` 已经**从 JDK 25 中删除**。现在的统一写法是 `StructuredTaskScope.open(Joiner)`，常用的 `Joiner` 工厂方法有：`allSuccessfulOrThrow()`、`awaitAllSuccessfulOrThrow()`、`awaitAll()`、`anySuccessfulResultOrThrow()`、`allUntil(Predicate)`。

### 35.8.3 结构化并发的三大保障

1. **生命周期绑定**：子任务的生命周期与父作用域绑定，不会成为孤儿线程
2. **失败传播**：任一子任务失败时，其他子任务会被自动取消
3. **取消传播**：作用域取消时，所有子任务都会被通知取消

---

## 35.9 Implicitly Declared Classes

### 35.9.1 背景：Java 也能写"脚本"了？

你有没有想过：**写一个简单的 Java 程序，能不能连类声明都不用写？**

传统的 Java 程序：

```java
public class Hello {
    public static void main(String[] args) {
        System.out.println("Hello!");
    }
}
```

**Compact Source Files and Instance Main Methods（紧凑源文件与实例 main 方法）** 让 Java 可以像脚本一样运行。它从 Java 21（JEP 445）开始预览，历经 Java 22（JEP 463）、Java 23（JEP 477）、Java 24（JEP 495）四轮打磨，最终在 **Java 25（JEP 512）正式转正**，不再需要 `--enable-preview`：

```java
// HelloJava.java —— 不需要 class 声明，不需要 public，不需要 static
void main() {
    System.out.println("Java 也能写脚本了！");
    System.out.println("Hello from Java " + System.getProperty("java.version"));
}
```

直接运行：`java HelloJava.java`

> 📌 **注意**：**直接运行单个 `.java` 源码文件**（不写 `class`、不手动 `javac`）其实从 **Java 11** 就支持了（JEP 330）；而**省略 `class` 声明、把 `main` 写成实例方法**是后来逐步预览、到 Java 25 才转正的能力。这两件事不要混为一谈。

### 35.9.2 隐式声明类的规则

```java
// Chapter35ImplicitClass.java
// 不需要 class 关键字！编译器会隐式创建一个同文件名的类
// 不需要 public 修饰符
// 不需要 static 修饰 main 方法

// 实例字段
String name = "阿柴";

// 实例 main 方法（注意：不是 static）
void main() {
    System.out.println("你好，名字: " + name);
    doStuff();
    System.out.println("计算 1+2 = " + add(1, 2));
}

// 其他实例方法
void doStuff() {
    System.out.println("这是隐式类的实例方法");
}

int add(int a, int b) {
    return a + b;
}

// 也可以有静态方法
static void staticMethod() {
    System.out.println("静态方法也可以");
}
```

> ⚠️ **限制**：隐式声明类不能被其他文件引用，不能声明 `public` 成员，不能使用完整模块系统。它仅限于**单文件脚本**场景。

### 35.9.3 与虚拟线程结合

隐式声明类特别适合快速原型和脚本场景，结合虚拟线程也很简单：

```java
// Chapter35ImplicitWithVT.java
// 直接运行：java Chapter35ImplicitWithVT.java（Java 25 起无需 --enable-preview）

void main() {
    System.out.println("隐式类 + 虚拟线程演示");

    Thread.ofVirtual().start(() -> {
        System.out.println("我是隐式类中的虚拟线程！");
    });

    System.out.println("主线程继续执行...");
    try {
        Thread.sleep(100);
    } catch (InterruptedException ignored) {}
}
```

---

## 本章小结

Java 21～26 是 Java 语言史上变化最剧烈的六年。以下是关键要点回顾：

| 特性 | Java 版本 | 状态 | JEP |
|------|---------|------|-----|
| 虚拟线程（Virtual Threads） | 21 | 正式版 | JEP 444 |
| 字符串模板（String Templates） | 21 | **已撤回（Withdrawn）** | JEP 430 → JEP 465 |
| Pattern Matching for switch | 21 | 正式版 | JEP 441 |
| Record Patterns | 21 | 正式版 | JEP 440 |
| Scoped Values | 21～25 | 预览 → **25 正式版** | JEP 446 → JEP 506 |
| Foreign Function & Memory API | 21～22 | 预览 → **22 正式版** | JEP 454 |
| Stream Gatherers | 22～24 | 预览 → **24 正式版** | JEP 461 → JEP 485 |
| Structured Concurrency | 21～26 | **仍是预览版** | JEP 453 → JEP 505（6th: JEP 525） |
| Compact Source Files / 实例 main | 21～25 | 预览 → **25 正式版** | JEP 445 → JEP 512 |

**核心启示**：

1. **并发模型革新是主旋律**：虚拟线程、Scoped Values、结构化并发三者共同构成了 Java 新一代并发编程范式。
2. **FFM API 终结了 JNI 的时代**：纯 Java 调用 native 库 + 自动内存管理，JNI 可以逐步退出历史舞台了。
3. **语言表达力持续增强**：Record Patterns、Pattern Matching for switch、Stream Gatherers、模式匹配等让 Java 越来越接近"少写代码多干活"的理想。
4. **Java 正在拥抱脚本化**：紧凑源文件（Compact Source Files）与实例 main 方法降低了 Java 的入门门槛，让 Java 也可以像 Python 一样写即跑。
5. **预览机制是把双刃剑**：好消息是它在正式发布前留足了打磨空间（比如 Scoped Values、结构化并发都迭代了四五轮）；坏消息是**预览特性随时可能改名甚至被撤回**（字符串模板就是活生生的例子）。所以生产环境尽量以"已转正"的特性为准，预览特性要盯紧 JEP 编号和版本。

这些特性不是孤立的，它们共同指向 Java 的未来方向：**更高的开发效率、更安全、更简洁、更强大的并发处理能力**。掌握它们，你就不只是 Java 程序员，而是一个**现代 Java 开发者**。
