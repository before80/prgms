+++
title = "第4章 常量"
weight = 40
date = "2026-03-20T08:39:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false

+++
# 第4章 常量

> 欢迎来到第四章！这一章我们要聊的是 Go 语言的"不变"哲学——常量。常量就像是编程世界里的"刻在石头上"，一旦定义就不能改变。常量在 Go 中有很多独特的特性，比如可以在编译时计算确定的值，还有那个神秘的 `iota` 枚举器。准备好了吗？让我们开始！

## 4.1 常量声明

> 常量是 Go 程序中"不可改变"的值。一旦定义，常量的值就不能再被修改。这就像是你写在合同里的条款，一旦签字就不能改了。常量在 Go 中主要用于定义那些在程序运行期间不会改变的值，比如数学常数、配置值等。

#### 4.1.1 单常量声明

使用 `const` 关键字可以声明一个常量。


```go
package main

import "fmt"

const Pi float64 = 3.14159

func main() {
    fmt.Printf("Pi = %.5f\n", Pi) // Pi = 3.14159
}

```

#### 4.1.2 多常量声明

可以一次声明多个常量。


```go
package main

import "fmt"

const (
    StatusOK  = 200
    StatusNotFound = 404
    StatusServerError = 500
)

func main() {
    fmt.Printf("StatusOK = %d\n", StatusOK) // StatusOK = 200
    fmt.Printf("StatusNotFound = %d\n", StatusNotFound) // StatusNotFound = 404
    fmt.Printf("StatusServerError = %d\n", StatusServerError) // StatusServerError = 500
}
```

#### 4.1.3 常量组

常量可以分组声明，这在定义一组相关的常量时很有用。


```go
package main

import "fmt"

const (
    // 星期
    Sunday = 0
    Monday = 1
    Tuesday = 2
    Wednesday = 3
    Thursday = 4
    Friday = 5
    Saturday = 6
)

const (
    // 月份
    January = 1
    February = 2
    March = 3
    April = 4
    May = 5
    June = 6
)

func main() {
    fmt.Printf("Friday = %d\n", Friday) // Friday = 5
    fmt.Printf("July = %d\n", July) // July = 7
}
```

#### 4.1.4 声明位置

常量可以在函数外部（包级）声明，也可以在函数内部声明。


```go
package main

import "fmt"

const GlobalConst = "我是全局的"

func main() {
    const LocalConst = "我是局部的"
    fmt.Println(GlobalConst) // 我是全局的
    fmt.Println(LocalConst) // 我是局部的
}
```

## 4.2 常量分类

> Go 的常量分为有类型常量和无类型常量。无类型常量在运算时会获得更大的精度。

#### 4.2.1 有类型常量

显式指定类型的常量。


```go
package main

import "fmt"

const a int = 42
const b float64 = 3.14

func main() {
    fmt.Printf("a = %d (类型: %T)\n", a, a) // a = 42 (类型: int)
    fmt.Printf("b = %.2f (类型: %T)\n", b, b) // b = 3.14 (类型: float64)
}
```

#### 4.2.2 无类型常量

没有显式指定类型的常量，编译器会根据上下文推导类型。


```go
package main

import "fmt"

const (
    x = 42         // 无类型整数常量
    y = 3.14       // 无类型浮点常量
    z = "hello"    // 无类型字符串常量
)

func main() {
    fmt.Printf("x = %d (类型: %T)\n", x, x) // x = 42 (类型: int)
    fmt.Printf("y = %.2f (类型: %T)\n", y, y) // y = 3.14 (类型: float64)
    fmt.Printf("z = %s (类型: %T)\n", z, z) // z = hello (类型: string)
}
```

#### 4.2.3 默认类型

无类型常量在用于变量赋值时会获得默认类型：


```go
package main

import "fmt"

const x = 42  // 无类型常量

func main() {
    var i int = x    // x 在这里获得 int 类型
    var f float64 = x // x 在这里获得 float64 类型

    fmt.Printf("i = %d (类型: %T)\n", i, i) // i = 42 (类型: int)
    fmt.Printf("f = %.2f (类型: %T)\n", f, f) // f = 42.00 (类型: float64)
}
```

## 4.3 常量特性

> 常量有一些独特的特性，让它和变量有所不同。

#### 4.3.1 编译期确定

