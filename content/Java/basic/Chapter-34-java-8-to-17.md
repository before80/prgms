+++
title = "第34章 Java 8~17 新特性全景"
weight = 340
date = "2026-03-30T14:33:56.918+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++
# 第三十四章 Java 8~17 新特性全景

> "Talk is cheap. Show me the code." —— Linus Torvalds
>
> 这句话放到 Java 身上简直太合适了。从 Java 8 开始，Oracle 对 Java 的演进速度就像开了挂一样，每半年发布一个大版本，每版本都带着让人眼前一亮的新特性。本章我们就来一次 Java 新特性的"全景扫描"，从 Java 8 的革命性突破，一路看到 Java 17 的成熟稳重。

## 特性时间线

在正式开始之前，先来看一张时间线总览，直观感受 Java 这些年的"进化史"：

```mermaid
timeline
    title Java 8~17 新特性演进史
    2014年3月: Java 8 发布
        : Lambda表达式 : Stream API : Optional : 新的Date/Time API
    2017年9月: Java 9 发布
        : 模块化系统 : 集合工厂方法 : 私有接口方法
    2018年3月: Java 10 发布
        :局部变量类型推断 : 应用程序类数据共享
    2018年9月: Java 11 发布
        : HTTP Client API : 单文件程序 : String底层改进
    2019年3月: Java 12~17 发布
        : Switch表达式 : Records : Pattern Matching : Sealed Classes : 文本块
```

---

## 34.1 Java 8 特性：改变游戏规则的版本

Java 8 可以说是 Java 历史上最重要的版本之一，它的出现彻底改变了 Java 程序员写代码的方式。如果说之前的 Java 是一个"严谨的中年人"，那 Java 8 之后，Java 终于学会了"函数式编程"这门炫酷的新技能。

### 34.1.1 Lambda 表达式：匿名内部类的"掘墓人"

**Lambda 表达式**是什么？简单来说，就是一种"匿名函数"的语法糖——你没有名字的函数，一行就能写完，用完即弃。它让代码从"又臭又长"变得"短小精悍"。

在 Java 8 之前，如果你想对一个列表按字符串长度排序，是这样写的：

```java
// Java 7 及之前的写法：啰嗦到让人想打人
List<String> names = Arrays.asList("Alice", "Bob", "Charlie", "David");
Collections.sort(names, new Comparator<String>() {
    @Override
    public int compare(String s1, String s2) {
        return Integer.compare(s1.length(), s2.length());
    }
});
```

Java 8 之后，一行搞定：

```java
// Java 8 的 Lambda 写法：简洁优雅
List<String> names = Arrays.asList("Alice", "Bob", "Charlie", "David");
names.sort((s1, s2) -> Integer.compare(s1.length(), s2.length()));

// 甚至还能更简洁（方法引用）
names.sort(Comparator.comparingInt(String::length));
```

**语法解释**：`->` 是 Lambda 操作符，左边是参数（可以推断类型时省略类型声明），右边是方法体。如果方法体只有一条语句，花括号也可以省略。

Lambda 表达式的几种形式：

```java
// 形式1：无参数，方法体是一条语句
Runnable r = () -> System.out.println("Hello Lambda!");

// 形式2：单个参数，参数类型可推断时省略括号
Consumer<String> consumer = msg -> System.out.println(msg);

// 形式3：多个参数，方法体是多条语句
BinaryOperator<Integer> add = (a, b) -> {
    int sum = a + b;
    System.out.println("计算结果：" + sum);
    return sum;
};
```

> **为什么重要？** Lambda 表达式不只是一个语法糖，它是 Java 迈向函数式编程的第一步。正是因为 Lambda，Stream API 才能如此优雅，函数式接口才能大放异彩。可以说，没有 Lambda，Java 8 的一半精华都将黯然失色。

### 34.1.2 Stream API：集合操作的"瑞士军刀"

**Stream API**（注意这里的 Stream 跟 InputStream/OutputStream 没有任何关系）是 Java 8 献给集合处理的一把瑞士军刀。它不是数据结构，不存储数据，而是一个"数据流处理视图"。

Stream 的核心思想是：**把数据的"加工流水线"描述出来，而不是一步一步执行**。这叫做"声明式编程"——你告诉计算机"要什么"，而不是"怎么做"。

先看一个传统写法 vs Stream 写法的对比：

