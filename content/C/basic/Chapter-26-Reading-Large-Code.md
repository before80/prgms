+++
title = "第 26 章：Linux 内核与开源项目阅读方法"
weight = 260
date = "2026-03-29T22:34:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 第 26 章：Linux 内核与开源项目阅读方法

> 恭喜你！能走到这一章，说明你已经不是一个只会写 `Hello World` 的小白了。你甚至已经能够用 C 语言写一些小项目，解决实际问题。但现在你可能面临一个终极挑战——阅读大型 C 代码。想象一下，当你打开一个几十万行代码的项目，满屏都是陌生的函数和结构体，那种感觉就像走进了一座没有地图的迷宫。没关系！本章就是你的"大型代码阅读指南"，专门为你解锁 Linux 内核、Git、Redis、SQLite、NGINX 这些顶级开源项目的阅读姿势。

本章专为阅读 / 维护 Linux 内核、Git、Redis、SQLite、NGINX 等大型开源 C 项目而设。我们会从 Linux 内核的编码风格和核心技巧讲起，再介绍一系列强大的代码阅读工具，最后以几个经典开源项目为例，手把手教你如何庖丁解牛般地拆解大型代码库。准备好了吗？让我们开始这场代码探索之旅！

---

## 26.1 Linux 内核代码的特点

Linux 内核是人类写出的最复杂的 C 代码之一——数千万行代码，几万名贡献者，历经三十多年依然活跃开发。阅读内核代码就像是阅读一座运转了三十年的城市的设计图纸：处处是历史的痕迹，到处有精妙的优化，但也夹杂着为了兼容性而留下的"奇奇怪怪"的代码。理解内核代码的特点，是你成为内核 hack（黑客/高手）的第一步。

### 26.1.1 编码风格：Linux kernel coding style

Linux 内核有一套严格的编码规范，叫 **kernel coding style**（内核编码风格）。这套规范不是随便制定的，而是无数前辈踩坑后总结出来的最佳实践。内核官方文档甚至专门有一章 `CodingStyle` 来讲这件事。

**核心规则如下：**

**1. 缩进用 Tab，不用空格。**

这和很多现代编辑器的默认设置相反。在内核看来，一个 Tab 就是 8 个字符的宽度，这是老祖宗留下来的规矩，不接受反驳。

```c
/*
 * 内核代码示例：Tab 缩进
 * 注意看，每个缩进都是一个 Tab 字符
 */
void set_mode(int new_mode)
{
    if (new_mode == MODE_NORMAL) {
        do_normal_thing();  // Tab 缩进
    } else if (new_mode == MODE_FAST) {
        do_fast_thing();    // Tab 缩进
    }
}
```

**2. if/for/while 的括号规则：左括号不换行，右括号另起一行。**

这个风格被叫做 "K&R 风格"（Kernighan & Ritchie 风格），是 C 语言发明者推荐的格式：

```c
/* 内核风格：括号这样放 */
if (condition) {
    do_something();
    do_another_thing();
} else {
    do_else();
}

/* for 循环也一样 */
for (i = 0; i < MAX; i++) {
    process(i);
}
```

**3. 命名规范：**

- 变量名和函数名全小写，用下划线分隔（snake_case 风格）
- 拒绝驼峰命名法（`myVariable` 这种在内核里是不存在的）
- 宏（macro）全大写
- 结构体、枚举、typedef 名字全小写

```c
/* 内核命名风格示例 */
unsigned long total_memory;       /* 全小写，下划线分隔 */
struct task_struct;               /* 结构体全小写 */
enum cpu_state { CPU_IDLE, CPU_RUNNING }; /* 枚举值全大写 */
#define MAX_BUFFER_SIZE 4096       /* 宏全大写 */
static inline void do_schedule(void); /* 静态函数全小写 */
```

> 为什么内核要搞这么"复古"的风格？因为内核代码 age（年龄）很大，很多规则是在 90 年代制定的。而且全世界的开发者都在贡献代码，统一风格可以避免"这个空格是 Tab 还是 4 个空格"这种无聊的争论。

**4. 每行代码长度限制在 80 个字符以内。**

这条规则是为了保证在古老的终端上也能正常显示。虽然现在屏幕大了，但这条规矩依然被执行着。

**5. 函数不要太长，最好不超过一页（约 40 行）。**

一个函数做一件事，做完就结束。如果一个函数超过了一屏，那么它大概率需要被拆分成多个小函数。

```c
/* 内核风格的短函数示例 */
static int alloc_buffer(struct buffer *buf, size_t size)
{
    if (!buf || size == 0)
        return -EINVAL;

    buf->data = kmalloc(size, GFP_KERNEL);
    if (!buf->data)
        return -ENOMEM;

    buf->size = size;
    atomic_set(&buf->refcnt, 1);
    return 0;
}
```

### 26.1.2 GNU Extension 广泛使用

Linux 内核大量使用 GNU C 扩展（GCC 特有的语法）。这些扩展让 C 语言变得像魔法一样强大——但也意味着这些代码只能在 GCC 下编译，其他编译器（比如 MSVC）会报一大堆错误。

**常见 GNU Extension：**

**1. 内联汇编（Inline Assembly）：直接在 C 代码里写汇编**

```c
/* 内联汇编示例：获取当前 CPU 的 ID */
static inline unsigned int get_cpu_id(void)
{
    unsigned int id;
    /*
     * "=a"(id) 表示把 eax 寄存器的值输出到 id 变量
     * "0" 表示输入和输出使用同一个操作数
     * "cpuid" 是汇编指令
     */
    asm volatile("cpuid" : "=a"(id) : "0"(0));
    return id;
}
```

**2. `__attribute__`：给变量或函数添加属性**

这是 GNU C 特有的语法，用来告诉编译器一些额外信息：

```c
/* __attribute__((packed))：紧凑布局，不对齐 */
struct __attribute__((packed)) small_packet {
    char flags;    /* 1 字节 */
    int data;      /* 4 字节（不填充，直接挨着 flags） */
};
/* 整个结构体只有 5 字节，而不是 8 字节 */

/* __attribute__((aligned(n)))：指定对齐 */
struct __attribute__((aligned(64))) cache_line {
    char data[64]; /* 强制 64 字节对齐，方便 CPU 缓存 */
};

/* __attribute__((noreturn))：告诉编译器这个函数不返回 */
void __attribute__((noreturn)) panic(const char *msg)
{
    printk("Kernel panic: %s\n", msg);
    while (1) ; /* 死机 */
}

/* __attribute__((unused))：可能未使用，不报警告 */
static int __attribute__((unused)) debug_only_function(void)
{
    return 42;
}

/* __attribute__((deprecated))：标记为已废弃 */
void __attribute__((deprecated)) old_function(void)
{
    /* 旧函数，但仍能编译，只是会报警告 */
}
```

**3. `__builtin` 系列：编译器内置函数**

这些函数不是库函数，而是编译器自己知道的"魔法"：

```c
/* __builtin_expect：告诉编译器哪个分支更可能执行 */
#define likely(x)    __builtin_expect(!!(x), 1)   /* x 很可能是真的 */
#define unlikely(x)  __builtin_expect(!!(x), 0)   /* x 很可能是假的 */

/* 用法：编译器会优化，把更可能的分支放在前面 */
if (likely(ptr != NULL)) {
    /* 这里是正常情况，CPU 更容易预取这条指令 */
    process(ptr);
}

if (unlikely(error < 0)) {
    /* 这是异常情况，但代码还是要写 */
    printk("Error: %d\n", error);
}

/* __builtin_popcount：计算一个整数有多少个 1 */
int ones = __builtin_popcount(0xFF);  /* 返回 8，因为 0xFF = 11111111 */

/* __builtin_clz：计算前导零的数量（Count Leading Zeros） */
int leading_zeros = __builtin_clz(16); /* 返回 27（32位系统） */
```

### 26.1.3 链表结构：list_head

在用户态程序里，我们通常这样定义一个链表：

```c
/* 用户态程序员的链表：把指针直接塞进结构体 */
struct person {
    char name[32];
    int age;
    struct person *next;  /* 指向下一个 */
    struct person *prev;  /* 指向前一个 */
};
```

但在 Linux 内核里，链表是这样定义的：

```c
/* 内核的链表：链表节点本身不关心数据 */
struct list_head {
    struct list_head *next, *prev;
};

/* 用的时候，把 list_head 当成"零件"嵌进去 */
struct person {
    char name[32];
    int age;
    struct list_head list;  /* 嵌进去！这就是"侵入式链表"的思想 */
};
```

这叫**侵入式链表**（intrusive linked list）——链表结构不存储数据，它只是一个"连接件"，你需要什么数据，就把"连接件"装到你的结构体里。

**为什么这样做？** 想象一下，你有一堆积木（各种结构体），你想用链表串起来。如果每个积木里都内置了一个"标准接口"（list_head），那任何积木都可以被串起来。这就是内核"高内聚低耦合"的设计哲学。

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* 模拟 Linux 内核的 list_head */
struct list_head {
    struct list_head *next, *prev;
};

/* 初始化宏 */
#define LIST_HEAD_INIT(name) { &(name), &(name) }
#define LIST_HEAD(name) struct list_head name = LIST_HEAD_INIT(name)

/* 插入操作：在 prev 和 next 之间插入 */
static inline void __list_add(struct list_head *new,
                               struct list_head *prev,
                               struct list_head *next)
{
    next->prev = new;
    new->next = next;
    new->prev = prev;
    prev->next = new;
}

/* 在链表头插入 */
static inline void list_add(struct list_head *new, struct list_head *head)
{
    __list_add(new, head, head->next);
}

/* 在链表尾插入 */
static inline void list_add_tail(struct list_head *new, struct list_head *head)
{
    __list_add(new, head->prev, head);
}

/* 判断链表是否为空 */
static inline int list_empty(const struct list_head *head)
{
    return head->next == head;
}

/* 遍历链表 */
#define list_for_each(pos, head) \
    for (pos = (head)->next; pos != (head); pos = pos->next)

/* 获取包含某个成员的结构的指针！这就是 container_of 的思想 */
#define container_of(ptr, type, member) \
    ((type *)((char *)(ptr) - offsetof(type, member)))

#define offsetof(type, member) ((size_t)&((type *)0)->member)

/* 一个具体的数据结构：人物 */
struct person {
    char name[32];
    int age;
    struct list_head list;  /* 嵌进去的链表节点 */
};

/* 演示：创建三个人，用链表串起来 */
int main(void)
{
    LIST_HEAD(people_list);  /* 初始化一个空链表头 */

    struct person p1, p2, p3;
    strcpy(p1.name, "张三");
    p1.age = 25;
    strcpy(p2.name, "李四");
    p2.age = 30;
    strcpy(p3.name, "王五");
    p3.age = 35;

    /* 把三个人加入链表（尾插法） */
    list_add_tail(&p1.list, &people_list);
    list_add_tail(&p2.list, &people_list);
    list_add_tail(&p3.list, &people_list);

    /* 遍历链表，打印信息 */
    struct list_head *pos;
    struct person *p;
    printf("=== 链表里的人：===\n");
    list_for_each(pos, &people_list) {
        /* 关键：container_of！通过 list 指针找到 person 指针 */
        p = container_of(pos, struct person, list);
        printf("%s, 年龄 %d\n", p->name, p->age);
    }
    // 输出：
    // === 链表里的人：===
    // 张三, 年龄 25
    // 李四, 年龄 30
    // 王五, 年龄 35

    return 0;
}
```

### 26.1.4 container_of 宏：通过成员指针找到容器结构体

上一节的 `container_of` 宏是内核最经典的宏之一。它的作用是：**已知一个结构体的某个成员的指针，反推出这个结构体的指针。**

```c
#define container_of(ptr, type, member) \
    ((type *)((char *)(ptr) - offsetof(type, member)))
