+++
title = "第 24 章：线程与并发编程"
weight = 240
date = "2026-03-29T22:34:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 第 24 章：线程与并发编程

> "人生最痛苦的事是什么？是你在洗碗，女朋友在催你陪她聊天，老板在催你交报告，而你只能一件事一件事来。欢迎来到并发编程的世界——在这里，你可以同时"分身乏术"变成"分身有术"！"

## 24.1 线程基础

### 24.1.1 线程 vs 进程：共享地址空间的"合租室友"

在正式进入线程的世界之前，咱们先来聊聊线程和进程这对"孪生兄弟"。它们都是操作系统调度的基本单位，但性格迥异，各有各的脾气。

**进程（Process）** 就像是独栋别墅。每栋别墅有自己独立的地址空间（内存）、独立的门牌号（PID）、独立的院子（系统资源）。别墅之间互不干扰，你想拆墙装修随便你，隔壁别墅完全感知不到。但如果两栋别墅要互相串门？那得走大门、填访客登记，麻烦得很。

**线程（Thread）** 则像是合租公寓里的室友。大家共享同一套公寓的地址空间、厨房、卫生间、客厅，但各自有自己独立的"小卧室"（栈空间、寄存器上下文）。室友之间交流直接喊一嗓子就行，不用出门，不用登记。但问题来了——厨房只有一间，早上两个人同时想用灶台炒菜，那就得打架了！

```
┌─────────────────────────────────────────────────────────┐
│                      进程 A                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐      │
│  │   线程 1    │  │   线程 2    │  │   线程 3    │      │
│  │  栈 | 寄存器│  │  栈 | 寄存器│  │  栈 | 寄存器│      │
│  └─────────────┘  └─────────────┘  └─────────────┘      │
│  ←─────────── 共享地址空间（堆、全局数据、代码）────────→ │
└─────────────────────────────────────────────────────────┘

┌───────────────────┐        ┌───────────────────┐
│     进程 A        │        │     进程 B        │
│ ┌───┐ ┌───┐ ┌───┐│        │ ┌───┐ ┌───┐      │
│ │T1 │ │T2 │ │T3 ││        │ │T1 │ │T2 │      │
│ └───┘ └───┘ └───┘│        │ └───┘ └───┘      │
│ 独立地址空间       │        │ 独立地址空间       │
└───────────────────┘        └───────────────────┘
```

线程的优势在哪里？

1. **创建销毁快**：创建线程比创建进程快 10~100 倍，因为不用复制整个地址空间
2. **通信简单**：共享地址空间意味着数据共享是"免费的"，不用进程间通信（IPC）那些繁琐手段
3. **切换开销小**：线程切换只切换寄存器和栈，进程切换还要切换页表、缓存等"大家伙"

但线程的劣势也很明显——**共享即麻烦**。同一块内存可以被多个线程同时读写，稍不注意就乱成一锅粥。这正是我们本章要重点攻克的问题！

### 24.1.2 线程创建与回收：`pthread_create` / `pthread_join` / `pthread_detach`

好，理论讲够了，咱们来点实际的！POSIX 线程（俗称 `pthread`）是 Unix/Linux 系统下线程编程的事实标准。在 Linux 上使用时，记得编译时加 `-pthread` 链接选项：

```bash
gcc -pthread my_thread.c -o my_thread
```

#### 创建线程：`pthread_create`

```c
#include <stdio.h>
#include <pthread.h>
#include <unistd.h>

// 线程执行函数，返回 void*，参数是 void*
void* hello_thread(void* arg) {
    char* name = (char*)arg;
    printf("你好，我是线程：%s！\n", name);  // 输出：我好，我是线程：Worker1！
    printf("我的线程 ID 是：%lu\n", pthread_self());  // 输出：我的线程 ID 是：140234567890112
    sleep(1);
    return NULL;  // 返回值会被 pthread_join 获取
}

int main() {
    pthread_t tid1, tid2;

    // pthread_create 的四个参数：
    // 1. pthread_t* - 用来存储新线程的 ID
    // 2. const pthread_attr_t* - 线程属性（NULL 用默认属性）
    // 3. void* (*)(void*) - 线程执行函数
    // 4. void* - 传给线程函数的参数
    int ret = pthread_create(&tid1, NULL, hello_thread, "Worker1");
    if (ret != 0) {
        perror("线程1创建失败");
        return 1;
    }

    ret = pthread_create(&tid2, NULL, hello_thread, "Worker2");
    if (ret != 0) {
        perror("线程2创建失败");
        return 1;
    }

    printf("主线程：我已经创建了两个工人！\n");
    printf("主线程继续执行其他任务...\n");

    // 等待线程结束（如果不等待，main 提前结束可能导致线程被强制终止）
    pthread_join(tid1, NULL);
    pthread_join(tid2, NULL);

    printf("主线程：两个工人都干完活了，收工！\n");
    return 0;
}
```

> 主线程就像包工头，创建完工人后得等他们都干完活才能宣布项目完成。`pthread_join` 就是包工头的"点名册"——必须所有人都到齐了才能散会。

#### 线程回收：`pthread_join` 与 `pthread_detach`

线程结束后，它的"遗产"（主要是栈空间）需要有人来处理。POSIX 线程提供了两种回收方式：

**`pthread_join`**：主线程等待指定线程结束，并获取其返回值。这就像"领导必须确认每个人完成任务才让下班"。

```c
#include <stdio.h>
#include <pthread.h>
#include <unistd.h>

void* compute_sum(void* arg) {
    int n = *(int*)arg;
    long long sum = 0;
    for (int i = 1; i <= n; i++) {
        sum += i;
    }
    printf("[线程 %lu] 计算 1 到 %d 的和 = %lld\n", pthread_self(), n, sum);

    long long* result = malloc(sizeof(long long));
    *result = sum;
    return result;  // 返回动态分配的内存
}

int main() {
    pthread_t tid;
    int num = 100;

    pthread_create(&tid, NULL, compute_sum, &num);

    void* retval;
    // pthread_join 会阻塞，直到线程结束
    // retval 接收线程的返回值（void*）
    pthread_join(tid, &retval);

    long long* result = (long long*)retval;
    printf("主线程：收到结果 %lld，分配内存已释放。\n", *result);
    free(result);  // 别忘了释放线程返回的内存！

    return 0;
}
```

**`pthread_detach`**：将线程标记为"自生自灭"模式，线程结束后自动释放资源，主线程无需等待。这就像"授权员工自己管理自己的时间，到点下班不用汇报"。

```c
#include <stdio.h>
#include <pthread.h>
#include <unistd.h>

void* background_task(void* arg) {
    int id = *(int*)arg;
    printf("[线程 %d] 开始后台任务...\n", id);
    sleep(2);
    printf("[线程 %d] 后台任务完成！\n", id);
    return NULL;
}

int main() {
    pthread_t tid;
    int task_id = 42;

    pthread_create(&tid, NULL, background_task, &task_id);

    // 立即 detach，之后主线程无法再 pthread_join 这个线程
    pthread_detach(tid);

    printf("主线程：任务交给后台了，我先去干别的~\n");

    // 模拟主线程做其他事
    sleep(1);
    printf("主线程：别的事也干完了~\n");

    // 注意：detach 后的线程，其返回值会被系统自动丢弃
    // 所以不要在 detached 线程里返回栈上的局部变量！

    sleep(3);  // 等待 detached 线程执行完，否则 main 提前结束
    return 0;
}
```

> 什么时候用 `join`，什么时候用 `detach`？
> - 需要获取线程的**计算结果** → `pthread_join`
> - 只是"发出去了就不管了" → `pthread_detach`
> - 不确定？先 `join`，等确认不需要结果了再 detach 也不迟

### 24.1.3 线程终止：`pthread_exit` / `pthread_cancel`

线程的退出方式有三种：

1. **线程函数执行到 `return`**（最优雅）
2. **调用 `pthread_exit(void* retval)`**（显式退出）
3. **被其他线程调用 `pthread_cancel(pthread_t thread)`**（被取消）