```java
// 场景：找出年龄大于18岁的用户，按名字排序，去重，输出

// 传统写法：一步一步来，过程导向
List<User> filtered = new ArrayList<>();
for (User user : users) {
    if (user.getAge() > 18) {
        filtered.add(user);
    }
}
Collections.sort(filtered, Comparator.comparing(User::getName));
List<User> unique = new ArrayList<>(new LinkedHashSet<>(filtered));
for (User user : unique) {
    System.out.println(user.getName());
}

// Stream 写法：一气呵成，声明式
users.stream()
      .filter(user -> user.getAge() > 18)        // 过滤
      .map(User::getName)                         // 转换
      .distinct()                                 // 去重
      .sorted()                                   // 排序
      .forEach(System.out::println);              // 输出
```

Stream 的三大操作类型：

```java
// 1. 创建 Stream
List<String> list = Arrays.asList("a", "b", "c");
Stream<String> stream = list.stream();          // 从集合创建
int[] arr = {1, 2, 3};
IntStream intStream = Arrays.stream(arr);       // 从数组创建
Stream<Integer> rangeStream = IntStream.range(1, 10).boxed(); // 数值范围

// 2. 中间操作（返回 Stream，可以链式调用）
stream.filter(s -> s.length() > 0)   // 过滤：保留满足条件的元素
      .map(String::toUpperCase)       // 映射：转换元素类型
      .sorted()                        // 排序
      .distinct()                      // 去重
      .limit(10)                       // 截取前N个
      .skip(5);                        // 跳过前N个

// 3. 终端操作（触发执行，返回结果）
long count = stream.count();          // 计数
List<String> result = stream.collect(Collectors.toList()); // 收集为List
String joined = stream.collect(Collectors.joining(", "));    // 字符串拼接
stream.forEach(System.out::println);  // 遍历
Optional<String> first = stream.findFirst(); // 找第一个
boolean anyMatch = stream.anyMatch(s -> s.startsWith("a")); // 任意匹配
```

> **重要提示**：Stream 有两大致命误区！第一，Stream 不是数据结构，它不会修改原始数据（除非你用 `forEach` 这种副作用操作）；第二，**Stream 只能消费一次**，消费完再调用会抛出 `IllegalStateException`。

### 34.1.3 接口默认方法：协议也可以有"默认实现"

**默认方法**（Default Method）是 Java 8 给接口带来的一项"破坏性创新"。之前接口里只能声明抽象方法，现在可以写具体实现了！

为什么要这样？主要是为了**向后兼容**。想象一下，你有一个接口被成千上万的类实现，现在想给它加一个新方法，如果没有默认方法，所有实现类都得修改——这简直是一场噩梦。默认方法让新增接口方法成为可能，而不必破坏现有代码。

```java
// Java 8 之前的接口：只能声明，不能有实现
interface Animal {
    void speak();  // 必须实现
}

// Java 8 的接口：可以有默认实现
interface Animal {
    void speak();  // 必须实现

    // 默认方法：实现类可以继承这个实现，也可以覆盖它
    default void eat() {
        System.out.println("动物在吃东西...");
    }

    // 静态方法：属于接口本身，不属于实现类
    static void info() {
        System.out.println("这是动物接口");
    }
}

// 实现类可以省略eat方法，直接使用默认实现
class Dog implements Animal {
    @Override
    public void speak() {
        System.out.println("汪汪汪！");
    }
}

public class DefaultMethodDemo {
    public static void main(String[] args) {
        Dog dog = new Dog();
        dog.speak();  // 输出：汪汪汪！
        dog.eat();    // 输出：动物在吃东西...（继承默认实现）

        Animal.info(); // 输出：这是动物接口（静态方法直接调用）
    }
}
```

> **注意事项**：如果一个类同时实现了两个接口，而这两个接口都有同名的默认方法，就会产生**菱形继承问题**，此时必须手动解决冲突。

### 34.1.4 Optional：null 的"终结者"

**Optional** 是 Java 8 引入的"null 安全容器"。它的核心思想是：**用"有值"或"无值"的明确语义，替代 null 的模糊语义**。

在 Java 8 之前，面对可能为空的值，我们只能靠 if 判断和文档注释来猜测：

```java
// 这种代码到处都是，你永远不确定 user 是否为 null
User user = getUser(id);
if (user != null) {
    Address address = user.getAddress();
    if (address != null) {
        String city = address.getCity();
        if (city != null) {
            System.out.println(city);
        }
    }
}
```

