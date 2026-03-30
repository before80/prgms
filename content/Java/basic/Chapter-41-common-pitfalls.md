+++
title = "第41章 Java 初学者常见坑大全（按类别整理）"
weight = 410
date = "2026-03-30T14:33:56.927+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++
# 第四十一章 Java 初学者常见坑大全（按类别整理）

> "Java 的坑，比你想的多；初学者的泪，比你想的咸。"
>
> 本章汇集了 Java 初学者最容易踩的 100+ 个坑，按类别整理，配有完整可运行的代码示例。学完本章，你可以骄傲地说："这些坑，我都踩过！"

---

## 41.1 语法层面的坑（30个）

### 坑1：分号才是真正的王者

你以为代码写得漂亮就能运行？不好意思，忘掉一个分号，Java 就会让你知道什么叫"一丝不苟"。

```java
// 错误示例
public class MissingSemicolon {
    public static void main(String[] args) {
        System.out.println("Hello")
        System.out.println("World")
    }
}
```

```java
// 正确示例
public class CorrectSemicolon {
    public static void main(String[] args) {
        System.out.println("Hello");
        System.out.println("World");
    }
}
```

**教训**：Java 不是 Python，别指望它会根据缩进猜测你的意图。

---

### 坑2：字符串比较请用 `equals()`，别用 `==`

`==` 比较的是引用（内存地址），`equals()` 比较的是内容。搞混了，你可能会在登录系统里遇到"密码对但不让进"的诡异情况。

```java
public class StringComparison {
    public static void main(String[] args) {
        String a = new String("java");
        String b = new String("java");

        // == 比较的是引用地址，a 和 b 是两个不同的对象
        System.out.println(a == b);             // false
        System.out.println(a.equals(b));       // true

        // 字符串字面量会进入字符串常量池，可能共享引用
        String c = "python";
        String d = "python";
        System.out.println(c == d);             // true（常量池复用）
        System.out.println(c.equals(d));       // true
    }
}
```

**建议**：永远用 `equals()` 比较字符串内容，`==` 留给基本类型。

---

### 坑3：`i++` 和 `++i` 傻傻分不清

前置++返回增加后的值，后置++返回增加前的值。在表达式里混用，一不小心就翻车。

```java
public class IncrementDemo {
    public static void main(String[] args) {
        int i = 5;

        // 后置++：先返回值，再自增
        int post = i++;
        System.out.println("post = " + post + ", i = " + i);  // post = 5, i = 6

        // 前置++：先自增，再返回值
        i = 5;
        int pre = ++i;
        System.out.println("pre = " + pre + ", i = " + i);    // pre = 6, i = 6

        // 在表达式中混用？恭喜你获得了玄学代码
        i = 5;
        int mystery = 2 * ++i + 2 * i++;
        System.out.println("mystery = " + mystery);  // 2*6 + 2*6 = 24? 不对!
        // 实际: 前半: 2*6=12(i变成6), 后半: 2*6=12(i变成7) = 24
    }
}
```

**建议**：单独一行用谁都行，在表达式里用请三思。

---

### 坑4：除法取整，丢失精度

整数相除结果还是整数，小数部分直接被"腰斩"。你以为算出来是 0.5，实际是 0。

```java
public class IntegerDivision {
    public static void main(String[] args) {
        int a = 5;
        int b = 2;

        // 整数除法：丢失小数部分
        System.out.println(a / b);        // 2，不是 2.5！

        // 解决方法：用 double
        System.out.println((double) a / b);  // 2.5
        System.out.println(a * 1.0 / b);     // 2.5
    }
}
```

---

### 坑5：`&`、`|` 和 `&&`、`||` 的区别

`&` 和 `|` 总是执行两边表达式，`&&` 和 `||` 才是短路操作。

```java
public class LogicalOperators {
    public static void main(String[] args) {
        int x = 10;

        // && 短路：左边 false，右边不执行
        if (x < 5 && (x = 100) > 0) {
            System.out.println("true");
        }
        System.out.println("x = " + x);  // x = 10，左边已经 false，右边没执行

        // & 不短路：两边都执行
        x = 10;
        if (x < 5 & (x = 100) > 0) {
            System.out.println("true");
        }
        System.out.println("x = " + x);  // x = 100，赋值语句执行了
    }
}
```

**忠告**：大多数情况下用 `&&` 和 `||`，除非你有特殊需求。

---

### 坑6：浮点数比较别用 `==`

0.1 + 0.2 在二进制浮点世界里不等于 0.3，这是一个著名的"历史遗留问题"。

```java
public class FloatComparison {
    public static void main(String[] args) {
        double a = 0.1;
        double b = 0.2;
        double sum = a + b;

        System.out.println(sum == 0.3);           // false！！
        System.out.println(sum);                 // 0.30000000000000004

        // 正确做法：使用 BigDecimal 或允许误差
        // 方法1：BigDecimal（精确）
        System.out.println(new java.math.BigDecimal("0.1")
            .add(new java.math.BigDecimal("0.2"))
            .compareTo(new java.math.BigDecimal("0.3")) == 0);  // true

        // 方法2：允许误差范围
        double epsilon = 0.0001;
        System.out.println(Math.abs(sum - 0.3) < epsilon);  // true
    }
}
```

---

### 坑7：变量命名踩雷

Java 有保留字（keyword），不能用 `class`、`int`、`if` 等作为变量名。

```java
// 这些都是非法的
// int class = 10;
// String if = "hello";
// double for = 3.14;

// 正确做法
int classCount = 10;
String condition = "hello";
double forRatio = 3.14;
```

---

### 坑8：类名和文件名必须匹配

`public class Hello` 必须放在 `Hello.java` 文件里，否则编译报错"类名与文件名不匹配"。

```java
// 文件名: Hello.java
public class Hello {
    public static void main(String[] args) {
        System.out.println("Hello, Java!");
    }
}
```

---

### 坑9：`main` 方法写错一个字都不行

`main` 方法是 Java 程序的入口，签名必须是 `public static void main(String[] args)`。

```java
// 这些都是错的
// public static main(String[] args) {}      // 缺少 void
// public void main(String[] args) {}        // 不是 static
// public static void Main(String[] args) {}  // 大写 M 不行
// public static void main(String args) {}    // 少了[]

// 正确写法
public class MainMethodDemo {
    public static void main(String[] args) {
        System.out.println("程序入口必须是这个签名！");
    }
}
```

---

### 坑10：switch 的 case 要加 break

忘了 break？那就恭喜你喜提"case 穿透"大礼包，程序会"义无反顾"地执行下一个 case。

```java
public class SwitchFallThrough {
    public static void main(String[] args) {
        int score = 85;

        switch (score / 10) {
            case 10:
            case 9:
                System.out.println("优秀");  // 90-100分都是优秀
                break;
            case 8:
                System.out.println("良好");
                break;
            case 7:
            case 6:
                System.out.println("及格");  // 60-79分都是及格
                break;
            default:
                System.out.println("不及格");
        }
    }
}
```

**提示**：故意利用穿透可以简化代码（如上例），但要加注释说明。

---

### 坑11：二维数组初始化要小心

```java
public class TwoDArrayInit {
    public static void main(String[] args) {
        // 创建一个 3x3 的二维数组
        int[][] arr = new int[3][3];

        // 下面这种创建方式只创建了外层数组，内层数组都是 null
        int[][] arr2 = new int[3][];
        // System.out.println(arr2[0][0]); // NullPointerException!

        // 正确做法：先创建外层，再逐行创建内层
        for (int i = 0; i < 3; i++) {
            arr2[i] = new int[3];
        }
        arr2[0][0] = 1;
        System.out.println("arr2[0][0] = " + arr2[0][0]);  // 1
    }
}
```

---

### 坑12：方法重载不看返回类型

方法重载（Overload）只看参数列表，和返回类型无关。

```java
public class OverloadDemo {
    // 这两个不是重载，是重复声明！编译错误
    // int add(int a, int b) { return a + b; }
    // double add(int a, int b) { return a + b; }

    // 正确重载：参数列表不同
    public static int add(int a, int b) {
        return a + b;
    }

    public static double add(double a, double b) {
        return a + b;
    }

    public static int add(int a, int b, int c) {
        return a + b + c;
    }

    public static void main(String[] args) {
        System.out.println(add(1, 2));       // 调用 int 版本
        System.out.println(add(1.5, 2.5));   // 调用 double 版本
        System.out.println(add(1, 2, 3));    // 调用三参数版本
    }
}
```

---

### 坑13：`byte` 和 `char` 不是一回事

`byte` 是有符号字节（-128~127），`char` 是无符号字符（0~65535），一字之差，天壤之别。

```java
public class ByteVsChar {
    public static void main(String[] args) {
        byte b = (byte) 200;  // 需要强制转型
        System.out.println("byte: " + b);    // -56（溢出）

        char c = 200;  // char 是 Unicode 字符
        System.out.println("char: " + c);    // Ę

        // byte[] 用于二进制数据，char[] 用于字符文本
        byte[] data = {65, 66, 67};
        System.out.println(new String(data));  // ABC
    }
}
```

---

### 坑14：static 方法不能访问实例成员

static 方法属于类，不依赖实例，所以不能访问 `this`、`instanceVar` 等实例成员。

```java
public class StaticMethodAccess {
    private int instanceVar = 100;  // 实例变量

    public static void staticMethod() {
        // System.out.println(instanceVar);  // 编译错误！
        // System.out.println(this);          // 编译错误！

        // 只能访问静态成员
        System.out.println("static method");
    }

    public void instanceMethod() {
        // 实例方法可以访问一切
        System.out.println(this.instanceVar);  // OK
        staticMethod();                         // OK
    }

    public static void main(String[] args) {
        staticMethod();
        // instanceMethod();  // 编译错误！静态上下文不能直接调用实例方法
        new StaticMethodAccess().instanceMethod();  // 需要创建实例
    }
}
```

