+++
title = "第2章 Java 版本演变史：从 1996 年到 2026 年"
weight = 20
date = "2026-03-30T14:33:56.875+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++
# 第二章 Java 版本演变史：从 1996 年到 2026 年

「如果你在 1996 年告诉别人，2026 年这门语言还会是最流行的编程语言之一，他们可能会觉得你疯了。但 Java 就是这么倔强——别人写胶水代码，它写企业级系统；别人追新特性，它稳扎稳打地演进。Java 的历史，就像一部编程界的『活着的传奇』，每十年一次大变局，每次变局都让程序员又爱又恨。」

## 2.1 Java 1.0 ~ Java 1.4（1996~2002）：蛮荒时代

1996 年 1 月，Sun Microsystems 发布了 Java 1.0。这门语言最初被设计用来做智能家电的控制程序，结果阴差阳错地成为了互联网时代的宠儿。那时的 Java，就像一个刚进城的农村青年——土气、朴实，但浑身是劲。

### 2.1.1 Applet 的兴衰：在浏览器里运行 Java 的梦想

Applet 是 Java 第一个「网红」特性。它允许 Java 程序嵌入到网页中，在浏览器里运行。1996 年，当你打开一个网页，看到一个会动的动画或交互式图表，那大概率就是 Applet 的功劳。

```java
// 一个经典的 Applet 示例
import java.applet.Applet;
import java.awt.Graphics;

public class HelloApplet extends Applet {
    @Override
    public void paint(Graphics g) {
        // 在网页上画出「Hello, World!」
        g.drawString("Hello, Applet World!", 20, 30);
    }
}
```

Applet 的核心理念很超前：**「一次编写，到处运行」**（Write Once, Run Anywhere）。你的程序可以在 Windows、Mac、Linux 的浏览器里同时运行，不用担心兼容性问题。这听起来是不是很像今天的 WebAssembly？

但 Applet 的问题也很明显：需要浏览器安装 Java 插件、安全限制让人抓狂、加载速度慢如蜗牛。随着 HTML5、CSS3 和 JavaScript 的崛起，Applet 逐渐被淘汰。下面这条时间线值得记准确：

- **2015 年 9 月**：Chrome 45 移除了 NPAPI 插件支持，Java 插件就此在 Chrome 中失效（不是 2016 年）
- **2017 年**：JDK 9 正式把 Applet API 标记为废弃（JEP 289）
- **2018 年**：JDK 11 移除了 JDK 自带的浏览器插件与 Java Web Start 部署栈（不是"Java 11 废弃 Applet API"）
- **2021 年**：JDK 17 通过 JEP 398 把 Applet API 标记为"废弃并计划移除"

Applet 成了 Java 历史上第一个「被拍死在沙滩上」的前浪。顺带说一句：`java.applet` 包在 JDK 25 里**仍然存在**，只是带着"已过时、待删除"的标记，所以今天用 `javac` 编译上面的示例只会收到一条警告。

> **小知识**：Applet 的遗产影响深远。后来 Android 的 App 运行环境、Java Web Start 技术，都能看到 Applet 的影子。

### 2.1.2 JDBC 的诞生：Java 连接数据库

在 Java 出现之前，连接数据库是个头疼的问题。每种数据库都有自己的 API——连接 MySQL 用一套，连接 Oracle 用另一套，程序员需要写大量重复代码。JDBC（Java Database Connectivity）的出现，彻底改变了这一切。

```java
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.Statement;

public class JdbcDemo {
    public static void main(String[] args) {
        // 有了 JDBC，不管你用 MySQL、Oracle 还是 PostgreSQL
        // 代码风格基本一致，这就是「统一的数据库访问接口」
        String url = "jdbc:mysql://localhost:3306/mydb";
        String user = "root";
        String password = "123456";

        try (Connection conn = DriverManager.getConnection(url, user, password);
             Statement stmt = conn.createStatement();
             ResultSet rs = stmt.executeQuery("SELECT * FROM users")) {

            while (rs.next()) {
                System.out.println("用户名: " + rs.getString("name"));
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```

JDBC 的设计理念非常优雅：**定义一套接口，让数据库厂商自己去实现**。程序员只需要学会 JDBC 这套 API，就能操作任何支持 JDBC 的数据库。这，就是面向接口编程的魅力。

### 2.1.3 Servlet 的出现：Java 做网站的起点

1997 年，Java Servlet API 发布，Java 正式进军 Web 开发领域。在那个 PHP 和 ASP 统治 web 开发的年代，Servlet 以其「跨平台」和「稳定性」的优势，逐渐成为企业级 Web 开发的首选。

```java,ignore
// 这个例子需要引入 Jakarta Servlet API（jakarta.servlet-api）才能编译，
// 单文件直接 javac 会因为找不到包而报错，这里只做概念演示。
import java.io.IOException;
import java.io.PrintWriter;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

// Servlet 是 Java Web 开发的基础，所有框架都建立在其之上
public class HelloServlet extends HttpServlet {
    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp)
            throws ServletException, IOException {
        resp.setContentType("text/html;charset=UTF-8");
        PrintWriter out = resp.getWriter();
        out.println("<html><body>");
        out.println("<h1>Hello, Servlet!</h1>");
        out.println("</body></html>");
    }
}
```

Servlet 的出现为后来 Java Web 框架的繁荣奠定了基础。Struts、Spring MVC、Hibernate 这些大名鼎鼎的框架，都是站在 Servlet 的肩膀上发展起来的。可以说，没有 Servlet，就没有今天 Java 在 Web 领域的地位。

### 2.1.4 JNDI、JavaMail、EJB——企业 Java 的雏形

1999 年，Java 进入了企业计算领域。Sun 公司推出了一整套企业级 API，构成了 Java EE（当时还叫 J2EE）的核心：

- **JNDI**（Java Naming and Directory Interface）：目录服务接口，简单说就是「帮你找东西的 API」。通过 JNDI，你可以找到数据库连接池、邮件服务器、企业内部的分布式服务等。想象一下，它就像一个电话本，你不用记住每个服务的具体地址，只需要记住它们的名字，JNDI 帮你查。

- **JavaMail**：处理电子邮件的 API，支持发送邮件（SMTP）、接收邮件（POP3/IMAP）。2000 年前后，邮件是企业通信的主流方式，JavaMail 让程序发送邮件变得轻而易举。

- **EJB**（Enterprise JavaBeans）：一种分布式组件规范，用于构建企业级应用。EJB 的理念很超前：**业务逻辑封装成组件，部署到服务器上，多个应用可以共享调用**。但说实话，EJB 有点过于复杂，配置 XML 能写到你怀疑人生。这也间接促成了 Spring 框架的崛起——「轻量级」的 Spring 对比「重量级」的 EJB，就像电动车对比燃油车。

---

## 2.2 Java 5 / Java 1.5（代号 Tiger，2004）：语法革命

如果说 Java 1.0 到 1.4 是「蛮荒时代」，那么 Java 5 就是「文艺复兴」。这一版的更新力度之大，堪称 Java 历史上最重要的一次版本升级，没有之一。

Java 5 引入了大量革命性的语法特性，让 Java 从一门「过程式面向对象语言」彻底蜕变为「现代编程语言」。很多人说「Java 8 是最重要的版本」，但 Java 5 才是真正的奠基者——没有泛型、没有注解、没有枚举，Java 8 的 Lambda 就是空中楼阁。

### 2.2.1 泛型（Generics）：写 `List<String>` 而不是 `List`，让代码更安全

在泛型出现之前，`List` 可以存放任何类型的对象，取出来的时候需要强制类型转换，还容易出现 `ClassCastException`。

```java
// 泛型之前的代码（危险操作，需要强制类型转换）
List list = new ArrayList();
list.add("Hello");
String s = (String) list.get(0);  // 需要强制转换，万一放错了类型就炸

// 泛型之后的代码（安全、优雅）
List<String> list = new ArrayList<>();
list.add("Hello");
String s = list.get(0);  // 不需要强制转换，编译器帮你检查类型
```

泛型的核心思想是**「参数化类型」**——`List<String>` 中的 `String` 就是类型参数。有了泛型，编译器能在编译阶段发现类型错误，而不是等到运行时才崩溃。泛型让集合操作变得既安全又简洁，是 Java 类型系统的一次重大升级。

```java
// 泛型方法示例
public static <T> T getFirst(List<T> list) {
    if (list == null || list.isEmpty()) {
        return null;
    }
    return list.get(0);
}

// 泛型接口示例（注意别和 JDK 自带的 java.lang.Comparable 撞名，这里叫 MyComparable）
public interface MyComparable<T> {
    int compareTo(T other);
}

// 多个类型参数的泛型（同样避免和 java.util.HashMap 撞名）
public class MyMap<K, V> {
    // K 是键的类型，V 是值的类型
}
```

### 2.2.2 注解（Annotations）：`@Override`、`@Deprecated`——代码的元数据

注解是 Java 5 引入的「语法糖」，它允许你给代码添加元数据（metadata）。简单理解，注解就是「写在代码上的标签」。

```java
import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

public class AnnotationDemo {

    // 自定义注解：RUNTIME 表示运行时仍可反射读取，METHOD 表示只能标在方法上
    @Retention(RetentionPolicy.RUNTIME)
    @Target(ElementType.METHOD)
    public @interface MyAnnotation {
        String value() default "默认值";  // 注解的属性，可以带默认值
        int count() default 1;
    }

    // @Override 告诉编译器：这个方法是重写的父类方法。
    // 如果方法名拼错、或返回值与父类不一致，编译器会直接报错。
    @Override
    public String toString() {
        return "AnnotationDemo";
    }

    // @Deprecated 标记这个方法已经过时，别人调用时编译器会给出警告
    @Deprecated
    public void oldMethod() {
    }

    // 使用自定义注解
    @MyAnnotation(value = "测试", count = 3)
    public void annotatedMethod() {
        System.out.println("这个方法被我注解了！");
    }

    public static void main(String[] args) {
        AnnotationDemo demo = new AnnotationDemo();
        System.out.println(demo);              // AnnotationDemo
        demo.annotatedMethod();                // 这个方法被我注解了！
    }
}
```

注解的用途非常广泛：Spring 用来做依赖注入、JUnit 用来标记测试方法、Hibernate 用来映射数据库表……没有注解，现代 Java 框架至少少一半威力。

### 2.2.3 枚举（Enum）：定义有限常量的优雅方式

在 Java 5 之前，定义常量是这样的：

```java
// 苦逼的常量定义方式
public static final int SPRING = 1;
public static final int SUMMER = 2;
public static final int AUTUMN = 3;
public static final int WINTER = 4;
```

这种方式容易写错（比如 `if (season == 5)` 编译器不会报错），也没有类型安全。枚举出现后：

```java
public class SeasonDemo {

    // 枚举：类型安全、有属性、有方法
    public enum Season {
        SPRING("春天", 1),
        SUMMER("夏天", 2),
        AUTUMN("秋天", 3),
        WINTER("冬天", 4);

        private final String chineseName;
        private final int order;

        Season(String chineseName, int order) {
            this.chineseName = chineseName;
            this.order = order;
        }

        public String getChineseName() { return chineseName; }
        public int getOrder() { return order; }
    }

    public static void main(String[] args) {
        Season s = Season.SPRING;

        // 传统 switch 写法（Java 5 起就支持），别忘了一个个 break
        switch (s) {
            case SPRING:
                System.out.println("春暖花开");
                break;
            case SUMMER:
                System.out.println("烈日炎炎");
                break;
            case AUTUMN:
                System.out.println("秋高气爽");
                break;
            case WINTER:
                System.out.println("冰天雪地");
                break;
        }

        // Java 14+ 的箭头形式更简洁，不需要 break，也不会意外穿透
        switch (s) {
            case SPRING -> System.out.println("春暖花开");
            case SUMMER -> System.out.println("烈日炎炎");
            case AUTUMN -> System.out.println("秋高气爽");
            case WINTER -> System.out.println("冰天雪地");
        }
    }
}
```

枚举不仅仅是常量集合，它还是一个完整的类——可以有属性、方法、构造函数，甚至可以实现接口。Java 的枚举还能被用于 `switch` 语句、作为 `Map` 的 key、放入集合中，简直是万能选手。

### 2.2.4 自动装箱/拆箱（Auto Boxing/Unboxing）：`int` ↔ `Integer` 自动转换

Java 5 之前，基本类型和包装类型之间的转换需要手动进行：

```java
// 手动装箱：把 int 转成 Integer
int primitive = 42;
Integer wrapper = Integer.valueOf(primitive);  // 手动装箱
int back = wrapper.intValue();                  // 手动拆箱
```

Java 5 引入了自动装箱/拆箱，编译器自动帮你完成转换：