常量的值在编译时就确定了，这带来了性能和安全性。


```go
package main

import "fmt"

const PI = 3.14159  // 编译时确定

func main() {
    // 常量在编译时就确定了值
    fmt.Printf("PI = %.5f\n", PI) // PI = 3.14159
}
```

#### 4.3.2 不可寻址

常量不能取地址。


```go
package main

import "fmt"

const X = 42

func main() {
    // fmt.Println(&X)  // ❌ 编译错误：cannot take the address of X
    fmt.Println("常量不能取地址") // 常量不能取地址
}
```

#### 4.3.3 不可修改

常量一旦定义就不能修改。


```go
package main

import "fmt"

const Y = 42

func main() {
    // Y = 100  // ❌ 编译错误：cannot assign to Y
    fmt.Println("常量不能修改") // 常量不能修改
}
```

## 4.4 常量表达式

> 常量表达式是在编译时计算的表达式。

#### 4.4.1 允许的操作

常量表达式可以使用各种算术运算符。


```go
package main

import "fmt"

const (
    a = 10 + 20    // 加法
    b = 30 - 5     // 减法
    c = 4 * 5      // 乘法
    d = 100 / 10   // 除法
    e = 17 % 5     // 取模
)

func main() {
    fmt.Printf("a = %d\n", a) // a = 30
    fmt.Printf("b = %d\n", b) // b = 25
    fmt.Printf("c = %d\n", c) // c = 20
    fmt.Printf("d = %d\n", d) // d = 10
    fmt.Printf("e = %d\n", e) // e = 2
}
```



#### 4.4.2 内置函数使用

Go 语言中真正能用于常量初始化表达式的内置函数非常有限，主要包括 `len()` 和 `cap()`。它们在用于常量大小的数组类型时，可以在编译时求值。


```go
package main

import "fmt"

// 定义一个常量大小的数组类型
type FixedArray [1024]byte

// 使用内置 len() 函数获取数组长度（编译时求值）
const ArrayLen = len(FixedArray{})

func main() {
    fmt.Printf("FixedArray 的长度: %d\n", ArrayLen) // FixedArray 的长度: 1024
}

```

**为什么 `math.Sqrt()` 不能用于常量？**

> `math.Sqrt()` 是一个普通函数调用，需要运行时才能计算。Go 的 const 初始化表达式必须是**编译时常量**，不能包含任何函数调用。
>
> 同理，`math.Pi` 也不是内置常量，它来自 `math` 包。如果需要 π 的近似值，可以直接写一个字面量：
>
> ```go
> const pi = 3.14159265358979323846
> ```


#### 4.4.3 数组长度约束

数组长度必须是常量。


```go
package main

import "fmt"

const N = 10

func main() {
    // 数组长度必须是常量
    arr := [N]int{1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
    fmt.Printf("数组长度: %d\n", len(arr)) // 数组长度: 10
}
```

## 4.5 iota 枚举器

> `iota` 是 Go 语言的一个神秘武器，它是一个从 0 开始递增的常量生成器。`iota` 这个名字来自希腊字母 iota，在编程中通常表示"微小增量"的意思。iota 是 Go 语言特有的概念，非常适合定义枚举类型。

#### 4.5.1 iota 语义

`iota` 在每个 `const` 块开始时重置为 0，每行递增 1。


```go
package main

import "fmt"

const (
    Sunday = iota    // 0
    Monday           // 1
    Tuesday          // 2
    Wednesday        // 3
    Thursday         // 4
    Friday           // 5
    Saturday         // 6
)

func main() {
    fmt.Printf("Sunday = %d\n", Sunday) // Sunday = 0
    fmt.Printf("Monday = %d\n", Monday) // Monday = 1
    fmt.Printf("Friday = %d\n", Friday) // Friday = 5
}
```

#### 4.5.2 iota 重置

每个 `const` 块都会重置 iota。


```go
package main

import "fmt"

const (
    // 第一个 iota 块，从 0 开始
    Sunday = iota  // 0
    Monday         // 1
)

const (
    // 新的 iota 块，重新从 0 开始
    Red = iota    // 0
    Green         // 1
    Blue          // 2
)

func main() {
    fmt.Printf("Sunday = %d\n", Sunday) // Sunday = 0
    fmt.Printf("Red = %d\n", Red) // Red = 0
    fmt.Printf("Blue = %d\n", Blue) // Blue = 2
}
```