```

这句话有点绕，我们用生活化的例子来解释：

> 想象一下，你有一排集装箱，每个集装箱里装的是人（`struct person`）。你只能看到集装箱里的一只手（`list` 成员的地址），但你想找到这个人所在的整个集装箱。你会怎么做？你测量一下手在集装箱里的位置（比如从集装箱门口往里走 50 米），然后用手现在的位置减去 50 米，就得到了集装箱的位置。这就是 `container_of` 干的事！

```c
#define offsetof(type, member) ((size_t)&((type *)0)->member)
```

`offsetof` 计算的是 `member` 在 `type` 结构体里的**偏移量**——也就是从结构体开头到该成员之间的距离（字节数）。

```c
#include <stdio.h>
#include <stddef.h>  /* offsetof 在这里定义 */

#define container_of(ptr, type, member) \
    ((type *)((char *)(ptr) - offsetof(type, member)))

struct person {
    char name[32];
    int age;
    double height;
    struct {
        int x;
        int y;
    } position;  /* 假设这个是 ptr 指向的成员 */
};

int main(void)
{
    struct person p;
    p.age = 30;
    p.position.x = 100;
    p.position.y = 200;

    /* 假设我们只有 position 的地址 */
    struct { int x; int y; } *pos_ptr = &p.position;

    /* 用 container_of 反推 person 的指针 */
    struct person *person_ptr = container_of(pos_ptr, struct person, position);

    printf("person 的 age 是: %d\n", person_ptr->age);
    printf("person 的 name 地址: %p\n", person_ptr->name);
    printf("position 的地址: %p\n", pos_ptr);
    // 输出：
    // person 的 age 是: 30
    // （地址会根据实际运行有所不同）

    /* 验证偏移量 */
    printf("position 在 person 中的偏移量: %zu 字节\n",
           offsetof(struct person, position));
    // position 是最后一个成员，所以偏移量 = sizeof(person) - sizeof(position)

    return 0;
}
```

在 Linux 内核中，`container_of` 随处可见。`list_entry` 就是一个别名：

```c
#define list_entry(ptr, type, member) \
    container_of(ptr, type, member)
```

### 26.1.5 likely / unlikely：__builtin_expect 封装

CPU 执行指令的时候，会"猜"（branch prediction，分支预测）if 条件会走哪个分支。如果猜对了，执行速度会非常快（因为 CPU 可以提前把后续指令流水线加载好）。如果猜错了，就需要清空流水线，性能会下降。

`likely()` 和 `unlikely()` 宏就是**告诉 CPU "我猜这个条件大概率会走哪边"**的工具：

```c
#define likely(x)    __builtin_expect(!!(x), 1)   /* 我猜 x 大概率为真 */
#define unlikely(x)  __builtin_expect(!!(x), 0)   /* 我猜 x 大概率为假 */
```

```c
#include <stdio.h>

/* 模拟 likely/unlikely 的实现 */
#define likely(x)    __builtin_expect(!!(x), 1)
#define unlikely(x)  __builtin_expect(!!(x), 0)

int main(void)
{
    int error = -1;

    /*
     * if (likely(ptr != NULL))
     * 相当于告诉 CPU："ptr 大概率不为空，所以把 if 分支当作热路径优化"
     */
    if (likely(error == 0)) {
        printf("操作成功！\n");
    } else {
        printf("操作失败！\n");
    }
    // 输出：
    // 操作失败！

    /*
     * 实际应用场景：
     * 内核代码里，错误永远是少数情况
     * 所以内核用 unlikely() 包裹所有错误检查
     */
    int ret = -1;
    if (unlikely(ret < 0)) {
        /* 这种情况很少发生，CPU 会把这个分支当作"冷路径" */
        printf("错误码: %d\n", ret);
    }

    return 0;
}
```

> 小知识：在用户态程序里，`likely`/`unlikely` 基本上没什么用，因为编译器优化没那么激进。但在 Linux 内核里，这是非常重要的性能优化手段，因为内核代码运行在最高优先级，需要榨干每一滴性能。

### 26.1.6 RCU（Read-Copy-Update）：无锁同步机制

**RCU（Read-Copy-Update）** 是 Linux 内核的一种高级同步机制，专门用于读多写少的场景。它的核心思想是：**读操作不加锁，只有写操作需要加锁。**

这在现实生活中的例子是什么？想象一下，你在一个图书馆里：
- **读操作**：你在书架间浏览书名，这个过程不需要锁，因为没人会阻止你看书。
- **写操作**：图书管理员要更换一批书。她不能在你看书的时候直接把书架上的书换走（你会一脸懵逼），但她可以先把新书放在一边，等所有人都看完旧书，再"悄悄地"把新书替换上去。

RCU 的工作原理类似：
1. 写线程复制一份数据
2. 在副本上修改
3. 等待所有正在读取的读者完成（用 `synchronize_rcu()`）
4. 原子性地替换旧数据

```c
/*
 * RCU 简化模拟（实际内核实现要复杂得多）
 * 这只是一个概念性演示
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <pthread.h>

/* 共享数据 */
char *shared_data = NULL;

/* 模拟 RCU 的读操作（无锁） */
void read_data(void)
{
    /* 读者只需要读取，不需要加锁 */
    /* 但要注意：读到的可能是旧数据 */
    printf("读者: 看到的数据是 [%s]\n", shared_data ? shared_data : "NULL");
}

/* 模拟 RCU 的写操作 */
void write_data(const char *new_data)
{
    /* 写操作需要加锁保护 */
    char *old_data = shared_data;

    /* 1. 复制一份副本 */
    char *copy = malloc(256);
    strcpy(copy, new_data);

    /* 2. 在副本上修改（此时读者还在读 old_data） */

    /* 3. 内存屏障，确保复制完成 */

    /* 4. 原子替换（读者下次读会读到新数据） */
    shared_data = copy;

    /* 5. 等待所有正在读的读者结束（简化版，实际用 rcu_barrier()） */
    /* 在这个简化版本中，我们直接释放旧数据 */
    /* 真实内核中，需要调用 synchronize_rcu() 等待 */
    if (old_data) {
        printf("写者: 释放旧数据 [%s]\n", old_data);
        free(old_data);
    }
}

int main(void)
{
    printf("=== RCU 演示 ===\n");

    /* 初始数据 */
    write_data("Hello, RCU!");

    /* 多个读者 */
    read_data();
    read_data();
    read_data();

    /* 写者更新 */
    write_data("Updated Data!");

    /* 更新后读者看到新数据 */
    read_data();

    /* 清理 */
    free(shared_data);

    return 0;
}
```

> 内核中的 RCU 实现要复杂得多，涉及内存屏障、宽限期（grace period）、以及各种优化。但核心思想就是这样：读者无锁，写者通过复制和等待来实现安全更新。

### 26.1.7 内存管理：slab allocator / vmalloc / kmalloc

Linux 内核有一套复杂的内存管理体系，针对不同的使用场景有不同的分配器：

**1. `kmalloc`：分配小块内存（物理连续）**

类似于用户态的 `malloc`，但分配的是物理连续的内存，而且速度极快：

```c
/* kmalloc 示例：分配一个固定大小的内核内存块 */
/* gfp_t 是"get free pages"的 flags，描述内存分配策略 */
void *ptr = kmalloc(128, GFP_KERNEL);  /* 分配 128 字节 */
if (!ptr) {
    /* 分配失败 */
    return -ENOMEM;
}

/* 使用完毕后释放 */
kfree(ptr);

/* 常见的 GFP flags：*/
#define GFP_KERNEL    0x00000000  /* 正常分配，可能休眠（睡眠分配） */
#define GFP_ATOMIC    0x00000020  /* 原子分配，不允许休眠（用于中断处理） */
#define GFP_USER      0x00000040  /* 用户进程内存分配 */
```

**2. `vmalloc`：分配虚拟连续但物理不一定连续的内存**

如果你需要大块内存（比如几 MB），但不需要物理地址连续，可以用 `vmalloc`：

```c
/* vmalloc 示例：分配大块内存 */
void *large_ptr = vmalloc(1024 * 1024);  /* 分配 1MB */
if (!large_ptr) {
    return -ENOMEM;
}

/* 释放 */
vfree(large_ptr);

/*
 * kmalloc vs vmalloc 的区别：
 *
 * kmalloc: 物理连续，高速，小块（最大几MB，看具体实现）
 *          想象：买一栋连续的门面房
 *
 * vmalloc: 虚拟连续，物理可能不连续，相对慢，大块
 *          想象：买一栋楼的不同楼层，房间不连续但你能自由上下楼
 */
```

**3. slab allocator：对象池**

内核经常需要反复分配和释放同样大小的结构体（比如 `task_struct`）。如果每次都调用 `kmalloc`，会有额外的开销（找到合适的空闲块、初始化等）。slab allocator 就是来解决这个问题的——它维护了一个"对象池"，相同大小的对象可以高效地复用：

```c
/*
 * slab allocator 的思想：
 * 1. 创建多个 "slab"（缓存块），每个 slab 包含多个对象
 * 2. 分配时，从 slab 中取一个空闲对象（O(1) 速度）
 * 3. 释放时，把对象放回 slab（非常快）
 *
 * 在内核中，你可以用 kmem_cache_create 创建自己的缓存：
 */
struct kmem_cache *my_cache;

/* 创建缓存：每个对象大小 64 字节 */
my_cache = kmem_cache_create("my_struct_cache",
                              64,     /* 对象大小 */
                              0,      /* 对齐（0 表示默认） */
                              SLAB_HWCACHE_ALIGN,  /* 对齐到 CPU 缓存线 */
                              NULL);  /* 构造函数 */

/* 从缓存中分配对象 */
void *obj = kmem_cache_alloc(my_cache, GFP_KERNEL);

/* 释放对象回缓存 */
kmem_cache_free(my_cache, obj);

/* 销毁缓存 */
kmem_cache_destroy(my_cache);
```

### 26.1.8 BUILD_BUG_ON_ZERO：编译期断言

有时候我们希望在编译时发现错误，而不是运行时。比如我们想确保某个结构体的大小正好是我们预期的：

```c
#define BUILD_BUG_ON_ZERO(e) (sizeof(struct { int:-!!(e); }))
```

这个宏的原理非常巧妙：
- 如果 `e` 为真（即 `e != 0`），则 `!!(e)` 为 1，`-1` 变成负数
- 位域（bit-field）宽度为负数是非法的，编译器会报错！
- 如果 `e` 为假，则位域宽度为 0，这是合法的

```c
#include <stdio.h>

/* 模拟 BUILD_BUG_ON_ZERO */
#define BUILD_BUG_ON_ZERO(e) (sizeof(struct { int :-!!(e); }))

/* 编译期检查：确保 int 的大小是 4 字节 */
int check_int_size[ BUILD_BUG_ON_ZERO(sizeof(int) != 4) + 1 ];

/*
 * 如果 sizeof(int) != 4，编译器会报错：
 * "error: negative width in bit-field"
 *
 * 如果 sizeof(int) == 4，数组大小是 1（正常）
 */

/* 另一个常见用法：检查结构体大小 */
#define COMPILE_TIME_ASSERT(expr) \
    extern int dummy[(expr) ? 1 : -1]

