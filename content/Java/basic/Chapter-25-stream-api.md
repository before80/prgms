+++
title = "第25章 Stream API——处理数据的新方式"
weight = 250
date = "2026-03-30T14:33:56.907+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++
# 第二十五章 Stream API——处理数据的新方式

想象一下，你有一仓库的快递（数据），传统做法是你得亲自一个个拆开、检查、分类、搬运。累不累？累死了！

Stream API 就是你的全自动智能分拣流水线——你只需要告诉它"我要什么"，它帮你搞定一切。

> **Stream 是什么？** Stream 是 Java 8 引入的高级 API，它不是数据结构，而是一条"数据处理流水线"。你可以把它想象成一条传送带，数据从一端进去，经过各种处理（过滤、映射、排序等），从另一端出来时就变成了你想要的样子。

---

## 25.1 Stream 的三个特性

Stream 有三个核心特性，记住了这些，你就掌握了 Stream 的精髓。

### 25.1.1 不存储数据

Stream 就像一条流水管道，它本身不存放任何数据。数据只是从它里面"流过"，处理完就没了（或者说， Stream 是一次性的）。

```java
import java.util.Arrays;
import java.util.List;
import java.util.stream.Stream;

public class StreamNoStorage {
    public static void main(String[] args) {
        List<String> names = Arrays.asList("Alice", "Bob", "Charlie");

        // Stream 本身不存储数据，它只是处理数据的一种方式
        Stream<String> stream = names.stream();

        // 消费 stream 之后，stream 就"用完了"
        stream.forEach(System.out::println);

        // 再次使用会抛出异常：Stream has already been operated upon or closed
        // stream.forEach(System.out::println); // 别试，会报错！
    }
}
```

### 25.1.2 不修改源数据

Stream 是个"只读"通道，它不会改变原始数据源。你用 Stream 过滤、映射、排序，原始集合毫发无损。

```java
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

public class StreamNoModifySource {
    public static void main(String[] args) {
        List<Integer> numbers = new ArrayList<>(Arrays.asList(1, 2, 3, 4, 5));

        System.out.println("原始数据: " + numbers);

        // 过滤出偶数，生成新列表
        List<Integer> evens = numbers.stream()
                                     .filter(n -> n % 2 == 0)
                                     .collect(Collectors.toList());

        System.out.println("过滤后的结果: " + evens);
        System.out.println("原始数据（毫发无损）: " + numbers);
    }
}
```

输出：
```
原始数据: [1, 2, 3, 4, 5]
过滤后的结果: [2, 4]
原始数据（毫发无损）: [1, 2, 3, 4, 5]
```

### 25.1.3 惰性执行

这是 Stream 最聪明的设计——**惰性求值（Lazy Evaluation）**。

Stream 只有遇到**终端操作**（Terminal Operation）时，才会真正开始执行中间的所有步骤。就像你下了订单，工厂不会马上生产，而是等你说"确认付款"才开始流水线。

```java
import java.util.Arrays;
import java.util.List;
import java.util.stream.Stream;

public class StreamLazy {
    public static void main(String[] args) {
        List<String> names = Arrays.asList("Alice", "Bob", "Charlie", "Diana");

        // 这只是"配置"流水线，没有实际执行
        Stream<String> stream = names.stream()
                                     .filter(name -> {
                                         System.out.println("过滤: " + name);
                                         return name.length() > 3;
                                     })
                                     .map(name -> {
                                         System.out.println("映射: " + name);
                                         return name.toUpperCase();
                                     });

        System.out.println("===== 我只是配置了流水线，还没开始干活 =====");

        // 只有调用终端操作，才会真正执行前面的步骤
        long count = stream.count();

        System.out.println("===== 执行完毕，共 " + count + " 个元素 =====");
    }
}
```

输出：
```
===== 我只是配置了流水线，还没开始干活 =====
过滤: Alice
映射: ALICE
过滤: Bob
过滤: Charlie
映射: CHARLIE
过滤: Diana
===== 执行完毕，共 2 个元素 =====
```

---

## 25.2 创建 Stream

