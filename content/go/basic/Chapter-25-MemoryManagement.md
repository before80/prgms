+++
title = "第25章 内存管理"
weight = 250
date = "2026-03-20T08:39:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++
# 第25章 内存管理

> Go语言以自动内存管理著称——你只管申请内存，不用操心释放，垃圾回收器（GC）会帮你搞定一切。就像有个贴心的管家，你吃完饭不用洗碗，管家会帮你处理。

## 25.1 内存分配

### 25.1.1 new 函数

`new(T)` 用于创建**值类型**的内存，它会分配内存并初始化为零值，返回 `*T`。

```go
package main

import "fmt"

func main() {
    // new(int) 分配一个int的内存，初始化为0
    p := new(int)
    fmt.Printf("*p = %d (零值)\n", *p) // *p = 0 (零值)

    // new(string) 分配字符串内存，初始化为空字符串
    s := new(string)
    fmt.Printf("*s = %q (零值)\n", *s) // *s = "" (零值)

    // new([5]int) 分配数组内存，所有元素初始化为0
    arr := new([5]int)
    fmt.Printf("*arr = %v (零值)\n", *arr) // *arr = [0 0 0 0 0] (零值)
}
```

**new vs 直接声明的区别：**

```go
p1 := new(int)    // 返回 *int，值为0
var p2 int         // 等价于 new(int)
```

### 25.1.2 make 函数

`make(T, ...)` 用于创建**引用类型**的内存：切片、map、channel。它会分配并初始化这些类型。

```go
package main

import "fmt"

func main() {
    // make([]int, 5) 创建切片：长度5，容量5，元素都是0
    s1 := make([]int, 5)
    fmt.Printf("s1: len=%d, cap=%d, value=%v\n", len(s1), cap(s1), s1) // s1: len=5, cap=5, value=[0 0 0 0 0]

    // make([]int, 3, 10) 创建切片：长度3，容量10
    // 前3个元素初始化为0，其余保留
    s2 := make([]int, 3, 10)
    fmt.Printf("s2: len=%d, cap=%d\n", len(s2), cap(s2)) // s2: len=3, cap=10

    // make(map[string]int) 创建空map
    m := make(map[string]int)
    m["Java"] = 98
    m["Go"] = 95
    fmt.Printf("m: %v\n", m) // m: map[Java:98 Go:95]

    // make(chan int) 创建无缓冲通道
    // make(chan int, 10) 创建缓冲通道，容量10
    ch1 := make(chan int)        // 无缓冲
    ch2 := make(chan int, 10)    // 有缓冲，容量10
    fmt.Printf("ch1: 无缓冲通道=%v\n", cap(ch1) == 0) // ch1: 无缓冲通道=true
    fmt.Printf("ch2: 有缓冲通道=%v, 容量=%d\n", cap(ch2) > 0, cap(ch2)) // ch2: 有缓冲通道=true, 容量=10
}
```

**make 能创建哪些类型？**

| 类型 | 示例 | 说明 |
|------|------|------|
| 切片 | `make([]int, 3, 10)` | 长度3，容量10 |
| Map | `make(map[string]int)` | 空map |
| Channel | `make(chan int, 5)` | 缓冲容量5 |

### 25.1.3 new vs make 对比

| 函数 | 适用类型 | 返回值 | 用途 |
|------|---------|--------|------|
| `new(T)` | 值类型 | `*T` | 分配并清零 |
| `make(T)` | 引用类型 | `T` | 分配并初始化 |

```go
package main

import "fmt"

type Person struct {
    Name string
    Age  int
}

func main() {
    // new 返回指针，适用于值类型
    p := new(Person)
    fmt.Printf("new(Person): %+v (指针)\n", p) // new(Person): &{Name:, Age:0} (指针)

    // make 返回值本身，适用于切片/map/channel
    s := make([]Person, 3)
    fmt.Printf("make([]Person, 3): len=%d\n", len(s)) // make([]Person, 3): len=3
}
```

