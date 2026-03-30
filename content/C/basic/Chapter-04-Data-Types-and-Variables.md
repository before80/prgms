+++
title = "第 4 章：数据类型与变量"
weight = 40
date = "2026-03-29T22:34:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 第 4 章：数据类型与变量

> "程序员的三大幻觉：栈不会溢出、整数不会负、char 永远有符号。" —— 某不愿透露姓名的 C 大师

欢迎来到 C 语言最核心的章节之一：**数据类型与变量**。

如果说 C 语言是一座大厦，那么数据类型就是这座大厦的**砖块**，而变量就是**砖块摆放的位置**。你有多少种砖，就决定了你能建多高、多漂亮房子。选错了砖块，轻则歪楼，重则塌楼（程序崩溃）。

这一章我们会从最基础的整数、浮点数讲起，一路讲到 C23 的`_BitInt`任意精度整数和十进制浮点数。内容很多，但别怕，我会用大量生活比喻让你觉得这些概念比早餐吃啥还简单。

让我们开始吧！

---

## 4.1 基本数据类型

C 语言的基本数据类型就像厨房里的调料盒，每种调料都有自己的用途。拿错了酱油倒进汤里，那汤可就毁了。

### 4.1.1 整型：`int` / `short` / `long` / `long long`

**整型**（Integer）就是没有小数点的整数——1、42、-7、0、23333，都是整型家族的一员。

想象你走进一家便利店：

- **`short`**（短整型）就像**存包柜的格子**——空间小，只能塞下小东西（范围：通常是 -32768 到 32767）
- **`int`**（整型）就像**便利店的货架**——大小中等，日常最常用（范围：通常是 -2147483648 到 2147483647）
- **`long`**（长整型）就像**仓库的货架**——比 int 能装更多
- **`long long`**（更长的整型）就像**大型物流中心的仓库**——空间巨大，能存下天文数字级别的数据

> **小知识：** 这些类型具体占多少字节，不是 C 语言规定的，而是由**实现（implementation）**决定的——也就是你的编译器 + 操作系统 + CPU 架构共同决定。你可以理解为"各地房价不同，各地字节数也不同"。想知道具体数字？include `<limits.h>` 头文件，里面有所有答案。

让我们用代码感受一下：

```c
#include <stdio.h>
#include <limits.h>  // 包含了整型的极限信息

int main(void) {
    printf("short 能装: %d ~ %d\n", SHRT_MIN, SHRT_MAX);
    // 输出: short 能装: -32768 ~ 32767

    printf("int 能装: %d ~ %d\n", INT_MIN, INT_MAX);
    // 输出: int 能装: -2147483648 ~ 2147483647

    printf("long 能装: %ld ~ %ld\n", LONG_MIN, LONG_MAX);
    // 输出: long 能装: (取决于平台)

    printf("long long 能装: %lld ~ %lld\n", LLONG_MIN, LLONG_MAX);
    // 输出: long long 能装: -9223372036854775808 ~ 9223372036854775807

    return 0;
}
```

> **生活比喻：** 把整型想象成不同大小的容器。`short`是马克杯，`int`是饮水机桶，`long`是浴缸，`long long`是游泳池。你要存多少水（数据），就选多大的容器。但注意——别用游泳池装一滴水（浪费），也别用马克杯装一吨水（装不下，溢出了）！

### 4.1.2 浮点型：`float` / `double` / `long double`

**浮点型**（Floating-point）就是带小数点的数——3.14、-0.5、6.02214076e23，都属于浮点型。

> **浮点是啥意思？** 简单说就是"小数点可以浮动的数"。比如 123.45 也可以写成 1.2345e2（科学计数法），小数点位置不固定，这就是"浮点"的含义。

- **`float`**（单精度浮点）——像普通卷尺，精度有限，能表示大约 6-7 位有效数字（C 标准保证至少 6 位不丢精度）
- **`double`**（双精度浮点）——像游标卡尺，精度更高，能表示大约 15-16 位有效数字
- **`long double`**（扩展精度浮点）——像激光测距仪，在 x86 架构上通常是 80 位扩展精度精度变态高（在某些平台上相当于 80 位，在其他平台上可能只是 double）

> **IEEE 754** 是浮点数的"交通规则"——它规定了浮点数怎么在内存里存放，怎么参与运算。大部分现代 CPU 都遵循这个标准。

```c
#include <stdio.h>
#include <float.h>  // 包含浮点型的极限信息

int main(void) {
    printf("float 能存的最小的正数: %e\n", FLT_MIN);
    // 输出: float 能存的最小的正数: 1.175494e-38

    printf("float 能存的最大数: %e\n", FLT_MAX);
    // 输出: float 能存的最大数: 3.402823e+38

    printf("float 十进制有效数字位数: %d 位\n", FLT_DIG);
    // 输出: float 十进制有效数字位数: 6 位
    // 说明：FLT_DIG=6 表示 float 可以"安全地"表示和还原最多 6 位十进制数。
    //       这不是说 float 只有 6 位有效数字——实际上 float 有约 24 位二进制尾数，
    //       折合约 7 位十进制有效数字。FLT_DIG 是用于"十进制字符串往返"的精度。

    printf("double 精度: %d 位\n", DBL_DIG);
    // 输出: double 精度: 15 位

    return 0;
}
```

> **小技巧：** 判断两个浮点数是否相等是个技术活（因为精度问题）。看个经典段子：
> - 面试官问："0.1 + 0.2 等于多少？"
> - C 程序员回答："0.30000000000000004"
> - 面试官："你被录用了"

```c
#include <stdio.h>

int main(void) {
    float a = 0.1f;
    float b = 0.2f;
    float sum = a + b;

    printf("a = %.20f\n", a);
    // 输出: a = 0.10000000149011611938

    printf("b = %.20f\n", b);
    // 输出: b = 0.20000000298023223877

    printf("sum = %.20f\n", sum);
    // 输出: sum = 0.30000001192092895508

    printf("sum == 0.3 ? %s\n", sum == 0.3f ? "Yes" : "No");
    // 输出: sum == 0.3 ? No

    // 正确做法：比较差值
    printf("fabs(sum - 0.3f) < 1e-6 ? %s\n",
           (sum - 0.3f > -1e-6 && sum - 0.3f < 1e-6) ? "Yes" : "No");
    // 输出: fabs(sum - 0.3f) < 1e-6 ? Yes

    return 0;
}
```

> **生活比喻：** 浮点数就像弹簧秤——你放上去的东西不一定是精确重量，弹簧会抖动，精度有限。所以金融计算（钱！）一般不用普通浮点数，而是用**十进制浮点**或者**定点数**。C23 引入的`_Decimal128`就是干这个的。

