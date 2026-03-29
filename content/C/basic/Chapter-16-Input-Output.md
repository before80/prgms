+++
title = "第 16 章：输入输出详解"
weight = 160
date = "2026-03-29T22:34:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 第 16 章：输入输出详解

> "程序的本质，就是数据进来、转一圈、结果出去。没有输入输出的程序，就像一台永远不启动的发动机——再强大也只能是个摆设。"

你有没有想过，当你敲击键盘输入数字、程序屏幕上神奇地出现文字时，背后到底发生了什么？这一章，我们将深入 C 语言的"输入输出"世界——`printf` 和 `scanf`。别看它们名字简单，里头的门道可深着呢！学会了这章，你就真正掌握了程序与外界"对话"的技巧。

---

## 16.1 `printf` 格式详解

`printf` 是 C 语言中最常用的输出函数，它的核心能力来自那个神奇的"格式字符串"。很多人只会在 `printf` 里写 `%d`，但其实它支持一大堆格式说明符、标志位、宽度和精度控制——简直就是一个小型的"格式化工厂"！

### 16.1.1 格式说明符： `%` 开头的魔法字母

格式说明符（format specifier）以 `%` 开头，后面跟一个字母，用来告诉 `printf"这个位置我要输出什么类型的数据"。就像一个占位符，每个 `%` 都对应一个后面的参数。

#### 整数家族

```c
#include <stdio.h>

int main(void) {
    int    a = 42;         // 普通整数
    long   b = 1234567890L;    // 长整数
    long long c = 9876543210LL; // 更长的整数（C99）
    unsigned int d = 4000000000U; // 无符号整数

    printf("普通int:  %d\n", a);          // 输出: 普通int:  42
    printf("long:     %ld\n", b);         // 输出: long:     1234567890
    printf("long long:%lld\n", c);         // 输出: long long:9876543210
    printf("unsigned: %u\n", d);           // 输出: unsigned: 4000000000

    // %o 是八进制（octal），%x 是十六进制（hexadecimal）
    printf("八进制:   %o\n", a);           // 输出: 八进制:   52
    printf("十六进制: %x\n", a);           // 输出: 十六进制: 2a

    return 0;
}
```

**生活比喻**：`%d`、`%ld`、`%lld` 的关系，就像买房子时的"普通住宅"、"改善型住宅"、"豪华别墅"——都是"整数"，但"户型面积"不同，能容纳的数字大小也不同。

#### 字符与字符串

```c
#include <stdio.h>

int main(void) {
    char grade = 'A';
    char name[] = "小明";

    printf("等级: %c\n", grade);   // %c = 单个字符（character）
    // 输出: 等级: A

    printf("名字: %s\n", name);    // %s = 字符串（string）
    // 输出: 名字: 小明

    // 注意：%c 用单引号，%s 用数组或指针
    printf("第一个字母: %c\n", name[0]);  // 输出: 第一个字母: 小

    return 0;
}
```

> 小白疑问：`'A'` 和 `"A"` 有区别吗？
>
> 区别大了！`'A'` 是一个字符常量，对应一个字节，存储的是 ASCII 码 65。`"A"` 是一个字符串常量，实际存储的是两个字节——`'A'` 和 `'\0'`（空字符，字符串结束标志）。`%c` 用来输出字符，`%s` 用来输出字符串，千万别混用！

#### 浮点数家族

```c
#include <stdio.h>

int main(void) {
    double pi = 3.14159265358979;
    long double e = 2.718281828459045L;

    // %f 默认输出 6 位小数
    printf("pi = %f\n", pi);
    // 输出: pi = 3.141593

    // %.12f 输出 12 位小数
    printf("pi = %.12f\n", pi);
    // 输出: pi = 3.141592653590

    // %Lf 用于 long double（C99）
    printf("e  = %Lf\n", e);
    // 输出: e  = 2.718282

    // %e 科学计数法
    printf("pi = %e\n", pi);
    // 输出: pi = 3.141593e+00

    // %a 十六进制浮点数（C99），精度更高
    printf("pi = %a\n", pi);
    // 输出: pi = 0x1.921fb544117d1p+1

    return 0;
}
```

**敲黑板**：`%lf`（long float）和 `%Lf`（long long float）不是一回事！`%lf` 在 `printf` 里基本等价于 `%f`（`double`），而 `%Lf` 是专门给 `long double` 用的。

#### 指针与神秘地址

```c
#include <stdio.h>

