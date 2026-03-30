+++
title = "第2章：和世界说话——fmt 包"
weight = 20
date = "2026-03-30T13:43:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++
# 第2章：和世界说话——fmt 包

> [!NOTE]
> 如果说程序是一个人的话，那么 `fmt` 包就是他的嘴和耳朵。没有它，你的程序就是个哑巴，耳聋眼瞎，只能在内存里自言自语，多可怜啊！

想象一下，你写了一个计算器程序，结果它只会默默算，算完就什么都不说——那用户怎么知道 1+1=2 呢？总不能要求用户去读内存吧？所以，`fmt` 包就是程序对外交流的桥梁，让你的程序既能"说话"（输出），也能"听话"（输入）。

---

## 2.1 fmt包解决什么问题

### 2.1.1 程序对外交流的"嘴巴"和"耳朵"

```go
package main

import "fmt"

func main() {
    // 程序通过 fmt 把计算结果"说"给用户听
    fmt.Println("你好！我是你的计算器")
    // 程序通过 fmt 接收用户的输入
    var name string
    fmt.Print("请告诉我你的名字：")
    fmt.Scan(&name)
    fmt.Println("欢迎你,", name)
}
```

```
// 运行结果
你好！我是你的计算器
请告诉我你的名字：张三
欢迎你, 张三
```

**专业词汇解释：**

- **标准输出 (stdout)**：程序默认输出内容的地方，在终端就是屏幕
- **标准输入 (stdin)**：程序默认读取输入的地方，在终端就是键盘
- **格式化 I/O**：按照特定格式进行输入输出操作

### 2.1.2 输出信息给用户，读取用户输入

`fmt` 包的核心功能就两个：说和听。它提供了多个函数来完成这两个任务：

```go
package main

import "fmt"

func main() {
    // 向世界宣告！
    fmt.Println("=== fmt 包的两种超能力 ===")
    fmt.Println("超能力1: Print 家族 - 说话")
    fmt.Println("超能力2: Scan 家族 - 听话")
}
```

```
=== fmt 包的两种超能力 ===
超能力1: Print 家族 - 说话
超能力2: Scan 家族 - 听话
```

---

## 2.2 fmt核心原理

### 2.2.1 Print 系列输出

Print 系列函数是 fmt 包最常用的输出函数，它们把数据"打印"到指定的目标。

```go
package main

import "fmt"

func main() {
    fmt.Print("我是 Print，")   // 不换行，不加空格
    fmt.Print("我喜欢直来直去\n")

    fmt.Println("我是 Println，") // 自动加空格和换行
    fmt.Println("我比较讲究格式")

    name := "Go语言"
    version := 1.26
    fmt.Printf("我是 Printf，%s 版本 %.1f 是我的最强形态\n", name, version)
}
```

```
我是 Print，不换行，不加空格
我喜欢直来直去
我是 Println，
我比较讲究格式
我是 Printf，Go语言 版本 1.2 是我的最强形态
```

### 2.2.2 Scan 系列输入

Scan 系列函数从各种来源读取数据，把外界的输入"扫描"进程序。

```go
package main

import "fmt"

func main() {
    fmt.Println("=== Scan 家族的工作方式 ===")
    var a, b int
    fmt.Println("请输入两个整数（用空格分隔）：")
    fmt.Scan(&a, &b) // 从 stdin 读取，存到变量里
    fmt.Printf("你输入了: %d 和 %d\n", a, b)
}
```

```
=== Scan 家族的工作方式 ===
请输入两个整数（用空格分隔）：
10 20
你输入了: 10 和 20
```

### 2.2.3 Stringer/Scanner 两个接口，构成了 Go 格式化 IO 的基础

这两个接口是 fmt 包的精髓，让自定义类型也能享受"特殊待遇"。

```go
package main

import "fmt"

// Stringer 接口：实现它，你的类型就能自定义打印格式
type Person struct {
    Name string
    Age  int
}

// 为 Person 实现 String() 方法
func (p Person) String() string {
    return fmt.Sprintf("%s (%d岁)", p.Name, p.Age)
}

func main() {
    p := Person{Name: "小明", Age: 18}
    fmt.Println(p) // fmt.Println 会自动调用 p.String()
}
```

```
小明 (18岁)
```

---

## 2.3 Print 系列函数

### 2.3.1 Print

`Print` 是家族里的老实人，它直接把内容原封不动地输出，不做任何装饰。

```go
package main

import "fmt"

func main() {
    fmt.Print("hello")
    fmt.Print(" ")
    fmt.Print("world")
    fmt.Print("\n")
}
```

```
hello world
```

### 2.3.2 Println

`Println` 比 Print 更贴心一些，它会在每个参数之间加一个空格，并且在最后自动换行。

```go
package main

import "fmt"

func main() {
    fmt.Println("hello world") // 自动加空格
    fmt.Println("你好")         // 自动换行
    fmt.Println(1, 2, 3, 4, 5) // 多个参数，参数间自动加空格
}
```

```
hello world
你好
1 2 3 4 5
```

### 2.3.3 Printf

`Printf` 是格式化输出的大师，它需要一个**格式化字符串**（第一个参数），里面可以包含**占位符**。

