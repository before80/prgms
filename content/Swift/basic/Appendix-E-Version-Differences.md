+++
title = "附录E 版本差异与易错点清单"
weight = 1040
date = "2026-09-14T22:30:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 附录E：版本差异与易错点清单

> Swift 的语法相对稳定，但并发、所有权和宏仍在快速演进。本附录按“功能线索”整理，不把版本号当考试题；真正重要的是知道你使用的工具链支持哪些特性。

## E.1 重要版本线索

| 版本系列 | 代表能力 |
| --- | --- |
| Swift 5.9 | `if`/`switch` 表达式、宏、参数包、`package` 访问控制 |
| Swift 6.0 | Swift 6 语言模式、严格并发检查、类型化抛出、`sending` |
| Swift 6.2 | Approachable Concurrency、`@concurrent`、`nonisolated(nonsending)`、默认隔离、`InlineArray`/`Span`、`isolated deinit` |
| Swift 6.3 | 工具链与库持续演进，模块选择器等能力可在对应工具链中使用 |

版本号不是目标，项目需要的是：固定工具链、明确语言模式、持续测试升级收益。

## E.2 语言模式与编译设置

| 问题 | 建议 |
| --- | --- |
| 默认语言模式不一定是 6 | 在包清单或 Xcode 中显式设置 |
| 严格并发警告太多 | 先按模块处理，再逐步提升为错误 |
| 旧依赖没有并发标注 | 用 `@preconcurrency import` 隔离风险 |
| UI 目标默认隔离混乱 | 考虑 `.defaultIsolation(MainActor.self)` |

## E.3 常见错误清单

| 错误或现象 | 常见原因 | 章节 |
| --- | --- | --- |
| `invalid UTF-8 found in source file` | 源文件不是 UTF-8（常见于用 GBK 等本地编码保存的文件），注释里的坏字节也算 | 第2章 |
| `input files must be encoded as UTF-8 instead of UTF-16` | 文件被编辑器存成了 UTF-16 | 第2章 |
| `cannot find 'xxx' in scope`，但名字明明一样 | 标识符的 Unicode 写法不同（预组合字符 vs 基字符 + 组合字符） | 第2章 |
| `'nil' cannot initialize specified type` | 给非可选类型赋 `nil` | 第9章 |
| `value of optional type must be unwrapped` | 忘记解包 | 第9章 |
| `type cannot conform to 'Hashable'` | 类型不可哈希却用作集合元素 | 第10、16章 |
| `switch must be exhaustive` | 枚举或分支未穷尽 | 第12、16章 |
| `cannot use mutating member on immutable value` | 对 `let` 值调用 `mutating` 方法 | 第17章 |
| `self used before super.init` | 违反两阶段初始化 | 第20章 |
| `escaping closure captures inout parameter` | 逃逸闭包捕获 `inout` | 第14章 |
| `overlapping accesses to` | 同一变量发生重叠写访问 | 第29章 |
| `actor-isolated property can not be referenced` | 跨隔离域直接访问状态 | 第31章 |
| `task or actor-isolated ... is not Sendable` | 跨域传递了不可安全共享的值 | 第31、32章 |
| `binary operator '==' cannot be applied` | 元组元素过多或类型不可比较 | 第8章 |
| `cannot find type 'TestingMacros'` | 工具链与 tools-version 不匹配 | 第33、34章 |

## E.4 迁移检查清单

- [ ] 固定 Swift 工具链和依赖版本。
- [ ] 把语言模式、并发检查设置写进项目配置。
- [ ] 清理全局可变状态，或将其纳入 actor/`@MainActor`。
- [ ] 为跨域数据补 `Sendable`，优先使用不可变值类型。
- [ ] 审查 `Task`、闭包和委托的生命周期。
- [ ] 用测试覆盖迁移前后的行为。
- [ ] 把 `@unchecked` 和 `nonisolated(unsafe)` 作为待偿还的技术债记录。

## E.5 语法糖的版本线索

写短代码之前，先确认工具链支持哪一版语法。下表只列“写法变短”的里程碑，详细规则见第 15B 章。

| 版本 | 语法糖 |
| --- | --- |
| Swift 5.3 | 多尾随闭包（`load { } onError: { }`） |
| Swift 5.4 | 隐式成员可以继续接成员（`.bold.union(.italic)`） |
| Swift 5.7 | `if let x`、`guard let x` 绑定简写 |
| Swift 5.9 | `if` / `switch` 表达式 |
| Swift 6.1 | 尾随逗号可用于参数列表与实参列表 |
