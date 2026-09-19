+++
title = "第19章 属性、方法与下标：把接口设计得顺手"
weight = 190
date = "2026-09-14T22:30:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 第十九章：属性、方法与下标：把接口设计得顺手

> 属性不只是“变量放在类型里”。它可以是算出来的、可以观察变化、可以延迟生成，甚至可以被属性包装器重新定义读写方式。方法和下标则决定使用者如何与你定义的类型互动。接口设计得好，调用处读起来像一句顺滑的话。

## 19.1 存储属性与计算属性

存储属性真的占一块存储；计算属性每次访问时运行代码：

```swift
struct Circle {
    var radius: Double

    var area: Double {
        get { Double.pi * radius * radius }
        set { radius = (newValue / Double.pi).squareRoot() }
    }
}

var circle = Circle(radius: 2)
print(circle.area)
// prints: 12.566370614359172
circle.area = Double.pi * 9
print(circle.radius)
// prints: 3.0
```

`Double.pi` 是标准库替你存好的 π 常量（`Float.pi` 同理），不用自己背小数位。它是**类型属性**的典型例子：写在类型名后面，属于类型本身，而不是某个实例——这一节的后面会讲怎么定义自己的类型属性。

只读计算属性可以省略 `get`：

```swift
var diameter: Double {
    radius * 2
}
```

计算属性不能直接存储值。可读写的计算属性可以临时传入 `inout`，读写会分别调用它的 getter 和 setter；只读计算属性则不行。

上面这句话值得配一个例子，因为它解释了"为什么有的属性不能传 `&`"：

```swift
import Foundation

struct Counter {
    private var _n = 0
    var n: Int {                    // 可读可写：get + set
        get { _n }
        set { _n = newValue }
    }
    var readOnlyN: Int { _n }       // 只读：只有 get
}

func bump(_ value: inout Int) { value += 1 }

var c = Counter()
bump(&c.n)          // ✅ 合法：写入会被送回 setter
print(c.n)
// prints: 1

// bump(&c.readOnlyN)  // ❌ 报错：cannot pass immutable value as inout argument
```

`inout` 的本质是"读出来、改一改、再写回去"。只读属性写不回去，所以编译器直接拦下——这比运行时才崩要好得多。

## 19.2 属性观察器：变化前后插一脚

`willSet` 在赋值前执行，`didSet` 在赋值后执行：

```swift
struct StepCounter {
    var steps = 0 {
        willSet {
            print("将从 \(steps) 变为 \(newValue)")
        }
        didSet {
            print("已经从 \(oldValue) 变为 \(steps)")
        }
    }
}

var counter = StepCounter()
counter.steps = 5
// prints: 将从 0 变为 5
// prints: 已经从 0 变为 5
```

初始化器里首次赋值不会触发观察器。观察器适合记录日志、刷新缓存、通知依赖变化的轻量行为；不要在里面放入昂贵的隐式工作，否则每次赋值都会变慢。

三条容易被忽略的细节：

- **`willSet` 拿不到旧值，`didSet` 拿不到新值。** 想同时看两边，就在 `didSet` 里读一次 `self`（那时已经是新值），旧值留给 `oldValue`。
- **`lazy` 属性也能挂观察器**，只是它的第一次"赋值"发生在初始化那一刻，观察器不触发：

```swift
import Foundation

struct Panel {
    lazy var width: Int = 100 {
        didSet { print("宽度 \(oldValue) → \(width)") }
    }
}

var panel = Panel()
print(panel.width)
// prints: 100
panel.width = 240
// prints: 宽度 100 → 240
```

- **类型属性上的观察器在 Swift 6 里需要隔离。** 可变的 `static var` 属于全局共享可变状态，直接写会报错：

```text
error: static property 'shared' is not concurrency-safe because it is nonisolated global shared mutable state
note: convert 'shared' to a 'let' constant to make 'Sendable' shared state immutable
note: add '@MainActor' to make static property 'shared' part of global actor 'MainActor'
```

  这不是刁难，而是把第 30–32 章的并发规则提前搬到了门口：要么让它不可变（`static let`），要么明确它属于哪个隔离域：

```swift
import Foundation

@MainActor
struct SettingsStore {
    static var shared = 0 {
        didSet { print("shared: \(oldValue) → \(shared)") }
    }
}
```