---

### 坑15：别在 for 循环里改集合

一边遍历一边删？ConcurrentModificationException 在向你招手。

```java
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

public class ConcurrentModificationDemo {
    public static void main(String[] args) {
        List<String> names = new ArrayList<>();
        names.add("Alice");
        names.add("Bob");
        names.add("Charlie");

        // 错误做法：直接 remove 会抛异常
        // for (String name : names) {
        //     if (name.equals("Bob")) {
        //         names.remove(name);  // ConcurrentModificationException!
        //     }
        // }

        // 正确做法1：使用 Iterator
        Iterator<String> it = names.iterator();
        while (it.hasNext()) {
            String name = it.next();
            if (name.equals("Bob")) {
                it.remove();  // 用 Iterator 的 remove，不影响遍历
            }
        }
        System.out.println("方法1: " + names);  // [Alice, Charlie]

        // 正确做法2：倒序遍历
        names.clear();
        names.add("Alice");
        names.add("Bob");
        names.add("Charlie");
        for (int i = names.size() - 1; i >= 0; i--) {
            if (names.get(i).equals("Bob")) {
                names.remove(i);
            }
        }
        System.out.println("方法2: " + names);  // [Alice, Charlie]
    }
}
```

---

### 坑16：`finalize()` 已经deprecated

别依赖 `finalize()` 做资源清理，它可能根本不会执行，而且已经被标记为 @Deprecated。

```java
public class FinalizeDemo {
    private static int count = 0;

    @Override
    @SuppressWarnings("deprecation")
    protected void finalize() throws Throwable {
        count++;
        System.out.println("finalize 被调用了");
    }

    public static void main(String[] args) throws InterruptedException {
        FinalizeDemo obj = new FinalizeDemo();
        obj = null;
        System.gc();  // 建议 GC 回收，但不保证立即执行
        Thread.sleep(1000);
        System.out.println("finalize 被调用次数: " + count);
    }
}
```

**替代方案**：使用 try-with-resources 或手动 close()。

---

### 坑17：数字字面量的下划线和类型

```java
public class NumericLiterals {
    public static void main(String[] args) {
        // Java 7+ 支持数字字面量加下划线（增加可读性）
        int billion = 1_000_000_000;
        System.out.println("十亿: " + billion);

        // 注意：下划线不能在开头、结尾、紧邻小数点
        // 1_000.5_5  // 错误
        // _100       // 错误

        // long 类型要加 L/l，否则会当作 int 处理
        // long big = 3000000000;  // 编译错误！超出 int 范围
        long big = 3000000000L;  // 正确

        // float 字面量要加 F/f
        float pi = 3.14F;  // 正确
        // float pi2 = 3.14;  // 错误！double 不能直接赋给 float
    }
}
```

---

### 坑18：位运算符优先级低

```java
public class BitOperatorPrecedence {
    public static void main(String[] args) {
        int x = 1;
        int y = 2;

        // 表达式  x & y == 1  被解析为  x & (y == 1)
        System.out.println(x & y == 1);   // false，不是 0！

        // 应该加括号
        System.out.println((x & y) == 1);  // false

        // 验证：x & y 的值
        System.out.println("x & y = " + (x & y));  // 0

        // 正确写法
        System.out.println((x & y) == 0);  // true
    }
}
```

---

### 坑19：浮点数的 NaN 和无穷大

```java
public class FloatNaNInfinity {
    public static void main(String[] args) {
        double d1 = 0.0 / 0.0;  // NaN
        double d2 = 1.0 / 0.0;  // Infinity
        double d3 = -1.0 / 0.0; // -Infinity

        System.out.println("d1 = " + d1);  // NaN
        System.out.println("d2 = " + d2);  // Infinity
        System.out.println("d3 = " + d3);  // -Infinity

        // NaN 非常特殊：它不等于任何值，包括自己
        System.out.println(d1 == d1);        // false！
        System.out.println(Double.isNaN(d1)); // true

        // Infinity 的比较
        System.out.println(d2 > 1000);  // true
        System.out.println(d2 == Double.POSITIVE_INFINITY);  // true
    }
}
```

---

### 坑20：short 和 byte 的自增要小心

```java
public class ShortByteIncrement {
    public static void main(String[] args) {
        short s = 1;
        // s = s + 1;    // 编译错误！int + short -> int，需要强制转型
        s = (short)(s + 1);  // 正确
        s += 1;              // 正确！+= 自动强制转型
        System.out.println("s = " + s);

        byte b = 1;
        // b = b + 1;    // 编译错误！
        b = (byte)(b + 1);  // 正确
        b += 1;             // 正确！+= 自动处理
        System.out.println("b = " + b);

        // 但++不一样！byte++ 和 short++ 是合法的
        byte bb = 127;
        bb++;  // 不报错，但会溢出变成 -128
        System.out.println("bb = " + bb);
    }
}
```

---

### 坑21：静态初始化块和实例初始化块

```java
public class InitializationOrder {
    static {
        System.out.println("静态初始化块 1");
    }

    {
        System.out.println("实例初始化块 1");
    }

    public InitializationOrder() {
        System.out.println("构造函数");
    }

    static {
        System.out.println("静态初始化块 2");
    }

    {
        System.out.println("实例初始化块 2");
    }

    public static void main(String[] args) {
        System.out.println("=== 创建第一个对象 ===");
        new InitializationOrder();
        System.out.println("=== 创建第二个对象 ===");
        new InitializationOrder();
    }
}
```

**输出顺序**：静态块（按出现顺序）→ 主方法 → 实例块+构造函数（每次 new 都执行）

---

### 坑22：可变参数要放最后

```java
public class VarargsOrder {
    // 正确：可变参数放最后
    public static void printAll(String prefix, int... numbers) {
        System.out.print(prefix);
        for (int n : numbers) {
            System.out.print(n + " ");
        }
        System.out.println();
    }

    // 编译错误：可变参数不能在中间
    // public static void error(String... args, int x) {}

    public static void main(String[] args) {
        printAll("数字: ", 1, 2, 3, 4, 5);
        printAll("结果: ");
    }
}
```

---

### 坑23：goto？Java 没有这回事

```java
// Java 没有 goto 语句
// goto;

public class LabelDemo {
    public static void main(String[] args) {
        // 但 Java 有标签（Label），配合 break/continue 使用
        outer:
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 5; j++) {
                if (j == 2) {
                    break outer;  // 直接跳出外层循环
                }
                System.out.println("i=" + i + ", j=" + j);
            }
        }
        System.out.println("循环结束");
    }
}
```

---

### 坑24：transient 变量不参与序列化

```java
import java.io.*;

public class TransientDemo implements Serializable {
    private static final long serialVersionUID = 1L;
    private String name;
    private transient String password;  // 不会被序列化

    public TransientDemo(String name, String password) {
        this.name = name;
        this.password = password;
    }

    @Override
    public String toString() {
        return "name='" + name + "', password='" + password + "'";
    }

    public static void main(String[] args) throws Exception {
        TransientDemo obj = new TransientDemo("张三", "secret123");

        // 序列化
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        ObjectOutputStream oos = new ObjectOutputStream(baos);
        oos.writeObject(obj);
        oos.close();

        // 反序列化
        ByteArrayInputStream bais = new ByteArrayInputStream(baos.toByteArray());
        ObjectInputStream ois = new ObjectInputStream(bais);
        TransientDemo restored = (TransientDemo) ois.readObject();
        ois.close();

        System.out.println("原对象: " + obj);
        System.out.println("恢复后: " + restored);
        // password 变成 null 了！
    }
}
```

---

### 坑25：Integer 缓存池的坑

```java
public class IntegerCacheDemo {
    public static void main(String[] args) {
        // Integer 缓存了 -128 到 127 的整数
        Integer a = 127;
        Integer b = 127;
        System.out.println(a == b);  // true（缓存）

        Integer c = 128;
        Integer d = 128;
        System.out.println(c == d);  // false（超出缓存范围）

        // 自动装箱的陷阱
        Integer e = 100;
        Integer f = 100;
        System.out.println(e == f);  // true

        // 但运算会拆箱
        System.out.println(e + f);   // 200，自动拆箱
    }
}
```

---

### 坑26：三元运算符的自动拆箱

```java
public class TernaryUnbox {
    public static void main(String[] args) {
        Integer a = null;

        // 三元运算符会把 null 自动拆箱，引发 NullPointerException
        // System.out.println(true ? a : 0);  // NPE!

        // 编译器看到的是：a.intValue()，但 a 是 null
        Integer b = 5;
        // 这行是安全的
        System.out.println(false ? b : 0);  // 0，但不推荐这样写
    }
}
```

---

### 坑27：this 和 super 在构造函数中的位置

```java
public class ThisSuperDemo {
    private int value;

    public ThisSuperDemo() {
        // super() 或 this() 必须放在构造函数第一行
        // 下面的写法是错误的：
        // System.out.println("在 super 之前打印");
        // super();

        // 正确做法
        this(0);  // 调用另一个构造函数，也必须第一行
    }

    public ThisSuperDemo(int value) {
        super();  // 默认调用 super()
        this.value = value;
    }
}
```

---

### 坑28：匿名内部类访问外部变量必须是 final

