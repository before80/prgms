+++
title = "第14章 闭包：捕获、逃逸与 @autoclosure"
weight = 140
date = "2026-09-14T22:30:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 第十四章：闭包：捕获、逃逸与 `@autoclosure`

> 闭包是“随身携带的代码块”。它可以脱离定义位置继续使用，还能记住定义时附近的变量。语法轻得像随手写的表达式，但捕获、逃逸和内存生命周期又足够深，值得你在这里慢下来。

## 14.1 闭包表达式：从完整写法到极简写法

闭包可以像函数一样接收参数、返回值：

```swift
let square = { (value: Int) -> Int in
    value * value
}
print(square(5))
// prints: 25
```

当类型能从上下文推断时，可以省略参数类型和箭头：

```swift
let double: (Int) -> Int = { value in
    value * 2
}
print(double(6))
// prints: 12
```

参数名也可以交给 `$0`、`$1` 这类位置参数：

```swift
let add: (Int, Int) -> Int = { $0 + $1 }
print(add(2, 3))
// prints: 5
```

单表达式闭包省略 `return`。位置参数适合很短、语义一眼可见的闭包；一旦逻辑超过一两行，还是给参数起名字更负责。

## 14.2 尾随闭包：把代码块放到括号外面

闭包是最后一个参数时，可以写成尾随闭包：

```swift
func operate(_ a: Int, _ b: Int, using operation: (Int, Int) -> Int) -> Int {
    operation(a, b)
}

let result = operate(3, 4) { $0 * $1 }
print(result)
// prints: 12
```

多个尾随闭包可以从 Swift 5.3 开始使用标签：

```swift
func load(success: () -> Void, failure: () -> Void) {
    success()
}

load {
    print("成功")
} failure: {
    print("失败")
}
// prints: 成功
```

如果闭包是唯一参数，通常可以连圆括号一起省略：

```swift
let values = [3, 1, 2].sorted { $0 < $1 }
print(values)
// prints: [1, 2, 3]
```

尾随闭包的完整规则只有四条：必须是最后一个参数、标签一并省略、它是唯一实参时圆括号可整个省略、前面还有别的实参时圆括号必须保留。第 15B.9 节把四条连例子一起列了出来（顺带说清“函数体最后是函数调用能省圆括号”这种说法为什么不对）。

## 14.3 捕获：闭包会记住外面的变量

闭包捕获的是变量本身，而不是当时的值：

```swift
var count = 0
let increment = {
    count += 1
    print(count)
}

increment()
increment()
// prints: 1
// prints: 2
```

多个闭包捕获同一个变量时，它们共享这份存储：

```swift
var total = 0
let addOne = { total += 1 }
let showTotal = { print(total) }

addOne()
addOne()
showTotal()
// prints: 2
```

这很像“函数带着一个小背包”。背包里装的不是快照，而是对原变量的访问通道。

## 14.4 捕获列表：把值固定下来

如果希望闭包拿到定义时的一份副本，可以在开头写捕获列表：

```swift
var score = 10
let snapshot = { [score] in
    print(score)
}

score = 99
snapshot()
// prints: 10
```

捕获列表也常用于给捕获的变量换一个名字：

```swift
let message = "hello"
let printer = { [text = message] in
    print(text.uppercased())
}
printer()
// prints: HELLO
```

对类实例，捕获列表能从一开始就说清是否强引用：

```swift
class Player {
    var name = "Mia"
    func makePrinter() -> () -> Void {
        { [weak self] in
            print(self?.name ?? "已释放")
        }
    }
}

let player = Player()
let printer = player.makePrinter()
printer()
// prints: Mia
```

`weak` 和 `unowned` 的完整讨论在第 28 章。现在先记住：闭包长期保存类实例时，捕获列表是打破循环引用的第一道闸门。

## 14.5 逃逸与非逃逸

函数参数中的闭包默认是非逃逸的：函数返回后，闭包不能继续存活：

```swift
func runNow(_ action: () -> Void) {
    action()
}

runNow { print("立即执行") }
// prints: 立即执行
```

如果闭包要被保存到以后执行，就要标 `@escaping`：

```swift
final class ActionStore {
    var stored: (() -> Void)?

    func store(_ action: @escaping () -> Void) {
        stored = action
    }
}

let store = ActionStore()
store.store { print("以后再执行") }
store.stored?()
// prints: 以后再执行
```

非逃逸闭包让编译器能做性能优化，也减少生命周期问题。`@escaping` 不是装饰品，而是“这段代码可能在函数返回后才跑”的正式声明。

在逃逸闭包里捕获 `inout` 参数会被禁止，因为原变量可能在闭包执行前就离开作用域：

```swift
func makeAdder(_ base: inout Int) -> () -> Void {
    { base += 1 }        // 想把 inout 参数带出函数
}
```

```text
error: escaping closure captures 'inout' parameter 'base'
```

（消息末尾的 `'base'` 就是参数名，你写成别的名字，这里跟着变。）

## 14.6 自动闭包：把表达式变成惰性参数

`@autoclosure` 会把一个普通表达式自动包装成闭包：

```swift
func log(_ message: @autoclosure () -> String) {
    print(message())
}

log("现在才求值")
// prints: 现在才求值
```

最有名的应用是 `??` 和断言函数。下面代码中右侧只有在需要时才求值：

```swift
func expensive() -> Int {
    print("计算很贵")
    return 0
}

let value: Int? = 7
print(value ?? expensive())
// prints: 7
```

`@autoclosure` 让调用处看不到闭包，所以要用在语义非常明显的地方，否则会隐藏执行时机。

## 14.7 `@Sendable` 与并发

并发代码中，跨任务传递的闭包往往需要遵循 `Sendable`：

```swift
@Sendable func work() {
    print("任务")
}

work()
// prints: 任务
```

闭包也可以写成 `@Sendable`。它表示闭包不会偷偷携带不可安全共享的可变状态。完整规则属于第 30–32 章的并发世界；现在只需要知道：`@Sendable` 是给编译器看的“跨隔离域通行证”。

## 14.8 本章小结

| 主题 | 关键结论 |
| --- | --- |
| 闭包表达式 | 用 `in` 分隔参数与主体，可省略类型和 `return` |
| 尾随闭包 | 最后一个闭包参数可移出圆括号 |
| 捕获 | 默认捕获变量本身，多个闭包可共享 |
| 捕获列表 | 可复制值、改名、指定 `weak`/`unowned` |
| 逃逸 | 默认非逃逸，存起来以后用要 `@escaping` |
| 自动闭包 | `@autoclosure` 延迟表达式求值 |
| `@Sendable` | 并发环境中的安全传递标记 |

## 14.9 本章易错点速查

| 易错点 | 正确理解 |
| --- | --- |
| 以为闭包捕获的是值快照 | 默认捕获变量本身，除非使用捕获列表 |
| 在逃逸闭包中忘了 `@escaping` | 保存闭包时必须标注 |
| 用 `[weak self]` 后直接写 `self.name` | `self` 是可选值，需解包或用 `self?.name` |
| 滥用 `$0` | 短闭包可以，复杂逻辑会降低可读性 |
| 把 `@autoclosure` 用在语义不清处 | 调用者可能完全看不出何时求值 |
| 认为 `@Sendable` 会自动解决所有并发安全问题 | 它只表达约束，不自动修复共享状态 |

## 14.10 下章预告

代码会出错，这不是悲观，而是工程事实。下一章我们学习如何把失败变成类型化信息：`throws`、`do-catch`、`defer`、`Result`，以及 Swift 6 的类型化抛出。