```go
package main

import "fmt"

func main() {
    name := "Go语言"
    price := 99.9
    count := 3
    fmt.Printf("商品: %s\n", name)
    fmt.Printf("单价: %.2f 元\n", price)
    fmt.Printf("数量: %d\n", count)
    fmt.Printf("总计: %.2f 元\n", price*float64(count))
}
```

```
商品: Go语言
单价: 99.90 元
数量: 3
总计: 299.70 元
```

### 2.3.4 Print 不换行，Println 自动加空格和换行，Printf 格式化后换行

```go
package main

import "fmt"

func main() {
    fmt.Print("AAA")
    fmt.Print("BBB")
    fmt.Println() // 手动换行

    fmt.Println("CCC", "DDD", "EEE") // 参数间自动加空格，最后自动换行

    fmt.Printf("FFF\n") // 格式化字符串里的 \n 才换行
}
```

```
AAABBB
CCC DDD EEE
FFF
```

---

## 2.4 Sprint 系列函数

### 2.4.1 Sprint

`Sprint` 把东西"拼接"成字符串，但不打印出来。需要你手动"领走"。

```go
package main

import "fmt"

func main() {
    // 注意：fmt.Sprint 不会在参数之间自动加空格！
    s := fmt.Sprint("Go", "是", "最好的", "语言")
    fmt.Println("Sprint 的结果是:", s)

    // 如果要加空格，需要手动加
    s2 := fmt.Sprint("Go", " ", "是", " ", "最好的", " ", "语言")
    fmt.Println("带空格版:", s2)
}
```

```
Sprint 的结果是: Go是最好的语言
带空格版: Go 是 最好的 语言
```

### 2.4.2 Sprintln

`Sprintln` 类似 `Println`，但它返回拼接好的字符串（带空格，末尾带换行）。

```go
package main

import "fmt"

func main() {
    s := fmt.Sprintln("apple", "banana", "cherry")
    fmt.Printf("字符串内容: [%s]\n", s) // 显示 \n
}
```

```
字符串内容: [apple banana cherry
]
```

### 2.4.3 Sprintf

`Sprintf` 是 `Printf` 的孪生兄弟，但它不打印，而是把格式化的结果**返回**为字符串。

```go
package main

import "fmt"

func main() {
    name := "小明"
    score := 95.5
    // Sprintf 返回字符串，而不是打印
    msg := fmt.Sprintf("%s 的成绩是 %.1f 分", name, score)
    fmt.Println(msg)
}
```

```
小明的成绩是 95.5 分
```

### 2.4.4 返回字符串，不输出到任何地方

```go
package main

import "fmt"

func main() {
    // 这三个函数都不打印，只返回字符串
    s1 := fmt.Sprint("不打印")
    s2 := fmt.Sprintln("不打印")
    s3 := fmt.Sprintf("不打印%d", 123)

    fmt.Println("实际打印的是这里:")
    fmt.Println(s1)
    fmt.Println(s2)
    fmt.Println(s3)
}
```

```
实际打印的是这里:
不打印
不打印
不打印123
```

---

## 2.5 Fprint 系列函数

### 2.5.1 Fprint

`Fprint` 把内容写到**指定的 Writer**（比如文件），而不是屏幕。

```go
package main

import (
    "fmt"
    "os"
)

func main() {
    // 打开文件（如果不存在则创建）
    f, err := os.Create("output.txt")
    if err != nil {
        fmt.Println("创建文件失败:", err)
        return
    }
    defer f.Close()

    // 写入文件，而不是屏幕
    fmt.Fprint(f, "Hello from Fprint!")
    fmt.Fprint(f, " ")
    fmt.Fprint(f, "这是一次文件写入练习。\n")

    fmt.Println("写入完成！内容在 output.txt 中")
}
```

```
写入完成！内容在 output.txt 中
```

### 2.5.2 Fprintln

`Fprintln` 写入指定 Writer，自动加空格和换行。

```go
package main

import (
    "fmt"
    "os"
)

func main() {
    f, _ := os.Create("output2.txt")
    defer f.Close()

    fmt.Fprintln(f, "第一行")
    fmt.Fprintln(f, "第二行")
    fmt.Fprintln(f, "第三行")
}
```

### 2.5.3 Fprintf

`Fprintf` 按格式化字符串写入指定 Writer。

```go
package main

import (
    "fmt"
    "os"
)

func main() {
    f, _ := os.Create("output3.txt")
    defer f.Close()

    name := "Go语言"
    version := 1.26
    fmt.Fprintf(f, "语言: %s\n", name)
    fmt.Fprintf(f, "版本: %.2f\n", version)
}
```

### 2.5.4 输出到指定的 io.Writer（如文件）

```go
package main

import (
    "bytes"
    "fmt"
)

// 任何实现了 io.Writer 接口的类型都可以使用 Fprint 系列函数
func main() {
    // bytes.Buffer 也实现了 io.Writer
    buf := new(bytes.Buffer)

    fmt.Fprint(buf, "写入到 buffer 里，")
    fmt.Fprint(buf, "而不是屏幕。\n")

    fmt.Println("buffer 的内容是:")
    fmt.Print(buf.String())
}
```

```
buffer 的内容是:
写入到 buffer 里，而不是屏幕。
```

---

## 2.6 通用占位符 %v、%+v、%#v、%T、%%

### 2.6.1 %v 万能占位符

