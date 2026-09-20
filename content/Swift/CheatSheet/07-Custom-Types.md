+++
title = "07 自定义类型"
linkTitle = "07 自定义类型"
weight = 70
date = "2026-09-16T11:00:00+08:00"
type = "docs"
description = "结构体、类、枚举、actor 的选择，初始化器家族，属性与下标的全部形态"
isCJKLanguage = true
draft = false
+++

# 07 自定义类型

## 四种类型，先看怎么选

| | `struct` | `class` | `enum` | `actor` |
| --- | --- | --- | --- | --- |
| 语义 | 值 | 引用 | 值 | 引用 |
| 继承 | ❌ | ✅ | ❌ | ❌ |
| 能表示"多选一" | ❌ | ❌ | ✅ | ❌ |
| 并发安全 | 天然（值不共享） | 需要自己保证 | 天然 | 由 actor 隔离保证 |
| 定义 `deinit` | ❌ | ✅ | ❌ | ✅ |
| 默认选择 | 🔥 首选 | 需要共享状态时才用 | 需要穷尽分支时用 | 需要可变共享状态时 |

💭 这是 Swift 里最重要的一张表。默认写 `struct`；需要继承或身份标识（两个对象是不是同一个）时才换 `class`；需要"这些情况互斥"时用 `enum`；需要并发下安全地共享可变状态时用 `actor`。

同一个"计数器"，四种类型各写一遍（`enum` 那栏换成状态机，毕竟枚举天生就不是用来存数字的）：

{{< tabpane text=true persist=disabled >}}

{{% tab header="struct（值语义）" %}}

```swift
struct Counter {
    private(set) var value = 0
    mutating func increment() { value += 1 }
}

var a = Counter()
a.increment()
var b = a          // 复制一份，与 a 无关
b.increment()
print(a.value, b.value)
// prints: 1 2
```

赋值即复制。你改 `b`，`a` 毫发无伤——这是最不容易出错的默认行为。

{{% /tab %}}

{{% tab header="class（引用语义）" %}}

```swift
final class Counter {
    private(set) var value = 0
    func increment() { value += 1 }
}

let a = Counter()
a.increment()
let b = a          // 指向同一个对象
b.increment()
print(a.value, b.value)
// prints: 2 2
```

`a` 和 `b` 是同一个东西的两个名字。需要共享状态时这正是你要的，不需要时这正是 bug。

{{% /tab %}}

{{% tab header="enum（穷尽分支）" %}}

```swift
enum State {
    case idle
    case loading(progress: Double)
    case failed(message: String)
    case done
}

let s = State.loading(progress: 0.5)
switch s {
case .idle:              print("空闲")
case .loading(let p):    print("加载中 \(p * 100)%")
case .failed(let msg):   print("失败：\(msg)")
case .done:              print("完成")
}
// prints: 加载中 50.0%
```

`enum` 的价值在 `switch` 的强制性：将来新增一个 case，所有没处理它的地方都会编译报错。这是"状态机"最便宜的正确性保证。

{{% /tab %}}

{{% tab header="actor（并发安全）" %}}

```swift
actor Counter {
    private(set) var value = 0
    func increment() { value += 1 }
    func snapshot() -> Int { value }
}

let c = Counter()
await c.increment()
await c.increment()
print(await c.snapshot())
// prints: 2
```

actor 像一个自带队列的对象：外部访问它的可变状态必须 `await`，编译器保证同一时刻只有一个任务在改它。见 [09 错误处理与并发]({{< relref "09-Error-Handling-and-Concurrency.md" >}})。

{{% /tab %}}

{{< /tabpane >}}

## 结构体

```swift
struct Point {
    var x: Double
    var y: Double

    var length: Double { (x * x + y * y).squareRoot() }   // 计算属性

    mutating func moveBy(dx: Double, dy: Double) {        // 改自己的方法要 mutating
        x += dx
        y += dy
    }
}

var p = Point(x: 3, y: 4)     // 编译器自动生成的成员逐一初始化器
print(p.length)
// prints: 5.0
p.moveBy(dx: 1, dy: -4)
print(p.x, p.y)
// prints: 4.0 0.0
```

规则速记：

