+++
title = "第 11 章：结构体、共用体与枚举"
weight = 110
date = "2026-03-29T22:34:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 第 11 章：结构体、共用体与枚举

> "数据结构学得好，C 语言就学会了一大半。" —— 某位不愿意透露姓名的 C 语言老师

欢迎来到 C 语言最"成人"的一章！前面我们学的数组，就像是一个装满相同类型鸡蛋的盒子。但现实世界的数据可不是这么单纯的——你的人口普查表里，有姓名（字符串）、年龄（整数）、身高（浮点数）、血型（枚举）……这些乱七八糟的东西，怎么塞进一个整齐的数组里？

答案就是本章的主角：**结构体（Struct）**。它就像是一个可以自定义的"万能收纳盒"，想装什么装什么。准备好了吗？让我们一起探索 C 语言的"收纳艺术"！

---

## 11.1 结构体：组织异构数据

想象一下，你要做一个学生信息管理系统。每个学生有：

- 姓名（"张三"）
- 年龄（18）
- 学号（2024001）
- GPA（3.75）

这些数据类型都不一样！字符串、整数、整数、浮点数。用数组？数组要求所有元素类型一致，你总不能建四个数组分别存吧？那管理起来简直是噩梦。

**结构体**就是用来解决这个问题的！它允许你把不同类型的数据"打包"在一起，给这个包起个名字，当作一种新的"复合数据类型"来用。

简单说：

- **数组** = 同类数据的"群居"（int 数组全是 int）
- **结构体** = 异类数据的"合租"（各种类型住一屋）

```c
#include <stdio.h>
#include <string.h>  // 为了使用 strcpy

// 定义一个学生结构体
struct Student {
    char name[50];   // 姓名，用字符数组存
    int age;         // 年龄
    int id;          // 学号
    float gpa;      // GPA
};

int main() {
    // 创建一个学生变量
    struct Student s1;

    // 给成员赋值
    strcpy(s1.name, "张三");
    s1.age = 18;
    s1.id = 2024001;
    s1.gpa = 3.75;

    // 打印看看
    printf("姓名: %s\n", s1.name);
    printf("年龄: %d\n", s1.age);
    printf("学号: %d\n", s1.id);
    printf("GPA: %.2f\n", s1.gpa);

    return 0;
}
```

输出：

```
姓名: 张三
年龄: 18
学号: 2024001
GPA: 3.75
```

> **什么是成员（member）？** 结构体里定义的每个变量叫"成员"，就像一个房子的各个房间。`name`、`age`、`id`、`gpa` 都是这个 `Student` 结构体的成员。

---

## 11.2 结构体定义、初始化、成员访问（`.` 运算符）

### 定义结构体的三种方式

**方式一：先定义类型，再声明变量（最标准）**

```c
struct Student {
    char name[50];
    int age;
    int id;
    float gpa;
};

struct Student s1;  // 用 struct Student 作为类型声明变量
```

**方式二：定义的同时声明变量**

```c
struct Student {
    char name[50];
    int age;
    int id;
    float gpa;
} s1, s2;  // 定义完直接声明了两个变量
```

**方式三：匿名结构体（不给结构体起名），直接声明**

```c
struct {
    char name[50];
    int age;
    int id;
    float gpa;
} s1;  // 只能声明这一个变量，因为没有类型名
```

> 方式三看起来省事，但缺点是你没法再创建第二个同类型的变量了。除非你确定这辈子只用一个，否则不建议用这种方式。

### 初始化：赋值的方式

**第一种：声明时按顺序初始化**

```c
struct Student s1 = {"张三", 18, 2024001, 3.75};
```

**第二种：指定成员名初始化（C99 开始支持，乱序也没问题）**

```c
struct Student s1 = {
    .name = "张三",
    .gpa = 3.75,
    .age = 18,
    .id = 2024001
};  // 注意顺序可以打乱，而且没写的成员会被自动初始化为 0
```

> 这种`.成员名 = 值`的方式叫**指定初始化器（designated initializer）**，简直是人类的伟大发明！当结构体有几十个成员，但你想只初始化其中几个时，这个语法就是救命稻草。

### 成员访问：用 `.` 运算符

用**点运算符（`.`）**来访问结构体变量的成员：

```c
struct Student s1;

// 赋值
strcpy(s1.name, "李四");  // 字符串要用 strcpy，不能直接 =
s1.age = 20;
s1.id = 2024002;
s1.gpa = 3.85;

// 读取
printf("姓名: %s\n", s1.name);
printf("年龄: %d\n", s1.age);
```

