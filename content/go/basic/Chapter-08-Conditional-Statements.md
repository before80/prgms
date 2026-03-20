+++
title = "第8章 条件语句"
weight = 80
date = "2026-03-20T08:39:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false

+++
# 第8章 条件语句

> 欢迎来到第八章！这一章我们要聊的是 Go 语言的"条件语句"。条件语句是什么？条件语句就是让程序做决定的语句——"如果今天下雨，我就带伞；否则，我就去跑步。"这就是一个典型的条件语句。程序有了条件语句，就像人有了判断力，不再是"一根筋"地执行到底了。

## 8.1 if 语句

### 8.1.1 简单条件

`if` 语句是最基本的条件判断。如果条件为 `true`，就执行 `if` 块内的代码；否则就跳过。

```go

package main

import "fmt"

func main() {
    age := 18

    if age >= 18 {
        fmt.Println("已成年，可以投票") // 已成年，可以投票
    }

    // 条件不满足，不执行
    if age < 18 {
        fmt.Println("未成年，不能投票") // 不会执行，age=18
    }
}

```

### 8.1.2 带初始化的条件

#### 8.1.2.1 初始化子句

`if` 语句可以包含一个初始化子句，在判断条件之前执行。这就像是"先打扫屋子，再请客人进门"。

```go

package main

import "fmt"

func main() {
    // 初始化 + 条件判断
    if age := 18; age >= 18 {
        fmt.Printf("年龄是 %d，已成年\n", age) // 年龄是 18，已成年
    }

    // 初始化部分定义的变量，只能在 if 块内访问
    if name := getName(); name != "" {
        fmt.Printf("名字是 %s\n", name) // 名字是 小明
    }
    // name 在这里不可见！
}

func getName() string {
    return "小明"
}

```

#### 8.1.2.2 作用域规则

在 `if` 初始化子句中声明的变量，只在该 `if` 语句的作用域内可见。

```go

package main

import "fmt"

func main() {
    // 错误示例：想在 if 外面使用初始化子句中声明的变量
    // if x := 10; x > 5 {
    //     fmt.Println("x =", x)
    // }
    // fmt.Println(x) // ❌ 编译错误：undefined: x

    // 正确做法：如果需要在 if 外面使用，先声明变量
    x := 10
    if x > 5 {
        fmt.Println("x =", x) // x = 10
    }
    fmt.Println("if 外面 x =", x) // if 外面 x = 10
}

```

### 8.1.3 if-else 链

`if-else` 链让你可以在多个条件中选择。

```go

package main

import "fmt"

func main() {
    score := 85

    if score >= 90 {
        fmt.Println("成绩等级：优秀！") // 成绩等级：优秀！
    } else if score >= 70 {
        fmt.Println("成绩等级：良好") // 成绩等级：良好
    } else if score >= 60 {
        fmt.Println("成绩等级：及格") // 不会执行，score=85 > 70
    } else {
        fmt.Println("成绩等级：不及格") // 不会执行
    }
}

```

### 8.1.4 嵌套 if

`if` 语句可以嵌套使用，就像俄罗斯套娃一样。

```go

package main

import "fmt"

func main() {
    age := 25
    hasTicket := true

    if age >= 18 {
        fmt.Println("年龄达标") // 年龄达标
        if hasTicket {
            fmt.Println("有票，可以入场") // 有票，可以入场
        } else {
            fmt.Println("没票，不能入场") // 不会执行，hasTicket=true
        }
    } else {
        fmt.Println("年龄不达标") // 不会执行
    }
}

```

## 8.2 switch 语句

### 8.2.1 表达式 switch

#### 8.2.1.1 switch 表达式

`switch` 语句是 `if-else` 链的简化版，特别适合多分支判断。

