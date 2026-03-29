+++
title = "第 14 章：动态内存管理 —— 程序的'房产证'之争"
weight = 140
date = "2026-03-29T22:34:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 第 14 章：动态内存管理 —— 程序的"房产证"之争

想象一下，你租房子住。

- **静态内存** 就像你买了一套公寓，大小固定，格局固定，你想在客厅放张床？门都没有！因为公寓的墙是"浇筑"好的，不能改。
- **动态内存** 就像你包下了一整块空地，今天想建小茅屋，明天想建大别墅，后天拆了建游泳池——随你心情，想怎么折腾就怎么折腾！

动态内存管理，是 C 语言中最强大、最危险、也是面试官最爱的技能之一。学会了，你就是"内存大亨"；学废了，分分钟把程序写成"内存凶杀案现场"。准备好了吗？我们出发！

---

## 14.1 先搞清楚战场：程序的内存布局

程序运行起来之后，操作系统会给你分配一块"虚拟内存空间"（别被"虚拟"两个字吓到，你就当它是一块真实的大蛋糕就好）。这块蛋糕从上到下，被切成了不同的区域，每个区域有各自的用途。

我们先上一张图，让你有个直观印象：

```
┌─────────────────────────────────────┐  高地址
│            内核空间                  │  (Kernel Space)
├─────────────────────────────────────┤
│                                     │
│    栈 (Stack) ←── 向下增长          │
│    存放：局部变量、函数参数、返回地址 │
│                                     │
├─────────────────────────────────────┤
│                                     │
│    ·····························     │
│    ··· (空闲区域) ···············    │
│    ·····························     │
│                                     │
├─────────────────────────────────────┤
│                                     │
│    堆 (Heap) ←── 向上增长           │
│    存放：动态分配的内存              │
│                                     │
├─────────────────────────────────────┤
│    全局数据区 (Data Segment)         │
│    存放：全局变量、静态变量           │
├─────────────────────────────────────┤
│    只读数据区 (RO Data)              │
│    存放：常量字符串、const 变量       │
├─────────────────────────────────────┤
│    代码区 (Text Segment)            │
│    存放：程序的机器指令              │
└─────────────────────────────────────┘  低地址
```

> **小贴士：** 你可能会好奇为什么这图里"堆"和"栈"中间隔着一大块空白？这是因为操作系统给每个程序分配的虚拟地址空间很大（比如 32 位系统通常是 4GB），但实际用到的就那么一小块，剩下的就是"空闲地带"，谁也没占着。

现在我们逐个认识这些区域：

### 代码区（Text Segment）

这是程序的"灵魂"所在，存放的是 CPU 能看懂的机器指令——也就是你写的 `if`、`for`、`printf` 翻译成的二进制指令。

**特点：只读，不可修改。** 你要是尝试往代码区写东西，操作系统会一巴掌拍死你的程序（段错误）。

### 只读数据区（RO Data）

存放程序中的"常量"。比如你写的字符串字面量 `"Hello, World!"`，还有用 `const` 修饰的全局常量。

### 全局数据区（Data Segment）

存放**全局变量**和**静态变量**（`static` 修饰的变量）。这些家伙程序一启动就存在，程序结束才消失。

### 栈（Stack）

**栈是函数的"工作间"。** 每次调用一个函数，就会在栈上开辟一块空间，叫"栈帧"（Stack Frame）。局部变量、函数参数、返回地址都存在这里。

栈的特点：**自动管理**，你不用操心。函数一返回，这块空间就被"自动回收"了。栈的分配/释放速度极快，因为本质上就是移动一个指针（叫"栈顶指针"）。

但栈也有缺点：**空间太小**（通常默认几 MB），而且大小在编译时就固定了——你没法在运行时决定"我要 1000 个局部变量数组"。

### 堆（Heap）

**堆才是我们的主角！** 堆是一大块"未分配"的内存空间，你可以随时向操作系统申请使用，用完再还回去。

堆的特点：**灵活，非常灵活！** 想分配多少字节都行（受物理内存限制），大小在运行时决定。但代价是：**你得自己管理！** 分配了要记得释放，释放了要记得别再用。这些"内存管理的脏活累活"，全丢给程序员了。

> **生活比喻：** 想象你去住酒店。栈就像酒店给你的"标准间"，床位固定（固定大小），你入住时自动分配，退房时自动回收，很方便但没得选。堆就像酒店旁边的"空地"，你爱怎么搭帐篷都行（灵活大小），但你得自己搭、自己拆。

---

## 14.2 为什么需要动态内存分配？

你可能会问："局部变量用得好好的，为啥要搞动态内存？"

好问题！让我们场景还原：

### 场景一：数组大小在运行时才确定