---

## 11.3 结构体的内存对齐（对齐规则：最大成员倍数）

这是一个非常"坑"但又不得不了解的知识点。

### 为什么要有内存对齐？

先看一个"诡异"的例子：

```c
#include <stdio.h>

struct A {
    char a;   // 1 字节
    int b;    // 4 字节
};

struct B {
    int b;    // 4 字节
    char a;   // 1 字节
};

int main() {
    printf("struct A 大小: %zu 字节\n", sizeof(struct A));
    printf("struct B 大小: %zu 字节\n", sizeof(struct B));
    printf("char 大小: %zu\n", sizeof(char));
    printf("int 大小: %zu\n", sizeof(int));

    return 0;
}
```

输出（在我的机器上）：

```
char 大小: 1 字节
int 大小: 4 字节
struct A 大小: 8 字节
struct B 大小: 8 字节
```

奇怪！`struct A` 和 `struct B` 的成员明明一样，只是顺序不同，为什么大小都是 8 字节？

### 内存对齐规则

这是因为**编译器会自动进行内存对齐**。规则如下：

> **结构体的大小必须是其最大成员大小的整数倍。**

- `struct A`：最大成员是 `int b`（4 字节），所以大小必须是 4 的倍数。`char a`（1字节）+ 3 字节 padding + `int b`（4字节）= 8 字节。
- `struct B`：`int b`（4字节）+ `char a`（1字节）+ 3 字节 padding = 8 字节。

内存对齐的**原因**是：CPU 访问内存时，一次性读取 4 字节（或 8 字节，取决于系统）比读取 1 字节更高效。如果 `int` 没有对齐到 4 字节边界，CPU 可能要读两次再拼接，效率大打折扣。

```mermaid
block-beta
    columns 8
    block:"struct A 的内存布局"
        col1:"a (1字节)" col2:"padding" col3:"padding" col4:"padding" col5:"b (4字节)" col6:"b" col7:"b" col8:"b"
    end

    block:"struct B 的内存布局"
        col1:"b (4字节)" col2:"b" col3:"b" col4:"b" col5:"a (1字节)" col6:"padding" col7:"padding" col8:"padding"
    end
```

> **Padding（填充字节）**就是编译器偷偷塞进去的"空白"，用来让每个成员都对齐到合适的位置。这是编译器自动干的，不需要你写代码。

### 11.3.1 `#pragma pack`：手动控制对齐

有时候你不想让编译器加那么多 padding，想节省空间，怎么办？

用 `#pragma pack` 可以**手动设置对齐字节数**：

```c
#include <stdio.h>

// 强制 1 字节对齐，不允许 padding
#pragma pack(push, 1)
struct Compact {
    char a;   // 1 字节
    int b;    // 4 字节
};
#pragma pack(pop)  // 恢复默认对齐

struct Normal {
    char a;   // 1 字节
    int b;    // 4 字节
};

int main() {
    printf("紧凑布局: %zu 字节\n", sizeof(struct Compact));
    printf("普通布局: %zu 字节\n", sizeof(struct Normal));

    return 0;
}
```

输出：

```
紧凑布局: 5 字节
普通布局: 8 字节
```

> `#pragma pack(push, 1)` 把当前对齐状态压栈，然后设置对齐为 1 字节。`#pragma pack(pop)` 恢复之前的对齐状态。这就像你告诉编译器："这屋子里给我挤一挤，能省空间就省！"

> 但要注意：**强制 1 字节对齐会损失性能**。因为 CPU 访问非对齐的内存会变慢，甚至在某些架构上直接崩溃。所以只有在对空间极度敏感时才用，比如网络协议包、文件格式解析。

### 11.3.2 `offsetof` 宏（`<stddef.h>`）：获取成员偏移量

想知道某个成员在结构体里从开头偏移了多少字节？用 `offsetof` 宏！

```c
#include <stdio.h>
#include <stddef.h>  // offsetof 宏在这里

struct Student {
    char name[50];   // 偏移 0
    int age;         // 偏移 50
    int id;          // 偏移 54
    float gpa;       // 偏移 58
};

int main() {
    printf("name 偏移量: %zu 字节\n", offsetof(struct Student, name));
    printf("age 偏移量:  %zu 字节\n", offsetof(struct Student, age));
    printf("id 偏移量:   %zu 字节\n", offsetof(struct Student, id));
    printf("gpa 偏移量:  %zu 字节\n", offsetof(struct Student, gpa));
    printf("\n结构体总大小: %zu 字节\n", sizeof(struct Student));

    return 0;
}
```