int main(void) {
    int num = 100;
    int *ptr = &num;

    // %p 打印指针（地址）
    printf("num 的地址: %p\n", (void*)&num);
    // 类似输出: num 的地址: 0x7ffd5a3c4b44

    printf("ptr 的值:   %p\n", (void*)ptr);
    // 输出: ptr 的值:   0x7ffd5a3c4b44（和上面一样）

    // void* 需要强制类型转换才能用在 %p
    void *vptr = (void*)ptr;
    printf("void*:      %p\n", vptr);
    // 输出: void*:      0x7ffd5a3c4b44

    return 0;
}
```

> **小知识**：地址的格式 `0x` 开头表示十六进制。地址本身就是一个整数（用十六进制表示），只是它大到普通整数装不下，所以需要用 `%p` 来专门打印。

### 16.1.2 标志位：格式字符串里的"装饰品"

在 `%` 和格式字母之间，还可以放一些"标志位"（flag），用来微调输出外观。

| 标志 | 名称 | 效果 |
|------|------|------|
| `-` | 左对齐 | 默认右对齐，加 `-` 变成左对齐 |
| `+` | 显示正号 | 正数前也加 `+`，默认不加 |
| 空格 | 正数前留空格 | 正数前加一个空格，负数前是 `-` |
| `#` |  Alternate form | 八进制前加 `0`，十六进制前加 `0x` |
| `0` | 零填充 | 宽度不够时用 `0` 而非空格填充 |

```c
#include <stdio.h>

int main(void) {
    int num = 42;

    // - 左对齐
    printf("|%d|\n", num);    // 默认右对齐
    printf("|%-5d|\n", num);   // 左对齐，宽度5
    // 输出:
    // |42|
    // |42   |

    // + 显示正号
    printf("|%d|\n",  42);    // |42|
    printf("|%+d|\n", 42);    // |+42|

    // 空格
    printf("|% d|\n", 42);    // | 42|
    printf("|% d|\n", -42);   // |-42|

    // # Alternate form
    printf("%o\n", 42);       // 52（普通八进制）
    printf("%#o\n", 42);      // 052（前面加0）
    printf("%x\n", 255);      // ff
    printf("%#x\n", 255);     // 0xff

    // 0 零填充
    printf("|%05d|\n", 42);    // |00042|
    printf("|%05d|\n", -42);   // |-0042|

    return 0;
}
```

**生活比喻**：标志位就像给数字"化妆"——有人喜欢左对齐（像中文排版），有人喜欢在正数前加 `+` 显示自信，有人喜欢用 `0` 填满宽度（像 LED 显示屏）。

### 16.1.3 宽度与精度：精确控制输出"身材"

#### 宽度（width）

宽度指定了输出**最少**占多少字符。如果内容不足，用空格（默认）或 `0`（配合 `0` 标志）填充。

```c
#include <stdio.h>

int main(void) {
    printf("|%5d|\n", 42);     // 总宽度5，右对齐
    printf("|%5d|\n", 1234);   // 宽度5，如果内容更宽则突破限制
    printf("|%-5d|\n", 42);    // 总宽度5，左对齐
    // 输出:
    // |   42|
    // | 1234|
    // |42   |

    printf("|%10s|\n", "Hi");  // 字符串也能设置宽度
    // 输出: |        Hi|

    return 0;
}
```

#### 精度（precision）

精度用在 `.` 后面，对不同类型有不同含义：

- 对 `%f`、`%e`：小数点后几位
- 对 `%s`：最多输出多少个字符

```c
#include <stdio.h>

int main(void) {
    double pi = 3.14159265;

    // %.4f —— 保留4位小数
    printf("%.4f\n", pi);      // 输出: 3.1416
    printf("%.2f\n", pi);      // 输出: 3.14

    // %8.4f —— 总宽度8，精度4
    printf("%8.4f\n", pi);
    // 输出: "  3.1416"（前面两个空格）

    // %.4s —— 最多4个字符
    printf("%.4s\n", "HelloWorld");  // 输出: Hell
    printf("%8.4s\n", "HelloWorld"); // 输出: "    Hell"

    return 0;
}
```

> **经典应用**：用 `%.2f` 做金额显示，再也不担心小数点后乱七八糟了！

