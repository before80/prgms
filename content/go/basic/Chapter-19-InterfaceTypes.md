+++
title = "第19章 接口类型"
weight = 190
date = "2026-03-20T08:39:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++
# 第19章 接口类型

> 接口（Interface），Go语言的"魔法契约"！如果说类型是"房产证"，那接口就是"职业资格证"——你不需要关心这个人姓甚名谁，只需要知道他能做什么。

## 19.1 接口的定义

### 19.1.1 接口声明语法

```go
package main

import "fmt"

type Writer interface {
    Write(p []byte) (n int, err error)
}

type Reader interface {
    Read(p []byte) (n int, err error)
}

func main() {
    var w Writer
    fmt.Printf("Writer接口初始值: %v\n", w) // <nil>

    var r Reader
    fmt.Printf("Reader接口初始值: %v, 动态类型: %T\n", r, r) // Reader接口初始值: <nil>, 动态类型: <nil>
}
```

### 19.1.2 接口命名惯例

| 惯例 | 示例 | 含义 |
|------|------|------|
| `-er`结尾 | `Reader`, `Writer` | 表示"能做什么" |

---

## 19.2 空接口

### 19.2.1 interface{} 是什么

```go
package main

import "fmt"

func main() {
    var i interface{}

    i = 42
    fmt.Printf("存整数: %d, 类型: %T\n", i, i) // 存整数: 42, 类型: int

    i = "hello world"
    fmt.Printf("存字符串: %s, 类型: %T\n", i, i) // 存字符串: hello world, 类型: string

    i = []int{1, 2, 3}
    fmt.Printf("存切片: %v, 类型: %T\n", i, i) // 存切片: [1 2 3], 类型: []int

    i = map[string]int{"Java": 98}
    fmt.Printf("存Map: %v, 类型: %T\n", i, i) // 存Map: map[Java:98], 类型: map[string]int
}
```

### 19.2.2 any 是 interface{} 的别名

```go
package main

import "fmt"

func main() {
    var data any = []int{1, 2, 3}
    fmt.Printf("data: %v, 类型: %T\n", data, data) // data: [1 2 3], 类型: []int
}
```

### 19.2.3 泛型容器

```go
package main

import "fmt"

type Container struct {
    value any
}

func NewContainer(v any) *Container {
    return &Container{value: v}
}

func (c *Container) Get() any {
    return c.value
}

func main() {
    containers := []*Container{
        NewContainer(100),
        NewContainer("Hello!"),
        NewContainer([]int{1, 2, 3}),
    }

    for i, c := range containers {
        fmt.Printf("容器%d: 值=%v, 类型=%T\n", i, c.Get(), c.Get())
    }

    // 容器0: 值=100, 类型=int
    // 容器1: 值=Hello!, 类型=string
    // 容器2: 值=[1 2 3], 类型=[]int
}
```

---

## 19.3 接口组合

### 19.3.1 接口嵌入

```go
package main

import "fmt"

type Reader interface {
    Read(p []byte) (n int, err error)
}

type Writer interface {
    Write(p []byte) (n int, err error)
}

type Closer interface {
    Close() error
}

type ReadWriter interface {
    Reader
    Writer
}

type ReadWriteCloser interface {
    ReadWriter
    Closer
}

type File struct {
    name string
}

func (f *File) Read(p []byte) (n int, err error) {
    fmt.Printf("[File] 读取文件 %s\n", f.name) // [File] 读取文件 data.txt
    return len(p), nil
}

func (f *File) Write(p []byte) (n int, err error) {
    fmt.Printf("[File] 写入文件 %s: %s\n", f.name, string(p)) // [File] 写入文件 data.txt: Hello
    return len(p), nil
}

func (f *File) Close() error {
    fmt.Printf("[File] 关闭文件 %s\n", f.name) // [File] 关闭文件 data.txt
    return nil
}

func main() {
    var rw ReadWriter = &File{name: "data.txt"}
    rw.Read(make([]byte, 10))
    rw.Write([]byte("Hello"))

    fmt.Println()

    var rwc ReadWriteCloser = &File{name: "log.txt"}
    rwc.Read(make([]byte, 10))
    rwc.Write([]byte("Log entry"))
    rwc.Close()
}
```