Optional 提供了优雅的链式操作：

```java
import java.util.Optional;

// 使用 Optional 替代 null 检查
Optional<User> userOpt = getUserOptional(id);

String city = userOpt
    .map(User::getAddress)          // 映射：如果有值，执行转换
    .map(Address::getCity)
    .orElse("未知城市");             // 如果链中任何一步为空，返回默认值

// 其他常用方法
userOpt.ifPresent(user -> System.out.println(user.getName())); // 有值才执行

// orElseGet：使用供给器提供默认值（延迟计算）
String name = userOpt.map(User::getName).orElseGet(() -> computeDefaultName());

// orElseThrow：没有值就抛异常
String email = userOpt.map(User::getEmail).orElseThrow(() -> new RuntimeException("用户不存在"));

// isPresent / isEmpty：判断是否存在
if (userOpt.isPresent()) {
    System.out.println("用户存在");
}
```

> **最佳实践**：Optional 主要用于**方法返回值**，不建议在字段、参数、方法内部滥用。过度使用 Optional 反而会让代码变得复杂。

### 34.1.5 新的 Date/Time API：终于可以和 Date 说拜拜了

Java 8 之前的 `java.util.Date` 和 `java.text.SimpleDateFormat` 可以说是 Java 早期设计的"黑历史"——不是线程安全的，月份从0开始，各种方法名让人摸不着头脑。

Java 8 的 `java.time` 包提供了一套全新的、线程安全的、语义清晰的日期时间 API：

```java
import java.time.*;

// 1. 获取当前时间（多种精度）
LocalDate today = LocalDate.now();        // 只有日期：2026-03-30
LocalTime now = LocalTime.now();          // 只有时间：14:30:45.123
LocalDateTime now2 = LocalDateTime.now(); // 日期+时间
ZonedDateTime zonedNow = ZonedDateTime.now(ZoneId.of("Asia/Shanghai")); // 带时区

// 2. 创建指定时间
LocalDate birthDay = LocalDate.of(1990, 1, 15);  // 注意：月份是1-12，不是0-11
LocalDateTime meeting = LocalDateTime.of(2026, 6, 1, 14, 0);
Instant timestamp = Instant.now();  // UTC时间戳，适合日志记录

// 3. 日期时间计算（返回新对象，原对象不变）
LocalDate tomorrow = today.plusDays(1);
LocalDate nextMonth = today.plusMonths(1);
Duration duration = Duration.between(now2, now2.plusHours(2));

// 4. 日期时间格式化
LocalDateTime dt = LocalDateTime.of(2026, 3, 30, 21, 10);
String formatted = dt.format(DateTimeFormatter.ofPattern("yyyy年MM月dd日 HH:mm:ss"));
System.out.println(formatted);  // 输出：2026年03月30日 21:10:00

// 5. 日期时间解析
LocalDate parsed = LocalDate.parse("2026-03-30");
LocalDateTime parsed2 = LocalDateTime.parse("2026-03-30T14:30:00");

// 6. 时间段计算
Period period = Period.between(
    LocalDate.of(2020, 1, 1),
    LocalDate.of(2026, 3, 30)
);
System.out.println(period.getYears() + "年" + period.getMonths() + "月" + period.getDays() + "天");
// 输出：6年2月29天

// 7. 时区转换
ZonedDateTime tokyoTime = zonedNow.withZoneSameInstant(ZoneId.of("Asia/Tokyo"));
```

> **使用建议**：新代码一律使用 `java.time`，不要再用旧的 `Date` 和 `Calendar` 了。旧 API 只在维护历史代码时使用。

---

## 34.2 Java 9~11 特性：稳中求进的六年

Java 8 打响了变革的第一枪，Java 9~11 则在"现代化 Java"的路上继续高歌猛进。这几个版本带来了模块化系统、类型推断增强、HTTP Client 等重磅功能。

### 34.2.1 模块化系统（Project Jigsaw）：Java 的"拼图游戏"

**模块化系统**（Module System）是 Java 9 引入的最重大特性，也被称为 Project Jigsaw。它的核心思想是：把 Java 应用分成多个**模块**，每个模块声明自己**依赖哪些模块**、**导出哪些包**。

为什么要模块化？主要有三个目的：