```java
// 自动装箱：编译器自动转换为 Integer.valueOf(42)
Integer boxed = 42;

// 自动拆箱：编译器自动转换为 boxed.intValue()
int unboxed = boxed;

// 集合里只能放对象，int 会自动装箱
List<Integer> numbers = new ArrayList<>();
numbers.add(1);      // 自动装箱：Integer.valueOf(1)
numbers.add(2);
numbers.add(3);

int sum = 0;
for (Integer n : numbers) {
    sum += n;        // 自动拆箱：n.intValue()
}
System.out.println("Sum = " + sum);
```

看起来很方便，但有个坑要注意：**自动装箱可能产生额外的对象，导致性能问题**。比如：

```java
// 性能陷阱：循环中的自动装箱
Long sum = 0L;  // 注意是 Long，不是 long
for (int i = 0; i < 1000000; i++) {
    sum += i;   // 每次 += 都会创建一个新的 Long 对象！
}
// 正确做法：用 long sum = 0L;
```

### 2.2.5 foreach 循环：`for (Type var : collection)` 更简洁

传统的 `for` 循环写起来有点啰嗦：

```java
// 传统 for 循环
for (Iterator<String> i = list.iterator(); i.hasNext(); ) {
    String s = i.next();
    System.out.println(s);
}

// 更简洁的写法
for (String s : list) {
    System.out.println(s);
}
```

foreach（增强 for 循环）既可以遍历数组，也可以遍历实现了 `Iterable` 接口的集合。它让代码更简洁、可读性更高，但有个限制：**无法获取当前元素的索引**（如果需要，用传统 `for` 循环）。

```java
// 遍历数组
String[] names = {"Alice", "Bob", "Charlie"};
for (String name : names) {
    System.out.println(name);
}

// 遍历集合
List<String> namesList = Arrays.asList("Alice", "Bob", "Charlie");
for (String name : namesList) {
    System.out.println(name);
}

// 遍历 Map（需要用 entrySet）
Map<String, Integer> ages = new HashMap<>();
ages.put("Alice", 25);
ages.put("Bob", 30);
for (Map.Entry<String, Integer> entry : ages.entrySet()) {
    System.out.println(entry.getKey() + " -> " + entry.getValue());
}
```

### 2.2.6 可变参数（Varargs）：`String... args`，参数数量可变

可变参数允许你传入零个或多个同类型的参数。在 `printf` 风格的 API 中特别有用：

```java
// 可变参数方法
public static void printAll(String... names) {
    for (String name : names) {
        System.out.println(name);
    }
}

// 调用方式很灵活
printAll();                      // 0 个参数
printAll("Alice");               // 1 个参数
printAll("Bob", "Charlie");      // 2 个参数
printAll("David", "Eve", "Frank", "Grace");  // 多个参数

// 可变参数实际上就是个语法糖，底层是数组
// 编译器会把 String... names 变成 String[] names
```

可变参数让方法调用更灵活，尤其适合「参数数量不确定」的场景，比如日志记录、错误处理、格式化输出等。

### 2.2.7 静态导入（Static Import）：`import static java.lang.Math.*;`

静态导入让你可以直接使用静态方法或静态字段，而不用写类名：

```java
// 没有静态导入之前
double area = Math.PI * Math.pow(radius, 2);
double sinValue = Math.sin(Math.PI / 2);
double maxValue = Math.max(Math.max(a, b), c);

// 使用静态导入之后
import static java.lang.Math.PI;
import static java.lang.Math.pow;
import static java.lang.Math.sin;
import static java.lang.Math.max;

double area = PI * pow(radius, 2);
double sinValue = sin(PI / 2);
double maxValue = max(max(a, b), c);

// 或者直接 import static java.lang.Math.*; 导入 Math 所有静态成员
```

静态导入虽好，但别滥用——如果两个类有同名的静态方法，静态导入会让你分不清哪个是哪个。

### 2.2.8 并发包（J.U.C）：`java.util.concurrent`，并发编程的基础

Java 5 引入了 `java.util.concurrent` 包，简称 J.U.C。这是 Java 并发编程的一次革命，提供了大量高质量的并发工具类：

- **`ExecutorService`**：线程池，告别 `new Thread()` 的苦海
- **`CountDownLatch`**：倒计时门闩，多线程协调
- **`CyclicBarrier`**：循环栅栏，线程间的同步点
- **`Semaphore`**：信号量，控制对资源的访问数量
- **`ConcurrentHashMap`**：线程安全的 HashMap，并发性能秒杀 Hashtable

```java
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;

public class ConcurrentDemo {
    public static void main(String[] args) throws InterruptedException {
        // 创建一个固定大小的线程池，比如同时执行 3 个任务
        ExecutorService executor = Executors.newFixedThreadPool(3);

        // CountDownLatch：等所有线程完成后再汇总结果
        CountDownLatch latch = new CountDownLatch(3);

        // 提交 3 个任务
        executor.submit(() -> {
            System.out.println("任务 A 完成");
            latch.countDown();  // 计数减一
        });
        executor.submit(() -> {
            System.out.println("任务 B 完成");
            latch.countDown();
        });
        executor.submit(() -> {
            System.out.println("任务 C 完成");
            latch.countDown();
        });

        // 等待所有任务完成
        latch.await(10, TimeUnit.SECONDS);

        // 关闭线程池
        executor.shutdown();
        System.out.println("所有任务完成，主线程继续执行");
    }
}
```

J.U.C 的出现，让 Java 的并发编程从「刀耕火种」进入「工业时代」。在它之前，程序员需要手动管理线程、担心死锁、性能调优；有了 J.U.C，这些问题变得可控多了。

---

## 2.3 Java 6 / Java 1.6（代号 Mustang，2006）：稳步前进

Java 6 没有像 Java 5 那样的大规模语法升级，而是把重心放在了**性能优化**和**企业级特性增强**上。这一版属于「修修补补又一年」的类型，但每一处改进都很实用。

### 2.3.1 性能提升和 Web Services 增强

Java 6 在 JVM 层面做了大量优化，启动速度更快、垃圾回收更高效。Web Services 支持也得到了显著增强：

- **JAX-WS 2.0**：Web Services 的标准 API，支持 SOAP 协议
- **JAXB 2.0**：Java Architecture for XML Binding，XML 和 Java 对象互转
- **WSIT（Web Services Interoperability Technologies）**：提升不同厂商 Web Services 之间的互操作性

```java
// Java 6 的 Web Services 示例
// ⚠️ 提醒：javax.xml.ws 这套 Java EE 模块在 JDK 11 已被移除（JEP 320）。
//    所以这段代码在 JDK 6~10 上可以直接跑，在 JDK 11+ 上需要自己引入
//    相应的 Jakarta XML Web Services 依赖（包名也从 javax.* 变成了 jakarta.*）。
import javax.xml.ws.Endpoint;

public class SimpleWebService {
    // 发布一个简单的 Web Service
    public String sayHello(String name) {
        return "Hello, " + name + "!";
    }

    public static void main(String[] args) {
        // 一行代码发布 Web Service（Java 6 的便捷之处）
        Endpoint.publish("http://localhost:8080/hello",
                        new SimpleWebService());
        System.out.println("Web Service 已发布在 http://localhost:8080/hello?wsdl");
    }
}
```

### 2.3.2 Java ME 和 Java EE 的分离

很多人以为"三个版本"是 Java 6 才有的，其实不正确——J2SE / J2EE / J2ME 这套划分从 **1999 年**就有了，Java 6 前后只是把名字统一改成了 Java SE / Java EE / Java ME。我们今天熟悉的三个方向是：

- **Java SE**（Standard Edition）：标准版，桌面和服务器应用
- **Java EE**（Enterprise Edition）：企业版，基于 SE 的企业级扩展
- **Java ME**（Micro Edition）：微型版，用于手机和嵌入式设备

这种分离让各平台可以独立演进，减少了互相牵绊。Java ME 后来主要用在 IoT 设备上，而 Java EE 则成为企业级应用开发的事实标准。

### 2.3.3 Scripting 脚本语言支持

Java 6 引入了 **Scripting API**（`javax.script`），允许 Java 程序嵌入其他脚本语言，比如 JavaScript、Python（通过 Jython）、Ruby（通过 JRuby）等。

```java
import javax.script.ScriptEngine;
import javax.script.ScriptEngineManager;
import javax.script.Invocable;

public class ScriptingDemo {
    public static void main(String[] args) throws Exception {
        ScriptEngineManager manager = new ScriptEngineManager();
        // 获取 JavaScript 引擎：
        //   Java 6/7 内置的是 Rhino，Java 8 换成了 Nashorn。
        //   ⚠️ 但 Nashorn 在 Java 11 被标记废弃（JEP 335），
        //      并在 Java 15 被彻底移除（JEP 372）。
        //      所以这段代码在 JDK 15 及以上会找不到引擎，engine 会是 null。
        //      今天要用脚本引擎，需要自己引入 GraalVM JS 等第三方实现。
        ScriptEngine engine = manager.getEngineByName("JavaScript");

        // 执行 JavaScript 代码
        engine.eval("var message = 'Hello from JavaScript!';");
        engine.eval("print(message)");

        // 在 JavaScript 中定义函数，然后在 Java 中调用
        engine.eval("function add(a, b) { return a + b; }");
        Invocable invocable = (Invocable) engine;

        Object result = invocable.invokeFunction("add", 10, 20);
        System.out.println("JavaScript add(10, 20) = " + result);
    }
}
```

这个特性让 Java 拥有了「动态脚本」能力，可以用来实现规则引擎、模板引擎，或者让非程序员编写业务逻辑。

---

## 2.4 Java 7（代号 Dolphin，2011）：量变到质变

Java 7 是 Oracle 收购 Sun 后发布的第一个大版本。它带来了不少实用的新特性，虽然没有 Java 5 那样革命性，但每一项都让代码更简洁。

### 2.4.1 try-with-resources：不用手动关流，资源自动关闭

在 Java 7 之前，关闭资源需要写 `finally` 块，还容易遗漏：

```java
// Java 7 之前的资源关闭（繁琐、易错）
BufferedReader reader = null;
try {
    reader = new BufferedReader(new FileReader("file.txt"));
    String line = reader.readLine();
    System.out.println(line);
} catch (IOException e) {
    e.printStackTrace();
} finally {
    if (reader != null) {
        try {
            reader.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
```

Java 7 引入了 **try-with-resources** 语法，资源会自动关闭，代码简洁到哭：

```java
// Java 7+ 的 try-with-resources（优雅、安全）
try (BufferedReader reader = new BufferedReader(new FileReader("file.txt"))) {
    String line = reader.readLine();
    System.out.println(line);
} catch (IOException e) {
    e.printStackTrace();
}
// 不用写 finally，编译器帮你自动关闭资源
```

只要类实现了 `AutoCloseable` 接口（`Closeable` 的父接口），就可以用 try-with-resources。需要关闭多个资源？用分号隔开：

```java
// 同时管理多个资源
try (BufferedReader reader = new BufferedReader(new FileReader("input.txt"));
     BufferedWriter writer = new BufferedWriter(new FileWriter("output.txt"))) {
    String line;
    while ((line = reader.readLine()) != null) {
        writer.write(line);
        writer.newLine();
    }
}  // 两个资源都会自动关闭
```

### 2.4.2 switch 支持 String：再也不用 if-else 链判断字符串了

这是无数 Java 程序员翘首以盼的功能！

```java
// Java 7 之前：字符串判断只能用 if-else 链
String day = "MONDAY";
if (day.equals("MONDAY")) {
    System.out.println("星期一");
} else if (day.equals("TUESDAY")) {
    System.out.println("星期二");
} else if (day.equals("WEDNESDAY")) {
    System.out.println("星期三");
} else if (day.equals("THURSDAY")) {
    System.out.println("星期四");
} else if (day.equals("FRIDAY")) {
    System.out.println("星期五");
} else if (day.equals("SATURDAY")) {
    System.out.println("星期六");
} else if (day.equals("SUNDAY")) {
    System.out.println("星期日");
} else {
    System.out.println("未知日期");
}

// Java 7+：switch 原生支持 String（Java 7 时代只有冒号写法）
switch (day) {
    case "MONDAY":
        System.out.println("星期一");
        break;
    case "TUESDAY":
        System.out.println("星期二");
        break;
    case "WEDNESDAY":
        System.out.println("星期三");
        break;
    case "THURSDAY":
        System.out.println("星期四");
        break;
    case "FRIDAY":
        System.out.println("星期五");
        break;
    case "SATURDAY":
        System.out.println("星期六");
        break;
    case "SUNDAY":
        System.out.println("星期日");
        break;
    default:
        System.out.println("未知日期");
        break;
}
// 补充：Java 14+ 之后才有箭头写法 case "MONDAY" -> ...
```

switch 支持 String 后，代码可读性大幅提升，尤其是处理枚举、状态码、命令类型等场景。

