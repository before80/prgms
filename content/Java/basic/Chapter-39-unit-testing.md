+++
title = "第39章 单元测试——代码质量的第一道防线"
weight = 390
date = "2026-03-30T14:33:56.924+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++
# 第三十九章 单元测试——代码质量的第一道防线

> "测试是活着代码的呼吸。没测试的代码，就像没系安全带的司机——技术再好也让人捏把汗。"

想象一下：你写了一堆代码，兴冲冲地部署上线，结果线上崩了。你挠挠头："本地明明跑得好好的啊？"——这时你需要的就是**单元测试（Unit Testing）**。

## 什么是单元测试？

**单元测试**是对软件中的最小可测试单元（通常是一个方法或一个类）进行验证的测试。它的核心目标是：**隔离被测单元，确保它在各种输入下都能给出正确的输出**。

为什么要强调"隔离"？因为单元测试的精髓就是——**不让你的测试受到外部世界的干扰**。数据库、网络、文件系统，这些通通靠边站！我们只测逻辑本身。

一个好的单元测试有以下几个特征，记住它们的英文缩写：**FIRST**：

- **F**ast（快速）：运行毫秒级，恨不得比泡面还快
- **I**ndependent（独立）：不依赖其他测试，不依赖执行顺序
- **R**epeatable（可重复）：每次运行结果一致，今天跑和明天跑一个样
- **S**elf-validating（自我验证）：测试自己判断通过还是失败，不需要人工干预
- **T**imely（及时）：与生产代码同步写，甚至先写测试再写代码（TDD）

Java 生态中，单元测试框架最常用的是 **JUnit**，而模拟外部依赖的利器则是 **Mockito**。这一章，我们就把这两个宝贝完全拆解给你看。

---

## 39.1 JUnit 5

### 39.1.1 JUnit 5 是什么？

**JUnit** 是 Java 世界里最流行的单元测试框架，没有之一。它的版本迭代也是 Java 社区的一面镜子——从 JUnit 3/4 到今天的 **JUnit 5（代号 Jupiter）**，整个架构都经历了脱胎换骨的改造。

JUnit 5 由三个子项目组成：

```
JUnit 5 = JUnit Platform + JUnit Jupiter + JUnit Vintage
```

- **JUnit Platform**：测试运行的基础设施。它定义了一套 API，任何测试引擎（比如 JUnit Jupiter、TestNG）都可以接入这个平台来运行测试。
- **JUnit Jupiter**：JUnit 5 的核心模块，提供了新的编程模型和扩展模型，也就是你写测试时直接打交道的注解和 API。
- **JUnit Vintage**：为了兼容旧项目而生的模块，允许在 JUnit 5 平台上运行 JUnit 3 和 JUnit 4 的测试。

```
┌─────────────────────────────────────────────────────────────┐
│                      JUnit 5 架构图                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   ┌─────────────────────────────────────────────────────┐   │
│   │                  JUnit Platform                      │   │
│   │    （测试运行基础设施，定义 TestEngine API）           │   │
│   └─────────────────────────────────────────────────────┘   │
│          ▲                ▲                ▲               │
│          │                │                │               │
│   ┌──────┴───┐      ┌─────┴────┐      ┌────┴────┐          │
│   │ Jupiter   │      │ Vintage   │      │ 其他引擎 │          │
│   │ Engine    │      │ Engine    │      │(TestNG等)│          │
│   │(JUnit 5)  │      │(JUnit 3/4)│      │          │          │
│   └───────────┘      └──────────┘      └──────────┘          │
│                                                             │
│   ┌─────────────────────────────────────────────────────┐   │
│   │                   JUnit Jupiter                      │   │
│   │         （编程模型 + 扩展模型 = 你写测试的API）        │   │
│   └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

简单说：Platform 是舞台，Jupiter 是台柱子演员，Vintage 是从老戏骨那里借来的演员（别急着退休）。

### 39.1.2 Maven 依赖

在 `pom.xml` 中加入 JUnit 5 的依赖：

```xml
<dependencies>
    <!-- JUnit Jupiter API：写测试时用的注解和断言 -->
    <dependency>
        <groupId>org.junit.jupiter</groupId>
        <artifactId>junit-jupiter-api</artifactId>
        <version>5.11.0</version>
        <scope>test</scope>
    </dependency>

    <!-- JUnit Jupiter Engine：运行 JUnit 5 测试的引擎 -->
    <dependency>
        <groupId>org.junit.jupiter</groupId>
        <artifactId>junit-jupiter-engine</artifactId>
        <version>5.11.0</version>
        <scope>test</scope>
    </dependency>
</dependencies>

<!-- Maven Surefire 插件：运行测试的 Maven 插件 -->
<build>
    <plugins>
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-surefire-plugin</artifactId>
            <version>3.2.5</version>
        </plugin>
    </plugins>
</build>
```

如果你用 Gradle，依赖更简洁：

```groovy
testImplementation 'org.junit.jupiter:junit-jupiter-api:5.11.0'
testRuntimeOnly 'org.junit.jupiter:junit-jupiter-engine:5.11.0'
```

### 39.1.3 第一个 JUnit 5 测试

废话少说，先看代码：

```java
// 文件：src/test/java/com/example/CalculatorTest.java

