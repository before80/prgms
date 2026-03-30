+++
title = "第23章 泛型——类型的保险箱"
weight = 230
date = "2026-03-30T14:33:56.905+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++
# 第二十三章 泛型——类型的保险箱

> "给你一个盒子，你不知道里面装的是什么——这叫`Object`。
> 给你一个贴了标签的盒子，你一眼就知道里面装的是什么——这叫泛型。"
>
> 泛型，是 Java 给类型系统买的一份保险。

---

## 23.1 为什么需要泛型？

### 故事的起源：没有泛型的日子

在 Java 5 之前，集合（Collection）是这样用的：

```java
// 模拟 Java 5 之前的代码
public class OldStyleBox {
    private Object value;

    public OldStyleBox(Object value) {
        this.value = value;
    }

    public Object getValue() {
        return value;
    }
}

// 使用时
OldStyleBox box = new OldStyleBox("Hello");
// 取出来用，得强制转型
String s = (String) box.getValue();
```

这段代码看起来没什么问题，直到有一天：

```java
OldStyleBox box = new OldStyleBox(123);
// 我以为取出来是 String，实际情况是...
String s = (String) box.getValue(); // 编译通过，运行时炸了！
// 抛出 ClassCastException: java.lang.Integer cannot be cast to java.lang.String
```

> 💥 **ClassCastException** — 编译时笑嘻嘻，运行时哭唧唧。

问题出在哪？编译器在强制转型那一刻完全信任了你，而你自己骗了自己。类型检查形同虚设。

### 泛型的救赎

Java 5 引入泛型，革命开始了：

```java
// 泛型版本
public class GenericBox<T> {
    private T value;

    public GenericBox(T value) {
        this.value = value;
    }

    public T getValue() {
        return value;
    }
}

// 使用时
GenericBox<String> box = new GenericBox<>("Hello");
String s = box.getValue(); // 不需要转型！直接就是 String！
```

如果你敢这么写：

```java
GenericBox<Integer> box = new GenericBox<>(123);
String s = box.getValue(); // 编译错误！Integer 不能赋值给 String
```

编译器在**编译时**就把你拦下来了，根本不给 ClassCastException 上场的机会。

### 泛型的三大好处

| 好处 | 说明 |
|------|------|
| **类型安全** | 编译器检查类型，消灭 ClassCastException |
| **消除强制转型** | `getValue()` 直接返回目标类型，不用 cast |
| **代码复用** | 一套泛型类/方法，可以支持所有类型 |

简单来说：**泛型把类型检查从"事后诸葛亮"变成了"事前保安"**。

---

## 23.2 泛型类

### 什么是泛型类？

泛型类就是**带有类型参数（Type Parameter）**的普通类。类型参数用尖括号 `<T>` 声明，放在类名后面。

```java
/**
 * 泛型类的基本语法
 * T 是类型参数（Type Parameter），名字可以随便起，
 * 但约定俗成有：T（Type）、K/V（Key/Value）、E（Element）、R（Return）
 */
public class Pair<K, V> {
    private K key;
    private V value;

    public Pair(K key, V value) {
        this.key = key;
        this.value = value;
    }

    public K getKey() { return key; }
    public V getValue() { return value; }

    @Override
    public String toString() {
        return "Pair{" + key + "=" + value + "}";
    }
}
```

使用泛型类时，在尖括号里指定具体的类型：

```java
public class Main {
    public static void main(String[] args) {
        // K=String, V=Integer
        Pair<String, Integer> ageMap = new Pair<>("Alice", 30);
        System.out.println(ageMap); // Pair{Alice=30}

        // K=String, V=String
        Pair<String, String> config = new Pair<>("host", "localhost");
        System.out.println(config); // Pair{host=localhost}

        // 编译器自动推断类型（钻石语法）
        Pair<String, Double> rate = new Pair<>("USD/EUR", 0.92);
        System.out.println(rate); // Pair{USD/EUR=0.92}
    }
}
```

> 💡 **钻石语法（Diamond Syntax）**：Java 7 开始，`new Pair<>("...", 123)` 的 `<>` 可以空着，编译器会自动推断。

### 多个类型参数

泛型类可以有多个类型参数：