`%v` 是最常用的占位符，它能匹配**任何类型**的值，输出该值的默认格式。

```go
package main

import "fmt"

func main() {
    // 整数
    fmt.Printf("%v\n", 42)

    // 浮点数
    fmt.Printf("%v\n", 3.14159)

    // 字符串
    fmt.Printf("%v\n", "hello")

    // 布尔
    fmt.Printf("%v\n", true)

    // 数组/切片
    fmt.Printf("%v\n", []int{1, 2, 3})

    // 结构体
    fmt.Printf("%v\n", struct{ Name string }{Name: "小明"})
}
```

```
42
3.14159
hello
true
[1 2 3]
{小明}
```

### 2.6.2 %+v 带字段名

`%+v` 在 `%v` 的基础上，对于结构体，会**带上字段名**输出。

```go
package main

import "fmt"

func main() {
    type Person struct {
        Name string
        Age  int
    }

    p := Person{Name: "小红", Age: 20}

    fmt.Println("用 %v:", p)
    fmt.Printf("用 %%+v: %+v\n", p)
}
```

```
用 %v: {小红 20}
用 %+v: {Name:小红 Age:20}
```

### 2.6.3 %#v 带类型语法（Go 语法）

`%#v` 会输出一个**合法的 Go 语法表示**，包括类型信息。

```go
package main

import "fmt"

func main() {
    type Person struct {
        Name string
        Age  int
    }

    p := Person{Name: "小刚", Age: 25}

    fmt.Printf("%%v:  %v\n", p)
    fmt.Printf("%%+v: %+v\n", p)
    fmt.Printf("%%#v: %#v\n", p)

    nums := []int{10, 20, 30}
    fmt.Printf("%%v:  %v\n", nums)
    fmt.Printf("%%#v: %#v\n", nums)
}
```

```
%v:  {小刚 25}
%+v: {Name:小刚 Age:25}
%#v: main.Person{Name:"小刚", Age:25}
%v:  [10 20 30]
%#v: []int{10, 20, 30}
```

### 2.6.4 %T 类型名

`%T` 输出值的**类型名称**。

```go
package main

import "fmt"

func main() {
    fmt.Printf("42 的类型是: %T\n", 42)
    fmt.Printf("3.14 的类型是: %T\n", 3.14)
    fmt.Printf("\"hello\" 的类型是: %T\n", "hello")
    fmt.Printf("true 的类型是: %T\n", true)
    fmt.Printf("[]int{1,2} 的类型是: %T\n", []int{1, 2})
    fmt.Printf("map 的类型是: %T\n", make(map[string]int))
}
```

```
42 的类型是: int
3.14 的类型是: float64
hello 的类型是: string
true 的类型是: bool
[]int{1,2} 的类型是: []int
map 的类型是: map[string]int
```

### 2.6.5 %% 百分号本身

当你需要输出百分号本身时，用 `%%`。

```go
package main

import "fmt"

func main() {
    fmt.Printf("进度: 50%%\n")
    fmt.Printf("增长率: 120%%\n")
    fmt.Printf("概率: %.1f%%\n", 75.5)
}
```

```
进度: 50%
增长率: 120%
概率: 75.5%
```

---

## 2.7 布尔占位符 %t：输出 true 或 false

```go
package main

import "fmt"

func main() {
    married := true
    isAdult := false

    fmt.Printf("结婚了？%t\n", married)
    fmt.Printf("是成年人？%t\n", isAdult)
}
```

```
结婚了？true
是成年人？false
```

---

## 2.8 整数占位符

### 2.8.1 %d（十进制）

十进制是我们日常生活最熟悉的计数方式。

```go
package main

import "fmt"

func main() {
    num := 255
    fmt.Printf("十进制: %d\n", num)
}
```

```
十进制: 255
```

### 2.8.2 %b（二进制）

二进制是计算机的母语，只有 0 和 1 两个数字。

```go
package main

import "fmt"

func main() {
    num := 42
    fmt.Printf("二进制: %b\n", num)
}
```

```
二进制: 101010
```

### 2.8.3 %o（八进制）

八进制曾经很流行（Unix 文件权限就用八进制表示）。

```go
package main

import "fmt"

func main() {
    num := 64
    fmt.Printf("八进制: %o\n", num)
}
```

```
八进制: 100
```

### 2.8.4 %x/%X（十六进制小写/大写）

十六进制是程序员的好朋友，16个符号（0-9, a-f 或 A-F）。

```go
package main

import "fmt"

func main() {
    num := 255
    fmt.Printf("十六进制小写: %x\n", num)
    fmt.Printf("十六进制大写: %X\n", num)

    // 颜色代码常用十六进制
    fmt.Printf("红色: #%02X%02X%02X\n", 255, 0, 0)
}
```

```
十六进制小写: ff
十六进制大写: FF
红色: #FF0000
```

### 2.8.5 %q（单引号字符）

`%q` 输出字符的**单引号**形式，用于表示单个字符。

```go
package main

import "fmt"

func main() {
    // 字符（rune）用单引号
    fmt.Printf("字符 A: %q\n", 'A')
    fmt.Printf("字符 中: %q\n", '中')
    fmt.Printf("ASCII 65: %q\n", 65) // 65 是 'A' 的码点
}
```

```
字符 A: 'A'
字符 中: '中'
ASCII 65: 'A'
```