```c
int main() {
    printf("请输入要处理的学生数量：");
    int n;
    scanf("%d", &n);

    // n 是用户输入的，可能是 100，也可能是 100000
    // 请问你怎么用局部变量声明数组？
    // int scores[n];  // C99 变长数组可以，但栈空间有限！
    // 如果 n = 1000000，栈直接爆了！
}
```

`int scores[n]` 虽然 C99 支持变长数组（VLA），但它是在**栈**上分配的。栈就那么大，如果 `n` 太大，直接栈溢出（Stack Overflow）！

动态内存就不一样了——堆的空间比栈大得多（受物理内存限制，通常是几 GB），可以轻松 hold 住。

### 场景二：数据的生命周期需要跨越函数

```c
void process() {
    // 这个数组只有 process 函数能用
    int data[100];
    // process 结束，data 就没了
}

// 想让某个数据在多个函数之间共享？
// 局部变量做不到！
```

如果数据需要**动态决定生命周期**——比如在函数之间传递、在多个模块之间共享——就得用动态内存。动态分配的内存在 `free` 之前**一直有效**，不会因为函数返回就消失。

### 场景三：需要动态扩展的数据结构

比如你写一个通讯录程序，用户不断往里加联系人：

```c
// 用数组？数组大小固定，不好扩展
// 用动态内存？想加人就 realloc 扩大，完美！
```

**结论：** 动态内存分配是 C 语言的精髓之一。没有它，你写不出链表、树、哈希表这些"高级数据结构"；没有它，你的程序就像被锁死的公寓，想扩展？门都没有！

---

## 14.3 `malloc`：在堆上开疆拓土

终于轮到主角登场了！`malloc` 是 "memory allocation" 的缩写，翻译过来就是"内存分配"。

### 函数签名

```c
#include <stdlib.h>

void *malloc(size_t size);
```

- **参数：** `size` —— 你想要多少**字节**（bytes）
- **返回值：** 成功返回分配好的内存的**首地址**（`void *` 类型），失败返回 `NULL`

### 最简单的使用

```c
#include <stdio.h>
#include <stdlib.h>

int main() {
    // 分配一个 int 大小的内存（约 4 字节）
    int *p = (int *)malloc(sizeof(int));

    if (p == NULL) {
        printf("内存分配失败！程序要崩了！\n");
        return 1;
    }

    *p = 42;
    printf("我分配了一个 int，值是：%d\n", *p);
    // 输出：我分配了一个 int，值是：42

    free(p);  // 用完记得释放！
    p = NULL; // 释放后指针置空，避免野指针

    return 0;
}
```

> **注意：** 上面代码中，我用了 `(int *)` 对 `malloc` 的返回值做了**强制类型转换**。在 C89/C90 中，这是必须的！但从 **C89 起（包括 C99、C11、C17、C23）**，如果你 `#include <stdlib.h>` 了，**`malloc` 返回 `void *`，可以直接赋给任何类型的指针，不需要强制转换**。
>
> 举例：`int *p = malloc(sizeof(int));` —— 完全合法，简洁美观！
>
> 为什么不推荐强制转换？有两个原因：
> 1. **多余代码**：C 语言会自动做 `void *` 到其他指针类型的隐式转换，多写等于画蛇添足
> 2. **掩盖错误**：如果你忘了 `#include <stdlib.h>`，编译器会警告你（因为 `void *` 不能隐式转换）。但如果你强制转换了，编译器就不警告了，错误就被隐藏了！

### 分配一块连续的内存（比如数组）

```c
#include <stdio.h>
#include <stdlib.h>

int main() {
    int n = 5;

    // 分配 5 个 int 的连续内存
    int *arr = (int *)malloc(n * sizeof(int));

    if (arr == NULL) {
        printf("内存分配失败！\n");
        return 1;
    }

    // 初始化数组
    for (int i = 0; i < n; i++) {
        arr[i] = (i + 1) * 10;
    }

    // 打印
    for (int i = 0; i < n; i++) {
        printf("arr[%d] = %d\n", i, arr[i]);
    }
    // 输出：
    // arr[0] = 10
    // arr[1] = 20
    // arr[2] = 30
    // arr[3] = 40
    // arr[4] = 50

    free(arr);
    arr = NULL;

    return 0;
}
```

> **小贴士：** 用 `malloc` 分配的内存，**里面的内容是"脏"的**——即使用 `%d` 打印，你看到的也是上次别人用过的"垃圾值"，不是什么 `0` 哦！别误以为会自动初始化为 0。

### `sizeof` 的一些技巧

```c
// 方法一：直接写死大小（不推荐）
int *p = (int *)malloc(100 * sizeof(int));

// 方法二：用 sizeof 自动算（推荐！）
int *p = (int *)malloc(n * sizeof(int));
// 或者更优雅：
int *p = (int *)malloc(n * sizeof *p);  // 不用写类型名，改了类型也能用！
```