```java
public class Triple<A, B, C> {
    private A first;
    private B second;
    private C third;

    public Triple(A first, B second, C third) {
        this.first = first;
        this.second = second;
        this.third = third;
    }

    public A getFirst() { return first; }
    public B getSecond() { return second; }
    public C getThird() { return third; }

    @Override
    public String toString() {
        return "(" + first + ", " + second + ", " + third + ")";
    }
}

// 使用
Triple<String, Integer, Boolean> flags = new Triple<>("debug", 1, true);
System.out.println(flags); // (debug, 1, true)
```

### 泛型类的继承

泛型类可以继承泛型类，也可以被非泛型类继承：

```java
// 父类
public class GenericParent<T> {
    protected T data;
    public T getData() { return data; }
}

// 子类保留泛型
class StringGenericChild<T> extends GenericParent<T> {
    @Override
    public String toString() {
        return "StringGenericChild{data=" + data + "}";
    }
}

// 子类具体化泛型
class StringSpecificChild extends GenericParent<String> {
    // data 的类型被固定为 String
}

// 子类新增类型参数
class ExtendedGenericChild<T, V> extends GenericParent<T> {
    private V extra;
    public ExtendedGenericChild(T data, V extra) {
        this.data = data;
        this.extra = extra;
    }
}
```

---

## 23.3 泛型接口

### 基本语法

泛型接口和泛型类的语法几乎一样，只是关键字换成了 `interface`：

```java
/**
 * 泛型接口：Comparable 接口被重新设计为泛型版本
 * 实现了泛型化的 Comparable，可以指定比较对象的类型
 */
public interface Comparable<T> {
    int compareTo(T other);
}

/**
 * 泛型容器接口
 */
public interface Container<T> {
    void add(T item);
    T get(int index);
    int size();
    boolean isEmpty();
}

/**
 * 实现泛型接口时，可以选择：
 * 1. 保持泛型
 * 2. 具体化类型
 */
public class StringList implements Container<String> {
    private String[] items = new String[100];
    private int count = 0;

    @Override
    public void add(String item) {
        if (count < items.length) {
            items[count++] = item;
        }
    }

    @Override
    public String get(int index) {
        if (index >= 0 && index < count) {
            return items[index];
        }
        throw new IndexOutOfBoundsException("索引: " + index);
    }

    @Override
    public int size() { return count; }

    @Override
    public boolean isEmpty() { return count == 0; }
}
```

```java
public class Main {
    public static void main(String[] args) {
        StringList list = new StringList();
        list.add("Java");
        list.add("Python");
        list.add("Go");

        System.out.println("第一个语言: " + list.get(0)); // Java
        System.out.println("总数: " + list.size()); // 3

        // 尝试添加非 String？编译器直接报错
        // list.add(123); // 编译错误！
    }
}
```

### 泛型接口的多种实现方式

```java
// 泛型接口
public interface Transformer<T, R> {
    R transform(T input);
}

// 实现方式一：保持泛型
class ArrayToList<T> implements Transformer<T, java.util.List<T>> {
    @Override
    public java.util.List<T> transform(T input) {
        return java.util.List.of(input);
    }
}

// 实现方式二：具体化类型
class StringToUpperCase implements Transformer<String, String> {
    @Override
    public String transform(String input) {
        return input.toUpperCase();
    }
}
```

---

## 23.4 泛型方法

### 什么是泛型方法？

泛型方法是指**在方法返回类型前面声明了类型参数的方法**。它可以是静态的，也可以是非静态的，甚至可以在普通类里定义。

```java
public class Algorithm {

    /**
     * 泛型方法：交换数组中两个位置的元素
     * <T> 是方法类型参数声明，必须在方法返回类型之前
     */
    public static <T> void swap(T[] array, int i, int j) {
        if (i < 0 || j < 0 || i >= array.length || j >= array.length) {
            throw new IllegalArgumentException("索引越界");
        }
        T temp = array[i];
        array[i] = array[j];
        array[j] = temp;
    }

    /**
     * 泛型方法：找出数组中的最大值
     * Comparable<T> 是类型参数约束，下一节会详细讲
     */
    public static <T extends Comparable<T>> T findMax(T[] array) {
        if (array == null || array.length == 0) {
            throw new IllegalArgumentException("数组不能为空");
        }
        T max = array[0];
        for (int i = 1; i < array.length; i++) {
            if (array[i].compareTo(max) > 0) {
                max = array[i];
            }
        }
        return max;
    }

    /**
     * 泛型方法：把两个对象装进 Pair
     */
    public static <K, V> Pair<K, V> makePair(K key, V value) {
        return new Pair<>(key, value);
    }
}
```

