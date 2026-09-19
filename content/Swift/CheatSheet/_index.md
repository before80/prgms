+++
title = "Swift 语言速查表"
linkTitle = "Swift 速查表"
weight = 2
date = "2026-09-16T11:00:00+08:00"
type = "docs"
description = "面向「已经会编程」的 Swift 6 速查表：一页一个主题，表格 + 可切换标签页，专治“我记得有这个语法，但忘了怎么写”"
isCJKLanguage = true
draft = false
+++

# Swift 语言速查表

这不是教程，是**字典**。教程教你走路，字典只在你卡住时递上一根拐杖。所以本页写得密、写得短、写得没什么耐心——每一条都假设你已经会编程，只是记不清 Swift 里这个动作该怎么写。

风格上参考 [Rust Language Cheat Sheet](https://cheats.rs/)，但内容完全按 Swift 6 重写：Swift 没有借用检查器，却有多标签、有 `async/await`、有值语义与引用语义的分野，还有一整套只有 Apple 生态才有的东西。所以照搬没有意义，该不一样的地方就让它不一样。

> 语言版本基线：**Swift 6.4**（写作时本机工具链的实际版本），示例一律按 Swift 6 语言模式（严格并发检查）编写。凡是只在新版本里才有的东西，都会当场标注 🆕。

---

## 图例说明

| 符号 | 含义 |
| --- | --- |
| 🔥 | 高频使用，值得先记住 |
| ⚠️ | 陷阱或易错点，踩过一次就该记住 |
| 🛑 | 错误示例，故意写错给你看 |
| 🆕 | 较新版本才有的语法，注意 `#available` 或工具链版本 |
| 🚧 | 有限制、仍在演进，或者只在特定平台可用 |
| 🝖 | 偏深的内容，第一遍可以跳过 |
| 💭 | 笔者见解，不是官方定论 |
| ↪ | 等价写法或语法糖展开 |
| 📘 | 指向官方文档或权威资料 |

> **关于 `// prints:`**：它标的是这段代码真实跑出来的输出。跟在后面的缩进 `//` 行表示"依次输出了好几行"；行尾那些中文注解（⚠️ 🛑 之类）只是给人看的，不属于输出内容。所有示例都在 Swift 6.4、`-swift-version 6` 下实跑过。

---

## 目录导航

| 主题 | 内容一句话 |
| --- | --- |
| [01 起步与运行方式]({{< relref "01-Quickstart.md" >}}) | 工具链怎么装、一段代码有哪五种跑法 |
| [02 语言主干]({{< relref "02-Language-Basics.md" >}}) | 变量、运算符、控制流、`let` 绑定全表、模式匹配 |
| [03 类型与字符串]({{< relref "03-Types-and-Strings.md" >}}) | 数值的边界、字符与字符串的所有写法、正则与格式化 |
| [04 集合与序列]({{< relref "04-Collections.md" >}}) | 数组、字典、集合、元组、区间与高阶函数 |
| [05 函数与闭包]({{< relref "05-Functions-and-Closures.md" >}}) | 参数标签、`inout`、尾随闭包、捕获列表 |
| [06 可选值]({{< relref "06-Optionals.md" >}}) | `?` 与 `!` 的完整解包手册 |
| [07 自定义类型]({{< relref "07-Custom-Types.md" >}}) | 结构体、类、枚举、actor，以及属性与下标的全部形态 |
| [08 协议与泛型]({{< relref "08-Protocols-and-Generics.md" >}}) | 协议、关联类型、`some` 与 `any` |
| [09 错误处理与并发]({{< relref "09-Error-Handling-and-Concurrency.md" >}}) | `throws`、`async/await`、actor、`Sendable` |
| [10 内存与值语义]({{< relref "10-Memory-and-Value-Semantics.md" >}}) | 值传递还是引用传递、ARC、写时复制、指针 |
| [11 标准库速查]({{< relref "11-Standard-Library.md" >}}) | 常用协议、格式化、Codable、KeyPath、结果构建器 |
| [12 语法糖与简写对照]({{< relref "12-Syntax-Sugar.md" >}}) | 一份代码的完整写法与简写并排看 |
| [13 工具链与工程]({{< relref "13-Tooling.md" >}}) | `swift` 命令表、`Package.swift` 模板、测试与条件编译 |
| [14 类型转换与互操作]({{< relref "14-Type-Casting-and-Interop.md" >}}) | `is` / `as?` / `as!`、`Any` 与元类型、Mirror、Objective-C 边界 |
| [15 宏与调试]({{< relref "15-Macros-and-Debugging.md" >}}) | 宏的声明与实现、`@` 属性全表、断言家族与调试输出 |

---

## 你好，Swift!

先让第一行代码跑起来。Swift 和那些「先装 SDK 再看文档」的语言不太一样：只要有 Xcode 或官方工具链，命令行里敲一个 `swift` 就能进交互模式。

{{< tabpane text=true persist=disabled >}}

{{% tab header="Hello World" %}}

```swift
// hello.swift
print("Hello, world!")
```

```console
$ swift hello.swift
Hello, world!
```

`print` 默认会换行。不想换行就传 `terminator`：

```swift
print("A", terminator: "")
print("B")
// prints: AB
```

{{% /tab %}}

{{% tab header="优势" %}}

**Swift 擅长这些事**

- **性能**：编译成原生机器码，没有虚拟机也没有 JIT 预热，适合从命令行工具到实时音频的各种负载。
- **安全**：可选值、值语义、默认的数组越界检查、严格的初始化规则，把大量运行时崩溃变成了编译期错误。
- **并发**：`async/await`、actor、`Sendable` 都由编译器做检查，"数据竞争"在 Swift 6 里是编译错误而不是线上事故。
- **表达力**：泛型、协议扩展、结果构建器、宏，让库作者能写出看起来像语言内置的 API（`@ViewBuilder` 就是靠这套东西做到的）。
- **互操作**：与 C、C++、Objective-C 都能直接互调，也能被 Objective-C 与 Python 调用。🚧
- **一套语言，全平台**：同一份代码从 watchOS 写到 Linux 服务端；SwiftPM 在 Apple 与 Linux 上都能用。

{{% /tab %}}

{{% tab header="劣势" %}}

**你可能会嫌它烦的地方**

- **编译器慢**：类型检查器遇上深层表达式会变慢，全量类型推断偶尔需要你主动写注解来"帮它一把"。
- **Apple 优先**：SwiftUI、Combine、大部分系统框架只在 Apple 平台可用；Linux 上只有 Swift Foundation 与少数服务端框架。🚧
- **版本分裂**：Swift 语言版本、语言模式（5/6）、平台部署目标、工具链版本，是四件不同的事，混起来能绕晕人。
- **ABI 与生态**：包管理器生态比主流语言小得多，很多领域得自己写或用 C 库。
- **字符串不按字节走**：`String` 的索引不是整数，刚上手会觉得处处别扭——但它是对的，见 [03 类型与字符串]({{< relref "03-Types-and-Strings.md" >}})。

{{% /tab %}}

{{% tab header="安装" %}}

**macOS**

- 想要完整生态（SwiftUI、App Store 开发）：从 App Store 装 **Xcode**。
- 只想要命令行工具链：`xcode-select --install`，或者用 [swiftly](https://www.swift.org/swiftly/) 管理多套工具链。

**Linux**

- 从 [swift.org/download](https://www.swift.org/download/) 下载官方 tarball，或用发行版仓库。Ubuntu 上官方推荐用 swiftly。

**Windows** 🚧

- 官方支持仍在完善，Windows 版工具链可以从 swift.org 获取，但系统框架相关的能力有限。

```console
$ swift --version
swift-driver version: 1.168.6 Apple Swift version 6.4 (swiftlang-6.4.0.34.1)
Target: arm64-apple-macosx26.0
```

{{% /tab %}}

{{% tab header="编辑器" %}}

| 场景 | 推荐 | 说明 |
| --- | --- | --- |
| Apple 平台开发 | **Xcode** | SwiftUI 预览、Instruments、模拟器，一步到位 |
| 跨平台 / 服务端 | **VS Code + Swift 扩展** | 底层就是 SourceKit-LSP，配合 SwiftPM 用着很顺 |
| JetBrains 用户 | VS Code / CLion 的 Swift 插件 🚧 | **AppCode 已停止维护**，CLion 插件仍在跟进 |
| 只想试几句 | `swift repl` 或 [SwiftFiddle](https://swiftfiddle.com/) | 不用装任何东西 |

{{% /tab %}}

{{% tab header="怎么读这份速查表" %}}

三条建议，按重要性排序：

1. **别顺读。** 卡住了去目录里点，解决问题就走。
2. **留意切换标签。** 本速查表大量使用多标签对比同一种效果的几种写法，比如「完整写法 / 尾随闭包 / `$0` 简写」——这页最值钱的东西都藏在那里。
3. **把 ⚠️ 当正文读。** 速查表的错误示例，往往比正确示例更省时间。

💭 如果你想要**系统学一遍**而不是速查，隔壁的 [Swift 基础部分]({{< relref "../basic/_index.md" >}}) 是按学习顺序写的教程；本目录负责在你忘了怎么写的时候救急。

{{% /tab %}}

{{< /tabpane >}}

---

## 一个 Swift 源文件长什么样

同一份"打印问候语"的功能，在不同工程形态下的最小骨架不太一样。搞混了会觉得 Swift 到处是规矩，其实只是入口不同。

{{< tabpane text=true persist=disabled >}}

{{% tab header="单文件脚本" %}}

```swift
// greet.swift —— 顶层代码是允许的，从上往下顺序执行
let name = "Swift"
print("你好，\(name)！")
// prints: 你好，Swift！
```

```console
$ swift greet.swift
```

也可以在文件头加 shebang，直接当可执行文件跑：

```swift
#!/usr/bin/env swift
print("hello from shebang")
```

{{% /tab %}}

{{% tab header="SwiftPM 可执行程序" %}}

```swift
// Sources/Hello/main.swift
// SwiftPM 会把 main.swift 当作程序的入口文件
print("Hello from SwiftPM")
```

```console
$ swift run Hello
```

不想用 `main.swift`，也可以在任何文件里写 `@main`：

```swift
// Sources/Hello/Hello.swift
@main
struct Hello {
    static func main() {
        print("Hello from @main")
    }
}
```

⚠️ 用 `swiftc` 直接编**单个**文件时，这个文件会被当成"允许顶层代码的入口"，`@main` 反而报错。想单文件验证，加 `-parse-as-library`：

```console
$ swiftc atmain.swift -o app
atmain.swift:1:1: error: 'main' attribute cannot be used in a module that contains top-level code
$ swiftc -parse-as-library atmain.swift -o app    # ✅
```

SwiftPM 里不用管这条，因为包里的文件本来就不是按"入口脚本"编的。

{{% /tab %}}

{{% tab header="App 入口" %}}

App 的入口不是 `main` 函数，而是一个带 `@main` 的类型：

```swift
import SwiftUI

@main
struct MyApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }
}
```

UIKit 老写法里还有 `@UIApplicationMain` 和 `application(_:didFinishLaunchingWithOptions:)`，新项目基本不用了。🝖

{{% /tab %}}

{{% tab header="库" %}}

```swift
// Sources/MyLib/Greeter.swift
public struct Greeter {
    public init() {}
    public func greet(_ name: String) -> String {
        "你好，\(name)！"
    }
}
```

库没有入口，只有 `public` 才能被外部看到。想看这一块的全部细节，去 [13 工具链与工程]({{< relref "13-Tooling.md" >}})。

{{% /tab %}}

{{< /tabpane >}}

---

## 版本这件事，先理清楚

Swift 里"版本"有四个互不相同的含义，网上的报错信息经常把它们混着说：

| 概念 | 例子 | 影响什么 |
| --- | --- | --- |
| 工具链版本 | Swift 6.4 | 你能用哪些语法、编译器有哪些新检查 |
| 语言模式 | `-swift-version 6` | 是否启用严格并发检查、`Sendable` 违规是警告还是错误 |
| 部署目标 | iOS 26 / macOS 26 | 什么 API 能直接调用，什么必须 `if #available` |
| 包版本 | `swift-tools-version: 6.2` | `Package.swift` 能写哪些清单 API |

```swift
if #available(macOS 26, iOS 26, *) {
    // 新 API 直接调用
} else {
    // 老系统上退回到兼容实现
}
```

⚠️ 语言模式不是工具链版本。用 Swift 6.4 的工具链，依然可以把某个 target 设成 Swift 5 语言模式，此时并发相关的严格检查会退化成警告。

---

## 官方资料去哪儿找

| 资料 | 链接 | 什么时候用 |
| --- | --- | --- |
| The Swift Programming Language | [docs.swift.org](https://docs.swift.org/swift-book/) | 语言语义的权威答案 |
| Swift Standard Library | [developer.apple.com/documentation/swift](https://developer.apple.com/documentation/swift) | 查具体 API 签名 |
| Swift Evolution | [swift-evolution](https://github.com/swiftlang/swift-evolution/tree/main/proposals) | 想知道某个语法是哪版加的、为什么这么设计 |
| Swift.org 博客 | [swift.org/blog](https://www.swift.org/blog/) | 新版本特性解读 |
| Swift Forums | [forums.swift.org](https://forums.swift.org/) | 官方团队会下场回答的社区 |