`sizeof *p` 这种写法非常妙——它根据 `p` 指向的类型自动计算大小，代码可维护性极高。

---

## 14.4 `calloc`：分房还带精装修

如果说 `malloc` 是分给你一块"毛坯房"，那 `calloc` 就是"精装修房"——分配内存的同时，还帮你把房子打扫得干干净净（**全部初始化为 0**）。

### 函数签名

```c
#include <stdlib.h>

void *calloc(size_t nmemb, size_t size);
```

- **参数 `nmemb`**：你要分配多少个"元素"（number of members）
- **参数 `size`**：每个元素多大（bytes）
- **返回值：** 和 `malloc` 一样，成功返回首地址，失败返回 `NULL`

### `malloc` vs `calloc`

```c
#include <stdio.h>
#include <stdlib.h>

int main() {
    // malloc：分配 5 个 int，内容是脏的
    int *a = (int *)malloc(5 * sizeof(int));

    // calloc：分配 5 个 int，内容全是 0
    int *b = (int *)calloc(5, sizeof(int));

    printf("malloc 分配的数组：");
    for (int i = 0; i < 5; i++) {
        printf("%d ", a[i]);  // 脏数据，未定义
    }
    printf("\n");

    printf("calloc 分配的数组：");
    for (int i = 0; i < 5; i++) {
        printf("%d ", b[i]);  // 全是 0
    }
    printf("\n");
    // 输出（malloc 的值未定义，这里显示的是残留垃圾）：
    // malloc 分配的数组：-842150451 -842150451 -842150451 -842150451 -842150451
    // calloc 分配的数组：0 0 0 0 0

    free(a);
    free(b);

    return 0;
}
```

> **选择建议：** 如果你分配内存后要立刻全部写入（覆盖掉原来的值），用 `malloc`（省了清零的开销）。如果你不确定要不要全部写入，用 `calloc` 更安全——至少不会因为没初始化就读取而出现奇怪的 bug。

---

## 14.5 `realloc`：房子不够住了？换大的！

当你发现"毛坯房"不够住了，想扩建怎么办？`realloc` 就是你的"拆迁队"！

### 函数签名

```c
#include <stdlib.h>

void *realloc(void *ptr, size_t size);
```

- **参数 `ptr`**：之前 `malloc`/`calloc`/`realloc` 分配的内存地址
- **参数 `size`**：新的总大小（字节）
- **返回值：** 新地址（注意！可能和旧地址不同！）

### 关键特性：可能"搬家"

这是 `realloc` 最容易让人踩坑的地方：

```
旧地址：[....数据....][空白区]
                        ↓ realloc 申请更大空间
新地址：[....数据....][新扩展的空白区]  ← 地址可能变了！
```

如果原来那块内存后面还有足够的空闲空间，`realloc` 就在原地扩展，返回原地址。

但如果后面不够了，`realloc` 会**另找一块足够大的新地方，把旧数据复制过去，然后释放旧地址**。这时候地址就变了！

### 使用示例

```c
#include <stdio.h>
#include <stdlib.h>

int main() {
    int *arr = (int *)calloc(3, sizeof(int));
    if (arr == NULL) {
        return 1;
    }

    arr[0] = 10;
    arr[1] = 20;
    arr[2] = 30;

    printf("扩展前的数组：");
    for (int i = 0; i < 3; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");
    // 输出：扩展前的数组：10 20 30

    // 扩展到 6 个元素
    int *new_arr = (int *)realloc(arr, 6 * sizeof(int));

    if (new_arr == NULL) {
        printf("realloc 失败！但 arr 还是有效的，别忘了 free！\n");
        free(arr);
        return 1;
    }

    // 重要：如果 realloc 返回了新地址，原来的 arr 就无效了！
    // 所以我们用 new_arr，以后都用 new_arr
    arr = new_arr;  // 如果不想换名字，这步很重要！

    // 新增两个元素
    arr[3] = 40;
    arr[4] = 50;
    arr[5] = 60;

    printf("扩展后的数组：");
    for (int i = 0; i < 6; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");
    // 输出：扩展后的数组：10 20 30 40 50 60

    free(arr);
    arr = NULL;

    return 0;
}
```

> **⚠️ 警告：** `realloc` 失败时返回 `NULL`，但**原来的内存块仍然是有效的**！很多新手会犯这个错误：先保存 `realloc` 的结果到一个临时变量，检查 `NULL` 之后，再赋值给原来的指针。直接 `ptr = realloc(ptr, new_size)` 是非常危险的做法——万一失败，`ptr` 就被覆盖成了 `NULL`，原来的地址就丢了，内存泄漏！

正确做法：
```c
void *tmp = realloc(ptr, new_size);
if (tmp == NULL) {
    // 处理错误，ptr 仍然有效
    free(ptr);
    return -1;
}
ptr = tmp;  // 成功后更新
```

