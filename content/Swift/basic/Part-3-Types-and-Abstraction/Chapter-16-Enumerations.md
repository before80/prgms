+++
title = "第16章 枚举：关联值、原始值与可选值的真身"
weight = 160
date = "2026-09-14T22:30:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 第十六章：枚举：关联值、原始值与可选值的真身

> 枚举经常被误解成“给整数起名字”。在 Swift 里，它的野心大得多：可以携带不同形状的数据，可以有方法、计算属性，甚至能递归表达一棵树。你从第 9 章开始使用的 `Int?`，其实就是枚举。

## 16.1 基本枚举与穷尽检查

枚举做的事情很朴素：把一组相关的名字圈进同一个类型里，从此它们不再是散落各处的魔法字符串。

```swift
enum Direction {
    case north
    case south
    case east
    case west
}

let direction = Direction.north
switch direction {
case .north: print("北")
case .south: print("南")
case .east: print("东")
case .west: print("西")
}
// prints: 北
```

同一行的多个 `case` 用逗号分隔：

```swift
enum Season { case spring, summer, autumn, winter }
print(Season.summer)
// prints: summer
```

枚举最重要的好处是：只要列出所有情况，编译器就会替你检查 `switch` 是否遗漏。字符串常量做不到这一点。

## 16.2 原始值：和某种底层值建立映射

有些枚举天生对应着一个数字或字符串——HTTP 状态码、文件权限位、数据库里存的码值。原始值就是给它们搭的那座桥：

```swift
enum HTTPStatus: Int {
    case ok = 200
    case notFound = 404
    case serverError = 500
}

print(HTTPStatus.ok.rawValue)
// prints: 200
```

连续的整数原始值可以只写第一个：

```swift
enum Priority: Int { case low = 1, medium, high }
print(Priority.high.rawValue)
// prints: 3
```

字符串枚举可以省略原始值，默认就是 `case` 名：

```swift
enum Role: String { case admin, editor, viewer }
print(Role.editor.rawValue)
// prints: editor
```

从原始值创建枚举可能失败，因此返回可选值：

```swift
print(HTTPStatus(rawValue: 404) as Any)
// prints: Optional(notFound)
print(HTTPStatus(rawValue: 418) as Any)
// prints: nil
```

**原始值枚举自带 `Codable` 能力**，只要你在声明时写上它。这一点在存 JSON、调接口时非常实用：

```swift
import Foundation

enum Role: String, Codable, CaseIterable {
    case admin, editor, viewer
}

let data = try JSONEncoder().encode([Role.editor, .viewer])
print(String(decoding: data, as: UTF8.self))
// prints: ["editor","viewer"]

let back = try JSONDecoder().decode([Role].self, from: data)
print(back == [.editor, .viewer])
// prints: true
```

⚠️ 这里藏着一个真实项目里一定会撞上的坑：**解码遇到没见过的码值会直接失败**。后端加了一个 `"archived"`，客户端旧版本的枚举里没有这一支，解码就抛错：

```swift
import Foundation

enum Status: String, Codable {
    case draft = "DRAFT"
    case published = "PUBLISHED"
}

do {
    _ = try JSONDecoder().decode(Status.self, from: Data("\"ARCHIVED\"".utf8))
} catch {
    print("解码失败：", error is DecodingError)
    // prints: 解码失败： true
}
```

两种常见的应对方式：给枚举加一个 `case unknown` 并在自定义 `init(from:)` 里兜住所有不认识的码值；或者**把这层防御放到接口模型上**，让"用户看到的枚举"和"线上可能出现的码值"解耦。选哪种取决于这份数据是"完全受你控制"还是"对方随时可能加值"。

## 16.3 关联值：每个分支可以携带不同数据

原始值要求所有分支共享同一种底层类型；关联值没有这个限制：

```swift
enum Payment {
    case cash(amount: Double)
    case card(number: String, amount: Double)
    case failed(reason: String)
}
```

匹配时可以提取数据：

```swift
let payment = Payment.card(number: "**** 1234", amount: 88.5)

switch payment {
case .cash(let amount):
    print("现金 \(amount)")
case .card(let number, let amount):
    print("卡 \(number) 支付 \(amount)")
case .failed(let reason):
    print("失败：\(reason)")
}
// prints: 卡 **** 1234 支付 88.5
```

关联值和"一个父类 + 若干子类"能表达的东西很像，但取舍不同，值得在前几秒就想清楚：

| 对比项 | 枚举 + 关联值 | 类继承 |
| --- | --- | --- |
| 分支数量 | 封闭，编译期就知道有几支 | 开放，别人可以随时加子类 |
| `switch` 检查 | 必须穷尽，漏一支就编译不过 | 没有穷尽检查 |
| 每个分支的数据 | 只带自己需要的那几项 | 靠属性，容易带上用不到的状态 |
| 扩展行为 | 靠扩展和协议 | 靠重写（`override`） |