| 规则 | 说明 |
| --- | --- |
| 自动生成成员初始化器 | 只要你不写自定义 `init`，编译器就送一个 |
| 一旦手写 `init` | 自动生成的那个**消失**，想保留就写进 `extension` |
| 改属性的方法要 `mutating` | 否则编译器报"不能修改自身" |
| `let` 实例不能调用 `mutating` | 值类型里的 `let` 是彻底的只读 |
| 默认合成 `Equatable` / `Hashable` | 所有成员都实现时，编译器自动合成 🔥 |

## 类

```swift
class Vehicle {
    let wheels: Int
    var summary: String { "\(type(of: self))，\(wheels) 个轮子" }

    init(wheels: Int) { self.wheels = wheels }      // 指定初始化器
    convenience init() { self.init(wheels: 4) }     // 便利初始化器，必须转调 self.init
    deinit { print("释放了 \(wheels) 轮车") }
}

final class Car: Vehicle {
    var brand: String

    init(brand: String) {
        self.brand = brand          // 先初始化自己的属性
        super.init(wheels: 4)       // 再调用父类初始化器
    }

    override var summary: String { super.summary + "，品牌 \(brand)" }
}

print(Car(brand: "Tesla").summary)
// prints: Car，4 个轮子，品牌 Tesla
```

### 继承：能覆写什么，必须写什么

```swift
class Vehicle {
    var wheels: Int
    var summary: String { "\(type(of: self)) / \(wheels) 个轮子" }
    init(wheels: Int) { self.wheels = wheels }
    func describe() -> String { "有 \(wheels) 个轮子" }
}

final class Bike: Vehicle {
    var brand: String

    init(brand: String) {
        self.brand = brand          // 先把子类自己的属性初始化完
        super.init(wheels: 2)       // 再调父类的指定初始化器
    }

    override func describe() -> String { super.describe() + "，品牌 \(brand)" }
    override var summary: String { super.summary + " b" }
}

let v: Vehicle = Bike(brand: "G")
print(v.describe())
// prints: 有 2 个轮子，品牌 G
print(v.summary)
// prints: Bike / 2 个轮子 b
```

🔥 `type(of: self)` 在父类的计算属性里也能给出子类的名字，这是多态最直观的体现：`self` 的静态类型是 `Vehicle`，运行期类型是 `Bike`。

| 父类的成员 | 子类怎么写 | 写错时报什么 |
| --- | --- | --- |
| 方法、计算属性 | 加 `override` | `overriding declaration requires an 'override' keyword` |
| 签名相同的指定初始化器 | 加 `override` | 同上（初始化器也算覆写） |
| `final` 方法、`final` 类型 | 不能覆写 / 不能继承 | `instance method overrides a 'final' instance method` |
| `static` 成员 | 不能覆写 | `cannot override static method` |
| `let` 存储属性 | 不能覆写 | `cannot override immutable 'let' property 'n' with the getter of a 'var'` |
| 存储属性（`var`） | 有三条路：加观察器、换成计算属性、或两者都来 | `override var value: Int { didSet { } }`、`override var value: Int { get { 5 } set { } }` 都合法；只写 `get` 会报 `cannot override mutable property with read-only property 'x'` |

初始化器的继承只有两条规则，但很容易记反：

```swift
class A {
    var name: String
    init(name: String) { self.name = name }
    convenience init() { self.init(name: "默认") }
}

class B: A {}          // 一个初始化器都不写 → 父类的初始化器全盘继承

print(B().name, B(name: "x").name)
// prints: 默认 x
```

```swift
class C: A {
    override init(name: String) { super.init(name: name) }   // 覆写了全部指定初始化器
}
print(C().name)
// prints: 默认     便利初始化器照样继承
```

🔥 规则要分两句话说：

- **指定初始化器**：子类不写任何自己的指定初始化器时，父类的全部继承；写了就只继承自己覆写的那些。
- **便利初始化器**：只要子类把父类的**所有**指定初始化器都实现了（覆写也算实现），父类的便利初始化器就继续继承；落下一个，这条链就断。

所以上面 `B` 什么都没写，白拿两个入口；`C` 用 `override` 补齐了唯一的指定初始化器 `init(name:)`，于是 `C()` 也还在。反过来，如果 `A` 有两个指定初始化器而 `C` 只覆写了一个，`C()` 就会报 `missing argument for parameter ...`——它已经没有 `init()` 这个入口了。想在保留老入口的同时加新入口，把新初始化器写进 `extension`（见 [12 语法糖]({{< relref "12-Syntax-Sugar.md" >}}) 里的成员逐一初始化器）。