package com.example;

import org.junit.jupiter.api.Test;                  // ① 测试方法注解
import static org.junit.jupiter.api.Assertions.*;    // ② 断言工具静态导入

/**
 * 计算器测试类
 * 演示 JUnit 5 最基本的用法
 */
class CalculatorTest {

    // 用 @Test 注解标记的方法就是一个测试方法
    @Test
    void testAdd() {
        Calculator calculator = new Calculator();
        int result = calculator.add(2, 3);
        assertEquals(5, result);  // 断言：期待值是 5，实际值是 result
    }

    @Test
    void testDivide() {
        Calculator calculator = new Calculator();
        // 断言异常：期待抛出 ArithmeticException
        assertThrows(ArithmeticException.class, () -> calculator.divide(1, 0));
    }
}
```

```java
// 文件：src/main/java/com/example/Calculator.java

package com.example;

/**
 * 一个简陋的计算器
 */
public class Calculator {
    public int add(int a, int b) {
        return a + b;
    }

    public int subtract(int a, int b) {
        return a - b;
    }

    public int multiply(int a, int b) {
        return a * b;
    }

    public int divide(int a, int b) {
        return a / b;  // 注意：整数除法，且未处理除零
    }
}
```

运行方式很简单：在 IDEA 中右键运行类或方法，或者在命令行执行 `mvn test`。

> **提示**：JUnit 5 的测试类和方法不需要是 `public` 的（只要是 package-private 或 public 都可以），这比 JUnit 4 宽松多了。

### 39.1.4 生命周期与常用注解

JUnit 5 提供了一套完整的测试生命周期管理注解，让你可以在测试的不同阶段做不同的事情：

```java
package com.example;

import org.junit.jupiter.api.*;

/**
 * JUnit 5 生命周期注解演示
 */
class LifecycleDemoTest {

    // 走，看看各个注解的执行顺序
    @BeforeAll
    static void beforeAll() {
        System.out.println("【@BeforeAll】所有测试之前执行一次，类似JUnit4的@BeforeClass");
    }

    @AfterAll
    static void afterAll() {
        System.out.println("【@AfterAll】所有测试之后执行一次，类似JUnit4的@AfterClass");
    }

    @BeforeEach
    void beforeEach() {
        System.out.println("【@BeforeEach】每个测试方法之前都执行一次，类似JUnit4的@Before");
    }

    @AfterEach
    void afterEach() {
        System.out.println("【@AfterEach】每个测试方法之后都执行一次，类似JUnit4的@After");
    }

    @Test
    void testA() {
        System.out.println("  → 测试A执行中");
    }

    @Test
    void testB() {
        System.out.println("  → 测试B执行中");
    }
}
```

运行结果大概是这样的：

```
【@BeforeAll】所有测试之前执行一次
【@BeforeEach】每个测试方法之前都执行一次
  → 测试A执行中
【@AfterEach】每个测试方法之后都执行一次
【@BeforeEach】每个测试方法之前都执行一次
  → 测试B执行中
【@AfterEach】每个测试方法之后都执行一次
【@AfterAll】所有测试之后执行一次
```

注意：**`@BeforeAll` 和 `@AfterAll` 必须配 static 关键字**（或在接口 default 方法上使用），因为它们在实例创建之前/之后执行，不属于某个具体实例。

### 39.1.5 断言（Assertions）

断言是测试的核心——没有断言，测试就失去了意义。JUnit Jupiter 提供了一套丰富的断言 API，大部分在 `org.junit.jupiter.api.Assertions` 中：

```java
package com.example;

import org.junit.jupiter.api.Test;
import java.time.LocalDateTime;
import java.util.Arrays;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

/**
 * JUnit 5 常用断言演示
 */
class AssertionsDemoTest {

    // 最基本的相等断言
    @Test
    void testBasicAssertions() {
        assertEquals(4, 2 + 2);
        assertNotEquals(5, 2 + 2);
    }

    // 布尔断言
    @Test
    void testBooleanAssertions() {
        assertTrue(true);
        assertFalse(false);
    }

    // 空与非空断言
    @Test
    void testNullAssertions() {
        String name = "小明";
        String nullValue = null;

        assertNotNull(name);   // 期待非空
        assertNull(nullValue); // 期待为空
    }

    // 数组断言：深度比较
    @Test
    void testArrayAssertions() {
        int[] expected = {1, 2, 3};
        int[] actual = {1, 2, 3};
        assertArrayEquals(expected, actual);  // 内容相等，长度也要相等
    }

    // 异常断言：期待抛出的异常类型
    @Test
    void testExceptionAssertions() {
        int result = assertThrows(
            ArithmeticException.class,
            () -> 10 / 0  // 期待这里抛出 ArithmeticException
        );
    }

    // 超时断言：测试方法执行时间不超过指定值
    @Test
    void testTimeoutAssertions() {
        assertTimeout(
            java.time.Duration.ofSeconds(2),  // 2秒内必须完成
            () -> {
                Thread.sleep(100);  // 模拟耗时操作
                return "done";
            }
        );
    }

