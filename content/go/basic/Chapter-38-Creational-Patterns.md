+++
title = "第38章 创建型模式"
weight = 380
date = "2026-03-23T08:39:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 第38章 创建型模式

## 38.1 单例模式

> 👑 **单例模式**大概是所有设计模式中最"简单粗暴"的一个——一个类只能有一个实例，并且要提供一个全局访问点。这听起来很简单，但实现一个**线程安全**、**延迟加载**、**高性能**的单例，可没那么容易！

### 38.1.1 once 实现

Go 标准库的 `sync.Once` 是实现单例模式的利器：

```go
package main

import (
    "fmt"
    "sync"
)

// Database 单例数据库连接
type Database struct {
    conn string
}

// sync.Once 保证了初始化代码只会执行一次
var (
    instance *Database
    once     sync.Once
)

// GetInstance 获取 Database 单例
func GetInstance() *Database {
    once.Do(func() {
        // 这个函数只会被执行一次
        instance = &Database{
            conn: "postgres://localhost:5432/mydb",
        }
        fmt.Println("数据库连接已创建")
    })
    return instance
}

func main() {
    fmt.Println("=== sync.Once 单例 ===")

    // 多次调用 GetInstance，只会创建一次连接
    db1 := GetInstance()
    db2 := GetInstance()
    db3 := GetInstance()

    fmt.Printf("db1 == db2: %v\n", db1 == db2) // true
    fmt.Printf("db2 == db3: %v\n", db2 == db3) // true
    fmt.Printf("所有引用都指向同一个实例: %p\n", db1) // 例如: 0x000000c00000
}
```

**为什么用 `sync.Once`？**

- ✅ **线程安全**：多个 goroutine 同时调用也不会创建多个实例
- ✅ **延迟加载**：只有在第一次使用时才会创建实例
- ✅ **高性能**：不需要加锁检查

### 38.1.2 惰性初始化

`sync.Once` 是"惰性初始化"的完美实现。但有时候你可能需要一个更灵活的方式：

```go
package main

import (
    "fmt"
    "sync"
)

// 方式一：双重检查锁定（Double-Checked Locking）
type LazySingleton struct {
    data string
}

var (
    lazyInstance *LazySingleton
    lazyMu       sync.Mutex
)

func GetLazyInstance() *LazySingleton {
    // 第一次检查：快速路径，大多数情况下直接返回
    if lazyInstance != nil {
        return lazyInstance
    }

    // 加锁
    lazyMu.Lock()
    defer lazyMu.Unlock()

    // 第二次检查：确认在加锁期间实例是否已被创建
    if lazyInstance == nil {
        lazyInstance = &LazySingleton{data: "延迟加载的数据"}
    }
    return lazyInstance
}

// 方式二：sync.Once（更简洁）
type OnceSingleton struct {
    data string
}

var (
    onceInstance *OnceSingleton
    onceSync     sync.Once
)

func GetOnceInstance() *OnceSingleton {
    onceSync.Do(func() {
        onceInstance = &OnceSingleton{data: "once 加载的数据"}
    })
    return onceInstance
}

func main() {
    fmt.Println("=== 惰性初始化 ===")

    s1 := GetLazyInstance()
    s2 := GetLazyInstance()
    fmt.Printf("lazy: %p == %p? %v\n", s1, s2, s1 == s2) // true

    s3 := GetOnceInstance()
    s4 := GetOnceInstance()
    fmt.Printf("once: %p == %p? %v\n", s3, s4, s3 == s4) // true
}
```

> 💡 **推荐**：`sync.Once` 是 Go 中实现单例的最佳实践。除非你有特殊需求（如需要传递参数），否则请使用它。

---

## 38.2 工厂模式

> 🏭 **工厂模式**是一种创建型设计模式，它提供了一种创建对象的最佳方式。工厂模式的核心思想是：**将对象的创建与使用分离**。

### 38.2.1 简单工厂

