+++
title = "第三篇 自定义类型与抽象"
weight = 30
date = "2026-09-14T22:30:00+08:00"
type = "docs"
description = "枚举、结构体、类、属性、初始化、扩展、协议、泛型、类型系统补全、宏"
isCJKLanguage = true
draft = false
+++

# 第三篇：自定义类型与抽象

> 语言主干让你会读代码，这一篇让你会设计类型。

Swift 的类型工具箱里，枚举、结构体、类各司其职：枚举表达“有限种可能”，结构体表达“一份不会被人偷偷改掉的数据”，类表达“有身份、可共享、有生命周期”。先把这个选择想清楚，再谈协议和泛型——它们负责把能力从具体类型里抽出来。

这一篇的最后三章是“补齐与深水区”：类型系统里零碎但关键的拼图（存在类型、元类型、键路径、反射、字面量协议）、访问控制与条件编译，以及宏。宏那章配了一个三文件、能真跑起来的最小例子，别只读不跑。

## 本篇章节

1. [枚举]({{< relref "Chapter-16-Enumerations.md" >}})
2. [结构体与值语义]({{< relref "Chapter-17-Structures-and-Value-Semantics.md" >}})
3. [类与继承]({{< relref "Chapter-18-Classes-and-Inheritance.md" >}})
4. [属性、方法与下标]({{< relref "Chapter-19-Properties-Methods-and-Subscripts.md" >}})
5. [初始化与反初始化]({{< relref "Chapter-20-Initialization-and-Deinitialization.md" >}})
6. [扩展与嵌套类型]({{< relref "Chapter-21-Extensions-and-Nested-Types.md" >}})
7. [协议]({{< relref "Chapter-22-Protocols.md" >}})
8. [泛型]({{< relref "Chapter-23-Generics.md" >}})
9. [类型系统补全]({{< relref "Chapter-24-Type-System-Toolbox.md" >}})
10. [访问控制、模块与条件编译]({{< relref "Chapter-25-Access-Control-Modules-and-Conditional-Compilation.md" >}})
11. [宏]({{< relref "Chapter-26-Macros.md" >}})

## 读完你应该能

- 面对一个建模问题，说得出该用枚举、结构体还是类，并讲清理由。
- 正确使用 `init?`、两阶段初始化、`deinit` 和 `isolated deinit`。
- 用协议 + 泛型写出既通用又类型安全的接口，并知道 `some` 和 `any` 该选谁。
- 看懂 `@` 属性与 `#` 指令在做什么，必要时自己写一个最小宏。