知道了 Stream 的特性，接下来看看怎么创建 Stream。创建方式有很多种，就像"条条大路通罗马"。

### 25.2.1 从集合创建

最常用的方式，Collection 接口提供了 `stream()` 方法。

```java
import java.util.Arrays;
import java.util.List;

public class CreateFromCollection {
    public static void main(String[] args) {
        List<String> fruits = Arrays.asList("Apple", "Banana", "Cherry", "Date");

        // 从 List 创建 Stream
        fruits.stream()
              .forEach(f -> System.out.println("水果: " + f));

        // 从 Set 创建 Stream（无序）
        // set.stream().forEach(...);

        // 从 Map 创建 Stream
        // map.entrySet().stream() // 键值对
        // map.keySet().stream()   // 键
        // map.values().stream()   // 值
    }
}
```

### 25.2.2 使用 Stream.of() 和 Stream.builder()

直接用静态方法创建 Stream，适合少量已知数据。

```java
import java.util.stream.Stream;

public class CreateWithOf {
    public static void main(String[] args) {
        // 使用 Stream.of() 直接创建
        Stream<String> stream1 = Stream.of("Java", "Python", "JavaScript", "Go");

        stream1.forEach(lang -> System.out.println("编程语言: " + lang));

        // 使用 Stream.builder() 构建
        Stream.Builder<String> builder = Stream.builder();

        builder.add("HTML")
               .add("CSS")
               .add("SQL");

        Stream<String> stream2 = builder.build();
        stream2.forEach(tech -> System.out.println("技术: " + tech));
    }
}
```

### 25.2.3 从数组创建

使用 `Arrays.stream()` 或 `Stream.of()`。

```java
import java.util.Arrays;
import java.util.stream.Stream;

public class CreateFromArray {
    public static void main(String[] args) {
        int[] numbers = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};

        // 从 int 数组创建 IntStream（专门处理 int 的 Stream，性能更好）
        int sum = Arrays.stream(numbers)
                        .filter(n -> n % 2 == 0)
                        .sum();

        System.out.println("1-10 中偶数的和: " + sum);

        // String 数组用 Stream.of()
        String[] names = {"Tom", "Jerry", "Spike"};
        Stream<String> nameStream = Stream.of(names);
        nameStream.forEach(System.out::println);
    }
}
```

### 25.2.4 使用 Stream.iterate() 和 Stream.generate()

创建无限 Stream（但通常配合 `limit()` 限制数量）。

```java
import java.util.stream.Stream;

public class CreateInfiniteStream {
    public static void main(String[] args) {
        // iterate: 种子值 + 一元运算符（生成奇数序列）
        Stream<Integer> oddNumbers = Stream.iterate(1, n -> n + 2)
                                          .limit(10);

        System.out.print("前10个奇数: ");
        oddNumbers.forEach(n -> System.out.print(n + " "));
        System.out.println();

        // generate: 使用 Supplier 生成随机数
        Stream<Double> randoms = Stream.generate(Math::random)
                                       .limit(5);

        System.out.print("5个随机数: ");
        randoms.forEach(d -> System.out.printf("%.4f ", d));
        System.out.println();
    }
}
```

### 25.2.5 其他创建方式

```java
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.stream.IntStream;
import java.util.stream.Stream;

public class CreateOtherWays {
    public static void main(String[] args) throws Exception {
        // 从文件行创建 Stream
        // Stream<String> lines = Files.lines(Paths.get("data.txt"));

        // 使用 IntStream/LongStream/DoubleStream 处理数值范围
        // 前闭后开 [start, end)
        long count = IntStream.range(1, 100)  // 1 到 99
                              .filter(n -> n % 7 == 0)  // 能被7整除
                              .count();

        System.out.println("1-99 中能被7整除的数有 " + count + " 个");

        // rangeClosed 是闭区间 [start, end]
        long count2 = IntStream.rangeClosed(1, 100)  // 1 到 100
                               .filter(n -> n % 7 == 0)
                               .count();

        System.out.println("1-100 中能被7整除的数有 " + count2 + " 个");
    }
}
```