简单工厂不是23种经典设计模式之一，但它是最常用的"入门级"工厂：

```go
package main

import "fmt"

// Product 产品接口
type Product interface {
    Use() string
}

// ConcreteProductA 具体产品 A
type ConcreteProductA struct{}

func (p *ConcreteProductA) Use() string {
    return "使用产品 A"
}

// ConcreteProductB 具体产品 B
type ConcreteProductB struct{}

func (p *ConcreteProductB) Use() string {
    return "使用产品 B"
}

// ProductType 产品类型枚举
type ProductType int

const (
    TypeA ProductType = iota
    TypeB
)

// SimpleFactory 简单工厂
type SimpleFactory struct{}

func (f *SimpleFactory) Create(productType ProductType) Product {
    switch productType {
    case TypeA:
        return &ConcreteProductA{}
    case TypeB:
        return &ConcreteProductB{}
    default:
        panic("未知的產品类型")
    }
}

func main() {
    fmt.Println("=== 简单工厂 ===")

    factory := &SimpleFactory{}

    productA := factory.Create(TypeA)
    fmt.Println(productA.Use())

    productB := factory.Create(TypeB)
    fmt.Println(productB.Use())
}
```

### 38.2.2 抽象工厂

**抽象工厂模式**提供一个创建一系列相关或相互依赖对象的接口，而无需指定它们具体的类：

```go
package main

import "fmt"

//Button 按钮接口
type Button interface {
    Render() string
}

// Input 输入框接口
type Input interface {
    Render() string
}

// WindowsButton Windows 风格的按钮
type WindowsButton struct{}

func (b *WindowsButton) Render() string {
    return "[ Windows 按钮 ]"
}

// WindowsInput Windows 风格的输入框
type WindowsInput struct{}

func (i *WindowsInput) Render() string {
    return "< Windows 输入框 >"
}

// MacButton Mac 风格的按钮
type MacButton struct{}

func (b *MacButton) Render() string {
    return "( Mac 按钮 )"
}

// MacInput Mac 风格的输入框
type MacInput struct{}

func (i *MacInput) Render() string {
    return "( Mac 输入框 )"
}

// GUIFactory 抽象工厂接口
type GUIFactory interface {
    CreateButton() Button
    CreateInput() Input
}

// WindowsFactory Windows 风格工厂
type WindowsFactory struct{}

func (f *WindowsFactory) CreateButton() Button {
    return &WindowsButton{}
}

func (f *WindowsFactory) CreateInput() Input {
    return &WindowsInput{}
}

// MacFactory Mac 风格工厂
type MacFactory struct{}

func (f *MacFactory) CreateButton() Button {
    return &MacButton{}
}

func (f *MacFactory) CreateInput() Input {
    return &MacInput{}
}

// GetFactory 根据系统类型获取工厂
func GetFactory(osType string) GUIFactory {
    switch osType {
    case "windows":
        return &WindowsFactory{}
    case "mac":
        return &MacFactory{}
    default:
        panic("不支持的系统类型")
    }
}

func main() {
    fmt.Println("=== 抽象工厂 ===")

    // 客户端代码不知道具体使用哪个工厂
    factory := GetFactory("mac")

    button := factory.CreateButton()
    input := factory.CreateInput()

    fmt.Printf("按钮: %s\n", button.Render()) // ( Mac 按钮 )
    fmt.Printf("输入框: %s\n", input.Render()) // ( Mac 输入框 )
}
```

> 🎯 **Mermaid 图：抽象工厂结构**
>
> ```mermaid
> classDiagram
>     class GUIFactory {
>         <<interface>>
>         +CreateButton()
>         +CreateInput()
>     }
>     class WindowsFactory {
>         +CreateButton()
>         +CreateInput()
>     }
>     class MacFactory {
>         +CreateButton()
>         +CreateInput()
>     }
>     class Button {
>         <<interface>>
>         +Render()
>     }
>     class Input {
>         <<interface>>
>         +Render()
>     }
>
>     GUIFactory <|.. WindowsFactory
>     GUIFactory <|.. MacFactory
>     Button <|.. WindowsButton
>     Button <|.. MacButton
>     Input <|.. WindowsInput
>     Input <|.. MacInput
> ```

