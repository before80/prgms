+++
title = "第33章 包与工程：SwiftPM 进阶、资源与 C 互操作"
weight = 330
date = "2026-09-14T22:30:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 第三十三章：包与工程：SwiftPM 进阶、资源与 C 互操作

> 一个包能满足“能编译”之外的更多要求：拆分模块、管理资源、声明平台、接入 C 库、发布产品。工程结构没有唯一正确答案，但有清晰和不清晰之分。清晰的边界会让编译更快，也会让错误更早暴露。

## 33.1 一个完整的包清单

一份写满常见字段的 `Package.swift` 长这样，下面逐块拆开看：

```swift
// swift-tools-version: 6.3
import PackageDescription

let package = Package(
    name: "ExpenseKit",
    platforms: [.macOS(.v13), .iOS(.v16)],
    products: [
        .library(name: "ExpenseCore", targets: ["ExpenseCore"]),
        .executable(name: "expense-cli", targets: ["ExpenseCLI"])
    ],
    dependencies: [
        .package(url: "https://github.com/apple/swift-argument-parser.git", from: "1.5.0")
    ],
    targets: [
        .target(name: "ExpenseCore"),
        .executableTarget(
            name: "ExpenseCLI",
            dependencies: ["ExpenseCore", .product(name: "ArgumentParser", package: "swift-argument-parser")]
        ),
        .testTarget(name: "ExpenseCoreTests", dependencies: ["ExpenseCore"])
    ]
)
```

重点不是字段越多越好，而是每个字段都表达真实约束：平台决定 API 可用范围，products 决定别人如何使用你的包，targets 决定模块边界。

## 33.2 依赖与版本解析

SwiftPM 的版本规则：

| 写法 | 含义 |
| --- | --- |
| `.upToNextMajor(from: "1.5.0")` | 允许 1.x，不跨 2.0 |
| `.upToNextMinor(from: "1.5.0")` | 允许 1.5.x，不跨 1.6 |
| `.exact("1.5.0")` | 只能使用精确版本 |
| `.branch("main")` | 跟随分支，不推荐发布 |
| `.revision("abc123")` | 固定提交 |

解析结果记录在 `Package.resolved`，它应该提交到版本库，保证团队和 CI 使用同一组版本。常用命令：

```bash
swift package resolve
swift package update
swift package show-dependencies
swift package dump-package
```

依赖不是越多越好。每加一个包，就多一份升级、兼容和安全维护成本。

## 33.3 资源与本地化

资源要显式声明：

```swift
.target(
    name: "ExpenseCore",
    resources: [
        .process("Resources"),
        .copy("Fixtures/sample.json")
    ]
)
```

访问包内资源使用 `Bundle.module`：

```swift
import Foundation

let url = Bundle.module.url(forResource: "sample", withExtension: "json")
print(url != nil)
// prints: true
```

`.process` 会让 SwiftPM 根据文件类型处理资源（例如编译资产目录），`.copy` 则保持原样复制。资源名冲突时，使用目录结构或显式 `Bundle.module` 查找避免歧义。

## 33.4 模块拆分

常见分层：

```text
Sources/
  ExpenseCore/        // 纯模型与规则
  ExpenseStorage/     // 文件/数据库实现
  ExpenseCLI/         // 命令行入口
```

依赖方向应该单向：入口依赖业务，业务依赖抽象，底层实现依赖抽象。不要让 `ExpenseCore` 反过来导入 `ExpenseCLI`，否则模块只会变成“更慢的文件夹”。

模块边界还能提升增量编译速度：改动一个模块时，只重新编译依赖它的部分。

## 33.5 C 互操作与系统库

Swift 可以直接调用 C。先准备一个 C 目标：

```swift
.target(
    name: "CKit",
    publicHeadersPath: "include"
)
```

目录里放一个头文件和一个实现文件，头文件放在 `publicHeadersPath` 指定的目录下：

```c
// Sources/CKit/include/CKit.h
#include <stdint.h>

int32_t ckit_add(int32_t a, int32_t b);
```

