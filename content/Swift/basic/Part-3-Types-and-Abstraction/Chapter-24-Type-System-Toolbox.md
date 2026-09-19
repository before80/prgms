+++
title = "第24章 类型系统补全：Any、Self、KeyPath 与类型擦除"
weight = 240
date = "2026-09-14T22:30:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 第二十四章：类型系统补全：`Any`、`Self`、`KeyPath` 与类型擦除

> 前面的协议和泛型已经足够搭出大多数抽象。但 Swift 的类型工具箱里还有一些“小而关键”的工具：`Any`、元类型、`Self`、键路径、可调用类型和类型擦除。它们不是每天都用，却经常出现在框架和库的底层。

## 24.1 `Any` 与 `AnyObject`

`Any` 能装任意类型的值：

```swift
let values: [Any] = [1, "two", 3.0]
for value in values {
    print(type(of: value), value)
}
// prints: Int 1
// prints: String two
// prints: Double 3.0
```

`AnyObject` 只能装类实例：

```swift
final class Item {}
let objects: [AnyObject] = [Item()]
```

`Any` 很方便，也会擦除类型信息。取出后通常要 `as?` 转回来，因此它更适合异构集合、调试和桥接层，不适合当主要数据模型。

`AnyHashable` 则能装任意可哈希值——它把"这个键原本是什么类型"这件事也一起装了进去，所以不同类型的键可以共存于同一个字典：

```swift
let mixed: [AnyHashable: String] = [1: "一", "two": "二"]
print(mixed[AnyHashable(1)] ?? "无")
// prints: 一
```

这种"混合键字典"在解析外部 JSON、处理数据库返回值时才常见；自己设计的数据结构最好不要用到它。

## 24.2 元类型：类型本身也是值

`T.self` 得到类型本身，类型写作 `T.Type`：

```swift
let type: Int.Type = Int.self
print(type)
// prints: Int
```

动态获取某个值的类型：

```swift
let value = 42
print(type(of: value) == Int.self)
// prints: true
```

元类型可以用于注册表、工厂和动态创建：

```swift
protocol DefaultConstructible {
    static func makeDefault() -> Self
}

func makeDefault<T: DefaultConstructible>(_ type: T.Type) -> T {
    type.makeDefault()
}
```

这类写法要谨慎：一旦大量依赖元类型，类型信息就从编译期滑向运行期，错误也更容易在运行时才暴露。

## 24.3 `Self`：当前动态类型

协议里的 `Self` 表示“遵循该协议的具体类型”：

```swift
protocol Duplicable {
    func duplicate() -> Self
}

struct Document: Duplicable {
    var title: String
    func duplicate() -> Document {
        Document(title: title)
    }
}

print(Document(title: "A").duplicate().title)
// prints: A
```

> 这里的协议故意叫 `Duplicable`，因为 `Copyable` 已经是标准库里用于值复制语义的协议名；教学示例不要和它抢名字。

在类型内部，`Self` 还可以作为返回值或工厂：

```swift
struct Point {
    var x = 0, y = 0
    static func origin() -> Self { Self() }
}
print(Point.origin().x)
// prints: 0
```

`Self` 比具体类型名更灵活，它让方法在子类中仍然描述“调用者的实际类型”。

## 24.4 `Never`：没有正常返回

`Never` 是没有任何值的类型，表示函数永远不返回：

```swift
func fail(_ message: String) -> Never {
    fatalError(message)
}
```

`Never` 也可以作为返回值出现在那些必然抛错、崩溃或陷入无限循环的函数里。泛型返回 `Never` 时，函数调用点被编译器视为“此处之后的代码不可达”。

## 24.5 键路径：把属性访问变成值

键路径用反斜杠加属性名表示：

```swift
struct User {
    var name: String
    var age: Int
}

let nameKey = \User.name
let user = User(name: "Mia", age: 28)
print(user[keyPath: nameKey])
// prints: Mia
```

键路径可以方便地用于映射：

```swift
let users = [User(name: "A", age: 20), User(name: "B", age: 30)]
print(users.map(\.name))
// prints: ["A", "B"]
print(users.map(\.age).reduce(0, +))
// prints: 50
```

可写键路径类型是 `WritableKeyPath`，可以修改值：

```swift
var mutable = user
mutable[keyPath: \User.age] = 29
print(mutable.age)
// prints: 29
```

键路径也是**有类型的值**，所以它们能进数组、能当参数，也能被擦除。`PartialKeyPath` 抹掉了"读写能力"这一层，让不同属性的键路径住进同一个数组；`AnyKeyPath` 连根类型也一起抹掉：

```swift
struct User { var name: String; var age: Int }
final class Account { var balance = 0 }

let partials: [PartialKeyPath<User>] = [\User.name, \User.age]
print(partials.count, type(of: partials[0]))
// prints: 2 WritableKeyPath<User, String>

let anyPath: AnyKeyPath = \Account.balance
print(type(of: anyPath))
// prints: ReferenceWritableKeyPath<Account, Int>

let account = Account()
account[keyPath: \Account.balance] = 100
print(account.balance)
// prints: 100
```