```c
#include <stdio.h>
#include <pthread.h>
#include <unistd.h>

void* worker_normal(void* arg) {
    printf("工人A：正常干活，正常下班~\n");
    return NULL;  // 正常退出
}

void* worker_exit(void* arg) {
    printf("工人B：遇到特殊情况，调用 pthread_exit 退出！\n");
    int* result = malloc(sizeof(int));
    *result = 9527;
    pthread_exit(result);  // 显式退出，并携带返回值
}

void* worker_wait_cancel(void* arg) {
    printf("工人C：正在等待被取消...\n");
    // 做一些工作
    for (int i = 0; i < 5; i++) {
        printf("  工作进行中 %d/5...\n", i + 1);
        sleep(1);
    }
    printf("工人C：工作太努力了，取消请求没来得及处理！\n");
    return NULL;
}

int main() {
    pthread_t t1, t2, t3;

    pthread_create(&t1, NULL, worker_normal, NULL);
    pthread_create(&t2, NULL, worker_exit, NULL);
    pthread_create(&t3, NULL, worker_wait_cancel, NULL);

    sleep(2);

    printf("主线程：发送取消请求给工人C！\n");
    pthread_cancel(t3);  // 请求取消线程 t3

    pthread_join(t1, NULL);
    pthread_join(t2, &void* retval);  // 获取显式退出的返回值
    pthread_join(t3, NULL);

    if (retval != NULL) {
        printf("主线程：从工人B那里收到了暗号：%d\n", *(int*)retval);
        free(retval);
    }

    printf("主线程：所有人都处理完毕！\n");
    return 0;
}
```

> 注意：`pthread_cancel` 只是一个**取消请求**，不保证立即生效。线程可以选择在某个"取消点"（如 `sleep`、`read`、`write` 等阻塞调用）才响应取消。关于取消点的细节，后面的 24.3 节会详细讲解。

## 24.2 线程同步

> "一个和尚挑水喝，两个和尚抬水喝，三个和尚没水喝。"——这个寓言讲的就是并发编程中最经典的问题：**共享资源被多人同时访问，结果谁都没用好**。

线程同步，就是解决"多人抢同一资源"的问题。想象一下：
- 抢厕所：得有人看着门，有人排队
- 抢红包：手慢了就没了
- 抢ATM：得锁门，进去一个出一个

接下来，我们逐一介绍各种同步机制。

### 24.2.1 互斥锁（Mutex）：保护共享资源的"看门大爷"

互斥锁（Mutual Exclusion，简称 Mutex）是最基本、最常用的同步工具。它的思想很简单：**一次只能有一个人进去，其他人在外面排队**。

想象你家的厕所——门上有个锁，里面的人出来后会解锁，下一个人才能进去。Mutex 就是这个锁的程序员版本。

```c
#include <stdio.h>
#include <pthread.h>
#include <unistd.h>

// 定义一个互斥锁
pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;

// 共享资源（假设是一个银行账户余额）
int balance = 1000;

// 取款操作
void* withdraw(void* arg) {
    char* name = (char*)arg;

    // 上锁！其他线程想执行下面的代码，必须在这里等待
    pthread_mutex_lock(&mutex);

    printf("[%s] 开始取款，当前余额：%d\n", name, balance);

    if (balance >= 100) {
        // 模拟取款操作需要时间
        usleep(100000);  // 100ms

        balance -= 100;
        printf("[%s] 取款成功！剩余余额：%d\n", name, balance);
    } else {
        printf("[%s] 余额不足，取款失败！\n", name);
    }

    // 解锁！让其他线程可以进来
    pthread_mutex_unlock(&mutex);

    return NULL;
}

int main() {
    pthread_t t1, t2, t3;

    printf("初始余额：%d\n", balance);
    printf("三个人同时来取钱...\n\n");

    // 三个线程同时取款
    pthread_create(&t1, NULL, withdraw, "张三");
    pthread_create(&t2, NULL, withdraw, "李四");
    pthread_create(&t3, NULL, withdraw, "王五");

    pthread_join(t1, NULL);
    pthread_join(t2, NULL);
    pthread_join(t3, NULL);

    printf("\n最终余额：%d（应该剩 700）\n", balance);

    // 销毁互斥锁
    pthread_mutex_destroy(&mutex);

    return 0;
}
```

运行结果（可以看到，余额不会乱套）：

```
初始余额：1000
三个人同时来取钱...

[张三] 开始取款，当前余额：1000
[张三] 取款成功！剩余余额：900
[李四] 开始取款，当前余额：900
[李四] 取款成功！剩余余额：800
[王五] 开始取款，当前余额：800
[王五] 取款成功！剩余余额：700

最终余额：700（应该剩 700）
```

如果没有互斥锁，可能出现这种情况（竞态条件）：

```
[张三] 读取余额 = 1000
[李四] 读取余额 = 1000  // 两个人读到了同样的值！
[张三] 计算 1000 - 100 = 900，写入余额 = 900
[李四] 计算 1000 - 100 = 900，写入余额 = 900  // 把张三的结果覆盖了！
最终余额：900（而不是 700！）—— 银行亏大了！
```

#### 动态初始化与销毁

`PTHREAD_MUTEX_INITIALIZER` 是静态初始化，适用于全局或静态变量。如果是局部变量或需要运行时配置属性，则需要动态初始化：

```c
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>

int main() {
    pthread_mutex_t mutex;

    // 动态初始化（可以指定属性）
    pthread_mutex_init(&mutex, NULL);  // NULL 表示默认属性

    // 使用 mutex...

    pthread_mutex_destroy(&mutex);  // 用完记得销毁
    return 0;
}
```

#### 互斥锁的属性

互斥锁有三种类型（`pthread_mutexattr_t`）：

```c
#include <pthread.h>
#include <stdio.h>

int main() {
    pthread_mutex_t mutex;
    pthread_mutexattr_t attr;

    pthread_mutexattr_init(&attr);

    // 设置类型
    // PTHREAD_MUTEX_NORMAL - 普通锁（不做死锁检测）
    // PTHREAD_MUTEX_ERRORCHECK - 错误检查锁（同一线程重复加锁会报错）
    // PTHREAD_MUTEX_RECURSIVE - 递归锁（同一线程可重复加锁，计数解锁）
    pthread_mutexattr_settype(&attr, PTHREAD_MUTEX_RECURSIVE);

    pthread_mutex_init(&mutex, &attr);

    // 递归锁示例：同一线程可以多次加锁
    pthread_mutex_lock(&mutex);
    printf("第一次加锁\n");
    pthread_mutex_lock(&mutex);
    printf("第二次加锁（递归锁允许）\n");
    pthread_mutex_unlock(&mutex);
    pthread_mutex_unlock(&mutex);

    pthread_mutex_destroy(&mutex);
    pthread_mutexattr_destroy(&attr);

    return 0;
}
```

> **新手警告**：普通锁下，同一线程对已持有的锁再次加锁会**死锁**（后面会讲死锁是什么）。如果不确定，优先使用 `PTHREAD_MUTEX_ERRORCHECK`，它会在调试阶段帮你发现问题。

### 24.2.2 读写锁：读的"宽松"，写的"严格"

想象一个图书馆：
- **看书**（读操作）：可以很多人同时看，互不影响
- **写书**（写操作**：写的时候不能有人看，也不能有人写**

读写锁（Read-Write Lock）就是这个逻辑的程序员实现。

- **读模式加锁**：允许多个线程同时进入读模式（"共享锁"）
- **写模式加锁**：独占访问，其他线程不管是读还是写都得等着（"排他锁"）

```c
#include <stdio.h>
#include <pthread.h>
#include <unistd.h>
#include <string.h>

pthread_rwlock_t rwlock = PTHREAD_RWLOCK_INITIALIZER;

// 共享数据：假设是一个配置信息
char config[256] = "mode=production;debug=false;";

void* reader(void* arg) {
    char* name = (char*)arg;

    pthread_rwlock_rdlock(&rwlock);  // 读锁（共享）
    printf("[读者 %s] 正在读取配置: %s\n", name, config);
    usleep(500000);  // 模拟读取耗时
    printf("[读者 %s] 读取完成\n", name);
    pthread_rwlock_unlock(&rwlock);

    return NULL;
}

void* writer(void* arg) {
    char* name = (char*)arg;

    pthread_rwlock_wrlock(&rwlock);  // 写锁（独占）
    printf("[作者 %s] 正在修改配置...\n", name);
    usleep(500000);  // 模拟写入耗时
    strcpy(config, "mode=development;debug=true;");
    printf("[作者 %s] 修改完成: %s\n", name, config);
    pthread_rwlock_unlock(&rwlock);

    return NULL;
}

int main() {
    pthread_t t[5];

    // 创建多个读者
    pthread_create(&t[0], NULL, reader, "小红");
    pthread_create(&t[1], NULL, reader, "小明");
    pthread_create(&t[2], NULL, writer, "管理员");
    pthread_create(&t[3], NULL, reader, "小芳");
    pthread_create(&t[4], NULL, reader, "小刚");

    for (int i = 0; i < 5; i++) {
        pthread_join(t[i], NULL);
    }

    pthread_rwlock_destroy(&rwlock);
    printf("\n所有人操作完毕，最终配置: %s\n", config);

    return 0;
}
```