1. **封装性增强**：以前 public 就是"全宇宙公开"，有了模块，你可以只暴露想暴露的类
2. **依赖明确化**：模块必须显式声明依赖，解决了类路径（ClassPath）的"类 hell"问题
3. **精简 JDK**：JDK 本身也被模块化了，你可以只加载需要的模块，打造更小的运行时镜像

**模块声明**通过 `module-info.java` 文件来定义：

```java
// 这是一个模块的声明文件，叫 module-info.java
// 放在模块根目录下

module com.myapp.core {           // 模块名，通常用反转域名命名
    requires com.myapp.utils;     // 声明依赖其他模块
    requires transitive org.apache.commons; // transitive：传递依赖，我的依赖者也能用

    exports com.myapp.core.api;   // 导出包（只导出这些包，别的模块才能用）
    exports com.myapp.core.model;

    // 只在模块内可见，外部无法访问
    // （没有 export 的包默认是模块私有）
}
```

一个完整的模块化项目结构示例：

```
my-project/
├── src/
│   ├── com.myapp.core/           # 模块一
│   │   ├── module-info.java
│   │   └── com/myapp/core/
│   │       ├── api/              # 导出的包
│   │       │   └── UserService.java
│   │       └── internal/         # 未导出的包，外部无法访问
│   │           └── InternalUtils.java
│   └── com.myapp.cli/            # 模块二，依赖 core
│       ├── module-info.java
│       └── com/myapp/cli/
│           └── Main.java
└── module-path/
```

在命令行编译和运行模块化程序：

```bash
# 编译
javac -d out --module-source-path src $(find src -name "*.java")

# 运行
java --module-path out --module com.myapp.cli/com.myapp.cli.Main
```

> **实际意义**：模块化对于大型企业级应用和 JDK 本身的瘦身（比如 JDK 9 之后的 `jlink` 工具可以创建自定义精简运行时）有巨大价值。不过对于日常的小项目，学习曲线有点陡，收益不一定明显。

### 34.2.2 集合工厂方法：一步创建不可变集合

在 Java 9 之前，创建小型字面量集合是件痛苦的事：

```java
// Java 8 及之前的做法
List<String> list = Arrays.asList("Apple", "Banana", "Orange");
Set<Integer> set = new HashSet<>(Arrays.asList(1, 2, 3));
Map<String, Integer> map = new HashMap<>();
map.put("A", 1);
map.put("B", 2);
```

Java 9 引入了一组**集合工厂方法**，让创建小型不可变集合变得极其简洁：

```java
import java.util.*;

// List.of()：创建不可变列表
List<String> list = List.of("Apple", "Banana", "Orange");

// Set.of()：创建不可变集合
Set<Integer> set = Set.of(1, 2, 3);

// Map.of()：创建不可变映射（键值对成对提供）
Map<String, Integer> map = Map.of("Apple", 1, "Banana", 2, "Orange", 3);

// 注意：这些集合都是不可变的！
// list.add("Pear");  // UnsupportedOperationException！

// 如果确实需要可变副本
List<String> mutableList = new ArrayList<>(list);
mutableList.add("Pear");
```

> **为什么叫"不可变"而不是"只读"？** 严格来说，"不可变"意味着对象创建后状态完全固定，而"只读"可能只是提供了修改接口但实际不修改。Java 的工厂方法创建的是真正的不可变集合——既不能添加、删除元素，也不能修改已有元素。

### 34.2.3 局部变量类型推断：var 让代码更简洁

**类型推断**（Type Inference）从 Java 10 开始引入 `var` 关键字，允许在局部变量声明时省略类型，由编译器自动推断。

```java
// Java 10 之前
String message = "Hello, Java!";
Map<String, List<Integer>> complexMap = new HashMap<>();
Iterator<Map.Entry<String, Object>> iterator = map.entrySet().iterator();

// Java 10+ 使用 var
var message = "Hello, Java!";                              // 推断为 String
var complexMap = new HashMap<String, List<Integer>>();     // 推断为 HashMap<String, List<Integer>>
var iterator = map.entrySet().iterator();                   // 推断为 Iterator<Map.Entry<String, Object>>

// var 在 for 循环中特别有用
List<String> names = List.of("Alice", "Bob", "Charlie");
for (var name : names) {  // 不用写 Iterator<String>
    System.out.println(name);
}
```

**使用 var 的注意事项**：