COMPILE_TIME_ASSERT(sizeof(long) >= 8);  /* 确保是 64 位 */

int main(void)
{
    printf("编译期断言通过！\n");
    printf("sizeof(int) = %zu\n", sizeof(int));
    return 0;
}
```

> 这个技巧的好处是：如果条件不满足，程序根本编译不过，而不是等到运行时才发现问题。这叫"Fail Fast"（快速失败）原则。

---

## 26.2 Linux 内核代码阅读工具链

阅读大型代码，没有趁手的工具，就像在黑暗中摸索——你会走很多弯路，效率极低。这一节介绍几款内核开发者常用的"瑞士军刀"，让代码阅读效率翻倍。

### 26.2.1 ctags / cscope：代码跳转

**ctags** 和 **cscope** 是两个经典的代码标签工具。它们能帮你快速找到函数定义、变量引用、结构体声明等，让你在海量代码中自由穿梭。

**ctags：生成标签文件，快速跳转到定义**

```bash
# 在项目根目录运行，生成 tags 文件
ctags -R .          # -R 递归扫描所有子目录

# 在 Vim/Emacs 中使用
# Vim:
vim -t func_name     # 跳转到 func_name 的定义
# 在 Vim 里：
# Ctrl + ]  跳转到光标下符号的定义
# Ctrl + t  返回上一个位置
# :tselect  列出所有匹配的定义
# :tag /pattern  搜索并跳转

# Emacs:
M-.  跳转到定义
M-*  返回上一个位置
```

```bash
# 常用 ctags 选项
ctags -R --languages=c --langmap=c:.h.k.xs  # 只扫描 C 相关文件
ctags -R --tag-relative=yes                  # 标签路径相对于标签文件
ctags -R -n                                   # 在标签文件中显示行号（便于编辑）
```

**cscope：更强大的代码浏览器，支持交叉引用查询**

```bash
# 初始化 cscope 数据库
cscope -Rbq           # -R 递归，-b 只构建数据库不进入交互，-q 加速索引

# 会生成 cscope.in.out 和 cscope.out 两个文件

# 查询示例
cscope -d             # 进入交互模式

# 常用查询选项：
# 0: 找到这个 C 符号的所有定义
# 1: 找到这个函数被调用的所有地方
# 2: 这个符号的定义
# 3: 找到这个字符串/文本出现的所有地方
# 4: 找到这个文件
# 5: 找到这个符号被定义的所有源文件
# 6: 找到一个虚拟寄存器的赋值（egoto）
# 7: 找到匹配一个正则表达式的所有 EGP 字符串
# 8: 找到一个数组的所有原始声明
# 9: 找到一个预处理宏的所有引用
# a: 找到一个调用指定函数的函数
# b: 打印数据库
# c: 找到指定函数的调用
```

```bash
# 在 Vim 中使用 cscope
vim -t some_function   # 跳转到定义

# Vim 里设置 cscope 路径
:cs add cscope.out     # 添加数据库
:cs find g func_name   # 查找 func_name 的定义
:cs find c symbol      # 查找 symbol 被调用的地方

# 快捷映射（可以加到 .vimrc）
nnoremap <C-]> :cs find g <C-R>=expand("<cword>")<CR><CR>
nnoremap <C-\> :cs find s <C-R>=expand("<cword>")<CR><CR>
```

```bash
# ctags + cscope 组合使用
# 生成 tags 和 cscope 数据库
ctags -R . && cscope -Rbq

# 或者使用 gtags（GNU GLOBAL），更现代
gtags                  # 生成 GPATH GRTAGS GSYMS GTAGS
global -r symbol       # 查找符号定义
global -s symbol       # 查找符号引用
global -g pattern      # 用正则搜索
```

### 26.2.2 LXR / OpenGrok：Web 界面交叉引用

有时候你想在浏览器里浏览代码，鼠标点击就能跳转。LXR 和 OpenGrok 就是这样的工具。

**LXR（Linux Cross Reference）**：专为 Linux 内核设计的代码浏览器

```
功能特点：
- Web 界面浏览代码
- 鼠标点击跳转定义/引用
- 多版本内核支持
- 全文搜索
```

```bash
# LXR 部署示例（需要 web 服务器如 Apache）
# 1. 下载 lxr
git clone https://github.com/ThomasPar勒/lxr.git

# 2. 配置
cd lxr
./configure --with-mod_perl --with-apache=/etc/apache2

# 3. 生成索引
perl bin/generatexref --linuxversion=5.15.0

# 4. 访问 http://your-server/lxr/
```

**OpenGrok**：通用的代码浏览器，支持各种语言

```bash
# OpenGrok 部署（需要 Java 和 web 服务器）
# 1. 下载 opengrok
wget https://github.com/oracle/opengrok/releases/download/1.7.25/opengrok-1.7.25.tar.gz
tar -xzf opengrok-1.7.25.tar.gz

# 2. 创建索引
OPENGROK_PATH=/path/to/your/project
OPENGROK_DATA=/var/opengrok/data
java -jar opengrok.jar -P -s $OPENGROK_PATH -d $OPENGROK_DATA

# 3. 部署 web 应用
cp source.war /var/lib/tomcat9/webapps/

# 4. 访问 http://your-server:8080/source/
```

> 如果你只是想快速搜索某个内核符号，可以直接访问 https://elixir.bootlin.com/linux/latest/source ，这是 Linus Torvalds 等人维护的在线代码浏览工具，支持内核全版本搜索！

### 26.2.3 pahole：显示结构体实际内存布局

当你用 `struct` 定义一个结构体时，编译器可能会在成员之间插入一些"填充"（padding）字节，让每个成员都对齐到特定边界。这会影响结构体的实际大小和内存布局。`pahole` 工具可以让你"看到"这些填充字节。

```bash
# pahole 读取 DWARF 调试信息，显示结构体布局
pahole vmlinux              # 查看内核镜像中所有结构体
pahole -C task_struct vmlinux   # 只看 task_struct

# 示例输出
struct task_struct {
    /* 0 */    volatile long          state;
    /* 8 */    void                 *stack;
    /* 16 */   unsigned int          flags;
    /* 24 */   struct mm_struct    *mm;
    /* 32 */   struct task_struct  *next_task;
    ...
    /* 大小: 8192 字节，缓存对齐 */
}
```

```bash
# 常用选项
pahole -C struct_name vmlinux    # 只显示特定结构体
pahole -s struct_name vmlinux   # 显示结构体简报（大小、对齐）
pahole -r struct_name vmlinux   # 显示递归展开的成员
pahole --show_padding vmlinux   # 显示填充字节（用黄色/特殊颜色标注）
```

```c
/*
 * 用一个简单的例子说明 padding（填充）
 */
#include <stdio.h>
#include <stddef.h>  /* offsetof */

/* 有填充的结构体 */
struct with_padding {
    char   a;     /* 1 字节 */
    int    b;     /* 4 字节，但编译器会在 a 后面填 3 个字节 */
    char   c;     /* 1 字节，但 b 是 4 字节对齐，所以后面可能再填 3 字节 */
};

/* 没有填充的结构体（手动紧凑） */
struct packed {
    char   a;
    char   b;
    int    c;
    char   d;
};

int main(void)
{
    printf("=== 结构体内存布局对比 ===\n\n");

    printf("with_padding:\n");
    printf("  char   a: 偏移 %zu, 大小 1\n", offsetof(struct with_padding, a));
    printf("  int    b: 偏移 %zu, 大小 4（前面有 3 字节填充）\n",
           offsetof(struct with_padding, b));
    printf("  char   c: 偏移 %zu, 大小 1（前面有 3 字节填充）\n",
           offsetof(struct with_padding, c));
    printf("  总大小: %zu 字节（实际用了 %zu 字节数据 + %zu 字节填充）\n\n",
           sizeof(struct with_padding),
           1 + 4 + 1,
           sizeof(struct with_padding) - 6);

    printf("packed（紧凑）:\n");
    printf("  char   a: 偏移 %zu\n", offsetof(struct packed, a));
    printf("  char   b: 偏移 %zu\n", offsetof(struct packed, b));
    printf("  int    c: 偏移 %zu\n", offsetof(struct packed, c));
    printf("  char   d: 偏移 %zu\n", offsetof(struct packed, d));
    printf("  总大小: %zu 字节（无填充！）\n", sizeof(struct packed));

    return 0;
}

// 输出：
// === 结构体内存布局对比 ===
//
// with_padding:
//   char   a: 偏移 0, 大小 1
//   int    b: 偏移 4, 大小 4（前面有 3 字节填充）
//   char   c: 偏移 8, 大小 1（前面有 3 字节填充）
//   总大小: 12 字节（实际用了 6 字节数据 + 6 字节填充）
//
// packed（紧凑）:
//   char   a: 偏移 0
//   char   b: 偏移 1
//   int    c: 偏移 2
//   char   d: 偏移 6
//   总大小: 7 字节（无填充！）
```

---

## 26.3 Git 源码阅读（经典 C 项目）

Git 是 Linus Torvalvalds 用 C 语言开发的版本控制系统，被全世界开发者广泛使用。Git 的代码量适中（约 30 万行 C 代码），注释完整，质量极高，是阅读大型 C 项目的绝佳入门选择。

### 26.3.1 对象模型：blob / tree / commit / tag

Git 的核心是一个"内容寻址文件系统"（Content-Addressable File System）。所有的数据都被当作"对象"存储，每个对象都有唯一的 SHA-1 哈希值作为"名字"。

```
mermaid
graph TD
    A["blob 对象<br/>（文件内容）"] --> B["tree 对象<br/>（目录快照）"]
    B --> C["commit 对象<br/>（版本快照）"]
    C --> D["tag 对象<br/>（标签）"]
```

**四种对象类型：**

1. **blob（Binary Large Object）**：存储文件内容。Git 会把文件内容哈希，得到一个 blob 对象的 SHA-1 值。

2. **tree（目录树）**：存储目录结构。它记录了文件名和对应的 blob/tree SHA-1，就像 Unix 的 inode 和目录项。

3. **commit（提交）**：记录一个目录快照 + 作者 + 时间 + 提交信息 + 父 commit。

4. **tag（标签）**：给某个 commit 起一个别名，比如 `v1.0.0`。

```c
/*
 * Git 对象结构体的简化版实现
 * 完整源码在 git 项目的 object.c 中
 */

/* 对象类型枚举 */
enum object_type {
    OBJ_NONE = 0,
    OBJ_BLOB = 1,
    OBJ_TREE = 2,
    OBJ_COMMIT = 3,
    OBJ_TAG = 4,
    OBJ_OFS_DELTA = 6,  /* 压缩类型 */
    OBJ_REF_DELTA = 7,
};

/* 对象头结构 */
struct object {
    unsigned char sha1[20];    /* SHA-1 哈希值（20 字节） */
    enum object_type type;     /* 对象类型 */
    unsigned int size;         /* 对象大小 */
    int ref_count;             /* 引用计数（垃圾回收用） */
};

/* blob 对象：最简单的对象，只有数据 */
struct blob {
    struct object object;
    /* 文件内容存储在独立的 blob 结构中 */
};

/* commit 对象结构 */
struct commit {
    struct object object;
    unsigned char tree_sha1[20];      /* 目录树的 SHA-1 */
    unsigned char parent_sha1[1][20]; /* 父提交的 SHA-1（可变长数组） */
    int parent_count;
    char *author;                      /* 作者字符串 */
    char *author_date;                 /* 作者时间 */
    char *committer;                   /* 提交者字符串 */
    char *committer_date;             /* 提交时间 */
    char *message;                     /* 提交信息 */
};