---

## 25.2 垃圾回收

### 25.2.1 GC 工作原理

Go使用**三色标记并发GC**：

1. **白色**：未被访问的对象
2. **灰色**：已被访问但依赖未处理
3. **黑色**：已被访问且依赖已处理

GC开始时所有对象都是白色，扫描后变成灰色或黑色，最后白色对象被回收。

```go
package main

import (
    "fmt"
    "runtime"
)

func main() {
    stats := &runtime.MemStats{}
    runtime.ReadMemStats(stats)

    fmt.Printf("GC轮次: %d\n", stats.NumGC) // GC轮次: 0
    fmt.Printf("NextGC阈值: %.2f MB\n", float64(stats.NextGC)/1024/1024) // NextGC阈值: 4.00 MB
    fmt.Printf("当前活跃对象: %d\n", stats.Mallocs) // 当前活跃对象数量
}
```

**GC触发条件：**
- 内存达到阈值（NextGC）
- 定时触发（2分钟）
- 手动调用 `runtime.GC()`

### 25.2.2 逃逸分析

Go编译器会分析变量的作用域，决定变量分配在**栈**还是**堆**上：

- **栈上分配**：函数返回后自动释放，速度快
- **堆上分配**：需要GC回收，可能影响性能

```go
package main

import "fmt"

// 返回字符串（不需要指针，字符串小，栈上分配够用）
func returnString() string {
    s := "hello world"  // 编译器知道s不会逃逸，分配在栈上
    return s
}

// 返回指针（指针可能逃逸到堆上）
func returnPointer() *int {
    x := 42              // x可能逃逸，因为返回了它的地址
    return &x
}

func main() {
    s := returnString()
    fmt.Println("字符串:", s) // 字符串: hello world

    p := returnPointer()
    fmt.Println("指针值:", *p) // 指针值: 42
}
```

**逃逸规则：**
- 如果函数外部没有引用，分配在栈上
- 如果函数外部有引用（如返回指针），分配在堆上

---

## 25.3 内存模式

### 25.3.1 sync.Pool 对象池

`sync.Pool` 是临时对象池，用于复用已分配的对象，减少GC压力。

**典型场景：**
- 高频分配/释放的对象（如buffer）
- 减少内存分配开销

```go
package main

import (
    "fmt"
    "sync"
)

// Pool 中存放可复用的byte数组
var bufferPool = sync.Pool{
    // New：池空时调用此函数创建
    New: func() interface{} {
        return make([]byte, 1024)  // 分配1KB
    },
}

func main() {
    fmt.Println("=== sync.Pool 演示 ===")

    // 第一次Get：池为空，调用New创建
    fmt.Println("第一次Get（池为空）:")
    b1 := bufferPool.Get().([]byte)
    fmt.Printf("  获取buffer，长度: %d，容量: %d\n", len(b1), cap(b1)) // 长度: 0, 容量: 1024

    // 使用完后放回池中
    bufferPool.Put(b1)

    // 第二次Get：复用之前的buffer
    fmt.Println("第二次Get（复用buffer）:")
    b2 := bufferPool.Get().([]byte)
    fmt.Printf("  获取buffer，长度: %d，容量: %d\n", len(b2), cap(b2)) // 长度: 0, 容量: 1024

    bufferPool.Put(b2)
}
```

**工作流程：**
```
Get() ──> 池非空 ──> 返回缓存对象
   │
   └──> 池为空 ──> 调用New()创建
```

### 25.3.2 内存泄漏防范

常见内存泄漏场景：

```go
package main

import (
    "fmt"
    "time"
)

func leakExample() {
    // 泄漏：slice持有大数据引用
    bigData := make([]int, 1_000_000)
    cache := make([]*[]int, 0)
    cache = append(cache, &bigData)  // bigData无法被GC回收
    fmt.Printf("cache长度: %d\n", len(cache)) // cache长度: 1
}

func noLeakExample() {
    // 不泄漏：及时清理
    cache := make([]*[]int, 0, 10)
    for i := 0; i < 5; i++ {
        bigData := make([]int, 1_000_000)
        cache = append(cache, &bigData)
    }
    fmt.Printf("处理完成后: cache长度=%d\n", len(cache)) // 处理完成后: cache长度=5
}

func main() {
    leakExample()
    noLeakExample()
}
```