---

## 14.6 `free`：有借有还，再借不难

终于说到"还房子"了！`free` 就是把之前借的内存还给操作系统。

### 函数签名

```c
#include <stdlib.h>

void free(void *ptr);
```

### 最重要的规则

```c
free(p);   // 正确：释放 malloc/calloc/realloc 返回的指针
free(NULL); // 安全：free(NULL) 什么也不做，完全合法
```

### ⚠️ 切勿释放非 `malloc`/`calloc`/`realloc` 返回值！

这是 C 语言中最容易犯的错误之一，也是最致命的一个。请记住：

> **只能 `free` 通过 `malloc` / `calloc` / `realloc` 获得的指针！**
>
> 只能 `free` 一次！不能重复 `free`！
>
> 不能 `free` 栈上的地址！不能 `free` 全局变量的地址！

以下全部是**犯罪现场**：

```c
// 罪行一：free 栈上的地址
int x = 10;
free(&x);  // ❌ 大错特错！x 在栈上，不是堆！

// 罪行二：free 常量区地址
char *s = "hello";
free(s);   // ❌ "hello" 在只读数据区，不能动！

// 罪行三：free 局部数组
int arr[10];
free(arr); // ❌ arr 在栈上！

// 罪行四：free 已经 free 过的
free(p);
free(p);   // ❌ 双重 free，undefined behavior！

// 罪行五：free 部分地址
int *arr = (int *)malloc(10 * sizeof(int));
free(arr + 3); // ❌ 只能 free 原始指针！
```

> **生活比喻：** 你借了一套公寓，`free` 就是还钥匙。你不能把钥匙还了之后还继续住（悬挂指针），也不能把别人家的钥匙还了（free 非堆地址），更不能同一套公寓的钥匙还两次（双重 free）。

### 释放后立即置空

```c
free(p);
p = NULL;  // 重要！防止悬挂指针
```

`free` 之后，指针 `p` 指向的那块内存虽然被归还了，但 `p` 本身的值**没有变**——它仍然指向原来的地址，这就是著名的"**悬挂指针**"（dangling pointer）。下次不小心用了这个指针，就是未定义行为。所以 `free` 后**立即把指针设为 `NULL`** 是一个好习惯。

---

## 14.7 内存分配返回值必须检查！

这是一个被无数面试官追问过的问题：**你 `malloc` 之后检查返回值了吗？**

操作系统不是无限的。当内存耗尽时，`malloc`/`calloc`/`realloc` 会返回 `NULL`。如果你不检查就继续用，程序就会试图访问地址 `0x0`（`NULL`），轻则程序崩溃，重则数据损坏。

### 标准范式

```c
#include <stdio.h>
#include <stdlib.h>

int main() {
    // 分配一块巨大的内存
    size_t huge = (size_t)-1;  // 最大值

    void *p = malloc(huge);
    if (p == NULL) {
        printf("内存分配失败！别硬撑了！\n");
        return 1;  // 或者妥善处理错误
    }

    printf("分配成功，地址是：%p\n", p);
    free(p);

    return 0;
}
```

> **小贴士：** 在现代桌面系统上，`malloc` 很少失败（因为有虚拟内存机制）。但在嵌入式系统、资源受限环境、或者处理超大内存分配时，`NULL` 检查是**必须的**。

---

## 14.8 常见内存错误 —— 程序员的花式作死大全

动态内存是 C 语言的"修罗场"。下面这些错误，如果你不认真学习，分分钟全部踩一遍！

### 14.8.1 野指针（未初始化指针）

**什么是野指针？** 就是"指向未知领地的指针"——指针声明了但没初始化，里面装的是随机垃圾值。

```c
int *p;        // 野指针！此时 p 的值是随机的
printf("%d", *p);  // ❌ 访问随机地址，程序可能直接爆炸
```

**野指针的三大来源：**

1. **声明指针时没初始化**
   ```c
   int *p;   // 随机值
   int *p = NULL;  // ✅ 初始化为 NULL
   ```

2. **指针指向的内存被 `free` 了**
   ```c
   int *p = (int *)malloc(sizeof(int));
   free(p);
   printf("%d", *p);  // ❌ free 后继续用，悬挂指针
   ```

3. **指针超出了作用域**
   ```c
   int *func() {
       int x = 10;
       return &x;  // ❌ x 在栈上，函数返回后就无效了
   }
   ```

> **生活比喻：** 野指针就像一张写了一半的地址卡，你根本不知道它指向哪里，可能是你家隔壁，也可能是火星。访问它轻则程序崩溃，重则把别人的数据踩得稀烂。

### 14.8.2 重复 `free`

这是**未定义行为**（Undefined Behavior）的典型代表。

```c
int *p = (int *)malloc(sizeof(int));
free(p);
free(p);  // ❌ 重复 free，同一块内存 free 两次！
```