---

## 38.3 建造者模式

> 🏗️ **建造者模式**用于构建复杂对象。当一个对象的构造过程需要多个步骤，或者有多个可选参数时，建造者模式就派上用场了。

### 38.3.1 功能选项模式

Go 中最著名的"建造者模式"变体：**Functional Options Pattern（功能选项模式）**。这种模式在 Go 的标准库中广泛使用，比如 `http.Server` 的配置：

```go
package main

import (
    "fmt"
    "time"
)

// Server 服务器选项
type Server struct {
    addr     string
    port     int
    timeout  time.Duration
    maxConns int
    enabled  bool
}

// ServerOption 服务器配置选项
type ServerOption func(*Server)

// WithAddr 设置地址
func WithAddr(addr string) ServerOption {
    return func(s *Server) {
        s.addr = addr
    }
}

// WithPort 设置端口
func WithPort(port int) ServerOption {
    return func(s *Server) {
        s.port = port
    }
}

// WithTimeout 设置超时
func WithTimeout(timeout time.Duration) ServerOption {
    return func(s *Server) {
        s.timeout = timeout
    }
}

// WithMaxConns 设置最大连接数
func WithMaxConns(maxConns int) ServerOption {
    return func(s *Server) {
        s.maxConns = maxConns
    }
}

// WithEnabled 设置是否启用
func WithEnabled(enabled bool) ServerOption {
    return func(s *Server) {
        s.enabled = enabled
    }
}

// NewServer 创建服务器
func NewServer(opts ...ServerOption) *Server {
    server := &Server{
        addr:    "localhost",
        port:    8080,
        timeout: 30 * time.Second,
        maxConns: 100,
        enabled:  true,
    }

    // 应用所有选项
    for _, opt := range opts {
        opt(server)
    }

    return server
}

func main() {
    fmt.Println("=== 功能选项模式 ===")

    // 使用默认配置
    server1 := NewServer()
    fmt.Printf("默认配置: %+v\n", server1) // &{addr:localhost port:8080 timeout:30s maxConns:100 enabled:true}

    // 使用选项自定义
    server2 := NewServer(
        WithAddr("0.0.0.0"),
        WithPort(9090),
        WithTimeout(60*time.Second),
        WithMaxConns(500),
    )
    fmt.Printf("自定义配置: %+v\n", server2) // &{addr:0.0.0.0 port:9090 timeout:1m0s maxConns:500 enabled:true}
}
```

### 38.3.2 链式建造者

传统的链式建造者：

```go
package main

import "fmt"

// User 用户建造者
type UserBuilder struct {
    user *User
}

type User struct {
    Name    string
    Age     int
    Email   string
    Phone   string
    Address string
}

func (b *UserBuilder) Name(name string) *UserBuilder {
    b.user.Name = name
    return b // 返回 builder 以支持链式调用
}

func (b *UserBuilder) Age(age int) *UserBuilder {
    b.user.Age = age
    return b
}

func (b *UserBuilder) Email(email string) *UserBuilder {
    b.user.Email = email
    return b
}

func (b *UserBuilder) Phone(phone string) *UserBuilder {
    b.user.Phone = phone
    return b
}

func (b *UserBuilder) Address(address string) *UserBuilder {
    b.user.Address = address
    return b
}

func (b *UserBuilder) Build() *User {
    return b.user
}

func NewUserBuilder() *UserBuilder {
    return &UserBuilder{user: &User{}}
}

func main() {
    fmt.Println("=== 链式建造者 ===")

    user := NewUserBuilder().
        Name("张三").
        Age(25).
        Email("zhang@example.com").
        Phone("13800138000").
        Address("北京市朝阳区").
        Build()

    fmt.Printf("构建的用户: %+v\n", user) // &{Name:张三 Age:25 Email:zhang@example.com Phone:13800138000 Address:北京市朝阳区}
}
}
```

