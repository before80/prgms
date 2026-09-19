+++
title = "附录C @ 属性与 # 指令速查"
weight = 1020
date = "2026-09-14T22:30:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 附录C：`@` 属性与 `#` 指令速查

> `@` 通常修饰声明，`#` 通常出现在表达式、编译控制或编译期字面量中。两者都会影响编译器行为，但作用时机和适用位置不同。

## C.1 常用 `@` 属性

| 属性 | 作用 | 示例 |
| --- | --- | --- |
| `@available` | 声明可用性 | `@available(macOS 13, *)` |
| `@autoclosure` | 表达式自动包装为闭包 | `func log(_ message: @autoclosure () -> String)` |
| `@backDeployed` | 回部署到旧系统 | 库兼容 |
| `@concurrent` | 要求并发执行 | `@concurrent func work() async` |
| `@discardableResult` | 允许忽略返回值 | 保存、打印类函数 |
| `@dynamicCallable` | 动态调用语法 | 脚本桥接 |
| `@dynamicMemberLookup` | 动态成员查找 | JSON 包装 |
| `@escaping` | 闭包可逃逸 | 保存回调 |
| `@frozen` | 冻结枚举或结构体 ABI | 库演化 |
| `@globalActor` | 自定义全局 actor | `@MyActor` |
| `@inlinable` | 跨模块内联 | 公共热路径 |
| `@inline` | 强制或禁止内联 | `@inline(never)`、`@inline(always)`、`@inline(__always)` |
| `@MainActor` | 主 actor 隔离 | UI 状态 |
| `@nonobjc` | 不暴露给 Objective-C | 兼容层 |
| `@objc` | 暴露给 Objective-C | 选择器、旧框架 |
| `@preconcurrency` | 兼容旧并发标注 | 迁移 |
| `@propertyWrapper` | 属性包装器 | `@Clamped` |
| `@resultBuilder` | 结果构建器 | SwiftUI、DSL |
| `@ViewBuilder` | SwiftUI 提供的结果构建器，让块里能写 `if` / `switch` / `ForEach` | 视图声明（第 15B.18 节） |
| `@retroactive` | 显式追溯性协议遵循 | 扩展外部类型 |
| `@Sendable` | 可安全跨隔离域 | 并发闭包 |
| `@testable` | 测试导入 | `@testable import App` |
| `@unchecked` | 关闭部分检查 | `@unchecked Sendable` |
| `@usableFromInline` | 允许内联代码引用 | 库内部优化 |
| `@warn_unqualified_access` | 未限定访问时警告 | 避免同名成员混淆 |

## C.2 编译控制与字面量

| 指令 | 用途 |
| --- | --- |
| `#if` / `#elseif` / `#else` / `#endif` | 条件编译 |
| `#available` | 运行时可用性判断 |
| `#unavailable` | 不可用性判断 |
| `#warning` | 编译警告 |
| `#error` | 编译错误 |
| `#sourceLocation` | 临时调整源码位置 |
| `#selector` | Objective-C 选择器 |
| `#keyPath` | 旧式键路径字符串 |

## C.3 编译期字面量

| 字面量 | 内容 |
| --- | --- |
| `#file` | 模块名 + 文件名（Swift 6 模式下与 `#fileID` 相同，详见 2.6） |
| `#fileID` | 模块和文件名 |
| `#filePath` | 完整文件路径 |
| `#line` | 行号 |
| `#column` | 列号 |
| `#function` | 函数名 |
| `#dsohandle` | 动态共享对象句柄 |

## C.4 宏相关

| 名称 | 用途 |
| --- | --- |
| `#externalMacro` | 指向宏实现 |
| `#Preview` | 生成 SwiftUI 预览 |
| `#expect` / `#require` | Swift Testing 断言 |

## C.5 使用原则

- 不要因为属性“看起来高级”就随手添加。
- 能用普通语法表达的，优先普通语法。
- 属性一旦进入公共 API，可能影响二进制兼容性。
- `@preconcurrency`、`@unchecked Sendable` 和 `nonisolated(unsafe)` 属于迁移工具，不是长期解决方案。