---

## 25.3 中间操作

中间操作（Intermediate Operations）就是流水线上的一道道工序，它们返回新的 Stream，可以链式调用。

> **重要概念：** 中间操作是**惰性的**，不会立即执行。只有碰到终端操作，整条流水线才会启动。

### 25.3.1 过滤 filter()

根据条件筛选元素，就像筛子过滤沙子。

```java
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

public class FilterDemo {
    public static void main(String[] args) {
        List<String> languages = Arrays.asList(
            "Java", "Python", "JavaScript", "C", "C++", "Rust", "Go", "Kotlin"
        );

        // 筛选名字长度大于4的语言
        List<String> longNames = languages.stream()
                                          .filter(lang -> lang.length() > 4)
                                          .collect(Collectors.toList());

        System.out.println("名字长度大于4的语言: " + longNames);

        // 筛选包含字母"a"的语言
        List<String> containA = languages.stream()
                                        .filter(lang -> lang.toLowerCase().contains("a"))
                                        .collect(Collectors.toList());

        System.out.println("包含字母a的语言: " + containA);
    }
}
```

### 25.3.2 映射 map()

把每个元素"变换"成另一个值，相当于函数式编程里的**映射**。

```java
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

public class MapDemo {
    public static void main(String[] args) {
        List<String> names = Arrays.asList("alice", "bob", "charlie", "david");

        // 全部转为大写
        List<String> upperNames = names.stream()
                                       .map(String::toUpperCase)
                                       .collect(Collectors.toList());

        System.out.println("大写: " + upperNames);

        // 提取名字长度
        List<Integer> lengths = names.stream()
                                      .map(String::length)
                                      .collect(Collectors.toList());

        System.out.println("名字长度: " + lengths);

        // 复杂映射：把数字列表转为它们的平方
        List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5);
        List<Integer> squares = numbers.stream()
                                        .map(n -> n * n)
                                        .collect(Collectors.toList());

        System.out.println("平方: " + squares);
    }
}
```

### 25.3.3 扁平化映射 flatMap()

这个有点绕——flatMap = map + flatten。当你的映射结果本身又是 Stream 时，flatMap 会把它们"压平"成一个 Stream。

```java
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

public class FlatMapDemo {
    public static void main(String[] args) {
        List<String> sentences = Arrays.asList(
            "Hello world",
            "Java Stream API",
            "flatMap is powerful"
        );

        // 用 map 分割单词（每个句子变成一个 String[]）
        // 结果是 Stream<String[]>，而不是 Stream<String>
        System.out.println("=== map 的结果 ===");
        sentences.stream()
                 .map(sentence -> sentence.split(" "))
                 .forEach(arr -> System.out.println("数组: " + Arrays.toString(arr)));

        // 用 flatMap 分割单词（所有单词压平到一个 Stream）
        System.out.println("\n=== flatMap 的结果 ===");
        List<String> words = sentences.stream()
                                      .flatMap(sentence -> Arrays.stream(sentence.split(" ")))
                                      .collect(Collectors.toList());

        System.out.println("所有单词: " + words);

        // 去重
        List<String> uniqueWords = sentences.stream()
                                           .flatMap(sentence -> Arrays.stream(sentence.split(" ")))
                                           .distinct()
                                           .collect(Collectors.toList());

        System.out.println("去重后: " + uniqueWords);
    }
}
```

### 25.3.4 排序 sorted()

对元素进行排序。

