+++
title = "第28章 同步原语"
weight = 280
date = "2026-03-20T08:39:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++
# 第28章 同步原语

> Go的sync包提供了各种同步原语，就像并发编程的"工具箱"。有了这些工具，多个协程才能安全地协作。

## 28.1 互斥锁 Mutex

### 28.1.1 为什么需要互斥锁

当多个协程同时访问共享变量时，会发生"数据竞争"：

```go
package main

import (
    "fmt"
    "sync"
)

var counter int  // 共享变量
var mu sync.Mutex  // 互斥锁

// SafeIncrement 安全地增加计数器
func SafeIncrement() {
    mu.Lock()       // 加锁：其他协程要等这里释放才能进来
    defer mu.Unlock()
    counter++       // 访问共享数据
}

func main() {
    var wg sync.WaitGroup

    fmt.Printf("初始计数器: %d\n", counter)

    // 启动1000个协程同时修改counter
    for i := 0; i < 1000; i++ {
        wg.Add(1)
        go func() {
            defer wg.Done()
            SafeIncrement()
        }()
    }

    wg.Wait()
    fmt.Printf("最终计数器: %d\n", counter)

    // 初始计数器: 0
    // 最终计数器: 1000 (正确！)
}
```

### 28.1.2 保护共享资源

典型应用：保护银行账户：

```go
package main

import (
    "fmt"
    "sync"
)

type BankAccount struct {
    balance int
    mu      sync.Mutex  // 每个账户有自己的锁
}

// Deposit 存款：原子操作
func (b *BankAccount) Deposit(amount int) {
    b.mu.Lock()
    defer b.mu.Unlock()
    b.balance += amount
}

// Withdraw 取款：原子操作
func (b *BankAccount) Withdraw(amount int) bool {
    b.mu.Lock()
    defer b.mu.Unlock()
    if b.balance >= amount {
        b.balance -= amount
        return true
    }
    return false
}

// Balance 查询余额：原子操作
func (b *BankAccount) Balance() int {
    b.mu.Lock()
    defer b.mu.Unlock()
    return b.balance
}

func main() {
    account := &BankAccount{balance: 1000}

    fmt.Printf("初始余额: %d\n", account.Balance()) // 初始余额: 1000

    // 模拟并发存款
    for i := 0; i < 10; i++ {
        account.Deposit(100)
    }
    fmt.Printf("存款后余额: %d\n", account.Balance()) // 存款后余额: 2000

    // 取款
    if account.Withdraw(500) {
        fmt.Printf("取款成功，余额: %d\n", account.Balance()) // 取款成功，余额: 1500
    }
}
```

---

## 28.2 读写锁 RWMutex

互斥锁让所有访问都串行化，但"读多写少"的场景下，读锁可以并发，提高性能。

### 28.2.1 读写锁原理

- **读锁（RLock）**：允许多个读者同时读
- **写锁（Lock）**：独占，只允许一个写者

```go
package main

import (
    "fmt"
    "sync"
    "time"
)

var (
    data string
    mu   sync.RWMutex
)

// ReadOnly 读取数据（可以多个同时读）
func ReadOnly() string {
    mu.RLock()         // 加读锁
    defer mu.RUnlock()
    return data
}

// Write 写入数据（独占）
func Write(newData string) {
    mu.Lock()          // 加写锁
    defer mu.Unlock()
    time.Sleep(50 * time.Millisecond)  // 模拟写入耗时
    data = newData
}

func main() {
    data = "initial"

    var wg sync.WaitGroup

    // 启动5个读者
    for i := 0; i < 5; i++ {
        wg.Add(1)
        go func(id int) {
            defer wg.Done()
            r := ReadOnly()
            fmt.Printf("Reader%d: read %q\n", id, r)
        }(i)
    }

    // 启动1个写者
    wg.Add(1)
    go func() {
        defer wg.Done()
        fmt.Println("Writer: 开始写入...")
        Write("updated")
        fmt.Println("Writer: 写入完成")
    }()

    wg.Wait()
    fmt.Printf("最终数据: %q\n", data)
}
```

### 28.2.2 什么时候用读写锁

| 场景 | 推荐锁 | 原因 |
|------|--------|------|
| 读 >> 写 | RWMutex | 读可以并发，提高性能 |
| 读写相当 | Mutex | 读写锁开销可能更大 |
| 写冲突 | Mutex | 保证写操作的原子性 |

