+++
title = "第10章 动态内存管理"
weight = 100
date = "2026-03-29T21:03:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++
# 第10章 动态内存管理

## 10.1 C风格内存管理：malloc/free

malloc和free是C语言的内存管理函数，也是C++兼容C遗产的一部分。但在现代C++中，我们应该尽量避免它们——就像你明明有自动挡汽车，却非要开个手动挡去兜风，虽然技术上可行，但纯属给自己找麻烦。

```cpp
#include <iostream>
#include <cstdlib>

int main() {
    // malloc: 分配指定字节的内存，返回void*
    // free: 释放malloc分配的内存
    
    // 分配5个int的空间
    int* arr = static_cast<int*>(malloc(sizeof(int) * 5));
    
    if (arr == nullptr) {
        std::cerr << "Memory allocation failed!" << std::endl;
        return 1;
    }
    
    // 使用分配的内存
    for (int i = 0; i < 5; ++i) {
        arr[i] = (i + 1) * 10;
    }
    
    std::cout << "Allocated array: ";
    for (int i = 0; i < 5; ++i) {
        std::cout << arr[i] << " ";  // 输出: Allocated array: 10 20 30 40 50
    }
    std::cout << std::endl;
    
    // 释放内存
    free(arr);
    arr = nullptr;  // 避免悬空指针
    
    // malloc不会调用构造函数！
    // free不会调用析构函数！
    // 这是它们和new/delete的主要区别
    
    std::cout << "malloc/free demo complete" << std::endl;
    
    return 0;
}
```

### malloc/free与new/delete的区别

想象malloc是个冷血的机器人，它只负责给你一块原始的土地（内存），但不会帮你盖房子（构造）。而new则是个全能管家，不仅给你土地，还帮你盖好房子、接通水电（构造+初始化）。

```cpp
#include <iostream>

struct Point {
    int x, y;
    Point() : x(0), y(0) { std::cout << "Point() called" << std::endl; }
    ~Point() { std::cout << "~Point() called" << std::endl; }
};

int main() {
    std::cout << "Using malloc/free:" << std::endl;
    Point* p1 = static_cast<Point*>(malloc(sizeof(Point)));
    // p1->x;  // 未初始化！构造函数没被调用！
    free(p1);
    
    std::cout << "\nUsing new/delete:" << std::endl;
    Point* p2 = new Point();  // 构造函数被调用
    p2->x = 10;  // 成员已初始化
    delete p2;  // 析构函数被调用
    
    // new/delete会调用构造函数和析构函数
    // malloc/free不会
    
    return 0;
}
```

> **冷知识**：malloc诞生于1973年，比C++的年龄还大40多岁！它退休了但还在加班，C++社区真是压榨老年员工的典范。

## 10.2 C++风格内存管理：new/delete

new是C++的"new"（新的），也是"new"（新手的）——新手喜欢用它，因为它比malloc更智能，会自动调用构造函数。就像新款扫地机器人，不仅能扫，还会自己倒垃圾（析构）。

```cpp
#include <iostream>

int main() {
    // new: 分配内存并构造对象
    // delete: 析构对象并释放内存
    
    // 分配单个对象
    int* p = new int(42);  // 分配并初始化为42
    std::cout << "*p = " << *p << std::endl;  // 输出: *p = 42
    delete p;
    p = nullptr;
    
    // 分配内置类型（不初始化）
    int* uninit = new int;
    std::cout << "*uninit (uninitialized) = " << *uninit << std::endl;  // 输出: 垃圾值
    
    // 分配内置类型（值初始化）
    int* valueInit = new int();  // 括号初始化为0
    std::cout << "*valueInit (value-initialized) = " << *valueInit << std::endl;  // 输出: *valueInit (value-initialized) = 0
    delete valueInit;
    
    // 分配数组
    int* arr = new int[5];
    for (int i = 0; i < 5; ++i) arr[i] = i * 10;
    std::cout << "arr[2] = " << arr[2] << std::endl;  // 输出: arr[2] = 20
    delete[] arr;  // 数组要用delete[]
    
    // new失败会抛std::bad_alloc异常
    // C++11后可以用nothrow版本来避免异常
    // int* p2 = new (std::nothrow) int;  // 失败返回nullptr
    
    return 0;
}
```