输出：

```
name 偏移量: 0 字节
age 偏移量:  50 字节
id 偏移量:   54 字节
gpa 偏移量:  58 字节

结构体总大小: 64 字节
```

> `offsetof` 是一个宏，它接受两个参数：`结构体类型` 和 `成员名`，返回该成员相对于结构体起始地址的字节偏移量。这个宏底层其实是用了一个巧妙的技巧：`((type*)0)->member`，把地址 0 当作结构体起始地址，然后访问成员，得到的就是偏移量。

### 11.3.3 `[[no_unique_address]]`（C23）：空结构体成员占用零字节

如果一个结构体里有一个成员是**空结构体**（没有成员的 struct），在 C23 之前，这个空结构体成员也要占至少 1 字节。但在 C23 里，你可以用 `[[no_unique_address]]` 告诉编译器："这个成员不占用额外空间"。

```c
#include <stdio.h>

// C23 特性
struct Empty {
    // 空结构体
};

struct WithEmpty {
    int x;
    struct Empty e;  // 以前至少占 1 字节
    int y;
};

struct WithEmptyC23 {
    int x;
    struct Empty e;  // 空结构体
    int y;
};

int main() {
    printf("C23 之前:\n");
    printf("空结构体大小: %zu 字节\n", sizeof(struct Empty));
    printf("WithEmpty 大小: %zu 字节\n", sizeof(struct WithEmpty));

    printf("\n（C23 [[no_unique_address]] 如果你的编译器支持的话）\n");

    return 0;
}
```

> 等等，这个属性有什么用？想象一下你需要"标记"某个结构体类型的存在，但又不希望在实例里占用空间。比如一个调试信息结构体，平时不需要的时候它就是空的。

---

## 11.4 结构体数组与结构体指针

### 结构体数组

要存多个学生信息？用结构体数组！

```c
#include <stdio.h>

struct Student {
    char name[50];
    int age;
    float gpa;
};

int main() {
    // 定义一个结构体数组，存 3 个学生
    struct Student class[3] = {
        {"张三", 18, 3.75},
        {"李四", 19, 3.90},
        {"王五", 20, 3.60}
    };

    // 遍历打印
    for (int i = 0; i < 3; i++) {
        printf("学生 %d: %s, 年龄 %d, GPA %.2f\n",
               i + 1, class[i].name, class[i].age, class[i].gpa);
    }

    return 0;
}
```

输出：

```
学生 1: 张三, 年龄 18, GPA 3.75
学生 2: 李四, 年龄 19, GPA 3.90
学生 3: 王五, 年龄 20, GPA 3.60
```

### 结构体指针

当结构体很大的时候，传指针比传整个结构体高效得多（关于传值和传指针的区别，稍后 11.6 节会详细讲）。

```c
#include <stdio.h>

struct Student {
    char name[50];
    int age;
    float gpa;
};

int main() {
    struct Student s1 = {"赵六", 21, 3.80};

    // 指向结构体的指针
    struct Student *ptr = &s1;

    // 用点运算符访问（解引用后）
    printf("姓名: %s\n", (*ptr).name);
    printf("年龄: %d\n", (*ptr).age);
    printf("GPA: %.2f\n", (*ptr).gpa);

    // 箭头运算符更方便（专门为结构体指针设计的语法糖）
    printf("\n用箭头运算符:\n");
    printf("姓名: %s\n", ptr->name);
    printf("年龄: %d\n", ptr->age);
    printf("GPA: %.2f\n", ptr->gpa);

    return 0;
}
```

输出：

```
姓名: 赵六
年龄: 21
GPA: 3.80

用箭头运算符:
姓名: 赵六
年龄: 21
GPA: 3.80
```

> **箭头运算符 `->`**：这是专门为结构体指针发明的语法。`ptr->member` 等价于 `(*ptr).member`，但写起来短多了，而且更直观——箭头本身就像是在"指向"结构体的成员。记住：**访问指针指向的结构体成员，用 `->`；访问普通结构体变量的成员，用 `.`**。

---

## 11.5 结构体嵌套

结构体里可以有另一个结构体，这叫**嵌套结构体**。