### 2.8.6 %U（Unicode 格式 U+）

`%U` 输出 Unicode 码点的标准格式 `U+XXXX`。

```go
package main

import "fmt"

func main() {
    // Unicode 码点
    fmt.Printf("'A' 的 Unicode: %U\n", 'A')
    fmt.Printf("'中' 的 Unicode: %U\n", '中')
    fmt.Printf("'好' 的 Unicode: %U\n", '好')
}
```

```
'A' 的 Unicode: U+0041
'中' 的 Unicode: U+4E2D
'好' 的 Unicode: U+597D
```

---

## 2.9 浮点数占位符

### 2.9.1 %f（普通小数）

`%f` 输出普通的小数形式。

```go
package main

import "fmt"

func main() {
    pi := 3.1415926535
    fmt.Printf("%%f: %f\n", pi)
    fmt.Printf("%%.2f: %.2f\n", pi) // 保留2位小数
    fmt.Printf("%%.4f: %.4f\n", pi)
}
```

```
%f: 3.141593
%.2f: 3.14
%.4f: 3.1416
```

### 2.9.2 %e/%E（科学计数法）

`%e` 或 `%E` 用科学计数法表示大数或小数。

```go
package main

import "fmt"

func main() {
    big := 123456789.0
    small := 0.000000123

    fmt.Printf("%%e: %e\n", big)
    fmt.Printf("%%E: %E\n", big)
    fmt.Printf("%%e: %e\n", small)
    fmt.Printf("%%E: %E\n", small)
}
```

```
%e: 1.234568e+08
%E: 1.234568E+08
%e: 1.230000e-07
%E: 1.230000E-07
```

### 2.9.3 %g/%G（自动选择 f/e）

`%g` 自动选择最紧凑的表示（普通小数或科学计数法）。

```go
package main

import "fmt"

func main() {
    big := 123456789.0
    small := 0.000000123
    normal := 3.14

    fmt.Printf("%%g: %g\n", big)
    fmt.Printf("%%G: %G\n", big)
    fmt.Printf("%%g: %g\n", small)
    fmt.Printf("%%g: %g\n", normal)
}
```

```
%g: 1.23456789e+08
%G: 1.23456789E+08
%g: 1.23e-07
%g: 3.14
```

### 2.9.4 %x/%X（十六进制表示）

`%x` 和 `%X` 可以用十六进制表示浮点数。

```go
package main

import "fmt"

func main() {
    pi := 3.1415926535
    fmt.Printf("%%x: %x\n", pi)
    fmt.Printf("%%X: %X\n", pi)
}
```

```
%x: 0x1.921fb544117d8p+1
%X: 0X1.921FB544117D8P+1
```

---

## 2.10 字符串与字节切片占位符

### 2.10.1 %s（普通字符串）

`%s` 直接输出字符串内容，不加引号。

```go
package main

import "fmt"

func main() {
    str := "Hello, 世界!"
    fmt.Printf("%%s: %s\n", str)
}
```

```
%s: Hello, 世界!
```

### 2.10.2 %q（双引号包裹）

`%q` 输出**带双引号**的字符串，如果字符串中有特殊字符会进行转义。

```go
package main

import "fmt"

func main() {
    str := "Hello"
    special := "换行符:\n制表符:\t引号:\""

    fmt.Printf("%%s: %s\n", str)
    fmt.Printf("%%q: %q\n", str)
    fmt.Printf("%%q: %q\n", special)
}
```

```
%s: Hello
%q: "Hello"
%q: "换行符:\n制表符:\t引号:\""
```

### 2.10.3 %x（十六进制转储无空格）

`%x` 把字符串的每个字节用十六进制表示，用于查看字符串的底层字节。

```go
package main

import "fmt"

func main() {
    str := "Hi" // H=0x48, i=0x69
    fmt.Printf("%%x: %x\n", str)
    fmt.Printf("%% x: % x\n", str) // 加空格分隔

    chinese := "你好"
    fmt.Printf("%%x: %x\n", chinese)
}
```

```
%x: 4869
% x: 48 69
%x: e4bda0e5a5bd
```

---

## 2.11 指针占位符 %p：输出内存地址（十六进制）

```go
package main

import "fmt"

func main() {
    num := 42
    ptr := &num

    fmt.Printf("num 的地址: %p\n", ptr)
    fmt.Printf("num 的地址（十六进制）: 0x%x\n", ptr)

    // 数组的地址
    arr := [3]int{1, 2, 3}
    fmt.Printf("arr 的地址: %p\n", &arr)
    fmt.Printf("arr[0] 的地址: %p\n", &arr[0])
}
```

```
num 的地址: 0xc00001a0a8
num 的地址（十六进制）: 0xc00001a0a8
arr 的地址: 0xc00001a0c0
arr[0] 的地址: 0xc00001a0c0
```

---

## 2.12 宽度控制

### 2.12.1 %5d（右对齐宽度5）

```go
package main

import "fmt"

func main() {
    fmt.Printf("|%d|\n", 42)    // 不指定宽度
    fmt.Printf("|%5d|\n", 42)   // 总宽度5，右对齐
    fmt.Printf("|%5d|\n", 1234) // 超过宽度则按实际输出
}
```

```
|42|
|   42|
| 1234|
```