> **警告**：new和delete必须成对出现，否则就是"内存泄漏"——你的程序会像漏水的桶一样，慢慢消耗系统内存，直到被操作系统Kill掉（OOM - Out Of Memory）。

## 10.3 new[]/delete[]与数组

### 数组new/delete匹配问题

这是C++中最容易踩的坑之一！new[]和delete必须配套使用，就像筷子和碗——用筷子吃饭没问题，用筷子喝汤...也不是不行，但总觉得哪里不对。

```cpp
#include <iostream>

int main() {
    // 必须匹配！
    // new[] 配 delete[]
    // new    配 delete
    
    // 正确配对
    int* arr1 = new int[10];
    delete[] arr1;  // 正确
    
    int* obj1 = new int[5];
    delete[] obj1;  // 正确
    
    // 错误配对（危险！）
    // int* arr2 = new int[10];
    // delete arr2;  // 错误！只释放了第一个元素！
    
    // int* obj2 = new int;
    // delete[] obj2;  // 错误！行为未定义
    
    // 建议：优先使用std::vector或std::array
    // 它们会自动管理内存，永远不会有配对问题
    
    std::cout << "new[]/delete[] matching demo" << std::endl;
    
    return 0;
}
```

> **血泪教训**：曾经有个程序员在深夜加班，不小心写了`delete arr`而不是`delete[] arr`。第二天服务器内存泄漏，全公司断电排查三小时。记住这个故事，不要成为那个人。

## 10.4 定位new（placement new）

定位new是C++中的"精装修二手房"——不是给你新房子，而是让你在已有的房子里装修（构造）对象。它不分配内存，只负责在指定地址调用构造函数。

用大白话说：`new(p) T(args)`的意思是："嘿，在地址p这个地方，给我建一个T类型的对象，用args初始化。"

```cpp
#include <iostream>
#include <new>  // 必须包含placement new

int main() {
    // 定位new：在指定内存地址构造对象
    // 不分配内存，只调用构造函数
    
    // 1. 在栈上
    struct Tracer {
        int value;
        Tracer(int v) : value(v) { std::cout << "Tracer(" << value << ") constructed" << std::endl; }
        ~Tracer() { std::cout << "Tracer(" << value << ") destroyed" << std::endl; }
    };
    
    alignas(Tracer) char buffer[sizeof(Tracer)];
    Tracer* p = new(buffer) Tracer(42);  // 在buffer地址构造Tracer
    std::cout << "p->value = " << p->value << std::endl;  // 输出: p->value = 42
    p->~Tracer();  // 手动调用析构函数（placement new不自动调用）
    
    // 2. 预分配的内存池
    static char memoryPool[1024];
    static size_t offset = 0;
    
    template<typename T>
    T* allocate() {
        T* ptr = new(memoryPool + offset) T();
        offset += sizeof(T);
        return ptr;
    }
    
    // 使用示例
    // int* a = allocate<int>();
    // double* b = allocate<double>();
    
    // 定位new用于内存池、嵌入式系统、性能关键代码
    
    std::cout << "Placement new demo complete" << std::endl;
    
    return 0;
}
```

> **应用场景**：游戏开发中，对象池（Object Pool）模式就用定位new——预先分配一大块内存，需要时在原地构造对象，避免频繁的malloc/free导致的内存碎片化。

## 10.5 内存泄漏与野指针

### 检测工具（Valgrind、AddressSanitizer）

内存泄漏（Memory Leak）就像你家的水龙头漏水——每滴一滴，看起来没什么大不了，但月底水费账单会让你怀疑人生。野指针（Dangling Pointer）则像是一把不知道通向哪里的钥匙，捅进去可能开门，也可能捅破邻居的鱼缸。

