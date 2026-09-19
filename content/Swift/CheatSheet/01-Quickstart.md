+++
title = "01 起步与运行方式"
linkTitle = "01 起步"
weight = 10
date = "2026-09-16T11:00:00+08:00"
type = "docs"
description = "Swift 代码的五种跑法、源文件的五个零件、常用编译选项与报错速查"
isCJKLanguage = true
draft = false
+++

# 01 起步与运行方式

## 一段代码的五种跑法

Swift 不像脚本语言只有一种执行方式，也不像编译型语言动不动就要建工程。同一个 `print`，下面五种跑法都成立，选哪种取决于你此刻想干什么。

{{< tabpane text=true persist=disabled >}}

{{% tab header="单文件直跑" %}}

最快的方式，适合验证一个语法点：

```swift
// demo.swift
let scores = [88, 92, 79]
print(scores.max() ?? 0)
// prints: 92
```

```console
$ swift demo.swift
92
```

⚠️ 单文件的顶层代码是**从上往下顺序执行**的，可以写 `print` 这样的语句；但在工程里，只有 `main.swift` 才有这个特权。

{{% /tab %}}

{{% tab header="交互式 REPL" %}}

```console
$ swift repl
  1> let x = 21
x: Int = 21
  2> x * 2
$R0: Int = 42
```

`:quit` 退出，`:` 开头的都是 REPL 命令（`:help` 能看到全部）。粘贴多行代码时用 `:` 加花括号的旧规矩已经不需要了，现代 REPL 会自己判断。

一次性执行一行代码可以用 `-e`：

```console
$ swift -e 'print(6 * 7)'
42
```

{{% /tab %}}

{{% tab header="编译成二进制" %}}

```console
$ swiftc -O demo.swift -o demo
$ ./demo
92
```

多文件就是一次列出来，入口放在 `main.swift`：

```console
$ swiftc -O main.swift Helper.swift -o tool
```

如果代码里既没有 `main.swift`、也没有 `@main`，编译立刻失败——顶层语句只属于 `main.swift`：

```console
$ swiftc Demo.swift Helper.swift -o tool
Demo.swift:1:1: error: expressions are not allowed at the top level
```

把那个带顶层代码的文件改名成 `main.swift`，或者给它加一个 `@main` 类型，两种都行。

{{% /tab %}}

{{% tab header="SwiftPM 项目" %}}

```console
$ swift package init --type executable
$ swift run
$ swift build -c release
$ swift test
```

🔥 `swift run` 会在源码改动后自动重新构建，写小型工具时比手动调 `swiftc` 舒服得多。工程细节见 [13 工具链与工程]({{< relref "13-Tooling.md" >}})。

{{% /tab %}}

{{% tab header="Xcode / Playground" %}}

| 场景 | 用什么 |
| --- | --- |
| 写 App、调试 UI | Xcode 工程，`⌘R` 运行 |
| 试算法、看中间结果 | Playground（Xcode 里 `File ▸ New ▸ Playground`） |
| 只跑一个片段 | `swift repl` |

Playground 的行内结果面板会在每行右侧显示变量当前值，这是它唯一的不可替代之处。

{{% /tab %}}

{{< /tabpane >}}

## 源文件的五个零件

一个 `.swift` 文件里允许出现的东西，全部可以归到这五类。认识它们，编译器报错时你才知道它在说哪一层。

| 零件 | 长这样 | 说明 |
| --- | --- | --- |
| 注释 | `//` `/* */` | 块注释**可以嵌套**，这是 Swift 少见的贴心之处 |
| 标识符 | `userName` `` `class` `` | 名字；撞上关键字就用反引号包起来 |
| 关键字 | `let` `struct` `await` | 语言保留字，分「声明 / 语句 / 表达式」三类 |
| 字面量 | `42` `3.14` `"hi"` `true` `nil` `[1,2]` | 源码里直接写出的值 |
| 特殊指令 | `#if` `#file` `#selector` | 以 `#` 开头，由编译器而非运行时处理 |

### 注释

```swift
// 行注释

/* 块注释
   /* 还能嵌套 */
   这是 C 语言做不到的
*/

/// 文档注释：会被 Xcode 提取成 Quick Help
/// - Parameter name: 用户名字
func greet(_ name: String) -> String { "你好，\(name)" }
```

### 标识符的规矩

```swift
let userName = 1          // 字母、数字、下划线
let _private = 2          // 可以下划线开头
let 用户 = 3               // Unicode 字母可以直接用
let 变量2 = 4              // 数字可以出现在中间（但不能打头）
let `class` = 5           // 撞上关键字就用反引号包起来
```

