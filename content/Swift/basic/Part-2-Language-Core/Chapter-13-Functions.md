+++
title = "第13章 函数：参数标签、inout 与函数类型"
weight = 130
date = "2026-09-14T22:30:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 第十三章：函数：参数标签、`inout` 与函数类型

> 函数是把一段逻辑装进盒子并给它取名的工具。Swift 的特别之处在于，调用处的参数标签是接口设计的一部分：`move(from:to:)` 读起来像句子；函数本身又是一等公民，可以赋给变量、当作参数、从函数里返回。闭包、回调和 SwiftUI 都建立在这套机制上。

## 13.1 定义与调用

一个函数最少要有三样东西：名字、参数表、返回值类型。

```swift
func add(_ a: Int, _ b: Int) -> Int {
    a + b
}

print(add(2, 3))
// prints: 5
```

单表达式函数可以省略 `return`。如果需要多行逻辑，就老老实实写 `return`：

```swift
func describe(_ value: Int) -> String {
    if value > 0 { return "正数" }
    return "非正数"
}

print(describe(7))
// prints: 正数
```

无返回值函数写作 `-> Void`，通常省略：

```swift
func hello() {
    print("hello")
}
hello()
// prints: hello
```

## 13.2 参数标签：让调用处说人话

第一个参数标签是调用处看到的词，第二个是函数体使用的名字：

```swift
func move(from start: Int, to end: Int) {
    print("从 \(start) 到 \(end)")
}

move(from: 1, to: 5)
// prints: 从 1 到 5
```

下划线表示调用时省略标签：

```swift
func square(_ value: Int) -> Int {
    value * value
}
print(square(4))
// prints: 16
```

只有一个名字时，它同时是标签和内部名称：

```swift
func greet(name: String) {
    print("你好，\(name)")
}
greet(name: "Mia")
// prints: 你好，Mia
```

参数标签不是装饰，而是 API 的一部分。设计清晰后，调用处往往像自然语言一样能自解释。

## 13.3 默认值、可变参数与 `inout`

默认值让常用场景更短：

```swift
func greet(_ name: String, punctuation: String = "!") {
    print("你好，\(name)\(punctuation)")
}

greet("Lin")
// prints: 你好，Lin!
greet("Lin", punctuation: "。")
// prints: 你好，Lin。
```

可变参数用 `...` 接收任意数量同类型参数，函数内部把它当成数组：

```swift
func sum(_ numbers: Int...) -> Int {
    numbers.reduce(0, +)
}
print(sum(1, 2, 3, 4))
// prints: 10
```

默认参数可以出现在参数列表的任意位置；可变参数后面也可以继续放其他参数。真正要注意的是调用处的歧义：后面的参数最好有清楚的标签，否则编译器很难判断某个实参到底属于谁。

`inout` 允许函数修改传入变量本身：

```swift
func doubleInPlace(_ value: inout Int) {
    value *= 2
}

var number = 21
doubleInPlace(&number)
print(number)
// prints: 42
```

调用时必须加 `&`。`inout` 不是“引用传递”的同义词：它保证函数获得一个可写副本，返回时再写回原位置。代价是这个副本在函数执行期间“独占”了原变量，同一个变量不能在调用里出现两次：

```swift
func take2(_ a: inout Int, _ b: inout Int) {}

var number = 0
take2(&number, &number)
```

```text
error: inout arguments are not allowed to alias each other
```

另有一类别名冲突编译器不一定能在编译期看出来，于是留到运行期兜底：函数正在写一个变量，代码又去读同一个变量，程序会当场停下，打印

```text
Simultaneous accesses to 0x..., but modification requires exclusive access.
```

两种情况说的是同一条规矩——**同一时刻，一个变量要么被读、要么被写**。完整规则在第 29 章展开。

本节这三个写法（`_` 标签、默认参数、可变参数、`inout` 的 `&`）都属于“函数的语法糖”，第 15B.5 节把它们和“方法当函数值”“运算符当函数值”“`some P` 参数”放在一起做了汇总。

## 13.4 返回多个值和提前退出

需要多个结果时用元组：

```swift
func divmod(_ a: Int, _ b: Int) -> (quotient: Int, remainder: Int) {
    (a / b, a % b)
}
let result = divmod(17, 5)
print(result.quotient, result.remainder)
// prints: 3 2
```