#### 4.5.3 跳过值

可以使用空白标识符跳过某些值。


```go
package main

import "fmt"

const (
    A = iota  // 0
    B         // 1
    _         // 2（跳过）
    C         // 3
    D         // 4
)

func main() {
    fmt.Printf("A = %d\n", A) // A = 0
    fmt.Printf("B = %d\n", B) // B = 1
    fmt.Printf("C = %d\n", C) // C = 3
    fmt.Printf("D = %d\n", D) // D = 4
}
```

#### 4.5.4 位掩码模式

iota 非常适合定义位掩码常量。


```go
package main

import "fmt"

const (
    Read  = 1 << iota  // 1 << 0 = 1
    Write             // 1 << 1 = 2
    Execute           // 1 << 2 = 4
)

func main() {
    fmt.Printf("Read = %d\n", Read) // Read = 1
    fmt.Printf("Write = %d\n", Write) // Write = 2
    fmt.Printf("Execute = %d\n", Execute) // Execute = 4

    // 组合权限
    all := Read | Write | Execute
    fmt.Printf("所有权限 = %d\n", all) // 所有权限 = 7
}
```

#### 4.5.5 算术模式

iota 可以用于各种算术表达式。


```go
package main

import "fmt"

const (
    KB = 1 << (10 * iota)  // 1 << 0 = 1
    MB                     // 1 << 10 = 1024
    GB                     // 1 << 20 = 1048576
    TB                     // 1 << 30 = 1073741824
)

func main() {
    fmt.Printf("KB = %d\n", KB) // KB = 1
    fmt.Printf("MB = %d\n", MB) // MB = 1024
    fmt.Printf("GB = %d\n", GB) // GB = 1048576
    fmt.Printf("TB = %d\n", TB) // TB = 1073741824
}
```

## 4.6 常量与变量运算

> 常量和变量可以一起运算，但结果会是什么类型呢？

#### 4.6.1 自动转换

无类型常量可以自动转换为任何兼容的类型。


```go
package main

import "fmt"

const X = 10

func main() {
    var y = 20
    result := X + y
    fmt.Printf("X + y = %d (类型: %T)\n", result, result) // X + y = 30 (类型: int)
}
```

#### 4.6.2 精度保持

无类型常量在运算时保持高精度。


```go
package main

import "fmt"

const a = 1.0        // 无类型浮点常量
const b = 2.0        // 无类型浮点常量

func main() {
    // 常量运算保持高精度
    result := a / b
    fmt.Printf("a / b = %.10f (类型: %T)\n", result, result) // a / b = 0.5000000000 (类型: float64)
}
```

#### 4.6.3 溢出检查

常量溢出在编译时会被检测。


```go
package main

import "fmt"

const Big = 1000000000000000000

func main() {
    // 常量溢出在编译时检测
    // const TooBig int8 = Big  // ❌ 编译错误：constant 1000000000000000000 overflows int8
    fmt.Println("大数字:", Big) // 大数字: 1000000000000000000
}

```


## 本章小结

本章我们学习了 Go 语言的常量，这是 Go 语言中一个简洁但强大的特性。主要内容包括：

1. **常量声明**：使用 `const` 关键字声明常量，可以是单常量、多常量或常量组。

2. **常量分类**：有类型常量和无类型常量，无类型常量在运算时获得更大精度。

3. **常量特性**：编译期确定、不可寻址、不可修改。

4. **常量表达式**：可以在编译时计算各种表达式。

5. **iota 枚举器**：Go 语言的独特特性，用于生成递增的枚举值。

6. **常量与变量运算**：无类型常量可以与变量自由运算。

常量是 Go 语言中一个简单但强大的特性。掌握好 `iota` 的用法，可以让你写出非常优雅的枚举定义代码。

---

> 到这里，第四章"常量"就全部结束了！你现在应该对 Go 语言的常量有了全面的了解。常量是 Go 语言中一个简洁但强大的特性，特别是 `iota` 这个枚举器，能让你写出非常优雅的代码。
>
> 现在，四章的内容全部完成了！从词法元素到类型系统，从常量到构建约束，你应该对 Go 语言的核心概念有了扎实的理解。恭喜你完成了 Go 语言基础教程的第一部分！