    // 分组断言：所有断言都会执行，最后一起报告
    @Test
    void testGroupedAssertions() {
        Person person = new Person("张三", 25);

        assertAll("person 完整信息验证",
            () -> assertEquals("张三", person.getName()),
            () -> assertEquals(25, person.getAge()),
            () -> assertNotNull(person.getId())
        );
    }

    // 列表断言
    @Test
    void testIterableAssertions() {
        List<String> expected = Arrays.asList("苹果", "香蕉", "橙子");
        List<String> actual = Arrays.asList("苹果", "香蕉", "橙子");
        assertIterableEquals(expected, actual);
    }

    // 简单的 Person 类用于测试
    static class Person {
        private String name;
        private int age;
        private String id;

        Person(String name, int age) {
            this.name = name;
            this.age = age;
        }

        String getName() { return name; }
        int getAge() { return age; }
        String getId() { return id; }
    }
}
```

### 39.1.6 嵌套测试（Nested Tests）

嵌套测试让你的测试代码更有层次感，用 **`@Nested`** 注解在内部类中可以表达测试的分组逻辑：

```java
package com.example;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

/**
 * 嵌套测试示例：针对栈数据结构
 */
class StackTest {

    Stack<String> stack;  // 被测对象

    @BeforeEach
    void createStack() {
        stack = new Stack<>();
    }

    @Nested   // 第一层嵌套：空栈的行为
    class WhenNew {

        @Test
        void shouldBeEmpty() {
            assertTrue(stack.isEmpty());
        }

        @Test
        void shouldThrowWhenPop() {
            assertThrows(IllegalStateException.class, stack::pop);
        }

        @Test
        void shouldThrowWhenPeek() {
            assertThrows(IllegalStateException.class, stack::peek);
        }
    }

    @Nested   // 第二层嵌套：压入元素后的行为
    class AfterPush {

        @BeforeEach
        void pushItem() {
            stack.push("第一");
            stack.push("第二");
        }

        @Test
        void shouldNotBeEmpty() {
            assertFalse(stack.isEmpty());
        }

        @Test
        void shouldReturnLifoOrder() {
            assertEquals("第二", stack.pop());  // 后进先出
            assertEquals("第一", stack.pop());
        }

        @Test
        void shouldReturnSizeTwo() {
            assertEquals(2, stack.size());
        }
    }

    // 简单的栈实现
    static class Stack<T> {
        private java.util.ArrayList<T> items = new java.util.ArrayList<>();

        void push(T item) { items.add(item); }
        T pop() {
            if (isEmpty()) throw new IllegalStateException("栈为空");
            return items.remove(items.size() - 1);
        }
        T peek() {
            if (isEmpty()) throw new IllegalStateException("栈为空");
            return items.get(items.size() - 1);
        }
        boolean isEmpty() { return items.isEmpty(); }
        int size() { return items.size(); }
    }
}
```

这样分层之后，测试报告读起来就像一本有条理的书：`StackTest > WhenNew > shouldBeEmpty`。

### 39.1.7 参数化测试（Parameterized Tests）

参数化测试让你用**不同的参数多次运行同一个测试**，再也不用复制粘贴 N 个测试方法了。

**依赖添加**（需要 junit-jupiter-params 模块，通常与 junit-jupiter 一起包含）：

```xml
<dependency>
    <groupId>org.junit.jupiter</groupId>
    <artifactId>junit-jupiter-params</artifactId>
    <version>5.11.0</version>
    <scope>test</scope>
</dependency>
```

```java
package com.example;

import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;    // CSV 格式参数
import org.junit.jupiter.params.provider.ValueSource; // 单一值来源
import org.junit.jupiter.params.provider.MethodSource; // 自定义方法来源
import org.junit.jupiter.params.provider.NullSource;  // 包含 null 参数

import static org.junit.jupiter.api.Assertions.*;

/**
 * 参数化测试示例
 */
class ParameterizedDemoTest {

    // 方式一：@ValueSource - 最简单的整数/字符串字面量数组
    @ParameterizedTest
    @ValueSource(ints = {1, 2, 3, 4, 5})
    void testIsOdd(int number) {
        assertTrue(number % 2 != 0);
    }

    // 方式二：@CsvSource - 多参数，每行是一个测试用例
    @ParameterizedTest
    @CsvSource({
        "1,      2,      3",
        "10,    20,     30",
        "100,   200,   300"
    })
    void testAdd(int a, int b, int expectedSum) {
        assertEquals(expectedSum, a + b);
    }

    // 方式三：@MethodSource - 引用一个返回 Stream 的静态方法
    @ParameterizedTest
    @MethodSource("stringProvider")
    void testStringLength(String input) {
        assertNotNull(input);
        assertTrue(input.length() >= 0);
    }

    // 提供测试数据的方法（必须是 static 的）
    static java.util.stream.Stream<String> stringProvider() {
        return java.util.stream.Stream.of("Hello", "World", "JUnit5");
    }

    // 方式四：@NullSource - 自动补充 null 值
    @ParameterizedTest
    @NullSource
    @ValueSource(strings = {"你好", "世界"})
    void testNullAndStrings(String input) {
        assertTrue(input == null || !input.isEmpty());
    }