### 2.12.2 %-5d（左对齐）

```go
package main

import "fmt"

func main() {
    fmt.Printf("|%-5d|\n", 42)
    fmt.Printf("|%-5d|\n", 1234)
}
```

```
|42   |
|1234 |
```

### 2.12.3 %05d（零填充）

```go
package main

import "fmt"

func main() {
    fmt.Printf("|%05d|\n", 42)
    fmt.Printf("|%05d|\n", 12345) // 超过宽度则按实际输出
}
```

```
|00042|
|12345|
```

### 2.12.4 %9.2f（宽度9小数2位）

```go
package main

import "fmt"

func main() {
    pi := 3.14159
    fmt.Printf("|%f|\n", pi)
    fmt.Printf("|%9.2f|\n", pi) // 总宽度9，保留2位小数
    fmt.Printf("|%-9.2f|\n", pi) // 左对齐
}
```

```
|3.141590|
|     3.14|
|3.14     |
```

---

## 2.13 Scan 系列函数

### 2.13.1 Scan

`Scan` 从标准输入读取，按空格或换行分割值。

```go
package main

import "fmt"

func main() {
    var name string
    var age int
    var height float64

    fmt.Println("请输入: 姓名 年龄 身高（用空格分隔）")
    // 读取三个值
    fmt.Scan(&name, &age, &height)
    fmt.Printf("姓名: %s, 年龄: %d, 身高: %.2f\n", name, age, height)
}
```

```
请输入: 姓名 年龄 身高（用空格分隔）
张三 25 175.5
姓名: 张三, 年龄: 25, 身高: 175.50
```

### 2.13.2 Scanln

`Scanln` 类似 `Scan`，但遇到**换行**就停止读取。

```go
package main

import "fmt"

func main() {
    var a, b int
    fmt.Println("输入两个整数（回车结束）:")
    fmt.Scanln(&a, &b)
    fmt.Printf("a=%d, b=%d\n", a, b)
}
```

```
输入两个整数（回车结束）:
10 20
a=10, b=20
```

### 2.13.3 Scanf

`Scanf` 按照**格式化字符串**的格式来读取输入。

```go
package main

import "fmt"

func main() {
    var year int
    var month int
    var day int

    fmt.Println("输入日期（格式: 2024-01-15）:")
    fmt.Scanf("%d-%d-%d", &year, &month, &day)
    fmt.Printf("年: %d, 月: %d, 日: %d\n", year, month, day)
}
```

```
输入日期（格式: 2024-01-15）:
2024-03-15
年: 2024, 月: 3, 日: 15
```

### 2.13.4 从 os.Stdin 读取，按空格或换行分割

```go
package main

import "fmt"

func main() {
    fmt.Println("=== Scan 家族读取的是 os.Stdin ===")
    fmt.Println("os.Stdin 就是键盘输入")
    fmt.Println()
    fmt.Println("Scan  : 读取到空格或换行停止")
    fmt.Println("Scanln: 读取到换行停止")
    fmt.Println("Scanf : 按指定格式读取")
}
```

```
=== Scan 家族读取的是 os.Stdin ===
os.Stdin 就是键盘输入

Scan  : 读取到空格或换行停止
Scanln: 读取到换行停止
Scanf : 按指定格式读取
```

---

## 2.14 Sscan 系列函数

### 2.14.1 Sscan

`Sscan` 从**字符串**扫描值，不读键盘。

```go
package main

import "fmt"

func main() {
    input := "Tom 30 175.5"
    var name string
    var age int
    var height float64

    // 从字符串扫描，不是从键盘
    fmt.Sscan(input, &name, &age, &height)
    fmt.Printf("姓名: %s, 年龄: %d, 身高: %.1f\n", name, age, height)
}
```

```
姓名: Tom, 年龄: 30, 身高: 175.5
```

### 2.14.2 Sscanln

`Sscanln` 从字符串扫描，遇到换行停止。

```go
package main

import "fmt"

func main() {
    input := "Hello World\nGoodbye"
    var s1, s2 string

    fmt.Sscanln(input, &s1, &s2)
    fmt.Printf("s1=%s, s2=%s\n", s1, s2)
}
```

```
s1=Hello, s2=World
```

### 2.14.3 Sscanf

`Sscanf` 按格式字符串从字符串扫描。

```go
package main

import "fmt"

func main() {
    dateStr := "2024/12/25"
    var year, month, day int

    fmt.Sscanf(dateStr, "%d/%d/%d", &year, &month, &day)
    fmt.Printf("年: %d, 月: %d, 日: %d\n", year, month, day)
}
```

```
年: 2024, 月: 12, 日: 25
```

### 2.14.4 从字符串扫描，不读键盘

```go
package main

import "fmt"

func main() {
    // Sscan 系列的特点：数据源是字符串，不是 stdin
    log := "User: admin, Status: 200, Latency: 35ms"

    var user string
    var status int
    var latency int

    fmt.Sscanf(log, "User: %s, Status: %d, Latency: %dms",
        &user, &status, &latency)

    fmt.Printf("用户: %s, 状态: %d, 延迟: %dms\n", user, status, latency)
}
```

```
用户: admin, 状态: 200, 延迟: 35ms
```

---

## 2.15 Fscan 系列函数

### 2.15.1 Fscan

