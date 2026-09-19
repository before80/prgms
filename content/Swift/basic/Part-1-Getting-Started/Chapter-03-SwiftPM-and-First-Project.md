+++
title = "第3章 第一个真正的项目：SwiftPM 与命令行工具"
weight = 30
date = "2026-09-14T22:30:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 第三章：第一个真正的项目：SwiftPM 与命令行工具

> 单文件的好处是"改一行就能跑"；坏处是当你的程序需要十几个文件、三四个依赖、一套测试时，它会立刻变成灾难现场。SwiftPM（Swift Package Manager）就是官方的"收拾现场"方案：它管源码怎么摆、依赖怎么拉、怎么编译、测试怎么跑。这一章我们不写什么精彩代码，但会把你之后所有项目的地基打好。

## 3.1 为什么需要"包"

一个 Swift 包（package）替你解决四件事：

- **目录约定**：源码放哪、测试放哪，不用每次重新发明。
- **依赖管理**：从某个 Git 仓库拉一个库进来，并锁定版本。
- **构建流程**：一条命令编译、运行、测试，跨 macOS、Linux、Windows 一致。
- **可分发性**：别人可以用一行依赖声明把你的库接进他的项目。

## 3.2 三十秒生成一个项目

```bash
$ swift package init --type executable --name Greeter
Creating executable package: Greeter
Creating Package.swift
Creating .gitignore
Creating Sources
Creating Sources/Greeter/Greeter.swift
Creating Tests/
Creating Tests/GreeterTests/
Creating Tests/GreeterTests/GreeterTests.swift
```

四步之后，一个能编译、能运行、能测试的项目就躺在那儿了。注意最后两行——工具连测试目录都替你建好了，这个细节能看出 SwiftPM 的态度：**测试不是可选项**。

## 3.3 目录结构：约定大于配置

| 路径 | 作用 | 能不能改名 |
|------|------|------------|
| `Package.swift` | 包清单，整个项目的入口 | 名字固定 |
| `Sources/<目标名>/` | 该目标的源码目录 | 目录名就是目标名，改名要同步清单 |
| `Tests/<目标名>Tests/` | 该目标的测试代码 | 习惯写法，测试目标名要能被清单引用 |
| `.build/` | 编译中间产物与拉取的依赖 | 别提交到版本库 |
| `.gitignore` | 生成时就替你忽略了 `.build/` 等 | 可以改 |

一条铁律：**目录名与清单里的目标名必须对得上**。构建系统不会读心，它只看名字。

## 3.4 Package.swift：一份用 Swift 写的说明书

它整个就是一段 Swift 代码——这不是"配置文件恰好长得像代码"，而是**清单本身就是用 Swift 执行的**，所以你可以在这里写条件、循环、复用变量：

```swift
// swift-tools-version: 6.3

import PackageDescription

let package = Package(
    name: "Greeter",
    targets: [
        .executableTarget(name: "Greeter"),
        .testTarget(name: "GreeterTests", dependencies: ["Greeter"]),
    ]
)
```

逐行看：

- **第一行必须是注释，而且必须是这一行的格式**。`swift-tools-version` 声明的是"编译这个包**至少**需要哪个工具链版本"。`swift package init` 会把这一行写成你本机工具链的版本（作者的开发机是 6.4 开发版，所以生成的是 6.4；在 6.3 工具链上生成的自然就是 6.3）。它**不是**语言模式，别和 `-swift-version` 搞混。
- **它是一个普通的 Swift 文件**，只是恰好被 SwiftPM 读去当配置。这意味着你可以在里面写变量、循环、条件——很多项目就是这么根据平台拼出不同配置的。
- `.executableTarget` 生成可执行程序；如果你在写库（给别人 `import` 的代码），换成 `.target`。
- `.testTarget` 的 `dependencies` 里写的是同包内的目标名，字符串即可。

## 3.5 三件套命令

日常 95% 的时间只会用到这三条：