```java
// ❌ 错误1：var 不能用于声明字段（只能用于局部变量）
class Example {
    var field = "error";  // 编译错误！
}

// ❌ 错误2：var 不能用于没有初始化值的声明
var noInit;  // 编译错误！编译器无法推断类型

// ❌ 错误3：var 不能用于 lambda 表达式（需要目标类型）
var lambda = (x, y) -> x + y;  // 编译错误！

// ❌ 错误4：var 不是关键字，是保留类型名（实际上 Java 10-16 中 var 不是关键字，但 Java 17 中它仍然是保留类型名）
// 这意味着你不能创建名为 var 的类或接口
```

> **最佳实践**：`var` 适合类型名很长但从右侧明显可推断的场景。对于局部变量，特别是循环变量、try-with-resources 资源声明等场景，使用 `var` 能显著提升可读性。但不要滥用——如果类型不明确或者会影响可读性，还是写清楚类型名为好。

### 34.2.4 String 底层改进：终于不是 char[] 了

Java 9 对 `String` 的内部实现做了重大改进：从 `char[]` 改为 `byte[]` 存储，配合**紧凑字符串**（Compact Strings）技术，大幅节省内存。

为什么重要？因为大多数字符串是 Latin-1 字符（只需1字节），而 Java 8 及之前每个字符都用2字节（UTF-16）的 `char[]` 存储，**白白浪费了一半内存**。

```java
// Java 8：String 内部是 char[]
// private final char value[];

// Java 9+：String 内部是 byte[]
// private final byte[] value;
// 加上coder字段标记编码：LATIN1(0) 或 UTF16(1)

public class StringMemoryDemo {
    public static void main(String[] args) {
        String ascii = "Hello";  // Latin-1 字符，1字节/字符
        String chinese = "你好";  // 非Latin-1，需要UTF-16

        // String 在 Java 9+ 会自动选择更节省空间的编码
        System.out.println("ASCII字符串长度：" + ascii.length());        // 5
        System.out.println("中文字符串长度：" + chinese.length());        // 2（按字符计）
        System.out.println("字节数演示：");
        System.out.println("ASCII: " + ascii.getBytes().length + " bytes");
        System.out.println("中文: " + java.nio.charset.StandardCharsets.UTF_16.encode(chinese).remaining() + " UTF-16 bytes");
    }
}
```

除了 String，Java 9 还对其他核心类做了类似优化，如 `StringBuilder`、`StringJoiner` 等。

### 34.2.5 HTTP Client API：终于有了标准化的 HTTP 客户端

Java 11 引入了全新的 `java.net.http` 包，提供了**标准化的、异步支持的 HTTP 客户端 API**。在此之前，Java 社区不得不依赖 Apache HttpClient、OkHttp 等第三方库。

```java
import java.net.URI;
import java.net.http.*;

// Java 11+ 的 HTTP Client
public class HttpClientDemo {
    public static void main(String[] args) throws Exception {
        HttpClient client = HttpClient.newHttpClient();

        // GET 请求
        HttpRequest getRequest = HttpRequest.newBuilder()
            .uri(URI.create("https://api.example.com/users/1"))
            .GET()
            .build();

        HttpResponse<String> response = client.send(getRequest, HttpResponse.BodyHandlers.ofString());
        System.out.println("状态码：" + response.statusCode());
        System.out.println("响应体：" + response.body());

        // POST 请求（带 JSON body）
        HttpRequest postRequest = HttpRequest.newBuilder()
            .uri(URI.create("https://api.example.com/users"))
            .header("Content-Type", "application/json")
            .POST(HttpRequest.BodyPublishers.ofString("{\"name\":\"张三\",\"age\":25}"))
            .build();

        HttpResponse<String> postResponse = client.send(postRequest, HttpResponse.BodyHandlers.ofString());
        System.out.println("POST响应：" + postResponse.body());
    }
}
```

支持**异步请求**（特别适合高并发场景）：

```java
import java.net.http.*;
import java.util.concurrent.CompletableFuture;

// 异步 HTTP 请求
HttpClient asyncClient = HttpClient.newAsyncHttpClient();

CompletableFuture<HttpResponse<String>> future =
    asyncClient.sendAsync(
        HttpRequest.newBuilder().uri(URI.create("https://api.example.com/data")).GET().build(),
        HttpResponse.BodyHandlers.ofString()
    );

// 注册回调（不阻塞）
future.thenAccept(resp -> System.out.println("异步收到：" + resp.body()));
System.out.println("主线程继续执行...");
Thread.sleep(1000); // 等待异步完成
```

