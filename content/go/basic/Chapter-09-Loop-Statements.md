+++
title = "第9章 循环语句"
weight = 90
date = "2026-03-20T08:39:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false

+++
# 第9章 循环语句

> 欢迎来到第九章！这一章我们要聊的是 Go 语言的"循环语句"。循环是什么？循环就是让程序"重复做一件事"的结构。想象一下，你每天早上起床、刷牙，洗脸、上班……这就是一个循环。程序中的循环也是如此——让计算机反复执行一段代码，直到满足某个条件才停下来。Go 语言只有一种循环关键字：`for`，但它的用法可以变化出花来！

## 9.1 for 语句

### 9.1.1 传统形式

Go 的 `for` 循环有三种形式，最基本的就是传统三段式：`for 初始化; 条件; 后置 { }`

```go

package main

import "fmt"

func main() {
    // 传统形式：初始化; 条件; 后置
    for i := 0; i < 5; i++ {
        fmt.Printf("第 %d 次循环\n", i+1) // 第 1 次循环 // 第 1 次循环
    }
}

```

#### 9.1.1.1 初始化子句

初始化子句在循环开始前执行，只执行一次。

```go

package main

import "fmt"

func main() {
    // 初始化 i := 0 只执行一次
    for i := 0; i < 3; i++ {
        fmt.Printf("i = %d\n", i) // i = 0 // i = 0, i = 1, i = 2
    }
}

```

#### 9.1.1.2 条件子句

条件子句在每次循环开始前判断，如果为 `true` 就继续执行。

```go

package main

import "fmt"

func main() {
    sum := 0
    i := 1

    for i <= 10 {
        sum += i
        i++
    }
    fmt.Printf("1+2+...+10 = %d\n", sum) // 1+2+...+10 = 55
}

```

#### 9.1.1.3 后置子句

后置子句在每次循环体执行完后执行。

```go

package main

import "fmt"

func main() {
    for i := 1; i <= 3; i++ {
        fmt.Printf("后置执行后 i = %d\n", i) // 后置执行后 i = 2 // i = 2, i = 3, i = 4
    }
}

```

### 9.1.2 条件形式

只有条件子句，没有初始化和后置时，语法和 `while` 类似。

```go

package main

import "fmt"

func main() {
    n := 1
    for n < 100 {
        n *= 2
    }
    fmt.Printf("n = %d\n", n) // n = 128
}

```

### 9.1.3 无限形式

如果三个子句都省略，就是无限循环。

```go

package main

import "fmt"

func main() {
    i := 0
    for {
        i++
        if i > 5 {
            break
        }
        fmt.Printf("无限循环 i = %d\n", i) // 无限循环 i = 1 // i = 1, 2, 3, 4, 5
    }
    fmt.Printf("循环结束，i = %d\n", i) // 循环结束，i = 6
}

```

### 9.1.4 range 形式

`range` 是 Go 特有的遍历语法，用于遍历数组、切片、字符串、映射和通道。

```go

package main

import "fmt"

func main() {
    nums := []int{10, 20, 30}

    for i, v := range nums {
        fmt.Printf("索引 %d: 值 %d\n", i, v) // 索引 0: 值 10
        // 索引 0: 值 10
        // 索引 1: 值 20
        // 索引 2: 值 30
    }
}

```

#### 9.1.4.1 range 子句

`range` 子句返回两个值：索引和元素值。

```go

package main

import "fmt"

func main() {
    names := []string{"Alice", "Bob", "Charlie"}

    for i, name := range names {
        fmt.Printf("%d: %s\n", i, name) // 0: Alice
        // 0: Alice
        // 1: Bob
        // 2: Charlie
    }
}

```

#### 9.1.4.2 迭代变量

`range` 返回的变量是副本，不是原元素。

```go

package main

import "fmt"

func main() {
    nums := []int{1, 2, 3}
    for _, v := range nums {
        v = v * 2
    }
    fmt.Printf("原切片: %v\n", nums) // 原切片: [1 2 3]
}

```

#### 9.1.4.3 迭代变量副本

关于迭代变量的副本特性：