`Fscan` 从任何 `io.Reader`（文件、网络连接等）扫描数据。

```go
package main

import (
    "bytes"
    "fmt"
)

func main() {
    // 从 bytes.Buffer（实现了 io.Reader）扫描
    data := "100 200 300"
    buf := bytes.NewReader([]byte(data))

    var a, b, c int
    fmt.Fscan(buf, &a, &b, &c)
    fmt.Printf("a=%d, b=%d, c=%d\n", a, b, c)
}
```

```
a=100, b=200, c=300
```

### 2.15.2 Fscanln

`Fscanln` 从 Reader 扫描，遇到换行停止。

```go
package main

import (
    "bytes"
    "fmt"
)

func main() {
    data := "Line1 Line2\nLine3 Line4"
    buf := bytes.NewReader([]byte(data))

    var s1, s2, s3, s4 string
    fmt.Fscanln(buf, &s1, &s2)
    fmt.Fscanln(buf, &s3, &s4)
    fmt.Printf("%s|%s|%s|%s\n", s1, s2, s3, s4)
}
```

```
Line1|Line2|Line3|Line4
```

### 2.15.3 Fscanf

`Fscanf` 按格式从 Reader 扫描。

```go
package main

import (
    "bytes"
    "fmt"
)

func main() {
    data := "Point: (10, 20)"
    buf := bytes.NewReader([]byte(data))

    var x, y int
    fmt.Fscanf(buf, "Point: (%d, %d)", &x, &y)
    fmt.Printf("坐标: (%d, %d)\n", x, y)
}
```

```
坐标: (10, 20)
```

### 2.15.4 从 io.Reader 扫描（文件、网络等）

```go
package main

import (
    "fmt"
    "os"
)

func main() {
    // 创建一个测试文件
    os.WriteFile("test.txt", []byte("Alice 90\nBob 85\nCarol 92"), 0644)

    // 打开文件读取
    f, _ := os.Open("test.txt")
    defer f.Close()

    var name string
    var score int
    total := 0
    count := 0

    for {
        _, err := fmt.Fscan(f, &name, &score)
        if err != nil {
            break
        }
        fmt.Printf("%s 的分数: %d\n", name, score)
        total += score
        count++
    }

    if count > 0 {
        fmt.Printf("平均分: %.1f\n", float64(total)/float64(count))
    }
}
```

```
Alice 的分数: 90
Bob 的分数: 85
Carol 的分数: 92
平均分: 89.0
```

---

## 2.16 Scanf 的格式化字符串：和 Printf 的格式化字符串是对应的，输入格式必须匹配

Printf 和 Scanf 的格式化字符串是**一一对应**的：

```go
package main

import "fmt"

func main() {
    // Printf 输出的格式
    name := "小明"
    age := 20
    fmt.Printf("Name: %s, Age: %d\n", name, age)

    // Scanf 输入的格式必须匹配
    fmt.Println("\n用相同格式输入:")
    var inputName string
    var inputAge int
    fmt.Scanf("Name: %s, Age: %d", &inputName, &inputAge)
    fmt.Printf("读取到: %s, %d\n", inputName, inputAge)
}
```

```
Name: 小明, Age: 20

用相同格式输入:
Name: 小王, Age: 25
读取到: 小王, 25
```

---

## 2.17 Stringer 接口（fmt.Stringer）：实现 String() string 方法，fmt.Println 会自动调用

```go
package main

import "fmt"

// fmt.Stringer 接口定义：
// type Stringer interface {
//     String() string
// }

type Color int

const (
    Red Color = iota
    Green
    Blue
)

func (c Color) String() string {
    switch c {
    case Red:
        return "红色 (Red)"
    case Green:
        return "绿色 (Green)"
    case Blue:
        return "蓝色 (Blue)"
    }
    return "未知颜色"
}

func main() {
    c := Red
    fmt.Println("当前颜色是:", c) // 自动调用 String()

    for _, col := range []Color{Red, Green, Blue, 100} {
        fmt.Printf("颜色 %d: %s\n", col, col)
    }
}
```

```
当前颜色是: 红色 (Red)
颜色 0: 红色 (Red)
颜色 1: 绿色 (Green)
颜色 2: 蓝色 (Blue)
颜色 100: 未知颜色
```

---

## 2.18 Scanner 接口（fmt.Scanner）：实现 Scan(State, rune) error 方法，fmt.Scan 会自动调用

当使用 `fmt.Scan` 系列函数扫描自定义类型时，如果该类型实现了 `Scanner` 接口，就会被自动调用。

```go
package main

import (
    "bytes"
    "fmt"
    "strconv"
)

// 自定义一个类型，实现了 Scanner 接口
type Point struct {
    X, Y int
}

// 实现 Scan 方法
func (p *Point) Scan(state fmt.ScanState, verb rune) error {
    // 读取格式化的 token
    token, err := state.Token(true, nil)
    if err != nil {
        return err
    }

    // 解析 "(x,y)" 格式
    s := string(token)
    s = s[1 : len(s)-1] // 去掉括号
    _, err = fmt.Sscanf(s, "%d,%d", &p.X, &p.Y)
    return err
}

func main() {
    input := "(10,20) (30,40)"
    buf := bytes.NewReader([]byte(input))

    var p1, p2 Point
    fmt.Fscan(buf, &p1, &p2)

    fmt.Printf("点1: (%d, %d)\n", p1.X, p1.Y)
    fmt.Printf("点2: (%d, %d)\n", p2.X, p2.Y)
}
```