运行结果（可以看到读者们可以并行，但写者会独占）：

```
[读者 小红] 正在读取配置: mode=production;debug=false;
[读者 小明] 正在读取配置: mode=production;debug=false;  // 两人同时读！
[作者 管理员] 正在修改配置...                              // 写者来了，读者都要让路
[读者 小芳] 正在读取配置: mode=development;debug=true;  // 写完才能读
[读者 小刚] 正在读取配置: mode=development;debug=true;

所有人操作完毕，最终配置: mode=development;debug=true;
```

> **适用场景**：读写锁适合"读多写少"的场景（如缓存、配置表）。如果读写频率差不多，甚至写更多，互斥锁可能更简单高效。

### 24.2.3 条件变量：线程间的"暗号"

条件变量（Condition Variable）是线程间通信的"暗号本"。它让线程可以**主动等待某个条件满足**才继续执行，而不是傻傻地一直轮询检查。

想象一下点外卖：
- 你（线程）不能每隔 5 秒就打电话问"外卖到了吗"——太耗资源（轮询）
- 你应该把手机号留给外卖小哥，等他打电话通知你（条件变量等待）
- 外卖到了，小哥打电话给你（信号通知）
- 你才下楼取餐（继续执行）

```c
#include <stdio.h>
#include <pthread.h>
#include <unistd.h>

pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t cond = PTHREAD_COND_INITIALIZER;

// 共享状态
int ready = 0;  // 0 = 数据未就绪，1 = 数据就绪
int data = 0;

// 生产者：制造数据
void* producer(void* arg) {
    printf("[生产者] 开始生产数据...\n");
    sleep(2);  // 模拟耗时操作

    pthread_mutex_lock(&mutex);
    data = 42;  // 制造了重要数据
    ready = 1;   // 标记数据就绪
    printf("[生产者] 数据准备好了！值 = %d，发送信号！\n", data);
    pthread_mutex_unlock(&mutex);

    // 通知等待中的消费者
    pthread_cond_signal(&cond);  // 唤醒至少一个等待的线程

    return NULL;
}

// 消费者：等待并消费数据
void* consumer(void* arg) {
    char* name = (char*)arg;

    pthread_mutex_lock(&mutex);

    // 关键！必须用 while 循环，不能用 if！
    // （关于为什么，后面 24.7.5 会详细解释"虚假唤醒"）
    while (ready == 0) {
        printf("[消费者 %s] 数据还没好，进入等待...\n", name);
        pthread_cond_wait(&cond, &mutex);  // 解锁互斥量并等待信号
        printf("[消费者 %s] 被唤醒了！\n", name);
    }

    printf("[消费者 %s] 收到数据！value = %d\n", name, data);

    pthread_mutex_unlock(&mutex);
    return NULL;
}

int main() {
    pthread_t prod, cons1, cons2;

    // 先启动消费者（它会等待）
    pthread_create(&cons1, NULL, consumer, "小明");
    pthread_create(&cons2, NULL, consumer, "小红");
    sleep(1);  // 确保消费者先进入等待
    pthread_create(&prod, NULL, producer, NULL);

    pthread_join(prod, NULL);
    pthread_join(cons1, NULL);
    pthread_join(cons2, NULL);

    pthread_mutex_destroy(&mutex);
    pthread_cond_destroy(&cond);

    printf("\n任务完成！\n");
    return 0;
}
```

运行结果：

```
[消费者 小明] 数据还没好，进入等待...
[消费者 小红] 数据还没好，进入等待...
[生产者] 开始生产数据...
[生产者] 数据准备好了！值 = 42，发送信号！
[消费者 小明] 被唤醒了！
[消费者 小明] 收到数据！value = 42
[消费者 小红] 被唤醒了！
[消费者 小红] 收到数据！value = 42

任务完成！
```

#### `pthread_cond_broadcast`：广播唤醒

如果有一个"全局通知"，需要唤醒所有等待者（比如"关门了，所有人都可以下班了"），用 `pthread_cond_broadcast`：

```c
#include <stdio.h>
#include <pthread.h>
#include <unistd.h>

pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t cond = PTHREAD_COND_INITIALIZER;

int game_over = 0;

void* player(void* arg) {
    char* name = (char*)arg;

    pthread_mutex_lock(&mutex);
    while (game_over == 0) {
        printf("[玩家 %s] 等待游戏开始...\n", name);
        pthread_cond_wait(&cond, &mutex);
    }
    printf("[玩家 %s] 收到开始信号，开始游戏！\n", name);
    pthread_mutex_unlock(&mutex);

    return NULL;
}

void* host(void* arg) {
    sleep(2);
    pthread_mutex_lock(&mutex);
    game_over = 1;
    printf("[主持人] 游戏开始！广播通知所有玩家！\n");
    pthread_cond_broadcast(&cond);  // 唤醒所有等待的线程
    pthread_mutex_unlock(&mutex);
    return NULL;
}

int main() {
    pthread_t t[4];

    for (int i = 0; i < 3; i++) {
        char name[20];
        sprintf(name, "玩家%d", i + 1);
        pthread_create(&t[i], NULL, player, name);
    }
    pthread_create(&t[3], NULL, host, NULL);

    for (int i = 0; i < 4; i++) {
        pthread_join(t[i], NULL);
    }

    pthread_mutex_destroy(&mutex);
    pthread_cond_destroy(&cond);

    return 0;
}
```

运行结果：

```
[玩家1] 等待游戏开始...
[玩家2] 等待游戏开始...
[玩家3] 等待游戏开始...
[主持人] 游戏开始！广播通知所有玩家！
[玩家2] 收到开始信号，开始游戏！
[玩家1] 收到开始信号，开始游戏！
[玩家3] 收到开始信号，开始游戏！
```

### 24.2.4 信号量（线程同步）：计数器式的"通行证"

信号量（Semaphore）是一种更通用的同步原语。它的核心是一个**计数器**，初始值为 N：
- 每当一个线程"获取"信号量，计数器减 1
- 如果计数器为 0，则线程阻塞等待
- 每当一个线程"释放"信号量，计数器加 1，如果有等待者则唤醒一个

你可以把信号量想象成**停车场的闸机**——一共 N 个车位，每进来一辆车计数减 1，满了就拦着不让进；每出去一辆计数加 1，计数值 > 0 就抬杆放一辆。

```c
#include <stdio.h>
#include <pthread.h>
#include <semaphore.h>
#include <unistd.h>

// 3 个座位的小组讨论室
sem_t room_sem;

// 用于互斥访问输出（避免打印混乱）
pthread_mutex_t print_mutex = PTHREAD_MUTEX_INITIALIZER;

void* person(void* arg) {
    char* name = (char*)arg;

    // 等座位（信号量值 - 1，如果为正则进入，否则等待）
    sem_wait(&room_sem);

    pthread_mutex_lock(&print_mutex);
    printf("[%s] 进入了讨论室（座位 -1）\n", name);
    pthread_mutex_unlock(&print_mutex);

    // 在讨论室里聊天
    sleep(2);

    pthread_mutex_lock(&print_mutex);
    printf("[%s] 讨论完毕，离开了讨论室（座位 +1）\n", name);
    pthread_mutex_unlock(&print_mutex);

    // 离开，释放座位（信号量值 + 1）
    sem_post(&room_sem);

    return NULL;
}

int main() {
    // 初始化信号量，初始值 = 3（即最多同时 3 人在讨论室）
    sem_init(&room_sem, 0, 3);

    pthread_t t[6];
    char names[6][20] = {"Alice", "Bob", "Charlie", "David", "Eve", "Frank"};

    // 6 个人抢 3 个座位
    for (int i = 0; i < 6; i++) {
        pthread_create(&t[i], NULL, person, names[i]);
    }

    for (int i = 0; i < 6; i++) {
        pthread_join(t[i], NULL);
    }

    sem_destroy(&room_sem);
    pthread_mutex_destroy(&print_mutex);

    printf("\n所有人都讨论完毕！\n");

    return 0;
}
```

运行结果（可以看到最多 3 人同时在讨论室）：

```
[Alice] 进入了讨论室（座位 -1）
[Bob] 进入了讨论室（座位 -1）
[Charlie] 进入了讨论室（座位 -1）
[David] 等待座位...
[Eve] 等待座位...
[Frank] 等待座位...
[Alice] 讨论完毕，离开了讨论室（座位 +1）
[David] 进入了讨论室（座位 -1）
[Bob] 讨论完毕，离开了讨论室（座位 +1）
[Eve] 进入了讨论室（座位 -1）
[Charlie] 讨论完毕，离开了讨论室（座位 +1）
[Frank] 进入了讨论室（座位 -1）
[David] 讨论完毕，离开了讨论室（座位 +1）
[Eve] 讨论完毕，离开了讨论室（座位 +1）
[Frank] 讨论完毕，离开了讨论室（座位 +1）

所有人都讨论完毕！
```