```c
#include <stdio.h>

int main(void) {
    double price = 19.9;
    double tax = price * 0.13;
    printf("商品价格: ￥%.2f\n", price);
    printf("税额(13%%): ￥%.2f\n", tax);
    printf("总计:     ￥%.2f\n", price + tax);
    // 输出:
    // 商品价格: ￥19.90
    // 税额(13%): ￥2.59
    // 总计:     ￥22.49

    return 0;
}
```

### 16.1.4 C99 新增长度修饰符：与时俱进

C99 引入了一批新的长度修饰符，让 `printf` 能够更精确地匹配各种整数类型。

```c
#include <stdio.h>
#include <stddef.h>   // 提供 size_t, ptrdiff_t
#include <inttypes.h> // 提供 intmax_t

int main(void) {
    // %zd —— size_t（无符号整数，通常是 unsigned int 或 unsigned long）
    size_t s = 12345;
    printf("size_t: %zd\n", s);        // 输出: size_t: 12345

    // %td —— ptrdiff_t（指针相减的结果类型）
    int arr[5];
    ptrdiff_t diff = &arr[5] - &arr[0];
    printf("ptrdiff_t: %td\n", diff);  // 输出: ptrdiff_t: 5

    // %hhd —— char 有符号解释（输出为一个 signed char）
    char c = 255;  // -1 的二进制表示（8位）
    printf("char (signed): %hhd\n", c); // 输出: char (signed): -1

    // %llu —— unsigned long long
    unsigned long long big = 18446744073709551615ULL;
    printf("unsigned long long: %llu\n", big);

    // %jd —— intmax_t（C99 中最宽的整数类型）
    intmax_t imax = 9223372036854775807;
    printf("intmax_t: %jd\n", imax);

    return 0;
}
```

**为什么要这些？** 想象一下，`int` 在 16 位系统上是 2 字节，在 32 位系统上是 4 字节，在 64 位系统上可能还是 4 字节（Windows）或 8 字节（Linux）。这些修饰符让你在打印 `size_t` 时不用担心它具体是 `unsigned int` 还是 `unsigned long`，写 `%zd` 就完事了！

### 16.1.5 `<inttypes.h>` 格式宏：跨平台的安全保障

`inttypes.h` 提供了一组**宏**，用于打印固定宽度的整数类型（如 `int64_t`、`uint32_t`）。这些宏展开后就是正确的格式说明符，确保在所有平台上都能正常工作。

```c
#include <stdio.h>
#include <inttypes.h>

int main(void) {
    int64_t  big_positive = 9223372036854775807LL;
    int64_t  big_negative = -9223372036854775807LL;
    uint32_t positive_unsigned = 4294967295U;

    // PRId64 展开为适合打印 int64_t 的格式（Linux 上通常是 "ld"，Windows 上是 "lld"）
    printf("正数: %" PRId64 "\n", big_positive);
    // 输出: 正数: 9223372036854775807

    printf("负数: %" PRId64 "\n", big_negative);
    // 输出: 负数: -9223372036854775807

    // PRIu32 展开为适合打印 uint32_t 的格式
    printf("无符号: %" PRIu32 "\n", positive_unsigned);
    // 输出: 无符号: 4294967295

    return 0;
}
```

> **重要提醒**：`PRId64` 这些宏不是函数，是**宏**。使用时要记住在两边加引号：`"%" PRId64 "\n"`，拼出来变成 `"%ld\n"` 或 `"%lld\n"`。

### 16.1.6 综合示例：打造一个"格式化仪表盘"

```c
#include <stdio.h>
#include <inttypes.h>

int main(void) {
    int    id       = 1001;
    char   name[]   = "张三丰";
    double score    = 98.756;
    int64_t salary  = 125000;

    printf("═══════════════════════════════════\n");
    printf("  员工信息卡\n");
    printf("═══════════════════════════════════\n");
    printf("  工号:   %05d\n", id);           // 5位，零填充
    printf("  姓名:   %-10s\n", name);        // 左对齐，宽度10
    printf("  绩效:   %+.2f 分\n", score);    // 显正负号，2位小数
    printf("  月薪:   ¥%'" PRIu64 "\n", salary); // 千位分隔符(C99)，需 PRIu64
    printf("═══════════════════════════════════\n");

    return 0;
}
```

---

## 16.2 `scanf` 格式详解与常见陷阱

如果说 `printf` 是"输出大炮"，那 `scanf` 就是"输入神器"。但这个神器脾气不太好，用错了会让你输得一败涂地。让我们一起来看看 `scanf` 的各种"雷区"和"安全通道"。