## 19.3 `lazy`：第一次需要时才生成

有些属性算起来不便宜，而你可能一次都用不上。`lazy` 让它在第一次被读取时才动手：

```swift
struct Report {
    var raw: String

    lazy var wordCount: Int = {
        print("计算一次")
        return raw.split(separator: " ").count
    }()
}

var report = Report(raw: "swift is fun")
print(report.wordCount)
// prints: 计算一次
// prints: 3
print(report.wordCount)
// prints: 3
```

`lazy` 只能用于 `var`。第一次读取后结果被保存，后续不会重复计算。适合昂贵且不一定用到的派生值，但要注意它在并发环境中访问时的线程安全问题。

## 19.4 类型属性：属于类型本身

`static` 表示属性属于类型，而不是某个实例：

```swift
struct AppInfo {
    static let name = "Prgms"
}
print(AppInfo.name)
// prints: Prgms
```

类中如果希望子类可以重写类型属性，使用 `class`：

```swift
class Base {
    class var label: String { "base" }
}

class Child: Base {
    override class var label: String { "child" }
}
print(Base.label, Child.label)
// prints: base child
```

结构体不能使用 `class` 关键字。

顺带把"类型成员"这一族凑齐，它们的关系可以用一张表记住：

| 写法 | 属于谁 | 能否被子类重写 |
| --- | --- | --- |
| `static let x` | 类型 | 不能 |
| `static var x` | 类型（Swift 6 需隔离） | 不能 |
| `class var x { }` | 类型 | 能（类专属） |
| `final class var x { }` | 类型 | 不能 |
| 普通 `var x` | 实例 | 能 |

⚠️ `class` 这个关键字在这里只表示"可以在子类里 `override`"，和面向对象里的"类"没关系。结构体、枚举都不支持它，因为值类型没有继承。

## 19.5 实例方法、类型方法与 `self`

方法是挂在实例上的函数，`self` 则是“当前这个实例”的正式名字。

```swift
struct Temperature {
    var celsius: Double

    func inFahrenheit() -> Double {
        celsius * 9 / 5 + 32
    }

    static func freezingPoint() -> Temperature {
        Temperature(celsius: 0)
    }
}
print(Temperature.freezingPoint().inFahrenheit())
// prints: 32.0
```

`self` 指当前实例。在值类型 `mutating` 方法里，`self` 可以被整体替换：

```swift
struct Name {
    var first: String

    mutating func uppercase() {
        self = Name(first: first.uppercased())
    }
}
```

这不会造成递归调用，因为右边先构造新值，再赋给 `self`。

### 方法签名也是接口的一部分

参数标签、默认值和返回值处理方式，直接决定调用处读起来顺不顺：

```swift
import Foundation

struct Wallet {
    private(set) var balance = 0

    @discardableResult
    mutating func deposit(_ amount: Int, note: String = "") -> Int {
        balance += amount
        return balance
    }
}

var wallet = Wallet()
wallet.deposit(100)                     // 忽略返回值，也不报"未使用结果"
print(wallet.deposit(50, note: "红包"))
// prints: 150
```

- `_ amount` 去掉了参数标签，调用处写 `deposit(100)` 而不是 `deposit(amount: 100)`；数值型参数通常这么写更自然。
- `note: String = ""` 让可选信息不必每次都填。
- `@discardableResult` 说明"返回值只是个附加信息，可以不要"；没有它，编译器会对忽略返回值发出警告。**这个标注其实是一种文档**：它告诉使用者"放心忽略"。

## 19.6 下标：用方括号访问自定义容器

下标让你给自己的类型配上 `[]` 语法，像访问数组那样访问它：

```swift
struct Matrix {
    let rows: Int
    let columns: Int
    private var storage: [Int]

    init(rows: Int, columns: Int) {
        self.rows = rows
        self.columns = columns
        self.storage = Array(repeating: 0, count: rows * columns)
    }

    subscript(row: Int, column: Int) -> Int {
        get { storage[row * columns + column] }
        set { storage[row * columns + column] = newValue }
    }
}

var matrix = Matrix(rows: 2, columns: 2)
matrix[1, 1] = 42
print(matrix[1, 1])
// prints: 42
```