```java
import java.util.Arrays;
import java.util.Comparator;
import java.util.List;
import java.util.stream.Collectors;

public class SortedDemo {
    public static void main(String[] args) {
        List<String> fruits = Arrays.asList("Banana", "Apple", "Cherry", "Date");

        // 自然顺序排序（需实现 Comparable）
        List<String> sorted1 = fruits.stream()
                                     .sorted()
                                     .collect(Collectors.toList());
        System.out.println("自然排序: " + sorted1);

        // 逆序
        List<String> sorted2 = fruits.stream()
                                     .sorted(Comparator.reverseOrder())
                                     .collect(Collectors.toList());
        System.out.println("逆序: " + sorted2);

        // 按长度排序
        List<String> byLength = fruits.stream()
                                      .sorted(Comparator.comparingInt(String::length))
                                      .collect(Collectors.toList());
        System.out.println("按长度排序: " + byLength);

        // 按长度倒序，长度相同按字母顺序
        List<String> complex = fruits.stream()
                                     .sorted(Comparator
                                         .comparingInt(String::length)
                                         .reversed()
                                         .thenComparing(Comparator.naturalOrder()))
                                     .collect(Collectors.toList());
        System.out.println("复杂排序: " + complex);
    }
}
```

### 25.3.5 去重 distinct()

去除重复元素，使用 `equals()` 判断相等性。

```java
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

public class DistinctDemo {
    public static void main(String[] args) {
        List<Integer> numbers = Arrays.asList(1, 2, 2, 3, 3, 3, 4, 4, 4, 4);

        List<Integer> distinct = numbers.stream()
                                        .distinct()
                                        .collect(Collectors.toList());

        System.out.println("去重前: " + numbers);
        System.out.println("去重后: " + distinct);

        // 对对象去重需要正确重写 equals 和 hashCode
        List<String> words = Arrays.asList("apple", "Apple", "APPLE", "banana");
        List<String> caseInsensitiveDistinct = words.stream()
                                                     .map(String::toLowerCase)
                                                     .distinct()
                                                     .collect(Collectors.toList());
        System.out.println("忽略大小写去重: " + caseInsensitiveDistinct);
    }
}
```

### 25.3.6 跳过和限制 limit() / skip()

```java
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

public class LimitSkipDemo {
    public static void main(String[] args) {
        List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5, 6, 7, 8, 9, 10);

        // 取前5个
        List<Integer> first5 = numbers.stream()
                                      .limit(5)
                                      .collect(Collectors.toList());
        System.out.println("前5个: " + first5);

        // 跳过前3个
        List<Integer> skip3 = numbers.stream()
                                     .skip(3)
                                     .collect(Collectors.toList());
        System.out.println("跳过前3个: " + skip3);

        // 跳过前2个，取3个（分页常用）
        List<Integer> page2 = numbers.stream()
                                     .skip(2)
                                     .limit(3)
                                     .collect(Collectors.toList());
        System.out.println("第2页（跳过2个取3个）: " + page2);

        // 找出第3大的数
        Integer thirdMax = numbers.stream()
                                  .sorted(Integer::compareTo)
                                  .skip(2)
                                  .findFirst()
                                  .orElse(null);
        System.out.println("第3大的数: " + thirdMax);
    }
}
```

### 25.3.7 peek() 调试神器

peek() 不会改变元素，它只是在每个元素经过时"偷看一眼"，非常适合调试。

```java
import java.util.Arrays;
import java.util.List;

public class PeekDemo {
    public static void main(String[] args) {
        List<String> names = Arrays.asList("Alice", "Bob", "Charlie", "Diana");

        // 在流水线中查看每个阶段的中间结果
        names.stream()
             .peek(name -> System.out.println("原始: " + name))
             .map(String::toUpperCase)
             .peek(name -> System.out.println("大写后: " + name))
             .filter(name -> name.length() > 4)
             .peek(name -> System.out.println("过滤后: " + name))
             .forEach(name -> {});
    }
}
```

---

## 25.4 终端操作

终端操作（Terminal Operations）是 Stream 流水线的终点，它们会触发整个流水线的执行，并返回最终结果。

### 25.4.1 遍历 forEach()

最常用的终端操作，对每个元素执行指定动作。

```java
import java.util.Arrays;
import java.util.List;

public class ForEachDemo {
    public static void main(String[] args) {
        List<String> tasks = Arrays.asList("洗碗", "扫地", "拖地", "倒垃圾");

        // 传统 forEach
        tasks.forEach(task -> System.out.println("完成任务: " + task));

        // 方法引用版本
        System.out.println("\n使用方法引用:");
        tasks.forEach(System.out::println);

        // 注意：forEach 是无序的，对于并行流不保证顺序
        System.out.println("\n并行流 forEach（无序保证）:");
        tasks.parallelStream()
             .forEach(task -> System.out.println("处理: " + task));
    }
}
```

