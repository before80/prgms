+++
title = "第7章 简单语句"
weight = 70
date = "2026-03-20T08:39:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false

+++
# 第7章 简单语句

> 欢迎来到第七章！这一章我们要聊的是 Go 语言的"简单语句"。简单语句是那些不需要大括号包围的独立语句，它们是 Go 代码的"基本粒子"。虽然叫"简单"，但功能可不简单哦！

## 7.1 表达式语句

表达式语句是在表达式后面加上分号（或者换行自动加分号）。最常见的就是函数调用。

```go

package main

import "fmt"

func greet(name string) string {
    return "你好，" + name + "！"
}

func main() {
    // 函数调用表达式语句
    fmt.Println("Hello, World!") // Hello, World!

    // 方法调用表达式语句
    msg := greet("小明")
    fmt.Println(msg) // 你好，小明！

    // 带接收者的方法调用
    s := "hello"
    fmt.Println("转为大写:", toUpper(s)) // 转为大写: HELLO
}

func toUpper(s string) string {
    result := ""
    for _, c := range s {
        if c >= 'a' && c <= 'z' {
            result += string(c - 'a' + 'A')
        } else {
            result += string(c)
        }
    }
    return result
}

```

## 7.2 自增语句 ++

自增语句 `++` 让变量加 1。这就像是按一下计算器的 "+1" 按钮。

```go

package main

import "fmt"

func main() {
    // 前置自增
    a := 0
    a++
    fmt.Printf("a = %d\n", a) // a = 1

    // 后置自增
    b := 5
    b++
    fmt.Printf("b = %d\n", b) // b = 6

    // 在表达式中使用（返回值是增加前的值）
    c := 10
    d := c++
    fmt.Printf("c = %d, d = %d\n", c, d) // c = 11, d = 10

    // 循环中的经典用法
    for i := 0; i < 3; i++ {
        fmt.Printf("循环第 %d 次\n", i+1) // 循环第 1 次
        // 循环第 1 次
        // 循环第 2 次
        // 循环第 3 次
    }
}

```

> **注意**：`++` 是语句，不是表达式。你不能写 `e := c++`，也不能写 `fmt.Println(c++)`。

## 7.3 自减语句 --

自减语句 `--` 让变量减 1。这就像是按计算器的 "-1" 按钮。

```go

package main

import "fmt"

func main() {
    x := 10
    x--
    fmt.Printf("x = %d\n", x) // x = 9

    y := 3
    y--
    fmt.Printf("y = %d\n", y) // y = 2

    // 递减循环
    fmt.Print("倒计时：") // 倒计时：
    for t := 3; t > 0; t-- {
        fmt.Printf("%d ", t) // 3 2 1 
    }
    fmt.Println("发射！") // 发射！
    // 3 2 1 发射！
}

```

## 7.4 赋值语句

### 7.4.1 普通赋值

普通赋值是最基本的赋值操作，使用 `=` 运算符。

```go

package main

import "fmt"

func main() {
    var x int
    x = 100
    fmt.Printf("x = %d\n", x) // x = 100

    x = 200
    fmt.Printf("x = %d\n", x) // x = 200

    // 不同类型不能直接赋值
    var y int
    // y = 3.14 // ❌ 编译错误：cannot use 3.14 (type float64) as type int
    fmt.Printf("y = %d\n", y) // y = 0
}

```

### 7.4.2 元组赋值

元组赋值允许同时给多个变量赋值。

```go

package main

import "fmt"

func main() {
    // 同时赋值多个变量
    a, b, c := 1, 2, 3
    fmt.Printf("a=%d, b=%d, c=%d\n", a, b, c) // a=1, b=2, c=3

    // 交换两个变量的值（无需临时变量）
    x, y := 10, 20
    x, y = y, x
    fmt.Printf("交换后: x=%d, y=%d\n", x, y) // 交换后: x=20, y=10

    // 同时返回多个值的函数
    result, err := divide(10, 2)
    if err != nil {
        fmt.Printf("错误: %s\n", err) // 这行不会执行，因为 divide(10,2) 成功
    } else {
        fmt.Printf("10 / 2 = %d\n", result) // 10 / 2 = 5
    }
}

func divide(a, b int) (int, error) {
    if b == 0 {
        return 0, fmt.Errorf("除数不能为零")
    }
    return a / b, nil
}

```

## 7.5 短变量声明语句

短变量声明语句 `:=` 是 Go 语言的特色之一，用于在函数内部快速声明新变量。

```go

package main

import "fmt"

func main() {
    // 基本用法
    name := "张三"
    age := 25
    fmt.Printf("%s 今年 %d 岁\n", name, age) // 张三 今年 25 岁

    // 同时声明多个变量
    width, height := 1920.0, 1080.0
    fmt.Printf("分辨率: %.0f x %.0f\n", width, height) // 分辨率: 1920 x 1080

    // 混合声明（新变量和已存在变量的赋值）
    newName := "李四"
    newName, age = "王五", 30 // newName 是新声明的，age 是已存在的
    fmt.Printf("%s 今年 %d 岁\n", newName, age) // 王五 今年 30 岁
}

```

> **重要**：`:=` 左边至少要有一个新变量，否则会编译错误。


## 本章小结

本章我们学习了 Go 语言的简单语句：

1. **表达式语句**：函数调用、方法调用等
2. **自增 `++` 和自减 `--`**：让变量加/减 1，是语句不是表达式
3. **赋值语句**：
   - 普通赋值 `=`
   - 元组赋值：同时给多个变量赋值，如 `a, b = b, a`
4. **短变量声明 `:=`**：在函数内部快速声明新变量，左边至少要有一个新变量