---

## 38.4 原型模式

> 📋 **原型模式**用于创建重复的对象，同时保证性能。这种模式适合当直接创建一个对象的成本比较大时（比如从数据库读取）。

### 38.4.1 浅拷贝

Go 的 `copy` 函数可以用于切片和数组的浅拷贝：

```go
package main

import "fmt"

// Prototype 原型接口
type Prototype interface {
    Clone() Prototype
}

// ConcretePrototype 具体原型
type ConcretePrototype struct {
    ID      int
    Name    string
    Values  []string
    MapData map[string]int
}

// Clone 实现原型接口 - 浅拷贝
func (p *ConcretePrototype) Clone() Prototype {
    // 创建一个新的实例
    cloned := &ConcretePrototype{
        ID:      p.ID,
        Name:    p.Name,
        Values:  make([]string, len(p.Values)), // 复制切片
        MapData: make(map[string]int),           // 复制 map
    }

    // 复制切片内容（浅拷贝）
    copy(cloned.Values, p.Values)

    // 复制 map 内容（浅拷贝）
    for k, v := range p.MapData {
        cloned.MapData[k] = v
    }

    return cloned
}

func main() {
    fmt.Println("=== 原型模式 - 浅拷贝 ===")

    original := &ConcretePrototype{
        ID:      1,
        Name:    "原始对象",
        Values:  []string{"A", "B", "C"},
        MapData: map[string]int{"X": 1, "Y": 2},
    }

    cloned := original.Clone().(*ConcretePrototype)

    fmt.Printf("原始对象: %+v\n", original) // &{ID:1 Name:原始对象 Values:[A B C] MapData:map[X:1 Y:2]}
    fmt.Printf("克隆对象: %+v\n", cloned) // &{ID:1 Name:原始对象 Values:[A B C] MapData:map[X:1 Y:2]}

    // 修改克隆对象的基本类型字段
    cloned.ID = 2
    cloned.Name = "克隆对象"

    // 修改克隆对象的切片
    cloned.Values[0] = "X"

    // 修改克隆对象的 Map
    cloned.MapData["Z"] = 99

    fmt.Println("\n修改后：")
    fmt.Printf("原始对象: %+v\n", original) // &{ID:1 Name:原始对象 Values:[A B C] MapData:map[X:1 Y:2 Z:99]}
    fmt.Printf("克隆对象: %+v\n", cloned) // &{ID:2 Name:克隆对象 Values:[X B C] MapData:map[X:1 Y:2 Z:99]}

    // 注意：切片和 Map 的内容是共享的（浅拷贝特性）
    fmt.Printf("\n原始对象 Values[0]: %s (因为浅拷贝，值已变成 'X')", original.Values[0])
}
```

### 38.4.2 深拷贝

深拷贝会复制所有嵌套的对象：

