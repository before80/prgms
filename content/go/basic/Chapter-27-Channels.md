+++
title = "第27章 通道 Channel"
weight = 270
date = "2026-03-20T08:39:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++
# 第27章 通道 Channel

> 通道是Go语言最有特色的发明！如果把Goroutine比作"分身术"，那Channel就是"电话线"——让分身之间可以互相通信、数据共享。

想象电话接线员：Goroutine们想通信，得通过Channel来传递消息。Channel保证了：
1. 通信的同步性（发送和接收必须配对）
2. 消息的安全性（一次只被一个接收者消费）

## 27.1 通道类型

### 27.1.1 声明与创建

通道是引用类型，用 `make` 创建：

```go
package main

import "fmt"

func main() {
    // 声明通道（零值是nil）
    var ch1 chan int
    var ch2 chan string

    fmt.Printf("ch1: %v (nil通道)\n", ch1) // ch1: <nil> (nil通道)
    fmt.Printf("ch2: %v (nil通道)\n", ch2) // ch2: <nil> (nil通道)

    // 用make创建通道
    intCh := make(chan int)      // 无缓冲通道
    stringCh := make(chan string) // 无缓冲通道

    fmt.Printf("intCh类型: %T\n", intCh)     // intCh类型: chan int
    fmt.Printf("stringCh类型: %T\n", stringCh) // stringCh类型: chan string
}
```

**通道类型说明：**
- `chan T` - 发送和接收T类型数据
- `chan<- T` - 只能发送T类型数据
- `<-chan T` - 只能接收T类型数据

### 27.1.2 缓冲通道

无缓冲通道：发送和接收必须配对，否则阻塞。
缓冲通道：有容量，发送直到满才阻塞，接收直到空才阻塞。

```go
package main

import "fmt"

func main() {
    // 创建缓冲通道，容量为3
    buffered := make(chan int, 3)

    // 查看通道状态
    fmt.Printf("初始状态: len=%d, cap=%d\n", len(buffered), cap(buffered)) // len=0, cap=3

    // 发送3个数据
    buffered <- 1
    buffered <- 2
    buffered <- 3

    fmt.Printf("发送3个后: len=%d, cap=%d\n", len(buffered), cap(buffered)) // len=3, cap=3

    // 接收一个数据
    v1 := <-buffered
    fmt.Printf("取出%d，剩余: len=%d\n", v1, len(buffered)) // 取出1，剩余: len=2
}
```

**缓冲 vs 无缓冲：**

| 特性 | 无缓冲 `make(chan T)` | 缓冲 `make(chan T, n)` |
|------|---------------------|----------------------|
| 容量 | 0 | n |
| 发送阻塞 | 需等接收者 | 需等缓冲区满 |
| 接收阻塞 | 需等发送者 | 需等缓冲区空 |

---

## 27.2 通道操作

### 27.2.1 发送操作

`<-` 箭头指向数据流向：

```go
package main

import "fmt"

func main() {
    // 创建容量为2的通道
    ch := make(chan int, 2)

    // 发送数据
    ch <- 1
    fmt.Println("发送 1 成功") // 发送 1 成功

    ch <- 2
    fmt.Println("发送 2 成功") // 发送 2 成功

    fmt.Printf("通道内数据量: %d\n", len(ch)) // 通道内数据量: 2
}
```

### 27.2.2 接收操作

接收数据有两种方式：

```go
package main

import "fmt"

func main() {
    ch := make(chan int, 3)
    ch <- 1
    ch <- 2
    ch <- 3

    // 方式1：只接收值
    v1 := <-ch
    fmt.Printf("v1 = %d\n", v1) // v1 = 1

    // 方式2：接收值和状态（comma-ok）
    v2, ok := <-ch
    fmt.Printf("v2 = %d, ok = %t\n", v2, ok) // v2 = 2, ok = true

    v3 := <-ch
    fmt.Printf("v3 = %d\n", v3) // v3 = 3

    // 通道已空，再接收
    v4, ok := <-ch
    fmt.Printf("v4 = %d, ok = %t (通道已空)\n", v4, ok) // v4 = 0, ok = false
}
```

### 27.2.3 关闭通道

发送者关闭通道，接收者通过 `ok` 判断通道是否已关闭：

```go
package main

import "fmt"

func main() {
    ch := make(chan int, 3)
    ch <- 1
    ch <- 2
    ch <- 3
    close(ch)  // 关闭通道

    // 关闭后仍可接收数据，直到通道空
    v1, ok := <-ch
    fmt.Printf("v1=%d, ok=%t\n", v1, ok) // v1=1, ok=true
    v2, ok := <-ch
    fmt.Printf("v2=%d, ok=%t\n", v2, ok) // v2=2, ok=true
    v3, ok := <-ch
    fmt.Printf("v3=%d, ok=%t\n", v3, ok) // v3=3, ok=true

    // 通道已空
    v4, ok := <-ch
    fmt.Printf("v4=%d, ok=%t (通道已关闭且为空)\n", v4, ok) // v4=0, ok=false
}
```

**注意：**
- 关闭已关闭的通道会panic
- 向已关闭的通道发送会panic
- 通道关闭后，接收方会收到零值

---

## 27.3 select 语句

`select` 类似于switch，但用于通道操作——等待多个通道，直到其中一个准备好。

### 27.3.1 基本用法

```go
package main

import "fmt"

func main() {
    ch1 := make(chan int, 1)
    ch2 := make(chan int, 1)

    ch1 <- 10  // ch1准备好了

    // select随机选择一个就绪的case执行
    select {
    case v1 := <-ch1:
        fmt.Printf("从ch1收到: %d\n", v1) // 从ch1收到: 10
    case v2 := <-ch2:
        fmt.Printf("从ch2收到: %d\n", v2)
    }
}
```

