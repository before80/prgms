+++
title = "第6章 语句概述"
weight = 60
date = "2026-03-20T08:39:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false

+++
# 第6章 语句概述

> 欢迎来到第六章！这一章我们要聊的是 Go 语言的"语句"。语句是什么？语句就是告诉计算机"做什么"的动作指令。如果说变量是名词，那语句就是动词——变量是名词的话，语句就是告诉计算机要做什么。顺序执行、条件判断、循环往复……这些都是语句的功能。准备好了吗？让我们开始吧！

## 6.1 语句分类

> Go 语言的语句可以分为三大类：简单语句、复合语句和控制语句。这就像是你日常生活中的行动——有些是一个人就能完成的（简单语句），有些需要团队配合（复合语句），还有些需要动脑筋做决定（控制语句）。

### 6.1.1 简单语句

简单语句是那些不需要大括号包围的独立语句。它们是 Go 代码的"基本粒子"。

```go

package main

import "fmt"

var globalVar = "我是一个全局变量"

func main() {
    // 表达式语句：调用函数
    fmt.Println("这是表达式语句") // 这是表达式语句

    // 赋值语句
    x := 10
    x = 20

    // 短变量声明语句
    y := 30

    // 空语句（什么都不做）
    ;
}

```

### 6.1.2 复合语句

复合语句是用大括号 `{}` 包围的语句序列。它们需要多个语句配合完成一个任务。

```go

package main

import "fmt"

func main() {
    // if 语句（复合语句）
    if x := 10; x > 5 {
        fmt.Printf("x = %d 大于 5\n", x) // x = 10 大于 5
    }

    // for 语句（复合语句）
    sum := 0
    for i := 1; i <= 5; i++ {
        sum += i
    }
    fmt.Printf("1+2+3+4+5 = %d\n", sum) // 1+2+3+4+5 = 15
}

```

### 6.1.3 控制语句

控制语句用于控制程序的执行流程——决定代码什么时候跑、往哪里跑。

```go

package main

import "fmt"

func main() {
    // if-else 控制流
    x := 10
    if x > 5 {
        fmt.Println("x 大于 5") // x 大于 5
    } else {
        fmt.Println("x 不大于 5") // 不会执行，因为 x=10 > 5
    }

    // switch 控制流
    day := 3
    switch day {
    case 1:
        fmt.Println("星期一") // 不会执行，day=3
    case 2:
        fmt.Println("星期二") // 不会执行，day=3
    case 3:
        fmt.Println("星期三") // 星期三
    default:
        fmt.Println("其他") // 其他
    }

    // for 循环控制流
    for i := 0; i < 3; i++ {
        if i == 2 {
            break // 跳出循环
        }
        fmt.Printf("i = %d\n", i) // i = 0
        // i = 0
        // i = 1
    }
}

```

## 6.2 空语句

空语句是什么都不做的语句。在 Go 中，你只需要写一个分号 `;` 就可以了。

```go

package main

import "fmt"

func main() {
    // 空语句通常用于占位
    ; // 这是一个空语句，什么都不做

    // 或者在 for 循环中
    sum := 0
    i := 0
    for ; i <= 10; i++ {
        sum += i
    }
    fmt.Printf("0+1+2+...+10 = %d\n", sum) // 0+1+2+...+10 = 55

    // for 的三个部分都可以省略
    j := 0
    for j < 3 {
        fmt.Printf("j = %d\n", j) // j = 0, j = 1, j = 2
        j++
    }
}

```

## 6.3 标号语句

标号语句（Label Statement）用于给语句打标签，主要配合 `goto`、`break`、`continue` 使用。这就像是给楼层贴门牌号，方便电梯（控制流）找到要去的地方。

```go

package main

import "fmt"

func main() {
    // 定义一个标号
    fmt.Println("开始执行") // 开始执行

    goto skip

    // 这段代码会被跳过
    fmt.Println("这段不会打印") // 不会打印，被 goto 跳过

skip:
    fmt.Println("跳到这里了！") // 跳到这里了！
}

```

标号更常用的场景是跳出多重循环：

```go

package main

import "fmt"

func main() {
    // 使用标号指定跳到哪个循环
outer:
    for i := 0; i < 3; i++ {
        for j := 0; j < 3; j++ {
            if i == 1 && j == 1 {
                fmt.Println("找到特殊位置，退出外层循环") // 找到特殊位置，退出外层循环
                break outer
            }
            fmt.Printf("(%d, %d)\n", i, j) // (0, 0)
            // (0, 0), (0, 1), (0, 2)
            // (1, 0), (1, 1)
        }
    }
}

```

## 6.4 语句块

语句块是用大括号 `{}` 包围的代码区域。在语句块中声明的变量，只在该块内部可见。

```go

package main

import "fmt"

func main() {
    // 这是一个语句块
    {
        x := 10
        fmt.Printf("块内: x = %d\n", x) // 块内: x = 10
    }
    // x 在这里不可见！
    // fmt.Printf("块外: x = %d\n", x) // ❌ 编译错误：undefined: x

    // if 语句的块
    if x := 5; x > 0 {
        fmt.Printf("if 块内: x = %d\n", x) // if 块内: x = 5
    }

    // for 语句的块
    for i := 0; i < 2; i++ {
        fmt.Printf("for 块内: i = %d\n", i) // for 块内: i = 0
        // for 块内: i = 0
        // for 块内: i = 1
    }
}
```

## 本章小结

本章我们学习了 Go 语言语句的基本概念：

1. **语句分类**：
   - **简单语句**：表达式语句、赋值语句、声明语句等
   - **复合语句**：用 `{}` 包围的语句序列，如 if、for
   - **控制语句**：控制程序执行流程的语句

2. **空语句**：什么操作都不做的语句，用 `;` 表示

3. **标号语句**：给语句打标签，用于 `goto`、`break`、`continue`

4. **语句块**：用 `{}` 包围的代码区域，块内声明的变量只在块内可见

