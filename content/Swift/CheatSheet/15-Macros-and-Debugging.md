+++
title = "15 宏与调试"
linkTitle = "15 宏与调试"
weight = 150
date = "2026-09-16T11:00:00+08:00"
type = "docs"
description = "宏的两种形态与写法、@ 属性全表、怎么看宏展开，以及断言家族与调试输出的全部选项"
isCJKLanguage = true
draft = false
+++

# 15 宏与调试

## 宏：编译期帮你写代码

宏不是运行期的魔法，它是**编译器在编译你的代码时，调用另一段代码生成源代码**。所以它有几个和函数完全不同的性质：

- 宏在编译期展开，运行期没有任何额外开销；
- 宏的声明和实现**是分开的**：声明告诉编译器"这个宏叫什么、能长在哪里"，实现在一个单独的编译期插件里；
- 宏只能"生成代码"，不能"猜"运行期的值——`#stringify(a + b)` 能拿到 `"a + b"` 这段源码，但拿不到 `a + b` 的值。

### 两种形态

| 形态 | 长这样 | 名字风格 | 例子 |
| --- | --- | --- | --- |
| 自由宏（freestanding） | `#名字(...)` | 小驼峰 | `#stringify(x)`、`#function`、`#warning("...")` |
| 附加宏（attached） | `@名字` | 大驼峰 | `@Observable`、`@Test`、`@OptionSet` |

📘 官方对宏的完整介绍在 [The Swift Programming Language · Macros](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/macros/)。

💭 顺带澄清一个常见误会：`#file`、`#line`、`#function`、`#warning`、`#error` 这些以 `#` 开头的东西，官方文档从 Swift 5.9 起把它们算作**标准库提供的自由宏**（见 [01 起步]({{< relref "01-Quickstart.md" >}}) 里那张表）。而 `#if`、`#available`、`#selector`、`#keyPath` 不是宏，它们是编译器自带的语法。

### 先用别人写好的宏

不需要自己写，也能立刻享受宏的好处。下面这个用的是 Observation 模块里的 `@Observable`，实测跑得通：

```swift
import Observation

@Observable
final class Model {
    var count = 0
    var name = "x"
}

let model = Model()
model.count += 1
print(model.count, model.name)
// prints: 1 x
```

这几行在编译期被展开成了一大段代码：一个 `ObservationRegistrar`、两个 `access` / `withMutation` 方法，以及每个属性上的 `@ObservationTracked`。手写这些很容易漏，所以这类"必须保持一致"的样板代码正是宏的主场。

🚧 `Foundation` 的 `#Predicate` 也是宏，但它要借助 Xcode 附带的 `FoundationMacros` 插件。只装 Command Line Tools 的机器上会报 `plugin for module 'FoundationMacros' not found`——这是环境问题，不是你的代码写错了。

### 想知道宏到底生成了什么

让编译器把展开结果打出来：

```console
$ swiftc -typecheck -Xfrontend -dump-macro-expansions demo.swift
@__swiftmacro_4demo5Model10ObservablefMm_.swift
------------------------------
@ObservationIgnored private let _$observationRegistrar = Observation.ObservationRegistrar()

internal nonisolated func access<Member>(
  keyPath: KeyPath<Model, Member>
) {
  _$observationRegistrar.access(self, keyPath: keyPath)
}
```

🔥 宏出错时，这条命令几乎是唯一能让你看懂现场的工具：报错位置常常落在展开出来的代码里，而不是你写的那一行。

### 自己写一个宏

先建骨架，模板里自带一个能跑的 `#stringify`：

```console
$ swift package init --type macro
```

一个宏要三份东西，分别住在三个地方：

| 角色 | 放在哪 | 长什么样 |
| --- | --- | --- |
| 声明 | 普通库 target | `@freestanding(expression) public macro ... = #externalMacro(module:type:)` |
| 实现 | `.macro` target（编译期插件） | 一个遵守 `ExpressionMacro` / `MemberMacro` … 的结构体 |
| 注册 | 插件的 `@main` 类型 | `CompilerPlugin.providingMacros` 数组 |