> **信号量 vs 互斥锁**：互斥锁只有 0/1 两种状态（"锁着"或"开着"），相当于信号量初始值为 1 的特殊情况。但信号量更灵活，可以用于控制 N 个资源的并发访问（比如连接池、缓冲区槽位等）。

### ⚠️ 24.2.5 死锁的四个必要条件（Coffman 条件）与预防策略

**死锁（Deadlock）** 是并发编程中最让人头疼的问题之一。想象一下：

> 两个小朋友抢玩具，A 拿到了机器人想要飞机，B 拿到了飞机想要机器人，谁都不肯放手，于是俩人都卡在那里哭。

这就是死锁——两个或多个线程互相等待对方持有的资源，导致大家都没法继续执行。

#### Coffman 条件（死锁的四个必要条件）

死锁发生必须同时满足以下四个条件（Coffman 出品，必属精品）：

1. **互斥条件（Mutual Exclusion）**：资源一次只能被一个线程使用
2. **占有并等待（Hold and Wait）**：线程持有资源的同时，还在等待其他资源
3. **不可抢占（No Preemption）**：资源不能被强制夺走，只能由线程主动释放
4. **循环等待（Circular Wait）**：形成循环链：A 等 B，B 等 C，C 等 A

只要破坏其中**任意一个**条件，死锁就不会发生！

#### 预防策略

| 策略 | 破坏哪个条件 | 实现方法 |
|------|------------|---------|
| **一次性申请所有资源** | 破坏"占有并等待" | 在开始前把所有需要的锁都 lock，结束后一次性 unlock |
| **资源排序** | 破坏"循环等待" | 规定锁的获取顺序，所有线程必须按固定顺序获取锁 |
| **设置超时** | 引入抢占可能 | 用 `pthread_mutex_timedlock` 替代 `pthread_mutex_lock` |
| **死锁检测** | 事后发现 | 用有向图检测循环等待，强制释放/回滚 |

**资源排序法**是最常用且最有效的预防手段：

```c
// 坏例子：容易死锁
void* bad_order(void* arg) {
    // 线程1 可能先锁 A 再锁 B，线程2 可能先锁 B 再锁 A
    if (id == 1) {
        pthread_mutex_lock(&mutex_A);
        pthread_mutex_lock(&mutex_B);  // 如果线程2已经锁了B，这里就卡住了
    } else {
        pthread_mutex_lock(&mutex_B);
        pthread_mutex_lock(&mutex_A);  // 如果线程1已经锁了A，这里就卡住了
    }
    // ...
}

// 好例子：统一顺序，按地址从小到大排序
void* good_order(void* arg) {
    // 确保 mutex_A 和 mutex_B 的地址始终按固定顺序加锁
    pthread_mutex_t* first = (mutex_A < mutex_B) ? &mutex_A : &mutex_B;
    pthread_mutex_t* second = (mutex_A < mutex_B) ? &mutex_B : &mutex_A;

    pthread_mutex_lock(first);
    pthread_mutex_lock(second);
    // ...
}
```

```c
#include <stdio.h>
#include <pthread.h>
#include <unistd.h>
#include <stdlib.h>

pthread_mutex_t mutex_A = PTHREAD_MUTEX_INITIALIZER;
pthread_mutex_t mutex_B = PTHREAD_MUTEX_INITIALIZER;

int id;

// 安全的加锁顺序：按地址排序
void lock_in_order(pthread_mutex_t* a, pthread_mutex_t* b) {
    if (a < b) {
        pthread_mutex_lock(a);
        pthread_mutex_lock(b);
    } else {
        pthread_mutex_lock(b);
        pthread_mutex_lock(a);
    }
}

void unlock_both() {
    pthread_mutex_unlock(&mutex_A);
    pthread_mutex_unlock(&mutex_B);
}

void* thread_func(void* arg) {
    int tid = *(int*)arg;
    printf("[线程 %d] 准备获取两个锁...\n", tid);

    lock_in_order(&mutex_A, &mutex_B);

    printf("[线程 %d] 两个锁都到手了！开始工作...\n", tid);
    sleep(1);

    unlock_both();
    printf("[线程 %d] 完成任务，释放锁！\n", tid);

    return NULL;
}

int main() {
    pthread_t t1, t2;

    int id1 = 1, id2 = 2;
    pthread_create(&t1, NULL, thread_func, &id1);
    pthread_create(&t2, NULL, thread_func, &id2);

    pthread_join(t1, NULL);
    pthread_join(t2, NULL);

    pthread_mutex_destroy(&mutex_A);
    pthread_mutex_destroy(&mutex_B);

    printf("安全完成，无死锁！\n");
    return 0;
}
```

## 24.3 线程取消

### 24.3.1 `pthread_cancel`

`pthread_cancel` 用来请求取消另一个线程。但注意，这只是**发出取消请求**，线程是否响应、什么时候响应，取决于线程的取消状态和取消类型。

```c
#include <stdio.h>
#include <pthread.h>
#include <unistd.h>

void* long_task(void* arg) {
    printf("[线程] 开始执行长时间任务...\n");

    // 模拟长时间工作，每秒报告一次
    for (int i = 0; i < 10; i++) {
        printf("[线程] 工作中... %d/10\n", i + 1);
        sleep(1);
    }

    printf("[线程] 任务完成！\n");
    return NULL;
}

int main() {
    pthread_t tid;
    pthread_create(&tid, NULL, long_task, NULL);

    sleep(3);  // 等 3 秒
    printf("[主线程] 这个任务不要了，取消！\n");
    pthread_cancel(tid);

    void* retval;
    pthread_join(tid, &retval);

    if (retval == PTHREAD_CANCELED) {
        printf("[主线程] 线程已被成功取消！\n");
    } else {
        printf("[主线程] 线程正常结束\n");
    }

    return 0;
}
```

### 24.3.2 取消点（Cancellation Points）

线程不会在任意时刻响应取消请求。POSIX 定义了一系列**取消点**（cancellation points），在这些函数调用中，线程会检查并处理待处理的取消请求。

常见的取消点包括：

| 函数 | 说明 |
|------|------|
| `sleep`, `nanosleep` | 睡眠 |
| `read`, `write` | 读写（某些情况下） |
| `wait`, `pthread_cond_wait` | 条件变量等待 |
| `sem_wait`, `pthread_join` | 等待 |
| `open`, `close` | 文件操作 |

```c
#include <stdio.h>
#include <pthread.h>
#include <unistd.h>

void* cancellable_task(void* arg) {
    printf("[线程] 开始（这是个取消点之后的日志）\n");

    // sleep 是取消点，会响应取消请求
    printf("[线程] 进入 sleep...\n");
    sleep(10);  // 如果在这期间收到取消请求，会被唤醒并取消

    printf("[线程] sleep 结束（不会执行到这里如果被取消了）\n");
    return NULL;
}

int main() {
    pthread_t tid;
    pthread_create(&tid, NULL, cancellable_task, NULL);

    sleep(1);
    printf("[主线程] 发送取消请求！\n");
    pthread_cancel(tid);

    pthread_join(tid, NULL);
    printf("[主线程] 线程已取消。\n");

    return 0;
}
```

> **新手注意**：如果你的线程函数里没有任何取消点（比如只有计算逻辑），那么 `pthread_cancel` 可能永远无法生效。可以用 `pthread_testcancel()` 手动插入取消点：

```c
void* my_task(void* arg) {
    while (1) {
        // 做一小块工作
        do_some_work();

        // 手动检查取消请求
        pthread_testcancel();
    }
}
```

#### 取消状态与类型

线程可以设置自己的取消行为：

```c
// 设置取消状态：启用/禁用取消
pthread_setcancelstate(PTHREAD_CANCEL_ENABLE, NULL);   // 允许取消（默认）
pthread_setcancelstate(PTHREAD_CANCEL_DISABLE, NULL);  // 禁用取消

// 设置取消类型：异步取消/延迟取消
pthread_setcanceltype(PTHREAD_CANCEL_DEFERRED, NULL);   // 延迟取消，只在取消点响应（默认）
pthread_setcanceltype(PTHREAD_CANCEL_ASYNCHRONOUS, NULL); // 异步取消，随时可能响应（危险！）
```

> **异步取消非常危险**，因为线程可能在任意指令处被强制终止，如果线程正在操作某些资源（如持有锁、写文件），会导致资源泄漏或损坏。除非你非常清楚自己在做什么，否则不要使用。