### 25.4.2 收集到集合 collect()

最灵活的终端操作，把结果收集成 List、Set、Map 等。

```java
import java.util.*;
import java.util.stream.Collectors;
import java.util.function.Supplier;

public class CollectDemo {
    public static void main(String[] args) {
        List<String> languages = Arrays.asList("Java", "Python", "JavaScript", "C", "Java");

        // 收集为 List
        List<String> list = languages.stream()
                                     .filter(l -> l.startsWith("J"))
                                     .collect(Collectors.toList());
        System.out.println("List: " + list);

        // 收集为 Set（自动去重）
        Set<String> set = languages.stream()
                                   .filter(l -> l.startsWith("J"))
                                   .collect(Collectors.toSet());
        System.out.println("Set: " + set);

        // 收集为指定集合（如 LinkedList）
        LinkedList<String> linkedList = languages.stream()
                                                  .collect(Collectors.toCollection(LinkedList::new));
        System.out.println("LinkedList: " + linkedList);

        // 收集为 Map（需要两个函数：keyMapper 和 valueMapper）
        List<Person> people = Arrays.asList(
            new Person("Alice", 25),
            new Person("Bob", 30),
            new Person("Charlie", 25)
        );

        Map<String, Integer> nameToAge = people.stream()
                                               .collect(Collectors.toMap(
                                                   Person::getName,
                                                   Person::getAge
                                               ));
        System.out.println("Map: " + nameToAge);

        // 分组收集
        Map<Integer, List<Person>> byAge = people.stream()
                                                  .collect(Collectors.groupingBy(Person::getAge));
        System.out.println("按年龄分组: " + byAge);

        // 统计（counting, summing, averaging）
        long count = languages.stream().count();
        System.out.println("总数: " + count);

        Double average = people.stream()
                               .collect(Collectors.averagingInt(Person::getAge));
        System.out.println("平均年龄: " + average);
    }
}

// 辅助类
class Person {
    private String name;
    private int age;

    public Person(String name, int age) {
        this.name = name;
        this.age = age;
    }

    public String getName() { return name; }
    public int getAge() { return age; }

    @Override
    public String toString() {
        return name + "(" + age + ")";
    }
}
```

### 25.4.3 匹配操作 match()

返回一个 boolean，非常适合"是否存在"、"是否全部满足"等判断。

```java
import java.util.Arrays;
import java.util.List;

public class MatchDemo {
    public static void main(String[] args) {
        List<Integer> numbers = Arrays.asList(2, 4, 6, 8, 10);

        // anyMatch: 是否有任意一个满足条件
        boolean hasOdd = numbers.stream()
                                .anyMatch(n -> n % 2 != 0);
        System.out.println("包含奇数? " + hasOdd);  // false

        // allMatch: 是否全部满足条件
        boolean allEven = numbers.stream()
                                 .allMatch(n -> n % 2 == 0);
        System.out.println("全是偶数? " + allEven);  // true

        // noneMatch: 是否全部不满足条件
        boolean noneOdd = numbers.stream()
                                 .noneMatch(n -> n % 2 != 0);
        System.out.println("没有奇数? " + noneOdd);  // true

        // 实战应用：验证用户输入
        List<String> usernames = Arrays.asList("alice", "bob", "charlie");
        boolean allValid = usernames.stream()
                                    .allMatch(name -> name.length() >= 3 && name.matches("\\w+"));
        System.out.println("所有用户名都合法? " + allValid);
    }
}
```

### 25.4.4 查找操作 find()

从 Stream 中找到满足条件的元素。