### 2.4.3 钻石操作符（Diamond Operator）：`new ArrayList<>()` 不用写两边类型

泛型类型推断让代码更简洁：

```java
// Java 7 之前：泛型类型要写两遍
Map<String, List<Map<String, Integer>>> complexMap =
    new HashMap<String, List<Map<String, Integer>>>();
// 看这一行就眼晕……

// Java 7+：钻石操作符，编译器自动推断类型
Map<String, List<Map<String, Integer>>> complexMap = new HashMap<>();
// 简洁多了！
```

`<>` 因为长得像钻石，所以叫 Diamond Operator。编译器会根据左边的类型自动推断右边的泛型参数。

### 2.4.4 NIO.2 文件系统：更强大的文件操作 API

Java 7 引入了新的文件操作 API，提供了更强大的文件系统访问能力：

- **`Path`**：表示文件路径，比 `File` 更灵活
- **`Files`**：文件操作工具类，复制、移动、读取、写入一条龙
- **`FileVisitor`**：遍历目录树
- **`WatchService`**：监控文件变化

```java
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.io.IOException;
import java.util.List;

public class Nio2Demo {
    public static void main(String[] args) throws IOException {
        Path source = Paths.get("input.txt");
        Path target = Paths.get("output.txt");

        // 复制文件（一行代码搞定）
        Files.copy(source, target, StandardCopyOption.REPLACE_EXISTING);

        // 读取文件所有行
        List<String> lines = Files.readAllLines(source);
        for (String line : lines) {
            System.out.println(line);
        }

        // 判断文件属性
        System.out.println("文件大小: " + Files.size(source) + " 字节");
        System.out.println("是否可读: " + Files.isReadable(source));
        System.out.println("是否可执行: " + Files.isExecutable(source));

        // 创建临时文件/目录
        Path tempFile = Files.createTempFile("prefix", ".tmp");
        Path tempDir = Files.createTempDirectory("dir");
        System.out.println("临时文件: " + tempFile);
        System.out.println("临时目录: " + tempDir);
    }
}
```

NIO.2 的 API 比老的 `File` 类好用太多，终于可以愉快地操作文件和目录了！

### 2.4.5 二进制字面量：`0b1010` 或 `0B1010`

Java 7 开始支持二进制字面量，对底层编程、网络协议、位运算特别有用：

```java
// 十进制
int decimal = 42;

// 十六进制（之前就有）
int hex = 0x2A;

// 八进制（之前就有）
int octal = 052;

// 二进制字面量（Java 7 新增）
int binary = 0b101010;

// Java 7+ 还可以给下划线分隔（类似数学中的千位分隔符）
int bigNumber = 1_000_000;           // 1000000
int binaryWithUnderscores = 0b1010_1010;  // 170
int hexWithUnderscores = 0xDEAD_BEEF;      // 注意：int 放不下这个值，实际存的是 -559038737
long bigHex = 0xDEAD_BEEFL;                // 想要 3735928559 这个正数，得用 long + L 后缀
```

下划线分隔符可以让大数字更易读，但并不是"随便加"：它**不能出现在数字的开头或结尾**，也**不能紧挨着小数点、`0x`/`0b` 前缀或 `L`/`f` 这类后缀**。比如 `1_000_000`、`0b1010_1010` 合法，而 `_1000`、`1000_`、`0x_FF` 都是错的。

### 2.4.6 异常处理改进：同一 catch 可以捕获多种异常

Java 7 之前，捕获多种异常需要写多个 catch 块：

```java
// Java 7 之前
try {
    // 可能抛出多种异常的操作
} catch (IOException e) {
    e.printStackTrace();
} catch (SQLException e) {
    e.printStackTrace();
} catch (ClassNotFoundException e) {
    e.printStackTrace();
}

// Java 7+：一个 catch 捕获多种异常（用 | 分隔）
try {
    // 可能抛出多种异常的操作
} catch (IOException | SQLException | ClassNotFoundException e) {
    // 注意：e 在这里实际上是 final 的，不能重新赋值
    e.printStackTrace();
    // 你可以通过 instanceof 判断具体类型
    if (e instanceof IOException) {
        System.out.println("IO 错误");
    } else if (e instanceof SQLException) {
        System.out.println("数据库错误");
    }
}
```

这个特性叫 **multi-catch**，让异常处理代码更简洁。

### 2.4.7 Fork/Join 框架：并行计算的基础

Fork/Join 框架是 Java 7 引入的并行计算框架，专门用于「分而治之」类型的任务——把大任务拆成小任务，并行执行，最后合并结果。

```java
import java.util.concurrent.ForkJoinPool;
import java.util.concurrent.RecursiveTask;

public class ForkJoinDemo {
    // 计算 1 到 n 的和，使用分治策略
    static class SumTask extends RecursiveTask<Long> {
        private final long from;
        private final long to;
        private static final long THRESHOLD = 10_000;  // 阈值

        SumTask(long from, long to) {
            this.from = from;
            this.to = to;
        }

        @Override
        protected Long compute() {
            // 如果范围足够小，直接计算
            if (to - from <= THRESHOLD) {
                long sum = 0;
                for (long i = from; i <= to; i++) {
                    sum += i;
                }
                return sum;
            }

            // 拆分任务
            long mid = (from + to) / 2;
            SumTask left = new SumTask(from, mid);
            SumTask right = new SumTask(mid + 1, to);

            // 叉出子任务，然后合并结果
            left.fork();
            right.fork();
            return left.join() + right.join();
        }
    }

    public static void main(String[] args) {
        ForkJoinPool pool = ForkJoinPool.commonPool();
        long n = 1_000_000;

        long start = System.currentTimeMillis();
        long result = pool.invoke(new SumTask(1, n));
        long end = System.currentTimeMillis();

        System.out.println("计算 1 到 " + n + " 的和");
        System.out.println("结果: " + result);
        System.out.println("耗时: " + (end - start) + " ms");
    }
}
```

Fork/Join 是后来 Java 8 Stream 并行流和 `CompletableFuture` 的底层基础。

---

## 2.5 Java 8（代号 Spider，2014）：现代化 Java 的起点——最重要版本

「Java 8 之前和 Java 8 之后，是两种完全不同的编程体验。」——不知道是谁说的，但每个 Java 程序员都会认同。

Java 8 是 Oracle 收购 Sun 后真正意义上的「现代化 Java」。它引入了 Lambda 表达式、Stream API、Optional 类、新的日期时间 API……这些特性彻底改变了 Java 的编程风格，让 Java 从一门「老派」语言，华丽转身为「现代」语言。

Java 8 是 Java 历史上最重要的版本，没有之一。即使到了 2026 年，很多公司的生产环境依然跑在 Java 8 上。

### 2.5.1 Lambda 表达式：匿名内部类的革命，代码从 10 行变成 1 行

Lambda 表达式是 Java 8 最核心的特性，它让函数式编程成为可能。在 Lambda 之前，Java 只有「面向对象」一条路；有了 Lambda，「函数」也可以作为一等公民了。

```java
// Java 7 的匿名内部类（啰嗦、冗长）
Runnable r1 = new Runnable() {
    @Override
    public void run() {
        System.out.println("Hello, Lambda!");
    }
};

// Java 8 的 Lambda 表达式（简洁、优雅）
Runnable r2 = () -> System.out.println("Hello, Lambda!");

// 执行
r2.run();
```

Lambda 的语法规则：

```java
// 完整语法：(参数列表) -> { 方法体 }
// 1. 参数类型可省略（编译器推断）
// 2. 单个参数时，括号可省略
// 3. 单行方法体时，return 和大括号可省略（隐含 return）

// 示例：各种 Lambda 形式
Runnable r1 = () -> System.out.println("无参数");

Consumer<String> c1 = (String s) -> System.out.println(s);  // 完整形式
Consumer<String> c2 = s -> System.out.println(s);             // 类型推断
Consumer<String> c3 = System.out::println;                    // 方法引用

// 多参数
Comparator<String> cmp = (s1, s2) -> s1.length() - s2.length();

// 有方法体
Predicate<Integer> p = n -> {
    if (n > 0) return true;
    return false;
};

// 带返回
Function<String, Integer> f = s -> s.length();
```

### 2.5.2 Stream API：集合操作的新方式，链式调用风靡编程界

Stream API 是 Java 8 的另一大杀器。它让你可以用「流」的方式处理集合——链式调用、函数式风格、一行代码搞定过滤/映射/排序/统计。

```java
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

public class StreamDemo {
    public static void main(String[] args) {
        List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5, 6, 7, 8, 9, 10);

        // 传统方式：过滤偶数，平方后求和
        int sum = 0;
        for (Integer n : numbers) {
            if (n % 2 == 0) {
                sum += n * n;
            }
        }
        System.out.println("传统方式: " + sum);

        // Stream 方式：一行搞定
        int streamSum = numbers.stream()
            .filter(n -> n % 2 == 0)      // 过滤偶数
            .mapToInt(n -> n * n)          // 平方
            .sum();                         // 求和
        System.out.println("Stream 方式: " + streamSum);

        // 更多示例
        List<String> names = Arrays.asList("Alice", "Bob", "Charlie", "David");

        // 找出长度大于 4 的名字，转大写，排序
        List<String> result = names.stream()
            .filter(name -> name.length() > 4)
            .map(String::toUpperCase)
            .sorted()
            .collect(Collectors.toList());
        System.out.println("结果: " + result);  // [ALICE, CHARLIE, DAVID]

        // 统计
        long count = names.stream().count();
        String longest = names.stream().max((a, b) -> a.length() - b.length()).orElse("");
        System.out.println("最长名字: " + longest);

        // 并行流（充分利用多核）
        long parallelSum = numbers.parallelStream()
            .filter(n -> n % 2 == 0)
            .mapToInt(n -> n * n)
            .sum();
        System.out.println("并行流结果: " + parallelSum);
    }
}
```

Stream 的操作分为**中间操作**（返回 Stream）和**终端操作**（返回结果）。常见的中间操作有 `filter`、`map`、`flatMap`、`distinct`、`sorted`、`limit`、`skip`；终端操作有 `forEach`、`collect`、`count`、`sum`、`reduce`、`min/max/findFirst/findAny`。

### 2.5.3 Optional 类：消灭 `NullPointerException` 的希望

`NullPointerException` 是 Java 程序员最常遇到的异常，江湖人称「十亿美金的错误」。Optional 提供了一种更优雅的空值处理方式。

```java
import java.util.Optional;

public class OptionalDemo {
    public static void main(String[] args) {
        // 创建 Optional
        Optional<String> empty = Optional.empty();
        Optional<String> name = Optional.of("Alice");  // 不能传 null
        Optional<String> nullable = Optional.ofNullable(null);  // 可以传 null

        // 安全地获取值
        String value = nullable.orElse("默认值");  // 为空就返回默认值
        String value2 = nullable.orElseGet(() -> "计算出来的默认值");  // 延迟计算版本
        // orElseThrow：为空就抛异常。注意 nullable 本身是空的，
        // 如果写成 nullable.orElseThrow(...) 这一行会立刻抛异常、程序直接中断，
        // 所以这里换成有值的 name 来演示：
        String value3 = name.orElseThrow(() -> new RuntimeException("不能为空！"));
        System.out.println("value / value2 / value3 = " + value + " / " + value2 + " / " + value3);

        // ifPresent：值存在时执行
        name.ifPresent(n -> System.out.println("名字是: " + n));

        // map 转换
        Optional<Integer> length = name.map(String::length);
        System.out.println("名字长度: " + length.orElse(0));

        // flatMap 链式调用
        Optional<String> result = name
            .map(String::toUpperCase)
            .filter(s -> s.length() > 3)
            .flatMap(s -> Optional.of("Hello, " + s));
        System.out.println(result.orElse("没结果"));

        // 链式操作示例：安全地获取用户所在城市名称
        String city = getUser()
            .flatMap(User::getAddress)
            .flatMap(Address::getCity)
            .map(City::getName)
            .orElse("未知城市");

        // 传统方式需要多层判断
        // if (user != null) {
        //     if (user.getAddress() != null) {
        //         if (user.getAddress().getCity() != null) {
        //             city = user.getAddress().getCity().getName();
        //         }
        //     }
        // }
    }

    // 示例方法
    static Optional<User> getUser() {
        return Optional.of(new User(new Address(new City("北京"))));
    }

    // 内部类示例
    static class User {
        private Address address;
        User(Address address) { this.address = address; }
        Optional<Address> getAddress() { return Optional.ofNullable(address); }
    }
    static class Address {
        private City city;
        Address(City city) { this.city = city; }
        Optional<City> getCity() { return Optional.ofNullable(city); }
    }
    static class City {
        private String name;
        City(String name) { this.name = name; }
        String getName() { return name; }
    }
}
```

