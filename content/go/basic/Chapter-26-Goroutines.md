+++
title = "第26章 协程 Goroutine"
weight = 260
date = "2026-03-20T08:39:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++
# 第26章 协程 Goroutine

> 如果说线程是"单线程社恐"，一次只能专心做一件事；那Goroutine就是"社交达人"，可以同时和很多人聊天！

想象你是一位餐厅服务员：
- **传统模式**：你一次只能服务一桌客人（点菜、上菜、结账都得排队）
- **Go模式**：你有了"分身术"，可以同时服务几十桌客人！

这就是Goroutine的魅力——用极低的成本，实现超高并发。

## 26.1 协程概念

### 26.1.1 线程 vs 协程

为什么Go选择用Goroutine而不是线程？让我们对比一下：

| 特性 | 传统线程 | Goroutine |
|------|---------|-----------|
| 栈大小 | 固定1-2MB | 初始2KB，可增长至1GB |
| 管理方 | 操作系统内核 | Go运行时（用户态） |
| 创建成本 | 约1-2μs | 约200ns（快10倍！） |
| 切换成本 | 约1-2μs | 约200ns |

```go
package main

import (
    "fmt"
    "runtime"
    "time"
)

func main() {
    // 查看当前系统的CPU核心数
    cpuNum := runtime.NumCPU()
    fmt.Printf("CPU核心数: %d\n", cpuNum) // CPU核心数: 8

    // GOMAXPROCS：控制有多少个"调度器"同时运行
    // 通常设置为CPU核心数
    gomaxprocs := runtime.GOMAXPROCS(0)
    fmt.Printf("GOMAXPROCS(调度P数量): %d\n", gomaxprocs) // GOMAXPROCS(调度P数量): 8

    const count = 100_000  // 创建10万个协程
    done := make(chan bool, count)

    start := time.Now()

    // 批量创建协程
    for i := 0; i < count; i++ {
        go func() {
            _ = i * 2  // 简单的计算任务
            done <- true
        }()
    }

    // 等待所有协程完成
    for i := 0; i < count; i++ {
        <-done
    }
    elapsed := time.Since(start)

    fmt.Printf("\n创建 %d 个协程总耗时: %v\n", count, elapsed) // 创建 100000 个协程总耗时: ~200ms
    fmt.Printf("平均每个协程创建成本: %v\n", elapsed/time.Duration(count)) // 平均每个协程创建成本: ~2000ns
}
```

### 26.1.2 M:N 调度模型

Go的调度器采用M:N模型：M个线程上调度N个Goroutine。

```
                         用户代码
                            ↓
    ┌───────────────────────────────────────────┐
    │              Goroutine (G)                │
    │   G1    G2    G3    G4    G5    G6        │
    │                                           │
    │  "我要干活！"  "我也要！"  "让我来！"      │
    └──────────────────┬────────────────────────┘
                       │
                       ↓
    ┌───────────────────────────────────────────┐
    │            Processor (P)                   │
    │         调度器，负责找活干                   │
    └──────────────────┬────────────────────────┘
                       │
    ┌──────────────────┼────────────────────────┐
    │                  │                        │
    ↓                  ↓                        ↓
 ┌──────┐        ┌──────┐                 ┌──────┐
 │  M1  │        │  M2  │                 │  M3  │   Machine (线程)
 │ OS线程│        │ OS线程│                 │ OS线程│
 └──────┘        └──────┘                 └──────┘
```

**模型解释：**
- **M（Machine）**：真正的OS线程
- **P（Processor）**：调度器，上有本地队列
- **G（Goroutine）**：任务，排队等调度

### 26.1.3 协程的生死

协程生命周期：
- **创建**：`go func()` 启动
- **运行**：被调度器分配给P执行
- **结束**：函数返回或panic

```go
package main

import (
    "fmt"
    "time"
)

// 永远运行的协程（模拟泄漏场景）
func leakyWorker(id int) {
    for {
        // 无限循环，每秒打印一次
        fmt.Printf("Worker %d: 我还在运行...\n", id)
        time.Sleep(time.Second)
    }
}

func main() {
    fmt.Println("主函数: 启动3个会永远运行的协程...")

    // 启动3个协程，它们永远不会结束
    for i := 1; i <= 3; i++ {
        go leakyWorker(i)
    }

    fmt.Println("主函数: 去喝杯咖啡...")
    time.Sleep(3 * time.Second)

    fmt.Println("主函数: 3秒后，程序仍在运行，协程还在跑！")
}
```