```go

package main

import "fmt"

func main() {
    day := 3

    switch day {
    case 1:
        fmt.Println("星期一") // 不会执行，day=3
    case 2:
        fmt.Println("星期二") // 不会执行，day=3
    case 3:
        fmt.Println("星期三") // 星期三
    case 4:
        fmt.Println("星期四") // 不会执行，day=3
    case 5:
        fmt.Println("星期五") // 不会执行，day=3
    default:
        fmt.Println("周末") // 不会执行
    }
}

```

#### 8.2.1.2 case 表达式

`case` 后面可以跟多个值，用逗号分隔。

```go

package main

import "fmt"

func main() {
    grade := 'B'

    switch grade {
    case 'A', 'B', 'C':
        fmt.Println("及格") // 及格
    case 'D', 'E', 'F':
        fmt.Println("不及格") // 不会执行
    default:
        fmt.Println("无效成绩") // 不会执行
    }
}

```

#### 8.2.1.3 case 列表

一个 `case` 可以匹配多个值。

```go

package main

import "fmt"

func main() {
    month := 12

    switch month {
    case 1, 2, 3:
        fmt.Println("第一季度") // 不会执行
    case 4, 5, 6:
        fmt.Println("第二季度") // 不会执行
    case 7, 8, 9:
        fmt.Println("第三季度") // 不会执行
    case 10, 11, 12:
        fmt.Println("第四季度") // 第四季度
    }
}

```

#### 8.2.1.4 default 分支

`default` 分支在没有匹配的情况下执行。

```go

package main

import "fmt"

func main() {
    color := "purple"

    switch color {
    case "red":
        fmt.Println("红色") // 不会执行
    case "blue":
        fmt.Println("蓝色") // 不会执行
    case "green":
        fmt.Println("绿色") // 不会执行
    default:
        fmt.Println("其他颜色") // 其他颜色
    }
}

```

### 8.2.2 类型 switch

#### 8.2.2.1 类型断言语法

类型 switch 用于判断接口变量的实际类型。

```go

package main

import "fmt"

func main() {
    var i interface{} = 42

    switch v := i.(type) {
    case int:
        fmt.Printf("是 int 类型，值是 %d\n", v) // 是 int 类型，值是 42 // 是 int 类型，值是 42
    case string:
        fmt.Printf("是 string 类型，值是 %s\n", v) // 不会执行，因为 v 是 int 类型
    case float64:
        fmt.Printf("是 float64 类型，值是 %f\n", v) // 不会执行
    default:
        fmt.Println("其他类型") // 不会执行
    }
}

```

#### 8.2.2.2 case 类型

`case` 后面可以跟类型名。

```go

package main

import "fmt"

func main() {
    checkType("hello") // 是字符串: hello
    checkType(123)     // 是整数: 123
    checkType(3.14)   // 是浮点数: 3.14
}

func checkType(v interface{}) {
    switch v.(type) {
    case int:
        fmt.Printf("是整数: %d\n", v.(int)) // 是整数: 123
    case string:
        fmt.Printf("是字符串: %s\n", v.(string)) // 不会执行
    case float64:
        fmt.Printf("是浮点数: %f\n", v.(float64)) // 不会执行
    }
}

```

### 8.2.3 无条件 switch

#### 8.2.3.1 替代 if-else 链

没有表达式的 `switch` 相当于 `switch true`，可以替代 `if-else if` 链。

```go

package main

import "fmt"

func main() {
    score := 85

    switch {
    case score >= 90:
        fmt.Println("优秀") // 不会执行
    case score >= 70:
        fmt.Println("良好") // 良好
    case score >= 60:
        fmt.Println("及格") // 及格
    default:
        fmt.Println("不及格") // 不会执行
    }
}

```

#### 8.2.3.2 逻辑条件

可以在 `case` 中写更复杂的条件。

```go

package main

import "fmt"

func main() {
    age := 20
    hasLicense := true

    switch {
    case age < 18:
        fmt.Println("不能开车") // 不会执行
    case age >= 18 && !hasLicense:
        fmt.Println("需要考驾照") // 不会执行
    case age >= 18 && hasLicense:
        fmt.Println("可以开车") // 可以开车
    }
}

```