    // 方式五：@CsvFileSource - 引用外部 CSV 文件
    // @ParameterizedTest
    // @CsvFileSource(resources = "/test-data.csv")
    // void testFromCsvFile(String col1, int col2) { ... }
}
```

### 39.1.8 动态测试（Dynamic Tests）

如果你在编译时不知道有多少个测试用例，可以用 **`@TestFactory`** 注解返回一个动态生成的测试集合：

```java
package com.example;

import org.junit.jupiter.api.TestFactory;
import java.util.Arrays;
import java.util.List;
import java.util.stream.Stream;

import static org.junit.jupiter.api.Assertions.*;
import static org.junit.jupiter.api.DynamicTest.*;

/**
 * 动态测试示例
 * 适用场景：测试用例数量需要运行时决定
 */
class DynamicDemoTest {

    @TestFactory
    Stream<DynamicTest> dynamicTestsFromCollection() {
        List<String> inputs = Arrays.asList("apple", "banana", "cherry");

        // 为每个输入动态生成一个测试
        return inputs.stream()
            .map(input ->
                dynamicTest("测试字符串: " + input, () -> {
                    assertNotNull(input);
                    assertTrue(input.length() > 0);
                })
            );
    }
}
```

### 39.1.9 条件执行与禁用测试

有时候你想让某些测试在特定条件下才执行：

```java
package com.example;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.condition.*;
import org.junit.jupiter.api.Disabled;

/**
 * 条件执行与禁用测试
 */
class ConditionalDemoTest {

    // 只在 Linux 上运行
    @Test
    @EnabledOnOs(OS.LINUX)
    void onlyOnLinux() {
        System.out.println("只在 Linux 上运行");
    }

    // 在 Windows 和 macOS 上禁用
    @Test
    @DisabledOnOs({OS.WINDOWS, OS.MAC})
    void notOnWindowsOrMac() {
        System.out.println("Windows 和 macOS 上不运行");
    }

    // 只在 JDK 17+ 上运行
    @Test
    @EnabledForJreRange(min = JRE.JAVA_17)
    void onlyOnJava17OrLater() {
        System.out.println("Java 17+ 才运行");
    }

    // 自定义条件：系统属性满足时才运行
    @Test
    @EnabledIfSystemProperty(named = "os.arch", matches = ".*64.*")
    void onlyOn64Bit() {
        System.out.println("64位系统专属");
    }

    // 彻底禁用这个测试
    @Test
    @Disabled("这个功能还在开发中，暂时跳过")
    void disabledTest() {
        // 不会执行
        fail("不应该到达这里");
    }
}
```

---

## 39.2 Mockito

### 39.2.1 为什么需要 Mockito？

好，现在你已经会写 JUnit 测试了。但现实往往是残酷的——你的代码不可能是一座孤岛，它总会依赖数据库、依赖外部 API、依赖文件系统。当你写单元测试时，这些外部依赖就成了拦路虎：

- 数据库可能不存在
- 外部 API 可能网络不通
- 文件系统可能被权限阻挡

这时候你就需要 **Mock（模拟）** 技术。**Mock 的本质是创造一个假的对象（Fake Object），它长得和真的一样，但行为完全由你控制。**

比如，你的服务需要调用一个 `UserRepository` 来获取用户数据，但数据库根本不存在——这时候你可以 Mock 掉这个 `UserRepository`，让它"假装"返回你指定的用户数据。

**Mockito** 是 Java 生态中最流行的 Mock 框架，以 API 简洁、错误信息清晰著称。它的口号很有意思——"Mockito tastes really good. It lets you write beautiful tests with a clean & simple API."（Mockito 尝起来美味极了，让你用简洁美观的 API 写出漂亮的测试。）

### 39.2.2 Maven 依赖

```xml
<dependency>
    <groupId>org.mockito</groupId>
    <artifactId>mockito-core</artifactId>
    <version>5.11.0</version>
    <scope>test</scope>
</dependency>

<!-- 如果你用 Java 9+ 并且遇到模块化问题，可能需要这个 -->
<dependency>
    <groupId>org.mockito</groupId>
    <artifactId>mockito-junit-jupiter</artifactId>
    <version>5.11.0</version>
    <scope>test</scope>
</dependency>
```

### 39.2.3 Mock 对象的创建与基本使用

```java
package com.example;

import org.junit.jupiter.api.Test;
import java.util.*;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

/**
 * Mockito 基础用法演示
 */
class MockitoBasicTest {

    @Test
    void testMockList() {
        // 方式一：mock() 方法直接创建
        List<String> mockedList = mock(List.class);

        // 使用这个假的 List，它不会真正存任何数据
        mockedList.add("one");
        mockedList.add("two");
        mockedList.clear();

        // 验证这些方法确实被调用了（后面会详细讲 verify）
        verify(mockedList).add("one");
        verify(mockedList).add("two");
        verify(mockedList).clear();
    }

