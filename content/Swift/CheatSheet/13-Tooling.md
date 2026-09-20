+++
title = "13 工具链与工程"
linkTitle = "13 工具链"
weight = 130
date = "2026-09-16T11:00:00+08:00"
type = "docs"
description = "swift / swiftc / SwiftPM 命令表、Package.swift 模板、Swift Testing 与条件编译"
isCJKLanguage = true
draft = false
+++

# 13 工具链与工程

## 命令行速查

| 命令 | 作用 |
| --- | --- |
| `swift --version` | 看工具链版本 |
| `swift file.swift` | 直接解释执行一个文件 |
| `swift -e 'print(1)'` | 执行一行代码 |
| `swift repl` | 交互式环境 🔥 |
| `swiftc file.swift -o app` | 编译成可执行文件 |
| `swiftc -typecheck file.swift` | 只做类型检查，最快 ✨ |
| `swiftc -O file.swift -o app` | 优化构建 |
| `swift build` | 构建 SwiftPM 包 |
| `swift build -c release` | 发布配置构建 |
| `swift run` | 构建并运行可执行产品 |
| `swift test` | 跑测试 |
| `swift test --filter Name` | 只跑匹配的测试 |
| `swift package init --type executable` | 新建可执行包 |
| `swift package resolve` | 解析依赖并写入 `Package.resolved` |
| `swift package update` | 把依赖更新到允许的最新版 |
| `swift package describe` | 打印包的目录与目标结构 |
| `swift package dump-package` | 以 JSON 打印解析后的清单，排查配置问题很好用 |
| `swift package show-dependencies` | 打印依赖树，看清每个依赖是从哪来的 |
| `swift package dump-symbol-graph` | 导出模块的 API 符号图，文档工具用得上 🝖 |
| `swift package add-dependency <url>` | 直接用命令改清单加依赖，不用手写 `.package(...)` 🆕 |
| `swift package add-target <名字>` | 加一个目标（还有 `add-product`、`add-setting`） |
| `swift package tools-version --set 6.2` | 改清单里的 `swift-tools-version` |
| `swift package archive-source` | 打包源码 zip，发布或存档用 |
| `swift package compute-checksum <文件>` | 算二进制依赖的校验和 |
| `swift package clean` | 清掉构建产物 |
| `swift package reset` | 连缓存一起清，构建"玄学问题"的最后一招 |
| `swift demangle` | 把 `$s4main3fooyyF` 这类符号名还原成 `main.foo() -> ()`，读崩溃日志用 🔥 |
| `swift format` | 官方格式化/风格检查工具，已随工具链提供，见下 |

### 透传编译参数

SwiftPM 自己不认识的参数，用 `-X` 前缀透传给下一层：

| 参数 | 透传给 |
| --- | --- |
| `-Xswiftc -Ounchecked` | Swift 编译器 |
| `-Xcc -DDEBUG` | C 编译器 |
| `-Xlinker -lz` | 链接器 |
| `-Xcxx -std=c++20` | C++ 编译器 |

```console
$ swift build -Xswiftc -warnings-as-errors -Xswiftc -strict-concurrency=complete
```

### 运行期检查

```console
$ swift test --sanitize=thread     # 抓数据竞争
$ swift test --sanitize=address    # 抓越界与释放后使用
$ swift test --sanitize=undefined  # 抓未定义行为
```

### 代码风格与文档

```console
$ swift format --in-place --recursive Sources Tests    # 官方格式化，直接改文件
$ swift format lint --recursive Sources                # 只检查、报告问题
$ swift format dump-configuration > .swift-format      # 生成配置模板再按需改
$ swiftlint --strict                                  # 第三方静态检查（需另装）
$ swift test --enable-code-coverage                    # 跑测试并收集覆盖率
$ swift test --show-code-coverage-path                 # 打印覆盖率 JSON 的路径
```