```go
package main

import (
    "encoding/json"
    "fmt"
)

// DeepPrototype 深度拷贝原型
type DeepPrototype struct {
    ID      int
    Name    string
    Nested  *NestedData
    Items   []Item
}

// NestedData 嵌套数据
type NestedData struct {
    Value string
}

// Item 条目
type Item struct {
    ID   int
    Name string
}

// Clone 深拷贝
func (p *DeepPrototype) Clone() *DeepPrototype {
    // 方法一：使用 JSON 序列化（简单但有性能开销）
    data, err := json.Marshal(p)
    if err != nil {
        panic(err)
    }

    var cloned DeepPrototype
    if err := json.Unmarshal(data, &cloned); err != nil {
        panic(err)
    }

    return &cloned
}

func main() {
    fmt.Println("=== 原型模式 - 深拷贝 ===")

    original := &DeepPrototype{
        ID:   1,
        Name: "原始对象",
        Nested: &NestedData{
            Value: "嵌套值",
        },
        Items: []Item{
            {ID: 1, Name: "条目1"},
            {ID: 2, Name: "条目2"},
        },
    }

    cloned := original.Clone()

    fmt.Printf("原始对象: %+v\n", original) // &{ID:1 Name:原始对象 Nested:0x... Items:[{1 条目1} {2 条目2}]}
    fmt.Printf("克隆对象: %+v\n", cloned) // &{ID:1 Name:原始对象 Nested:0x... Items:[{1 条目1} {2 条目2}]}

    // 修改克隆对象
    cloned.Nested.Value = "被修改的嵌套值"
    cloned.Items[0].Name = "被修改的条目"

    fmt.Println("\n修改克隆对象后：")
    fmt.Printf("原始对象 Nested.Value: %s\n", original.Nested.Value) // 嵌套值（深拷贝，互不影响）
    fmt.Printf("克隆对象 Nested.Value: %s\n", cloned.Nested.Value) // 被修改的嵌套值
    fmt.Printf("原始对象 Items[0].Name: %s\n", original.Items[0].Name) // 条目1（深拷贝，互不影响）
    fmt.Printf("克隆对象 Items[0].Name: %s\n", cloned.Items[0].Name) // 被修改的条目
}
```

---

## 38.5 对象池模式

> 🏊 **对象池模式**是一种预先分配和重用对象的模式，特别适合那些创建成本较高（如数据库连接、线程）的场景。

### 38.5.1 sync.Pool 实现

Go 标准库的 `sync.Pool` 是对象池的完美实现：

```go
package main

import (
    "fmt"
    "sync"
    "time"
)

// Pool 对象池示例
type Pool struct {
    pool sync.Pool
}

// NewPool 创建对象池
func NewPool(createFunc func() interface{}) *Pool {
    return &Pool{
        pool: sync.Pool{
            New: createFunc,
        },
    }
}

// Get 获取对象
func (p *Pool) Get() interface{} {
    return p.pool.Get()
}

// Put 归还对象
func (p *Pool) Put(obj interface{}) {
    p.pool.Put(obj)
}

// ExpensiveObject 模拟重量级对象
type ExpensiveObject struct {
    ID   int
    Data [1024]byte // 模拟大内存占用
}

func main() {
    fmt.Println("=== sync.Pool 对象池 ===")

    // 创建对象池
    pool := NewPool(func() interface{} {
        fmt.Println("对象池：创建新对象")
        return &ExpensiveObject{ID: 1}
    })

    // 从池中获取对象
    obj1 := pool.Get().(*ExpensiveObject)
    fmt.Printf("获取对象: ID=%d\n", obj1.ID) // 1

    // 用完后归还
    pool.Put(obj1)

    // 再次获取，可能复用之前的对象
    obj2 := pool.Get().(*ExpensiveObject)
    fmt.Printf("再次获取对象: ID=%d\n", obj2.ID) // 1 (复用了之前归还的对象)

    // 性能测试
    benchmarkPool()
}

func benchmarkPool() {
    pool := NewPool(func() interface{} {
        return make([]byte, 1024) // 模拟分配 1KB
    })

    iterations := 1000000

    start := time.Now()
    for i := 0; i < iterations; i++ {
        obj := pool.Get().([]byte)
        pool.Put(obj)
    }
    elapsed := time.Since(start)

    fmt.Printf("\n对象池性能: %d 次获取/归还耗时 %v\n", iterations, elapsed) // 例如: 1000000 次获取/归还耗时 123.456ms
    fmt.Printf("平均每次操作: %d 纳秒\n", elapsed.Nanoseconds()/int64(iterations)) // 例如: 123456 纳秒
}
```

### 38.5.2 自定义对象池

有时候你需要更精细的控制：

