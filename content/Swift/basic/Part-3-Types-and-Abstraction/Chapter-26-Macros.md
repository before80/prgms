+++
title = "第26章 宏：让编译器替你写代码"
weight = 260
date = "2026-09-14T22:30:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 第二十六章：宏：让编译器替你写代码

> 宏听起来像“高级魔法”，实际更像一台编译期代码生成器：你写一段简洁的调用，编译器在编译时展开成更多代码。它没有运行时开销，也没有偷偷修改对象；展开后的代码仍然要接受完整类型检查。

## 26.1 宏是什么，不是什么

宏在编译期工作。它可以：

- 把一段表达式展开成更完整的表达式。
- 为类型生成成员、访问器或协议实现。
- 生成诊断信息、编译期警告和错误。

宏不是：

- 运行时反射。
- 可以随便改环境的文本替换。
- 编译器的私有后门。

宏的展开结果必须是合法 Swift，并且会参与类型检查。错误会在编译阶段暴露，而不是等到程序运行。

## 26.2 自由宏：以 `#` 调用

自由宏像函数调用，但前面是 `#`：

```swift
let result = #stringify(1 + 2)
print(result.0)
// prints: 3
print(result.1)
// prints: 1 + 2
```

`#stringify` 不是标准库函数；它是编译器宏展开后得到的一个元组：第一个元素是表达式的值，第二个元素是表达式的源码文本。

宏声明看起来像函数，但实现来自单独的模块：

```swift
@freestanding(expression)
macro stringify<T>(_ value: T) -> (T, String) =
    #externalMacro(module: "MyMacros", type: "StringifyMacro")
```

`@freestanding(expression)` 表示这是独立的表达式宏；`#externalMacro` 指向真正负责展开的 Swift 类型。

`#expect` 是另一个熟悉的自由宏：

```swift
#expect(1 + 1 == 2)
```

它不只是打印一句话，而是会保留表达式文本、失败信息和调用位置，这正是宏比普通函数更适合测试断言的原因。

## 26.3 附着宏：贴在声明上的 `@`

附着宏用 `@` 写在声明前面，可以为原声明添加内容。成员宏会替类型生成成员：

```swift
@AddDescription
struct Product {
    let name: String
}

// 宏可能展开出：
// struct Product {
//     let name: String
//     var description: String { ... }
// }
```

声明看起来像：

```swift
@attached(member, names: prefixed(__generated_))
macro AddDescription() = #externalMacro(
    module: "MyMacros",
    type: "AddDescriptionMacro"
)
```

附着宏的常见角色有：

| 角色 | 作用 |
| --- | --- |
| `peer` | 生成与原声明并列的新声明 |
| `member` | 给类型生成成员 |
| `accessor` | 为属性添加访问器 |
| `memberAttribute` | 给成员附加属性 |
| `extension` | 生成扩展 |
| `conformance` | 自动添加协议遵循 |

SwiftUI 的 `#Preview` 是自由宏，`@Observable` 和 Swift Testing 的 `@Test` 是附着宏。`@Observable` 会生成观察相关代码，`@Test` 会登记测试函数。

框架自带的宏还有几个你会经常撞见：SwiftUI 的 `#Preview` 用来把一段视图登记成 Xcode 预览；SwiftData 的 `@Model` 是附着宏，会把一个类改造成可持久化的模型；Foundation 的 `#Predicate` 是自由宏，把闭包里的条件表达式展开成可序列化的查询谓词。它们和 `@Observable` 属于同一套机制，区别只在谁提供实现——这些实现随 Apple 平台框架一起分发，所以只能在对应的平台工程里编译，命令行工具链里看不到它们（官方链接见附录 F）。

## 26.4 宏的实现依赖编译器插件

宏的实现不能写在普通 App 目标里，必须放在独立的宏目标中，并通过 SwiftPM 暴露为编译插件：

```swift
// Package.swift 的简化示意
.macro(
    name: "MyMacros",
    dependencies: [
        .product(name: "SwiftSyntaxMacros", package: "swift-syntax"),
        .product(name: "SwiftCompilerPlugin", package: "swift-syntax")
    ]
)
```

实现侧通常要引入 `SwiftSyntax`、`SwiftSyntaxMacros` 和 `SwiftCompilerPlugin`，再提供一个 `CompilerPlugin` 入口。宏实现拿到的是语法树，不是普通的运行时值，所以它分析的是源码结构。

## 26.5 亲手写一个最小宏：三个文件跑起来

前面说的都是“宏做了什么”，现在让它真的跑起来。下面这个 `#stringify` 是官方示例里最经典的最小宏：输入一个表达式，得到一个元组——第一个元素是表达式的**值**，第二个元素是表达式的**源码文本**。

第一步，在 `Package.swift` 里同时声明宏目标和它的使用者：