```java
import java.util.Arrays;
import java.util.List;
import java.util.Optional;

public class FindDemo {
    public static void main(String[] args) {
        List<String> names = Arrays.asList("Alice", "Bob", "Charlie", "Diana", "Eve");

        // findAny: 找到任意一个（并行流时可能更快）
        Optional<String> any = names.stream()
                                     .filter(n -> n.length() > 4)
                                     .findAny();
        System.out.println("任意一个长度>4的: " + any.orElse("没有"));

        // findFirst: 找到第一个（保证顺序）
        Optional<String> first = names.stream()
                                      .filter(n -> n.length() > 4)
                                      .findFirst();
        System.out.println("第一个长度>4的: " + first.orElse("没有"));

        // 配合其他操作
        Optional<Integer> firstEven = Arrays.asList(1, 3, 5, 2, 4)
                                            .stream()
                                            .filter(n -> n % 2 == 0)
                                            .findFirst();
        System.out.println("第一个偶数: " + firstEven.orElse(-1));

        // Optional 的链式操作
        String result = names.stream()
                             .filter(n -> n.startsWith("Z"))
                             .findFirst()
                             .map(String::toUpperCase)
                             .orElse("未找到");
        System.out.println("查找结果: " + result);
    }
}
```

### 25.4.5 聚合操作 reduce()

把 Stream 中的元素"聚合"成一个值，是函数式编程的核心操作。

```java
import java.util.Arrays;
import java.util.List;
import java.util.Optional;

public class ReduceDemo {
    public static void main(String[] args) {
        List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5);

        // reduce(BinaryOperator<T> accumulator)
        // 求和
        Optional<Integer> sum = numbers.stream()
                                        .reduce((a, b) -> a + b);
        System.out.println("总和: " + sum.orElse(0));

        // reduce(T identity, BinaryOperator<T> accumulator)
        // 带初始值的求和
        int sumWithIdentity = numbers.stream()
                                      .reduce(0, Integer::sum);
        System.out.println("带初始值的总和: " + sumWithIdentity);

        // 求乘积
        int product = numbers.stream()
                             .reduce(1, (a, b) -> a * b);
        System.out.println("乘积: " + product);

        // 找出最长名字
        List<String> names = Arrays.asList("Alice", "Bob", "Charlie", "Diana");
        String longest = names.stream()
                              .reduce("", (a, b) -> a.length() > b.length() ? a : b);
        System.out.println("最长名字: " + longest);

        // 求最大值/最小值
        int max = numbers.stream()
                         .reduce(Integer.MIN_VALUE, Integer::max);
        int min = numbers.stream()
                         .reduce(Integer.MAX_VALUE, Integer::min);
        System.out.println("最大值: " + max + ", 最小值: " + min);

        // 字符串连接
        String joined = names.stream()
                             .reduce("", (a, b) -> a + ", " + b);
        System.out.println("连接: " + joined.substring(2));  // 去掉开头的 ", "
    }
}
```

### 25.4.6 数值统计 summaryStatistics()

对于数值型 Stream，可以一次性获取多种统计信息。

```java
import java.util.IntSummaryStatistics;
import java.util.List;

public class SummaryStatisticsDemo {
    public static void main(String[] args) {
        List<Integer> ages = List.of(25, 30, 35, 28, 32, 40, 22, 28, 35);

        IntSummaryStatistics stats = ages.stream()
                                         .mapToInt(Integer::intValue)
                                         .summaryStatistics();

        System.out.println("=== 年龄统计 ===");
        System.out.println("人数: " + stats.getCount());
        System.out.println("总和: " + stats.getSum());
        System.out.println("平均: " + String.format("%.2f", stats.getAverage()));
        System.out.println("最小: " + stats.getMin());
        System.out.println("最大: " + stats.getMax());

        // 或者用 LongSummaryStatistics 和 DoubleSummaryStatistics
        System.out.println("\n=== toString ===");
        System.out.println(stats.toString());
    }
}
```

---

## 25.5 并行流 ParallelStream

终于到了重头戏！ParallelStream 是 Stream 的多线程版本，让你的数据处理速度飙升。

> **ParallelStream 是什么？** 简单说就是把一个大任务拆成多个小任务，同时在多个CPU核心上执行，最后汇总结果。想象1000个快递让你一个人分拣要1小时，但如果你叫10个同事一起干，10分钟就搞定了。

