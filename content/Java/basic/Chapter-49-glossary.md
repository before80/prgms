+++
title = "第49章 常见术语表"
weight = 490
date = "2026-03-30T14:33:56.937+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++
# 第四十九章 常见术语表

> 本章整理了 Java 学习与开发中最常用的专业术语，按类别分组，方便查阅。配套视频持续更新中，建议收藏！

---

## 49.1 Java 基础术语

### JDK（Java Development Kit）

Java 开发工具包，写代码的人离不开它。包含了编译器、调试器、JRE，还有一堆命令行工具。没有它，Java 代码就是一堆天书。形象地说，JDK 就是厨师的整套厨具，没有锅碗瓢盆怎么做饭？

### JRE（Java Runtime Environment）

Java 运行环境。如果你的电脑只需要运行 Java 程序，而不是开发它，那装个 JRE 就够了。可以理解为做好了菜要上桌，你只需要一个餐桌，不需要整个厨房。

### JVM（Java Virtual Machine）

Java 虚拟机，这是 Java 最重要的核心概念之一。Java 之所以能"一次编写，到处运行"，全靠 JVM。它是一个抽象的计算机，屏蔽了底层操作系统的差异。代码编译后变成字节码（.class 文件），JVM 负责解释执行这些字节码。可以把它想象成一个"翻译官"，不管你说的是什么方言，它都能翻译成当地人听得懂的话。

### 字节码（Bytecode）

JVM 能读懂的语言。不是纯粹的机器码，也不是高级语言源代码，而是介于两者之间的中间产物。.class 文件里装的就是这玩意儿。好处是它跟平台无关，坏处是执行速度比不上纯机器码（所以有了 JIT 编译来补救）。

### 面向对象（OOP - Object-Oriented Programming）

一种编程思想，核心概念是"一切皆对象"。Java 是典型的面向对象语言，有三大特性：封装、继承、多态。简单理解就是：把数据和操作数据的方法打包成一个"东西"（对象），这个"东西"有自己的属性和行为。

### 封装（Encapsulation）

把数据和对数据的操作藏进一个类里，对外只暴露接口，不让你直接碰内部数据。好比电视机的遥控器，你按按钮就行，不需要知道内部电路怎么工作的。Java 中通过 private、protected、public 这些访问修饰符来实现。

### 继承（Inheritance）

子类"继承"父类的属性和方法，不用重复造轮子。比如"狗"继承自动物类，"猫"也继承自动物类，它们自动拥有了动物的一些通用特性。Java 只支持单继承（一个类只能有一个直接父类），但可以通过接口实现多继承的效果。

### 多态（Polymorphism）

同一个行为有不同的表现形式。体现在两个方面：编译时多态（方法重载）和运行时多态（方法重写 + 向上转型）。就像"叫"这个动作，狗是"汪汪"，猫是"喵喵"，同一个方法名，不同对象调用结果不同。

### 抽象类（Abstract Class）

用 `abstract` 关键字修饰的类，不能直接实例化。它是"半成品"，可以包含抽象方法（没有方法体的方法）和具体方法（有方法体的方法）。子类继承抽象类后，必须实现所有抽象方法，否则子类也只能是抽象类。可以理解为一张设计图，你不能直接使用设计图，但可以按它来造东西。

### 接口（Interface）

一种完全抽象的类型，用 `interface` 关键字声明。接口里只有方法签名（抽象方法）、常量、和默认方法（Java 8 之后）。类通过 `implements` 关键字来实现接口。接口用来定义"能做什么"，而抽象类可以定义"是什么"。一个类可以实现多个接口，但只能继承一个类。

### 重写（Override）

子类重新定义父类已有的方法，方法签名必须完全一致。@Override 注解不是必须的，但加上它编译器会帮你检查是否真的在重写而不是重载。

### 重载（Overload）

同一个类里，多个方法名字相同，但参数列表不同（参数个数、类型、顺序不同）。这是编译时多态，编译器根据参数来决定调用哪个方法。就像"打"这个动作，你可以"打篮球"、"打游戏"、"打人"，具体打什么看上下文。

### 构造方法（Constructor）

创建对象时调用的特殊方法，名字跟类名相同，没有返回类型（不是返回 void，是根本不写返回类型）。如果没写构造方法，编译器会自动生成一个无参构造方法。它的作用是初始化对象的状态。

### 静态（Static）

用 `static` 关键字修饰的成员属于类本身，而不是某个具体的对象。静态变量所有对象共享一份，静态方法只能访问静态成员。main 方法就是静态的，因为程序启动时还没有创建任何对象。

### final

三重身份，关键字多用的典范：

- 修饰变量：变成常量，值不能改变
- 修饰方法：方法不能被重写
- 修饰类：类不能被继承

可以理解为"铁饭碗"，一旦确定就不能改。

### this 和 super

- `this`：指向当前对象，就是"我自己"
- `super`：指向父类对象，就是"我爸爸"

在构造方法中，`this()` 可以调用本类的其他构造方法，`super()` 可以调用父类的构造方法。而且 `this` 和 `super` 在构造方法中必须是第一条语句。

### 反射（Reflection）

程序在运行时可以访问、检测和修改它自身状态或行为的能力。Java 提供了 java.lang.reflect 包支持反射。通过反射可以在运行时获取类的结构（属性、方法、构造器），可以调用任意方法，可以绕过访问修饰符的限制。Spring 框架、IDE 的智能提示都用到了反射。

### 注解（Annotation）

一种元数据，@ 开头的标识。可以理解为"标签"或者"记号"。注解本身不影响代码执行，但可以被编译器、解释器或框架读取并做出相应处理。比如 @Override 告诉编译器检查重写，@Autowired 告诉 Spring 注入依赖。

### 泛型（Generics）

参数化类型，让代码可以作用于不同类型的同时保证类型安全。在集合框架中用得最广泛：`List<String>` 表示一个只装字符串的列表。泛型在编译阶段做类型检查，运行阶段泛型信息会被擦除（类型擦除）。

---

## 49.2 集合框架术语

### 集合框架（Collection Framework）

Java 提供的一套用于存储和管理一组对象的统一架构。位于 java.util 包下，主要包含接口、实现类和工具类三大部分。核心接口有：Collection、List、Set、Queue、Map。

### Iterable 和 Iterator

- `Iterable`：实现这个接口的对象可以被迭代，可以用 for-each 循环遍历
- `Iterator`：迭代器接口，提供 hasNext()、next()、remove() 方法

简单说，Iterable 表示"可以被遍历"，Iterator 是"实际的遍历工具"。

### Collection

集合框架的根接口之一，继承自 Iterable。定义了集合的基本操作：add、remove、contains、size 等。但不包括"按键取值"的功能——那是 Map 的事。

### List

有序集合（也称为序列），元素有索引，可以重复。常见的实现类有：

- **ArrayList**：基于动态数组实现，读快写慢（指定位置插入/删除慢）
- **LinkedList**：基于双向链表实现，写快读慢，还实现了 Queue 接口
- **Vector**：古老的线程安全版本，现在一般不推荐使用