```cpp
#include <iostream>

/*
 * 内存泄漏检测工具介绍：
 * 
 * 1. Valgrind (Linux/macOS)
 *    命令行: valgrind --leak-check=full ./program
 *    能检测：内存泄漏、越界访问、未初始化内存等
 * 
 * 2. AddressSanitizer / MSan / UBSan (gcc/clang)
 *    编译时加: -fsanitize=address
 *    运行更快，适合生产环境
 * 
 * 3. Visual Studio (Windows)
 *    CRT库自带内存调试功能
 *    #define _CRTDBG_MAP_ALLOC
 *    使用 _CrtCheckMemory()
 * 
 * 4. Dr. Memory (Windows/Linux)
 *    跨平台，类似Valgrind但更轻量
 */

int main() {
    // 模拟内存泄漏
    while (false) {  // 用while(false)确保只执行一次
        int* leak = new int[100];
        // 忘记delete!
    }
    
    // 模拟野指针
    int* dangling = new int(10);
    delete dangling;
    // dangling现在悬空，访问它会崩溃
    
    std::cout << "Memory leak detection tools:" << std::endl;
    std::cout << "1. Valgrind (Linux)" << std::endl;
    std::cout << "2. AddressSanitizer (gcc/clang)" << std::endl;
    std::cout << "3. Dr. Memory (cross-platform)" << std::endl;
    
    return 0;
}
```

> **Debug神器**：VS Code配合 AddressSanitizer，简直是内存问题的"显微镜"。在cmake中加一行`set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fsanitize=address")`，然后正常运行——内存问题一览无余！

## 10.6 智能指针概述

智能指针是C++11引入的"自动还车租赁"——你借一辆车（指针），用完不用自己还（delete），系统自动收回去。完美解决"我到底什么时候该还车"的哲学问题。

智能指针三种类型：

- **unique_ptr**：独占所有权，就像你的专属自行车，别人想骑？门都没有，只能过户（移动）给你。

- **shared_ptr**：共享所有权，像共享单车，多个人可以同时骑，每多一个人就多一个记录，用完随便谁还都行。

- **weak_ptr**：弱引用，像自行车使用说明书——你可以看（访问），但不能骑（不增加引用计数），而且要确认车还在不在（解决循环引用）。

```cpp
#include <iostream>
#include <memory>

int main() {
    // 智能指针三种类型：
    // 1. std::unique_ptr: 独占所有权，唯一指针
    // 2. std::shared_ptr: 共享所有权，引用计数
    // 3. std::weak_ptr: 弱引用，不增加计数，解决循环引用
    
    std::cout << "Smart pointers overview:" << std::endl;
    std::cout << "- unique_ptr: exclusive ownership" << std::endl;
    std::cout << "- shared_ptr: shared ownership with reference counting" << std::endl;
    std::cout << "- weak_ptr: non-owning reference to shared_ptr" << std::endl;
    
    return 0;
}
```

## 10.7 std::unique_ptr（C++11）

### 独占所有权语义

unique_ptr是"霸道总裁"型指针——一旦拥有，绝对独占。不允许任何形式的复制（拷贝构造、拷贝赋值），只能移动（move）。就像你的初恋，过去了就过去了，不能脚踏两只船。

```cpp
#include <iostream>
#include <memory>

int main() {
    // unique_ptr: 独占所有权，同一时间只能有一个指针拥有对象
    // 不能拷贝，只能移动
    
    std::unique_ptr<int> p1 = std::make_unique<int>(42);
    std::cout << "*p1 = " << *p1 << std::endl;  // 输出: *p1 = 42
    
    // 移动语义
    std::unique_ptr<int> p2 = std::move(p1);  // p1变成空，p2接管
    // std::cout << "*p1 = " << *p1 << std::endl;  // 危险！p1已经为空
    std::cout << "*p2 = " << *p2 << std::endl;  // 输出: *p2 = 42
    
    // unique_ptr作为函数参数
    void process(std::unique_ptr<int> p) {
        std::cout << "Processing: " << *p << std::endl;
    }
    
    auto up = std::make_unique<int>(100);
    // process(up);  // 错误！不能拷贝unique_ptr
    process(std::move(up));  // OK，移动
    // up现在为空
    
    // 自动释放
    std::cout << "unique_ptr auto-deletes when out of scope" << std::endl;
    
    return 0;
}
```