### 4.1.3 字符型：`char`

**字符型**（Character）——`char`，是 C 语言里最"名不副实"的数据类型。

它的名字叫"字符"，但它实际上存的是**整数**！

`char`本质上就是一个字节的整数（"一个字节"是 C 标准的最低保证，实际上可能是 8 位、16 位或更多，但现代几乎都是 8 位）。你可以把它当作 -128 到 127 的有符号数，或者 0 到 255 的无符号数来用。但同时，你也可以把它当作字符来用——比如字符`'A'`对应的 ASCII 码是 65。

```c
#include <stdio.h>

int main(void) {
    char c = 'A';
    char c2 = 65;  // 和 'A' 完全等价

    printf("c = '%c', ASCII = %d\n", c, c);
    // 输出: c = 'A', ASCII = 65

    printf("c2 = '%c', ASCII = %d\n", c2, c2);
    // 输出: c2 = 'A', ASCII = 65

    printf("sizeof(char) = %zu 字节\n", sizeof(char));
    // 输出: sizeof(char) = 1 字节

    return 0;
}
```

> **⚠️ 可移植性陷阱！** `char`到底是有符号还是无符号，**由编译器实现决定**！这是 C 语言最坑的设计之一。在某些编译器上`char`是 signed，在某些上是 unsigned。这意味着如果你写：
> ```c
> char c = 255;  // 在有符号 char 的系统上，c 会变成 -1！
> ```
> **血的教训：** 如果你需要明确的符号性，使用`signed char`或`unsigned char`，不要裸用`char`存数值！

```c
#include <stdio.h>

int main(void) {
    // 明确指定有符号/无符号
    signed char sc = -1;
    unsigned char uc = 255;

    printf("signed char: %d\n", sc);
    // 输出: signed char: -1

    printf("unsigned char: %u\n", uc);
    // 输出: unsigned char: 255

    // char 本身的符号性不确定，千万别当数值用！
    return 0;
}
```

> **生活比喻：** `char`就像一个万能插座——既可以插冰箱（存字符），也可以接电热毯（存数值）。但到底是 110V 还是 220V，由你买的插座（编译器）决定。所以买插座前一定要问清楚（查文档）！

### 4.1.4 布尔型：`_Bool` / `bool`

C 语言诞生于 1972 年，那时候还没有"布尔"这个概念——因为发明者 Dennis Ritchie 可能觉得"Yes/No"太简单了，不如直接用整数！

所以 C 语言里，**0 表示假，非 0 表示真**。这种设计至今仍影响着 C 和 C++。

直到 **C99** 标准，才引入了原生的布尔类型：`_Bool`。

```c
#include <stdio.h>
#include <stdbool.h>  // C99 引入，提供 bool / true / false 宏

int main(void) {
    _Bool b1 = true;
    _Bool b2 = false;

    printf("b1 = %d, b2 = %d\n", b1, b2);
    // 输出: b1 = 1, b2 = 0

    // 使用更友好的名字（通过宏实现）
    bool b3 = true;
    bool b4 = false;

    printf("b3 = %d, b4 = %d\n", b3, b4);
    // 输出: b3 = 1, b4 = 0

    // C 语言传统写法（至今仍然有效）
    if (42) {
        printf("42 是真的（因为非 0）\n");
        // 输出: 42 是真的（因为非 0）
    }

    if (!0) {
        printf("0 是假的\n");
        // 输出: 0 是假的
    }

    return 0;
}
```

> **历史注记：** C99 引入`<stdbool.h>`时，`bool`/`true`/`false`只是**宏**（#define），不是真正的关键字。从 **C23** 开始，它们才正式成为关键字，地位稳固。如果你看到`bool x = true;`，这在 C23 里就是原生语法，不再是宏替换。

> **生活比喻：** 布尔值就像电灯开关——只有两种状态：开（true/1）或关（false/0）。C 语言里的"非 0 即真"就像说"除了关着的都是开着的"，虽然有点粗糙，但道理是一样的。

### 4.1.5 `void` 类型

`void`是 C 语言里最特别的存在——它表示"**没有类型**"或"**空**"。

`void`的用途有三种：

**1. 函数无返回值**

```c
#include <stdio.h>

void say_hello(void) {
    printf("你好，世界！\n");
    // 注意：这里不能写 return 0; 因为函数返回类型是 void
    return;  // 只能写 return; 或者直接省略 return
}

int main(void) {
    say_hello();
    // 输出: 你好，世界！
    return 0;
}
```

**2. 通用指针（指向未知类型）**

```c
#include <stdio.h>

int main(void) {
    int n = 42;
    void *ptr = &n;  // void* 可以指向任何类型

    // 使用前必须强制转换
    printf("n = %d\n", *(int *)ptr);
    // 输出: n = 42

    double d = 3.14;
    ptr = &d;  // void* 也能指向 double
    printf("d = %f\n", *(double *)ptr);
    // 输出: d = 3.140000

    return 0;
}
```

**3. sizeof 不适用于 void**

```c
// 下面的代码是无法编译的！
// printf("%zu", sizeof(void));  // 错误：sizeof 不能用于 void
```

> **生活比喻：** `void`就像"隐形斗篷"——它存在，但你看不见它的具体形状。你可以说"这有个东西"（void* 指针），但你不知道它是什么类型、大小多少。用于函数时，它表示"这个函数不返回任何东西"——就像一个不返回的漂流瓶。

---

## 4.2 有符号 vs 无符号

这是 C 语言里最容易出 bug 的知识点之一，请认真阅读！

**有符号（signed）** 类型可以表示正数、负数和零；**无符号（unsigned）** 类型只能表示零和正数。

| 类型 | 范围（假设 8 位） | 能表示负数吗？ |
|------|------------------|--------------|
| signed char | -128 ~ 127 | ✅ |
| unsigned char | 0 ~ 255 | ❌ |

```c
#include <stdio.h>
#include <limits.h>

int main(void) {
    signed char sc = -1;
    unsigned char uc = 255;

    printf("signed char: %d\n", sc);
    // 输出: signed char: -1

    printf("unsigned char: %u\n", uc);
    // 输出: unsigned char: 255

    // 如果都用 %d（按有符号打印）
    printf("uc as signed: %d\n", (signed char)uc);
    // 输出: uc as signed: -1（因为 255 的二进制在有符号解释下是 -1）

    // 无符号类型的用途：位运算、计数器、掩码
    unsigned int flags = 0xFF;  // 0xFF = 255，常用于位掩码
    printf("flags = 0x%X\n", flags);
    // 输出: flags = 0xFF

    return 0;
}
```