> **对比**：新的 HTTP Client API 支持 HTTP/1.1 和 HTTP/2，支持同步和异步，支持 WebSocket。比 `HttpURLConnection` 强大太多，建议新代码全部使用这个 API。

### 34.2.6 单文件程序：Java 也能写脚本

Java 11 引入了**单文件源代码程序**运行功能，允许直接运行一个 `.java` 文件，无需先编译。这让 Java 也能像 Python/Node.js 一样写脚本了！

```java
// 创建一个文件：hello.java
// 注意：文件名不需要和类名一致（Java 11+）
public class hello {
    public static void main(String[] args) {
        System.out.println("Hello, Java 11!");
    }
}
```

运行它：

```bash
# 直接运行，无需 javac 编译
java hello.java

# 甚至可以传参数
java hello.java Alice Bob
```

这个功能对于**小型工具、脚本、练习代码**非常方便，再也不用为了跑一个简单的 Java 程序而配置完整的项目结构了。

---

## 34.3 Java 12~17 特性：走向成熟的十年之约

从 Java 12 到 Java 17，Java 进入了"每半年一个大版本"的稳定发布节奏（直到 Java 17 宣布恢复每两年一个大版本的路线）。这一阶段的新特性更加注重**语法智能化**——让代码更简洁、更安全、更表达意图。

### 34.3.1 Switch 表达式：不仅仅是"更优雅的 if"

**Switch 表达式**从 Java 12 开始引入（预览特性），在 Java 14 正式成为标准特性。它彻底改变了 Switch 的使用方式。

传统的 Switch 语句（Java 12 之前）问题很多：忘记 `break` 导致**贯穿**（fall-through）bug、不能返回值、语法啰嗦：

```java
// 传统 Switch：容易出错
int day = 3;
String dayName;
switch (day) {
    case 1:
        dayName = "星期一";
        break;
    case 2:
        dayName = "星期二";
        break;
    case 3:
        dayName = "星期三";
        break;
    // ... 更多 case
    default:
        dayName = "未知";
}
```

Java 14+ 的 Switch 表达式焕然一新：

```java
// Java 14+：箭头表达式，语义清晰，无fall-through
String dayName = switch (day) {
    case 1 -> "星期一";
    case 2 -> "星期二";
    case 3 -> "星期三";
    case 4 -> "星期四";
    case 5 -> "星期五";
    case 6, 7 -> "周末";  // 多个值合并
    default -> "未知";
};

// Switch 表达式也支持多行代码块（需要 yield 返回值）
String dayType = switch (day) {
    case 1, 2, 3, 4, 5 -> {
        String result = "工作日";
        System.out.println("今天是第" + day + "天");
        yield result;  // yield：跳出 switch 并返回值
    }
    case 6, 7 -> "休息日";
    default -> "无效日期";
};
```

> **yield vs return**：在传统的 lambda 表达式 `() -> { return x; }` 中用 `return`，在 switch 表达式的多行代码块中用 `yield`。

### 34.3.2 Records：不可变数据类的"偷懒神器"

**Record** 是 Java 16 正式引入的特性，用于简洁地创建"只读数据类"。如果你写过大量的 getter/setter/equals/hashCode/toString 样板代码，Record 就是来拯救你的。

```java
// 传统 POJO：一个简单的"数据载体"类需要这么多代码
public class Point {
    private final int x;
    private final int y;

    public Point(int x, int y) {
        this.x = x;
        this.y = y;
    }

    public int getX() { return x; }
    public int getY() { return y; }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Point point = (Point) o;
        return x == point.x && y == point.y;
    }

    @Override
    public int hashCode() {
        return java.util.Objects.hash(x, y);
    }

    @Override
    public String toString() {
        return "Point{x=" + x + ", y=" + y + '}';
    }
}
```

用 Record，一行搞定：

```java
// Record：自动生成构造器、getter、equals、hashCode、toString
public record Point(int x, int y) {
    // 自动生成：构造器、getX()、getY()、equals()、hashCode()、toString()
}

// 使用起来超级简单
public class RecordDemo {
    public static void main(String[] args) {
        Point p = new Point(10, 20);

        // 自动生成的 getter，名字是字段名（不是getX()）
        System.out.println(p.x());  // 10
        System.out.println(p.y());  // 20

        // 自动生成的 toString
        System.out.println(p);  // Point[x=10, y=20]

        // 自动生成的 equals 和 hashCode
        Point p2 = new Point(10, 20);
        System.out.println(p.equals(p2));  // true
    }
}
```