给继承来的存储属性加观察器时，父子两边的观察器都会跑：

```swift
class Base { var value = 0 { didSet { print("Base 看到 \(oldValue) -> \(value)") } } }
class Sub: Base { override var value: Int { didSet { print("Sub 追加处理") } } }

let s = Sub()
s.value = 5
// prints: Base 看到 0 -> 5
//         Sub 追加处理
```

💭 继承在 Swift 里的地位比在 C++/Java 里低得多：能用协议 + 组合解决的事就别开继承。真开了，就给不打算被继承的类加 `final`——它既是语义声明，也让编译器省掉一层动态派发。

### 初始化器家族

| 种类 | 写法 | 规则 |
| --- | --- | --- |
| 指定初始化器 | `init(...)` | 完整的初始化路径，父类的指定初始化器必须被调用 |
| 便利初始化器 | `convenience init(...)` | 必须最终转调本类的指定初始化器 |
| 可失败初始化器 | `init?(...)` / `init!(...)` | 返回值会变成可选值 |
| 必需初始化器 | `required init(...)` | 子类必须实现 |
| 继承来的初始化器 | 见上文"初始化器的继承" | 指定初始化器：不写自己的才全盘继承；便利初始化器：把父类的指定初始化器全实现了才继承 |
| `deinit` | 只有类与 actor 有 | 对象销毁前调用，不能直接调用 |

```swift
struct Temperature {
    static let absoluteZero = -273.15
    private(set) var celsius: Double

    init(celsius: Double) { self.celsius = max(celsius, Self.absoluteZero) }
    init(fahrenheit: Double) { self.init(celsius: (fahrenheit - 32) * 5 / 9) }
    init?(from text: String) {
        guard let value = Double(text) else { return nil }
        self.init(celsius: value)
    }

    var fahrenheit: Double { celsius * 9 / 5 + 32 }
}

print(Temperature(fahrenheit: 212).celsius)
// prints: 100.0
print(Temperature(from: "25")!.fahrenheit)
// prints: 77.0
```

🔥 多个初始化器用**同一个**指定初始化器收口，是保证"不变量只在一处维护"的关键手法。上面所有初始化器最后都走 `init(celsius:)`，所以温度下界的修正逻辑只写了一遍。

## 枚举

```swift
enum Direction: String, CaseIterable {
    case north = "N"
    case south = "S"

    var opposite: Direction { self == .north ? .south : .north }
}

print(Direction.allCases.map(\.rawValue))
// prints: ["N", "S"]
print(Direction(rawValue: "N")?.opposite == .south)
// prints: true
```

| 能力 | 写法 |
| --- | --- |
| 原始值 | `enum E: String { case a = "A" }`，`E(rawValue:)` 返回可选值 |
| 关联值 | `case loading(progress: Double)` 🔥 |
| 遍历全部 | 遵守 `CaseIterable`，用 `E.allCases` |
| 递归枚举 | `indirect enum Node { case leaf(Int); case branch(Node, Node) }` |
| 模式匹配 | `if case .loading(let p) = state { }` |
| 合成 `Equatable` | 有关联值时也能自动合成 |
| 稳定 ABI | `@frozen enum` 表示不会再新增 case 🝖 |

```swift
enum Barcode {
    case upc(Int, Int, Int, Int)
    case qrCode(String)
}

let b = Barcode.qrCode("ABCD")
switch b {
case .upc(let a, let b, let c, let d):
    print(a, b, c, d)
case .qrCode(let s):
    print("qr:", s)
}
// prints: qr: ABCD
```

⚠️ 有关联值的枚举**不能**随便用 `==` 比较：只有当所有关联值类型都实现 `Equatable` 时，编译器才会帮你合成；否则得自己写比较逻辑，或者改用 `switch` 逐分支判断。

## 属性的七种形态

属性是 Swift 里最容易"会写但没系统学过"的一块。全家族摆在一起看：

| 形态 | 写法 | 什么时候用 |
| --- | --- | --- |
| 存储属性 | `var x = 0` | 默认 |
| 常量属性 | `let x = 0` | 初始化后不变 |
| 懒加载 | `lazy var x = compute()` | 开销大、可能用不到 🔥 |
| 计算属性 | `var x: T { get { } set { } }` | 由其他状态派生 |
| 只读计算属性 | `var x: T { expr }` | 省略 `get` |
| 观察器 | `var x = 0 { willSet { } didSet { } }` | 值变化时联动 |
| 类型属性 | `static let shared = ...` | 全局唯一，与实例无关 |

