+++
title = "第22章 类型断言"
weight = 220
date = "2026-03-20T08:39:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++
# 第22章 类型断言

> 类型断言是Go语言处理接口值的"透视镜"。它允许你"窥视"接口内部，提取出具体的类型和值。

## 22.1 断言语法

### 22.1.1 直接断言

```go
package main

import "fmt"

type Writer interface {
    Write(p []byte) (n int, err error)
}

type File struct {
    name string
}

func (f *File) Write(p []byte) (n int, err error) {
    fmt.Printf("[File] 写入文件 %s: %s\n", f.name, string(p)) // [File] 写入文件 test.txt: Hello
    return len(p), nil
}

type StringWriter struct{}

func (s *StringWriter) Write(p []byte) (n int, err error) {
    fmt.Printf("[StringWriter] 写入: %s\n", string(p)) // [StringWriter] 写入: Another message
    return len(p), nil
}

func main() {
    var w Writer = &File{name: "test.txt"}
    f := w.(*File)
    fmt.Printf("断言成功，文件名: %s\n", f.name) // 断言成功，文件名: test.txt

    var w2 Writer = &StringWriter{}
    fmt.Printf("w2的类型: %T\n", w2) // w2的类型: *main.StringWriter
}
```

### 22.1.2 comma-ok 断言

```go
package main

import "fmt"

func main() {
    var i interface{} = "hello world"

    if str, ok := i.(string); ok {
        fmt.Printf("断言成功: %q\n", str) // 断言成功: "hello world"
    }

    var i2 interface{} = 42
    if str, ok := i2.(string); ok {
        fmt.Printf("这行不会打印: %q\n", str)
    } else {
        fmt.Println("断言失败，i2不是string类型，是int") // 断言失败，i2不是string类型，是int
    }
}
```

### 22.1.3 多个类型尝试

```go
package main

import "fmt"

type Any interface{}

func inspect(i Any) {
    if v, ok := i.(string); ok {
        fmt.Printf("字符串类型: %q\n", v) // 字符串类型: "hello"
        return
    }

    if v, ok := i.(int); ok {
        fmt.Printf("整数类型: %d\n", v) // 整数类型: 42
        return
    }

    if v, ok := i.(float64); ok {
        fmt.Printf("浮点数类型: %f\n", v) // 浮点数类型: 3.140000
        return
    }

    fmt.Printf("未知类型: %T\n", i)
}

func main() {
    inspect("hello")
    inspect(42)
    inspect(3.14)
    inspect([]int{1, 2, 3})
}
```

---

## 22.2 断言成功的情况

### 22.2.1 断言为具体类型

```go
package main

import "fmt"

type Shape interface {
    Area() float64
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

func main() {
    var s Shape = Circle{Radius: 5}

    fmt.Printf("接口动态类型: %T\n", s) // 接口动态类型: main.Circle

    if c, ok := s.(Circle); ok {
        fmt.Printf("成功断言为Circle，半径=%.2f，面积=%.2f\n", c.Radius, c.Area()) // 成功断言为Circle，半径=5.00，面积=78.54
    }

    if r, ok := s.(Rectangle); ok {
        fmt.Printf("Rectangle: %v\n", r)
    } else {
        fmt.Println("s不是Rectangle类型，它是Circle") // s不是Rectangle类型，它是Circle
    }
}
```

### 22.2.2 断言为接口类型

```go
package main

import "fmt"

type Reader interface {
    Read(p []byte) (n int, err error)
}

type Writer interface {
    Write(p []byte) (n int, err error)
}

type ReadWriter interface {
    Reader
    Writer
}

type File struct{}

func (f *File) Read(p []byte) (n int, err error) {
    fmt.Println("[File.Read] 读取") // [File.Read] 读取
    return len(p), nil
}

func (f *File) Write(p []byte) (n int, err error) {
    fmt.Println("[File.Write] 写入") // [File.Write] 写入
    return len(p), nil
}

func main() {
    var rw ReadWriter = &File{}

    if r, ok := rw.(Reader); ok {
        fmt.Printf("成功断言为Reader: %T\n", r) // 成功断言为Reader: *main.File
        r.Read(make([]byte, 10))
    }

    if w, ok := rw.(Writer); ok {
        fmt.Printf("成功断言为Writer: %T\n", w) // 成功断言为Writer: *main.File
        w.Write(make([]byte, 10))
    }
}
```