### 16.2.1 空白符处理：scanf 的"默认跳过"行为

`scanf` 在解析输入时，会**自动跳过**格式字符串中的空白符（空格、制表符 `\t`、换行符 `\n` 等），也会跳过输入中的任意空白符。

```c
#include <stdio.h>

int main(void) {
    int a, b, c;

    // 注意：格式字符串中的空格可以"吸收"任意数量的空白符
    printf("请输入三个整数（用空格或回车分隔）: ");
    scanf("%d", &a);
    scanf("%d", &b);
    scanf("%d", &c);

    // 下面这行，一次性读三个整数，格式串中的空格可以忽略任意空白
    // scanf("%d %d %d", &a, &b, &c);  // 同样OK

    printf("你输入了: %d, %d, %d\n", a, b, c);

    return 0;
}
```

> **关键概念**：`scanf("%d", &a)` 中的 `&` 是**取地址运算符**，告诉 `scanf"把读到的数放到变量 a 所在的内存地址去"`。没有 `&`，程序会崩溃或产生奇怪行为！

### 16.2.2 返回值：成功读取的项数

`scanf` 的返回值很有用——它返回**成功读取并赋值的数据项个数**。

```c
#include <stdio.h>

int main(void) {
    int a, b, c;

    printf("请输入三个整数: ");

    int count = scanf("%d %d %d", &a, &b, &c);

    printf("成功读取了 %d 个整数\n", count);

    if (count != 3) {
        printf("哎呀，你输入有问题，我只读到了 %d 个！\n", count);
    }

    return 0;
}
```

这个返回值在**循环读取**时特别有用：

```c
#include <stdio.h>

int main(void) {
    int num;
    int sum = 0;
    int count = 0;

    printf("请输入一系列整数（输入非数字结束）:\n");

    // 只读取数字，遇到非数字字符就停止
    while (scanf("%d", &num) == 1) {
        sum += num;
        count++;
        printf("  累计: %d 个数字, 和 = %d\n", count, sum);
    }

    printf("\n最终结果: 共输入 %d 个整数, 总和 = %d\n", count, sum);

    return 0;
}
```

**生活比喻**：把 `scanf` 想成一个挑剔的收银员，它会告诉你"我收了几个人的钱"。如果返回 0，说明没人付款（输入无效）；返回 EOF（-1），说明"关门了"（文件结束或错误）。

### 16.2.3 ⚠️ `scanf("%c")` 会读入换行符的陷阱

这是**最最最常见的新手灾难**！当你用 `scanf("%c")` 读取字符时，它会把**空格和换行符**也当作合法字符读进来，而不是跳过。

```c
#include <stdio.h>

int main(void) {
    int age;
    char grade;

    printf("请输入年龄: ");
    scanf("%d", &age);
    printf("年龄: %d\n", age);

    printf("请输入等级(A/B/C): ");
    scanf("%c", &grade);
    printf("等级: '%c'\n", grade);  // 哎呀！读到了 '\n'！

    return 0;
}
```

运行结果：

```
请输入年龄: 25
年龄: 25
请输入等级(A/B/C): 等级: '
'
```

为什么？因为输入 `25` 后你按了回车，`scanf("%d", &age)` 只拿走了 `25`，**那个回车键产生的 `\n` 还残留在输入缓冲区**。然后 `scanf("%c", &grade)` 立刻把这个 `\n` 拿走了。

#### 解决方案一：空格"吃"掉空白符

在 `%c` 前加一个空格，告诉 `scanf"先把空白符跳过"`：

```c
scanf(" %c", &grade);  // 注意 %c 前有个空格！
```

#### 解决方案二：清空缓冲区

```c
#include <stdio.h>

int main(void) {
    int age;
    char grade;

    printf("请输入年龄: ");
    scanf("%d", &age);

    // 方法A: 用 getchar() 吃掉换行
    getchar();

    printf("请输入等级(A/B/C): ");
    scanf("%c", &grade);

    printf("年龄: %d, 等级: %c\n", age, grade);

    return 0;
}
```

#### 解决方案三：使用 scanset 跳过所有空白

```c
scanf(" %c", &grade);  // 空格 + %c = 先跳过所有空白，再读一个非空白字符
```

### 16.2.4 宽度限制： `%ns` 防止缓冲区溢出

`%s` 默认读到空白符为止，但如果输入超长，就会发生**缓冲区溢出**（buffer overflow）——把数据写到数组外面去了！