```c
#include <stdio.h>
#include <string.h>

// 先定义被嵌套的结构体
struct Date {
    int year;
    int month;
    int day;
};

struct Student {
    char name[50];
    struct Date birthday;  // 嵌套了一个 Date 结构体
    float gpa;
};

int main() {
    struct Student s1;

    strcpy(s1.name, "孙七");
    s1.birthday.year = 2005;
    s1.birthday.month = 8;
    s1.birthday.day = 15;
    s1.gpa = 3.95;

    printf("学生: %s\n", s1.name);
    printf("生日: %d年%02d月%02d日\n",
           s1.birthday.year,
           s1.birthday.month,
           s1.birthday.day);
    printf("GPA: %.2f\n", s1.gpa);

    return 0;
}
```

输出：

```
学生: 孙七
生日: 2005年08月15日
GPA: 3.95
```

> 访问嵌套结构体的成员，要用多个 `.`：先是 `s1.birthday`，然后 `s1.birthday.year`。就像你走进一栋楼，先找到楼层，再找到房间。

---

## 11.6 结构体与函数：传值 vs 传指针（传指针避免复制开销）

### 传值：整个结构体都复制一份

```c
#include <stdio.h>
#include <string.h>

struct Student {
    char name[50];
    int age;
};

// 传值：接收结构体的副本
void printStudent(struct Student s) {
    printf("姓名: %s, 年龄: %d\n", s.name, s.age);
    // 注意：这里修改 s 不会影响外面的原变量
}

int main() {
    struct Student s1;
    strcpy(s1.name, "周八");
    s1.age = 22;

    printStudent(s1);  // 把整个结构体复制一份传进去
    // s1 不会被修改

    return 0;
}
```

输出：

```
姓名: 周八, 年龄: 22
```

### 传指针：只传地址，不复制

```c
#include <stdio.h>
#include <string.h>

struct Student {
    char name[50];
    int age;
};

// 传指针：只传 8 字节（64位系统），不复制整个结构体
void birthday(struct Student *s) {
    s->age++;  // 直接修改原变量
    printf("生日快乐！%s 现在 %d 岁了\n", s->name, s->age);
}

int main() {
    struct Student s1;
    strcpy(s1.name, "吴九");
    s1.age = 23;

    birthday(&s1);  // 只传地址
    printf("main 里: %s 年龄是 %d\n", s1.name, s1.age);  // 已经被修改了

    return 0;
}
```

输出：

```
生日快乐！吴九 现在 24 岁了
main 里: 吴九 年龄是 24
```

> **为什么传指针更高效？** 假设你的 `Student` 结构体有 100 个成员，总共 1000 字节。传值意味着要把这 1000 字节全部复制一份放到函数栈帧里。如果传 1000 次函数调用，就要复制 1000 次。但如果传指针，只需要复制 8 字节的地址。这就是为什么**大结构体优先传指针**。

> 但传指针有个风险：**函数内部可以直接修改原数据**。如果不想被修改，可以加 `const`：`void printStudent(const struct Student *s)`。

---

## 11.7 `typedef` 与结构体：`typedef struct { ... } Name;`

每次定义结构体变量都要写 `struct Student`，好麻烦！用 `typedef` 给结构体类型起个别名，就可以省掉 `struct` 关键字：

```c
#include <stdio.h>
#include <string.h>

// 不用 typedef：声明变量要写 struct
struct Student1 {
    char name[50];
    int age;
};
struct Student1 s1;  // 必须带 struct

// 用 typedef：声明变量不用写 struct
typedef struct {
    char name[50];
    int age;
} Student;  // Student 就是这个结构体类型的别名

Student s2;  // 直接写 Student，不用 struct
```

```c
#include <stdio.h>
#include <string.h>

typedef struct {
    char name[50];
    int age;
    float gpa;
} Student;

int main() {
    Student s1;
    strcpy(s1.name, "郑十");
    s1.age = 24;
    s1.gpa = 4.00;

    printf("%s，%d岁，GPA %.2f\n", s1.name, s1.age, s1.gpa);

    return 0;
}
```

输出：

```
郑十，24岁，GPA 4.00
```

> **typedef 是什么？** `typedef` 是给已有类型起别名的关键字。就像你给"中华人民共和国"起别名叫"中国"，两种叫法指的都是同一个东西。`typedef struct { ... } Student;` 就是给这个匿名结构体类型起了个名字叫 `Student`。