### 25.5.1 创建并行流

两种方式：从集合创建或转换现有流。

```java
import java.util.List;
import java.util.stream.Stream;

public class CreateParallelStream {
    public static void main(String[] args) {
        List<String> items = List.of("A", "B", "C", "D", "E");

        // 方式1：从集合直接创建
        items.parallelStream()
             .forEach(item -> System.out.println("处理: " + item + " -> 线程: " + Thread.currentThread().getName()));

        System.out.println("\n--- 分割线 ---\n");

        // 方式2：从普通流转换
        Stream<String> sequential = items.stream();
        sequential.parallel()
                   .forEach(item -> System.out.println("处理: " + item + " -> 线程: " + Thread.currentThread().getName()));

        // 检查是否是并行流
        boolean isParallel = items.parallelStream().isParallel();
        System.out.println("\n是并行流? " + isParallel);
    }
}
```

### 25.5.2 性能对比

来一个直观的性能测试。

```java
import java.util.LongSummaryStatistics;
import java.util.stream.IntStream;

public class ParallelPerformanceDemo {
    public static void main(String[] args) {
        int limit = 10_000_000;  // 一千万

        // 顺序流计算
        long startSeq = System.currentTimeMillis();
        long sumSeq = IntStream.range(1, limit)
                               .asLongStream()
                               .sum();
        long timeSeq = System.currentTimeMillis() - startSeq;

        // 并行流计算
        long startPar = System.currentTimeMillis();
        long sumPar = IntStream.range(1, limit)
                               .parallel()
                               .asLongStream()
                               .sum();
        long timePar = System.currentTimeMillis() - startPar;

        System.out.println("=== 计算 1 到 " + limit + " 的和 ===");
        System.out.println("顺序流结果: " + sumSeq + ", 耗时: " + timeSeq + " ms");
        System.out.println("并行流结果: " + sumPar + ", 耗时: " + timePar + " ms");
        System.out.println("加速比: " + String.format("%.2f", (double) timeSeq / timePar) + "x");

        // 统计操作
        System.out.println("\n=== 统计操作 ===");
        long startStats = System.currentTimeMillis();
        IntSummaryStatistics stats = IntStream.range(1, limit)
                                              .parallel()
                                              .summaryStatistics();
        System.out.println("并行统计耗时: " + (System.currentTimeMillis() - startStats) + " ms");
        System.out.println("统计结果: count=" + stats.getCount() + ", sum=" + stats.getSum());
    }
}
```

### 25.5.3 并行流的注意事项

并行流虽然强大，但不是万能的。以下情况要慎用：

```java
import java.util.ArrayList;
import java.util.List;

public class ParallelCaveats {
    public static void main(String[] args) {
        // ⚠️ 注意事项1：避免使用可变变量
        // ❌ 错误示例：并行流中修改共享变量
        List<Integer> numbers = List.of(1, 2, 3, 4, 5);
        int[] sum = {0};  // 可变变量，在并行流中是危险的！

        // numbers.parallelStream().forEach(n -> sum[0] += n);  // 不要这样做！

        // ✓ 正确做法：使用 reduce 或 atomic
        int correctSum = numbers.parallelStream()
                                .reduce(0, Integer::sum);
        System.out.println("正确求和: " + correctSum);

        // ⚠️ 注意事项2：顺序敏感的操作可能出问题
        // findFirst 是有序的，parallelStream 可能比 stream 慢
        // 如果不关心顺序，用 findAny()

        // ⚠️ 注意事项3：不要用 ArrayList 创建并行流（拆分效率低）
        // 建议用 LinkedList 或 Arrays.asList()

        // ⚠️ 注意事项4：小数据量不要用并行流
        // 创建线程池的开销可能比计算本身还大

        // ⚠️ 注意事项5：boxed 类型流的性能问题
        // IntStream, LongStream 比 Stream<Integer> 快很多
    }
}
```

### 25.5.4 自定义线程池

默认情况下，并行流使用公共的 ForkJoinPool.commonPool()。你可以自定义线程池来满足特殊需求。

