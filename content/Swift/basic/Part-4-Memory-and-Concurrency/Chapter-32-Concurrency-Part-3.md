+++
title = "第32章 并发（三）：Approachable Concurrency 与迁移"
weight = 320
date = "2026-09-14T22:30:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 第三十二章：并发（三）：Approachable Concurrency 与迁移

> 并发安全最难的不是新项目，而是把已有代码从“能跑”搬到“编译器能证明安全”。Swift 6 提供了严格检查，也提供了 Approachable Concurrency 这套更顺手的默认规则。迁移的关键不是一次性改完，而是让边界逐步清楚。

## 32.1 Swift 6 语言模式：严格并发检查

Swift 6 模式把很多数据竞争从运行时警告提升为编译错误。开启方式有两种：

```swift
// Package.swift
let package = Package(
    name: "App",
    targets: [
        .executableTarget(name: "App", swiftSettings: [.swiftLanguageMode(.v6)])
    ]
)
```

Xcode 中也可以把目标的 Swift Language Version 设为 6。开启后，全局可变状态、跨隔离域捕获、非 `Sendable` 类型传递都会受到更严格的检查。

最能说明问题的例子是全局可变状态。下面这段代码在 Swift 5 模式下只是“有点可疑”，在 Swift 6 模式下根本过不了编译：

```swift
var counter = 0          // ❌ 没有隔离保护的全局可变状态

func bump() -> Int {
    counter += 1
    return counter
}
```

```text
error: var 'counter' is not concurrency-safe because it is nonisolated global shared mutable state
```

三种常见修法，代价各不相同：

```swift
@MainActor var mainCounter = 0        // 方案一：交给主 actor 串行化，访问要 await 或本来就在主 actor

nonisolated(unsafe) var unsafeCounter = 0   // 方案二：人工担保“我保证安全”，编译器不再管你

actor Counter {                        // 方案三：把状态关进 actor，推荐用于真的要共享的可变状态
    private var value = 0
    func bump() -> Int {
        value += 1
        return value
    }
}
```

方案二一定要慎用：它不是“让代码变安全”，而是“让编译器闭嘴”。真正安全的做法是方案一或方案三。

迁移时不要一开始就把整个项目切成 6 模式。先把模块边界整理清楚，再一个模块一个模块推进，效果通常更好。

## 32.2 默认隔离：让 UI 代码少写 `@MainActor`

SwiftPM 支持把默认隔离设为 `MainActor`：

```swift
.executableTarget(
    name: "App",
    swiftSettings: [
        .defaultIsolation(MainActor.self),
        .enableUpcomingFeature("ApproachableConcurrency")
    ]
)
```

这样，目标里未显式标注隔离的代码默认属于主 actor，适合以 UI 为主的项目。底层库、服务器代码或高性能计算目标不该盲目套用这套默认值，它们通常更适合显式设计隔离边界。

## 32.3 `nonisolated(nonsending)`：不隔离，但留在调用者身边

`nonisolated` 函数不属于某个 actor，但不代表它一定会跳走。Approachable Concurrency 引入了 `nonisolated(nonsending)`，让异步函数默认在调用者的执行上下文继续运行：

```swift
nonisolated(nonsending)
func summarize(_ values: [Int]) async -> Int {
    values.reduce(0, +)
}

@main
struct App {
    @MainActor
    static func main() async {
        // 调用者已经在主 actor 上，summarize 不会切到别的线程去
        print(await summarize([1, 2, 3]))
        // prints: 6
    }
}
```

这对“只是想写异步语法，不想额外换执行器”的代码很友好：`summarize` 里读到的隔离状态仍然属于调用者，不会莫名其妙跳到后台线程，也就不会突然冒出“跨隔离域访问”的编译错误。

它也减少无意义的上下文切换。对比一下：普通 `nonisolated` 异步函数在旧语义下可能被调度到全局并发执行器上，而 `nonisolated(nonsending)` 明确表示“我留在原地”。

## 32.4 `@concurrent`：明确要求并发执行

如果函数确实应该离开当前 actor，在全局并发执行器上运行，就使用 `@concurrent`：

```swift
@concurrent
func heavyWork() async -> Int {
    (0..<1_000).reduce(0, +)
}

@main
struct App {
    static func main() async {
        // heavyWork 会离开主 actor，在全局并发执行器上算，算完再把结果送回来
        print(await heavyWork())
        // prints: 499500
    }
}
```