```java
public class AnonymousClassDemo {
    private int outerVar = 10;

    public void test() {
        final int localVar = 20;  // 必须加 final（Java 8+ 可省略但仍是隐式 final）
        int mutableVar = 30;     // Java 8+ 可以省略 final，但不建议改

        new Thread(new Runnable() {
            @Override
            public void run() {
                // 内部类访问外部变量
                System.out.println("outerVar = " + outerVar);  // OK，外部类实例字段
                System.out.println("localVar = " + localVar);   // OK，final 变量
                // localVar = 999;  // 编译错误，不能修改
            }
        }).start();
    }

    public static void main(String[] args) {
        new AnonymousClassDemo().test();
    }
}
```

---

### 坑29：枚举可以switch

```java
public class EnumSwitchDemo {
    enum Color {
        RED, GREEN, BLUE
    }

    public static void main(String[] args) {
        Color c = Color.GREEN;

        // 枚举可以直接用在 switch 里
        switch (c) {
            case RED:
                System.out.println("红色");
                break;
            case GREEN:
                System.out.println("绿色");
                break;
            case BLUE:
                System.out.println("蓝色");
                break;
        }
    }
}
```

---

### 坑30：boolean 类型只有 true 和 false

```java
public class BooleanDemo {
    public static void main(String[] args) {
        // Java 的 boolean 只有 true 和 false
        boolean isJavaFun = true;
        boolean isFishTasty = false;

        // 没有 "1" 或 "0"，没有 null（作为字面量）
        // boolean notBool = 1;   // 编译错误！

        // 不要用 Boolean.TRUE/FALSE 比较，直接用 == 或 !=
        Boolean flag = Boolean.TRUE;
        if (flag == Boolean.TRUE) {  // 可以，但不推荐
            System.out.println("flag 是 true");
        }
        if (flag) {  // 推荐写法
            System.out.println("flag 是 true（推荐写法）");
        }
    }
}
```

---

## 41.2 OOP 层面的坑（20个）

### 坑31：子类构造函数必须调用父类构造函数

如果父类没有无参构造函数，子类必须显式调用有参构造函数。

```java
public class ConstructorChainDemo {
    public static void main(String[] args) {
        new Child();
    }
}

class Parent {
    Parent() {
        System.out.println("Parent() 无参构造");
    }
}

class Child extends Parent {
    Child() {
        // super() 会自动调用父类的无参构造函数
        // 如果父类没有无参构造函数，子类必须显式调用 super(参数)
        System.out.println("Child() 构造");
    }
}
```

```java
// 没有无参构造函数的父类
class Parent2 {
    private String name;

    Parent2(String name) {
        this.name = name;
    }
}

// 子类必须显式调用 super
class Child2 extends Parent2 {
    Child2() {
        super("默认名称");  // 必须调用！
        System.out.println("Child2()");
    }
}
```

---

### 坑32：重写方法不能缩小访问权限

子类重写父类方法时，访问修饰符必须大于等于父类的可见性。

```java
public class AccessModifierDemo {
    public static void main(String[] args) {
        Parent p = new Child();
        p.say();  // 输出什么？取决于实际类型
    }
}

class Parent {
    public void say() {
        System.out.println("Parent: 你好");
    }
}

class Child extends Parent {
    // 不能缩小访问权限！下面会编译错误：
    // private void say() {}     // 错误！比 public 更严格
    // void say() {}              // 错误！默认是 package-private，比 public 严格

    public void say() {
        System.out.println("Child: 你好");
    }
}
```

---

### 坑33：static 方法不能被重写，只能被隐藏

子类定义与父类 static 方法签名相同的方法，不是重写，是"隐藏"。

```java
public class StaticOverrideDemo {
    public static void main(String[] args) {
        Parent p = new Child();

        // 调用的是父类的 static 方法（因为引用类型是 Parent）
        p.hello();  // Parent: hello

        // 实际上调用的取决于编译时类型，不是运行时类型
    }
}

class Parent {
    public static void hello() {
        System.out.println("Parent: hello");
    }
}

class Child extends Parent {
    // 这不是重写，是隐藏（Override 是运行时多态，隐藏是编译时绑定）
    public static void hello() {
        System.out.println("Child: hello");
    }
}
```

---

### 坑34：构造函数的陷阱——不要在构造函数里调用可被重写的方法

```java
public class ConstructorOverrideTrap {
    public static void main(String[] args) {
        SubClass obj = new SubClass();
        // 输出顺序：
        // 1. SubClass 构造函数调用 super()
        // 2. Parent 构造函数调用 doSomething()
        // 3. 因为多态，实际调用的是 SubClass 的 doSomething()
        // 4. 此时 SubClass 的字段还没初始化！
    }
}

class Parent {
    Parent() {
        System.out.println("Parent 构造开始");
        doSomething();  // 陷阱：调用了可被重写的方法
        System.out.println("Parent 构造结束");
    }

    public void doSomething() {
        System.out.println("Parent.doSomething()");
    }
}

class SubClass extends Parent {
    private int value = printAndReturn(100);

    public SubClass() {
        System.out.println("SubClass 构造");
    }

    @Override
    public void doSomething() {
        // 此时 value 还是 0！因为父类构造函数先于子类字段初始化执行
        System.out.println("SubClass.doSomething(), value = " + value);
    }

    private static int printAndReturn(int v) {
        System.out.println("SubClass 字段初始化: " + v);
        return v;
    }
}
```

---

### 坑35：instanceof 和强制转换

```java
public class InstanceofDemo {
    public static void main(String[] args) {
        Object obj = "Hello";

        // instanceof 检查类型
        if (obj instanceof String) {
            String s = (String) obj;  // 安全转换
            System.out.println("字符串长度: " + s.length());
        }

        // Java 16+ 支持 instanceof 模式匹配（不需要显式转型）
        if (obj instanceof String s) {
            System.out.println("字符串长度(模式匹配): " + s.length());
        }
    }
}
```

---

### 坑36：equals 和 hashCode 必须配对使用

如果两个对象 equals，它们必须有相同的 hashCode。

```java
import java.util.HashSet;
import java.util.Set;

public class EqualsHashCodeDemo {
    public static void main(String[] args) {
        Set<Point> points = new HashSet<>();
        Point p1 = new Point(1, 2);
        Point p2 = new Point(1, 2);

        points.add(p1);
        System.out.println(points.contains(p2));  // false！如果没有正确实现 hashCode

        // 正确实现后
        points.clear();
        points.add(new GoodPoint(1, 2));
        System.out.println(points.contains(new GoodPoint(1, 2)));  // true
    }
}

class Point {
    int x, y;

    Point(int x, int y) {
        this.x = x;
        this.y = y;
    }

    // 没有重写 equals 和 hashCode
}

// 正确实现
class GoodPoint {
    int x, y;

    GoodPoint(int x, int y) {
        this.x = x;
        this.y = y;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        GoodPoint that = (GoodPoint) o;
        return x == that.x && y == that.y;
    }

    @Override
    public int hashCode() {
        return 31 * x + y;
    }
}
```

---

### 坑37：组合优先于继承

继承是强耦合，用组合更灵活。

```java
// 不推荐：继承用于"是"的关系，不是用于"有"的关系
class Dog extends Animal {
    // Dog is Animal，可以
}

class Car extends Animal {  // 这就不合理了
    // Car has Engine，应该用组合
}

// 推荐：组合
class Car {
    private Engine engine;  // Car has Engine
    private Wheel[] wheels;

    public void start() {
        engine.start();
    }
}
```

---

### 坑38：接口和抽象类的选择

接口用于行为抽象，抽象类用于代码复用。

```java
// 接口：支持多实现
interface Flyable {
    void fly();
}

interface Swimmable {
    void swim();
}

// 类：单继承
abstract class Animal {
    void eat() {
        System.out.println("吃东西");
    }
}

// 可以同时实现多个接口，但只能继承一个类
class Duck extends Animal implements Flyable, Swimmable {
    @Override
    public void fly() {
        System.out.println("鸭子飞");
    }

    @Override
    public void swim() {
        System.out.println("鸭子游泳");
    }
}
```

---

### 坑39：内部类和外部类的访问

```java
public class InnerClassAccess {
    private int outerField = 10;
    private static int staticField = 20;

    public static void main(String[] args) {
        // 静态内部类可以直接访问外部类的静态成员
        System.out.println(InnerClassAccess.staticField);
    }

    public void instanceMethod() {
        // 实例内部类可以访问外部类的一切成员
        class LocalClass {
            void display() {
                System.out.println(outerField);  // OK
                System.out.println(staticField);  // OK
            }
        }
    }

    // 非静态内部类持有外部类引用
    public class Inner {
        int innerField = 30;

        void accessOuter() {
            System.out.println(outerField);  // 自动持有外部类引用
            System.out.println(this.innerField);  // this 是内部类的
            System.out.println(InnerClassAccess.this.outerField);  // 外部类引用
        }
    }

    public static void main(String[] args) {
        InnerClassAccess outer = new InnerClassAccess();
        Inner inner = outer.new Inner();
        inner.accessOuter();
    }
}
```

---

### 坑40：序列化会破坏单例

反序列化会创建新对象，破坏单例模式。

```java
import java.io.*;

public class SerializableSingleton implements Serializable {
    private static final long serialVersionUID = 1L;
    private static final SerializableSingleton INSTANCE = new SerializableSingleton();

    private SerializableSingleton() {
        // 私有构造函数
    }

    public static SerializableSingleton getInstance() {
        return INSTANCE;
    }

    // 防止反序列化创建新对象
    protected Object readResolve() {
        return INSTANCE;
    }

    public static void main(String[] args) throws Exception {
        SerializableSingleton s1 = SerializableSingleton.getInstance();
        SerializableSingleton s2 = SerializableSingleton.getInstance();
        System.out.println(s1 == s2);  // true

        // 序列化
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        ObjectOutputStream oos = new ObjectOutputStream(baos);
        oos.writeObject(s1);

        // 反序列化
        ByteArrayInputStream bais = new ByteArrayInputStream(baos.toByteArray());
        ObjectInputStream ois = new ObjectInputStream(bais);
        SerializableSingleton s3 = (SerializableSingleton) ois.readObject();

        System.out.println(s1 == s3);  // 有 readResolve 返回 true，否则 false
    }
}
```