---

## 25.4 性能调优

### 25.4.1 减少内存分配

字符串拼接时，每次`+`都会创建新字符串（旧字符串被遗弃等待GC）。用`strings.Builder`复用buffer：

```go
package main

import (
    "fmt"
    "strings"
    "time"
)

// 低效：每次拼接都创建新字符串
func badExample() int64 {
    start := time.Now()
    var s string
    for i := 0; i < 100; i++ {
        s = s + "a"  // 每次创建新字符串，旧字符串被GC回收
    }
    _ = s
    return time.Since(start).Microseconds()
}

// 高效：复用buffer
func goodExample() int64 {
    start := time.Now()
    var builder strings.Builder  // 内部有buffer
    for i := 0; i < 100; i++ {
        builder.WriteString("a")  // 写入buffer，不创建新字符串
    }
    _ = builder.String()
    return time.Since(start).Microseconds()
}

func main() {
    badTime := badExample()
    goodTime := goodExample()

    fmt.Printf("字符串+拼接: %d 微秒\n", badTime)   // 字符串+拼接: ~500微秒
    fmt.Printf("Builder拼接: %d 微秒\n", goodTime)   // Builder拼接: ~10微秒
    fmt.Printf("性能提升: %d 倍\n", badTime/goodTime) // 性能提升: ~50倍
}
```

### 25.4.2 预分配内存

对于切片，提前指定容量可以减少重新分配：

```go
package main

import "fmt"

func withoutPrealloc() int64 {
    var s []int
    for i := 0; i < 1000; i++ {
        s = append(s, i)  // 可能触发多次扩容
    }
    return int64(cap(s))
}

func withPrealloc() int64 {
    s := make([]int, 0, 1000)  // 预分配容量1000
    for i := 0; i < 1000; i++ {
        s = append(s, i)  // 不需要扩容
    }
    return int64(cap(s))
}

func main() {
    fmt.Printf("不预分配: 最终容量=%d\n", withoutPrealloc()) // 不预分配: 最终容量=1024
    fmt.Printf("预分配: 最终容量=%d\n", withPrealloc())      // 预分配: 最终容量=1000
}
```

---

## 25.5 常用调试工具

### 25.5.1 查看内存统计

```go
package main

import (
    "fmt"
    "runtime"
)

func printMemStats() {
    var m runtime.MemStats
    runtime.ReadMemStats(&m)

    fmt.Printf("Alloc: %.2f KB\n", float64(m.Alloc)/1024)      // 已分配且未释放
    fmt.Printf("TotalAlloc: %.2f KB\n", float64(m.TotalAlloc)/1024) // 累计分配
    fmt.Printf("Sys: %.2f KB\n", float64(m.Sys)/1024)          // 向系统获取的内存
    fmt.Printf("NumGC: %d\n", m.NumGC)                         // GC次数
}

func main() {
    printMemStats()

    // 分配一些内存
    _ = make([]byte, 1024*1024)  // 1MB

    printMemStats()
}
```

---

## 本章小结

本章我们学习了Go的内存管理：

**内存分配：**
- `new(T)`：分配值类型，返回`*T`，零值
- `make(T, ...)`：分配引用类型（切片/map/channel）

**垃圾回收：**
- Go使用三色标记并发GC
- 逃逸分析决定变量在栈还是堆上分配

**性能优化：**
- 使用`sync.Pool`复用临时对象
- 使用`strings.Builder`拼接字符串
- 预分配切片容量

**最佳实践：**
- 不要返回局部变量的指针（Go会处理，但影响GC）
- 及时清理不需要的引用
- 高频对象使用对象池