### 19.3.2 组合接口的方法集

```go
package main

import "fmt"

type A interface {
    MethodA()
}

type B interface {
    MethodB()
}

type C interface {
    A
    B
}

type MyStruct struct{}

func (s *MyStruct) MethodA() {
    fmt.Println("MethodA 被调用") // MethodA 被调用
}

func (s *MyStruct) MethodB() {
    fmt.Println("MethodB 被调用") // MethodB 被调用
}

func main() {
    var c C = &MyStruct{}
    c.MethodA()
    c.MethodB()
}
```

---

## 19.4 接口设计原则

### 19.4.1 接口隔离原则

```go
package main

import "fmt"

type Engine interface {
    Start()
    Stop()
}

type SpeedController interface {
    Accelerate()
    Brake()
}

type Car struct {
    speed int
}

func (c *Car) Start() {
    fmt.Println("发动机启动") // 发动机启动
}

func (c *Car) Stop() {
    fmt.Println("发动机停止") // 发动机停止
}

func (c *Car) Accelerate() {
    c.speed += 10
    fmt.Printf("加速到 %d km/h\n", c.speed) // 加速到 10 km/h
}

func (c *Car) Brake() {
    c.speed -= 10
    fmt.Printf("减速到 %d km/h\n", c.speed) // 减速到 0 km/h
}

func main() {
    car := &Car{}

    var engine Engine = car
    var speedCtrl SpeedController = car

    engine.Start()
    speedCtrl.Accelerate()
    speedCtrl.Brake()
    engine.Stop()
}
```

### 19.4.2 小接口优于大接口

```go
package main

import (
    "bytes"
    "fmt"
    "io"
)

type MemoryBuffer struct {
    data []byte
}

func (b *MemoryBuffer) Read(p []byte) (n int, err error) {
    copy(p, b.data)
    return len(b.data), nil
}

func (b *MemoryBuffer) Write(p []byte) (n int, err error) {
    b.data = append(b.data, p...)
    return len(p), nil
}

func main() {
    buffer := &MemoryBuffer{data: []byte("Hello, ")}

    var rw io.ReadWriter = buffer
    rw.Write([]byte("World!"))

    buf := make([]byte, 100)
    n, _ := rw.Read(buf)
    fmt.Printf("读取内容: %s\n", string(buf[:n])) // 读取内容: Hello, World!
}
```

### 19.4.3 接口定义位置

```go
package main

import "fmt"

type Persistence interface {
    Save(data []byte) error
    Load() ([]byte, error)
}

type Service struct {
    storage Persistence
}

func NewService(p Persistence) *Service {
    return &Service{storage: p}
}

func (s *Service) ProcessAndSave(data []byte) error {
    processed := append(data, []byte("_processed")...)
    return s.storage.Save(processed)
}

type FileStorage struct {
    filename string
}

func (f *FileStorage) Save(data []byte) error {
    fmt.Printf("[FileStorage] 保存到文件 %s: %s\n", f.filename, string(data)) // [FileStorage] 保存到文件 data.bin: 原始数据_processed
    return nil
}

func (f *FileStorage) Load() ([]byte, error) {
    fmt.Printf("[FileStorage] 从文件 %s 加载\n", f.filename) // [FileStorage] 从文件 data.bin 加载
    return []byte("loaded data"), nil
}

func main() {
    storage := &FileStorage{filename: "data.bin"}
    service := NewService(storage)

    err := service.ProcessAndSave([]byte("原始数据"))
    if err != nil {
        fmt.Println("错误:", err)
    }
}
```

---

## 19.5 标准库常用接口

### 19.5.1 io 包接口

#### io.Reader