/* tree 对象：一个 tree 包含多个 tree_entry */
struct tree {
    struct object object;
    struct tree_entry *entries;
    int entries_count;
};

/* tree 中的条目 */
struct tree_entry {
    char *name;                        /* 文件/目录名 */
    unsigned char sha1[20];            /* 指向 blob 或 tree */
    enum object_type type;             /* OBJ_BLOB 或 OBJ_TREE */
    unsigned int mode;                 /* Unix 权限位 */
};
```

### 26.3.2 核心命令实现：sha1_file.c / object.c

Git 的核心对象操作在 `sha1_file.c` 和 `object.c` 中：

```c
/*
 * sha1_file.c 中的核心函数
 * 演示：如何写入一个 blob 对象
 */

/*
 * 写入一个 blob 到对象库
 * 返回 SHA-1 哈希值
 */
unsigned char *hash_sha1_file(const void *buf,
                               unsigned long size,
                               const char *type,
                               unsigned char *sha1)
{
    struct object *object;
    /* 1. 创建对象 */
    object = create_object(sha1, type, buf, size);

    /* 2. 写入对象库（.git/objects/ 目录） */
    write_sha1_buffer(sha1, buf, size);

    /* 3. 返回 SHA-1 */
    return sha1;
}

/*
 * 从对象库读取一个对象
 */
void *read_sha1_file(unsigned const char *sha1,
                     enum object_type *type,
                     unsigned long *size)
{
    char *path;
    void *buf;

    /* 1. 根据 SHA-1 构建路径：.git/objects/ab/cdef1234... */
    path = sha1_to_path(sha1);

    /* 2. 从文件读取并解压（Git 用 zlib 压缩） */
    buf = read_file(path, size);

    /* 3. 解析对象头，获取真实类型和大小 */
    *type = parse_sha1_header(buf, size);

    return buf;
}

/*
 * 将 SHA-1 转换为文件路径
 * SHA-1: abcdef0123456789...
 * Path:  .git/objects/ab/cdef0123456789...
 */
char *sha1_to_path(const unsigned char *sha1)
{
    static char path[50];
    /* 前两位作为目录名，后 38 位作为文件名 */
    sprintf(path, ".git/objects/%.2s/%.38s",
            sha1_to_hex(sha1),
            sha1_to_hex(sha1) + 2);
    return path;
}
```

```c
/*
 * object.c 中的对象解析
 */

/* 解析对象（根据类型调用不同的解析函数） */
struct object *parse_object(const unsigned char *sha1)
{
    struct object *obj;
    void *data;
    unsigned long size;
    enum object_type type;

    /* 1. 读取原始数据 */
    data = read_sha1_file(sha1, &type, &size);
    if (!data)
        return NULL;

    /* 2. 根据类型解析 */
    switch (type) {
    case OBJ_BLOB:
        obj = parse_blob(data);
        break;
    case OBJ_TREE:
        obj = parse_tree(data, size);
        break;
    case OBJ_COMMIT:
        obj = parse_commit(data);
        break;
    case OBJ_TAG:
        obj = parse_tag(data);
        break;
    default:
        /* 未知类型 */
        return NULL;
    }

    return obj;
}
```

### 26.3.3 diff 算法：diff.c / patch.c（Myers 算法）

Git 的 diff 功能使用 **Myers 算法**，这是一种经典的最长公共子序列（LCS）变体，能在 O(ND) 时间复杂度内找到两个序列的最小差异。

```c
/*
 * Git diff 的简化版实现演示
 * 展示 Myers 算法的核心思想
 */

/*
 * Myers diff 算法思路：
 * 把两个序列的编辑过程看作"编辑图"上的路径查找
 * 每个格子 (i,j) 表示 A[0..i] 和 B[0..j] 的差异
 * 对角线移动 = 匹配（不操作）
 * 水平移动 = 删除
 * 垂直移动 = 插入
 */

/*
 * 演示：简单的行级 diff
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_LINES 1000

typedef enum {
    DIFF_MATCH,     /* 行匹配 */
    DIFF_DELETE,    /* 从 A 删除 */
    DIFF_INSERT     /* 插入到 B */
} diff_type;

/* diff 结果条目 */
typedef struct {
    diff_type type;
    char *line;
} diff_result;

/*
 * 计算两个字符串数组的最长公共子序列
 * 这只是演示，实际 Git 用更复杂的 Myers 算法
 */
int lcs(char **a, int a_len, char **b, int b_len, int *lcs_len)
{
    /* 动态规划计算 LCS */
    int **dp = malloc((a_len + 1) * sizeof(int *));
    for (int i = 0; i <= a_len; i++)
        dp[i] = malloc((b_len + 1) * sizeof(int));

    for (int i = 0; i <= a_len; i++) {
        for (int j = 0; j <= b_len; j++) {
            if (i == 0 || j == 0) {
                dp[i][j] = 0;
            } else if (strcmp(a[i-1], b[j-1]) == 0) {
                dp[i][j] = dp[i-1][j-1] + 1;
            } else {
                dp[i][j] = (dp[i-1][j] > dp[i][j-1]) ?
                           dp[i-1][j] : dp[i][j-1];
            }
        }
    }

    *lcs_len = dp[a_len][b_len];

    /* 回溯找 LCS */
    int result_len = 0;
    int i = a_len, j = b_len;
    while (i > 0 && j > 0) {
        if (strcmp(a[i-1], b[j-1]) == 0) {
            result_len++;
            i--; j--;
        } else if (dp[i-1][j] > dp[i][j-1]) {
            i--;
        } else {
            j--;
        }
    }

    for (int i = 0; i <= a_len; i++)
        free(dp[i]);
    free(dp);

    return 0;
}

/*
 * 简单的行对行 diff
 */
void simple_diff(const char **a, int a_len,
                 const char **b, int b_len,
                 diff_result *results, int *result_len)
{
    int pos = 0;

    /* 简化版：O(n*m) 暴力比较 */
    int i = 0, j = 0;
    while (i < a_len || j < b_len) {
        if (i < a_len && j < b_len &&
            strcmp(a[i], b[j]) == 0) {
            /* 匹配 */
            results[pos].type = DIFF_MATCH;
            results[pos].line = (char *)a[i];
            pos++;
            i++; j++;
        } else if (j < b_len && (i >= a_len || j < b_len)) {
            /* 插入 */
            results[pos].type = DIFF_INSERT;
            results[pos].line = (char *)b[j];
            pos++;
            j++;
        } else {
            /* 删除 */
            results[pos].type = DIFF_DELETE;
            results[pos].line = (char *)a[i];
            pos++;
            i++;
        }
    }

    *result_len = pos;
}

/* 演示 */
int main(void)
{
    /* 旧文件的行 */
    const char *old_text[] = {
        "第一行",
        "第二行",
        "第三行",
        "第四行",
        "第五行"
    };
    int old_len = 5;

    /* 新文件的行 */
    const char *new_text[] = {
        "第一行",
        "第二行（修改了）",
        "第三行",
        "新增的行",
        "第五行"
    };
    int new_len = 5;

    diff_result results[20];
    int result_len;

    simple_diff(old_text, old_len,
                new_text, new_len,
                results, &result_len);

    printf("=== Git 风格 Diff ===\n\n");

    for (int i = 0; i < result_len; i++) {
        switch (results[i].type) {
        case DIFF_MATCH:
            printf("  %s\n", results[i].line);
            break;
        case DIFF_DELETE:
            printf("- %s\n", results[i].line);
            break;
        case DIFF_INSERT:
            printf("+ %s\n", results[i].line);
            break;
        }
    }

    return 0;
}

// 输出：
// === Git 风格 Diff ===
//
//   第一行
// - 第二行
// + 第二行（修改了）
//   第三行
// + 新增的行
//   第五行
```

### 26.3.4 Git 的链表与 hash table 实现

Git 大量使用自定义的链表和哈希表，这些实现比标准库更轻量、更适合 Git 的使用场景。

```c
/*
 * Git 的链表实现（simplified-sha1-array.c 的思想）
 */

/* Git 风格的链表节点 */
struct sha1_entry {
    unsigned char sha1[20];       /* Git 的 SHA-1 是 20 字节 */
    struct sha1_entry *next;
};

/* 头插法插入 */
static void sha1_list_insert(struct sha1_entry **list,
                              const unsigned char *sha1)
{
    struct sha1_entry *new_entry = malloc(sizeof(*new_entry));
    memcpy(new_entry->sha1, sha1, 20);
    new_entry->next = *list;
    *list = new_entry;
}

/*
 * Git 的哈希表实现（hash.h 的思想）
 * 用于快速查找对象
 */

#define HASHSIZE 256

struct object_entry {
    unsigned char sha1[20];
    enum object_type type;
    struct object_entry *next;
};

struct object_hash {
    struct object_entry *table[HASHSIZE];
};

/* 计算 SHA-1 的哈希值（取前几个字节） */
static unsigned int hash_sha1(const unsigned char *sha1)
{
    return sha1[0];  /* 取第一个字节作为哈希值（简化版） */
}

/* 插入对象 */
void object_hash_insert(struct object_hash *hash,
                        const unsigned char *sha1,
                        enum object_type type)
{
    unsigned int idx = hash_sha1(sha1);
    struct object_entry *entry = malloc(sizeof(*entry));

    memcpy(entry->sha1, sha1, 20);
    entry->type = type;
    entry->next = hash->table[idx];
    hash->table[idx] = entry;
}

/* 查找对象 */
struct object_entry *
object_hash_lookup(struct object_hash *hash,
                   const unsigned char *sha1)
{
    unsigned int idx = hash_sha1(sha1);
    struct object_entry *entry;

    for (entry = hash->table[idx]; entry; entry = entry->next) {
        if (memcmp(entry->sha1, sha1, 20) == 0)
            return entry;
    }
    return NULL;
}
```

---

## 26.4 SQLite 源码阅读（规模适中，注释完整）

SQLite 是世界上最广泛部署的数据库引擎——你的手机浏览器里大概率就在跑 SQLite。它大约有 15 万行 C 代码，注释极其完整（有时注释比代码还多），是学习大型 C 项目和数据库内部原理的绝佳资源。

### 26.4.1 虚拟数据库引擎（VDBE）

VDBE（Virtual Database Engine）是 SQLite 的核心。它不是真正执行 SQL 的引擎，而是一个"虚拟机"——它把 SQL 语句编译成一套"字节码"（bytecode），然后执行这些字节码。

```
mermaid
graph LR
    A["SQL 语句<br/>SELECT * FROM users"] --> B["SQLite 编译器<br/>生成字节码"]
    B --> C["VDBE 虚拟机<br/>执行字节码"]
    C --> D["结果集<br/>返回给用户"]
```

```c
/*
 * VDBE 字节码指令示例
 * 类似于 Java 的字节码，但针对数据库操作设计
 */