```swift
struct Person {
    let name: String
    var nickname: String = ""

    lazy var displayName: String = {       // 第一次访问才计算
        print("计算了一次")
        return nickname.isEmpty ? name : nickname
    }()

    var formalName: String { "\(name)（\(nickname)）" }   // 每次访问都算

    var age: Int = 0 {
        willSet { print("年龄将从 \(age) 变成 \(newValue)") }
        didSet { print("年龄从 \(oldValue) 变成了 \(age)") }
    }

    static let anonymous = Person(name: "匿名", nickname: "")
}

var alice = Person(name: "Alice")
print(alice.displayName, alice.displayName)
// prints: 计算了一次
//         Alice Alice

alice.age = 30
// prints: 年龄将从 0 变成 30
//         年龄从 0 变成了 30
```

| 细节 | 说明 |
| --- | --- |
| `lazy` 只能在 `var` 上 | 常量没有"稍后再算"的概念 |
| `lazy` 不是线程安全的 | 多线程同时首次访问可能算两次 🚧 |
| 计算属性不能加 `lazy` | 它本来就不存东西 |
| `willSet` 拿 `newValue`，`didSet` 拿 `oldValue` | 名字固定，但可以省略参数名 |
| 初始化器里赋值不触发观察器 | 刻意设计，避免初始化期间乱响 |
| `didSet` 里改自己不会再触发一次 | 但会覆盖你刚才的赋值 🝖 |

### 属性包装器

把"每次读写都要做的加工"抽成一个类型，这就是属性包装器：

```swift
@propertyWrapper
struct Clamped {
    var wrappedValue: Int {
        didSet { wrappedValue = min(max(wrappedValue, range.lowerBound), range.upperBound) }
    }
    private let range: ClosedRange<Int>

    init(wrappedValue: Int, _ range: ClosedRange<Int>) {
        self.range = range
        self.wrappedValue = min(max(wrappedValue, range.lowerBound), range.upperBound)
    }
}

struct Player {
    @Clamped(0...100) var health: Int = 120
}

var player = Player()
print(player.health)
// prints: 100
player.health = -10
print(player.health)
// prints: 0
```

包装器还能通过 `projectedValue` 额外暴露一个值（`@Published` 的 `$name` 就是这么来的），SwiftUI 的状态管理大量依赖这个机制 🝖。

## 方法与下标

```swift
struct Matrix {
    let rows: Int, columns: Int
    var grid: [Double]

    init(rows: Int, columns: Int) {
        self.rows = rows
        self.columns = columns
        grid = Array(repeating: 0, count: rows * columns)
    }

    subscript(row: Int, column: Int) -> Double {
        get { grid[row * columns + column] }
        set { grid[row * columns + column] = newValue }
    }
}

var m = Matrix(rows: 2, columns: 2)
m[0, 1] = 5
print(m[0, 1])
// prints: 5.0
```

| 形态 | 写法 |
| --- | --- |
| 实例方法 | `func f()` |
| 改自身的方法 | `mutating func f()`（值类型） |
| 类型方法 | `static func f()` / `class func f()`（后者可被覆写） |
| 下标 | `subscript(index: Int) -> T` |
| 多参数下标 | `subscript(row: Int, column: Int)` |
| 类型下标 | `static subscript(...)` 🝖 |
| 动态成员 | `@dynamicMemberLookup` + `subscript(dynamicMember:)` 🝖 |
| 可调用实例 | `callAsFunction`，让实例像函数一样被调用 🆕 |

```swift
@dynamicMemberLookup
struct Settings {
    private var storage: [String: String] = [:]
    subscript(dynamicMember key: String) -> String? {
        get { storage[key] }
        set { storage[key] = newValue }
    }
}

var s = Settings()
s.theme = "dark"
print(s.theme ?? "none")
// prints: dark
```

## 扩展

`extension` 能给已有类型（包括别人的、甚至标准库的）加东西：

| 能加 | 不能加 |
| --- | --- |
| 计算属性、类型属性 | 存储属性 |
| 方法、下标 | 覆写已有实现 |
| 初始化器（有约束） | 类的 `deinit` |
| 协议遵守 | 改变已有类型的布局 |
| 嵌套类型 | |