```go
package main

import (
    "container/list"
    "fmt"
    "sync"
)

// GenericPool 通用对象池
type GenericPool struct {
    mu    sync.Mutex
    list  *list.List
    New   func() interface{} // 创建新对象的函数
    Reset func(interface{})   // 重置对象的函数
}

// NewGenericPool 创建通用对象池
func NewGenericPool(newFunc, resetFunc func(interface{})) *GenericPool {
    return &GenericPool{
        list:  list.New(),
        New:   newFunc,
        Reset: resetFunc,
    }
}

// Acquire 获取对象
func (p *GenericPool) Acquire() interface{} {
    p.mu.Lock()
    defer p.mu.Unlock()

    if p.list.Len() == 0 {
        return p.New()
    }

    // 从列表头部取出
    ele := p.list.Remove(p.list.Front())
    return ele
}

// Release 释放对象
func (p *GenericPool) Release(obj interface{}) {
    if p.Reset != nil {
        p.Reset(obj)
    }

    p.mu.Lock()
    defer p.mu.Unlock()

    p.list.PushBack(obj)
}

func main() {
    fmt.Println("=== 自定义对象池 ===")

    // 创建一个缓冲区池
    bufferPool := NewGenericPool(
        func() interface{} {
            return make([]byte, 1024)
        },
        func(obj interface{}) {
            // 重置缓冲区
            b := obj.([]byte)
            for i := range b {
                b[i] = 0
            }
        },
    )

    // 获取缓冲区
    buf1 := bufferPool.Acquire().([]byte)
    fmt.Printf("获取缓冲区: 长度=%d, 容量=%d\n", len(buf1), cap(buf1)) // 长度=1024, 容量=1024

    // 使用缓冲区
    for i := 0; i < 10; i++ {
        buf1[i] = byte('A' + i)
    }
    fmt.Printf("写入数据: %s\n", string(buf1[:10])) // ABCDEFGHIJ

    // 释放回池
    bufferPool.Release(buf1)

    // 再次获取
    buf2 := bufferPool.Acquire().([]byte)
    fmt.Printf("再次获取缓冲区: 前10字节=%v (已被清零)\n", buf2[:10]) // [0 0 0 0 0 0 0 0 0 0]
}
}
```

### 38.5.3 池化策略

不同的池化策略适用于不同的场景：

```go
package main

import (
    "fmt"
    "sync"
    "time"
)

// PoolStrategy 池策略接口
type PoolStrategy interface {
    Acquire() interface{}
    Release(interface{})
    Close()
}

// LIFOPool 后进先出池（默认策略）
type LIFOPool struct {
    pool sync.Pool
}

func NewLIFOPool(newFunc func() interface{}) *LIFOPool {
    return &LIFOPool{
        pool: sync.Pool{New: newFunc},
    }
}

func (p *LIFOPool) Acquire() interface{} {
    return p.pool.Get()
}

func (p *LIFOPool) Release(obj interface{}) {
    p.pool.Put(obj)
}

func (p *LIFOPool) Close() {
    // sync.Pool 没有 Close 方法
}

// AdaptivePool 自适应池（根据使用情况动态调整）
type AdaptivePool struct {
    mu           sync.Mutex
    available    []interface{}
    inUse        int
    maxSize      int
    minSize      int
    newFunc      func() interface{}
}

func NewAdaptivePool(min, max int, newFunc func() interface{}) *AdaptivePool {
    pool := &AdaptivePool{
        maxSize: max,
        minSize: min,
        newFunc: newFunc,
    }

    // 预热池
    for i := 0; i < min; i++ {
        pool.available = append(pool.available, newFunc())
    }

    return pool
}

func (p *AdaptivePool) Acquire() interface{} {
    p.mu.Lock()
    defer p.mu.Unlock()

    p.inUse++

    if len(p.available) > 0 {
        obj := p.available[len(p.available)-1]
        p.available = p.available[:len(p.available)-1]
        return obj
    }

    return p.newFunc()
}

func (p *AdaptivePool) Release(obj interface{}) {
    p.mu.Lock()
    defer p.mu.Unlock()

    p.inUse--

    // 如果当前池大小超过最小值，可以释放一些对象
    if len(p.available) < p.minSize {
        p.available = append(p.available, obj)
    }
    // 否则丢弃（让 GC 回收）
}

func (p *AdaptivePool) Close() {
    p.mu.Lock()
    defer p.mu.Unlock()
    p.available = nil
}

func main() {
    fmt.Println("=== 池化策略 ===")

    // LIFO 策略（默认）
    lifoPool := NewLIFOPool(func() interface{} {
        return make([]byte, 1024)
    })

    buf1 := lifoPool.Acquire().([]byte)
    buf2 := lifoPool.Acquire().([]byte)

    lifoPool.Release(buf1)
    lifoPool.Release(buf2)

    // buf2 会被优先复用（因为是最后放入的）
    buf3 := lifoPool.Acquire().([]byte)
    fmt.Printf("LIFO: 复用了最后放入的对象\n")

    // 自适应池
    adaptivePool := NewAdaptivePool(2, 10, func() interface{} {
        fmt.Println("创建新对象")
        return make([]byte, 1024)
    })

    fmt.Println("\n自适应池示例：")
    for i := 0; i < 5; i++ {
        obj := adaptivePool.Acquire()
        adaptivePool.Release(obj)
    }
}
```