Record 还可以有**自定义逻辑**和**额外字段**：

```java
// Record 支持自定义构造器（可以添加校验）
public record Person(String name, int age) {
    // 紧凑构造器：只做校验，不赋值（赋值自动完成）
    public Person {
        if (age < 0 || age > 150) {
            throw new IllegalArgumentException("年龄不合理：" + age);
        }
    }
}

// Record 支持静态字段和方法
public record Circle(double radius) {
    // 静态字段
    static double PI = 3.14159;

    // 静态方法（工厂方法很常见）
    public static Circle unitCircle() {
        return new Circle(1.0);
    }

    // 实例方法
    public double area() {
        return PI * radius * radius;
    }
}
```

> **Record 的限制**：Record 是"名义子类"（nominal subtype），不能继承其他类，不能有可变字段，所有的字段都是 final 的。Record 适合作为**纯数据载体**（DTO、返回值、复合键等）。

### 34.3.3 Pattern Matching（模式匹配）：instanceof 的华丽升级

**Pattern Matching** 从 Java 16 正式引入，让 `instanceof` 检查和类型转换一步到位，并且可以顺带提取对象的"模式"。

```java
// Java 15 之前的 instanceof 和强制类型转换
Object obj = getSomeObject();
if (obj instanceof String) {
    String s = (String) obj;  // 先检查 instanceof，再强制类型转换
    int len = s.length();
}

// Java 16+ 的 Pattern Matching for instanceof
Object obj = getSomeObject();
if (obj instanceof String s) {  // 检查 + 转换 一步完成
    int len = s.length();  // s 在这个 if 块内是 String 类型
}

// 还可以配合 null 检查
if (obj instanceof String s && s.length() > 5) {
    System.out.println("长字符串：" + s);
}
```

模式匹配在 switch 中更加威力强大（Java 21 进一步完善了 switch 的模式匹配，Java 17 时还只是预览）：

```java
// 更强大的 switch 模式匹配（Java 21 正式版，Java 17 是预览版）
static String formatterPatternMatch(Object obj) {
    return switch (obj) {
        case Integer i when i > 0 -> "正整数: " + i;
        case Integer i -> "负整数或零: " + i;
        case String s -> "字符串: " + s;
        case null -> "null值";
        default -> "其他类型: " + obj;
    };
}
```

### 34.3.4 Sealed Classes（密封类）：类的"访问控制"新时代

**Sealed Classes**（密封类）从 Java 17 正式引入，它的作用是：**限制哪些类可以继承或实现某个类/接口**。

在 Java 17 之前，`final` 关键字让类不能被继承，或者不加限制让任何类都能继承。Sealed 类提供了一种中间方案——你可以精确指定"只有这些类可以继承我"。

```java
// 定义一个密封类/接口：只有 permit 列表中的类可以扩展它
public sealed class Shape permits Circle, Rectangle, Triangle {
    // Shape 是密封类的"根"
}

public final class Circle extends Shape {  // final：不能再被继承
    double radius;
}

public sealed class Rectangle extends Shape permits Square {  // Rectangle 还是密封的
    double width, height;
}

public non-sealed class Square extends Rectangle {  // non-sealed：解除密封，可以被任何类继承
    double side;
}

public final class Triangle extends Shape {  // final：不能再被继承
    double base, height;
}

// 密封类层次结构的规则：
// - sealed: 允许子类继承，但子类必须继续限制继承规则
// - final: 禁止任何继承
// - non-sealed: 解除密封，任何类都可以继承
```

密封类有什么用？最大的价值在于**穷举式类型检查**。配合 `switch` 表达式，编译器可以检查是否覆盖了所有可能的情况：

```java
// 当 Shape 是 sealed 且所有子类都是 final/non-sealed 时
// 编译器知道 switch 覆盖了所有可能
static double area(Shape s) {
    return switch (s) {
        case Circle c -> Math.PI * c.radius() * c.radius();
        case Rectangle r -> r.width() * r.height();
        case Triangle t -> 0.5 * t.base() * t.height();
        case Square s -> s.side() * s.side();  // Square 扩展自 Rectangle
    };
    // 编译器可以检查：是否覆盖了所有 Shape 的直接子类？
    // 如果你忘记了一个子类，编译器会报警告
}
```