---

### 坑41：可变对象作为参数传入后被修改

```java
import java.util.Date;

public class MutableParamDemo {
    private Date birthDate;

    public MutableParamDemo(Date birthDate) {
        // 危险！外部的 Date 对象和内部引用指向同一个对象
        this.birthDate = birthDate;
    }

    public static void main(String[] args) {
        Date d = new Date(2000, 1, 1);
        MutableParamDemo obj = new MutableParamDemo(d);

        // 外部修改 Date
        d.setYear(3000);

        // 内部的值也被改了！
        System.out.println("birthDate: " + obj.birthDate);
    }
}
```

**正确做法**：防御性拷贝

```java
public MutableParamDemo(Date birthDate) {
    this.birthDate = new Date(birthDate.getTime());  // 拷贝
}
```

---

### 坑42：equals 的对称性和传递性

自定义 equals 要注意数学性质。

```java
public class EqualsSymmetry {
    public static void main(String[] args) {
        // 违反对称性
        CaseInsensitiveString s1 = new CaseInsensitiveString("java");
        String s2 = new String("JAVA");

        // s1.equals(s2) 可能不等于 s2.equals(s1)
    }
}

class CaseInsensitiveString {
    private String s;

    public CaseInsensitiveString(String s) {
        this.s = s;
    }

    @Override
    public boolean equals(Object obj) {
        if (obj instanceof CaseInsensitiveString) {
            return s.equalsIgnoreCase(((CaseInsensitiveString) obj).s);
        }
        // 违反对称性！String 不认识我们
        if (obj instanceof String) {
            return s.equalsIgnoreCase((String) obj);
        }
        return false;
    }
}
```

---

### 坑43：lambda 表达式里的 this

lambda 表达式里的 this 指的是包含它的外部类实例，不是 lambda 本身。

```java
public class LambdaThisDemo {
    private String field = "外部类字段";

    public void method() {
        Runnable r = () -> {
            // 这里的 this 是 LambdaThisDemo，不是 Runnable
            System.out.println(this.field);
        };
        r.run();
    }

    public static void main(String[] args) {
        new LambdaThisDemo().method();  // 输出：外部类字段
    }
}
```

---

### 坑44：方法引用和 lambda 的区别

方法引用和 lambda 都能实现函数式接口，但方法引用更简洁。

```java
import java.util.Arrays;
import java.util.List;
import java.util.function.Consumer;
import java.util.function.Function;
import java.util.function.Supplier;

public class MethodReferenceDemo {
    public static void main(String[] args) {
        List<String> names = Arrays.asList("Alice", "Bob", "Charlie");

        // Lambda 写法
        names.forEach(name -> System.out.println(name));

        // 方法引用写法（更简洁）
        names.forEach(System.out::println);

        // 四种方法引用
        // 1. 静态方法引用: ClassName::staticMethod
        Function<String, Integer> parser = Integer::parseInt;

        // 2. 实例方法引用: instance::instanceMethod
        String str = "Hello";
        Supplier<Integer> length = str::length;

        // 3. 对象方法引用: ClassName::instanceMethod
        Function<String, String> upper = String::toUpperCase;

        // 4. 构造函数引用: ClassName::new
        Supplier<StringBuilder> sbSupplier = StringBuilder::new;
    }
}
```

---

### 坑45：序列化版本 UID

每个可序列化类都应该声明 `serialVersionUID`，否则类结构变化后旧对象无法反序列化。

```java
import java.io.*;

public class SerialVersionUIDDemo implements Serializable {
    // 推荐显式声明
    private static final long serialVersionUID = 1L;

    private String name;

    public SerialVersionUIDDemo(String name) {
        this.name = name;
    }
}
```

---

### 坑46：final 字段初始化时机

final 字段必须在构造函数或初始化块中初始化。

```java
public class FinalFieldInit {
    private final int a;
    private final String b = "初始化";

    public FinalFieldInit(int a) {
        this.a = a;  // 必须在构造函数中初始化
    }

    // 错误：final 字段没有初始化
    // private final int c;

    public static void main(String[] args) {
        FinalFieldInit obj = new FinalFieldInit(10);
        System.out.println("a = " + obj.a + ", b = " + obj.b);
    }
}
```

---

### 坑47：接口里的常量

接口里的字段默认是 `public static final`，可以直接使用。

```java
public interface MathConstants {
    // 等价于 public static final double PI = 3.14159;
    double PI = 3.14159;

    // 等价于 public static final double E = 2.71828;
    double E = 2.71828;
}

class Circle {
    public double area(double radius) {
        return MathConstants.PI * radius * radius;
    }
}
```

---

### 坑48：枚举的构造函数是 private

枚举的构造函数隐式是 private，不用写也能生效。

```java
public enum Weekday {
    MONDAY("周一"),
    TUESDAY("周二"),
    WEDNESDAY("周三"),
    THURSDAY("周四"),
    FRIDAY("周五"),
    SATURDAY("周六"),
    SUNDAY("周日");

    private final String chinese;

    // 枚举构造函数必须是 private（隐式）
    Weekday(String chinese) {
        this.chinese = chinese;
    }

    public String getChinese() {
        return chinese;
    }
}
```

---

### 坑49：返回 null 还是空集合？

方法返回集合时，避免返回 null，用空集合代替。

```java
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class ReturnEmptyVsNull {
    // 反面教材
    public List<String> getBadList() {
        return null;  // 调用方必须检查 null
    }

    // 正面教材
    public List<String> getGoodList() {
        return Collections.emptyList();  // 返回不可变的空列表
    }

    // 如果要返回可变列表
    public List<String> getEmptyMutableList() {
        return new ArrayList<>();  // 返回空的可变列表
    }
}
```

---

### 坑50：Cloneable 接口是破损的设计

`Cloneable` 没有定义 `clone()` 方法，Object 的 `clone()` 是 protected 的，克隆很麻烦。

```java
public class CloneableDemo {
    public static void main(String[] args) throws CloneNotSupportedException {
        Student s1 = new Student("张三", 20);
        Student s2 = (Student) s1.clone();  // 需要类型转换

        s2.name = "李四";
        System.out.println("s1: " + s1);  // 不变
        System.out.println("s2: " + s2);
    }
}

class Student implements Cloneable {
    String name;
    int age;

    Student(String name, int age) {
        this.name = name;
        this.age = age;
    }

    @Override
    public Object clone() throws CloneNotSupportedException {
        return super.clone();  // Object 的 clone 是浅拷贝
    }

    @Override
    public String toString() {
        return name + ", " + age;
    }
}
```

**推荐**：使用拷贝构造函数或工厂方法。

---

## 41.3 集合层面的坑（20个）

### 坑51：ArrayList 初始化容量

ArrayList 默认容量是 10，不断 add 会触发扩容，指定初始容量可以减少扩容开销。

```java
import java.util.ArrayList;

public class ArrayListInit {
    public static void main(String[] args) {
        // 不指定容量，默认空数组，第一次 add 时扩容到 10
        ArrayList<String> list1 = new ArrayList<>();

        // 预知大小，指定初始容量
        ArrayList<String> list2 = new ArrayList<>(100);

        // 使用 List.of() 创建不可变列表（Java 9+）
        var immutable = java.util.List.of("A", "B", "C");
        // immutable.add("D");  // UnsupportedOperationException!
    }
}
```

---

### 坑52：HashMap 的 key 要重写 equals 和 hashCode

```java
import java.util.HashMap;
import java.util.Map;

public class HashMapKeyDemo {
    public static void main(String[] args) {
        Map<PointKey, String> map = new HashMap<>();
        PointKey key = new PointKey(1, 2);

        map.put(key, "第一个点");
        System.out.println(map.get(key));  // 正常获取

        // 如果 key 的 hashCode/equals 实现有问题
        System.out.println(map.get(new PointKey(1, 2)));  // 可能 null!
    }
}

class PointKey {
    int x, y;

    PointKey(int x, int y) {
        this.x = x;
        this.y = y;
    }

    // 错误实现：只基于 x
    @Override
    public int hashCode() {
        return x;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        PointKey that = (PointKey) o;
        return x == that.x;  // 忽略了 y！
    }
}
```

---

### 坑53：HashMap 的死循环（Java 7 及之前）

在多线程环境下，Java 7 的 HashMap 扩容时可能导致环形链表，造成死循环。Java 8 修复了这个问题，但仍不是线程安全。

```java
// 危险代码示例（仅供理解，不要在实际代码中使用）
import java.util.HashMap;
import java.util.Map;

public class HashMapThreadUnsafe {
    // 不要在多线程环境下共享 HashMap
    private static final Map<Integer, Integer> map = new HashMap<>();

    public static void main(String[] args) throws InterruptedException {
        Thread t1 = new Thread(() -> {
            for (int i = 0; i < 1000; i++) {
                map.put(i, i);
            }
        });

        Thread t2 = new Thread(() -> {
            for (int i = 0; i < 1000; i++) {
                map.put(i, i);
            }
        });

        t1.start();
        t2.start();
        t1.join();
        t2.join();

        System.out.println("map.size() = " + map.size());
        // 可能有数据丢失，或抛出 ConcurrentModificationException
    }
}
```

**正确做法**：使用 `ConcurrentHashMap`。

---

### 坑54：Arrays.asList() 返回的列表不支持结构性修改

`Arrays.asList()` 返回的是固定大小的视图，不能 add/remove。