---

## 38.6 依赖注入

> 💉 **依赖注入（DI）**是一种实现控制反转（IoC）的技术。通过依赖注入，对象的依赖由外部在运行时提供，而不是在对象内部创建。

### 38.6.1 构造函数注入

最简单的依赖注入方式：通过构造函数接收依赖：

```go
package main

import "fmt"

// Logger 日志接口
type Logger interface {
    Log(msg string)
}

// ConsoleLogger 控制台日志
type ConsoleLogger struct{}

func (l *ConsoleLogger) Log(msg string) {
    fmt.Printf("[控制台] %s\n", msg)
}

// FileLogger 文件日志
type FileLogger struct {
    filename string
}

func (l *FileLogger) Log(msg string) {
    fmt.Printf("[文件:%s] %s\n", l.filename, msg)
}

// UserService 依赖 Logger
type UserService struct {
    logger Logger
}

// NewUserService 构造函数注入
func NewUserService(logger Logger) *UserService {
    return &UserService{logger: logger}
}

func (s *UserService) CreateUser(name string) {
    s.logger.Log("创建用户: " + name)
}

func main() {
    fmt.Println("=== 构造函数注入 ===")

    // 注入控制台日志
    consoleLogger := &ConsoleLogger{}
    userService1 := NewUserService(consoleLogger)
    userService1.CreateUser("张三")

    // 注入文件日志
    fileLogger := &FileLogger{filename: "app.log"}
    userService2 := NewUserService(fileLogger)
    userService2.CreateUser("李四")
}
```

### 38.6.2 属性注入

通过公开属性（字段）注入依赖：

```go
package main

import "fmt"

// Cache 缓存接口
type Cache interface {
    Get(key string) string
}

// MemoryCache 内存缓存
type MemoryCache struct {
    data map[string]string
}

func NewMemoryCache() *MemoryCache {
    return &MemoryCache{data: make(map[string]string)}
}

func (c *MemoryCache) Get(key string) string {
    return c.data[key]
}

// ProductService 属性注入
type ProductService struct {
    Cache  Cache  // 公开字段
    Logger Logger // 另一个依赖
}

func (s *ProductService) GetProduct(id string) string {
    if s.Cache != nil {
        if cached := s.Cache.Get(id); cached != "" {
            s.Logger.Log("缓存命中: " + id)
            return cached
        }
    }

    // 模拟从数据库读取
    product := "产品: " + id
    s.Logger.Log("从数据库读取: " + id)
    return product
}

func main() {
    fmt.Println("=== 属性注入 ===")

    service := &ProductService{}

    // 注入依赖
    service.Cache = NewMemoryCache()
    service.Logger = &ConsoleLogger{}

    // 使用服务
    service.GetProduct("P001")
    service.GetProduct("P001") // 第二次应该命中缓存
}
```