### 27.3.2 超时处理

用 `time.After` 实现超时：

```go
package main

import (
    "fmt"
    "time"
)

func main() {
    ch := make(chan int, 1)

    // 模拟：1秒后发送数据
    go func() {
        time.Sleep(1 * time.Second)
        ch <- 42
    }()

    // 等待500ms，如果没收到就超时
    select {
    case v := <-ch:
        fmt.Printf("收到: %d\n", v) // 收到: 42
    case <-time.After(500 * time.Millisecond):
        fmt.Println("超时！等了500ms还没收到") // 超时！等了500ms还没收到
    }
}
```

### 27.3.3 default 分支

当没有任何通道准备好时，执行default（如果有）：

```go
package main

import "fmt"

func main() {
    ch := make(chan int, 1)
    ch <- 1

    // ch1有数据，执行这个case
    select {
    case v := <-ch:
        fmt.Printf("收到: %d\n", v) // 收到: 1
    default:
        fmt.Println("通道未就绪")
    }

    // 空通道，走default
    emptyCh := make(chan int)

    select {
    case v := <-emptyCh:
        fmt.Printf("收到: %d\n", v)
    default:
        fmt.Println("通道为空，执行default") // 通道为空，执行default
    }
}
```

---

## 27.4 通道模式

### 27.4.1 信号模式

用空结构体 `struct{}` 作为信号，不需要传递数据：

```go
package main

import (
    "fmt"
    "time"
)

func worker(done chan struct{}) {
    fmt.Println("Worker: 开始工作...")
    for i := 0; i < 3; i++ {
        fmt.Printf("  工作进度 %d/3\n", i+1)
        time.Sleep(50 * time.Millisecond)
    }
    fmt.Println("Worker: 完工！")
    done <- struct{}{}  // 发送完成信号
}

func main() {
    done := make(chan struct{})  // 空结构体通道，不传递数据

    go worker(done)

    fmt.Println("主函数: 等待Worker完成...")
    <-done  // 等待信号

    fmt.Println("主函数: 收到完成信号!")

    // 主函数: 等待Worker完成...
    // Worker: 开始工作...
    //   工作进度 1/3
    //   工作进度 2/3
    //   工作进度 3/3
    // Worker: 完工！
    // 主函数: 收到完成信号!
}
```

### 27.4.2 管道模式

管道：数据从一系列阶段流过，每个阶段可能 transforming 数据：

```go
package main

import "fmt"

func producer(nums ...int) <-chan int {
    out := make(chan int)
    go func() {
        for _, n := range nums {
            out <- n  // 发送数据
        }
        close(out)  // 数据发完，关闭通道
    }()
    return out
}

func square(in <-chan int) <-chan int {
    out := make(chan int)
    go func() {
        for n := range in {  // 从输入通道接收，直到关闭
            out <- n * n  // 平方后发送
        }
        close(out)
    }()
    return out
}

func main() {
    // 创建管道：producer -> square -> 输出
    pipeline := producer(1, 2, 3, 4, 5)  // 输出: 1, 2, 3, 4, 5
    squared := square(pipeline)            // 平方: 1, 4, 9, 16, 25

    fmt.Print("平方结果: ")
    first := true
    for v := range squared {  // 遍历，直到通道关闭
        if !first {
            fmt.Print(", ")
        }
        fmt.Print(v)
        first = false
    }
    fmt.Println()

    // 平方结果: 1, 4, 9, 16, 25
}
```

**管道图解：**
```
producer(1,2,3,4,5) --> [1] --> [2] --> [3] --> [4] --> [5] --> close
                              |
                              v
                        square: n*n
                              |
                              v
                         [1] --> [4] --> [9] --> [16] --> [25] --> close
```

---

## 27.5 通道进阶

### 27.5.1 单向通道

通道可以限制方向：只能发送或只能接收：

```go
package main

import "fmt"

type Sender chan<- int      // 只能发送
type Receiver <-chan int    // 只能接收

// producer 只发送，不接收
func producer(out chan<- int) {
    out <- 1
    out <- 2
    out <- 3
    close(out)
}

// consumer 只接收，不发送
func consumer(in <-chan int) {
    for v := range in {
        fmt.Printf("收到: %d\n", v)
    }
}

func main() {
    ch := make(chan int)
    go producer(ch)
    consumer(ch)

    // 收到: 1
    // 收到: 2
    // 收到: 3
}
```

### 27.5.2 遍历通道

用 `for range` 自动等待通道关闭：

```go
package main

import "fmt"

func main() {
    ch := make(chan int, 5)

    // 发送者
    go func() {
        for i := 1; i <= 5; i++ {
            ch <- i
        }
        close(ch)  // 重要：关闭通道
    }()

    // range自动等待通道关闭
    fmt.Print("收到: ")
    for v := range ch {
        fmt.Printf("%d ", v)
    }
    fmt.Println()

    // 收到: 1 2 3 4 5
}
```

---

## 本章小结

本章我们学习了通道：

**通道基础：**
- `make(chan T)` 创建无缓冲通道
- `make(chan T, n)` 创建缓冲通道
- `<-` 发送和接收操作

**select语句：**
- 多通道选择：随机选择已就绪的case
- 超时处理：`case <-time.After()`
- default分支：非阻塞

**通道模式：**
- 信号模式：用 `chan struct{}` 表示完成
- 管道模式：一系列处理阶段串联

**最佳实践：**
- 发送者关闭通道（接收者不要关闭）
- 使用 `range` 遍历通道直到关闭
- 用 `comma-ok` 判断通道状态