Optional 的核心思想是：**「让空值检查变得可视化、可链式操作」**。虽然 Optional 不能完全消灭 NPE，但它让代码更清晰、更安全。

### 2.5.4 接口的默认方法（Default Methods）：接口可以写实现了

Java 8 之前，接口只能声明方法，不能写实现。Java 8 引入了 `default` 方法，让接口可以包含具体实现。

```java
// Java 8 之前的接口（这里叫 AnimalOld，只是为了不和下面的接口重名）
interface AnimalOld {
    void speak();  // 抽象方法，必须实现
}

// Java 8+ 的接口可以有默认方法
interface Animal {
    void speak();  // 抽象方法

    default void breathe() {  // 默认方法，有默认实现
        System.out.println("呼吸中...");
    }

    default void sleep() {
        System.out.println("睡着了zzZ");
    }
}

// 实现类只需要关注自己特有的行为
class Dog implements Animal {
    @Override
    public void speak() {
        System.out.println("汪汪汪！");
    }
    // breathe() 和 sleep() 可以直接使用默认实现

    // 也可以重写默认方法
    @Override
    public void sleep() {
        System.out.println("狗趴着睡...");
    }
}

// 默认方法的好处：
// 1. 向后兼容：给现有接口添加方法不用改所有实现类
// 2. 多继承：类可以实现多个接口，每个接口可以有默认方法
// 3. 代码复用：减少重复代码
```

> **小知识**：Java 8 的 `List` 接口添加了 `sort()` 默认方法、`Stream` 的 `forEachOrdered()` 等，这就是为什么Collections.sort 可以直接用 `list.sort()` 代替。

### 2.5.5 新的日期时间 API（`java.time`）：终于不用 `SimpleDateFormat` 了

Java 8 之前，处理日期时间是个噩梦：`Date` 类可变且坑多，`SimpleDateFormat` 线程不安全，月份从 0 开始……

```java
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.LocalTime;
import java.time.ZonedDateTime;
import java.time.Period;
import java.time.Duration;
import java.time.format.DateTimeFormatter;
import java.time.temporal.ChronoUnit;

public class DateTimeDemo {
    public static void main(String[] args) {
        // LocalDate：日期（年-月-日）
        LocalDate today = LocalDate.now();
        LocalDate birthday = LocalDate.of(1990, 1, 15);  // 直接用数字，不用减 1
        System.out.println("今天: " + today);
        System.out.println("生日: " + birthday);

        // LocalTime：时间（时:分:秒）
        LocalTime now = LocalTime.now();
        System.out.println("现在时间: " + now);

        // LocalDateTime：日期+时间
        LocalDateTime meeting = LocalDateTime.of(2026, 3, 30, 14, 30);
        System.out.println("会议时间: " + meeting);

        // ZonedDateTime：带时区的日期时间
        ZonedDateTime tokyoTime = ZonedDateTime.now(java.time.ZoneId.of("Asia/Tokyo"));
        System.out.println("东京时间: " + tokyoTime);

        // 日期计算（链式调用，爽！）
        LocalDate nextWeek = today.plusWeeks(1);
        LocalDate nextMonth = today.plusMonths(1);
        LocalDate lastYear = today.minusYears(1);
        System.out.println("下周: " + nextWeek);

        // Period：日期间隔
        Period age = Period.between(birthday, today);
        System.out.println("年龄: " + age.getYears() + " 岁");

        // Duration：时间间隔
        Duration twoHours = Duration.ofHours(2);
        LocalTime endTime = now.plus(twoHours);
        System.out.println("两小时后: " + endTime);

        // ChronoUnit：更方便的日期时间计算
        long daysBetween = ChronoUnit.DAYS.between(birthday, today);
        System.out.println("活了 " + daysBetween + " 天");

        // 格式化（线程安全！终于！）
        DateTimeFormatter fmt = DateTimeFormatter.ofPattern("yyyy年MM月dd日 HH:mm:ss");
        String formatted = meeting.format(fmt);
        System.out.println("格式化: " + formatted);

        // 解析
        LocalDate parsed = LocalDate.parse("2026-03-30");
        System.out.println("解析: " + parsed);
    }
}
```

`java.time` API 的设计非常出色：类是不可变的（线程安全）、API 清晰直观、时区和格式化都处理得很好。唯一的问题是——迁移老代码成本较高，很多人还是习惯性地用 `Date`。

### 2.5.6 方法引用（Method Reference）：`String::valueOf` 的优雅

方法引用是 Lambda 表达式的简写形式。当 Lambda 体只是调用某个方法时，可以用方法引用替代。

```java
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.function.Function;
import java.util.function.Consumer;
import java.util.function.Supplier;

public class MethodReferenceDemo {
    public static void main(String[] args) {
        // 方法引用一共四种形式（注意第 2、3 种很容易被混为一谈）：

        // 1. 静态方法引用：ClassName::staticMethod
        Function<Integer, String> f1 = String::valueOf;     // 等价于 n -> String.valueOf(n)
        System.out.println(f1.apply(42));  // "42"

        // 2. 未绑定实例方法引用：ClassName::instanceMethod
        //    接收者作为"第一个参数"传进来
        Function<String, Integer> f2 = String::length;      // 等价于 s -> s.length()
        System.out.println(f2.apply("World"));  // 5

        // 3. 绑定实例方法引用：instance::instanceMethod
        //    接收者已经固定，剩下的才是方法参数
        Consumer<String> c1 = System.out::println;          // 等价于 s -> System.out.println(s)
        c1.accept("Hello, Method Reference!");

        String str = "Hello";
        Supplier<Integer> s0 = str::length;                 // 等价于 () -> str.length()
        System.out.println(s0.get());  // 5

        // 4. 构造方法引用：ClassName::new
        Supplier<List<String>> s1 = ArrayList::new;         // 等价于 () -> new ArrayList<>()
        System.out.println(s1.get().size());  // 0

        // 实际应用：结合 Stream 使用
        List<String> names = Arrays.asList("alice", "bob", "charlie");

        // 全部转成大写
        names.stream()
              .map(String::toUpperCase)   // 等价于 s -> s.toUpperCase()
              .forEach(System.out::println);

        // 排序（使用 Comparable 的方法引用）
        names.stream()
              .sorted(String::compareToIgnoreCase)
              .forEach(System.out::println);
    }
}
```

方法引用让代码更简洁、更易读，尤其在 Stream 操作中非常实用。

### 2.5.7 CompletableFuture：异步编程的利器

Java 8 的 `CompletableFuture` 是在 `Future` 基础上封装的异步编程利器，支持流式调用、回调、组合等操作。

```java
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutionException;

public class CompletableFutureDemo {
    public static void main(String[] args) throws ExecutionException, InterruptedException {
        // 创建异步任务
        CompletableFuture<String> future = CompletableFuture.supplyAsync(() -> {
            // 模拟耗时操作
            try {
                Thread.sleep(2000);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            return "Hello, CompletableFuture!";
        });

        // 注册回调（不阻塞）
        future.thenAccept(result -> System.out.println("收到结果: " + result));

        // 链式调用：先查用户，再查订单，最后发邮件
        CompletableFuture<Void> chain = CompletableFuture
            .supplyAsync(() -> "user123")           // 异步获取用户ID
            .thenCompose(userId ->                   // 扁平化，接收一个新的 CompletableFuture
                CompletableFuture.supplyAsync(() -> getOrderByUserId(userId)))
            .thenCompose(order ->                    // 再查订单详情
                CompletableFuture.supplyAsync(() -> getOrderDetails(order)))
            .thenAccept(details ->                   // 最后发送邮件
                System.out.println("发送邮件: " + details));

        chain.join();  // 等待完成

        // 异常处理
        CompletableFuture<String> withError = CompletableFuture
            .supplyAsync(() -> {
                if (true) throw new RuntimeException("出错了！");
                return "result";
            })
            .exceptionally(ex -> {
                System.err.println("捕获异常: " + ex.getMessage());
                return "默认值";
            })
            .thenApply(result -> result + " - 处理后");

        System.out.println("异常处理结果: " + withError.get());

        // 组合多个 Future
        CompletableFuture<String> future1 = CompletableFuture.supplyAsync(() -> "A");
        CompletableFuture<String> future2 = CompletableFuture.supplyAsync(() -> "B");
        CompletableFuture<String> combined = CompletableFuture
            .allOf(future1, future2)  // 等待所有完成
            .thenApply(v -> future1.join() + future2.join());
        System.out.println("组合结果: " + combined.get());  // "AB"
    }

    static String getOrderByUserId(String userId) {
        return "Order-" + userId;
    }
    static String getOrderDetails(String orderId) {
        return "Details of " + orderId;
    }
}
```

CompletableFuture 让异步编程变得优雅、可读、可组合，是微服务架构中处理并发请求的核心工具。

### 2.5.8 Metaspace 取代 PermGen：再也不用调 PermGen 大小了

Java 8 之前，JVM 使用 **PermGen**（Permanent Generation）来存储类的元数据（类名、方法名、字段名等）。这带来了一个大问题：**`java.lang.OutOfMemoryError: PermGen space`**——只要你加载的类足够多（比如用大量框架、动态代理、字节码生成），PermGen 就会爆掉。

Java 8 用 **Metaspace** 取代了 PermGen：

- Metaspace 使用本地内存（Native Memory），而不是 JVM 堆内存
- Metaspace 默认可以动态扩展，只受限于物理内存和操作系统限制
- 不会再出现 PermGen space 的 OOM

```java
// JVM 参数对比
// Java 7 及之前：需要手动设置 PermGen 大小
// -XX:PermSize=256m -XX:MaxPermSize=512m

// Java 8+：Metaspace 自动管理，一般不需要设置
// 如果想限制 Metaspace 大小（可选）：
// -XX:MaxMetaspaceSize=256m
// -XX:MetaspaceSize=128m
```

这个改动对开发者来说是重大利好——少了一个需要调的参数，少了一类噩梦般的 OOM。

---

## 2.6 Java 9（2017，模块化项目 Project Jigsaw）：模块化时代

Java 9 发布了！等了好久的模块化系统终于来了。三年磨一剑，Java 9 带来的最大变化就是 **Jigsaw 模块化系统**（Jigsaw 是项目名，并不是版本的发布代号）。

### 2.6.1 模块化系统（Jigsaw）：Java 自己的模块化管理

模块化是 Java 9 最核心的特性。它的目标很宏大：**让 Java 应用可以模块化，告别「一整包 JAR」式的依赖管理**。

```java
// module-info.java
// 这是一个模块的声明文件，放在模块根目录下

module com.myapp {
    // 导出（exports）：这个模块向其他模块开放的包
    exports com.myapp.api;
    exports com.myapp.service;

    // 依赖（requires）：这个模块依赖的其他模块
    requires com.fasterxml.jackson.core;  // 需要 Jackson
    requires java.sql;                     // 需要 JDBC

    // 传递性导出（exports ... to）
    // 只有指定的模块才能访问这个包
    exports com.myapp.internal to com.myapp.impl;

    // 服务提供（provides ... with）：提供服务实现
    provides com.myapp.spi.Logger with com.myapp.impl.FileLogger;

    // 服务使用（uses）：依赖某个服务接口
    uses com.myapp.spi.Logger;
}
```

模块化的好处：

- **显式依赖**：每个模块声明自己需要什么，不用再靠猜测和文档
- **封装**：内部实现可以隐藏起来，只暴露必要的 API
- **可配置性**：可以选择性加载模块，构建更小、更安全的运行时（JLink 可以打包出裁剪过的 JRE）
- **安全**：限制模块间的访问，减少攻击面

```bash
# 使用 jlink 创建自定义运行时
jlink --add-modules java.base,java.sql,com.myapp --output my-runtime
# 生成了一个只包含必要模块的小型 JRE
```

### 2.6.2 JShell：交互式编程，像 Python 一样玩 Java（REPL）

Python 程序员可以输入一行代码立即看到结果，Java 程序员只能写完类、编译、运行……JShell 让 Java 也有了 REPL（Read-Eval-Print Loop）！

```bash
# 启动 JShell
$ jshell
|  欢迎使用 JShell — 您的代码片段在此处生效。
|  要获得相关信息，请键入 /help

jshell> int x = 10
x ==> 10

jshell> int y = 20
y ==> 20

jshell> x + y
$3 ==> 30

jshell> String greeting(String name) {
   ...>     return "Hello, " + name + "!";
   ...> }
|  已创建 方法 greeting(String)

jshell> greeting("Java")
$5 ==> "Hello, Java!"

jshell> /exit
|  再见
```

JShell 特别适合：快速测试 API、验证算法思路、调试代码片段、学习 Java 新特性。不用再为了「试试这个方法怎么用」而创建一个新项目。

### 2.6.3 接口私有方法：接口内部也可以写私有工具方法了