/* VDBE 指令类型枚举（sqlite3.h 中定义） */
typedef enum {
    OP_Goto,           /* 无条件跳转 */
    OP_Halt,           /* 停止执行 */
    OP_NewRowid,       /* 生成新的 Row ID */
    OP_Sort,           /* 排序 */
    OP_MakeRecord,     /* 创建记录 */
    OP_OpenRead,       /* 打开表读取 */
    OP_OpenWrite,      /* 打开表写入 */
    OP_OpenEphemeral,  /* 打开临时表 */
    OP_OpenAutoindex,  /* 打开自动索引 */
    OP_Integer,        /* 加载整数常量 */
    OP_String8,        /* 加载字符串 */
    OP_Null,           /* NULL 值 */
    OP_ResultRow,      /* 返回结果行 */
    OP_Move,           /* 移动游标 */
    OP_Yield,          /* 协程让出 */
    OP_Column,         /* 读取列值 */
    OP_Add,            /* 加法 */
    OP_Subtract,       /* 减法 */
    OP_Multiply,       /* 乘法 */
    OP_Divide,         /* 除法 */
    OP_Remainder,      /* 取模 */
    OP_Function,       /* 调用函数 */
    OP_Eq,             /* 比较：等于 */
    OP_Ne,             /* 比较：不等于 */
    OP_Lt,             /* 比较：小于 */
    OP_Le,             /* 比较：小于等于 */
    OP_Gt,             /* 比较：大于 */
    OP_Ge,             /* 比较：大于等于 */
    OP_IsNull,         /* 判断是否为 NULL */
    OP_NotNull,        /* 判断是否非 NULL */
    OP_And,            /* 逻辑与 */
    OP_Or,             /* 逻辑或 */
    OP_Not,            /* 逻辑非 */
    OP_Concat,         /* 字符串连接 */
    OP_Blob,           /* 二进制数据 */
    OP_Transaction,    /* 开始事务 */
    OP_ReadCookie,     /* 读取数据库 cookie */
    OP_SetCookie,      /* 设置数据库 cookie */
    OP_VerifyCookie,   /* 验证 cookie */
    OP_LoadAnalysis,   /* 加载分析信息 */
    OP_DropTable,      /* 删除表 */
    OP_DropIndex,      /* 删除索引 */
    OP_DropTrigger,    /* 删除触发器 */
    OP_IntegrityCk,    /* 完整性检查 */
    OP_IdxInsert,      /* 索引插入 */
    OP_IdxDelete,      /* 索引删除 */
    OP_IdxRowid,       /* 从索引获取 Row ID */
    OP_IdxGE,          /* 索引比较 >= */
    OP_IdxLT,          /* 索引比较 < */
    OP_MemLoad,        /* 从内存加载 */
    OP_MemStore,       /* 存储到内存 */
    OP_MemInt,         /* 存储整数到内存 */
    OP_VUpdate,        /* 虚拟表更新 */
    OP_VFilter,        /* 虚拟表过滤 */
    /* ... 还有更多 */
} OpCode;

/*
 * 一条 VDBE 指令
 * 类似于汇编语言的一条指令
 */
typedef struct VdbeOp Op;
struct VdbeOp {
    OpCode opcode;       /* 操作码 */
    int p1;             /* 第一个操作数 */
    int p2;             /* 第二个操作数 */
    int p3;             /* 第三个操作数（通常是指针） */
    char *p4.p;         /* 第四个操作数（更复杂的类型） */
};

/*
 * 例子：执行 SELECT name FROM users WHERE id = 1
 *
 * 生成的字节码大致如下：
 *
 * 0: OP_Transaction   0     # 开始读取事务
 * 1: OP_Integer       1     # 加载常数 1（id 的值）
 * 2: OP_OpenRead      0 2   # 打开表/索引，cursor 0，root 2
 * 3: OP_Rewind        0 9   # 如果表为空，跳到第 9 行
 * 4: OP_Column        0 0   # 读取第 0 列（id）到栈顶
 * 5: OP_Ne            1 8   # 与栈顶比较，不相等则跳到第 8 行
 * 6: OP_Column        0 1   # 读取第 1 列（name）到栈顶
 * 7: OP_ResultRow     1     # 返回结果行
 * 8: OP_Halt          0     # 结束
 * 9: OP_Transaction   0     # 开始写入事务（如果这是 INSERT/UPDATE/DELETE）
 */

/*
 * SQLite 字节码的"寄存器"
 * VDBE 有一个虚拟的寄存器集合，用于存储临时值
 * 类似于 CPU 的寄存器，但数量更多（通常几百个）
 */
```

### 26.4.2 B-tree 实现 / pager 模块

SQLite 使用 B-tree（特别是 B-tree 的一种变体 B+tree）来存储数据。B+tree 的特点是所有数据都在叶子节点，非叶子节点只存储索引。

```
mermaid
graph TD
    A["B+Tree 根节点<br/>[ptr1|ptr2|ptr3]"] --> B["中间节点1<br/>[key|ptr]"]
    A --> C["中间节点2<br/>[key|ptr]"]
    B --> D["叶子节点1<br/>[data1|data2|data3|...]"]
    B --> E["叶子节点2<br/>[data1|data2|data3|...]"]
    C --> F["叶子节点3<br/>[data1|data2|data3|...]"]
    C --> G["叶子节点4<br/>[data1|data2|data3|...]"]
```

```c
/*
 * SQLite 的 B-tree 实现（btree.c）
 * 这里展示核心数据结构和概念
 */

/*
 * SQLite 存储的基本单位是"页面"（page）
 * 默认页面大小是 4096 字节（4KB）
 * 所有 B-tree 节点都存储在一个页面内
 */

/* 页面类型 */
typedef enum {
    PTRMAP_WHITESPACE,   /* 空白页面 */
    PTRMAP_FREEPAGE,     /* 空闲页面 */
    PTRMAP_BTREE_PAGE,   /* B-tree 叶子页面 */
    PTRMAP_OVERFLOW_PAGE /* 溢出页面 */
} Pgtype;

/*
 * B-tree 页面头部结构
 */
typedef struct BtPage {
    unsigned char flags;         /* 页面类型标志 */
    unsigned short first_free;   /* 第一个空闲槽的偏移 */
    unsigned short cell_count;   /* 单元格数量 */
    unsigned short cell_offset;  /* 单元格数组起始偏移 */
    unsigned char right_ptr[4];  /* 最右指针（用于 B-tree） */
} BtPage;

/*
 * B+tree 叶子页面中的"单元格"
 * 每个单元格存储一个 key-value 对
 */
typedef struct BtreeCell {
    int key_len;                  /* key 的长度 */
    int data_len;                 /* data 的长度 */
    unsigned char *key_data;       /* key 数据 */
    unsigned char *payload;        /* 数据载荷 */
} BtreeCell;

/*
 * SQLite 使用两层缓存：pager 层和 btree 层
 *
 * pager 层负责：
 * 1. 从磁盘读取/写入页面
 * 2. 管理页面缓存
 * 3. 处理事务和 WAL（Write-Ahead Logging）
 * 4. 提供页面锁
 */

/*
 * pager 结构（简化版）
 */
typedef struct Pager {
    int fd;                      /* 文件描述符 */
    unsigned int page_size;      /* 页面大小（通常 4096） */
    int max_page;                /* 文件中的最大页号 */
    void *cache;                 /* 页面缓存（LRU 链表） */
    unsigned char db_header[100];/* 数据库文件头 */

    /* WAL 相关（Write-Ahead Logging） */
    unsigned char *write_log;
    unsigned int log_size;

    /* 锁相关 */
    int lock_state;              /* NO_LOCK, SHARED_LOCK, RESERVED_LOCK... */
} Pager;

/*
 * 从 pager 获取一个页面
 * 如果页面不在缓存中，会从磁盘读取
 */
void *sqlite3PagerGet(Pager *pager, Pgno page_num, int *rc)
{
    /* 检查缓存 */
    PgHdr *page;
    for (page = pager->cache; page; page = page->p_next) {
        if (page->pgno == page_num) {
            /* 缓存命中！直接返回 */
            return page->pData;
        }
    }

    /* 缓存未命中，从磁盘读取 */
    page = malloc(sizeof(PgHdr) + pager->page_size);
    page->pgno = page_num;
    page->pData = (unsigned char *)page + sizeof(PgHdr);

    /* 计算文件中的偏移量并读取 */
    long offset = (page_num - 1) * (long)pager->page_size;
    lseek(pager->fd, offset, SEEK_SET);
    read(pager->fd, page->pData, pager->page_size);

    /* 加入缓存（LRU 队列） */
    add_to_cache(page);

    return page->pData;
}

/*
 * B-tree 游标（用于遍历）
 * 类似于 C++ 的迭代器
 */
typedef struct BtreeCursor {
    BtCursor *pCur;
    int pgno;                    /* 当前页面号 */
    int idx;                     /* 当前页面中的单元格索引 */
    unsigned char *current_key; /* 当前 key */
    unsigned char *current_data; /* 当前 data */
} BtreeCursor;

/* 移动游标到下一个位置 */
int sqlite3BtreeNext(BtreeCursor *pCur)
{
    MemPage *pPage;

    pPage = (MemPage *)sqlite3PagerGet(pCur->pPager, pCur->pgno);

    if (pCur->idx >= pPage->nCell) {
        /* 当前页已遍历完，移到下一页 */
        if (pPage->right) {
            pCur->pgno = pPage->right;
            pCur->idx = 0;
        } else {
            /* 没有更多页面了 */
            return SQLITE_DONE;
        }
    } else {
        pCur->idx++;
    }

    return SQLITE_OK;
}
```

---

## 26.5 Redis 源码阅读（事件驱动 + 数据结构）

Redis 是用 C 语言写的高性能内存数据库，支持多种数据结构（字符串、列表、哈希、集合、有序集合），被广泛应用于缓存、消息队列等场景。它的代码结构清晰，注释丰富，而且使用了大量精巧的数据结构实现。

### 26.5.1 事件循环：aeEventLoop

Redis 的核心是一个事件驱动框架，基于 `epoll`（Linux）、`kqueue`（macOS/BSD）或 `select`（Windows）实现高性能 I/O 多路复用。

```c
/*
 * Redis 事件循环的核心结构
 * 源码在 anet.c / ae.c 中
 */

/* 文件事件类型 */
typedef struct aeFileEvent {
    int mask;                   /* AE_NONE, AE_READABLE, AE_WRITABLE */
    aeFileProc *rFileProc;      /* 读事件回调函数 */
    aeFileProc *wFileProc;      /* 写事件回调函数 */
    void *clientData;          /* 传递给回调的用户数据 */
} aeFileEvent;

/* 时间事件（用于定时任务） */
typedef struct aeTimeEvent {
    long long id;              /* 事件 ID */
    long when_sec;             /* 触发时间（秒） */
    long when_ms;              /* 触发时间（毫秒） */
    aeTimeProc *timeProc;      /* 事件处理函数 */
    aeEventFinalizerProc *finalizerProc; /* 清理函数 */
    void *clientData;
    struct aeTimeEvent *next;
} aeTimeEvent;

/* 已触发的事件 */
typedef struct aeFiredEvent {
    int fd;
    int mask;
} aeFiredEvent;

/* 主事件循环结构 */
typedef struct aeEventLoop {
    int maxfd;                 /* 当前注册的最大 fd */
    long long timeEventNextId; /* 下一个时间事件 ID */
    aeFileEvent *events;       /* 文件事件数组 */
    aeFiredEvent *fired;       /* 已触发事件数组 */
    aeTimeEvent *timeEventHead; /* 时间事件链表 */
    int stop;                  /* 停止标志 */
    void *apidata;             /* 底层 I/O 多路复用的数据 */
    int beforesleep;           /* 睡眠前的回调 */
} aeEventLoop;

/* 事件处理主循环 */
void aeMain(aeEventLoop *eventLoop)
{
    eventLoop->stop = 0;
    while (!eventLoop->stop) {
        /* 处理文件事件和时间事件 */
        aeProcessEvents(eventLoop, AE_ALL_EVENTS);
    }
}