```java
import java.util.Arrays;
import java.util.List;

public class ArraysAsListDemo {
    public static void main(String[] args) {
        String[] array = {"A", "B", "C"};
        List<String> list = Arrays.asList(array);

        list.set(0, "X");  // OK，可以修改
        System.out.println("array[0] = " + array[0]);  // 数组也被改了！

        // list.add("D");  // UnsupportedOperationException!
        // list.remove(0); // UnsupportedOperationException!

        // 如果需要可变列表
        java.util.ArrayList<String> mutableList = new java.util.ArrayList<>(list);
        mutableList.add("D");  // OK
    }
}
```

---

### 坑55：subList 不是独立的新列表

`List.subList()` 返回的是原列表的视图，对 subList 的修改会影响原列表。

```java
import java.util.ArrayList;
import java.util.List;

public class SubListDemo {
    public static void main(String[] args) {
        List<Integer> list = new ArrayList<>();
        for (int i = 0; i < 10; i++) {
            list.add(i);
        }

        List<Integer> sub = list.subList(2, 5);  // [2, 3, 4]
        System.out.println("sub: " + sub);

        // 修改 subList
        sub.set(0, 99);  // 修改会影响原列表
        System.out.println("list: " + list);  // list[2] 变成 99

        // subList 的操作范围不能超出原列表
        // sub.clear();  // 清空 subList 会清空原列表对应范围！
    }
}
```

---

### 坑56：Iterator.remove() 的正确姿势

必须先 `next()` 再 `remove()`，不能连续 remove。

```java
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

public class IteratorRemoveDemo {
    public static void main(String[] args) {
        List<String> list = new ArrayList<>();
        list.add("A");
        list.add("B");
        list.add("C");

        Iterator<String> it = list.iterator();

        // 正确做法：先 next，再 remove
        while (it.hasNext()) {
            String s = it.next();
            if (s.equals("B")) {
                it.remove();  // OK
            }
        }
        System.out.println("删除 B 后: " + list);

        // 错误做法：没有 next 就 remove
        // Iterator<String> it2 = list.iterator();
        // it2.remove();  // IllegalStateException!
    }
}
```

---

### 坑57：Set 的 add 返回值

`Set.add()` 返回 boolean，表示是否添加成功（元素不存在则添加成功返回 true）。

```java
import java.util.HashSet;
import java.util.Set;

public class SetAddReturnDemo {
    public static void main(String[] args) {
        Set<String> set = new HashSet<>();

        System.out.println(set.add("A"));  // true
        System.out.println(set.add("A"));  // false，已存在

        System.out.println("set = " + set);  // [A]

        // 利用返回值检测重复
        if (!set.add("B")) {
            System.out.println("B 已存在！");
        }
    }
}
```

---

### 坑58：TreeSet 的自然排序和自定义排序

TreeSet 元素必须可比较，要么实现 Comparable，要么提供 Comparator。

```java
import java.util.Set;
import java.util.TreeSet;

public class TreeSetDemo {
    public static void main(String[] args) {
        // 自然排序：元素实现 Comparable
        Set<Integer> numSet = new TreeSet<>();
        numSet.add(3);
        numSet.add(1);
        numSet.add(2);
        System.out.println(numSet);  // [1, 2, 3]

        // 自定义排序
        Set<String> strSet = new TreeSet<>((a, b) -> b.compareTo(a));  // 逆序
        strSet.add("Apple");
        strSet.add("Banana");
        strSet.add("Cherry");
        System.out.println(strSet);  // [Cherry, Banana, Apple]
    }
}
```

---

### 坑59：LinkedList 不是 List 的最佳实现

ArrayList 随机访问 O(1)，LinkedList 随机访问 O(n)。大多数场景下 ArrayList 更高效。

```java
import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;

public class ArrayListVsLinkedList {
    public static void main(String[] args) {
        int n = 100000;

        // ArrayList 随机访问快
        List<Integer> arrayList = new ArrayList<>();
        for (int i = 0; i < n; i++) arrayList.add(i);
        long start = System.nanoTime();
        arrayList.get(n / 2);  // O(1)
        System.out.println("ArrayList get: " + (System.nanoTime() - start) + " ns");

        // LinkedList 随机访问慢
        List<Integer> linkedList = new LinkedList<>();
        for (int i = 0; i < n; i++) linkedList.add(i);
        start = System.nanoTime();
        linkedList.get(n / 2);  // O(n)，要遍历一半
        System.out.println("LinkedList get: " + (System.nanoTime() - start) + " ns");
    }
}
```

---

### 坑60：HashSet 底层是 HashMap

HashSet 内部用一个 HashMap 存储元素，value 是固定的 PRESENT 对象。

```java
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;

public class HashSetInternal {
    public static void main(String[] args) {
        Set<String> set = new HashSet<>();
        set.add("Hello");
        set.add("World");

        // HashSet 底层是 HashMap，添加的元素是 key
        // value 是一个固定的对象（private static final Object PRESENT = new Object()）

        // 如果需要同时存 key 和 value，用 HashMap
        Map<String, Integer> map = new HashMap<>();
        map.put("Alice", 25);
        map.put("Bob", 30);
    }
}
```

---

### 坑61：Collections.sort() 会修改原列表

`Collections.sort()` 是原地排序，直接修改列表顺序。

```java
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class CollectionsSortDemo {
    public static void main(String[] args) {
        List<Integer> list = new ArrayList<>();
        list.add(3);
        list.add(1);
        list.add(2);

        List<Integer> backup = new ArrayList<>(list);  // 先备份

        Collections.sort(list);  // 原地排序
        System.out.println("排序后: " + list);  // [1, 2, 3]

        // 如果需要保留原列表，先拷贝
        List<Integer> sorted = new ArrayList<>(backup);
        Collections.sort(sorted);
        System.out.println("原列表: " + backup);
    }
}
```

---

### 坑62：Comparable 和 Comparator 的区别

Comparable 是自然排序（一目了然），Comparator 是自定义排序（灵活多样）。

```java
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;

public class ComparableVsComparator {
    public static void main(String[] args) {
        List<Student> students = new ArrayList<>();
        students.add(new Student("张三", 85));
        students.add(new Student("李四", 92));
        students.add(new Student("王五", 78));

        // Student 已实现 Comparable（按分数降序）
        // students.sort(null);  // 使用 Comparable

        // 也可以用 Comparator 覆盖
        students.sort(Comparator.comparing(Student::getName));
        System.out.println("按姓名排序: " + students);

        students.sort(Comparator.comparingInt(Student::getScore).reversed());
        System.out.println("按分数降序: " + students);
    }
}

class Student implements Comparable<Student> {
    private String name;
    private int score;

    Student(String name, int score) {
        this.name = name;
        this.score = score;
    }

    public String getName() { return name; }
    public int getScore() { return score; }

    @Override
    public int compareTo(Student other) {
        return Integer.compare(other.score, this.score);  // 按分数降序
    }

    @Override
    public String toString() {
        return name + "(" + score + ")";
    }
}
```

---

### 坑63：ConcurrentHashMap 不允许 null

HashMap 可以存 null key 和 null value，但 ConcurrentHashMap 不允许。

```java
import java.util.ConcurrentHashMap;
import java.util.HashMap;

public class NullInConcurrentHashMap {
    public static void main(String[] args) {
        // HashMap 可以
        HashMap<String, String> map = new HashMap<>();
        map.put(null, "value");
        map.put("key", null);
        System.out.println("HashMap: " + map);

        // ConcurrentHashMap 不行
        ConcurrentHashMap<String, String> chm = new ConcurrentHashMap<>();
        // chm.put(null, "value");  // NullPointerException!
        // chm.put("key", null);   // NullPointerException!
        chm.put("key", "value");  // OK
    }
}
```

---

### 坑64：fail-fast 机制

迭代时修改集合会触发 fail-fast，快速失败。

```java
import java.util.ArrayList;
import java.util.List;

public class FailFastDemo {
    public static void main(String[] args) {
        List<String> list = new ArrayList<>();
        list.add("A");
        list.add("B");
        list.add("C");

        for (String s : list) {
            if (s.equals("B")) {
                list.remove(s);  // 可能触发 ConcurrentModificationException
            }
        }

        // 正确做法：用 Iterator
        for (java.util.Iterator<String> it = list.iterator(); it.hasNext(); ) {
            String s = it.next();
            if (s.equals("B")) {
                it.remove();
            }
        }
        System.out.println(list);
    }
}
```

---

### 坑65：EnumSet 的高效实现

EnumSet 使用位向量实现，比 HashSet 更高效。

```java
import java.util.EnumSet;

public class EnumSetDemo {
    public static void main(String[] args) {
        // EnumSet 是抽象类，不能 new，用 of() 创建
        EnumSet<Color> set = EnumSet.noneOf(Color.class);  // 空集合
        set.add(Color.RED);
        set.add(Color.BLUE);

        // 其他创建方式
        EnumSet<Color> set2 = EnumSet.allOf(Color.class);  // 全部
        EnumSet<Color> set3 = EnumSet.of(Color.RED, Color.GREEN);  // 指定
        EnumSet<Color> set4 = EnumSet.range(Color.RED, Color.GLUE);  // 范围
    }
}

enum Color {
    RED, ORANGE, YELLOW, GREEN, BLUE, INDIGO, VIOLET, BLACK, WHITE, GLUE
}
```

---

### 坑66：PriorityQueue 的堆特性

PriorityQueue 是基于堆的优先级队列，不保证 FIFO，按自然顺序或自定义顺序出队。