为什么会出问题？因为 `free` 之后，内存已经还给操作系统了，但 `p` 还是指向那块地址。第二次 `free` 的结果完全不可预测——可能什么也不发生，可能程序崩溃，可能踩到其他数据……

### 14.8.3 内存泄漏（长期运行程序的隐形杀手）

**内存泄漏**（Memory Leak）就是"分配了内存但忘了释放"。对于一次性运行的程序来说，可能影响不大；但对于服务器、守护进程这些**长期运行的程序**，内存泄漏就像水龙头没关紧——慢慢慢慢地，内存就被耗尽了。

```c
void leak_example() {
    int *p = (int *)malloc(sizeof(int));
    *p = 100;
    // 函数结束了，但 p 没有 free！
    // 每次调用 leak_example，就泄漏一个 int 的内存！
}
```

服务器如果每秒调用一次这个函数，一小时后你就泄漏了 3600 个 int。运行一天？72 MB 没了。

**如何检测内存泄漏？** 后面我们会讲 `valgrind` 和 AddressSanitizer。

### 14.8.4 越界访问（缓冲区溢出）

分配的内存是一块有限的空间，访问超出范围就是越界。

```c
int *arr = (int *)malloc(5 * sizeof(int));  // 分配了 5 个 int 的空间

for (int i = 0; i <= 5; i++) {  // ⚠️ i 从 0 到 5，共 6 次！
    arr[i] = i;  // arr[5] 越界了！
}
```

`arr[5]` 越界访问会修改堆上的其他数据（或者元数据），后果可能是：
- 改了别人的数据，程序算出了错误的结果
- 改了堆的元数据，下次 `malloc`/`free` 直接崩溃
- 被黑客利用，执行任意代码（著名的缓冲区溢出攻击原理）

> **生活比喻：** 你订了一个 5 人份的披萨，结果叫了 6 个人来吃。第 6 个人吃的是别人家的披萨——要么别人找上门，要么你被物业赶走。

### 14.8.5 悬挂指针（`free` 后继续使用）

这其实是野指针的一种，但值得单独拿出来讲：

```c
int *p = (int *)malloc(sizeof(int));
*p = 42;

free(p);  // 内存还给系统了
printf("%d\n", *p);  // ❌ 还在用！这是悬挂指针
```

`free` 后继续使用，访问的是已经不属于你的内存。可能看起来"还能用"（因为那块内存还没被其他代码用到），但这纯属运气——下次 `malloc` 分配到这块内存，你的程序就彻底乱了。

---

## 14.9 内存检测工具 —— 你的内存"监控摄像头"

写 C 语言程序，内存错误是家常便饭。好消息是，有很多工具能帮你"监控"内存问题，就像程序员的 X 光机。

### valgrind（Linux / macOS）

`valgrind` 是 Linux 下最强大的内存检测工具，专门用来抓内存泄漏、越界访问、使用未初始化内存等错误。

**安装（Linux）：**
```bash
sudo apt install valgrind   # Debian/Ubuntu
sudo yum install valgrind   # RHEL/CentOS
```

**安装（macOS）：**
```bash
brew install valgrind
```

**使用：**
```bash
valgrind --leak-check=full ./my_program
```

假设我们的程序有内存泄漏：
```c
// leak.c
#include <stdlib.h>

void leak() {
    int *p = (int *)malloc(sizeof(int));
    *p = 42;
    // 忘记 free 了！
}

int main() {
    leak();
    leak();
    leak();
    return 0;
}
```

编译并运行：
```bash
gcc -g leak.c -o leak
valgrind --leak-check=full ./leak
```

`valgrind` 会输出：
```
==12345== Memcheck, a memory error detector
==12345== Copyright (C) 2002-2017, and GNU GPL'd, by Julian Seward et al.
...
==12345== HEAP SUMMARY:
==12345==     in use at exit: 12 bytes in 3 blocks
==12345==   total heap usage: 3 allocs, 0 frees, 12 bytes allocated
==12345== 
==12345== LEAK SUMMARY:
==12345==    definitely lost: 12 bytes in 3 blocks
==12345==       ...

All heap blocks were freed -- no leaks are possible  // 只有 all free 了才显示这句
```

> **小贴士：** `valgrind` 只能在 Linux/macOS 上跑，不支持 Windows。

### Visual Leak Detector（Windows + Visual Studio）

Windows 用户如果用 Visual Studio 写 C/C++，可以用 **Visual Leak Detector**（VLD）插件。

**使用方法：**
1. 下载并安装 VLD
2. 在代码中加一行：
   ```c
   #include <vld.h>
   ```
3. 正常编译运行，程序退出时会自动输出内存泄漏报告

### AddressSanitizer（交叉平台，高性能）

