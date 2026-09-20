+++
title = "12 语法糖与简写对照"
linkTitle = "12 语法糖"
weight = 120
date = "2026-09-16T11:00:00+08:00"
type = "docs"
description = "同一段代码的完整写法与简写并排看：闭包、可选值、属性、初始化器、协议与 DSL"
isCJKLanguage = true
draft = false
+++

# 12 语法糖与简写对照

Swift 的简写规则很多，而且**大都只能省、不能加**——你要读懂别人写的简写，也要知道自己的简写能被还原成什么。这一页全部用"完整写法 / 简写"并排的方式呈现。

## 闭包的四个阶段

{{< tabpane text=true persist=disabled >}}

{{% tab header="完整写法" %}}

```swift
let squares = [1, 2, 3].map { (n: Int) -> Int in
    return n * n
}
print(squares)
// prints: [1, 4, 9]
```

{{% /tab %}}

{{% tab header="省类型与 return" %}}

```swift
let squares = [1, 2, 3].map { n in
    n * n
}
print(squares)
// prints: [1, 4, 9]
```

单表达式闭包自动返回，不需要 `return`。

{{% /tab %}}

{{% tab header="$0 简写" %}}

```swift
let squares = [1, 2, 3].map { $0 * $0 }
print(squares)
// prints: [1, 4, 9]
```

{{% /tab %}}

{{% tab header="尾随闭包" %}}

```swift
func retry(times: Int, task: () -> Void) {
    for _ in 0..<times { task() }
}

retry(times: 2) { print("尝试一次") }
// prints: 尝试一次
//         尝试一次

// 等价于
retry(times: 2, task: { print("尝试一次") })
```

{{% /tab %}}

{{% tab header="多尾随闭包" %}}

```swift
func configure(setup: () -> Void, completion: () -> Void) {
    setup()
    completion()
}

configure {
    print("setup")
} completion: {
    print("completion")
}
// prints: setup
//         completion
```

第一个闭包不带标签，后面的带。SwiftUI 里的 `Button { } label: { }`、UIKit 里的 `UIView.animate(withDuration:) { } completion: { }` 都靠它。

{{% /tab %}}

{{% tab header="运算符就是函数" %}}

```swift
print([1, 2, 3].reduce(0, +))
// prints: 6
print([3, 1, 2].sorted(by: >))
// prints: [3, 2, 1]
print([1, 2, 3].map(-))
// prints: [-1, -2, -3]
```

运算符本身就是函数，可以当参数传。

{{% /tab %}}

{{< /tabpane >}}

## 属性与初始化器

{{< tabpane text=true persist=disabled >}}

{{% tab header="计算属性的 get/set" %}}

```swift
struct Temperature {
    var celsius: Double
    var fahrenheit: Double {
        get { celsius * 9 / 5 + 32 }
        set { celsius = (newValue - 32) * 5 / 9 }
    }
}
```

只读时可以把 `get` 和括号全部省掉：

```swift
struct Temperature {
    var celsius: Double
    var fahrenheit: Double { celsius * 9 / 5 + 32 }
}
```

{{% /tab %}}

{{% tab header="属性观察器" %}}

```swift
var score = 0 {
    willSet(newValue) { print("变成 \(newValue)") }
    didSet(oldValue) { print("从 \(oldValue) 变成 \(score)") }
}
```

参数名有默认值，绝大多数时候直接省：

```swift
var score = 0 {
    willSet { print("变成 \(newValue)") }
    didSet { print("从 \(oldValue) 变成 \(score)") }
}
```

{{% /tab %}}

{{% tab header="成员逐一初始化器" %}}

```swift
struct Point { var x: Double; var y: Double }

// 一个 init 都不写，编译器白送一个"成员逐一初始化器"
print(Point(x: 1, y: 2))
// prints: Point(x: 1.0, y: 2.0)

// 想再加一个入口，就放进 extension —— 成员逐一初始化器依然在
extension Point {
    init(square side: Double) {
        self.init(x: side, y: side)
    }
}

print(Point(square: 3))
// prints: Point(x: 3.0, y: 3.0)
```

⚠️ 但**同签名**的手写初始化器往哪塞都不行。`extension Point { init(x: Double, y: Double) }` 会直接撞上编译器合成的那份，报 `invalid redeclaration of synthesized memberwise 'init(x:y:)'`——它不会"顶掉"合成版本，只是纯粹报错。

💭 一句话记住：自定义初始化器写在**类型声明体内**，成员逐一初始化器就不再生成了；写在 **`extension`** 里，它就还在，前提是签名别撞车。

{{% /tab %}}