> **注意**：上面这种写法，`Student` 虽然可以当类型名用了，但它其实还是一个**匿名结构体**（没有标签名）。如果你的代码里有其他文件也要用这个类型，或者你要写头文件声明，可能会有问题。更好的做法是同时给结构体标签名和 typedef 名字：

```c
typedef struct Student {
    char name[50];
    int age;
} Student;
```

---

## 11.8 匿名结构体（C11）

C11 支持**匿名结构体**：直接在另一个结构体里声明一个没有名字的结构体，可以直接访问其成员：

```c
#include <stdio.h>

struct Outer {
    int x;

    struct {   // 匿名结构体，没有名字
        int y;
        int z;
    };          // 注意这里有分号，表示匿名结构体成员结束
};

int main() {
    struct Outer o;
    o.x = 10;
    o.y = 20;   // 直接访问匿名结构体的成员！
    o.z = 30;

    printf("x=%d, y=%d, z=%d\n", o.x, o.y, o.z);

    return 0;
}
```

输出：

```
x=10, y=20, z=30
```

> **匿名结构体有什么用？** 它适合表示"只在特定上下文中使用"的临时组合。比如你定义一个"坐标"可能只需要在某个特定的图形结构里用，就可以嵌套进来，不用专门定义一个 `Point` 结构体类型。

> 但匿名结构体也有缺点：**代码可读性会下降**（别人看你的代码不知道 `y` 是什么类型），而且**调试困难**（调试器显示的类型是匿名的）。所以除非真的能简化代码，否则慎用。

---

## 11.9 共用体（Union）：同一内存空间的不同解释方式

终于到了共用体！如果说结构体是"合租"，那共用体就是"换装游戏"——同一块内存，一会儿当整数用，一会儿当浮点数用，一会儿又当字符数组用。但注意：**同一时间只能穿一套衣服**！

```c
#include <stdio.h>
#include <string.h>

union Data {
    int i;      // 4 字节
    float f;    // 4 字节
    char str[20];  // 20 字节
};

int main() {
    union Data data;

    // 存整数
    data.i = 10;
    printf("作为整数: %d\n", data.i);

    // 存浮点数（会覆盖整数的内容！）
    data.f = 3.14;
    printf("作为浮点数: %.2f\n", data.f);

    // 存字符串（又会覆盖！）
    strcpy(data.str, "Hello");
    printf("作为字符串: %s\n", data.str);

    // 打印共用体大小
    printf("\nunion Data 大小: %zu 字节\n", sizeof(union Data));
    printf("（等于最大成员的大小: int=%zu, float=%zu, str[20]=%zu）\n",
           sizeof(int), sizeof(float), sizeof(char[20]));

    return 0;
}
```

输出：

```
作为整数: 10
作为浮点数: 3.14
作为字符串: Hello

union Data 大小: 20 字节
（等于最大成员的大小: int=4, float=4, str[20]=20）
```

> **共用体的特点**：所有成员**共享同一块内存**。这块内存的大小等于最大成员的大小。往任何一个成员写入，都会覆盖其他成员的值。所以叫"共用"——大家一起用同一块地儿。

### 11.9.1 共用体的用途：大小端检测、内存复用、tagged union

#### 用途一：检测大小端

```c
#include <stdio.h>

union EndianCheck {
    int value;
    char bytes[4];  // 把整数按字节查看
};

int main() {
    union EndianCheck check;
    check.value = 1;  // 0x00000001

    // 如果第一个字节是 1，说明是小端（低位在前）
    // 小端: 01 00 00 00 (x86)
    // 大端: 00 00 00 01 (网络字节序)

    if (check.bytes[0] == 1) {
        printf("小端字节序 (Little Endian)\n");
        printf("内存布局: %02X %02X %02X %02X\n",
               (unsigned char)check.bytes[0],
               (unsigned char)check.bytes[1],
               (unsigned char)check.bytes[2],
               (unsigned char)check.bytes[3]);
    } else {
        printf("大端字节序 (Big Endian)\n");
    }

    return 0;
}
```

> **什么是大小端？** 计算机存储多字节数据（比如 `int`）时，有两种顺序。假设 `int` 值是 `0x0A0B0C0D`（4字节）：小端序把低位字节放在低地址（内存里是 `0D 0C 0B 0A`）；大端序把高位字节放在低地址（内存里是 `0A 0B 0C 0D`）。x86 系列 CPU 是小端的，网络协议常用大端。

#### 用途二：内存复用（节省空间）