AddressSanitizer（简称 ASan）是 Google 开发的编译器级内存检测工具，比 `valgrind` 快 2 倍左右（10-50 倍加速！），非常适合生产环境和 CI/CD。

**使用超级简单，编译时加个 flag：**
```bash
gcc -fsanitize=address -g leak.c -o leak
./leak
```

运行时如果有内存错误，会立即报错：
```
=================================================================
==12345== ERROR: AddressSanitizer: heap-buffer-overflow on address 0x602000000030
    #0 0x7f7... in main leak.c:6
...
```

AddressSanitizer 可以检测：
- 堆、栈、全局变量的缓冲区溢出
- 使用 `free` 后的内存（悬挂指针）
- 双重 free
- 内存泄漏（需要额外工具）

> **推荐：** 在开发和测试阶段，用 `gcc -fsanitize=address -g -O1` 编译（不要用 `-O2` 或更高优化，否则错误信息可能不够准确）。发布版本不要带 sanitizer！

---

## 14.10 C11 `aligned_alloc` —— 对齐我有特殊要求

### 什么是内存对齐？

现代 CPU 访问内存有"对齐要求"——某些类型的数据必须放在特定倍数的地址上。比如 `int`（4 字节）最好在 4 的倍数地址上，`double`（8 字节）最好在 8 的倍数地址上。

如果不对齐，CPU 需要两次内存访问才能读到一个数据，性能会下降；在某些架构上甚至直接报错。

### 函数签名

```c
#include <stdlib.h>

void *aligned_alloc(size_t alignment, size_t size);
```

- **`alignment`**：对齐要求，必须是 2 的幂（如 8, 16, 32, 64……）
- **`size`**：要分配的字节数，**必须是 `alignment` 的倍数**（这是 C 标准的要求）

### 示例：分配 16 字节对齐的内存

```c
#include <stdio.h>
#include <stdlib.h>

int main() {
    // 分配 64 字节，16 字节对齐
    void *p = aligned_alloc(16, 64);

    if (p == NULL) {
        printf("对齐分配失败！\n");
        return 1;
    }

    printf("分配的地址：%p\n", p);
    printf("地址模 16 的余数：%zu\n", (size_t)p % 16);
    // 如果对齐正确，余数应该是 0

    free(p);

    return 0;
}
```

> **使用场景：** `aligned_alloc` 常用于：
> - SIMD 指令集编程（如 SSE/AVX，需要 16/32 字节对齐的数据）
> - 编写自定义内存分配器
> - 与硬件外设通信（外设寄存器地址往往有对齐要求）

---

## 14.11 内存池技术 —— 未雨绸缪的内存管理

### 什么是内存池？

想象你要举办一场万人演唱会。如果每个人来都要你现场建一个新房子给他住，你是不是得累死？`malloc`/`free` 就是这样——每次分配都要找操作系统要内存，效率不高（系统调用有开销）。

**内存池（Memory Pool）** 是一种"预分配"技术：提前向操作系统要一大块内存放在池子里，之后程序需要内存时，直接从池子里"切"一块给你，快得跟从冰箱拿饮料一样！只有池子空了，才再向操作系统要新的一大块。

```
操作系统 ──大块──▶ 内存池（预分配）──小块──▶ 程序
                  ↑                      ↑
            一次系统调用              N 次快速分配
```

### 最简单的固定块内存池

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define BLOCK_SIZE 256       // 每个块的大小
#define POOL_SIZE  10        // 池子里块的数量

typedef struct MemBlock {
    char data[BLOCK_SIZE];
    int used;
} MemBlock;

typedef struct MemPool {
    MemBlock *blocks;
    int pool_size;
    int free_count;
} MemPool;

// 初始化内存池
MemPool *pool_create(int pool_size) {
    MemPool *pool = (MemPool *)malloc(sizeof(MemPool));
    if (pool == NULL) return NULL;

    pool->blocks = (MemBlock *)calloc(pool_size, sizeof(MemBlock));
    if (pool->blocks == NULL) {
        free(pool);
        return NULL;
    }

    pool->pool_size = pool_size;
    pool->free_count = pool_size;
    return pool;
}

// 从池子分配一个块
void *pool_alloc(MemPool *pool) {
    if (pool->free_count == 0) {
        printf("池子空了！需要扩容或处理错误。\n");
        return NULL;
    }

    for (int i = 0; i < pool->pool_size; i++) {
        if (!pool->blocks[i].used) {
            pool->blocks[i].used = 1;
            pool->free_count--;
            return pool->blocks[i].data;
        }
    }
    return NULL;  // 不应该走到这里
}

// 释放一个块回池子
void pool_free(MemPool *pool, void *ptr) {
    if (ptr == NULL) return;

    for (int i = 0; i < pool->pool_size; i++) {
        if (pool->blocks[i].data == ptr) {
            pool->blocks[i].used = 0;
            pool->free_count++;
            return;
        }
    }
}