---

## 26.2 协程创建

### 26.2.1 go 关键字

`go` 关键字用于启动协程，语法：`go 函数名(参数)`

```go
package main

import (
    "fmt"
    "time"
)

// 普通函数，被协程调用
func say(msg string, times int) {
    for i := 0; i < times; i++ {
        fmt.Printf("[%s] 第%d次\n", msg, i+1)
        time.Sleep(10 * time.Millisecond)  // 模拟工作
    }
}

func main() {
    fmt.Println("主函数: 开始...")

    // 用go关键字启动协程
    // 注意：say函数还没执行完，主函数就继续往下走了
    go say("Hello", 3)  // 并发执行
    go say("World", 3)  // 另一个并发执行

    fmt.Println("主函数: 我不等了，先走一步...")
    time.Sleep(100 * time.Millisecond)  // 等待协程完成

    fmt.Println("主函数: 退出")
}
```

**注意：** 如果主函数退出太快，协程可能还没执行完！

### 26.2.2 匿名函数协程

协程也可以直接用匿名函数：

```go
package main

import (
    "fmt"
    "time"
)

func main() {
    // 匿名函数协程：带参数
    go func(name string) {
        for i := 0; i < 3; i++ {
            fmt.Printf("Hello from %s, round %d\n", name, i+1)
            time.Sleep(20 * time.Millisecond)
        }
    }("closure")

    // 匿名函数协程：捕获外部变量
    counter := 0
    go func() {
        for i := 0; i < 5; i++ {
            counter++  // 捕获counter变量
            time.Sleep(10 * time.Millisecond)
        }
    }()

    time.Sleep(100 * time.Millisecond)
    fmt.Printf("最终counter值: %d\n", counter) // 最终counter值: 5
}
```

---

## 26.3 协程调度

### 26.3.1 主动让出

`runtime.Gosched()` 让当前协程主动让出CPU，让其他协程有机会运行：

```go
package main

import (
    "fmt"
    "runtime"
)

func cooperative() {
    for i := 0; i < 3; i++ {
        fmt.Printf("协程A: 我在做事 %d\n", i)
        runtime.Gosched()  // 主动说：我先休息一下让别人干
    }
}

func greedy() {
    for i := 0; i < 3; i++ {
        fmt.Printf("协程B: 我也在做事 %d\n", i)
    }
}

func main() {
    runtime.GOMAXPROCS(1)  // 只用1个CPU核心，更容易看到调度效果

    done := make(chan bool, 2)

    go func() {
        cooperative()
        done <- true
    }()

    go func() {
        greedy()
        done <- true
    }()

    <-done
    <-done
}
```

### 26.3.2 阻塞与调度

当协程阻塞时（如等待channel），调度器会自动切到其他协程：

```go
package main

import (
    "fmt"
    "time"
)

func blockingTask(id int, ch chan int) {
    fmt.Printf("Task %d: 开始，等待数据...\n", id)
    result := <-ch  // 阻塞等待数据
    fmt.Printf("Task %d: 收到数据 %d\n", id, result)
}

func main() {
    ch := make(chan int)

    // 启动3个协程，它们都会阻塞在channel上
    for i := 1; i <= 3; i++ {
        go blockingTask(i, ch)
    }

    time.Sleep(100 * time.Millisecond)  // 等协程们都开始等待

    fmt.Println("主函数: 发送数据...")

    // 按顺序发送数据，调度器会自动唤醒对应协程
    for i := 1; i <= 3; i++ {
        ch <- i * 100
        time.Sleep(50 * time.Millisecond)
    }
}
```

---

## 26.4 协程同步

### 26.4.1 sync.WaitGroup

`WaitGroup` 用于等待一组协程完成：