```bash
$ swift build
Build complete! (13.63秒)

$ swift run
Build complete! (0.24秒)
Hello, world!

$ swift test
Build complete! (1.83秒)
◇ Test run started.
↳ Testing Library Version: 2084
↳ Target Platform: arm64e-apple-macos14.0
◇ Test example() started.
✔ Test example() passed after 0.001 seconds.
✔ Test run with 1 test in 0 suites passed after 0.001 seconds.
```

（括号里的耗时跟着你的系统语言走，中文环境显示"秒"，英文环境显示 `s`。）

生成的源码长这样，用的是 `@main` 作为程序入口：

```swift
// Sources/Greeter/Greeter.swift
@main
struct Greeter {
    static func main() {
        print("Hello, world!")
    }
}

// 运行 swift run 的结果：
// prints: Hello, world!
```

生成的测试文件用的是 Swift Testing（`@Test` + `#expect`），不是老式的 XCTest。测试框架的细节在第 34 章，这里你只要知道：**新项目默认就带测试，跑测试就是 `swift test`**。

另外三个常用动作：

| 命令 | 作用 |
|------|------|
| `swift run 目标名 参数...` | 运行某个可执行目标，并把参数传给它 |
| `swift build -c release` | 以优化模式构建（发布用） |
| `swift package clean` | 清掉构建产物，安静执行、不打印任何东西 |

## 3.6 程序入口：`main.swift`、`@main` 与顶层代码

一个可执行程序从哪里开始跑？Swift 给你两种正式写法。

第一种，使用 `@main`。这个类型提供 `static func main()`，它就是入口：

```swift
@main
struct App {
    static func main() {
        print("程序从这里开始")
        // prints: 程序从这里开始
    }
}
```

`main()` 也可以抛出错误或异步执行：

```swift
@main
struct AsyncApp {
    static func main() async throws {
        print("异步入口")
        // prints: 异步入口
    }
}
```

`async` 是"这个入口要等异步结果"的标记，`throws` 是"它可能失败"的标记。这两个词现在只需要认得形状：错误处理在第 15 章讲，`async` / `await` 从第 30 章开始讲。

第二种，使用名为 `main.swift` 的文件。它是 SwiftPM 可执行目标里的特殊入口文件，顶层语句按顺序执行：

```swift
// Sources/Greeter/main.swift
print("第一行")
print("第二行")
// prints: 第一行
// prints: 第二行
```

单文件脚本也经常直接写顶层代码。但这种“脚本式”入口只适合简单程序；当项目变大时，顶层变量会散落在全局作用域里，依赖关系也更难看清。

读取命令行参数用 `CommandLine.arguments`：

```swift
// 假设运行：swift run Greeter Mia 42
let arguments = CommandLine.arguments
print(arguments)
// prints: [".../Greeter", "Mia", "42"]
print(arguments.dropFirst().joined(separator: ", "))
// prints: Mia, 42
```

第一个参数是程序路径，真正的用户参数从 `dropFirst()` 开始。需要立即结束进程时可以调用 `exit(0)`；不过大多数代码应该通过 `return`、`throws` 或错误类型表达结束原因。

入口规则很简单：

| 写法 | 入口位置 | 适合场景 |
| --- | --- | --- |
| `@main` | 标注类型里的 `static func main()` | 项目、测试、SwiftUI App |
| `main.swift` | 文件顶层语句 | 小型可执行目标 |
| 单文件脚本 | 文件顶层语句 | 随手验证、短小工具 |

同一个可执行目标里不要同时放 `@main` 和 `main.swift`，否则编译器不知道怎么选入口。一个程序只能有一个起点。

这里有个坑值得提前踩平。你拿单个 `.swift` 文件直接 `swift file.swift` 运行时，它被当成**脚本**处理，文件顶层本身就是入口，此时再写 `@main` 会直接报错：

```text
error: 'main' attribute cannot be used in a module that contains top-level code
```

所以本书后面出现的 `@main struct App { static func main() async { ... } }` 这类例子，请放进 SwiftPM 可执行目标的源文件里运行（比如 `Sources/App/App.swift`）；想随手试，先建一个包：

```bash
swift package init --type executable
```

把代码贴进 `Sources/` 下的源文件，再 `swift run` 即可。如果你把例子贴进的是 `main.swift`，那反过来——直接写顶层语句，不要再加 `@main`。