下标可以有多个参数，也可以只读：

```swift
struct Bag<Element> {
    private var items: [Element] = []

    mutating func append(_ item: Element) { items.append(item) }

    subscript(index: Int) -> Element? {
        guard items.indices.contains(index) else { return nil }
        return items[index]
    }
}
```

如果下标可以修改，调用位置的实例必须是 `var`；只读下标则可以被 `let` 实例读取。

## 19.7 属性包装器：把读写规则装进类型

属性包装器用一个类型包住属性的读写逻辑：

```swift
@propertyWrapper
struct Clamped {
    var value: Int
    let range: ClosedRange<Int>

    init(wrappedValue: Int, _ range: ClosedRange<Int>) {
        self.range = range
        self.value = min(max(wrappedValue, range.lowerBound), range.upperBound)
    }

    var wrappedValue: Int {
        get { value }
        set { value = min(max(newValue, range.lowerBound), range.upperBound) }
    }
}

struct Player {
    @Clamped(0...100) var health = 80
}

var player = Player()
player.health = 150
print(player.health)
// prints: 100
player.health = -5
print(player.health)
// prints: 0
```

包装器可以额外暴露 `projectedValue`，通常写作 `$property`：

```swift
@propertyWrapper
struct Logged<Value> {
    private var value: Value

    init(wrappedValue: Value) { value = wrappedValue }

    var wrappedValue: Value {
        get { value }
        set {
            print("写入 \(newValue)")
            value = newValue
        }
    }

    var projectedValue: String { "当前值：\(value)" }
}

struct Settings {
    @Logged var theme = "light"
}

var settings = Settings()
settings.theme = "dark"
// prints: 写入 dark
print(settings.$theme)
// prints: 当前值：dark
```

SwiftUI 的 `@State`、`@Binding` 等机制都建立在属性包装器之上。初学阶段不必手写复杂包装器，但要能读懂 `$` 和 `wrappedValue` 的关系。

第 15B.6 节把属性包装器展开的 `_property` / `property` / `$property` 三个成员讲透了，还给了完整的自定义包装器例子，值得回头对读一遍——19.7 这里是"够用版"，那里是"看穿版"。

## 19.8 本章小结

| 主题 | 关键结论 |
| --- | --- |
| 计算属性 | 每次读取运行代码，可以有 getter/setter |
| 属性观察器 | `willSet` 看新值，`didSet` 可看旧值 |
| `lazy` | 第一次访问时初始化，只能用于 `var` |
| 类型属性 | `static` 属于类型，类中可用 `class` 支持重写 |
| 方法 | 实例方法默认不能改值类型；`mutating` 可以 |
| 下标 | 自定义方括号访问，可多参数、可读写 |
| 属性包装器 | 用类型封装属性读写逻辑，`$` 访问投影值 |
| 参数标签与默认值 | `_ label`、默认参数决定调用处的可读性 |
| `@discardableResult` | 明确告诉使用者"返回值可以忽略" |

## 19.9 本章易错点速查

| 易错点 | 正确理解 |
| --- | --- |
| 把计算属性当存储属性 | 它不占存储，每次访问都会执行 |
| 在初始化器里期待观察器触发 | 初始化阶段首次赋值不触发 |
| 在 `lazy` 属性里访问未初始化的 `self` | 可能形成复杂依赖，要保持简单 |
| 以为 `static` 每个实例一份 | 类型属性全局一份 |
| 下标越界不处理 | 应主动检查或明确文档化崩溃约束 |
| 看到 `$` 就以为是语法糖 | 它通常来自属性包装器的 `projectedValue` |
| 用只读计算属性当 `inout` | 写不回去；只有 get+set 的属性才能传 `&` |
| 以为可变 `static var` 随便写 | Swift 6 下报并发安全错误；用 `static let` 或加隔离 |
| 在初始化器里等 `didSet` 触发 | 首次赋值不触发观察器；`lazy` 的首次取值同样不触发 |

## 19.10 下章预告

对象如何诞生、如何确保创建到一半时仍然合法、如何优雅地失败、又如何释放？下一章专讲初始化与反初始化。它是类与结构体设计中规则最多、也最能体现 Swift 严谨性的部分。