---

## 22.3 断言失败的情况

### 22.3.1 comma-ok断言安全处理

```go
package main

import "fmt"

type Any interface{}

func safeAssert(i Any) {
    fmt.Printf("尝试断言 %T: ", i)

    if s, ok := i.(string); ok {
        fmt.Printf("是字符串 %q\n", s)
        return
    }

    if n, ok := i.(int); ok {
        fmt.Printf("是整数 %d\n", n)
        return
    }

    fmt.Printf("不是字符串也不是整数\n")
}

func main() {
    fmt.Println("=== comma-ok断言安全处理 ===")

    safeAssert("hello")   // 尝试断言 string: 是字符串 "hello"
    safeAssert(42)        // 尝试断言 int: 是整数 42
    safeAssert(3.14)      // 尝试断言 float64: 不是字符串也不是整数
}
```

### 22.3.2 类型选择处理

```go
package main

import "fmt"

type Any interface{}

func inspectType(i Any) {
    fmt.Printf("%v (类型: %T) -> ", i, i)

    switch v := i.(type) {
    case nil:
        fmt.Println("nil值")
    case int:
        fmt.Printf("整数: %d (两倍=%d)\n", v, v*2)
    case string:
        fmt.Printf("字符串: %q (长度=%d)\n", v, len(v))
    case float64:
        fmt.Printf("浮点数: %.2f\n", v)
    case bool:
        fmt.Printf("布尔值: %t\n", v)
    default:
        fmt.Printf("其他类型: %T\n", v)
    }
}

func main() {
    values := []Any{nil, 42, 7, "hi", true, 3.14}

    fmt.Println("=== type switch ===\n")

    for _, v := range values {
        inspectType(v)
    }

    // <nil> (类型: <nil>) -> nil值
    // 42 (类型: int) -> 整数: 42 (两倍=84)
    // 7 (类型: int) -> 整数: 7 (两倍=14)
    // hi (类型: string) -> 字符串: "hi" (长度=2)
    // true (类型: bool) -> 布尔值: true
    // 3.14 (类型: float64) -> 浮点数: 3.14
}
```

---

## 22.4 断言与接口类型转换

### 22.4.1 接口转具体类型

```go
package main

import "fmt"

type Writer interface {
    Write(p []byte) (n int, err error)
}

type File struct {
    name string
}

func (f *File) Write(p []byte) (n int, err error) {
    fmt.Printf("[File.Write] %s: %s\n", f.name, string(p)) // [File.Write] data.txt: test
    return len(p), nil
}

type StringWriter struct{}

func (s *StringWriter) Write(p []byte) (n int, err error) {
    fmt.Printf("[StringWriter.Write] %s\n", string(p)) // [StringWriter.Write] test
    return len(p), nil
}

func main() {
    var w Writer = &File{name: "data.txt"}

    if f, ok := w.(*File); ok {
        fmt.Printf("断言为*File成功: %s\n", f.name) // 断言为*File成功: data.txt
        f.Write([]byte("test"))
    }

    var w2 Writer = &StringWriter{}
    if f, ok := w2.(*File); ok {
        fmt.Println("这行不会打印")
    } else {
        fmt.Println("w2不是*File类型，无法断言") // w2不是*File类型，无法断言
    }
}
```

---

## 本章小结

本章我们学习了Go的**类型断言**：

**两种断言语法：**
- **直接断言**：`value.(Type)`，失败会panic
- **comma-ok断言**：`value, ok := value.(Type)`，安全

**最佳实践：**
- 除非你100%确定断言会成功，否则使用comma-ok形式
- 当检查多种类型时，使用type switch更清晰

