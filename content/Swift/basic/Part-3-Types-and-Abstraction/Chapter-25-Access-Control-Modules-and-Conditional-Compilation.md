+++
title = "第25章 访问控制、模块与条件编译"
weight = 250
date = "2026-09-14T22:30:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 第二十五章：访问控制、模块与条件编译

> 代码长大了，边界就比功能更重要。访问控制决定“谁能看见什么”，模块决定“哪些类型属于同一个发布单元”，条件编译决定“哪些代码在哪些平台参与构建”。这些规则没有花哨效果，却直接影响 API 是否稳定、二进制是否兼容。

## 25.1 五级访问控制

Swift 的访问级别从大到小：

| 级别 | 可见范围 |
| --- | --- |
| `open` | 模块内外可见，且允许继承和重写 |
| `public` | 模块内外可见，但不允许模块外继承和重写 |
| `package` | 同一个 Swift 包内可见 |
| `internal` | 当前模块内可见，默认级别 |
| `fileprivate` | 当前文件内可见 |
| `private` | 当前声明及其扩展内可见 |

```swift
public struct API {
    public var name: String
    internal var cache: [String: Int] = [:]
    private var secret = "hidden"

    public init(name: String) {
        self.name = name
    }
}
```

`open` 只适用于类和类成员，不能用于结构体或枚举。`public` 暴露给模块外，但库作者可以决定不允许被继承。两者的分界只有在**跨模块**时才看得出来，所以先看一组"能继承、能重写、不能重写"的对照：

```swift
open class Base {
    open func run() -> String { "base" }        // 模块外也能继承并重写
    public final func id() -> String { "id" }   // 能看见，但谁都别想重写
}

class Sub: Base {
    override func run() -> String { "sub" }
}

print(Sub().run(), Sub().id())
// prints: sub id
```

`public` 是"能看见"，`open` 是"能看见，还允许你在自己模块里动手改"，`final` 是"到此为止"。同一个模块内部 `public` 本来也能重写，所以上面这段代码体现不出差别——真正的差别出现在你把这段代码编译成库、再被另一个模块使用时：`public` 的 `run` 会被拒之门外，`open` 的才行。

## 25.2 `private`、`fileprivate` 和扩展

`private` 默认限定在声明及其同文件的扩展中：

```swift
struct Counter {
    private var value = 0
}

extension Counter {
    mutating func increment() {
        value += 1
    }
}
```

同文件扩展能访问 `private`——注意这句话的主语是"**同一个类型的**扩展"。另一个类型即使和它住在同一个文件里，也拿不到 `private` 成员，这时候要用 `fileprivate`：

```swift
struct Vault {
    private var secret = 1
    fileprivate var shared = 2
}

struct Inspector {
    func peek(_ vault: Vault) -> Int {
        // vault.secret   // 编译错误，见下面的报错
        vault.shared      // fileprivate：同一文件内都可见
    }
}

print(Inspector().peek(Vault()))
// prints: 2
```

把那行注释打开，编译器会说：

```text
error: 'secret' is inaccessible due to 'private' protection level
```

一句话记法：`private` 是"自己家的人"，`fileprivate` 是"同一个屋檐下的邻居"。跨文件扩展就都访问不到了；如果确实需要跨文件共享，只能把成员提升到 `internal`，或把相关代码放进同一个文件。

允许外部读、内部写时，用 `private(set)`：

```swift
public struct LoginState {
    public private(set) var attempts = 0

    public mutating func recordFailure() {
        attempts += 1
    }
}
```

外部看到 `attempts` 可读，但不能直接修改。

## 25.3 模块与包

模块是编译和导入的边界。一个 Swift 包可以包含多个目标，每个目标通常就是一个模块：

```swift
// Package.swift
let package = Package(
    name: "App",
    products: [.library(name: "Core", targets: ["Core"])],
    targets: [
        .target(name: "Core"),
        .executableTarget(name: "App", dependencies: ["Core"])
    ]
)
```

模块边界和访问控制息息相关：

- `internal` 在模块内可见，跨模块不可见。
- `package` 在同一个包内的不同模块间可见。
- `public` 和 `open` 才能被包外使用者看到。
- 测试可以用 `@testable import` 访问以测试为目标的 `internal` 成员。

不要让所有东西都变成 `public`。公开面越大，未来修改时越容易被兼容性绑住。

## 25.4 条件编译

`#if` 让代码只在满足条件时参与编译：

```swift
#if os(macOS)
print("桌面平台")
#elseif os(iOS)
print("移动平台")
#else
print("其他平台")
#endif
// 在 macOS 上会打印：桌面平台
```

常用条件包括：

