+++
title = "3.1 为 Swift 包添加依赖"
date = 2026-09-11T21:45:00+08:00
weight = 1
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++


> 原文链接: [https://docs.swift.org/latest/documentation/packagemanagerdocs/addingdependencies/](https://docs.swift.org/latest/documentation/packagemanagerdocs/addingdependencies/)

# 3.1 为 Swift 包添加依赖

在你的包中使用其他 Swift 包、系统库或二进制依赖。

## 概述 {#Overview}

要依赖另一个 Swift 包，先定义一个依赖；如果它是远程依赖，还要定义对它版本的要求，然后把这个依赖的某个产品添加到你的一或多个目标中。

远程依赖需要一个位置（用 URL 表示），以及一条关于包管理器可以使用哪些版本的要求。

下面的例子展示了一个依赖 [PlayingCard](https://github.com/apple/example-package-playingcard) 的包，它用 `from` 要求版本至少为 `4.0.0`，并允许在依赖解析时使用直到下一个主版本之前的任何可用版本。然后它把产品 `PlayingCard` 用作目标 `MyPackage` 的依赖：

```swift
// swift-tools-version:6.1
import PackageDescription

let package = Package(
    name: "MyPackage",
    dependencies: [
        .package(url: "https://github.com/apple/example-package-playingcard.git", 
                 from: "4.0.0"),
    ],
    targets: [
        .target(
            name: "MyPackage",
            dependencies: [
                .product(name: "PlayingCard", 
                         package: "example-package-playingcard")
            ]
        ),
        .testTarget(
            name: "MyPackageTests",
            dependencies: ["MyPackage"]
        ),
    ]
)
```

当你调用 [swift run](../../swiftcommands/7.7-SwiftRun/) 或 [swift build](../../swiftcommands/7.1-SwiftBuild/) 时，包管理器会自动解析包。你也可以用 [swift package resolve](../../swiftcommands/7.3-SwiftPackageCommands/7.3.3-PackageResolve/) 命令显式解析这些包。关于解析包版本的更多信息，参见[解析与更新依赖](3.1.1-ResolvingPackageVersions/)。

### 约束依赖版本 {#Constraining-dependency-versions}

在声明依赖时约束远程依赖的版本。包管理器使用 git 标签（把它们解释为语义化版本）来识别包的可选版本。

> 注意：包版本的标签应当包含语义化版本的全部三个部分：主版本、次版本和补丁版本。
> 只包含其中一个或两个部分的标签不会被解释为语义化版本。

在声明依赖时使用版本要求，来限制包管理器可以选择的范围。版本要求可以是可能的语义化版本区间、某个具体的语义化版本、分支名或提交哈希。[Package.Dependency](https://docs.swift.org/latest/documentation/packagedescription/package/dependency) 的 API 参考文档中定义了可以使用的各个方法。

### 带特性的包 {#Packages-with-Traits}

特性（trait）随 Swift 6.1 引入，让包可以提供额外的 API，其中可能包含可选的依赖。包应当通过提供特性来给出核心之外的 API。例如，某个包可能提供实验性 API、需要额外依赖的可选 API，或者并不关键、开发者只希望在特定情况下启用的功能。

如果某个包提供了特性，而你依赖它时没有定义要使用的特性，该包就会使用它的默认特性集合。在下面的例子中，依赖 `example-package-playingcard` 使用它的默认特性（如果有的话）：
```swift
dependencies: [
  .package(url: "https://github.com/swiftlang/example-package-playingcard", 
           from: "4.0.0")
]
```

要确定某个包提供了哪些特性（包括默认特性），你可以查看它的 `Package.swift` 清单文件，也可以用 [swift package show-dependencies](../../swiftcommands/7.3-SwiftPackageCommands/7.3.15-PackageShowDependencies/) 打印已解析的依赖及其特性。

启用一个特性应当只会扩充包提供的 API。如果某个包提供了默认特性，你可以在声明依赖时声明一个空的特性集合，从而选择不使用这些特性。下面的依赖声明示例就使用不带任何特性的依赖，即使该包通常会提供一组默认启用的特性：

```swift
dependencies: [
  .package(url: "https://github.com/swiftlang/example-package-playingcard", 
           from: "4.0.0",
           traits: [])
]
```

Swift 包管理器会依据项目中整个依赖图来确定要启用哪些特性。某个依赖被启用的特性，是所有依赖它的包所要求的特性的并集。例如，即使你选择不启用任何特性，但你使用的某个依赖使用了同一个包并启用了某个特性，那么该包仍会以该特性启用的方式使用这个依赖。

> 注意：禁用任何默认特性都可能让你所用依赖中已有的 API 不再可用。

要了解如何提供带特性的包，参见[用特性提供可配置的包](3.1.2-PackageTraits/)。

### 本地依赖 {#Local-Dependencies}

要把本地包用作依赖，可以使用 [package(name:path:)](https://developer.apple.com/documentation/packagedescription/package/dependency/package(name:path:)) 或 [package(path:)](https://developer.apple.com/documentation/packagedescription/package/dependency/package(path:))，用该包的本地路径来定义它。本地依赖不强制版本约束，而是使用你提供的路径上现有的版本。

### 系统库依赖 {#System-Library-Dependencies}

除了依赖 Swift 包，你还可以依赖系统库，或者在 Apple 平台上依赖预编译的二进制依赖。

关于把系统提供的库用作依赖的更多信息，参见[添加对系统库的依赖](3.1.4-AddingSystemLibraryDependency/)。

### Apple 平台的预编译二进制目标 {#Precompiled-Binary-Targets-for-Apple-platforms}

要添加对预编译二进制目标的依赖，在你的目标列表中指定 `.binaryTarget`：可下载的目标使用 [binarytarget(name:url:checksum:)](https://developer.apple.com/documentation/packagedescription/target/binarytarget(name:url:checksum:))，本地二进制文件使用 [binarytarget(name:path:)](https://developer.apple.com/documentation/packagedescription/target/binarytarget(name:path:))。添加二进制目标之后，你就可以把它加入任何其他目标的依赖列表。

关于识别和验证二进制目标的更多信息，参见[识别二进制依赖](https://developer.apple.com/documentation/xcode/identifying-binary-dependencies)。关于创建二进制目标的更多信息，参见[创建多平台二进制框架包](https://developer.apple.com/documentation/xcode/creating-a-multi-platform-binary-framework-bundle)。