    @Test
    void testStubbing() {
        // Mock 一个 LinkedList
        LinkedList<String> mockedList = mock(LinkedList.class);

        // Stubbing（打桩）：设定指定方法在指定参数下返回什么
        when(mockedList.get(0)).thenReturn("first");
        when(mockedList.get(1)).thenReturn("second");

        // 调用 get(0)，返回 "first"
        assertEquals("first", mockedList.get(0));

        // 调用 get(999)，没有打桩，返回 null
        assertNull(mockedList.get(999));
    }

    @Test
    void testStubbingExceptions() {
        Stack<Integer> mockedStack = mock(Stack.class);

        // 打桩抛出异常
        when(mockedStack.pop())
            .thenThrow(new IllegalStateException("栈为空"));

        assertThrows(IllegalStateException.class, mockedStack::pop);
    }

    // 简单的 Stack 类用于演示
    static class Stack<T> {
        public T pop() { throw new UnsupportedOperationException(); }
        public void push(T item) {}
        public T peek() { throw new UnsupportedOperationException(); }
    }
}
```

### 39.2.4 @Mock 注解——告别重复的 mock() 调用

如果一个测试类里需要很多 Mock 对象，手动每次 `mock(...)` 就太烦了。Mockito 提供了 **`@Mock` 注解**，配合 **`MockitoExtension`**，可以自动注入 Mock 对象：

```java
package com.example;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

/**
 * 使用 @Mock 注解的示例
 * 需要配合 @ExtendWith(MockitoExtension.class) 使用
 */
@ExtendWith(MockitoExtension.class)   // JUnit 5 扩展
class MockAnnotationTest {

    // 注解方式声明 Mock 对象
    @Mock
    private List<String> mockList;

    @Mock
    private Map<String, Integer> mockMap;

    @Test
    void testMockList() {
        // 直接使用 mockList，它已经被自动创建好了
        when(mockList.get(0)).thenReturn("Hello");
        when(mockList.size()).thenReturn(1);

        assertEquals("Hello", mockList.get(0));
        assertEquals(1, mockList.size());

        verify(mockList).get(0);
    }

    @Test
    void testMockMap() {
        when(mockMap.get("age")).thenReturn(25);

        assertEquals(25, mockMap.get("age"));
    }
}
```

> **小技巧**：`@Mock` 注解的对象默认是 `null`，需要 `MockitoExtension` 或 `MockitoAnnotations.openMocks(this)` 来初始化。如果你用 JUnit 5，用 `@ExtendWith(MockitoExtension.class)` 最省事。

### 39.2.5 打桩（Stubbing）进阶

基础的 `when(...).thenReturn(...)` 只是开胃菜，Mockito 的打桩还有更多玩法：

```java
package com.example;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.List;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

/**
 * Mockito 打桩进阶
 */
@ExtendWith(MockitoExtension.class)
class StubbingAdvancedTest {

    @Mock
    private List<String> mockList;

    @Mock
    private Map<String, Integer> mockMap;

    // 连续打桩：每次调用返回不同的值（类似迭代器）
    @Test
    void testConsecutiveStubbing() {
        when(mockList.get(anyInt()))
            .thenReturn("第一次调用")    // 第一次
            .thenReturn("第二次调用")    // 第二次
            .thenThrow(new RuntimeException("没了")); // 第三次及以后抛异常

        assertEquals("第一次调用", mockList.get(0));
        assertEquals("第二次调用", mockList.get(1));
        assertThrows(RuntimeException.class, () -> mockList.get(2));
    }

    // doReturn-when 风格：适合在 spy 或不想立即调用时使用
    @Test
    void testDoReturnStyle() {
        doReturn("绕过").when(mockList).get(0);

        assertEquals("绕过", mockList.get(0));
    }

    // doThrow-when 风格：适合 void 方法
    @Test
    void testDoThrowStyle() {
        doThrow(new IllegalStateException("列表坏了")).when(mockList).clear();

        assertThrows(IllegalStateException.class, () -> mockList.clear());
    }

    // 用参数匹配器（Argument Matchers）灵活匹配参数
    @Test
    void testArgumentMatchers() {
        when(mockMap.get(anyString())).thenReturn(100);
        when(mockMap.containsKey(null)).thenReturn(false);

        assertEquals(100, mockMap.get("北京"));
        assertEquals(100, mockMap.get("上海"));
        assertFalse(mockMap.containsKey(null));
    }

    // 懒验证（lenient）：某些情况下允许不必要的 stub 警告
    @Test
    void testLenientStubbing() {
        lenient().when(mockList.size()).thenReturn(10);  // 不常用但不会警告

        // mockList.size() 可能根本没被调用，但不会报警
    }

    // 验证方法调用的次数
    @Test
    void testVerificationModes() {
        mockList.add("a");
        mockList.add("b");
        mockList.add("a");

        // 验证 add("a") 被调用了恰好 2 次
        verify(mockList, times(2)).add("a");

        // 验证 add("b") 被调用了至少 1 次
        verify(mockList, atLeast(1)).add("b");

        // 验证从来没有调用过 clear()
        verify(mockList, never()).clear();

        // 验证没有更多调用了（可选）
        verifyNoMoreInteractions(mockList);
    }