### 24.3.3 清理处理函数：`pthread_cleanup_push` / `pthread_cleanup_pop`

当线程被取消时，它可能正持有着锁、分配着内存、或者操作着某个文件。如果不处理这些"烂摊子"，就会造成资源泄漏或不一致状态。

清理处理函数（Cleanup Handler）就是用来解决这个问题——在线程退出前，自动执行一段"收尾代码"。

```c
#include <stdio.h>
#include <pthread.h>
#include <stdlib.h>

pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;
int shared_data = 0;

void cleanup_mutex(void* arg) {
    printf("[清理] 解锁互斥锁！\n");
    pthread_mutex_unlock(&mutex);
}

void cleanup_free(void* arg) {
    printf("[清理] 释放内存！\n");
    free(arg);
}

void* worker(void* arg) {
    pthread_cleanup_push(cleanup_mutex, NULL);  // 注册清理函数
    pthread_cleanup_push(cleanup_free, malloc(sizeof(int)));  // 注册另一个清理

    pthread_mutex_lock(&mutex);
    shared_data = *(int*)arg;
    printf("[线程] 开始处理数据: %d\n", shared_data);

    // 模拟可取消的操作
    sleep(5);  // 这是取消点

    pthread_mutex_unlock(&mutex);

    // pop(0) 表示执行清理函数
    // pop(1) 表示不执行清理函数（跳过），仅移除
    pthread_cleanup_pop(0);  // 不执行，因为没到这行就可能已被取消
    pthread_cleanup_pop(0);

    return NULL;
}

int main() {
    pthread_t tid;
    int data = 123;

    pthread_create(&tid, NULL, worker, &data);

    sleep(1);
    printf("[主线程] 取消线程！\n");
    pthread_cancel(tid);

    pthread_join(tid, NULL);
    printf("[主线程] 线程已取消。\n");

    pthread_mutex_destroy(&mutex);
    return 0;
}
```

运行结果（可以看到即使线程被取消，互斥锁也被正确解锁了）：

```
[线程] 开始处理数据: 123
[主线程] 取消线程！
[清理] 解锁互斥锁！    // 清理函数被执行了！
[清理] 释放内存！     // 另一个清理函数也被执行了！
[主线程] 线程已取消。
```

> `pthread_cleanup_pop` 的参数：`0` = 执行清理函数后移除；`1` = 仅移除，不执行。如果 `pthread_cleanup_pop` 在 `return` 或 `pthread_exit` 之前被调用且参数为 `1`，则对应的清理函数不会被执行——这模拟了"成功路径不需要清理"的情况。

## 24.4 线程局部存储（TLS）

### 24.4.1 POSIX TLS：`pthread_key_create` / `pthread_getspecific` / `pthread_setspecific`

线程局部存储（Thread-Local Storage，简称 TLS）是一种让每个线程都有自己独立的数据副本的机制。

想象一下：你是公司的员工（线程），公司有一本公共通讯录（全局数据），但每个员工还有自己的私人笔记本（线程局部存储）。私人笔记本里的内容只有你自己能看到，不会被其他员工看到或修改。

```c
#include <stdio.h>
#include <pthread.h>
#include <string.h>

// 创建线程局部存储的键
pthread_key_t session_key;
pthread_key_t name_key;

// 初始化函数（只执行一次）
void init_once(void) {
    printf("TLS 键创建成功！\n");
}

// 线程清理函数（线程退出时自动调用）
void cleanup_session(void* value) {
    printf("[清理] 释放线程 %s 的 session: %s\n",
           (char*)pthread_getspecific(name_key), (char*)value);
    free(value);
}

void* session_worker(void* arg) {
    char* thread_name = (char*)arg;

    // 给这个线程设置名字
    pthread_setspecific(name_key, thread_name);

    // 为当前线程分配一个"会话ID"
    char session_id[64];
    snprintf(session_id, sizeof(session_id), "session-%s-%lu",
             thread_name, pthread_self() % 10000);

    char* my_session = strdup(session_id);
    pthread_setspecific(session_key, my_session);

    printf("[线程 %s] 我的 session: %s\n", thread_name, (char*)pthread_getspecific(session_key));

    // 模拟使用 session 做一些事
    sleep(1);

    printf("[线程 %s] session 仍在使用: %s\n", thread_name, (char*)pthread_getspecific(session_key));

    // 注意：返回前不要 free，因为我们已经注册了 cleanup_session
    // pthread_cleanup_push(cleanup_session, my_session);  // 注册了但还没到 pop
    // pthread_cleanup_pop(1);  // 这会 free

    return NULL;
}

int main() {
    // 创建 TLS 键
    // 参数2是析构函数，当线程退出时如果值为非NULL，会自动调用此函数
    pthread_key_create(&session_key, cleanup_session);
    pthread_key_create(&name_key, NULL);  // 这个键不需要析构函数

    pthread_t t1, t2, t3;

    pthread_create(&t1, NULL, session_worker, "Alice");
    pthread_create(&t2, NULL, session_worker, "Bob");
    pthread_create(&t3, NULL, session_worker, "Charlie");

    pthread_join(t1, NULL);
    pthread_join(t2, NULL);
    pthread_join(t3, NULL);

    pthread_key_delete(session_key);
    pthread_key_delete(name_key);

    printf("\n主线程：所有 TLS 数据都是独立的，互不干扰！\n");

    return 0;
}
```

运行结果（注意每个线程的 session_id 都是独立的）：

```
TLS 键创建成功！
[线程 Alice] 我的 session: session-Alice-1234
[线程 Bob] 我的 session: session-Bob-5678
[线程 Charlie] 我的 session: session-Charlie-9012
[线程 Alice] session 仍在使用: session-Alice-1234
[线程 Bob] session 仍在使用: session-Bob-5678
[线程 Charlie] session 仍在使用: session-Charlie-9012
[清理] 释放线程 Alice 的 session: session-Alice-1234
[清理] 释放线程 Bob 的 session: session-Bob-5678
[清理] 释放线程 Charlie 的 session: session-Charlie-9012

主线程：所有 TLS 数据都是独立的，互不干扰！
```

### 24.4.2 C11 `_Thread_local` / `thread_local`（C23 起关键字）

C11 引入了更简洁的线程局部存储关键字：`_Thread_local`（或等价的 `thread_local`，C23 起作为关键字）。这是编译器层面的支持，比 `pthread_key` 方便得多！

```c
#include <stdio.h>
#include <threads.h>
#include <pthread.h>

// 方式1：C11 关键字（推荐）
_Thread_local int thread_id_counter = 0;
_Thread_local char thread_name[64];

// 方式2：等价的写法
thread_local int alternative_counter = 0;

// 使用 POSIX pthread 版本（为了跨平台兼容性）
void* posix_worker(void* arg) {
    _Thread_local int local_counter = 0;  // 每个线程有独立的 local_counter

    _Thread_local char name[64];
    snprintf(name, sizeof(name), "Thread-%lu", pthread_self() % 1000);

    for (int i = 0; i < 3; i++) {
        local_counter++;
        printf("[%s] local_counter = %d\n", name, local_counter);
    }

    return NULL;
}

// 使用 C11 threads.h 版本（功能更完整，但 glibc 支持不完全）
int c11_worker(void* arg) {
    thrd_current();  // 获取当前线程 ID

    return thrd_success;
}

int main() {
    pthread_t t1, t2, t3;

    printf("=== POSIX 线程测试 ===\n");
    pthread_create(&t1, NULL, posix_worker, NULL);
    pthread_create(&t2, NULL, posix_worker, NULL);
    pthread_create(&t3, NULL, posix_worker, NULL);

    pthread_join(t1, NULL);
    pthread_join(t2, NULL);
    pthread_join(t3, NULL);

    printf("\n每个线程的 local_counter 都是独立的（都是 3），互不干扰！\n");

    return 0;
}
```

> **编译器关键字 vs POSIX API**：`_Thread_local` / `thread_local` 是编译器直接支持的语法，用起来简单，而且静态初始化时自动为零初始化。但它不能绑定析构函数（不像 `pthread_key_create` 的第二个参数可以指定清理函数）。对于需要复杂清理逻辑的场景，仍然需要用 `pthread_key`。

## 24.5 C11 `<threads.h>`

> ⚠️ **重要警告**：C11 `<threads.h>` 的实现状况参差不齐。**glibc（大多数 Linux 发行版）只实现了部分**，很多函数实际上是"空壳"或未实现。生产环境强烈建议使用 POSIX `<pthread.h>`。本节作为知识储备，遇到实际问题请回归 pthread。