```go

package main

import "fmt"

func main() {
    slice := []int{1, 2, 3}
    for i, v := range slice {
        fmt.Printf("副本值: %d\n", v) // 副本值: 1
        // 副本值: 1
        // 副本值: 2
        // 副本值: 3
    }
}

```

## 9.2 range 详解

### 9.2.1 数组 range

#### 9.2.1.1 索引迭代

只获取索引。

```go

package main

import "fmt"

func main() {
    arr := [5]int{10, 20, 30, 40, 50}

    for i := range arr {
        fmt.Printf("索引: %d, 值: %d\n", i, arr[i])
        // 索引: 0, 值: 10
        // 索引: 1, 值: 20
        // 索引: 2, 值: 30
    }
}

```

#### 9.2.1.2 值迭代

只获取值。

```go

package main

import "fmt"

func main() {
    arr := [5]int{10, 20, 30, 40, 50}

    for _, v := range arr {
        fmt.Printf("值: %d\n", v)
        // 值: 10
        // 值: 20
        // 值: 30
    }
}

```

#### 9.2.1.3 索引值迭代

同时获取索引和值。

```go

package main

import "fmt"

func main() {
    arr := [3]string{"甲", "乙", "丙"}

    for i, v := range arr {
        fmt.Printf("%d: %s\n", i, v)
        // 0: 甲
        // 1: 乙
        // 2: 丙
    }
}

```

### 9.2.2 切片 range

#### 9.2.2.1 迭代语义

切片的遍历和数组相同。

```go

package main

import "fmt"

func main() {
    slice := []int{1, 2, 3}

    for i, v := range slice {
        fmt.Printf("slice[%d] = %d\n", i, v)
        // slice[0] = 1
        // slice[1] = 2
        // slice[2] = 3
    }
}

```

#### 9.2.2.2 副本陷阱

遍历切片时，值是元素的副本。

```go

package main

import "fmt"

func main() {
    s := []int{1, 2, 3}
    for i, v := range s {
        s[i] = v * 10
    }
    fmt.Printf("修改后: %v\n", s) // 修改后: [10 20 30]
}

```

### 9.2.3 字符串 range

#### 9.2.3.1 字节遍历

`range` 遍历字符串时，`i` 是字节索引，`v` 是字节值（byte）。

```go

package main

import "fmt"

func main() {
    str := "Hello"

    for i, v := range str {
        fmt.Printf("索引 %d: 字节值 %d (字符 '%c')\n", i, v, v)
        // 索引 0: 字节值 72 (字符 'H')
        // 索引 1: 字节值 101 (字符 'e')
    }
}

```

#### 9.2.3.2 符文遍历

Go 的字符串是 UTF-8 编码，需要用 `[]rune` 转换来正确遍历 Unicode 码点。

```go

package main

import "fmt"

func main() {
    str := "Hello世界"

    for i, v := range str {
        fmt.Printf("索引 %d: %c (字节值 %d)\n", i, v, v)
    }
}

```

### 9.2.4 map range

#### 9.2.4.1 键值迭代

遍历映射，返回键和值。

```go

package main

import "fmt"

func main() {
    m := map[string]int{
        "Apple":  1,
        "Banana": 2,
        "Cherry": 3,
    }

    for k, v := range m {
        fmt.Printf("%s: %d\n", k, v)
        // Apple: 1
        // Banana: 2
    }
}

```

#### 9.2.4.2 键迭代

只遍历键。

```go

package main

import "fmt"

func main() {
    m := map[string]int{
        "A": 1,
        "B": 2,
    }

    for k := range m {
        fmt.Printf("%s\n", k)
        // A
        // B
    }
}

```

#### 9.2.4.3 遍历顺序

映射的遍历顺序是随机的！

```go

package main

import "fmt"

func main() {
    m := map[string]int{
        "一": 1,
        "二": 2,
        "三": 3,
    }

    fmt.Println("遍历多次，观察顺序：")
    for i := 0; i < 3; i++ {
        fmt.Printf("第 %d 次: ", i+1)
        for k := range m {
            fmt.Printf("%s ", k)
        }
        fmt.Println()
    }
}

```

