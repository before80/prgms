+++
title = "第21章 扩展与嵌套类型：在原有类型上继续生长"
weight = 210
date = "2026-09-14T22:30:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 第二十一章：扩展与嵌套类型：在原有类型上继续生长

> 扩展让你给已有类型添加新能力，却不必改动原声明；哪怕类型的源码不在你手里也能做到。它的力量来自“保持类型身份不变”：扩展后的 `String` 仍然是 `String`，不是某个包装类。用得好，代码分层清晰；用过头，则会把职责撒得到处都是。

## 21.1 扩展能添加什么

扩展可以添加计算属性、方法、初始化器、下标、协议实现和嵌套类型。它不能添加存储属性，也不能给已有属性加属性观察器。

```swift
extension Int {
    var squared: Int { self * self }

    func times(_ action: () -> Void) {
        for _ in 0..<self { action() }
    }
}

print(5.squared)
// prints: 25
3.times { print("hi") }
// prints: hi
// prints: hi
// prints: hi
```

这段扩展没有创建新类型，`5.squared` 仍然是普通的 `Int` 运算。

## 21.2 用扩展组织协议实现

一个常见做法是把类型主体保持简短，把协议实现集中到扩展里：

```swift
struct User {
    let name: String
}

extension User: CustomStringConvertible {
    var description: String { "User(\(name))" }
}

print(User(name: "Mia"))
// prints: User(Mia)
```

扩展可以按职责拆分到不同文件，例如 `User+Networking.swift`、`User+Validation.swift`。但不要为了“文件整齐”把类型撕成互不相干的碎片。

## 21.3 用扩展补充初始化器

值类型可以在扩展里添加初始化器，而且不会丢掉自动生成的成员逐一初始化器：

```swift
struct Point {
    var x: Int
    var y: Int
}

extension Point {
    init(value: Int) {
        self.init(x: value, y: value)
    }
}

print(Point(x: 1, y: 2).x, Point(value: 5).y)
// prints: 1 5
```

类扩展也可以添加便利初始化器，但不能添加指定初始化器。

## 21.4 条件扩展：满足条件才拥有能力

泛型扩展可以带 `where` 约束：

```swift
struct Stack<Element> {
    private var items: [Element] = []

    mutating func push(_ item: Element) { items.append(item) }
    mutating func pop() -> Element? { items.popLast() }
}

extension Stack where Element: Equatable {
    func contains(_ item: Element) -> Bool {
        items.contains(item)
    }
}

var stack = Stack<Int>()
stack.push(1)
print(stack.contains(1))
// prints: true
```

条件遵循协议时，语法写成：

```swift
extension Stack: Equatable where Element: Equatable {
    static func == (lhs: Stack, rhs: Stack) -> Bool {
        lhs.items == rhs.items
    }
}
```

`items` 是私有属性，为什么这里能访问？因为扩展写在同一个文件里，`private` 在文件作用域内可见。跨文件扩展就访问不到它。

## 21.5 扩展外部类型：别乱认亲戚

你可以扩展标准库或框架里的类型：

```swift
import Foundation

extension String {
    var isBlank: Bool {
        trimmingCharacters(in: .whitespacesAndNewlines).isEmpty
    }
}

print("   ".isBlank, "hi".isBlank)
// prints: true false
```

但扩展外部类型并遵循你自己的协议，叫“追溯性遵循”。Swift 6 会提高这类做法的检查强度，避免两个模块各自给同一个外部类型加上冲突的实现。真的需要时，可以使用 `@retroactive` 明确表达意图：

```swift
// 假设 Marked 由另一个模块提供，而 String 来自标准库：
extension String: @retroactive Marked {}
```

这不是鼓励你到处给标准库加协议，而是让这种做法必须被看见。

## 21.6 嵌套类型：把相关名字收进命名空间

类型可以嵌套在另一个类型里：

```swift
struct Store {
    struct Item {
        let name: String
    }

    enum State {
        case loading, loaded, failed
    }

    var state: State = .loading
}

let item = Store.Item(name: "Book")
print(item.name, Store.State.loaded)
// prints: Book loaded
```

嵌套类型适合“只在这个类型内部有意义”的概念。它的作用域更窄，名字不容易污染全局。

嵌套类型可以被外部访问，只要访问级别允许：

```swift
extension Store.Item {
    var displayName: String { name.uppercased() }
}
print(item.displayName)
// prints: BOOK
```

如果嵌套类型只服务内部实现，就把它声明为 `private` 或 `fileprivate`，让 API 表面保持干净。

## 21.7 扩展不是万能补丁

扩展适合添加与类型职责自然相关的能力。不适合：

- 把所有工具函数都挂到 `String`、`Int` 上。
- 用扩展绕过原类型的设计限制。
- 在多个文件里反复扩展同一个类型，让行为难以追踪。
- 给外部类型添加与命名空间冲突的高频名字，例如 `String.count` 已有含义时再定义 `countText` 也要慎重。

判断标准很简单：**这个能力是不是该类型天然应该拥有的？** 如果答案是“它只是碰巧能用上”，那它可能属于一个独立函数或独立类型。

## 21.8 本章小结

| 能力 | 说明 |
| --- | --- |
| 计算属性 | 可以添加，不能添加存储属性 |
| 方法 | 可以添加实例方法和类型方法 |
| 初始化器 | 值类型可加，类只能加便利初始化器 |
| 下标 | 可以添加自定义下标 |
| 协议实现 | 可以将遵循拆分到扩展 |
| 条件扩展 | 用 `where` 约束泛型能力 |
| 嵌套类型 | 把相关类型收进外层类型命名空间 |

## 21.9 本章易错点速查

| 易错点 | 正确理解 |
| --- | --- |
| 在扩展里添加存储属性 | 不允许；只能加计算属性 |
| 以为扩展会改变类型身份 | 扩展只增加能力，类型仍是原类型 |
| 在类扩展里定义指定初始化器 | 类扩展只能添加便利初始化器 |
| 给外部类型随意加协议 | 可能产生追溯性遵循冲突，必要时使用 `@retroactive` |
| 把扩展当杂物间 | 只添加与类型职责相关的功能 |
| 忽略嵌套类型的访问控制 | 内部实现用 `private` 收窄 |

## 21.10 下章预告

下一章讲协议。它是 Swift 抽象能力的中心：描述“能做什么”，而不是“是什么”。你还会遇到关联类型、协议扩展和 `@resultBuilder`，这些是构建 DSL 和 SwiftUI 风格接口的关键积木。