```java
public class Main {
    public static void main(String[] args) {
        // 测试 swap
        String[] languages = {"Java", "Python", "Go", "Rust"};
        Algorithm.swap(languages, 0, 2);
        System.out.println("交换后: " + java.util.Arrays.toString(languages));
        // [Go, Python, Java, Rust]

        // 测试 findMax
        Integer[] numbers = {3, 9, 1, 4, 7, 2, 8};
        Integer max = Algorithm.findMax(numbers);
        System.out.println("最大值: " + max); // 9

        // 测试 makePair
        Pair<String, Integer> pair = Algorithm.makePair("score", 100);
        System.out.println(pair); // Pair{score=100}
    }
}
```

### 泛型方法和泛型类的区别

```java
public class MyClass<T> {
    // 这是泛型类的方法，不是泛型方法！
    // T 来自类的类型参数
    public T doSomething(T input) {
        return input;
    }

    // 这才是真正的泛型方法！方法自己声明了 <V>
    public <V> V convert(T input, Class<V> clazz) throws Exception {
        return clazz.getDeclaredConstructor().newInstance();
    }
}
```

> 🎯 **判断技巧**：看方法的返回类型前面有没有 `<Something>`。有，就是泛型方法；没有，就是用类的类型参数的普通方法。

---

## 23.5 类型参数约束

### 上界 bounded wildcard —— `extends`

有时候，你需要限制泛型允许的类型范围。比如"只要是数字就行"或"只要实现了某个接口就行"。这时就用 `extends` 关键字设置**上界（Upper Bound）**。

```java
/**
 * 计算所有数字类型的通用计算器
 * <T extends Number> 表示 T 必须是 Number 或 Number 的子类
 * 这样 T 就一定有 intValue()、doubleValue() 等方法
 */
public class NumberCalculator<T extends Number> {
    private T[] numbers;

    @SafeVarargs
    public NumberCalculator(T... numbers) {
        this.numbers = numbers;
    }

    /**
     * 计算总和（自动转换为 double）
     */
    public double sum() {
        double total = 0.0;
        for (T n : numbers) {
            total += n.doubleValue(); // 安全的，因为 T 一定是 Number 的子类
        }
        return total;
    }

    /**
     * 计算平均值
     */
    public double average() {
        return numbers.length == 0 ? 0 : sum() / numbers.length;
    }
}
```

```java
public class Main {
    public static void main(String[] args) {
        NumberCalculator<Integer> intCalc = new NumberCalculator<>(1, 2, 3, 4, 5);
        System.out.println("整数总和: " + intCalc.sum());       // 15.0
        System.out.println("整数平均: " + intCalc.average());    // 3.0

        NumberCalculator<Double> doubleCalc = new NumberCalculator<>(1.5, 2.5, 3.0);
        System.out.println("Double总和: " + doubleCalc.sum());  // 7.0
        System.out.println("Double平均: " + doubleCalc.average()); // 2.333...

        // NumberCalculator<String> strCalc = new NumberCalculator<>("a"); // 编译错误！
        // String 不是 Number 的子类，不满足 <T extends Number> 约束
    }
}
```

### 多重约束

Java 也支持多重约束，用 `&` 连接：

```java
/**
 * T 必须同时实现 Serializable 和 Comparable 接口
 * 这在设计框架类时非常有用
 */
public static <T extends Serializable & Comparable<T>> void process(T item) {
    // T 一定可以序列化和比较
}
```

> ⚠️ 注意：多重约束中，**如果有类参与约束，必须放在第一位**。因为 Java 不允许多继承，但接口可以多继承，所以用 `&` 连接时，类只能出现一次且必须在最前。

### 下界约束 —— `super`（在通配符中详细讲）

下界约束用在通配符中 `<T super SomeType>`，留待 23.6 节。

---

## 23.6 泛型通配符

### 通配符 `?` —— 不知道是什么类型