---

## 28.3 等待组 WaitGroup

WaitGroup 用于等待一组协程完成：

```go
package main

import (
    "fmt"
    "sync"
    "time"
)

func worker(id int, wg *sync.WaitGroup) {
    defer wg.Done()  // 完成后通知
    fmt.Printf("Worker%d: 开始工作\n", id)
    time.Sleep(time.Duration(100*id) * time.Millisecond)
    fmt.Printf("Worker%d: 完成！\n", id)
}

func main() {
    var wg sync.WaitGroup

    fmt.Println("主函数: 启动5个Worker...")

    for i := 1; i <= 5; i++ {
        wg.Add(1)          // 注册一个协程
        go worker(i, &wg)
    }

    fmt.Println("主函数: 等待Worker们完成...")
    wg.Wait()             // 阻塞，直到所有注册的协程都调用Done

    fmt.Println("主函数: 所有Worker已完成!")

    // 主函数: 启动5个Worker...
    // 主函数: 等待Worker们完成...
    // Worker1: 开始工作
    // Worker2: 开始工作
    // ...
    // Worker1: 完成！
    // Worker2: 完成！
    // ...
    // 主函数: 所有Worker已完成!
}
```

**WaitGroup 三个方法：**
- `Add(n)` - 注册n个协程
- `Done()` - 协程完成时调用（等价于 `Add(-1)`）
- `Wait()` - 阻塞，直到计数归零

---

## 28.4 单次执行 Once

有些初始化操作只需要执行一次，Once 保证多次调用只执行一次：

```go
package main

import (
    "fmt"
    "sync"
)

var (
    once     sync.Once  // 单次执行器
    resource string    // 共享资源
)

// InitResource 初始化资源（只会执行一次）
func InitResource() {
    fmt.Println("初始化资源中...（真的只执行一次）")
    resource = "数据库连接、缓存等"
}

// GetResource 获取资源（需要时才初始化）
func GetResource() string {
    once.Do(InitResource)  // 多次调用只执行一次InitResource
    return resource
}

func main() {
    fmt.Println("第一次获取:")
    r1 := GetResource()
    fmt.Printf("  资源: %s\n", r1)

    fmt.Println("\n第二次获取:")
    r2 := GetResource()
    fmt.Printf("  资源: %s\n", r2)

    fmt.Println("\n第三次获取:")
    r3 := GetResource()
    fmt.Printf("  资源: %s\n", r3)

    // 第一次获取:
    // 初始化资源中...（真的只执行一次）
    //   资源: 数据库连接、缓存等
    //
    // 第二次获取:
    //   资源: 数据库连接、缓存等
    //
    // 第三次获取:
    //   资源: 数据库连接、缓存等
}
```

**典型应用场景：**
- 配置文件读取（只需要读一次）
- 数据库连接初始化
- 单例模式

---

## 28.5 并发安全 Map

`sync.Map` 是专门为并发访问设计的Map：

```go
package main

import (
    "fmt"
    "sync"
)

func main() {
    var m sync.Map

    // 存储键值对
    m.Store("name", "张三")
    m.Store("age", 25)

    // 读取单个键
    if v, ok := m.Load("name"); ok {
        fmt.Printf("name: %v\n", v) // name: 张三
    }

    // LoadOrStore：如果键存在返回现有值，否则存储新值
    v, loaded := m.LoadOrStore("country", "中国")
    fmt.Printf("LoadOrStore: 值=%v, 已存在=%t\n", v, loaded) // LoadOrStore: 值=中国, 已存在=false

    // 再次调用：键已存在
    v, loaded = m.LoadOrStore("country", "美国")
    fmt.Printf("LoadOrStore: 值=%v, 已存在=%t\n", v, loaded) // LoadOrStore: 值=中国, 已存在=true

    // 删除键
    m.Delete("age")

    // 遍历所有键值对
    fmt.Println("\n遍历Map:")
    m.Range(func(key, value interface{}) bool {
        fmt.Printf("  %s: %v\n", key, value)
        return true  // 返回true继续遍历
    })

    // 遍历Map:
    //   name: 张三
    //   country: 中国
}
```

**sync.Map vs map+Mutex：**

| 操作 | sync.Map | map+Mutex |
|------|----------|-----------|
| 读 | 快 | 需要加锁 |
| 写 | 快 | 需要加锁 |
| 适合场景 | 高并发读 | 低并发 |