> **重要警告：** 当有符号数和无符号数混合运算时，C 语言会自动进行**隐式类型转换**——有符号数会被转换成无符号数！这可能导致意外结果：
>
> ```c
> #include <stdio.h>
>
> int main(void) {
>     int n = -1;
>     unsigned int u = 10;
>
>     if (n < u) {
>         printf("-1 < 10（这是对的）\n");
>     } else {
>         printf("-1 >= 10？\n");
>     }
>     // 实际输出：无符号转换后，-1 变成了最大的无符号整数，10 比较小
>     // 所以会输出：-1 >= 10
>     // 输出: -1 >= 10
>
>     return 0;
> }
> ```

> **生活比喻：** 有符号数就像温度计——可以显示零下（负数）和零上（正数）。无符号数就像计数器——只能从 0 开始往上数，不能倒数。如果温度计坏了（溢出），零下 10 度可能显示成零上 280 度；如果计数器从 0 再减，就可能突然变成 4 亿（取决于位数）。这就是为什么嵌入式开发里位运算常用无符号数。

---

## 4.3 `sizeof` 运算符

`sizeof`是 C 语言里的"量尺"——它告诉你一个类型或变量占用多少字节。

**重要的事情说三遍：`sizeof`是运算符，不是函数！不是函数！不是函数！**

```c
#include <stdio.h>

int main(void) {
    // sizeof 的用法一：sizeof(类型)
    printf("sizeof(int) = %zu\n", sizeof(int));
    // 输出: sizeof(int) = 4（在大多数 32/64 位系统上）

    // sizeof 的用法二：sizeof(表达式/变量)
    int x = 100;
    printf("sizeof(x) = %zu\n", sizeof(x));
    // 输出: sizeof(x) = 4

    // sizeof 的高级用法：sizeof 数组（在数组作用域内）
    int arr[] = {1, 2, 3, 4, 5};
    printf("sizeof(arr) = %zu\n", sizeof(arr));
    // 输出: sizeof(arr) = 20（5个int × 4字节 = 20）

    // 算数组元素个数
    int count = sizeof(arr) / sizeof(arr[0]);
    printf("数组元素个数: %d\n", count);
    // 输出: 数组元素个数: 5

    printf("sizeof(double) = %zu\n", sizeof(double));
    // 输出: sizeof(double) = 8

    printf("sizeof(long long) = %zu\n", sizeof(long long));
    // 输出: sizeof(long long) = 8

    return 0;
}
```

> **小技巧：** `%zu`是`sizeof`返回类型`size_t`对应的格式说明符。在老代码里你可能看到`%lu`和`(unsigned long)`的组合，但`%zu`是 C99 标准的正确写法。

> **生活比喻：** `sizeof`就像问"这个箱子占多大地方"——问 int 这个箱子占 4 个格子，问 double 占 8 个格子，问你的行李箱占多少取决于里面塞了多少东西（变量）。它不执行任何代码，只是"看看大小"。

---

## 4.4 常量：`const`、`#define`、`enum`

### 4.4.1 `const` 限定符

`const`（constant，常量）修饰的变量，意思是"**我只读不动**"——初始化后就不能再改了。

```c
#include <stdio.h>

int main(void) {
    const int MAX_RETRY = 3;  // 最大重试次数，不会变
    const double PI = 3.14159265358979;  // 圆周率

    printf("最大重试次数: %d\n", MAX_RETRY);
    // 输出: 最大重试次数: 3

    printf("PI ≈ %.15f\n", PI);
    // 输出: PI ≈ 3.141592653589790

    // 下面这行如果取消注释，编译会报错！
    // MAX_RETRY = 5;  // 错误：向只读变量 MAX_RETRY 赋值

    return 0;
}
```

> **注意：** `const`修饰的并不是"真正的常量"，而是"只读变量"。编译器会在编译时报错，但如果你绕弯子（比如通过指针），还是可以在运行时修改它。所以`const`更多是一种**代码意图的表达**和**编译期检查**，而不是硬件级别的保护。

### 4.4.2 `#define` 宏常量

`#define`是**预处理器指令**，在编译前就把名字替换成实际内容。没有类型，不占内存，纯粹是"复制粘贴"。

```c
#include <stdio.h>

#define MAX_RETRY 3          // 整数常量
#define PI 3.14159265358979  // 浮点常量
#define NAME "Tom"           // 字符串常量
#define NEWLINE '\n'         // 字符常量

int main(void) {
    printf("最大重试次数: %d\n", MAX_RETRY);
    // 输出: 最大重试次数: 3

    printf("PI ≈ %.15f\n", PI);
    // 输出: PI ≈ 3.141592653589790

    printf("你好，%s！%c", NAME, NEWLINE);
    // 输出: 你好，Tom！

    return 0;
}
```

> **const vs #define 的区别：**
> - `#define`：纯文本替换，没有类型，没有地址，可能产生多个副本（如果用在多个文件）
> - `const`：有类型，是真正的变量（只不过只读），占用内存，有地址
>
> 一般来说，简单的宏用`#define`，复杂一点的推荐用`const`或`enum`。

### 4.4.3 `enum` 枚举常量

`enum`（enumeration，枚举）是一种创建**命名整数常量**的方式，比一堆`#define`优雅得多。

```c
#include <stdio.h>

// 定义枚举类型，值默认从 0 开始递增
enum Color {
    RED,    // 0
    GREEN,  // 1
    BLUE    // 2
};

// 也可以手动指定值
enum Weekday {
    MONDAY = 1,   // 从 1 开始
    TUESDAY,      // 2
    WEDNESDAY,    // 3
    THURSDAY,     // 4
    FRIDAY,       // 5
    SATURDAY,     // 6
    SUNDAY        // 7
};

enum { MAX_BUFFER_SIZE = 1024 };  // 匿名枚举，直接创建一个整型常量（不是变量！）

int main(void) {
    enum Color c = RED;
    printf("RED = %d, GREEN = %d, BLUE = %d\n", RED, GREEN, BLUE);
    // 输出: RED = 0, GREEN = 1, BLUE = 2

    enum Weekday today = FRIDAY;
    printf("今天星期%d\n", today);
    // 输出: 今天星期5

    printf("最大缓冲区: %d 字节\n", MAX_BUFFER_SIZE);
    // 输出: 最大缓冲区: 1024 字节

    return 0;
}
```

> **生活比喻：** `enum`就像给你的一叠便签贴上名字——"这是第一张便签"、"这是第二张"...比每次说"编号为 2 的那个"方便多了。枚举让代码可读性大增：`today == FRIDAY`比`today == 5`好懂一万倍！