```c
#include <stdio.h>

int main(void) {
    char name[10];  // 只能存9个字符 + '\0'

    printf("请输入名字（最多9个字符）: ");
    // %9s —— 最多读取9个字符，不会超出 name 的范围
    scanf("%9s", name);

    printf("你好, %s!\n", name);

    return 0;
}
```

> **安全警告**：未限制宽度的 `%s` 是危险的！如果有人输入超长的字符串，会覆盖相邻的内存，可能导致程序崩溃甚至被黑客利用！

### 16.2.5 扫描集（Scanset）： `%[a-z]` 和否定扫描集 `%[^0-9]`

扫描集是 `scanf` 的高级技能——用方括号 `[]` 围起来，告诉 `scanf"只接受这些字符"`。

#### 基本扫描集

```c
#include <stdio.h>

int main(void) {
    char hex[20];

    // %[0-9a-fA-F] —— 只接受十六进制字符
    printf("请输入十六进制数: ");
    scanf("%[0-9a-fA-F]", hex);  // 遇到非十六进制字符自动停止

    printf("你输入的十六进制数: %s\n", hex);

    return 0;
}
```

#### 否定扫描集

```c
#include <stdio.h>

int main(void) {
    char line[100];

    // %[^\n] —— 读入所有字符直到遇到换行符
    // 这常用于读取一整行，保留其中的空格！
    printf("请输入一句话: ");
    scanf("%[^\n]", line);

    printf("你输入的是: %s\n", line);

    return 0;
}
```

> **对比**：`scanf("%s", line)` 会**跳过空格**，遇到空格就停；而 `%[^\n]` 可以读取一整行，包含空格！

### 16.2.6 赋值抑制符： `%*d` 跳过不需要的项

`*`（赋值抑制符）告诉 `scanf"读这个位置，但不要赋值"——常用于跳过某些字段。

```c
#include <stdio.h>

int main(void) {
    int day, month, year;

    // 假设输入格式是: 2026/03/29
    // 我们只想读年份，跳过前两个
    printf("请输入日期 (YYYY/MM/DD): ");

    // %*d 读一个整数但不赋值，%d 读要的那个
    scanf("%d/%*d/%*d", &year);
    printf("年份是: %d\n", year);

    // 更实用的例子：只读取第二个数字
    int a, b, c;
    printf("\n输入三个整数，但只要第二个: ");
    scanf("%*d %d %*d", &b);
    printf("第二个整数是: %d\n", b);

    return 0;
}
```

### 16.2.7 `%i`：智能整数——自动识别进制

`%d` 只能读十进制数，但 `%i` 更聪明，能自动识别：

- `123` → 十进制 123
- `0x1A` → 十六进制 26
- `075` → 八进制 61

```c
#include <stdio.h>

int main(void) {
    int num;

    printf("用 %%i 读取数字（可识别进制）:\n");

    printf("输入 123 (十进制): "); scanf("%i", &num); printf("→ %d\n", num);
    // 输出: → 123

    printf("输入 0x1A (十六进制): "); scanf("%i", &num); printf("→ %d\n", num);
    // 输出: → 26

    printf("输入 075 (八进制): "); scanf("%i", &num); printf("→ %d\n", num);
    // 输出: → 61

    return 0;
}
```

---

## 16.3 `sprintf` 与 `snprintf`：把数据"写"成字符串

`printf` 输出到屏幕，而 `sprintf` 把格式化的内容**写入一个字符数组**（字符串）。这在需要"数字转字符串"时特别有用。

### 16.3.1 `sprintf`：简单但危险

```c
#include <stdio.h>

int main(void) {
    char buffer[100];
    int age = 25;
    double score = 98.5;

    // 把格式化的内容"打印"到 buffer 字符串中
    sprintf(buffer, "姓名: 张三, 年龄: %d, 分数: %.1f", age, score);

    printf("生成的字符串: %s\n", buffer);
    // 输出: 生成的字符串: 姓名: 张三, 年龄: 25, 分数: 98.5

    return 0;
}
```

> ⚠️ **危险警告**：`sprintf` 没有宽度保护！如果 `buffer` 不够大，或者格式化的内容超出了数组范围，就会发生**缓冲区溢出**！C99 引入了更安全的 `snprintf`，我们强烈建议使用它！

### 16.3.2 `snprintf`（C99）：安全版本

`snprintf` 多了一个参数：`size`，告诉你"最多写多少字符"。

```c
#include <stdio.h>