### 9.2.5 channel range

#### 9.2.5.1 接收迭代

`range` 可以遍历通道，直到通道关闭。

```go

package main

import "fmt"

func main() {
    ch := make(chan int, 5)

    for i := 1; i <= 3; i++ {
        ch <- i
    }
    close(ch)

    fmt.Println("从通道接收：")
    for v := range ch {
        fmt.Printf("%d ", v) // 1 2 3
    }
    fmt.Println("\n接收完成")
}

```

#### 9.2.5.2 关闭检测

通道关闭后，`range` 自动结束。

```go

package main

import "fmt"

func producer(ch chan int) {
    ch <- 1
    ch <- 2
    ch <- 3
    close(ch)
}

func main() {
    ch := make(chan int)
    go producer(ch)

    for v := range ch {
        fmt.Printf("收到: %d\n", v) // 收到: 1
    }
    fmt.Println("通道已关闭，循环结束")
}

```

## 9.3 循环控制

### 9.3.1 break

#### 9.3.1.1 直接跳出

`break` 用于跳出当前循环。

```go

package main

import "fmt"

func main() {
    for i := 1; i <= 10; i++ {
        if i == 5 {
            break
        }
        fmt.Printf("i = %d\n", i) // i = 0 // i = 1, 2, 3, 4
    }
    fmt.Println("循环在 i=5 时终止")
}

```

#### 9.3.1.2 标号跳出

`break` 可以配合标号跳出多重循环。

```go

package main

import "fmt"

func main() {
outer:
    for i := 0; i < 3; i++ {
        for j := 0; j < 3; j++ {
            if i == 1 && j == 1 {
                break outer
            }
            fmt.Printf("(%d, %d)\n", i, j)
            // (0, 0), (0, 1), (0, 2), (1, 0)
        }
    }
    fmt.Println("外层循环结束")
}

```

### 9.3.2 continue

#### 9.3.2.1 直接继续

`continue` 跳过本次循环，继续下一次。

```go

package main

import "fmt"

func main() {
    for i := 1; i <= 5; i++ {
        if i == 3 {
            continue
        }
        fmt.Printf("i = %d\n", i) // i = 0 // i = 1, 2, 4, 5
    }
}

```

#### 9.3.2.2 标号继续

`continue` 也可以配合标号继续指定循环。

```go

package main

import "fmt"

func main() {
outer:
    for i := 0; i < 2; i++ {
        for j := 0; j < 3; j++ {
            if j == 1 {
                continue outer
            }
            fmt.Printf("(%d, %d)\n", i, j)
            // (0, 0), (1, 0)
        }
    }
}

```

## 9.4 循环模式

### 9.4.1 无限循环模式

```go

package main

import "fmt"

func main() {
    count := 0
    for {
        count++
        if count > 5 {
            break
        }
        fmt.Printf("计数: %d\n", count) // 计数: 1, 2, 3, 4, 5
    }
}

```

### 9.4.2 条件循环模式

```go

package main

import "fmt"

func main() {
    n := 1
    for n < 50 {
        n *= 2
    }
    fmt.Printf("最终 n = %d\n", n) // 最终 n = 64
}

```

### 9.4.3 集合遍历模式

```go

package main

import "fmt"

func main() {
    nums := []int{1, 2, 3, 4, 5}
    sum := 0

    for _, v := range nums {
        sum += v
    }
    fmt.Printf("Sum = %d\n", sum) // Sum = 15
}

```

### 9.4.4 并行迭代模式

```go

package main

import (
    "fmt"
    "sync"
)

func main() {
    nums := []int{1, 2, 3, 4, 5}
    result := make([]int, len(nums))
    var wg sync.WaitGroup

    for i, v := range nums {
        wg.Add(1)
        go func(idx int, val int) {
            result[idx] = val * 2
            wg.Done()
        }(i, v)
    }

    wg.Wait()
    fmt.Printf("并行结果: %v\n", result) // 并行结果: [2 4 6 8 10]
}

```

## 9.5 循环性能

### 9.5.1 边界检查消除