### Set

无序、不重复的集合。常用的实现类有：

- **HashSet**：基于哈希表实现，是最常用的 Set，性能优秀，但不保证顺序
- **LinkedHashSet**：继承自 HashSet，维护元素的插入顺序
- **TreeSet**：基于红黑树实现，元素自动排序（需要元素实现 Comparable 或提供 Comparator）

### Queue

队列接口，遵循 FIFO（先进先出）原则。常见的实现类有：

- **LinkedList**：既实现了 List 又实现了 Queue
- **PriorityQueue**：基于堆实现的优先队列，元素按优先级出队，不保证 FIFO
- **ArrayDeque**：双端队列，两端都可以插入和删除

### Deque

双端队列，两端都可以操作。继承自 Queue。ArrayDeque 是常用的实现，比 LinkedList 效率更高（因为 ArrayDeque 不需要维护前后引用）。

### Map

键值对映射，不是 Collection 的子接口，但它是集合框架的重要组成部分。键（Key）唯一，值（Value）可以重复。常用实现类：

- **HashMap**：最常用的 Map，键值对无序，支持快速查找
- **LinkedHashMap**：维护插入顺序
- **TreeMap**：键按自然顺序或自定义顺序排序
- **Hashtable**：古老的线程安全版本，基本被 ConcurrentHashMap 取代
- **ConcurrentHashMap**：线程安全的高性能 Map，并发编程首选

### HashMap 的底层原理

JDK 8 及之后，HashMap 底层是"数组 + 链表 + 红黑树"的组合。当哈希冲突严重（同一个桶里链表过长）时，链表会转化为红黑树以提升查询效率。扩容因子默认 0.75，即当元素数量超过容量的 75% 时会触发扩容。

### 哈希冲突（Hash Collision）

不同的 key 经过哈希函数计算后得到相同的哈希值。无法完全避免，只能尽量减少。处理方法有：开放地址法（线性探测、二次探测）、链地址法（HashMap 用的是这个）、再哈希法。

### equals() 和 hashCode()

- `equals()`：判断两个对象是否"相等"
- `hashCode()`：返回对象的哈希码

这两个方法有契约关系：如果两个对象 equals 返回 true，它们的 hashCode 必须相同。反过来不一定（哈希冲突时 hashCode 相同但对象不一定 equal）。在使用 HashMap、HashSet 等基于哈希的集合时，重写 equals 必须同时重写 hashCode。

### 红黑树（Red-Black Tree）

一种自平衡的二叉查找树，Java 中 TreeMap 和 HashMap 的链表树化都用到了它。它通过着色和旋转操作来保持大致平衡，保证查找、插入、删除的时间复杂度为 O(log n)。

### 扩容（Resize/Rehashing）

当集合中的元素数量超过阈值时，底层数组需要扩容。HashMap 每次扩容为原来的 2 倍，并重新计算所有元素的位置（rehash）。这是比较耗时的操作，所以预知大小时建议指定初始容量。

### fail-fast 和 fail-safe

- **fail-fast**：在迭代过程中，如果集合被结构化修改（增删元素），迭代器会快速失败，抛出 ConcurrentModificationException。ArrayList、HashMap 等非线程安全集合是 fail-fast 的
- **fail-safe**：在迭代时基于原集合的拷贝进行，修改原集合不会影响迭代器。ConcurrentHashMap、CopyOnWriteArrayList 是 fail-safe 的

---

## 49.3 并发编程术语

### 进程（Process）

程序的一次执行过程，是操作系统分配资源的基本单位。每个进程都有独立的内存空间，进程之间相互隔离。启动一个 Java 程序，操作系统就会创建一个进程。

### 线程（Thread）

进程内的执行单元，是 CPU 调度的基本单位。一个进程可以包含多个线程，线程共享进程的堆内存，但有独立的栈内存。线程的创建和销毁成本比进程低很多。

### 线程与进程的区别

进程像独立的工厂，各有各的地盘；线程像工厂里的工人，共享工厂的资源但各有各的任务。线程开销小，通信方便，但管理不当容易出问题。

### Thread

Java 中创建线程最基础的方式。继承 Thread 类并重写 run() 方法，然后调用 start() 启动。缺点是类已经继承了 Thread 就不能再继承其他类。

```java
Thread thread = new Thread() {
    @Override
    public void run() {
        System.out.println("线程执行中...");
    }
};
thread.start();
```

### Runnable 和 Callable

- `Runnable`：函数式接口，只有一个 run() 方法，无返回值，不能抛出受检异常
- `Callable`：带泛型的接口，有 call() 方法，有返回值，可以抛出异常

```java
Runnable task = () -> System.out.println("干活了");
Callable<String> task2 = () -> "干完了";
```

### 线程池（Thread Pool）

线程池（Thread Pool）：管理一组线程的容器，避免频繁创建和销毁线程带来的性能开销。Java 通过 Executor 框架提供线程池支持。常用线程池：

- **FixedThreadPool**：固定数量的线程池
- **CachedThreadPool**：可缓存的线程池，线程数量不固定
- **SingleThreadExecutor**：单线程的线程池
- **ScheduledThreadPool**：定时任务线程池

### Executors

创建线程池的工具类，提供了各种便捷工厂方法。但阿里 Java 规范不推荐使用 Executors 创建线程池，因为默认的拒绝策略可能有问题，建议使用 ThreadPoolExecutor 手动创建以便更好地控制参数。

### 线程安全（Thread Safety）

多个线程访问同一个对象时，如果不需要额外的同步控制，调用结果始终正确，就说明这个对象是线程安全的。线程安全不是非此即彼的，它有多个级别：不可变、绝对线程安全、相对线程安全、线程兼容、线程对立。

### 同步（Synchronized）

解决线程安全问题的最基本手段。加了 synchronized 的代码块同一时刻只能有一个线程进入。可以修饰方法或代码块。原理是每个对象都有一把"锁"，进去之前要抢到这把锁才能执行。

### volatile

轻量级的同步机制。保证变量的可见性（一个线程修改后其他线程立即看到）和禁止指令重排序，但不保证原子性。它不涉及排队和等待，只是确保每次读取都从主内存读，而不是从 CPU 缓存读。

### CAS（Compare-And-Swap）

乐观锁的实现方式。全称"比较并交换"，操作包含三个值：内存位置 V、旧的预期值 A、新值 B。如果当前值等于预期值 A，就把位置 V 的值更新为 B；否则什么都不做。整个操作是原子的。Java 并发包中大量使用了 CAS，比如 AtomicInteger 的实现。

### ABA 问题

CAS 的一个经典陷阱：线程1读取到 A，线程2把 A 改成 B 又改回 A，线程1的 CAS 操作仍然成功，但线程1并不知道数据已经被修改过。解决方案是使用版本号（AtomicStampedReference）或者加时间戳（AtomicMarkableReference）。

### AQS（AbstractQueuedSynchronizer）