```go
package main

import (
    "fmt"
    "sync"
    "time"
)

func worker(id int, wg *sync.WaitGroup) {
    defer wg.Done()  // 完成后通知WaitGroup
    fmt.Printf("Worker %d: 开始工作\n", id)
    time.Sleep(time.Duration(100*id) * time.Millisecond)  // 模拟工作
    fmt.Printf("Worker %d: 完成！\n", id)
}

func main() {
    var wg sync.WaitGroup  // 等待组

    fmt.Println("主函数: 启动3个Worker...")

    for i := 1; i <= 3; i++ {
        wg.Add(1)      // 注册一个协程
        go worker(i, &wg)
    }

    fmt.Println("主函数: 等待Worker们完成...")
    wg.Wait()          // 阻塞，直到所有注册的协程都调用Done

    fmt.Println("主函数: 所有Worker已完成!")

    // 主函数: 启动3个Worker...
    // 主函数: 等待Worker们完成...
    // Worker 1: 开始工作
    // Worker 2: 开始工作
    // Worker 3: 开始工作
    // Worker 1: 完成！
    // Worker 2: 完成！
    // Worker 3: 完成！
    // 主函数: 所有Worker已完成!
}
```

### 26.4.2 sync.Mutex（重要！）

多个协程同时修改共享数据会造成**数据竞争**。Mutex可以加锁保护：

```go
package main

import (
    "fmt"
    "sync"
)

var (
    counter int  // 共享变量
    mu      sync.Mutex  // 互斥锁
)

// SafeIncrement 安全地增加计数器
func SafeIncrement() {
    mu.Lock()      // 加锁：其他协程要等这里释放才能进来
    defer mu.Unlock()
    counter++       // 访问共享数据
    // 函数结束自动解锁
}

func main() {
    var wg sync.WaitGroup

    fmt.Printf("初始counter: %d\n", counter)

    // 启动1000个协程同时修改counter
    for i := 0; i < 1000; i++ {
        wg.Add(1)
        go func() {
            defer wg.Done()
            SafeIncrement()
        }()
    }

    wg.Wait()
    fmt.Printf("最终counter: %d (正确！)\n", counter)

    // 初始counter: 0
    // 最终counter: 1000 (正确！)
}
```

---

## 26.5 协程模式

### 26.5.1 工作池模式

预先创建一组Worker，从任务池取任务执行：

```go
package main

import (
    "fmt"
    "sync"
    "time"
)

const (
    numWorkers = 3   // Worker数量
    numJobs    = 10  // 任务数量
)

// Worker 从jobs取任务，处理后发送到results
func worker(id int, jobs <-chan int, results chan<- int, wg *sync.WaitGroup) {
    defer wg.Done()

    for job := range jobs {  // 从jobs取任务，nil时会阻塞
        fmt.Printf("Worker %d: 接到任务 %d\n", id, job)
        time.Sleep(50 * time.Millisecond)  // 模拟处理
        results <- job * 2                 // 发送结果
        fmt.Printf("Worker %d: 完成任务 %d -> %d\n", id, job, job*2)
    }
}

func main() {
    // 创建通道
    jobs := make(chan int, numJobs)    // 任务池
    results := make(chan int, numJobs)  // 结果池

    var wg sync.WaitGroup

    // 启动Worker们
    for i := 1; i <= numWorkers; i++ {
        wg.Add(1)
        go worker(i, jobs, results, &wg)
    }

    // 发送任务
    for j := 1; j <= numJobs; j++ {
        jobs <- j
    }
    close(jobs)  // 关闭任务通道，表示没有更多任务

    // 等待所有Worker完成，然后关闭结果通道
    go func() {
        wg.Wait()
        close(results)
    }()

    // 收集结果
    count := 0
    for result := range results {
        fmt.Printf("  主函数: 收到结果 %d\n", result)
        count++
    }

    fmt.Printf("\n共处理 %d 个任务\n", count)
}
```

### 26.5.2 扇出模式

一个生产者，多个消费者并行处理：