> **哲理**：unique_ptr教会我们一个人生道理——不是你的，就别强求；是你的，记得珍惜（及时释放）。

### 自定义删除器

unique_ptr不仅霸道，还很包容——你可以自定义它的"清理方式"。默认是delete，但你可以改成fclose（关闭文件）、free（释放C风格内存）、甚至自定义逻辑。

```cpp
#include <iostream>
#include <memory>
#include <fstream>

int main() {
    // unique_ptr支持自定义删除器
    // 用于文件句柄、线程、C风格数组等
    
    // 方式1：函数指针删除器
    std::unique_ptr<FILE, decltype(&fclose)> 
        file(fopen("test.txt", "w"), fclose);
    
    if (file) {
        fprintf(file.get(), "Hello from unique_ptr!\n");
        // 自动调用fclose
    }
    
    // 方式2：lambda删除器
    auto deleter = [](int* p) {
        std::cout << "Custom deleting int: " << *p << std::endl;
        delete p;
    };
    
    std::unique_ptr<int, decltype(deleter)> 
        custom(new int(42), deleter);
    
    // 数组的unique_ptr
    std::unique_ptr<int[]> arr(new int[5]);
    for (int i = 0; i < 5; ++i) arr[i] = i * 10;
    std::cout << "arr[3] = " << arr[3] << std::endl;  // 输出: arr[3] = 30
    // 自动调用delete[]
    
    // C++17: std::unique_ptr<T[]>
    // C++20: std::unique_ptr<std::byte[]> 用于裸内存
    
    return 0;
}
```

## 10.8 std::shared_ptr（C++11）

### 引用计数原理

shared_ptr是"合租公寓"型指针——多人共享一套房（对象），用"引用计数"记录有多少室友（指针）。最后一个离开的室友负责关灯（释放内存）。

```cpp
#include <iostream>
#include <memory>

int main() {
    // shared_ptr: 共享所有权，使用引用计数
    // 最后一个shared_ptr销毁时，对象才被删除
    
    auto sp1 = std::make_shared<int>(42);  // 引用计数=1
    std::cout << "sp1 ref count: " << sp1.use_count() << std::endl;  // 输出: 1
    
    {
        auto sp2 = sp1;  // 拷贝，引用计数=2
        std::cout << "sp1 ref count: " << sp1.use_count() << std::endl;  // 输出: 2
        std::cout << "*sp2 = " << *sp2 << std::endl;  // 输出: *sp2 = 42
    }  // sp2销毁，引用计数=1
    
    std::cout << "sp1 ref count after scope: " << sp1.use_count() << std::endl;  // 输出: 1
    
    // 移动不增加计数
    auto sp3 = std::move(sp1);  // sp1变为空，sp3接管
    std::cout << "sp3 ref count: " << sp3.use_count() << std::endl;  // 输出: 1
    
    return 0;
}
```

### 循环引用问题

shared_ptr有个致命弱点——**循环引用**。想象两个互相依赖的人，谁都不愿意先放手，结果就是僵持不下（内存泄漏）。

```cpp
#include <iostream>
#include <memory>

struct Node {
    int value;
    std::shared_ptr<Node> next;  // shared_ptr会形成循环引用！
    // std::weak_ptr<Node> prev;  // 解决方案：把next或prev改成weak_ptr
    
    Node(int v) : value(v) {
        std::cout << "Node(" << value << ") created" << std::endl;
    }
    ~Node() {
        std::cout << "Node(" << value << ") destroyed" << std::endl;
    }
};

int main() {
    // 循环引用导致内存泄漏！
    auto head = std::make_shared<Node>(1);
    auto tail = std::make_shared<Node>(2);
    
    head->next = tail;  // head引用tail
    tail->next = head;  // tail引用head -> 循环！
    // 引用计数永远无法降到0，无法销毁！
    
    std::cout << "Circular reference prevents cleanup!" << std::endl;
    // head和tail超出作用域，但引用计数都是1（互相引用）
    // 内存泄漏！
    
    return 0;
}
```