队列同步器，是 Java 并发包的核心组件。ReentrantLock、Semaphore、CountDownLatch、ThreadPoolExecutor 等都基于 AQS 实现。它用 CLH 队列来管理等待的线程，用 state 变量来表示同步状态，开发者可以基于它来实现自定义的同步器。

### ReentrantLock

可重入锁，比 synchronized 更灵活。加锁和解锁需要手动控制，可以尝试非阻塞地获取锁（tryLock()），可以设置公平锁还是非公平锁。但 synchronized 更简单，ReentrantLock 功能更强。

### ReentrantReadWriteLock

读写锁，适合读多写少的场景。读锁是共享的，多个线程可以同时读；写锁是排他的，一次只能有一个线程写。读和写不能同时进行。它内部维护了 ReadLock 和 WriteLock 两把锁。

### Semaphore

信号量，用来控制同时访问特定资源的线程数量。acquire() 获取许可，release() 释放许可。相当于停车场的车位指示牌：有多少个许可，就允许多少个线程同时操作。

### CountDownLatch

倒计时门闩。在初始化时设置一个计数，线程调用 await() 等待，其他线程调用 countDown() 让计数减 1。当计数减到 0 时，所有等待的线程被唤醒继续执行。常用于"主线程等待子线程执行完毕"的场景。

### CyclicBarrier

循环屏障，跟 CountDownLatch 相反。多个线程相互等待，等所有人都到了屏障点，才一起继续执行。可以循环使用，所以叫"循环"的。

### ThreadLocal

线程局部变量。每个线程都有自己独立的副本，线程之间互不影响。通常用来保存线程上下文信息，比如用户会话、事务 ID 等。常用方法：set()、get()、remove()、initialValue()。用完记得 remove()，否则可能导致内存泄漏。

### 内存可见性（Memory Visibility）

一个线程对共享变量的修改，能被其他线程看到。由于 CPU 缓存和编译器的指令重排序，没有同步的共享变量可能产生可见性问题。volatile、synchronized、final（初始化安全）都可以解决可见性问题。

### 指令重排序（Instruction Reordering）

编译器或处理器为了优化性能，可能会改变代码的执行顺序。但它只保证单线程执行结果不变，在多线程环境下可能导致问题。volatile 通过插入内存屏障来禁止指令重排序。

### 死锁（Deadlock）

两个或多个线程相互等待对方持有的资源，导致谁都無法继续执行。产生死锁必须同时满足四个条件：互斥、占有并等待、不可抢占、循环等待。解决思路是打破其中任意一个条件。

### 活锁（Livelock）

线程虽然没有阻塞，但一直在重复执行相同的操作——通常是因为某种条件没满足，导致不断重试。区别于死锁：死锁是大家都不动，活锁是大家都在动但没进展。

### 饥饿（Starvation）

某些线程永远得不到所需的资源（不是因为死锁，而是优先级太低或调度策略导致一直得不到 CPU 时间片）。比如非公平锁可能让某些线程一直抢不到锁。

### JMM（Java Memory Model）

Java 内存模型，定义了 JVM 如何协调不同硬件和操作系统的内存访问差异。它规定了线程之间如何通过内存交互，确保并发程序在各种平台上的行为一致。volatile、synchronized、final 的语义都由 JMM 规定。

---

## 49.4 JVM 术语

### JVM 内存区域

JVM 在运行时把内存划分成若干区域，各司其职：

- **程序计数器（Program Counter Register）**：当前线程执行的字节码行号指示器。每个线程都有自己独立的 PC 寄存器，线程切换后能恢复到正确的执行位置。是唯一不会发生 OutOfMemoryError 的区域。
- **虚拟机栈（VM Stack）**：每个方法执行时都会创建一个栈帧（Stack Frame），用于存储局部变量表、操作数栈、动态链接、方法出口等信息。线程私有，生命周期与线程相同。
- **本地方法栈（Native Method Stack）**：为 JVM 使用到的 Native 方法服务，跟虚拟机栈类似。
- **堆（Heap）**：最大的一块内存区域，几乎所有对象实例和数组都在这里分配。是 GC 的主要管理区域，也叫"GC 堆"。线程共享。
- **方法区（Method Area）**：存储类信息（类的元数据）、常量、静态变量、即时编译器编译后的代码。JDK 8 之前用永久代（PermGen）实现，JDK 8 之后改用元空间（Metaspace），使用本地内存而不是堆内存。

### 栈帧（Stack Frame）

方法调用时在虚拟机栈中分配的数据结构。每个方法从调用到执行完成，就对应着一个栈帧在虚拟机栈中的入栈和出栈。

### 局部变量表

栈帧中的一部分，用于存储方法参数和局部变量。索引从 0 开始，0 位通常是 this（实例方法中）。

### 对象的内存布局

在 HotSpot 虚拟机中，对象在堆中的存储布局分为三部分：

- **对象头（Header）**：包含 Mark Word（存储哈希码、GC 分代年龄、锁状态等）和类型指针（指向类元数据的指针）
- **实例数据（Instance Data）**：对象实际存储的字段内容
- **对齐填充（Padding）**：HotSpot 要求对象大小是 8 字节的整数倍，不足时填充

### 对象的创建过程

new 一个对象时，JVM 经历了：检查类是否加载 → 分配内存（指针碰撞或空闲列表）→ 初始化为零值 → 设置对象头 → 执行构造函数。

### 分配内存的线程安全问题

两个线程同时给一个对象分配内存，可能导致指针碰撞出问题。解决方案：CAS + 重试（乐观锁），或者使用 TLAB（Thread Local Allocation Buffer），每个线程预先在堆中分配一小块专属区域。

### TLAB（Thread Local Allocation Buffer）

线程本地分配缓冲区。JVM 为每个线程在堆中预留的一小块空间，新对象优先在 TLAB 中分配，避免多线程竞争。TLAB 用完了才去使用公共空间。

### GC（Garbage Collection）

垃圾回收，自动管理内存。Java 不用手动释放对象，JVM 的 GC 线程会自动回收那些不再被引用的对象。GC 是 Java 最大的优点之一，也是面试最喜欢问的内容。

### 引用计数法（Reference Counting）

一种古老的 GC 算法：为每个对象维护一个引用计数器，有引用就加 1，引用消失就减 1。计数器为 0 就回收。简单但无法处理循环引用的问题（两个对象互相引用但外部已无引用），所以 JVM 没有采用这种方式。

### 可达性分析（Reachability Analysis）

JVM 主流的垃圾判定算法。通过一系列"GC Roots"对象作为起点，向下搜索，走过的路径称为"引用链"。如果一个对象到 GC Roots 没有任何引用链相连，则判定为可回收。GC Roots 包括：虚拟机栈中引用的对象、方法区中静态属性引用的对象、方法区中常量引用的对象、本地方法栈中 JNI 引用的对象等。

### 强引用（Strong Reference）