判断口诀：**分支是"有限且已知"的，用枚举；分支会被外部无限扩展的，用协议或继承。** 订单状态、网络结果、加载状态这类东西属于前者；插件、格式解析器这类属于后者。

如果只需要部分关联值：

```swift
switch payment {
case .card(_, let amount):
    print(amount)
default:
    break
}
// prints: 88.5
```

## 16.4 方法、计算属性与 `mutating`

枚举可以拥有行为：

```swift
enum Coin {
    case head, tail

    var label: String {
        switch self {
        case .head: "正面"
        case .tail: "反面"
        }
    }

    mutating func flip() {
        self = self == .head ? .tail : .head
    }
}

var coin = Coin.head
print(coin.label)
// prints: 正面
coin.flip()
print(coin.label)
// prints: 反面
```

枚举是值类型，修改 `self` 的方法必须标 `mutating`。`self` 在这里代表“当前这个枚举值”。

## 16.5 `CaseIterable`：遍历所有分支

没有关联值的枚举可以让编译器生成 `allCases`：

```swift
enum Weekday: CaseIterable {
    case monday, tuesday, wednesday, thursday, friday, saturday, sunday
}

print(Weekday.allCases.count)
// prints: 7
for day in Weekday.allCases.prefix(3) {
    print(day)
}
// prints: monday
// prints: tuesday
// prints: wednesday
```

有关联值的分支也能遵循 `CaseIterable`，但需要手动实现 `allCases`。

`allCases` 的顺序**就是声明顺序**，所以"工作日/周末"这类需要按顺序展示的场景，直接按想要的顺序写 `case` 即可，不必再排一次序：

```swift
enum Weekday: CaseIterable, Identifiable {
    case monday, tuesday, wednesday, thursday, friday, saturday, sunday

    var id: Self { self }      // 让它在 SwiftUI 的 ForEach 里可以直接用
}

for day in Weekday.allCases.suffix(2) {
    print(day)
}
// prints: saturday
// prints: sunday
```

## 16.6 递归枚举：用 `indirect` 表达树

枚举的关联值如果又是该枚举自身，需要写 `indirect`：

```swift
indirect enum Expression {
    case number(Int)
    case add(Expression, Expression)
    case multiply(Expression, Expression)
}

func evaluate(_ expression: Expression) -> Int {
    switch expression {
    case .number(let value):
        return value
    case .add(let left, let right):
        return evaluate(left) + evaluate(right)
    case .multiply(let left, let right):
        return evaluate(left) * evaluate(right)
    }
}

let expression = Expression.add(.number(2), .multiply(.number(3), .number(4)))
print(evaluate(expression))
// prints: 14
```

也可以只让某个分支间接存储：

```swift
enum List {
    case empty
    indirect case node(Int, next: List)
}
```

递归枚举在解析器、抽象语法树和状态机里非常常见。

为什么必须写 `indirect`？因为枚举的大小要在编译期算出来：`Expression` 的一个分支里放着两个 `Expression`，编译器就开始算"要几个 `Expression` 才能装下一个 `Expression`"——这题没有答案。`indirect` 相当于告诉编译器"这个分支别内联存放，改成放一个盒子"，于是大小立刻可算。可以整体标 `indirect enum`，也可以只标需要的那个分支（像上面的 `List`）。代价是多一次间接访问和一点堆分配。

## 16.7 实战：用枚举表达状态机

订单、上传、支付、订阅……它们的共同点是"有一组有限状态，每种状态允许的操作不一样"。这正是枚举最擅长的活，而且编译器会帮你守住规则：

```swift
import Foundation

enum OrderState: Equatable {
    case pending
    case paid(at: Date)
    case shipped(tracking: String)
    case cancelled(reason: String)
    case refunded
}

extension OrderState {
    var canCancel: Bool {
        switch self {
        case .pending, .paid: true
        case .shipped, .cancelled, .refunded: false
        }
    }

    var title: String {
        switch self {
        case .pending: "待支付"
        case .paid: "已支付"
        case .shipped(let tracking): "已发货（\(tracking)）"
        case .cancelled(let reason): "已取消：\(reason)"
        case .refunded: "已退款"
        }
    }

    func cancelling(reason: String) -> OrderState? {
        guard canCancel else { return nil }
        return .cancelled(reason: reason)
    }
}

let states: [OrderState] = [.pending, .paid(at: .now), .shipped(tracking: "SF123"), .refunded]
for state in states {
    print(state.title, state.canCancel ? "可取消" : "不可取消")
}
// prints: 待支付 可取消
// prints: 已支付 可取消
// prints: 已发货（SF123） 不可取消
// prints: 已退款 不可取消

print(OrderState.shipped(tracking: "SF123").cancelling(reason: "改主意") as Any)
// prints: nil
```