注意 `Account` 是类，它的键路径类型是 `ReferenceWritableKeyPath`——"可写"这件事对值类型和引用类型的含义不同（第 17、18 章）。`PartialKeyPath`、`AnyKeyPath` 牺牲了类型信息，换来"把一堆不同的键路径装在一起"的能力，数据绑定、排序规则和响应式框架都靠它。

## 24.6 `callAsFunction`：让实例像函数一样调用

实现 `callAsFunction` 后，实例可以加括号调用：

```swift
struct Multiplier {
    let factor: Int

    func callAsFunction(_ value: Int) -> Int {
        value * factor
    }
}

let triple = Multiplier(factor: 3)
print(triple(4))
// prints: 12
```

它可以有多个重载和不同参数。这个特性很适合“配置加行为”的轻量对象，但不要让调用语法隐藏太多真实工作。

## 24.7 动态成员查找：点语法接住任意名字

`@dynamicMemberLookup` 允许把未知属性名转成方法调用：

```swift
@dynamicMemberLookup
struct DynamicBag {
    private var values: [String: String] = [:]

    subscript(dynamicMember key: String) -> String? {
        get { values[key] }
        set { values[key] = newValue }
    }
}

var bag = DynamicBag()
bag.name = "Mia"
print(bag.name ?? "nil")
// prints: Mia
```

动态成员查找常用于 JSON、脚本接口和动态配置。代价是拼写错误可能只在运行时暴露，所以静态模型更清晰的场景不要为了少写代码而使用它。

与它相邻的还有 `@dynamicCallable`，它把参数列表交给 `dynamicallyCall` 方法：

```swift
@dynamicCallable
struct Sum {
    func dynamicallyCall(withArguments values: [Int]) -> Int {
        values.reduce(0, +)
    }
}

let sum = Sum()
print(sum(1, 2, 3))
// prints: 6
```

动态调用适合脚本桥接和高度动态的接口；它牺牲的同样是编译期参数检查。

## 24.8 类型擦除：把具体类型藏进一个稳定的盒子

存在类型 `any P` 能直接擦除类型，但有时你需要把多个泛型能力统一成一个具体包装类型。典型做法是用闭包保存操作：

```swift
protocol Animal {
    associatedtype Food
    func eat(_ food: Food) -> String
}

struct AnyAnimal: Animal {
    private let eatClosure: (Any) -> String

    init<A: Animal>(_ animal: A) {
        eatClosure = { food in
            guard let food = food as? A.Food else { return "食物类型不对" }
            return animal.eat(food)
        }
    }

    func eat(_ food: Any) -> String {
        eatClosure(food)
    }
}
```

这个例子的类型安全被削弱了，但换来一个可以统一存放的 `AnyAnimal`。现代 Swift 在许多场景下可以优先使用 `any P` 或 `some P`；需要手写类型擦除时，再引入这样的包装类型。

## 24.9 `Codable`：把模型变成可传输的数据

`Encodable` 表示能编码，`Decodable` 表示能解码，`Codable` 是两者的组合。纯数据模型通常可以让编译器自动合成实现：

```swift
import Foundation

struct UserDTO: Codable, Equatable {
    let id: Int
    var name: String
}

let user = UserDTO(id: 1, name: "Mia")
let data = try JSONEncoder().encode(user)
let decoded = try JSONDecoder().decode(UserDTO.self, from: data)
print(decoded == user)
// prints: true
```

当 JSON 字段名和 Swift 属性名不一致时，用 `CodingKeys` 指定映射：

```swift
import Foundation

struct Article: Codable {
    let title: String
    let authorName: String

    enum CodingKeys: String, CodingKey {
        case title
        case authorName = "author_name"
    }
}
```

`Codable` 不负责网络、文件或数据库，它只负责“值 ↔ 编码格式”的转换。日期策略、键名策略和错误处理都应该在边界层明确配置。

## 24.10 常用标准协议

类型系统里有一些协议几乎每天都会遇到：

| 协议 | 用途 | 典型做法 |
| --- | --- | --- |
| `Equatable` | 判断值相等 | 实现 `==` |
| `Hashable` | 作为字典键、集合元素 | 实现 `hash(into:)` |
| `Comparable` | 排序 | 实现 `<` |
| `Codable` | 编码解码 | 合成 `Encodable`/`Decodable` |
| `Identifiable` | 稳定身份 | 提供 `id` |
| `CustomStringConvertible` | 自定义打印 | 提供 `description` |
| `CaseIterable` | 枚举遍历 | 提供 `allCases` |
| `OptionSet` | 位集合选项 | 组合多个标志 |
| `RawRepresentable` | 原始值与类型互转 | 提供 `rawValue` 和 `init?(rawValue:)` |
| `Sequence` / `Collection` | 遍历与集合能力 | 自定义容器时遵循 |