⚠️ 三条禁令：不能以数字开头、不能包含空白或箭头字符、不能包含 `#`（`#` 属于特殊指令的地盘）。至于 Emoji，编译器居然真的允许 `let 🐶 = 1`——但请别这么写，同事会记住你。

### 关键字速查

| 分类 | 关键字 |
| --- | --- |
| 声明 | `associatedtype` `class` `deinit` `enum` `extension` `func` `import` `init` `inout` `let` `protocol` `rethrows` `static` `struct` `subscript` `typealias` `var` `operator` `precedencegroup` |
| 语句 | `break` `case` `catch` `continue` `default` `defer` `do` `else` `fallthrough` `for` `guard` `if` `in` `repeat` `return` `switch` `throw` `where` `while` |
| 表达式与类型 | `Any` `as` `await` `false` `is` `nil` `self` `Self` `super` `throws` `true` `try` |
| 访问控制 | `private` `fileprivate` `internal` `package` `public` `open` |
| 模式 | `_` `let` `var` `case` `is` `as` |

后面这几组叫**上下文关键字**，它们不是保留字，出现在别的上下文里时可以照常当普通名字用：

| 分类 | 关键字 |
| --- | --- |
| 并发 | `actor` `async` `isolated` `nonisolated` `sending` `distributed` |
| 所有权 | `borrowing` `consuming` `each` `sending` `~Copyable` |
| 继承、覆写与修饰 | `final` `override` `required` `convenience` `dynamic` `indirect` `nonmutating` |
| 属性玩法 | `lazy` `get` `set` `willSet` `didSet` `mutating` `optional` `weak` `unowned` |
| 其他 | `some` `any` `macro` `infix` `prefix` `postfix` `left` `right` `none` |

### 字面量

| 写法 | 类型 | 备注 |
| --- | --- | --- |
| `42`、`0xFF`、`0b1010`、`0o755` | `Int` | 下划线可以随便加：`1_000_000` |
| `3.14`、`1.5e3`、`0x1p2` | `Double` | 十六进制浮点用 `p` 表示 2 的幂 |
| `"你好"`、`#"C:\path"#` | `String` | `#` 包裹的是原始字符串，反斜杠不转义 |
| `"A"` | `Character` | 只有在明确要求 `Character` 时才成立 |
| `true` / `false` | `Bool` | 不是 `0` / `1` |
| `nil` | `Optional` | 单独写会报错，必须有上下文类型 |
| `[1, 2]` / `["a": 1]` | `Array` / `Dictionary` | 空字面量必须写类型：`let a: [Int] = []` |

### 特殊指令 `#`

| 指令 | 作用 |
| --- | --- |
| `#if` `#elseif` `#else` `#endif` | 条件编译 |
| `#available` / `#unavailable` | 运行期可用性判断 |
| `#file` `#fileID` `#filePath` | 当前文件名（`#fileID` 更短，推荐用于日志） |
| `#line` `#column` `#function` | 行号、列号、当前函数名 |
| `#warning("...")` `#error("...")` | 主动产生编译警告 / 编译错误 |
| `#selector(...)` `#keyPath(...)` | 取 Objective-C 选择器 / 字符串化的 KeyPath |
| `#sourceLocation(file:line:)` | 手工改写后续代码的调试位置信息 🝖 |

💭 这些 `#` 开头的写法其实分两类：`#file` `#fileID` `#line` `#function` `#warning` `#error` 在官方文档里算**标准库提供的自由宏**，而 `#if` `#available` `#selector` `#keyPath` 是编译器自带的特殊语法。宏那一套（包括自己写宏）见 [15 宏与调试]({{< relref "15-Macros-and-Debugging.md" >}})。

另一个符号是 `@`：它不产生值，而是**贴在声明上**的开关——`@available`、`@discardableResult`、`@MainActor`、`@objc`、`@propertyWrapper` 都属于这一类。完整清单见 [15 章末尾的属性速查]({{< relref "15-Macros-and-Debugging.md" >}})。

```swift
#if DEBUG
print("调试构建")
#endif

#warning("别忘了删掉这段")
#error("这一行会让编译直接失败")

func log(_ msg: String, file: String = #fileID, line: Int = #line) {
    print("[\(file):\(line)] \(msg)")
}
```

## 条件编译速查

```swift
#if os(macOS) || os(iOS)
    // 平台判断
#elseif os(Linux)
#endif

#if arch(arm64) && compiler(>=6.0)
    // 架构 + 编译器版本，可以用 && || ! 组合
#endif

#if canImport(Foundation)
    import Foundation
#endif

#if targetEnvironment(simulator)
    // 只跑在模拟器里
#endif

#if DEBUG
    // 需要编译时加 -D DEBUG
#endif
```