```java
import java.util.PriorityQueue;
import java.util.Queue;

public class PriorityQueueDemo {
    public static void main(String[] args) {
        // 默认是最小堆（自然顺序）
        Queue<Integer> pq = new PriorityQueue<>();
        pq.add(5);
        pq.add(2);
        pq.add(8);
        pq.add(1);

        System.out.println("出队顺序: ");
        while (!pq.isEmpty()) {
            System.out.print(pq.poll() + " ");  // 1, 2, 5, 8（不是添加顺序）
        }
        System.out.println();

        // 最大堆（逆序）
        Queue<Integer> maxPq = new PriorityQueue<>((a, b) -> b - a);
        maxPq.add(5);
        maxPq.add(2);
        maxPq.add(8);
        System.out.println("最大堆出队: " + maxPq.poll());  // 8
    }
}
```

---

### 坑67：LinkedHashSet 保持插入顺序

```java
import java.util.LinkedHashSet;
import java.util.Set;

public class LinkedHashSetDemo {
    public static void main(String[] args) {
        Set<String> set = new LinkedHashSet<>();
        set.add("Zhao");
        set.add("Sun");
        set.add("Li");
        set.add("Qian");

        System.out.println("保持插入顺序: " + set);
        // 输出: [Zhao, Sun, Li, Qian]

        // 用 LinkedHashSet 实现 LRU 缓存
    }
}
```

---

### 坑68：Collections 工具类的坑

```java
import java.util.Collections;
import java.util.List;

public class CollectionsStaticDemo {
    public static void main(String[] args) {
        // Collections.max/min 要求列表非空
        // Collections.max(List.of())  // NoSuchElementException

        // synchronizedXXX 返回的集合方法都要手动同步
        // List<String> syncList = Collections.synchronizedList(new ArrayList<>());
        // 遍历时需要手动同步: synchronized(syncList) { for(String s : syncList) {...} }

        // unmodifiableXXX 返回的集合不可修改
        // List<String> unmod = Collections.unmodifiableList(new ArrayList<>());
        // unmod.add("new");  // UnsupportedOperationException
    }
}
```

---

### 坑69：List.toArray() 的类型问题

```java
import java.util.ArrayList;
import java.util.List;

public class ListToArrayDemo {
    public static void main(String[] args) {
        List<String> list = new ArrayList<>();
        list.add("A");
        list.add("B");

        // toArray() 返回 Object[]
        Object[] arr1 = list.toArray();
        System.out.println("arr1 类型: " + arr1.getClass());  // class [Ljava.lang.Object;

        // toArray(T[] a) 返回指定类型的数组
        String[] arr2 = list.toArray(new String[0]);
        System.out.println("arr2 类型: " + arr2.getClass());  // class [Ljava.lang.String;

        // 指定数组长度小于集合大小时，会创建新数组
        String[] arr3 = list.toArray(new String[100]);
        System.out.println("arr3 长度: " + arr3.length);  // 100
    }
}
```

---

### 坑70：集合和数组的相互转换

```java
import java.util.Arrays;
import java.util.List;

public class CollectionArrayConvert {
    public static void main(String[] args) {
        // 数组转 List
        String[] array = {"A", "B", "C"};

        // Arrays.asList() - 固定大小
        List<String> list1 = Arrays.asList(array);
        // list1.add("D");  // UnsupportedOperationException

        // new ArrayList<>() - 可变
        List<String> list2 = new java.util.ArrayList<>(Arrays.asList(array));
        list2.add("D");  // OK

        // List.of() - Java 9+，不可变
        List<String> list3 = List.of(array);

        // List 转数组
        List<String> list = Arrays.asList("X", "Y", "Z");
        String[] arr = list.toArray(new String[0]);
        String[] arr2 = list.toArray(String[]::new);  // 方法引用
    }
}
```

---

## 41.4 并发层面的坑（15个）

### 坑71：volatile 不保证原子性

volatile 保证可见性和有序性，但不保证原子性（如 i++）。

```java
public class VolatileDemo implements Runnable {
    // volatile 保证可见性：一个线程修改，其他线程立即看到
    private volatile boolean running = true;
    private int count = 0;

    @Override
    public void run() {
        while (running) {
            count++;  // volatile 不能保证这个操作的原子性
        }
        System.out.println("线程结束，count = " + count);
    }

    public static void main(String[] args) throws InterruptedException {
        VolatileDemo demo = new VolatileDemo();
        Thread t = new Thread(demo);
        t.start();

        Thread.sleep(1000);
        demo.running = false;  // 停止线程

        // count 可能小于 1000000，因为 i++ 不是原子操作
        System.out.println("main: running = false, count = " + demo.count);
    }
}
```

**正确做法**：使用 `AtomicInteger` 或 `synchronized`。

---

### 坑72：synchronized 加错对象

```java
public class WrongLockObject {
    // 错误：在不同对象上加锁，等于没锁
    private final Object lock1 = new Object();
    private final Object lock2 = new Object();

    public void method1() {
        synchronized (lock1) {
            // 业务逻辑1
        }
    }

    public void method2() {
        synchronized (lock2) {
            // 业务逻辑2
        }
    }

    // 正确做法：用同一个锁
    private final Object lock = new Object();

    public void correctMethod1() {
        synchronized (lock) {
            // 业务逻辑1
        }
    }

    public void correctMethod2() {
        synchronized (lock) {
            // 业务逻辑2
        }
    }
}
```

---

### 坑73：Thread.sleep 不释放锁

`sleep()` 会让线程进入 TIMED_WAITING 状态，但不会释放已持有的锁。

```java
public class SleepNoReleaseLock {
    private final Object lock = new Object();

    public void method() {
        synchronized (lock) {
            System.out.println("获得锁");
            try {
                Thread.sleep(5000);  // 睡5秒，锁还在手里
                // 其他等待这个锁的线程只能干等
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }
}
```

**替代**：使用 `wait()/notify()` 会释放锁。

---

### 坑74：wait() 必须在 synchronized 中调用

`wait()`、`notify()`、`notifyAll()` 必须先获得对象的监视器锁，否则抛 IllegalMonitorStateException。

```java
public class WaitNotifyDemo {
    private final Object lock = new Object();

    public void waitDemo() throws InterruptedException {
        // 错误写法
        // lock.wait();  // IllegalMonitorStateException!

        // 正确写法
        synchronized (lock) {
            while (someConditionNotMet()) {
                lock.wait();  // 等待并释放锁
            }
            // 继续执行
        }
    }

    public void notifyDemo() {
        synchronized (lock) {
            // 做一些准备
            lock.notify();  // 唤醒一个等待的线程
            // 或者 lock.notifyAll(); 唤醒所有
        }
    }

    private boolean someConditionNotMet() {
        return true;
    }
}
```

---

### 坑75：线程池的七大参数

```java
import java.util.concurrent.*;

public class ThreadPoolParams {
    public static void main(String[] args) {
        // 七大参数详解
        ThreadPoolExecutor executor = new ThreadPoolExecutor(
            2,                          // corePoolSize：核心线程数
            5,                          // maximumPoolSize：最大线程数
            60L,                        // keepAliveTime：多余线程存活时间
            TimeUnit.SECONDS,           // 时间单位
            new LinkedBlockingQueue<>(3),  // 任务队列
            Executors.defaultThreadFactory(),  // 线程工厂
            new ThreadPoolExecutor.AbortPolicy()  // 拒绝策略
        );

        // 拒绝策略：
        // AbortPolicy - 抛 RejectedExecutionException
        // CallerRunsPolicy - 由调用者线程执行
        // DiscardPolicy - 丢弃任务
        // DiscardOldestPolicy - 丢弃队列中最老的任务

        executor.execute(() -> System.out.println("任务执行"));
        executor.shutdown();
    }
}
```

---

### 坑76：CountDownLatch 和 CyclicBarrier 的区别

`CountDownLatch` 是倒计时门闩，只能用一次；`CyclicBarrier` 是循环栅栏，可重复使用。

```java
import java.util.concurrent.*;

public class LatchVsBarrier {
    public static void main(String[] args) throws InterruptedException {
        // CountDownLatch：等所有玩家加载完成才开始游戏
        CountDownLatch latch = new CountDownLatch(3);
        for (int i = 0; i < 3; i++) {
            new Thread(() -> {
                System.out.println("玩家加载完成");
                latch.countDown();  // 计数减1
            }).start();
        }
        latch.await();  // 等待计数为0
        System.out.println("游戏开始！");

        // CyclicBarrier：等所有玩家都到达某个点后一起继续
        CyclicBarrier barrier = new CyclicBarrier(3, () ->
            System.out.println("所有人都到了，出发！"));
        for (int i = 0; i < 3; i++) {
            new Thread(() -> {
                System.out.println("玩家到达出发点");
                try {
                    barrier.await();  // 等待其他人
                } catch (InterruptedException | BrokenBarrierException e) {
                    e.printStackTrace();
                }
            }).start();
        }
    }
}
```

---

### 坑77：Future.get() 的阻塞

`Future.get()` 会阻塞等待结果，永远不用或用错会导致线程卡住。

```java
import java.util.concurrent.*;

public class FutureGetDemo {
    public static void main(String[] args) throws Exception {
        ExecutorService executor = Executors.newSingleThreadExecutor();
        Future<Integer> future = executor.submit(() -> {
            Thread.sleep(2000);
            return 42;
        });

        System.out.println("做其他事情...");

        // future.get() 会阻塞等待结果
        Integer result = future.get();  // 阻塞2秒
        System.out.println("结果是: " + result);

        // 正确做法：用超时
        try {
            result = future.get(1, TimeUnit.SECONDS);  // 只等1秒
        } catch (TimeoutException e) {
            System.out.println("超时了！");
        }

        executor.shutdown();
    }
}
```

---

### 坑78：ThreadLocal 的内存泄漏