这些协议看起来零散，却构成了 Swift 数据建模的公共语言。看到一个类型声明遵循它们，调用者就能立刻知道它能做哪些事。

表里那些"实现某某"平时都由编译器合成（第 15B.16 节），但你需要知道手写版长什么样。`Hashable` 的手写版尤其值得看一眼，因为它有条不能违反的规矩：**相等的值必须有相同的哈希值**。

```swift
struct Point: Hashable {
    var x: Int
    var y: Int

    func hash(into hasher: inout Hasher) {
        hasher.combine(x)          // 参与哈希的字段
        hasher.combine(y)
    }

    static func == (lhs: Point, rhs: Point) -> Bool {
        lhs.x == rhs.x && lhs.y == rhs.y
    }
}

print(Set([Point(x: 1, y: 2), Point(x: 1, y: 2)]).count)
// prints: 1
print(Point(x: 1, y: 2).hashValue == Point(x: 1, y: 2).hashValue)
// prints: true
```

一旦你写了自己版本的 `hash(into:)` 和 `==`，编译器就不再替你合成——所以"参与比较的字段"和"参与哈希的字段"必须对得上，否则会出现"两个值相等，却在 `Set` 里同时存在"这种灵异事件。

## 24.11 反射：`Mirror`

Swift 不鼓励依赖运行时反射，但标准库给了一个只读的 `Mirror`，用来查看任意值的内部结构。调试日志、通用打印和工具代码里偶尔会用到它：

```swift
struct Point {
    var x: Int
    var y: Int
}

let p = Point(x: 3, y: 4)
let mirror = Mirror(reflecting: p)

print(mirror.displayStyle == .struct)
// prints: true
for child in mirror.children {
    print(child.label ?? "?", child.value)
}
// prints: x 3
// prints: y 4
```

`mirror.children` 是"每个存储属性一个元素"的序列，每项有 `label`（属性名）和 `value`（值）；`label` 是可选的，因为有些布局拿不到名字，所以要 `?? "?"` 兜底。

两个限制必须记住：`Mirror` 只读，改不了属性；它也不承诺暴露类型的全部内部存储，优化后的布局可能看不到。所以它适合“展示和诊断”，不适合当序列化或依赖注入的底座——那类需求应该交给 `Codable` 或显式协议。

## 24.12 自定义字面量

`42`、`"hi"`、`[1, 2]` 这些字面量背后其实是一组协议：`ExpressibleByIntegerLiteral`、`ExpressibleByStringLiteral`、`ExpressibleByArrayLiteral` 等。让自己的类型遵循它们，调用点就能写得像内建类型一样自然：

```swift
struct RGB: ExpressibleByArrayLiteral, CustomStringConvertible {
    var values: [Int]

    init(arrayLiteral elements: Int...) {
        values = elements
    }

    var description: String { "RGB\(values)" }
}

let color: RGB = [255, 128, 0]
print(color)
// prints: RGB[255, 128, 0]
```

（`values` 是数组，字符串插值会带上方括号，所以连起来是 `RGB[255, 128, 0]`。想让输出更像 `RGB(255, 128, 0)`，自己拼一下 `values.map(String.init).joined(separator: ", ")` 即可。）

每个字面量协议只要求一个初始化器。好处是调用点更干净，同时类型安全一点没丢：`let c: RGB = "abc"` 会被编译器直接拒绝。

## 24.13 本章小结

| 工具 | 用途 |
| --- | --- |
| `Any` / `AnyObject` | 装任意值 / 任意类实例 |
| 元类型 | 把类型本身当作值传递 |
| `Self` | 表示当前实际类型 |
| `Never` | 表示永远不会正常返回 |
| `KeyPath` | 把属性访问变成可传递的值 |
| `callAsFunction` | 让实例像函数一样调用 |
| `@dynamicMemberLookup` | 支持动态点语法 |
| 类型擦除 | 用统一包装隐藏具体泛型类型 |
| `Mirror` | 只读地查看值的内部结构 |
| 字面量协议 | 让自定义类型接受 `42`、`"hi"`、`[1, 2]` 这类写法 |

## 24.14 本章易错点速查

| 易错点 | 正确理解 |
| --- | --- |
| 到处用 `Any` | 会丢掉编译期类型信息，尽量用泛型或协议 |
| 以为 `type(of:)` 返回静态类型 | 它返回运行时动态类型 |
| 把 `Self` 当成简单别名 | 它表达当前实际类型，和动态派发有关 |
| 滥用键路径 | 清晰的直接属性访问通常更易读 |
| 依赖动态成员查找拼写 | 拼写错误可能只在运行时暴露 |
| 手写类型擦除过早 | 先考虑 `some`/`any` 是否够用 |
| 用 `Mirror` 做序列化 | 它只读且不一定覆盖全部存储，序列化请用 `Codable` |

## 24.15 下章预告

当项目变大，类型和模块的边界就需要规则。下一章讲访问控制、模块、条件编译和可用性检查：谁能看见什么、什么代码只在某些平台存在、怎样在不破坏兼容性的情况下标记旧接口。