```c
#include <stdio.h>

// 如果用 struct，需要 4+20=24 字节（还要考虑对齐）
// 如果用 union，只需要 20 字节
union Value {
    int number;           // 整数
    char text[20];        // 文本
};

int main() {
    union Value v;

    // 可以当整数用
    v.number = 42;
    printf("整数: %d\n", v.number);

    // 也可以当文本用
    sprintf(v.text, "数字是 %d", v.number);
    printf("文本: %s\n", v.text);

    printf("共用体大小: %zu 字节\n", sizeof(union Value));

    return 0;
}
```

#### 用途三：Tagged Union（带标签的共用体）

这是实现"变体类型"的标准方法——用一个枚举标记当前存的是什么：

```c
#include <stdio.h>
#include <string.h>

enum Type { TYPE_INT, TYPE_FLOAT, TYPE_STRING };

struct TaggedValue {
    enum Type type;  // 标签，标记当前存的是什么
    union {
        int i;
        float f;
        char s[50];
    } value;
};

void printTagged(struct TaggedValue *tv) {
    switch (tv->type) {
        case TYPE_INT:
            printf("整数: %d\n", tv->value.i);
            break;
        case TYPE_FLOAT:
            printf("浮点数: %.2f\n", tv->value.f);
            break;
        case TYPE_STRING:
            printf("字符串: %s\n", tv->value.s);
            break;
    }
}

int main() {
    struct TaggedValue tv1, tv2, tv3;

    tv1.type = TYPE_INT;
    tv1.value.i = 100;

    tv2.type = TYPE_FLOAT;
    tv2.value.f = 3.14159;

    tv3.type = TYPE_STRING;
    strcpy(tv3.value.s, "Hello Tagged Union!");

    printTagged(&tv1);
    printTagged(&tv2);
    printTagged(&tv3);

    return 0;
}
```

输出：

```
整数: 100
浮点数: 3.14
字符串: Hello Tagged Union!
```

> **Tagged Union（带标签的共用体）**：这是编程中的经典模式。共用体本身不知道当前存的是什么类型，所以需要额外一个"标签"来记录。读取之前先看标签，就知道该怎么解释那块内存了。JSON 库、脚本引擎、状态机实现里经常能看到这个模式。

### 11.9.2 匿名共用体（C11）

和匿名结构体类似，C11 也支持**匿名共用体**：

```c
#include <stdio.h>

struct Container {
    int type;

    union {   // 匿名共用体，直接访问其成员
        int i;
        float f;
    };
};

int main() {
    struct Container c;

    c.type = 1;   // 1 表示整数模式
    c.i = 123;    // 直接写，不用 c.value.i
    printf("整数模式: %d\n", c.i);

    c.type = 2;   // 2 表示浮点模式
    c.f = 9.87;   // 直接写
    printf("浮点模式: %.2f\n", c.f);

    return 0;
}
```

---

## 11.10 位域（Bit-field）：压缩结构体成员占用位数

有时候你不需要完整的字节，只需要几个位。比如一个布尔值，0 或 1，一个 bit 就够了。**位域（Bit-field）** 就是用来做这件事的——让你用"位"而不是"字节"来定义结构体成员。

### 11.10.1 位域语法与限制

```c
#include <stdio.h>

// 定义位域结构体
struct Flags {
    unsigned int is_active : 1;    // 只用 1 位，0 或 1
    unsigned int is_visible : 1;   // 只用 1 位
    unsigned int is_admin : 1;     // 只用 1 位
    unsigned int reserved : 5;     // 保留 5 位（凑够一个字节）
    unsigned int level : 8;       // 用 8 位，范围 0-255
};

int main() {
    struct Flags f;

    // 初始化所有位为 0
    f.is_active = 0;
    f.is_visible = 1;
    f.is_admin = 0;
    f.reserved = 0;
    f.level = 15;

    printf("Flags 结构体大小: %zu 字节\n", sizeof(struct Flags));
    printf("is_active=%d, is_visible=%d, is_admin=%d, level=%d\n",
           f.is_active, f.is_visible, f.is_admin, f.level);

    return 0;
}
```

输出：

```
Flags 结构体大小: 4 字节
```

> **位域的语法**：`类型 成员名 : 位数;` 这个结构体本来需要很多字节，但通过位域打包，5 个成员（1+1+1+5+8=16 位）只需要 2 个字节（实际上编译器给了 4 字节）。不过位域的具体布局是**实现相关的**，不同编译器可能不一样。

### 位域的限制：`&` 不能用于位域