最普通的引用写法：`Object obj = new Object()`。只要强引用还在，垃圾收集器永远不会回收这个对象。内存泄漏的元凶之一。

### 软引用（Soft Reference）

`SoftReference<Object>`，描述还有用但非必需的对象。在内存溢出前才会回收。常用于实现内存敏感的缓存。

### 弱引用（Weak Reference）

`WeakReference<Object>`，比软引用更弱。下一次垃圾收集时一定会被回收，不管内存是否够用。常用于非强制持有的缓存，比如 WeakHashMap。

### 虚引用（Phantom Reference）

`PhantomReference<Object>`，最弱的引用。完全不影响垃圾收集，唯一作用是在对象被回收时收到一个系统通知。常用于追踪对象的回收过程。

### Minor GC 和 Major GC / Full GC

- **Minor GC**：新生代 GC，非常频繁，速度较快
- **Major GC / Old GC**：老年代 GC，通常伴随 Minor GC
- **Full GC**：整堆收集，包括新生代、老年代、方法区。速度最慢，应尽量避免

### 分代收集理论（Generational Collection）

现代 JVM 垃圾收集的理论基础。核心假设：大部分对象的生命周期很短，只有少数对象存活时间较长。因此将堆分为新生代和老年代，分别采用不同的收集策略。新生代对象多，使用标记-复制算法；老年代对象少，使用标记-清除或标记-整理算法。

### 新生代（Young Generation）

又叫年轻代，存放新创建的对象。分为 Eden 区和两个 Survivor 区（From 和 To，也叫 S0 和 S1）。对象优先在 Eden 区分配。Minor GC 后，存活的对象被复制到 Survivor 区，Eden 区清空。

### 老年代（Old/Tenured Generation）

存放生命周期较长的对象。经过多次 Minor GC 后仍然存活的对象会被晋升到老年代。老年代空间不足时触发 Major GC（也叫 Old GC）。

### 永久代（PermGen）和元空间（Metaspace）

JDK 8 之前，方法区使用永久代实现，位于 JVM 堆内存中，容易发生 OutOfMemoryError: PermGen space。JDK 8 改用元空间，使用本地内存（Native Memory），不再受堆大小限制，默认可以动态扩展。

### 标记-清除算法（Mark-Sweep）

最基础的 GC 算法。标记阶段：找出所有需要回收的对象并标记。清除阶段：统一回收被标记的对象。缺点是会产生内存碎片，导致后续分配大对象时找不到连续空间。

### 标记-复制算法（Mark-Copy）

为了解决标记-清除的碎片问题而生。将内存分成两块，每次只使用一块。GC 时把存活的对象复制到另一块，然后一次性清理这块。缺点是可用内存减半。非常适合对象存活率低的新生代（HotSpot 的新生代用的就是这个）。

### 标记-整理算法（Mark-Compact）

老年代的常用算法。标记阶段跟标记-清除一样，但后续不是直接清理，而是让存活对象向一端移动，然后清理边界以外的内存。避免了碎片，但移动对象开销较大。

### Serial 收集器

最古老、最简单的单线程收集器。GC 时必须暂停所有用户线程（Stop The World）。适合单核 CPU 或小内存场景。现在基本不用了。

### ParNew 收集器

Serial 的多线程版本，多个线程并行进行 GC。GC 时同样需要 Stop The World。是 CMS 收集器的搭档，JDK 9 之前配合 CMS 使用。

### Parallel Scavenge 收集器

跟 ParNew 类似，也是多线程并行收集，但关注点不同：目标是达到一个可控的吞吐量（吞吐量 = 用户代码运行时间 / 总时间）。适合后台计算任务。配合 Serial Old 或 Parallel Old 使用。

### CMS（Concurrent Mark Sweep）收集器

老年代收集器，以获取最短回收停顿时间为目标。GC 过程分为：初始标记（Stop The World）→ 并发标记（与用户线程并发）→ 重新标记（Stop The World）→ 并发清除（与用户线程并发）。缺点是对 CPU 资源敏感、无法处理浮动垃圾、会产生空间碎片。

### G1（Garbage-First）收集器

JDK 7 引入，JDK 9 之后成为默认垃圾收集器。它把堆划分为多个大小相等的 Region（区域），每个 Region 可以独立作为 Eden、Survivor 或老年代。优先回收垃圾最多的区域，因此叫 Garbage-First。兼顾吞吐量和停顿时间，是目前最先进的 GC 之一。

### ZGC（Z Garbage Collector）

JDK 11 引入的超低延迟 GC。目标是将 Stop The World 的停顿时间控制在毫秒级以内，且不随堆大小增加而增加停顿时间。支持并发标记、并发压缩、使用着色指针实现读屏障。

### 类加载器（ClassLoader）

负责将 .class 文件加载到 JVM 中。Java 中有三层类加载器：

- **Bootstrap ClassLoader**：启动类加载器，加载 Java 核心类库（%JAVA_HOME%/lib）
- **Extension ClassLoader**：扩展类加载器，加载 %JAVA_HOME%/lib/ext 目录下的类
- **Application ClassLoader**：应用程序类加载器，加载用户 classpath 上的类

### 双亲委派模型（Parent Delegation Model）

类加载器的委托机制：当一个类加载器收到加载请求时，它先把这个请求委托给父类加载器处理，只有父加载器找不到时，才自己尝试加载。这样保证了类的唯一性和安全性——比如你不能写一个 java.lang.String 来冒充核心类库。

### 类的生命周期

加载 → 验证 → 准备 → 解析 → 初始化 → 使用 → 卸载。其中验证、准备、解析统称为链接（Linking）。

### 即时编译器（JIT - Just-In-Time Compiler）

JVM 解释执行字节码效率不高，JIT 编译器出场了。它在程序运行过程中，把热点代码（Hot Spot Code）编译成机器码并缓存起来，下次直接执行机器码，大幅提升性能。HotSpot 虚拟机有两个 JIT 编译器：C1（Client Compiler）和 C2（Server Compiler）。

### 解释器和 JIT 编译器

- **解释器**：一条一条地解释执行字节码，启动快，执行慢
- **JIT 编译器**：把热点代码编译成本地机器码，执行快，但编译需要时间

JVM 会先用解释器执行，统计发现热点代码后交给 JIT 编译。两者配合，启动快的同时又有高性能。

### 逃逸分析（Escape Analysis）

JIT 编译器的优化手段。分析一个对象的动态作用域：如果对象只在方法内部使用（不逃逸），就可能进行栈上分配（直接分配在栈上，方法结束自动回收，不需要 GC）、标量替换（把对象拆散成基本类型）等优化。

### 字节码指令

JVM 的指令集，每条指令以一个字节的操作码（opcode）开头，所以叫字节码。常见的有：iconst、bipush、aload、astore、invokevirtual、ireturn 等。了解字节码对阅读反编译结果（javap -c）有帮助。

### OOM（OutOfMemoryError）

内存溢出，JVM 分配不出更多内存了。常见的 OOM 类型：