int main(void) {
    char buffer[50];  // 比较小的缓冲区
    int age = 25;
    const char *name = "张三丰";

    // snprintf(buffer, size, format, ...)
    // 最多写 size-1 个字符，最后留一个位置给 '\0'
    snprintf(buffer, sizeof(buffer),
             "姓名: %s, 年龄: %d", name, age);

    printf("结果: %s\n", buffer);
    // 输出: 结果: 姓名: 张三丰, 年龄: 25

    // 尝试写入超出缓冲区容量的内容
    char small[10];
    snprintf(small, sizeof(small), "HelloWorld123");
    printf("小缓冲区: %s\n", small);
    // 输出: 小缓冲区: HelloWorl（只写了9个字符 + \0）

    return 0;
}
```

### 16.3.3 C11 安全版本：`sprintf_s` / `snprintf_s`

C11 引入了一族 `_s` 后缀的安全函数，它们不仅限制长度，还会在运行时检测**空指针**等问题。

```c
#define __STDC_WANT_LIB_EXT1__ 1
#include <stdio.h>
#include <string.h>

int main(void) {
    char buffer[50];

    // sprintf_s 不需要传 size，会自动检查缓冲区边界
    sprintf_s(buffer, sizeof(buffer), "Hello, %s!", "小明");
    printf("%s\n", buffer);
    // 输出: Hello, 小明!

    // snprintf_s 是 snprintf 的安全版本
    int result = snprintf_s(buffer, sizeof(buffer), "Test %d", 123);
    printf("%s (返回值: %d)\n", buffer, result);
    // 输出: Test 123 (返回值: 8)

    return 0;
}
```

> **注意**：`sprintf_s` 等函数需要定义 `__STDC_WANT_LIB_EXT1__ 1` 才能启用。而且并不是所有编译器都完整支持它们（MSVC 支持较好，GCC/Clang 可能需要特定条件）。

---

## 16.4 `sscanf` / `sscanf_s`：从字符串中"提取"数据

`scanf` 从键盘/文件读取，而 `sscanf` 从**字符串**中解析数据。相当于"反向"的 `sprintf`。

```c
#include <stdio.h>

int main(void) {
    const char *data = "1001 张三 98.5";

    int id;
    char name[50];
    double score;

    // 从 data 字符串中解析出 id, name, score
    int count = sscanf(data, "%d %s %lf", &id, name, &score);

    printf("解析成功 %d 项\n", count);
    printf("学号: %d, 姓名: %s, 成绩: %.1f\n", id, name, score);
    // 输出:
    // 解析成功 3 项
    // 学号: 1001, 姓名: 张三, 成绩: 98.5

    return 0;
}
```

### C11 `sscanf_s`：安全增强版

```c
#define __STDC_WANT_LIB_EXT1__ 1
#include <stdio.h>

int main(void) {
    const char *data = "1001 张三 98.5";

    int id;
    char name[50];
    double score;

    // sscanf_s 需要提供每个字符串的缓冲区大小
    sscanf_s(data, "%d %s %lf", &id, name, sizeof(name), &score);

    printf("学号: %d, 姓名: %s, 成绩: %.1f\n", id, name, score);

    return 0;
}
```

---

## 16.5 `printf` / `scanf` 返回值详解

### `printf` 的返回值

`printf` 返回**打印的字符数**（不包括字符串结尾的 `\0`），如果发生错误则返回负数。

```c
#include <stdio.h>

int main(void) {
    int chars_printed = printf("Hello, 世界!\n");
    printf("上面一行打印了 %d 个字符\n", chars_printed);
    // 输出:
    // Hello, 世界!
    // 上面一行打印了 14 个字符

    // 利用返回值做格式化宽度计算
    char buf[20];
    int len = sprintf(buf, "%s", "test");
    printf("sprintf 返回值: %d\n", len);  // 输出: 4

    return 0;
}
```

### `scanf` 的返回值

| 返回值 | 含义 |
|--------|------|
| 成功赋值的项数 | 正常情况，1、2、3... |
| 0 | 没有成功赋值（输入不匹配） |
| EOF（通常是 -1） | 到达文件末尾或出错 |

```c
#include <stdio.h>