{{% tab header=".init 与默认参数" %}}

```swift
struct Config { var name = "默认"; var retries = 3 }

let a = Config()
let b = Config(name: "自定义")
let c: Config = .init(retries: 5)

print(a.name, b.name, c.retries)
// prints: 默认 自定义 5
```

类型已经能从上下文推出来时，`.init(...)` 比 `Config(...)` 短一截。

{{% /tab %}}

{{< /tabpane >}}

## 类型、枚举与分支

{{< tabpane text=true persist=disabled >}}

{{% tab header="静态成员查找" %}}

```swift
enum Direction { case north, south }

let a = Direction.north      // 完整写法
let b: Direction = .north    // 类型已知时省略类型名
```

⚠️ 这叫**前导点**（隐式成员表达式），前提是上下文类型已经确定。少了上下文就没法省：`let b = .north` 报的是 `reference to member 'north' cannot be resolved without a contextual type`；如果这个点号落在元组里（`let t = (1, .north)`），报的则是 `cannot infer contextual base in reference to member 'north'`——同一件事的两种说法。枚举 `case`、静态属性、静态方法、`.init` 全都适用，完整规律和几个坑见 [06 可选值]({{< relref "06-Optionals.md" >}})。

{{% /tab %}}

{{% tab header="类型推断" %}}

```swift
let a: [String: Int] = ["x": 1]
let b = ["x": 1]                          // 推断为 [String: Int]
let c: [Any] = [1, "two"]
let d: [Int] = []                         // 空字面量必须写类型
```

⚠️ 推断不是万能的：`let e = []` 直接报错，因为编译器没有任何线索。

{{% /tab %}}

{{% tab header="if / switch 表达式 🆕" %}}

```swift
let score = 87

// 老写法
let letter1: String
if score >= 90 { letter1 = "A" } else { letter1 = "B" }

// 5.9 起
let letter2 = if score >= 90 { "A" } else { "B" }

let grade = switch score {
case 90...:   "A"
case 80..<90: "B"
default:      "C"
}

print(letter1, letter2, grade)
// prints: B B B
```

{{% /tab %}}

{{% tab header="枚举的隐式原始值" %}}

```swift
enum Weekday: Int { case mon = 1, tue, wed }    // tue = 2, wed = 3
enum Suit: String { case hearts, spades }       // "hearts", "spades"

print(Weekday.wed.rawValue, Suit.spades.rawValue)
// prints: 3 spades
```

整数原始值只写第一个，后面的自动递增；字符串原始值则默认等于 case 名。

{{% /tab %}}

{{% tab header="可选模式 ?" %}}

```swift
let value: Int? = 7

switch value {
case .some(let v): print(v)     // 完整写法
case .none: break
}

switch value {
case let v?: print(v)           // 后缀 ? 简写
case nil: break
}

if let v = value { print(v) }
```

三种写法等价。`case let v?` 在读别人的代码时会突然出现，认得就行。

{{% /tab %}}

{{< /tabpane >}}

## 可选值：五种写法做同一件事

💭 这里比的是"同一个解包需求怎么写得更短"。`let` 还能跟在 `while`、`case`、`catch` 后面，那份完整清单在 [02 语言主干]({{< relref "02-Language-Basics.md" >}})。

{{< tabpane text=true persist=disabled >}}

{{% tab header="if let + 解包" %}}

```swift
let raw: String? = "42"

if let text = raw, let value = Int(text) {
    print(value)
} else {
    print("没有数字")
}
// prints: 42
```

{{% /tab %}}

{{% tab header="5.7 起的简写" %}}

```swift
let raw: String? = "42"

if let raw, let value = Int(raw) {
    print(value)
}
// prints: 42
```

变量名相同时，右边可以直接省略。`guard` 同理：

```swift
func handle(_ text: String?) {
    guard let text else { return }
    print(text)
}
handle("ok")
// prints: ok
```

{{% /tab %}}

{{% tab header="?? 兜底" %}}

```swift
let raw: String? = nil
print(Int(raw ?? "") ?? 0)
// prints: 0
```

`??` 的链式兜底能让"多层可选值"变成一行。

{{% /tab %}}

{{% tab header="可选链" %}}

```swift
let dict = ["key": "value"]
print(dict["missing"]?.count ?? -1)
// prints: -1
print(dict["key"]?.count ?? -1)
// prints: 5
```

{{% /tab %}}

{{% tab header="map 处理" %}}

```swift
let raw: String? = "42"
let doubled: Int? = raw.map { Int($0) ?? 0 }.map { $0 * 2 }
print(doubled ?? -1)
// prints: 84

print([1, nil, 3].compactMap { $0 })
// prints: [1, 3]
```