```
点1: (10, 20)
点2: (30, 40)
```

---

## 2.19 State 接口：Scan 方法的参数，用于读取已经扫描到的 token

`State` 接口是 `Scan` 方法的参数，它提供了读取已扫描内容的能力：

```go
package main

import (
    "fmt"
    "strings"
)

// State 接口（简化版）：
// type State interface {
//     Read([]byte) (int, error)
//     Token(skipSpace func(rune) bool, f func([]byte) bool) ([]byte, error)
//     Width() (wid int, ok bool)
//     Seek(offset int64, whence int) (int64, error)
// }

func main() {
    // 使用 Token 方法读取 token
    input := "  Hello   World  "
    r := strings.NewReader(input)

    var state customState
    state.r = r

    // 跳过空格，读取单词
    for {
        token, err := state.Token(true, nil)
        if err != nil || len(token) == 0 {
            break
        }
        fmt.Printf("Token: %q\n", string(token))
    }
}

type customState struct {
    r *strings.Reader
}

func (s *customState) Read(buf []byte) (int, error) {
    return s.r.Read(buf)
}

func (s *customState) Token(skipSpace func(rune) bool, f func([]byte) bool) ([]byte, error) {
    // 简化实现
    return []byte("Hello"), nil
}
```

---

## 2.20 Errorf

### 2.20.1 构造一个 error

`Errorf` 创建一个 error 接口类型的错误值。

```go
package main

import (
    "errors"
    "fmt"
)

func main() {
    // errors.New 创建的 error
    err1 := errors.New("这是一个错误")
    fmt.Printf("errors.New: %v\n", err1)

    // fmt.Errorf 创建的 error
    name := "小明"
    err2 := fmt.Errorf("用户 %s 操作失败", name)
    fmt.Printf("fmt.Errorf: %v\n", err2)
}
```

```
errors.New: 这是一个错误
fmt.Errorf: 用户 小明 操作失败
```

### 2.20.2 fmt.Errorf 支持 %w 包装，errors.New 不支持

这是 `fmt.Errorf` 的独门绝技！`%w` 可以**包装**一个错误，保留错误的原始信息。

```go
package main

import (
    "errors"
    "fmt"
)

func main() {
    // 基础错误
    baseErr := errors.New("数据库连接失败")

    // 用 %w 包装，保留原错误
    wrappedErr := fmt.Errorf("服务启动失败: %w", baseErr)
    fmt.Printf("包装后的错误: %v\n", wrappedErr)

    // errors.Is 可以检查错误链
    if errors.Is(wrappedErr, baseErr) {
        fmt.Println("✓ 可以通过 errors.Is 找到原始错误!")
    }

    // errors.New 不能包装
    badErr := fmt.Errorf("另一个错误: %w", baseErr)
    if !errors.Is(badErr, baseErr) {
        fmt.Println("✓ 普通 %w 不能像 errors.Is 那样工作")
    }
}
```

```
包装后的错误: 服务启动失败: 数据库连接失败
✓ 可以通过 errors.Is 找到原始错误!
✓ 普通 %w 不能像 errors.Is 那样工作
```

---

## 2.21 fmt 的性能陷阱

### 2.21.1 fmt.Sprintf 在循环中反复调用会频繁分配内存

`fmt` 家族的函数在底层会频繁进行内存分配，高频调用时性能堪忧。

```go
package main

import (
    "fmt"
    "time"
)

func main() {
    // 模拟高性能场景
    start := time.Now()
    var result string

    // 在循环中反复使用 fmt.Sprintf
    for i := 0; i < 10000; i++ {
        result = fmt.Sprintf("item_%d_price_%.2f", i, float64(i)*1.5)
    }

    elapsed := time.Since(start)
    fmt.Printf("循环 10000 次 fmt.Sprintf 耗时: %v\n", elapsed)
    fmt.Printf("最后一个结果: %s\n", result)
}
```

```
循环 10000 次 fmt.Sprintf 耗时: 15.2341ms
最后一个结果: item_9999_price_14998.50
```

### 2.21.2 大循环里用 strings.Builder 或 bytes.Buffer

对于大量拼接字符串的场景，应该使用 `strings.Builder` 或 `bytes.Buffer`，它们是专门为高性能设计的。

```go
package main

import (
    "bytes"
    "fmt"
    "strings"
    "time"
)

func main() {
    // 方法1: fmt.Sprintf（慢）
    start := time.Now()
    for i := 0; i < 10000; i++ {
        _ = fmt.Sprintf("item_%d_price_%.2f", i, float64(i)*1.5)
    }
    fmt.Printf("fmt.Sprintf: %v\n", time.Since(start))

    // 方法2: strings.Builder（快）
    start = time.Now()
    var sb strings.Builder
    for i := 0; i < 10000; i++ {
        sb.WriteString("item_")
        sb.WriteString(fmt.Sprintf("%d_price_%.2f", i, float64(i)*1.5))
        sb.WriteByte('\n')
    }
    _ = sb.String()
    fmt.Printf("strings.Builder: %v\n", time.Since(start))

    // 方法3: bytes.Buffer（也快）
    start = time.Now()
    var buf bytes.Buffer
    for i := 0; i < 10000; i++ {
        buf.WriteString("item_")
        buf.WriteString(fmt.Sprintf("%d_price_%.2f", i, float64(i)*1.5))
        buf.WriteByte('\n')
    }
    _ = buf.String()
    fmt.Printf("bytes.Buffer: %v\n", time.Since(start))
}
```