```swift
// swift-tools-version: 6.0
import PackageDescription
import CompilerPluginSupport            // 宏需要它

let package = Package(
    name: "StringifyDemo",
    platforms: [.macOS(.v13)],
    dependencies: [
        // 宏实现依赖 swift-syntax：操作语法树的类型都在那里
        .package(url: "https://github.com/swiftlang/swift-syntax.git", from: "600.0.0")
    ],
    targets: [
        // 宏实现住在独立目标里，最终编译成编译器插件
        .macro(
            name: "StringifyMacros",
            dependencies: [
                .product(name: "SwiftSyntaxMacros", package: "swift-syntax"),
                .product(name: "SwiftCompilerPlugin", package: "swift-syntax")
            ]
        ),
        // 普通代码依赖宏目标，就能用 #stringify
        .executableTarget(name: "App", dependencies: ["StringifyMacros"])
    ]
)
```

第二步，写宏实现。注意它操作的是**语法树节点**，不是运行时的值：

```swift
// Sources/StringifyMacros/StringifyMacros.swift
import SwiftSyntax
import SwiftSyntaxMacros
import SwiftCompilerPlugin

public struct StringifyMacro: ExpressionMacro {
    public static func expansion(
        of node: some FreestandingMacroExpansionSyntax,
        in context: some MacroExpansionContext
    ) throws -> ExprSyntax {
        // node 就是 #stringify(...) 这整棵子树，取出第一个参数的表达式
        guard let argument = node.arguments.first?.expression else {
            throw MacroExpansionErrorMessage("需要且只需要一个参数")
        }
        // 展开成元组：左边保留原表达式，右边把源码文本塞进字符串字面量
        return "(\(argument), \(literal: argument.formatted().description))"
    }
}

@main
struct StringifyPlugin: CompilerPlugin {          // 插件入口：告诉编译器有哪些宏
    let providingMacros: [Macro.Type] = [StringifyMacro.self]
}
```

第三步，声明并使用：

```swift
// Sources/App/main.swift
@freestanding(expression)
macro stringify<T>(_ value: T) -> (T, String) =
    #externalMacro(module: "StringifyMacros", type: "StringifyMacro")

let result = #stringify(1 + 2)
print(result.0)
// prints: 3
print(result.1)
// prints: 1 + 2
```

`swift run` 之后你会看到 `3` 和 `1 + 2`：表达式真的算了一遍，源码文本也被原样保留。普通函数无论如何都拿不到第二样东西——这就是宏值得存在的地方。

两个细节值得记住：`#externalMacro(module:type:)` 里的模块名和类型名必须与宏目标、实现类型逐字对上，写错就是编译期报错“找不到宏”；首次构建要下载并编译 swift-syntax，会慢一点，之后就走增量了。

想确认宏到底展开了什么，两个办法最实用：在 Xcode 里对着宏调用点右键选 “Expand Macro”，展开结果会直接显示出来；写库里更正式的做法是给宏写测试——swift-syntax 提供的 `assertMacroExpansion` 可以把你期望的展开结果写成断言，宏一改错测试就红。

## 26.6 宏的边界

宏很强，但它受几项限制：

- 宏展开必须是确定的，不能依赖运行时状态。
- 宏不能绕过访问控制，展开后的代码仍受可见性约束。
- 宏输出必须通过类型检查，不能强行生成非法代码。
- 一个宏声明和它的实现必须匹配角色与签名。
- 宏会被编译器缓存，修改宏实现后要清理并重新构建。

因此，宏适合消除有规律的样板代码，例如模型生成、依赖注入、测试登记和观察代码生成。普通业务逻辑用函数、泛型和协议通常更清楚。

## 26.7 什么时候用宏

可以用宏：

- 代码模式高度重复，而且无法靠泛型表达。
- 需要在编译期读取表达式文本、保留调用位置或生成成员。
- 希望提供接近语言级别的声明式接口。

不要用宏：

- 只是为了避免写一个普通函数。
- 逻辑依赖运行时数值、文件或网络。
- 团队还不熟悉宏，但收益只是“看起来高级”。

宏的正式入口在 Swift 官方仓库的 swift-syntax 和 macro 示例中。学习时建议先读官方宏示例，再尝试实现一个最小宏，而不是一上来写复杂代码生成器。

## 26.8 本章小结

| 类型 | 形式 | 例子 |
| --- | --- | --- |
| 自由表达式宏 | `#name(...)` | `#stringify(1 + 2)` |
| 自由声明宏 | `#name` | 生成声明 |
| 附着成员宏 | `@name` | 给类型添加成员 |
| 附着访问器宏 | `@name` | 为属性生成 get/set |
| 附着协议宏 | `@name` | 自动添加协议遵循 |
| 宏实现 | 独立模块 + 编译器插件 | `swift-syntax` |

## 26.9 本章易错点速查

| 易错点 | 正确理解 |
| --- | --- |
| 把宏当成运行时反射 | 宏在编译期展开 |
| 以为宏可以跳过类型检查 | 展开结果仍会完整检查 |
| 在 App 目标里直接实现宏 | 宏实现需要独立宏目标与插件 |
| 用宏替代普通函数 | 简单逻辑优先使用语言既有结构 |
| 随意生成大量代码 | 展开后难读、难调试、编译压力更大 |
| 忘记清理宏缓存 | 修改实现后可能仍然使用旧的展开结果 |

## 26.10 下章预告

第三篇到此结束。第四篇进入所有 Swift 程序最终都绕不开的主题：内存与并发。先从值语义、写时复制和 ARC 讲起，然后处理循环引用、所有权，最后进入 async/await 与隔离域。