### 38.6.3 接口注入

通过接口方法注入依赖：

```go
package main

import "fmt"

// Injectable 可注入接口
type Injectable interface {
    InjectLogger(Logger)
}

// DetailedService 接口注入
type DetailedService struct {
    logger Logger
}

func (s *DetailedService) InjectLogger(logger Logger) {
    s.logger = logger
}

func (s *DetailedService) Process() {
    s.logger.Log("处理中...") // 输出: [控制台] 处理中...
}

func main() {
    fmt.Println("=== 接口注入 ===")

    service := &DetailedService{}

    // 通过接口注入
    var injectable Injectable = service
    injectable.InjectLogger(&ConsoleLogger{})

    service.Process() // 输出: [控制台] 处理中...
}
```

### 38.6.4 依赖注入框架

在大型项目中，手动注入依赖会变得繁琐。Go 中常用的 DI 框架有：

| 框架 | 特点 |
|------|------|
| google/wire | 编译时代码生成，性能好 |
| uber-go/dig | 运行时反射，简单易用 |
| facebookgo/inject | 自动注入 |
| rsms-service/di | 轻量级 |

**使用 uber-go/dig 示例**：

```go
package main

import (
    "fmt"
    "go.uber.org/dig"
)

// 依赖定义
type Config struct {
    DBHost string
    DBPort int
}

type Database struct {
    Config Config
}

type Handler struct {
    DB *Database
}

func NewDatabase(cfg Config) *Database {
    return &Database{Config: cfg}
}

func NewHandler(db *Database) *Handler {
    return &Handler{DB: db}
}

func main() {
    fmt.Println("=== dig 依赖注入框架 ===")

    container := dig.New()

    // 注册依赖
    container.Provide(func() Config {
        return Config{DBHost: "localhost", DBPort: 5432}
    })
    container.Provide(NewDatabase)
    container.Provide(NewHandler)

    // 解析依赖
    err := container.Invoke(func(h *Handler) {
        fmt.Printf("Handler 注入成功: %+v\n", h)
    })

    if err != nil {
        panic(err)
    }
}
```

---

## 本章小结

> 🎉 恭喜你完成了创建型模式的学习！这一章我们探索了 5 种创建型设计模式。

### 核心要点回顾

1. **单例模式**：确保一个类只有一个实例，并提供全局访问点。Go 中推荐使用 `sync.Once` 实现。

2. **工厂模式**：将对象的创建与使用分离。简单工厂适用于简单场景，抽象工厂适用于创建一系列相关对象。

3. **建造者模式**：分步骤构建复杂对象。Go 的"功能选项模式"是其最佳实践。

4. **原型模式**：通过克隆现有对象创建新对象。有浅拷贝和深拷贝之分。

5. **对象池模式**：预先分配和重用对象，减少对象创建开销。`sync.Pool` 是标准库的实现。

6. **依赖注入**：通过外部注入依赖，实现控制反转。构造函数注入是最简单的方式。

### 模式对比

| 模式 | 适用场景 | Go 实现建议 |
|------|----------|-------------|
| 单例 | 全局唯一资源 | sync.Once |
| 工厂 | 对象创建逻辑复杂 | 函数返回接口 |
| 建造者 | 多步骤/多参数构建 | Functional Options |
| 原型 | 相似对象批量创建 | Clone 方法 |
| 对象池 | 重量级对象复用 | sync.Pool |
| DI | 解耦组件依赖 | 构造函数注入 / wire |

> 💡 **最后一句话**：设计模式是经验总结，不是银弹。选择哪种模式，要根据实际场景来决定。在 Go 中，很多传统模式都有更简洁的实现方式（如用 `sync.Once` 代替懒加载单例）。理解模式的本质，而不是死记硬背代码结构。