int main(void) {
    int a, b;

    printf("输入两个整数: ");

    // 常见用法：检查是否成功读取了所有需要的项
    if (scanf("%d %d", &a, &b) == 2) {
        printf("成功读取: %d 和 %d, 和 = %d\n", a, b, a + b);
    } else {
        printf("读取失败！\n");
    }

    // EOF 测试（可以用 Ctrl+D 或 Ctrl+Z 触发）
    printf("\n循环读取整数直到文件结束:\n");
    int num;
    while (scanf("%d", &num) == 1) {
        printf("  读取到: %d\n", num);
    }
    printf("输入结束（EOF）\n");

    return 0;
}
```

---

## 16.6 行缓冲： `setbuf` / `setvbuf`

标准输出（`stdout`）默认是**行缓冲**（line buffered）的——意思是：只有遇到换行符 `\n`，或者缓冲区满了，数据才会真正发送到屏幕。

### 为什么要关心缓冲？

有时候你调试程序，发现 `printf` 执行了但屏幕没输出——就是因为数据还在缓冲区里"排队"！

```c
#include <stdio.h>

int main(void) {
    printf("第一行");
    printf("第二行\n");  // 遇到 \n，输出整行
    printf("第三行");

    // 程序结束了，但"第三行"可能还在缓冲区
    // 如果想立刻看到，可以加 \n 或者调用 fflush

    return 0;
}
```

### `setbuf`：简单的缓冲控制

```c
#include <stdio.h>

int main(void) {
    // 设置 stdout 为无缓冲（unbuffered）
    // 这样每次 printf 都会立刻输出
    setbuf(stdout, NULL);  // 禁用缓冲

    printf("立刻看到我！");

    return 0;
}
```

> **注意**：`setbuf` 必须在任何 I/O 操作之前调用，否则可能出问题。

### `setvbuf`：更精细的控制

```c
#include <stdio.h>

int main(void) {
    char buffer[1024];

    // fopen 返回 FILE* 后，立刻设置缓冲模式
    FILE *fp = fopen("test.txt", "w");
    if (fp == NULL) {
        perror("打开文件失败");
        return 1;
    }

    // _IOLBF = 行缓冲（默认对 stdout）
    // _IOFBF = 全缓冲（对文件默认）
    // _IONBF = 无缓冲（每个字符立即输出）
    setvbuf(fp, buffer, _IOFBF, sizeof(buffer));

    fprintf(fp, "第一句话\n");
    fprintf(fp, "第二句话\n");

    fclose(fp);

    printf("文件写入完成！\n");

    return 0;
}
```

**三种缓冲模式对比**：

| 模式 | 宏 | 行为 |
|------|-----|------|
| 无缓冲 | `_IONBF` | 每次 I/O 立即执行，零延迟 |
| 行缓冲 | `_IOLBF` | 遇到换行符或满时输出（默认 stdout） |
| 全缓冲 | `_IOFBF` | 缓冲区满时才输出（默认文件） |

### `fflush`：强制刷新缓冲区

```c
#include <stdio.h>

int main(void) {
    printf("正在计算...");
    fflush(stdout);  // 立刻把缓冲区内容输出！

    // 模拟耗时操作
    for (volatile long i = 0; i < 1000000000; i++);

    printf(" 完成！\n");

    return 0;
}
```

> **关键点**：`fflush` 只对**输出流**（`stdout`、`FILE*`）有效，对输入流无效！

---

## 16.7 ⚠️ `fflush(stdin)`：标准未定义的"危险操作"

**这是本章最重要的警告之一！**

`fflush` 函数在 C 标准中的定义是：**只能用于输出流或更新流**。`stdin` 是**输入流**，所以 `fflush(stdin)` 的行为在标准中是**未定义的**（undefined behavior）！

```c
#include <stdio.h>

int main(void) {
    printf("输入一个数字: ");
    int num;
    scanf("%d", &num);
    printf("你输入了: %d\n", num);

    // 危险！fflush(stdin) 不是标准行为！
    // 有些编译器（如 MSVC）提供了这个扩展
    // 但在 Linux/GCC 下，可能根本不起作用！
    // fflush(stdin);  // 不要这样用！

    printf("再输入一个数字: ");
    scanf("%d", &num);
    printf("你输入了: %d\n", num);

    return 0;
}
```

### 为什么 MSVC 能用但其他编译器不行？

MSVC（Microsoft Visual C++）把 `fflush(stdin)` 当作**编译器扩展**实现了，所以你在 Windows 上用它可能有效。但 POSIX 标准明确说 `fflush` 用于输入流是**未定义行为**，GCC/Clang 不会支持它。

### 正确的"清空输入缓冲区"方法

#### 方法一：使用 `getchar()` 循环吃掉字符

```c
#include <stdio.h>