- **java.lang.OutOfMemoryError: Java heap space** —— 堆内存不足，最常见
- **java.lang.OutOfMemoryError: PermGen space** —— 永久代满了（ JDK 8 前）
- **java.lang.OutOfMemoryError: Metaspace** —— 元空间满了（JDK 8+）
- **java.lang.OutOfMemoryError: unable to create new native thread** —— 线程数太多，栈空间耗尽

### StackOverflowError

栈溢出。线程请求的栈深度超过了 JVM 允许的最大深度。常见于递归没有正确写终止条件，导致无限递归。

---

## 49.5 框架术语

### Spring Framework

Java 生态中最核心的企业级开发框架。提供 IoC 容器和 AOP 支持，是几乎所有 Java Web 开发的基础。Spring 的核心理念是"轻量级"——它不是一站式解决方案，而是通过组合各种组件来构建应用。

### IoC（Inversion of Control）

控制反转，也叫依赖注入（DI）。不是什么新技术，而是一种设计思想。传统程序是我们自己创建依赖对象；IoC 模式下，控制权反转了，由 Spring 容器来创建和管理对象，我们只需要"接收"注入。打个比方：自己做饭 vs. 点外卖——自己做饭要自己买菜、洗菜、炒菜；IoC 就是 Spring 帮你把做好的饭送到嘴边。

### DI（Dependency Injection）

依赖注入，IoC 的一种具体实现。通过构造函数、setter 方法或字段注入，让 Spring 容器在创建对象时把依赖传进来。

### Spring IoC 容器

Spring 的核心，负责对象的创建、组装和管理。两大主流实现：

- **BeanFactory**：最基础的容器，延迟加载
- **ApplicationContext**：功能更强大，启动时就加载所有 Bean，企业开发常用

### Bean

由 Spring IoC 容器管理的对象。在 Spring 中就是加了 @Component、@Service、@Repository、@Controller 等注解的类，或者通过 XML/配置类声明的类。

### @Component、@Service、@Repository、@Controller

Spring 中用于声明 Bean 的注解：

- `@Component`：通用组件，任何类都可以用
- `@Service`：业务逻辑层组件，跟 @Component 语义相同，只是起名更明确
- `@Repository`：数据访问层组件（DAO），Spring 还会对数据库异常做特殊封装
- `@Controller`：控制器层，Spring MVC 的核心组件

### AOP（Aspect-Oriented Programming）

面向切面编程。核心思想是把那些分散在多个模块中的"横切关注点"（如日志、事务、安全）抽取出来统一处理。Spring AOP 基于动态代理实现，AspectJ 则是字节码编织，功能更强大但配置更复杂。

### 切面（Aspect）

横切关注点的模块化。在 Spring AOP 中，用 @Aspect 注解标注的类就是一个切面，里面定义了切点（Pointcut）和通知（Advice）。

### 切点（Pointcut）

定义在哪些地方（Join Point）执行通知。Spring AOP 中用 @Pointcut 注解来定义切点表达式，决定"在哪个方法上增强"。

### 通知（Advice）

切面在某个连接点执行的动作。分为五种类型：

- **@Before**：前置通知，在方法执行前运行
- **@AfterReturning**：返回通知，方法正常返回后运行
- **@AfterThrowing**：异常通知，方法抛出异常后运行
- **@After**：后置通知，无论方法正常还是异常都运行
- **@Around**：环绕通知，最强大，可以控制方法何时开始、何时结束

### 动态代理（Dynamic Proxy）

AOP 的实现基础。JDK 动态代理基于接口，Spring 默认用它来代理实现了接口的类；CGLIB 通过继承生成子类来代理，不需要接口但无法代理 final 类和 final 方法。

### Spring MVC

基于 Servlet API 的 Web 框架。处理流程：请求 → DispatcherServlet → HandlerMapping（找处理器）→ HandlerAdapter（执行处理器）→ ViewResolver（解析视图）→ 渲染。注解驱动开发让配置大幅简化。

### DispatcherServlet

Spring MVC 的前端控制器，所有的请求都经过它来分发。它是整个 Spring MVC 的门户，是请求的第一站。

### Spring Boot

"让 Spring 更易用"的框架。核心目标是：开箱即用、自动配置、内嵌服务器。不用再繁琐地配置 XML，写几行代码一个 Web 应用就跑起来了。它的底层还是 Spring Framework，但把大量配置工作自动化了。

### Spring Cloud

微服务框架，基于 Spring Boot 构建。提供了一整套分布式系统的解决方案：服务注册与发现（Eureka/Nacos）、负载均衡（Ribbon）、服务调用（Feign/OpenFeign）、熔断器（Hystrix/Sentinel）、配置中心（Config/Nacos）、网关（Gateway）等。

### Hibernate

全自动的 ORM（对象关系映射）框架。定义实体类后，Hibernate 自动生成 SQL、自动执行、自动映射结果到对象。配置简单但 SQL 控制力弱一些。JPA（Java Persistence API）就是以 Hibernate 为参考实现的。

### JPA（Java Persistence API）

Java 持久化规范，定义了 ORM 的标准接口。Hibernate、 EclipseLink 是 JPA 的实现。用了 JPA 注解（@Entity、@Table、@Column 等），理论上换一个 JPA 实现不用改代码。

### MyBatis

半自动的 ORM 框架。相比 Hibernate，MyBatis 更灵活——SQL 自己写，对数据库的控制力更强。在国内互联网公司使用非常广泛。MyBatis 不会自动生成 SQL，但可以通过逆向工程生成基础代码。

### ORM（Object-Relational Mapping）

对象关系映射，把数据库表映射成对象，把 SQL 操作映射成对象操作。不用写繁琐的 JDBC 代码，不用手动拼接 SQL，结果集自动映射到 Java 对象。

### 事务（Transaction）

一组操作要么全部成功，要么全部失败，不允许部分成功。ACID 特性：原子性（Atomicity）、一致性（Consistency）、隔离性（Isolation）、持久性（Durability）。Spring 通过 @Transactional 注解来声明事务管理。

### Spring 事务传播行为

当一个事务方法被另一个事务方法调用时，被调用方法的事务如何"传播"。常见的有：

- **REQUIRED**（默认）：如果有事务就加入，没有就新建
- **REQUIRES_NEW**：挂起当前事务，自己新建一个事务
- **NESTED**：如果当前有事务，就在嵌套事务中执行

### 声明式事务 vs 编程式事务

- **声明式事务**：用 @Transactional 注解搞定，简单方便，侵入性低
- **编程式事务**：用 TransactionTemplate 或 TransactionManager 手动控制，更精确但代码繁琐

### 过滤器（Filter）

Servlet 规范中的组件，在请求到达 Servlet 之前和响应返回之前执行过滤逻辑。适合处理字符编码、登录校验、全局日志等。Filter 的执行顺序由 @Order 注解或 web.xml 配置决定。

### 拦截器（Interceptor）