// 销毁内存池
void pool_destroy(MemPool *pool) {
    free(pool->blocks);
    free(pool);
}

// 测试
int main() {
    MemPool *pool = pool_create(POOL_SIZE);
    if (pool == NULL) return 1;

    printf("池子创建成功！总块数：%d\n", pool->pool_size);
    // 输出：池子创建成功！总块数：10

    char *buf1 = (char *)pool_alloc(pool);
    char *buf2 = (char *)pool_alloc(pool);
    char *buf3 = (char *)pool_alloc(pool);

    strcpy(buf1, "第一条消息");
    strcpy(buf2, "第二条消息");
    strcpy(buf3, "第三条消息");

    printf("buf1: %s\n", buf1);
    printf("buf2: %s\n", buf2);
    printf("buf3: %s\n", buf3);
    printf("剩余空闲块：%d\n", pool->free_count);
    // 输出：
    // buf1: 第一条消息
    // buf2: 第二条消息
    // buf3: 第三条消息
    // 剩余空闲块：7

    pool_free(pool, buf2);
    printf("释放 buf2 后，剩余空闲块：%d\n", pool->free_count);
    // 输出：释放 buf2 后，剩余空闲块：8

    pool_destroy(pool);

    return 0;
}
```

### 内存池的优势

| 对比项 | 直接用 `malloc`/`free` | 内存池 |
|---|---|---|
| 系统调用次数 | 每次分配都要 | 池空时才要 |
| 分配速度 | 慢（系统调用开销） | 快（池内指针操作） |
| 内存碎片 | 容易产生（频繁分配释放） | 少（固定大小块） |
| 适用场景 | 大小不一的通用分配 | 大小固定的重复分配 |

> **典型应用场景：**
> - **网络服务器**：每个连接/请求处理完后，立即释放，用内存池效率极高
> - **游戏开发**：大量小对象（粒子、子弹、特效）的创建和销毁
> - **嵌入式系统**：减少系统调用开销

---

## 14.12 常见面试题：Buddy 算法 / Slab 分配器

这一节我们来看看操作系统和高级语言虚拟机中实际使用的内存分配算法。面试官最爱拿这些来"为难"你了！

### Buddy 算法（伙伴算法）

**Buddy 算法**是一种经典的内存分配算法，核心思想是：**始终将内存分裂成"伙伴"——大小相等，地址连续的两个块**。

```
初始：有一块 64KB 的内存

分配 8KB：
  64KB → 32KB + 32KB（右边这块备用）
          32KB → 16KB + 16KB（右边备用）
              16KB → 8KB + 8KB（右边备用）
                  8KB ← 分配出去！

释放时：
  如果"伙伴"（buddy）也是空闲的，就合并成更大的块！
  8KB + 8KB（伙伴空闲） → 16KB
  16KB + 16KB（伙伴空闲）→ 32KB
  ...一直合并到 64KB
```

**Buddy 算法的优点：** 合并（coalesce）非常简单——因为伙伴的地址关系是确定的，合并只需 O(1) 时间。

**Buddy 算法的缺点：** 内存利用率不高——即使只需要 9KB，也得分配 16KB（下一档）。这叫**内部碎片**（分配的块比实际用的大）。

```c
// Buddy 算法分配的块大小必须是 2 的幂
// 2^0=1, 2^1=2, 2^2=4, 2^3=8, 2^4=16, 2^5=32, ...
```

### Slab 分配器

**Slab 分配器**是 Linux 内核使用的内存分配技术（1994 年由 Sun 的 Jeff Bonwick 提出）。它的核心思想是：**根据对象大小分类，为每类对象预分配"板料"（slab）**。

```
场景：内核中有各种大小的数据结构（task_struct, inode, pipe...）

Slab 分配器的工作方式：

  1. 为每种对象类型创建一个 cache（缓存）
  2. 每个 cache 管理多个 slab
  3. 每个 slab 包含多个相同大小的对象
  4. 分配时：从 cache 的空闲链表取一个对象
  5. 释放时：归还到 cache 的空闲链表

  ┌──────────────────────────────────┐
  │   Cache for "task_struct"       │
  ├──────────────────────────────────┤
  │  slab1: [obj][obj][obj][obj]...  │
  │  slab2: [obj][obj][obj][obj]...  │
  │  slab3: [obj][obj][...空闲...]   │ ← 部分分配的 slab
  └──────────────────────────────────┘