C11 引入了标准化的线程支持库 `<threads.h>`，提供了一套与平台无关的线程 API。设计目标是"一次编写，到处运行"（write once, run anywhere），但现实是骨感的。

### 24.5.1 线程管理：`thrd_create` / `thrd_detach` / `thrd_current` / `thrd_sleep`

```c
#include <stdio.h>
#include <threads.h>
#include <time.h>

// C11 线程函数签名：int (*)(void*)，返回 thrd_success/error/busy
int worker(void* arg) {
    char* name = (char*)arg;
    printf("[线程 %s] 开始工作！\n", name);

    for (int i = 0; i < 3; i++) {
        printf("[线程 %s] 工作中 %d...\n", name, i + 1);
        thrd_sleep(&(struct timespec){.tv_sec = 1}, NULL);  // 睡眠 1 秒
    }

    printf("[线程 %s] 工作完成！\n", name);
    return thrd_success;  // 返回成功状态
}

int main() {
    thrd_t t1, t2;

    printf("=== C11 threads.h 测试 ===\n");

    // 创建线程
    if (thrd_create(&t1, worker, "Alice") != thrd_success) {
        fprintf(stderr, "线程1创建失败！\n");
        return 1;
    }

    if (thrd_create(&t2, worker, "Bob") != thrd_success) {
        fprintf(stderr, "线程2创建失败！\n");
        return 1;
    }

    // 等待线程结束
    thrd_join(t1, NULL);
    thrd_join(t2, NULL);

    // 获取当前线程 ID
    thrd_t current = thrd_current();
    printf("当前线程 ID: %ld\n", (long)current);

    // 分离线程（如果不需要等待其结束）
    // 注意：thrd_detach 后不能再 thrd_join
    // thrd_detach(tid);

    printf("主线程：任务完成！\n");

    return 0;
}
```

> 注意：`thrd_detach` 在 C11 中是存在的，但很多系统尚未实现。`thrd_sleep` 的第二个参数如果传 `NULL`，表示不需要获取剩余睡眠时间。

### 24.5.2 互斥锁：`mtx_init`（`mtx_plain`/`mtx_recursive`/`mtx_timed`）/ `mtx_lock` / `mtx_trylock`

```c
#include <stdio.h>
#include <threads.h>

mtx_t mutex;
mtx_t recursive_mutex;

int counter = 0;

// 线程函数
int incrementer(void* arg) {
    char* name = (char*)arg;

    for (int i = 0; i < 5; i++) {
        // mtx_lock: 阻塞加锁
        mtx_lock(&mutex);

        int old = counter;
        counter++;
        printf("[%s] counter: %d -> %d\n", name, old, counter);

        mtx_unlock(&mutex);
    }

    return thrd_success;
}

// 尝试加锁（非阻塞）
int try_incrementer(void* arg) {
    char* name = (char*)arg;

    for (int i = 0; i < 5; i++) {
        if (mtx_trylock(&mutex) == thrd_busy) {
            printf("[%s] 锁被占用，跳过...\n", name);
        } else {
            int old = counter;
            counter++;
            printf("[%s] 获得锁，counter: %d -> %d\n", name, old, counter);
            mtx_unlock(&mutex);
        }
    }

    return thrd_success;
}

int main() {
    // 初始化普通互斥锁
    if (mtx_init(&mutex, mtx_plain) != thrd_success) {
        fprintf(stderr, "互斥锁初始化失败！\n");
        return 1;
    }

    // 初始化递归互斥锁（同一线程可多次加锁）
    if (mtx_init(&recursive_mutex, mtx_recursive) != thrd_success) {
        fprintf(stderr, "递归互斥锁初始化失败！\n");
        return 1;
    }

    thrd_t t1, t2;
    thrd_create(&t1, incrementer, "Thread-1");
    thrd_create(&t2, incrementer, "Thread-2");

    thrd_join(t1, NULL);
    thrd_join(t2, NULL);

    printf("\n最终 counter = %d（应该是 10）\n", counter);

    mtx_destroy(&mutex);
    mtx_destroy(&recursive_mutex);

    return 0;
}
```

互斥锁类型：
- `mtx_plain`：最基本的互斥锁
- `mtx_recursive`：递归锁，同一线程可重复加锁，加锁次数需要匹配解锁次数
- `mtx_timed`：支持超时（超时后自动解锁，返回 `thrd_timedout`）

### 24.5.3 条件变量：`cnd_init` / `cnd_wait` / `cnd_signal` / `cnd_broadcast`

C11 条件变量的用法与 POSIX `pthread_cond_*` 类似，但接口略有不同：

```c
#include <stdio.h>
#include <threads.h>
#include <stdbool.h>

mtx_t mutex;
cnd_t cond;

bool data_ready = false;
int shared_value = 0;

int producer(void* arg) {
    (void)arg;

    thrd_sleep(&(struct timespec){.tv_sec = 1}, NULL);  // 模拟生产

    mtx_lock(&mutex);
    shared_value = 42;
    data_ready = true;
    printf("[生产者] 数据准备好了！value = %d，发送信号！\n", shared_value);
    mtx_unlock(&mutex);

    cnd_signal(&cond);  // 唤醒一个等待者
    return thrd_success;
}

int consumer(void* arg) {
    char* name = (char*)arg;

    mtx_lock(&mutex);

    // 必须用 while，不能用 if！（防止虚假唤醒）
    while (!data_ready) {
        printf("[消费者 %s] 等待中...\n", name);
        cnd_wait(&cond, &mutex);  // 等待信号
    }

    printf("[消费者 %s] 收到数据！value = %d\n", name, shared_value);
    mtx_unlock(&mutex);

    return thrd_success;
}

int main() {
    mtx_init(&mutex, mtx_plain);
    cnd_init(&cond);

    thrd_t prod, cons;
    thrd_create(&cons, consumer, "小明");
    thrd_create(&prod, producer, NULL);

    thrd_join(prod, NULL);
    thrd_join(cons, NULL);

    mtx_destroy(&mutex);
    cnd_destroy(&cond);

    printf("完成！\n");
    return 0;
}
```

### 24.5.4 一次性初始化：`call_once`

`call_once` 保证某个初始化函数只被调用一次，即使多个线程同时调用。这在单例模式、延迟初始化等场景非常有用：

```c
#include <stdio.h>
#include <threads.h>

once_flag init_flag = ONCE_FLAG_INIT;

void expensive_init(void) {
    printf("[初始化] 这是一个昂贵的初始化操作，只执行一次！\n");
    // 假设这里有耗时的资源分配操作
}

int worker(void* arg) {
    char* name = (char*)arg;
    printf("[线程 %s] 准备初始化...\n", name);
    call_once(&init_flag, expensive_init);  // 保证只执行一次
    printf("[线程 %s] 初始化完成，继续工作...\n", name);
    return thrd_success;
}

int main() {
    thrd_t t1, t2, t3;

    thrd_create(&t1, worker, "Alice");
    thrd_create(&t2, worker, "Bob");
    thrd_create(&t3, worker, "Charlie");

    thrd_join(t1, NULL);
    thrd_join(t2, NULL);
    thrd_join(t3, NULL);

    printf("\n只执行了一次 expensive_init！\n");

    return 0;
}
```

运行结果：

```
[线程 Alice] 准备初始化...
[线程 Bob] 准备初始化...
[线程 Charlie] 准备初始化...
[初始化] 这是一个昂贵的初始化操作，只执行一次！
[线程 Alice] 初始化完成，继续工作...
[线程 Bob] 初始化完成，继续工作...
[线程 Charlie] 初始化完成，继续工作...

只执行了一次 expensive_init！
```

## 24.6 原子操作（C11 `<stdatomic.h>`）

### 24.6.1 `_Atomic` 类型限定符

原子操作（Atomic Operations）是并发编程的"神器"——它保证某些操作是不可分割的，要么全部完成，要么全部不完成，不会有"一半"的状态。

```c
#include <stdio.h>
#include <stdatomic.h>
#include <pthread.h>

// 使用 _Atomic 关键字声明原子变量
_Atomic int counter = 0;
_Atomic long long big_counter = 0;

// 或者用 typedef 的原子类型（更直观）
atomic_int posix_atomic_counter = 0;

void* increment_worker(void* arg) {
    int id = *(int*)arg;

    for (int i = 0; i < 100000; i++) {
        // 原子自增：读取、+1、写入 三步合为一，不可分割
        atomic_fetch_add_explicit(&counter, 1, memory_order_relaxed);
        atomic_fetch_add_explicit(&big_counter, 1, memory_order_relaxed);
    }

    printf("[线程 %d] 完成！\n", id);
    return NULL;
}

int main() {
    printf("=== 原子操作测试 ===\n");
    printf("初始 counter = %d\n", atomic_load(&counter));

    pthread_t t[4];
    int ids[] = {1, 2, 3, 4};

    for (int i = 0; i < 4; i++) {
        pthread_create(&t[i], NULL, increment_worker, &ids[i]);
    }

    for (int i = 0; i < 4; i++) {
        pthread_join(t[i], NULL);
    }

    printf("\n最终 counter = %d（期望 400000）\n", atomic_load(&counter));
    printf("最终 big_counter = %lld（期望 400000）\n", atomic_load(&big_counter));

    // 验证是否正确
    if (atomic_load(&counter) == 400000) {
        printf("\n✓ 原子操作完美无竞态！\n");
    } else {
        printf("\n✗ 出错了！有竞态条件！\n");
    }

    return 0;
}
```