> **解决方案**：用weak_ptr打破循环！详见下一节。

## 10.9 std::weak_ptr（C++11）

### 打破循环引用

weak_ptr是shared_ptr的"备胎"——它可以观察shared_ptr指向的对象，但不拥有（不增加引用计数）。当你需要访问对象时，先用`lock()`检查对象是否还活着，然后升级为shared_ptr使用。

简单说：weak_ptr就是那个"我不占你便宜，但你有事我可以帮忙"的君子型指针。

```cpp
#include <iostream>
#include <memory>

struct Node {
    int value;
    std::shared_ptr<Node> next;
    std::weak_ptr<Node> prev;  // 用weak_ptr打破循环！
    
    Node(int v) : value(v) {
        std::cout << "Node(" << value << ") created" << std::endl;
    }
    ~Node() {
        std::cout << "Node(" << value << ") destroyed" << std::endl;
    }
};

int main() {
    auto head = std::make_shared<Node>(1);
    auto tail = std::make_shared<Node>(2);
    
    head->next = tail;
    tail->prev = head;  // weak_ptr不增加计数！
    
    std::cout << "head ref count: " << head.use_count() << std::endl;  // 输出: 1
    std::cout << "tail ref count: " << tail.use_count() << std::endl;  // 输出: 1
    
    // weak_ptr使用前需要检查和升级
    if (auto p = tail->prev.lock()) {  // lock()返回shared_ptr或nullptr
        std::cout << "tail->prev.value = " << p->value << std::endl;
        // 输出: tail->prev.value = 1
    }
    
    return 0;
}
```

## 10.10 std::make_unique（C++14）与std::make_shared（C++11）

### 异常安全优势

make_unique和make_shared是创建智能指针的"官方推荐方式"。它们比直接用new创建智能指针更安全、更高效。

```cpp
#include <iostream>
#include <memory>

struct Widget {
    Widget() { std::cout << "Widget constructed" << std::endl; }
    ~Widget() { std::cout << "Widget destructed" << std::endl; }
};

void processAndThrow() {
    // 危险写法：new Widget()分配内存后，如果构造函数抛出异常，
    // 我们根本得不到w指针（w未定义），之前分配的内存就泄漏了！
    Widget* w = new Widget();  // 如果构造失败，分配的内存泄漏！
    throw std::runtime_error("Oops!");
    delete w;  // 永远不会执行
}

void processSafely() {
    // 安全写法：make_unique自动管理
    auto w = std::make_unique<Widget>();  // 构造Widget
    // 如果make_unique之后抛出异常，unique_ptr自动释放
    // RAII保证！
}

int main() {
    // make_unique vs new
    // 1. 更简洁
    auto p1 = std::make_unique<int>(42);
    
    // int* p2 = new int(42);  // 更长
    
    // 2. 异常安全
    try {
        // processAndThrow();  // 会泄漏Widget
        processSafely();  // 不会泄漏
    } catch (const std::exception& e) {
        std::cout << "Caught: " << e.what() << std::endl;
    }
    
    // 3. make_shared只分配一次内存（控制块+对象一起）
    // new+shared_ptr需要两次（对象一次，控制块一次）
    auto sp = std::make_shared<int>(100);
    std::cout << "*sp = " << *sp << std::endl;  // 输出: *sp = 100
    
    return 0;
}
```

> **性能提示**：make_shared比`shared_ptr<T>(new T)`更高效，因为前者一次分配（对象+控制块），后者需要两次。想象你去超市买菜——一次买齐 vs 分五次去买。