### 8.2.4 case 执行

#### 8.2.4.1 自动 break

Go 的 `switch` case 执行完会自动 break，不会"穿透"到下一个 case。

```go

package main

import "fmt"

func main() {
    num := 2

    switch num {
    case 1:
        fmt.Println("case 1") // case 1
    case 2:
        fmt.Println("case 2") // case 2
    case 3:
        fmt.Println("case 3") // case 3
    }
    // 不会继续执行 case 3！
}

```

#### 8.2.4.2 fallthrough

如果你想让 case "穿透"到下一个 case，可以使用 `fallthrough`。

```go

package main

import "fmt"

func main() {
    num := 2

    switch num {
    case 1:
        fmt.Println("case 1") // case 1
        fallthrough
    case 2:
        fmt.Println("case 2") // case 2
        fallthrough
    case 3:
        fmt.Println("case 3") // case 3 // case 3（穿透上来）
    }
}

```

#### 8.2.4.3 多 case 合并

多个 case 可以合并。

```go

package main

import "fmt"

func main() {
    char := 'e'

    switch char {
    case 'a', 'e', 'i', 'o', 'u':
        fmt.Println("是元音") // 是元音
    case 'b', 'c', 'd', 'f':
        fmt.Println("是辅音") // 不会执行
    default:
        fmt.Println("其他字符") // 不会执行
    }
}

```

## 8.3 条件优化

### 8.3.1 短路求值优化

Go 使用短路求值来优化布尔表达式。

```go

package main

import "fmt"

func main() {
    // && 的短路：第一个为 false，后面不计算
    a := false
    result := a && expensiveOperation()
    fmt.Printf("a && result = %t\n", result) // a && result = false
    // expensiveOperation() 没有被调用！

    // || 的短路：第一个为 true，后面不计算
    b := true
    result = b || expensiveOperation()
    fmt.Printf("b || result = %t\n", result) // b || result = true
    // expensiveOperation() 没有被调用！
}

func expensiveOperation() bool {
    fmt.Println("这个函数被调用了！") // 不会被调用（短路求值）
    return true
}

```

### 8.3.2 分支预测

现代 CPU 会尝试预测分支走向，Go 编译器也会优化。

```go

package main

import "fmt"

func main() {
    // 常见的分支预测优化
    for i := 0; i < 100; i++ {
        if i%2 == 0 {
            fmt.Printf("%d 是偶数\n", i) // %d 是偶数
        } else {
            fmt.Printf("%d 是奇数\n", i) // %d 是奇数
        }
    }
}

```

### 8.3.3 条件编译

使用构建标签可以实现条件编译。

```go

// +build linux

package main

import "fmt"

func main() {
    fmt.Println("只在 Linux 上编译") // 只在 Linux 上编译
}

```


## 本章小结

本章我们学习了 Go 语言的条件语句：

1. **if 语句**：
   - 简单条件：`if 条件 { ... }`
   - 带初始化：`if 初始化; 条件 { ... }`
   - `if-else` 链：多个条件判断
   - 嵌套 `if`：在 `if` 块内再判断

2. **switch 语句**：
   - 表达式 switch：`switch 表达式 { case 值: ... }`
   - 类型 switch：`switch v := i.(type) { case 类型: ... }`
   - 无条件 switch：`switch { case 条件: ... }`
   - `default` 分支：都不匹配时执行

3. **case 执行**：
   - 自动 `break`：不会穿透到下一个 case
   - `fallthrough`：强制穿透到下一个 case
   - 多个值：`case 1, 2, 3:` 匹配多个值

4. **条件优化**：
   - 短路求值：`&&` 和 `||` 的优化
   - 分支预测：CPU 和编译器优化
   - 条件编译：使用构建标签