```swift
extension String {
    var isPalindrome: Bool {
        let cleaned = lowercased().filter(\.isLetter)
        return cleaned == String(cleaned.reversed())
    }
}

print("上海自来水来自海上".isPalindrome)
// prints: true
```

⚠️ 类扩展里**不能**加指定初始化器（只能加 `convenience`），结构体扩展里加初始化器则完全没问题——因为结构体没有"指定"这一说。

🔥 把"协议遵守"单独放进一个 `extension`，是社区里最常见的组织方式：主定义只放存储属性与核心逻辑，扩展里放 `Codable`、`Equatable` 之类。

## typealias：给类型起个短名字

`typealias` 不创建新类型，只是给已有的类型加个别名。三个最常见的用法：

```swift
typealias UserID = Int                 // 给基础类型贴个业务标签
typealias Handler = (Int) -> Void      // 让难读的闭包类型有名字
typealias Pair<T> = (T, T)             // 泛型别名

let id: UserID = 7
let onDone: Handler = { print("完成", $0) }
onDone(id)
// prints: 完成 7

let bounds: Pair<Int> = (0, 100)
print(bounds.0, bounds.1)
// prints: 0 100
```

它也能出现在类型内部，给"自己用的那个类型参数"起名：

```swift
struct Box<T> {
    typealias Element = T          // 让外部可以写 Box<String>.Element
    var value: Element
}
print(Box(value: 3).value)
// prints: 3
```

| 要点 | 说明 |
| --- | --- |
| 只是别名 | `typealias X = Int` 之后，`X` 和 `Int` 完全等价，没有任何运行期成本 |
| 能写进协议 | `associatedtype Element` 的实现方可以用 `typealias Element = Int` 把它定下来 |
| 不能滥用 | 别名太多会让"这到底是什么类型"变得难查；`UserID`、`Seconds`、`Handler` 这类有语义的名字值得，`MyInt` 不值得 💭 |

🔥 `typealias` 最值钱的地方是**表达意图**：`func load(id: UserID)` 比 `func load(id: Int)` 少一半的注释。

## 访问控制

| 级别 | 可见范围 |
| --- | --- |
| `private` | 当前声明内部（同一个文件里的 `extension` 也能看到） |
| `fileprivate` | 当前文件 |
| `internal` | 当前模块，**默认值** |
| `package` | 同一个包内的多个模块 🆕 |
| `public` | 其他模块可见，但不能继承 / 覆写 |
| `open` | 其他模块可见、可继承、可覆写（仅类成员） |

```swift
public struct API {
    public private(set) var version = "1.0"   // 外部可读，内部可写
    private var secret = "内部状态"

    public init() {}
}
```

⚠️ `public` 类型的成员默认还是 `internal`，所以库的公开 API 必须逐个成员标 `public`——包括那个空 `public init() {}`，否则外部根本构造不出你的类型。

## 嵌套类型

```swift
struct Company {
    struct Employee {
        var name: String
    }
    enum Department { case engineering, design }
}

let e = Company.Employee(name: "Alice")
print(e.name, Company.Department.engineering)
// prints: Alice engineering
```

嵌套能让命名空间保持整洁：`Company.Employee` 比一堆 `CompanyEmployee` 前缀好读。

## 陷阱速查

| 陷阱 | 说明 |
| --- | --- |
| 用 `class` 但不需要共享 | 改 `struct`，值语义问题会少一大半 |
| 自定义 `init` 后成员初始化器消失 | 把**签名不同**的自定义 `init` 移进 `extension` 就能两者兼得；签名撞车会报重定义 |
| `lazy` 属性在并发下初始化两次 | 需要线程安全就加锁，或者改用 `static let` |
| 循环引用 | 类之间互相强引用、闭包捕获 `self` 都会造成泄漏 |
| 计算属性里做重活 | 每次访问都执行，调用方看不出来；需要缓存就用 `lazy` |
| 在 `didSet` 里改自己 | 会造成递归或覆盖赋值，想清楚再写 |
| 扩展加存储属性 | 编译不过，Swift 不允许 |
| 枚举关联值比较 | 需要 `Equatable`，否则要手写比较逻辑 |
| 把继承当默认选项 | 优先用协议 + 组合；`final` 既是语义也是性能上的好事 |