```java
import java.util.concurrent.ForkJoinPool;
import java.util.concurrent.ForkJoinTask;
import java.util.stream.LongStream;
import java.util.stream.LongUnaryOperator;

public class CustomThreadPoolDemo {
    public static void main(String[] args) {
        // 创建自定义线程池（4个线程）
        ForkJoinPool customPool = new ForkJoinPool(4);

        try {
            // 在自定义线程池中执行并行计算
            LongUnaryOperator task = n -> LongStream.range(1, n)
                                                    .parallel()
                                                    .sum();

            // 使用 submit 而不是 invoke
            ForkJoinTask<Long> future = customPool.submit(() -> task.applyAsLong(10_000_000L));

            Long result = future.get();
            System.out.println("自定义线程池计算结果: " + result);

        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            customPool.shutdown();
        }

        // 使用系统属性配置公共线程池的并行度
        // System.setProperty("java.util.concurrent.ForkJoinPool.common.parallelism", "8");
    }
}
```

### 25.5.5 并行流的最佳实践

```java
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;
import java.util.stream.IntStream;

public class ParallelBestPractices {
    public static void main(String[] args) {
        // ✅ 最佳实践1：对于数值计算，使用专门的原始类型流
        long sum = IntStream.range(1, 1_000_000)
                           .parallel()
                           .asLongStream()
                           .sum();

        // ✅ 最佳实践2：确保操作是无状态的、不依赖外部可变状态
        List<String> words = List.of("hello", "world", "java", "stream", "parallel");
        List<String> uppercased = words.parallelStream()
                                       .map(String::toUpperCase)  // 无副作用的纯函数
                                       .collect(Collectors.toList());

        // ✅ 最佳实践3：考虑使用 Collectors.groupingByConcurrent
        // 它是线程安全的分组收集器
        List<Map<String, Object>> data = List.of(
            Map.of("category", "A", "value", 1),
            Map.of("category", "B", "value", 2),
            Map.of("category", "A", "value", 3)
        );

        Map<String, List<Map<String, Object>>> grouped = data.parallelStream()
                                                                .collect(Collectors.groupingByConcurrent(
                                                                    m -> m.get("category").toString()
                                                                ));

        System.out.println("并发分组结果: " + grouped);

        // ✅ 最佳实践4：判断是否值得并行
        System.out.println("\n=== 判断是否值得并行 ===");

        // 小数据量
        long smallStart = System.currentTimeMillis();
        IntStream.range(1, 100).parallel().sum();
        System.out.println("100个元素并行耗时: " + (System.currentTimeMillis() - smallStart) + " ms");

        // 大数据量
        long largeStart = System.currentTimeMillis();
        IntStream.range(1, 10_000_000).parallel().sum();
        System.out.println("1000万元素并行耗时: " + (System.currentTimeMillis() - largeStart) + " ms");
    }
}
```

---

## 本章小结

本章我们深入学习了 Java Stream API，这是 Java 8 引入的革命性特性：

| 概念 | 说明 |
|------|------|
| **Stream 的三个特性** | 不存储数据、不修改源数据、惰性执行 |
| **创建 Stream** | 从集合、数组、Stream.of()、iterate()、generate() 等方式创建 |
| **中间操作** | filter、map、flatMap、sorted、distinct、limit、skip、peek 等 |
| **终端操作** | forEach、collect、match、find、reduce、summaryStatistics 等 |
| **并行流** | ParallelStream 让数据处理利用多核 CPU，通过 parallelStream() 或 parallel() 创建 |

**核心记忆点：**
- Stream 是数据处理流水线，本身不存储数据
- 中间操作返回新 Stream，是惰性的
- 终端操作触发实际执行
- 并行流适合大数据量、无状态操作的场景
- 小数据量或涉及状态修改时，慎用并行流

> 学习 Stream 的最好方式就是多写多练。下次处理集合数据时，试着先用传统方式实现，再用 Stream 重构，感受一下代码从"苦力活"变成"优雅艺术"的过程吧！