    // 验证调用顺序
    @Test
    void testInOrderVerification() {
        InOrder inOrder = inOrder(mockList);

        mockList.add("第一");
        mockList.add("第二");
        mockList.add("第三");

        inOrder.verify(mockList).add("第一");
        inOrder.verify(mockList).add("第二");
        inOrder.verify(mockList).add("第三");
    }
}
```

### 39.2.6 Argument Matchers（参数匹配器）

参数匹配器是 Mockito 中最强大的武器之一。它允许你用 **`anyInt()`、`anyString()`、`any()`、`eq()`** 等通配符来匹配参数，而不是写死具体值：

```java
package com.example;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.*;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

/**
 * 参数匹配器（Argument Matchers）演示
 */
@ExtendWith(MockitoExtension.class)
class ArgumentMatchersTest {

    @Mock
    private List<String> mockList;

    @Mock
    private Map<String, Object> mockMap;

    @Test
    void testVariousMatchers() {
        // anyInt() / anyString()：匹配任意值
        when(mockList.get(anyInt())).thenReturn("匹配任何整数索引");
        assertEquals("匹配任何整数索引", mockList.get(0));
        assertEquals("匹配任何整数索引", mockList.get(999));

        // any()：匹配任意对象（包括 null，除非用 anyNonNull()）
        when(mockMap.put(any(), any())).thenReturn(0);
        mockMap.put("key", new Object());

        // eq()：精确匹配某个值，常和其他匹配器混用
        when(mockList.contains(eq("Java"))).thenReturn(true);
        assertTrue(mockList.contains("Java"));
    }

    @Test
    void testComplexMatchers() {
        // anyList() / anySet() / anyMap()：匹配任意集合
        when(mockMap.containsKey(anyList())).thenReturn(false);

        List<String> keys = Arrays.asList("a", "b");
        assertFalse(mockMap.containsKey(keys));

        // nullable()：可以匹配 null
        when(mockMap.get(nullable(String.class))).thenReturn("可以为null");
        assertEquals("可以为null", mockMap.get(null));

        // startsWith / contains / endsWith：字符串通配
        // 需要导入 import static org.mockito.Mockito.*;
        // 和 import org.mockito.ArgumentMatchers.*;
    }

    @Test
    void testCombineMatchers() {
        // 混合使用精确值和通配符
        when(mockList.set(anyInt(), eq("Hello"))).thenReturn("原值");

        assertEquals("原值", mockList.set(0, "Hello"));
        assertEquals("原值", mockList.set(5, "Hello"));
    }
}
```

> **注意**：使用参数匹配器时，所有参数都要用匹配器，或者都不用。不能一个用 `anyInt()` 另一个用具体值。

### 39.2.7 @InjectMocks——自动注入的最佳拍档

当一个类依赖多个 Mock 对象时，手动一个个 `new` 并 set 进去非常繁琐。**`@InjectMocks`** 可以帮你自动把 Mock 对象注入到待测类中：

```java
package com.example;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

/**
 * @InjectMocks 演示：自动依赖注入
 */
@ExtendWith(MockitoExtension.class)
class InjectMocksTest {

    // 这些都是外部依赖，打造成 Mock
    @Mock
    private UserRepository userRepository;

    @Mock
    private EmailService emailService;

    @Mock
    private Logger logger;

    // 待测的 Service，mockito 会自动把上面的 Mock 注入进来
    @InjectMocks
    private UserService userService;

    @Test
    void testRegister() {
        // 给 Mock 对象打桩
        when(userRepository.findByEmail("test@example.com"))
            .thenReturn(null);  // 没有重复用户
        when(userRepository.save(any(User.class)))
            .thenAnswer(invocation -> invocation.getArgument(0)); // 保存并返回
        doNothing().when(emailService).sendWelcomeEmail(any(User.class));

        // 调用真正的业务方法
        User newUser = userService.register("张三", "test@example.com");

        // 验证结果
        assertNotNull(newUser);
        assertEquals("张三", newUser.getName());
        assertEquals("test@example.com", newUser.getEmail());

        // 验证交互
        verify(userRepository).findByEmail("test@example.com");
        verify(userRepository).save(any(User.class));
        verify(emailService).sendWelcomeEmail(any(User.class));
    }

    // 下面是需要用到的几个类

    static class UserService {
        private final UserRepository userRepository;
        private final EmailService emailService;
        private final Logger logger;

        // 构造函数注入
        UserService(UserRepository userRepository,
                    EmailService emailService,
                    Logger logger) {
            this.userRepository = userRepository;
            this.emailService = emailService;
            this.logger = logger;
        }

        User register(String name, String email) {
            User existing = userRepository.findByEmail(email);
            if (existing != null) {
                throw new IllegalArgumentException("邮箱已被注册");
            }
            User user = new User(name, email);
            User saved = userRepository.save(user);
            emailService.sendWelcomeEmail(saved);
            return saved;
        }
    }

    static class User {
        private String name;
        private String email;
        User(String name, String email) { this.name = name; this.email = email; }
        String getName() { return name; }
        String getEmail() { return email; }
    }

    interface UserRepository {
        User findByEmail(String email);
        User save(User user);
    }