**重要**：位域变量**不能取地址**！不能用 `&` 运算符。

```c
#include <stdio.h>

struct Flags {
    unsigned int is_active : 1;
    unsigned int level : 8;
};

int main() {
    struct Flags f = {1, 100};

    // printf("地址: %p\n", &f.is_active);  // 错误！不能取地址
    // int *ptr = &f.is_active;              // 错误！

    printf("is_active=%d, level=%d\n", f.is_active, f.level);

    return 0;
}
```

> **为什么不能取地址？** 因为位域成员可能不是从字节开头开始的，CPU 没有办法直接对"几位"取地址。地址的粒度是字节，不是位。所以 `&f.is_active` 这样的表达式是非法的。

### 11.10.2 位域对齐规则（实现相关）

位域的对齐规则非常复杂，不同编译器有不同实现。但有几个通用规则：

1. **一个位域不能跨两个存储单元**（如果一个位域放不下，编译器会把它放到下一个存储单元）
2. **位域的存储单元大小**取决于编译器（通常是 int 或更大的类型）
3. **匿名位域**可以用来调整对齐：

```c
#include <stdio.h>

struct BitfieldDemo {
    unsigned int a : 3;   // 占 3 位
    unsigned int : 5;     // 匿名位域，跳过 5 位
    unsigned int b : 8;   // 占 8 位
};

int main() {
    struct BitfieldDemo d = {7, 255};
    printf("大小: %zu 字节\n", sizeof(struct BitfieldDemo));
    printf("a=%u, b=%u\n", d.a, d.b);

    return 0;
}
```

> **匿名位域** `unsigned int : 5;` 表示跳过 5 位不用。这就像在排队的时候插队说"这 5 个位置空着，下一个从第 9 位开始"。

---

## 11.11 枚举（Enum）：定义命名常量

枚举是用来定义一组相关的**命名常量**的。它的本质就是一组整数，只是给了它们好听的名字。

```c
#include <stdio.h>

// 定义一个颜色枚举
enum Color {
    RED,     // 0
    GREEN,   // 1
    BLUE     // 2
};

// 也可以显式赋值
enum Weekday {
    MONDAY = 1,
    TUESDAY = 2,
    WEDNESDAY = 3,
    THURSDAY = 4,
    FRIDAY = 5,
    SATURDAY = 6,
    SUNDAY = 7
};

int main() {
    enum Color c = RED;
    enum Weekday day = FRIDAY;

    printf("颜色: %d (0=红, 1=绿, 2=蓝)\n", c);
    printf("今天是周%d\n", day);

    // 枚举也可以当整数用
    for (int i = MONDAY; i <= SUNDAY; i++) {
        printf("%d ", i);
    }
    printf("\n");

    return 0;
}
```

输出：

```
颜色: 0 (0=红, 1=绿, 2=蓝)
今天是周5
1 2 3 4 5 6 7
```

### 11.11.1 ⚠️ C 语言枚举固定为 `int` 类型，不支持指定其他底层整数类型

> **这是 C 语言和 C++ 差得最大的地方之一！**

在 C++11 里，你可以写 `enum class Color : unsigned char { RED, GREEN, BLUE };`，这样枚举的底层类型就是 `unsigned char`。

但在 **C 语言里，枚举的底层类型固定是 `int`**（标准规定至少能表示 `int` 的范围）。你没法改成 `char`、`short`、或者 `unsigned int`：

```c
// C 语言不支持这种语法！
// enum Color : unsigned char { RED, GREEN, BLUE };  // 错误！C 编译不过

// C++ 可以：
// enum class Color : unsigned char { RED, GREEN, BLUE };  // C++11 支持
```

> 如果你在 C 代码里看到 `: unsigned char` 这样的东西，那一定是 C++ 代码，不是 C 语言。

### 11.11.2 枚举的 typedef 简化命名

和结构体一样，枚举前面也可以加 `typedef`，省掉 `enum` 关键字：

```c
#include <stdio.h>

// 不用 typedef
enum Status {
    OK,
    ERROR,
    PENDING
};
enum Status s1 = OK;

// 用 typedef
typedef enum {
    SUCCESS,
    FAILURE,
    UNKNOWN
} Result;  // Result 就是枚举类型别名

Result r1 = SUCCESS;
```

---

## 11.12 `sizeof` 结构体（考虑 padding）

前面 11.3 节已经讨论过内存对齐，这里再总结一下 `sizeof` 结构体时要注意的点：