---

## 4.5 字面量后缀

字面量（Literal）就是代码里直接写出来的值，比如`42`、`3.14`、`'A'`。

后缀（Suffix）的作用是**明确告诉编译器这个字面量的类型**，避免隐式转换带来的麻烦。

```c
#include <stdio.h>

int main(void) {
    // 整数字面量后缀
    int a = 42;           // 默认是 int
    long b = 42L;         // 加 L 表示 long
    long long c = 42LL;   // 加 LL 表示 long long
    unsigned int d = 42U; // 加 U 表示 unsigned
    unsigned long e = 42UL; // U 和 L 可以组合

    // 浮点字面量后缀
    float f = 3.14f;      // 加 f 表示 float（否则是 double）
    double g = 3.14;      // 默认是 double
    long double h = 3.14L; // 加 L 表示 long double

    printf("a=%d, b=%ld, c=%lld\n", a, b, c);
    // 输出: a=42, b=42, c=42

    printf("f=%.2f, g=%.2f, h=%.2Lf\n", f, g, h);
    // 输出: f=3.14, g=3.14, h=3.14

    // 十六进制 + 后缀
    unsigned int hex = 0xFFU;  // 255U
    printf("hex = %u\n", hex);
    // 输出: hex = 255

    return 0;
}
```

> **小技巧：** 整数字面量的类型由**值**和**后缀**共同决定：
> - `42` → `int`（值太小，直接用 int）
> - `42U` / `42u` → `unsigned int`
> - `42L` / `42l` → `long`
> - `42LL` / `42ll` → `long long`
> - `42UL` / `42LU` → `unsigned long`（U 和 L 可以组合）
> - `42ULL` → `unsigned long long`
>
> 浮点字面量：
> - `3.14` → `double`（默认！）
> - `3.14f` / `3.14F` → `float`
> - `3.14L` / `3.14l` → `long double`
>
> ⚠️ **新手常犯的错误：** 以为 `3.14` 可以直接赋给 `float`——错！`float f = 3.14;` 虽然能编译（因为 double 会自动缩窄），但会有**精度警告**。正确写法是 `float f = 3.14f;`，加那个 `f` 后缀！

> **C23 新增：** C23 引入了二进制字面量（`0b`前缀）和更明确的后缀组合，比如`0b1010ULL`表示无符号长长整型的二进制值 1010。

---

## 4.6 进制表示

C 语言支持四种进制表示法，就像你可以在不同地区用不同单位制（英制/公制）：

| 进制 | 前缀 | 示例 | 人类友好度 |
|------|------|------|----------|
| 十进制 | 无 | `42` | ⭐⭐⭐⭐⭐ |
| 八进制 | `0` | `052` | ⭐⭐ |
| 十六进制 | `0x` | `0x2A` | ⭐⭐⭐⭐ |
| 二进制 | `0b`（C23） | `0b101010` | ⭐⭐⭐⭐⭐ |

```c
#include <stdio.h>

int main(void) {
    int dec = 42;
    int oct = 052;       // 前面加 0 表示八进制，052 = 5×8 + 2 = 42
    int hex = 0x2A;      // 0x 表示十六进制，2A = 2×16 + 10 = 42
    int bin = 0b101010;  // C23 新增！二进制，42

    printf("dec=%d, oct=%d, hex=%d, bin=%d\n", dec, oct, hex, bin);
    // 输出: dec=42, oct=42, hex=42, bin=42

    // printf 可以用 %o 输出八进制，%x 输出十六进制
    printf("42 的八进制: %o\n", 42);
    // 输出: 42 的八进制: 52

    printf("42 的十六进制: %x\n", 42);
    // 输出: 42 的十六进制: 2a

    // %X 是大写版本
    printf("42 的十六进制(大写): %X\n", 42);
    // 输出: 42 的十六进制(大写): 2A

    // C23 二进制输出（需要手动转换或用库函数）
    // printf 没有原生的二进制格式，需要自己写函数
    printf("42 的二进制表示需要库函数或手写循环\n");

    return 0;
}
```

> **为什么 C23 才加二进制？** 因为在嵌入式开发、位操作、网络协议等领域，二进制字面量非常有用。以前要写`0b101010`得用十六进制`0x2A`或者宏`#define B(x) ((x/1000*8+x/100%10*4+x/10%10*2+x%10) /* 粗暴转换 */`，很不优雅。

> **生活比喻：** 四种进制就像四种语言——说"四十二"、"fifty-two"、"二八"、"二 A"，都指同一个数。编译器是个精通四国语言的翻译，你写啥它都能听懂。

---

## 4.7 隐式类型转换

C 语言会在某些情况下**自动"变身"**数据类型，这个过程叫做**隐式类型转换**（Implicit Conversion）。

这就像你妈让你去买"一斤鸡蛋"，你理解成一斤（重量），但她实际想要的是一盒（数量）——虽然单位不同，但你还是把蛋买回来了，只是一路上可能会有点小麻烦。

隐式转换发生在三种情况：

### 4.7.1 整型提升

**整型提升**（Integer Promotion）：比`int`小的类型（`char`、`short`）在进行运算时，会自动提升为`int`或`unsigned int`。

```c
#include <stdio.h>

int main(void) {
    char c1 = 100;
    char c2 = 50;
    char c3 = c1 + c2;  // char 会被提升为 int 再运算

    printf("c3 = %d\n", c3);
    // 输出: c3 = 150

    // 陷阱：如果 char 是有符号且范围是 -128~127
    signed char sc1 = 100;
    signed char sc2 = 100;
    signed char sc3 = sc1 + sc2;  // 提升为 int，100+100=200，但 char 存不下，变成 -56
    printf("sc3 = %d (应该是 200，但 char 存不下！)\n", sc3);
    // 输出: sc3 = -56 (惊不惊喜，意不意外)

    return 0;
}
```

### 4.7.2 寻常算术转换

**寻常算术转换**（Usual Arithmetic Conversions）：当两个不同类型进行运算时，较小的类型会自动转换成较大的类型。

```c
#include <stdio.h>

int main(void) {
    int i = 10;
    double d = 3.14;

    // int 会自动提升为 double，结果是 double
    double result = i + d;
    printf("i + d = %f\n", result);
    // 输出: i + d = 13.140000

    // int / int = int（小数部分被丢弃！）
    printf("10 / 3 = %d\n", 10 / 3);
    // 输出: 10 / 3 = 3（不是 3.333！）

    // 想要浮点结果，至少有一个操作数是浮点
    printf("10.0 / 3 = %f\n", 10.0 / 3);
    // 输出: 10.0 / 3 = 3.333333

    printf("10 / 3.0 = %f\n", 10 / 3.0);
    // 输出: 10 / 3.0 = 3.333333

    return 0;
}
```