`guard` 负责把失败路径赶出函数：

```swift
func initial(_ text: String) -> Character? {
    guard let first = text.first else { return nil }
    return first
}
print(initial("Swift") as Any)
// prints: Optional("S")
```

## 13.5 嵌套函数：把辅助逻辑关在门内

函数里可以再定义函数：

```swift
func makeCounter() -> () -> Int {
    var count = 0
    func next() -> Int {
        count += 1
        return count
    }
    return next
}

let counter = makeCounter()
print(counter(), counter(), counter())
// prints: 1 2 3
```

`next` 捕获了外部的 `count`，所以每次调用都会继续累加。这正好是理解下一章闭包的入口。

## 13.6 函数类型：函数也是值

函数类型由参数和返回值组成，例如 `(Int, Int) -> Int`：

```swift
func add(_ a: Int, _ b: Int) -> Int { a + b }
func multiply(_ a: Int, _ b: Int) -> Int { a * b }

var operation: (Int, Int) -> Int = add
print(operation(3, 4))
// prints: 7

operation = multiply
print(operation(3, 4))
// prints: 12
```

函数可以接收函数，也可以返回函数：

```swift
func apply(_ value: Int, using operation: (Int) -> Int) -> Int {
    operation(value)
}

print(apply(5, using: { $0 * 2 }))
// prints: 10

func makeAdder(_ amount: Int) -> (Int) -> Int {
    { value in value + amount }
}

let addTen = makeAdder(10)
print(addTen(5))
// prints: 15
```

## 13.7 `@discardableResult` 与重载

有些函数的结果经常可以忽略，但仍希望保留返回值：

```swift
@discardableResult
func save(_ name: String) -> Bool {
    print("保存 \(name)")
    return true
}

save("settings")
// prints: 保存 settings
```

没有这个属性时，忽略返回值会产生警告；加了它，调用方可以选择接收或不接收。

函数重载指同名但参数类型或标签不同的函数：

```swift
func show(_ value: Int) { print("整数 \(value)") }
func show(_ value: String) { print("字符串 \(value)") }

show(7)
// prints: 整数 7
show("七")
// prints: 字符串 七
```

编译器根据实参类型选择重载。不要只靠返回值类型区分重载，那样的调用经常无法推断。

## 13.8 参数模式与可变参数的小陷阱

参数名本身就是一个局部作用域。函数体里不能再定义同名变量：

```text
error: invalid redeclaration of 'name'
```

可变参数每次调用都会得到一个数组，空调用时就是空数组：

```swift
func countAll(_ values: Int...) -> Int {
    values.count
}
print(countAll())
// prints: 0
```

`inout` 参数不能有默认值，也不能是 `let` 常量。传入前要确保变量类型完全匹配，Swift 不会为了 `inout` 偷做隐式转换。

## 13.9 本章小结

| 主题 | 要点 |
| --- | --- |
| 参数标签 | 调用处的可读性由标签决定，`_` 表示省略 |
| 默认值 | 常见参数可省略，调用处更短 |
| 可变参数 | `T...`，函数内是 `[T]` |
| `inout` | 调用加 `&`，可写回原变量，有独占访问限制 |
| 返回值 | 单表达式可省略 `return`，多值用元组 |
| 函数类型 | `(参数) -> 返回值`，函数可以传递和返回 |
| 嵌套函数 | 能捕获外层变量，形成闭包 |
| `@discardableResult` | 允许安全忽略返回值 |

## 13.10 本章易错点速查

| 易错点 | 正确理解 |
| --- | --- |
| 忽略参数标签设计 | 调用处会变得难读，标签是 API 的一部分 |
| 认为 `_` 是参数名 | `_` 只是“调用时不需要标签” |
| 在 `inout` 调用处漏写 `&` | 必须写 `&number` |
| 把 `inout` 当成共享引用 | 它遵守独占访问规则，不能产生重叠访问 |
| 用返回值类型做过载区分 | 编译器通常无法仅凭返回值选择重载 |
| 忘记函数类型也要写完整 | 例如 `(Int) -> String`，参数标签不进入函数类型 |

## 13.11 下章预告

函数已经能当值用了，下一步就是让它的定义更轻、更贴近调用现场。闭包会把这些“函数值”写得像一段可移动的逻辑，同时引入捕获、逃逸和循环引用这些必须认真对待的细节。