```c
#include <stdio.h>
#include <stddef.h>

struct Person {
    char name[10];   // 10 字节
    int age;         // 4 字节（可能需要 2 字节 padding）
    double height;   // 8 字节
};

int main() {
    printf("sizeof(char[10])  = %zu\n", sizeof(char[10]));
    printf("sizeof(int)       = %zu\n", sizeof(int));
    printf("sizeof(double)    = %zu\n", sizeof(double));

    printf("\nstruct Person 大小 = %zu 字节\n", sizeof(struct Person));
    printf("offsetof(name)  = %zu\n", offsetof(struct Person, name));
    printf("offsetof(age)    = %zu\n", offsetof(struct Person, age));
    printf("offsetof(height) = %zu\n", offsetof(struct Person, height));

    return 0;
}
```

输出（在我的 64 位系统上）：

```
sizeof(char[10])  = 10
sizeof(int)       = 4
sizeof(double)    = 8

struct Person 大小 = 32 字节
offsetof(name)  = 0
offsetof(age)    = 12
offsetof(height) = 24
```

可以看到：`age` 前面有 2 字节 padding（因为 `int` 要对齐到 4 字节边界），`height` 前面有 4 字节 padding（因为 `double` 要对齐到 8 字节边界）。最后还有 8 字节 padding（让整个结构体大小是最大成员 8 的倍数）。

---

## 11.13 `_Static_assert`（C11）：编译期断言

有时候我们希望在**编译时**就检查某个条件是否成立，而不是等到运行时报错。比如你写了一个网络协议包，假设 `int` 必须是 4 字节，如果不是，编译就应该失败而不是偷偷出 bug。

`static_assert`（C11 的宏名是 `_Static_assert`，C23 简化成了 `static_assert`）就是干这个的：

### 11.13.1 `static_assert`（C23）：不需要括号

**C23 版本（更简洁）：**

```c
#include <stdio.h>

// C23: static_assert 不需要额外的括号
static_assert(sizeof(int) == 4, "int 必须占 4 字节");
static_assert(sizeof(void*) == 8, "只支持 64 位系统");

struct Packet {
    char header[4];
    int payload;
};

int main() {
    printf("sizeof(Packet) = %zu\n", sizeof(struct Packet));
    return 0;
}
```

**C11 版本（稍微繁琐一点）：**

```c
#include <stdio.h>

// C11: _Static_assert(表达式, "消息字符串");
_Static_assert(sizeof(int) == 4, "int 必须占 4 字节");

struct Packet {
    char header[4];
    int payload;
};

int main() {
    printf("sizeof(Packet) = %zu\n", sizeof(struct Packet));
    return 0;
}
```

如果条件不满足（比如在 16 位系统上 `sizeof(int) != 4`），编译会直接失败，并显示你写的消息：

```
error: static_assert failed: "int 必须占 4 字节"
```

> **编译期断言 vs 运行期断言**：
> - `assert()` 是**运行期**断言，程序跑起来才检查，不满足就崩溃
> - `_Static_assert` / `static_assert` 是**编译期**断言，编译不过就不生成可执行文件
>
> 编译期能检查的问题，就不要留到运行期。早发现，早治疗！

---

## 本章小结

本章我们学习了 C 语言中三种重要的自定义类型：

1. **结构体（Struct）**：把不同类型的数据打包成一个整体，就像一个万能收纳盒。成员访问用 `.`（变量）或 `->`（指针）。传大结构体给函数时，**优先传指针**避免复制开销。结构体有内存对齐规则，大小通常是最大成员的对齐倍数，中间可能填充 padding。

2. **共用体（Union）**：所有成员共享同一块内存，大小等于最大成员的大小。适合需要同一块内存存不同类型数据的场景，比如大小端检测、带标签的变体类型（Tagged Union）。

3. **枚举（Enum）**：定义一组命名常量，底层类型固定是 `int`（C 语言，不支持指定其他类型）。可以用 `typedef` 简化命名。

4. **位域（Bit-field）**：用位数而不是字节来定义成员，可以压缩空间，但不能对位域取地址（`&` 不适用）。

5. **`_Static_assert` / `static_assert`**：编译期断言，在编译时检查条件，不满足则编译失败。

这些概念在系统编程、嵌入式开发、网络协议、游戏开发等领域都有广泛应用。掌握好它们，你的数据组织能力会提升一大截！

> "编程的精髓在于选择合适的数据结构。" —— C.A.R. Hoare