> **常见错误：** `int a = 5, b = 2; double c = a / b;` → c = 2.0 而不是 2.5！因为两个 int 相除还是 int。

### 4.7.3 默认实参提升

**默认实参提升**（Default Argument Promotions）：在可变参数函数（如`printf`、`scanf`）中，`char`/`short`会自动提升为`int`，`float`会提升为`double`。

```c
#include <stdio.h>

int main(void) {
    char c = 'A';
    short s = 100;
    float f = 3.14f;

    // printf 会自动提升，所以可以直接传
    printf("%c %d %f\n", c, s, f);
    // 输出: A 100 3.140000

    return 0;
}
```

---

## 4.8 显式类型转换（强制类型转换）

**显式类型转换**（Explicit Conversion）也叫**强制类型转换**（Cast），就是明明白白告诉编译器："我要把这个数从 A 类型变成 B 类型，别废话。"

语法：`(目标类型)表达式`

```c
#include <stdio.h>

int main(void) {
    int total = 17;
    int count = 5;

    // 强转：把 int 转成 double
    double avg = (double)total / count;
    printf("平均值 = %f\n", avg);
    // 输出: 平均值 = 3.400000

    // 不强转（两个 int 相除）
    double avg2 = total / count;
    printf("错误平均值 = %f\n", avg2);
    // 输出: 错误平均值 = 3.000000

    // 常见用途：抑制警告
    void *ptr = (void *)0x1234;  // 把整数字面量强转为指针
    printf("ptr = %p\n", ptr);
    // 输出: ptr = 0x1234

    // 指针类型互转
    int n = 42;
    char *cp = (char *)&n;
    printf("n 的第一个字节 = 0x%X\n", (unsigned char)*cp);
    // 输出: n 的第一个字节 = 0x2A（小端序）

    return 0;
}
```

> **生活比喻：** 强制类型转换就像改装车——你把吉姆尼（微型车）的发动机拆下来装到大发（另一微型车）里。技术上可行，但你要清楚自己在干啥，别装错了接口（C 类型不匹配可能导致未定义行为）。

---

## 4.9 `typedef`：给类型起别名

`typedef`（Type Definition）就是给类型起**外号**。北京人叫"故宫"也喊"紫禁城"，叫法不同，东西一样。

```c
#include <stdio.h>
#include <stdint.h>

// 给 int 起个外号
typedef int Integer;
typedef unsigned int UInteger;

// 给复杂类型起个好记的名字
typedef double Speed;
typedef double Distance;

// C99 风格：可以写成类似变量的样子（更直观）
typedef int32_t Int32;
typedef uint64_t Uint64;

int main(void) {
    Integer x = 100;
    UInteger y = 200;
    Speed v = 120.5;  // 时速 120.5
    Distance d = 500.0;  // 距离 500.0

    printf("x = %d, y = %u\n", x, y);
    // 输出: x = 100, y = 200

    printf("速度 = %.1f, 距离 = %.1f\n", v, d);
    // 输出: 速度 = 120.5, 距离 = 500.0

    Int32 big_num = 1234567890;
    Uint64 huge_num = 18446744073709551615ULL;

    printf("big_num = %d\n", big_num);
    // 输出: big_num = 1234567890

    return 0;
}
```

> **typedef vs #define 的区别：**
> - `#define`是纯文本替换，没有类型检查
> - `typedef`是类型别名，有类型检查，更安全
>
> ```c
> #define PCHAR char *
> typedef char *TPCHAR;
>
> PCHAR p1, p2;  // p1 是 char*，但 p2 只是 char！（define 不会让 p2 变成指针）
> TPCHAR p3, p4; // p3 和 p4 都是 char*（typedef 正确处理了）
> ```

> **生活比喻：** `typedef`就像给人取小名——"王小明"的小名是"明明"，叫哪个都是指同一个人。但"明明"这个名字比"王小明"更好记、更亲切。给复杂类型起小名，代码更好读。

---

## 4.10 固定宽度整数类型（`<stdint.h>`）

这是 C99 引入的重要头文件，专门解决"**这个 int 到底占几个字节**"的可移植性问题。

在`<limits.h>`里你可以看到，int 在某些平台上是 16 位（老古董），在另一些上是 32 位或 64 位。这让跨平台代码头疼不已。

`<stdint.h>`提供了一套**固定宽度的类型别名**，无论在什么平台上，`int32_t`永远是你认识的**32 位有符号整数**。

### 4.10.1 精确宽度类型

**精确宽度**（Exact Width）：精准到 bit 的类型。

```c
#include <stdio.h>
#include <stdint.h>

int main(void) {
    int8_t i8 = -1;      // 精准 8 位有符号
    int16_t i16 = 42;    // 精准 16 位有符号
    int32_t i32 = 123456; // 精准 32 位有符号
    int64_t i64 = 9876543210LL; // 精准 64 位有符号

    uint8_t u8 = 255;    // 精准 8 位无符号
    uint32_t u32 = 4000000000U; // 精准 32 位无符号

    printf("i8=%d, i16=%d, i32=%d, i64=%lld\n", i8, i16, i32, i64);
    // 输出: i8=-1, i16=42, i32=123456, i64=9876543210

    printf("u8=%u, u32=%u\n", u8, u32);
    // 输出: u8=255, u32=4000000000

    return 0;
}
```

### 4.10.2 最小宽度类型

**最小宽度**（Least Width）：保证**至少**有这么宽的类型。

```c
#include <stdio.h>
#include <stdint.h>

int main(void) {
    int_least8_t l8 = 127;    // 至少 8 位
    int_least16_t l16 = 1000; // 至少 16 位
    int_least32_t l32 = 100000; // 至少 32 位
    int_least64_t l64 = 10000000000LL; // 至少 64 位

    printf("int_least32_t 能存的最小正数: %jd\n", (intmax_t)INT_LEAST32_MIN);
    printf("int_least32_t 能存的最大正数: %jd\n", (intmax_t)INT_LEAST32_MAX);

    return 0;
}
```

### 4.10.3 最快宽度类型

**最快宽度**（Fast Width）：选择**运算最快**的宽度。编译器会选择最适合 CPU 字长的类型。