```

**Slab 分配器的优势：**
- **零碎片**：每个 slab 里全是相同大小的对象，没有内部碎片
- **极快分配**：空闲链表操作，时间复杂度 O(1)
- **缓存友好**：刚释放的对象可能还在 CPU 缓存里，下次分配命中缓存，性能爆表

### Buddy vs Slab 对比

| 特性 | Buddy 算法 | Slab 分配器 |
|---|---|---|
| 分配单位 | 2 的幂，大小固定 | 对象大小，自定义 |
| 合并条件 | 伙伴必须都是空闲的 | 归还给同一个 cache |
| 内存利用率 | 有内部碎片 | 几乎无内部碎片 |
| 应用场景 | 操作系统物理内存管理 | Linux 内核对象管理 |
| 分配速度 | 快 | 极快（对象缓存） |

---

## 14.13 `alloca`：栈上的"临时工"

最后介绍一个"非标准但广泛支持"的函数——`alloca`。

### 函数签名

```c
#include <alloca.h>  // 或者 <stdlib.h>

void *alloca(size_t size);
```

### 它是干嘛的？

`alloca` 在**栈上**分配内存，而不是堆上！分配方式和 `malloc` 类似，但不需要 `free`。

```c
#include <stdio.h>
#include <alloca.h>

int main() {
    int n = 100;
    // 在栈上分配 100 个 int
    int *arr = (int *)alloca(n * sizeof(int));

    for (int i = 0; i < n; i++) {
        arr[i] = i * i;
    }

    printf("arr[99] = %d\n", arr[99]);  // 99 * 99 = 9801
    // 输出：arr[99] = 9801

    // 函数返回时，arr 自动消失，不需要 free！
    return 0;
}
```

### 为什么叫"临时工"？

因为 `alloca` 分配的内存**随栈帧一起消亡**——函数返回时，栈被自动弹出，内存自动回收。相当于你请了一个临时工，它跟你一起上下班（栈帧），你下班它也下班，不用你操心遣散费（`free`）。

### ⚠️ `alloca` 的坑

1. **非标准**：不是 ANSI C 标准库函数，有些编译器可能不支持
2. **不能跨函数使用**：分配的内存在当前函数栈帧上，函数返回就没了
3. **可能导致栈溢出**：如果分配过大的内存，栈空间有限，会直接崩溃
4. **`free` 会帮倒忙**：`alloca` 分配的东西千万不能 `free`！

> **选择建议：** 在需要小块临时内存、且确定大小不会太大时，`alloca` 是一个选择。但在可移植性要求高的代码中，慎用。嵌入式开发有些平台不支持。

---

## 本章小结

本章我们深入探索了 C 语言的动态内存管理，这是 C 语言中最强大也最危险的技能之一。

1. **内存布局**：程序的虚拟地址空间从上到下分为内核空间、栈、堆、全局数据区、只读数据区和代码区。栈向下增长，堆向上增长。

2. **为什么需要动态内存**：运行时确定大小、数据跨函数共享、动态扩展数据结构——这些是栈上静态分配做不到的事。

3. **`malloc`**：向堆申请内存，返回首地址或 `NULL`。分配后内容是"脏"的，需要手动初始化。

4. **`calloc`**：分配并初始化为 0，适合"不确定是否全部写入"的场景。

5. **`realloc`**：调整已有内存块的大小。**可能返回新地址**，失败返回 `NULL`（原块仍有效），使用时必须先保存结果再更新指针。

6. **`free`**：归还内存给操作系统。**只能 free `malloc`/`calloc`/`realloc` 的返回值**，只能 free 一次，free 后立即置 `NULL`。

7. **返回值检查**：`malloc`/`calloc`/`realloc` 失败返回 `NULL`，必须检查。

8. **常见内存错误**：野指针（未初始化指针）、重复 `free`、内存泄漏（长期运行的隐形杀手）、越界访问（缓冲区溢出）、悬挂指针（free 后继续使用）。

9. **内存检测工具**：`valgrind`（Linux/macOS）、Visual Leak Detector（Windows）、AddressSanitizer（`gcc -fsanitize=address`，跨平台）。

10. **`aligned_alloc`**（C11）：分配指定对齐要求的内存，常用于 SIMD 编程。

11. **内存池**：预分配一大块内存，按固定大小切成小块分配，减少系统调用开销，适合高频分配/释放场景。

12. **Buddy 算法**：按 2 的幂分裂/合并内存块，合并快速，但有内部碎片。

13. **Slab 分配器**：按对象类型分类管理 slab，零碎片、O(1) 分配，是 Linux 内核的核心内存管理技术。

14. **`alloca`**：在栈上分配临时内存，随函数返回自动回收。非标准但广泛支持，慎用。

> **终极忠告：** 动态内存管理的核心原则只有一句话——**"谁分配，谁释放；配对使用，永不越界。"** 记住这 12 个字，90% 的内存错误都会远离你！

---

*写完这一章，你的 C 语言内功又精进了一层。内存管理是 C 语言的灵魂，也是区分"会写 C"和"精通 C"的分水岭。多练习，多踩坑，多用工具检测——终有一天，你也能成为内存管理的大师！*
