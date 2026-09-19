+++
title = "第23章 类型选择"
weight = 230
date = "2026-03-20T08:39:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++
# 第23章 类型选择

> 类型选择（type switch）是Go语言处理多种接口类型的"超级开关"。如果说普通switch是根据值来选择分支，那type switch就是根据**类型**来选择分支。

## 23.1 type switch 语法

### 23.1.1 基本语法

type switch的语法和普通switch类似，但case比较的是类型而不是值。关键字是`i.(type)`，它只能在type switch中使用：

```go
package main

import "fmt"

// Any 是空接口，相当于"任意类型"
type Any interface{}

func inspectType(i Any) {
    // 固定语法：switch v := i.(type)
    // v会自动获得i的实际类型值
    switch v := i.(type) {
    case nil:                        // i是nil时
        fmt.Println("i是nil，类型未知")
    case int:                        // i是int时
        fmt.Printf("i是int，值: %d\n", v)
    case string:                     // i是string时
        fmt.Printf("i是string，值: %q\n", v)
    case bool:                       // i是bool时
        fmt.Printf("i是bool，值: %t\n", v)
    case float64:                    // i是float64时
        fmt.Printf("i是float64，值: %f\n", v)
    default:                         // 前面都没匹配
        fmt.Printf("i是其他类型: %T\n", v)
    }
}

func main() {
    fmt.Println("=== type switch 基本用法 ===")
    inspectType(nil)              // i是nil，类型未知
    inspectType(42)               // i是int，值: 42
    inspectType("hello")           // i是string，值: "hello"
    inspectType(true)              // i是bool，值: true
    inspectType(3.14)             // i是float64，值: 3.140000
    inspectType([]int{1, 2, 3})   // i是其他类型: []int
}
```

**语法解释：**
```go
switch v := i.(type) {  // 固定写法
case int:               // 如果i的实际类型是int
    // v是int类型的值
case string:
    // v是string类型的值
}
```

### 23.1.2 case 匹配多种类型

一个case可以同时匹配多种类型，用逗号分隔：

```go
package main

import "fmt"

type Any interface{}

func classifyNumber(i Any) {
    switch v := i.(type) {
    // 同时匹配所有整数类型
    case int8, int16, int32, int64:
        fmt.Printf("整数类型 %T，值: %d\n", v, v)
    // 同时匹配所有浮点数类型
    case float32, float64:
        fmt.Printf("浮点数类型 %T，值: %f\n", v, v)
    default:
        fmt.Printf("其他类型: %T\n", v)
    }
}

func main() {
    values := []Any{int8(10), int64(42), float32(3.14), float64(2.718)}

    for _, v := range values {
        classifyNumber(v)
    }

    // 整数类型 int8，值: 10
    // 整数类型 int64，值: 42
    // 浮点数类型 float32，值: 3.140000
    // 浮点数类型 float64，值: 2.718000
}
```

---

## 23.2 default 分支

### 23.2.1 default 是可选的

和普通switch一样，default也是可选的。如果没有default且所有case都不匹配，就什么都不做：

```go
package main

import "fmt"

type Any interface{}

func processNoDefault(i Any) {
    // 没有default分支
    switch v := i.(type) {
    case int:
        fmt.Printf("整数: %d\n", v)
    case string:
        fmt.Printf("字符串: %s\n", v)
    }
    // 如果都不匹配，函数直接结束
}

func main() {
    processNoDefault(42)              // 整数: 42
    processNoDefault("hello")          // 字符串: hello
    processNoDefault([]int{1, 2, 3})  // 没有任何输出！因为没有匹配任何case，也没有default
}
```

**什么时候需要default？**

```go
func handle(i Any) {
    switch v := i.(type) {
    case int:
        // 处理整数
    case string:
        // 处理字符串
    default:
        // 重要！如果我们不知道怎么处理这个类型，应该有个兜底方案
        fmt.Printf("未知类型: %T\n", v)
    }
}
```

---

## 23.3 与接口配合

### 23.3.1 多重分派（重要应用）

type switch最常见的用途之一是实现"多重分派"。当你有多种类型需要分别处理时，它比if-else链清晰得多：

```go
package main

import "fmt"

// Shape 定义几何图形接口
type Shape interface {
    Area() float64  // 所有图形都能计算面积
}

type Circle struct {
    Radius float64
}

func (c Circle) Area() float64 {
    return 3.14159 * c.Radius * c.Radius
}

type Rectangle struct {
    Width, Height float64
}

func (r Rectangle) Area() float64 {
    return r.Width * r.Height
}

type Triangle struct {
    Base, Height float64
}

func (t Triangle) Area() float64 {
    return 0.5 * t.Base * t.Height
}

// describeShape 根据具体类型打印不同的描述
// 这就是"多重分派"——同一个函数，不同类型不同行为
func describeShape(s Shape) {
    switch v := s.(type) {
    case Circle:
        // v是Circle类型，可以直接访问Circle的字段
        fmt.Printf("圆形: 半径=%.2f, 面积=%.2f\n", v.Radius, v.Area())
    case Rectangle:
        fmt.Printf("矩形: 宽=%.2f, 高=%.2f, 面积=%.2f\n", v.Width, v.Height, v.Area())
    case Triangle:
        fmt.Printf("三角形: 底=%.2f, 高=%.2f, 面积=%.2f\n", v.Base, v.Height, v.Area())
    default:
        fmt.Printf("未知形状: %T\n", s)
    }
}

func main() {
    // 创建不同类型的Shape
    shapes := []Shape{
        Circle{Radius: 5},
        Rectangle{Width: 4, Height: 6},
        Triangle{Base: 3, Height: 4},
    }

    // 同一个函数，不同类型，不同输出
    for _, s := range shapes {
        describeShape(s)
    }

    // 圆形: 半径=5.00, 面积=78.54
    // 矩形: 宽=4.00, 高=6.00, 面积=24.00
    // 三角形: 底=3.00, 高=4.00, 面积=6.00
}
```