## 10.11 自定义删除器

shared_ptr同样支持自定义删除器，用法和unique_ptr类似，但有一个关键区别：**删除器不是shared_ptr类型的一部分**（unique_ptr的删除器是类型的一部分）。

```cpp
#include <iostream>
#include <memory>
#include <functional>

int main() {
    // shared_ptr也支持自定义删除器
    
    // 方式1：lambda
    auto deleter = [](FILE* f) {
        std::cout << "Closing file!" << std::endl;
        if (f) fclose(f);
    };
    
    std::shared_ptr<FILE> filePtr(
        fopen("test.txt", "w"),
        deleter
    );
    
    if (filePtr) {
        fprintf(filePtr.get(), "Hello!\n");
    }  // 自动调用deleter
    
    // 方式2：函数指针
    void (*deleterFunc)(FILE*) = [](FILE* f) {
        if (f) fclose(f);
    };
    
    // 注意：shared_ptr的删除器不是类型的一部分
    // 不同删除器的shared_ptr仍然是相同类型（和unique_ptr不同）
    // shared_ptr<T> deleter只是构造时的参数，类型始终是shared_ptr<T>
    
    std::cout << "Custom deleter demo complete" << std::endl;
    
    return 0;
}
```

## 10.12 内存对齐与对齐new（C++11）

内存对齐（Memory Alignment）是计算机的基本概念——CPU访问内存时，希望数据地址是某个数字的倍数。这就像你希望抽屉的高度是整数厘米，这样东西才能整齐放进去。

```cpp
#include <iostream>
#include <cstdlib>
#include <cstdalign>

struct AlignedData {
    double d;
    int i;
};

int main() {
    // 内存对齐：数据在内存中的地址必须是某个值的倍数
    // 影响：性能、硬件要求
    
    std::cout << "Alignment of basic types:" << std::endl;
    std::cout << "char:   " << alignof(char) << std::endl;    // 输出: 1
    std::cout << "short:  " << alignof(short) << std::endl;   // 输出: 2
    std::cout << "int:    " << alignof(int) << std::endl;      // 输出: 4
    std::cout << "double: " << alignof(double) << std::endl;  // 输出: 8
    
    // alignas指定对齐要求
    alignas(16) char buffer[32];  // buffer地址必须是16的倍数
    
    // aligned_alloc (C11/C++17)
    // void* aligned_alloc(size_t alignment, size_t size);
    
    // 动态分配对齐内存
    void* aligned = nullptr;
    if (posix_memalign(&aligned, 32, 64) == 0) {
        std::cout << "Aligned memory at: " << aligned << std::endl;
        // 地址是32的倍数
        std::free(aligned);
    }
    
    // C++17: std::aligned_alloc
    // double* arr = static_cast<double*>(std::aligned_alloc(alignof(double), sizeof(double) * 10));
    
    std::cout << "Memory alignment demo complete" << std::endl;
    
    return 0;
}
```

> **为什么重要**：未对齐的内存访问可能导致性能下降（在某些架构上甚至会崩溃）。SSE指令集要求16字节对齐，AVX要求32字节对齐。所以写高性能代码时，内存对齐是必修课。

## 10.13 内存管理最佳实践

### 优先使用智能指针

这是最重要的最佳实践，没有之一：**忘掉裸指针，用智能指针**。就像忘掉手动挡，学会开自动挡。