Spring MVC 提供的组件，类似于 Filter 但只针对 Spring MVC 的请求。可以获取 HandlerMethod 和 ModelAndView 信息。比 Filter 更"懂"Spring MVC 的上下文。

### RESTful API

一种设计风格，用 HTTP 动词（GET/POST/PUT/DELETE）表达对资源的操作。URL 名词复数，不含动词。例如：GET /users（查用户列表）、POST /users（新增用户）、PUT /users/1（更新 ID 为 1 的用户）、DELETE /users/1（删除用户）。

### Ribbon

Netflix 提供的客户端负载均衡组件。配合服务发现（Eureka）使用，在发起服务调用时自动选择一个可用的服务器节点。

### Hystrix / Resilience4j

熔断器。某个服务故障时快速失败，防止故障蔓延影响整个系统。当某个服务调用失败次数达到阈值，"熔断器"就会打开，后续请求直接返回错误而不再真正调用，避免系统雪崩。Hystrix 已进入维护模式，Spring 推荐使用 Resilience4j。

### Sentinel

阿里巴巴开源的流量控制和熔断降级组件。比 Hystrix 功能更丰富，提供了实时监控、控制台配置、规则持久化等。在国内分布式系统中使用广泛。

### Nacos

阿里巴巴开源的服务发现、配置管理平台。可以作为注册中心（替代 Eureka）和配置中心（替代 Spring Cloud Config）。开箱即用，在国内云原生场景中使用量很大。

### Dubbo

阿里巴巴开源的高性能 RPC 框架，主要用于微服务之间的远程调用。与 Spring Cloud 对比：Dubbo 更专注于 RPC，Spring Cloud 是完整的微服务生态。Dubbo 支持多种序列化协议和负载均衡策略。

---

## 49.6 数据库术语

### SQL（Structured Query Language）

结构化查询语言，数据库的标准操作语言。所有关系型数据库（RDBMS）都支持 SQL。包含四大金刚：DDL（数据定义语言）、DML（数据操作语言）、DCL（数据控制语言）、DQL（数据查询语言）。

### DDL、DML、DCL、DQL

- **DDL**（Data Definition Language）：CREATE、DROP、ALTER、TRUNCATE，操作表结构
- **DML**（Data Manipulation Language）：INSERT、UPDATE、DELETE，操作数据
- **DCL**（Data Control Language）：GRANT、REVOKE，控制权限
- **DQL**（Data Query Language）：SELECT，查询数据

### 关系型数据库（RDBMS）

基于关系模型（表和表之间的关联）的数据库。用二维表来组织数据，每行是记录，每列是字段。常见的关系型数据库：MySQL、Oracle、PostgreSQL、SQL Server。

### NoSQL

非关系型数据库的统称，特点是没有固定的表结构。常见的 NoSQL 类型：

- **键值数据库**：Redis、Memcached
- **文档数据库**：MongoDB
- **列族数据库**：HBase、Cassandra
- **图数据库**：Neo4j

### 主键（Primary Key）

唯一标识表中每一行数据的字段（或字段组合）。主键值不能为空（NOT NULL）且不能重复。一张表只能有一个主键，但可以有复合主键（多列联合作为主键）。

### 外键（Foreign Key）

表与表之间的引用约束。一个表中的某个字段引用了另一张表的主键，就形成了外键关系。外键保证了数据的参照完整性，但过多的外键约束会影响写入性能。

### 索引（Index）

数据库中用于加速查询的数据结构。类似于书的目录，索引越大，查找越快。但索引不是免费的——它会占用额外的存储空间，且写入数据时要同步维护索引，增加写入开销。

### 聚簇索引（Clustered Index）

数据行与索引结构一一对应的索引。InnoDB 中，主键索引就是聚簇索引，叶子节点存储完整的数据行。一张表只有一个聚簇索引。

### 非聚簇索引（Non-Clustered Index）

叶子节点存储的是主键值（或者是索引键值 + 主键值），而不是完整的数据行。查询时需要"回表"——先在非聚簇索引中找到主键，再通过主键去聚簇索引查找完整数据。

### 覆盖索引（Covering Index）

查询的所有列都包含在索引中，查询时不需要回表，直接从索引中获取结果，性能最优。在 SQL 优化中很常用。

### 事务（Transaction）

数据库事务，ACID 四特性：原子性（Atomicity）、一致性（Consistency）、隔离性（Isolation）、持久性（Durability）。BEGIN → 执行 SQL → COMMIT/ROLLBACK。

### 隔离级别（Isolation Level）

多个事务并发执行时，数据库系统需要保证事务之间的隔离程度。标准定义了四个隔离级别：

- **READ UNCOMMITTED**：最低级别，存在脏读
- **READ COMMITTED**：解决脏读，但存在不可重复读
- **REPEATABLE READ**：解决不可重复读（MySQL InnoDB 的默认级别），但存在幻读
- **SERIALIZABLE**：最高级别，事务串行执行，完全避免了各种并发问题，但性能最差

### 脏读（Dirty Read）

一个事务读取了另一个事务尚未提交的数据。如果那个事务最后回滚了，读到的数据就是"脏"的、无效的。

### 不可重复读（Non-Repeatable Read）

同一事务中，两次读取同一行数据，结果不一样（因为中间被另一个事务修改并提交了）。

### 幻读（Phantom Read）

同一事务中，两次查询返回的记录数不一样（因为中间被另一个事务插入或删除了记录）。

### MVCC（Multi-Version Concurrency Control）

多版本并发控制。InnoDB 通过隐藏的两列（事务 ID 和回滚指针）和 undo log 实现。每个事务看到的数据版本可能不同，实现了读不加锁，提升并发性能。快照读和当前读是它的两个读模式。

### 快照读 vs 当前读

- **快照读**：读取历史版本（快照），不加锁。普通的 SELECT 语句就是快照读
- **当前读**：读取最新数据，加锁。SELECT ... FOR UPDATE、INSERT、UPDATE、DELETE 都是当前读

### 锁（Lock）

数据库用来控制并发访问的机制。加锁后，其他事务必须等待锁释放才能操作被锁定的资源。锁的粒度可以是行锁、表锁、页锁。

### 共享锁（Shared Lock / S Lock）

读锁。事务读取一行数据时加共享锁，多个事务可以同时持有同一行的共享锁，但不能加排他锁。

### 排他锁（Exclusive Lock / X Lock）

写锁。事务修改一行数据时加排他锁，排他锁和其他任何锁互斥。

### 意向锁（Intention Lock）

表级锁，表示事务即将在某一行的某列上加锁。InnoDB 自动加的，分为 IS（意向共享锁）和 IX（意向排他锁）。方便表锁和行锁的兼容性判断。

### 死锁（Deadlock）

两个或多个事务相互持有对方需要的锁，形成循环等待。数据库系统通常通过死锁检测（超时检测或等待图检测）来发现死锁，然后回滚代价最小的事务来解除死锁。

### 连接池（Connection Pool）