```go
package main

import (
    "bytes"
    "fmt"
    "io"
)

func main() {
    data := "Hello, Go I/O!"
    buffer := bytes.NewBufferString(data)

    var reader io.Reader = buffer
    p := make([]byte, 1024)

    n, err := reader.Read(p)
    fmt.Printf("读取了 %d 字节: %q\n", n, string(p[:n])) // 读取了 16 字节: "Hello, Go I/O!"

    n, err = reader.Read(p)
    fmt.Printf("再次读取: n=%d, err=%v\n", n, err) // 再次读取: n=0, err=<nil>
}
```

#### io.Writer

```go
package main

import (
    "bytes"
    "fmt"
    "io"
)

func main() {
    buffer := new(bytes.Buffer)
    var writer io.Writer = buffer

    n, err := writer.Write([]byte("Hello, "))
    fmt.Printf("写入 %d 字节, err: %v\n", n, err) // 写入 6 字节, err: <nil>

    n, err = writer.Write([]byte("World!"))
    fmt.Printf("写入 %d 字节, err: %v\n", n, err) // 写入 6 字节, err: <nil>

    fmt.Printf("缓冲区内容: %s\n", buffer.String()) // 缓冲区内容: Hello, World!
}
```

#### io.Closer

```go
package main

import (
    "bytes"
    "fmt"
    "io"
)

func main() {
    buffer := new(bytes.Buffer)
    var closer io.Closer = buffer

    err := closer.Close()
    fmt.Printf("Close err: %v\n", err) // Close err: <nil>
}
```

#### io.Seeker

```go
package main

import (
    "bytes"
    "fmt"
    "io"
)

func main() {
    data := []byte("0123456789")
    buffer := bytes.NewBuffer(data)

    var seeker io.Seeker = buffer

    p := make([]byte, 5)
    n, _ := buffer.Read(p)
    fmt.Printf("读取: %q, 剩余: %d 字节\n", string(p), buffer.Len()) // 读取: "01234", 剩余: 5 字节

    offset, err := seeker.Seek(-2, io.SeekCurrent)
    fmt.Printf("Seek -2: 位置=%d, err=%v\n", offset, err) // Seek -2: 位置=3, err=<nil>

    n, _ = buffer.Read(p[:3])
    fmt.Printf("再读取: %q\n", string(p[:3])) // 再读取: "345"
}
```

### 19.5.2 fmt 包接口

#### fmt.Stringer

```go
package main

import "fmt"

type Color string

const (
    Red   Color = "红色"
    Green Color = "绿色"
    Blue  Color = "蓝色"
)

func (c Color) String() string {
    return string(c)
}

func main() {
    colors := []Color{Red, Green, Blue}

    fmt.Println("=== fmt.Stringer 演示 ===")
    for _, c := range colors {
        fmt.Printf("颜色: %s\n", c)
    }

    fmt.Printf("\n%v 格式: %v\n", Red, Red) // 红色
    fmt.Printf("%s 格式: %s\n", Red, Red)   // 红色
}
```

#### fmt.GoStringer

```go
package main

import "fmt"

type Point struct {
    X, Y int
}

func (p Point) String() string {
    return fmt.Sprintf("Point(%d,%d)", p.X, p.Y)
}

func (p Point) GoString() string {
    return fmt.Sprintf("main.Point{X:%d, Y:%d}", p.X, p.Y)
}

func main() {
    p := Point{X: 10, Y: 20}

    fmt.Printf("%v  格式: %v\n", p, p)    // Point(10,20)
    fmt.Printf("%#v 格式: %#v\n", p, p)   // main.Point{X:10, Y:20}
}
```

### 19.5.3 sort 包接口