**多重分派的好处：**

```go
// ❌ 不用type switch的写法：繁琐
func describeShape(s Shape) {
    if c, ok := s.(Circle); ok {
        fmt.Printf("圆形: 半径=%.2f\n", c.Radius)
    } else if r, ok := s.(Rectangle); ok {
        fmt.Printf("矩形: 宽=%.2f, 高=%.2f\n", r.Width, r.Height)
    } else if ...
}

// ✅ 用type switch的写法：清晰
func describeShape(s Shape) {
    switch v := s.(type) {
    case Circle:
        fmt.Printf("圆形: 半径=%.2f\n", v.Radius)
    case Rectangle:
        fmt.Printf("矩形: 宽=%.2f, 高=%.2f\n", v.Width, v.Height)
    }
}
```

### 23.3.2 处理器模式（实际应用）

在Web框架、RPC框架中，经常需要根据请求类型调用不同的处理器。type switch是实现这个模式的好方法：

```go
package main

import "fmt"

// Handler 接口：所有处理器都要实现Handle方法
type Handler interface {
    Handle()
}

// fileHandler 处理文件相关请求
type fileHandler struct {
    filename string
}

func (m *fileHandler) Handle() {
    fmt.Printf("[fileHandler] 正在读取文件: %s\n", m.filename)
    // 实际会调用 os.ReadFile(m.filename)
}

type HttpHandler struct {
    path string
}

func (h *HttpHandler) Handle() {
    fmt.Printf("[HttpHandler] 正在处理HTTP请求: %s\n", h.path)
    // 实际会调用 http.Handle(h.path, ...)
}

type GrpcHandler struct {
    service string
}

func (g *GrpcHandler) Handle() {
    fmt.Printf("[GrpcHandler] 正在处理gRPC调用: %s\n", g.service)
    // 实际会调用 grpc.RegisterService(g.service)
}

// dispatch 根据handler的具体类型进行分派
// 这就是"处理器模式"的核心
func dispatch(h Handler) {
    switch v := h.(type) {
    case *fileHandler:
        v.Handle()
    case *HttpHandler:
        v.Handle()
    case *GrpcHandler:
        v.Handle()
    default:
        fmt.Printf("未知处理器类型: %T，无法处理\n", h)
    }
}

func main() {
    // 创建不同类型的handler
    handlers := []Handler{
        &fileHandler{filename: "config.yaml"},
        &HttpHandler{path: "/api/users"},
        &GrpcHandler{service: "UserService"},
    }

    // 统一调度，不同类型自动分派到不同的处理函数
    for _, h := range handlers {
        dispatch(h)
    }

    // [fileHandler] 正在读取文件: config.yaml
    // [HttpHandler] 正在处理HTTP请求: /api/users
    // [GrpcHandler] 正在处理gRPC调用: UserService
}
```

---

## 23.4 嵌套 type switch

### 23.4.1 外层 type switch，内层普通 switch

type switch 的每个分支里，变量已经被转换成对应类型，因此可以在分支内部再写一个针对**具体类型**的普通 switch，两层互不干扰：

```go
package main

import "fmt"

type Any interface{}

func inspectDeep(i Any) {
    // 外层：先判断大类
    switch v := i.(type) {
    case int:
        // 内层：再细分
        switch {
        case v < 0:
            fmt.Printf("负整数: %d\n", v)
        case v == 0:
            fmt.Printf("零: %d\n", v)
        default:
            fmt.Printf("正整数: %d\n", v)
        }
    case string:
        switch {
        case len(v) == 0:
            fmt.Println("空字符串")
        case len(v) < 5:
            fmt.Printf("短字符串: %q\n", v)
        default:
            fmt.Printf("长字符串: %q\n", v)
        }
    default:
        fmt.Printf("其他类型: %T\n", v)
    }
}

func main() {
    inspectDeep(-5)           // 负整数: -5
    inspectDeep(0)           // 零: 0
    inspectDeep(42)          // 正整数: 42
    inspectDeep("")          // 空字符串
    inspectDeep("hi")        // 短字符串: "hi"
    inspectDeep("hello")     // 长字符串: "hello"
}
```

---

## 本章小结

本章我们学习了type switch：

**基本语法：**
```go
switch v := i.(type) {
case nil:
    // i是nil
case int:
    // v是int类型
case string:
    // v是string类型
default:
    // 未知类型
}
```

**使用场景：**
- **多重分派**：同一函数，不同类型不同行为
- **类型检查**：判断接口值的实际类型
- **处理器模式**：根据类型分派到不同处理器

**注意事项：**
- `i.(type)`只能在switch内使用
- case可以匹配多个类型，用逗号分隔
- default是可选的

**vs 类型断言：**
```go
// if-else链
if v, ok := i.(int); ok {
    // 处理int
} else if v, ok := i.(string); ok {
    // 处理string
}

// type switch（更清晰）
switch v := i.(type) {
case int:
    // 处理int
case string:
    // 处理string
}
```