/* 处理所有已触发的事件 */
int aeProcessEvents(aeEventLoop *eventLoop, int flags)
{
    int processed = 0;

    /* 处理时间事件 */
    if (flags & AE_TIME_EVENTS) {
        processed += processTimeEvents(eventLoop);
    }

    /* 处理文件事件 */
    if (flags & AE_FILE_EVENTS) {
        int numevents;

        /* 调用 epoll_wait / kqueue / select 获取就绪事件 */
        numevents = aeApiPoll(eventLoop, tvp);

        for (int i = 0; i < numevents; i++) {
            int fd = eventLoop->fired[i].fd;
            int mask = eventLoop->fired[i].mask;

            /* 根据事件类型调用回调函数 */
            if (mask & AE_READABLE) {
                eventLoop->events[fd].rFileProc(
                    eventLoop, fd,
                    eventLoop->events[fd].clientData, mask);
            }
            if (mask & AE_WRITABLE) {
                eventLoop->events[fd].wFileProc(
                    eventLoop, fd,
                    eventLoop->events[fd].clientData, mask);
            }
            processed++;
        }
    }

    return processed;
}
```

### 26.5.2 对象系统：robj

Redis 的"对象系统"是其灵活性的核心。每个值（string、list、hash 等）在 Redis 内部都是一个 `robj`（Redis Object），通过类型和编码的组合，实现了一种"多态"的效果。

```c
/*
 * Redis 对象结构
 * 源码在 server.h 中定义
 */

/* 对象类型 */
typedef enum {
    OBJ_STRING,   /* 字符串 */
    OBJ_LIST,     /* 列表 */
    OBJ_SET,      /* 集合 */
    OBJ_ZSET,     /* 有序集合 */
    OBJ_HASH,     /* 哈希 */
    OBJ_MODULE,   /* 模块类型 */
    OBJ_STREAM    /* 流（Redis 5.0+） */
} redis_type;

/* 编码方式（同一个类型可以用不同的底层实现） */
typedef enum {
    /* 字符串可以用这些编码 */
    OBJ_ENCODING_INT,        /* 整数（当字符串可以表示为数字时） */
    OBJ_ENCODING_EMBSTR,     /* embstr 编码的字符串（<= 44 字节） */
    OBJ_ENCODING_RAW,        /* 原始字符串（动态分配） */

    /* 列表可以用这些编码 */
    OBJ_ENCODING_LINKEDLIST, /* 双端链表（旧实现） */
    OBJ_ENCODING_ZIPLIST,     /* 压缩列表（小列表） */
    OBJ_ENCODING_QUICKLIST,  /* 快速列表（ziplist + linkedlist） */

    /* 哈希可以用这些编码 */
    OBJ_ENCODING_HT,         /* 哈希表（dict） */
    OBJ_ENCODING_ZIPLIST,    /* 压缩列表（小哈希） */

    /* 集合可以用这些编码 */
    OBJ_ENCODING_INTSET,     /* 整数集合（纯整数集合） */
    OBJ_ENCODING_HT,         /* 哈希表 */

    /* 有序集合可以用这些编码 */
    OBJ_ENCODING_ZIPLIST,    /* 压缩列表（小有序集合） */
    OBJ_ENCODING_SKIPLIST    /* 跳表（大数据集） */
} redis_encoding;

/* Redis 对象结构 */
typedef struct redisObject {
    unsigned type:4;          /* 对象类型（4 位） */
    unsigned encoding:4;       /* 编码方式（4 位） */
    unsigned lru:LRU_BITS;    /* LRU 时间或访问频率 */
    int refcount;             /* 引用计数（用于垃圾回收） */
    void *ptr;                /* 指向实际数据的指针 */
} robj;

/* 创建字符串对象 */
robj *createStringObject(const char *ptr, size_t len)
{
    robj *o;

    if (len <= 44) {
        /* 小字符串使用 embstr 编码：对象和数据在一次分配中 */
        o = zmalloc(sizeof(robj) + len + 1);
        o->encoding = OBJ_ENCODING_EMBSTR;
        o->ptr = (char *)o + sizeof(robj);
        memcpy(o->ptr, ptr, len);
    } else {
        /* 大字符串使用 raw 编码：数据和对象分开分配 */
        o = zmalloc(sizeof(robj));
        o->encoding = OBJ_ENCODING_RAW;
        o->ptr = zmalloc(len + 1);
        memcpy(o->ptr, ptr, len);
    }

    o->type = OBJ_STRING;
    o->refcount = 1;
    return o;
}

/*
 * 为什么 Redis 要用不同的编码？
 * 想象你要装东西：
 * - 小东西（几颗弹珠）用小盒子就行，不用开一个大柜子
 * - 大东西（大象）得用大房间
 * Redis 的"编码"就是"根据数据大小选择合适的存储方式"
 */
```

### 26.5.3 SDS 字符串 / 列表 / 哈希 / 集合 / 有序集合实现

Redis 的每种数据结构都有精妙的实现：

**SDS（Simple Dynamic String）：Redis 的字符串类型**

SDS 比标准 C 字符串更安全、更高效，因为它记录了长度，而且支持动态扩展：

```c
/*
 * SDS 实现
 * 源码在 sds.h / sds.c 中
 */

/* SDS 头结构 */
struct sdshdr {
    int len;      /* 已使用的长度 */
    int free;     /* 剩余空闲长度 */
    char buf[];   /* 柔性数组，存储实际字符串 */
};

/*
 * 为什么要记录 len？
 * 1. strlen() 是 O(1)，而不是 O(n)
 * 2. 二进制安全，可以包含 \0
 * 3. 避免缓冲区溢出
 */

/* 创建一个 SDS 字符串 */
sds sdsnew(const char *init) {
    size_t initlen = (init == NULL) ? 0 : strlen(init);
    sds s = s_malloc(sizeof(struct sdshdr) + initlen + 1);
    struct sdshdr *sh = (void *)s;

    sh->len = initlen;
    sh->free = 0;
    if (initlen && init)
        memcpy(s + sizeof(struct sdshdr), init, initlen);
    s[sizeof(struct sdshdr) + initlen] = '\0';
    return s;
}

/* 追加字符串（自动扩容） */
sds sdscat(sds s, const char *t) {
    return sdscatlen(s, t, strlen(t));
}

sds sdscatlen(sds s, const void *t, size_t len) {
    struct sdshdr *sh, *newsh;
    size_t curlen = sdslen(s);

    /* 扩容：如果剩余空间不够，就扩大容量 */
    sh = (void *)(s - sizeof(struct sdshdr));
    if (sdsavail(s) < len) {
        size_t newlen = curlen + len;
        newsh = s_realloc(sh, sizeof(struct sdshdr) + newlen + 1);
        newsh->free = 0;
        newsh->len = newlen;
        s = (char *)newsh + sizeof(struct sdshdr);
    }

    /* 追加数据 */
    memcpy(s + curlen, t, len);
    sh = (void *)(s - sizeof(struct sdshdr));
    sh->len = curlen + len;
    s[curlen + len] = '\0';
    return s;
}
```

**QuickList：列表的底层实现**

Redis 的列表使用 quicklist（快速列表），它是 ziplist 和 linkedlist 的结合——用 linkedlist 串联多个 ziplist，既避免了 ziplist 过大时的扩容成本，又避免了纯 linkedlist 的内存开销：

```c
/*
 * QuickList 结构
 * 本质上是一个双向链表，每个节点是一个 ziplist
 */

/* QuickList 节点 */
typedef struct quicklistNode {
    struct quicklistNode *prev;
    struct quicklistNode *next;
    unsigned char *zl;         /* 压缩列表指针 */
    size_t sz;                 /* ziplist 字节大小 */
    unsigned int count : 16;   /* ziplist 中的元素数量 */
    unsigned int encoding : 2; /* RAW（原始）还是 LZF（压缩） */
} quicklistNode;

/* QuickList 主结构 */
typedef struct quicklist {
    quicklistNode *head;        /* 头节点 */
    quicklistNode *tail;        /* 尾节点 */
    unsigned long count;       /* 总元素数 */
    unsigned int fill : 16;    /* 每个 ziplist 最大容量 */
    unsigned int compress : 16;/* 压缩深度 */
} quicklist;
```

### 26.5.4 zmalloc：包装 libc malloc

Redis 不用标准的 `malloc`，而是封装了一个自己的内存分配器 `zmalloc`，目的是追踪内存使用情况：

```c
/*
 * zmalloc 内存分配器
 * 源码在 zmalloc.c 中
 */

/* 全局变量：已分配的内存总量 */
static size_t used_memory = 0;

/* 线程安全 */
pthread_mutex_t used_memory_mutex = PTHREAD_MUTEX_INITIALIZER;

/* 分配内存（带统计） */
void *zmalloc(size_t size) {
    void *ptr = malloc(size + sizeof(size_t));

    if (!ptr) {
        /* 内存分配失败，Redis 会尝试 flush 到磁盘然后退出 */
        zmalloc_oom_handler();
    }

    /* 在分配的内存前面存储大小，方便 free 时统计 */
    *((size_t *)ptr) = size;

    /* 更新全局内存计数 */
    update_zmalloc_stat(zmalloc_size(ptr));

    /* 返回实际可用的内存起始地址 */
    return (char *)ptr + sizeof(size_t);
}

/* 释放内存 */
void zfree(void *ptr) {
    if (ptr == NULL) return;

    void *realptr = (char *)ptr - sizeof(size_t);
    size_t oldsize = *((size_t *)realptr);

    /* 更新统计并释放 */
    update_zmalloc_stat_free(oldsize);
    free(realptr);
}

/* 获取已使用的内存总量 */
size_t zmalloc_used_memory(void) {
    size_t um;
    pthread_mutex_lock(&used_memory_mutex);
    um = used_memory;
    pthread_mutex_unlock(&used_memory_mutex);
    return um;
}

/* 显示内存使用统计 */
void zmalloc_dump_rss(void) {
    size_t rss = zmalloc_get_rss(); /* /proc/self/statm 中的 RSS */
    printf("Redis used_memory: %zu, rss: %zu, ratio: %.2f\n",
           zmalloc_used_memory(),
           rss,
           (double)rss / zmalloc_used_memory());
}
```

---

## 26.6 NGINX 源码阅读（高性能服务器）

NGINX 是高性能 HTTP 服务器和反向代理服务器，以事件驱动、非阻塞 I/O 著称。它的代码结构优雅，模块化设计非常值得学习。

### 26.6.1 模块化架构

NGINX 的核心非常小，只提供基本的事件处理和 HTTP 框架。所有的功能（HTTP、负载均衡、SSL 等）都以**模块**的形式存在：

```
mermaid
graph TB
    A["NGINX Core<br/>ngx_core<br/>事件循环、模块管理"] --> B["HTTP 模块链"]
    A --> C["Mail 模块链"]
    A --> D["Stream 模块链"]
    B --> E["ngx_http_module<br/>HTTP 核心模块"]
    B --> F["ngx_http_static_module<br/>静态文件"]
    B --> G["ngx_http_proxy_module<br/>反向代理"]
    B --> H["ngx_http_ssl_module<br/>SSL/TLS"]
    B --> I["ngx_http_gzip_module<br/>压缩"]
```

```c
/*
 * NGINX 模块结构
 * 源码在 ngx_module.h 中
 */