Java 9 允许接口包含 `private` 方法，这些方法可以作为内部工具方法，被 `default` 方法调用：

```java
public interface StringProcessor {
    default String process(String input) {
        // 调用私有工具方法
        String cleaned = cleanInput(input);
        String normalized = normalize(cleaned);
        return applyTransform(normalized);
    }

    // 私有方法：接口内部的实现细节
    private String cleanInput(String input) {
        if (input == null) {
            return "";
        }
        return input.trim().toLowerCase();
    }

    private String normalize(String input) {
        // 规范化处理逻辑
        return input.replaceAll("\\s+", " ");
    }

    private String applyTransform(String input) {
        // 子类可以覆盖 process 方法，但无法调用这些私有方法
        return "[" + input + "]";
    }
}

// 使用
class UpperCaseProcessor implements StringProcessor {
    // process 是默认方法，子类不实现也能直接用；
    // 接口里的 private 方法只在接口内部可见，子类既看不到也调不到
}

class InterfacePrivateDemo {
    public static void main(String[] args) {
        StringProcessor processor = new UpperCaseProcessor();
        System.out.println(processor.process("  Hello   WORLD  "));
        // 输出: [hello world]
    }
}
```

这个特性解决了接口中 `default` 方法代码重复的问题，让接口可以包含更复杂的默认实现逻辑。

### 2.6.4 集合工厂方法：`List.of()`、`Set.of()`、`Map.of()`，一行创建不可变集合

Java 9 为集合接口添加了静态工厂方法，可以一行代码创建不可变集合：

```java
import java.util.List;
import java.util.Set;
import java.util.Map;

public class CollectionFactoryDemo {
    public static void main(String[] args) {
        // 不可变 List
        List<String> immutableList = List.of("Apple", "Banana", "Cherry");
        // immutableList.add("Date");  // UnsupportedOperationException!

        // 不可变 Set
        Set<Integer> immutableSet = Set.of(1, 2, 3, 4, 5);

        // 不可变 Map
        Map<String, Integer> immutableMap = Map.of(
            "Alice", 25,
            "Bob", 30,
            "Charlie", 35
        );

        // Map 还有另一种方式：entries 方式
        Map<String, Integer> anotherMap = Map.ofEntries(
            Map.entry("David", 40),
            Map.entry("Eve", 45)
        );

        // 遍历
        System.out.println("List: " + immutableList);
        System.out.println("Set: " + immutableSet);
        System.out.println("Map: " + immutableMap);

        // Map.getOrDefault
        int unknownAge = immutableMap.getOrDefault("Frank", -1);  // -1，不存在的 key
        System.out.println("Frank's age: " + unknownAge);
    }
}
```

> **注意**：这些集合是不可变的，但内部元素如果是可变对象（比如 `List<StringBuilder>`），元素本身还是可以修改的。

### 2.6.5 Stream 新增方法：`takeWhile()`、`dropWhile()`、`iterate()` 重载

Java 9 为 Stream 添加了几个实用的新方法：

```java
import java.util.stream.Stream;
import java.util.stream.Collectors;
import java.util.List;

public class StreamEnhancementDemo {
    public static void main(String[] args) {
        List<Integer> numbers = List.of(1, 2, 3, 4, 5, 6, 7, 8, 9, 10);

        // takeWhile：从头开始取，满足条件就停止（遇到不满足的立即停止）
        List<Integer> taken = numbers.stream()
            .takeWhile(n -> n < 5)
            .collect(Collectors.toList());   // 注意：Stream.toList() 是 Java 16 才有的，
                                             // Java 9 时代要用 collect(Collectors.toList())
        System.out.println("takeWhile(< 5): " + taken);  // [1, 2, 3, 4]
        // 注意 takeWhile 是"遇到第一个不满足就立刻收工"：
        // List.of(3, 1, 4, 1, 5, 9, 2, 6) 用 takeWhile(n -> n < 5) 得到的是 [3, 1, 4, 1]，
        // 后面的 2 虽然也小于 5，但因为在 5 之后，已经被跳过了（这和 filter 完全不同）

        // dropWhile：从头开始丢弃，满足条件的都丢掉，遇到第一个不满足的就开始保留
        List<Integer> dropped = numbers.stream()
            .dropWhile(n -> n < 5)
            .collect(Collectors.toList());
        System.out.println("dropWhile(< 5): " + dropped);  // [5, 6, 7, 8, 9, 10]

        // iterate 重载：增加终止条件
        // Java 8 的 Stream.iterate(start, unaryOperator) 是无限的
        // Java 9 的 iterate(start, predicate, unaryOperator) 有终止条件
        List<Integer> fibonacci = Stream.iterate(
            new long[]{0, 1},                  // 起始值
            t -> t[0] < 1000,                  // 终止条件：作用于"当前元素"
            t -> new long[]{t[1], t[0] + t[1]} // 迭代函数
        ).map(t -> (int) t[0]).collect(Collectors.toList());
        System.out.println("Fibonacci < 1000: " + fibonacci);

        // ofNullable：处理可能为 null 的元素
        String nullable = null;
        List<String> result = Stream.ofNullable(nullable)
            .collect(Collectors.toList());
        System.out.println("ofNullable(null): " + result);  // []，空流
    }
}
```

### 2.6.6 HTTP Client 标准化：`java.net.http` 模块

Java 9 把新的 HTTP Client 作为**孵化模块**（`jdk.incubator.http`）引入，到 **Java 11 才正式标准化**为 `java.net.http` 包，支持 HTTP/2 和 WebSocket（因此下面这段代码请按 Java 11+ 来理解）：

```java
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

public class HttpClientDemo {
    public static void main(String[] args) throws Exception {
        // 创建 HTTP Client
        HttpClient client = HttpClient.newBuilder()
            .version(HttpClient.Version.HTTP_2)  // 默认 HTTP/2，自动降级
            .connectTimeout(java.time.Duration.ofSeconds(10))
            .build();

        // 发送 GET 请求
        HttpRequest request = HttpRequest.newBuilder()
            .uri(URI.create("https://api.github.com/users"))
            .header("Accept", "application/json")
            .GET()
            .build();

        HttpResponse<String> response = client.send(request,
            HttpResponse.BodyHandlers.ofString());

        System.out.println("状态码: " + response.statusCode());
        System.out.println("响应体: " + response.body().substring(0, 200) + "...");

        // 异步发送请求
        client.sendAsync(request, HttpResponse.BodyHandlers.ofString())
            .thenAccept(resp -> System.out.println("异步收到: " + resp.statusCode()))
            .join();

        // POST 请求
        HttpRequest postRequest = HttpRequest.newBuilder()
            .uri(URI.create("https://httpbin.org/post"))
            .header("Content-Type", "application/json")
            .POST(HttpRequest.BodyPublishers.ofString("{\"name\":\"Java\"}"))
            .build();

        HttpResponse<String> postResponse = client.send(postRequest,
            HttpResponse.BodyHandlers.ofString());
        System.out.println("POST 响应: " + postResponse.statusCode());
    }
}
```

之前，Java 只能用 `HttpURLConnection` 或者第三方库（Apache HttpClient、OkHttp）来发送 HTTP 请求。现在有了标准 API，简单多了。

---

## 2.7 Java 10~11（2018 年 3 月 ~ 2018 年 9 月）：快速迭代

Oracle 改变了 Java 的发布节奏——从每两年一个大版本，变成每六个月一个小版本。Java 10 和 Java 11 就是新节奏下的第一批产物。

### 2.7.1 `var` 局部变量类型推断：写 `var` 而不是 `String`，编译器帮你推断

Java 10 引入了局部变量类型推断（`var` 关键字），让你在声明局部变量时可以省略类型：

```java
// 之前的写法
String name = "Alice";
Map<String, List<Integer>> complex = new HashMap<String, List<Integer>>();
Iterator<Map.Entry<String, Object>> iterator = map.entrySet().iterator();

// var 写法：编译器自动推断类型
var name = "Alice";  // String
var complex = new HashMap<String, List<Integer>>();  // HashMap<String, List<Integer>>
var iterator = map.entrySet().iterator();  // Iterator<Map.Entry<String, Object>>

// var 不是关键字，是保留类型名
// 所以 var 可以作为变量名，但建议不要
int var = 42;  // 合法，但不推荐
```

> **注意**：`var` 只能用于**局部变量**（方法内、代码块内），不能用于字段、方法参数、返回值。`var` 不是动态类型，是编译时类型推断。

### 2.7.2 字符串增强：`isBlank()`、`lines()`、`strip()`、`repeat()`

Java 11 给 `String` 类添加了一堆实用方法：

```java
public class StringEnhancementDemo {
    public static void main(String[] args) {
        String str = "  Hello\nWorld  ";

        // isBlank()：判断是否为空或只包含空白字符
        System.out.println("  ".isBlank());  // true（Java 11+）

        // strip()：去除首尾空白（Unicode 感知，比 trim() 更智能）
        System.out.println("  hello  ".strip());  // "hello"（trim 只处理 ASCII）
        System.out.println("\u2002hello\u2002".strip());  // "hello"（trim 不处理这个）

        // lines()：按行分割，返回 Stream
        String multiline = "line1\nline2\nline3";
        long lineCount = multiline.lines().count();
        System.out.println("行数: " + lineCount);

        // repeat()：重复字符串
        System.out.println("Ha".repeat(5));  // "HaHaHaHaHa"

        // ⚠️ 版本提醒：下面这两个方法不属于 Java 11。
        // stripIndent()、translateEscapes() 和文本块 """...""" 都是 Java 13 预览、
        // Java 15 才正式转正的特性，在 Java 11 上写完会直接编译失败。

        // （Java 15+）文本块 + stripIndent()：移除每行公共的前导缩进
        String indented = """
            Hello
                World
            """;
        System.out.println(indented.stripIndent());

        // （Java 15+）translateEscapes()：把字面量里的转义序列真正转换出来
        String escaped = "Hello\\nWorld".translateEscapes();
        System.out.println(escaped);  // Hello(换行)World
    }
}
```

### 2.7.3 文件操作增强：`readString()`、`writeString()` 一行搞定

Java 11 给 `Files` 类添加了直接读写 String 的方法：

```java
import java.nio.file.Files;
import java.nio.file.Path;

public class FilesStringDemo {
    public static void main(String[] args) throws Exception {
        Path tempFile = Files.createTempFile("test", ".txt");

        // 一行代码写文件
        Files.writeString(tempFile, "Hello, Java 11!");

        // 一行代码读文件
        String content = Files.readString(tempFile);
        System.out.println("文件内容: " + content);

        // 追加内容
        Files.writeString(tempFile, "\n新一行", java.nio.file.StandardOpenOption.APPEND);

        // 读取所有行
        var lines = Files.readAllLines(tempFile);
        System.out.println("行数: " + lines.size());

        // 清理
        Files.deleteIfExists(tempFile);
    }
}
```

之前要读写文本文件需要用 BufferedReader/BufferedWriter，现在一行搞定。

### 2.7.4 集合 `toArray(IntFunction)`：更方便的集合转数组

Java 11 为集合添加了 `toArray(IntFunction)` 方法：

```java
import java.util.List;
import java.util.ArrayList;

public class CollectionToArrayDemo {
    public static void main(String[] args) {
        List<String> names = new ArrayList<>();
        names.add("Alice");
        names.add("Bob");
        names.add("Charlie");

        // Java 11 之前：只能传一个现成的数组（数组太小会被自动替换成新数组）
        String[] arr1 = names.toArray(new String[0]);

        // Java 11 新增：可以传一个 IntFunction，由集合自己决定数组大小
        String[] arr2 = names.toArray(length -> new String[length]);
        // 最常见的写法就是构造方法引用，效果和上面完全一样
        String[] arr3 = names.toArray(String[]::new);

        System.out.println("数组长度: " + arr3.length);
        for (String name : arr3) {
            System.out.println(name);
        }
    }
}
```

### 2.7.5 局部变量 Lambda 语法：`var` 可以用在 Lambda 参数上了

Java 11 允许在 Lambda 参数上使用 `var`：

```java
import java.util.function.Function;

public class LambdaVarDemo {
    public static void main(String[] args) {
        // 之前的 Lambda 参数
        Function<String, String> f1 = (String s) -> s.toUpperCase();
        Function<String, String> f2 = s -> s.toUpperCase();

        // Java 11+：可以用 var（给参数加注解时必须用 var）
        Function<String, String> f3 = (@Nonnull var s) -> s.toUpperCase();

        // 有什么用？可以在参数上加注解！
        System.out.println(f3.apply("hello"));
    }

    // 自定义注解
    @interface Nonnull {}
}
```

这个特性主要是为了**给 Lambda 参数加注解**。比如你想标记某个参数为 `@Nullable` 或 `@Nonnull`，就必须用 `var`。

### 2.7.6 ZGC：低延迟垃圾收集器（实验特性）