通配符 `?` 表示"我不知道是什么类型"（或者"我不在乎是什么类型"）。它有三种形态：

| 形态 | 名称 | 含义 | 用途 |
|------|------|------|------|
| `<?>` | 无界通配符 | 不知道什么类型 | 只读操作 |
| `<? extends T>` | 上界通配符 | 不知道具体类型，但知道是 T 或 T 的子类 | **生产者**（读取数据） |
| `<? super T>` | 下界通配符 | 不知道具体类型，但知道是 T 或 T 的父类 | **消费者**（写入数据） |

### PECS 原则：Producer Extends, Consumer Super

这是 Java 泛型中最著名的原则之一。

```java
import java.util.ArrayList;
import java.util.List;

/**
 * PECS: Producer Extends, Consumer Super
 *
 * 如果你的泛型参数是用来**生产（读取）**数据的，用 extends
 * 如果你的泛型参数是用来**消费（写入）**数据的，用 super
 */
public class WildcardDemo {

    // 生产者：读取数据，只关心能读出什么
    public static double sumOfAll(List<? extends Number> numbers) {
        double total = 0.0;
        for (Number n : numbers) {
            total += n.doubleValue(); // 可以安全读取
        }
        // numbers.add(1); // 编译错误！不能写入（不知道具体类型）
        return total;
    }

    // 消费者：写入数据
    public static void addNumbers(List<? super Integer> list) {
        // 可以安全写入 Integer 或其子类
        list.add(1);
        list.add(2);
        list.add(3);
        // Integer i = list.get(0); // 编译错误！只能当 Object 取出来
    }

    public static void copy(List<? extends Object> src, List<? super Object> dest) {
        for (Object item : src) {
            dest.add(item); // 写入 OK
        }
    }
}
```

```java
public class Main {
    public static void main(String[] args) {
        // extends 用法
        List<Integer> integers = List.of(1, 2, 3);
        List<Double> doubles = List.of(1.1, 2.2, 3.3);

        System.out.println("整数和: " + WildcardDemo.sumOfAll(integers)); // 6.0
        System.out.println("Double和: " + WildcardDemo.sumOfAll(doubles)); // 6.6

        // super 用法
        List<Number> numbers = new ArrayList<>();
        List<Object> objects = new ArrayList<>();
        WildcardDemo.addNumbers(numbers);
        WildcardDemo.addNumbers(objects);
        System.out.println("Numbers: " + numbers); // [1, 2, 3]
        System.out.println("Objects: " + objects); // [1, 2, 3]
    }
}
```

### `<?>` 无界通配符

当你既不需要读也不需要写具体类型时：

```java
/**
 * 打印列表中的元素（只读）
 * List<?> 可以接受 List<String>、List<Integer> 等任何类型
 */
public static void printList(List<?> list) {
    for (Object item : list) {
        System.out.println(item);
    }
    // list.add("something"); // 编译错误！不能写入
}
```

### 为什么 `List<Object>` 和 `List<?>` 不一样？

这是一个经典面试题：

```java
List<Object> objectList = new ArrayList<String>(); // 编译错误！
List<?>  wildcardList  = new ArrayList<String>(); // 编译通过！
```

`List<Object>` 看起来更"宽"，为什么反而不允许？

> 因为如果允许 `List<Object> = new ArrayList<String>()`，那么就可以往里面 `add(new Integer(123))`，但底层其实是 `ArrayList<String>`，运行时就会乱套。**泛型的设计初衷就是类型安全**，所以这种"看似合理"的赋值被禁止了。

`List<?>` 则明确表示"我什么都不知道"，所以只能读（返回 Object），不能写（编译器也不知道你写进去的是什么）。

---

## 23.7 类型擦除

### 泛型的幕后真相

Java 的泛型是**伪泛型**——它在编译后就把泛型信息擦掉了。这就是所谓的**类型擦除（Type Erasure）**。

为什么要擦除？因为 Java 诞生于 1995 年，泛型是 2004 年才加进来的。为了保持向后兼容（让旧代码还能跑），Java 选择了"编译时检查，运行时忽略"的方案。

### 类型擦除的过程

```java
// 源代码
public class ErasureBox<T> {
    private T value;

    public T getValue() {
        return value;
    }

    public void setValue(T value) {
        this.value = value;
    }
}
```