void clear_input_buffer(void) {
    int c;
    while ((c = getchar()) != '\n' && c != EOF) {
        // 不断读取，直到遇到换行符或文件结束
    }
}

int main(void) {
    int age;
    char grade;

    printf("年龄: ");
    scanf("%d", &age);
    clear_input_buffer();  // 正确地清空输入缓冲区

    printf("等级: ");
    scanf("%c", &grade);  // 这里不会再读到残留的 \n
    printf("结果: 年龄=%d, 等级=%c\n", age, grade);

    return 0;
}
```

#### 方法二：使用 `scanf` 的空白符

```c
#include <stdio.h>

int main(void) {
    int age;
    char grade;

    printf("年龄: ");
    scanf("%d", &age);

    // 用 " %c"（空格 + %c）跳过所有空白，包括换行符
    printf("等级: ");
    scanf(" %c", &grade);

    printf("结果: 年龄=%d, 等级=%c\n", age, grade);

    return 0;
}
```

#### 方法三：C11 `scanf` 的分配内存扩展（部分支持）

```c
#include <stdio.h>

int main(void) {
    // GCC 的扩展：%ms 自动分配内存存储字符串
    // 但这不是标准 C！只在部分编译器上有效
    // char *line = NULL;
    // scanf("%ms", &line);
    // free(line);

    return 0;
}
```

> **总结**：`fflush(stdin)` 能不用就不用，跨平台代码必须用 `getchar()` 循环或 `scanf(" %c")` 的方式清空缓冲区。

---

## 本章小结

本章我们深入探索了 C 语言的输入输出系统，主要内容包括：

### `printf` 格式化输出

- **格式说明符**是 `printf` 的核心：`%d`（整数）、`%f`（浮点）、`%s`（字符串）、`%p`（地址）、`%c`（字符）、`%x`（十六进制）等
- **标志位**可以微调输出格式：`-`（左对齐）、`+`（显示正号）、`#`（Alternate form）、`0`（零填充）
- **宽度和精度**让你精确控制输出的"身材"：如 `%8.2f`（总宽8，2位小数）
- **C99 新增长度修饰符**：`%zd`（size_t）、`%td`（ptrdiff_t）、`%hhd`（signed char）、`%llu`（unsigned long long）
- **`<inttypes.h>` 宏**（`PRId64`、`PRIu32` 等）保证了跨平台打印固定宽度整数的安全性

### `scanf` 格式化输入

- `scanf` 会**跳过格式串中的空白符和输入中的任意空白符**
- 返回值表示**成功赋值的项数**，可以用作循环退出条件
- **`%c` 会读入空格和换行符**，需要在前面加空格 ` %c` 或用其他方法清缓冲区
- **`%ns` 设置宽度限制**，防止缓冲区溢出
- **扫描集** `%[a-z]` 和否定扫描集 `%[^0-9]` 提供了强大的模式匹配输入能力
- **`%*d` 赋值抑制符**可以跳过不需要的输入项
- **`%i` 自动识别进制**，比 `%d` 更智能

### 字符串格式化函数

- **`sprintf`** 把格式化的内容写入字符串（注意缓冲区溢出风险！）
- **`snprintf`**（C99）是安全版本，需要指定缓冲区大小
- **`sscanf`** 从字符串中解析数据，类似"反向的 sprintf"
- C11 的 `_s` 后缀版本（`sprintf_s`、`snprintf_s`、`sscanf_s`）增加了运行时安全检查

### 缓冲与 `fflush`

- `printf` 默认是**行缓冲**，遇到 `\n` 才输出
- `setbuf` / `setvbuf` 可以控制缓冲模式：`_IONBF`（无缓冲）、`_IOLBF`（行缓冲）、`_IOFBF`（全缓冲）
- `fflush(stdout)` 强制刷新输出缓冲区
- **⚠️ `fflush(stdin)` 行为未定义**，标准禁止对输入流使用 `fflush`！跨平台代码必须用 `getchar()` 循环或 `scanf(" %c")` 代替

---

**下章预告**：第 17 章我们将探讨 C 语言的**文件操作**——如何读写文件、管理文件指针、处理二进制文件，以及那些藏在标准库里的文件系统函数。敬请期待！