```c
// Sources/CKit/CKit.c
#include "CKit.h"

int32_t ckit_add(int32_t a, int32_t b) { return a + b; }
```

Swift 侧导入模块名即可，调用方式和普通 Swift 函数没有区别：

```swift
import CKit

print(ckit_add(2, 3))
// prints: 5
```

类型会被自动映射：`int32_t` 变成 `Int32`，指针类型变成 `UnsafeMutablePointer` / `UnsafePointer` 家族。名字太“C 味”的接口，可以在 Swift 层包一层更顺眼的包装，而不是让业务代码到处出现下划线函数名。

系统库通过 `.systemLibrary` 声明：

```swift
.systemLibrary(
    name: "CZlib",
    pkgConfig: "zlib",
    providers: [
        .brew(["zlib"]),
        .apt(["zlib1g-dev"])
    ]
)
```

C 互操作要处理指针生命周期、空指针、内存所有权和线程安全。把不安全的边界包成小型 Swift 接口，是比把指针散落到业务代码里更好的做法。

反过来把 Swift 函数暴露给 C，可以使用 `@_cdecl` 指定稳定的 C 符号名：

```swift
@_cdecl("add_numbers")
public func addNumbers(_ a: Int32, _ b: Int32) -> Int32 {
    a + b
}
```

`@_cdecl` 带有下划线，说明它更偏底层且可能随工具链演进；把它限制在桥接层，不要让业务代码直接依赖这类导出。

## 33.6 Swift Build 与构建产物

最新工具链正在推进开源的 Swift Build 构建系统。日常命令不变：

| 命令 | 用途 |
| --- | --- |
| `swift build` | 调试构建 |
| `swift build -c release` | 发布构建 |
| `swift run 目标名` | 运行可执行目标 |
| `swift test` | 运行测试 |
| `swift package clean` | 清理构建产物 |

在 CI 中建议固定工具链版本，并缓存 `.build` 与 `Package.resolved`。不要把本机 `DerivedData`、`.build` 或临时数据库提交进仓库。

## 33.7 延伸：Android 与跨平台

Swift 的跨平台能力仍在快速变化。Android 上可以使用 Swift Android SDK 构建原生库，再通过 JNI 与 Kotlin/Java 互操作。它适合把核心算法或共享业务逻辑放到 Swift 中，而不是把整个 UI 层都强行搬过去。

跨平台前先明确边界：哪些模块是纯 Swift、哪些依赖 Foundation、哪些必须走平台桥接。边界清楚，构建脚本才不会长成一片森林。

## 33.8 本章小结

| 主题 | 关键结论 |
| --- | --- |
| Package.swift | 包清单同时描述产品、依赖、平台和目标 |
| 版本解析 | `Package.resolved` 锁定实际版本 |
| 资源 | 用 `.process`/`.copy` 声明，用 `Bundle.module` 访问 |
| 模块拆分 | 依赖方向应单向，边界越清晰越好 |
| C 互操作 | 支持 C 目标和系统库，但要把不安全边界封装起来 |
| 构建 | 命令简单，CI 中要固定工具链和依赖 |

## 33.9 本章易错点速查

| 易错点 | 正确理解 |
| --- | --- |
| 依赖使用 `branch: "main"` 发布 | 版本不可重复，优先使用稳定版本 |
| 忘记提交 `Package.resolved` | 团队和 CI 可能解析到不同版本 |
| 资源没有声明却直接读取 | 运行时找不到文件 |
| 模块之间互相导入 | 形成循环依赖，拆分失去意义 |
| C 指针生命期超出分配范围 | 会产生悬垂指针和难以复现的崩溃 |
| 把平台差异塞进一个巨大 `#if` | 抽成独立模块或协议实现更容易维护 |

## 33.10 下章预告

工程结构有了，下一步是证明它工作正常。下一章同时讲 Swift Testing 和 XCTest：一个偏现代、表达力强，一个仍然是大量现有项目的主力。测试不是“写完再补”，而是设计的一部分。