数据库连接的缓存池。频繁创建和销毁数据库连接非常消耗资源，连接池预先创建一批连接放在池中，程序需要时从池中取用，用完后归还而不是销毁。常见连接池：HikariCP、Druid、C3P0、DBCP。

### HikariCP

目前性能最好的 JDBC 连接池之一。Spring Boot 2.x 默认使用 HikariCP。特点是轻量、可靠、快速，配置简单。

### Druid

阿里巴巴开源的数据库连接池，除了连接池功能外还提供强大的监控功能：SQL 防火墙、慢 SQL 记录、连接泄漏检测等。国内使用非常广泛。

### SQL 注入（SQL Injection）

一种安全攻击手段。通过在用户输入中注入恶意 SQL 来破坏原有 SQL 的语义。比如拼接字符串时用户输入 `' OR '1'='1` 可能导致身份验证被绕过。防范措施：使用预编译语句（PreparedStatement）、严格过滤输入参数。

### ORM 框架

对象关系映射框架，前面框架章节已讲过。

### 分库分表

当单表数据量太大或单机数据库扛不住时，把数据拆分到多个库/表中：

- **水平分表**：把同一张表的数据按行拆分到多个表（比如按用户 ID 取模）
- **垂直分表**：把一张表的字段拆到多个表（比如把大字段拆分出去）
- **分库**：把表拆分到不同的数据库实例中

常用中间件：ShardingSphere、MyCat。

### 读写分离

主库负责写操作，从库负责读操作，通过主从复制保持数据同步。这是缓解数据库读压力的经典方案，通常配合连接池（如 ShardingSphere-JDBC）使用。

### 数据库连接池

见"连接池"。

---

## 49.7 网络与分布式术语

### TCP（Transmission Control Protocol）

传输控制协议，面向连接的可靠传输协议。三次握手建立连接，四次挥手断开连接。TCP 提供流量控制、拥塞控制、差错校验，保证数据按顺序、不丢失、不重复地到达。HTTP、HTTPS、FTP 都基于 TCP。

### UDP（User Datagram Protocol）

用户数据报协议，无连接、不可靠的传输协议。不保证数据一定能到达，也不保证到达顺序。但速度比 TCP 快，开销小。DNS 查询、视频流、实时游戏等场景常用 UDP。

### HTTP（HyperText Transfer Protocol）

超文本传输协议，无状态的应用层协议。定义了客户端和服务器之间的请求-响应模型。HTTP/1.0 每次请求都要建立 TCP 连接，HTTP/1.1 增加了 keep-alive 持久连接，HTTP/2 增加了多路复用、头部压缩，HTTP/3 基于 QUIC（UDP）。

### HTTPS

HTTP + TLS/SSL，在 HTTP 外面加了一层加密层。传输内容加密，防止中间人攻击和数据窃听。证书认证在 TLS 握手阶段完成，之后对称加密传输数据。

### Socket

网络编程的抽象概念，代表了一个网络连接的端点。应用程序通过 Socket 向网络写入或读取数据。Java 中使用 java.net.Socket（客户端）和 java.net.ServerSocket（服务端）来进行 Socket 编程。

### 四次挥手（Four-Way Handshake）

TCP 断开连接的过程：主动关闭方发送 FIN → 被动关闭方回复 ACK → 被动关闭方发送 FIN → 主动关闭方回复 ACK。为什么是四次？因为 TCP 是全双工的，每一方的关闭都需要单独确认。

### 三次握手（Three-Way Handshake）

TCP 建立连接的过程：客户端发送 SYN → 服务器回复 SYN+ACK → 客户端发送 ACK。为什么不是两次？三次是确认双方都有发送和接收能力的最小次数。

### 序列化（Serialization）

把 Java 对象转换为字节流的过程，可以存储到磁盘或通过网络传输。反序列化就是从字节流恢复出对象。常见序列化协议：Java 原生序列化（ObjectOutputStream，兼容性最好但效率低且不安全）、JSON（文本格式，人类友好）、Protobuf（Google 高效二进制协议）、Kryo（高性能）。

### REST（Representational State Transfer）

一种架构风格，不是协议。REST 强调无状态、统一接口、资源寻址、可缓存。符合 REST 约束的 API 叫 RESTful API。

### RPC（Remote Procedure Call）

远程过程调用。让你像调用本地方法一样调用远程服务器上的方法，对调用方屏蔽了网络细节。Dubbo、gRPC、Thrift 都是 RPC 框架。

### gRPC

Google 开源的高性能 RPC 框架，基于 HTTP/2 协议和 Protocol Buffers 序列化协议。支持多语言、双向流、流控等高级特性。相比 REST，gRPC 在微服务内部通信中效率更高。

### 分布式系统

由多个独立节点（服务器）组成的系统，对外表现为一个整体。节点之间通过网络通信协调。分布式系统的优势是横向扩展能力强，但面临 CAP 理论、网络延迟、分布式事务等挑战。

### CAP 定理

分布式系统的基本定理：一个分布式系统不可能同时满足一致性（Consistency）、可用性（Availability）和分区容错性（Partition tolerance）。最多只能同时满足其中两个。实际工程中通常在 C 和 A 之间做权衡——CP 系统优先保证一致，AP 系统优先保证可用。

### BASE 理论

对 CAP 定理的补充和实践指导：Basically Available（基本可用）、Soft state（软状态）、Eventually consistent（最终一致性）。BASE 理论告诉我们：不需要实时一致，只要最终一致就行。这为最终一致性系统提供了理论依据。

### 一致性哈希（Consistent Hashing）

分布式缓存/存储系统中常用的哈希算法。解决了普通哈希在节点增减时大量数据需要重新映射的问题。一致性哈希把哈希值空间组织成一个环，每个节点映射到环上一点，数据根据哈希值落在顺时针方向的第一个节点上。节点增减时影响范围最小化。

### 负载均衡（Load Balancing）

把请求分配到多个服务器上，避免单点过载。负载均衡器可以工作在四层（TCP/UDP）或七层（HTTP）。常用算法：轮询、加权轮询、最少连接、IP 哈希。常见组件：Nginx（反向代理 + 七层负载均衡）、LVS（四层负载均衡）、Ribbon（客户端负载均衡）、Gateway（Spring Cloud 的网关层）。

### CDN（Content Delivery Network）

内容分发网络。通过在全球部署边缘节点，把静态资源缓存到离用户最近的节点，减少访问延迟。比如你的图片、视频、JS/CSS 文件可以放在 CDN 上，用户就近获取，访问速度飞快。

### DNS（Domain Name System）

域名系统，把域名解析成 IP 地址。层层递归查询：浏览器 → 本地 DNS 缓存 → 根域名服务器 → 顶级域名服务器 → 权威域名服务器。DNS 污染和劫持是常见的安全问题。

### 正向代理 vs 反向代理

- **正向代理**：代表客户端向服务器发请求，服务器不知道真实客户端是谁。VPN 就是正向代理
- **反向代理**：代表服务器接收客户端请求，客户端不知道真实服务器是谁。Nginx 就是反向代理

### 限流（Rate Limiting）