/* 模块类型 */
typedef enum {
    NGX_CORE_MODULE = 0,      /* 核心模块（event, error_log, cpuinfo...） */
    NGX_CONF_MODULE,           /* 配置解析模块 */
    NGX_EVENT_MODULE,          /* 事件模块（epoll, kqueue, select...） */
    NGX_HTTP_MODULE,           /* HTTP 模块 */
    NGX_MAIL_MODULE,           /* Mail 模块 */
    NGX_STREAM_MODULE          /* Stream 模块（TCP/UDP 代理） */
} ngx_module_type_e;

/* 模块上下文（每个类型的模块有自己特定的接口） */
typedef struct {
    ngx_str_t             name;           /* 模块名称 */
    ngx_uint_t            type;           /* 模块类型 */
    void               *(*init_master)(ngx_log_t *log);
    ngx_int_t           (*init_module)(ngx_cycle_t *cycle);
    ngx_int_t           (*init_process)(ngx_cycle_t *cycle);
    ngx_int_t           (*init_thread)(ngx_cycle_t *cycle);
    void                (*exit_thread)(ngx_cycle_t *cycle);
    void                (*exit_process)(ngx_cycle_t *cycle);
    void                (*exit_master)(ngx_cycle_t *cycle);
} ngx_core_module_t;

/* HTTP 模块特定上下文 */
typedef struct {
    /* 配置解析阶段：创建每-server/每-location 的配置结构 */
    ngx_int_t   (*preconfiguration)(void);
    ngx_int_t   (*postconfiguration)(void);

    /* 创建模块配置（用于 http {} 块） */
    void       *(*create_main_conf)(ngx_conf_t *cf);
    char       *(*init_main_conf)(ngx_conf_t *cf, void *conf);

    /* 创建 server 配置（用于 server {} 块） */
    void       *(*create_srv_conf)(ngx_conf_t *cf);
    char       *(*merge_srv_conf)(ngx_conf_t *cf, void *parent, void *child);

    /* 创建 location 配置（用于 location {} 块） */
    void       *(*create_loc_conf)(ngx_conf_t *cf);
    char       *(*merge_loc_conf)(ngx_conf_t *cf, void *parent, void *child);
} ngx_http_module_t;

/* NGINX 模块结构（所有模块都长这样） */
typedef struct ngx_module_s {
    ngx_uint_t            ctx_index;     /* 在同类模块中的索引 */
    ngx_uint_t            index;          /* 全局模块索引 */

    char                 *name;           /* 模块名称 */

    /* 模块特定上下文 */
    void                 *ctx;

    /* 模块命令（配置指令）数组 */
    ngx_command_t        *commands;

    /* 模块类型 */
    ngx_uint_t            type;

    /* 回调函数 */
    ngx_int_t           (*init_master)(ngx_log_t *log);
    ngx_int_t           (*init_module)(ngx_cycle_t *cycle);
    ngx_int_t           (*init_process)(ngx_cycle_t *cycle);
    ngx_int_t           (*init_thread)(ngx_cycle_t *cycle);
    void                (*exit_thread)(ngx_cycle_t *cycle);
    void                (*exit_process)(ngx_cycle_t *cycle);
    void                (*exit_master)(ngx_cycle_t *cycle);
} ngx_module_t;

/*
 * 理解 NGINX 模块化的关键：
 * NGINX 把"模块"当作插件。只要遵循统一的接口，
 * 任何人都可以编写新模块并编译进 NGINX。
 * 这就是 NGINX 生态如此丰富的原因！
 */
```

### 26.6.2 事件驱动：ngx_event_t / ngx_connection_t

NGINX 的 I/O 模型基于事件驱动，使用 `epoll`（Linux）或 `kqueue`（BSD/macOS）实现高效的多路复用：

```c
/*
 * NGINX 事件结构
 * 源码在 ngx_event.h 中
 */

/* 事件结构 */
typedef struct ngx_event_s {
    void            *data;           /* 通常指向对应的 connection */

    unsigned         write:1;        /* 写事件 */
    unsigned         accept:1;       /* 接受连接事件 */

    /* 事件状态标志 */
    unsigned         instance:1;    /* 用于避免惊群效应 */
    unsigned         active:1;      /* 是否已添加到 I/O 多路复用 */
    unsigned         disabled:1;   /* 是否被禁用 */
    unsigned         locked:1;      /* 正在处理（防止重入） */

    unsigned         ready:1;       /* 事件就绪 */
    unsigned         error:1;       /* 发生错误 */
    unsigned         eof:1;        /* 对端关闭连接 */
    unsigned         timedout:1;    /* 超时 */
    unsigned         dested:1;      /* 已关闭 */

    /* 事件处理程序 */
    ngx_event_handler_pt  handler;  /* 事件回调函数！ */

    ngx_uint_t       instance;      /* 实例计数器 */
    ngx_uint_t       log;           /* 日志 */

    /* 定时器 */
    ngx_msec_t       timer;         /* 定时器到期时间 */
    unsigned         timer_set:1;   /* 是否已设置定时器 */

    /* 异步 I/O */
    void            *file;          /* 关联的文件 */
    int              fd;            /* 文件描述符 */
} ngx_event_t;

/* 事件处理函数类型（函数指针） */
typedef void (*ngx_event_handler_pt)(ngx_event_t *ev);

/* 连接结构 */
typedef struct ngx_connection_s {
    int               fd;            /* 套接字文件描述符 */
    ngx_event_t      *read;         /* 读事件 */
    ngx_event_t      *write;        /* 写事件 */

    /* 远端地址信息 */
    struct sockaddr  *sockaddr;
    socklen_t         socklen;
    ngx_str_t         addr_text;   /* IP 地址字符串 */

    /* 请求对象 */
    void             *data;         /* 通常指向 ngx_http_request_t */

    /* 状态 */
    unsigned          shared:1;     /* 是否是共享连接 */
    unsigned          sendfile:1;   /* 是否使用 sendfile */
    unsigned          lingering_close:1; /* 优雅关闭中 */

    /* 缓冲 */
    ngx_buf_t        *recv_start;
    ngx_buf_t        *recv_end;
    ngx_buf_t        *send_start;
    ngx_buf_t        *send_end;
} ngx_connection_t;

/*
 * NGINX 事件处理流程：
 *
 * 1. 主进程监听端口（socket fd）
 * 2. 某个 worker 进程调用 accept() 接受连接，得到 connection
 * 3. 设置 connection->read->handler = ngx_http_request_handler
 * 4. 把 fd 添加到 epoll 中（EPOLLIN）
 * 5. epoll_wait() 返回就绪事件
 * 6. 调用对应的 handler
 */
```

### 26.6.3 内存池：ngx_pool_t

NGINX 的内存池是其高性能的秘诀之一。很多情况下，一个请求需要多次分配内存（读请求头、读请求体、生成响应头、生成响应体……），如果每次都调用 `malloc`，会有大量碎片和开销。NGINX 的做法是：**每个连接一个内存池，连接结束时一次性释放所有内存。**

```c
/*
 * NGINX 内存池
 * 源码在 ngx_palloc.h / ngx_palloc.c 中
 */

/* 内存块（chain of blocks） */
typedef struct ngx_pool_s {
    /* 内存块链表 */
    struct ngx_pool_s       *current;  /* 当前可用的块 */
    struct ngx_pool_s       *large;    /* 大块内存链表（> page_size） */

    /* 清理回调链表（请求结束时执行） */
    ngx_pool_cleanup_t     *cleanup;

    size_t                  max;      /* 小块最大 size（通常 4096） */
    size_t                  size;     /* 当前块的大小 */
    size_t                  aligned;  /* 对齐后的大小 */

    /* 分配统计（可选） */
    ngx_uint_t              count;    /* 分配次数 */
} ngx_pool_t;

/* 分配一块内存 */
void *ngx_palloc(ngx_pool_t *pool, size_t size)
{
    ngx_pool_t *p;

    /* 如果是小块分配，尝试从当前块获取 */
    if (size <= pool->max) {
        p = pool->current;

        /* 遍历当前块和后续块 */
        do {
            u_char *m = p->d.last;      /* 当前块的空闲起始位置 */

            /* 对齐到 NGX_ALIGNMENT（通常是 8 或 16） */
            m = ngx_align_ptr(m, NGX_ALIGNMENT);

            /* 检查当前块剩余空间够不够 */
            if ((size_t)(p->d.end - m) >= size) {
                p->d.last = m + size;  /* 移动指针，表示已分配 */
                return m;               /* 返回分配的地址 */
            }

            p = p->d.next;             /* 当前块不够，试试下一个块 */
        } while (p);

        /* 所有现有块都不够，创建新块 */
        p = ngx_new_pool(pool, size);
        if (!p) return NULL;
    }

    /* 如果是大块分配，直接用 malloc（挂在 large 链表上） */
    return ngx_palloc_large(pool, size);
}

/* 创建新块 */
static ngx_pool_t *ngx_new_pool(size_t size)
{
    ngx_pool_t *p;

    /* 用 malloc 分配一个块（包括 ngx_pool_t 头 + 实际可用空间） */
    p = malloc(size);
    if (!p) return NULL;

    /* 初始化块头部 */
    p->d.end = (u_char *)p + size;        /* 块末尾 */
    p->d.last = (u_char *)p + sizeof(ngx_pool_t); /* 跳过头部，从可用空间开始 */
    p->d.next = NULL;
    p->d.failed = 0;

    return p;
}

/* 销毁内存池（一次性释放所有内存） */
void ngx_destroy_pool(ngx_pool_t *pool)
{
    ngx_pool_t *p, *n;
    ngx_pool_large_t *l;

    /* 释放 large 链表 */
    for (l = pool->large; l; l = l->next) {
        if (l->alloc) {
            free(l->alloc);  /* 大块用 malloc，直接 free */
        }
    }

    /* 释放所有块 */
    for (p = pool, n = pool->d.next; /* nothing */; p = n) {
        free(p);  /* 整块 free，包括头部 */
        n = p->d.next;
        if (!n) break;
    }
}

/*
 * 内存池的好处：
 *
 * 1. 减少 malloc 调用次数（一大块分多次用）
 * 2. 减少内存碎片
 * 3. 一次性释放所有内存（连接关闭时）
 * 4. 分配 O(1) 速度
 *
 * 这就像一次性买一整箱可乐，
 * 比每次口渴了去便利店买一瓶更高效、更方便处理空瓶子。
 */

/*
 * 清理回调（请求结束时执行收尾工作）
 */
typedef void (*ngx_pool_cleanup_pt)(void *data);

typedef struct ngx_pool_cleanup_s {
    ngx_pool_cleanup_pt   handler;  /* 清理函数 */
    void                 *data;    /* 传递给清理函数的数据 */
    ngx_pool_cleanup_t   *next;    /* 链表 */
} ngx_pool_cleanup_t;

/* 注册清理回调 */
ngx_pool_cleanup_t *ngx_pool_cleanup_add(ngx_pool_t *p, size_t size)
{
    ngx_pool_cleanup_t *c;

    c = ngx_palloc(p, sizeof(ngx_pool_cleanup_t));
    if (!c) return NULL;

    /* 如果调用者需要额外数据空间 */
    if (size) {
        c->data = ngx_palloc(p, size);
    } else {
        c->data = NULL;
    }

    c->handler = NULL;
    c->next = p->cleanup;
    p->cleanup = c;

    return c;
}
```

---

## 26.7 阅读大型 C 代码的通用技巧

读大型代码就像在一座陌生的城市里找路——你需要地图、指南针，还需要一些"探险技巧"。这一节总结的方法适用于任何大型 C 项目。

### 26.7.1 从 Makefile / CMakeLists.txt 了解项目结构

拿到一个陌生项目，第一步不是打开源码就开始读，而是先弄清楚项目是怎么组织的。`Makefile` 和 `CMakeLists.txt` 就是你的"项目地图"。

```bash
# 先看项目结构
ls -la
# 常见的目录结构：
# src/       - 源代码
# include/   - 头文件
# test/      - 测试
# docs/      - 文档
# build/     - 构建目录
# lib/       - 库文件