```c
#include <stdio.h>
#include <stdint.h>

int main(void) {
    int_fast8_t f8 = 100;
    int_fast16_t f16 = 1000;
    int_fast32_t f32 = 100000;
    int_fast64_t f64 = 10000000000LL;

    printf("int_fast8_t 大小: %zu 字节\n", sizeof(int_fast8_t));
    printf("int_fast16_t 大小: %zu 字节\n", sizeof(int_fast16_t));
    printf("int_fast32_t 大小: %zu 字节\n", sizeof(int_fast32_t));
    printf("int_fast64_t 大小: %zu 字节\n", sizeof(int_fast64_t));

    return 0;
}
```

> **什么时候用哪种？**
> - 需要**精确字节数**（网络协议、文件格式）→ 用 `intN_t`
> - 只要求**够用就行**（一般存储）→ 用 `int_leastN_t`
> - 追求**最快速度**（大量计算）→ 用 `int_fastN_t`

### 4.10.4 指针相关宽度类型

**指针相关宽度**（Pointer-related Width）：用于存储指针值。

```c
#include <stdio.h>
#include <stdint.h>

int main(void) {
    int n = 42;
    int *ptr = &n;

    // intptr_t：能完整存储指针值的整数类型（可以安全地在指针和整数之间互转）
    intptr_t iptr = (intptr_t)ptr;
    uintptr_t uptr = (uintptr_t)ptr;

    printf("指针地址: %p\n", (void *)ptr);
    // 输出: 指针地址: 0x...（具体值）

    printf("intptr_t 值: %jd\n", (intmax_t)iptr);
    // 输出: intptr_t 值: （对应地址的整数值，64位系统上是一个大整数）
    // 注意：这里转成 intmax_t 再用 %jd 打印，是跨平台安全做法。
    //       切勿在 64 位 Windows 上把 intptr_t 强制转成 long 再用 %ld 打印！
    //       因为 Windows 上 long 只有 32 位，而 intptr_t 是 64 位，会截断成错误的值。

    printf("指针转回整数再转回指针: %p\n",
           (void *)(intptr_t)iptr);
    // 输出: 指针转回整数再转回指针: 0x...（同样地址）

    return 0;
}
```

> **用途：** 主要用于需要把指针当整数存储的场景，比如哈希计算、调试输出、或者某些需要指针算术运算的情况。

### 4.10.5 最宽整数类型

**最宽整数**（Widest Integer）：C 标准里能表示的最大整数类型。

```c
#include <stdio.h>
#include <stdint.h>

int main(void) {
    intmax_t imax = 9223372036854775807LL;  // long long 的最大值
    uintmax_t uimax = 18446744073709551615ULL; // unsigned long long 的最大值

    printf("intmax_t 最大值: %jd\n", imax);
    // 输出: intmax_t 最大值: 9223372036854775807

    printf("uintmax_t 最大值: %ju\n", uimax);
    // 输出: uintmax_t 最大值: 18446744073709551615

    return 0;
}
```

### 4.10.6 `<inttypes.h>`：格式转换宏

`<inttypes.h>`为固定宽度类型提供了**跨平台安全**的 printf/scanf 格式宏。

> **为什么需要？** 因为在 32 位系统上`int32_t`是`int`，格式是`%d`；但在 64 位 Windows 上`int32_t`是`long`，格式是`%ld`！`inttypes.h`解决了这个可移植性噩梦。

```c
#include <stdio.h>
#include <stdint.h>
#include <inttypes.h>

int main(void) {
    int32_t i32 = -12345;
    int64_t i64 = -123456789012345LL;
    uint32_t u32 = 4000000000U;
    uint64_t u64 = 18446744073709551615ULL;

    // 使用 PRId32/PRId64 等宏进行安全打印
    printf("int32_t: %" PRId32 "\n", i32);
    // 输出: int32_t: -12345

    printf("int64_t: %" PRId64 "\n", i64);
    // 输出: int64_t: -123456789012345

    printf("uint32_t: %" PRIu32 "\n", u32);
    // 输出: uint32_t: 4000000000

    printf("uint64_t: %" PRIu64 "\n", u64);
    // 输出: uint64_t: 18446744073709551615

    // 扫描输入也一样安全
    int32_t scanned;
    sscanf("12345", "%" SCNd32, &scanned);
    printf("扫描得到: %" PRId32 "\n", scanned);
    // 输出: 扫描得到: 12345

    return 0;
}
```

> **规则：** printf 用 `PRI*`，scanf 用 `SCN*`，后面跟类型宽度（8/16/32/64）。
>
> 常见宏：`PRId32`、`PRIu32`、`PRId64`、`PRIx32`（十六进制）...

---

## 4.11 重要类型别名

C 标准库定义了几个"出场率极高"的类型别名，理解它们对写出正确的 C 代码至关重要。

### 4.11.1 `size_t`

**`size_t`**（size type）—— 无符号整数类型，用于表示**大小**和**索引**。

- `sizeof`的返回类型就是`size_t`
- 数组下标最好用`size_t`
- `strlen`返回`size_t`

```c
#include <stdio.h>
#include <string.h>

int main(void) {
    const char *s = "Hello, C语言！";

    size_t len = strlen(s);
    printf("字符串长度: %zu\n", len);
    // 输出: 字符串长度: 13（一个汉字占 3 字节，这里只统计字节数）

    printf("sizeof(size_t) = %zu 字节\n", sizeof(size_t));
    // 在 64 位系统上输出: sizeof(size_t) = 8 字节

    // 循环用 size_t 作为索引
    for (size_t i = 0; i < len; i++) {
        printf("%c", s[i]);
    }
    printf("\n");
    // 输出: Hello, C语言！

    return 0;
}
```

### 4.11.2 `ptrdiff_t`

**`ptrdiff_t`**（pointer difference）—— 有符号整数类型，用于表示**两个指针之间的差距**。

```c
#include <stdio.h>
#include <stddef.h>

int main(void) {
    int arr[] = {10, 20, 30, 40, 50};
    int *p1 = &arr[1];  // 指向 20
    int *p2 = &arr[4];  // 指向 50

    ptrdiff_t diff = p2 - p1;
    printf("p2 - p1 = %td\n", diff);
    // 输出: p2 - p1 = 3

    // 指针减法返回 ptrdiff_t
    printf("指针间距: %td 个元素\n", diff);
    // 输出: 指针间距: 3 个元素

    return 0;
}
```

### 4.11.3 `wchar_t`

**`wchar_t`**（wide character）—— 宽字符类型，用于表示**Unicode 字符**。

普通`char`只能表示 ASCII 字符（一个字节），而`wchar_t`通常能表示更宽的字符（Windows 上是 16 位，Linux 上是 32 位）。