注意 `canCancel` 这个计算属性里的 `switch`：它**没有 `default`**，所以将来有人往枚举里加一个 `.returned` 分支，这段代码立刻编译不过，逼着他去想"退货状态能不能取消"。这就是第 16.1 节那句"编译器替你检查"的真实价值——它不是省事，是把"忘了处理新情况"变成了不可能。

把 `canCancel` 写成 `switch` 而不是 `if self == .pending || ...` 还有一层好处：`Equatable` 比较对带关联值的分支要求所有关联值也相等，用 `switch` 则可以用 `case .paid:` 忽略具体时间戳，语义更贴近"只要处于已支付状态"。

## 16.8 可选值的真身

可选值本质上就是带泛型的枚举：

```swift
enum MyOptional<Wrapped> {
    case none
    case some(Wrapped)
}

let a: MyOptional<Int> = .some(1)
let b: MyOptional<Int> = .none

switch a {
case .some(let value): print(value)
case .none: print("nil")
}
// prints: 1
```

Swift 的 `Optional` 和这个结构等价，`.none` 可以写成 `nil`，`Optional<Int>` 可以写成 `Int?`。知道这一点后，很多语法都顺了：

```swift
let x: Int? = .some(42)
let y: Int? = .none
print(x as Any, y as Any)
// prints: Optional(42) nil
```

既然 `Optional` 只是一个普通的泛型枚举，它当然也能被扩展——这是"理解真身"最直接的回报：

```swift
import Foundation

extension Optional where Wrapped == String {
    var isBlank: Bool {
        switch self {
        case .none: true
        case .some(let text): text.trimmingCharacters(in: .whitespaces).isEmpty
        }
    }
}

let nickname: String? = "   "
print(nickname.isBlank)
// prints: true

let missing: String? = nil
print(missing.isBlank)
// prints: true
```

注意最后这次调用：`"   ".isBlank` 是**编译不过**的——`isBlank` 挂在 `Optional<String>` 上，一个普通的 `String` 字面量不会自动"提升"成可选值来匹配这个扩展。要用它，就得先声明成 `String?`。这就是"知道 `nil` 的真身"最实用的一条副产品：你知道该去哪一层写扩展。

顺带一提，`Optional` 还遵循 `ExpressibleByNilLiteral`，这正是"任何类型都能被赋值为 `nil`"的实现方式；`?`、`!`、`??`、`if let`、`guard let` 这一整套语法，都是在这个小小枚举之上长出来的糖衣（第 15B 章有专门整理）。

## 16.9 本章小结

| 能力 | 关键结论 |
| --- | --- |
| 基本枚举 | 一组互斥状态，`switch` 由编译器检查穷尽性 |
| 原始值 | 每个分支映射到同一种底层值，可用 `rawValue` 获取 |
| 关联值 | 每个分支可携带不同结构的数据 |
| 行为 | 枚举可以有计算属性、方法和 `mutating` 方法 |
| `CaseIterable` | 无关联值枚举可自动获得 `allCases` |
| 递归枚举 | 使用 `indirect` 间接存储自身 |
| 状态机 | 枚举 + 穷尽 `switch` 把业务规则固化成编译期检查 |
| 可选值 | `Optional` 是 `.some` / `.none` 枚举 |

## 16.10 本章易错点速查

| 易错点 | 正确理解 |
| --- | --- |
| 把原始值和关联值混为一谈 | 原始值同型且每支唯一；关联值每支可不同 |
| 用 `rawValue` 初始化后直接使用 | 返回可选值，原始值不合法时为 `nil` |
| 忘记 `mutating` | 值类型方法修改 `self` 必须标注 |
| 递归枚举漏写 `indirect` | 编译器无法计算大小 |
| 在 `switch` 中漏 `case` | 枚举会被严格检查，必须穷尽 |
| 认为 `nil` 是特殊对象 | `nil` 就是 `.none` 的语法糖 |
| 解码线上数据时没有兜底分支 | 后端加新码值会让旧客户端解码失败，需自定义 `init(from:)` |
| 用 `default` 掩盖枚举分支 | 会失去"加新分支时编译报错"的保护 |

## 16.11 下章预告

下一章进入结构体。它是 Swift 日常建模的默认选择：轻、值语义、线程间传递时不容易共享暗状态。你会发现，理解“赋值到底复制了什么”，比背语法更重要。