> 如果不用原子操作，四个线程各加 10 万次，最终结果很可能**不是 40 万**（有丢失的加法）。用了原子操作，结果必然精确无误。

### 24.6.2 5 种内存顺序语义

内存顺序（Memory Order）是一个深入的话题，涉及处理器架构和编译器优化。C11 定义了 5 种内存顺序：

| 顺序 | 说明 | 适用场景 |
|------|------|---------|
| `memory_order_relaxed` | 最松散，只保证原子性，不保证操作顺序 | 计数器、标志位等独立操作 |
| `memory_order_consume` | 依赖于此加载（dependent load），谨慎使用 | 高性能场景，慎用 |
| `memory_order_acquire` | 获取：之后的读写不能重排到此操作之前 | 读端，需要看到写端的数据 |
| `memory_order_release` | 释放：之前的读写不能重排到此操作之后 | 写端，需要让其他线程看到 |
| `memory_order_seq_cst` | 顺序一致（默认）：最强保证，性能最低 | 需要严格顺序的场景 |

> 关于内存顺序的详细讲解，请参考 **第 4C 章**（高级主题：内存模型与内存顺序）。

### 24.6.3 `atomic_load` / `atomic_store` / `atomic_fetch_add` 等函数族

完整的原子操作函数家族：

```c
#include <stdio.h>
#include <stdatomic.h>
#include <pthread.h>

atomic_int shared_flag = 0;
atomic_int data[10];

void* writer(void* arg) {
    (void)arg;

    // 原子写入
    atomic_store(&shared_flag, 1);

    atomic_store(&data[0], 100);
    atomic_store(&data[1], 200);
    atomic_store(&data[2], 300);

    printf("[写入者] 写入完成：flag=1, data={100,200,300}\n");
    return NULL;
}

void* reader(void* arg) {
    (void)arg;

    // 等待 flag 变为 1
    while (atomic_load(&shared_flag) == 0) {
        // busy wait（忙等待），实际应用中应配合条件变量或睡眠
    }

    // 读取数据
    printf("[读取者] 读取数据：flag=%d, data={%d,%d,%d}\n",
           atomic_load(&shared_flag),
           atomic_load(&data[0]),
           atomic_load(&data[1]),
           atomic_load(&data[2]));

    return NULL;
}

// 各种原子操作示例
void atomic_examples() {
    atomic_int value = 0;

    // 原子交换
    int old = atomic_exchange(&value, 42);
    printf("exchange: old=%d, value=%d\n", old, atomic_load(&value));

    // 原子比较交换（CAS - Compare-And-Swap）
    // 如果 value == 10，则设为 20；否则不变。返回是否成功。
    int expected = 42;
    int success = atomic_compare_exchange_strong(&value, &expected, 20);
    printf("CAS: expected was %d, success=%d, value=%d\n", expected, success, atomic_load(&value));

    // 原子加减
    atomic_fetch_add(&value, 5);   // value += 5
    atomic_fetch_sub(&value, 3);   // value -= 3
    atomic_fetch_and(&value, 0xF); // value &= 0xF
    atomic_fetch_or(&value, 0x10); // value |= 0x10

    printf("after ops: value=%d\n", atomic_load(&value));
}

int main() {
    pthread_t r, w;

    pthread_create(&r, NULL, reader, NULL);
    sleep(1);  // 确保 reader 先开始等待
    pthread_create(&w, NULL, writer, NULL);

    pthread_join(w, NULL);
    pthread_join(r, NULL);

    printf("\n--- 原子操作函数示例 ---\n");
    atomic_examples();

    return 0;
}
```

运行结果：

```
[读取者] 读取数据：flag=1, data={100,200,300}
[写入者] 写入完成：flag=1, data={100,200,300}

--- 原子操作函数示例 ---
exchange: old=0, value=42
CAS: expected was 42, success=1, value=20
after ops: value=50
```

## 24.7 常见并发问题

> 并发编程是"甜蜜的陷阱"——写起来简单，看起来也没问题，但问题总在不经意间跳出来咬你一口。本节带你认识这些"坑"，让你下次遇到它们时能一眼认出并绕过去。

### 24.7.1 竞态条件（Race Condition）

**竞态条件**是指多个线程对共享数据的访问顺序不确定，最终结果依赖于线程执行的时序。

想象双十一抢红包：

```
时间线：
T1: 用户A读取余额 = 100
T2: 用户B读取余额 = 100  // 还没来得及减！
T3: 用户A抢到红包，余额 = 100 - 50 = 50，写入
T4: 用户B抢到红包，余额 = 100 - 50 = 50，写入  // 把A的结果覆盖了！
结果：两个人都抢了 50，但余额只扣了 50
```

```c
#include <stdio.h>
#include <pthread.h>

int balance = 1000;  // 共享资源，没有同步保护！

void* buggy_withdraw(void* arg) {
    char* name = (char*)arg;

    // 读取、修改、写回 —— 三步操作不原子！
    int current = balance;
    printf("[%s] 读取余额: %d\n", name, current);
    current -= 100;
    // 这中间可能有其他线程也在读同一个 balance！
    balance = current;
    printf("[%s] 写入余额: %d\n", name, balance);

    return NULL;
}

int main() {
    pthread_t t1, t2, t3, t4;

    printf("初始余额: %d\n", balance);

    // 10 个人同时取钱
    for (int i = 0; i < 4; i++) {
        char name[20];
        sprintf(name, "用户%d", i + 1);
        pthread_create(&t[i], NULL, buggy_withdraw, name);  // 注意：t[i] 在下标访问
    }

    for (int i = 0; i < 4; i++) {
        pthread_join(t[i], NULL);
    }

    printf("\n最终余额: %d（应该是 600）\n", balance);
    printf("问题：部分取款操作"丢失"了！\n");

    return 0;
}
```

运行结果（每次可能不同，这就是"竞态"的含义）：

```
初始余额: 1000
[用户1] 读取余额: 1000
[用户2] 读取余额: 1000
[用户3] 读取余额: 1000
[用户4] 读取余额: 1000
[用户1] 写入余额: 900
[用户2] 写入余额: 900  // 覆盖了用户1的结果！
[用户3] 写入余额: 900  // 又覆盖了！
[用户4] 写入余额: 900  // 又又覆盖了！

最终余额: 900（应该是 600！）—— 银行笑了！
```

**解决方案**：使用互斥锁或原子操作。

### 24.7.2 死锁（Deadlock）

死锁已经在 24.2.5 详细讨论过了。简单回顾：**两个或更多线程互相等待对方持有的锁，形成循环等待，谁都无法继续执行。**

```c
// 经典的死锁场景
void* thread_A(void* arg) {
    pthread_mutex_lock(&mutex_A);  // 先拿 A
    sleep(1);                       // 假装在做事
    pthread_mutex_lock(&mutex_B);  // 再拿 B —— 但 B 可能已经被线程B拿了
    // 永远不会到达这里！
}

void* thread_B(void* arg) {
    pthread_mutex_lock(&mutex_B);  // 先拿 B
    sleep(1);
    pthread_mutex_lock(&mutex_A);  // 再拿 A —— 但 A 可能已经被线程A拿了
    // 永远不会到达这里！
}
```

### 24.7.3 活锁（Livelock）

活锁比死锁更"阴险"。在死锁中，线程们都在等待，什么都不做；在活锁中，线程们都在忙，但忙的事情没有进展——就像两个人在狭窄的走廊里互相让路，你左我也左，你右我也右，永远过不去。

```c
#include <stdio.h>
#include <stdbool.h>
#include <pthread.h>
#include <unistd.h>

// 两个人抢一个资源
typedef struct {
    char name;
    _Atomic bool waiting;
} Person;

void* person_a(void* arg) {
    Person* p = (Person*)arg;
    while (1) {
        printf("[%c] 正在尝试获取资源...\n", p->name);
        // 模拟每次检测到冲突后"礼让"——但可能一直礼让
        usleep(100000);
        printf("[%c] 检测到冲突，礼让！\n", p->name);
        usleep(100000);
        printf("[%c] 再次尝试...\n", p->name);
        usleep(100000);
        // 实际上如果两个人永远同步让路，就活锁了
        // 现实中一般会加入随机退避
    }
    return NULL;
}
```