```go
package main

import (
    "fmt"
    "sort"
)

type Person struct {
    Name string
    Age  int
}

type PersonSlice []Person

func (p PersonSlice) Len() int           { return len(p) }
func (p PersonSlice) Less(i, j int) bool { return p[i].Age < p[j].Age }
func (p PersonSlice) Swap(i, j int)     { p[i], p[j] = p[j], p[i] }

func main() {
    people := PersonSlice{
        {"Alice", 30},
        {"Bob", 25},
        {"Charlie", 35},
    }

    fmt.Println("=== 排序前（按年龄）===")
    for _, p := range people {
        fmt.Printf("  %s: %d岁\n", p.Name, p.Age)
    }

    sort.Sort(people)

    fmt.Println("\n=== 排序后 ===")
    for _, p := range people {
        fmt.Printf("  %s: %d岁\n", p.Name, p.Age)
    }

    // === 排序前（按年龄）===
    //   Alice: 30岁
    //   Bob: 25岁
    //   Charlie: 35岁
    //
    // === 排序后 ===
    //   Bob: 25岁
    //   Alice: 30岁
    //   Charlie: 35岁
}
```

---

## 19.6 接口实现机制

### 19.6.1 接口的内部结构

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

    fmt.Printf("接口类型: %T\n", w)  // 接口类型: *main.File
    fmt.Printf("接口值: %v\n", w)   // 接口值: &{test.txt}

    t := reflect.TypeOf(w)
    if t != nil {
        fmt.Printf("动态类型: %s\n", t.Name())     // 动态类型: File
        fmt.Printf("动态类型种类: %v\n", t.Kind()) // 动态类型种类: ptr
    }
}
```

### 19.6.2 接口缓存

```go
package main

import (
    "fmt"
    "io"
    "time"
)

type Counter struct {
    count int
}

func (c *Counter) Write(p []byte) (n int, err error) {
    c.count++
    return len(p), nil
}

func main() {
    var w io.Writer = &Counter{}

    start := time.Now()
    for i := 0; i < 1_000_000; i++ {
        w.Write([]byte("test"))
    }
    elapsed := time.Since(start)

    fmt.Printf("接口调用100万次耗时: %v\n", elapsed) // 接口调用100万次耗时: ~200ms
    fmt.Printf("计数器值: %d\n", w.(*Counter).count) // 计数器值: 1000000
}
```

---

## 19.7 空接口详解

### 19.7.1 反射与空接口

```go
package main

import (
    "fmt"
    "reflect"
)

func inspectInterface(i interface{}) {
    val := reflect.ValueOf(i)
    typ := reflect.TypeOf(i)

    fmt.Printf("类型: %v\n", typ)        // 类型: int / string / main.Person
    fmt.Printf("种类(Kind): %v\n", val.Kind())
}

type Person struct {
    Name string
    Age  int
}

func main() {
    fmt.Println("=== 整数 ===")
    inspectInterface(42)

    fmt.Println("\n=== 字符串 ===")
    inspectInterface("hello")

    fmt.Println("\n=== 结构体 ===")
    person := Person{Name: "小明", Age: 18}
    inspectInterface(person)
}
```

### 19.7.2 any 类型演进

```go
package main

import "fmt"

type Stack[T any] struct {
    data []T
}

func (s *Stack[T]) Push(v T) {
    s.data = append(s.data, v)
}

func (s *Stack[T]) Pop() T {
    if len(s.data) == 0 {
        var zero T
        return zero
    }
    v := s.data[len(s.data)-1]
    s.data = s.data[:len(s.data)-1]
    return v
}

func main() {
    fmt.Println("=== 泛型Stack演示 ===")

    intStack := &Stack[int]{}
    intStack.Push(1)
    intStack.Push(2)
    intStack.Push(3)

    fmt.Printf("弹出: %d\n", intStack.Pop()) // 弹出: 3
    fmt.Printf("弹出: %d\n", intStack.Pop()) // 弹出: 2
    fmt.Printf("弹出: %d\n", intStack.Pop()) // 弹出: 1
}
```

---

## 本章小结

本章我们学习了Go接口：

**接口基础：**
- 接口定义了一组方法签名
- Go使用隐式实现

**空接口（any）：**
- 任何类型都满足空接口
- Go 1.18+推荐使用any

**接口组合：**
- 通过嵌入来组合新接口

**设计原则：**
- 小接口优于大接口
- 由使用方定义接口

**标准库重要接口：**
- `io.Reader/Writer/Closer`
- `fmt.Stringer`
- `sort.Interface`

