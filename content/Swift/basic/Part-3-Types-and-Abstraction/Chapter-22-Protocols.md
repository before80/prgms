+++
title = "第22章 协议：描述能力，打通类型边界"
weight = 220
date = "2026-09-14T22:30:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 第二十二章：协议：描述能力，打通类型边界

> 协议不是在问“你是什么类型”，而是在问“你能做什么”。它让结构体、枚举和类站在同一张能力清单前，各自给出实现。写好协议，代码之间就能依赖抽象而不是依赖具体实现。

## 22.1 定义与遵循协议

协议只规定“要有什么”，不规定“怎么实现”：

```swift
protocol Greeter {
    func greet() -> String
}

struct EnglishGreeter: Greeter {
    func greet() -> String { "Hello" }
}

struct ChineseGreeter: Greeter {
    func greet() -> String { "你好" }
}

let greeters: [Greeter] = [EnglishGreeter(), ChineseGreeter()]
for greeter in greeters {
    print(greeter.greet())
}
// prints: Hello
// prints: 你好
```

遵循协议的类型必须实现所有必需成员。协议可以要求属性：

```swift
protocol Named {
    var name: String { get }
}

struct Person: Named {
    let name: String
}
```

`{ get }` 表示只要可读；`{ get set }` 表示必须可读可写。`let` 属性可以满足 `get`，但不能满足 `get set`。

## 22.2 协议继承与组合

协议可以继承另一个协议：

```swift
protocol Identifiable: Named {
    var id: Int { get }
}
```

也可以临时组合多个能力，使用 `&`：

```swift
protocol Aged {
    var age: Int { get }
}

func printInfo(_ value: Named & Aged) {
    print(value.name, value.age)
}
```

组合适合“我只关心参数同时满足这几种能力”的场景，不需要专门再造一个空协议。

## 22.3 类专用协议与弱引用委托

如果协议只能由类遵循，让它继承 `AnyObject`：

```swift
protocol DownloaderDelegate: AnyObject {
    func downloadDidFinish(_ name: String)
}

final class Downloader {
    weak var delegate: DownloaderDelegate?
}
```

`weak` 只能修饰类实例类型。加 `AnyObject` 是为了让编译器确认“这个协议的值一定可以弱引用”，从而避免循环引用。委托模式几乎总会用到这一组合。

## 22.4 默认实现：共享行为的捷径

协议扩展可以提供默认实现：

```swift
protocol Describable {
    var label: String { get }
}

extension Describable {
    func describe() -> String {
        "对象：\(label)"
    }
}

struct Item: Describable {
    let label: String
}

print(Item(label: "书").describe())
// prints: 对象：书
```

默认实现能减少重复，也会带来一个关键问题：通过协议类型调用时，分派的是协议要求里的实现；只在扩展里定义、没有写进协议要求的方法，不一定走动态派发。

```swift
protocol P {}
extension P {
    func onlyExtension() -> String { "协议扩展" }
}

struct S: P {
    func onlyExtension() -> String { "具体类型" }
}

let value: P = S()
print(value.onlyExtension())
// prints: 协议扩展
```

如果方法是协议要求，行为会更符合“多态”的直觉；如果只是扩展里的普通方法，调用时可能按静态类型选择实现。写抽象接口时，把真正需要多态的方法放进协议声明。

## 22.5 关联类型：协议里的占位类型

协议可以用 `associatedtype` 表示暂未确定的类型：

```swift
protocol Container {
    associatedtype Item

    mutating func append(_ item: Item)
    var count: Int { get }
}

struct IntBox: Container {
    private var values: [Int] = []

    mutating func append(_ item: Int) { values.append(item) }
    var count: Int { values.count }
}
```

`Item` 会在遵循时由编译器推断为 `Int`。也可以在协议上声明主关联类型，让 `any Container<Int>` 这种写法更简洁：

```swift
protocol Container<Item> {
    associatedtype Item
    mutating func append(_ item: Item)
}
```

## 22.6 `some` 与 `any`

`some P` 表示“某个具体的、实现 P 的类型，但我不告诉你是谁”：

```swift
func makeGreeter() -> some Greeter {
    EnglishGreeter()
}
```

调用者只能把它当成 `Greeter` 使用，编译器保留具体类型信息，因此很多操作更高效。

`any P` 表示“任意的 P 类型”，是一个存在类型盒子：

```swift
let greeters: [any Greeter] = [EnglishGreeter(), ChineseGreeter()]
```

需要把不同类型放进同一个数组、属性或参数位置时，通常使用 `any`。需要保留具体类型、构建流畅链式接口时，优先考虑 `some`。第 24 章会继续讲存在类型和类型擦除。

## 22.7 协议中的初始化器

协议可以要求初始化器：

```swift
protocol Buildable {
    init(name: String)
}

struct Project: Buildable {
    let name: String
    init(name: String) { self.name = name }
}
```

如果类遵循带 `init` 要求的协议，实现时要写 `required init`，因为子类也必须能提供这个初始化入口。

## 22.8 `@resultBuilder`：把语句拼成结果

结果构建器可以把一串语句收集成一个值，SwiftUI 的视图声明就是典型应用。下面用一个小例子构建字符串：

```swift
@resultBuilder
struct TextBuilder {
    static func buildBlock(_ parts: String...) -> String {
        parts.joined(separator: "\n")
    }
}

func makeText(@TextBuilder _ content: () -> String) -> String {
    content()
}

let text = makeText {
    "第一行"
    "第二行"
}
print(text)
// prints: 第一行
// prints: 第二行
```

构建器还支持 `buildIf`、`buildEither`、`buildArray` 等静态方法，让 `if`、`else` 和循环也能参与构造。SwiftUI 的 `@ViewBuilder` 就是标准库之外最有名的一个：`View` 协议把 `body` 声明成了 `@ViewBuilder`，所以实现里能直接并列写视图、写 `if` 和 `ForEach`。语法糖的完整侧写在第 15B.18 节。不要为了炫技手写构建器；当某个接口确实需要“像 DSL 一样声明数据”时，它才是好工具。

## 22.9 本章小结

| 概念 | 作用 |
| --- | --- |
| 协议 | 描述类型必须具备的能力 |
| 协议继承 | 在已有能力上扩展新要求 |
| 协议组合 | 用 `A & B` 表达多个能力 |
| `AnyObject` | 限定协议只能由类遵循，便于 `weak` 委托 |
| 默认实现 | 在协议扩展中共享行为 |
| 关联类型 | 协议中的待定类型，满足泛型化需求 |
| `some` | 隐藏具体类型但保留身份 |
| `any` | 承载任意符合协议的类型 |
| `@resultBuilder` | 把声明式语句构造成结果 |

## 22.10 本章易错点速查

| 易错点 | 正确理解 |
| --- | --- |
| 用 `let` 满足 `get set` 要求 | `let` 不满足可写要求 |
| 以为协议扩展方法一定动态派发 | 只有协议要求中的成员走协议见证分派 |
| 委托属性没有 `weak` | 可能造成循环引用 |
| 把 `any` 到处使用 | 存在类型会擦除具体类型，性能与能力都受限 |
| 给 `some` 返回不同类型分支 | `some` 必须始终返回同一种具体类型 |
| 为简单功能手写 `@resultBuilder` | 构建器应服务于清晰的声明式接口 |

## 22.11 下章预告

协议解决“能做什么”，泛型解决“对任意类型都成立”。下一章会把泛型函数、泛型类型、关联类型约束、`some`/`any` 和 Swift 6 的值泛型连成完整的一套工具。