    interface EmailService {
        void sendWelcomeEmail(User user);
    }

    interface Logger {
        void log(String message);
    }
}
```

`@InjectMocks` 会尝试按以下顺序注入：
1. **构造函数注入**（优先使用参数最多的构造函数）
2. **setter 注入**
3. **字段注入**（直接反射赋值）

### 39.2.8 Spy——部分 Mock

有时候你不想完全 Mock 一个对象，而是想 Mock 它其中的一部分方法，保留其他部分的真实行为——这时候用 **`@Spy`** 或 **`spy()`** 方法：

```java
package com.example;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Spy;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.ArrayList;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

/**
 * Spy（监视真实对象）演示
 */
@ExtendWith(MockitoExtension.class)
class SpyDemoTest {

    // @Spy：创建一个真实对象的"间谍"，部分方法可以被 Mock
    @Spy
    private List<String> realList = new ArrayList<>();

    @Test
    void testSpy() {
        // 真实行为：add 方法真的会把元素加进去
        realList.add("第一");
        realList.add("第二");

        assertEquals(2, realList.size()); // 真实行为

        // Mock 行为：get(0) 被 stub，返回"被监视的值"
        when(realList.get(0)).thenReturn("被监视的值");

        assertEquals("被监视的值", realList.get(0)); // Mock 行为
        assertEquals("第二", realList.get(1));       // 真实行为
    }

    @Test
    void testSpyWithDoReturn() {
        // Spy 不能用 when().thenReturn() 因为会立即调用真实方法
        // 要用 doReturn().when() 风格
        doReturn("不走原路").when(realList).get(10);

        assertEquals("不走原路", realList.get(10)); // 10越界，但被拦截了
    }
}
```

> **警告**：Spy 会调用真实方法，如果 `when(...).thenReturn(...)` 中间真实方法出错，你就掉坑里了。因此 Spy 中推荐用 `doReturn(...).when(...)` 风格。

### 39.2.9 实战：一个完整的 Service 测试

最后，我们用一个更完整的例子，把 JUnit 5 + Mockito 的组合拳打出来：

```java
package com.example;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.math.BigDecimal;
import java.util.Arrays;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

/**
 * 完整的业务场景测试：订单服务 + Mockito
 */
@ExtendWith(MockitoExtension.class)
class OrderServiceTest {

    @Mock
    private PaymentGateway paymentGateway;

    @Mock
    private InventoryService inventoryService;

    @Mock
    private NotificationService notificationService;

    private OrderService orderService;

    @BeforeEach
    void setUp() {
        orderService = new OrderService(
            paymentGateway, inventoryService, notificationService
        );
    }

    @Test
    void testPlaceOrder_Success() {
        // ============ 准备数据（Arrange）============

        // 模拟库存服务：检查库存，所有商品都有货
        when(inventoryService.checkStock("商品A", 2))
            .thenReturn(true);
        when(inventoryService.checkStock("商品B", 1))
            .thenReturn(true);

        // 模拟支付网关：支付成功
        when(paymentGateway.process("6222-****-****-1234",
            new BigDecimal("150.00")))
            .thenReturn(true);

        // 准备订单
        Order order = new Order(
            "ORDER-001",
            "张三",
            "6222-****-****-1234",
            Arrays.asList(
                new OrderItem("商品A", 2, new BigDecimal("80.00")),
                new OrderItem("商品B", 1, new BigDecimal("70.00"))
            )
        );

        // ============ 执行操作（Act）============
        OrderResult result = orderService.placeOrder(order);

        // ============ 验证结果（Assert）============
        assertTrue(result.isSuccess());
        assertEquals("订单支付成功！", result.getMessage());

        // 验证支付网关确实被调用了
        verify(paymentGateway).process(eq("6222-****-****-1234"), any(BigDecimal.class));

        // 验证通知服务发送了邮件
        verify(notificationService).sendEmail(eq("张三"), contains("订单"));
    }

    @Test
    void testPlaceOrder_InsufficientStock() {
        // 模拟库存不足
        when(inventoryService.checkStock("商品A", 2))
            .thenReturn(false);  // 商品A库存不足

        Order order = new Order(
            "ORDER-002",
            "李四",
            "6222-****-****-5678",
            Arrays.asList(
                new OrderItem("商品A", 2, new BigDecimal("80.00"))
            )
        );

        OrderResult result = orderService.placeOrder(order);

        assertFalse(result.isSuccess());
        assertEquals("商品A 库存不足", result.getMessage());

        // 库存不足时，不应该调用支付网关
        verify(paymentGateway, never()).process(anyString(), any(BigDecimal.class));
    }

    @Test
    void testPlaceOrder_PaymentFailed() {
        // 有库存，但支付失败
        when(inventoryService.checkStock(anyString(), anyInt()))
            .thenReturn(true);
        when(paymentGateway.process(anyString(), any(BigDecimal.class)))
            .thenReturn(false);  // 支付失败

        Order order = new Order(
            "ORDER-003",
            "王五",
            "6222-****-****-9999",
            Arrays.asList(
                new OrderItem("商品C", 1, new BigDecimal("50.00"))
            )
        );

        OrderResult result = orderService.placeOrder(order);

        assertFalse(result.isSuccess());
        assertEquals("支付失败，请重试", result.getMessage());
    }