ThreadLocalMap 的 Entry 引用 ThreadLocal，如果 ThreadLocal 被回收，但 Entry 还存在，可能导致内存泄漏。

```java
public class ThreadLocalDemo {
    // ThreadLocal 变量
    private static final ThreadLocal<String> tl = new ThreadLocal<>();

    public static void main(String[] args) {
        tl.set("主线程值");

        Thread t = new Thread(() -> {
            tl.set("子线程值");
            System.out.println("子线程: " + tl.get());
            // 如果不 remove，子线程用完回收时可能有问题
        });

        t.start();
        t.join();

        System.out.println("主线程: " + tl.get());

        // 用完要 remove（尤其是在线程池中）
        tl.remove();
    }
}
```

---

### 坑79：死锁

两个或多个线程互相等待对方持有的锁。

```java
public class DeadLockDemo {
    private final Object lock1 = new Object();
    private final Object lock2 = new Object();

    public void method1() {
        synchronized (lock1) {
            System.out.println("method1 获得 lock1");
            try {
                Thread.sleep(100);
            } catch (InterruptedException e) {}

            synchronized (lock2) {  // 等待 lock2
                System.out.println("method1 获得 lock2");
            }
        }
    }

    public void method2() {
        synchronized (lock2) {
            System.out.println("method2 获得 lock2");
            try {
                Thread.sleep(100);
            } catch (InterruptedException e) {}

            synchronized (lock1) {  // 等待 lock1 - 可能死锁！
                System.out.println("method2 获得 lock1");
            }
        }
    }

    public static void main(String[] args) {
        DeadLockDemo demo = new DeadLockDemo();

        new Thread(demo::method1).start();
        new Thread(demo::method2).start();
    }
}
```

**避免死锁**：按固定顺序获取锁，或使用 `tryLock()` 并设置超时。

---

### 坑80：notify() 和 notifyAll() 的误用

唤醒一个线程时用 `notify()`，唤醒所有线程时用 `notifyAll()`。

```java
public class NotifyVsNotifyAll {
    private boolean condition = false;

    // notify() 只唤醒一个线程，可能唤醒错误的线程
    // notifyAll() 唤醒所有等待的线程，更安全

    public synchronized void waitForCondition() throws InterruptedException {
        while (!condition) {  // 用 while 不用 if，防止伪唤醒
            wait();
        }
        System.out.println("条件满足，继续执行");
    }

    public synchronized void signalCondition() {
        condition = true;
        notifyAll();  // 推荐使用 notifyAll()
    }
}
```

---

### 坑81：原子类不是万能的

`AtomicInteger`、`AtomicReference` 等只能保证单个操作的原子性，复合操作仍需加锁。

```java
import java.util.concurrent.atomic.AtomicInteger;

public class AtomicTrap {
    private AtomicInteger counter = new AtomicInteger(0);

    // 这个操作不是原子的！
    public void incrementNotAtomic() {
        // 虽然 get() 和 set() 各自是原子的，但中间可能被其他线程插队
        int current = counter.get();
        counter.set(current + 1);
    }

    // 正确做法：用 incrementAndGet()
    public void incrementAtomic() {
        counter.incrementAndGet();
    }

    // CAS 操作
    public void incrementWithCAS() {
        while (true) {
            int current = counter.get();
            if (counter.compareAndSet(current, current + 1)) {
                break;  // 成功就退出
            }
            // 否则重试
        }
    }
}
```

---

### 坑82：Executors 创建线程池的坑

```java
import java.util.concurrent.*;

public class ExecutorsTrap {
    public static void main(String[] args) {
        // 危险：FixedThreadPool 和 SingleThreadPool 队列无限大
        ExecutorService exec1 = Executors.newFixedThreadPool(1);  // 队列 Integer.MAX_VALUE
        // ExecutorService exec2 = Executors.newSingleThreadExecutor();

        // 危险：CachedThreadPool 线程数无上限
        // ExecutorService exec3 = Executors.newCachedThreadPool();

        // 推荐：手动创建线程池，明确参数
        ThreadPoolExecutor executor = new ThreadPoolExecutor(
            4, 4, 60L, TimeUnit.SECONDS,
            new LinkedBlockingQueue<>(100)  // 有界队列
        );

        // 或者用 abortPolicy 防止任务丢失
        executor.execute(() -> {
            // 任务
        });

        executor.shutdown();
    }
}
```

---

### 坑83：Thread.interrupt() 不是立即停止线程

`interrupt()` 只是设置中断标志，线程需要主动检查并处理。

```java
public class InterruptDemo {
    public static void main(String[] args) throws InterruptedException {
        Thread t = new Thread(() -> {
            while (!Thread.currentThread().isInterrupted()) {
                try {
                    System.out.println("工作中...");
                    Thread.sleep(1000);
                } catch (InterruptedException e) {
                    // sleep 期间被打断会抛异常并清除中断标志
                    System.out.println("被打断了！");
                    // 处理完后应该退出，或者重新设置中断标志
                    Thread.currentThread().interrupt();  // 重新设置
                    break;
                }
            }
            System.out.println("线程退出");
        });

        t.start();
        Thread.sleep(3000);
        t.interrupt();  // 设置中断标志
        t.join();
    }
}
```

---

### 坑84：守护线程的陷阱

Java 进程会在所有用户线程结束后终止，守护线程会被直接杀掉。

```java
public class DaemonThreadDemo {
    public static void main(String[] args) {
        Thread daemon = new Thread(() -> {
            while (true) {
                System.out.println("守护线程运行中...");
                try {
                    Thread.sleep(1000);
                } catch (InterruptedException e) {
                    break;
                }
            }
        });

        daemon.setDaemon(true);  // 必须在 start() 之前设置
        daemon.start();

        System.out.println("主线程开始其他工作...");
        try {
            Thread.sleep(5000);
        } catch (InterruptedException e) {}

        System.out.println("主线程结束，进程即将退出");
        // JVM 不会等待守护线程，会直接退出
    }
}
```

---

### 坑85：CompletableFuture 的坑

```java
import java.util.concurrent.*;

public class CompletableFutureDemo {
    public static void main(String[] args) throws Exception {
        // 默认使用 ForkJoinPool.commonPool()，不一定是你想要的
        CompletableFuture<String> cf = CompletableFuture.supplyAsync(() -> {
            return "Hello";
        });

        // 如果任务抛出异常，get() 会抛出 ExecutionException
        CompletableFuture<String> errorCf = CompletableFuture.supplyAsync(() -> {
            throw new RuntimeException("故意的");
        });

        try {
            errorCf.get();
        } catch (ExecutionException e) {
            System.out.println("异常: " + e.getCause());
        }

        // 正确做法：用 exceptionally 或 handle 处理异常
        CompletableFuture<String> safeCf = CompletableFuture
            .supplyAsync(() -> {
                throw new RuntimeException("错误");
            })
            .exceptionally(ex -> "默认值")
            .thenApply(s -> s.toUpperCase());

        System.out.println(safeCf.get());  // 默认值转大写
    }
}
```

---

## 41.5 异常层面的坑（10个）

### 坑86：捕获具体异常而非 Exception

```java
public class CatchSpecificException {
    public static void main(String[] args) {
        // 反面教材：捕获 Exception 太宽泛
        try {
            riskyMethod();
        } catch (Exception e) {
            // 这样会捕获所有异常，包括 RuntimeException、Error 等
            // 可能隐藏真正的 bug
        }

        // 正确做法：按具体类型捕获
        try {
            riskyMethod();
        } catch (IOException e) {
            // 处理 IO 异常
        } catch (SQLException e) {
            // 处理 SQL 异常
        } finally {
            // 释放资源
        }
    }

    private static void riskyMethod() throws IOException, SQLException {}
}
```

---

### 坑87：不要吞噬异常

```java
public class SwallowException {
    // 反面教材
    public void badMethod() {
        try {
            // 可能抛异常
        } catch (Exception e) {
            // 什么都没做，异常消失了！
            // e.printStackTrace();  // 最多打印一下日志
        }
    }

    // 正确做法
    public void goodMethod() {
        try {
            // 可能抛异常
        } catch (SpecificException e) {
            // 记录日志
            Logger.getLogger().log(Level.SEVERE, "操作失败", e);
            // 或者转换异常重新抛出
            throw new BusinessException("业务操作失败", e);
            // 或者恢复并给出默认值
        }
    }
}

class Logger {
    static java.util.logging.Logger getLogger() {
        return java.util.logging.Logger.getLogger("test");
    }
}

class SpecificException extends Exception {}
class BusinessException extends RuntimeException {
    BusinessException(String msg, Throwable cause) {
        super(msg, cause);
    }
}
```

---

### 坑88：finally 里抛异常会覆盖原异常

```java
public class FinallyException {
    public static void main(String[] args) {
        try {
            throw new RuntimeException("原始异常");
        } catch (RuntimeException e) {
            System.out.println("捕获: " + e.getMessage());
        } finally {
            // 如果这里抛异常，会覆盖原来的异常
            // throw new RuntimeException("finally 异常");
        }
    }

    // 正确做法
    public void correctApproach() {
        RuntimeException original = null;
        try {
            throw new RuntimeException("原始异常");
        } catch (RuntimeException e) {
            original = e;
        } finally {
            try {
                // 可能抛异常的代码
            } catch (Exception e) {
                if (original != null) {
                    original.addSuppressed(e);  // 把 finally 的异常加到原异常
                    throw original;
                }
                throw e;
            }
        }
    }
}
```

---

### 坑89：不要在 finally 里 return