---

## 28.6 原子操作

对于简单的整数操作，原子操作比锁更高效：

### 28.6.1 原子整数

```go
package main

import (
    "fmt"
    "sync"
    "sync/atomic"
)

var counter int64  // 必须是对齐的int64

func main() {
    var wg sync.WaitGroup

    fmt.Printf("初始计数器: %d\n", atomic.LoadInt64(&counter))

    // 启动1000个协程同时增加计数器
    for i := 0; i < 1000; i++ {
        wg.Add(1)
        go func() {
            defer wg.Done()
            atomic.AddInt64(&counter, 1)  // 原子增加
        }()
    }

    wg.Wait()
    fmt.Printf("最终计数器: %d\n", atomic.LoadInt64(&counter))

    // 初始计数器: 0
    // 最终计数器: 1000
}
```

### 28.6.2 CAS 操作

CAS（Compare-And-Swap）是原子操作的基础：

```go
package main

import (
    "fmt"
    "sync/atomic"
)

var value int64 = 100

func main() {
    fmt.Printf("初始值: %d\n", value)

    // CAS(100->200)：如果当前值是100，则改为200
    ok := atomic.CompareAndSwapInt64(&value, 100, 200)
    fmt.Printf("CAS(100→200): 成功=%v, 当前值=%d\n", ok, value) // 成功=true, 当前值=200

    // 再次尝试CAS(100->300)：当前值已是200，失败
    ok = atomic.CompareAndSwapInt64(&value, 100, 300)
    fmt.Printf("CAS(100→300): 成功=%v, 当前值=%d\n", ok, value) // 成功=false, 当前值=200

    // 正确的CAS
    ok = atomic.CompareAndSwapInt64(&value, 200, 300)
    fmt.Printf("CAS(200→300): 成功=%v, 当前值=%d\n", ok, value) // 成功=true, 当前值=300
}
```

**原子操作类型：**
- `AddInt64` - 加法
- `SwapInt64` - 赋值
- `LoadInt64` - 读取
- `StoreInt64` - 存储
- `CompareAndSwapInt64` - CAS

---

## 28.7 条件变量 Cond

Cond 用于协程间的条件等待：

```go
package main

import (
    "fmt"
    "sync"
    "time"
)

func main() {
    var mu sync.Mutex
    cond := sync.NewCond(&mu)
    ready := false

    // 启动3个Worker，它们等待条件满足
    for i := 1; i <= 3; i++ {
        go func(id int) {
            mu.Lock()
            for !ready {
                cond.Wait()  // 等待条件满足（自动释放锁）
            }
            mu.Unlock()
            fmt.Printf("Worker%d: 收到信号，开始工作！\n", id)
        }(i)
    }

    fmt.Println("主函数: 准备发送信号...")
    time.Sleep(1 * time.Second)

    // 设置条件并广播
    mu.Lock()
    ready = true
    mu.Unlock()

    fmt.Println("主函数: 广播信号！")
    cond.Broadcast()  // 唤醒所有等待的协程

    time.Sleep(100 * time.Millisecond)

    // 主函数: 准备发送信号...
    // (1秒后)
    // 主函数: 广播信号！
    // Worker1: 收到信号，开始工作！
    // Worker2: 收到信号，开始工作！
    // Worker3: 收到信号，开始工作！
}
```

**Cond 的三个方法：**
- `Wait()` - 等待信号（自动释放锁）
- `Signal()` - 唤醒一个等待者
- `Broadcast()` - 唤醒所有等待者

---

## 本章小结

本章我们学习了同步原语：

**互斥锁：**
- `sync.Mutex`：基本互斥锁
- `sync.RWMutex`：读写锁，读可以并发

**等待组：**
- `sync.WaitGroup`：等待协程完成

**单次执行：**
- `sync.Once`：多次调用只执行一次

**并发安全Map：**
- `sync.Map`：专门为并发设计的Map

**原子操作：**
- `sync/atomic`：高效的原子上操作

**条件变量：**
- `sync.Cond`：协程间的条件等待

**选择指南：**
- 简单计数器 → 原子操作
- 读多写少 → RWMutex
- 复杂共享资源 → Mutex + map
- 等待多个协程 → WaitGroup
- 一次性初始化 → Once