```cpp
#include <iostream>
#include <memory>
#include <vector>

class Resource {
public:
    Resource() { std::cout << "Resource acquired" << std::endl; }
    ~Resource() { std::cout << "Resource released" << std::endl; }
};

int main() {
    // 最佳实践1：优先使用智能指针而不是裸指针
    
    // 独占资源：用unique_ptr
    auto unique = std::make_unique<Resource>();
    
    // 共享资源：用shared_ptr
    auto shared1 = std::make_shared<Resource>();
    auto shared2 = shared1;
    
    // 最佳实践2：用make_unique/make_shared而不是new
    // auto p1 = std::unique_ptr<int>(new int(42));  // 不推荐
    auto p2 = std::make_unique<int>(42);  // 推荐
    
    // 最佳实践3：避免返回裸指针，用智能指针
    // std::unique_ptr<Widget> createWidget();  // 好！
    // Widget* createWidget();  // 差！调用者可能忘记delete
    
    // 最佳实践4：使用容器而不是动态数组
    std::vector<int> vec(100);  // 自动管理内存
    // int* arr = new int[100];  // 不推荐
    
    std::cout << "Best practices demo complete" << std::endl;
    
    return 0;
}
```

### RAII原则

RAII（Resource Acquisition Is Initialization，资源获取即初始化）是C++的核心编程范式。它的思想是：**资源的获取和释放与对象的构造/析构绑定**。

简单说：你在构造函数里"开门"（获取资源），在析构函数里"关门"（释放资源）。无论函数正常结束还是抛出异常，析构函数都会执行，资源一定会被释放。

```cpp
#include <iostream>
#include <memory>
#include <mutex>

// RAII: Resource Acquisition Is Initialization
// 资源获取即初始化
// 核心思想：资源的获取和释放与对象的构造/析构绑定

class MutexGuard {
    std::mutex& mutex_;
public:
    explicit MutexGuard(std::mutex& m) : mutex_(m) {
        mutex_.lock();
        std::cout << "Mutex locked" << std::endl;
    }
    ~MutexGuard() {
        mutex_.unlock();
        std::cout << "Mutex unlocked" << std::endl;
    }
};

std::mutex globalMutex;

void criticalSection() {
    MutexGuard guard(globalMutex);  // 锁在构造时获取
    // ... 做任何操作 ...
    // 无论是否抛出异常，析构函数都会解锁
}  // guard销毁，自动解锁

int main() {
    criticalSection();
    
    // C++11后有更方便的std::lock_guard和std::unique_lock
    {
        std::lock_guard<std::mutex> lock(globalMutex);
        std::cout << "Using lock_guard" << std::endl;
    }  // 自动解锁
    
    std::cout << "RAII principle ensures automatic cleanup" << std::endl;
    
    return 0;
}
```

> **RAII名言**："如果你还在手动管理资源，时代在抛弃你之前，不会和你说再见。"

## 本章小结

本章我们深入探讨了C++的动态内存管理，从古老的malloc/free到现代的智能指针，涵盖了以下核心知识点：

### 核心概念

1. **malloc/free**：C风格的内存管理函数，不调用构造/析构函数，已不推荐使用
2. **new/delete**：C++的内存管理运算符，会调用构造/析构函数
3. **new[]/delete[]**：数组版本的new和delete，必须严格匹配使用
4. **定位new（placement new）**：在预分配内存上构造对象，用于内存池等场景
5. **内存对齐**：数据地址必须是某个值的倍数，影响性能和硬件访问

### 智能指针家族

| 指针类型 | 所有权 | 拷贝行为 | 典型用途 |
|---------|--------|---------|---------|
| `unique_ptr` | 独占 | 不可拷贝，只能移动 | 单个对象的唯一所有权 |
| `shared_ptr` | 共享 | 可拷贝，引用计数 | 多个指针共享所有权 |
| `weak_ptr` | 无 | 可拷贝，不增加计数 | 打破循环引用，观察对象 |

### 最佳实践

1. **优先使用智能指针**：忘掉裸指针，让编译器帮你管理内存
2. **使用make_unique/make_shared**：更安全、更高效
3. **避免循环引用**：用weak_ptr打破循环
4. **遵循RAII原则**：资源获取即初始化，自动管理
5. **使用容器**：std::vector、std::array比动态数组更安全

> **终极忠告**：在现代C++中，手动`delete`一个指针已经成了一种"代码异味"（code smell）——除非你有极其特殊的理由，否则请把delete从你的代码库中驱逐出去。智能指针就是你最好的朋友！