```java
public class FinallyReturnDemo {
    public static void main(String[] args) {
        System.out.println("返回值: " + test());
    }

    public static int test() {
        try {
            return 1;
        } finally {
            // finally 里的 return 会覆盖 try 的 return
            return 2;
        }
    }
    // 输出: 返回值: 2
}
```

---

### 坑90：Checked Exception 和 Unchecked Exception

RuntimeException 及子类是未受检异常，不需要强制捕获；其他 Throwable 是受检异常，必须捕获或声明 throws。

```java
import java.io.*;

public class CheckedVsUnchecked {
    // 受检异常：必须处理
    public void readFile() throws FileNotFoundException {
        FileReader reader = new FileReader("file.txt");
    }

    // 未受检异常：可以选择捕获
    public void accessArray(int[] arr, int index) {
        // 数组越界是 RuntimeException，不需要声明 throws
        // 如果不捕获，会一直上抛直到 JVM
        System.out.println(arr[index]);
    }
}
```

---

### 坑91：自定义异常要有意义

```java
// 反面教材
class MyException extends Exception {}

// 正面教材
class InsufficientFundsException extends RuntimeException {
    private final double deficit;

    public InsufficientFundsException(double deficit) {
        super(String.format("余额不足，差 %.2f 元", deficit));
        this.deficit = deficit;
    }

    public double getDeficit() {
        return deficit;
    }
}

class Account {
    private double balance;

    public void withdraw(double amount) {
        if (amount > balance) {
            throw new InsufficientFundsException(amount - balance);
        }
        balance -= amount;
    }
}
```

---

### 坑92：异常链和根本原因

```java
public class ExceptionChaining {
    public static void main(String[] args) {
        try {
            level3();
        } catch (RuntimeException e) {
            System.out.println("顶层异常: " + e.getMessage());
            Throwable cause = e.getCause();
            while (cause != null) {
                System.out.println("  原因: " + cause.getMessage());
                cause = cause.getCause();
            }
        }
    }

    static void level3() {
        try {
            level2();
        } catch (Exception e) {
            throw new RuntimeException("业务层错误", e);  // 保留原因
        }
    }

    static void level2() throws Exception {
        level1();
    }

    static void level1() throws Exception {
        throw new Exception("根本原因：数据库连接失败");
    }
}
```

---

### 坑93：try-with-resources 自动关闭资源

```java
import java.io.*;

public class TryWithResourcesDemo {
    public static void main(String[] args) {
        // Java 7+ 推荐用法
        try (BufferedReader reader = new BufferedReader(
                new FileReader("file.txt"));
             BufferedWriter writer = new BufferedWriter(
                new FileWriter("output.txt"))) {
            // 自动关闭，即使发生异常也会关闭
            String line;
            while ((line = reader.readLine()) != null) {
                writer.write(line);
                writer.newLine();
            }
        } catch (IOException e) {
            // 只处理业务异常
            e.printStackTrace();
        }

        // 自定义资源类需要实现 AutoCloseable
    }
}

// 自定义可关闭资源
class DatabaseConnection implements AutoCloseable {
    @Override
    public void close() {
        System.out.println("关闭数据库连接");
    }
}
```

---

### 坑94：断言不是业务逻辑

断言在生产环境可能被禁用，不能依赖它做业务判断。

```java
public class AssertDemo {
    public static void main(String[] args) {
        // 默认禁用，需要 -ea 或 -enableassertions 开启
        assert args.length > 0 : "必须提供参数";

        // 正确用法：检查不应该发生的情况（内部 invariants）
        int balance = -100;  // 不应该发生
        assert balance >= 0 : "余额不能为负";

        // 错误用法：不能用于公开 API 的参数校验
        // public void withdraw(double amount) {
        //     assert amount > 0;  // 不靠谱！可能没开启断言
        // }
    }
}
```

---

### 坑95：异常匹配顺序

catch 块按顺序匹配，先捕获子类再捕获父类。

```java
public class ExceptionCatchOrder {
    public static void main(String[] args) {
        try {
            throw new FileNotFoundException("文件不存在");
        } catch (Exception e) {
            // 如果 Exception 在前面，后面的具体 catch 永远不会执行
        }

        // 正确顺序：从小到大（子类在前，父类在后）
        try {
            throw new FileNotFoundException("文件不存在");
        } catch (FileNotFoundException e) {
            // 先捕获具体的
        } catch (IOException e) {
            // 再捕获宽泛的
        } catch (Exception e) {
            // 最后兜底
        }
    }
}
```

---

## 41.6 泛型层面的坑（5个）

### 坑96：泛型类型擦除

泛型信息在编译后被擦除，运行时不认识泛型。

```java
import java.util.ArrayList;

public class TypeErasureDemo {
    public static void main(String[] args) {
        ArrayList<String> stringList = new ArrayList<>();
        ArrayList<Integer> intList = new ArrayList<>();

        // 运行时类型都是 ArrayList
        System.out.println(stringList.getClass() == intList.getClass());  // true

        // 不能这样判断
        // if (stringList instanceof ArrayList<String>)  // 编译错误！

        // 如果需要泛型的运行时类型信息
        System.out.println(stringList instanceof ArrayList<?>);  // 可以
    }
}
```

---

### 坑97：泛型不能用于基本类型

```java
public class GenericPrimitiveDemo {
    // 错误：泛型不能是基本类型
    // List<int> intList = new ArrayList<>();

    // 正确：使用包装类
    java.util.List<Integer> intList = new java.util.ArrayList<>();
    intList.add(42);  // 自动装箱

    // 获取时自动拆箱
    int val = intList.get(0);  // 自动拆箱
}
```

---

### 坑98：泛型方法

```java
public class GenericMethodDemo {
    // 泛型方法：类型参数放在返回类型之前
    public static <T> T returnFirst(T first, T second) {
        return first;
    }

    // 多个类型参数
    public static <K, V> java.util.Map<K, V> createMap(K key, V value) {
        java.util.Map<K, V> map = new java.util.HashMap<>();
        map.put(key, value);
        return map;
    }

    public static void main(String[] args) {
        // 调用时自动推断类型
        String first = returnFirst("Hello", "World");
        Integer num = returnFirst(42, 100);

        // 也可以显式指定
        String s = GenericMethodDemo.<String>returnFirst("A", "B");
    }
}
```

---

### 坑99：泛型通配符

`? extends T` 表示上界（生产者），`? super T` 表示下界（消费者）。

```java
import java.util.*;

public class WildcardDemo {
    // PECS 原则：Producer-Extends, Consumer-Super

    // 生产者：只读取数据，用 extends
    public static double sumOfList(List<? extends Number> list) {
        double sum = 0;
        for (Number n : list) {
            sum += n.doubleValue();
        }
        return sum;
    }

    // 消费者：只写入数据，用 super
    public static void addNumbers(List<? super Integer> list) {
        list.add(1);
        list.add(2);
        // list.get(0) 返回的是 Object，不是 Integer
    }

    public static void main(String[] args) {
        List<Integer> ints = Arrays.asList(1, 2, 3);
        List<Double> doubles = Arrays.asList(1.1, 2.2);

        System.out.println(sumOfList(ints));     // OK
        System.out.println(sumOfList(doubles)); // OK

        List<Number> numbers = new ArrayList<>();
        addNumbers(numbers);
        System.out.println(numbers);
    }
}
```

---

### 坑100：泛型数组

Java 不允许创建具体类型的泛型数组，但可以创建通配符数组。

```java
public class GenericArrayDemo {
    // 错误：不能 new T[]
    // public static <T> T[] createArray() {
    //     return new T[10];  // 编译错误！
    // }

    // 正确做法1：使用 Class<T>
    public static <T> T[] createArray(Class<T> clazz, int size) {
        @SuppressWarnings("unchecked")
        T[] array = (T[]) java.lang.reflect.Array.newInstance(clazz, size);
        return array;
    }

    // 正确做法2：使用 List<T>
    public static <T> List<T> createList() {
        return new ArrayList<>();
    }

    // 通配符数组（有警告）
    public static void wildcardArray() {
        // @SuppressWarnings("unchecked")
        // List<String>[] array = new List<String>[10];  // 编译错误！

        List<?>[] array = new List<?>[10];  // OK
        array[0] = Arrays.asList("A");
    }

    public static void main(String[] args) {
        String[] arr = createArray(String.class, 5);
        arr[0] = "Hello";
        System.out.println(Arrays.toString(arr));
    }
}
```

---

## 本章小结

本章汇集了 Java 初学者最常踩的 100 个坑，按语法、OOP、集合、并发、异常、泛型六个类别整理：

| 类别 | 坑的数量 | 核心要点 |
|------|----------|----------|
| 语法层面 | 30个 | 分号、字符串比较、类型转换、运算符优先级 |
| OOP层面 | 20个 | 构造链、访问修饰符、static 方法、equals/hashCode |
| 集合层面 | 20个 | 初始化容量、fail-fast、null 值、subList 视图 |
| 并发层面 | 15个 | volatile 原子性、死锁、线程池参数、ThreadLocal 泄漏 |
| 异常层面 | 10个 | 异常吞噬、finally return、try-with-resources |
| 泛型层面 | 5个 | 类型擦除、通配符 PECS、泛型数组 |

**学习建议**：

1. **动手实践**：每个坑都自己运行一遍，印象深刻
2. **理解原理**：知道"为什么错"比知道"怎么改"更重要
3. **养成习惯**：遵循最佳实践，从源头避免踩坑
4. **持续积累**：遇到新坑就记录下来，形成自己的"避坑手册"

> "纸上得来终觉浅，绝知此事要躬行。"
>
> 踩坑不可怕，可怕的是踩了同一个坑两次。希望本章能帮你少走弯路，写出更健壮的 Java 代码！

---

*下一章我们将进入 Java 高级特性的学习，敬请期待！*