Java 11 引入了 **ZGC**（Z Garbage Collector）作为实验特性。ZGC 的目标是：**停顿时间不超过 10ms，且停顿时间不随堆大小增加而增加**。

```bash
# 启用 ZGC（Java 11 实验，Java 15+ 正式支持）
java -XX:+UseZGC -Xmx8g MyApp

# Java 21+ 推荐配置
java -XX:+UseZGC -Xmx64g MyApp
```

ZGC 非常适合大内存（64GB+）低延迟的应用，比如金融交易、游戏服务器、实时数据处理等。

### 2.7.7 Java 11 是 LTS 版本，很多公司开始从 8 迁移到 11

Java 11 是继 Java 8 之后的第一个 **LTS（Long-Term Support）** 版本。Oracle 的新策略是：

- **LTS 版本**：每两年发布一次，持续支持时间远长于普通版本（以 Java 21 为例，Oracle JDK 的高级支持到 2028 年 9 月，延长支持到 2031 年 9 月；不同厂商的支持周期略有差异）
- **非 LTS 版本**：每六个月一个，支持六个月

很多企业发现 Java 8 的安全漏洞越来越多，而 Java 11 不但性能更好，还有长期支持，于是开始了大规模的版本迁移。Java 11 成了「新一代 Java 8」。

---

## 2.8 Java 12~16（2019~2021）：特性爆发

从 Java 12（2019 年 3 月）到 Java 16（2021 年 3 月）这两年，是 Java 新特性最密集的爆发期。Oracle 采用「预览特性」机制——新功能先以预览版发布，收集反馈后再决定是否保留。这种方式让 Java 既能快速迭代，又能保持稳定性。

### 2.8.1 Switch 表达式预览（Java 12）→ 正式版（Java 14）

Java 12 引入了新的 Switch 表达式，Java 14 正式发布。

```java
// 传统 switch 语句（Java 14 前）
String dayType;
switch (day) {
    case "MONDAY":
    case "TUESDAY":
    case "WEDNESDAY":
    case "THURSDAY":
    case "FRIDAY":
        dayType = "工作日";
        break;
    case "SATURDAY":
    case "SUNDAY":
        dayType = "周末";
        break;
    default:
        dayType = "未知";
}

// Java 14+ 的 switch 表达式（箭头语法）
String dayType = switch (day) {
    case "MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY" -> "工作日";
    case "SATURDAY", "SUNDAY" -> "周末";
    default -> "未知";
};

// switch 表达式可以有返回值
int days = switch (month) {
    case "JAN", "MAR", "MAY", "JUL", "AUG", "OCT", "DEC" -> 31;
    case "APR", "JUN", "SEP", "NOV" -> 30;
    case "FEB" -> 28;  // 忽略闰年简化示例
    default -> 0;
};
```

新 switch 的优势：**箭头语法不会再漏写 `break`、一个 `case` 可以用逗号分隔多个值、`switch` 可以直接作为表达式返回值**。

### 2.8.2 文本块（Text Blocks）预览（Java 13）→ 正式版（Java 15）

文本块让你可以写多行字符串，而不用拼接和转义：