编译器会优化掉不必要的边界检查。

```go

package main

import "fmt"

func main() {
    arr := [5]int{1, 2, 3, 4, 5}

    for i := 0; i < len(arr); i++ {
        fmt.Printf("arr[%d] = %d\n", i, arr[i])
    }
}

```

### 9.5.2 循环展开

编译器可能会将简单循环展开。

```go

package main

import "fmt"

func main() {
    sum := 0
    for i := 0; i < 4; i++ {
        sum += i
    }
    fmt.Printf("sum = %d\n", sum) // sum = 6
}

```

### 9.5.3 迭代变量优化

编译器可能会优化迭代变量的使用。

```go

package main

import "fmt"

func main() {
    for i := 0; i < 3; i++ {
        fmt.Printf("i = %d\n", i) // i = 0
    }
}

```

## 9.6 高级循环技巧

### 9.6.1 循环展开

手动展开循环减少迭代次数。

```go

package main

import "fmt"

func main() {
    nums := []int{1, 2, 3, 4, 5, 6}
    sum := 0

    for i := 0; i < len(nums); i += 2 {
        sum += nums[i]
        if i+1 < len(nums) {
            sum += nums[i+1]
        }
    }
    fmt.Printf("sum = %d\n", sum) // sum = 21
}

```

### 9.6.2 逆序遍历

```go

package main

import "fmt"

func main() {
    nums := []int{1, 2, 3, 4, 5}

    for i := len(nums) - 1; i >= 0; i-- {
        fmt.Printf("%d ", nums[i]) // 5 4 3 2 1
    }
    fmt.Println()
}

```

## 9.7 递归 vs 迭代

### 9.7.1 尾递归优化

Go 不支持尾递归优化，但可以用迭代替代。

```go

package main

import "fmt"

func main() {
    result := iterativeSum(100000)
    fmt.Printf("1+2+...+100000 = %d\n", result)
}

func iterativeSum(n int) int {
    sum := 0
    for i := 1; i <= n; i++ {
        sum += i
    }
    return sum
}

```

### 9.7.2 递归转迭代

将递归算法改写为迭代。

```go

package main

import "fmt"

func main() {
    fmt.Printf("递归 Fibonacci(10) = %d\n", fibRecursive(10))
    fmt.Printf("迭代 Fibonacci(10) = %d\n", fibIterative(10))
}

func fibRecursive(n int) int {
    if n <= 1 {
        return n
    }
    return fibRecursive(n-1) + fibRecursive(n-2)
}

func fibIterative(n int) int {
    if n <= 1 {
        return n
    }
    a, b := 0, 1
    for i := 2; i <= n; i++ {
        a, b = b, a+b
    }
    return b
}

```

### 9.7.3 相互递归

两个函数相互调用。

```go

package main

import "fmt"

func main() {
    fmt.Printf("isEven(10) = %t\n", isEven(10))
    fmt.Printf("isOdd(10) = %t\n", isOdd(10))
}

func isEven(n int) bool {
    if n == 0 {
        return true
    }
    return isOdd(n - 1)
}

func isOdd(n int) bool {
    if n == 0 {
        return false
    }
    return isEven(n - 1)
}
```


## 本章小结

本章我们学习了 Go 语言的循环语句：

1. **for 循环**：
   - 传统形式：`for i := 0; i < n; i++ { }`
   - 条件形式：`for 条件 { }`
   - 无限形式：`for { }`
   - `range` 形式：遍历数组、切片、字符串、映射、通道

2. **range 详解**：
   - 数组/切片：索引和值
   - 字符串：字节索引和字节值
   - 映射：无序遍历
   - 通道：阻塞接收直到关闭

3. **循环控制**：
   - `break`：跳出循环
   - `continue`：跳过本次循环
   - 标号配合使用可以控制多重循环

4. **循环模式**：
   - 无限循环、条件循环、集合遍历、并行迭代

5. **性能优化**：
   - 边界检查消除
   - 循环展开
   - 迭代变量优化

6. **递归 vs 迭代**：
   - Go 不支持尾递归优化
   - 推荐使用迭代替代递归