**解决方案**：引入随机退避（random backoff），或限制重试次数后强制获取。

### 24.7.4 饥饿（Starvation）

饥饿是指一个或多个线程**长期无法获得所需的资源**，因为其他线程一直优先于它。

想象食堂排队：
- 一个老爷爷慢慢排队，每次到窗口都被插队的年轻人挤到后面
- 结果老爷爷永远打不到饭

```c
#include <stdio.h>
#include <pthread.h>
#include <unistd.h>

pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;
int resources = 0;

void* greedy_worker(void* arg) {
    char* name = (char*)arg;
    while (1) {
        pthread_mutex_lock(&mutex);
        resources++;
        printf("[%s] 获取资源: %d\n", name, resources);
        // 模拟长时间持有资源
        usleep(500000);
        resources--;
        pthread_mutex_unlock(&mutex);
        printf("[%s] 释放资源\n", name);
    }
    return NULL;
}

void* patient_worker(void* arg) {
    char* name = (char*)arg;
    while (1) {
        // 模拟低优先级，总是礼让
        usleep(100);
        pthread_mutex_lock(&mutex);
        printf("[%s] 终于获取到资源！\n", name);
        resources++;
        printf("[%s] 释放资源\n", name);
        resources--;
        pthread_mutex_unlock(&mutex);
    }
    return NULL;
}
```

**解决方案**：使用公平锁（FIFO 队列），或引入优先级机制（但要防止优先级反转）。

### ⚠️ 24.7.5 虚假唤醒（Spurious Wakeup）：条件变量 wait **必须用 while 循环**

虚假唤醒是条件变量特有的现象：等待中的线程可能在没有任何线程调用 `signal` 或 `broadcast` 的情况下**莫名其妙地醒来**。

为什么会这样？原因是底层操作系统为了提高效率，可能会有"伪信号"混在真实信号里。这不是 bug，是设计选择。

> **核心原则**：所有对 `pthread_cond_wait` 和 `cnd_wait` 的等待，都必须放在 `while` 循环里，而不是 `if` 条件判断！

```c
// 错误写法 ❌（用 if）
void* bad_consumer(void* arg) {
    pthread_mutex_lock(&mutex);
    if (ready == 0) {  // 如果被虚假唤醒，这里不会重新检查！
        pthread_cond_wait(&cond, &mutex);
    }
    // 继续使用 data，但 data 可能还没准备好！
    printf("数据: %d\n", data);
    pthread_mutex_unlock(&mutex);
    return NULL;
}

// 正确写法 ✓（用 while）
void* good_consumer(void* arg) {
    pthread_mutex_lock(&mutex);
    while (ready == 0) {  // 被唤醒后重新检查条件
        pthread_cond_wait(&cond, &mutex);
    }
    // 现在 data 一定准备好了
    printf("数据: %d\n", data);
    pthread_mutex_unlock(&mutex);
    return NULL;
}
```

```c
#include <stdio.h>
#include <pthread.h>
#include <unistd.h>
#include <stdlib.h>
#include <time.h>

pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t cond = PTHREAD_COND_INITIALIZER;

int ready = 0;
int data = 0;

// 模拟虚假唤醒的测试
void* faker_producer(void* arg) {
    (void)arg;
    srand(time(NULL));

    for (int i = 0; i < 10; i++) {
        pthread_mutex_lock(&mutex);
        data = i;
        ready = 1;

        // 模拟"虚假唤醒"：发送信号但数据没准备好
        // 故意在 ready=0 时发信号（模拟 bug）
        printf("[生产者] 发送信号 (但这里故意乱发)\n");
        pthread_cond_signal(&cond);
        pthread_mutex_unlock(&mutex);

        usleep(500000);
    }
    return NULL;
}

void* careful_consumer(void* arg) {
    char* name = (char*)arg;

    for (int i = 0; i < 10; i++) {
        pthread_mutex_lock(&mutex);

        // 关键：while 循环！
        while (ready == 0) {
            printf("[%s] 等待数据...\n", name);
            pthread_cond_wait(&cond, &mutex);
        }

        printf("[%s] 收到数据: %d\n", name, data);
        ready = 0;  // 消费完标记为未就绪

        pthread_mutex_unlock(&mutex);
    }

    return NULL;
}

int main() {
    pthread_t prod, cons;

    pthread_create(&cons, NULL, careful_consumer, "小明");
    pthread_create(&prod, NULL, faker_producer, NULL);

    pthread_join(prod, NULL);
    pthread_join(cons, NULL);

    pthread_mutex_destroy(&mutex);
    pthread_cond_destroy(&cond);

    printf("\n完成！即使有信号丢失，while 循环也能保证正确性。\n");

    return 0;
}
```

> **为什么 while 循环比 if 好？**
> 1. **防止虚假唤醒**：线程醒来后条件可能仍然不满足
> 2. **防止丢失信号**：如果多个消费者，生产者发了 signal 但只有一个被唤醒，另一个醒来时条件仍然满足（因为 signal 只唤醒一个），需要重新检查
> 3. **防止"惊群"效应**：broadcast 唤醒了所有等待者，但资源只有一份，多余的醒来后条件已经不满足了

---

## 本章小结

本章我们深入探索了 C 语言中线程与并发编程的核心知识，以下是本章要点回顾：

### 线程基础
- **线程 vs 进程**：线程共享地址空间（堆、全局区、代码段），但有独立的栈和寄存器；进程拥有完全独立的地址空间
- **`pthread_create`**：创建新线程，指定执行函数和参数
- **`pthread_join`**：主线程等待目标线程结束并获取其返回值
- **`pthread_detach`**：将线程标记为"自管理"模式，结束时自动释放资源
- **`pthread_exit`**：线程显式退出，携带返回值
- **`pthread_cancel`**：向目标线程发送取消请求（是否响应取决于线程的取消状态）

### 线程同步
- **互斥锁（Mutex）**：`pthread_mutex_lock/unlock`，一次只允许一个线程进入临界区
- **读写锁（RWLock）**：`pthread_rwlock_rdlock/wrlock`，适合"读多写少"场景
- **条件变量（Condition Variable）**：`pthread_cond_wait/signal/broadcast`，实现线程间的"信号通知"
- **信号量（Semaphore）**：`sem_init/wait/post`，计数器式的资源控制，N 个许可
- **死锁（Coffman 条件）**：互斥 + 占有等待 + 不可抢占 + 循环等待；通过资源排序、一次性申请、超时机制预防

### 线程取消
- 取消请求通过取消点（sleep、read、wait 等）生效
- **`pthread_cleanup_push/pop`**：注册清理函数，确保资源在取消时也能正确释放
- **取消状态（enable/disable）** 和 **取消类型（deferred/async）** 可控制取消行为

### 线程局部存储（TLS）
- **`pthread_key_create/getspecific/setspecific`**：POSIX TLS API
- **`_Thread_local` / `thread_local`**：C11 关键字，编译器级支持，更简洁

### C11 `<threads.h>`
- **线程管理**：`thrd_create/join/detach/current/sleep`
- **互斥锁**：`mtx_init/lock/trylock/destroy`（支持 plain/recursive/timed 类型）
- **条件变量**：`cnd_init/wait/signal/broadcast`
- **一次性初始化**：`call_once`
- ⚠️ **警告**：glibc 支持不完全，生产环境推荐 POSIX `<pthread.h>`

### 原子操作 `<stdatomic.h>`
- **`_Atomic` 关键字** 和 `atomic_*` 函数族
- 5 种内存顺序：`relaxed`、`consume`、`acquire`、`release`、`seq_cst`
- 原子操作保证"读取-修改-写入"的不可分割性，完美避免竞态条件

### 常见并发问题
- **竞态条件**：多个线程对共享数据的访问顺序不确定 → 用互斥锁或原子操作解决
- **死锁**：循环等待 → 用资源排序、超时、检测解决
- **活锁**：线程都在运行但没有进展 → 引入随机退避
- **饥饿**：低优先级线程长期无法获得资源 → 使用公平锁
- **虚假唤醒**：`wait` 必须用 `while` 循环，不能用 `if`

> 并发编程的核心挑战是：**共享 + 竞争 = 混乱**。记住这个公式，你就能理解所有同步机制的必要性。下一章我们将深入探讨 C 语言的更多高级主题，敬请期待！