```go
package main

import (
    "fmt"
    "sync"
)

// 生产者：产生数据
func producer(nums ...int) <-chan int {
    out := make(chan int)
    go func() {
        for _, n := range nums {
            out <- n
        }
        close(out)  // 数据发完，关闭通道
    }()
    return out
}

// 消费者：处理数据
func processor(id int, in <-chan int, out chan<- int, wg *sync.WaitGroup) {
    defer wg.Done()
    for v := range in {
        result := v * v  // 平方运算
        fmt.Printf("Processor %d: %d² = %d\n", id, v, result)
        out <- result
    }
}

func main() {
    data := []int{1, 2, 3, 4, 5}
    input := producer(data...)  // 创建生产者

    const numProcessors = 2     // 2个消费者
    results := make(chan int, len(data))

    var wg sync.WaitGroup

    // 启动消费者
    for i := 1; i <= numProcessors; i++ {
        wg.Add(1)
        go processor(i, input, results, &wg)
    }

    // 等待完成后关闭结果通道
    go func() {
        wg.Wait()
        close(results)
    }()

    // 收集结果
    sum := 0
    for r := range results {
        sum += r
    }
    fmt.Printf("\n平方和: %d\n", sum) // 1+4+9+16+25 = 55
}
```

---

## 26.6 协程与通道

协程和通道是好搭档：协程负责干活，通道负责传递数据：

```go
package main

import (
    "fmt"
    "time"
)

// sender 协程：发送数据
func sender(ch chan<- string) {
    messages := []string{"Hello", "World", "Go", "Routines"}
    for _, msg := range messages {
        fmt.Printf("[发送者] 发送: '%s'\n", msg)
        ch <- msg  // 发送数据，阻塞直到接收者准备好
        time.Sleep(30 * time.Millisecond)
    }
    close(ch)  // 发送完毕，关闭通道
}

func main() {
    ch := make(chan string)  // 创建通道

    go sender(ch)  // 启动发送协程

    fmt.Println("[主函数] 开始接收...")

    // range channel：自动等待通道关闭
    for msg := range ch {
        fmt.Printf("[主函数] 收到: '%s'\n", msg)
    }

    fmt.Println("[主函数] 通道已关闭，接收完毕")

    // [主函数] 开始接收...
    // [发送者] 发送: 'Hello'
    // [主函数] 收到: 'Hello'
    // [发送者] 发送: 'World'
    // [主函数] 收到: 'World'
    // ...
    // [主函数] 通道已关闭，接收完毕
}
```

---

## 26.7 常见问题

### 26.7.1 主协程退出

**问题：** 如果主协程（main函数）退出，其他协程会被直接终止！

```go
package main

import (
    "fmt"
    "time"
)

func lazyWorker() {
    fmt.Println("Worker: 我刚开始...")
    time.Sleep(100 * time.Millisecond)
    fmt.Println("Worker: 我终于干完了！")
}

func main() {
    go lazyWorker()  // 启动协程

    fmt.Println("主函数: 我不等了，再见！")
    time.Sleep(10 * time.Millisecond)  // 只等10ms

    fmt.Println("主函数: 退出！")
    // 此时Worker还没执行完，但程序已经退出了
    // Worker的结果不会被看到
}
```

### 26.7.2 数据竞争

**问题：** 多个协程同时修改同一个变量：

```go
package main

import (
    "fmt"
    "sync"
)

var counter int

func main() {
    var wg sync.WaitGroup

    for i := 0; i < 1000; i++ {
        wg.Add(1)
        go func() {
            defer wg.Done()
            counter++  // 数据竞争！
        }()
    }

    wg.Wait()
    fmt.Printf("counter: %d (可能是978或1023等，而不是1000)\n", counter)
}
```

**解决：** 使用Mutex或atomic操作保护共享变量。

---

## 本章小结

本章我们学会了Goroutine：

**核心概念：**
- Goroutine由Go运行时管理，初始栈仅2KB（vs线程1-2MB）
- M:N调度模型：M个线程调度N个协程
- GOMAXPROCS控制并发数，通常=CPU核心数

**创建与同步：**
- `go func()` 创建协程
- `sync.WaitGroup` 等待协程完成
- `sync.Mutex` 保护共享资源

**通道模式：**
- 工作池：预先创建Worker，消费任务池
- 扇出：一个生产者，多个消费者并行处理

**黄金法则：**
> 主协程退出 = 所有协程强制终止！一定要等所有协程完成再退出。

