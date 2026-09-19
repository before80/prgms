+++
title = "附录B 标准库与 Foundation 的分界"
weight = 1010
date = "2026-09-14T22:30:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 附录B：标准库与 Foundation 的分界

> 很多错误不是语法错误，而是“这个 API 到底属于谁”。标准库提供语言最核心的类型和算法，Foundation 提供日期、文件、网络、格式化等系统能力。分清边界，能让你写出更可移植、依赖更清楚的代码。

## B.1 标准库常见内容

不需要额外导入即可使用：

| 类别 | 例子 |
| --- | --- |
| 基础类型 | `Int`、`Double`、`Bool`、`String`、`Character` |
| 集合 | `Array`、`Dictionary`、`Set`、`Collection`、`Sequence` |
| 可选值 | `Optional`、`Result` |
| 错误 | `Error`、`Never` |
| 并发 | `Task`、`AsyncSequence`、`actor`、`Sendable` |
| 内存与所有权 | `Span`、`InlineArray`、`~Copyable` |
| 协议 | `Equatable`、`Hashable`、`Comparable`、`Codable` 相关协议 |

`Codable`、`Equatable`、`Hashable` 这些协议虽然常用，但具体编码器和解码器通常由 Foundation 或其他库提供。

## B.2 Foundation 提供什么

`import Foundation` 后常见能力：

| 类别 | 例子 |
| --- | --- |
| 日期与时间 | `Date`、`Calendar`、`TimeZone`、`DateFormatter` |
| 文件系统 | `FileManager`、`URL`、`Data` |
| JSON | `JSONEncoder`、`JSONDecoder` |
| 数字处理 | `Decimal`、`Measurement` |
| 字符串与格式化 | `NumberFormatter`、`String(format:)` |
| 网络基础 | `URLSession`、`URLRequest` |
| 线程与锁 | `DispatchQueue`、`OperationQueue`、`Lock` |
| 国际化和本地化 | `Locale`、`DateComponents` |

Foundation 在新平台上有 Swift 原生实现和 CoreFoundation 桥接两套路径。跨平台代码要留意某些 API 在 Linux 或 Windows 上不可用。

## B.3 选择原则

- 能用标准库表达，就不要引入 Foundation。
- 数据模型优先使用纯 Swift 类型，格式化放到边界层。
- 时间计算尽量用 `Calendar` 和 `DateComponents`，不要手工加减秒数。
- 货币使用 `Decimal`，不要用 `Double` 表示金额。
- 文件、网络和系统 API 集中封装，避免散落在业务代码里。

## B.4 本章小结

| 问题 | 优先选择 |
| --- | --- |
| 数组、字符串、可选值 | 标准库 |
| 日期、文件、JSON | Foundation |
| 跨平台纯逻辑 | 标准库 + 自定义协议 |
| 平台格式化 | 边界层使用 Foundation |
| 金额 | `Decimal` |