```c
#include <stdio.h>
#include <wchar.h>
#include <locale.h>

int main(void) {
    // 设置本地化（让 wprintf 能正确输出中文）
    setlocale(LC_ALL, "");

    wchar_t chinese[] = L"你好，世界！";
    wprintf(L"宽字符字符串: %ls\n", chinese);
    // 输出: 宽字符字符串: 你好，世界！

    printf("wchar_t 大小: %zu 字节\n", sizeof(wchar_t));
    // 在 Windows 64 位上输出: wchar_t 大小: 2 字节
    // 在 Linux 64 位上输出: wchar_t 大小: 4 字节

    return 0;
}
```

### 4.11.4 `max_align_t`

**`max_align_t`** —— 对齐要求最严格的基本类型，用于确定**内存对齐的基准**。

```c
#include <stdio.h>
#include <stddef.h>

int main(void) {
    printf("max_align_t 对齐要求: %zu 字节\n", alignof(max_align_t));
    // 输出: max_align_t 对齐要求: 16 字节（在大多数 64 位系统上）

    return 0;
}
```

---

## 4.12 存储类别与 linkage

（详见第 4B 章）

> 第 4B 章将深入讲解**存储期**（storage duration）、**链接**（linkage）、`static`、`extern`、`register`等概念。这些是变量"生命周期"和"可见性"的核心。

---

## 4.13 `_Atomic` 类型限定符

（详见第 4C 章）

> 第 4C 章将介绍 C11 引入的**原子操作**，用于多线程编程中避免数据竞争（data race），实现无锁算法。

---

## 4.14 `_Alignas` / `_Alignof`（C11）

C11 引入了两个下划线开头的关键字，用于**控制对齐**（alignment）。

**对齐**是什么？简单说就是数据在内存里的"门牌号"必须是某个数的倍数。比如 4 字节对齐意味着地址必须是 4 的倍数。

```c
#include <stdio.h>
#include <stdalign.h>

int main(void) {
    // alignof 返回类型的对齐要求
    printf("alignof(int) = %zu\n", alignof(int));
    // 输出: alignof(int) = 4（在大多数系统上）

    printf("alignof(double) = %zu\n", alignof(double));
    // 输出: alignof(double) = 8（在大多数系统上）

    printf("alignof(char) = %zu\n", alignof(char));
    // 输出: alignof(char) = 1

    // alignas 指定对齐要求
    alignas(16) char c;  // 让 char c 使用 16 字节对齐
    printf("c 的地址模 16 = %zu\n", (size_t)&c % 16);
    // 输出: c 的地址模 16 = 0

    // 常见的对齐用法：结构体对齐
    struct AlignedStruct {
        alignas(8) double a;
        alignas(4) int b;
    };

    printf("AlignedStruct 大小: %zu\n", sizeof(struct AlignedStruct));
    // 对齐后可能比未对齐时大

    return 0;
}
```

> **用途：** 在 SIMD（单指令多数据）指令、网络协议解析、硬件驱动等场景下，内存对齐至关重要。不对齐的数据访问可能导致性能下降甚至硬件异常。

---

## 4.15 C23 `_BitInt`（任意精度整数）

C23 最大的新特性之一——**`_BitInt`**允许你声明任意位宽的整数，不再受限于 8/16/32/64。

```c
#include <stdio.h>
#include <stdint.h>

int main(void) {
    // C23 新特性：_BitInt(N) 表示恰好 N 位的整数
    // 注意：这是 C23 特性，需要支持 C23 的编译器

    _BitInt(7) nibble;    // 7 位有符号整数（范围 -64 ~ 63）
    unsigned _BitInt(8) byte;  // 8 位无符号整数（范围 0 ~ 255）

    nibble = 63;
    byte = 255;

    printf("nibble = %d\n", nibble);
    // 输出: nibble = 63

    printf("byte = %u\n", byte);
    // 输出: byte = 255

    // 超大整数
    _BitInt(1024) big;  // 1024 位整数！
    big = 1;
    for (int i = 0; i < 1023; i++) {
        big *= 2;  // 计算 2^1023
    }
    // _BitInt_max(N) 宏返回 N 位有符号 _BitInt 类型能表示的最大值
    _BitInt(1024) max_val = _BitInt_max(1024);
    printf("1024 位整数的最大值位数验证: %d\n", 1024);
    printf("big = 2^1023（这是一个约 309 位的十进制数，循环乘了 1023 次）\n");
    // _BitInt 在大数计算、密码学等领域非常有用

    return 0;
}
```

> **注意：** `_BitInt`是 C23 的新特性写作本书时（2025年），主流编译器（GCC 14+、Clang 18+）已支持，但需要加`-std=c23`编译参数。

---

## 4.16 C23 `_Decimal32` / `_Decimal64` / `_Decimal128`

这是 C23 引入的**十进制浮点类型**，基于 IEEE 754-2019 标准。

> **为什么需要十进制浮点？** 传统的二进制浮点数（如`float`、`double`）在表示十进制小数时存在精度问题：`0.1 + 0.2 ≠ 0.3`（因为 0.1 在二进制里是无限循环小数）。在**金融计算**中，这种误差是不可接受的。十进制浮点直接用十进制存储，精确表示常见的十进制小数。

```c
#include <stdio.h>

int main(void) {
    // _Decimal32：32 位十进制浮点，约 7 位十进制精度
    // _Decimal64：64 位十进制浮点，约 16 位十进制精度
    // _Decimal128：128 位十进制浮点，约 34 位十进制精度

    _Decimal64 price = 19.99DF;  // 注意后缀 DF（_Decimal64 用 DF，_Decimal128 才用 DD）
    _Decimal64 tax = price * 0.08DF;  // 8% 税
    _Decimal64 total = price + tax;

    printf("商品价格: %Df\n", price);
    printf("税额(8%%): %Df\n", tax);
    printf("总价: %Df\n", total);

    // 十进制浮点能精确表示 0.1、0.2 等
    _Decimal64 a = 0.1DD;
    _Decimal64 b = 0.2DD;
    _Decimal64 sum = a + b;

    printf("0.1 + 0.2 = %DD\n", sum);
    // 输出: 0.1 + 0.2 = 0.30000000000000000DD
    // 注意：这里是精确的 0.3！

    return 0;
}
```

> **生活比喻：** 二进制浮点数就像用分数（1/3 = 0.333333...无限循环）来表示小数，而十进制浮点数就像直接用小数点（0.33333...可以精确表示 1/3 吗？不能！但 0.1 在十进制可以精确表示，在二进制反而不行）。金融计算用十进制，就像会计用"元、角、分"，而不是"盎司、磅"。

---

## 4.17 常见错误

### 4.17.1 变量未初始化