可选值也有 `map`，写法比 `if let` 更紧凑，代价是可读性下降。

{{% /tab %}}

{{< /tabpane >}}

## 协议与自动合成

{{< tabpane text=true persist=disabled >}}

{{% tab header="手写实现" %}}

```swift
struct Money: Equatable, Hashable {
    var amount: Int
    var currency: String

    static func == (lhs: Money, rhs: Money) -> Bool {
        lhs.amount == rhs.amount && lhs.currency == rhs.currency
    }

    func hash(into hasher: inout Hasher) {
        hasher.combine(amount)
        hasher.combine(currency)
    }
}
```

{{% /tab %}}

{{% tab header="自动合成" %}}

```swift
struct Money: Equatable, Hashable {
    var amount: Int
    var currency: String
}

print(Money(amount: 1, currency: "CNY") == Money(amount: 1, currency: "CNY"))
// prints: true
```

只要所有存储属性都满足条件，`Equatable`、`Hashable`、`Codable` 编译器都会替你补上。

⚠️ 但 `CaseIterable` **不在这个名单里**：它是"枚举专用"的，只有**没有关联值的枚举**才能合成 `allCases`。结构体哪怕全是简单属性也不行：

```swift
enum Suit: CaseIterable { case hearts, spades }
print(Suit.allCases.count)      // prints: 2      ✅

struct Bad: CaseIterable { var a: Int }
// 🛑 error: type 'Bad' does not conform to protocol 'CaseIterable'
//    note: protocol requires property 'allCases'
```

{{% /tab %}}

{{% tab header="协议默认实现" %}}

```swift
protocol Greeter { var name: String { get } }

extension Greeter {
    func greet() -> String { "你好，\(name)" }
}

struct Guest: Greeter { let name: String }
struct Robot: Greeter {
    let name: String
    func greet() -> String { "\(name) 上线" }
}

print(Guest(name: "小明").greet(), Robot(name: "R2").greet())
// prints: 你好，小明 R2 上线
```

⚠️ 想让默认实现在 `any` 上也生效，必须把方法同时写进协议**要求**里，否则会被静态派发。细节见 [08 协议与泛型]({{< relref "08-Protocols-and-Generics.md" >}})。

{{% /tab %}}

{{% tab header="条件遵循" %}}

```swift
struct Wrapper<T> { var value: T }
extension Wrapper: Equatable where T: Equatable {}

print(Wrapper(value: "a") == Wrapper(value: "a"))
// prints: true
```

一行声明让泛型类型"在条件满足时才具备某项能力"，标准库的 `Array`、`Optional` 全靠这个机制。

{{% /tab %}}

{{< /tabpane >}}

### 字面量协议：让自己的类型"长得像内建类型"

`let x: MyType = "一句话"` 这种写法不是内建类型专属。只要遵守对应的 `ExpressibleBy...Literal` 协议，你的类型也能用字面量初始化：

| 协议 | 写法 | 标准库里的例子 |
| --- | --- | --- |
| `ExpressibleByIntegerLiteral` | `let x: T = 42` | `Int`、`Double`、`Decimal` |
| `ExpressibleByFloatLiteral` | `let x: T = 3.14` | `Double`、`Float` |
| `ExpressibleByStringLiteral` | `let x: T = "hi"` | `String`、`StaticString`（⚠️ **不是 `Character`**） |
| `ExpressibleByBooleanLiteral` | `let x: T = true` | `Bool` |
| `ExpressibleByArrayLiteral` | `let x: T = [1, 2]` | `Array`、`Set` |
| `ExpressibleByDictionaryLiteral` | `let x: T = ["a": 1]` | `Dictionary` |
| `ExpressibleByNilLiteral` | `let x: T = nil` | `Optional` |
| `ExpressibleByExtendedGraphemeClusterLiteral` | `let x: T = "A"` | `Character`（**它在这里，不在 `ExpressibleByStringLiteral` 里**） |

```swift
struct Meters: ExpressibleByStringLiteral {
    let text: String
    init(stringLiteral value: String) { text = value }
}

struct Point: ExpressibleByArrayLiteral {
    let coords: [Int]
    init(arrayLiteral elements: Int...) { coords = elements }
}

let distance: Meters = "一小时的路程"
print(distance.text)
// prints: 一小时的路程

print(Point(arrayLiteral: 1, 2, 3).coords)
// prints: [1, 2, 3]
```