### 34.3.5 文本块（Text Blocks）：多行字符串的救星

**Text Blocks**（文本块）是 Java 15 引入的预览特性，Java 15 正式确立。它让你可以方便地写多行字符串，而不需要大量的转义和拼接。

```java
// Java 14 之前：JSON 字符串的痛苦
String json = "{\n" +
              "    \"name\": \"张三\",\n" +
              "    \"age\": 25,\n" +
              "    \"skills\": [\"Java\", \"Python\"]\n" +
              "}";

// Java 15+ 的文本块：清爽！
String json = """
    {
        "name": "张三",
        "age": 25,
        "skills": ["Java", "Python"]
    }
    """;

// HTML 示例
String html = """
    <html>
        <body>
            <h1>Hello, Java 15!</h1>
        </body>
    </html>
    """;

// SQL 示例
String sql = """
    SELECT id, name, email
    FROM users
    WHERE age > 18
    ORDER BY name
    """;
```

文本块的格式化规则：

```java
// 文本块的前导缩进由最左边的非空格字符决定
// 结束的 """ 前的空格决定"基准线"
String s = """
    line one    // 前面有4个空格
    line two    // 前面有4个空格
        indented // 前面有8个空格，结果会是4个空格的缩进
    """;         // 这个 """ 前的空格数决定基准线

// \s 保留末尾空格
// \- 去掉末尾自动换行（让最后一行不独立成行）
String formatted = """
    Apples: 5
    Bananas: 3\s
    Oranges: 2
    """;  // Oranges 那行末尾会有2个空格（因为 \s）
```

### 34.3.6 新GC与性能提升：看不见的进化

虽然 Java 12~17 没有像 Java 8 那样革命性的语法变化，但在**垃圾回收器**和**性能**方面持续进化：

| 版本 | GC 特性 |
|------|---------|
| Java 12 | **Shenandoah GC**（低暂停时间GC，与堆大小无关） |
| Java 14 | **JFR (Java Flight Recorder)** 开放为正式API |
| Java 15 | **Shenandoah** 成为正式特性；**ZGC**（可扩展低延迟GC）正式生产可用 |
| Java 17 | **ZGC** 支持并发类卸载；**Flighting GC** 概念提出 |

```java
// 启用特定的 GC（命令行参数）
// -XX:+UseShenandoahGC  启用 Shenandoah
// -XX:+UseZGC            启用 ZGC

// Java 16+ 默认 G1 GC 进一步优化，延迟更低
public class GCDemo {
    public static void main(String[] args) {
        // 运行时获取 GC 信息
        System.out.println("默认GC: " + System.getProperty("java.vm.version"));

        // 推荐使用 ZGC 的场景：需要极低暂停时间（<10ms）的大内存应用
        // 推荐使用 Shenandoah 的场景：需要低暂停时间但堆内存相对较小的应用
    }
}
```

> **实际建议**：除非你有明确的性能问题需要特定GC解决，默认的 G1 GC 已经足够好。不要在没有benchmark数据支撑的情况下过早优化。

---

## 本章小结

本章我们全景式地浏览了 **Java 8 到 Java 17** 十年间最重要的新特性：

| 版本 | 标志性特性 |
|------|-----------|
| **Java 8** | Lambda 表达式、Stream API、Optional、新的 Date/Time API |
| **Java 9** | 模块化系统（Project Jigsaw）、集合工厂方法 |
| **Java 10** | 局部变量类型推断（var） |
| **Java 11** | HTTP Client API、单文件程序运行 |
| **Java 12~17** | Switch 表达式、Records、Pattern Matching、Sealed Classes、文本块 |

**核心学习建议**：

1. **Java 8 是基础**：Lambda 和 Stream 是现代 Java 编程的基石，必须熟练掌握
2. **模块化按需学习**：如果不是构建大型系统，可以先了解概念，具体用时再深入
3. **新语法提升效率**：var、Switch 表达式、Records、文本块都是"偷懒神器"，能显著提升代码可读性和编写效率
4. **保持更新**：Java 的发布节奏加快，每半年都有新东西，保持学习的习惯很重要

> Java 从"古老稳重"到"现代敏捷"的蜕变，这十年是关键。希望本章能帮你建立起对 Java 新特性的系统性认知，在实际项目中游刃有余地选用合适的特性，写出更优雅、更高效的 Java 代码！