| 工具 | 从哪来 | 干什么 |
| --- | --- | --- |
| `swift format` | **随工具链**（就是 swift-format） | 格式化 + `lint`，规则写在 `.swift-format` 里 🔥 |
| [SwiftLint](https://github.com/realm/SwiftLint) | `brew install swiftlint` | 社区规则集，抓强制解包、命名、复杂度这类问题 |
| [DocC](https://github.com/swiftlang/swift-docc-plugin) | 作为**依赖**加进包 | 把 `///` 注释变成可浏览的文档 |

⚠️ **DocC 不是 SwiftPM 内置子命令。** 实测 `swift package --help` 的子命令列表里没有 `generate-documentation` / `preview-documentation`——它们是 swift-docc-plugin 提供的插件命令，得先往 `Package.swift` 里加依赖，之后才有：

```console
$ swift package generate-documentation --target MyLib
$ swift package preview-documentation --target MyLib
```

🔥 并发代码写完后跑一次 `--sanitize=thread`。它抓到的都是真问题，而且比线上复现便宜一万倍。

## 命令行程序常用 API

写一个能跑的工具，绕不开这四件事：拿参数、读环境、碰文件、往外报错。它们**基本都在 `Foundation` 里**，只有一个例外：

| 需求 | 写法 |
| --- | --- |
| 参数列表 | `CommandLine.arguments` → `[String]`，第 0 个是可执行文件路径（**标准库**，不用 import） |
| 参数个数 | `CommandLine.argc`（同样在标准库） |
| 环境变量 | `ProcessInfo.processInfo.environment["KEY"]` → `String?` |
| 进程名 / 系统版本 | `ProcessInfo.processInfo.processName`、`operatingSystemVersionString` |
| 临时目录 | `FileManager.default.temporaryDirectory` |
| 目录是否存在 | `FileManager.default.fileExists(atPath:)` |
| 列目录 | `FileManager.default.contentsOfDirectory(atPath:)` |
| 读文件 | `try String(contentsOf: url, encoding: .utf8)` |
| 写文件 | `try text.write(to: url, atomically: true, encoding: .utf8)` |
| 标准错误 | `FileHandle.standardError.write(Data("...".utf8))` |
| 正常 / 异常退出码 | `EXIT_SUCCESS` / `EXIT_FAILURE`，配合 `exit()` |

⚠️ **`CommandLine` 在标准库，不在 Foundation**，所以下面的代码即使一行 `import` 都不写也能编译；而 `ProcessInfo`、`FileManager`、`FileHandle` 必须 `import Foundation`，否则报 `cannot find 'ProcessInfo' in scope`。

```swift
import Foundation

// 参数取决于你怎么调用（argv[0] 是可执行文件路径），这里只确认它拿得到
let args: [String] = CommandLine.arguments
print(args.isEmpty)
// prints: false

// 环境变量是一个 [String: String]
print(ProcessInfo.processInfo.environment["HOME"]?.hasPrefix("/") ?? false)
// prints: true

// 临时目录 + 读写文件都走 URL
let tmp = FileManager.default.temporaryDirectory.appendingPathComponent("demo.txt")
try "你好".write(to: tmp, atomically: true, encoding: .utf8)
print(try String(contentsOf: tmp, encoding: .utf8))
// prints: 你好
print(FileManager.default.fileExists(atPath: tmp.path))
// prints: true

FileHandle.standardError.write(Data("出错啦\n".utf8))   // 走 stderr，不会被管道当数据收走
```

⚠️ 三个容易忽略的细节：

1. **`try` 写在哪里。** 上面 `try "你好".write(...)` 里 `try` 管的是整个表达式，别写成 `"你好".write(...)` 才发现忘了——编译器会直接拦住你。
2. **标准输出别用来报错。** 工具的输出经常被 `>` 或管道接走，诊断信息走 `FileHandle.standardError` 才不会被当成数据。
3. **临时目录是"系统清理时会删"的地方**，别拿它存要留的文件；要长期保存就写到 `FileManager.default.urls(for:in:)` 给出的用户目录里。

💭 调试时还有一个顺手的小工具：`readLine()` 从标准输入读一行（返回 `String?`），交互式小脚本里比折腾 `FileHandle` 省事得多。

## 包的结构

```text
MyTool/
├── Package.swift            # 清单，唯一的配置入口
├── Package.resolved         # 依赖锁文件，建议提交到版本控制
├── Sources/
│   ├── MyTool/              # 可执行目标（与 target 同名）
│   │   └── main.swift       # 入口，或者用 @main
│   └── MyLib/               # 库目标
│       └── MyLib.swift
├── Tests/
│   └── MyLibTests/
│       └── MyLibTests.swift
└── .build/                  # 构建产物，别提交
```

| 文件 / 目录 | 说明 |
| --- | --- |
| `Package.swift` | 包名、平台、产品、依赖、目标 |
| `Package.resolved` | 锁定的依赖版本；应用建议提交，库可以不提交 |
| `Sources/<Target>/` | 目标源码，目录名必须与 target 名一致 |
| `Tests/<Target>Tests/` | 测试目标 |
| `.build/` | 中间产物与缓存，加入 `.gitignore` |
| `Plugins/` | 命令插件与构建插件 🝖 |

## Package.swift 模板

{{< tabpane text=true persist=disabled >}}

{{% tab header="库" %}}

```swift
// swift-tools-version: 6.2
import PackageDescription

let package = Package(
    name: "MyLib",
    platforms: [.macOS(.v15), .iOS(.v18)],
    products: [
        .library(name: "MyLib", targets: ["MyLib"]),
    ],
    targets: [
        .target(name: "MyLib"),
        .testTarget(name: "MyLibTests", dependencies: ["MyLib"]),
    ]
)
```

{{% /tab %}}

{{% tab header="可执行程序" %}}

```swift
// swift-tools-version: 6.2
import PackageDescription

let package = Package(
    name: "MyTool",
    platforms: [.macOS(.v15)],
    dependencies: [
        .package(url: "https://github.com/apple/swift-argument-parser.git", from: "1.5.0"),
    ],
    targets: [
        .executableTarget(
            name: "MyTool",
            dependencies: [
                .product(name: "ArgumentParser", package: "swift-argument-parser"),
            ]
        ),
        .testTarget(name: "MyToolTests", dependencies: ["MyTool"]),
    ]
)
```

{{% /tab %}}

{{% tab header="多目标与编译设置" %}}

```swift
// swift-tools-version: 6.2
import PackageDescription

let package = Package(
    name: "App",
    targets: [
        .target(
            name: "Core",
            swiftSettings: [
                .swiftLanguageMode(.v6),
                .enableUpcomingFeature("ExistentialAny"),
                .define("DEBUG", .when(configuration: .debug)),
            ]
        ),
        .target(name: "UI", dependencies: ["Core"]),
        .target(name: "Features", dependencies: ["Core"]),
        .executableTarget(name: "App", dependencies: ["UI", "Features"]),
    ]
)
```

⚠️ target 之间必须**显式声明依赖**。`UI` 里想 `import Core`，就得在 `dependencies` 里写明；写漏了编译器会告诉你 "no such module"。

{{% /tab %}}

{{% tab header="条件依赖" %}}

```swift
// swift-tools-version: 6.2
import PackageDescription

let package = Package(
    name: "Cross",
    dependencies: [
        .package(url: "https://github.com/apple/swift-log.git", from: "1.6.0"),
    ],
    targets: [
        .target(
            name: "Cross",
            dependencies: [
                .product(
                    name: "Logging",
                    package: "swift-log",
                    condition: .when(platforms: [.linux])
                ),
            ]
        ),
    ]
)
```

条件依赖让同一份清单在 Apple 平台与 Linux 上用不同实现，是跨平台库的常见手法。

{{% /tab %}}

{{< /tabpane >}}

## 测试

Swift 6 时代有两个测试框架：官方的 **Swift Testing** 与老牌的 **XCTest**。新代码默认用前者。

{{< tabpane text=true persist=disabled >}}

{{% tab header="Swift Testing（推荐）" %}}

```swift
import Testing
@testable import MyLib

@Test func additionWorks() {
    #expect(1 + 1 == 2)
}

@Test("解析合法输入")
func parseValid() throws {
    let value = try #require(Int("42"))
    #expect(value == 42)
}

@Test(arguments: [1, 2, 3])
func positive(n: Int) {
    #expect(n > 0)
}

@Suite("分组示例")
struct GroupTests {
    @Test func insideGroup() { #expect(true) }
}
```

| 写法 | 作用 |
| --- | --- |
| `@Test` | 标记一个测试函数（可以是自由函数，不必继承任何类） |
| `@Test("说明")` | 给测试加显示名 |
| `@Test(arguments:)` | 参数化，一次跑多组数据 🔥 |
| `@Suite` | 给测试分组 |
| `#expect(...)` | 断言，失败时输出表达式两边的值 |
| `try #require(...)` | 断言并解包，失败立刻中止这个测试 |
| `.tags(...)` | 打标签，按标签筛选运行 |

跑起来大致长这样（真的输出还会多几行版本号与耗时）：

```text
◇ Test run started.
◇ Suite "分组示例" started.
◇ Test additionWorks() started.
✔ Test additionWorks() passed after 0.001 seconds.
✔ Test run with 4 tests in 1 suite passed after 0.001 seconds.
```

🚧 两个测试框架都随工具链提供：装了完整 Xcode 才有 `TestingMacros` 插件与 `XCTest` 框架，只装 Command Line Tools 时 `import Testing` 会找不到模块。

{{% /tab %}}

{{% tab header="XCTest（老项目）" %}}

```swift
import XCTest
@testable import MyLib

final class MyLibTests: XCTestCase {
    func testAddition() {
        XCTAssertEqual(1 + 1, 2)
    }

    func testThrowing() throws {
        let value = try XCTUnwrap(Int("42"))
        XCTAssertEqual(value, 42)
    }

    func testAsync() async throws {
        let result = await fetchSomething()
        XCTAssertNotNil(result)
    }
}
```

| 断言 | 作用 |
| --- | --- |
| `XCTAssertEqual` / `XCTAssertNotEqual` | 相等比较 |
| `XCTAssertTrue` / `XCTAssertFalse` | 真假 |
| `XCTAssertNil` / `XCTAssertNotNil` | 可选值 |
| `XCTAssertThrowsError` | 期望抛错 |
| `XCTUnwrap` | 解包并断言非空 |
| `XCTSkip` | 主动跳过 |

🚧 UI 测试与性能测试目前仍是 XCTest 的地盘；纯逻辑测试建议迁到 Swift Testing。

{{% /tab %}}

{{< /tabpane >}}

## 条件编译与可用性

```swift
#if os(macOS) || os(iOS)
    import Darwin
#elseif os(Linux)
    import Glibc
#endif

#if canImport(FoundationNetworking)
    import FoundationNetworking      // Linux 上网络相关 API 单独成模块
#endif

#if DEBUG
    print("调试构建")
#endif
```

| 条件 | 判断什么 |
| --- | --- |
| `os(macOS)` `os(iOS)` `os(Linux)` | 目标操作系统 |
| `arch(arm64)` `arch(x86_64)` | CPU 架构 |
| `swift(>=6.0)` | **语言模式**，不是工具链版本 |
| `compiler(>=6.0)` | 编译器（工具链）版本 |
| `canImport(Module)` | 该模块能否导入 |
| `targetEnvironment(simulator)` | 是否模拟器 |
| `DEBUG` | 由 `-Xswiftc -DDEBUG` 之类的自定义标志决定 |

```swift
if #available(macOS 26, iOS 26, *) {
    // 新 API
} else {
    // 兼容实现
}

@available(macOS 26, *)
func onlyOnNewOS() { }

@available(*, deprecated, message: "改用 newAPI()")
func oldAPI() { }
```

| 用法 | 含义 |
| --- | --- |
| `if #available(...)` | 运行期分支 |
| `if #unavailable(...)` | 反向判断，写"系统太老"的兼容分支更直白（Swift 5.6 起） |
| `guard #available(...) else { return }` | 前置检查 |
| `@available(...)` | 标注声明的可用范围 |
| `@available(*, unavailable)` | 彻底禁止使用 |
| `@available(*, deprecated, renamed:)` | 给出替代建议 |
| `@available(*, noasync)` | 禁止在异步上下文使用 🝖 |

## 调试与性能

| 工具 | 用途 |
| --- | --- |
| `swiftc -typecheck` | 最快地检查语法与类型 |
| `-Xswiftc -warnings-as-errors` | 让警告变成错误，CI 上必备 |
| `swift test --sanitize=thread` | 数据竞争检测 |
| `swift build --sanitize=address` | 内存问题检测 |
| **Instruments** | macOS / iOS 性能与内存分析 |
| **Xcode 的 Memory Graph** | 一眼看出循环引用与泄漏 |
| `swift package diagnose-api-breaking-changes` | 检查 API 破坏性变更 |

⚠️ 别把 `-typecheck` 当"完整编译的快速版"：它只跑到类型检查就收工，少数诊断要再往后走一步才会报（例如逃逸闭包捕获 `inout` 参数的 `escaping closure captures 'inout' parameter 'x'`，`swiftc -typecheck` 一路绿灯，真的编一次才报）。拿它换即时反馈没问题，发版前那把关还是得跑完整编译。

💭 性能优化的正确顺序：先量，再改，改完再量。没有测量数据的优化，基本等于在给代码加复杂度。

## 官方资源

| 资料 | 链接 |
| --- | --- |
| Swift 官网 | [swift.org](https://www.swift.org/) |
| 语言指南 | [docs.swift.org/swift-book](https://docs.swift.org/swift-book/) |
| 标准库文档 | [developer.apple.com/documentation/swift](https://developer.apple.com/documentation/swift) |
| Swift Evolution 提案 | [swift-evolution](https://github.com/swiftlang/swift-evolution/tree/main/proposals) |
| SwiftPM 文档 | [docs.swift.org/packagemanagerdocs](https://docs.swift.org/packagemanagerdocs/) |
| Swift Testing | [developer.apple.com/documentation/testing](https://developer.apple.com/documentation/testing) |
| 官方包索引 | [swiftpackageindex.com](https://swiftpackageindex.com/) |
| swift-format | [swiftlang/swift-format](https://github.com/swiftlang/swift-format) |
| SwiftLint | [realm/SwiftLint](https://github.com/realm/SwiftLint) |

## 陷阱速查

| 陷阱 | 说明 |
| --- | --- |
| 把 `.build/` 提交进仓库 | 体积大且会互相污染 |
| 忘记提交 `Package.resolved` | 依赖版本漂移，CI 上与本地结果不一致 |
| 平台要求没写进 `platforms` | 用了新 API 却在低版本上编译失败 |
| target 依赖写漏 | 报 "no such module" |
| 把 `swift(>=6.0)` 当工具链版本用 | 它判断的是语言模式，工具链要用 `compiler(>=)` |
| 只在 debug 下测性能 | debug 没开优化，数字没有参考价值 |
| 用 `print` 做日志 | 用 `os.Logger` / `swift-log`，可分级、可过滤 |
| 把 `swift package reset` 当日常命令 | 它会清空整个缓存，只在卡住时用 |
