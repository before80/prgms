+++
title = "4.2 创建模块映射"
date = 2026-09-11T21:45:00+08:00
weight = 2
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++


> 原文链接: [https://docs.swift.org/latest/documentation/packagemanagerdocs/modulemaps/](https://docs.swift.org/latest/documentation/packagemanagerdocs/modulemaps/)

# 4.2 创建模块映射

为系统库目标、预编译库或 C 语言目标定义 C 和 C++ 头文件如何暴露给 Swift。

## 概述 {#Overview}

模块映射在 C、C++ 库与 Swift 代码之间架起桥梁。它们定义 Clang 模块系统如何组织头文件，以便 Swift 能够导入这些头文件。当你为了在 Swift Package Manager 中使用而包装一个 C 库时，你要创建一个模块映射来描述该库的公共接口。

在下列情况下需要创建模块映射：

- 为 Swift Package Manager 包装一个 C 或 C++ 库。
- 定义一个引用预安装库的系统库目标。
- 在 artifact bundle 中打包一个二进制库。
- 需要控制 Swift 可以导入哪些头文件。

当 Swift Package Manager 找到你的模块映射时，会自动配置构建系统：

- 把模块映射加入编译器搜索路径。
- 配置头文件包含目录。
- 链接模块映射中指定的二进制库。
- 从 artifact bundle 中选择平台特定的变体。

你不需要手动配置编译器标志或搜索路径。

本文介绍如何为你正在包装的库创建模块映射。完整的语法细节参见[模块映射语法参考](4.2.1-ModuleMapReference/)。要诊断导入失败和编译错误，参见[调试模块映射](4.2.2-DebuggingModuleMaps/)。

### 创建一个基本模块映射 {#Create-a-basic-module-map}

为了演示如何创建模块映射，这个例子从一个只暴露单个头文件的简单模块映射开始。

在你的库的 include 目录中创建一个名为 `module.modulemap` 的文件：

```
module MyLibrary {
    header "MyLibrary.h"
    export *
}
```

这个模块映射定义了一个名为 `MyLibrary` 的模块，它包含一个头文件。`export *` 指令让该头文件中的所有符号都对导入该模块的代码可用。

#### 头文件使用相对路径 {#Use-relative-paths-for-headers}

头文件路径要相对于模块映射文件所在的位置来指定。如果你的模块映射位于 `include/module.modulemap`，那么 `header "MyLibrary.h"` 这条头文件指令查找的就是 `include/MyLibrary.h`。

引用头文件时不要使用绝对路径或父目录引用（`../`）。相对路径能确保你的模块映射在不同的系统和构建配置下都能工作。

#### 让模块名与产物名一致 {#Match-the-module-name-to-your-artifact}

模块映射中的模块名必须与 Swift Package Manager 中的产物名一致。如果你的 Package.swift 定义了一个名为 `MyLibrary` 的二进制目标，那么你的模块映射必须声明 `module MyLibrary`。

在 Swift 中使用模块映射里暴露的函数时，你通过 `import` 来访问它们。对于上面的例子，用下面这行来访问你在模块映射中暴露的 C 函数：

```swift
import MyLibrary
```

### 为 C++ 创建模块映射 {#Create-a-module-map-for-C++}

C++ 库需要额外一条指令来启用 C++ 语言支持。在你的模块映射中加入 `requires cplusplus` 指令：

```
module MyCppLibrary {
    header "MyCppLibrary.h"
    requires cplusplus
    export *
}
```

没有这条指令的话，编译器会把该头文件当作 C 代码处理，遇到 C++ 语法时就会报错。

你还可以要求特定的 C++ 标准版本：

```
module ModernCppLibrary {
    header "ModernCppLibrary.h"
    requires cplusplus11
    export *
}
```

用 `cplusplus11` 表示 C++11 或更高版本。如果构建时没有启用所要求的 C++ 标准，编译器会拒绝该模块。

### 用伞形头文件组织多个头文件 {#Organize-multiple-headers-with-umbrella-headers}

当你的库有多个头文件时，用伞形头文件把它们全部包含进来。

创建一个主头文件，在其中包含其他头文件：

```c
// MyLibrary.h
#ifndef MYLIBRARY_H
#define MYLIBRARY_H

#include "Core.h"
#include "Utils.h"
#include "Types.h"

#endif
```

然后在模块映射中用 `umbrella header` 指令引用它：

```
module MyLibrary {
    umbrella header "MyLibrary.h"
    export *
}
```

对于拥有多个公共头文件的库来说，伞形头文件模式很常见。它提供了访问全部功能的单一入口，并清晰地定义了公共 API。

### 标记系统库 {#Mark-system-libraries}

在包装系统库（系统内置或预安装的库）时，要加上 `[system]` 属性：

```
module SystemLib [system] {
    header "systemlib.h"
    link "systemlib"
    export *
}
```

`[system]` 属性确保本地构建与客户端构建的行为一致。它会影响 Swift 导入某些 Objective-C 类型的方式，尤其是 `NSUInteger`——对系统模块它映射为 `Int`，对非系统模块则映射为 `UInt`。

### 链接二进制库 {#Link-binary-libraries}

用 `link` 指令指定链接器应当包含的库：

```
module ZLib [system] {
    header "zlib.h"
    link "z"
    export *
}
```

Swift Package Manager 会自动把这些信息传给链接器。库名不要带 `lib` 前缀和文件扩展名。例如，对 `libz.a` 或 `libz.dylib` 写 `"z"`。

### 为系统库目标添加模块映射 {#Add-a-module-map-to-a-system-library-target}

当你包装的库需要用户在自己的系统上单独安装时，请创建系统库目标。暴露系统库的常见约定是在库名前加上 `C` 前缀。这样你就可以创建一个以该 C 库命名的 Swift 模块，由它提供更符合 Swift 习惯的接口。

#### 创建目标目录 {#Create-the-target-directory}

在包的根目录中为你的系统库目标创建一个目录：

```bash
mkdir -p SystemLibraries/CSystemLib
```

#### 创建模块映射文件 {#Create-the-module-map-file}

在该目标目录中添加一个 `module.modulemap` 文件：

```
module CSystemLib [system] {
    header "shim.h"
    link "systemlib"
    export *
}
```

#### 创建垫片头文件 {#Create-a-shim-header}

添加一个垫片（shim）头文件，由它包含真正的系统头文件：

```c
// shim.h
#include <systemlib.h>
```

垫片头文件让编译器能够通过搜索路径找到真正的头文件，从而避免硬编码绝对路径破坏可移植性。

#### 声明目标 {#Declare-the-target}

在你的 Package.swift 中添加系统库目标：

```swift
.systemLibrary(
    name: "CSystemLib",
    pkgConfig: "systemlib",
    providers: [
        .apt(["libsystemlib-dev"]),
        .brew(["systemlib"])
    ]
)
```

构建你的包的用户需要先安装该库。包管理器会用 `pkg-config` 定位该库并配置搜索路径。