    // ========== 以下是被测代码和依赖的定义 ==========

    // 订单服务
    static class OrderService {
        private final PaymentGateway paymentGateway;
        private final InventoryService inventoryService;
        private final NotificationService notificationService;

        OrderService(PaymentGateway paymentGateway,
                     InventoryService inventoryService,
                     NotificationService notificationService) {
            this.paymentGateway = paymentGateway;
            this.inventoryService = inventoryService;
            this.notificationService = notificationService;
        }

        OrderResult placeOrder(Order order) {
            // 1. 检查库存
            for (OrderItem item : order.getItems()) {
                if (!inventoryService.checkStock(item.getName(), item.getQuantity())) {
                    return new OrderResult(false, item.getName() + " 库存不足");
                }
            }

            // 2. 计算总价
            BigDecimal total = order.getItems().stream()
                .map(item -> item.getPrice().multiply(BigDecimal.valueOf(item.getQuantity())))
                .reduce(BigDecimal.ZERO, BigDecimal::add);

            // 3. 支付
            boolean paid = paymentGateway.process(order.getCardNumber(), total);
            if (!paid) {
                return new OrderResult(false, "支付失败，请重试");
            }

            // 4. 发送通知
            notificationService.sendEmail(order.getCustomerName(), "订单 " + order.getId() + " 已确认");

            return new OrderResult(true, "订单支付成功！");
        }
    }

    // 订单类
    static class Order {
        private final String id;
        private final String customerName;
        private final String cardNumber;
        private final List<OrderItem> items;

        Order(String id, String customerName, String cardNumber, List<OrderItem> items) {
            this.id = id;
            this.customerName = customerName;
            this.cardNumber = cardNumber;
            this.items = items;
        }

        String getId() { return id; }
        String getCustomerName() { return customerName; }
        String getCardNumber() { return cardNumber; }
        List<OrderItem> getItems() { return items; }
    }

    // 订单项类
    static class OrderItem {
        private final String name;
        private final int quantity;
        private final BigDecimal price;

        OrderItem(String name, int quantity, BigDecimal price) {
            this.name = name; this.quantity = quantity; this.price = price;
        }
        String getName() { return name; }
        int getQuantity() { return quantity; }
        BigDecimal getPrice() { return price; }
    }

    // 订单结果
    static class OrderResult {
        private final boolean success;
        private final String message;
        OrderResult(boolean success, String message) {
            this.success = success; this.message = message;
        }
        boolean isSuccess() { return success; }
        String getMessage() { return message; }
    }

    // 外部依赖接口（由 Mockito Mock）
    interface PaymentGateway {
        boolean process(String cardNumber, BigDecimal amount);
    }

    interface InventoryService {
        boolean checkStock(String productName, int quantity);
    }

    interface NotificationService {
        void sendEmail(String to, String content);
    }
}
```

这就是经典的 **Arrange-Act-Assert（AAA）模式**：先准备数据（Arrange），再执行操作（Act），最后验证结果（Assert）。配合 Mockito 的 Mock 和 verify，测试既干净又可靠。

---

## 本章小结

本章我们系统学习了 Java 单元测试的两大支柱——JUnit 5 和 Mockito：

**JUnit 5 核心要点：**

- JUnit 5 由 Platform（运行基础设施）、Jupiter（编程模型）、Vintage（兼容旧版）三部分组成
- 常用注解：`@Test`（测试方法）、`@BeforeEach`/`@AfterEach`（每个测试前后）、`@BeforeAll`/`@AfterAll`（全部测试前后）
- 断言是测试的灵魂：`assertEquals`、`assertThrows`、`assertAll` 等组合使用
- `@Nested` 支持嵌套测试，表达更清晰的测试层次
- `@ParameterizedTest` 让同一个测试用不同数据反复运行
- `@Disabled` 可以临时跳过某些测试

**Mockito 核心要点：**

- Mock 是用假对象替代真实外部依赖的技术，Mockito 是 Java 最流行的 Mock 框架
- `mock()` 创建 Mock 对象，`when(...).thenReturn(...)` 打桩，`verify(...)` 验证调用
- `@Mock` 注解 + `@ExtendWith(MockitoExtension.class)` 自动注入，省去手动 mock 繁琐
- `@InjectMocks` 自动将 Mock 对象注入待测 Service
- `@Spy` 可以监视真实对象，保留部分真实行为
- 参数匹配器（`anyInt()`、`anyString()`、`eq()`）让打桩更灵活
- 验证方法调用次数（`times()`、`atLeast()`、`never()`）

**两者的黄金组合：**

JUnit 5 负责测试的运行、生命周期和断言，Mockito 负责隔离外部依赖，两者配合使用，构成了现代 Java 单元测试的标准范式。写好单元测试，不仅是提升代码质量，更是给未来的自己留下一份可信赖的保障——毕竟，代码会变，但跑过的测试不会骗人。

> 记住：**没有测试的代码，终究是在走钢丝。测了之后，才算真正落地。**
