+++
title = "第16章 函数类型"
weight = 160
date = "2026-03-20T08:39:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false

+++
# 第16章 函数类型

> "函数是 Go 的一等公民（first-class citizen）。" —— 这是 Go 语言的设计哲学之一。

在 Go 里，函数不只是用来调用的代码块——**函数本身也是一种类型**，可以像变量一样赋值、传递、作为参数、作为返回值。听起来有点抽象，但它带来的编程范式革命是巨大的：你可以在 Go 里写高阶函数、装饰器、回调、策略模式——这些在其他语言里需要特殊语法才能做到的事情，在 Go 里只是普通代码。

---

## 16.1 函数类型定义

### 16.1.1 参数列表

函数类型由它的参数列表和结果列表决定：

```go
// 参数列表决定函数类型的签名
type AddFunc func(a, b int) int

// 使用
var add AddFunc = func(a, b int) int {
    return a + b
}
fmt.Println(add(1, 2))  // 3
```

`AddFunc` 是一个函数类型：接收两个 `int`，返回一个 `int`。所有满足这个签名的函数都可以赋值给 `AddFunc` 类型的变量。

### 16.1.2 结果列表

函数类型的结果列表也是类型签名的一部分：

```go
type Processor func(input string) (output string, err error)

// processor1 和 processor2 可以赋给 Processor 类型的变量
processor1 := func(input string) (string, error) {
    return strings.ToUpper(input), nil
}
processor2 := func(input string) (string, error) {
    return strings.ToLower(input), nil
}

var proc Processor = processor1
fmt.Println(proc("Hello"))  // HELLO <nil>
```

---

## 16.2 函数值

### 16.2.1 函数变量

函数可以像普通变量一样赋值、传递：

```go
import "strings"

// 标准库函数可以直接赋给同签名的函数类型变量
var toUpper func(string) string = strings.ToUpper
fmt.Println(toUpper("hello"))  // HELLO

// 函数变量之间也可以互相赋值（只要签名一致）
toUpper2 := toUpper
fmt.Println(toUpper2("world"))  // WORLD

// 不同签名的函数不能互相赋值
// var bad func(string) (string, error) = strings.ToUpper  // 编译错误：类型不匹配
```

> 函数变量本质上是一个指向代码的指针加上捕获的闭包环境，所以它的零值是 `nil`，而且**不能用作 map 的键**、也不能用 `==` 比较（见 16.3 节）。

### 16.2.2 nil 函数值

声明但未赋值的函数类型变量默认是 `nil`：

```go
var f func(int) int
fmt.Println(f == nil)  // true

// 调用 nil 函数会 panic
// f(1) // panic: runtime error: invalid memory address or nil pointer dereference
```

这意味着在调用函数值之前，**一定要检查它是否为 nil**：

```go
var f func(int) int

if f != nil {
    fmt.Println(f(10))
} else {
    fmt.Println("f is nil, skip calling")
}
```

---

## 16.3 函数不能比较

Go 里**函数值之间不能比较**——`==` 和 `!=` 都不行。唯一的例外是和 `nil` 比较：

```go
add := func(a, b int) int { return a + b }
add2 := add
add3 := func(a, b int) int { return a + b }

fmt.Println(add == nil)    // false —— 和 nil 比较是允许的
fmt.Println(add2 == nil)   // false

// fmt.Println(add == add2)  // 编译错误：invalid operation: add == add2 (func can only be compared to nil)
// fmt.Println(add == add3)  // 同样是编译错误，跟两个函数是不是同一段代码无关
```

> 为什么不允许？因为闭包让“相等”没有合理的定义：两个由同一个字面量生成的函数，捕获的环境可能不同，底层实现也可能不同。语言干脆规定函数类型**不可比较**（因此也不能做 map 的键），只留下“是不是 nil”这一个判断。
>
> 如果你确实需要区分两个函数，通常是给它加一个可比较的标识（比如 ID 或名字），比较那个标识，而不是比较函数本身。

---

## 16.4 函数模式

### 16.4.1 回调模式

把函数作为参数传递给另一个函数，实现"回调"：