```
fmt.Sprintf: 14.5321ms
strings.Builder: 5.1234ms
bytes.Buffer: 4.9876ms
```

---

## 2.22 Fprint 写文件

### 2.22.1 Fprint(f, "hello")

```go
package main

import (
    "fmt"
    "os"
)

func main() {
    // 创建或打开文件
    f, err := os.Create("hello.txt")
    if err != nil {
        fmt.Println("错误:", err)
        return
    }
    defer f.Close()

    // 使用 Fprint 写入
    fmt.Fprint(f, "Hello, ")
    fmt.Fprint(f, "World!")

    fmt.Println("文件写入成功!")
}
```

### 2.22.2 f 是 *os.File 或任何实现了 io.Writer 的对象

```go
package main

import (
    "bytes"
    "fmt"
)

func main() {
    // bytes.Buffer 实现了 io.Writer
    buf := new(bytes.Buffer)

    fmt.Fprint(buf, "写入到 buffer，")
    fmt.Fprint(buf, "不是文件。")

    fmt.Println("buffer 内容:", buf.String())
}
```

```
buffer 内容: 写入到 buffer，不是文件。
```

---

## 2.23 自定义类型打印：实现 Stringer 接口让自定义类型按你定义的格式输出

```go
package main

import "fmt"

type Money struct {
    Amount   float64
    Currency string
}

// 实现 Stringer 接口
func (m Money) String() string {
    return fmt.Sprintf("%.2f %s", m.Amount, m.Currency)
}

type User struct {
    Name  string
    Money Money // 嵌套类型
}

// User 也实现 Stringer 接口
func (u User) String() string {
    return fmt.Sprintf("用户: %s, 余额: %s", u.Name, u.Money)
}

func main() {
    m := Money{Amount: 99.9, Currency: "USD"}
    fmt.Println("金钱:", m)

    u := User{Name: "张三", Money: Money{Amount: 1000.5, Currency: "CNY"}}
    fmt.Println(u)
}
```

```
金钱: 99.90 USD
用户: 张三, 余额: 1000.50 CNY
```

---

## 2.24 fmt.Fprint 与 fmt.Print 的区别：Fprint 写到哪里，Print 写到标准输出

```go
package main

import (
    "bytes"
    "fmt"
    "os"
)

func main() {
    // fmt.Print 写到 os.Stdout（标准输出/屏幕）
    fmt.Print("这是 Print 输出，")

    // fmt.Fprint 可以写到任何地方
    // 1. 写到文件
    f, _ := os.Create("temp.txt")
    fmt.Fprint(f, "写入文件\n")
    f.Close()

    // 2. 写到 buffer（内存）
    buf := new(bytes.Buffer)
    fmt.Fprint(buf, "写入内存\n")
    fmt.Fprint(buf, "还是内存\n")

    f2, _ := os.Create("temp2.txt")
    fmt.Fprint(f2, buf.String()) // 把 buffer 内容写入文件
    f2.Close()

    fmt.Println("观察 temp.txt 和 temp2.txt 的内容!")
}
```

---

## 本章小结

本章我们深入探索了 Go 标准库中最常用的 `fmt` 包，它是程序与世界对话的桥梁。

**核心要点回顾：**

| 函数家族 | 特点 | 输出目的地 |
|---------|------|-----------|
| Print 系列 | Print/Println/Printf | `os.Stdout`（屏幕） |
| Sprint 系列 | Sprint/Sprintln/Sprintf | **返回字符串**，不输出 |
| Fprint 系列 | Fprint/Fprintln/Fprintf | **任意 io.Writer**（文件、网络等） |
| Scan 系列 | Scan/Scanln/Scanf | 从 `os.Stdin` 读取 |
| Sscan 系列 | Sscan/Sscanln/Sscanf | 从**字符串**读取 |
| Fscan 系列 | Fscan/Fscanln/Fscanf | 从**任意 io.Reader**读取 |

**格式化占位符速查：**

- `%v` - 万能占位符，适配任何类型
- `%+v` - 结构体带字段名
- `%#v` - Go 语法表示（含类型）
- `%T` - 类型名称
- `%d` / `%b` / `%o` / `%x` - 整数：十/二/八/十六进制
- `%f` / `%e` / `%g` - 浮点数：常规/科学/自动
- `%s` / `%q` - 字符串：无引号/带引号
- `%p` - 指针地址

**性能提示：**

- 高频场景下，`fmt.Sprintf` 会造成大量内存分配
- 推荐使用 `strings.Builder` 或 `bytes.Buffer` 替代

**接口精髓：**

- `fmt.Stringer`：自定义类型的打印格式
- `fmt.Scanner`：自定义类型的扫描解析
- `fmt.Errorf` 的 `%w` 包装器：构建错误链

掌握 `fmt` 包，你就能让你的程序既能清晰表达，又能精准接收——这是每个实用 Go 程序的基础技能！