⚠️ **`swift(>=6.0)` 检查的是语言模式，不是工具链版本。** 用 Swift 6.4 的工具链、但不加 `-swift-version 6` 时，`swift(>=6.0)` 为假。要判断工具链请用 `compiler(>=6.0)`。这个坑每年都要坑一批人。

```swift
#if swift(>=6.0)
    // 只在 Swift 6 语言模式下编译
#endif
```

## 常用编译选项

| 选项 | 作用 |
| --- | --- |
| `-O` | 优化构建，接近 release 性能 |
| `-Osize` | 优先优化体积 |
| `-Onone` | 不优化，调试构建默认值 |
| `-g` | 生成调试信息 |
| `-swift-version 5` / `6` | 指定语言模式 🔥 |
| `-strict-concurrency=minimal\|targeted\|complete` | 并发检查强度 |
| `-enable-upcoming-feature X` | 提前启用某个未来特性 |
| `-warnings-as-errors` | 把警告当错误，CI 里值得开 |
| `-suppress-warnings` | 屏蔽全部警告 |
| `-D DEBUG` | 定义条件编译标志 |
| `-parse-as-library` | 禁止顶层代码，强制要求 `@main` |
| `-module-name` | 指定模块名，影响日志与调试符号 |
| `-target` / `-sdk` | 交叉编译时指定目标三元组与 SDK |
| `-emit-library` / `-static` | 输出动态库 / 静态库 |
| `-typecheck` | 只做类型检查，不生成产物，检查语法时最快 |

```console
$ swiftc -typecheck -swift-version 6 -strict-concurrency=complete Sources/*.swift
```

## 报错速查

编译器的话术很固定，认识这几句能省下大量搜索时间：

| 报错 | 真实含义 |
| --- | --- |
| `cannot find 'x' in scope` | 拼错、没 import、或者定义在使用之后（顶层代码尤其常见） |
| `value of optional type 'String?' must be unwrapped` | 忘了处理 `?`，见 [06 可选值]({{< relref "06-Optionals.md" >}}) |
| `cannot use mutating member on immutable value` | 改动 `let` 了，换成 `var` |
| `missing argument label 'x:' in call` | 参数标签对不上，Swift 默认要求写标签 |
| `cannot convert value of type 'Int' to expected argument type 'Double'` | Swift **不做**隐式数值转换，得手写 `Double(x)` |
| `type 'X' does not conform to protocol 'Sendable'` | 跨界共享了不安全的类型，见 [09 错误处理与并发]({{< relref "09-Error-Handling-and-Concurrency.md" >}}) |
| `main actor-isolated ... can not be referenced from a nonisolated context` | 在主线程之外碰了 UI 相关代码 |
| `self used before all stored properties are initialized` | 初始化器里属性还没齐就用了 `self` |
| `'nil' requires a contextual type` | 单独写 `nil`，编译器不知道你要哪种可选值 |
| `'main' attribute cannot be used in a module that contains top-level code` | 用 `swiftc` 编单文件时 `@main` 与"顶层代码入口"打架，加 `-parse-as-library` |
| `invalid UTF-8 found in source file` | 文件编码不是 UTF-8，见下一节 |

## 编码：Swift 只认 UTF-8

Swift 源文件**必须**是 UTF-8，没有别的选项。这不是建议，是硬性要求：换个编码，编译器连文件都读不进去。

```console
$ file demo.swift
demo.swift: UTF-8 Unicode text

$ file latin1.swift
latin1.swift: ISO-8859 text

$ swiftc -typecheck latin1.swift
latin1.swift:1:11: error: invalid UTF-8 found in source file
```

⚠️ 两个容易忽略的点：

1. **字符串字面量里的内容也受这条规则约束。** 文件是 UTF-8，字符串里就能直接写 `你好`、`café`，不需要转义成 `\u{4F60}`。
2. **`String` 内部不以字节为单位。** 你写进去的是一个"扩展字形簇"序列，所以 `count` 数的是字形簇而不是字节，索引也不是整数。细节见 [03 类型与字符串]({{< relref "03-Types-and-Strings.md" >}})。

想让编辑器统一行为，工程里常见两种做法：在文件头写注释提醒，或者用 `.editorconfig` / 格式化工具统一约束：

```swift
// -*- coding: utf-8 -*-
```

💭 顺带一句：本速查表所有示例都按 UTF-8 保存，中文注释与中文输出都直接写在源码里，不需要任何转义。