先看一个自由宏。声明部分（放在能被 `import` 的库里）：

```swift
@freestanding(expression)
public macro stringify<T>(_ value: T) -> (T, String) =
    #externalMacro(module: "MacroDemoMacros", type: "StringifyMacro")
```

实现在 `.macro` target 里，干的事就是"把表达式和它的源码一起返回"：

```swift
import SwiftCompilerPlugin
import SwiftSyntax
import SwiftSyntaxBuilder
import SwiftSyntaxMacros

public struct StringifyMacro: ExpressionMacro {
    public static func expansion(
        of node: some FreestandingMacroExpansionSyntax,
        in context: some MacroExpansionContext
    ) -> ExprSyntax {
        guard let argument = node.arguments.first?.expression else {
            fatalError("宏没拿到参数")
        }
        return "(\(argument), \(literal: argument.description))"
    }
}
```

再补一个附加宏。附加宏是加在**类型或成员身上**的，角色写在声明前面：

```swift
@attached(member, names: named(kind))
public macro Kind() = #externalMacro(module: "MacroDemoMacros", type: "KindMacro")
```

```swift
import SwiftSyntax
import SwiftSyntaxMacros

public struct KindMacro: MemberMacro {
    public static func expansion(
        of node: AttributeSyntax,
        providingMembersOf declaration: some DeclGroupSyntax,
        in context: some MacroExpansionContext
    ) throws -> [DeclSyntax] {
        ["static var kind: String { String(describing: Self.self) }"]
    }
}
```

最后把两个宏登记进插件，并写一个调用方：

```swift
import SwiftCompilerPlugin
import SwiftSyntaxMacros

@main
struct MacroDemoPlugin: CompilerPlugin {
    let providingMacros: [Macro.Type] = [
        StringifyMacro.self,
        KindMacro.self,
    ]
}
```

```swift
import MacroDemo

let a = 17
let b = 25
let (result, code) = #stringify(a + b)
print("The value \(result) was produced by the code \"\(code)\"")
// prints: The value 42 was produced by the code "a + b"

@Kind
struct Config { var name = "默认"; var retries = 3 }

print(Config.kind, Config().name)
// prints: Config 默认
```