## 3.7 加一个依赖：三行清单，一行 import

真实项目很少从零写所有东西。以官方的命令行参数解析库 `swift-argument-parser` 为例：

```swift
// swift-tools-version: 6.3

import PackageDescription

let package = Package(
    name: "tool",
    dependencies: [
        .package(url: "https://github.com/apple/swift-argument-parser.git", from: "1.5.0"),
    ],
    targets: [
        .executableTarget(
            name: "tool",
            dependencies: [
                .product(name: "ArgumentParser", package: "swift-argument-parser"),
            ]
        ),
    ]
)
```

```swift
// Sources/tool/main.swift
import ArgumentParser

struct Tool: ParsableCommand {
    @Argument(help: "要说的话") var message: String = "你好"

    func run() {
        print("echo: \(message)")
    }
}

Tool.main()
```

```bash
$ swift run tool 你好世界
Build complete! (1.35秒)
echo: 你好世界
```

清单里有两处依赖声明，新手最容易被它们绕晕：

| 写在哪 | 写法 | 意思 |
|--------|------|------|
| `dependencies:`（包的层级） | `.package(url:from:)` | 我要用这个仓库；`from: "1.5.0"` 表示允许升到 1.x 的最新版，但不跨 2.0 |
| `targets:` 里某个目标的 `dependencies:` | `.product(name:package:)` | 这个目标要用那个包里的哪一个产品 |

构建之后你会看到两样东西：依赖的源码被拉进 `.build/checkouts/`，而**选定的版本被记在 `Package.resolved` 里**（我这次跑出来是 1.8.2，因为 `from: "1.5.0"` 允许升到 1.x 的最新版）。`Package.resolved` 应该提交到版本库——它保证同事和你装的是同一份依赖。

## 3.8 本章小结

| 你想做的事 | 做法 |
|------------|------|
| 新建可执行项目 | `swift package init --type executable --name 名字` |
| 新建库项目 | `swift package init --type library --name 名字` |
| 编译 | `swift build`（发布用 `-c release`） |
| 运行 | `swift run`（多目标时加目标名） |
| 测试 | `swift test` |
| 清理 | `swift package clean` |
| 加依赖 | 包级 `.package(url:from:)` + 目标级 `.product(name:package:)` |
| 锁定依赖版本 | 提交 `Package.resolved` |

## 3.9 本章易错点速查

| 容易踩的地方 | 正确认识 |
|--------------|----------|
| `swift-tools-version` 就是语言模式 | 不是。它声明"这个包至少需要哪版工具链"；语言模式由 `swiftLanguageMode(.v5/.v6)` 之类的设置决定（见第 32 章的迁移话题） |
| 第一行的注释可以随便写 | 必须是文件第一行、必须是 `// swift-tools-version: 版本号` 这种格式，写错了 SwiftPM 会直接拒绝 |
| `Sources/` 下的目录名随便起 | 目录名就是目标名，和清单里的名字必须一致，否则构建系统找不到源码 |
| 改了包名只改清单就行 | 目录名、目标名、`Package.resolved` 里的记录都可能要跟着动；改名前先 `swift package describe` 看清结构 |
| `swift run` 不需要目标名 | 只有一个可执行目标时可以省略；有多个时必须写清楚是哪一个 |
| 依赖写一次就够了 | 是两处：包级声明"要用哪个仓库"，目标级声明"要用哪个产品" |
| `Package.resolved` 是临时文件 | 它锁定依赖的确切版本，应当提交；否则每个人装到的版本可能不同 |
| `.build/` 也一起提交 | 不要。它是构建产物和依赖缓存，体积大且随平台变化 |
| 包名和目录名带点号、空格、中文都无所谓 | 尽量用 ASCII 字母、数字、连字符。名字越规整，工具推导出的目标名和模块名越不容易出意外 |

## 3.10 下章预告

项目地基打好了，可以开始正经学语言了。下一章从最基础的两位主角讲起：`let` 和 `var`——为什么 Swift 官方风格是"默认用 `let`"、类型推断到底能推多远、以及"整数和浮点之间没有隐式转换"这件事会怎样在第一天就拦住你。
