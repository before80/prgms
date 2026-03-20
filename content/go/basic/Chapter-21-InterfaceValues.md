+++
title = "第21章 接口值"
weight = 210
date = "2026-03-20T08:39:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++
# 第21章 接口值

> 接口值是Go语言中最有趣的数据结构之一。把它想象成一个"万能遥控器"——可以指向不同品牌的电视（具体类型），但遥控器本身的操作方式是固定的。

## 21.1 接口值结构

### 21.1.1 接口值的组成

```go
package main

import (
    "fmt"
    "reflect"
)

type Writer interface {
    Write(p []byte) (n int, err error)
}

type File struct {
    name string
}

func (f *File) Write(p []byte) (n int, err error) {
    return len(p), nil
}

func main() {
    var w Writer = &File{name: "test.txt"}

    fmt.Printf("接口类型: %T\n", w) // 接口类型: *main.File
    fmt.Printf("接口值: %v\n", w)   // 接口值: &{test.txt}

    t := reflect.TypeOf(w)
    fmt.Printf("动态类型名称: %s\n", t.Name())   // 动态类型名称: File
    fmt.Printf("动态类型种类: %v\n", t.Kind())  // 动态类型种类: ptr
}
```

### 21.1.2 接口值的相等性

```go
package main

import "fmt"

type Equaler interface {
    Equal(other interface{}) bool
}

type Point struct {
    X, Y int
}

func (p Point) Equal(other interface{}) bool {
    o, ok := other.(Point)
    if !ok {
        return false
    }
    return p.X == o.X && p.Y == o.Y
}

func main() {
    p1 := Point{1, 2}
    p2 := Point{1, 2}
    p3 := Point{1, 3}

    var e Equaler = p1

    fmt.Printf("p1 == p2: %v\n", e.Equal(p2)) // p1 == p2: true
    fmt.Printf("p1 == p3: %v\n", e.Equal(p3)) // p1 == p3: false
}
```

---

## 21.2 动态类型与动态值

### 21.2.1 同一接口，不同类型

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

type Triangle struct {
    Base, Height float64
}

func (t Triangle) Area() float64 {
    return 0.5 * t.Base * t.Height
}

func printArea(s Shape) {
    fmt.Printf("%-12s 面积: %.2f\n", fmt.Sprintf("%T", s), s.Area())
}

func main() {
    shapes := []Shape{
        Circle{Radius: 5},
        Rectangle{Width: 4, Height: 6},
        Triangle{Base: 3, Height: 4},
    }

    fmt.Println("=== 不同类型的同一接口 ===")
    for _, shape := range shapes {
        printArea(shape)
    }

    // main.Circle     面积: 78.54
    // main.Rectangle  面积: 24.00
    // main.Triangle    面积: 6.00
}
```

### 21.2.2 类型信息保留

```go
package main

import (
    "fmt"
    "reflect"
)

type DataHolder interface {
    Get() any
}

type IntValue struct {
    value int
}

func (i *IntValue) Get() any {
    return i.value
}

type StringValue struct {
    value string
}

func (s *StringValue) Get() any {
    return s.value
}

func inspectHolder(h DataHolder) {
    fmt.Printf("动态类型: %T\n", h)    // *main.IntValue 或 *main.StringValue
    fmt.Printf("值: %v\n", h.Get())  // 42 或 "hello"
    fmt.Printf("实际类型: %T\n", h.Get()) // int 或 string
}

func main() {
    holders := []DataHolder{
        &IntValue{value: 42},
        &StringValue{value: "hello"},
    }

    fmt.Println("=== 接口保留类型信息 ===")
    for _, holder := range holders {
        inspectHolder(holder)
        fmt.Println()
    }

    // 动态类型: *main.IntValue
    // 值: 42
    // 实际类型: int
    //
    // 动态类型: *main.StringValue
    // 值: hello
    // 实际类型: string
}
```

---

## 21.3 接口值的nil

### 21.3.1 nil接口 vs nil值接口

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
    if f == nil {
        return 0, fmt.Errorf("file is nil")
    }
    fmt.Printf("写入文件 %s: %s\n", f.name, string(p)) // 写入文件 test.txt: test
    return len(p), nil
}

func main() {
    var f *File = nil
    var w Writer = f

    fmt.Printf("w == nil: %v\n", w == nil) // w == nil: false
    fmt.Printf("w的动态类型: %T\n", w)      // w的动态类型: *main.File
    fmt.Printf("w的值: %v\n", w)          // w的值: <nil>

    n, err := w.Write([]byte("test"))
    fmt.Printf("Write返回: n=%d, err=%v\n", n, err) // Write返回: n=0, err=file is nil
}
```

---

## 21.4 接口与nil比较

```go
package main

import "fmt"

type MyInterface interface {
    Method()
}

type MyStruct struct {
    data int
}

func (m *MyStruct) Method() {
    fmt.Println("Method called")
}

func main() {
    var i1 MyInterface
    fmt.Printf("i1: 动态类型=%T, 动态值=%v, i1==nil=%v\n", i1, i1, i1 == nil) // i1: 动态类型=<nil>, 动态值=<nil>, i1==nil=true

    var i2 MyInterface = (*MyStruct)(nil)
    fmt.Printf("i2: 动态类型=%T, 动态值=%v, i2==nil=%v\n", i2, i2, i2 == nil) // i2: 动态类型=*main.MyStruct, 动态值=<nil>, i2==nil=false

    i3 := &MyStruct{data: 42}
    var i4 MyInterface = i3
    fmt.Printf("i4: 动态类型=%T, 动态值=%v, i4==nil=%v\n", i4, i4, i4 == nil) // i4: 动态类型=*main.MyStruct, 动态值=&{42}, i4==nil=false
}
```

---

## 21.5 接口性能

### 21.5.1 接口调用开销

```go
package main

import (
    "fmt"
    "time"
)

type Adder interface {
    Add(a, b int) int
}

type SimpleAdder struct{}

func benchmarkInterface() int {
    var a Adder = &SimpleAdder{}
    result := 0
    for i := 0; i < 1_000_000; i++ {
        result = a.Add(1, 2)
    }
    return result
}

func main() {
    fmt.Println("=== 接口调用性能测试 ===")

    start := time.Now()
    benchmarkInterface()
    interfaceTime := time.Since(start)
    fmt.Printf("接口调用100万次耗时: %v\n", interfaceTime) // 接口调用100万次耗时: ~150ms
}
```

---

## 本章小结

本章我们学习了接口值的内部机制：

**接口值结构：**
- 由tab指针和数据指针组成

**动态特性：**
- 同一接口变量可以存储不同具体类型的值
- 运行时通过接口表动态分派方法调用

**nil陷阱：**
- 真正的nil接口：动态类型为nil，动态值为nil
- nil值接口：动态类型非nil，动态值为nil