`@concurrent` 和 `nonisolated(nonsending)` 是一对相反的选择：前者说“请换个执行器去跑”，后者说“就留在调用者这里”。写之前先问自己一句——这段代码是在等 I/O 还是在烧 CPU？烧 CPU 的才值得 `@concurrent`。

它也**不会凭空让代码安全**：函数参数和返回值仍然要满足 `Sendable`，函数体里也不能随便访问别的隔离域状态。

## 32.5 `sending`：把值的所有权安全送走

`sending` 用在返回值和参数上，表示这个值可以安全地转移到另一个隔离域：

```swift
func makeValues() -> sending [Int] {
    [1, 2, 3]
}

@main
struct App {
    static func main() async {
        let task = Task { makeValues() }
        print(await task.value)
        // prints: [1, 2, 3]
    }
}
```

`sending` 的重点是**所有权转移**，而不是“随便共享”。当一个值被送走后，原隔离域不应该继续持有并使用它——编译器会检查这一点。典型的适用场景是：在任务之间搬运一个内部可变、但对整个程序来说只有一份的值。

## 32.6 迁移策略：从警告到错误

一个稳妥的迁移顺序：

1. 先开启严格并发警告，不急着把它们全部变成错误。
2. 整理全局可变状态：能改成 `let` 的就改，需要共享的包进 actor 或 `@MainActor`。
3. 给跨任务传递的数据补上 `Sendable`，把可变类改造成不可变模型或 actor。
4. 检查闭包捕获列表，尤其是逃逸闭包、任务和回调。
5. 对外部旧库使用 `@preconcurrency import`，把风险限制在边界处。
6. 最后再切到 Swift 6 语言模式，让编译器持续守住规则。

常用迁移工具：

| 工具 | 用途 |
| --- | --- |
| `@preconcurrency import` | 暂时容忍旧模块的并发标注缺失 |
| `nonisolated(unsafe)` | 明确声明“这里由我人工保证安全” |
| `MainActor.assumeIsolated` | 确认当前已在主 actor，安全转换隔离 |
| `@unchecked Sendable` | 人工承诺类型可以跨域，风险自担 |
| `-strict-concurrency=complete` | 更严格的并发诊断 |

这些工具是过渡桥梁，不是终局。用得越多，说明需要治理的边界越多。

## 32.7 数据竞争安全不是“没有并发”

数据竞争安全和“单线程”不是一回事。actor、`Sendable`、隔离域和任务让并发仍然可用，只是把共享状态变成需要明确建模的东西：

- 值在隔离域之间传递时，所有权和可变性必须清楚。
- 共享状态必须由一个隔离域保护。
- UI 状态尽量留在 `@MainActor`。
- 纯计算和 I/O 可以在合适的执行器上运行。
- 跨域接口尽量传递不可变快照，而不是可变对象引用。

当编译器开始抱怨，不要立刻用 `@unchecked` 把它按下去。先问：这个状态到底该归谁管？

## 32.8 本章小结

| 特性 | 含义 |
| --- | --- |
| Swift 6 模式 | 更严格的数据竞争检查 |
| 默认 `MainActor` 隔离 | 让 UI 目标少写隔离标注 |
| `nonisolated(nonsending)` | 不隔离但留在调用者上下文 |
| `@concurrent` | 明确要求并发执行 |
| `sending` | 安全转移值所有权 |
| `@preconcurrency` | 兼容未标注并发的旧代码 |
| `nonisolated(unsafe)` | 人工承担同步安全责任 |

## 32.9 本章易错点速查

| 易错点 | 正确理解 |
| --- | --- |
| 一上来就把整个项目切成 Swift 6 | 容易产生大量难定位错误，建议分模块迁移 |
| 给所有目标都默认 `MainActor` | 只有 UI 型目标通常适合 |
| 用 `@concurrent` 解决所有性能问题 | 并发不能修复算法和 I/O 结构 |
| 用 `@unchecked Sendable` 消除报错 | 这是承诺，不是修复 |
| 认为 `sending` 等于共享 | 它表达所有权转移 |
| 把 `nonisolated` 理解成“永不在主线程” | 它只表示不归属于 actor 隔离 |

## 32.10 下章预告

第五篇开始转向工程与质量：SwiftPM 进阶、资源、依赖、C 互操作、测试、调试和性能。到这一步，语言能力已经够用，接下来要把它们组织成可维护的项目。