```go
import "fmt"

type VisitFunc func(int)

// 对切片中每个元素执行回调
func visit(nums []int, fn VisitFunc) {
    for _, n := range nums {
        fn(n)
    }
}

nums := []int{1, 2, 3, 4, 5}

visit(nums, func(n int) {
    fmt.Printf("%d*2=%d\n", n, n*2)
})
// 1*2=2
// 2*2=4
// 3*2=6
// 4*2=8
// 5*2=10
```

### 16.4.2 策略模式

把不同的算法封装成函数，根据需要选择不同的策略：

```go
type SortStrategy func(items []int) []int

func bubbleSort(items []int) []int {
    // 冒泡排序实现...
    result := make([]int, len(items))
    copy(result, items)
    for i := 0; i < len(result); i++ {
        for j := 1; j < len(result)-i; j++ {
            if result[j] < result[j-1] {
                result[j], result[j-1] = result[j-1], result[j]
            }
        }
    }
    return result
}

func quickSort(items []int) []int {
    // 快速排序实现...
    if len(items) < 2 {
        return items
    }
    pivot := items[0]
    var left, right []int
    for _, v := range items[1:] {
        if v < pivot {
            left = append(left, v)
        } else {
            right = append(right, v)
        }
    }
    left = quickSort(left)
    right = quickSort(right)
    return append(append(left, pivot), right...)
}

func sortItems(items []int, strategy SortStrategy) []int {
    return strategy(items)
}

data := []int{5, 2, 8, 1, 9}
fmt.Println(sortItems(data, bubbleSort))  // [1 2 5 8 9]
fmt.Println(sortItems(data, quickSort))   // [1 2 5 8 9]
fmt.Println(data)                         // [5 2 8 1 9] —— 原切片没被动过
```

> 注意这两个排序函数都先复制了输入再排序（`bubbleSort` 用 `copy`，`quickSort` 用 `append` 生成新切片），所以调用 `sortItems` 不会修改调用方的 `data`。这是作为“策略”传进来的函数应该遵守的约定之一。

### 16.4.3 装饰器模式

用一个函数包装另一个函数，在其执行前后加上额外的行为：

```go
type Handler func() string

// 装饰器：计时
func withTimer(next Handler) Handler {
    return func() string {
        start := time.Now()
        result := next()
        fmt.Printf("took %v\n", time.Since(start))
        return result
    }
}

// 装饰器：重试
func withRetry(next Handler) Handler {
    return func() string {
        for i := 0; i < 3; i++ {
            result := next()
            if result != "" {
                return result
            }
            fmt.Println("retry...", i+1)
        }
        return ""
    }
}

handler := func() string {
    return "done"
}

// 链式装饰
wrapped := withRetry(withTimer(handler))
fmt.Println(wrapped())
```

### 16.4.4 中间件模式

在 web 服务中，中间件就是一个接收 `http.HandlerFunc`、返回 `http.HandlerFunc` 的函数：

```go
import (
    "fmt"
    "net/http"
    "time"
)

func loggingMiddleware(next http.HandlerFunc) http.HandlerFunc {
    return func(w http.ResponseWriter, r *http.Request) {
        start := time.Now()
        next.ServeHTTP(w, r)
        fmt.Printf("%s %s took %v\n", r.Method, r.URL.Path, time.Since(start))
    }
}

func authMiddleware(next http.HandlerFunc) http.HandlerFunc {
    return func(w http.ResponseWriter, r *http.Request) {
        if r.Header.Get("Authorization") == "" {
            http.Error(w, "Unauthorized", http.StatusUnauthorized)
            return
        }
        next.ServeHTTP(w, r)
    }
}

helloHandler := func(w http.ResponseWriter, r *http.Request) {
    fmt.Fprintln(w, "Hello, World!")
}

// 中间件的包裹顺序 = 执行顺序的外到内：
// 请求先被 loggingMiddleware 打点计时，再交给 authMiddleware 鉴权，最后才到业务处理
wrapped := loggingMiddleware(authMiddleware(helloHandler))
// http.HandleFunc("/hello", wrapped)
fmt.Println("Middleware chain ready!")
```

> 顺带一提：`http.HandlerFunc` 本身就是一个“把普通函数包装成接口实现”的适配器——它是函数类型，同时实现了 `http.Handler` 的 `ServeHTTP` 方法。所以这里的 `next.ServeHTTP(w, r)` 和 `next(w, r)` 完全等价。

---