限制单位时间内的请求数量，保护系统不被冲垮。常用算法：

- **计数器算法**：最简单的滑动窗口
- **令牌桶算法**：以固定速率往桶里放令牌，请求来了先取令牌，取到才能处理。Redis 的令牌桶实现用得很多
- **漏桶算法**：请求以任意速率进入漏桶，漏桶以固定速率漏出，超出容量就丢弃

### 熔断（Circuit Breaker）

当某个服务故障率超过阈值时，"熔断器"打开，后续请求直接返回降级结果而不真正调用故障服务。一段时间后熔断器进入半开状态，放少量请求试试，如果成功就关闭熔断器恢复正常，否则继续保持打开。防止故障蔓延。

### 降级（Degradation）

在系统压力过大或依赖服务不可用时，主动关闭部分非核心功能，保证核心功能正常运行。比如商品详情页依赖商品服务、库存服务、评价服务，库存服务挂了就把库存显示为"有货"而不是报错，牺牲实时性换取可用性。

### 幂等性（Idempotency）

一个操作执行一次和执行多次的效果相同。分布式系统中，网络调用可能因为超时而重试，如果操作不幂等，重试就会导致问题。HTTP 的 GET、PUT、DELETE 是幂等的，POST 不是。保证幂等的常用方法：唯一键 + 去重表。

### 分布式事务

跨多个数据库或服务的事务。单个数据库的事务可以靠 ACID 保证，但跨库就不行了。常见的分布式事务解决方案：

- **两阶段提交（2PC）**：协调者让所有参与者 Prepare，成功后统一 Commit。缺点是同步阻塞、单点故障、数据不一致风险
- **TCC（Try-Confirm-Cancel）**：业务层面的补偿模式，把准备和提交/回滚都交给业务代码
- **本地消息表**：把事务消息存在本地数据库，通过定时任务或 MQ 驱动最终一致性
- **Saga 模式**：把大事务拆成多个本地事务，每个子事务有正向和补偿操作，按顺序执行

### Seata

阿里巴巴开源的分布式事务解决方案。支持 AT、TCC、Saga、XA 四种模式。AT 模式是全自动的，对业务零侵入，使用最广泛。

### 消息队列（Message Queue）

异步通信的中间件。生产者把消息发到队列，消费者从队列取消息处理。优点是解耦、削峰、异步。常见的消息队列：RabbitMQ（功能丰富、路由灵活）、Kafka（高吞吐、日志场景）、RocketMQ（阿里巴巴开源、事务消息）、ActiveMQ（老牌）。

### RabbitMQ

使用最广泛的开源消息队列之一。核心概念：Producer（生产者）、Consumer（消费者）、Exchange（交换机）、Queue（队列）、Binding（绑定）。Exchange 是核心，它决定消息路由到哪个队列。路由方式灵活：direct、fanout、topic、headers。

### Kafka

高吞吐量、低延迟的分布式消息系统。设计用于处理日志和流数据。核心概念：Topic（主题）、Partition（分区）、Producer（生产者）、Consumer（消费者）、Consumer Group（消费者组）。消息持久化到磁盘，支持消息回溯（从任意 offset 消费）。

### RocketMQ

阿里巴巴开源的分布式消息中间件，对标 Kafka。比 Kafka 多了事务消息、延迟消息、顺序消息等企业级特性。在国内电商、金融场景用得很多。

### 消息堆积

消费者处理速度跟不上生产者发送速度，消息在队列中积压。短时间消息堆积是正常的，但长时间堆积可能导致内存溢出或消息丢失。需要监控堆积情况，增加消费者或优化消费逻辑。

### 顺序消息

消息按发送顺序被消费。比如下单、支付、发货、收货这个流程，每个步骤的消息必须按顺序处理。Kafka 的 Partition 可以保证单分区内有序，全局有序需要单 Partition。

### 分布式锁

多个进程/线程竞争同一把锁，需要分布式协调。单机锁（synchronized、ReentrantLock）只能控制单个 JVM 内的线程。Redis 的 SETNX + 过期时间、ZooKeeper 的临时有序节点、数据库唯一索引都可以实现分布式锁。

### Redis

最流行的内存数据库，支持多种数据结构（String、Hash、List、Set、ZSet、Geo、Stream）。常用于：缓存、分布式锁、计数器、排行榜、消息队列（Stream）、限流（滑动窗口或令牌桶）。

### 缓存穿透、缓存击穿、缓存雪崩

- **缓存穿透**：查询一个数据库和缓存中都不存在的 key，每次都打到数据库。解决方案：布隆过滤器、缓存空值
- **缓存击穿**：某个热点 key 过期瞬间，大量请求同时打到数据库。解决方案：互斥锁、永不过期 + 异步更新
- **缓存雪崩**：大量 key 同时过期，或者 Redis 宕机，导致大量请求打到数据库。解决方案：过期时间加随机值、Redis 高可用 + 限流

### 布隆过滤器（Bloom Filter）

一个巧妙的数据结构，用来判断一个元素"一定不存在"或"可能存在"。利用多个哈希函数将元素映射到位数组中。空间效率高，但可能有假阳性（不存在的元素判断为存在）。非常适合解决缓存穿透问题。

### 服务注册与发现

微服务架构中，服务实例动态增减，需要一个"电话簿"让服务之间能互相找到。原理：每个服务启动时向注册中心注册自己的地址，停止时注销。调用方从注册中心获取服务实例列表。常见实现：Eureka（已停止维护）、Nacos、Consul、ZooKeeper。

### ZooKeeper

分布式协调服务。提供：配置管理、分布式锁、命名服务、选主（Leader Election）等功能。虽然可以用作注册中心，但现在更推荐 Nacos 或 Consul。ZK 的 ZAB 协议保证了强一致性。

### Sentinel

见"49.5 框架术语"中的 Sentinel。

---

## 本章小结

本章按七大类别系统梳理了 Java 学习和开发中最核心的术语：

1. **Java 基础术语**：涵盖了面向对象核心概念、关键字、反射、泛型等 JDK 层面的基本功
2. **集合框架术语**：重点解析了 List、Set、Map 三大体系的底层原理和选型依据
3. **并发编程术语**：从线程创建方式到 JUC 并发工具类，从锁机制到 JMM 模型，是进阶必备
4. **JVM 术语**：深入理解了内存区域、GC 算法与收集器、类加载机制等面试高频考点
5. **框架术语**：以 Spring 生态为核心，辐射到持久化框架和微服务组件
6. **数据库术语**：从 SQL 基础到事务隔离、索引原理，再到连接池和分库分表
7. **网络与分布式术语**：补全了 RPC、分布式事务、消息队列、CAP/BASE 等现代架构知识

这些术语不是孤立的，它们彼此关联、互相支撑。建议结合代码实践和项目经验来加深理解，死记硬背不如动手实验。下一章我们将进入新的专题，继续深化对 Java 各领域知识的理解。

> 📺 配套视频正在持续更新中，欢迎关注！