```java
// 传统方式：字符串拼接和转义
String json = "{\n" +
              "    \"name\": \"Alice\",\n" +
              "    \"age\": 25\n" +
              "}";

// Java 15+ 文本块
String json = """
        {
            "name": "Alice",
            "age": 25
        }
        """;

// HTML 示例
String html = """
        <html>
            <body>
                <h1>Hello, Text Blocks!</h1>
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

文本块会自动处理缩进，`"""` 后面的内容会作为字符串的起始位置，不需要手动去对齐。

### 2.8.3 record 记录类预览（Java 14）→ 正式版（Java 16）

`record` 是 Java 16 正式发布的「数据传输对象（DTO）」的简洁写法：

```java
import java.util.Objects;

public class RecordDemo {
    // 传统方式：定义一个 Point 类，代码量惊人
    public static class PointClass {
        private final double x;
        private final double y;

        public PointClass(double x, double y) {
            this.x = x;
            this.y = y;
        }

        public double x() { return x; }
        public double y() { return y; }

        @Override
        public boolean equals(Object o) {
            if (!(o instanceof PointClass)) return false;
            PointClass p = (PointClass) o;
            return Double.compare(p.x, x) == 0 && Double.compare(p.y, y) == 0;
        }

        @Override
        public int hashCode() {
            return Objects.hash(x, y);
        }

        @Override
        public String toString() {
            return "Point[x=" + x + ", y=" + y + "]";
        }
    }

    // record 方式：一行代码搞定！
    // 它自动生成：构造函数、取值方法 x()/y()、equals、hashCode、toString
    // record 是不可变的（所有字段都是 final）
    public record Point(double x, double y) {}

    public static void main(String[] args) {
        Point p = new Point(3.0, 4.0);
        System.out.println(p.x());   // 3.0
        System.out.println(p.y());   // 4.0
        System.out.println(p);       // Point[x=3.0, y=4.0]
    }
}
```

`record` 特别适合：**数据传输对象（DTO）、元组返回值、配置对象、日志记录**等场景。

> **注意**：record 的构造函数可以做参数验证：

```java
public record Person(String name, int age) {
    // compact（紧凑）构造函数：不用重复写参数列表和赋值语句
    public Person {
        if (age < 0) {
            throw new IllegalArgumentException("年龄不能为负数");
        }
        // 给参数重新赋值，就会改变最终写入字段的值，例如：
        // name = name.trim();
        // 这算是"规范化"参数，不是直接改字段（record 的字段始终是 final）
    }
}
```

### 2.8.4 Pattern Matching for instanceof 预览（Java 14）→ 正式版（Java 16）

以前 instanceof 后需要强制类型转换：

```java
// Java 14 前
if (obj instanceof String) {
    String s = (String) obj;  // 啰嗦，还要强制转换
    System.out.println(s.length());
}

// Java 16+ Pattern Matching for instanceof
if (obj instanceof String s) {  // 一步到位
    System.out.println(s.length());  // s 直接可用，不用强制转换
}

// 可以组合条件
if (obj instanceof String s && s.length() > 5) {
    System.out.println("长字符串: " + s);
}
```

这个特性让 `instanceof` 检查和类型转换一步完成，代码更简洁。

### 2.8.5 密封类（Sealed Classes）预览（Java 15）→ 正式版（Java 17）

密封类限制哪些类可以继承它，实现更精细的继承控制：

```java
// 密封类：只有 permit 的类才能继承
public sealed class Shape
    permits Circle, Rectangle, Triangle {
}

// Circle 可以继续被继承
public final class Circle extends Shape {  // final：不能再被继承
    private double radius;
    public Circle(double radius) { this.radius = radius; }
}

// Rectangle 也可以是 sealed，但 sealed 类必须写明 permits 列表
public sealed class Rectangle extends Shape permits Square {
    private double width, height;
    public Rectangle(double w, double h) { this.width = w; this.height = h; }
}

// Square 继承 Rectangle，并标记为 final
public final class Square extends Rectangle {
    public Square(double side) { super(side, side); }
}

// Triangle 是 non-sealed，可以被任何类继承
public non-sealed class Triangle extends Shape {
    private double a, b, c;
    public Triangle(double a, double b, double c) { this.a = a; this.b = b; this.c = c; }
}
```

密封类的 `permits` 列表让编译器知道「只有这些类可以继承我」，这对于**模式匹配**特别重要——编译器可以检查所有可能的子类，确保 `switch` 表达式处理了每一种情况。

### 2.8.6 jpackage 打包工具（Java 14）：打包成原生安装程序

Java 14 引入的 `jpackage` 可以把 Java 应用打包成原生安装程序：

```bash
# 打包成 Windows MSI 安装程序
jpackage --name MyApp \
  --input target/ \
  --main-jar myapp.jar \
  --type msi \
  --win-console

# 打包成 macOS DMG
jpackage --name MyApp \
  --input target/ \
  --main-jar myapp.jar \
  --type dmg

# 打包成 Linux deb/rpm
jpackage --name MyApp \
  --input target/ \
  --main-jar myapp.jar \
  --type deb
```

`jpackage` 让 Java 应用的分发变得简单——不用再让用户手动安装 JRE，直接分发一个安装包就行。

### 2.8.7 移除 Nashorn JavaScript 引擎

Java 11 废弃了 Nashorn，Java 15 正式移除。Nashorn 是 Java 8 引入的 JavaScript 引擎，让 Java 可以执行 JavaScript 代码。随着 WebAssembly 的发展和 GraalJS 的成熟，Nashorn 显得有些鸡肋，Oracle 决定让它退出历史舞台。

---

## 2.9 Java 17（LTS，2021）：成熟稳重

Java 17 是继 Java 11 之后的下一个 LTS 版本。它带来了更多预览特性正式化、同时移除了一些历史遗留。

### 2.9.1 密封类正式发布

Java 17 正式发布了密封类（Sealed Classes），这是 Java 15/16 预览后的正式版本。现在你可以放心地在生产环境中使用密封类了。

```java
// 密封类在 Java 17 正式可用
public class SealedExprDemo {

    // 密封接口：只允许下面三种实现
    public sealed interface Expr permits ConstantExpr, AddExpr, MulExpr {}

    // 常量表达式
    public record ConstantExpr(int value) implements Expr {}

    // 加法表达式
    public record AddExpr(Expr left, Expr right) implements Expr {}

    // 乘法表达式
    public record MulExpr(Expr left, Expr right) implements Expr {}

    // 编译器知道 Expr 只有三种实现，switch 可以穷尽检查
    static int eval(Expr e) {
        return switch (e) {
            case ConstantExpr c -> c.value();
            case AddExpr a -> eval(a.left()) + eval(a.right());
            case MulExpr m -> eval(m.left()) * eval(m.right());
            // 不需要 default！编译器确保所有情况都覆盖了
        };
    }

    public static void main(String[] args) {
        // 计算 (1 + 2) * 3 = 9
        Expr expr = new MulExpr(
                new AddExpr(new ConstantExpr(1), new ConstantExpr(2)),
                new ConstantExpr(3));
        System.out.println("结果: " + eval(expr)); // 结果: 9
    }
}
```

### 2.9.2 废弃 Security Manager、Applet API（注意：是"废弃"，不是"移除"）

这里必须纠正一个流传极广的说法：**Java 17 并没有"移除"Security Manager 和 Applet API，只是把它们标记为"废弃并计划移除"**。

- **Applet API**：JDK 9（2017，JEP 289）标记废弃，JDK 17（2021，JEP 398）标记为"废弃并计划移除"。到今天（JDK 25）`java.applet` 包**依然存在**，只是编译时会给出"已过时、待删除"的警告。
- **Security Manager**：JDK 17（2021，JEP 411）标记废弃并计划移除；**JDK 24（2025，JEP 486）把它永久禁用**——`System.setSecurityManager()` 直接抛 `UnsupportedOperationException`，`System.getSecurityManager()` 永远返回 `null`。

所以准确的时间线是"JDK 17 废弃 → 后续版本逐步禁用/删除"，写代码时千万别照着"Java 17 已经没有它们了"去理解。

### 2.9.3 新的 macOS 渲染引擎

Java 17 引入了新的 macOS 渲染引擎，用 Apple 的 Metal 框架取代了老的 OpenGL 渲染。这意味着 Java 应用在 macOS 上的图形性能更好。

### 2.9.4 随机数生成器增强

Java 17 增强了随机数生成器 API，引入了 `RandomGenerator` 接口和新的实现：

```java
// ⚠️ 包名要记准：随机数生成器在 java.util.random 下，不是 java.random
import java.util.random.RandomGenerator;
import java.util.random.RandomGeneratorFactory;
import java.util.random.JumpableGenerator;

public class RandomDemo {
    public static void main(String[] args) {
        // 获取所有可用的随机数生成器
        System.out.println("可用算法:");
        RandomGeneratorFactory.all()
            .forEach(factory -> System.out.println("  " + factory.group() + "/" + factory.name()));

        // 使用新的 Xoroshiro128PlusPlus 生成器
        RandomGenerator rng = RandomGeneratorFactory.of("Xoroshiro128PlusPlus").create();
        System.out.println("随机数: " + rng.nextInt(100));

        // JumpableGenerator：可以"跳跃"到序列中很远的位置
        // 注意：RandomGeneratorFactory.create() 返回的是 RandomGenerator，
        // 想调用 jump() 必须显式转成 JumpableGenerator
        JumpableGenerator jumpable =
            (JumpableGenerator) RandomGeneratorFactory.of("L32X64MixMix").create();
        jumpable.jump();  // 跳到下一个「时代」
        System.out.println("跳跃后随机数: " + jumpable.nextInt(100));
    }
}
```

### 2.9.5 Java 17 是 Java 11 之后的又一个 LTS 版本——企业迁移的目标版本

Java 17 是 Oracle 在 2021 年 9 月发布的 LTS 版本（继 Java 8、Java 11 之后的第三个 LTS）。以 Oracle JDK 为例，高级支持到 2026 年 9 月，延长支持到 2029 年 9 月；其他厂商的支持周期会更长一些。很多企业开始从 Java 8/11 迁移到 Java 17，享受新特性带来的好处：

- **性能提升**：G1 GC 改进、ZGC 逐步成熟、JIT 编译器优化（注意：写"AOT 编译"是不对的——实验性的 `jaotc` AOT 编译器恰恰是在 Java 17 被移除了，见 JEP 410）
- **新特性**：密封类、模式匹配、文本块、record、Stream API 增强
- **安全性**：移除不安全的旧 API、更强的加密算法
- **现代语法**：switch 表达式、文本块、record，让代码更简洁

---

## 2.10 Java 21 LTS（2023）：虚拟线程革命——21 世纪最重要的 Java 版本

「Java 21 之于 Java，就如同智能手机之于功能机。」——这是 Java 社区对 Java 21 的评价。

Java 21 是又一个 LTS 版本，也是自 Java 8 以来最重要的版本。虚拟线程（Virtual Threads）的正式发布，标志着 Java 并发编程范式的根本性转变。

### 2.10.1 虚拟线程（Virtual Threads）正式发布

虚拟线程是 Java 21 最大的亮点，它彻底改变了 Java 的线程模型。

**背景知识**：在虚拟线程出现之前，Java 的线程（称为「平台线程」）直接映射到操作系统的线程。一个线程占用 1MB 左右的栈内存，如果你需要同时处理 10000 个请求，就需要 10000 个线程——光线程栈就要消耗 10GB 内存！这导致 Java 服务器必须使用异步编程、线程池等技术来「假装」并发。

**虚拟线程**：也叫「轻量级线程」，由 JVM 管理，不直接绑定 OS 线程。多个虚拟线程可以共享一个 OS 线程（载体线程），大幅降低内存占用。

```java
import java.time.Duration;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;
import java.util.concurrent.ThreadFactory;

public class VirtualThreadDemo {
    public static void main(String[] args) throws Exception {
        // 创建虚拟线程（方式一：Thread.ofVirtual()）
        Thread virtualThread = Thread.ofVirtual().start(() -> {
            System.out.println("我是虚拟线程！");
            System.out.println("载体线程: " + Thread.currentThread());
        });

        // 方式二：用 ThreadFactory
        ThreadFactory factory = Thread.ofVirtual().factory();
        Thread t2 = factory.newThread(() -> {
            System.out.println("另一个虚拟线程");
        });
        t2.start();

        // 方式三：ExecutorService 自动管理
        try (ExecutorService executor = Executors.newVirtualThreadPerTaskExecutor()) {
            List<Future<?>> futures = new ArrayList<>();
            for (int i = 0; i < 100; i++) {
                final int taskId = i;
                futures.add(executor.submit(() -> {
                    // 模拟 I/O 操作（sleep 不占 CPU，非常适合虚拟线程）
                    Thread.sleep(Duration.ofSeconds(1));
                    return "任务 " + taskId + " 完成";
                }));
            }

            for (Future<?> f : futures) {
                System.out.println(f.get());
            }
        }

        // 虚拟线程 vs 平台线程的内存对比
        // 平台线程：每个约 1MB 栈
        // 虚拟线程：每个约 200B~1KB 栈（按需扩展）
        // 10 万并发：平台线程需要 ~100GB 内存，虚拟线程只需要 ~1GB

        System.out.println("主线程结束");
    }
}
```

```java
// 一个小而完整的 HTTP 服务：每个请求交给一个虚拟线程处理
import com.sun.net.httpserver.HttpServer;
import java.net.InetSocketAddress;
import java.nio.charset.StandardCharsets;
import java.util.concurrent.Executors;

public class VirtualThreadHttpServer {
    public static void main(String[] args) throws Exception {
        // 端口 8080，第二个参数 0 表示使用系统默认的 backlog
        HttpServer server = HttpServer.create(new InetSocketAddress(8080), 0);

        // 关键的一行：把执行器换成"每个任务一个虚拟线程"
        server.setExecutor(Executors.newVirtualThreadPerTaskExecutor());

        server.createContext("/", exchange -> {
            byte[] body = "Hello from a virtual thread!\n".getBytes(StandardCharsets.UTF_8);
            exchange.sendResponseHeaders(200, body.length);
            try (var out = exchange.getResponseBody()) {
                out.write(body);
            }
        });

        server.start();
        System.out.println("服务器已启动：http://localhost:8080/");
        System.out.println("每个请求都会由一个独立的虚拟线程处理");
    }
}
```

> **重要提示**：虚拟线程适合 I/O 密集型任务（网络请求、文件操作、数据库查询），不适合 CPU 密集型任务（计算密集）。对于 CPU 密集型，还是需要平台线程和并行流。

### 2.10.2 Pattern Matching for switch 正式版

Java 21 正式发布了 Pattern Matching for switch，让 `switch` 语句可以匹配模式：

```java
public class PatternSwitchDemo {

    // 1. 用模式替代"先 instanceof 再强转"
    static String describe(Object obj) {
        return switch (obj) {
            // when 是"守卫条件"，让同一个类型可以走不同分支
            case String s when s.length() > 5 -> "长字符串: " + s;
            case String s -> "短字符串: " + s;
            case Integer i -> "数字: " + i;
            // 同时匹配 null 和"其他所有情况"
            case null, default -> "其他";
        };
    }

    // 2. record + switch 模式匹配：密封接口保证 switch 可以穷尽
    sealed interface Shape permits Circle, Rectangle, Triangle {}
    record Circle(double radius) implements Shape {}
    record Rectangle(double width, double height) implements Shape {}
    record Triangle(double a, double b, double c) implements Shape {}

    static double area(Shape s) {
        return switch (s) {
            case Circle c -> Math.PI * c.radius() * c.radius();
            case Rectangle r -> r.width() * r.height();
            case Triangle t -> {
                // 海伦公式
                double s2 = (t.a() + t.b() + t.c()) / 2;
                yield Math.sqrt(s2 * (s2 - t.a()) * (s2 - t.b()) * (s2 - t.c()));
            }
        };
    }

    public static void main(String[] args) {
        System.out.println(describe("hello"));
        System.out.println(describe(42));
        System.out.println(area(new Rectangle(3, 4)));  // 12.0
        System.out.println(area(new Circle(1)));        // 3.141592653589793
    }
}
```

### 2.10.3 Record Patterns：record 可以用在 pattern matching 里

```java
public class RecordPatternDemo {

    record Point(int x, int y) {}
    record Line(Point start, Point end) {}

    // 1. instanceof + 记录模式：一步完成类型检查和字段解构
    static void printSum(Object obj) {
        if (obj instanceof Point(int x, int y)) {
            // 直接拿到 x 和 y，不用再强转和调 getter
            System.out.println("Sum = " + (x + y));
        }
    }

    // 2. 结合 switch 使用，还能嵌套解构
    static String describe(Object obj) {
        return switch (obj) {
            case Point(int x, int y) when x == y -> "对角线上的点";
            case Point(int x, int y) -> "普通点 (" + x + ", " + y + ")";
            // 嵌套记录模式：直接解构出线段的两个端点坐标
            case Line(Point(int x1, int y1), Point(int x2, int y2))
                    -> "线段 (" + x1 + "," + y1 + ") → (" + x2 + "," + y2 + ")";
            case null -> "空";
            default -> "其他形状";
        };
    }

    public static void main(String[] args) {
        printSum(new Point(3, 4));                                  // Sum = 7
        System.out.println(describe(new Point(5, 5)));              // 对角线上的点
        System.out.println(describe(new Line(new Point(0, 0), new Point(1, 2))));
    }
}
```

### 2.10.4 Scoped Values 与结构化并发：比 ThreadLocal 更安全的数据传递（预览特性）

> ⚠️ **先把版本说清楚**：`ScopedValue` 与结构化并发（`StructuredTaskScope`）**都是预览特性，至今没有转正**。它们在 Java 21 首次预览，之后每个版本都在修订。使用它们必须加 `--enable-preview` 参数，而且**编译和运行必须用同一个 JDK 版本**（预览特性是按版本绑定的）。写业务代码时请谨慎采用。

`ThreadLocal` 的问题：线程池环境下，`ThreadLocal` 的值可能被错误复用；值传递也不够安全。

`ScopedValue` 的优势：值与代码块的作用域绑定，出了作用域就自动失效，不需要手动 `remove()`；配合结构化并发还能安全地传给子任务。

```java
// ⚠️ 下面这段代码需要 --enable-preview 才能编译运行
// 注意：ScopedValue 位于 java.lang 包，不需要 import！
import java.util.concurrent.StructuredTaskScope;

// ScopedValue：线程安全的数据容器
public class ScopedValueDemo {
    // 定义一个 ScopedValue：注意创建方式是 newInstance()，不是 empty()
    static final ScopedValue<String> CURRENT_USER = ScopedValue.newInstance();

    public static void main(String[] args) {
        // 作用域外取值：用 orElse 提供兜底值
        String result = CURRENT_USER.orElse("Anonymous");
        System.out.println("作用域外的用户: " + result);

        // 绑定值并运行：API 是 ScopedValue.where(...).run(...)
        ScopedValue.where(CURRENT_USER, "Alice").run(() -> {
            System.out.println("作用域内的用户: " + CURRENT_USER.get());
            callService();  // 被调用的子方法也能读到这个值
        });

        // ScopedValue 在结构化并发中特别有用。
        // ⚠️ 结构化并发仍是预览 API，各版本写法不同：
        //    Java 21~24：new StructuredTaskScope.ShutdownOnFailure()
        //    Java 25+  ：StructuredTaskScope.open(...)（API 被重新设计过）
        try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
            Future<Integer> f1 = scope.fork(() -> {
                return doTask1(CURRENT_USER.get());  // 自动继承 ScopedValue
            });
            Future<Integer> f2 = scope.fork(() -> {
                return doTask2(CURRENT_USER.get());
            });

            scope.join();
            System.out.println("结果: " + (f1.resultNow() + f2.resultNow()));
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    static void callService() {
        // 子方法可以直接访问 ScopedValue
        System.out.println("服务调用者: " + CURRENT_USER.get());
    }

    static Integer doTask1(String user) { return 1; }
    static Integer doTask2(String user) { return 2; }
}
```

### 2.10.5 String Templates（字符串模板）：预览后被撤回，**至今没有正式版**

> ⚠️ **这一条必须纠正**：网络上大量文章说"String Templates 会在 Java 26 转正"，这是**不准确的**。真实情况是：
> String Templates 在 **Java 21 首次预览**（JEP 430）、**Java 22 第二次预览**（JEP 459），随后被**撤回**——从 Java 23 起，`STR."..."` 这套语法**已经不在 JDK 里了**，也没有进入任何后续正式版本。JDK 25 中同样没有它。
>
> 也就是说，下面这段代码**在今天的任何 JDK（包括最新的正式版）里都编译不过**。保留它只是为了说明"曾经有过这样一个设计"，写代码时请改用 `String.format()`、`StringBuilder` 或文本块。

```java
// ⚠️ 已被撤回的预览语法（仅 Java 21/22 的预览版能用，且需要 --enable-preview）
// 在 Java 23 及以后的版本中，这段代码无法编译

// 简单的模板
String name = "Alice";
String greeting = STR."Hello, \{name}!";  // "Hello, Alice!"

// 表达式
int x = 10, y = 20;
String math = STR."\{x} + \{y} = \{x + y}";  // "10 + 20 = 30"

// 复杂表达式
String multi = STR."""
    第一行: \{x}
    第二行: \{y}
    计算结果: \{x * y}
    """;

// TemplateProcessor 自定义模板处理器
// FMT 处理器：格式化数字
String formatted = FMT."""
    整数: %d\{x}
    浮点: %.2f\{(double)x / y}
    十六进制: %x\{x}
    """;
```

### 2.10.6 Foreign Function & Memory API（Java 22 正式版）

> ⚠️ 版本纠正：FFM API 在 Java 21 是**预览**，在 **Java 22 就正式转正**了（JEP 454），并不是"Java 26 正式发布"。它让 Java 可以直接调用 native 代码、安全地操作堆外内存，目标是逐步取代 JNI。

```java
// FFM API（Java 22 起为正式特性）
// 使用 MemorySegment 和 Arena

// 分配堆外内存
// 注意要用 Arena.ofConfined() 这类"可关闭"的 Arena；
// Arena.global() 是全局共享的，关闭它会抛出异常
try (Arena arena = Arena.ofConfined()) {
    MemorySegment segment = arena.allocate(1024);
    // 操作内存
    segment.set(ValueLayout.JAVA_INT, 0, 42);
    int value = segment.get(ValueLayout.JAVA_INT, 0);
    System.out.println("读取值: " + value);
}
```

这个 API 的目标是取代 JNI（Java Native Interface），让 Java 与 C/C++ 库交互更安全、更高效。

### 2.10.7 Sequenced Collection：集合有了统一的顺序访问接口

Java 21 引入了「序列集合」概念，统一了 List、Deque、Set 的顺序访问接口：

```java
import java.util.ArrayList;
import java.util.List;

public class SequencedCollectionDemo {
    public static void main(String[] args) {
        // List 从 Java 21 起实现了 SequencedCollection，
        // 于是有了统一的首尾访问方法（Deque、LinkedHashSet、SortedSet 同理）
        List<Integer> list = new ArrayList<>(List.of(1, 2, 3));
        list.addFirst(0);              // [0, 1, 2, 3]
        list.addLast(4);               // [0, 1, 2, 3, 4]
        int first = list.getFirst();   // 0
        int last = list.getLast();     // 4
        System.out.println("first=" + first + ", last=" + last);

        // reversed() 返回的是"反向视图"，不是副本：
        // 改原列表会同步反映到 reversed 上
        List<Integer> reversed = list.reversed();
        System.out.println(reversed);  // [4, 3, 2, 1, 0]
        list.addFirst(-1);
        System.out.println(reversed);  // [-1, 4, 3, 2, 1, 0]  ← 视图跟着变了
    }
}
```

> 📌 **补充**：`SequencedCollection` 是 JDK 自带的接口（`java.util.SequencedCollection`），它定义的方法包括 `reversed()`、`addFirst/addLast`、`getFirst/getLast`、`removeFirst/removeLast`。`Map` 对应的接口是 `SequencedMap`，提供 `putFirst/putLast`、`sequencedKeySet()`、`reversed()` 等——注意 `Map` 本身**没有** `getFirst/getLast`。

### 2.10.8 ZGC 和 Shenandoah GC（注意：它们不是 Java 21 才转正的）

> ⚠️ 版本纠正：**ZGC 和 Shenandoah 都是在 Java 15 就转正了**（JEP 377、JEP 379），并不是 Java 21 才"正式发布"。它们真正与 Java 21 相关的变化是：ZGC 在 Java 21 引入了**分代模式**（JEP 439，`-XX:+UseZGC -XX:+ZGenerational`，后来成为默认行为）。

- **ZGC**：低延迟 GC，适合大内存（64GB+）应用
- **Shenandoah**：低延迟 GC，适合中等内存应用，Red Hat 主导

```bash
# 启用 ZGC
java -XX:+UseZGC -Xmx64g MyApp

# 启用 Shenandoah
java -XX:+UseShenandoahGC -Xmx16g MyApp
```

---

## 2.11 Java 22~26（2024~2026）：持续进化

Java 的发布节奏已经稳定在每六个月一个大版本。下面这一节按版本梳理近年变化，涉及版本状态的判断都以可实测的 JDK 为准（本地 JDK 25 实测：`ScopedValue` 可用、`StructuredTaskScope` 仍是预览 API、JDK 中没有 `java.lang.StringTemplate`）。

### 2.11.1 Java 22（2024.3）：FFM API 与 Unnamed Variables 转正

Java 22 转正的特性：

- **Foreign Function & Memory API（JEP 454）**：正式成为标准 API，取代了 JNI 的绝大部分日常用途，让 Java 调用本地库、访问堆外内存有了安全且高效的正规途径。
- **Unnamed Variables & Patterns（JEP 456）**：用 `_` 表示「这个变量我不需要」。

同时继续处于预览或孵化状态的还有：String Templates（第二次预览，JEP 459）、Statements before super()（JEP 447）、Implicitly Declared Classes（JEP 463）、Class-File API、Stream Gatherers、Structured Concurrency、Scoped Values。

> ⚠️ 常见误传：网上流传的 "Statement Expressions"（可以在任意表达式位置写 `{ ... }` 代码块，例如 `System.out.println({ int m = ...; m; })`）**不是 Java 22 的特性，也不存在于任何 JDK 中**，这段代码无法通过编译。

**FFM API 示例**（Java 22 起标准 API，无需预览参数）：

```java
import java.lang.foreign.Arena;
import java.lang.foreign.MemorySegment;
import java.lang.foreign.ValueLayout;

public class FfmDemo {
    public static void main(String[] args) {
        try (Arena arena = Arena.ofConfined()) {
            MemorySegment segment = arena.allocate(8);
            segment.set(ValueLayout.JAVA_INT, 0, 42);
            int value = segment.get(ValueLayout.JAVA_INT, 0);
            System.out.println("读取值: " + value); // 读取值: 42
        }
    }
}
```

**Unnamed Variables 示例**（JDK 25 实测通过）：

```java
public class UnnamedVariablesDemo {
    record Point(int x, int y) {}

    public static void main(String[] args) {
        String[] parts = "a-b-c".split("-");
        String _ = parts[1];          // 明确表示「这个值拿到但不用」
        System.out.println(parts[0] + parts[2]);   // ac

        Object o = new Point(3, 4);
        if (o instanceof Point(int x, int _)) {    // 模式里也能用 _ 忽略某个分量
            System.out.println("x = " + x);        // x = 3
        }

        // 另一个典型场景：catch 里不关心异常对象
        try {
            Integer.parseInt("abc");
        } catch (NumberFormatException _) {
            System.out.println("转换失败，忽略具体异常信息");
        }
    }
}
```

### 2.11.2 Java 23（2024.9）：String Templates 被撤回

**String Templates（字符串模板）在 Java 23 被撤下**。它在 Java 21、22 各预览过一次（JEP 430、JEP 459），原计划继续预览的 JEP 465 最终被撤销，此后各版本 JDK 都不再包含这个特性——在 JDK 25 里，`java.lang.StringTemplate` 这个类根本不存在。所以「Java 26 会正式发布 String Templates」这样的说法是不可信的。

Java 23 的其他变化：

- 文档注释支持 Markdown（预览，JEP 467）
- ZGC 默认使用分代模式（JEP 474）
- 弃用 `sun.misc.Unsafe` 的内存访问方法（JEP 471），为彻底移除做准备
- Module Import Declarations 首次预览（JEP 476，Java 25 转正）

### 2.11.3 Java 24（2025.3）：Class-File API、Stream Gatherers 转正

- **Class-File API（JEP 484）**：正式发布，标准库可以直接读写、生成 class 文件，不再必须依赖 ASM。
- **Stream Gatherers（JEP 485）**：正式发布，为 Stream 添加自定义中间操作的能力。
- **永久禁用 SecurityManager（JEP 486）**：该项在 Java 17 就已弃用（JEP 411），Java 24 起无法再通过 `-Djava.security.manager` 启用。
- **虚拟线程不再因 `synchronized` 而钉住载体线程（JEP 491）**：虚拟线程在同步块中阻塞时不再占用平台线程。
- ZGC 移除非分代模式（JEP 490），AOT 类加载与链接支持（JEP 483）。

> ⚠️ 版本纠正：**Scoped Values 在 Java 24 仍然是预览特性**，它到 Java 25 才转正；**Structured Concurrency 到 Java 25 也还是预览特性**（`StructuredTaskScope` 在 JDK 25 上不加 `--enable-preview` 会直接报错）。另外，「Smart Enum Values」并不是一个 Java 特性——下面那种写法只是普通的**穷尽 switch 表达式**（Java 14 起支持，Java 21 起用于模式匹配）。

枚举上的穷尽 switch（不是新特性，但很好用）：

```java
enum Color {
    RED, GREEN, BLUE;

    Color opposite() {
        // 覆盖全部常量后不必写 default，编译器会检查穷尽性
        return switch (this) {
            case RED -> GREEN;
            case GREEN -> RED;
            case BLUE -> RED;
        };
    }
}
```

### 2.11.4 Java 25（2025.9，LTS）：Scoped Values、简洁源文件转正

Java 25 是新的 LTS 版本，转正的特性包括：

- **Scoped Values（JEP 506）**：正式发布，用来在虚拟线程之间安全地共享不可变数据，API 形如 `ScopedValue.where(KEY, value).run(...)`，比 `ThreadLocal` 更可控。
- **Module Import Declarations（JEP 511）**：正式发布，写一行 `import module java.base;` 就能把整个模块的包引入进来。
- **Compact Source Files and Instance Main Methods（JEP 512）**：正式发布，可以直接写 `void main() { ... }` 而不必声明类，非常适合教学和脚本。
- **Flexible Constructor Bodies（JEP 513）**：正式发布，构造函数里可以把校验语句写在 `super(...)` 之前。
- **Compact Object Headers（JEP 519）**：正式发布，降低对象头开销。
- 移除 32 位 x86 支持（JEP 503）。

以下代码在 JDK 25 上无需任何预览参数即可运行：

```java
import module java.base;
import java.lang.ScopedValue;

void main() {
    ScopedValue<String> USER = ScopedValue.newInstance();
    ScopedValue.where(USER, "alice").run(() -> System.out.println("当前用户: " + USER.get()));
    System.out.println("简洁源文件 + 模块导入 + ScopedValue 都可用");
}
```

仍在预览中的有：Structured Concurrency（第五次预览）、Primitive Types in Patterns（第三次预览）、Key Derivation API 等。

### 2.11.5 关于 Java 26 的说法：请以官方 JEP 列表为准

早期资料里关于「Java 26」的内容有不少错误或推测，至少下面几条可以肯定是不对的：

| 常见说法 | 实际情况 |
| --- | --- |
| FFM API 在 Java 26 才正式发布 | ❌ FFM API 在 **Java 22** 就已转正（JEP 454） |
| `catch (Exception e) when (...)` 异常过滤 | ❌ **Java 根本没有这种语法**，`when` 不能出现在 `catch` 之后（javac 会直接报 `'{' expected`） |
| String Templates 在 Java 26 正式发布 | ❌ 该特性在 Java 23 已被撤回，JDK 25 中不存在 `java.lang.StringTemplate` |
| Structured Concurrency 已是最终版 | ❌ 截至 JDK 25 它仍是预览特性 |

想了解某个 JDK 版本到底包含哪些特性，最可靠的做法是直接查该版本的 JEP 列表与官方发行说明，或者在本机用 `java -version` 对应的 JDK 亲手编译一次——很多「新特性」只要写几行代码就能验证真假。

**未来展望**：

- **Project Leyden**：AOT 相关的启动与内存占用优化，相关能力正逐步进入 JDK
- **Project Loom**：虚拟线程已落地，后续继续优化其调度与调试体验
- **Project Amber**：语法增强，包括模式匹配扩展等
- **Project Panama / Babylon**：前者产出了 FFM API，后者在探索更自然的外部代码与 GPU 加速支持


---

## 本章小结

回顾 Java 从 1996 到 2026 这三十年的发展历程，我们可以清晰地看到几条主线：

1. **语法现代化**：从 Java 5 的泛型、注解、枚举，到 Java 8 的 Lambda、Stream，再到 Java 14+ 的 record、密封类、模式匹配——Java 的语法越来越简洁、表达力越来越强。

2. **并发模型革新**：从原始的 `Thread` 到 `ExecutorService`，从 J.U.C 到 `CompletableFuture`，再到 Java 21 的虚拟线程——Java 的并发编程经历了三次革命。

3. **平台轻量化**：从 Applet 到 Java Web Start，从 J2EE 到 Spring，从模块化到 jlink 裁剪运行时——Java 一直在追求更轻、更快、更灵活。

4. **发布节奏稳定**：Oracle 采用的每六个月一个版本、LTS 每两年的策略，让 Java 既能快速迭代，又能保持稳定。

5. **向后兼容**：Java 30 年，始终保持惊人的向后兼容性。1996 年的 JAR 文件，今天的 JVM 依然能跑。这种稳定性，是 Java 成功的基石。

**各版本的「江湖地位」**：

- **Java 5**：语法革命奠基者
- **Java 8**：现代化转折点（最重要版本）
- **Java 9**：模块化开山之作
- **Java 11**：LTS 迁移目标
- **Java 17**：成熟稳重 LTS
- **Java 21**：虚拟线程革命（21 世纪最重要版本）
- **Java 26**：FFM API 正式版、功能完善

Java 不是一门靠「追新」取胜的语言。它的成功在于：**稳扎稳打、持续演进、向后兼容**。三十年过去了，Java 依然是全球最流行的编程语言之一，依然在企业级应用、后端开发、Android 开发等领域占据统治地位。

正如 James Gosling（Java 之父）所说：「Java 不是最好的语言，但它是一门将正确的事情做对的语言。」

下一章，我们将深入 Java 的核心机制——JVM 虚拟机。理解 JVM，才能真正理解 Java 的强大之处。