⚠️ 字面量协议会**放宽**类型检查：写 `let x: MyType = "随便什么字符串"` 都可能编过，因为编译器不知道你的语义。给单位、货币、ID 这类类型加它要谨慎，别把编译期检查换成运行期惊喜。

## DSL 视角：结果构建器

SwiftUI 里那些"看起来不像 Swift"的代码，靠的就是结果构建器 + 尾随闭包：

```swift
// 概念示意，不是真实 SwiftUI 代码
VStack {
    Text("标题")
    if showDetail {
        Text("详情")
    }
    ForEach(items) { item in
        Text(item.name)
    }
}
```

它是三层语法糖叠起来的结果：

| 层次 | 机制 |
| --- | --- |
| 1 | 尾随闭包：`VStack { ... }` 而不是 `VStack(content: { ... })` |
| 2 | 结果构建器：闭包里连写多行，编译器把它们收集成数组 |
| 3 | 类型推断：`.font(.title)` 这样的静态成员查找省掉了类型名 |

## 语法糖大表

一句话版本，方便扫读：

| 完整写法 | 简写 | 备注 |
| --- | --- | --- |
| `let x: Int = 1` | `let x = 1` | 类型推断 |
| `Direction.north` | `.north` | 上下文已知类型时 |
| `Config(x: 1)` | `.init(x: 1)` | 同上 |
| `{ return x }` | `{ x }` | 单表达式隐式返回 |
| `func f() -> Int { return 1 }` | `func f() -> Int { 1 }` | 同上 |
| `var x: Int { get { 1 } }` | `var x: Int { 1 }` | 只读计算属性 |
| `if let x = x` | `if let x` | Swift 5.7+ |
| `guard let x = x else` | `guard let x else` | 同上 |
| `array.map { $0 * 2 }` | 同左 | 闭包参数简写 |
| `reduce(0, { $0 + $1 })` | `reduce(0) { $0 + $1 }` | 尾随闭包 |
| `reduce(0, +)` | 同左 | 运算符当函数 |
| `x.map { $0 }` | `x.map(\.self)` | 少见但合法 🝖 |
| `struct E: Equatable { static func == ... }` | `struct E: Equatable {}` | 自动合成 |
| `for x in a { }` | `a.forEach { x in }` | 不能 `break`，慎用 |
| `switch` + `return` 每个分支 | `let x = switch ...` | Swift 5.9+ |
| `#keyPath(User.name)` | `\User.name` | 前者只在 ObjC 互操作时用 |
| `Optional.some(1)` | `.some(1)` / `1` | 上下文已知时 |

## 常见误传（Swift 里**没有**这些简写）

网上流传的一些"Swift 语法糖"，其实并不存在。别在代码里试：

| 传说 | 真相 |
| --- | --- |
| "函数体最后一句是函数调用可以省圆括号" | ❌ Swift 没有这条规则。只有尾随闭包可以挪出去 |
| "字符串可以用单引号" | ❌ `'a'` 不是合法的 Swift |
| "可选值能自动参与算术" | ❌ 必须先解包 |
| "`switch` 会像 C 一样穿透" | ❌ 要穿透得显式写 `fallthrough` |
| "整数和浮点能隐式互转" | ❌ 必须 `Double(i)` |
| "可以用 `+` 拼接字符串和数字" | ❌ 用插值 `"\(n)"` |
| "`if 1 { }` 能当条件" | ❌ 没有真值转换，必须写 `if x > 0` |
| "分号可有可无，随便加" | ⚠️ 合法但社区风格一律不加 |
| "尾随闭包能用在 if 条件里" | ⚠️ 能编过，但编译器分不清花括号是参数还是语句体，会给一条警告。写进括号最省事，见 [05 函数与闭包]({{< relref "05-Functions-and-Closures.md" >}}) |
| "Swift 有 `goto`" | ❌ 没有，`goto` 连关键字都不是。用带标签的 `break` / `continue`，或写 `while` + `switch` 的状态循环，见 [02 语言主干]({{< relref "02-Language-Basics.md" >}}) |

## 使用建议

| 简写 | 用不用 |
| --- | --- |
| 类型推断 | 🔥 用，但如果影响可读性就写全 |
| 单表达式隐式返回 | 🔥 用 |
| `$0` | 🔥 单层、参数少于 3 个时用 |
| 尾随闭包 | 🔥 用 |
| `.init(...)` | 类型名很长时用 |
| `if let x` 简写 | 🔥 用 |
| `case let v?` | 能看懂就行，写不写随你 |
| `map(-)` 这类 | 🚧 别人不一定一眼看懂，团队风格优先 |
| 自定义运算符 | 🛑 除非数学库，别写 |