| 条件 | 含义 |
| --- | --- |
| `os(macOS)` | 目标操作系统 |
| `arch(arm64)` | 目标 CPU 架构 |
| `swift(>=6.0)` | Swift 版本 |
| `canImport(Foundation)` | 是否可导入模块 |
| `DEBUG` | 自定义编译标志 |
| `targetEnvironment(simulator)` | 是否模拟器环境 |

可以通过 `-D DEBUG` 传入自定义标志：

```swift
#if DEBUG
print("调试构建")
#else
print("发布构建")
#endif
// 常见的两种输出：调试构建 或 发布构建
```

条件编译不是普通 `if`。不满足条件的代码不会被类型检查，也不会进入二进制。

## 25.5 可用性检查

有些 API 只在新系统版本可用。声明时用 `@available`：

```swift
@available(macOS 13, *)
func useNewAPI() {
    print("新系统才有的 API")
}
```

运行时判断系统版本用 `#available`：

```swift
if #available(macOS 13, *) {
    print("使用新 API")
} else {
    print("使用旧方案")
}
// 在 macOS 13 及以上打印：使用新 API
```

反向判断用 `#unavailable`：

```swift
if #unavailable(macOS 13) {
    print("系统版本较低")
} else {
    print("系统版本满足要求")
}
// 在 macOS 13 及以上打印：系统版本满足要求
```

还可以标记废弃或不可用：

```swift
@available(*, deprecated, message: "改用 newLoad()")
func oldLoad() {}

@available(*, unavailable, message: "该平台不支持")
func unavailableFeature() {}
```

`@available` 是给编译器和调用者的兼容性契约，尤其适合库的长期维护。

## 25.6 模块选择器

当两个模块导出了同名符号，模块选择器可以明确指定来源：

```swift
import Foundation

let date = Foundation::Date()
print(date.timeIntervalSince1970 > 0)
// prints: true
```

这里的 `Foundation::Date` 就是模块选择器。它的典型用途是消除同名类型、函数或扩展之间的歧义，而不是日常替代普通 `import`。能否使用取决于工具链和模块导出方式。

## 25.7 Objective-C 互操作标记

在 Apple 平台上，`@objc` 会把 Swift 声明暴露给 Objective-C 运行时；`#selector` 可以取得方法选择器：

```swift
import Foundation

@objcMembers
final class TimerBridge: NSObject {
    func fire() {
        print("触发")
    }
}

let selector = #selector(TimerBridge.fire)
print(selector)
// prints: fire
```

注意两点：`#selector` 指向的方法必须对 Objective-C 可见；`@objcMembers` 会给类型及其成员批量加 `@objc`，但并不是所有 Swift 特性都能暴露给 Objective-C。跨平台项目要把这类代码隔离在 Apple 平台专用模块中，而不是让整个代码库都背上运行时约束。

如果你需要的是 Objective-C 风格的键路径字符串，`#keyPath` 仍然存在；新代码通常优先使用 Swift 的键路径表达式 `\Type.property`。

```swift
import Foundation

final class Profile: NSObject {
    @objc dynamic var name = "Mia"
}

print(#keyPath(Profile.name))
// prints: name
```

## 25.8 导入的形式

除了整体 `import Foundation`，还可以只导入需要的声明：

```swift
import struct Foundation.Date
import class Foundation.NSString
```

精确导入能减少名字冲突，也让依赖关系更清楚。但它不会改变可见性规则：被导入的声明仍然要满足自己的访问级别。

## 25.9 本章小结

| 主题 | 关键结论 |
| --- | --- |
| `open` | 跨模块可见且可继承、重写 |
| `public` | 跨模块可见，但不可跨模块继承 |
| `package` | 同一个包内跨模块可见 |
| `internal` | 模块内可见，默认级别 |
| `fileprivate` | 文件内可见 |
| `private` | 声明及同文件扩展内可见 |
| `#if` | 按平台、架构、版本或自定义标志编译 |
| `@available` | 声明可用性、废弃和不可用 |
| `#available` | 运行时检查系统版本 |
| 模块选择器 | 用 `Module::Name` 消除同名歧义 |

## 25.10 本章易错点速查

| 易错点 | 正确理解 |
| --- | --- |
| 把 `public` 当成 `open` | `public` 不允许模块外继承和重写 |
| 用 `fileprivate` 共享跨文件成员 | 它只在当前文件内可见 |
| 忘记写 `public init` | 外部仍然无法创建你的类型 |
| 在条件编译里写普通逻辑 | 条件不满足的代码根本不参与编译 |
| 在运行时才检查 API 可用性 | 同时考虑 `@available` 与 `#available` |
| 用模块选择器替代设计清晰的命名 | 它主要解决同名歧义 |

## 25.11 下章预告

下一章讲宏。宏不是运行时魔法，而是编译器在编译期帮你生成代码的正式机制。你会看到 `#` 开头的自由宏、`@` 开头的附着宏，以及 Swift Testing、SwiftUI 和 Observation 中大量使用的宏到底如何工作。