这是 C 语言最常见的 bug 之一。**未初始化的局部变量**里装的是垃圾值（上次使用这块内存留下的残留数据），每次运行可能都不一样。

```c
#include <stdio.h>

int main(void) {
    // 全局变量会自动初始化为 0
    static int global_var;
    printf("全局 static 变量: %d（自动初始化为 0）\n", global_var);
    // 输出: 全局 static 变量: 0（自动初始化为 0）

    // 局部变量不会自动初始化！
    int uninitialized;
    printf("未初始化局部变量: %d（垃圾值！每次不同）\n", uninitialized);
    // 输出: 未初始化局部变量: （一个随机数，比如 -858993460）

    // 正确做法：初始化
    int initialized = 0;
    printf("已初始化变量: %d\n", initialized);
    // 输出: 已初始化变量: 0

    return 0;
}
```

> **教训：** 养成声明变量时立即初始化的习惯！`int x = 0;`比`int x;`安全一万倍。

### 4.17.2 `char` 符号陷阱

前面 4.1.3 讲过，`char`的有符号性由实现决定。这会导致可移植性 bug：

```c
#include <stdio.h>

int main(void) {
    // 错误写法：假设 char 是有符号的
    char c = 200;  // 在有符号 char 系统上会变成 -56
    printf("char c = %d\n", c);
    // 在有符号 char 系统输出: char c = -56
    // 在无符号 char 系统输出: char c = 200

    // 正确写法：明确指定
    unsigned char uc = 200;
    printf("unsigned char uc = %u\n", uc);
    // 输出: unsigned char uc = 200（所有平台一致）

    // 另一个陷阱：char* 字符串字面量
    const char *s = "你好";
    // "你好"在内存中是以 char 或 signed char 存储的
    // 在某些平台上可能有问题（C23 建议用 const unsigned char *）

    return 0;
}
```

### 4.17.3 整数溢出

整数溢出（Integer Overflow）——当一个整数超出了它的表示范围，会"绕回来"（wrap around）。

```c
#include <stdio.h>
#include <stdint.h>

int main(void) {
    // 有符号整数溢出：未定义行为！（编译器可能优化掉你的判断）
    int i = INT_MAX;
    printf("INT_MAX = %d\n", i);
    // 输出: INT_MAX = 2147483647

    i = i + 1;  // UB！溢出后行为不可预测
    // printf("%d\n", i);  // 可能输出 -2147483648，但也可能输出 0，甚至程序崩溃

    // 无符号整数溢出：定义良好的行为，绕回到 0
    unsigned int u = UINT_MAX;
    printf("UINT_MAX = %u\n", u);
    // 输出: UINT_MAX = 4294967295

    u = u + 1;
    printf("UINT_MAX + 1 = %u\n", u);
    // 输出: UINT_MAX + 1 = 0（定义良好的行为）

    // 常见错误：循环终止条件写错
    for (unsigned int j = 10; j >= 0; j--) {
        // 这个循环是死循环！因为 j 是无符号整数，永远 >= 0
        // printf("%u\n", j);
    }
    // 正确写法：
    for (unsigned int j = 10; j > 0; j--) {
        // printf("%u\n", j);  // 10, 9, 8, ... 1
    }

    // 避免溢出的技巧：检查
    int a = 1000000;
    int b = 1000000;
    long long sum = (long long)a + b;  // 先升级类型再运算
    printf("a + b = %lld\n", sum);
    // 输出: a + b = 2000000

    return 0;
}
```

> **有符号整数溢出是未定义行为（Undefined Behavior）**！这意味着编译器可以"假设它不会发生"，然后把你的代码优化得面目全非。比如：
> ```c
> if (x + 1 > x) {  // 如果 x + 1 溢出，编译器可能直接优化成 "永远为真"
>     safe_printf("不会执行到这里！\n");
> }
> ```
> 编译器一看：哦，x + 1 肯定大于 x 啊（溢出是 UB 嘛），直接把这个 if 块删了！然后你发现 safe_printf 永远不执行。这就是 UB 的可怕之处——它让"看起来没问题"的代码悄悄消失。
> **无符号整数溢出是定义良好的行为**——它保证绕回到 0。但别因此就放松警惕，溢出仍然是不应该发生的事。

---

## 本章小结

本章我们深入探讨了 C 语言的数据类型与变量体系，以下是核心要点：

1. **基本数据类型**是 C 语言的基石：`int`/`short`/`long`/`long long`用于整数，`float`/`double`/`long double`用于浮点数，`char`用于字符，`_Bool`/`bool`用于布尔值，`void`表示"空"或"无类型"。

2. **`char`是最特殊的基本类型**：名字叫"字符"，实际上是个 1 字节整数，且有符号/无符号由实现决定。存数值时务必用`signed char`或`unsigned char`。

3. **`sizeof`是运算符不是函数**：用于查询类型或变量占用的字节数，返回`size_t`类型。`%zu`是 C99 标准推荐的格式说明符。

4. **有符号 vs 无符号**：有符号数可以表示负数，但范围较小；无符号数只能表示非负数，但范围更大。混合运算时要小心隐式转换陷阱。

5. **常量有三种写法**：`const`变量（只读变量）、`#define`宏（纯文本替换）、`enum`枚举（命名整数常量）。

6. **字面量后缀**（`L`、`U`、`f`、`LL`等）用于明确字面量的类型，避免歧义。

7. **进制表示**：十进制（无前缀）、八进制（`0`前缀）、十六进制（`0x`前缀）、二进制（`0b`前缀，C23新增）。

8. **隐式类型转换**发生在整型提升、寻常算术转换和默认实参提升中，可能导致精度损失或意外结果。能用显式转换就不用隐式转换。

9. **`typedef`给类型起别名**，让复杂类型更易读，也是跨平台代码的好帮手。

10. **`<stdint.h>`和`<inttypes.h>`** 是 C99 引入的固定宽度整数类型库，解决了"int 到底占几字节"的可移植性问题。

11. **`size_t`**是对象大小的标准类型（无符号），**`ptrdiff_t`**是指针减法的标准类型（有符号），**`wchar_t`**用于宽字符和 Unicode。

12. **C23 新特性**：`_BitInt`（任意精度整数）、十进制浮点（`_Decimal32/64/128`）、`bool`/`true`/`false`成为关键字、二进制字面量`0b`。

13. **三大常见错误**：变量未初始化（垃圾值）、`char`符号陷阱（跨平台不一致）、整数溢出（UB 或绕回）。

> **下一章预告：** 第 4B 章我们将深入探讨变量的"存储期"和"链接"——也就是变量从出生到死亡的全过程，以及它们在程序不同作用域之间的可见性关系。敬请期待！