🔥 上面这段是**实测跑过的**：`swift package init --type macro` 建包、把两个宏登记进 `providingMacros`、`swift run` 之后，输出就是注释里那两行。宏包首次构建要从 [swift-syntax](https://github.com/swiftlang/swift-syntax) 拉一堆源码，慢是正常的。

### 常见的角色

| 角色 | 加在哪 | 干什么 |
| --- | --- | --- |
| `@freestanding(expression)` | 表达式位置 | 产出一个值，例如 `#stringify(x)` |
| `@freestanding(declaration)` | 声明位置 | 产出一段声明 |
| `@attached(peer)` | 类型 / 成员旁边 | 在旁边补一个新声明 |
| `@attached(member)` | 类型里面 | 往里加成员（`@Observable` 加的注册器就在这里） |
| `@attached(accessor)` | 属性上 | 给属性加 `get` / `set` |
| `@attached(extension, conformances:)` | 类型上 | 加一个遵守协议的扩展 |

⚠️ 宏**不能**读取自己声明之外的运行期状态，也**不能**凭空发明类型：它只能根据你写下的语法节点生成新代码。所以"宏能做什么"的边界很清晰——凡是需要"模板化的样板代码"，它都行；凡是需要"运行期才知道的信息"，它就不行。

## 断言家族：什么时候该崩

四种"出事了"的写法，区别只在**在哪种构建下仍然生效**：

| 写法 | 用于 | `-Onone`（调试） | `-O`（发布） | `-Ounchecked` |
| --- | --- | --- | --- | --- |
| `assert(_:_:)` | 开发者自检，比如"这个数组不该是空的" | ✅ 生效 | ❌ 被去掉 | ❌ 被去掉 |
| `assertionFailure(_:)` | 走到这里就说明逻辑错了 | ✅ 生效 | ❌ 被去掉 | ⚠️ 实测仍会崩 |
| `precondition(_:_:)` | 调用方的错，比如参数越界 | ✅ 生效 | ✅ 生效 | ❌ 被去掉 |
| `preconditionFailure(_:)` | 调用方给的组合不可能成立 | ✅ 生效 | ✅ 生效（不再打印消息） | ✅ 生效（不再打印消息） |
| `fatalError(_:)` | 彻底没救了，必须停下 | ✅ 生效 | ✅ 生效 | ✅ 生效 |

```swift
func average(_ numbers: [Int]) -> Double {
    precondition(!numbers.isEmpty, "空数组没有平均值")
    return Double(numbers.reduce(0, +)) / Double(numbers.count)
}

print(average([1, 2, 3]))
// prints: 2.0
```

实测的崩溃长这样：

```text
$ ./demo
demo/demo.swift:2: Precondition failed: 空数组没有平均值
```

格式固定为 `<模块名>/<文件名>.swift:<行号>: <种类>: <消息>`。种类只有三种：`assert` 给 `Assertion failed`，`precondition` 给 `Precondition failed`，`assertionFailure` 与 `fatalError`、`preconditionFailure` 给 `Fatal error`。文件与行号取自 `#fileID` / `#line`。

⚠️ 第三条是最容易写错的：**`assert` 在发布版本里会被整个删掉**，所以断言表达式里不要写有副作用的东西——`assert(cleanup())` 在 debug 里会清理，在 release 里不会，这种 bug 只在发布版本出现。

⚠️ `-Ounchecked` 是把安全带剪掉：连数组越界都不再检查。实测 `let a = [1, 2, 3]; print(a[5])` 在 `-Onone` 下报 `Fatal error: Index out of range`，在 `-Ounchecked` 下**不报错**、直接给你一段垃圾数据。它只适合"性能优先级压过一切、且已经压测过"的场景。

💭 选哪个的一句话版本：**自己的逻辑错了用 `assert`，别人传错了用 `precondition`，世界末日用 `fatalError`。** 想要"文档里写明的、必须成立的契约"，就用 `precondition`——它在发布版本里还拦得住。

## 打印与调试输出

同一个结构体，四种输出方式看到的东西不一样：

```swift
struct Point { var x = 1; var y = 2 }

print(Point())
// prints: Point(x: 1, y: 2)
print(String(describing: Point()))
// prints: Point(x: 1, y: 2)
```

同一个值，四种写法打出来的东西并不一样（下面 `demo` 是模块名，也就是你的 target 名）：

```text
$ swift demo.swift
Point(x: 1, y: 2)            ← print / String(describing:)
demo.Point(x: 1, y: 2)       ← debugPrint / String(reflecting:)，会把模块名带上
▿ demo.Point                 ← dump：递归展开层级
  - x: 1
  - y: 2
```

先把四种 `print` 的区别记清楚，就不会再说"`print` 怎么打不出类型名"：

| 写法 | 看什么 | 特点 |
| --- | --- | --- |
| `print(x)` | `CustomStringConvertible.description` | 面向用户，最漂亮 |
| `debugPrint(x)` | `CustomDebugStringConvertible.debugDescription` | 面向调试，会带模块名、给字符串加引号 |
| `dump(x)` | 反射出来的 `Mirror` 树 | 递归展开层级，适合看嵌套结构 |
| `String(reflecting: x)` | 同上，但产出字符串 | 想拼日志时用它 |

想让自己的类型输出好看，实现对应协议就行：

```swift
struct Money: CustomStringConvertible, CustomDebugStringConvertible {
    var cents: Int
    var description: String { "¥\(Double(cents) / 100)" }
    var debugDescription: String { "Money(cents: \(cents))" }
}

let m = Money(cents: 1250)
print(m)
// prints: ¥12.5
debugPrint(m)
// prints: Money(cents: 1250)
```

💭 小程序里 `print` 就够；工具链和库代码还是用 `os.Logger` / `swift-log`（见 [13 工具链与工程]({{< relref "13-Tooling.md" >}})），能分级、能过滤、发布版本里也能优雅地关掉。

## 调试时常用的几件小事

| 想干什么 | 怎么做 |
| --- | --- |
| 让编译器把宏展开打出来 | `swiftc -typecheck -Xfrontend -dump-macro-expansions 文件.swift` |
| 让警告直接变成错误 | `swiftc -warnings-as-errors`，CI 上必备 |
| 只做类型检查（最快） | `swiftc -typecheck 文件.swift` ⚠️ 少数诊断它看不到，见 [13 工具链]({{< relref "13-Tooling.md" >}}) |
| 构造一个"绝对不会走到"的分支 | `fatalError("分支不该到这里")` |
| 主动产生编译警告 / 错误 | `#warning("...")`、`#error("...")` |
| 单测里断言并解包 | `try #require(...)`（Swift Testing）、`XCTUnwrap`（XCTest） |

## 属性（`@`）速查

`#` 是"编译期的**表达式 / 指令**"，`@` 是"贴在声明上的**开关**"。Swift 的属性不多，一张表能装下：

### 声明与可用性

| 属性 | 贴在 | 作用 |
| --- | --- | --- |
| `@main` | 类型上 | 指定程序入口（`static func main()` 或 SwiftUI 的 `App`） |
| `@available(...)` | 任意声明 | 版本门槛：`@available(macOS 13, *)`、`@available(*, deprecated, message: "…")` |
| `@discardableResult` | 函数上 | 忽略返回值时不再报警告 |
| `@warn_unqualified_access` | 成员上 | 不写 `self.` / 类型名就调用它时警告，专治"同名成员打架" |
| `@testable import X` | `import` 上 | 让测试代码能看见 `internal` 成员 |

```swift
import Foundation

@available(macOS 13, *)
func newOnly() -> Int { 1 }
print(newOnly())
// prints: 1

struct Hidden {
    @warn_unqualified_access func value() -> Int { 1 }
    static func value() -> Int { 2 }
}
print(Hidden().value(), Hidden.value())
// prints: 1 2
```

### 性能与 ABI

| 属性 | 贴在 | 作用 |
| --- | --- | --- |
| `@inline(__always)` / `@inline(never)` | 函数上 | 建议内联 / 禁止内联（只是建议，编译器仍可无视） |
| `@inlinable` | `public` 函数上 | 把实现体一起暴露给调用方，跨模块也能优化 🔥 |
| `@usableFromInline` | `internal` 声明上 | 给 `@inlinable` 代码开一扇内部的门 |
| `@frozen` | `public` 枚举 / 结构体上 | 承诺"以后不再加 case / 改字段"，换来调用方更好的优化 |
| `@backDeployed(before:)` | `public` 函数上 | 新 API 在老系统上也能用：实现被复制进 App |

⚠️ 两个实测会挡路的规矩：

| 你写的 | 报什么 |
| --- | --- |
| 给非 public 枚举加 `@frozen` | `warning: @frozen has no effect on non-public enums`（只是没效果） |
| 给 `internal` 函数加 `@backDeployed` | `error: '@backDeployed' may not be used on internal declarations` |

### 并发与互操作

| 属性 | 贴在 | 作用 | 详见 |
| --- | --- | --- | --- |
| `@MainActor` / `@globalActor` | 类型 / 函数 / 属性 | 把它钉在某个执行器上 | [09 并发]({{< relref "09-Error-Handling-and-Concurrency.md" >}}) |
| `@Sendable` | 闭包 / 函数类型 | 允许跨并发域传递 | [09 并发]({{< relref "09-Error-Handling-and-Concurrency.md" >}}) |
| `@unchecked Sendable` | 类上 | "我保证它是线程安全的"，编译器不再检查 | [09 并发]({{< relref "09-Error-Handling-and-Concurrency.md" >}}) |
| `@preconcurrency` | `import` / 协议 / 声明 | 给还没适配并发检查的老代码降一档 | [09 并发]({{< relref "09-Error-Handling-and-Concurrency.md" >}}) |
| `@objc` / `@objcMembers` / `@nonobjc` | 类 / 成员 | 暴露给 Objective-C，或者反过来拦住 | [14 互操作]({{< relref "14-Type-Casting-and-Interop.md" >}}) |
| `@retroactive` | 扩展上 | 声明"这是在给别人的类型补协议"，避免重复遵循冲突 | 见下 |

`@retroactive` 是 Swift 6 新加的礼貌用语。标准库和你的模块都管不着的两个类型要凑一起时，编译器会提醒你"这可能是别人也在做的事"，明确写出来就不再抱怨：

```swift
extension Int: @retroactive Identifiable {   // Int 与 Identifiable 都不是本模块的
    public var id: Int { self }
}
print(5.id)
// prints: 5
```

### 扩展语言能力

| 属性 | 贴在 | 作用 | 详见 |
| --- | --- | --- | --- |
| `@propertyWrapper` | 类型上 | 做出 `@Published`、`@State` 那类东西 | [07 自定义类型]({{< relref "07-Custom-Types.md" >}}) |
| `@resultBuilder` | 类型上 | 做出 SwiftUI 那种"花括号里写列表"的 DSL | [12 语法糖]({{< relref "12-Syntax-Sugar.md" >}}) |
| `@freestanding` / `@attached` | 宏声明上 | 声明宏的角色 | 本章上文 |
| `@dynamicMemberLookup` | 类型上 | 让 `obj.任意名字` 走 `subscript(dynamicMember:)` | [07 自定义类型]({{< relref "07-Custom-Types.md" >}}) |
| `@dynamicCallable` | 类型上 | 让实例能像函数一样被调用 | 🔍 用得上再查 |
| `@autoclosure` / `@escaping` | 参数上 | 控制求值时机与逃逸 | [05 函数与闭包]({{< relref "05-Functions-and-Closures.md" >}}) |
| `@Observable` / `@ObservationIgnored` | 类型 / 属性上 | 让类型可被观察；让某个属性**不**参与观察 | [11 标准库]({{< relref "11-Standard-Library.md" >}}) |

💭 **下划线开头的属性（`@_spi`、`@_exported`、`@_disfavoredOverload`、`@_specialize`）都是非正式 API**：它们没有稳定性承诺，工具链升级就可能导致行为变化。写库的时候尽量避开，实在需要就在注释里写明依赖哪个版本。

## 陷阱速查

| 陷阱 | 说明 |
| --- | --- |
| 断言里有副作用 | `assert` 在 `-O` 下会被删掉，副作用跟着消失 |
| 用 `assert` 校验用户输入 | 发布版本里它不在了，用 `precondition` 或正经的错误处理 |
| 以为 `fatalError` 会被优化掉 | 它永远生效，是"我就是不跑了"的意思 |
| 用 `-Ounchecked` 换性能 | 越界检查也没了，实测会安静地给你垃圾数据 |
| 把 `@frozen` 写在非 public 的类型上 | 编译器只给一句 `@frozen has no effect on non-public enums`，什么都没发生 |
| 以为 `@inline(__always)` 一定内联 | 它是建议不是命令，跨模块还要配合 `@inlinable` 才有意义 |
| 忘了写 `@retroactive` | 两个"外来"类型凑一起时，编译器会为重复遵循的隐患提醒你 |
| 把 `@objc` 那种"有运行期代价"的假设套到宏上 | 宏在编译期就展开完了，运行期没有开销 |
| 自己写宏却忘了注册 | 报 `external macro implementation type ... could not be found`，检查 `providingMacros` |
| 用 `Mirror` / `dump` 输出生产日志 | 它们会暴露内部结构，日志请用 Logger |
| 把宏当"万能代码生成器" | 它只能按语法节点生成代码，运行期的值它看不到 |
