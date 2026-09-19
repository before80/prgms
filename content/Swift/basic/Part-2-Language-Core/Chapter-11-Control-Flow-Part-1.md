+++
title = "第11章 控制流（一）：分支、循环与跳转"
weight = 110
date = "2026-09-14T22:30:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 第十一章：控制流（一）：分支、循环与跳转

> 程序真正开始“活”起来，是它会根据条件走不同路线、把同一段逻辑重复执行。控制流没有玄学，但 Swift 在细节上很讲究：条件必须是真正的 `Bool`，循环标签能让你从深层嵌套里优雅脱身，`if` 与 `switch` 还能直接产出值。

## 11.1 `if`：条件必须是 `Bool`

`if` 的形状和大多数语言一样，只有一条硬规矩：括号里必须是一个真正的 `Bool`。

```swift
let temperature = 31

if temperature > 30 {
    print("热")
} else if temperature > 20 {
    print("舒服")
} else {
    print("凉")
}
// prints: 热
```

Swift 不会把 `0`、空字符串、空数组自动当成 `false`：

```text
error: type 'Int' cannot be used as a boolean; test for '!= 0' instead
```

如果要判断集合是否为空，就明确写出来：

```swift
let names: [String] = []
if names.isEmpty {
    print("没有名字")
}
// prints: 没有名字
```

## 11.2 `if` 也是表达式

当每个分支都产生同一种类型的值时，可以直接把 `if` 的结果赋给变量：

```swift
let score = 86
let level = if score >= 90 { "A" } else if score >= 80 { "B" } else { "C" }
print(level)
// prints: B
```

求值顺序和普通 `if` 完全一样。注意：分支类型必须一致，也不能省略 `else`，否则编译器不知道“没有分支时”该得到什么。

分支里能不能多写几句、什么情况下允许以 `throw` 收尾，以及“为什么不能写 `do` 表达式”，第 15B.12 节有完整规则。

## 11.3 `for-in`：遍历是主旋律

Swift 的 `for` 只有一个形态——`for 元素 in 序列`，没有“初始化、条件、增量”那套三件套：

```swift
for number in 1...5 {
    print(number)
}
// prints: 1
// prints: 2
// prints: 3
// prints: 4
// prints: 5
```

`1...5` 是闭区间，`1..<5` 是半开区间：

```swift
for number in 1..<5 {
    print(number)
}
// prints: 1
// prints: 2
// prints: 3
// prints: 4
```

遍历数组时经常同时要下标：

```swift
let fruits = ["apple", "pear"]
for (index, fruit) in fruits.enumerated() {
    print(index, fruit)
}
// prints: 0 apple
// prints: 1 pear
```

`stride` 适合不等步长：

```swift
for value in stride(from: 0, through: 10, by: 2) {
    print(value)
}
// prints: 0
// prints: 2
// prints: 4
// prints: 6
// prints: 8
// prints: 10
```

## 11.4 `while` 与 `repeat-while`

`while` 先判断再执行：

```swift
var countdown = 3
while countdown > 0 {
    print(countdown)
    countdown -= 1
}
// prints: 3
// prints: 2
// prints: 1
```

`repeat-while` 至少执行一次，适合“先做一次再看结果”的流程：

```swift
var input = ""
repeat {
    input += "x"
} while input.count < 2
print(input)
// prints: xx
```

遍历集合通常优先用 `for-in`；`while` 更适合“循环次数事先不知道，只关心何时满足条件”。

## 11.5 `break`、`continue` 与标签

`continue` 跳过本轮剩余代码，`break` 结束整个循环：

```swift
for number in 0..<5 {
    if number == 1 { continue }
    if number == 4 { break }
    print(number)
}
// prints: 0
// prints: 2
// prints: 3
```

嵌套循环里，`break` 默认只结束最内层。想直接结束外层，就给外层循环贴标签：

```swift
outer: for i in 1...3 {
    for j in 1...3 {
        if i * j == 4 {
            print("found", i, j)
            break outer
        }
    }
}
// prints: found 2 2
```

标签同样可以配合 `continue`，直接进入指定层的下一轮。标签名不超过一个单词，冒号紧贴循环关键字。

## 11.6 `where`：给循环再加一道门槛

`for-in` 可以带 `where`，它等价于在循环体开头写一个 `if`，但读起来更集中：

```swift
for number in 1...10 where number.isMultiple(of: 3) {
    print(number)
}
// prints: 3
// prints: 6
// prints: 9
```

`where` 只负责过滤，不负责变换。需要同时比较原值和变换结果时，老实用 `if` 更清楚。

## 11.7 `defer`：离开作用域前的收尾

普通的 `do { ... }` 可以单独创造一个作用域。它常和 `defer`、临时变量以及错误处理配合：

```swift
do {
    let temporary = "只在这个块里存在"
    print(temporary)
}
// prints: 只在这个块里存在
```

`temporary` 不会泄漏到 `do` 之外。作用域越小，变量的影响范围就越容易看清。

`defer` 注册一段代码，当前作用域结束时执行。多个 `defer` 按后进先出执行：

```swift
func work() {
    defer { print("最后执行") }
    defer { print("先于上一条") }
    print("正在工作")
}

work()
// prints: 正在工作
// prints: 先于上一条
// prints: 最后执行
```

它常用于释放资源、恢复状态或记录结束日志。即使函数中途 `return` 或 `throw`，已注册的 `defer` 仍会执行。注意：`defer` 不能用来改变已经定好的返回值类型，也不能替代错误处理。

## 11.8 本章小结

| 结构 | 用途 | 关键点 |
| --- | --- | --- |
| `if` | 二选一或链式分支 | 条件必须是 `Bool` |
| `if` 表达式 | 直接产生一个值 | 所有分支类型一致，必须有兜底分支 |
| `for-in` | 遍历序列或区间 | 可配 `where` |
| `while` | 先判断再循环 | 可能一次也不执行 |
| `repeat-while` | 至少执行一次 | 条件在末尾 |
| `break` / `continue` | 跳出 / 提前下一轮 | 可配循环标签处理嵌套 |
| `defer` | 离开作用域时收尾 | 后进先出，异常路径也会执行 |

## 11.9 本章易错点速查

| 易错点 | 正确理解 |
| --- | --- |
| 把整数条件写成 `if value` | 必须显式写成 `if value != 0` |
| 想用 `if` 表达式却漏掉 `else` | 表达式必须能覆盖所有路径 |
| 以为 `break` 能跳出所有循环 | 默认只跳出当前层，嵌套时使用标签 |
| `repeat-while` 和 `while` 混用 | 前者至少执行一次，后者可能零次 |
| 在 `for-in` 中修改被遍历集合 | 容易产生意外行为，先收集修改意图 |
| 忘记 `defer` 的执行顺序 | 后来注册的先执行 |

## 11.10 下章预告

下一章的 `switch` 不是“多分支版的 `if`”，而是一台模式匹配引擎：它能把区间、元组、枚举、可选值、类型转换甚至自定义表达式放进 `case` 里。放心，它没有隐式穿透，也不会因为你少写一个 `break` 就把事情搞乱。