编译后（字节码层面等价于）：

```java
// 类型擦除后的样子（伪代码，实际上 .class 里看不到 T）
public class ErasureBox {
    private Object value;  // T 被替换为 Object

    public Object getValue() {
        return value;
    }

    public void setValue(Object value) { // T 被替换为 Object
        this.value = value;
    }
}
```

对于有上界的泛型，擦除规则如下：

| 泛型声明 | 擦除后 |
|---------|--------|
| `<T>` | `Object` |
| `<T extends Number>` | `Number` |
| `<T extends Comparable & Serializable>` | `Comparable` |

### 桥接方法（Bridge Methods）

类型擦除会导致一个有趣的现象——**桥接方法**。当你继承一个泛型类或实现一个泛型接口时，编译器会自动生成桥接方法来保持多态：

```java
// 源代码
public interface Comparable<String> {
    int compareTo(String other);
}

public class Person implements Comparable<Person> {
    private String name;

    public Person(String name) {
        this.name = name;
    }

    @Override
    public int compareTo(Person other) {
        return this.name.compareTo(other.name);
    }
}
```

编译后，Person 类里会有**两个** `compareTo` 方法：

```java
// 编译器自动生成的桥接方法
public int compareTo(Object other) {
    return compareTo((Person) other); // 调用我们的 compareTo(Person)
}

// 我们自己写的
public int compareTo(Person other) {
    return this.name.compareTo(other.name);
}
```

这就是为什么你调 `person.compareTo(anotherPerson)` 能正常工作的原因——编译器在背后偷偷帮你做了适配。

### 类型擦除的影响

因为类型信息被擦除了，有些事情在泛型代码里是做不了的：

```java
public class ErasureLimitation<T> {
    // 编译错误！不能 new T()
    public T create() {
        return new T(); // ❌ 无法实例化类型参数
    }

    // 编译错误！不能 new T[]
    public T[] createArray(int size) {
        return new T[size]; // ❌ 无法创建泛型数组
    }

    // 编译错误！不能 instanceof T
    public boolean check(Object obj) {
        return obj instanceof T; // ❌ instanceof 不支持泛型类型
    }

    // 编译错误！不能获取 T 的 Class
    public Class<T> getType() {
        return T.class; // ❌ 不能直接获取
    }
}
```

### 绕过类型擦除

虽然类型擦除有限制，但有些技巧可以绕过：

```java
public class WorkaroundDemo<T> {

    // 绕过1：通过 Class 对象创建实例
    public <T> T createInstance(Class<T> clazz) throws Exception {
        return clazz.getDeclaredConstructor().newInstance();
    }

    // 绕过2：通过反射获取泛型数组的组件类型
    public <T> T[] createArray(int size, Class<T> componentType) {
        @SuppressWarnings("unchecked")
        T[] array = (T[]) java.lang.reflect.Array.newInstance(componentType, size);
        return array;
    }

    // 绕过3：使用泛型标记类
    public static <T> void demo(Class<T> clazz) {
        System.out.println("类型: " + clazz.getName());
    }
}
```

---

## 本章小结

本章我们深入探讨了 Java 泛型（Generics）这座"类型的保险箱"：

| 知识点 | 核心要点 |
|--------|----------|
| **为什么需要泛型** | 泛型将类型检查提前到编译期，消除 ClassCastException，告别强制转型 |
| **泛型类** | `<T>` 声明类型参数，类名后跟尖括号，如 `class Box<T>` |
| **泛型接口** | 与泛型类类似，如 `interface Transformer<T, R>` |
| **泛型方法** | 在返回类型前声明类型参数，如 `<T> void method(T arg)` |
| **类型参数约束** | `<T extends Number>` 限制 T 的上界，多重约束用 `&` 连接 |
| **泛型通配符** | `? extends T`（生产者）/ `? super T`（消费者）/ `?`（无界），遵循 PECS 原则 |
| **类型擦除** | 泛型仅在编译期有效，运行时被擦除为 Object（或上界类型），编译器通过桥接方法维护多态 |

> 泛型是 Java 类型系统的地基级特性。掌握它，你不仅能写出更安全的代码，还能读懂 Java 集合框架、Stream API、Lombok 等几乎所有现代 Java 库的核心实现。