# 看 Makefile，了解编译规则
cat Makefile

# 如果用 CMake
cat CMakeLists.txt

# 常见的构建命令
make            # 普通构建
make -j8        # 8 核并行构建（快很多）
make clean      # 清理
make test       # 运行测试
make install    # 安装

# 如果是 autotools 项目
./configure && make
```

```cmake
# CMakeLists.txt 示例解读
cmake_minimum_required(VERSION 3.10)
project(MyProject C)  # 项目名，使用 C 语言

# 设置 C 标准
set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED ON)

# 头文件目录
include_directories(include)

# 源文件目录
aux_source_directory(src SRCS)

# 生成可执行文件
add_executable(myapp ${SRCS})

# 链接库
target_link_libraries(myapp pthread m)  # 链接 pthread 和 math 库

# 添加编译选项
target_compile_options(myapp PRIVATE -Wall -Wextra -O2)

# 测试
enable_testing()
add_test(NAME myapp_test COMMAND myapp)
```

### 26.7.2 找到入口点：main 函数

任何程序都有入口点，从 `main` 函数开始，顺藤摸瓜，是最直接的阅读方式：

```c
/*
 * main 函数是程序的"大门"
 * 从这里开始，你可以画出程序的"调用路线图"
 */

int main(int argc, char *argv[])
{
    /* 1. 解析命令行参数 */
    parse_options(argc, argv);

    /* 2. 初始化 */
    init_environment();

    /* 3. 加载配置 */
    load_config();

    /* 4. 主循环 / 主要逻辑 */
    return run_main_loop();
}

/*
 * 常见入口点模式：
 *
 * 服务器程序：main -> 初始化 -> 事件循环（永不退出）
 * 命令行工具：main -> 解析参数 -> 执行命令 -> 退出
 * 守护进程：main -> fork() -> 子进程进入事件循环，父进程退出
 */
```

### 26.7.3 关注核心数据结构：先读 .h 文件，再读 .c 实现

大型 C 项目，头文件是"骨架"，源文件是"血肉"。读代码的正确顺序是：

```
1. 先读 .h 文件，搞清楚数据结构、函数签名
2. 再读 .c 文件，理解函数实现
```

```bash
# 找核心头文件
find . -name "*.h" -type f | head -20

# 看某个模块的头文件，了解它的接口
cat include/module.h

# 看对应的实现
cat src/module.c

# 如果某个结构体很复杂，用 pahole 工具看内存布局
pahole build/module.elf -C ComplexStruct
```

```c
/*
 * 头文件阅读技巧
 * 头文件 = 模块的"说明书"
 */

/* 1. 先看结构体定义，搞清楚有哪些成员 */
struct my_struct {
    int field1;         /* 这个字段干什么用 */
    void *field2;       /* 指向什么 */
    /* ... */
};

/* 2. 看函数声明，了解模块提供什么功能 */
void my_struct_init(struct my_struct *s);
void my_struct_destroy(struct my_struct *s);
int my_struct_process(struct my_struct *s, int data);

/* 3. 看宏定义，了解常量、配置选项 */
#define MY_MAX_SIZE 1024
#define MY_FLAG_ENABLED 0x01
#define MY_FLAG_VERBOSE 0x02

/* 4. 看条件编译，了解平台差异 */
#ifdef __linux__
    /* Linux 特有代码 */
#elif defined(_WIN32)
    /* Windows 特有代码 */
#endif
```

### 26.7.4 画图笔记：函数调用图、数据流图、状态机图

读代码时，一定要动笔！画图能帮你理清思路，发现隐藏的关系：

**函数调用图示例：**

```
mermaid
graph TD
    A["main()"] --> B["init()"]
    A --> C["parse_args()"]
    B --> D["setup_event_loop()"]
    B --> E["load_config()"]
    D --> F["epoll_create()"]
    D --> G["register_handlers()"]
    G --> H["on_read()"]
    G --> I["on_write()"]
    H --> J["process_request()"]
    J --> K["query_database()"]
    J --> L["generate_response()"]
```

**数据流图示例：**

```
mermaid
graph LR
    A["输入数据<br/>bytes"] --> B["解析器<br/>Parser"]
    B --> C{"数据有效?"}
    C -->|是| D["业务逻辑<br/>Processor"]
    C -->|否| E["错误处理<br/>Error Handler"]
    D --> F["格式化<br/>Formatter"]
    F --> G["输出数据<br/>Response"]
    E --> G
```

**状态机图示例：**

```
mermaid
graph TD
    A["IDLE"] -->|"收到请求| REQUESTED"]
    REQUESTED -->|"验证通过| VERIFIED"]
    REQUESTED -->|"验证失败| REJECTED"]
    VERIFIED -->|"处理中| PROCESSING"]
    PROCESSING -->|"成功| COMPLETED"]
    PROCESSING -->|"失败| FAILED"]
    COMPLETED -->|"超时或重置| IDLE"]
    REJECTED -->|"重试| REQUESTED"]
    FAILED -->|"重试| REQUESTED"]
```

### 26.7.5 善用 grep -r / ctags / cscope 做符号追踪

代码量大的时候，`grep` 是你的好朋友：

```bash
# 查找函数定义
grep -rn "void process_data" --include="*.c"
grep -rn "void process_data" --include="*.h"

# 查找结构体定义
grep -rn "struct my_struct {" --include="*.h"

# 查找宏定义
grep -rn "#define MAX_" --include="*.h"

# 查找某个符号的所有引用
grep -rn "callback" --include="*.c" | head -30

# 忽略某些目录（构建产物）
grep -rn "TODO" --exclude-dir=build --exclude-dir=.git

# 用 ripgrep（更快）
rg "process_data" -t c

# 统计某个函数的调用次数
rg "process_data\(" -t c | wc -l
```

```bash
# ctags + cscope 组合
# 生成 tags 文件
ctags -R --languages=c -f tags .

# 在 Vim 中使用
vim -t function_name        # 跳转到定义
Ctrl + ]                    # 跳转
Ctrl + t                    # 返回
:tselect                    # 列出所有匹配

# 生成 cscope 数据库
cscope -Rbq

# 查找函数定义
vim -t my_function

# 在 Vim 中查询
:cs find g function_name    # 找定义
:cs find c function_name    # 找调用
:cs find s symbol          # 找符号
```

### 26.7.6 理解平台特定代码：#ifdef _WIN32 / __linux__ 分支

跨平台代码里，到处都是条件编译。理解这些分支是阅读跨平台代码的关键：

```c
/*
 * 跨平台代码示例
 */

#include <stdio.h>

/* 1. Windows vs Linux 的基本差异 */
#ifdef _WIN32
    /* Windows */
    #include <windows.h>
    #define SLEEP_MS(ms) Sleep(ms)
    typedef int sockfd_t;
#else
    /* Linux / Unix / macOS */
    #include <unistd.h>
    #include <sys/socket.h>
    #define SLEEP_MS(ms) usleep((ms) * 1000)
    typedef int sockfd_t;
#endif

/* 2. 获取错误信息 */
#ifdef _WIN32
    char *get_error_message(DWORD err) {
        static char buf[256];
        FormatMessageA(FORMAT_MESSAGE_FROM_SYSTEM,
                       NULL, err, 0, buf, sizeof(buf), NULL);
        return buf;
    }
#else
    char *get_error_message(int err) {
        return strerror(err);
    }
#endif

/* 3. 文件路径分隔符 */
#ifdef _WIN32
    #define PATH_SEP '\\'
    #define PATH_SEP_STR "\\"
#else
    #define PATH_SEP '/'
    #define PATH_SEP_STR "/"
#endif

/* 4. 原子操作 */
#ifdef _WIN32
    #define atomic_inc(ptr) InterlockedIncrement(ptr)
    #define atomic_dec(ptr) InterlockedDecrement(ptr)
#else
    #define atomic_inc(ptr) __sync_add_and_fetch(ptr, 1)
    #define atomic_dec(ptr) __sync_sub_and_fetch(ptr, 1)
#endif

/* 5. 大小端检测 */
#ifdef __BYTE_ORDER__
    #if __BYTE_ORDER__ == __ORDER_BIG_ENDIAN__
        #define IS_BIG_ENDIAN 1
    #else
        #define IS_BIG_ENDIAN 0
    #endif
#endif

int main(void)
{
    printf("当前平台: ");
#ifdef _WIN32
    printf("Windows\n");
#elif defined(__linux__)
    printf("Linux\n");
#elif defined(__APPLE__)
    printf("macOS\n");
#else
    printf("Unknown\n");
#endif

    printf("路径分隔符: %s\n", PATH_SEP_STR);

    /* 休眠 100 毫秒 */
    SLEEP_MS(100);

    printf("错误信息示例: %s\n", get_error_message(0));

    return 0;
}
```

---

## 本章小结

恭喜你完成了"大型 C 代码阅读"的探索之旅！本章我们一起揭开了 Linux 内核、Git、Redis、SQLite、NGINX 这些顶级开源项目的面纱。

**核心要点回顾：**

1. **Linux 内核编码风格**：Tab 缩进、K&R 括号风格、全小写命名、80 字符限制。理解了这些，你就不会在内核代码里迷路。

2. **GNU C 扩展**：内联汇编、`__attribute__`、`__builtin_expect` 等。这些扩展让 C 语言变得更强大，但也会让代码看起来"不像 C"。

3. **内核数据结构**：侵入式链表 `list_head`、`container_of` 宏、`likely`/`unlikely` 分支预测优化、RCU 无锁同步、slab allocator 内存池。这些是内核代码的"基础设施"。

4. **代码阅读工具链**：`ctags`/`cscope` 做符号跳转、`pahole` 看结构体内存布局、`LXR`/`OpenGrok` 做 Web 交叉引用。工具用对了，事半功倍。

5. **Git 源码**：理解了 blob/tree/commit/tag 四种对象模型，以及 SHA-1 对象库的工作方式。

6. **SQLite 源码**：理解了 VDBE 虚拟数据库引擎和 B+tree 存储引擎。数据库不是魔法，它也是用 C 代码实现的！

7. **Redis 源码**：理解了事件循环 `aeEventLoop`、对象系统 `robj`、SDS 字符串、快速列表 `quicklist`，以及自定义内存分配器 `zmalloc`。

8. **NGINX 源码**：理解了模块化架构、事件驱动 I/O（`ngx_event_t`/`ngx_connection_t`）、内存池 `ngx_pool_t`。

9. **通用阅读技巧**：从 Makefile 了解结构、从 `main` 函数开始、头文件先行、善用 grep/画图理清思路、理解跨平台条件编译。

**继续学习之路：**

- 选择一个感兴趣的项目（推荐 Git 或 Redis），clone 到本地，用本章介绍的工具和方法深入阅读
- 尝试给这些项目提交一个 bug fix 或小功能，这是最好的学习方式
- 阅读内核邮件列表（LKML）和各项目的 issue，了解开发者们是怎么讨论问题的

大型代码阅读不是一朝一夕的事，它需要耐心、好奇心和正确的方法。希望本章能成为你探索路上的"藏宝图"，带你发现代码世界里的无限精彩！

> 记住：每一行伟大的代码，都是从"Hello World"开始的。你已经走了很远，继续加油！
